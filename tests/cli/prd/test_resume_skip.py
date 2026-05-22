"""Unit tests for the prd CLI resume-skip logic.

Covers the Stage A `skip_until_idx` loop and the Stage B `_execute_stage_b`
sub-stage skip + on-disk artifact detection introduced by PR #71 — review
finding M4 flagged the complete absence of coverage for this behaviour.
Also exercises the Cluster 4 pattern-decoupling: Stage B detection runs
through the compiled regexes in `_artifact_patterns.py`, so a filename
that violates the pattern is correctly NOT treated as a present artifact.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.prd._artifact_patterns import investigation_filename
from superclaude.cli.prd.config import resolve_config
from superclaude.cli.prd.executor import _STAGE_A_STEPS, PrdExecutor
from superclaude.cli.prd.models import PrdPipelineResult, PrdStepResult, PrdStepStatus

_STAGE_A_IDS = [s[0] for s in _STAGE_A_STEPS]


def _make_executor(tmp_path: Path, resume_from=None) -> PrdExecutor:
    """Build a PrdExecutor with a real (writable) task dir."""
    config = resolve_config(
        "resume-skip test", product="resume-test", tier="standard",
        dry_run=False, resume_from=resume_from,
    )
    task_dir = tmp_path / "prd-resume-test"
    config.task_dir = task_dir
    config.work_dir = tmp_path
    return PrdExecutor(config)


# ---------------------------------------------------------------------------
# Stage A skip-until loop (PrdExecutor.run)
# ---------------------------------------------------------------------------


def test_run_with_no_resume_invokes_every_stage_a_step_in_order(
    tmp_path: Path, monkeypatch
):
    """resume_from=None runs every Stage A step, in declared order."""
    executor = _make_executor(tmp_path, resume_from=None)
    called: list[str] = []

    def _record(step_id, step_name, builder_name):
        called.append(step_id)
        return PrdStepResult(status=PrdStepStatus.PASS)

    monkeypatch.setattr(executor, "_execute_step", _record)
    monkeypatch.setattr(executor, "_execute_stage_b", lambda result: None)
    executor.run()

    assert called[: len(_STAGE_A_IDS)] == _STAGE_A_IDS


def test_run_with_resume_from_research_notes_skips_earlier_stage_a_steps(
    tmp_path: Path, monkeypatch
):
    """resume_from='research-notes' skips check-existing/parse/scope."""
    executor = _make_executor(tmp_path, resume_from="research-notes")
    called: list[str] = []

    def _record(step_id, step_name, builder_name):
        called.append(step_id)
        return PrdStepResult(status=PrdStepStatus.PASS)

    monkeypatch.setattr(executor, "_execute_step", _record)
    monkeypatch.setattr(executor, "_execute_stage_b", lambda result: None)
    executor.run()

    for skipped in ("check-existing", "parse-request", "scope-discovery"):
        assert skipped not in called
    assert "research-notes" in called
    assert called.index("research-notes") == 0


def test_run_with_resume_from_stage_b_id_skips_all_of_stage_a(
    tmp_path: Path, monkeypatch
):
    """A Stage B resume target skips every Stage A step entirely."""
    executor = _make_executor(tmp_path, resume_from="assembly")
    called: list[str] = []

    def _record(step_id, step_name, builder_name):
        called.append(step_id)
        return PrdStepResult(status=PrdStepStatus.PASS)

    monkeypatch.setattr(executor, "_execute_step", _record)
    monkeypatch.setattr(executor, "_execute_stage_b", lambda result: None)
    executor.run()

    for stage_a_id in _STAGE_A_IDS:
        assert stage_a_id not in called


# ---------------------------------------------------------------------------
# Stage B sub-stage skip (_execute_stage_b) + artifact detection
# ---------------------------------------------------------------------------


def _stage_b_groups(executor: PrdExecutor, monkeypatch) -> list[str]:
    """Run _execute_stage_b with parallel/QA/assembly stubbed; return the
    group names actually dispatched to _execute_parallel_steps."""
    groups: list[str] = []
    monkeypatch.setattr(
        executor, "_execute_parallel_steps",
        lambda steps, result, group: groups.append(group),
    )
    monkeypatch.setattr(executor, "_execute_qa_fix_cycle", lambda *a, **k: None)
    monkeypatch.setattr(executor, "_execute_step", lambda *a, **k: PrdStepResult(
        status=PrdStepStatus.PASS))
    executor._execute_stage_b(PrdPipelineResult(config=executor._config))
    return groups


def test_execute_stage_b_skips_investigation_when_artifact_present(
    tmp_path: Path, monkeypatch
):
    """An on-disk investigation artifact skips the investigation sub-stage."""
    executor = _make_executor(tmp_path)
    research = executor._config.research_dir
    research.mkdir(parents=True)
    (research / investigation_filename(1, "core")).write_text("x", encoding="utf-8")

    groups = _stage_b_groups(executor, monkeypatch)
    assert "investigation" not in groups


def test_execute_stage_b_runs_investigation_when_only_web_artifact_present(
    tmp_path: Path, monkeypatch
):
    """A web-NN-*.md file must NOT false-match the investigation pattern."""
    executor = _make_executor(tmp_path)
    research = executor._config.research_dir
    research.mkdir(parents=True)
    (research / "web-01-foo.md").write_text("x", encoding="utf-8")

    groups = _stage_b_groups(executor, monkeypatch)
    assert "investigation" in groups


def test_execute_stage_b_skips_synthesis_when_synth_artifact_present(
    tmp_path: Path, monkeypatch
):
    """An on-disk synth-NN-*.md skips the synthesis sub-stage."""
    executor = _make_executor(tmp_path)
    synthesis = executor._config.synthesis_dir
    synthesis.mkdir(parents=True)
    (synthesis / "synth-01-foo.md").write_text("x", encoding="utf-8")

    groups = _stage_b_groups(executor, monkeypatch)
    assert "synthesis" not in groups


def test_execute_stage_b_pattern_decoupling_rename_breaks_skip(
    tmp_path: Path, monkeypatch
):
    """Detection is anchored to INVESTIGATION_FILENAME_RE, not a substring.

    A canonically-named file (01-core.md) skips investigation; renaming it
    to a pattern-violating single-digit name (1-core.md) makes the skip
    no longer fire — proving the regex is the authority.
    """
    executor = _make_executor(tmp_path)
    research = executor._config.research_dir
    research.mkdir(parents=True)
    canonical = research / investigation_filename(1, "core")
    canonical.write_text("x", encoding="utf-8")
    assert "investigation" not in _stage_b_groups(executor, monkeypatch)

    canonical.rename(research / "1-core.md")
    assert "investigation" in _stage_b_groups(executor, monkeypatch)
