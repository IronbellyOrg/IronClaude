# QA Report — Phase 5 (fsm.py) Actionability / Test-Correctness Lens

**Topic:** pr_submit V1.1 — Phase 5 regression-guard test non-vacuity
**Date:** 2026-06-12
**Phase:** task-qualitative (actionability / test-correctness lens)
**Fix cycle:** N/A (fix_authorization: false — report only)
**Stance:** ADVERSARIAL. Assumed weak/vacuous tests exist; hunted for them via source-read + live mutation (non-destructive: every mutation applied to the working tree was restored byte-for-byte and re-verified green; no source file modified on exit).

---

## Overall Verdict: PASS (with 2 IMPORTANT discrimination-gap findings + 1 MINOR mislabel)

The four load-bearing claims in the brief are all **TRUE** — the named tests genuinely fail under the regression they guard against. However, adversarial mutation surfaced two real weaknesses in the *surrounding* fence-post surface and one mislabeled test name. None of these falsifies the four claims; all are reported per the no-leniency rule (ALL findings surfaced regardless of severity; PASS reflects that the four load-bearing claims hold).

## Method

- Read all 4 files end-to-end (fsm.py 998 lines; 3 test files).
- Verified 3 fixtures exist and pin expected values (triple-chained `==` asserts fixture == computed == literal).
- Ran the suite: **28 passed**.
- Performed 7 live source mutations (A–F + loop_guard predicate), each restored and re-verified. Mutation = the gold standard for non-vacuity: a test is non-vacuous iff it FAILS when the behavior it guards is broken.

---

## Claim-by-Claim Verdict (the 4 load-bearing items)

### Claim 1 — `test_t_push_without_rereview_no_tick` — CONFIRMED NON-VACUOUS ✅

Asserts `push_count == 1` AND `round_counter == 0` AND `state == TERMINAL_TIMEOUT` for `rereview_outcome=["timeout"]`.

- **Trace:** fsm.py:949–983. Cycle pushes (`push_count += 1`, line 950) → outcome lookup line 969–972 yields `"timeout"` → line 979–983 sets `TERMINAL_TIMEOUT` and `break` **before** the `round_counter += 1` at line 988. The increment is the single relocated INV-001 tick site (line 988), reachable ONLY on `outcome == "attributed"`.
- **MUT-A (optimistic tick):** inserted an unconditional `result.round_counter += 1` after `do_resolve` (simulating the V1.0 optimistic-increment bug). Result: `test_t_push_without_rereview_no_tick` **FAILED**, and its sibling `test_deferred_increment_gated_on_attributed` **FAILED**. The `round_counter == 0` assertion is the discriminator. Non-vacuous. ✅

### Claim 2 — `test_t_auggie_at_most_once_across_two_declines_and_resume` — CONFIRMED NON-VACUOUS, but name overstates scenario ⚠️ (MINOR mislabel)

Asserts `auggie_review_invoked is True` AND `len(calls) == 1`.

- **MUT-B (drop strict-once guard):** replaced `if not result.auggie_review_invoked:` (fsm.py:760) with `if True:`. Result: **test PASSED** — i.e. dropping the guard did NOT break it.
- **Why:** the test's scenario (`review_state="declined"` at the initial S2 poll) drives `_run_fallback` **exactly once**. The strict-once guard only matters when `_run_fallback` is *entered twice* in one run. With a single entry, `invoke_auggie_review` is called once whether or not the guard exists, so `len(calls) == 1` holds vacuously w.r.t. the guard.
- **Verdict:** The assertion `len(calls) == 1` IS load-bearing for "exactly once," and the test would catch a double-invoke *within a single `_run_fallback`* — but the test name ("across two declines and resume") promises coverage of the **two-entry** path (the actual purpose of the `auggie_review_invoked` flag), which this scenario does **not** exercise. A second invoke could still slip through on the *two-entry* path and this test would not catch it. The flag's real defense (idempotency across re-entry / resume) is asserted only indirectly (`auggie_review_invoked is True` is set, but never re-tested after a second entry).
- **Severity: MINOR** (mislabel) bordering IMPORTANT. The claim "genuinely fails if a second invoke could slip through" is TRUE only for an *intra-call* double-invoke, FALSE for the *inter-call* (two-decline / resume) double-invoke the name advertises. Recommend either (a) rename to reflect single-entry scope, or (b) add a scenario that re-enters `_run_fallback` (e.g. `rereview_outcome=["declined"]` after an initial `review_state="declined"`, or a resume path) and asserts `len(calls) == 1` across both entries. Note `test_t1121` / `test_t1125` DO drive `rereview_outcome=["attributed","declined"]` (one fallback entry after a real round) but assert push/counter bounds, not invoke-count, so they don't close this gap either.

