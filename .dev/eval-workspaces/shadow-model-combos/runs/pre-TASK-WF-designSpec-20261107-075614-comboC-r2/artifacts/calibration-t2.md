# Wave 3C: per-card blind calibration (Tier 2)

Calibrator: `confidence-calibrator`, class opus (disjoint set empty: reviewers use sonnet, haiku and opus; fallback is the highest capability class, so `calibrator_diversity: degraded`). One independent instance per card, input = the card only (persona and model headers stripped).

| Card (persona, served model) | Cit. | Cov. | Class. | Risk | Action. | C |
|---|---|---|---|---|---|---|
| reviewer-1 (analyzer, claude-sonnet-5-5) | 0.85 | 0.75 | 0.70 | 0.75 | 0.60 | 0.73 |
| reviewer-2 (qa, claude-haiku-5-5) | 0.88 | 0.80 | 0.72 | 0.75 | 0.55 | 0.74 |
| reviewer-3 (refactorer, claude-opus-5-5) | 0.88 | 0.78 | 0.65 | 0.72 | 0.70 | 0.75 |

Calibrator remarks that matter: reviewer-1 F4 (HOLD after failed engage) is weaker than stated, because a failed engage already halts before any edit (spec 68, 274); reviewer-1 F5 is true only for the tests plan 170-172 do not cover; reviewer-2 F9 (inertness below monitor 3) is largely refuted by plan 73, 166, 172; reviewer-2 F11 is partly refuted by plan 90; reviewer-2 F1 overstates "cannot be written" (the decision could tell the skill to supply the inputs); reviewer-3 F4 depends on whether the existing pins are themselves prefixes.
Per-finding confidences are in `panel/cards/reviewer-N.md` (`calibration: per_finding`).
