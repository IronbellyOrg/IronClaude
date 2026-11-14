# Merge Log (Q21)

## Metadata

- Base: Variant 2 (proposal-B), `adversarial/variant-2-original.md`
- Plan: `adversarial/refactor-plan.md`
- Executor: merge-executor
- Output: `../merged-proposal.md`
- Changes applied: 4 of 4
- Status: complete; validation passed, with one wording tension noted for the orchestrator
- Timestamp: 2026-11-14

## Changes Applied

### Change 1: watcher store as the fallback signal, not a new input now

- Status: applied
- Target: step 3 of "What happens next if the owner picks it", and "What stays unresolved"
- Before: step 3 ended with "SW-10 records "no reliable signal" and stops; the label is not guessed." "What stays unresolved" had two bullets (D-B, D-A).
- After: step 3 adds that the reopen option is a label from the watcher's versioned store `dispatch.json` (`operation_id`, `launch_cwd`, checked `schema_version`: `record.py:69-95`), needing its own owner approval of a file read; not `status --json` (`cycle.py:1308-1323`); no worktree-path fallback. "What stays unresolved" gains a third bullet: whether the owner approves reading `dispatch.json` if FU-1 shows no usable signal.
- Provenance: `<!-- Source: Change 1 (Variant 1, Answer; round1-advocate-V1.md Strength 1 and Concession 1) -->`

### Change 2: document the blind spot now

- Status: applied
- Target: step 1
- Before: step 1 ended with the SW-06 follow-up row and its trigger "after FU-1".
- After: step 1 appends that, until SW-10 lands, the sweep design and the contract-note draft (XC-05) say a Run-less session may have been started by the watcher and the sweep cannot tell (ADJ lines 227, 242). The name "XC-05" for the contract-note draft is taken from Variant 3 step 2.
- Provenance: `<!-- Source: Base (Variant 2) + Change 2 (Variant 3, step 2) -->`

### Change 3: guard against a signal that holds on one row and drifts later

- Status: applied
- Target: step 3
- Before: step 3 described the fixture test only for a watcher-launched session not being labelled person-started.
- After: step 3 adds that the label may only move a row from "unknown" to "machine-started"; a row with a missing or unrecognised signal stays "could not determine", never person-started; the fixture test also covers an empty `prompt`.
- Provenance: `<!-- Source: ... Change 3 (Variant 3, round1-advocate-V3.md Weaknesses 1 and 2) ... -->`

### Change 4: WA-07 dependency note

- Status: applied
- Target: "What it unlocks"
- Before: three bullets (SW-10 and WA-07 gate; readers can tell sessions apart; no allow-list widening).
- After: a fourth bullet: if SW-10 ends in "no reliable signal", WA-07 item (3) uses its other route ("bound to a Run", merged-requirements.md line 309); the dependency row is updated then. The line 309 citation is carried from Variant 3 step 4.
- Provenance: `<!-- Source: Change 4 (Variant 3, round1-advocate-V3.md Concession 1; route wording from Variant 3 step 4) -->`

## Post-Merge Validation

### Structural

- Pass. One H1 (the base title, unchanged) and the base's five H2 sections in the base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No heading levels skipped. Numbered steps stay 1 to 4.
- Provenance header comments present (Base: Variant 2 (proposal-B); merge date 2026-11-14), plus one `<!-- Source: ... -->` comment per section and per changed block.
- No em dashes or en dashes in the merged file (checked by search).

### References

- Pass. The new internal reference "(step 3)" in "What stays unresolved" points to step 3, which holds the `dispatch.json` fallback.
- All base citations kept (merged-requirements.md line 306, ADJ lines 162 and 714, dependency row 74, `src/superclaude/cli/sweep/probes.py:55`, A-009, WC-16). New citations come only from the plan or the variants: `record.py:69-95`, `cycle.py:1308-1323` (plan Change 1), ADJ lines 227 and 242 (plan Change 2, Variant 3), merged-requirements.md line 309 (Variant 3). These were carried as given and not re-checked against source files.

### Contradictions

- Pass: no direct contradiction introduced. The rejected options stay out: the allow-list is not widened now (the `dispatch.json` read is stated as a separate future owner approval, consistent with "No widening of the allow-list"), there is no worktree-path fallback, and the label is not deferred to SW-13.
- Wording tension noted, not resolved (outside the plan): Change 3 says a row with a missing or unrecognised signal stays "could not determine", never person-started, while the base cost bullet still says "A false negative (a watcher session still shown as a person's) stays possible". The two read consistently if "never person-started" limits what the new label asserts and the cost bullet describes the sweep's existing display of Run-less sessions. If the orchestrator intends "could not determine" to replace that display, the cost bullet needs a planned edit.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 4 | 4 | 0 | 0 |
