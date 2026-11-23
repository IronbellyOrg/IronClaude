# QA Report - Phase 6 report validation, fix verification (Gate 3, fix cycle 1)

**Topic:** Observer visual-parity investigation (issue #606)
**Date:** 2026-11-17
**Phase:** fix-cycle
**Fix cycle:** 1 (verifying the cycle-1 fixes; F_1 was 10)
**Fix authorization:** false (report only; no other file modified)
**Report under review:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md
**Inputs read:** qa/qa-consolidated-findings-phase6.md (27 lines), qa/qa-fix-log.md (15 lines), the whole report in ranges (lines 1-1905).

Note: this path previously held a different summary (a structural check of the task file's cycle-2 fix items). It was replaced because the prompt names this path as the output.

---

## Section A - Re-verification of the 10 blocking findings

| # | Finding | Result | Evidence |
|---|---|---|---|
| 1 | Rubric rows RB-01, 04, 14, 16, 17, 22 lacked measurable anchors; SC-14 and Section 9 stale | FIXED (but see N1) | Section 8.4 lines 1388, 1391, 1401, 1403, 1404, 1409 now carry pass/fail anchors with a checker; SC-14 (line 568) points at 8.4 and 8.5; Section 9 row 15 (line 1812) says the rubric is drafted in 8.4; grep for "NOT yet defined", "not drafted", "rubric is not" finds nothing. |
| 2 | Phase 0 harness contract inconsistent (passes, depth selector, file names, `--check`) | FIXED | Step 0.3 (line 1464) is the single contract: command, five passes, `--depth`, per-depth file names, `--check` writes `checks.json`. G2 (line 1419) and step 7.3 (line 1681) refer to it, include `--check` and five passes; grep for "four passes" finds nothing. Step 0.6 anchor now "after line 967": re-read tests/observe/test_render.py:958-967, the test starting at :958 ends at :967. |
| 3 | RB-10 / SC-6 depend on a non-existent `STATE_ROLE` table | FIXED (minor imprecision, see note M1) | Step 1.4 (line 1494) gives a minimum non-empty table. I checked its inputs against code: fixtures hold workerState running/idle/blocked/exited/succeeded/failed/ready/stopped/abandoned, dispatchStatus active/blocked/completed/failed/dispatched, liveness verdict alive/live/ended/exited/unverifiable (grep over `src/superclaude/cli/observe/fixtures`); `view.py:509` builds `"{verdict} ({source})"`; `render.py:151-152` `_verdict` reads `row.raw.liveness_verdict`; `view.py:106` `FROZEN_MARKER = "FROZEN"`. D-7 is defined in 8.2 (line 1363); RB-10(d) forbids an empty table. |
| 4 | D-8 undefined; 7.3 / 9.1 omit D-7, D-8; id-less owner decisions | FIXED | 8.2 now holds D-1 to D-12 (lines 1357-1368). 7.3 lists O-1 (D-1), OPEN-1 to 3 (D-3) plus D-7, D-8, D-2, D-5, D-12, D-6, D-10, D-11, D-4, D-9 = the full set of 12; 9.1 lists D-7 and D-8 and its closing paragraph maps every D-id to a row (rows 5, 6, 7, 8, 10, 14, 15 in 9.2 checked). No remaining "D-1 to D-8". |
| 5 | Open `--once --width` box-line question had no decision id | FIXED | D-9 (line 1365) states default yes and the effect if no; step 3.6 (line 1549) is marked as depending on D-9; Phase 3 Dependencies cites D-9; 4.1b, 7.3, 9.2 row 8 cite it. |
| 6 | Hash contradiction (5.1.5 / 5.6 vs 2.3, 3.8, 4.1b, 7.2, 8.1) | FIXED | 5.1.5 (line 781) and the 5.6 Q7 row (line 889) now say the earlier claim is superseded. I re-ran the fixture through `r3_rows` / `r3_screen` (probe below): hash whole and last at 160/116/80. `DESK_TEXT_LINES = 4` view.py:99, `ASK_CAP = 400` parse.py:475, cut applied parse.py:503 all confirmed. grep for "silently clipped" / "clipped today" leaves only the deliberate superseded notes. |
| 7 | Section 2.5 environment facts without proving commands | FIXED | Two proving-command tables added (lines 361-371, 384-395). I re-ran: `zellij --version` -> `zellij 0.44.2`; `command -v zellij` -> `/usr/local/bin/zellij`; `zellij setup --check` -> version 0.44.2, config dir, "Well defined."; `command -v` for the 12 tools -> none found; node `/usr/local/bin/node`, npx, `v24.22.2`; `ls ~/.cache/ms-playwright` -> No such file; `fc-list` -> four DejaVu Sans Mono files; `uv --version` 0.11.8, Python 3.10.20, rich 15.0.0; import of PIL, cairosvg, pyte, playwright, fontTools -> ModuleNotFoundError. All match. |
| 8 | Colour-depth and `export_text` probes lacked arguments and caveats | FIXED | Lines 173 and 220 now give the Console arguments and both caveats. Re-measured: one process per depth gives `1;91`, `1;38;5;208`, `1;38;2;255;136;0`; the same Text in one process prints `1;91` for all three depths (caveat 1 confirmed); `export_text()` then `export_text(styles=True)` gives `'hello\n'` then `''` (caveat 2 confirmed); `color_system="auto"` on a StringIO gives `None` and plain `x`. |
| 9 | Q7 fixture not in the report; "4 desk lines" claim did not reproduce | FIXED | Fixture text added (line 275); I rebuilt it: 222 characters; desk text lines 2 / 3 / 3 at 160 / 116 / 80, cell widths [157, 64], [85, 71, 64], [78, 78, 64], hash whole and last, all lines within width. Matches the report exactly. The "4 desk lines" claim is withdrawn (line 277); the four-line case is pinned by the `"word " * 200` test at :958-967. |
| 10 | "12-column" / "4-column" / "3-column" ledger counts | FIXED | `render.py:166-178` has 11 names, `:197-204` 6, `:216-222` 5; the report (2.1 line 144, 2.4 lines 317-319) says 11 / 6 / 5. grep for "12-column", "4-column", "3-column" finds nothing. `SEPARATOR = " "` (render.py:45) so 2+114+22+12+10 = 160 holds. |

Result: all 10 original blocking findings are fixed.

## Section B - New issues introduced by the fixes (adversarial pass)

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| N1 | IMPORTANT (blocking) | Section 8.4 RB-01(c) (line 1388) against step 1.4 (line 1494), RB-16(a) (line 1403) and Section 3.2 | The new RB-01 anchor says "every question age and every question-text line **in the list and in the desk** is amber", and one counter-example fails the row. Step 1.4 builds the list question line as age `attention` bold, subject `body_bold`, tail `muted`, and RB-16(a) requires every list question row line to carry bold `body_bold`. Research 04 line 57 (the source of the palette) says question text is "amber bold in desks, base bold in the 160 ledger". So a P1 built exactly as the plan says fails RB-01(c) on every list row; RB-01 is High and in scope from P1, so the phase can never close (G6 stops after 3 iterations). RB-01(c) and RB-16(a) also conflict with step 1.4's `selected` role for the selected row. This gap was introduced by fix F1. | Change RB-01(c) to: question ages (list and desk) and desk question-text lines are amber; list question subject text is base and bold (consistent with RB-16(a) and 3.2); say explicitly how the selected row is scored (its marker/line carries the `selected` role, and RB-16(a) excludes it or accepts it). |

## Section C - Minor notes (not rechecked later, no fix pass triggered)

| # | Location | Note |
|---|---|---|
| M1 | Step 1.6(e) (line 1496), RB-10(d) (line 1397), SC-6 (line 560) | They say `T/test_theme.py` asserts `STATE_ROLE` "contains the keys `running`, `succeeded`, `failed`, `completed` and `FROZEN`", but step 1.4 defines `STATE_ROLE` as `dict[tuple[str, str], str]` keyed by `(field, value)`, and the `FROZEN` flag is described outside the dict. Shorthand; an implementer will reconcile. |
| M2 | Step 3.6 / D-9 (lines 1365, 1549) | `T/test_commands.py:672-675` and `:690`: the `COORDINATOR QUESTIONS` whole-line assertions are at :671 and :691 (read at lines 664-691); :690 is the `cell_len` check. Off by one on a true claim. |
| M3 | Step 0.8 (line 1469) | "Expected: RB-01 to RB-04 and RB-10 to RB-18 FAIL; script rows pass" overlaps: RB-13, 14, 16, 17 are script rows that are expected to fail at baseline. Wording. |
| M4 | RB-04(c) (line 1391) | The tile inner width is 38 at 42 cells, so the 67-character `counts_line` wraps; the check needs `panes_flat` (whitespace-collapsed), not a single-line match. Say so. |
| M5 | 5.1.3 (line 779) and 5.6 vs 2.1 / 3.4 | 5.1.3 still says the `safe_box` probe was "not re-probed" while 2.1 and 3.4 cite a probe; it is labelled external context, so not contradictory. Also "Seven phases" for P0 to P7, test-line cites (:747-760 vs :747-756 in row 39), and remaining original minor findings from the consolidated list. |

## Section D - Structure, tables and Table of Contents

| Check | Result | Evidence |
|---|---|---|
| 10 sections present, in order | PASS | grep `^## ` returns Table of Contents, 1. Problem Statement (25), 2. Current State Analysis (105), 3. Target State (482), 4. Gap Analysis (610), 5. External Research Findings (765), 6. Options Analysis (939), 7. Recommendation (1242), 8. Implementation Plan (1322), 9. Open Questions (1781), 10. Evidence Trail (1872). |
| ToC links match headers | PASS | Lines 12-21 anchors `#1-problem-statement` ... `#10-evidence-trail` match the ten headers. |
| Tables intact | PASS | Read in full from line 1 to line 1905: no broken pipe rows seen in the edited areas (2.1, 2.3, 2.4, 2.5, 3.6, 8.2, 8.4, 7.3, 9.1). 8.2 now has 12 rows D-1 to D-12; 8.4 has RB-01 to RB-23. |
| Source files untouched | PASS | `git status --short` for `src` and `tests` prints nothing; the report is the only untracked path listed. |

## Confidence

Checklist items: 10 original findings + 4 structure checks + the new-issue pass (adversarial reading of every edited region) = 15 verified items, 0 unchecked, 0 unverifiable.
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 16 | Grep: 8 | Glob: 0 | Bash: 7 (read-only probes and version commands; no tavily or web use)
- Probes re-run read-only with `uv run python -I -B -c`; no code, record or golden script was run.

## Summary

- Original blocking findings fixed: 10 / 10
- New blocking issues introduced: 1 (N1)
- Remaining blocking count: 1
- Minor notes: 5 (not rechecked)
- Count check: F_1 = 10, now 1, so the count shrinks strictly (no monotonicity halt). One more fix cycle is allowed (cycle 2 of 2).

## Recommendations

- Fix N1 in Section 8.4 (RB-01(c), and the selected-row wording in RB-16(a)) so the rubric matches step 1.4 and the mockups, then run the cycle-2 verification. Fix M1 and M4 only if editing the same rows.

## Overall Verdict: FAIL

Remaining blocking findings: 1 (N1).

## QA Complete
