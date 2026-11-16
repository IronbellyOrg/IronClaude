# Execute the cuts that survived the debate (Orca observer, issue 409)

Source of truth: the final list of the adversarial debate, /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/ponytail-review-20261116/cuts-debate/final-cut-list.md (rows R1, R2, R3, S2, T5, T7, T8, T9, D1, D2, D13, class EXECUTE-NOW; return contract in the adversarial/ folder next to it). The rows below are copied from it. Every other row (KEEP, owner decisions, low confidence) is out of scope. Repository: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp, branch 409-Phase2. Paths: PKG = src/superclaude/cli/observe/, TESTS = tests/observe/, SPECDIR = .dev/issues/409/bmad/spec-orca-observer/.

## Constraints

- Scope is the eleven rows below and nothing else. No commit, no push, no pull request.
- Never touch: the sanitizer (PKG/sanitize.py and its use), the argv allow-list and forbidden verbs in PKG/adapter.py, process-group kill and output caps, terminal restore on exit and signals, the rule that message bodies, payload and to_handle are never kept, snapshot redaction, the disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, `QUESTION_GATE_TEXT` (PKG/commands.py:68-70, pinned by TESTS/test_commands.py:632), any DIRECTION-SELECTED line, and any file git does not track (for example `.dev/issues/409/handoff-mvp-brainstorm.md`).
- Line numbers in the rows come from reviewers and are a lead only: re-grep every target in the live files right before editing, because other sessions share the worktree (HEAD was f104ca51a when the list was made).
- Gate after every task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` must pass (the baseline is 694 passed; the count falls only by the tests a task deliberately removes, and the task must state the new count) and `uv run ruff check src/superclaude/cli/observe tests/observe` must be clean. UV only, never bare python or pip.
- A step that fails its gate is reported as a finding; it is never loosened to pass.
- Plan edits touch only `src/`, `tests/`, `.dev/issues/409/` and this package's `./artifacts/`; nothing under `.claude/`.
- Facts the debate found false in the earlier proposal (do not repeat them): R1 test ranges were too wide (see the row), R3 must not drop the five parsed row fields, T9 keeps the test_render copy and deletes the test_terminal copy, T7 keeps the 32-character rule and the id rule, T8 keeps all 27 cases, D1 touches decisions 6 and 8 only.

## The eleven rows (execution order from the final list)

### Step 1: R1 and T9 in one change

R1 (CUT-SMALLER, confidence 80). Production: PKG/terminal.py:41-53 (`PALETTE`, `_FORBIDDEN_ATTRS`), :161-172 (`palette_style`), glyphs `sep` (:33), `vrule` (:37), `cross` (:38), `TerminalPolicy.box_style` (:72-74), and the imports that become unused (`Style`, `box`; `field` at commands.py:14). PKG/adapter.py:65-82 `CODES` deleted (not moved) and the comment at :340 reworded. PKG/parse.py:723-733 `Fixture.parse`. PKG/questions.py:70-76 `closure_evidence`, `never_read`, and `CLOSURE_EVIDENCE` (:25). PKG/commands.py:142 `Deps.extra`. PKG/collector.py: remove the `question_fixture` argument, state and replay (:97, :102-104, :134-140); keep `read_questions` as a 2-line stub returning FAILED with code `no-question-fixture` (the CycleSource protocol needs it). Tests: delete TESTS/test_terminal.py:56-59 and :73-82 (not :65-70, see T9); edit :126 (drop the `box_style` assert), :132-133 (use `selected`), and the `box` and `palette_style` imports; delete TESTS/test_adapter.py:719; in TESTS/test_collector.py keep :662-666 and delete :667-678; rewrite TESTS/test_fixtures.py:44 and :139-151 through `parse_page` plus `apply_frozen` (that test is spec test T34 and must stay); edit only TESTS/test_questions.py:46, :52, :98. Surviving guards: no-blink test TESTS/test_render.py:182-190; `--fixture` with `--questions` refused at commands.py:177-178; ASCII boxes `safe_box` test TESTS/test_terminal.py:142-149; closure wording pins at view.py:65 and :693; the rewritten T34 test; exact code check TESTS/test_adapter.py:718.

T9 (CUT-SMALLER, confidence 70). Delete TESTS/test_terminal.py:65-70 (the decorator and `test_no_blink_code_in_any_console_output`, with the T28 header at :62) in the same change as R1; keep TESTS/test_render.py:182-190, which checks the real screen at every width and both colour modes.

### Step 2: R3 and R2

R3 (CUT-SMALLER, confidence 75). Delete `ParsedPage.unrecognised_keys` (PKG/parse.py:177) and its sum (:409); `Coverage.unrecognised_keys` (:195) and its sum (:647). Keep `_FIELDS`, `_KNOWN`, `_count_unexpected`, `_BLOCK_FIELDS` (:91-93, the sanitizer block mode), the per-row count (:155, :356) and the inspector line (PKG/view.py:407). Surviving guards: TESTS/test_parse.py:188 and :198, TESTS/test_fixtures.py:145 and :166, TESTS/test_view.py:722 (adjust only the assertions that read the two removed aggregate counters).

R2 (CUT-SMALLER, confidence 80). Delete `QuestionsPanel.count_text` (PKG/view.py:209) and its assignment (:732); drop `open_text` only if it becomes unused. Keep the other 21 fields; no comment edits. Surviving guards: panel tests TESTS/test_question_cap.py:71-134, the questions-off golden (TESTS/test_render.py:616-629), and the export reads of `open_total`, `window_full`, `retained`, `evicted` (PKG/export.py:165-168).

### Step 3: S2

S2 (CUT-SMALLER, confidence 77). PKG/export.py: remove the `resources` import (:14), the `Draft7Validator` import (:18), `SCHEMA_PACKAGE` and `SCHEMA_FILE` (:24-25), and the schema load plus `check_schema` (:29-34). Keep `SCHEMA_VERSION` (:23, used at :195). Define `SCHEMA` in TESTS/conftest.py (read the schema file, run `Draft7Validator.check_schema`); update the imports at TESTS/test_commands.py:34 and TESTS/test_snapshot_schema.py:15. After the move, TESTS/test_snapshot_schema.py:60 compares the file with itself; keep :61-62 and the closed-object checks. Surviving guard: TESTS/test_snapshot_schema.py:54-72 (draft 7, closed producer side).

### Step 4: test-only changes T8, T5, T7

T8 (CUT-SMALLER, confidence 89). TESTS/test_render.py:95-100: replace the assertion that ends in `or True` with `assert len(overflow) == 1`; keep all 27 cases. Run it; if it fails, that is a finding to report, not a reason to loosen it.

T5 (CUT-SMALLER, confidence 70). Delete TESTS/test_question_quiet_scope.py:192-203 only (the tests of the fake mailbox itself). Keep :137-145, :148-171, :174-179, :182-189; the fake asserts the exact argv on every call (:68-76), and TESTS/test_adapter.py:158-192 keeps the forbidden-prefix tests.

T7 (CUT-SMALLER, confidence 75). TESTS/test_golden_contract.py:214-215 and :518-519 (the duplicated SENSITIVE loops) only. Keep :213 and :517 (`isascii`), :216 (the 32-character rule), :520 (Run, terminal and message id rule), :521-527. Drop the `SENSITIVE` import there only if it becomes unused. Surviving guard: TESTS/test_fixtures.py:185-191 runs the same scan over every packaged fixture, goldens included.

### Step 5: text and help (documents and one comment and help text)

D2 (CUT-SMALLER, confidence 77). Change the QUESTION-OBSERVATION status lines only, so they say it passed on 2026-11-12 and cite `.dev/issues/409/owner-pass-record-20261112.md`: .dev/issues/409/bmad/prd-orca-observer/prd.md:106 and :491; SPECDIR/unverified-register.md:27; SPECDIR/adapter-contract.md:3 and :62; SPECDIR/rendering-rules.md:89; PKG/commands.py:63-66 (comment), :86-88 (HELP text) and :452-453 (`--questions` help). Do not touch `QUESTION_GATE_TEXT`, any DIRECTION-SELECTED line, or the untracked handoff-mvp-brainstorm.md. `release-gates.md` lines 12 and 38 are already correct. Run TESTS/test_commands.py after the help text edit.

D1 (CUT-SMALLER, confidence 70). In place only: mark open owner decision 6 (permission to read the question scope) and decision 8 (what identifies a human question) as decided by `.dev/issues/409/owner-decisions-20261111.md` in SPECDIR/SPEC.md:104 and :106 and SPECDIR/owner-decisions-and-risks.md:22 and :24; check .dev/issues/409/bmad/prd-orca-observer/prd.md:423 and :469 and fix the same rows if they still read open. No collapse of the lists, no pointer in place of prd.md section 12.1 (the OQ-n labels exist only there). Decision 5 (fallback date) stays open.

D13 (CUT-SMALLER, confidence 70). SPECDIR/acceptance-tests.md: add the snapshot schema test id (TESTS/test_snapshot_schema.py); mark T7, T17, T45 and T50 "not built / no automated test" with the reason (T7 cannot run as written: PKG/commands.py:177-178 refuses `--questions` with `--fixture`); strike nothing. Rows T45 (OQ-13) and T50 (AC-S) keep their references.

## Acceptance for the whole package

- After the last task: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` passes and ruff is clean; the final test count equals 694 minus the tests the tasks removed.
- `grep -rn "run-use" src/superclaude/cli/observe/` still shows `run-use` only in the forbidden set and the help text that says the observer never runs it.
- `git status --short` shows changes only in the files named above, `.dev/issues/409/` and this package.
