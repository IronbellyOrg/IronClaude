# QA Report: Adversarial Review of the Routing Consolidation Plan

**Topic:** IronClaude "what to use when" consolidation plan
**Target:** `05-CONSOLIDATION-PLAN.md` (this folder). Not edited.
**Evidence checked:** `01-agent-facing-core.md`, `02-human-docs.md`, `03-help-recommend.md`, `04-machinery-and-references.md`
**Source truth:** `/tmp/ic-master` (SNAPSHOT.txt: origin/master `ee1c1787`, 2026-10-11); commit history checked in `/Users/cmerritt/GFxAI/IronClaude`
**Date:** 2026-10-12
**Phase:** report-validation (plan review, report only, no fixes applied)
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

The plan's core direction is sound and most of its file:line claims check out against the source. It fails because of 13 concrete issues: two documents marked "not changed" or "no inbound links" actually hold links to retiring files, the installer cleanup step is under-specified and misses a stale file, one "orphaned" core file is still used by a command, the shared-flags list contradicts the research and the live command files, several research-flagged fixes were dropped, and the order of work is missing steps.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Retiring core files are not `@`-imported | PASS | Only `@` import in any core file or root CLAUDE.md/AGENTS.md is `src/superclaude/core/CLAUDE.md:3` `@BASH_INSPECTION_POLICY.md` (grep). Import removal commit `4b19eb08` (2026-03-16) confirmed with `git show` in the IronClaude repo. |
| 2 | Retiring core files are not read by hook, test, or code | PASS | Grep of the snapshot (excluding `.dev`): only `install_core.py:141-149` known list, `sc-task-protocol/SKILL.md:407-408`, `recommend/prompts.py:16` comment, test docstrings `test_critical_corrections.py:7,61`, `RESEARCH_CONFIG.md:133`, docs, PROJECT_INDEX. Only hook reading a core file is `freshness-subagent-start.sh:7` (BASH policy). |
| 3 | `install_core` globs `core/*.md` | PASS | `install_core.py:39` `sorted(core_source.glob("*.md"))`, copy at `:56`. 13 `.md` files present in `core/` (ls). |
| 4 | Guide in `core/` is not auto-loaded | PASS | No loader of `~/.claude/*.md` exists in hooks or CLI (grep of `hooks/scripts`, `cli/*.py`); `install_user_setup.py:5-6,110` only handles `~/.claude/rules/` and excludes it via `claudeMdExcludes`. Residual risk: an author writing `@HOW-WE-WORK.md` into core/CLAUDE.md (issue 14). |
| 5 | Installer cleanup step | FAIL | Issue 3. |
| 6 | recommend.md activation coupling | PASS | `recommend.md:56` `> Skill sc-recommend`; `install_skills.py:30-32` regex; `test_cli_doctor.py:79`; `test_cli_install.py:138` all match plan line 62. |
| 7 | help.md ranges and counts | PASS | 149 lines; table rows at 30-53 (22 `/sc:` rows); flag block starts line 55, ends before Boundaries at ~129; 43 commands, 36 skills. |
| 8 | commands/README.md install quirk | PARTIAL | `install_commands.py:37` globs every `*.md` (README included); README index is 4 lines (7-10). Cleanup of already-installed copies missing (issue 3). |
| 9 | README.md constraints | PARTIAL | `readme-quality-check.yml:113-117,145,255` confirm the 5-broken-link ceiling. Dropped PLANNING.md/TASK.md fix (issue 7). |
| 10 | Docs retirements and inbound links | FAIL | Issues 1, 2, 11. Other inbound lists (quick-start, examples-cookbook, basic-examples, advanced-*, integration-patterns, commands-list, suggested-commands, comprehensive-features, guides Developer-Guide copy) match grep. |
| 11 | Research items carried into plan | FAIL | Issues 4, 5, 6, 7, 8, 9, 10, 12. |
| 12 | Internal consistency and section 5 order | FAIL | Issues 1, 8, 11, 13. |
| 13 | Section 1 factual claims | PASS | `workflow.md:12` and `implement.md:63-65` match item 6; 13 core files; 22 of 43 commands in help. |

