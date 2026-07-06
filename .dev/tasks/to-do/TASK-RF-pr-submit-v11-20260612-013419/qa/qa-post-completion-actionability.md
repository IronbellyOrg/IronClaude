# QA Report — task-qualitative (POST-COMPLETION actionability / test-correctness lens)

**Topic:** pr-submit V1.1 oversized-PR auggie-review fallback (FR-9 / FR-9.5 / FR-10)
**Date:** 2026-06-12
**Phase:** task-qualitative (final-state, post FR-9.5 fix: test_t1117 added + T-ID renames)
**Fix cycle:** N/A
**fix_authorization:** false — report only, nothing modified. Source tree left clean (`make`-style restore verified: 176 passed; loop_guard.py/classifier.py/fsm.py restored to their uncommitted post-completion state).

---

## Overall Verdict: FAIL

Not because tests are broken — all 176 pass and the headline late-added test (`test_t1117`) is genuinely non-vacuous — but because **two of the changed/late tests carry assertions that do not discriminate the behavior their names claim to guard**. Under POST-COMPLETION rules (any issue of any severity = FAIL), these must be surfaced.

## Method

Mutation-probe each late-added/changed test: surgically break the exact production logic the test names, run ONLY that test, confirm it fails. A test that still passes when its named logic is removed is vacuous/weak. All probes run via `uv run pytest` (bare `python3` gave stale-bytecode garbage — flagged and discarded). `__pycache__` cleared between every mutation.

## Items Reviewed
| # | Check (late/changed test) | axis | Result | Evidence (mutation → outcome) |
|---|---|---|---|---|
| 1 | `test_t1117_ec22_attributed_rereview_wins_over_decline` | none | PASS (non-vacuous) | Force `attributed_rereview=False` in classifier → t1117 FAILS (`declined != findings`). Force `attributed_rereview` over-broad (`or`) → t1117 FAILS (contrast "stays declined" sub-assert catches it). All 4 sub-clauses discriminate. |
| 2 | `test_t1121_clamp_to_one_on_fallback_engage` | none | PASS (non-vacuous) | `clamp_max_rounds` `min→max` → t1121 FAILS. Label matches body (asserts `effective_max_rounds==1` from `max_rounds=5`). No T-1121/T-1122 swap. |
| 3 | `test_t1122_total_push_bound_inv_r2` | AX-4 | **FAIL (weak assertion)** | Suppress the fallback push (`push_count += 1 → += 0`) → t1122 STILL PASSES. Bound `<=3` has slack; scenario already pushes 3, and the fallback's "AT MOST one push" claim is never pinned. Catches gross over-push (+5 → fails) but not the fallback's own ±1 contribution. |
| 4 | `test_t1116_fallback_findings_pass_verify_before_remediate` | AX-4 | **FAIL (redundantly pinned / weak)** | Remove the fallback's `verify` gate alone (`verified = list(fallback_findings)`) → t1116 STILL PASSES, because `_default_apply_edits` re-filters `verification_status != "unverified"` downstream and holds `push_count==0`. Only fails when BOTH gates are removed. The test cannot detect a regression isolated to FR-9.4 (the fallback-level verify the name claims). |
| 5 | `test_t1110_t1113b_decline_at_initial_poll_routes_to_fallback` (renamed) | none | PASS | Body asserts `fallback_engaged`, `decline_detected`, `round_counter==0` (frozen) — matches the T-1113b "initial-poll decline routes to fallback, no Augment round" name. |
| 6 | `test_t1114_auggie_at_most_once_across_two_declines_and_resume` (renamed) | none | PASS (non-vacuous) | Break strict-once guard (`if not result.auggie_review_invoked → if True`) → t1114 FAILS (recorder fires twice). Cross-entry (`_run_fallback` twice on same result) genuinely exercises the guard, not an inert recorder. |
| 7 | `test_t626_off_by_one_canonical` + `test_t620_629_fence_post_matrix` + `test_gate_uses_ge_not_gt` | none | PASS (non-vacuous) | `should_halt` `>=→>` → t626 FAILS + gate_uses_ge FAILS (`should_halt(2,2)` flips). The P0 fence-posts discriminate. |
| 8 | `test_deferred_increment_gated_on_attributed` (T-PUSH-WITHOUT-REREVIEW-NO-TICK) | none | PASS (non-vacuous) | Make `timeout` path tick `round_counter` → test FAILS. The "push without attributed re-review does NOT tick" guard is live. |
| 9 | `test_ec23_t1118_stale_pre_watermark_decline_ignored` | none | PASS (non-vacuous) | Disable watermark staleness check → t1118 FAILS. Discriminates EC-23. |
| 10 | `test_t1125_round_counter_frozen_two_independent_counters` | none | PASS | Asserts `round_counter==1` (frozen pre-fallback) + `fallback_round_counter==1` independently. Consistent with traced counters (3-push scenario: 2 main + 1 fallback). |

