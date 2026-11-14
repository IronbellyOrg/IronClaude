<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->
<!-- Incorporated: Variant 3 (re-ask trigger), Variant 1 (caller-side capture as the later path), advocates' additions; see adversarial/refactor-plan.md and adversarial/merge-log.md -->

# Proposal B (merged): keep both programs separate, joined by one short written contract note

<!-- Source: Base (Variant 2, Answer), unchanged -->
## Answer

Keep the observer and the sweep as two separate programs with no runtime link in version 1, and write one short contract note between them: which file each publishes, what their shared words mean, which Orca commands each may call, and how their rows would be matched. Neither program reads the other and neither gains a file or key.

<!-- Source: Base (Variant 2, What happens next); step 1 clause from Variants 1 and 2 advocates (Change 4); step 4 from Variant 3 and the Variants 2 and 3 advocates (Change 1); step 5 addition from the Variant 1 advocate (Change 3) -->
## What happens next if the owner picks it

1. XC-05: the note `docs/designs/observe-sweep-contract.md` is drafted on a master-based branch (not in the PR #539 checkout), with the registry of contracts, units, versioning rule ("consumers ignore unknown keys"), mapping table of shared words, verb lists per caller, binary resolution, and "candidate join basis" (not "join key") until the real-id comparison is done. The mapping table states each program's stale threshold (45 seconds in the observer's feed, and the sweep's own), because the comparison test guards words, not meanings (`merged-requirements.md:1160`).
2. XC-06: one test compares the note's verb lists, schema versions, join basis and shared words with the two programs' constants and fails if either changes without the note.
3. XC-07: after PR #539 merges and the real-id comparison (XC-04), the note, the test and links from the sweep design and the observer spec merge in one PR opened by the PR session.
4. Once the real-id comparison (XC-04) is recorded, Q17 (an observer panel for sweep facts) is asked once more with its result: whether the observer's dispatch ids match the sweep's row ids. The re-ask does not hold the note.
5. A shared parser is revisited after #539 merges; Q9 and Q17 stay at "not now". The #409 correction pass records this choice, so the live #409 body's "one shared set of facts" proposal (body line 55, read 2026-11-14) does not contradict the owner's answer.

<!-- Source: Base (Variant 2, What it unlocks), unchanged -->
## What it unlocks

- Ends the confusion of two files both called "v1", three vocabularies and two Orca allow-lists that disagree on one command (ADJ Part 1.1).
- Three other planned texts (the Coder#477 status record, the v2 field list, the #409 mapping table) depend on the note (ADJ Part 2.3).
- No code change in either program; no change to the sweep's one-report-per-run rule.

<!-- Source: Base (Variant 2, What it costs or risks); last bullet from Variant 2 advocate concession 3 and Variant 3 advocate concession 2 (Change 5) -->
## What it costs or risks

- The person still sees two views that can classify the same session differently; the note documents the difference, it does not remove it.
- The test compares words and constants, not behaviour; "stale" can mean 45 seconds in one program and 6 hours in the other and still pass (`merged-requirements.md:1160`).
- The note and its test cannot land before PR #539 merges.
- The #409 body's "one shared set of facts" proposal is set aside for version 1.
- The draft may need revising before it lands: the comparison test reads constants that exist only on #539's head. The Q1 ruling is expected to change the git allow-list, not the note's contents (keys, shared words, Orca verbs, join basis), which "Add no JSON keys and no files inside #539" (ADJ line 210) keeps stable.

<!-- Source: Base (Variant 2, What stays unresolved); last bullet from Variant 1 (Change 2) -->
## What stays unresolved

- Whether an observer panel for sweep facts is ever wanted (Q17) and how the sweep JSON would be kept (Q9).
- Whether the candidate join basis holds on real ids (XC-04).
- If Q17 later becomes "yes", the named path is Variant 1's: the panel reads a copy of the sweep JSON captured from the coordinator's at-most-every-5-minutes pass (Q9 caller-side capture) and never runs the sweep itself, because running it writes a report and runs `git status` in every worktree (ADJ Part 8, line 808).