## Issues Found

### Issue 1 (IMPORTANT): `mcp-servers.md` is marked "not changed" but links to two retiring files

- **Plan text:** line 177, "`mcp-servers.md`, `mcp-installation.md`, `memory-system.md` ... (Not changed by this plan)". Lines 78 and 85 list `mcp-servers.md:341` and `mcp-servers.md:351` as inbound links that must be repointed.
- **Evidence:** `/tmp/ic-master/docs/user-guide/mcp-servers.md:341` (quick-start.md) and `:351` (examples-cookbook.md), found by grep.
- **Corrected text:** remove `mcp-servers.md` from section 8 and add a 3.3 row: "`docs/user-guide/mcp-servers.md` | **Keep, update links only** | Repoint line 341 (quick-start) and line 351 (examples-cookbook) to the guide | n/a".

### Issue 2 (IMPORTANT): wrong "none" inbound for the generated cross-reference

- **Plan text:** line 96, "`commands-skills-cross-reference.md` | **Retire** (or regenerate) | ... | none".
- **Evidence:** `/tmp/ic-master/docs/generated/contributor-knowledge-base/visual-architecture-summary.md:592` links `./commands-skills-cross-reference.md`.
- **Corrected text:** "Inbound links to repoint: `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:592` (also `:316,461,468` mention `/sc:recommend` per `04` section 4.2)".

### Issue 3 (IMPORTANT): installer cleanup step is under-specified and misses a stale file

- **Plan text:** line 51, "**add a step that deletes retired files from `~/.claude/`**"; line 67, "**Stop installing it** (exclude in `install_commands.py:37`)"; line 25, core/CLAUDE.md reaches "Every agent, every session".
- **Evidence:**
  - `install_commands.py:37,57` already copied `README.md` to `~/.claude/commands/sc/README.md` for every existing user; excluding it only helps new installs (`04` rule R1). The plan's cleanup targets `~/.claude/` core files only.
  - `install_core.py:50-52` skips any existing destination file when `force` is false, so a plain `superclaude install` never replaces an existing `~/.claude/CLAUDE.md`; only `update` (`main.py:307-310`, force=True) or `install --force` delivers the new routing block. `01` line 26 also flags that `update` overwrites the user's own global CLAUDE.md.
  - `FLAGS.md`, `MODES.md`, `COMMANDS.md` are generic names a user could own in `~/.claude/`; `04` section 6 row 4 says whether user CLAUDE.md files still `@`-import them is UNVERIFIED.
- **Corrected text:** "Add a cleanup step, called from both install and update, that removes exactly this named list from `~/.claude/` (ORCHESTRATOR, COMMANDS, PERSONAS, MODES, FLAGS, MCP, BUSINESS_PANEL_EXAMPLES, BUSINESS_SYMBOLS) and `~/.claude/commands/sc/README.md`, only when the file matches a previously shipped version (hash list) and otherwise leaves it and prints a notice; report every deletion in the install output; add tests for both cases. Note in the release notes that the routing block in `~/.claude/CLAUDE.md` arrives through `superclaude update` or `install --force`."

### Issue 4 (IMPORTANT): BUSINESS_SYMBOLS is not orphaned, the merge breaks a size limit, and plugin copies are missed

- **Plan text:** line 47, "**Merge into `commands/business-panel.md`** as a file it reads, or retire | Orphaned, not routing"; line 145 removes only `plugins/superclaude/core/FLAGS.md`.
- **Evidence:**
  - `/tmp/ic-master/src/superclaude/commands/business-panel.md:78` "`--structured` - Use symbol system for efficiency". The symbol system is defined only in `core/BUSINESS_SYMBOLS.md` (225 lines). Retiring it leaves `--structured` undefined.
  - `business-panel.md` is 129 lines; merging 225 lines gives about 354, over the `make lint-architecture` 200-line warning (`Makefile:398-410`, `04` section 1.6).
  - `plugins/superclaude/core/BUSINESS_PANEL_EXAMPLES.md` and `plugins/superclaude/core/BUSINESS_SYMBOLS.md` exist (ls) and are shipped in the wheel via `plugins/**` (`pyproject.toml:79-88`).
  - "as a file it reads" is unclear: a command has no folder of its own to read from, and the core copy would be deleted by the cleanup step.
