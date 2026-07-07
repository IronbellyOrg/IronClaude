# QA Report — G6 enum/numbers-consistency lens

**Target:** TASK-RF-t2-fallback-ladder-20260706-050832 change set
**Phase:** task-qualitative (Step 6.G6), report-only
**Date:** 2026-07-07

## Overall Verdict: PASS (enum/numeric consistency) — 2 MINOR test-coverage advisories

The "≥5 enum/numeric inconsistencies" hypothesis is NOT confirmed. Every enum token and numeric default matches its authoritative source (design §3/§6/§7). Zero token mismatches, zero off-by-one, zero invented/missing tokens.

## Items Reviewed (10/10 PASS)

| # | Check | Result |
|---|-------|--------|
| 1 | `TERMINAL_REASONS` = 8 tokens byte-identical to design §6 | PASS |
| 2 | `aborted_or_cancelled` deliberately ABSENT (documented) | PASS |
| 3 | `TIER2_CERTIFICATION_BASES` = 3 named tokens = design §6 | PASS |
| 4 | Ladder default `("T1Model01","T1Model02")` = §7.2; not overridden in `resolve_config` | PASS |
| 5 | `tier2_fallback_max_attempts` default = 2 = §7.2 | PASS |
| 6 | `reviewer_count` = CONTRIBUTING count (2), not attempt-ledger (4) | PASS |
| 7 | `build_fallback_metadata` validates BOTH enums (raises `ValueError`) — code present | PASS |
| 8 | `FALLBACK_ELIGIBLE_STATUSES`/`WorkerStatus` set consistency | PASS |
| 9 | `T1_MODEL_MAX_SLOTS`=9 ≥ ladder length; `t1_models` + `_collect_models` present | PASS |
| 10 | Fixture `pass_with_t2_fallback.yaml` internal enum/number consistency (by hand) | PASS |

## Issues Found

| # | Severity | Location | Issue | Fix decision |
|---|----------|----------|-------|--------------|
| G1 | MINOR | `tests/cli/reflect/fixtures/pass_with_t2_fallback.yaml` | Orphaned fixture — no test loads it (sibling `pass_no_t2_fallback.yaml` IS consumed). The positive-witness fixture's internal consistency is never machine-verified (verified by hand — correct). | FIX: add a `test_verdict_mapping.py` case loading it and asserting `derive_verdict(...).verdict is Verdict.PASS` (same reason as `pass.yaml`). (Dedup with conformance finding #1.) |
| G2 | MINOR | `fallback.py:111-116` guard / `test_contract_fallback_metadata.py` | The `ValueError` guard on unknown `terminal_reason`/`certification_basis` — the only thing preventing a typo'd enum token from entering a contract — has zero test coverage. | FIX: add two `pytest.raises(ValueError)` cases (`terminal_reason="not_a_real_reason"`, `certification_basis="bogus"`) asserting the message contains the offending token. |

## Recommendation

The enum/numbers lens is clean. Both advisories are non-blocking test-hardening (MINOR); G2 is the more worthwhile (it protects the enum-consistency guarantee this lens defends). Fold both into the final fix cycle.
