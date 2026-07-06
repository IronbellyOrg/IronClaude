# QA Report — Dual-Surface Lock-Step (Phase 5, fsm.py)

**Topic:** pr_submit V1.1 — fsm.py `transition()` vs `run_skill()`/`_run_fallback()` lock-step
**Date:** 2026-06-12
**Phase:** task-integrity (dual-surface drift lens)
**Fix authorization:** false (report only)
**File under review:** `/config/workspace/IronClaude/src/superclaude/pr_submit/fsm.py`

---

## Overall Verdict: FAIL

The two surfaces AGREE on the critical `fallback_skip` terminal selector
(Edge 6, the explicitly-flagged concern). But they DRIFT on Edges 1, 2,
and 5 — the inline `run_skill()` loop does NOT reproduce the
`transition()` re-trigger/re-review/re-entry topology. Several of these
are intentional architectural differences, but at least two are genuine
behavioral drift that will diverge under real inputs. Per the
zero-tolerance + adversarial mandate, any unreconciled drift = FAIL.

---

## Edge-by-Edge: transition() ↔ run_skill()/_run_fallback()

### Edge 1 — RESOLVING/resolved → S5A_RETRIGGER_REVIEW ↔ run_skill posts re-trigger (do_retrigger) after resolve

- **transition():** `fsm.py:622-626` — `(RESOLVING, "resolved")` returns
  `S5A_RETRIGGER_REVIEW`. The state machine routes resolve → S5a
  (re-trigger) → THEN awaits re-review.
- **run_skill():** `fsm.py:953` `config.do_resolve(...)` → `fsm.py:959-961`
  `if result.applied_edits > 0: config.do_retrigger(...)` →
  `fsm.py:962` `result.state = MonitorState.S5_AWAITING_REREVIEW`.

**DRIFT-1 (IMPORTANT — intermediate state never materialized).**
`transition()` makes `S5A_RETRIGGER_REVIEW` a real intermediate state
between RESOLVING and S5_AWAITING_REREVIEW. `run_skill()` posts the
re-trigger (`do_retrigger`, `fsm.py:960`) but assigns
`result.state = S5_AWAITING_REREVIEW` directly (`fsm.py:962`) — the
`S5A_RETRIGGER_REVIEW` state is NEVER set on `result.state` anywhere in
`run_skill()` or `_run_fallback()`. A caller that asserts on the
observable state will see S5a from `transition()` but never from
`run_skill()`. The behavior (a re-trigger comment IS posted) agrees; the
**observable state** does not. This is exactly the dual-surface trap the
lens exists to catch: the flat table grew an S5a node, the inline loop
collapsed it.

**DRIFT-2 (IMPORTANT — guard predicate divergence).**
`transition()` Edge 1 is UNCONDITIONAL: any `(RESOLVING, "resolved")`
routes to S5a regardless of `applied_edits`. `run_skill()` gates the
re-trigger on `if result.applied_edits > 0:` (`fsm.py:959`). On the
inline surface, a resolve with `applied_edits == 0` would NOT post a
re-trigger; on the `transition()` surface the same resolve still routes
through S5a. In practice the inline loop only reaches `fsm.py:953`
(`do_resolve`) AFTER a `decision.authorized` push (predicate-5 requires
`applied_edits > 0`), so `applied_edits > 0` is already guaranteed and
the guard is dead-but-harmless here. Still a latent surface mismatch:
the guard belongs to neither the spec edge nor a reachable
counter-case, so it silently encodes an assumption the table does not.

### Edge 2 — S5A_RETRIGGER_REVIEW/retriggered → S5_AWAITING_REREVIEW

- **transition():** `fsm.py:627-630` — `(S5A_RETRIGGER_REVIEW,
  "retriggered")` returns `S5_AWAITING_REREVIEW`. Comment confirms the
  re-trigger does NOT tick `round_counter`.
