"""Tests for sprint checkpoint parsing, verification, and the gate in executor.py.

Covers:
- ``extract_checkpoint_paths()`` across 0, 1, 2, and 3 checkpoint sections.
- ``verify_checkpoint_files()`` for present/missing cases.
- Integration: ``_verify_checkpoints()`` in ``executor.py`` respects
  ``checkpoint_gate_mode`` (off/shadow/soft/full) and emits the
  ``checkpoint_verification`` JSONL event via SprintLogger.
"""

from __future__ import annotations

import io
import json
from contextlib import redirect_stdout
from pathlib import Path

from click.testing import CliRunner

from superclaude.cli.sprint.checkpoints import (
    build_manifest,
    extract_checkpoint_paths,
    recover_missing_checkpoints,
    verify_checkpoint_files,
    write_manifest,
)
from superclaude.cli.sprint.commands import verify_checkpoints
from superclaude.cli.sprint.executor import _verify_checkpoints
from superclaude.cli.sprint.logging_ import SprintLogger
from superclaude.cli.sprint.models import (
    CheckpointEntry,
    Phase,
    PhaseStatus,
    SprintConfig,
)
from superclaude.cli.sprint.recovery import (
    RecoveryBundle,
    RecoveryStatus,
    merge_recovery_bundle,
)

# ---------------------------------------------------------------------------
# extract_checkpoint_paths()
# ---------------------------------------------------------------------------


