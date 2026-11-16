| Status | Result |
|---|---|
| DONE | Verdict: **FAIL**. The eight numbers stay, but the default registered them without a measure, a comparison rule or a consequence. |
| DONE | Refactor applied to `DESIGN.md` and `results/owner-decisions.md` only. Nothing was staged, committed or pushed. |
| NEXT | You confirm or change the new registration text (`DESIGN.md` section 15.1a), and a follow-up adds code and tests for the measure. |

**Debate.** Advocates were Haiku (defend), Sonnet (attack) and Sonnet (alternative design), at standard depth, plus one Sonnet fault-finder. No Opus was used. I did the orchestration and merge myself in this Sonnet session. The Haiku defender moved from PASS to FAIL in Round 2.

**Three blocking defects survived:**
- **Mismatch between band and measurement.** The band is "act given the item is on the sheet, including merge survival". The stage `act` in `analysis/analyze.py` is not conditional on selection and excludes survival (lines 894-896, 910-912). If the model behaves exactly as planned, C2 would measure about 0.18 against a floor of 0.20, and C7 about 0.13 against 0.15.
- **No rule or consequence.** Even if every midpoint is true, all eight classes land inside their bands only 2.6% of the time at 10 item-runs per class and 9.2% at 18. The REQ-45 wording for C4 and C8 has no registered link to the bands.
- **Population not pinned.** Stage 2 also runs SS on the haiku and sonnet panels, but the band is for the primary panel. The fault-finder found this one.

**Your attack questions:**
- **Unmeasured estimates.** True and disclosed, but not blocking.
- **Width.** Not the defect.
- **Invalidating an arm.** No gate or code reads a band, so an outside result cannot invalidate an arm.
- **Pooled band.** Rejected, because it depends on the unknown hold-out class mix.
- **Z0-anchored band.** Rejected, because Z0 act is a different quantity.

**The refactor (`DESIGN.md` 15.1a, written once, with a pointer in `owner-decisions.md`):**
- **Measure:** per class, the share of item-runs where the finding survives merge, among selected item-runs. Primary panel, SS arm only, with stages and sets kept apart.
- **Rule:** 95% Wilson interval, and "not assessable" under 10 item-runs.
- **Consequence:** report-only. A "below" flag on C4 or C8 adds a caveat beside the unchanged REQ-45 sentence.
- **May-not list:** the bands cannot change a gate or arm outcome, move a band, pool classes, or be compared with any other rate.

**Tests.** The sweep-sheet suite exited 0 with `749 passed, 4 deselected in 219.26s (0:03:39)`. No test pinned the old text, so none changed.

**Not built:** no code computes the new measure or flag. `analyze.py`, the tests and `TESTING.md` were outside the files I could edit, so the rule is applied by hand until a follow-up.

**Unverified:** the Round 2.5 fixes were not re-debated, and scoring was condensed, not a full dual-pass. The hold-out class mix is unknown, so some classes may turn out not assessable. The return contract status is `partial`.

**Recommended action:** read `results/debate/1-act-bands/VERDICT.md` and `DESIGN.md` section 15.1a. If you accept the text, record the confirmation and commit id in `results/owner-decisions.md` before the first hold-out run. I cannot do that for you, and the order check does not cover this file. Then open the follow-up for code, tests and an attestation line.
