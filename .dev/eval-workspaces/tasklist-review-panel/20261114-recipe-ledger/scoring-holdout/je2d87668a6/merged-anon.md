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
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | ARG-1, LA-6, LA-7, ST-5 | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | yes | single | MAJOR | 15, 17.2, 17.5 | R3 |
| L7 | open | yes | single | MAJOR | 19, 51 | R3 |
| L8 | open | no | single | MAJOR | 116, 211, 377 | R3 |
| L9 | open | yes | single | MAJOR | - | R2 |
| L10 | open | no | single | MAJOR | - | R2 |
| L11 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L6

#### L6.t3-1 (F1)

- claim: The goal implies an agent launches for every chosen level, contradicting the defined `none` mode and potentially causing an agent to launch when none was requested.
- anchor: "launches a Claude Code agent behind the ccsession shim at the chosen level"
- anchor2: "`none` creates the worktree and launches no agent"

### L7

#### L7.t3-1 (F2)

- claim: The required create command omits `--agent`, but the project policy says a hook blocks worktree creation without it, so the planned command cannot create the worktree.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

### L9

#### L9.t4-1 (F1)

- claim: The required create call omits --agent, contrary to repository instructions that require it and say a hook blocks creation without it.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L1 (MAJOR, open, single): SKILL description and step 6 are never updated, leaving 'then stops' stale against the new launch behaviour.
- L2 (MAJOR, open, single): No mapping gives launch_status not_requested or enforcement_hook null for none and failed-worktree claims.
- L3 (MAJOR, open, single): Temporary name is not required to differ from the nonce pattern, so a half-written record could be visible to the hook.
- L4 (MINOR, open, single): LA-7 and ARG-1 cases and the ST-5 template files-table pin from source section 13 are not carried.
- L5 (MINOR, open, single): Literal grep shows pre-existing hits in untouched files, so the check needs a baseline diff it does not state.
- L8 (MAJOR, open, single): The plan omits the required check with Orca before retrying after a timeout, even though the timed-out launch may have started an agent; retrying can launch a duplicate.
- L10 (MAJOR, open, single): The plan omits the required common-block statement that the agent was started by `/sc:issue --claim <N>`.
- L11 (MAJOR, open, single): The source requires the brainstorm folder to be committed with the change, but the plan never instructs staging it.

## Reviser brief

Blocking finding ids: L6, L7, L9.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
