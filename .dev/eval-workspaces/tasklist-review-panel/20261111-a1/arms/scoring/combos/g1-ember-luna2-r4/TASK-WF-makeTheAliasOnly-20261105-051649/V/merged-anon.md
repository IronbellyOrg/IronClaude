review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R2: report <redacted>, block ok false

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MINOR | - | R1 |
| L4 | open | no | single | MINOR | - | R1 |
| L5 | open | yes | single | MAJOR | - | R3 |
| L6 | open | no | single | MINOR | - | R3 |

## Blocking findings

### L5

#### L5.R3 (F1)

- claim: The required unchanged-tree run cannot fail exactly seven tests in the reviewed checkout because the existing policy test file runs green with 13 passed.
- anchor: "run on the unchanged tree fails exactly these seven tests"

## Other findings

- L1 (MAJOR, open, single): A builder who follows the scope line literally refuses to edit docs and tests, then the later steps cannot pass.
- L2 (MAJOR, open, single): A builder could allow-list the reflect default on day one, so the expected first failure would never appear.
- L3 (MINOR, open, single): The stated line numbers are stale, so the builder must search by name instead of line.
- L4 (MINOR, open, single): The same check already exists in that test file, so the new test would be a duplicate.
- L6 (MINOR, open, single): These launcher line references are stale in the reviewed checkout, so the follow-up spec must verify and correct them before quoting the anchors.

## Reviser brief

Blocking finding ids: L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
