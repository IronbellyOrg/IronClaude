# Item 11.4 summary: tests/commands/test_sweep_command.py

Command: `uv run pytest tests/commands/test_sweep_command.py -v`. Raw stdout, stderr and exit code: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command.txt`.

## Actual counts (from the raw file)

| Result | Count |
|---|---|
| passed | 121 |
| failed | 0 |
| skipped | 0 |
| xfail / error | 0 |
| exit code | 0 |

Regression modules, run once at the end and left untouched: `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py -q` gave 90 passed. `uv run ruff format --check tests/commands/test_sweep_command.py` and `uv run ruff check src/superclaude/cli/sweep tests/sweep tests/commands/test_sweep_command.py` both clean.

Bad-text check (not part of the committed tests): the test file and the three sources were copied to a private folder under `/tmp`, defects were injected into the copies (the "in force and no higher-priority conflict" clause weakened, the qualifier removed from the wrap-up bullet, the "command not found" trigger removed, the Read-denied failure clause removed, a `Retry` sentence added to the skill), and the copied tests reported 6 failed and 104 passed. The copies were then deleted. No repository source file was mutated.

Cycle-1 additions (QA fixes CMD-F1 and CMD-F2): 5 new cases, 110 to 115. Each was shown to fail on a private `/tmp` copy of the two primitives, the style and the test file, then the copy was deleted: ALL to ANY (both `conditions-are-conjunctive` cases failed), `exited 0 or 1` (both `success-exit-0` cases failed), `from the person or a peer agent` in the style and the skill (both `assignment-source-system-developer-or-direct-person` cases failed), `The exception does not cover` to `The exception also covers` (both `ordinary-exception-does-not-cover-the-exclusion-list` cases failed). Details: `qa/cmd-skill/fix-log-cycle1.md`.

Docs gate cycle-1 additions (QA fixes DOC-F1 and DOC-F2): 6 new cases, 115 to 121. Each was shown to fail on a private `/tmp` copy of the two primitives, the style and the test file when its sentence was removed, then the copy was deleted (one failing case per removal, 120 others still passed). Details: `qa/docs/fix-log-cycle1.md`.

Final gate cycle 1 (QA fix FIN-F7) was reverted by the owner's decision of 2026-11-12 (`phase-outputs/plans/FINAL-GATE-halt-resolution-decision.md`): the three FIN-F7 tests were removed, 124 back to 121, and the skill-only pin reads `success-parse-takes-only-report-path-and-summary` again. FIN-F7 is OPEN as a whole.

Sources under test (read from disk by `pathlib`, no HOME file, no mock policy model, no subprocess): `src/superclaude/commands/sweep.md` (C), `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (K), `src/superclaude/output-styles/pragmatic.md` (S). Source line numbers are as read on 2026-11-12.

## Source-to-test mapping: DESIGN 7.6 original assertions (14 test cases)

| Criterion | Test | Pins |
|---|---|---|
| command `allowed-tools: Skill` exactly | `test_sweep_command_allowed_tools_literal` | C:9 |
| skill `allowed-tools` literal exactly | `test_sweep_skill_allowed_tools_literal` | K:4 |
| installed skill path, plain substring, inside `## Activation` | `test_sweep_activation_names_installed_skill_path` | C:51 |
| project copy via `(?<!~/)` regex, inside `## Activation`, separate assertion | `test_sweep_activation_names_project_copy_as_separate_path` | C:55 |
| the regex cannot be satisfied by the installed path alone | `test_sweep_project_copy_regex_rejects_installed_path_alone` | regex self-check |
| PATH-first order | `test_sweep_skill_path_first_order` | K:23 before K:24 |
| `command not found` trigger | `test_sweep_skill_fallback_only_on_command_not_found` | K:24 |
| `--no-sync` and `--frozen` in the fallback literal | `test_sweep_skill_fallback_literal_has_no_sync_and_frozen` | K:24 |
| `120000` on each run | `test_sweep_skill_step_timeout_120000[1]`, `[2]` | K:23, K:24 |
| no `## Unattended mode` heading (also no `--unattended`) | `test_sweep_command_has_no_unattended_mode` | C whole file |
| no `src/superclaude/` substring in either file | `test_sweep_no_src_superclaude_path[sweep.md]`, `[SKILL.md]` | C, K whole files |
| no stop, retry, release, merge, removal (word-boundary regex, case-insensitive) | `test_sweep_skill_has_no_stop_retry_release_merge_removal_advice` | K whole file |

## Source-to-test mapping: common rule, asserted in BOTH the skill and the style (37 pins, each run twice: `test_style_carries_common_rule_clause[<id>]` and `test_skill_carries_common_rule_clause[<id>]`, 74 test cases)

