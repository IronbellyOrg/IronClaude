# F-12: Retry only fires on OSError -- post-launch transient failures bypass

**Final severity (Stage 2 preliminary)**: HIGH
**Pattern tags**: P4, P8
**Identified by**: D-5
**File:line**: `src/superclaude/cli/prd/process.py:63-86, 208-219`; `src/superclaude/cli/prd/executor.py:502-509`

## Evidence

```python
# process.py:208-219
for attempt in range(self._max_retries + 1):
    try:
        proc = self.start()
        return proc                       # returns immediately on Popen success
    except OSError as exc:
        last_error = exc
        stderr_text = str(exc)            # OSError repr, NOT child stderr

        if not _is_transient_failure(1, stderr_text):
            raise RuntimeError(...) from exc
```

## Trace

- `subprocess.Popen` raises `OSError` only for kernel-level launch failures (executable not found, permission denied, fork failure). It does NOT raise for cases where the binary started and then died -- including 429s, 503s, rate-limit messages, network errors.
- Those all manifest as `start()` returning normally and then `proc.wait()` yielding a nonzero exit code with the real error in `error_file`.
- Result: `_TRANSIENT_PATTERNS` and `_NON_TRANSIENT_PATTERNS` (process.py:38-60) are effectively dead -- they are only matched against `str(OSError)`, never against actual child stderr.
- The 5s/15s exponential backoff (`_retry_delays`) is unreachable for any practical scenario.
- `_is_transient_failure` has `137` in `_TRANSIENT_EXIT_CODES` (process.py:37), claiming SIGKILL is transient and retryable, but this code is never consulted post-launch.

## Reproduction sketch

Stub `claude` with a script that prints "rate limit exceeded" to stderr and exits 1. Run the pipeline. Observe: zero retries, immediate ERROR halt.

## Confidence (aggregated)

0.92 -- Agent D verified via direct read of Python subprocess semantics and the retry loop logic.

## Cross-agent corroboration

- **Agent D** identified the gap between the intended retry behavior (transient pattern matching) and the actual behavior (only OSError on launch), noting that 99% of real transient failures bypass the retry harness entirely.
