---
title: "T07.01 — Wire --tui into `superclaude swarm run`"
domain: code
source: seed-brief.md
adversarial_status: pass
convergence_score: 0.92
recommended_approach: "A — threaded dispatch + main-thread file-tailing poller"
design_stage_needed: false
created: 2026-06-18T16:43:40+00:00
scope: fresh-run-only-v1
target_files:
  - src/superclaude/cli/swarm/commands.py        # run_cmd glue + scope guards (primary change)
  - src/superclaude/cli/swarm/tui.py             # consumer (already built; likely no change)
  - src/superclaude/cli/swarm/logging_.py        # from_json(EventRecord, line) reader (reuse)
  - src/superclaude/cli/swarm/state.py           # read_state() reader (reuse)
  - tests/swarm/test_tui.py                       # unit (exists)
  - tests/swarm/test_inv012_tui_opt_in.py         # currently vacuous — tighten
  - tests/swarm/                                  # NEW run->tui integration test
unchanged_by_design:
  - src/superclaude/cli/swarm/dispatch.py        # dispatch_wave1 signature MUST NOT change (C3)
  - src/superclaude/execution/parallel.py        # ParallelExecutor untouched (AC-004/NFR-001)
---

# Merged Requirements — Wire `--tui` into `swarm run`

## Summary

`tui.py` (the Rich `Live` dashboard, `should_enable_tui()` gate, `_project_workers()`
projection) is fully built and unit-tested but **unreachable** — `run_cmd` has no `--tui`
option and never imports it. The blocker is architectural: `run_cmd` makes a single
**blocking** `dispatch_wave1(...)` call (commands.py:1807) with no callback/observer seam,
so there is nowhere to pump `tui.update()` mid-run.

**Recommended approach (unanimous, convergence 0.92): Approach A.** Run `dispatch_wave1`
on a **background thread**; the **main thread** owns the entire TUI lifecycle —
`should_enable_tui()` → `TUI.start()` → poll loop {`read_state()` + tail `event-log.jsonl`
→ `tui.update(state, events)`} until the worker thread joins → `tui.stop()` → continue to
`normalize_wave2`/`reduce_wave3`. **No change to `dispatch_wave1` or `ParallelExecutor`.**