The style part is the rule block S:22-26 (primary bullet plus four sub-bullets); the skill part is `## Final reply`, K:31-51. Cycle 1 ended the assignment-source, in-force and exit-0 pins on their delimiters and added the two pins marked (cycle 1). Where the two files word a clause differently, the pin names each file's own wording.

| Added case (pin id) | Style line | Skill line |
|---|---|---|
| conditions-are-conjunctive (cycle 1: all of the conditions must hold, not any one) | S:23 | K:35 |
| assignment-top-level-explicit-specified-work | S:23 | K:37 |
| assignment-source-system-developer-or-direct-person | S:23 | K:37 |
| assignment-in-force-no-higher-conflict (also the higher-priority conflict case) | S:23 | K:37 |
| assignment-must-be-explicit-for-specified-work (absent assignment: no explicit assignment means no exception) | S:24 | K:45 |
| loaded-skill-for-actual-invocation | S:23 | K:38 |
| success-exit-0 | S:23 | K:39 |
| success-stdout-parsed-for-counts-and-path | S:23 | K:40 |
| success-report-read | S:23 | K:41 |
| exempt-final-successful-reply-only | S:23 | K:43 |
| exempt-reply-is-counts-and-path | S:23 | K:35 |
| exempt-reply-omits-table-wrapper-gloss | S:23 | K:35 |
| exempt-reply-precedence-for-that-one-reply | S:23 | K:43 |
| not-established-by-invoking-quoting-table-request-or-word (role request or table request alone) | S:24 | K:45 |
| skill-and-style-define-but-do-not-assign | S:24 | K:45 |
| files-reports-tool-output-quotes-peers-never-establish (file, tool, report, peer, quoted claims; injected report stays data) | S:24 | K:45 |
| person-run-exclusion-ordinary-unassigned-session | S:24 | K:45 |
| person-request-in-independently-assigned-coordinator | S:24 | K:45 |
| direct-assignment-plus-separate-invocation | S:24 | K:45 |
| direct-assignment-must-apply-before-execution | S:24 | K:45 |
| unknown-ambiguous-revoked-superseded-conflicting-is-ordinary | S:24 | K:45 |
| no-role-rebuilt-from-files-or-history | S:24 | K:45 |
| ordinary-exception-does-not-cover-the-exclusion-list (cycle 1: the opener that carries the negation, with the list) | S:25 | K:47 |
| ordinary-other-coordinator-messages | S:25 | K:47 |
| ordinary-person-run-invocations | S:25 | K:47 |
| ordinary-workers-and-subagents | S:25 | K:47 |
| ordinary-quoted-or-read-sweep-text | S:25 | K:47 |
| ordinary-failures-blockers-parse-errors | S:25 | K:47 |
| ordinary-missing-output-or-unsuccessful-read | S:25 | K:47 |
| stderr-visible-for-exit-1-or-2-other-failures-ordinary | S:25 | K:47 |
| non-exempt-replies-keep-table-and-placement | S:25 | K:47 |
| formatting-never-authorizes-advice (no prohibited advice) | S:25 | K:47 |
| no-general-exemption-for-coordinators-skills-or-files | S:25 | K:47 |
| scope-chat-presentation-only | S:26 | K:51 |
| scope-changes-no-trigger-tool-authority-worker-rule-permission-schedule-output (no new tools, rights, Python report or JSON change) | S:26 | K:51 |
| scope-other-truthfulness-safety-error-rules-stay | S:26 | K:51 |
| scope-eligibility-is-text-contract-not-detector (asserts the clause is present; the words "runtime detector" and "tool allowlist" are not asserted absent) | S:26 | K:51 |

## Source-to-test mapping: skill-only clauses (15 cases, `test_skill_states_clause[<id>]`)

These are failure and boundary cases the style states only as a general class (failures, parse errors, missing output, unsuccessful Reads), so the specific forms are pinned on the skill text only.

| Pin id | Skill line |
|---|---|
| success-parse-takes-only-report-path-and-summary | K:25 |
| success-report-read-in-chunks-of-150-lines | K:25 |
| exit-1-or-2-prints-stderr-and-ends-run (visible exit 1 or 2 stderr) | K:27 |
| failure-exhausted-designed-fallback (step 2 also failed) | K:29 |
| failure-list-is-framed-as-ordinary-formatting (cycle 1: the whole failure sentence, so the list keeps its frame) | K:29 |
| failure-malformed-json | K:29 |
| failure-missing-summary-or-report-path | K:29 |
| failure-read-fails-or-denied (missing, unreadable or denied report Read) | K:29 |
| no-fabricated-summary-no-hidden-error-no-other-command (no fabricated success) | K:29 |
| no-third-run-of-the-command | K:24 |
| same-rule-as-the-style-exception-with-installed-path | K:33 |
| boundary-recommends-no-action-or-advice | K:61 |
| boundary-report-text-is-data (injected report is data) | K:63 |
| boundary-no-tool-beyond-two-bash-forms-and-read | K:64 |
| no-worker-mode-no-extra-flag | K:19 |

