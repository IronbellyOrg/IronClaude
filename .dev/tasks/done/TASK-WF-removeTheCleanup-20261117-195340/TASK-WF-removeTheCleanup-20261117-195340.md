---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeTheCleanup-20261117-195340
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove the cleanup-audit headless runner (6.0.0, pull request 2)

Source: ./source.md
Goal: `superclaude --help` no longer lists `cleanup-audit`, the package `src/superclaude/cli/cleanup_audit/` and its test are gone, and no tracked file outside the historical records names the removed runner, while the `sc-cleanup-audit-protocol` skill, the `/sc:cleanup-audit` command, the five `audit-*` agents and `src/superclaude/cli/audit/` are untouched.

## Constraints

- Source of truth is `src/superclaude/`. Do not touch `src/superclaude/skills/sc-cleanup-audit-protocol/`, `src/superclaude/commands/cleanup-audit.md`, the five `audit-*` agents or `src/superclaude/cli/audit/` (its docstring and `.cleanup-audit.json` name belong to the audit helpers, not to the runner).
- Do not edit historical records: `CHANGELOG.md`, `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, and anything under `.dev/` other than this package. Do not add a CHANGELOG entry.
- References that name the skill or the slash command (`/sc:cleanup-audit`, `sc-cleanup-audit-protocol`) are not the runner and stay, including `core/HOW-WE-WORK.md`, `core/WORKER-CONTRACT.md`, `docs/user-guide/commands.md` and their routing tests.
- Do not stage anything under `.claude/` (the mirror is gitignored; no mirror holds the runner, so `make sync-dev` changes nothing).
- Dependency map for every path and line below: `.dev/cleanup/cleanup-audit-runner/dependency-map.md`.

## Phase 1: Unregister and delete the runner

## Task 1: Remove the runner registration from the main command group

In `src/superclaude/cli/main.py` delete the deferred import `from superclaude.cli.cleanup_audit import cleanup_audit_group ...` (line 527), the line `main.add_command(cleanup_audit_group, name="cleanup-audit")` (line 529) and the blank line that separates them from the `tasklist_group` import, so the sprint, roadmap and tasklist registrations stay in the same style.

Acceptance criteria:
- `src/superclaude/cli/main.py` contains no `cleanup_audit` and no `cleanup-audit`.
- `uv run superclaude --help` exits 0 and its command list has no `cleanup-audit` entry, and still lists `sprint`, `roadmap`, `tasklist`, `cli-portify`, `prd`, `eval`, `swarm`, `recommend`, `init-lite`, `reflect` and the install commands.

## Task 2: Delete the cleanup_audit package

Depends on: Task 1

Delete the 13 files of `src/superclaude/cli/cleanup_audit/`: `__init__.py`, `commands.py`, `config.py`, `diagnostics.py`, `executor.py`, `gates.py`, `logging_.py`, `models.py`, `monitor.py`, `portify-summary.md`, `process.py`, `prompts.py`, `tui.py`. Use `git rm` so the deletion is tracked, and remove any leftover `__pycache__` directory so the folder is gone. Its only imports are the shared `superclaude.cli.pipeline` modules, which other runners use and which stay. Its only importers are `src/superclaude/cli/main.py` (Task 1) and `tests/test_cleanup_audit_structure.py` (Task 4).

Acceptance criteria:
- The directory `src/superclaude/cli/cleanup_audit/` does not exist.
- `src/superclaude/cli/pipeline/` and `src/superclaude/cli/audit/` are unchanged (`git status` shows no change under them).
- `uv run python -c "import superclaude.cli.main"` exits 0.

## Task 3: Release the reserved CLI module names in cli_portify

Depends on: Task 2

In `src/superclaude/cli/cli_portify/config.py` remove the two entries `"cleanup-audit"` and `"cleanup_audit"` from `_KNOWN_CLI_MODULES` (lines 29-30). The set is read only at `config.py:282` to refuse a portified CLI module name that collides with an existing module; that module no longer exists. Keep `"sprint"`, `"roadmap"`, `"tasklist"`, `"audit"`, `"pipeline"` and `"main"`.

Acceptance criteria:
- `_KNOWN_CLI_MODULES` has exactly the six remaining names.
- `uv run pytest tests/cli_portify -q` has no new failures against the baseline in `.dev/issues/v6-cleanup-audit-runner/baseline-test.log`.

## Phase 2: Update the tests that name the runner

## Task 4: Delete the runner's structure test

Depends on: Task 2

`git rm tests/test_cleanup_audit_structure.py`. It imports `superclaude.cli.cleanup_audit` and asserts that `cleanup-audit` is in `main.commands`, so it can only test the removed runner. Record its test count (collected before deleting, from the baseline log) in `.dev/issues/v6-cleanup-audit-runner/removed-tests.txt`, so the final pass count can be checked against "baseline minus removed".

Acceptance criteria:
- `tests/test_cleanup_audit_structure.py` does not exist.
- `.dev/issues/v6-cleanup-audit-runner/removed-tests.txt` lists the removed test ids and their count.

## Task 5: Update the expected top-level command set

Depends on: Task 1

In `tests/cli/test_cli_registration.py` remove `"cleanup-audit"` from `EXPECTED_TOP_LEVEL_COMMANDS` (line 33). Leave every other entry and the test logic as they are.

Acceptance criteria:
- `uv run pytest tests/cli/test_cli_registration.py -q` passes.
- The file contains no `cleanup-audit`.

## Task 6: Update the swarm registration test

Depends on: Task 1

In `tests/swarm/test_cli_registration.py` remove `cleanup-audit` from the module docstring (line 7) and from the `forbidden_parents` tuple (line 86), leaving `("sprint", "roadmap", "tasklist")`. The test must still assert that `swarm` is not nested under the other groups. Make no other change to swarm tests or swarm code.

Acceptance criteria:
- `uv run pytest tests/swarm/test_cli_registration.py -q` passes.
- The file contains no `cleanup-audit`, and `git diff --stat` shows only this file changed under `tests/swarm/`.

## Task 7: Remove the runner file from the packaged-resources baseline list

Depends on: Task 2

In `tests/unit/test_cli_install.py` remove the token `cleanup_audit/portify-summary.md` from the `"cli"` entry of `_PACKAGE_RESOURCES` (line 72), keeping the neighbouring tokens (`audit/wiring_whitelist.yaml`, `eval/pty/CHECKLIST.md`, ...) in place and the block's line layout valid for ruff format. `_assert_present` (line 502, used by the parametrized test at line 894) requires every listed file to exist, so the entry would fail once the file is deleted.

Acceptance criteria:
- `uv run pytest tests/unit/test_cli_install.py -q` passes, with the same number of tests as the baseline (the parametrization is by resource class, not by file).
- `uv run ruff format --check tests/unit/test_cli_install.py` stays as it was at baseline (the file is not in `.dev/issues/v6-cleanup-audit-runner/baseline-format-files.txt`, so it must pass).

## Phase 3: Update the developer docs and project indexes

## Task 8: Update the CLI description in the technical architecture guide

Depends on: Task 1

In `docs/developer-guide/technical-architecture.md` line 315, remove `cleanup-audit` from the list of pipeline commands (`sprint`, `roadmap`, `tasklist`, `eval`, `swarm`, `reflect`, `prd`, `cli-portify` and `cleanup-audit`), fixing the "and" so the sentence stays grammatical (`... `prd` and `cli-portify` commands ...`). Do not change the rest of the sentence or the `/sc:cleanup-audit` mentions elsewhere in the file.

Acceptance criteria:
- Line 315 no longer contains `cleanup-audit` and still reads as one correct sentence.
- `git diff` of this file changes only that sentence.

## Task 9: Reword the README workflow list

Depends on: Task 1

In `README.md` line 142 change `- audit and cleanup audit flows` to `- audit flows`, because the runner was the only CLI cleanup-audit flow. Make no other README change.

Acceptance criteria:
- `README.md` line 142 reads `- audit flows` and `git diff` of the file shows only that line.

## Task 10: Update the machine-readable project index

Depends on: Task 1

In `PROJECT_INDEX.json` remove `"cleanup-audit"` from the `groups` array (line 46) and `"cleanup_audit"` from the `subpackages` array (line 94), keeping the other items in order and the JSON valid.

Acceptance criteria:
- `uv run python -c "import json; json.load(open('PROJECT_INDEX.json'))"` exits 0.
- The file contains neither `cleanup-audit` nor `cleanup_audit`.

## Task 11: Update the readable project index

Depends on: Task 10

In `PROJECT_INDEX.md` remove `` `cleanup-audit` `` from the Groups line (line 36) and `` `cleanup_audit/` `` from the Subpackages line (line 68), so both lines match the edited `PROJECT_INDEX.json`.

Acceptance criteria:
- `PROJECT_INDEX.md` contains neither `cleanup-audit` nor `cleanup_audit`, and the two edited lines list the same names as the JSON arrays.

## Phase 4: Update the generated contributor docs

## Task 12: Update the generated architecture guide

Depends on: Task 1

In `docs/generated/contributor-knowledge-base/architecture-guide.md` remove the bullet `` - `cleanup_audit/` `` (line 162), the diagram node `F --> Q[cleanup-audit group]` (line 302) and the node `CLI --> CLEANUP[cleanup_audit/]` (line 315). Check the mermaid blocks still have no dangling node reference to `Q` or `CLEANUP`.

Acceptance criteria:
- The file contains neither `cleanup_audit` nor the group node, and no remaining line references node `Q` or `CLEANUP`.

## Task 13: Update the generated CLI inventory

Depends on: Task 1

In `docs/generated/contributor-knowledge-base/cli-api-inventory.md`: remove `cleanup-audit` from the subsystems row (line 18, and the `cleanup_audit/` mention in its note); remove the tree entry `├── cleanup_audit/` (line 34); remove the command row for `superclaude cleanup-audit ...` (line 60); remove `cleanup-audit` from the `main.py` description (line 67); delete the whole section `## cleanup_audit/ subpackage` (lines 145-170 through its last row, up to the next `##` heading); remove `cleanup-audit` from the root subgroups row (line 231), delete the `Cleanup-audit subcommands` row (line 234), and fix the wording at lines 246, 263, 274 and 284 so they list only `sprint` and `roadmap`. Keep line 211 (it describes `src/superclaude/cli/audit/`) and line 287 (the "cleanup/audit internals" pointer to `cli/audit/`).

