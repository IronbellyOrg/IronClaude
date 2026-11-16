review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 cfd8f983d22ab8af1638ffb2a464215e56048f753f7902e3066435d8de176ca4
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R1, R3 |
| L2 | open | no | single | MINOR | - | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, overlap): Values listed tier3/tier2/tier1a after file order t1/t2/t3 (actual t1=tier1a, t2=tier2, t3=tier3); positional mapping asserts wrong pins.
- L2 (MINOR, open, single): The referenced probe report is absent from the checkout, and no task creates it, so the new reference page may contain a broken evidence link.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
