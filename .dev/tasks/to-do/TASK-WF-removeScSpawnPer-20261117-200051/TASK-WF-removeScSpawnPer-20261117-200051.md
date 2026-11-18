---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeScSpawnPer-20261117-200051
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove /sc:spawn (IronClaude 6.0.0, PR 5)

Source: ./source.md
Goal: `/sc:spawn` is gone from the commands, the plugin mirror, the routing guide, the worker contract, the launch-level hook, the docs and the tests that pin it, with no file outside the historical records naming it, and the routing, worker-contract, hook and install checks passing.

## Constraints

- Source of truth is `src/superclaude/`. Never stage anything under `.claude/` except `.claude/settings.json`; the local mirror copy of the command in the project's `.claude` folder is gitignored sync output.
- Do not edit historical records: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries, and anything under `.dev/` other than the plan's own package. Do not add a `CHANGELOG.md` entry (the release PR does that).
- Swarm and everything in the issue's "Kept for now" list stays untouched. Edit only the `/sc:spawn` lines of `launch-level-guard.sh` and its test (PRs 7 and 8 edit the same files later).
- The frozen research package `.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/` is not edited; the 47-command record in `routing_refresh_cases.json` must keep matching its Appendix C.
- Never hardcode `src/superclaude/...` paths in installed primitives; the adversarial skill edit must only remove a citation.
- Detail and line numbers for every item are in `.dev/cleanup/spawn/dependency-map.md`.

## Phase 1: Remove the command and its citations

## Task 1: Delete the command file and its three copies

Delete `src/superclaude/commands/spawn.md`, `plugins/superclaude/commands/spawn.md` and `commands/sc-spawn.md` from the repo, and delete the untracked local mirror copy of the command in the project's `.claude` folder (gitignored, so `make sync-dev` would leave it behind). Run `make sync-dev` afterwards so the other mirrors stay current. Dependents that name the file are handled by the later tasks: the install test (Task 8), the routing-refresh test (Task 6), the guide (Task 3) and the docs (Tasks 9 to 12).

Acceptance criteria:
- None of the four paths exists, and `ls src/superclaude/commands | grep -c spawn` prints 0.
- `git status` shows exactly three tracked deletions for this task and no staged `.claude/` path.

## Task 2: Drop the spawn citation from the adversarial skill

Depends on: Task 1

In `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`, two places cite `spawn.md` Rule 2.5 as the producer of the `branch-trace.md` artifact: the `evidence_preference` line near line 1203 (`per ~/.claude/commands/sc/spawn.md Rule 2.5`) and the fault-finder prompt near lines 1262 to 1263 (`per spawn.md Rule 2.5`). Remove only the spawn citation in each place and keep the surrounding "if a branch-trace exists, cite specific branches; otherwise enumerate the source inline" rule. No `plugins/superclaude` copy of this skill exists, so there is no mirror to edit. Run `make sync-dev` so the local mirror matches.

Acceptance criteria:
- `grep -n "spawn" src/superclaude/skills/sc-adversarial-protocol/SKILL.md` prints only unrelated sub-agent "spawn" wording, no `spawn.md`, and the two `branch-trace` sentences still read as complete rules.
- `uv run pytest tests/skills -k adversarial -q` shows no new failure.

## Phase 2: Routing guide and worker contract

## Task 3: Remove /sc:spawn from the routing guide and its twin

Depends on: Task 1

In `src/superclaude/core/HOW-WE-WORK.md` delete the `/sc:spawn` row of the Other-commands table (line 334) and delete the sentence "spawn's final decomposition-only stop wins over earlier execution prose." from the "Other deferred differences" bullet (line 270). Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (the two are identical today). If the level-table copy into `src/superclaude/core/CLAUDE.md` is affected, re-run it; the dependency map shows no spawn text there, so expect no change.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and neither file contains `spawn` as a command name.
- The twin readers still pass: `uv run pytest tests/skills/test_review_prompt_overrides.py tests/skills/test_review_brief_placement.py tests/skills/test_spec_panel_review_loop.py -q`.

## Task 4: Remove /sc:spawn from the never-as-worker list and its pins

Depends on: Task 1

In `src/superclaude/core/WORKER-CONTRACT.md` line 23, drop `/sc:spawn` from the never-as-worker list, leaving `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:sweep` and `/sc:swarm-wizard`, plus the `/sc:pr-submit` clause unchanged. In `tests/skills/test_worker_contract.py` make three edits: the pinned phrase at line 89 (same list), the `NEVER_AS_WORKER` tuple at line 468, and the `NOT_CONVERTED_IN_P1` tuple at line 1455 (remove `"spawn"`). Check whether `WORKER-CONTRACT.md` is also pinned elsewhere by a count of the list's names and adjust only if a test fails for that reason.

Acceptance criteria:
- `grep -n spawn src/superclaude/core/WORKER-CONTRACT.md tests/skills/test_worker_contract.py` prints nothing about the command.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes, with its parametrized case count down by exactly the two removed parameters (one in `NEVER_AS_WORKER`, one in `NOT_CONVERTED_IN_P1`).

## Phase 3: Routing tests

## Task 5: Update the routing-table test for the Other-commands set

Depends on: Task 3

