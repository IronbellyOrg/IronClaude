"""Unit tests for the cosmetic-failure auto-remediation lane.

Covers the classifier (cosmetic vs semantic) and the deterministic transforms
(C1-C10) defined in superclaude.cli.roadmap.cosmetic_remediator. Every test
is hermetic -- markdown is built inline, no fixture files required.
"""

from __future__ import annotations

from superclaude.cli.roadmap.cosmetic_remediator import (
    Classification,
    _compute_fenced_indices,
    _is_in_fenced_block,
    apply_cosmetic_remediations,
    classify_gate_failure,
)

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def _content_with_milestone(
    subsections: list[str],
    *,
    mid: str = "1",
    frontmatter: str = "---\nspec_source: epics.md\n---\n",
    extras: str = "",
) -> str:
    """Assemble a minimal roadmap-ish markdown with one milestone."""
    h2 = f"## M{mid}: Foundation\n\nObjective: x | Duration: y | Exit: z\n\n"
    subs = "\n\n".join(subsections) + "\n"
    return (
        frontmatter
        + "\n# Test Roadmap\n\n## Executive Summary\nfoo\n\n"
        + h2
        + subs
        + extras
    )


_GATE = "template_sections_present"


# --------------------------------------------------------------------------
# Classifier basics
# --------------------------------------------------------------------------


