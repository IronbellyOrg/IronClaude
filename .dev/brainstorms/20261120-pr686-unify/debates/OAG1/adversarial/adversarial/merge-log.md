# Merge Log (OAG1)

## Metadata

- Base variant: Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/adversarial/variant-1-original.md`
- Incorporated variant: Variant 2 (CLAY), `variant-2-original.md` (same folder)
- Refactoring plan: `refactor-plan.md` (same folder)
- Executor: merge-executor
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG1/adversarial/merged-output.md`
- Changes applied: 9 of 9 planned; 4 rejected alternatives listed once, not as claims
- Status: Success
- Timestamp: 2026-11-20

## Changes Applied

### Change 1: Define "reminder" as display plus age of the wait; push notice reserved
- Status: Applied
- Before (Claim 3): "A waiting go gets no new push reminder in the first build. It keeps its slot, counts toward `max_in_flight`, and is shown as 'waiting on a person' with the age of the wait."
- After (Claim 3 and Terms): "A waiting go gets no push notice in the first build. ... is shown as 'waiting on a person' with the age of the wait, which is the reminder as defined in Terms." Terms defines "reminder" as display plus age and "push notice" as a message through a notice step, reserved. Mechanism last bullet and cost bullet 3 reworded to match.
- Provenance tag: `Source: Variant 2 (CLAY), Mechanism "Reaching the person"` folded into Base-modified tags on Terms, Mechanism and "What it costs"
- Validation: no sentence says "no reminder"; every "reminder" use is covered by the Terms definition, including the quoted K9 and S15b wording. Passed.

