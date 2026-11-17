# Reviewer 1 brief — persona: analyzer (root-cause / deviation lens)

## T1 card excerpt

Verbatim excerpt from t1-card.md (deviation-relevant slice):

> ## Findings (hypotheses)
>
> - **H1 (coverage note, MINOR).** INF-007's clause "no codegraph_node file mode without symbolsOnly:true" appears nowhere in the tasklist as a prohibition; the tasklist pins `symbolsOnly:true` only as Scan-step usage (Task 2, "file outline with symbolsOnly:true"). Every file-mode use the tasklist names carries `symbolsOnly:true`, so the shipped result conforms, but a future edit adding node file-mode elsewhere would not be gated by any AC. Family: constraint without matching AC (shadow06/shadow10 recurrence).
> - **H2 (plan accuracy, MINOR).** Spec ownership (source.md:5) says "the grep over tests/ found none that pins analyze.md content" — true at authoring time (first analyze.md pin landed in the same PR #511 as this package's execution, commit 7764bb623). Not a defect; recorded because Task 3's test-discovery step correctly found and ran `tests/skills/test_codegraph_adoption.py` (t3-test.log: 146 passed).
> - **H3 (audit-vantage context, advisory).** Package is archived in done/ and its commit (7764bb623, PR #511) bundles four commands + agents, while the tasklist scope is analyze.md only. Bundling is coordinator-level merge action across sibling packages (issue #504), not executor drift; no before-state baseline exists for a strict byte-diff re-check (shadow08 corpus class — discount to advisory).
> - **H4 (verified conformance).** Current HEAD analyze.md satisfies every tasklist AC mechanically: mcp-servers line 6; single readiness instruction line 30 ("exactly once per run"); per-step fresh-only clauses lines 32-34; Codegraph section lines 61-70 (10 lines < 25); no `src/superclaude` reference (grep exit 1); reflect.md parity (reflect.md:6 declares codegraph the same way).

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:13Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md:9-17

```text
| ID | Requirement |
|---|---|
| R1 | Exactly one codegraph readiness check per run, done once before the Discover step, following section 2 of `~/.claude/CODEGRAPH.md`. No re-check unless the run itself wrote a file (analyze writes only the report, so none). |
| R2 | When `index_state: fresh` and `access: mcp`, use `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files` before the existing Glob/Grep/Read step in Discover, Scan and Evaluate. The Glob/Grep/Read step stays unchanged. |
| R3 | Any other state (`stale`, `not_initialized`, `foreign_index`, `absent`, `disabled`, `error`, `access: none`) continues on Glob/Grep/Read, records the matching `graph:*` token from the closed list, and never stops the run. |
| R4 | Frontmatter declares the codegraph MCP server the way `reflect.md` does (`mcp-servers: [codegraph]`); Tool Coordination names the tools. |
| R5 | Every existing behaviour, flag, the Unattended mode section and every Boundary (Will / Will Not / Output / Next Step) is kept as written. |
| R6 | No new `src/superclaude/` read-instruction; the guide is named by its installed path `~/.claude/CODEGRAPH.md`. |
| R7 | codegraph stays read-only: no `codegraph init`, `index`, `sync`, `explore`, `context`, no `codegraph_node` file mode without `symbolsOnly:true`, no wildcard allowlist. |
```

### .dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/TASK-WF-analyzeCodegraph-20261111-193557.md:17-23

```text
## Constraints

- Edit only `src/superclaude/commands/analyze.md`; a test that pins that file may change only if one must. Do not create a skill for `/sc:analyze`.
- Do not edit `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or anything under `.claude/`; `.claude/` is gitignored sync output and is never staged.
- Keep every existing flag, behaviour, the Unattended mode section and every Boundary (Will, Will Not, Output, Next Step) of the command as written.
- Name the guide by its installed path `~/.claude/CODEGRAPH.md`; add no instruction that reads a `src/superclaude/...` path.
- No commit, no push, no PR. Leave staging and committing to the coordinator.
```

### .dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/progress.md:3-9

```text
T1: start sha=54799c0c0d9e743d7eb7d5c1213df639f3fade72
T1: complete verdict=compliant ac=T1.AC1,T1.AC2,T1.AC3 evidence=T1.AC1@src/superclaude/commands/analyze.md:6,T1.AC2@src/superclaude/commands/analyze.md:64,T1.AC3@src/superclaude/commands/analyze.md:61 extras=lint:skip,typecheck:skip,test:skip files=src/superclaude/commands/analyze.md
T2: complete verdict=compliant ac=T2.AC1,T2.AC2,T2.AC3 evidence=T2.AC1@src/superclaude/commands/analyze.md:30,T2.AC2@src/superclaude/commands/analyze.md:106,T2.AC3@src/superclaude/commands/analyze.md:36
T3: complete verdict=compliant ac=T3.AC1,T3.AC2,T3.AC3 evidence=T3.AC1@./artifacts/t3-sync.log:9,T3.AC1@./artifacts/t3-sync.log:51,T3.AC2@./artifacts/t3-test.log:15,T3.AC2@./artifacts/t3-test.log:39,T3.AC3@./artifacts/t3-staged.log:2 extras=test:pass
FINAL: pass evidence=src/superclaude/commands/analyze.md:6,src/superclaude/commands/analyze.md:30,./artifacts/t3-sync.log:51,./artifacts/t3-test.log:39
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 one readiness check (R1) | T2 mapping | covered | tasklist:40 |
| INF-007 read-only + symbolsOnly file-mode ban (R7) | T1/T2 partial | covered-with-gap | source.md:17 vs tasklist:29,40 |
| INF-014 validation checks (a)-(f) | T1-T3 ACs | covered | source.md:53-60 |
| H1 constraint-without-AC risk | hypothesis | open | t1-card.md |
| H3 bundled-PR vantage | hypothesis (advisory) | open | t1-card.md |
