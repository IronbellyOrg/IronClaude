review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 674f7eb859158e25665c4915047233eac392eff1f1d94e9311d9833e640b4e0e
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | single | MAJOR | 2.3 | R1 |
| L2 | open | no | overlap | MAJOR | 2.4 | R1, R2 |
| L3 | open | no | overlap | MAJOR | - | R1, R2 |
| L4 | open | no | overlap | MAJOR | - | R1, R3 |
| L5 | open | no | single | MAJOR | 2.2 | R1 |
| L6 | open | no | single | MAJOR | 2.2 | R2 |
| L7 | open | no | single | MAJOR | - | R2 |
| L8 | open | no | single | MINOR | 2.4 | R2 |

## Blocking findings

none.

## Other findings

- L1 (MAJOR, open, single): Candidate omits the access: mcp condition, so a fresh index in the status-only branch has no stated branch for unavailable MCP lookup tools.
- L2 (MAJOR, open, overlap): Candidate never names SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off or graph:disabled as source 2.4 item 1 requires.
- L3 (MAJOR, open, overlap): Acceptance check is weaker than source validation (d), which requires no src/superclaude hit at all.
- L4 (MAJOR, open, overlap): Task 1 also restates the one-check rule in the Codegraph section, so a strict count could fail a correct implementation.
- L5 (MAJOR, open, single): Candidate shows the correct file-outline call but never states the ban on codegraph_node file mode without symbolsOnly:true.
- L6 (MAJOR, open, single): Candidate gates codegraph use on index_state: fresh alone, dropping source R2's and access: mcp condition, so a status-only run could be told to call unlisted lookup tools.
- L7 (MAJOR, open, single): Task 3 acceptance requires the pytest run to pass while also leaving any unrelated failure unfixed, which cannot both hold when such a failure exists.
- L8 (MINOR, open, single): Candidate states no repeat absolutely, omitting source R1's re-check after a run write and the explicit off-switch mapping to graph:disabled.

## Reviser brief

Blocking finding ids: none.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: PASS