- **run_skill():** collapsed into `fsm.py:960-962` (post `do_retrigger`,
  set `S5_AWAITING_REREVIEW`). No `round_counter` tick occurs at this
  point (`fsm.py:962` only sets state). The increment is relocated to
  `fsm.py:988` and fires only on `outcome == "attributed"`.

**AGREES on the load-bearing invariant** (re-trigger does not tick the
counter — INV-R1): neither surface increments `round_counter` between
resolve and the attributed re-review. The increment-site comment at
`fsm.py:985-988` is consistent with the `transition()` Edge 2/INV-001
note at `fsm.py:632`. The only delta is the same materialization gap as
DRIFT-1 (the S5a node is skipped as an observable state). No NEW drift
beyond DRIFT-1.

### Edge 3 — S5_AWAITING_REREVIEW/declined → S5B_AUGGIE_FALLBACK ↔ run_skill routes a declined S5 outcome into _run_fallback

- **transition():** `fsm.py:635-639` — `(S5_AWAITING_REREVIEW,
  "declined")` returns `S5B_AUGGIE_FALLBACK`.
- **run_skill():** `fsm.py:969-972` computes `outcome` for the cycle;
  `fsm.py:974-978` `if outcome == "declined": _run_fallback(result,
  config); break`. The decline at the post-push re-review poll routes
  into the fallback. `_run_fallback` sets `result.state` to a TERMINAL
  (TERMINAL_CLEAN / HALT_MAX_ROUNDS / VALIDATION_FAIL / etc.), NOT to the
  literal `S5B_AUGGIE_FALLBACK`.

**DRIFT-3 (MINOR — intermediate state never materialized, consistent
with DRIFT-1).** Same pattern: `transition()` exposes
`S5B_AUGGIE_FALLBACK` as an observable state; `_run_fallback`
(`fsm.py:737-834`) never assigns `result.state =
MonitorState.S5B_AUGGIE_FALLBACK` — it always lands on a terminal. The
**routing behavior** (declined-at-S5 → fallback) AGREES. The drift is
again the observable-state gap, not the control flow. Rated MINOR
because the fallback is a synchronous inline call whose intermediate
state is genuinely transient by design; but it is still a surface
disagreement a state-asserting test would catch.

### Edge 4 — S2_CLASSIFY/declined → S5B_AUGGIE_FALLBACK ↔ run_skill routes review_state=="declined" into _run_fallback

- **transition():** `fsm.py:640-642` — `(S2_CLASSIFY, "declined")`
  returns `S5B_AUGGIE_FALLBACK`.
- **run_skill():** `fsm.py:871-876` `if config.review_state ==
  "declined": _run_fallback(result, config); return result`. The INITIAL
  S2-poll decline routes into the fallback.

**AGREES on routing.** Both surfaces send an initial-poll decline into
the S5b fallback path. Same observable-state materialization caveat as
DRIFT-3 (the literal `S5B_AUGGIE_FALLBACK` is never set on
`result.state`), but the control-flow target is identical. No new drift
beyond the shared materialization gap.

### Edge 5 — S5B_AUGGIE_FALLBACK/fallback_findings → S2_CLASSIFY ↔ _run_fallback re-enters the pipeline once

- **transition():** `fsm.py:643-646` — `(S5B_AUGGIE_FALLBACK,
  "fallback_findings")` returns `S2_CLASSIFY`. The comment promises the
  fallback findings "re-enter classification ONCE under the clamp (no
  loop-back)".
- **_run_fallback():** `fsm.py:771-834`. The fallback loads
  `config.fallback_findings` (`fsm.py:772`), runs verify-before-remediate
  (`fsm.py:776`), and — when verified findings exist and the ceiling
  permits — applies edits / validates / pushes / replies / resolves
  INLINE (`fsm.py:794-825`). It then lands on a TERMINAL via the
  fallback_skip selector (`fsm.py:829-833`).

