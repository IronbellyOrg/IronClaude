# Ponytail review: observer tests and fixtures

Reviewer: ponytail-tests (lite level). Date: 2026-11-16. Branch 409-Phase2.
Scope: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/ and /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/fixtures/. Read-only review; this file is the only thing written.

## Summary

- The suite is 694 tests in 22 seconds. It is sound on the six safety rules, but about 1,000 to 1,300 of the roughly 9,600 test lines are removable with no loss: duplicate argv checks, tests of the recorder scripts, tests of test fakes, tests of fixture contents, and source-text grep tests.
- The rules are each guarded in more than one place, so every trim below leaves a named surviving test. One vacuous assertion (`or True`) at /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_render.py:95-100 guards nothing and should be fixed, not kept.
- The golden whole-screen file has caused no churn (one commit in its history); keep it, optionally cut to two variants.

## Measurements

Run once: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q --durations=8` gave 694 passed in 22.15 s. Slowest: test_collector.py thread-publish test 5.4 s, the pty key tests about 4 s together, the real-subprocess kill test 1.5 s. Everything else is under 0.5 s, so run time is not the cost; reading and maintenance are.

Source: 4,555 lines in /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/*.py.

Test functions per file (count of `def test_`, lines from `wc -l`):

| File | Tests | Lines |
|---|---|---|
| test_view.py | 45 | 1100 |
| test_render.py | 44 | 843 |
| test_adapter.py | 43 | 752 |
| test_parse.py | 36 | 646 |
| test_commands.py | 30 | 750 |
| test_collector.py | 29 | 678 |
| test_snapshot_schema.py | 20 | 558 |
| test_golden_contract.py | 19 | 638 |
| test_session.py | 19 | 433 |
| test_fixtures.py | 22 | 324 |
| test_export.py | 17 | 309 |
| test_terminal.py | 17 | 231 |
| test_questions.py | 15 | 180 |
| test_sanitize.py | 10 | 122 |
| test_keys_spike.py | 8 | 270 |
| test_inspector_scroll.py | 7 | 104 |
| test_question_cap.py | 6 | 156 |
| test_question_quiet_scope.py | 5 | 203 |
| test_registration.py | 5 | 71 |
| test_cancel.py | 3 | 80 |
| test_deep_nesting.py | 2 | 38 |
| conftest.py (helpers) | 0 | 306 |
| record_golden.py and record_golden_questions.py (dev scripts) | 0 | 385 + 297 |
| spike_child.py and release1_surface.py (helpers) | 0 | 103 + 62 |

The 694 runs exceed the roughly 440 test functions because of parametrize (test_render matrix alone is 27 cases; test_snapshot_schema and test_collector run 10 variants each).

Fixtures in /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/fixtures/: 19 JSON files; 1,520 lines of the total are question-cap-100.json and 317 are the four golden-question files. Every file name appears in at least one file under tests/observe (substring grep; "base" and "empty" are loose matches, so a real load of those two is UNVERIFIED). No orphan fixture found. History: fixtures 2 commits, tests/observe 6 commits.

`git log --oneline -- tests/observe/golden_release1_surface.json` prints one commit (c69ce4b3a). No churn so far.

## Keep

Each of these fails on a real defect in one of the six rules. Do not touch them. (Paths below are under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/.)

1. Read-only argv guard: test_adapter.py:242-299 (unlisted argv rejected; every forbidden prefix rejected in every position; templates pass), test_adapter.py:636-700 (the one message template and its neighbours), test_question_cap.py:137-156 (every real message argv has `--types question`, none has `--peek` or `--ack`), test_commands.py:137 (live once only produces allow-listed argv).
2. No subprocess outside the adapter: test_commands.py:578-594 (a grep test, but the one mechanical check that no other module can shell out).
3. Injection: test_sanitize.py:40-122, test_parse.py:604, test_render.py:154-179 (no ESC, C1 or format character on screen), test_export.py:115, test_view.py:1065.
4. Unknown is never 0 or false: test_view.py:116-165, test_parse.py:154 and :559, test_view.py:1023 and :1038.
5. Source loss never closes a question: test_questions.py:50-101, test_collector.py:543-630, test_view.py:1008.
6. 100-row cap: test_question_cap.py:58-135, test_collector.py:647, test_view.py:1073, test_render.py:547.
7. Output width: test_render.py:67 (base, 3 widths), :463-478 (every screen line fits with the panel, 9 cases), :207 and :223, test_terminal.py:169-202 (clip).
8. Real-process kill and reap: test_adapter.py:519-583, test_cancel.py. Cannot be faked.
9. The questions-off golden: test_render.py:616-629 plus release1_surface.py and golden_release1_surface.json. It compares against release 1 bytes from commit 9e2608b03, not against current code, so it is the only proof of "questions off equals release 1" (T47). Keep.
10. test_deep_nesting.py, test_inspector_scroll.py, test_registration.py: small, each guards one concrete failure.
11. All 19 fixtures. question-cap-100.json is the recorded shape of the 100-row cap and test_question_cap.py:58 loads it.

## Trim candidates (ranked by lines saved)

Paths are under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/ unless full. "Read" means I read the live lines; UNVERIFIED means I judged from test names or a partial read.

### 1. Golden whole-screen file: cut from 5 variants to 2 (about 320 lines, optional)
- Where: golden_release1_surface.json (545 lines), `VARIANTS` at release1_surface.py:25, consumer test_render.py:616-629. Read.
- What: it stores 5 variants x (3 widths x 2 heights of screen lines, 3 printed screens, record text, snapshot JSON). Only one commit has touched it, so it has forced no churn yet; the risk is a future wording change to release 1 text, which fails every variant at once.
- Trim: keep `base` and `injection`; drop `empty`, `source-loss`, `missing-fields` (those three states are already pinned by test_view.py:1008, :1023, :116 on current code, but not against release 1 bytes, so this loses a little T47 strength).
- Surviving guard: the same test on 2 variants. Do this one only if reading cost matters more than the extra T47 coverage.

### 2. Recorder tests in test_golden_contract.py (about 221 lines, 6 tests)
- Where: test_golden_contract.py:219-366 (synthetic envelope, three redaction tests, "four kinds derived from one sample") and :540-638 (two recorder tests: redacts ids and bodies; run ids inside an error message). Lines 219-366 Read; 540-638 judged from names (UNVERIFIED).
- What: they test the dev scripts record_golden.py and record_golden_questions.py (682 lines), not the observer. The committed output is already scanned for paths, handles, tokens, URLs and escape bytes.
- Rule duplicated: no sensitive data in fixtures. Surviving guard: test_fixtures.py:185-191 (scans every committed .json) plus the question-specific scan at test_golden_contract.py:508-521.
- Open decision: if the owner will rerun the recorders on a real Orca capture, keep the one test at :282 (redaction of identifiers) and delete the rest (about 170 lines saved). If the recorders are one-shot, delete the scripts too (682 more lines, not counted here).

### 3. Pty key tests: reduce test_keys_spike.py and spike_child.py (about 170 lines, UNVERIFIED line split)
- Where: test_keys_spike.py:117-222 (lone escape, key burst while repainting, SIGTSTP/SIGCONT, resize repaint within 1 s) and the matching modes in spike_child.py (103 lines). File header read; bodies not read.
- What: 8 tests, about 4 s, skipped without pexpect. None of the six safety rules depends on them. They guard terminal restore and key reading.
- Trim: keep `test_terminal_attributes_restored` (:153, the q and exception cases; a terminal left in cbreak is a real user harm) and the pure decoder tests at :224-270. Drop the SIGTSTP, resize and burst tests unless a real defect was seen in those paths (I did not find one in git; UNVERIFIED).
- Surviving guard: test_keys_spike.py:153 and :242; test_commands.py:303 (scripted keys restore the terminal).

### 4. Tests of test support and of fixture contents in test_fixtures.py (about 150 lines)
- Where: :81-134 (80 rows and 8 runs; "empty has no rows"; uneven, shared, historical shapes; long identifiers; duplicate variant; read) and :208-308 (guard tests for the subprocess blocker, fake runner, fake clock, make_rows, console factory; :208-230 read, :232-308 judged from names, UNVERIFIED).
- What: they check the test data and the test fakes themselves. If a fixture changes shape, the consuming tests (test_view, test_render, test_collector) fail anyway. Keep :36-72 (loader works, unsafe names refused, replay), :139-167 (frozen marker), :185-202 (leak scan), :310-324.
- Surviving guard: the consuming tests. Careful: :208-218 (subprocess blocked by default) is the thing that stops a test from spawning real Orca; keep those two.

### 5. test_question_quiet_scope.py: tests of the test fake (about 64 lines)
- Where: :148-171 (observer sends no consuming argv), :174-179 (a consuming fake is detected), :182-189 (check sees a new question), :192-203 (the fake refuses consuming argv), plus the `consuming` branch of FakeOrcaMailbox at :48 and :78-81. Read.
- What: :174, :182 and :192 test the fake and the harness, not product code. :148 repeats the real adapter guard.
- Rule duplicated: no consuming argv. Surviving guard: test_adapter.py:242-299 (rejected before any call), test_question_cap.py:137-156, and test_question_quiet_scope.py:137 (repeated reads leave the mailbox fingerprint unchanged, which is the one test that shows the observer has no write effect).

### 6. Source-text grep tests (about 79 lines, 6 tests)
- Where: test_adapter.py:158-192 (counts `"check"` and flag words in adapter.py text; Read), test_adapter.py:585-589 (import layering; Read), test_view.py:864-869 (Read), test_export.py:238-244 (Read), test_terminal.py:214-231 (Read), test_collector.py:414-421 (Read).
- What: they restate how the implementation is written (text counts, import lines). The first breaks the moment someone adds a comment containing `--wait` or a second `"check"` template. They catch layering drift, which is not one of the six rules.
- Rule duplicated: read-only argv (adapter 158). Surviving guard: the runtime rejection tests in Keep item 1, and test_commands.py:578-594 (no subprocess import outside the adapter). Layering drift tests can go; if the team wants one, keep test_adapter.py:585 only.

### 7. Duplicate leak scans (about 20 lines)
- Where: test_golden_contract.py:206-216 and :508-521. Read.
- What: test_fixtures.py:185-191 already scans every .json in the fixtures package with the same SENSITIVE patterns, and that includes the golden and question golden files. The two extra checks (32-character token regex, `run_`/`msg_` id regex) are the only new content.
- Trim: move those two regexes into the single test in test_fixtures.py and delete the two parametrized copies. Surviving guard: that one test.

### 8. test_render.py matrix and vacuous assert (6 lines, 24 cases)
- Where: test_render.py:80-107 (27 cases: 3 widths x 3 runs x 3 row counts). Read.
- Defect: lines 95-100 `assert (len(overflow) == 1 and overflow[0].startswith(f"{... if False else ''}") is True or True)` always passes. Replace with `assert len(overflow) == 1`.
- Trim: parametrize `n_rows` over [50, 100] and `n_runs` over [5, 10] only (12 cases), or use one case per width at (100, 10). The width rule is also guarded at :67 (3 cases) and :463-478 (9 cases).

### 9. No-blink duplicate (9 lines)
- Where: test_render.py:182-190 repeats test_terminal.py:65-71. Read. Blink is not one of the six rules. Keep test_terminal.py:65.

### 10. Variant parametrization (cases only, no lines)
- test_snapshot_schema.py:80 and :297 and test_collector.py:372 run every one of 10 variants through every cycle. Three variants (`base`, `missing-fields`, `injection`) carry the same rules (schema valid, unknown strings, no forbidden keys). Saves about 14 cases of the 694 and under 1 s. Low value; do only if touching those files anyway.

Estimated total: about 720 test lines plus 320 JSON lines (about 1,040), 70 to 80 fewer cases at no change in the six guards. UNVERIFIED parts above (items 2 second half, 3, 4 second half) could move the total by 100 to 150 lines either way.

### Not recommended to trim
- test_view.py literal-pinning tests (:238-339, :911-1100, the `fNN` and `tNN` tests). They pin wording, so they break on text edits, but the literals are the contract in the PRD rendering rules and several are the "not proof / unknown / 100+" disclosures. Wording churn is the price of that contract. I did not read all of them (UNVERIFIED which ones restate a constant rather than check behaviour; test_view.py:455 `test_format_age` is the most likely candidate).
- test_parse.py and test_session.py: no duplication found in the names; not read in full.

## Open questions this component is connected to

From /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/prd-orca-observer/prd.md lines 415-473 (read).

- OQ-3 command name: test_registration.py:15-71 pins `observe` in the group, help and main.py. The suite assumes the recommended name; a rename touches about 5 tests. It does not justify the name, only follows the recommendation.
- OQ-5 sample capture: the four golden-question files and four golden-worker files are the redacted samples, and the recorder tests (trim 2) exist for that permission. The suite shows the redaction works on a synthetic envelope; it does not show a real capture was done (UNVERIFIED; no evidence read).
- OQ-6 message-content exposure: the suite already acts as if "no body, handle or payload ever" were decided: test_view.py:1086, test_parse.py:586, test_snapshot_schema.py:491 and :297. If the owner allows more display or export, those tests change. So the suite pre-empts the answer to its most restrictive reading.
- OQ-7 (decided, coordinator questions only): justified by test_parse.py:531 (status rows dropped and counted) and the `--types question` check in test_question_cap.py:137.
- OQ-12 row order: test_snapshot_schema.py:343 and test_view.py:811 pin timestamp order, newest first, untimed last. If the owner picks the ledger's source order, both change.
- OQ-14 width matrix: test_render.py `WIDTHS = (160, 116, 80)` pins the A width set and the 80-column floor (:223); heights 14, 24, 40 at :463. B's coordinates and C's 44-row contract are not tested (UNVERIFIED; no matching test names).
- OQ-15 `stage.detail` and `activity` in the snapshot: test_snapshot_schema.py:297-327 fails if either value appears in a snapshot, so the suite decides "inspector only, not in the snapshot". Flip the answer and that test must change.
- OI-6: the PRD says no test pins "selected <id> no longer in source window". test_view.py:688 (`a_selected_row_that_left_the_source_stays_selected_with_a_placeholder`) and test_render.py:383 (selection placeholder line) now exist. The PRD line looks stale (UNVERIFIED which literal each test asserts).
- Not tied to any test: OQ-1, OQ-2, OQ-4, OQ-8, OQ-9, OQ-10, OQ-11, OQ-13 (the only `k of N` check is the loose `k <= n` regex at test_render.py:92; header placement is not pinned, UNVERIFIED), OI-1 (per-call timeout is injected by the fake, test_adapter.py:473).

## Not checked

- Bodies of test_parse.py, test_session.py, test_collector.py (apart from names and :414-421), test_export.py (apart from :238-244), most of test_view.py and test_render.py beyond the ranges quoted. Duplication inside them was judged from test names only.
- Whether `base` and `empty` fixtures are loaded by name in any test beyond substring matches.
- Whether any test fails if a fixture is mutated (no mutation testing run). The claim "the consuming tests fail anyway" in trims 4 and 5 is reasoning, not an experiment. Safest check before deleting: remove one candidate at a time and run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q`; I did not do this because the brief makes me read-only.
- The pexpect-skipped state: pexpect was present here (the key tests ran); on a machine without it, test_keys_spike.py silently skips.
- Time per test beyond the top 8 durations.
- The recorder scripts record_golden.py and record_golden_questions.py were not read.
