# Synthesis Accuracy Review (Synthesis Quality Review)

**Date:** 2026-11-17
**Status:** Complete
**Topic:** Observer visual-parity investigation (issue #606)
**Fix authorization:** false (report only)

**Method:** read all six synthesis files in full (synth-01 to synth-06), all seven research files (01 to 05, web-01, web-02) and `gaps-and-questions.md`; traced claims back to research; spot-read code and tests under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/` (terminal.py:18-135, render.py:1-50, 94-135, 155-250, 296-387, 422-531, commands.py:196-280, view.py constant lines, test_render.py:248-259, 394-404, 608-625, test_terminal.py:100-117, 178-199, test_commands.py:112-129, 745-773, release1_surface.py:20-62, rendering-rules.md:13-74, render_current.py:30-94, pyproject.toml:41). No web research was needed or done.

Finding IDs: B-nn = blocking, M-nn = minor.

---

## Checklist item 1: report section headers match the Report Structure (10 sections across six files)

**Result: PASS.**

| File | Sections found (grep of `##` headings) | Expected |
|---|---|---|
| synth-01 | `## 1. Problem Statement`, `## 2. Current State Analysis` | 1, 2 |
| synth-02 | `## 3. Target State`, `## 4. Gap Analysis` | 3, 4 |
| synth-03 | `## 5. External Research Findings` | 5 |
| synth-04 | `## 6. Options Analysis`, `## 7. Recommendation` | 6, 7 |
| synth-05 | `## 8. Implementation Plan` | 8 |
| synth-06 | `## 9. Open Questions`, `## 10. Evidence Trail` | 9, 10 |

All ten sections are present once, in order, with sub-numbering (1.1-1.6, 2.1-2.8, 3.1-3.8, 4.1-4.5, 5.1-5.6, 6.0-6.4, 7.1-7.4, 8.1-8.10, 9.1-9.6). The task file's own Report Structure template was not read (instructed not to); the check is against the numbered 1-10 list given in the review prompt. Note: see M-14 (section 8 places unnumbered `### Phase N` headings between 8.7 and 8.8).

## Checklist item 2: table column structures

**Result: PASS.**

- Gap tables (synth-02 4.1a, 4.1b, 4.1c): header row is `Gap | Current State | Target State | Severity | Notes` in all three tables, 18 + 12 + 4 rows. Severity values are Critical / Important / Minor as the file's own scale defines.
- Options tables (synth-04 6.1-6.4): per-option `Assessment` tables (Effort, Risk, Reuse, Files, Pros, Cons) plus a comparison table per decision with `Criterion | <option> | <option> | <option>` (A/B/C, H1/H2/H3, D1/D2/D3, Z1/Z2/Z3).
- Plan tables (synth-05 Phases 0-7): `Step | Action | Files | Details` in every phase.
- Remediation table (synth-02 4.2) and rubric table (synth-05 8.4) are extra, correctly formed.

## Checklist item 3: fabrication beyond research content

**Result: PASS (no fabricated findings; one inherited false code claim is logged under item 6 as B-01).**

Traced and confirmed against research and code (sample):

| Synthesis claim | Research source | Code or file check |
|---|---|---|
| `make_console` builds `color_system=None if no_color else "standard"` (terminal.py:121) | 01 section 1 | terminal.py:114-125 read: exact |
| Four width classes (terminal.py:63-70) | 01 section 1 | terminal.py:63-70 read: full, line, short, narrow |
| GLYPHS has three names (terminal.py:30-34) | 01 | read: `selected`, `truncate`, `hrule` only |
| `render()` is one `Text(no_wrap=True, overflow="crop")` per line (render.py:524-531) | 01 section 3 | render.py:524-531 read: exact |
| Header gate `width_class == "full" and view.visible_rows` at render.py:497; mirrored at :439 | 01 4.3 | render.py:439, 497 read: exact |
| `_help_lines` clips when questions off (304-308) | 01 4.5 | read: exact |
| M-05 counts line is render.py:373, not 374 (synth-02 corrects 04) | 04 vs 01 | render.py:373 is `wrap(panel.counts_line)`: correct |
| `POLICY FROZEN unavailable (no source)` (view.py:948) vs RR 20 `FROZEN unavailable ...` | 01 | view.py:948 and RR line 20 read: both as stated |
| `DESK_TEXT_LINES = 4` (view.py:99), `QUESTIONS_TITLE = "COORDINATOR QUESTIONS"` (view.py:53), `DESK_TITLE` (:85), `FROZEN_MARKER` (:106) | 01 section 5 | grep: exact lines |
| No `READ ONLY` / `count_figure` / `RETAIN` text under `src/superclaude/cli/observe/` | 01 | grep: no match |
| Both gates True, single-line, `# fmt: skip`; tests at test_commands.py:747-756 and 762-772 | 02 section 4, 03 4d | commands.py:67, 70 and test_commands.py:745-773 read: exact |
| `export.py` imports no Rich (export.py:11-18) | 02 section 5 | grep of imports: json, os, tempfile, Path, Any, sanitize, view types |
| 766-test baseline, 28 Python files, 22 test modules, 2 goldens | 03 section 7 | `ls`: 28 `.py`, 22 `test_*.py`; golden JSON files hold no ESC (grep count 0) |
| `inputs/current/` holds 0 ESC bytes; mockup `signal-bridge.ansi` has 48 ESC lines | 04, 05 | Bash check: 0 files with ESC in `current/`; 48 in the mockup |
| RR has 107 lines | 04 gap MINOR-3 | `wc -l`: 107 |
| `.dev/issues/606/issue-body.md:84` lists the four presentation files | 03 4a | sed line 84: exact |
| `render_current.py` HEIGHT = 50 (:38), `main()` at line 93 with no guard | 04, 05 | read: exact |
| `pexpect>=4.9` at pyproject.toml:41; `ASK_CAP = 400` at parse.py:475 | 02, 05 | grep: exact |
| No test references `LiveScreen` or `run_interactive` | 02 9.3, 03 | grep of `tests/observe`: only `spike_child.py:64` raw `Live(` |

Invented content (theme table, `Line` layer, `_frame`, `_two_columns`, `_count_tile`, `_BIG` font, RB rubric, D-1 to D-8) is plan design, labelled as plan or default, and does not claim to come from research. No research file was found to contain an invented claim. Mockup colour and geometry tables in synth-01 2.4 and synth-02 3.2 match research 04 sections 2 to 4 cell by cell.

## Checklist item 4: findings cite real file paths and evidence

**Result: PASS (minor citation drifts only).**

Every finding row carries a `file:line` or a research-file section. Research-file line cites in synth-04 (`R01:44-52`, `R03:36`, `R03:204`, `R04:63-76`, `R05:49-68`, `R02:197-198` and about 40 more) were checked against the research files and all resolve to the stated content. GAPS-row cites in synth-04 (rows 1 to 14, 25, 26, 29, 32, 34-42, 54) resolve to the stated gaps.

Minor drifts (moved line numbers on true claims): see M-05 and M-07.

## Checklist item 5: options analysis has at least 2 options with pros and cons tables

**Result: PASS.**

Four decisions are analysed: Q1 composition (3 options A, B, C), Q3 harness (H1, H2, H3), Q4 colour depth (D1, D2, D3), Q6 Zellij (Z1, Z2, Z3). Each option has an Assessment table with Pros and Cons rows, and each decision a comparison table. Option B (Rich renderables) states its cons with research evidence (test_render.py:399, rendered line counts, `safe_box`). External context is labelled with URLs.

## Checklist item 6: implementation plan has specific steps with file paths

**Result: FAIL (2 blocking findings in plan steps; steps are otherwise specific, with files, line anchors, test names and goldens per phase).**

### B-01 (blocking): the plan and gap tables tell the implementer to add heading rows to `reserved`, which already counts them

- Where: synth-05 step 2.2 (line 192): "use it at the three places that today test `policy.width_class == "full"` (lines 439, 497 and the `reserved` sum)". synth-02 RN-2 (line 202): "add the 2 heading rows to `ledger_fixed` (:438-440) and `reserved` (:499-501)". synth-01 2.4 map row M-10 (line 312) lists `:499-501` as a height term to change.
- Evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/render.py:495-502`. `body = wrap(view.ledger_title...)` (495); the heading rows are appended to `body` at 497-498; then `reserved = len(top) + len(body) + footer_height + 1` (499-501). `reserved` has no `width_class` test and reads `len(body)`, so once the gate at 497 is relaxed, `reserved` counts the heading rows automatically. Only `ledger_fixed` (438-440, computed before `body` exists) holds a second, separate copy of the `full` test. The statement that `reserved` must be edited or has a third "full" test is false; following it literally double-counts 2 rows and removes two ledger rows at 116 and 80.
- Origin: inherited from research 01 section 8.1 row M-10 (line 195), which says "also the height terms ledger_fixed 438-440 and reserved 499-501 (+1 or +2 line)". The synthesis repeated it without checking `reserved`.
- Required fix: say that only `ledger_fixed` (438-440) and the gate at 497 change; `reserved` needs no edit (it reads `len(body)`). Correct synth-01 2.4 (M-10), synth-02 RN-2 and synth-05 2.2.

### B-03 (blocking): phase 1 and phase 2 golden handling conflict, so step 2.7 as written breaks T47

- Where: synth-05 step 1.6(c) (line 170): T47 is changed to "compare `strip_sgr(current[variant][key])` for the `printed_*` keys; the golden file bytes do not change". Step 2.7 (line 197) and step 6.6 (line 332): "Regenerate both presentation goldens from the current tree", with the release-1 golden produced by `json.dumps(surface(), ...)`, and 6.6 expects the diff to include `printed_*`.
- Evidence: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/release1_surface.py:34-38, 60`: `_printed` prints `render(view, policy)` through `make_console(policy, ...)` with `resolve_policy({}, ...)`, i.e. the `"standard"` colour system. After phase 1 styles exist, so `surface()["printed_*"]` contains ESC bytes. A golden regenerated from `surface()` in phase 2 therefore holds ESC bytes, while the phase 1 T47 compares `strip_sgr(current)` (no ESC) with the golden (ESC): the test fails. Step 2.1 lists `T/release1_surface.py` among its files but its Details never say what changes there.
- Required fix: state one consistent rule, for example make `_printed` (or the golden writer) strip SGR so `printed_*` stay plain text, or keep T47 comparing raw bytes and regenerate with ESC included, and apply the same rule in 1.6(c), 2.7 and 6.6.

Other plan statements checked and found correct: the width arithmetic (1+114+2+42+1 = 160; 1+70+2+42+1 = 116; 1+76+2+80+1 = 160; 1+66+2+46+1 = 116; inner width = width - 6 gives 154/110/74; Phase 5 inner widths 72/110/74 and 62), the `resolve_policy(env, "utf-8", {"ascii": ...}, width, height)` signature, `make_console(policy, file=io.StringIO(), record=True)`, `_emit`/`run_once`/`LiveScreen` line anchors (commands.py:200-279), `counts_lines` cut path (render.py:127-132), the source-scan constraints (test_render.py:400-404, test_terminal.py:181-198) and the 16-colour table (eight distinct named colours, so RB-09 can pass). Other plan defects are minor: M-01, M-02, M-04, M-13.

## Checklist item 7: cross-references between sections are consistent (gaps in Section 4 addressed in Section 8)

**Result: FAIL (1 blocking cross-section contradiction, several minor mismatches).**

Gap-to-plan coverage is good: every Section 4 row has a home in Section 8 (M-01 to M-18 in the 8.10 map; RN-1 to RN-3 map to steps 1.4, 2.2, 2.3; G-1 to P3; Q4/G-2 to P1; Q5 to steps 1.5, 1.6; G-F to step 1.6(g); G-G to steps 0.7, 3.8; G-A to D-2; Q7 to steps 0.6, 3.7, 5.5; Q6 to step 7.4; G-H to step 7.1; O-1 to D-1; OPEN-1 to OPEN-3 to D-3). The defect is between Sections 3, 7 and 8.

### B-02 (blocking): three incompatible phase schemes and two incompatible orders use the same labels P0 to P5

| Where | Scheme |
|---|---|
| synth-02 3.8 (Q2 row, line 132) | P0 tests; P1 style; P2 text; P3 width-gated 160 layout; P4 boxed panes; P5 optional Rich renderables |
| synth-04 7.1 "Recommended sequence" (lines 321-329) and 7.2 Q2 answer (line 354) | P0 tests; harness step; P1 style; P2 text; P3 additive two-column layouts (160, then 116); P4 boxed panes and count tile as hand-built lines; optional Z2 |
| synth-05 Phases 0 to 7 | P0 harness and tests; P1 style and colour depth; P2 text and budget; P3 single-column frames; P4 two-column questions, tile, RETAIN; P5 Decision Desk two columns; P6 ledger panes; P7 spec and PR |

The order differs, not only the labels: section 7.1 puts two-column layouts (step 5) before boxed panes (step 6); the plan puts frames (P3) before two columns (P4, P5). Section 7.2 Q2 says P4 touches the whole-line tests and both goldens; in the plan those whole-line tests are touched in P3 and the golden list is split across P2, P3, P4 and P6. The plan's 8.1 Q2 row says the plan is "03 section 6 with P2 and P6 added", but it does not tell the reader that 7.1 and 7.2 use the older numbering, and `P3` and `P4` mean different things in the two sections. A reader of the assembled report who follows 7.1 reaches a different build order from 8.
- Required fix: either renumber 7.1 and 7.2 Q2 to the Section 8 phases, or add an explicit mapping note and state that Section 8 supersedes the 7.1 order; align synth-02 3.8 the same way.

### Minor cross-reference mismatches

- M-01: synth-05 8.1 Q2 row (line 10) says "Seven phases" but lists P0 to P7 (eight).
- M-02: D-8 is referenced in Phase 5 dependencies (line 282), step 5.1 (line 301), 8.8 and checklist row 15 ("D-1 to D-8") but the 8.2 decision table lists D-1 to D-7 only.
- M-03: the owner-decision lists differ: synth-04 7.3 lists a PNG-dependency decision, bold/dim survival under NO_COLOR and the RR 61 wording as decisions; 8.2 has none of them (D-7 appears only in 8.2). 8.8 lists the NO_COLOR bold item as "excluded", not as a decision.
- M-08: synth-04 7.1 Q3 says image-to-image comparison "is not part of the gate" and Q-7 is "closed as no for the gate"; synth-05 G3/G4 make the Playwright-rendered PNG the default reviewer input (falling back to text and ANSI only if step 0.4 fails).
- M-09: Q6 headline differs: synth-04 7.2 says "Conditional go as an optional layout"; synth-05 8.1, synth-01 2.5, synth-06 row 16 say "no-go as a dependency; optional manual check". The substance is the same; the label is not.
- M-10: severity scales differ without a bridge. synth-02 grades M-08, M-10, M-11 Critical (C8 defects); synth-05 8.10 column "Severity per FINDINGS" and rubric RB-11, RB-12, RB-13 say Medium. The gate treats High and Medium alike, so no phase outcome changes, but the report shows two severities for the same item.

## Checklist item 8: no doc-only claims in Sections 2, 6, 7 or 8

**Result: PASS (minor untagged items).**

- Section 2 states code facts with `file:line` and [CODE-VERIFIED], spec facts as "spec says" with RR line numbers (RR lines 17, 20, 25, 41, 43, 57, 61, 70 re-read at `rendering-rules.md:13-74`: content as quoted), and moves every unverified item to 2.7. Web material is kept out of Section 2.
- Sections 6, 7 and 8 label every web-sourced statement "external context" with a URL, and 8.8 lists the unverified items with handling.
- M-11 (minor): untagged items that rest on a document header or on a second-hand report: synth-01 2.5 "Provenance: provisioned from `/etc/skel`" (taken from file headers, research 05 section 1.2; not tagged); synth-01 2.5 "Both Gate 1 QA reviewers read mockup PNGs successfully" (taken from gaps-and-questions row 40; the QA reports were not re-read here); synth-05 step 0.4 names the tool `browser_take_screenshot`, which no research file lists (the route is flagged [UNVERIFIED] in 8.8, the tool name is not).

## Checklist item 9: stale documentation discrepancies are surfaced

**Result: PASS.**

Every `[CODE-CONTRADICTED]` and `[STALE DOC]` item in research files 01 to 05 appears in synth-02 4.3a or 4.3b (width classes, `safe_box`, `FROZEN` token, M-10 location, 153 cells, slack arithmetic, RR 61 vs RR 42, RR 37-41 and 60-61, RR 33, RR 38 title, RR 59, `render_current.py` docstring, three stale `.dev` review notes, the Zellij header notes, the `attachments/` note) and, again, in synth-06 9.5 and the corrected-claims table C1-C8. Research 02 reported none; the synthesis says so. Spot checks: RR line 20 reads `FROZEN unavailable (no source)` and view.py:948 reads `POLICY FROZEN ...`; RR line 61 does list the two 80-column invariant lines and RR line 42 conflicts with the first.

## Checklist item 10: key finding coverage (research Key Takeaways reflected in synthesis)

**Result: PASS (two minor omissions).**

Research 01 (terminal, call chain, render sections, view facts, consumers, colour depth, per-finding map, Q7 probe), 02 (paths, export_text probe, LiveScreen, gate regexes, screen-only proof, section 9 live trace), 03 (assertions at risk, goldens, 64-hex fixture, phase table, baseline), 04 (RR citations, palette, 16-colour downgrade, geometry, M-01 to M-18, harness, Q7), 05 (Zellij, offline tools, pyproject, harness options, reviewer, Q6), web-01 and web-02 are all carried, with the research disagreements resolved in 4.3a and 8.6. Omissions:

- M-12 (minor): research 02 Key Takeaways "key handling is independent of rendering and styling; only `n`, `p`, `escape` affect the desk" and the exact desk join (`raw.dispatch_id == line.dispatch_id`, view.py:838-842) are not carried; research 04 notes that the mockups draw a `7/7 lines shown` counter in every pane and that RR 26 shows inspector text untruncated while the desk cuts it. None changes an option, but they are research takeaways with no synthesis home.
- Related minor inconsistencies in how the same finding is tagged: M-06 synth-03 tags `test_render.py:399` and `safe_box` as [UNVERIFIED in this synthesis] (5.1.2, 5.1.3, 5.2.6) while synth-01 and synth-02 verify them (test_render.py:399 read; probe reproduced by two reviewers).

## Additional checks required by the prompt

### Direct answers Q1 to Q7 in synth-04 7.2

| Q | Supported by research? | Note |
|---|---|---|
| Q1 | Yes (01 section 8.2, 03 section 6, W01 H, R02 section 5) | Option C is consistent with test_render.py:399 and the source guards (read) |
| Q2 | Yes for the per-phase test and golden impact (03 sections 4, 6) | Phase labels contradict Section 8 (B-02) |
| Q3 | Yes (05 sections 2 to 6, W02 B1-B7) | image-gate wording conflicts with plan (M-08) |
| Q4 | Yes (01 section 7, 04 section 3) | consistent with `terminal.py:121` (read) |
| Q5 | Yes (02 sections 2 and 9) | consistent with commands.py:238-245 (read) |
| Q6 | Yes (05 section 7, W02 A1-A7) | label differs across sections (M-09) |
| Q7 | Yes (01 4.9, 03 5c, 04 section 8) | measured values reproduced from research; synthetic fixture only |

### Plan closes every finding M-01 to M-18

The 8.10 map names a closing phase, steps and rubric row for all 18 findings (M-17 is marked optional and has step 2.6). M-02 and M-09 close in two parts (P3 then P6; P1 then P5), stated. Two step-level defects touch closing steps: B-01 (M-10, step 2.2) and B-03 (golden handling in steps 1.6, 2.7, 6.6). Minor plan notes:

- M-04: synth-05 step 1.4 says the liveness verdict (`_verdict`) exists "in all layouts"; code shows `_verdict` only in the `line` layout (render.py:209), the `full` layout uses `r.liveness` (:188) and the `short` layout has no liveness column (:223-229). synth-02 M-09 row says "at 116 and 80 only the liveness verdict ... can be coloured"; only 116 is right (synth-01 2.4 has it right). Inherited from research 01 8.1 row M-09.
- M-13: step 3.3 does not say where the desk frame sits relative to the retention line. Today `_panel_lines` inserts the desk lines (render.py:383) before the empty/window-full texts, notes and retention line (:384-387); the plan frames the list body "including retention" and calls the desk "a separate frame", which leaves its position (inside the list frame, after it, or between the rows and the retention line) undecided.

### Minor citation drifts

- M-05: synth-05 step 3.6 cites `T/test_commands.py:672-675` and `:690`; the assertions are at lines 671, 673-674 and 691 (grep). synth-01 header cites the source guard as test_render.py:396-403; it is 396-404.
- M-07: synth-06 row 39 says the guard test is "now :747-760"; synth-02 4.3a/4.3b and SC-16 say 747-756, which matches the file (test ends at 756).
- M-14: synth-05 puts unnumbered `### Phase 0 ... Phase 7` headings between `8.7` and `8.8`, so 8.8 to 8.10 follow the phases; RB-07 is "in scope from P3" in 8.4 but phase 1 scores "RB-05 to RB-11".

## Issues Requiring Fixes

| # | Severity | File and place | Check | Issue | Required fix |
|---|---|---|---|---|---|
| B-01 | Blocking | synth-05 step 2.2; synth-02 RN-2; synth-01 2.4 M-10 row | 6 | Says `reserved` (render.py:499-501) must gain the heading rows; it reads `len(body)` and already counts them | Only `ledger_fixed` (438-440) and the gate at 497 change |
| B-02 | Blocking | synth-02 3.8; synth-04 7.1 and 7.2 Q2; synth-05 Phases 0-7 | 7 | Three phase numbering schemes; 7.1 builds two columns before frames, the plan builds frames first | Renumber or add a mapping and state the plan supersedes 7.1 |
| B-03 | Blocking | synth-05 steps 1.6(c), 2.1, 2.7, 6.6 | 6 | T47 strips SGR in phase 1 but phase 2 regenerates `printed_*` from `surface()` with ESC bytes | One rule for `printed_*` in the golden and in T47, applied in all four steps |
| M-01 | Minor | synth-05 8.1 Q2 | 7 | "Seven phases" for P0-P7 | Say eight |
| M-02 | Minor | synth-05 8.2 | 7 | D-8 used but not in the decision table | Add D-8 |
| M-03 | Minor | synth-04 7.3 vs synth-05 8.2 | 7 | Decision lists differ | Align |
| M-04 | Minor | synth-05 1.4; synth-02 M-09 | 6 | `_verdict` "all layouts" / "116 and 80" | Say `line` layout only |
| M-05 | Minor | synth-05 3.6; synth-01 header | 4 | Line drifts (671/673-674/691; 396-404) | Correct |
| M-06 | Minor | synth-03 5.1.2, 5.1.3, 5.2.6 | 10 | [UNVERIFIED in this synthesis] for facts verified in synth-01/02 | Retag with the verifying source |
| M-07 | Minor | synth-06 row 39 | 4 | 747-760 vs 747-756 | Use 747-756 |
| M-08 | Minor | synth-04 7.1 Q3 vs synth-05 G3/G4 | 7 | Image gate "not part of the gate" vs plan default | Reword one |
| M-09 | Minor | synth-04 7.2 Q6 vs 8.1, synth-01, synth-06 | 7 | "Conditional go" vs "no-go" | One label |
| M-10 | Minor | synth-02 4.1a vs synth-05 8.10, 8.4 | 7 | C8 defects Critical vs Medium | Add a bridge sentence |
| M-11 | Minor | synth-01 2.5; synth-05 0.4 | 8 | Untagged header-sourced, second-hand and tool-name claims | Tag |
| M-12 | Minor | synth-01 to 06 | 10 | Research 02/04 takeaways not carried | Add one line each or list as excluded |
| M-13 | Minor | synth-05 3.3 | 6 | Desk frame position undecided | State it |
| M-14 | Minor | synth-05 headings; 8.4 RB-07 | 7 | Unnumbered phase headings inside section 8; RB-07 scope | Format |

## Summary

**Status:** Complete

| Measure | Count |
|---|---|
| Synthesis files reviewed | 6 |
| Research files read | 7 (plus gaps log) |
| Checklist items passed | 8 of 10 (items 6 and 7 failed) |
| Blocking findings | 3 (B-01, B-02, B-03) |
| Minor findings | 14 (M-01 to M-14) |
| Q1 to Q7 answers supported by research | 7 of 7 (labels inconsistent for Q2, Q6) |
| Findings M-01 to M-18 with a closing step in the plan | 18 of 18 |

**VERDICT: FAIL** (3 blocking findings; fix B-01 to B-03 before assembly, minor findings are notes).
