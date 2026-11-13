## T1 Tool-use profile per model (median per run unless marked)

| model | runs | tool calls | Read | Bash | Grep+Glob | MCP (codegraph/augment/...) | Web | distinct repo files (Read or named in Bash) | runs reading source.md | runs touching a plan-named repo file | runs touching any test file | runs touching a plan-named test file | runs touching any .py/.sh code | turns | wall s | output tok |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ember | 207 | 12 | 2 | 8 | 0 | 0 (mean 0.0) | 0.00 mean | 15 (mean 16.2) | 55% | 99% | 95% | 95% | 67% | 13 | 41 | 10531 |
| luna | 246 | 14.0 | 11.0 | 1.0 | 0.0 | 0.0 (mean 1.6) | 0.00 mean | 8.0 (mean 8.0) | 78% | 93% | 85% | 85% | 52% | 16.0 | 102.0 | 4894.5 |
| haiku | 75 | 9 | 2 | 5 | 0 | 0 (mean 0.0) | 0.49 mean | 16 (mean 17.6) | 69% | 100% | 100% | 100% | 67% | 10 | 233 | 53797 |
| sonnet | 78 | 15.0 | 2.0 | 12.0 | 0.0 | 0.0 (mean 0.0) | 0.26 mean | 17.0 (mean 17.3) | 99% | 100% | 100% | 100% | 67% | 16.0 | 227.5 | 30457.5 |
| grok | 24 | 31.0 | 11.5 | 10.0 | 0.0 | 2.0 (mean 8.8) | 0.00 mean | 16.0 (mean 16.4) | 83% | 100% | 100% | 100% | 62% | 33.5 | 790.0 | 53130.5 |
| terra | 42 | 11.5 | 9.0 | 2.0 | 0.0 | 0.0 (mean 0.5) | 0.00 mean | 7.0 (mean 6.8) | 100% | 88% | 76% | 76% | 40% | 12.5 | 54.5 | 2286.5 |
| wonder | 24 | 18.0 | 8.5 | 9.5 | 0.0 | 0.0 (mean 0.0) | 0.00 mean | 17.5 (mean 19.8) | 75% | 100% | 100% | 100% | 67% | 19.0 | 133.5 | 15770.5 |
| sol | 3 | 19 | 15 | 4 | 0 | 0 (mean 0.7) | 0.00 mean | 11 (mean 14.0) | 100% | 100% | 100% | 100% | 67% | 21 | 154 | 3870 |

### T1a Method markers (share of runs)

| model | invoked a Skill | Read the candidate with a tool | repo files via Read tool (mean) | searched or opened tests/ | ran pytest | ran code/make/ruff | used codegraph/augment MCP | median thinking tokens |
|---|---|---|---|---|---|---|---|---|
| ember | 1% | 64% | 2.4 | 96% | 11% | 27% | 1% | 7094 |
| luna | 84% | 13% | 8.0 | 85% | 2% | 0% | 38% | 3559.5 |
| haiku | 0% | 67% | 1.0 | 100% | 20% | 36% | 4% | 45791 |
| sonnet | 0% | 77% | 1.4 | 100% | 22% | 45% | 1% | 22861.5 |
| grok | 67% | 12% | 6.7 | 100% | 12% | 29% | 62% | 48528.5 |
| terra | 0% | 0% | 5.7 | 76% | 17% | 0% | 36% | 336.5 |
| wonder | 0% | 71% | 5.7 | 100% | 12% | 12% | 0% | 11206.5 |
| sol | 33% | 100% | 9.7 | 100% | 33% | 33% | 33% | 766 |

### T1b Tool-use per model per package (mean distinct repo files / share opening any test file / mean tool calls)