**Why A over B/hybrid:** the active branch exists to kill a Rich `Live` *cross-thread
render crash* (sprint/tui.py:104-126; #181/#182/#184), and swarm `tui.py:221-226` starts
`Live` with Rich's **default `redirect_stdout/stderr=True`** — the trap is armed. A makes
"exactly one thread touches the Console" a *structural property* (workers' only output
channel is the filesystem); B's callback fires from worker threads and re-opens the crash
class unless policed by discipline inside worker code; hybrid pays B's signature churn for
a latency win that is imperceptible at this event volume (N workers × ~3 events). See
`adversarial/debate-transcript.md`.

## Requirements

### FR-1 — Single-writer Console topology *(non-negotiable gate; crash-safety C2)*

`run_cmd` MUST run `dispatch_wave1` on a background thread and perform **all**
`TUI.start/update/stop` calls on the main thread. No worker/dispatch code path
(`dispatch_wave1`, `ParallelExecutor`, `_run_worker`, or any callable they invoke) may
import, reference, or call any `TUI` / `rich.live.Live` / `rich.console.Console` method.

- **Acceptance:** extend the existing grep/AST audit (`test_inv012_tui_opt_in.py`, today
  vacuous) to assert `tui`/`Live`/`Console` symbols are reachable from **zero** functions on
  the dispatch/worker side; a runtime assertion that `TUI.update` only ever runs on the main
  thread (`threading.get_ident()` check).

### FR-2 — INV-012 gate + non-TUI no-regression *(C1 + C3)*

The Rich `Live` activates **only** when `should_enable_tui(--tui, stream)` is `True`
(`--tui` AND `stream.isatty()`). When it returns `False` (flag absent, or non-TTY), `run_cmd`
MUST execute the pre-existing **synchronous** `dispatch_wave1` path with byte-identical
behavior — no thread spawned, no tail loop, no Rich import side effects, and the
`dispatch_wave1` signature unchanged.

- **Acceptance:** `swarm run` piped to a non-TTY, with and without `--tui`, yields identical
  exit code, identical `event-log.jsonl` + state output, and **zero** ANSI bytes on stdout.

### FR-3 — Scope guards: detached + resume *(D1 / D2)*

- `--tui --detached` MUST raise a `UsageError` **before** dispatch (mirror the existing
  resume+detached rejection at commands.py:1547).
- `--tui` on a **resume / non-fresh** invocation MUST be rejected (v1 scope = fresh-run only;
  the resume `dispatch_wave1` at 2264 does **not** enter the TUI loop).

- **Acceptance:** both invocations exit with `UsageError` naming the incompatibility; the
  resume path with `--tui` does not spawn the TUI loop.

### FR-4 — Event/state read path (reuse existing readers, byte-offset tail)

The poll loop MUST source data from the **already-built** readers: `read_state()`
(state.py:178) for the `SwarmState` snapshot and a JSONL tail of `event-log.jsonl` parsed
via the **existing** `from_json(EventRecord, line)` (logging_.py:46). The tail MUST track a
**byte offset** (not re-read the whole file), deliver each event **exactly once**, and
tolerate a partial trailing line (resume at the next newline). Refresh cadence: reuse the
TUI's own `refresh_per_second=2` (≈0.5s loop sleep). Loop exit is driven by the worker
thread no longer being alive; an optional iteration ceiling (mirroring
`watch_max_iterations`) guards against an unbounded spin.

- **Acceptance:** feed an incrementally-written `event-log.jsonl` with a mid-line truncation;
  assert exactly-once delivery, no parse error on the partial line, and ≥1 worker row
  projected via `_project_workers`.

### FR-5 — Thread exception not masked *(non-negotiable gate)*

If the background `dispatch_wave1` thread raises any `BaseException`, `run_cmd` MUST capture
it, call `tui.stop()` **first**, and **then** re-raise on the main thread preserving the
original traceback and producing a non-zero exit. A worker crash MUST NOT be hidden behind a
clean dashboard teardown. (Worker thread is **non-daemon** with an explicit `join()` so
`event-log.jsonl` is never truncated at interpreter shutdown.)

- **Acceptance:** inject a `dispatch_wave1` that raises; assert `tui.stop()` ran, the terminal
  is restored, the process exits non-zero, and the **original** exception/traceback reaches
  the caller (not a generic "TUI closed" message).

### FR-6 — Idempotent teardown on every exit path

`tui.stop()` (idempotent per tui.py:230) MUST run exactly once via `finally` on **all** exit
paths: normal completion, worker exception, and `KeyboardInterrupt`. No run may leave the
terminal in `Live`'s render state.

- **Acceptance:** parametrize the three exit paths (clean / exception / SIGINT); assert
  `stop()` was called and is idempotent on a second call; SIGINT mid-run leaves the terminal
  restored with an exit code reflecting interruption.

### FR-7 — Non-vacuous integration test (run → tui seam)

Add an integration test under `tests/swarm/` that drives `run_cmd` with `--tui` against a
**forced-TTY** stream (or a `should_enable_tui` shim returning `True`) on a real fresh-run
dispatch, and asserts the dashboard rendered **≥1 non-vacuous worker row** sourced from the
tailed `event-log.jsonl`. This closes the gap left by `test_inv012_tui_opt_in.py` (grep-only,
passes vacuously) and `test_tui.py` (unit-only) — neither exercises the `run_cmd → tui` seam.

- **Acceptance:** the test fails if `--tui` is unwired (regression guard), and passes with a
  populated worker table; INV-012 companion assertion confirms zero ANSI on a non-TTY run.

## RECOMMENDED APPROACH

**Approach A — threaded dispatch + main-thread file-tailing poller.** Unanimous across all
three proposals (B's own advocate conceded that a crash-safe B collapses into "A plus a queue
plus signature churn"). A is the only driver that makes the crash-safety invariant
*structural*, reuses three proven readers, and leaves the C3 non-TUI path and the
`dispatch_wave1`/`ParallelExecutor` signatures **completely unchanged**.

Implementation shape (in `run_cmd`, fresh-run path only):

```python
from superclaude.cli.swarm.tui import TUI, should_enable_tui  # new import

result_box, exc_box = {}, {}
def _worker():
    try:    result_box["v"] = dispatch_wave1(...)        # UNCHANGED call
    except BaseException as e:  exc_box["e"] = e
t = threading.Thread(target=_worker, name="swarm-wave1", daemon=False)
tui = None
try:
    t.start()
    if should_enable_tui(tui_flag, sys.stdout):
        tui = TUI(); tui.start()
        offset = 0
        while t.is_alive():
            state = read_state(run_dir)
            events, offset = _tail_events(event_log_path, offset)   # new helper
            tui.update(state, events)
            time.sleep(0.5)                                          # 2/s
    t.join()
finally:
    if tui is not None:  tui.stop()                                  # idempotent
if "e" in exc_box:  raise exc_box["e"]                               # re-raise AFTER stop()
worker_results = result_box["v"]
# normalize_wave2 / reduce_wave3 continue unchanged
```

New code is confined to: the import, the thread wrapper + gated poll loop in `run_cmd`, one
small `_tail_events` helper, the two scope-guard rejects (FR-3), and the FR-1/FR-7 tests.

## VERDICT: Design stage needed?

**No — skip `/sc:design`; go straight to `/task-builder`.** Unanimous across all three
proposals.

**Debate:** A `/sc:design` component-spec stage adds value when interfaces between *multiple*
components or non-obvious data contracts are still unresolved. Here, none are:

- **The architecture is already decided.** This adversarial debate *was* the design stage —
  it converged (0.92) on a single driver (A), a settled topology (background dispatch /
  main-thread render / filesystem thread boundary), a settled data source (existing
  `event-log.jsonl` via existing `from_json`/`read_state`), and settled scope gates (D1/D2).
  A `/sc:design` pass would only re-state these constraints.
- **The component is built and tested.** `tui.py` already has a pure `render()`, idempotent
  `stop()`, the INV-012 gate, and dual-timestamp parsing explicitly designed for on-disk
  reads. There is no new component to specify — only glue.
- **The data contract is fixed.** `TUI.update(SwarmState, Iterable[EventRecord])` pins the
  interface; the readers exist. Nothing is left to architect.
- **The remaining work is mechanical wiring** with a well-understood seam: ~1 glue block in
  `run_cmd`, 1 small tail helper, 2 scope guards, and the tests — precisely `/task-builder`'s
  sweet spot. Running `/sc:design` here would be process gold-plating that re-derives content
  this brainstorm already produced, contradicting the same minimal-change principle that
  selected Approach A.

The seven FRs above **are** the component spec at the granularity that matters and should be
handed to `/task-builder` as the acceptance contract — with FR-1 and FR-5 flagged as the
non-negotiable gates whose violation re-opens the cross-thread crash class.

## Next step (paste-ready)

```
/task-builder Wire the --tui flag into `superclaude swarm run` per Approach A in the brainstorm output: run dispatch_wave1 on a non-daemon background thread; the main thread gates on should_enable_tui(), runs TUI.start() then a 2/s poll loop that calls read_state() + tails event-log.jsonl via from_json(EventRecord, line) (byte-offset, exactly-once, partial-line tolerant) into tui.update(), joins, then tui.stop() in finally and re-raises any captured worker BaseException AFTER stop(). Add the --tui Click option to run_cmd; hard-error on --tui --detached (mirror the resume+detached reject at commands.py:1547); fresh-run path only (resume dispatch at 2264 excluded, v1). Do NOT change dispatch_wave1 or ParallelExecutor signatures (C3/AC-004). Tighten the vacuous tests/swarm/test_inv012_tui_opt_in.py grep-audit and add a forced-TTY run->tui integration test asserting >=1 worker row. Files: src/superclaude/cli/swarm/commands.py, tui.py, logging_.py, state.py; tests under tests/swarm/. --spec /config/workspace/IronClaude/.dev/brainstorms/swarm-tui-wiring/merged-requirements.md
```
