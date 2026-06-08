# Tool-Write Test Baseline (Step 1.4)

**Command:** `uv run pytest tests/roadmap/ -k tool_write -q`
**Captured:** 2026-06-02 17:52

**Result (literal pytest output):** `157 passed, 1 skipped, 1808 deselected in 0.77s`

| Metric | Count |
|--------|-------|
| passed | 157 |
| skipped | 1 |
| deselected | 1808 |
| failed | 0 |

**Deviation from expected (research file 03 §5 = 157p/1s):** NONE — exact match.

This is the regression baseline. Phase 6 Step 6.3 compares against it: the new run must have 0 failures and passed >= 157 (the MD regression + parametrized cases ADD to the count).
