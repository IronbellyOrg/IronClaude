# QA Report — INV-fidelity Domain Lens (Phase 5: fsm.py)

**Topic:** pr_submit V1.1 — INV-001 verbatim preservation + INV-R1/R2/R3 arithmetic
**Date:** 2026-06-12
**Phase:** task-integrity (domain lens — INV fidelity)
**Stance:** ADVERSARIAL (fix_authorization: false — report only)
**Files traced:**
- `src/superclaude/pr_submit/fsm.py`
- `src/superclaude/pr_submit/loop_guard.py` (gate + tick delegation)
- `src/superclaude/pr_submit/models.py` (counter field defaults)
- `src/superclaude/pr_submit/run_log.py:140-189` (replay fold — adversarial cross-check)
- `tests/pr_submit/test_loop_guard.py`
- Task file Normative Invariants §, lines 164-200

---

## Overall Verdict: PASS

All four invariant clusters trace correctly against the ACTUAL code with worked
examples, and execution confirms (42 inv/loop_guard/p0 tests pass; 171/171 full
suite green). The adversarial probe surfaced ONE legitimate cross-cutting
OBSERVATION (run-log replay fold) that is architecturally intended and NOT a
Phase-5 INV violation — documented below for traceability.

---

## (a) INV-001 — PRESERVED VERBATIM

### (a1) The attributed-rereview edge is byte-identical
`fsm.py:631-632`:
```
if edge == (MonitorState.S5_AWAITING_REREVIEW, "rereview_attributed"):
    return MonitorState.S2_CLASSIFY  # loop-guard increments at this edge (INV-001)
```
The edge `(S5_AWAITING_REREVIEW, "rereview_attributed") → S2_CLASSIFY` is present
verbatim. VERIFIED.

### (a2) The `>=` HALT gate is unchanged
- `loop_guard.py:30`: `return round_counter >= max_rounds` (`>=`, not `>`).
- `fsm.py:142`: `should_halt_rounds` delegates to `loop_guard_should_halt` — SINGLE
  source for the gate, no drift between in-FSM check and the module.
- `test_loop_guard.py:118-123` (`test_gate_uses_ge_not_gt`) asserts `should_halt(2,2)
  is True`, `should_halt(1,2) is False`. PASSES. VERIFIED.

### (a3) EXACTLY ONE monotone `round_counter += 1` site
`grep "round_counter += 1"` over `fsm.py` returns exactly THREE hits:
- `fsm.py:779` → `fallback_round_counter += 1` (SEPARATE counter)
- `fsm.py:825` → `fallback_round_counter += 1` (SEPARATE counter)
- `fsm.py:988` → `result.round_counter += 1` (the ONE INV-001 site)

Only `fsm.py:988` touches `round_counter`. No decrement anywhere (monotone).
VERIFIED.

### (a4) Worked N=2 trace — `max_rounds=2 ⇒ exactly 2 pushes`, ordering correct
Inputs: `max_rounds=2`, `findings=[f1]`, `rereview_findings=[[f2],[f3]]`,
`rereview_outcome=[]` (empty ⇒ every cycle defaults `"attributed"`, fsm.py:972).
`cycles = [[f1],[f2],[f3]]` (3 cycles).

| cycle_index | top gate `should_halt(rc,2)` (fsm.py:884) | push (950) | p4=`rc<2` (177) | tick (988) | rc after |
|---|---|---|---|---|---|
| 0 | `0>=2`=False → open | push_count→1 | `0<2`=T | +1 | **1** |
| 1 | `1>=2`=False → open | push_count→2 | `1<2`=T | +1 | **2** |
| 2 | `2>=2`=**True** → HALT_MAX_ROUNDS, summary, break | — | — | — | 2 |

Result: `round_counter==2` (NOT 3), `push_count==2`, `state==HALT_MAX_ROUNDS`,
`summary_posted==True`.

**Ordering confirmed:** the tick (line 988) fires AFTER the push (line 950) →
monotonicity; and BEFORE the next iteration's top-of-loop `should_halt_rounds`
(line 884) → `max_rounds=N ⇒ N pushes` preserved. The tick is also gated on
`outcome == "attributed"` (lines 974/979 return early for declined/timeout BEFORE
988), so an optimistic over-tick is impossible.

