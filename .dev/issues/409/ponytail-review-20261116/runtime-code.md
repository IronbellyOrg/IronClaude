# Ponytail review: observer runtime code

Reviewer: ponytail-runtime. Date: 2026-11-16. Read-only on product code.
Scope: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/ (all files except export.py, which another reviewer has).
Method: read every in-scope file in full, traced the flow from commands.py down, counted callers with Grep, checked the tests and the spec text. Line numbers were read live on 2026-11-16. Line counts for trims are approximate and say so.

## Summary

1. The runtime is mostly justified: almost every large block traces to a spec test, an owner decision or a safety rule. The weight comes from spec-mandated disclosure text and a three-width layout, not from stray abstractions.
2. About 300 of the roughly 4,280 in-scope lines (about 7 percent) have no verifiable return. The safest 85 are code that only tests call (dead in production). The next largest is the 22-field coordinator-questions panel model, which mirrors strings that could be built once.
3. No safety item is on the trim list. Two items need an owner answer before cutting: inspector scroll (d/u) and the permanently-open question gate constant. The test suite (9,639 lines in /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/) is more than twice the size of the runtime, so any trim also removes tests.

## Keep

All paths below are under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/.

- sanitize.py (48 lines, whole file): escape-sequence injection from worker text (safety c, issue AC 7). Every worker string passes through it in parse.py `_value` and `_clean_json`.
- adapter.py:29-50, 110-208 (argv allowlist, `assert_allowed`, run-id and cursor checks): the only barrier against consuming reads and Orca writes (safety c). It is slightly redundant, since the exact-template allowlist already rejects everything the forbidden-prefix scan rejects, but the scan gives T53 its named error and is cheap. Leave it.
- adapter.py:214-330 (process-group kill, 8 MiB output cap, stderr cap, `cancel_active`): bounded collection (issue AC 9) and no orphan Orca process on quit.
- adapter.py:413-485 `read_pages` paging with cap, cursor and total checks: needed for the 80 to 100 session scenarios (issue AC 6) and the PARTIAL disclosure (AC 3).
- keys.py:36-141 (cbreak, restore on exit, SIGINT/TERM/HUP/TSTP/CONT handlers): terminal never left in a broken mode (safety c); the suspend and resume handlers are pinned by tests/observe/test_keys_spike.py.
- terminal.py `clip`, `resolve_policy`, `make_console`, NO_COLOR, `--ascii`: issue AC 5 (NO_COLOR, ASCII, display-cell width truncation).
- render.py three width layouts (`_columns`, 148-223): issue AC 5 names 160, 116 and 80 columns. The code could be table-driven (see trims) but the three layouts themselves are required.
- collector.py:343-370 (daemon thread, `stop`, `cancel`) and the 15 s interval plus doubling backoff to 60 s (146-198, 315, 330): bounded, deterministic collection (issue AC 9) and no hammering of Orca after failures; pinned by test_collector.py:135-142.
- parse.py `parse_page` strict envelope and lenient rows, `merge` with `not reobserved` and out-of-order flags: issue AC 6 (duplicates, out-of-order, missing fields, historical) and AC 3 (stale, partial).
- parse.py `parse_questions` (464-544): type must be `question`, wrong-Run rows dropped, `body`, `payload` and `to_handle` never kept: owner decisions 6 and 8 (owner-decisions-20261111.md) and the leaked-body safety rule.
- questions.py retention at 1,000: spec test T46 (acceptance-tests.md:52) and owner-decisions-and-risks.md:47. Keep the bound; see the small trim of the evicted-key list below.
- view.py status literals, `source_state` STALE at 45 s, `_changes` and the `m` mark: issue AC 2 ("meaningful changes since last look") and AC 3 (freshness).
- view.py filter `/`, historical toggle `h`: listed keys in rendering-rules.md:21 and the filtered-versus-global counts rule (rendering-rules.md:74); issue AC 6 names historical records.
- commands.py `run_once`, `--width`, `--snapshot`, `--fixture`, `--run`, `--questions` with its refusals before any Orca call: each maps to a spec requirement or owner decision; registered in main.py:572-574 (OQ-3 recommended name `observe`).
- Fixtures (parse.py:685-785, collector.py `FixtureSource.read_pages`): ten variants named in acceptance-tests.md:19 and the SYNTHETIC banner; they let a user see the screen without Orca.

## Trim candidates

