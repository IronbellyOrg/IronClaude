---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-executeNowBrief-20261116-202439
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Execute the debated Orca observer cuts (eleven approved rows)

Source: ./source.md
Goal: The eleven cuts that survived the adversarial debate (rows R1, R2, R3, S2, T5, T7, T8, T9, D1, D2, D13) are applied to the Orca observer, its tests and its design text, with `uv run pytest tests/observe -q` passing and ruff clean after every task, and no protected safety rule weakened.

## Constraints

- Shorthand. PKG is `src/superclaude/cli/observe/`. TESTS is `tests/observe/`. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`. The debate's final list and its row text are copied into `./source.md`; each task below restates what it needs.
- Scope is these eleven rows only. No commit, no push, no pull request. Every other row of the debate (KEEP, owner decisions, low confidence) is out of scope.
- Never touch: the sanitizer (`PKG/sanitize.py` and its use), the argv allow-list and forbidden verbs in `PKG/adapter.py`, process-group kill and output caps, terminal restore on exit and signals, the rule that message bodies, payload and `to_handle` are never kept, snapshot redaction, the disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, `QUESTION_GATE_TEXT` in `PKG/commands.py` (pinned by `TESTS/test_commands.py`), any DIRECTION-SELECTED line, and any file git does not track (for example `.dev/issues/409/handoff-mvp-brainstorm.md`).
- Line numbers in the tasks were read live on 2026-11-16 at HEAD f104ca51a and are leads only: re-grep every target right before editing, because other sessions share the worktree.
- Gate for every task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` passes and `uv run ruff check src/superclaude/cli/observe tests/observe` is clean. The baseline is 694 passed; the passed count falls only by the test functions a task deliberately deletes, and the task states the number it expects and the number it got. UV only; never bare python or pip. A failing gate is reported as a finding and never loosened to pass.
- Edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Whole-package checks, applied by the final review and not tasks of their own: Task 1 first saves `git status --short` to `./artifacts/baseline-status.txt`; at the end `git status --short` differs from that baseline only by the files these tasks name, `.dev/issues/409/` and this package; the full gate passes with the passed count equal to 694 minus the test cases the tasks removed (9 in Task 1 and 1 in Task 9, so 684, unless Task 6 had to remove an aggregate-only test); and `grep -rn "run-use" src/superclaude/cli/observe/` shows `run-use` only in the forbidden set in `PKG/adapter.py` and in the help text that says the observer never runs it.
- Names, not line numbers, wherever a check or a document points at code, because earlier tasks shift line numbers (for example `_question_refusal` in `PKG/commands.py`). A Grep check below means uses of the named symbol, not test function names that merely contain the word (`tests/observe/test_questions.py:50` and `tests/observe/test_view.py:174` keep such names).
- Labels. T5, T7, T8 and T9 in task titles are the debate's row names; the spec test ids in Task 12 are written "spec test T7", "T17", "T45" and "T50".
- Facts the debate found false in the earlier proposal, not to be repeated: the R1 test ranges were too wide, R3 must not drop the five parsed row fields, T9 keeps the `test_render.py` copy and deletes the `test_terminal.py` copy, T7 keeps the 32-character rule and the id rule, T8 keeps all 27 cases, D1 touches owner decisions 6 and 8 only.

## Phase 1: Remove production code that only tests call (R1 and T9)

## Task 1: Remove the unused palette, glyphs and box style from terminal.py and their tests (R1 part, T9)

Before any edit in this plan, save the output of `git status --short` to `./artifacts/baseline-status.txt` in this package (it lists the untracked paths that exist today) so the whole-package check at the end has a baseline.

Edit `src/superclaude/cli/observe/terminal.py`: delete `PALETTE` with the comment above it (:41-42), `_FORBIDDEN_ATTRS` with its comment (:44-53), `palette_style` (:161-172), the glyph entries `sep`, `vrule` and `cross` in the glyph table (:33, :37, :38), the `TerminalPolicy.box_style` property (:72-74), and the imports `from rich import box` (:18) and `from rich.style import Style` (:21) once Grep shows no remaining use in the file. Keep `safe_box=policy.ascii` in `make_console`.

