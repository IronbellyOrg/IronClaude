# Variant 3 (sonnet, architect): act bands

## 1 Verdict

**FAIL, narrowly.** The eight numbers can stay, but row 2 registers them without the quantity, rule or consequence, so a band can later be compared with data in two incompatible ways (F3, F4), whichever suits.

## 2 The best alternative

- **Numerator:** `stages.jsonl` rows with `act` true (supported PROBLEM on a selected item covering the planted item; `analyze.py:894-896,934-943`).
- **Denominator:** rows of the same class with `selection` true, no fallback.
- **Arm:** SS only. The numbers come from the SS table MR 3.1(d). RL has its own lower ranges (MR 3.2(d)); Z0, K, Zh have no sheet and a different act (`analyze.py:897-909`). No band for them.
- **Material:** Stage 1 HO-1 to HO-4 and Stage 2 planted, reported separately, never pooled. Derivation set excluded.
- **Rule:** per class, 95% Wilson interval (`WILSON_Z` 1.96) against the band: below, above, or not contradicted (any overlap).
- **Not evaluable:** fewer than 10 selected item-runs, or fewer than 3 distinct items.
- **May:** one report sentence per flagged class; the measured rate replaces the planning value (MR 5.8, last row); if C4 or C8 is "below", drop the REQ-45 "consistency expected" wording for it.
- **May not:** change D1-D7 or G0, disqualify or re-run an arm, change the 5.8 action, move a band, pool classes.

## 3 Why it beats the alternatives

Computed in `work/v3_rule_sim.py` (output `v3_rule_sim.out`; exact binomial, independent trials, so clustering is ignored).

- **Default plus a point rule "observed rate inside band":** all eight inside at n=18 only 9% of the time even if every midpoint is true (F9); C3 at n=5 has no allowed outcome. My interval rule flags a correct class at most 0.9% (C3, n=10); P(no class flagged) is 0.976 at n=10, 0.986 at n=18.
- **Quantity mismatch:** stage rows are unconditional on selection; the planning act is conditional (MR 3.1(d), 3.0.8). If the model is exactly right, the unconditional expectation (act mid x s mid) is 0.034 for C3, 0.131 for C7, 0.179 for C2; the chance of landing inside the band at n=10 is then 0.25, 0.35, 0.54.
- **Pooled-only band 0.223-0.456:** depends on the hold-out class mix, which is unregistered and not knowable here. Class-mid average: 0.339 even mix, 0.462 C4-heavy, 0.172 C1/C3/C6 only. A correct model can sit outside purely because of the mix. It says nothing about C4, C5, C8, the classes INV-004 names (F7).
- **Z0-anchored band:** Z0 act is a different quantity (no sheet, no selection), does not exist before the first hold-out run, and builds SS-beats-Z0 into the yardstick, which D2 already tests.

## 4 Attack list

- **(a) Unmeasured:** all are priors (F2); a report-only rule avoids the circularity a gate would carry.
- **(b) Width:** widths 0.12-0.30 against sd 0.067-0.118 at n=18 (F9E) ruin a point rule. The interval rule has low power: a band-width miss on the high side is caught 35-83% at n=18; a low-side miss is never caught for C1, C3, C6, even at n=30. Accepted for report-only.
- **(c) Outside:** section 2.
- **(d) Unfair invalidation:** impossible by construction; no gate reads a band (F6), and the text now says so.
- **(e) Few items:** minimum trials. Planted: 18 item-runs times mid s gives about 16 (C4), 14 (C5), 16 (C8), 7-10 others; so likely only C4, C5, C8 are evaluable there. Stated before the run (planning values).
- **(f) Pooled or Z0-anchored:** section 3.

## 5 Replacement text for DESIGN.md 15.1 row 2

| 2 | Per-class act-rate bands (REQ-41), report-only planning priors, none a result; SS arm only. C1 0.10-0.40, C2 0.20-0.45, C3 0.03-0.15, C4 0.50-0.75, C5 0.35-0.60, C6 0.05-0.30, C7 0.15-0.35, C8 0.40-0.65. Measure: among `stages.jsonl` rows of the class with `selection` true (no fallback), the share with `act` true; Stage 1 HO-1 to HO-4 and Stage 2 planted reported separately. Rule: 95% Wilson interval against the band gives below, above or not contradicted; not evaluable under 10 selected item-runs or 3 distinct items. Merge survival is not counted. Outside a band the report may add one sentence, replace the planning value with the measured rate, and drop the REQ-45 "consistency expected" wording for C4 or C8 if below. It may not change D1-D7, G0, any arm, the 5.8 action or a band, or pool classes. RL, K, Z0, Zh: no band. | as listed |

Copy the same text under decision 2 in `results/owner-decisions.md`.

## 6 Non-blocking notes and unverified

- No code does this. `class_reach` counts judge credit, not act; nothing reads `ACT_BANDS` beyond `prereg` (F6). A small script over `stages.jsonl` or hand counting is needed; it cannot be added under this decision's file limits. The registration is valid without it.
- UNVERIFIED: hold-out class mix, so how many classes are evaluable in Stage 1.
- Item-runs on one item are correlated, so real false alarms exceed my figures.
- Selection factors are planning values; my z is 1.96, F9's 1.645.
