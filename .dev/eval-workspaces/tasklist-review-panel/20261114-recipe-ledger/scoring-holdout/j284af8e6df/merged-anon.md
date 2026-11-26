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
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | overlap | MAJOR | - | R1, R2 |
| L5 | open | no | single | MINOR | ARG-1, LA-6, LA-7 | R1 |
| L6 | open | yes | overlap | MAJOR | - | R3, R2 |
| L7 | open | yes | single | MAJOR | FO-18, LA-1 | R2 |
| L8 | open | no | single | MAJOR | - | R2 |
| L9 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: No task creates the brainstorm folder, so an implementer who follows the plan skips the copy and Task 8 existence check fails.
- anchor: "already copied into this repository and part of the change"
- anchor2: "The folder `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/` exists"

### L6

#### L6.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a worktree-create call without --agent, and that call is rejected by the repository hook because every Orca worktree creation must include --agent.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

#### L6.t4-1 (F1)

- claim: The required create call omits --agent, but the repository instructions say a hook blocks Orca worktree creation without that flag, so worktree creation fails.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

### L7

#### L7.t4-1 (F2)

- claim: FO-18 forbids launch-only flags in any recorded Orca call, while Task 6 requires those flags in the launch call, making the required tests mutually incompatible.
- anchor: "appears in any recorded `orca` call."
- anchor2: "orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt"

## Other findings

- L2 (MAJOR, open, overlap): Plan names ten fields but never defines not_requested or null values for none and failed worktree cases.
- L3 (MAJOR, open, single): Planned prompt test omits the full block itself, so full block could hold banned tokens while tests pass.
- L4 (MAJOR, open, overlap): Plan omits timeout check-Orca note and hand command not-governed note required by the design.
- L5 (MINOR, open, single): Launch test list ends at LA-6, so LA-7 and ARG-1 have no planned test.
- L8 (MAJOR, open, single): The test requirements do not pin the source requirement that invalid flag combinations stop before any GitHub or Orca call.
- L9 (MAJOR, open, single): The guide update does not require stating that Orca is required or naming E-ORCA-REQUIRED, as the source requires.

## Reviser brief

Blocking finding ids: L1, L6, L7.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
