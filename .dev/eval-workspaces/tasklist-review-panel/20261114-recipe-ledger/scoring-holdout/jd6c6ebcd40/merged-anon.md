review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R1, R2, R3 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | yes | overlap | CRITICAL | - | R1, R3 |
| L5 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L4

#### L4.t2b-1 (F4)

- claim: Field names only; not_requested for none and failed Wave 7 stays implicit by reference.
- anchor: "replace the claim-mode return contract with the ten fields of design section 10"

#### L4.t4-1 (F1)

- claim: An implementer who follows the goal literally launches an agent and writes a level record for `--pipeline none`, contradicting the explicit no-agent, no-record behavior in the later requirements.
- anchor: "creates or reuses an Orca worktree `issue-<N>`, launches a Claude Code agent behind the ccsession shim at the chosen level, and records the level in the hook's launch store"
- anchor2: "Wave 8: runs only when `--pipeline` is not `none` and Wave 7 status is `created` or `reused`; run `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]`; never attempted for a `fai"

## Other findings

- L1 (MAJOR, open, overlap): Task 6 drops the required note on hand_command that a hand-started agent is not governed by the hook.
- L2 (MAJOR, open, single): On created status the copy/stale warning cannot both be the status code and fill the warning field.
- L3 (MAJOR, open, single): SKILL.md Wave 5 step 6 never gets the Plan boundary and launch-prompt update.
- L5 (MAJOR, open, single): The required worktree-create command omits `--agent`, which the repository policy says Orca requires; Orca blocks the command, so the worktree step cannot complete.

## Reviser brief

Blocking finding ids: L4.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
