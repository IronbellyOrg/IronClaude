# Dependency map: remove /sc:index and /sc:index-repo (6.0.0, PR 9)

Measured 2026-11-18 on branch clayphi/v6-index at 956f49642 (= origin/integration), after the
removals of /sc:build, /sc:improve and cli-portify. The plan counted 6 files deleted and 9 edited
outside, measured at d4d1662a8; the re-measure below finds more edits outside (shared files and
tests changed since), listed in full.

Method: `git grep` over every tracked file for `sc:index`, `sc-index`, `index-repo`, `index_repo`,
`sc/index`, `sc:sc:index`; a second pass for bare `/index`, `index.md`, `PROJECT_INDEX`, "Repository
Indexing" and "knowledge base" prose; codegraph search (`index-repo`: only test symbols; `PROJECT_INDEX`:
not a code symbol) and codegraph impact (nothing in Python code calls either command). Both commands are
markdown only: no Python module, no skill, no hook, no installer list names them.

## Scope rules applied

- Historical records are not edited: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past
  `CHANGELOG.md` entries (and no new CHANGELOG entry).
- `.dev/` holds working records (about 2,000 research, task and experiment files name the commands, for
  example `.dev/research/346-review-loop-experiments`, `.dev/tasks/done`). They are records of past work,
  not shipped surface, and are not edited. The leftover search excludes `.dev/`. This is stated in the PR body.
- Kept on purpose (not part of this removal): the `repo-index` agent (agents are issue 572), codegraph,
  `/sc:graph`, the generated `PROJECT_INDEX.md` and `PROJECT_INDEX.json` files at the repo root (they are
  data files other PRs of this wave also touch, not commands), `src/superclaude/execution/reflection.py:321`
  (reads `PROJECT_INDEX.md` if present; needs no command), and the frozen command record of the
  recommend-refresh package in `tests/recommend/fixtures/routing_refresh_cases.json` (the `commands` list at
  lines 665-666 stays, as it did for build, improve, save and load).
- No kept skill or command needs the removed commands: nothing under `src/superclaude/skills/`, `agents/`,
  `hooks/` or `cli/` names them (checked), and `launch-level-guard.sh` does not list them (so there is no
  hook entry to keep, unlike `improve`).

## A. Delete (6 files)

| Path | Why |
|---|---|
| `src/superclaude/commands/index.md` | source of truth |
| `src/superclaude/commands/index-repo.md` | source of truth |
| `plugins/superclaude/commands/index.md` | plugin mirror |
| `plugins/superclaude/commands/index-repo.md` | plugin mirror |
| `commands/sc-index.md` | legacy root commands folder |
| `commands/sc-index-repo.md` | legacy root commands folder |

`.claude/commands/sc/index.md` and `index-repo.md` are gitignored mirrors: removed by deleting them locally
(`make sync-dev` copies but does not delete; check and remove by hand). Never staged.

## B. Edit: shipped text

| path:line | Change |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md:193` | delete the whole table row (its only subject is `/sc:index`) |
| `src/superclaude/core/HOW-WE-WORK.md:324,325` | delete both rows of the Other-commands block |
| `src/superclaude/core/HOW-WE-WORK.md:365` | `document-built` row: drop "coordinated project docs" from the intent, drop step `1b ... /sc:index`, renumber `1c` to `1b` |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:193,324,325,365` | byte-for-byte copy of the guide (CLAUDE.md rule); `cp` after editing |
| `src/superclaude/core/CLAUDE.md` | no mention; the level-table block is not touched, so no re-copy. `tests/core/test_claude_md_routing_block.py` confirms |
| `src/superclaude/core/WORKER-CONTRACT.md:329` | default set: "15 commands converted in P1 (... index-repo ... index ...)" becomes 13, remove both names |
| `src/superclaude/core/WORKER-CONTRACT.md:334` | "12 commands that are ready with brief constraints" becomes 11; `/sc:index-repo` and `/sc:init-lite` sentence becomes `/sc:init-lite` alone; "15 rows" becomes 14 |
| `src/superclaude/core/WORKER-CONTRACT.md:345` | delete the `/sc:index-repo` row of the brief flag table |
| `commands/sc-README.md:8` | delete the `index-repo.md` bullet |
| `commands/sc-help.md:40` | delete the `/sc:sc:index` row |

## C. Edit: docs

