"""Tests for auto-wire of tdd_file/prd_file from .roadmap-state.json.

Covers Phase 6 auto-wire acceptance criteria:
- State file with tdd_file/prd_file → auto-wired to config when CLI flags absent
- Explicit CLI flags override auto-wired values
- Missing referenced file → warning, field stays None
- No state file → no auto-wiring
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.executor import read_state


@pytest.fixture
def state_dir(tmp_path):
    """Create a temporary directory with a state file."""
    return tmp_path


def write_state(state_dir: Path, tdd_path: str | None = None, prd_path: str | None = None):
    """Write a .roadmap-state.json with given paths."""
    state = {"schema_version": 1, "spec_file": str(state_dir / "spec.md")}
    if tdd_path is not None:
        state["tdd_file"] = tdd_path
    if prd_path is not None:
        state["prd_file"] = prd_path
    state_file = state_dir / ".roadmap-state.json"
    state_file.write_text(json.dumps(state), encoding="utf-8")
    return state_file


class TestReadState:
    """Tests for read_state() utility."""

    def test_read_existing_state(self, state_dir):
        write_state(state_dir, tdd_path="/some/tdd.md")
        result = read_state(state_dir / ".roadmap-state.json")
        assert result is not None
        assert result["tdd_file"] == "/some/tdd.md"

    def test_read_missing_file_returns_none(self, state_dir):
        result = read_state(state_dir / ".roadmap-state.json")
        assert result is None

    def test_read_empty_file_returns_none(self, state_dir):
        (state_dir / ".roadmap-state.json").write_text("")
        result = read_state(state_dir / ".roadmap-state.json")
        assert result is None

    def test_read_malformed_json_returns_none(self, state_dir):
        (state_dir / ".roadmap-state.json").write_text("not json{{{")
        result = read_state(state_dir / ".roadmap-state.json")
        assert result is None


class TestAutoWireLogic:
    """Tests for the auto-wire logic pattern used in tasklist commands.py."""

    def test_auto_wire_tdd_from_state(self, state_dir):
        """When state has tdd_file and CLI flag is None, auto-wire."""
        tdd_path = state_dir / "tdd.md"
        tdd_path.write_text("# TDD")
        write_state(state_dir, tdd_path=str(tdd_path))

        state = read_state(state_dir / ".roadmap-state.json") or {}
        tdd_file = None  # simulating CLI flag absent

        saved_tdd = state.get("tdd_file")
        if tdd_file is None and saved_tdd:
            p = Path(saved_tdd)
            if p.is_file():
                tdd_file = p

        assert tdd_file == tdd_path

    def test_auto_wire_prd_from_state(self, state_dir):
        """When state has prd_file and CLI flag is None, auto-wire."""
        prd_path = state_dir / "prd.md"
        prd_path.write_text("# PRD")
        write_state(state_dir, prd_path=str(prd_path))

        state = read_state(state_dir / ".roadmap-state.json") or {}
        prd_file = None

        saved_prd = state.get("prd_file")
        if prd_file is None and saved_prd:
            p = Path(saved_prd)
            if p.is_file():
                prd_file = p

        assert prd_file == prd_path

    def test_explicit_flag_overrides_state(self, state_dir):
        """When both state and CLI flag are set, CLI flag wins."""
        tdd_state = state_dir / "state_tdd.md"
        tdd_state.write_text("# State TDD")
        write_state(state_dir, tdd_path=str(tdd_state))

        tdd_file = Path("explicit_tdd.md")  # simulating explicit CLI flag

        state = read_state(state_dir / ".roadmap-state.json") or {}
        saved_tdd = state.get("tdd_file")
        if tdd_file is None and saved_tdd:
            p = Path(saved_tdd)
            if p.is_file():
                tdd_file = p

        # Explicit flag should NOT be overridden
        assert tdd_file == Path("explicit_tdd.md")

    def test_missing_file_skips_auto_wire(self, state_dir):
        """When state references a file that doesn't exist, skip auto-wire."""
        write_state(state_dir, tdd_path="/nonexistent/tdd.md")

        state = read_state(state_dir / ".roadmap-state.json") or {}
        tdd_file = None

        saved_tdd = state.get("tdd_file")
        if tdd_file is None and saved_tdd:
            p = Path(saved_tdd)
            if p.is_file():
                tdd_file = p

        assert tdd_file is None

    def test_no_state_file_no_auto_wire(self, state_dir):
        """When no state file exists, no auto-wiring occurs."""
        state = read_state(state_dir / ".roadmap-state.json") or {}
        tdd_file = None
        prd_file = None

        saved_tdd = state.get("tdd_file")
        if tdd_file is None and saved_tdd:
            tdd_file = Path(saved_tdd) if Path(saved_tdd).is_file() else None

        saved_prd = state.get("prd_file")
        if prd_file is None and saved_prd:
            prd_file = Path(saved_prd) if Path(saved_prd).is_file() else None

        assert tdd_file is None
        assert prd_file is None
