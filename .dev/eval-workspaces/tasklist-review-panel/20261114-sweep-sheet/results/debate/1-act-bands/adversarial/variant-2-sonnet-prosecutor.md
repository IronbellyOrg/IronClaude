# Variant 2 (sonnet prosecutor): act bands, DESIGN.md 15.1 row 2

## 1 Verdict

FAIL. The numbers can stay, but the registration as written names the wrong quantity and gives no rule for a result outside a band, so a pre-registered band cannot be checked or acted on without an after-the-fact choice.

## 2 Blocking defects

**B-1. The band and the measured number are different quantities.**
- Claim: the band is act given selection and including merge survival. The measured `act` is not conditional on selection and excludes merge survival.
- Evidence: `MR:539` ("act is the probability that the item is extracted, the model acts on it and the finding survives. s is the selection factor... reach = act x s") and `MR:357` (F3). `analyze.py:894-896` sets `ids` to the selected sheet items covering the item, so an unselected item gives `act = False`. Survival is a separate field at `analyze.py:910-912` (F4). Z0 and K have no sheet, so their `act` is "a finding anchored on the item" (`analyze.py:897-909`).
- Failure scenario: C2 band midpoint 0.325 times the `MR:545` selection midpoint 0.55 predicts a measured act of 0.18, below the band's own floor of 0.20. C7: 0.25 x 0.525 = 0.13, below 0.15. A run in which the model behaves exactly as planned is reported "below band" in 2 of 8 classes. At the low end of the planning values, 8 of 8 are below. At the MR:543-553 selection midpoints, C4 reads 0.55 against a pre-registered 0.50-0.75, which is only barely inside.
- Why blocking: the comparison is misleading (a selection miss reads as an act miss). That is the exact confusion `MR:357` and `MR:662` say the stage split exists to prevent (F5).

**B-2. No consequence is registered, so the band cannot do its stated job.**
- Evidence: INV-004's purpose is "pre-register act-rate tolerances" (F7). REQ-41, REQ-44 and REQ-45 say nothing about a result outside a band. `analyze.py:1072-1103` only checks `0 <= lo < hi <= 1`, and no gate uses a band (F6). `TESTING.md:142-143` tests only the schema.
- Failure scenario: the hold-out run gives C4 act of 0.45 (below 0.50). REQ-45 allows the sentence "consistency expected for I4". Nothing says whether the report keeps it, retracts it or ignores the band. The owner can pick whichever reading suits after seeing the data, which defeats pre-registration.
- Why blocking: an unmeasurable registration. The "nothing consumes it" argument is not a defense. It shows the registration is decorative, while `prereg.json` is stamped "owner values" with `owner_confirmed: true` (`analyze.py:1099-1101`) and gates `open-manual-checks.sh:8,41`.

**B-3. Point bands cannot be tested with the item counts available.**
- Evidence: F8 and F9. Stage 1 has about 36-40 items over 8 classes, so about 5 per class (25 item-runs at 5 runs each, fewer once only selected items count). Stage 2 has 18 item-runs per class, and only for arms that pass in Stage 1 (`MR:1050`).
- Failure scenario (exact binomial, true rate at band midpoint, independent trials, so generous): P(observed rate inside own band) at n=10 is C3 0.39, C7 0.53, C4 0.66. P(all 8 inside) is 0.026 at n=10 and 0.092 at n=18. C3 at n=5 has no allowed value (`band_sim.out` D: allowed k = none). A perfectly calibrated planning table is reported as mostly "outside" by chance. A point-in-band check at an edge value passes only 41-60% at n=18 (F9 B).
- Why blocking: any use of the bands in the report, in the REQ-45 wording, or by the owner will be misleading, and any use against an arm will be unfair to it.

**B-4. The registration does not say which arm or document set it covers.** `MR:539` defines act for the primary panel with H1-H4, which is the SS arm. Z0 and K act is measured differently (F4). DESIGN.md:800 says "per class" only. A Z0 act rate compared with an SS band is a category error. This part is smaller than B-1 to B-3, but the fix is the same sentence.

## 3 Answers to the attack list

(a) The bands are the union of unmeasured planning ranges (F2, `MR:1207`). The only measured count is C8's 7 of 8. Registering them unlabeled implies calibration. Owner decision 1 already carries "an estimate, not a validated figure". Decision 2 has no such label.
(b) Width is not the defect. At n=18 a 0.25-wide band is hit 65-90% of the time at the midpoint. The fault is definition and consequence (B-1, B-2). Widening would hide the problem.
(c) Today nothing happens (F6). That is B-2.
(d) By code, no. By report reading, yes: an interval-free "outside band" label on one class, applied to a weak arm and not to Z0, is an unfair verdict (B-3, B-4).
(e) With about 5 to 25 item-runs per class and run-to-run correlation (F8), only intervals are honest. A class with fewer than 10 selected item-runs cannot be assessed.
(f) A pooled band (0.223-0.456) is checkable at n=40 (0.91 inside at the midpoint, 0.02-0.04 at 0.10 or 0.60), but it erases the class split that INV-004 and REQ-45 depend on. I would keep per-class bands, and add the pooled one as a cross-check only if the owner wants one. A Z0-anchored band would need the Z0 act rate first, which is not measured before the freeze (F10 gives the freeze order).

## 4 Replacement text for DESIGN.md 15.1 row 2

Decision: "Per-class act-rate bands to pre-register (REQ-41). Defaults are the act ranges of `MR` 3.1(d). A band is an expectation for the SS arm, not a gate, and is read as defined below."

Recommended: "C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65. These are estimates, not validated figures."

Rule sentence, added under the table:
"Bands apply to SS only. The measured figure is the share of item-runs with `selection` true and `merge_survival` true whose `act` is true, over item-runs with `selection` true and `merge_survival` not null, with a 90% Wilson interval and n. A class is reported 'inside', 'overlaps' or 'outside' (interval wholly outside the band). A class with n below 10 is 'not assessable'. A result outside a band changes no gate and invalidates no arm. It only removes the matching claim wording: for C4 or C8, REQ-45's 'consistency expected' is dropped, not the arm."

## 5 Non-blocking notes

- `MR:1206` in F2 is `MR:1207` in the file I read.
- C1 and C6 bands are unions of two issues each (B1/B2, B6/B8). That is fine for a planning range.
- INV-004 lists C4, C5, C8, while REQ-45 lists only I4 and I7. That is a wording mismatch, not a defect of the bands.

## 6 What would make me switch to PASS

- DESIGN text, or a `prereg.json` field, that defines the band's measured figure as in B-1 (conditional on selection, with survival), plus one sentence stating that a result outside a band triggers nothing.
- Evidence that the hold-out has at least 10 selected item-runs per class. I would still need the Z0-versus-SS restriction in B-4.
