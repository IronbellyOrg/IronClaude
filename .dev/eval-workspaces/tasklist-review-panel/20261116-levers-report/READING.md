# Joint report: how to read it (DRAFT for review by the other session; written 2026-11-17)

**Context for a reader with no history.** The "Review Panel" has cheap reviewer models report plan defects; a blind Opus judge scores each run against a hidden defect list (4 plans, 36 known defects, 10 blocking). Two sessions tested levers on the plain ember panel (`muse-ember-1.0` + 2x `gpt-6-luna`): this session tested a narrower blocking rule in the brief (`../20261116-severity-test/`); the other tested different reviewer panels (`../20261116-stronger-panel/`). Earlier, a redesign (Recipe Ledger) failed its frozen gates (`../20261116-holdout/RESULTS-HOLDOUT-20261116.md`). `REPORT.md` here is produced by `joint_report.py` (run `bash run-joint.sh`) from the score files of all tests; every number below is quoted from it. Status: DRAFT until the other session has read it. Open questions for the owner: `../OPEN-DECISIONS-20261115.md`.

## What the numbers say

1. **One panel met its registered lever rule: `wonsol` = `muse-wonder-1.0` + `gpt-6.1-sol` + `muse-ember-1.0`.** Found fraction 0.432 against 0.188 for the same-day ember control (+0.243, 5th-percentile bound +0.025; the rule is at least +0.10 with a bound above 0). Against the two same-day controls pooled (0.257) it is +0.175, bound +0.040. The other five arms (Sonnet panel A, sole2, wonder1, sonsol, emsol2) did not meet the rule: differences +0.05 to +0.13, bounds below 0.
2. **That is one hit among six arms compared with one control: weak evidence**, as both sessions agreed beforehand; no correction was applied.
3. **The result leans on the smallest plan.** HX-1 has 2 known defects; wonsol found both in every run (1.00 against 0.30 for the control). Without HX-1, wonsol's lead falls to +0.091, below the +0.10 rule; without any other single plan it stays +0.24 to +0.32. Sonsol and A rise when HX-1 is left out; emsol2 and sole2 fall to about +0.01 to +0.02. Every panel arm stays at or above its control in every leave-one-plan-out cut; wonsol is the largest in three of the four cuts (+0.24 to +0.32); without HX-1 it is +0.091 and sonsol and A (+0.167 each) are ahead of it. None of the arms is secure.
4. **The controls disagree:** the ember control scored 0.188 (stronger-panel test), 0.325 (severity test) and 0.223 (earlier hold-out comparison) on the same plans. A control that moves by 0.14 between three batches of 20 runs is the noise level any lever has to beat; the registered comparison used the lowest of the three.
5. **Cost in time:** wonsol's median panel time was 151 s against 85 s for the ember control (about 1.8 times); panels with a Sonnet reviewer took 264 to 289 s (about 3 times). Time columns for sonsol, wonsol and emsol2 carry load from several panels running at once (load column in the table); do not compare them with sole2 or wonder1 (run alone).
6. **Wrong blockers:** wonsol 0.90 per run against 1.10 (control B) and 1.50 (severity-test control): not distinguishable from the control (no test was registered for wrong blockers; 20 runs per arm). The lowest wrong-blocker panel arm is emsol2 (0.70), not wonsol. Recipe Ledger had 0.50 against 0.95 on the same plans, and the narrowed rule 1.00 against 1.50 (but lost recall, gate G3); the bootstrap intervals in `REPORT.md` for those two reach or approach 0, so none of the wrong-blocker differences is firm.
6b. **Judge noise is not the explanation:** a second blind judge agreed on every sampled run (21 of 21 in the stronger-panel test, 6 of 6 in the severity test, 9 of 9 in the Recipe Ledger comparison). The answer key has 36 items, and the wrong-blocker count depends on it.
6c. **Control B is older than the last arms:** arms A and B ran interleaved (22:33 to 00:40 UTC); sole2 and wonder1 ran alone after; sonsol, wonsol and emsol2 ran from 03:44, overlapping each other. B is 3 to 5 hours older than the last three arms, and a Claude Code program update happened in between.
7. **The narrowed severity rule** passed G1 (wrong blockers), G2 (real blockers) and G4 (time) and failed G3 (found fraction -0.076, all of it from HX-1); the sensitivity table shows it ahead of its control on the other three plans.
8. **Recipe Ledger** failed D1, D2, D3 and D6 in its frozen test; the lever table lists it for context (found fraction +0.036).

