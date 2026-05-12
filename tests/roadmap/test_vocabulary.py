"""Tests for shared obligation vocabulary module."""

from __future__ import annotations

from superclaude.cli.vocabulary import (
    DISCHARGE_TERMS,
    PREFERRED_ALTERNATIVES,
    SCAFFOLD_TERMS,
    build_prompt_constraint_block,
)


class TestScaffoldTerms:
    def test_has_exactly_11_entries(self):
        assert len(SCAFFOLD_TERMS) == 11

    def test_all_entries_are_word_boundary_regex(self):
        for term in SCAFFOLD_TERMS:
            assert term.startswith(r"\b"), f"{term} missing word boundary"


class TestDischargeTerms:
    def test_has_exactly_9_entries(self):
        assert len(DISCHARGE_TERMS) == 9


class TestPreferredAlternatives:
    def test_has_16_entries(self):
        assert len(PREFERRED_ALTERNATIVES) == 16

    def test_covers_all_scaffold_stems(self):
        base_words = [
            "mock", "stub", "skeleton", "placeholder", "scaffold",
            "temporary", "hardcoded", "hardwired", "no-op", "dummy", "fake",
        ]
        for word in base_words:
            matches = [k for k in PREFERRED_ALTERNATIVES if word in k or k in word]
            assert matches, f"No alternative for scaffold term '{word}'"


class TestBuildPromptConstraintBlock:
    def test_output_under_800_chars(self):
        block = build_prompt_constraint_block()
        assert len(block) < 800, f"Block is {len(block)} chars, likely >200 tokens"

    def test_contains_vocabulary_constraint_header(self):
        block = build_prompt_constraint_block()
        assert "VOCABULARY CONSTRAINT" in block

    def test_contains_at_least_one_alternative(self):
        block = build_prompt_constraint_block()
        assert "\u2192" in block


class TestVocabularyIdentity:
    """Verify obligation_scanner imports from vocabulary (not local copies)."""

    def test_scanner_scaffold_terms_is_same_object(self):
        from superclaude.cli.roadmap.obligation_scanner import (
            SCAFFOLD_TERMS as scanner_terms,
        )
        assert scanner_terms is SCAFFOLD_TERMS

    def test_scanner_discharge_terms_is_same_object(self):
        from superclaude.cli.roadmap.obligation_scanner import (
            DISCHARGE_TERMS as scanner_terms,
        )
        assert scanner_terms is DISCHARGE_TERMS
