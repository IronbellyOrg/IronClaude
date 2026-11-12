# PILOT DESIGN (not the confirmatory run): first measurement of the reflect Tier 2 panel

**This is a pilot.** It estimates the discordance d between arms and the within-arm noise d0. It does not decide H-B. The confirmatory run is a separate run that needs owner approval of its spend before it starts (see "Owner approval").

Task 7 of `TASK-WF-implementStages0-20261111-202912.md`. Source: `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md` (cited below as `src:<line>`), section "First measurement" (`src:522-544`), the Stage 0 row of "Staged migration" (`src:408`) and "Cost model" (`src:474-500`). Stage 0 evidence from this package: `stage0a-report.md` (Task 4), `cluster-pairs-50.csv` (Task 5), `consumer-inventory.md` and `lint-test-design.md` (Task 6).

Reading rules for this document:

- Every sentence either restates the source (with a `src:` line) or a Stage 0 artifact (with its file name), or is marked **(own arithmetic)** or **(own note)**.
- All token figures are estimates from the source's cost model, not measurements (`src:477`).
- Every threshold is stated once, in the table "Thresholds"; other sections refer to it by id (T-1 to T-10).

## Thresholds (the only place threshold values are stated)

| Id | What it bounds | Value | Source |
|---|---|---|---|
| T-1 | H-A: T2 recall minus T1 recall on seeded defects (superiority); used as margin M in the H-A sample size | at least 15 percentage points (M = 0.15) | `src:527`, `src:536` |
| T-2 | H-B: panel-parity T2 recall versus legacy T2 recall, and precision likewise (non-inferiority); used as margin M in the H-B sample size | within 10 percentage points, judged on the one-sided 95% bound (M = 0.10) | `src:528`, `src:536` |
| T-3 | H-C: median panel-T2 tokens | at most 1.05 x the legacy median | `src:529` |
| T-4 | H-C: p95 panel-T2 tokens, in the profile's claude-token unit (the same number as the profile's hard kill line) | at most 65k | `src:529`, `src:479`, `src:498` |
| T-5 | Safety list (below) | zero events; any one event fails regardless of savings | `src:530` |
| T-6 | Within-arm noise rule | if d0 is at least 0.8 x d between arms, the arms are indistinguishable from noise | `src:538` |
| T-7 | Non-sparse quota | at least 25% of plans whose source carries labelled requirement ids | `src:540` |
| T-8 | Test level and power used in the sample-size formula | one-sided 95% (z = 1.645), 80% power (z = 0.842) at a true difference of 0 | `src:536` |
| T-9 | Stage 0 conversion share gate (O-7), redefined by the owner on 2026-11-12 (`conversion-gate-redefinition.md`) | at least 90% of findings convert with an unambiguous `(path, line)`, measured on cards written under the findings-v2 reviewer brief; the recorded legacy cards are reported as a baseline (67.28%) and gate nothing | `src:408`, `src:542`, `src:555`, `conversion-gate-redefinition.md` |
| T-10 | Pooled headline across strata | shown only if a heterogeneity check across strata is not significant (the source gives no test or level for this check) | `src:540` |

Design parameters (not thresholds): 12 plan+spec pairs, 5 seeded defects per pair, 6 plans for arm D, 6 repeats of arm B, clustering factor 1.3 (`src:536`, `src:538`).

## Hypotheses

- **H-A (worth).** T2 recall beats T1 recall on seeded defects by T-1 (superiority) (`src:527`). If not, the result is recorded as "the T2 spend does not buy recall on plans", and the owner chooses between shrinking T2 to 2 reviewers and tuning the rubric (O-8) (`src:527`, `src:556`). This is not an automatic veto of the migration, which the source also justifies by maintenance (`src:527`).
- **H-B (non-inferiority).** Panel-parity T2 recall is within T-2 of legacy T2 recall, and precision likewise (`src:528`). The source drops two other margins: a 5-point margin, because it is not resolvable at feasible n, and the H-A margin used as a non-inferiority bound, because that is a different hypothesis (`src:528`).
- **H-C (cost).** Median panel-T2 tokens meet T-3 and p95 meets T-4, in the profile unit (`src:529`). A saving is reported, not required (`src:529`).
- **Safety (T-5; fails regardless of savings)** (`src:530`):
  1. a forbidden model or executor-class collision dispatched when the executor is known;
  2. a MALFORMED contract;
  3. an unsupported citation certified;
  4. any repository write by a reviewer;
  5. a T1 or `--depth quick` run that calls the panel.