Edit `tests/observe/test_terminal.py`: delete `test_colour_only_where_the_palette_sets_it` (:56-59), `test_palette_refuses_forbidden_styles` and `test_palette_accepts_plain_colour_and_bold` (:73-82), the T28 header comment (:62) and `test_no_blink_code_in_any_console_output` with its parametrize decorator (:65-70); drop the `box_style` assertion at :126; change the two `sep` assertions in `test_glyph_table_maps_to_ascii` (:132-133) to assert the `selected` glyph under the UTF and the ASCII policy instead; remove the `box` and `palette_style` imports if they become unused. The no-blink guard that survives is `tests/observe/test_render.py:182-190` (real screen, every width, both colour modes); do not edit that file in this task.

Acceptance criteria:
- Grep over `src/superclaude/cli/observe` and `tests/observe` finds no `PALETTE`, `_FORBIDDEN_ATTRS`, `palette_style`, `box_style`, or glyph names `"sep"`, `"vrule"`, `"cross"`.
- `tests/observe/test_render.py:182-190` (no blink) still exists and passes; the `safe_box` test around `tests/observe/test_terminal.py:142-149` and the ASCII-mode test pass.
- The task states the number of test functions it deleted (expected 4: the palette-colour test, the forbidden-styles test, the plain-colour test and the no-blink test) and the number of collected cases that disappear (expected 9: the forbidden-styles test runs 5 cases and the no-blink test 2), and the gate passes with the passed count lower by exactly that number.
- `./artifacts/baseline-status.txt` exists and holds the `git status --short` output taken before the first edit.

## Task 2: Remove the unused CODES set from adapter.py (R1 part)

Edit `src/superclaude/cli/observe/adapter.py`: delete the `CODES` frozenset (:65-82) and reword the comment at :340 (`# a code from CODES, or "exit:<n>"`) so it no longer names `CODES`. Edit `tests/observe/test_adapter.py`: delete only the assertion `assert expected in adapter.CODES` (:719); keep the exact-code assertion at :718 and the rest of `test_error_envelopes_map_to_source_codes_whatever_the_exit_status`.

Acceptance criteria:
- Grep for `\bCODES\b` over `src/superclaude/cli/observe` and `tests/observe` finds nothing.
- `tests/observe/test_adapter.py:718` still asserts the exact source code (`consumer-fenced` and `no-active-terminal`) and the test passes.
- No test function is deleted: the passed count is unchanged and the gate passes. `PKG/adapter.py`'s argv allow-list, forbidden prefixes and error mapping are otherwise unchanged (`git diff` of the file shows only the deleted set and the reworded comment).

## Task 3: Remove Fixture.parse from parse.py and route its test callers through parse_page and apply_frozen (R1 part)

Edit `src/superclaude/cli/observe/parse.py`: delete the `Fixture.parse` method (:723-733). Keep `Fixture.cycle` and `apply_frozen` (:736; also used by `PKG/collector.py:297`). Edit `tests/observe/test_fixtures.py`: the three callers (`fixture.parse(...)` at :44, :141 and :149) must call `parse_page(cycle.envelope, namespace, cycle_number, source_rank_base)` followed by `apply_frozen(parsed, cycle.frozen, source_rank_base)` through one small local helper in the test file, with the same arguments the removed method used. Add `apply_frozen` to the existing `from superclaude.cli.observe.parse import (...)` block at `tests/observe/test_fixtures.py:14-19` (`parse_page` is already imported there). The frozen-marker test (`test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true`, spec test T34) and `test_every_variant_loads_and_every_cycle_parses` keep their names and assertions.

Acceptance criteria:
- Grep for `fixture.parse(` and `def parse(` inside the `Fixture` class finds nothing; `apply_frozen` and `parse_page` are still used by `PKG/collector.py`.
- Both tests named above pass with their original assertions, including that only `w-003` is frozen and that the source-rank offsets are honoured.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 4: Remove closure_evidence, never_read, CLOSURE_EVIDENCE and Deps.extra (R1 part)

Edit `src/superclaude/cli/observe/questions.py`: delete the `closure_evidence` property (:70-72), the `never_read` property (:74-76) and the constant `CLOSURE_EVIDENCE` (:25). Edit `src/superclaude/cli/observe/commands.py`: delete the `extra` field of `Deps` (:142) and `field` from the `from dataclasses import dataclass, field` import (:14), after Grep confirms `field(` has no other use there and nothing passes `extra=` to `Deps`. Edit `tests/observe/test_questions.py`: at :46 change the tuple assertion to check only `state.last_read_cycle == 1`; delete the two `closure_evidence` assertions at :52 and :98. The on-screen wording `unavailable (no source)` stays pinned by `PKG/view.py` (`QUESTIONS_CLOSED`, :65, and the counts line, :693) and the view tests.

