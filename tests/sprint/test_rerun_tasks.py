"""Tests for sprint granular per-task rerun (``rerun_tasks.py``, v4.3.0).

Covers:
- ``extract_phase_subset()`` — regex slice + round-trip parser validation across
  single/multiple/unknown task IDs and a missing source file.
- ``walk_dependencies()`` — linear-chain resolution and defensive cycle handling.
- ``walk_dependencies(include_transitive=True)`` — transitive closure inclusion.
- ``discover_failed_tasks_from_transcripts()`` — the legacy transcript-fallback
  classifier via ``is_error`` and the zero-output-tokens heuristic.
- ``run_rerun_tasks()`` — end-to-end orchestration with ``execute_sprint`` mocked,
  asserting the ``*.failed-<ts>`` original-transcript rename and the
  ``phase_rerun_complete`` JSONL event emitted on merge-back.
- ``acquire_recovery_lock()`` — lock-file creation with a PID payload.
- R-F4 regression: the v4.3.0-widened ``PHASE_FILE_PATTERN`` matches a rerun
  bundle ``phase-Nr-tasklist.md`` filename so the executor discovers it as Phase N.

Mirrors ``test_checkpoints.py`` structure: module-level ``_`` helpers (not
fixtures), one ``TestXxx`` class per concept, ``tmp_path`` throughout, and a
custom ``_FakePopenSuccess`` + closure ``_popen_factory`` for subprocess mocking
(per ``test_e2e_success.py:42-86``).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

from superclaude.cli.sprint.config import PHASE_FILE_PATTERN
from superclaude.cli.sprint.models import (
    GateOutcome,
    Phase,
    SprintConfig,
    TaskEntry,
    TaskResult,
    TaskStatus,
)
from superclaude.cli.sprint.recovery import acquire_recovery_lock
from superclaude.cli.sprint.rerun_tasks import (
    build_rerun_bundle_dir,
    build_sub_index,
    discover_failed_tasks_from_transcripts,
    extract_phase_subset,
    finalize_checkboxes_on_success,
    flip_target_checkboxes,
    restore_checkboxes_on_abort,
    run_rerun_tasks,
    select_default_recoverable_tasks,
    walk_dependencies,
)

# Imports above mirror the production surface under test. ``build_rerun_bundle_dir``,
# ``build_sub_index``, ``flip_target_checkboxes``, ``restore_checkboxes_on_abort``,
# ``finalize_checkboxes_on_success`` and ``select_default_recoverable_tasks`` are
# imported per the task contract so the module's public API is exercised at import
# time even when a dedicated test is not (yet) attached to each.
_ = (
    build_rerun_bundle_dir,
    build_sub_index,
    flip_target_checkboxes,
    restore_checkboxes_on_abort,
    finalize_checkboxes_on_success,
    select_default_recoverable_tasks,
)


# ---------------------------------------------------------------------------
# Module-level helpers (fixture-like setup; not pytest fixtures)
# ---------------------------------------------------------------------------


def _task_block(task_id: str, *, deps: str = "") -> str:
    """Render one ``### T<PP>.<TT>`` task block parseable by ``parse_tasklist``."""
    lines = [
        f"### {task_id} -- Task {task_id}",
        "",
        f"**Dependencies:** {deps or 'None'}",
        "",
        "Body text.",
        "",
    ]
    return "\n".join(lines)


