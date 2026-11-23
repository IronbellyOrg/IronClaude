# T1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/source.md` (53 lines)
Plan: `.dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md` (149 lines, 12 tasks)
Repository HEAD at audit: f104ca51a6e83aaae1c181963d8c7db6846dd4b6 (same as the plan's HEAD).
self_reported_confidence: 0.88

## Requirement extraction

Pass 1 (regex `R-|REQ-|SPEC-|T-` + digits): 0 parsed IDs (the source labels rows `R1`, `T5`, `D13` without a hyphen). parsed_count = 0.
Pass 2 (inferred, each row quote-pinned to source.md): 23 rows, inferred_count = 23. inferred_count > parsed_count, so `coverage_degraded: parsed-sparse` (Step 1B.2b).

## Coverage matrix (source -> plan)

| id | source quote (source.md:line) | matched plan item | method |
|---|---|---|---|
| INF-001 | "Scope is the eleven rows below and nothing else. No commit, no push, no pull request." (source.md:7) | plan Constraints, plan:20 | containment |
| INF-002 | "Never touch: the sanitizer (PKG/sanitize.py and its use), the argv allow-list and forbidden verbs in PKG/adapter.py ..." (source.md:8) | plan Constraints, plan:21 | containment |
| INF-003 | "Line numbers in the rows come from reviewers and are a lead only: re-grep every target in the live files right before editing" (source.md:9) | plan:22 | containment |
| INF-004 | "Gate after every task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` must pass (the baseline is 694 passed ...) and `uv run ruff check ...` must be clean." (source.md:10) | plan:23 and each task's acceptance | containment |
| INF-005 | "A step that fails its gate is reported as a finding; it is never loosened to pass." (source.md:11) | plan:23 | containment |
| INF-006 | "Plan edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`." (source.md:12) | plan:24 | containment |
| INF-007 | "Facts the debate found false in the earlier proposal (do not repeat them): R1 test ranges were too wide ..., R3 must not drop the five parsed row fields, T9 keeps the test_render copy ..." (source.md:13) | plan:25 | containment |
| INF-008 | "R1 ... Production: PKG/terminal.py:41-53 (`PALETTE`, `_FORBIDDEN_ATTRS`), :161-172 (`palette_style`) ..." (source.md:19) | Tasks 1, 2, 3, 4, 5 | containment |
| INF-009 | "Tests: delete TESTS/test_terminal.py:56-59 and :73-82 ...; delete TESTS/test_adapter.py:719; ... edit only TESTS/test_questions.py:46, :52, :98." (source.md:19) | Tasks 1, 2, 3, 4, 5 | containment |
| INF-010 | "Surviving guards: no-blink test TESTS/test_render.py:182-190; `--fixture` with `--questions` refused at commands.py:177-178; ASCII boxes `safe_box` test ..." (source.md:19) | acceptance of Tasks 1, 2, 3, 4, 5 | containment |
| INF-011 | "T9 ... Delete TESTS/test_terminal.py:65-70 (the decorator and `test_no_blink_code_in_any_console_output`, with the T28 header at :62) in the same change as R1" (source.md:21) | Task 1 | containment |
| INF-012 | "R3 ... Delete `ParsedPage.unrecognised_keys` (PKG/parse.py:177) and its sum (:409); `Coverage.unrecognised_keys` (:195) and its sum (:647)." (source.md:25) | Task 6 | containment |
| INF-013 | "R2 ... Delete `QuestionsPanel.count_text` (PKG/view.py:209) and its assignment (:732)" (source.md:27) | Task 7 | containment |
| INF-014 | "S2 ... PKG/export.py: remove the `resources` import (:14), the `Draft7Validator` import (:18), `SCHEMA_PACKAGE` and `SCHEMA_FILE` (:24-25), and the schema load plus `check_schema` (:29-34)." (source.md:31) | Task 8 | containment |
| INF-015 | "T8 ... replace the assertion that ends in `or True` with `assert len(overflow) == 1`; keep all 27 cases." (source.md:35) | Task 9 | containment |
| INF-016 | "T5 ... Delete TESTS/test_question_quiet_scope.py:192-203 only (the tests of the fake mailbox itself)." (source.md:37) | Task 9 | containment |
| INF-017 | "T7 ... TESTS/test_golden_contract.py:214-215 and :518-519 (the duplicated SENSITIVE loops) only." (source.md:39) | Task 9 | containment |
| INF-018 | "D2 ... Change the QUESTION-OBSERVATION status lines only, so they say it passed on 2026-11-12 and cite `.dev/issues/409/owner-pass-record-20261112.md`" (source.md:43) | Task 10 | containment |
| INF-019 | "D1 ... mark open owner decision 6 ... and decision 8 ... as decided by `.dev/issues/409/owner-decisions-20261111.md`" (source.md:45) | Task 11 | containment |
| INF-020 | "D13 ... add the snapshot schema test id (TESTS/test_snapshot_schema.py); mark T7, T17, T45 and T50 \"not built / no automated test\" with the reason" (source.md:47) | Task 12 | containment |
| INF-021 | "After the last task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` passes and ruff is clean; the final test count equals 694 minus the tests the tasks removed." (source.md:51) | none (per-task gates only; no final package check) | none |
| INF-022 | "`grep -rn \"run-use\" src/superclaude/cli/observe/` still shows `run-use` only in the forbidden set and the help text that says the observer never runs it." (source.md:52) | none | none |
| INF-023 | "`git status --short` shows changes only in the files named above, `.dev/issues/409/` and this package." (source.md:53) | none | none |

parsed rows: 0 (coverage_pct = null). union: 20 of 23 matched, coverage_pct_union = 0.8696. unmapped_requirements_union = [INF-021, INF-022, INF-023]. S_dev_density = 3/23 = 0.1304.

## Structural signals

S_scope = 12 tasks. S_domains = 3 (code under src/, tests under tests/, docs under .dev/issues/409/). S_dev_density = 0.1304.

## Findings (each grounded; path:line re-read in this run)

F1. Task 4 acceptance cannot pass as written. plan:63 says "Grep finds no `closure_evidence`, `never_read` or `CLOSURE_EVIDENCE` in `src/superclaude/cli/observe` or `tests/observe`". The plan edits only tests/observe/test_questions.py :46, :52, :98 (plan:60), so the kept test at tests/observe/test_questions.py:50 `test_nothing_is_ever_closed_and_closure_evidence_is_unavailable` still contains the string `closure_evidence`. tests/observe/test_view.py:174 `test_a_released_row_without_an_outcome_never_reads_done_complete_or_settled` contains the substring `never_read`. Both are unrelated to the removed properties. An executor following the criterion literally cannot pass it, and the plan forbids renaming or deleting that test (plan:65). After :52 is deleted that test's name also claims something it no longer asserts.

F2. Task 5 acceptance cannot pass as written. plan:72 says Grep for `question_fixture` and `_question_index` "finds only the string code `no-question-fixture`". The plan renames the test to `test_a_fixture_source_has_no_question_fixture` (plan:69), which contains `question_fixture`; the current name at tests/observe/test_collector.py:662 does too. The hyphenated code `no-question-fixture` does not match the underscore pattern at all, so the criterion is wrong in both directions.

F3. A source requirement is dropped. source.md:49-53 ("Acceptance for the whole package") has three checks: the final pytest count equals 694 minus removed tests, the `grep -rn "run-use"` check, and the `git status --short` scope check. The plan has no whole-package acceptance and no task that runs those checks; plan:21, :123 and :127 mention run-use only as a "keep" instruction. The final count is never stated (the plan only says Task 1 removes 9 cases and Task 9 removes 1, so 684).

F4. Line numbers that the plan itself will shift. plan:69 (Task 5) and plan:143 (Task 12) cite `commands.py:177-178` as the `--questions` with `--fixture` refusal. Live today: src/superclaude/cli/observe/commands.py:177-178. Task 4 deletes commands.py:142 (plan:60), so after Task 4 the lines are 176-177. Task 12 writes that citation into a design document, where it would be wrong from the day it is written.

F5. Task 1 leaves an orphan comment. src/superclaude/cli/observe/terminal.py:41 reads "# Palette table (CD-8): empty, so every style is plain text and meaning lives in words." The plan deletes `PALETTE` at :42 and the attrs block :44-53 (plan:31) but not :41; source.md:19 gives the range :41-53. The comment would describe a table that no longer exists.

F6. Task 5 leaves an orphan comment. src/superclaude/cli/observe/collector.py:102 reads "# SYNTHETIC question cycles: each an envelope dict or ``{"fail": <code>}``." The plan removes :103 and :104 state (plan:69) but not :102; source.md:19 gives :102-104.

F7. tests/observe/test_snapshot_schema.py:1 says "no ID assigned in acceptance-tests.md". Task 12 (plan:143) assigns the id in acceptance-tests.md, but no task updates this docstring, so it becomes false.

F8. The plan uses the label T7 for the debate row (Task 9, plan:107) and for the spec test T7 (Task 12, plan:143); T5, T8 and T9 are also spec test ids in acceptance-tests.md. Plan:51 does mark T34 as "spec test", but the other labels are not disambiguated.

## Verified true (re-Read in this run)

- Every line range named for Tasks 1, 2, 3, 6, 7, 8, 9, 10, 11 and 12 matches live files (terminal.py:42,44-53,161-172,33,37,38,72-74,18,21; adapter.py:65-82,340; parse.py:177,195,409,647,723-733; view.py:209,732,693,718; export.py:14,18,24-25,29-34,195; test_render.py:95-100; test_question_quiet_scope.py:192-203; test_golden_contract.py:214-215,518-519; prd.md:106,491,423,469; SPEC.md:104,106; owner-decisions-and-risks.md:22,24; acceptance-tests.md:25,28,51,56,64-66).
- The 9-case count for Task 1 is right: 1 + 5 + 1 + 2.
- No protected rule is touched: QUESTION_GATE_TEXT (commands.py:68-70, pinned at tests/observe/test_commands.py:632) is outside every edit; the forbidden-word test at tests/observe/test_adapter.py:158-192 counts words in adapter.py and Task 2's deletion adds none; the SENSITIVE scan removed by Task 9 still runs over the same files via tests/observe/test_fixtures.py:185-191.
- The QUESTION-OBSERVATION text edits in Task 10 are not pinned by any test (no test greps "off until" or "refused until"); the pinned help phrases are tests/observe/test_commands.py:727, :728, :738.
- Dependency order is sound: Tasks 3 and 6 both edit parse.py, Tasks 4 and 10 both edit commands.py, Tasks 10 and 11 both edit prd.md; each pair is ordered.

## Not verified

- The baseline of 694 passing tests and the post-task counts (the audit may not run tests).
- Whether `assert len(overflow) == 1` (Task 9) holds on all 27 cases.

## Recommendations

R1. Rewrite plan:63 and plan:72 so the grep targets code uses only (for example `\.closure_evidence\b`, `\bnever_read\b`, `question_fixture=`), then re-run the Task 4 and Task 5 gates.
R2. Add a final whole-package acceptance (source.md:49-53) to the plan, with the expected final count 684.
R3. In Task 12 cite `_question_refusal` in commands.py instead of line numbers.
R4. Add terminal.py:41 and collector.py:102 to Tasks 1 and 5.
