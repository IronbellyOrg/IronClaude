# QA Report — INV-Fidelity Domain Lens (POST-COMPLETION, M3 final state)

**Topic:** sc:pr-submit v11 — INV-001 + INV-R1/R2/R3 fidelity after Phase-7 FR-9.5 classifier fix
**Date:** 2026-06-12
**Phase:** post-completion / report-validation (final-state re-verification)
**Fix authorization:** false (report only — nothing modified)
**Stance:** Adversarial. Assume ≥1 INV violation survived prior gates.

---

## Overall Verdict: PASS

No INV-001 violation found. INV-R1/R2/R3 still hold. The FR-9.5 classifier change is counter-free.
Adversarial probes (below) actively tried to break each invariant and failed to.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | EXACTLY ONE `[^_]round_counter += 1` in fsm.py | PASS | `grep -nE '[^_]round_counter \+= 1'` → single hit `fsm.py:1001`. No second site. |
| 2 | The one increment is the INV-001 attributed-rereview site | PASS | `fsm.py:998-1001`: fires only on `outcome == "attributed"`, AFTER push (`push_count += 1` at L955), BEFORE next-iter top-of-loop `should_halt_rounds` (L889). Monotonic, optimistic tick preserved. |
| 3 | `fallback_round_counter` is a SEPARATE counter (not round_counter) | PASS | `fsm.py:782` + `:828` increment `fallback_round_counter` only; matched by `[^_]`-excluded grep. Frozen `round_counter` confirmed by docstring L744-747 and absence of any round_counter mutation inside `_run_fallback` (L737-839). Two independent counters intact. |
| 4 | S5→S2 `rereview_attributed` edge byte-identical | PASS | `fsm.py:631-632` verbatim: `if edge == (MonitorState.S5_AWAITING_REREVIEW, "rereview_attributed"):` → `return MonitorState.S2_CLASSIFY  # loop-guard increments at this edge (INV-001)`. Comment + target unchanged. |
| 5 | HALT gate uses `>=` not `>` (INV-5) | PASS | `loop_guard.py:30` `return round_counter >= max_rounds`; docstring L24 + header L6-7 reaffirm `>=` not `>`. `fsm.py:135-142` `should_halt_rounds` delegates to it (single source, no drift). |
| 6 | FR-9.5 classifier change is counter-free | PASS | classifier.py grep for `round_counter|fallback_round_counter|push|clamp|effective_max` → **0** hits (case-insensitive). The FR-9.5 arbiter (`_is_attributed_review` L100-115 + `classify` L147-164) touches NO counter, push, or clamp. Pure review/decline arbitration only. |
| 7 | INV-R1 (rereview_request_count ≤ max_rounds) | PASS | Single increment site `fsm.py:970`, gated by `if result.applied_edits > 0` (L964) inside the per-cycle push path which is itself bounded by the round budget. run_log fold (`run_log.py:174` IDIOM A) is count-only monotone. No path increments it without a push. |
| 8 | INV-R2 (auggie review at-most-once / push ≤ max_rounds+1) | PASS | `fsm.py:763-765` strict-once guard `if not result.auggie_review_invoked:` sets flag immediately after invoke. run_log `auggie_review_invoked` set keyed on pr_number (`run_log.py:33`, IDIOM B add-to-set fold L181-182). Fallback contributes at most one push. |
| 9 | INV-R3 (effective_max_rounds clamp monotone non-increasing) | PASS | `fsm.py:760` `clamp_max_rounds(base)` = `min(effective, 1)` (L145-153), recorded once per fallback. run_log IDIOM C monotone-min fold (`run_log.py:190-194`): `min(prev, clamp)`, None seeds first clamp — a later higher value never raises it. One-way. |
| 10 | Two independent counters never re-open each other's loop | PASS | `round_counter` advances only at L1001 (main loop); `fallback_round_counter` only at L782/L828 (fallback). `_run_fallback` has NO loop-back to the main `for` loop (single-shot terminal selectors L834-839). Confirmed independent. |

---

## Adversarial Probes (attempted breaks)

- **Probe A — hidden second increment via classifier.** classifier.py has zero counter tokens (item 6). The FR-9.5 fix only changes which review state is *returned*; the increment remains exclusively at `fsm.py:1001`, fed downstream. No leak.
- **Probe B — FR-9.5 "review wins over decline" double-ticking.** When the attributed re-review wins (classifier returns clean/findings instead of declined), it flows back through the normal `S2_CLASSIFY` loop where the single L1001 tick applies once per attributed cycle — identical to the legacy path. A decline that loses does NOT enter `_run_fallback`, so `fallback_round_counter` is untouched. No double-count across the decline↔review boundary.
- **Probe C — clamp regression via re-entry.** `_run_fallback` is single-shot (no loop-back); even a hypothetical re-entry hits `min(prev, clamp)` which cannot raise the value. INV-R3 monotonicity holds.
- **Probe D — `>=`→`>` silent off-by-one.** Gate is the canonical `loop_guard.should_halt` (single source); `>=` confirmed at the only definition (L30). `fsm.py` does not re-implement the comparison.

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical (INV-001) issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None. No INV-001, INV-R1, INV-R2, or INV-R3 violation detected in the final state.

## Confidence

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 12 | Glob: 0 | Bash: 3
- All 10 checklist items VERIFIED with cited tool output (grep line hits + file:line reads). No web research performed (none required; all claims are local-source).

## QA Complete

VERDICT: PASS
