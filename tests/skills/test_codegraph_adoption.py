"""Drift guards for codegraph adoption in skills and commands (issue #323, Phase 3).

Pins the codegraph tier placed above each Phase 1 Grep/Read floor in validate-roadmap,
brainstorm, task, tasklist, cleanup-audit and auggie-review, the `mcp-servers:`
metadata those primitives gained, the run state handed to the auggie-review deep-pass
agent, and that no Serena tool name came back. CI-safe: pure file-content assertions.
"""

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_SRC = _REPO / "src" / "superclaude"
_PLUGIN = _REPO / "plugins" / "superclaude"

_VR_SKILL = _SRC / "skills" / "sc-validate-roadmap-protocol" / "SKILL.md"
_VR_CMD = _SRC / "commands" / "validate-roadmap.md"
_BS_SKILL = _SRC / "skills" / "sc-brainstorm-protocol" / "SKILL.md"
_BS_ROUTING = _SRC / "skills" / "sc-brainstorm-protocol" / "refs" / "handoff-routing.md"
_BS_CMD = _SRC / "commands" / "brainstorm.md"
_BS_PLUGIN_CMD = _PLUGIN / "commands" / "brainstorm.md"
_TASK_SKILL = _SRC / "skills" / "sc-task-protocol" / "SKILL.md"
_TASK_CMD = _SRC / "commands" / "task.md"
_TASK_PLUGIN_CMD = _PLUGIN / "commands" / "task.md"
_TASKLIST_SKILL = _SRC / "skills" / "sc-tasklist-protocol" / "SKILL.md"
_CA_SKILL = _SRC / "skills" / "sc-cleanup-audit-protocol" / "SKILL.md"
_CA_CMD = _SRC / "commands" / "cleanup-audit.md"
_AR_SKILL = _SRC / "skills" / "sc-auggie-review-protocol" / "SKILL.md"
_AR_CMD = _SRC / "commands" / "auggie-review.md"

_ALL = [
    _VR_SKILL, _VR_CMD, _BS_SKILL, _BS_ROUTING, _BS_CMD, _BS_PLUGIN_CMD, _TASK_SKILL,
    _TASK_CMD, _TASK_PLUGIN_CMD, _TASKLIST_SKILL, _CA_SKILL, _CA_CMD, _AR_SKILL, _AR_CMD,
]
_STATE_FIELDS = ("index_state", "checked_at", "worktree_root", "projectPath")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, start: str, end_pattern: str) -> str:
    after = text.split(start, 1)
    assert len(after) == 2, f"missing anchor {start!r}"
    return re.split(end_pattern, after[1], maxsplit=1, flags=re.M)[0]


def _rel(path: Path) -> str:
    return str(path.relative_to(_REPO))


def test_validate_roadmap_step05_puts_codegraph_above_grep_and_never_skips():
    step = _section(_text(_VR_SKILL), "#### Step 0.5", r"^#### |^### ")
    assert "codegraph_search" in step and "Grep" in step
    assert step.index("codegraph_search") < step.index("call `Grep` for its definition")
    assert "skip" not in step.lower(), "Step 0.5 must never skip where the Grep floor exists"


def test_brainstorm_tier2_names_codegraph_files_and_search():
    tier2 = _section(_text(_BS_ROUTING), "**Tier 2 (fallback_1)**: codegraph", r"^\*\*Final fallback")
    assert "codegraph_files" in tier2 and "codegraph_search" in tier2
    assert "Glob for files matching topic keywords" in tier2, "native Glob/Grep floor must stay"


def test_task_protocol_standard_step2_names_codegraph_callers():
    standard = _section(_text(_TASK_SKILL), "**STANDARD Execution**:", r"^\*\*LIGHT Execution")
    step2 = next(ln for ln in standard.splitlines() if ln.startswith("2. "))
    assert "codegraph_callers" in step2 and "Grep" in step2


def test_tasklist_strict_row():
    assert "| STRICT | None | codegraph, Context7 | Yes (recorded) |" in _text(_TASKLIST_SKILL).splitlines()


@pytest.mark.parametrize("path", [_CA_SKILL, _AR_SKILL, _AR_CMD], ids=_rel)
def test_cleanup_audit_and_auggie_review_name_codegraph(path):
    assert "codegraph" in _text(path)


def test_auggie_review_deep_pass_brief_passes_run_state():
    step5 = next(ln for ln in _text(_AR_SKILL).splitlines() if "spawn the `auggie-reviewer` agent" in ln)
    for field in _STATE_FIELDS:
        assert field in step5, f"deep-pass brief does not pass {field}"


@pytest.mark.parametrize(
    "path", [_VR_CMD, _VR_SKILL, _BS_CMD, _BS_PLUGIN_CMD, _BS_SKILL, _CA_CMD, _CA_SKILL, _AR_CMD, _AR_SKILL],
    ids=_rel,
)
def test_mcp_servers_gain_codegraph(path):
    line = next(ln for ln in _text(path).splitlines() if ln.startswith("mcp-servers:"))
    assert "codegraph" in line, f"{_rel(path)} mcp-servers lacks codegraph"


@pytest.mark.parametrize("path", [_TASK_CMD, _TASK_PLUGIN_CMD], ids=_rel)
def test_task_command_mcp_servers_unchanged(path):
    line = next(ln for ln in _text(path).splitlines() if ln.startswith("mcp-servers:"))
    assert "serena" not in line and "codegraph" not in line


@pytest.mark.parametrize("path", _ALL, ids=_rel)
def test_no_serena_tool_names(path):
    assert "mcp__serena" not in _text(path)
