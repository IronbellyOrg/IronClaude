# D-0025: Debate YAML Output and Registry Wiring

## Summary

Debate output YAML written per finding to `output_dir/debates/{stable_id}/debate.yaml`. Registry updated via `wire_debate_verdict()` after each debate.

## YAML Output Schema

```yaml
finding_stable_id: <16-char hex>
dimension: <dimension name>
description: <finding description>
prosecutor:
  evidence_quality: <0-3>
  impact_specificity: <0-3>
  logical_coherence: <0-3>
  concession_handling: <0-3>
  weighted_score: <0.0-1.0>
defender:
  evidence_quality: <0-3>
  impact_specificity: <0-3>
  logical_coherence: <0-3>
  concession_handling: <0-3>
  weighted_score: <0.0-1.0>
margin: <float>
verdict: <CONFIRM_HIGH|DOWNGRADE_TO_MEDIUM|DOWNGRADE_TO_LOW>
```

## Registry Wiring

- `wire_debate_verdict()` records `debate_verdict` and `debate_transcript` path in registry.
- DOWNGRADE verdicts update the finding's `severity` field.

## Acceptance Criteria Verification

| Criterion | Status |
|-----------|--------|
| Debate YAML written per finding | PASS |
| YAML contains rubric scores, margin, verdict | PASS |
| Registry updated with debate_verdict and transcript path | PASS |
| YAML parse failure defaults scores to 0 | PASS |

## Test Evidence

```
uv run pytest tests/roadmap/test_semantic_layer.py -v -k "debate_output or wire_verdict"
```
All debate output tests pass.
