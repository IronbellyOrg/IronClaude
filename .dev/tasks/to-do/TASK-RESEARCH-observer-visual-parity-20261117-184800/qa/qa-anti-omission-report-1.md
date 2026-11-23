## Anti-Omission Report

**Status:** Complete (see the last line)
**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md
**Input files checked:** research/01-render-view-terminal-pipeline.md, research/02-live-screen-commands-export.md, research/03-tests-goldens-fixtures.md, research/web-01-rich-composition-and-colour.md, synthesis/synth-01-problem-current-state.md, synthesis/synth-02-target-gaps.md, synthesis/synth-03-external-findings.md (total findings enumerated: 1070)
**Date:** 2026-11-17

## Method

- Coverage judged by meaning, never by ID citation. The report was read directly at lines 1-480 and 939-1920; Sections 3-5 (lines 482-938) were verified mechanically against the synthesis files (see "Synthesis files").
- The 4 research files were enumerated finding by finding and each finding was searched in the report by substance (Read plus fixed-string greps on distinctive tokens such as `_prefix_length`, `INSPECTOR_HELP`, `display failed`, `ZWJ`, `make_question_rows`).
- The 3 synthesis files: each non-blank, non-separator line (a table row, bullet or paragraph) is one finding. Each was tested for a byte-exact copy in the report (`grep -Fx`). 644 of 668 lines are copied byte for byte; the 24 that differ were compared against the report text and are edited or corrected versions of the same finding (see "Synthesis files").
- Statuses: R = represented (anchor given); D = covered-by-dedup (merged or superseded; surviving item named); X = omitted (substance appears nowhere in the report). "R (decl)" = represented as a declared, reasoned exclusion in the report itself (report 4.5, 7.4, 9.6): counted as represented because it is not a silent drop, and listed separately in the Summary.
- Anchors are report section numbers.

