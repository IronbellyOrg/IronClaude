review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 71d4a7455d11818d9ad4718605a9254142cf1e3e250889cfdfa89285eb5f7d24
reviewers:
- R2: report <redacted>, block ok true
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R3 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MAJOR | - | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): An exclusive reading of the two-write constraint drops the pushback comment and the mode label that Wave 5 still requires.
- L2 (MAJOR, open, single): Comparing the read-back value to Simple, Medium, or Complex reports a successful single-select write as not set, because that field is the option id.
- L3 (MAJOR, open, single): Writing ./artifacts/ from the repo root puts the owner check in the unstaged root artifacts folder, not in the task package.
- L4 (MAJOR, open, single): The mode row says a feature is issue type Feature or Bug, which is false when the area is tests.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
