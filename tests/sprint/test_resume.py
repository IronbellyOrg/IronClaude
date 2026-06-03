"""Auto-resume feature tests (v4.3.5) — maps 1:1 to AC-1..AC-9 + invariants.

Covers ResumePlanner (FR-1), DriftAssessor (FR-3), BoundaryIntegrityGate (FR-2),
and the CLI wiring (FR-4) per design.md §9. Validator-corrected invariants
(FR-2.5 non-destructive quarantine, DD-2 advisory-only Haiku, INV-001 same-fn
hash) are locked here too.

All tests are deterministic. The gate's advisory coherence read (``invoke_sonnet``)
is stubbed to "" by an autouse fixture so it never shells out to ``claude`` (the
CI-safe no-LLM path), except where a test explicitly drives a mocked verdict.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.sprint import commands as sprint_commands
from superclaude.cli.sprint import summarizer as sprint_summarizer
from superclaude.cli.sprint.commands import sprint_group
from superclaude.cli.sprint.rerun_tasks import (
    _content_sha256_excluding_rerun_block,
    _content_sha256_ws_excluding_rerun_block,
)
from superclaude.cli.sprint.resume.drift import DriftAssessor
from superclaude.cli.sprint.resume.integrity import BoundaryIntegrityGate
from superclaude.cli.sprint.resume.models import Granularity
from superclaude.cli.sprint.resume.planner import ResumePlanner

# A transcript that _classify_transcript scores as PASS (result event + tokens).
PASS_TRANSCRIPT = (
    '{"type":"assistant","message":{"usage":{"output_tokens":42}}}\n'
    '{"type":"result","subtype":"success","is_error":false}\n'
)


@pytest.fixture(autouse=True)
def _stub_invoke_sonnet(monkeypatch):
    """Default: advisory coherence read returns '' (no-LLM, CI-safe)."""
    monkeypatch.setattr(sprint_summarizer, "invoke_sonnet", lambda *a, **k: "")


# --------------------------------------------------------------------------- #
# Fixture builders                                                            #
# --------------------------------------------------------------------------- #


def _write_index(release: Path, phase_numbers) -> Path:
    rows = "".join(f"| phase-{n}-tasklist.md |\n" for n in phase_numbers)
    index = release / "index.md"
    index.write_text(f"# Index\n| File |\n|---|\n{rows}", encoding="utf-8")
    return index


def _complete_phase(results: Path, n: int) -> list[dict]:
    (results / f"phase-{n}-result.json").write_text(
        json.dumps({"phase": n, "status": "pass", "task_results": []}),
        encoding="utf-8",
    )
    return [
        {"event": "phase_start", "phase": n},
        {"event": "phase_complete", "phase": n, "status": "pass"},
    ]


def _write_log(release: Path, events: list[dict]) -> None:
    (release / "execution-log.jsonl").write_text(
        "\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8"
    )


def _task_block(task_id: str, *, deliverable: Path | None = None) -> str:
    block = f"### {task_id} -- task {task_id}\n"
    if deliverable is not None:
        block += f"**Artifacts (Intended Paths):**\n- `{deliverable}`\n"
    return block + "\n"


# --------------------------------------------------------------------------- #
# ResumePlanner — AC-1 / AC-2 / AC-3                                          #
# --------------------------------------------------------------------------- #


class TestResumePlanner:
    def test_resume_planner_phase_boundary(self, tmp_path):
        """AC-1: result.json for P1,P2 + a dangling phase_start for P3 ⇒
        interrupted_phase==3, completed==[1,2], crash."""
        results = tmp_path / "results"
        results.mkdir()
        for n in (1, 2, 3):
            (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = _complete_phase(results, 1) + _complete_phase(results, 2)
        events.append({"event": "phase_start", "phase": 3})  # dangling — crash
        _write_log(tmp_path, events)

        plan = ResumePlanner().plan(index)

        assert plan.interrupted_phase == 3
        assert plan.completed_phases == [1, 2]
        assert plan.interrupt_kind == "crash"
        assert plan.start_phase == 3

    def test_resume_task_level_recoverable(self, tmp_path):
        """AC-2: P3 result.json with one fail_recoverable task ⇒ TASK granularity,
        rerun_task_ids == [that task]."""
        results = tmp_path / "results"
        results.mkdir()
        for n in (1, 2, 3):
            (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = _complete_phase(results, 1) + _complete_phase(results, 2)
        (results / "phase-3-result.json").write_text(
            json.dumps(
                {
                    "phase": 3,
                    "status": "incomplete",
                    "task_results": [
                        {"task": {"task_id": "T03.01"}, "status": "pass"},
                        {"task": {"task_id": "T03.02"}, "status": "fail_recoverable"},
                    ],
                }
            )
        )
        events += [
            {"event": "phase_start", "phase": 3},
            {"event": "phase_complete", "phase": 3, "status": "incomplete"},
        ]
        _write_log(tmp_path, events)

        plan = ResumePlanner().plan(index)

        assert plan.granularity is Granularity.TASK
        assert plan.rerun_task_ids == ["T03.02"]
        roles = {bt.task_id: bt.role for bt in plan.boundary_tasks}
        assert roles["T03.01"] == "last_completed"
        assert roles["T03.02"] == "next_unfinished"

    def test_resume_hard_crash_phase_level(self, tmp_path):
        """AC-3: P3 phase_start, no result.json, no per-task transcripts ⇒
        PHASE granularity (whole-phase re-run)."""
        results = tmp_path / "results"
        results.mkdir()
        for n in (1, 2, 3):
            (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = _complete_phase(results, 1) + _complete_phase(results, 2)
        events.append({"event": "phase_start", "phase": 3})  # dangling, no result.json
        _write_log(tmp_path, events)

        plan = ResumePlanner().plan(index)

        assert plan.interrupted_phase == 3
        assert plan.interrupt_kind == "crash"
        assert plan.granularity is Granularity.PHASE
        # F-4/CG-3: the PHASE hard-crash path now emits exactly ONE prior-tail
        # last_completed boundary task (the prior phase's tail) so the gate can
        # double-validate it. There is no next_unfinished/pending in the boundary
        # on a no-per-task-data hard crash; only the prior-tail validation entry.
        assert [bt.role for bt in plan.boundary_tasks] == ["last_completed"]
        assert plan.boundary_tasks[0].task_id == "T02.01"

    def test_resume_hard_crash_double_validates_prior_phase_tail(self, tmp_path):
        """AC-3 / merged-req: a PHASE hard crash (P3 phase_start, no result.json,
        no per-task transcripts) double-validates the PRIOR completed phase's
        tail (P2's last task) before re-running P3 (F-4 / CG-3)."""
        results = tmp_path / "results"
        results.mkdir()
        # P2's tail task gets a real PASS transcript + a present deliverable so the
        # gate can re-derive it (Signal B) rather than vacuously pass.
        p2_deliv = tmp_path / "p2_tail_deliverable.txt"
        p2_deliv.write_text("done\n")
        (tmp_path / "phase-1-tasklist.md").write_text(_task_block("T01.01"))
        (tmp_path / "phase-2-tasklist.md").write_text(
            "# Phase 2\n" + _task_block("T02.01", deliverable=p2_deliv)
        )
        (tmp_path / "phase-3-tasklist.md").write_text(_task_block("T03.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = _complete_phase(results, 1) + _complete_phase(results, 2)
        events.append({"event": "phase_start", "phase": 3})  # dangling, no result.json
        _write_log(tmp_path, events)
        (results / "phase-2-task-T02.01-output.txt").write_text(PASS_TRANSCRIPT)

        plan = ResumePlanner().plan(index)
        assert plan.granularity is Granularity.PHASE
        # (i) plan-level: a last_completed boundary task now points at P2's tail.
        lc = [bt for bt in plan.boundary_tasks if bt.role == "last_completed"]
        assert lc and lc[0].task_id == "T02.01"  # fails today (boundary empty)
        # (ii) gate-level: validated_last is a REAL re-derivation, not vacuous.
        report = BoundaryIntegrityGate().run(plan)
        assert report.validated_last is True  # genuinely re-derived P2 tail

    def test_resume_hard_crash_prior_tail_overclaim_stops(self, tmp_path):
        """AC-3 negative companion: a PHASE hard crash whose prior-phase tail
        deliverable is MISSING ⇒ the prior-tail double-validation can actually
        STOP (validated_last False / passed False), proving it is non-vacuous
        (F-4 / CG-3). Mirrors test_gate_hard_stops_on_last_completed_overclaim
        for the PHASE hard-crash path."""
        results = tmp_path / "results"
        results.mkdir()
        # P2's tail DECLARES a deliverable but it is NEVER written to disk ⇒
        # artifacts_ok is False ⇒ the prior-tail validation must STOP.
        p2_deliv = tmp_path / "p2_tail_deliverable.txt"  # intentionally absent
        (tmp_path / "phase-1-tasklist.md").write_text(_task_block("T01.01"))
        (tmp_path / "phase-2-tasklist.md").write_text(
            "# Phase 2\n" + _task_block("T02.01", deliverable=p2_deliv)
        )
        (tmp_path / "phase-3-tasklist.md").write_text(_task_block("T03.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = _complete_phase(results, 1) + _complete_phase(results, 2)
        events.append({"event": "phase_start", "phase": 3})
        _write_log(tmp_path, events)
        (results / "phase-2-task-T02.01-output.txt").write_text(PASS_TRANSCRIPT)

        plan = ResumePlanner().plan(index)
        lc = [bt for bt in plan.boundary_tasks if bt.role == "last_completed"]
        assert lc and lc[0].task_id == "T02.01"
        report = BoundaryIntegrityGate().run(plan)
        assert report.validated_last is False  # missing P2 deliverable ⇒ STOP
        assert report.passed is False

    def test_planner_performs_no_writes(self, tmp_path):
        """The planner is pure-read — results/ is byte-identical after planning."""
        results = tmp_path / "results"
        results.mkdir()
        for n in (1, 2, 3):
            (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = _complete_phase(results, 1) + _complete_phase(results, 2)
        events.append({"event": "phase_start", "phase": 3})
        _write_log(tmp_path, events)

        before = {p.name: p.read_bytes() for p in results.iterdir()}
        ResumePlanner().plan(index)
        after = {p.name: p.read_bytes() for p in results.iterdir()}
        assert before == after


def _build_task_interrupted(
    tmp_path: Path,
    current_body: str,
    *,
    record_hash: bool = False,
    recorded_body: str | None = None,
) -> Path:
    """P1,P2 complete; P3 interrupted with a per-task result.json (TASK path).

    ``current_body`` is the tasklist as it exists NOW (possibly operator-edited).
    When ``record_hash`` is set, the recorded ``tasklist_sha256`` baseline is the
    hash of ``recorded_body`` (defaulting to ``current_body``) — computed via the
    SAME ``_content_sha256_excluding_rerun_block`` over the SAME file, so drift is
    measured against the tasklist as it was WHEN THE PHASE RAN.
    """
    results = tmp_path / "results"
    results.mkdir()
    (tmp_path / "phase-1-tasklist.md").write_text(_task_block("T01.01"))
    (tmp_path / "phase-2-tasklist.md").write_text(_task_block("T02.01"))
    p3 = tmp_path / "phase-3-tasklist.md"
    index = _write_index(tmp_path, (1, 2, 3))
    events = _complete_phase(results, 1) + _complete_phase(results, 2)
    rj = {
        "phase": 3,
        "status": "incomplete",
        "task_results": [
            {"task": {"task_id": "T03.01"}, "status": "pass"},
            {"task": {"task_id": "T03.02"}, "status": "incomplete"},
        ],
    }
    if record_hash:
        # Hash the baseline body via the exact same fn+file, then write current.
        p3.write_text(recorded_body if recorded_body is not None else current_body)
        rj["tasklist_sha256"] = _content_sha256_excluding_rerun_block(p3)
        # F-3/CG-2 co-edit: persist the whitespace-normalized hash of the SAME
        # recorded body too, so the drift fix's "WS-missing ⇒ conservative <0.8"
        # fallback does NOT fire on the synthetic AC-4/AC-5 fixtures. Without this,
        # test_drift_trailing_whitespace_high_conf (AC-4) would hit the WS-missing
        # branch and FAIL its confidence>=0.8 / cosmetic assertions.
        rj["tasklist_sha256_ws"] = _content_sha256_ws_excluding_rerun_block(p3)
    p3.write_text(current_body)
    (results / "phase-3-result.json").write_text(json.dumps(rj))
    events += [
        {"event": "phase_start", "phase": 3},
        {"event": "phase_complete", "phase": 3, "status": "incomplete"},
    ]
    _write_log(tmp_path, events)
    return index


# Canonical P3 body with two well-formed task headings.
_P3 = "# Phase 3\n" + _task_block("T03.01") + _task_block("T03.02")


# --------------------------------------------------------------------------- #
# DriftAssessor — AC-4 / AC-5 / INV-001                                       #
# --------------------------------------------------------------------------- #


class TestDriftAssessor:
    def test_inv001_tier0_exact_hash_match(self, tmp_path):
        """INV-001: stored tasklist_sha256 and current hash use the SAME function
        over the SAME per-phase file ⇒ Tier 0 matches on an unchanged tasklist."""
        index = _build_task_interrupted(tmp_path, _P3, record_hash=True)
        plan = ResumePlanner().plan(index)
        drift = DriftAssessor().assess(index, plan)
        assert drift.confidence == 1.0
        assert drift.tier == "hash"
        assert drift.cosmetic_only is True

    def test_drift_trailing_whitespace_high_conf(self, tmp_path):
        """AC-4: trailing-whitespace-only edit (task-ID structure intact) ⇒ ≥0.8.

        Baseline recorded for the ORIGINAL body; current adds trailing whitespace
        so the block-stripped hash differs (Tier-0 misses) and Tier-1 cosmetic
        scoring applies."""
        index = _build_task_interrupted(
            tmp_path, _P3 + "   \n", record_hash=True, recorded_body=_P3
        )
        plan = ResumePlanner().plan(index)
        drift = DriftAssessor().assess(index, plan)
        assert drift.confidence >= 0.8
        # Lock that this is the AC-4 *Tier-1 cosmetic* path, not a vacuous Tier-0
        # hash match: the baseline hash is of the ORIGINAL body and the current
        # body has trailing whitespace, so the block-stripped hash MUST differ
        # (Tier 0 misses) and the structural cosmetic comparator must carry it.
        # If the hash fn ever normalized whitespace, Tier 0 would match (1.0) and
        # AC-4's real path would stop being exercised — this catches that.
        assert drift.tier != "hash"
        assert drift.cosmetic_only is True
        assert drift.explanation

    def test_drift_material_edit_low_conf(self, tmp_path):
        """AC-5: a completed (PASS) task removed/renamed ⇒ <0.8 (resume STOPs)."""
        material = "# Phase 3\n" + _task_block("T03.09") + _task_block("T03.02")
        index = _build_task_interrupted(
            tmp_path, material, record_hash=True, recorded_body=_P3
        )
        plan = ResumePlanner().plan(index)
        drift = DriftAssessor().assess(index, plan)
        assert drift.confidence < 0.8
        # Lock the *removed-completed-task* path (not the corrupt/empty-file guard
        # which also scores 0.3): the current body parses to a NON-empty ID set
        # missing the completed T03.01, so the explanation must name that task.
        assert "T03.01" in drift.explanation
        assert drift.cosmetic_only is False
        assert drift.explanation

    def test_drift_same_id_material_body_edit_low_conf(self, tmp_path):
        """AC-5: a same-ID body/deliverable edit to a COMPLETED task ⇒ <0.8 (STOP).

        Companion to test_drift_material_edit_low_conf (ID removal). Here the
        completed task T03.01 keeps its '### T03.01' heading but its BODY /
        declared deliverable changes — the Tier-0 hash misses (content changed)
        and Tier 1 must NOT dismiss it as cosmetic on the unchanged ID set
        (F-3 / CG-2)."""
        # Same IDs as _P3 (T03.01, T03.02) but T03.01's body/deliverable is edited.
        edited = (
            "# Phase 3\n"
            + _task_block("T03.01", deliverable=tmp_path / "new_deliverable.txt")
            + _task_block("T03.02")
        )
        index = _build_task_interrupted(
            tmp_path, edited, record_hash=True, recorded_body=_P3
        )
        plan = ResumePlanner().plan(index)
        drift = DriftAssessor().assess(index, plan)
        assert drift.confidence < 0.8  # fails today (gets 0.9), passes post-F-3
        assert drift.cosmetic_only is False
        assert drift.explanation

    def test_drift_not_yet_run_change_advisory(self, tmp_path):
        """Adding a brand-new task in the not-yet-run region ⇒ ~0.85 (advisory)."""
        added = _P3 + _task_block("T03.03")
        index = _build_task_interrupted(
            tmp_path, added, record_hash=True, recorded_body=_P3
        )
        plan = ResumePlanner().plan(index)
        drift = DriftAssessor().assess(index, plan)
        assert drift.confidence == pytest.approx(0.85)

    def test_drift_missing_recorded_hash_no_crash(self, tmp_path):
        """No recorded hash (pre-v4.3.5 phase) ⇒ no Tier-0, no crash."""
        index = _build_task_interrupted(tmp_path, _P3, record_hash=False)
        plan = ResumePlanner().plan(index)
        drift = DriftAssessor().assess(index, plan)
        assert drift.tier != "hash"
        assert drift.explanation


# --------------------------------------------------------------------------- #
# Planner edges — AC-6 / AC-8                                                 #
# --------------------------------------------------------------------------- #


class TestPlannerEdges:
    def test_nothing_to_resume(self, tmp_path):
        """AC-6: all phases complete ⇒ granularity NONE (nothing to resume)."""
        results = tmp_path / "results"
        results.mkdir()
        for n in (1, 2, 3):
            (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = (
            _complete_phase(results, 1)
            + _complete_phase(results, 2)
            + _complete_phase(results, 3)
        )
        _write_log(tmp_path, events)

        plan = ResumePlanner().plan(index)
        assert plan.granularity is Granularity.NONE

    def test_ambiguous_release_dirs_stop(self, tmp_path):
        """AC-8: >1 plausible release dir carrying state ⇒ ambiguous, no auto-pick."""
        release = tmp_path / "release"
        release.mkdir()
        (release / ".roadmap-state.json").write_text("{}")  # release indicator
        (release / "execution-log.jsonl").write_text(
            json.dumps({"event": "phase_start", "phase": 1}) + "\n"
        )
        (release / "results").mkdir()
        tasklist = release / "tasklist"
        tasklist.mkdir()
        for n in (1, 2):
            (tasklist / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tasklist, (1, 2))
        # tasklist/ ALSO carries state → two candidates
        (tasklist / "execution-log.jsonl").write_text(
            json.dumps({"event": "phase_start", "phase": 1}) + "\n"
        )

        plan = ResumePlanner().plan(index)
        assert plan.ambiguous is True
        assert plan.ambiguity_reasons


# --------------------------------------------------------------------------- #
# CLI wiring — AC-7 / AC-9 / nothing-to-resume                               #
# --------------------------------------------------------------------------- #


class TestCliWiring:
    def test_explicit_start_bypasses_autodetect(self, tmp_path, monkeypatch):
        """AC-7: an explicit --start (even --start 1) bypasses auto-resume; the
        planner/_auto_resume is NOT called. Proves parameter-source, not value
        comparison, gates the bypass."""
        index = _build_task_interrupted(tmp_path, _P3, record_hash=True)
        calls = {"n": 0}
        original = sprint_commands._auto_resume

        def _counting(*a, **k):
            calls["n"] += 1
            return original(*a, **k)

        monkeypatch.setattr(sprint_commands, "_auto_resume", _counting)
        runner = CliRunner()

        runner.invoke(sprint_group, ["run", str(index), "--start", "1", "--dry-run"])
        assert calls["n"] == 0  # explicit --start 1 bypassed auto-resume
        runner.invoke(sprint_group, ["run", str(index), "--start", "4", "--dry-run"])
        assert calls["n"] == 0  # explicit --start 4 bypassed too

        runner.invoke(sprint_group, ["run", str(index), "--dry-run"])
        assert calls["n"] == 1  # bare invocation auto-resumes exactly once

    def test_auto_resume_yes_path_prints_plan_and_partial_paths(
        self, tmp_path, monkeypatch, capsys
    ):
        """NEW-R1 / AC-1 / FR-4.2 / design §7: on the --yes/CI proceed path,
        _auto_resume prints the inferred plan AND the half-written partial-work
        paths BEFORE proceeding — realizing the visible-by-default 'print_plan
        then prompt(skipped: --yes)' sequence (only the confirm is skipped, not
        the print)."""
        from superclaude.cli.sprint.resume import models as resume_models

        index = _build_gate_fixture(
            tmp_path, lc_deliverable_exists=True, nu_partial=True
        )
        partial = tmp_path / "results" / "phase-3-task-T03.02-output.txt"
        # Pin a passing gate (carrying partial_paths) + high drift so the test
        # exercises the proceed-PRINT control flow (drift/gate have their own
        # tests); the planner runs for real to produce a genuine plan.
        monkeypatch.setattr(
            "superclaude.cli.sprint.resume.DriftAssessor.assess",
            lambda self, idx, plan: resume_models.DriftAssessment(
                confidence=1.0, tier="hash", cosmetic_only=True
            ),
        )
        monkeypatch.setattr(
            "superclaude.cli.sprint.resume.BoundaryIntegrityGate.run",
            lambda self, plan, **kw: resume_models.BoundaryReport(
                validated_last=True, passed=True, partial_paths=[partial]
            ),
        )

        decision = sprint_commands._auto_resume(index, assume_yes=True, dry_run=False)

        assert decision.action == "proceed"
        out = capsys.readouterr().out
        assert "Auto-resume plan" in out  # the inferred plan is printed (AC-1)
        # the half-written partial-work path is surfaced on the --yes path (CG-4 YES
        # informedness premise; F-2 reach extended to the proceed path):
        assert "phase-3-task-T03.02-output.txt" in out

    def test_nothing_to_resume_cli(self, tmp_path):
        """AC-6 (CLI): bare run on an all-complete release exits 0 with a message."""
        results = tmp_path / "results"
        results.mkdir()
        for n in (1, 2):
            (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tmp_path, (1, 2))
        _write_log(tmp_path, _complete_phase(results, 1) + _complete_phase(results, 2))

        result = CliRunner().invoke(sprint_group, ["run", str(index)])
        assert result.exit_code == 0
        assert "Nothing to resume" in result.output

    def test_rerun_tasks_autodetect_parity(self, tmp_path, monkeypatch):
        """AC-9: bare `rerun-tasks <idx>` produces the SAME run_rerun_tasks call
        (phase + tasks) as the equivalent explicit --phase/--tasks."""
        results = tmp_path / "results"
        results.mkdir()
        for n in (1, 2, 3):
            (tmp_path / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        index = _write_index(tmp_path, (1, 2, 3))
        events = _complete_phase(results, 1) + _complete_phase(results, 2)
        (results / "phase-3-result.json").write_text(
            json.dumps(
                {
                    "phase": 3,
                    "status": "incomplete",
                    "task_results": [
                        {"task": {"task_id": "T03.01"}, "status": "pass"},
                        {"task": {"task_id": "T03.02"}, "status": "fail_recoverable"},
                    ],
                }
            )
        )
        events.append({"event": "phase_start", "phase": 3})
        _write_log(tmp_path, events)

        captured = []
        from superclaude.cli.sprint import rerun_tasks as rt_mod

        monkeypatch.setattr(
            rt_mod,
            "run_rerun_tasks",
            lambda config, **kw: (
                captured.append((kw.get("phase"), kw.get("tasks"))) or 0
            ),
        )
        runner = CliRunner()
        runner.invoke(sprint_group, ["rerun-tasks", str(index)])
        runner.invoke(
            sprint_group,
            ["rerun-tasks", str(index), "--phase", "3", "--tasks", "T03.02"],
        )
        assert len(captured) == 2
        assert captured[0] == captured[1] == (3, ["T03.02"])


# --------------------------------------------------------------------------- #
# Validator-corrected invariants — FR-2.5 / DD-2                              #
# --------------------------------------------------------------------------- #


def _build_gate_fixture(
    tmp_path: Path, *, lc_deliverable_exists: bool, nu_partial: bool
) -> Path:
    """TASK-interrupted fixture: T03.01 last-completed (PASS transcript +
    optional deliverable), T03.02 next-unfinished (optional partial transcript)."""
    results = tmp_path / "results"
    results.mkdir()
    lc_deliv = tmp_path / "lc_deliverable.txt"
    if lc_deliverable_exists:
        lc_deliv.write_text("done\n")
    (tmp_path / "phase-1-tasklist.md").write_text(_task_block("T01.01"))
    (tmp_path / "phase-2-tasklist.md").write_text(_task_block("T02.01"))
    (tmp_path / "phase-3-tasklist.md").write_text(
        "# Phase 3\n"
        + _task_block("T03.01", deliverable=lc_deliv)
        + _task_block("T03.02")
    )
    index = _write_index(tmp_path, (1, 2, 3))
    events = _complete_phase(results, 1) + _complete_phase(results, 2)
    (results / "phase-3-result.json").write_text(
        json.dumps(
            {
                "phase": 3,
                "status": "incomplete",
                "task_results": [
                    {"task": {"task_id": "T03.01"}, "status": "pass"},
                    {"task": {"task_id": "T03.02"}, "status": "incomplete"},
                ],
            }
        )
    )
    events.append({"event": "phase_start", "phase": 3})
    _write_log(tmp_path, events)
    (results / "phase-3-task-T03.01-output.txt").write_text(PASS_TRANSCRIPT)
    if nu_partial:
        # An incomplete transcript (no terminal result event) for the next task.
        (results / "phase-3-task-T03.02-output.txt").write_text(
            "partial work, killed mid-task\n"
        )
    return index


class TestInvariants:
    def test_gate_hard_stops_on_last_completed_overclaim(self, tmp_path):
        """FR-2.4 (negative direction): a last-completed task that is persisted
        PASS with a PASS transcript but a MISSING declared deliverable is an
        over-claim — ``validated_last``/``passed`` go False with blocking_reasons,
        and the explicit ``accept_suspect`` override flips ``passed`` back to True.

        Without this the whole gate could regress to an always-True no-op while
        every other (positive-direction) test still passed — this locks the hard
        STOP that is the gate's reason to exist."""
        index = _build_gate_fixture(
            tmp_path, lc_deliverable_exists=False, nu_partial=False
        )
        plan = ResumePlanner().plan(index)

        report = BoundaryIntegrityGate().run(plan)
        assert report.validated_last is False
        assert report.passed is False  # hard STOP (FR-2.4)
        assert report.blocking_reasons
        assert any(s.role == "last_completed" for s in report.suspects)

        # Explicit operator override proceeds despite the suspect seam.
        accepted = BoundaryIntegrityGate().run(plan, accept_suspect=True)
        assert accepted.passed is True

    def test_boundary_quarantine_nondestructive(self, tmp_path):
        """FR-2.5: default report-only (NO results/ mutation); opt-in cleanup
        copies under .resume-quarantine-<ts>/ with a manifest, leaves the
        original untouched, writes an audit line + lock, and is reversible by
        the EXISTING restore_from_bundle."""
        from superclaude.cli.sprint.rerun_tasks import restore_from_bundle

        index = _build_gate_fixture(
            tmp_path, lc_deliverable_exists=True, nu_partial=True
        )
        results = tmp_path / "results"
        plan = ResumePlanner().plan(index)

        # Default: report-only — zero mutation.
        before = sorted(p.name for p in results.iterdir())
        report = BoundaryIntegrityGate().run(plan)
        after = sorted(p.name for p in results.iterdir())
        assert before == after
        assert report.quarantined == {}
        # Partial work is surfaced (next-unfinished suspect) but does NOT block.
        assert report.passed is True
        assert any(s.role == "next_unfinished" for s in report.suspects)

        # Opt-in: reversible copy-to-quarantine.
        report2 = BoundaryIntegrityGate().run(plan, cleanup_opted_in=True)
        qdirs = [
            d for d in results.iterdir() if d.name.startswith(".resume-quarantine-")
        ]
        assert len(qdirs) == 1
        qdir = qdirs[0]
        assert (qdir / "preserved" / "manifest.json").exists()
        assert (results / "recovery-audit.log").exists()
        assert "resume_quarantine" in (results / "recovery-audit.log").read_text()
        assert (results / ".recovery-locks").exists()
        assert report2.quarantined
        original = results / "phase-3-task-T03.02-output.txt"
        assert original.read_text() == "partial work, killed mid-task\n"  # untouched

        # restore_from_bundle reverses it: corrupt original, restore, verify.
        original.write_text("CORRUPTED\n")
        restored = restore_from_bundle(qdir, results)
        assert restored >= 1
        assert original.read_text() == "partial work, killed mid-task\n"

    def test_boundary_partial_paths_surfaced_in_report(self, tmp_path):
        """FR-2.2 / item 3.2: report-only partial work surfaces the artifact
        PATHS (not just the next-unfinished task) in the BoundaryReport (CG-1/F-2).

        design §4(b): "report suspect paths in BoundaryReport (always)" — the
        paths must be carried on the DEFAULT report-only path, independent of
        cleanup opt-in, where ``quarantined`` is empty."""
        index = _build_gate_fixture(
            tmp_path, lc_deliverable_exists=True, nu_partial=True
        )
        plan = ResumePlanner().plan(index)
        report = BoundaryIntegrityGate().run(plan)  # default report-only
        assert report.passed is True  # still non-blocking (§7)
        assert report.quarantined == {}  # no mutation
        # The partial-work PATHS are carried (the F-2 gap this locks):
        surfaced = [str(p) for p in report.partial_paths]
        assert any(s.endswith("phase-3-task-T03.02-output.txt") for s in surfaced)

    def test_haiku_coherence_advisory_only(self, tmp_path, monkeypatch):
        """DD-2: (a) a SUSPECT verdict on a deterministically-validated TASK adds
        a coherence_warning but leaves passed/validated_last unchanged; (b) on
        PHASE/empty transcript the LLM is not invoked; (c) empty verdict ⇒ a
        BoundaryReport identical to the no-LLM path."""
        # (a) suspect verdict — advisory only.
        index = _build_gate_fixture(
            tmp_path, lc_deliverable_exists=True, nu_partial=False
        )
        plan = ResumePlanner().plan(index)
        monkeypatch.setattr(
            sprint_summarizer, "invoke_sonnet", lambda *a, **k: "SUSPECT: looks off"
        )
        report = BoundaryIntegrityGate().run(plan)
        assert report.coherence_warnings  # surfaced
        assert report.validated_last is True  # UNCHANGED
        assert report.passed is True  # UNCHANGED (NFR-3)

        # (b) PHASE granularity ⇒ invoke_sonnet NOT called.
        calls = {"n": 0}
        monkeypatch.setattr(
            sprint_summarizer,
            "invoke_sonnet",
            lambda *a, **k: calls.__setitem__("n", calls["n"] + 1) or "SUSPECT: x",
        )
        phase_dir = tmp_path / "phase_case"
        phase_dir.mkdir()
        results = phase_dir / "results"
        results.mkdir()
        for n in (1, 2, 3):
            (phase_dir / f"phase-{n}-tasklist.md").write_text(_task_block(f"T0{n}.01"))
        pindex = _write_index(phase_dir, (1, 2, 3))
        pevents = _complete_phase(results, 1) + _complete_phase(results, 2)
        pevents.append({"event": "phase_start", "phase": 3})
        _write_log(phase_dir, pevents)
        pplan = ResumePlanner().plan(pindex)
        assert pplan.granularity is Granularity.PHASE
        BoundaryIntegrityGate().run(pplan)
        assert calls["n"] == 0

        # (c) empty verdict ⇒ identical to no-LLM path (no warnings).
        monkeypatch.setattr(sprint_summarizer, "invoke_sonnet", lambda *a, **k: "")
        report_c = BoundaryIntegrityGate().run(plan)
        assert report_c.coherence_warnings == []
        assert report_c.passed is True
