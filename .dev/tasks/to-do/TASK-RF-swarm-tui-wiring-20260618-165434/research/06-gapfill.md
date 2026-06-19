# Research: Gap-Fill Round 1

**Status:** In Progress
**Date:** 2026-06-18

---

## Scope

Resolves the six gaps flagged by the research quality gate. Every resolution is
grounded in an actual source read with a `file:line` citation. Project root:
`/config/workspace/IronClaude/`. Spec:
`/config/workspace/IronClaude/.dev/brainstorms/swarm-tui-wiring/merged-requirements.md`.

---

## G1 (CRITICAL) — Dispatch thread is NON-DAEMON (`daemon=False`) + explicit `join()`

**Also corrected in `03-patterns-conventions.md` (Part A).** Stated plainly here:

The swarm dispatch worker thread MUST be:

```python
t = threading.Thread(target=_worker, name="swarm-wave1", daemon=False)
t.start()
# ... main thread runs gated TUI poll loop ...
t.join()   # explicit, mandatory
```

**Why `daemon=False` (not `daemon=True`):** spec **FR-5**, `merged-requirements.md:99-105`
— the spec text reads: *"(Worker thread is **non-daemon** with an explicit `join()` so
`event-log.jsonl` is never truncated at interpreter shutdown.)"* [NOTE: the spec's
`event-log.jsonl` is the stale filename; the real on-disk file is `execution-log.jsonl`
per the [CODE-VERIFIED] resolution in `02-reader-contracts.md` §7.] A daemon thread
can be killed by the interpreter mid-`write(2)` at process exit, truncating the JSONL
log; a non-daemon thread + `join()` guarantees the dispatch completes (and its log
flushes) before the process can exit.

**The `pipeline/executor.py:413-432` precedent uses `daemon=True`** (verified — `executor.py:416`
`threading.Thread(target=_worker, args=(i, s), daemon=True)`). That is a DIFFERENT
lifecycle (a fire-and-forget fan-out pool where daemon is the process-exit safety net).
The **result-box / exception-box** structural pattern from that precedent IS reusable for
the swarm dispatch thread; **only the daemon flag differs** — copy the box, flip the flag
to `False`.

**Source reads:**
- `merged-requirements.md:99-105` (FR-5 — non-daemon mandate + traceback re-raise contract).
- `src/superclaude/cli/pipeline/executor.py:416` (the `daemon=True` precedent that must NOT be copied verbatim).

---

## G2 (IMPORTANT) — `state_output_dir is None` guard: when to spawn the TUI path

**`state_output_dir` is set ONLY when `preflight_result.manifest_path` is truthy** —
i.e. only when an `--output` directory exists. **[CODE-VERIFIED]**

`src/superclaude/cli/swarm/commands.py:1726-1731`:

```python
1726    state_output_dir: Optional[Path] = None
1727    if preflight_result.manifest_path:
1728        from superclaude.cli.swarm.logging_ import Logger as _Logger
1729
1730        manifest_dir = Path(preflight_result.manifest_path).parent
1731        state_output_dir = manifest_dir
```

- `state_output_dir` initializes to `None` at `commands.py:1726`.
- It is assigned `manifest_dir` **only inside** the `if preflight_result.manifest_path:`
  block (`commands.py:1727`, assignment at `:1731`).
- The same gate constructs the `Logger` that writes `execution-log.jsonl`
  (`commands.py:1732-1740`, jsonl path at `:1733`). So **when `state_output_dir is None`,
  there is NO `execution-log.jsonl` and NO `.swarm-state.json` on disk** — the poll loop
  would have nothing to tail and `read_state()` would always return `None`.
- The docstring at `commands.py:1722-1725` confirms: `state_output_dir` is `None` "for the
  spec-only smoke path that runs without a materialised output directory."

**Concrete guard rule (DECISION — simplest correct behavior):**

> The thread+poll TUI path is spawned **only when BOTH** conditions hold:
> `should_enable_tui(tui, sys.stdout)` is `True` **AND** `state_output_dir is not None`.
> Otherwise the existing fully-synchronous `dispatch_wave1(...)` path
> (`commands.py:1807-1813`) runs byte-identically — no thread, no tail loop, no Rich import.

Gating local to test: `state_output_dir` (`commands.py:1726` / assigned `:1731`).

