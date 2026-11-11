# p22 live A/B: Jev-split merge vs current merge (7-reviewer panel, 2026-11-11)

**Result: no improvement. Splitting the merge's rows with Jev made the final specs slightly worse (-3.0 fixed defects, p = 0.18, n = 6 per arm), with the same loop tokens.** Do not adopt it.

## Design

- **Both arms:** the pn1d2 panel (1 Sonnet + 6 Haiku in round 1, Sonnet re-reviews), the same frozen command, rules, spec and harness as the p19 replicate. 6 runs per arm, in blocked random order (seed 20261111), with at most 12 runs and 9 workers per arm in flight.
- **Control (c3):** the current merge. Findings that share a section reference are chained into one row (union-find over `same_defect`).
- **Jev arm (j3):** the same merge in round 1, but a pair of findings is linked only if `same_defect` matches AND Jev answers the p21 pilot Noul with P(same) >= 0.7. A missing answer means no link. Rounds 2 and 3 are unchanged. Code: `harness/harness_j3.py` (`jev_oracle`) and `harness/ledger_jev_split.diff`.
- **Scoring:** the 12 final specs were scored blind by Sonnet with the p17 instrument, as s130-s141 (sids assigned by a seeded shuffle; arm hidden from the scorers).
- **Sanity check:** the control's mean of 17.67 fixed matches the earlier pn1d2 replicate (17.67) exactly.

## Results

| Metric | Control (c3) | Jev split (j3) | Jev - control | p (permutation) |
|---|---|---|---|---|
| Fixed ledger defects /44 | 17.67 | 14.67 | -3.0 | 0.18 |
| Residual blocking /20 | 9.17 | 10.33 | +1.2 | 0.47 |
| Weighted residual | 58.3 | 65.5 | +7.2 (worse) | 0.19 |
| Introduced patterns | 0.83 | 0.33 | -0.5 | 0.41 |
| Round-1 ledger rows | 23.7 | 70.2 | +46.5 | 0.003 |
| Round-1 blocking rows (blockers sent to V1) | 4.3 | 14.0 | +9.7 | 0.003 |
| Loop output tokens (no audits) | 570,518 | 570,952 | +0.1% | 0.99 |
| Jev stage | - | 2,011 pairs, 246 linked, 0 failures, $0.051 total | | |

Adjudication (ADJ verdicts confirmed/rejected/unsure per run):
- **Control:** about 1-2 confirmed out of about 22 rows.
- **Jev arm:** 4-16 confirmed out of about 70 rows.

Every run in both arms ended in ESCALATE.

## Reading

- **The split worked as designed.** It cut cross-defect lumping (the pilot predicted rows rising from about 23 to about 56 to 70), and the Jev stage was cheap and reliable: $0.008 per run, no failed calls.
- **It did not help the outcome.** With 3x the blocking rows, the first revision (V1) got 14 narrow blockers instead of 4 broad clusters. The broad control rows, such as one row with 36 sub-claims, seem to work as useful "clusters of related problems": the reviser fixes root causes across them. Narrow rows lead to narrower edits. That is a plausible mechanism, not a measured one.
- **No token saving.** The adjudicator sees about 3x the rows, but total loop tokens are unchanged.
- **Small sample:** n = 6 per arm, so the 95% interval on the fixed-count difference is roughly -7 to +1. "No improvement" is solid; "it makes things worse" is not established.

## Implication for the Jev placements

The p21/p22 work found one placement where Jev beats a code rule on its own metric (duplicate detection: AUC 0.98-0.99). This A/B shows that winning on that metric did not carry over to the loop's real outcome. Before any Jev placement is adopted, it needs an end-to-end outcome test like this one, not just a component metric. Of the remaining candidates, issue-mode classification (test 3) has a direct outcome: the label is the output. The 10 proposals in `JEV-OUTSIDE-USES-AND-PROPOSALS.md` should each be judged that way.

## Files

- `slotter.py`, `drive.sh`: scheduler and driver.
- `harness/`: both arms' harness copies and the ledger patch.
- `runs/<run>/`: state.json, ledger.json and the Jev oracle for each run.
- `scores/`: s130-s141 with `key-p22.json`.
- `analyze_ab.py`, `ab_rows.json`: analysis script and per-run rows.
