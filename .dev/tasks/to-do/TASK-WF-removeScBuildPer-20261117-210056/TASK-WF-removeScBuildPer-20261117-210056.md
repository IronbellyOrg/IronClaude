---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeScBuildPer-20261117-210056
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove /sc:build (IronClaude 6.0.0, PR 7)

Source: ./source.md
Goal: `/sc:build` is gone from the commands, the plugin mirror, the legacy root commands folder, the routing guide, the worker contract, the launch-level hook, the docs and the tests that pin it, with no file outside the historical records naming it, and the full test suite shows no new failure.

## Constraints

- Source of truth is `src/superclaude/`. Never stage anything under `.claude/` except `.claude/settings.json`; the local mirror copy of the command in the project's `.claude` folder is gitignored sync output.
- Do not edit historical records: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries, and anything under `.dev/` other than this plan's own package. Do not add a `CHANGELOG.md` entry.
- Swarm and everything in the issue's "Kept for now" list stays untouched. In `launch-level-guard.sh` and its test edit only the `/sc:build` lines.
- The frozen research package `.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/` is not edited; the 47-command record in `tests/recommend/fixtures/routing_refresh_cases.json` stays as it is.
- The `sc-cli-portify-protocol` skill is removed later by another change; edit only its one `/sc:build` mention.
- Never hardcode `src/superclaude/` paths in installed primitives.
- Detail and line numbers for every item are in `.dev/cleanup/build/dependency-map.md`. `.dev/tasks/` is always staged with the commit.

## Phase 1: Remove the command and its skill mention

## Task 1: Delete the command file and its copies

Delete `src/superclaude/commands/build.md`, `plugins/superclaude/commands/build.md` and `commands/sc-build.md` from the repo, and delete the untracked local mirror `.claude/commands/sc/build.md` (gitignored; never staged).

Acceptance criteria:
- None of the four paths exists, and `ls src/superclaude/commands | grep -c '^build'` prints 0.
- `git status` shows exactly three tracked deletions for this task and no staged `.claude/` path.

## Task 2: Drop the build bullet from the cli-portify skill

Depends on: Task 1

In `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md` line 594, delete the bullet that reads "`/sc:build` — Build and compile after generating" so the surrounding list stays a valid list of the remaining commands.

Acceptance criteria:
- `git grep -n 'sc:build' -- src/superclaude/skills` prints nothing.
- The list that held the bullet still reads as a complete list (read the lines around 590-598).

## Phase 2: Routing guide, worker contract and launch-level hook

## Task 3: Remove /sc:build from the routing guide and its twin

Depends on: Task 1

In `src/superclaude/core/HOW-WE-WORK.md` delete the `/sc:build` row of the Other-operations table (line 324) and change "the 16 phase 1 commands" to "the 15 phase 1 commands" in the `--unattended` bullet (line 403). Copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. The level table is untouched, so `src/superclaude/core/CLAUDE.md` needs no edit.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and neither file contains `/sc:build`.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_brief_placement.py tests/skills/test_spec_panel_review_loop.py -q` shows no new failure once Task 6 is done.

## Task 4: Update the converted-command count in the worker contract

Depends on: Task 1

In `src/superclaude/core/WORKER-CONTRACT.md` line 329 change "the 16 commands converted in P1 (adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test)" to "the 15 commands" and delete `build, ` from the list.

Acceptance criteria:
- `grep -n 'analyze, business-panel' src/superclaude/core/WORKER-CONTRACT.md` finds the edited sentence and it names 15 commands.
- The never-as-worker list on the same file is unchanged.

## Task 5: Remove build from the launch-level guard and its plugin twin

Depends on: Task 1

In `src/superclaude/hooks/scripts/launch-level-guard.sh` change line 43 to `b='starting /sc:implement, /task, /sc:improve or /sc:cleanup (or their skills).'` and line 409 to `implement | task | improve | cleanup) LL_CLASSES+='IMPL ' ;;`. Make the same two edits in `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, keeping both files identical.

Acceptance criteria:
- `diff src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh` prints nothing, and `grep -c build` on either file prints 0.
- `bash -n src/superclaude/hooks/scripts/launch-level-guard.sh` exits 0.

## Phase 3: Tests that pin the command

## Task 6: Update the routing, hook and refresh tests

Depends on: Task 3, Task 5