Acceptance criteria:
- `grep -n 'cleanup_audit\|cleanup-audit' docs/generated/contributor-knowledge-base/cli-api-inventory.md` prints only the `cli/audit/` description (line 211 before editing) and the line 287 pointer, neither of which names the runner.
- No table in the file is left with a broken header or a stray separator row.

## Task 14: Update the generated components guide

Depends on: Task 1

In `docs/generated/contributor-knowledge-base/components-guide.md` delete the entry `#### src/superclaude/cli/cleanup_audit/` and its one-sentence description (lines 54-56), keeping one blank line between the neighbouring entries.

Acceptance criteria:
- The file contains neither `cleanup_audit` nor `cleanup-audit`, and the headings before and after the removed entry are intact.

## Task 15: Update the generated visual architecture summary

Depends on: Task 1

In `docs/generated/contributor-knowledge-base/visual-architecture-summary.md` remove the node `CLI --> CLI_CLEANUP[cleanup_audit/]` (line 219), the node `B --> K[cleanup-audit group]` (line 251), the `K --> K1 ...` block that describes `src/superclaude/cli/cleanup_audit/` with its `K2`, `K3`, `K4` children (lines 287-290 and any further `K1` lines), and the word `` `cleanup_audit`, `` in the subsystem list at line 614. Leave line 615 (it names the `cleanup-audit` protocol-backed command, which stays).

