## Anti-Omission Report

**Status:** Complete
**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md
**Date:** 2026-11-17

**Input files checked:** research/04-spec-mockups-and-findings.md, research/05-zellij-and-render-harness-environment.md, research/web-02-zellij-and-terminal-capture.md, gaps-and-questions.md, synthesis/synth-04-options-recommendation.md, synthesis/synth-05-implementation-plan.md, synthesis/synth-06-questions-evidence.md (all under the task directory); 675 items enumerated (634 distinct findings plus 41 restatements counted as COVERED-BY-DEDUP; counts per file in Summary).

**Method.** Coverage judged by meaning, never by ID citation. The report (1918 lines) was read directly for lines 1-979 (Sections 1-6.1). Sections 6-10 reproduce synth-04, synth-05 and synth-06 near-verbatim: a line-exact comparison (`grep -v -F -x -f report synth`) found 15 of 293 nonblank synth-04 lines, 26 of 344 synth-05 lines and 10 of 106 synth-06 lines not verbatim; I read each such line and its report counterpart (they are edits: decision ids D-1..D-12, RB and step wording, Section 9 row rewrites; no finding was removed). Report headings for 6.0-6.4, 7.1-7.4, 8.1-8.10, Phases 0-7, 9.1-9.6 and 10 match the synth structure. Targeted greps then tested every candidate omission.

## Enumeration (by input file; each item judged by meaning)

### research/04-spec-mockups-and-findings.md (120 items)

| Group | Items | Representation in report |
|---|---|---|
| RR citation table: RR 13, 17, 20, 21, 25, 30, 31, 32, 33, 38-50, 57, 61, 70, 93 | 14 | REPRESENTED: 1.3, 2.4 ("Spec lines ... FIND citations all resolved"), 3.7 (AD-1..7), 4.3b. Detail of RR 17 header wording, RR 21 key list, RR 26 not carried: see O2, O3, O4 |
| Mockup colour decode: 8 roles, selected, borders, titles, count tile, bold use, method and sequence format | 14 | REPRESENTED: 2.4 colour table, 3.2 table with 16-colour and 256 indexes |
| Colour depth: truecolor assumption, code cap, Rich downgrade table, Q4 consequence, NO_COLOR, no detection | 6 | REPRESENTED: 2.1, 3.2, 3.4, 6.3, 7.2 Q4 |
| Pane geometry: 9 screen/width rows, common chrome, 2 anomalies, frame size | 13 | REPRESENTED: 2.4 geometry table, 3.3, 7.1 budgets, 8.3; titles anomalies in 4.3b |
| M-01..M-18 plus 4 table notes (render.py:528, M-10 location, M-11 cause, M-14 three places) | 22 | REPRESENTED: 1.3, 2.4 change map, 4.1a, 4.2 RN-1..RN-3, 8.10 |
| Guards G-1, G-2, AD-1..AD-7, OPEN-1..3, O-1 | 14 | REPRESENTED: 1.3, 3.7, 4.1b/4.1c, 7.3, 9.1 |
| Mockup versus current, 9 screen/width rows | 9 | REPRESENTED (condensed): 2.4 "Spec versus code", 3.1, 3.3 |
| render_current.py mechanics (6 facts) | 6 | 5 REPRESENTED (2.4, 2.5, steps 0.1-0.3); 1 OMITTED (O1) |
| Q7 context (hash, wrap, 74 inner width, line-budget risk) | 4 | REPRESENTED: 2.3 Q7, 7.2 Q7, 9.2 row 10 |
| Gaps (6 UNVERIFIED, 2 CODE-CONTRADICTED) | 8 | REPRESENTED: 2.7, 4.3a, 4.4, 9.4 |
| Owner questions | 4 | REPRESENTED: 7.3, 9.1, 9.2 |
| Stale documentation | 6 | REPRESENTED: 4.3b, 9.5 |

(Per-group items sum to 120.) 

### research/05-zellij-and-render-harness-environment.md (65 items)