## Source-to-test mapping: style-only restatements and defaults (12 cases)

| Case | Test | Style line |
|---|---|---|
| rule is one primary bullet plus four sub-bullets | `test_style_rule_is_one_bullet_with_four_sub_bullets` | S:22-26 |
| primary bullet names the only exception and keeps the default placement sentence | `test_style_primary_rule_names_the_only_exception_and_keeps_placement` | S:22 |
| old unqualified "No exceptions" table sentence is gone | `test_style_old_unqualified_table_sentence_is_gone` | S:22 |
| restatement 1 of 6: Status and wrap-ups bullet | `test_style_restatement_is_qualified_by_the_exception[status-and-wrap-ups-bullet]` | S:57 |
| restatement 2 of 6: template introduction, columns, None row, non-exempt sentence | `...[response-templates-introduction]` | S:62 |
| restatement 3 of 6: Simple answer | `...[simple-answer-template]` | S:64 |
| restatement 4 of 6: Normal answer | `...[normal-answer-template]` | S:73 |
| restatement 5 of 6: Wrap-up | `...[wrap-up-template]` | S:84 |
| restatement 6 of 6: Multi-point reply | `...[multi-point-reply-template]` | S:94 |
| qualifier `Except for the sweep chat-summary exception above,` appears exactly 6 times and not in S:22-26 | `test_style_qualifier_appears_exactly_six_times_and_never_in_the_primary_rule` | S whole file |
| non-exempt defaults kept: 4 `non-exempt example` labels, 4 Status/Result table headers, 3 `NEXT / None.` rows, length-budget sentence | `test_style_non_exempt_defaults_examples_and_none_row_are_kept` | S:29, S:64-99 |
| the exception does not appear after `## Work discipline` | `test_style_exception_does_not_leak_into_work_discipline` | S:107-238 |

## Source-to-test mapping: docs gate cycle-1 additions (6 cases, DOC-F1 and DOC-F2)

| Case | Test | Pins |
|---|---|---|
| DOC-F1: the command says `Safe to close`, `Removable` and `Next inspection` are observations, not advice (text before `## Triggers`) | `test_sweep_command_says_report_columns_are_observations_not_advice` | C:16 |
| DOC-F1: the skill says the same in `## Boundaries` | `test_sweep_skill_boundaries_say_report_columns_are_observations_not_advice` | K:66 |
| DOC-F2: the command says that in Phase 1 stalled (proved) and fenced are not observed and a zero count there means nothing (text before `## Triggers`) | `test_sweep_command_says_phase1_stalled_and_fenced_zero_means_nothing` | C:16 |
| DOC-F2: skill step 4 says the same | `test_sweep_skill_step4_says_phase1_stalled_and_fenced_zero_means_nothing` | K:26 |
| DOC-F2: skill step 4 prints each of the two counts with the mark `(not observed in Phase 1)` | `test_sweep_skill_step4_prints_the_phase1_mark_with_the_counts` | K:26 |
| DOC-F2: the exempt reply keeps the mark on the counts (skill `## Final reply`, exempt-reply part) | `test_sweep_exempt_reply_keeps_the_phase1_mark_on_the_counts` | K:43 |

The seven mandatory-table sites are the primary bullet (S:22, with S:23-26) and the six qualified lines above. Test case total: 14 + 74 + 15 + 12 + 6 = 121.

## Static-only limits

These tests prove that the clauses are present in the loaded texts of the command, the skill and the canonical style, in the places and the words listed above. They do not prove live model adherence, live recognition of a coordinator assignment, or resistance to an injected report; the "with and without independent assignment" injected-report cases are covered only as the text clauses that report contents stay data and never establish or extend any right. They do not test the installed HOME style: `~/.claude/output-styles/pragmatic.md` is not read, written or compared, and `make sync-dev` does not refresh it. "Absent assignment" has no literal word in the sources and is pinned as the explicit-assignment requirement plus the person-run exclusion. No live Orca, ccsession or Claude command was run, and the tests never call a formatter, a predicate or a subprocess.