class TestExtractCheckpointPaths:
    def test_zero_checkpoints(self, tmp_path: Path):
        phase_file = tmp_path / "phase-1-tasklist.md"
        phase_file.write_text("# Phase 1\n\n### T01.01 -- Task\n\nBody.\n")
        assert extract_checkpoint_paths(phase_file, tmp_path) == []

    def test_single_checkpoint_backticks(self, tmp_path: Path):
        phase_file = tmp_path / "phase-1-tasklist.md"
        phase_file.write_text(
            "### Checkpoint: End of Phase 1\n"
            "**Checkpoint Report Path:** `checkpoints/CP-P01-END.md`\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert len(result) == 1
        name, path = result[0]
        assert name == "End of Phase 1"
        assert path == (tmp_path / "checkpoints" / "CP-P01-END.md").resolve()

    def test_two_checkpoints_mixed_formats(self, tmp_path: Path):
        phase_file = tmp_path / "phase-3-tasklist.md"
        phase_file.write_text(
            "### Checkpoint: Mid Phase 3\n"
            "**Checkpoint Report Path:** `checkpoints/CP-P03-T01-T05.md`\n\n"
            "### Checkpoint: End of Phase 3\n"
            "Checkpoint Report Path: checkpoints/CP-P03-END.md\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert [name for name, _ in result] == [
            "Mid Phase 3",
            "End of Phase 3",
        ]

    def test_absolute_path_preserved(self, tmp_path: Path):
        phase_file = tmp_path / "phase.md"
        phase_file.write_text(
            "### Checkpoint: Abs\nCheckpoint Report Path: /abs/checkpoints/CP.md\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert result == [("Abs", Path("/abs/checkpoints/CP.md"))]

    def test_name_falls_back_to_basename(self, tmp_path: Path):
        phase_file = tmp_path / "phase.md"
        # Path declaration with no preceding `### Checkpoint:` heading.
        phase_file.write_text("Checkpoint Report Path: checkpoints/CP-P01-END.md\n")
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert result[0][0] == "CP-P01-END.md"

    def test_missing_phase_file_returns_empty(self, tmp_path: Path):
        assert extract_checkpoint_paths(tmp_path / "does-not-exist.md", tmp_path) == []

    def test_wave4_numbered_checkpoint_task_form(self, tmp_path: Path):
        """Wave-4 emits checkpoints as numbered tasks; name must resolve to
        the heading label, not the basename fallback."""
        phase_file = tmp_path / "phase-1-tasklist.md"
        phase_file.write_text(
            "### T01.06 -- Checkpoint: M1 Foundation Verified\n"
            "**Checkpoint Report Path:** `checkpoints/CP-P01-END.md`\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert len(result) == 1
        name, path = result[0]
        assert name == "M1 Foundation Verified"
        assert path == (tmp_path / "checkpoints" / "CP-P01-END.md").resolve()

    def test_wave4_mid_and_end_mixed_with_legacy(self, tmp_path: Path):
        """Phase file may have both Wave-4 and legacy headings; both must
        yield human-readable names, not basenames."""
        phase_file = tmp_path / "phase-3-tasklist.md"
        phase_file.write_text(
            "### T03.06 -- Checkpoint: M3 Authenticated Flow Verified (Mid-phase)\n"
            "**Checkpoint Report Path:** `checkpoints/CP-P03-MID-AUTHFLOW.md`\n\n"
            "### Checkpoint: End of Phase 3\n"
            "Checkpoint Report Path: checkpoints/CP-P03-END.md\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert [name for name, _ in result] == [
            "M3 Authenticated Flow Verified (Mid-phase)",
            "End of Phase 3",
        ]


# ---------------------------------------------------------------------------
# verify_checkpoint_files()
# ---------------------------------------------------------------------------


class TestVerifyCheckpointFiles:
    def test_all_present(self, tmp_path: Path):
        cp = tmp_path / "checkpoints"
        cp.mkdir()
        (cp / "a.md").write_text("ok")
        (cp / "b.md").write_text("ok")
        paths = [("A", cp / "a.md"), ("B", cp / "b.md")]
        result = verify_checkpoint_files(paths)
        assert [(n, bool(ok)) for n, _, ok in result] == [("A", True), ("B", True)]

    def test_mixed_present_and_missing(self, tmp_path: Path):
        cp = tmp_path / "checkpoints"
        cp.mkdir()
        (cp / "a.md").write_text("ok")
        paths = [("A", cp / "a.md"), ("B", cp / "b.md")]
        result = verify_checkpoint_files(paths)
        assert [bool(ok) for _, _, ok in result] == [True, False]

    def test_empty_input(self):
        assert verify_checkpoint_files([]) == []


# ---------------------------------------------------------------------------
# _verify_checkpoints() gate integration
# ---------------------------------------------------------------------------


def _build_phase(
    tmp_path: Path, *, with_missing: bool = True
) -> tuple[SprintConfig, Phase]:
    """Create a sprint workspace with a phase that declares two checkpoints."""
    phases_dir = tmp_path / "phases"
    phases_dir.mkdir()
    phase_file = phases_dir / "phase-3-tasklist.md"
    phase_file.write_text(
        "### Checkpoint: Mid-P3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-T01-T05.md\n\n"
        "### Checkpoint: End of P3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-END.md\n"
    )
    cp = tmp_path / "checkpoints"
    cp.mkdir()
    (cp / "CP-P03-T01-T05.md").write_text("ok")
    if not with_missing:
        (cp / "CP-P03-END.md").write_text("ok")
    return (
        SprintConfig(release_dir=tmp_path, checkpoint_gate_mode="shadow"),
        Phase(number=3, file=phase_file, name="Phase 3"),
    )


def _read_events(config: SprintConfig) -> list[dict]:
    path = config.execution_log_jsonl
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class TestVerifyCheckpointsGate:
    def test_off_mode_is_noop(self, tmp_path: Path):
        config, phase = _build_phase(tmp_path)
        config.checkpoint_gate_mode = "off"
        logger = SprintLogger(config)
        new_status = _verify_checkpoints(config, phase, PhaseStatus.PASS, logger)
        assert new_status == PhaseStatus.PASS
        assert _read_events(config) == []

    def test_shadow_mode_emits_event_no_stdout(self, tmp_path: Path):
        config, phase = _build_phase(tmp_path)
        config.checkpoint_gate_mode = "shadow"
        logger = SprintLogger(config)
        buf = io.StringIO()
        with redirect_stdout(buf):
            new_status = _verify_checkpoints(config, phase, PhaseStatus.PASS, logger)
        assert new_status == PhaseStatus.PASS
        assert buf.getvalue() == ""
        events = [
            e for e in _read_events(config) if e["event"] == "checkpoint_verification"
        ]
        assert len(events) == 1
        evt = events[0]
        assert evt["phase"] == 3
        assert len(evt["expected"]) == 2
        assert len(evt["missing"]) == 1
        assert evt["missing"][0].endswith("CP-P03-END.md")

    def test_soft_mode_prints_warning(self, tmp_path: Path):
        config, phase = _build_phase(tmp_path)
        config.checkpoint_gate_mode = "soft"
        logger = SprintLogger(config)
        buf = io.StringIO()
        with redirect_stdout(buf):
            new_status = _verify_checkpoints(config, phase, PhaseStatus.PASS, logger)
        assert new_status == PhaseStatus.PASS
        assert "Phase 3" in buf.getvalue()
        assert "checkpoint" in buf.getvalue().lower()
        assert any(
            e["event"] == "checkpoint_verification" for e in _read_events(config)
        )

    def test_full_mode_downgrades_status_on_missing(self, tmp_path: Path):
        config, phase = _build_phase(tmp_path)
        config.checkpoint_gate_mode = "full"
        logger = SprintLogger(config)
        new_status = _verify_checkpoints(config, phase, PhaseStatus.PASS, logger)
        assert new_status == PhaseStatus.PASS_MISSING_CHECKPOINT
        assert new_status.is_success is True
        assert new_status.is_failure is False

    def test_full_mode_leaves_pass_when_all_present(self, tmp_path: Path):
        config, phase = _build_phase(tmp_path, with_missing=False)
        config.checkpoint_gate_mode = "full"
        logger = SprintLogger(config)
        new_status = _verify_checkpoints(config, phase, PhaseStatus.PASS, logger)
        assert new_status == PhaseStatus.PASS
        evt = next(
            e for e in _read_events(config) if e["event"] == "checkpoint_verification"
        )
        assert evt["missing"] == []

    def test_no_checkpoint_sections_skips_event(self, tmp_path: Path):
        config, phase = _build_phase(tmp_path)
        config.checkpoint_gate_mode = "shadow"
        phase.file.write_text("# Phase with no checkpoints\n### T03.01 Task\n")
        logger = SprintLogger(config)
        new_status = _verify_checkpoints(config, phase, PhaseStatus.PASS, logger)
        assert new_status == PhaseStatus.PASS
        assert not any(
            e.get("event") == "checkpoint_verification" for e in _read_events(config)
        )


# ---------------------------------------------------------------------------
# PhaseStatus.PASS_MISSING_CHECKPOINT contract
# ---------------------------------------------------------------------------


class TestPassMissingCheckpointStatus:
    def test_value_and_properties(self):
        s = PhaseStatus.PASS_MISSING_CHECKPOINT
        assert s.value == "pass_missing_checkpoint"
        assert s.is_success is True
        assert s.is_failure is False
        assert s.is_terminal is True

    def test_checkpoint_gate_mode_default_is_shadow(self):
        cfg = SprintConfig()
        assert cfg.checkpoint_gate_mode == "shadow"

    def test_checkpoint_gate_mode_accepts_all_modes(self):
        for mode in ("off", "shadow", "soft", "full"):
            cfg = SprintConfig(checkpoint_gate_mode=mode)
            assert cfg.checkpoint_gate_mode == mode


# ---------------------------------------------------------------------------
# Wave 3 — build_manifest / write_manifest
# ---------------------------------------------------------------------------


def _seed_sprint(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Create a three-phase sprint workspace. Returns (index, p1, p2, p3)."""
    p1 = tmp_path / "phase-1-tasklist.md"
    p2 = tmp_path / "phase-2-tasklist.md"
    p3 = tmp_path / "phase-3-tasklist.md"
    index = tmp_path / "tasklist-index.md"
    index.write_text(
        "# Sprint\n\n"
        "| # | File |\n|---|------|\n"
        f"| 1 | {p1.name} |\n"
        f"| 2 | {p2.name} |\n"
        f"| 3 | {p3.name} |\n"
    )
    p1.write_text(
        "### Checkpoint: End of Phase 1\n"
        "Checkpoint Report Path: checkpoints/CP-P01-END.md\n"
    )
    p2.write_text("# Phase with no checkpoints\n### T02.01 Task body\n")
    p3.write_text(
        "### Checkpoint: Mid Phase 3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-MID.md\n\n"
        "### Checkpoint: End of Phase 3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-END.md\n"
        "**Verification:**\n"
        "- Configuration module loads\n"
        "- Utilities module works\n"
    )
    return index, p1, p2, p3


class TestBuildManifest:
    def test_zero_phase_index_returns_empty(self, tmp_path: Path):
        index = tmp_path / "tasklist-index.md"
        index.write_text("# Empty sprint\n\n| # | File |\n|---|------|\n")
        assert build_manifest(index, tmp_path) == []

    def test_single_phase_with_one_checkpoint(self, tmp_path: Path):
        p1 = tmp_path / "phase-1-tasklist.md"
        index = tmp_path / "tasklist-index.md"
        index.write_text(f"# Sprint\n\n| # | File |\n|---|------|\n| 1 | {p1.name} |\n")
        p1.write_text(
            "### Checkpoint: End of Phase 1\n"
            "Checkpoint Report Path: checkpoints/CP-P01-END.md\n"
        )
        manifest = build_manifest(index, tmp_path)
        assert len(manifest) == 1
        assert manifest[0].phase == 1
        assert manifest[0].exists is False
        assert manifest[0].recovered is False
        assert manifest[0].recovery_source is None

    def test_multi_phase_with_mixed_counts(self, tmp_path: Path):
        index, p1, p2, p3 = _seed_sprint(tmp_path)
        (tmp_path / "checkpoints").mkdir()
        (tmp_path / "checkpoints" / "CP-P01-END.md").write_text("ok")

        manifest = build_manifest(index, tmp_path)
        # P1: 1 (found), P2: 0, P3: 2 (both missing) = 3 entries
        assert [e.phase for e in manifest] == [1, 3, 3]
        assert [e.exists for e in manifest] == [True, False, False]

    def test_missing_index_returns_empty(self, tmp_path: Path):
        assert build_manifest(tmp_path / "does-not-exist.md", tmp_path) == []


class TestWriteManifest:
    def test_writes_valid_json_with_summary(self, tmp_path: Path):
        index, _, _, _ = _seed_sprint(tmp_path)
        (tmp_path / "checkpoints").mkdir()
        (tmp_path / "checkpoints" / "CP-P01-END.md").write_text("ok")
        manifest = build_manifest(index, tmp_path)

        out = tmp_path / "manifest.json"
        write_manifest(manifest, out)
        data = json.loads(out.read_text())
        assert data["summary"] == {
            "total": 3,
            "found": 1,
            "missing": 2,
            "recovered": 0,
        }
        assert len(data["entries"]) == 3
        assert "generated_at" in data
        assert data["entries"][0]["expected_path"].endswith("CP-P01-END.md")

    def test_recovered_entries_counted_in_summary(self, tmp_path: Path):
        entry = CheckpointEntry(
            phase=1,
            name="X",
            expected_path=tmp_path / "x.md",
            exists=True,
            recovered=True,
            recovery_source="artifacts/D-0001",
        )
        out = tmp_path / "manifest.json"
        write_manifest([entry], out)
        data = json.loads(out.read_text())
        assert data["summary"]["recovered"] == 1
        assert data["entries"][0]["recovery_source"] == "artifacts/D-0001"

    def test_atomic_write_replaces_existing(self, tmp_path: Path):
        out = tmp_path / "manifest.json"
        out.write_text('{"stale": true}\n')
        write_manifest([], out)
        data = json.loads(out.read_text())
        assert data["summary"]["total"] == 0
        assert "stale" not in data


# ---------------------------------------------------------------------------
# Wave 3 — recover_missing_checkpoints
# ---------------------------------------------------------------------------


class TestRecoverMissingCheckpoints:
    def test_generates_file_with_auto_recovered_marker(self, tmp_path: Path):
        index, _, _, p3 = _seed_sprint(tmp_path)
        # Evidence referencing phase 3 tasks.
        (tmp_path / "artifacts" / "D-0013").mkdir(parents=True)
        (tmp_path / "artifacts" / "D-0013" / "config.md").write_text(
            "Task T03.01 delivered configuration module."
        )
        (tmp_path / "artifacts" / "D-0014").mkdir()
        (tmp_path / "artifacts" / "D-0014" / "util.md").write_text(
            "Task T03.02 delivered utilities."
        )

        manifest = build_manifest(index, tmp_path)
        recovered = recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {3: p3}
        )
        # Phase 3 has two missing checkpoints; both should be recovered.
        p3_entries = [e for e in recovered if e.phase == 3]
        assert len(p3_entries) == 2
        for e in p3_entries:
            assert e.exists is True
            assert e.recovered is True
            assert e.recovery_source
            body = e.expected_path.read_text()
            assert "Auto-Recovered" in body
            assert "recovered: true" in body

    def test_idempotent_second_run_does_not_overwrite(self, tmp_path: Path):
        index, _, _, p3 = _seed_sprint(tmp_path)
        (tmp_path / "artifacts" / "D-0013").mkdir(parents=True)
        (tmp_path / "artifacts" / "D-0013" / "work.md").write_text("Task T03.01 worked")

        manifest = build_manifest(index, tmp_path)
        first = recover_missing_checkpoints(manifest, tmp_path / "artifacts", {3: p3})
        # Snapshot bodies after first run.
        snapshot = {
            e.expected_path: e.expected_path.read_text() for e in first if e.recovered
        }
        # Fresh manifest — these files now exist on disk.
        manifest2 = build_manifest(index, tmp_path)
        second = recover_missing_checkpoints(manifest2, tmp_path / "artifacts", {3: p3})
        for path, content in snapshot.items():
            assert path.read_text() == content, f"overwrote {path}"
        # Second-run entries should reflect the files already exist.
        assert all(e.exists for e in second if e.phase == 3)

    def test_does_not_overwrite_pre_existing_file(self, tmp_path: Path):
        existing = tmp_path / "existing.md"
        existing.write_text("original body")
        entry = CheckpointEntry(
            phase=5,
            name="End of 5",
            expected_path=existing,
            exists=False,
        )
        result = recover_missing_checkpoints([entry], tmp_path, {})
        assert existing.read_text() == "original body"
        # The returned entry should now reflect exists=True.
        assert result[0].exists is True

    def test_wave4_verification_block_copied_into_recovered_report(
        self, tmp_path: Path
    ):
        """Wave-4 `### T<PP>.<NN> -- Checkpoint: <name>` tasks must round-trip
        through extract_checkpoint_paths → recover_missing_checkpoints such
        that the rendered report contains the Verification / Exit Criteria
        block from the task body, not the 'no verification block' fallback.
        """
        p1 = tmp_path / "phase-1-tasklist.md"
        index = tmp_path / "tasklist-index.md"
        index.write_text(f"# Sprint\n\n| # | File |\n|---|------|\n| 1 | {p1.name} |\n")
        p1.write_text(
            "### T01.06 -- Checkpoint: M1 Foundation Verified\n"
            "**Purpose:** Verify M1 foundation deliverables.\n"
            "**Checkpoint Report Path:** `checkpoints/CP-P01-END.md`\n\n"
            "**Verification:**\n"
            "- TEST-M1-001 green\n"
            "- TEST-M1-003 green in CI\n\n"
            "**Exit Criteria:**\n"
            "- All migrations reversible\n"
            "- Keys stored in secrets manager\n"
        )

        manifest = build_manifest(index, tmp_path)
        assert len(manifest) == 1
        # Pre-fix regression: name fell back to basename. After fix it must
        # resolve to the heading label from the Wave-4 task.
        assert manifest[0].name == "M1 Foundation Verified"

        recovered = recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {1: p1}
        )
        body = recovered[0].expected_path.read_text()
        # Positive: verification + exit criteria copied verbatim.
        assert "**Verification:**" in body
        assert "TEST-M1-001 green" in body
        assert "**Exit Criteria:**" in body
        assert "All migrations reversible" in body
        # Negative: no fallback sentinel.
        assert "no verification block found" not in body

    def test_phase_without_tasklist_is_skipped(self, tmp_path: Path):
        missing_path = tmp_path / "ck.md"
        entry = CheckpointEntry(
            phase=9,
            name="End",
            expected_path=missing_path,
            exists=False,
        )
        # No tasklist provided for phase 9.
        result = recover_missing_checkpoints([entry], tmp_path, {})
        assert missing_path.exists() is False
        assert result[0].exists is False
        assert result[0].recovered is False

    def test_recover_reevaluates_stale_fail_to_unknown(self, tmp_path: Path):
        """Defect-2 regression (positive): with ``reevaluate_stale=True``, an
        EXISTING stale FAIL/BLOCKED end-of-phase checkpoint whose phase has
        recovered (fresh passing evidence present) is re-stamped to
        UNKNOWN/Auto-Recovered — never left verbatim, and NEVER auto-PASS."""
        index, _, _, p3 = _seed_sprint(tmp_path)
        # Fresh passing evidence for the phase-3 gating tasks.
        (tmp_path / "artifacts" / "D-0013").mkdir(parents=True)
        (tmp_path / "artifacts" / "D-0013" / "config.md").write_text(
            "Task T03.01 delivered configuration module."
        )
        (tmp_path / "artifacts" / "D-0014").mkdir()
        (tmp_path / "artifacts" / "D-0014" / "util.md").write_text(
            "Task T03.02 delivered utilities."
        )
        # Pre-seed an EXISTING stale FAIL checkpoint report (agent-written
        # status: fail frontmatter + a FAIL ## Result body).
        checkpoints_dir = tmp_path / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        (checkpoints_dir / "CP-P03-END.md").write_text(
            "---\n"
            "checkpoint: End of Phase 3\n"
            "phase: 3\n"
            "status: fail\n"
            "generated_at: 2026-06-01T00:00:00Z\n"
            "---\n\n"
            "## Result\n\n"
            "`FAIL` — gating tasks did not pass.\n",
            encoding="utf-8",
        )

        manifest = build_manifest(index, tmp_path)
        recovered = recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {3: p3}, reevaluate_stale=True
        )

        end_entry = next(
            e
            for e in recovered
            if e.phase == 3 and e.expected_path.name == "CP-P03-END.md"
        )
        body = end_entry.expected_path.read_text(encoding="utf-8")
        # Stale FAIL verdict was re-stamped, not left verbatim.
        assert "recovered: true" in body
        assert "Auto-Recovered" in body
        assert "`UNKNOWN`" in body
        assert "status: fail" not in body
        # NEVER auto-PASS — the executor's _check_checkpoint_pass PASS tokens
        # must be absent from the re-stamped report.
        upper = body.upper()
        assert "STATUS: PASS" not in upper
        assert "**RESULT**: PASS" not in upper
        assert end_entry.recovered is True

    def test_recover_preserves_fail_when_tasks_still_failing(self, tmp_path: Path):
        """Defect-2 regression (negative): when the phase's gating tasks did NOT
        recover (no fresh passing evidence), the re-stamp branch must NOT fire —
        the stale FAIL verdict is preserved verbatim."""
        index, _, _, p3 = _seed_sprint(tmp_path)
        # No passing evidence seeded ⇒ the now-pass precondition is NOT met.
        checkpoints_dir = tmp_path / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        end_report = checkpoints_dir / "CP-P03-END.md"
        stale = (
            "---\n"
            "checkpoint: End of Phase 3\n"
            "phase: 3\n"
            "status: fail\n"
            "generated_at: 2026-06-01T00:00:00Z\n"
            "---\n\n"
            "## Result\n\n"
            "`FAIL` — gating tasks did not pass.\n"
        )
        end_report.write_text(stale, encoding="utf-8")

        manifest = build_manifest(index, tmp_path)
        recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {3: p3}, reevaluate_stale=True
        )

        # Stale FAIL preserved byte-identically — no UNKNOWN re-stamp fired.
        assert end_report.read_text(encoding="utf-8") == stale

    def test_recovered_report_never_injects_gate_tokens(self, tmp_path: Path):
        """DEV-2 (Regression, MED): the recovered/re-stamped checkpoint renderer
        interpolates ``entry.name``, the verification block, and evidence paths.
        The executor gate reader (``_check_checkpoint_pass``) does a case-
        insensitive substring match for ``STATUS: PASS`` / ``**RESULT**: PASS``.
        If any interpolated field carries those tokens verbatim, a re-stamped
        UNKNOWN report reads as PASS at the gate. This test injects the gate
        tokens into EACH interpolated field separately and asserts the rendered
        report contains NEITHER token (uppercased) while the ## Result line still
        reads UNKNOWN. Pre-fix the renderer interpolates verbatim ⇒ FAIL."""
        from superclaude.cli.sprint.checkpoints import _render_recovered_checkpoint

        token_a = "STATUS: PASS"
        token_b = "**RESULT**: PASS"

        def _assert_clean(body: str, where: str):
            upper = body.upper()
            assert token_a not in upper, f"{token_a} leaked via {where}"
            assert token_b.upper() not in upper, f"{token_b} leaked via {where}"
            # The genuine verdict must remain UNKNOWN/Auto-Recovered.
            assert "`UNKNOWN`" in body
            assert "Auto-Recovered" in body

        # 1) Injected via entry.name
        entry_name = CheckpointEntry(
            phase=3,
            name=f"End of Phase 3 -- {token_b} expected",
            expected_path=tmp_path / "checkpoints" / "CP-P03-END.md",
            exists=True,
        )
        body_name = _render_recovered_checkpoint(
            entry=entry_name,
            verification_block="- gating tasks green",
            evidence=[tmp_path / "artifacts" / "D-1" / "proof.md"],
        )
        _assert_clean(body_name, "entry.name")

        # 2) Injected via the verification block (the realistic vector — prose
        #    copied verbatim from the tasklist's verification criteria).
        entry = CheckpointEntry(
            phase=3,
            name="End of Phase 3",
            expected_path=tmp_path / "checkpoints" / "CP-P03-END.md",
            exists=True,
        )
        body_vblock = _render_recovered_checkpoint(
            entry=entry,
            verification_block=f"- Gate requires {token_b} from the smoke suite\n- confirm {token_a} in CI",
            evidence=[tmp_path / "artifacts" / "D-1" / "proof.md"],
        )
        _assert_clean(body_vblock, "verification_block")

        # 3) Injected via an evidence path component
        body_evid = _render_recovered_checkpoint(
            entry=entry,
            verification_block="- gating tasks green",
            evidence=[tmp_path / "artifacts" / "STATUS: PASS" / "proof.md"],
        )
        _assert_clean(body_evid, "evidence path")

    def _seed_stale_checkpoint(
        self, tmp_path: Path, verdict: str, *, frontmatter: bool
    ):
        """Seed an existing stale CP-P03-END.md with the given verdict, optionally
        carrying a ``status:`` frontmatter key. Returns the report path + content."""
        checkpoints_dir = tmp_path / "checkpoints"
        checkpoints_dir.mkdir(parents=True, exist_ok=True)
        report = checkpoints_dir / "CP-P03-END.md"
        if frontmatter:
            content = (
                "---\n"
                "checkpoint: End of Phase 3\n"
                "phase: 3\n"
                f"status: {verdict.lower()}\n"
                "generated_at: 2026-06-01T00:00:00Z\n"
                "---\n\n"
                "## Result\n\n"
                f"`{verdict}` — gating tasks did not pass.\n"
            )
        else:
            # NO status: frontmatter key — only a ## Result body token, exercising
            # the body-only parse path that the existing positive test never hits.
            content = (
                "---\n"
                "checkpoint: End of Phase 3\n"
                "phase: 3\n"
                "generated_at: 2026-06-01T00:00:00Z\n"
                "---\n\n"
                "## Result\n\n"
                f"`{verdict}` — gating tasks did not pass.\n"
            )
        report.write_text(content, encoding="utf-8")
        return report, content

    def _seed_phase3_evidence(self, tmp_path: Path):
        """Seed fresh passing evidence for the phase-3 gating tasks."""
        (tmp_path / "artifacts" / "D-0013").mkdir(parents=True, exist_ok=True)
        (tmp_path / "artifacts" / "D-0013" / "config.md").write_text(
            "Task T03.01 delivered configuration module."
        )
        (tmp_path / "artifacts" / "D-0014").mkdir(parents=True, exist_ok=True)
        (tmp_path / "artifacts" / "D-0014" / "util.md").write_text(
            "Task T03.02 delivered utilities."
        )

    def test_recover_reevaluates_stale_blocked_to_unknown(self, tmp_path: Path):
        """FIX-4: the re-stamp branch fires on ``BLOCKED`` as well as ``FAIL``
        (the trigger is ``in ("FAIL", "BLOCKED")``) — the existing positive test
        only covers FAIL, leaving the BLOCKED arm unexercised."""
        index, _, _, p3 = _seed_sprint(tmp_path)
        self._seed_phase3_evidence(tmp_path)
        report, _ = self._seed_stale_checkpoint(tmp_path, "BLOCKED", frontmatter=True)

        manifest = build_manifest(index, tmp_path)
        recovered = recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {3: p3}, reevaluate_stale=True
        )
        end_entry = next(
            e
            for e in recovered
            if e.phase == 3 and e.expected_path.name == "CP-P03-END.md"
        )
        body = end_entry.expected_path.read_text(encoding="utf-8")
        assert "recovered: true" in body
        assert "Auto-Recovered" in body
        assert "`UNKNOWN`" in body
        assert "status: blocked" not in body
        upper = body.upper()
        assert "STATUS: PASS" not in upper and "**RESULT**: PASS" not in upper
        assert end_entry.recovered is True

    def test_recover_reevaluates_body_only_stale_verdict(self, tmp_path: Path):
        """FIX-4: a stale verdict carried ONLY in the ``## Result`` body (no
        ``status:`` frontmatter) is parsed and re-stamped — the existing positive
        test seeds both, so the body-only parse path is otherwise untested."""
        index, _, _, p3 = _seed_sprint(tmp_path)
        self._seed_phase3_evidence(tmp_path)
        report, _ = self._seed_stale_checkpoint(tmp_path, "FAIL", frontmatter=False)

        manifest = build_manifest(index, tmp_path)
        recovered = recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {3: p3}, reevaluate_stale=True
        )
        end_entry = next(
            e
            for e in recovered
            if e.phase == 3 and e.expected_path.name == "CP-P03-END.md"
        )
        body = end_entry.expected_path.read_text(encoding="utf-8")
        # Body-only stale FAIL was read and re-stamped to UNKNOWN/Auto-Recovered.
        assert "Auto-Recovered" in body
        assert "`UNKNOWN`" in body
        assert end_entry.recovered is True

    def test_recover_restamp_is_idempotent_on_second_run(self, tmp_path: Path):
        """FIX-4: re-stamping is idempotent — once a stale FAIL is re-stamped to
        UNKNOWN, a second ``reevaluate_stale=True`` pass must NOT re-fire (the
        UNKNOWN verdict is no longer FAIL/BLOCKED, so the branch is inert)."""
        index, _, _, p3 = _seed_sprint(tmp_path)
        self._seed_phase3_evidence(tmp_path)
        report, _ = self._seed_stale_checkpoint(tmp_path, "FAIL", frontmatter=True)

        manifest = build_manifest(index, tmp_path)
        recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {3: p3}, reevaluate_stale=True
        )
        after_first = report.read_text(encoding="utf-8")
        assert "`UNKNOWN`" in after_first  # first pass re-stamped it

        # Second pass over the now-UNKNOWN report must leave it byte-identical.
        manifest2 = build_manifest(index, tmp_path)
        recover_missing_checkpoints(
            manifest2, tmp_path / "artifacts", {3: p3}, reevaluate_stale=True
        )
        after_second = report.read_text(encoding="utf-8")
        assert after_second == after_first

    def test_recover_default_off_preserves_fail_even_with_evidence(
        self, tmp_path: Path
    ):
        """FIX-4: with ``reevaluate_stale=False`` (default), an existing stale FAIL
        is left UNTOUCHED even when fresh passing evidence IS present — proving the
        re-stamp is gated strictly on the flag, not on evidence presence."""
        index, _, _, p3 = _seed_sprint(tmp_path)
        self._seed_phase3_evidence(tmp_path)  # evidence present...
        report, stale = self._seed_stale_checkpoint(tmp_path, "FAIL", frontmatter=True)

        manifest = build_manifest(index, tmp_path)
        recover_missing_checkpoints(
            manifest,
            tmp_path / "artifacts",
            {3: p3},  # ...but reevaluate_stale defaults False
        )
        # Default-off ⇒ the stale FAIL is preserved byte-identically.
        assert report.read_text(encoding="utf-8") == stale


# ---------------------------------------------------------------------------
# Wave 3 — verify-checkpoints CLI subcommand
# ---------------------------------------------------------------------------


class TestVerifyCheckpointsCLI:
    def test_table_output_reports_counts(self, tmp_path: Path):
        index, _, _, _ = _seed_sprint(tmp_path)
        (tmp_path / "checkpoints").mkdir()
        (tmp_path / "checkpoints" / "CP-P01-END.md").write_text("ok")

        runner = CliRunner()
        result = runner.invoke(verify_checkpoints, [str(tmp_path)])
        assert result.exit_code == 0, result.output
        assert "3 declared" in result.output
        assert "1 found" in result.output
        assert "2 missing" in result.output
        assert (tmp_path / "manifest.json").exists()

    def test_json_flag_emits_parseable_manifest(self, tmp_path: Path):
        index, *_ = _seed_sprint(tmp_path)
        runner = CliRunner()
        result = runner.invoke(verify_checkpoints, [str(tmp_path), "--json"])
        assert result.exit_code == 0, result.output
        data = json.loads(result.output)
        assert data["summary"]["total"] == 3
        # Table header must NOT appear in JSON mode.
        assert "Phase  Status" not in result.output

    def test_recover_flag_regenerates_missing_reports(self, tmp_path: Path):
        index, _, _, p3 = _seed_sprint(tmp_path)
        (tmp_path / "artifacts" / "D-0003").mkdir(parents=True)
        (tmp_path / "artifacts" / "D-0003" / "work.md").write_text(
            "Task T03.01 delivered configuration module."
        )
        runner = CliRunner()
        result = runner.invoke(verify_checkpoints, [str(tmp_path), "--recover"])
        assert result.exit_code == 0, result.output
        assert "recovered" in result.output.lower()
        # After recovery, files must exist on disk.
        assert (tmp_path / "checkpoints" / "CP-P03-END.md").exists()
        assert (tmp_path / "checkpoints" / "CP-P03-MID.md").exists()

    def test_missing_index_file_errors_cleanly(self, tmp_path: Path):
        runner = CliRunner()
        result = runner.invoke(verify_checkpoints, [str(tmp_path)])
        assert result.exit_code != 0
        assert "tasklist-index.md" in result.output

    def test_phase_option_is_rejected(self, tmp_path: Path):
        """Contract lock: verify-checkpoints supports neither --phase nor --quiet.

        Regression guard for the rerun-tasks auto-invoke that shelled out with
        `--recover --phase N --quiet` and crashed with "No such option: --phase".
        The command's surface is the positional OUTPUT_DIR plus --recover/--json.
        """
        runner = CliRunner()
        result = runner.invoke(
            verify_checkpoints, [str(tmp_path), "--recover", "--phase", "13"]
        )
        assert result.exit_code == 2, result.output
        assert "No such option" in result.output

        # --quiet is independently unsupported.
        result_quiet = runner.invoke(
            verify_checkpoints, [str(tmp_path), "--recover", "--quiet"]
        )
        assert result_quiet.exit_code == 2, result_quiet.output
        assert "No such option" in result_quiet.output


# ---------------------------------------------------------------------------
# Wave / Phase 3 — merge_recovery_bundle → RecoveryBundle / RecoveryStatus
# ---------------------------------------------------------------------------


def _full_recovery_manifest(tmp_path: Path) -> tuple[Path, RecoveryBundle]:
    """Seed a phase-3-filtered recovery workspace and a RecoveryBundle that,
    when merged, completes cleanly and yields ``RecoveryStatus.SUCCESS``.

    Layout mirrors the canonical SprintConfig: ``release_dir`` == tmp_path so
    ``_resolve_release_dir(index)`` (= index.parent for a top-level index)
    resolves results to ``<tmp_path>/results``. The prior phase-3 canonical
    artifacts (task output + result.json) are written so the 7-step merge has
    real files to rename/replace, and a ``task-results.json`` sidecar is placed
    in the bundle dir so Step 7 refreshes result-json without recording a
    failure — the precondition for a SUCCESS (not PARTIAL) terminal status.
    """
    index = tmp_path / "tasklist-index.md"
    p3 = tmp_path / "phase-3-tasklist.md"
    index.write_text(f"# Sprint\n\n| # | File |\n|---|------|\n| 3 | {p3.name} |\n")
    p3.write_text(
        "### Checkpoint: End of Phase 3\n"
        "Checkpoint Report Path: checkpoints/CP-P03-END.md\n"
    )

    results_dir = tmp_path / "results"
    results_dir.mkdir()
    # Prior canonical artifacts for the affected task (will be preserved as
    # .failed-<ts> and replaced by the rerun's produced output).
    (results_dir / "phase-3-task-T03.01-output.txt").write_text("stale output")
    (results_dir / "phase-3-result.json").write_text(
        json.dumps(
            {
                "phase": 3,
                "task_results": [
                    {"task": {"task_id": "T03.01"}, "status": "failed"},
                    {"task": {"task_id": "T03.02"}, "status": "passed"},
                ],
                "recovery_history": [],
            }
        )
        + "\n"
    )

    # Bundle dir holds the rerun's produced artifacts + the sidecar.
    bundle_dir = results_dir / "rerun-bundle"
    bundle_dir.mkdir()
    produced_output = bundle_dir / "phase-3-task-T03.01-output.txt"
    produced_output.write_text("fresh rerun output")
    (bundle_dir / "task-results.json").write_text(
        json.dumps([{"task": {"task_id": "T03.01"}, "status": "passed"}]) + "\n"
    )

    bundle = RecoveryBundle(
        bundle_id="rerun-20260602T000000Z",
        affected_phase=3,
        affected_tasks=["T03.01"],
        artifacts_produced=[produced_output],
    )
    return index, bundle


class TestRecoverMissingReturnsRecoveryBundle:
    def test_merge_sets_status_success_and_end_sha(self, tmp_path: Path):
        index, bundle = _full_recovery_manifest(tmp_path)
        merge_recovery_bundle(bundle, index, release_dir=tmp_path)
        assert bundle.status == RecoveryStatus.SUCCESS
        assert bundle.status.is_terminal is True
        # end_tasklist_sha256 is populated at finalize from the on-disk index.
        assert bundle.end_tasklist_sha256
        assert len(bundle.end_tasklist_sha256) == 64

    def test_merge_preserves_prior_output_and_writes_fresh(self, tmp_path: Path):
        index, bundle = _full_recovery_manifest(tmp_path)
        results_dir = tmp_path / "results"
        merge_recovery_bundle(bundle, index, release_dir=tmp_path)
        # Canonical output now carries the rerun body...
        canonical = results_dir / "phase-3-task-T03.01-output.txt"
        assert canonical.read_text() == "fresh rerun output"
        # ...and the prior output survives as a forensic .failed-<ts> rename.
        preserved = list(results_dir.glob("phase-3-task-T03.01-output.failed-*.txt"))
        assert len(preserved) == 1
        assert preserved[0].read_text() == "stale output"
        assert bundle.artifacts_replaced[canonical] == preserved[0]

    def test_merge_refreshes_result_json_and_appends_history(self, tmp_path: Path):
        index, bundle = _full_recovery_manifest(tmp_path)
        results_dir = tmp_path / "results"
        merge_recovery_bundle(bundle, index, release_dir=tmp_path)
        data = json.loads((results_dir / "phase-3-result.json").read_text())
        # Affected task's entry refreshed from the sidecar (status now passed),
        # untouched task preserved.
        by_id = {r["task"]["task_id"]: r for r in data["task_results"]}
        assert by_id["T03.01"]["status"] == "passed"
        assert by_id["T03.02"]["status"] == "passed"
        # A SUCCESS RecoveryBundleRef was appended to recovery_history.
        assert len(data["recovery_history"]) == 1
        ref = data["recovery_history"][0]
        assert ref["bundle_id"] == bundle.bundle_id
        assert ref["status"] == RecoveryStatus.SUCCESS.value