| Group | Items | Representation |
|---|---|---|
| Zellij version, setup --check output, no session started | 3 | REPRESENTED: 2.5 table and proving-commands table, 5.4 |
| config.kdl directives and no keybinds; header purpose | 3 | 2 REPRESENTED (2.5); header purpose (suppress first-run wizards in a CI contract test) OMITTED (O5) |
| default.kdl (tab bar 1, status bar 2), agent.kdl (theme, status bar only, magenta), aidev02.kdl (ANSI-16 only, mapping, ban on blue) | 7 | REPRESENTED: 2.5, 3.5 Zellij chrome, 5.2.7, 5.4.4-5.4.5 |
| Zellij help-text capabilities (layout flags, run -f size/position, dump-screen flags, action list partial, bars as plugins, theme reuse, command-pane syntax unverified) | 7 | 6 REPRESENTED (2.5, 5.4.1-5.4.3, 9.3); remaining `zellij run` flags and `--max-panes` OMITTED (O6) |
| Offline tools: Rich 15.0.0 and its export methods, missing Python modules, missing binaries, node/npx, no ms-playwright cache, DejaVu font, pip list | 8 | REPRESENTED: 2.5 tool tables, 5.5 |
| Dev dependencies, pyproject lines, no image dependency, Makefile has no render target (plus Makefile target list) | 3 | REPRESENTED: 2.5 bullet; Makefile target list with line numbers OMITTED (O9, MINOR) |
| render_current.py mechanics (6) and mockup input files | 7 | REPRESENTED: 2.5, steps 0.1-0.3 |
| Harness options table (7 options) | 7 | REPRESENTED: 5.5, 6.2 H1-H3 |
| Fresh reviewer scoring inputs and weaker text-vs-PNG comparison (4) | 4 | REPRESENTED: 5.5.9, 8.5 G4, 6.2 H3 |
| Q6 evidence (for, against, standalone requirement, recommendation) | 4 | REPRESENTED: 2.5, 5.4 contradiction note, 6.4, 7.2 Q6 |
| Gaps and Questions (9 incl. PNG question) | 9 | REPRESENTED: 2.7, 4.4, 9.3, 9.2 row 15 |
| Stale documentation (3) | 3 | REPRESENTED: 4.3b, 9.5 row 41 |

### research/web-02-zellij-and-terminal-capture.md (58 raw items: 46 distinct + 12 restatements)

| Group | Items | Representation |
|---|---|---|
| "What we already know" restated local facts | 5 | COVERED-BY-DEDUP with 2.5 and 5.5 |
| A1 layouts, floating_panes, command panes, swap layouts | 5 | 4 REPRESENTED (5.4.1); command-pane exit code/Enter re-run/`start_suspended` and swap-layout constraints OMITTED (O7) |
| A2 dump-screen options, headless recipes, 0.44.0 CLI, fidelity inference | 5 | REPRESENTED: 5.4.2-5.4.3 |
| A3 bars, zjstatus | 2 | REPRESENTED: 5.4.4; zjstatus excluded with rationale (5.6) |
| A4 themes, legacy spec, theme_dark/light | 2 | REPRESENTED: 5.4.5 |
| A5 ZELLIJ env var, other vars, TMPDIR caveat | 3 | REPRESENTED: 5.4.6 |
| A6 colour pass-through not documented; COLORTERM/TERM background | 2 | REPRESENTED: 5.4.7, 5.2.2 |
| A7 docs 0.46.0 vs local 0.44.2 | 1 | REPRESENTED: 5.4.8 |
| B1 Rich export_svg/export_html, issue 2153 browser-only | 3 | REPRESENTED: 5.5.1, 5.3.4 |
| B2 Playwright screenshot options; MCP session-only | 3 | REPRESENTED: 5.5.2 |
| B3 freeze | 3 | REPRESENTED: 5.5.3 |
| B4 pyte | 2 | REPRESENTED: 5.5.4 |
| B5 aha, ansi2html, termshot | 2 | REPRESENTED: 5.5.5 |
| B6 cairosvg, rsvg-convert | 2 | REPRESENTED: 5.5.6 |
| B7 reviewer comparison, fixed size and font | 3 | REPRESENTED: 5.5.8-5.5.9 |
| B8 export_text(styles=True) discrepancy, not-found list | 2 | REPRESENTED: 5.3 contradiction paragraph, 4.3a |
| Key External Findings (7) | 7 | COVERED-BY-DEDUP with 5.6 table |
| Recommendations 1-6 | 6 | REPRESENTED: 5.5.8, 6.2 H3, 6.4 Z2, 7.1, 7.2, 9.3 row 21 |

(Rows sum to 58 raw items; the 12 restatements are the 5 "already know" items and the 7 Key External Findings, each restating an item above or a local fact already enumerated in file 05.)

### gaps-and-questions.md (106 raw rows: 77 distinct + 29 restatements)

