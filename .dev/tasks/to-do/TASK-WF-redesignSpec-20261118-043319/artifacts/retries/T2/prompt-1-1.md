44d6d4a7628251c9af1c2a7a991e22859276b9d6
Review one task for spec compliance.

Task brief: ## Task 2: Write the fixed rubric, the reviewer prompt and the PNG-route note

Depends on: Task 1

Spec steps 0.4 and 0.5. Create `.dev/issues/409/visual-parity/rubric/rubric.md` containing the spec's section 8.4 table verbatim (RB-01 to RB-23), the Part C rows RB-24 to RB-29 (replacing RB-19 by RB-27 as Part C states), the palette of RB-01 and the geometry table of section 8.3. Create `.dev/issues/409/visual-parity/rubric/reviewer-prompt.md` naming the inputs a fresh reviewer gets (the rubric, the mockup `.png` and text for the width from `.dev/issues/409/attachments/` and the design package zip `.dev/issues/409/orca-observer-design-package.zip`, and the rendered `.png`, `.txt`, `.ansi` and `checks.json`), the pairing (ledger to signal-bridge, questions to attention-ledger, desk to decision-desk), the PASS or FAIL JSON shape with one evidence line per in-scope row, a ban on edits, and a note that the retired mockup title `OPEN HUMAN QUESTIONS` is not scored. Prove the PNG route once: open one `.html` through `mcp__plugin_playwright_playwright__browser_navigate` with a `file://` URL, set `font-family: "DejaVu Sans Mono"` and width `<cols>ch`, take a screenshot with `browser_take_screenshot`, read the PNG back, and record viewport, font and result in `.dev/issues/409/visual-parity/png-route.md`. If it fails, record that the text and ANSI tier is the gate and that no dependency is added.

Acceptance criteria:
- `rubric.md` contains the row ids RB-01 to RB-29 and its wording is frozen from this task on (later tasks never edit it).
- `png-route.md` states PASS or FAIL for the Playwright route with the viewport and font used.
- `reviewer-prompt.md` lists exactly the inputs named above and the JSON shape.
Global constraints: - Numbering: plan Phase N is spec Phase N-1 (plan Phase 1 is the spec's Phase 0, plan Phase 8 is the spec's Phase 7). Task text names the plan phase unless it says "spec Phase".
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
Start sha: 44d6d4a7628251c9af1c2a7a991e22859276b9d6
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b: Grep floor; the task adds four new documents and changes no symbol; no dependents.

Touched files (new, untracked, full-file diffs below): .dev/issues/409/visual-parity/rubric/rubric.md, .dev/issues/409/visual-parity/rubric/reviewer-prompt.md, .dev/issues/409/visual-parity/png-route.md. The spec the rubric must copy is /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/source.md (section 8.3 lines 288-296, section 8.4 lines 302-328, Part C section C.3 lines 217-226) and the plan is /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/TASK-WF-redesignSpec-20261118-043319.md. Mockup files: .dev/issues/409/attachments/ and .dev/issues/409/orca-observer-design-package.zip.

