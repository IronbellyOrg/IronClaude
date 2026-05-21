# Tier 1 Calibration Report — confidence-calibrator

**Card**: tier1-hypothesis.md
**Card tier**: 1
**Rubric**: refs/escalation-rubric.md
**Flags context**: --type security --scope src/superclaude/cli/eval/ --depth standard (implied)

## Independent re-grading (no anchoring on agent self-score)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| **Evidence grounding** | 1.0 | All cited file:line targets verified by Read against the on-disk fixtures: `commands.py:1472-1477` shows the `output_dir=output_dir` self-reference; `commands.py:815-823` shows doctor's positional-only call; `config.py:219-220` shows the kwarg appending to the allowlist; `config.py:225-229` shows the tautological `resolved == prefix` match. Real code, real lines, exhibits the symptom. |
| **Symptom coverage** | 1.0 | Explains both halves of the reported asymmetry — why doctor rejects (no kwarg, default allowlist) and why eval_run silently accepts (kwarg self-extends the allowlist with the candidate). 100% coverage. |
| **Reproducibility fit** | 1.0 | Symptom is a deterministic input → deterministic output mismatch; the user's report (silently succeeds vs. correctly rejects) IS the reproducer. No flakiness, no env dependence. |
| **Fix directness** | 0.9 | Fix is highly localised (one kwarg removal at commands.py:1476). Slight uncertainty because two competing fix mechanisms exist (remove the kwarg entirely vs. pass a different value like `None` or the already-validated home_root) — needs Tier 2 debate to lock in. |
| **Domain coherence** | 0.5 | Crosses two related-but-distinct domains: **security** (allowlist enforcement / policy bypass) and **API correctness** (misuse of an optional kwarg). Not unrelated, but not single-domain either — exactly the case the rubric scores at 0.5. |

**Calibrated confidence**: (1.0 + 1.0 + 1.0 + 0.9 + 0.5) / 5 = **0.88**

(Agent self-reported 0.92 — slight downward adjustment due to honest Domain coherence scoring; the bug straddles security policy + API misuse.)

## Escalation decision (Wave 2 input)

Apply rubric rules in order:

1. Hard stops: `--no-escalate` not set, `--depth quick` not set → continue.
2. Forced escalation: `--depth deep` not set → continue.
3. Signal-driven escalation:
   - `confidence < 0.85`? **No** (0.88 ≥ 0.85). Does not trigger.
   - Multi-domain (Domain coherence ≤ 0.5)? **YES** (0.5). → ESCALATE `multi_domain`.
   - Intermittent? No.
   - Reproducibility 0.0? No.
   - `--type security` AND confidence < 0.95? **YES** (0.88 < 0.95). → ESCALATE `security_caution`.

**Two triggers fire.** First matching rule wins per rubric ordering: `multi_domain` fires first in the list, but both apply. Audit recorded `escalation_reason: security_caution + multi_domain`. Either alone is sufficient.

## Verdict

**ESCALATE to Tier 2.** Calibrated confidence 0.88 passes the generic 0.85 bar but the `--type security` floor of 0.95 is unmet and the domain coherence is mixed. The Tier 1 hypothesis is almost certainly correct; Tier 2 exists to harden the *fix mechanism* via security-engineer review, second-opinion grounding, and an adversarial debate between two viable fixes (remove-the-kwarg vs. pass-None-explicitly).