| Group | Items | Representation |
|---|---|---|
| Section A: R-1 (safe_box false claim, corrected), R-2 (live path never traced, section 9 added) | 2 | REPRESENTED: 2.1, 2.2, 4.3a, 9.5 C1-C2 |
| Section B rows 1-8 (G-A..G-H: goldens, colour depth, styled capture, O-1, hard-wrap/hash, LiveScreen untested, small heights, RR 61 contradiction) | 8 | REPRESENTED: 4.1b, 7.3, 9.2 rows 5-14 |
| Section B rows 9-19 (153 cells, four width classes, FROZEN wording, slate/muted inference, styles=True caveat, height 50 vs 48/42, ambiguous glyphs, `+1` terms, fixtures, unmeasured live screens, 02 no doc claims) | 11 | REPRESENTED: 2.6, 2.7, 4.3a, 9.4 (row 19 trivial, 4.5) |
| Section B rows 20-27 (blink/mouse constraint, view.py line numbers, Windows, 02 coverage, adapter.py, PYTHONPATH layout, F-06 test classification, no recorder for goldens) | 8 | REPRESENTED: 3.7, 2.2, 4.4, 4.5, 9.4 rows 31-36 |
| Section B rows 28-33 (pr-591 premise, selected-row look, navy background, plan-ask content, light terminals, M-10 location) | 6 | REPRESENTED: 4.1b, 4.3a, 4.4, 9.4 |
| Section B rows 34-42 (Zellij unverified items, CI presence, install questions, PNG read, Q3 rubric, Zellij chrome arithmetic) | 9 | REPRESENTED: 2.5, 3.5, 4.4, 9.3 |
| Section B rows 43-58 (gate-test ranges, headers lacking scope list, 78-cell and 139-char corrections, RR 107 lines, ESC counts, grep counts, attachments, research-notes lines, render.py:373, slack, m8 uncited detection, Summary placement, test_terminal 109/115, live.py 125-130) | 16 | REPRESENTED: 4.3a, 4.3b, 4.5 (cosmetic corrections). Row 55's console.py:805/955/964 citation OMITTED (O8) |
| Section C rows not duplicating Section B (#10, #28-#39: commands.py:63-66 comment, RR 37-41/60-61 stale, RR 33 flags column, RR 41/43, RR 61, OPEN HUMAN QUESTIONS, RR 59, render_current docstring, c69ce4b3a commit, QUESTION_GATE_PASSED doc, design-docs line shift, Zellij headers, config.kdl upstream cites) | 13 | REPRESENTED: 4.3b, 4.4, 9.5 |
| Section D Q-1..Q-4 (O-1, OPEN-1, OPEN-2, OPEN-3) | 4 | REPRESENTED: 7.3, 9.1 |
| Section C rows duplicating Section B (26) and Q-5, Q-6, Q-7 (3) | 29 | COVERED-BY-DEDUP (each names its Section B row; e.g. C#1 = B row 9, Q-5 = B row 2) |

(Distinct rows: 2+8+11+8+6+9+16+13+4 = 77; restatements 29.)

### synthesis/synth-04-options-recommendation.md (83 items)

| Group | Items | Representation |
|---|---|---|
| 6.0 contradictions 1-9 | 9 | REPRESENTED: report 6.0 (verbatim), 2.6, 4.3a |
| 6.1 Q1: bounding facts (7), Options A, B, C, comparison table | 11 | REPRESENTED: report 6.1 (verbatim) |
| 6.2 Q3: facts (6), H1, H2, H3, comparison | 10 | REPRESENTED: report 6.2 |
| 6.3 Q4: facts (6), D1, D2, D3, comparison | 10 | REPRESENTED: report 6.3 |
| 6.4 Q6: facts, Z1, Z2, Z3, comparison | 5 | REPRESENTED: report 6.4 |
| 7.1 recommendation rows (Q1, Q3, Q4, Q6) | 4 | REPRESENTED: report 7.1 |
| 7.1 recommended sequence P0..P7 | 8 | REPRESENTED: report 7.1 list (verbatim) |
| 7.1 width and height budgets (3 width rows, 5 height rows) | 8 | REPRESENTED: report 7.1 budgets tables |
| 7.2 direct answers Q1..Q7 | 7 | REPRESENTED: report 7.2 |
| 7.3 owner decisions (O-1, OPEN-1..3) and 6 further decisions | 10 | REPRESENTED: report 7.3 (re-labelled D-1..D-12; D-9 and D-12 are new splits, nothing lost) |
| 7.4 coverage note and exclusions | 1 | REPRESENTED: report 7.4 |

### synthesis/synth-05-implementation-plan.md (188 items)

| Group | Items | Representation |
|---|---|---|
| 8.1 planning decisions Q1..Q7 and the data-flow diagram | 7 | REPRESENTED: report 8.1 |
| 8.2 owner decisions D-1..D-7 | 7 | REPRESENTED: report 8.2 (extended to D-12) |
| 8.3 geometry and height budget rows | 8 | REPRESENTED: report 8.3 |
| 8.4 rubric RB-01..RB-23 | 23 | REPRESENTED: report 8.4 (RB wording refined in 7 rows) |
| 8.5 gate protocol G1..G6 | 6 | REPRESENTED: report 8.5 (G2, G3 refined) |
| 8.6 contradictions (9), 8.7 external context (5) | 14 | REPRESENTED: report 8.6, 8.7 |
| Phase 0 steps 0.1-0.8, Phase 1 steps 1.1-1.7, Phase 2 steps 2.1-2.8, Phase 3 steps 3.1-3.10, Phase 4 steps 4.1-4.9, Phase 5 steps 5.1-5.7, Phase 6 steps 6.1-6.7, Phase 7 steps 7.1-7.6 | 62 | REPRESENTED: report Phases 0-7 (steps 0.2, 0.3, 0.6, 0.8, 1.4, 1.6, 3.6, 7.3 reworded, content kept) |
| 8.8 unverified items (16) and excluded findings (9) | 25 | REPRESENTED: report 8.8 |
| 8.9 integration checklist 1..17 | 17 | REPRESENTED: report 8.9 |
| 8.10 finding-to-phase map M-01..M-18 | 18 | REPRESENTED: report 8.10 |
| Summary | 1 | REPRESENTED: report Summary |

### synthesis/synth-06-questions-evidence.md (55 items)

| Group | Items | Representation |
|---|---|---|
| 9.1 owner decisions rows 1-4 | 4 | REPRESENTED: report 9.1 |
| 9.2 decision-level gaps rows 5-15 | 11 | REPRESENTED: report 9.2 (rows 5, 6, 7, 8, 10, 14, 15 reworded) |
| 9.3 Zellij and environment rows 16-22 | 7 | REPRESENTED: report 9.3 |
| 9.4 design-evidence rows 23-37 | 15 | REPRESENTED: report 9.4 |
| 9.5 stale docs rows 38-41 and corrected claims C1-C8 | 12 | REPRESENTED: report 9.5 |
| 9.6 exclusion note | 1 | REPRESENTED: report 9.6 |
| 10 evidence trail (codebase, web, gaps log, synthesis files, QA reports) | 5 | REPRESENTED: report 10 |

## Per-omission verification evidence

Each OMITTED item below was searched in the report with several wordings; no match anywhere:
- `grep` for "mode=fixture", "mode=live", "Not captured", "error states": 0 hits (O1).
- `grep` for "SYNTHETIC FIXTURE": 0 hits; "SYNTHETIC" appears only as the mockup badge (O2).
- `grep` for "RR 26", "RR line 26", "untruncated": 0 hits (O3).
- `grep` for "Up/Down", "j/k": 0 hits; `KEYS_LITERAL` appears only as a test pin (O4).
- `grep` for "first-run", "wizard": 0 hits (O5).
- `grep` for "--pinned", "--stacked", "--blocking", "--max-panes": 0 hits (O6).
- `grep` for "start_suspended", "exit code", "re-run with", "swap_floating_layout": 0 hits; "swap" matches only the safe_box row (O7).
- `grep` for "console.py:805": 0 hits (O8).
- `grep` for "Makefile line", "lint-architecture", "verify-sync": 0 hits (O9).

### Omissions Found

| # | Source finding | Source file | Status | If deduped by which report item | Severity |
|---|---|---|---|---|---|
| O1 | `render_current.py` provenance: the ledger capture uses fixture-mode data (`mode=fixture`) while questions and desk use live-mode data (explains the different first lines); and the captures do NOT cover NO_COLOR, `--ascii`, live observer, error states, any hash-bearing question or heights other than 50 (section 7 last bullet). Report says only "synthetic data at height 50" (2.4) and 0 ESC bytes | research/04-spec-mockups-and-findings.md section 7 | OMITTED (partial) | n/a (the no-hash-fixture and height 50 parts are covered at 2.3 and 3.5) | MINOR |
| O2 | RR line 17 header contract wording: fixture header reads `SYNTHETIC FIXTURE <variant>, not Orca data`; `one Run only: <runId>`; the contract has no READ ONLY badge. Report keeps only "RR 17 changes (badge)" | research/04 section 1 | OMITTED (detail) | n/a | MINOR |
| O3 | Inspector and export paths show the full question text untruncated (RR 26) but the Decision Desk does not | research/04 section 8 | OMITTED | n/a | MINOR |
| O4 | RR line 21 key list contents (Up/Down, j/k, Enter, Esc, `/`, h, m, e, q; n/p with link; no `r`) | research/04 section 1 | OMITTED (detail; the 107-character literal pin is covered at 2.3) | n/a | MINOR |
| O5 | `config.kdl` header states the file exists to suppress first-run wizards for a CI contract test, not to style anything | research/05 section 1.2 | OMITTED | n/a | MINOR |
| O6 | `zellij run` further flags (`--pinned`, `--stacked`, `--blocking`, `--block-until-exit[-success\|-failure]`, `--in-place`, `--cwd`, `-c/--close-on-exit`, `--borderless`) and `--max-panes`, `-c/--config`, `--config-dir` | research/05 section 1.6 | OMITTED (detail; float/size flags are covered) | n/a | MINOR |
| O7 | Zellij command panes show exit code, can be re-run with Enter or started suspended (`start_suspended`); `swap_floating_layout`/`swap_tiled_layout` with `max_panes`, `min_panes`, `exact_panes` | research/web-02 section A1 | OMITTED | n/a | MINOR |
| O8 | Citation for Rich colour auto-detection: console.py lines 805, 955, 964 (gaps row 55 asks to add the citation) | gaps-and-questions.md row 55 | OMITTED (citation only; behaviour covered at 5.2.2 citing console.py without lines) | n/a | MINOR |
| O9 | Makefile target inventory with line numbers (install 5, test 13, lint 48, format 53, sync-dev 109, verify-sync 166, verify-deps 356, lint-architecture 362, eval-skill 497, reflect-eval 508) behind "no render, screenshot or observe target" | research/05 section 3 | OMITTED (the conclusion is covered at 2.5; only the supporting inventory is dropped) | n/a | MINOR |

No CRITICAL or IMPORTANT omission found. Items checked and judged NOT omitted (examples, for the record): the muted-role colour index collision (3.2, 6.3, 7.2), the 64-hex hash analysis (2.3, 7.2, 8.1 Q7, 9.2 row 10), the Zellij go/no-go split (5.4 contradiction note, 6.4, 7.2), every M-01..M-18 change point (2.4 map, 4.1a, 8.10), every guard and accepted divergence (1.3, 3.7), the 58 gap rows (4.3a, 4.3b, 4.4, 4.5, 9.x), all seven Q answers (7.2), every plan step 0.1-7.6 (Phases 0-7), RB-01..RB-23 (8.4), and the evidence trail (10). Edits from Gate 3 and the coordinator fix (decisions D-9 to D-12, the harness contract in step 0.3, the proving-commands tables in 2.5) add content and removed none of the enumerated findings.

### Summary

| Measure | Count |
|---|---|
| Findings enumerated (raw items) | 675 (634 distinct findings + 41 restatements) |
| Per file | 04: 120; 05: 65; web-02: 58 raw (46 distinct); gaps-and-questions: 106 raw (77 distinct); synth-04: 83; synth-05: 188; synth-06: 55 |
| REPRESENTED | 625 |
| COVERED-BY-DEDUP | 41 (12 in web-02, 29 in gaps-and-questions: Section C rows that point to a Section B row, and Q-5..Q-7) |
| OMITTED | 9 (all MINOR; 0 CRITICAL, 0 IMPORTANT) |

(625 + 41 + 9 = 675.)

**Verdict: FAIL (9 omissions, all MINOR).** By the stated rule the verdict is FAIL because the omitted count is above zero; the omissions are redundant detail (provenance notes, flag inventories, a citation), not foundational findings. Recommended handling: add one or two sentences for O1, O2, O3 and O4 if the coordinator wants a strict PASS; O5-O9 are low-value and may be dismissed with a log line.

**Status:** Complete
