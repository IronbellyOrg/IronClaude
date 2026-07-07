# QA Report — Phase 2 Verdict-Honesty Qualitative QA

**Topic:** Reflect Tier-2 Fallback Ladder — Phase 2 verdict-honesty/domain lens
**Date:** 2026-07-06
**Phase:** Step 2.G4 verdict-honesty review
**Fix authorization:** false

---

## Overall Verdict: FAIL

Phase 2's implementation and tests get the core F6 first-match ordering right, and the scoped test run is green. However, the verdict-honesty test coverage is weaker than the design's "terminal_reason rides alongside, never gates" guarantee requires. `contract.py` does NOT currently gate on `t2_fallback` (correct), but the Phase 2 tests do not pin the design §8 degraded-with-fallback-metadata counter-case, and two assertions are too narrow.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | F6 test asserts `degraded-tier1` as verdict reason and does not assert `single-reviewer-fallback` as the reason | PASS | `test_degraded_tier1_first_match_precedes_single_reviewer_fallback` sets `merge_method="single-reviewer-fallback"`, asserts it only as a contract field, and asserts `result.reason == "degraded-tier1"`. |
| 2 | Metadata `terminal_reason` is treated as explanatory telemetry alongside the real first-match reason, never the gate | FAIL | Source is correct (no `t2_fallback`/`terminal_reason` reference in `contract.py`), but no test pins a degraded contract where a populated `t2_fallback.terminal_reason` coexists with the real `degraded-tier1` first-match reason. |
| 3 | No-proxy-key assertion dumps YAML and searches for proxy strings | FAIL | Test dumps YAML and checks env-var-name fragments, but does not catch lower-case/value shapes such as `proxy_url`, `proxy_key`, `api_key`, `base_url`, `http://`, `https://`, `:4000/cli`. |
| 4 | Metadata tests do not imply `t2_fallback` changes verdict behavior | FAIL | `test_populated_fallback_metadata_does_not_change_verdict` asserts verdict enum and exit code but not `reason` equality; a fallback-derived reason change preserving PASS/0 would slip through. |

## Summary

- Checks passed: 1 / 4
- Checks failed: 3
- Important issues: 3

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `tests/cli/reflect/test_verdict_mapping.py` and/or `tests/cli/reflect/test_contract_fallback_metadata.py` | No test proves the design §8 counter-case: a degraded fallback outcome may carry `t2_fallback.terminal_reason` (e.g. `fallback_pool_exhausted`) but the real returned verdict reason must still be first-match `degraded-tier1`. | Add a test that builds/loads a Tier-1 degraded contract, sets `merge_method: single-reviewer-fallback`, attaches a populated `t2_fallback` block with `terminal_reason: fallback_pool_exhausted`, asserts `derive_verdict(...).reason == "degraded-tier1"` AND `contract["t2_fallback"]["terminal_reason"] == "fallback_pool_exhausted"`. |
| 2 | IMPORTANT | `tests/cli/reflect/test_contract_fallback_metadata.py` | Populated `t2_fallback` verdict-unchanged regression compares verdict enum and exit code but not returned reason. | Extend `test_populated_fallback_metadata_does_not_change_verdict` to assert `with_fallback.reason == without_fallback.reason`. |
| 3 | IMPORTANT | `tests/cli/reflect/test_contract_fallback_metadata.py` | No-proxy leak test checks env-var-name fragments only, missing lower-case/value leak shapes. | Broaden the forbidden-string list to include `T1ProxyUrl`, `T2ProxyUrl`, `proxy_url`, `proxy_key`, `api_key`, `base_url`, `http://`, `https://`, `:4000/cli`, while avoiding the legitimate `proxy_error` status token. Keep the YAML dump as the searched source. |

## Actions Taken

No files modified (`fix_authorization: false`). Scoped tests green (39 passed). `contract.py` diff empty. `grep` for `t2_fallback`/`terminal_reason` in `contract.py`: no matches.

## Recommendations

1. Add a degraded-with-fallback-metadata test proving `t2_fallback.terminal_reason` is telemetry alongside, not instead of, `degraded-tier1`.
2. Extend populated fallback metadata verdict regression to assert reason equality.
3. Broaden the proxy leak assertion to catch lower-case key/url/value leak shapes while preserving `proxy_error` status telemetry.

## QA Complete
