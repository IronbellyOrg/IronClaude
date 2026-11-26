# Round 2 — V1

## R-1 — FAIL on the unchanged registration

Yes: a reader has legitimate textual grounds to compare the report's named “act” rate with the registered “act-rate” band; that comparison would mislead. It is not a statistically legitimate like-for-like comparison: selection and survival differ (F3–F4). The shared label silently licenses precisely the selection-as-model-miss confusion the stage split was intended to prevent (F5). That meets “misleading” without requiring an adoption gate. I therefore change to **FAIL**, narrowly, on the unnamed measure—not on the endpoints, missing consequences alone, or sample size.

I would accept this exact additional sentence as removing that blocker:

> “These unvalidated SS planning bands describe the proportion of selected item-runs in which act occurs and the finding survives merge; any numerical comparison must use that same quantity, separately for Stage 1 and Stage 2, not the unconditional operational act stage, and no departure changes an adoption gate or invalidates an arm.”

This names what is registered and forbids the misleading comparison; a full statistical decision rule is an improvement, not necessary to remove this defect (F6–F7).

## R-2 — Prefer act-and-survive among selected rows

Use all selected item-runs of the class as denominator and selected item-runs with both act and merge survival as numerator. Missing survival must be disclosed, not silently removed to change the population. This preserves the quantity used to construct the bands (F3), whereas excluding survival deliberately changes it. Merge variation is part of that target, not merely unwanted noise. Act among selected rows remains useful separately: its “below” direction is conservative because act-and-survive cannot exceed act; its “above” direction cannot establish that the historical quantity exceeds the band (F3–F4).

## R-3 — Caveat, not deletion

Add a caveat beside the fixed REQ-45 sentence if a registered descriptive rule flags C4/C8 below; do not present the expectation as corroborated. `TESTING.md:149–150` explicitly requires the generator's sentence to equal REQ-45 and a reviewer to confirm that wording. Deleting it would introduce a separate requirement conflict. F7 establishes no automatic withdrawal rule.

## R-4 — Accept 95% Wilson and 10 as conventions only

Accept 95% Wilson and a minimum of 10 selected item-runs for descriptive flags; report smaller samples as not assessable and retain their counts. Neither choice is a validated evidential threshold: repeated runs are correlated (F8), so ordinary Wilson coverage is not guaranteed. Do not restore the unsupported distinct-item floor or interpret overlap as confirmation. F9 defeats a point-in-band rule, not registration itself.
