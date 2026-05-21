# Tier 1 Calibration — confidence-calibrator (independent regrade)

**Card under review**: `tier1-hypothesis.md`
**Rubric**: `refs/escalation-rubric.md`
**Card tier**: 1

## Per-dimension regrade (fresh context, no formation anchoring)

| Dimension | Agent self-score | Calibrator score | Rationale |
|-----------|------------------|------------------|-----------|
| Evidence grounding | 1.0 | 1.0 | Three direct file:line citations to canonical policy doc + code + existing tests. All citations were independently verified by reading the files. |
| Symptom coverage | 1.0 | 0.9 | The hypothesis explains "test fails" cleanly. Has a small wrinkle: it spends a paragraph reasoning about whether doctor actually exits 0 (per user report) or exits 2 (per code), and acknowledges uncertainty. The diagnosis is robust to either reading, but the symptom→code chain isn't 100% tight. Score 0.9. |
| Reproducibility fit | 1.0 | 1.0 | Fully deterministic policy question. Existing positive/negative tests in same file independently verify both branches of the doctor contract. |
| Fix directness | 1.0 | 1.0 | One file, ≤10 lines of test code to delete/rewrite. No production code touched. |
| Domain coherence | 0.5 | 0.5 | Diagnosis spans test-correctness + security-adjacent policy. Agent's self-score is correct. |

**Calibrated confidence** = (1.0 + 0.9 + 1.0 + 1.0 + 0.5) / 5 = **0.88**

(Note: hypothesis card's prose summary at the end claimed 0.92; the calibrator drops it slightly because of the symptom-coverage wrinkle and to compensate for self-grading anchoring. Overall confidence remains above the 0.85 STOP threshold but the multi-domain dimension is decisive for escalation.)

## Escalation rubric application

Applying `refs/escalation-rubric.md` rules in order:

1. **Hard stops**: `--no-escalate` NOT set, `--depth quick` NOT set. Skip.
2. **Forced escalation**: `--depth deep` NOT set. Skip.
3. **Signal-driven escalation** (any one triggers):
   - confidence (0.88) < 0.85? **NO** (0.88 ≥ 0.85).
   - Multi-domain (Domain coherence ≤ 0.5)? **YES** (scored 0.5). → **ESCALATE**, reason: `multi_domain`.
   - Intermittent? No.
   - Reproducibility 0.0? No.
   - --type security + confidence < 0.95? `--type` is `test`, not `security`. But: the *content* of the policy is security-adjacent. This isn't a strict rule-3.5 trigger, but it's a reinforcement signal.

4. **Default**: would have STOPPED at Tier 1 if multi-domain hadn't fired.

## Verdict

**ESCALATE to Tier 2.**
- Primary reason: `multi_domain` (test correctness + security-adjacent policy intent).
- Reinforcement: the *asymmetric cost* of agreeing with a wrong test that polices a security-adjacent allowlist is exactly the case where a second independent perspective pays back its token cost. A Tier 2 fan-out that includes `security-engineer` will independently verify the OPS-002 contract against the code rather than trusting the test's claim.

## Calibrated confidence

**0.88** (down from agent-reported 0.92).

## Calibration output for audit

```yaml
card_path: tier1-hypothesis.md
card_tier: 1
calibrated_confidence: 0.88
agent_self_confidence: 0.92
verdict: escalate
escalation_reason: multi_domain
notes: |
  Hypothesis is well-grounded (policy doc + code + existing tests independently
  verified). Domain coherence is genuinely 0.5 because diagnosis hinges on
  understanding a security-adjacent policy. The asymmetric cost of being wrong
  ("fix the code to make the test pass" would weaken or break OPS-002) is the
  decisive escalation signal even though raw confidence is above 0.85.
```
