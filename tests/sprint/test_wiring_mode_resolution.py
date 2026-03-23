"""Tests for _resolve_wiring_mode() in sprint executor.

Verifies scope-based gate resolution, fallback to direct mode,
grace-period shadow forcing, and enabled=False producing 'off'.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.sprint.executor import _resolve_wiring_mode
from superclaude.cli.sprint.models import (
    Phase,
    SHADOW_GRACE_INFINITE,
    SprintConfig,
)


def _make_config(tmp_path: Path, **overrides) -> SprintConfig:
    """Build a minimal SprintConfig with wiring-gate overrides."""
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")

    defaults = dict(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        start_phase=1,
        end_phase=1,
        max_turns=5,
        wiring_gate_mode="soft",
        wiring_gate_scope="none",
        wiring_gate_enabled=True,
        wiring_gate_grace_period=0,
    )
    defaults.update(overrides)
    return SprintConfig(**defaults)


class TestResolveWiringMode:
    """Unit tests for _resolve_wiring_mode() scope resolution logic."""

    def test_resolve_uses_scope_when_set(self, tmp_path: Path) -> None:
        """When wiring_gate_scope is a recognized scope ('task'),
        _resolve_wiring_mode delegates to resolve_gate_mode().

        Task scope with grace_period=0 yields GateMode.BLOCKING -> 'full'.
        """
        config = _make_config(tmp_path, wiring_gate_scope="task", wiring_gate_grace_period=0)
        result = _resolve_wiring_mode(config)
        # task scope + grace_period=0 -> GateMode.BLOCKING -> "full"
        assert result == "full"

    def test_resolve_falls_back_to_direct_mode(self, tmp_path: Path) -> None:
        """When wiring_gate_scope is not in the scope_map (e.g. 'none'),
        _resolve_wiring_mode returns config.wiring_gate_mode directly.
        """
        config = _make_config(tmp_path, wiring_gate_scope="none", wiring_gate_mode="soft")
        result = _resolve_wiring_mode(config)
        assert result == "soft"

    def test_grace_period_forces_shadow(self, tmp_path: Path) -> None:
        """A grace_period >= SHADOW_GRACE_INFINITE causes SprintConfig.__post_init__
        to set wiring_gate_mode='shadow'. With scope='none' (fallback path),
        _resolve_wiring_mode returns that derived 'shadow' value.

        Additionally, with a recognized scope like 'task' and any positive
        grace_period, resolve_gate_mode returns TRAILING which maps to 'shadow'.
        """
        # Path A: __post_init__ derives "shadow" via SHADOW_GRACE_INFINITE,
        # and scope="none" causes fallback to the derived wiring_gate_mode.
        config_fallback = _make_config(
            tmp_path,
            wiring_gate_scope="none",
            wiring_gate_grace_period=SHADOW_GRACE_INFINITE,
        )
        assert _resolve_wiring_mode(config_fallback) == "shadow"

        # Path B: scope="task" + grace_period>0 -> TRAILING -> "shadow"
        config_scope = _make_config(
            tmp_path,
            wiring_gate_scope="task",
            wiring_gate_grace_period=10,
        )
        assert _resolve_wiring_mode(config_scope) == "shadow"

    def test_enabled_false_forces_off(self, tmp_path: Path) -> None:
        """When wiring_gate_enabled=False, SprintConfig.__post_init__ sets
        wiring_gate_mode='off'. With scope='none' (fallback path),
        _resolve_wiring_mode returns 'off'.

        The caller run_post_task_wiring_hook then short-circuits on mode=='off'.
        """
        config = _make_config(
            tmp_path,
            wiring_gate_enabled=False,
            wiring_gate_scope="none",
        )
        result = _resolve_wiring_mode(config)
        assert result == "off"
