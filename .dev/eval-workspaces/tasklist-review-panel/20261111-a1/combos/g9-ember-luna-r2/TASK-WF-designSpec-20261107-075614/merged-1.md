review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g9-ember-luna-r2/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g9-ember-luna-r2/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t2b-1, t4-1 |
| L2 | open | no | single | MAJOR | - | t2b-1 |
| L3 | open | no | single | MINOR | - | t2b-1 |
| L4 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Wave 0 bullet must carry no L3 condition yet must contain an at-L3 off-line clause; implementer must guess which reading the test enforces
- anchor: "one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition"

#### L1.t4-1 (F1)

- claim: The Wave 0 bullet must state the L3/off behavior, but its acceptance test is required to fail when the bullet names an L3 condition, so the task's acceptance criteria cannot all pass.
- anchor: "and that at L3 with `--merge-guard off` the line"
- anchor2: "fails when it names an L3 or `draft` condition"

## Other findings

- L2 (MAJOR, open, single): resume_decision re-enters release_decision but has no applied_edits or target_sha to pass, so the release rows cannot be evaluated as specified
- L3 (MINOR, open, single): The ./artifacts base is ambiguous; only the package-relative reading satisfies the Task 13 git-status acceptance
- L4 (MINOR, open, single): Fold acceptance shorthand omits the prior HELD settle that the phase restore depends on

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
