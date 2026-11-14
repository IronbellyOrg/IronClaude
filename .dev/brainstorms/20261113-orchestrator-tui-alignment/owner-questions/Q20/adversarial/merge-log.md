# Merge Log: Q20 (base Variant 2, proposal-B)

## Metadata

- Base: Variant 2 (proposal-B.md, identical to adversarial/variant-2-original.md)
- Plan: adversarial/refactor-plan.md (6 planned changes, risk Low, approved auto 2026-11-14)
- Output: merged-proposal.md
- Merge date: 2026-11-14
- Executor: merge-executor (Step 5)
- Planned changes applied: 6 of 6
- Consistency edits beyond the plan: 2 (listed below)

## Changes Applied

### Change 1: Cleanup rule gates the schedule, not FU-1

- Status: Applied
- Source: Variant 1 (proposal-A) "What happens next" bullet 4 (U-001); round1-advocate-1.md, -2.md, -3.md
- Target: "What happens next if the owner picks it", appended bullet
- Before: (no such bullet)
- After: "Before the watcher's schedule is enabled (WA-05), a written rule says who closes watcher sessions and by when. FU-1 itself launches one session on one test issue (merged-requirements.md line 306), so it does not wait for that rule."
- Provenance tag: `Variant 1 (proposal-A) "What happens next" bullet 4 (U-001) with advocate findings, merged per Change #1`
- Validation: Text matches the plan verbatim. Consistent with the base FU-1 bullet (line 306 citation already in base and plan).

### Change 2: The confirmed day cap

- Status: Applied
- Source: round1-advocate-1.md and -2.md, A-001
- Target: "Answer" (wording refinement) and "What happens next" (appended bullet)
- Before: "Yes, that one worktree may hold up to 6 watcher sessions a day; ..."
- After: "Yes, that one worktree may hold up to the confirmed day cap of watcher sessions a day (default 6); ..." plus the new bullet "The day cap is a code constant (`DAY_CAP = 6`) that the design lists as a proposal for you to confirm after the shadow run; lowering it is a small code change, not a configuration edit."
- Provenance tags: `Base (original, modified); reason: day-cap wording replaced, merged per Change #2` on "Answer"; `Advocate findings A-001 (...), merged per Change #2` on the new bullet
- Validation: Replacement string found once and replaced. The plan's source citations (cycle.py lines 33 and 36, issue-watcher-setup.md line 238) are not in the plan's integration text, so none were added to the document.

### Change 3: Review cadence and absence fallback

- Status: Applied
- Source: round1-advocate-2.md "Concessions"; round1-advocate-3.md "Overall"
- Target: "What happens next", ledger bullet (extended)
- Before: "The ledger records "Q20: ..." with the date."
- After: same sentence, then "The ledger also records how often that person looks at the open sessions, and either a named substitute or the rule that the schedule is disabled while the owner is away."
- Provenance tag: `Base (original, modified); reason: review cadence and absence fallback appended from advocate findings (...), merged per Change #3`
- Validation: Text matches the plan verbatim.

### Change 4: What "owns" covers

- Status: Applied
- Source: round1-advocate-1.md "Strengths claimed" 3
- Target: "What it costs or risks", first bullet (extended)
- Before: bullet ended "...; the named person must close them by hand."
- After: appended "Orca's creator rule covers the agent made when the worktree is created; the watcher starts later sessions itself, so the named person is their owner by this decision and their reviewer, not by Orca's record (whether Orca attributes them to the creator is UNVERIFIED). The runbook gives no command to end a running session; it is closed by hand in Orca."
- Provenance tag: shared with consistency edit C-1 on the same bullet (see below)
- Validation: Text matches the plan verbatim. The UNVERIFIED marker is kept.

### Change 5: Read-only count in the coordinator's check

