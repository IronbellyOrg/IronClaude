# Codegraph grounding, TASK-WF-phase3OfTheOrcaT-20261117-061534

## Run state

- index_state: fresh (status answer: 3829 files, "Changes since index: 0 added, 0 modified, 0 removed")
- access: mcp (codegraph_status, codegraph_search, codegraph_node, codegraph_callers, codegraph_callees, codegraph_impact, codegraph_files listed)
- checked_at: 2026-11-17T06:17:54Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp
- tokens: none (SUPERCLAUDE_CODEGRAPH_PRIMITIVES is unset)

## Resolved symbols

All read with `codegraph_node` outlines or file ranges, then confirmed by reading the ranges named in the tasks.

- src/superclaude/cli/observe/parse.py: `Question` (line 416, frozen dataclass; docstring says body, payload and to_handle are not kept), `ParsedQuestions` (438), `_QUESTION_FIELDS` (450), `parse_questions` (461), `Row.dispatch_id` and `Row.worktree_id` (fields from `_FIELDS`, lines 58 and 68), `UNKNOWN`, `ShapeError`.
- src/superclaude/cli/observe/questions.py: `QuestionRecord`, `QuestionState`, `merge_questions` (81); holds `Question` unchanged.
- src/superclaude/cli/observe/collector.py: `Collector.__init__` (135, kwargs `run_id`, `questions`), `Collector._question_fields` (203, the one caller of `parse_questions`), `CycleResult` question fields (56 to 68).
- src/superclaude/cli/observe/view.py: `Session` (114), `QuestionLine` (185), `QuestionsPanel` (196), `View` (251), `_questions_panel` (588), `build_view` (762), `apply_key` (992), `_move` (956), `KEYS_LINE` (87), `QUESTIONS_KEYS_LINE` (78), `INSPECTOR_HELP` (90).
- src/superclaude/cli/observe/render.py: `_panel_lines` (304), `screen_lines` (326, the questions-win-over-ledger height budget at lines 369 to 395), `_help_lines` (297).
- src/superclaude/cli/observe/export.py: `_question_lines` (89), `_questions_dict` (148), `snapshot_dict` (173).
- src/superclaude/cli/observe/commands.py: `QUESTION_GATE_PASSED` (67, one line pinned by a regex in tests/observe/test_commands.py), `_questions_on` (168), `run_loop` (calls `apply_key` at 268), `Session()` created at 222 and 280, `Collector(... questions=_questions_on(options))` at 355.
- src/superclaude/cli/observe/sanitize.py: `sanitize(text, mode)`.
- src/superclaude/cli/observe/snapshot.schema.json: `questions` group (line 65), description says no subject, body, handle or payload is ever exported.

## Dependents

- `parse_questions` (impact depth 1): `Collector._question_fields` only in src; tests in tests/observe/test_parse.py (including `test_no_parsed_object_keeps_a_body_payload_or_recipient` at line 586), tests/observe/test_view.py, tests/observe/test_snapshot_schema.py.
- `QuestionLine` (impact depth 1): `_questions_panel` in view.py; read in render.py `_panel_lines` and export.py `_question_lines`, `_questions_dict` (attribute access, not constructor calls).
- `apply_key` callers (13 found): commands.py `run_loop`; tests test_session.py, test_view.py, test_render.py, test_inspector_scroll.py.
- `Question` is also used by `QuestionRecord` in questions.py and by tests/observe/test_questions.py; `Collector` is used by 14 files (tests construct it with keyword arguments, so a new keyword with a default keeps them working).
- Golden pin to keep byte-identical: tests/observe/golden_release1_surface.json (R1 surface, questions off).
- Spec files that quote the old rule: .dev/issues/409/bmad/spec-orca-observer/adapter-contract.md line 41 ("body, payload and to_handle are not kept"), rendering-rules.md lines 50, 51 and 78 ("Lines are listed, not selectable"), snapshot-export-schema.md, unverified-register.md line 33, acceptance-tests.md (last row T56).

## Pre-check

Run after the gate passed (index_state fresh, no new readiness check). Advisory; the plan was not edited from it.

- Files named by tasks all exist: the seven observer modules under src/superclaude/cli/observe/, snapshot.schema.json, tests/observe/conftest.py, test_parse.py, test_deep_nesting.py, test_questions.py, test_commands.py, test_collector.py, test_golden_contract.py, test_registration.py, test_view.py, test_session.py, test_inspector_scroll.py, test_render.py, test_question_cap.py, test_export.py, test_snapshot_schema.py, golden_release1_surface.json, and the six spec files under .dev/issues/409/bmad/spec-orca-observer/.
- Symbols and lines resolve (read this run): `Question` parse.py:416, `parse_questions` parse.py:461, `Collector.__init__` collector.py:135, the `parse_questions` call collector.py:217, `Session` view.py:114, `QuestionLine` view.py:185, `View` view.py:251, `_questions_panel` view.py:588, `build_view` view.py:762, `apply_key` view.py:992, `QUESTIONS_KEYS_LINE` view.py:78, `_panel_lines` render.py:304, `screen_lines` render.py:326, `_question_lines` export.py:89, `_questions_dict` export.py:148, `snapshot_dict` export.py:173, `QUESTION_GATE_PASSED` commands.py:67, `_questions_on` commands.py:168, `run_loop` calling `apply_key` commands.py:268, `Collector(...)` commands.py:355; tests `test_no_parsed_object_keeps_a_body_payload_or_recipient` test_parse.py:586, `test_the_guard_is_true_only_with_a_cited_owner_record_that_exists` test_commands.py:746, `test_no_key_can_reach_the_adapter_or_collector` test_session.py:359.
- Task 4 builds `Row.worktree_id` text from `RowView.raw`; `Row.worktree_id` exists (parse.py:127).
- Dependents no task names, by design: tests/observe/release1_surface.py and record_golden*.py (recorders, untouched; the golden file they feed is pinned unchanged), tests/observe/test_fixtures.py (pins the fixture variant list, no fixture is added), tests/observe/test_terminal.py and test_sanitize.py (unaffected).
- Count: 7 tasks checked, 0 missing files, 0 unresolved symbols, 0 unnamed production dependents.
