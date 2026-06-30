# QA Report — FINAL-PHASE M3 Domain-Accuracy Lens (pr_submit V1.1)

**Topic:** pr_submit V1.1 — complete change-set domain-accuracy audit
**Date:** 2026-06-12
**Phase:** doc-qualitative (domain-accuracy lens, FINAL-PHASE M3 gate)
**Fix cycle:** N/A (fix_authorization: false — report only)
**Stance:** Adversarial. Assumed ≥5 domain errors; verified by reading.

---

## Overall Verdict: PASS

The three load-bearing domain claims hold against source. The four
domain facts (Augment triggers on PR-open or explicit operator comment;
pushes do NOT auto-trigger; "abnormally large" decline = App refusing;
fallback is pr_submit's OWN /sc:auggie-review) are respected verbatim in
both the core and the skill layer. No domain errors of CRITICAL or
IMPORTANT severity found. Two MINOR observations logged below — neither
is a defect; both are recorded for honesty per the adversarial mandate.

---

## Files Read (evidence base)

- `src/superclaude/pr_submit/fsm.py` (1011 lines, full)
- `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (138 lines, full)
- `src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md` (full)
- `src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md` (full)
- `.dev/.../phase-outputs/plans/oq1-recovery-resume-target.md` (full)

---

## Claim Verification

### Claim 1 — Fallback re-enters the V0.1 pipeline under the clamp; findings NOT trusted verbatim (FR-9.4)

**VERDICT: PASS.**

- **Clamp recorded once, monotone:** `_run_fallback` sets
  `result.effective_max_rounds = clamp_max_rounds(base)` where
  `clamp_max_rounds(effective, hard=1) = min(effective, hard)`
  (fsm.py:760, :145-153). One-way non-increasing — matches INV-R3 and
  auggie-fallback.md:44.
- **NOT trusted verbatim (FR-9.4):** the fallback re-grades through
  verify-before-remediate BEFORE any edit:
  `verified = [f for f in fallback_findings if config.verify(f)]`
  (fsm.py:779); an all-unverified set converges clean with no push
  (fsm.py:780-785). This matches auggie-fallback.md:52-55 ("NOT trusted
  verbatim … re-enter verify-before-remediate … all-unverified … no
  push") and the RunConfig docstring (fsm.py:714-717).
- **Pipeline tail under clamp:** after verify, the fallback runs the
  G-edit gate (fsm.py:791), apply_edits (fsm.py:797), run_validation
  (fsm.py:798), and the INV-016 G-push conjunction against
  `fallback_round_counter` vs the CLAMPED `effective_max_rounds`
  (fsm.py:805-812) — i.e. verify→fix→validate→push under the clamp, with
  the budget gate using the clamped value. Confirmed.
- **Strict-once + single-shot:** `invoke_auggie_review` is gated on
  `result.auggie_review_invoked` (fsm.py:763-765, INV-R2); the
  structural cap `loop_guard_should_halt(fallback_round_counter,
  effective_max_rounds)` (fsm.py:768) terminates without loop-back; the
  frozen `round_counter` is never touched in `_run_fallback` (only
  `fallback_round_counter` increments, fsm.py:782/828). Matches
  auggie-fallback.md:46-49.

**MINOR observation (not a defect):** The docstrings/refs phrase the
re-entry as "re-enter the V0.1 pipeline (verify→fix→validate→push)" and
auggie-fallback.md:47 lists "classify → re-grade → verify-before-remediate
→ route → fix → validate → push". The core `_run_fallback` does NOT
literally re-run a classify/severity-remap step — it consumes
`config.fallback_findings` (already-classified input) and enters at the
verify step (fsm.py:775-779). This is consistent with NFR-6 core purity
(the classify/re-grade work is the SKILL's job via Waves 2-3, SKILL.md:94
"re-enter Waves 2-6 ONCE under the clamp"), not a contradiction — the
core records decisions on already-normalized findings exactly as the
main loop does. Flagged only because the verbatim verb list in the ref
is broader than what the core function itself performs; the SKILL layer
supplies the missing classify/re-grade stage. No fix required.

### Claim 2 — Augment-trigger facts: a push does NOT auto-trigger; the re-trigger comment drives the re-review

**VERDICT: PASS.**

- **Push does NOT auto-trigger (core):** in the main loop, after
  push→reply→resolve, the FSM routes through S5a re-trigger BEFORE
  awaiting the re-review: `result.state = S5A_RETRIGGER_REVIEW;
  config.do_retrigger(...)` then `S5_AWAITING_REREVIEW` (fsm.py:960-971).
  The inline comment states verbatim "a push does NOT auto-trigger an
  Augment re-review — post the re-trigger comment" (fsm.py:960-963).
- **Transition table:** `RESOLVING → S5A_RETRIGGER_REVIEW` (fsm.py:622-626,
  comment: "a push does NOT auto-trigger an Augment re-review"), then
  `S5A_RETRIGGER_REVIEW → S5_AWAITING_REREVIEW` on "retriggered"
  (fsm.py:627-630), then the INV-001 round tick fires only at
  `S5_AWAITING_REREVIEW → S2_CLASSIFY` on "rereview_attributed"
  (fsm.py:631-632). The re-trigger itself does NOT tick the counter
  (fsm.py:628-629).
- **Re-trigger gated on applied_edits > 0:** fsm.py:964 — only a cycle
  that actually pushed posts the comment. Matches INV-R1
  (review-retrigger.md:44-48).
- **Timeout semantics:** a push WITHOUT an attributed re-review (outcome
  "timeout") routes to TERMINAL_TIMEOUT and does NOT advance
  round_counter (fsm.py:992-996). Matches review-retrigger.md:50-53.
- **Skill layer:** SKILL.md:93 states "a push does NOT auto-trigger an
  Augment re-review … post the re-trigger comment via
  scripts/retrigger-review.sh … BEFORE re-entering the S5 poll … round_counter
  ticks only when the subsequent poll attributes the re-review to our
  pushed SHA." review-retrigger.md:3-6 confirms the
  `augmentcode[bot]` reviews ONLY on PR-open or explicit
  augment/auggie/augmentcode review comment; pushes do not auto-trigger.
  Body token is exactly `auggie review` (review-retrigger.md:25-31),
  one of the accepted trigger phrases. All consistent with the stated
  domain fact and with memory `reference_augment_review_triggers.md`.
- **Decline = App refusing:** auggie-fallback.md:3-5 / SKILL.md:94 frame
  the "abnormally large" decline as the App refusing to auto-review and
  asking for a trigger comment; the "Do NOT take the App's bait"
  guidance (auggie-fallback.md:21-23, SKILL.md:94) correctly distinguishes
  the App's decline comment from our operator re-trigger, and the
  fallback is pr_submit invoking its OWN /sc:auggie-review. Domain fact
  respected.

### Claim 3 — OQ-1 PENDING handling: recovery.py UNCHANGED, decision left to human

**VERDICT: PASS.**

- The plan explicitly states "DECISION: PENDING — requires human
  sign-off. recovery.py source is LEFT UNCHANGED" (oq1 plan:3) and
  "recovery.py is NOT modified by this task. The V1.0 Branch-A behavior
  (→ S5_AWAITING_REREVIEW) ships unchanged" (oq1 plan:42-43).
- The tension is correctly characterized: post-V1.1 a push does NOT
  auto-trigger, so a crash recovered as "landed" between push and
  re-trigger-comment post MAY need to resume at S5A_RETRIGGER_REVIEW
  rather than S5_AWAITING_REREVIEW (oq1 plan:11-21). This is domain-accurate
  and consistent with the Claim-2 finding above (S5a precedes S5).
- The trade-off is honest and bidirectional: resuming to S5A when the
  comment WAS already posted → double-post (bounded benign, INV-R1
  `<= max_rounds`, App idempotent); resuming to S5 when it was NOT posted →
  waits forever → TERMINAL_TIMEOUT (oq1 plan:23-32). The disambiguator
  (a re-trigger-comment watermark) is correctly noted as unspecified by
  the addendum (oq1 plan:30-32), so leaving it to a human is the correct
  HALT-not-auto-default posture (consistent with memory
  `feedback_human_decision_items_must_halt.md`).
- Disposition logs it as a blocking High-priority human decision under
  Follow-Up Items + Task Summary (oq1 plan:41-45). Correct.

**Cross-check vs domain facts:** the INV-R1 boundedness the plan relies on
("INV-R1 bounds it to <= max_rounds", oq1 plan:26) matches
review-retrigger.md:44-48 and fsm.py:964/970. The App-idempotency claim
is consistent with the trigger-phrase model. No domain error.

---

## Adversarial Sweep — errors hunted, NOT found

Per the ≥5-errors mandate, the following candidate domain errors were
explicitly tested and CLEARED:

1. **Did the fallback trust App findings verbatim?** No — verify gate at
   fsm.py:779 (FR-9.4 honored).
2. **Did the core treat a push as auto-triggering a re-review (V1.0
   regression)?** No — S5a re-trigger interposed (fsm.py:960-971,
   transition fsm.py:622-630).
3. **Did the re-trigger comment tick round_counter (INV-001 violation)?**
   No — tick is solely at S5→S2 attributed edge (fsm.py:1001, :631-632);
   re-trigger does not (fsm.py:628-629, review-retrigger.md:47-48).
4. **Did the fallback's clamp leak into / re-open the main round_counter?**
   No — counters independent; round_counter frozen in `_run_fallback`
   (fsm.py:747 docstring, only fallback_round_counter mutates).
5. **Did the fallback fire its OWN review more than once?** No — strict-once
   on `auggie_review_invoked` (fsm.py:763-765, INV-R2).
6. **Did OQ-1 silently auto-default recovery.py to the new S5a target?**
   No — recovery.py unchanged, PENDING + human HALT (oq1 plan:3,42-43).
7. **Did the re-trigger body or fallback target the upstream instead of
   the fork?** No — review-retrigger.md:25-31 pins
   `repos/IronbellyOrg/IronClaude/...`; fork-pin enforced.
8. **Did the decline get confused with the operator re-trigger ("take the
   bait")?** No — explicitly guarded (auggie-fallback.md:21-23, SKILL.md:94).

---

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source:** ~20 distinct
   code/doc assertions, each with file:line citation (fsm.py clamp,
   verify gate, G-push budget, S5a interposition, transition edges,
   round-tick site, counter independence, strict-once gate; ref-level
   trigger semantics and fork-pin; OQ-1 disposition).
2. **Files read:** fsm.py, SKILL.md, review-retrigger.md,
   auggie-fallback.md, oq1-recovery-resume-target.md (all full).
3. **If 0 issues — why trust the check?** I did not report 0 issues; I
   logged 1 MINOR phrasing observation (ref verb-list breadth vs core
   function scope) and explicitly ran 8 adversarial error-hunts, each
   cleared with a specific file:line. The verdict rests on read evidence,
   not absence of looking.
4. **Web research:** none performed (instructed "No web search"); no
   Tavily/fallback engagement to report.

## Confidence
Verified: 3/3 claims (20+ sub-assertions) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

## Tool engagement
Read: 5 | Grep: 0 | Glob: 0 | Bash: 1 (file listing)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | refs/auggie-fallback.md:47 | Re-entry verb list ("classify → re-grade → …") is broader than what core `_run_fallback` performs (core enters at verify on already-classified `fallback_findings`; classify/re-grade is the SKILL's Wave 2-3 job). | None required — consistent with NFR-6 core purity; noted for honesty only. Optionally clarify the ref that classify/re-grade is SKILL-layer, not core. |

---

VERDICT: PASS
