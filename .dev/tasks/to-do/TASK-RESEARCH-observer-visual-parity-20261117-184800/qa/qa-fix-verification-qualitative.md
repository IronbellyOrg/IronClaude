# QA Report - Report Qualitative (Gate 3 fix verification, cycle 1)

**Topic:** observer visual-parity investigation, report after Phase 6 report-validation fixes
**Date:** 2026-11-18
**Phase:** report-qualitative (fix-cycle verification)
**Fix cycle:** 1
**Stance:** adversarial; fix_authorization false (only this report is written)
**Report under review:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md (1918 lines at review time; the findings file says 1877 before fixes)
**Inputs read:** qa/qa-consolidated-findings-phase6.md (10 blocking findings F1-F10), qa/qa-fix-log.md
**Inherited Structural Verdict:** none in the spawn prompt; standalone behaviour applied

## Overall Verdict: FAIL (1 blocking, 6 minor notes)

Remaining blocking count: 1 (N-1, introduced by the F1 fix). All ten Gate 3 findings F1 to F10 are applied; nine are fully resolved and F1 is resolved except for one wrong anchor (RB-01(c)) that it introduced.

## Items Reviewed

### A. Verification of the ten Gate 3 blocking findings (fix verification)

| # | Finding | Result | Evidence |
|---|---|---|---|
| F1 | Rubric rows without a measurable anchor; SC-14 and Section 9 stale | PASS with new issue N-1 | Read 8.4 (lines 1384-1412): RB-01, RB-04, RB-14, RB-16, RB-17, RB-22 now carry lettered pass/fail anchors with a stated checker. SC-14 (line 568) points at 8.4 and the 8.5 closure rule; 9.2 row 15 (line 1812) says the rubric is drafted in 8.4; 8.1 Q3 row (line 1332) says 8.4. Grep for `NOT yet defined`, `not drafted`, `(8.3)`: 0 hits. But RB-01(c) contradicts step 1.4 and RB-16(a): see N-1. |
| F2 | Phase 0 harness contract inconsistent | PASS | Step 0.3 (line 1464) is the single contract: command, 4 screens, widths with heights 48/42/42, five passes, `--depth` selector with the pre-P1 limitation, per-depth file names, `--check` writing `checks.json`. G2 (line 1419) says five passes, includes `--check` and `--heights`, and defers to 0.3; step 7.3 (line 1681) says "exactly as defined in step 0.3", five passes, `--check`. G3 names `<screen>.<depth>.html` which matches the 0.3 file names. Step 0.6 anchor is now "after line 967, the last line of the test that starts at :958" (line 1467). Grep `after line 958`: 0 hits. |
| F3 | RB-10 and SC-6 depend on a non-existent STATE_ROLE table | PASS (see N-3) | Step 1.4 (line 1494) gives a minimum fixed non-empty table keyed by (field, exact value) with the fixture values listed; D-7 (line 1363) records the default and the effect if the owner differs; RB-10(d) (line 1397) requires the table to be non-empty and asserted in `T/test_theme.py`; SC-6 (line 560) lists the same seven values; 8.8 (line 1702) and 9.1 D-7 (line 1793) agree. The vacuous-pass hole is closed. |
| F4 | D-8 undefined; owner decisions without D-ids; 7.3 and 9.1 differ | PASS | 8.2 (lines 1355-1368) defines D-1 to D-12. 7.3 (lines 1296-1316): first table holds D-1 and D-3, second table holds D-7, D-8, D-2, D-5, D-12, D-6, D-10, D-11, D-4, D-9, so together exactly D-1 to D-12. 9.1 (line 1796) maps every id to a row (D-1 row 1, D-3 rows 2-4, D-2 row 5, D-5 row 6, D-12 row 7, D-4 and D-9 row 8, D-6 row 10, D-11 row 14, D-10 row 15, D-7 and D-8 own rows); each target row exists and names that decision (lines 1802-1812). 8.8 (line 1712) and 8.9 row 15 (line 1747) say D-1 to D-12. Grep `D-1 to D-8`: 0 hits. |
| F5 | Open owner question on box lines in `--once --width` unowned | PASS | D-9 (line 1365) has the default yes, what step 3.6 does, and the "no" alternative (a `frames` switch; edits to `test_commands.py:672-675, :690` dropped). Step 3.6 (line 1549) is marked as depending on D-9; Phase 3 Dependencies (line 1538) names D-9; 4.1b (line 646), 7.3 (line 1316) and 9.2 row 8 (line 1805) cite D-9 consistently. |
| F6 | Hash "silently clipped today" contradicts the code measurement | PASS | Lines 781 and 889 now say the earlier claim is SUPERSEDED by the code measurement (wrap runs before `render()`; only the 4-line desk cap and the 400-char ask cap can cut a trailing hash). Grep `silently clipped|clipped today`: the 2 remaining hits are these deliberate supersession notes. Consistent with 2.3, 3.8 (line 606), 4.1b (line 651), 7.2 Q7 (line 1292), 8.1 Q7 (line 1336). |
| F7 | Section 2.5 environment facts without proving commands | PASS | Two proving-command tables (lines 361-369 and 384-395) give command and observed output; the three items not re-run are labelled with the research file and "not re-run" (lines 368, 369, 395), which is honest. |
| F8 | Rich colour-depth and `export_text` probes without arguments and caveats | PASS | Lines 173 and 220 give the probe arguments, one process per depth, the call-order caveat and the research citations (file 01 line 173; file 02 section 2). |
| F9 | Q7 fixture text missing; "exactly 4 desk lines" does not reproduce | PASS, independently re-measured | Fixture text and helper call are in line 275. I ran a read-only probe (`uv run --no-sync python -I -B -c`, `r3_rows` + `r3_screen` from `tests/observe/test_render.py:853-887`, link on, height 70) with that 222-character ask: 160 -> 2 desk text lines [157, 64]; 116 -> 3 lines [85, 71, 64]; 80 -> 3 lines [78, 78, 64]; the last line equals the 64-hex hash at all three widths. This matches line 275 exactly. The withdrawn claim is stated in line 277. |
| F10 | "12-column / 4-column / 3-column" wrong | PASS, independently re-read | `render.py:166-178` has 11 (name, width) pairs for `full`; `:197-204` has 6 for `line`; `:216-222` has 5 for `short` (all counting the 2-cell marker). Lines 144, 317, 318, 319 and 522 now say 11, 6, 5. Grep `12-column`: 0 hits. |

