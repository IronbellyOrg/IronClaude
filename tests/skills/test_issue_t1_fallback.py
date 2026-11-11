"""Static tests for the /sc:issue T1 -> T2 fallback (users who cannot see tier 1).

A failed ``issue-worker-t1`` spawn (``claude-gw-tier1b`` not served) is retried once
with ``issue-worker-t2``. T2 and T3 have no fallback and there is no alias fallback.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "src/superclaude/skills/sc-issue-protocol"
FALLBACK_LINE = "Handled by issue-worker-t2 (tier 2): tier1b is not available to this user."

DOCS = ["SKILL.md", "refs/tiers.md", "refs/claim.md", "refs/create.md"]


def _text(rel: str) -> str:
    return (SKILL / rel).read_text(encoding="utf-8")


@pytest.mark.parametrize("rel", DOCS)
def test_doc_states_the_t1_to_t2_fallback(rel):
    text = _text(rel)
    assert "issue-worker-t1" in text and "issue-worker-t2" in text
    assert "T1 -> T2 fallback" in text, f"{rel} lost the T1 -> T2 fallback wording"


@pytest.mark.parametrize("rel", ["SKILL.md", "refs/tiers.md", "refs/claim.md", "refs/create.md"])
def test_doc_names_the_stop_when_the_fallback_is_not_served(rel):
    assert "E-TIER-UNAVAILABLE" in _text(rel)


@pytest.mark.parametrize("rel", ["SKILL.md", "refs/tiers.md", "refs/create.md"])
def test_doc_keeps_no_alias_fallback(rel):
    assert "no alias fallback" in _text(rel)


def test_fallback_line_is_defined_in_skill_and_tiers():
    for rel in ("SKILL.md", "refs/tiers.md"):
        assert FALLBACK_LINE in _text(rel)


def test_tiers_says_no_fallback_for_t3_or_t2():
    assert "no fallback for T3 or T2" in _text("refs/tiers.md")


def test_accuracy_check_template_has_the_optional_fallback_line():
    text = _text("templates/accuracy-check-comment.md")
    assert FALLBACK_LINE in text and "Optional" in text


def test_next_steps_line_offers_tier2_when_tier1b_is_missing():
    first = _text("templates/next-steps.md").splitlines()[0]
    assert first == (
        "/model <claude-gw-tier2 for simple work | claude-gw-tier1b for medium and complex "
        "work; use claude-gw-tier2 when tier1b is not in your /model list>"
    )


def test_no_tier1a_left_in_the_issue_workers_or_skill():
    paths = [ROOT / "src/superclaude/agents/issue-worker-t1.md", *SKILL.rglob("*")]
    for p in paths:
        if p.is_file() and p.suffix in {".md", ".py", ".json"}:
            assert "claude-gw-tier1a" not in p.read_text(encoding="utf-8"), p
