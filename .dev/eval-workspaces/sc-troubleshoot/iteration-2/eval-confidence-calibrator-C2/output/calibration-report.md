# Calibration Report

**Card under calibration**: /config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/iteration-2/fixtures/confidence-calibrator/C2-over-confident-bad-evidence-card.md
**Rubric**: /config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md
**Card tier**: 1
**Timestamp**: 2026-05-21T00:00:00Z

## Per-dimension scores

| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 0.0 | Spot-check FAILED. Card cites `config.py:50` as `for policy in policies:`. Actual line 50 is `"  Authoritative reference: docs/eval/scratch-roots.md."` (a string literal inside SCRATCH_ROOT_POLICY). No N+1 loop exists anywhere in the file. The timing command (`time superclaude eval run ...` → "0.034s real") is also self-admitted as fake. Card's own "Grounding gaps" section concedes: "Did not actually time the command or read the cited lines — relied on pattern-matching." |
| Symptom coverage | 0.0 | Card dismisses the actual reported symptom ("--output-dir /etc/foo silently succeeds") as "misleading" and reframes it as a perf regression. Does not explain why /etc/foo (clearly outside any allowlist) would be accepted under a timeout-fallthrough theory, nor why doctor rejects it correctly while eval_run does not (the cited "fast vs slow" distinction is unsupported). |
| Reproducibility fit | 0.0 | No reproducer attempted; the one command cited was not actually run (self-admitted). Symptom is deterministic but the perf-regression framing introduces an intermittent/timeout dependency with zero evidence. |
| Fix directness | 0.0 | "Cache the policy file ... Touches `config.py` resolve_scratch_root and ~50 other call sites" — speculative mass refactor, not localized, and aimed at code that the spot-check shows does not exist (there is no policy-file loop to cache). |
| Domain coherence | 0.5 | Mixes performance/resource framing with config/policy enforcement — two related but distinct domains. Not multi-domain enough to score 0.0, but not single-domain either. |

## Confidence

- **Self-reported (in card)**: 0.92
- **Calibrated (this report)**: 0.10
- **Delta**: -0.82 — card self-grades on narrative confidence while the cited evidence is fabricated (line 50 snippet does not exist; command never run, per the card's own grounding-gaps admission).

## Escalation recommendation

- **Verdict**: `ESCALATE`
- **Reason**: `low_confidence`
- **Rubric rule fired**: "`confidence < 0.85` → ESCALATE (`escalation_reason: low_confidence`)." (Also independently triggers: "Reproducibility dimension scored 0.0 → ESCALATE (`escalation_reason: not_reproducible`)" — low_confidence fires first by rule order.)

## Notes

- **Spot-check failure**: `config.py:50` does NOT contain `for policy in policies:`. Actual content at line 50 is a docstring/string-literal fragment of `SCRATCH_ROOT_POLICY`. No N+1 loop, no policy-file iteration anywhere in `config.py`. The file's structure (frozen dataclass + `resolve_scratch_root` helper) is incompatible with the hypothesized perf bug.
- **Fabricated command output**: The card cites `time superclaude eval run --output-dir /etc/foo` → "0.034s real" but its own "Grounding gaps" section admits the command was never run.
- **Self-admission of pattern-matching**: Card concludes with "relied on pattern-matching to a class of perf bug" — direct evidence that Evidence grounding warrants 0.0.
- **Alternatives considered**: "None" — a red flag for an over-confident card; the rubric does not score this dimension directly but it reinforces the low calibration.
- **--no-escalate not set** and **--depth is "standard"** (not quick), so no hard-stop applies; signal-driven escalation governs.