### B. Content quality after the fixes (report-qualitative checklist, adapted to a fix cycle)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement still matches the findings and the Q1-Q7 questions | PASS | Section 1 (lines 25-99) unchanged in substance; the seven questions are answered in 7.2 (lines 1286-1292) and planned in 8.1 (lines 1328-1336). |
| 2 | Current state (Section 2) still describes code that exists | PASS | Re-read `render.py:150-234` (column counts, F10) and re-ran the Q7 probe (F9); both match the report. The F7, F8 probe additions are labelled as re-run or "not re-run". |
| 3 | Options (6.1-6.4) are distinct and unchanged by the fixes | PASS | A/B/C, H1/H2/H3, D1/D2/D3 and Z1/Z2/Z3 differ in mechanism, effort and test impact (comparison tables lines 1026-1039, 1104-1113, 1175-1183, 1232-1240). |
| 4 | Recommendation follows from the comparison | PASS | 7.1 (lines 1246-1251): C beats A on role assignment at build time and beats B on `test_render.py:399`; H3 is the only offline, byte-checking harness; D2 fixes G-2 where D3 fails; Z2 meets the stated conditions. Each rationale matches its comparison table; none of the fixes touched 6.x or 7.1. |
| 5 | Implementation plan is still concrete and actionable | FAIL (N-1) | Phases 0-7 give files, line anchors, signatures and tests, and the harness contract (0.3) is now single-sourced. One gating anchor, RB-01(c), cannot be met by the plan's own step 1.4, so the P1 render gate cannot close as written. |
| 6 | Q1 to Q7 answers consistent with the plan | PASS (notes N-2, N-4) | Q1: 7.2 Option C = 8.1 Q1 `Line` layer. Q2: 7.2 phase list = 8.1 Q2 = 7.1 sequence; golden-changing phases P2, P3, P4, P6 agree in 3.8 (line 601), 7.1 (lines 1257-1261), 7.2 (line 1287) and steps 2.7, 3.9, 4.8, 6.6; P1 and P5 leave both goldens untouched in all places. Q3: H3 gate, session-only image tier, D-10 default "no" agree in 7.2, 8.1, G3 and step 0.4. Q4: D2 in two steps (7.1) = steps 1.1 and 1.2 (one phase); D-5 default = 8.1. Q5: 7.2 gate list (i)-(vii) = steps 1.5, 1.6(f)(g); D-4 default plain = line 1360. Q6: Z2/no-go = 8.1 Q6 = step 7.4. Q7: pane inner widths 154/110/74 (P3) and 72/110/74 (P5) check against geometry (width-6; 160-4-80-4=72; 116-4-4=110; 80-6=74) and 5.5 (line 1631); D-6 default agrees in 7.2, 8.1, 8.2 and RB-19. |
| 7 | No fix introduced a contradiction | FAIL (N-1) | Cross-checked every fix against its neighbours (see A). Only the F1 anchor RB-01(c) contradicts a neighbour. F2, F3, F4, F5, F6, F9, F10 additions are mutually consistent. |
| 8 | Gaps are honest (UNVERIFIED items stay marked) | PASS | 8.8 (lines 1696-1712) and 9.x rows keep the unverified items (PNG route, `LiveScreen` under a pty, flags width, `+1` terms, Zellij runtime). F7 labels the not-re-run commands. F9 withdraws the unreproducible claim instead of hiding it. |
| 9 | External research is relevant (Section 5) | PASS (note N-5) | Each row ties to a Q and to a codebase relationship; contradictions between web and code resolved to the probe (lines 841, 901-910). Tag inconsistency noted in N-5. |
| 10 | Numeric and scale claims substantiated (no scale claims exist; adapted: geometry and counts) | PASS | Geometry arithmetic re-derived: 1+114+2+42+1=160; 1+70+2+42+1=116; 1+76+2+80+1=160; 1+66+2+46+1=116; 2+114+22+12+10=160 (render.py:159-192 read). Column counts 11/6/5 read from code. Q7 line counts re-measured. |
| 11 | Risk assessment complete | PASS | Per-option risks, per-phase rollback lines, D-1 to D-12 "if the owner rules otherwise" effects, height-crop risk and golden churn are all present. |
| 12 | Evidence trail complete; no circular reasoning; conclusion proportionate | PASS (minor stubs) | Section 10 lists 5 code files, 2 web files, gaps log, 6 synthesis files, QA reports. The "this file" self-reference (line 1914) and "will be added there" (line 1918) are the stale template notes already logged as minor at Gate 3. Confidence labels (High/Medium, [UNVERIFIED]) match the evidence strength. |

