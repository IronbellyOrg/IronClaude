# QA Report: Fix verification, qualitative (Gate 3 cycle 2, Phase 6 report validation)

**Topic:** Observer visual-parity investigation (issue #606)
**Date:** 2026-11-18
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 2
**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md (1918 lines, read in full in ranges)
**Inputs:** qa/qa-consolidated-findings-phase6-cycle2.md, qa/qa-fix-log-cycle2.md
**fix_authorization:** false (no file modified except this report)

---

## Overall Verdict: FAIL (1 blocking finding remains; the cycle-2 fix target N1 is verified fixed)

Remaining blocking count: 1 (N2-Q below). The open defect is the same class as N1, one clause away: the desk age colour.

## Verification of the cycle-2 fix log, item by item

| # | Fix-log claim | Result | Evidence |
|---|---|---|---|
| 1 | N1: RB-01(c) rewritten (ages amber bold, desk question text amber bold, list subject `body_bold` never amber, selected row under `selected`) | VERIFIED | Report line 1388 reads as claimed. Matches step 1.4 (line 1494: age `attention` bold, subject `body_bold`, selected row `selected` bold amber) and research 04 lines 47 and 57. I decoded the mockup `.ansi`: `45 MIN`, `20 MIN`, `10 MIN` in agent-focus-attention-ledger 160 are `ESC[0;1;38;2;250;178;25m` (bold amber). |
| 2 | N1: RB-16(a) rewritten | VERIFIED | Line 1403 matches RB-01(c), step 1.4 and RB-23 (line 1410). Minor note M-Q2. |
| 3 | N1: step 1.4 states `selected` as bold amber | VERIFIED | Line 1494; consistent with 8.8 (line 1708). |
| 4 | N1: Section 3.2 amber rows narrowed to "desk question text" | VERIFIED | Lines 289 and 502 both say desk question text amber, list and 160 ledger question rows base. |
| 5 | M1/N-3: `STATE_ROLE` tuple keys, `FROZEN_ROLE = "state_frozen"` | VERIFIED | Step 1.4 (1494), step 1.6(e) (1496), RB-10(d) (1397), SC-6 (560) agree; step 1.2 role list has `state_frozen` (1492). SC-6 key list equals the step 1.4 table. |
| 6 | M3/N-2: step 0.8 baseline sentence | VERIFIED | Line 1469 matches. |
| 7 | M4: RB-04(c) reads `panes_flat` | VERIFIED | Line 1391; `panes_flat` defined in step 4.6 (line 1591). |

## Blocking finding

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| N2-Q | IMPORTANT (blocking) | RB-01(c) line 1388 vs step 5.3 line 1629 (also step 1.4 line 1494, RB-14(a) line 1401, 3.2 line 502) | RB-01(c) requires every question age "in the list and in the desk" to be amber and bold, and 3.2 line 502 lists ages as amber. Step 5.3 builds the desk first body line `qid  age <age>` with a "muted age". A Phase 5 built exactly as written fails RB-01(c), a High row, so P5 cannot close under G6. Step 1.4 names no role for the desk `qid  age` line, so the P1 scoring of the desk age is undefined. The 160 desk mockup has no age token (0 `MIN` hits in decision-desk.ansi), so nothing supports a muted age; research 04 line 47 supports amber bold. Same class as N1. The structural cycle-2 report (qa/qa-fix-verification-cycle2.md line 17) independently found the same contradiction. | Pick one and state it in all places. Evidence-supported: desk age is `attention` bold. Change step 5.3 to bold `attention` qid and age, add the desk `qid  age` line to step 1.4, keep RB-01(c). If muted is intended, change RB-01(c) and line 502 to "ages in the list" and add a desk-age clause to RB-14. |

## Minor findings (notes only)

- M-Q1: Step 1.4 gives desk question text only the role name `attention`, while age and the tile figure say "`attention` bold" (step 4.3 "one bold `attention` line"). RB-01(c) and RB-14(b) need amber and bold; step 1.2 never says whether `attention` carries bold. Fix together with N2-Q.
- M-Q2: RB-16(a) says "every question row line is bold" but step 1.4 sets the `QUESTIONS_REASON` tail to `muted`. Word (a) as "age and subject spans are bold".
- Carried, not fixed by design: M2, N-4, N-5, N-6.

## Coherence and Q1 to Q7 consistency (checked, no defect)

| Check | Result | Evidence |
|---|---|---|
| Q1 to Q7 answers (7.2, lines 1286 to 1292) agree with 3.8, 6.x, 8.1 | PASS | Q1 Option C (6.1, 7.1, 8.1 line 1330); Q2 P0 to P7 scheme stated as authoritative in 7.1, 8 and 3.8; Q3 H3 gate with H1 extra (7.1 vs 8.1 line 1332, D-10 default no); Q4 D2 in two steps (7.1) vs step 1.1; Q5 `console.file.getvalue()` (7.2, step 1.5); Q6 Z2 optional only (7.1, 8.1, 7.4); Q7 hash whole inside four lines, cap exceptions (7.2, D-6, RB-19, 8.1 line 1336). |
| Numbers across sections | PASS | 160 = 1+114+2+42+1 and 116 = 1+70+2+42+1 in 2.4, 3.3, 7.1, 8.3, step 4.2; 766 tests in 1.2, 2.3, 8.5, 8.9; 78/74 inner width at 80 in 2.3, 7.2, step 3.7. |
| Decision set D-1 to D-12 | PASS | 7.3, 8.2 and 9.1 map each id; D-7 and D-8 rows agree with steps 1.4 and 5.1. |
| Finding-to-phase map vs rubric rows | PASS | 8.10 rubric ids match 8.4 findings column. |
| Standing constraints (screen-only question text, records unchanged) | PASS | 3.7, step 4.1 (`count_figure` not read by export.py), 8.9 rows 3 and 4. |

## Inherited Structural Verdict, Reliance Audit and Self-Audit

No Inherited Structural Verdict block was in the spawn prompt, so I ran standalone (no reliance on any rf-qa PASS item).

## Self-Audit

**(a) Reliance list:** none (no inherited verdict supplied; the structural cycle-2 report was read only after I found N2-Q, as corroboration).

**(b) Independent semantic checks:**
- Desk age colour: read report lines 1388, 1494, 1629, 502; decoded `ESC` colour codes of the 160 desk and ledger mockups with grep and sed; found 0 age tokens in the desk mockup and bold amber ages in the ledger mockup.
- Read research/04 lines 38 to 65 to confirm the amber and base question-text claim behind the N1 fix.
- Read all 1918 report lines in ranges (1-500, 500-760, 760-990, 990-1190, 1190-1380, 1380-1510, 1510-1620, 1620-1770, 1770-1918) and cross-checked Q1 to Q7 in 3.8, 7.2 and 8.1.

## Confidence and tool engagement

Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%. Items: 7 fix-log claims, 5 coherence checks. Verdict is FAIL on content (one blocking defect), not on confidence.
Tool engagement: Read: 13 | Grep: 4 | Glob: 1 | Bash: 3. No web research was needed (Tavily not used; no external lookup).

## Recommendations

1. This is review 3 of 3 for the Gate 3 loop (first review, cycle-1 re-review, cycle-2 re-review). Do not run a fourth review. Escalate to the user with the open blocking finding N2-Q and its one-place-each fix (steps 5.3 and 1.4; RB-01(c) unchanged).

## QA Complete
