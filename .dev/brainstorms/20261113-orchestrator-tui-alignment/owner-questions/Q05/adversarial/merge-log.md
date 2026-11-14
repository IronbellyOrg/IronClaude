# Merge Log: Q5

## Metadata

- Base: Variant 2 (proposal-B), `adversarial/variant-2-original.md`
- Plan: `adversarial/refactor-plan.md` (5 planned changes, overall risk Low, auto-approved 2026-11-14)
- Incorporated sources: `adversarial/variant-1-original.md`, `adversarial/variant-3-original.md`, advocates' additions in `adversarial/debate-transcript.md`
- Context read: `adversarial/debate-transcript.md`, `question.md`
- Output: `merged-proposal.md`
- Merge date: 2026-11-14
- Executor: merge-executor (sc-adversarial-protocol Step 5)

## Changes Applied

### Change 1: re-ask Q17 once the real-id comparison is recorded

- Status: APPLIED
- Before: "What happens next" had four steps; nothing tied Q17 to the result of XC-04.
- After: new step 4 after base step 3: once XC-04 is recorded, Q17 is asked once more with its result (whether the observer's dispatch ids match the sweep's row ids); the re-ask does not hold the note. Base step 4 is renumbered 5.
- Provenance: Variant 3 (U-003, its step 3 trigger); Variants 2 and 3 advocates (debate transcript, "Additions proposed by more than one advocate").
- Validation: insert only; base steps 1 to 3 unchanged in meaning. The note's landing (step 3) is not made to wait on the re-ask.

### Change 2: name the later path if Q17 becomes "yes"

- Status: APPLIED
- Before: "What stays unresolved" listed Q17 and Q9 and the XC-04 join basis, with no named path.
- After: appended bullet: if Q17 later becomes "yes", the panel reads a copy captured from the coordinator's at-most-every-5-minutes pass (Q9 caller-side capture) and never runs the sweep, because running it writes a report and runs `git status` in every worktree (ADJ Part 8, line 808).
- Provenance: Variant 1 (U-001, its step 1 and Answer); Variants 1 and 2 advocates.
- Validation: append only; framed as a later path conditional on an owner answer, not as something that exists. Citation matches the plan and `question.md` (Part 8 row X-013, line 808).

### Change 3: the #409 correction pass records the choice

- Status: APPLIED
- Before: base step 4: "A shared parser is revisited after #539 merges; Q9 and Q17 stay at 'not now'."
- After: same text, now step 5 after the Change 1 insert, with an appended sentence: the #409 correction pass records this choice so the live #409 body's "one shared set of facts" proposal (body line 55, read 2026-11-14) does not contradict the owner's answer.
- Provenance: Variant 1 advocate (debate transcript, additions); source fact from `question.md` (`gh issue view 409`, body line 55).
- Validation: append only. The plan targets "step 4"; after Change 1 that step is numbered 5. Same step, renumbered only.

### Change 4: the mapping table states each program's stale threshold

- Status: APPLIED
- Before: step 1 listed the note's contents without thresholds.
- After: appended clause: the mapping table states each program's stale threshold (45 seconds in the observer's feed, and the sweep's own), because the comparison test guards words, not meanings (`merged-requirements.md:1160`).
- Provenance: Variants 1 and 2 advocates (debate transcript, additions); `merged-requirements.md:1160`.
- Validation: append clause only. The sweep's threshold is described as "the sweep's own" as in the transcript; no new value is stated in step 1. The 6-hour example stays in the base's costs bullet, as cited there.

### Change 5: the draft may need revising before it lands

- Status: APPLIED
- Before: "What it costs or risks" had four bullets.
- After: appended fifth bullet: the comparison test reads constants that exist only on #539's head; the Q1 ruling is expected to change the git allow-list, not the note's contents (keys, shared words, Orca verbs, join basis), which "Add no JSON keys and no files inside #539" (ADJ line 210) keeps stable.
- Provenance: Variant 2 advocate concession 3; Variant 3 advocate concession 2 (debate transcript, Round 1).
- Validation: append only; wording follows the plan's rationale and the transcript; citation ADJ line 210 as in the plan and transcript.

## Post-Merge Validation

### Structural integrity

- PASS. One H1 title and five H2 sections in the base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved.
- PASS. Provenance header comments present (Provenance, Base, Merge date) and one `<!-- Source: ... -->` comment on each of the five sections.
- PASS. Numbered list in "What happens next" runs 1 to 5 with no gaps.

### Internal references

- PASS. Every id and citation in the merged text appears in the base, the plan, a variant, the transcript or `question.md`: XC-04, XC-05, XC-06, XC-07, Q1, Q9, Q17, PR #539, #409 body line 55, Coder#477, ADJ Part 1.1, ADJ Part 2.3, ADJ Part 8 line 808, ADJ line 210, `merged-requirements.md:1160`, `docs/designs/observe-sweep-contract.md`.
- No new facts, ids, paths or line numbers were introduced.

### New contradictions

- None found. The Answer is unchanged: keep both programs, one contract note, no runtime link in version 1.
- Checked: step 5 says Q9 and Q17 stay at "not now", while step 4 re-asks Q17 after XC-04. Compatible: the recorded answer stays "not now" unless the re-ask changes it.
- Checked: the Change 2 bullet describes a conditional later path only; the merged text does not claim an orchestrator that manages work, a watcher-to-orchestrator handoff, the v2 knowledge layer or a TUI decision loop exists.
- Checked: no em dashes or en dashes in either output file.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 5 | 5 | 0 | 0 |
