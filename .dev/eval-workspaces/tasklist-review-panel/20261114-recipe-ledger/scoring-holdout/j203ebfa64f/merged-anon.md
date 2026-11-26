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
| L2 | open | no | single | MAJOR | FO-18, LA-1 | R1 |
| L3 | open | no | single | MAJOR | FO-12 | R1 |
| L4 | open | no | overlap | MAJOR | - | R1, R3, R2 |
| L5 | open | yes | overlap | MAJOR | - | R1, R2 |
| L6 | open | yes | overlap | CRITICAL | - | R1, R3 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L5

#### L5.t2b-1 (F7)

- claim: Branch and path source and failed null rule are unstated, so failed rows may carry stale or missing values.
- anchor: "add `worktree --repo <R> --number <N> --base origin/<B> --source <D>`, printing `{status, path, branch, match_key, warning, detail}`"

#### L5.t4-1 (F1)

- claim: The required create call omits --agent, which the project hook requires; following the plan makes real worktree creation fail.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

### L6

#### L6.t2b-1 (F8)

- claim: Goal reads as launching for every pipeline value, while none must create only and launch nothing.
- anchor: "creates or reuses an Orca worktree `issue-<N>`, launches a Claude Code agent behind the ccsession shim at the chosen level"

#### L6.t3-1 (F1)

- claim: An implementer who follows the stated text as written builds a claim flow that launches an agent for `--pipeline none`, and that is wrong because the driving document says `none` creates or reuses the worktree but launches no agent.
- anchor: "launches a Claude Code agent behind the ccsession shim at the chosen level"
- anchor2: "`none` launches no agent."

## Other findings

- L1 (MAJOR, open, single): Contract lists ten names but not not_requested for none or failed worktree nor null enforcement hook, so none claims get a wrong launch state.
- L2 (MAJOR, open, single): FO-18 says no call may contain agent prompt surface, but launch must contain them, so a whole suite scan fails LA-1.
- L3 (MAJOR, open, single): Post create unusable list cannot have no create call since create precedes it, so the FO-12 check as written cannot pass on that case.
- L4 (MAJOR, open, overlap): Both steps set one launch warning with no precedence, so missing hook plus bad shim leaves the emitted code to an undocumented choice.
- L7 (MAJOR, open, single): The user-guide requirements omit the instruction that full and submit levels are for test issues only until the enforcement hook exists.

## Reviser brief

Blocking finding ids: L5, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
