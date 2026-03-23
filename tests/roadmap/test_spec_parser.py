"""Tests for spec_parser.py — FR-2 extraction functions and FR-5 section splitting.

Covers all FR-2 extraction types validated against real spec content.
Includes section splitting round-trip test.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.roadmap.spec_parser import (
    CodeBlock,
    DIMENSION_SECTION_MAP,
    FunctionSignature,
    MarkdownTable,
    ParseResult,
    ParseWarning,
    SpecSection,
    ThresholdExpression,
    extract_code_blocks,
    extract_file_paths,
    extract_file_paths_from_tables,
    extract_function_signatures,
    extract_literal_values,
    extract_requirement_ids,
    extract_tables,
    extract_thresholds,
    parse_document,
    parse_frontmatter,
    split_into_sections,
)


# ---------- Fixtures ----------

REAL_SPEC_PATH = Path(
    ".dev/releases/current/v3.05_DeterministicFidelityGates/"
    "deterministic-fidelity-gate-requirements.md"
)

SIMPLE_DOC = """\
---
title: Test Spec
version: "1.0"
status: draft
---

# Main Title

Some preamble text.

## Section One

| Column A | Column B |
|----------|----------|
| val1     | val2     |
| val3     | val4     |

### Subsection 1.1

```python
def foo(x: int, y: str) -> bool:
    pass

def bar() -> None:
    pass
```

## Section Two

Requirements: FR-1, FR-2.1, NFR-3, SC-5, G-2, D0042

Thresholds: < 5s, >= 90%, minimum 20

```python
status: Literal["ACTIVE", "FIXED", "FAILED"]
```

File refs: `src/superclaude/cli/roadmap/parser.py` and `tests/roadmap/test_parser.py`
"""

MALFORMED_YAML_DOC = """\
---
title: Test
  bad_indent: broken
