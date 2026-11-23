# Reviewer 2 brief (qa persona, model class haiku)

## T1 card excerpt

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
F3. A source requirement is dropped. source.md:49-53 ("Acceptance for the whole package") has three checks: the final pytest count equals 694 minus removed tests, the `grep -rn "run-use"` check, and the `git status --short` scope check. The plan has no whole-package acceptance and no task that runs those checks; plan:21, :123 and :127 mention run-use only as a "keep" instruction. The final count is never stated (the plan only says Task 1 removes 9 cases and Task 9 removes 1, so 684).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T20:41Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp

### .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/source.md:1-53
```markdown
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
```

### .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:1-27
```markdown
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
- Facts the debate found false in the earlier proposal, not to be repeated: the R1 test ranges were too wide, R3 must not drop the five parsed row fields, T9 keeps the `test_render.py` copy and deletes the `test_terminal.py` copy, T7 keeps the 32-character rule and the id rule, T8 keeps all 27 cases, D1 touches owner decisions 6 and 8 only.

## Phase 1: Remove production code that only tests call (R1 and T9)
```

### .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:117-149
```markdown
## Phase 3: Correct stale status text (D2, D1, D13)

## Task 10: State that QUESTION-OBSERVATION passed on 2026-11-12 where it still says not passed (D2)

Depends on: Task 4

Change the QUESTION-OBSERVATION status wording only, so each place says the gate passed on 2026-11-12 on the terms of the owner-written record `.dev/issues/409/owner-pass-record-20261112.md` (cite that path): `.dev/issues/409/bmad/prd-orca-observer/prd.md` lines 106 and 491; `.dev/issues/409/bmad/spec-orca-observer/unverified-register.md` line 27; `.dev/issues/409/bmad/spec-orca-observer/adapter-contract.md` lines 3 and 62 (line 62 also says the owner has not named the Run; the owner record names `run_93bfa00cae2b`); `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` line 89; and in `src/superclaude/cli/observe/commands.py` the comment above `QUESTION_GATE_PASSED` (:63-66), the HELP text (:86-88, "off until the owner records that QUESTION-OBSERVATION passed") and the `--questions` option help (:452-453, "refused until QUESTION-OBSERVATION has passed"). Do not edit `QUESTION_GATE_TEXT` (pinned), any DIRECTION-SELECTED line, `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` (lines 12 and 38 are already correct) or the untracked `handoff-mvp-brainstorm.md`. Keep the disclosure label and the sentence that the observer never runs run-use in the help text.

Acceptance criteria:
- Grep for `NOT passed`, `not passed` and `has not passed` near QUESTION-OBSERVATION in the files above finds no live claim that the gate has not passed; the refusal text `question read not enabled: QUESTION-OBSERVATION has not passed` in `QUESTION_GATE_TEXT` is unchanged.
- `uv run pytest tests/observe/test_commands.py tests/observe/test_registration.py -q` passes, including the tests that read the help text (`never runs run-use`, the disclosure label, `one named Run`).
- No other line of these files changes (`git diff` is limited to the status wording); the full gate passes with the passed count unchanged.

## Task 11: Mark owner decisions 6 and 8 as decided where they are still listed as open (D1)

Depends on: Task 10

In place only, mark open owner decision 6 (permission to read the question scope) and open owner decision 8 (what identifies a human question) as decided by `.dev/issues/409/owner-decisions-20261111.md` (decision 6: "Permission granted, proceed", one named Run, `--types question`, never run-use; decision 8: "coordinator questions only") in `.dev/issues/409/bmad/spec-orca-observer/SPEC.md` lines 104 and 106 and `.dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md` lines 22 and 24; check `.dev/issues/409/bmad/prd-orca-observer/prd.md` lines 423 (OQ-5) and 469 (12.3 item 6) and fix the same rows if they still read as open. Do not collapse the lists, do not replace prd.md section 12.1 with a pointer (the OQ-n labels exist only there), and leave decision 5 (fallback date) open.

Acceptance criteria:
- Each of the rows named above says decided and cites `owner-decisions-20261111.md` by path; the decision numbering and the OQ-n labels still resolve (Grep for `OQ-5` and `open owner decision 6` finds the same labels as before).
- Decision 5 (fallback date) and every other open row are unchanged (`git diff` touches only the rows named).
- The gate passes with the passed count unchanged (document-only task).

## Task 12: Correct the test-id bookkeeping in acceptance-tests.md (D13)

Edit `.dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md`. In the section "Snapshot schema test (CAP-10, recorded owner decision 2)" (about line 64-66) replace "Test ID not yet assigned." with the real test file, `tests/observe/test_snapshot_schema.py`. Mark T7, T17, T45 and T50 as "not built / no automated test" with a reason: T7 and T17 are defined inside the AC-3 and AC-6 mapping rows (about lines 25 and 28), so add the note there (T7 cannot run as written because `src/superclaude/cli/observe/commands.py:177-178` refuses `--questions` with `--fixture`; for T17 state that no test cites it); T45 and T50 are table rows (about lines 51 and 56): T45's `read k of N Runs since start` header text is not built, and T50 is a reviewer check on design images, not a test. Re-grep the live file for the exact lines first. Strike nothing; the T45 (OQ-13) and T50 (AC-S input) references stay.

Acceptance criteria:
- The four test ids each carry the words `not built` or `no automated test` with a stated reason, and the snapshot schema section names `tests/observe/test_snapshot_schema.py` instead of "not yet assigned".
- Every test id and table row that existed before the edit is still present (compare `grep -c` of the `| T<n> |` rows and of the ids T1 to T56 before and after), and the OQ-13 and AC-S input references are intact.
- The gate passes with the passed count unchanged (document-only task).
```

