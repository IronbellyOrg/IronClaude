"""Structural pin on the sc:reflect Tier 3 remediation route table.

There is one route: ``--remediate`` -> sc:workflow -> /sc:implement, at every depth.
The MDTM route (task-builder -> /task for ``--depth deep``) was removed in 6.1.0.
Reads the SOURCE files (not the ``.claude/`` mirror).
"""

from __future__ import annotations

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3] / "src/superclaude"
_REF = (_ROOT / "skills/sc-reflect-protocol/refs/remediation-handoff.md").read_text()
_SKILL = (_ROOT / "skills/sc-reflect-protocol/SKILL.md").read_text()
_CMD = (_ROOT / "commands/reflect.md").read_text()

_PROHIBITION = re.compile(r"\b(never|not|forbid\w*)\b", re.IGNORECASE)


def _row(prefix: str) -> str:
    return next(ln for ln in _REF.splitlines() if ln.startswith(prefix))


def test_route_table_pins_the_single_plan_route():
    assert "Route selection" in _REF
    plan = _row("| `--remediate` (any depth)")
    assert "sc:workflow-protocol" in plan and "/sc:implement" in plan
    headless = [ln for ln in _REF.splitlines() if ln.startswith("| headless")]
    assert len(headless) == 1
    assert "remediation_plan_path" in headless[0] and "/sc:implement" in headless[0]
    assert "--depth deep" not in headless[0]
    assert "regardless of depth" not in _REF


def test_no_task_file_route_is_left_in_the_reflect_files():
    for name, text in (("ref", _REF), ("skill", _SKILL), ("command", _CMD)):
        assert "task-builder" not in text, name
        assert "BUILD_REQUEST:" not in text, name
        assert not re.search(r"(?<![\w:/])/task\b(?!s)", text), name
    assert "MDTM route" not in _CMD
    assert "**MDTM route**" not in _REF


def test_state_section_present():
    assert "Reflect Verdict State" in _REF


def test_handoff_implement_only_appears_as_a_prohibition():
    assert "--handoff none" in _REF
    for text in (_REF, _SKILL, _CMD):
        for ln in text.splitlines():
            if "--handoff implement" in ln:
                assert _PROHIBITION.search(ln), ln


def test_legacy_grammar_still_documented():
    assert "--type task --analyze" in _CMD and "--type task --validate" in _CMD
