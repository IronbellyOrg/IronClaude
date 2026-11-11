# PN3 results: capture-recapture estimate as a stop rule

DECISION: FALSIFIED ; live: NOT RUN (gate)

Pre-registered prediction for the live arm (see the validity note on timing): the stop rule will often demand another whole-document panel round,
and with the cap of 3 reviews many runs will ESCALATE. Original plan figure: R_TOK about 3.3 on a loop-plus-audit basis, which D6 converts
to R_LOOP = (3.3 x 169,468 - 69,044) / 100,424 = 4.88 (the DROP limit; the ADOPT limit 2.5 converts to 3.53). Loop-only forecast (a forecast for scheduling, not a limit):
about 200,000 output tokens per panel round x 2 plus about 90,000 for revises and re-reviews is about 490,000 per run, so R_LOOP is about 4.9, on the DROP edge.

Gate for the live arm c3: **FAIL** (F1 FALSIFIED; F3 not run). F3 not run (no PN1 data): gate rests on F1 alone

## Offline results (O1-O3)

# Falsification (offline, O3)

S_ref = 22 clusters in the catalog (all 36 sources, not revision-introduced); S_conf = 12; clusters captured by at least one of the 12 primary R1 occasions = 7.

## Capture profile (12 primary occasions; blocking clusters)

Q_j = number of clusters captured by exactly j occasions: Q1=2, Q2=0, Q3=2, Q4=1, Q5=1, Q6=0, Q7=0, Q8=1, Q9=0, Q10=0, Q11=0, Q12=0; never captured by a primary occasion (Q0) = 15.

Per-cluster capture counts: D1:4, D2:1, D3:3, D4:0, D5:0, D6:0, D7:0, D8:0, D9:0, D10:0, D11:0, D12:8, D13:0, D14:0, D15:0, D16:1, D17:0, D18:0, D19:5, D20:3, D21:0, D22:0

Occasion cluster sets: a2-r1=2; a2-r2=2; a2-r3=0; a2-r4=1; a2-r5=2; a2-r6=1; a3-r1=2; a3-r2=2; a3-r3=3; a3-r4=3; a3-r5=3; a3-r6=4. Mean pairwise Jaccard = 0.242 (min 0.00, max 1.00).

## F1 held-out prediction, reference S_ref

| k | subsets | mean S_obs | MAE_obs | Chao2 MAE | Chao2 COVER | Jack1 MAE | Jack1 COVER | Jack2 MAE | Chapman MAE | Chapman COVER |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 66 | 3.41 | 18.59 | 16.77 | 0.41 | 17.27 | 0.00 | 17.27 | 17.42 | 0.06 |
| 3 | 220 | 4.30 | 17.70 | 15.49 | 0.37 | 15.90 | 0.00 | 15.22 | - | - |
| 4 | 495 | 4.94 | 17.06 | 14.93 | 0.39 | 15.14 | 0.00 | 14.38 | - | - |
| 6 | 500 | 5.83 | 16.17 | 14.37 | 0.46 | 14.33 | 0.00 | 13.76 | - | - |

**F1 verdict at k=4 (S_ref): FALSIFIED**

## F1 reference S_conf (secondary)

| k | subsets | mean S_obs | MAE_obs | Chao2 MAE | Chao2 COVER | Jack1 MAE | Jack1 COVER | Jack2 MAE | Chapman MAE | Chapman COVER |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 66 | 3.41 | 8.59 | 6.93 | 0.71 | 7.27 | 0.00 | 7.27 | 7.63 | 0.12 |
| 3 | 220 | 4.30 | 7.70 | 5.72 | 0.79 | 5.90 | 0.05 | 5.26 | - | - |
| 4 | 495 | 4.94 | 7.06 | 5.17 | 0.77 | 5.14 | 0.11 | 4.44 | - | - |
| 6 | 500 | 5.83 | 6.17 | 4.60 | 0.79 | 4.33 | 0.19 | 3.85 | - | - |

F1 verdict at k=4 (S_conf): WEAK

## Full-data estimates

| data | S_obs | Q1 | Q2 | Chao2 N [95%] | Jack1 N [95%] | Jack2 N | unseen_upper95 | stop (open=0) |
|---|---|---|---|---|---|---|---|---|
| 12 occasions | 7 | 2 | 0 | 7.916667 [7.065812, 19.767906] | 8.833333 [7.0, 11.255958] | 10.5 | 12.767906 | False |
| 15 occasions | 20 | 8 | 5 | 25.973333 [21.269145, 48.113974] | 27.466667 [20.0, 37.072222] | 30.37619 | 28.113974 | False |

S_ref = 22, S_conf = 12. S_ref is itself a lower bound (it is built from the same kind of review); an estimate above S_ref is not a failure by itself.

## Extra (not pre-registered): reference = clusters reported by any source of the 12 primary runs (arm 1 excluded), S_ref12 = 9