| path:line | Change |
|---|---|
| `docs/user-guide/commands.md:89,90` | delete both table rows |
| `docs/user-guide/commands.md:297-` | delete the `### /sc:index` section (to the next `###`) |
| `docs/user-guide/commands.md:1135-` | delete the `### /sc:index-repo` section (to the next `###`) |
| `docs/user-guide/commands.md` (anchors) | `#scindex-repo---repository-indexing` link goes with row 89; check no other anchor links in or out |
| `docs/user-guide/flags.md:108` | delete the "Index Command Flags" section |
| `docs/generated/contributor-knowledge-base/architecture-guide.md:243,244` | delete the `index.md` and `index-repo.md` bullets |
| `docs/generated/contributor-knowledge-base/components-guide.md:164,165` | same |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1315` | layout (d) list: drop `index, index-repo`, "20 commands" becomes 18 |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:81,196,290,317,710,745,1319,1321,1958,2197,2230` | converted-command and command-file counts. Measured now: 27 of 40 command files carry `## Unattended mode` (doc says 28 of 41: already one behind after the cli-portify removal). After this PR: 25 of 38 (13 in P1, 12 in P2); P1 15 to 13; `UNATTENDED_EXPECT` 27 to 25 keys |

Not edited: `README.md:225` and `docs/generated/contributor-knowledge-base/repository-overview.md:94`
(`PROJECT_INDEX.md` as a file in the repo, true while the file exists); count statements such as "45 slash
commands" in `docs/developer-guide/technical-architecture.md:43` and `docs/getting-started/upgrading.md:85`
(already stale before this PR, shared with other PRs of the wave; left for the release PR).

## D. Edit: tests

| path:line | Change |
|---|---|
| `tests/core/test_how_we_work_routing_table.py:33,34` | remove `sc:index`, `sc:index-repo` from `_OTHER_COMMANDS` |
| `tests/core/test_how_we_work_routing_table.py:879` | remove `sc:index` from the `document-built` token set |
| `tests/core/test_how_we_work_routing_table.py:1014-1020` | `test_other_operations_...`: drop the three assertions that pin `mode=quick or mode=update`, `PROJECT_INDEX.md and PROJECT_INDEX.json`, `Coordinated project docs/API/structure/README` |
| `tests/recommend/fixtures/routing_refresh_cases.json:~481-501` | retire case S24 (its repeat and variants go with it); `commands` list at 665-666 stays |
| `tests/recommend/test_routing_refresh.py:314-316` | drop the `index-repo` mode check (explain and tasklist checks keep the test meaningful) |
| `tests/recommend/test_routing_refresh.py:352-355` | `test_route_check_rejects_other_route_for_a_routed_command` uses `sc:index` as a stand-in name; use a command that stays |
| `tests/recommend/test_routing_refresh.py` header, `_POST_REFRESH_REMOVALS`, case-id list | add `index`, `index-repo` to removals; S24 retired in the id list and docstring |
| `tests/recommend/test_routing_refresh.py:681` | `formatting_only` list derives from the frozen record: stays |
| `tests/skills/test_codegraph_adoption.py:258,280` | remove `index-repo.md` from `_ISSUE_504_COMMANDS` and `_OWN_CHECK_COMMANDS` |
| `tests/skills/test_worker_contract.py:481,489,554-558,604-608` | remove `index-repo` and `index` from `P1_COMMANDS` and `UNATTENDED_EXPECT`; fix every count (15 to 13, 27 to 25, "fifteen" wording) |
| `tests/skills/test_worker_contract.py:1267-1270` | delete `test_index_repo_output_format_states_where_the_files_land` |
| `tests/unit/test_cli_install.py:116,400,525,543,639` | remove `index-repo.md index.md` from the two sample lists; the assertions at 525, 543, 639 use `index-repo` as a sample command: switch to a command that stays |

Tests that fail until edited are found by running the suite; the list above is the grep result plus the count
checks in `test_worker_contract.py` (1400-1401, 1599-1606).

## E. Install code and CLI

No entry. `superclaude install` copies whatever is in `src/superclaude/commands/`; nothing lists the two
commands (checked `src/superclaude/cli/install_*.py`, `pyproject.toml`, `Makefile`, `.github/`, plugin
manifests). Installed copies of `index.md` and `index-repo.md` in existing workspaces stay until the retire
step (PR 12); the `improve` precedent for hooks does not apply because no hook names them.

## F. Check at the end

1. `git grep -nE 'sc:index|sc-index|index-repo|index_repo|sc/index'` outside the historical records and `.dev/`:
   only the frozen record in `tests/recommend/fixtures/routing_refresh_cases.json` (commands list) and the
   `repo-index` agent are allowed.
2. `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/`, `git diff --check`.
3. Full test suite: 0 new failures; pass count drops only by the removed tests.
4. `superclaude install` into a throwaway HOME, then `superclaude doctor` there.
