# Full Tool-Write Suite — Final vs Baseline (Step 6.3)

**Command:** `uv run pytest tests/roadmap/ -k tool_write -q`
**Captured:** 2026-06-02 18:04
**Verdict: PASS — no regression, count increased as expected.**

| Metric | Baseline (Step 1.4) | Final (Step 6.3) | Delta |
|--------|---------------------|------------------|-------|
| passed | 157 | **161** | **+4** |
| skipped | 1 | 1 | 0 |
| deselected | 1808 | 1808 | 0 |
| failed | 0 | 0 | 0 |

- **0 failures.** Final passed count (161) ≥ baseline (157).
- The **+4** is exactly the new `test_all_schemas_accept_md_family[extract|extract_tdd|generate|merge]` parametrized regression cases added in Step 5.5.
- All 55 extra-family fixture usages still pass (no previously-passing test flipped to fail — the four rebuilt guard tests and all `test_valid_output_passes_schema` / id-check render tests remain green).
- Result line: `161 passed, 1 skipped, 1808 deselected in 0.80s`.
