# Reviewer behaviour patterns per model (tool use, report shape, coverage overlap)

Date: 2026-11-13. Read-only quantitative investigation. Scripts and scratch output: `/tmp/pc-patterns/` (`collect.py`, `analyze.py`, `gtproxy.py`, `theory.py`, `rev.py`; tables in `out.md`, `gt.md`, `theory.md`, `rev.md`, `surf.md`).

Data: `EVAL=.dev/eval-workspaces/tasklist-review-panel/20261111-a1`. Rows: every run with era `source.md` in `EVAL/analysis/allsets/allsets.json` (76 rows). Reviewer runs: `EVAL/<pkg>/reviews/combos/<row>/<rid>.meta.json` for the three packages, 699 reviewer runs, all `model_ok: true`, no duplicate reports (sha256 of `<rid>.md`). For each run the transcript used is the `<rid>.attempt<N>.json` whose `.attempt<N>.md` is byte-identical to `<rid>.md` (matched for 699/699). Model comes from `observed_model` (`grok-4.7-build` mapped to grok).

Package short names: DS = `TASK-WF-designSpec-20261107-075614`, AL = `TASK-WF-makeTheAliasOnly-20261105-051649`, DE = `TASK-WF-design-20261108-041415`.

Runs per model: luna 246, ember 207, sonnet 78, haiku 75, terra 42, grok 24, wonder 24, sol 3 (sol left out of comparisons).

## 1. Tool-use profile

The reviewer sandbox exposes Read and Bash but no Grep or Glob tool (the `system/init` tool list in every transcript), so all searching happens through Bash. Every reviewer runs with cwd `/tmp/evalsb/repo`, so most Bash commands use relative paths; "files touched" below counts files opened with Read plus file paths named in Bash commands (grep, sed, cat, wc, ls). That over-counts content actually read for Bash-heavy models.

Medians per run unless marked.

| model | tool calls | Read | Bash | MCP calls (mean) | repo files touched (mean) | read source.md | touched any test file | turns | wall s | output tok | thinking tok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ember | 12 | 2 | 8 | 0.0 | 15 (16.2) | 55% | 95% | 13 | 41 | 10,531 | 7,094 |
| luna | 14 | 11 | 1 | 1.6 | 8 (8.0) | 78% | 85% | 16 | 102 | 4,895 | 3,560 |
| haiku | 9 | 2 | 5 | 0.0 | 16 (17.6) | 69% | 100% | 10 | 233 | 53,797 | 45,791 |
| sonnet | 15 | 2 | 12 | 0.0 | 17 (17.3) | 99% | 100% | 16 | 228 | 30,458 | 22,862 |
| grok | 31 | 11.5 | 10 | 8.8 | 16 (16.4) | 83% | 100% | 33.5 | 790 | 53,131 | 48,529 |
| terra | 11.5 | 9 | 2 | 0.5 | 7 (6.8) | 100% | 76% | 12.5 | 54.5 | 2,287 | 336 |
| wonder | 18 | 8.5 | 9.5 | 0.0 | 17.5 (19.8) | 75% | 100% | 19 | 134 | 15,771 | 11,207 |

Method markers (share of runs):

| model | called the sc:spec-panel Skill | ran pytest | ran code, make or ruff | recursive repo search (grep -r, rg, find, git grep) | recursive search over tests/ or repo root | recursive search segments per run |
|---|---|---|---|---|---|---|
| ember | 1% | 11% | 27% | 78% | 49% | 3.7 |
| luna | 84% | 2% | 0% | 23% | 4% | 0.2 |
| haiku | 0% | 20% | 36% | 92% | 81% | 5.2 |
| sonnet | 0% | 22% | 45% | 96% | 94% | 6.7 |
| grok | 67% | 12% | 29% | 92% | 79% | 4.0 |
| terra | 0% | 17% | 0% | 31% | 24% | 0.5 |
| wonder | 0% | 12% | 12% | 96% | 88% | 7.8 |

Files the plan names versus files it does not name (mean per run):

| model | plan-named files touched | files touched that the plan does not name | runs touching a test file the plan does not name | DE: touched `tests/skills/test_worker_contract.py` | DS: touched `CHANGELOG.md` |
|---|---|---|---|---|---|
| ember | 15.4 | 0.8 | 8% | 0/69 | 0/69 |
| luna | 7.7 | 0.3 | 1% | 0/82 | 0/82 |
| haiku | 16.7 | 0.9 | 0% | 0/25 | 0/25 |
| sonnet | 14.1 | 3.1 | 35% | 7/26 | 0/26 |
| grok | 15.2 | 1.2 | 33% | 1/8 | 1/8 |
| terra | 6.0 | 0.9 | 2% | 0/14 | 0/14 |
| wonder | 18.8 | 1.1 | 25% | 0/8 | 0/8 |

