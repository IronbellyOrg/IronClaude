# Dependency map: remove /sc:review-translation and sc-review-translation-protocol

Measured at: integration `783832f11` (branch `clayphi/v6-review-translation`), 2026-11-17.
Method (read-only): `git grep -n -i -E 'review[-_ ]?translation'` over tracked files (excluding the
historical records), a broader `git grep` for `translat|locali[sz]|l10n|tone[- ]matrix`,
`git ls-files | grep -i review-translation`, codegraph search for `review_translation`, a check of
`plugins/`, `commands/`, `skills/`, `agents/`, `.claude-plugin/`, install code and hooks, and a read of
the `/sc:spawn` removal commit `5b7d13e73` as the precedent for which files carry names and counts.

Codegraph result: no function, class or import names the item. The only indexed hits are the test
file `tests/unit/test_review_translation.py` and the variable `P2_NEW_BRIEF_ROWS` in
`tests/skills/test_worker_contract.py`. No Python code under `src/superclaude/` (cli, install code,
hooks, pm_agent) refers to it.

Plan counts vs measured: the plan said 3 files deleted, 12 edited (4 tests, 5 docs, 3 other).
Measured: 3 files deleted (command, skill, its unit test), 14 files edited outside the deleted
three (5 test files incl. the fixture, 6 docs, 3 shipped files; see B to D below), plus 2 local mirror copies removed by hand (ignored by git).

## A. Delete (3 tracked files)

| Path | Action |
|---|---|
| `src/superclaude/commands/review-translation.md` | delete (blob a2a5f8e0f, same on fork) |
| `src/superclaude/skills/sc-review-translation-protocol/SKILL.md` | delete (blob c5a26e491, same on fork; the only file in that folder, no `refs/`) |
| `tests/unit/test_review_translation.py` | delete (565 lines, 44 test functions; imports only `re` and `pytest`, tests no production code) |

Local mirrors, gitignored, never staged: `.claude/commands/sc/review-translation.md` and
`.claude/skills/sc-review-translation-protocol/`. `make sync-dev` copies but never prunes, so delete
them by hand or `make verify-sync` reports stale files. No tracked copy exists under
`plugins/superclaude/commands|skills`, root `commands/`, root `skills/` or `agents/`.

## B. Edit: shipped text (source of truth `src/superclaude/`)

