# Research: DRIFT-3 + DRIFT-4 — FR-5 "worker crash not masked" edges in the poll loop

**Topic type:** Data Flow Tracer + Integration Points
**Scope:** `src/superclaude/cli/swarm/commands.py:1943-1995`, `src/superclaude/cli/swarm/state.py`
**Status:** Complete
**Date:** 2026-06-19

---

## Poll-loop control flow (CODE-VERIFIED, commands.py:1943-1995)

```python
while True:
    state = read_state(state_output_dir / SWARM_STATE_FILENAME)        # 1944  <-- UNGUARDED
    events, offset = _tail_events(.../EXECUTION_LOG_JSONL_FILENAME, offset)  # 1945  <-- UNGUARDED
    assert threading.get_ident() == main_ident, (...)                  # 1952  (FR-1, outside guard by design)
    try:
        tui_obj.update(state, events)                                  # 1957
    except Exception:                                                  # 1958  render-glitch latch
        pass                                                           # 1962
    if not dispatch_thread.is_alive():
        break
    iterations += 1
    if max_iterations is not None and iterations >= max_iterations:
        break
    time.sleep(_TUI_POLL_INTERVAL_SEC)
except KeyboardInterrupt:
    interrupted = True                                                 # 1975
finally:
    if tui_obj is not None: tui_obj.stop()                            # 1982
    dispatch_thread.join()                                            # 1983
if interrupted:
    raise click.exceptions.Exit(130)                                  # 1984-1986  <-- runs FIRST
if "e" in exc_box:
    raise exc_box["e"]                                                # 1990-1991  <-- runs SECOND
worker_results = result_box["v"]
```

## DRIFT-3 (FR-5, MED) — unguarded readers can bypass the exc_box re-raise

`read_state()` (state.py:~195) raises `json.JSONDecodeError` (corrupt JSON) or `ValueError` (shape-invalid payload, e.g. unknown `state` Literal). `_tail_events` can raise on a malformed line. These calls (1944-1945) are OUTSIDE the `try/except Exception` (which wraps only `tui_obj.update`). The loop's only top-level `except` is `KeyboardInterrupt`.

→ A `ValueError`/`JSONDecodeError` from a reader propagates out of the `while`, runs the `finally` (stop+join), and **bypasses** `if "e" in exc_box: raise exc_box["e"]` — masking a concurrent worker crash behind a state-read error. Mitigated by atomic `write_state` (os.replace) so torn reads are unlikely, but an unexpected `ValueError` is unguarded. Narrow gap in the non-negotiable FR-5 guarantee.

**Fix:** wrap the two reader calls in a defensive guard that catches the expected reader exceptions and **continues** the loop (a transient/torn read is not a worker crash; keep last-good `state`/`events`). MUST stay scoped to `Exception` (or the specific `(ValueError, OSError)` reader set) so `KeyboardInterrupt` (BaseException) still propagates to FR-6. Suggested:

```python
try:
    state = read_state(state_output_dir / SWARM_STATE_FILENAME)
    events, offset = _tail_events(.../EXECUTION_LOG_JSONL_FILENAME, offset)
except Exception:
    # FR-5: a transient/torn reader error must NOT bypass the post-loop
    # exc_box re-raise. Keep the last good snapshot and re-poll; the loop
    # still exits via dispatch_thread.is_alive() and surfaces exc_box['e'].
    state, events = _last_state, _last_events   # or leave prior values bound
    continue   # (only after seeding last-good defaults so the first iter is safe)
```
The executor must pick a concrete shape (continue with last-good, or catch+log+continue) that guarantees the loop still terminates on worker death AND reaches the exc_box re-raise.

## DRIFT-4 (FR-5, MED) — exception precedence inversion masks a worker crash on SIGINT

`if interrupted: raise Exit(130)` (1984-1986) runs BEFORE `if "e" in exc_box: raise exc_box["e"]` (1990-1991). If a SIGINT arrives concurrently with a real worker crash, the run exits 130 ("clean interrupted") and **silently discards** `exc_box["e"]` — the literal FR-5 masking failure mode ("a worker crash MUST NOT be hidden"). Edge: requires concurrent SIGINT + crash; untested (the FR-6 SIGINT test injects no concurrent worker exception).

**Fix (preferred):** a worker crash dominates a concurrent interrupt — check `exc_box` first:

```python
if "e" in exc_box:
    raise exc_box["e"]        # FR-5 non-negotiable: never mask a worker crash
if interrupted:
    raise click.exceptions.Exit(130)
```
Alternatively chain (`raise exc_box["e"] from KeyboardInterrupt()`); preserve the ORIGINAL worker traceback either way. The executor must keep FR-6 intact (stop()+join() already ran in `finally`).

## Regression tests required (see research/03)
- DRIFT-3: inject a `read_state` that raises `ValueError` once while `exc_box` holds a worker exception → assert the worker exception (not the ValueError, not a clean exit) reaches the caller.
- DRIFT-4: set `interrupted=True` AND seed `exc_box["e"]` → assert the worker exception is raised/surfaced, not a bare `Exit(130)`.
