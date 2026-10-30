# Socratic dialogue — self-answered (user not available)

Run: `/sc:brainstorm` P3 codegraph opportunities, 2026-10-29. Domain `architecture`, strategy `systematic`, depth `standard` (Clarify + Validate batches, questions 1-10 of the architecture bank in `~/.claude/skills/sc-brainstorm-protocol/refs/socratic-templates.md`).

Answer sources: `.dev/codegraph-migration/research/codegraph-evaluation.md` (cited as `EVAL §n`), `.dev/codegraph-migration/inventory/primitive-usage.md` sections 1 and 4 (cited as `INV §n`), and native Grep of the target primitives (cited by path:line, recorded in `enrichment/codebase-context.md`). No answer adds a codegraph capability beyond EVAL.

## Classification decisions

- **Domain = architecture.** The topic names file paths (code signal) but spans more than 3 components (skills, commands, agents, core, hooks; about 15 named primitives). The taxonomy edge rule says lean `architecture` when ≥3 components.
- **Strategy = systematic.** The literal heuristic lists the word "audit" as an enterprise signal, and the topic contains "audit" only as the name of a skill (`cleanup-audit`) and a review kind, not compliance/regulation. Treated as no enterprise signal. Deviation recorded: a literal reading would select `enterprise`, which would force `--depth deep` (not applicable anyway because `--depth standard` was passed explicitly) and the 5-persona enterprise roster.

## Clarify batch

1. **What problem is the current architecture causing?** Serena is being removed. Beyond its symbol-lookup holes (INV §4: SYM 10 LB rows, REF 3 LB rows), primitives answer structural questions (who calls X, what breaks if X changes, which tests cover this diff) with two tools that cannot answer them exactly: auggie (semantic retrieval, no call graph) and Grep (lexical). Results: review scope is the diff only, test selection is "the changed area" by guess (`sc-pr-submit-protocol/SKILL.md:206` VG-1 `uv run pytest <changed-area>`), and impact before edits is not checked at all in most primitives.
2. **Scope of change?** Guidance text in `src/superclaude/{skills,commands,agents,core,hooks}` (+ `plugins/superclaude/` mirror), `tools:` allowlists, return-contract degraded values, and 3-5 possible new primitives. Not in scope: IronClaude Python CLI code, the installer phase (EVAL §7 owns it), the Serena removal itself (Phase 1).
3. **Constraint hierarchy?** (1) citation correctness (the evidence-validator / hallucination contract must still hold), (2) fail-open availability (codegraph may be absent or not initialized in a worktree), (3) Claude token cost, (4) implementation effort. Avoid hard dependency: upstream is effectively single-maintainer (EVAL §1).
4. **Who maintains it / cross-team coordination?** IronClaude maintainer owns primitives. The Coder image owner owns the baked binary and any per-worktree `codegraph init` hook (EVAL §4, §7 "open follow-ups").
5. **Migration tolerance?** Gradual. Each primitive gains an optional codegraph tier inside its existing fallback ladder; no big-bang rewrite. Each tier must be removable by deleting its lines.

## Validate batch

6. **Patterns already in use — adopt or break?** Adopt: tiered fallback ladders with recorded quality tier (brainstorm `quality_tier`, reuse-auditor `degraded:` list `agents/reuse-auditor.md:131,141`, troubleshoot `mcps_available` `sc-troubleshoot-protocol/SKILL.md:168`); evidence-validator re-Read gate; enforced `tools:` allowlists; installed-path rule (CLAUDE.md). Break from: "MCP tools are unavailable to background subagents" workaround of orchestrator-only MCP work (`sc-cleanup-audit-protocol/SKILL.md:86`) — the codegraph CLI via Bash gives subagents with Bash a graph without MCP.
7. **Data model impact?** None owned by IronClaude: per-worktree `.codegraph/codegraph.db`, self-ignoring (EVAL §2). Direct SQLite queries are possible but the schema is UNVERIFIED (EVAL §6.1), so no idea may depend on it.
8. **API/contract impact?** Return contracts that list degraded components (reflect `degraded_components`, troubleshoot `mcps_available`, reuse-auditor `degraded`) need a `codegraph` value. `tools:` allowlists must name `mcp__codegraph__*` tools only where the body calls them (INV §4 ALLOW hint). Critical: by default codegraph lists only `codegraph_explore` (EVAL §3, `DEFAULT_MCP_TOOLS`); the other 7 tools are not listed unless `CODEGRAPH_MCP_TOOLS` is set. The planned registration env (EVAL §7 step 5) sets only telemetry and update-check vars.
9. **Operational impact?** Index freshness: the daemon watcher runs only while an MCP client is connected; `codegraph sync` fails on the writer lock while a daemon runs (EVAL §5.7); a new sibling worktree is "not initialized" until `codegraph init`; a nested worktree is answered from the parent index with a warning (EVAL §4, §5.8). Accuracy: caller rows give the caller's definition line, not the call-site line (EVAL §5.5); `explore` can pull in unrelated same-word symbols (EVAL §5.6); no text search, no data flow, no diagnostics (EVAL §6).
10. **Rollback story?** Every codegraph step is an optional tier gated on `codegraph_status` / `codegraph status` success; rollback is deleting the tier lines and allowlist entries. No IronClaude state is stored in codegraph.

## Open questions (debate seeds)

- Should primitives prefer the MCP tools or the CLI (`codegraph callers …` via Bash)? CLI works in subagents with Bash and in scripts; MCP works in read-only agents only if allowlisted and listed.
- Is a shared "codegraph grounding" ref/skill worth it, or does each primitive inline 3 lines?
- How much citation accuracy is lost to definition-line caller rows, and must every codegraph-derived citation be re-Read before use?
- Does `codegraph affected` (test-file impact only) improve pr-submit VG-1 enough to replace "changed area" selection, given VG-2 escalation to `make test` exists?
- Is `codegraph_explore` (24,913 characters for one query, EVAL §5.6) a token saving or a token cost compared with auggie (free, server-side) for primitives that already lean on auggie?
