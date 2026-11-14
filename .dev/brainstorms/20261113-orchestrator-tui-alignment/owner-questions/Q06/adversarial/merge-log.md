# Merge Log: Q6 merged answer

## Metadata

- Base: `variant-3-original.md` (proposal C)
- Executor: merge-executor
- Plan: `refactor-plan.md` (2 planned changes, auto-approved 2026-11-14)
- Changes applied: 2 of 2 (Change 1, Change 2)
- Status: success
- Timestamp: 2026-11-14
- Output: `../merged-answer.md`

## Changes Applied

### Change 1: tell the owner what the narrow scope really means

- Status: applied
- Source: Variant 2 (proposal B), "What it unlocks", third bullet
- Provenance tag: `<!-- Source: Base (original, modified), Change 1 (from Variant 2, proposal B) -->` on "Answer" and "What stays unresolved"
- Guard kept: the scope sentence stays the owner's; neither added sentence picks a scope, and no "Changes NOT Being Made" row was applied.

"Answer", before:

> Do not flip the guard before the seeded consumption test (and the other listed prerequisites) has run; the owner writes the scope sentence, "this Run only" or "any Run my terminal holds", after seeing the test and live-layout records.

"Answer", after (one sentence appended):

> ... after seeing the test and live-layout records. Note when choosing: "this Run only" means the pinned Run `run_93bfa00cae2b`, which is an old "Claim issue 375" Run, so the narrow scope would let the panel read only that old Run; the choice between the two scopes stays the owner's.

"What stays unresolved", before:

> The scope sentence itself until W2; consumption on any live Run other than the disposable one OB-04 reads (the test is necessary, not sufficient).

"What stays unresolved", after:

> The scope sentence itself until W2, including whether the narrow scope, which covers only the old pinned Run `run_93bfa00cae2b`, is worth a flip; consumption on any live Run other than the disposable one OB-04 reads (the test is necessary, not sufficient).

### Change 2: a non-circular park fallback when the live lanes cannot run

- Status: applied
- Source: Variant 1 (proposal A), "What happens next" (dated park entry in the ledger); trigger replaced per the plan with the ORCA-AVAILABLE gate wording, not "release 3 is opened"
- Provenance tag: `<!-- Source: Base (original, modified), Change 2 (from Variant 1, proposal A) -->` on "What happens next if the owner picks it"

Before: the section ended with the bullet "If OB-03 shows any seeded message missing, OB-06 stops and the record says "consumes" (`merged-requirements.md:1000`)."

After (new last bullet):

> - If the live lanes cannot run (the Orca app is not reachable, or Q24 or Q30 is not answered), OB-03, OB-04, OB-05 and OB-06 are recorded in the ledger as "parked by owner, Q6, date", with the trigger "the Orca app answers a read verb and Q24 and Q30 are answered" (the ORCA-AVAILABLE gate, `merged-requirements.md:604`).

## Post-Merge Validation

- Heading structure: pass. One H1 and the same five H2 sections in base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). Each section carries one Source comment.
- Internal references resolve: pass. All references in the merged text already appear in the base or in the plan: `merged-requirements.md:254`, `:604`, `:1000`, `:1001`, ADJ line 195, ADJ X-016, OB-03 to OB-06, Q24, Q30, W1, W2, `run_93bfa00cae2b`. No new ids or line numbers were invented.
- Writing rules: pass. No em dashes or en dashes in the merged file.
- New contradictions introduced: 0. Change 1 is consistent with "What it unlocks" (the owner may still choose the narrow scope on evidence). Change 2 is consistent with the third "What it costs or risks" bullet (live tests need Orca reachable and Q24 and Q30 answered) and gives the defined outcome when they are not.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 2 | 2 | 0 | 0 |
