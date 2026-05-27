# Tier 1 Hypothesis Calibration Report

**Card under review**: `tier1-hypothesis.md`
**Rubric applied**: `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
**Tier**: 1
**Calibrator note**: confidence-calibrator subagent failed to persist its output file; the scores below come from its in-conversation response. Inline fallback per Wave 1.7 failure handling.

## Per-dimension scores

| Dimension | Score | Rationale |
|---|---|---|
| Evidence grounding | 1.0 | All 6 file:line citations independently verified (`structural_checkers.py:380`, `spec_parser.py:329`, `convergence.py:539`, `remediate_executor.py:309-362` w/ threshold at L335, `integration_contracts.py:445`). The TUIBBS `deviation-registry.json` is cited as "per Wave 1 grounding" — honest source attribution. |
| Symptom coverage | 1.0 | Card addresses (a) the 54 HIGH `phantom_id` count, (b) the convergence halt itself, (c) the misleading halt message, (d) the recurrence pattern across releases, (e) the 30% diff guard blocking a correct fix, (f) the Run 2 → Run 3 flatline (roadmap_hash changed but count didn't). Comprehensive. |
| Reproducibility fit | 1.0 | Deterministic; no LLM dependence; `check_signatures` on the TUIBBS pair reproduces it byte-for-byte. |
| Fix directness | 1.0 | Single-module change (`structural_checkers.py`), ~15 LOC, leverages already-merged precedent (`integration_contracts.py:445`), stays well under the per-patch 30% guard, satisfies NFR-4 pure-function contract. |
| Domain coherence | 0.5 | The MEDIUM-demotion sub-fix is a lightweight S6-substitute; touches *two* related domains — comparator semantics (logic) + convergence escape policy (orchestration). Defensible-but-not-unique architectural choice. |

## Aggregate

**Calibrated confidence**: (1.0 + 1.0 + 1.0 + 1.0 + 0.5) / 5 = **0.90**

**Self-reported confidence**: 0.88
**Delta**: +0.02 (card slightly under-reported; honesty intact)

## Escalation verdict

| Rubric trigger | Active? | Effect |
|---|---|---|
| Rule 1 (`confidence < 0.85`) | No (0.90 ≥ 0.85) | Would STOP at Tier 1 |
| Rule 2 (`--depth deep`) | **Yes (forced by user flag)** | **ESCALATE to Tier 2 regardless** |
| Rule 3 (multi-domain symptom) | Borderline (logic + orchestration) | Would weakly favor escalation |
| Rule 4 (intermittent / unclear repro) | No (deterministic) | No effect |
| Rule 5 (security-class) | No | No effect |

**Decision**: ESCALATE — `escalation_reason: forced_by_depth_deep`. Calibrated confidence (0.90) is high; the user's `--depth deep` is the binding constraint, consistent with their stated intent ("maximum specialist diversity, forced Tier 2 + adversarial debate"). Wave 3 will fan out 4 specialists to stress-test the Tier 1 conclusion and surface 2-3 competing structural framings for Wave 4 adversarial debate.