- **Corrected text:** "`core/BUSINESS_SYMBOLS.md` | **Decision needed** | Used by `business-panel.md:78` (`--structured`). Either keep it as is, or move only the symbols `--structured` needs into `business-panel.md` while staying under 200 lines, then retire. Retire `plugins/superclaude/core/BUSINESS_SYMBOLS.md` and `BUSINESS_PANEL_EXAMPLES.md` together with the src copies." Add both plugin copies to section 6.

### Issue 5 (IMPORTANT): the shared-flags list contradicts the research and the live commands

- **Plan text:** line 44 "The few real shared flags (`--focus`, `--scope`, `--depth`) go into the guide"; same list at lines 114 and 141 ("the 3 real shared flags").
- **Evidence:**
  - `01-agent-facing-core.md:196,204` names `--focus`, `--scope`, `--validate`, `--no-mcp`, and the `--think*` trio; `--depth` is not on it.
  - `--depth` appears in 13 command files with per-command values (grep), and `/sc:workflow` bans `--depth shallow|normal` and `--validate` (`commands/workflow.md:42`, `E-LEGACY`). `--scope` is used by only `reflect.md` and `troubleshoot.md` (plus help.md).
- **Corrected text:** "FLAGS.md: **Retire.** Flags are defined per command; the guide's routing table lists the safe flags per workflow step (for example `--monitor 1`, `--no-post-pr`) and never presents a flag as shared across commands. No content moves from FLAGS.md." Update section 4 row 7 and section 6 line 141 to match.

### Issue 6 (IMPORTANT): core/CLAUDE.md update drops fixes the research required

- **Plan text:** line 38, "Remove the stale persona auto-activation table and the `KNOWLEDGE.md` pointer"; line 45 "`core/CLAUDE.md:52-60` already has a better MCP table"; line 115 "Stays in `core/CLAUDE.md`".
- **Evidence:** `/tmp/ic-master/src/superclaude/core/CLAUDE.md:91-92` point to `PLANNING.md` and `TASK.md`, which do not exist in the snapshot (ls failed); `:94-95` give repo paths `src/superclaude/core/RULES.md` and `PRINCIPLES.md` that do not exist in a user project; `:16-50` describe IronClaude's own source tree to every user; `:102` claims "wave strategies live in the skill files" (false per `01:81`). `01:90` verdict lists fixes (b) MCP flags marked advisory, (c) move contributor sections to repo-root CLAUDE.md, (d) fix Key Docs paths.
- **Corrected text:** "core/CLAUDE.md | Update | Add the routing block. Remove the persona table, and the Key Docs entries for KNOWLEDGE.md, PLANNING.md, TASK.md; repoint RULES.md and PRINCIPLES.md to `~/.claude/RULES.md` and `~/.claude/PRINCIPLES.md`. Move Project Structure, Dev Commands, and Component Sync (`:16-50`) to the repo-root CLAUDE.md. In the MCP table mark the flag column as advisory. Remove the 'wave strategies' claim at `:102`. Keep `@BASH_INSPECTION_POLICY.md`."

### Issue 7 (MINOR): README row drops the PLANNING.md and TASK.md fix

- **Plan text:** line 77, "remove Sequential, Magic, Chrome DevTools; fix the already-broken `.dev/` link".
- **Evidence:** `/tmp/ic-master/README.md:200-201` list `PLANNING.md` and `TASK.md`, which do not exist; `02-human-docs.md` summary row 1 requires the fix.
- **Corrected text:** append "remove the `PLANNING.md` and `TASK.md` entries (lines 200-201)".

### Issue 8 (MINOR): RESEARCH_CONFIG row calls RULES.md retired

