# Round 2, V3 (final)

## 1. Code check
Re-read `analyze.py:856-914` and `_sheet_acts` 934-955. V2 is right: `pairs` grows only inside `if hit`, and `acted` is set in that same branch, so `acting` is non-empty only when act is true. Survival true therefore implies act true for SS. On the null rows: `merge_survival` is None only when `members` is None, meaning no `merged/ledger.json` (line 911). That is a run-level gap, and it nulls act-true and act-false rows alike. Excluding those rows is right. Counting null as "not survived" would bias the measure low and could fire a false "below". I disagree with V1 only here (V1 wants missing survival kept in the denominator).
Caveat: whether "selected" implies "extracted" is UNVERIFIED (`items.json` vs `candidates.json`), so the measure is equal to or above the band quantity. Only "below" is safe to act on, as V2 says.

## 2. Power
`v3_rule_sim.out` section 2 confirms V2: low-side flag at n=10/18 is 0.00 for C1, C3, C6, C7. The zeros for C1, C3 and C6 are partly clamped-truth artefacts. The structural reason holds without the sim: Wilson 95% upper bound at k=0 is 3.84/(n+3.84), which is 0.18 at n=18, above the lows 0.10, 0.03, 0.05 and 0.15. For C4 and C8 at one band-width below, power is 0.24/0.20 at n=10 and 0.52/0.72 at n=18; Stage 2 should give about 16 selected item-runs each (V3 paper, UNVERIFIED mix). So the clause is not pointless: it governs exactly the two REQ-45 classes, and the flag can fire there. For the other classes silence is not confirmation, and the may-not list says so. Acceptable.

## 3. Smallest change
V2's text can lose: the rewritten Decision cell (leave it as it is), the separate "May" sentence (fold into the consequence), and the "disclose count" duplicate. Keep everything else.

**Recommended cell (replaces the current one):** C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65. Planning values, not results. *Measure:* SS arm only; Stage 1 and Stage 2 apart, never pooled; derivation set excluded. Per class: among item-runs with `selection` true and `merge_survival` not null, the share with `merge_survival` true. It is not the unconditional `act` stage rate. *Rule:* 95% Wilson interval; under 10 such item-runs "not assessable" (counts shown); else "below" if the whole interval is under the band, "above" if over, else "not contradicted". *Consequence:* report only. A "below" flag on C4 or C8 adds a caveat beside the unchanged REQ-45 sentence: "measured share below its planning band; consistency not corroborated". *May not:* change a gate, G0 or D1-D7 result; disqualify or re-rank an arm; move a band; pool classes; read "above" or "not contradicted" as confirmation; compare the unconditional `act` stage with a band.

**Not checked (add):**
- Selected item-runs are not shown to be extracted, so the measure is equal to or above the band quantity; only "below" is acted on.
- Wilson ignores correlation between runs on one item. At 10-18 item-runs the "below" flag cannot fire for C1, C3, C6 or C7. Item-runs without a merge file are excluded and counted.
- Hold-out class mix is unknown; some classes may be not assessable.

## 4. Code that does not exist
Nothing computes the measure or the flag. `ACT_BANDS` (`analyze.py:508-517`) is only range-checked by `prereg` (1072-1103); `test_prereg.py` and `TESTING.md:142-143` pin only the numbers and the commit order. Add to Not checked, one line: "Not built: no code computes the per-class measure or the flag, and no test covers them. Until a follow-up change adds both, the rule is applied by hand from `stages.jsonl` and the report says so." This is a recorded follow-up, not a stub. The registration is valid without it because the rule is fixed before the data.

## 5. Residual disagreements
- V1: null survival belongs in the denominator. I say excluded and counted.
- V1: its one sentence suffices. It lacks the rule and the C4/C8 caveat.
- A hand-written caveat is outside the generator test of `TESTING.md:149`; the named-reviewer check (150) should confirm it.
- Wilson coverage under clustering is unknown; accepted because the result is report-only.

## Verdict
FAIL on the unchanged row (unnamed measure); the text above removes the blocker.
