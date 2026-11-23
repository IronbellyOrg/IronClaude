# Blind calibration of the Tier 1 card (confidence-calibrator, sonnet class)

Calibrated confidence: 0.54 (self-reported 0.78, not used). Escalate: yes.

- Citation grounding 0.55: findings F1 to F6 cite task numbers only; the 23-of-23 coverage claim was hand-checked, not matcher-checked.
- Coverage completeness 0.75.
- Deviation-classification clarity 0.50: only F6 is labelled a deviation.
- Risk surface coverage 0.60: sanitizer safety, the read-only guarantee, spike outcome and STALE/UNKNOWN edges are not discussed in the card.
- Recommendation actionability 0.30: no fixes or owners given.

calibrator_diversity: degraded (the sonnet class is also a reviewer class; all three classes are used by reviewers).