| model | DS files | DS test% | DS calls | AL files | AL test% | AL calls | DE files | DE test% | DE calls |
|---|---|---|---|---|---|---|---|---|---|
| ember | 12.8 (n=69) | 96% | 11.4 | 23.0 (n=69) | 97% | 15.2 | 12.7 (n=69) | 93% | 12.5 |
| luna | 4.5 (n=82) | 66% | 11.7 | 10.8 (n=82) | 95% | 17.9 | 8.8 (n=82) | 95% | 13.5 |
| haiku | 15.6 (n=25) | 100% | 8.0 | 27.3 (n=25) | 100% | 10.6 | 10.0 (n=25) | 100% | 10.5 |
| sonnet | 14.6 (n=26) | 100% | 15.1 | 24.5 (n=26) | 100% | 18.7 | 12.8 (n=26) | 100% | 15.2 |
| grok | 16.1 (n=8) | 100% | 45.6 | 19.0 (n=8) | 100% | 33.8 | 14.1 (n=8) | 100% | 26.8 |
| terra | 2.5 (n=14) | 36% | 7.4 | 10.6 (n=14) | 100% | 17.4 | 7.4 (n=14) | 93% | 11.1 |
| wonder | 15.0 (n=8) | 100% | 16.5 | 29.5 (n=8) | 100% | 27.9 | 15.0 (n=8) | 100% | 17.0 |
| sol | 8.0 (n=1) | 100% | 18.0 | 23.0 (n=1) | 100% | 29.0 | 11.0 (n=1) | 100% | 19.0 |

### T1c Share of runs that opened specific repo files tied to ground-truth issues

| model | DE:test_worker_contract.py | DE:test_issue_protocol.py | DS:CHANGELOG.md | DS:fsm.py | DS:run_log.py | DS:models.py | AL:ccsession-models.json | AL:commands.py | AL:test_issue_worker_agents.py |
|---|---|---|---|---|---|---|---|---|---|
| ember | 0% | 93% | 0% | 84% | 91% | 99% | 91% | 100% | 46% |
| luna | 0% | 95% | 0% | 21% | 35% | 22% | 63% | 40% | 24% |
| haiku | 0% | 100% | 0% | 68% | 84% | 92% | 96% | 100% | 64% |
| sonnet | 27% | 100% | 0% | 85% | 96% | 81% | 77% | 96% | 54% |
| grok | 12% | 100% | 12% | 38% | 50% | 50% | 75% | 100% | 0% |
| terra | 0% | 93% | 0% | 0% | 0% | 7% | 7% | 100% | 7% |
| wonder | 0% | 100% | 0% | 62% | 88% | 88% | 100% | 100% | 75% |
| sol | 0% | 100% | 0% | 0% | 100% | 0% | 0% | 100% | 100% |

## T2 Report profile per model

| model | findings/run (median, mean) | blocking/run (mean) | anchor located in candidate | findings citing source.md | findings spanning >=2 Tasks | findings spanning >=2 sections (incl. Constraints/Goal) | with anchor2 | citing a repo file in refs | contradiction | unpassable-check | missing-requirement | other | data-loss/safety | distinct Tasks anchored/run (mean) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ember | 4, 4.19 | 0.57 | 98% | 14% | 30% | 45% | 28% | 1% | 19% | 11% | 26% | 43% | 0% | 4.57 |
| luna | 2.0, 1.75 | 1.25 | 93% | 25% | 21% | 58% | 51% | 9% | 35% | 34% | 21% | 9% | 1% | 1.91 |
| haiku | 8, 8.35 | 1.40 | 99% | 9% | 39% | 54% | 47% | 4% | 15% | 13% | 25% | 46% | 1% | 7.60 |
| sonnet | 7.0, 6.36 | 0.28 | 100% | 22% | 42% | 57% | 54% | 1% | 20% | 15% | 40% | 26% | 0% | 6.24 |
| grok | 4.0, 3.92 | 1.29 | 97% | 44% | 46% | 60% | 76% | 1% | 27% | 24% | 26% | 20% | 3% | 4.71 |
| terra | 3.0, 2.45 | 2.00 | 99% | 6% | 34% | 67% | 61% | 2% | 50% | 29% | 13% | 7% | 2% | 2.50 |
| wonder | 5.0, 5.38 | 1.12 | 100% | 19% | 57% | 71% | 57% | 1% | 27% | 12% | 29% | 30% | 2% | 6.58 |
| sol | 2, 2.67 | 2.00 | 100% | 25% | 50% | 75% | 50% | 0% | 25% | 38% | 12% | 12% | 12% | 4.33 |

### T2b Finding content markers (share of findings whose claim matches)

