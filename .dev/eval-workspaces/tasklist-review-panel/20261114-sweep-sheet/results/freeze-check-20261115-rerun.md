# Second freeze check, after the fixture repair (2026-11-15, 21:20 UTC)

Context: see `freeze-check-20261115.md` (the first failing check) and `../OPEN-ITEMS.md`. The recall plans now have repository snapshots (`fixtures/recall/<plan>/snapshot/`, untracked, rebuilt by `fixtures/recall/build-snapshots.sh`) and 5 C8 seeds instead of 1 (41 seeds in all). Report of the repair: `../option1-report/RECALL-REPAIR.md`. No extractor was changed.

## Result: the gate still FAILS

| Extractor | Class | Before (no snapshot) | After | Gate 0.8 | Candidates, hit a seed (after) |
|---|---|---|---|---|---|
| E1 | C1, C6 | 2 / 11 | 2 / 11 | fail | 2 of 60 |
| E2 | C4 | 3 / 6 | 3 / 6 | fail | 52 of 220 |
| E3 | C8 | 0 / 1 | 1 / 5 | fail | 3 of 50 |
| E4 | C5 | 1 / 5 | 1 / 5 | fail | 1 of 47 |
| E7 | C7 | 0 / 7 | 0 / 7 | fail | 0 of 6 |

Command: `uv run --frozen --project <repo> pytest -p no:cacheprovider <SW>/tests/test_recall.py -q -s -m freeze`.

## Correction of my earlier reading

The first note said the missing snapshot probably depressed E2, E3 and E4 and called it a fixture gap. That was only partly right. The recall test runs the extractors' `find` step only (candidates before evidence is attached). The snapshot changed E3 (0 to 50 candidates, recall 0/1 to 1/5) and changed nothing for E1, E2, E4 or E7. So the low recall of E1, E2, E4 and E7 is not a fixture gap.

## What it means

On four plans with defects written by someone who had not read the extractors, the script pre-pass finds the seeded defect's location for roughly 0 to 50% of seeds (pooled: 7 of 34 gated seeds, 21%), against the design's requirement of 80%. Precision is very low (E1 3%, E4 2%, E7 0%): the extractors flag many places that are not defects.

Not known: whether the seeds are typical of real defects; whether a few extra phrasing shapes per extractor would lift recall (the design says a new shape is one new extractor and a re-freeze); how recall moves on a plan not used to adjust the extractors. Nothing has been tuned.

## Options for the owner

1. Iterate the extractors on three of the four plans (a train/test split) with a fresh second-author seeding of a fifth plan as the untouched test; re-run this gate.
2. Stop the Sweep Sheet here and report the result: the deterministic pre-pass does not locate independently written defects well enough. Rely on the Recipe Ledger, which needs no extractor.
3. Keep the design but lower the gate (not recommended: it would be set after seeing the result).