class TestClassifierBasics:
    def test_non_roadmap_gate_classifies_as_non_cosmetic(self):
        cl = classify_gate_failure(
            "# anything\n",
            gate_name="sprint_some_gate",
            failure_reason="x",
            step_id="s1",
        )
        assert cl.is_pure_cosmetic is False
        assert any(
            "not in roadmap remediation surface" in s for s in cl.semantic_violations
        )

    def test_placeholder_sentinel_is_semantic(self):
        content = _content_with_milestone(
            [
                "### Integration Points",
                "### Milestone Dependencies",
                "### Risk Assessment",
                "{{SC_PLACEHOLDER:something}}",
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is False
        assert any("SC_PLACEHOLDER" in s for s in cl.semantic_violations)

    def test_oq_in_deliverable_id_is_semantic(self):
        # Build a content with an OQ-001 row in a deliverable table
        content = _content_with_milestone(
            [
                "| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |",
                "|---|---|---|---|---|---|---|---|---|",
                "| 1 | OQ-001 | bad | row | C | - | x | S | P0 |",
                "### Integration Points -- M1",
                "### Milestone Dependencies -- M1",
                "### Risk Assessment and Mitigation -- M1",
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is False
        assert any("OQ-xxx" in s for s in cl.semantic_violations)


# --------------------------------------------------------------------------
# C1-C4: milestone H3 defects (the actual TUIBBS failure shape)
# --------------------------------------------------------------------------


class TestMilestoneH3Defects:
    def test_c1_stem_alias_classified_and_fixed(self):
        # "Risk Assessment" instead of "Risk Assessment and Mitigation"
        content = _content_with_milestone(
            [
                "### Integration Points -- M1",
                "### Milestone Dependencies -- M1",
                "### Risk Assessment",  # alias, no suffix either
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        new, transforms = apply_cosmetic_remediations(content, cl)
        assert "### Risk Assessment and Mitigation -- M1" in new
        assert any("Risk Assessment and Mitigation" in t for t in transforms)

    def test_c2_missing_milestone_suffix_fixed(self):
        # All three required stems present, none with -- M{N} suffix
        content = _content_with_milestone(
            [
                "### Integration Points",
                "### Milestone Dependencies",
                "### Risk Assessment and Mitigation",
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        new, _ = apply_cosmetic_remediations(content, cl)
        assert "### Integration Points -- M1" in new
        assert "### Milestone Dependencies -- M1" in new
        assert "### Risk Assessment and Mitigation -- M1" in new

    def test_c3_u2014_literal_dash_variant_fixed(self):
        # The actual TUIBBS template-corruption pattern: literal "u2014"
        content = _content_with_milestone(
            [
                "### Integration Points u2014 M1",
                "### Milestone Dependencies u2014 M1",
                "### Risk Assessment and Mitigation u2014 M1",
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        assert any(v.klass == "C3" for v in cl.cosmetic_violations)
        new, _ = apply_cosmetic_remediations(content, cl)
        assert "u2014" not in new
        assert "### Integration Points -- M1" in new

    def test_c3_em_dash_normalized_to_double_hyphen(self):
        # Em-dash is gate-accepted but remediator normalizes to double-hyphen
        # for stable cross-encoding behavior.
        content = _content_with_milestone(
            [
                "### Integration Points — M1",
                "### Milestone Dependencies — M1",
                "### Risk Assessment and Mitigation — M1",
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        new, _ = apply_cosmetic_remediations(content, cl)
        assert "### Integration Points -- M1" in new

    def test_full_tuibbs_failure_shape_remediated(self):
        # The exact pattern Opus produced on the TUIBBS run: short stems, no suffix
        content = _content_with_milestone(
            [
                "### Integration Points",
                "### Milestone Dependencies",
                "### Open Questions",
                "### Risk Assessment",
            ]
        )
        cl = classify_gate_failure(
            content, _GATE, "tuibbs failure", step_id="generate-opus-architect"
        )
        assert cl.is_pure_cosmetic is True
        new, transforms = apply_cosmetic_remediations(content, cl)
        # Every required canonical heading should be in place
        assert "### Integration Points -- M1" in new
        assert "### Milestone Dependencies -- M1" in new
        assert "### Open Questions -- M1" in new
        assert "### Risk Assessment and Mitigation -- M1" in new
        assert len(transforms) >= 3  # at least the 3 gate-required H3s rewrote


# --------------------------------------------------------------------------
# C5-C10: whitespace / blanks / quotes / tables / frontmatter
# --------------------------------------------------------------------------


class TestNonH3Cosmetics:
    def test_c5_c6_trailing_whitespace_stripped(self):
        # Header + body lines with trailing whitespace
        content = _content_with_milestone(
            [
                "### Integration Points -- M1   ",  # header trailing ws (C5)
                "### Milestone Dependencies -- M1",
                "### Risk Assessment and Mitigation -- M1",
                "some body text   ",  # body trailing ws (C6)
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        new, _ = apply_cosmetic_remediations(content, cl)
        for line in new.splitlines():
            # No line ends with whitespace except inside fenced blocks (none here)
            assert line == line.rstrip(), f"trailing ws survived on: {line!r}"

    def test_c7_blank_line_collapse(self):
        content = (
            "---\nspec_source: x\n---\n"
            "# T\n\n## Executive Summary\nfoo\n\n\n\n\n"  # 4 blank lines
            "## M1: F\n\nbody\n\n"
            "### Integration Points -- M1\n"
            "### Milestone Dependencies -- M1\n"
            "### Risk Assessment and Mitigation -- M1\n"
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        new, _ = apply_cosmetic_remediations(content, cl)
        assert "\n\n\n" not in new

    def test_c8_smart_quotes_folded(self):
        content = _content_with_milestone(
            [
                "### Integration Points -- M1",
                "### Milestone Dependencies -- M1",
                "### Risk Assessment and Mitigation -- M1",
                "Some “curly” quotes and ‘single’ ones.",
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        new, _ = apply_cosmetic_remediations(content, cl)
        assert "“" not in new
        assert "”" not in new
        assert "‘" not in new
        assert "’" not in new
        assert '"curly"' in new
        assert "'single'" in new

    def test_c10_frontmatter_trailing_whitespace_stripped(self):
        # Frontmatter line has trailing whitespace
        content = (
            "---\nspec_source: epics.md   \nother: v\n---\n"
            "# T\n## Executive Summary\nfoo\n## M1: F\nb\n"
            "### Integration Points -- M1\n"
            "### Milestone Dependencies -- M1\n"
            "### Risk Assessment and Mitigation -- M1\n"
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        new, _ = apply_cosmetic_remediations(content, cl)
        # Frontmatter line no longer has trailing whitespace
        assert "spec_source: epics.md   " not in new
        assert "spec_source: epics.md" in new


# --------------------------------------------------------------------------
# Idempotency & invariants
# --------------------------------------------------------------------------


class TestIdempotency:
    def test_canonical_input_classifies_as_not_cosmetic(self):
        # A clean roadmap has nothing to fix -> is_pure_cosmetic = False
        # (False here means "nothing to do", not "must halt"; the executor
        # handles this branch by treating it as the gate having actually
        # failed for a real reason.)
        content = _content_with_milestone(
            [
                "### Integration Points -- M1",
                "### Milestone Dependencies -- M1",
                "### Risk Assessment and Mitigation -- M1",
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is False
        assert cl.cosmetic_violations == []
        assert cl.semantic_violations == []

    def test_remediation_is_idempotent(self):
        content = _content_with_milestone(
            [
                "### Integration Points",
                "### Milestone Dependencies",
                "### Risk Assessment",
            ]
        )
        cl1 = classify_gate_failure(content, _GATE, "x", step_id="s1")
        once, _ = apply_cosmetic_remediations(content, cl1)
        cl2 = classify_gate_failure(once, _GATE, "x", step_id="s1")
        twice, _ = apply_cosmetic_remediations(once, cl2)
        assert once == twice

    def test_c11_resource_subsection_alias_fixed(self):
        # The actual TUIBBS-secondary failure: long-form ``External Dependencies
        # (PRD-confirmed, TDD-pinned)`` and short ``Infrastructure`` under
        # ``## Resource Requirements and Dependencies`` should both normalize.
        content = (
            "---\nspec_source: epics.md\n---\n"
            "# Test\n\n## Executive Summary\nfoo\n\n"
            "## M1: F\n\nb\n\n"
            "### Integration Points -- M1\n"
            "### Milestone Dependencies -- M1\n"
            "### Risk Assessment and Mitigation -- M1\n\n"
            "## Resource Requirements and Dependencies\n\n"
            "### External dependencies (PRD-confirmed, TDD-pinned)\n\nfoo\n\n"
            "### Infrastructure\n\nbar\n"
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is True
        assert any(v.klass == "C11" for v in cl.cosmetic_violations)
        new, transforms = apply_cosmetic_remediations(content, cl)
        assert "### External Dependencies\n" in new
        assert "### Infrastructure Requirements\n" in new
        assert "(PRD-confirmed" not in new  # the parenthetical metadata is gone
        assert sum(1 for t in transforms if "resource H3" in t) == 2

    def test_mixed_cosmetic_and_semantic_refuses_to_remediate(self):
        # A cosmetic defect AND a semantic defect -> classify says not pure,
        # apply returns content unchanged.
        content = _content_with_milestone(
            [
                "### Integration Points",  # C2 cosmetic
                "### Milestone Dependencies",
                "### Risk Assessment",  # C1 cosmetic
                "{{SC_PLACEHOLDER:bad}}",  # semantic
            ]
        )
        cl = classify_gate_failure(content, _GATE, "x", step_id="s1")
        assert cl.is_pure_cosmetic is False
        assert cl.semantic_violations
        new, transforms = apply_cosmetic_remediations(content, cl)
        assert new == content
        assert transforms == []


# --------------------------------------------------------------------------
# Classification dataclass surface
# --------------------------------------------------------------------------


class TestClassificationDataclass:
    def test_step_id_and_gate_name_round_trip(self):
        content = _content_with_milestone(
            [
                "### Integration Points",
                "### Milestone Dependencies",
                "### Risk Assessment and Mitigation",
            ]
        )
        cl = classify_gate_failure(
            content,
            gate_name=_GATE,
            failure_reason="some reason",
            step_id="generate-opus-architect",
        )
        assert isinstance(cl, Classification)
        assert cl.gate_name == _GATE
        assert cl.step_id == "generate-opus-architect"


class TestComputeFencedIndices:
    """M1: precomputed fenced-block index set replaces O(N²) per-line walk.

    The new ``_compute_fenced_indices`` set must satisfy
    ``(idx in fenced_indices) == _is_in_fenced_block(lines, idx)`` for every
    line index, including delimiter lines. The existing helper counts fence
    markers in ``range(idx)``, which means the opener-marker line is
    EXCLUDED (count == 0 → False) and the closer-marker line is INCLUDED
    (count == 1 → True). The precompute MUST preserve this asymmetric truth
    function bit-for-bit — this is a performance refactor, not a behavior
    change.
    """

    def test_matches_is_in_fenced_block_on_mixed_sample(self):
        # Four fenced regions with text before / after / between them. Includes
        # a length-1 region (single line between adjacent fences) to exercise
        # the closer-immediately-after-opener edge.
        sample = (
            "intro line A\n"
            "intro line B\n"
            "```\n"          # opener of region 1 (idx=2) → EXCLUDED
            "inside 1a\n"    # idx=3 → INCLUDED
            "inside 1b\n"    # idx=4 → INCLUDED
            "```\n"          # closer of region 1 (idx=5) → INCLUDED
            "between A\n"    # idx=6 → EXCLUDED
            "```py\n"        # opener of region 2 (idx=7, with info string)
            "inside 2\n"     # idx=8 → INCLUDED
            "```\n"          # closer of region 2 (idx=9) → INCLUDED
            "between B\n"    # idx=10 → EXCLUDED
            "```\n"          # opener of region 3 (idx=11)
            "```\n"          # closer of region 3 (idx=12) — length-1 region
            "between C\n"    # idx=13 → EXCLUDED
            "  ```\n"        # opener of region 4, indented (idx=14)
            "inside 4\n"     # idx=15 → INCLUDED
            "```\n"          # closer of region 4 (idx=16) → INCLUDED
            "trailing\n"     # idx=17 → EXCLUDED
        )
        lines = sample.splitlines(keepends=True)
        fenced_indices = _compute_fenced_indices(lines)
        # Equivalence with the oracle helper across every index.
        for idx in range(len(lines)):
            assert (idx in fenced_indices) == _is_in_fenced_block(lines, idx), (
                f"semantic divergence at idx={idx!r}: "
                f"set={idx in fenced_indices} "
                f"helper={_is_in_fenced_block(lines, idx)}"
            )

    def test_empty_input(self):
        assert _compute_fenced_indices([]) == set()

    def test_no_fences(self):
        lines = ["plain line 1\n", "plain line 2\n", "plain line 3\n"]
        assert _compute_fenced_indices(lines) == set()
        for idx in range(len(lines)):
            assert not _is_in_fenced_block(lines, idx)

    def test_unclosed_fence_preserves_oracle_semantics(self):
        # Pathological case: opener with no closer. Whatever the helper
        # returns for trailing lines, the set must match — preserves
        # bit-for-bit equivalence even on malformed input.
        lines = "before\n```\nstill inside\nnever closes\n".splitlines(
            keepends=True
        )
        fenced_indices = _compute_fenced_indices(lines)
        for idx in range(len(lines)):
            assert (idx in fenced_indices) == _is_in_fenced_block(lines, idx)
