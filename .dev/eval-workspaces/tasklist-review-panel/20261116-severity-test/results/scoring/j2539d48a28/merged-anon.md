review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 2da8dc1d6e06cf9a184d60842a7a79012d17e24d428a6f885f95a80a56569c06
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | C-1, C-15, C-17, C-8 | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | WC-11 | R3 |
| L4 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: The design file is absent from the worktree, so exact section 10.2 wording cannot be taken and Tasks 1 to 7 must invent it, failing the Goal of carrying every v1 row.
- anchor: "Use the exact wording of section 10.2 of the design (read it in pieces of at most 80 lines)."
- anchor2: "carries every v1 liveness row (C-1 to C-8 and C-15 to C-17)"

## Other findings

- L2 (MAJOR, open, single): Source.md allows leaving a wait on the worker's own observation, but the plan's stall proof list drops that proof, so a leave-wait case the source allows is not carried.
- L3 (MAJOR, open, single): Source.md names the worker-list projection fields and transcript timestamps the sweep should respect, but Task 6 never requires them, so the state table has no stated basis.
- L4 (MINOR, open, single): The artifacts path is not anchored to the package directory, while repo rules stage package artifacts but never the project root one, so logs can land in the wrong folder.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
