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

from superclaude.cli.sprint.checkpoints import (
    extract_checkpoint_paths,
    verify_checkpoint_files,
)
from superclaude.cli.sprint.executor import _verify_checkpoints
from superclaude.cli.sprint.logging_ import SprintLogger
from superclaude.cli.sprint.models import Phase, PhaseStatus, SprintConfig

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