## Batch 1: research/01-render-view-terminal-pipeline.md (127 findings)

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R01-01 | Constants MIN_WIDTH 80, MIN_ROWS 8, FULL_WIDTH 160, LINE_WIDTH 116 | R | 2.1 |
| R01-02 | TOO_NARROW_TEXT / TOO_SMALL_TEXT diagnostics | R | 3.3 narrow row; 2.3 |
| R01-03 | GLYPHS holds three names only, no box glyph (G-1) | R | 2.1, 4.1b G-1 |
| R01-04 | TerminalPolicy fields; no colour-depth or styled flag | R | 2.1 |
| R01-05 | width_class has four classes incl. `short` (task prompt wrong) | R | 2.1, 4.3a |
| R01-06 | resolve_policy: NO_COLOR and ASCII independent; no TERM/COLORTERM/isatty | R | 2.1 |
| R01-07 | make_console arguments; colour hard-coded "standard" (Q4) | R | 2.1 |
| R01-08 | safe_box does not ASCII-ize a Rich Panel (probe) | R | 2.1, 4.3a, 9.5 C1 |
| R01-09 | glyph / ascii_safe (`?` per non-ASCII) / clip semantics, plain str | R | 2.1 |
| R01-10 | Only one `Console(` in observe/ | R | 2.1 |
| R01-11 | terminal.py takeaways (two colour switches; GLYPHS must grow; style after clip) | R | 3.4, 8 step 1.3 |
| R01-12 | sanitize strips OSC/DCS/SOS/PM/APC/CSI/ESC, Cc/Cf/Cs | R | 2.1 |
| R01-13 | sanitize `line` vs `block` modes and newline normalisation | X | OM-2 |
| R01-14 | Markup safety not sanitize's job; styled spans must come from the renderer | R | 2.1 |
| R01-15 | A 64-char hex token passes sanitize unchanged; cut decided by wrap/clip | X | OM-2 |
| R01-16 | No sanitizer change needed for styling | R | 2.1 (implicit), 3.7 |
| R01-17 | Return types of build_view / screen_lines / render and helpers | R | 2.1 |
| R01-18 | No render.py function returns Text/Table/Panel/Layout/Columns; imports | R | 2.1 |
| R01-19 | render() only Rich builder; source guard regex test_render.py:396-403 | R | 2.1, 2.3 |
| R01-20 | Callers of render/make_console (commands.py:38-41, 240-242, 264-274, 244) | R | 2.2 |
| R01-21 | Styled output reaches a person only via LiveScreen; `--width --once` strips styles | R | 2.2 |
| R01-22 | Probe: Rich emits ANSI into StringIO; RGB downsampled to 16 colours | R | 2.1 colour table |
| R01-23 | printed() captures gain ESC once styled | R | 2.1, 2.3, 8 step 1.6 |
| R01-24 | cell_len of an escape run counts its printable part, so width test needs strip | R | 3.6 SC-1 |
| R01-25 | Call-chain takeaways | R | 2.8 |
| R01-26 | `_prefix_length` is per-character; combining/zero-width chars never joined to base; len() used as char index | X | OM-3 |
| R01-27 | wrap(): cell-based, break at last space, hard cut, never truncates | R | 2.1 |
| R01-28 | _pad / _cell = clip then pad | R | 2.1 helper table, 8 step 3.2 |
| R01-29 | counts_lines token list and protected/unprotected rule | R | 2.1 |
| R01-30 | counts_lines layout (two-space join, second line, cut path, cut=True) | R | 2.1, 8 step 2.4 |
| R01-31 | Measured COUNTS line counts at 160/116/80 | R | 2.1 measured table |
| R01-32 | RR 20 `FROZEN` vs code `POLICY FROZEN unavailable` | R | 2.1, 4.3a |
| R01-33 | `_marker` always 2 cells; first column ("",2) | R | 2.1 `_columns` row ("2-cell marker column") |
| R01-34 | full layout: 11 columns, fixed sum 114, 160 cells used, flags elastic | R | 2.1, 3.5, 6.1 |
| R01-35 | line/short column widths (kind 18/14, liveness 14, age 7/6, flags 16, id 38 at 80) | X | OM-4 (the `line` id formula is in 2.1/M-17; the individual widths are not) |
| R01-36 | _row_line: cells joined by a space, rstrip, clip; offsets derivable | R | 8 step 1.4 |
| R01-37 | _header_lines rule is dashed per column; only called at render.py:498 | X | OM-4 |
| R01-38 | Header gate `width_class == "full" and visible_rows` and mirror at 439 (M-10) | R | 2.1, 4.1a M-10, RN-2 |
| R01-39 | Inspector (render.py:255-287): title, wrapped label:value, scroll window, above/below, `[:max(budget,1)]` as the only hard height clamp, INSPECTOR_HELP footer | X | OM-1 |
| R01-40 | `_notes` joins filter/historical/duplicates/selection notes with two spaces into one wrapped element | X | OM-4 |
| R01-41 | _help_lines: clip when questions off, wrap when on (M-11) | R | 2.1, RN-3 |
| R01-42 | _question_line link on/off; age is part of `lead`; `...` cut | R | 2.1 |
| R01-43 | _desk_lines stacked; DESK_TEXT_LINES 4 | R | 2.1 |
| R01-44 | _panel_lines exact order | R | 2.1 |
| R01-45 | cell_len vs len inventory (cell_len at listed lines; len for counts; `sep = len(SEPARATOR)`) | X | OM-3 |
| R01-46 | screen_lines in order (narrow/small branches, head, tail, footer probe, ledger, footer) | R | 2.1, 8 steps 2.2-2.3 |
| R01-47 | header1 is one string wrapped; as-of lands alone at 80; no READ ONLY text | R | 2.1, 4.1a M-13 |
| R01-48 | Footer height probe (423-431) | R | 8 step 2.3 |
| R01-49 | Questions-on height budget `spare` formula, ledger_fixed, base | R | 2.1 |
| R01-50 | Desk sized first, DESK_HIDDEN replacement, owner comment 2026-11-12 | R | 2.1, 8 step 5.4 |
| R01-50x | Third fallback: no panel, `gap_notice` plus `; decision desk hidden...` when a desk existed | X | OM-5 |
| R01-51 | At least one ledger row always forced (`max(...,1)`) | R | 2.1, 3.5 |
| R01-52 | Measured screens table at base fixture | R | 2.1 |
| R01-53 | Pinned questions-on link-off screen sizes (24/24/25 rows, widths 160/113/80, 12/13 question-block lines) | R | 7.1 height rules; 2.3 |
| R01-53x | 80-column questions screen footer is 3 lines; no heading line at 116/80 on the questions screen | X | OM-5 |
| R01-54 | Where width and height budgets are enforced | R | 2.1 |
| R01-55 | No final `lines[:height]` clamp | R | 2.1, 3.5 |
| R01-56 | Q7 probes (wrap whole hash; label moves; 100-char token hard cut; desk; _question_line `...`; `_cell` `>`) | R | 2.3, 7.2 Q7 |
| R01-57 | Frames reduce width 2-4; hard-wrap path needs a visible tested rule | R | 4.1b, 7.2 Q7, 9.2 row 10 |
| R01-58 | render.py takeaways (every wrap width reduced; flags elastic; two single-condition causes) | R | 2.8, 3.5 |
| R01-59 | View constants list (GAP_NOTICE ... FROZEN_MARKER) | R | 2.1 and plan steps cite the used ones |
| R01-60 | text_of: bare `unknown` vs quoted real value | R | 2.1 |
| R01-61 | Lines the view decides (header1, counts_tokens, changes_line, ...) | R | 2.4 change map, 8 |
| R01-62 | QuestionLine text vs screen_text/shown/ask; export writes q.text only | R | 2.1, 2.2, 3.7 |
| R01-63 | DeskView fields; single linked row; DESK_WORKTREE_NOTE | R | 2.1, 3.7 AD-4 |
| R01-64 | RowView raw strings available to colour table | R | 2.1 |
| R01-65 | screen_lines defined at render.py:390 and called only at :529; render imported only by commands.py:38 | X | OM-6 |
| R01-66 | tests/observe modules that import screen_lines/render | R | 2.3 |
| R01-67 | Consequences 1-3 (T47, T64, printed equality) | R | 2.3, 3.6 SC-5, SC-19 |
| R01-68 | Consumers takeaways (keep screen_lines stable, add styled path) | R | 6.1 C, 7 |
| R01-69 | Depth probes standard/256/truecolor | R | 2.1 table |
| R01-70 | `auto` resolves to None on StringIO | R | 2.1 |
| R01-71 | Rich caches Style codes per process | R | 2.1, 9.4 row 33 |
| R01-72 | Inference that slate and muted collapse to greys | D | superseded by 04 measurement; report 2.6 row 1, 6.0 row 1 |
| R01-73 | Colour and ASCII independent; NO_COLOR drops bold | R | 2.1, 3.4 |
| R01-74 | Map M-01 | R | 2.4 map |
| R01-75 | Map M-02 | R | 2.4 map |
| R01-76 | Map M-03 | R | 2.4 map |
| R01-77 | Map M-04 | R | 2.4 map |
| R01-78 | Map M-05 | R | 2.4 map |
| R01-79 | Map M-06 | R | 2.4 map |
| R01-80 | Map M-07 | R | 2.4 map |
| R01-81 | Map M-08 | R | 2.4 map |
| R01-82 | Map M-09 (only full layout and desk carry state columns) | R | 2.4 map, 4.1a |
| R01-83 | Map M-10 | R | 2.4 map |
| R01-84 | Map M-11 | R | 2.4 map |
| R01-85 | Map M-12 | R | 2.4 map |
| R01-86 | Map M-13 | R | 2.4 map |
| R01-87 | Map M-14 | R | 2.4 map |
| R01-88 | Map M-15 | R | 2.4 map |
| R01-89 | Map M-16 | R | 2.4 map |
| R01-90 | Map M-17 | R | 2.4 map |
| R01-91 | Map M-18 | R | 2.4 map |
| R01-92 | Map G-1 | R | 2.4 map |
| R01-93 | Map G-2 | R | 2.4 map |
| R01-94 | View.footer feeds budget; ledger_fixed/base/spare must count frame rows | R | 3.5, 8.3 |
| R01-95 | Candidate glyphs are 1 cell; CJK 2 cells; Rich spans are char indexes | R | 6.1 facts, 8 step 1.3 |
| R01-96 | Option 1 style map over strings (regex/offset hazards) | R | 6.1 Option A |
| R01-97 | Option 2 segment builders; wrap/clip stay authorities | R | 6.1 Option C |
| R01-98 | Option 3 hand-built frame helper and its five problems | R | 6.1 Option A, 8 step 3.2 |
| R01-99 | Option 4 Rich Panel/Table/Columns and its five cons | R | 6.1 Option B |
| R01-100 | Option 5 two-column zip with cell_len; candidate widths 114+42 etc. | R | 6.1, 8 step 4.2 |
| R01-101 | Option 6 count tile render-only from panel fields; block glyphs 1 cell | R | 4.1a M-05, 8 step 4.3 |
| R01-102 | Option 7 ASCII mapping must go through glyph() | R | 8 step 3.1 |
| R01-103 | Map/insertion takeaways (four render-only findings; M-09 narrow; NO_COLOR drops bold) | R | 2.8, 4.1a |
| R01-104 | Gap 1 "153 cells" unverified | R | 4.3a, 9.4 row 29 |
| R01-105 | Gap 2 width classes | R | 4.3a |
| R01-106 | Gap 3 safe_box | R | 4.3a, 9.5 C1 |
| R01-107 | Gap 4 FROZEN token | R | 4.3a, 9.5 row 38 |
| R01-108 | Gap 5 styled capture for ANSI exports | R | 4.1b, 9.2 row 8 |
| R01-109 | Gap 6 colour depth policy options | R | 6.3, 9.2 row 6 |
| R01-110 | Gap 7 T47/T64 re-baseline | R | 9.2 row 5 |
| R01-111 | Gap 8 no height clamp, frame-heavy at 24/8 unmeasured | R | 9.2 row 12 |
| R01-112 | Gap 9 East-Asian-ambiguous glyphs | R | 9.4 row 25 |
| R01-113 | Gap 10 which +1 is which | R | 9.4 row 27 |
| R01-114 | Gap 11 injection / long-identifiers fixtures | R | 9.4 row 28 |
| R01-115 | Gap 12 real --questions/--run screens; 5-cell ids | R | 9.4 row 28 |
| R01-116 | Gap 13 hard-wrap path has no marker | R | 9.2 row 10 |
| R01-117 | Stale RR 37-41/60-61 design reference | R | 4.3b |
| R01-118 | Stale RR 20 | R | 4.3b |
| R01-119 | Stale RR 33 (flags column) | R | 4.3b |
| R01-120 | FINDINGS M-10 misattribution / M-06 153 | R | 4.3a |
| R01-121 | FINDINGS claims checked [CODE-VERIFIED] list | R | 2.4 ("FIND citations all resolved"), 2.1 |
| R01-122 | Other FINDINGS quotes of RR lines re-read and match | R | 2.4 |
| R01-123 | Summary | R | 2.8 |
| R01-124 | test_terminal.py:47-51 pins SGR 31; color_system itself unpinned | R | 8 step 1.6(d) |
| R01-125 | 16-colour roles must use named ANSI colours, not downgraded hex | R | 3.2, 6.3 D1 |

