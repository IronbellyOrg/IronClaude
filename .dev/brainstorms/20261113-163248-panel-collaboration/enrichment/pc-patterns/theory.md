## Theory test A: reasoning budget. Model-level medians and within-model split at the model's own median thinking tokens

| model | median thinking tok | median wall s | GT-proxy hits/run (all) | hard hits/run | low-think: hits/run | high-think: hits/run | low-think: hard/run | high-think: hard/run |
|---|---|---|---|---|---|---|---|---|
| ember | 7094 | 41 | 0.45 | 0.24 | 0.38 (n=104) | 0.53 (n=103) | 0.25 | 0.22 |
| luna | 3560 | 102 | 0.35 | 0.09 | 0.31 (n=123) | 0.39 (n=123) | 0.09 | 0.09 |
| haiku | 45791 | 233 | 0.88 | 0.49 | 0.61 (n=38) | 1.16 (n=37) | 0.29 | 0.70 |
| sonnet | 22862 | 228 | 1.27 | 0.60 | 1.03 (n=39) | 1.51 (n=39) | 0.46 | 0.74 |
| grok | 48528 | 790 | 0.88 | 0.29 | 0.50 (n=12) | 1.25 (n=12) | 0.08 | 0.50 |
| terra | 336 | 54 | 0.26 | 0.17 | 0.14 (n=21) | 0.38 (n=21) | 0.14 | 0.19 |
| wonder | 11206 | 134 | 1.54 | 0.67 | 1.42 (n=12) | 1.67 (n=12) | 0.67 | 0.67 |

Spearman rho across the 7 models, median thinking tokens vs GT-proxy hits/run: 0.64

## Theory test B: search scope. Repo files touched per run, split into files the plan names and files it does not

| model | plan-named files/run | not-plan-named files/run | share of runs touching any not-plan-named test file | share touching test_worker_contract.py (DE) | share touching CHANGELOG.md (DS) | DE I7 proxy hit | DS I5 proxy hit |
|---|---|---|---|---|---|---|---|
| ember | 15.4 | 0.8 | 8% | 0% | 0% | 0% | 0% |
| luna | 7.7 | 0.3 | 1% | 0% | 0% | 0% | 0% |
| haiku | 16.7 | 0.9 | 0% | 0% | 0% | 16% | 0% |
| sonnet | 14.1 | 3.1 | 35% | 27% | 0% | 23% | 0% |
| grok | 15.2 | 1.2 | 33% | 12% | 12% | 12% | 0% |
| terra | 6.0 | 0.9 | 2% | 0% | 0% | 0% | 0% |
| wonder | 18.8 | 1.1 | 25% | 0% | 0% | 0% | 0% |

DE runs touching test_worker_contract.py: 8 (models {'sonnet': 7, 'grok': 1}); I7 proxy hit among them 7/8; among the other 225 runs 4/225

## Theory test C: report shape. Volume, locality and grading

| model | findings/run | share of runs with <=1 finding | blocking share of findings | local findings (one section, no anchor2) | category other | missing-requirement findings/run | non-blocking findings/run |
|---|---|---|---|---|---|---|---|
| ember | 4.19 | 1% | 14% | 46% | 43% | 1.09 | 3.61 |
| luna | 1.75 | 46% | 72% | 37% | 9% | 0.37 | 0.50 |
| haiku | 8.35 | 0% | 17% | 33% | 46% | 2.11 | 6.95 |
| sonnet | 6.36 | 0% | 4% | 30% | 26% | 2.51 | 6.08 |
| grok | 3.92 | 0% | 33% | 16% | 20% | 1.00 | 2.62 |
| terra | 2.45 | 33% | 82% | 22% | 7% | 0.31 | 0.45 |
| wonder | 5.38 | 0% | 21% | 18% | 30% | 1.54 | 4.25 |

Within-model: GT-proxy hits/run by findings-count tercile (low / mid / high)

| model | low | mid | high |
|---|---|---|---|
| ember | 0.25 (findings 2.8) | 0.52 (findings 4.2) | 0.59 (findings 5.6) |
| luna | 0.13 (findings 0.8) | 0.28 (findings 1.6) | 0.63 (findings 2.8) |
| haiku | 0.64 (findings 6.3) | 0.68 (findings 8.2) | 1.32 (findings 10.6) |
| sonnet | 1.23 (findings 4.5) | 0.92 (findings 6.6) | 1.65 (findings 8.0) |
| grok | 0.75 (findings 2.8) | 0.38 (findings 3.9) | 1.50 (findings 5.1) |
| terra | 0.07 (findings 0.1) | 0.21 (findings 3.0) | 0.50 (findings 4.3) |
| wonder | 2.12 (findings 4.2) | 1.12 (findings 5.4) | 1.38 (findings 6.5) |

## Skill invocation (luna, grok): runs that called the sc:spec-panel Skill vs runs that did not

| model | skill runs | findings/run (skill) | findings/run (no skill) | GT hits/run (skill) | GT hits/run (no skill) | repo files (skill) | repo files (no skill) |
|---|---|---|---|---|---|---|---|
| luna | 207/246 | 1.79 | 1.51 | 0.35 | 0.36 | 8.1 | 7.6 |
| grok | 16/24 | 3.88 | 4.00 | 0.94 | 0.75 | 16.6 | 16.0 |
