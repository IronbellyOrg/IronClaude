# QA Report: Qualitative fix verification, Phase 5 synthesis gate (Gate 2), cycle 1

**Topic:** observer visual-parity investigation (issue #606), six synthesis files after the cycle-1 fixes
**Date:** 2026-11-17
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 1
**Fix authorization:** false (no file modified except this report)

Inputs read in full: `qa/qa-consolidated-findings-phase5.md`, `qa/qa-fix-log-phase5.md`, `synthesis/synth-01` to `synth-06`. Code read to check the fixes: `src/superclaude/cli/observe/render.py` (62-80, 326-356, 390-531), `tests/observe/release1_surface.py`, `rendering-rules.md` lines 38-51, greps over `view.py` and `parse.py`. The Inherited Structural Verdict section was not supplied, so structural checks were done standalone.

---

## Overall Verdict: PASS (with 7 minor notes)

Remaining blocking count: 0. All five cycle-1 blocking findings are fixed and verified against code; no fix introduced a contradiction; the story and the Q1 to Q7 answers are consistent with the plan of record (P0 to P7 in synth-05).

## Part A. The five blocking findings of cycle 1, re-verified

| # | Finding | Result | Evidence |
|---|---|---|---|
| F1 | Three incompatible phase schemes | FIXED | synth-05 opening of Section 8 now states P0 to P7 is authoritative and that Sections 3.8 and 7 mirror it. synth-04 7.1 lists P0 to P7 with the same golden per phase as synth-05 (P1 none, P2 both presentation goldens after the records split, P3 link-off, P4 link-off, P5 none, P6 release-1, P7 none; synth-05 steps 1.6(c), 2.7, 3.9, 4.8, 5.6, 6.6). synth-04 7.2 Q2 row gives the same assignment. synth-02 3.8 Q2 row labels the old P0 to P5 as research 03's own grouping and gives P0 to P7. synth-04 7.3 tables use P4 and P5 for the two-column phases and P2, P3, P4, P6 for golden changes, as synth-05 does. The remaining old-scheme strings are labelled as research labels (synth-04 line 70, synth-06 rows 9, 31 and Section 10 line 102). A grep for phase labels over synth-06 returns only those labelled uses. No scheme conflict remains. |
| F2 | Suite not green after Phase 2 (printed_* and T47) | FIXED | Read `tests/observe/release1_surface.py`: `_printed` (lines 34-38) builds the string through `make_console` and `render()`, and `surface()` stores it as `printed_{width}` (line 60), so the finding's mechanism is real. synth-05 step 1.6(c) now makes `_printed` return `strip_sgr(...)`, leaves T47 unedited, and keeps the golden bytes unchanged in P1. Step 2.7 regenerates the golden through the same `surface()`, so `printed_*` is SGR-free by construction, and adds `test_presentation_goldens_hold_no_escape_bytes`. Step 6.6 repeats the rule. `strip_sgr` is created in P0 step 0.7 before P1 imports it (order correct). synth-02 M-01 note and RN-1 were corrected to the same route. No side of T47 is stripped asymmetrically in any phase. Grep over tests for `make_console`, `console_factory`, `export_text`, `getvalue()`: only test_render, release1_surface, test_terminal, conftest and test_fixtures (plain `export_text` on a NO_COLOR console) touch a console, and step 1.6(b) covers test_render. test_commands reads `deps.stdout.getvalue()` on the one-shot path, which D-4 keeps plain. Each phase leaves the suite green by the plan's own accounting. |
| F3 | Q7 hash: "never cut" vs the 4-line cap | FIXED | Code check, `_desk_lines` render.py:339-346: when the wrapped ask has more than `DESK_TEXT_LINES` (view.py:99, value 4) lines, line 4 is replaced by its prefix of `width - 3` cells plus `...`, and later lines are dropped. `ASK_CAP = 400` at parse.py:475, applied at parse.py:503. `wrap` (render.py:62-80) breaks at the last space or hard-splits with no marker. The new rule in synth-05 8.1 Q7 matches this: whole by wrap, but only if inside the first four wrapped lines, otherwise not shown. D-6 default ("today's rule, no cap changed") agrees. Step 0.6 pins the `...` cut as the one stated exception and RB-19 is scoped to the `PLAN_ASK` fixture. synth-04 Q7 answer and 7.3 table, synth-02 SC-10 and G-E row, synth-06 row 10 and synth-01 2.8 all agree with it. Inner widths 154/110/74 (P3) and 72/110/74 (P5) are arithmetically right (160-6, 116-6, 80-6; 76-4, 114-4, 78-4). |
| F4 | False instruction to add heading rows to `reserved` | FIXED | render.py:495-502 read: `body` gets the heading rows at 497-498, then `reserved = len(top) + len(body) + footer_height + 1`, so a separate addition double counts. render.py:438-440 shows `ledger_fixed` is the separate term that needs the +2. synth-05 step 2.2 says exactly this (`_heading_rows` used at the gate and in `ledger_fixed`, `reserved` read only). synth-02 RN-2 and the synth-01 M-10 row say the same. No instruction to edit `reserved` remains. |
| F5 | Step 4.5 dropped required text with the RETAIN pane | FIXED | synth-05 step 4.5 now relocates `run_line`, `caveat_line` and `retention_line` to the left body in P3 order when the pane is dropped, and `counts_line` when the tile is dropped, with one recompute of `base` and `capacity`. Step 4.4 and step 4.7 are consistent with it; 4.7 adds the height 24 and 26 test at 116 and 160. The literals in the test were checked against code and spec: `one Run only: {run}` view.py:794, `no read marker in source: answered questions stay listed` view.py:73, `retention reset at {hhmm}; questions observed before this start are not retained` view.py:67, spec lines 42, 44, 48 of rendering-rules.md. The step no longer contradicts its own "no fact disappears". |

Blocking findings still open from cycle 1: 0.

## Part B. Coherence after the fixes (report-qualitative checklist, adapted)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Problem statement matches findings; the story builds current state, gaps, options, recommendation, plan | PASS | synth-01 (problem, current state) feeds synth-02 (target, gaps), synth-03 (external), synth-04 (options, recommendation, Q1 to Q7 answers), synth-05 (plan), synth-06 (open questions, trail). The Q1 to Q7 list in synth-01 1.4 is answered one by one in synth-04 7.2 and carried into synth-05 8.1. No section drifted into an unrelated topic. |
| 2 | Current state is current (fix-touched claims) | PASS | Code re-read for every claim the fixes touched: render.py 62-80, 326-356, 390-531 (`ledger_fixed`, `reserved`, `body`, `_desk_lines`, `wrap`), release1_surface.py 34-62, view.py:67, 73, 99, 794, parse.py:475, 503, rendering-rules.md 42-51. All match. Claims the fixes did not touch were not re-traced (see Self-Audit). |
| 3 | Options are genuinely distinct | PASS | Option A (strings plus a style pass), B (Rich renderables), C (text model plus roles built at build time) differ in where roles come from and what breaks `test_render.py:399`; D1/D2/D3, H1/H2/H3, Z1/Z2/Z3 differ in dependencies and verified status. The qualitative-report minor note that A and C differ mainly in role assignment stands as a note only. |
| 4 | Recommendation follows from the comparison tables | PASS | 7.1 picks C, H3, D2 (via D1 floor), Z2, each the best row of its comparison table in 6.1 to 6.4. The phase list after the F1 rewrite matches the plan of record, so the recommendation and the plan no longer disagree on order. |
| 5 | Plan is actionable | PASS | Each step names files, functions and line ranges that match code (spot-checked 2.2 against render.py:438-440, 495-502; 1.6(c) against release1_surface.py:34-38). Steps are ordered so each phase's inputs exist (0.7 `strip_sgr` before 1.6(c); 2.1 records golden before 2.7 regeneration). |
| 6 | Gaps are honest | PASS | [UNVERIFIED] items are listed in synth-05 8.8 and synth-06 9.4; steps that depend on them say so (1.6(g), 6.1, 7.4). The F3 fix states the hash behaviour as "not guaranteed to appear" instead of promising it. |
| 7 | External research is relevant | PASS | synth-03 findings each name the question served and their relationship to code; synth-04 and synth-05 use them for Q1, Q3, Q4, Q5, Q6 and mark them external context. No padding found. No new web lookup was needed for this cycle (Tavily not used; no fallback needed). |
| 8 | Scale claims substantiated (adapted: width and height budget arithmetic) | PASS | 1+114+2+42+1=160, 1+70+2+42+1=116, 1+76+2+80+1=160, 1+66+2+46+1=116, inner widths 154/110/74 and 72/110/74 recomputed by hand and correct. No performance or capacity claims exist. |
| 9 | Risk assessment complete | PASS | Height crop, golden churn, NO_COLOR, ASCII, hash handling, live path without a test, Zellij unverified are each in a risk or open-item row. The cycle-1 gaps (golden strip, RETAIN pane relocation) are now covered. |
| 10 | Evidence trail complete | PASS | Glob confirmed every file named in synth-06 Section 10 exists: research 01 to 05, web-01, web-02, research-notes.md, gaps-and-questions.md and the Gate 1 QA reports. Content-level tracing back into the research files was not redone this cycle. |
| 11 | No circular reasoning | PASS | Facts cite code lines or research files; synthesis files cite each other only for plan mirroring (synth-04 7.1 mirrors synth-05, stated openly). |
| 12 | Conclusion proportionate | PASS | Confidence labels in synth-04 7.2 are Medium or High with named caveats; the plan treats owner decisions D-1 to D-8 as defaults with an "if different" column. |

### Fix-specific contradiction sweep (no fix introduced a contradiction)

- Golden assignment per phase, checked in every place it is stated (synth-02 3.8, synth-04 6.1 table, 7.1, 7.2, 7.3; synth-05 steps 1.6, 2.7, 3.9, 4.8, 5.6, 6.6, 8.9 item 13): consistent. synth-02 3.8 says "P2, P3, P4, P6" are golden-changing and synth-05 agrees.
- "Hash is whole" statements: synth-02 SC-10 and G-E, synth-04 Q7, synth-05 8.1, D-6, 0.6, 3.7, 5.5, RB-19, synth-06 row 10: all say whole by wrap, cut only by the 4-line cap or ASK_CAP. No remaining "never cut" absolute.
- `reserved`: synth-01 M-10, synth-02 RN-2, synth-05 2.2, synth-04 7.1 P2 all say it needs no edit.
- RETAIN pane drop: synth-05 4.4, 4.5, 4.7 agree; RB-17 is scored at the gate heights (48, 42, 42), where the pane is drawn, so it does not conflict with the relocation at heights 24 and 26.
- Q1 to Q7 answers against the plan: Q1 Option C and the `Line` layer (8.1); Q2 P0 to P7; Q3 H3 plus session PNG with fallback; Q4 detection plus per-depth tables (P1); Q5 `console.file.getvalue()` and D-4 default plain; Q6 not a dependency; Q7 rule per surface. All consistent.

## Part C. Issues found (all MINOR; recorded as notes, not fixed, not rechecked later)

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| 1 | MINOR | synth-05 8.1, Q2 row | Says "Seven phases" for P0 to P7, which is eight (carried from the cycle-1 analyst note, still present). The phase list itself is correct everywhere. | Say "Eight phases, P0 to P7". |
| 2 | MINOR | synth-05 8.1, Q7 row, rule (2) | The rule says a value wider than "the pane's inner width minus 2" is hard-split, then gives "62 at 116 in P5". 62 is the inner width (66-4); inner minus 2 is 60 (step 5.2 wraps the value at `inner - 2`). The conclusion (a 64-cell value splits at 116, fits at 160 and 80) is the same either way. | Write "60 at 116 (inner 62)". |
| 3 | MINOR | synth-05 step 0.6 vs steps 3.7 and 5.5 | The fixture is required to fit "under four desk lines at 80 columns", but step 5.5 asserts a whole hash in the question pane at 160 where the P5 inner width is 72, narrower than the 74 at 80. Whether the 222-character fixture still holds the hash inside line 4 at 72 was not measured (the cycle-1 measurements were at full width). The plan does say to measure and re-pin at implementation. | State the fixture size constraint at the narrowest inner width (72), and measure it in step 0.6 or 5.5. |
| 4 | MINOR | synth-02 3.5, "Frame cost, height" row | Still lists `reserved` among the terms every added row "must be counted inside". True only through `body`; it can be read as a separate addition, which is the error F4 removed elsewhere. | Say rows are counted through `top` and `body`, which `reserved` reads. |
| 5 | MINOR | synth-05 8.9 item 13 | "Both presentation goldens regenerated" for P2, P3, P4, P6; P3 and P4 regenerate only the link-off golden and P6 only the release-1 golden. | Say "the golden named in the phase". |
| 6 | MINOR | synth-04 7.1 Q4 and Q3 rows vs synth-05 1.1 and G3 | Q4 says detection comes second, after the 16-colour floor; the plan builds detection first (step 1.1) inside one phase. Q3 calls the PNG step an optional extra; the plan makes it step G3 of every gate when step 0.4 proves the route. Neither changes a decision. | Align the wording to the plan. |
| 7 | MINOR | synth-05 8.2 vs steps 5.1 and 7.1 | D-8 (desk evidence title) is used but missing from the 8.2 table; it is defined inline in step 5.1. | Add a D-8 row. |

Counts: CRITICAL 0, IMPORTANT 0, MINOR 7.

## Self-Audit

**(a) Reliance list. rf-qa PASS items skipped for structural re-check:**
- None. No `## Inherited Structural Verdict` was supplied; the review fell back to standalone behaviour. The structural report `qa-synthesis-structure.md` and the other Gate 2 reports were deliberately not read, so this review is independent of them.

**(b) Independent semantic checks (at least one required, INV-019):**
- F4 "false instruction" fix: read render.py:438-440 and 495-502 and confirmed `reserved` reads `len(body)` after the heading rows are appended; the fix is correct, not just present.
- F2 golden mechanism: read release1_surface.py:34-62 and confirmed `printed_*` is produced by `make_console` plus `render()`, so the SGR strip in `_printed` is the right point; grepped all test modules for console use to confirm no other module needs the same strip.
- F3 hash rule: read `_desk_lines` render.py:339-346 and `wrap` 62-80; the per-surface rule matches the code, including that line 4 is cut at `width - 3` and later lines are dropped.
- F5 literals: matched three required lines against view.py:67, 73, 794 and rendering-rules.md lines 42, 44, 48.
- F1 labels: grepped the synthesis files for phase labels and for "seven/eight phases" and read each remaining old label to confirm it is marked as a research label.
- Arithmetic: recomputed all column widths and inner widths by hand.

Factual claims independently verified against source this cycle: 22 (the five fixes' code claims, nine view/parse/render/spec literals and line numbers, eight width sums). Files read: the six synthesis files, the two QA input files, render.py, release1_surface.py, rendering-rules.md, plus greps of view.py, parse.py and tests/observe. Not re-verified: research files 01 to 05 and web files (their content), code claims the fixes did not touch, the PNG route and Zellij behaviour (marked [UNVERIFIED] in the synthesis itself).

If I told the user I found 0 blocking issues, the evidence is Part A (each fix traced to code) and the contradiction sweep in Part B; the seven minor notes show the files were read closely enough to find defects.

Web research: none performed (no Tavily call, no fallback).

## Confidence Gate

- Checklist items: 5 fix checks (F1 to F5) + 12 report-qualitative checks = 17.
- VERIFIED with tool evidence: 17. UNVERIFIABLE: 0. UNCHECKED: 0.
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 15 | Grep: 7 | Glob: 4 | Bash: 0 (Read + Grep + Glob = 26, at least the 17 items)
- Scope note: items 2 and 10 were adapted (code claims touched by the fixes; evidence-trail file existence), as stated in their rows. Remaining risk that could hide an undetected issue: claims in the synthesis that the fixes did not touch and that were not re-traced to code or research this cycle.