Acceptance criteria:
- No line of the file references node `K`, `K1`..`K4` or `CLI_CLEANUP` after the edit, and the file contains no `cleanup_audit`.
- The `cleanup-audit` mention that remains is only the protocol-backed command family at the former line 615.

## Task 16: Update the generated sprint data-model doc

Depends on: Task 1

In `docs/generated/sprint-cli/02-data-models.md` remove the three tree lines `+-> CleanupAuditConfig (cleanup_audit/models.py)` (line 17), `+-> CleanupAuditStep (cleanup_audit/models.py)` (line 21) and `+-> CleanupAuditStepResult (cleanup_audit/models.py)` (line 25). If a base-model line is left with a single child, keep the tree layout valid.

Acceptance criteria:
- The file contains no `CleanupAudit` and no `cleanup_audit`.

## Task 17: Update the generated sprint gates doc and prove no reference is left

Depends on: Task 16

In `docs/generated/sprint-cli/04-gates-validation.md` remove the line `- cleanup_audit/gates.py defines GATE_G001..GATE_G006 with same pattern` (line 198, with its backticks as written in the file).

Acceptance criteria:
- `git grep -nIiE 'cleanup_audit|CleanupAudit|superclaude cleanup-audit' -- . ':!.dev' ':!.claude' ':!CHANGELOG.md' ':!docs/releases' ':!docs/testing/v5.0.0' ':!docs/designs'` prints nothing.
- `git grep -nIE 'cleanup-audit' -- . ':!.dev' ':!.claude' ':!CHANGELOG.md' ':!docs/releases' ':!docs/testing/v5.0.0' ':!docs/designs'` prints only lines that name the skill, the `/sc:cleanup-audit` command, the `cli/audit` helpers or the `cleanup-audit-v2-UNIFIED-SPEC` release folder, each listed in the Constraints or the dependency map.
- `make sync-dev` then `make verify-sync` pass, and `git diff --check` is clean.
