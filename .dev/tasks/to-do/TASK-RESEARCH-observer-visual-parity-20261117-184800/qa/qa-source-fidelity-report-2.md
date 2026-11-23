# QA Report: Source-Document Fidelity (agent fidelity-agent-2)

**Status:** Complete
**Verdict:** PASS (with notes); blocking findings 0, minor findings 10
**Phase:** source-fidelity (report validation against sources), fix authorization false
**Date:** 2026-11-17

## Source-Document Fidelity Report

**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md (1918 lines, read in full in nine ranges; the coordinator fix to the desk age in step 5.3 is present and was read as it stands now)
**Source files checked:** about 45 files (19 named text sources, 9 mockups at 80 columns, the 116 and 160 mockup text and ANSI files by script, 9 current-state captures, 3 attachment PNGs, render_questions_screen.py, pr-591-comment.md), about 6,300 lines of text sources; the test files were checked at their cited ranges, not whole (see Summary)
**Date:** 2026-11-17

### Checklist 1: Semantic coverage (result: PASS, with minor omissions listed under item 2)

| Source component | Corresponding report content | Result |
|---|---|---|
| commands.py live screen: `LiveScreen.draw` :264-274, `run_loop` :282, `run_interactive` :351, `REDRAW_SECONDS` :58, shape tuple :265 | 2.2 live-path table and hop list; 6.3 D2 (shape tuple must include depth) | Covered and accurate |
| commands.py one-shot: `run_once` :225-251, `make_console(..., file=io.StringIO(), record=True)` :240, `export_text()` :242, `_emit` :245, `record_text` branch :243-244 | 2.2 path table, 2.8 diagram, 5.3 | Covered and accurate |
| export.py record and snapshot writers: `record_text` :71, `_question_lines` :89-118, `_questions_dict` :158-180, `snapshot_dict` :183, `snapshot_json` :219, `write_atomic` :257 (note: `export_text` is a Rich call in commands.py, not in export.py) | 2.2 "Export contract", 3.7 constraints, 7.2 Q1 | Covered; record file naming and state directory are not in the report (item 2) |
| Question-text-screen-only guarantee: `write_atomic` only at :216 and :327; text only via `.ask`/`screen_text`/`.shown` | 2.2, 3.7, SC-7, P0 canary tests | Covered and accurate (grep confirmed no use of `.ask`, `screen_text`, `.shown` outside view.py and render.py) |
| collector.py link flow: `Collector(questions, link)` :152-153, `read_questions`, `parse_questions(..., link=...)` | 2.2 "Data flow for question text" | Covered at the level the redesign needs |
| questions.py retention store | RR quotes only (retention wording); store constants not described | Not described (4.5 excludes "collector, parse and key-map internals" with a rationale) |
| keys.py: cbreak only :61, `_HANDLED` signals, no SIGWINCH, no mouse | 2.2 "Resize is by polling...", 3.7 "No blinking, no mouse" | Covered and accurate; the key decoder (arrow keys only) is not described |
| FINDINGS.md: 18 merged findings M-01..M-18 (5 High, 9 Medium, 4 Low), G-1, G-2, AD-1..AD-7, OPEN-1..3, O-1, R-1..R-3 | 1.3, 4.1a, 4.1b, 4.1c, 8.10 | All ids, severities, reviewer disagreements and the O-1 recommendation survive |
| rendering-rules.md cited lines (13, 17, 20, 25, 31, 32, 33, 38, 41, 42, 43, 47, 49, 50, 57, 59, 61, 70, 82, 91, 93) | 2.4, 4.3b, 3.7 | All cited line contents match (checked line by line) |
| render_current.py emit flow (`emit` :68-75, `HEIGHT = 50` :38, `main()` at :93, docstring :6-9) | 2.1, 2.5, 5.x, Phase 0 steps 0.1 and 0.2 | Covered and accurate (line count off by one, item 3) |
| Zellij `config.kdl`, `themes/aidev02.kdl`, `layouts/agent.kdl`, `layouts/default.kdl` | 2.5, 5.4, 6.4 | Covered and accurate |
| pyproject.toml dependencies and Makefile targets | 2.5, 5.5, 6.2 | Covered and accurate |
| Mockups (80-column set read directly; 116 and 160 geometry measured by script) and `inputs/current/` | 2.4 colour decode, pane geometry, "Spec versus code" | Colour codes and pane geometry match; two descriptive slips and one omission (items 2 and 3) |

