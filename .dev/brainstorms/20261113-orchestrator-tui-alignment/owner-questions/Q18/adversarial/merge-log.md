# Merge Log: Q18

## Metadata

- Base: Variant 1 (proposal-A.md, identical to adversarial/variant-1-original.md)
- Plan: adversarial/refactor-plan.md (5 planned changes, all Low risk)
- Output: merged-proposal.md
- Merge date: 2026-11-14
- Executor: merge-executor (Step 5)
- Supporting evidence read: none beyond the plan; every change carried its exact text in the plan

## Changes Applied

### Change 1: Data exposure as a fifth CO-04 design concern

- Status: Applied
- Source: Variant 2 "What it costs or risks" bullet 1; diff points C-005, U-002; round1-advocate-3.md A-001
- Target: "What happens next if the owner picks it", CO-04 bullet (extend)
- Before: "...must name four things before any code: a transport, an identity envelope, an age rule (Q22) and a re-sanitising step (ADJ line 306)."
- After: "...must name four things before any code: a transport, an identity envelope, an age rule (Q22) and a re-sanitising step (ADJ line 306), and who may read a copy, because the snapshot is written with mode 0600 on purpose (ADJ line 244), including whether the whole snapshot or only part of it leaves the host."
- Provenance tag: `<!-- Source: Base (original, modified); reason: Variant 2 "What it costs or risks" bullet 1 (data exposure) merged per Change #1 -->`
- Validation: Text matches the plan. A comma was placed before "and who may read" so the added clause attaches after the closing citation. Only new citation is ADJ line 244, as the plan allows. See contradiction C1 below: the unchanged word "four" in this same sentence now counts five items.

### Change 2: Accurate Coder#477 wording

- Status: Applied
- Source: round1-advocate-1.md Concessions 4; round1-advocate-3.md C-002 verdict
- Target: "What happens next if the owner picks it", CO-01 bullet (replace wording)
- Before: "The Coder#477 reply (CO-01) states that no channel to the TUIBBS host exists or is planned yet (merged-requirements.md line 353, "the channel per Q18")."
- After: "The Coder#477 reply (CO-01) states that no channel exists and one is deferred until observer release 4 or an owner decision on a TUIBBS screen (merged-requirements.md line 353, "the channel per Q18")."
- Provenance tag: `<!-- Source: Base (original, modified); reason: wording replaced per round1-advocate-1.md Concessions 4 and round1-advocate-3.md C-002 (Variant 1 and Variant 3 advocates), merged per Change #2; base citation kept -->`
- Validation: The plan's replacement text covers the statement only; the base citation (line 353) was kept because the plan does not say to drop it. Consistent with the Answer's two triggers and with "Coder#477's text may need a second edit".

### Change 3: Remove an overclaim

- Status: Applied
- Source: round1-advocate-1.md Concessions 3
- Target: "What it unlocks", third bullet (replace)
- Before: "...so a later channel needs no change to the observer's file."
- After: "...so a later channel starts from the existing file; whether the identity and age pieces need new fields in it is not yet decided."
- Provenance tag: `<!-- Source: Base (original, modified); reason: overclaim removed per round1-advocate-1.md Concessions 3 (Variant 1 advocate), merged per Change #3 -->`
- Validation: Exact plan text. The retained base phrase "TUIBBS-ready shape" is softened by the new clause but does not contradict it.

### Change 4: Conditional contract-note sentence

- Status: Applied
- Source: Variant 2 "What happens next" bullet 5; round1-advocate-3.md Concessions
- Target: "What happens next if the owner picks it", contract-note bullet (extend)
- Before: "The contract note keeps "single owner, single OS user, single host" (line 453)."
- After: "The contract note keeps "single owner, single OS user, single host" (line 453) and adds one guard sentence: any future copy off this host is read-only and may start only after CO-04's design names all its pieces."
- Provenance tag: `<!-- Source: Base (original, modified); reason: Variant 2 "What happens next" bullet 5 (guard sentence) merged per Change #4 -->`
- Validation: Exact plan text. "All its pieces" resolves to the CO-04 bullet directly above. The single-host line is unchanged, as the plan requires.

### Change 5: The ledger is the authoritative record

- Status: Applied
- Source: round1-advocate-2.md A-002
- Target: "What happens next if the owner picks it", first bullet (extend)
- Before: "The ledger records "Q18: not before R4 or a TUIBBS statement" with the date."
- After: "The ledger records "Q18: not before R4 or a TUIBBS statement" with the date. The ledger is the authoritative record; the Coder#477 sentence below only repeats it."
- Provenance tag: `<!-- Source: Base (original, modified); reason: ledger-authority sentence appended from round1-advocate-2.md A-002 (Variant 2 advocate), merged per Change #5 -->`
- Validation: Exact plan text. "The Coder#477 sentence below" resolves to the next bullet.

## Post-Merge Validation

### Heading hierarchy

- Pass. One H1 (title) and the base's five H2 sections in base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No section added, removed or reordered.

### Internal references

- Pass. "the Coder#477 sentence below" (Change 5) points to the next bullet. "CO-04's design names all its pieces" (Change 4) points to the CO-04 bullet above. "Q4 (line 1177)", "Q22", CO-01 and CO-04 are unchanged base references.
- Citations: base citations (lines 353, 356, 306, 453, 145, 306, 1177) unchanged; the only new one is ADJ line 244, allowed by the plan.
- No em dashes or en dashes in the merged file (checked by search).

### Contradiction re-scan

- C1 (found, not fixed): CO-04 bullet. The unchanged base words "name four things" now introduce five items, because Change 1 appends a fifth concern (who may read a copy). The plan's own title calls it "a fifth CO-04 design concern" but its integration point adds text only and does not change "four". Left as is to follow the plan exactly. Suggested fix for the orchestrator: change "four things" to "five things" in that sentence.
- C2 (found, minor, not fixed): "What it costs or risks", bullet 1, unchanged base text: "the four missing pieces (transport, identity, age, re-sanitising) are designed later". After Change 1 the CO-04 design has five concerns, so this list omits data exposure. It is accurate as a list of the four pieces ADJ line 306 names as missing, but a reader may take it as the full list. Suggested fix: add "and who may read a copy" or say "the missing pieces".
- No other conflict found: the Answer's triggers match Change 2's "release 4 or an owner decision on a TUIBBS screen"; "Coder#477's text may need a second edit" fits Change 2 and Change 5; "CO-01 can be posted with a settled channel sentence" fits Change 2; "single host" in the Answer fits Change 4's guard.

## Summary

- Changes planned: 5. Applied: 5. Skipped: 0. Failed: 0.
- Structure: intact (five base sections, plain English, no dashes).
- Contradictions: 2 found between unchanged base text and Change 1 (C1 wording count in the same sentence; C2 minor list in the costs section). Both reported, not fixed, because the plan does not cover them.
- Status: success, with C1 and C2 for the orchestrator to decide.

## Orchestrator resolution of C1 and C2 (added after the merge)

- C1: changed "name four things" to "name five things" in the CO-04 bullet of merged-proposal.md.
- C2: changed the first "What it costs or risks" bullet to "the five missing pieces (transport, identity, age, re-sanitising, who may read a copy)", with a provenance tag marking the orchestrator edit.
- Result: no remaining contradiction.
