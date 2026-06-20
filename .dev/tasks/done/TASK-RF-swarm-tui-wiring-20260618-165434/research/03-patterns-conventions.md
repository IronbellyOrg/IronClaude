# Research: Patterns & Conventions

**Status:** Complete
**Date:** 2026-06-18

**Scope:** Code-style idioms the `--tui` wiring must match so it reads like the surrounding code. All paths absolute. Every claim cites file:LINE.

---

## 1. Click `is_flag` option idiom (template for `--tui`)

The exact shape `--tui` must copy is the existing `--detached` / `--force-relens` flags on `run_cmd`. All boolean flags in this module use the **3-arg decorator form** (`"--name"`, `"dest"`, `is_flag=True`) + `default=False` + a multi-line parenthesized `help=(...)` string that opens with a `T07.xx / FR-xxx --` task tag.

`/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:1452-1469` (`--detached`, the closest analogue — also lives in the FR-014 detached family):

```python
@click.option(
    "--detached",
    "detached",
    is_flag=True,
    default=False,
    help=(
        "T07.11 / FR-014 -- launch the run inside a detached tmux "
        ...
    ),
)
```

`/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:1434-1451` (`--force-relens`) is the same shape.

**Dest-naming convention:** dest string == flag name with dashes→underscores, no prefix (`"--force-relens"` → `"force_relens"`, `"--detached"` → `"detached"`). So `--tui` → dest `"tui"`.

**Decorator placement:** the LAST decorator before the function is always `@auto_inject_guard_option` (`commands.py:1470`), and the corresponding param `auto_inject_guard: bool` is the LAST positional in the signature (`commands.py:1485`). A new `--tui` `@click.option` goes in the decorator stack **above** `@auto_inject_guard_option`; its `tui: bool` param goes in the signature **before** `auto_inject_guard` (R1 owns the exact line anchor).

**Signature style:** every param is type-annotated; flags are `bool`, optionals are `Optional[...]` (`commands.py:1471-1486`). Click supplies the value, params are bare annotations (e.g. `detached: bool,` at `commands.py:1484`).

**A precedent flag whose option dest differs from a one-word name is `--stdin` → `"stdin_mode"`** (`commands.py:1310-1316`) — proof the dest is free-form, but the `--detached`/`--force-relens` 1:1 convention is what to follow for `--tui`.

---

## 2. `UsageError` reject idiom + `EXIT_USAGE`

**Constant definition** — `/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:188-190`:

```python
EXIT_OK: int = 0
EXIT_INVALID: int = 1
EXIT_USAGE: int = 2
```

Module-level constants in `commands.py` itself (no import needed — same file). Comment at `commands.py:184-187` explains `2` matches Click's usage-error convention.

**The reject idiom** is uniform across the module: `click.echo("<cmd> <subcmd>: <message>", err=True)` immediately followed by `raise click.exceptions.Exit(EXIT_USAGE)`. The message prefix is the dotted command path so stderr lines are grep-attributable.

**The FR-3 D1 mirror — the verbatim resume+detached mutual-exclusion reject** at `/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:1547-1553`:

```python
        if detached:
            click.echo(
                "swarm run --resume: --resume is mutually exclusive with "
                "--detached (resume orchestrates its own pipeline inline)",
                err=True,
            )
            raise click.exceptions.Exit(EXIT_USAGE)
```

This is the exact pattern a `--tui` mutual-exclusion reject (e.g. `--tui` + `--detached`, or `--tui` + `--resume`) must mirror: prefix `"swarm run --<flag>: "`, a `<flag> is mutually exclusive with <other>` body with a parenthetical reason, `err=True`, then `raise click.exceptions.Exit(EXIT_USAGE)`.

The sibling resume reject (mutual exclusion with SPEC_PATH/--stdin/--lens) at `commands.py:1540-1546` shows the same shape using `any([...])`. The `--force-relens requires --resume` no-op-trap reject (`commands.py:1573-1579`) is the model for "this flag only has meaning in combination X" rejects — relevant if `--tui` is rejected outside inline mode.