### src/superclaude/cli/observe/commands.py:60-93
```python
)
WIDTHS = ("160", "116", "80")

# The live coordinator-questions read is guarded by this one constant. It stays False until
# the owner has given a record that QUESTION-OBSERVATION passed (release-gates.md, "Agents
# cite the owner's statement"); plan Task 18 flips it only against that
# record, cited by path. While False, ``--questions`` makes no Orca call, not even discovery.
QUESTION_GATE_PASSED = True  # owner record: .dev/issues/409/owner-pass-record-20261112.md
QUESTION_GATE_TEXT = (
    "question read not enabled: QUESTION-OBSERVATION has not passed"  # PROPOSED wording
)
QUESTIONS_NEED_RUN_TEXT = (
    "--questions needs --run <runId>: it reads the questions of one named Run only"
)
QUESTIONS_NEED_LIVE_TEXT = (
    "--questions needs a live source; it cannot be combined with --fixture"
)

HELP = """Read-only terminal observer for Orca workers.

Shows the worker ledger Orca reports for its workers (verbatim next-action kind,
freshness, collected / reported counts) and can write a plain-text record and a versioned JSON
snapshot. It never writes to Orca: no key and no option maps to an Orca call.

Poll caps (one read every 15 s, at most 5 calls per read) are per observer process; several
observers running at once multiply the load on Orca.

Coordinator questions (--questions, off until the owner records that QUESTION-OBSERVATION
passed): with --run <runId> the observer lists the messages of type question of that one
named Run, from one read per cycle. Run it from the terminal that already holds the Run: the
observer never runs run-use and never binds to a Run. The list is bounded best effort;
coverage unknown; bursts over 100 rows between reads may be lost. Message bodies are
received by this process; subjects are shown, bodies are not kept.
"""
```

### src/superclaude/cli/observe/commands.py:441-455
```python
@click.option(
    "--snapshot",
    "snapshot",
    type=click.Path(dir_okay=False),
    default=None,
    help="Write the JSON snapshot to this file (default for live mode: the per-user state directory).",
)
@click.option(
    "--questions",
    "questions",
    is_flag=True,
    help="List the coordinator questions (message type question) of the one Run named by "
    "--run. Needs --run and a live source; refused until QUESTION-OBSERVATION has passed.",
)
@click.pass_context
```

