# Gate stop: colour and theme phase (plan Phase 2, spec P1)

Status: STOPPED after iteration 3. The next phase is not started. Owner decision needed.

## Failing rows after iteration 3

- RB-08 at width 80 (High). Evidence: the ledger screen's key list is cut at 80 columns (`... m mark  e exp>`, the `e export all  q quit` part is lost) and the last line of the screen is `shown 31/54 | collected 80 / reported 80`, so "the footer keys are the last lines" does not hold. The script check (`checks.json`, RB-08, case `ledger@80`) fails the same way in all three iterations. All other in-scope rows (RB-01, RB-05, RB-06, RB-07, RB-09, RB-10, RB-11, RB-23) pass at all three widths in iteration 3.

## Iteration scores (failing High and Medium rows, per width)

| Iteration | 160 | 116 | 80 | What changed before it |
|---|---|---|---|---|
| 1 | RB-11 | RB-11 | RB-08, RB-11 | first render |
| 2 | RB-11 | none | RB-08, RB-11 | absent values at the end of a counts token muted; the selected question keeps its reason muted |
| 3 | none | none | RB-08 | the counts line `... unavailable (no source)` muted |

Reviewer answers (one per width per iteration): `artifacts/gates/p1/iter-<n>/reviewer-outputs/width-<W>.scores.md` in the plan package.

## Why this cannot be fixed inside this phase

The cut key list at 80 columns is finding M-11. The spec closes it in the text-defects phase (spec P2, step 2.3, `wrap_groups`, rubric RB-13) and that phase regenerates both presentation goldens. The colour phase must leave every `screen_lines` string and both goldens byte-identical (spec P1, "Byte-identical in this phase"). Fixing it here would break that rule. The same defect already failed on the baseline (`scores/baseline.json`, RB-08 at 80 is FAIL), although the spec's baseline expectation listed RB-08 as passing.

## Decision needed from the owner

Choose one:

- Option A (recommended): for this phase's gate only, treat the footer-key clause of RB-08 at width 80 as deferred to the text-defects phase, where RB-13 and the footer fix land, and close this phase as passed. Nothing else changes.
- Option B: pull the key-list fix (M-11) forward into this phase and re-baseline the release-1 presentation golden here; the colour phase then loses its "no text change" guarantee.

Until the owner answers, no later task of the plan is started.
