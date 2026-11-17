# Joint report: levers on the plain ember panel, four hold-out plans

## Summary for readers outside the project (plain language)

*Written by the other session and checked and corrected against this report's tables by the session that built the report. Figures are quoted from the tables below unless marked otherwise.*

**The setting.** Before a software change is built, a written plan says what to build. A mistake in the plan is cheap to fix on paper and expensive to fix after the code exists. So we use a "review panel": a few small, inexpensive AI models each read the plan and list the problems they see, and a script merges their lists. The question for this study was simple: **does the panel catch enough of the real problems, and can we make it catch more without making it much slower or noisier?**

**How we tested it.** We took plans whose real problems were already known (36 known problems across four plans, written down in an answer key). We ran the panel on them many times, in many variations, and a separate AI judge, who did not know which variation produced which report, checked each report against the answer key. We counted two things: how many of the known problems the panel found, and how many "false alarms" it raised (a finding it called blocking, meaning "do not build until fixed", that was not a real problem). The tables below hold 240 judged panel runs from three tests; the project ran more in earlier studies.

**What we learned.**
1. **The everyday panel misses most problems.** The standard cheap panel found about one in five of the known problems on two testing days (19 and 22 percent) and about one in three on a third (33 percent); it raised about one false blocking alarm per run (0.95 to 1.50).
2. **Rewriting the instructions did not help much.** Three families of ideas either did not find more problems or lost some. Having the reviewers confer did nothing reliable. A checklist and ledger of findings (the best of them) roughly halved false alarms (0.50 against 0.95) but did not raise the share of problems found in any firm way (+0.04). Narrowing the rule for what counts as blocking cut false alarms by a third and kept the real blockers, but found fewer of the known problems (25 against 33 percent), almost all of that on one plan with two known problems.
3. **Which models sit on the panel mattered more than how they are told to work.** Six alternative panels were tried. One stood out: a panel of three different models (called wonder, sol and ember in our notes) found 43 percent of the known problems, about 2.3 times the same-day baseline (19 percent) and 1.3 times the best baseline day (33 percent). Its false alarms were about the same as the baseline's (0.9 against 1.1, within the noise of 20 runs). A separate per-model analysis by the other session (not reproduced by this report's script) found that one of the three models (sol) was by far the most accurate: about a quarter of its blocking findings were wrong, against about three quarters for the others.
4. **It costs time.** That panel took about 1.8 times as long as the standard one (about 2.5 minutes instead of 1.4 per review), which is still small next to the cost of building from a flawed plan.

**What this means, and what it does not.** The result points to a cheap, practical improvement: change which models review, not how they are instructed. But it is one promising result, not a proven one. It came from only four plans, one of which has just two known problems and contributed much of the gain (without it the lead is +0.09, below the +0.10 bar we set). We compared six panels against one baseline, so a single winner can arise by chance. The answer key was itself written by an AI and may miss real problems, which makes some "false alarms" real findings. And the baseline panel scored differently on different days (0.19 to 0.33), so a gain has to be large to count.

**What happens next.** Nothing is changed in the product yet. The recommended next step is to repeat the winning combination against a fresh baseline on at least two plans nobody has used, with the success rule written down first. If it holds, the default review models should change; if not, the project keeps the standard panel and stops tuning it. The decision to run that confirming test, and any change to the default, belongs to the project owner.

Built by `joint_report.py` from 240 scored runs; rerun it to reproduce every number in the tables. The summary above and the notes after the tables are hand-written.

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