### .dev/issues/409/bmad/prd-orca-observer/prd.md:106-106
```markdown
| R2 Attention Ledger (B) | `COORDINATOR QUESTIONS` for one named Run (messages of type `question` only), with observer-side retention, the 100-row disclosure, "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost". One Run only, no rotation. | QUESTION-OBSERVATION: **NOT passed**. Candidate verb, never an available source until the open items are recorded: `orca orchestration check --all --types question --run <runId> --json` for one named Run, never `run-use`, one message call per cycle inside the 5-call cap. Open items (`release-gates.md`): Q-1 (an observer terminal with a handle but no Run, UNVERIFIED), the message rate and identity on the Run the owner names (the owner has not named it), and the owner's written pass record. Seen on probe Runs only: the read returns only the bound Run's mailbox (`consumer_fenced` for another Run), and non-consumption as the Run's owner for the visible effects tested (INV-022, T51). Question identity is `message.id`, a worker `dispatchId` is never a question's identity. Owner decisions 8 and 6 decided 2026-11-11 (coordinator questions only; one named Run, `--types question`, never `run-use`). | Closed |
```

### .dev/issues/409/bmad/prd-orca-observer/prd.md:491-491
```markdown
| U3 | QUESTION-OBSERVATION open items: Q-1, message rate and identity on the named Run, the owner's written pass record (proof (a) as first worded is withdrawn, `release-gates.md`) | Gate stays closed (NOT passed) |
```

### .dev/issues/409/bmad/prd-orca-observer/prd.md:419-427
```markdown
- **OQ-1.** Does the owner's staged choice satisfy DIRECTION-SELECTED, and where is the dated owner-written selection record?
- **OQ-2.** Which production-integration reading applies (1: registering the command or any live subprocess outside the fake runner; 2: wiring into the shipped product)?
- **OQ-3.** Final command name (recommended `superclaude observe`)?
- **OQ-4.** Fallback date for QUESTION-OBSERVATION?
- **OQ-5.** Sample capture and acquisition permission for live reads (open owner decision 6)?
- **OQ-6.** Message-content exposure (open owner decision 7)?
- **OQ-7.** Decided 2026-11-11 (OWNER, `owner-decisions-20261111.md`): coordinator questions only (message type `question`); the list is not labelled "human".
- **OQ-8.** Multi-observer restriction (open owner decision 9)?
- **OQ-9.** Licence opinion before any Go screen reads the snapshot?
```

### .dev/issues/409/bmad/prd-orca-observer/prd.md:466-470
```markdown
3. **Command name and placement.** Recommend `superclaude observe`, registered in `cli/main.py` (deferred import, then `add_command`). The name is the owner's. (OQ-3)
4. **Production-integration boundary.** Reading 1 (V1) or reading 2 (V3), both UNVERIFIED; the stricter applies until confirmed. (OQ-2)
5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option. (OQ-4)
6. **Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, with the owner setting redaction rules. Unblocks B's headline panel. (OQ-5)
7. **Message-content exposure.** What may be displayed and what exported, kept as separate permissions; no recommendation beyond that. (OQ-6)
```

### .dev/issues/409/bmad/spec-orca-observer/SPEC.md:100-108
```markdown
- Does the owner's staged choice satisfy DIRECTION-SELECTED, and where is the dated owner-written selection record?
- Which production-integration reading applies (1: registering the command or any live subprocess outside the fake runner; 2: wiring into the shipped product)?
- Final command name (recommended `superclaude observe`)?
- Fallback date for QUESTION-OBSERVATION?
- Sample capture and acquisition permission for live reads (open owner decision 6)?
- Message-content exposure (open owner decision 7)?
- What identifies a human question (open owner decision 8)?
- Multi-observer restriction (open owner decision 9)?
- Licence opinion before any Go screen reads the snapshot?
```

