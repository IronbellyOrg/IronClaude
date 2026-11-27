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


_ROW_PREFIX = "| `sc:workflow-protocol` (skill, not agent)"


def _region(text: str, start: str, end: str) -> str:
    assert text.count(start) == 1, f"anchor {start!r} must occur exactly once"
    assert text.count(end) == 1, f"anchor {end!r} must occur exactly once"
    first, last = text.index(start), text.index(end)
    assert first < last, f"anchor {start!r} must come before {end!r}"
    return text[first:last]


def _depth_tokens(text: str) -> list[str]:
    return re.findall(r"--depth\s+([^\s`]+)", text)


def _delegation_row() -> str:
    rows = [ln for ln in _SKILL.splitlines() if ln.startswith(_ROW_PREFIX)]
    assert len(rows) == 1, f"expected one delegation row, found {len(rows)}"
    return rows[0]


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


# Not covered: prose outside the three Phase A sites and outside `sc:workflow` lines.
def test_phase_a_depth_ref_region():
    region = _region(_REF, "### Phase A", "### Phase B")
    tokens = _depth_tokens(region)
    assert tokens, "ref Phase A region: no --depth token (a deleted flag cannot pass)"
    assert all(t == "standard" for t in tokens), f"ref Phase A region: {tokens}"
    assert "--depth standard --handoff none" in region, "ref Phase A region: call text"
    assert "--strategy" not in region, "ref Phase A region: --strategy must be absent"


def test_phase_a_depth_skill_region():
    region = _region(_SKILL, "- **Phase A", "- **Phase B")
    tokens = _depth_tokens(region)
    assert tokens, (
        "SKILL.md Phase A bullet: no --depth token (a deleted flag cannot pass)"
    )
    assert all(t == "standard" for t in tokens), f"SKILL.md Phase A bullet: {tokens}"
    assert "--strategy" not in region, "SKILL.md Phase A bullet: --strategy present"


def test_phase_a_depth_delegation_row():
    row = _delegation_row()
    tokens = _depth_tokens(row)
    assert tokens, (
        "SKILL.md delegation row: no --depth token (a deleted flag cannot pass)"
    )
    assert all(t == "standard" for t in tokens), f"SKILL.md delegation row: {tokens}"
    assert "--strategy" not in row, "SKILL.md delegation row: --strategy present"


def test_no_placeholder_depth_on_sc_workflow_lines():
    for name, text in (("ref", _REF), ("skill", _SKILL), ("command", _CMD)):
        for ln in text.splitlines():
            if "sc:workflow" not in ln:
                continue
            for token in _depth_tokens(ln):
                assert not token.startswith(("<", "{", "$")), f"{name}: {ln}"


def test_review_only_decision_stays_written_down():
    for name, text in (("ref", _REF), ("skill", _SKILL), ("command", _CMD)):
        for banned in ("plan_depth", "Plan depth", "--plan-depth"):
            assert banned not in text, f"{name}: {banned} must not appear"
    sentence = "`--depth deep` only sets the review depth"
    assert sentence in _SKILL, "SKILL.md: the review-only sentence is missing"
    assert sentence in _CMD, "reflect.md: the review-only sentence is missing"
    row = _delegation_row()
    last_cell = row.rstrip().rstrip("|").rsplit("|", 1)[-1].strip()
    expected = "None; surface the report path and recommend manual planning"
    assert last_cell == expected, f"SKILL.md delegation row last cell: {last_cell!r}"
    assert "--depth deep" not in row, "SKILL.md delegation row: --depth deep present"
