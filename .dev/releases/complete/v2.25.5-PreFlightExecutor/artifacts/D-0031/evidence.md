# D-0031 Evidence: SC-002 Nested Claude Without Deadlock

**Task:** T05.03 — Verify SC-002: Nested Claude Without Deadlock
**Date:** 2026-03-16
**Status:** PASS

## SC-002 Requirement
`subprocess.run()` with `capture_output=True` can execute nested `claude --print -p "hello"` without deadlock from pipe buffer exhaustion, with 120s timeout as backstop.

## Pre-conditions
- `claude` binary location: `/config/.local/bin/claude` (confirmed available)
- Execution method: `subprocess.run(['claude', '--print', '-p', 'hello'], capture_output=True, timeout=120)`

## Test Result

| Field | Value |
|---|---|
| Exit code | 0 |
| Duration | 5.941s |
| Stdout length | 33 bytes |
| Stdout content | `Hello! How can I help you today?` |
| Stderr | (empty) |
| Deadlock observed | NO |
| Completed within 120s timeout | YES |

## Acceptance Criteria Verification
- [x] `claude --print -p "hello"` executes successfully via `subprocess.run()` with `capture_output=True`
- [x] Command completes without deadlock within 120s timeout (completed in 5.941s)
- [x] stdout contains a non-empty response (`Hello! How can I help you today?`)
- [x] No pipe buffer exhaustion observed (output is small: 33 bytes)

## Notes
- Output is small (33 bytes), well within pipe buffer limits
- The 120s timeout backstop is available for large output cases per R-061
- `capture_output=True` uses internal pipes which could theoretically deadlock with very large output, but for typical `--print` responses this is not a concern