### .dev/issues/409/bmad/spec-orca-observer/owner-decisions-and-risks.md:18-26
```markdown
2. **Stack.** Settled by recorded owner decision 2 above (the source listed it as open; it departed from the issue's Go Bubble Tea v2 preference).
3. **Command name and placement.** Recommend `superclaude observe`, registered in `cli/main.py` (deferred import, then `add_command`). Name is the owner's.
4. **Production-integration boundary.** Reading 1 (V1) or reading 2 (V3), both UNVERIFIED; stricter applies until confirmed (`release-gates.md`).
5. **Fallback deadline.** Date by which QUESTION-OBSERVATION must pass; expiry triggers re-confirmation, never a switch. Recommend A on the same adapter as the re-confirm option.
6. **Sample capture and acquisition permission.** Permission to capture one non-empty redacted sample from the candidate `check --all` read; acquisition permission must cover the actual read scope before any message call, separate from display and export. Recommend yes, owner sets redaction rules. Unblocks B's headline panel.
7. **Message-content exposure.** What may be displayed and what exported; kept as separate permissions; no recommendation beyond that.
8. **Question-type choices.** What makes a message a "human question", which `type` values count, which handle or Run carries it. Needs the owner or Orca. Recommend an explicit message type, never text inference.
9. **Multi-observer restriction.** Caps are per process, no singleton. Recommend disclosure only.
10. **Still open from owner-decisions-20261108.md:** write-back stage (summary decision 3), TUIBBS licence opinion (decision 4), TUIBBS as staff platform (decision 5).
```

### .dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md:21-31
```markdown
| AC | Requirement | Tests |
|---|---|---|
| AC-1 | Read-only, no consuming check | T1: across every adapter path, argv equals one exact template (`adapter-contract.md`): the `worker-list` template per cycle, plus at most one `skills list --json` discovery probe per candidate (at most two) before the first cycle, intercepted by patching the `subprocess.run` that `_find_orca()` calls. T2: static test that `--ack`, `--wait`, `--retry-request`, `--peek` and `run-use` appear in the adapter module only inside the forbidden set, and `check` appears only there and in the one R2 message template. T3: no key maps to an Orca call. |
| AC-2 | Deterministic, bounded collection | T4: a fake always returning `hasMore=true` stops at the 5-call cap and renders `PARTIAL: collected 500 of reported T`. T5: a fake sleeping past a configured per-call timeout injected into the fake runner (the real value is measured at the first permitted live read) shows `FAILED (timeout)`; the cycle ends within the 15 s budget. T6: same input renders byte-identical text twice. |
| AC-3 | Attention items, reasons, scope, changes since last look, evidence | T7: `base` (8 orchestrators, 80 sessions) in fixture mode lists every question oldest first with requester/owner and affected IDs. T8: after `m`, a fixture step changing one `nextAction.kind` stars exactly that row and shows `changed since HH:MM (1)`. T9: live mode with no message source shows `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` (`rendering-rules.md`) and titles the ledger `worker-reported, not questions`. |
| AC-4 | Seen is not resolved | T10: `m` on every item leaves the open count unchanged. T11: `source-loss` keeps the open count and every retained item; nothing becomes resolved or failed. T12: an item missing next cycle stays, marked `no longer in source window`. |
| AC-5 | Separate lifecycle, outcome, report, acceptance, tests, approval; unknown never 0/false | T13: `missing-fields` renders `unknown` for every absent field; `0`/`false` never stand in (asserted per field). T14: `terminalState=released` with `outcome` absent never renders `done`, `complete` or `settled`. T15: report, acceptance, tests and approval each render `unavailable (no source)` live; no row or inspector ever renders `admitted` from evidence fields (inspectable evidence is not admission). |
| AC-6 | Filtered and global counts with denominators; 100-row cap disclosed | T16: matrix {5, 8, 10 orchestrators} x {50, 80, 100 sessions} x {160, 116, 80 columns} (27 renders); every count line matches `k of n`, every hidden overflow shows `x/y shown` with y = fixture total. T17: `uneven` per-owner counts sum to the global count. T18: `page.total=287` with 100 rows shows `collected 100 / reported 287`, never `287 workers`; `page.total` absent shows `reported unknown`. T19 (R2, no longer a placeholder; fake-runner test with `--questions` on): the question panel carries the disclosure verbatim, `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost`, under the title `COORDINATOR QUESTIONS` and the line `one Run only: <runId>`; its first state line reads `question read: OK 3s` (or the other state forms), its counts line reads `seen, not resolved: <n> | closed by evidence: unavailable (no source)`, and `no read marker in source: answered questions stay listed` is present. |
| AC-7 | No one-to-one session/worktree assumption | T20: `shared-unmapped` shows two sessions sharing one worktree as two rows; opening the inspector on each shows the same `resource.worktreeId`, and the inspector of the session with no worktree shows `unknown (absent in source)` for it; no count divides one by the other, and no `conflict` label appears for the shared worktree. |
| AC-8 | Historical records, duplicates, out-of-order | T21: released/retained rows hidden by default with `k historical hidden (h)`; after `h` listed with `terminalState`, not counted active; a row with absent or any other `terminalState` is always shown with its raw value (or `unknown`) and not counted active. T22: `duplicate-out-of-order` shows `k duplicate rows ignored`; an older `observedAt` never overwrites a newer one; a row missing both timestamps is flagged `order unknown`; a backward timestamp shows `conflict (time went back)`. |
| AC-9 | Widths, keyboard, NO_COLOR, export, full IDs, no blink | T23: at 160/116/80 every screen line has `cell_len <= W`. T24: `long-identifiers` truncates with `>` in lists; inspector shows the full ID. T25: reorder between cycles keeps selection on the same row ID. T26: `NO_COLOR=1` and `NO_COLOR=yes` emit no SGR colour; meaning stays readable as words. T27: `e`/`--once` writes the record export: no ESC byte, full IDs, no truncation. T28: SGR 5/6 (blink) never appears. |
```

