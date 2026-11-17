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
| L1 | open | yes | single | CRITICAL | ST-8 | R3 |
| L2 | open | no | single | MAJOR | LA-1, LA-7 | R3 |
| L3 | open | no | single | MAJOR | ARG-1 | R3 |
| L4 | open | no | single | MAJOR | - | R3 |
| L5 | open | no | single | MAJOR | - | R3 |
| L6 | open | yes | overlap | MAJOR | - | R1, R2 |
| L7 | open | no | single | MAJOR | - | R1 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: ST-8 requires only submit to contain the tokens and also requires worktree to contain them, so the acceptance test cannot pass.
- anchor: "only the `submit` block contains `/sc:pr-submit --monitor 3`, `git push` and the commit instruction"
- anchor2: "only the `worktree` block also contains those tokens (as a prohibition)"

### L6

#### L6.t3-1 (F1)

- claim: The required create call omits --agent, which the repository's Orca hook requires and otherwise rejects, so worktree creation fails.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"
- anchor2: "no forbidden flag (`--issue`, `--pr`, `--reference*`, `--linear-issue`, `--gitlab-*`, `--agent`"

#### L6.t4-1 (F1)

- claim: The required create command omits --agent, which the repository hook blocks, so the claim cannot create the worktree needed for the separate launch.
- anchor: "orca worktree create --repo path:<main> --name issue-<N> --base-branch origin/<B> --no-parent --comment \"sc:issue <R>#<N>\" --json"

## Other findings

- L2 (MAJOR, open, single): LA-7 is missing: no test pins no launch call for a failed record and no pending record for none.
- L3 (MAJOR, open, single): ARG-1 for every subcommand is not pinned; only preflight bad arguments are in the acceptance test.
- L4 (MAJOR, open, single): Contract null rules are missing: not_requested for none and failed worktree, and enforcement_hook null when no agent was requested.
- L5 (MAJOR, open, single): SKILL.md claim step 6 (Wave 5 additions) update from design section 12 is missing.
- L7 (MAJOR, open, single): Timeout handling omits the required instruction to check Orca before retrying, risking a duplicate launch if the timed-out call already started an agent.

## Reviser brief

Blocking finding ids: L1, L6.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