## Arms

All arms run on the same plans, and graders do not see which arm produced a result (`src:532`).

| Arm | What runs | Plans in the pilot | Source |
|---|---|---|---|
| A | T1 only, a `--tier 1` pin (flag semantics `SKILL.md:362`) | all 12 | `src:532`, `src:538` |
| B | legacy T2 | all 12, plus 6 repeats to estimate d0 | `src:532`, `src:538` |
| C | panel-parity T2: a development-build `--t2-engine panel` (owner decision: the development-build panel, not the `shadow` form, because the shadow form keeps the legacy writers authoritative and so does not exercise the panel as the shipped T2); debate kept; the measurement runs on a development build and Stage 3 ships the same code to users | all 12 | `src:532`, `src:538` |
| D | panel-lite, the `@reflect-lite` template (sonnet, haiku, Opus calibrator), to price the Opus-moves ablation | 6 of the 12 (pilot subset only) | `src:532`, `src:538` |

(own note) The source does not say on which plans the 6 repeats of arm B run, nor whether "6 repeats" means 6 extra runs in total or 6 per plan. This design reads it as 6 extra arm-B runs in total, run one per block in blocks 1-6 (Stop rule S-1); the cost section prices that reading (row C-5) and the other one (row C-5b).

## Ground truth

- **Seeded defects**, scripted and not derived from reviewer output, of five kinds (`src:534`):
  1. ordering;
  2. missing acceptance;
  3. spec-uncovered requirement;
  4. wrong file path;
  5. cross-task contradiction.
- **Union ledger** of natural findings from all arms, scored by a blinded grader (`src:534`).
- **Circularity caveat.** The source applies the ledger circularity caveat of `LEDGER-RESULTS.md:49` (`src:534`). That line (in `.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md`) says the ledger comes from findings of the same runs, so an arm whose reviewers found more could look better; the earlier study checked this by restricting to defects supported by several arm families. (own note) Recall on seeded defects does not have this problem; recall and precision on the union ledger do, so ledger-based numbers are reported with the caveat.

## Pilot (what runs)

- 12 plan+spec pairs x 5 seeded defects = 60 defects; arms A, B and C on all 12; arm D on 6 of them (`src:538`).
- 6 repeats of arm B estimate the within-arm noise discordance d0 (`src:538`). The noise rule is T-6: when d0 reaches it, the arms are indistinguishable from noise (`src:538`).
- Hygiene: blinded arm identity, a stop rule (see "Stop rule") and the pilot labelled as a pilot (`src:538`).
- **The pilot estimates d; it does not decide H-B** (`src:536`). Its outputs are d between arms B and C (d_BC), d between arms A and B (d_AB), and d0, which size the confirmatory run (`src:538`).

## Sample size

Pairing is by defect. Discordance d is the share of defects found by exactly one of the two arms compared (`src:536`). The standard error of the paired recall difference is about sqrt(d/n) (`src:536`). For a one-sided non-inferiority test at the level and power of T-8, with a true difference of 0 (`src:536`):

`n = d x (z_level + z_power)^2 / M^2 = 6.185 x d / M^2` (`src:536`)

- H-B, M from T-2: **n = 618 x d** defects (`src:536`).
- H-A, M from T-1: **n = 275 x d** defects (`src:536`).
- Multiply by 1.3 for clustering of defects within plans (`src:536`).
- Confirmatory size from the pilot's observed d: `n_plans = ceil(1.3 x max(618 x d_BC, 275 x d_AB) / 5)` (`src:538`).