### Checklist 2: Detail preservation (result: PASS with minor omissions)

Preserved correctly (each checked against source): function signatures and line ranges for `run_once`, `LiveScreen.draw`, `run_loop`, `_write_snapshot`, `record_text`, `snapshot_dict`; the exact `make_console` option list (`width`, `height`, `highlight=False`, `markup=False`, `emoji=False`, `color_system=None if no_color else "standard"`, `no_color`, `safe_box=policy.ascii`, `record`); `GLYPHS` has exactly `selected`, `truncate`, `hrule`; `MIN_WIDTH=80`, `MIN_ROWS=8`, `FULL_WIDTH=160`, `LINE_WIDTH=116`; four width classes; `SCHEMA_VERSION = 1`; `_TEXT_FIELDS` :25-45; both gate constants at :67 and :70 with `# fmt: skip` and the test regexes at test_commands.py:747-756 and :762-772; `REDRAW_SECONDS = 0.5`; the 8 mockup RGB triples and bold usage; the 16-colour and 256-colour indexes (recomputed with Rich 15.0.0: base 15/189, muted 7/145, slate 8/60, amber 11/214, cyan 14/80, green 7/115, red 7/210, violet 7/147, identical to 2.4); the `bold #ff8800` depth outputs `\x1b[1;91m`, `\x1b[1;38;5;208m`, `\x1b[1;38;2;255;136;0m` (re-run, identical); the `export_text` and `export_text(styles=True)` NO_COLOR table (re-run, identical); `safe_box` True and False print identical rounded borders (re-run); golden structure (5 variants x 14 keys; link-off scenarios `five` and `long_subject` at 24/24/25 and 22/22/23 lines; no ESC byte; release-1 file has no trailing newline, link-off file has one); 766 tests passed (re-run: 766 passed in 23.80s); pyproject dependency list and line range 34-43, `pexpect>=4.9` at :41, `ruff==0.15.20`; Zellij 0.44.2 path, config directives (theme `aidev02`, `show_release_notes false`, `default_shell "/bin/bash"`, welcome-screen plugin), `default.kdl` bars (1-row tab-bar, 2-row status-bar), `agent.kdl` theme `aidev02_agent` with magenta 5 in `frame_selected` and `ribbon_selected` background (aidev02 uses 6 cyan), `aidev02` ANSI-16 only with ANSI 4 forbidden.

Details that did not survive into the report (all minor, none contradicts a report statement):

- export.py file naming and location: record file `observe-<generated_at with ":" replaced by "-">.txt` (export.py:247-250), `SNAPSHOT_NAME = "snapshot.json"`, `state_dir()` under `$XDG_STATE_HOME` or `~/.local/state/superclaude/observe`, atomic 0600 write via `mkstemp` and `os.replace` (export.py:236-274).
- collector.py constants `INTERVAL = 15.0`, `MAX_BACKOFF = 60.0`, `QUESTION_PAGE_CAP = 4`; questions.py `RETENTION_BOUND = 1000`, `WINDOW_ROWS = 100`, `NO_LONGER_IN_WINDOW`, `RETENTION_EXCEEDED`; keys.py `ESC_WAIT`, `READ_TIMEOUT`, and that only Up/Down arrows are decoded. Report 4.5 excludes these on purpose ("no gap: unchanged by presentation work"), so this is a stated scope choice.
- The colour decode omits cyan as a pane-frame colour in two mockups (finding F-2 below).

### Checklist 3: Phantom finding detection (result: PASS, no phantom found; 34 claims traced, requirement was at least 5)