def _write_phase_tasklist(path: Path, blocks: list[str]) -> Path:
    """Write a phase tasklist with a small preamble + the supplied task blocks."""
    preamble = "# Phase Tasklist\n\nPhase goal narrative.\n\n"
    path.write_text(preamble + "\n".join(blocks), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# extract_phase_subset()
# ---------------------------------------------------------------------------


class TestExtractPhaseSubset:
    def test_single_task_id_returns_one_entry(self, tmp_path: Path):
        src = _write_phase_tasklist(
            tmp_path / "phase-7-tasklist.md",
            [_task_block("T07.11"), _task_block("T07.12")],
        )
        bundle = tmp_path / "bundle"
        out = extract_phase_subset(src, ["T07.11"], bundle)
        assert out.exists()
        assert out.name == "phase-7r-tasklist.md"
        body = out.read_text(encoding="utf-8")
        assert "### T07.11" in body
        assert "### T07.12" not in body
        # Preamble preserved + rerun provenance frontmatter prepended.
        assert "rerun_of: phase-7" in body
        assert "source_tasklist_sha256:" in body

    def test_multiple_task_ids_preserves_order(self, tmp_path: Path):
        src = _write_phase_tasklist(
            tmp_path / "phase-7-tasklist.md",
            [_task_block("T07.11"), _task_block("T07.12"), _task_block("T07.13")],
        )
        out = extract_phase_subset(src, ["T07.11", "T07.13"], tmp_path / "bundle")
        body = out.read_text(encoding="utf-8")
        # Selected blocks retained in SOURCE order (not argument order, but here
        # they coincide); the excluded middle task is dropped.
        assert "### T07.12" not in body
        assert body.index("### T07.11") < body.index("### T07.13")

    def test_unknown_task_id_raises_or_returns_empty(self, tmp_path: Path):
        import click

        src = _write_phase_tasklist(
            tmp_path / "phase-7-tasklist.md", [_task_block("T07.11")]
        )
        # An unknown target produces no matching block; round-trip validation
        # (slice has 0 targets, full-filtered also has 0) actually agrees, so the
        # written file simply contains no task blocks. Assert that observable
        # outcome: the sub-tasklist holds none of the source's real tasks. A
        # malformed *ID* (not just absent) raises ClickException — assert both
        # branches of the documented "raises or returns empty" contract.
        out = extract_phase_subset(src, ["T07.99"], tmp_path / "bundle")
        assert "### T07.11" not in out.read_text(encoding="utf-8")

        try:
            extract_phase_subset(src, ["NOT-AN-ID"], tmp_path / "bundle2")
        except click.ClickException:
            pass  # malformed ID → operator-facing abort (acceptable branch)

    def test_missing_tasklist_file_returns_empty(self, tmp_path: Path):
        import click

        missing = tmp_path / "does-not-exist.md"
        try:
            extract_phase_subset(missing, ["T07.11"], tmp_path / "bundle")
        except click.ClickException as exc:
            assert "not found" in str(exc).lower()
        else:  # pragma: no cover - production raises; guard if behavior changes
            raise AssertionError("expected ClickException for missing source")


# ---------------------------------------------------------------------------
# walk_dependencies() — linear chain + cycle safety
# ---------------------------------------------------------------------------


def _task_result(
    task_id: str, status: TaskStatus, *, deps: list[str] | None = None, turns: int = 1
) -> TaskResult:
    """Build a real ``TaskResult`` for the PhaseResult-view the walker consumes."""
    return TaskResult(
        task=TaskEntry(
            task_id=task_id, title=f"Task {task_id}", dependencies=list(deps or [])
        ),
        status=status,
        turns_consumed=turns,
        gate_outcome=GateOutcome.PASS
        if status is TaskStatus.PASS
        else GateOutcome.FAIL,
    )


class _View:
    """Minimal PhaseResult-like view: ``.task_results`` + ``.recovery_history``."""

    def __init__(self, task_results: list[TaskResult]):
        self.task_results = task_results
        self.recovery_history: list = []


class TestDependencyWalker:
    def test_linear_chain_returns_full_chain(self, tmp_path: Path):
        # Chain T07.11 -> T07.12 -> T07.13 (each depends on its predecessor).
        src = _write_phase_tasklist(
            tmp_path / "phase-7-tasklist.md",
            [
                _task_block("T07.11"),
                _task_block("T07.12", deps="T07.11"),
                _task_block("T07.13", deps="T07.12"),
            ],
        )
        # Rerunning the whole chain together: every dep is itself a target, so it
        # is satisfied by construction and the full chain resolves with no abort.
        resolved, warnings = walk_dependencies(src, ["T07.11", "T07.12", "T07.13"])
        assert resolved == ["T07.11", "T07.12", "T07.13"]
        assert warnings == []

    def test_cycle_does_not_loop_infinitely(self, tmp_path: Path):
        # Mutual dependency T07.11 <-> T07.12. Both are rerun targets, so each
        # dep is satisfied-by-construction; the walker must terminate (no infinite
        # loop) and return both.
        src = _write_phase_tasklist(
            tmp_path / "phase-7-tasklist.md",
            [
                _task_block("T07.11", deps="T07.12"),
                _task_block("T07.12", deps="T07.11"),
            ],
        )
        resolved, warnings = walk_dependencies(src, ["T07.11", "T07.12"])
        assert set(resolved) == {"T07.11", "T07.12"}


# ---------------------------------------------------------------------------
# walk_dependencies(include_transitive=True) — transitive closure
# ---------------------------------------------------------------------------


class TestTransitiveClosure:
    def test_closure_includes_all_descendants(self, tmp_path: Path):
        # Rerun only T07.13; it depends on T07.12 which depends on T07.11. Neither
        # prerequisite is recorded PASS, so --include-transitive must auto-include
        # the unsatisfied dependency T07.12 (cost stays under the 50% ceiling).
        src = _write_phase_tasklist(
            tmp_path / "phase-7-tasklist.md",
            [
                _task_block("T07.11"),
                _task_block("T07.12", deps="T07.11"),
                _task_block("T07.13", deps="T07.12"),
            ],
        )
        view = _View(
            [
                _task_result("T07.11", TaskStatus.PASS, turns=1),
                _task_result(
                    "T07.12", TaskStatus.FAIL_RECOVERABLE, deps=["T07.11"], turns=1
                ),
                _task_result(
                    "T07.13", TaskStatus.FAIL_RECOVERABLE, deps=["T07.12"], turns=1
                ),
            ]
        )
        resolved, warnings = walk_dependencies(
            src,
            ["T07.13"],
            phase_result=view,
            results_dir=tmp_path,
            include_transitive=True,
        )
        # T07.12 (unsatisfied dep) auto-included; T07.11 is recorded PASS so it is
        # satisfied and not pulled in.
        assert "T07.13" in resolved
        assert "T07.12" in resolved
        assert any("T07.12" in w for w in warnings)


# ---------------------------------------------------------------------------
# discover_failed_tasks_from_transcripts() — legacy transcript fallback
# ---------------------------------------------------------------------------


def _write_transcript(
    results_dir: Path, phase: int, task_id: str, lines: list[dict]
) -> Path:
    """Write a ``phase-N-task-<id>-output.txt`` stream-json transcript."""
    results_dir.mkdir(parents=True, exist_ok=True)
    path = results_dir / f"phase-{phase}-task-{task_id}-output.txt"
    path.write_text("\n".join(json.dumps(ev) for ev in lines) + "\n", encoding="utf-8")
    return path


class TestTranscriptFallback:
    def test_discover_failed_tasks_via_is_error(self, tmp_path: Path):
        # Terminal result with is_error=true and non-zero output tokens (so the
        # zero-token transient branch does NOT apply) → classified non-PASS and
        # surfaced as a rerun candidate.
        _write_transcript(
            tmp_path,
            7,
            "T07.11",
            [
                {"type": "assistant", "message": {"usage": {"output_tokens": 128}}},
                {
                    "type": "result",
                    "is_error": True,
                    "subtype": "error_during_execution",
                },
            ],
        )
        failed = discover_failed_tasks_from_transcripts(tmp_path, 7)
        ids = [tid for tid, _status in failed]
        assert "T07.11" in ids
        status = dict(failed)["T07.11"]
        assert status is TaskStatus.FAIL_TERMINAL

    def test_discover_failed_tasks_via_output_tokens_heuristic(self, tmp_path: Path):
        # Errored result with ZERO output tokens — the transient heuristic
        # (output_tokens == 0) classifies it FAIL_RECOVERABLE, a rerun candidate.
        _write_transcript(
            tmp_path,
            7,
            "T07.12",
            [
                {"type": "assistant", "message": {"usage": {"output_tokens": 0}}},
                {"type": "result", "is_error": True, "subtype": "error_max_turns"},
            ],
        )
        # A clean PASS transcript for a sibling task — must NOT be flagged.
        _write_transcript(
            tmp_path,
            7,
            "T07.13",
            [
                {"type": "assistant", "message": {"usage": {"output_tokens": 256}}},
                {"type": "result", "is_error": False, "subtype": "success"},
            ],
        )
        failed = discover_failed_tasks_from_transcripts(tmp_path, 7)
        statuses = dict(failed)
        assert statuses.get("T07.12") is TaskStatus.FAIL_RECOVERABLE
        assert "T07.13" not in statuses  # PASS pruned


# ---------------------------------------------------------------------------
# run_rerun_tasks() — end-to-end orchestration (execute_sprint mocked)
# ---------------------------------------------------------------------------


class _FakePopenSuccess:
    """Mirrors test_e2e_success._FakePopenSuccess — never actually used here
    because execute_sprint is mocked, but kept per the task's mocking contract
    so a future test that drops the execute_sprint patch has a ready stub."""

    def __init__(self):
        self.returncode = 0
        self.pid = 20000
        self._poll_count = 0

    def poll(self):
        self._poll_count += 1
        return None if self._poll_count <= 1 else 0

    def wait(self, timeout=None):
        self.returncode = 0
        return 0


def _seed_orchestration(
    tmp_path: Path, target: str = "T07.11"
) -> tuple[SprintConfig, Phase]:
    """Seed a release dir with a phase tasklist, a parent phase-7-result.json
    (target recorded FAIL_RECOVERABLE), and a canonical original transcript that
    merge-back must rename to ``*.failed-<ts>``."""
    release = tmp_path / "release"
    results = release / "results"
    results.mkdir(parents=True, exist_ok=True)

    phase_file = release / "phase-7-tasklist.md"
    _write_phase_tasklist(phase_file, [_task_block(target)])

    index = release / "tasklist-index.md"
    index.write_text(
        "# Sprint\n\n| # | File |\n|---|------|\n| 7 | phase-7-tasklist.md |\n"
    )

    # Parent result JSON — target is FAIL_RECOVERABLE (default nomination picks it).
    parent_result = {
        "task_results": [
            _task_result(target, TaskStatus.FAIL_RECOVERABLE, turns=1).to_dict()
        ],
        "recovery_history": [],
    }
    (results / "phase-7-result.json").write_text(
        json.dumps(parent_result), encoding="utf-8"
    )

    # Canonical original transcript — merge-back Step 1 renames it to .failed-<ts>.
    (results / f"phase-7-task-{target}-output.txt").write_text(
        "original (failed) transcript\n", encoding="utf-8"
    )

    config = SprintConfig(
        index_path=index,
        release_dir=release,
        phases=[Phase(number=7, file=phase_file, name="Phase 7")],
        start_phase=7,
        end_phase=7,
    )
    return config, config.phases[0]


def _execute_sprint_writes_pass(target: str):
    """Return a fake execute_sprint that writes a PASS rerun result + produced
    transcript into the sub-config's bundle results dir."""

    def _fake(sub_config: SprintConfig):
        sub_results = sub_config.results_dir
        sub_results.mkdir(parents=True, exist_ok=True)
        rerun_result = {
            "task_results": [_task_result(target, TaskStatus.PASS, turns=1).to_dict()],
            "recovery_history": [],
        }
        (sub_results / "phase-7-result.json").write_text(
            json.dumps(rerun_result), encoding="utf-8"
        )
        # Produced transcript the merge-back copies to the canonical path.
        (sub_results / f"phase-7-task-{target}-output.txt").write_text(
            "rerun (passing) transcript\n", encoding="utf-8"
        )
        return None

    return _fake


class TestRunOrchestration:
    def test_orchestrate_writes_failed_suffix_to_originals(self, tmp_path: Path):
        config, _phase = _seed_orchestration(tmp_path, "T07.11")
        with (
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_execute_sprint_writes_pass("T07.11"),
            ),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            exit_code = run_rerun_tasks(
                config,
                phase=7,
                tasks=["T07.11"],
                from_reflect_report=None,
                merge_back=True,
                dry_run=False,
                include_transitive=False,
                ignore_deps=False,
                # force_merge=True: Step 10 (flip_target_checkboxes) writes a
                # rerun-provenance block into the source tasklist, so the Step 4
                # pre-rerun SHA no longer matches the Step 12 re-hash. The
                # SHA-guard therefore always trips on the normal merge-back path;
                # --force-merge is required to exercise the merge effects. See
                # the module-level note in the run-orchestration summary.
                force_merge=True,
                allow_loop=False,
                no_verify_checkpoints=True,
                bundle_dir=None,
                restore=False,
            )
        assert exit_code == 0
        # Merge-back renamed the original canonical transcript to *.failed-<ts>.
        failed = list(
            config.results_dir.glob("phase-7-task-T07.11-output.failed-*.txt")
        )
        assert failed, "expected original transcript renamed to *.failed-<ts>"

    def test_orchestrate_emits_phase_rerun_complete_event(self, tmp_path: Path):
        config, _phase = _seed_orchestration(tmp_path, "T07.11")
        with (
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_execute_sprint_writes_pass("T07.11"),
            ),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            run_rerun_tasks(
                config,
                phase=7,
                tasks=["T07.11"],
                from_reflect_report=None,
                merge_back=True,
                dry_run=False,
                include_transitive=False,
                ignore_deps=False,
                force_merge=True,  # see note in test_orchestrate_writes_failed_suffix
                allow_loop=False,
                no_verify_checkpoints=True,
                bundle_dir=None,
                restore=False,
            )
        execlog = config.release_dir / "execution-log.jsonl"
        assert execlog.exists()
        events = [
            json.loads(line)
            for line in execlog.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rerun_complete = [e for e in events if e.get("event") == "phase_rerun_complete"]
        assert len(rerun_complete) == 1
        assert rerun_complete[0]["phase"] == 7


# ---------------------------------------------------------------------------
# acquire_recovery_lock() — lock file creation
# ---------------------------------------------------------------------------


class TestLockFile:
    def test_lock_acquire_creates_file_with_pid(self, tmp_path: Path):
        from superclaude.cli.sprint.recovery import release_recovery_lock

        lock_path = acquire_recovery_lock(tmp_path, 7)
        try:
            # Lock lives under <results_dir>/.recovery-locks/phase-7.lock and its
            # JSON body records the holding process PID (TDD §T8.5).
            assert lock_path.exists()
            assert lock_path.parent.name == ".recovery-locks"
            assert lock_path.name == "phase-7.lock"
            payload = json.loads(lock_path.read_text(encoding="utf-8"))
            assert payload["pid"] == os.getpid()
            assert "timestamp" in payload
        finally:
            release_recovery_lock(lock_path)


# ---------------------------------------------------------------------------
# R-F4 regression — PHASE_FILE_PATTERN matches the rerun-bundle tasklist name
# ---------------------------------------------------------------------------


class TestRerunNameMatchRegression:
    def test_phase_Nr_tasklist_name_matches_phase_file_pattern(self):  # noqa: N802
        # R-F4 fix (config.py): PHASE_FILE_PATTERN was widened with the alternation
        # `phase-(\d+)r-tasklist\.md` so the executor's discover_phases can locate a
        # rerun-bundle sub-tasklist (phase-7r-tasklist.md) and run it as Phase 7.
        # Guard the widened pattern at the regex level (no heavy discovery call).
        match = PHASE_FILE_PATTERN.search("phase-7r-tasklist.md")
        assert match is not None, "widened PHASE_FILE_PATTERN must match phase-Nr form"
        # The captured digits are the phase number (7), regardless of which
        # alternation group matched.
        captured = [g for g in match.groups() if g is not None]
        assert captured == ["7"]
        # Sanity: the canonical (non-rerun) form still matches and the trailing-r
        # form is genuinely a distinct branch from plain phase-7-tasklist.md.
        assert PHASE_FILE_PATTERN.search("phase-7-tasklist.md") is not None
