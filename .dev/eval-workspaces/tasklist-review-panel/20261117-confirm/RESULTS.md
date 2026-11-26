# Confirming test of the wonsol panel: results (2026-11-17)

**Context for a reader with no history.** The "Review Panel" has cheap reviewer models read an implementation plan and report plan defects; a blind Opus judge scores each run against a hidden list of known defects. In the earlier stronger-panel test (`../20261116-stronger-panel/EXPERIMENT-REPORT.md`) the panel `wonsol` (`muse-wonder-1.0` + `gpt-6.1-sol` + `muse-ember-1.0`) was the only one of six to meet its lever rule against the plain ember panel (0.432 against 0.188), on weak evidence. This test repeats the comparison on five plans nobody had used, with the control (ember panel B) run in the same interleaved schedule. Design and decision rule were frozen before any run: `PREREG.md` (hash in `FROZEN.txt`).

## Result

**Not confirmed.** Neither measure cleared the frozen bar of a lead of at least +0.10 with a 5th-percentile bound above 0. The lead is in the same direction as before but smaller, and it just misses.

| Measure (W = wonsol, B = ember control) | B | W | Lead | Lower bound | Bar met |
|---|---|---|---|---|---|
| M1: mean of per-run found fractions (each plan counts equally) | 0.183 | 0.282 | +0.099 | -0.004 | no |
| M2: found / possible (each defect counts equally) | 0.182 | 0.291 | +0.109 | -0.006 | no (bound) |

M2's lead is above +0.10, but its bound is below 0, so it fails the rule. M1 misses on both counts, narrowly (+0.099).

## What was run

50 panel runs (2 arms x 5 plans x 5 replicates), interleaved, one panel at a time, 06:12 to 07:45 UTC, Claude Code 2.1.326 throughout. No run was invalid, no reviewer was killed. 5 plans, 33 known defects (1 blocking), answer key by a fresh Sonnet session from earlier independent review reports; all 33 quotes verified in the plans. Blind Opus judge on all 50 plus a second judge on 8: identical sets of found defects on 8 of 8; judge audit 58 folders, 0 bad.

## Descriptive measures

| Measure | B | W |
|---|---|---|
| Wrong blockers per run | 0.52 | 0.20 |
| Blocking findings that matched a known defect, per run | 0.44 | 0.72 |
| Median panel seconds | 85 | 132 (1.56 times B) |
| Distinct defects found at least once, of 33 | 17 | 18 |

Per plan, found fraction (B, W): NP-1 0.15, 0.33; NP-2 0.18, 0.33; NP-3 0.04, 0.24; NP-4 0.27, 0.23; NP-5 0.28, 0.28. Leave one plan out (descriptive; M1 lead and bound): without NP-1 +0.081 (-0.014); NP-2 +0.085 (-0.034); NP-3 +0.074 (-0.037); NP-4 +0.133 (+0.025); NP-5 +0.124 (+0.008). Raw output: `RESULTS-raw.txt`.

## What this means

- **The earlier claim is not reproduced at its size.** On new plans the lead is about +0.10 (earlier +0.243), and its lower bound is about 0 (earlier +0.032). The earlier lead rested on a plan with 2 known defects; this set has no such plan, and a lead of +0.07 to +0.14 remains in every leave-one-plan-out cut.
- **The direction holds, and accuracy looks better, not worse.** W found more on 3 of 5 plans, tied on 1, and was lower on 1 (NP-4, by 0.04). It raised fewer wrong blockers (0.20 against 0.52 per run) and more of its blocking findings matched a known defect (0.72 against 0.44 per run; the key itself marks only 1 defect blocking, so this counts findings the panel graded blocking, not the key's blocking class). Neither figure had a registered test.
- **Reach did not widen.** Both arms found about half of the 33 defects at least once (17 and 18), so the gain is more consistent finding of the same defects, not new ones.
- **Cost:** 1.56 times the control's median panel time (earlier test: 1.8 times).

## Limits

Five small plans (5 to 9 defects each), so each plan's score moves in coarse steps and power is low; only 1 blocking defect in the key; the key is a model's, and an unlisted real defect counts as a wrong blocker; NP-2 to NP-5 use bases derived from history (the progress files record tree ids), and three plans cite files that exist only in the uncommitted start state (`author-out/NP-*/notes.md`); the second authoring batch overwrote the first batch's summary file (NP-1 and its notes are intact); one arm, one mix of models, plans only. A "not confirmed" result does not show that wonsol is no better: it shows it did not clear this bar on these plans. The two bars (M1 and M2) are the ones frozen before the runs, not tuned after.

## Files

`PREREG.md`, `FROZEN.txt`, `schedule/schedule.tsv`, `run.sh`, `analyze.py`, `RESULTS-raw.txt`, `logs/`, `confirm-gt/` (answer key), `author-out/` (authoring output; session transcripts not committed). Scores: `../20261114-recipe-ledger/scoring-confirm/` (score.json, anonymised reports, labels). Raw run folders `../20261114-recipe-ledger/runs-confirm/` are not committed.
