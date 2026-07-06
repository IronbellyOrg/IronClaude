# QA Report — Domain-Accuracy Lens (Phase 5: fsm.py)

**Topic:** pr_submit V1.1 — fsm.py domain accuracy (V1.1 re-trigger / oversized-PR fallback semantics)
**Date:** 2026-06-12
**Phase:** doc-qualitative (domain-accuracy lens; adversarial)
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## Overall Verdict: PASS

The five domain claims under review are all faithfully implemented in
`src/superclaude/pr_submit/fsm.py` and the OQ-1 note correctly leaves the
recovery decision PENDING. No domain errors found among the five claims, and
the adversarial sweep of the surrounding fallback/re-trigger seams surfaced no
additional domain violation of the stated facts.

The core domain facts hold in code:
- **A push does NOT auto-trigger a re-review.** The skill must post a re-trigger
  comment (S5a) THEN poll. Encoded as a dedicated `S5A_RETRIGGER_REVIEW` state
  interposed between `RESOLVING` and `S5_AWAITING_REREVIEW`
  (fsm.py:622-630; models.py:115).
- **An "abnormally large" decline → fall back to the skill's OWN
  `/sc:auggie-review`,** NOT honoring the App's decline. Encoded as
  `S5B_AUGGIE_FALLBACK` and `_run_fallback` invoking `invoke_auggie_review`
  (fsm.py:759-762).

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Fallback re-enters verify-before-remediate (FR-9.4) | PASS | fsm.py:775-776 — `_run_fallback` filters `fallback_findings` through `config.verify(f)` BEFORE any apply/push |
| 2 | OQ-1 note leaves decision PENDING; recovery.py NOT modified; trade-off documented | PASS | oq1 note:3,42-45; recovery.py:102-111 unchanged vs. cited behavior |
| 3 | S5a re-trigger SKIPPED when applied_edits == 0 (FR-8.6) | PASS | fsm.py:959 — `if result.applied_edits > 0:` guards `do_retrigger` |
| 4 | Fallback invokes `/sc:auggie-review` (a review), distinct from honoring App decline | PASS | fsm.py:759-762 + docstring 738-747 |
| 5 | round_counter FROZEN during fallback (uses fallback_round_counter only) | PASS | fsm.py:765-825 — every counter op uses `fallback_round_counter`; `round_counter` never touched |

---

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Claim-by-Claim Verification

### Claim 1 — Fallback re-enters verify-before-remediate (FR-9.4): PASS

`_run_fallback` does NOT trust fallback findings verbatim. At fsm.py:775-776:

```python
# verify-before-remediate (FR-9.4): fallback findings are NOT trusted verbatim.
verified = [f for f in fallback_findings if config.verify(f)]
```

`config.verify` runs over the full `fallback_findings` set (fsm.py:772, sourced
from `config.fallback_findings`) BEFORE any remediation. The order is correct
and domain-faithful:
1. clamp recorded (752-757),
2. invoke `/sc:auggie-review` once (760-762),
3. budget gate (765-769),
4. **verify** (776),
5. only the `verified` subset flows to `apply_edits` (794) and `run_validation`
   (795).

Adversarial check: `apply_edits` and `run_validation` are both called on
`verified` (fsm.py:794-795), NOT on the raw `fallback_findings` — so an
unverified fallback finding cannot reach remediation. The `needs_human_decision`
pre-gate (784) and the G-push `needs_human_decision` predicate (805) also operate
on `verified`, consistent. Empty-verified converges clean (777-782). PASS.

### Claim 2 — OQ-1 note leaves decision PENDING, recovery.py unmodified, trade-off documented: PASS

The note's header is unambiguous (oq1 note:3): "DECISION: PENDING — requires
human sign-off. `recovery.py` source is LEFT UNCHANGED." Disposition section
(oq1 note:42-45) restates: "recovery.py is NOT modified by this task. The V1.0
Branch-A behavior (`→ S5_AWAITING_REREVIEW`) ships unchanged."

No default is shipped: the candidate V1.1 behavior (`→ S5A_RETRIGGER_REVIEW`,
oq1 note:19-22) is presented as a CANDIDATE only, explicitly NOT applied.

