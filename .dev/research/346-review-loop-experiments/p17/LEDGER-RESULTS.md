# #346 defect-ledger rescoring (2026-11-10)

Method: all 511 blocking findings (first reviews and frozen audits, 13 arms, 140 audits) were clustered into 20 chunks; 20 validator agents (11 Opus, 9 Sonnet) merged them into defects and checked each against the original spec; one Opus reconciler deduplicated them into a ledger of **44 defects (20 blocking, 5 minor, 19 medium)**, 7 introduced-defect patterns, 5 unvalidated candidates, 9 rejected and 2 unverifiable. Then each of the 70 final specs was scored blind (arm names removed, order shuffled) by one Sonnet agent against every ledger defect: FIXED / DELETED_OK / PARTIAL / PRESENT / WORSE / MOOT_BAD. Six specs were scored again by Opus as a calibration.

Calibration (6 specs, Sonnet vs Opus): exact status agreement 96.2%, fixed-vs-residual agreement 98.1%; Opus is slightly stricter (5 FIXED to PARTIAL, 4 PRESENT to PARTIAL), by about the same amount on a baseline spec and on an ab3 spec, so arm comparisons are not affected.

## Results: residual ledger defects per final spec (lower is better)

`resid_blk` = blocking defects still present (PRESENT, PARTIAL, WORSE, MOOT_BAD) out of 20; `weighted` = 3 x blocking + 2 x medium + 1 x minor residual; `fixed` = defects FIXED or DELETED_OK out of 44; p = two-sided permutation test (20,000 shuffles) on the weighted score vs the fresh Sonnet baseline (Haiku arms vs the Haiku baseline). Loop tokens are output tokens per run, loop steps only (no audits). ab2 and ab3 have no R1 step in their recount, so ~31k (baseline R1) was added: marked ~.

| arm | n | resid_blk /20 | weighted | fixed /44 | p vs baseline | introduced patterns | loop tokens | x fresh |
|---|---|---|---|---|---|---|---|---|
| FRESH baseline | 6 | 17.3 | 94.8 | 2.8 | - | 1.2 | 53,623 | 1.00x |
| stored baseline (stale) | 6 | 16.7 | 91.3 | 4.2 | 0.432 | 0.7 | 100,424 | 1.87x |
| ab1 k=3 union+verify | 6 | 14.3 | 85.5 | 6.0 | 0.079 | 1.3 | 122,146 | 2.28x |
| ab2 verify gate k=1 | 6 | 17.5 | 95.2 | 2.7 | 0.945 | 0.7 | ~74,152 | 1.38x |
| ab3 final whole-doc gate | 6 | 13.8 | 83.2 | 6.8 | 0.022 | 0.7 | ~122,552 | 2.29x |
| ab4 lint + k=2 + verify | 6 | 14.3 | 84.8 | 6.3 | 0.027 | 1.2 | 106,519 | 1.99x |
| PN1 panel+merge+ledger | 6 | 10.0 | 63.0 | 15.7 | 0.003 | 0.8 | 408,316 | 7.61x |
| PN2 mechanical lint | 6 | 18.5 | 98.5 | 1.5 | 0.227 | 0.3 | 47,033 | 0.88x |

| Haiku arm | n | resid_blk /20 | weighted | fixed /44 | p vs Haiku baseline | loop tokens |
|---|---|---|---|---|---|---|
| Haiku baseline | 6 | 17.7 | 93.5 | 3.7 | - | 167,382 |
| ab1 (Haiku) | 4 | 14.5 | 84.0 | 6.8 | 0.081 | 419,037 |
| ab2 (Haiku) | 4 | 16.5 | 91.5 | 4.0 | 0.730 | 235,803 |
| ab3 (Haiku) | 4 | 13.8 | 80.2 | 8.2 | 0.034 | 319,005 |
| ab4 (Haiku) | 4 | 13.0 | 75.5 | 10.2 | 0.025 | 254,000 |

## Marginal cost of each fix (Sonnet arms, vs the fresh baseline)

| arm | extra fixed defects | extra loop tokens | fixes per 100k extra tokens |
|---|---|---|---|
| ab1 | 3.2 | 68,523 | 4.6 |
| ab3 | 4.0 | 68,929 | 5.8 |
| ab4 | 3.5 | 52,896 | 6.6 |
| pn1 | 12.8 | 354,693 | 3.6 |

## What this shows

