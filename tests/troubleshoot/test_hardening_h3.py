"""H3 (Unmask-and-Sweep classifier) content-assertion tests.

Asserts the documented FR-7 / FR-8 / FR-9 / §5.7 grammar / §5.6 H3 markers in the
source-of-truth ref src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
H3 = (REFS / "unmask-and-sweep.md").read_text(encoding="utf-8")


def test_h3_word_boundary_rejects_incomplete_representation() -> None:
    """FR-8 AC1+AC2: the word-boundary rule and the mandatory near-miss negative fixtures
    (incomplete vs complete, representation vs present)."""
    low = H3.lower()
    assert "word-boundary" in low, "FR-8 word-boundary rule not documented"
    # mandatory near-miss negatives
    assert "must not match `complete`" in low, "incomplete-vs-complete near-miss missing"
    assert "must not match `present`" in low, "representation-vs-present near-miss missing"


def test_h3_small_grammar_rejects_setext_and_decorated_verdicts() -> None:
    """§5.7 grammar: the small formal allow-list grammar is reproduced (NOT CommonMark,
    NOT substring) and setext-like headings + decorated/bolded verdict lines are fixtures
    NOT accepted control syntax."""
    low = H3.lower()
    assert "small formal allow-list grammar" in low
    assert "commonmark" in low, "grammar must state it is NOT a full CommonMark parser"
    assert "substring" in low, "grammar must state substring is never behavior-controlling"
    assert "setext" in low
    assert "decorated" in low
    assert "fixtures" in low


def test_h3_sweep_card_requires_k_true_k_swept_and_mixed_fixture() -> None:
    """FR-9 + §5.6 H3 schema: the Unmask/Sweep/Classifier Card enumerates K_true, K_swept,
    coverage_proof, and the full_artifact_mixed_fixture/sibling_negative_fixture/
    positive_fixture fields."""
    for field in (
        "anchor_failure",
        "sibling_family_discovery_method",
        "K_true",
        "K_swept",
        "coverage_proof",
        "positive_fixture",
        "sibling_negative_fixture",
        "full_artifact_mixed_fixture",
        "severity_assertions_by_consumer",
        "heuristic_cost_rationale",
    ):
        assert field in H3, f"H3 card field missing: {field}"