**Why this is the cleaner option (vs. "spawn thread but skip poll loop"):** when
`state_output_dir is None`, even with `--tui` + a TTY, there is no log file and no state
file to render — a TUI would show an empty dashboard forever. Spawning a thread just to
`join()` it with no observable benefit adds a thread-boundary and an exception-box round-trip
for zero gain. Keeping the no-output path on the **existing synchronous call** means it runs
the exact pre-existing code path (`commands.py:1807-1813`) with no new behavior — this is
the byte-identical guarantee **FR-2** (`merged-requirements.md:63-72`) demands: *"no thread
spawned, no tail loop, no Rich import side effects, and the `dispatch_wave1` signature
unchanged."*

**No behavioral regression:** the `--tui`+TTY+`state_output_dir is None` combination is the
only NEW path the guard touches, and it routes to the **unchanged** synchronous call. All
existing invocations (no `--tui`, or non-TTY, or no `--output`) keep hitting
`commands.py:1807` exactly as today. FR-2's "zero ANSI bytes / identical exit code / identical
log output" acceptance holds because nothing new executes on those paths.

**Source reads:**
- `src/superclaude/cli/swarm/commands.py:1721-1749` (state_output_dir None-init + the single `if preflight_result.manifest_path` gate that sets it and the Logger).
- `src/superclaude/cli/swarm/commands.py:1807-1813` (the existing synchronous `dispatch_wave1` call the non-TUI / no-output path must keep using unchanged).
- `merged-requirements.md:63-72` (FR-2 byte-identical no-regression contract).

---

## G3 (IMPORTANT) — SIGINT during `join()` + exit code (FR-6)

**Precedent A — `TUI.stop()` is idempotent** (`src/superclaude/cli/swarm/tui.py:230-234`):

```python
230    def stop(self) -> None:
231        """Stop the Live display. Idempotent."""
232        if self._live is not None:
233            self._live.stop()
234            self._live = None
```

So calling `stop()` in `finally` AND again on a clean path is a safe no-op.

**Precedent B — the existing `swarm status --watch` KeyboardInterrupt handling**
(`src/superclaude/cli/swarm/commands.py:2585-2613`):

```python
2585    try:
2586        while True:
2587            ...
2605            time.sleep(watch_interval)
2606    except KeyboardInterrupt:
2607        # Operator-initiated stop is a clean exit ...
2611        pass
2612
2613    raise click.exceptions.Exit(last_exit_code)
```

That precedent **swallows** SIGINT and exits with the last observed code — appropriate for a
read-only watcher. The TUI run path is NOT read-only (a worker is mutating the filesystem), so
v1 must differ: it should surface interruption as a non-zero exit, not a clean `pass`.

**Concrete v1 pattern:**

```python
tui = None
try:
    t.start()
    if should_enable_tui(tui_flag, sys.stdout) and state_output_dir is not None:
        tui = TUI(); tui.start()
        offset = 0
        while t.is_alive():
            state = read_state(state_output_dir / ".swarm-state.json")
            events, offset = _tail_events(state_output_dir / "execution-log.jsonl", offset)
            tui.update(state, events)
            time.sleep(0.5)
    t.join()
finally:
    if tui is not None:
        tui.stop()        # idempotent (tui.py:230-234); ALWAYS runs
if "e" in exc_box:
    raise exc_box["e"]    # FR-5: re-raise worker exception AFTER stop()
```

**SIGINT decision (v1, precise):**
- A `KeyboardInterrupt` raised during the poll loop or during `t.join()` propagates out of
  the `try`. The `finally: tui.stop()` **always runs first** — the terminal is restored
  before anything else (satisfies **FR-6**, `merged-requirements.md:111-119`: `stop()` runs
  on the SIGINT path).
- After `finally`, the `KeyboardInterrupt` continues to propagate. We do **not** swallow it
  (unlike the `status --watch` precedent) — it must reach Click so the exit code reflects
  interruption.
- **The realistic SIGINT window is the poll loop** (the main thread sleeps 0.5s/iteration).
  Once `t.join()` is reached, the main thread is blocked in `join()`; a SIGINT there also
  raises `KeyboardInterrupt` on the main thread, runs `finally`, and propagates.
