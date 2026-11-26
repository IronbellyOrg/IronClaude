# Joint report: levers on the plain ember panel, four hold-out plans

**Full experiment write-up (statistics, why each model behaved as it did, recommendations): `../20261116-stronger-panel/EXPERIMENT-REPORT.md`. How to read this report: `READING.md` in this folder.**

Built by `joint_report.py` from 240 scored runs; rerun it to reproduce every number in the tables. The notes after the tables are hand-written.

## All arms (as run)

| Source/arm | runs | found fraction | blocking found | wrong blockers/run | blocking precision | median s | load at start (other claude processes, min-max) | runs with a killed reviewer |
|---|---|---|---|---|---|---|---|---|
| holdout/K | 20 | 0.213 | 0.125 | 1.40 | 0.125 (4/32) | 117.257 | 0-0 | 3 |
| holdout/RL | 20 | 0.259 | 0.258 | 0.50 | 0.444 (8/18) | 141.767 | 0-0 | 4 |
| holdout/Z0 | 20 | 0.223 | 0.200 | 0.95 | 0.269 (7/26) | 99.762 | 0-0 | 1 |
| sev/S | 20 | 0.249 | 0.117 | 1.00 | 0.231 (6/26) | 81.466 | 2-4 | 2 |
| sev/Z0 | 20 | 0.325 | 0.075 | 1.50 | 0.118 (4/34) | 88.227 | 2-4 | 0 |
| stronger/A | 20 | 0.238 | 0.408 | 1.10 | 0.290 (9/31) | 289.090 | 0-4 | 0 |
| stronger/B | 20 | 0.188 | 0.225 | 1.10 | 0.312 (10/32) | 85.368 | 0-4 | 0 |
| stronger/emsol2 | 20 | 0.321 | 0.317 | 0.70 | 0.300 (6/20) | 136.499 | 3-8 | 0 |
| stronger/sole2 | 20 | 0.281 | 0.342 | 0.95 | 0.269 (7/26) | 125.743 | 0-0 | 0 |
| stronger/sonsol | 20 | 0.313 | 0.533 | 0.90 | 0.379 (11/29) | 264.188 | 0-8 | 1 |
| stronger/wonder1 | 20 | 0.314 | 0.425 | 1.65 | 0.267 (12/45) | 150.012 | 0-0 | 0 |
| stronger/wonsol | 20 | 0.432 | 0.458 | 0.90 | 0.379 (11/29) | 151.114 | 0-7 | 0 |

Moved-aside originals are never judged, so as-run scores exist only where a run needed no rerun; the table below lists what was moved aside and why. Elapsed times are comparable only between arms with a similar load column.

## All arms (rerun substituted)

| Source/arm | runs | found fraction | blocking found | wrong blockers/run | blocking precision | median s | load at start (other claude processes, min-max) | runs with a killed reviewer |
|---|---|---|---|---|---|---|---|---|
| holdout/K | 20 | 0.213 | 0.125 | 1.40 | 0.125 (4/32) | 117.257 | 0-0 | 3 |
| holdout/RL | 20 | 0.259 | 0.258 | 0.50 | 0.444 (8/18) | 141.767 | 0-0 | 4 |
| holdout/Z0 | 20 | 0.223 | 0.200 | 0.95 | 0.269 (7/26) | 99.762 | 0-0 | 1 |
| sev/S | 20 | 0.249 | 0.117 | 1.00 | 0.231 (6/26) | 81.466 | 2-4 | 2 |
| sev/Z0 | 20 | 0.325 | 0.075 | 1.50 | 0.118 (4/34) | 88.227 | 2-4 | 0 |
| stronger/A | 20 | 0.238 | 0.408 | 1.10 | 0.290 (9/31) | 289.090 | 0-4 | 0 |
| stronger/B | 20 | 0.188 | 0.225 | 1.10 | 0.312 (10/32) | 85.368 | 0-4 | 0 |
| stronger/emsol2 | 20 | 0.321 | 0.317 | 0.70 | 0.300 (6/20) | 136.499 | 3-8 | 0 |
| stronger/sole2 | 20 | 0.281 | 0.342 | 0.95 | 0.269 (7/26) | 125.743 | 0-0 | 0 |
| stronger/sonsol | 20 | 0.313 | 0.533 | 0.90 | 0.379 (11/29) | 264.188 | 0-8 | 1 |
| stronger/wonder1 | 20 | 0.314 | 0.425 | 1.65 | 0.267 (12/45) | 150.012 | 0-0 | 0 |
| stronger/wonsol | 20 | 0.432 | 0.458 | 0.90 | 0.379 (11/29) | 151.114 | 0-7 | 0 |

## Moved-aside originals (invalid first attempts, rerun once; never judged)