- **Plan text:** line 49, "drop pointers to retired `MCP.md` and `RULES.md`".
- **Evidence:** RULES.md is kept (plan lines 50, 177). `/tmp/ic-master/src/superclaude/core/RESEARCH_CONFIG.md:15` "See RULES.md §Planning Efficiency" stays valid; only `:133` points at MCP.md.
- **Corrected text:** "Fix the Tavily version mismatch; drop the MCP.md pointer at line 133."

### Issue 9 (MINOR): sc-task-protocol pointer edit is incomplete

- **Plan text:** line 40 "`skills/sc-task-protocol/SKILL.md:408` (repoint to `commands/task.md`)"; line 45 "`skills/sc-task-protocol/SKILL.md:407`" with no target.
- **Evidence:** `/tmp/ic-master/src/superclaude/skills/sc-task-protocol/SKILL.md:403-406` cite `config/tier-keywords.yaml`, `config/verification-routing.yaml`, `config/tier-acceptance-criteria.yaml`, which do not exist in the skill folder (`01:105,431`). Line 407 "Circuit breakers: See MCP.md" gets no replacement.
- **Corrected text:** "Rewrite `SKILL.md:403-408`: point routing at `commands/task.md:71-93`, drop the three missing config files, and replace 'Circuit breakers: See MCP.md' with a pointer to the MCP table in `~/.claude/CLAUDE.md` (or delete it)."

### Issue 10 (IMPORTANT): the guide is unreachable for plugin installs and recommend's hot path may fail outside IronClaude

- **Plan text:** line 24, "copies it to `~/.claude/HOW-WE-WORK.md`, a fixed path that agents, `/sc:help`, and `/sc:recommend` can read from any project"; line 63 "(or the source copy in the IronClaude repo)".
- **Evidence:**
  - Plugin builds copy only agents, commands, hooks, scripts, skills (`scripts/build_superclaude_plugin.py:75`, `04` section 1.7); `core/` is never built, so plugin users have no `~/.claude/HOW-WE-WORK.md`. The fallback source copy exists only inside the IronClaude repo.
  - `skills/sc-recommend/SKILL.md:48,53,220` run `uv run superclaude recommend ...`; `03:195,311` flag that this likely fails in a consumer project (UNVERIFIED). The plan's "any project" goal does not address it.
- **Corrected text:** add to 3.2 sc-recommend row: "If the guide is not found at either path, say so and fall back to live enumeration only. Make the `uv run superclaude recommend` hot path optional: on command failure, skip to the cold path." Add to section 7 decision 1: "If the plugin tree is kept, decide how plugin users get the guide (ship it in a skill `refs/` folder, or add `core/HOW-WE-WORK.md` to the plugin build)."

### Issue 11 (MINOR): "retire" versus "replace with a pointer" is ambiguous, and one page is described as existing when it does not

- **Plan text:** line 78 "**Retire, replace with a short pointer**" plus 9 inbound links to repoint; line 146 "Remove ... (replace with a pointer)"; line 30 "`docs/user-guide/how-we-work.md` becomes a one-paragraph pointer".
- **Evidence:** If a pointer stays at `docs/getting-started/quick-start.md`, the 9 inbound links stay valid and need no edit; if the file is deleted they all break. `/tmp/ic-master/docs/user-guide/` has no `how-we-work.md` (ls), so it does not "become" anything; it is new (section 5 step 1 correctly says "add").
- **Corrected text:** line 78: "**Replace body with a short pointer** (keep the path so its 9 inbound links stay valid; repoint them only if the file is later deleted)". Line 30: "Add `docs/user-guide/how-we-work.md` as a one-paragraph pointer".

### Issue 12 (MINOR): commands.md slim-down misses its table of contents and one research decision

- **Plan text:** line 80 removal list for `docs/user-guide/commands.md`.
- **Evidence:** `/tmp/ic-master/docs/user-guide/commands.md:19,49` link the `#-visual-map-when-to-use-what` anchor of the section being removed. `02-human-docs.md` content row 8 (index-repo versus Serena, `commands.md` 1396-1501, "user decides") appears nowhere in the plan or section 7.
- **Corrected text:** add "Update the table of contents (lines 19, 49 and any other entries for removed sections)." Add section 7 item: "Keep the index-repo versus Serena comparison (`commands.md` 1396-1501), move it to `mcp-servers.md`, or drop it?"

