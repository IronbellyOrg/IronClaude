# D-0024: validate_semantic_high() Debate Protocol (FR-4.1)

## Summary

Implemented `validate_semantic_high()` in `semantic_layer.py` — the lightweight adversarial debate protocol for semantic HIGH validation.

## Implementation

- **`validate_semantic_high()`**: Accepts `finding`, `registry`, `output_dir`, and `claude_process_factory` parameter for test injection.
- **Parallel execution**: Prosecutor and defender execute in parallel via `ThreadPoolExecutor(max_workers=2)`.
- **Deterministic judge**: `score_argument()` + `judge_verdict()` — same rubric scores always produce same verdict.
- **Conservative tiebreak**: Margin within ±0.15 always produces `CONFIRM_HIGH`.
- **YAML parse failure**: All rubric scores default to 0 for the failing side.
- **Token budget**: Prompt templates fit within ~3,800 tokens per finding (hard cap: 5,000).

## Protocol Steps (FR-4.1)

1. Build prosecutor + defender prompts from finding context
2. Execute both via ClaudeProcess in parallel (2 LLM calls)
3. Parse YAML responses; default scores to 0 on parse failure
4. Score both via `score_argument()` against 4-criterion rubric
5. Compute verdict via `judge_verdict()`
6. Write debate YAML to `output_dir/debates/{stable_id}/debate.yaml`
7. Call `wire_debate_verdict()` to update registry

## Acceptance Criteria Verification

| Criterion | Status |
|-----------|--------|
| `validate_semantic_high()` exists with `claude_process_factory` param | PASS |
| Parallel execution (2 LLM calls) | PASS |
| Deterministic judge: same scores → same verdict | PASS |
| Conservative tiebreak → CONFIRM_HIGH | PASS |
| YAML parse failure defaults to 0 | PASS |

## Test Evidence

```
uv run pytest tests/roadmap/test_semantic_layer.py -v -k "debate or validate_semantic_high"
```
All debate protocol tests pass.
