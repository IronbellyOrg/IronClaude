"""H0 (Applicability Gate + Boundary Scan) content-assertion tests.

Asserts the documented FR-1 / §5.6 H0 markers in the source-of-truth ref
src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md.
Content gate over the markdown Claude Code consumes at runtime (see tests/skills/).
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS = (
    REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
)
CLOSURE = (REFS / "pipeline-hardening-closure.md").read_text(encoding="utf-8")


def test_h0_applicability_skip_requires_boundary_scan() -> None:
    """FR-1 AC2: an applicable=false skip requires a recorded one-sentence reason
    AND the boundary scan — a bare reason is insufficient."""
    low = CLOSURE.lower()
    # the skip sets applicable=false ...
    assert (
        "pipeline_hardening_applicable = false" in low
        or "pipeline_hardening_applicable=false" in low
    ), "H0 skip flag (applicable=false) not documented"
    # ... and requires BOTH a one-sentence reason AND the boundary scan
    assert "one-sentence reason" in low, "skip must record a one-sentence reason"
    assert "boundary scan" in low, "skip must record the boundary scan"
    # a bare reason is insufficient: bare "looks local" is invalid
    assert "looks local" in low and "invalid" in low, (
        'a bare "looks local" reason must be documented as invalid'
    )


def test_h0_boundary_scan_schema_rejects_bare_local_reason() -> None:
    """FR-1 AC1 + §5.6 H0 schema: the 6-field Boundary Scan Row schema is enumerated
    AND a bare "looks local" rationale is INVALID."""
    for field in (
        "boundary_type",
        "producer",
        "transformers",
        "consumer",
        "evidence_source",
        "risk",
        "decision",
        "rationale",
    ):
        assert field in CLOSURE, f"H0 boundary-scan field missing: {field}"
    # representative values of the 9-value boundary_type enum
    assert "CLI/subprocess" in CLOSURE
    assert "generated-artifact-parser" in CLOSURE
    # bare "looks local" rationale is INVALID
    low = CLOSURE.lower()
    assert "looks local" in low and "invalid" in low