- **Out of v1 scope:** fully interrupting an **in-flight non-daemon worker mid-call**. Because
  the worker is `daemon=False` (G1/FR-5), if SIGINT arrives while the worker is still inside
  `dispatch_wave1`, the worker keeps running to completion before the process can actually
  exit (the interpreter waits on non-daemon threads at shutdown). v1 accepts this: the
  `finally: tui.stop()` restores the terminal immediately, the `KeyboardInterrupt` is recorded
  as the exit reason, and the worker drains its log to disk (the FR-5 anti-truncation
  guarantee) rather than being killed mid-write. Cancelling the worker mid-call would require a
  cooperative cancel token through `dispatch_wave1`/`ParallelExecutor` — explicitly frozen
  (AC-004/NFR-001), so out of scope.

**Exit-code expectation:** Click surfaces an uncaught `KeyboardInterrupt` as exit **130**
(SIGINT = 128+2) via `click.BaseCommand.main`'s `except (EOFError, KeyboardInterrupt)` handler.
v1 should let `KeyboardInterrupt` propagate (do NOT catch-and-`pass`); Click yields 130. If a
deterministic test-surface code is wanted, an explicit `raise click.exceptions.Exit(130)` after
`tui.stop()` is the equivalent. The key correctness point: the exit code must be **non-zero**
and distinct from a clean run (`EXIT_OK = 0`, `commands.py:188`).

**How `run_cmd` currently treats `KeyboardInterrupt`:** it does **not** — there is no
`except KeyboardInterrupt` anywhere in `run_cmd`'s fresh-run dispatch path (verified via
`grep -n "KeyboardInterrupt" commands.py` → only hits are `status --watch` at `:2606` and
`logs --follow` at `:2826`; `run_cmd` spans `:1471-1912` and contains none). The fresh-run
path ends at `commands.py:1912` `raise click.exceptions.Exit(EXIT_OK)`. So today a SIGINT
during the synchronous `dispatch_wave1` simply propagates to Click → exit 130 with no TUI
teardown needed (no TUI exists yet). The new TUI path must ADD the `try/finally: tui.stop()`
so the Live display is torn down on that same SIGINT propagation.

**Source reads:**
- `src/superclaude/cli/swarm/tui.py:230-234` (idempotent `stop()`).
- `src/superclaude/cli/swarm/commands.py:2585-2613` (`status --watch` SIGINT precedent — swallow+exit-last-code; deliberately diverged from for the mutating run path).
- `src/superclaude/cli/swarm/commands.py:1471` (`run_cmd` def) / `:1912` (`raise click.exceptions.Exit(EXIT_OK)` terminal) / `:188` (`EXIT_OK = 0`) — confirms no existing KeyboardInterrupt handler in `run_cmd`.
- `merged-requirements.md:111-119` (FR-6 idempotent teardown on clean/exception/SIGINT).

---

## G4 (IMPORTANT) — `tui.py` UNCHANGED verdict + the Rich redirect trap

**`TUI.start()` uses Rich's DEFAULT `redirect_stdout/redirect_stderr=True`.** **[CODE-VERIFIED]**

`src/superclaude/cli/swarm/tui.py:218-228`:

```python
218    def start(self) -> Live:
219        """Start the Live display. Caller owns :meth:`stop`."""
220        self._started_at = time.time()
221        self._live = Live(
222            self.render(self._state, self._events),
223            console=self.console,
224            refresh_per_second=self._refresh,
225            screen=False,
226        )
227        self._live.start()
228        return self._live
```

`Live(...)` is constructed with `screen=False` and **no** `redirect_stdout=`/`redirect_stderr=`
argument (`tui.py:221-226`). Rich's `Live.__init__` defaults both to `True`, so the redirect
**is on** — any thread that writes to the real `sys.stdout`/`sys.stderr` while this Live is
active gets its bytes funneled into the Live's Console buffer. This is the exact mechanism
behind the #181/#182/#184 cross-thread "Thread-1 NoneType render crash" documented for the
sprint TUI (`03-patterns-conventions.md` §4d, citing `sprint/tui.py:108-128`).

**VERDICT: Approach A requires NO change to `tui.py` (v1) — SAFE.**

**Reasoning (the trap is present-but-not-armed):**
- In Approach A, the **only** thread that touches the `Console`/`Live` is the **main thread**
  (it owns `TUI.start/update/stop`, per FR-1, `merged-requirements.md:51-61`).
