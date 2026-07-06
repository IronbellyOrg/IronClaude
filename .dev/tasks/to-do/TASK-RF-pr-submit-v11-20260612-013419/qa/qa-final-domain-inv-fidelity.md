# QA Report — INV-Fidelity Domain Lens (FINAL-PHASE M3)

**Topic:** pr_submit V1.1 — INV-001 verbatim + INV-R1/R2/R3 end-to-end
**Date:** 2026-06-12
**Phase:** report-validation (domain lens, FINAL-PHASE M3 gate)
**Fix authorization:** false (report only — nothing modified)
**Stance:** Adversarial. Traced arithmetic; did not accept claims.

---

## Overall Verdict: PASS

All four invariants verified by READING the source and TRACING the arithmetic
(not by reading docstrings). No INV-001 finding (would be CRITICAL). No INV-R1/R2/R3
violation. Two MINOR observations recorded below; neither breaks an invariant.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | INV-001: exactly one `round_counter += 1` | PASS | `grep -nE '[^_]round_counter \+= 1' fsm.py` → **1 match** (line 1001). Unfiltered grep → 2 matches (782 `fallback_round_counter`, 1001 `round_counter`); the `_` boundary in the regex correctly excludes the fallback counter. EXACTLY ONE. |
| 2 | INV-001: S5→S2 `rereview_attributed` edge byte-identical | PASS | fsm.py:631-632 `if edge == (MonitorState.S5_AWAITING_REREVIEW, "rereview_attributed"): return MonitorState.S2_CLASSIFY  # loop-guard increments at this edge (INV-001)`. Single edge; comment intact. |
| 3 | INV-001: `>=` gate via loop_guard, unchanged | PASS | loop_guard.py:30 `return round_counter >= max_rounds`. fsm.py:142 `should_halt_rounds` delegates to `loop_guard_should_halt` (single source, no drift). test_loop_guard.py:118-123 asserts `should_halt(2,2) is True`, `should_halt(1,2) is False`. |
| 4 | INV-001: `max_rounds=N ⇒ N pushes` (N=2 traced) | PASS | Worked trace below → push_count=2, round_counter=2 at HALT_MAX_ROUNDS. Matches test_t626_off_by_one_canonical (lines 52-58) and fence-post matrix (lines 69-114). |
| 5 | INV-001: increment placement (after push, before next gate) | PASS | push at fsm.py:955; `round_counter += 1` at 1001 (AFTER push → monotone); next-iter `should_halt_rounds` at 889 (top of loop, AFTER increment). Ordering preserves N⇒N. |
| 6 | INV-R1: `rereview_request_count <= max_rounds`, monotone | PASS | Single increment site fsm.py:970 (`+= 1`, never decrements → monotone). Gated by `if result.applied_edits > 0` (964). One tick per main-loop push; main-loop pushes ≤ max_rounds ⇒ bound holds. test:176-187 asserts `<= 2` and `== push_count`. |
| 7 | INV-R1: re-trigger does NOT tick round_counter | PASS | S5a re-trigger (`do_retrigger` 969 + count 970) is decoupled from `round_counter += 1` (1001), which is gated separately on `outcome == "attributed"` (982-985, 998-1001). Re-trigger fires; round tick only on attribution. |
| 8 | INV-R2: `/sc:auggie-review` at-most-once | PASS | `auggie_review_invoked` flag guard fsm.py:763-765. `_run_fallback` itself called at ≤1 site per run: 880 (review_state=="declined", followed by `return` 881 → main loop skipped) XOR 990 (outcome=="declined", followed by `break` 991). Mutually exclusive. Flag is belt-and-suspenders. |
| 9 | INV-R2: `push_count <= max_rounds + 1` (worst case traced) | PASS | Main-loop pushes ≤ max_rounds (gate `>=` halts at counter==max_rounds; timeout/decline break immediately). Fallback adds ≤1 push (cap-1, see #11). Worst case = max_rounds + 1. R3-test trace: max_rounds=5, push_count=3 ≤ 6. |
| 10 | INV-R3: clamp monotone non-increasing | PASS | Two surfaces, both non-increasing: `clamp_max_rounds` fsm.py:153 `min(effective, hard=1)`; run_log monotone-min fold run_log.py:190-194 `clamp if prev is None else min(prev, clamp)` (None-seed; later higher value never raises). |
| 11 | INV-R3: fallback cap-1 (structural, not just budget) | PASS | `_run_fallback` 768-772: `loop_guard_should_halt(fallback_round_counter, effective_max_rounds=1)`; `should_halt(1,1) is True` (test:217). Single re-entry, NO loop-back, NO second invoke/re-trigger. |
| 12 | INV-R3: round_counter & fallback_round_counter independent | PASS | `round_counter += 1` only at 1001 (main loop). `fallback_round_counter += 1` only at 782 & 828 (both inside `_run_fallback`). Neither path mutates the other. test:191-209 confirms round=1, fallback=1, effective=1. |
| 13 | run_log folds back the right EventType enums (not dead code) | PASS | `grep` models.py: ROUND_INCREMENTED(50), PUSH_COMPLETED(62), REREVIEW_REQUESTED(76), AUGGIE_FALLBACK_INVOKED(78), MAX_ROUNDS_CLAMPED(79) all exist. Folds at run_log.py:172,174,181,186,195 are live. |
| 14 | run_log round_counter fold matches FSM single-tick | PASS | run_log.py:172-173 `if et == ROUND_INCREMENTED.value: state["round_counter"] += 1` — pure count fold; one ROUND_INCREMENTED per attributed cycle mirrors the one in-memory tick. No divergence. |

---

## Worked Examples

### INV-001 — `max_rounds=2 ⇒ exactly 2 pushes` (N=2)

`_run(max_rounds=2, residual_cycles=2)` → `cycles = [[f(1)], [f(100)], [f(101)]]` (3 cycles).
`rereview_outcome` empty ⇒ every cycle defaults to `"attributed"` (fsm.py:985).

| cycle_index | top `should_halt(rc, 2)` | push? | push_count | outcome | `round_counter += 1`? | rc after | next |
|---|---|---|---|---|---|---|---|
| 0 | `should_halt(0,2)=False` | yes (955) | 1 | attributed | yes (1001) | 1 | 0+1=1 < 3 → loop |
| 1 | `should_halt(1,2)=False` | yes | 2 | attributed | yes | 2 | 1+1=2 < 3 → loop |
| 2 | `should_halt(2,2)=True` (889) | — | 2 | — | — | 2 | HALT_MAX_ROUNDS (890), summary_posted=True, break |

**Result:** `push_count == 2`, `round_counter == 2`, `state == HALT_MAX_ROUNDS`.
The `>=` gate fires AT counter==2 (loop_guard.py:30) so the 3rd fix cycle never opens
— the canonical off-by-one is correct (counter 2, NOT 3). Matches asserts at
test_loop_guard.py:55-57.

### INV-R3 / R1 / R2 — attributed-then-declined (max_rounds=5)

`RunConfig(monitor_ordinal=3, max_rounds=5, findings=[f(1)], rereview_findings=[[f(2)]],
rereview_outcome=["attributed","declined"], fallback_findings=[f(9)])` → cycles=[[f(1)],[f(2)]].

| cycle_index | push_count | outcome | round_counter | action |
|---|---|---|---|---|
| 0 | 1 | attributed | 0→1 | loop (1<2) |
| 1 | 2 | declined | 1 (frozen) | `_run_fallback` (990) → break |

Inside `_run_fallback`: base=`effective_max_rounds(None)`→`config.max_rounds=5`;
`clamp_max_rounds(5)=min(5,1)=1` → `effective_max_rounds=1` (INV-R3 5→1).
`auggie_review_invoked` False → invoke once → True (INV-R2).
`loop_guard_should_halt(0,1)=False` → proceed. verify f(9) → verified. gate_edit(3)=True.
push_decision: `round_counter=fallback_round_counter=0 < max_rounds=1` (p4 True) → authorized.
do_push → push_count=3. `fallback_round_counter += 1` → 1 (828). No residual → TERMINAL_CLEAN.

**Result:** `round_counter==1` (INV-R3 independence: main froze), `fallback_round_counter==1`
(INV-R3 cap-1), `effective_max_rounds==1` (INV-R3 monotone clamp), `push_count==3 <= 5+1`
(INV-R2). Matches test_loop_guard.py:206-209 asserts. **No counter bleed.**

### INV-R2 — `push_count <= max_rounds + 1` bound

- Main loop: each push (955) ⇒ either an attributed tick (rc advances toward the `>=`
  gate, ≤ max_rounds pushes) OR a timeout/decline that breaks the loop. Either way
  main-loop pushes ≤ max_rounds.
- Fallback: ≤1 push (cap-1, structural — `_run_fallback` runs once per run, single
  re-entry, no loop-back).
- **Worst case** = max_rounds (main) + 1 (fallback) = `max_rounds + 1`. Bound holds.

---

## Summary

- Checks passed: 14 / 14
- Checks failed: 0
- Critical issues: 0 (no INV-001 finding)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | fsm.py:178-179, 186 | INV-016 predicate-5 stored as the raw int `applied_edits` (`p5 = applied_edits`; `predicate_5_applied_edits=p5`) rather than a bool, while p1–p4 are bools. `authorized` correctly uses `p5 > 0`, and `push_fail_state` uses `<= 0`, so behavior is correct — but the field type is inconsistent with its sibling predicates. Not an INV violation. | (No action required for correctness; optionally normalize to `bool(p5 > 0)` for type symmetry. Out of INV-fidelity scope.) |
| 2 | MINOR | fsm.py:985 | The `"attributed"` default vs `"timeout"` default for a NON-EMPTY-but-short `rereview_outcome` is correct per the docstring (976-981), but the optimistic-vs-explicit branch (`"attributed" if not config.rereview_outcome else "timeout"`) is subtle. Verified correct by trace (empty ⇒ N⇒N preserved; non-empty short ⇒ trailing timeout, no tick). Documenting as a fragility note, not a defect. | None. Behavior matches INV-001 and EC-18. |

## Actions Taken

None — `fix_authorization: false`. Report only.

## Recommendations

- INV-001 is preserved verbatim: the single relocated increment (fsm.py:1001), the
  `rereview_attributed` edge (631-632), the `>=` loop-guard gate, and `max_rounds=N ⇒
  N pushes` all hold. The two MINOR items are cosmetic/type-symmetry, not invariant
  violations, and are explicitly out of the INV-fidelity remit.
- No blocking findings. Green light from the INV-fidelity lens.

## Confidence

**Verified:** 14/14 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence: 100.0%**
**Tool engagement:** Read: 4 | Grep: 6 | Glob: 0 | Bash: 6 (grep-only, each mapped to a specific check)

No web research performed (external lookup not required; all claims are local-source-truth).

## QA Complete

VERDICT: PASS
