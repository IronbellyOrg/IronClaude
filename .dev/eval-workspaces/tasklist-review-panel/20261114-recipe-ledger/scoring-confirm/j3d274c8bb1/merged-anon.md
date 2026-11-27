review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 9f610e5d808c275bde4f84a63cf17ff433dad6004e81609f02e3953c7c7c9df8
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R3, R1, R2 |
| L2 | open | no | single | MINOR | 4 | R3 |
| L3 | open | no | single | MAJOR | - | R3 |
| L4 | open | no | single | MINOR | 3.2 | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, overlap): The design.md text omits the access:mcp definition, so an implementer may treat status-only listing as enabling lookups.
- L2 (MINOR, open, single): The plan omits the within-run-only state rule and no-agent statement, so readiness state may be propagated to a brief that should not carry it.
- L3 (MAJOR, open, single): The acceptance allows failing tests deemed unrelated to pass, so the run may be accepted without the source-required test pass.
- L4 (MINOR, open, single): The placement citation wrongly attributes the section spot to 3.1, which governs frontmatter, not placement.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
