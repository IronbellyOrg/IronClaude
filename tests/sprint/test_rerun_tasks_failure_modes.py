"""AC4-AC8 — failure-mode tests for sprint rerun-tasks.

Each test drives the real CLI surface (`sprint rerun-tasks`) through a
``CliRunner`` against a ``tmp_path`` sprint release, with subprocess and
executor side-effects stubbed via stacked ``patch()`` so nothing real spawns.
Abort messages asserted here are quoted byte-for-byte from the production
abort sites in ``rerun_tasks.py`` / ``recovery.py``; if production wording
changes these tests must change with it.

Layer note: the orchestrator ``run_rerun_tasks`` raises ``click.ClickException``
for operator-facing aborts and *returns* a non-zero exit code for the
abort-before-merge path. The CLI command wrapper (`commands.rerun_tasks`)
turns both into a process exit: a ``ClickException`` is caught by Click and
rendered as ``exit_code == 1`` with the message on stdout/stderr, and a
non-zero return is re-raised as ``SystemExit(code)``. ``CliRunner.invoke``
captures that ``SystemExit`` and exposes it as ``result.exit_code`` /
``result.exception``; failure-path tests therefore assert
``result.exit_code != 0`` (the captured ``SystemExit.code``).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.recovery import compute_tasklist_sha256

# ---------------------------------------------------------------------------
# Shared seed helpers (module-level functions, mirroring the sprint test
# convention of `_`-prefixed builders rather than fixtures).
# ---------------------------------------------------------------------------

_PHASE = 7
_T1 = "T07.11"
_T2 = "T07.12"


def _phase_tasklist_body(*, t1_deps: str = "none") -> str:
    """A minimal but parser-valid phase-7 tasklist with two tasks.

    The ``### T<PP>.<TT> -- Title`` headings and ``**Dependencies:**`` line are
    exactly what ``config.parse_tasklist`` and ``rerun_tasks`` regexes consume.
    """
    return (
        "# Phase 7: Failure-mode fixtures\n"
        "\n"
        f"### {_T1} -- First target task\n"
        f"**Dependencies:** {t1_deps}\n"
        "\n"
        "Body text for the first task.\n"
        "\n"
        f"### {_T2} -- Second target task\n"
        "**Dependencies:** none\n"
        "\n"
        "Body text for the second task.\n"
    )


def _write_sprint(tmp_path: Path, *, tasklist_body: str | None = None) -> Path:
    """Write a canonical single-phase sprint release; return the index path.

    Layout mirrors what ``load_sprint_config`` expects: a ``tasklist-index.md``
    with a ``File`` column pointing at ``phase-7-tasklist.md`` living alongside
    it. ``release_dir`` resolves to ``tmp_path`` (the index's parent), so
    results live under ``tmp_path/results``.
    """
    body = tasklist_body if tasklist_body is not None else _phase_tasklist_body()
    phase_file = tmp_path / "phase-7-tasklist.md"
    phase_file.write_text(body, encoding="utf-8")

    index = tmp_path / "tasklist-index.md"
    index.write_text(
        "# TASKLIST INDEX\n"
        "\n"
        "## Phase Files\n"
        "\n"
        "| Phase | File | Phase Name |\n"
        "|---|---|---|\n"
        "| 7 | phase-7-tasklist.md | Failure-mode fixtures |\n",
        encoding="utf-8",
    )
    return index


def _phase_result_payload(
    *,
    statuses: dict[str, str],
    recovery_history: list[dict] | None = None,
) -> dict:
    """Build a phase-N-result.json payload with the given per-task statuses.

    ``statuses`` maps task_id -> serialized ``TaskStatus`` value (e.g.
    ``"fail_recoverable"``, ``"pass"``). The nested ``task`` dict matches
    ``TaskResult.to_dict`` so ``TaskResult.from_dict`` and the default-nominator
    JSON reader both round-trip it.
    """
    task_results = []
    for tid, status in statuses.items():
        task_results.append(
            {
                "task": {
                    "task_id": tid,
                    "title": f"Task {tid}",
                    "description": "",
                    "dependencies": [],
                    "command": "",
                    "classifier": "",
                },
                "status": status,
                "turns_consumed": 5,
                "exit_code": 0 if status == "pass" else 1,
                "started_at": "2026-06-01T00:00:00+00:00",
                "finished_at": "2026-06-01T00:01:00+00:00",
                "output_bytes": 100,
                "gate_outcome": "pass" if status == "pass" else "fail",
                "reimbursement_amount": 0,
                "output_path": "",
            }
        )
    return {
        "phase": _PHASE,
        "task_results": task_results,
        "recovery_history": recovery_history or [],
    }


def _seed_recovery_bundle_history(
    tmp_path: Path, *, task_id: str, attempts: int
) -> Path:
    """Seed phase-7-result.json with ``attempts`` prior reruns of ``task_id``.

    Each history entry carries ``affected_tasks`` containing ``task_id`` so
    ``recovery.retry_count_for_task`` counts it. The task itself is recorded
    FAIL_RECOVERABLE so the default nominator picks it when ``--tasks`` is
    omitted. Returns the index path of the seeded sprint.
    """
    index = _write_sprint(tmp_path)
    results = tmp_path / "results"
    results.mkdir(parents=True, exist_ok=True)
    history = [
        {
            "bundle_id": f"rerun-prior-{i}",
            "affected_tasks": [task_id],
            "status": "success",
            "timestamp": f"2026-06-01T0{i}:00:00+00:00",
        }
        for i in range(attempts)
    ]
    payload = _phase_result_payload(
        statuses={task_id: "fail_recoverable"}, recovery_history=history
    )
    (results / f"phase-{_PHASE}-result.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    return index


def _seed_sprint_with_recorded_sha(tmp_path: Path) -> tuple[Path, str]:
    """Seed a sprint whose target is FAIL_RECOVERABLE; return (index, sha).

    The returned SHA is the source tasklist's hash captured BEFORE any
    mutation — the value ``run_rerun_tasks`` records at step 4 and re-checks at
    merge time (step 12). Tests mutate ``phase-7-tasklist.md`` after capture to
    drive the mid-flight-edit abort.
    """
    index = _write_sprint(tmp_path)
    results = tmp_path / "results"
    results.mkdir(parents=True, exist_ok=True)
    payload = _phase_result_payload(statuses={_T1: "fail_recoverable"})
    (results / f"phase-{_PHASE}-result.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    phase_file = tmp_path / "phase-7-tasklist.md"
    return index, compute_tasklist_sha256(phase_file)


def _seed_legacy_sprint(tmp_path: Path) -> Path:
    """Seed a pre-v4.3.0 sprint: transcripts on disk, NO phase-7-result.json.

    Writes a ``phase-7-task-T07.11-output.txt`` transcript whose terminal
    stream-json ``result`` event is errored (``is_error: true``) so
    ``discover_failed_tasks_from_transcripts`` classifies it non-PASS and the
    default nominator falls back to it. Returns the index path.
    """
    index = _write_sprint(tmp_path)
    results = tmp_path / "results"
    results.mkdir(parents=True, exist_ok=True)
    transcript = (
        json.dumps(
            {
                "type": "assistant",
                "message": {"usage": {"output_tokens": 0}},
            }
        )
        + "\n"
        + json.dumps({"type": "result", "is_error": True, "subtype": "error"})
        + "\n"
    )
    (results / f"phase-{_PHASE}-task-{_T1}-output.txt").write_text(
        transcript, encoding="utf-8"
    )
    return index


def _invoke(index: Path, *extra: str):
    """Run `sprint rerun-tasks <index> --phase 7 ...` via CliRunner."""
    runner = CliRunner()
    return runner.invoke(
        sprint_group,
        ["rerun-tasks", str(index), "--phase", str(_PHASE), *extra],
        catch_exceptions=True,
    )


def _passing_executor(bundle_targets: list[str]):
    """Return a fake ``execute_sprint`` that writes a PASS result JSON.

    ``run_rerun_tasks`` runs the rerun against an isolated sub-config whose
    ``release_dir`` is the bundle, then reads success back from
    ``<bundle>/results/phase-7-result.json`` via ``_rerun_targets_passed``.
    This stub writes that file marking every target ``pass`` so the merge-back
    branch (where the SHA re-check lives) is reached.
    """

    def _fake(sub_config) -> None:
        results = sub_config.release_dir / "results"
        results.mkdir(parents=True, exist_ok=True)
        payload = _phase_result_payload(
            statuses={tid: "pass" for tid in bundle_targets}
        )
        (results / f"phase-{_PHASE}-result.json").write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )

    return _fake


# ---------------------------------------------------------------------------
# AC4 — concurrent-recovery lock
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRerunTasksLocking:
    def test_second_concurrent_invocation_aborts_with_lock_pid(self, tmp_path):
        """A held lock (live PID) aborts the second invocation, naming the PID.

        Production: ``recovery.acquire_recovery_lock`` reads
        ``<results_dir>/.recovery-locks/phase-7.lock``, and when its recorded
        PID is alive raises::

            Recovery lock held by PID {pid} since {ts}. Remove `{lock}` if the
            prior process crashed.

        We pre-create the lock with THIS process's PID (guaranteed alive), so
        the abort fires before any nomination/executor work.
        """
        index = _write_sprint(tmp_path)
        results = tmp_path / "results"
        locks_dir = results / ".recovery-locks"
        locks_dir.mkdir(parents=True, exist_ok=True)
        live_pid = os.getpid()
        (locks_dir / f"phase-{_PHASE}.lock").write_text(
            json.dumps({"pid": live_pid, "timestamp": "2026-06-01T00:00:00+00:00"}),
            encoding="utf-8",
        )

        result = _invoke(index, "--tasks", _T1)

        assert result.exit_code != 0
        assert "Recovery lock held by PID" in result.output
        assert str(live_pid) in result.output


# ---------------------------------------------------------------------------
# AC5 — source-tasklist SHA256 mid-flight-edit guard
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRerunTasksSHACheck:
    def test_source_tasklist_sha_mismatch_aborts(self, tmp_path):
        """Editing the source tasklist mid-rerun aborts the merge-back.

        The SHA guard lives at step 12 (merge branch), so the rerun must reach
        a successful executor first; we stub ``execute_sprint`` to mark the
        target PASS, then mutate ``phase-7-tasklist.md`` after the pre-rerun SHA
        is captured. Production abort (byte-exact)::

            Source tasklist modified since rerun started. Bundle preserved at
            {bundle}. To force, use --force-merge.
        """
        index, _sha = _seed_sprint_with_recorded_sha(tmp_path)
        phase_file = tmp_path / "phase-7-tasklist.md"

        def _fake_execute(sub_config):
            # Mutate the canonical source AFTER step-4 SHA capture but before
            # the step-12 re-check, so current_sha != source_sha.
            phase_file.write_text(
                phase_file.read_text(encoding="utf-8") + "\nedited mid-flight\n",
                encoding="utf-8",
            )
            _passing_executor([_T1])(sub_config)

        with (
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_fake_execute,
            ),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = _invoke(index, "--tasks", _T1)

        assert result.exit_code != 0
        assert "Source tasklist modified since rerun started." in result.output
        assert "To force, use --force-merge." in result.output

    def test_force_merge_proceeds_with_warning(self, tmp_path):
        """``--force-merge`` overrides the SHA mismatch and completes the merge.

        Same mid-flight mutation as above, but with ``--force-merge`` the merge
        branch proceeds instead of aborting. ``merge_recovery_bundle`` and the
        post-merge ``verify-checkpoints`` subprocess are stubbed so only the
        rerun-tasks control flow is exercised; success prints the
        ``Rerun merged:`` line and exits 0.
        """
        index, _sha = _seed_sprint_with_recorded_sha(tmp_path)
        phase_file = tmp_path / "phase-7-tasklist.md"

        def _fake_execute(sub_config):
            phase_file.write_text(
                phase_file.read_text(encoding="utf-8") + "\nedited mid-flight\n",
                encoding="utf-8",
            )
            _passing_executor([_T1])(sub_config)

        with (
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_fake_execute,
            ),
            patch("superclaude.cli.sprint.recovery.merge_recovery_bundle"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = _invoke(index, "--tasks", _T1, "--force-merge")

        assert result.exit_code == 0
        assert "Source tasklist modified since rerun started." not in result.output
        assert "Rerun merged:" in result.output


# ---------------------------------------------------------------------------
# AC6 — retry cap (3) and --allow-loop bypass
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRerunTasksRetryCap:
    def test_fourth_attempt_aborts_with_cap_message(self, tmp_path):
        """A task already rerun 3 times aborts the 4th attempt (step 8).

        ``retry_count_for_task`` counts the 3 seeded ``recovery_history``
        entries; step 8 then raises (byte-exact prefix)::

            Task {tid} has been rerun 3 times. Manual intervention required.
            Inspect bundles: {bundles}

        The abort precedes the executor, so no executor stub is required.
        """
        index = _seed_recovery_bundle_history(tmp_path, task_id=_T1, attempts=3)

        result = _invoke(index, "--tasks", _T1)

        assert result.exit_code != 0
        assert f"Task {_T1} has been rerun 3 times." in result.output
        assert "Manual intervention required." in result.output
        assert "Inspect bundles:" in result.output

    def test_allow_loop_bypasses_cap(self, tmp_path):
        """``--allow-loop`` skips the retry-cap abort and runs the rerun.

        With the cap bypassed the executor runs (stubbed PASS) and the merge
        completes; the cap message must NOT appear and the run exits 0.
        ``merge_recovery_bundle`` + verify-checkpoints subprocess are stubbed.

        ``--force-merge`` is also passed because of a real engine interaction:
        step 10 (``flip_target_checkboxes``) writes a ``rerun_in_progress``
        provenance block to the source tasklist, which changes its SHA256.
        The step-12 mid-flight-edit guard then recomputes the hash and sees the
        engine's own write as a "modification", so any merge-back run aborts on
        the SHA mismatch unless ``--force-merge`` is set. This test isolates the
        retry-cap bypass, so it opts past that self-induced SHA guard to reach
        the merge. (See the prominent finding reported alongside this file.)
        """
        index = _seed_recovery_bundle_history(tmp_path, task_id=_T1, attempts=3)

        with (
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_passing_executor([_T1]),
            ),
            patch("superclaude.cli.sprint.recovery.merge_recovery_bundle"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = _invoke(index, "--tasks", _T1, "--allow-loop", "--force-merge")

        assert result.exit_code == 0
        assert "has been rerun 3 times" not in result.output
        assert "Rerun merged:" in result.output


# ---------------------------------------------------------------------------
# AC7 — legacy fallback (transcript inspection when phase-N-result.json absent)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRerunTasksLegacyFallback:
    def test_missing_phase_result_json_falls_back_to_transcript_inspection(
        self, tmp_path
    ):
        """No phase-7-result.json → nomination comes from transcript discovery.

        With ``--tasks`` omitted and the result JSON absent,
        ``select_default_recoverable_tasks`` returns ``[]`` and
        ``run_rerun_tasks`` falls back to
        ``discover_failed_tasks_from_transcripts`` (which finds the errored
        ``T07.11`` transcript). We assert the fallback path is actually taken
        via a spy and that the run proceeds with T07.11 nominated.
        """
        index = _seed_legacy_sprint(tmp_path)

        from superclaude.cli.sprint import rerun_tasks as rt

        real_discover = rt.discover_failed_tasks_from_transcripts
        calls: list[tuple] = []

        def _spy(results_dir, phase):
            calls.append((results_dir, phase))
            return real_discover(results_dir, phase)

        with (
            patch.object(
                rt, "discover_failed_tasks_from_transcripts", side_effect=_spy
            ),
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_passing_executor([_T1]),
            ),
            patch("superclaude.cli.sprint.recovery.merge_recovery_bundle"),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            # No --tasks: forces the default-nomination → legacy fallback path.
            # --force-merge: get past the engine's self-induced step-10/step-12
            # SHA guard (see TestRerunTasksRetryCap.test_allow_loop_bypasses_cap)
            # so the run reaches a clean merge and the success assertions hold.
            result = _invoke(index, "--force-merge")

        assert calls, "legacy transcript fallback was not invoked"
        assert calls[0][1] == _PHASE
        # The errored transcript's task was nominated and the run merged it.
        assert result.exit_code == 0
        assert "Rerun merged:" in result.output


# ---------------------------------------------------------------------------
# AC8 — abort-before-merge auto-restore of the source tasklist
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestRerunTasksAbortRestore:
    def test_abort_before_merge_back_restores_source_tasklist(self, tmp_path):
        """An executor failure restores the source tasklist byte-for-byte.

        ``run_rerun_tasks`` writes a ``rerun_in_progress`` provenance block to
        the source tasklist (step 10) before running the executor; when the
        executor raises, the ``finally`` block calls
        ``restore_checkboxes_on_abort`` which strips that block. Net effect: the
        on-disk tasklist must equal its pre-rerun bytes.
        """
        index = _seed_sprint_with_recorded_sha(tmp_path)[0]
        phase_file = tmp_path / "phase-7-tasklist.md"
        original_bytes = phase_file.read_text(encoding="utf-8")

        def _boom(sub_config):
            raise RuntimeError("simulated executor crash")

        with (
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_boom,
            ),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = _invoke(index, "--tasks", _T1)

        # Abort-before-merge returns exit code 1 (a non-success rerun), which
        # the CLI wrapper re-raises as SystemExit(1).
        assert result.exit_code != 0
        assert isinstance(result.exception, SystemExit)
        assert result.exception.code != 0
        assert phase_file.read_text(encoding="utf-8") == original_bytes

    def test_abort_clears_rerun_in_progress_flag(self, tmp_path):
        """After an aborted rerun, no ``rerun_in_progress`` marker remains.

        The provenance block written at step 10 carries a ``rerun_in_progress:``
        key; the auto-restore must remove the whole block so neither the marker
        nor the ``<!-- SUPERCLAUDE-RERUN`` delimiter survives on disk.
        """
        index = _seed_sprint_with_recorded_sha(tmp_path)[0]
        phase_file = tmp_path / "phase-7-tasklist.md"

        def _boom(sub_config):
            raise RuntimeError("simulated executor crash")

        with (
            patch(
                "superclaude.cli.sprint.executor.execute_sprint",
                side_effect=_boom,
            ),
            patch("superclaude.cli.sprint.rerun_tasks.subprocess.run"),
        ):
            result = _invoke(index, "--tasks", _T1)

        assert result.exit_code != 0
        final = phase_file.read_text(encoding="utf-8")
        assert "rerun_in_progress" not in final
        assert "SUPERCLAUDE-RERUN" not in final