Observations:

- luna reads whole files with the Read tool (median 11 Reads) and almost never searches (0.2 recursive searches per run, 4% of runs search tests/). It calls the sc:spec-panel Skill in 84% of runs; Skill and non-Skill luna runs do not differ (findings 1.79 vs 1.51, proxy hits 0.35 vs 0.36).
- ember touches as many files as sonnet and haiku through Bash (`ls`, `grep -n` on named files), but its median wall time is 41 s and median thinking is 7.1k tokens, against 228 s and 22.9k for sonnet.
- haiku searches the repo as much as sonnet (81% of runs search tests/), yet opened `test_worker_contract.py` in 0 of 25 DE runs: its searches target the test file the plan names (`tests/skills/test_issue_protocol.py`).

## 2. Report profile (findings-v1 block)

Task attribution: Task numbers from `refs`, plus the candidate section that contains `anchor` or `anchor2` (anchors located in the candidate for 93% to 100% of findings per model).

| model | findings/run (mean) | runs with at most 1 finding | blocking share | findings citing source.md | spanning 2 or more Tasks | with anchor2 | local (one section, no anchor2) | contradiction | unpassable-check | missing-requirement | other | distinct Tasks anchored per run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ember | 4.19 | 1% | 14% | 14% | 30% | 28% | 46% | 19% | 11% | 26% | 43% | 4.57 |
| luna | 1.75 | 46% | 72% | 25% | 21% | 51% | 37% | 35% | 34% | 21% | 9% | 1.91 |
| haiku | 8.35 | 0% | 17% | 9% | 39% | 47% | 33% | 15% | 13% | 25% | 46% | 7.60 |
| sonnet | 6.36 | 0% | 4% | 22% | 42% | 54% | 30% | 20% | 15% | 40% | 26% | 6.24 |
| grok | 3.92 | 0% | 33% | 44% | 46% | 76% | 16% | 27% | 24% | 26% | 20% | 4.71 |
| terra | 2.45 | 33% | 82% | 6% | 34% | 61% | 22% | 50% | 29% | 13% | 7% | 2.50 |
| wonder | 5.38 | 0% | 21% | 19% | 57% | 57% | 18% | 27% | 12% | 29% | 30% | 6.58 |

Only 1% to 9% of findings put a repo file in `refs`; findings almost never cite repo evidence in the block itself.

Surface or process findings (claim about the artifact path or edit scope, the hash, or line numbers): ember 21%, luna 23%, terra 18%, haiku 12%, wonder 13%, grok 12%, sonnet 9%. Among blocking findings: luna 31% (n=308), terra 20%, ember 15%, sonnet 14% (n=22), haiku 9%. On DE, 72 of luna's 212 findings (34%) are the Task 12 "artifact outside the edit scope" finding, which the judge scores as a wrong blocker (for example `EVAL/arms/scoring/combos/g6-luna2-ember2-r1/TASK-WF-design-20261108-041415/R/score.json`).

## 3. Coverage overlap and concentration

Pairwise Jaccard of the Task sets two reviewers in the same row and package anchored (selected pairs; the full list is in `/tmp/pc-patterns/out.md`):

| pair | pairs | mean Jaccard | zero overlap |
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
| grok+haiku | 18 | 0.44 | 0% |
| grok+luna | 15 | 0.20 | 27% |
| haiku+wonder | 12 | 0.63 | 0% |
| grok+sonnet | 9 | 0.36 | 0% |

Run-to-run Jaccard for one model on one package (how repeatable its focus is), DS / AL / DE: ember 0.30 / 0.46 / 0.42; luna 0.12 / 0.33 / 0.53; haiku 0.67 / 0.72 / 0.64; sonnet 0.51 / 0.61 / 0.70; grok 0.44 / 0.58 / 0.49; terra 0.01 / 0.52 / 0.73; wonder 0.55 / 0.70 / 0.59.