diff --git a/.dev/issues/409/visual-parity/rubric/rubric.md b/.dev/issues/409/visual-parity/rubric/rubric.md
new file mode 100644
index 000000000..091ef29df
--- /dev/null
+++ b/.dev/issues/409/visual-parity/rubric/rubric.md
@@ -0,0 +1,60 @@
+# Fixed rubric for every render gate (observer visual parity, issue 606)
+
+Written once in plan Phase 1. The wording is frozen: no later task edits it. Source: spec section 8.4 (RB-01 to RB-23), Part C section C.3 (RB-24 to RB-29; RB-27 replaces RB-19), section 8.3 (geometry) and the palette of 04 section 2 as quoted in RB-01.
+
+## Palette (RGB, from RB-01)
+
+base 225,233,238; muted 165,182,194; slate 82,108,128; amber 250,178,25; cyan 112,205,226; green 139,215,175; red 240,141,150; violet 194,173,242.
+
+## Geometry and height budgets (spec section 8.3)
+
+| Screen | 160 | 116 | 80 |
+|---|---|---|---|
+| Questions screen | stacked at every width (owner ruling D-1, AD-8): panes `width - 2` wide with margin 1; at 160 and 116 three panes (count strip, list, RETAIN CONTEXT) | same | one column, panes 78 wide, no strip and no RETAIN pane |
+| Decision Desk | left 76 (question over list), right 80 (session evidence) (1+76+2+80+1=160) | question 114 full width over 66 + 46 (1+66+2+46+1=116) | three stacked panes 78 wide |
+| Ledger | table keeps all 160 cells today (render.py:159-192); a border-only frame needs `flags` to give 2 cells | `line` layout, frame 114 | `short` layout, frame 78 |
+| Inner width of a framed pane | pane width minus 4 (border plus one cell padding each side) | same | same |
+| Frame row cost | 2 rows per frame (top and bottom border) | 2 | 2 |
+| Harness height for scoring | 48 (mockup frame height) | 42 | 42 |
+| Extra height matrix (text only) | 44, 40, 24, 12, 8 | same | same |
+
+## Rows RB-01 to RB-23 (spec section 8.4, verbatim)
+
+| ID | Criterion | Severity | Findings | Checked by | In scope from |
+|---|---|---|---|---|---|
+| RB-01 | Colour roles, measured on the truecolour `.ansi` by mapping each SGR foreground RGB to a role (palette: base 225,233,238; muted 165,182,194; slate 82,108,128; amber 250,178,25; cyan 112,205,226; green 139,215,175; red 240,141,150; violet 194,173,242; 04 section 2). Pass only if all hold: (a) every foreground colour in the file is one of the eight triples; (b) the `header1` title text is cyan and bold; (c) every question age (in the list and in the desk) is amber and bold, and every question-text line in the desk is amber and bold; in the list the question subject text is base colour and bold (`body_bold`, step 1.4, RB-16(a); 04 line 57: amber question text in the desks, base bold in the 160 ledger), never amber; the one selected list row is scored under the `selected` role (marker and line bold amber, step 1.4; an unverified design choice, no mockup shows a selected row) and is exempt from the base-colour subject rule but not from the amber-age rule; (d) the `header2` freshness line, the keys hint and the footer text are muted; (e) every secondary-pane border glyph and the footer rule is slate (not applicable before P3, when no border exists); (f) ledger cells that carry no state or absent value are base. One counter-example, quoted with its line number, fails the row | High | M-01 | Script (`checks.json` role census for (a)) plus Reviewer for (b) to (f) | P1 |
+| RB-02 | Every pane the mockup frames has a titled border with the title inset in the top border: heavy amber for the attention pane, rounded slate for secondary panes, cyan for the count strip | High | M-02 | Reviewer | P3 (questions, desk), P6 (ledger) |
+| RB-03 | Layout structure matches 8.3: the Decision Desk is two columns at 160 and 116 and stacked at 80; the questions screen is stacked at every width (strip, list, RETAIN CONTEXT in that order at 160 and 116; list only at 80) | High | M-04 (desk); M-03 is closed by AD-8 | Reviewer | P4 (questions order), P5 (desk) |
+| RB-04 | Count strip, at 160 and 116 only (none at 80). Pass only if all hold: (a) the strip frame's border glyphs carry the cyan role and its top border holds the title `QUESTIONS_COUNT_LABEL.upper()`; (b) when the figure is drawable (digits or `+`) and fits, the figure occupies 3 consecutive rows made of the block glyph (`█`, ASCII `#`), otherwise it is one bold amber figure; either way the figure is the tallest text on the screen; (c) the plain pass contains `seen, not resolved: N \| closed by evidence: unavailable (no source)` whole on one line, with N equal to the figure; (d) at 80 columns no strip frame exists and (c) still holds | High | M-05 | Script for (a) border role, (c) and (d); Reviewer for (b) | P4 |
+| RB-05 | Required literals intact and uncut: gap notice, counts tokens without a mid-token cut, `PARTIAL (...)` text, the disclosure, `reason unknown`, desk title, retention line, `nextAction.kind` verbatim | High | guards RR 20, 31, 32, 47, 49 | Script (substring list) | every phase |
+| RB-06 | NO_COLOR pass: zero ESC bytes; text equals the coloured pass after SGR removal; hierarchy is carried by text and glyphs | High | G-1 | Script | every phase |
+| RB-07 | ASCII pass: output is pure ASCII; borders are `+ - |`; no `?` where a border should be | High | G-1 | Script | P3, and every phase for the ASCII text part |
+| RB-08 | Fit: every line at most the width in cells; rows at most the height; the footer keys are the last lines; no SGR 5 or 6 (blink); no mouse sequences | High | AD-5, standing constraints | Script | every phase |
+| RB-09 | 16-colour pass: the eight roles map to eight distinct ANSI colours (no two roles share an index) | High | G-2 | Script (theme table test plus SGR read) | P1 |
+| RB-10 | State words follow the fixed `STATE_ROLE` table of step 1.4 (D-7 default). Pass only if all hold: (a) every `workerState`, `dispatchStatus` or liveness cell, desk field or flags cell whose raw value is in the table carries exactly the table's role in the `.ansi`; (b) every other value (and `terminalState`, `nextAction.kind`) carries the `body` role, never a state role; (c) the word is printed in the plain pass in every case; (d) the table is non-empty: `T/test_theme.py` asserts that the tuple keys `("workerState", "running")`, `("workerState", "succeeded")`, `("workerState", "failed")`, `("dispatchStatus", "completed")` and `("liveness", "alive")` are in `STATE_ROLE` and that `FROZEN_ROLE == "state_frozen"`, so the row cannot pass on an empty table; (e) at the `standard` depth the four state roles have four different SGR codes | Medium | M-09 | Script (`.ansi` census against the table, `T/test_theme.py`) | P1 (desk fields P5) |
+| RB-11 | Absent values (`unknown`, `unavailable (no source)`, `reason unknown`) are muted; plain under NO_COLOR | Medium | M-08 | Reviewer | P1 |
+| RB-12 | A column heading and rule appear at 116 and 80 whenever rows are visible | Medium | M-10 | Reviewer plus script | P2 |
+| RB-13 | The 80-column key list is not cut and no key pair is split across lines | Medium | M-11 | Script | P2 |
+| RB-14 | Desk, measured on the plain and `.ansi` passes of `desk` and `desk-planask`. Pass only if all hold: (a) the question text leads: the first body line of the first pane after `DESK_TITLE` is `qid  age`, and all question-text lines (at most `DESK_TEXT_LINES`) come before any `label: value` line; (b) question-text lines carry the amber role and bold; (c) in the evidence pane every one-line field starts its value at the same cell offset (`label_width` = longest label plus its colon), measured as the column of the first character after the label on each such line; (d) a value that does not fit beside its label sits on the next line indented two cells, and no line exceeds the width | Medium | M-12 | Script for (a), (c), (d); Reviewer for (b) | P5 |
+| RB-15 | Title bar: the left title and a right `READ ONLY` badge (OPEN-3, gating until ruled) | Medium | M-13 | Reviewer | P2 |
+| RB-16 | Question list hierarchy (OPEN-1, gating until ruled). Pass only if all hold in the `.ansi`: (a) every question row line is bold, and its subject text carries the `body_bold` role (base colour); the one selected row is accepted with its marker and line in the bold amber `selected` role (step 1.4) and is not counted against this clause; (b) every run, state, caveat and retention line carries the `muted` role and no bold; (c) at 160 and 116 the first line inside the list pane after the disclosure is a question row (the caveat lines sit in the RETAIN CONTEXT pane, step 4.4), and at 80 the row lines carry strictly more bold characters than the caveat lines (0) | Medium | M-07 | Script (role census per line class) | P4 |
+| RB-17 | RETAIN CONTEXT grouping at 160 and 116 (OPEN-2, gating until ruled). Pass only if all hold: (a) when a frame whose top border contains `RETAIN CONTEXT` is drawn, it is slate-bordered, full pane width, below the list pane, and its body contains each of `run_line`, `caveat_line` and `retention_line` exactly once; (b) none of those three strings occurs anywhere else on the screen; (c) when the degrade rule of step 4.5 dropped the pane (small height), no such frame exists and each of the three strings still occurs exactly once, in the list pane; (d) at 80 columns no RETAIN CONTEXT frame exists | Medium | M-14 | Script (string census on the plain pass) | P4 |
+| RB-18 | Ledger screen: observation and attention content is in titled panes, with no invented owner, requester, mapped-tree or SIGNALS content (AD-1 to AD-4) | Medium | M-06 | Reviewer | P6 |
+| RB-19 | Q7: for the `PLAN_ASK` fixture (hash inside the first four wrapped lines) the 64-hex hash is whole on one line in the 80-column desk, nothing is lost, no line exceeds 80 cells; the trailing-hash fixture still ends its fourth line with `...` (D-6) | Medium | Q7 | Script | P3 |
+| RB-20 | A rule line precedes the footer and the key pair `n/p question` is intact | Low | M-15 | Script | P2 |
+| RB-21 | The 80-column counts strip is not cut inside a token | Low | M-16 | Script | P2 |
+| RB-22 | No wide blank band after the id column at 116 and 80: the longest run of consecutive spaces between two non-space characters inside a ledger row line, on the `base` fixture, is at most N, where N is the same measure on the 160-column rows of the same fixture, recorded in `VP/scores/baseline.md` in step 0.8 (a number measured at the current commit, not assumed) | Low | M-17 | Script | P2 |
+| RB-23 | The selected question has a role style in addition to the glyph | Low | M-18 | Reviewer | P1 |
+
+A phase closes only when every High and Medium row that is in scope for it passes; Low rows are recorded and may be deferred with a log line. A reviewer scores only the rows in scope for the phase, and marks later rows `N/A (scheduled P<n>)`.
+
+## Rows RB-24 to RB-29 (spec Part C section C.3, verbatim; RB-27 replaces RB-19)
+
+| ID | Criterion | Severity | Checked by | In scope from |
+|---|---|---|---|---|
+| RB-24 | No fact is printed twice on a screen: for the `desk` and `questions` fixtures at each width, the question text, the Run id, the count words and the freshness state of a source each occur once (header and panel state line excepted as RR 45 requires). | Medium | Script (string census) | Phase 2 |
+| RB-25 | Reasons: no `reason unknown` suffix on any question row when no reason is given; the title carries `reasons: none in source`; a row with a reason shows it. | Medium | Script | Phase 2 |
+| RB-26 | Status: dispatch, terminal and outcome show as one `ACTIVE` badge only when they are `active`, `active`, `none`; any other combination, including an absent value (`unknown`), shows three separate raw rows. | High (safety: unknown is not none) | Script | Phase 2 |
+| RB-27 | Hash: no run of 32 or more hexadecimal characters appears on the questions screen or the Decision Desk at any width; the rest of the ask is intact; both canaries pass. (Replaces RB-19.) | High | Script | Phase 2 |
+| RB-28 | Ledger: no `flags` column, no rule row, no `+N more` row above a `shown n/N` footer; liveness is a dot with a legend, and any non-alive value is spelled out, also under NO_COLOR. | Medium | Script plus Reviewer | Phase 2 |
+| RB-29 | Order and labels: question rows lead the list pane; desk labels are plain words with one aligned value column; no internal `msg_` id and no raw field name on the desk except in an expanded status row. | Medium | Reviewer | Phase 2 |
diff --git a/.dev/issues/409/visual-parity/rubric/reviewer-prompt.md b/.dev/issues/409/visual-parity/rubric/reviewer-prompt.md
new file mode 100644
index 000000000..46d33898d
--- /dev/null
+++ b/.dev/issues/409/visual-parity/rubric/reviewer-prompt.md
@@ -0,0 +1,40 @@
+# Reviewer prompt for the render gate (one fresh reviewer per width, no resume)
+
+You score one rendered width of the `superclaude observe` screens against the fixed rubric. You do not edit any file. You do not see the author's reasoning.
+
+## Inputs (and only these)
+
+- The rubric: `.dev/issues/409/visual-parity/rubric/rubric.md` (rows RB-01 to RB-29; score only the rows the caller lists as in scope for the phase, and mark every later row `N/A (scheduled P<n>)`).
+- For your width W: the mockup references from `.dev/issues/409/attachments/` (`signal-bridge.png`, `attention-ledger.png`, `decision-desk.png`) and the mockup text and ANSI exports inside `.dev/issues/409/orca-observer-design-package.zip` (`orca-observer-20261106/exports/<W>/` and `agent-focus/exports/<W>/`).
+- The rendered output for width W from the gate output folder you are given: `<screen>.txt`, `<screen>.<depth>.ansi`, `<screen>.nocolor.txt`, `<screen>.ascii.txt`, the `.png` rasterisations when present, and the folder's `checks.json` (script-checked rows).
+
+## Screen pairing
+
+- `ledger` is scored against `signal-bridge`.
+- `questions` is scored against `attention-ledger`.
+- `desk` and `desk-planask` are scored against `decision-desk`.
+
+Pairing is for colour, weight, titled borders and pane order only. The mockup title `OPEN HUMAN QUESTIONS` is retired by the spec and is not scored, and facts the screen does not have (owner, requester, mapped trees, SIGNALS bars, affected-session lists) must not be drawn (accepted divergences AD-1 to AD-8 in the spec).
+
+## What to do
+
+- Rows marked "Script" in the rubric are decided by `checks.json`; copy its status and verify one evidence line yourself by Reading the rendered file.
+- Rows marked "Reviewer" are yours: read the rendered files and the mockup files and decide.
+- A row passes only when every part of its wording holds. One quoted counter-example with its line number fails the row.
+
+## Output
+
+Return only this JSON (a `scores.json` for width W):
+
+```json
+{
+  "width": 160,
+  "iteration": 1,
+  "rows": {
+    "RB-01": {"result": "PASS|FAIL|N/A", "evidence": "one line: file:line or quoted text"}
+  },
+  "failing_high_medium": ["RB-.."]
+}
+```
+
+One evidence line per in-scope row. Do not suggest fixes. Do not edit files.
diff --git a/.dev/issues/409/visual-parity/png-route.md b/.dev/issues/409/visual-parity/png-route.md
new file mode 100644
index 000000000..fd1eba63e
--- /dev/null
+++ b/.dev/issues/409/visual-parity/png-route.md
@@ -0,0 +1,9 @@
+# PNG route (spec step 0.4)
+
+Result: FAIL. The text and ANSI tier is the gate for this work.
+
+- Date: 2026-11-18.
+- Attempt: `mcp__plugin_playwright_playwright__browser_navigate` to a `file://` URL of `ledger.16.html` (the harness capture at width 160, folder `iter-1/160/` of the Phase 1 gate output).
+- Tool answer: `Chromium distribution 'chrome' is not found at /opt/google/chrome/chrome. Run "npx playwright install chrome"`. No browser is installed in this workspace.
+- Font: `DejaVu Sans Mono` is installed (`/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf`), but its coverage of the mockup glyphs stays untested because no page could be rendered. Viewport: none was set, since the browser never started.
+- Decision: no dependency is added (owner decision D-10 default: no new PNG renderer). In the gate (spec section 8, step 3) the reviewer compares the `.txt` and `.ansi` files with the mockup text and ANSI exports, and uses the mockup PNGs as the visual reference. Installing a browser (`npx playwright install chrome`, or a tool such as `freeze`) needs a separate owner approval first.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
