---
topic: "Opportunities for IronClaude skills, commands, refs and agents (src/superclaude/{skills,commands,agents,core,hooks}) to use codegraph (colbymchenry/codegraph v1.6.2) beyond replacing Serena symbol tools, across token cost, citation accuracy, impact analysis before edits, review scoping, test selection, troubleshooting grounding, planning/workflow, reflection/audit and onboarding; ranked ideas with target primitives, value, effort (S/M/L), risk, explicit drops, and 3-5 candidate new /sc: commands or skills."
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-10-29T16:24:11Z
---

# Seed Brief: p3-codegraph-opportunities

## Problem Statement

Serena is being removed from IronClaude primitives. The removal plan fills its symbol-lookup holes, but primitives also answer structural questions (who calls X, what breaks if X changes, which tests cover a diff, where is the code for this symptom) with auggie (semantic, no call graph) and Grep (lexical). codegraph v1.6.2 offers a local, read-only call graph. The question is where, beyond 1:1 Serena replacement, codegraph measurably improves token cost, citation accuracy or safety — and where it does not pay off.

## Known Context

Ground truth: `.dev/codegraph-migration/research/codegraph-evaluation.md` (EVAL). Do not claim any capability not in it.

- **MCP tools (all read-only, optional `projectPath`)**: `codegraph_explore {query, maxFiles}` (source + call paths + blast radius in one call), `codegraph_search {query, kind, limit}`, `codegraph_callers {symbol, file, limit≤100}`, `codegraph_callees {symbol, file, limit}`, `codegraph_impact {symbol, file, depth=2}` (inbound), `codegraph_node {symbol|file, includeCode, symbolsOnly, line, offset, limit}` (file mode = Read-equivalent with line numbers), `codegraph_files {path, pattern, format, maxDepth}`, `codegraph_status`. EVAL §3.
- **Only `codegraph_explore` is listed by default.** The other 7 need `CODEGRAPH_MCP_TOOLS=explore,node,search,callers,callees,impact,files,status` in the server env (they answer `tools/call` unlisted, but Claude Code can only call listed tools). The planned registration (EVAL §7 step 5) sets only `CODEGRAPH_TELEMETRY=0`, `CODEGRAPH_NO_UPDATE_CHECK=1`.
- **CLI**: `init`, `index`, `sync`, `status`, `query <s> [--kind --limit --json]`, `explore`, `context <task…>`, `node`, `files`, `callers`, `callees`, `impact [--depth]`, `affected [files…] [--stdin --depth --filter --json --quiet]` (upstream example: `git diff --name-only | codegraph affected --stdin`). EVAL §3.
- **Measured**: CLI query ~290-300 ms; MCP callers 3-15 ms, explore 253-771 ms; one `explore` returned 24,913 characters and pulled 2 unrelated `install` functions. Index 500 files in ~4.5 s, ~70 KB/file. EVAL §5.
- **Accuracy gaps**: caller rows cite the caller's **definition** line, not the call site (`main.py:46` not `:255`); no regex/semantic search, no text search, no data flow / cross-service, no Cypher, no LSP diagnostics, no edits, no memories; `affected` maps to test files only, no diff-to-symbol mapping. EVAL §5.5, §6.
- **Freshness/ops**: daemon watcher only while an MCP client is connected; `codegraph sync` fails on the writer lock while a daemon runs; new sibling worktree = "not initialized"; nested worktree = parent index + warning; per-worktree `init` has no owner yet. EVAL §4, §5.7, §5.8.
- **Rejected upstream pieces**: `prompt-hook` (injects an explore payload into every prompt), `codegraph install` (its CLAUDE.md block is erased by `superclaude install`). EVAL §5.9, §7.
- **Today's usage (INV §1, §4)**: codebase-memory has 0 primitive references; Serena has 86 load-bearing rows. Load-bearing SYM/REF rows: troubleshoot command + skill, reflect (6 SYM, 2 REF), validate-roadmap (2 SYM), reuse-auditor (1 REF). Reflect is the heaviest consumer. MEM/NUDGE/ACT jobs are not graph jobs.

## Constraints

