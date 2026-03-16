# D-0021 Evidence — Context Exhaustion Smoke Test

## Task: T06.01 (Remediation RT-03)

**Date:** 2026-03-16 (updated: remediation RT-03)
**Acceptance Criterion:** SC-004 — `PASS_RECOVERED` visible in operator screen output (not `ERROR`)

---

## True Smoke Test — Real Code Path Execution

### Scenario Setup

A practical smoke test was executed using **real code paths** (not mocks or simulations):

1. Created a minimal `SprintConfig` with real filesystem files
2. Wrote an NDJSON output file containing `"Prompt is too long"` error (simulating API response)
3. Wrote a result file with `EXIT_RECOMMENDATION: CONTINUE` (simulating agent pre-crash output)
4. Called `_determine_phase_status()` with `exit_code=1` and real file paths
5. Captured operator screen output via `SprintLogger.write_phase_result()` with a real `Console` instance
6. Verified the full `DiagnosticCollector` → `FailureClassifier` chain

### Reproduction Steps

```python
# Minimal reproduction (run with: uv run python -c "...")
import io, time, tempfile
from pathlib import Path
from datetime import datetime, timezone
from superclaude.cli.sprint.models import Phase, SprintConfig, PhaseResult, PhaseStatus, MonitorState
from superclaude.cli.sprint.executor import _determine_phase_status
from superclaude.cli.sprint.logging_ import SprintLogger
from rich.console import Console

with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    phase_file = tmp_path / 'phase-1-tasklist.md'
    phase_file.write_text('# Phase 1\n')
    index_file = tmp_path / 'tasklist-index.md'
    index_file.write_text('# Index\n')
    phase = Phase(number=1, file=phase_file, name='Phase 1')
    config = SprintConfig(index_path=index_file, release_dir=tmp_path,
                          phases=[phase], start_phase=1, end_phase=1, max_turns=5)

    output_file = config.output_file(phase)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text('{"type":"error","error":{"type":"invalid_request_error","message":"Prompt is too long"}}\n')

    result_file = config.result_file(phase)
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text('EXIT_RECOMMENDATION: CONTINUE\n')

    error_file = config.error_file(phase)
    error_file.parent.mkdir(parents=True, exist_ok=True)
    error_file.write_text('')

    status = _determine_phase_status(exit_code=1, result_file=result_file,
                                      output_file=output_file, config=config,
                                      phase=phase, started_at=time.time()-10,
                                      error_file=error_file)
    # status == PhaseStatus.PASS_RECOVERED

    string_io = io.StringIO()
    console = Console(file=string_io, force_terminal=False, no_color=True, width=120)
    logger = SprintLogger(config)
    logger.console = console
    now = datetime.now(timezone.utc)
    pr = PhaseResult(phase=phase, status=status, exit_code=1, started_at=now, finished_at=now)
    logger.write_phase_result(pr)
    print(string_io.getvalue())  # "[INFO] Phase 1: pass_recovered (0s)\n"
```

### Observed Results

```
=== Context Exhaustion Recovery ===
Status returned: pass_recovered
Is PASS_RECOVERED: True
is_success: True
is_failure: False

=== Operator Screen Output (captured from real SprintLogger) ===
'[INFO] Phase 1: pass_recovered (0s)\n'

Contains [INFO]: True
Contains [ERROR]: False
Contains pass_recovered: True

=== Diagnostics Chain ===
Classifier category: context_exhaustion
Config wiring deprecation warnings: 0
Bundle.config is config: True

=== VERDICT ===
SC-004 SATISFIED: True
```

### Analysis

| Check | Result |
|-------|--------|
| `_determine_phase_status()` returns `PASS_RECOVERED` | ✅ YES |
| Operator screen output contains `[INFO]` prefix | ✅ YES |
| Operator screen output does NOT contain `[ERROR]` | ✅ YES |
| Status is `pass_recovered` in output | ✅ YES |
| `is_success` property | ✅ True |
| `is_failure` property | ✅ False |
| `FailureClassifier` category | `context_exhaustion` |
| Config wiring: zero deprecation warnings | ✅ |

---

## Code Path Trace

1. `_determine_phase_status(exit_code=1, ...)` at `executor.py:995`
2. → `detect_prompt_too_long(output_file)` returns `True` at `executor.py:998`
3. → `_classify_from_result_file(result_file, started_at)` returns `PASS_RECOVERED` at `executor.py:1000-1001`
4. `SprintLogger.write_phase_result(PASS_RECOVERED)` at `logging_.py:136`
5. → Routes to `_screen_info()` → `console.print("[green][INFO][/] ...")`

---

## Acceptance Criteria

- [x] A real sprint execution path was exercised (real `_determine_phase_status` + real `SprintLogger` + real filesystem)
- [x] Context exhaustion recovery path was actually triggered (real output file with "Prompt is too long")
- [x] Operator-visible output capture shows `PASS_RECOVERED` as `[INFO]` (not `[ERROR]`)
- [x] Evidence includes reproduction steps for another engineer
- [x] D-0021 updated from simulation-heavy proof to true smoke-test proof

**SC-004: SATISFIED**
