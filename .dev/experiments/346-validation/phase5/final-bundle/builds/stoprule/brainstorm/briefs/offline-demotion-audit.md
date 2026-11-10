# Recorder step: offline demotion audit, after both replicates (source spec section 5.3)

Placeholders: `<reports>` every finalized review report of both replicates, space-separated; `<seed>` a fixed integer recorded in the run log before the draw; `<spec of report>` the spec version each sampled report reviewed (the `<saved copy>` of the next review, or the final spec for review 3); `<sample file>` and `<audit file>` output files of this step. `<skill base>` is `~/.claude/skills/sc-spec-panel-stoprule-protocol`.

1. Draw the sample: `uv run --no-project python "<skill base>/scripts/stoprule.py" audit-sample --report <reports> --seed <seed> --owner-k 5 > <sample file>`. Each JSON line is one item with `report`, `id`, `status`, `claimed`, `stratum`, `p` (its inclusion probability) and `owner`. The strata are fixed by the script:
   - `non-blocking`: 25% of the grader-`minor`, `minor-form` and `late-found` dispositions, minimum 2, at least 1 per non-empty sub-stratum;
   - `confirmed`: 25% of the confirmed blockers, minimum 2;
   - `resolved-prior`: 25% of the reviewer-`resolved` priors, minimum 2;
   - `critical-demoted`: every claim the reviewer labelled CRITICAL that ended demoted (not random, `p=1.0`).
2. Audit: one fresh general-purpose Agent call per report that has sampled items. Its prompt gives the full `<spec of report>`, the frozen rubric (`<skill base>/refs/rubric.md`) and, per sampled item, the claim's quote, span, outcome and evidence from the report's ledger, with no grader reason and no status. It asks, per item, "is this a blocking defect under the rubric?" and a JSON line `{"id":"<id>","real":true|false,"why":"<= 25 words"}`. Save the replies in `<audit file>`.
3. Owner labels: the owner independently labels the 5 items with `owner: true`, the same question, without seeing the auditor's answer.
4. Report:
   - demotion error rate = auditor-says-blocking / audited demotions (items of the `non-blocking` and `critical-demoted` strata), weighted by `1/p` and also unweighted;
   - auditor-owner agreement on the 5 owner items, as its own number;
   - the confirmed and resolved-prior strata as a check of the other direction.
5. Read the result against the pre-registered falsifier F2: an error rate above 20% over at least 8 audited demotions means the grader removes real defects. Fewer than 8 audited demotions: the accuracy claim is NOT ESTABLISHED, not passed. The audit never changes a recorded verdict.
