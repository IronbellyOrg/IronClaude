"""Regression tests for PR #63 comment r3275576561.

When ``shutil.copy2`` raises for every source file, all four installers
must surface the per-file failure details rather than returning the
misleading "nothing installed" sentinel via an early-return guard.

This locks in the fix that widened
``if not installed and not skipped`` to also require ``not failed``,
matching the precedent already in
``src/superclaude/cli/install_skills.py``.
"""

from __future__ import annotations

import shutil

import pytest

from superclaude.cli import install_agents as install_agents_mod
from superclaude.cli import install_commands as install_commands_mod
from superclaude.cli import install_core as install_core_mod
from superclaude.cli import install_templates as install_templates_mod


def _raise_permission_error(*_args, **_kwargs):
    raise PermissionError("simulated read-only target")


_INSTALLER_CASES = [
    pytest.param(
        install_templates_mod,
        "install_templates",
        "No templates were installed",
        id="templates",
    ),
    pytest.param(
        install_core_mod,
        "install_core_files",
        "No core framework files were installed",
        id="core",
    ),
    pytest.param(
        install_agents_mod,
        "install_agents",
        "No agents were installed",
        id="agents",
    ),
    pytest.param(
        install_commands_mod,
        "install_commands",
        "No commands were installed",
        id="commands",
    ),
]


@pytest.mark.parametrize("module,fn_name,empty_sentinel", _INSTALLER_CASES)
def test_install_surfaces_failure_details_on_copy_error(
    tmp_path, monkeypatch, module, fn_name, empty_sentinel
):
    """Every installer must return failure details, not the empty-source sentinel.

    Acceptance criteria from PR #63 r3275576561:
      (a) return tuple is (False, message)
      (b) message contains "❌ Failed to install" and per-file failure lines
      (c) message does NOT contain "source directory empty?" (or the
          installer's equivalent "nothing installed" sentinel)
      (d) message contains "📁 Installation directory:" footer
    """
    monkeypatch.setattr(shutil, "copy2", _raise_permission_error)

    installer = getattr(module, fn_name)
    target = tmp_path / "install_target"

    result = installer(target_path=target)

    assert isinstance(result, tuple) and len(result) == 2, (
        f"{fn_name} did not return a (success, message) tuple: {result!r}"
    )
    success, message = result

    # (a) success must be False
    assert success is False, (
        f"{fn_name} returned success=True despite PermissionError on every copy"
    )

    # (b) per-file failure details must be present
    assert "❌ Failed to install" in message, (
        f"{fn_name} message missing failure header:\n{message}"
    )
    assert "PermissionError" in message or "simulated read-only target" in message, (
        f"{fn_name} message missing per-file failure detail:\n{message}"
    )

    # (c) misleading "nothing installed" sentinel must NOT appear
    assert "source directory empty?" not in message, (
        f"{fn_name} returned the misleading empty-source message:\n{message}"
    )
    assert empty_sentinel not in message, (
        f"{fn_name} returned the empty-source sentinel '{empty_sentinel}' "
        f"instead of failure details:\n{message}"
    )

    # (d) installation directory footer must be present
    assert "📁 Installation directory:" in message, (
        f"{fn_name} message missing installation directory footer:\n{message}"
    )
