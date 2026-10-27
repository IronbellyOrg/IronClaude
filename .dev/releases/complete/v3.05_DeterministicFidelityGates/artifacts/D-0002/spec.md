# D-0002: Spec Parser API Documentation

**Module**: `src/superclaude/cli/roadmap/spec_parser.py`
**Implements**: FR-2

## Public API

### Data Classes
- `ParseWarning(category, message, location)` — degradation warning
- `CodeBlock(language, content, start_line, end_line)` — fenced code block
- `TableRow(cells)` — single table row
- `MarkdownTable(heading_path, headers, rows, start_line, end_line)` — extracted table
- `FunctionSignature(name, params, return_type)` — Python function signature
- `ThresholdExpression(operator, value, raw)` — numeric threshold
- `SpecSection(heading, heading_path, level, content, start_line, end_line)` — document section
- `ParseResult(frontmatter, tables, code_blocks, requirement_ids, function_signatures, literal_values, thresholds, file_paths, sections, warnings)` — aggregated result

### Functions
- `parse_document(text) -> ParseResult` — full parse pipeline
- `parse_frontmatter(text, warnings) -> dict` — YAML frontmatter extraction
- `extract_tables(text, warnings) -> list[MarkdownTable]` — table extraction
- `extract_code_blocks(text, warnings) -> list[CodeBlock]` — fenced block extraction
- `extract_requirement_ids(text) -> dict[str, list[str]]` — requirement ID families
- `extract_function_signatures(code_blocks) -> list[FunctionSignature]` — Python signatures
- `extract_literal_values(code_blocks) -> list[list[str]]` — Literal enum values
- `extract_thresholds(text) -> list[ThresholdExpression]` — numeric thresholds
- `extract_file_paths(text) -> list[str]` — backtick-quoted file paths
- `extract_file_paths_from_tables(tables) -> list[str]` — paths from table cells
- `split_into_sections(text) -> list[SpecSection]` — heading-based sectional splitting
- `DIMENSION_SECTION_MAP` — dimension-to-section routing dict
