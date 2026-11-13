review: 1 of 3
# Merged review 1 (coordinator script; panel of 2 reviewers)
candidate: <candidate file> sha256 044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481
reviewers:
- R1: report <redacted>, block ok true
- R2: report <redacted>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MINOR | - | R1 |
| L6 | open | no | single | MAJOR | - | R2 |
| L7 | open | no | single | MAJOR | - | R2 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): A heading named "Merge guard" does not match the hyphenated grep that the criterion says must show the section heading; the heading text is not fixed.
- L2 (MAJOR, open, overlap): The exit code for the not_open result is not stated or asserted, so a script that exits 0 with ok:false is allowed.
- L3 (MAJOR, open, overlap): The Wave 0 bullet must be free of L3 and draft wording yet must contain 'at L3' and 'no draft call', so a literal scan fails on its own required text.
- L4 (MAJOR, open, single): Only the start text of the pinned sentences is recorded, so a start-text constant cannot prove the whole sentence is unchanged.
- L5 (MINOR, open, single): Held-guard reporting on resume and the merge_guard output row also change ordinals 0 to 2, beyond the one report line the scope limit allows.
- L6 (MAJOR, open, single): Resume cannot supply applied_edits and target_sha to the row 4 release re-entry, so the implementer must invent their source.
- L7 (MAJOR, open, single): The retry key format is asserted without a construction rule, so implementers invent incompatible groupings.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
