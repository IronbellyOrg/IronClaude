# Merge Log (Q23)

## Metadata

- Base: Variant 3 (proposal-C), `adversarial/variant-3-original.md`
- Plan: `adversarial/refactor-plan.md` (auto-approved 2026-11-14)
- Executor: merge-executor
- Output: `../merged-proposal.md`
- Changes applied: 4 of 4
- Status: SUCCESS
- Timestamp: 2026-11-14

## Changes Applied

### Change 1: observed fixture facts in the mapping row
- Status: APPLIED
- Target: "What happens next", step 1 (append)
- Before: step 1 wrote only the ADJ draft row with "Q23 answered: its own state" and the date.
- After: step 1 adds the plan's text on the fixture (`golden-success.json`, one redacted live worker-list read): 9 reclaimable workers, `workerState: succeeded`, `outcome: succeeded`, `ownershipState: owned`, `releaseState: not_requested`, next action `release`, liveness `unverifiable`; "This is one sample, not Orca's definition."
- Provenance: `<!-- Source: Change 1, Variant 2 advocate (fixture evidence), verified by the orchestrator -->`

### Change 2: named reopen step with an owner and wave
- Status: APPLIED
- Target: "What happens next", step 4 (replace)
- Before: "The question is reopened when Orca's meaning is recorded, for example by adding one line to the shared read-only capture (XC-03)..."
- After: the XC-03 capture session (the session Q24 names, wave W1) adds two read-only items: Orca's help text for terminal states and one `worker-show` detail read of one reclaimable worker, recording whether its session has exited and whether release is automatic or done by a person.
- Provenance: `<!-- Source: Change 2, Variant 3 advocate Concession 3 and Variant 2 advocate concession (replaces base step 4) -->`

### Change 3: what the reopen decides
- Status: APPLIED
- Target: "What it unlocks" (append one bullet)
- Before: last bullet said both later choices stay open at no cost, with no rule for choosing.
- After: new bullet: session exited and release automatic leads to Variant 1 (hide with historical, small observer change); release needs a person leads to Variant 2's wording "not historical: awaiting release", never "live"; either is a separate owner answer.
- Provenance: `<!-- Source: Change 3, Variant 1 and Variant 2 (conditional outcome) -->`

### Change 4: related states and the sweep's different words
- Status: APPLIED
- Target: "What happens next" step 1 (append) and "What stays unresolved" (append two bullets)
- Before: no mention of `release_pending`, `release_unknown`, or the sweep's meanings of "historical" and "settled".
- After: step 1 says the same rule covers `release_pending` and `release_unknown` and that the sweep's "historical" (6 h window) and "settled" (`outcome`, `classify.py:98,114-115`) differ from the observer's terminal-state rule; "What stays unresolved" lists Orca's meaning of the two related states (behaviour UNVERIFIED) and the remaining difference in meaning between the programs.
- Provenance: `<!-- Source: Change 4, Variant 1 ("What stays unresolved", U-001) and Variant 3 advocate Concession 4 -->`

### Consistency edits (required by the changes)
- "What it costs or risks", third bullet: base said "without a trigger it can stay provisional indefinitely". Change 2 names the trigger, so it now says step 4 names who and which wave, and the row stays provisional only if that capture is not run.
- "What it unlocks", first bullet: added "the fixture in step 1 is one sample, not a definition" so Change 1 does not read as a definition.

### Not merged
- The plan's "Out-of-scope observation" (2 `retained` rows with `workerState: ready`) was not merged, as instructed.

## Post-Merge Validation

### Structural
- PASS. One H1 (base title) and the base's five H2 sections in the base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No new headings. Numbered steps 1 to 4 kept.
- PASS. No em dashes or en dashes in the merged file.

### References
- PASS. "step 1" and "step 4" in "What it unlocks" and "What it costs or risks" point at existing steps. "Variant 1" and "Variant 2" match the variant files. Citations kept from base (`view.py:35`, `classify.py:479-481`, ADJ line 258, INV-023) and taken from sources (`classify.py:98,114-115` from Variant 1; fixture path from the plan).

### Contradictions
- PASS. The Answer ("neither program calls it live or historical"), step 2 ("no text calls them live") and Change 3 ("never 'live'") agree. The fixture facts are labelled as one sample, consistent with "Orca's definition is UNVERIFIED". The cost bullet about an indefinite provisional row was updated to match the named reopen step. The sweep-versus-observer difference appears in step 1 and in "What stays unresolved" with the same wording.

## Summary

- Planned: 4
- Applied: 4
- Failed: 0
- Skipped: 0