| # | Report claim | Source read | Result |
|---|---|---|---|
| 1 | Gates `QUESTION_GATE_PASSED` (commands.py:67) and `QUESTION_LINK_PASSED` (:70) are True | commands.py:67, :70 | True |
| 2 | `--once --width` path: `make_console(policy, file=io.StringIO(), record=True)` :240, `console.print(render(...))` :241, `export_text()` :242 | commands.py:238-245 | True |
| 3 | `write_atomic` called only at commands.py:216 and :327 | commands.py (all uses) | True |
| 4 | `record_text` writes `q.qid | q.text` plus ` | dispatchId=<id> | link=<state>` (export.py:103-111) | export.py:103-111 | True |
| 5 | export.py imports no Rich; `test_export.py:238-243` forbids it | export.py:11-18; test_export.py:238-243 | True |
| 6 | `counts_line` written verbatim to the record (export.py:99); `header1` read at export.py:76 | export.py:76, :99 | True |
| 7 | No test references `LiveScreen` or `run_interactive`; `FakeScreen` at test_commands.py:285-297 | grep over tests/observe; test_commands.py:285-297 | True |
| 8 | Live resize is polling, `_HANDLED` = INT/TERM/HUP/TSTP/CONT, cbreak at keys.py:61, no SIGWINCH | keys.py:27-33, :61; grep SIGWINCH none | True |
| 9 | Only one `Console(` in the package (terminal.py:114); no `force_terminal`, `legacy_windows`, `_environ` | grep over observe/*.py | True |
| 10 | No `READ ONLY` text anywhere under the package | case-sensitive grep, 0 matches | True |
| 11 | `render()` is one `Text(line, no_wrap=True, overflow="crop")` per line, render.py:524-531; imports :12-14 | render.py | True |
| 12 | `QuestionLine.text` is subject based (view.py:744), counts token `POLICY FROZEN unavailable (no source)` (view.py:948), `counts_line` view.py:761, `DESK_TEXT_LINES = 4` view.py:99, `QUESTIONS_TITLE = "COORDINATOR QUESTIONS"` view.py:53 | view.py | True |
| 13 | `ASK_CAP = 400` parse.py:475, applied :503 | parse.py | True |
| 14 | Mockup frame heights 48 (160) and 42 (116, 80) | `wc -l` of all nine `.txt` | True |
| 15 | Nine `.ansi` files use 8 truecolor foregrounds, bold only, no background, no dim/italic/underline/reverse; `ESC[0;1;` count 3 to 16 per file; 48 ESC lines in 160 signal-bridge | SGR census over all `.ansi` | True |
| 16 | All nine `current/*/ansi-*.txt` hold 0 ESC bytes | grep per file | True |
| 17 | Attachments' three PNGs are byte-identical to the 160 mockup PNGs | `cmp` x3 | True |
| 18 | Pane geometry for all nine mockups (46/74/34, 114+42, 76+80, 66+46, 70+42, 78-wide stacks, row starts 6/14/16/21) | script over `.txt` top borders | True for every pane listed |
| 19 | Current screens at height 40: 40 lines at 160, 116 and 80; 28/29/28 rows; 80-column footer cut at `e exp>`; 0 ESC | re-ran `LINES=40 superclaude observe --once --width W --fixture base` | True |
| 20 | Current questions and desk captures: disclosure wraps to two lines at 116, `n/p` then `question` split, desk has 9 `label: value` lines | `current/116/questions.txt`, `current/80/desk.txt` | True |
| 21 | FINDINGS counts (5 High, 9 Medium, 4 Low; 3 DEFECTs M-08, M-10, M-11; 7 ADs; 2 guards) | FINDINGS.md lines 12-18 | True |
| 22 | "153 cells" is not on RR line 30 | rendering-rules.md:30 | True (line 30 has no such number) |
| 23 | RR 61 requires the two 80-column invariant lines; RR 42 states in-memory retention; RR 43 says one stacked block was built | rendering-rules.md:42, :43, :61 | True |
| 24 | RR 38 retires `OPEN HUMAN QUESTIONS`; the 160 and 116 mockups still title it so | rendering-rules.md:38; mockup `.txt` | True |
| 25 | pr-591-comment.md lines 26-31 list the plan-ask storage as unverified; consideration 8 asks for a hash fixture | pr-591-comment.md | True |
| 26 | `render_current.py` has no `__main__` guard (calls `main()` at :93), writes `export_text(styles=True)` :75, `HEIGHT = 50` :38 | render_current.py | True |
| 27 | pyproject runtime dependency list and line range; no image or render dependency; Makefile has no render, screenshot or observe target | pyproject.toml:34-56; Makefile target list | True |
| 28 | `zellij --version` 0.44.2, `/usr/local/bin/zellij`, `setup --check` config well defined, help text flags `-l/--layout`, `--layout-string`, `run -f --width --height -x -y`, `dump-screen -a -f -p --path` | ran the commands | True |
| 29 | `config.kdl` cites upstream `default.kdl:511` and `:236-238` | config.kdl comments | True |
| 30 | `aidev02` forbids ANSI 4 (blue); `agent.kdl` differs in `frame_selected` and `ribbon_selected` (5 vs 6) | themes/aidev02.kdl:80-95, layouts/agent.kdl:151-165 | True |
| 31 | 16-colour and 256-colour downgrade table | recomputed with Rich 15.0.0 | True, all 16 values identical |
| 32 | `export_text` NO_COLOR probe table and `safe_box` identical borders | re-ran probes | True |
| 33 | Gate-test line ranges 747-756 and 762-772; `test_commands.py:121`, `:99`, `:105`; `test_export.py:53`, `:307-332`; `test_snapshot_schema.py:457-479`; `test_golden_contract.py:43-58` | test files | True (all content matches) |
| 34 | Goldens: 14 keys x 5 variants, scenarios and line counts, git history (`cd8736199`, `3206bdb9c`), commit `9e2608b03` exists, `.dev/issues/606/issue-body.md:84` lists the four files, 22 test modules and 28 Python files, 766 passed | json load, `git log`, `git cat-file`, `sed`, `pytest -q` | True |

No claim in the report lacks a traceable source. All [UNVERIFIED] and [CODE-CONTRADICTED] tags that were checked against code were tagged correctly (the corrected claims C1 to C8 in 9.5 all reproduce).

### Checklist 4: Accuracy of code characterization and intent labelling (result: PASS, 3 minor imprecisions)

- The report separates code from intent well: FINDINGS and RR are called "design reference" or "intent" wherever code does not confirm them (2.4, 4.3b, "RR 61 self-contradiction"), and statements built from the spec carry [CODE-CONTRADICTED] or [STALE DOC] when code differs (checked FROZEN token, `render()` versus `screen_lines` location, 153 cells, width classes).
- The one-shot and live path descriptions match commands.py exactly, including that `export_text()` (not `styles=True`) is what `run_once` calls, and that `run_once` without `--width` uses `record_text` with no Rich.
- Imprecision A (7.2 Q1): "export.py ... writes ids, times and counts (never question text)". True for `_questions_dict`; the record (`record_text`) also writes each question's subject-based `q.text` (`age  subject  reason unknown`, view.py:744, export.py:103-111). Sections 2.2 and 3.7 state this correctly, so the summary is a compression, not an error in the evidence. Minor.
- Imprecision B (2.8 diagram): `snapshot_json(view) export.py:183`; `snapshot_dict` starts at :183, `snapshot_json` at :219. Minor citation.
- Imprecision C (2.4, "Spec versus code", ledger 116 row): "5 header lines". `current/116/ledger.txt` lines 1-4 are the header (title, freshness, two counts lines), then the gap notice at line 5. 2.1's measured table and the 160 row use the same convention as 4 header lines plus a separate gap notice, so the 116 row is inconsistent. Minor.

### Checklist 5: No aspirational claims (result: PASS)

- Section 2 states only code-traced facts; items the research marks [UNVERIFIED] are moved to 2.7 and not asserted. Sections 3 (target) and 8 (plan) are labelled as target and plan, and every new name there (`theme.py`, `Line`, `_frame`, `STATE_ROLE`, `render_compare.py`, `T/test_theme.py`, `count_figure`, `RETAIN_TITLE`) is described as to be added, never as present. Grep of the package confirms none exists today (`LiveScreen` has no test, no `theme.py`, no box glyphs in `GLYPHS`).
- Zellij capabilities: nothing is described as exercised. The report states "no session was started" and tags runtime behaviour [UNVERIFIED]. Two capabilities it tags [UNVERIFIED] are in fact verifiable from local help text (finding F-5): this understates evidence, it does not overstate it.
- Web findings are labelled external context with URLs and kept out of Section 2.

### Fidelity Findings

Severity rule applied (I16): CRITICAL and IMPORTANT are blocking (wrong behaviour, a false claim, a missing required deliverable); MINOR is wording, citation, a moved line, or an omission that makes no statement false. No blocking finding was found. Every row below is MINOR and is recorded as a note.

| # | Type | Source File | Report Section | Finding | Severity |
|---|---|---|---|---|---|
| F-1 | Inaccurate | `.dev/issues/409/visual-parity/inputs/mockups/80/agent-focus-attention-ledger.txt` (lines 7-9, 12-18) | 2.4 "Mockup pane geometry", row "attention-ledger 80" | The row says "three plain question lines above one SELECTED SIGNALS pane". The three lines above the pane (7-9) are a focused card: headline `Choose schema compatibility policy`, `Owner Human operator ...`, `Evidence demo:messages/Q01`. The question lines `Q01 45m`, `Q02 20m`, `Q03 10m` and the two invariant lines are inside the pane (lines 14-18). The report knows the card (AD-7 "forced focused card"), so the geometry row is a loose description, not a missed fact. | MINOR |
| F-2 | Missing | `mockups/80/agent-focus-attention-ledger.ansi`; `mockups/160/signal-bridge.ansi`; `mockups/160/signal-bridge.png` | 2.4 and 3.2 colour tables; rubric RB-01(e) and RB-02 in 8.4 | The tables list cyan for "screen title, count tile, running sessions" and slate for "secondary pane borders". Script census of border glyphs: the only pane at 80 columns in the attention ledger (SELECTED SIGNALS, round) is cyan (188 cyan border glyphs, slate only on the 78-glyph footer rule); the 160 signal-bridge SIGNALS heavy pane is cyan (133 glyphs); STALE in the SIGNALS list is bold amber (FINDINGS M-09 also says "stale amber"; the amber row omits it). RB-01(e) "every secondary-pane border glyph and the footer rule is slate" and RB-02 would therefore disagree with the 80-column mockup if a reviewer scored against it. The plan chooses its own pane colours (P3 weight rule), so no report statement is false; the census is incomplete. | MINOR |
| F-3 | Distorted | all nine mockup `.txt` files, line 2 (`SYNTHETIC · READ ONLY`) | 3.2 colour table, amber row (line 502) | Writes the badge as `SYNTHETIC / READ ONLY` (slash). The source and section 2.4 (line 289) have `SYNTHETIC · READ ONLY` (middle dot). | MINOR |
| F-4 | Inaccurate | `inputs/current/116/ledger.txt` (lines 1-5) | 2.4 "Spec versus code", row "ledger 116" | "5 header lines": the header is lines 1-4 (title, freshness, two counts lines) and the gap notice is line 5. Section 2.1's measured table and the 160 row count 4 header lines plus a separate gap notice. | MINOR |
| F-5 | Missing evidence (understated) | `zellij action --help` line 124 (`send-keys`), `zellij attach --help` line 11 (`-b, --create-background`); commands.py:165-166 and :373 | 5.4.3; 5.6 roll-up; 2.2, 4.1b, 8.8 and 9.2 row 11 | The report tags `send-keys` and `attach --create-background` on 0.44.2 as [UNVERIFIED] because the research read only the first 120 lines of `zellij action --help`. Both are in the local help text (read-only commands, no session started). Likewise "whether `run_interactive` accepts `--fixture` [UNVERIFIED]" is answerable from code: `run_interactive` builds `FixtureSource` through `_build_source` (:165-166) and sets `live = not options.fixture` (:373); only the pty behaviour of the real `LiveScreen` is unverified. The hedges are honest and no step depends on them wrongly (step 1.6(g) builds `LiveScreen` itself), so this is understated evidence, not a false claim. | MINOR |
| F-6 | Inaccurate citation | `render_current.py` (93 lines by `wc -l` and by the read); `export.py:183` vs `:219`; `test_commands.py:671, :674, :691`; `pyproject.toml:41` | 2.5 and 6.2 ("94 lines"); 2.8 diagram ("snapshot_json ... export.py:183", that is `snapshot_dict`; `snapshot_json` is :219); step 3.6 and 8.2 D-9 (":672-675 and :690", actual `COORDINATOR QUESTIONS` at :671 and :691, `seen, not resolved: 4` at :673-675); 6.2 ("`pexpect` 4.9.0 (declared)", declared as `pexpect>=4.9`; 4.9.0 is the installed version per the research) | Moved or off-by-one citations on true claims; each true statement is otherwise unchanged. | MINOR |
| F-7 | Inaccurate (compression) | `export.py:103-111`; `view.py:744` | 7.2 Q1 | "export.py ... writes ids, times and counts (never question text)". The record also writes each question's subject-based line text (`age  subject  reason unknown`). 2.2 and 3.7 state this precisely; the payload question text is indeed never written. | MINOR |
| F-8 | Missing | `export.py:236-274`; `collector.py:28-34`; `questions.py:21-24`; `keys.py:22-23, 217-235` | 2.2, 4.5 | Record file naming, default snapshot path and 0600 atomic write, collector timing and question-page constants, retention store constants and the arrow-only key decoder are not in the report. 4.5 declares collector, parse and key-map internals out of scope for a presentation redesign, so this is a stated omission. | MINOR |
| F-9 | Inaccurate (dangling reference) | `FINDINGS.md` lines 12-18, 26-139 (High/Medium/Low) | 4.1 intro (line 614), 4.1a | "Severity follows the scale in the header": the report header has no severity scale. 4.1a shows FIND High as Critical, Medium as Important, Low as Minor (with the FIND label kept in Notes, and M-08, M-10, M-11 raised by the C8 rule that is explained), while 1.3 and 8.10 keep High, Medium and Low. No severity is lost, but the mapping is implicit. | MINOR |
| F-10 | Distorted attribution | `mockups/160/decision-desk.ansi` (line 9 `Scope: 4 sessions | observed 45m ago`); `mockups/160/agent-focus-attention-ledger.ansi` (`45 MIN` bold amber) | 2.4 and 3.2 amber row ("ages"); steps 1.4 and 5.3; RB-01(c) and RB-14 | Bold amber ages exist in the 160 and 116 ledger list only. The desk mockup shows the age as base-colour text. The coordinator fix (desk `qid  age` bold amber, step 5.3) is consistent with step 1.4, RB-01(c) and RB-14, so the plan is internally coherent, but the role table presents "ages" as a mockup colour use without saying the desk extension is a design choice. | MINOR |

### Summary

- **Files checked:** 19 named source files read or inspected (5 observe modules read whole; 5 test files and the golden and linkoff tests checked at every cited range, not whole; FINDINGS.md, rendering-rules.md, render_current.py, 4 Zellij files, pyproject.toml, Makefile), plus the 9 mockup files under `mockups/80/` (3 PNG read, 2 TXT read, 4 by script census), `mockups/116` and `mockups/160` `.txt` and `.ansi` by script, 6 files under `current/80/` plus the 116 and 160 captures (partly read, ESC census on all nine `ansi-*`), `render_questions_screen.py`, the 3 attachment PNGs (read, and byte-identical to the 160 mockup PNGs), `pr-591-comment.md`. Not read whole: test_render.py, test_terminal.py, test_linkoff_screen_reference.py, view.py, parse.py, terminal.py (only the report's cited lines), which are outside the assigned list.
- **Claims verified:** 34 traced in the table above, plus about 40 further line and content checks of the cited ranges, five re-run probes (Rich downgrade, `export_text`, `safe_box`, `LINES=40` one-shot screens, pytest baseline) and the Zellij command outputs.
- **Fidelity issues:** 10, all MINOR (Missing 3: F-2, F-5, F-8; Inaccurate or distorted 7: F-1, F-3, F-4, F-6, F-7, F-9, F-10). Blocking (CRITICAL or IMPORTANT): 0.
- **Verdict: PASS (with notes).** The report represents the code, spec, findings, mockups, Zellij setup and tooling faithfully; no phantom finding, no false behaviour claim and no aspirational claim was found. The coordinator fix (desk age bold amber in step 5.3) is present and consistent with steps 1.4, RB-01(c) and RB-14. Minor findings are not rechecked and need no fix pass.

**Self-audit.** If I told the owner I found no blocking issue, the evidence is: every code citation was compared with the file text (not with another report), the numeric probes were re-run in fresh processes, the mockup geometry and colour tables were recomputed by script from the `.txt` and `.ansi` files rather than read from the report, and the three 80-column PNGs plus the three attachment PNGs were viewed. I did not read the PNGs at 116, and I viewed the 160 set only through the byte-identical attachments.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist items 1 to 5; item 2 verified with three minor omissions recorded)
**Tool engagement:** Read: 28 (2 more over-size reads rejected and re-issued in ranges) | Grep: 7 | Glob: 0 | Bash: 27 read-only commands (counts, censuses, `--once` re-runs, Rich probes, `pytest -q -p no:cacheprovider` with bytecode writing off, Zellij help text). Read+Grep+Glob = 35, above the 5 checklist items. No web tools used. No file was modified except this report.
**Unchecked items:** none. **Unverifiable items:** none (the 116-column PNGs and `mockups/116/*.png` were not viewed; their `.txt` and `.ansi` twins were measured instead).

## QA Complete

**Status:** Complete