## Added 2026-11-17 from the other session's full report (`../20261116-stronger-panel/EXPERIMENT-REPORT.md`, section 3.2)

The "only wonsol is a lever" statement in point 1 holds only for the registered metric (mean of per-run found fractions, every plan weighted equally). The other session re-ran the same bootstrap (`../20261116-stronger-panel/analysis/arms-items.py`, output `arms-items-results.txt`; quoted here, not recomputed by `joint_report.py`):

| Arm | Registered | Every defect equal (36) | Registered, no HX-1 | Every defect equal, no HX-1 |
|---|---|---|---|---|
| A (Sonnet in seat S) | +0.050 (bound -0.154) | **+0.139 (+0.023)** | **+0.167 (+0.100)** | **+0.165 (+0.100)** |
| sole2 | +0.092 (-0.033) | +0.033 (-0.032) | +0.023 (-0.039) | +0.018 (-0.039) |
| wonder1 | +0.126 (-0.013) | +0.072 (-0.013) | +0.068 (-0.028) | +0.059 (-0.028) |
| sonsol (Sonnet in seat S) | +0.125 (-0.029) | **+0.150 (+0.057)** | **+0.167 (+0.078)** | **+0.159 (+0.078)** |
| wonsol | **+0.243 (+0.032)** | +0.117 (+0.021) | +0.091 (-0.006) | +0.082 (-0.006) |
| emsol2 | +0.132 (-0.025) | +0.033 (-0.030) | +0.010 (-0.044) | +0.006 (-0.044) |

Reading: the winner depends on the weighting. The two arms with Sonnet in seat S (A and sonsol) are levers whenever the large plans carry their weight; wonsol is a lever on the registered metric and, by a smaller margin, with every defect equal, but not without HX-1. My leave-one-plan-out table shows the same HX-1 effect. Arm A is a lever on those weightings too (the other report's recommendation 3 was corrected to say so); sonsol differs from A by being cleaner (0.90 against 1.10 wrong blockers, 1.25 against 1.00 blocking found per run), both about 3 times the control's panel time. Per-model behaviour, per-seat effects and the 8 of 36 defects no arm found are in that report (sections 4 and 3.3), from its own per-reviewer tables, which this report does not reproduce.

## What this means for the review panel's goals

- **A different reviewer panel is the more promising lever than a process redesign or a brief rule on these plans,** but only one arm shows it, with a lead that depends on a 2-defect plan, a low control and a 1.8 times time cost. It is a candidate for a confirming test, not an adoption.
- **The conditional combined arm (Sonnet panel + narrowed rule)** that the two sessions pre-agreed does not run: the Sonnet panel is not a lever and the rule failed G3. A different combination (wonsol with the narrowed rule) is a new idea that needs its own pre-registration and the owner's order.
- **Decision-grade next step (my recommendation, for the owner):** run wonsol against a same-day ember control on at least two NEW plans (not the four used so far, which now carry three tests' worth of knowledge), with the same registered rule and the time cost stated, before any change to the panel's default models.

## Limits

One ember-based family of panels, plans only, 36 known defects, two plans with no blocking defect, ground truth written by a model session, 5 runs per arm per plan, the four plans reused across tests, several arms run under different machine load, the Claude Code program updated twice during the day (a few runs lost to a missing binary and rerun once), originals of rerun runs never judged (so "as run" and "rerun substituted" scores coincide; the moved-aside runs are counted in the table).
