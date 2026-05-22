# Escalation Rubric

Used in Wave 1.7 (to calibrate the Tier 1 hypothesis confidence) and in Wave 2 (to decide whether to escalate to Tier 2).

## Confidence calibration (Wave 1.7)

The `root-cause-analyst` returns a self-reported confidence. The skill **re-grades** it against this rubric — agent confidence is not trusted directly.

Score each dimension 0.0–1.0 and average.

| Dimension | 1.0 (strong) | 0.5 (partial) | 0.0 (weak) |
|-----------|--------------|---------------|------------|
| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
| **Symptom coverage** | Proposed cause explains 100% of the reported symptoms (stack trace, error message, observed behaviour all addressed) | Explains the main symptom but leaves secondary symptoms unexplained | Only explains part of the symptom |
| **Reproducibility fit** | Reproducer exists and matches the cited cause; OR symptom is a deterministic exception with a clear trigger | Symptom is deterministic but no reproducer attempted in Tier 1 | Symptom is intermittent or environment-dependent |
| **Fix directness** | Proposed fix touches the exact code identified in evidence; small, localised change | Fix is in the right area but requires broader changes | Fix is speculative or requires investigation to specify |
| **Domain coherence** | Single domain (e.g. pure logic bug, pure config issue) | Touches two related domains (e.g. logic + tests) | Spans unrelated domains (e.g. perf + auth) |

**Confidence** = arithmetic mean of the five dimension scores.

Round to two decimals.

## Escalation decision (Wave 2)

After confidence is calibrated, apply these rules **in order**. The first matching rule wins.

1. **Hard stops**
   - `--no-escalate` set → STOP at Tier 1 (regardless of confidence). Note in report that escalation was suppressed.
   - `--depth quick` set → STOP at Tier 1.

2. **Forced escalation**
   - `--depth deep` set → ESCALATE (set `escalation_reason: forced_by_depth_deep`).

3. **Signal-driven escalation** (any one triggers escalation)
   - `confidence < 0.85` → ESCALATE (`escalation_reason: low_confidence`).
   - Multi-domain symptom (dimension score 0.5 or lower on "Domain coherence") → ESCALATE (`escalation_reason: multi_domain`).
   - Symptom described as intermittent / flaky / "only sometimes" → ESCALATE (`escalation_reason: intermittent`).
   - Reproducibility dimension scored 0.0 → ESCALATE (`escalation_reason: not_reproducible`).
   - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`). Security bugs have asymmetric cost-of-being-wrong; raise the bar.

4. **Default**
   - `confidence ≥ 0.85` AND single-domain AND reproducible → STOP at Tier 1.

## Why 0.85?

Below 0.85, the average Tier 1 hypothesis card has at least one dimension scoring 0.5 or lower — meaning at least one piece of the puzzle is inferred rather than evidenced. That's the threshold where a second independent perspective begins to pay back its token cost. Above 0.85, additional hypotheses tend to converge on the same answer (waste).

This number is calibrated, not arbitrary — change it only based on eval data, not intuition.

## What escalation does NOT mean

Escalation does **not** mean the Tier 1 hypothesis was wrong. It means the skill judged that one perspective is insufficient evidence to recommend a fix with confidence. The Tier 1 card is always retained in the report as one of the candidate hypotheses.