## Summary
- Checks passed: 8 / 10 (non-vacuous)
- Checks failed (weak/vacuous assertions): 2 — items 3 (T-1122) and 4 (T-1116)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization:false)
- Test suite: 176 passed on the clean post-completion tree.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | IMPORTANT | tests/pr_submit/test_auggie_fallback.py::test_t1116 (lines 209-225) | Asserts FR-9.4 (fallback findings re-enter verify-before-remediate) but `push_count==0` is actually held by the **downstream** `_default_apply_edits` `!= "unverified"` filter (fsm.py:686-688), not the fallback's own `verify` gate (fsm.py:779). Removing only the fallback verify gate leaves the test green — the named behavior is not pinned. | Add a direct assertion on the fallback verify boundary: inject a custom `apply_edits` seam that counts ALL `in_diff` findings (no verification re-filter), so the only thing standing between an unverified fallback finding and a push is the fallback's `verify`. Then `push_count==0` genuinely proves FR-9.4. (Confirmed: with that apply_edits seam, killing fallback verify → push_count=1, test fails as it should.) |
| 2 | MINOR | tests/pr_submit/test_auggie_fallback.py::test_t1122 (lines 191-206) | Name/docstring claim "single-shot fallback sub-loop contributes AT MOST one push." Assertion is only the upper bound `push_count <= max_rounds + 1` (3). Suppressing the fallback's `push_count += 1` (fsm.py:824) drops the count 3→2, still `<=3` → passes. The specific "fallback adds exactly one (and only one) push" is never observed. | Assert the fallback contribution exactly: in this 2-main-push + decline scenario, assert `push_count == 3` (equality), or split: assert main-loop pushes == 2 AND fallback pushed exactly once (e.g. via `fallback_round_counter==1` AND total `push_count == 3`). Equality at the boundary makes both an under-push and over-push detectable. |

## Actions Taken
None (fix_authorization:false). Source restored after every mutation; final `uv run pytest tests/pr_submit/ -q` = 176 passed; `git diff --stat` shows only the pre-existing uncommitted post-completion deltas in classifier.py (+110) and fsm.py (+212), loop_guard.py clean.

## Notes on the prompt's specific suspicions
- **test_t1117 (FR-9.5 arbiter):** NON-VACUOUS — confirmed fails when the arbiter is removed (item 1). The fix did its job.
- **Renamed T-1113b / T-1114 / T-1116:** T-1113b and T-1114 genuinely assert their named behavior (items 5, 6). **T-1116 does NOT** (item 4 / Issue 1) — the rename is fine but the assertion was always weak.
- **Swapped T-1121 / T-1122 labels:** NO SWAP. t1121 body = clamp (`effective_max_rounds==1`); t1122 body = push-bound. Both labels match their bodies. However t1122's bound is too loose (item 3 / Issue 2).
- **Regression guards:** T-PUSH-WITHOUT-REREVIEW-NO-TICK (item 8), T-AUGGIE-AT-MOST-ONCE (item 6), and the 9 INV-001 fence-posts (item 7) all still discriminate.

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt → standalone behavior (Critical Rule #11 fallback). Relied on the harness's "176 passed" only as a starting baseline, not as verification of discrimination.

**(b) Independent semantic checks (≥1 required, INV-019):**
- FR-9.5 arbiter discrimination — verified by mutating `attributed_rereview` to `False` and to over-broad `or` in classifier.py:157 and re-running t1117 (both FAIL). Tool: Bash `uv run pytest` + Edit-via-python mutation.
- FR-9.4 fallback verify boundary — verified by single-gate vs dual-gate mutation in fsm.py:779/686, proving t1116's pass is held by the redundant apply_edits filter (Issue 1). Tool: Bash mutation + pytest.
- INV-R2 fallback push contribution — verified by suppressing fsm.py:824 push increment and observing t1122 still green (Issue 2). Tool: Bash mutation + instrumented `uv run python` counter trace (push_count=3 boundary).
- INV-001 `>=` fence-post — verified `should_halt` `>=→>` flips t626 + gate_uses_ge (loop_guard.py:30). Tool: Bash mutation + pytest.

## Self-Audit numbers
- How many factual claims independently verified against source: 10 test/logic pairings, each via a targeted source mutation + isolated pytest run (8 confirmed-strong by induced failure, 2 confirmed-weak by induced NON-failure).
- Files read to verify: tests/pr_submit/test_detection_contract.py, test_auggie_fallback.py, test_loop_guard.py; src/superclaude/pr_submit/classifier.py, fsm.py, loop_guard.py, models.py; fixtures (decline-comment / stale-decline / auggie-fallback-findings).
- Why trust this found real issues: the two FAIL findings were each proven by a mutation that the test FAILED to catch, then cross-confirmed (Issue 1 by the dual-gate mutation that DID flip it).
- Web research: none performed (prompt: no web search). Tavily N/A.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Grep: 2 | Glob: 0 | Bash: 10

## QA Complete

VERDICT: FAIL
