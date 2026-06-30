# Phase 5 — CONTENT Verification (adversarial, fix_authorization: false)

**Task:** TASK-RF-pr-submit-v11-20260612-013419 (pr_submit V1.1, highest-risk)
**Date:** 2026-06-12
**Agent:** Phase 5 CONTENT verifier — verify only, no modifications
**Method:** Every claim was confirmed by **mutation testing** (introduce the exact
defect the test claims to guard, confirm the named test fails, restore byte-clean).
Mutation is the only adversarial way to disprove vacuity; reading the assert is not.

Files read: `qa-fix-applied-phase5.md`, `test_auggie_fallback.py`,
`test_loop_guard.py`, `fsm.py` (+ `loop_guard.py`, `models.py` for guard internals).

Test surface (live, restored to baseline): **29 passed** across
`test_auggie_fallback.py` (9) + `test_review_retrigger.py` (7) + `test_loop_guard.py` (13).
No web search (per instruction).

---

## Overall Verdict: PASS

All four claims (a)-(d) confirmed NON-VACUOUS by mutation. Every test under review
fails when its guarded invariant is broken, and the four Phase-5 fixes did not weaken
any pre-existing INV-001 fence-post test. Restore was byte-clean (`diff` empty on both
`fsm.py` and `loop_guard.py`).

---

## (a) `test_t_auggie_at_most_once_across_two_declines_and_resume` — NON-VACUOUS cross-entry — CONFIRMED

The strengthened test (test_auggie_fallback.py:93-126) does three things:
1. First engagement via `run_skill` → asserts `len(calls) == 1`.
2. **Second `_run_fallback(result, config)` on the SAME `result`** → asserts `len(calls)
   STILL == 1` (the cross-entry strict-once assertion, line 118-120).
3. Fresh `SkillResult()` control → asserts `len(calls) == 2` and
   `fresh.auggie_review_invoked is True` (line 124-126).

**Mutation 1 — remove the strict-once guard** (`if not result.auggie_review_invoked:` →
unconditional invoke at fsm.py:763-765):
Result: `FAILED ... assert 2 == 1` at line 118. The test fails at the EXACT second-entry
assertion — proving the re-entry path genuinely exercises the
`if not result.auggie_review_invoked` guard. A removed guard double-invokes and is caught.

**Mutation 2 — never invoke** (`if False:` around the invoke block):
Result: `FAILED ... assert result.auggie_review_invoked is True` (first-engagement +
fresh-result both fail). This proves the recorder is NOT inert — the fresh-result control
(calls==2) and the first-engagement (calls==1) both genuinely depend on the guard firing.

Both directions of the guard (suppress-on-reentry AND invoke-on-fresh) are independently
pinned. The mechanism is sound: `_run_fallback` (fsm.py:762-765) re-runs the invoke block
on every entry, gated only by the `auggie_review_invoked` flag (default `False`, models.py:210);
the second call sees `result.auggie_review_invoked == True` from the first and suppresses.
**(a) CONFIRMED non-vacuous for cross-entry.**

---

## (b) `test_transition_v11_edges` — NON-VACUOUS — CONFIRMED

The test (test_auggie_fallback.py:231-261) asserts 10 `transition()` results covering the
6 V1.1 edges + the byte-identical INV-001 edge + the `fallback_skip` residual selector
(both branches) + the `needs_human` pre-gate short-circuit.

**Mutation 1 — break `RESOLVING/resolved` → S5a edge** (retarget to `S5_AWAITING_REREVIEW`,
skipping S5a):
Result: `FAILED — S5a_RETRIGGER_REVIEW != S5_AWAITING_REREVIEW` at line 235. Caught.

**Mutation 2 — invert the `fallback_skip` residual selector** (swap TERMINAL_CLEAN ↔
HALT_MAX_ROUNDS):
Result: `FAILED — TERMINAL_CLEAN != HALT_MAX_ROUNDS` at line 248-256. Caught — and this is
the load-bearing residual branch that the fix doc (F4) calls the "dual-surface" selector
agreeing with `_run_fallback`'s residual logic (fsm.py:834-838). Both branches discriminate.

