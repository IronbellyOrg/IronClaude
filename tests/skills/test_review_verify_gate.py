"""Pins for the verify-before-fix gate of the review-loop rules file (#346, A/B design 2).

Enforcement type: STATIC - assertions over the text of the rules file.
"""

from __future__ import annotations

import re
from pathlib import Path

from tests.skills.test_review_prompt_overrides import lint_brief

_REPO = Path(__file__).resolve().parents[2]
RULES = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"


def _text() -> str:
    return RULES.read_text(encoding="utf-8")


def _flat() -> str:
    return " ".join(_text().split())


def _verify_brief() -> str:
    m = re.search(r'- Verify brief: "([^"]+)"', _text())
    assert m, "no quoted Verify brief"
    return m.group(1)


def test_verify_prompt_sits_between_re_review_and_revise():
    t = _text()
    assert t.index("### RE-REVIEW prompt") < t.index("### VERIFY prompt") < t.index("### REVISE prompt")


def test_routing_table_sends_every_failing_report_to_verify_first():
    t = _text()
    assert "| After a review report with open blocking findings, before any revision | VERIFY prompt |" in t
    assert "| After the VERIFY prompt confirmed at least one blocking finding, to revise | REVISE prompt |" in t
    assert "| After a review report with open blocking findings, to revise |" not in t


def test_verifier_sees_only_the_candidate_and_the_finding_list():
    brief = _verify_brief()
    for literal in (
        "{{CANDIDATE}}",
        "{{FINDINGS}}",
        "You see only the candidate and this finding list, not the review report or the reviewer's reasoning",
        "`grep -nF`",
        "check both",
        "Confirm a finding only if both hold",
        "Add no finding, regrade nothing and edit nothing",
        "`confirmed: <ids>`",
        "`confirmed: none`",
    ):
        assert literal in brief, literal
    assert "give it only the candidate and the finding list, pasted into the brief" in _flat()


def test_rejected_findings_are_kept_and_the_gate_fails_closed():
    for literal in (
        "A rejected finding is never deleted and never revised",
        "`noted, unactioned`",
        "treats a rejected id as a note, not a prior blocking finding",
        "A reply that is missing or has no `confirmed:` line confirms every finding",
        "If none is confirmed, revise nothing",
    ):
        assert literal in _flat(), literal


def test_ids_and_findings_values():
    flat = _flat()
    assert "`{{IDS}}`: the blocking finding ids the verifier confirmed, and only those." in flat
    assert "`{{FINDINGS}}`:" in flat
    assert "listed in the report's `Reviser brief`, and only those" not in flat


def test_review_three_still_verifies_then_escalates():
    assert (
        "At `review: 3` with an open blocking finding the VERIFY prompt still runs, then the loop escalates "
        "to the user with the confirmed findings; no REVISE prompt and no fourth review." in _flat()
    )


def test_verify_brief_passes_the_brief_lint():
    assert lint_brief(_verify_brief()) == []