---

## 3. Deferred-import idiom (template for `from ...tui import TUI, should_enable_tui`)

`run_cmd` defers heavy imports to **inside the function body**, with a comment citing module-load-surface + circular-import avoidance. The canonical block is `/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:1522-1527`:

```python
    # Imports are deferred so the module load surface stays light and
    # circular-import-free; preflight + dispatch both pull in many
    # downstream pieces (schema, lenses, transports) that are not
    # needed for ``validate`` / ``validate-lenses`` invocations.
    from superclaude.cli.swarm.dispatch import dispatch_wave1
    from superclaude.cli.swarm.preflight import PreflightError, run_preflight
```

Additional in-body deferred imports in the same function confirm "import at point of use, not module top":
- `from superclaude.cli.swarm.logging_ import Logger as _Logger` — `commands.py:1728`
- `from superclaude.cli.swarm.transports.openai_compat import TransportEnvError` — `commands.py:1757`
- `from superclaude.cli.swarm.models import from_dict as _from_dict` — `commands.py:1800`
- `from superclaude.cli.swarm.normalize import normalize_wave2` / `from superclaude.cli.swarm.reduce import reduce_wave3` — `commands.py:1828-1829`

**Pattern for the new code:** `from superclaude.cli.swarm.tui import TUI, should_enable_tui` belongs as an in-body deferred import in `run_cmd`, fully-qualified `superclaude.cli.swarm.tui` (matching the module-absolute style above), placed near where the TUI is constructed — NOT at module top. Deferring also keeps Rich off the import path for `validate`/`validate-lenses`.

---

## 4. Threading precedent in repo

Two repeated idioms: a **background-monitor-thread** idiom and a **fan-out-worker-thread + join + result-box** idiom. Both are daemon-thread based. **No non-daemon worker thread exists in the swarm package** — Approach A's threaded dispatch is closest to the `pipeline/executor.py` fan-out pattern.

### 4a. Fan-out worker thread + join() + result-box (the Approach-A dispatch-thread precedent)

`/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py:413-432` — the canonical "spawn thread(s), main coordinates, join()" + **result-box / no-exception-propagation** pattern:

```python
    cancel_event = threading.Event()
    results: list[StepResult | None] = [None] * len(steps)

    def _worker(idx: int, step: Step) -> None:
        ...
        result = _execute_single_step(step, config, run_step, combined_cancel)
        results[idx] = result          # result-box: worker writes its slot
        if result.status != StepStatus.PASS:
            cancel_event.set()

    threads = [
        threading.Thread(target=_worker, args=(i, s), daemon=True)
        for i, s in enumerate(steps)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()                       # main blocks until all workers done
```

Key idioms to copy for the dispatch thread: pre-allocate a result slot (`results = [None] * N` / a 1-element box), the worker writes its slot rather than returning, `join()` rejoins on the main thread. **Defensive None-replacement** afterward (`executor.py:434-449`) handles "thread did not produce a result". Note: this precedent uses `daemon=True` AND `join()` together — daemon is the process-exit safety net, `join()` is the real synchronization.

> **FR-5 OVERRIDE:** the swarm dispatch worker thread MUST be non-daemon (`daemon=False`) with an explicit `join()`. The `pipeline/executor.py:413-432` precedent uses `daemon=True`, but that is a DIFFERENT lifecycle (fire-and-forget pool); do NOT copy its daemon flag here. The result-box/exception-box pattern from that precedent IS reusable; only the daemon flag differs. Per spec FR-5 (`merged-requirements.md:99-105`), the worker is non-daemon precisely so `execution-log.jsonl` is never truncated at interpreter shutdown — a daemon thread can be killed mid-write at process exit. The dispatch thread for `--tui` is `threading.Thread(target=_worker, name="swarm-wave1", daemon=False)` + an explicit `t.join()` after the tail-poller sees terminal state.

