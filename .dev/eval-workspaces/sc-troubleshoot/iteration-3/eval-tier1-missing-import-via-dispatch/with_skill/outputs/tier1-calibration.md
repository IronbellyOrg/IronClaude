# Tier 1 Confidence Calibration

**Agent**: confidence-calibrator
**Card under review**: `tier1-hypothesis.md`
**Rubric**: `refs/escalation-rubric.md`
**Card tier**: 1
**Flags context**: `--type bug` (auto-detected), `--depth standard`, no `--no-escalate`, no `--fix`

## Dimension scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | **1.0** | Card cites `payments/refund_handler.py:7-11` (imports list) and `:47` (offending statement). Both citations were verifiable in the fixture file via direct Read. The symptom (`NameError: name 'datetime' is not defined`) is the deterministic consequence of the cited code path. |
| Symptom coverage | **1.0** | The hypothesis explains 100% of the symptom: the exact name (`datetime`), the exact line (47), the exact exception class (`NameError`), and the trigger context ("when the worker processes a refund" — i.e. when `process()` reaches the persistence step). Nothing in the user's report is left unexplained. |
| Reproducibility fit | **1.0** | This is a deterministic Python name-resolution failure. Any call to `RefundHandler.process()` that reaches line 47 will raise the same NameError on every invocation, in every environment. No reproducer needed beyond "execute the line"; the trigger is clear. |
| Fix directness | **1.0** | The proposed fix is a single import line at module scope, touching the exact module where the missing name lives. No cross-file changes, no refactor, no test redesign required. The optional `datetime.now(timezone.utc)` modernization is called out separately as a follow-up, not bundled into the minimal fix. |
| Domain coherence | **1.0** | Single domain: Python module-level name resolution. No interaction with concurrency, environment, configuration, state, or external services. |

## Calibrated confidence

`(1.0 + 1.0 + 1.0 + 1.0 + 1.0) / 5 = 1.00`

Rounded to two decimals: **1.00**

(Self-reported was 0.95. The calibrator-side score is fractionally higher because the analyst's risk section acknowledged a hypothetical "second hidden cause" caveat that the rubric does not penalize — the rubric grades evidence and coverage, not the analyst's epistemic modesty.)

## Escalation decision

Walking the rules in order:

1. **Hard stops** — `--no-escalate`? No. `--depth quick`? No. Skip.
2. **Forced escalation** — `--depth deep`? No. Skip.
3. **Signal-driven escalation** —
   - `confidence < 0.85`? No (1.00 ≥ 0.85).
   - Multi-domain (Domain coherence ≤ 0.5)? No (scored 1.0).
   - Intermittent / flaky language? No — the symptom is described as deterministic ("when the worker processes a refund").
   - Reproducibility scored 0.0? No (scored 1.0).
   - `--type security` AND confidence < 0.95? No (`--type bug`).
4. **Default** — confidence ≥ 0.85 AND single-domain AND reproducible → **STOP at Tier 1**.

## Verdict

```
verdict: stop_tier1
calibrated_confidence: 1.00
escalation_reason: none
```

No escalation. Tier 1 is sufficient.