- The **workers / dispatch thread write SOLELY to the filesystem** via the `Logger`
  (`commands.py:1732-1740` constructs the Logger; dispatch appends through it). They do not
  call `click.echo`, `print`, or touch `sys.stdout`/`sys.stderr`.
- Therefore, even though `redirect_stdout/stderr` stays default-`True`, **no other thread
  writes to stdout/stderr while Live is active** → there is no cross-thread write for the
  redirect to capture → the crash class is NOT armed. The redirect only becomes dangerous
  when a *second* thread writes to the redirected streams concurrently; Approach A
  structurally eliminates that second writer.
- This is precisely why **FR-1** (single-writer Console topology) is a *non-negotiable gate*:
  it converts "no worker writes to stdout" from a discipline into a structural property,
  enforced by the AST/grep audit (`merged-requirements.md:58-61` — the `test_inv012_tui_opt_in.py`
  audit asserts `tui`/`Live`/`Console` are reachable from ZERO dispatch/worker functions).

**Residual risk + the guarantee that contains it:** the residual risk is that *some* worker-side
code path emits to stdout/stderr (e.g. a stray `print`, a transport that logs to stderr) while
Live is active — that single write WOULD be captured by the still-default-on redirect and could
trip the crash. The FR-1 AST audit is the structural enforcement: if any
dispatch/worker-reachable function references `print`/`sys.stdout`/`sys.stderr`/`Console`/`Live`,
the audit fails and the build stops. **Final verdict: `tui.py` unchanged = SAFE under FR-1's
single-writer guarantee**, because the only writer to the redirected streams during a Live
session is the main thread itself (which writes *through* the Live, not around it).

**Worker-side stdout scan (CRITICAL-flag check):** I did not find a worker-side stdout write in
the dispatch path that would leak into Live. The dispatch path routes output through the
`Logger` (filesystem), and `dispatch_wave1`'s signature (`dispatch.py:334-343`, per
`02-reader-contracts.md:116-128`) takes a `logger=` rather than a console. **No CRITICAL flag
raised** — but the FR-1 audit must be the runtime gate that keeps it that way (a future transport
that prints to stderr would re-arm the trap; the audit catches it).

**Source reads:**
- `src/superclaude/cli/swarm/tui.py:218-228` (`Live(...)` with `screen=False`, no redirect kwargs → Rich default `redirect_stdout/stderr=True`).
- `src/superclaude/cli/swarm/commands.py:1732-1740` (worker output channel = the filesystem `Logger`, not the console).
- `merged-requirements.md:51-61` (FR-1 single-writer Console topology + the zero-reachability AST audit).

---

## G5 (MINOR) — `state=None` header rendering is safe

**`_build_header` handles `state is None` with a `"-"` fallback — no crash.** **[CODE-VERIFIED]**

`src/superclaude/cli/swarm/tui.py:272-285`:

```python
272    def _build_header(
273        self,
274        state: Optional[SwarmState],
275        workers: dict[int, WorkerSnapshot],
276    ) -> Text:
277        state_value = state.state if state is not None else "-"
278        job_id = state.job_id if state is not None else "-"
279        elapsed = max(0.0, time.time() - self._started_at)
280        return Text.from_markup(
281            f"[dim]job:[/] [bold]{job_id or '-'}[/]    "
282            ...
283        )
```

- `tui.py:277` — `state_value = state.state if state is not None else "-"`: the `None` branch
  yields the literal `"-"`, never dereferences `state`.
- `tui.py:278` — `job_id = state.job_id if state is not None else "-"`: same guard.
- The markup at `:281` further guards `{job_id or '-'}`, so even an empty-string `job_id`
  renders `-`.

**`read_state()` returning `None` mid-run does NOT crash render.** `read_state(path)` returns
`None` when `.swarm-state.json` is missing (`state.py:190-193`, per `02-reader-contracts.md:60`).
This is exactly the early-run window — the poll loop starts before/just as the worker writes
the state file. `TUI.update(None, events)` (`tui.py:236-245`) stores `state=None`, then `render`
(`tui.py:251-270`) calls `_build_header(None, workers)` which takes the `"-"` fallback at
`tui.py:277-278`. No `AttributeError`. The worker table (`_build_worker_table`, `tui.py:287+`)
is built purely from `events` and is independent of `state`, so it also renders during the
`state is None` window.

