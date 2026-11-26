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
| L1 | open | yes | overlap | MAJOR | - | R1, R2 |
| L2 | open | no | single | MAJOR | - | R1 |
| L3 | open | no | single | MAJOR | 2.3 | R3 |
| L4 | open | no | single | MAJOR | 2.4 | R3 |
| L5 | open | no | single | MAJOR | 2.5 | R3 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: Lookup tools are gated on fresh alone, so in the status-only branch the command directs calls to unlisted MCP tools instead of the floor with graph:unlisted.
- anchor: "used only when `index_state: fresh` and always before the matching Glob/Grep/Read step, which stays the floor."

#### L1.t1b-1 (F3)

- claim: The standing ban on codegraph_node file mode without symbolsOnly:true is never stated, although R7 requires it.
- anchor: "codegraph stays read-only (never `codegraph init`, `index`, `sync`, `explore` or `context`)"

#### L1.t1b-1 (F4)

- claim: Byte-identical is ambiguous between step names and whole step lines, and the whole-line reading cannot pass once the required clauses are added to steps 1 to 3.
- anchor: "are byte-identical to `git show HEAD:src/superclaude/commands/analyze.md` apart from the intended additions (check with `git diff` on that file)"

#### L1.t1b-1 (F5)

- claim: The exactly-one-instruction check can be miscounted against the Codegraph section statement Task 1 also requires.
- anchor: "`src/superclaude/commands/analyze.md` contains exactly one readiness-check instruction, placed before step 1"
- anchor2: "the one readiness check per run follows section 2 of `~/.claude/CODEGRAPH.md`"

#### L1.t1b-1 (F6)

- claim: codegraph_impact is named without the depth argument the source interface specifies, leaving blast-radius depth to a tool default.
- anchor: "in step 3 (Evaluate) `codegraph_impact` and `codegraph_callers` as dependency and blast-radius evidence for architecture and quality findings (dead-code candidates as leads only)"

#### L1.t4-1 (F1)

- claim: The candidate omits the explicit access:mcp lookup gate and access:none fallback required by R2 and R3; fresh status alone does not establish lookup availability.
- anchor: "Each clause says \"when `index_state: fresh`\""

#### L1.t4-1 (F2)

- claim: The outline recipe specifies symbolsOnly:true but does not carry R7's general prohibition on codegraph_node file mode without it.
- anchor: "file outline with `symbolsOnly:true`"

## Other findings

- L2 (MAJOR, open, single): The check permits a non-read src/superclaude mention to remain, while source validation (d) requires no grep hit at all.
- L3 (MAJOR, open, single): Source requires fresh AND access:mcp; plan never names access, so implementer calls lookup tools when access is none.
- L4 (MAJOR, open, single): Plan never enumerates the closed graph token list, so degraded reporting tokens are invented per state.
- L5 (MAJOR, open, single): Plan omits that return-contract fields stay unchanged and a missing graph leaves the run succeeded.

## Reviser brief

Blocking finding ids: L1.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
