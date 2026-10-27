# D-0020: Run-to-Run Memory (FR-10)

## Overview

Per-finding tracking of `first_seen_run` and `last_seen_run` integers. Prior findings summary via `get_prior_findings_summary()` with max 50 entries, oldest-first truncation.

## Implementation

### Finding Lifecycle
- `first_seen_run`: set on creation in `merge_findings()`, never updated
- `last_seen_run`: updated on every run where finding is present
- Fixed findings retain their `first_seen_run` for historical tracking

### Prior Findings Summary
- `get_prior_findings_summary(max_entries=50)` returns markdown table
- Sorted by `first_seen_run` (oldest first)
- Columns: Stable ID (truncated), Severity, Status, Source Layer, First Seen Run
- Truncation message appended when entries exceed `max_entries`

### Fixed Findings Behavior
- When a previously-FIXED finding reappears, it reactivates (status -> ACTIVE) using the same stable ID
- No duplicate entries created; `first_seen_run` preserved from original detection

## Verification

```
uv run pytest tests/roadmap/test_convergence.py -v -k "memory or prior_findings"
```

Tests: `TestRunToRunMemory` (4 tests) all PASS.
