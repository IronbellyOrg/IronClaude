# QA Report - Routing rows lens (R1 to R8)

**Topic:** Routing and documentation rows R1 to R8 of revised DESIGN section 9
**Date:** 2026-11-12
**Phase:** docs gate, routing-rows lens (T293)
**Reviewer stance:** adversarial, fix_authorization false (report is the only file written)

## Verdict

Verdict: PASS (no BLOCKING or MAJOR finding; 2 MINOR notes, see Findings). Blocking count: 0 (restated at the end).

Source of truth for R1 to R8: `docs/designs/orchestrator-mode.md:713-722` (the revised DESIGN section 9, read now from disk). Working tree is uncommitted (nothing staged for these files); `git diff` was used for every change.

## Per-row findings

| Row | File and position (read now) | Text vs DESIGN | Checking test | Result |
|---|---|---|---|---|
| R1 | `src/superclaude/core/HOW-WE-WORK.md:334`, inside `<!-- other-commands:v1 -->` (318) to `<!-- /other-commands -->` (338), directly after the `/sc:spawn` row (333) | Byte-for-byte equal to the DESIGN R1 quoted text (script compare in /tmp, True) | `tests/core/test_how_we_work_routing_table.py::test_other_commands_membership_and_live_references` (lines 292-312); removing the row in a private copy makes it fail (C17) | PASS |
| R2 | Same file, `:405`, in `## Orca coordination` (397), directly after the never-workers bullet (404) and before the Orca-creates-worktrees bullet (406) | Byte-for-byte equal to the DESIGN R2 quoted text (script compare, True), including the owner-approved "at most once every 5 minutes, beside \"The sweep.\"" wording | DESIGN names "R1 test plus parity test"; neither reads the bullet (C17: removing it leaves 79/79 passing) | PASS with MINOR-1 |
| R3 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`: `cmp` prints nothing; both files have git blob `a8a8fa7b9`; diff is the same 2 insertions | Byte-identical to the R1+R2 result | `tests/commands/test_routing_plugin_parity.py:38`; the file passes (5 tests) | PASS |
| R4 | `tests/core/test_how_we_work_routing_table.py:34` (`"sc:sweep",` after `"sc:spawn"` at 33; set opens at 27) | One insertion, nothing else | itself; removing it in a private copy makes the membership test fail (C17) | PASS |
| R5 | `tests/recommend/test_routing_refresh.py:33` `{"graph", "impact", "issue", "sweep"}` | Exact set from DESIGN | itself, assertion at line 648 (`shipped - _POST_REFRESH_ADDITIONS == active`); 332 tests in the three routing files pass | PASS with MINOR-2 |
| R6 | `docs/user-guide/commands.md:116` in `### 8. UTILITIES` (105), after the `/sc:issue` row (115) and before `/sc:recommend` (117) | Four cells equal to DESIGN R6 | manual review (per DESIGN); no forbidden word | PASS |
| R7 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:991` | List now `agent, git, help, issue, pm, spawn, sweep and swarm-wizard`, the same order as `src/superclaude/core/WORKER-CONTRACT.md:23` | manual review against contract line 23: equal | PASS |
| R8 | `CHANGELOG.md:7` `### sweep: read-only supervision snapshot (Phase 1)`, `:9` `#### Added (sweep)`, under `## [Unreleased]` (5), before `### ccsession...` (17) | Names `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-16 and `.dev/sweeps/` ignored | manual review; claims match the tree (WC-16 at `WORKER-CONTRACT.md:275`, 5-minute cap in `sweep.md:20`) | PASS |

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | R1 row exists at the DESIGN position with DESIGN text | PASS |
| C2 | R2 bullet exists at the DESIGN position, byte-equal to DESIGN row R2 (plan item 13.1 pin) | PASS |
| C3 | R2 text agrees with WC-16 (`WORKER-CONTRACT.md:277`) and "The sweep." (`:110`): same pass, adds to and does not replace, read-only, never a worker | PASS |
| C4 | R2 has a checking test that would fail on removal or rewording | FAIL (MINOR-1; the DESIGN itself names no test that reads the bullet) |
| C5 | R3 plugin copy byte-identical (`cmp`) | PASS |
| C6 | Parity test passes | PASS |
| C7 | R4 `"sc:sweep"` in `_OTHER_COMMANDS` and the membership test fails without it | PASS |
| C8 | R5 set equals `{"graph","impact","issue","sweep"}` and the refresh test passes | PASS |
| C9 | R6 row position, four cells, text | PASS |
| C10 | R7 list text and order equal contract line 23 | PASS |
| C11 | R8 heading, sub-heading, five required contents | PASS |
| C12 | Level table untouched: `git diff -U0` of the guide has only hunks at lines 334 and 405 (level table is lines 7-31 of section 1); `src/superclaude/core/CLAUDE.md` has no change in `git status` | PASS |
| C13 | No row removed or reworded: the only deleted lines in the 8 files are the R5 set line and the R7 list line, both edits DESIGN prescribes | PASS |
| C14 | R1 and R6 rows contain none of stop, retry, release, merge, removal (`grep -niwE`, no hit) | PASS |
| C15 | No `.claude/` path changed; no `WC-14` in CHANGELOG or `.gitignore` additions | PASS |
| C16 | `uv run pytest tests/core/test_how_we_work_routing_table.py tests/commands/test_routing_plugin_parity.py tests/recommend/test_routing_refresh.py`: 332 passed; `tests/commands/test_sweep_command.py`: 115 passed; `ruff check` clean and `ruff format --check` clean on the two edited test files | PASS |
| C17 | Mutation on private /tmp copies (deleted afterwards): without R1 the membership test fails; without the R4 entry it fails; without R2 all 79 tests still pass | PASS (R1, R4 caught); confirms C4 |
| C18 | Bounded style contract (`src/superclaude/output-styles/pragmatic.md:22` now carries the scoped sweep exception; the unqualified "No exceptions" is gone; the other table rules say "Except for the sweep chat-summary exception above") consistent with the sweep summary-only reply; no routing row contradicts it | PASS |
| C19 | `.gitignore:256` `.dev/sweeps/` ignored and `.dev/tasks/` not ignored (`git check-ignore` exit 0 and 1) | PASS |

## Findings

| Id | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| MINOR-1 | MINOR | `docs/designs/orchestrator-mode.md:716` ("Checked by": "R1 test plus parity test"); `tests/core/test_how_we_work_routing_table.py:292-312`; `tests/commands/test_routing_plugin_parity.py:38` | No test reads the R2 bullet. Deleting or rewording it in both guide copies leaves every test green (C17). The text is held only by plan item 13.1 and this review. | Optional: one assert in `test_how_we_work_routing_table.py` that the guide holds `The coordinator runs `/sc:sweep` on every wake`. Not required by DESIGN. |
| MINOR-2 | MINOR | `tests/recommend/test_routing_refresh.py:28-31` | The comment above `_POST_REFRESH_ADDITIONS` still lists only issue #323 and #302; it does not say that `sweep` was added. | Add "and issue #339 adds /sc:sweep" to the comment. |

No BLOCKING or MAJOR finding. Experiments changed no repository file; the report is the only file written (`git status` shows no change beyond the pre-existing set).

Verdict: PASS

Blocking count: 0
