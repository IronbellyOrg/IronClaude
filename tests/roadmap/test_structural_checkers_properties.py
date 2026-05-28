"""Property-based tests for structural_checkers canonicalization.

Locks the family-agnostic invariant of the spec-fidelity-canonicalizer fix:
when a roadmap ID's canonical form matches a spec ID's canonical form,
zero HIGH `phantom_id` findings are emitted. Surface-form drift may emit
MEDIUM `id_schema_drift` findings, but the convergence-blocking HIGH tier
must remain empty.

Precedent: tests/sprint/test_property_based.py (hypothesis posture).
"""

from __future__ import annotations

from pathlib import Path

import pytest

# Skip the entire module if hypothesis is unavailable (per task spec).
pytest.importorskip("hypothesis")

from hypothesis import given  # noqa: E402
from hypothesis import strategies as st

from superclaude.cli.roadmap.structural_checkers import check_signatures  # noqa: E402

# ---------------------------------------------------------------------------
# Strategies — surface-form variants across all 5 requirement families.
# ---------------------------------------------------------------------------


@st.composite
def id_form_pairs(draw):
    """Yield (family, canonical_id, surface_variants) tuples.

    canonical_id is the spec-form ID (e.g. "D5", "FR-7", "NFR-2"). Each
    surface_variant in the returned list canonicalizes to canonical_id under
    `_canonicalize_requirement_id`. Covers all 5 families: FR, NFR, SC, G, D.
    """
    family = draw(st.sampled_from(["FR", "NFR", "SC", "G", "D"]))
    num = draw(st.integers(min_value=1, max_value=99))
    # canonical form: single-letter family -> no separator; multi-letter -> hyphen
    if len(family) == 1:
        canonical = f"{family}{num}"
        # surface variants: zero-padded, with/without separator
        variants = [
            canonical,
            f"{family}0{num}" if num < 10 else f"{family}{num}",
            f"{family}-{num}",
            f"{family}-0{num}" if num < 10 else f"{family}-{num}",
        ]
    else:
        canonical = f"{family}-{num}"
        variants = [
            canonical,
            f"{family}-0{num}" if num < 10 else f"{family}-{num}",
        ]
    return family, canonical, variants


# ---------------------------------------------------------------------------
# Property under test
# ---------------------------------------------------------------------------


@given(id_form_pairs())
def test_canonicalization_property_holds_across_families(
    tmp_path_factory: pytest.TempPathFactory,
    pair: tuple[str, str, list[str]],
) -> None:
    """For every (family, canonical, surface_variants) tuple: a spec containing
    only the canonical form + a roadmap referencing every surface variant must
    yield zero HIGH `phantom_id` findings. Drift findings are acceptable.
    """
    family, canonical, variants = pair
    tmp_path: Path = tmp_path_factory.mktemp("prop")
    spec = tmp_path / "spec.md"
    roadmap = tmp_path / "roadmap.md"
    spec.write_text(
        f"---\ntitle: Spec\n---\n\n# Spec\n\n## Requirements\n\nSee {canonical}.\n",
        encoding="utf-8",
    )
    roadmap.write_text(
        "---\ntitle: Roadmap\n---\n\n# Roadmap\n\n## Refs\n\n"
        + ", ".join(variants)
        + "\n",
        encoding="utf-8",
    )

    findings = check_signatures(str(spec), str(roadmap))
    high_phantoms = [
        f for f in findings if f.rule_id == "phantom_id" and f.severity == "HIGH"
    ]
    assert len(high_phantoms) == 0, (
        f"Family={family!r} canonical={canonical!r} variants={variants!r}: "
        f"expected 0 HIGH phantom_id; got "
        f"{[(f.roadmap_quote, f.spec_quote) for f in high_phantoms]}"
    )
