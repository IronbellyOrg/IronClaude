# Research: IronClaude human-facing routing docs (consolidation inventory)

**Scope:** /tmp/ic-master (snapshot of IronClaude origin/master ee1c1787, 2026-10-11): README.md, docs/getting-started/*, docs/user-guide/*, docs/reference/*, docs/guides/*, docs/developer-guide/* (routing sections only), docs/swarm/wizard-guide.md, plus other docs/ files whose main job is "what to use when".
**Anchor:** /Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md (242 lines; called "the new guide" below)
**Status:** Complete
**Date:** 2026-10-12

---

## Method

- Command inventory taken from `ls /tmp/ic-master/src/superclaude/commands` and `src/superclaude/skills` (snapshot).
- Stale-term and new-skill mention counts produced by a scripted line scan of each doc (line numbers cited are from that scan, re-checkable with grep).
- Inbound references: whole-snapshot grep for each filename (basename and relative path), excluding the file itself.
- All paths below are relative to /tmp/ic-master unless absolute.
- The snapshot contains IronClaude's own `.dev/` tree. Inbound references from `.dev/` (old release archives, review JSON, reflect stdout) are counted separately as "historical artifacts" and do not block a retire.

## Accuracy baseline (what "current" means) [CODE-VERIFIED]

| Fact | Evidence |
|---|---|
| 44 slash command files ship in `src/superclaude/commands/` (adversarial, agent, analyze, auggie-review, brainstorm, build, business-panel, cleanup-audit, cleanup, cli-eval, cli-portify, design, document, explain, git, help, implement, improve, index-repo, index, init-lite, load, pm, post-release, pr-submit, recommend, reflect, release-split, research, review-translation, roadmap, save, spawn, spec-panel, swarm-wizard, task, tasklist, tdd, test, troubleshoot, validate-roadmap, validate-tests, workflow, plus README.md) | `ls src/superclaude/commands` |
| No `estimate.md`, `select-tool.md`, or bare `sc.md` command exists | same listing |
| Unprefixed skills `task`, `task-builder`, `prd`, `tdd`, `tech-research`, `tech-reference`, `roadmap`, `readme`, `operational-guide` ship in `src/superclaude/skills/`; `pr-submit`, `swarm-wizard`, `reflect`, `recommend` ship as `/sc:` commands backed by `sc-*-protocol` / `sc-recommend` skills | `ls src/superclaude/skills` |
| Installable MCP servers are context7, playwright, serena, morphllm-fast-apply, tavily, auggie, plus the AIRIS gateway. No `sequential-thinking`, `magic`, or `chrome-devtools` entry | `src/superclaude/cli/install_mcp.py:18-95`; `src/superclaude/mcp/configs/` holds airis-agent, auggie, context7, mindbase, morphllm, playwright, serena, serena-docker only |
| `/sc:workflow` now writes a phased plan package to `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/<id>.md`, bans `--parallel`, `--validate`, `--depth shallow/normal`, `--output`, runs an advisory `/sc:reflect --mode pre`, and hands off to `/sc:implement` (not `/task`); `/sc:implement` treats that package as "managed" (sibling `progress.md`, archive to `.dev/tasks/done/<id>/`) | `src/superclaude/commands/workflow.md:12,42,46,60-79`; `implement.md:63-65` |
| `/sc:implement` is now a "middleweight spec executor": walks a spec/PRD/tasklist/prompt, per-task spec-compliance QA, ledger at `.dev/implement/<slug>/progress.md`, `--resume`; old persona/framework flags are banned (`E-LEGACY`) | `src/superclaude/commands/implement.md:2-3,30-35,58-68` |
| NOTE: the new guide (lines 15, 110, 207) still says `/sc:workflow` writes `.dev/workflow/<name>/plan.md`; current code says `.dev/tasks/to-do/TASK-WF-.../<id>.md`. The new guide itself needs that path corrected before it becomes the anchor. [CODE-CONTRADICTED] | workflow.md:12 vs guide:15 |

---

## 1. README.md (root, 272 lines)

1. **Purpose and audience.** Project front page for new users and contributors: identity (IronClaude vs `superclaude` package, lines 1-31), install (53-75), CLI quick start (77-106), concepts (108-148), repo structure, dev workflow, doc map, MCP list. Mixed audience, leans contributor.
2. **Routing content.** Thin. No "which slash command when" guidance at all. It routes only at the CLI-pipeline level: `superclaude sprint/roadmap/tasklist/reflect run` (88-96) and a doc map (195-205). Overlap with the new guide: none on slash-command routing. Overlap with `docs/getting-started/installation.md` (install) and `docs/developer-guide/contributing-code.md` (dev workflow, make targets).
3. **Accuracy.**
   - Lists "Sequential" (38, 217) and "Magic" (219) and "Chrome DevTools" (220) as integrations; none are in the installer registry. [CODE-CONTRADICTED]
   - Doc map points at `PLANNING.md` (200) and `TASK.md` (201), which do not exist at repo root. [CODE-CONTRADICTED]
   - Never mentions any slash command or skill: no task-builder, task, prd, tdd, tech-research, tech-reference, roadmap, pr-submit, swarm-wizard. Only reflect via the CLI guide link (98).
   - License says MIT (272); not checked against LICENSE file content. UNVERIFIED.
4. **Unique content to keep.** Naming reality (17-31), install commands, `make` target table (172-185), source-of-truth vs `.claude/` mirror rule (144-148), Linux-only `eval` platform note (246-268). None of this belongs in the routing guide; it stays in README.
5. **Inbound references.** CODE/INSTALL (packaging-bound): `pyproject.toml:9` (`readme = "README.md"`, PyPI long description), `pyproject.toml:95`, `MANIFEST.in:2`, `package.json:13` (files list), `Makefile:100,103` (translation targets). `Makefile:128-401` only skip component READMEs in loops, not this file. DATA: `PROJECT_INDEX.json:122`.
6. **Verdict: KEEP BUT UPDATE.** Cannot be retired (packaging-bound). Add a short "Which command do I use?" section that links to the new user guide as the single routing entry point; drop Sequential, Magic, Chrome DevTools from the MCP list; fix the dead PLANNING.md / TASK.md links.

---

## 2. docs/getting-started/quick-start.md (505 lines)

1. **Purpose and audience.** Marketing-style first-session tour for new users of "SuperClaude v4.1.5" (lines 3, 9, 502). Badges, HTML tables, emoji headings.
2. **Routing content.** (a) "Instant Start" sample commands (96-106); (b) "First Project Session" 7-step lifecycle brainstorm, load, analyze, workflow, implement, test, save (212-255); (c) "Domain-Specific Workflows" table mapping domain to `@agent-*` and MCP (257-269); (d) "When to Use: SuperClaude vs Standard Claude Code" (273-326); (e) a 4-week learning path (330-387). Overlap: the lifecycle table duplicates the new guide sections 1 and 3.1/3.3 in an older, incompatible form; also overlaps `docs/user-guide/commands.md` "workflow" sections, `docs/reference/basic-examples.md`, and `docs/reference/examples-cookbook.md`. The "when to use" table overlaps new-guide section 1 level 1 vs higher levels.
3. **Accuracy.**
   - Counts "21 commands, 14 agents, 6 modes, 6 MCP" (31-35, 141-142). Actual: 44 command files, 46 agent files in `src/superclaude/agents/`, 7 `MODE_*.md` files in `src/superclaude/modes/`. [CODE-CONTRADICTED]
   - Version badge 4.1.5 (9, 502); `pyproject.toml:7` says 4.3.5. [CODE-CONTRADICTED]
   - Magic MCP (191, 263). Removed. [CODE-CONTRADICTED]
   - Agent handles `@agent-architect`, `@agent-security`, `@agent-frontend`, `@agent-backend`, `@agent-qa`, `@agent-devops` (105, 160-163, 263-267). Real agent files are `security-engineer`, `frontend-architect`, `backend-architect`, `quality-engineer`, `devops-architect`, `system-architect`. [CODE-CONTRADICTED]
   - Step 4/5 say `/sc:workflow "payment integration"` produces an "implementation roadmap" and `/sc:implement "Stripe checkout"` "builds with best practices" (237-243). Current `/sc:workflow` writes a plan package and `/sc:implement` is a spec executor with per-task QA (see baseline). Loosely compatible but describes old behavior.
   - No mention of task-builder, task, prd, tdd, tech-research, tech-reference, roadmap skill, pr-submit, swarm-wizard, reflect.
   - `pipx install SuperClaude && SuperClaude install` (83-91). README uses lowercase `superclaude`; package name is `superclaude` (`pyproject.toml:6`). Mixed case may still work on case-insensitive filesystems only. UNVERIFIED.
4. **Unique content to absorb.** Only the "SuperClaude vs plain Claude Code" framing (273-326) is not in the new guide; the new guide's level 1 ("Ask a question") covers the same intent. Nothing else is unique. The install snippet is already in installation.md and README.
5. **Inbound references (live, non-.dev).** DOC only: `docs/user-guide/agents.md:1024`, `docs/user-guide/modes.md:701,715`, `docs/user-guide/mcp-servers.md:341`, `docs/getting-started/installation.md:504,548`, `docs/reference/README.md:44,262`. No code/test/install references. 2 historical `.dev/` references.
6. **Verdict: RETIRE (replace with the new user guide).** Its routing content is outdated and fully superseded by the new guide sections 1, 3, and 5. Repoint the 8 doc links above to the new guide. If the project wants a "getting started" page to stay at this path, replace its body with a short pointer: install (link installation.md), then "read the user guide".

---

## 3. docs/getting-started/installation.md (553 lines)

1. **Purpose and audience.** Install, verify, update, uninstall, troubleshoot. New users.
2. **Routing content.** Minimal: "Test in Claude Code" (308-315) and a "Learning Journey" table of next docs (487-519). No decision content. Overlap: README install section (53-75), `docs/user-guide/mcp-installation.md`.
3. **Accuracy.**
   - Title "21 Commands, 14 Agents & 6 MCP Servers" (5) and closing counts (536). [CODE-CONTRADICTED] (see quick-start).
   - `python3 -m SuperClaude --version` expecting 4.1.5 (299-301); version is 4.3.5 (`pyproject.toml:7`). [CODE-CONTRADICTED]
   - `SuperClaude install --list-components` (304): the `install` command exposes `--list`, not `--list-components` (`src/superclaude/cli/main.py:29-56`). [CODE-CONTRADICTED]
   - `@agent-security` (314): no such agent file; it is `security-engineer`. [CODE-CONTRADICTED]
   - "Global policy activation" (40-60) and `superclaude update` (`src/superclaude/cli/main.py:284`) are current. [CODE-VERIFIED]
4. **Unique content to absorb.** All install/update/backup/troubleshooting content is unique and must stay; none of it belongs in the routing guide. The "next steps" table (487-519) is the only routing piece and should become one link to the new guide.
5. **Inbound references (live).** DOC only: `docs/user-guide/modes.md:703`, `docs/user-guide/mcp-servers.md:25`, `docs/getting-started/quick-start.md:448`, `docs/reference/troubleshooting.md:170`, `docs/reference/examples-cookbook.md:116`. No code/test/install references.
6. **Verdict: KEEP BUT UPDATE.** Fix counts, version, `--list-components`, agent name; replace the "Learning Journey" table with "Next: read the user guide" plus links to commands reference and installation-only follow-ups.

---

## 4. docs/user-guide/commands.md (1700 lines) - the largest routing doc

1. **Purpose and audience.** "SC Commands Reference" for both Claude Code ("skip these if you're human", 35-41) and humans (43-53). Last updated 2026-01-18 (line 9). Claims "all 30 commands" (47).
2. **Routing content (heavy, this is the main competitor to the new guide).**
   - Command categories table, 8 groups (149-212).
   - Document-only vs execution command lists (216-249).
   - Per-command "When to use / What it does / Syntax / Examples" for ~24 commands (253-1029).
   - "When to Use Which Panel" spec-panel vs business-panel (934-944).
   - "Visual Map: When to Use What" decision tree (1033-1082).
   - "Key Differences" table (1086-1095); spawn vs task vs implement (1099-1218); task vs implement (1222-1290); design vs workflow (1294-1392); index-repo vs Serena (1396-1501).
   - "Typical Workflows": new project, new feature, bug fix, refactoring, code review, business idea, improving a PRD, architecture validation, pitch prep, enterprise feature (1505-1644).
   Overlap: the decision tree, key differences, and typical workflows overlap the new guide sections 1, 3.1-3.8, and 5 almost one-for-one, but with different (older) answers. Also overlaps `docs/reference/basic-examples.md`, `advanced-workflows.md`, `examples-cookbook.md`, `commands-list.md`, `docs/getting-started/quick-start.md` (lifecycle), `docs/user-guide/modes.md`, `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md`.
3. **Accuracy.**
   - `/sc:implement` section (473-503) documents `--type`, `--framework`, `--safe`, `--with-tests`, personas, and Magic. All four flags are now banned and STOP with `E-LEGACY` (`src/superclaude/skills/sc-implement-protocol/SKILL.md:32,45,49`). Same banned flags in examples at 1165 and 1261. [CODE-CONTRADICTED]
   - `/sc:workflow` section (362-391) is mostly current (matches `workflow.md:12,42`), but line 390 still says "workflow = planning (`plan.md`)" and the design-vs-workflow example (1333-1353) shows week-based phases. Partly stale.
   - Visual map (1044-1057) routes "PRD ready" to `/sc:workflow` then `/sc:implement`; the new guide routes PRD/TDD work to `/roadmap` + `/task` (guide 3.1) and only small changes to `/sc:workflow` (guide level 3). Conflicting routing.
   - `/sc:task` (329-358): lists Magic among MCPs (358); `task.md:6` lists context7, serena, playwright, morphllm. [CODE-CONTRADICTED]. Does not mention the compliance tiers that `task.md:19,44` now centre on.
   - `/sc:troubleshoot` (566-591) uses `--trace` which is not in `troubleshoot.md:8` argument-hint; misses `--depth`, tiers, report path. [CODE-CONTRADICTED]
   - `/sc:brainstorm` handoff names `/sc:task-builder` (405); no such command, the skill is `/task-builder`. [CODE-CONTRADICTED]
   - `/sc:research` output to `claudedocs/research_*.md` (454) matches `research.md:104`. [CODE-VERIFIED]
   - `/sc:pm` "always active automatically" (259) UNVERIFIED (no hook found wiring it; not checked exhaustively).
   - Missing entirely: `/task-builder`, `/task`, `/prd`, `/tdd` (skill), `/tech-research` (only named at 402), `/tech-reference`, `/roadmap` (skill), `/readme`, `/operational-guide`, `/sc:pr-submit`, `/sc:swarm-wizard`, `/sc:adversarial`, `/sc:auggie-review`, `/sc:cleanup-audit`, `/sc:release-split`, `/sc:roadmap`, `/sc:tasklist`, `/sc:recommend` (only in the file map, 97), `/sc:init-lite`, `/sc:cli-eval`, `/sc:cli-portify`, `/sc:post-release`, `/sc:review-translation`, `/sc:validate-*`.
   - "Notes for future sessions" (1662-1696) refers to itself as `SC_COMMANDS_REFERENCE.md` (1669), and to `TASK.md` and `PLANNING.md` (136-138, 1674-1675) which do not exist. [CODE-CONTRADICTED]
   - MCP table (1652-1658) omits auggie; morphllm name is `morphllm-fast-apply` in the installer.
4. **Unique content to absorb.**
   - "When to Use Which Panel" spec-panel vs business-panel table (934-944): the new guide 3.6 has one row each; the PRD = "Both" nuance (944) is worth one sentence in the guide.
   - `/sc:reflect` legacy grammar and the `superclaude reflect run` CLI wrapper section (986-1029): exit-code meanings (pass 0, halted 10, degraded 11, blocked 2) and `--promote` default on. This is reference material; it already lives in `docs/guides/reflect-cli-tools-guide.md` (the canonical, test-pinned doc). No need to keep a copy.
   - index-repo vs Serena comparison (1396-1501): not in the new guide; it is a tool-setup topic, not workflow routing. Candidate to move into `docs/user-guide/mcp-servers.md` or `session-management.md`, or drop.
   - Document-only vs execution command list (216-249): useful "does it change files?" signal. The new guide covers this per row ("It only reports"). Could become one column in a slimmed per-command reference.
   - Per-command syntax blocks for commands the new guide does not cover (git, build, index, load, save, spawn, agent): keep as reference only after correcting.
5. **Inbound references (live).** DATA: `PROJECT_INDEX.json:128`. DOC: `docs/user-guide/mcp-installation.md:239`, `agents.md:1017`, `modes.md:5,702,727`, `mcp-servers.md:340`, `flags.md:307`, `brainstorm.md:230`, `docs/getting-started/quick-start.md:449,481`, `installation.md:505`, `docs/reference/troubleshooting.md:171`, `examples-cookbook.md:179`. No code or test references. 58 historical `.dev/` references.
6. **Verdict: KEEP BUT UPDATE, as a per-command reference only.** Strip all routing sections (Visual Map 1033-1082, Key Differences 1086-1095, spawn/task/implement 1099-1290, design vs workflow 1294-1392, Typical Workflows 1505-1644) and replace them with one link to the new guide. Rewrite the `/sc:implement`, `/sc:task`, `/sc:troubleshoot` entries from the current command files; add rows for every command and skill listed as missing above; remove the "For Claude Code" file-map and session-notes sections (they are agent-facing and stale). Removal list for the user to adjudicate is in the Summary.

---

## 5. docs/user-guide/agents.md (1048 lines)

1. **Purpose and audience.** Human guide to "16 domain specialist agents" (line 3), manual `@agent-` invocation, keyword auto-activation, per-agent profiles (146-653), troubleshooting, quick reference.
2. **Routing content.** Agent selection rules and decision tree (74-102); "Agent Trigger Lookup" keyword-to-agent table (812-829); "Command-Agent Mapping" (831-843); "Effective Agent Combinations" (845-862). This is routing of *agents*, not of commands/skills; the new guide does not route agents at all. Overlap: `docs/user-guide/modes.md` (auto-activation story), `docs/reference/README.md`, `docs/reference/advanced-patterns.md` (multi-agent combos).
3. **Accuracy.**
   - "16 agents" (3) vs "14 specialized AI experts" (1046); profiles cover 15 persona agents. `src/superclaude/agents/` holds 46 agent files including rf-*, audit-*, eval-*, reflect-reviewer, evidence-validator, etc., none documented here. [CODE-CONTRADICTED]
   - Short handles `@agent-security`, `@agent-frontend`, `@agent-architect` (47-49, 140) do not match agent file names (`security-engineer`, etc.). [CODE-CONTRADICTED]
   - `/sc:audit` (129): no such command. [CODE-CONTRADICTED]
   - "Frontend architect + Magic MCP should activate" (20) and Magic in MCP list (70, 680). [CODE-CONTRADICTED]
   - Examples rely on `/sc:implement "JWT authentication"` auto-activating personas (15-19, 120). Current `/sc:implement` is a spec executor with per-task QA; persona auto-activation is not part of its documented behavior (`implement.md:2-3`). UNVERIFIED whether any persona routing still happens.
   - Agents dir path `superclaude/Agents/` (38) is wrong case; actual `src/superclaude/agents/`. [CODE-CONTRADICTED]
4. **Unique content to absorb.** Per-agent profiles (146-653) and the keyword trigger table (812-829) are unique reference content. They do not belong in the routing guide. The new guide could add one line: "To get a specialist view, address an agent directly, for example `@agent-security-engineer`" (UNVERIFIED that the `@agent-<file-name>` handle form is what Claude Code resolves; confirm before writing).
5. **Inbound references (live).** DATA `PROJECT_INDEX.json:129`; DOC `docs/user-guide/modes.md:707`, `mcp-servers.md:346`, `docs/getting-started/quick-start.md:460`, `installation.md:514`, `docs/reference/examples-cookbook.md:180`. No code/test refs.
6. **Verdict: KEEP BUT UPDATE (as agent reference, not routing).** Remove the "Testing Agent Activation" block and the auto-activation-via-`/sc:implement` claims; fix handles, counts, Magic, `/sc:audit`; add a short section listing the workflow agents (rf-*, audit-*, reflect-reviewer, evidence-validator) as "used internally by skills, not invoked directly". Point command routing to the new guide.

---

## 6. docs/user-guide/modes.md (727 lines)

1. **Purpose and audience.** Explains behavioral modes (brainstorming, introspection, deep research, task management, orchestration, token efficiency) and their flags. Humans.
2. **Routing content.** Mode quick-reference with auto-triggers (7-16); "Real-World Examples" workflow walk-throughs (419-470); "Mode Activation Patterns" (473-500). Overlap with `docs/user-guide/flags.md` (same mode flags), `agents.md` (auto-activation), `commands.md`.
3. **Accuracy.**
   - Lists 6 modes; `src/superclaude/modes/` has 7 (`MODE_Business_Panel.md` missing from the table). [CODE-CONTRADICTED]
   - Magic in orchestration and workflow examples (265, 438). [CODE-CONTRADICTED]
   - Uses `/sc:implement "core productivity features"` as a planning step (431-434), which contradicts current `/sc:implement` (spec executor). [CODE-CONTRADICTED]
   - `/sc:reflect --type mode-status` (603) and `SuperClaude install --diagnose` (613): neither exists (`reflect.md:10` legacy grammar only accepts `--type task --analyze|--validate`; `install` options are `--target/--force/--list`). [CODE-CONTRADICTED]
   - Sequential reference (261). [CODE-CONTRADICTED]
4. **Unique content to absorb.** Mode descriptions and manual override flags (`--brainstorm`, `--introspect`, `--task-manage`, `--orchestrate`, `--uc`) are unique reference material backed by `src/superclaude/modes/*.md` and `src/superclaude/core/FLAGS.md`. Not routing. Nothing for the new guide except possibly a footnote that `--uc` shortens output.
5. **Inbound references (live).** DATA `PROJECT_INDEX.json:131`; DOC `agents.md:1023`, `mcp-servers.md:345`, `brainstorm.md:231`, `quick-start.md:459`, `installation.md:513`. No code/test refs.
6. **Verdict: KEEP BUT UPDATE.** Delete the "Real-World Examples" workflow section (it is routing and wrong); fix mode count, Magic, Sequential, and the two nonexistent diagnostics commands.

---

## 7. docs/user-guide/flags.md (309 lines)

1. **Purpose and audience.** Flag reference: global auto-activation flags, MCP flags, mode flags, per-command flag tables. Humans.
2. **Routing content.** "Common Usage Patterns" (214-250) gives per-domain command sequences. Small. Overlap with `modes.md`, `commands.md`, `docs/reference/basic-examples.md`.
3. **Accuracy.**
   - MCP flag table (17-24) lists only current servers (context7, playwright, tavily, morphllm, serena) and omits auggie. Mostly current.
   - `/sc:task` flags (95-101) omit `--compliance`, `--verify`, `--force-strict` (`task.md:19,44`). Partly stale.
   - `/sc:workflow` flags (103-111) current. [CODE-VERIFIED] against `workflow.md:30-40`.
   - `/sc:troubleshoot --trace` (117) not in `troubleshoot.md:8`; table omits `--depth`, `--scope`, `--no-escalate`. [CODE-CONTRADICTED]
   - `/sc:reflect` table (129-150) is detailed and current against `reflect.md:10,87`. [CODE-VERIFIED]
   - Usage patterns use `/sc:implement "responsive dashboard" --c7` (219) and `--validate`, `--safe-mode`, `--all-mcp` globally; whether `/sc:implement` accepts `--c7` is UNVERIFIED (not in its known-options list, `sc-implement-protocol/SKILL.md:49`).
4. **Unique content to absorb.** Per-command flag tables are reference content. The `/sc:reflect` table is the best human-readable reflect flag list in the docs set; keep it here (or in the reflect guide), not in the routing guide.
5. **Inbound references (live).** DATA `PROJECT_INDEX.json:130`; DOC `modes.md:516,641,708`. No code/test refs.
6. **Verdict: KEEP BUT UPDATE.** Drop "Common Usage Patterns" (routing duplicate); refresh `/sc:task` and `/sc:troubleshoot` tables; add auggie and rows for `/sc:implement`, `/sc:pr-submit`, `/sc:auggie-review` defaults that the new guide calls out as surprising (guide 5, lines 237-242).

---

## 8. docs/user-guide/mcp-servers.md (352 lines) and docs/user-guide/mcp-installation.md (239 lines)

1. **Purpose and audience.** MCP server descriptions, auto-activation logic, manual flags (mcp-servers); installation commands and API keys (mcp-installation). Humans.
2. **Routing content.** Only "which MCP server activates for which request" (mcp-servers 27-36). Not command routing. No overlap with the new guide.
3. **Accuracy.** Server lists match the installer (`src/superclaude/cli/install_mcp.py:35-95`): context7, playwright, serena, morphllm-fast-apply, tavily, auggie. [CODE-VERIFIED] No Sequential or Magic in either file (scan found none). `/sc:implement ... --no-mcp` and `--all-mcp` examples (mcp-servers 233-243) are UNVERIFIED against the current `/sc:implement` option list.
4. **Unique content.** All unique, all non-routing. The index-repo vs Serena material from commands.md 1396-1501 could move into mcp-servers.md if the user wants to keep it.
5. **Inbound references (live).** mcp-servers: DATA `PROJECT_INDEX.json:133`; DOC `mcp-installation.md:237`, `agents.md:1018`, `modes.md:713,726`, `flags.md:308`, `quick-start.md:470`, `installation.md:522`, `examples-cookbook.md:181`, `mcp-server-guide.md:602`. mcp-installation: no live inbound references (25 historical `.dev/` only).
6. **Verdict: KEEP AS IS** (both), apart from re-checking the `/sc:implement` flag examples in mcp-servers.md. Out of scope for routing consolidation. Note the near-duplicate `docs/reference/mcp-server-guide.md` (section 19).

---

## 9. docs/user-guide/brainstorm.md (233 lines)

1. **Purpose and audience.** Full guide to `/sc:brainstorm` v2: flags, waves, artifacts, handoff targets. Humans.
2. **Routing content.** "Pipeline Position" (209-226) and "Handoff Targets" (165-173) say where brainstorm sits: topic, then brainstorm, then design / tasklist / task-builder. Overlap with new guide 3.1 step 1 and 3.6 row 1 (both say brainstorm ends at `merged-requirements.md` and feeds `/prd`).
3. **Accuracy.** Current against `src/superclaude/commands/brainstorm.md:39,60,71`. [CODE-VERIFIED] One naming error repeated from the command file: handoff target written as `/sc:task-builder` (14, 54-ish table, 186, 225); the actual skill is `task-builder` (`/task-builder`), and the command file itself has the same slip (`brainstorm.md:134`). Note the new guide routes brainstorm output to `/prd`, while this doc offers `--handoff task` straight to task-builder; the two are compatible but the guide does not mention `--handoff`.
4. **Unique content.** Flag table, wave description, artifacts list. All per-command reference. The new guide could add "add `--handoff task` to go straight to a task file" only if the user wants that path promoted.
5. **Inbound references (live).** DOC `commands.md:77,164,441`, `modes.md:82,86`, `docs/reference/basic-examples.md:40`. No code/test refs.
6. **Verdict: KEEP BUT UPDATE** (rename `/sc:task-builder` to `/task-builder` here and in `src/superclaude/commands/brainstorm.md:134`). It is a per-command deep dive the new guide should link to from 3.1 step 1.

---

## 10. docs/user-guide/session-management.md (377 lines)

1. **Purpose and audience.** Serena-backed persistence: `/sc:load`, `/sc:save`, `/sc:reflect` as memory tools, per-turn session context envelope (v4.3), cross-conversation continuity.
2. **Routing content.** "Session Lifecycle Patterns" (110-157) are workflow sequences (brainstorm, save, workflow, save; load, reflect, implement, save). Overlap with new guide 3.12 (resume after crash), which uses different mechanics (re-run `/task`, `--resume`, sc-crash-recovery).
3. **Accuracy.**
   - Presents `/sc:reflect` as "Progress Assessment with Memory Context" with `--scope project|session` (59-82), `--cleanup` (318), `--repair` (326). Current `/sc:reflect` is a pre/post spec-adherence audit; `--scope` takes a path; `--cleanup` and `--repair` do not exist (`reflect.md:10,87`). [CODE-CONTRADICTED]
   - `/sc:workflow` used for "implementation planning" (122, 156): compatible but old framing.
   - "Per-Turn Session Context Envelope (v4.3+)" (159-188) ties to freshness hooks, current (cross-ref `freshness-hooks.md`). UNVERIFIED in detail.
4. **Unique content to absorb.** The `/sc:load` / `/sc:save` usage is unique and not in the new guide. Worth one row in new-guide 3.12 only if the team actually uses Serena session memory (UNVERIFIED team practice).
5. **Inbound references (live).** DATA `PROJECT_INDEX.json:132`; DOC `agents.md:1019`, `modes.md:714,725`, `mcp-servers.md:347`, `flags.md:309`, `quick-start.md:461`, `docs/reference/README.md:168`, `comprehensive-features.md:124`.
6. **Verdict: KEEP BUT UPDATE.** Remove every `/sc:reflect` usage (it is the wrong tool for this); remove the lifecycle workflow sequences or replace them with a link to new-guide 3.12.

---

## 11. docs/user-guide/memory-system.md (292), eval-pipeline.md (403), freshness-hooks.md (166)

1. **Purpose.** ReflexionMemory for the PM agent; `superclaude eval` operator guide (last verified 2026-05-22, line 5); freshness hooks installed by `superclaude install`.
2. **Routing content.** None of substance (eval-pipeline has "Common workflows" 286-333 for the eval CLI only).
3. **Accuracy.** Not in routing scope; the scan found no stale command or MCP names in any of the three.
4. **Unique content.** All unique, none routing.
5. **Inbound references (live).** memory-system: `docs/memory/README.md:38,276`. eval-pipeline: `CHANGELOG.md:121`, `docs/developer-guide/documentation-index.md:66-80`, `docs/eval/retry.md:81`. freshness-hooks: `CHANGELOG.md:177`, `README.md:40`, `session-management.md:188`, `installation.md:523`, `technical-architecture.md:72`, `docs/reference/troubleshooting.md:109`.
6. **Verdict: KEEP AS IS** (out of routing scope).

---

## 12. docs/reference/README.md (266 lines)

1. **Purpose and audience.** "Navigation Hub" for the reference folder with learning paths by experience level (37-95), a command/flag quick reference (97-127), framework quick starts (129-161), problem-solving pointers (163-183). Claims "Status: Current - All content verified" (5) and "All examples tested" (189).
2. **Routing content.** Learning paths that route a user from quick-start to basic-examples to advanced-patterns etc.; "Command Quick Reference" (101-108) which routes almost everything through `/sc:load`, `/sc:save`, and global flags. Overlap with `examples-cookbook.md` (same hub role), `quick-start.md` learning path, `commands.md`.
3. **Accuracy.** "Magic for UI" (219). [CODE-CONTRADICTED] Index omits 7 of the 16 files actually in `docs/reference/` (commands-list, suggested-commands, comprehensive-features, claude-code-history-management, deviation-report-format, nfr-conv-2-prose-determinism, pm-agent-autonomous-reflection). The "verified" claims are unsupported (UNVERIFIED; no test pins this folder). Mentions none of the new skills.
4. **Unique content.** None that the new guide needs. The flag quick reference duplicates `docs/user-guide/flags.md`.
5. **Inbound references (live).** DOC only: `docs/reference/pm-agent-autonomous-reflection.md:424,434`. (Several other files link "README" generically; those were not counted.)
6. **Verdict: KEEP BUT UPDATE (shrink to a plain index)** if the reference folder survives: list only the files that are kept after this consolidation, drop learning paths and "verified" claims, link the new guide for "what to use when". If the examples collections below are retired, this becomes a 20-line index.

---

## 13. docs/reference/examples-cookbook.md (199 lines)

1. **Purpose and audience.** Hub that points to three example collections (basic-examples, advanced-workflows, integration-patterns) by experience level and use case. All users.
2. **Routing content.** It is pure routing-to-docs: "By Experience Level" (44-65), "By Use Case" (67-88), "Quick Reference Matrix" (142-150), learning roadmap (112-140). Overlap: `docs/reference/README.md` (same hub job), `quick-start.md` and `installation.md` learning tables.
3. **Accuracy.**
   - 26 of its 38 section anchors into the three collections do not match any heading in the target files (scripted slug check), so most links are dead. [CODE-CONTRADICTED]
   - `../CONTRIBUTING.md` (188) resolves to `docs/CONTRIBUTING.md`, which does not exist (the file is at repo root). [CODE-CONTRADICTED]
   - Community links point to `SuperClaude-Org/SuperClaude_Framework` (186-187), not IronbellyOrg/IronClaude.
   - "Verified Commands Reference" (90-110) describes `/sc:reflect` as "Context analysis and optimization" (101), which is wrong for the current pre/post audit. [CODE-CONTRADICTED]
   - No mention of any of the new skills.
4. **Unique content.** None. The new guide is the replacement "cookbook".
5. **Inbound references (live).** DOC only: `docs/user-guide/agents.md:1025`, `modes.md:709,724`, `mcp-servers.md:351`, `docs/getting-started/quick-start.md:450,484`, `installation.md:515`, `docs/reference/README.md:25`. No code/test refs.
6. **Verdict: RETIRE.** Repoint its 8 inbound links to the new user guide (the guide is effectively the cookbook: section 3 is a set of worked recipes).

---

## 14. docs/reference/basic-examples.md (613 lines)

1. **Purpose and audience.** "Copy-paste ready" beginner examples: one-liners per command, manual agent calls, usage patterns, getting-started examples, common tasks, troubleshooting, flags, learning progression.
2. **Routing content.** "Basic Usage Patterns" Discovery to Implementation, Development to Quality, Problem to Solution (215-262); "Getting Started Examples" (265-329); "Common Development Tasks" (331-389); learning progression (545-587). Overlap: new guide 3.2, 3.3, 3.4, 3.5; `commands.md` Typical Workflows; `advanced-workflows.md`; `integration-patterns.md`; `quick-start.md`.
3. **Accuracy.**
   - 39 `/sc:implement` lines (scan: 55, 58, 62, 187, 229, 237, 245, 261, 306, 313, 326, 327, ...), all used as "describe a feature, get complete code". Under the new guide this routing is wrong for anything beyond one file: multi-file features must go through `/sc:workflow` + `/sc:implement` (plan first) or `/task-builder` + `/task` (guide line 20). Current `/sc:implement` accepts an inline prompt, so the commands run, but the routing contradicts the guide's hard limit.
   - `/sc:brainstorm` entry (28-40) is current. [CODE-VERIFIED] against `brainstorm.md:39`.
   - Sequential reference (199). [CODE-CONTRADICTED]
   - Bug flow "troubleshoot, analyze, implement" (249-262) lacks the guide's "write a failing test first" step (guide 3.4 step 3).
   - No mention of task-builder, task, prd, tdd, tech-research, tech-reference, roadmap, pr-submit, swarm-wizard, reflect.
4. **Unique content to absorb.** Very little. Possibly the `/sc:analyze --focus security` one-liner (already in guide 3.5) and the troubleshooting one-liners for environment issues (426-440), which are generic and could be dropped.
5. **Inbound references (live).** DOC only: `examples-cookbook.md` (15 links), `docs/reference/README.md:24,46,169,264`. No code/test refs.
6. **Verdict: RETIRE.** Superseded by new-guide section 3; keeping it would preserve conflicting routing.

---

## 15. docs/reference/advanced-workflows.md (310 lines)

1. **Purpose and audience.** "Complex command sequences" for experienced users: full-stack sequence, problem-solving, project phases, migration, enterprise analysis, QA workflows, session patterns.
2. **Routing content.** Entire file is workflow sequences (20-267). Overlap: new guide 3.1, 3.2, 3.4, 3.7; `commands.md` Typical Workflows; `advanced-patterns.md` (near-duplicate topics: large codebase analysis, migration, review); `integration-patterns.md`.
3. **Accuracy.** 16 `/sc:implement` uses as free-form builders (33, 38, 62, 92, ...); `/sc:workflow` used for "improvement recommendations" (148); Sequential (150, 198) [CODE-CONTRADICTED]; `/sc:load legacy-system/` with a path (110) contradicts `/sc:load`'s project-name usage (UNVERIFIED). Routes enterprise and migration work through `@agent` prompts plus `/sc:implement`, where the new guide requires PRD/TDD/roadmap/task files (guide 3.1) or task-builder (3.7 step 3). Has an honest "What these workflows ARE NOT" section (269-283) stating no real coordination happens.
4. **Unique content to absorb.** The "Important Clarifications: what these ARE / ARE NOT" framing (269-283) is a good honesty note but obsolete now that real orchestration exists (task files, reviewer panels). Nothing to carry over.
5. **Inbound references (live).** DOC only: `examples-cookbook.md` (14 links), `docs/reference/README.md:30,61,72,173,179,248`.
6. **Verdict: RETIRE.**

---

## 16. docs/reference/advanced-patterns.md (329 lines)

1. **Purpose and audience.** "Advanced context usage patterns": multi-agent context, command sequencing, flag combinations, complex project, migration, review/audit patterns.
2. **Routing content.** Whole file (21-325). Overlap: near-duplicate of `advanced-workflows.md` sections (Large Codebase Analysis 172 vs advanced-workflows 133; migration 224 vs 107; review 256 vs 177); also `integration-patterns.md`, `agents.md` combos.
3. **Accuracy.** 11 `/sc:implement` uses including `--no-mcp` and `--c7` flags (72, 158, 162) whose acceptance by the current executor is UNVERIFIED; `/sc:workflow "improvement plan based on analysis"` (187). No new skills mentioned. Security audit pattern (258-266) uses `/sc:analyze` + agents, while the new guide routes pre-PR security to `/security-review` (guide 3.11 step 3).
4. **Unique content.** None needed.
5. **Inbound references (live).** DOC only: `docs/reference/README.md:29,59,181,249,250,266`.
6. **Verdict: RETIRE.**

---

## 17a. docs/reference/commands-list.md (88 lines)

1. **Purpose and audience.** "Complete list of all 30 slash commands ... v4.1.9+" (3), grouped by category, with install and help notes.
2. **Routing content.** A one-line-per-command category list (5-59). Overlap: `commands.md` categories (149-212), `comprehensive-features.md`, `src/superclaude/commands/README.md` (agent/installer-facing README, out of my scope), `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md`.
3. **Accuracy.**
   - Lists `/estimate` (11), `/select-tool` (55), and `/sc` (59, 88); none exist in `src/superclaude/commands/`. [CODE-CONTRADICTED]
   - `/reflect` = "Reflection and retrospectives" (27) is wrong; `/task` = "Task management and tracking" (41) conflates `/sc:task` with the MDTM `/task` skill; `/workflow` = "Custom workflow automation" (42) is wrong for the plan generator.
   - Missing 16 current commands (adversarial, auggie-review, cleanup-audit, cli-eval, cli-portify, init-lite, post-release, pr-submit, release-split, review-translation, roadmap, swarm-wizard, tasklist, tdd, validate-roadmap, validate-tests) and all unprefixed skills.
   - "30 commands" vs 44 files. [CODE-CONTRADICTED]
4. **Unique content.** None.
5. **Inbound references (live).** DOC only: `docs/reference/comprehensive-features.md:7,189`.
6. **Verdict: RETIRE.** If a flat command list is wanted, it belongs as one table inside the slimmed `commands.md` (section 4), generated from the command files.

---

## 17b. docs/reference/suggested-commands.md (158 lines)

1. **Purpose and audience.** Japanese-language list of install, dev-env, test, and slash commands (title "推奨コマンド集", line 1). Looks like a copy of a Serena `suggested_commands` memory (commands.md 1415 names that memory file). UNVERIFIED origin.
2. **Routing content.** A short "development commands" block (140-158). Overlap: README dev workflow, installation.md.
3. **Accuracy.** `SuperClaude install --list-components` and `--components` (17-21): not options of `install` (`src/superclaude/cli/main.py:29-56`). [CODE-CONTRADICTED] `@agent-backend`, `@agent-security` (155-156) wrong handles. Uses `pip install -e` while README mandates UV (README 68, 189).
4. **Unique content.** None.
5. **Inbound references (live).** None. One historical `.dev/` reference.
6. **Verdict: RETIRE.** Orphan, wrong language for the rest of the docs set, inaccurate.

---

## 17c. docs/reference/comprehensive-features.md (192 lines)

1. **Purpose and audience.** Feature inventory "restored in v4.1.9+" (3): counts and lists of commands, agents, modes, MCP servers, docs.
2. **Routing content.** None (inventory only). Overlap: `commands-list.md`, `agents.md`, `mcp-installation.md`.
3. **Accuracy.** Counts 30 commands, 20 agents, 7 modes, 8 MCP (174-183): commands and agents counts are wrong (44 and 46). MCP list (68-74) is current. Related-doc links use `../User-Guide/` and `../Getting-Started/` capitalised paths (189-192) that do not exist on a case-sensitive filesystem (folders are lowercase). [CODE-CONTRADICTED]
4. **Unique content.** None that the routing guide needs.
5. **Inbound references (live).** None. 38 historical `.dev/` references (including PR-202 review JSON).
6. **Verdict: RETIRE.** Orphan inventory with wrong counts.

---

## 17d. Non-routing reference files (kept out of this consolidation)

| File | Purpose | Routing content | Accuracy notes | Live inbound refs | Verdict |
|---|---|---|---|---|---|
| `docs/reference/common-issues.md` (89) | Quick troubleshooting | None | Not deep-checked | `agents.md:691,761`, `modes.md:507,606`, `docs/reference/README.md` (6), `mcp-server-guide.md:603`, **`src/superclaude/agents/rf-team-lead.md:407`** and **`src/superclaude/templates/documents/agent_template_worker.md:340`** (shipped agent and template text) | KEEP AS IS (out of scope; note the two shipped-asset references) |
| `docs/reference/troubleshooting.md` (176) | Troubleshooting guide | None | Magic API key (98), `@agent-security` (79), `SuperClaude install --components` (95) [CODE-CONTRADICTED] | `agents.md:692`, `modes.md:508`, `mcp-servers.md:25`, `common-issues.md:89`, `examples-cookbook.md:193`, `docs/reference/README.md` (3) | KEEP BUT UPDATE (fix the three stale items; not routing) |
| `docs/reference/diagnostic-reference.md` (338) | Advanced diagnostics | None | Not deep-checked | `agents.md:767`, `modes.md:617`, `docs/reference/README.md` (4), `mcp-server-guide.md:604` | KEEP AS IS |
| `docs/reference/mcp-server-guide.md` (625) | MCP troubleshooting | None | The one "Sequential" hit (198) is "Sequential server restart", a false positive | `docs/reference/README.md:27,61` | KEEP AS IS (consider merging with `docs/user-guide/mcp-servers.md` later; not a routing issue) |
| `docs/reference/claude-code-history-management.md` (623) | 2025-10-09 research on `.jsonl` history rotation | "When to use" hits (332, 350) refer to cleanup scripts, not commands | Not checked | None (2 historical) | KEEP AS IS or move to `.dev/research` (out of scope) |
| `docs/reference/deviation-report-format.md` (106) | Canonical deviation-report schema | None | Live contract | **CODE: `src/superclaude/cli/tasklist/prompts.py:36`** | KEEP AS IS (code-referenced contract) |
| `docs/reference/nfr-conv-2-prose-determinism.md` (166) | Task-builder prose-determinism boundary | None | Live contract | **TEST: `tests/audit/test_nfr_conv_9_zero_trust.py:68`** | KEEP AS IS (test-pinned) |
| `docs/reference/pm-agent-autonomous-reflection.md` (662) | 2025-10-17 PM-agent design note | None | Not checked | `docs/user-guide/memory-system.md:269` | KEEP AS IS (out of scope) |

---

## 17. docs/reference/integration-patterns.md (316 lines)

1. **Purpose and audience.** Framework-specific prompt patterns (React, Node, Python, full-stack), MCP/agent combinations, API/DB/testing patterns, debugging and review patterns.
2. **Routing content.** Whole file is "for framework X, run these commands". Overlap: `basic-examples.md` common tasks, `advanced-patterns.md`, `flags.md` usage patterns.
3. **Accuracy.** 26 `/sc:implement` uses, many with `--c7` (22, 43, 64) UNVERIFIED against the current option list. No Sequential/Magic hits. No new skills.
4. **Unique content.** Framework-specific prompt wording is generic and not IronClaude-specific. Nothing to carry.
5. **Inbound references (live).** DOC only: `examples-cookbook.md` (18 links), `docs/reference/README.md:31,74,175,241-244,251`.
6. **Verdict: RETIRE.**

---

## 18. docs/guides/prd-skill-release-guide.md (699) and docs/guides/tdd-skill-release-guide.md (747)

1. **Purpose and audience.** Release guides for the `/prd` and `/tdd` skills (frontmatter last_updated 2026-04-03 for PRD, line 5): what, when, how, the 7-phase pipeline, tiers, QA gates, artifacts, limits, troubleshooting, use cases. Users and maintainers.
2. **Routing content.**
   - "Use when" lists (PRD 92-98; TDD section 2 at 89).
   - Input requirements table WHAT / WHY / WHERE / OUTPUT (PRD 106-113): same four inputs as new guide section 2.
   - "End-to-End Workflow: PRD, TDD, Roadmap, Tasklist, Execution" (PRD 461-505; TDD 483-537). This routes PRD then TDD then `superclaude roadmap run spec.md` then `/sc:tasklist` then `superclaude sprint run`.
   Overlap: new guide 3.1 (PRD then spec-panel then TDD then spec-panel then release-split then `/roadmap` then `/task`); `roadmap-cli-tools-release-guide.md` section 11; `sprint-cli-tools-release-guide.md`.
3. **Accuracy.**
   - Skills exist (`src/superclaude/skills/prd`, `src/superclaude/skills/tdd`). [CODE-VERIFIED] Stage A / Stage B description (PRD 43-50) matches the canonical task-builder + task architecture.
   - The section 9 pipeline conflicts with the new guide: the guide's default is the `/roadmap` skill producing task files run with `/task`, and it labels `/sc:roadmap` + `/sc:tasklist` + `superclaude sprint run` as "a separate release pipeline; use `/roadmap` unless your lead says otherwise" (guide 232). The release guides present only the release pipeline and never mention the `/roadmap` skill. Conflicting routing.
   - PRD "Use when" (98) says feed into `/tdd` or `/sc:roadmap`. Same conflict.
   - The "Sequential" scan hits (PRD 181, 451; TDD 198, 473) are the word "Sequential" in phase tables, not the removed MCP. False positives.
   - Neither mentions `/sc:spec-panel` critique or `/sc:release-split`, which the new guide inserts between PRD, TDD, and roadmap.
4. **Unique content to absorb.** Pipeline internals, tiers, gates, costs, limitations, troubleshooting are unique per-skill reference and must stay. For the new guide: the PRD example prompts (PRD 117-133) are good models of a strong request; the guide already has its own. The "Feature PRD vs Product PRD misclassification" gotcha (PRD 543) is worth one line in the guide's 3.1 step 2 (UNVERIFIED whether still true).
5. **Inbound references (live).** PRD: `docs/guides/RELEASE-GUIDE-INSTRUCTIONS.md:33`, `tdd-skill-release-guide.md:493`. TDD: `RELEASE-GUIDE-INSTRUCTIONS.md:34`. No code/test refs (one historical reflect-stdout JSON each).
6. **Verdict: KEEP BUT UPDATE (both).** Replace each section 9 with: "Default path: `/prd`, `/tdd`, `/roadmap`, `/task` (see the user guide 3.1). Alternative release pipeline: `superclaude roadmap run`, `/sc:tasklist`, `superclaude sprint run`." Change PRD line 98 accordingly.

---

## 19. docs/guides/roadmap-cli-tools-release-guide.md (1414) and docs/guides/sprint-cli-tools-release-guide.md (594)

1. **Purpose and audience.** CLI reference for `superclaude roadmap run/validate/accept-spec-change` and `superclaude sprint run`. Operators.
2. **Routing content.** "Command Reference: When and How to Use" (roadmap 96), "End-to-End Workflow: Spec, Roadmap, Tasklist, Execution" (roadmap 1048-1108), "Integration with Slash Commands and Skills" (roadmap 1175-1199, compares CLI vs `/sc:roadmap`). Sprint guide frames itself inside "spec, roadmap, tasklist, execution" (sprint 6-10).
3. **Accuracy.** CLI groups exist (`src/superclaude/cli/main.py:455-467`). [CODE-VERIFIED] The roadmap guide never mentions the `/roadmap` skill (the scan's `/roadmap` hits at 136, 1265, 1388 are path fragments like `<output_dir>/roadmap.md`), so a reader cannot tell `/roadmap` (skill) from `superclaude roadmap` (CLI) from `/sc:roadmap` (slash command). This is the exact mix-up the new guide warns about (guide 232).
4. **Unique content.** All unique CLI reference. Nothing moves to the routing guide except a disambiguation sentence.
5. **Inbound references (live).** Roadmap: `RELEASE-GUIDE-INSTRUCTIONS.md:31`, `prd-skill-release-guide.md:487`, `tdd-skill-release-guide.md:509`. Sprint: **TEST `tests/sprint/test_sprint_docs_cli_parity.py:38`** (flag parity test pins this file's option bullets), `KNOWLEDGE.md:325`, `RELEASE-GUIDE-INSTRUCTIONS.md:32`, `prd-skill-release-guide.md:503`, `tdd-skill-release-guide.md:525`.
6. **Verdict: KEEP BUT UPDATE (roadmap guide):** add a 3-line "Not to be confused with" box naming `/roadmap` (skill, default for feature work) vs `/sc:roadmap` vs `superclaude roadmap`. **KEEP AS IS (sprint guide):** test-pinned; do not move or rename.

---

## 20. docs/guides/reflect-cli-tools-guide.md (468)

1. **Purpose and audience.** `superclaude reflect run` auto-fix engine: flags, carve-outs, exit codes, gate sites. Operators.
2. **Routing content.** "Command Reference: When and How to Use" (72) and the "task / per-phase gate, audit, auto-fix, verify, promote" workflow (12). Overlap: `commands.md` 997-1029 (summary copy), `flags.md` 129-150 (skill flags), new guide 3.1 step 9 and 3.10 (when a human should run `/sc:reflect` by hand).
3. **Accuracy.** Test-pinned against the Click command (`tests/cli/reflect/test_docs_cli_parity.py:25-40` reads this file and compares `--long` flags). [CODE-VERIFIED by test design; test not executed here]
4. **Unique content.** Canonical. Nothing to move.
5. **Inbound references (live).** **TEST `tests/cli/reflect/test_docs_cli_parity.py:30`**, `README.md:98`, `POST-REFLECT-TASK.md:594`, `docs/user-guide/commands.md:1029`, `docs/user-guide/flags.md:150`.
6. **Verdict: KEEP AS IS.** It is the canonical target that commands.md's duplicate summary (997-1029) should collapse into.

---

## 21. docs/guides/cli-portify-and-pipeline-runner-guide.md (647), suites-guide.md (600), RELEASE-GUIDE-INSTRUCTIONS.md (168), RELEASE-GUIDE-TEMPLATE.md (320)

| File | Purpose | Routing content | Accuracy notes | Live inbound refs | Verdict |
|---|---|---|---|---|---|
| `cli-portify-and-pipeline-runner-guide.md` | How to port an inference workflow to a deterministic CLI runner | Explains `/sc:roadmap` vs `superclaude roadmap run` (25-35, 92-95); contributor-facing | "Sequential" hits (170, 183, 327, 341) not checked line by line; likely prose usage. UNVERIFIED | None live (20 historical) | KEEP AS IS (developer topic, not user routing) |
| `suites-guide.md` | cliEval suites operator guide | None for slash commands | Not checked | **CODE/DATA: `src/superclaude/cli/eval/suites/eval_cli_doc_parity.yaml:8,14,64,95`**, `src/superclaude/agents/eval-docs-loader.md:41`, `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:108` and 4 refs files | KEEP AS IS (code-pinned) |
| `RELEASE-GUIDE-INSTRUCTIONS.md` | How to write a release guide | None | Links to the prd/tdd/roadmap/sprint guides (31-34) | None live | KEEP AS IS (authoring meta) |
| `RELEASE-GUIDE-TEMPLATE.md` | Template for release guides | Template "when to use" heading (14) | "Sequential" hit (120) not checked. UNVERIFIED | `RELEASE-GUIDE-INSTRUCTIONS.md:36` | KEEP AS IS. Optional: add a template line "Where this fits in the user guide" so future release guides link the routing guide instead of re-describing workflows |

---

## 22. docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md (2126) and docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md (2084)

1. **Purpose and audience.** Contributor guide to authoring commands, agents, skills (v1.0.0, 2026-02-21, lines 3-5). Not user routing.
2. **Routing content.** Command archetypes (around 318-360), thinking-depth flag "when to use" (935-941 developer-guide copy). Minor.
3. **Accuracy.** The two files are identical except for 42 blank lines (verified: `diff` after stripping blank lines is empty). Both start with a stray `p` before the H1 (`p# SuperClaude Developer Guide...`, line 1). Mentions `/sc:task-unified` (developer-guide copy ~323), which no longer exists (current file is `task.md`). [CODE-CONTRADICTED] Wave-enabled command list and persona frontmatter are older-generation. Not deep-checked beyond the routing sections.
4. **Unique content.** Authoring guidance is unique to these two files (one copy).
5. **Inbound references (live).** None for either copy. guides/ copy: 52 historical `.dev/` doc refs plus 12 in `.dev/releases/*/v3.66-tdd-skill-refactor-v2/*.json`. developer-guide/ copy: 24 historical.
6. **Verdict:** `docs/guides/` copy: **RETIRE (MERGE INTO `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`)**, a byte-for-byte duplicate apart from blank lines. `docs/developer-guide/` copy: **KEEP BUT UPDATE** (remove the stray `p`, fix `/sc:task-unified`); out of routing scope otherwise.

---

## 23. docs/developer-guide/* (only sections about choosing commands)

| File | Routing content | Accuracy notes | Live inbound refs | Verdict |
|---|---|---|---|---|
| `README.md` (198) | Index of developer docs only | Not checked | `SuperClaude-Developer-Guide...md:1230`, `git-standards-protocols.md:110` | KEEP AS IS |
| `documentation-index.md` (295) | Topic index into developer docs | Not checked | `README.md:27` | KEEP AS IS |
| `technical-architecture.md` (367) | "Command Processing" (218-222) and "How Claude Code Reads Context" (286-290) use `/sc:implement "auth system"` auto-activating security-engineer and Context7 | Lists `select-tool.md` in the installed tree (102) [CODE-CONTRADICTED]; paths `superclaude/Commands/implement.md` (287) and `commands/sc/implement.md` (218) are old layouts; `@agent-security` (118) wrong handle | 40+ DOC refs (documentation-index, user-guide, getting-started), DATA `PROJECT_INDEX.json:137` | KEEP BUT UPDATE (fix examples; not routing) |
| `contributing-code.md` (431) | Example `/sc:implement` (88) | Minor | 43 DOC refs, DATA `PROJECT_INDEX.json:136` | KEEP AS IS for this effort |
| `git-standards-protocols.md` (894) | "When to Use Hotfix" (613) is git branching, not command routing | Looks like a GFxAI-style git standard (Golden Path test tiers, line 68). UNVERIFIED whether it applies to IronClaude | `documentation-index.md` (10) | Out of scope; flag to the user as possibly foreign content |
| `testing-debugging.md` (332), `sprint-tui-reference.md` (992) | None | Not checked | testing-debugging 33 DOC refs + `.github/workflows/README.md:173`; sprint-tui none live | KEEP AS IS |

---

## 24. docs/swarm/wizard-guide.md (222)

1. **Purpose and audience.** Plain-language guide to `/sc:swarm-wizard` for non-experts (3-10): what it asks, the 7 lenses as goals (58-66), safety rules, credentials, reading results, troubleshooting, flags.
2. **Routing content.** "You want to..." to lens table (58-66) and "Related commands" hand-offs (208-213). This is routing *inside* swarm. Overlap: new guide 3.6 row 4 (one line pointing at `/sc:swarm-wizard`); `docs/swarm/user-guide.md` section 4 "Choosing a lens" (186-196, same 7 lenses with hand-off targets); `docs/swarm/lens-catalog.md`.
3. **Accuracy.**
   - Flag list (194-206) matches `src/superclaude/commands/swarm-wizard.md:7` argument-hint exactly. [CODE-VERIFIED]
   - Hand-off target `/sc:code-review` (210, and `user-guide.md` lens table) does not exist as a command; the code-review tool is the Claude Code `/code-review` skill. [CODE-CONTRADICTED]
   - Says a run produces `merged.md` and `return-contract.yaml` (98-103). `docs/swarm/README.md:7-14` says the Wave 2/3 writer "is not yet wired into the run path". Code shows `reduce_wave3` writing `merged.md` (`src/superclaude/cli/swarm/reduce.py:74,138`) and the run path calling it (`src/superclaude/cli/swarm/commands.py:973-976, 2087-2088`), so the wizard guide looks current and the swarm README status note looks stale. Partly UNVERIFIED (run path read only at comment level).
4. **Unique content.** All unique and well-pitched for humans. The new guide should link it from 3.6 ("You want reviewers from other AI model families").
5. **Inbound references (live).** `docs/swarm/README.md:23` only. No code/test refs. (Note `docs/swarm/user-guide.md` is test-pinned by `tests/swarm/test_e2e_user_guide.py:1`; the wizard guide is not.)
6. **Verdict: KEEP BUT UPDATE.** Replace `/sc:code-review` with `/code-review`; link it from the new guide 3.6. Separately, the swarm README's "implementation status" box (7-14) should be re-verified and probably removed (out of my scope, flagged).

---

## 25. docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md (292) and siblings

1. **Purpose and audience.** Generated contributor map of commands to skills (1-13). Claims to be "current, repository-grounded".
2. **Routing content.** Command-to-skill matrix (55-124, 260-280). It routes contributors, not users.
3. **Accuracy.** Heavily stale: references `task-unified.md`, `task-mcp.md`, `sc-task-unified-protocol`, `sc-forensic-qa-protocol`, `sc-recommend-protocol`, `sc.md`, `select-tool.md`, `estimate` (69, 95, 110-112, 116-122, 270); none exist in `src/superclaude/commands` or `skills` today. Says `/sc:implement`, `/sc:workflow`, `/sc:brainstorm`, `/sc:reflect`, `/sc:troubleshoot` have no protocol skill (117-120, 270), but `sc-implement-protocol`, `sc-workflow-protocol`, `sc-brainstorm-protocol`, `sc-reflect-protocol`, `sc-troubleshoot-protocol` all exist. Absolute paths point at `/config/workspace/SuperClaude_Framework/` (284-291). [CODE-CONTRADICTED]
4. **Unique content.** None that is still true.
5. **Inbound references (live).** `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:592`. Siblings `contributor-workflow.md` and `README.md` are only referenced inside the same generated bundle.
6. **Verdict: RETIRE** the cross-reference file (or regenerate it from code if the agent-facing workstream wants a command-to-skill table). The rest of the generated bundle is out of routing scope.

---

## Related routing surfaces found but NOT in my scope (hand to the agent-facing workstream)

| Path | Why it matters |
|---|---|
| `src/superclaude/commands/README.md` (22 lines) | Installed to `~/.claude/commands/sc/`; lists a handful of commands. Agent/installer-facing. |
| `src/superclaude/core/COMMANDS.md` (195 lines), `ORCHESTRATOR.md`, `FLAGS.md`, `MCP.md` | Agent-facing routing rules loaded by Claude; likely the largest "which command when" surface for agents. |
| `commands/sc-*.md`, `commands/sc-README.md`, `agents/sc-*.md` (repo root) and `plugins/` | Plugin/distribution copies of commands and agents; may carry stale routing text. |
| `src/superclaude/commands/brainstorm.md:134` | Says hand-off goes to `/sc:task-builder`; the skill is `task-builder`. |
| `docs/swarm/README.md:7-14` | "Wave 2/3 writer not yet wired" status box looks stale against `cli/swarm/commands.py:973-976`. |

---

## Overlap matrix (routing topics vs files)

Rows are the routing topics the new guide covers; cells name the other files that also try to answer them. "Conflicts" means the other file gives a different answer than the new guide.

| Routing topic (new guide section) | Other files covering it | Conflicts? |
|---|---|---|
| How much process / which level (1) | `commands.md` Visual Map 1033-1082 and task-vs-implement 1222-1290; `quick-start.md` "When to Use" 273-326; `modes.md` activation table 473-486 | Yes: commands.md routes "PRD ready" to `/sc:workflow` and "critical code" to `/sc:task`; new guide routes multi-file/risky work to `/task-builder` + `/task` |
| How to write a request (2) | `prd-skill-release-guide.md` 106-113, `tdd-skill-release-guide.md` section 2 (same WHAT/WHY/WHERE/OUTPUT) | No (consistent) |
| Full spec workflow PRD, TDD, roadmap (3.1) | `prd-skill-release-guide.md` 461-505, `tdd-skill-release-guide.md` 483-537, `roadmap-cli-tools-release-guide.md` 1048-1108, `commands.md` "Enterprise-level Feature" 1627-1639 and "Business Idea" 1571-1582, `advanced-workflows.md` 67-130 | Yes: release guides route to `superclaude roadmap run` + `/sc:tasklist` + sprint; commands.md routes to `/sc:workflow` + `/sc:spawn` + `/sc:task` |
| Add a feature (3.2) | `commands.md` "New Feature" 1528-1536; `basic-examples.md` 215-329; `advanced-workflows.md` 20-46; `integration-patterns.md`; `quick-start.md` 212-255 | Yes: all route features straight to `/sc:implement "<feature>"` |
| Small change (3.3) | `commands.md` 1233-1290; `basic-examples.md` 309-329 | Partly: they use banned `/sc:implement --type/--framework` flags |
| Fix a bug (3.4) | `commands.md` "Bug Fix" 1540-1546; `basic-examples.md` 249-262, 391-440; `advanced-workflows.md` 47-65; `integration-patterns.md` 244-260 | Yes: no failing-test-first step; `--trace` flag does not exist |
| Investigate (3.5) | `commands.md` `/sc:research` 445-469; `basic-examples.md` 94-142 | No major conflict, but none mention `/tech-research` |
| Decide / compare (3.6) | `commands.md` panels 934-944, "Pitch" 1614-1623; `brainstorm.md`; `swarm/wizard-guide.md`; `swarm/user-guide.md` 186-196 | No |
| Refactor / cleanup (3.7) | `commands.md` "Refactoring" 1550-1557; `advanced-patterns.md` 224-254 | Yes: no cleanup-audit, no commit-first, no task-builder for large refactors |
| Tests (3.8) | `commands.md` `/sc:test` 651-679; `flags.md` | No |
| Document (3.9) | `commands.md` `/sc:document` 738-763; `agents.md` technical-writer | Partly: none mention `/tech-reference`, `/readme`, `/operational-guide` |
| Check a plan (3.10) | `flags.md` reflect table 129-150; `commands.md` 968-995; `session-management.md` 59-82 | Yes: session-management.md uses `/sc:reflect` as a memory progress check |
| Review and PR (3.11) | `commands.md` "Code Review" 1561-1567; `advanced-patterns.md` 256-286 | Yes: route review to `/sc:analyze`; no `/code-review`, `/security-review`, `/sc:auggie-review`, `/sc:pr-submit` |
| Resume (3.12) | `session-management.md` 110-157 (`/sc:load`, `/sc:save`) | Different mechanism, not strictly conflicting |
| Mix-ups (5) | `commands.md` Key Differences 1086-1095, spawn/task/implement 1099-1218, design vs workflow 1294-1392 | Yes: old distinctions; none cover `/task` vs `/sc:task`, `/roadmap` vs `/sc:roadmap`, `/tech-research` vs `/sc:research` |

---

## Content the new guide (or a kept file) must absorb so nothing valuable is lost

| # | Content | Source | Suggested home |
|---|---|---|---|
| 1 | spec-panel vs business-panel by document type, PRD = both | `commands.md` 934-944 | New guide 3.6 (one sentence) |
| 2 | "Does it change files?" split: document-only vs execution commands | `commands.md` 216-249 | Slimmed `commands.md` reference, one column |
| 3 | `/sc:brainstorm --handoff task` straight to a task file | `brainstorm.md` 165-173 | New guide 3.1 step 1 (optional sentence) |
| 4 | Swarm lens chooser (goal to lens) | `swarm/wizard-guide.md` 58-66 | Stays in wizard guide; new guide links it from 3.6 |
| 5 | `/roadmap` vs `/sc:roadmap` vs `superclaude roadmap` disambiguation | Only in new guide 5 today | Add a short box to `roadmap-cli-tools-release-guide.md` and to PRD/TDD guide section 9 |
| 6 | Reflect CLI exit codes (0, 10, 11, 2) and `--promote` default on | `commands.md` 997-1029, canonical in `reflect-cli-tools-guide.md` | Keep only in `reflect-cli-tools-guide.md` |
| 7 | `/sc:load` / `/sc:save` session memory | `session-management.md` | New guide 3.12, one row, only if the team uses Serena memory (UNVERIFIED) |
| 8 | index-repo vs Serena comparison | `commands.md` 1396-1501 | `docs/user-guide/mcp-servers.md` or drop (user decides) |
| 9 | Per-agent profiles and keyword triggers | `agents.md` 146-653, 812-829 | Stay in `agents.md` |
| 10 | `/sc:git`, `/sc:build`, `/sc:spawn`, `/sc:index`, `/sc:agent`, `/sc:help` syntax | `commands.md` per-command sections | Slimmed `commands.md` reference |
| 11 | Correction for the new guide itself: `/sc:workflow` output path is `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/<id>.md`, and `/sc:implement` on a managed package uses the sibling `progress.md` and archives to `.dev/tasks/done/` | `src/superclaude/commands/workflow.md:12`, `implement.md:63-65` | New guide lines 15, 110-113, 207 |

---

## Summary: verdicts

| # | File | Lines | Verdict | Blocking refs (code/test/install) |
|---|---|---|---|---|
| 1 | `README.md` | 272 | KEEP BUT UPDATE (add link to user guide; drop Sequential/Magic/Chrome DevTools; fix PLANNING.md/TASK.md links) | INSTALL: `pyproject.toml:9,95`, `MANIFEST.in:2`, `package.json:13`, `Makefile:100,103` |
| 2 | `docs/getting-started/quick-start.md` | 505 | RETIRE (replace with user guide, or a pointer stub) | none |
| 3 | `docs/getting-started/installation.md` | 553 | KEEP BUT UPDATE | none |
| 4 | `docs/user-guide/commands.md` | 1700 | KEEP BUT UPDATE as per-command reference; strip routing sections | none |
| 5 | `docs/user-guide/agents.md` | 1048 | KEEP BUT UPDATE (agent reference only) | none |
| 6 | `docs/user-guide/modes.md` | 727 | KEEP BUT UPDATE | none |
| 7 | `docs/user-guide/flags.md` | 309 | KEEP BUT UPDATE | none |
| 8 | `docs/user-guide/mcp-servers.md`, `mcp-installation.md` | 352, 239 | KEEP AS IS | none |
| 9 | `docs/user-guide/brainstorm.md` | 233 | KEEP BUT UPDATE (`/sc:task-builder` to `/task-builder`) | none |
| 10 | `docs/user-guide/session-management.md` | 377 | KEEP BUT UPDATE (remove `/sc:reflect` misuse) | none |
| 11 | `docs/user-guide/memory-system.md`, `eval-pipeline.md`, `freshness-hooks.md` | | KEEP AS IS | none |
| 12 | `docs/reference/README.md` | 266 | KEEP BUT UPDATE (shrink to index) | none |
| 13 | `docs/reference/examples-cookbook.md` | 199 | RETIRE | none |
| 14 | `docs/reference/basic-examples.md` | 613 | RETIRE | none |
| 15 | `docs/reference/advanced-workflows.md` | 310 | RETIRE | none |
| 16 | `docs/reference/advanced-patterns.md` | 329 | RETIRE | none |
| 17 | `docs/reference/integration-patterns.md` | 316 | RETIRE | none |
| 17a | `docs/reference/commands-list.md` | 88 | RETIRE | none |
| 17b | `docs/reference/suggested-commands.md` | 158 | RETIRE | none |
| 17c | `docs/reference/comprehensive-features.md` | 192 | RETIRE | none |
| 17d | `common-issues`, `troubleshooting` (update), `diagnostic-reference`, `mcp-server-guide`, `claude-code-history-management`, `deviation-report-format`, `nfr-conv-2-prose-determinism`, `pm-agent-autonomous-reflection` | | KEEP (troubleshooting.md: KEEP BUT UPDATE) | CODE: `cli/tasklist/prompts.py:36` (deviation-report-format); TEST: `tests/audit/test_nfr_conv_9_zero_trust.py:68` (nfr-conv-2); shipped assets `src/superclaude/agents/rf-team-lead.md:407`, `src/superclaude/templates/documents/agent_template_worker.md:340` (common-issues) |
| 18 | `docs/guides/prd-skill-release-guide.md`, `tdd-skill-release-guide.md` | 699, 747 | KEEP BUT UPDATE (section 9 pipeline) | none |
| 19 | `docs/guides/roadmap-cli-tools-release-guide.md` / `sprint-cli-tools-release-guide.md` | 1414, 594 | KEEP BUT UPDATE (disambiguation box) / KEEP AS IS | TEST: `tests/sprint/test_sprint_docs_cli_parity.py:38` (sprint) |
| 20 | `docs/guides/reflect-cli-tools-guide.md` | 468 | KEEP AS IS (canonical) | TEST: `tests/cli/reflect/test_docs_cli_parity.py:30` |
| 21 | `docs/guides/cli-portify...`, `suites-guide.md`, `RELEASE-GUIDE-*` | | KEEP AS IS | CODE/DATA: `src/superclaude/cli/eval/suites/eval_cli_doc_parity.yaml:8,14,64,95` and sc-cli-eval-protocol refs (suites-guide) |
| 22 | `docs/guides/SuperClaude-Developer-Guide-...md` | 2126 | RETIRE, MERGE INTO `docs/developer-guide/` copy (identical apart from blank lines) | none live |
| 22 | `docs/developer-guide/SuperClaude-Developer-Guide-...md` | 2084 | KEEP BUT UPDATE (stray `p`, `/sc:task-unified`) | none live |
| 23 | `docs/developer-guide/technical-architecture.md` | 367 | KEEP BUT UPDATE (examples only) | none |
| 23 | other developer-guide files | | KEEP AS IS (git-standards-protocols flagged as possibly foreign) | `.github/workflows/README.md:173` (testing-debugging) |
| 24 | `docs/swarm/wizard-guide.md` | 222 | KEEP BUT UPDATE (`/sc:code-review` to `/code-review`; link from guide 3.6) | none |
| 25 | `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md` | 292 | RETIRE (or regenerate from code) | none |

**Net effect:** human routing collapses to one document (the new user guide) plus per-command references (`commands.md` slimmed, `brainstorm.md`, `swarm/wizard-guide.md`, the per-skill release guides). 10 human-facing routing files retire; none has a code, test, or install reference.

## Proposed removals (each for the user to adjudicate)

- **Remove `docs/getting-started/quick-start.md`**: its whole job is first-session routing, and every route it gives is superseded or wrong (Magic, fake agent handles, old `/sc:implement`). Repoint 8 doc links to the new guide.
- **Remove `docs/reference/examples-cookbook.md`**: a hub to three retiring collections; 26 of 38 anchors are already dead.
- **Remove `docs/reference/basic-examples.md`**: routes every feature through `/sc:implement`, contradicting the new guide's hard limit.
- **Remove `docs/reference/advanced-workflows.md`**: workflow sequences for large work that bypass task files; Sequential references.
- **Remove `docs/reference/advanced-patterns.md`**: near-duplicate of advanced-workflows topics; same routing problems.
- **Remove `docs/reference/integration-patterns.md`**: framework prompt recipes built on old `/sc:implement`; no IronClaude-specific value.
- **Remove `docs/reference/commands-list.md`**: lists removed `/estimate`, `/select-tool`, `/sc`; misses 16 commands.
- **Remove `docs/reference/suggested-commands.md`**: orphan Japanese-language file with invalid install flags; no inbound links.
- **Remove `docs/reference/comprehensive-features.md`**: orphan inventory with wrong counts and broken capitalised links.
- **Remove `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`**: exact duplicate of the `docs/developer-guide/` copy.
- **Remove `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md`**: generated map that is now wrong on most rows.
- **Remove from `docs/user-guide/commands.md` these sections**: Visual Map (1033-1082), Key Differences (1086-1095), spawn vs task vs implement (1099-1218), task vs implement (1222-1290), design vs workflow (1294-1392), Typical Workflows (1505-1644), File Map and Notes for Future Sessions (57-145, 1648-1696). Why: routing duplicates that conflict with the new guide, or agent-facing notes pointing at nonexistent files.
- **Remove from `docs/user-guide/modes.md` "Real-World Examples" (419-470)** and from `docs/user-guide/flags.md` "Common Usage Patterns" (214-250): routing duplicates with stale commands.
- **Remove from `docs/user-guide/session-management.md` all `/sc:reflect` usage** (59-82, 135-157, 241-326): wrong tool for memory checks; flags `--cleanup`, `--repair`, `--scope project` do not exist in that form.

## Gaps and open questions

| # | Item | Status |
|---|---|---|
| 1 | Whether `/sc:implement` silently accepts or rejects unknown flags like `--c7`, `--no-mcp`, `--all-mcp` (used in many examples) | UNVERIFIED; only the four banned flags are confirmed STOPs |
| 2 | Whether persona auto-activation still happens for `/sc:implement`, `/sc:design`, `/sc:troubleshoot` as agents.md claims | UNVERIFIED |
| 3 | Whether `@agent-<file-name>` (for example `@agent-security-engineer`) is the handle Claude Code resolves | UNVERIFIED |
| 4 | Whether `/sc:pm` is really "always active" | UNVERIFIED |
| 5 | Swarm README status box vs code: run path appears to call `reduce_wave3` and write `merged.md` | Partly verified (`cli/swarm/commands.py:973-976, 2087-2088`; `reduce.py:74,138`) |
| 6 | `docs/developer-guide/git-standards-protocols.md` looks like GFxAI-origin content | UNVERIFIED |
| 7 | The new guide's own `/sc:workflow` plan path (`.dev/workflow/<name>/plan.md`) disagrees with current code | [CODE-CONTRADICTED], must be fixed before the guide becomes the anchor |
| 8 | Reflect and sprint docs parity tests were read, not executed | Tests not run |
| 9 | Several non-routing files (diagnostic-reference, common-issues, cli-portify guide, RELEASE-GUIDE-TEMPLATE) were not deep-checked for accuracy | Out of routing scope |


