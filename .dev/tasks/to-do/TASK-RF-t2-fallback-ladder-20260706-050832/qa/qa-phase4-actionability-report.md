# QA Report — Swarm-Test Actionability Lens (Step 4.G4)

**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**Date:** 2026-07-07
**Phase:** task-qualitative (swarm-test actionability lens, report-only)

## Overall Verdict: PASS (with 2 MINOR advisory findings)

All 5 required verification targets are satisfied and the new tests are demonstrably concrete (mutation-verified). Two MINOR mirror-completeness gaps are recorded; neither defeats actionability (a real T1/F3 regression is still caught).

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | T1 config tests mirror T2 | PASS | 5 sub-assertions present. Mutation (`t1_models=()`) → 4/5 T1 tests FAIL; empty-default correctly stays green. |
| 2 | F3 `read_env_for_pool` reads T1 pool | PASS | Asserts base_url/api_key/models. Mutation (hardcode T2 prefix) → T1 tests FAIL. |
| 3 | F3 missing-T1-vars raise with T1 names | PASS (minor gap) | Only all-missing case tested; partial-absence not mirrored (MINOR-1). |
| 4 | F3 thin `read_env` still passes T2 body | PASS | T2 body intact; mutation (`max_slots=2` wrapper) → T2 happy-path FAILS. |
| 5 | wrapper == pool reader for T2 | PASS (under-powered) | `read_env(env) == read_env_for_pool(T2…)`; only 2 models → can't alone detect slot-count divergence (MINOR-2). |
| 6 | Network-free | PASS | Env dicts only; no httpx.Client; live lane skipif-gated. |
| 7 | No clobber of T2 regression body | PASS | `git diff` +137/−0; 46/46 pass. |
| 8 | Concrete, not tautological | PASS | 3 mutations → targeted FAILs. |

## Summary
- Checks passed: 8 / 8 (all 5 required targets satisfied)
- Critical: 0 | Important: 0 | Minor: 2

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | test_openai_compat.py (T1 missing-var) | T1 missing-var coverage asymmetric with T2 (T2 has 4 distinct missing-var tests; T1 only has all-missing). | Add ≥1 partial-absence T1 case (e.g. `T1ProxyUrl`+`T1Model01` set, `T1ProxyKey` absent) asserting `"T1ProxyKey" in .missing`. |
| 2 | MINOR | test_openai_compat.py (wrapper==pool) | Equivalence test uses only 2 model slots → can't independently detect a `max_slots` divergence. | Broaden the delegation test to a dense-skip / near-ceiling shape so `via_wrapper == via_pool` also certifies slot-count equivalence. |

## Observations (not scored)

- **Source whitespace inconsistency (pre-existing, not test-introduced):** config `_collect_models` uses `if value:` with no `.strip()`, whereas transport `read_env_for_pool` strips before the truthiness check. This T2-vs-config asymmetry predates this change (the original `_collect_t2_models` also did not strip); the tests faithfully mirror each other. Out of the test-actionability scope; noted for source-review.
- Magic literals (`"T1Model0"`, `9`) in T1 transport tests are acceptable — `read_env_for_pool` is a generic parameterized reader.
- Ceiling test quirk (`T1Model010` never probed) mirrors the T2 ceiling test exactly — not a defect.

## Recommendations

Proceed. Optionally address MINOR-1 (partial-absence T1 test) and MINOR-2 (broaden equivalence test) for full T1↔T2 parity — additive test-only edits.

## QA Complete
