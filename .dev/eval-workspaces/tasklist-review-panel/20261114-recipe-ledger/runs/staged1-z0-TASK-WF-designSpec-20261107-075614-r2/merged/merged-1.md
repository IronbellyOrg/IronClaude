review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r2/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r2/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r2/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | t3-1 |
| L2 | open | yes | single | CRITICAL | - | t4-1 |
| L3 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L2

#### L2.t4-1 (F1)

- claim: An implementer who follows the stated text as written edits only files under src/superclaude/, and that is wrong because required artifact, test, and user-guide changes are outside that directory.
- anchor: "Edit canonical files under `src/superclaude/` only, then run `make sync-dev`;"
- anchor2: "Edit `docs/user-guide/commands.md`:"

## Other findings

- L1 (MAJOR, open, single): The plan does not require scenario tests for crashes before and after each guard request and settle, as the source requires, leaving those resume boundaries untested.
- L3 (MAJOR, open, single): Tasks 9, 10, and 12 consume Task 1's pre-build record but omit it from their dependency lists, contrary to the plan requirement to declare each consumed earlier task.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