For Approach A specifically, the work the dispatch thread wraps is the `dispatch_wave1(...)` call (+ its post-dispatch normalize/reduce pipeline) at `/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:1807-1893`. That whole block currently runs inline on the main thread; Approach A moves it onto a worker thread while the main thread tails `execution-log.jsonl` and drives the TUI. **An exception box is required** — `dispatch_wave1` and the reduce wave can raise `PreflightError`/`Exit`/arbitrary exceptions; the existing inline code lets those propagate to Click. On a worker thread they must be captured into a box and re-raised on the main thread after `join()` so the existing `EXIT_*` semantics survive. (No in-repo swarm exception-box exists; the `results[idx]=result` slot pattern above is the structural model to extend with a `[exc]` box.)

### 4b. Background-monitor-thread idiom (daemon + Event + join(timeout))

`/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py:448-478` and the near-identical `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/monitor.py:61-89` (`OutputMonitor`): a `threading.Event` stop signal, a `daemon=True` named thread, `start()`/`stop()` lifecycle, and `stop()` = `self._stop_event.set()` + `self._thread.join(timeout=2.0)`:

```python
    self._stop_event = threading.Event()
    self._thread: threading.Thread | None = None
    ...
    self._thread = threading.Thread(
        target=self._poll_loop, daemon=True, name="output-monitor",
    )
    self._thread.start()
    ...
    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
```

Poll loop uses `Event.wait(interval)` not `time.sleep` for promptly-cancellable polling (`monitor.py:499-502`):

```python
    def _poll_loop(self):
        while not self._stop_event.is_set():
            self._poll_once()
            self._stop_event.wait(self.poll_interval)
```

**This is the inverse of Approach A's layout** — here the *poller* is the background thread and the work is on the main thread. Approach A flips it: dispatch is the background thread, the poller/TUI is on the main thread (which is the correct topology for FR-1's single-console-writer rule, see §4d). The `Event` + daemon + `join(timeout)` lifecycle is still the idiom to reuse for any helper thread.

### 4c. Lock idioms

`threading.Lock` for serialized appends: `/config/workspace/IronClaude/src/superclaude/cli/swarm/logging_.py:117` (`self._lock = threading.Lock()`), with the rationale at `logging_.py:18-34` (interleaved `write(2)` syscalls corrupt JSONL; GIL does not serialize the kernel write). `threading.RLock` (reentrant) at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:1046` for a guarded method that calls another guarded method. The stub transport uses a `threading.Lock` for round-robin counter safety (`transports/stub.py:114`).

### 4d. "Exactly one thread touches the console" discipline — FR-1 single-writer rule + the #181/#182/#184 crash class

The crash class FR-1's single-writer rule prevents lives in **`/config/workspace/IronClaude/src/superclaude/cli/sprint/tui.py`** (`SprintTUI`). The `Live` is started at `sprint/tui.py:119-128`:

```python
        _redirect = os.environ.get("SUPERCLAUDE_SPRINT_RENDER_DIAG") != "1"
        self._live = Live(
            self._render(),
            console=self.console,
            refresh_per_second=2,
            screen=False,
            redirect_stdout=_redirect,
            redirect_stderr=_redirect,
        )
