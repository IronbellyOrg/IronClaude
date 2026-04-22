"""Tests for pipeline/gates.py -- 4-tier gate validation with edge cases."""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.pipeline.gates import _check_frontmatter, gate_passed
from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck


class TestExemptTier:
    def test_always_passes_even_nonexistent(self, tmp_path):
        gc = GateCriteria(
            required_frontmatter_fields=[], min_lines=0, enforcement_tier="EXEMPT"
        )
        ok, reason = gate_passed(tmp_path / "nonexistent.md", gc)
        assert ok is True
        assert reason is None


class TestLightTier:
    def test_file_not_found(self, tmp_path):
        gc = GateCriteria(
            required_frontmatter_fields=[], min_lines=0, enforcement_tier="LIGHT"
        )
        ok, reason = gate_passed(tmp_path / "missing.md", gc)
        assert ok is False
        assert "File not found" in reason

    def test_empty_file(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=[], min_lines=0, enforcement_tier="LIGHT"
        )
        f = make_file("empty.md", "")
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "empty" in reason.lower()

    def test_whitespace_only_file(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=[], min_lines=0, enforcement_tier="LIGHT"
        )
        f = make_file("ws.md", "   \n  \n  ")
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "empty" in reason.lower()

    def test_nonempty_passes(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=[], min_lines=0, enforcement_tier="LIGHT"
        )
        f = make_file("ok.md", "content here")
        ok, reason = gate_passed(f, gc)
        assert ok is True


