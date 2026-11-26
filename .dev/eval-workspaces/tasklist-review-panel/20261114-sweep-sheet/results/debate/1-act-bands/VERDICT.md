# Verdict: per-class act-rate bands to pre-register (DESIGN.md 15.1 row 2)

## 1. Verdict: FAIL

The eight numbers are fine to keep. The default fails because it registers them without saying what is measured, how a result is compared with a band, or what an outside result may change. Three blocking defects survived. All three advocates ended on FAIL (the Haiku defender changed from PASS in Round 2).

## 2. Surviving blocking defects, with evidence

**BD-1. The registration names no measured quantity, and the band and the measured stage rate are different quantities** (all three advocates, after Round 2).
- The band is the planning act range of `MR` 3.1(d): the chance, given that the item is on the sheet, that it is extracted, acted on and survives (`MR` 539, 357). The stage `act` in `analysis/analyze.py` is not conditional on selection (an unselected item is `act` false, lines 894-896) and excludes merge survival (lines 910-912).
- Failure case with numbers (`work/v3_rule_sim.out` section 3): if the model behaves exactly as planned, the unconditional rate is expected at 0.179 for C2 and 0.131 for C7, below the band floors 0.20 and 0.15; the chance of landing inside the band at 10 item-runs is 0.25 (C3), 0.35 (C7), 0.54 (C2). A selection miss would be read as a reviewer miss, the confusion `MR` 357 and 662 say the stage split exists to prevent.
- Blocking because the comparison would be misleading and no stated requirement says which quantity to use.

**BD-2. No comparison rule and no consequence** (V2 and V3; V1 accepted the fix; V2 judged it blocking only as the necessary companion of BD-1).
- Nothing consumes a band (`ACT_BANDS` appears only in `prereg()`, `analysis/analyze.py:508-517, 1072-1103`; no gate D1 to D7 or G0 reads it), but the REQ-45 claim for C4 and C8 rests on INV-004's "act-rate tolerances" (`MR` 1199; probe file `nested/adversarial-1/adversarial/invariant-probe.md:12`), and `TESTING.md` 149 pins that sentence.
- With no rule fixed before the data, a point reading of "inside the band" fails by chance: even if every planning midpoint is true, all eight classes are inside their bands with probability 0.026 at 10 item-runs per class and 0.092 at 18 (`work/band_sim.out` A); C3 at 5 item-runs has no possible inside value. The owner could then pick the reading after seeing the data.

**BD-3. The population is not pinned** (found by the Round 2.5 probe, INV-013, HIGH; not debated by the advocates).
- The band is for the primary panel (`MR` 539), but Stage 2 also runs SS on the haiku and sonnet panels (`TESTING.md` 263-264), `stages.jsonl` rows have no `panel` or `set` field, and `all --stage 2` loads them together (`analysis/analyze.py:579-583, 1234-1235, 1281-1290`). "SS only" would pool three panels and several material sets into one rate set against a primary-panel band.

## 3. Non-blocking notes

- The numbers are unmeasured planning values built from the three derivation packages (`MR` 543-553, 1206); only C8 cites a count (7 of 8 runs). Disclosed, so not blocking. That they transfer to hold-out and planted material is assumed.
- Width is not the defect. At the band midpoint a 0.25-wide band is hit 65-90% of the time at 18 item-runs (`band_sim.out` A).
- An outside result cannot invalidate an arm by code: no gate reads a band (probe INV-019). It could only do so through a misreading, now barred by the may-not list.
- Pooled band (0.223-0.456) rejected: it depends on the unregistered class mix (0.172 to 0.462 expected for the same true rates) and says nothing about C4, C5, C8. A Z0-anchored band rejected: Z0 act is a different quantity, does not exist before the freeze, and D2 already tests SS against Z0.
- Power is low: at 10 to 18 item-runs the "below" flag cannot fire for C1, C3, C6 or C7 (power 0.00) and fires only 0.20 to 0.72 of the time for C4 and C8 when the truth is one band-width below. Stage 2 should give about 16 selected item-runs for C4, C5, C8 (planning, UNVERIFIED; the hold-out class mix is unknown, ground truth was not opened).
- The Wilson interval ignores correlation between runs on one item and between items that share evidence (so figures are optimistic).
- Residual gaps logged in `adversarial/debate/invariant-probe.md` (8 MEDIUM, 1 LOW unaddressed before the merge; seven were folded into the text, the rest are in 15.2): the direction "measure at or above the band quantity" is assumed, not shown (INV-005); `bin/open-manual-checks.sh` has no attestation for applying the rule (INV-023); no order check covers the text (INV-017).
- Nothing computes the new measure or flag: `analysis/analyze.py`, `prereg()`, the tests and `TESTING.md` were not edited (outside the files this task may edit). The rule is applied by hand until a follow-up adds code and tests. This is recorded in `DESIGN.md` 15.2.

## 4. Refactored value (applied)

The single governing text is `DESIGN.md` section 15.1a (not copied here). In one line each:
1. Numbers unchanged: C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65, as planning values.
2. Measure: per class, among item-runs with `selection` true and `merge_survival` not null (and a finished reviewer), the share with `merge_survival` true; SS arm, primary panel only; Stage 1 and Stage 2 apart, Stage 2 sets apart; derivation set excluded.
3. Rule: 95% Wilson; under 10 item-runs "not assessable"; else below, above or not contradicted.
4. Consequence: report only; a "below" flag, or "not assessable", on C4 or C8 adds one sentence beside the unchanged REQ-45 sentence.
5. May not: change a gate or arm outcome, move a band, pool classes, treat above or not contradicted as confirmation, or compare a band with any other rate. Only "below" is acted on.

Status: the text is a recommendation. The owner has not confirmed it (`results/owner-decisions.md`).

## 5. Files changed and test result

- Changed: `DESIGN.md` (15.1 row 2, new 15.1a, the 14.3 `stages.jsonl` row, two bullets in 15.2) and `results/owner-decisions.md` (the open bullet for the act bands). Nothing else was edited. Nothing was staged, committed or pushed.
- No test pinned the old text, so no test was changed.
- Test run: `uv run --frozen --project /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel pytest -p no:cacheprovider .../20261114-sweep-sheet/tests -q -m 'not freeze'` -> exit status 0; last line `749 passed, 4 deselected in 219.26s (0:03:39)`.

## 6. How the debate was run, and its limits

- Advocates: Haiku (V1, defend), Sonnet (V2, attack), Sonnet (V3, alternative); one Sonnet fault-finder for Round 2.5. No Opus. Depth standard (Round 1, Round 2, Round 2.5).
- The orchestrator and merge were done by the main Sonnet session, not by the `debate-orchestrator` and `merge-executor` agents; scoring was condensed (no 30-criterion dual-pass), because a dual pass by the same session would not be independent. Return contract status: partial.
- The BD-3 fix and the probe-driven additions were not re-debated (no Round 3 at standard depth).
- No `ground-truth*.json` or score file was opened by this session; advocates and the fault-finder were told not to, and the modified-file check found no edit outside the output folder by them.
- Artifacts: `adversarial/` (variants, `diff-analysis.md`, `debate/`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`, `work/`).
