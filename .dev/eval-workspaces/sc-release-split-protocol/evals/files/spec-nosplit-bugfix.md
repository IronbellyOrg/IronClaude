---
title: "v2.28 — Sprint Executor Timeout & Retry Hardening"
version: "2.28.0"
status: draft
date: 2026-03-16
complexity_class: LOW
domain_distribution:
  backend: 90
  testing: 10
estimated_scope: 150-200 lines production code
priority: P0
---

# v2.28 Release Spec: Sprint Executor Timeout & Retry Hardening

## 1. Executive Summary

The sprint executor's subprocess management has three related bugs that cause phase failures under load. All three share the same root cause: the poll loop treats timeouts as terminal errors instead of retriable conditions. This release fixes all three in a single coordinated change to the poll loop and its error classification.

## 2. Problem Statement

### Bug 1: Subprocess Timeout Kills Phase (P0)

When a Claude subprocess exceeds `max_turns`, the poll loop raises `TimeoutError` which propagates to `execute_sprint()` as a phase failure. But `max_turns` timeout is an expected condition — the agent ran out of turns, not a system error. The phase should transition to `PASS_NO_SIGNAL`, not `FAILED`.

**Evidence**: Sprint log 2026-03-14, phase 3: `TimeoutError: Subprocess exceeded max_turns (51)` → phase marked `FAILED` → sprint aborted. Manual inspection showed all 8 tasks completed successfully before turn limit.

### Bug 2: Transient I/O Errors Not Retried (P0)

The poll loop reads subprocess output via `process.stdout.readline()`. Occasionally on loaded systems, this returns an empty string (not EOF) due to pipe buffer pressure. The current code treats empty reads as "subprocess died" and raises `SubprocessError`. Adding a single retry with 100ms backoff would handle this.

**Evidence**: CI flake rate on `test_sprint_parallel` went from 2% to 18% after infrastructure migration. All failures show the same empty-read → SubprocessError pattern.

### Bug 3: Zombie Process Cleanup Race (P1)

When a phase is cancelled (user Ctrl+C or timeout), `_cleanup_subprocess()` sends SIGTERM but doesn't wait for the process to exit. This leaves zombie processes that hold file locks on result files, causing the next phase to fail with `PermissionError` on Windows or stale reads on Linux.

**Evidence**: 3 user reports of "cannot write phase-N-result.md" errors, all traced to zombie Claude processes from the previous phase.

## 3. Requirements

### R1: Reclassify max_turns timeout (P0)
- `TimeoutError` from max_turns must map to `PASS_NO_SIGNAL`, not `FAILED`
- Add `TimeoutClassification` enum: `SYSTEM_TIMEOUT` (retriable), `TURN_LIMIT` (expected)
- Log the distinction clearly for debugging

### R2: Add transient I/O retry (P0)
- Empty reads from subprocess stdout get 3 retries with 100ms exponential backoff
- After 3 retries, treat as genuine EOF
- Add retry counter to phase metrics for observability

### R3: Fix zombie cleanup (P1)
- `_cleanup_subprocess()` must `process.wait(timeout=5)` after SIGTERM
- If wait times out, escalate to SIGKILL + wait
- On Windows, use `process.terminate()` + `process.wait()`
- Release file locks before next phase starts

### R4: Add regression tests (P1)
- Test: max_turns timeout produces PASS_NO_SIGNAL status
- Test: empty stdout read is retried (mock pipe buffer pressure)
- Test: zombie process is fully cleaned up before next phase
- Test: file locks released after cleanup

## 4. Architecture

All changes are in two files:
- `src/superclaude/cli/sprint/executor.py` — poll loop, cleanup, classification
- `src/superclaude/cli/sprint/models.py` — `TimeoutClassification` enum

No new modules. No interface changes. No database changes.

### Change Map

```
executor.py:
  _poll_subprocess()     ← R1 (timeout classification) + R2 (retry logic)
  _cleanup_subprocess()  ← R3 (wait + escalate)
  execute_phase()        ← R1 (map TURN_LIMIT to PASS_NO_SIGNAL)

models.py:
  + TimeoutClassification enum
```

## 5. Testing Strategy

- Unit tests for each bug fix (4 tests per R4)
- Integration test: full sprint with artificial max_turns limit
- CI flake monitoring: track `test_sprint_parallel` flake rate for 1 week post-deploy

## 6. Rollout

Direct deployment. No shadow mode needed — these are bug fixes with clear before/after behavior. Rollback is revert-to-previous-version.

## 7. Success Criteria

- max_turns timeout produces `PASS_NO_SIGNAL` (not `FAILED`)
- CI flake rate on `test_sprint_parallel` returns to <3%
- Zero zombie processes after sprint cancellation
- No file lock errors between phases
