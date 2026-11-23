# QA Report: Gate 3 (Phase 6 report validation), cycle-2 fix verification

**Topic:** Observer visual-parity redesign (issue #606)
**Date:** 2026-11-18
**Phase:** fix-cycle (report validation)
**Fix cycle:** 2 (fix_authorization false; no file modified except this report)
**Report verified:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md

## Overall Verdict: FAIL (1 blocking finding remains)

## Items Reviewed (cycle-1 blocking finding N1 and the fix-log claims)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | N1: RB-01(c) no longer contradicts step 1.4 / RB-16(a) for the LIST (subject base bold, age amber bold, selected row exempt from base rule) | PASS | Report line 1388 (RB-01(c)), line 1494 (step 1.4: age `attention` bold, subject `body_bold`, selected bold amber), line 1403 (RB-16(a)); research 04 line 57 ("amber bold in desks, base bold in the 160 ledger") and line 44 |
| 2 | N1: desk QUESTION TEXT amber bold consistent across RB-01(c), RB-14(b), step 1.4, step 5.3, 3.2 | PASS | Lines 1388, 1401, 1494, 1629 ("in `attention` bold"), 289 and 502 (narrowed to desk question text); research 04 line 47 |
| 3 | N1: desk AGE consistent with RB-01(c) ("every question age (in the list and in the desk) is amber and bold") | FAIL | Line 1629 (step 5.3) builds the desk first body line as `qid  age <age>` with a "muted age"; RB-01(c) at line 1388 demands an amber bold age in the desk. See N2 |
| 4 | M1/N-3: `STATE_ROLE` tuple keys and separate `FROZEN_ROLE` consistent in 1.4, 1.6(e), RB-10(d), SC-6 | PASS | Lines 1494, 1496, 1397, 560 (grep of `FROZEN`/`STATE_ROLE`); 1363 and 1793 are neutral and agree |
| 5 | M3/N-2: step 0.8 baseline sentence | PASS | Line 1469 now says RB-01 to RB-04 and RB-09 to RB-18 FAIL, RB-05 to RB-08 expected to pass |
| 6 | M4: RB-04(c) uses `panes_flat` | PASS | Line 1391 |
| 7 | Fix log claim "RB-01(c), RB-14(b), RB-16(a), RB-23, step 1.4, 3.2 and the open-items row agree" | PARTIAL | True for the rows listed; step 5.3 was not checked and disagrees (N2) |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N2 | IMPORTANT (blocking) | Report line 1629 (step 5.3) vs line 1388 (RB-01(c)) | Same defect class as N1, left over by the cycle-2 fix. RB-01(c) is a High row in scope from P1 and re-scored in every later phase ("plus all earlier rows", P5 line 1639). It requires every desk question age to be amber and bold. Step 5.3 specifies the desk age as `muted`, so a Phase 5 built exactly as planned fails RB-01(c) and the phase cannot close. 04 line 47 lists ages as amber bold. The same text is in synthesis/synth-05-implementation-plan.md:303. | Change step 5.3 to "`qid  age <age>` (`attention` bold qid, `attention` bold age)", or narrow RB-01(c) to list ages only and add a desk-age clause to RB-14. Either way make the desk age role identical in RB-01(c), RB-14 and step 5.3. |

Minor notes (not blocking): M2 (`test_commands.py` assertion lines :671 and :691), N-4, N-5, N-6 were not fixed, as the fix log says; the step 0.8 baseline sentence is silent on RB-19 to RB-23. I found no `MIN` age token in `inputs/mockups/160/decision-desk.ansi`, so desk-age colour in the mockup rests on 04 line 47 only; N2 stands on the internal contradiction regardless.

## Halt guards

- Regression: no item that passed in cycle 1 fails now.
- Monotonicity: |F_2| = 1 and |F_3| = 1, so the count did not strictly shrink: `[HALT-MONOTONICITY] |F|=1`.
- Hard cap: two fix cycles are done (three reviews). No fourth review. Escalate to the user with open blocking finding N2 (a one-line edit to step 5.3 or RB-01(c)).

## Summary
- Checks passed: 5 / 7 (1 failed, 1 partial)
- Blocking findings remaining: 1 (N2)
- Issues fixed in-place: 0 (fix_authorization false)

## Confidence
Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% of checks made; verdict FAIL regardless
Tool engagement: Read: 9 | Grep: 8 | Glob: 2 | Bash: 0

## Verdict: FAIL. Remaining blocking count: 1

## QA Complete

