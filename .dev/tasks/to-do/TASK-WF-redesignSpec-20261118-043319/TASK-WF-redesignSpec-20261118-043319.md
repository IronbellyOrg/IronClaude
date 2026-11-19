---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-redesignSpec-20261118-043319
version: "1"
priority: Medium
created_date: "2026-11-18"
---

# Observer visual parity: theme, frames and layout (issue 606)

Source: ./source.md
Goal: `superclaude observe` matches the three design mockups (Signal Bridge, Attention Ledger, Decision Desk) at 160, 116 and 80 columns, with each phase closed by a passing render gate, and the record, the JSON snapshot and the observer rules unchanged.

## Constraints

- Numbering: plan Phase N is spec Phase N-1 (plan Phase 1 is the spec's Phase 0, plan Phase 8 is the spec's Phase 7). Task text names the plan phase unless it says "spec Phase".
- Shorthand used in every task: OBS is `src/superclaude/cli/observe/`; T is `tests/observe/`; VP is `.dev/issues/409/visual-parity/`; RR is `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`; "the spec" is `./source.md` (its section numbers, Part B step numbers such as 1.4 and Part C step numbers such as 2.12 are cited in each task).
- Do not edit `OBS/export.py`. `record_text` and `snapshot_json` stay byte-identical. Question text appears on screen only; both hash canaries (record and snapshot) pass from Phase 1 onward.
- NO_COLOR output has zero ESC bytes and the same text as the coloured output after SGR removal. ASCII output is pure ASCII with `+ - |` borders and `#` for the block glyph. The 16-colour theme keeps eight distinct role colours.
- Draw only facts the screen has: no owner, requester, mapped-tree, SIGNALS bars or affected-session list (accepted divergences AD-1 to AD-8 of the spec).
- Existing source guards stay true: `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (`OBS/commands.py` lines 67 and 70) untouched, the words `release-gates.md` and `Task 18` stay in `OBS/commands.py`, no `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in `OBS/render.py`, and `len(group.renderables) == len(screen_lines(...))` holds.
- Owner rulings already applied (spec section 10 and Part C): Decision Desk in two columns at 160 and 116 and stacked at 80; questions screen stacked at every width; the 64-hex hash is never shown on screen; the other defaults of spec section 10 apply (D-2 to D-5, D-7 to D-12). OPEN-1 to OPEN-3 are treated as Medium and gating.
- Phase gate rule (spec section 8): each phase ends with the render gate, at most 3 iterations, a fresh reviewer per width each iteration. A phase closes only when every in-scope High and Medium rubric row passes in the last iteration. If a row still fails after iteration 3, or two consecutive iterations do not improve the passing count, write `./.dev/issues/409/visual-parity/scores/<phase>/stop.md` (path relative to the repository root), stop, and ask the owner. Never start the next phase before the previous gate closes.
- Gate outputs (renders, captures, scores) are written under `./artifacts/gates/<phase>/iter-<n>/` in this package; the closing record `scores.json` of the last iteration is also copied to `.dev/issues/409/visual-parity/scores/<phase>/` because the spec's definition of done reads it there.
- The spec's Phase 0 inputs (`render_current.py` and the baseline captures) exist only untracked in a local checkout that must never be edited. They are not on this branch, so Phase 1 rebuilds `render_current.py` from the observer's own view builders and fixtures. Never edit the local checkout.
- Goldens are regenerated only from the current tree, in the same change set as the change that moves them; styled bytes are never written into a golden.
- Nothing under `.claude/` is staged. This plan does not commit, push or open a PR before a human asks; the final task states the PR route for that moment (`/sc:pr-submit --monitor 3`, target `IronbellyOrg/IronClaude`, never `SuperClaude-Org`).
- Judgment call recorded here: spec step 2.13 names `_field_lines`, a function that step 5.2 only creates in the desk phase (spec Phase 5, plan Phase 6). The space-diet work (spec Phase 2, plan Phase 3) therefore applies the label, alignment and badge changes to the existing desk field loop in `OBS/render.py` (lines 347-353 today), and plan Phase 6 replaces that loop with `_field_lines` while keeping those changes.

## Phase 1: Render-compare harness, rubric, baseline and pinning tests (no src change)

## Task 1: Rebuild the baseline capture script and add the render-compare harness