### .dev/issues/409/bmad/spec-orca-observer/acceptance-tests.md:49-70
```markdown
| T43 | With the selected row visible and others hidden, `+N more` excludes the selected row. | AC-6 |
| T44 | Worker text containing Rich markup (e.g. `[bold]`) renders literally. | AC-10 |
| T45 | Default view chosen at start-up, never switches mid-session; header shows `read k of N Runs since start` (which views carry it is an open question, `SPEC.md`). | AC-3 |
| T46 | For the one named Run, at 1,001 retained questions (distinct Run plus `message.id`), eviction does not lower the seen-not-resolved total; the counts line reads `seen, not resolved: unknown (retention exceeded) (retained 1000)` (and the collapsed one-line summary reads `unknown (retention exceeded)`, never a bare number); oldest first. Test file: `tests/observe/test_questions.py` and `test_view.py`. | AC-4 |
| T47 | With `--questions` off, and before QUESTION-OBSERVATION passes, the question area reads `source UNVERIFIED, 0 rows interpreted, not "no questions"` and the output is byte-identical to release 1; no count from `result.count`; `changed during read` and mismatch notes render per `rendering-rules.md`. Test file: `tests/observe/test_view.py`. | AC-3, AC-6 |
| T48 | Screen renderer and record export read the same view model; an ID truncated with `>` on screen appears in full in the export. | AC-9 |
| T49 | When height cannot hold coverage, scope, PARTIAL and the question-source gap notice ahead of optional panels, a too-small diagnostic shows and still carries the gap notice. | AC-9 |
| T50 | R0 renders of A, B, C at 160/116/80 each carry "synthetic fixture, not live evidence" with a degraded version beside each. | AC-S input |
| T51 | R2, no longer a placeholder (`tests/observe/test_question_quiet_scope.py`): a stateful fake Orca backend over the probe shapes first establishes readable identity (every row has a `msg_` id, a Run id and a created time), then repeated reads on a quiet scope return identical question ids, order and an unchanged fake mailbox state; a consuming fake makes the companion test fail; a pass covers only the visible effects tested, as the Run's owner on a probe Run, and says nothing about a non-owner reader (Q-1) (INV-022). | AC-1 |
| T52 | With the recorded `consumer_fenced` (exit status 1) and `no_active_terminal` error envelopes, the question source is `FAILED` with code `consumer-fenced` or `no-active-terminal`, the panel says `this terminal does not hold the named Run; the observer never binds to a Run`, the worker-list state is unchanged and retained questions stay. Test file: `test_adapter.py`, `test_collector.py`, `test_view.py`. | AC-4, AC-5 |
| T53 | The fake runner receives exactly the R2 message argv `(orca, orchestration, check, --all, --types, question, --run, <runId>, --json)`; `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`, `inbox`, plain `check`, `check --peek`, an unfiltered `check --all` and the template without `--run` are rejected before any call. Test file: `test_adapter.py`. | AC-1 |
| T54 | A 100-row reply (the recorded-shape cap fixture) shows `window full: older questions may be missing` with the disclosure label, the counts line `seen, not resolved: 100+ (window full) | closed by evidence: unavailable (no source)`, and, when the panel is collapsed, the summary count text `100+ (window full)`; a 99-row reply shows none of these and a plain `seen, not resolved: 99`; a moved window keeps dropped questions as `[no longer in source window]` ahead of the subject (only the subject is clipped, so the state word is never cut); an empty good read collapsed reads `0 (source window only; not proof none exist)`; no total is taken from `result.count`. Test file: `test_question_cap.py`. | AC-6, AC-4 |
| T55 | The four recorded redacted samples of the message read (success, missing, stale, contradictory) are each pinned in a contract test: success parses to the expected rows, missing gives `FAILED` with retained questions kept, stale shows `STALE` after 45 s on the monotonic clock, contradictory rows are dropped and counted. Test file: `test_golden_contract.py` and `test_fixtures.py`. | AC-4, AC-5 |
| T56 | While the gate guard constant is off, `--questions` exits non-zero with `question read not enabled: QUESTION-OBSERVATION has not passed` and makes no Orca call, not even discovery. Test file: `test_commands.py`. | AC-1 |

## Snapshot schema test (CAP-10, recorded owner decision 2)

- Validates every R1 snapshot against `snapshot-export-schema.md`; rejects an unknown `schemaVersion` major; asserts missing values are the string `UNKNOWN`; asserts no message bodies, prompts, file contents or credentials. Test ID not yet assigned.

## Reviewer-checked and manual (never reported as automated tests)

- **AC-S:** a reviewer checks the owner's dated selection record exists and names the date, option, who decided, where the owner's statement lives, the pre-observation default, the post-observation default, the post-link choice or deferral, the fallback date, the stack confirmation, the command name and the confirmed production-integration reading (`release-gates.md`). No agent writes the record.
```