Acceptance criteria:
- Grep for the attribute and name uses `.closure_evidence`, `.never_read` and `CLOSURE_EVIDENCE` in `src/superclaude/cli/observe` and `tests/observe` finds nothing (the kept test names `tests/observe/test_questions.py:50` and `tests/observe/test_view.py:174` contain the words and stay), and `Deps` has no `extra` field.
- `tests/observe/test_questions.py` tests for T11, T12 and the no-read-marker case still pass; the closure-wording assertions in `tests/observe/test_view.py` still pass.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 5: Remove the synthetic question replay from FixtureSource (R1 part)

Edit `src/superclaude/cli/observe/collector.py`: in `FixtureSource` remove the `question_fixture` constructor argument (:97), `self._question_fixture` (:103), `self._question_index` and the replay loop in `read_questions` (:128-142); keep `read_questions` as a two-line method that returns `SourceResult("FAILED", code="no-question-fixture")` (the `CycleSource` protocol needs it). Edit `tests/observe/test_collector.py`: in `test_a_fixture_source_has_no_question_fixture_unless_one_is_supplied` keep the assertions up to the `no-question-fixture` check (:662-666), delete the synthetic-replay part (:667-678), and rename the test to `test_a_fixture_source_has_no_question_fixture` so the name is true. `--questions` with `--fixture` stays refused by `_question_refusal` in `PKG/commands.py`. Remove the comment `# SYNTHETIC question cycles: ...` (about :102) together with the attributes it describes.

Acceptance criteria:
- Grep for `question_fixture=`, `_question_fixture`, `question_fixture:` and `_question_index` in `src/superclaude/cli/observe` and `tests/observe` finds nothing; the string code `no-question-fixture` and the renamed test name `test_a_fixture_source_has_no_question_fixture` stay, and the synthetic-cycles comment is gone.
- The refusal test for `--questions` with `--fixture` in `tests/observe/test_commands.py` and the collector tests that use `FixtureSource` pass; `FixtureSource` still satisfies the `CycleSource` protocol (the collector tests that build one with `questions=True` pass).
- No test function is deleted: the passed count is unchanged and the gate passes.

## Phase 2: Remove dead counters, one panel field and the production schema import (R3, R2, S2, T8, T5, T7)

## Task 6: Remove the two aggregate unrecognised-key counters from parse.py (R3)

Depends on: Task 3

Edit `src/superclaude/cli/observe/parse.py`: delete `ParsedPage.unrecognised_keys` (:177) and its sum in `parse_page`'s return (:409), and `Coverage.unrecognised_keys` (:195) and its sum (:647). Keep `_FIELDS`, `_KNOWN`, `_count_unexpected`, `_BLOCK_FIELDS` (:91-93, the sanitizer block mode), the per-row field and its count (:155, :356), and the inspector line in `PKG/view.py:407`. Adjust only test assertions that read an aggregate counter (a `page.unrecognised_keys` or `coverage.unrecognised_keys` access); the per-row reads in `tests/observe/test_parse.py:188`, `:198`, `tests/observe/test_fixtures.py:145`, `:166` and `tests/observe/test_view.py:722` stay.

Acceptance criteria:
- Grep for `unrecognised_keys` matches only the per-row field, the `_count_unexpected` call in the row builder, `PKG/view.py:407` and the per-row test reads; no page-level or coverage-level counter remains, and `PKG/export.py` and `PKG/view.py` do not read one.
- The row-level tests listed above pass unchanged.
- The gate passes and the passed count equals the count before the task, unless an aggregate-only assertion was removed from an otherwise kept test.

## Task 7: Remove QuestionsPanel.count_text (R2)

Edit `src/superclaude/cli/observe/view.py`: delete the `count_text` field of `QuestionsPanel` (:209) and its assignment `count_text=open_text` (:732). Keep `open_text` (it is also used at :693 and :718) and the other 21 fields; make no comment edits. Do not edit any golden file.

Acceptance criteria:
- Grep for `count_text` over `src/superclaude/cli/observe` and `tests/observe` finds nothing; `open_text` is still used by the counts line and the header cell.
- The panel tests (`tests/observe/test_question_cap.py:71-134`, `tests/observe/test_view.py`, `tests/observe/test_render.py`) and the questions-off golden test (`tests/observe/test_render.py:616-629`) pass with `tests/observe/golden_release1_surface.json` unchanged (`git diff` shows no change to it). The export fields `open_total`, `window_full`, `retained`, `evicted` read at `PKG/export.py:165-168` still work.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 8: Move the snapshot schema load and validation out of export.py into the test conftest (S2)

