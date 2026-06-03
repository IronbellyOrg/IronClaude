"""Stage-0 H2 gate 1 — serial isolation smoke (real-subprocess e2e).

Replaces the un-exercisable "serial corruption" gate with a functionality-intact
smoke test: drive a small per-task sprint through the REAL spawn path (the
``claude_shim`` fake executable on ``$PATH`` — NOT ``_subprocess_factory``) and
assert that each isolated child actually received a per-task
``CLAUDE_SETTINGS_DIR`` (and ``CLAUDE_PLUGIN_DIR``) pointing under the release's
``.isolation`` tree. Before the H1 Path-B wiring, ``_run_task_subprocess`` passed
NO ``env_vars`` and the child inherited the parent env verbatim, so this test
fails loudly if the isolation env is absent.

The child env is observed via the ``fake_claude`` shim's additive ``env_log``
(each task records the isolation env it was spawned with into the shared control
file).
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from superclaude.cli.sprint.executor import execute_sprint


@pytest.mark.integration
class TestSerialIsolationSmoke:
    def test_each_task_child_receives_isolated_settings_dir(
        self, claude_shim, real_release
    ):
        config, _index = real_release
        # No failures: all three T01.NN tasks pass, exercising the real per-task
        # spawn path end to end.
        claude_shim.set_failures()

        with patch("superclaude.cli.sprint.notify._notify"):
            try:
                execute_sprint(config)
            except SystemExit as exc:  # all-pass sprint may exit(0)
                assert exc.code in (0, None), f"unexpected non-zero exit: {exc.code}"

        # The shim recorded the env each task child actually received.
        env_log = claude_shim.control().get("env_log", {})
        assert set(env_log) >= {"T01.01", "T01.02", "T01.03"}, (
            f"not all tasks spawned for real; env_log keys={sorted(env_log)}"
        )

        for tid, env in env_log.items():
            settings = env.get("CLAUDE_SETTINGS_DIR", "")
            plugin = env.get("CLAUDE_PLUGIN_DIR", "")
            # Isolation env must be present (the regression this gate guards).
            assert settings, f"{tid}: child received no CLAUDE_SETTINGS_DIR"
            assert plugin, f"{tid}: child received no CLAUDE_PLUGIN_DIR"
            # And it must be scoped under the release's .isolation tree so the
            # child resolves an isolated settings dir, not the real ~/.claude.
            assert ".isolation" in settings, (
                f"{tid}: CLAUDE_SETTINGS_DIR not under .isolation: {settings!r}"
            )
            assert "settings" in settings, (
                f"{tid}: CLAUDE_SETTINGS_DIR missing settings segment: {settings!r}"
            )
            assert f"task-{tid}" in settings, (
                f"{tid}: CLAUDE_SETTINGS_DIR not scoped to this task: {settings!r}"
            )
            assert ".isolation" in plugin, (
                f"{tid}: CLAUDE_PLUGIN_DIR not under .isolation: {plugin!r}"
            )

        # Per-task settings dirs must be pairwise distinct (one per task scope).
        settings_dirs = [e.get("CLAUDE_SETTINGS_DIR") for e in env_log.values()]
        assert len(set(settings_dirs)) == len(settings_dirs), (
            f"per-task CLAUDE_SETTINGS_DIR not unique across tasks: {settings_dirs}"
        )
