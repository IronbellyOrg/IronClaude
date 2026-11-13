review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R2: report <redacted>, block ok true
- R3: report <redacted>, block ok true
- R4: report <redacted>, block ok true
- R1: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R1, R2, R3, R4 |
| L2 | open | no | overlap | MAJOR | - | R1, R2, R3, R4 |
| L3 | open | no | overlap | MAJOR | - | R2, R3 |
| L4 | open | no | overlap | MAJOR | - | R2, R4 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, overlap): The required Wave 0 bullet contains an L3 clause that the stated acceptance test, read literally, rejects.
- L2 (MAJOR, open, overlap): Resume row 4 must re-enter release_decision but the stated resume signature supplies neither applied_edits nor target_sha for the head-equality proof.
- L3 (MAJOR, open, overlap): A literal first-match guard_status reports off for a held PR under mode OFF while resume must report it held, and no acceptance case pins which wins.
- L4 (MAJOR, open, overlap): Start-text constants cannot prove whole sentences byte-identical, so the Task 10 check as worded cannot pass as a byte-identity assertion.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