### .dev/issues/409/bmad/spec-orca-observer/unverified-register.md:27-27
```markdown
`check --all --types question --run <runId> --json`, for one named Run, is a candidate, never an available source, until the open items in `release-gates.md` (QUESTION-OBSERVATION: not passed) are recorded. Not used in R0 or R1: `check --peek`, the candidate `check --all`, `inbox`. Unfiltered `check --all` and `--peek` are not allowed in any R2 argv; plain `check`, `--ack` and `run-use` are never run.
```

### .dev/issues/409/bmad/spec-orca-observer/adapter-contract.md:62-62
```markdown
- **Acquisition permission (INV-017):** decision 6 is granted for one named Run (OWNER, `owner-decisions-20261111.md`, 2026-11-11: one named Run, `--types question`, never `run-use`), and the Run must be named before the first call (the owner has not named it yet; no message call is made until then). Permission must cover the actual read scope before a message call, separately from display and export permission. Dropping a body at parse time cannot undo its receipt, so the design never claims bodies were not acquired, only that they are not kept or shown; if a narrow read cannot honour the permission the call is skipped. Raw output never enters logs, fixtures or exports. Run-wide consent is not substituted for terminal consent while terminal-attribution fields are UNVERIFIED.
```

### .dev/issues/409/bmad/spec-orca-observer/rendering-rules.md:89-89
```markdown
| Parsing `check --peek/--all` or `inbox --json` rows before QUESTION-OBSERVATION | Row fields UNVERIFIED; `check --all --types question --run <runId> --json` is the one candidate verb, behind the gate (status: not passed). |
```

