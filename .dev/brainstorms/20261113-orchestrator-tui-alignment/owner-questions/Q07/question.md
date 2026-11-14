# Q7: owner authorship of the pass record, and saving the records that exist only in the sibling worktree

## The question, verbatim from the spec row

Source: `merged-requirements.md:534` (section 3, "Owner decisions").

> | Q7 | Will the owner write the pass record and commit or archive the sibling-only records? | Yes, both, before the sibling worktree is cleaned | PLAN INFERENCE: OB-06 cannot open (its (d) fails); `issue-409-mvp` must not be cleaned | OB-01, OB-06 | W1 |

Original wording (ADJ Part 7, `alignment-findings-adjudicated.md:777`): "Will you write the pass record yourself (git cannot show who typed it) and commit or archive the records that exist only in the sibling worktree (`owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`)?"

## Spec's recommended answer

"Yes, both, before that worktree is cleaned" (ADJ:777; `merged-requirements.md:534`).

## Default if unanswered

PLAN INFERENCE (a point the spec derived, not stated by a debate file): OB-06 cannot open because its prerequisite (d), "the owner-written pass record is committed in this PR", fails; the sibling worktree `issue-409-mvp` must not be cleaned (`merged-requirements.md:534`).

## What it gates (work items, in words)

- OB-01, the owner commits or archives the sibling-only records: `owner-decisions-20261108.md`, the 2026-11-12 record, `live-test-guide.md` and `tuibbs-review/` are on master or in a named archive the owner chose, done before the sibling is cleaned, and the owner (not an agent) is the author of the pass record (`merged-requirements.md:249`). OB-01 also blocks OB-08, the #409 issue-body correction pass.
- OB-06, the switch-on pull request for the observer's questions read; prerequisite (d) commits the owner-written pass record in that PR (`merged-requirements.md:254`).
- Wave W1 (the first batch of work after the intake questions).

## Facts the question depends on

| Fact | Source |
|---|---|
| Only `owner-decisions-20261111.md` of the owner's 409 records is on master; the 2026-11-08 and 2026-11-12 records, the pass record, `live-test-guide.md` and `tuibbs-review/` are untracked or in unpushed commits in the sibling | ADJ E-16 (line 142), A-015 (line 328), INV-002 (line 457) |
| Re-checked 2026-11-14 (read-only `git status`, `git log`): in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp` the untracked files are `handoff-mvp-brainstorm.md`, `live-test-guide.md`, `owner-decisions-20261108.md` and `tuibbs-review/`; `owner-pass-record-20261112.md` and `owner-decisions-20261112.md` exist only in local commits `1ae72e1a1` and `f104ca51a`; no remote branch contains those commits and `409-Phase2` is absent on the remote | this worker's read on 2026-11-14 |
| `handoff-mvp-brainstorm.md` is also untracked in the sibling but is not named by the spec or ADJ | this worker's read on 2026-11-14 |
| The pass record file exists and its first lines say "Written by the owner."; git cannot show who typed it | sibling `owner-pass-record-20261112.md` lines 1-3; ADJ INV-014 (line 478) |
| `origin/master` is not an ancestor of the sibling HEAD, so a fresh master-based branch is needed for any commit | ADJ E-02 (line 128); `merged-requirements.md:234`, `:249` |
| Rule for owner records: "agents may cite, never write it" (stated for the direction-selection record) | sibling `.dev/issues/409/bmad/spec-orca-observer/release-gates.md:22` |
| Cleaning the sibling before OB-01 deletes records the flip PR must cite | `merged-requirements.md:264` |
