review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | MAJOR | - | R1 |
| L2 | open | yes | single | MAJOR | - | R1 |
| L3 | open | yes | overlap | MAJOR | - | R1, R3, R2 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MINOR | - | R1 |
| L7 | open | yes | single | MAJOR | - | R3 |
| L8 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Warning field cannot hold W-ORIGIN-BASE-STALE or W-WORKTREE-COPY-FAILED on created or reused results.
- anchor: "The warning field holds the one code that set the status; any other problem goes in `detail`."
- anchor2: "a failed `git fetch origin` with the ref present continues with warning `W-ORIGIN-BASE-STALE`"

#### L1.t2b-1 (F6)

- claim: A single new non-matching row has no status, warning, or test case.
- anchor: "exactly one new row whose basename matches the issue pattern is `created`"

### L2

#### L2.t2b-1 (F2)

- claim: Task 8 requires the folder yet no task copies or creates it and it is absent on disk.
- anchor: "already copied into this repository and part of the change"
- anchor2: "The folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` exists with `merged-requirements.md`, `launch-levels-addendum.md`, `seed-brief.md`, `adversarial/` and `enrichment/`"

### L3

#### L3.t2b-1 (F3)

- claim: Timeout detail omits the source rule to check Orca before re-running.
- anchor: "a nonzero exit, timeout or `ok` not true removes the launch record, returns `failed` with `W-LAUNCH-FAILED`, the first stderr line and a `hand_command`"

#### L3.t3-1 (F2)

- claim: An implementer who follows the stated text as written builds a failure response that offers the same launch call without the marker, and that is wrong because a timed-out launch may already have started an agent and the response omits the required instruction to check Orca before retrying.
- anchor: "a nonzero exit, timeout or `ok` not true removes the launch record, returns `failed` with `W-LAUNCH-FAILED`, the first stderr line and a `hand_command` (the same call without the marker)."

#### L3.t4-1 (F2)

- claim: The candidate omits the required timeout guidance to check Orca before re-running, so following its recovery output can launch a duplicate agent if the timed-out launch actually started.
- anchor: "a nonzero exit, timeout or `ok` not true removes the launch record"

### L7

#### L7.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a worktree step that calls orca worktree create without --agent, and that is wrong because the project’s Orca instructions say a hook blocks that call without --agent.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment"

### L8

#### L8.t4-1 (F1)

- claim: An implementer who follows the stated text as written builds a prompt containing the common and selected level blocks, but the Task 5 acceptance criterion requires only the selected level block, so the prompt test cannot pass.
- anchor: "levels keep only their own block"
- anchor2: "keeps `common` plus the level block"

#### L8.t4-1 (F3)

- claim: The candidate's required common-block statements omit the source requirement to identify the agent as started by `/sc:issue --claim <N>`.
- anchor: "common (read `issue-summary.md` and `next-steps.md`;"

## Other findings

- L4 (MAJOR, open, single): Contract omits not_requested and null-value rules for launch_status and enforcement_hook.
- L5 (MINOR, open, single): Outputs text overstates launch-prompt.md for pipeline none.
- L6 (MINOR, open, single): The only clause contradicts tasks that must edit tests and docs.

## Reviser brief

Blocking finding ids: L1, L2, L3, L7, L8.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