Matches `test_t626_off_by_one_canonical` (asserts rc==2, pushes==2,
HALT_MAX_ROUNDS, summary) and the full fence-post matrix
`test_t620_629_fence_post_matrix` (max_rounds∈{1,2,3,5} ⇒ pushes==max_rounds).
ALL PASS. VERIFIED.

**INV-001 cluster: PASS (verbatim preserved).**

---

## (b) INV-R1 — re-trigger boundedness

- **Increment site & guard:** `fsm.py:959-961` —
  `if result.applied_edits > 0: config.do_retrigger(...); result.rereview_request_count += 1`.
  Monotone (only `+= 1`), emitted at most once per pushed cycle, gated on
  `applied_edits > 0`. VERIFIED.
- **Does NOT tick `round_counter`:** line 961 mutates `rereview_request_count`; the
  `round_counter` tick is the distinct line 988. No coupling. VERIFIED.
- **Bound `rereview_request_count <= max_rounds`:** the retrigger is reached only on
  the authorized-push path; a push requires p4 (`round_counter < max_rounds`,
  fsm.py:177) and is followed by an attributed tick advancing `round_counter`.
  Therefore #pushes ≤ max_rounds ⇒ #retriggers ≤ max_rounds. In the N=2 trace it
  reached exactly 2. `test_inv_r1_..._monotone_and_bounded` (lines 176-187) asserts
  `<= 2` AND `== push_count`. PASS.
- **Timeout sub-case (no over-count):** `rereview_outcome=["timeout"]`, max_rounds=2 →
  cycle 0 pushes, retrigger→1, outcome "timeout" → TERMINAL_TIMEOUT break;
  count=1 ≤ 2. `test_deferred_increment_gated_on_attributed` (lines 149-172) confirms
  push_count==1, round_counter==0 (push without attributed re-review does NOT tick).
  VERIFIED.

**INV-R1: PASS.**

---

## (c) INV-R2 — auggie strict-once + total-push bound

- **`/sc:auggie-review` at-most-once:** `fsm.py:760-762` in `_run_fallback`:
  `if not result.auggie_review_invoked: config.invoke_auggie_review(...);
  result.auggie_review_invoked = True`. Flag-guarded strict-once. VERIFIED.
- **`_run_fallback` runs at most once:** called at exactly two sites — `fsm.py:875`
  (initial `review_state=="declined"`, followed by `return` at 876) and `fsm.py:977`
  (per-cycle `outcome=="declined"`, followed by `break` at 978). Both terminate the
  run; there is NO loop-back into the main cycle loop after fallback. So the fallback
  (and its single `config.do_push`, line 820) executes at most once. VERIFIED.
- **Worked worst case `push_count <= max_rounds + 1` (N=2):** inputs
  `rereview_outcome=["attributed","declined"]`, max_rounds=2, fallback_findings=[f9]:
  - cycle 0: push (count→1), p4=`0<2`=T, attributed → rc→1.
  - cycle 1: top gate `1>=2`=False, push (count→2), p4=`1<2`=T, outcome "declined"
    → `_run_fallback`, break.
  - fallback: clamp `effective_max_rounds=min(2,1)=1`; auggie invoked once; fallback
    gate `should_halt(0,1)`=False; p4=`fallback_round_counter(0) < 1`=T → fallback
    push (count→**3**), fallback_round_counter→1.
  - Final `push_count==3 == max_rounds(2)+1`. Bound HOLDS at equality (tightest case).
  `test_fallback_round_counter_cap_one` (lines 213-227) confirms the fallback never
  runs >1 remediation cycle. VERIFIED.

**INV-R2: PASS.**

---

## (d) INV-R3 — clamp monotonicity + counter independence + round_counter frozen

- **Monotone non-increasing clamp:** `fsm.py:752-757` —
  `base = result.effective_max_rounds if not None else config.max_rounds;
  result.effective_max_rounds = clamp_max_rounds(base)`, and
  `clamp_max_rounds(effective, hard=1) = min(effective, hard)` (fsm.py:145-153).
  One-way: `min(.,1)`. `_run_fallback` runs once (see c), recorded once. Even on a
  hypothetical re-entry, `base = prior effective (≤1)` ⇒ `min(≤1,1)` never raises.
  Non-increasing. VERIFIED.
