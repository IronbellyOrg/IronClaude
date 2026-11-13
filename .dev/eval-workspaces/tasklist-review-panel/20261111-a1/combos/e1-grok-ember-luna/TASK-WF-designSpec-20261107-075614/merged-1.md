review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/e1-grok-ember-luna/t4-2.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/e1-grok-ember-luna/t2b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/e1-grok-ember-luna/t4-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | t4-2 |
| L2 | open | yes | single | MAJOR | - | t4-2 |
| L3 | open | no | single | MAJOR | - | t4-2 |
| L4 | open | no | overlap | MAJOR | - | t2b-1, t4-2 |
| L5 | open | no | single | MAJOR | - | t2b-1 |
| L6 | open | no | single | MINOR | - | t2b-1 |

## Blocking findings

### L1

#### L1.t4-2 (F1)

- claim: The origin-resolution fallback line has no --repo, so the static check fails, and adding --repo stops the fallback from discovering the repo.
- anchor: "asserts every `gh` line carries `--repo` or a `repos/` path"
- anchor2: "the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests"

### L2

#### L2.t4-2 (F2)

- claim: Resume has no target_sha and no edit count, so a confirmed fix push cannot take the release row, and Task 11's release check cannot pass without skipping the head proof.
- anchor: "`resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`"
- anchor2: "crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger"

#### L2.t4-2 (F5)

- claim: A landed call that was settled failed makes the observed count miss the exact reconcile match, so resume holds instead of confirming.
- anchor: "`resume_reconciled` (live state matches the request and observed equals `run_toggles + 1`)"
- anchor2: "`ok` when observed equals `run_toggles + failed_mutations`"

## Other findings

- L3 (MAJOR, open, single): A landed CI-fix crash is told both to run the review re-trigger and to return to the CI poll, and the plan never says which wins.
- L4 (MAJOR, open, overlap): The Wave 0 bullet must contain the level-3 off sentence, and one reading of its test rejects any level-3 condition.
- L5 (MAJOR, open, single): Task 2 grep acceptance is ambiguous against the existing 42nd-43rd comment, so an implementer must guess whether zero hits or no claim is required.
- L6 (MINOR, open, single): The candidate never names the package folder on disk, so the artifacts path is not self-contained.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
