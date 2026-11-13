review: 1 of 3
# Merged review 1 (coordinator script; panel of 5 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/h2-sonnet-luna2-ember2-r3/t1b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/h2-sonnet-luna2-ember2-r3/t4-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/h2-sonnet-luna2-ember2-r3/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/h2-sonnet-luna2-ember2-r3/t2b-1.md, block ok false
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/h2-sonnet-luna2-ember2-r3/t3-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 4.1, 4.2, 5 | t1b-1 |
| L2 | open | no | single | MAJOR | 4.1, 4.2 | t1b-1 |
| L3 | open | no | single | MAJOR | 4.5 | t1b-1 |
| L4 | open | no | single | MINOR | 3, 4.6 | t1b-1 |
| L5 | open | no | single | MINOR | 5 | t1b-1 |
| L6 | open | no | single | MINOR | 4.4 | t1b-1 |
| L7 | open | no | single | MINOR | 10, 7 | t1b-1 |
| L8 | open | yes | single | MAJOR | - | t4-2 |
| L9 | open | no | single | MAJOR | - | t4-2 |
| L10 | open | no | single | MINOR | - | t2b-1 |
| L11 | open | no | single | MAJOR | - | t3-1 |
| L12 | open | no | single | MAJOR | - | t3-1 |
| L13 | open | no | single | MAJOR | - | t3-1 |
| L14 | open | no | single | MAJOR | - | t3-1 |
| L15 | open | no | single | MINOR | - | t3-1 |

## Blocking findings

### L8

#### L8.t4-2 (F1)

- claim: When the timeline is unreadable and the PR is already ready, the specified path can continue pushing and report held while leaving the PR ready.
- anchor: "Timeline unreadable at a checkpoint after engage | Do not release; report `held (timeline unreadable)`; keep pushing."

## Other findings

- L1 (MAJOR, open, single): A guard still held from an earlier cycle is never tied to a later cycle's id, so a resume after a crash in the later cycle can read the earlier cycle's push as published and release a PR whose newer fixes are unpublished.
- L2 (MAJOR, open, single): No criterion covers the user_override fold row (disabled_cause never stated) or mode OFF with a held record, so a wrong guard_status or fold passes Task 3.
- L3 (MAJOR, open, single): The Wave 0 bullet must carry no L3 or draft condition yet must say that at L3 with --merge-guard off a line is printed and that no draft call is made, so a literal test written from the criterion fails the required sentence.
- L4 (MINOR, open, single): The engage trigger is a routed review finding, but a CI-fix cycle has none, so when a CI-fix cycle engages is undefined.
- L5 (MINOR, open, single): The real flow appends push_initiated between fix_applied and push_completed, so an exact-order check can fail a correct driver; the source requires only that the events appear in this order.
- L6 (MINOR, open, single): The exit code for error not_open is not specified, so a test cannot assert it.
- L7 (MINOR, open, single): Comparing against a recorded start text proves only the beginning of each pinned sentence, not that the whole sentence is unchanged.
- L9 (MAJOR, open, single): The fold contract does not explicitly require updating its stored cycle_id on later requests, which can make publication checks use an earlier cycle.
- L10 (MINOR, open, single): The allowed-program rule is stated but no example shows what to do with a fenced line outside that list; following the text still yields a compliant reference file.
- L11 (MAJOR, open, single): Wave 0 bullet must avoid any L3 gate but must state the L3 off case, and the test as worded can fail on the required L3 mention.
- L12 (MAJOR, open, single): Task 7 allows fixture but Task 11 import rule only works with a plain helper; fixture choice breaks scenario imports.
- L13 (MAJOR, open, single): Prefix-only byte-identical check cannot catch suffix edits to the S5a and Wave 6 pinned sentences.
- L14 (MAJOR, open, single): On the current tree with 45 members, literal replay adds duplicate alias members instead of the assumed 43-to-45 edit.
- L15 (MINOR, open, single): Root artifacts path would appear in git status, breaking the allowed-paths acceptance unless package-relative.

## Reviser brief

Blocking finding ids: L8.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
