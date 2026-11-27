review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 674f7eb859158e25665c4915047233eac392eff1f1d94e9311d9833e640b4e0e
reviewers:
- R3: report <path>, block ok true
- R1: report <path>, block ok true
- R2: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | no | overlap | MAJOR | - | R3, R2 |
| L2 | open | no | single | MAJOR | - | R3 |
| L3 | open | yes | single | CRITICAL | 2.2, 2.4 | R1 |
| L4 | open | no | single | MAJOR | 2.4 | R1 |
| L5 | open | yes | single | MAJOR | - | R2 |

## Blocking findings

### L3

#### L3.t3-1 (F1)

- claim: Gates codegraph use on fresh alone, dropping source R2 condition fresh and access:mcp, so status-only runs try unlisted MCP lookups instead of the floor.
- anchor: "Each clause says \"when `index_state: fresh`\" and leaves the Glob/Grep/Read step in place."

#### L3.t3-1 (F2)

- claim: Omits source 2.2 detail codegraph_impact {symbol, depth} and Scan call-path purposes (security entry to sinks; performance hot-path callers), giving weaker guidance than required.
- anchor: "in step 3 (Evaluate) `codegraph_impact` and `codegraph_callers` as dependency and blast-radius evidence for architecture and quality findings (dead-code candidates as leads only)"

#### L3.t3-1 (F4)

- claim: Task 1 also requires a readiness statement in the Codegraph section while Task 2 acceptance says exactly one instruction; whether the summary counts is ambiguous and needs a guess to fail.
- anchor: "contains exactly one readiness-check instruction, placed before step 1"

### L5

#### L5.t4-1 (F1)

- claim: The required sync changes the generated analysis command under .claude/, contradicting the blanket prohibition on editing anything there; both instructions cannot be satisfied literally.
- anchor: "or anything under `.claude/`"
- anchor2: "Run `make sync-dev` then `make verify-sync`"

## Other findings

- L1 (MAJOR, open, overlap): The fresh gate omits the source condition access: mcp, so the text allows MCP lookup calls in the status-only or no-access branch.
- L2 (MAJOR, open, single): The check passes with a non-read src/superclaude mention in analyze.md, while source validation (d) requires no grep hit at all.
- L4 (MAJOR, open, single): Names only a matching graph:* token, without source R3 closed-list and invent-none rule from guide section 3, so an implementer could invent a token.

## Reviser brief

Blocking finding ids: L3, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
