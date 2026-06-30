# Merge Log

## Metadata
- Base: Variant 1 (proposed), byte-identical to OURS
- Executor: merge-executor (no-op merge — base already final)
- Changes applied: 0
- Status: success
- Timestamp: 2026-06-04
- merged-output.md SHA-256: `3dce671fb375148764ac9a50916cad03ebca58c1d1adf728961c653066cd7b53` (== `.resolved`)

## Changes Applied
None. Base variant adopted verbatim as the merged output.

## Post-Merge Validation
- **Structural integrity**: PASS — `ast.parse` succeeds; 12 classes / 66 test nodes intact.
- **Conflict markers**: PASS — zero `<<<<<<< / ======= / >>>>>>>` lines.
- **Coverage union**: PASS — merged node-set == OURS node-set == THEIRS node-set (66 nodes); the 4 MD-family additions (`_write_md_fixture_with_allowlist` + 3 tests) present.
- **Name-shadowing rescan**: PASS — no within-class duplicate method names; repeated names (`test_all_findings_have_correct_dimension`, `test_findings_use_correct_machine_keys`, `test_findings_have_severity_from_rules`, `test_produces_findings`) are class-scoped across distinct checker test classes and collected independently by pytest. Zero module-level duplicate functions.
- **Contract conformance**: PASS — MD-family fixtures (`M1-D01`…`M3-D01`) align with `ID_PATTERNS["MD"] = M\d+-D-?\d+`.
- **New contradictions introduced**: 0.

## Summary
- Planned: 0 | Applied: 0 | Failed: 0 | Skipped: 0
- Merged output is the resolved test file with the single L1 comment-header diff (C-001) resolved toward the branch-local provenance label.
