# QA Report - Research Gate (evidence-quality lens)

**Topic:** observer visual-parity redesign (issue #606)
**Date:** 2026-11-17
**Phase:** research-gate
**Fix cycle:** N/A
**Status:** Complete
**Fix authorization:** false (report only; no research file was modified)
**Scope:** research files 01 to 05 under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/`, plus research-notes.md. The analyst report `qa/analyst-completeness-report.md` did not exist; full independent verification performed.

---

## Checklist results (appended incrementally)

### Item 1 - File inventory: PASS
All five files exist; each has `**Status:** Complete` and a `## Summary` section (01 lines 4 and 250, 02 lines 4 and 155, 03 lines 4 and 241, 04 lines 4 and 240, 05 lines 4 and 149; read in full this session).

### Item 2 - Evidence density: PASS (Dense, well above 80 percent)
Independently re-verified against code and data, not against the other reports:
- Line numbers: every def or constant cited for render.py (51, 62, 83, 87, 94, 141-159, 233, 246, 255, 290, 304, 311, 329, 359, 390, 438-447, 497-502, 524-528), terminal.py (21-24, 30-34, 63-70, 73-92, 110-135), commands.py (38, 57-58, 67, 70, 173-200, 225-242, 257-270, 282, 351, 388), view.py (44-105, 158, 206, 229, 243, 303, 377, 643, 814, 894, 948, 1150), keys.py (22, 27-33, 61, 127-136, 146), collector.py (28-32, 152-153, 193-273), parse.py (469-475, 479-512), questions.py (21-22), export.py (71-118) matched by `grep -n` and `sed -n`.
- Measured screens: re-ran `superclaude observe --once --width {160,116,80} --fixture base` with LINES=40. Section 4.8 of file 01 (row counts 28/29/28, 40 lines total, heading and rule only at 160, `runs seen>` and `e exp>` cuts at 80, `as of` wrapped at 80) matches exactly.
- Rich probes (Rich 15.0.0, `uv run python -I`): `safe_box` True and False give identical `Panel` output; `export_text(styles=True)` keeps colour under NO_COLOR; `standard` turns `#ff8800` into `91`; `auto` on a StringIO gives `None`; `cell_len` of an SGR string is 16; the style cache across colour systems reproduced; glyph widths all 1 cell; the 8 mockup RGBs downgrade exactly as the 04 table states (standard: 15, 8, 14, 7, 11, 7, 7, 7; 256: 189, 60, 80, 145, 214, 115, 210, 147).
- Goldens and tests: `golden_questions_linkoff.json` five = 24/24/25 lines, long_subject = 22/22/23, max widths 160/113/80, panel block 12/13/13 lines; `golden_release1_surface.json` has 5 variants x 14 keys; no ESC byte in either golden; 28 .py files, 22 test_*.py, 766 tests collected; all ~55 test_render.py test names sit at the cited line numbers.
- Mockups: the nine `.ansi` use only `ESC[0;(1;)38;2;R;G;Bm` and `ESC[0m` (8 RGB values, no 48, no 256-colour, no dim); the nine `.txt` are 48 lines at 160 and 42 at 116 and 80, every line the exact column width; pane corner positions match the 04 geometry table row by row (for example 160 signal-bridge `┏1 ┓46 ╭49 ╮122 ┏125 ┓158`); the role-to-text decode (amber attention frame and question text, cyan identity, slate secondary panes, green/red/violet states) matches; the PNG viewed (decision-desk 160) shows the dark navy background claimed in 04 Gap 3.
- Environment (file 05): Zellij 0.44.2, config/layout/theme line numbers and sizes, missing tools, missing Python modules, node v24.22.2, Python 3.10.20, uv 0.11.8, no `~/.cache/ms-playwright`, DejaVu Sans Mono present: all match.
- Spec and findings: RR lines 13, 17, 20, 21, 25, 33, 38, 40, 42, 50, 59, 60, 70, 93 and FINDINGS M-10 and O-1 read and match; `inputs/current/*` line citations match; all nine `ansi-*.txt` hold 0 ESC bytes.

### Item 3 - Scope coverage: PASS (two minor notes)
Every EXISTING_FILES entry of research-notes.md is examined: render, view, terminal, sanitize (01); commands, export, collector, questions, keys (02); tests/observe and both goldens (03); rendering-rules, FINDINGS, mockups, current renders, pr-591-comment, render_current.py (04); Zellij files, pyproject.toml, Makefile, render_current.py (05).
- Note: `.dev/issues/409/attachments/` is named in no research file, but `cmp` shows the three PNGs there are byte-identical to the 160 mockup PNGs (signal-bridge, agent-focus-attention-ledger, decision-desk), so no information is lost (MINOR-6).
- Note: parse.py and adapter.py are context only per the notes; parse.py is read for the link and ask path (02 section 6), adapter.py is not read.

### Item 4 - Documentation cross-validation: FAIL (one blocking finding, B-1)
Every `[CODE-VERIFIED]` claim I re-checked held, except one: file 04 line 147 (G-1 row) tags as `[CODE-VERIFIED]` the statement that `terminal.py:123 safe_box=policy.ascii` "covers only Rich `Box` objects". That is false (see B-1). All other doc-sourced claims are tagged and true: FINDINGS M-10 location drift, "153 cells" unreproducible, RR 20 versus code `POLICY FROZEN`, RR 61 versus RR 42, stale commit hash c69ce4b3a (git log prints cd8736199), pre-#592 `QUESTION_GATE_PASSED = False` in older reviews.

### Item 5 - Contradiction resolution: FAIL (same root, B-1)
Files 03 (line 194) and 04 (line 147) state that `make_console(... safe_box=policy.ascii)` gives or covers an ASCII fallback for Rich boxes. File 01 (lines 19, 204, 229) states the opposite and proves it by probe. The synthesis would receive two conflicting claims about the G-1 guard with no marker saying which wins. I confirmed 01 is right: probe output identical for `safe_box=True` and `False` (`╭─────── T ────────╮`), and Rich source `.venv/lib/python3.10/site-packages/rich/box.py:79-83` (`substitute()` only swaps for `legacy_windows`, or to `ASCII` when `options.ascii_only`) and `rich/panel.py:156-157`.
Other cross-file pairs checked and consistent: Q5 and export_text (01 vs 02), LiveScreen untested (02 vs 03), styled capture route (02 vs 03 are alternatives, flagged as open decisions), colour collapse (01 vs 04 compatible, see MINOR-5).

### Item 6 - Gap severity: PASS
Gaps sections of all five files read. Open items (colour depth policy, T47 re-baseline, styled `--once` capture, 153-cell figure, unmeasured 8-row behaviour, Zellij runtime, PNG renderer) are each flagged UNVERIFIED or as an owner decision and none is needed as fact by the synthesis. No CRITICAL or IMPORTANT gap other than B-1. The unmeasured 24-row and MIN_ROWS behaviour (01 Gap 8) is MINOR for a Standard-tier report.

### Item 7 - Depth appropriateness (Standard): PASS
Complete flow traced end to end: Collector (`questions=`, `link=`) -> `parse_questions` -> `QuestionState` -> `build_view` -> `screen_lines` -> `render` -> `LiveScreen` or `export_text` (02 sections 1 and 6, 01 section 3).

### Item 8 - Integration point coverage: PASS
screen_lines to render seam (01 section 3), export_text seam (02 section 2, verified by probe), LiveScreen seam (02 section 3, Rich `Live.start` source lines 127-128 confirmed), golden seam (03 section 4, `surface()` and `capture()` reproduce both goldens byte for byte) all documented.

### Item 9 - Pattern documentation: PASS
Pinned-regex gate constants (verified in test_commands.py), source-scan guards (test_render.py 400-404, test_terminal.py 181-198, test_export.py 238-243, all verified verbatim), plain-lines-as-source-of-truth, independent colour and ASCII policy, sanitize-then-Text.

### Item 10 - Incremental writing compliance: UNVERIFIABLE
No write history is available. Structure shows iteration (inline `[CODE-CONTRADICTED]` corrections, probe notes added mid-section, per-section Key Takeaways), so there is no sign of one-shot generation, but I cannot prove it.

## Issues Found

### Blocking

| # | Severity | File and location | Evidence | Proposed fix |
|---|----------|-------------------|----------|--------------|
| B-1 | IMPORTANT | `research/03-tests-goldens-fixtures.md` line 194 (section 6 design rule 3) and `research/04-spec-mockups-and-findings.md` line 147 (G-1 row, tagged `[CODE-VERIFIED]`) | 03:194 says boxes get their ASCII fallback from `make_console(...safe_box=policy.ascii)` "for Rich boxes". 04:147 says `safe_box=policy.ascii` "covers only Rich `Box` objects". Both are false and contradict 01 lines 19, 204, 229. Probe (Rich 15.0.0, exact `make_console` arguments): `Panel` prints identical rounded Unicode borders with `safe_box=True` and `False`. Source: `rich/box.py:79-83` (`substitute` uses `safe` only for `legacy_windows`; ASCII only when `options.ascii_only`), `rich/panel.py:156-157`. `--ascii` on a UTF-8 terminal therefore needs an explicit `box=rich.box.ASCII` or hand-built `+-\|` glyphs; a plan that trusts 03 or 04 would ship Unicode borders under `--ascii` and break guard G-1 (RR line 25) and the ASCII-only tests. | 03 line 194: replace the safe_box clause with "`safe_box` does not ASCII-ize a Rich box on UTF-8 output (rich/box.py:79-83; 01 section 1); a Rich frame needs an explicit `box=rich.box.ASCII` when `policy.ascii`, or hand-built glyphs", tag `[CODE-CONTRADICTED]`. 04 line 147: delete "covers only Rich `Box` objects", state that `safe_box` does not affect Rich boxes on UTF-8 output, move the corrected clause out of the `[CODE-VERIFIED]` tag, and cross-reference 01 section 1 and Gap 3. Also drop "pinned by test_terminal.py:114-116" as support: that test only pins the attribute value, not any ASCII box behaviour. |

### Minor (notes; not rechecked in later rounds)

| # | Severity | Location | Issue | Suggested fix |
|---|----------|----------|-------|---------------|
| MINOR-1 | MINOR | 03 section 5c, width 80 bullet | Says line 2 `files: src/superclaude/cli/observe/render.py tests/observe/test_render.py hash` is "exactly the width". Reproduced with the same text: desk lines at 80 are 78, 78 and 64 cells; that line is 78 cells. | Say 78 cells, or drop "exactly the width". |
| MINOR-2 | MINOR | 03 section 5c, long-path bullet | "a 140-character path" is described as splitting into three pieces (`...TASK-` / `RESEARCH-...fixtur` / `es.md`). A hard cut at 80 cells gives two pieces for 139 characters (reproduced: `[80, 59]`); three pieces need about 165 characters. Behaviour claim (hard cut mid-word, no marker) is right; the number is not. | Correct the length or the split. |
| MINOR-3 | MINOR | 04 section 1 | "RR (108 lines total)": `wc -l` of rendering-rules.md is 107. | Change to 107. |
| MINOR-4 | MINOR | 04 section 2 | "Count of `ESC[0;1;` sequences is 2 to 15 per file": per-file occurrences counted here are 3 to 16 (160 signal-bridge 16, 80 attention-ledger 3). | State the measure (occurrences or distinct) and the numbers. |
| MINOR-5 | MINOR | 01 section 7 last bullets versus 04 section 3 | 01 infers slate and muted "can collapse" to greys; 04 computed slate 8 and muted 7 (distinct), with muted, green, red and violet all at 7. The 04 table is the measured one. | Point 01's inference at the 04 table. |
| MINOR-6 | MINOR | 03 section 2 intro; scope | Grep hit counts differ from the re-run (test_render 64 vs 65, conftest 4 vs 2, test_fixtures 4 vs 2, test_export 2 vs 3); `.dev/issues/409/attachments/` unnamed (identical to the 160 mockup PNGs); research-notes.md line 24 still says width classes full/line/narrow (code has four, already corrected in 01) and line 95 says O-1 is "recorded in the findings" while FINDINGS and 04 treat it as pending the owner. | Cosmetic; correct when next edited. |

## Overall Verdict: FAIL

One blocking finding (B-1) is open. Everything else in the five research files verified against code, data and live probes. After B-1 is corrected in files 03 and 04 the gate should pass; no research file was modified by this review.

## Summary

| Measure | Count |
|---|---|
| Checks passed | 7 of 10 (items 1, 2, 3, 6, 7, 8, 9) |
| Checks failed | 2 (items 4 and 5, one shared root cause) |
| Unverifiable | 1 (item 10) |
| Blocking findings (CRITICAL or IMPORTANT) | 1 (B-1, IMPORTANT) |
| Minor findings (notes) | 6 (MINOR-1 to MINOR-6) |
| Issues fixed in place | 0 (fix_authorization false) |

## Confidence Gate

- **Confidence:** Verified: 9/10 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% (9 / (10 - 1))
- **Tool engagement:** Read: 10 | Grep: 5 (one returned a path error and was repeated) | Glob: 1 | Bash: 17 (read-only inspection, `uv run python -I` probes, `superclaude observe --once` runs)
- Web research: none needed; the one external fact (Rich `safe_box` behaviour) was verified from the installed Rich 15.0.0 source and a probe. `tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0`.
- UNVERIFIABLE item: item 10, no write history exists to prove incremental writing.
- Self-audit: a zero-finding verdict would have been wrong, because 03:194 and 04:147 contradict 01 on an ASCII guard; the proof is the probe output and rich/box.py:79-83 cited in B-1.

## Recommendations

1. Correct the `safe_box` statements in `research/03-tests-goldens-fixtures.md` line 194 and `research/04-spec-mockups-and-findings.md` line 147 as described in B-1, then re-review once (fix cycle 1).
2. Synthesis must not state "153 cells" as fact, must use four width classes (full, line, short, narrow), and must treat `--ascii` frames as needing an explicit box choice.

## QA Complete