## Summary

- Checks passed: 20 / 22 (A: 10 of 10 findings applied, F1 with a new issue; B: 10 of 12 pass, items 5 and 7 fail on N-1)
- Checks failed: 2 (both caused by the single defect N-1)
- Blocking issues: 1 (IMPORTANT)
- Minor notes: 6 (not rechecked in later rounds, never fail the review)
- Issues fixed in place: 0 (fix_authorization is false; no file was modified except this report)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N-1 | IMPORTANT (blocking; contradiction introduced by the F1 fix) | Report Section 8.4, row RB-01, anchor (c) (line 1388), against step 1.4 (line 1494), RB-16(a) (line 1403) and Section 3.2 (line 499) | RB-01(c) says "every question age and every question-text line **in the list** and in the desk is amber", and "one counter-example fails the row". Step 1.4 builds the list question line as age `attention` (amber) bold, **subject `body_bold`** (base colour, bold), and RB-16(a) requires every list row line to carry `body_bold`. The mockup agrees with step 1.4: in `inputs/mockups/160/agent-focus-attention-ledger.ansi` line 9 the age `45 MIN` is `0;1;38;2;250;178;25` (amber bold) while the question text `Choose schema compatibility policy` is `0;1;38;2;225;233;238` (base bold); 3.2 lists base for "question rows in the 160 ledger". RB-01 is High and in scope from P1, so the P1 render gate would fail on the plan's own correct output (3 iterations, then G6 stops and asks the owner), or the implementer would break step 1.4 and RB-16. | Change RB-01(c) to: "every question age is amber (bold) and every question-text line **in the desk question pane** is amber; question-text in the list is `body_bold` (RB-16(a))". Keep the desk part, which matches step 1.4 (`desk question text attention`) and RB-14(b). Then re-check RB-01 against step 1.4 once more. |
| N-2 | MINOR | Step 0.8 (line 1469) | "Expected: RB-01 to RB-04 and RB-10 to RB-18 FAIL; script rows pass. A baseline that passes any High rubric row is a sign the rubric is not discriminating". The guard rows RB-05 to RB-08 are High, script-checked, and pass at baseline by design, so the second sentence is wrong for them (and "script rows pass" is wrong for RB-10, RB-14, RB-16, RB-17). Intent is clear, one-time revision only. | Say "a baseline that passes any High finding-driven row (RB-01 to RB-04) ..."; list RB-05 to RB-08 as expected PASS guards. |
| N-3 | MINOR | RB-10(d) (line 1397), SC-6 (line 560), step 1.6(e) (line 1496) | They say `STATE_ROLE` "contains the keys `running`, `succeeded`, `failed`, `completed` and `FROZEN`", but step 1.4 types the table `dict[tuple[str, str], str]` keyed by (field, value), and the `FROZEN` flag has no (field, value) form given. A literal key test fails or is ambiguous. | Write the keys out, for example `("workerState","running")` and `("flags","FROZEN")`, or say "values of the key tuples". |
| N-4 | MINOR | RB-04(b) (line 1391) | In the narrow-tile fallback the figure is "one bold amber line", yet "either way it is the largest figure on the screen (taller than any other text in the right column)": a one-line figure cannot be taller. Branch is practically unreachable (tile inner 38 cells against `4 * len(figure)`). | Drop "taller than" from the fallback branch or require "bold and amber" only. |
| N-5 | MINOR | 5.1.3 (line 779), 5.2.6 (line 813), 5.6 roll-up (line 927) against 2.1, 4.3a, 6.0, 9.5 C1; 9.5 row 39 (line 1851) | Section 5 tags the `safe_box` no-effect probe and the 16-colour collapse as [UNVERIFIED in this synthesis] while Sections 2, 4, 6 and 9 treat both as measured and reproduced by two reviewers. 9.5 row 39 says the guard test is now `:747-760`; every other place says `:747-756`. | Add "(verified in Section 2.1 and 4.3a)" to the Section 5 tags; change 9.5 row 39 to `:747-756`. |
| N-6 | MINOR | 0.3 (line 1464) against 8.4 (lines 1397, 1399, 1388, 1519) | 0.3 says RB-10(d) comes from the `.ansi` census, 8.4 says from `T/test_theme.py`; RB-12 is "Reviewer plus script" but is not in the 0.3 `checks.json` list; RB-01(e) exempts the footer rule only "before P3" although step 2.3 adds the rule in P2 and gives it no role. | Align the three statements in the same edit as N-1. |