## Batch 2: research/02-live-screen-commands-export.md (77 findings)

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R02-01 | Table of the 5 output paths (live, one-shot width, one-shot, e export, snapshot) | R | 2.2 |
| R02-02 | Rich 15.0.0; scoped file line counts | R | 2.2, 2.5 |
| R02-03 | force_terminal/legacy_windows/_environ never passed; Rich autodetects is_terminal (TTY_COMPATIBLE, FORCE_COLOR) | R | 2.2, 5.2.3 |
| R02-04 | color_system literal "standard" unless NO_COLOR gives None | R | 2.1 |
| R02-05 | `--width` feeds `_policy_maker` (`options.width or columns`) and also applies to the interactive path | X | OM-7 |
| R02-06 | Interactive loop calls make_policy every draw; resize seen within REDRAW_SECONDS | R | 2.2 |
| R02-07 | No other output path exists (grep of print/echo/write) | R | 2.2 ("Only two paths use Rich"), 3.7 |
| R02-08 | Paths takeaways (two Rich paths, one factory) | R | 2.2 |
| R02-09 | export_text signature, clear=True empties buffer, styles drop | R | 2.2 (call-order caveat) |
| R02-10 | export_text(styles=True) ignores NO_COLOR and down-conversion (probe table) | R | 2.2 |
| R02-11 | Stream holds ANSI although is_terminal False (`_render_buffer`) | R | 2.1, 5.3.3 |
| R02-12 | Three routes to styled one-shot text (getvalue, styles=True guarded, export_html/svg) | R | 5.3, 7.2 Q5 |
| R02-13 | Today nothing is styled; tests pin `"\x1b" not in out` | R | 2.3, 8 step 1.5 |
| R02-14 | Q5 gate list (i)-(iv) and tests to change/keep | R | 7.2 Q5 |
| R02-15 | LiveScreen: Live creation, shape tuple, rebuild | R | 2.2 |
| R02-16 | Alt screen only on a terminal; no mouse/blink codes | R | 2.2 |
| R02-17 | auto_refresh False; redraw on dirty or every 0.5 s | R | 2.2 |
| R02-18 | Resize by polling; no SIGWINCH handler | R | 2.2 |
| R02-19 | Styles survive Live | R | 2.2, 5.3.6 |
| R02-20 | Failure and exit: `observe: display failed: ...` to stderr, exit 1; finally stops collector and closes screen; q / Ctrl-C end loop | X | OM-8 |
| R02-21 | `_on_tstp` SIGSTOP after restoring tty; `_on_cont` re-enters cbreak and sets redraw flag | X | OM-8 |
| R02-22 | Shape tuple must cover every style-affecting policy field | R | 8 step 1.5, 6.3 D2 |
| R02-23 | Gate constants QUESTION_GATE_PASSED / QUESTION_LINK_PASSED with comments, `# fmt: skip` | R | 2.2 |
| R02-24 | `_questions_on`, `_link_on`, `_question_refusal` (exit 1 gate text, exit 2 fixture/missing run), refusal before any Orca call | X | OM-8 (`_link_on` alone is in 2.2) |
| R02-25 | Other constants: READ_TIMEOUT 0.1, MAX_TIMEOUT 0.25, WIDTHS, refusal texts; collector INTERVAL/CYCLE_BUDGET/MAX_BACKOFF/JOIN_TIMEOUT/QUESTION_PAGE_CAP; RETENTION_BOUND 1000, WINDOW_ROWS 100; PAYLOAD_CAP 64 KiB | X | OM-8 (only REDRAW_SECONDS, ASK_CAP and the 1,000 bound appear) |
| R02-26 | Pinned-regex tests over commands.py text (two gate lines, release-gates.md, Task 18) | R | 2.2, 3.6 SC-16 |
| R02-27 | Styled change must keep both gate lines byte-identical in shape | R | 3.6 SC-16, 8 step 1.5 |
| R02-28 | Gate takeaways (both True; `_link_on` is the only switch) | R | 2.2 |
| R02-29 | export.py imports no Rich | R | 2.2 |
| R02-30 | record_text structure (header1.. ledger rows, question lines, sanitize) | R | 2.2 |
| R02-31 | `_question_lines` suffix ` | dispatchId=.. | link=..` | R | 2.2 |
| R02-32 | q.text (subject based) vs screen_text/ask/shown (screen only) | R | 2.1, 2.2 |
| R02-33 | Five-point proof that question text is never written (writers, record, snapshot, rows, tests) | R | 2.2 |
| R02-34 | Anomaly: `--once --width` stdout carries question text (screen, not record) | R | 2.2, 3.7 |
| R02-35 | Snapshot contract: SCHEMA_VERSION 1, pinned by schema tests | R | 2.2 |
| R02-36 | File mechanics: state_dir (XDG_STATE_HOME), record/snapshot names, write_atomic 0700 + mkstemp + fsync + os.replace, json.dumps indent=2 sort_keys | X | OM-9 |
| R02-37 | Export takeaways | R | 2.2, 3.7 |
| R02-38 | Collector init: `_questions`/`_link` flags, initial CycleResult states | R (decl) | 4.5 row "Collector, parse and key-map internals" |
| R02-39 | Callers pass questions/link; tests pin both paths | R (decl) | 4.5 |
| R02-40 | Per-cycle question read within budget; failure states; FixtureSource no-question-fixture | R (decl) | 4.5 |
| R02-41 | parse_questions link states, ask sanitize and cap 400, sender check | R (decl) | 4.5; ASK_CAP also in 2.2 |
| R02-42 | Retention merge keyed (Run, id), bound 1,000, `_carry` on failed read | R (decl) | 4.5 |
| R02-43 | View reads result.questions; `_questions_panel`, `_desk` build lines | R | 2.2 data-flow line |
| R02-44 | Decision Desk join by exact dispatch_id; field list; unlinked notes; DESK_EVICTED; DESK_NO_TEXT; desk None unless link_on and selected | R (decl) | 4.5 |
| R02-45 | Flow takeaways (Options.questions -> gate -> Collector -> parse -> view) | R | 2.2 |
| R02-46 | KeySource decodes only enter/backspace/ctrl_c/up/down/escape/text; mouse reports consumed | R (decl) | 4.5 ("key-map internals"); no-mouse fact in 2.2 |
| R02-47 | apply_key full key map | R (decl) | 4.5; AD-5 in 1.3 |
| R02-48 | What changes the display; Effect NONE/EXPORT/QUIT; no key reaches Orca | R (decl) | 4.5; 3.7 Read-only row |
| R02-49 | Help text strings KEYS_LINE etc. at view.py:79, :105 | R (decl) | 4.5; 9.4 row 35 |
| R02-50 | Key takeaways (n/p/escape for desk; handling independent of rendering) | R (decl) | 4.5 |
| R02-51 | Five places a styled change touches | R | 5.6 implications, 8 steps 1.3, 1.5, 1.1, 1.6 |
| R02-52 | Five must-stay-byte-identical items | R | 3.7, 8.9 |
| R02-53 | Change-surface takeaways | R | 5.6 |
| R02-54 | Gap: FINDINGS/RR not read by this agent; task line refs checked | D | meta note; the doc claims are covered by research 04 content in 1.3 and 2.4 |
| R02-55 | Mouse/blink grep; future style must not add blink SGR | R | 3.7, 8.9 #10 |
| R02-56 | view.py help-string line numbers unverified | R | 9.4 row 35 |
| R02-57 | Open: styles=True vs getvalue route is a design decision | R | 9.2 row 8 |
| R02-58 | Open: may a piped `--once --width` carry ANSI | R | 8.2 D-4, 9.2 row 8 |
| R02-59 | Open: Windows legacy_windows; interactive refuses win32 | R | 9.4 row 36 |
| R02-60 | Not covered: render.py row/column styling points | D | covered by R01 findings (2.4 map) |
| R02-61 | Stale docs: none found; comments checked against code | D | no finding to carry |
| R02-62 | commands.py:63-66 owner-record file not opened | R | 9.4 row 35 |
| R02-63 | Summary | R | 2.8 |
| R02-64 | Addendum intro: section 9 added after Phase 3 gate | R | 9.5 C2 |
| R02-65 | 7-hop trace of the live path | R | 2.2 |
| R02-66 | Measurement 1: 5-line group, 10x3 console, exact bytes | R | 2.2 |
| R02-67 | Measurement 2: same group at height 5 fits, all five lines | D | subsumed by measurement 3 (2.2 crop at 38 vs 40) |
| R02-68 | Measurement 3: real 80-col screen at height 38 loses last two lines, no ellipsis | R | 2.2 |
| R02-69 | Measurement 4: non-terminal console writes nothing; plain print never crops | R | 2.2, 5.3.7 |
| R02-70 | Capture routes A, B, C and limits | R | 2.2, 9.2 row 11 |
| R02-71 | No test references LiveScreen/run_interactive | R | 2.2, 2.3 |
| R02-72 | Styles reach the live terminal as SGR (measured) | R | 2.2 |
| R02-73 | Height is a hard silent cut; uncounted rows lose the footer first | R | 3.5, 8.3 |
| R02-74 | Inspector body `max(...,1)` (render.py:491) can overflow height | X | OM-1 |
| R02-75 | Frame-heavy design must count rows, assert heights 24/40/44/8, each frame row costs a ledger row | R | 3.5, 8 step 0.7 |
| R02-76 | Width safe on live path: no_wrap crop plus Screen padding | R | 5.1.5, 5.3.5 |
| R02-77 | Section 9 takeaways | R | 2.2, 5.3 |

