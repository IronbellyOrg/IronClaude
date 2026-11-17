# Reviewer 3 brief — persona: refactorer (structural / tech-debt lens)

## T1 card excerpt

Verbatim excerpt from t1-card.md (structural slice):

> ## Findings (hypotheses)
>
> - **H1 (coverage note, MINOR).** INF-007's clause "no codegraph_node file mode without `symbolsOnly:true`" appears nowhere in the tasklist as a prohibition; the tasklist pins `symbolsOnly:true` only as Scan-step usage (Task 2, "file outline with symbolsOnly:true"). Every file-mode use the tasklist names carries `symbolsOnly:true`, so the shipped result conforms, but a future edit adding node file-mode elsewhere would not be gated by any AC. Family: constraint without matching AC (shadow06/shadow10 recurrence).
> - **H3 (audit-vantage context, advisory).** Package is archived in done/ and its commit (7764bb623, PR #511) bundles four commands + agents, while the tasklist scope is analyze.md only. Bundling is coordinator-level merge action across sibling packages (issue #504), not executor drift; no before-state baseline exists for a strict byte-diff re-check (shadow08 corpus class — discount to advisory).
> - **H4 (verified conformance).** Current HEAD analyze.md satisfies every tasklist AC mechanically: mcp-servers line 6; single readiness instruction line 30 ("exactly once per run"); per-step fresh-only clauses lines 32-34; Codegraph section lines 61-70 (10 lines < 25); no `src/superclaude` reference (grep exit 1); reflect.md parity (reflect.md:6 declares codegraph the same way).
>
> ## Structural signals
>
> S_scope = 3 tasks; S_domains = 1 (docs/command file); S_dev_density = 0.0 (union). Pin: `--tier 2` (hard override §5.1); parsed-sparse pre-filter independently forces T2.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:13Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### src/superclaude/commands/analyze.md:28-36 (current HEAD, Behavioral Flow)

```text
## Behavioral Flow

Before step 1, run the codegraph readiness check exactly once per run, as section 2 of `~/.claude/CODEGRAPH.md` describes: on the MCP path it first waits up to 60 s for a running `init` or `index` (guide step 3), and `checked_at` comes from one `date -u +%Y-%m-%dT%H:%M:%SZ` Bash run right after the single `codegraph_status` call. Keep `index_state`, `access`, `checked_at` and `worktree_root` for the whole run and do not repeat the check. Below, "`index_state: fresh`" means `index_state: fresh` with `access: mcp` (the lookup tools are listed); with `access: cli` or `access: none` every step stays on Glob, Grep and Read, and no codegraph tool, including `codegraph_files`, is called.

1. **Discover**: Categorize source files using language detection and project analysis. When `index_state: fresh`, first call `codegraph_files {format:"grouped", maxDepth:2, path}` for the layout, with `path` set to the target's directory when the target is narrower than the repo; for a directory or package target add `codegraph_node {file, symbolsOnly:true}` on its main files, and use `codegraph_search` only when the target names a symbol
2. **Scan**: Apply domain-specific analysis techniques and pattern matching. When `index_state: fresh`, first call `codegraph_node` (symbol body with `includeCode:true` only for symbols Discover found, file outline with `symbolsOnly:true`), `codegraph_callers` and `codegraph_callees` for call paths (security: entry points to sinks; performance: hot-path callers)
3. **Evaluate**: Generate prioritized findings with severity ratings and impact assessment. When `index_state: fresh`, use `codegraph_impact` and `codegraph_callers` as dependency and blast-radius evidence for architecture and quality findings (dead-code candidates are leads only)
4. **Recommend**: Create actionable recommendations with implementation guidance
5. **Report**: Present comprehensive analysis with metrics and improvement roadmap, with one line `Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>` (with `--format json` it is the top-level `"codegraph"` string field; a missing or stale graph leaves the run succeeded once the report is written)
```

### src/superclaude/commands/analyze.md:61-70 (current HEAD, Codegraph section)

```text
## Codegraph (optional)

Full rules: `~/.claude/CODEGRAPH.md` (read it before the first codegraph call). This section is the short form for `/sc:analyze`.

- **Readiness**: the single check named before step 1 of the Behavioral Flow; never repeat it. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` means `graph:disabled`.
- **Use only when `index_state: fresh` and `access: mcp`.** Otherwise continue on Glob, Grep and Read, add the matching `graph:*` token to the report's Codegraph line, and go on: never halt, never ask. A missing, stale or failing graph never fails the run (it is succeeded once the report is written).
- **Leads, not citations**: re-Read a `file:line` before citing it (at `--depth quick`, a line found by Grep need not be re-Read, but a graph row cited as a finding is still confirmed by Grep or Read); an empty result is not a "no callers" finding; caller rows give the definition line, so confirm the call site (guide section 5) before citing; a caller list shorter than its total is `graph:truncated`; a single lookup that fails or returns nothing records `graph:empty` (or `graph:unresolved` for a row you could not confirm) on the Codegraph line and falls back to Glob, Grep and Read for that lookup.
- **Read-only**: never run `codegraph init`, `index`, `sync`, `explore` or `context`.
- **Names**: exact tool names `mcp__codegraph__codegraph_<tool>`, with `projectPath` set to `worktree_root` on every call.
- **Subagents** (if the run fans out): the brief carries `index_state`, `checked_at` and `worktree_root`; they call codegraph only when `index_state: fresh`.
```

### .dev/tasks/done/TASK-WF-analyzeCodegraph-20261111-193557/source.md:62-64 (risk budget)

```text
## 4. Risks
- Over-long edit to a basic-complexity command: keep the new section under about 25 lines.
- Another session edits other src files in this checkout: `verify-sync` may name files not owned here; re-run `make sync-dev` once, never edit them.
```

### HEAD vs PR511 delta note (structural)

analyze.md was 139 lines at execution (PR #511, commit 7764bb623) and is 139 lines at current HEAD after PR #513 (commit 930c5ebc8, wording tightening: the 60 s wait, `checked_at` via date, `path` arg, `includeCode` scoping, `graph:empty` token, json field, guide-read-first) and PR #515 (commit 077f9dd38, mcp-server grants). The tasklist's byte-diff AC (T2.AC2) was verified against the package's own HEAD at execution time, not current HEAD.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-012 Codegraph section ≤ ~25 lines | Task 1 AC2 | covered (10 lines) | analyze.md:61-70 |
| INF-005/INF-013 boundaries preserved | Task 2 AC2 | covered-at-execution | progress.md:6 |
| H1 file-mode symbolsOnly gate | hypothesis | open | source.md:17 |
| Post-execution evolution (PR 513/515) | vantage note | open | analyze.md:30-36 |