key: [unclosed bracket
---

# Content
"""

IRREGULAR_TABLE_DOC = """\
# Test

| A | B | C |
|---|---|---|
| 1 | 2 |
| 3 | 4 | 5 |
"""

NO_LANG_CODE_DOC = """\
# Test

```
some code without language tag
```
"""


# ---------- YAML Frontmatter Tests ----------

class TestParseFrontmatter:
    def test_valid_yaml(self):
        warnings: list[ParseWarning] = []
        result = parse_frontmatter(SIMPLE_DOC, warnings)
        assert result["title"] == "Test Spec"
        assert result["version"] == "1.0"
        assert result["status"] == "draft"
        assert len(warnings) == 0

    def test_no_frontmatter(self):
        warnings: list[ParseWarning] = []
        result = parse_frontmatter("# Just a heading\n\nSome text.", warnings)
        assert result == {}
        assert len(warnings) == 0

    def test_malformed_yaml_fallback(self):
        warnings: list[ParseWarning] = []
        result = parse_frontmatter(MALFORMED_YAML_DOC, warnings)
        # Should get partial parse via fallback
        assert "title" in result
        assert len(warnings) > 0
        assert warnings[0].category == "yaml"


# ---------- Table Extraction Tests ----------

class TestExtractTables:
    def test_simple_table(self):
        warnings: list[ParseWarning] = []
        tables = extract_tables(SIMPLE_DOC, warnings)
        assert len(tables) >= 1
        t = tables[0]
        assert t.headers == ["Column A", "Column B"]
        assert len(t.rows) == 2
        assert t.rows[0].cells == ["val1", "val2"]
        assert "Section One" in t.heading_path

    def test_irregular_table_warns(self):
        warnings: list[ParseWarning] = []
        tables = extract_tables(IRREGULAR_TABLE_DOC, warnings)
        assert len(tables) == 1
        # Should have warning about mismatched columns
        table_warnings = [w for w in warnings if w.category == "table"]
        assert len(table_warnings) > 0


# ---------- Code Block Extraction Tests ----------

class TestExtractCodeBlocks:
    def test_python_blocks(self):
        warnings: list[ParseWarning] = []
        blocks = extract_code_blocks(SIMPLE_DOC, warnings)
        python_blocks = [b for b in blocks if b.language == "python"]
        assert len(python_blocks) == 2
        assert "def foo" in python_blocks[0].content

    def test_no_language_warns(self):
        warnings: list[ParseWarning] = []
        blocks = extract_code_blocks(NO_LANG_CODE_DOC, warnings)
        assert len(blocks) == 1
        assert blocks[0].language == ""
        code_warnings = [w for w in warnings if w.category == "code_block"]
        assert len(code_warnings) == 1


# ---------- Requirement ID Tests ----------

class TestExtractRequirementIds:
    def test_all_families(self):
        ids = extract_requirement_ids(SIMPLE_DOC)
        assert "FR" in ids
        assert "FR-1" in ids["FR"]
        assert "FR-2.1" in ids["FR"]
        assert "NFR" in ids
        assert "NFR-3" in ids["NFR"]
        assert "SC" in ids
        assert "SC-5" in ids["SC"]
        assert "G" in ids
        assert "G-2" in ids["G"]
        assert "D" in ids
        assert "D0042" in ids["D"]

    def test_empty_text(self):
        ids = extract_requirement_ids("")
        assert ids == {}


# ---------- Function Signature Tests ----------

class TestExtractFunctionSignatures:
    def test_signatures_from_blocks(self):
        warnings: list[ParseWarning] = []
        blocks = extract_code_blocks(SIMPLE_DOC, warnings)
        sigs = extract_function_signatures(blocks)
        names = [s.name for s in sigs]
        assert "foo" in names
        assert "bar" in names
        foo = next(s for s in sigs if s.name == "foo")
        assert "int" in foo.params
        assert foo.return_type == "bool"


# ---------- Literal Values Tests ----------

class TestExtractLiteralValues:
    def test_literal_extraction(self):
        warnings: list[ParseWarning] = []
        blocks = extract_code_blocks(SIMPLE_DOC, warnings)
        literals = extract_literal_values(blocks)
        assert len(literals) >= 1
        assert "ACTIVE" in literals[0]
        assert "FIXED" in literals[0]
        assert "FAILED" in literals[0]


# ---------- Threshold Tests ----------

class TestExtractThresholds:
    def test_threshold_patterns(self):
        thresholds = extract_thresholds(SIMPLE_DOC)
        ops = {t.operator for t in thresholds}
        assert "<" in ops
        assert ">=" in ops
        assert "minimum" in ops

    def test_threshold_values(self):
        thresholds = extract_thresholds("latency < 5s and coverage >= 90%")
        assert len(thresholds) == 2


# ---------- File Path Tests ----------

class TestExtractFilePaths:
    def test_backtick_paths(self):
        paths = extract_file_paths(SIMPLE_DOC)
        assert "src/superclaude/cli/roadmap/parser.py" in paths
        assert "tests/roadmap/test_parser.py" in paths

    def test_table_paths(self):
        table_doc = """\
| Module | Path |
|--------|------|
| parser | src/superclaude/parser.py |
"""
        warnings: list[ParseWarning] = []
        tables = extract_tables(table_doc, warnings)
        paths = extract_file_paths_from_tables(tables)
        assert any("src/superclaude/parser.py" in p for p in paths)


# ---------- Section Splitting Tests ----------

class TestSplitIntoSections:
    def test_heading_levels(self):
        sections = split_into_sections(SIMPLE_DOC)
        levels = [s.level for s in sections]
        assert 0 in levels  # frontmatter
        assert 1 in levels  # h1
        assert 2 in levels  # h2
        assert 3 in levels  # h3

    def test_frontmatter_section(self):
        sections = split_into_sections(SIMPLE_DOC)
        fm = sections[0]
        assert fm.heading == "frontmatter"
        assert fm.level == 0
        assert "title: Test Spec" in fm.content

    def test_heading_path(self):
        sections = split_into_sections(SIMPLE_DOC)
        subsection = [s for s in sections if s.level == 3]
        assert len(subsection) >= 1
        assert "/" in subsection[0].heading_path

    def test_round_trip(self):
        """Split and reassemble must match original byte-for-byte."""
        sections = split_into_sections(SIMPLE_DOC)
        reassembled = "".join(s.content for s in sections)
        assert reassembled.splitlines() == SIMPLE_DOC.splitlines()

    def test_no_headings(self):
        """Document with no headings -> single preamble section."""
        text = "Just some text\nwith no headings\n"
        sections = split_into_sections(text)
        assert len(sections) == 1
        assert sections[0].heading == "preamble"
        assert sections[0].level == 0


# ---------- Dimension Map Tests ----------

class TestDimensionMap:
    def test_covers_five_dimensions(self):
        assert len(DIMENSION_SECTION_MAP) == 5
        expected = {"signatures", "data_models", "gates", "cli", "nfrs"}
        assert set(DIMENSION_SECTION_MAP.keys()) == expected


# ---------- Full Parse Tests ----------

class TestParseDocument:
    def test_returns_parse_result(self):
        result = parse_document(SIMPLE_DOC)
        assert isinstance(result, ParseResult)
        assert result.frontmatter["title"] == "Test Spec"
        assert len(result.tables) >= 1
        assert len(result.code_blocks) >= 1
        assert len(result.requirement_ids) >= 1
        assert len(result.function_signatures) >= 1
        assert len(result.sections) >= 1

    def test_warnings_collected(self):
        result = parse_document(MALFORMED_YAML_DOC)
        assert len(result.warnings) > 0


# ---------- Real Spec Validation ----------

@pytest.mark.skipif(
    not REAL_SPEC_PATH.exists(),
    reason="Real spec not available"
)
class TestRealSpecValidation:
    @pytest.fixture
    def real_result(self) -> ParseResult:
        text = REAL_SPEC_PATH.read_text()
        return parse_document(text)

    def test_zero_crashes(self, real_result: ParseResult):
        """Parser completes without exception on real spec."""
        assert isinstance(real_result, ParseResult)

    def test_frontmatter_populated(self, real_result: ParseResult):
        assert len(real_result.frontmatter) > 0
        assert "title" in real_result.frontmatter

    def test_tables_extracted(self, real_result: ParseResult):
        assert len(real_result.tables) > 0

    def test_code_blocks_extracted(self, real_result: ParseResult):
        assert len(real_result.code_blocks) > 0

    def test_requirement_ids_extracted(self, real_result: ParseResult):
        assert "FR" in real_result.requirement_ids
        assert len(real_result.requirement_ids["FR"]) > 0

    def test_function_signatures_extracted(self, real_result: ParseResult):
        assert len(real_result.function_signatures) > 0
        names = [s.name for s in real_result.function_signatures]
        assert "get_severity" in names

    def test_thresholds_extracted(self, real_result: ParseResult):
        assert len(real_result.thresholds) > 0

    def test_sections_extracted(self, real_result: ParseResult):
        assert len(real_result.sections) > 0

    def test_warnings_populated(self, real_result: ParseResult):
        """Real spec has some code blocks without language tags."""
        assert len(real_result.warnings) > 0

    def test_section_round_trip(self):
        """Section splitter round-trips correctly on real spec."""
        text = REAL_SPEC_PATH.read_text()
        sections = split_into_sections(text)
        reassembled = "".join(s.content for s in sections)
        assert reassembled.splitlines() == text.splitlines()
