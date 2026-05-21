# F-27: Test surface gaps -- `_evaluate_gate` barely exercised, mocks defeat real chain, CLI knobs unverified

**Final severity (Stage 2 preliminary)**: MEDIUM
**Pattern tags**: P6, P9
**Identified by**: F-6, F-8, F-9
**File:line**: `tests/cli/prd/test_integration.py:197-223` (only gate-through-real-chain test); `tests/cli/prd/test_e2e.py:224-253` (mock factory); `tests/cli/prd/test_cli_smoke.py:28-79` (CLI smoke only)

## Evidence

```python
# test_e2e.py:245-250 -- mock writes passing content to stream file, bypassing real chain
def write_output_and_return():
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(output_text, encoding="utf-8")
    return exit_code
mock_proc.wait.side_effect = write_output_and_return
```

## Trace

**Gate chain coverage** (F-6):
- `test_integration.py:197-223` is the ONLY test that calls `_evaluate_gate`. It feeds hand-built content, never the result of `_resolve_step_content`. Every other gate test calls individual `_check_*` predicates standalone.
- The gate's most important data-source dependency ("did this content come from a disk artifact or the NDJSON stream?") is never tested.

**Mock harness** (F-9):
- The mock factory writes pre-cooked passing content directly into the NDJSON stream file path. No mock simulates a subprocess writing via the Write tool to a different path while emitting only commentary on stdout.
- `_resolve_step_content`'s most interesting branch (search for disk artifact, fall back to stream) never gets exercised.

**CLI knobs** (F-8):
- `--tier` end-to-end: checks string presence in output, not that heavyweight gate thresholds are applied.
- `--max-turns`: asserts halt occurs, not that specific budget allocation matched.
- `--where`: no test references this flag with content assertions.
- `--output`: confirms default path only, not that artifacts land at user-supplied location.

## Reproduction sketch

A two-actor mock that (a) writes "I am done" to the stream file and (b) writes a separate full-content artifact to `task_dir/<resolved-artifact-name>` would have caught Bug 1 the day it was introduced.

## Confidence (aggregated)

0.90 -- Agent F verified the gap by exhaustive survey of all 12 test modules.

## Cross-agent corroboration

- **Agent F** surveyed every test file and identified three systemic gaps: the gate-through-real-chain test surface is a single test, the mock harness conflates stream and disk output, and CLI knobs have no behavioral verification beyond string presence.
