review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 2da8dc1d6e06cf9a184d60842a7a79012d17e24d428a6f885f95a80a56569c06
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | single | MINOR | WC-10 | R1 |
| L4 | open | no | single | MAJOR | WC-11 | R2 |

## Blocking findings

### L1

#### L1.t2b-1 (F1)

- claim: Cited design file is absent from the worktree, so the implementer cannot obtain exact section 10.2 wording and the contract cannot match the design as required.
- anchor: "Use the exact wording of section 10.2 of the design (read it in pieces of at most 80 lines)."

## Other findings

- L2 (MAJOR, open, overlap): Task 6 sweep omits source-required projection.liveness, projection.stage.activity, projection.attention.categories, requiresAction/nextAction and millisecond timestamps.
- L3 (MINOR, open, single): Without a distinct key name the new WC-10 pin can overwrite the existing WC-10 entry and drop the cadence and 4-minute phrases.
- L4 (MAJOR, open, single): The plan requires a worker-list sweep but omits the source's specified liveness, stage, attention, action, and transcript evidence fields for interpreting worker state.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
