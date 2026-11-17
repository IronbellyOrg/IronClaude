# Dependency map: remove `/sc:save` and `/sc:load` (6.0.0, PR 6)

Measured on 2026-11-17 at `783832f11` (branch `clayphi/v6-save-load`, same commit as `origin/integration`). Method: `git grep` over tracked files for `sc:save`, `sc:load`, `sc-save`, `sc-load`, `sc/save`, `sc/load`, `commands/(save|load)`, `save.md`, `load.md`, quoted bare `"save"`/`"load"` names and "session lifecycle / session pattern" wording, then a read of every hit. Historical records are excluded by the issue 571 rule (`docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries) and so are tracked `.dev/**` working records. The code-graph index was not usable in this session (the codegraph tools disconnected), so the search is `git grep` plus Read. Nothing in `src/superclaude/cli/`, hooks, `Makefile`, `pyproject.toml`, `.github/` or the installer names either command (checked), so there is no code to change, only files and text.

What stays: the `sc-crash-recovery` skill, the `<project>/.superclaude/memory/` folder convention (still written by `/sc:pm`, the PM agent, `sc-pm-protocol`, `sc-task-protocol`, `sc-reflect-protocol`, `sc-validate-roadmap-protocol`), and `ccsession`. No kept skill or command needs the removed commands to work (see section E).

## A. Delete (6 files, matches the plan's count)

| Path | Note |
|---|---|
| `src/superclaude/commands/save.md`, `src/superclaude/commands/load.md` | Source of truth. |
| `plugins/superclaude/commands/save.md`, `plugins/superclaude/commands/load.md` | Plugin mirror. |
| `commands/sc-save.md`, `commands/sc-load.md` | Root namespaced copies (they even read `/sc:sc:sc:save`). |

Also remove the gitignored dev copies `.claude/commands/sc/save.md` and `.claude/commands/sc/load.md` by hand: `make sync-dev` copies but never prunes, and `make verify-sync` and the parity tests would otherwise see them. They are never staged.

## B. Edit outside the deleted files (18 files; the plan counted 19: 2 tests, 11 docs, 7 other)

Re-measured (the roadmap skill also had a sixth clause at line 234, and the architecture reference a third count at line 196, both found while editing): 5 test files (the plan said 2), 11 docs, 7 other primitives. The plan missed `tests/unit/test_cli_install.py`, `tests/recommend/*` and `tests/skills/test_worker_contract.py` and counted `plugins/` copies with their source. Totals: 23 edited files, 2 of them byte-copies (`plugins/.../HOW-WE-WORK.md`, `plugins/.../RULES.md`). Confirmed at the end by `git diff HEAD --stat`: 29 files changed, 6 deleted and 23 edited.

### B1. Primitives and core files (7)

| # | Reference | Change |
|---|---|---|
| 1 | `src/superclaude/core/HOW-WE-WORK.md:238` | Delete the paragraph "`/sc:save` and `/sc:load` store and load project memory ...". Keep the next sentences about other command-owned continuations (reword to start "Command-owned continuations keep their own supplied pipeline ..."). |
| 2 | `src/superclaude/core/HOW-WE-WORK.md:331` and `:333` | Delete the `/sc:load` and `/sc:save` rows of the Other commands table. |
| 3 | `src/superclaude/core/HOW-WE-WORK.md:375` | Resume row: drop "`/sc:save` and `/sc:load` are memory, not executor resume;". |
| 4 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Byte copy of #1-#3 (`cmp` identical today; the test `tests/commands/test_routing_plugin_parity.py` and the repo rule require it). |
| 5 | `src/superclaude/core/RULES.md:49-50` (+ `plugins/superclaude/core/RULES.md`, identical) | Delete "Session Lifecycle ... /sc:load" and "Session Pattern ... /sc:save" lines; keep "Checkpoint Triggers". |
| 6 | `src/superclaude/core/WORKER-CONTRACT.md:204` | The brief-layout example `Command: /sc:load ...` becomes `Command: /sc:design ...`, then `Command: /sc:workflow ...` (both are converted commands that `tests/issue_pipeline/test_brief.py` already builds in that order). |
| 7 | `src/superclaude/skills/sc-crash-recovery/SKILL.md:157` | Delete the "does not replace `/sc:load` ..." bullet. The skill has no other mention (`refs/`, `scripts/` checked). |
| 8 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:190,215,272,297,316,326,420` | Delete each "Trigger `sc:save` with ..." clause and completion step 3 (renumber step 4), and reword line 420 to "sc:roadmap persists session state at each wave boundary ...". The skill keeps its own `<output_dir>/.session-memory.md` persistence and resume protocol, so it works without `sc:save`. |

`src/superclaude/core/CLAUDE.md` names neither command (the "level table" copy is not touched by these rows), so it needs no edit. Counted in the plan's "7 other": #1-#8 above group to HOW-WE-WORK (2 copies), RULES (2 copies), WORKER-CONTRACT, crash-recovery, roadmap.

### B2. Tests (5)

| # | Reference | Change |
|---|---|---|
| 9 | `tests/core/test_how_we_work_routing_table.py:38-39` and `:1077-1080` | Remove `"sc:save"`, `"sc:load"` from `_OTHER_COMMANDS`; delete the four asserts in `test_other_operations_preserve_requested_authority_and_owned_state` that pinned the removed rows' wording (`needs no MCP server`, `.superclaude/memory/`, `writes memory; not durable task execution state`, `Not executor resume`). Found when the test failed after the guide edit. |
| 10 | `tests/recommend/fixtures/routing_refresh_cases.json:565-587` (case S25, with its load repeat) | Delete case S25 (as S27 was retired for `/sc:spawn`). The frozen command-disposition rows at `:754` and `:764` stay (frozen 47-command record). |
| 11 | `tests/recommend/test_routing_refresh.py` | Case id list skips 25 and 27; `_POST_REFRESH_REMOVALS` gains `save` and `load`; docstring notes S25 is retired; the `formatting_only` list at `:666-667` stays (it checks the frozen record). |
| 12 | `tests/skills/test_worker_contract.py:1429-1434` and `:1447-1449` | Delete `test_load_usage_line_declares_checkpoint_and_load_is_not_converted` (reads `load.md`); drop `"load"` from `NOT_CONVERTED_IN_P1`. The synthetic `cmds / "load.md"` at `:1602-1607` writes a temp file and does not need the real command, but is changed to another unconverted name (`pm`) so no `load` is left. |
| 13 | `tests/unit/test_cli_install.py:116,118,404` | Remove `load.md` and `save.md` from both expected command lists. |

### B3. Docs (11)

| # | Reference | Change |
|---|---|---|
| 14 | `README.md:100` | Session memory bullet: say the folder is read and written by `/sc:pm` and the PM agent. |
| 15 | `docs/user-guide/commands.md:110-111` (table), `:411-428` (load section), `:654-666` (save section) | Delete both rows and both sections. Line 428 of the PM section ("Loads/Saves project memory ... not a way to resume") stays: those lines describe `/sc:pm`. |
| 16 | `docs/user-guide/session-management.md` (27 lines) | Remove the two command sections and every `/sc:save`/`/sc:load` example and instruction; keep the memory-folder description, the resume section and the context-envelope section. Memory is now written by `/sc:pm` and the PM agent. The "Upgrading from Serena memory" section keeps the `cp` recipe but drops the end-of-fallback text. |
| 17 | `docs/developer-guide/session-memory.md` (10 lines) | Drop the save and load rows, subsections and the "Legacy fallback" section (it lived only in `load.md`), re-point the layout/write-rule sources to `pm-agent.md`, and reword "Changing the store" and "Stores this is not". Contents list renumbered. |
| 18 | `docs/developer-guide/README.md:56,82` | Reword the two lines to `/sc:pm` and the PM agent. |
| 19 | `docs/getting-started/upgrading.md:241-248` | Step 5 keeps the copy recipe; says `/sc:pm` and the PM agent keep memory in `.superclaude/memory/`, and that 6.0.0 removed `/sc:save`, `/sc:load` and the `.serena` fallback. |
| 20 | `docs/onboarding/ironclaude-onboarding.html:534,574` | Remove the "Not a resume method" card text and the `/sc:save` trap; reword to name no removed command. |
| 21 | `docs/reference/pm-agent-autonomous-reflection.md:195` | "written by `/sc:save`" becomes "written by the PM agent". |
| 22 | `docs/user-guide/codegraph.md:123,125` | Delete the `/sc:load` bullet and drop `load.md` from the Source line. |
| 23 | `docs/user-guide/memory-system.md:18` | "that `/sc:save` writes and `/sc:load` reads" becomes "the PM agent writes and reads". |
| 24 | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:196`, `:1321` and `:2203` | "Seven command files with no section" becomes five (`implement`, `post-release`, `roadmap`, `validate-roadmap`, `validate-tests`), 46 command files becomes 44, phase P3 list loses `save`, and the sentence about `/sc:load` and the `:204` brief line is removed. |

## C. Looked at and NOT changed (with the reason)

| Reference | Why it stays |
|---|---|
| `docs/releases/**`, `docs/testing/v5.0.0/**` (the session-memory test plan), `docs/designs/**`, `CHANGELOG.md` | Historical records (issue 571 rule). The release PR adds the 6.0.0 entry. |
| Tracked `.dev/**` (task packages, brainstorms, orca-command-refactor, benchmarks, reflect runs) | Dated working records of past work. |
| `tests/recommend/fixtures/routing_refresh_cases.json:754,764` and the `formatting_only` list in `test_routing_refresh.py` | The frozen command-disposition record; the test compares it with the shipped set through `_POST_REFRESH_REMOVALS`. |
| `src/superclaude/skills/ccsession-tag/install.sh:45`, `tests/unit/test_ccsession_tag.py:1081,1151` | `PLAN-context-save-load.md` is an old file name the installer cleans up; it is not the command. |
| `PROJECT_INDEX.md:14` (43 commands), `docs/developer-guide/technical-architecture.md:43` (45 commands), `docs/getting-started/upgrading.md:85` (45 commands) | Counts that are already stale before this PR (46 command files today) and sit in shared files other wave-2 PRs edit. Not changed here, to avoid conflicts; the release PR recounts. |
| `src/superclaude/cli/**`, hooks, `Makefile`, `pyproject.toml`, `.github/**`, installer | No reference (checked). `cli/pipeline/dataflow_graph.py:220` `"load"` is an unrelated verb. |
| `.claude/settings.json` | Names hook scripts only. |
| `pm.md`, `pm-agent.md`, `sc-pm-protocol` | Describe the memory folder and its lifecycle without naming either command. |

## D. Install and routing surface

- `superclaude install` copies every `src/superclaude/commands/*.md`; deleting the two files drops them from the install set. `tests/unit/test_cli_install.py` pins the list (B2 #13).
- The installer does not remove commands a release stops shipping; that is PR 12 (retire step). Existing workspaces keep `~/.claude/commands/sc/save.md` until then.
- Mirrors: `.claude/commands/sc/{save,load}.md` (gitignored, removed by hand, section A); `plugins/superclaude/**` and root `commands/` are tracked and edited here.
- Routing: both commands live only in the Other-commands block of `HOW-WE-WORK.md`; the routing test lists them in `_OTHER_COMMANDS` (B2 #9).

## E. Does any kept skill or command need the removed commands?

No. `sc-crash-recovery` mentions `/sc:load` only to say it does not replace it. `sc-roadmap-protocol` triggers `sc:save` as an extra, and keeps its own `.session-memory.md` persistence and resume protocol. `WORKER-CONTRACT.md` uses `/sc:load` only as an example line. No STOP needed.

## F. Acceptance checks derived from this map

1. `git grep -n -E 'sc:save|sc:load|sc-save|sc-load'` outside the section C historical set returns nothing; `git grep -n -E '(save|load)\.md'` returns only the `ccsession-tag` clean-up lines.
2. `tests/core/test_how_we_work_routing_table.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/recommend/`, `tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py` pass.
3. `superclaude install` into a throwaway HOME succeeds, no `save.md` or `load.md` is installed, `sc-crash-recovery` is installed, `superclaude doctor` passes.
4. Full suite: failures equal baseline (2 known); pass count drops only by the removed test (`test_load_usage_line_declares_checkpoint_and_load_is_not_converted`, 1 test) plus the parametrized `load` case of `test_unconverted_command_has_no_unattended_section`, plus the S25 case tests, if any are parametrized by case id.