### Change 2: K15 expiry for `waiting_reapproval` only
- Status: Applied
- Before: Claim 3 had no expiry bullet.
- After: bullet under Claim 3: "A hand-back waiting for re-approval (`waiting_reapproval`) moves to `stopped` after an owner-set limit (K15). No default number is given. This expiry does not free capacity, because that state is outside the cap. No waiting merge go ever expires." (CLAY's capacity wording corrected as the plan says.)
- Provenance tag: `Source: Variant 2 (CLAY), Cited fact 5 (K15) and QG1 OD-13, merged per Change #2`
- Validation: expiry is attached only to `waiting_reapproval`; the waiting merge go is stated as never expiring. Passed.

### Change 3: Both waiting states side by side
- Status: Applied
- Before (Cited fact 5): K9 quote credited to "QG1 OD-13 and merged requirements K9 and INV-023".
- After (Cited fact 5): two sub-bullets. Waiting merge go (worker done, PR open, counts toward `max_in_flight`, never expires; the quoted text is K9 at `merged-requirements.md:311`). Waiting re-approval (no worker, no PR, outside the cap per QG1 OD-13 at `debates/QG1/VERDICT.md:30-34`, K15 expiry on an owner-set limit, OA-14 line 690).
- Provenance tag: `Source: Base (original, modified)` on Cited facts (tag names Changes #7, #3, #8)
- Validation: the K9 misattribution is removed; line references come only from the inputs. Passed.

### Change 4: Reserve a go age check for the merge-automation build
- Status: Applied
- Before (Claim 1): "Merge automation stays off until the owner records a number, so no unattended process can fire a go typed days ago."
- After (Claim 1, appended): "The build of merge automation must carry a go age check, and it must refuse to start unless the owner has recorded a number or the explicit value 'none'. This is a requirement on that future build, not a setting added now ..." No key name added; no default number; the 24-hour figure marked UNVERIFIED.
- Provenance tag: `Source: Variant 2 (CLAY), Claim 1 and the owner-set number, merged per Change #4`
- Validation: does not contradict "no clock expiry by default" because it is a requirement on a build that does not exist (rows 28 and 29 DESIGN ONLY). Passed.

### Change 5: Hold clock start
- Status: Applied
- Before (Claim 2): "... a wait of 60 minutes (UNVERIFIED default), then escalation to the person."
- After (Claim 2): "... a wait of 60 minutes (UNVERIFIED default, owner-settable) ... The clock starts when the final head's checks finish (D06 item 4; ADD4, D:138)." Also in Answers OA-13b and Cited fact 7.
- Provenance tag: folded into `Source: Base (original, modified)` on Claim
- Validation: 60 minutes marked UNVERIFIED in Claim 2, Answers, Cited facts 2 and 7, and What it risks. Passed.

### Change 6: Existing re-listing surface
- Status: Applied
- Before (Mechanism last bullet): sweep fields and "An unanswered 'Needs you' entry stays ... woken daily at 07:00 local" with no caveat.
- After: same facts, plus "That report is configured for one named person today (Clay), so for the repository owner the sweep and the observer are the surfaces that show the wait."
- Provenance tag: `Source: Variant 2 (CLAY), Mechanism "Reaching the person" and Cited fact 8, merged per Change #6`
- Validation: SKILL.md:22 and :30 citations unchanged. Passed.

### Change 7: Correct the D06 reading
- Status: Applied
- Before: Claim 1 "It ends in exactly three ways"; fact 1 "D06 item 1 and Q01 item 5: a go ends on the named action, a head move or a revoke".
- After: Claim 1 "Following Q01 item 5, it ends in three ways ... D06 item 1 words this differently: it says the go 'expires (number is an Owner DECISION, no source gives one)'. This paper takes Q01 item 5 as the default and records the D06 wording as the owner's open option." Cited fact 1 states the two wordings separately; fact 2 notes OA-13 "No expiry" is one open owner option, not a requirement.
- Provenance tag: `Source: Base (original, modified)` on Claim and Cited facts
- Validation: "exactly" removed. Passed.

### Change 8: D:1177 omitted half restored
- Status: Applied
- Before (Cited fact 6): D:1177 (AD-B4) calls the notice cap "not ruled on; open".
- After: the same, plus "The same row also says 'Settled as recommended (ruling 39)', a cap of 5 notices a day; D11 treats ruling 39 as Clay's ruling, not the repository owner's, and the owner has not ruled."
- Provenance tag: `Source: Base (original, modified)` on Cited facts
- Validation: only inputs used (refactor plan, base-selection source error 2). Passed.

### Change 9: OA-13c sentence
- Status: Applied
- Before: `changes_requested` appeared only in Cited fact 8.
- After: Claim 2 ends "`changes_requested` stays a hard refusal that no go overrides (D06 item 3, D:583)." Answers item 3 (OA-13c) added.
- Provenance tag: folded into `Source: Base (original, modified)` on Claim
- Validation: matches Cited fact 8. Passed.

### Additions required by the merge brief (not plan changes)
- "Answers" section after Claim with OA-13a, OA-13b, OA-13c, OA-25a, OA-25b as numbered lines (answer, reason, source). Tag: Base (original, modified).
- "Considered and not adopted" section listing the four rejected alternatives (C-001, C-003, C-004 merge go, C-002) with the plan's reasons, none stated as a claim.
- "Terms" made a heading; added definitions for reminder, push notice, ADD4, AD-B4, K9, K15, S15b, D11 and other row names so the merged text can be read alone. All definitions come from the inputs.

## Post-Merge Validation

### Structural integrity
- One H1 (title "Merged position for OAG1: merge go lifetime and waiting policy"), then H2 sections in order: Terms, Claim, Answers, Mechanism, Cited facts, What it costs, What it risks, What it gets right, Considered and not adopted. No heading levels skipped. Passed.
- Provenance header lines (3) present at the top; a Source tag precedes every section and every merged block. Passed.

### Internal references
- Claim 3 points to Cited facts 6 (exists). Answers point to Cited facts 1 to 8, Claim 1, 2, 3 and "Mechanism, last bullet" (all exist). Terms points to Claim 3 (exists). Cited fact 1 mentions "(Change #7)" and fact 5 "(Change #3)" were removed from the document body so no body text points to the plan. Change numbers appear only in HTML comments. Passed.

### New contradictions
- "No reminder" versus "with a reminder": scan for "no reminder" and "no new push reminder" returns no hits; the K9 and S15b quotes "with a reminder" are covered by the Terms definition (display plus age; push notice is separate). Passed.
- Waiting merge go expiry: no sentence says a waiting merge go expires; Claim 3 bullet, Answers 5 and Cited fact 5 state it never expires. The "expires" hits are the D06 item 1 quote (the owner's open clock option), the K15 `waiting_reapproval` expiry, and the rejected alternatives. K15 expiry is attached only to `waiting_reapproval`. Passed.
- Claim 1 "no clock expiry by default" versus the reserved age check: consistent, the check is a future build requirement with owner-recorded number or "none". Passed.
- UNVERIFIED marking: 60-minute hold and 24-hour figure carry UNVERIFIED in Claim 1, Claim 2, Answers 2, Cited facts 2 and 7, What it risks, and Considered and not adopted. Passed.
- Style: scan for em dashes returns none. Passed.
- New facts, line numbers or numbers beyond the inputs: none added.

## Summary

- Planned changes: 9
- Applied: 9
- Failed: 0
- Skipped: 0
- Rejected alternatives recorded: 4 (in "Considered and not adopted")
- Validation issues: 0 open
