review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R2: report <path>, block ok true
- R1: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R2 |
| L2 | open | no | single | MAJOR | - | R2 |
| L3 | open | no | single | MAJOR | FO-11 | R2 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MAJOR | LA-1, LA-6, LA-7, ST-6 | R2 |
| L6 | open | no | single | MAJOR | IR-1 | R2 |
| L7 | open | no | single | MAJOR | - | R2 |
| L8 | open | no | single | MAJOR | ST-5 | R2 |
| L9 | open | no | single | MINOR | - | R2 |
| L10 | open | yes | single | MAJOR | - | R1 |
| L11 | open | no | single | MAJOR | - | R1 |
| L12 | open | no | single | MAJOR | OB-1, OB-2, OB-4, OB-9 | R3 |

## Blocking findings

### L10

#### L10.t3-1 (F1)

- claim: The required create call omits --agent, but the repository rule says a hook blocks orca worktree create without it, so the worktree step cannot succeed.
- anchor: "no forbidden flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`, `--agent`"

## Other findings

- L1 (MAJOR, open, single): Task 8 edits only the design doc with no copy step, so the absent requirements folder is never delivered.
- L2 (MAJOR, open, single): The plan never defines the main checkout as the parent of the absolute git common dir, so linked-worktree claims can use the wrong selector.
- L3 (MAJOR, open, single): Reusing an old record after create reports reused on a stale path instead of created for the new row or failed when not listed.
- L4 (MAJOR, open, single): Omitting the skill Wave 5 update leaves the Plan boundary and launch-prompt steps out of the skill summary.
- L5 (MAJOR, open, single): Stopping launch tests at LA-6 leaves no pin for no launch on a failed worktree or Wave 8 after Wave 7.
- L6 (MAJOR, open, single): Allowing any temporary name can publish a half-written record that the hook reads as the level.
- L7 (MAJOR, open, single): Dropping the hand-command note and timed-out check-Orca detail invites a blind retry that starts a duplicate agent.
- L8 (MAJOR, open, single): Pinning only the script lets the launch-prompt template row be added without any files-table test.
- L9 (MINOR, open, single): The goal sentence implies every level including none launches an agent, contrary to the later Wave 8 skip.
- L11 (MAJOR, open, single): The candidate omits the required instruction to check Orca before rerunning after a timeout, which may already have started an agent.
- L12 (MAJOR, open, single): The plan omits the explicitly deferred owner-run checks OB-1, OB-2, and OB-4 through OB-9 after merge, so those required live integration checks are not tracked as follow-up work.

## Reviser brief

Blocking finding ids: L10.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
