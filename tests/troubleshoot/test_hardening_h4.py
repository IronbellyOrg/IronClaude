"""H4 (Effective-Input Proof) content-assertion tests.

Asserts the documented FR-10 / §5.6 H4 markers in the source-of-truth ref
src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
H4 = (REFS / "effective-input-proof.md").read_text(encoding="utf-8")


def test_h4_nonempty_wrong_surface_fails_closed() -> None:
    """FR-10 AC1 / F-D1 (the real E5 mechanism): H4 fails closed when effective input is
    non-empty but the WRONG surface — E>0 is NOT sufficient; surface-correctness of
    |E ∩ true_runtime_surface| must be proven."""
    low = H4.lower()
    assert "fails closed" in low
    assert "wrong surface" in low, "non-empty wrong-surface fail-closed not documented"
    assert "e > 0" in low and "sufficient" in low, "E>0-is-not-sufficient rule not documented"
    assert "true_runtime_surface" in H4
    assert "intersection" in low


def test_h4_manifest_schema_requires_intersection_proof() -> None:
    """§5.6 H4 manifest schema: the manifest enumerates intersection_proof and the
    dirty/staged/unstaged-inclusion + foreign-commit-exclusion fields."""
    for field in (
        "selector_command",
        "base_ref",
        "head_ref",
        "dirty_files",
        "staged_files",
        "unstaged_files",
        "included_files",
        "excluded_foreign_commits",
        "runtime_surface_claim",
        "intersection_proof",
        "validation_command",
    ):
        assert field in H4, f"H4 manifest field missing: {field}"