1. **The loop does not converge, and the audits were hiding that.** The unchanged design fixes about 3 of 44 ledger defects (17 of 20 blocking defects remain in its final spec). A frozen audit reports about 1.2 blocking findings per spec, i.e. it samples roughly 7% of the blocking defects actually present. That sampling is why n=6 audit scores could not separate anything.
2. **With the ledger the instrument is far tighter** (residual blocking sd about 2 per spec on a mean of 17, against roughly 60% relative noise for the audit count) and **three designs differ from baseline at p<0.05: PN1 (p=0.003), ab3 (0.022) and ab4 (0.027); ab1 is at p=0.08.** The same pattern holds on Haiku (ab3h p=0.034, ab4h p=0.025, ab1h p=0.08).
3. **PN1 has by far the largest effect** (15.5 fixed against 2.8; 10 of 20 blocking left against 17) but needs about 408k loop tokens in its complete runs (r4-r6), 7.6x the baseline, spread over Fable, Sonnet and Haiku tiers. The earlier 66,240 figure for PN1 was wrong (it lacked most of the R1 panel steps) and is withdrawn. Runs r1 and r2 still have unmatched panel steps, so their totals are undercounts.
4. **ab4 is the most economical improvement** (6.6 extra fixes per 100k tokens, about 2x baseline cost); ab3 and ab1 land near it. **PN2 (mechanical lint alone) and ab2 (verify gate alone) do nothing for the final spec**, though PN2 is the cheapest arm.
5. **No design makes the loop converge.** Even PN1 leaves half the blocking defects. The ones that survive in almost every arm are the P1 scope and AC-0.4 step-3 defects (per-defect table: `score/perdefect.md`): reviewers raise them but the revise step does not resolve them.

## Checks done and limits

- **Circularity.** The ledger comes from findings of the same runs, so an arm whose reviewers found more could look better. Leave-source-out check: restricting to defects supported by 2 or by 3 or more arm families leaves the ranking and significance unchanged (PN1 p=0.003, ab3 0.022, ab4 0.027/0.049, ab1 0.079/0.047). 14 of 44 defects were raised by one arm family only (ab4, pn1, ab3).
- **Fix by deletion.** DELETED_OK occurs 0-2 times per arm in total; PN1 specs stay about the size of the original (290 vs 285 lines) with 54 changed diff lines per spec on average; WORSE or MOOT_BAD occurs 3 times across the 6 PN1 specs and 0 times in the baseline.
- **New defects.** Introduced-pattern hits are 0.3-1.3 per spec in every arm with no trend; unvalidated "other new defects" are 0.2-0.8 per spec (PN1 0.8, baseline 0.2).
- **Ledger completeness is unknown.** 5 candidate defects found only while reconciling were present in nearly every spec; 14 defects have a single source arm family. A defect nobody found is invisible to this method.
- n=6 per Sonnet arm (4 per Haiku arm). The ledger scorer is Sonnet; Opus agrees with it on 96% of 264 judgements.

## Token lanes: where PN1's 408k loop tokens come from (added 2026-11-10)

Complete PN1 runs b1-r4..r6, mean output tokens per run, by lane (per-step models from the transcripts; `tokens_models.py`):

| lane | models in this experiment | live-environment meaning | tokens | share | x fresh baseline (53,623) |
|---|---|---|---|---|---|
| primary | Sonnet 5.5 (R1.t1b reviewer, V1, V2, R2, R3) | primary model | 106,357 | 26% | 1.98x |
| parallel Tier 2/3 reviewers | Haiku 5.5 stand-ins (R1.t2-1, R1.t3-1, R1.t3-2) | Tier 2 and Tier 3 gateway models, possibly other providers | 290,600 | 71% | 5.42x |
| adjudicator | Fable 5.2 (ADJ) | Tier 0 premium | 11,359 | 3% | 0.21x |
| total loop | | | 408,316 | 100% | 7.61x |

Reading: PN1's cost is dominated by the three parallel reviewers on cheaper stand-in models; its primary-lane cost (about 2x baseline) is equal to ab4's (106.5k). Per 100k extra primary-lane tokens PN1 buys about 24 extra fixed defects (12.9 for 52.7k), ab4 about 6.6. Caveats: the Haiku stand-ins wrote 68k-108k tokens each against 23k for the Sonnet reviewer, so live Tier 2/3 volume may differ; Tier 2/3 models are priced (only subscription models are free of marginal cost); Fable output is $50/M against Sonnet's $10/M, so the adjudicator's 11k tokens cost about half as much as the 106k primary tokens; input tokens are not counted.

**Policy note (owner rule, 2026-11-10):** Fable / Tier 0 is forbidden in all pipelines and Opus 5.5 is the ceiling (sparingly). PN1's historical runs used a Fable adjudicator, so the PN1 numbers above were produced under a condition that is no longer allowed. Later arms (ab5) run the adjudicator on Sonnet; if their ledger scores fall below PN1's, part of PN1's gain came from the Fable adjudicator.
