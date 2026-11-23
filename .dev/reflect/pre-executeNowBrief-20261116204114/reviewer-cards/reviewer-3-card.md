---
reviewer: 3
persona: refactorer
model_class: opus
reviewer_model_self_report: claude-gw-tier1a (the brief lists model class opus)
---
# Reviewer 3 card (refactorer): Tasks 8, 9 and plan structure

F1 | MAJOR | blocking=true | unpassable-check | Task 5 | confidence 0.9
Claim: Task 5's check says Grep for question_fixture must find only the string no-question-fixture. It cannot pass: the same task renames the test to test_a_fixture_source_has_no_question_fixture (contains question_fixture) and the hyphenated code never matches the underscore pattern.
Citations: .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:69,72; tests/observe/test_collector.py:662; src/superclaude/cli/observe/collector.py:133

F2 | MAJOR | blocking=false | missing-requirement | whole plan | confidence 0.8
Claim: the plan drops two of the source's whole-package checks (run-use grep; git status --short); only the final test count survives, through the per-task gate. The run-use check guards a protected rule and Task 10 rewrites help text two lines above the "never runs run-use" sentence. Today the check passes with exactly 2 hits.
Citations: .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/source.md:49-53; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:15,23; src/superclaude/cli/observe/commands.py:87-90; src/superclaude/cli/observe/adapter.py:43

F3 | MINOR | blocking=false | other | Task 8 | confidence 0.75
Claim: followed literally, Task 8's import instructions fail the gate: replacing line 15 of test_snapshot_schema.py with "from tests.observe.conftest import SCHEMA" drops snapshot_json; both test files already import from tests.observe.conftest (test_commands.py:36, test_snapshot_schema.py:18) so a second line from the same module would probably fail import sorting [INFERRED: ruff would merge]; removing the self-comparison read leaves "from importlib import resources" (test_snapshot_schema.py:8) unused, which the plan does not say to remove.
Citations: .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:100; tests/observe/test_snapshot_schema.py:8,15,18,55-60; tests/observe/test_commands.py:34,36; pyproject.toml:185

F4 | MINOR | blocking=false | stale-reference | Task 8 | confidence 0.7
Claim: after Task 8 the design spine still says the schema is "checked with Draft7Validator.check_schema at import"; Task 8 removes that import-time check from production code and no task updates the line (the source's S2 row does not ask for it; noted only).
Citations: .dev/issues/409/bmad/spec-orca-observer/ARCHITECTURE-SPINE.md:142; src/superclaude/cli/observe/export.py:32-34

F5 | MINOR | blocking=false | other | Task 9 | confidence 0.7
Claim: after the T7 cut the two golden scan tests keep names that promise checks they no longer run (..._hold_no_path_handle_token_credential_url_or_escape_byte); Task 5 renames its test "so the name is true" but Task 9 does not apply the same standard.
Citations: tests/observe/test_golden_contract.py:207,509; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:69

F6 | MINOR | blocking=false | stale-reference | Tasks 6, 8, 9 | confidence 0.8
Claim: Task 3 adds a helper to test_fixtures.py, yet Tasks 6 and 9 still cite its pre-Task-3 lines (:145, :166, :185-191) although Task 6 lists Task 3 as a dependency; Task 8 cites the schema test as :52-72 and it is really :54-74. The plan calls line numbers leads, so impact is low.
Citations: .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:82,100,109,114; tests/observe/test_fixtures.py:139-151,185-191; tests/observe/test_snapshot_schema.py:54-74

F7 | MINOR | blocking=false | stale-reference | Task 12 | confidence 0.9
Claim: (T1 F4, confirmed and refined) Task 12 writes commands.py:177-178 into a design document; the number will be wrong when written: Task 4 deletes line 142, Task 10 rewrites :63-66 and :86-88 and can move lines again; Task 12 lists no dependency on Task 4 or Task 10.
Citations: src/superclaude/cli/observe/commands.py:142,177-178; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:123,143

F8 | MINOR | blocking=false | other | Task 1 | confidence 0.9
Claim: (T1 F5, confirmed) the "Palette table (CD-8)" comment at terminal.py:41 is not removed with PALETTE; the source range is :41-53.
Citations: src/superclaude/cli/observe/terminal.py:41-42; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:31; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/source.md:19

F9 | MINOR | blocking=false | other | Task 5 | confidence 0.9
Claim: (T1 F6, confirmed) the "SYNTHETIC question cycles" comment at collector.py:102 is left behind.
Citations: src/superclaude/cli/observe/collector.py:102-104; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:69

F10 | MINOR | blocking=false | stale-reference | Tasks 8, 12 | confidence 0.6
Claim: (T1 F7, refined) test_snapshot_schema.py:1 says "no ID assigned in acceptance-tests.md"; after Task 12 acceptance-tests.md names this file; Task 12 records the file path, not a T-number, so the docstring is arguably still literally true; Task 8 already edits this file and is the natural place to fix it.
Citations: tests/observe/test_snapshot_schema.py:1; .dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md:66; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:143

F11 | MINOR | blocking=false | other | Tasks 1, 9, 12 | confidence 0.7
Claim: (T1 F8, confirmed) the plan uses the debate-row labels T5, T7, T8, T9, which are also spec test ids in acceptance-tests.md; Task 12 then uses T7 to mean the spec test.
Citations: .dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md:24-25; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:107,143

Checked, no defect: T8 vacuous assertion: or True only at test_render.py:95-100; 27 cases = 3x3x3 (:80-82); footer starts with "shown x/y" (view.py:314) so the overflow pattern should match exactly one line. T5 deleted test: only test of the fake's own refusals; the observer argv is still guarded by test_question_quiet_scope.py:166-171, the fake's per-call assertions (:68-76) and test_adapter.py:158-192. T7 guard is real: test_golden_contract.py:21 imports SENSITIVE from test_fixtures (identical patterns); fixture_files() (test_fixtures.py:25-30) lists the fixtures package root (parse.py:687) where the goldens live; SENSITIVE used only at :21, :214, :518 so its import must go. Task 8: no production code reads SCHEMA; resources only at export.py:14,:30; test_export.py:239-243 unaffected; jsonschema stays in pyproject.toml:39. Task 5 retention: deleted assertion "second.questions is first.questions" (test_collector.py:678) is still covered at :568 and :600. Order: 3->6, 4->10, 10->11 and 7 before 9 correct; each task keeps the tree green. Task 1 count 1+5+1+2=9 correct. Not checked: whether pytest and ruff pass (could not run anything); the import-sorting failure in F3 is inferred from ruff rules.
