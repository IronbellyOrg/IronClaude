review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n5-sonnet-ember/t2b-1.md, block ok false
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n5-sonnet-ember/t4-1.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/n5-sonnet-ember/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L3 | open | no | single | MAJOR | - | t2b-1 |
| L4 | open | yes | overlap | CRITICAL | - | t1b-1, t2b-1, t4-1 |
| L5 | open | no | single | MINOR | - | t1b-1 |
| L6 | open | no | single | MINOR | - | t1b-1 |

## Blocking findings

### L4

#### L4.t2b-1 (F4)

- claim: Wave 0 bullet must state the L3 offline line yet must not name an L3 condition.
- anchor: "it states that on `--resume`, or when the run log already holds guard events, the ref `refs/merge-guard.md` (Resume and Exit report) is loaded before Wave 1"

#### L4.t4-1 (F1)

- claim: The Wave 0 bullet must state the L3/off behavior, while its acceptance test is required to fail when the bullet names an L3 condition.
- anchor: "at L3 with `--merge-guard off` the line \"Remediation is unprotected: --merge-guard off.\" is printed once"
- anchor2: "fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition"

#### L4.t1b-1 (F2)

- claim: The Wave 0 test is worded to fail on any L3 mention, yet the required bullet text itself says 'at L3 with --merge-guard off'.
- anchor: "when it names an L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line"

## Other findings

- L1 (MAJOR, open, overlap): Resume cannot re-enter release because applied edits, target sha and cycle id have no stated source.
- L2 (MAJOR, open, overlap): Helper-or-fixture import is ambiguous; a pytest fixture is not callable as a helper.
- L3 (MAJOR, open, single): Command task omits git write verbs that the constraint list requires.
- L5 (MINOR, open, single): A draft_guard_unavailable halt after a failed first read leaves no guard record, so guard_status returns released and no task tests the override to unavailable.
- L6 (MINOR, open, single): Constants hold only the literal start text of the two pinned sentences, so the check cannot prove whole-sentence byte identity.

## Reviser brief

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