## Batch 3: research/03-tests-goldens-fixtures.md (148 findings)

Section 1 (test_render.py assertions, 36 rows then R3 block). Test classes that the report covers only at class level (flat-text tolerant checks) are marked R because the class-level substance (whole-line and `startswith` checks break under frames; flat checks tolerate them) is in 3.6 step 3.6, 4.7, 5.5, 6.5.

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R03-01 | every_line_fits_the_width (cell_len <= width at 160/116/80) | R | 3.6 SC-1 |
| R03-02 | matrix test: lines fit, `len(lines)<=30`, `^\d+/\d+ shown`, collected N / reported N | R | 8 steps 2.7, 6.5 |
| R03-03 | long_identifiers_truncate_with_a_marker (`>` marker, full id not in list); also test_export an_id_truncated_on_screen (needs `>` at 80) | X | OM-10 |
| R03-04 | inspector shows full wrapped identifier (`dispatchId:` / two-space continuation) | R | 8 step 3.6 |
| R03-05 | worker text with markup renders literally | R | 3.6 SC-18 |
| R03-06 | injection: no ESC/C1/format chars in NO_COLOR output | R | SC-18 |
| R03-07 | no blink SGR 5/6 | R | SC-4 |
| R03-08 | counts strip tokens intact; `Human questions` above ledger_title | R | SC-8, 8 step 6.3 |
| R03-09 | PARTIAL literal never truncated at 80 | R | SC-8 |
| R03-10 | below 80 narrow diagnostic with counts and gap notice | R | 3.3 narrow row |
| R03-11 | too-small terminal diagnostic; `GAP_NOTICE in lines` exact | R | 2.3 pins |
| R03-12 | rendering twice byte-identical; colour vs NO_COLOR printed equal | R | SC-5, 8 step 1.6(a) |
| R03-13 | ASCII mode renders only ASCII | R | SC-3 |
| R03-14 | full width table header test (eight column names, no stage column) | R | 8 step 6.5 |
| R03-15 | line and short forms order kind < id < verdict; 80 has no liveness | R | 8 step 2.7 |
| R03-16 | marks, flags, overflow, empty text exact lines | R | 8 step 6.5 |
| R03-17 | changed rows ` *` and filter/baseline notes startswith | R | 8 step 6.5 |
| R03-18 | selection placeholder and `"/ab" in lines` | R | 2.3 pins |
| R03-19 | render returns one renderable per line; source regex on render.py | R | 2.3 |
| R03-20 | t19 questions panel flat phrases, 5 `reason unknown` lines | R | 8 step 4.7 |
| R03-21 | every_screen_line_fits with panel at 3 heights x 3 widths | R | SC-1, SC-9 |
| R03-22 | long question list windowed `questions shown ... of 60` | R | 2.3, 8 step 4.7 |
| R03-23 | t47 questions-off screen is the release 1 screen | R | 2.3 |
| R03-24 | pending screen / fenced state whole-line GAP_NOTICE | R | 2.3 pins |
| R03-25 | t12 / empty good read (flat-based, border tolerant) | R | 3.6 step 3.6 (flat vs whole-line) |
| R03-26 | window_full text exact line at 100 rows | R | 2.3, step 3.6 |
| R03-27 | t49 too-small, inspector, ASCII non-ASCII subject, panel twice | R | 2.3 |
| R03-28 | t47 golden byte-identical test (:611) | R | 2.3 |
| R03-29 | decision_1: two-space separator after age pins question line | R | 8 step 4.5 |
| R03-30 | decision_2: 8 `reason unknown` at height 26 with 30 workers (vertical budget) | R | 8 step 3.6 |
| R03-31 | decision_3_and_4: flat count phrases | R | 8 step 4.7 |
| R03-32 | f04: line containing `[no longer in source window]` once at 3 widths; layout must keep state word before subject | X | OM-10 |
| R03-33 | f07: header2 strings are view-model; header redesign must keep view.header2 or change test | R | 8.9 #3, 8 step 2.5 (header1 not edited) |
| R03-34 | f08: 80-col key line in last 3-4 lines; no line ending `>` containing `exp` | R | SC-11 |
| R03-35 | f01: gap_notice view text | R | 2.3 (view-model strings), SC-8 |
| R03-36 | f17_f15 / f39 / latest-empty text-only checks | R | 8 step 4.7 |
| R03-37 | R3: selected glyph row and desk follows (:891) | R | 8 step 5.5 |
| R03-38 | R3: each unlinked reason shows in desk (:919) | R | 5.5 |
| R03-39 | R3: linked question lines keep age, state, reason unknown (:930) | R | 2.3, 5.5 |
| R03-40 | R3: desk text bounded to four lines at 80 (:943, :958) | R | 2.3, 5.5 |
| R03-41 | R3: hostile text inert (:970) | R | SC-18 |
| R03-42 | R3: NO_COLOR has no ESC (:985) | R | SC-2 |
| R03-43 | R3: desk gives way by height at 116 (:990) | R | 5.5 |
| R03-44 | R3: selection beyond window (:1009) | R | 5.5 |
| R03-45 | R3: help_line == QUESTIONS_LINK_KEYS_LINE and `n/p question` (:1017) | R | 2.3 (KEYS_LITERAL), RB-20 |
| R03-46 | conftest helper inventory (FakeClock, make_rows, make_envelope, console_factory, QRUN, question_payload, make_question_rows, make_question_error, routed_runner_responses) and autouse `_subprocess_guard` blocking subprocess.Popen/run | X | OM-11 |
| R03-47 | test_render local helpers policy_for, fixture_view, generated_view, printed, bad_chars, r3_rows, r3_screen | R | 8 step 1.6(b) (printed audit), 0.6 |
| R03-48 | Takeaway: whole-line equality and startswith break under frames; flat checks tolerate | R | 8 step 3.6 |
| R03-49 | Takeaway: test_render.py:399 one renderable per line | R | 2.3 |
| R03-50 | Takeaway: render.py source grep tokens | R | 2.3 |

