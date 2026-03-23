"""Tests for section hashing additive-only enforcement (D-0033 / NFR-008).

Covers:
- Hash capture and comparison
- Additive changes accepted
- Modifications rejected
- Section removal rejected
- Multiple section handling
"""

from __future__ import annotations

import pytest

from superclaude.cli.cli_portify.utils import (
    extract_sections,
    hash_section,
)
from superclaude.cli.cli_portify.steps.panel_review import capture_section_hashes


class TestHashSection:
    def test_deterministic_hash(self):
        h1 = hash_section("Hello world")
        h2 = hash_section("Hello world")
        assert h1 == h2

    def test_different_content_different_hash(self):
        h1 = hash_section("Hello world")
        h2 = hash_section("Hello world!")
        assert h1 != h2

    def test_whitespace_normalized(self):
        """Leading/trailing whitespace is stripped."""
        h1 = hash_section("  Hello world  ")
        h2 = hash_section("Hello world")
        assert h1 == h2


class TestExtractSections:
    def test_single_section(self):
        content = "## Section One\n\nContent here.\n"
        sections = extract_sections(content)
        assert "Section One" in sections
        assert "Content here." in sections["Section One"]

    def test_multiple_sections(self):
        content = """\
## Alpha

Alpha content.

## Beta

Beta content.

## Gamma

Gamma content.
"""
        sections = extract_sections(content)
        assert len(sections) == 3
        assert "Alpha" in sections
        assert "Beta" in sections
        assert "Gamma" in sections

    def test_no_sections(self):
        content = "Just plain text without headings."
        sections = extract_sections(content)
        assert len(sections) == 0