```

The H-C probe comment at `sprint/tui.py:108-118` names the crash class verbatim: **Rich's default `redirect_stdout/redirect_stderr=True` funnels watchdog `print()`/logger output emitted from OTHER threads into the Live's Console buffer — the suspected cross-thread source of a "Thread-1 NoneType render crash."** Disabling the redirect isolates the refresh thread as the sole writer (but then cross-thread output corrupts the terminal visually). PRs #181/#182 added an opt-in `SUPERCLAUDE_SPRINT_RENDER_DIAG=1` escape hatch + faulthandler; the takeaway for FR-1 is structural: **only one thread may write to the Live/Console.** The sprint architecture lets a background monitor thread feed state while the main/executor thread owns every `Live.update()` — and even that boundary produced the crash because Rich's stdout/stderr redirect smuggles other threads' writes into the buffer.

The defensive `update()` wrapper at `sprint/tui.py:150-172` is the other half of the discipline: render errors are caught, `self._live_failed` latches True, and all future updates are silenced with a single stderr notice — a display glitch must never abort the run. **Approach A's FR-1 rule (main thread is the sole console writer; the dispatch worker thread must never call `click.echo` / touch the TUI) is exactly this discipline applied correctly:** put dispatch (which logs, prints, may emit via transports) on the background thread but route ALL its observable output through the log file, and let the single main-thread poller be the only thing that reads that file and writes the console. The swarm `TUI` already exposes the right single-writer surface (`start`/`update`/`stop`, all main-thread, at `/config/workspace/IronClaude/src/superclaude/cli/swarm/tui.py:218-245`). NOTE: swarm `TUI.start()` (`swarm/tui.py:221-226`) does NOT pass `redirect_stdout/redirect_stderr` (defaults to Rich's `True`), so the same cross-thread-redirect hazard applies — the dispatch thread must not write to the real stdout/stderr while the Live is active, or it will be captured into the Live buffer and can trip the same crash. This is the load-bearing reason FR-1 wants dispatch output to go to the log file only.

---

## 5. Byte-offset / incremental file-tail idiom (read-new-bytes-since-offset + partial-trailing-line)

**Found — strong, duplicated idiom.** The cleanest reference is the `OutputMonitor` pair (`sprint/monitor.py` and the byte-for-byte twin `cleanup_audit/monitor.py`). This is the exact pattern the FR-2 main-thread file-tailing poller should adopt for tailing `execution-log.jsonl`.

**Offset-tracked incremental read** — `/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py:541-550` (identical at `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/monitor.py:134-143`):

```python
    def _read_new_chunk(self, current_size: int) -> str:
        """Read only the bytes added since last poll."""
        try:
            with open(self.output_path, errors="replace") as f:
                f.seek(self._last_read_pos)
                chunk = f.read(current_size - self._last_read_pos)
                self._last_read_pos = current_size
                return chunk
        except (OSError, UnicodeDecodeError):
            return ""
```

**Size-gated poll** (only read when the file grew) — `sprint/monitor.py:504-519`:

```python
        try:
            size = self.output_path.stat().st_size
        except FileNotFoundError:
            return
        ...
        if size > self._last_read_pos:
            chunk = self._read_new_chunk(size)
            if chunk:
                self._process_chunk(chunk, now)
```

**Partial-trailing-line handling** (buffer the last split element across polls) — `/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py:552-563` (twin at `cleanup_audit/monitor.py:145-156`):

```python
    def _process_chunk(self, chunk: str, now: float):
        """Split chunk into lines, parse complete NDJSON lines, buffer partials."""
        # Prepend any leftover partial line from previous poll
        data = self._line_buffer + chunk
        lines = data.split("\n")
        # Last element is either "" (if chunk ended with \n) or a partial line
        self._line_buffer = lines[-1]
        # Process all complete lines (everything except the last split element)
        for line in lines[:-1]:
            line = line.strip()
            if not line:
                continue
            ...
            try:
                event = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                ...