Section 2 (per-module table and inventory).

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R03-51 | 28 .py files = 22 test modules + 6 support, 2 goldens | R | 2.3 |
| R03-52 | Only 10 files touch screen text; LiveScreen untested; FakeScreen records only | R | 2.3, 2.2 |
| R03-53 | test_render.py row (54 tests, 1022 lines, layers pinned) | R | 2.3 |
| R03-54 | test_terminal.py row (NO_COLOR gating, width classes, too_small, glyph table, console options, clip, source scan) | R | 2.3 (source scan), 8 step 1.6(d) |
| R03-55 | test_commands.py row (`--once` record, `--once --width`, ascii, argv, loop tests, guards) | R | 2.2, 8 step 3.6 |
| R03-56 | test_view.py row (60 defs, view model only) | R | 2.3 last bullet, 9.4 row 31 |
| R03-57 | test_export.py row (record, no ESC, question line suffix, source scan, truncated-id test) | R | 2.3 (source scan), 2.2 |
| R03-58 | test_snapshot_schema.py row (schema, no forbidden keys, link-on == link-off, no question text) | R | 3.6 SC-7 |
| R03-59 | test_golden_contract.py row (four redacted fixtures, collected 100 / reported 428) | R | 8 step 6.5, 2.3 |
| R03-60 | test_linkoff_screen_reference.py row | R | 2.3 |
| R03-61 | test_inspector_scroll.py row (imports fixture_view/policy_for from test_render) | R | 2.3, 8 step 2.7 |
| R03-62 | test_question_cap.py row | R | 8 step 3.6 |
| R03-63 | test_fixtures.py row (console_factory fixture) | R | 2.3 module list |
| R03-64 | Presentation-blind modules and the real-pty test_keys_spike | R | 2.3, 9.4 row 31 |
| R03-65 | Counts are `grep -c "^def test_"`; parametrisation multiplies | R | 9.5 C7 |
| R03-66 | Takeaway: presentation-sensitive modules list | R | 2.3 |
| R03-67 | Takeaway: 766 tests can pass and the Live screen still look wrong | R | 1.2, 2.2 |
| R03-68 | test_keys_spike.py drives real Live on a pty but not the observer screen | R | 2.2 (spike_child.py:64) |

Section 3 (colour vs NO_COLOR printed-bytes tests).

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R03-69 | render() unstyled, so colour and NO_COLOR bytes identical; goldens hold no ESC | R | 2.3 |
| R03-70 | test_render.py:250-259 must be rewritten (strip SGR) not deleted | R | 3.6 SC-5, 8 step 1.6(a) |
| R03-71 | injection test: NO_COLOR scan keeps meaning; colour print must never be bad_chars-scanned | R | 8 step 1.6(b) |
| R03-72 | no-blink test is the guard for a style phase | R | SC-4 |
| R03-73 | :970-987 NO_COLOR no ESC valid under styling | R | SC-2 |
| R03-74 | test_terminal.py:40-51 pins the console contract | R | 8 step 1.6(d) |
| R03-75 | test_commands.py:99/105/121 hold while `--once` keeps export_text() | R | 8 step 1.5, 7.2 Q5 |
| R03-76 | golden printed_* 15 values change, 30 lines_* stay | R | 2.3 |
| R03-77 | Takeaway: exactly one test asserts colour printed == NO_COLOR | R | 2.3 |
| R03-78 | Takeaway: export_text() without styles keeps `--once --width` ESC-free | R | 2.2, 7.2 Q5 |

Section 4 (goldens).

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R03-79 | 4a producer surface() release1_surface.py:41-62, VARIANTS, runs | R | 2.3 |
| R03-80 | 14 keys per variant | R | 2.3 |
| R03-81 | Policy resolve_policy colour allowed, not ASCII | R | 2.3 (printed_* colour on) |
| R03-82 | Pinning T47 and companions (:487-491, test_view.py:947) | R | 2.3 |
| R03-83 | Docstring claim `git archive 9e2608b03`; commit exists | R | 2.3 |
| R03-84 | Serialisation json.dumps(indent=1, sort_keys, ensure_ascii=False), no trailing newline | R | 2.3, 8 step 2.1 |
| R03-85 | Git history cd8736199; c69ce4b3a stale | R | 2.3, 4.3b |
| R03-86 | Regeneration command shape for release-1 golden (not run) and meaning change | R | 8 step 2.7, 9.4 row 32 |
| R03-87 | release1_surface.py imports only release-1 names (Collector, FixtureSource, record_text, snapshot_json, render, screen_lines, make_console, resolve_policy, Session, build_view, FakeClock); a rename breaks recorder and test | X | OM-12 |
| R03-88 | 4b producer capture(), scenarios five/long_subject, 4 workers, link off | R | 2.3 |
| R03-89 | Pinning T64 and KEYS_LITERAL 107 chars | R | 2.3 |
| R03-90 | No recorder for link-off golden; serialisation | R | 2.3 |
| R03-91 | Link-off regeneration one-liner | R | 8 step 2.7 |
| R03-92 | record_golden.py: live Orca CLI, 3 worker-list calls, exit code 3, never run | R | 2.3 ("redacted fixtures"), 9.4 row 32 |
| R03-93 | record_golden_questions.py: no Orca call, evidence files, writes golden-question-*.json and question-cap-100.json | R | 2.3 |
| R03-94 | In-memory experiment reproduces both goldens byte for byte | R | 2.3 |
| R03-95 | 4d gate regex tests pin commands.py source | R | 2.2 |
| R03-96 | Gate test line ranges 747-760 and 762-777 | R | 4.3a ("747-756, 762-772") |
| R03-97 | Guards monkeypatched in many tests; with guard False questions refused with `question read not enabled: QUESTION-OBSERVATION has not passed` | X | OM-8 |
| R03-98 | Takeaway: which keys change per change type (style-only, text, view string) | R | 2.3 golden table |
| R03-99 | No recorder for link-off golden; derived command unverified | R | 9.4 row 32 |

Section 5 (helpers, fixtures, 64-hex).

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R03-100 | make_question_rows/question_payload carry text; ASK_CAP 400 at parse.py:495-505; link needs dispatchId and from_handle | R | 2.2 (ASK_CAP, link), 0.6 |
| R03-101 | r3_rows, r3_screen, DESK constants; test_view r3 helpers | R | 8 step 0.6 |
| R03-102 | Existing tests exercising the 80-col desk (5 listed) | R | 2.3, 8 step 5.5 |
| R03-103 | No fixture has 64-hex token or long path; no path in session_fields | R | 2.3 |
| R03-104 | Measured at 160: hash alone on line 2 | R | 2.3 Q7 |
| R03-105 | Measured at 116 | R | 2.3 Q7 |
| R03-106 | Measured at 80 | R | 2.3 Q7 |
| R03-107 | List line cut with `...` before the hash | R | 2.3 Q7 |
| R03-108 | Token longer than width hard-split at width, no marker, mid-word | R | 2.3 Q7 |
| R03-109 | Hash fits at 80; frames narrow the text width; paths cut earlier | R | 7.2 Q7 |
| R03-110 | Proposed location and test name | R | 8 step 0.6 |
| R03-111 | Proposed assertions (cell_len, hash whole, nothing lost) | R | 8 step 0.6 |
| R03-112 | Screen-only canary | R | 8 step 0.6 |
| R03-113 | Variant: 120-character resource.worktreeId | R | 8 step 0.6 |
| R03-114 | Takeaway: add the test before the layout phase | R | 7.1 P0, 7.2 Q7 |
| R03-115 | Takeaway: decide path-aware breaking | R | 9.2 row 10 |
| R03-116 | 16 spare cells at 80; wraps cleanly while text width >= 64 | R | 7.2 Q7 |

