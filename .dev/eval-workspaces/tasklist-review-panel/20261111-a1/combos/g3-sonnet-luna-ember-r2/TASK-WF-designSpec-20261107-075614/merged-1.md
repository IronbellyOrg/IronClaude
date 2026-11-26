review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/candidate.md sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- t1b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g3-sonnet-luna-ember-r2/t1b-1.md, block ok true
- t4-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g3-sonnet-luna-ember-r2/t4-1.md, block ok true
- t2b-1: report /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/reviews/combos/g3-sonnet-luna-ember-r2/t2b-1.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L2 | open | yes | overlap | MAJOR | - | t1b-1, t2b-1 |
| L3 | open | no | overlap | MAJOR | - | t1b-1, t2b-1 |
| L4 | open | no | single | MINOR | - | t1b-1 |
| L5 | open | no | overlap | MINOR | - | t1b-1, t2b-1 |
| L6 | open | no | single | MAJOR | - | t4-1 |

## Blocking findings

### L2

#### L2.t1b-1 (F2)

- claim: The engage trigger is a verified Medium-or-higher finding, which a failing CI check is not, and the plan does not say where the ci cycle id is minted.
- anchor: "review-fix cycles and CI-fix cycles; mints the cycle id with `fix_cycle_id` in the single place named by Task 1 O1"
- anchor2: "a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll"

#### L2.t1b-1 (F7)

- claim: No task writes or tests the PR-body gate wording, so the owner decision that the PR body states the gate has no carrier.
- anchor: "the PR body states the gate plainly"

#### L2.t2b-1 (F1)

- claim: Task 10 requires byte-identical proof from start-text-only constants, which cannot pass as written
- anchor: "are asserted byte-identical by comparing the live text with string constants (the literal start text recorded in `./artifacts/pre-build-gate.md`, as the existing pins write them)"
- anchor2: "and the literal start text of the S5a sentence and of the Wave 6 pre-push sentence as the existing pins write them, so later tests can compare against string constants."

## Other findings

- L1 (MAJOR, open, overlap): Row 4 must re-enter release_decision, which needs applied_edits, target_sha and cycle_id, but the stated resume_decision signature supplies none, so resume either never releases after a good push or releases without head proof.
- L3 (MAJOR, open, overlap): The Wave 0 bullet must have no L3 condition yet must say the off notice prints at L3, so a test that rejects any L3 mention would fail the required text.
- L4 (MINOR, open, single): The ref states no protocol outcome for the RETRY_RELEASE and HOLD(ownership_unproven) actions that engage_decision returns.
- L5 (MINOR, open, overlap): The ok value for a timeline-only failure and the exit code for not_open are unspecified, which changes whether engage row 8 is reachable.
- L6 (MAJOR, open, single): The plan does not resolve whether a held guard must appear as `held` in the `merge_guard` output field during off-mode or below-ordinal resume, so that field can report `off` while the PR remains draft.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
