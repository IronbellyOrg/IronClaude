# Step 08 results: fallback LLM judge, five runs (not a Jev run)

Truth: panel mean >= 4.0 (82 blockers of 318). Status-quo baseline (every finding was filed as blocking): precision 25.8%, recall 100%.

| Run | Rows | BLOCKING | SHOW_USER | FOLLOW_UP | NOTE | Accuracy (SHOW_USER = not blocker) | Precision | Recall | Accuracy (SHOW_USER = blocker) | Precision | Recall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 318 | 198 | 103 | 13 | 4 | 59.1% | 37.9% | 91.5% | 31.1% | 27.2% | 100.0% |
| 2 | 318 | 196 | 105 | 9 | 8 | 57.2% | 36.2% | 86.6% | 31.1% | 27.2% | 100.0% |
| 3 | 318 | 226 | 79 | 8 | 5 | 50.9% | 33.6% | 92.7% | 29.9% | 26.9% | 100.0% |
| 4 | 318 | 180 | 117 | 17 | 4 | 64.2% | 41.1% | 90.2% | 32.4% | 27.6% | 100.0% |
| 5 | 318 | 172 | 126 | 12 | 8 | 62.3% | 39.0% | 81.7% | 32.1% | 27.5% | 100.0% |

Findings answered in all five runs: 318. Findings whose blocker call flips between runs: 132 (41.5%).

Majority of five runs (BLOCKING in 3 or more runs) against the panel:

| | Panel blocker | Panel not blocker |
|---|---|---|
| Judge blocker | 76 | 126 |
| Judge not blocker | 6 | 110 |

Majority accuracy 58.5%, precision 37.6%, recall 92.7%.

BLOCKING verdicts by confidence (pooled over runs): how often the panel agreed

| Confidence bin | Verdicts | Panel agreed |
|---|---|---|
| 0.3-0.4 | 64 | 30 (47%) |
| 0.4-0.5 | 36 | 17 (47%) |
| 0.5-0.6 | 26 | 20 (77%) |
| 0.6-0.7 | 11 | 10 (91%) |
| 0.7-0.8 | 370 | 81 (22%) |
| 0.8-0.9 | 389 | 147 (38%) |
| 0.9-1.0 | 76 | 58 (76%) |

Largest disagreements (panel mean in brackets):

- F-B07-010 [2.00] panel not blocker, judge majority blocker
- F-B09-003 [2.33] panel not blocker, judge majority blocker
- F-B06-001 [2.33] panel not blocker, judge majority blocker
- F-B01-004 [2.33] panel not blocker, judge majority blocker
- F-B01-018 [2.67] panel not blocker, judge majority blocker
- F-B09-002 [3.00] panel not blocker, judge majority blocker
- F-B04-001 [3.00] panel not blocker, judge majority blocker
- F-B06-021 [3.00] panel not blocker, judge majority blocker
- F-B08-004 [3.00] panel not blocker, judge majority blocker
- F-B02-006 [3.00] panel not blocker, judge majority blocker
- F-B05-017 [4.00] panel blocker, judge majority not blocker
- F-B03-024 [3.00] panel not blocker, judge majority blocker
- F-B07-031 [3.00] panel not blocker, judge majority blocker
- F-B08-002 [3.00] panel not blocker, judge majority blocker
- F-B09-005 [3.00] panel not blocker, judge majority blocker

## Diagnosis (added by hand after the run; no threshold or wording was changed)

Per-question mean probability (average of five runs) for the 82 panel blockers against the 236 others, and how well each question alone separates the two (AUC: 0.5 is a coin flip, 1.0 is perfect):

| Question | Mean, panel blockers | Mean, others | AUC |
|---|---|---|---|
| S safety, data loss, wrong target | 0.22 | 0.06 | 0.73 |
| W wrong result from following the text | 0.82 | 0.70 | 0.75 |
| E statement contradicts a named source | 0.59 | 0.55 | 0.53 |
| M required item absent | 0.25 | 0.26 | 0.54 |
| C quoted constraint broken | 0.25 | 0.23 | 0.55 |
| D a decision or result depends on it | 0.71 | 0.57 | 0.73 |

BLOCKING verdicts over all five runs, by the rule that fired, and how many the panel did not call a blocker: S rule 181 (60 not blockers); M or C rule 232 (194 not blockers); W with D rule 559 (355 not blockers).

## What this shows

1. The text-only judge is a weak classifier. Against the panel it gets 50.9% to 64.2% accuracy per run (SHOW_USER counted as not blocker), precision 34% to 41% and recall 82% to 93%. Always calling a finding a blocker (today's behaviour for this table) gives precision 25.8%. The gain is real but small.
2. It is unstable: 132 of 318 findings (41.5%) change their blocker call between runs.
3. Its confidence is not reliable as a gate. BLOCKING verdicts in the 0.7 to 0.9 confidence bins (759 verdicts) matched the panel only 22% to 38% of the time; the 0.9 to 1.0 bin matched 76%.
4. M, C and E are at chance here (AUC 0.53 to 0.55). With only a description and a context line to read, the judge cannot tell whether a required item is really absent or a constraint is really broken, and the rule "M or C is Y means BLOCKING" produced 194 false blockers in 232. These questions need the code-supplied inputs (required items, constraints, quoted evidence) that the historical table does not have.
5. S, W and D carry the signal (AUC 0.73 to 0.75). Reviewer descriptions almost always name a wrong result (W averages 0.70 even for non-blockers), so W alone does not separate; D (does something the document rests on depend on it) and S do more.

## What this does not show

- Nothing here measures Jev. The judges are Claude agents of the same model family as the three scorers, so agreement is probably flattered.
- The questions were finalised after reading the scored table, so the result measures consistency with the panel, not accuracy on unseen findings.
- Changing the table or thresholds now to lift these numbers, using the same 318 rows, would be fitting to the test. A fair second round needs the full inputs and a fresh set of findings.

## Spec section 7.6 items measured (added after the run)

| Group | Rows | TP | FP | FN | TN | Agreement | Cohen's kappa |
|---|---|---|---|---|---|---|---|
| All | 318 | 76 | 126 | 6 | 110 | 58.5% | 0.27 |
| Spec | 171 | 47 | 77 | 4 | 43 | 52.6% | 0.20 |
| Tasklist | 147 | 29 | 49 | 2 | 67 | 65.3% | 0.33 |

Contested rows (scorers differ by 2 or more points): 1 (F-B05-030). Too few to report separately in any useful way.

Not measured: per-question band reliability table, rows with a decision basis (this variant has none), recall on blockers a reviewer called minor (the table holds only findings filed as blocking), any code-review findings.