Each asserted edge maps to a real `transition()` branch (fsm.py:622-654) and would fail if
that edge were wrong. **(b) CONFIRMED non-vacuous.**

---

## (c) The 9 pre-existing INV-001 fence-post tests — STILL UNCHANGED + discriminating — CONFIRMED

The 9 fence-post items in `test_loop_guard.py`: `test_t626_off_by_one_canonical` (1) +
`test_t620_629_fence_post_matrix` (6 parametrized rows) + `test_gate_uses_ge_not_gt` (1) +
`test_t_vanished_mono_irrevocable` (1) = 9.

**Untouched by the fix:** The Phase-5 fix table (qa-fix-applied-phase5.md:5-10) lists ONLY
`fsm.py` and `test_auggie_fallback.py` as modified. `test_loop_guard.py` is not in the fix
set; F6 explicitly states the `>=` gate matrix was "No change." Confirmed: the fix did not
edit this file.

**Still discriminating** (3 mutations against `loop_guard.py`):
- **`>=` → `>`** (the canonical off-by-one defect): `FAILED` × 3 —
  `test_t626_off_by_one_canonical`, `test_gate_uses_ge_not_gt`, `test_fallback_round_counter_cap_one`
  (`should_halt(1,1)` now False). The fence-post tests catch the exact P0 defect they exist for.
- **`vanished_rereview` decrements** (break INV-4 monotonicity): `FAILED` —
  `test_t_vanished_mono_irrevocable` (`assert 1 == 2`). Caught.
- **`on_rereview` increments without attribution**: `FAILED` —
  `test_t_vanished_mono_irrevocable` (`on_rereview(...,sha_attributed=False)` now True). Caught.

The fence-post matrix drives the `>=` gate end-to-end through `run_skill` (max_rounds=N ⇒
exactly N pushes, counter==N) and the gate mutation flips it. **(c) CONFIRMED — unchanged
and still discriminating.**

---

## (d) No new test vacuous/tautological — CONFIRMED

Every new/strengthened test was killed by a targeted mutation (above): the strict-once test
(2 mutations, both directions), the transition test (2 edge mutations). The `_ff()` helper
uses a distinct path (`src/app/db.py`) so fallback output is visibly attributable. The
fresh-result control in (a) proves the recorder is causal, not inert. The
`test_fallback_findings_pass_verify_before_remediate` (line 206) asserts an all-unverified
set produces `push_count == 0` — a real behavioral discriminator (verify-before-remediate,
not a tautology). No assertion observed that is true-by-construction independent of the SUT.
**(d) CONFIRMED — no vacuous/tautological new test.**

---

## Cross-checks on the fix doc's own claims
- **EXACTLY ONE `round_counter += 1`**: `grep -cE '[^_]round_counter \+= 1'` = **1**
  (the `[^_]` correctly excludes the two `fallback_round_counter += 1` sites). INV-001's
  single relocated increment (fsm.py:1001) is intact. Confirmed.
- **172 / +1 transition test**: the Phase-5 surface (the 3 files under review) = 29 passed;
  the +1 is `test_transition_v11_edges` (9 in test_auggie_fallback.py). Consistent.
- **Restore integrity**: `diff` of `fsm.py` and `loop_guard.py` vs pre-mutation backups =
  empty (FSM CLEAN / LOOPGUARD CLEAN). No residual mutation left in the tree.

## Self-Audit
- **Claims independently verified against source:** 4/4 (a-d) + 3 fix-doc cross-checks,
  all via executed mutation tests, not reading-only.
- **Files read:** fsm.py, loop_guard.py, models.py, test_auggie_fallback.py, test_loop_guard.py.
- **Tool engagement:** Read 4 | Grep/Bash mutation cycles 6 (each introduced a real defect
  and observed the named test fail, then restored). Tool calls ≥ claims verified.
- **Why trust this:** Every PASS is backed by a FAILING mutation run with the exact assertion
  line and message quoted — not "the assert looks fine." If any test were vacuous, its
  corresponding mutation would have stayed green; none did.

VERDICT: PASS
