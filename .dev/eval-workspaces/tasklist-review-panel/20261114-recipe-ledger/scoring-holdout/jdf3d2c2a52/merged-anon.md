review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <path> sha256 81cf9cc6829b4a5c05ca8308aeb332623ecaba791deddbcd4c55205e30ca4fcb
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | CRITICAL | FO-18, LA-1 | R1 |
| L2 | open | yes | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | no | overlap | MAJOR | - | R1, R2 |

## Blocking findings

### L2

#### L2.t2b-1 (F2)

- claim: An implementer who follows the stated text builds a change without copying the brainstorm folder, and Task 8 acceptance cannot pass because no task orders the copy and the folder is absent.
- anchor: "already copied into this repository and part of the change."

## Other findings

- L1 (CRITICAL, open, single): An implementer who follows FO-18 as written builds a test that scans every orca call, and it fails because the required launch call contains --agent, --prompt, --surface.
- L3 (MAJOR, open, single): Candidate forces failed on any copy problem while source allows W-WORKTREE-COPY-FAILED with created/reused status for tracked and .prev files.
- L4 (MINOR, open, single): Outside the B2 row, the original design still states the claim stops without running next-step commands, leaving false acceptance text noted only as amended.
- L5 (MAJOR, open, overlap): Candidate omits the source rule that timeout detail must warn to check Orca before re-running because a timeout may have started an agent.

## Reviser brief

Blocking finding ids: L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