Ranked by approximate lines saved. Paths are under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/ and tests under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/. "ROI" means one of the four tests in the brief. Nothing here was run; "risk" is my reading of the callers.

### T1. Coordinator-questions panel model and builder (about 100 lines)

- Where: view.py:52-81 (30 literal lines), 184-239 (`QuestionLine`, `QuestionsPanel` with 22 fields and `window()`), 589-744 (`_questions_panel`, 156 lines); render.py:304-323 (`_panel_lines`) and 369-395 (the panel height budget that rebuilds the panel with `replace(panel, lines=(), empty_text=None)` just to count lines).
- Why no verifiable ROI: the panel itself is required (owner decisions 6 and 8, pass record 2026-11-12, and the disclosure label the owner said must stay on screen). What has no ROI is the shape: `QuestionsPanel` carries the same facts several times as pre-built strings (`title`, `run_line`, `header_cell`, `count_text`, `counts_line`, `summary`, `state_lines`) plus typed copies (`open_total`, `retained`, `evicted`, `window_full`). `replaces_gap` and `summary` exist only to swap one line on the screen. A smaller version builds one `list[str]` of panel lines in view.py and passes the four typed numbers the exporter needs.
- Dependents: export.py:103-116 and 160-168 read `panel.empty_text`, `window_full_text`, `notes`, `open_total`, `window_full`, `retained`, `evicted` (so those must stay); tests test_view.py, test_render.py, test_questions.py, test_golden_contract.py (golden text must stay byte-equal).
- Risk: medium. tests/observe/test_golden_contract.py and record_golden_questions.py exist, so the exact words are probably pinned (I did not open them; UNVERIFIED), which makes the saving real only if the strings stay identical. The "oldest questions stay, newer cut with a count" rule (view.py:222-238, render.py:380) cites an "owner decision, 2026-11-12" that I could not find in owner-decisions-20261108.md, owner-decisions-20261111.md or owner-pass-record-20261112.md (UNVERIFIED; it may be in the release 2 plan). Keep that behaviour until the owner record is found.

### T2. Code that only tests call, dead in production (about 85 lines)