Spec Part B steps 0.1, 0.2 and 0.3. Create `.dev/issues/409/visual-parity/inputs/tools/render_current.py` (the spec's step 0.1 assumes it exists; it does not on this branch). It builds the ledger, questions, desk and desk-planask views from the observer's own fixtures (`OBS/fixtures/`) and view builders and writes plain captures, wrapped in `if __name__ == "__main__":` so it is importable. Then create `.dev/issues/409/visual-parity/tools/render_compare.py` that loads `render_current.py` by path, exposes `render_case(view, width, height, *, env, ascii, depth="16") -> CaseOutput` (fields `plain`, `stream`, `html`) built on `resolve_policy`, `make_console(policy, file=io.StringIO(), record=True)`, `render` and `console.file.getvalue()` (never `export_text(styles=True)`), and implements the full CLI contract of step 0.3: screens `ledger`, `questions`, `desk`, `desk-planask`; widths 160, 116, 80 at heights 48, 42, 42; five passes (truecolor, 256, 16-colour, NO_COLOR, ASCII); the output file names and `manifest.json` per width; `--depth`, `--heights` and `--check` flags; `--check` writes `checks.json` with the script-checked rows listed in step 0.3 (RB-01(a), RB-04, RB-05 to RB-10, RB-13, RB-14, RB-16, RB-17, RB-19 to RB-22 for the parts marked Script). Before Phase 2 lands `TerminalPolicy.color_system`, the harness produces only the 16-colour depth and marks the other two `not-available-before-P1` in `manifest.json`. The desk-planask view uses the synthetic plan-ask built in Task 3 (import it from the tests helper or duplicate the constant with a comment naming its twin).

Acceptance criteria:
- `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out ./artifacts/gates/p0/iter-1 --check --heights 44,40,24,12,8` exits 0 and writes, for every screen and width, the `.txt`, `.nocolor.txt`, `.ascii.txt`, `.ascii.ansi`, `.16.ansi` and `.16.html` files plus `manifest.json` and `checks.json`.
- The `.nocolor.txt` file contains no ESC byte and the `.ascii.txt` file passes `str.isascii()`, as `checks.json` records.
- The observer package is unchanged: `git diff --stat -- src/` is empty.

## Task 2: Write the fixed rubric, the reviewer prompt and the PNG-route note

Depends on: Task 1

Spec steps 0.4 and 0.5. Create `.dev/issues/409/visual-parity/rubric/rubric.md` containing the spec's section 8.4 table verbatim (RB-01 to RB-23), the Part C rows RB-24 to RB-29 (replacing RB-19 by RB-27 as Part C states), the palette of RB-01 and the geometry table of section 8.3. Create `.dev/issues/409/visual-parity/rubric/reviewer-prompt.md` naming the inputs a fresh reviewer gets (the rubric, the mockup `.png` and text for the width from `.dev/issues/409/attachments/` and the design package zip `.dev/issues/409/orca-observer-design-package.zip`, and the rendered `.png`, `.txt`, `.ansi` and `checks.json`), the pairing (ledger to signal-bridge, questions to attention-ledger, desk to decision-desk), the PASS or FAIL JSON shape with one evidence line per in-scope row, a ban on edits, and a note that the retired mockup title `OPEN HUMAN QUESTIONS` is not scored. Prove the PNG route once: open one `.html` through `mcp__plugin_playwright_playwright__browser_navigate` with a `file://` URL, set `font-family: "DejaVu Sans Mono"` and width `<cols>ch`, take a screenshot with `browser_take_screenshot`, read the PNG back, and record viewport, font and result in `.dev/issues/409/visual-parity/png-route.md`. If it fails, record that the text and ANSI tier is the gate and that no dependency is added.

Acceptance criteria:
- `rubric.md` contains the row ids RB-01 to RB-29 and its wording is frozen from this task on (later tasks never edit it).
- `png-route.md` states PASS or FAIL for the Playwright route with the viewport and font used.
- `reviewer-prompt.md` lists exactly the inputs named above and the JSON shape.

## Task 3: Add the plan-ask hash fixture, pinning tests and height test

Spec steps 0.6 and 0.7. In `tests/observe/test_render.py` (new R3 block after the test ending at line 967) add a `PLAN_ASK` constant (a plan path, two file paths and `"0123456789abcdef" * 4`, under `ASK_CAP = 400` from `OBS/parse.py:475` and under four desk lines at 80 columns) and these tests: the plan-ask wraps cleanly in the desk at every width in `WIDTHS` (every line `cell_len <= width`, the hash whole on one desk line, the ask intact when not cut); a second fixture with the hash after a long path list that fills `DESK_TEXT_LINES = 4` pinning today's `...` cut; a worker with a 120-character `resource.worktreeId` pinning the continuation indent at `OBS/render.py` lines 347-353; and the canary `HASH not in record_text(view)` and `HASH not in snapshot_json(view)`. In `tests/observe/conftest.py` add `strip_sgr(text)` and `sgr_params(text)` with a self-test. Create `tests/observe/test_height_budget.py` with `test_questions_on_screen_fits_the_height(width, height)` for heights 24, 40, 44; if a height fails on today's code, record the failing heights in `.dev/issues/409/visual-parity/scores/baseline.md` and pin only the passing set (a finding for Phase 4, not a fix here).

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green (baseline 766 passed on 2026-11-17, plus the new tests).
- Both hash canaries pass against `OBS/export.py` unchanged.
- `git diff --stat -- src/` is empty.

## Task 4: Score the baseline and close Phase 1

Depends on: Task 1, Task 2, Task 3

Spec step 0.8. Run the harness (Task 1) at the current commit into `./artifacts/gates/p0/iter-1/`, rasterise per `png-route.md`, spawn one fresh reviewer per width with the reviewer prompt, and store the scores in `.dev/issues/409/visual-parity/scores/baseline.json`. Measure the RB-22 threshold N (the longest interior blank run in the 160-column rows of the `base` fixture) and write it to `.dev/issues/409/visual-parity/scores/baseline.md`. Expected: RB-01 to RB-04 and RB-09 to RB-18 FAIL; the plain-text rows RB-05 to RB-08 pass. If the baseline passes any High row, revise `rubric.md` once, then freeze it.

Acceptance criteria:
- `scores/baseline.json` and `scores/baseline.md` exist, the latter holding the measured number N for RB-22.
- No High rubric row passes on the baseline, or the single permitted rubric revision is recorded with the reason.
- `uv run pytest tests/observe/ -v` is green.

## Phase 2: Colour depth, theme, role spans and styled-capture gates (style only)

## Task 5: Resolve the colour system in the policy and add the theme module

Depends on: Task 4

Spec steps 1.1 and 1.2. In `OBS/terminal.py` add `color_system: str | None = "standard"` as the last field of the frozen `TerminalPolicy`; in `resolve_policy` return `None` when NO_COLOR is set or `TERM` is `dumb` or `unknown`, `"truecolor"` for `COLORTERM` `truecolor` or `24bit`, `"256"` when `TERM` ends `256color`, else `"standard"`; in `make_console` (line 121) use `color_system=policy.color_system`, keeping `no_color=policy.no_color`. The `NO_COLOR` literal stays only in `terminal.py`. Create `OBS/theme.py` with `ROLES` (title, attention, attention_title, identity, secondary, body, body_bold, muted, selected, border_attention, border_secondary, border_count, state_running, state_settled, state_failed, state_frozen), `style_for(role, depth)` (None for no depth), one table per depth using the palettes of step 1.2 (truecolor RGB, 256 indexes, 16-colour named ANSI colours), Style objects cached per `(role, depth)`, `STATE_ROLE` and `FROZEN_ROLE = "state_frozen"` as in step 1.4, and none of the literals `Console(`, `NO_COLOR`, `COLUMNS`, `stdout.encoding`, `getpreferredencoding` (comments included). Add depth cases to `tests/observe/test_terminal.py` and create `tests/observe/test_theme.py` per step 1.6(d) and (e).

Acceptance criteria:
- `tests/observe/test_terminal.py` covers NO_COLOR, `TERM=dumb`, COLORTERM truecolor, TERM `xterm-256color` and none, each checking `make_console(...).color_system`; the callers that build policies with an empty env (`tests/observe/test_render.py`, `test_commands.py`, `release1_surface.py`, `conftest.py`, `test_export.py`, `test_question_cap.py`, `test_linkoff_screen_reference.py`, `test_golden_contract.py`) still pass unchanged.
- `tests/observe/test_theme.py` asserts every role exists at every depth, eight distinct palette roles at `"standard"`, four distinct state-role SGR codes at `"standard"`, the five required `STATE_ROLE` keys, `FROZEN_ROLE == "state_frozen"`, and no blink.
- The source scan of `tests/observe/test_terminal.py` (lines 181-198) passes, so no forbidden literal sits in `theme.py`.

## Task 6: Add the Line layer to render.py

Depends on: Task 5

Spec step 1.3. In `OBS/render.py` add frozen `Span(start, end, role)` and `Line(plain, spans)` with `seg`, `join`, `Line.clipped`, an `ascii_safe` path that keeps offsets valid, and `_roled(strings, role)`. Rename the body of `screen_lines` (line 390) to `_compose(view, policy, message=None) -> list[Line]` and define `screen_lines(...) = [l.plain for l in _compose(...)]` with the public signature unchanged. `render` (line 524) builds `Text(l.plain, no_wrap=True, overflow="crop")` per line and stylizes spans through `theme.style_for` only when `policy.color_system` is not None. Wrap every existing builder output as one `body` line so behaviour is unchanged.

Acceptance criteria:
- Every `screen_lines` string result is unchanged: `tests/observe/test_render.py`, `test_linkoff_screen_reference.py`, `test_golden_contract.py`, `test_inspector_scroll.py`, `test_question_cap.py` and `test_export.py` pass with no edit to a golden.
- `len(group.renderables) == len(screen_lines(...))` still holds (`tests/observe/test_render.py:399`) and the source guards at lines 400-404 pass.

## Task 7: Assign roles at the builders

Depends on: Task 6

Spec step 1.4 (no text edits). In `OBS/render.py` give roles at `counts_lines`, `_row_line` (rebuilt as `_row_segments`), `_header_lines`, `_inspector_lines`, `_question_line`, `_desk_lines`, `_panel_lines` and the footer exactly as step 1.4 lists: title, muted header2 and footer, protected counts tokens `identity` and `UNAVAILABLE` suffix muted, question line segments (age `attention` bold, subject `body_bold`, reason tail muted, selected marker and line `selected`), desk title and qid and question text `attention` bold, field labels muted. A cell whose stripped text is the bare `unknown` is muted; `workerState`, `dispatchStatus` (full layout) and the liveness verdict take `STATE_ROLE` by exact `(field, raw value)` equality (the verdict is `row.raw.liveness_verdict`, and in the `full` layout the cell text is `<verdict> (<source>)`); a flags cell containing `FROZEN_MARKER` is `state_frozen`; `nextAction.kind` and `terminalState` stay `body`. Re-read `RowView` construction (`OBS/view.py` lines 481-518) and the `OBS/parse.py` value sets before coding. No regex runs over worker-controlled text.

Acceptance criteria:
- With colour on, the plain text is unchanged: `strip_sgr(coloured print) == NO_COLOR print` at 160, 116 and 80 for the base fixture.
- A selected question has a bold amber role in addition to its glyph; absent values are muted; state words are always printed.
- `uv run pytest tests/observe/ -v` is green with both goldens untouched.

## Task 8: Make the one-shot path style-capable and update the style-sensitive tests

Depends on: Task 7

Spec steps 1.5 and 1.6 parts (a), (b), (c), (f). In `OBS/commands.py` add `_screen_text(view, policy, *, styled)` returning `console.file.getvalue()` when styled and `console.export_text()` otherwise; `run_once` (line 225, the `export_text()` call at line 242) sets `styled = policy.color_system is not None and stdout_is_tty`, taking stdout from the same dependency object `_emit` uses; add `policy.color_system` to the `LiveScreen` shape tuple (line 265). Leave lines 67 and 70 untouched. In `tests/observe/release1_surface.py` make `_printed` return `strip_sgr(buffer.getvalue())` (import `strip_sgr` from `tests.observe.conftest`). In `tests/observe/test_render.py` replace the check at lines 250-259 with `strip_sgr(colour) == nocolor` plus the ESC assertions, and apply `strip_sgr` before `cell_len` or `bad_chars` at every `printed(` call (lines 76, 161, 181, 255-256, 277, 605, 977, 987). Create `tests/observe/test_styled_capture.py` per step 1.6(f).

Acceptance criteria:
- `tests/observe/test_commands.py:121` (no ESC in piped one-shot output) still passes; the gate-constant tests at `tests/observe/test_commands.py:747-772` pass.
- `tests/observe/golden_release1_surface.json` and `golden_questions_linkoff.json` are byte-identical to before (`git diff --stat` shows neither).
- `_screen_text(styled=True)` at 160, 116 and 80 contains SGR and `strip_sgr` of it equals the `export_text()` text; NO_COLOR gives zero ESC; ASCII stays ASCII.

## Task 9: Add the live pty test and close the Phase 2 gate

Depends on: Task 7, Task 8

Spec steps 1.6(g) and 1.7. Read `OBS/commands.py` lines 257-279 (`LiveScreen.__init__`, `draw`, `close`) and `tests/observe/spike_child.py:64`. Create `tests/observe/live_child.py` (builds the fixture view and drives the real `LiveScreen` under `pexpect.spawn` with a fixed pty size) and `tests/observe/test_live_screen_pty.py` asserting the stream contains `\x1b[?1049h`, SGR `38;2` when `COLORTERM=truecolor`, only 16-colour codes otherwise, no SGR under `NO_COLOR=1`, no SGR 5 or 6 and none of `\x1b[?1000h`, `?1002h`, `?1003h`, `?1006h`; if Rich emits a bare reset under NO_COLOR, adjust with the measured bytes and note it. Update the harness to produce real 256 and truecolor passes now that the policy carries `color_system`. Run the render gate (spec section 8) into `./artifacts/gates/p1/` with rubric rows RB-01, RB-05 to RB-11 and RB-23 in scope.

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green including the pty test.
- Gate record `.dev/issues/409/visual-parity/scores/p1/scores.json` shows every in-scope High and Medium row PASS in the last iteration within 3 iterations, or `stop.md` exists and the run has stopped for the owner.
- The 16-colour pass maps the eight roles to eight distinct ANSI colours (RB-09) and the state roles pass the RB-10 census.

## Phase 3: Text and budget defects on the existing layouts, plus the space diet

## Task 10: Split the records golden from the presentation golden

Depends on: Task 9

Spec step 2.1 (first in this phase). Create `tests/observe/golden_release1_records.json` from the current `tests/observe/golden_release1_surface.json`, keeping per variant (`base`, `empty`, `source-loss`, `injection`, `missing-fields`) only `header1`, `header2`, `gap_notice`, `record_text` and `snapshot_json`, written with `json.dumps(..., indent=1, sort_keys=True, ensure_ascii=False)` and no trailing newline. Add `test_release1_records_are_byte_identical_to_the_recorded_surface` to `tests/observe/test_render.py` comparing those keys from `surface()` in `tests/observe/release1_surface.py`. This file is never regenerated afterwards.

Acceptance criteria:
- The new test passes and `git diff --stat -- src/` is empty.
- `golden_release1_records.json` holds no `lines_*` or `printed_*` key.

## Task 11: Heading at every width, whole key groups, footer rule, counts never cut

Depends on: Task 10

Spec steps 2.2, 2.3 and 2.4 in `OBS/render.py`. Add `_heading_rows(view, policy)` (2 when `view.visible_rows`, else 0) and use it at the `ledger_fixed` term (line 439) and the heading gate (line 497) in place of the `width_class == "full"` tests, without adding heading rows to `reserved`; add `wrap_groups(text, width, policy)` next to `wrap` and use it in `_help_lines` (line 304) in both branches, removing the `clip(...)` branch for `view.questions is None`; add one `glyph("hrule") * width` row before the footer and count it in `footer_height` (lines 423-431) and the footer branch (lines 514-521); remove the branch of `counts_lines` (lines 127-129) that clips an unprotected token, so a token that does not fit is dropped whole and the line ends with the existing ` >` marker, protected tokens keeping their wrap path.

Acceptance criteria:
- A column heading and rule appear at 116 and 80 whenever rows are visible and are absent when there are none.
- No key line at 80 columns ends in `>`; the pair `n/p question` is never split across lines; no counts line ends inside a token; the footer rule precedes the footer.
- `tests/observe/test_inspector_scroll.py` still passes (the inspector returns earlier).

## Task 12: Title bar badge and the optional blank-band fix

Depends on: Task 11

Spec steps 2.5 and 2.6. Add `READ_ONLY_BADGE = "READ ONLY"` to `OBS/view.py` and `_title_bar(lines, policy)` to `OBS/render.py`, placing the badge right-aligned on the first wrapped header line if it fits, else the last, else on its own line, in the `attention` role; `view.header1` is not edited. Apply step 2.6 (the `line` and `short` id rule of `_columns`, lines 195-196 and 215) only if RB-22 against the baseline number N fails; otherwise log the skip in the Task 16 commit notes.

Acceptance criteria:
- `READ ONLY` appears exactly once on the screen and every line fits the width at 160, 116 and 80; `header1` in `tests/observe/golden_release1_records.json` is unchanged.
- The RB-22 outcome (fixed or skipped with its measured numbers) is written into `.dev/issues/409/visual-parity/scores/p2/notes.md`.

## Task 13: Reasons once and no hash on screen (view side)

Depends on: Task 12

Spec Part C steps 2.11 and 2.12. In `OBS/view.py` add `strip_hex(text) -> str` (remove every run of 32 or more `[0-9a-fA-F]` characters and collapse the double space left behind) applied only where the display strings `shown` and `DeskView.ask` are built, never to `ask`, `text` or anything `record_text` or `snapshot_json` read. Add the title note `reasons: none in source` and print the row suffix `reason unknown` only when the source gave a reason (decision D-13); the unknown-versus-none rule holds because the note is about the source. Rewrite the Q7 tests from Task 3 to assert the hash is absent from every screen line at 160, 116 and 80, the rest of the ask is intact, the screen fits, both canaries still pass, and the trailing-hash fixture keeps its four-line cut with `...`. Rewrite the `^\s*\d+[smh]  ` row checks and the `reason unknown` counting checks (`tests/observe/test_render.py` lines 453 and 930-948) to the new form.

Acceptance criteria:
- No run of 32 or more hex characters appears on the questions screen or the Decision Desk at any width; both hash canaries pass; the inspector keeps the full question text (default of Part C).
- A question row shows no `reason unknown` suffix when no reason is given, the title carries `reasons: none in source`, and a row with a reason shows it.
- `git diff --stat -- src/superclaude/cli/observe/export.py` is empty.

## Task 14: Show each fact once, questions first, aligned labels and one status badge (desk and list)

Depends on: Task 13

Spec Part C steps 2.9, 2.10 and 2.13 in `OBS/render.py` and `OBS/view.py`. Apply 2.9 (a) to (e): the full question text only in the desk pane and the selected list row cut to one line with `>`; the Run id once (the freshness header cell for questions becomes `questions OK 0s`, the panel keeps its first state line); the count once (figure, `seen, not resolved` and `closed by evidence: unavailable` in one place, the separate counts row and tile echo removed, `(no source)` dropped from that phrase on screen only; `record_text` still writes `counts_line` unchanged); the `msg_` id leaves the desk pane (kept in the inspector); the second copy of the retention and `worker-reported, not questions` lines under the desk dropped. Apply 2.10: question rows first, then the disclosure verbatim (never shortened), with `no read marker in source: answered questions stay listed` and the retention sentence verbatim and adjacent. Apply 2.13 to the existing desk field loop: label column of about 9 cells, plain labels `session`, `state`, `alive`, `next`, `status`, `worktree`, one `alive` value built from verdict, source and evidence age, `worktree` reading `wt-1  (this session only)` (full note to the inspector), absent values `unknown` and muted; one `ACTIVE` badge only when dispatchStatus is `active`, terminalState is `active` and outcome is `none`, any other combination (an absent value included) expanding to three separate rows with raw values (decision D-14).

Acceptance criteria:
- For the `desk` and `questions` fixtures at each width, the question text, the Run id, the count words and a source's freshness state each occur once on the screen (header and panel state line excepted as RR line 45 requires), checked by a string-census test.
- The ACTIVE badge test covers active/active/none, a changed outcome, and an absent value (`unknown`, expanded to three rows).
- `record_text` and `snapshot_json` are unchanged (`tests/observe/golden_release1_records.json` test passes).

## Task 15: Ledger diet

Depends on: Task 14

Spec Part C step 2.14 in `OBS/render.py` (`_columns`, `_row_segments`, footer) and `OBS/view.py`. Merge dispatchStatus, terminalState and outcome into one `status` cell with the Task 14 badge rule; replace the `alive (terminal)` text column with a dot `●` coloured by state plus one legend line, spelling out any non-alive value in amber and in words under NO_COLOR (decision D-15); drop the `flags` column and show the changed marker `*` in the first cell; drop the separator rule row and the `+N more` row above a footer that already says `shown n/N`; put the gap notice and `26 historical hidden (h)` on one row; drop `mode=` and `as of` from the header, the second `scope=all`, and `collected` from the footer; replace the three `unavailable (no source)` tokens with one dim token `no source: settled, frozen, cost`; footer keys become `j/k move  Enter detail  / filter  n/p question  h history  e export  q quit` (dropped keys still work); `source counts` (when unknown) and `runs seen` leave the screen for the inspector (D-16). Keep verbatim: `collected n / reported T` and PARTIAL, `seen, not resolved`, `closed by evidence: unavailable`, `worker-reported, not questions`, the Human questions gap notice.

Acceptance criteria:
- No `flags` column, no rule row and no `+N more` row above a `shown n/N` footer at 160, 116 and 80; a non-alive liveness value is spelled out also under NO_COLOR.
- The FROZEN marker role of Task 7 still reaches the screen through the first cell or status cell (`tests/observe/test_render.py` frozen-row checks pass or are rewritten with evidence).
- `uv run pytest tests/observe/` shows only the position-sensitive tests listed in Task 16 failing before that task and none after it.

## Task 16: Re-baseline both presentation goldens, rewrite position-sensitive tests, close the Phase 3 gate

Depends on: Task 15

Spec steps 2.7, 2.8 and 2.15. Regenerate `tests/observe/golden_questions_linkoff.json` with the capture command of step 2.7 and `tests/observe/golden_release1_surface.json` with `surface()` from `tests/observe/release1_surface.py` (indent 1, sort_keys, ensure_ascii False, no trailing newline), from the current tree, in one change set. Add `test_presentation_goldens_hold_no_escape_bytes`; retitle the docstring of `test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface` (`tests/observe/test_render.py:611`). Re-run and adjust, with evidence, the row-count and position tests: `test_matrix_lines_fit...` (line 83), `test_decision_2...` (line 660), `test_line_and_short_forms_follow_kind_id_verdict_age` (lines 314-326, restricted to row lines), `test_f08` (line 748), `tests/observe/test_inspector_scroll.py`. Add the tests listed at the end of step 2.7. Run the render gate into `./artifacts/gates/p2/` with RB-12, RB-13, RB-15, RB-20 to RB-22 and RB-24 to RB-29 in scope plus all earlier rows as regression; if the phase is too large, split the gate into 2a (Tasks 10 to 12) and 2b (Tasks 13 to 15) as the spec allows and record that choice.

Acceptance criteria:
- Both goldens regenerated; neither contains `\x1b`; `tests/observe/golden_release1_records.json` untouched and its test green.
- `uv run pytest tests/observe/ -v` is green.
- Gate record `.dev/issues/409/visual-parity/scores/p2/scores.json` (or the 2a and 2b records) shows all in-scope High and Medium rows PASS, including RB-26 (status badge) and RB-27 (no hash), or `stop.md` exists.

## Phase 4: Frame primitive and single-column titled panes (questions-on screens)

## Task 17: Box glyphs, the frame helper, inner-width threading and budget

Depends on: Task 16

Spec steps 3.1 to 3.4. In `OBS/terminal.py` add to `GLYPHS` (line 30) the rounded `box_tl box_tr box_bl box_br box_h box_v` and heavy `hbox_*` entries with ASCII forms `+`, `-`, `|`; never write a box character as a literal (`ascii_safe` would turn it into `?`). In `OBS/render.py` add `MARGIN = 1`, `FRAME_ROWS = 2`, `INNER_PAD = 1`, `Line.padded`, and `_frame(title, body, width, policy, *, weight="round")` returning lines exactly `width` cells wide with the title clipped to `inner - 2`. Thread the inner width (`pane = policy.width - 2*MARGIN`, `inner = pane - 4`) through `_question_line`, `_desk_lines` and `_panel_lines`; the list pane is heavy when no desk is shown and round when a desk is shown, the desk pane heavy. `base` and `len(desk)` in the sizing block (lines 433-481) are measured from returned lists so frame rows are counted without a new term; read the comment at render.py lines 444-445 before touching the three `+1` terms, which stay. Where the desk does not fit and `DESK_HIDDEN` applies, the notice sits inside the list frame body.

Acceptance criteria:
- At every width the ASCII pass of the questions-on screen shows `+---+` borders and `|`, never `?`.
- Every frame line is exactly its pane width in cells and every added row is counted so no screen exceeds `policy.height` at heights 12, 24, 40 and 44.
- `tests/observe/test_terminal.py` covers the new glyph pairs, and questions-off screens and the inspector are byte-identical (`golden_release1_surface.json` unchanged by this task).

## Task 18: Frame-aware tests, Q7 re-pin, height and pty checks, golden, close the Phase 4 gate

Depends on: Task 17

Spec steps 3.5 to 3.10. Add `unframe(line)` and `title_of(lines)` to `tests/observe/conftest.py`. Convert the whole-line checks to frame-aware ones as step 3.6 lists (`DESK_TITLE in title_of(lines)` at `tests/observe/test_render.py` lines 900, 924, 997; `unframe` at 897, 964 and the desk slice 951-966, 938, 948, 479, 646, 547; `tests/observe/test_question_cap.py` lines 77 and 121; `tests/observe/test_commands.py` lines 672-675 and 690, per decision D-9 default yes), re-pin `test_decision_2` (line 660) from the measured value and record in the commit notes that "the questions win on a short terminal" still holds, and keep `test_r3_the_desk_gives_way...` (line 990) passing. Re-pin the Q7 tests through `unframe` with the single-column inner widths (154, 110, 74). Extend `tests/observe/test_height_budget.py` to framed screens at heights 8 (diagnostic), 12, 24, 40, 44 and, in `tests/observe/test_live_screen_pty.py`, assert at heights 24 and 40 that the last stream row holds the `shown x/y` footer. Regenerate `tests/observe/golden_questions_linkoff.json`. Run the gate into `./artifacts/gates/p3/` with RB-02 (questions, desk), RB-07 and earlier rows in scope.

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green; `golden_release1_surface.json` and `golden_release1_records.json` are untouched.
- Gate record `.dev/issues/409/visual-parity/scores/p3/scores.json` shows all in-scope High and Medium rows PASS with the NO_COLOR and ASCII passes present (ASCII pass: `+ - |` borders, no `?`), or `stop.md` exists.

## Phase 5: Count strip and RETAIN CONTEXT pane on the stacked questions screen

## Task 19: Add the render-only figure field, the block glyph and the 3-row font

Depends on: Task 18

Spec steps 4.1 and 4.2. In `OBS/view.py` add `count_figure: str = ""` to the panel view (dataclass near lines 246-266, set where `counts_line` is built near line 761, reading lines 746-766 first) holding the exact figure text already used inside `counts_line`; leave `counts_line`, `run_line`, `caveat_line` and `retention_line` unedited. Add a `T/test_view.py` check for the default and a source-scan test next to `tests/observe/test_export.py:238-243` that `count_figure` does not appear in `OBS/export.py`. In `OBS/terminal.py` add glyph `block` (`█`, ASCII `#`); in `OBS/render.py` add `_BIG`, a 3x3-cell font for `0` to `9` and `+` built only from `block` and spaces; a figure containing any other character (for example `unknown`) is not drawn in the font.

Acceptance criteria:
- `count_figure` is not read by `OBS/export.py` (source-scan test) and `record_text` and `snapshot_json` are unchanged.
- Every digit and `+` renders in 3 rows and the digits are pairwise distinguishable (a test compares the glyph grids).

## Task 20: Build the count strip, the RETAIN CONTEXT pane and the stacked composition

Depends on: Task 19

Spec steps 4.3 to 4.5 in `OBS/render.py` and `OBS/view.py`. Add `RETAIN_TITLE = "RETAIN CONTEXT"` to `OBS/view.py`. Add `_count_strip(panel, width, policy)`: a `border_count` (cyan) frame titled `QUESTIONS_COUNT_LABEL.upper()`, a 3-row body (figure in the font in `attention`, `panel.counts_line` in `identity` on the middle row two cells right of it) when the figure is drawable and `figure_width + 2 + cell_len(panel.counts_line) <= inner`, else a one-row body (bold figure, two spaces, wrapped `counts_line`). Add `_retain_pane(panel, width, policy)`: a round slate frame holding `run_line`, `caveat_line`, `retention_line` in `muted`. At `full` and `line` the questions panel is strip, list frame, RETAIN pane in that order; the three lines leave the list body while the pane is drawn. Height rule (`MIN_QUESTION_ROWS = 3`): when fewer rows fit, drop the RETAIN pane first, then the strip, relocating `run_line`, `caveat_line`, `retention_line` (and `counts_line` for the strip) into the list body in the Phase 4 order, recomputing `base` and `capacity` once (not a loop); measure and record the real trigger heights at 160 and 116. At 80 columns the screen stays as Phase 4 left it.

Acceptance criteria:
- At 160 and 116 the plain pass contains `seen, not resolved: N | closed by evidence: unavailable (no source)` whole on one line with N equal to the figure and, at 80, no strip frame exists.
- At heights 24 and 26 (and the measured trigger heights) at 116 and 160 columns the screen still contains the run line, the caveat and the retention sentence exactly once whether the pane is drawn or dropped, every line at most the width, at most the height.
- The question line format `<age>  <subject>  ...` and `OBS/export.py` are unchanged.

## Task 21: Phase 5 tests, golden and gate

Depends on: Task 20

Spec steps 4.6 to 4.8. Update `tests/observe/test_render.py` phrase checks to read unframed text with `in` (`test_t19...` lines 437-453, `test_decision_3_and_4` 679-700, `test_f17_f15` 786-805) and row checks through a new `pane_body(lines, title, policy)` in `tests/observe/conftest.py`; add the tests of step 4.6 (strip, list, retain order; each pane `width - 2` wide; relocation at the trigger heights; degrade order RETAIN first then strip; `#` font in ASCII mode with no `?`). Regenerate `tests/observe/golden_questions_linkoff.json`. Run the gate into `./artifacts/gates/p4/` with RB-03 (questions order), RB-04, RB-16 and RB-17 in scope plus all earlier rows; the reviewer also checks the strip, pane titles and order against the stacked option in the layout comparison on issue 606 and that no owner, requester or mapped-tree content appears.

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green; both release-1 goldens untouched.
- Gate record `.dev/issues/409/visual-parity/scores/p4/scores.json` shows all in-scope High and Medium rows PASS (RB-04 (a) cyan border role and (c) text form, RB-16, RB-17) or `stop.md` exists.

## Phase 6: Decision Desk as question pane plus evidence pane

## Task 22: Add the two-column composer, the evidence title and aligned field lines

Depends on: Task 21

Spec steps 5.0 to 5.2. In `OBS/render.py` add `_two_columns(left, right, wl, wr, gap=2)` (rows from `zip_longest`, right-side span offsets shifted by the character length of the padded left side plus the gap, never cell widths) and `_field_lines(label, value, inner, label_width, policy)` replacing the desk field loop (lines 347-353 today) while keeping the Part C labels, aligned column and ACTIVE badge of Task 14; `label_width` is the longest label plus its colon across `desk.session_fields` (`OBS/view.py` lines 843-853); `workerState`, `dispatchStatus` and the liveness verdict take `STATE_ROLE`, `nextAction.kind` stays `body`. Add `DESK_EVIDENCE_TITLE = "LINKED SESSION"` to `OBS/view.py` (D-8). Add `split_columns` and `panes_flat` to `tests/observe/conftest.py` (`pane_body` already exists from Task 21).

Acceptance criteria:
- Every one-line field starts its value at the same cell offset; a value that does not fit beside its label sits on the next line indented two cells; no line exceeds the width.
- Right-column span offsets are correct: a test shows a styled evidence line in a two-column row keeps its role on the right-hand text only.

## Task 23: Build the desk panes and compose the two-column desk with its budget

Depends on: Task 22

Spec steps 5.3 and 5.4 in `OBS/render.py` (`_desk_lines` line 329, `_panel_lines` line 359, sizing lines 458-479). Add `_desk_question_pane(desk, width, policy)` (heavy frame titled `DESK_TITLE`, first body line `qid  age <age>` with age `attention` bold, then `wrap(desk.ask, inner)` limited to `DESK_TEXT_LINES` with the last line cut by `...`, in `attention` bold) and `_desk_evidence_pane(desk, width, policy)` (round slate frame titled `DESK_EVIDENCE_TITLE`, field lines, then `desk.notes` muted). Compose: at `full` left = question pane over the list frame (76 wide) and right = evidence pane (80 wide); at `line` the question pane full width then `_two_columns(evidence, list, 66, 46)`; at `short` three stacked 78-wide frames. When rows are fewer than the question pane plus one list row, or fewer than the evidence pane, use the existing `DESK_HIDDEN` path (`OBS/view.py:97`) so a half-drawn desk never reaches the screen. The panes read only `DeskView`, never record fields.

Acceptance criteria:
- At 160 the desk is two columns of 76 and 80 cells with 1+76+2+80+1 = 160; at 116 the question pane spans the width over panes of 66 and 46; at 80 three stacked panes of 78.
- The Decision Desk screen is never taller than `policy.height` at 8, 12, 24, 40 and 44, and the desk gives way through `DESK_HIDDEN` rather than drawing partially.
- `record_text` still writes `q.text` (never `q.shown` or `q.ask`) and the questions-off and link-off screens are unchanged.

## Task 24: Rework the desk tests and close the Phase 6 gate

Depends on: Task 23

Spec steps 5.5 to 5.7. Rework the R3 tests in `tests/observe/test_render.py` on `pane_body`, `title_of` and `panes_flat` (lines 891, 919, 930, 943, 958, 970, 985, 990, 1009, 1017) and add the new tests of step 5.5 adjusted to Part C (no hash on screen): the plan-ask question's long path in the 46-cell list pane at 116 is hard-split with nothing lost; aligned label column; a value too wide for its label moves to an indented line and a value wider than the inner width is hard-split with nothing lost; a 64-character `resource.worktreeId` at 116 (evidence inner 62) is hard-split with nothing lost; the ask text bounded to four lines with `...`. No golden changes. Run the gate into `./artifacts/gates/p5/` with screens `desk` and `desk-planask` and RB-03 (desk), RB-10 (desk fields), RB-14, RB-27 plus earlier rows in scope.

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green; no golden file changed (`git diff --stat -- tests/observe/*.json` empty).
- Gate record `.dev/issues/409/visual-parity/scores/p5/scores.json` shows all in-scope High and Medium rows PASS or `stop.md` exists.

## Phase 7: Ledger screen panes (questions off)

## Task 25: Measure the flags column and parametrise the ledger columns

Depends on: Task 24

Spec steps 6.1 and 6.2. Part C removed the `flags` column in Task 15, so first re-measure what spec step 6.1 asks on the table as it now exists: the longest content of the first-cell marker and status cell over the fixtures (`base`, `empty`, `source-loss`, `injection`, `missing-fields`, `long-identifiers`) and the FROZEN case, and whether a border-only frame (inner width `width - 2`, no padding or margin) fits the 160-column table; if it does not, keep the 160-column table unframed under a titled rule and frame it only at 116 and 80. Then change `_columns` (`OBS/render.py` line 155) to `_columns(policy, avail)` using `avail` in every width sum, with callers passing the pane inner width, and make rows and heading clip to `avail`. Record the measurement and the decision in `.dev/issues/409/visual-parity/scores/p6/notes.md`.

Acceptance criteria:
- `notes.md` holds the measured numbers and the chosen 160-column frame form.
- The three layouts keep their column sets (AD-3, AD-6) and `uv run pytest tests/observe/ -v` is green with no golden change.

## Task 26: Compose the ledger head panes and the small-height fallback

Depends on: Task 25

Spec steps 6.3 and 6.4 in `OBS/render.py` (head lines 409-414, gap part 482-485, `_notes` 290-301, `_compose`). Order: title bar, attention pane (heavy amber, title `QUESTIONS_TITLE`, body `view.gap_notice` or `panel.summary` when questions are on and nothing is read yet), observation pane (round slate, title `OBSERVATION WINDOW`, body `header2`, the counts lines called with the inner width, `changes_line`), then the ledger pane (round slate, title `view.ledger_title`, heading and rule, rows, overflow line). The `/filter` input line, the one-off message and the footer stay outside the frames. If the framed screen would leave fewer than three ledger rows at `policy.height`, use the Phase 3 plain head instead (heights 12 and 8 stay plain so the `lines_*x12` keys keep their plain form); choose the threshold from measured row counts at 12, 24 and 40 and record it; the forced single ledger row (line 502) stays the last resort. No invented owner, requester, mapped-tree or SIGNALS content.

Acceptance criteria:
- At heights 24, 40 and 44 the framed ledger screen has at most `policy.height` rows; at 12 and 8 it falls back to the plain head.
- Every pane body is built from `view.gap_notice`, `header2`, the counts, `changes_line` or the ledger rows only, checked by a source-scan test.

## Task 27: Ledger tests, release-1 golden and the Phase 7 gate

Depends on: Task 26

Spec steps 6.5 to 6.7. Make the whole-line checks frame-aware (`GAP_NOTICE in [unframe(l) for l in lines]` at `tests/observe/test_render.py` lines 242, 490, 494, 509 and `tests/observe/test_commands.py:121`; the `no successful worker-list read yet` and `no observed items` lines at 352-356; the `shown` row regex at 94 and 337; the row `startswith` checks 373-375; the header and row checks 287-326; `tests/observe/test_golden_contract.py` lines 43-58, `tests/observe/test_question_cap.py`), adapting to the Part C footer wording from Task 15. Add the height and fallback tests and the no-invented-content scan. Regenerate `tests/observe/golden_release1_surface.json` (`lines_{160,116,80}x40` and the `printed_*` keys change; `lines_*x12` unchanged); the records and link-off goldens stay untouched and no golden holds an escape byte. Run the gate into `./artifacts/gates/p6/` with RB-02 (ledger), RB-18 and all earlier rows in scope.

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green; `golden_release1_records.json` and `golden_questions_linkoff.json` are byte-identical to before this task.
- Gate record `.dev/issues/409/visual-parity/scores/p6/scores.json` shows all in-scope High and Medium rows PASS, with RB-18 free of invented content, or `stop.md` exists.

## Phase 8: Spec reconciliation, final gate matrix and PR

## Task 28: Reconcile the rendering rules and the capture script docstring

Depends on: Task 27

Spec steps 7.1 and 7.2 and Part C section C.4. Edit `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` lines 17, 20, 22, 23, 25, 30, 33, 41, 44, 45, 47, 48, 50, 53, 57, 61, 65, 70, 71, 76, 81 and 82 so they match the built screens: title bar and badge and no `mode=` or `as of` (17), the single `no source: settled, frozen, cost` token (20, 81, 82), footer wording (22), gap notice and historical-hidden on one row (23), box glyph ASCII forms (25), one status cell and badge (30, 71), `flags` column removed and the `*` marker (33, 65), RETAIN CONTEXT built (41), merged and reordered counts, run and caveat lines with wording kept (44, 45, 47, 48, 53), reasons once (50), the Decision Desk in two columns with the fields moved to the inspector (57; RR line 43 stays stacked), muting implemented (70), no `+N more` row (76), RR line 61 reworded against RR line 42 and AD-7 (D-11). Record the pane titles `OBSERVATION WINDOW`, `RETAIN CONTEXT` and the D-8 title. Keep verbatim: the disclosure (RR 49), `no read marker in source: answered questions stay listed`, the retention sentence, `worker-reported, not questions`, `collected n / reported T`, PARTIAL, `seen, not resolved`, `closed by evidence: unavailable`. Update the docstring of `.dev/issues/409/visual-parity/inputs/tools/render_current.py` (it must no longer say ANSI captures are empty of escapes), keep the baseline captures as the pre-fix baseline, and write post-fix harness output only under the gate output directory.

Acceptance criteria:
- Each edited rule line matches the behaviour pinned by a test in `tests/observe/` (name the test next to each edit in the commit notes) and RR line 43 still says stacked.
- No path under `src/superclaude/` appears in any file this task edits except as a maintainer note.

## Task 29: Run the final gate matrix, the optional Zellij check and the full checks

Depends on: Task 28

Spec steps 7.3 to 7.5. Run `render_compare.py --check --heights 44,40,24,12,8` exactly as defined in Task 1 into `./artifacts/gates/final/`: widths 160, 116, 80 at heights 48, 42, 42, the five passes, plus a pty run at each width through `tests/observe/test_live_screen_pty.py`, and one fresh reviewer per width scoring every rubric row. Write the closing record to `.dev/issues/409/visual-parity/scores/final/scores.json`. Write `.dev/issues/409/visual-parity/zellij-note.md`: run `zellij action dump-screen --help` on the installed 0.44.2 first, then the observer in a pane and `zellij action dump-screen --ansi`, recording colour, box and wide-glyph fidelity; or record that the owner declined. Zellij is never a dependency and the observer may read `ZELLIJ` only as a hint. Run `uv run pytest tests/observe/ -v`, `make test` and `make lint`.

Acceptance criteria:
- Every High and Medium rubric row passes in the final record; Low rows pass or each is logged as deferred with a reason.
- `uv run pytest tests/observe/ -v`, `make test` and `make lint` all pass, `tests/observe/test_commands.py:747-772` (gate constants intact) pass, and `git diff --stat -- src/superclaude/cli/observe/export.py` is empty.
- `git status` shows no staged `.claude/` path; `.dev/tasks` is staged with `git add .dev/tasks` (staging only, no commit); `.dev/issues/409/visual-parity/zellij-note.md` exists.

## Task 30: Open the PR (only when a human asks for it)

Depends on: Task 29

Spec step 7.6. This task is not run during plan execution unless a person requests the PR in the same session. When requested: confirm `git remote get-url origin` and `gh repo view IronbellyOrg/IronClaude --json nameWithOwner -q .nameWithOwner` both name `IronbellyOrg/IronClaude`; `git fetch origin` and rebase the branch onto `origin/master`; then run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` with the decision record of spec section 10 (D-1 to D-12 and OPEN-1 to OPEN-3 with the owner's answers) in the PR body, and check the returned URL starts `https://github.com/IronbellyOrg/IronClaude/pull/`. Never run a bare `gh pr create` and never target `SuperClaude-Org`.

Acceptance criteria:
- The returned PR URL starts `https://github.com/IronbellyOrg/IronClaude/pull/`; if it points at `SuperClaude-Org`, stop, report it, and take no action on that PR.
- The branch was rebased on `origin/master` before the push, and the PR body carries the decision record.
