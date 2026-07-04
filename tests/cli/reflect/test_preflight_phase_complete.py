"""RED-first unit tests for preflight()'s phase-incompleteness guard (REPORT §9).

R-002 D-I1: the guard blocks on any unchecked ``- [ ]`` item BEFORE the reflect-gate
boundary token (``superclaude reflect run`` / ``SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE``);
it fails open for sprint ``### T`` shapes and unparseable files, and never self-blocks
the gate item or the trailing Done-transition item (both at/after the boundary).
"""

from __future__ import annotations

from pathlib import Path

import superclaude.cli.reflect.runner as runner_mod
from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.runner import preflight

_BASE = "1111111111111111111111111111111111111111"

_FM = (
    "---\n"
    'id: "TASK-PF-0001"\n'
    'status: "🟠 Doing"\n'
    f'start_commit: "{_BASE}"\n'
    'spec_path: ""\n'
    'reflect_post: ""\n'
    "---\n\n"
)

_GATE_ITEM = (
    "### T01.09 -- Post-Execution Reflection: superclaude reflect run\n"
    "- [ ] Run the Gate Command `superclaude reflect run <tasklist>`\n"
    "- [ ] Transition frontmatter status to Done\n"
)


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "TASK-PF-0001.md"
    p.write_text(_FM + body, encoding="utf-8")
    return p


def _config(tasklist: Path):
    return resolve_config(str(tasklist), depth="standard", model="test-model")


def test_preflight_blocks_on_unchecked_item_before_gate(
    tmp_path, patch_git, monkeypatch
) -> None:
    """A ``- [ ]`` item BEFORE the reflect-gate boundary -> 'phase-incomplete'.

    RED pre-fix: ``preflight`` has no phase-completeness check yet, so it returns
    ``None``, not ``"phase-incomplete"`` (RED-by-absence)."""
    monkeypatch.setattr(runner_mod.shutil, "which", lambda name: "/usr/bin/claude")
    body = "### Phase 1\n- [x] Step 1 done\n- [ ] Step 2 NOT done\n\n" + _GATE_ITEM
    config = _config(_write(tmp_path, body))
    assert preflight(config) == "phase-incomplete"


def test_preflight_fail_open_when_only_gate_and_done_unchecked(
    tmp_path, patch_git, monkeypatch
) -> None:
    """Self-block regression guard (the #1 trap, REPORT risk): all pre-gate items
    checked; only the gate item + Done-transition item (both at/after the boundary)
    unchecked -> None (NO self-block). PASSES pre-fix (no phase check) AND post-fix
    (boundary token positionally excludes the gate + Done items)."""
    monkeypatch.setattr(runner_mod.shutil, "which", lambda name: "/usr/bin/claude")
    body = "### Phase 1\n- [x] Step 1 done\n- [x] Step 2 done\n\n" + _GATE_ITEM
    config = _config(_write(tmp_path, body))
    assert preflight(config) is None


def test_preflight_fail_open_when_no_boundary_token(
    tmp_path, patch_git, monkeypatch
) -> None:
    """Fail-open regression guard (R-002 D-I1 item 3): a sprint-shape ``### T`` file
    with an unchecked ``- [ ]`` item but NO ``superclaude reflect run`` /
    ``SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`` boundary token -> None (no in-file
    completion signal to judge). PASSES pre-fix AND post-fix."""
    monkeypatch.setattr(runner_mod.shutil, "which", lambda name: "/usr/bin/claude")
    body = "### T01.01 -- Some task\n- [ ] not done\n"
    config = _config(_write(tmp_path, body))
    assert preflight(config) is None