```

State carried across polls: `self._last_read_pos: int = 0` and `self._line_buffer: str = ""` (init at `monitor.py:454-455`; reset on phase change at `monitor.py:491-492`). Per-event JSON parse is wrapped in `try/except (json.JSONDecodeError, ValueError)` so a malformed line never kills the tail.

**For Approach A:** the swarm log is `execution-log.jsonl` (each line is an `EventRecord` JSON, see `commands.py:1733` + the round-trip contract at `logging_.py:36-49`). The poller reads new bytes via `seek(last_pos)` + `read(size-last_pos)`, splits on `\n`, buffers the partial trailing line, parses each complete line, and feeds the resulting `EventRecord`s to `TUI.update(state, events)`. The swarm `TUI` already consumes a list of `EventRecord` via `_project_workers` (`swarm/tui.py:145-189`), so the poller's job is exactly file-tail → `EventRecord` list → `TUI.update`. This idiom is in-repo and proven; **reuse it, do not author fresh.**

---

## 6. `time.sleep` poll-loop + `watch_max_iterations` ceiling (FR-4)

**Found — and it is in `swarm/commands.py` itself, so FR-4 has an exact in-file precedent.** The `swarm status --watch` loop is the template.

**Option definitions** (`--watch` / `--watch-interval` / `--watch-max-iterations`) at `/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:2513-2540`:

```python
@click.option(
    "--watch", "watch", is_flag=True, default=False, help=(...),
)
@click.option(
    "--watch-interval", "watch_interval",
    type=click.FloatRange(min=0.01), default=2.0, show_default=True,
    help="Seconds between polls when --watch is set.",
)
@click.option(
    "--watch-max-iterations", "watch_max_iterations",
    type=click.IntRange(min=1), default=None, ...
)
```

**The poll loop with the iteration ceiling + KeyboardInterrupt** at `/config/workspace/IronClaude/src/superclaude/cli/swarm/commands.py:2583-2613`:

```python
    last_exit_code = EXIT_OK
    iterations = 0
    try:
        while True:
            exit_code, line = _read_status_once(output_path, job_id)
            ...
            if "phase=" + TERMINAL_STATE_VALUE in line:
                break
            iterations += 1
            if watch_max_iterations is not None and iterations >= watch_max_iterations:
                break
            time.sleep(watch_interval)
    except KeyboardInterrupt:
        # Operator-initiated stop is a clean exit ...
        pass
    raise click.exceptions.Exit(last_exit_code)
```

The `swarm logs --watch` loop is the same shape at `commands.py:2802` (`if watch_max_iterations is not None and iterations > watch_max_iterations:`) — note `>` vs `>=` differs between the two; the **status loop's `>=`** is the cleaner ceiling semantic to copy.

Constant: `watch_max_iterations` is a `click.IntRange(min=1)` option defaulting to `None` (unbounded). The help text frames it as "primarily a test-determinism / CI guard." **For FR-4, the TUI poller loop should follow this exact shape:** `iterations` counter, terminal-state break, `if watch_max_iterations is not None and iterations >= watch_max_iterations: break`, `time.sleep(interval)` at loop tail, wrapped in `try/except KeyboardInterrupt: pass`. The poll module `module=time` is already imported in `commands.py` (used at `commands.py:2605`).

---

## 7. `finally:` teardown idiom (idempotent stop on all exit paths)

**Found — two strong references; the cleanup_audit executor is the cleanest direct template for Approach A.**

**Cleanest / simplest** — `/config/workspace/IronClaude/src/superclaude/cli/cleanup_audit/executor.py:69-182`. The `Live` is started OUTSIDE the `try`, the work runs INSIDE, and the `finally` guarantees idempotent stop of TUI + monitor + signal handler:

```python
    tui.start()
    try:
        for step in _build_steps(config):
            ...
            while process.is_running():
                ...
                try:
                    tui.update(step, state)
                except Exception:
                    pass
                time.sleep(0.5)
            ...
    finally:
        tui.stop()
        monitor.stop()
        handler.restore()
```

This is the **exact skeleton for Approach A**: start the swarm `TUI` outside the `try`, spawn the dispatch thread, run the main-thread tail-poller loop inside the `try` (calling `tui.update(...)` each iteration), and in `finally` call `tui.stop()` (idempotent — see swarm `tui.py:230-234`) + `join()` the dispatch thread. `tui.update` is wrapped in `try/except Exception: pass` so a render glitch never aborts the run (matches the sprint `_live_failed` latch in §4d).

**Sprint variant with per-resource exception isolation** — `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2496-2511`:

```python
    finally:
        # Ensure monitor thread and subprocess are cleaned up even on exception.
        try:
            monitor.stop()
        except Exception:
            pass
        if proc_manager is not None:
            try:
                proc_manager.terminate()
            except Exception:
                pass
        try:
            tui.stop()
        except Exception:
            pass
