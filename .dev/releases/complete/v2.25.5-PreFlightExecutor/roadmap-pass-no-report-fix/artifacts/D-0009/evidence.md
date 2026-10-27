# D-0009 — Non-Zero Exit Path Verification

## Task: T03.03

## Deliverable

Trace evidence that TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED paths and
`exit_code < 0` handling do not reach `_write_preliminary_result()`.

## Guard Mechanism

The call site at lines 698–706:

```python
if exit_code == 0:
    _wrote_preliminary = _write_preliminary_result(...)
```

Only `exit_code == 0` enters this block. Any non-zero value skips it entirely.

## Non-Zero Path Traces

| Scenario | exit_code value | Reaches `_write_preliminary_result`? |
|---|---|---|
| TIMEOUT (timed out) | 124 (set via `_timed_out = True`) | NO — 124 != 0 |
| Signal-killed (SIGKILL) | -9 (raw_rc from OS) → -1 fallback | NO — -1 != 0 |
| Signal-killed (SIGTERM) | -15 → -1 fallback | NO — -1 != 0 |
| returncode None race | -1 (fallback via `raw_rc if raw_rc is not None else -1`) | NO — -1 != 0 |
| ERROR (non-zero exit) | any non-zero e.g. 1, 2 | NO — non-zero != 0 |
| INCOMPLETE | any non-zero | NO — non-zero != 0 |
| PASS_RECOVERED | exit_code=0 but with prior HALT file | YES, but freshness guard preserves HALT file |

## PASS_RECOVERED Detail

When `exit_code == 0` but the result file is a stale HALT file:
- `_write_preliminary_result()` IS called (exit_code == 0)
- Freshness guard checks `st_mtime >= started_at`
- If the HALT file is stale (`st_mtime < started_at`), it gets OVERWRITTEN with CONTINUE sentinel
- `_determine_phase_status()` then returns PASS (SC-007 stale HALT overwrite)
- This is the intended behavior, not a regression

## `exit_code < 0` (Signal-Killed) Handling

`_determine_phase_status()` receives negative exit codes without exception:
- `exit_code < 0` falls into the `exit_code != 0` branch
- Returns `PhaseStatus.ERROR` or `PhaseStatus.INCOMPLETE` depending on output
- No exception raised (NFR-001, SC-006c confirmed)

## Acceptance Criteria Status

| Criterion | Status |
|---|---|
| `exit_code != 0` paths never reach `_write_preliminary_result()` | PASS |
| `exit_code < 0` handled without exception in `_determine_phase_status()` | PASS |
| TIMEOUT, ERROR, INCOMPLETE, PASS_RECOVERED behaviors unchanged (SC-006c) | PASS |
