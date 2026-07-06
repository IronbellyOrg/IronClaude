# FX7 cli/reflect suite summary (Step 3.5)

**Command:** `uv run pytest tests/cli/reflect/ -v`
**Overall:** 173 passed, 1 xpassed, 0 failed. EXIT 0.

| Metric | Count |
|--------|-------|
| Passed | 173 |
| xpassed | 1 (pre-existing xfail-now-passing, unrelated to FX7) |
| Failed | 0 |

## Preserved clean-run routing (the R2-F2 / FR-RH2.9 witnesses) — ALL STILL PASS
- `test_r2f2_build_reflect_contract_emits_honest_verification_fields` — PASSED (exempt `tool-unavailable` skip reason UNCHANGED).
- `test_i1_positive_witness_real_fanout` — PASSED (clean full-reviewer PASS/exit-0 preserved).
- `test_i3_partial_two_of_three_distinct_pass_eligible` — PASSED (FR-RH2.9: 2-of-3 shortfall stays PASS-eligible despite the new benign `reviewer-shortfall` token).
- `test_verification_skip_exemption_not_degraded` — PASSED (exemption behavior preserved).

## New FX7 tests — all green
- `test_fx7_reviewer_shortfall_populates_visible_token_and_unverified_flag`
- `test_fx7_emits_verification_visibility_fields_with_none_guard`
- `test_fx7_clean_run_preserves_exempt_skip_reason_and_empty_degraded`
- `test_fx7_reviewer_shortfall_token_does_not_over_degrade` (additive-safety witness — FR-RH2.9 preserved)
- `test_fx7_vacuous_no_verify_stays_exempt_but_visible`
- `test_fx7_writeback_includes_verified_visibility_keys`

## Additivity confirmed
Zero pre-existing cli/reflect test regressed. The FX7 change is strictly additive:
- New `reviewers_requested` kwarg (defaulted None) + `*_verified` visibility fields + a benign
  `reviewer-shortfall` token that does NOT flip any verdict.
- `_VERIFICATION_SKIP_EXEMPTIONS` and `_DEGRADED_COMPONENTS_HALT_SET` BYTE-UNCHANGED; `status` never set to
  "degraded"; `deviation_count_by_class.regression` never given a non-int; clean-run skip reason unchanged.
- The two aggressive verdict-DEGRADE routings (degrade-on-unverified, degrade-on-reviewer-shortfall) are
  deferred as needs_human_decision PENDINGs, NOT applied (would reverse R2-F2 / FR-RH2.9 and break test_r2f2/test_i1/test_i3).