Worked numbers (the d values are the source's examples, not measurements; columns after "source" are own arithmetic, rows A-4 to A-9 of the arithmetic table):

| Hypothesis | d | n (source) | n unrounded | n x 1.3 (rounded up) | plans at 5 defects, `ceil(n x 1.3 / 5)` |
|---|---:|---:|---:|---:|---:|
| H-B | 0.10 | 62 | 61.8 | 81 | 17 |
| H-B | 0.20 | 124 | 123.6 | 161 | 33 |
| H-B | 0.30 | 185 | 185.4 | 242 | 49 |
| H-A | 0.35 | 96 | 96.25 | 126 | 26 |

The 33 plans at d = 0.20 match the source's confirmatory example (`src:538`).

## Power at the pilot size

At 60 defects the source gives power of about 79% when d = 0.10 and about 54% when d = 0.20 (SE 0.058, bound 0.095), and concludes that the pilot estimates d and does not decide H-B (`src:536`). Recomputed (own arithmetic, rows A-10 and A-11): 78.9% at d = 0.10 and 53.5% at d = 0.20 (see source discrepancy SD-2 for the rounding of the second figure).

(own note) These figures use n = 60 and do not apply the 1.3 clustering factor that the source applies to the confirmatory size. With the factor (effective n = 60 / 1.3 = 46.2), power falls to about 69% at d = 0.10 and about 45% at d = 0.20 (row A-12). This strengthens the source's conclusion that the pilot cannot decide H-B.

## Arithmetic checks

All rows are own arithmetic. "Match" means the source figure reproduces.

| Row | Check | Computation | Result | Source figure | Match |
|---|---|---|---|---|---|
| A-1 | z constant (T-8) | (1.645 + 0.842)^2 = 2.487^2 | 6.185 (exact normal quantiles give 6.183) | 6.185 (`src:536`) | yes |
| A-2 | H-B coefficient | 6.185 / M^2, M^2 = 0.0100 | 618.5 (618.3 with exact quantiles) | 618 (`src:536`) | yes (truncated) |
| A-3 | H-A coefficient | 6.185 / M^2, M^2 = 0.0225 | 274.9 | 275 (`src:536`) | yes |
| A-4 | H-B, d = 0.10 | 618 x 0.10 | 61.8, up to 62 | 62 | yes |
| A-5 | H-B, d = 0.20 | 618 x 0.20 | 123.6, up to 124 | 124 | yes |
| A-6 | H-B, d = 0.30 | 618 x 0.30 | 185.4; nearest 185, rounded up 186 | 185 | yes by nearest rounding; see SD-1 |
| A-7 | H-A, d = 0.35 | 275 x 0.35 | 96.25; nearest 96, rounded up 97 | 96 | yes by nearest rounding; see SD-1 |
| A-8 | times 1.3 | 61.8, 123.6, 185.4, 96.25 each x 1.3 | 80.34, 160.68, 241.02, 125.125 (up to 81, 161, 242, 126) | factor only | n/a |
| A-9 | plans | ceil of (A-8 / 5) | 17, 33, 49, 26 | 33 at d = 0.20 (`src:538`) | yes |
| A-10 | pilot power, d = 0.10 | SE = sqrt(0.10 / 60) = 0.0408; M / SE = 2.449; 2.449 - 1.645 = 0.804; Phi(0.804) | 0.789 | about 79% | yes |
| A-11 | pilot power, d = 0.20 | SE = sqrt(0.20 / 60) = 0.0577; bound 1.645 x 0.0577 = 0.0950; M / SE = 1.732; 1.732 - 1.645 = 0.087; Phi(0.087) | SE 0.058, bound 0.095, power 0.535 | SE 0.058, bound 0.095, about 54% | SE and bound yes; power see SD-2 |
| A-12 | pilot power with the 1.3 factor | effective n = 60 / 1.3 = 46.15; d = 0.10: SE 0.0465, power 0.693; d = 0.20: SE 0.0658, power 0.450 | about 69% and 45% | not in source | n/a |
| A-13 | pilot defects | 12 x 5 | 60 | 60 (`src:538`) | yes |

## Cost

Unit: the published profile's claude-orchestration tokens (turn-budget unit; "1 turn ≈ 1k claude tokens") (`src:479`, `src:538`). Per run the profile gives T1 3k-8k plus 2k-5k auggie, and T2 35k-70k plus 10k-25k auggie (`src:479`). These are estimates (`src:477`). The source keeps three cost bases separate and never sums them (`src:477`); this section uses only the profile basis, as the source's pilot costing does (`src:538`). Retrieval (auggie) tokens are listed separately and are not summed with claude tokens (`src:538`).

| Row | Item | Computation (own arithmetic) | Claude tokens | Source figure | Match |
|---|---|---|---|---|---|
| C-1 | per plan, arms A+B+C | low 3k + 35k + 35k; high 8k + 70k + 70k | 73k-148k | 73k-148k (`src:538`) | yes |
| C-2 | pilot, 12 plans, arms A+B+C | 12 x 73k = 876k; 12 x 148k = 1,776k | 0.876M-1.776M, rounded 0.9M-1.8M | 0.9M-1.8M (`src:538`) | yes |
| C-3 | arm D, 6 plans | 6 x 35k = 210k; 6 x 70k = 420k | 210k-420k | "adds 6 x 35k-70k" (`src:538`) | yes |
| C-4 | arm B repeats for d0, read as 6 extra T2 runs | 6 x 35k = 210k; 6 x 70k = 420k | 210k-420k | not costed in the source | see SD-3 |
| C-5 | whole pilot (C-2 + C-3 + C-4) | 876k + 210k + 210k = 1,296k; 1,776k + 420k + 420k = 2,616k | 1.30M-2.62M | not in source | n/a |
| C-5b | whole pilot if the repeats are 6 per plan (C-2 + C-3 + 72 x 35k-70k) | 876k + 210k + 2,520k = 3,606k; 1,776k + 420k + 5,040k = 7,236k | 3.61M-7.24M | not in source | see SD-3 |
| C-6 | confirmatory, 33 plans (d = 0.20), arms A+B+C | 33 x 73k = 2,409k; 33 x 148k = 4,884k | 2.41M-4.88M, rounded 2.4M-4.9M | 2.4M-4.9M (`src:538`) | yes |

If "6 repeats of arm B" instead means 6 repeats on each of the 12 plans (72 extra runs), C-4 becomes 72 x 35k-70k = 2.52M-5.04M (own arithmetic); the owner should confirm the reading before the pilot is priced (SD-3).

Retrieval tokens, listed separately and never added to the rows above (own arithmetic from `src:479`):

| Row | Item | Computation | Auggie tokens |
|---|---|---|---|
| R-1 | per plan, arms A+B+C | low 2k + 10k + 10k; high 5k + 25k + 25k | 22k-55k |
| R-2 | pilot, 12 plans, arms A+B+C | 12 x 22k = 264k; 12 x 55k = 660k | 264k-660k |
| R-3 | arm D, 6 plans | 6 x 10k-25k | 60k-150k |
| R-4 | arm B repeats, 6 runs | 6 x 10k-25k | 60k-150k |
| R-6 | whole pilot (R-2 + R-3 + R-4); with 6 repeats per plan, R-4 = 72 x 10k-25k = 720k-1,800k | 6 repeats in total: 264k + 60k + 60k = 384k to 660k + 150k + 150k = 960k; 6 per plan: 264k + 60k + 720k = 1,044k to 660k + 150k + 1,800k = 2,610k | 384k-960k (6 in total); 1,044k-2,610k (6 per plan) |
| R-5 | confirmatory, 33 plans | 33 x 22k = 726k; 33 x 55k = 1,815k | 726k-1,815k |

The measured tokens of arms B and C are also the H-C data: median against T-3 and p95 against T-4 (`src:529`, `src:498`). A run killed at the kill value counts as above T-4, and at pilot size T-3 and T-4 are descriptive (Stop rule S-3.4, S-4).

## Strata and the non-sparse quota

Results are reported split by `--depth` and by escalation path, never only pooled (`src:540`). Strata (`src:540`):

1. standard depth, escalated by the parsed-sparse pre-filter;
2. standard depth, escalated by rule 4, 5 or 6 without the pre-filter;
3. `--depth deep`;
4. `--tier 2` pin.

Each stratum reports n, recall, precision, tokens and a confidence interval; a pooled headline follows T-10 (`src:540`).

Quota: T-7, because 34 of 38 recorded pre decisions were parsed-sparse (`src:540`, `src:142`). If the quota cannot be met, the report states that it measured sparse-labelled plans only (`src:540`).

- (own arithmetic) Pilot: 12 x T-7 = 3.0, so at least 3 of the 12 plans must carry labelled requirement ids. Confirmatory at 33 plans: 33 x T-7 = 8.25, so at least 9 plans.
- (own arithmetic) In the recorded history 38 - 34 = 4 of 38 pre decisions (10.5%) were not parsed-sparse, so plans meeting the quota must mostly be chosen or written for the measurement, not drawn from recorded runs.
- **Stage 0a does not replace this estimate.** `stage0a-report.md` does not count labelled requirement ids or `coverage_degraded` values; it reports conversion, clusters, merged-verdict agreement, null scores and calibration only. The 34 of 38 figure therefore stays the source's count (`src:142`), not re-checked by Task 4.

## Stage 0a numbers used here (from `stage0a-report.md`)

| Item | Source estimate | Stage 0a result | Effect on this pilot design |
|---|---|---|---|
| Recorded `reviewer-cards/` directories | 42 (`src:542`) | 43; the report notes that 1 of them is this plan's own reflect run, recorded after the source's count (`stage0a-report.md`, Inputs) | none; the pilot uses new seeded plans, not recorded cards |
| Of those, with `adversarial/merged-verdict.yaml` | 33 (`src:542`) | 34 (`stage0a-report.md`, Inputs) | none |
| Conversion share on recorded cards | not measured | 479 / 712 = 67.28% (`stage0a-report.md`, "Conversion share"); the report's FAIL against the old T-9 wording is superseded by the redefinition in `conversion-gate-redefinition.md` | the recorded share is a baseline only; T-9 now gates cards written under the findings-v2 brief; see the Stage 0 exit checklist |
| Agreement with the recorded merged verdict | not measured | 24 / 358 = 6.70%, descriptive, seeds no gate (`stage0a-report.md`, "Agreement") | none; descriptive only, as the source says (`src:542`) |
| Recorded null convergence scores at T2 | 7, cause UNVERIFIED (`src:436`, `src:438`) | 8: skipped-similar debate 0, single-reviewer-fallback 2, illegal merge_method value 4, other 1, undetermined 1 (`stage0a-report.md`, "Recorded null convergence scores") | (own note) no recorded null comes from a skipped-similar debate, so the recorded evidence does not trigger the separate decision of `src:436`; a null score in an arm-B or arm-C run is still recorded as a T2 outcome |
| Recorded numeric calibration | not stated | 0 of 689 findings carry a numeric `finding_confidence` (`stage0a-report.md`, "Recorded calibration") | (own note) no recorded calibration can seed the pilot; the pilot scores recall and precision against the ground truth, not calibrated confidence |

(own arithmetic) Null-score causes sum to 0 + 2 + 4 + 1 + 1 = 8, matching the report's total.

## Stop rule

The source requires "a stop rule" as pilot hygiene but does not state one (`src:538`). What the source and the profile fix:

- any safety event (T-5) fails the measurement regardless of savings (`src:530`);
- when d0 reaches T-6, the arms are indistinguishable from noise (`src:538`);
- a caller must abort a run that exceeds 1.25 times the profile midpoint (`cost-profile.yaml:68-70`), and reflect itself does not read the profile at run time (`cost-profile.yaml:4-5`), so the pilot harness, as the caller, enforces the kill: the T-4 value for a T2 run (`src:479`) and 6 x 1.25 = 7.5k claude tokens for a T1 run (own arithmetic from `cost-profile.yaml:43,70`).

**PROPOSED stop rule (own note, not in the source; the owner confirms or replaces it before the pilot runs).** It merges two independent reviews of the earlier three-line rule, each with three defects and three improvements, and a debate between them (`stop-rule/proposal-A.md`, `stop-rule/proposal-B.md`, `stop-rule/debate-A-on-B.md`, `stop-rule/debate-B-on-A.md`; arm letters follow this document, not the review brief). The earlier rule halted the pilot on a safety event in any arm, so a baseline fault of the legacy arm could end it before any estimate; named an "approved ceiling" with no approval step, value or meter; and did not say what happens to a run that ends without a result. S-2 (safety) takes precedence over S-3 (spend). S-4 lists what never stops the pilot. Runs go one at a time, so no run is ever in flight when a rule fires.

**S-0. Before run 1.** The owner approves in writing: this rule, the reading of "6 repeats of arm B" (SD-3), the two ceilings of S-3.1, the rerun allowance of S-3.5 (default none) and the Stage 0 exit state (see "Stage 0 exit checklist": item 2 is FAIL and the plan stops for owner review). The pilot does not start before that.

**S-1. Run order.** The pilot runs in plan blocks: one plan with arms A, B and C (and D, if the plan is one of the 6 arm-D plans, chosen at random before the first block) run back to back in a random arm order that is recorded. The 6 arm-B repeats run one per block in blocks 1-6 (the "6 in total" reading of SD-3; under the other reading every block carries 6 repeats). A block starts only after the previous one has finished, so an S-3 (spend) stop, which is tested only between blocks, leaves only complete blocks: every defect keeps its pair, and from block 6 on d0 can be estimated. An S-2 (safety) stop is tested after every run and can end a block early; S-5 records which estimates the completed blocks still allow.

**S-2. Safety (T-5).**

1. After every run the operator checks events 1, 2, 4 and 5 of the T-5 list (dispatch record, contract status, the snapshot's `git status` and tree hash taken before and after the run, and whether a T1 or `--depth quick` run called the panel). For event 3 (an unsupported citation certified) the operator, not a grader, re-reads every `file:line` citation that an arm C or D run certified against the snapshot (the evidence-validator pattern); the blinded grader's check after the last block remains the record (`src:534`). A fatal panel fault is therefore seen at the run that causes it, not after the whole spend.
2. STOP and report to the owner: any event in arm C or D; event 5 in any arm; event 4 in any arm (a reviewer write changes the repository that later runs read).
3. LOG and continue: events 1, 2 and 3 in arm A or B. These are legacy code paths that the panel does not change (the legacy engine already yields a MALFORMED contract for some recorded runs, see the Stage 0a null-score causes above); their counts are reported per arm beside arm C's as the baseline (own note: the source does not say whether its safety list covers the legacy arms, so the owner confirms this reading in S-0).
4. Event 3 found in arm C or D at grading fails the measurement under T-5 the same way; no runs remain to stop.
5. A stopped pilot does not restart by itself; the owner decides.

**S-3. Spend and runs that end without a result.**

1. Before run 1 the owner sets two ceilings, one per unit (the bases are never summed, `src:477`): claude tokens, at least the upper bound of row C-5 for the confirmed SD-3 reading (rows C-5 and C-5b), and retrieval tokens, at least the upper bound of row R-6. Rows C-1 to C-6 price the arms only; the cost of blinded grading, seeding and orchestration is outside them (SD-8), so the owner's figure must cover it. Dropping arm D or the repeats to fit a ceiling is not allowed: the repeats are the only source of d0, so T-6 could not be applied and the confirmatory request could not state d0.
2. Spend is the measured token count of each run in each unit, the same claude-token figure used for H-C (T-3, T-4); reruns count.
3. Before each block: if spend so far plus the block's runs at the profile band tops (claude: 8k per arm-A run and 70k per arm-B, C or D run; retrieval: 5k and 25k; `src:479`) would exceed either ceiling, the block does not start (STOP, report the blocks completed). After each block the operator also projects the total as spend so far plus the remaining runs of each arm at that arm's observed mean; a projection above a ceiling is a PAUSE (no new block until the owner answers) with the projection in the record. For claude tokens the band tops are above the kill values, so the first test is conservative; no kill value exists for retrieval tokens.
4. A run killed at the kill value is not rerun. For H-C it counts as above T-4 (its true cost is unknown but at least the kill value; without this T-4 cannot fail when kills are enforced). For recall its partial output is scored; if it wrote no report, its seeded defects are scored as not found in that arm (own note).
5. A run that crashed, timed out or ended with no contract at all is a failed run, not a MALFORMED contract (own note; the owner confirms in S-0). It is rerun only up to the allowance the owner set in S-0 (default none); a rerun that also fails is recorded as failed and scored as in S-3.4, and the block is kept. The report lists killed and failed runs per arm.

**S-4. Never a stop.**

- Any apparent result for H-A, H-B or H-C before the last block, in either direction: interim recall and precision are not computed, grading runs after the last block (which keeps graders blind to arm, `src:532`), and the pilot cannot decide H-B in any case (`src:536`).
- T-6: applied once after the last block, from the 6 repeats and the full set of plans, and reported in the confirmatory request (see "Owner approval"). (own note) For H-B, d_BC close to d0 is what parity predicts, so it is not a futility signal.
- T-4 at pilot size: with 12 runs in arm C (one per plan; arm B has 18 runs, 12 plus 6 repeats) a p95 is essentially the largest run (own arithmetic: 0.95 x 12 = 11.4, so the 12th ranked value); T-3 and T-4 are reported as descriptive values of the pilot, not as a pass.
- A shortfall against T-7: the report states that it measured sparse-labelled plans only (`src:540`).
- Events logged under S-2.3 and runs handled under S-3.4 and S-3.5.

**S-5. Stop record.** Every STOP and every PAUSE writes one record to `<pilot output dir>/stop-record.md` before anything else happens (own note), with: the rule id (S-2 to S-3) and the threshold id (T-n) with the observed value against it; the run id (plan, arm, repeat number) and its UTC start and end; cumulative claude and retrieval tokens, per arm and in total, and the projection if S-3.3 was involved; the detector output that triggered it (for event 4 the before and after repository status and the diff; for event 3 the citation re-read result; for events 1, 2 and 5 the dispatch record or contract status); the blocks completed and which of d_BC, d_AB and d0 they can estimate (each estimate is stated with its n; a safety stop fails the measurement under T-5 whatever the estimates); any other rule that fired at the same boundary; and, for a PAUSE, the owner's answer and its time. The operator writes the record; graders keep seeing blinded input.

## Inconclusive is not a pass

If the confirmatory interval crosses the margin (T-2), H-B is inconclusive and Stage 3 does not proceed; Stages 0-2 still ship (`src:544`). A pilot result is never read as a pass of H-B (`src:536`). Stage 3 entry needs the first measurement passed (H-B, H-C, safety) (`src:411`).

## Owner approval

- **Before the confirmatory run:** the owner approves the spend (`src:538`). The request states the pilot's observed d_BC, d_AB and d0, the resulting `n_plans` from the confirmatory formula, and its cost from rows C-1 and R-1 (own note on what the request contains).
- If H-A fails, the owner chooses between shrinking T2 to 2 reviewers and tuning the rubric (O-8) (`src:527`).
- (own note) Task 4's FAIL against the old T-9 wording stopped this plan for owner review; the owner redefined T-9 on 2026-11-12 (`conversion-gate-redefinition.md`).
- **Before the pilot (Stop rule S-0, own note):** the owner approves the stop rule, the reading of "6 repeats of arm B" (SD-3), the claude-token and retrieval-token ceilings of S-3.1, the rerun allowance of S-3.5 and the Stage 0 exit state.

## Source discrepancies

| Id | Where | What | How this document handles it |
|---|---|---|---|
| SD-1 | `src:536` | 618 x 0.30 = 185.4 and 275 x 0.35 = 96.25 are rounded to the nearest whole number (185, 96), while sample sizes are normally rounded up (186, 97). | Source figures kept as stated and the rounded-up value shown (rows A-6, A-7). Plan counts use the source's own `ceil` formula on unrounded values, so they do not change (49 and 26). |
| SD-2 | `src:536` | Power at d = 0.20 recomputes to 53.5% (Phi(0.087) = 0.535), which rounds to 53%, not "about 54%". | Recomputed value shown (row A-11). The conclusion (the pilot does not decide H-B) is unchanged. |
| SD-3 | `src:538` | The 6 repeats of arm B are not costed, and the text does not say whether they are 6 runs in total or 6 per plan. | Costed as 6 runs (row C-4), the other reading priced in a note; owner to confirm. |
| SD-4 | `src:536` | Pilot power is quoted without the 1.3 clustering factor that the confirmatory size uses. | Not an arithmetic error; power with the factor shown (row A-12). |
| SD-5 | `src:542`, `src:436`, `src:438` | Recorded counts 42, 33 and 7 differ from Stage 0a's 43, 34 and 8; the source's null breakdown (2 single-reviewer-fallback, 3 illegal values, 1 adversarial with a null score, 1 `sc-adversarial-protocol-mode-a`) differs from Stage 0a's classification. | Stage 0a values used (table above); the source counts are not silently changed. |
| SD-6 | `src:538` | "A stop rule" is required but not defined. | Proposed rule S-0 to S-5 marked as own, for owner decision; it also settles the safety scope for the legacy arms, the handling of killed and failed runs and the run order, which the source does not state. |
| SD-7 | `src:540` | The heterogeneity check for pooling has no named test or level. | Recorded in T-10; to be fixed before the confirmatory run. |
| SD-8 | `src:538`, `src:479` | The cost rows price the arms only: blinded grading, seeding and orchestration are not priced, retrieval is outside the claude-token sum, and the source does not say whether the `shadow` form of arm C costs more than one panel run. | Not priced here (no source figure). The owner's ceiling in Stop rule S-3.1 must cover them; the cost of the `shadow` form is unknown. |

## Stage 0 exit checklist

The four exit items of the Stage 0 row (`src:408`), each with the artifact that answers it:

| # | Exit item (`src:408`) | Artifact | Status |
|---|---|---|---|
| 1 | 50-pair hand-labelled cluster check | `cluster-pairs-50.csv` | **PENDING (owner labels).** AI labels exist (`pair-labels/README.md`, `cluster-pairs-50.ai-labelled.csv`: precision 0.84, recall 0.95 on the sample) and are not human labels; they do not meet "hand-labelled". The sheet holds 50 of 50 rows (25 merged, 25 apart; shortfall none) with the `human_same_defect` column blank; it is scored with `uv run python scripts/reflect_cluster_pairs.py score` after the owner fills it. |
| 2 | Conversion share of at least the T-9 value | `stage0a-report.md`, `conversion-gate-redefinition.md` | **Recorded cards: 67.28%** (479 / 712), now a baseline, not a gate (owner redefinition, 2026-11-12). **Redefined gate: NOT YET MEASURED**; it needs cards written under the findings-v2 reviewer brief (`conversion-gate-redefinition.md`, "How it is measured"). |
| 3 | Consumer grep result stored | `consumer-inventory.md` | Stored: 320 hit files (producer 51, validator 4, consumer 239, not in scope 26). It records 2 prose lines in `src/` with a `contract_version == "1.8.0"` equality (0 Python code lines) and no match in `.dev/eval-workspaces/sc-reflect/grader.py`. |
| 4 | Pilot designed and costed | `pilot-design.md` (this file) | Designed and costed as a pilot; the stop rule, the reading of the arm-B repeats and the spend ceilings await the owner (SD-3, SD-6, SD-8). |

Also shipped in Stage 0 (not an exit item): the lint test design, `lint-test-design.md` (Task 6; implemented by Task 15).

**Stage 0 exit: PENDING.** Item 1 waits for the owner's labels and item 2 (redefined) has no measurement yet, so the Stage 0 exit is not met (plan Constraints; `stage0a-report.md`; `conversion-gate-redefinition.md`).
