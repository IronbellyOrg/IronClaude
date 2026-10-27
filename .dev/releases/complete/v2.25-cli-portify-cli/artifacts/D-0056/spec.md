---
deliverable_id: D-0056
task_id: T09.03
roadmap_item: R-060
status: complete
---

# D-0056 — Failure Diagnostics Collection

## Summary

`diagnostics.py` created at `src/superclaude/cli/cli_portify/diagnostics.py` implementing FR-042.

## Deliverables Produced

- `src/superclaude/cli/cli_portify/diagnostics.py` — `DiagnosticsBundle`, `DiagnosticsCollector`

## API

### DiagnosticsBundle (dataclass)

| Field | Type | Description |
|-------|------|-------------|
| `step_id` | `str` | Step where failure occurred |
| `gate_failures` | `list[GateFailure]` | Structured gate failure records |
| `exit_code` | `Optional[int]` | Process exit code |
| `missing_artifacts` | `list[str]` | Missing artifact paths |
| `resume_guidance` | `str` | Human-readable resume command |

### DiagnosticsCollector

| Method | Signature | Purpose |
|--------|-----------|---------|
| `record_gate_failure()` | `(GateFailure) -> None` | Record a gate failure |
| `record_exit_code()` | `(int) -> None` | Record exit code |
| `record_missing_artifact()` | `(str) -> None` | Record missing artifact |
| `set_resume_guidance()` | `(str) -> None` | Set resume guidance |
| `build_bundle()` | `(step_id) -> DiagnosticsBundle` | Construct bundle |
| `emit_diagnostics()` | `(workdir, step_id) -> Path` | Write diagnostics.md |

## Acceptance Criteria — All Met

- `uv run pytest tests/cli_portify/ -k "diagnostics_collector"` — 8 tests pass
- `uv run pytest tests/cli_portify/ -k "diagnostics_emit"` — 8 tests pass
- `DiagnosticsBundle` contains all 5 required fields
- `emit_diagnostics()` writes `diagnostics.md` with all collected fields
- Gate failure from G-003 shows missing section name in diagnostic message