**Source reads:**
- `src/superclaude/cli/swarm/tui.py:272-285` (`_build_header` None-safe via `"-"` fallback at `:277-278`).
- `src/superclaude/cli/swarm/tui.py:236-245` (`update` accepts `Optional[SwarmState]`) + `:251-270` (`render` pure path).

---

## G6 (MINOR) — `_tail_events` location, signature, and the `_follow_log` name fix

**Recommendation: `_tail_events` lives as a module-level private function in
`src/superclaude/cli/swarm/commands.py`**, alongside `_follow_log` (`commands.py:2737`) and
`_drain_appended` (`commands.py:2834`) — NOT in `tui.py`.

**Rationale:**
- `_tail_events` is `run_cmd`-specific glue (it bridges the on-disk `execution-log.jsonl` to
  `TUI.update`); it is not consumer/render logic. `tui.py` must stay consumer-only/pure
  (`render` is documented pure at `tui.py:256-260`), so file-tailing I/O does not belong there.
- It reuses the **same byte-offset idiom** already proven in `commands.py`: `_drain_appended`
  (`commands.py:2834-2858`) is the byte-offset primitive — `open(log_path, "rb")` →
  `fh.seek(start_pos)` → `fh.read()` → `return fh.tell()` (`commands.py:2844-2847`,2858).
  `_tail_events` mirrors this `seek/read/tell` bookkeeping but **yields parsed `EventRecord`s
  instead of echoing to stdout** (`_drain_appended` ends in `click.echo(text, nl=False)` at
  `commands.py:2857`, which `_tail_events` must NOT do).

**Signature:**

```python
def _tail_events(path: Path, offset: int) -> tuple[list[EventRecord], int]:
    """Read EventRecords appended since `offset`; return (events, new_offset).

    Buffers a partial trailing line: advances `offset` only past the last
    complete newline so a half-written JSON line is re-read on the next poll.
    Tolerates JSONDecodeError on a partial line by NOT advancing past it.
    """
```

- Returns `(newly-parsed events, new byte offset)`.
- **Partial-trailing-line tolerance:** advance the returned offset only up to the last `\n`;
  a trailing partial line is left unconsumed so the next poll re-reads it once complete. This
  is the cleaner discipline than `_drain_appended`'s `errors="replace"` (`commands.py:2853-2856`)
  because a half-written JSON object must be re-parsed whole, not decoded with replacement chars.
- **JSONDecodeError handling:** if a line fails `from_json(EventRecord, line)`, do NOT advance
  the offset past it (treat as still-partial); retry next poll. Per-line parse uses
  `from_json(EventRecord, line)` — and note the corrected import: `from_json` lives in
  **`models.py:1820`**, NOT `logging_.py` (`02-reader-contracts.md:65-81` / TL;DR item 1).

**Name-mislabel fix (from `02-reader-contracts.md`):** `02-reader-contracts.md` refers to the
follow helper as **`_follow_log_file`** (lines 141, 147, 168). **That name is WRONG.** The actual
function is named **`_follow_log`** (`src/superclaude/cli/swarm/commands.py:2737`
`def _follow_log(`). **[CODE-VERIFIED]** — verified by direct read of `commands.py:2737`. The
byte-offset primitive it calls, `_drain_appended`, is correctly named at `commands.py:2834`.
Use `_follow_log` (not `_follow_log_file`) as the structural reference when authoring
`_tail_events`.

**Source reads:**
- `src/superclaude/cli/swarm/commands.py:2737` (`def _follow_log(` — the correct name; fixes `02-reader-contracts.md`'s `_follow_log_file` mislabel at its lines 141/147/168).
- `src/superclaude/cli/swarm/commands.py:2834-2858` (`_drain_appended` — the `seek`/`read`/`tell` byte-offset primitive to mirror; ends in `click.echo` at `:2857`, which `_tail_events` must replace with parse+yield).
- `src/superclaude/cli/swarm/commands.py:2790` (`last_pos = len(existing.encode("utf-8"))` — offset-seed idiom) / `:2818-2825` (truncation-restart + size-gated drain skeleton).
- `02-reader-contracts.md:65-81` (`from_json` is in `models.py:1820`, not `logging_.py`).

---

**Status:** Complete