| model | claim names a missing/omitted update | claim names a test/test file | claim names a repo path |
|---|---|---|---|
| ember | 11% | 26% | 1% |
| luna | 9% | 19% | 1% |
| haiku | 9% | 25% | 2% |
| sonnet | 10% | 29% | 2% |
| grok | 5% | 28% | 1% |
| terra | 12% | 34% | 0% |
| wonder | 16% | 29% | 2% |
| sol | 12% | 38% | 0% |

## T3 Task anchoring: concentration per model per package

Share of a model's task anchors (across all its runs on that package) that fall in its 3 most-cited tasks, and the top tasks with run share (share of runs citing that task).

| model | pkg | runs | task anchors | top-3 share | top tasks (share of runs citing) | distinct tasks ever |
|---|---|---|---|---|---|---|
| ember | DS | 69 | 345 | 39% | T9 74%, T4 58%, T1 52%, T7 52% | 13 |
| luna | DS | 82 | 130 | 50% | T4 37%, T8 23%, T11 18%, T3 17% | 12 |
| haiku | DS | 25 | 359 | 38% | T8 96%, T3 100%, T1 92%, T13 84% | 13 |
| sonnet | DS | 26 | 226 | 46% | T8 77%, T4 85%, T9 100%, T10 69% | 12 |
| grok | DS | 8 | 56 | 55% | T4 88%, T3 88%, T11 75%, T9 75% | 10 |
| terra | DS | 14 | 7 | 71% | T9 14%, T3 7%, T2 7%, T7 7% | 5 |
| wonder | DS | 8 | 70 | 44% | T4 75%, T8 88%, T9 100%, T7 88% | 10 |
| sol | DS | 1 | 3 | 100% | T4 100%, T8 100%, T9 100% | 3 |
| ember | AL | 69 | 415 | 63% | T1 96%, T9 77%, T2 65%, T6 57% | 9 |
| luna | AL | 82 | 204 | 70% | T9 70%, T1 54%, T5 30%, T6 27% | 9 |
| haiku | AL | 25 | 327 | 57% | T1 100%, T9 96%, T6 92%, T2 100% | 9 |
| sonnet | AL | 26 | 232 | 61% | T1 100%, T9 92%, T2 92%, T6 69% | 9 |
| grok | AL | 8 | 47 | 68% | T1 100%, T9 100%, T2 75%, T6 62% | 8 |
| terra | AL | 14 | 75 | 84% | T1 93%, T9 93%, T6 57%, T8 29% | 8 |
| wonder | AL | 8 | 86 | 66% | T6 100%, T9 100%, T1 100%, T2 88% | 8 |
| sol | AL | 1 | 11 | 55% | T1 100%, T6 100%, T9 100%, T2 100% | 8 |
| ember | DE | 69 | 405 | 55% | T1 75%, T12 96%, T8 74%, T2 51% | 11 |
| luna | DE | 82 | 206 | 91% | T12 91%, T1 63%, T2 20%, T6 10% | 10 |
| haiku | DE | 25 | 290 | 47% | T2 100%, T1 88%, T12 100%, T8 92% | 12 |
| sonnet | DE | 26 | 295 | 57% | T2 100%, T3 100%, T12 96%, T8 96% | 10 |
| grok | DE | 8 | 46 | 72% | T1 100%, T2 100%, T12 50%, T10 50% | 9 |
| terra | DE | 14 | 66 | 77% | T12 100%, T1 93%, T2 93%, T6 71% | 6 |
| wonder | DE | 8 | 71 | 54% | T2 100%, T1 100%, T8 100%, T12 88% | 12 |
| sol | DE | 1 | 2 | 100% | T12 100%, T2 100% | 2 |

### T3b Share of runs that anchor at least one finding in the task where a ground-truth issue lives