- Status: Applied
- Source: Variant 3 (proposal-C) "What happens next" bullet 3 (U-003); round1-advocate-2.md "Concessions"
- Target: "What it unlocks", appended bullet
- Before: (no such bullet)
- After: "Optionally, the coordinator's recurring check may report a read-only count of open sessions in `issue-watch`, without reading their transcripts and without owning them, so the named person gets a reminder."
- Provenance tag: `Variant 3 (proposal-C) "What happens next" bullet 3 (U-003), narrow form, merged per Change #5`
- Validation: Text matches the plan verbatim. Does not imply ownership; consistent with "Answer" (never owned by a coordinator) and the base "never" adoption bullet.

### Change 6: Second-agent ownership if Q2 keeps the default

- Status: Applied
- Source: all three advocates, A-002
- Target: "What stays unresolved", appended bullet
- Before: (no such bullet)
- After: "If Q2 keeps the default claim level, each claim also starts a second agent in its own `issue-<N>` worktree; you would also name who owns those agents. Under Q2's recommended `--pipeline none` there is no second agent."
- Provenance tag: `Advocate findings A-002 (all three advocates), merged per Change #6`
- Validation: Text matches the plan verbatim.

## Consistency edits

| ID | Location | Before | After | Reason | Tag |
|---|---|---|---|---|---|
| C-1 | "What it costs or risks", bullet 1 | "Up to 6 sessions a day accumulate in one worktree and "nothing closes or reaps those sessions" (round2-rebuttal-V2.md line 91)" | "Up to the day cap (default 6) of sessions a day accumulate in one worktree and, by the watcher's design, "nothing closes or reaps those sessions" (round2-rebuttal-V2.md line 91)" | "Up to 6" contradicted Change 2's confirmable cap; the bare quote "nothing closes" contradicted Change 1 (a written closing rule) and Change 4 (closed by hand in Orca). The quote itself is unchanged; only its scope is stated. | Base (original, modified); reason: consistency with Change #2 and with Change #1 and Change #4 |
| C-2 | "What stays unresolved", bullet 1 | "Who closes or reaps watcher sessions, and when." | "Who closes or reaps watcher sessions, and when; that rule must be written before the schedule is enabled (WA-05)." | After Change 1 the open question has a deadline; the bare bullet read as having none. | Base (original, modified); reason: consistency with Change #1 |

Reviewed and left unchanged (no contradiction found):

- "What it unlocks" bullet 1 ("...then its schedule (WA-05)"): still true; Change 1 adds a precondition, it does not withdraw the unlock.
- "What it unlocks" bullet 2 ("a worktree's creator owns its agent"): speaks of the creation agent only, which Change 4 confirms.
- "What happens next" FU-1 bullet (line 306): consistent with Change 1 ("FU-1 ... does not wait for that rule").
- "What it costs or risks" bullet 2 (observer cannot see the sessions): Change 5 is a count of open sessions in the worktree, not observer visibility; no contradiction.
- "What it costs or risks" bullet 3 and "What stays unresolved" bullet 2 ("never"): consistent with Changes 3 and 5.
- Title and "Answer" ownership sentences: consistent with Change 4 (owner by this decision).

## Post-Merge Validation

- Heading hierarchy: one H1 (title), five H2 sections in base order (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved). No skipped levels. Pass.
- Internal references: WA-02, WA-03, WA-04, WA-05, FU-1, Q2, Q21, WC-13 and #450 all appear in the base or the plan. File citations (merged-requirements.md lines 304, 305, 306; variant-2-original.md line 48; round2-rebuttal-V2.md line 91; ADJ line 242) all come from the base or the plan; no new line numbers added. Pass.
- Remaining "up to 6" wording: none; both occurrences of 6 are "(default 6)" or `DAY_CAP = 6`. Pass.
- Remaining unscoped "nothing closes" wording: none. Pass.
- Em dashes and en dashes: none. Pass.
- Provenance: header comments present; a Source tag precedes every section and every changed or added block. Pass.
- Content outside the plan: none beyond consistency edits C-1 and C-2. Pass.

## Summary

All 6 planned changes were applied as the plan specifies. Two minimal consistency edits (C-1, C-2) align unchanged base sentences with Changes 1, 2 and 4. Structure, citations and the base's five sections are intact. Status: success.