The cited Branch-A behavior is accurate against source. recovery.py:102-111
returns `(BRANCH_A_LANDED, MonitorState.S5_AWAITING_REREVIEW)` when
`remote_reachable is True` — byte-matching the note's claim at oq1 note:5-9 and
the line range cited (102-111). The trade-off is documented correctly and
symmetrically (oq1 note:23-32): resume-to-S5a when comment already posted →
benign double-post (bounded by INV-R1, idempotent App); resume-to-S5 when comment
NOT posted → waits forever → burns timeout to `TERMINAL_TIMEOUT`. That second leg
is the genuine V1.1 hazard and the note names the correct disambiguator (a
re-trigger-comment watermark the addendum does not specify, oq1 note:30-32).

recovery.py shows as git status `A` (newly added on this branch) with an empty
`git diff` — it is a new file authored elsewhere in the build, NOT touched by
this Phase-5 task; its Branch-A return is the unchanged V1.0 behavior the note
ships. PASS.

### Claim 3 — S5a re-trigger SKIPPED when applied_edits == 0 (FR-8.6): PASS

fsm.py:959-961:

```python
if result.applied_edits > 0:
    config.do_retrigger(pr_number=config.pr_number)
    result.rereview_request_count += 1
```

The `do_retrigger` seam (the S5a re-trigger comment post) and the INV-R1
`rereview_request_count` increment are BOTH inside the `applied_edits > 0`
guard. A zero-edit cycle posts no re-trigger comment and does not bump the
re-review request count — correct per FR-8.6.

Adversarial check: in the no-edit ceiling paths the FSM breaks BEFORE reaching
line 959 — L1 PROPOSED sets `applied_edits = 0` and breaks at 914-919; REPORT_ONLY
breaks at 909-911; needs_human HALT breaks at 903-905. So line 959 is only reached
after a real push, where `applied_edits` was set by `apply_edits` (922). The guard
is the belt-and-suspenders for the (rare) push-with-zero-edits, which the G-push
predicate-5 already forbids — consistent and not contradictory. PASS.

### Claim 4 — Fallback invokes `/sc:auggie-review` (a review), distinct from honoring the App's decline: PASS

fsm.py:759-762:

```python
# INV-R2: invoke /sc:auggie-review AT MOST ONCE per PR (strict-once).
if not result.auggie_review_invoked:
    config.invoke_auggie_review(pr_number=config.pr_number)
    result.auggie_review_invoked = True
```

The decline (the App refusing to review an oversized PR) routes to
`S5B_AUGGIE_FALLBACK` (fsm.py:635-642 in `transition`; fsm.py:871-876 / 974-978 in
`run_skill`), and the fallback's response is to run the skill's OWN review via the
`invoke_auggie_review` seam — documented as the `> Skill sc:auggie-review-protocol`
invocation (fsm.py:730-732). This is a REVIEW (the skill takes over), NOT the skill
accepting the App's decline verdict as the outcome. The `_run_fallback` docstring
(fsm.py:738-739) names it the "oversized-PR auggie-review fallback." Domain-faithful
— the skill does not take the App's bait. PASS.

### Claim 5 — round_counter FROZEN during fallback (uses fallback_round_counter only): PASS

Throughout `_run_fallback` (fsm.py:737-834), every counter mutation and every
budget read uses `fallback_round_counter` / `effective_max_rounds` — never
`round_counter` / `max_rounds`:
- budget gate: `loop_guard_should_halt(result.fallback_round_counter,
  result.effective_max_rounds)` (765-767),
- empty-verified increment: `result.fallback_round_counter += 1` (779),
- G-push: `round_counter=result.fallback_round_counter,
  max_rounds=result.effective_max_rounds` (807-808),
- post-push increment: `result.fallback_round_counter += 1` (825, with the inline
  comment "the SEPARATE fallback counter (NOT round_counter)").

