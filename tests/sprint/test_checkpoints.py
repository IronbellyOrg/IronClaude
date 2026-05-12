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
            "### Checkpoint: Abs\n"
            "Checkpoint Report Path: /abs/checkpoints/CP.md\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert result == [("Abs", Path("/abs/checkpoints/CP.md"))]

    def test_name_falls_back_to_basename(self, tmp_path: Path):
        phase_file = tmp_path / "phase.md"
        # Path declaration with no preceding `### Checkpoint:` heading.
        phase_file.write_text(
            "Checkpoint Report Path: checkpoints/CP-P01-END.md\n"
        )
        result = extract_checkpoint_paths(phase_file, tmp_path)
        assert result[0][0] == "CP-P01-END.md"

    def test_missing_phase_file_returns_empty(self, tmp_path: Path):
        assert extract_checkpoint_paths(
            tmp_path / "does-not-exist.md", tmp_path
        ) == []

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


def _build_phase(tmp_path: Path, *, with_missing: bool = True) -> tuple[SprintConfig, Phase]:
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
            new_status = _verify_checkpoints(
                config, phase, PhaseStatus.PASS, logger
            )
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
            new_status = _verify_checkpoints(
                config, phase, PhaseStatus.PASS, logger
            )
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
        index.write_text(
            "# Sprint\n\n| # | File |\n|---|------|\n"
            f"| 1 | {p1.name} |\n"
        )
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
        (tmp_path / "artifacts" / "D-0013" / "work.md").write_text(
            "Task T03.01 worked"
        )

        manifest = build_manifest(index, tmp_path)
        first = recover_missing_checkpoints(
            manifest, tmp_path / "artifacts", {3: p3}
        )
        # Snapshot bodies after first run.
        snapshot = {
            e.expected_path: e.expected_path.read_text()
            for e in first
            if e.recovered
        }
        # Fresh manifest — these files now exist on disk.
        manifest2 = build_manifest(index, tmp_path)
        second = recover_missing_checkpoints(
            manifest2, tmp_path / "artifacts", {3: p3}
        )
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
        index.write_text(
            "# Sprint\n\n| # | File |\n|---|------|\n"
            f"| 1 | {p1.name} |\n"
        )
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
        result = runner.invoke(
            verify_checkpoints, [str(tmp_path), "--recover"]
        )
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
