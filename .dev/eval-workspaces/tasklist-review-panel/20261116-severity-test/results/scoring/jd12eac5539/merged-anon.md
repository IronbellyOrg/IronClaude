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
| L1 | open | no | single | MAJOR | C-7 | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MINOR | - | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): C-7 restart rule omits worker's own observation as positive proof.
- L2 (MAJOR, open, single): Task 6 omits projection.liveness/stage/attention fields and millisecond timestamps.
- L3 (MAJOR, open, single): Design file section 10.2 is absent from this checkout so exact wording cannot be verified.
- L4 (MINOR, open, single): Artifacts path is ambiguous between package artifacts and project-root artifacts.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
