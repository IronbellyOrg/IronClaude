review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R3: report <redacted>, block ok false
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | AC-1 | R1 |
| L2 | open | no | single | MAJOR | AC-1 | R1 |
| L3 | open | no | single | MINOR | AC-2 | R1 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): A section headed "Merge guard" has no hyphen, so the criterion grep -n "merge-guard" cannot show the heading line as the criterion says it does.
- L2 (MAJOR, open, single): The Wave 0 bullet must carry no L3 condition and also say at L3 with off the line is printed, so a test that rejects any L3 condition would fail the bullet as described.
- L3 (MINOR, open, single): The text does not say whether a failed timeline call alone sets ok:false and exits 1, which decides whether the timeline_unreadable reason is reachable at engage.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