**DRIFT-4 (IMPORTANT — re-entry semantics diverge: state vs inline
remediation).** `transition()` Edge 5 models the fallback's productive
path as a re-entry to `S2_CLASSIFY` — i.e. the findings flow back through
the classify→verify→fix pipeline as a fresh classification pass.
`_run_fallback` does NOT route back to `S2_CLASSIFY`; instead it
RE-IMPLEMENTS the verify→diagnose→fix→validate→push→reply→resolve
sequence INLINE (`fsm.py:776-825`) and terminates directly. The
`transition()` `fallback_findings → S2_CLASSIFY` edge has NO counterpart
that sets `result.state = S2_CLASSIFY` inside `_run_fallback`. The two
surfaces describe the SAME intent ("remediate the fallback findings
once") via TWO DIFFERENT mechanisms (table: loop-back-to-classify;
inline: re-implement-the-pipeline). This is the most consequential
drift: a maintainer editing the classify/verify/fix logic in the main
loop (`fsm.py:907-953`) would NOT automatically update the duplicated
inline remediation in `_run_fallback` (`fsm.py:776-824`). The pipeline
is forked, not shared. Each step
(verify-before-remediate, the `ordinal >= 3 and needs_human_decision`
HALT_HUMAN guard, the `gate_edit` PROPOSED branch, the
evaluate_push_decision call) is HAND-COPIED into `_run_fallback` rather
than reached via the `S2_CLASSIFY` re-entry the table specifies. Compare
`fsm.py:784-786` (`_run_fallback` HALT_HUMAN) with `fsm.py:903-905`
(`run_skill` HALT_HUMAN), and `fsm.py:788-792` (`_run_fallback`
PROPOSED) with `fsm.py:914-919` (`run_skill` PROPOSED): these are
parallel hand-copies, the textbook dual-surface drift vector.

### Edge 6 — S5B_AUGGIE_FALLBACK/fallback_skip → TERMINAL_CLEAN | HALT_MAX_ROUNDS ↔ _run_fallback terminal selector

- **transition():** `fsm.py:647-654` — `(S5B_AUGGIE_FALLBACK,
  "fallback_skip")` returns `HALT_MAX_ROUNDS if
  ctx.get("fallback_residual_findings") else TERMINAL_CLEAN`.
- **_run_fallback():** `fsm.py:829-833` —
  `if config.fallback_residual_findings: ... result.state =
  HALT_MAX_ROUNDS; else: result.state = TERMINAL_CLEAN`.

**CRITICAL CHECK — AGREES.** This is the explicitly-flagged concern: the
table keys on `ctx.get("fallback_residual_findings")` and the inline
selector keys on `config.fallback_residual_findings`. Both are truthy
EXACTLY when a residual finding set is present:

- residual present → BOTH yield `HALT_MAX_ROUNDS`
  (`fsm.py:651` ↔ `fsm.py:830-831`).
- no residual → BOTH yield `TERMINAL_CLEAN`
  (`fsm.py:653` ↔ `fsm.py:833`).

The truthiness semantics match: `ctx.get("fallback_residual_findings")`
returns the list (truthy iff non-empty / falsy when absent-or-empty),
and `config.fallback_residual_findings` is a `list[Finding]` defaulting
to `field(default_factory=list)` (`fsm.py:719`), truthy iff non-empty.
Empty-list and missing-key both go to TERMINAL_CLEAN on both surfaces.
**The fallback_skip terminal selector AGREES on both surfaces.** This
specific concern PASSES.

There is ONE additional inline-only convergence terminal NOT modeled as
a `transition()` edge: `fsm.py:777-782` — when the fallback's
verify-before-remediate yields NO verified findings, `_run_fallback`
goes straight to `TERMINAL_CLEAN` (`fsm.py:780`). The table has no
`(S5B_AUGGIE_FALLBACK, <no-verified>)` edge; this "empty after verify →
clean" terminal exists only on the inline surface (see DRIFT-5).

---

## Additional Drift Found (beyond the 6 named edges)

