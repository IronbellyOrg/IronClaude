# D-0033: AST Plugin for ToolOrchestrator

## Deliverable
AST analyzer plugin function `ast_references_plugin` in `src/superclaude/cli/audit/wiring_analyzer.py` that hooks into the `ToolOrchestrator` plugin seam and populates `FileAnalysis.references` with import-derived cross-file references.

## Implementation

### Plugin Interface (tool_orchestrator.py)
- Added `register_plugin()` method to `ToolOrchestrator`
- Added `plugins` property for read-only access to registered plugins
- Plugin signature: `(str, str, FileAnalysis) -> FileAnalysis`
- Plugins run after primary analyzer in `analyze_file()`, in registration order
- Results cached after plugin enrichment

### Plugin Function (wiring_analyzer.py)
- `ast_references_plugin(file_path, content, analysis)` → enriched `FileAnalysis`
- Parses content with `ast.parse()` to extract cross-file references
- Merges AST-derived references with existing `FileAnalysis.references`
- Handles `SyntaxError` gracefully — returns original analysis unchanged
- Zero imports from `pipeline/*` (NFR-007 compliance)

## Acceptance Criteria Verification
- [x] Plugin registers with ToolOrchestrator without modifying existing interface
- [x] FileAnalysis.references populated with import-derived references for files with imports
- [x] Plugin handles circular imports and missing modules without raising exceptions
- [x] No imports from pipeline/* in wiring_analyzer.py (NFR-007)

## Validation
- `uv run pytest tests/audit/test_wiring_analyzer.py -k "plugin" -v` exits 0 (5 tests pass)