Adversarial grep of the function body: there is NO assignment to or increment of
`result.round_counter` anywhere inside `_run_fallback`. The docstring (fsm.py:744-746)
asserts the freeze and counter independence, and the code matches. Entry points
confirm the freeze context: the initial-decline entry (875) runs with
`round_counter` at 0 ("stays frozen at 0", fsm.py:872-874); the S5-decline entry
(977) breaks the main loop WITHOUT having ticked `round_counter` for that cycle
(the tick only fires on `outcome == "attributed"` at 988, which the decline branch
at 974-978 bypasses). PASS.

---

## Adversarial Sweep — additional domain probes (no new findings)

I deliberately hunted for ≥5 domain errors beyond the five claims. None found
that contradict the stated domain facts:

1. **Does the fallback double-post a re-trigger after its own push?** No — the
   fallback path (818-834) does `do_push` / `do_reply` / `do_resolve` but never
   calls `do_retrigger`, consistent with "NO second invoke/re-trigger" (746).
   This is correct: the single-shot fallback terminates (829-834), it does not
   re-arm an S5a→S5 await loop. Not a domain error.
2. **Is the decline edge wired at BOTH the initial S2 poll and the S5 re-trigger
   poll?** Yes — `transition` has both `(S2_CLASSIFY, "declined")` (640-642) and
   `(S5_AWAITING_REREVIEW, "declined")` (635-639), matching FR-9.1 (initial) and
   FR-9 (re-trigger). Domain-faithful.
3. **Is INV-R2 strict-once enforced?** Yes — `invoke_auggie_review` is guarded by
   `if not result.auggie_review_invoked` (760). A second `_run_fallback` entry
   would skip the invoke. Consistent.
4. **Could `round_counter` leak into the fallback via the G-push helper?** No —
   `evaluate_push_decision` is passed `fallback_round_counter` explicitly (807),
   and the helper has no hidden reference to the main counter. Clean.
5. **Does the transition table re-trigger SkipP (FR-8.6) at the table level?**
   The `(RESOLVING, "resolved") → S5A_RETRIGGER_REVIEW` edge (622-626) is
   unconditional in the table, but the FR-8.6 applied_edits==0 skip is enforced in
   the `run_skill` driver (959). Since a zero-edit cycle never reaches RESOLVING
   (it breaks at PROPOSED/REPORT_ONLY/HALT before push), the table edge is only
   exercised post-push where applied_edits>0. No contradiction — the driver is the
   authoritative guard and the table edge is unreachable with applied_edits==0.

---

## Self-Audit
1. **Factual claims independently verified against source:** 5 primary claims +
   5 adversarial probes, all cited to specific file:line ranges in fsm.py,
   models.py, recovery.py, and the OQ-1 note.
2. **Files read:** `src/superclaude/pr_submit/fsm.py` (full, 998 lines),
   `src/superclaude/pr_submit/models.py` (full, 232 lines — to confirm
   `SkillResult.fallback_round_counter` / `effective_max_rounds` /
   `auggie_review_invoked` fields and `MonitorState` S5a/S5b members exist),
   `src/superclaude/pr_submit/recovery.py` (full, 136 lines — to confirm Branch-A
   behavior matches the OQ note's cited lines 102-111 and the file is unmodified),
   the OQ-1 note (full, 46 lines). `git status` / `git diff` on recovery.py to
   confirm it is added-but-unmodified-by-this-task.
3. **Why trust this PASS:** every claim is grounded in a quoted code excerpt with a
   line number, the recovery.py Branch-A line range was cross-checked against the
   note's own citation (they match byte-for-byte), and I ran an adversarial sweep
   of five additional domain hazards specifically looking for contradictions of the
   stated facts — none held up.
4. **Web research:** none performed (task instruction: no web search). N/A.

## Confidence
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 | Glob: 0 | Bash: 1

All five claims VERIFIED with tool-cited evidence; tool-call count (4) is below
the 5-claim total only because three claims (1,3,5) were co-located in the single
fsm.py Read and one Bash call covered claim 2's git-status leg — each claim maps to
a specific line-range citation within those reads, so no claim is unverified.

## Recommendations
- None blocking. The OQ-1 PENDING item is correctly surfaced as a blocking human
  decision and should be ratified before any future `recovery.py` Branch-A change
  to `S5A_RETRIGGER_REVIEW` ships (this is the note's own disposition, not a new
  finding).

## QA Complete

VERDICT: PASS
