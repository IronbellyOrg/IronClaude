# Structural Comparison: wiring-verification.md

**Test 2**: `.dev/test-fixtures/results/test2-spec-modified/wiring-verification.md`
**Test 3**: `.dev/test-fixtures/results/test3-spec-baseline/wiring-verification.md`

---

## Frontmatter Field Comparison

| Field Name | Test 2 | Test 3 | Status |
|---|---|---|---|
| gate | PRESENT | PRESENT | MATCH |
| target_dir | PRESENT | PRESENT | MATCH |
| files_analyzed | PRESENT | PRESENT | MATCH |
| files_skipped | PRESENT | PRESENT | MATCH |
| rollout_mode | PRESENT | PRESENT | MATCH |
| analysis_complete | PRESENT | PRESENT | MATCH |
| audit_artifacts_used | PRESENT | PRESENT | MATCH |
| unwired_callable_count | PRESENT | PRESENT | MATCH |
| orphan_module_count | PRESENT | PRESENT | MATCH |
| unwired_registry_count | PRESENT | PRESENT | MATCH |
| critical_count | PRESENT | PRESENT | MATCH |
| major_count | PRESENT | PRESENT | MATCH |
| info_count | PRESENT | PRESENT | MATCH |
| total_findings | PRESENT | PRESENT | MATCH |
| blocking_findings | PRESENT | PRESENT | MATCH |
| whitelist_entries_applied | PRESENT | PRESENT | MATCH |

**Field Count**: Test 2 = 16, Test 3 = 16 -- MATCH

---

## Body Section Header Comparison

| Section Header | Test 2 | Test 3 | Status |
|---|---|---|---|
| ## Summary | PRESENT | PRESENT | MATCH |
| ## Unwired Optional Callable Injections | PRESENT | PRESENT | MATCH |
| ## Orphan Modules / Symbols | PRESENT | PRESENT | MATCH |
| ## Unregistered Dispatch Entries | PRESENT | PRESENT | MATCH |
| ## Suppressions and Dynamic Retention | PRESENT | PRESENT | MATCH |
| ## Recommended Remediation | PRESENT | PRESENT | MATCH |
| ## Evidence and Limitations | PRESENT | PRESENT | MATCH |

**Header Count**: Test 2 = 7, Test 3 = 7 -- MATCH

---

## Value Comparison (codebase-derived, should be near-identical)

| Metric | Test 2 | Test 3 | Status |
|---|---|---|---|
| files_analyzed | 166 | 166 | MATCH |
| files_skipped | 31 | 31 | MATCH |
| rollout_mode | soft | soft | MATCH |
| total_findings | 7 | 7 | MATCH |
| blocking_findings | 0 | 0 | MATCH |
| orphan_module_count | 7 | 7 | MATCH |
| critical_count | 0 | 0 | MATCH |
| major_count | 7 | 7 | MATCH |
| scan_duration | 0.4995s | 0.4917s | ~MATCH |

All 7 orphan modules are identical between both runs (same 7 cli_portify steps files).

---

## Notes

- Wiring verification is codebase-derived (static analysis), not LLM-generated. Both runs analyze the same codebase and produce identical results.
- All 16 frontmatter fields match in name and value.
- All 7 section headers are identical.
- All 7 orphan module findings are the same files in both runs.
- This is the strongest structural match of all 9 artifacts, as expected for a deterministic static analysis tool.

---

## Overall Verdict: MATCH

Structural equivalence confirmed. Near-identical output in both structure and values. This is expected because wiring-verification is codebase-derived, not LLM-generated.
