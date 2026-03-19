# D-0034: Dual Evidence Rule for Orphan Detection

## Deliverable
Dual evidence rule implementation in `wiring_gate.py` that combines import-graph evidence with `FileAnalysis.references` evidence before confirming orphan status.

## Implementation

### Modified Function: `analyze_orphan_modules()`
- Added optional `file_references: dict[str, list[str]] | None` parameter
- When `file_references` is provided (dual evidence active):
  - Aggregates all references into a set
  - Module must have BOTH zero imports AND zero references to be flagged
  - Modules with references but no imports are NOT flagged (false positive prevention)
  - Finding detail includes "(dual evidence: import-graph + AST references)"
- When `file_references` is None (plugin not loaded):
  - Falls back to import-graph-only evidence
  - Finding detail includes "(import-graph only; AST plugin not loaded)"
- Backward-compatible: existing callers pass no `file_references` argument

## Acceptance Criteria Verification
- [x] Orphan detection requires both import-graph and FileAnalysis.references when plugin loaded
- [x] Modules with FileAnalysis.references but no imports NOT flagged as orphans
- [x] Fallback to import-graph-only with note when plugin not loaded
- [x] Dual evidence rule reduces false positive rate

## Validation
- `uv run pytest tests/audit/ -k "dual_evidence" -v` exits 0 (3 tests pass)
- All 78 existing wiring gate tests pass (zero regressions)