Edit `src/superclaude/cli/observe/export.py`: remove the `from importlib import resources` import (:14), `from jsonschema import Draft7Validator` (:18), `SCHEMA_PACKAGE` and `SCHEMA_FILE` (:24-25), and the `SCHEMA` load plus `Draft7Validator.check_schema` call (:29-34); keep `SCHEMA_VERSION` (:23, used at :195) and re-check that `resources` has no other use in the file. Edit `tests/observe/conftest.py`: define `SCHEMA` there (read `snapshot.schema.json` from the package `superclaude.cli.observe` with `importlib.resources`, parse it, and run `Draft7Validator.check_schema` on it). Remove `SCHEMA` from the `from superclaude.cli.observe.export import ...` lines: in `tests/observe/test_commands.py:34` the whole line goes (it imports only `SCHEMA`), and in `tests/observe/test_snapshot_schema.py:15` keep `snapshot_json`, which the file uses about eleven times. Add `SCHEMA` to the existing `from tests.observe.conftest import ...` line in each file (`tests/observe/test_commands.py:36`, `tests/observe/test_snapshot_schema.py:18`). In `tests/observe/test_snapshot_schema.py` (:52-72) remove only the assertion that now compares the file with a copy of itself (`assert json.loads(text) == SCHEMA`, :60), the read that exists only for it, and the `from importlib import resources` import (:8) if nothing else in the file uses it; keep `Draft7Validator.check_schema(SCHEMA)`, the draft-07 `$schema` check and the closed-object checks.

Acceptance criteria:
- `PKG/export.py` no longer imports `jsonschema` or `importlib.resources` and defines no `SCHEMA`; Grep shows `SCHEMA` is read only from `tests/observe/conftest.py` by the two test modules; ruff reports no unused import in either test module and `snapshot_json` is still imported in `tests/observe/test_snapshot_schema.py`.
- `tests/observe/test_snapshot_schema.py::test_the_schema_ships_in_the_package_is_draft_7_and_closed_on_the_producer_side` and every snapshot validation test still pass, and a snapshot written by `export.py` still validates against the schema.
- No test function is deleted: the passed count is unchanged and the gate passes.

## Task 9: Fix the vacuous render assertion and remove two duplicated test blocks (T8, T5, T7)

Edit `tests/observe/test_render.py` (T8): replace the assertion at :95-100 that ends in `or True` with `assert len(overflow) == 1`; keep all 27 cases of the test. If the corrected assertion fails, report that as a finding and do not loosen it. Edit `tests/observe/test_question_quiet_scope.py` (T5): delete only `test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given` (:192-203, the test of the fake mailbox itself); keep :137-145, :148-171, :174-179 and :182-189 and the fake's own argv assertions. Edit `tests/observe/test_golden_contract.py` (T7): in the two golden leak scans delete only the duplicated `for what, pattern in SENSITIVE.items(): assert not pattern.search(...)` pairs (:214-215 and :518-519); keep the `isascii` checks (:213, :517), the 32-character rule (:216), the run, terminal and message id rule (:520) and :521-527; remove the `SENSITIVE` import there only if it becomes unused. The surviving guard for the removed scans is `tests/observe/test_fixtures.py:185-191`, which runs the same patterns over every packaged fixture.

Acceptance criteria:
- `tests/observe/test_render.py` has no `or True`; the test passes with all 27 parametrized cases.
- `test_t51_the_backend_refuses_every_consuming_argv_it_could_be_given` no longer exists; the other tests in `tests/observe/test_question_quiet_scope.py` pass; `tests/observe/test_adapter.py:158-192` still holds the forbidden-prefix tests.
- `tests/observe/test_golden_contract.py` still contains the 32-character rule and the id rule and passes; `tests/observe/test_fixtures.py:185-191` passes.
- The task states one deleted test function (T5) and the gate passes with the passed count reduced by exactly 1.

## Phase 3: Correct stale status text (D2, D1, D13)

## Task 10: State that QUESTION-OBSERVATION passed on 2026-11-12 where it still says not passed (D2)

Depends on: Task 4

