review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 674f7eb859158e25665c4915047233eac392eff1f1d94e9311d9833e640b4e0e
reviewers:
- R3: report <path>, block ok true
- R2: report <path>, block ok true
- R1: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | 2.2, 2.3 | R3, R1 |
| L2 | open | no | single | MAJOR | 2.2, 2.4 | R3 |
| L3 | open | no | single | MINOR | 2.4 | R3 |
| L4 | open | no | single | MAJOR | - | R2 |
| L5 | open | no | single | MINOR | - | R2 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, overlap): Gate omits access:mcp: candidate conditions use on index_state alone, so implementer builds MCP calls when fresh even if access is cli/none.
- L2 (MAJOR, open, single): Exactly-one count collides with required Codegraph-section readiness mention; strict grep counts two mentions and fails.
- L3 (MINOR, open, single): Closed graph:* list lives in guide section 3 but candidate points only to section 2, so degraded-state token choice is underspecified.
- L4 (MAJOR, open, single): The fresh-only condition omits the source's `access: mcp` requirement, so an implementer may direct MCP lookups when lookup access is unavailable instead of using the floor.
- L5 (MINOR, open, single): The plan omits the source's placement instruction to add this bullet after Bash/Write; no behavioral consequence was identified.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
