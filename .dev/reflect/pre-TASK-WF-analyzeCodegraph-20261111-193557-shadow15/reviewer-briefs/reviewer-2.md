# Reviewer 2 brief — persona: qa (coverage / acceptance lens)

## T1 card excerpt

Verbatim excerpt from t1-card.md (coverage-relevant slice):

> ## Coverage matrix (Step 1B.0, two-pass)
>
> Pass 1 (ID_REGEX `\b(R-\d+|REQ-\d+|SPEC-\d+|T-\d+)\b`): **0 parsed IDs** — the spec labels requirements `R1`..`R7` (no hyphen); the tasklist labels `Task 1..3`. Pass 2 inference emitted 14 valid quote-pinned rows.
>
> Summary: parsed=0, inferred=14 → `coverage_degraded: parsed-sparse` (Step 1B.2b; 8th consecutive run in this workspace). `coverage_pct: null` (0 parsed). `coverage_pct_union: 1.0` (14/14 matched). `unmapped_requirements_union: []`. `S_dev_density: 0.0` (union denominator).
>
> - **H2 (plan accuracy, MINOR).** Spec ownership (source.md:5) says "the grep over tests/ found none that pins analyze.md content" — true at authoring time (first analyze.md pin landed in the same PR #511 as this package's execution, commit 7764bb623). Not a defect; recorded because Task 3's test-discovery step correctly found and ran `tests/skills/test_codegraph_adoption.py` (t3-test.log: 146 passed).
> - **H4 (verified conformance).** Current HEAD analyze.md satisfies every tasklist AC mechanically: mcp-servers line 6; single readiness instruction line 30 ("exactly once per run"); per-step fresh-only clauses lines 32-34; Codegraph section lines 61-70 (10 lines < 25); no `src/superclaude` reference (grep exit 1); reflect.md parity (reflect.md:6 declares codegraph the same way).

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:13Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md:1-65 (full spec body — audit the matrix against this)

```text
# Design spec: codegraph support in /sc:analyze (issue #504, analyze session)

- Type: component. Format: spec. Target: `src/superclaude/commands/analyze.md` (125 lines, no backing skill, none to be created).
- Guide followed: `~/.claude/CODEGRAPH.md` (installed copy of `src/superclaude/core/CODEGRAPH.md`). Pattern copied in spirit from `sc-troubleshoot-protocol` and `sc-reflect-protocol`: one readiness check, codegraph only when `index_state: fresh`, permanent Grep/Glob/Read floor, a `graph:*` note on degradation, never halt.
- Ownership: only `src/superclaude/commands/analyze.md` (plus a pinning test only if one must change; the grep over `tests/` found none that pins analyze.md content).

## 1. Requirements

| ID | Requirement |
|---|---|
| R1 | Exactly one codegraph readiness check per run, done once before the Discover step, following section 2 of `~/.claude/CODEGRAPH.md`. No re-check unless the run itself wrote a file (analyze writes only the report, so none). |
| R2 | When `index_state: fresh` and `access: mcp`, use `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files` before the existing Glob/Grep/Read step in Discover, Scan and Evaluate. The Glob/Grep/Read step stays unchanged. |
| R3 | Any other state (`stale`, `not_initialized`, `foreign_index`, `absent`, `disabled`, `error`, `access: none`) continues on Glob/Grep/Read, records the matching `graph:*` token from the closed list, and never stops the run. |
| R4 | Frontmatter declares the codegraph MCP server the way `reflect.md` does (`mcp-servers: [codegraph]`); Tool Coordination names the tools. |
| R5 | Every existing behaviour, flag, the Unattended mode section and every Boundary (Will / Will Not / Output / Next Step) is kept as written. |
| R6 | No new `src/superclaude/` read-instruction; the guide is named by its installed path `~/.claude/CODEGRAPH.md`. |
| R7 | codegraph stays read-only: no `codegraph init`, `index`, `sync`, `explore`, `context`, no `codegraph_node` file mode without `symbolsOnly:true`, no wildcard allowlist. |

## 2. Interface (edits to analyze.md)

### 2.1 Frontmatter
`mcp-servers: []` becomes `mcp-servers: [codegraph]`. No `allowed-tools` is added: the file has none today and `reflect.md` declares codegraph only through `mcp-servers`.

### 2.2 Behavioral Flow
Keep the five numbered steps. Add one lead-in line before step 1 and one short codegraph clause per step:

- Before step 1: "**Readiness (once per run, before Discover):** run the codegraph readiness check of `~/.claude/CODEGRAPH.md` section 2 once and keep `index_state`, `checked_at`, `worktree_root` for the whole run. Do not repeat it."
- 1 Discover: when fresh, `codegraph_files {format:"grouped", maxDepth:2}` for layout and `codegraph_search` to locate symbols in the target; then the existing language detection (Glob/Read).
- 2 Scan: when fresh, `codegraph_node {symbol, file?, includeCode:true}` for a symbol body, `codegraph_node {file, symbolsOnly:true}` for a file outline, `codegraph_callers` / `codegraph_callees` for call paths (security: entry points to sinks; performance: hot-path callers); then the existing Grep pattern matching.
- 3 Evaluate: when fresh, `codegraph_impact {symbol, depth}` and `codegraph_callers` supply dependency and blast-radius evidence for architecture and quality findings (coupling, change reach, dead-code candidates as leads only).
- 4, 5 unchanged. Report gets one line: `Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>`.

### 2.3 Tool Coordination
Add one bullet group after Bash/Write, keeping the existing five bullets unchanged:

- **codegraph** (`mcp__codegraph__codegraph_status` once; then `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`): used only when `index_state: fresh`, always before the matching Glob/Grep/Read step; Glob, Grep and Read remain the floor.

### 2.4 New section `## Codegraph (optional)` (after Key Patterns, before Examples)
A compact rule block; the guide is the only place the full rules live:

1. Readiness: once per run; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` means `graph:disabled` and the floor (all handled by the guide's section 2).
2. Use only when `index_state: fresh`. Otherwise Glob/Grep/Read, add the matching `graph:*` token to the report's Codegraph line, continue; never halt, never ask.
3. Graph rows are leads, never citations: re-Read a `file:line` before citing it; an empty result is not a "no callers" finding; caller rows give the definition line, so confirm a call site (guide section 5) before citing; a caller list showing fewer than the total is `graph:truncated`.
4. Read-only: never run `codegraph init`, `index`, `sync`, `explore` or `context`.
5. Exact tool names only (`mcp__codegraph__codegraph_<tool>`), `projectPath` = `worktree_root` on every call.
6. Subagents (if the run fans out): pass `index_state`, `checked_at`, `worktree_root`; they call codegraph only when `index_state: fresh`.

### 2.5 Unattended mode and Boundaries
Unchanged. The Codegraph report line is written into the report; `return-contract.yaml` fields do not change. An unreadable or missing codegraph does not make the run failed (success remains "report written").

## 3. Validation

| Acceptance | Check |
|---|---|
| (a) one readiness check, tools named per step | `grep -n 'readiness' analyze.md` shows one check instruction; Discover/Scan/Evaluate lines name the tools |
| (b) fresh-only, floor with note | text "only when `index_state: fresh`" and "graph:*" and "never halt" present |
| (c) frontmatter | `mcp-servers: [codegraph]` |
| (d) no src path | `grep -n 'src/superclaude' analyze.md` has no hit |
| (e) sync | `make sync-dev` then `make verify-sync` |
| (f) tests | `uv run pytest` over tests that cover command files / install of commands |

## 4. Risks
- Over-long edit to a basic-complexity command: keep the new section under about 25 lines.
- Another session edits other src files in this checkout: `verify-sync` may name files not owned here; re-run `make sync-dev` once, never edit them.
```

### .dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md:31-58 (acceptance criteria)

```text
Task 1 ACs:
- The frontmatter of `src/superclaude/commands/analyze.md` contains `mcp-servers: [codegraph]` and no `allowed-tools` key.
- `grep -n 'index_state: fresh' src/superclaude/commands/analyze.md` matches in Tool Coordination and in the new Codegraph section, and the section names `graph:*`, `never halt` (or equivalent wording), `~/.claude/CODEGRAPH.md` and the read-only ban on `codegraph init`, `index`, `sync`, `explore` and `context`.
- `grep -n 'src/superclaude' src/superclaude/commands/analyze.md` prints no line that tells an agent to read a `src/superclaude/...` path.

Task 2 ACs:
- `src/superclaude/commands/analyze.md` contains exactly one readiness-check instruction, placed before step 1, and the Discover, Scan and Evaluate steps each name the codegraph tools they use and state they apply only when `index_state: fresh`.
- The five step names (Discover, Scan, Evaluate, Recommend, Report), the usage flags, `## Unattended mode` and `## Boundaries` are byte-identical to `git show HEAD:src/superclaude/commands/analyze.md` apart from the intended additions (check with `git diff` on that file).
- The report description includes the `Codegraph: index_state=..., checked_at=...; degraded: ...` line, and a missing or stale graph is stated to leave the run succeeded (report written).

Task 3 ACs:
- `make sync-dev` and `make verify-sync` exit 0, or any remaining `verify-sync` output names only files owned by other sessions.
- The `uv run pytest` run over the tests that cover command files and their install passes; any failure not caused by `src/superclaude/commands/analyze.md` is reported as such and left unfixed.
- `git status --short` shows no staged path under `.claude/`.
```

### .dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/artifacts/t3-test.log:1-16 (verification evidence)

```text
## uv run pytest tests/skills/test_codegraph_adoption.py tests/unit/test_cli_install.py -q
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-504
collected 146 items
tests/skills/test_codegraph_adoption.py ................................ [ 21%]
..................                                                       [ 34%]
tests/unit/test_cli_install.py ......................................... [ 62%]
......................................................                   [100%]
============================= 146 passed in 1.07s ==============================
rc=0
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001..INF-014 (R1-R7 + interface + validation) | 14 inferred rows | covered (14/14 union) | t1-card.md |
| Spec section 3 validation (a)-(f) | INF-014 | covered | source.md:53-60 |
| T3 test evidence | progress.md:8 | verified | t3-test.log:15 |
| H2 pinning-test claim | hypothesis | open | source.md:5 |