In `tests/core/test_how_we_work_routing_table.py` delete `"sc:build"` from `_OTHER_COMMANDS` (line 28). In `tests/hooks/test_launch_level_guard.py` add the rewrite from `/sc:improve, /sc:cleanup or /sc:build` to `/sc:improve or /sc:cleanup` to `_REMOVED_COMMAND_TEXT` after the existing spawn entry (line 81), and delete `"sc:build"` from `IMPL_SPELLINGS` (line 917). In `tests/recommend/test_routing_refresh.py` add `"build"` to `_POST_REFRESH_REMOVALS` (line 35, comment names 6.0.0 and the removed command), and drop build from `test_example_only_flags_are_not_declared_or_routed` (docstring, the `("build", "--validate")` tuple and the `sc:build` route at lines 589-599). Leave `tests/recommend/fixtures/routing_refresh_cases.json` untouched.

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/hooks/test_launch_level_guard.py tests/recommend/test_routing_refresh.py -q` shows no new failure against the baseline (the one timing test `test_speed_large_commands[heredoc-git-words-64KB]` failed under load before any edit; re-run it alone).
- `git grep -n 'sc:build' -- tests` prints nothing.

## Task 7: Update the worker-contract test pins

Depends on: Task 1

In `tests/skills/test_worker_contract.py` drop `"build"` from `P1_COMMANDS` and change the comment "The sixteen commands" to "The fifteen commands" (lines 473-485), delete the `"build"` entry of `UNATTENDED_EXPECT` (lines 583-587), delete the `build = _artifacts_clause(...)` assertions (lines 1394-1399), change the 16 checks in `_check_p1_set` to 15 including the messages (lines 1467-1468), and change the 31 check in `_check_p2_set` to 30 including the message (line 1675).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` shows no new failure and `grep -n '"build"' tests/skills/test_worker_contract.py` prints nothing.
- The P1 set has 15 names, the P2 set 15, and `UNATTENDED_EXPECT` 30.

## Task 8: Update the install test file lists

Depends on: Task 1

In `tests/unit/test_cli_install.py` delete `build.md` from the two expected command-file lists (lines 114 and 402), keeping the lines' alphabetical order and wrapping.

Acceptance criteria:
- `uv run pytest tests/unit/test_cli_install.py -q` shows no new failure.
- `grep -n 'build.md' tests/unit/test_cli_install.py` prints nothing.

## Phase 4: Docs and legacy command copies

## Task 9: Remove /sc:build from the user guide

Depends on: Task 1

In `docs/user-guide/commands.md` delete the `/sc:build` row of the command table (line 70) and the whole `### /sc:build - Project Building` section with its trailing `---` (lines 1191-1219). In `docs/user-guide/flags.md` delete the `### Build Command Flags (/sc:build)` block (lines 60-68). In `docs/user-guide/agents.md` line 157 change "`/sc:implement`, `/sc:build` and `/sc:improve` do not call it" to "`/sc:implement` and `/sc:improve` do not call it".

Acceptance criteria:
- `git grep -n 'sc:build\|scbuild' -- docs/user-guide` prints nothing.
- No anchor link `#scbuild---project-building` remains in `docs/`.

## Task 10: Remove /sc:build from the developer guide and the architecture reference

Depends on: Task 4, Task 7

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` delete `/sc:build` from the Unified Executor examples (line 342) and change the converted-command counts at lines 976-977 to 30 commands (15 from phase 1, 15 from phase 2) and "the 15 phase 1 commands". In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` drop `build` from the IMPL class row (line 1605) and change each current-state count of converted commands from 31 to 30 and of phase 1 from 16 to 15 where it names the converted set (lines 317, 745, 1321, 1355, 1958, 2197 and 2203; read each line first and leave dated historical sentences alone).

Acceptance criteria:
- `git grep -n 'sc:build' -- docs/developer-guide docs/architecture` prints nothing.
- Each edited count agrees with `grep -rl '^## Unattended mode' src/superclaude/commands | wc -l`, which prints 30.

## Task 11: Remove the command from the generated knowledge-base docs and the legacy root commands

Depends on: Task 1

In `docs/generated/contributor-knowledge-base/architecture-guide.md` (line 239) and `components-guide.md` (line 158) delete the `build.md` list entry. In `commands/sc-help.md` delete the `/sc:sc:build` table row (line 31) and the example line at line 123 that uses `/sc:sc:build`. In `commands/sc-recommend.md` replace each `/sc:sc:build` (25 lines) with `/sc:sc:implement`, and at line 490 delete the `"/sc:sc:build", ` entry instead because `/sc:sc:implement` already follows it.

Acceptance criteria:
- `git grep -n -E 'sc:sc:build|sc:build|build\.md' -- docs/generated commands` prints nothing (other than unrelated `build-request` hits).
- `git diff --stat commands/sc-recommend.md` shows only changed lines, no other command renamed.
