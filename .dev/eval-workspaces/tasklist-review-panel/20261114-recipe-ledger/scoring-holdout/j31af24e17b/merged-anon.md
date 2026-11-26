review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | LA-1, LA-7 | R3 |
| L2 | open | no | single | MAJOR | ARG-1 | R3 |
| L3 | open | no | single | MINOR | FO-18 | R3 |
| L4 | open | yes | overlap | MAJOR | - | R3, R1 |
| L5 | open | no | single | MINOR | - | R3 |
| L6 | open | no | single | MAJOR | - | R1 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L4

#### L4.t2b-1 (F-T2EXACT)

- claim: Task 2 says the script runs exactly seven commands, but preflight and launch run more.
- anchor: "The commands the script runs are exactly:"

#### L4.t3-1 (F1)

- claim: The specified create call omits --agent, but the repository hook blocks worktree creation without it; the required real worktree cannot be created.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L1 (MAJOR, open, single): Plan never assigns test LA-7, so no launch call for a failed worktree record is pinned.
- L2 (MAJOR, open, single): Plan never assigns test ARG-1 for bad arguments of every subcommand.
- L3 (MINOR, open, single): FO-18 wording says any recorded call, but launch legitimately uses --agent, --prompt and --surface.
- L5 (MINOR, open, single): Outputs wording implies launch-prompt.md for every claim, but none writes none.
- L6 (MAJOR, open, single): If the recorded-call check includes launch calls, it rejects the required launch flags; clarify that the check covers only the worktree list and create calls.
- L7 (MAJOR, open, single): Launch failure handling omits the required warning that a timeout may still have started an agent and that the manual fallback is ungoverned, so an operator may rerun and create a duplicate.

## Reviser brief

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
