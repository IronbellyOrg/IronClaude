## evidence-quality QA Report

**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md
**Lens:** evidence-quality
**Date:** 2026-11-17
**Status:** Complete

### Checklist results (appended incrementally)

**a. Specific file path and line for every factual claim: PASS (with minor notes).**
The report (1877 lines, read in nine ranges) cites `file:line` for nearly every code claim. I re-read the cited lines of `render.py`, `terminal.py`, `view.py`, `commands.py`, `export.py`, `parse.py`, `sanitize.py`, `keys.py` and `collector.py` under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/`. I did the same for the cited lines of ten test modules under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/`. Roughly 150 line citations were checked and all resolved to the claimed content, with the small exceptions in the findings table (F-3, F-4). Examples that matched exactly:
- render.py:528 (`Text(line, no_wrap=True, overflow="crop")`)
- render.py:497-498 (`policy.width_class == "full" and view.visible_rows`)
- render.py:439 (the mirrored `ledger_fixed` term)
- render.py:304-308 (the questions-off `clip` branch)
- terminal.py:30-34, :63-70 and :121-123
- view.py:53, :99 and :948
- commands.py:67, :70, :242, :265 and :270
- parse.py:475 and :503
- test_render.py:250-259 (the colour vs NO_COLOR compare is :256)
- test_render.py:396-404, :611-624 and :177-185
- test_commands.py:121, :747-756 and :762-772
- test_linkoff_screen_reference.py:50-64 and :67-75
- release1_surface.py:34-38 and :41-62
- pyproject.toml:34-43 (pexpect at :41)
- spike_child.py:64

Some citations name a research file by line (for example R01:44-52, R04:63-76). A sample of these resolved to the claimed text in `research/01...`, `research/02...`, `research/03...` and `research/04...`. The `GAPS row N` citations I checked (rows 1, 2, 3, 5, 6, 9, 10, 12, 13, 14, 25, 26, 29, 32, 34-40, 42, 54) all matched the gaps log.

