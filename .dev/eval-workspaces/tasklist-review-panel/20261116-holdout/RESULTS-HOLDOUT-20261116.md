# Frozen hold-out comparison of Recipe Ledger: results (2026-11-16)

**Context for a reader with no history.** The "Review Panel" of this repository has cheap reviewer models read a plan and report real defects; a blind Opus judge scores each run against a hidden defect list. Recipe Ledger (RL) is a redesign in which each reviewer first runs eight written recipes and writes a ledger of one row per step. An exploratory check on the three study packages (never frozen) had RL at 2.00 defects per replicate against 0.67 for the control (Z0) and 0.56 for a plain-words checklist (K). This file reports the confirming test the requirements call for: RL frozen (tag `rl-freeze-1553f5dd29b1`), pre-registered gates (`../20261114-recipe-ledger/config/prereg.json`, `PREREG-ADDENDUM-20261116.md`, `PREREG-ADDENDUM-2-20261116.md`), fresh documents, ground truth written by an independent session after the freeze and before any run. Background and open questions for the owner: `../OPEN-DECISIONS-20261115.md`.

## Result

**RL is not adopted: it failed four of the pre-registered gates (D1 time, D2 effect, D3 consistency, D6 non-regression), one of them the blocking gate.** The exploratory lead did not reproduce on new documents.

## What was run

- 4 plans not used to design the recipes: HO-2, HO-3, HX-1, HX-3 (36 ground-truth items, 10 of them blocking). 3 arms (Z0, K, RL) x 5 replicates = 60 panel runs, ember panel (`muse-ember-1.0` + 2x `gpt-6-luna`), one panel at a time, sandbox rebuilt between runs when needed, no fallback model.
- Blind Opus judge on all 60, plus a second judge on 9 runs (15%): **the second judge gave the identical set of found defects on 9 of 9**. Judge audit: 69 folders, 0 bad.
- One run (`stage1-z0-HX-3-r1`) was invalid because the Claude Code program was updated while it started (all reviewers exited after 0.005 s). It was moved aside (`../20261114-recipe-ledger/runs-holdout-invalid/`) and rerun once with the same seed; the rerun is valid. Runs before 19:55 UTC used an earlier program version (not recorded per run).

## Numbers (pooled over the four documents; 20 runs per arm)

| Measure | Z0 (control) | K (checklist) | RL |
|---|---|---|---|
| Found fraction of known defects, mean per run | 0.223 | 0.213 | **0.259** |
| Wrong blockers per run | 0.95 | 1.40 | **0.50** |
| Real blocking defects found (fraction of blocking items) | 0.040 | 0.029 | 0.053 |
| Items reached in at least 3 of 5 runs ("consistent") | 5 | 4 | 6 |
| Median panel seconds | 99.8 | 117.3 | 141.8 |
| Output tokens per run | 21,036 | 20,872 | 24,339 |
| Reviewer kills | 1 | 4 | 4 |

Per document, found fraction (Z0 / K / RL): HO-2 0.26 / 0.22 / 0.22; HO-3 0.10 / 0.12 / 0.17; HX-1 0.50 / 0.50 / 0.60; HX-3 0.03 / 0.02 / 0.05.

## Gates (as pre-registered)

| Gate | Rule | Result |
|---|---|---|
| D1 time | per-document median at most 1.35 x Z0, p90 at most 1.5 x, kills at most 10% | **FAIL**: median ratios HO-2 1.20, HO-3 1.53, HX-1 1.82, HX-3 1.06; kills 4 of 60 (6.7%) |
| D2 effect | found fraction at least Z0 + 0.12, 90% bootstrap lower bound above Z0 + 0.04 | **FAIL**: difference +0.036, lower bound -0.090 |
| D3 consistency | consistent items at least Z0's count + 3 | **FAIL**: 6 against 5 |
| D4 precision | wrong blockers at most Z0 + 1.0 | pass (difference -0.45) |
| D5 generality | planted set | not run (no planted documents) |
| D6 non-regression | items Z0 reaches at 0.5 or more stay within 0.1 | **FAIL** (blocking gate): HO-2 GT2 and GT3 regressed |
| D7 beats the checklist | gain over K at least 0.04 | pass (+0.046), though K itself is no better than Z0 (-0.010) |

Shares of the gain: the plain checklist added -0.010, the redesign +0.036 over Z0.

## Format reading (pre-registered: lenient decides, strict reported)

- Lenient (owner-approved allowances): ledger missing in 0 of 56 reviewer reports (limit 10%): pass.
- Strict (nothing forgiven): 26 of 56 reports (46%) would fail. Forgiven slips: 253 row ids with a prefix or suffix, 5 headings between ledger and findings, 1 line with a trailing comma. 4 reviewer reports had no ledger file at all. The format gate passes only with the allowances.
- Quote validity: 505 of 604 quoted rows (83.6%) found in the plan. 8 rows were over the lens cap.

## What this means

- **Recipe Ledger helps a little on found defects and clearly on wrong blockers, but not enough to pass.** It finds about 0.3 more defects per run than the control (36 items over 4 plans; an effect this size is within noise here), halves the wrong blockers (0.50 against 0.95), costs about 40% more time on the median and fails the time rule on two of four documents.
- **The exploratory result did not reproduce.** The earlier gap (+1.33 defects per replicate) came from the three study packages, whose ten known defects the recipes were derived from, with p-values computed after seeing the data. On fresh plans the gap is +0.036 of the items. Likely reason (not tested): the recipes fit the study packages' defect classes; on new documents they add less. Regression to the mean is also possible.
- **The one consistent benefit is precision** (fewer wrong blockers), which passes D4 and matches the earlier set (5 against 14 wrong blockers there). It does not by itself justify the extra time.
- **The ground-truth set is small and uneven**: HX-1 has only 2 items, HO-3 and HX-3 have the most but few found. Two documents (HX-1, HX-3) have no blocking items, so blocking-defect comparisons are descriptive only.

## Limits

One panel (ember); plans only (no specs or documentation targets; D5 not run); 36 items; the ground-truth author is a model session (owner's choice); a Claude Code program update occurred mid-stage (one run lost, later runs on a newer version); documents HO-1, HO-4 (plans in the repository are later versions than the reviewed ones) and HX-2 (base commit lacks files) were dropped before any run and replaced by HX-1 and HX-3 as recorded in addendum 2; freeze.json does not cover the format-allowance code or launchers, so `config/runtime-hashes.json` (37 files, written during run 1) was checked after the runs and after judging and matches.

## Files

Run folders `../20261114-recipe-ledger/runs-holdout/` (not committed), scores `scoring-holdout/`, analysis `results-holdout/{report.md,metrics.json,d1.json,stages.jsonl}`, incidents `runs-holdout/INCIDENTS.md`.