Section 6 (phase grouping), Section 7 (baseline).

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R03-117 | Rule 1: screen_lines stays plain source; Rich Panel/Table as last step | R | 6.1, 8.8 |
| R03-118 | Rule 2: forbidden tokens in render.py/terminal-only literals; theme reads policy only | R | 8.9 #6, step 1.2 |
| R03-119 | Rule 3: boxes need explicit ASCII choice (corrected) | R | 9.5 C1 |
| R03-120 | Rule 4: each phase updates tests and goldens in same commit | R | 7.2 Q2 |
| R03-121 | Phase P0 (tests only) | R | 3.8, 8 Phase 0 |
| R03-122 | Phase P1 style-only (1 test, 15 values) | R | 3.8, 8 Phase 1 |
| R03-123 | Phase P2 text-only | R | 3.8, 8 Phase 2 |
| R03-124 | Phase P3 width-gated 160 layout | R | 7.1 note on ordering by width |
| R03-125 | Phase P4 boxed panes | R | 8 Phase 3 |
| R03-126 | Phase P5 optional Rich renderables | R | 6.1 B, 8.8 |
| R03-127 | Ordering note P1/P2 independent, P3 before P4, P0 first | R | 7.1 |
| R03-128 | Checklist: plain-text equality/startswith tests | R | 8 step 3.6 |
| R03-129 | Checklist: vertical budget tests | R | 8 steps 3.6, 5.5 |
| R03-130 | Checklist: byte pins | R | 2.3 |
| R03-131 | Takeaway: smallest safe sequence | R | 7.1 |
| R03-132 | Takeaway: style-only leaves link-off golden and lines_* unchanged | R | 2.3, 8 Phase 1 |
| R03-133 | Takeaway: each golden-changing phase needs an owner re-baseline decision | R | 9.2 row 5 |
| R03-134 | Baseline `uv run pytest tests/observe/ -q -p no:cacheprovider` = 766 passed in 25.70 s; no tracked file changed | R | 2.3 |

Gaps, stale docs, summary.

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| R03-135 | Gap: PYTHONPATH layout unverified | R | 9.4 row 32 |
| R03-136 | Gap: ten modules classified from docstrings | R | 9.4 row 31 |
| R03-137 | Gap: test_view.py not read assertion by assertion | R | 9.4 row 31 |
| R03-138 | Gap: owner decision on re-baselining T47 | R | 9.2 row 5 |
| R03-139 | Gap: box-drawing in `--once --width` output | R | 8.2 D-9 |
| R03-140 | Gap: real LiveScreen has no test | R | 9.2 row 11 |
| R03-141 | Gap: no test runs wide chars, hash or long path through session_fields | R | 8 step 0.6 |
| R03-142 | Gap: record_golden*.py are not the generators | R | 9.4 row 32 |
| R03-143 | Gap: pr-591-comment consideration 8 premise (no frame yet) | R | 9.4 row 26 |
| R03-144 | Stale: c69ce4b3a and test line shift | R | 4.3b |
| R03-145 | Stale: 05-observe-built-state QUESTION_GATE_PASSED False | R | 4.3b |
| R03-146 | Stale: design-docs-and-gates.md:46 line shift | R | 4.3b |
| R03-147 | pr-591-comment claims and counts verified | R | 9.4 row 26 |
| R03-148 | Summary | R | 2.8, 7.2 |

## Batch 4: research/web-01-rich-composition-and-colour.md (50 findings)

