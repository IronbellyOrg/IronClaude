# Severity-rule test: results (2026-11-17)

**Context for a reader with no history.** The "Review Panel" has cheap reviewer models report plan defects; a blind Opus judge scores each run against a hidden defect list. A frozen comparison of the Recipe Ledger redesign (`../20261116-holdout/RESULTS-HOLDOUT-20261116.md`) found its only consistent benefit was fewer wrong blockers (findings marked blocking that match no real defect). This test asks whether one cheap change gives that benefit alone: a narrower wording of the "contradiction" blocking clause in the reviewer's brief (arm S, the owner-approved wording of `../20261114-severity/PLAN.md`) against the plain control brief (arm Z0). Registered before any run in `PREREG.md` and `PREREG-ADDENDUM-1.md` (convergence with a second test, a stronger reviewer panel, run by another session on the same plans; the joint report is a later step). Background and open questions: `../OPEN-DECISIONS-20261115.md`.

## Result

**Not adopted: the rule passes three of four pre-registered gates and fails the recall gate (G3).** It cuts wrong blockers by a third and keeps real blockers, but finds fewer defects overall on this set, and one reviewer was killed by the time limit in 2 of its 5 HO-3 runs while the control had none.

## What was run

- 4 plans (HO-2, HO-3, HX-1, HX-3; 36 known defects, 10 blocking), 2 arms x 5 replicates = 40 panel runs, ember panel (`muse-ember-1.0` + 2x `gpt-6-luna`), block-randomised, one panel at a time, no fallback, own sandbox root, harness identical except one file (`../20261116-sev-z0/briefs/base.txt` against `../20261116-sev-s/briefs/base.txt`).
- Blind Opus judge on all 40 plus a second judge on 6 (15%); judge audit: 46 folders, 0 bad.
- First pass: 5 runs invalid (4 on HO-3 where a reviewer hit the 150 s guard in the S arm, 1 `sev1-s-HX-1-r4` where the Claude Code program was missing during an update); moved aside (`results/INVALID-FIRST-PASS.txt`) and rerun once as registered. After the rerun, 2 runs (`sev1-s-HO-3-r1`, `sev1-s-HO-3-r3`) still had one reviewer killed; they stay and are scored on the reports that were returned. Claude Code program versions: `results/cli-version.log` (2.1.326 throughout; two one-minute "binary missing" windows at 22:49 and 23:19 UTC).

## Numbers (pooled over the four plans, 20 runs per arm)

| Measure | Z0 (control) | S (narrowed rule) |
|---|---|---|
| Found fraction of known defects | 0.325 | 0.249 |
| Real blocking defects found (fraction of blocking items, 2 plans with blocking items) | 0.075 | 0.117 |
| Wrong blockers per run | 1.50 | 1.00 |
| Blocking rows per run | 1.70 | 1.30 |
| Blocking precision (matched/blocking rows) | 0.12 (4/34) | 0.23 (6/26) |
| Rows per run | 6.0 | 5.0 |
| Median panel seconds | 88.2 | 81.5 |
| Runs with a killed reviewer after rerun | 0 | 2 (both HO-3) |

## Gates (as pre-registered)

| Gate | Rule | Result |
|---|---|---|
| G1 | wrong blockers per run at most 0.70 x Z0 | **pass**: 1.00 against 1.50 (ratio 0.67) |
| G2 | real blocking matches at least Z0's | **pass**: 6 against 4 |
| G3 | found fraction at least Z0 - 0.02 | **FAIL**: 0.249 against 0.325 (-0.076) |
| G4 | pooled median time at most 1.10 x Z0 | **pass**: ratio 0.92 |

The 90% bootstrap interval (plans, then runs) for wrong blockers, S minus Z0, is [-1.30, +0.05]: it reaches 0, so even the pass on G1 is not firmly separated from noise.

## What this means

- **The rule does what it was meant to do on blocking findings:** fewer wrong blockers, a larger share of blocking findings that hit real defects, no loss of real blockers. It does not slow the panel.
- **It costs recall on this set, by the pre-registered rule.** Per plan (found fraction, Z0 against S): HO-2 0.10 / 0.18, HO-3 0.13 / 0.17, HX-3 0.07 / 0.05, HX-1 1.00 / 0.60. The whole gap comes from HX-1, a plan with two known defects, where Z0 found both in all five runs and S found them in three of five. Without HX-1, S is at or above Z0 on three plans. This reading is after the fact and descriptive; the registered gate fails.
- **The control moved:** this Z0 averaged 0.325 against 0.223 for the same configuration earlier the same day (HX-1: 1.00 against 0.50). A control that swings that much on 5 runs per plan makes any 0.05 to 0.1 difference unreliable. The joint report will compare against the second test's control too.
- **HO-3 reviewer kills:** in the S arm one luna reviewer hit the 150 s guard in 4 of 5 first-pass HO-3 runs and 2 of 5 after rerun; the control had none. It may be the rule making that reviewer think longer on that plan, or chance on a slow plan. Not tested.

## Limits

One panel (ember), plans only, 36 items (two plans without blocking items), plans reused from the Recipe Ledger comparison, 5 runs per arm per plan, ground truth by a model session, a second test running at the same time on the same machine (affects both arms alike), two short Claude Code program outages. A "no adoption" result here does not show that the rule is bad: it shows it did not pass all four gates on this set.

## Files

`results/report.md`, `results/metrics.json` (analysis), `results/scoring/` (scores and anonymised reports), `results/runs/` (run and timing records), `results/driver.log`, `results/cli-version.log`, `results/INVALID-FIRST-PASS.txt`. Raw run folders and judge transcripts are not committed.