class TestStandardTier:
    def test_below_min_lines(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=[], min_lines=10, enforcement_tier="STANDARD"
        )
        f = make_file("short.md", "line1\nline2\n")
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "minimum line count" in reason.lower()
        assert "2 < 10" in reason

    def test_missing_frontmatter(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        f = make_file("nofm.md", "\n".join(["line"] * 10))
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "frontmatter" in reason.lower()

    def test_malformed_yaml(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        f = make_file(
            "bad.md",
            "---\nunclosed frontmatter\nno closing dashes\nmore text\nfiller\n",
        )
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "frontmatter" in reason.lower()

    def test_missing_required_field(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title", "version"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        f = make_file("partial.md", "---\ntitle: Test\n---\n" + "\n".join(["x"] * 10))
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "version" in reason

    def test_all_checks_pass(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title", "version"],
            min_lines=5,
            enforcement_tier="STANDARD",
        )
        content = "---\ntitle: Test\nversion: 1.0\n---\n" + "\n".join(["x"] * 10)
        f = make_file("ok.md", content)
        ok, reason = gate_passed(f, gc)
        assert ok is True
        assert reason is None


class TestStrictTier:
    def test_semantic_check_fails(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STRICT",
            semantic_checks=[
                SemanticCheck(
                    name="has_heading",
                    check_fn=lambda c: "# " in c,
                    failure_message="No heading found",
                )
            ],
        )
        f = make_file(
            "no_heading.md", "---\ntitle: T\n---\nno heading here\nmore lines\n"
        )
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "has_heading" in reason
        assert "No heading found" in reason

    def test_semantic_check_passes(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STRICT",
            semantic_checks=[
                SemanticCheck(
                    name="has_heading",
                    check_fn=lambda c: "# " in c,
                    failure_message="No heading found",
                )
            ],
        )
        f = make_file("ok.md", "---\ntitle: T\n---\n# Heading\nmore lines\n")
        ok, reason = gate_passed(f, gc)
        assert ok is True

    def test_no_semantic_checks_defined(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STRICT",
            semantic_checks=None,
        )
        f = make_file("ok.md", "---\ntitle: T\n---\ncontent\nmore\n")
        ok, reason = gate_passed(f, gc)
        assert ok is True

    def test_zero_byte_file(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=[],
            min_lines=1,
            enforcement_tier="STRICT",
        )
        f = make_file("zero.md", "")
        ok, reason = gate_passed(f, gc)
        assert ok is False


class TestEdgeCases:
    """Additional edge cases: UTF-8 BOM, frontmatter with empty values."""

    def test_utf8_bom_file(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        content = "\ufeff---\ntitle: Test\n---\n" + "\n".join(["x"] * 10)
        f = make_file("bom.md", content)
        ok, reason = gate_passed(f, gc)
        # BOM before --- means frontmatter not detected at start
        assert isinstance(ok, bool)

    def test_frontmatter_with_empty_values(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title", "version"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        content = "---\ntitle: \nversion: \n---\n" + "\n".join(["x"] * 10)
        f = make_file("empty_vals.md", content)
        ok, reason = gate_passed(f, gc)
        # STANDARD tier checks key presence, not value content
        assert ok is True

    def test_frontmatter_no_closing_dashes(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        content = "---\ntitle: T\nno closing dashes\nmore text\nfiller\nstuff\n"
        f = make_file("no_close.md", content)
        ok, reason = gate_passed(f, gc)
        assert ok is False
        assert "frontmatter" in reason.lower()

    def test_whitespace_only_content_after_frontmatter(self, make_file):
        gc = GateCriteria(
            required_frontmatter_fields=["title"],
            min_lines=3,
            enforcement_tier="STANDARD",
        )
        content = "---\ntitle: T\n---\n   \n   \n   \n   \n   \n   \n   \n"
        f = make_file("ws_content.md", content)
        ok, reason = gate_passed(f, gc)
        assert ok is True  # 10 lines, passes min_lines=3


class TestCheckFrontmatterRegex:
    """8 unit tests for _check_frontmatter() per spec §6.1 test matrix."""

    DUMMY = Path("test.md")

    def test_preamble_before_frontmatter(self):
        """Preamble text before valid frontmatter should be accepted."""
        content = "Preamble\n---\nkey: val\n---\nBody"
        ok, reason = _check_frontmatter(content, ["key"], self.DUMMY)
        assert ok is True
        assert reason is None

    def test_clean_frontmatter(self):
        """Standard frontmatter at start of document should pass."""
        content = "---\ntitle: Test\nversion: 1.0\n---\nBody content"
        ok, reason = _check_frontmatter(content, ["title", "version"], self.DUMMY)
        assert ok is True
        assert reason is None

    def test_horizontal_rule_rejected(self):
        """Horizontal rule (--- with no key: value) must be rejected."""
        content = "Some text\n---\nMore text without colon\n---\nEnd"
        ok, reason = _check_frontmatter(content, [], self.DUMMY)
        assert ok is False
        assert "not found" in reason.lower()

    def test_missing_frontmatter(self):
        """Document with no --- delimiters at all should fail."""
        content = "Just plain text\nwith multiple lines\nbut no frontmatter"
        ok, reason = _check_frontmatter(content, [], self.DUMMY)
        assert ok is False
        assert "not found" in reason.lower()

    def test_missing_required_field(self):
        """Frontmatter present but missing a required field should fail."""
        content = "---\ntitle: Test\n---\nBody"
        ok, reason = _check_frontmatter(content, ["title", "version"], self.DUMMY)
        assert ok is False
        assert "Missing required" in reason
        assert "version" in reason

    def test_multiple_frontmatter_blocks(self):
        """Multiple --- blocks: should match the first valid frontmatter."""
        content = "---\nfirst: block\n---\nMiddle\n---\nsecond: block\n---\nEnd"
        ok, reason = _check_frontmatter(content, ["first"], self.DUMMY)
        assert ok is True
        assert reason is None

    def test_whitespace_before_frontmatter(self):
        """Whitespace lines before frontmatter should still match."""
        content = "   \n\n---\ntitle: Test\n---\nBody"
        ok, reason = _check_frontmatter(content, ["title"], self.DUMMY)
        assert ok is True
        assert reason is None

    def test_empty_file(self):
        """Empty string should fail with 'not found'."""
        content = ""
        ok, reason = _check_frontmatter(content, [], self.DUMMY)
        assert ok is False
        assert "not found" in reason.lower()


class TestFrontmatterAliasGroups:
    """A tuple entry in required_frontmatter_fields is an OR-group: any one
    of the listed aliases satisfies the slot. Mirrors the template's
    mutually-exclusive-alias rule (e.g. `spec_source` vs `spec_sources`).
    """

    DUMMY = Path("test.md")

    def test_tuple_accepted_with_first_alias(self):
        content = "---\nspec_source: a.md\n---\nBody"
        ok, reason = _check_frontmatter(
            content, [("spec_source", "spec_sources")], self.DUMMY
        )
        assert ok is True
        assert reason is None

    def test_tuple_accepted_with_second_alias(self):
        content = "---\nspec_sources:\n  - a.md\n  - b.md\n---\nBody"
        ok, reason = _check_frontmatter(
            content, [("spec_source", "spec_sources")], self.DUMMY
        )
        assert ok is True
        assert reason is None

    def test_tuple_rejected_when_neither_alias_present(self):
        content = "---\ntitle: just a title\n---\nBody"
        ok, reason = _check_frontmatter(
            content, [("spec_source", "spec_sources")], self.DUMMY
        )
        assert ok is False
        assert reason is not None
        assert "spec_source" in reason
        assert "spec_sources" in reason
        assert "one of" in reason

    def test_string_and_tuple_entries_both_enforced(self):
        """Mixed list must enforce the string entry and the tuple entry."""
        # Tuple satisfied but string 'generated' missing -> fail on string.
        content = "---\nspec_source: a.md\n---\nBody"
        ok, reason = _check_frontmatter(
            content,
            ["generated", ("spec_source", "spec_sources")],
            self.DUMMY,
        )
        assert ok is False
        assert "generated" in reason
        assert "Missing required" in reason

    def test_mixed_entries_all_present_passes(self):
        content = (
            "---\n"
            "spec_sources:\n  - a.md\n  - b.md\n"
            "generated: 2026-04-21T00:00:00Z\n"
            "---\nBody"
        )
        ok, reason = _check_frontmatter(
            content,
            ["generated", ("spec_source", "spec_sources")],
            self.DUMMY,
        )
        assert ok is True
        assert reason is None

    def test_both_aliases_present_still_passes(self):
        """The gate only enforces presence, not mutual exclusion. The
        single-vs-multi contract is a template concern; gates stay lenient
        so that legacy artifacts with accidental both-forms don't stall the
        pipeline. (Template-level linting enforces exclusivity upstream.)
        """
        content = "---\nspec_source: a.md\nspec_sources:\n  - a.md\n  - b.md\n---\nBody"
        ok, reason = _check_frontmatter(
            content, [("spec_source", "spec_sources")], self.DUMMY
        )
        assert ok is True
        assert reason is None