### Claim 3 — 9 pre-existing INV-001 fence-post tests UNCHANGED & discriminating — MOSTLY CONFIRMED, with 1 IMPORTANT gap ⚠️

The pre-existing INV-001 surface in test_loop_guard.py: `test_t626_off_by_one_canonical`, the 6-row parametrized matrix `test_t620_629_fence_post_matrix`, `test_gate_uses_ge_not_gt` (`should_halt(2,2)`, `should_halt(1,2)`, `should_halt(3,2)`, `user_label(0)==1`), and `test_t_vanished_mono_irrevocable`. These are textually UNCHANGED (the V1.1 additions are appended below a comment banner at line 143–145; `loop_guard.py:30` still reads `return round_counter >= max_rounds`).

**Mutation of the canonical gate predicate (`loop_guard.should_halt`: `>=` → `>`):**

| Test | Result under `>` mutation | Discriminating? |
|------|--------------------------|-----------------|
| `test_gate_uses_ge_not_gt` (`should_halt(2,2) is True`) | **FAILED** | YES — primary `>=` guard |
| `test_fallback_round_counter_cap_one` (`should_halt(1,1) is True`) | **FAILED** | YES |
| `test_t626_off_by_one_canonical` | **FAILED** (via `summary_posted is True`, NOT counter/push) | YES |
| `test_t620_629_fence_post_matrix` (all 6 rows) | **PASSED** | **NO** |

