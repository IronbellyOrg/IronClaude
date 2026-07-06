# Research: Source Fix Points (M1/M2/M3)

**Status: Complete**
**Date: 2026-06-04**
**Researcher topic:** File Inventory + Patterns & Conventions — exact source fix points
**Scope:** `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/handoff.py`, `src/superclaude/cli/pipeline/process.py`

All citations verified by reading files at HEAD on branch `SprintCLIWireDead`.

---

## Quick contract facts (shared, verified)

These base-class facts from `src/superclaude/cli/pipeline/process.py` underpin all three fixes:

- `ClaudeProcess.start()` (process.py:114-157) opens `self._stdout_fh` (process.py:120 or :122) and `self._stderr_fh` (process.py:123). These are plain `open()` file objects (initialized to `None` in `__init__`, process.py:70-71).
- `_close_handles()` (process.py:238-244) closes both `_stdout_fh`/`_stderr_fh`, each guarded `if fh is not None` and wrapped in `try/except Exception: pass`. **Idempotent and safe to call multiple times** — a closed file's `.close()` is a no-op; a `None` handle is skipped.
- `wait()` (process.py:159-171) is the ONLY happy-path caller of `_close_handles()` — it calls it at process.py:170 after the process exits (or after `terminate()` on `TimeoutExpired`). `wait()` bounds the child with `self._process.wait(timeout=self.timeout_seconds)` (process.py:162); on `TimeoutExpired` it calls `self.terminate()` and returns `124` (process.py:163-165).
- `terminate()` (process.py:173-214): on entry, if `self._process is None or self._process.poll() is not None` (i.e. already-exited child), it **calls `_close_handles()` and returns immediately** (process.py:175-177). Otherwise it does SIGTERM → wait 10s → SIGKILL, then `_close_handles()` at process.py:214. **So `terminate()` is safe to call when the process has already exited — it just closes handles and returns.**

**Conclusion on M1's cleanup question:** Both `proc.terminate()` and `proc._close_handles()` are safe on an already-exited child. `terminate()` is the review's recommendation and is correct; `_close_handles()` is the more minimal/direct option (it does nothing but close FDs, no signal logic). Either is safe. See M1 below for the recommended shape.

---

## M1 — Subprocess file handles leak when an exception interrupts the per-task wait

### (a) Exact current code — `executor.py:1493-1520` (inside `_run_task_subprocess`, def at executor.py:1468)

```python
proc = ClaudeProcess.__new__(ClaudeProcess)                 # 1493
proc.config = config                                        # 1494
proc.phase = phase                                          # 1495
from superclaude.cli.pipeline.process import ClaudeProcess as _Base   # 1496

_Base.__init__(                                             # 1498
    proc,
    prompt=prompt,
    output_file=config.task_output_file(phase, task),
    error_file=config.task_error_file(phase, task),
    max_turns=config.max_turns,
    model=config.model,
    permission_flag=config.permission_flag,
    timeout_seconds=config.max_turns * 120 + 300,
    output_format="stream-json",
    env_vars=_task_env(task, config, phase),
)
proc.start()                                                # 1514  ← opens _stdout_fh/_stderr_fh
_poll_with_stall_watchdog(                                  # 1518  ← may raise; if so, wait() never runs
    proc, config, output_path=config.task_output_file(phase, task)
)
exit_code = proc._process.returncode if proc._process else -1   # 1521
output_path = config.task_output_file(phase, task)              # 1522
output_bytes = output_path.stat().st_size if output_path.exists() else 0  # 1523
turns = max(count_turns_from_stream_json(output_path), 0)       # 1528
return (exit_code if exit_code is not None else -1, turns, output_bytes)  # 1529
```

Note: `_poll_with_stall_watchdog` itself calls `proc.wait()` internally (executor.py:1425 disabled path, executor.py:1465 main path) — that is the ONLY place `_close_handles()` runs on the happy path. If the watchdog body raises **before** reaching its own `proc.wait()` (e.g. `KeyboardInterrupt` during `time.sleep` at executor.py:1440, or any uncaught error), the handles opened at `start()` leak.

### (b) Minimal fix shape

