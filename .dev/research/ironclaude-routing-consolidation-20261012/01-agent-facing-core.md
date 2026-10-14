# Research: IronClaude agent-facing framework files (routing consolidation)

**Scope:** /tmp/ic-master/src/superclaude/core/*.md, /tmp/ic-master/CLAUDE.md, AGENTS.md, KNOWLEDGE.md, PROJECT_INDEX.md/.json (snapshot of IronClaude origin/master)
**Status:** Complete
**Date:** 2026-10-12
**Method:** read-only; grep across the whole snapshot; install chain traced in src/superclaude/cli. Line numbers refer to /tmp/ic-master paths unless stated.

---

## 1. Loading chain (how core files reach an agent)

Snapshot identity: `/tmp/ic-master/SNAPSHOT.txt` says "snapshot of origin/master ee1c1787 (2026-10-11)".

### 1.1 Install step [CODE-VERIFIED]

| Step | Evidence | Effect |
|---|---|---|
| `superclaude install` calls `install_core_files(force=force)` as Step 1 | `src/superclaude/cli/main.py:155-161` | copies core files |
| `superclaude update` calls `install_core_files(force=True)` | `src/superclaude/cli/main.py:298,307-310` | always overwrites |
| `install_core_files` globs `core/*.md` and copies EVERY one flat into `~/.claude/` | `src/superclaude/cli/install_core.py:30,39,48-57` | all 13 core `.md` files land at `~/.claude/<NAME>.md` |
| Source dir is `<package>/core` | `install_core.py:89-108` | `src/superclaude/core/` in an editable install |
| `list_installed_core_files` has a HARD-CODED set of the 13 names | `install_core.py:139-153` | renaming or removing a file without editing this set makes `--list` lie |
| Packaging includes core | `MANIFEST.in:15` (`recursive-include src/superclaude/core *.md`); wheel `packages = ["src/superclaude"]` and force-include `src` at `pyproject.toml:79-88` | any new or renamed core file ships automatically |
| `make sync-dev` does NOT copy `core/` | `Makefile:109-160` copies skills, agents, commands, hooks, templates only | inside the repo, core files reach Claude only through `superclaude install`, never through sync-dev |

Side effect worth flagging: because `core/CLAUDE.md` is copied to `~/.claude/CLAUDE.md`, `superclaude update` (force=True) overwrites the user's personal global `~/.claude/CLAUDE.md` with the framework one every time. [CODE-VERIFIED: `install_core.py:51-56` uses `shutil.copy2` with no merge; `main.py:309` passes `force=True`.]

### 1.2 What Claude Code actually loads [CODE-VERIFIED for file content; Claude Code loading behavior is documented platform behavior]

- Claude Code auto-loads `~/.claude/CLAUDE.md` (user memory) in every session. That file is the installed copy of `src/superclaude/core/CLAUDE.md`.
- `src/superclaude/core/CLAUDE.md` contains exactly ONE `@` import: `@BASH_INSPECTION_POLICY.md` (`core/CLAUDE.md:3`). It names RULES.md and PRINCIPLES.md only as prose pointers (`core/CLAUDE.md:94-95`), which are not imports.
- Therefore, of the 13 installed core files, only `CLAUDE.md` and `BASH_INSPECTION_POLICY.md` are in every agent's context. The other 11 (ORCHESTRATOR, COMMANDS, MODES, FLAGS, PERSONAS, MCP, RULES, PRINCIPLES, RESEARCH_CONFIG, BUSINESS_SYMBOLS, BUSINESS_PANEL_EXAMPLES) sit in `~/.claude/` and are NOT auto-loaded.
- History: the original installed entry point imported 8 of them (`@COMMANDS.md @FLAGS.md @PRINCIPLES.md @RULES.md @MCP.md @PERSONAS.md @ORCHESTRATOR.md @MODES.md`, commit `de177847`, 2026-02-13). Commit `4b19eb08` (2026-03-16) removed those imports (found via `git log -S "@ORCHESTRATOR.md" -- src/superclaude/core/CLAUDE.md`). Since then they have been dead weight for always-on context.
- `BASH_INSPECTION_POLICY.md` has two more delivery paths: the SubagentStart hook injects `~/.claude/BASH_INSPECTION_POLICY.md` as additionalContext (`src/superclaude/hooks/scripts/freshness-subagent-start.sh:7,30`), and Python pipelines embed it in generated prompts via `importlib.resources` (`src/superclaude/cli/prompt_policy.py:5-17`, used by `cli/sprint/process.py:22,237` and `cli/tasklist/prompts.py:14,192`).

### 1.3 On-demand reads (who still points an agent at the uninjected files)

| Pointer | Target | Evidence |
|---|---|---|
| sc-task-protocol skill | ORCHESTRATOR.md, MCP.md | `skills/sc-task-protocol/SKILL.md:407-408` ("Circuit breakers: See MCP.md", "Routing logic: See ORCHESTRATOR.md") |
| /sc:research command | RESEARCH_CONFIG.md | `commands/research.md:93,97` |
| deep-research, deep-research-agent agents | RESEARCH_CONFIG.md | `agents/deep-research.md:47`, `agents/deep-research-agent.md:158` |
| MCP_Tavily mode doc | RESEARCH_CONFIG.md | `mcp/MCP_Tavily.md:76` |
| sc-brainstorm-protocol skill | RESEARCH_CONFIG.md | `skills/sc-brainstorm-protocol/SKILL.md:189` |
| sc-tasklist-protocol skill + phase template | BASH_INSPECTION_POLICY.md ("globally installed") | `skills/sc-tasklist-protocol/SKILL.md:120,945`, `templates/phase-template.md:28` |
| MODE_Orchestration | PRINCIPLES.md (principle name only) | `modes/MODE_Orchestration.md:46` |
| core/CLAUDE.md | RULES.md, PRINCIPLES.md (as "referenced by skills") | `core/CLAUDE.md:94-95` |

None of these pointers give a path an agent can resolve reliably: they say "See X.md" with no `~/.claude/` prefix. Whether an agent actually opens the file is UNVERIFIED (no hook or loader code reads them; it depends on the model following a prose pointer).

Out of scope but adjacent: `install_user_setup.py:1-17,28` installs `src/superclaude/rules/{core,contextual,prompts}` into `~/.claude/rules/` and lists them in `claudeMdExcludes`, so those are also on-demand, not always-on. The routing consolidation should check those groups separately.

## 2. Current command / skill / MCP inventory (ground truth)

[CODE-VERIFIED by directory listing of `/tmp/ic-master/src/superclaude/`]

- **Commands (43 `.md`, excluding README):** adversarial, agent, analyze, auggie-review, brainstorm, build, business-panel, cleanup, cleanup-audit, cli-eval, cli-portify, design, document, explain, git, help, implement, improve, index, index-repo, init-lite, load, pm, post-release, pr-submit, recommend, reflect, release-split, research, review-translation, roadmap, save, spawn, spec-panel, swarm-wizard, task, tasklist, tdd, test, troubleshoot, validate-roadmap, validate-tests, workflow.
- **Removed commands:** `estimate`, `select-tool`, `sc` dispatcher, `post-release-update` alias (commit `3ae238b1`, 2026-09-30; `commands/estimate.md`, `select-tool.md`, `sc.md` confirmed absent).
- **Skills (36 with SKILL.md):** ccsession-tag, confidence-check, operational-guide, prd, readme, roadmap, task, task-builder, tdd, tech-reference, tech-research, plus 25 `sc-*` (adversarial, auggie-review, bare-review, brainstorm, cleanup-audit, cli-eval, cli-portify, crash-recovery, implement, init-lite, pm, post-release, pr-submit, recommend, reflect, release-split, review-translation, roadmap, swarm-wizard, task, tasklist, troubleshoot, validate-roadmap, validate-tests, workflow).
- **Changed meanings to watch:** `/sc:implement` is now "Middleweight spec executor" (`commands/implement.md:3`), not a persona-driven feature builder. `/sc:workflow` is now "Generate a phased implementation plan from a PRD, spec, or feature prompt" (`commands/workflow.md:3`). `/sc:tdd` is the Technical Design Document skill (`commands/tdd.md:3`), not test-driven development.
- **MCP servers shipped by `superclaude mcp`:** context7, playwright, serena, morphllm-fast-apply, tavily, auggie, plus the airis-mcp-gateway option (`cli/install_mcp.py:20-26,36-76`). Config JSON also exists for airis-agent and mindbase (`mcp/configs/`).
- **Removed MCPs:** sequential-thinking, magic, chrome-devtools (commit `3ae238b1`; Sequential references scrubbed again in `046a03ab`, 2026-10-03).
- **Framework flags with zero live use:** `--wave-mode` and `--seq`/`--magic` appear in 0 commands, 0 skills, 0 agents, 0 CLI files. `--delegate` in 2 commands, `--uc` and `--loop` in 1 each (help.md listing). Persona flags (`--persona-*`) appear in 0 commands. [CODE-VERIFIED via grep counts over `src/superclaude/{commands,skills,agents,cli}`.] The "wave" orchestration engine described in ORCHESTRATOR/COMMANDS has no implementing code; it is prose only.

## 3. Per-file findings

### 3.1 `src/superclaude/core/CLAUDE.md` (150 lines)

**Purpose and audience.** Agent-facing global entry point. Header "SuperClaude: Framework Context" (`:1`, dash replaced here per style rule). Mixes three audiences: every agent in every repo (Core Rules `:76-87`, Context freshness `:104-150`), IronClaude contributors only (Project Structure `:16-32`, Dev Commands `:34-45`, Component Sync `:47-50`), and users choosing tools (MCP table `:52-60`, Personas table `:62-74`, Skills and Commands `:97-102`).

**Loading.** ALWAYS LOADED. Installed to `~/.claude/CLAUDE.md` by `install_core.py:48-57`; Claude Code reads it as user memory in every session. It pulls in `BASH_INSPECTION_POLICY.md` via `@` at `:3`. Not touched by `make sync-dev`.

**Routing content and accuracy.**

| Lines | Content | Accuracy |
|---|---|---|
| `:52-60` MCP table | auggie, serena, context7, tavily, playwright with flags `--serena --c7 --tavily --play` | Servers correct (no removed MCP listed). Missing morphllm-fast-apply, which `install_mcp.py:57` still ships. The flags are unenforced prose: `--tavily` has 0 uses anywhere in commands/skills/agents/cli. |
| `:62-74` Personas table | 9 personas, "auto-activated by context; override with --persona-X" | STALE. No command uses `--persona-*` (0 hits in `commands/`). Personas are not a runtime mechanism; the real specialist surface is the 43 agents in `src/superclaude/agents/`. Table also omits `performance` and `mentor` that PERSONAS.md defines. |
| `:80` Core Rule 3 | confidence check thresholds and trigger surface | Accurate; matches `skills/confidence-check`. Not routing. |
| `:94-95` Key Docs | "`src/superclaude/core/RULES.md` ... (referenced by skills)" | Wrong path once installed globally (the file lives at `~/.claude/RULES.md`). `PLANNING.md` and `TASK.md` (`:91-92`) do not exist in the snapshot. |
| `:97-102` Skills and Commands | "use `/sc:help` to list all available"; "Full behavioral specs (personas, MCP workflows, wave strategies) live in the skill files" | `/sc:help` exists. The claim that wave strategies live in skill files is false (0 skill hits for `wave-mode`). This is the ONLY always-on "which command when" pointer, and it contains no decision guidance; it defers to `/sc:help` and, implicitly, `/sc:recommend`. |
| `:39` Dev Commands | "`make sync-dev # src/superclaude/{skills,agents,commands}`" | Incomplete: sync-dev also copies hooks and templates (`Makefile` sync-dev block). Contributor-only content installed globally into every user's session. |

**Inbound references.**
- Code / install: `src/superclaude/cli/install_core.py:143` (known_core set); copied by glob at `install_core.py:39`.
- Tests (break on rename or on removing the import): `tests/cli/test_bash_inspection_policy.py:31-33` reads `src/superclaude/core/CLAUDE.md` and asserts `"@BASH_INSPECTION_POLICY.md" in claude_md`.
- Docs: `CHANGELOG.md:155`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:99` and its duplicate `docs/guides/...:99` (both list "Core files (always loaded)" including the 8 no-longer-imported files: stale); `docs/developer-guide/testing-debugging.md:32,72,90` and `docs/reference/diagnostic-reference.md:64` (diagnostic loops over `CLAUDE.md FLAGS.md RULES.md PRINCIPLES.md`).
- `.dev/` history: many; not load-bearing.

**Verdict: KEEP BUT UPDATE.** This is the single always-on agent surface, so it is the natural home for a short, accurate "which command or skill when" table. Required changes: (a) drop or replace the personas table with a pointer to agents, (b) remove unenforced MCP flags or mark them advisory, add morphllm or state it is optional, (c) move the contributor-only sections (Project Structure, Dev Commands, Component Sync) out to the repo-root `CLAUDE.md`, since a globally installed file should not describe IronClaude's own source tree, (d) fix Key Docs paths, (e) add a compact routing table (or an `@` import of one new routing file) covering the current 43 commands and the task-builder / task / prd / tdd / tech-research / roadmap / pr-submit / swarm-wizard / workflow / implement surfaces. What would break if removed: the BASH policy import test (`test_bash_inspection_policy.py:33`) and the global import chain for BASH_INSPECTION_POLICY. Also flag to the owner: `superclaude update` overwrites a user's own `~/.claude/CLAUDE.md` (see 1.1); a consolidation is a good moment to decide whether this file should be appended or imported rather than copied over.

### 3.2 `src/superclaude/core/ORCHESTRATOR.md` (389 lines)

**Purpose and audience.** Agent-facing "Intelligent Routing System" (`:1-3`): request detection, complexity scoring, wave orchestration, master routing table, `/sc:task` tier classification, persona and flag auto-activation, quality gates, emergency protocols.

**Loading.** Installed to `~/.claude/ORCHESTRATOR.md`; NOT imported by any CLAUDE.md since commit `4b19eb08` (2026-03-16). Only on-demand pointer: `skills/sc-task-protocol/SKILL.md:408` ("Routing logic: See ORCHESTRATOR.md"). Effectively not loaded.

**Routing content and accuracy.**

| Lines | Content | Accuracy |
|---|---|---|
| `:5-93` Detection Engine | resource zones, complexity table, domain table, operation table, intent algorithm, wave scoring | Prose only, no implementing code. Operation table names removed MCP Magic at `:69,70`. Resource zones and "historical success rate" (`:28,334`) describe telemetry nothing collects. UNVERIFIED that any agent has ever executed this algorithm. |
| `:99-134` Wave Routing | wave tiers `/analyze /build /implement /improve` then `/design /task` | STALE. `--wave-mode` and related flags have 0 uses in commands, skills, agents, cli. Contradicts COMMANDS.md `:195` which says 7 wave commands incl. `/workflow`. |
| `:136-159` Master Routing Table | 20 pattern rows mapping phrases to personas and flags | STALE. Activates personas and flags (`--ultrathink`, `--delegate --parallel-dirs`, `--multi-agent`, `--wave-*`) that no command consumes. Does not route to ANY current skill (task-builder, task, prd, tdd, tech-research, roadmap, pr-submit, swarm-wizard, reflect, troubleshoot, recommend). "optimize performance" row says "performance persona" (`:147`) but the CLAUDE.md persona table has no performance persona. |
| `:161-236` Tier Classification Routing | `/sc:task` STRICT / EXEMPT / LIGHT / STANDARD decision tree, boosters, compound overrides, tier-to-verification | PARTLY ACCURATE but DUPLICATED and DRIFTED. The live classifier is in `commands/task.md:71-93` (runs before the skill, per `skills/sc-task-protocol/SKILL.md:56`). Drift: ORCHESTRATOR lists "multi-file" as a STRICT keyword (`:195`) and an "all test files: STANDARD +0.2" booster (`:207`), neither in task.md; ORCHESTRATOR tie-break "scores within 0.1 escalate" (`:181-184`) vs task.md "first matching tier wins" (`task.md:71`); task.md has "change api" compound and what/how/why EXEMPT patterns that ORCHESTRATOR lacks. The `config/tier-keywords.yaml` etc. cited by `sc-task-protocol/SKILL.md:404-406` do not exist in the skill dir (only `__init__.py` and `SKILL.md`). |
| `:238-330` Decision Trees, delegation, flag auto-activation, flag precedence | tool selection lists Magic for UI (`:247`); 10 flag precedence rules | STALE (removed MCP; unconsumed flags). |
| `:336-344` 7-step validation cycle | quality gates | Aspirational; no code. |
| `:358-364` MCP quick selection | "Context7 (docs) / Magic (UI) / Playwright (testing)" | STALE: Magic removed; omits auggie, serena, tavily. |

**Inbound references.**
- Code: `src/superclaude/cli/install_core.py:148` (known_core set). `src/superclaude/cli/recommend/prompts.py:16` (docstring only, says the classifier mirrors "core/ORCHESTRATOR.md Tier Classification Routing"; not a file read, will not break at runtime).
- Skills: `src/superclaude/skills/sc-task-protocol/SKILL.md:408`.
- Tests: `tests/sc-roadmap/compliance/test_critical_corrections.py:7,61` mention the name in docstrings only; the assertions read `skill_md_content` (SKILL.md), not ORCHESTRATOR.md (`:63-74`). Will not break on removal.
- Docs: `PROJECT_INDEX.md:48`; `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:99,369,749,1028,1087,1181` and the duplicate `docs/guides/...:99,374,754,1034,1095,1194` (both instruct contributors to "register" every new command in COMMANDS.md and ORCHESTRATOR.md: a stale process instruction).
- `.dev/` and archived release artifacts: about 200 files; historical, not load-bearing.

**Verdict: RETIRE** (after extracting one piece). It is not loaded, its routing table routes to flags and personas nothing reads, and it names a removed MCP. Extract first: nothing, because the `/sc:task` tier rules already live authoritatively in `commands/task.md:71-93`; the ORCHESTRATOR copy is a drifted duplicate. What breaks: the known_core set entry (`install_core.py:148`) must be removed or `--list` shows it as "not installed"; `sc-task-protocol/SKILL.md:408` pointer must be repointed to `commands/task.md`; the `recommend/prompts.py:16` docstring should be repointed; the two developer guides' "register in ORCHESTRATOR.md" steps must be rewritten; `PROJECT_INDEX.md:48` updated. Already-installed users keep a stale `~/.claude/ORCHESTRATOR.md` because install never deletes; a cleanup step in `install_core` would be needed (UNVERIFIED whether any uninstall path exists; none found in `install_core.py`).

### 3.3 `src/superclaude/core/COMMANDS.md` (195 lines)

**Purpose and audience.** Agent-facing "Command Execution Framework" (`:1-3`): per-command auto-persona, MCP, tools, wave eligibility, plus the `/sc:task` flag reference.

**Loading.** Installed to `~/.claude/COMMANDS.md`; not imported; no skill, command, or agent points to it (grep of `src/` returns only `install_core.py:144` and the file itself). NOT LOADED.

**Routing content and accuracy.**

| Lines | Content | Accuracy |
|---|---|---|
| `:23` | "MCP Servers: Context7, Magic, Playwright integration" | STALE (Magic removed; auggie/serena/tavily missing). |
| `:28-33`, `:193-195` | wave-enabled lists: 6 commands then "7 commands ... /workflow" | Self-contradictory and unimplemented. |
| `:37-47` | `/build`, `/implement` auto-persona + "MCP: Magic (UI)" | STALE. `/sc:implement` is now a "Middleweight spec executor" (`commands/implement.md:3`), not persona-routed feature building. |
| `:51-55`, `:63-67`, `:162` | `/analyze`, `/improve`, `/design` list Magic | STALE (removed MCP). |
| `:76-81` | `/cli-eval` with "Subagents: audit-scanner ... audit-validator" | WRONG: those are the cleanup-audit agents; cli-eval uses eval-docs-loader, eval-suite-author, eval-run-reporter (`src/superclaude/agents/eval-*.md`). Copy-paste error. |
| `:89` | `/estimate` | REMOVED command (`3ae238b1`). Also in Planning category `:186`. |
| `:91` and `:95` | `/task` listed twice with different meanings ("Long-term project management" vs unified compliance task) | Contradictory; only the second matches `commands/task.md`. |
| `:101-156` | `/sc:task` flag tables and tier flow | Mostly accurate vs `commands/task.md:19,44`. `--reason` (`:137`) and the "Complexity >=0.7 → STRICT" trigger (`:152`) do not appear in task.md. Duplicates task.md. |
| missing | no entries for adversarial, agent, auggie-review, brainstorm, business-panel, cli-portify, help, index-repo, init-lite, pm, post-release (present, `:85`), pr-submit, recommend, reflect, release-split, research, review-translation, roadmap, save, spec-panel, swarm-wizard, tasklist, tdd, validate-roadmap, validate-tests; and no mention of the standalone skills task-builder, task, prd, tdd, tech-research, tech-reference, roadmap, operational-guide, readme | Covers about 18 of 43 commands and 0 of the non-sc skills. |

**Inbound references.**
- Code: `src/superclaude/cli/install_core.py:144`.
- Tests: none.
- Docs: `PROJECT_INDEX.md:44`; both developer guides at the same lines as ORCHESTRATOR (`:99,368/373,749/754,1028/1034,1087/1095,1181/1194`).
- `.dev/`: about 110 historical files.

**Verdict: RETIRE, MERGE the idea INTO the one routing surface.** As a per-command spec it duplicates each command's own frontmatter and body, and it is wrong in 7+ places. The consolidated "which command when" table (see 3.1 verdict) should be generated from or checked against `src/superclaude/commands/*.md` frontmatter `description:` lines rather than hand-maintained here. What breaks: `install_core.py:144` set entry; developer-guide "register in COMMANDS.md" steps; `PROJECT_INDEX.md:44`. No code or test reads it.

### 3.4 `src/superclaude/core/PERSONAS.md` (214 lines)

**Purpose and audience.** Agent-facing persona system: 11 personas (architect, frontend, security, backend, analyzer, mentor, refactorer, performance, qa, devops, scribe) with priorities, MCP preferences, command lists, and an auto-activation scoring formula (`:53-189`).

**Loading.** Installed to `~/.claude/PERSONAS.md`; not imported. Only referenced by ORCHESTRATOR.md `:305,368` (itself unloaded). NOT LOADED.

**Routing content and accuracy.**
- Auto-activation formula "keyword 30%, context 40%, user history 20%, performance metrics 10%" (`:189`): no code implements it. UNVERIFIED as behavior.
- Every persona lists "Avoided: Magic" or "Primary: Magic" (`:65,84,104,117,135,144,154,163,172,183`): Magic is a removed MCP.
- Command lists use `/estimate` (`:66`, removed) and sub-flags `--arch`, `--perf`, `--security`, `--api`, `--detailed`, `--benchmark` (`:66,85,105,118,127,155`) that do not appear in `commands/improve.md`, `build.md`, `explain.md`, `test.md`, or `analyze.md` (grep returned 0 hits).
- `--persona-*` flags: 0 uses in `src/superclaude/commands/`.
- The real specialist routing today is agent-based: `src/superclaude/agents/` has backend-architect, frontend-architect, security-engineer, performance-engineer, quality-engineer, refactoring-expert, devops-architect, technical-writer, learning-guide, root-cause-analyst, system-architect, socratic-mentor, which cover the same domains as the 11 personas.

**Inbound references.**
- Code: `install_core.py:149`. Persona keyword appears in `cli/roadmap/prompts.py` (grep for `persona-`), but as roadmap prompt text, not a read of PERSONAS.md (UNVERIFIED whether that text depends on this file's definitions; no file read found).
- Tests: none.
- Docs: `PROJECT_INDEX.md:43` ("9 personas", while the file defines 11); both developer guides `:99,371/376,1029/1035`.
- Core: `ORCHESTRATOR.md:305,368`; the 9-row persona table is duplicated in `core/CLAUDE.md:62-74`.

**Verdict: RETIRE.** Replace the always-on persona table in `core/CLAUDE.md` with a short "domain to agent" pointer if any persona guidance is kept. What breaks: `install_core.py:149` set entry; `ORCHESTRATOR.md` cross-refs (moot if ORCHESTRATOR is retired); developer-guide registration steps; `PROJECT_INDEX.md:43`.

### 3.5 `src/superclaude/core/MODES.md` (307 lines)

**Purpose and audience.** Agent-facing consolidated mode reference: Task Management (`:15-63`), Introspection (`:65-136`), Token Efficiency incl. symbol system (`:138-275`), and short Brainstorming (`:277-285`), Deep Research (`:287-297`), Orchestration (`:299-307`) blocks.

**Loading.** Installed to `~/.claude/MODES.md`; not imported; no skill, command, or agent points to it. NOT LOADED. Note: the separate per-mode files in `src/superclaude/modes/MODE_*.md` (7 files) are packaged (`MANIFEST.in:13`) but NOT installed by any CLI installer (grep of `src/superclaude/cli/` for `modes` finds only unrelated `failure_modes`), so they are not loaded either. MODES.md is a merged duplicate of those 7 files (the original `de177847` entry point said "Merged into MODES.md: Brainstorming, DeepResearch, Orchestration, Introspection, Task Management, Token Efficiency").

**Routing content and accuracy.**
- Task Management layers (`:24-46`): "Layer 2: /task Command (Project Management) ... Epic → Story → Task" contradicts the current `/sc:task` (compliance-tiered executor, `commands/task.md`). "Layer 4: /loop Command" (`:43-46`): no `/loop` command exists (`commands/loop.md` absent). It does not mention task-builder / task MDTM skills, which are the current multi-session task mechanism.
- Mode triggers: `--brainstorm`, `--research`, `--introspect`, `--task-manage`, `--uc` (`:279,289` and FLAGS). The live routes are `/sc:brainstorm` and `/sc:research` commands; the flags appear only in `commands/help.md` listings.
- Orchestration tool selection (`:305`): "Magic (UI) | Serena | Morphllm | Context7 | Playwright | MultiEdit": Magic removed; omits auggie and tavily.
- Cross-refs `RULES.md`, `PRINCIPLES.md` (`:80`) and `MCP.md §Caching Strategies` (`:273`).

**Inbound references.**
- Code: `install_core.py:147` only.
- Tests: none. (The "3 TodoWrite states" test at `tests/sc-roadmap/compliance/test_critical_corrections.py:77-88` checks the roadmap SKILL.md, not MODES.md, which lists 4 states incl. `blocked` at `:29,58-61`.)
- Docs: `PROJECT_INDEX.md:47`; both developer guides `:99`; `docs/developer-guide/technical-architecture.md:37-43,144-150,333` describes `@MODE_*.md` imports and `~/.claude/MODE_NewMode.md` that no longer exist; `docs/mcp/mcp-integration-policy.md:459,473` (`~/.claude/superclaude/modes/` path not produced by any installer).

**Verdict: RETIRE.** No live consumer, contains removed-MCP routing and nonexistent commands. If the Token Efficiency symbol legend is still wanted, it already exists in `src/superclaude/modes/MODE_Token_Efficiency.md`; decide separately whether `modes/` should be installed or deleted (it is a second dead copy). What breaks: `install_core.py:147` set entry, `PROJECT_INDEX.md:47`, docs listed above.

### 3.6 `src/superclaude/core/FLAGS.md` (146 lines)

**Purpose and audience.** Agent-facing behavioral flag catalog: mode flags (`:5-30`), MCP flags (`:32-72`), depth flags (`:74-89`), execution control (`:91-121`), output (`:123-138`), priority rules (`:140-146`). Each flag lists a "Trigger" (auto-activation condition) and "Behavior".

**Loading.** Installed to `~/.claude/FLAGS.md`; not imported; no skill, command, or agent cites it. NOT LOADED.

**Routing content and accuracy.**
- MCP flags (`:34-72`): c7, morph, serena, play, tavily, frontend-verify, all-mcp, no-mcp. Clean of removed MCPs since `3ae238b1`. Missing auggie, which `core/CLAUDE.md:56` calls the auto-first codebase tool. `--frontend-verify` has 0 uses in commands and skills. `--tavily` has 0 uses.
- Auto-activation "Triggers" (e.g. `--delegate` at ">7 directories OR >50 files" `:95`, `--safe-mode` at "Resource usage >85%" `:120`) are prose with no implementing hook or code. UNVERIFIED as behavior.
- Flags that ARE consumed by individual commands: `--focus` (8 commands, 14 skills), `--scope` (3 commands, 9 skills), `--validate` (7 commands, 8 skills), `--no-mcp` (3 commands, 7 skills, 7 CLI files), `--iterations` (2 commands), `--concurrency` (1). Those commands define their own flags locally, so FLAGS.md is not their source.
- A drifted second copy exists at `plugins/superclaude/core/FLAGS.md` (2 differing lines vs src).

**Inbound references.**
- Code: `install_core.py:145`.
- Tests: none.
- Docs: `PROJECT_INDEX.md:45`; developer guides `:99,370/375,1029/1035`; `docs/developer-guide/testing-debugging.md:32,72,90` (diagnostic `for file in CLAUDE.md FLAGS.md RULES.md PRINCIPLES.md` would report a missing file after removal); `docs/developer-guide/contributing-code.md:64`; `docs/developer-guide/technical-architecture.md:27,133` (describes `@FLAGS.md` import that no longer exists); `docs/reference/diagnostic-reference.md:64`; `docs/reference/comprehensive-features.md:99`. Human-facing flag doc `docs/user-guide/flags.md` covers the same ground (owned by the human-docs track).

**Verdict: MERGE INTO the consolidated routing surface, then RETIRE the file.** The few cross-command flags that are real and shared (`--focus`, `--scope`, `--validate`, `--no-mcp`, the `--think*` depth trio) deserve one short always-on line in the routing table; the auto-activation triggers should be dropped because nothing enforces them. What breaks: `install_core.py:145`; diagnostic snippets in `testing-debugging.md:72` and `diagnostic-reference.md:64` (shell loops expecting the file); doc pointers above.

### 3.7 `src/superclaude/core/MCP.md` (213 lines)

**Purpose and audience.** Agent-facing MCP server selection and orchestration reference: selection algorithm (`:5-15`), Context7 (`:17-45`), Playwright (`:47-86`), Auggie (`:88-120`), use cases by command category (`:122-160`), orchestration and caching (`:162-178`), circuit breakers (`:180-213`).

**Loading.** Installed to `~/.claude/MCP.md`; not imported. On-demand pointers: `skills/sc-task-protocol/SKILL.md:407` ("Circuit breakers: See MCP.md"), `core/ORCHESTRATOR.md:362,380`, `core/MODES.md:273`, `core/RESEARCH_CONFIG.md:133`. Effectively not loaded.

**Routing content and accuracy.**
- No sections for Serena, Tavily, or Morphllm, although all three are shipped (`cli/install_mcp.py:50,57,66`) and Serena is the STRICT-tier required server (`:205`). Tavily routing actually lives in RESEARCH_CONFIG.md and `src/superclaude/mcp/MCP_Tavily.md`.
- Clean of Magic and Sequential in this file (grep found none).
- "Use Cases by Command Category" (`:122-160`) uses abstract categories, not command names; "Loop Command" (`:159`) does not exist; "Scribe Persona" (`:144`) is an unloaded persona.
- Circuit breaker table (`:188-195`) and tier-to-server table (`:199-206`) duplicate `skills/sc-task-protocol/SKILL.md:285-295`. No code implements the thresholds (grep of `cli/` for circuit breaker found none relevant). UNVERIFIED as behavior.
- A per-server doc set already exists at `src/superclaude/mcp/MCP_*.md` (Airis-Agent, Auggie, Context7, Mindbase, Morphllm, Playwright, Serena, Tavily), also packaged but not installed by the CLI.

**Inbound references.**
- Code: `install_core.py:146`.
- Skills: `skills/sc-task-protocol/SKILL.md:407`.
- Tests: none.
- Docs: `PROJECT_INDEX.md:46`; developer guides `:99`; about 150 `.dev/` historical files.

**Verdict: MERGE the one real routing fact (which MCP for what, plus the STRICT tier needs Serena) INTO the routing table in `core/CLAUDE.md`, then RETIRE.** `core/CLAUDE.md:52-60` already carries a better, more current MCP table. Repoint `sc-task-protocol/SKILL.md:407` to its own `:285-295` section. What breaks: `install_core.py:146`; the SKILL.md pointer; `RESEARCH_CONFIG.md:133` cross-ref; `PROJECT_INDEX.md:46`.

### 3.8 `src/superclaude/core/RULES.md` (260 lines)

**Purpose and audience.** Agent-facing behavioral rules with priority markers: rule priority (`:5-16`), agent orchestration (`:18-49`), workflow (`:51-67`), verification before recommendation (`:69-82`), planning efficiency (`:83-95`), completeness, scope, code organization, workspace hygiene, failure investigation, honesty, git, tool optimization (`:203-218`), file organization, safety, temporal awareness (`:248-260`).

**Loading.** Installed to `~/.claude/RULES.md`; not imported. `core/CLAUDE.md:94` says it is "full behavioral rules (referenced by skills)", but grep of `src/superclaude/{skills,agents,commands,hooks,rules}` finds only one mention, `skills/sc-auggie-review-protocol/refs/auggie-prompts.md:153`, which says pointing Auggie at RULES.md "could be a future extension". [CODE-CONTRADICTED: no skill reads it.] Cross-refs from `ORCHESTRATOR.md:350` and `RESEARCH_CONFIG.md:15` ("See RULES.md §Planning Efficiency"). NOT LOADED.

**Routing content and accuracy.** Mostly behavior, not routing. Routing-relevant pieces:
- `:22-28` "Claude Code automatically selects appropriate specialist agents ... `@agent-[name]` prefix routes directly": generic Claude Code behavior; no IronClaude code. Acceptable.
- `:30-49` PM Agent auto-activates "after task completion", "immediately when errors occur", "Monthly Maintenance": no hook or code triggers `pm-agent` automatically (UNVERIFIED; the only PM entry points found are `/sc:pm` and `skills/sc-pm-protocol`).
- `:62-63` "Session Lifecycle: Initialize with /sc:load ... save before end": `/sc:load` and `/sc:save` exist. Accurate as commands; the "30 min checkpoint" is unenforced.
- `:210` "morphllm for bulk edits, context7 for docs": current MCPs. Accurate.
- `:69-82` Verification Before Recommendation: duplicated nearly word for word in `core/CLAUDE.md:80` (Core Rule 3), which IS loaded.
- Overlap: `src/superclaude/rules/core/` (10 files incl. `tool_selection.md`, `quality_gates.md`, `anti_hallucination_task_completion_rules.md`) is installed to `~/.claude/rules/core/` by `install_user_setup.py:28` and covers tool selection and completion honesty again. A third copy of RULES.md sits at `plugins/superclaude/core/RULES.md` (identical).

**Inbound references.**
- Code: `install_core.py:152`.
- Tests: none.
- Core: `core/CLAUDE.md:94`, `ORCHESTRATOR.md:350`, `MODES.md:80`, `RESEARCH_CONFIG.md:15`.
- Skills: `sc-auggie-review-protocol/refs/auggie-prompts.md:153` (non-load-bearing).
- Docs: `PROJECT_INDEX.md:41`; developer guides `:99`; `docs/developer-guide/testing-debugging.md:72`, `contributing-code.md:64`, `docs/reference/diagnostic-reference.md:64`, plus 2 more under `docs/reference/`.

**Verdict: KEEP BUT UPDATE (low routing priority).** It is the fullest statement of behavioral rules and is the target of several prose pointers, but it is not loaded, so today it changes no agent's behavior. For the routing consolidation: strip the PM Agent auto-activation claims (`:30-49`) or mark them aspirational, and either `@`-import a trimmed version from `core/CLAUDE.md` or fold its unique rules into `src/superclaude/rules/core/` and retire it. That choice belongs to the rules-consolidation owner, not the routing work. What breaks on removal: `install_core.py:152`, the CLAUDE.md Key Docs pointer, diagnostic shell loops in docs.

### 3.9 `src/superclaude/core/PRINCIPLES.md` (68 lines)

**Purpose and audience.** Agent-facing engineering philosophy: core directive (`:3`), SOLID, systems thinking, decision framework, quality quadrants.

**Loading.** Installed to `~/.claude/PRINCIPLES.md`; not imported. Pointers: `core/CLAUDE.md:95` ("referenced by skills", CODE-CONTRADICTED as for RULES.md), `modes/MODE_Orchestration.md:46` (principle name only), `MODES.md:80`. NOT LOADED.

**Routing content.** None. No commands, skills, flags, or MCPs named.

**Inbound references.** Code: `install_core.py:150`. Tests: none. Docs: `PROJECT_INDEX.md:42`; developer guides `:99`; `testing-debugging.md:72`, `diagnostic-reference.md:64`, `contributing-code.md:64`, and 2 under `docs/reference/`. Identical copy at `plugins/superclaude/core/PRINCIPLES.md`.

**Verdict: KEEP AS IS for routing purposes (out of routing scope).** No routing content, so nothing to consolidate. Separately note it is not loaded; whether to import or retire it is a rules question.

### 3.10 `src/superclaude/core/RESEARCH_CONFIG.md` (142 lines)

**Purpose and audience.** Agent-facing configuration for deep research: defaults (`:3-28`), strategy selection (`:36-42`), source credibility (`:44-56`), Tavily depth profiles (`:58-78`), multi-hop patterns, discovery routing (`:89-98`), output formats, error handling, MCP roles (`:135-142`).

**Loading.** Installed to `~/.claude/RESEARCH_CONFIG.md`; not imported. It is the most actively referenced on-demand core file: `commands/research.md:93,97`, `agents/deep-research.md:47`, `agents/deep-research-agent.md:158`, `mcp/MCP_Tavily.md:76`, `skills/sc-brainstorm-protocol/SKILL.md:189`, `examples/deep_research_workflows.md:473`. Whether agents open it at runtime is UNVERIFIED (prose pointers only, no path given).

**Routing content and accuracy.**
- Routing is internal to research (which Tavily tool at which depth, `:58-98`), not "which command when". Accurate against `mcp__tavily__tavily_map` / `_crawl` naming (normalized in commit `156f2829`).
- Drift: `:62` says "Tavily MCP version: 0.2.20 (pinned)" but `src/superclaude/cli/install_mcp.py:31` pins `TAVILY_MCP_VERSION = "0.2.22"`. [CODE-CONTRADICTED.]
- `:13` "sequential_override_requires_justification" refers to sequential execution, not the removed Sequential MCP. Clean.
- `:133` cross-refs MCP.md (retire candidate) and `:15` RULES.md.
- Drifted older copy at `plugins/superclaude/core/RESEARCH_CONFIG.md` (492 differing lines) and a `.secrets.baseline:178-181` entry for that plugin copy.

**Inbound references.**
- Code: `install_core.py:151`.
- Tests (BREAK on rename, move, or table-format change): `tests/core/test_research_config.py:13` reads `src/superclaude/core/RESEARCH_CONFIG.md` and parses the Depth Profiles rows; `tests/commands/test_research_command.py:13,35,46,50` asserts `/sc:research` tiers match this file's Depth Profiles header and rows.
- Commands, agents, skills, mcp docs: listed above.
- Docs: `docs/reference/...` (1), plus `.dev/` history.

**Verdict: KEEP BUT UPDATE (fix Tavily version at `:62` to match `install_mcp.py:31`, or drop the hard-coded number and point to `install_mcp.py`).** It is a domain config consumed by research surfaces and guarded by two tests, not part of the general routing layer. Do not merge into the routing table. Removal or rename breaks 2 test files plus 6 prose pointers.

### 3.11 `src/superclaude/core/BUSINESS_SYMBOLS.md` (225 lines)

**Purpose and audience.** Agent-facing symbol legend for business panel output (`:1-3`), tables of emoji and their meanings.

**Loading.** Installed to `~/.claude/BUSINESS_SYMBOLS.md`; not imported; NO pointer from `commands/business-panel.md`, `agents/business-panel-experts.md`, `modes/MODE_Business_Panel.md`, or any skill (grep of `src/superclaude/{commands,skills,agents,modes}` for `BUSINESS_` returns nothing). The `/sc:business-panel` command mentions `--structured` "Use symbol system" (`commands/business-panel.md:78`) without naming the file. NOT LOADED by any path. The original entry point said "On-demand via skills: BUSINESS_PANEL_EXAMPLES, BUSINESS_SYMBOLS, RESEARCH_CONFIG, MODE_Business_Panel" (commit `de177847`), but no skill was ever wired to it in the current tree.

**Routing content.** None.

**Inbound references.** Code: `install_core.py:142`. Tests: none. Docs: `docs/reference/comprehensive-features.md:102`. Near-identical copy (1 line differs) at `plugins/superclaude/core/BUSINESS_SYMBOLS.md`.

**Verdict: MERGE INTO `agents/business-panel-experts.md` or `commands/business-panel.md` (as a ref the command explicitly reads), or RETIRE.** It is orphaned. Not a routing file. What breaks on removal: `install_core.py:142` set entry and one doc line.

### 3.12 `src/superclaude/core/BUSINESS_PANEL_EXAMPLES.md` (218 lines)

**Purpose and audience.** Usage examples for `/sc:business-panel` (`:1-60`), cross-command integration (`:68-92`), expert selection (`:94-114`), output formats.

**Loading.** Same as 3.11: installed, never imported, no pointer from any command, agent, mode, or skill. NOT LOADED.

**Routing content and accuracy.**
- `:73,81,89` route business analysis through `/analyze ... --business-panel`, `/improve ... --business-panel --iterative`, `/design ... --business-panel`. `--business-panel` has 0 uses in `src/superclaude/commands/`. [CODE-CONTRADICTED.]
- Flags used in examples but absent from `commands/business-panel.md`: `--christensen-focus`, `--porter-focus`, `--interaction`, `--symbols`, `--budget`, `--depth`, `--experts-max`, `--iterative`, `--quick`, `--comprehensive`, `--validate` (diff of `--flag` tokens between the two files).
- `:168-169` workflow chains "/improve roadmap", "/implement mitigation --validate": `/sc:implement` is now a spec executor (`commands/implement.md:3`).

**Inbound references.** Code: `install_core.py:141`. Tests: none. Docs: `docs/reference/comprehensive-features.md:101`. Drifted copy at `plugins/superclaude/core/BUSINESS_PANEL_EXAMPLES.md` (136 differing lines).

**Verdict: RETIRE (or move the still-valid `/sc:business-panel` examples into the command file's own Examples section after pruning nonexistent flags).** What breaks: `install_core.py:141` set entry, one doc line.

### 3.13 `src/superclaude/core/BASH_INSPECTION_POLICY.md` (93 lines)

**Purpose and audience.** Agent-facing execution policy: batch five or more serial Bash inspections into one generated script (`:1-25` and following), eligibility, limits (`:70-71`).

**Loading.** ALWAYS LOADED through three channels: `@` import from `core/CLAUDE.md:3`; SubagentStart hook injection (`hooks/scripts/freshness-subagent-start.sh:7,30`); embedded in Python-generated prompts via `cli/prompt_policy.py:5-17` (sprint `process.py:237`, tasklist `prompts.py:192`). Also cited by `skills/sc-tasklist-protocol/SKILL.md:120,945` and `templates/phase-template.md:28`.

**Routing content.** None ("which tool" only in the narrow sense of preferring Read / search / MCP over Bash, `:22-24`).

**Inbound references.**
- Code (BREAK on rename or move): `cli/prompt_policy.py:5,10` (hard-coded filename under package `core/`, raises `RuntimeError` at import if missing, `:13-14`), `cli/install_core.py:140`, `hooks/scripts/freshness-subagent-start.sh:7`, `cli/sprint/process.py:22,237`, `cli/tasklist/prompts.py:14,192`.
- Tests (BREAK): `tests/cli/test_bash_inspection_policy.py:7-44` (content assertions, CLAUDE.md import assertion, install listing), `tests/hooks/test_freshness_subagent_start_policy.py:16,22`, `tests/tasklist/test_prd_prompts.py:14,120`, `tests/tasklist/test_bash_policy_contract.py:23`, `tests/sprint/test_process.py:9,104`.
- Docs: `docs/user-guide/...` (1).

**Verdict: KEEP AS IS.** It is the only core file besides CLAUDE.md that is genuinely live, it is code-loaded, and it has no routing content to consolidate. Renaming it would break 5 code sites and 5 test files.

### 3.14 `/tmp/ic-master/CLAUDE.md` (repo root, 401 lines)

**Purpose and audience.** Contributor-facing agent instructions for sessions working INSIDE the IronClaude repo: UV rule (`:5-7`), the /sc: skill-invocation rule (`:9-14`), never stage `.claude/` (`:16-33`), PR target is the fork (`:35-60`), structure, workflow, sync, worktrees (`:256-291`), PM agent patterns, MCP guidance (`:320-341`), install (`:343-383`), package info (`:385-401`).

**Loading.** Auto-loaded as project memory by Claude Code when the working directory is the IronClaude repo (platform behavior). NOT shipped to users: `MANIFEST.in` and `pyproject.toml` wheel/sdist includes do not list it (`MANIFEST.in:1-33`, `pyproject.toml:79-99`), and `install_core` copies only `src/superclaude/core/*.md`. In a contributor session both this file and `~/.claude/CLAUDE.md` (the installed `core/CLAUDE.md`) load, so UV rules, project structure, sync, and confidence thresholds appear twice.

**Routing content and accuracy.**

| Lines | Content | Accuracy |
|---|---|---|
| `:9-14` | "When ANY message starts with /sc:<command>, you MUST invoke the corresponding skill via the Skill tool" | ACCURATE and load-bearing. Matches the command-file pattern (e.g. `commands/task.md:161` defers to `sc-task-protocol`). This is the most important routing rule in the repo and is NOT in `core/CLAUDE.md`, so end users never receive it. Candidate to move into `core/CLAUDE.md`. |
| `:206-210` | "Commands installed to: `~/.claude/commands/`. Available: /pm, /research, /index-repo, and 27 others" | STALE: 43 commands (not 30), installed to `~/.claude/commands/sc/` (`main.py:32`). |
| `:320-341` | "Recommended: airis-mcp-gateway"; "HIGHET PRIORITY SERVER Auggie"; high priority Tavily, Context7, Serena, Mindbase; optional Playwright | Partly accurate: gateway and servers exist in `install_mcp.py:20-76`. Conflicts with `core/CLAUDE.md:52-60` (no gateway, no Mindbase, adds playwright as peer). Two always-on MCP guides with different advice. Typo "HIGHET". |
| `:122` | "make sync-dev # Copy src/superclaude/{skills,agents} → .claude/" | Incomplete: also commands, hooks, templates (Makefile sync-dev). |
| `:74,77,206,345,388` | "v4.2.0" | STALE: `pyproject.toml:7` is 4.3.5 (and `VERSION` file says 3.7). |
| `:357` | `./install.sh` | File does not exist in the snapshot. |
| `:380-383` | "Plugin System (v5.0 - Not Yet Available) ... See `docs/plugin-reorg.md`" | `docs/plugin-reorg.md` does not exist; `.claude-plugin/plugin.json` does exist at repo root. |
| `:245-252` | branch from `integration` | Conflicts with `:55` and core rules that target `master` on the fork. UNVERIFIED whether an `integration` branch is still used. |

No table of "which command when" exists in this file.

**Inbound references.**
- Code: none that read this specific file (`pm_agent/confidence.py:125` checks for any `project_root / "CLAUDE.md"`, generic; `agents/pm-agent.md` and `agents/rf-task-researcher.md:120` refer to project CLAUDE.md generically).
- Tests: none found that read the repo-root CLAUDE.md (grep of `tests/` for `CLAUDE.md` hits only `test_bash_inspection_policy.py`, which reads `core/CLAUDE.md`).
- Docs: many under `docs/` and `.dev/`; generic.

**Verdict: KEEP BUT UPDATE.** It is the contributor entry point and owns repo-only safety rules (`.claude/` staging, fork PR target, worktree location) that must stay. For routing: (a) copy the /sc: skill-invocation rule (`:9-14`) into `core/CLAUDE.md` so users get it, (b) replace the stale "27 others" line with a pointer to the single routing table, (c) reconcile the MCP section with `core/CLAUDE.md` so only one MCP guide exists (keep it in core, point here), (d) receive the contributor-only sections removed from `core/CLAUDE.md` (see 3.1), (e) fix version, install.sh, plugin-reorg, sync-dev scope. Nothing breaks on edit; no code or test depends on its text.

### 3.15 `/tmp/ic-master/AGENTS.md` (44 lines)

**Purpose and audience.** Generic "Repository Guidelines" for coding agents that read the AGENTS.md convention (for example Codex). Structure, build, style, tests, commits, plugin deploy.

**Loading.** Claude Code does not auto-load AGENTS.md (platform behavior; UNVERIFIED for the exact Claude Code version in use). Not installed, not packaged, not imported by any CLAUDE.md. Referenced only as a filename in `PROJECT_INDEX.json:125` and as a generic doc-type label in `src/superclaude/templates/documents/readme_template.md:541` and `src/superclaude/skills/readme/SKILL.md:1998`.

**Routing content.** None (no commands, skills, or MCPs).

**Accuracy (staleness).** `:7,17,31` describe `pm/`, `research/`, `index/` TypeScript agents: none of those directories exist. `:43-44` `make install-plugin`, `make reinstall-plugin`: no such Makefile targets (only `install`, `test-plugin`, `build-plugin`, `sync-plugin-repo`). `:39` CODEOWNERS: no CODEOWNERS file at root or `.github/`. `:8` `skills/` and `commands/` at root: these exist but are legacy mirrors, not the source of truth (`src/superclaude/`).

**Inbound references.** Code: none. Tests: none. Docs: `PROJECT_INDEX.json:125`; ~20 `.dev/` files.

**Verdict: RETIRE, or KEEP BUT UPDATE as a 10-line pointer to `CLAUDE.md`** if non-Claude agents are expected to work in the repo. It carries no routing content and most of its facts are wrong. Nothing breaks on removal except the `PROJECT_INDEX.json:125` listing.

### 3.16 `/tmp/ic-master/KNOWLEDGE.md` (325 lines)

**Purpose and audience.** Contributor and agent knowledge base of debugging lessons (`:1-9`): freshness system F1-F5 (`:12-142`), anti-instinct gate (`:156`), obligation scanner (`:209`), roadmap tokenizer fix (`:223`), sprint 429 recovery (`:269`).

**Loading.** Not auto-loaded. Pointed to by repo-root `CLAUDE.md:97,295`, `core/CLAUDE.md:93` (which, once installed globally, points users at a repo-relative file that is not in their project), `README.md:202`, `docs/user-guide/commands.md:137,1673`. A code comment cites it at `src/superclaude/cli/roadmap/structural_checkers.py:300`. `src/superclaude/cli/audit/profiler.py:47` lists "KNOWLEDGE.md" as a docs path pattern (generic classifier, not a read).

**Routing content.** None. Domain lessons only.

**Inbound references.** Code: `cli/roadmap/structural_checkers.py:300` (comment), `cli/audit/profiler.py:47` (pattern string). Tests: none. Docs: as above, plus ~110 `.dev/` files.

**Verdict: KEEP AS IS (out of routing scope).** One fix belongs to the routing work: remove the `KNOWLEDGE.md` pointer from `core/CLAUDE.md:93`, because the installed global file should not point at a file that only exists in the IronClaude repo.

### 3.17 `/tmp/ic-master/PROJECT_INDEX.md` (298 lines) and `PROJECT_INDEX.json` (245 lines)

**Purpose and audience.** Generated repository index for fast agent orientation, produced by `/sc:index-repo` (`src/superclaude/commands/index-repo.md:13,72`) and the `repo-index` agent (`src/superclaude/agents/repo-index.md:15`, "Generate/update ... when stale (>7 days)").

**Loading.** Not auto-loaded. Read on demand by agents following `/sc:index-repo` guidance; `docs/user-guide/commands.md:1478` explicitly says reading it each session "is not required". `src/superclaude/execution/reflection.py:321` checks whether `<repo>/PROJECT_INDEX.md` exists and is under 7 days old to adjust a confidence score (generic, exported from `execution/__init__.py:23,82`).

**Routing content and accuracy.** It lists commands, agents, skills, MCPs, which makes it an accidental routing catalog, and it is badly stale:
- `PROJECT_INDEX.md:2-4` "Generated 2026-03-23, Version 4.2.0"; `PROJECT_INDEX.json` metadata "generated_at 2025-10-29, version 0.4.0".
- `PROJECT_INDEX.md:170-181` "38 command definitions" incl. `sc.md` dispatcher (removed), `task-unified.md`, `sprint.md` (neither exists in `src/superclaude/commands/`). Actual: 43.
- `:183-197` "29 agent definitions": actual 43 (missing rf-*, eval-*, reuse-auditor, evidence-validator, confidence-calibrator, auggie-reviewer, reflect-reviewer).
- `:199-216` "13 skill packages" incl. `sc-recommend-protocol`, `sc-task-unified-protocol` (actual names `sc-recommend`, `sc-task-protocol`); missing task, task-builder, prd, tdd, tech-research, tech-reference, roadmap, pr-submit, swarm-wizard, workflow, implement, reflect, troubleshoot and more. Actual: 36.
- `:218-235` MCP table lists Sequential, Magic, Chrome DevTools (all removed in `3ae238b1`). `PROJECT_INDEX.json:233` "sequential".
- `:41-48` core file comments (e.g. "PERSONAS.md # 9 personas") feed the same misconceptions retired above.

**Inbound references.**
- Code: `src/superclaude/execution/reflection.py:321` (existence and age only; filename hard-coded; removing the repo's copy lowers a confidence score, does not crash).
- Commands / agents that generate it: `src/superclaude/commands/index-repo.md:13,72,160-161`, `src/superclaude/agents/repo-index.md:15,28-29`, legacy mirrors `commands/sc-index-repo.md`, `agents/sc-repo-index.md`, `plugins/superclaude/commands/index-repo.md`, `plugins/superclaude/agents/repo-index.md`.
- Tests: none.
- Docs: `README.md:203`, `docs/user-guide/commands.md:66,771,1402,1462,1470,1486,1515,1668`, `docs/generated/contributor-knowledge-base/repository-overview.md:94`.

**Verdict: KEEP BUT UPDATE (regenerate with `/sc:index-repo`), and do NOT treat it as a routing source.** It is generated output, so the fix is regeneration, not hand edits. The consolidated routing table should not depend on it. Nothing breaks on regeneration; deleting it only affects the reflection confidence bonus.

---

## 4. Summary

### 4.1 Verdict table

| File | Loaded into agent context? | Routing content | Verdict |
|---|---|---|---|
| core/CLAUDE.md | YES, always (installed as `~/.claude/CLAUDE.md`) | MCP table, persona table, `/sc:help` pointer | KEEP BUT UPDATE: make it the one routing home |
| core/BASH_INSPECTION_POLICY.md | YES, always (`@` import, SubagentStart hook, Python prompts) | none | KEEP AS IS |
| core/ORCHESTRATOR.md | no (import removed 2026-03-16) | master routing table, wave rules, `/sc:task` tiers (drifted copy) | RETIRE |
| core/COMMANDS.md | no | per-command table, about 18 of 43 commands, `/estimate`, Magic | RETIRE (idea merged into routing table) |
| core/PERSONAS.md | no | persona auto-activation, `/estimate`, Magic | RETIRE |
| core/MODES.md | no | mode triggers, `/loop`, Magic | RETIRE |
| core/FLAGS.md | no | flag auto-activation | MERGE the few real shared flags into routing table, then RETIRE |
| core/MCP.md | no (one skill pointer) | MCP selection, circuit breakers | MERGE one MCP line into routing table, then RETIRE |
| core/RULES.md | no (prose pointers only) | small (PM auto-activation claims) | KEEP BUT UPDATE (rules owner decides import vs fold into `rules/core/`) |
| core/PRINCIPLES.md | no | none | KEEP AS IS (out of routing scope) |
| core/RESEARCH_CONFIG.md | on demand (6 pointers) | research-internal Tavily routing | KEEP BUT UPDATE (Tavily version drift) |
| core/BUSINESS_SYMBOLS.md | no, orphaned | none | MERGE INTO business-panel command or agent, or RETIRE |
| core/BUSINESS_PANEL_EXAMPLES.md | no, orphaned | cross-command chains with nonexistent flags | RETIRE |
| CLAUDE.md (repo root) | YES for contributors in the repo | /sc: skill-invocation rule, stale command count, MCP guidance | KEEP BUT UPDATE |
| AGENTS.md | no | none | RETIRE or reduce to pointer |
| KNOWLEDGE.md | no | none | KEEP AS IS |
| PROJECT_INDEX.md / .json | on demand | stale catalog of commands, agents, skills, MCPs | KEEP BUT UPDATE (regenerate) |

### 4.2 Key findings

1. Only 2 of the 13 installed core files are ever in an agent's context: `CLAUDE.md` and `BASH_INSPECTION_POLICY.md`. The 8 routing-heavy files lost their `@` imports in commit `4b19eb08` (2026-03-16). Every routing decision tree in ORCHESTRATOR, COMMANDS, PERSONAS, MODES, FLAGS, and MCP has had no effect since then, yet `superclaude install` still copies them and the developer guides still tell contributors to "register" new commands in them.
2. There is currently NO accurate always-on "which command or skill when" guidance. `core/CLAUDE.md:97-102` only says "use `/sc:help`". The stale catalogs that do exist (COMMANDS.md, ORCHESTRATOR.md, PROJECT_INDEX.md) all reference removed `/sc:estimate`, `/sc:sc` dispatcher, Magic, Sequential, or Chrome DevTools, and none mention task-builder, task, prd, tdd, tech-research, roadmap, pr-submit, swarm-wizard, or the new meaning of implement and workflow.
3. The `/sc:task` tier classifier exists in three places with drift: `commands/task.md:71-93` (live, authoritative), `skills/sc-task-protocol/SKILL.md:56-63` (reference copy), `core/ORCHESTRATOR.md:161-236` (stale, extra keywords and a different tie-break). The SKILL.md also cites `config/tier-keywords.yaml` and two other YAML files that do not exist in the skill directory (`SKILL.md:404-406`).
4. The most important routing rule ("a message starting with /sc:<command> MUST invoke the matching skill first", repo-root `CLAUDE.md:9-14`) is only in the contributor file, so installed users never get it.
5. A second, drifted copy of 6 core files lives at `plugins/superclaude/core/` (RESEARCH_CONFIG differs by 492 lines, BUSINESS_PANEL_EXAMPLES by 136). The plugin build script copies only agents, commands, hooks, scripts, skills (`scripts/build_superclaude_plugin.py:75-76`), so that copy is shipped only inside the wheel as `_plugins` and is otherwise unused. Same for `src/superclaude/modes/` and `src/superclaude/mcp/MCP_*.md`: packaged, never installed.
6. `superclaude update` force-overwrites `~/.claude/CLAUDE.md` with the framework file (`main.py:309`, `install_core.py:51-56`), erasing any personal global instructions.
7. Install never deletes. Retiring a core file leaves the old copy in every existing user's `~/.claude/` unless an explicit cleanup step is added to `install_core.py`.

### 4.3 What breaks if the RETIRE verdicts are executed (consolidated)

| Location | Kind | Required change |
|---|---|---|
| `src/superclaude/cli/install_core.py:139-153` | code | remove retired names from the `known_core` set; add a removal step for stale installed copies |
| `src/superclaude/skills/sc-task-protocol/SKILL.md:407-408` | skill pointer | repoint "Routing logic" to `commands/task.md`, "Circuit breakers" to its own `:285-295` |
| `src/superclaude/cli/recommend/prompts.py:16` | docstring | repoint to `commands/task.md` |
| `core/RESEARCH_CONFIG.md:15,133` | cross-ref | drop "See RULES.md / MCP.md" or repoint |
| `tests/sc-roadmap/compliance/test_critical_corrections.py:7,61` | test docstrings only | optional wording update; assertions unaffected |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:99,368-371,749,1028-1029,1087,1181` and duplicate `docs/guides/...` | contributor docs | rewrite "Core files (always loaded)" and "register in COMMANDS.md / ORCHESTRATOR.md / FLAGS.md / PERSONAS.md" steps |
| `docs/developer-guide/technical-architecture.md:27,133,144-150,333`, `testing-debugging.md:32,72,90`, `docs/reference/diagnostic-reference.md:64`, `comprehensive-features.md:99-102`, `contributing-code.md:64`, `docs/mcp/mcp-integration-policy.md:459,473` | docs | remove or rewrite stale import and diagnostic snippets |
| `PROJECT_INDEX.md:41-48` | generated doc | regenerate |
| No test reads ORCHESTRATOR, COMMANDS, PERSONAS, MODES, FLAGS, MCP, or the BUSINESS files. | | none |

Files that must NOT be renamed without code changes: `BASH_INSPECTION_POLICY.md` (5 code sites, 5 test files), `RESEARCH_CONFIG.md` (2 test files), `core/CLAUDE.md` (test asserts its `@` import).

### 4.4 Gaps and UNVERIFIED items

- Whether any agent actually follows the prose "See X.md" pointers to unloaded core files at runtime: UNVERIFIED (no loader code; depends on model behavior).
- Claude Code not auto-loading AGENTS.md: platform behavior, not verified against the exact installed Claude Code version.
- Whether an `integration` branch is still part of the workflow (repo-root `CLAUDE.md:245-252`): UNVERIFIED.
- PM Agent "auto-activation" claims in `RULES.md:30-49`: no implementing hook found; UNVERIFIED as behavior.
- Circuit breaker thresholds in `MCP.md:188-195` and FLAGS auto-activation triggers: no implementing code found; UNVERIFIED as behavior.
- `src/superclaude/rules/{core,contextual,prompts}` (installed to `~/.claude/rules/`) were not audited for routing content; they are outside this file set and should be checked by the owner of that surface.
- `VERSION` file says `3.7` while `pyproject.toml:7` says `4.3.5`; which is canonical was not determined.

