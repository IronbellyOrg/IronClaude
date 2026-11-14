# Merge Log: Q31

## Metadata

- Base: Variant 3 (proposal-C), `adversarial/variant-3-original.md`
- Executor: merge-executor agent
- Changes applied: 6 of 6
- Status: success
- Timestamp: 2026-11-14

## Changes Applied

### Change 1: Idle-only firing

- Status: applied
- Source: diff-analysis A-002; all three advocates ACCEPT
- Target: "What happens next if the owner picks it", cron bullet (insert)
- Before: the cron bullet ended with "(a one-shot subscription that sends nothing to the peer)."
- After: adds "The job fires only while the coordinator session is idle, so a long busy turn delays it; "about every 10 minutes" is a ceiling, not a guarantee."
- Provenance tag: `<!-- Source: Base (original, modified) with Change #1, Change #3 and Change #4 -->`
- Validation: pass; additive, matches the plan's integration point

### Change 2: Correct the overstatement about non-worker peers

- Status: applied
- Source: round1-advocate-3.md, Concessions, "Overstated claim"
- Target: "What it unlocks", first bullet (replace)
- Before: "... never appear in the Orca message queue, so only a timer-driven check sees them go idle."
- After: "... never appear in the Orca message queue, so until `/sc:sweep` is runnable, only a timer-driven check sees them go idle. Once SWEEP-RUNNABLE holds, WC-16's sweep report also lists person-started sessions."
- Provenance tag: `<!-- Source: Base (original, modified) with Change #2 -->`
- Validation: pass; second sentence states the plan's rationale (WORKER-CONTRACT.md:288 as quoted in the concession)

### Change 3: Message-less subscriptions

- Status: applied
- Source: round1-advocate-3.md, Concessions, "Never messaged tension"
- Target: "What happens next if the owner picks it", cron bullet (insert)
- Before: no statement that only message-less subscriptions are used
- After: adds "Only message-less subscriptions are used, so person-started sessions are never messaged (WC-16)."
- Provenance tag: `<!-- Source: Base (original, modified) with Change #1, Change #3 and Change #4 -->`
- Validation: pass; plan gave no exact wording, text taken from the concession

### Change 4: Ledger entry is the coordinator's own record

- Status: applied
- Source: round1-advocate-3.md, Concessions, "Ledger write wording"
- Target: "What happens next if the owner picks it", expiry bullet (insert)
- Before: "... re-creates it on expiry or after a resume."
- After: adds "That ledger entry is the coordinator's own local record, not an action of the check, so it does not conflict with line 579's "or any write"."
- Provenance tag: `<!-- Source: Base (original, modified) with Change #1, Change #3 and Change #4 -->`
- Validation: pass; plan gave no exact wording, text taken from the concession

### Change 5: Owner's yes as fresh confirmation

- Status: applied
- Source: diff-analysis A-001; all three QUALIFY
- Target: "Answer" (append one sentence)
- Before: the Answer ended with "... more often than WC-16 allows."
- After: appends "The order comes from a 9-day-old memory note, so the owner's yes here is the fresh confirmation that settles it, not the memory."
- Provenance tag: `<!-- Source: Base (original, modified) with Change #5 -->`
- Validation: pass; one sentence, as planned

### Change 6: Contract promotion as a separate later decision

- Status: applied
- Source: Variant 2, "Answer" and "What it unlocks" (U-001)
- Target: "What stays unresolved", first bullet (replace)
- Before: "Whether the rule should become part of the worker contract for all coordinators (not asked here)."
- After: "Whether to write the rule into the worker contract for all coordinators is a separate owner decision, best raised as its own item."
- Provenance tag: `<!-- Source: Base (original, modified) with Change #6 (from Variant 2) -->`
- Validation: pass; uses the plan's integration point text verbatim

## Post-Merge Validation

### Structural Integrity

- One H1 and the base's five H2 headings, in base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No heading added or removed.
- Provenance header present; one Source tag before each section.
- No em dashes or en dashes in the merged document (grep check).

### Internal References

- Line references (section 6.6 line 1026, spec line 579), WC-16, `WORKER-CONTRACT.md:288`, INV-010, Q25, Q33, #539 and the memory note name are unchanged from the base or taken from the cited concession. All resolve to the same targets as in the base.
- "line 579" in Change 4 points to the same spec line already cited in the "Limits kept" bullet.

### Contradiction Re-Scan

- Resolved by the merge: "no write of any kind" (Limits kept) against recording the job id in the ledger is now reconciled by Change 4.
- Resolved by the merge: "only a timer-driven check" against WC-16's sweep report is now scoped to before SWEEP-RUNNABLE (Change 2).
- Residual, not a contradiction: the Answer still says "about every 10 minutes"; the cron bullet now qualifies this as a ceiling (Change 1). The Answer was not changed because the plan does not list it.
- No new contradiction found. The new first "What stays unresolved" bullet and the unchanged cost "The rule stays in a memory note" agree.

## Summary

All 6 planned changes were applied in plan order to Variant 3. Changes are wording or added sentences only; the answer (yes, read-only, this program's coordinator) is unchanged. No unplanned edits. Output: `owner-questions/Q31/merged-output.md`.
