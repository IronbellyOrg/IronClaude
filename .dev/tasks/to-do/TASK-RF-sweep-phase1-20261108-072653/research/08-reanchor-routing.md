# Research: Re-anchor after fast-forward (routing and CLI side)

**Status:** Complete
**Date:** 2026-11-08
**Base:** e8db2fe6 -> 5dc29d23

---

## 1. What changed in the seven files (git diff e8db2fe6 5dc29d23)

| File | Change | Effect on line numbers |
|---|---|---|
| `src/superclaude/core/HOW-WE-WORK.md` | 2 lines rewritten in place: line 65 (spec-panel step) and line 329 (`/sc:issue` row, #422/#434 claim pipeline) | None. No line added or removed. |
| `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Same 2 lines | None |
| `src/superclaude/cli/main.py` | +4 lines at 562-565: `issue_watch_group` deferred import (563) and `main.add_command(issue_watch_group, name="issue-watch")` (565) | Everything after old 561 moves down 4. `if __name__ == "__main__":` 564 -> 568. File 565 -> 569 lines. |
| `CHANGELOG.md` | +1 line at 139, 1 line rewritten at 147 | Lines 1-138 unchanged |
| `docs/user-guide/commands.md` | Line 115 rewritten in place; all other hunks from line 348 onward | Lines 1-347 unchanged |
| `tests/pr_submit/test_conflict_scripts.py` | +158 lines appended at 1829-1986 | Lines 1-1828 unchanged |
| `tests/unit/test_cli_install.py` | Line 145 rewritten in place | None |

## 2. Citation table

Statuses: CONFIRMED (same text, same line), MOVED (same text, new line), CHANGED (text differs).

### 2.1 `src/superclaude/cli/main.py`

| Citing file:line | Old path:line | New path:line | Status | Note |
|---|---|---|---|---|
| research/05-test-verification.md:58 | main.py:519-561 (registration block) | main.py:519-565 | CHANGED | Block now ends with the `issue-watch` pair, not `reflect`. |
| research/01-file-inventory.md:221 | main.py:559 reflect import | main.py:559 | CONFIRMED | |
| research/01-file-inventory.md:221 | main.py:561 `main.add_command(reflect_group, name="reflect")` | main.py:561 | CONFIRMED | No longer the last pair. |
| research/01-file-inventory.md:221 | main.py:564 `if __name__ == "__main__":` | main.py:568 | MOVED | |
| research/01-file-inventory.md:221 | "File is 565 lines" | 569 lines | CHANGED | |
| research/01-file-inventory.md:228 | main.py:547-549 swarm, :551-553 recommend | same | CONFIRMED | |
| research/01-file-inventory.md:324 | "after line 561" | after main.py:565 | CHANGED | Insertion point moves past `issue-watch`. |
| research/02-patterns-conventions.md:12 | main.py:551-553, 559-561 ("the last pair"), 564 | 551-553 and 559-561 CONFIRMED; last pair is now 563-565; `if __name__` at 568 | CHANGED | "reflect is the last pair" is no longer true. |
| research/02-patterns-conventions.md:13 | main.py:519 comment, repeated through 559 | 519, repeated through 563 | CHANGED | Comment text identical; one more occurrence at 563. |
| research/02-patterns-conventions.md:15 | main.py:551, :531 | same | CONFIRMED | |
| research/02-patterns-conventions.md:16 | main.py:559 | 559 | CONFIRMED | |
| research/02-patterns-conventions.md:17 | "append after main.py:561" | after main.py:565 | CHANGED | |
| research/02-patterns-conventions.md:151 | "after main.py:561"; pattern 551-561 | after 565; pattern 551-565 | CHANGED | |
| research/02-patterns-conventions.md:165 | "after :561" | after :565 | CHANGED | |
| docs/designs/orchestrator-mode.md:28 | 519-561; last pair reflect (559, 561); `if __name__` 564 | 519-565; last pair issue-watch (563, 565); `if __name__` 568 | CHANGED | |
| docs/designs/orchestrator-mode.md:915 (step 1.7) | "after line 561" | after line 565 | CHANGED | |
| docs/designs/orchestrator-mode.md:951 (rollback row) | "after line 561" | after line 565 | CHANGED | |

`issue_watch` imports from the `cli` module directly (`from superclaude.cli.issue_watch.cli import issue_watch_group`), like `reflect.commands`, not through the package `__init__`.

### 2.2 `src/superclaude/core/HOW-WE-WORK.md`

| Citing file:line | Old path:line | New path:line | Status | Note |
|---|---|---|---|---|
| research/01-file-inventory.md:238; research/03-integration-points.md:64; design:694 | :318 `<!-- other-commands:v1 -->`, :320-321 header, :337 `<!-- /other-commands -->` | same | CONFIRMED | |
| research/01-file-inventory.md:239; research/03-integration-points.md:64; design:694 | :333 `/sc:spawn` row; :335 closing prose | same | CONFIRMED | R1 still goes at new line 334. |
| research/01-file-inventory.md:240; design:695 | :396 `## Orca coordination` | 396 | CONFIRMED | |
| research/01-file-inventory.md:241; design:695 | :403 never-workers bullet; :404 "Orca creates the worktrees" | same | CONFIRMED | Bullet text unchanged. |
| research/01-file-inventory.md:338 | "after 333 (R1), after 403 (R2)" | same | CONFIRMED | R2 shifts to after 404 once R1 lands (already noted at 01:354). |
| (not cited by line) | :329 `/sc:issue` row | 329 | CHANGED | Now says the claim "creates an Orca worktree and launches an agent in it at the `--pipeline` level ... and never merges". No research citation depends on its text. |

### 2.3 `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`

| Citing file:line | Claim | Status |
|---|---|---|
| research/01-file-inventory.md:247 | `cmp` against src guide: IDENTICAL | CONFIRMED (re-run on 5dc29d23: IDENTICAL) |
| research/03-integration-points.md:66; design:696 | byte copy checked by `test_routing_plugin_parity.py:38` | Copy relationship CONFIRMED; the test file is outside this re-anchor's file list |

### 2.4 `docs/user-guide/commands.md`

| Citing file:line | Old path:line | New path:line | Status | Note |
|---|---|---|---|---|
| research/01-file-inventory.md:264; research/03-integration-points.md:69; design:699 | :105 `### 8. UTILITIES`; :107-108 header | same | CONFIRMED | |
| research/03-integration-points.md:69 | :109-118 row range | same | CONFIRMED | |
| research/01-file-inventory.md:265; research/03-integration-points.md:69; design:699 | :115 `/sc:issue` row | 115 | CHANGED | Purpose cell now "Claim a GitHub issue (assign, accuracy check, summary, next-step prompt, then an Orca worktree and a launched agent) or create a templated issue". Position unchanged. |
| research/01-file-inventory.md:265; research/03-integration-points.md:69 | :116 `/sc:recommend` row | 116 | CONFIRMED | |
| research/01-file-inventory.md:341 | "after line 115" | after line 115 | CONFIRMED | |

### 2.5 `CHANGELOG.md`

| Citing file:line | Old path:line | New path:line | Status | Note |
|---|---|---|---|---|
| research/01-file-inventory.md:275; research/03-integration-points.md:71; design:701 | :5 `## [Unreleased]` | 5 | CONFIRMED | |
| research/01-file-inventory.md:275; research/03-integration-points.md:71 | :7 `### ccsession: a shim never forwards to another shim` | 7 | CONFIRMED | |
| research/01-file-inventory.md:275; research/03-integration-points.md:71 | :9 `#### Fixed (...)`, :19 `#### Added (...)` | same | CONFIRMED | |
| research/03-integration-points.md:71 | :33 ... :131 further `#### Added (...)` headings | same | CONFIRMED | Diff touches only lines 138 onward. |
| research/01-file-inventory.md:343 | "under line 5" | under line 5 | CONFIRMED | |

### 2.6 `tests/pr_submit/test_conflict_scripts.py`

| Citing file:line | Old path:line | New path:line | Status |
|---|---|---|---|
| research/05-test-verification.md:60 | :60-64 `_base_env`, `env["HOME"] = str(home)` at 63 | same | CONFIRMED |
| research/05-test-verification.md:91 | :48-64 `_FIXED_IDENTITY` and `_base_env` | same | CONFIRMED |
| research/05-test-verification.md:92, :121 | :46 `GIT = shutil.which("git")`; :88-91 module `pytestmark` skipif | same | CONFIRMED |

Note for 05:92: the module `pytestmark` at 88-91 skips on `not _merge_tree_works()` (git, jq, bash and `merge-tree --write-tree`), not on git alone. That was already true on the old base.

### 2.7 `tests/unit/test_cli_install.py`

| Citing file:line | Old path:line | New path:line | Status |
|---|---|---|---|
| research/03-integration-points.md:100 | :53 `_PACKAGE_RESOURCES = {` | 53 | CONFIRMED |
| research/03-integration-points.md:100 | `_assert_present` :502-505 (def at 501) | same | CONFIRMED |

The only change (line 145) adds `scripts/require-orca-worktree-agent.sh` to the hooks baseline list; no citation depends on it.

## 3. Requested facts

**(a) New anchors for R1, R2, R6, R8**

- R1: other-commands table `src/superclaude/core/HOW-WE-WORK.md:318` (open marker) to `:337` (close marker), header `:320-321`; `/sc:spawn` row `:333`. Insert the sweep row at new line 334. Unchanged from the old base.
- R2: `## Orca coordination` at `HOW-WE-WORK.md:396`; never-workers bullet at `:403`; next bullet "Orca creates the worktrees" at `:404`. Unchanged. After R1 lands these become 397, 404 and 405.
- R6: `docs/user-guide/commands.md:105` `### 8. UTILITIES`; `/sc:issue` row at `:115` (text changed, position same); `/sc:recommend` at `:116`. Insert after 115.
- R8: `CHANGELOG.md:5` `## [Unreleased]`. Heading style unchanged: a topic heading `### <title>` (first one at `:7`) with `#### Fixed (<topic>)` and `#### Added (<topic>)` sub-headings (`:9`, `:19`). There is still no bare `### Added` under `[Unreleased]`.

**(b) Byte identity.** `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing and exits 0: IDENTICAL on 5dc29d23.

**(c) Deferred-registration insertion point.** The last deferred `add_command` is now `src/superclaude/cli/main.py:565` `main.add_command(issue_watch_group, name="issue-watch")`, with its import at `:563`. `if __name__ == "__main__":` is at `:568`. The sweep pair goes after line 565 (blank line 566), not after 561. Every "after line 561" in the design (lines 28, 915, 951) and the research (01:324, 02:12, 02:17, 02:151, 02:165) should read "after line 565".

**(d) Does master already mention a sweep?** No. A case-insensitive grep of the current `HOW-WE-WORK.md` for `sweep`, `wake` and `poll` finds nothing. The only #422/#434 change in the guide is the `/sc:issue` row at `:329` ("then creates an Orca worktree and launches an agent in it at the `--pipeline` level ... and never merges"), which says nothing about a coordinator sweep or wake. The `## Orca coordination` section (396-405) is byte-identical to the old base. R2 ("The coordinator sweeps on every wake") does not duplicate anything on master.

## Summary

- Only `cli/main.py` shifted: #447 added the `issue-watch` pair at 563-565, so the sweep registration goes after line 565 (not 561) and `if __name__` is now at 568. Eleven citing lines (design 28, 915, 951; research 01:221, 01:324, 02:12, 02:13, 02:17, 02:151, 02:165, 05:58) need that update.
- Every HOW-WE-WORK, commands.md, CHANGELOG, test_conflict_scripts and test_cli_install anchor is CONFIRMED at the same line. The rows at HOW-WE-WORK:329 and commands.md:115 (`/sc:issue`) changed text in place, which affects no R1-R8 anchor.
- The plugin HOW-WE-WORK copy is still byte-identical, and master has no sweep or wake text, so R1, R2, R6 and R8 can land as designed.
