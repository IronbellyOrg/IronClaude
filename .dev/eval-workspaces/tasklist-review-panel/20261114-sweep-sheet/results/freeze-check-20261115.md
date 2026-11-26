# First freeze check: extractor recall on independently seeded plans (2026-11-15)

Context for a reader with no history: the Sweep Sheet design relies on a script pre-pass (extractors E1 to E7) that finds, in a plan, the places where a defect of a given class (C1 to C8) can hide. The design's freeze gate (REQ-21, test `tests/test_recall.py`, marker `freeze`) requires recall of at least 0.8 for E1, E2, E3, E4 and E7 on plans in which a second author, who had not read the extractors, seeded defects. See `../OPEN-ITEMS.md` and `../../OPEN-QUESTIONS-20261115.md`.

## What was run

- Fixtures: `fixtures/recall/` written by a fresh Sonnet session (not a person) on 2026-11-15: 4 real plans, 37 seeds (C1 5, C2 7, C4 6, C5 5, C6 6, C7 7, C8 1). Report: `second-author-report/REPORT.md`. The session did not run any extractor.
- Command: `uv run --frozen --project <repo> pytest -p no:cacheprovider <SW>/tests -q -m freeze`.

## Result: the gate FAILS

| Extractor | Class | Seeds found / seeded | Recall (gate 0.8) | Candidates produced, how many hit a seed (precision) |
|---|---|---|---|---|
| E1 | C1, C6 | 2 / 11 | 0.18 | 2 of 60 (0.03) |
| E2 | C4 | 3 / 6 | 0.50 | 52 of 220 (0.24) |
| E3 | C8 | 0 / 1 | 0.00 | 0 of 0 |
| E4 | C5 | 1 / 5 | 0.20 | 1 of 47 (0.02) |
| E7 | C7 | 0 / 7 | 0.00 | 0 of 6 |
| E6 (experimental, not gated) | C3 | no seeds | n/a | 0 of 45 |
| E5 (needs source) | C2 | not in the gated list | n/a | 0 of 0 |

The other freeze test, the lint against the real ground-truth files, fails only because `LINT_REAL_GT_GLOB` is not set (it was not run).

## How to read it (and what is not known)

- **The result is real but not yet a verdict on the design.** The extractors were built from the design's description of defect shapes and tested here for the first time against defects someone else wrote. Low recall means the shapes the extractors recognise do not match how independent seeds are phrased, or that the seeds are not the kind of defect the extractors target. This note does not say which.
- **E2 to E4 ran without a repository snapshot.** The test contract searches the repository only if `fixtures/recall/<plan>/snapshot/` exists; the second author did not provide one (the instruction did not require it). Evidence-searching extractors therefore had no tree to search. This depresses E2, E3 and E4 and is a fixture gap, not an extractor result. E1 and E7 do not depend on a snapshot, and they scored 0.18 and 0.00.
- **C8 has one seed**, so its recall figure means nothing.
- **Matching is strict:** a candidate counts only if its class equals the seed's and its anchor text contains the quote or is contained in it.
- **Class labels of seeds can be ambiguous** (the second author notes some seeds fit two classes).
- **Nothing has been tuned.** No extractor was changed after seeing this result. Tuning extractors to these four plans is allowed by the design (they are not hold-out documents) but would risk overfitting four plans; the hold-out test later is the real check.

## Options for the owner

1. **Diagnose, then fix the fixtures first:** add `snapshot/` checkouts to the recall plans (pre-implementation commits of each plan), add C8 seeds, and re-run. This isolates how much of the failure is the missing snapshot.
2. **Then iterate the extractors** on three of the four plans and test on the fourth (train/test split), with the second author re-seeding at least one new plan for a fresh check; re-run the gate.
3. **Stop the Sweep Sheet** if recall stays far below 0.8 after fair fixes, and rely on the Recipe Ledger (which has no extractor). Report this as the finding.

Nothing is committed. The freeze, the tag and the hash list wait on this.
