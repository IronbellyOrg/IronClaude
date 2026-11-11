# PN1 randomized-order replicate: original panel (1S+3H) vs doubled Haiku (1S+6H)

Issue #346. Six runs per arm, 12 runs total, same real spec (S1), same 44-defect ledger v1, blind Sonnet scorers (sids s94–s105, run order shuffled, key in `key-rep.json`). No Fable/Tier 0 anywhere. No Jev calls were made in this replicate.

## Design
- Arms: `pn1o` = original PN1 panel (1 Sonnet + 3 Haiku reviewers, merge, typed ledger, ADJ), `pn1d2` = same with 6 Haiku reviewers (1S+6H). ADJ ran on Sonnet in both.
- Order: blocked randomization, seed 20261110, order `o,d,d,o,o,d,o,d,o,d,d,o` (see `slots.json`). Slot-limited concurrency: slots 0–2 launched at 20:25 (k=3), slots 3–11 at 20:36 (k=12). Worker cap per directory 9.
- Scoring: same ledger procedure as ab5 and pn1m/pn1d. Fixed = FIXED + DELETED_OK. Weighted residual = 3/2/1 on blocking/medium/minor over PRESENT+PARTIAL+WORSE+MOOT_BAD.

## Per-run results

| sid | arm | run | start slot | fixed | weighted residual | blocking residual | introduced |
|---|---|---|---|---|---|---|---|
| s96 | pn1o | o2-r1 | 0 | 21 | 49 | 6 | 1 |
| s99 | pn1o | o2-r2 | 3 | 13 | 69 | 11 | 1 |
| s103 | pn1o | o2-r3 | 4 | 15 | 62 | 9 | 0 |
| s94 | pn1o | o2-r4 | 6 | 15 | 68 | 13 | 2 |
| s105 | pn1o | o2-r5 | 8 | 13 | 66 | 9 | 3 |
| s101 | pn1o | o2-r6 | 11 | 15 | 64 | 10 | 1 |
| s97 | pn1d2 | d2-r1 | 1 | 15 | 63 | 10 | 0 |
| s102 | pn1d2 | d2-r2 | 2 | 20 | 51 | 7 | 0 |
| s95 | pn1d2 | d2-r3 | 5 | 17 | 57 | 8 | 0 |
| s100 | pn1d2 | d2-r4 | 7 | 16 | 62 | 9 | 2 |
| s104 | pn1d2 | d2-r5 | 9 | 19 | 53 | 7 | 0 |
| s98 | pn1d2 | d2-r6 | 10 | 19 | 55 | 8 | 1 |

## Arm summary (this replicate and earlier same-protocol batches)

| arm | n | fixed (mean ± sd) | weighted residual | blocking residual |
|---|---|---|---|---|
| pn1 (earlier original) | 6 | 15.7 ± 3.5 | 63.0 ± 9.9 | 10.0 |
| **pn1o (replicate original)** | 6 | **15.3 ± 2.9** | 63.0 ± 7.3 | 9.7 |
| pn1d (earlier 1S+6H) | 6 | 19.3 ± 1.8 | 53.0 ± 3.6 | 7.2 |
| **pn1d2 (replicate 1S+6H)** | 6 | **17.7 ± 2.0** | 56.8 ± 4.8 | 8.2 |
| pn1m (earlier 3S+3H) | 6 | 18.7 ± 5.4 | 54.0 ± 14.0 | 7.2 |

Permutation tests (50k shuffles, two-sided, difference in means):

| comparison | fixed | weighted residual |
|---|---|---|
| pn1d2 vs pn1o (replicate, randomized) | +2.33, p=0.168 | −6.17, p=0.129 |
| pn1o vs pn1 (original reproduces?) | −0.33, p=0.929 | 0.00, p=1.000 |
| pn1d2 vs pn1d (doubled Haiku reproduces?) | −1.67, p=0.202 | +3.83, p=0.176 |
| pooled 1S+6H (pn1d+pn1d2, n=12) vs 1S+3H (pn1+pn1o, n=12) | **+3.00, p=0.013** | **−8.08, p=0.008** |

