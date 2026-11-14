# Q21: may the sweep label machine-started sessions separately?

## The question, verbatim

Spec row (merged-requirements.md section 3, line 548): "May the sweep label machine-started sessions separately?"

Original wording (ADJ Part 7, line 791): "May the sweep label machine-started sessions separately from person-started ones, reading `worktree ps` agent rows (`prompt`, `paneKey`)?"

## Spec's recommended answer

"Yes, in Phase 2, only after FU-1 shows what the rows hold (D-B)." (merged-requirements.md line 548; ADJ line 791.)

Plain meaning: yes, but only in the sweep's second phase, and only after the issue watcher's first live test (FU-1) has recorded what Orca's `worktree ps` agent rows actually contain for a session the watcher started (open item D-B).

## Default if unanswered

"PLAN INFERENCE: SW-10 does not start" (merged-requirements.md line 548). PLAN INFERENCE means the spec derived this rule; no debate file states it.

## What it gates

- SW-10 (merged-requirements.md line 199): "Label machine-started sessions in the sweep (Phase 2)". Done when: a row exists for it in the follow-up table of issue #534 (work item SW-06); the label reads `worktree ps` agent rows (`prompt`, `paneKey`) only in the shape FU-1 recorded; a test with the FU-1 fixture shows a watcher-launched session is not labelled person-started; no new Orca command outside the owner-signed allow-list (NFR-014) unless the owner signs a new one; the PR is opened by the PR session under its own permission row. Depends on SW-05 (PR #539 merged), SW-06, WA-04 (FU-1 recorded), Q21, Q25.
- Through SW-10, WA-07 (line 309), the deferred handoff from the watcher to an orchestrator: its item (3) needs "a handed-off session is visible to the sweep as a labelled row (SW-10) or bound to a Run". Dependency table row 74 (line 721): SW-13, SW-12, SW-10 must be done before WA-07.
- Wave needed by: W4, "Phase 2 starts" (line 864), whose entry needs WA-04 recorded and SW-05 merged.

## Facts the question depends on

| Fact | Source |
|---|---|
| A session the watcher starts is Run-less (not attached to any Orca Run); today the sweep prints `could not determine` for it, later possibly "person session (active)" | ADJ line 373, row X-003, 78 percent; code cited `classify.py:302-315,748-767` |
| Read in this checkout: `_rule_person_active` (classify.py:302) labels a row "person_active" when `person_started is True` and the transcript is recent; `_person_origin` (classify.py:748-767) returns `True` with the note "origin not proved" when no join problem is found | `src/superclaude/cli/sweep/classify.py` read on 2026-11-13 (PR #539 head, this checkout) |
| The firm claim "a watcher session will be mislabelled person-started" was withdrawn: it depended on a join V2 did not run; `prompt` was empty or not a slash command on all 27 live agent rows seen | ADJ line 162 (withdrawn findings table) |
| D-B, unresolved: "does the agent row's `prompt` hold the claim? Settled by one `worktree ps --json` agent row after the launch" | ADJ line 493 (Part 5.3) |
| FU-1 (work item WA-04) records item (e): one `worktree ps --json` agent row after the launch, whether `prompt` holds `/sc:issue --claim N` and whether `paneKey` equals a tab-map name | merged-requirements.md line 306 |
| Sessions with no Run (watcher-launched, person-started) are not observable by either program today | ADJ lines 227, 242 (A-008) |
| The watcher records only an Orca operation id for what it launches; whether `agent launch` creates a Run is unknown (D-A) | merged-requirements.md line 128 |
| The sweep's `SessionRow` has a `person_started` field (true, false or unknown) and no "machine-started" field | `src/superclaude/cli/sweep/models.py:150-152` read on 2026-11-13 |
| The sweep may run only the owner-signed list of Orca and git commands (NFR-014) | ADJ line 84 |
| The watcher-to-orchestrator handoff (L1) is NOT BUILT; WA-07 is DEFERRED | merged-requirements.md lines 93, 128 |
| ADJ decision note: "[Decision: Q21 (yes, Phase 2, after FU-1). Waits for: FU-1. Unblocks: the label in #534. Undo: yes.]" | ADJ line 274 |