| ID | Finding | Status | Report anchor / note |
|---|---|---|---|
| W01-01 | Executor summary 1: screen_lines plain list[str], render unstyled Text | D | restates R01-17/R01-18 (report 2.1) |
| W01-02 | Executor summary 2: make_console colour None if NO_COLOR else standard | D | restates R01-07 |
| W01-03 | Executor summary 3: Rich 15.0.0, Panel identical borders, box.ASCII needed | D | restates R01-08 |
| W01-04 | Executor summary 4: export_text() default styles=False; styles=True ignores NO_COLOR | D | restates R02-09/R02-10 |
| W01-05 | Executor summary 5: Live screen=True alt screen, padded rows, silent crop | D | restates R02-65..R02-69 |
| W01-06 | Executor summary 6: tests require one renderable per line; forbid Console( and sorted( | D | restates R03-49/R03-50 |
| W01-07 | Executor summary 7: 16-colour downgrade maps muted/green/red/violet to 7, slate to 8 | D | restates the 04 table (report 2.1) |
| W01-08 | A: color_system values None/auto/standard/256/truecolor/windows | R | 5.2.1 |
| W01-09 | A: auto detection (COLORTERM, last part of TERM, notebook, dumb) | R | 5.2.2 |
| W01-10 | A: is_terminal order (force_terminal, IDLE, notebook, TTY_COMPATIBLE, FORCE_COLOR, isatty) | R | 5.2.3 |
| W01-11 | B: TERM=dumb/unknown; FORCE_COLOR; NO_COLOR beats FORCE_COLOR | R | 5.2.4 |
| W01-12 | B: Rich NO_COLOR keeps bold/dim; project color_system=None is stricter | R | 5.2.5, 9.2 row 7 |
| W01-13 | B: Style.render with None returns text; without_color keeps bold/dim; dim is SGR 2 | R | 5.2.5 |
| W01-14 | C: export_text(clear, styles) needs record=True | R | 5.3.1 |
| W01-15 | C: source behaviour; recorded segments keep original styles; capture the written stream | R | 5.3.2, 5.3.3 |
| W01-16 | C: export_html / export_svg params; not for NO_COLOR test | R | 5.3.4 |
| W01-17 | D: screen=True docs; vertical_overflow ellipsis/crop/visible | R | 5.3.5 |
| W01-18 | D: live.py transient, home-cursor control, stop sets visible | R | 2.2 hop table, 5.3.5 |
| W01-19 | D: screen.py set_shape crops rows and pads; discrepancy vs docs ellipsis | R | 5.3.5 |
| W01-20 | D: styles survive Live; padded cells use console style | R | 5.3.6 |
| W01-21 | E: cell_len table-based; wide 2, combining 0, ambiguous 1, ASCII fast path, cache under 512 | R | 5.1.6, 9.4 row 25 |
| W01-22 | E: ZWJ makes next code point skipped; VS16 can add one cell after certain narrow-to-wide characters | X | OM-13 |
| W01-23 | E: widths 160/116/80 measured by cells; pad with cell_len not len | R | 5.1.6 |
| W01-24 | F: Text.truncate modes fold/crop/ellipsis/ignore; Text.wrap long word | R | 5.1.5 |
| W01-25 | F: Span exclusive end; append/stylize/assemble; later span wins | R | 5.1.1 |
| W01-26 | F: Text.from_ansi parses ANSI strings | X | OM-13 |
| W01-27 | G: Safe Box is legacy Windows only; Panel defaults ROUNDED, expand, border_style | R | 5.1.3 |
| W01-28 | G: ASCII/ASCII2/HEAVY not listed in fetched docs; confirm dir(rich.box) | R | 5.1.4 |
| W01-29 | G2: truecolor to 256 arithmetic, grey ramp | R | 5.2.6 |
| W01-30 | G2: truecolor to standard palette match; first 16 colours terminal-theme dependent | R | 5.2.6 |
| W01-31 | G2: Layout/Columns/Table/Panel measure with cell_len but replace one-Text-per-line | R | 5.1.2 |
| W01-32 | H: not a documented pattern; derived options | R | 5.1.7 |
| W01-33 | H: Text plus Span separation keeps plain string identical | R | 5.1.1, 5.1.7 |
| W01-34 | H: records and one-shot plain use Text.plain | R | 5.1.7 |
| W01-35 | Key external 1-9: content/style separation | R | 5.6 Q1 |
| W01-36 | Key external: color_system values/auto | R | 5.6 Q4 |
| W01-37 | Key external: NO_COLOR bold/dim; NO_COLOR beats FORCE_COLOR | R | 5.6 Q4 |
| W01-38 | Key external: export_text(styles) | R | 5.6 Q5 |
| W01-39 | Key external: Live screen=True pad/crop, no ellipsis | R | 5.6 Q5/Q7 |
| W01-40 | Key external: Text crop/ellipsis/fold on long token | R | 5.6 Q7 |
| W01-41 | Key external: cell_len table-based | R | 5.6 Q1/Q7 |
| W01-42 | Key external: downgrade arithmetic, roles collapse | R | 5.6 Q4 |
| W01-43 | Key external: Panel default box ROUNDED, expand, safe_box | R | 5.1.3 |
| W01-44 | Recommendation Q1 composition (line model plus thin style layer) | R | 6.1, 7.1 |
| W01-45 | Recommendation Q4 colour depth (auto cheap; named ANSI floor; NO_COLOR choice) | R | 6.3, 7.1 |
| W01-46 | Recommendation Q5 capture gate (stream capture, SGR assertions) | R | 7.2 Q5 |
| W01-47 | Recommendation Q7 long token (ellipsis; cell_len; own overflow row) | R | 5.1.5, 3.5 |
| W01-48 | Discrepancy notes 1 and 2 (Live ellipsis; NO_COLOR bold) | R | 5.3.5, 5.2.5 |
| W01-49 | Not found: line-model-plus-styles pattern; guidance for muted roles at 16 colours | R | 5.1.7, 5.2.7 |
| W01-50 | Status/date/topic header of web-01 | D | covered by report 10 Evidence Trail |

## Batch 5: synthesis files (668 findings by line)

Method: every non-blank, non-separator, non-code-fence line of each synthesis file was tested for a byte-exact copy in the report (`grep -Fx`). Result below. The 24 lines that are not byte-exact were read against the report and are listed with their classification.

| Synthesis file | Findings (lines) | Byte-exact in report | Edited or absent |
|---|---|---|---|
| synthesis/synth-01-problem-current-state.md | 319 | 310 | 9 |
| synthesis/synth-02-target-gaps.md | 227 | 214 | 13 |
| synthesis/synth-03-external-findings.md | 122 | 120 | 2 |
| Total | 668 | 644 | 24 |

Classification of the 24 non-exact lines.

| ID | Synthesis line | Status | Report anchor / note |
|---|---|---|---|
| S01-a | synth-01 title/"Feeds report Sections 1 and 2" line defining OBS, RR and FIND with their paths and the relative-path convention | X | OM-15 (OBS is defined at report 2 intro and RR at 8 intro; the `FIND` path `.dev/issues/409/visual-parity/merged/FINDINGS.md` appears nowhere, yet `FIND` is used from 1.3 on) |
| S01-b | synth-01 `_columns` row (line/short counts) | R | 2.1 row now adds "`line` 6 and `short` 5, all counting the 2-cell marker column" |
| S01-c | synth-01 Q7 bullet "synthetic 222-character plan ask ... desk text 2/3/3 lines" | R | 2.3 Q7 fixture bullets (fixture text and re-measured 157/64, 85/71/64, 78/78/64 cells) |
| S01-d | synth-01 Q7 bullet "Desk lines at 80 columns 78, 78, 64 ... `_desk_lines` produced 4 lines" | R | 2.3: 78/78/64 kept; the 4-line claim is withdrawn in the report with the reason (replacement, not a drop) |
| S01-e | synth-01 amber role row | R | 2.4 (amber row now says desk question text amber, list question text base bold) |
| S01-f | synth-01 ledger 160 row (12-column) | R | 2.4 (corrected to 11-column, marker + 10 named columns) |
| S01-g | synth-01 ledger 116 row (4-column) | R | 2.4 (corrected to 6-column with names) |
| S01-h | synth-01 ledger 80 row (3-column) | R | 2.4 (corrected to 5-column with names) |
| S01-i | synth-01 title line "Synthesis 01: Problem Statement and Current State Analysis" | D | report title and section 1/2 headings |
| S02-a | synth-02 title line | D | report title and section 3/4 headings |
| S02-b | synth-02 "Research question" line | D | report 1.1 |
| S02-c | synth-02 "Inputs weighed" line | D | report header ("Research files: 5 codebase + 2 web") and Section 10 |
| S02-d | synth-02 "Conventions used below" heading | D | no content of its own |
| S02-e | synth-02 convention bullet defining `render.py`, `view.py`, `terminal.py`, `commands.py`, `export.py`, `RR`, `FIND` and the mockup path | X | OM-15 |
| S02-f | synth-02 tag legend bullet ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED], [STALE DOC]; doc-only claims never stated as current state) | R | 2 intro ("All claims are [CODE-VERIFIED] unless tagged otherwise"), 9 intro (UNVERIFIED and CODE-CONTRADICTED defined); `[STALE DOC]` and the doc-only rule are used but not defined |
| S02-g | synth-02 bullet "Web findings are marked [external context]" | R | 5 intro ("All findings in this section are EXTERNAL CONTEXT") |
| S02-h | synth-02 severity-scale bullet: Critical = FINDINGS "High" or a C8 defect (spec-required behaviour not wired); Important = FINDINGS "Medium", a gating decision, or a Gate 1 "Important" gap; Minor = FINDINGS "Low" or a note; Gate 1 found 0 Critical research gaps | X | OM-14 (4.1 says "Severity follows the scale in the header" but no such scale exists in the report) |
| S02-i | synth-02 amber role row | R | 3.2 (amber row, edited as in S01-e) |
| S02-j | synth-02 SC-6 | R | 3.6 SC-6 (rewritten with the STATE_ROLE table) |
| S02-k | synth-02 SC-14 | R | 3.6 SC-14 (rubric now defined in 8.4) |
| S02-l | synth-02 Live versus one-shot row | R | 4.1b (adds D-4, D-9) |
| S02-m | synth-02 Render harness row | R | 4.1b (adds D-10, rubric in 8.4) |
| S03-a | synth-03 row 5.1.5 | R | 5.1.5 (the "silently clipped today" claim is replaced by the measured correction) |
| S03-b | synth-03 Q7 summary row | R | 5.6 Q7 (same correction) |

Counts for batch 5: 668 findings; 24 non-exact; of those 3 X (S01-a, S02-e, S02-h), 5 D (S01-i, S02-a to S02-d), 16 R; plus 644 byte-exact R. So batch 5 totals: R 660, D 5, X 3.

### Omissions Found

One row per cluster of omitted findings (28 findings in 15 rows). Finding IDs refer to the batches above. Nothing is "COVERED-BY-DEDUP" here: the dedup items are listed in the batches with their surviving item.

