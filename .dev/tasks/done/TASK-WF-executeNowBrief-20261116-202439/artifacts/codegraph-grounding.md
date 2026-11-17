# Codegraph grounding: TASK-WF-executeNowBrief-20261116-202439

## Run state

- index_state: fresh
- checked_at: 2026-11-16T20:24:39Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp
- access: mcp (codegraph_status answered "Changes since index: 0 added, 0 modified, 0 removed"; 3148 files indexed)
- degraded tokens: none
- Method note: the plan's targets are small private helpers, constants and test lines in one package. The lookups below were made with Grep and Read (the permanent floor) because a name-level Grep answers "who uses this name" for these module-private names more directly than a call-edge row; graph rows are leads only.

## Resolved symbols

All paths repo-relative under src/superclaude/cli/observe/ (PKG) and tests/observe/ (TESTS). Line numbers read live on 2026-11-16 at HEAD f104ca51a.

- terminal.py: `from rich import box` (:18), `from rich.style import Style` (:21), `PALETTE` (:42), `_FORBIDDEN_ATTRS` (:45), `TerminalPolicy.box_style` (:73-74), `palette_style` (:161). Only users: TESTS/test_terminal.py (:20 import, :57-59, :73-82, :126).
- adapter.py: `CODES` (:66); the only other mentions are the comment at :340 and TESTS/test_adapter.py:719.
- parse.py: `Fixture.parse` (:723-733, calls `parse_page` then `apply_frozen`); `apply_frozen` (:736) is also used by collector.py:297, so it stays. Only callers of `Fixture.parse`: TESTS/test_fixtures.py:44, :141, :149.
- questions.py: `CLOSURE_EVIDENCE` (:25), `QuestionState.closure_evidence` (:71), `QuestionState.never_read` (:75). Only users: TESTS/test_questions.py:46, :52, :98.
- commands.py: `Deps.extra` (:142, the only use of `field` in the file; import at :14). `extra=` is passed nowhere in src or tests/observe (the `extra=1` hits in test_snapshot_schema.py:152-154 are dict updates, not `Deps`).
- collector.py: `FixtureSource.__init__(variant, question_fixture)` (:97), `_question_fixture` (:103), `_question_index`, `read_questions` (:128-142). Only caller passing `question_fixture=`: TESTS/test_collector.py:669. `commands.py:177-178` refuses `--questions` with `--fixture`, so production never reaches the replay.
- parse.py counters: `ParsedPage.unrecognised_keys` (:177), its sum (:409); `Coverage.unrecognised_keys` (:195), its sum (:647); per-row field (:155, :356) stays and is read at view.py:407 and TESTS/test_parse.py:188, :198, TESTS/test_fixtures.py:145, :166.
- view.py: `QuestionsPanel.count_text` (:209), assigned at :732 from `open_text`; `open_text` is also used at :693 and :718, so it stays. No test or other module reads `count_text`.
- export.py: `SCHEMA` (:29), `Draft7Validator` import (:18), `resources` import (:14), `SCHEMA_PACKAGE` and `SCHEMA_FILE` (:24-25), `check_schema` call (:32). `SCHEMA_VERSION` (:23) stays (used at :195). Readers of `export.SCHEMA`: TESTS/test_commands.py:34 and TESTS/test_snapshot_schema.py:15 only. Tests import helpers with `from tests.observe.conftest import ...` (tests/observe has an `__init__.py`).

## Dependents

- Tests that must keep passing unchanged: TESTS/test_render.py:182-190 (no blink on the real screen), :616-629 (questions-off golden), TESTS/test_terminal.py:142-149 (ASCII `safe_box`), TESTS/test_adapter.py:718 (exact error code), TESTS/test_question_cap.py:71-134 (panel), TESTS/test_view.py and TESTS/test_render.py (panel and inspector text), TESTS/test_snapshot_schema.py closed-object checks, TESTS/test_fixtures.py:185-191 (leak scan over every fixture).
- Files two tasks both touch (so the tasks are ordered): parse.py and TESTS/test_fixtures.py (Task 3, Task 6); commands.py (Task 4, Task 10); prd.md (Task 10, Task 11).

## Pre-check

Advisory, read-only, run after the quick gate passed (Grep, Glob and Read; no second readiness check).

- Files: every file the 12 tasks name exists (src/superclaude/cli/observe/{terminal,adapter,parse,questions,commands,collector,view,export}.py; tests/observe/{test_terminal,test_adapter,test_fixtures,test_questions,test_collector,test_parse,test_view,test_render,test_snapshot_schema,test_commands,test_question_quiet_scope,test_golden_contract,test_question_cap,test_registration,conftest}.py; the SPECDIR documents, prd.md and the two owner records).
- Symbols: all names the tasks delete resolve at the cited lines (PALETTE, _FORBIDDEN_ATTRS, palette_style, box_style, CODES, Fixture.parse, closure_evidence, never_read, CLOSURE_EVIDENCE, Deps.extra, question_fixture, the aggregate unrecognised_keys fields, count_text, the SCHEMA load). `apply_frozen` and `parse_page` stay.
- Correction made while checking: in tests/observe/test_terminal.py the forbidden-styles test runs 5 cases and the no-blink test 2, so Task 1 expects 9 fewer passed cases (not 5). In acceptance-tests.md, T7 and T17 are defined inside the AC-3 and AC-6 mapping rows (lines 25 and 28), not as table rows, and the snapshot schema section is at about line 64; Task 12 was reworded to match.
- Dependents no task names (reported, none blocks): `glyph("selected"|"truncate"|"hrule")` in render.py (:124, :139, :241) and terminal.py:187 stay untouched because only the glyph names sep, vrule and cross are removed; `tests/observe/test_golden_contract.py` and `record_golden_questions.py` do not call `Fixture.parse` (Grep: only test_fixtures.py does).
- Unverified until execution: the exact passed-count change of Tasks 2 to 8 (the plan expects none) and whether removing the `Style` and `box` imports leaves any other use in terminal.py (Task 1 greps first).
