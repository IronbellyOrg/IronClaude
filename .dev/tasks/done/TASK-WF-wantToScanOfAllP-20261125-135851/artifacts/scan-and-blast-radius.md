# Scan and blast radius: the "dashboard does not replace the coordinator" sentence

Scan run 2026-11-25 (Grep over the main checkout, `gh search` over issues and PRs, transcript search under `~/.claude/projects`). Folder below = `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/` on branch `ironbelly/orch-ledger-20261122` (tracked, 131 files, not on master).

## The contradiction

The owner's 2026-11-22 note in issue 727 says "The ultimate goal is NOT to replace interacting with the coordinator sessions". The owner has since said that is false: the dashboard is meant to replace direct communication with the coordinators, and the note's own 1.8 line (first write and respond features) says so. Issue 727's body is already corrected (2026-11-25, with a dated correction above the unchanged verbatim quote).

A second, related staleness: the issue body and the drafts say issue 726's question "may the read-only rule be relaxed" is open. The owner answered yes in chat on 2026-11-22 (recorded as a comment on 726).

## Where the wrong text lives (needs a change)

| Place | What | Count | Origin |
|---|---|---|---|
| agent1/tools/render.py line 137 | "Before step 1" paragraph in the story template | 1 template, rendered into 73 story drafts | generator |
| agent1/tools/plan_common.py line 28 | `GOAL` constant, "does not replace" | 1 constant, rendered into 1 draft (EPIC-12-STORY-01 Owner goal bullet) | generator |
| agent1/tools/plan_common.py line 10 | `L726` constant, stale "open decision ... relaxed" | 1 constant, rendered into 9 drafts | generator |
| agent1/tools/plan_e01.py line 65 | EPIC-01-STORY-03 done item "decision to relax the read-only rule is recorded ... issue #726 is told" | 1 item, rendered into 1 draft | generator |
| agent1/issue-drafts/*.md | rendered copies | 89 files; 73 carry the sentence; 9 carry the stale 726 text; EPIC drafts (15) and README carry neither | output of render.py |
| agent1/RELEASE-PLAN.md line 69 | "Goal text that every epic must keep" with the wrong sentence and the stale 726 text | 1 paragraph | hand-written |
| .dev/issues/727/issue-body.md | stale local copy of the issue body | 1 file | copy; OWNER-INSTRUCTIONS.md tells agents "Read that file first" |
| PIPELINE-RECORD.md | no entry yet for the correction | add 1 row (the file is append-only; a correction is a new row that names the old one) | record |

Fix order follows the generators: the 73 + 9 drafts are never edited by hand; fix the four generator spots, re-run `uv run python agent1/tools/render.py` (idempotent, overwrites only `agent1/issue-drafts/`), and check the diff.

## Blast radius (what the wrong text would do if left)

- Every one of the 73 story drafts tells the BMAD planner, in the step "Before step 1", that the dashboard does not replace talking to the coordinators. Each BMAD session reads it as a constraint and plans the story under it. Highest risk: EPIC-12 (1.8 write and respond, 8 stories), EPIC-15 (2.0, 5 stories) and EPIC-01 (release 2 prep, 7 stories: the two-way requirements, storage and Postgres, cross-coordinator history). A planner honoring the wrong sentence would keep a terminal-only fallback for conversations the owner wants in the dashboard, shrink the answer-delivery and history requirements, and under-size the database.
- Nothing is filed yet (drafts are on disk only; the owner schedules each release). So nothing needs to be edited on GitHub except issue 727 (done). Cost of fixing now: one regeneration. Cost after filing: 88 live issues to edit.
- RELEASE-PLAN.md line 69 is what a new reader (or the next coordinator) copies as the "goal text that every epic must keep".
- `.dev/issues/727/issue-body.md` is the file the planning agents were told to read first; a coordinator that reads it instead of the live issue gets the old text.
- The 1.8 line also lists a notice that the person is needed in the coordinator session for a q&a or longer conversation. That is the one place direct talking survives in the plan (EPIC-12-STORY-05). It is now an open owner question (in issue 727), not a contradiction; the story gets one added line saying so and its design is not changed.

## Checked and left alone (and why)

- Owner's verbatim text (issue 727 quote, OWNER-INSTRUCTIONS.md, `.dev/issues/727/issue-body.md` quote section): the record of the original note. Not edited; the issue already carries the dated correction above the quote.
- `docs/user-guide/observer.md` and every "read-only" statement about the current observer: true of the code today. Release 1.8 (EPIC-12-STORY-02) already plans to change it.
- Issues 409, 706, 604, 716, 718, 726, 731: no copy of the sentence (GitHub search finds it only in 727). Their read-only wording describes the current product; 706's older "must stay read-only" is already flagged by the backlog review.
- Transcripts, `.dev/tasks/done/**`, `.dev/research/**` and other hits of the broad regex "does not replace": unrelated text.
- Other worktrees and memory files: no copy of the folder or of the issue body.

## Risks of the fix

- PIPELINE-RECORD.md has an uncommitted modification in the main checkout; append one row and keep that modification.
- Re-running render.py overwrites every draft. If any draft was hand-edited after the last render, its edit would be lost; the diff check in the render task catches that.
- The folder is on branch `ironbelly/orch-ledger-20261122`, not on master or on this worktree's branch.