| Source/arm | moved aside | killed reviewer | other bad report status | other |
|---|---|---|---|---|
| holdout/Z0 | 1 | 0 | 1 | 0 |
| stronger/A | 1 | 1 | 0 | 0 |
| stronger/B | 1 | 1 | 0 | 0 |
| stronger/emsol2 | 1 | 0 | 1 | 0 |
| stronger/sole2 | 1 | 1 | 0 | 0 |
| stronger/sonsol | 5 | 4 | 1 | 0 |
| stronger/wonsol | 2 | 0 | 1 | 1 |

## Severity-rule test gates (own control, interleaved)

- PASS G1 wrong blockers S <= 0.70 x Z0
- PASS G2 real blocking matches S >= Z0
- FAIL G3 found fraction S >= Z0 - 0.02
- PASS G4 pooled median time S <= 1.10 x Z0

## Stronger-panel test (lever = difference >= +0.10 and bootstrap lower bound above 0, against its same-day arm B)

- A: difference +0.050, lower bound -0.154: no demonstrated lever
- sole2: difference +0.092, lower bound -0.032: no demonstrated lever
- wonder1: difference +0.126, lower bound -0.008: no demonstrated lever
- sonsol: difference +0.125, lower bound -0.021: no demonstrated lever
- wonsol: difference +0.243, lower bound 0.025: LEVER
- emsol2: difference +0.133, lower bound -0.025: no demonstrated lever

Several arms are compared with one control: a single hit among them is weak evidence; no multiplicity correction is applied.

Secondary, not the registered decision: the same rule against the two same-day controls pooled (found fraction 0.257; pooling allowed by the rule fixed before any score was read):

- A: difference -0.018, lower bound -0.355: no demonstrated lever
- sole2: difference +0.024, lower bound -0.112: no demonstrated lever
- wonder1: difference +0.057, lower bound -0.091: no demonstrated lever
- sonsol: difference +0.057, lower bound -0.193: no demonstrated lever
- wonsol: difference +0.175, lower bound 0.040: LEVER
- emsol2: difference +0.064, lower bound -0.035: no demonstrated lever

## Sensitivity: found-fraction difference against the arm's own control, leaving one plan out (descriptive)

HX-1 has only 2 known defects, so one run there swings the pooled mean by up to 0.5 of its plan weight.

| Arm | all four plans | without HO-2 | without HO-3 | without HX-1 | without HX-3 |
|---|---|---|---|---|---|
| holdout/K | -0.010 | +0.000 | -0.019 | -0.013 | -0.008 |
| holdout/RL | +0.036 | +0.061 | +0.026 | +0.014 | +0.042 |
| sev/S | -0.076 | -0.128 | -0.112 | +0.032 | -0.096 |
| stronger/A | +0.050 | +0.000 | +0.022 | +0.167 | +0.011 |
| stronger/emsol2 | +0.133 | +0.150 | +0.193 | +0.010 | +0.177 |
| stronger/sole2 | +0.092 | +0.083 | +0.134 | +0.023 | +0.129 |
| stronger/sonsol | +0.125 | +0.067 | +0.133 | +0.167 | +0.133 |
| stronger/wonder1 | +0.126 | +0.094 | +0.173 | +0.068 | +0.168 |
| stronger/wonsol | +0.243 | +0.244 | +0.319 | +0.091 | +0.319 |

## Controls

The two ember Z0 controls (sev/Z0, stronger/B) differ by a 90% interval of -0.435 to 0.083 on found fraction and -1.000 to 0.200 on wrong blockers: **pooled analysis allowed**.
The severity test's control is interleaved with its arm in the same blocks. In the stronger-panel test, arms A and B were interleaved with each other (22:33 to 00:40 UTC on 2026-11-16); sole2 and wonder1 then ran alone (00:47 to 02:39); sonsol, wonsol and emsol2 overlapped each other from 03:44. So arm B is 3 to 5 hours older than the last three arms.

## Causes of the moved-aside runs with an error (from the other session's review)

- emsol2 HO-2 r1: `claude: not found` (a short window with no Claude Code binary).
- sonsol HO-2 r3 and wonsol HX-3 r5: `[claude-code:unrecognized_model]` for `muse-ember-1.0` and `muse-wonder-1.0` respectively (the program rejected the model name once, one reviewer each; both happened while three panels ran at once, so a link to load cannot be excluded).
- wonsol: one run was cut short by the other session's own restart. sonsol HO-3 r3 was killed again in its rerun and stays as run; sonsol HX-1 r2 has a format-invalid reviewer report and was kept as run (not rerun).

## Judging

One blind Opus judge per run; a second judge on a sample (21 runs in the stronger-panel test, agreeing on all 21 found-item sets; 6 in the severity test, agreeing on all 6; 9 in the Recipe Ledger comparison, agreeing on all 9). Judge noise is not the explanation for arm differences; the answer key holds 36 items, and wrong-blocker counts depend on it.

## Limits

One panel family (ember or sonnet with luna), plans only, 36 known defects, ground truth by a model session, 5 runs per arm per plan, plans already used for an earlier test. See each test's own pre-registration for the full list.
