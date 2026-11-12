# QA Report - Test-coverage lens (T247)

**Date:** 2026-11-12
**Lens:** test coverage (DESIGN 7.6, routing refresh R5, chat-output addendum, severity regression)
**fix_authorization:** false

**Scope:** `tests/commands/test_sweep_command.py` (572 lines, 110 cases) against DESIGN 7.6 (`docs/designs/orchestrator-mode.md:666`), DESIGN 9 row R5 (`:719`), the chat-output-exception addendum (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/chat-output-exception-20261109-133150/design-addendum.md:13-37`), and the three primitives as they are on disk now (`src/superclaude/commands/sweep.md` 68 lines, `src/superclaude/skills/sc-sweep-protocol/SKILL.md` 62 lines, `src/superclaude/output-styles/pragmatic.md` 238 lines). All were read from disk in chunks of at most 150 lines. Earlier reviews were not relied on.

**Safety:** no live Orca, ccsession or Claude command, no `superclaude sweep run`. Only `uv run pytest`, `uv run ruff`, `grep` and `git diff` were run. Mutation experiments used private copies under `/tmp/ironclaude-batch.*`, removed on exit (`ls` afterwards shows none). The only repository file written is this report.

## Fresh runs (this review)

| Command | Result |
|---|---|
| `uv run pytest tests/commands/test_sweep_command.py -q` | 110 passed |
| `uv run pytest tests/commands tests/recommend -q` | 628 passed |
| `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py -q` | 90 passed |
| `uv run ruff check` and `ruff format --check` on the two test files | clean, 2 files formatted |
| `git status --short tests/skills` and `git diff --stat HEAD -- tests/skills` | empty (severity tests untouched) |

628 + 90 = 718, which equals the `718 passed` in `phase-outputs/test-results/phase11-validation.md:62`. The saved raw file `test-sweep-command.txt:125` (110 passed) and the summary table `test-sweep-command-summary.md:9` (110) agree with my run.

## Mapping A: DESIGN 7.6 Test bullet (`orchestrator-mode.md:666`) to tests

| DESIGN 7.6 assertion | Test (file `tests/commands/test_sweep_command.py`) | Asserts what DESIGN says? |
|---|---|---|
| two `allowed-tools` literals exactly | `test_sweep_command_allowed_tools_literal` (:106), `test_sweep_skill_allowed_tools_literal` (:110) | Yes: exact equality with `_COMMAND_TOOLS` (:29) and `_SKILL_TOOLS` (:30-33); matches `sweep.md:9` and `SKILL.md:4` |
| installed skill path in Activation | `test_sweep_activation_names_installed_skill_path` (:114) | Yes: substring inside the `## Activation` section only (`sweep.md:42-56`) |
| dual-surface (project copy) path in Activation, apart from the installed path | `test_sweep_activation_names_project_copy_as_separate_path` (:119) with `_PROJECT_COPY = (?<!~/)\.claude/skills/sc-sweep-protocol/SKILL\.md` (:37); self-check `test_sweep_project_copy_regex_rejects_installed_path_alone` (:124) | Mostly. The regex rejects the `~/` spelling, so the installed path alone fails the test (mutation M4b below fails as it should). It does not reject other prefixes, see F4 |
| PATH-first order, "command not found" trigger | `test_sweep_skill_path_first_order` (:131), `test_sweep_skill_fallback_only_on_command_not_found` (:138) | Yes (`SKILL.md:23-24`) |
| `--no-sync` in the fallback literal | `test_sweep_skill_fallback_literal_has_no_sync_and_frozen` (:144) | Yes, stronger: exact literal equality plus both flags |
| timeout 120000 | `test_sweep_skill_step_timeout_120000[1,2]` (:150-152) | Yes, on each run step |
| no `## Unattended mode` heading | `test_sweep_command_has_no_unattended_mode` (:155) | Command only; the skill is not checked (F6, minor) |
| no `src/superclaude/` in either file | `test_sweep_no_src_superclaude_path[sweep.md,SKILL.md]` (:162) | Yes, both files |
| no stop, retry, release, merge, removal advice in the skill | `test_sweep_skill_has_no_stop_retry_release_merge_removal_advice` (:167) with `_FORBIDDEN_ADVICE` (:34-36) | Base words only (F5, minor) |

## Mapping B: routing refresh R5 (`orchestrator-mode.md:719`)

`git diff -- tests/recommend/test_routing_refresh.py` is one changed line: `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` becomes `{"graph", "impact", "issue", "sweep"}` (`test_routing_refresh.py:33`). Nothing else changed. The consuming assertion is `shipped - _POST_REFRESH_ADDITIONS == active` at `:648`, where `shipped` is every `commands/*.md` stem (`:647`). With `src/superclaude/commands/sweep.md` present, the set without `sweep` would not equal the 43 active names, so the edit is needed and the assertion is not vacuous. Saved run `phase-outputs/test-results/r5-routing-refresh.txt:259`: `248 passed`, no FAILED/ERROR/SKIPPED lines (grep count 0). The file mtime (06:22:00) is after the edit (06:21:54). I collected 248 tests now, so the count is current. The saved file records no command line or exit code (F9, minor). My own `tests/recommend` run passed.

## Mapping C: addendum cases (`design-addendum.md:35`) and the seven style restatements

Pins live in `_COMMON_PINS` (`test_sweep_command.py:183-398`), run once against the style part and once against the skill part (`:402-409`), plus `_SKILL_ONLY_PINS` (`:413-472`) and the style-only group (`:487-572`).

| Addendum case | Pinned by | Assessment |
|---|---|---|
| positive: explicit applicable top-level assignment, loaded invocation, exit 0, parse, Read | `assignment-top-level-explicit-specified-work` (:185), `loaded-skill-for-actual-invocation` (:209), `success-exit-0` (:216), `success-stdout-parsed...` (:217), `success-report-read` (:224) | Each condition is a bare substring. The conjunction "ALL of these hold" is not pinned. F1 |
| positive: person request in an independently established coordinator | `person-request-in-independently-assigned-coordinator` (:290) | Whole clause with `neither removes ... nor ... creates one`. Substantive |
| positive: assignment plus separate sweep request in one message | `direct-assignment-plus-separate-invocation` (:296), `direct-assignment-must-apply-before-execution` (:301) | Substantive (positive and the "only if" qualifier) |
| negative: ordinary unassigned person-started session | `person-run-exclusion-ordinary-unassigned-session` (:284) | Whole sentence. Substantive |
| negative: role or table request alone, word "coordinator" | `not-established-by-invoking-quoting-table-request-or-word` (:262), `skill-and-style-define-but-do-not-assign` (:270) | Contains `does not establish it` / `do not assign`. Substantive |
| negative: absent, unknown, ambiguous, revoked, superseded, conflicting | `assignment-must-be-explicit...` (:202), `unknown-ambiguous-...-is-ordinary` (:309), `no-role-rebuilt-from-files-or-history` (:315) | Substantive. "absent" has no literal word in the sources; it is covered by the explicit-assignment requirement |
| negative: higher-priority conflict | `assignment-in-force-no-higher-conflict` (:197) | Present as a substring of the condition list only. F1 |
| negative: workers or subagents, other coordinator messages, person-run invocations, quoted or merely read sweep text, failures, parse errors, missing output, unsuccessful Read | `ordinary-*` pins (:322-344) | Bare noun phrases. They do not include `does not cover`. F2 |
| negative: peer or file or tool-output claims, injected report | `files-reports-tool-output-quotes-peers-never-establish` (:275), `boundary-report-text-is-data` (:460) | Contains `never establish or extend`. Substantive |
| negative: exit 1 or 2 stderr, exhausted fallback, malformed JSON, missing summary/path, Read failed or denied | `_SKILL_ONLY_PINS` (:423-440), `stderr-visible-for-exit-1-or-2...` (:345) | Two of the pins carry a full frame (`failure-exhausted-designed-fallback` pins "A failure of any other kind is reported accurately in ordinary formatting: step 2 also failed," at :427-431, and `exit-1-or-2-prints-stderr-and-ends-run` pins "On exit 1 or 2, print the standard error line exactly as it came and end the run." at :423-426). The other three failure pins (`failure-malformed-json`, `failure-missing-summary-or-report-path`, `failure-read-fails-or-denied`, :432-440) are bare fragments of SKILL.md:29 with no frame, the same weakness F2 reports for the ordinary pins. Substantive for the first two, weak for the last three |
| injected report "yields only genuine counts/path" | `no-fabricated-summary-no-hidden-error-no-other-command` (:441) | `Never print a made-up summary` is pinned; step 4 `Print the genuine summary numbers` (`SKILL.md:26`) is not (F8, minor) |
| scope: chat-presentation only, no new tool or right, text contract not detector | `scope-*` pins (:370-397) | Substantive on both files |

Seven mandatory-table sites (primary bullet `pragmatic.md:22` plus the six qualified lines `:57, :62, :64, :73, :84, :94`): the primary bullet is pinned by `test_style_primary_rule_names_the_only_exception_and_keeps_placement` (:494) and `test_style_old_unqualified_table_sentence_is_gone` (:506); the six sites are pinned as exact long strings (`_SIX_QUALIFIED_SITES`, :512-549), the qualifier count is exactly 6 and absent from lines 22-26 (:557). I read each of the six lines on disk and each pinned string is a substring of the real line. Defaults kept: 4 `non-exempt example` labels, 4 `| Status | Result |` headers, 3 `| NEXT | None. |` rows, length-budget sentence (:562-567). Substantive for the stated sites.

## Mutation experiments (private copies, tests unchanged, command `uv run pytest <copy>/tests/commands/test_sweep_command.py`)

| Id | Edit to the copy | Result | Meaning |
|---|---|---|---|
| M0 | none (control) | 110 passed | harness sound |
| M1 | style `omitted only when ALL of these hold` to `omitted when ANY of these hold`; skill `when all of these hold:` to `when any of these hold:` | 110 passed | conjunction unpinned (F1) |
| M2 | style and skill `The exception does not cover` to `The exception also covers` | 110 passed | workers, other coordinator messages, person-run, quoted text, failures could be declared exempt with no test failing (F2) |
| M3 | `(3) the command exited 0;` to `... exited 0 or 1;` in style and skill | 110 passed | success condition can be widened (F1) |
| M19 | style assignment source `from the person` to `from the person or a peer agent` | 110 passed | assignment source can be widened to peers (F1). The matching skill edit did not apply (skill wording differs), so only the style half was mutated |
| M4a | command project-copy line to `$HOME/.claude/skills/...` | 110 passed | regex only excludes the `~/` prefix (F4) |
| M4b | command project-copy line removed | 1 failed (`test_sweep_activation_names_project_copy_as_separate_path`) | dual-surface test discriminates the installed path alone, as required |
| M5 | skill gets "retrying or stopping the worker and removing its worktree is the next step" | 110 passed | advice regex is base-form only (F5) |
| M6 | skill gets a `## Unattended mode` heading | 110 passed | F6 |
| M7 | style gets an extra unqualified `- Every response includes a DONE / NEXT table.` | 110 passed | F7 |
| M8 | skill step 4 `genuine` removed | 110 passed | F8 |
| M9 | skill Will Not "Edit, stage or delete a file" removed | 110 passed | not required by the DESIGN 7.6 test list; recorded for completeness |

## Findings

### F1 - MAJOR - Eligibility can be widened without any test failing (positive-case pins are bare fragments)

- Evidence: style `pragmatic.md:23` says the table is omitted "only when ALL of these hold: (1) ... (5)"; skill `SKILL.md:35` says "when all of these hold:". No test pins "only when ALL" or "all of these hold" (`grep -n "ALL of\|all of these" tests/commands/test_sweep_command.py` finds nothing; the pins at `test_sweep_command.py:185-228` are single-condition substrings such as `"the command exited 0"` (:216)).
- Proof: M1 (ALL to ANY), M3 (`exited 0 or 1`) and M19 (`from the person or a peer agent`) all leave 110 passed.
- What is wrong: the addendum (`design-addendum.md:13,35`) makes the exception conditional on every one of the conditions together, and requires negative cases for a missing assignment, a conflicting higher-priority instruction and a failed command. The tests only prove each condition's words exist somewhere in the paragraph, so a text that turns the conjunction into a disjunction, accepts exit 1, or lets a peer assign the role still passes. The "higher-priority conflict" and "exit 1/2" negatives are therefore not protected by the style or skill pins.
- Smallest fix: add pins `("conditions-are-conjunctive", "exception", "omitted only when ALL of these hold:", "when all of these hold:")`; end each condition pin on its delimiter or full clause (`"(3) the command exited 0;"`, skill `"- the command exited 0;"`, `"... from the person, and that assignment is still in force and conflicts with no higher-priority instruction"`).

### F2 - MAJOR - The addendum's negative cases for workers, subagents, other coordinator messages, person-run invocations, quoted sweep text and failures are pinned without the negation

- Evidence: `test_sweep_command.py:322-344` pin `"other coordinator messages"`, `"ordinary person-run invocations"`, `"workers or subagents"`, `"quoted or merely read sweep text"`, `"failures, blockers, parse errors"` and `"missing required output or unsuccessful report Reads"` (skill: `"missing output or an unsuccessful Read of the report"`) as bare phrases inside the "What stays ordinary" part. The only words that make them exclusions are `The exception does not cover` (style `pragmatic.md:25`, skill `SKILL.md:47`), and that sentence opener is not pinned anywhere.
- Proof: M2 (`The exception does not cover` to `The exception also covers`) leaves 110 passed.
- What is wrong: these are exactly the negative cases the addendum lists (`design-addendum.md:35`: workers/subagents, other coordinator messages, ordinary person-run, quoted or merely read sweep text, malformed/missing output). A flipped sentence that exempts workers still passes, so the narrowness the revision exists to guarantee is untested for these cases.
- Smallest fix: pin the sentence start with its list, for example `"The exception does not cover other coordinator messages, ordinary person-run invocations, workers or subagents, quoted or merely read sweep text, failures, blockers, parse errors,"` (same string in both files, then the file-specific tail), replacing the six bare pins or adding to them.

### F4 - MINOR - Project-copy regex rejects only the `~/` prefix

- Evidence: `test_sweep_command.py:37` `(?<!~/)\.claude/skills/...`. M4a (`$HOME/.claude/skills/...` in the Activation block) passes as if it were the project copy. The real text (`sweep.md:49,53`) is correct and M4b shows the installed path alone fails the test. Fix: anchor on the preceding backtick, `` (?<=`)\.claude/skills/sc-sweep-protocol/SKILL\.md ``, or reject any `[\w~$/]` before the dot.

### F5 - MINOR - Advice regex matches base words only

- Evidence: `test_sweep_command.py:34-36` `\b(?:stop|retry|release|merge|removal)\b`. M5 added "retrying or stopping the worker and removing its worktree is the next step" and passed. DESIGN 7.6 says "no stop, retry, release, merge or removal advice"; inflected forms are advice too. Fix: `\b(?:stop|retr(?:y|ies|ying)|releas\w*|merg\w*|remov\w*)` or `stop\w*`, then re-run to confirm the current skill still has no match.

### F6 - MINOR - `## Unattended mode` is checked only in the command

- Evidence: `test_sweep_command.py:155-159` reads `_COMMAND` only; M6 added the heading to the skill and passed. DESIGN 7.6 attaches the Unattended rule to the command (`orchestrator-mode.md:657`), so this is a small gap, not a miss of the stated bullet.

### F7 - MINOR - No guard against a further unqualified table mandate in the style

- Evidence: tests pin the seven known sites and `count == 6` for the qualifier (:557), but M7 (a new unqualified "Every response includes a DONE / NEXT table." appended) passed. `grep -n "DONE / NEXT" pragmatic.md` shows lines 22, 23, 29, 57, 62, 64, 73, 84, 94 today, all accounted for. Fix, if wanted: assert every line containing `DONE / NEXT` is one of those nine.

### F8 - MINOR - "genuine counts" for an injected report is not pinned

- Evidence: `SKILL.md:26` `Print the genuine summary numbers` (M8 removed `genuine`, 110 passed). The neighbouring rule `Never print a made-up summary` is pinned (:441), so the intent is partly covered.

### F9 - MINOR - Evidence files lack a command and exit code, and the severity run has no raw file

- Evidence: `r5-routing-refresh.txt` begins at the pytest banner (no `Command:` or exit-code line); the 90-passed severity run is stated only in `test-sweep-command-summary.md:15`, and `phase11-validation.md` keeps the last 30 lines of the combined run (718 passed). I reproduced all three numbers (110, 90, 628 + 90 = 718), so the numbers are right; the saved evidence is thinner than the addendum's "raw stdout/stderr/exit" ask for the 11.4 run (`design-addendum.md:31`).

## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | Inputs read from disk in chunks of at most 150 lines (command, skill, style, test file, DESIGN 7.6 and 9, addendum, BUILD-REQUEST, result files, OQ-6, `cli/sweep/commands.py`) | PASS |
| C2 | DESIGN 7.6: both `allowed-tools` literals asserted exactly | PASS |
| C3 | DESIGN 7.6: dual-surface test tells the installed `~/.claude/skills/...` path from the project `.claude/skills/...` copy (M4b fails, regex self-check at :124) | PASS (minor F4) |
| C4 | DESIGN 7.6: PATH-first order, `command not found` trigger, `--no-sync` and `--frozen` in the fallback literal, timeout 120000 on each run | PASS |
| C5 | DESIGN 7.6: no `## Unattended mode` heading | PASS (minor F6) |
| C6 | DESIGN 7.6: no `src/superclaude/` in either file | PASS |
| C7 | DESIGN 7.6: no stop/retry/release/merge/removal advice in the skill | PASS (minor F5) |
| C8 | Routing refresh adds only `sweep` to `_POST_REFRESH_ADDITIONS`; assertion at :648 is not vacuous; saved run passed (248 passed, 0 failures, after the edit); my run passed | PASS (minor F9) |
| C9 | Addendum positive cases map to substantive assertions (assignment, success conditions, person request in coordinator session, assignment plus separate request) | FAIL (F1) |
| C10 | Addendum negative cases map to substantive assertions (person-run, role/table request, unknown/ambiguous/revoked/superseded/conflicting, higher-priority conflict, workers, subagents, other coordinator messages, quoted text, exit 1/2, fallback exhausted, malformed JSON, missing summary/path, Read failure) | FAIL (F1, F2) |
| C11 | Injected-report, peer and file-tool claims stay data (both files); no fabricated summary | PASS (minor F8) |
| C12 | All seven mandatory-table restatements pinned to the actual style text (primary bullet plus six qualified sites, count 6, none in lines 22-26) | PASS (minor F7) |
| C13 | Ordinary defaults kept: examples, columns, None row, length budget, no leak into Work discipline | PASS |
| C14 | Raw, summary and scoped severity agreement: 110 = 110, 90 passed, 628 + 90 = 718 = phase11 | PASS (minor F9) |
| C15 | No severity test weakening: `tests/skills` has no diff or status entry | PASS |
| C16 | No live-adherence or activation claim: test docstring (:13-17), summary "Static-only limits" (`test-sweep-command-summary.md:120`), step-7.10 limits (`step-7.10-style-exception.md:98`) all disclaim it | PASS |
| C17 | Mutation: widening eligibility (ALL to ANY, exit 0 or 1, peer assigner) is caught | FAIL (M1, M3, M19) |
| C18 | Mutation: inverting the exclusion sentence is caught | FAIL (M2) |
| C19 | `ruff check` and `ruff format --check` on the two test files | PASS |
| C20 | Option defaults in `sweep.md:35-38` (6h, at most 720h or 30d, 1 to 9999) agree with `cli/sweep/commands.py:27-28,44,228` (no test pins them; DESIGN 7.6 does not require one) | PASS |

## Summary

The static tests cover the DESIGN 7.6 bullet, the R5 edit, the seven style sites and most addendum cases with real assertions on the actual style and skill text, and the three result files agree with my reruns. The gate fails on two real gaps: the eligibility conjunction and the "does not cover" exclusion are not pinned, so the two properties the addendum exists to guarantee (all conditions required, listed sessions excluded) can be reversed with all 110 tests still green. Both are fixed by adding exact-sentence pins to `_COMMON_PINS`; no change to the primitives is needed.

Verdict: FAIL
Blocking count: 2