### Issue 13 (IMPORTANT): section 5 order of work is missing steps

- **Plan text:** lines 122-130.
- **Gaps found:**
  1. No step gates the work on the user's answers. Section 7 decision 4 changes the guide written in step 1; decision 1 changes the scope of step 3 (plugin copies); decision 2 changes the help design; section 6 removals must be adjudicated before step 4.
  2. Several 3.1 and 3.3 rows belong to no step: repo-root `CLAUDE.md` (line 52), `AGENTS.md` (line 53), `RESEARCH_CONFIG.md` (line 49), `RULES.md` (line 50), `commands/brainstorm.md:175` (line 83), and the plugin `core/` removals (line 145). Step 6 names only a few kept docs.
  3. No step adds tests, yet the plan creates new behavior: installer cleanup, `HOW-WE-WORK.md` in `known_core` and installed, no `@HOW-WE-WORK` import in core/CLAUDE.md, and (if decision 1 keeps the plugin) a src-versus-plugins equality test for help.md and recommend.md like `tests/commands/test_workflow_command.py:86-87`.
  4. Step 8 omits `make sync-dev` before `make verify-sync`, although `help.md`, `recommend.md`, and `brainstorm.md` change (`Makefile:228-251` byte-compares src against `.claude/commands/sc/`). Its clause "after deleting stale local mirrors" does not apply: no `src/superclaude/commands/*.md` is retired, and README is skipped by sync-dev (`Makefile:134`).
  5. Line 102 applies the Tavily guard to `docs/` only, but the guide lives in `src/superclaude/core/`, which `tests/docs/test_tavily_doc_alignment.py:13` also scans (stale token and single version pin rules apply).
- **Corrected text:** insert "0. **Get decisions:** the user rules on every section 6 removal and every section 7 decision; record them in the task file." Expand step 6 to "Update every 'Keep, update' row in 3.1 and 3.3 not handled earlier (repo-root CLAUDE.md, AGENTS.md, RESEARCH_CONFIG.md, RULES.md, commands/brainstorm.md, mcp-servers.md links, and the docs list)." Add "7a. **Add tests** for installer cleanup, guide install and listing, no `@` import of the guide, and plugin parity if kept." Change step 8 to "`make sync-dev` then `make verify-sync`". Change line 102 to "All edits under `docs/` and `src/superclaude/` must pass `tests/docs/test_tavily_doc_alignment.py`."

### Issue 14 (note on target design, folded into issue 13 item 3)

The design is sound: `install_core.py:39` globs `core/*.md`, so `HOW-WE-WORK.md` lands at `~/.claude/HOW-WE-WORK.md`; nothing auto-loads it (only `CLAUDE.md` plus its single `@` import load, and no hook reads it). The one way it could load every session is if the new routing block writes it as an `@` import. Line 25 should say so explicitly: "Refer to the guide as a plain path in backticks; never `@HOW-WE-WORK.md`." Back this with the test in issue 13.

## Summary

- Checks passed: 7 of 13 (2 partial, 4 failed)
- Issues: 14 (IMPORTANT: 8, MINOR: 5, note: 1)
- Issues fixed in place: 0 (report only, as instructed)

## Confidence

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (for the checks run; verdict is FAIL on findings, not on coverage)
- **Tool engagement:** Read: 1 | Grep: 0 (grep run through Bash) | Glob: 0 | Bash: 22 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- Not verified, and not needed for the verdict: whether upstream SuperClaude still ships help/recommend/README (drives the root `commands/sc-*.md` rule); whether `uv run superclaude recommend` works in a consumer project (carried as UNVERIFIED from `03`).

## Recommendations

Apply the corrected text for issues 1 to 13 to `05-CONSOLIDATION-PLAN.md`, then re-run this QA as fix cycle 1 before the plan goes to `/task-builder`.

## QA Complete
