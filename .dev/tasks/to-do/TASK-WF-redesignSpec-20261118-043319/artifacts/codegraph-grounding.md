# Codegraph grounding: TASK-WF-redesignSpec-20261118-043319

## Run state

- index_state: not fresh. `codegraph_status` reported 3835 files indexed, 0 changes since index, but "Pending resolution: 160192 references from an interrupted index run; some caller/impact edges are missing".
- checked_at: 2026-11-18 (session start, Wave 1 step 0)
- worktree_root: the issue-606 worktree (this checkout)
- projectPath: the issue-606 worktree
- access mode: MCP tool `codegraph_status`
- token: graph:partial-index. Caller and impact edges are not trusted, so Grep, Glob and Read did every lookup below (permanent floor, normal evidence).

## Resolved symbols

Verified by Grep and Read on this branch (observer package is `src/superclaude/cli/observe/`):

- `terminal.py`: `GLYPHS` (line 30), `resolve_policy` (73), `make_console` (110); line 121 reads `color_system=None if policy.no_color else "standard"`.
- `commands.py`: `QUESTION_GATE_PASSED` (67), `QUESTION_LINK_PASSED` (70), `run_once` with `console.export_text()` (242), `class LiveScreen` (257) with `draw` and the `shape` tuple (265).
- `render.py`: `wrap` (62), `_pad` (83), `counts_lines` (94), `_columns` (155), `_row_line` (233), `_header_lines` (246), `_help_lines` (304), `_question_line` (311), `_desk_lines` (329), `_panel_lines` (359), `screen_lines` (390), `render` (524).
- `view.py`: `DESK_TITLE` (85), `DESK_TEXT_LINES` (99), `UNAVAILABLE` (100), `FROZEN_MARKER` (106), `RowView` (158), `QuestionLine` (206), `DeskView` (229), `counts_line` (761), `QUESTIONS_COUNT_LABEL` (70). `parse.py`: `ASK_CAP` (475).
- `pyproject.toml:41` declares `pexpect>=4.9`.
- `observe` is registered in `src/superclaude/cli/main.py` (line 582).

Not on this branch (verified absent): `.dev/issues/409/visual-parity/inputs/` (so `render_current.py` and the baseline captures do not exist here). Present: the three mockup PNGs in `.dev/issues/409/attachments/`, `.dev/issues/409/orca-observer-design-package.zip`, `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`.

## Dependents

Files that mention each changed symbol (Grep, file level; not call-site confirmed):

- `resolve_policy`: `commands.py`, `terminal.py`; tests `test_question_cap.py`, `test_render.py`, `test_terminal.py`, `release1_surface.py`, `conftest.py`, `test_export.py`, `test_commands.py`, `test_linkoff_screen_reference.py`, `test_golden_contract.py`.
- `make_console`: `commands.py`, `terminal.py`; tests `test_render.py`, `test_terminal.py`, `release1_surface.py`, `test_fixtures.py`, `conftest.py`.
- `screen_lines`: `render.py`; tests `test_question_cap.py`, `test_render.py`, `release1_surface.py`, `test_inspector_scroll.py`, `test_export.py`, `test_linkoff_screen_reference.py`, `test_golden_contract.py`.
- `TerminalPolicy(`: constructed only in `terminal.py`.
- `GLYPHS`: `terminal.py`, `test_terminal.py`. `glyph(`: `render.py`, `terminal.py`, `test_terminal.py`.
- `counts_lines`, `_desk_lines`, `_panel_lines`: `render.py` only.
- `_question_line`: `render.py`, and the same name also appears in `export.py`, `test_export.py`, `test_commands.py`, `test_render.py`; read each before editing, it may be a different function in `export.py`.

## Pre-check

Wave 4 pre-check (Grep and Read floor, no codegraph):

- Existing files and symbols the tasks name resolve: all `OBS/` modules, `tests/observe/` files and goldens, `pexpect` in `pyproject.toml`, `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED`, `LiveScreen`, `run_once`, `resolve_policy`, `make_console`, `GLYPHS`, the `render.py` builders and the `view.py` constants.
- Files named but absent by design (created by a task): `OBS/theme.py`, `tests/observe/test_theme.py`, `test_styled_capture.py`, `test_height_budget.py`, `test_live_screen_pty.py`, `live_child.py`, `golden_release1_records.json`, and everything under `.dev/issues/409/visual-parity/` except `REDESIGN-SPEC.md`.
- Gap found: `.dev/issues/409/visual-parity/inputs/tools/render_current.py` does not exist on this branch although spec step 0.1 edits it; Task 1 rebuilds it.
- Dependents of touched symbols that no task names: `tests/observe/test_fixtures.py` (calls `make_console`) and `tests/observe/test_golden_contract.py` (calls `resolve_policy` and `screen_lines`) are covered only through "full suite green"; Task 5 and Task 27 name `test_golden_contract.py`, `test_fixtures.py` is unnamed.
- Count: 30 tasks, 8 phases; 1 gap, 1 unnamed dependent, 0 unresolved symbols.
