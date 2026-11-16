review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-k-TASK-WF-designSpec-20261107-075614-r4/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-k-TASK-WF-designSpec-20261107-075614-r4/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-k-TASK-WF-designSpec-20261107-075614-r4/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | t2b-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | single | MAJOR | - | t2b-1 |
| L4 | open | no | single | MINOR | - | t2b-1 |
| L5 | open | no | single | MINOR | - | t2b-1 |
| L6 | open | no | single | MAJOR | - | t3-1 |
| L7 | open | no | single | MAJOR | - | t4-1 |
| L8 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): Task 8 requires the clear command on engage but never the source-required message naming --merge-guard off, and no task test checks it.
- L2 (MAJOR, open, single): Task 7 omits the gh repo view fallback that the _RESOLUTION_SCRIPTS tests require, so an origin-only script fails those tests until the fallback is inferred.
- L3 (MAJOR, open, single): Task 5 does not state the Path form used by neighbouring CORE_PURE_FILES entries, so a literal string entry breaks the purity test.
- L4 (MINOR, open, single): Task 13 does not say package-relative, so a repo-root artifacts path fails its own git-status criterion.
- L5 (MINOR, open, single): The literal Task 2 grep still matches the retained 42nd-43rd comment, so it shows a hit even with no 43-member claim left.
- L6 (MAJOR, open, single): The plan records that the PR body must state the release gate but never requires or checks that the PR body actually does so.
- L7 (MAJOR, open, single): Task 3 does not require a negative-`n` test, so an implementation could accept values that the source contract says must raise.
- L8 (MAJOR, open, single): Task 11 does not require tests for crashes before and after each request and settle, as the source test design requires.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