| model | DE GT1(missing-task: T12 gate + T2/3/5 edits) | DE GT2(ambiguity T1 read-back) | DS GT1/GT2(T1 AC3) | DS GT3(T9) | DS GT4/GT5(T8) | DS GT8(T10) | DS GT6(T3) | DS GT7(T4 resume sig) | DS GT9(T12 grep) | DS GT10(T2 changelog) | AL GT1/GT2(T6) | AL GT3/GT4(T7) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ember | 96% | 75% | 52% | 74% | 33% | 29% | 32% | 58% | 14% | 46% | 57% | 13% |
| luna | 91% | 63% | 10% | 13% | 23% | 7% | 17% | 37% | 2% | 6% | 27% | 6% |
| haiku | 100% | 88% | 92% | 100% | 96% | 76% | 100% | 80% | 24% | 80% | 92% | 56% |
| sonnet | 96% | 81% | 50% | 100% | 77% | 69% | 46% | 85% | 23% | 8% | 69% | 27% |
| grok | 50% | 100% | 50% | 75% | 50% | 50% | 88% | 88% | 0% | 12% | 62% | 12% |
| terra | 100% | 93% | 0% | 14% | 0% | 0% | 7% | 7% | 0% | 7% | 57% | 0% |
| wonder | 88% | 100% | 50% | 100% | 88% | 50% | 75% | 75% | 62% | 0% | 100% | 38% |
| sol | 100% | 0% | 0% | 100% | 100% | 0% | 0% | 100% | 0% | 0% | 100% | 0% |

## T4 Pairwise Jaccard of anchored Task sets between reviewers in the same row and package

| pair | n pairs | mean Jaccard | share with zero overlap |
|---|---|---|---|
| ember+luna | 246 | 0.25 | 19% |
| luna+luna | 90 | 0.33 | 37% |
| luna+sonnet | 78 | 0.21 | 22% |
| ember+haiku | 57 | 0.47 | 2% |
| haiku+luna | 57 | 0.23 | 16% |
| ember+sonnet | 57 | 0.43 | 0% |
| ember+ember | 54 | 0.41 | 6% |
| ember+terra | 30 | 0.25 | 37% |
| haiku+sonnet | 21 | 0.55 | 0% |
| haiku+terra | 18 | 0.35 | 28% |
| grok+haiku | 18 | 0.44 | 0% |
| grok+luna | 15 | 0.20 | 27% |
| luna+wonder | 12 | 0.14 | 25% |
| haiku+wonder | 12 | 0.63 | 0% |
| grok+wonder | 9 | 0.53 | 0% |
| sonnet+wonder | 9 | 0.54 | 0% |
| grok+sonnet | 9 | 0.36 | 0% |
| terra+wonder | 6 | 0.34 | 33% |
| luna+terra | 6 | 0.25 | 33% |
| ember+grok | 6 | 0.36 | 0% |
| haiku+haiku | 6 | 0.67 | 0% |

### T4b Run-to-run Jaccard of anchored Task sets for the same model on the same package (all pairs of runs)

| model | DS | AL | DE |
|---|---|---|---|
| ember | 0.30 (runs=69) | 0.46 (runs=69) | 0.42 (runs=69) |
| luna | 0.12 (runs=82) | 0.33 (runs=82) | 0.53 (runs=82) |
| haiku | 0.67 (runs=25) | 0.72 (runs=25) | 0.64 (runs=25) |
| sonnet | 0.51 (runs=26) | 0.61 (runs=26) | 0.70 (runs=26) |
| grok | 0.44 (runs=8) | 0.58 (runs=8) | 0.49 (runs=8) |
| terra | 0.01 (runs=14) | 0.52 (runs=14) | 0.73 (runs=14) |
| wonder | 0.55 (runs=8) | 0.70 (runs=8) | 0.59 (runs=8) |
| sol | - | - | - |

## T5 Within-model link between exploration and report shape

Runs split at the model's own median of distinct repo files read; mean findings per run, share of runs with a finding that names a test, share of runs anchoring any GT task.

| model | low-explore runs | findings (low) | findings (high) | test-claim runs (low) | test-claim runs (high) |
|---|---|---|---|---|---|
| ember | 115 (<= 15) | 4.23 | 4.14 (n=92) | 73% | 74% |
| luna | 133 (<= 8.0) | 1.49 | 2.05 (n=113) | 20% | 41% |
| haiku | 42 (<= 16) | 8.21 | 8.52 (n=33) | 93% | 97% |
| sonnet | 45 (<= 17.0) | 6.24 | 6.52 (n=33) | 96% | 100% |
| grok | 13 (<= 16.0) | 3.85 | 4.00 (n=11) | 46% | 91% |
| terra | 22 (<= 7.0) | 1.55 | 3.45 (n=20) | 32% | 75% |
| wonder | 12 (<= 17.5) | 5.33 | 5.42 (n=12) | 92% | 100% |
