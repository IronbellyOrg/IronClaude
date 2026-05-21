# Tier 1 Calibration

**Agent**: confidence-calibrator
**Card under review**: tier1-hypothesis.md
**Rubric**: refs/escalation-rubric.md
**Card tier**: 1
**Mode**: independent re-grade

## Per-dimension re-grade

### Evidence grounding: 1.0

The card cites multiple concrete pieces of evidence from the provided code: the `create_session` docstring stating intent
explicitly, the function signature `create_sessions_async` returning `list[Session]`, the test's own inline comment
acknowledging it was not updated, the commit message, and the spec. Every claim is grounded in a quotable artifact. The
agent's self-score of 1.0 is correct.

Caveat: the citations are to inline-pasted code rather than disk-resident files. For the purpose of this triage that is
acceptable (the user provided the code as authoritative context), but the evidence-validator pass at Wave 5 should note this
as a grounding gap.

### Symptom coverage: 1.0

The hypothesis explains the exact assertion text ("expected 1 session, got 4"). The "got 4" matches the device count (4
devices in the test's `devices` list), which is the deterministic consequence of one-session-per-device. The CI-vs-local
asymmetry is acknowledged but correctly identified as a SECONDARY signal that doesn't change the primary diagnosis. The
agent's self-score of 1.0 holds.

### Reproducibility fit: 0.5 (downgrade from 1.0)

The hypothesis says "the symptom is deterministic" given the new code. That is correct for the test failure itself — 4
devices will deterministically produce 4 sessions. BUT the user reports "fails 4 out of 5 runs in CI" — i.e. it sometimes
passes. That intermittency is NOT explained by the stale-test hypothesis (which would predict 5/5 failures, not 4/5). The
card acknowledges this but does not fully resolve it.

Downgrade rationale: the agent is correct about WHY the test fails when it fails, but the residual 1/5-pass mystery means
the diagnosis is INCOMPLETE on the reproducibility dimension. A second perspective (e.g. on test isolation / DB state
leakage) would be valuable.

### Fix directness: 1.0

The proposed fix is a one-file change to a test file. No production code touched. The change is small and well-specified
(replace one assertion with four). The agent's self-score of 1.0 holds.

### Domain coherence: 1.0

Single domain — test alignment with shipped feature. The DB thread-safety concern is correctly flagged as orthogonal and
out of scope. The agent's self-score of 1.0 holds.

## Calibrated confidence

Arithmetic mean: (1.0 + 1.0 + 0.5 + 1.0 + 1.0) / 5 = **0.90**

## Escalation decision (applying rubric in order)

1. Hard stops: `--no-escalate` not set, `--depth quick` not set → continue.
2. Forced: `--depth deep` not set → continue.
3. Signal-driven:
   - `confidence < 0.85`? 0.90 ≥ 0.85 → does not trigger.
   - Multi-domain (domain coherence ≤ 0.5)? No (1.0) → does not trigger.
   - Intermittent / "passes locally, fails in CI"? **YES — user said "passes locally but fails 4 out of 5 runs in CI"**. This
     triggers `escalation_reason: intermittent`.
4. Default would have been STOP at Tier 1, but rule 3 fired first.

## Verdict

**ESCALATE to Tier 2** with `escalation_reason: intermittent`.

Note: the primary diagnosis (test is stale) is strong and high-confidence. Escalation is NOT because the diagnosis is
suspect — it is because the user's symptom included an intermittency dimension that one hypothesis card cannot fully
address. The Tier 2 fan-out should retain the Tier 1 card as the leading hypothesis and use the additional agents to
either (a) confirm the test-is-stale diagnosis with a second voice, or (b) explain the 1/5-pass mystery as a separate
sub-finding (DB state leakage, fixture isolation, etc.).

This is exactly the case the escalation rubric is designed for: a strong single-domain diagnosis with a residual
intermittency wrinkle.
