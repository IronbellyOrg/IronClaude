## Proxy calibration against judged panel rows (46 rows): TP=116 FP=47 FN=14 precision=0.71 recall=0.89

| label | TP | FP | FN |
|---|---|---|---|
| B1 | 0 | 4 | 0 |
| B2 | 0 | 0 | 0 |
| B3 | 42 | 0 | 1 |
| B4 | 2 | 6 | 0 |
| B5 | 1 | 3 | 0 |
| I1 | 1 | 2 | 0 |
| I2 | 21 | 0 | 13 |
| I3 | 2 | 13 | 0 |
| I4 | 1 | 0 | 0 |
| I5 | 0 | 0 | 0 |
| B6 | 0 | 1 | 0 |
| B7 | 10 | 6 | 0 |
| B8 | 1 | 2 | 0 |
| I6 | 0 | 0 | 0 |
| I7 | 2 | 1 | 0 |
| I8 | 33 | 9 | 0 |

## Proxy hit rate per reviewer run (share of that model's runs on the package whose findings match the issue)

| model | B1 (DS, satisfiability) | B2 (DS, satisfiability) | B3 (DS, satisfiability) | B4 (DS, contradiction) | B5 (DS, contradiction) | I1 (DS, contradiction) | I2 (DS, contradiction) | I3 (DS, contradiction) | I4 (DS, satisfiability) | I5 (DS, missing-task/cross-doc) | B6 (AL, contradiction) | B7 (AL, cross-doc) | B8 (AL, cross-doc) | I6 (AL, cross-doc) | I7 (DE, missing-task/cross-doc) | I8 (DE, ambiguity) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ember | 3% | 0% | 65% | 0% | 1% | 1% | 22% | 3% | 0% | 0% | 0% | 3% | 0% | 0% | 0% | 38% |
| luna | 0% | 0% | 10% | 5% | 0% | 0% | 5% | 4% | 0% | 0% | 1% | 17% | 0% | 0% | 0% | 63% |
| haiku | 12% | 0% | 88% | 12% | 12% | 4% | 24% | 20% | 0% | 0% | 0% | 24% | 8% | 0% | 16% | 44% |
| sonnet | 15% | 0% | 100% | 19% | 15% | 12% | 38% | 38% | 15% | 0% | 4% | 15% | 12% | 0% | 23% | 73% |
| grok | 0% | 0% | 62% | 12% | 0% | 38% | 25% | 12% | 0% | 0% | 0% | 12% | 0% | 0% | 12% | 88% |
| terra | 0% | 0% | 14% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 36% | 0% | 0% | 0% | 29% |
| wonder | 12% | 0% | 88% | 0% | 50% | 38% | 75% | 0% | 0% | 0% | 12% | 88% | 0% | 12% | 0% | 88% |

## Proxy hits per run by issue kind (mean number of issues of that kind matched per run on the relevant packages)

| model | cross-doc / missing-task (I5, I7, B7, B8, I6) | satisfiability (B1, B2, B3, I4) | in-plan contradiction (B4, B5, I1, I2, I3, B6) |
|---|---|---|---|
| ember | 0.03 of 5 | 0.68 of 4 | 0.28 of 6 |
| luna | 0.17 of 5 | 0.10 of 4 | 0.15 of 6 |
| haiku | 0.48 of 5 | 1.00 of 4 | 0.72 of 6 |
| sonnet | 0.50 of 5 | 1.31 of 4 | 1.27 of 6 |
| grok | 0.25 of 5 | 0.62 of 4 | 0.88 of 6 |
| terra | 0.36 of 5 | 0.14 of 4 | 0.00 of 6 |
| wonder | 1.00 of 5 | 1.00 of 4 | 1.75 of 6 |
