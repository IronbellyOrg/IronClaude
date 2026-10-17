"""Structural pin on the sc:reflect Tier 3 remediation route table.

``--remediate`` -> sc:workflow -> /sc:implement (default); ``--remediate --depth deep``
-> task-builder -> /task. Reads the SOURCE files (not the ``.claude/`` mirror).
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


def test_route_table_pins_both_routes_and_headless_follows_depth():
    assert "Route selection" in _REF
    plan = _row("| `--remediate` (depth")
    assert "sc:workflow-protocol" in plan and "/sc:implement" in plan
    mdtm = _row("| `--remediate --depth deep`")
    assert "task-builder" in mdtm and "/task" in mdtm
    # Headless follows the same depth rule (no exception): plan by default, MDTM on deep.
    headless = [ln for ln in _REF.splitlines() if ln.startswith("| headless")]
    assert len(headless) == 2
    plan_h = next(ln for ln in headless if "--depth deep" not in ln)
    deep_h = next(ln for ln in headless if "--depth deep" in ln)
    assert "remediation_plan_path" in plan_h and "/sc:implement" in plan_h
    assert "remediation_task_path" in deep_h and "/task" in deep_h
    assert "regardless of depth" not in _REF


def test_state_section_and_build_request_schema_present():
    assert "Reflect Verdict State" in _REF
    assert "BUILD_REQUEST:" in _REF  # M1 schema preserved for the deep route


def test_handoff_implement_only_appears_as_a_prohibition():
    assert "--handoff none" in _REF
    for text in (_REF, _SKILL, _CMD):
        for ln in text.splitlines():
            if "--handoff implement" in ln:
                assert _PROHIBITION.search(ln), ln


def test_legacy_grammar_still_documented():
    assert "--type task --analyze" in _CMD and "--type task --validate" in _CMD
