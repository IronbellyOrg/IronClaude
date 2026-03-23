---
title: "Fix spec_structural_audit false positive: deduplicate test_name_count"
status: completed
priority: high
complexity: low
source: "GFxAI OntRAG pipeline — false positive warning (indicators=36, requirements=14)"
target_files:
  - src/superclaude/cli/roadmap/spec_structural_audit.py
  - tests/roadmap/test_spec_structural_audit.py
verification: "uv run pytest tests/roadmap/test_spec_structural_audit.py -v"
---

## Problem

`audit_spec_structure()` counts ALL occurrences of `test_\w+` in the spec text, not unique names. When a spec references the same test file multiple times across acceptance criteria, dependency notes, and exit criteria, the indicator count inflates dramatically.

**Evidence**: OntRAG spec has 5 unique test names mentioned 21 times total. This inflates `total_structural_indicators` from ~20 to 36, pushing the ratio from 0.70 (PASS) to 0.389 (FAIL at threshold 0.5).

## Root Cause

Line 55 of `spec_structural_audit.py`:
```python
test_name_count = len(re.findall(r"\btest_\w+", spec_text))
```
Should count unique matches, not total occurrences.

## Scope

- ONLY deduplicate `test_name_count` (proven false positive, high impact)
- Do NOT deduplicate `must_shall_count` (each keyword = different obligation)
- Do NOT deduplicate `function_signature_count` or `class_definition_count` (no evidence of false positives — YAGNI)

## Checklist

### Phase 1: Implementation

- [x] 1.1 — Change `test_name_count` in `audit_spec_structure()` at `src/superclaude/cli/roadmap/spec_structural_audit.py:55` from `len(re.findall(...))` to `len(set(re.findall(...)))`. Single line change. **File**: `spec_structural_audit.py:55`
- [x] 1.2 — Update docstring comment for `test_name_count` in `SpecStructuralAudit` dataclass at line 32: change `# test_* patterns` to `# Unique test_* patterns`. **File**: `spec_structural_audit.py:32`
- [x] 1.3 — Update `audit_spec_structure()` docstring to note that test name counting uses unique matches to avoid inflation from repeated references. **File**: `spec_structural_audit.py:38-43`

### Phase 2: Testing

- [x] 2.1 — Run existing test suite to verify no regressions: `uv run pytest tests/roadmap/test_spec_structural_audit.py -v`. All 20 tests must pass unchanged (RICH_SPEC fixture has 3 unique / 3 total test names — no behavior change).
- [x] 2.2 — Add `REPEATED_TEST_NAMES_SPEC` fixture to test file: a spec containing `test_foo`, `test_bar`, `test_foo`, `test_bar`, `test_foo` (3 occurrences of `test_foo`, 2 of `test_bar`) plus a MUST clause and a code block for non-zero other indicators. Place after `MIXED_SPEC` fixture. **File**: `tests/roadmap/test_spec_structural_audit.py`
- [x] 2.3 — Add `TestDeduplication` test class with: (a) `test_repeated_test_names_counted_uniquely` — asserts `test_name_count == 2` for the fixture (not 5), (b) `test_total_indicators_not_inflated_by_repeats` — asserts `total_structural_indicators` equals sum of individual counts. **File**: `tests/roadmap/test_spec_structural_audit.py`
- [x] 2.4 — Run full test suite again: `uv run pytest tests/roadmap/test_spec_structural_audit.py -v`. All tests including new ones must pass.

### Phase 3: Validation

- [x] 3.1 — Verify fix against the real OntRAG spec by running: `python3 -c "from superclaude.cli.roadmap.spec_structural_audit import check_extraction_adequacy; spec=open('/config/workspace/GFxAI/.dev/releases/current/feature-Ont-RAG/r0-r1/release-spec-ontrag-r0-r1.md').read(); passed,audit=check_extraction_adequacy(spec,14); print(f'passed={passed} indicators={audit.total_structural_indicators} test_names={audit.test_name_count} ratio={14/audit.total_structural_indicators:.3f}')"`. Expected: `passed=True`, `test_name_count=5`, `total_structural_indicators ~20`, ratio >= 0.5.