## Actions Taken

None (fix_authorization false). No file was modified other than this report. Read-only probe run: the Q7 fixture measurement (output in A, F9).

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was in the spawn prompt; standalone behaviour applied.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None relied on. The consolidated Gate 3 findings file records template-conformance, evidence-quality and domain-accuracy lenses as PASS; I did not re-run those lenses and make no claim about them beyond what I read.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- F9 Q7 measurement: re-ran the fixture through `r3_rows` and `r3_screen` (Bash probe): 2/3/3 desk lines of 157+64, 85+71+64, 78+78+64 cells, hash whole and last. Matches line 275.
- F10 column counts: Read `render.py:150-234`: 11, 6, 5 columns; also re-derived 2+114+22+12+10 = 160.
- F1 anchor vs plan consistency: cross-read RB-01(c) against step 1.4, RB-16(a), RB-14(b) and the mockup ANSI (Bash, `agent-focus-attention-ledger.ansi` line 9): found the RB-01(c) contradiction (N-1). A structural pass would not catch this.
- Greps of the report for stale strings (`silently clipped`, `12-column`, `NOT yet defined`, `after line 958`, `D-1 to D-8`, `(8.3)`, `4 desk lines`): only the deliberate supersession notes remain.
- Decision-id closure: checked that each of D-1 to D-12 appears in 8.2, 7.3 and a 9.1/9.2 row, and that each pointer in line 1796 lands on a row naming that decision.
- Geometry arithmetic for inner widths 154/110/74 and 72/110/74 re-derived against steps 3.3, 5.4, 5.5 and 8.1 Q7.

**Q1 How many factual claims independently verified against source?** About 30: 11 column/width figures, 3 probe measurements, 9 decision-id placements, 7 stale-string greps, plus the mockup colour codes.
**Q2 Files read:** the report (1918 lines, all lines, 11 ranges), qa-consolidated-findings-phase6.md, qa-fix-log.md, `src/superclaude/cli/observe/render.py` (150-234), `tests/observe/test_render.py` (850-888), the mockup `.txt` and `.ansi` of `agent-focus-attention-ledger` at 160, and the prior content of the report file.
**Q3 Zero issues?** Not applicable; one blocking and five minor findings were found.
**Q4 Web research:** none performed; no Tavily or fallback call was made. Section 5 URLs were not re-fetched (they were out of scope for a fix verification).

## Confidence Gate

- **Confidence:** Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (eligible for PASS on confidence; verdict is FAIL on the blocking finding N-1, not on coverage)
- **Tool engagement:** Read: 18 | Grep: 2 | Glob: 0 | Bash: 3
- Note: Read + Grep + Glob = 20, which is below the 22 checklist items, so the rule marks this review as suspect. Reason: the section B items are judgment checks answered from the same eleven range reads that covered every line of the report; they were not separate lookups. The factual claims were checked by the 5 targeted reads, greps and probes listed above.
- UNCHECKED items: none. UNVERIFIABLE items: none.

## Recommendations

- Fix N-1 (RB-01(c)) in the report, and align N-6 in the same edit. Then run the cycle-2 verification of N-1 only. Minor notes N-2 to N-6 may be fixed in the same edit but are not rechecked.
- This is fix cycle 1; one more fix cycle (cycle 2) is allowed before escalation to the user.

## Final Verdict

**FAIL. Remaining blocking count: 1** (N-1).

## QA Complete
