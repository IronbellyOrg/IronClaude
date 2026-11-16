# Recipe Ledger experiment, 3 replicates (derivation check), 2026-11-16

Context for a reader with no history: the Recipe Ledger (RL) asks each cheap reviewer to run eight written recipes (one per class of plan defect) and to write a ledger of one row per recipe step before writing findings. This experiment compares it with two controls on the three study packages: Z0 (the plain panel with the harness fixes and brief edits) and K (the eight checks in plain words, no ledger). Panel: muse-ember-1.0 + 2 x gpt-6-luna (primary panel). Each arm ran 3 replicates on each of 3 packages: 27 panel runs, one at a time. Judging: blind Opus judge, one judge per run plus a second judge on 4 runs. Owner order 2026-11-16. Background: `../../../OPEN-QUESTIONS-20261115.md`, `../../POST-BUILD-LOG-20261115.md`.

**Status of this evidence: exploratory.** The design was never frozen, no hold-out documents exist, and the requirements say the study packages are only a derivation check, never evidence for adoption. n = 3 per cell.

## Result: found of the known defects (judge credit; GT: designSpec 10 items, makeAlias 4, design 2 = control)

| Arm | designSpec (3 runs) | makeAlias (3 runs) | design, control (3 runs) | Both defect-rich packages, found per replicate (sum of 14 possible) |
|---|---|---|---|---|
| Z0 | 0, 0, 0 | 0, 0, 1 | 0, 0, 0 | 0, 0, 1 (mean 0.33) |
| K | 1, 0, 0 | 0, 0, 0 | 0, 0, 0 | 1, 0, 0 (mean 0.33) |
| RL | 1, 3, 1 | 1, 0, 0 | 0, 1, 0 | 2, 3, 1 (mean 2.00) |

- **RL found 6 defects in total, Z0 and K found 1 each.** Most of RL's finds are on designSpec (5 of 6).
- **Not statistically established.** Exact permutation test on the three replicate sums, RL against Z0 or K: one-sided p = 0.10, two-sided p = 0.20 (my calculation; with 3 versus 3 the smallest possible one-sided p is 0.05).
- **Real blocking finds** (found items that would block the implementer): RL 1, Z0 1, K 0. No difference.
- **Wrong blockers** (blocking findings that match no known defect), summed over the 3 replicates on the two defect-rich packages: RL 3, Z0 5, K 7. Fewer for RL, also not established.
- **Control package:** RL found 1 of its 2 items in one run, Z0 and K none.
- **Second judge** agreed with the first on 4 of 4 re-judged runs (3 with no finds, 1 with GT3). The audit of every judge output flagged nothing (0 bad of 31 judgings, plus one orphan folder from the first pass).

## Time (panel seconds per run, the clock the design uses)

| Package | Z0 | K | RL | RL / Z0 median |
|---|---|---|---|---|
| designSpec | 99, 138, 129 | 128, 150, 150 | 152, 179, 136 | 1.18 |
| makeAlias | 142, 153, 102 | 140, 180, 169 | 148, 194, 164 | 1.16 |
| design | 67, 69, 89 | 76, 85, 101 | 80, 82, 139 | 1.18 |

Same-package median ratios for RL are 1.16 to 1.18, inside the +35% cap. (A pooled median ratio of 1.45 over all runs is not meaningful: it mixes packages of different size.) Runs finished out of schedule order (see below), so load drift is not cancelled by the block design.

## Format compliance (RL)

- With the owner-approved allowances: ledger missing in 0 of 27 reviewer reports, 0 format errors, quote validity 262 of 292 (89.7%), about 10 to 12 rows per reviewer, no run used the ember re-ask, no fallback, no killed reviewer, no refused merge.
- **Strict reading (nothing forgiven): ledger missing in 16 of 27 reports (59%), which would FAIL the 10% gate.** Almost all of it is one slip: the row id written with a prefix or suffix (166 rows); 3 reports had a heading between the ledger and the findings. The finds above depend on the allowances. Recipes not run: C2 2, C3 1, C4 1, C7 1.

## What went wrong or limits the reading

1. **First pass finished only 9 of 27 runs.** The reviewers leave `.venv/` and `uv.lock` in the sandbox and the launcher refuses a dirty sandbox (known gap, item 6 of `POST-BUILD-LOG-20261115.md`). A second driver (`run2.sh`) rebuilt dirty sandboxes before each of six passes and re-ran the schedule. No run used a dirty sandbox; 9 runs are flagged `sandbox_dirty` because they left residue after they finished.
2. **Block randomisation is broken** by the reruns: refused runs waited for a later pass.
3. **One package dominates.** Z0 and K almost never found anything on any package; RL found its defects mostly on designSpec.
4. **The control package** has only 2 items, so it says little about false positives.
5. **No hold-out test, no freeze, no shared control, no parity test.** The sibling redesign (Sweep Sheet) was stopped and its shared pieces (cards, briefs) are provisional copies.
6. **Earlier numbers do not transfer:** the same-harness baseline in the collaboration experiment found about 0.9 per run on ember; Z0 here found 0.33.

## Where the files are

`scores-table.json` (per-run scores), `schedule.tsv`, `run.log` and `run2.log`, `schedule-run*.out`, `judge-run*.out`; run folders under `../../runs/staged1-*`; blind-judge folders under `../../scoring/`.