## Findings
1. **Original PN1 is stable.** The replicate (15.3) reproduces the earlier batch (15.7) almost exactly; the difference is noise (p=0.93).
2. **Doubling Haiku helps, by about +2 to +3 fixes (≈ +15%).** The replicate alone is underpowered (p=0.17) but moves the same direction as the first batch. The first batch regressed toward the mean (19.3 → 17.7). Pooling the two independent 6-run batches per protocol gives +3.0 fixes and −8.1 weighted residual (p≈0.01). The pooled test treats batches as exchangeable; the earlier pn1d batch ran under a different launch schedule (MAX_CONCURRENT 8) and an earlier harness copy, so treat the pooled p-value as supporting, not definitive.
3. **Variance is lower with six Haiku reviewers.** sd 2.0 (pn1d2) and 1.8 (pn1d) versus 2.9 (pn1o) and 3.5 (pn1). The one very high original run (o2-r1, 21 fixes) has no counterpart among the doubled-Haiku runs.
4. **Start order does not explain it.** Rank correlation between launch slot and fixed count is −0.02 over all 12 (pn1o −0.03, pn1d2 +0.37). The three runs launched at k=3 averaged 18.7 fixes versus 15.8 for the other nine (+2.9, p=0.155, confounded by the o2-r1 outlier). The earlier worry that fix conversion declines with launch order is not reproduced under randomized blocks.
5. **Variety of defects caught.** Distinct defects fixed in at least one run: pn1o 26, pn1d2 28, combined 32 of 44. Defects fixed in all six runs: 7 in each arm. Defects fixed in exactly one run: 5 (pn1o), 7 (pn1d2). Four defects were fixed only by pn1o, six only by pn1d2. D08, D22, D24, D25 and D30 were fixed at least 50 points more often by pn1d2, and none the other way. The extra Haiku reviewers mostly raise the fix probability for defects that are already catchable, and add a few new ones, rather than opening a different set.
6. **Cost.** Mean tokens (out + in + cache-write, audits excluded; indicative only): primary Sonnet lane 1.23M (pn1o) vs 1.16M (pn1d2); parallel Haiku lane 0.65M vs 1.48M. The extra roughly 0.83M Haiku tokens bought about +2.4 fixes in this replicate.
7. **Introduced defects** are comparable: mean 1.3 (pn1o) vs 0.5 (pn1d2) per run. No evidence that more reviewers add regressions.

## Caveats and anomalies
- The first scoring pass was discarded: my build step produced empty diff files (wrong relative path) and left the `__OUT__` placeholder unfilled. All 12 scorers were stopped or discarded (kept in the scratchpad, not in this directory), diffs and prompts were regenerated, and a clean pass of all 12 scored. Only the clean pass is reported.
- Monitors: duplicate LAUNCH lines were launched once. One monitor printed a traceback when two watches overlapped; all state files parsed afterward and the monitor was stopped. No run was lost.
- `o2-r6 R1.t1b-1` reported writing one temporary script in the run's parent directory outside its sandbox; it read only the report and candidate spec and was deleted.
- Scorers are Sonnet, blind to arm; ledger v1 has 5 candidate defects (N01–N05) that were PRESENT everywhere and do not affect comparisons.
- Token figures are from the harness state logs and exclude audits; earlier lane figures for old PN1 came from a transcript matcher, so cross-batch token comparisons are indicative only.

## Files
`scores/s94–s105.json` blind ledger scores, `key-rep.json` sid → arm/run map, `slots.json` order and launch times, `analyze_rep.py` / `tok_union.py` analysis, `build_score.py` scoring-set builder (corrected here for the diff-path and `__OUT__` bugs described above), `slotter.py` / `drive_rep.sh` scheduler.
