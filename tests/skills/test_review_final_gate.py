"""Pins for the final whole-document gate of the review loop (#346, A/B design 3).

Enforcement type: STATIC - assertions over the rules file and both spec-panel copies.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.skills.test_review_prompt_overrides import lint_brief

_REPO = Path(__file__).resolve().parents[2]
RULES = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
LABEL = "This is a first review of a complete document; no prior rounds exist. "


def _text() -> str:
    return RULES.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _brief(label: str) -> str:
    m = re.search(rf'- {label}: "([^"]+)"', _text())
    assert m, label
    return m.group(1)


def test_gate_prompt_follows_revise_and_precedes_never():
    t = _text()
    assert t.index("### REVISE prompt") < t.index("### GATE prompt") < t.index("## Never")


def test_gate_brief_is_the_first_review_brief_with_the_label():
    assert _brief("Gate brief") == LABEL + _brief("First-review brief")


def test_gate_brief_passes_the_brief_lint():
    assert lint_brief(_brief("Gate brief")) == []


def test_routing_rows_and_own_numbering():
    t = _text()
    assert (
        "| After the loop's PASS (a scoped PASS, or a first review that passed) "
        "| GATE prompt, once |" in t
    )
    assert (
        "| After a gate review with open blocking findings | REVISE prompt, then one "
        "RE-REVIEW prompt: the gate loop |" in t
    )
    assert "so no report is ever a fourth review" in _flat(t)


def test_gate_loop_is_bounded_with_a_stall_rule_and_a_ceiling():
    flat = _flat(_text())
    for literal in (
        "fresh context that has seen no report of this loop",
        "starts one gate loop: one REVISE prompt with the gate's blocking ids, then one "
        "RE-REVIEW prompt with the gate report as PRIOR",
        "with no second gate loop and no further review",
        "**Stall rule**: if every blocking finding of the gate review repeats a blocking "
        "finding of an earlier review in this loop",
        "escalate to the user with them and start no gate loop",
        "at most 5 reviews and 3 fix cycles in all",
    ):
        assert literal in flat, literal


@pytest.mark.parametrize("rel", SPEC_PANELS)
def test_spec_panel_bullet_five_names_the_gate_and_the_ceiling(rel):
    lines = (_REPO / rel).read_text(encoding="utf-8").splitlines()
    start = lines.index("## Review Loop") + 1
    bullet = _flat(next(line for line in lines[start:] if line.startswith("5. **")))
    for literal in (
        "whole-document assurance needs a separate, labelled first review, the gate review,",
        "never start a fourth review",
        "they start at most one gate loop of one fix cycle and one re-review",
        "a FAIL or a stall there escalates to the user",
        "a document gets at most 5 reviews and 3 fix cycles in all",
    ):
        assert literal in bullet, (rel, literal)
    assert "whose blockers are escalated" not in bullet
    cap = _flat(next(line for line in lines[start:] if line.startswith("4. **")))
    assert (
        "at most 2 fix cycles (3 reviews), then escalate to the user with the open "
        "blocking findings" in cap
    )


def test_spec_panel_stays_within_500_lines():
    for rel in SPEC_PANELS:
        assert len((_REPO / rel).read_text(encoding="utf-8").splitlines()) <= 500
