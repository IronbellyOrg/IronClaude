# Scoring Framework — Reflect A/B Harness

Consumes: all `<run-dir>/run-report.md` (one method's 5 runs at a time) + `return-contract.yaml`
per run + the hidden `<EXP>/ground-truth.yaml`. Produces: `matrix.md` (runs × metrics) and
`scorecard.md` (per-method aggregate + cross-method delta + consistency index + verdict).

## Metric groups (the things that actually matter)

| ID | Metric | Definition | Direction | Weight |
|----|--------|------------|-----------|--------|
| **G1** | Fan-out | `fanned_out` (≥2 reviewer cards) + `reviewer_card_count`; `degraded_to_fixture` flag | — (descriptive) | — |
| **G2** | **Regression recall** | planted regressions detected / planted regressions (the HIGH-stakes class) | ↑ | **3.0** |
| **G3** | Overall detection recall | planted deviations detected (any class) / total planted | ↑ | 2.0 |
| **G4** | Classification accuracy | of detected, fraction with correct 4-cat class | ↑ | 1.5 |
| **G5** | False-positive rate | reported deviations with no ground-truth match / total reported (clean controls are bait) | ↓ | 1.5 |
| **G6** | Citation accuracy | `citation_resolves==true` / cited | ↑ | 1.0 |
| **G7** | Verdict correctness | `regression_present==true` AND `promotion_would_fire==false` (both required) | ↑ (binary) | 2.0 |
| **G8** | Within-method consistency | see formula below | ↑ | 1.5 |
| **G9** | Cost | tokens_total, wall_clock_ms (context, not scored for quality) | — | — |

A detection "match" = same file AND overlapping line range (±5) as a ground-truth plant. A
regression detected but mis-classified as drift still counts for G2/G3 recall (it was *found*),
and the mis-class is captured by G4 (mirrors sc-reflect eval dim #6).

## G8 — within-method consistency index (the within-method axis)

Across the 5 runs of one method:
- **Set stability** = mean pairwise Jaccard of the `{file:line}` detected-deviation sets (1.0 = every run found the same set).
- **Verdict stability** = fraction of runs agreeing with the modal `verdict_status` AND modal `regression_present`.
- **Tier stability** = fraction agreeing with modal `tier_reached`.
- **Score dispersion** = 1 − normalized stddev of the per-run composite quality score (G2–G7 weighted).
- **Consistency index** `C = 0.4·SetStability + 0.3·VerdictStability + 0.15·TierStability + 0.15·ScoreDispersion`.

> Interpretation: high C + high quality = trustworthy. High C + LOW quality = consistently wrong
> (worse than noise — it *looks* reliable). Low C = the method's verdict is luck-of-the-draw.
> Suspiciously perfect SetStability on the inference arm may indicate in-session context carryover
> (flag it; recommend fresh-session re-run).

## Per-run composite quality score

`Q_run = (3·G2 + 2·G3 + 1.5·G4 + 1.5·(1−G5) + 1·G6 + 2·G7) / 11`  → 0.0–1.0.

## matrix.md (runs × metrics)

| run_id | fanned_out | cards | G2 reg-rec | G3 rec | G4 class | G5 FP | G6 cite | G7 verdict | Q_run | tokens | wall_ms |
|--------|-----------|-------|-----------|--------|----------|-------|---------|-----------|-------|--------|---------|
| inference-01 | … | … | … | … | … | … | … | … | … | … | … |
| … (all 5) | | | | | | | | | | | |

## scorecard.md

```
METHOD: <inference|cli>   sample_commit=<sha>  base=<sha>  n_runs=5
Fan-out: <X>/5 runs fanned out (mean cards=<m>); degraded-to-fixture: <Y>/5
Quality (mean ± stddev across runs):
  G2 regression-recall : 0.__ ± 0.__
  G3 detection-recall  : 0.__ ± 0.__
  G4 classification    : 0.__ ± 0.__
  G5 false-positive    : 0.__ ± 0.__   (lower better)
  G6 citation-accuracy : 0.__ ± 0.__
  G7 verdict-correct   : _/5 runs correct
  Q (composite)        : 0.__ ± 0.__
Consistency index C    : 0.__   (Set=__ Verdict=__ Tier=__ Disp=__)
Cost: mean tokens=____  mean wall=__s
HEADLINE: <one-line verdict on this method's trustworthiness>
```

## Cross-method comparison (run once both methods' scorecards exist)

A final `comparison.md`: side-by-side per-metric `cli − inference` deltas, a statement on whether
fan-out (cli) measurably improved G2/G3/G4/G6 over inference, and whether either method is
consistent enough to trust as a default gate. Tie this back to the HD-1 decision: if inference
either degrades-to-fixture (G1) OR scores low on G2/G7, that is direct evidence for flipping the
default to cli; if inference matches cli on quality AND consistency, it supports keeping skill mode.