| k | subsets | mean S_obs | MAE_obs | Chao2 MAE | Chao2 COVER | Jack1 MAE | Jack1 COVER | Jack2 MAE | Chapman MAE | Chapman COVER |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 66 | 3.41 | 5.59 | 4.11 | 0.73 | 4.31 | 0.02 | 4.31 | 4.91 | 0.27 |
| 3 | 220 | 4.30 | 4.70 | 3.30 | 0.84 | 3.05 | 0.37 | 2.63 | - | - |
| 4 | 495 | 4.94 | 4.06 | 2.89 | 0.85 | 2.35 | 0.57 | 2.22 | - | - |
| 6 | 500 | 5.83 | 3.17 | 2.31 | 0.90 | 1.63 | 0.69 | 1.96 | - | - |

F1 verdict at k=4 (S_ref12): WEAK

## F2 per-run test (secondary)

| run | N_hat (LOO Jack1) | R1 clusters | fixed | predicted residual | observed (all audits) | observed (first audit) |
|---|---|---|---|---|---|---|
| a2-r1 | 8.82 | 2 | 2 | 6.82 | 2 | 2 |
| a2-r2 | 8.82 | 2 | 2 | 6.82 | 2 | 2 |
| a2-r3 | 8.82 | 0 | 0 | 8.82 | 3 | 3 |
| a2-r4 | 8.82 | 1 | 1 | 7.82 | 3 | 3 |
| a2-r5 | 8.82 | 2 | 2 | 6.82 | 2 | 2 |
| a2-r6 | 8.82 | 1 | 1 | 7.82 | 0 | 0 |
| a3-r1 | 8.82 | 2 | 2 | 6.82 | 2 | 2 |
| a3-r2 | 8.82 | 2 | 2 | 6.82 | 3 | 2 |
| a3-r3 | 8.82 | 3 | 3 | 5.82 | 2 | 2 |
| a3-r4 | 8.82 | 3 | 1 | 7.82 | 3 | 2 |
| a3-r5 | 6.91 | 3 | 3 | 3.91 | 1 | 0 |
| a3-r6 | 6.91 | 4 | 3 | 3.91 | 1 | 0 |

Spearman rho (predicted vs observed, all audits) = 0.554; first audit only = 0.602 (n=12, ties averaged). Read: rho <= 0 is consistent with falsification. Weak by construction: the leave-one-out N_hat is almost the same for every run, so the prediction varies only with the number fixed.

## Sensitivity: adjudication overrides ignored (mechanical clusters only)

Mechanical clusters: S_ref = 17, S_conf = 7.

| k | subsets | mean S_obs | MAE_obs | Chao2 MAE | Chao2 COVER | Jack1 MAE | Jack1 COVER | Jack2 MAE | Chapman MAE | Chapman COVER |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 66 | 2.32 | 14.68 | 14.07 | 0.06 | 13.95 | 0.00 | 13.95 | 14.37 | 0.00 |
| 3 | 220 | 2.80 | 14.20 | 13.54 | 0.25 | 13.25 | 0.00 | 12.90 | - | - |
| 4 | 495 | 3.17 | 13.83 | 13.06 | 0.25 | 12.70 | 0.00 | 12.15 | - | - |
| 6 | 500 | 3.79 | 13.21 | 12.12 | 0.34 | 11.79 | 0.00 | 10.98 | - | - |

F1 verdict at k=4 (mechanical, S_ref): FALSIFIED; (mechanical, S_conf): WEAK. Verdict is unchanged versus the adjudicated catalog (FALSIFIED).

## Product CLI cross-check

`superclaude review estimate` output equals the library result on 12/12 matrices (12 and 15 occasions plus 10 random subsets).


## F1 VERDICT (pre-registered, section 2): **FALSIFIED** (S_conf: WEAK; mechanical clusters: FALSIFIED)

Pre-registered rule: FALSIFIED at k=4 if for both Chao2 and Jackknife-1 MAE_est(4) >= MAE_obs(4) or COVER(4) < 0.5; SUPPORTED if an estimator has MAE_est(4) <= 0.7 * MAE_obs(4) and COVER(4) >= 0.7; otherwise WEAK.


Catalog: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/catalog/BUILD-NOTES.md

## Shadow calibration (F3)

# Shadow calibration (F3)

Not run: 0 completed PN1 runs found (need at least 5 with both audits ingested).


## Live arm c3

Not run: the gate failed, so no workers were launched.

## Validity notes

- The prediction above was written into this script after the offline phases had run (the plan asked for it before analysis); it concerns the live arm, which has not run.
- Cost policy (D6): cost is judged only after runs complete; nothing in the harness stops, truncates or skips a run on token or dollar cost.
- The 12 primary occasions are one model with one prompt, so detection is correlated and every estimator here is a lower bound.
- Defects have very unequal detection probability (cluster capture counts in the profile), which is why Mh-type estimators (Chao2, Jackknife-1) are used.
- The reference truth (the catalog) is itself built from the same kind of review: 21 audits and 15 first reviews, adjudicated by one reader; arm-1 reports are a different instrument and add 10 clusters the primary occasions never saw.
- Dedupe overrides: the sensitivity run ignoring them is in the offline section.
- Re-reviews are scoped to changed lines and are not capture occasions (C7).
- Token method (C9.1): output tokens, each message id counted once (max over its lines); D2: the decision uses loop-only tokens.
- Haiku stratum: panel composition unchanged (sonnet anchor plus haiku stand-ins); the non-panel loop workers (reviser, scoped re-reviewer) run on Haiku; audits always Sonnet; never pooled with Sonnet.
