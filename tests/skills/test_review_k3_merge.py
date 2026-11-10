"""Pins for three independent first reviews and the MERGE rule (#346, A/B design 1).

Enforcement type: STATIC - assertions over the text of the rules file.
"""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
RULES = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"


def _flat() -> str:
    return " ".join(RULES.read_text(encoding="utf-8").split())


def test_first_review_runs_three_times_then_merges():
    assert "| First review of a document | FIRST-REVIEW prompt, three times, then the MERGE rule |" in _flat()


def test_three_first_reviews_are_independent():
    assert (
        "brief three reviewers with the first-review brief, each in a fresh context that sees no other "
        "review and no transcript, each writing its own report" in _flat()
    )


def test_merge_rule_never_drops_and_feeds_verify():
    for literal in (
        "**MERGE rule**, applied by the coordinator, not by a reviewer",
        "the same path:line or the same quoted words",
        "`M1`, `M2`",
        "Never drop a finding in the merge",
        "The merged findings go to the VERIFY prompt",
        "a merged finding is confirmed when any of its sub-entries holds",
        "the header `review: 1 of 3`",
        "The merged report is the prior report of review 2.",
    ):
        assert literal in _flat(), literal


def test_merge_rule_lies_inside_the_first_review_prompt():
    f = _flat()
    order = ["### FIRST-REVIEW prompt", "**Three first reviews**", "**MERGE rule**", "- First-review brief:", "### RE-REVIEW prompt"]
    assert [f.index(x) for x in order] == sorted(f.index(x) for x in order)