**DRIFT-5 (MINOR — inline-only terminal with no table edge).**
`_run_fallback` has FOUR distinct exit terminals
(`HALT_MAX_ROUNDS` at `fsm.py:768`; `TERMINAL_CLEAN` at `fsm.py:780`;
`HALT_HUMAN` at `fsm.py:785`; `PROPOSED` at `fsm.py:789`;
`VALIDATION_FAIL` at `fsm.py:797`; plus the `push_fail_state` /
`S4_HALT_BEFORE_PUSH` branch at `fsm.py:811-816`; and the
residual/clean selector at `fsm.py:829-833`). `transition()` models the
S5b node with only TWO outgoing edges (`fallback_findings` → S2_CLASSIFY,
`fallback_skip` → terminal). The inline fallback can reach
`HALT_HUMAN`, `PROPOSED`, `VALIDATION_FAIL`, and `S4_HALT_BEFORE_PUSH`
from S5b — NONE of which have a corresponding `(S5B_AUGGIE_FALLBACK, *)`
edge in the table. The fallback's reachable-state set is STRICTLY LARGER
on the inline surface than the table admits. Rated MINOR because these
are all legitimate ceiling/validation HALTs reused from the main loop,
but they are a genuine surface-coverage gap: `transition()` does not
enumerate the fallback's full exit fan-out.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Edge 1 RESOLVING/resolved→S5a both surfaces | FAIL | `transition` fsm.py:622-626 unconditional; `run_skill` fsm.py:959-962 gates on applied_edits>0 and never sets S5a state (DRIFT-1, DRIFT-2) |
| 2 | Edge 2 S5a/retriggered→S5_AWAITING both surfaces | PASS* | `transition` fsm.py:627-630 ↔ `run_skill` fsm.py:960-962; INV-R1 no-tick agrees (fsm.py:962 vs 988). *S5a state not materialized (DRIFT-1) |
| 3 | Edge 3 S5/declined→S5b both surfaces | PASS* | `transition` fsm.py:635-639 ↔ `run_skill` fsm.py:974-978 routes to `_run_fallback`. *S5b state not materialized (DRIFT-3) |
| 4 | Edge 4 S2/declined→S5b both surfaces | PASS* | `transition` fsm.py:640-642 ↔ `run_skill` fsm.py:871-876 routes review_state=="declined" to `_run_fallback`. *S5b state not materialized |
| 5 | Edge 5 S5b/fallback_findings→S2_CLASSIFY ↔ re-enter once | FAIL | `transition` fsm.py:643-646 loops back to S2_CLASSIFY; `_run_fallback` fsm.py:776-825 re-implements pipeline INLINE, never sets S2_CLASSIFY (DRIFT-4, forked pipeline) |
| 6 | Edge 6 fallback_skip terminal selector AGREES | PASS | `transition` fsm.py:647-654 (`ctx.get`) ↔ `_run_fallback` fsm.py:829-833 (`config.`); residual→HALT_MAX_ROUNDS, none→TERMINAL_CLEAN on BOTH. CRITICAL concern resolved. |
| 7 | S5b exit fan-out coverage in table | FAIL | `_run_fallback` reaches HALT_HUMAN/PROPOSED/VALIDATION_FAIL/S4_HALT_BEFORE_PUSH (fsm.py:785,789,797,811-816) + empty-verify→TERMINAL_CLEAN (fsm.py:780); table models only 2 S5b edges (DRIFT-5) |

## Summary

