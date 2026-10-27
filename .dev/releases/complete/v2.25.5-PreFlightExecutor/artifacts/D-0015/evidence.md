# Evidence: D-0015 — execute_preflight_phases()

## Task
T03.01 — Create `preflight.py` with `execute_preflight_phases()`

## Function Signature

```python
def execute_preflight_phases(config: SprintConfig) -> list[PhaseResult]
```

## Location
`src/superclaude/cli/sprint/preflight.py`

## Implementation Details

### Phase Filtering
- Filters `config.active_phases` where `phase.execution_mode == "python"`
- Skips claude-mode and skip-mode phases entirely

### Task Parsing
- Calls `parse_tasklist(phase_content, execution_mode="python")` per phase
- Reads phase file via `phase.file.read_text(encoding="utf-8")`

### Subprocess Execution
- Command tokenized via `shlex.split(task.command)`
- Executed via `subprocess.run(cmd, shell=False, capture_output=True, timeout=120, cwd=config.work_dir)`
- Captures `stdout.decode("utf-8", errors="replace")`, `stderr.decode("utf-8", errors="replace")`, `returncode`
- Wall-clock duration measured via `time.monotonic()`

### Classifier Application
- If `task.classifier` is non-empty: calls `run_classifier(task.classifier, exit_code, stdout, stderr)`
- If `task.classifier` is empty: falls back to `"pass"` for exit_code 0, `"fail"` for non-zero
- Unknown classifier names log WARNING and fall back to exit-code classification

### TimeoutExpired Handling
- `subprocess.TimeoutExpired` caught, sets `exit_code = -1`, `classification = "timeout"`
- Task status → `TaskStatus.FAIL`, `GateOutcome.FAIL`

### PhaseResult Construction
- `PhaseStatus.PREFLIGHT_PASS` when all tasks pass
- `PhaseStatus.HALT` when any task fails or times out
- exit_code: 0 for PREFLIGHT_PASS, 1 for HALT

## Verification

Test command: `uv run pytest tests/sprint/test_preflight.py -v -k "preflight and not evidence"` — 42 passed

Key tests:
- `test_preflight_echo_hello`: echo hello → PREFLIGHT_PASS, exit_code 0
- `test_preflight_exit_code_captured`: false → HALT, exit_code 1
- `test_preflight_timeout`: TimeoutExpired → HALT
- `test_preflight_filters_only_python_mode`: only python phases executed