**b. No unverified assertion presented as fact: PASS.**
Unverified material is consistently tagged [UNVERIFIED] (Zellij runtime behaviour, plan-ask content, selected-row look, light backgrounds, installability of PNG tools, glyph width in the owner's terminals, the `+1` terms in `spare`, `dir(rich.box)` and others). I looked for untagged assertions and found none that matters. I reproduced the load-bearing measurements in fresh processes against the installed Rich 15.0.0:
- `safe_box` True and False both print `╭──╮`, and `box.ASCII` prints `+---+`.
- Amber `bold #ff8800` under `standard` gives `\x1b[1;91m`, under `256` gives `\x1b[1;38;5;208m`, and under `truecolor` gives `\x1b[1;38;2;255;136;0m`.
- Under NO_COLOR the stream is `hello\n` while `export_text(styles=True)` still returns `\x1b[1;31mhello\x1b[0m\n`.
- The mockup downgrade is base 15, muted 7, slate 8, amber 11, cyan 14, green 7, red 7, violet 7 (256: 189, 145, 60, 214, 80, 115, 210, 147).
- `pytest --collect-only` reports 766 tests.
- `cell_len` is 1 for every candidate frame glyph.
- `cell_len` of an SGR run counts its printable part (the 16-cell example resolves to research 01 line 61).

**c. No hallucinated paths; at least 8 line ranges spot-read: PASS.**
Every path I checked exists:
- All 8 research files, `gaps-and-questions.md`, the 6 synthesis files and the QA reports listed in section 10.
- The mockup directories: 9 `.png`, 9 `.ansi` and 9 `.txt` files, 48/42/42 lines per width.
- `inputs/current/*/` with 0 ESC bytes in all nine `ansi-*.txt`, against 48 ESC lines in `mockups/160/signal-bridge.ansi`.
- `.dev/issues/409/attachments/`, `.dev/issues/606/issue-body.md` (line 84 matches), `pr-591-comment.md` (lines 26-31 match) and `.dev/issues/409/visual-parity/merged/FINDINGS.md` (line 171 holds O-1).
- `/home/coder/.config/zellij/{config.kdl 53, layouts/default.kdl 58, layouts/agent.kdl 265, themes/aidev02.kdl 252}` (line counts and default.kdl 48-58 match).
- `/usr/local/bin/zellij` 0.44.2, DejaVu Sans Mono, node 24.22.2, uv 0.11.8, and the missing-tool list (chromium, rsvg-convert, inkscape, convert, magick, freeze, termshot, aha, ansi2html, unzip, `~/.cache/ms-playwright`).
- Git objects `9e2608b03`, `cd8736199`, `3206bdb9c` and `c69ce4b3a`. The last is not an ancestor of HEAD, which supports the report's "likely pre-squash hash".

Absence claims also held:
- No test references `LiveScreen` or `run_interactive`.
- `Console(` appears only at terminal.py:114.
- `READ ONLY`, `ZELLIJ` and `mouse|blink` appear nowhere in the observe sources (grep matched only stale `.pyc`).
- No 64-hex literal appears in the test sources.

Mockup decode:
- The nine `.ansi` files contain exactly three SGR shapes: `0`, `0;1;38;2;R;G;B` and `0;38;2;R;G;B`. They carry the 8 stated RGB roles and no background, dim, italic or underline.
- Bold counts are 3 to 16 per file, as stated.
- The pane-border geometry I read in the 160 ledger, desk and bridge mockups and the 80 ledger mockup matches the report.
- The `agent.kdl` vs `aidev02.kdl` difference in `frame_selected` and `ribbon_selected` (5 vs 6) is true, although the `agent.kdl` header comment says only `frame_selected.base` differs.

**d. Code evidence vs doc evidence distinguished; web claims carry URLs: PASS.**
[CODE-VERIFIED], [CODE-CONTRADICTED], [STALE DOC] and [UNVERIFIED] are used consistently, and section 4.3b lists the stale docs. I checked these doc-vs-code claims and each held:
- RR 20 vs view.py:948
- QUESTION_GATE_PASSED False in `05-observe-built-state.md:27` vs True at commands.py:67
- research-notes.md:24 (three width classes)
- the `render()` vs `screen_lines` location of the M-10 gate
- RR line count (107)

External claims carry URLs. I re-fetched two. zellij.dev/news/terminal-inbox-session-previews confirms 0.46.0 on 2026-11-11. Rich issue 2153 confirms that rsvg-convert, ImageMagick and Inkscape fail on Rich SVG (Rich 12.1.0, `foreignObject` and `@font-face`).

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| F-1 | MINOR | 1.3, 1.4, 4.1 to 4.3, 6 to 9 (abbreviations); 10 (Evidence Trail) | The report cites its sources by abbreviation and gives no legend or path for them until section 8. `FIND` (used from 1.3: "Source of the list: `FIND`") is `.dev/issues/409/visual-parity/merged/FINDINGS.md`, and that path appears nowhere in the report. `RR` is expanded only in the intro of section 8 (about line 1292), but sections 1 to 7 cite "RR 43" and "RR 57" throughout. `R01` to `R05`, `W01`, `W02` and "GAPS row N" are never defined. Section 10 does not list FINDINGS.md, rendering-rules.md, the mockups directory, `.dev/issues/606/issue-body.md` or `pr-591-comment.md`. A reader cannot resolve the main source of M-01 to M-18 from the report alone. All the claims I traced through these citations were correct; this is a traceability gap, not a false claim. | Add a one-line legend near the top (FIND, RR, R01-R05, W01-W02, GAPS with full paths) and add FINDINGS.md and rendering-rules.md to section 10. |
| F-2 | MINOR | 2.5, 6.2 | `render_current.py` is described as "94 lines". `wc -l` gives 93 and `main()` is on line 93. The same file is cited elsewhere as having `main()` at line 93, so the count contradicts the report's own citation. | Say 93 lines. |
| F-3 | MINOR | 2.3 (whole-line pins), 8 steps 1.6(b) and 6.5 | A few line citations point to a test's `def` line or to a negated assertion instead of the asserting line. `GAP_NOTICE in lines (:242, :454, :490)`: :454 is `GAP_NOTICE not in lines`. Step 6.5 cites :494 and :509 (both `def` lines) and `^\d+/80 shown...` at :337 (a `def` line; the regex is at :350). Step 1.6(b) lists `printed(` at :161 (the call is an `assert bad_chars(out)`). The tests exist and the intent is right; only the pointers are loose. | Cite :497/:512 style assertion lines, or say "in test X" instead of a line number. |
| F-4 | MINOR | 5.1.2 to 5.1.4, 5.2.6, 6.1 Option B | Section 5 tags as "[UNVERIFIED in this synthesis]" facts that the report's own sections 2, 3, 4, 6 and 9 carry as probe-verified or [CODE-CONTRADICTED]: the `safe_box` no-effect probe, the 16-colour collapse mapping and the one-renderable-per-line test pin (test_render.py:399). The tag in 5.1.4 and 6.1 that `box.HEAVY` and `box.ASCII` are unconfirmed is also stale. I probed Rich 15.0.0: `hasattr(rich.box, "HEAVY")` is True and `box.ASCII` prints `+---+`. The tags describe provenance in the web file, so this is honest, but it leaves two conflicting statuses for one fact. | Add a note in section 5 pointing to the 2.1/4.3a probe result, and update the HEAVY/ASCII existence tag. |

No blocking evidence-quality defect was found. Items I tried to falsify and could not:
- fabricated paths
- wrong line citations on load-bearing claims
- the Rich probes
- the 16-colour collapse
- the 766-test baseline
- mockup palette, geometry and ESC counts
- Zellij and tool-availability facts
- the doc-vs-code contradictions
- web citations (two re-fetched)

### Summary

- Total findings: 4
- Critical: 0
- Important: 0
- Minor: 4 (F-1 to F-4, notes only)
- Verdict: **PASS (with notes)**

Confidence: Verified: 4/4 checklist items | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. This is scoped to the evidence-quality lens only. Other dimensions are out of scope for this review.

Tool engagement: Read: 12 (task line 283, 9 report ranges, this report file twice) | Grep: 0 (grep and sed ran inside Bash, which does not count as a tracked Read) | Glob: 0 | Bash: about 17 executed plus 1 blocked by the uv-only hook and re-run with `uv run python -I`. Read plus Grep plus Glob is 12, below the roughly 4 checklist items times ~150 line citations I checked, so the minimum-engagement flag applies by count: the citations were verified through batched Bash `sed -n` reads, which the policy says are not tracked Reads. Tavily: `tavily_extract` 1 call (2 URLs), no fallback to WebFetch or WebSearch.

No fix authorization was given; no file other than this report was modified (temporary probe scripts under /tmp were removed).

## QA Complete

