<!-- Provenance: merged proposal for Q23 (sc:adversarial Step 5) -->
<!-- Base: Variant 3 (proposal-C) -->
<!-- Incorporated: Variant 2 (2 changes), Variant 1 (2 changes), per adversarial/refactor-plan.md -->
<!-- Merge date: 2026-11-14 -->
<!-- Executor: merge-executor -->

# Proposal C: its own state, shown with Orca's word, until its meaning is known

<!-- Source: Base (Variant 3), unchanged -->
## Answer

`reclaimable` is its own state: neither program calls it live or historical. Readers show Orca's word `reclaimable` as it is, and the contract note records that its side of the line is undecided until Orca's meaning is confirmed.

<!-- Source: Base (Variant 3); step 1 extended by Change 1 (Variant 2 advocate) and Change 4 (Variant 1, Variant 3 advocate Concession 4); step 4 replaced by Change 2 (Variant 3 advocate Concession 3, Variant 2 advocate concession) -->
## What happens next if the owner picks it

1. The contract note draft (XC-05) writes the mapping row ADJ already drafted: "the note decides which side of 'historical' `reclaimable` is (Q23); until then show Orca's word `reclaimable` and do not call it live or historical" (ADJ line 258), with "Q23 answered: its own state" and the date.
   <!-- Source: Change 1, Variant 2 advocate (fixture evidence), verified by the orchestrator -->
   The row adds the observed facts, as observations: "In the observer's recorded fixture (`src/superclaude/cli/observe/fixtures/golden-success.json`, one redacted live worker-list read), all 9 reclaimable workers had a finished task (`workerState: succeeded`, `outcome: succeeded`), resources still held (`ownershipState: owned`, `releaseState: not_requested`), next action `release`, and liveness `unverifiable`. This is one sample, not Orca's definition."
   <!-- Source: Change 4, Variant 1 ("What stays unresolved", U-001) and Variant 3 advocate Concession 4 -->
   The row also says that the same "own state, Orca's word" rule covers `release_pending` and `release_unknown`, and that the sweep's "historical" (its 6 h window) and "settled" (from `outcome`, `classify.py:98,114-115`) are different measures from the observer's terminal-state rule.
2. No code change now. The observer keeps reclaimable rows in its default view (`view.py:35`), but no text calls them live; the sweep keeps "could not determine" for safe-to-close (`classify.py:479-481`).
3. OB-06 prerequisite (e) is met by the row in the note draft or the observer spec.
   <!-- Source: Change 2, Variant 3 advocate Concession 3 and Variant 2 advocate concession (replaces base step 4) -->
4. Reopen step: the session that runs the shared read-only capture (XC-03; the session Q24 names, wave W1) adds two read-only items: Orca's help text for terminal states, and one detail read (`worker-show`) of one reclaimable worker, recording whether its session has exited and whether release is automatic or done by a person. The question is reopened when that capture is recorded.

<!-- Source: Base (Variant 3); last bullet added by Change 3 (Variant 1 and Variant 2, conditional outcome) -->
## What it unlocks

- OB-06 and XC-05 proceed now without deciding a meaning nobody has confirmed (Orca's definition is UNVERIFIED in every file read; the fixture in step 1 is one sample, not a definition).
- No code change and no wrong claim: a person sees the exact word Orca uses.
- Leaves both later choices open (hide it as historical, or keep it as awaiting release) at no cost.
  <!-- Source: Change 3, Variant 1 and Variant 2 (conditional outcome) -->
- The step 4 capture decides between them. If it shows the session has exited and release is automatic, the follow-up is Variant 1 (hide it with the historical states, a small observer change); if release needs a person, the follow-up is Variant 2's wording "not historical: awaiting release", never "live". Either follow-up is a separate owner answer.

<!-- Source: Base (Variant 3); third bullet updated for consistency with Change 2 -->
## What it costs or risks

- The observer's default view is unchanged, so it can still be filled with finished workers (27 reclaimable, 0 active at the probe, INV-023); "its own state" names the problem without fixing it.
- "Its own state" is a non-answer to a reader who asks "is this worker still running?"; the meaning is deferred, not settled.
  <!-- Source: Base (Variant 3), reworded because Change 2 now names the trigger -->
- A provisional row needs someone to revisit it. Step 4 names who adds the capture items and in which wave, but if that capture is not run, the row stays provisional.

<!-- Source: Base (Variant 3); items 2 and 3 added by Change 4 (Variant 1 U-001, Variant 3 advocate Concession 4) -->
## What stays unresolved

- Which side of "historical" `reclaimable` belongs on, and Orca's own definition.
  <!-- Source: Change 4, Variant 1 ("What stays unresolved") -->
- Orca's meaning of `release_pending` and `release_unknown` (listed in `worker-list --help`, behaviour UNVERIFIED); until it is known they follow the same rule as `reclaimable`.
  <!-- Source: Change 4, Variant 1 (U-001) -->
- The sweep's "historical" (6 h window) and "settled" (`outcome`) still differ from the observer's terminal-state rule whatever Q23 answers; the note states the difference but does not remove it.
