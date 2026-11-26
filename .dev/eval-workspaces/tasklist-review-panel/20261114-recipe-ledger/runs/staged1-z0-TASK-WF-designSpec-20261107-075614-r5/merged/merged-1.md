review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /tmp/evalsb-recipe/cand/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r5/normalised/t2b-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r5/normalised/t3-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/runs/staged1-z0-TASK-WF-designSpec-20261107-075614-r5/normalised/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 4.1, 4.6 | t2b-1 |
| L2 | open | no | single | MINOR | 4.4, 4.7 | t2b-1 |
| L3 | open | no | single | MAJOR | - | t3-1 |
| L4 | open | no | single | MAJOR | - | t4-1 |
| L5 | open | no | single | MAJOR | - | t4-1 |
| L6 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): The acceptance test checks n equals 0 but not a negative n, so a wrong build that accepts negative n passes the stated check.
- L2 (MINOR, open, single): The repo-pin wording can be read to include the gh or jq presence check line, which carries no --repo flag.
- L3 (MAJOR, open, single): The plan records the PR-body disclosure as a decision but assigns no task or acceptance check to ensure the actual PR body states the release gate.
- L4 (MAJOR, open, single): The design rejects every n < 1, but the candidate requires a test only for n == 0, so a negative cycle number could violate the contract without failing the stated acceptance checks.
- L5 (MAJOR, open, single): The design requires crash coverage before and after each request and settle; the candidate does not require those individual guard-event crash boundaries to be tested.
- L6 (MAJOR, open, single): The design gives `mode == OFF` precedence for status mapping, but the candidate tests OFF only when there is no guard record, leaving the case of an existing guard record in OFF mode unverified.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