- Checks passed: 4 / 7 (3 with materialization caveats)
- Checks failed: 3 (Edge 1, Edge 5, S5b fan-out coverage)
- Critical issues: 1 (DRIFT-4 — forked remediation pipeline, Edge 5)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix (advisory) |
|---|----------|----------|-------|------------------------|
| DRIFT-1 | IMPORTANT | fsm.py:962 vs 622-626 | `run_skill` never sets `result.state = S5A_RETRIGGER_REVIEW`; jumps straight to S5_AWAITING_REREVIEW. State-asserting tests will diverge from `transition()`. | Either set S5a as an observable intermediate state before S5_AWAITING_REREVIEW, or document the table's S5a node as a non-materialized routing-only edge. |
| DRIFT-2 | IMPORTANT | fsm.py:959 vs 622-626 | re-trigger gated on `applied_edits > 0` inline, but `transition()` Edge 1 is unconditional. Dead-but-harmless given predicate-5, encodes an untabled assumption. | Make the guard explicit in the table comment OR drop the guard (it is implied by the only reachable path). |
| DRIFT-3 | MINOR | fsm.py:737-834 vs 635-639 | `_run_fallback` never sets `result.state = S5B_AUGGIE_FALLBACK`; the S5b node is transient inline. | Document S5b as routing-only, or set it transiently for observability parity. |
| DRIFT-4 | CRITICAL | fsm.py:776-825 vs 643-646 | Edge 5 models fallback remediation as re-entry to S2_CLASSIFY; `_run_fallback` re-implements verify→fix→validate→push→reply→resolve INLINE. Pipeline is FORKED — main-loop edits won't propagate to the fallback copy. | Refactor the shared remediation into a single helper called by BOTH the main loop and `_run_fallback`, OR make `_run_fallback` actually re-enter via the same code path the table's S2_CLASSIFY edge implies. |
| DRIFT-5 | MINOR | fsm.py:780,785,789,797,811-816 vs 643-654 | `_run_fallback` exit terminals (HALT_HUMAN/PROPOSED/VALIDATION_FAIL/S4_HALT_BEFORE_PUSH/empty-verify→TERMINAL_CLEAN) have no `(S5B_AUGGIE_FALLBACK,*)` edges. Table under-models the fallback's reachable-state set. | Add table edges (or a documented note) enumerating the fallback's ceiling/validation HALT exits. |

## What AGREES (verified, not assumed)

- **Edge 6 fallback_skip terminal selector** — the CRITICAL flagged
  concern. `ctx.get("fallback_residual_findings")` (fsm.py:651-653) and
  `config.fallback_residual_findings` (fsm.py:829-833) have identical
  truthiness (both empty/missing → TERMINAL_CLEAN; both non-empty →
  HALT_MAX_ROUNDS). `config.fallback_residual_findings` defaults to an
  empty list (fsm.py:719), matching `ctx.get(...)` returning
  None/empty. PASS.
- **INV-R1 (re-trigger does not tick round_counter)** — neither surface
  increments between resolve and attributed re-review (fsm.py:962 sets
  state only; the single increment is at fsm.py:988 under
  outcome=="attributed").
- **Decline routing (Edges 3 & 4)** — both initial-S2 (fsm.py:871-876)
  and post-push-S5 (fsm.py:974-978) declines route into `_run_fallback`,
  matching the table's two S5b-entry edges (fsm.py:635-642).

## Recommendations

1. **DRIFT-4 must be reconciled before Phase 5 sign-off.** The forked
   inline remediation in `_run_fallback` is the highest-value
   dual-surface hazard: it duplicates the entire fix pipeline rather
   than re-entering it. A future edit to the main-loop verify/fix/push
   logic will silently skip the fallback copy. Extract a shared
   remediation helper or genuinely re-enter `S2_CLASSIFY`.
2. **DRIFT-1/DRIFT-3/DRIFT-5 are state-materialization gaps.** Decide
   the contract: are S5a/S5b observable states or routing-only table
   nodes? Document the decision so state-asserting tests target the
   right surface and the table edges stop implying observability the
   inline loop does not deliver.
3. Re-run this lens AFTER reconciliation — `transition()` and the inline
   loop must be re-diffed because fixing DRIFT-4 will move code.

## Confidence

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 0 | Glob: 0 | Bash: 0
  (single-file scope; the entire 998-line file was read in one pass and
  every cited line verified against that read — every edge on both
  surfaces was located by direct line citation, no claim relies on a
  prior report)

## QA Complete

VERDICT: FAIL