Concentration (share of a model's Task anchors on a package that fall in its top 3 Tasks; share of runs citing each top Task):

| model | DS top-3 share (top Tasks) | AL top-3 share | DE top-3 share (top Tasks) |
|---|---|---|---|
| ember | 39% (T9 74%, T4 58%, T1 52%, T7 52%) | 63% | 55% (T12 96%, T1 75%, T8 74%) |
| luna | 50% (T4 37%, T8 23%, T11 18%); 1.6 anchors/run | 70% | 91% (T12 91%, T1 63%, T2 20%) |
| haiku | 38% (T3 100%, T8 96%, T1 92%) | 57% | 47% (T2 100%, T12 100%, T1 88%) |
| sonnet | 46% (T9 100%, T4 85%, T8 77%) | 61% | 57% (T2 100%, T3 100%, T12 96%) |
| grok | 55% (T4 88%, T3 88%, T11 75%) | 68% | 72% (T1 100%, T2 100%) |

Share of runs anchoring at least one finding in the Task where a ground-truth issue sits (from `EVAL/<pkg>/ground-truth.json`, plan_quote located in the candidate):

| model | DS T1 (GT1/2) | DS T9 (GT3) | DS T8 (GT4/5) | DS T4 (GT7) | DS T12 (GT9) | DS T2 (GT10) | AL T6 (GT1/2) | AL T7 (GT3/4) | DE T12 (GT1) | DE T1 (GT2) |
|---|---|---|---|---|---|---|---|---|---|---|
| ember | 52% | 74% | 33% | 58% | 14% | 46% | 57% | 13% | 96% | 75% |
| luna | 10% | 13% | 23% | 37% | 2% | 6% | 27% | 6% | 91% | 63% |
| haiku | 92% | 100% | 96% | 80% | 24% | 80% | 92% | 56% | 100% | 88% |
| sonnet | 50% | 100% | 77% | 85% | 23% | 8% | 69% | 27% | 96% | 81% |
| grok | 50% | 75% | 50% | 88% | 0% | 12% | 62% | 12% | 50% | 100% |

ember and luna are spread differently: ember visits the right Tasks often (DS T1 52%, DS T2 46%) but on a different point; luna rarely reaches most DS Tasks at all and repeats one DE Task (T12, 91% of runs).

## 4. Ground-truth hits per reviewer run (keyword proxy)

Per-reviewer judged hits do not exist for all rows, so `gtproxy.py` matches each finding's claim, anchors and refs against a signature per issue (labels from `EVAL/analysis/issue-table/issue-legend.tsv`). Calibrated against the judged per-row results in `EVAL/analysis/issue-table/issue-*.json` (46 rows): precision 0.71, recall 0.89. Reliable labels: B3 (42 true, 0 false), I2 (21 true, 0 false), I8 (33 true, 9 false). I3, B4 and B1 are noisy and are not used for conclusions. I7 was hand-checked (below).

| model | B3 DS T9 condition (satisfiability) | I2 DS resume_decision signature | I8 DE read-back match | B7 AL "nothing is set" vs repo | I7 DE worker-contract test (missing task, cross-document) | I5 DS CHANGELOG (missing task) | B2 DS T1 scope | I6 AL user-guide text |
|---|---|---|---|---|---|---|---|---|
| ember | 65% | 22% | 38% | 3% | 0% | 0% | 0% | 0% |
| luna | 10% | 5% | 63% | 17% | 0% | 0% | 0% | 0% |
| haiku | 88% | 24% | 44% | 24% | 0% true (16% proxy) | 0% | 0% | 0% |
| sonnet | 100% | 38% | 73% | 15% | 23% | 0% | 0% | 0% |
| grok | 62% | 25% | 88% | 12% | 12% | 0% | 0% | 0% |
| wonder | 88% | 75% | 88% | 88% | 0% | 0% | 0% | 12% |

I7 hand check: 8 DE runs touched `tests/skills/test_worker_contract.py` (7 sonnet, 1 grok); 7 of those 8 reported the missing worker-contract update (for example sonnet `j1-sonnet-luna2-r1/t1b-1`: "The plan rewrites exact gh api lines that test_worker_contract.py keys word for word and never updates it"). None of the other 225 DE runs reported it; the haiku proxy matches name neither the file nor its table (the one inspected is about stale line numbers). All 7 true I7 findings were graded non-blocking. Path to the file in sonnet runs: a reverse-dependency search such as `grep -rl "sc:issue\|sc-issue" .` that lists every test referencing the edited files, then a grep inside `test_worker_contract.py`.

I5 (CHANGELOG) was found by no reviewer of any model; `CHANGELOG.md` was touched by 1 of 233 DS runs.

Judge-based attribution on an older subset of rows (`EVAL/analysis/attrib.out`), ground-truth items per run / wrong blockers per run: ember 0.65 / 0.62, luna 0.30 / 0.75, haiku 1.35 / 0.65, sonnet 1.44 / 0.17, grok 1.19 / 1.00.

## 5. Contrast: ember, luna, haiku against sonnet and grok

- ember: fast and shallow. 41 s, 7.1k thinking tokens, 4.2 findings that are mostly local (46% one section and no anchor2, lowest anchor2 rate at 28%) and 43% category "other". It reaches the right Tasks but checks wording there, not whether the acceptance check can pass (DS T1 anchored in 52% of runs, the unbounded-inventory issue matched in 3%).
- luna: narrow and terse. Reads 8 named files whole, almost no searching (4% of runs search tests/), 1.75 findings per run with 46% of runs at 0 or 1 finding, 72% marked blocking, a third of DE findings are the same scope objection. Its picks are unstable on DS (run-to-run Jaccard 0.12).
- haiku: close to sonnet on volume, breadth and in-plan checks (B3 88% vs 100%, 1.35 vs 1.44 judged items per run) but differs on two points: it never opened the unnamed test file (0/25 vs 7/26), and its blocking findings are more often wrong (0.65 vs 0.17 per run).
- sonnet and grok: the only models that open test files the plan does not name in a third of runs (35% and 33%), the only ones that found I7, and the ones that most often put both sides of a contradiction in the block (anchor2 54% and 76%; spanning 2 or more Tasks 42% and 46%).

## 6. Three candidate theories for the misses

### Theory A: reasoning budget

ember and luna stop early. Median thinking tokens and wall time: ember 7.1k / 41 s, luna 3.6k / 102 s, against sonnet 22.9k / 228 s, haiku 45.8k / 233 s, grok 48.5k / 790 s. Across the 7 models, Spearman rho between median thinking tokens and proxy hits per run is 0.64. Within every model the half of runs with more thinking finds more (ember 0.38 to 0.53, luna 0.31 to 0.39, haiku 0.61 to 1.16, grok 0.50 to 1.25, sonnet 1.03 to 1.51 hits per run).

Weakens it: within ember and luna the hard issues (cross-document, missing task, satisfiability) do not rise with thinking (ember 0.25 to 0.22, luna 0.09 to 0.09 per run), while they do for haiku (0.29 to 0.70) and grok (0.08 to 0.50). wonder finds the most (1.54 per run) on 11.2k thinking tokens. Budget explains haiku's variance, not ember's or luna's ceiling.

### Theory B: search scope (files the plan names versus files that depend on them)

Cross-document and missing-task issues need a file the plan never names. Files touched that the plan does not name, per run: sonnet 3.1, grok 1.2, haiku 0.9, ember 0.8, luna 0.3. Runs touching an unnamed test file: sonnet 35%, grok 33%, ember 8%, luna 1%, haiku 0%. Opening the file is close to decisive: 7 of 8 DE runs that touched `test_worker_contract.py` reported I7, 0 of 225 that did not. `CHANGELOG.md` was touched once and I5 was never found.

Weakens it: haiku searches as much as sonnet (81% of runs search tests/, 5.2 recursive searches per run) yet never left the named test file, so search volume is not the variable; the variable is a reverse-dependency search (who references the files this plan edits). Even sonnet did this in only 7 of 26 DE runs, so every model misses missing-task issues most of the time; ember, luna and haiku are at 0, not far below.

### Theory C: report shape and the grading rule

The review prompt grades a requirement the document never states as Medium, non-blocking, and offers no missing-task category (`~/.claude/rules/prompts/document_review_loop_prompts.md` lines 31 and 60). All 7 true I7 findings were non-blocking. luna and terra report almost only blocker-grade findings (72% and 82% blocking; 1.75 and 2.45 findings per run), so Medium issues such as missing tasks and ambiguities rarely reach the block; within luna, the run tercile with the most findings has about 5 times the hits of the lowest (0.63 vs 0.13 per run). ember files many findings, but they are local (46%), surface-level (21%) and "other" (43%), so a two-place contradiction or an unpassable check is rarely stated.

Weakens it: haiku has the volume (8.35 per run, 83% non-blocking) and a locality share close to sonnet's (33% vs 30%), so shape does not explain haiku's cross-document gap; that is Theory B. Volume is not sufficient either: within wonder the lowest-volume tercile finds more than the highest (2.12 vs 1.38 per run), and sonnet's middle tercile finds least (0.92).

### Reading across the three

For luna, B and C both hold strongly (no reverse search, few Medium findings). For ember, C (local, surface findings) and the flat hard-issue ceiling in A hold; B holds partly (49% of runs search tests/, but 0 opened the unnamed test file). For haiku, only B holds; on in-plan checks it is close to sonnet, and its weakness is wrong blockers.

## Limits

- "Files touched" counts file paths named in Bash commands, not content read; luna's Read-tool reads are whole files and are under-counted against Bash slices.
- The ground-truth proxy is a regex (precision 0.71 against judged rows); only I7 was hand-checked per run.
- grok and wonder have 24 runs each (8 per package); their percentages move by 12 points per run.
- Thinking-token counts come from the `result` element's `usage.output_tokens_details.thinking_tokens`; providers may count them differently, so cross-model budget comparisons are approximate.
