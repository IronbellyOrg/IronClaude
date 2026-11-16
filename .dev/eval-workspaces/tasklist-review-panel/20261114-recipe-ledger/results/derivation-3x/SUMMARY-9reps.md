# Recipe Ledger experiment, 9 replicates per arm (derivation check), 2026-11-16

Context for a reader with no history: see `SUMMARY.md` in this folder (the first 3 replicates; what RL, Z0 and K are; the panel; how judging works). This file pools replicates 1 to 9: 81 panel runs (3 arms x 3 study packages x 9), all judged blind by an Opus judge, one judge per run plus a second judge on 12 runs. Replicates 4 to 9 ran under the same driver (`run3.sh`, schedule `schedule-9reps.tsv`, seed 20261117; replicates 1 to 3 used seed 20261116). Owner order 2026-11-16 ("run 6 more").

**Status: exploratory.** Never frozen, no pre-registered gates, no hold-out documents, only the three study packages (the requirements say they are a derivation check, never evidence for adoption). The p-values below were chosen after seeing the data and are not corrected for the three metrics.

## Found of the known defects (designSpec 10 items + makeAlias 4 = 14; sum per replicate over both packages, 9 replicates)

| Arm | Per replicate | Total | Mean per replicate | Runs with at least one find (of 18) |
|---|---|---|---|---|
| Z0 | 0, 0, 1, 0, 1, 1, 1, 1, 1 | 6 | 0.67 | 6 |
| K | 1, 0, 0, 0, 0, 1, 1, 2, 0 | 5 | 0.56 | 4 |
| RL | 2, 3, 1, 2, 3, 3, 3, 1, 0 | 18 | **2.00** | 11 |

- RL against Z0: +1.33 per replicate, permutation test two-sided p = 0.012 (one-sided 0.006). RL against K: +1.44, p = 0.013. (My calculation, 100,000 permutations of the 9 + 9 replicate sums.)
- By package: designSpec RL 14 total, Z0 3, K 5; makeAlias RL 4, Z0 3, K 0. The lead is mostly on designSpec.
- Control package (2 items, 9 runs per arm): RL 2 finds in total, Z0 0, K 0.

## Real blocking finds and wrong blockers (two defect-rich packages, 9 replicates)

| Measure | Z0 | K | RL | RL vs Z0 (two-sided p) |
|---|---|---|---|---|
| Real blocking finds (total) | 3 | 1 | 4 | 1.00: no difference |
| Wrong blockers (blocking findings matching no known defect, total) | 14 | 16 | **5** | 0.005 |

## Time: the +35% cap is NOT met on two of three packages

Panel seconds per run, median over 9 runs:

| Package | Z0 | K | RL | RL / Z0 | K / Z0 |
|---|---|---|---|---|---|
| designSpec | 99 | 121 | 145 | **1.46** | 1.22 |
| makeAlias | 151 | 135 | 156 | 1.03 | 0.90 |
| design (control) | 87 | 101 | 139 | **1.60** | 1.16 |

This corrects the earlier 3-replicate reading (RL/Z0 1.16 to 1.18, "inside the cap"): with 9 replicates the design's per-document rule (median at most 1.35) fails for designSpec and design. The 90th-percentile run is 1.7 to 1.8 times Z0's median on those two packages. Runs finished out of schedule order (see below), so drift is not cancelled by blocks, and elapsed time includes the gateway load of the day.

## Format compliance (RL, 81 reviewer reports)

- With the owner-approved allowances: ledger missing in 1 of 81 (1.2%, limit 10%), 0 format errors, quote validity 803 of 919 (87.4%).
- **Strict reading (nothing forgiven): ledger missing in 47 of 81 (58%), which would FAIL the 10% gate.** Almost all of it is the row-id prefix or suffix slip (481 rows); 7 reports had a heading between the ledger and the findings. The finds above rely on the allowances.
- No fallback, no skipped check, no refused merge in any of the 81 runs. 23 runs are flagged `sandbox_dirty` (the reviewers left `.venv/` and `uv.lock` after they finished; the driver rebuilt the sandbox before every pass, so no run started on a dirty sandbox).
- Second judge: identical found-sets on 12 of 12 re-judged runs. The audit of every judge output flagged nothing (0 bad of 97 judge folders, including leftovers from the first pass).

## How to read it

- **The signal is now stronger than at 3 replicates**, and it comes from two arms that found almost nothing: Z0 and K found at least one defect in only 6 and 4 of 18 runs. RL's advantage is in finding something at all, concentrated on one package.
- **Cost:** RL is slower than the cap on two of three packages.
- **Baseline weakness:** Z0 found 0.67 per replicate here, below the 0.9 the same panel scored in the earlier collaboration experiment, so an inflated gap is possible. Whether the ledger or only the extra reading time helps is not separated: K (plain words, no ledger) found no more than Z0, which argues against "just more instructions".
- **Not tested:** hold-out documents (the real generalisation test), other panels (haiku, sonnet), a frozen pre-registered comparison.
