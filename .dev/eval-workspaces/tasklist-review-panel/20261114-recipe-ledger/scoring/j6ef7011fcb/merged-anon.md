review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | - | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): An implementer who follows the exactly-two constraint builds create that writes only type and Complexity, and X is wrong because it drops the mode label and pushback comment required by Tasks 1-2.
- L2 (MAJOR, open, single): T3 edit verified only by protocol tests; worker-contract tests pinning T3 remain unchecked and can stay red.
- L3 (MAJOR, open, single): The plan does not require preserving the area in the pushback comment, which the driving document requires alongside flags.md.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