Each item below has zero production callers (Grep over src/superclaude/cli/observe/*.py and tests/observe/*.py):
- terminal.py:41-53 (`PALETTE`, `_FORBIDDEN_ATTRS`) and 161-172 (`palette_style`): about 25 lines. Only test_terminal.py:57-82 calls it. The palette is empty by design (CD-8), so it can never style anything.
- terminal.py:33, 37, 38: glyphs `sep`, `vrule`, `cross` are never looked up (only `selected`, `truncate`, `hrule` are, render.py:124, 139, 241; terminal.py:187). 3 lines.
- terminal.py:72-75 `TerminalPolicy.box_style`: only test_terminal.py:126. 4 lines. (Keep `safe_box=policy.ascii` in `make_console`, terminal.py:146.)
- adapter.py:65-82 `CODES`: only `assert expected in adapter.CODES` at test_adapter.py:719 and a comment at adapter.py:340. 17 lines. Move the set into the test.
- collector.py:97-104 and 128-140 (`FixtureSource.question_fixture`, `FixtureSource.read_questions`): about 17 lines. `--questions` with `--fixture` is refused (commands.py:177-178), so production can never reach it. The only caller is test_collector.py:662-669. Move to a test double.
- parse.py:723-733 `Fixture.parse`: 11 lines. Only test_fixtures.py:44, 141, 149 call it.
- questions.py:70-76 `QuestionState.closure_evidence` and `never_read`: 6 lines. View uses its own literal `QUESTIONS_CLOSED` (view.py:65); only test_questions.py:46-98 call these.
- commands.py:142 `Deps.extra`: 1 line, zero uses anywhere.
- Risk: very low. Delete the matching tests with them. This is the safest first cut.

### T3. Unrecognised-key counter and five parsed-but-never-shown fields (about 42 lines)

- Where: parse.py:91-106 (`_KNOWN` tree), 317-324 (`_count_unexpected`), the count fields at 155, 177, 195, the sums at 356, 409, 647, and view.py:407 (inspector line "N unrecognised keys"). Also five row fields that no code outside parse.py reads: `resource_id`, `ownership_state`, `release_state`, `recovery_attempt_count`, `workspace_kind` (parse.py:65-67, 71, 78 and 124-126, 130, 137).
- Why no verifiable ROI: no issue AC names it and I found no owner decision for it (the module docstring cites AD-7, which I did not trace; UNVERIFIED). The five fields exist only so the counter does not count them as "unrecognised". The two go together: drop the counter and the five fields, or keep both.
- Dependents: test_parse.py, test_fixtures.py (field names), view.py:407.
- Risk: low to medium. The count is a drift alarm if Orca adds keys, a (d)-style behaviour only an owner reading the inspector would notice. Ask whether anyone wants it.

### T4. Inspector scroll with d and u (about 35 lines)

- Where: view.py:93 (`INSPECTOR_SCROLL_STEP`), 127 (`inspector_scroll`), 975-981 (`inspector_line_bound`), 1009-1013 (the d/u branch), `_move` and escape resetting the field; render.py:248-280 (`_inspector_lines` windowing with "n lines above/below"); tests/observe/test_inspector_scroll.py (7 tests).
- Why no verifiable ROI: the spec says the inspector is a full-screen replacement with "no per-panel scrolling" (.dev/issues/409/bmad/architecture-orca-observer/inputs/extract-prd-ux.md:106, and rendering-rules.md:13). The only text asking for d/u is .dev/issues/409/live-test-guide.md:68 and a release 2 task prompt. No owner decision found (UNVERIFIED).
- Counter-argument: the inspector shows about 25 field lines, so on a 24-row terminal something must give; that is a real user behaviour (test (d)). The smaller option is to clip with one "n more lines, e exports all" line and no state.
- Risk: medium. Needs an owner yes or no first.

### T5. Table-driven width layouts (about 25 lines)

- Where: render.py:148-223 `_columns` is 76 lines for three layouts with repeated width arithmetic. A list of (header, width, attribute) per class would be about 50.
- ROI of the layouts themselves: required (issue AC 5). The saving is only in how they are written.
- Risk: medium. I did not open test_golden_contract.py or test_render.py to see how exactly they pin column text (UNVERIFIED); any width rounding change could fail them.

### T6. COUNTS strip priority and cut logic (about 20 lines)

- Where: render.py:87-128 `counts_lines` with protected and unprotected tokens, a 2-line cap and a clip-with-marker branch (`CountsToken.protected`, view.py:131-133).
- Why weak ROI: the denominators must never be cut (issue AC 3), which `protected` guarantees, but a plain wrap of all tokens (never cut anything) meets that rule with about 8 lines, at the cost of a COUNTS strip that may take 3 or 4 lines on an 80-column screen. I did not trace which spec test (T-number) pins the 2-line cap (UNVERIFIED).
- Risk: medium; the strip is on every screen.

### T7. Question fields spread across `CycleResult` (about 15 lines)

- Where: collector.py:55-68 (7 `question_*` fields) and 201-212 (`_carry` copies all seven by hand). One frozen `QuestionRead` dataclass with a single `previous.question` carry would remove `_carry` and the repeated keyword lists at 215-254.
- Dependents: view.py:589-600, 696-713; export.py via the view; test_collector.py (assertion count not counted).
- Risk: low to medium; wide but mechanical.

### T8. The permanently open question gate (about 13 lines)

- Where: commands.py:63-70 (`QUESTION_GATE_PASSED = True`, `QUESTION_GATE_TEXT`), 168-170 (`_questions_on`), 185-186 (the refusal branch).
- Why: the constant is True and cites the owner's pass record, so the False branch cannot run in production. But release-gates.md calls this guard the control; removing it is a decision for the owner, not a cleanup. Listed only so it is on record.
- Risk: governance, not technical. Leave unless the owner says otherwise.

### T9. Duplicate Orca-call error mapping (about 12 lines)

- Where: adapter.py:436-454 (`read_pages`) and 503-511 (`read_questions`) repeat the same chain: `TimeoutError`/`TimeoutExpired` to overrun or timeout, `RunnerFailure` to code, `OSError` to spawn-error, with the same `budget_limited` rule. One private `_call(argv, remaining)` helper returns the reply or a ready `SourceResult`.
- Dependents: test_adapter.py (both entry points). Behaviour must stay identical (safety-adjacent: it decides what the user sees on failure).
- Risk: low.

### T10. Evicted-key list in question retention (about 9 lines)

- Where: questions.py:47-50 (`evicted_keys` field and its own "shortcut" comment) and 129-138. It prevents counting a dropped question twice if a later read returns it. Evicted questions are the oldest by creation time, and a read returns only the newest 100 rows, so the case needs a source whose row order disagrees with `created_at` (UNVERIFIED that it cannot). The displayed total already reads `unknown (retention exceeded)` whenever anything was evicted (questions.py:68, view.py:655), so only the exported integer `evicted` (snapshot.schema.json:77) could be off by a few.
- The recent commit list shows two fix commits touching this bookkeeping (bb1f0431c "bound the evicted-key bookkeeping", 2083db2ae "count an evicted question once"), a sign of effort spent on a case with no visible payoff.
- Keep the 1,000 bound and the `evicted` integer (T46 and the schema require them). Risk: low; tests test_questions.py (18 matches on eviction terms) change.

Total if all ten are done: about 355 lines in the first count, about 300 after overlap (T1 and T7 share view.py code). T2 alone is 85 lines at near-zero risk.

## Open questions this component is connected to

PRD lines 415 to 473 (/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/prd-orca-observer/prd.md). Only the ones this code touches:

- OQ-3 (command name): justified as built; `observe_group` is registered in cli/main.py:572-574. Nothing to trim.
- OQ-5 and OQ-6 (sample capture, display versus export of message content): the code already separates them. parse.py `Question` keeps the subject and drops body, payload and `to_handle`; the exporter's questions group carries "ids, times and counts only (never subject or body)" (export.py:161). No extra machinery needed whichever way the owner answers.
- OQ-7 (coordinator questions only): decided. It justifies the `type == "question"` filter and the `contradictory_rows` count in parse.py:503-513 and the "COORDINATOR QUESTIONS" wording in view.py:53.
- OQ-8 (multi-observer): the code does nothing beyond the HELP disclosure (commands.py:84-85), which matches the spec's "disclosure only" recommendation. It adds no singleton or lock. Good as is.
- OQ-12 (which row order is authoritative): the code keeps both orders, `all_rows` sorted by time and `visible_rows` in source order (view.py:841-847), and render.py draws `visible_rows`. If the owner picks one order, `all_rows` and `_sort_key` (view.py:373-378, about 10 lines) go, unless the exporter needs the time sort (export.py, not checked).
- OQ-13 (`read k of N Runs` placement): the code prints `runs seen: ...` in the COUNTS strip only (view.py:811-816) and nowhere else, which is neither of the two readings exactly. No trim; the owner answer may change a line.
- OQ-14 (width matrix contents): render.py:148-223 hard-codes the three layouts, so the open question is settled in code by whoever wrote it. T5 above is the only simplification, and it is only worth doing after OQ-14 is answered.
- OQ-15 (`stage.detail` and `stage.activity` in the snapshot): the code treats them as inspector-only (view.py:405-406) and gives them the one "block" sanitize mode (parse.py:91-93, sanitize.py:27-48). If the owner decides they are not needed at all, the block mode, `_BLOCK_FIELDS` and two parsed fields (about 12 lines) can go.
- OQ-1, OQ-2, OQ-4, OQ-9, OQ-10, OQ-11: no code in this component depends on them. The gate answer for QUESTION-OBSERVATION is already in the code as a constant (T8).
- OI-6 (tests missing for `selected <id> no longer in source window` and the `collected n / reported T (mismatch)` form): the code paths exist (view.py:859-872 and 521-524) with no pinning test per the PRD. I did not check whether later tests were added (UNVERIFIED).

## Not checked

- export.py (assigned to another reviewer) and the JSON snapshot schema beyond two greps for `evicted`.
- I did not run any test or any command. Every claim of "no production caller" comes from Grep over src/superclaude/cli/observe/*.py and tests/observe/*.py, not from running coverage. Dynamic use (getattr, string lookup) would escape it; I saw none in the files I read.
- The test files were not read, apart from matching lines. Whether a trim would break a golden file (test_golden_contract.py, record_golden.py, record_golden_questions.py) is UNVERIFIED.
- The spec tests (T-numbers) cited are only the ones I found by grep in acceptance-tests.md (T46, T53, T34 by code comment). I did not trace the AD-numbers cited in module docstrings to their definitions.
- The "owner decision, 2026-11-12" cited in view.py:227 and render.py:380 (oldest questions kept, questions win on short terminals): not found in the three owner files. It may be in the release 2 plan under .dev/tasks/; not searched.
- The fixtures directory (JSON data) and snapshot.schema.json were not read.
- Whether the "unknown (retention exceeded)" and `m`/`h`/`/` behaviours match what a real user needs was not tested against a live Orca; no live reads were made.
- Line counts for trims are estimates by reading the line ranges, not by diff.