In `tests/core/test_how_we_work_routing_table.py` remove `"sc:spawn"` from the `_OTHER_COMMANDS` set (line 33).

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py -q` passes, including the check that the table members equal `_OTHER_COMMANDS` (near line 298).

## Task 6: Retire routing case S27 and make the command-set check expect the removal

Depends on: Task 3

In `tests/recommend/fixtures/routing_refresh_cases.json` delete the whole case object `S27` (lines 610 to 629; it routes to `/sc:spawn`). Leave the `spawn` entry of the frozen `commands` list (line 787) because it must equal Appendix C of the frozen research package. In `tests/recommend/test_routing_refresh.py` change the case-id check at line 135 so it expects S01 to S29 without S27, and change the shipped-versus-active comparison at lines 645 to 648 so a new set `_POST_REFRESH_REMOVALS = {"spawn"}` (next to `_POST_REFRESH_ADDITIONS`, with a comment saying the command was removed in 6.0.0) is subtracted from the frozen active set before comparing with the shipped commands. Update the docstring text that says "S01-S29 cases" only if it would now be false. Fix any further assertion in that file that fails because case S27 is gone, and keep every other check unchanged.

Acceptance criteria:
- `grep -n "sc:spawn" tests/recommend/fixtures/routing_refresh_cases.json` prints nothing; the only remaining `spawn` in that file is the frozen `commands` record.
- `uv run pytest tests/recommend -q` passes, and its pass count drops only by the tests that ran for S27 (its parametrized case and variants).

## Phase 4: Launch-level hook and install test

## Task 7: Drop spawn from the launch-level guard and its test

Depends on: Task 1

In `src/superclaude/hooks/scripts/launch-level-guard.sh` edit only two `/sc:spawn` lines: the LL-IMPL message at line 43 (`starting /sc:implement, /task, /sc:improve, /sc:cleanup or /sc:build (or their skills).`) and the skill-name case at line 409 (`implement | task | improve | cleanup | build`). Copy the file byte for byte to `plugins/superclaude/hooks/scripts/launch-level-guard.sh` (they are identical today). In `tests/hooks/test_launch_level_guard.py` remove `"sc:spawn"` from `IMPL_SPELLINGS` (line 907); check that no test pins the exact LL-IMPL message text and adjust it if one does.

Acceptance criteria:
- `diff src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh` prints nothing, and `git diff` for the script shows only the two spawn lines changed.
- `uv run pytest tests/hooks/test_launch_level_guard.py -q` passes with one fewer parametrized case (`sc:spawn`).
- `make verify-sync` prints "All components in sync."

## Task 8: Drop spawn.md from the install test's expected file lists

Depends on: Task 1

In `tests/unit/test_cli_install.py` remove `spawn.md` from the two expected command lists (lines 118 and 405). Keep each list in its current alphabetical order and line shape.

Acceptance criteria:
- `uv run pytest tests/unit/test_cli_install.py -q` passes.
- `grep -n spawn tests/unit/test_cli_install.py` prints nothing.

## Phase 5: Documentation

## Task 9: Remove /sc:spawn from the user guide

Depends on: Task 1

In `docs/user-guide/commands.md` delete the table row at line 39 and the whole `### /sc:spawn` section (lines 669 to 697, from its heading to the line before the `### /sc:swarm-wizard` heading, keeping one `---` separator between neighbours). In `docs/user-guide/flags.md` delete the "Spawn Command Flags" block (lines 160 to 165) including its blank line. Check both files for anchors or links to `#scspawn---meta-system-task-orchestration` and remove them.

Acceptance criteria:
- `grep -n -i "spawn" docs/user-guide/commands.md docs/user-guide/flags.md` prints nothing about the command, and neighbouring sections still have one `---` separator and one blank line between blocks.
- `git diff --check` is clean for both files.

## Task 10: Remove /sc:spawn from the developer guide

Depends on: Task 1

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` edit the Meta-Orchestrator archetype (lines 333 to 345): make the example list `/sc:adversarial` only, rewrite the "Worker fit" sentence so it speaks only about `/sc:adversarial` (keeping the WC-7 and WC-8 clause and the section 7.7 link), and delete the "Example from `/sc:spawn`" paragraph with its fenced block. At line 991 remove `/sc:spawn` from the never-as-worker list so it matches `WORKER-CONTRACT.md` after Task 4.

Acceptance criteria:
- `grep -n "sc:spawn" docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints nothing and the archetype still reads as a complete section.
- The never-as-worker list at line 991 names the same seven commands as `src/superclaude/core/WORKER-CONTRACT.md` line 23.

## Task 11: Remove /sc:spawn from the supervised-orchestration reference

Depends on: Task 4

In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` drop `/sc:spawn` from the never-as-worker list at lines 714 and 2196, recount the names of the list at line 714 as it then reads (including the `/sc:pr-submit` clause) and set its "Eight entries" wording to that count, drop `spawn` from the IMPL skill-name list at line 1605, and drop it from the guard-class glossary text at line 2212. Do not touch the `Orca spawn` and `PTY spawn` mentions elsewhere in the file; they are unrelated.

Acceptance criteria:
- `grep -n "sc:spawn\|cleanup\`, \`spawn\`" docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` prints nothing.
- The entry count written at line 714 equals the number of command names in the list that sentence now holds.

## Task 12: Remove the spawn row from the root legacy help copy

Depends on: Task 1

In `commands/sc-help.md` delete the `/sc:sc:spawn` table row at line 44.

Acceptance criteria:
- `grep -n spawn commands/sc-help.md` prints nothing and the table around line 44 stays contiguous.
- `git diff --check` is clean.