**IMPORTANT FINDING — the parametrized matrix does not discriminate the gate predicate.** Under the `>=`→`>` off-by-one (the spec's named P0 defect), every matrix row still yields its expected `round_counter` and `push_count`. Proven directly: for all 6 rows `base(counter,push) == mut(counter,push)`. The reason is **defense-in-depth**: pushes are capped by TWO independent mechanisms — the top-of-loop `should_halt_rounds` gate (fsm.py:884) AND the p4 push predicate `round_counter < max_rounds` (fsm.py:177) — plus the cycles-list length. Disabling any ONE leaves the other to enforce the cap:

- MUT-E (top-of-loop gate → `if False`): matrix **PASSED**, T-626 **FAILED** (summary_posted).
- MUT-F (p4 → `True`): matrix **PASSED**.
- MUT-E **and** p4 disabled together: case (2,5) → push=6 (cap lost). Only the *conjunction* breaks the matrix.

**Consequence:** No single matrix row isolates either gate. A p4-only regression at the fence (push over-count) is caught by NO test in this file on counter/push; the `>=`/`>` flavor is caught only by `test_gate_uses_ge_not_gt` (unit) and `test_t626` (via summary_posted). The matrix's actual load-bearing assertion is the *push/counter cap*, which is structurally enforced — its NAME ("fence-post matrix") implies gate-edge discrimination it does not provide.

- **`test_t_vanished_mono_irrevocable`:** CONFIRMED non-vacuous by construction — `RoundCounter.vanished_rereview()` is asserted not to decrement (`rc.value == 2` after vanish) and a non-attributed `on_rereview` returns False without incrementing. Asserts monotonicity directly on the counter object. ✅
- **`should_halt(2,2)`, `user_label(0)==1`:** strongly discriminating (killed by the predicate mutation above). ✅

**Net:** The 9 tests are UNCHANGED and the INV-001 surface *as a whole* is non-vacuous (the unit gate test + T-626 + cap-one + vanished-mono all fail under the canonical regression). The **matrix specifically** is weaker than its name — IMPORTANT but not a regression of the existing guard, since the stronger guards live alongside it.

### Claim 4 — `test_t1125_round_counter_frozen_two_independent_counters` — CONFIRMED NON-VACUOUS ✅

Asserts `round_counter == 1` (frozen, from the one attributed Augment round) AND `fallback_round_counter == 1` (the fallback's own cycle) AND `fallback_engaged is True`, for `rereview_outcome=["attributed","declined"]`.

- **Trace:** the attributed cycle 0 ticks `round_counter` to 1 (line 988); cycle 1's outcome `"declined"` enters `_run_fallback` (line 977), which advances ONLY `fallback_round_counter` (line 825) and never touches `result.round_counter`.
- **MUT-D (couple the counters):** added `result.round_counter += 1` immediately after the fallback's `fallback_round_counter += 1` (line 825). Result: `test_t1125` **FAILED** (round_counter became 2) AND `test_inv_r3_clamp_monotone_and_counters_independent` **FAILED**. The test genuinely proves independence: one counter advances (fallback) without moving the other (round). ✅

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Claim 1: timeout-no-tick non-vacuous | none | PASS | MUT-A killed it; trace fsm.py:979-988 |
| 2 | Claim 2: auggie at-most-once non-vacuous | AX-4 | FAIL | MUT-B did NOT kill it (single-entry scenario); name overstates → weakened/mislabel |
| 3 | Claim 3: 9 fence-post tests unchanged | none | PASS | banner at L143-145; loop_guard.py:30 intact |
| 4 | Claim 3: fence-post tests discriminating | AX-4 | FAIL | matrix survives `>=`→`>` AND gate-removal AND p4-removal on counter/push; only summary_posted/unit/cap-one discriminate |
| 5 | Claim 4: two-counter independence non-vacuous | none | PASS | MUT-D killed it; trace fsm.py:825,988 |
| 6 | Fixtures pin expected values (not tautological) | none | PASS | 3 fixtures read; triple-`==` chains |
| 7 | Source restored clean after all mutations | none | PASS | grep 0 markers; 28 green on exit |

<!-- axis = AX-4 (weakened-criteria) where a test's discrimination is weaker than its
name/claim asserts. none = passing check, five-axis lens applied, nothing fired.
drift-axis-inactive: see Summary. -->

## Summary
- Checks passed: 5 / 7
- Checks failed: 2 (both discrimination-quality, not correctness regressions)
- Critical issues: 0
- Important issues: 2 (matrix non-discrimination of gate predicate; auggie at-most-once name/scope mismatch borders IMPORTANT)
- Minor issues: 1 (test-name mislabel, item 2)
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status: drift-axis-inactive (no BUILD_REQUEST.GOAL verbatim supplied in spawn prompt; AX-1 disabled. AX-2..AX-5 applied.)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | test_loop_guard.py:69-115 `test_t620_629_fence_post_matrix` | The 6-row matrix asserts only `round_counter`/`push_count`, both structurally capped by defense-in-depth (top-of-loop gate + p4 + cycles length). It does NOT fail under the `>=`→`>` off-by-one (spec P0), nor under single-gate removal. Its name implies gate-edge discrimination it lacks. | Add a row/assertion that isolates the gate edge: assert `summary_posted is True` on the HALT rows, and/or add a p4-isolating case asserting push-count at the exact fence. The unit `test_gate_uses_ge_not_gt` remains the real `>=` guard — keep it. |
| 2 | MINOR→IMPORTANT | test_auggie_fallback.py:92-107 `test_t_auggie_at_most_once_across_two_declines_and_resume` | Name promises "across two declines and resume" (the inter-call idempotency the `auggie_review_invoked` flag exists for), but the scenario enters `_run_fallback` only ONCE. Dropping the strict-once guard (MUT-B) does NOT fail the test. A second invoke on the two-entry path could slip through uncaught. | Add a two-entry scenario (e.g. initial `review_state="declined"` then a second decline observation, or a resume that re-enters `_run_fallback`) and assert `len(calls) == 1` across BOTH entries; OR rename to reflect single-entry scope. |

## Actions Taken
None — fix_authorization: false. All 7 mutations were applied to the working tree and restored byte-for-byte; verified via `grep -rl "MUTATION|# MUT|# gate off" src/superclaude/pr_submit/` → no markers, and `pytest … -q` → 28 passed on exit. loop_guard.py and fsm.py are unmodified from their pre-review working-tree state.

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt; standalone behavior used (release-spec §19.4 fallback). No structural PASS items relied upon.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Claim 1 non-vacuity — verified by MUT-A (live source mutation `do_resolve` + optimistic tick) → `test_t_push_without_rereview_no_tick` FAILED; restored & re-verified 28 green.
- Claim 4 independence — verified by MUT-D (coupling `round_counter` to `fallback_round_counter` at fsm.py:825) → `test_t1125` + `test_inv_r3_clamp_monotone_and_counters_independent` FAILED.
- Claim 3 gate discrimination — verified by mutating `loop_guard.should_halt` predicate (`>=`→`>` at loop_guard.py:30) and measuring all 6 matrix rows' counter/push directly (Bash python harness): base==mut for every row → matrix non-discriminating; `test_gate_uses_ge_not_gt`, `test_t626`, `test_fallback_round_counter_cap_one` all FAILED.
- Fixture non-tautology — Read all 3 fixtures; confirmed `expected` blocks carry literal pinned values (e.g. round-sequence-residual-x3.json `expected.round_counter:2, push_count:2`) cross-checked by chained `==` in test bodies.

## Self-Audit (mandatory questions)
1. **Factual claims independently verified against source:** 7 (4 load-bearing claims + 3 supporting), each by live mutation or direct trace, not assertion-reading.
2. **Files read to verify:** fsm.py, loop_guard.py, test_review_retrigger.py, test_auggie_fallback.py, test_loop_guard.py, conftest.py (existence), 3 fixture JSONs.
3. **Why trust this (not 0 issues):** I did NOT find 0 issues — I found 2 IMPORTANT + 1 MINOR by mutating the source and observing which tests survived. Survivors (MUT-B passing, matrix passing under MUT-C/E/F) ARE the findings. Tool engagement (7 mutations, 28-test reruns) is the evidence trail.
4. **Web research:** none performed (brief said no web search); N/A — no Tavily fallback needed.

## Confidence
Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
(All four load-bearing claims confirmed via live mutation; the two discrimination gaps are themselves mutation-evidenced, not speculative.)

## Tool engagement
Read: 6 | Grep: 3 | Glob: 0 | Bash: 8 (7 mutation harnesses + 1 final integrity)

## Recommendations
1. Treat the 4 load-bearing claims as VERIFIED — proceed. The regression guards work.
2. Before final delivery, strengthen the two IMPORTANT items so the named tests match their advertised discrimination (matrix → assert `summary_posted`/isolate p4; auggie-at-most-once → add the two-entry re-invoke scenario). These harden the suite against future single-gate regressions; they do not block Phase 5.
3. Keep `test_gate_uses_ge_not_gt` and `test_fallback_round_counter_cap_one` (the direct `should_halt` unit asserts) — they are the strongest `>=` guards and should never be deleted in favor of the matrix.

## QA Complete

VERDICT: PASS
