# D-0012 Evidence: _determine_phase_status() error_file Parameter + execute_sprint() Wiring

## Deliverable
`_determine_phase_status()` in `src/superclaude/cli/sprint/executor.py` accepts `error_file: Path | None = None` keyword-only parameter and forwards it to `detect_prompt_too_long(error_path=error_file)`. The `execute_sprint()` call site passes `config.error_file(phase)`.

## Implementation

### _determine_phase_status() signature change
**File:** `src/superclaude/cli/sprint/executor.py`

Added `error_file: Path | None = None` as keyword-only parameter (after `started_at`):
```python
def _determine_phase_status(
    exit_code: int,
    result_file: Path,
    output_file: Path,
    *,
    config: SprintConfig | None = None,
    phase: Phase | None = None,
    started_at: float = 0.0,
    error_file: Path | None = None,
) -> PhaseStatus:
```

### detect_prompt_too_long() forwarding
```python
if detect_prompt_too_long(output_file, error_path=error_file):
```

### execute_sprint() call site update
```python
status = _determine_phase_status(
    exit_code=exit_code,
    result_file=config.result_file(phase),
    output_file=config.output_file(phase),
    config=config,
    phase=phase,
    started_at=started_at.timestamp(),
    error_file=config.error_file(phase),
)
```

`config.error_file(phase)` resolves to `results_dir / f"phase-{phase.number}-errors.txt"` (already defined in SprintConfig).

## Verification

`uv run pytest tests/sprint/ -v --tb=short` → **629 passed** in 37.22s

## Milestone
M3.3 satisfied.