### .dev/issues/409/owner-pass-record-20261112.md:1-13
```markdown
# QUESTION-OBSERVATION pass record, 2026-11-12

Written by the owner.

QUESTION-OBSERVATION passes for release 2 on these terms:

- I, Ryan wiancko, accept the Q-1 result: FAIL. The observer reads only from the terminal that holds the Run. - accepted on 11/12/2026

- I also accept that The Run is run\_93bfa00cae2b, the coordinator's own Run, read with --types question, one call per cycle.

- I am aware and don't care that message rate and identity on real traffic are unmeasured, and non-consumption by a non-owner reader is unverified.

- It's accepted that The label "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost" stays on screen```

### .dev/issues/409/owner-decisions-20261111.md:1-17
```markdown
# Owner decisions, 2026-11-11 (phase 2 gate)

Source: owner replies in the coordinator session after the phase 2 gate research report
(`.dev/tasks/to-do/TASK-RESEARCH-phase2-gate-20261111-200400/RESEARCH-REPORT-phase2-gate.md`).

| Decision | Owner answer | Meaning for phase 2 |
|---|---|---|
| 8: what identifies a human question | "coordinator questions only" | The list shows only messages of type `question`, labelled "coordinator questions" (not "human"). Worker completion reports and escalations are out of scope. |
| 6: permission to read that scope | "Permission granted, proceed" | The observer may read one named Run's question messages. Read scope as recommended in the report: one named Run, `--types question`, never `run-use`. The owner did not name the Run beyond that; phase 2 plan must state which Run. |

## Coordinator measurement taken after decision 6 (read-only, own Run run_93bfa00cae2b)

- `check --all --run <run>` returned 100 rows (the cap): 91 heartbeat, 8 worker_done, 1 question. A read of the whole mailbox therefore hides most questions behind heartbeats.
- `check --all --run <run> --types question` returned 41 rows. So the cap is applied after the type filter; phase 2 must pass `--types question`.
- A later consuming `check` found 0 pending: the reads did not consume. Tested as the Run's owner only.

Still UNVERIFIED: read from an unbound observer terminal (Q-1), effect of `run-use` on a live coordinator (Q-2), message rate on a Run other than this one.
```


## Coverage slice

| Requirement | Plan item | Status | Grounding |
|---|---|---|---|
| INF-001 | plan Constraints | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:17-25 |
| INF-002 | plan Constraints | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:17-25 |
| INF-003 | plan Constraints | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:17-25 |
| INF-004 | plan Constraints | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:17-25 |
| INF-005 | plan Constraints | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:17-25 |
| INF-006 | plan Constraints | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:17-25 |
| INF-007 | plan Constraints | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:17-25 |
| INF-018 | Task 10 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:119-128 |
| INF-019 | Task 11 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:130-139 |
| INF-020 | Task 12 | covered | .dev/tasks/to-do/TASK-WF-executeNowBrief-20261116-202439/TASK-WF-executeNowBrief-20261116-202439.md:141-148 |
| INF-021 | none | unmapped | source.md:51 |
| INF-022 | none | unmapped | source.md:52 |
| INF-023 | none | unmapped | source.md:53 |