- **Two counters INDEPENDENT, `round_counter` FROZEN during fallback:** grep confirms
  `_run_fallback` (lines 737-834) writes ONLY `fallback_round_counter` (lines 779,
  825) and the fallback G-push uses `round_counter=result.fallback_round_counter`
  (line 806) against `effective_max_rounds` (line 807) — never the frozen
  `round_counter`. No `round_counter` write exists anywhere inside `_run_fallback`.
  Neither counter re-opens the other's loop. VERIFIED.
- **Worked trace:** `test_inv_r3_clamp_monotone_and_counters_independent`
  (lines 191-209), max_rounds=5, one attributed cycle then declined → asserts
  `round_counter==1` (advanced once on the Augment round then FROZE),
  `fallback_round_counter==1`, `effective_max_rounds==1` (monotone clamp 5→1). PASS.

**INV-R3: PASS.**

---

## Adversarial Probe — Observations (NOT Phase-5 violations)

The adversarial mandate ("assume ≥1 INV violation exists") drove a hunt for a
second logical increment site and for replay/live divergence. One item surfaced:

- **OBS-1 (run-log replay fold, NOT a violation).** `run_log.py:173`
  `state["round_counter"] += 1` is a SECOND textual `round_counter` increment. On
  inspection it is the JSONL REPLAY fold in `rebuild_state()` — it counts
  `EventType.ROUND_INCREMENTED` events to RECONSTRUCT the counter from the event
  stream, not a live FSM transition. It is a faithful 1-event⇒+1 fold mirroring the
  single live site (fsm.py:988), so it does NOT add a second FSM increment edge and
  does NOT violate INV-001's "and nowhere else" (which scopes FSM transitions). This
  is the intended NFR-6 split (core records decisions; run-log replays events).
  **Out of Phase-5 scope** (fsm.py owns the live tick; run_log owns the replay).

- **OBS-2 (seam boundary, informational).** The live tick at `fsm.py:988` does not
  itself emit a `ROUND_INCREMENTED` run-log event — that emission is the
  SKILL/run-log-writer layer's job (NFR-6 core purity; fsm.py is recording-only via
  seams). The replay fold (OBS-1) therefore depends on a `ROUND_INCREMENTED` event
  being written outside fsm.py. This is the intended Phase-boundary seam, not a
  Phase-5 fsm.py defect. Flagged only so the Phase-6/7 layer that emits run-log
  events keeps the live-tick ↔ event-emission pairing 1:1.

Neither observation is an INV violation in the Phase-5 surface under review.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a1 | INV-001 edge byte-identical | PASS | fsm.py:631-632 verbatim |
| a2 | `>=` HALT gate unchanged, single source | PASS | loop_guard.py:30, fsm.py:142; test L118-123 |
| a3 | EXACTLY ONE `round_counter += 1` | PASS | grep ⇒ only fsm.py:988 (779/825 are fallback) |
| a4 | N=2 worked trace: 2 pushes, tick after push/before gate | PASS | traced; test_t626 + matrix pass |
| b | INV-R1 monotone, `<=max_rounds`, no rc tick | PASS | fsm.py:959-961; test L176-187, L149-172 |
| c1 | auggie at-most-once | PASS | fsm.py:760-762 flag guard |
| c2 | `push_count <= max_rounds+1` worst case | PASS | traced ⇒ 3 = 2+1; fallback single-call (L820) |
| d1 | clamp monotone non-increasing | PASS | fsm.py:145-153, 752-757 |
| d2 | counters independent, rc frozen in fallback | PASS | grep: no rc write in _run_fallback; test L191-209 |

## Summary
- Checks passed: 9 / 9
- Checks failed: 0
- CRITICAL issues (INV-001 verbatim): 0
- Observations (non-violations, out-of-scope): 2 (OBS-1 run-log fold, OBS-2 seam)

## Confidence
Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 4 | Grep: 3 | Glob: 0 | Bash: 4 (incl. 3 pytest executions confirming the traces)

## QA Complete

VERDICT: PASS
