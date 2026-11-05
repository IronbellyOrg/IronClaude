# Codebase enrichment (Wave 2A)

quality_tier: `fallback_2` (native Glob/Grep). Tier 1 `mcp__auggie__codebase-retrieval` was not available in this session's tool list; Tier 2 Serena was skipped by the run brief (Serena is being removed). Searches ran against `src/superclaude/` in worktree `feat-codememory-codegraph-init`, 2026-10-29.

## Files inspected (line counts)

| File | Lines |
|---|---:|
| skills/sc-troubleshoot-protocol/SKILL.md | 711 |
| skills/sc-reflect-protocol/SKILL.md | 2045 |
| skills/sc-auggie-review-protocol/SKILL.md | 393 |
| skills/sc-pr-submit-protocol/SKILL.md | 250 |
| skills/sc-workflow-protocol/SKILL.md | 74 |
| skills/sc-implement-protocol/SKILL.md | 174 |
| skills/sc-cleanup-audit-protocol/SKILL.md | 171 |
| agents/reuse-auditor.md | 185 |
| commands/index-repo.md | 177 |
| commands/explain.md | 104 |
| commands/load.md | 106 |
| agents/repo-index.md | 34 |

## Grep hits that matter for codegraph opportunities

### sc-troubleshoot-protocol

- `:4` allowed-tools: `… mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, …` (enforced allowlist).
- `:156` "Resolve `--scope` to a concrete path/symbol. If given, narrow auggie/serena queries to that target."
- `:168` audit header `mcps_available: <auggie|serena|context7|tavily|none>`.
- `:183-216` Wave 1 Tier 1 Real-Code Grounding: auggie query "Find the code involved in …" (`:192`) + Serena overview/find_symbol (`:193`); exit "auggie + serena results captured in audit log, or Glob/Grep fallback noted" (`:216`).
- `:286` Wave 1.6 Branch A log-call inspection "on the `failing_component` and immediate callers".
- `:256` Wave 1.5 budget ≤ 2k Claude tokens: "the auggie calls offload heavy retrieval".

### sc-auggie-review-protocol

- `:20` token contract: auggie does retrieval (free), Claude validates and synthesizes.
- `:126-138` inputs: `diff.patch`, `files.txt` (`git diff --name-only`), chunking by diff lines/files.
- `:218` findings citing lines outside diff hunks are downgraded or dropped.

### sc-pr-submit-protocol

- `:193` Wave 3 evidence-validator confirms each finding's cited file:line.
- `:206` VG-1 targeted tests `uv run pytest <changed-area>`; `:207` VG-2 cross-cutting change → `make test`.

### sc-reflect-protocol

- `:42` hallucination contract (Grounded vs `[INFERRED]`; others dropped).
- `:344` "For each overlap edge, query `mcp__serena__find_referencing_symbols` to determine whether the symbol is genuinely shared".
- `:514` `mcp__serena__find_referencing_symbols <symbol> include_info:true   # downstream impact + signatures`.

### agents/reuse-auditor.md

- `:5` tools: `Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols` (no Bash → cannot run the codegraph CLI).
- `:126` one capability-keyed auggie query per candidate.
- `:131` auggie-down fallback: Serena `find_symbol` + ripgrep, cap at advisory, `degraded: ["neighbour-search:auggie_unavailable"]`.

### sc-cleanup-audit-protocol

- `:8` allowed-tools include `Bash(git *)`, `Bash(find *)` but not a codegraph Bash pattern.
- `:75` "Every DELETE requires grep proof; every KEEP requires reference citation".
- `:83` Serena for import-chain tracing in discovery.
- `:86` "MCP tools are unavailable to background subagents — all MCP-dependent work … executes in the orchestrator only".
- `:151` no DELETE without grep proof of zero references and no dynamic loading.

### sc-implement-protocol / sc-workflow-protocol

- implement `:9` QA is spec-compliance; lint/tests are extras. `:121` review scoped to the task's touched files.
- workflow `:4` allowed-tools `Read, Glob, Grep, Write, Edit, Bash, Skill` (Bash present → CLI usable; no MCP names).

### Onboarding commands

- index-repo `:3,12-19,72` PROJECT_INDEX.md from 5 parallel Globs; claims 58K → 3K tokens.
- load `:6` `mcp-servers: [serena]`; `:27-43` Serena activation + memory (MEM/ACT jobs, not graph jobs).
- explain `:6` `mcp-servers: [context7]`; `:48` Read/Grep/Glob for code analysis.

## Observations for the debate

1. Bash-capable primitives (workflow, implement, cleanup-audit orchestrator, pr-submit, troubleshoot) can use the CLI without any allowlist or `CODEGRAPH_MCP_TOOLS` change; read-only agents (reuse-auditor, troubleshoot-analyst, reflect-reviewer, evidence-validator, audit-*) need MCP names in `tools:` and the tools listed.
2. Every target primitive already has a degraded/fallback vocabulary; codegraph fits as one more tier.
3. No target primitive today computes callers of changed symbols for review scope or test selection.