- Planning only; ideas target guidance text, `tools:` allowlists, return-contract values, and new primitives — not IronClaude Python CLI code or the installer phase.
- Installed-path rule: no `src/superclaude/...` paths inside primitives; dual-surface lookups.
- Fail-open: every codegraph step must have a named native fallback (Read/Grep/Glob, auggie) and record a degraded value; never STOP because codegraph is absent or uninitialized.
- Citation contract: any `file:line` from codegraph must be re-Read before it lands in a report (definition-line gap).
- Read-only agents (`tools: Read, Grep, Glob, …`) cannot run the CLI; they need `mcp__codegraph__*` names in `tools:` and the tool must be listed.
- No `prompt-hook`; no reliance on direct SQLite schema (UNVERIFIED).
- Cover all nine vectors: token cost, citation accuracy, impact before edits, review scoping (auggie-review, pr-submit, reflect), test selection (`affected`), troubleshooting Tier 1, planning (workflow, implement, tasklist), reflection/audit (reflect, cleanup-audit, reuse-auditor), onboarding (index-repo, explain, load).

## Success Criteria

- Every idea names target primitive(s), expected value, effort S/M/L, and risk.
- A single ranked list; low-value ideas explicitly dropped with a reason.
- 3-5 candidate new `/sc:` commands or skills that other primitives call, each with its callers.
- Every capability claim traceable to EVAL; prerequisites (tool listing env, per-worktree init, freshness) called out as blockers where they apply.

## Open Questions

- MCP tools or CLI via Bash as the default access path, per primitive class?
- Shared grounding ref/skill vs. inline steps per primitive?
- Is `codegraph_explore` a net token saving versus auggie (free, server-side) and targeted Read?
- Does `codegraph affected` beat "changed area" test selection enough to change pr-submit / implement gates?
- Where does codegraph conflict with the evidence-validator's re-Read discipline?

## Enrichment Context

Source: native Glob/Grep (quality tier `fallback_2`; auggie MCP not available in this session, Serena forbidden by the run brief). Full notes: `enrichment/codebase-context.md`. Research enrichment skipped: EVAL is the mandated ground truth.

- `sc-troubleshoot-protocol/SKILL.md:183-216` Wave 1 Tier 1 grounding = one auggie query + Serena `get_symbols_overview`/`find_symbol`; exit criteria accept a Glob/Grep fallback. Wave 1.6 diagnosability audit inspects the failing component "and immediate callers" (line 286) via auggie/Grep.
- `sc-auggie-review-protocol/SKILL.md:126-138,218` collects `diff.patch` + `files.txt`; chunking by diff size; findings outside diff hunks are downgraded. No caller/blast-radius context for changed symbols.
- `sc-pr-submit-protocol/SKILL.md:193,206-207` Wave 3 evidence-validator; VG-1 `uv run pytest <changed-area>`, VG-2 escalate to `make test`.
- `sc-reflect-protocol/SKILL.md:42,344,514` hallucination contract; overlap edges and downstream impact via `mcp__serena__find_referencing_symbols`.
- `agents/reuse-auditor.md:5,126,131` tools allowlist includes Serena; one auggie capability query per candidate; auggie-down fallback = Serena `find_symbol` + ripgrep, findings capped at advisory.
- `sc-cleanup-audit-protocol/SKILL.md:75,83,86,151` DELETE requires grep proof of zero references; Serena for import-chain tracing; MCP unavailable to background subagents.
- `sc-implement-protocol/SKILL.md:121` Q-step scopes review to the task's touched files; lint/tests are extras.
- `sc-workflow-protocol/SKILL.md:4` allowed-tools `Read, Glob, Grep, Write, Edit, Bash, Skill` — no MCP; planning has no impact step.
- `commands/index-repo.md:12-19,72` builds `PROJECT_INDEX.md` from 5 parallel Globs (claims 58K→3K tokens). `commands/load.md:6,27-43` is Serena-memory based. `commands/explain.md:6,48` uses context7 + Read/Grep only.
- Hooks: `hooks/scripts/freshness-*.sh` gate edits on fresh Reads; matcher includes Serena edit tools (INV §4 EDIT).
