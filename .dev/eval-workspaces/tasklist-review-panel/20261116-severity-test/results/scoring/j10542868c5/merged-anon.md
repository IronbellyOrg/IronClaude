review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R2: report <path>, block ok true
- R3: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | FO-18, LA-1, ST-4 | R2 |
| L3 | open | yes | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | overlap | MAJOR | - | R2, R3 |
| L6 | open | no | single | MINOR | - | R2 |

## Blocking findings

### L3

#### L3.t2b-1 (F3)

- claim: Warning wording drops W-ORIGIN-BASE-STALE and W-WORKTREE-COPY-FAILED on created/reused status.
- anchor: "The warning field holds the one code that set the status"

#### L3.t2b-1 (F8)

- claim: Record key match never states matching by realpath against the worktree.json path.
- anchor: "key order marker (comment contains `sc:issue <R>#<N>` not followed by a digit), record, basename (`^issue-<N>(-|$)`), branch"

#### L3.t3-1 (W1)

- claim: The required create call omits --agent, which the repository instructions say is blocked by a hook, so the worktree cannot be created.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L1 (MAJOR, open, single): No task copies the brainstorm folder into the repo, so the folder-existence acceptance has no creating step.
- L2 (MAJOR, open, single): Task 2 forbids --agent/--prompt/--surface in any recorded call while Task 6 requires them in the launch call.
- L4 (MAJOR, open, single): Contract lists ten fields but never defines launch_status not_requested or null handling on STOP.
- L5 (MAJOR, open, overlap): Timeout handling omits the source detail that a timeout may have launched an agent and to check Orca first.
- L6 (MINOR, open, single): Common block summary omits the required statement that the agent was started by /sc:issue --claim <N>.

## Reviser brief

Blocking finding ids: L3.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
