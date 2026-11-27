review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 674f7eb859158e25665c4915047233eac392eff1f1d94e9311d9833e640b4e0e
reviewers:
- R1: report <path>, block ok true
- R3: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | - | R1 |
| L2 | open | no | overlap | MAJOR | - | R1, R2 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | 2.2, 2.3 | R3 |
| L5 | open | no | single | MAJOR | 2.4 | R3 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): The gate omits access: mcp, so a fresh index reached through the status-only branch still directs MCP lookup tools that are not listed instead of the Glob/Grep/Read floor.
- L2 (MAJOR, open, overlap): The candidate never enumerates the non-fresh states, never points at the closed degraded-token list, and never states that SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off means graph:disabled, so an invented token passes its checks.
- L3 (MAJOR, open, single): This check permits a src/superclaude mention that is not a read instruction, while the driving document requires the grep to have no hit at all.
- L4 (MAJOR, open, single): Candidate gates codegraph tools on fresh only and never states access: mcp, so a status-only registration gets MCP-tool instructions for tools that are not listed.
- L5 (MAJOR, open, single): Codegraph section wording never names SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off mapping to graph:disabled, relying entirely on the section 2 delegation.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