Wrap `start()` + `_poll_with_stall_watchdog(...)` in a `try/finally` (or `try/except`) so cleanup runs on the exception path. Two equivalent safe options:

- **Option A (review's recommendation):** on exception, call `proc.terminate()` — which kills a still-running child AND closes handles (process.py:175-177 early-return path closes handles even if already exited).
- **Option B (most minimal):** on exception, call `proc._close_handles()` directly — closes FDs with no signal logic.

Recommended builder-checklist shape (Option A, since a poll-interrupt may leave a live child that should be reaped):

```python
proc.start()
try:
    _poll_with_stall_watchdog(proc, config, output_path=config.task_output_file(phase, task))
except BaseException:
    proc.terminate()   # closes handles; reaps a still-running child on KeyboardInterrupt
    raise
```

Use `except BaseException` (not `except Exception`) so `KeyboardInterrupt` — explicitly named in the review's "Why this matters" — is also handled. Re-raise to preserve the original failure semantics (the caller still sees the exception; we only added cleanup).

- **No new imports required.** `ClaudeProcess`/`_Base` already imported; `terminate`/`_close_handles` are methods on the constructed `proc`.
- **Placement:** wrap lines 1514+1518-1520. Keep `start()` outside the `try` (if `start()` itself raises before opening both handles, `_close_handles` still tolerates the partially-`None` state, so wrapping `start()` inside the try is also acceptable and slightly more defensive).

### (c) Contract facts that make it safe

- `_close_handles()` is idempotent and exception-swallowing (process.py:238-244) → calling it on the exception path AND having the happy path's `proc.wait()` close again is harmless (double-close is a no-op).
- `terminate()` early-returns + closes handles when `self._process.poll() is not None` (process.py:175-177) → safe even if the child already exited by the time we catch.
- The happy path is unchanged: when the watchdog returns normally, `proc.wait()` already closed handles inside `_poll_with_stall_watchdog`; the new `finally`/`except` only fires on exception.

### (d) Risk / regression to watch

- **Do NOT put `_close_handles()` in an unconditional `finally`** if you also keep the watchdog's internal `proc.wait()` — that's fine (idempotent) but redundant. The cleaner intent is `except BaseException: proc.terminate(); raise` so normal returns are untouched.
- Tests that assert on subprocess teardown (Researcher 2's domain) may need a seam where the poll is forced to raise. The fix must not swallow the exception (re-raise), or callers that depend on the failure propagating (e.g. KeyboardInterrupt aborting the sprint) would regress.
- `proc.terminate()` sends SIGTERM to the process **group** (`os.killpg`, process.py:186) — correct here (it kills the whole child tree), same as the normal `wait()→terminate()` timeout path, so no new behavior.

---

## M2 — Per-task stall watchdog waits unbounded in default `warn` mode

### (a) Exact current code — `executor.py:1422-1465` (inside `_poll_with_stall_watchdog`, def at executor.py:1402)

```python
timeout = getattr(config, "startup_stall_timeout", 0) or 0      # 1422
underlying = getattr(proc, "_process", None)                   # 1423
if underlying is None or timeout <= 0:                         # 1424  ← disabled path
    proc.wait()                                               # 1425
    return                                                    # 1426

def _size() -> int:                                           # 1428
    try:
        if output_path is not None and output_path.exists():
            return output_path.stat().st_size
    except OSError:
        return 0
    return 0

last_size = _size()                                           # 1436
last_progress = time.monotonic()                             # 1437
acted = False                                                 # 1438
while underlying.poll() is None:                             # 1439  ← can spin forever in warn mode
    time.sleep(poll_interval)                               # 1440
    cur = _size()                                          # 1441
    if cur != last_size:                                   # 1442
        last_size = cur
        last_progress = time.monotonic()
        acted = False
    elif not acted and (time.monotonic() - last_progress) > timeout:   # 1446
        acted = True                                       # 1447
        _stall_logger.warning(...)                         # 1448
        if on_stall is not None:                           # 1454
            try: on_stall(proc)
            except Exception: pass
        if getattr(config, "stall_action", "warn") == "kill":   # 1459
            try: underlying.terminate()                    # 1461
            except Exception: pass
            break                                          # 1464  ← ONLY break is kill-mode
proc.wait()                                                 # 1465  ← only reached if loop exits
```

**The unbounded path:** In `warn` mode (default), the `break` at executor.py:1464 is inside the `if ... == "kill":` block only. When a child produces no output AND never exits, the loop warns once (`acted=True`, executor.py:1447), then every subsequent iteration the `elif` at executor.py:1446 is `False` (because `not acted` is now `False`), so the loop just runs `while poll() is None: sleep(0.5)` forever. The bounded `proc.wait()` at executor.py:1465 is never reached.

### (b) Minimal fix shape

Add an **absolute wall-clock ceiling** so the `while` loop is guaranteed to exit in `warn` mode and fall through to the bounded `proc.wait()` at executor.py:1465. Cleanest shape:

1. Capture loop-start monotonic before the loop:
   ```python
   loop_started = time.monotonic()
   ceiling = proc.timeout_seconds   # absolute wall-clock bound on the poll loop
   ```
2. Add the ceiling to the `while` guard (or as a `break` inside):
   ```python
   while underlying.poll() is None and (time.monotonic() - loop_started) < ceiling:
       ...
   proc.wait()   # 1465 — now always reached; bounded by proc.timeout_seconds
   ```

When the ceiling trips, the loop exits with the child still running, control reaches `proc.wait()` (executor.py:1465). `proc.wait()` then bounds the wait by `self.timeout_seconds` (process.py:162) and on `TimeoutExpired` calls `terminate()` and returns 124 (process.py:163-165) → the child IS killed and handles ARE closed. So adding the ceiling restores liveness without changing kill-mode (kill mode still `break`s at executor.py:1464 exactly as before).

### Ceiling source — verified recommendation

Use **`proc.timeout_seconds`** (NOT a multiple of `startup_stall_timeout`, NOT a separate config field):

- `_run_task_subprocess` constructs the proc with `timeout_seconds=config.max_turns * 120 + 300` (executor.py:1506). That is the per-task wall-clock budget already chosen by this code path.
- `proc.wait()` already enforces exactly this value via `self._process.wait(timeout=self.timeout_seconds)` (process.py:162). So bounding the poll loop by the SAME `proc.timeout_seconds` makes the total wait coherent: "watch for stalls, but never spin past the task's own timeout budget; then hand to the bounded wait."
- `proc.timeout_seconds` is a public attribute set in `_Base.__init__` (process.py:61, assigned from the `timeout_seconds=` kwarg). Reachable as `getattr(proc, "timeout_seconds", <fallback>)` for the watchdog's generic `proc` (the watchdog is also called from elsewhere; use `getattr` with a sane fallback to stay duck-typed like the existing `getattr(proc, "_process", None)` at executor.py:1423).

Note: `config.timeout_seconds` is NOT the right source — `SprintConfig` carries `max_turns`/`startup_stall_timeout`/`stall_action` (models.py:544-545 per the review), and the per-task budget actually used is the derived `config.max_turns * 120 + 300` already passed as `proc.timeout_seconds`. Prefer the value already on the proc to avoid recomputing/diverging.

### (b-alt) Builder note: the slightly larger but also-acceptable alternative

The review's second option — "always `terminate()` after the stall warning regardless of `stall_action`" — would change `warn` semantics (warn would now also kill). The ceiling approach is preferred because it preserves `warn` = "log loudly, keep watching up to the task budget, then bound the wait" without converting warn into kill. Recommend the ceiling shape.

### (c) Contract facts that make it safe

- `proc.wait()` is bounded (process.py:162) and self-cleans on timeout (process.py:163-165, 170) → once the loop exits, liveness + handle cleanup are guaranteed.
- kill-mode path (`underlying.terminate(); break` at executor.py:1461-1464) is untouched → no kill-mode regression.
- The disabled path (`timeout <= 0` → plain `proc.wait()`, executor.py:1424-1426) is untouched.
- Progress-resetting logic (executor.py:1442-1445) is untouched, so a child that keeps producing output keeps extending — the ceiling only catches the genuinely-wedged "no output AND no exit" case. (Caveat: a child that produces output forever but never exits would still be bounded by the ceiling — that is the intended liveness guarantee and matches `proc.wait()`'s own contract.)

### (d) Risk / regression to watch

- **Existing watchdog tests** (Researcher 2's domain) likely assert the warn-mode loop exits when the child exits, and kill-mode terminates. A `ceiling = proc.timeout_seconds` of `max_turns*120+300` is far larger than any test's fake-stall window, so real tests that drive the child to *exit* are unaffected. But any test that constructs a proc with a tiny `timeout_seconds` and expects the OLD unbounded behavior would now exit early — verify none assert "loops forever."
- Use `getattr(proc, "timeout_seconds", <fallback>)` not `proc.timeout_seconds` directly, because `_poll_with_stall_watchdog` takes a duck-typed `proc` (no type annotation, executor.py:1403) and is documented as shared across call sites; a fallback (e.g. a large constant or `timeout * N`) avoids `AttributeError` if a caller passes a proc without `timeout_seconds`.
- Do not move `proc.wait()` (executor.py:1465) inside the loop or change its call — it must remain the single post-loop bounded wait so handle-close + 124-on-timeout still happen exactly once.

---

## M3 — Corrupted handoff file raises an unhandled exception on resume

### (a) Exact current code — `handoff.py:62-71` (`FileHandoffStore.read`)

```python
def read(self, *, phase, task) -> HandoffRecord | None:        # 62
    """Return the stored ``HandoffRecord`` or typed ``None`` if absent."""
    path = self.config.handoff_file(phase, task)              # 68
    if not path.exists():                                    # 69
        return None                                          # 70
    return HandoffRecord.from_dict(json.loads(path.read_text()))   # 71  ← unwrapped parse
```

`json` is already imported at handoff.py:18. `HandoffRecord` is imported at handoff.py:20.

**Raise analysis (verified):**
- `json.loads(path.read_text())` on truncated/garbled content raises `json.JSONDecodeError`. **`json.JSONDecodeError` is a subclass of `ValueError`** (verified at runtime: `issubclass(json.JSONDecodeError, ValueError) is True`).
- `HandoffRecord.from_dict` (models.py:329-350) uses `data.get(key, default)` for every field and stores raw values — it does **NOT** call `GateOutcome(...)`/`TaskStatus(...)`, so `from_dict` itself does **not** raise `ValueError` on bad enum strings (those are validated lazily later in `is_validated_success`, handoff.py:36-40, which already has its own `try/except ValueError`). However, if `json.loads` returns a non-dict (e.g. a JSON array or scalar from a corrupt file), `from_dict` indexing/`.get` would raise `AttributeError`/`TypeError`. The review's recommended `(json.JSONDecodeError, ValueError)` covers the realistic JSON-corruption case; consider whether to also catch the malformed-but-valid-JSON shape (see risk below).

### (b) Minimal fix shape

Wrap the parse in `try/except` and return `None` on corruption (corrupt == absent):

```python
def read(self, *, phase, task) -> HandoffRecord | None:
    path = self.config.handoff_file(phase, task)
    if not path.exists():
        return None
    try:
        return HandoffRecord.from_dict(json.loads(path.read_text()))
    except (json.JSONDecodeError, ValueError):
        return None
```

- Because `json.JSONDecodeError` subclasses `ValueError`, `except ValueError` alone would cover the JSON case; the review's explicit `(json.JSONDecodeError, ValueError)` is fine and self-documenting. **No new imports** (`json` already at handoff.py:18).
- Optionally update the docstring (handoff.py:63-67) to state that a corrupt/unparseable file also returns `None` (currently it only promises `None` on *absence*).

### (c) Contract facts that make `None` the correct degrade — caller behavior verified

Both resume-skip callers in `executor.py` guard with `if _prior is not None and is_validated_success(_prior):` — so `None` means "no skip → re-run the task," which is exactly the desired degrade for a corrupt record:

- **Parallel `_worker`** — `executor.py:1103` reads `_prior = handoff_store.read(...)`, then `executor.py:1104`: `if _prior is not None and is_validated_success(_prior):` → returns a PASS/skip tuple; otherwise falls through to the budget gate (executor.py:1120) and runs the task. `None` ⇒ task runs.
- **Sequential loop** — `executor.py:1277` reads `_prior = handoff_store.read(...)`, then `executor.py:1278`: `if _prior is not None and is_validated_success(_prior):` → `results.append(...PASS...)` + `continue`; otherwise falls through to the budget gate (executor.py:1300) and runs the task. `None` ⇒ task runs.

Both call sites are themselves gated by `(config.results_dir / "handoff").exists()` (executor.py:1101 / :1275) before calling `read`, so the back-compat "no handoff dir" path is independent of this fix.

### (d) Risk / regression to watch

- **`is_validated_success` already swallows `ValueError`** from a bad `gate_outcome` string (handoff.py:36-40), so the ONLY uncovered raise today is in `read` itself (the `json.loads`). The fix is correctly localized to `read`.
- If a corrupt file is valid JSON but the WRONG SHAPE (e.g. a top-level list), `from_dict` could raise `AttributeError`/`TypeError`, which the `(json.JSONDecodeError, ValueError)` clause does NOT catch. This is an edge beyond the review's stated scope (review names `JSONDecodeError` and "`ValueError` from from_dict / GateOutcome"). Recommend sticking to the review's `(json.JSONDecodeError, ValueError)` to match the finding exactly; if the builder wants belt-and-suspenders, a broader `except (json.JSONDecodeError, ValueError, TypeError, OSError)` would also catch read/shape errors — but that widens scope and should be a deliberate decision, not silent.
- Do not catch a bare `except Exception:` — that would mask programming errors (e.g. a real bug in `from_dict`). Keep the except narrow per the finding.
- Researcher 2 owns the test seam: the regression test will write a truncated/garbled handoff JSON to `config.handoff_file(phase, task)` and assert `read(...) is None` AND that resume re-runs the task rather than aborting.

---

## Summary

| Finding | Fix location | Minimal fix | New imports | Caller/base contract verified |
|---|---|---|---|---|
| **M1** resource-leak | `executor.py:1514-1520` (`_run_task_subprocess`) | Wrap `start()`+poll: `try: _poll_...(...) except BaseException: proc.terminate(); raise` | None | `terminate()`/`_close_handles()` both safe on exited child (process.py:175-177, 238-244); idempotent close |
| **M2** liveness | `executor.py:1436-1465` (`_poll_with_stall_watchdog`) | Add absolute ceiling to `while` guard using `getattr(proc, "timeout_seconds", <fallback>)`; loop falls through to bounded `proc.wait()` (executor.py:1465) | None | `proc.wait()` bounded by `timeout_seconds` + self-cleans on timeout (process.py:162-170); kill-mode `break` untouched (executor.py:1464) |
| **M3** error-handling | `handoff.py:71` (`FileHandoffStore.read`) | Wrap parse in `try/except (json.JSONDecodeError, ValueError): return None` | None (`json` at handoff.py:18) | Both callers gate on `_prior is not None` (executor.py:1104, :1278) → `None` ⇒ re-run; `JSONDecodeError ⊂ ValueError` verified |

**Key cross-cutting facts:**
- `_close_handles()` (process.py:238-244) is idempotent + exception-swallowing → double-close is harmless, making all three fixes' cleanup paths safe.
- `proc.timeout_seconds` is set to `config.max_turns * 120 + 300` (executor.py:1506) and is the value `proc.wait()` already enforces (process.py:162) → it's the natural ceiling source for M2, no new config field needed.
- `HandoffRecord.from_dict` is forward-compatible `data.get(...)` (models.py:329-350) and does NOT itself validate enums, so M3's realistic raise is `json.loads` (a `ValueError` subclass), and `is_validated_success` already handles bad enum strings (handoff.py:36-40).
- All three fixes require **no new imports**.

**Nothing left Unverified.** Every claim above is grounded in a read of the cited file at HEAD plus a runtime confirmation that `json.JSONDecodeError ⊂ ValueError`.
