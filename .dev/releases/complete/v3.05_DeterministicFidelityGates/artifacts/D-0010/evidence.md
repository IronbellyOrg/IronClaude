# D-0010: Test Coverage Evidence

**Task**: T01.06
**File**: `tests/roadmap/test_spec_parser.py`
**Result**: 33/33 PASS

## Test Names and Results

| Test | Status |
|---|---|
| TestParseFrontmatter::test_valid_yaml | PASS |
| TestParseFrontmatter::test_no_frontmatter | PASS |
| TestParseFrontmatter::test_malformed_yaml_fallback | PASS |
| TestExtractTables::test_simple_table | PASS |
| TestExtractTables::test_irregular_table_warns | PASS |
| TestExtractCodeBlocks::test_python_blocks | PASS |
| TestExtractCodeBlocks::test_no_language_warns | PASS |
| TestExtractRequirementIds::test_all_families | PASS |
| TestExtractRequirementIds::test_empty_text | PASS |
| TestExtractFunctionSignatures::test_signatures_from_blocks | PASS |
| TestExtractLiteralValues::test_literal_extraction | PASS |
| TestExtractThresholds::test_threshold_patterns | PASS |
| TestExtractThresholds::test_threshold_values | PASS |
| TestExtractFilePaths::test_backtick_paths | PASS |
| TestExtractFilePaths::test_table_paths | PASS |
| TestSplitIntoSections::test_heading_levels | PASS |
| TestSplitIntoSections::test_frontmatter_section | PASS |
| TestSplitIntoSections::test_heading_path | PASS |
| TestSplitIntoSections::test_round_trip | PASS |
| TestSplitIntoSections::test_no_headings | PASS |
| TestDimensionMap::test_covers_five_dimensions | PASS |
| TestParseDocument::test_returns_parse_result | PASS |
| TestParseDocument::test_warnings_collected | PASS |
| TestRealSpecValidation::test_zero_crashes | PASS |
| TestRealSpecValidation::test_frontmatter_populated | PASS |
| TestRealSpecValidation::test_tables_extracted | PASS |
| TestRealSpecValidation::test_code_blocks_extracted | PASS |
| TestRealSpecValidation::test_requirement_ids_extracted | PASS |
| TestRealSpecValidation::test_function_signatures_extracted | PASS |
| TestRealSpecValidation::test_thresholds_extracted | PASS |
| TestRealSpecValidation::test_sections_extracted | PASS |
| TestRealSpecValidation::test_warnings_populated | PASS |
| TestRealSpecValidation::test_section_round_trip | PASS |
