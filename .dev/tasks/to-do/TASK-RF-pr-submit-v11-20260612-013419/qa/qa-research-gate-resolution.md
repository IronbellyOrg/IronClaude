# A.8 Research Quality Gate — Resolution

**Date:** 2026-06-12
**Track:** pr_submit V1.1 extension (single track)

## Gate agent verdicts (5 agents)

| Agent | Lens | Verdict |
|---|---|---|
| rf-analyst | completeness | PASS (8/8) |
| rf-analyst | cross-validation | PASS (conditional carry) |
| rf-qa | evidence-quality | FAIL → resolved |
| rf-qa | gap-detection | FAIL → resolved |
| rf-qa-qualitative | research-depth | PASS |

## Root cause of both FAILs: ONE shared factual error (now fixed)

Both FAIL verdicts were driven by a SINGLE IMPORTANT issue: research file `05-test-infra-fixtures-markers.md`
miscounted the current `IDEMPOTENCY_SETS` as **4** (it dropped `processed_review_ids`). The verified
truth is **5** (`run_log.py:27-33`, module comment literally "The 5 idempotency sets"), confirmed
independently by files 01/03/06/07, all three other gate agents, and the orchestrator's own grounding.
The addendum adds the 6th set `auggie_review_invoked` → **5 → 6**.

**Fix applied:** file 05's miscount corrected in place (5→6, phantom "reconcile/maybe a 5th" framing
removed). No new research needed — the corrected value was already established by 4 independent reads.

Because the FAIL was entirely attributable to this one corrected error (not a coverage gap), a full
5-agent re-gate is not warranted (the other findings were all PASS or MINOR carry-flags). **Gate: RESOLVED/PASS.**

## MINOR carry-forward flags → baked into BUILD_REQUEST (builder action, not research gaps)

1. **state-machine.md [MOD]** — `refs/state-machine.md` declares itself the single FSM source and owns the
   topology; the new S5a/S5b edges require amending it even though addendum §6.5 omits it. Builder MUST
   add a state-machine.md [MOD] item. (R4 §D; confirmed by cross-validation agent.)
2. **recovery.py Branch-A (Open Question / needs_human_decision)** — `recovery.py:111` hard-resumes to
   `S5_AWAITING_REREVIEW`; post-V1.1 it may semantically need `S5A_RETRIGGER_REVIEW` (re-trigger not yet
   posted on recovery). The addendum does NOT resolve this. Builder MUST surface it as an Open Question
   that HALTS rather than auto-defaulting a behavior change (per memory feedback_human_decision_items_must_halt).
3. **fallback_skip terminal predicate** — the `(S5B_AUGGIE_FALLBACK,"fallback_skip") → HALT_MAX_ROUNDS|TERMINAL_CLEAN`
   edge has a conditional terminal selector no file fully specifies. Builder defines the predicate
   (clean residual → TERMINAL_CLEAN; residual findings → HALT_MAX_ROUNDS) per spec §3.2 intent.
4. **loop-guard.md possible 6th "33→37" site** — R4 cites a member-count assertion in `refs/loop-guard.md`;
   R3's 5-place enumeration omits it. Builder's loop-guard.md [MOD] item must re-grep for "33" and bump if present.
5. **__init__ export surface** — if any test imports new top-level fns (`is_decline`/`clamp_max_rounds`/
   `STATE_DECLINED`) at package root, `__init__.py` `__all__`/re-export needs an edit. Builder includes a
   re-grep+wire item.
6. **status-enum granularity (spec §11.1, non-blocking)** — reuse `terminal_clean`/`terminal_max_rounds`
   (spec recommendation) vs add `terminal_fallback_*`. Builder follows the reuse recommendation, flags the
   alternative in Open Questions.

VERDICT: PASS (after surgical correction of the single blocking miscount).