| # | Source finding | Source file | Status | If deduped by which report item | Severity |
|---|---|---|---|---|---|
| OM-14 | Severity scale for Section 4 (and 7): Critical = FINDINGS "High" or a C8 defect (spec-required behaviour not wired); Important = FINDINGS "Medium", a decision that gates other rows, or a Gate 1 "Important" gap; Minor = FINDINGS "Low" or a note; Gate 1 found 0 Critical research gaps, so Critical marks product gaps. Report 4.1 says "Severity follows the scale in the header" but the report has no such scale, so every Critical/Important/Minor label in 4.1 and 4.2 has no stated meaning (S02-h, 1 finding) | synthesis/synth-02-target-gaps.md (header conventions) | OMITTED | n/a | IMPORTANT |
| OM-15 | Abbreviation and path conventions: `FIND` = `.dev/issues/409/visual-parity/merged/FINDINGS.md` is never defined (the path appears nowhere in the report, yet `FIND` is used from 1.3); `RR`, `OBS` and the mockup directory are defined only late (2 intro, 8 intro); the relative-path convention of Sections 1-4 is not stated (S01-a, S02-e, 2 findings) | synthesis/synth-01-problem-current-state.md, synth-02-target-gaps.md | OMITTED | n/a | MINOR |
| OM-1 | Inspector screen (render.py:255-287): `INSPECTOR  <dispatchId>` title, wrapped `label: value` with two-cell continuation, scroll window with above/below lines counted in the budget, result sliced `lines[:max(budget,1)]` as the only explicit height clamp in render.py, footer `INSPECTOR_HELP`; and the forced `max(...,1)` inspector body (render.py:491) that can overflow the console height (R01-39, R02-74, 2 findings) | research/01 section 4.4; research/02 section 9.4 | OMITTED | n/a | MINOR |
| OM-2 | `sanitize(text, mode="line"\|"block")`: line turns newlines into spaces, block keeps them, newlines are normalised first; a 64-char unbroken hex token passes sanitize unchanged and is cut only by wrap/clip (R01-13, R01-15, 2 findings) | research/01 section 2 | OMITTED | n/a | MINOR |
| OM-3 | Character versus cell arithmetic in render.py: `_prefix_length` returns a character index (combining and zero-width characters are never joined to their base), `len()` is used for line counts and as character indexes, `cell_len` at the listed lines (R01-26, R01-45, 2 findings) | research/01 sections 4.1, 4.5 | OMITTED | n/a | MINOR |
| OM-4 | Layout details of the ledger and notes: `line` and `short` column widths (kind 18/14, liveness 14, age 7/6, flags 16, id 38 at 80 columns), the header rule is dashed per column (not continuous), and `_notes` joins the filter, historical, duplicates and selection notes with two spaces into one wrapped element (R01-35, R01-37, R01-40, 3 findings) | research/01 sections 4.3, 4.5 | OMITTED | n/a | MINOR |
| OM-5 | Questions-on sizing and screen shape: the third fallback when neither desk nor notice fits (no panel; `gap_notice` plus `; decision desk hidden...`), and the measured facts that the 80-column questions screen footer is 3 lines and that the questions screen has no column heading at 116 or 80 (R01-50x, R01-53x, 2 findings) | research/01 sections 4.7, 4.8 | OMITTED | n/a | MINOR |
| OM-6 | Consumer map in src: `screen_lines` is defined at render.py:390 and called only at render.py:529; `render` is imported only by commands.py:38 (grep over src, scripts, plugins) (R01-65, 1 finding) | research/01 section 6 | OMITTED | n/a | MINOR |
| OM-7 | The `--width` option feeds `_policy_maker` (`options.width or columns`, commands.py:150-161) and so also applies to the interactive screen, not only `--once` (R02-05, 1 finding) | research/02 section 1 | OMITTED | n/a | MINOR |
| OM-8 | commands.py loop and gate behaviour: failure and exit (`observe: display failed: ...` on stderr, exit 1, `finally` stops the collector and closes the screen), `_on_tstp`/`_on_cont` job-control handlers, `_question_refusal` exit codes (1 gate text, 2 fixture or missing run) before any Orca call, the unreported constants (READ_TIMEOUT 0.1, MAX_TIMEOUT 0.25, WIDTHS, refusal texts, collector INTERVAL/CYCLE_BUDGET/MAX_BACKOFF/JOIN_TIMEOUT/QUESTION_PAGE_CAP, RETENTION_BOUND, WINDOW_ROWS, PAYLOAD_CAP) and the gate-False refusal text `question read not enabled: QUESTION-OBSERVATION has not passed` (R02-20, R02-21, R02-24, R02-25, R03-97, 5 findings) | research/02 sections 3, 4; research/03 section 4d | OMITTED | n/a | MINOR |
| OM-9 | Export file mechanics: `state_dir()` under `$XDG_STATE_HOME/superclaude/observe` or `~/.local/state/superclaude/observe`, record name `observe-<generated_at>.txt`, `snapshot.json`, `write_atomic` (directory 0700, mkstemp, fsync, os.replace), snapshot `json.dumps(indent=2, sort_keys=True)` (R02-36, 1 finding) | research/02 section 5 | OMITTED | n/a | MINOR |
| OM-10 | Test pins a layout change must keep: `test_long_identifiers_truncate_with_a_marker_in_lists` (a `>` marker in lists, full id absent) and `test_export.py:130-138` (an id truncated on screen at 80 columns appears in full in the record and needs a `>` on screen); `test_f04` (a `[no longer in source window]` line once, state word before the subject) (R03-03, R03-32, 2 findings) | research/03 section 1 | OMITTED | n/a | MINOR |
| OM-11 | tests/observe conftest inventory: FakeClock, make_rows, make_envelope, console_factory (default width 160, height 40), QRUN, question_payload, make_question_rows, make_question_error, routed_runner_responses, and the autouse `_subprocess_guard` that blocks subprocess.Popen/run (relevant to the planned pexpect live test) (R03-46, 1 finding) | research/03 section 1 | OMITTED | n/a | MINOR |
| OM-12 | `release1_surface.py` imports only names that exist in release 1 (Collector, FixtureSource, record_text, snapshot_json, render, screen_lines, make_console, resolve_policy, Session, build_view, FakeClock); renaming any of them in the redesign breaks the recorder and T47 (R03-87, 1 finding) | research/03 section 4a | OMITTED | n/a | MINOR |
| OM-13 | Rich details: `cell_len` treats ZWJ as skipping the next code point and VS16 as possibly adding one cell; `Text.from_ansi` parses ANSI strings (W01-22, W01-26, 2 findings) | research/web-01 sections E, F | OMITTED | n/a | MINOR |

Declared exclusions (11 findings: R02-38, R02-39, R02-40, R02-41, R02-42, R02-44, R02-46, R02-47, R02-48, R02-49, R02-50): collector, parse and key-map internals. The report names this exclusion with a reason in 4.5 ("Collector, parse and key-map internals (02 sections 6 and 7): no gap, unchanged by presentation work"). They are counted as represented because the drop is not silent; OM-8 covers only the commands.py and constants items that 4.5 does not name.

### Summary

- **Findings enumerated:** 1070 (research/01: 127; research/02: 77; research/03: 148; research/web-01: 50; synthesis: 668 lines, of which 644 byte-exact in the report and 24 edited or absent, each classified)
- **Represented:** 1024 (includes 11 declared exclusions)
- **Covered-by-dedup:** 18 (R01-72; R02-54, R02-60, R02-61, R02-67; W01-01 to W01-07 and W01-50; S01-i, S02-a to S02-d)
- **Omitted:** 28 (grouped in 15 rows: 1 IMPORTANT, 27 MINOR, 0 CRITICAL)
- **Verdict: FAIL (28 omitted findings)**

Reading of the verdict. The report is a faithful, near-verbatim carry of all three synthesis files (644 of 668 lines byte-exact; every edited line is a correction or an update, and the withdrawn "4-line desk" and "silently clipped hash" claims are replaced with the measured result, not dropped), and it carries almost all research detail through Sections 6 to 9 (options, plan steps, rubric, open questions). The one finding worth fixing is OM-14: Section 4 refers to a severity scale "in the header" that the assembly dropped, so the Critical/Important/Minor labels of the gap table are undefined; adding the one-paragraph scale (and the `FIND` path, OM-15) to the Section 4 or report header closes it. The 27 MINOR rows are low-level implementation detail (inspector body, sanitize modes, constants, export file paths, test-helper inventory) that the plan does not depend on; the orchestrator may dismiss them as out of scope or add a short "not carried" note.

**Status:** Complete


