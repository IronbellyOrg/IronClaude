review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet-src/t4-1.md, block ok true
- t3-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet-src/t3-1.md, block ok true
- t4-2: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet-src/t4-2.md, block ok true
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/r2-sonnet-src/t1b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1 |
| L2 | open | no | overlap | MAJOR | - | t3-1, t4-1 |
| L3 | open | no | overlap | MAJOR | - | t1b-1, t3-1, t4-1 |
| L4 | open | yes | overlap | MAJOR | - | t1b-1, t3-1, t4-1, t4-2 |
| L5 | open | no | overlap | MINOR | - | t3-1, t4-1, t4-2 |
| L6 | open | no | single | MINOR | - | t4-1 |
| L7 | open | no | overlap | MAJOR | - | t1b-1, t3-1 |

## Blocking findings

### L1

#### L1.t4-1 (F1)

- claim: The Wave 0 bullet must name an L3 condition for the off line, but its acceptance test fails any Wave 0 bullet that names an L3 condition.
- anchor: "carries no L3 or `draft` condition; it states that on `--resume`"
- anchor2: "and that at L3 with `--merge-guard off` the line"

#### L1.t3-1 (M4)

- claim: The mandated Wave 0 text names L3 and no draft call, so a bare-word test for L3 or draft cannot pass it.
- anchor: "contains no `L3 only` or `draft` gate wording"
- anchor2: "is printed once and no draft call is made"

#### L1.t1b-1 (F1)

- claim: The Wave 0 bullet must say 'at L3' for the off line while the test must fail when the bullet names an L3 condition, so the stated test can fail on the real file.
- anchor: "carries no L3 or `draft` condition"
- anchor2: "at L3 with `--merge-guard off` the line"

### L4

#### L4.t4-1 (F6)

- claim: read_events returns every event, so an exact-order assertion needs a filter the text does not state.
- anchor: "The acceptance-trace test asserts the exact event order"

#### L4.t4-1 (F8)

- claim: A failed engage gets a release-named phase and an unavailable status, while the exit rule requires held for uncertain work.
- anchor: "`settled(draft, failed)` gives `RELEASE_PENDING`"
- anchor2: "an exit with unpublished or uncertain work leaves the PR draft and reports `held`"

#### L4.t4-1 (F9)

- claim: A guard that never engaged reports released, which reads as if a draft was released.
- anchor: "no record at ordinal 3 (`released`)"

#### L4.t3-1 (F1)

- claim: Engage proceeds on a short timeline although the candidate says an unreadable timeline at engage halts before any edit.
- anchor: "`unreadable` for a failed, incomplete or short timeline"
- anchor2: "The ref states that engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit"

#### L4.t3-1 (M7)

- claim: The repo at HEAD already contains the guard module, script, enum members and SKILL text, and the plan states no precondition check for that.
- anchor: "Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6"

#### L4.t4-2 (F1)

- claim: Resume has no target commit and no edit count, so a published fixing push re-enters release and holds, and the scenario criterion that it releases cannot pass.
- anchor: "resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"
- anchor2: "crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger"

#### L4.t4-2 (F2)

- claim: A failed draft settle leaves ownership false, so every later engage holds and the plan never says whether edits then run on a still-ready pull request.
- anchor: "settled(draft, failed)` gives `RELEASE_PENDING`, increments `failed_mutations` and leaves `owned_draft` unchanged"

#### L4.t4-2 (F3)

- claim: A held guard keeps the first cycle id, so a later cycle's push is not the publication proof resume uses.
- anchor: "held_cycle_published` is true for a normal and for a recovered (`recovered: true`) `push_completed` of the guard's `cycle_id`"

#### L4.t1b-1 (F4)

- claim: Engage row 6 returns HOLD after a failed engage and the plan never maps an engage HOLD to a halt, so an Engage section may edit with the PR still ready.
- anchor: "engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable`"
- anchor2: "(all 11 rows, first match wins, `notes` carries `auto_merge_armed`)"

## Other findings

- L2 (MAJOR, open, overlap): An ambiguous resume reconciliation holds, but the text never says whether the run may edit, push or halt.
- L3 (MAJOR, open, overlap): No decision row counts release attempts, so the one-retry cap has no enforcement and no defined inputs for a later retry.
- L5 (MINOR, open, overlap): git status does not list gitignored .claude mirrors, so the acceptance wording is inaccurate.
- L6 (MINOR, open, single): The grep for 43 will match a non-claim comment in models.py, so the check depends on reading the output.
- L7 (MAJOR, open, overlap): The literal scan would reject the exit-127 check line, so the scan must be limited to gh pr and gh api lines.

## Reviser brief

Blocking finding ids: L1, L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
