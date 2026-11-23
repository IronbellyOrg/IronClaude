---
reviewer: 1
persona: analyzer
model_class: sonnet
reviewer_model_self_report: claude-gw-tier1b[1m]
---
# Reviewer 1 card (analyzer): Tasks 1-7 against source.md

F1 | MAJOR | blocking=true | unpassable-check | Task 4 | confidence 0.95
Claim: acceptance criterion 1 of Task 4 (plan:63) requires Grep to find no closure_evidence or never_read in tests/observe; it cannot pass. The kept test test_nothing_is_ever_closed_and_closure_evidence_is_unavailable (tests/observe/test_questions.py:50) contains closure_evidence; Task 4 deletes only assertions at :46, :52, :98 and plan:65 forbids deleting a test function. tests/observe/test_view.py:174 test_a_released_row_without_an_outcome_never_reads_done_complete_or_settled contains the substring never_read. After :52 is deleted the first test's name claims a check it no longer makes. Refinement: plan:65 does not forbid a rename (Task 5 renames a test); fix by renaming the test or anchoring the grep on \.closure_evidence|\.never_read|CLOSURE_EVIDENCE.
Citations: .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:60,63,65; tests/observe/test_questions.py:46,50,52,98; tests/observe/test_view.py:174

F2 | MAJOR | blocking=true | unpassable-check | Task 5 | confidence 0.95
Claim: acceptance criterion 1 of Task 5 (plan:72) is wrong in both directions: the pattern question_fixture does not match the hyphenated code no-question-fixture, and it does match the renamed test test_a_fixture_source_has_no_question_fixture (plan:69). Correct pattern: \bquestion_fixture\b limited to src/superclaude/cli/observe plus _question_index and _question_fixture, or exclude the test name.
Citations: .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:69,72; tests/observe/test_collector.py:662,669; src/superclaude/cli/observe/collector.py:97,103,104

F3 | MAJOR | blocking=false | missing-requirement | whole package | confidence 0.9
Claim: source.md:49-53 has three whole-package acceptance checks (final pytest count = 694 minus removed tests; grep -rn "run-use" shows run-use only in the forbidden set and help text; git status --short shows only the named files). The plan has no final task or criterion for any; per-task gates cover pytest and ruff only. The only run-use mention is a keep-instruction in Task 10 (plan:123). The expected final count is never stated (reviewer computes 694 - 9 - 1 = 684).
Citations: .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/source.md:49-53; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:23,38,115,123

F4 | MINOR | blocking=false | stale-reference | Tasks 5, 12 (also 10) | confidence 0.9
Claim: commands.py:177-178 is correct today (if options.fixture: at :177, return at :178) but Task 4 deletes the Deps.extra line at :142, so the refusal moves to :176-177. Task 5 (plan:69) and Task 12 (plan:143) cite :177-178 as fixed; Task 12 writes the cite into a design document. Task 10's cites :63-66 and :86-88 stay put; :452-453 shifts.
Citations: src/superclaude/cli/observe/commands.py:142,177,178; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:60,69,123,143

F5 | MINOR | blocking=false | stale-reference | Task 1 | confidence 0.95
Claim: terminal.py:41 is the comment "# Palette table (CD-8): empty ..." above PALETTE at :42; the plan deletes :42 and :44-53 but not :41 although source.md:19 gives :41-53. Orphan comment remains.
Citations: src/superclaude/cli/observe/terminal.py:41,42,44-53; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:31

F6 | MINOR | blocking=false | stale-reference | Task 5 | confidence 0.9
Claim: collector.py:102 "# SYNTHETIC question cycles ..." is left behind (plan removes :103 and :104 only). The read_questions docstring at :131 "Replay the supplied synthetic question cycles..." is also stale.
Citations: src/superclaude/cli/observe/collector.py:102,103,104,131

F7 | MINOR | blocking=false | stale-reference | Tasks 8, 12 | confidence 0.85
Claim: tests/observe/test_snapshot_schema.py:1 says "no ID assigned in acceptance-tests.md"; Task 12 assigns the id and no task updates the docstring.
Citations: tests/observe/test_snapshot_schema.py:1; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:143

F8 | MINOR | blocking=false | other | Task 8 | confidence 0.6
Claim: tests/observe/test_snapshot_schema.py:15 is "from superclaude.cli.observe.export import SCHEMA, snapshot_json"; plan:100 says to change it to "from tests.observe.conftest import SCHEMA", which read literally drops snapshot_json. The executor must keep that import and move only SCHEMA.
Citations: tests/observe/test_snapshot_schema.py:15; .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:100

F9 | MINOR | blocking=false | other | Task 3 | confidence 0.7
Claim: the three callers need apply_frozen, which tests/observe/test_fixtures.py does not import (imports show only parse_page at :18); the plan does not mention adding the import; ruff would fail with F821 if missed.
Citations: tests/observe/test_fixtures.py:18,44,141,149; src/superclaude/cli/observe/parse.py:736

Not adopted: T1 F8 (label overlap) judged a clarity issue, not verified against acceptance-tests.md.

Checked, no defect (condensed): Task 1: box used only at terminal.py:73-74, Style only at :161-164; remaining imports still used; sep/vrule/cross appear nowhere else (render.py sep hits are a local variable); 9-case arithmetic 1+2+5+1; survivors exist (test_render.py:182-190, test_terminal.py:138-149). Task 2: CODES only at adapter.py:66, comment :340, test_adapter.py:719. Task 3: exactly three .parse( callers; apply_frozen and parse_page used at collector.py:293,297; Fixture.parse at parse.py:723-733. Task 4: CLOSURE_EVIDENCE only questions.py:25,:72; field( only commands.py:142; no extra= passed to Deps (test_commands.py:55,:238); view.py:65,:693 pinned by test_commands.py:668, test_render.py:453, test_export.py:280, test_view.py:941. Task 5: question_fixture= only test_collector.py:669; json and question_reply still used after deletion. Task 6: lines :177,:195,:409,:647 correct; unrecognised_keys only in parse.py, view.py, test_parse.py, test_fixtures.py; test_view.py:722 matches the label string, not the attribute. Task 7: count_text only view.py:209,:732; open_text at :693,:718; QuestionsPanel has 22 fields. Task 9 spot check: the T5 test is one non-parametrized test at test_question_quiet_scope.py:192-203.