```

When teardown itself may raise (and one failure must not mask another), wrap EACH teardown call in its own `try/except Exception: pass`. Use this hardened form if `tui.stop()` + thread `join()` could each fail independently; use the plain `cleanup_audit` form otherwise.

**Idempotency contract is already satisfied by the swarm TUI**: `swarm/tui.py:230-234` — `stop()` checks `if self._live is not None` and nulls `self._live` after stopping, so a double `stop()` (e.g. clean path + `finally`) is a no-op. KeyboardInterrupt is handled by the FR-4 `try/except KeyboardInterrupt` (§6) wrapping the poll loop, with the `finally` still firing `tui.stop()` on the Ctrl-C path.

---

## Patterns-to-copy summary (keyed to each new code element)

| New code element | Copy from (file:LINE) | One-line rule |
|---|---|---|
| **`--tui` option** | `commands.py:1452-1469` (`--detached`) | 3-arg decorator `("--tui","tui",is_flag=True)`, `default=False`, `T07.xx/FR-xx --` help; place ABOVE `@auto_inject_guard_option` (`:1470`); param `tui: bool` BEFORE `auto_inject_guard` (`:1485`). |
| **`--tui` usage reject** | `commands.py:1547-1553` (resume+detached) | `click.echo("swarm run --tui: <flag> is mutually exclusive with <x> (reason)", err=True)` → `raise click.exceptions.Exit(EXIT_USAGE)`. `EXIT_USAGE` is the in-file const at `:190`. |
| **deferred import** | `commands.py:1522-1527` | In-body `from superclaude.cli.swarm.tui import TUI, should_enable_tui`, fully-qualified, NOT module-top. |
| **dispatch worker thread** | `pipeline/executor.py:413-432` + lifecycle from `monitor.py:467-478` | **`daemon=False`** thread (FR-5 OVERRIDE — NOT `daemon=True` as the precedent uses; non-daemon + explicit `join()` so `execution-log.jsonl` is never truncated at interpreter shutdown) wrapping the `commands.py:1807-1893` dispatch+reduce block; result-box + **add an exception-box** to re-raise on main thread after `join()` (preserves `EXIT_*`). Reuse the precedent's box pattern; only the daemon flag differs. |
| **main-thread tail poller** | `sprint/monitor.py:504-563` (`_poll_once`/`_read_new_chunk`/`_process_chunk`) | `stat().st_size` gate → `seek(last_pos)`+`read(size-last_pos)` → split `\n`, buffer `lines[-1]`, parse `lines[:-1]` as `EventRecord`; feed `TUI.update`. Reuse, do not author fresh. |
| **poll loop + ceiling** | `commands.py:2583-2613` (`status --watch`) | `iterations` counter, terminal break, `if watch_max_iterations is not None and iterations >= watch_max_iterations: break`, `time.sleep(interval)`, in `try/except KeyboardInterrupt: pass`. |
| **`finally:` teardown** | `cleanup_audit/executor.py:69-182` (+ hardened form `sprint/executor.py:2496-2511`) | `tui.start()` outside `try`; poll loop inside; `finally: tui.stop(); thread.join()`. `swarm/tui.py:230-234` already makes `stop()` idempotent. |
| **single-console-writer (FR-1)** | `sprint/tui.py:108-128, 150-172` (crash class #181/#182) | ONLY the main thread touches `Live`/`Console`; dispatch thread routes all output to `execution-log.jsonl`. Rich's default stdout/stderr redirect captures other threads' writes → the Thread-1 NoneType render crash. swarm `TUI.start()` (`:221-226`) does NOT disable that redirect. |

---
