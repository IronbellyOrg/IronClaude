# Round 2, V2 (FAIL on the unchanged row)

## R-1. V1's sentence is necessary but not sufficient
V1's sentence names the measure, but "any numerical comparison must use that same quantity" leaves the comparison itself open. INV-004 asks for "tolerances"; a tolerance without a rule is a number the owner reads after the data. F9 shows a point-in-band reading fails by chance (all eight inside: 0.026 at n=10). So the rule is required. The consequence is required in one narrow place only. REQ-41 and REQ-44 are met by numbers plus commit order. But `TESTING.md:149` pins the REQ-45 sentence, so a below result on C4 or C8 would otherwise ship that sentence unqualified. That is the misleading outcome, so one consequence clause is required. A consequence beyond that clause is nice to have.

## R-2. Denominator: survival among selected rows
Read in `analyze.py:856-914`: `_sheet_acts` appends to `pairs` only inside `if hit`, and the non-sheet branch sets `act = bool(acting)`. So `acting` is empty whenever `act` is false, and `merge_survival` cannot be true with `act` false (V3 is right). Numerator is therefore `merge_survival` true alone. The band includes survival (`MR:539`), so drop nothing the band includes. One gap remains that nobody named: `MR:539` also puts extraction inside act, while selected rows already passed it. The measured value can therefore only be at or above the band quantity, so only "below" may be acted on. Null `merge_survival` means no `merged/ledger.json` (line 911), a run-level fact: exclude those item-runs, disclose the count. Treating null as "not survived" biases low and breaks the one safe direction.

## R-3. Caveat beside the sentence
Agree with V1: caveat, no deletion, sentence unchanged (`TESTING.md:149-150`).

## R-4. 95% Wilson, minimum 10
95% (`WILSON_Z`, line 49): false flags at most 0.9% (`v3_rule_sim.out` 1). Minimum 10 selected item-runs. Honest limit: at n=10 to 18 the below flag cannot fire for C1, C3, C6 or C7 (power 0.00, section 2); it can for C2, C4, C5, C8, which includes both REQ-45 classes.

## Replacement for 15.1 row 2

**Decision cell:** Per-class act-rate bands to pre-register (REQ-41, INV-004): the numbers, the quantity they describe, and what a result outside them may change. Defaults are the act ranges of `MR` 3.1(d).

**Recommended cell:** C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65. Planning values, not results. *Measure:* SS arm only, Stage 1 and Stage 2 apart, never pooled, derivation set excluded; per class, the share of item-runs with `selection` true and `merge_survival` not null whose `merge_survival` is true. It is not the `act` stage rate over all rows. *Rule:* 95% Wilson interval; under 10 such item-runs the class is "not assessable" (counts shown); otherwise "below" if the whole interval lies under the band, "above" if over, else "not contradicted". *Consequence:* report only. A "below" flag on C4 or C8 puts a caveat beside the REQ-45 sentence ("the measured share was below its planning band; consistency is not corroborated"); the sentence is unchanged. *May:* state the flag; add that caveat. *May not:* change a gate, G0 or D1-D7 result; disqualify or re-rank an arm; move a band; pool classes; read "above" or "not contradicted" as confirmation; compare the unconditional `act` stage with a band.

## Replacement for "Not checked" (add)
- Bands include extraction and survival (`MR:539`); the measure is conditional on selection, so it is at or above the band quantity. Only "below" is acted on.
- Wilson ignores correlation between runs on one item; the false-flag and power figures are optimistic.
- Item-runs without a merge file are excluded; hold-out class mix is unknown, so some classes may be not assessable.

## Round 1 positions changed
- Denominator: leaned to V3's act-only; now survival among selected rows (numerator `merge_survival` alone).
- Dropped V3's 3-distinct-item floor (concession kept, now removed from the text).
- Consequence narrowed to "below" only; the "above" direction is report-only.
- Dropped the optional pooled cross-check and the 90% interval.
- Unchanged: FAIL on the unchanged row, on the unnamed measure only.
