# F-09: `_handle_shutdown` accesses non-existent `step` attribute on PrdStepResult

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P1, P8
**Identified by**: A-7
**File:line**: `src/superclaude/cli/prd/executor.py:957-970`, `src/superclaude/cli/prd/models.py:220-235`

## Evidence

```python
# executor.py:957-970
def _handle_shutdown(self, result: PrdPipelineResult) -> None:
    ...
    completed = [r for r in self._step_results if r.status.is_terminal]
    if completed:
        last = completed[-1]
        last_step = (
            getattr(last.step, "name", "unknown") if last.step else "unknown"
        )

# models.py:220-234 -- PrdStepResult has NO step field
class PrdStepResult(StepResult):
    exit_code: int = 0
    output_bytes: int = 0
    error_bytes: int = 0
    artifacts_produced: list[str] = field(default_factory=list)
    agent_type: str = ""
    fix_cycle: int = 0
    qa_verdict: Optional[str] = None
```

## Trace

- **Writer**: nothing in the PRD module assigns `step` on a PrdStepResult. The executor never does `step_result.step = ...` anywhere in `_run_subprocess_step` or `_run_check_existing`.
- **Reader**: `_handle_shutdown` accesses `last.step` and `last.step.name`.
- **Outcome A** (if `StepResult` declares `step: Optional[...] = None`): the `if last.step` guard goes false, returns `"unknown"`, masking the real halt step. Resume info is useless.
- **Outcome B** (if `StepResult` lacks `step`): `last.step` raises `AttributeError`, crashing during SIGINT handling. No resume state is written at all.

## Reproduction sketch

`kill -INT $(pgrep -f "superclaude prd run")` during a long pipeline. Either `AttributeError` aborts the shutdown handler (no resume state written) or `halt_step="unknown"` is recorded (resume info useless).

## Confidence (aggregated)

0.85 -- Agent A confirmed the local code is unambiguous. Uncertainty depends on the upstream `StepResult` schema (deferred).

## Cross-agent corroboration

- **Agent A** identified the field mismatch and traced both possible failure outcomes (AttributeError vs. silent "unknown") depending on the parent `StepResult` class definition.