| Path:line | Change |
|---|---|
| `src/superclaude/core/HOW-WE-WORK.md:252` | delete the "Localization review" outcome row |
| `src/superclaude/core/HOW-WE-WORK.md:383` | delete the `localization-review` routing row |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:252,383` | byte-for-byte copy of the source file after the edit (CLAUDE.md rule) |
| `src/superclaude/core/WORKER-CONTRACT.md:330` | "15 commands converted in P2" becomes 14; remove `review-translation` from the list |
| `src/superclaude/core/WORKER-CONTRACT.md:334` | "the five P2 commands" becomes four (name list drops `/sc:review-translation`); "so it has 17 rows" becomes 16 |
| `src/superclaude/core/WORKER-CONTRACT.md:350` | delete the `/sc:review-translation` table row |
| `src/superclaude/core/CLAUDE.md` | no mention; the level table is unchanged, so no re-copy needed (verify with the routing test) |

## C. Edit: tests

| Path:line | Change |
|---|---|
| `tests/skills/test_worker_contract.py:504` | remove from `P2_COMMANDS` |
| `tests/skills/test_worker_contract.py:679-690` | remove the `UNATTENDED_EXPECT["review-translation"]` entry |
| `tests/skills/test_worker_contract.py:1006` | remove from `P2_NEW_BRIEF_ROWS` |
| `tests/skills/test_worker_contract.py:1668-1676` | P2 count 15 becomes 14 (message too); `UNATTENDED_EXPECT` size 31 becomes 30 |
| `tests/skills/test_worker_contract.py:1814-1824` | remove the two `review-translation` gate-resolution tuples |
| `tests/core/test_how_we_work_routing_table.py:~58` | comment on stable row ids: note `localization-review` left in 6.0.0 |
| `tests/core/test_how_we_work_routing_table.py:86` | remove `localization-review` from `_EXPECTED_IDS` |
| `tests/core/test_how_we_work_routing_table.py:305` | remove `sc:review-translation` from the "not in other commands" set |
| `tests/core/test_how_we_work_routing_table.py:672-683` | remove the S07 tuple |
| `tests/core/test_how_we_work_routing_table.py:836,850-855` | docstring drops S07; remove the `localization-review` assertions |
| `tests/recommend/fixtures/routing_refresh_cases.json:32-33` | remove fixture inputs `source-strings` and `locale-files` (only S07 uses them) |
| `tests/recommend/fixtures/routing_refresh_cases.json:175-~195` | remove case S07 (like S27 for `/sc:spawn`) |
| `tests/recommend/fixtures/routing_refresh_cases.json:762` | keep: frozen 47-command record, as with spawn |
| `tests/recommend/test_routing_refresh.py:3` | docstring: S07 retired too |
| `tests/recommend/test_routing_refresh.py:35` | `_POST_REFRESH_REMOVALS = {"spawn", "review-translation"}` and its comment |
| `tests/recommend/test_routing_refresh.py:139` | case ids skip 7 and 27 |
| `tests/unit/test_cli_install.py:118` | remove `review-translation.md` from the expected command list |
| `tests/unit/test_cli_install.py:288` | remove `sc-review-translation-protocol/SKILL.md` from the expected skill list |

## D. Edit: docs

| Path:line | Change |
|---|---|
| `docs/user-guide/commands.md:95` | delete the table row |
| `docs/user-guide/commands.md:587-615` | delete the whole `/sc:review-translation` section and its closing rule |
| `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:976` | 31 converted becomes 30 (16 from phase 1, 14 from phase 2) |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1315` | drop `review-translation` from the 22-command list (21) |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1840` | five P2 rows becomes four; 15 P2 names becomes 14; 31 becomes 30 in the same sentence; row count words |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1989` | "five P2 rows (...)" becomes four, drop the name |
| `docs/generated/contributor-knowledge-base/architecture-guide.md:261` | remove the skill list line |
| `docs/generated/contributor-knowledge-base/components-guide.md:188` | remove the list line |
| `docs/generated/contributor-knowledge-base/visual-architecture-summary.md:28,308,320,446-478,606` | drop the TOC entry, nodes C7/S7 (renumber), the family section's bullet and `Translation` subgraph, retitle the section, drop the name from line 606 |

## E. Counts that were already stale (not changed here)

`docs/developer-guide/technical-architecture.md:43` (45 commands), `docs/getting-started/upgrading.md:85`
(45 commands, 38 skills), `PROJECT_INDEX.*` and the dated snapshot counts of "31 converted commands" in
`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (lines 196, 290, 317, 710, 745,
957, 1309, 1319, 1355, 1958, 2197, 2203, 2230, snapshot of 2026-11-12). Disk has 46 commands and 40
skills before this PR, so those numbers were already out of date; the `/sc:spawn` removal left them
alone and so does this PR. They are for the release's docs pass.

## F. Leave alone (historical records and task records)

`.dev/**` (including `.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-*`), `docs/releases/`,
`docs/testing/v5.0.0/`, `docs/designs/`, `CHANGELOG.md`, the frozen record line
`tests/recommend/fixtures/routing_refresh_cases.json:762`, and the architecture-record hits under
`docs/architecture/` that are not in section D.

## G. Not affected (checked)

Install code (`src/superclaude/cli/install*.py`) copies by directory scan and has no name list;
hooks (`launch-level-guard.sh` etc.) do not name it; `.claude-plugin/`, `package.json` and
`pyproject.toml` do not name it; `Makefile` `translate` target is about README translation and is
unrelated; swarm and everything in "Kept for now" is untouched.
