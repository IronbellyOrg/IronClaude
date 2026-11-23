# QA Report - Research-Gate Qualitative (research-depth lens)

**Topic:** Observer visual-parity redesign (issue #606)
**Date:** 2026-11-17
**Phase:** research-gate-qualitative (research-depth lens)
**Fix cycle:** N/A
**Status:** Complete

---

**Scope read in full:** research-notes.md and research files 01 to 05 (web-01 and web-02 do not exist yet, as stated in the prompt; not counted as defects). Fix authorization: false; no research file was modified. No Inherited Structural Verdict was supplied, so this review is standalone.

## Evaluation by question

### Q1 Safest composition approach (styled spans, titled panes, count tile, two columns): ADEQUATE
- 01 section 8.2 weighs seven insertion options with code-derived constraints. I confirmed the hard constraints they rest on: `render()` returns one `Text` per line (render.py:524-531), the test at test_render.py:399 asserts `len(group.renderables) == len(screen_lines(...))`, and `GLYPHS` holds only `selected`, `truncate`, `hrule` (terminal.py:30-34).
- 01's probe that `safe_box=True` does not ASCII-ize a Rich `Panel` is correct. I re-ran it on Rich 15.0.0: both `safe_box` values printed the same `╭─╮│╰╯` panel.
- Width numbers are real: 160 ledger 114+42, 160 desk 76+80, 116 ledger 70+42, 160 bridge 46+74+34 (04 section 4). I re-read `mockups/160/agent-focus-attention-ledger.txt` and the 80-column desk PNG; the geometry matches.
- 01's full table at 160 uses exactly 160 cells. I re-derived it from render.py:159-165: 2 + 22 + 114 + 12 + 10 separators = 160.
- Weakness (minor): 01 section 8.2 item 5 computes "114+1+42 = 157 of 160" with a 1-cell gap, while 04 shows the mockups use a 1-cell margin each side and a 2-cell gap (1+114+2+42+1 = 160). The two files give different slack; the synthesis must use 04's.
- Weakness (see B1): no option was tested against the live path, which crops overflow silently.

### Q2 Tests and goldens per phase: STRONG
- 03 gives a P0 to P5 phase table naming which tests and golden keys change in each phase. I confirmed the baseline: `uv run pytest tests/observe/ -q` gave 766 passed. I confirmed the link-off golden line counts (five 24/24/25, long_subject 22/22/23).
- 03 correctly separates style-only changes (15 `printed_*` values, one test at test_render.py:256) from text and layout changes (all `lines_*`, whole-line tests, both goldens).
- Citations spot-checked: test_render.py:399, test_commands.py:99/105/121, commands.py:67/70/242/257 all hold.

### Q3 Render-to-image harness and reviewer rubric: ADEQUATE (limits honestly stated)
- 05 section 2 environment facts all reproduced: PIL, cairosvg, pyte, playwright, fontTools absent; chromium, chrome, rsvg-convert, convert, magick, inkscape, freeze, termshot, aha, ansi2html absent; no `~/.cache/ms-playwright`; Rich `export_svg`, `export_html`, `export_text` present.
- 05 lists "subagent Read of a PNG works" as UNVERIFIED. As this reviewing agent, I read `mockups/80/decision-desk.png` with the Read tool and it displayed correctly (dark navy background, amber heavy frame, slate rounded frames). The synthesis may treat PNG viewing by a Claude agent as confirmed. What is still untested is whether a rendered SVG or HTML can become a PNG offline.
- No reviewer rubric criteria are drafted in the files. 04 sections 2 and 4 supply the raw material (eight colour roles, pane geometry), which is enough for a synthesis agent to write the rubric. Not a blocking gap.

### Q4 ANSI colour depth: STRONG
- Probed and reproduced: `bold #ff8800` under `standard` gives `\x1b[1;91m`. The eight mockup colours downgrade as 04 states: base 15, slate 8, cyan 14, amber 11, and muted, green, red, violet all 7 (256-colour: 189, 60, 80, 214, 145, 115, 210, 147). The mockups hold no background codes and no dim, italic, underline, reverse or blink attributes: grep for `48;` and for attribute codes 2/3/4/5/7/9 found 0 matches in all nine `.ansi` files.
- Rich's detection is stated from code and probe: `auto` on a non-terminal gives no colour. I confirmed Rich's detection reads `COLORTERM` (console.py:805) and the `FORCE_COLOR` and `TTY_COMPATIBLE` variables (console.py:955-964). 01 says "a real terminal would read COLORTERM/TERM" without citing that code (minor).
- 02 correctly warns that `export_text(styles=True)` ignores NO_COLOR. I reproduced it: `color_system=None, no_color=True` gives a plain stream but `export_text(styles=True)` returns `'\x1b[1;31mhello\x1b[0m\n'`.

### Q5 Live path versus one-shot path styling and the styled-capture gate: INSUFFICIENT (blocking B1)
- The one-shot half is deep: `export_text()` at commands.py:242 drops styles; `getvalue()` keeps them and honours NO_COLOR; a four-point gate is proposed in 02 section 2.
- The live half is asserted from reading ("Live renders through the console's normal pipeline", 02 section 3) and never measured. The issue body requires it: `.dev/issues/606/issue-body.md:58` says the spec states the depth and that "ANSI-styled output is verified on the live screen path with captures that keep their styling". No file says how to capture the live screen's bytes with styling, and no file records what those bytes are. See B1.

### Q6 Zellij 0.44.2 go or no-go: ADEQUATE for evidence gathered, dependent on web-02
- 05 section 1 facts reproduced: `zellij 0.44.2`; layouts/default.kdl:48-58 is a 1-row tab bar, `children`, a 2-row status bar. The files and sizes in `~/.config/zellij` match.
- 05 states plainly that every runtime behaviour is UNVERIFIED because no session was started. The no-go recommendation is limited to "as a harness or dependency" and the observer-works-outside-Zellij requirement is addressed. Acceptable.
- Missing derivation (minor): the 3 rows of tab and status bar chrome and the pane frame are never turned into usable rows and columns against the 160/116/80 widths and the 44-row contract.

### Q7 64-character hex hash at 80 columns: STRONG
- 01 (section 4.9) and 03 (section 5c) measured independently and agree: the 64-cell token never overflows 80 columns, `wrap` moves it whole to its own line, and a token longer than the width is hard-cut with no marker. 03 proposes a named fixture and test.
- Caveat (minor): 03's proposed fixture is deliberately kept under 4 desk lines. A realistic plan ask puts the hash after a path and a file list; with `DESK_TEXT_LINES = 4` the trailing hash would be replaced by `...`. 04 raises this as an owner question, so it is not lost, but the synthesis must carry it.

## M-01 to M-18, guards, divergences: STRONG
- 04 section 5 maps every finding to its RR lines, mockup evidence, current-output evidence and code location; 01 section 8.1 gives a second, independent map. The two agree except one citation (m1 below).
- Verified: render.py:373 is the `counts_line` wrap and 374 is the caveat line; header gate at render.py:497; `_columns` at 155-230; no `READ ONLY` screen text in the package (the only matches are docstrings and the HELP text); RR line 20 says `FROZEN unavailable (no source)` while the code prints `POLICY FROZEN ...`, as 01 reports.
- M-09's narrowing (no workerState or dispatchStatus column at 116 and 80) is correct against `_columns`.

## Lens questions

1. Actionable or vague? Mostly actionable: findings carry file:line, measured values and named tests. Vague spots are limited to the ones listed as gaps.
2. Beyond surface code reading? Yes for the one-shot path (probes of Rich 15.0.0, StringIO bytes, NO_COLOR). No for the live path: the bytes the person sees were never traced (B1).
3. Enough raw evidence for Q1 to Q7 and M-01 to M-18? Yes except the live-path half of Q5 and the height consequence for Q1.
4. Width and height budgets with real numbers? Width: yes (01 section 4.3 and 4.8, 04 section 4). Height: partial. 01 measured the base ledger at height 40 only, and 03 measured the desk at height 70; the cost of added frame rows at 24, 40 and 44 rows is not derived (01 gap 8 admits it). Together with B1 this matters, because overflow is cropped from the bottom (the footer).
5. Rich colour system and `export_text` from code? Yes, by probe plus source reads (02 read the installed `export_text` signature; I confirmed the behaviour).
6. Gaps honest? Yes. Every file has a Gaps section and labels UNVERIFIED and CODE-CONTRADICTED items. One mislabel: 03 gap 9 is tagged CODE-CONTRADICTED but says it is not a contradiction (cosmetic).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B1 | BLOCKING (IMPORTANT) | 02 sections 2, 3, 8; 01 section 3 and 4.8; Q5 and Q1 height budget | The live path (`LiveScreen`, commands.py:264-274, `Live(..., screen=True)`) is described only from reading and never probed. I probed it: `Live(screen=True)` under a forced-terminal Console of height 3 given a 5-line `Group` emitted `\x1b[?1049h` (alternate screen), `\x1b[?25l`, then only the first 3 lines, each padded with trailing spaces to the console width, then `\x1b[?25h\x1b[?1049l`. Lines 4 and 5 were silently dropped with no ellipsis. Rich's `Live` sets `vertical_overflow="ellipsis"` by default (live.py:68) and wraps the renderable in `Screen` when on the alternate screen (live.py:228); `LiveScreen` passes neither. None of the five files mentions this. Consequences the files miss: (a) 01 says "no final height clamp" as if it were harmless, but on the live path any frame, tile or heading row beyond `policy.height` removes the bottom of the screen, which is the footer key list and `shown x/y`; the plain `screen_lines` tests would not notice. (b) The styled-capture gate demanded by issue-body.md:58 has no capture method: the Live path writes to the real stdout, has no test (03 section 2 confirms), and its bytes include alt-screen codes and padded lines that differ from the one-shot `getvalue()` output. (c) 05 notes `pexpect` is a declared dependency and 03 notes test_keys_spike.py runs Rich `Live` on a real pty, but nobody connects these to a live-path capture. | Add to the research (a short addendum to 02 is enough): the measured Live bytes (alt screen, per-line padding, bottom crop at `policy.height`), the `vertical_overflow` and `Screen` behaviour from the Rich source, and a stated capture route for live styled output (for example a pty run through `pexpect`, or a `Console(force_terminal=True, file=StringIO)` Live as I did) with its limits. Restate the height budget with the bottom-crop consequence. |
| m1 | MINOR | 04 section 5, M-05 row | Cites `render.py:374` for `wrap(panel.counts_line)`; the line is 373 (374 is `caveat_line`). 01 has it right. | Use 373. |
| m2 | MINOR | 01 section 8.2 item 5 vs 04 section 4 | 01 computes 157 of 160 with a 1-cell gap and calls it UNVERIFIED; 04's mockup measurements give 1+114+2+42+1 = 160. | Synthesis should use 04's numbers. |
| m3 | MINOR | 01 section 3 vs 02 section 2 vs 03 section 3 | Three different advice lines for the one-shot styled capture: 01 says use `export_text(styles=True)`, 02 shows that bypasses NO_COLOR and prefers `getvalue()`, 03 says keep `export_text()` unstyled. Each is labelled, but the synthesis must reconcile them (02's finding wins). | Reconcile in the synthesis. |
| m4 | MINOR | 01 gap 8, 03 gap 6 | Height cost of frames at 24, 40 and 44 rows and the desk screens at link-on and heights below 70 are unmeasured; derivable from 04's pane row counts and 01's `spare` formula. | Derive in the synthesis, or note it as a gap. |
| m5 | MINOR | 05 section 7, 1.3 | Zellij chrome (tab bar 1 row + status bar 2 rows, default.kdl:50-56, plus pane frame) is not converted into usable rows and columns. | Add the arithmetic in synthesis or web-02. |
| m6 | MINOR | 05 section 6 gap | "Subagent Read of a PNG" is UNVERIFIED; it works for this agent (verified above). | Update the note. |
| m7 | MINOR | 03 section 5d | The proposed 64-hex fixture avoids the case where the hash trails a long ask and is cut by the 4-line cap. | Add a second fixture, or carry 04's owner question into the report. |
| m8 | MINOR | 01 section 7, 03 gap 9 | Rich auto-detection on real terminals is asserted without a code citation (it is correct: console.py:805); one tag mislabelled CODE-CONTRADICTED. | Cosmetic. |

## Confidence Gate

Checklist items (13): Q1, Q2, Q3, Q4, Q5, Q6, Q7, M-01 to M-18 map, actionable-vs-vague, data-flow depth, width and height budgets, Rich colour system and `export_text` from code, gaps honesty. Each was checked with tool evidence (the Q5 and data-flow checks produced the failing finding B1).
- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 10 | Glob: 1 | Bash: 5. Read + Grep + Glob = 25, at least the 13 checklist items.
- Unchecked items: none. Unverifiable items: none. Not reviewed because they do not exist yet: web-01 and web-02 (Rich composition, Zellij documentation); several Q5 and Q6 conclusions depend on them.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. No Inherited Structural Verdict was in the spawn prompt, so I ran standalone and re-checked claims myself.

**(b) Independent semantic checks (at least 1 required):**
- Rich `safe_box` and `Panel` behaviour: reproduced with a probe (Rich 15.0.0).
- Mockup palette downgrade table: reproduced with `Color.downgrade` for all eight colours, and grepped the `.ansi` files for background and attribute codes (0 matches).
- `export_text(styles=True)` versus NO_COLOR: reproduced.
- Screen line counts at 160/116/80: ran `superclaude observe --once --width W --fixture base` with `LINES=40`; each gave 40 lines and the 80-column head matched 01's table.
- Baseline suite: ran the tests (766 passed); golden counts re-read.
- Environment tool absence: re-ran `command -v` and imports; Zellij version and default.kdl lines re-read.
- Live path bytes and cropping: probed, which produced B1.
- Claims verified against source: about 30. Files read for verification: render.py (150-234, 359-388), terminal.py (18-129), rendering-rules.md (1-75), a mockup `.txt` and `.png`, Rich console.py and live.py, `default.kdl`, issue-body.md and draft-notes.md matches.
- Zero-issue trust: not applicable; one blocking finding and eight minor findings were found.
- Web research: none performed, so no Tavily or fallback use to record.

## Recommendations
- Fix B1 before synthesis starts (a short addendum to 02 with the Live bytes, the `Screen` crop and a capture route). It changes Q5 and the height budget in Q1.
- Carry m2, m3, m5 and m7 into the synthesis as reconciliation notes.

## QA Complete

## Summary
- Questions evaluated: Q1 to Q7, M-01 to M-18 map, and the six lens questions.
- Blocking findings: 1 (B1)
- Minor findings: 8 (m1 to m8)

## Overall Verdict: FAIL

Reason: one blocking finding (B1). Q5's live-path half and the height budget rest on an unmeasured assumption that the Live screen carries styles and fits; I measured that it crops overflow silently from the bottom and pads every line, and no research file says so or gives a live-capture route. All other questions are answerable from the files. Minor findings are notes and do not affect the verdict.