Change the QUESTION-OBSERVATION status wording only, so each place says the gate passed on 2026-11-12 on the terms of the owner-written record `.dev/issues/409/owner-pass-record-20261112.md` (cite that path): `.dev/issues/409/bmad/prd-orca-observer/prd.md` lines 106 and 491; `.dev/issues/409/bmad/spec-orca-observer/unverified-register.md` line 27; `.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md` lines 3 and 62 (line 62 also says the owner has not named the Run; the owner record names `run_93bfa00cae2b`); `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` line 89; and in `src/superclaude/cli/observe/commands.py` the comment above `QUESTION_GATE_PASSED` (:63-66; keep the strings `release-gates.md` and `Task 18` in it, because `tests/observe/test_commands.py:750` asserts both appear in the file text), the HELP text (:86-88, "off until the owner records that QUESTION-OBSERVATION passed") and the `--questions` option help (:452-453, "refused until QUESTION-OBSERVATION has passed"). Do not edit `QUESTION_GATE_TEXT` (pinned), any DIRECTION-SELECTED line, `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` (lines 12 and 38 are already correct) or the untracked `handoff-mvp-brainstorm.md`. Keep the disclosure label and the sentence that the observer never runs run-use in the help text.

Acceptance criteria:
- Grep for `NOT passed`, `not passed` and `has not passed` near QUESTION-OBSERVATION in the files above finds no live claim that the gate has not passed; the refusal text `question read not enabled: QUESTION-OBSERVATION has not passed` in `QUESTION_GATE_TEXT` is unchanged.
- `uv run pytest tests/observe/test_commands.py tests/observe/test_registration.py -q` passes, including the tests that read the help text (`never runs run-use`, the disclosure label, `one named Run`) and the guard test that requires `release-gates.md` and `Task 18` in the source text.
- No other line of these files changes (`git diff` is limited to the status wording); the full gate passes with the passed count unchanged.

## Task 11: Mark owner decisions 6 and 8 as decided where they are still listed as open (D1)

Depends on: Task 10

In place only, mark open owner decision 6 (permission to read the question scope) and open owner decision 8 (what identifies a human question) as decided by `.dev/issues/409/owner-decisions-20261111.md` (decision 6: "Permission granted, proceed", one named Run, `--types question`, never run-use; decision 8: "coordinator questions only") in `.dev/issues/409/bmad/spec-orca-observer/SPEC.md` lines 104 and 106 and `.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md` lines 22 and 24; check `.dev/issues/409/bmad/prd-orca-observer/prd.md` lines 423 (OQ-5) and 469 (12.3 item 6) and fix the same rows if they still read as open. Do not collapse the lists, do not replace prd.md section 12.1 with a pointer (the OQ-n labels exist only there), and leave decision 5 (fallback date) open.

Acceptance criteria:
- Each of the rows named above says decided and cites `owner-decisions-20261111.md` by path; the decision numbering and the OQ-n labels still resolve (Grep for `OQ-5` and `open owner decision 6` finds the same labels as before).
- Decision 5 (fallback date) and every other open row are unchanged (`git diff` touches only the rows named).
- The gate passes with the passed count unchanged (document-only task).

## Task 12: Correct the test-id bookkeeping in acceptance-tests.md (D13)

Edit `.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md`. In the section "Snapshot schema test (CAP-10, recorded owner decision 2)" (about line 64-66) replace "Test ID not yet assigned." with the real test file, `tests/observe/test_snapshot_schema.py`. Mark T7, T17, T45 and T50 as "not built / no automated test" with a reason: T7 and T17 are defined inside the AC-3 and AC-6 mapping rows (about lines 25 and 28), so add the note there (spec test T7 cannot run as written because `_question_refusal` in `src/superclaude/cli/observe/commands.py` refuses `--questions` with `--fixture`; for T17 state that no test cites it); T45 and T50 are table rows (about lines 51 and 56): T45's `read k of N Runs since start` header text is not built, and T50 is a reviewer check on design images, not a test. Re-grep the live file for the exact lines first. Strike nothing; the T45 (OQ-13) and T50 (AC-S input) references stay.

Acceptance criteria:
- The four test ids each carry the words `not built` or `no automated test` with a stated reason, and the snapshot schema section names `tests/observe/test_snapshot_schema.py` instead of "not yet assigned".
- Every test id and table row that existed before the edit is still present (compare `grep -c` of the `| T<n> |` rows and of the ids T1 to T56 before and after), and the OQ-13 and AC-S input references are intact.
- The gate passes with the passed count unchanged (document-only task).
