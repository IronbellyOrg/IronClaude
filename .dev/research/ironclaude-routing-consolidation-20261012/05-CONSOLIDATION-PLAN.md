# IronClaude "What To Use When" Consolidation Plan

**Date:** 2026-10-12
**Source checked:** IronClaude origin/master `ee1c1787` (2026-10-11), snapshot at `/tmp/ic-master`
**Evidence:** `01-agent-facing-core.md`, `02-human-docs.md`, `03-help-recommend.md`, `04-machinery-and-references.md` (same folder)
**Status:** Removal list approved and all six section 7 decisions made by the user on 2026-10-12. Nothing in IronClaude code or docs has been changed yet.

---

## 1. What we found

1. **Twenty-plus files try to answer "what do I use when", and they disagree.** Human docs (quick start, the commands reference's Visual Map, four example collections, two command lists, a generated cross-reference) send features straight to `/sc:implement` or `/sc:workflow`. None of them mention `/task-builder`, `/task`, `/prd`, `/tdd`, `/tech-research`, `/roadmap`, or `/sc:pr-submit`. Several use flags that now stop the command with an error. (`02-human-docs.md`, overlap matrix)
2. **The agent-facing routing files are dead.** `superclaude install` copies 13 files from `src/superclaude/core/` into `~/.claude/`, but only `CLAUDE.md` and `BASH_INSPECTION_POLICY.md` are ever loaded into an agent's context. `ORCHESTRATOR.md`, `COMMANDS.md`, `PERSONAS.md`, `MODES.md`, `FLAGS.md`, and `MCP.md` lost their `@` imports on 2026-03-16 (commit `4b19eb08`). Since then they change nothing, and they still describe removed commands and MCP servers. (`01-agent-facing-core.md` sections 1.2, 4.2)
3. **The one always-loaded file has almost no routing.** `core/CLAUDE.md` only says "use `/sc:help`". The most important rule (a `/sc:<name>` message must invoke its skill) lives only in the contributor `CLAUDE.md`, so installed users never get it. (`01` section 4.2 items 2 and 4)
4. **`/sc:help` is a hand-written list** of 22 of 43 commands and none of the 36 skills, with six outdated descriptions. (`03` section 1)
5. **`/sc:recommend` never reads any workflow document,** recommends one tool at a time rather than a sequence, prefers plain edits and `/sc:*` commands where our guide says otherwise, only looks inside the IronClaude repo's own `src/` folder (so it may find nothing in a user project), and two of its four cached answers route to the wrong tool. (`03` sections 2, 3.2)
6. **Our new guide is already out of date in one place:** master changed `/sc:workflow` to write `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/<id>.md` (not `.dev/workflow/<name>/plan.md`), and `/sc:implement` now keeps its progress file beside that plan and moves the package to `.dev/tasks/done/` when finished. (`02` item 11)
7. **Removing files has three traps.** The installer never deletes, so retired files linger in every user's `~/.claude/` unless we add a cleanup step. `make sync-dev` never deletes, so local `make verify-sync` fails until stale mirrors are removed by hand. Root `commands/sc-*.md` are regenerated from the upstream SuperClaude repo every 6 hours by `pull-sync-framework.yml`, so they cannot be retired locally. (`04` section 5, rules R1-R3)

## 2. Target design: one source of truth, three ways in

| Piece | Role | Who uses it |
|---|---|---|
| **`src/superclaude/core/HOW-WE-WORK.md`** (the guide, moved into IronClaude) | The only place that says which tool, in what order, with which safe flags. Absorbs the unique content listed in section 4. Ends with one machine-readable routing table that help and recommend read. | Humans read it; `superclaude install` copies it to `~/.claude/HOW-WE-WORK.md`, a fixed path that agents, `/sc:help`, and `/sc:recommend` can read from any project. It is not imported into every session, so it costs no context until read. It must always be referred to as a plain path in backticks, never as an `@HOW-WE-WORK.md` import (an import would load it into every session); a test enforces this. Plugin installs do not get `core/` files, so see section 7 decision 1. |
| **`core/CLAUDE.md`** (always loaded for every user) | A short block: the six levels in one table, the hard limit, the `/sc:<name>` must-invoke-skill rule, and "for the full workflows read `~/.claude/HOW-WE-WORK.md`; unsure, run `/sc:recommend`". | Every agent, every session, once they run `superclaude update` (or `install --force`): a plain `install` does not replace an existing `~/.claude/CLAUDE.md`. |
| **`/sc:help`** (kept) | Lists what is actually installed (commands and skills, read live), prints the guide's level table, and points to the guide and `/sc:recommend`. No hand-maintained list. | Humans who want the menu. |
| **`/sc:recommend`** (kept) | Reads the guide first to decide the order of steps and the safe flags, then checks every command and flag against the real files (it already does this part well), and returns an ordered, paste-ready sequence. | Humans and agents who have a goal but not a tool. |
| **Per-tool reference docs** (kept, slimmed) | Exact syntax and options per command or skill: `docs/user-guide/commands.md` (reference only), the PRD, TDD, roadmap, sprint, and reflect release guides, `brainstorm.md`, `swarm/wizard-guide.md`, `agents.md`. They link to the guide for "when", and stop answering "when" themselves. | Humans needing detail. |

Add `docs/user-guide/how-we-work.md` as a one-paragraph pointer to the guide's location in source, so the content is authored once.

## 3. Every file: keep, update, merge, or retire

### 3.1 Agent-facing files (`src/superclaude/core/`, repo root)

| File | Verdict | What changes | References to update first |
|---|---|---|---|
| `core/CLAUDE.md` | **Update** | Add the routing block (section 2). Remove the persona auto-activation table, the "wave strategies live in the skill files" claim (`:102`, false), and the Key Docs entries for `KNOWLEDGE.md`, `PLANNING.md`, and `TASK.md` (`:91-93`; repo-only or nonexistent files). Repoint `RULES.md` and `PRINCIPLES.md` (`:94-95`) to `~/.claude/RULES.md` and `~/.claude/PRINCIPLES.md`. Move the IronClaude-contributor sections (Project Structure, Dev Commands, Component Sync, `:16-50`) to the repo-root `CLAUDE.md`. Mark the MCP table's flag column as advisory. Keep the `@BASH_INSPECTION_POLICY.md` import (a test pins it). | `tests/cli/test_bash_inspection_policy.py:31-33` must keep passing |
| `core/HOW-WE-WORK.md` | **New** (the guide) | Moved from `.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md`, corrected for master, with section 4 content absorbed | Add to `install_core.py:139-153` known file list |
| `core/ORCHESTRATOR.md` | **Retire** | Not loaded since March; routes to removed tools; its `/sc:task` tier rules are a drifted copy of `commands/task.md:71-93` | `skills/sc-task-protocol/SKILL.md:403-408` (point routing at `commands/task.md:71-93`, drop the three config files that do not exist, and replace "Circuit breakers: See MCP.md" with a pointer to the MCP table in `~/.claude/CLAUDE.md`); `cli/recommend/prompts.py:16` comment; both developer-guide copies; `PROJECT_INDEX.md:48`; test docstring `test_critical_corrections.py:7,61` |
| `core/COMMANDS.md` | **Retire** | Not loaded; covers 18 of 43 commands; wrong in 7+ places. Its job moves to the guide's routing table. | Developer-guide copies; `PROJECT_INDEX.md:44` |
| `core/PERSONAS.md` | **Retire** | Not loaded; persona flags are used by zero commands | `ORCHESTRATOR.md` (retiring); developer-guide copies; `PROJECT_INDEX.md:43` |
| `core/MODES.md` | **Retire** | Not loaded; references removed MCPs and commands. The separate `src/superclaude/modes/MODE_*.md` files are untouched. | Developer-guide line 99; `PROJECT_INDEX.md:47` |
| `core/FLAGS.md` | **Retire** | Flags are defined per command and often differ (for example `/sc:workflow` bans `--depth shallow|normal` and `--validate`). The guide's routing table lists the safe flags per workflow step and never presents a flag as shared. Nothing moves from this file. | 8 developer-guide and reference lines (`04` section 4.1); `plugins/superclaude/core/FLAGS.md` (drifted copy, nothing reads it) |
| `core/MCP.md` | **Retire** | `core/CLAUDE.md:52-60` already has a better MCP table | `skills/sc-task-protocol/SKILL.md:407` (handled in the ORCHESTRATOR row); `core/RESEARCH_CONFIG.md:133` |
| `core/BUSINESS_PANEL_EXAMPLES.md` | **Retire**, with its plugin copy `plugins/superclaude/core/BUSINESS_PANEL_EXAMPLES.md` | Orphaned; examples use flags that do not exist | `install_core.py:141`; one doc line |
| `core/BUSINESS_SYMBOLS.md` | **Decision needed (section 7)** | Not orphaned: `commands/business-panel.md:78` (`--structured`, "use symbol system") depends on it. Merging all 225 lines into the 129-line command would pass the 200-line lint warning. Options: keep as is, or move only the symbols `--structured` needs into the command (staying under 200 lines) and retire it with its plugin copy. | `install_core.py:142`; one doc line |
| `core/BASH_INSPECTION_POLICY.md` | **Keep as is** | Live, code-loaded, no routing | (5 code sites and 5 tests pin the name) |
| `core/RESEARCH_CONFIG.md` | **Keep, small fix** | Fix the Tavily version mismatch; drop the `MCP.md` pointer at line 133 (`RULES.md` is kept, so line 15 stays) | 2 tests pin it |
| `core/RULES.md`, `core/PRINCIPLES.md` | **Keep** (out of routing scope) | Only remove `RULES.md`'s claims that the PM agent auto-activates (no code does this) | none |
| `install_core.py` | **Update** | Remove retired names from the known-file list and add the guide. **Add a cleanup step, run by both install and update,** that removes exactly the retired files (ORCHESTRATOR, COMMANDS, PERSONAS, MODES, FLAGS, MCP, BUSINESS_PANEL_EXAMPLES, and BUSINESS_SYMBOLS if retired) from `~/.claude/` and `~/.claude/commands/sc/README.md`, **only when the file matches a version IronClaude shipped** (hash list). A file the user has changed, or their own file with the same name, is left alone with a printed notice. Every deletion is reported in the install output. Release notes say the new `~/.claude/CLAUDE.md` routing block arrives through `superclaude update` or `install --force`. | `tests/cli/test_bash_inspection_policy.py:36-44` must keep passing |
| Repo-root `CLAUDE.md` (contributors) | **Update** | Fix the stale command count and MCP list; point to the guide | none |
| `AGENTS.md` | **Reduce to a pointer** to `CLAUDE.md` and the guide | Most of its facts are wrong; no routing | `PROJECT_INDEX.json:125` |
| `KNOWLEDGE.md` | **Keep as is** (out of scope) | Debugging-lessons log read by shipped skills | none |
| `PROJECT_INDEX.md` / `.json` | **Regenerate** with `/sc:index-repo` after the other changes | Generated, stale since March; `reflection.py:320-334` lowers a score if the `.md` is missing | none |

### 3.2 In-session routing (`/sc:help`, `/sc:recommend`) and their copies

| File | Verdict | What changes | References and checks |
|---|---|---|---|
| `commands/help.md` | **Keep, rewrite** | Replace the static 22-row table with a live listing of installed commands and skills (name plus description, grouped), then the guide's level table, then pointers to the guide and `/sc:recommend`. Move the 75-line flag block out (to `docs/user-guide/flags.md`). Include Claude Code built-ins the guide uses (`/code-review`, `/security-review`). | No test pins its content; stay under the 200-line lint warning |
| `commands/recommend.md` | **Keep, update** | Keep the `> Skill sc-recommend` activation line exactly (removing it silently stops the skill installing and fails `tests/unit/test_cli_doctor.py:79`) | `tests/unit/test_cli_install.py:138` pins the command name |
| `skills/sc-recommend/SKILL.md` | **Update** | Phase 0 reads `~/.claude/HOW-WE-WORK.md` (or the source copy in the IronClaude repo) before anything else. Phase 1 lets the guide's levels and hard limit override the "native first" rule. Phase 2 can output an ordered, numbered workflow. Allow the Claude Code built-ins the guide names. When the guide names a safe flag (for example `--monitor 1`, `--no-post-pr`, `--no-promote`), the recommendation must include it. If the guide is found at neither path, say so and fall back to live enumeration only. Make the `uv run superclaude recommend` cache step optional: if the command fails (likely outside the IronClaude repo, UNVERIFIED), skip straight to the normal path. | `tests/agents/test_tavily_tool_parity.py` if `allowed-tools` changes |
| `skills/sc-recommend/refs/delegation-vs-native-heuristics.md` | **Update** | Rewrite line 27 (`/sc:tasklist` becomes `/roadmap` plus `/task-builder`), line 38 (scope rule becomes a pointer to the guide's hard limit), line 61 (drop "skills without a command are rare") | none |
| `skills/sc-recommend/refs/surface-enumeration.md`, `hooks/scripts/sc-recommend-phase0.sh`, `cli/recommend/prompts.py`, `cli/recommend/cache.py`, `dispatch.py` | **Update together** | Search the installed locations (`~/.claude/commands/sc/`, `~/.claude/skills/`, the project's `.claude/`) as well as `src/superclaude/`. The same search list exists in all of these files, so they must change together. Include the guide's hash in the cache fingerprint so editing the guide invalidates old cached answers. | `tests/cli/test_install_hooks.py:96`; `tests/recommend/*` |
| `.claude/cache/sc-recommend-lookup.yaml` | **Clear the 4 rows** | Already ignored at load (fingerprint mismatch); two rows route to the wrong tool and would come back if refilled | `cli/recommend/commands.py:26` default path stays |
| `commands/README.md` | **Stop installing it** (exclude in `install_commands.py:37`) and rewrite its 4-line stale index | It is installed as a fake `/sc:README` slash command | generated knowledge-base line 172 |
| `plugins/superclaude/commands/help.md`, `recommend.md` | **Decision needed (section 7)** | Hand-maintained plugin copy, 17 commands behind, not checked by any sync | `scripts/build_superclaude_plugin.py:75`; `install_commands.py:112-119` fallback |
| Root `commands/sc-help.md`, `sc-recommend.md`, `sc-README.md` | **Cannot retire here** | Regenerated from the upstream SuperClaude repo every 6 hours; any local change is overwritten | Only fixable by changing `scripts/sync_from_framework.py` or the upstream repo (out of scope) |

### 3.3 Human-facing docs (`docs/`, root `README.md`)

None of the retire candidates below is read by code, tests, install, or CI (`04` section 5). The cost of retiring each is the inbound links listed, which must be repointed in the same change.

| File | Verdict | What changes | Inbound links to repoint |
|---|---|---|---|
| `README.md` (root) | **Keep, update** (cannot retire: packaging and CI need it) | Link to the guide; remove Sequential, Magic, Chrome DevTools; remove the `PLANNING.md` and `TASK.md` entries (lines 200-201, files do not exist); fix the already-broken `.dev/` link. Keep broken markdown links at 5 or fewer (`readme-quality-check.yml`). | n/a |
| `docs/getting-started/quick-start.md` | **Replace its body with a short pointer** to the guide and installation, keeping the file path | Every route it gives is superseded or wrong. Keeping the path means its 9 inbound links stay valid. | none while the pointer stays (`installation.md:504,548`; `docs/reference/README.md:44,262`; `agents.md:1024`; `mcp-servers.md:341`; `modes.md:701,715` would need repointing only if the file is later deleted) |
| `docs/getting-started/installation.md` | **Keep, update** | Remove options and commands that do not exist; replace `make dev` with `make install` | n/a |
| `docs/user-guide/commands.md` (1700 lines) | **Keep as per-command reference only** | Remove its routing sections (Visual Map 1033-1082, Key Differences 1086-1095, spawn/task/implement 1099-1218, task vs implement 1222-1290, design vs workflow 1294-1392, Typical Workflows 1505-1644, File Map and future-session notes 57-145 and 1648-1696). Update the table of contents (lines 19, 49 and every entry for a removed section). Correct every per-command entry against current command files and add the missing commands. The index-repo versus Serena comparison (1396-1504) stays exactly as it is (section 7 decision 6); keep its table-of-contents entry. | n/a (10 files link to it; it stays) |
| `docs/user-guide/mcp-servers.md` | **Keep, update links only** | Repoint line 351 (examples-cookbook, retiring) to the guide; line 341 (quick-start) stays valid because quick-start keeps its path | n/a |
| `docs/user-guide/agents.md`, `modes.md`, `flags.md` | **Keep, update** | Remove the routing duplicates (`modes.md` 419-470, `flags.md` 214-250); `flags.md` receives the flag block moved out of `help.md` | n/a |
| `docs/user-guide/session-management.md` | **Keep, update** | Remove the misuse of `/sc:reflect` as a memory check (59-82, 135-157, 241-326) | n/a |
| `docs/user-guide/brainstorm.md` | **Keep, update** | `/sc:task-builder` becomes `/task-builder` (same fix in `commands/brainstorm.md:175`) | n/a |
| `docs/reference/README.md` | **Keep, shrink to an index** of what remains | | n/a |
| `docs/reference/examples-cookbook.md` | **Retire** | Hub for the three collections below; 26 of 38 anchors already dead | `installation.md:515`; `quick-start.md` (retiring); `docs/reference/README.md:25`; `agents.md:1025`; `mcp-servers.md:351`; `modes.md:709,724` |
| `docs/reference/basic-examples.md` | **Retire** | Sends every feature through `/sc:implement`, against the guide's hard limit | `docs/reference/README.md`; `examples-cookbook.md` (retiring) |
| `docs/reference/advanced-workflows.md` | **Retire** | Large-work sequences that bypass task files | same two hubs |
| `docs/reference/advanced-patterns.md` | **Retire** | Near-duplicate of advanced-workflows | `docs/reference/README.md` |
| `docs/reference/integration-patterns.md` | **Retire** | Prompt recipes built on old `/sc:implement` | same two hubs |
| `docs/reference/commands-list.md` | **Retire** | Lists removed commands, misses 16 | `comprehensive-features.md` (retiring) |
| `docs/reference/suggested-commands.md` | **Retire** | Orphan, invalid install flags | none |
| `docs/reference/comprehensive-features.md` | **Retire** | Orphan inventory, wrong counts | none |
| `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | **Retire** (duplicate) | Same content as the `docs/developer-guide/` copy | none live |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` | **Keep, update** | Rewrite "core files are always loaded" and the "register new commands in COMMANDS.md / ORCHESTRATOR.md / FLAGS.md / PERSONAS.md" steps to "add a row to the guide's routing table" | n/a |
| `docs/developer-guide/technical-architecture.md`, `testing-debugging.md`, `contributing-code.md`, `docs/reference/diagnostic-reference.md`, `docs/mcp/mcp-integration-policy.md` | **Keep, update** | Remove references to retired core files | n/a |
| `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md` | **Retire** (or regenerate) | Generated map, wrong on most rows; names a non-existent `sc:recommend-protocol` | `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:592` (link); the same file's lines 316, 461, 468 also name the nonexistent `sc:recommend-protocol` and need correcting |
| `docs/guides/prd-skill-release-guide.md`, `tdd-skill-release-guide.md` | **Keep, update** section 9 (pipeline) to match the guide | | n/a |
| `docs/guides/roadmap-cli-tools-release-guide.md` | **Keep, update**: add a short `/roadmap` vs `/sc:roadmap` vs `superclaude roadmap` box | | n/a |
| `docs/guides/sprint-…`, `reflect-cli-tools-guide.md`, `cli-portify-…`, `suites-guide.md`, `RELEASE-GUIDE-*` | **Keep as is** (tests and eval suites pin them) | | n/a |
| `docs/swarm/wizard-guide.md` | **Keep, update**: `/sc:code-review` becomes `/code-review` | | n/a |

All edits under `docs/` and `src/superclaude/` (including the guide) must pass `tests/docs/test_tavily_doc_alignment.py` (single Tavily version pin, no stale tokens, and no restated default parameters under `docs/`).

## 4. Content the guide must absorb so nothing valuable is lost

| # | Content | Taken from | Where it goes |
|---|---|---|---|
| 1 | Correct `/sc:workflow` and `/sc:implement` paths and behavior on master (plan package under `.dev/tasks/to-do/TASK-WF-…/`, progress file beside it, plan-versus-source check now built in, package moved to done when finished, `--output` removed) | `commands/workflow.md`, `commands/implement.md:63-65` | Guide level 3, 3.3, 3.10, 3.12 |
| 2 | The `/sc:<name>` message must invoke its skill first | Repo-root `CLAUDE.md:9-14` | `core/CLAUDE.md` routing block |
| 3 | Which panel for which document: `/sc:spec-panel` for specs, `/sc:business-panel` for strategy, both for a PRD | `commands.md` 934-944 | Guide 3.6 |
| 4 | `/sc:brainstorm --handoff task` goes straight to a task file | `brainstorm.md` 165-173 | Guide 3.1 step 1 |
| 5 | Swarm lens chooser (goal to lens) | `swarm/wizard-guide.md` 58-66 | Stays there; guide 3.6 links to it |
| 6 | "Does this command change files?" split | `commands.md` 216-249 | Slimmed `commands.md` (one column) |
| 7 | Safe flags per workflow step (for example `--monitor 1`, `--no-post-pr`, `--no-promote`), never presented as shared across commands | The guide's own sections 3 and 5 (nothing taken from `core/FLAGS.md`) | Guide routing table |
| 8 | Which MCP server is used for what | `core/MCP.md`, `core/CLAUDE.md:52-60` | Stays in `core/CLAUDE.md` |
| 9 | Session memory save and load (`/sc:save`, `/sc:load`) | `session-management.md` | Guide 3.12, one row (only if the team uses it; see section 7) |
| 10 | Commands the guide does not yet mention: `/sc:build`, `/sc:git`, `/sc:spawn`, `/sc:index-repo`, `/sc:agent`, `/sc:pm`, `/sc:save`, `/sc:load`, `/sc:cli-eval`, `/sc:post-release`, `/sc:review-translation`, `/sc:validate-tests`, `/sc:init-lite` | Command inventory (`01` section 2) | Guide gets a short "Other commands" table so `/sc:help` and `/sc:recommend` can route everything |
| 11 | Machine-readable routing table (intent, ordered steps, mandatory safe flags) | New | End of the guide, read by help and recommend |

## 5. Order of work

0. **Get decisions:** you rule on every section 6 removal and every section 7 decision; the answers are recorded in the task file before any edit.
1. **Correct and extend the guide** (section 4) and place it at `src/superclaude/core/HOW-WE-WORK.md`; add the pointer page `docs/user-guide/how-we-work.md`.
2. **Update `core/CLAUDE.md`** as described in 3.1 (routing block, removals, contributor sections moved to the repo-root `CLAUDE.md`).
3. **Rewrite `/sc:help`** and **update `/sc:recommend`** and its supporting files, hook, and cache; copy both into the plugin tree if decision 1 keeps it.
4. **Repoint every inbound reference** listed in section 3, then **retire** the approved files (src and plugin copies together).
5. **Update `install_core.py` and `install_commands.py`** (known files, the new guide, the guarded cleanup step, stop installing `commands/README.md`).
6. **Update every remaining "Keep, update" row** in 3.1 and 3.3: repo-root `CLAUDE.md`, `AGENTS.md`, `RESEARCH_CONFIG.md`, `RULES.md`, `skills/sc-task-protocol/SKILL.md`, `commands/brainstorm.md:175`, `commands.md` slim-down, `mcp-servers.md`, `agents.md`, `modes.md`, `flags.md`, `session-management.md`, `brainstorm.md`, `installation.md`, `docs/reference/README.md`, release guides, developer guide and its sibling docs, `swarm/wizard-guide.md`, `visual-architecture-summary.md`, and `README.md`.
7. **Add tests:** installer cleanup (deletes shipped versions, leaves changed or user-owned files), the guide is installed and listed, `core/CLAUDE.md` never `@`-imports the guide, and (if the plugin tree is kept) the src and plugin copies of `help.md` and `recommend.md` match, like the existing `tests/commands/test_workflow_command.py:86-87`.
8. **Regenerate `PROJECT_INDEX.md`/`.json`.**
9. **Verify:** full pytest, `make sync-dev` then `make verify-sync`, `make lint-architecture`, the README link check, and a live run of `/sc:help` and `/sc:recommend` on each of the guide's workflows from a non-IronClaude project.
10. **Ship** as a pull request to IronClaude through `/sc:pr-submit`.

This touches well over five files across code, skills, tests, and docs, so per project rule it runs as a task file: `/task-builder` with this plan as the spec, then `/task`.

## 6. Proposed removals (each needs your yes or no)

Retire whole files:
- **Remove `src/superclaude/core/ORCHESTRATOR.md`:** not loaded since March; its routing points at removed tools; the live tier rules are in `commands/task.md`.
- **Remove `src/superclaude/core/COMMANDS.md`:** not loaded; covers 18 of 43 commands and is wrong in 7+ places; replaced by the guide's routing table.
- **Remove `src/superclaude/core/PERSONAS.md`:** not loaded; persona flags are used by no command.
- **Remove `src/superclaude/core/MODES.md`:** not loaded; references removed MCPs and commands.
- **Remove `src/superclaude/core/FLAGS.md`:** not loaded; drives nothing; flags are defined per command.
- **Remove `src/superclaude/core/MCP.md`** (after repointing one skill line): not loaded; `core/CLAUDE.md` already has a better MCP table.
- **Remove `src/superclaude/core/BUSINESS_PANEL_EXAMPLES.md`:** orphaned; examples use flags that do not exist.
- **Remove `plugins/superclaude/core/FLAGS.md` and `plugins/superclaude/core/BUSINESS_PANEL_EXAMPLES.md`:** drifted copies that nothing reads.
- **Replace the body of `docs/getting-started/quick-start.md` with a pointer** (path kept): every route in it is superseded or wrong.
- **Remove `docs/reference/examples-cookbook.md`:** hub for retiring collections; most anchors already dead.
- **Remove `docs/reference/basic-examples.md`:** contradicts the guide's hard limit.
- **Remove `docs/reference/advanced-workflows.md`:** large-work sequences that bypass task files.
- **Remove `docs/reference/advanced-patterns.md`:** near-duplicate of advanced-workflows.
- **Remove `docs/reference/integration-patterns.md`:** recipes built on old `/sc:implement`.
- **Remove `docs/reference/commands-list.md`:** lists removed commands, misses 16.
- **Remove `docs/reference/suggested-commands.md`:** orphan with invalid install flags.
- **Remove `docs/reference/comprehensive-features.md`:** orphan with wrong counts.
- **Remove `docs/guides/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`:** duplicate of the `docs/developer-guide/` copy.
- **Remove `docs/generated/contributor-knowledge-base/commands-skills-cross-reference.md`:** generated map, wrong on most rows.

Remove sections inside kept files:
- **Remove from `docs/user-guide/commands.md`** the routing sections listed in 3.3: they conflict with the guide.
- **Remove from `docs/user-guide/modes.md` 419-470 and `flags.md` 214-250:** routing duplicates with stale commands.
- **Remove from `docs/user-guide/session-management.md`** the `/sc:reflect` memory-check usage: wrong tool, flags that do not exist.
- **Remove from `commands/help.md`** the static command table (30-53) and the flag block (55-129): replaced by the live listing; flags move to `flags.md`.
- **Remove from `core/CLAUDE.md`** the persona auto-activation table, the "wave strategies" claim, and the `KNOWLEDGE.md`, `PLANNING.md`, `TASK.md` pointers: nothing implements auto-activation or waves, and those files are repo-only or do not exist. The contributor-only sections move to the repo-root `CLAUDE.md` rather than being deleted.
- **Remove from `README.md`** the `PLANNING.md` and `TASK.md` entries: those files do not exist.
- **Remove the 4 cached rows** in `.claude/cache/sc-recommend-lookup.yaml`: already ignored; two route to the wrong tool.
- **Rewrite lines 27, 38, 61** of `refs/delegation-vs-native-heuristics.md`: they contradict the guide.
- **Stop installing `commands/README.md`:** it appears to users as a fake `/sc:README` command.

## 7. Decisions only you can make

1. **The hand-maintained plugin copy (`plugins/superclaude/`).** It is 17 commands behind and nothing checks it, and plugin installs never receive `core/` files, so plugin users would not get the guide. Recommended: keep it, copy the help and recommend changes into it, ship the guide inside the `sc-recommend` skill's `refs/` folder for plugin users, and add a test that the copies match (the repo already does this for `workflow.md` and `implement.md`). Alternative: retire the plugin tree (larger decision, affects `make build-plugin`).
   - **DECIDED 2026-10-12: Keep.** Copy the new help and recommend into the plugin tree, ship the guide in `skills/sc-recommend/refs/`, and extend `tests/skills/test_task_workspace_smoke.py:40` to cover `help.md` and `recommend.md`. The other 17 missing plugin commands stay out of scope.
2. **How `/sc:help` lists commands.** Recommended: read the installed files live each time (never drifts, costs a few tool calls). Alternative: a generated static list kept current by a Makefile target and a test.
   - **DECIDED 2026-10-12: Read live.** `/sc:help` lists `~/.claude/commands/sc/`, `~/.claude/skills/`, and the project's `.claude/` at run time; no hand-kept or generated table.
3. **Session memory (`/sc:save`, `/sc:load`).** Does the team use them? If yes, they get a row in the guide's resume table; if no, the guide leaves them in "Other commands" only.
   - **DECIDED 2026-10-12: Not used for resuming.** `/sc:save` and `/sc:load` go in "Other commands" only, and the guide never routes to them. The guide's resume table names exactly two ways to resume: (a) ccsession (tag a session with the `ccsession-tag` skill, reopen it with `ccsession <name>` from the shell; shipped via `cli/install_ccsession.py`), and (b) the work's on-disk state: the task file for `/task`, and the progress file beside the plan for `/sc:implement`. Section 4 row 9 (`session-management.md` save/load content) is therefore not absorbed as a routing row.
4. **Project-rule wording in the guide.** The guide currently lets "more than 5 edits or more than one source file" use the simple checked plan (level 3), not only a task file. Keep that, or require a task file as IC-Harness's own rule does?
   - **DECIDED 2026-10-12: Keep.** The hard limit stays as written in `IRONCLAUDE-NEW-USER-GUIDE.md:20`: over 5 edits or more than one source file needs a written plan; level 3 (`/sc:workflow` + `/sc:implement`) for a few files with clear scope, level 4 (`/task-builder` + `/task`) for anything larger, longer, or riskier. IC-Harness's stricter task-file-only rule is not adopted in the IronClaude guide.
5. **`core/BUSINESS_SYMBOLS.md`.** `/sc:business-panel --structured` depends on it. Recommended: keep it as is (it is out of routing scope). Alternative: move only the symbols `--structured` needs into the command, keeping it under 200 lines, and retire the file and its plugin copy.
   - **DECIDED 2026-10-12: Leave alone, no action and no follow-up.** Correction to the plan's premise: nothing actually reads the file (`commands/business-panel.md:78` never names it; no skill, agent, or test refers to it). `BUSINESS_SYMBOLS.md` and its plugin copy stay untouched and stay in `install_core.py:142`. The only inbound reference, `docs/reference/comprehensive-features.md:102`, disappears when that file is retired.
6. **The index-repo versus Serena comparison** (`docs/user-guide/commands.md` 1396-1501). Recommended: move it to `docs/user-guide/mcp-servers.md`. Alternatives: keep it in `commands.md`, or drop it.
   - **DECIDED 2026-10-12: Leave alone, out of scope.** The section (`docs/user-guide/commands.md:1396-1504`) is not moved, edited, or dropped. Only the surrounding routing sections listed in section 3.3 are removed.

## 8. Not changed by this plan

`BASH_INSPECTION_POLICY.md`, `RESEARCH_CONFIG.md` (small fix only), `RULES.md`, `PRINCIPLES.md`, `KNOWLEDGE.md`, root `commands/sc-*.md` (generated from upstream), the sprint, reflect, cli-portify, and suites guides, `mcp-installation.md`, `memory-system.md`, `eval-pipeline.md`, `freshness-hooks.md`, and the `src/superclaude/rules/` folder (not audited for routing; a follow-up).

## 9. Later user decisions

- **DECIDED 2026-10-13: No installer cleanup.** Nothing is deleted from existing users' `~/.claude/` (the cleanup step in the 3.1 `install_core.py` row, section 5 steps 5 and 7, and the related release-note text are dropped). The installers only stop shipping the retired files and `commands/README.md`.
- **DECIDED 2026-10-13: No business-panel changes.** The `/sc:business-panel` entry in `docs/user-guide/commands.md` and the guide's business-panel row are left as they are. `BUSINESS_PANEL_EXAMPLES.md` and its plugin copy are not retired.
