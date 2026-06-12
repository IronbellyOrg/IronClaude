"""H1 (Runtime-Entrypoint Verification) content-assertion test.

Asserts the documented FR-3 / FR-4 / §5.6 H1 markers in the source-of-truth ref
src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
H1 = (REFS / "runtime-entrypoint-verification.md").read_text(encoding="utf-8")


def test_h1_runtime_card_requires_negative_and_positive_witness() -> None:
    """FR-3 + FR-4 + §5.6 H1 schema: the H1 card (10 §5.6 rows / 12 atomic field tokens)
    enumerates BOTH negative_witness_command/_result AND positive_witness_command/_result; a green H1 is
    REJECTED without a fix-reverted->FAIL negative witness (a never-failing test does not
    satisfy H1); and proof stopping at helper/mock construction FAILs."""
    # H1 Runtime-Entrypoint Card schema (§5.6) — 10 table rows, 12 atomic field tokens
    for field in (
        "producer",
        "transformers",
        "consumer_or_evaluator",
        "boundary_crossed",
        "replay_command",
        "production_boundary_reach_proof",
        "forbidden_interpretation",
        "negative_witness_command",
        "negative_witness_result",
        "positive_witness_command",
        "positive_witness_result",
        "accepted_substitute_rationale",
    ):
        assert field in H1, f"H1 card field missing: {field}"

    low = H1.lower()
    # FR-4: green H1 rejected without a fix-reverted->FAIL negative witness
    assert "negative witness" in low
    assert "fix reverted" in low, "FR-4 fix-reverted negative witness not documented"
    # FR-4 AC2: a never-failing test does NOT satisfy H1
    assert "never been observed to fail" in low
    assert "satisfy h1" in low
    # FR-3: proof stopping at helper/mock construction FAILs
    assert "helper construction" in low
