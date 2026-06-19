# Adversarial Debate Transcript — swarm-tui-wiring

**Mode:** Mode B (parallel proposal generation + debate + merge)
**Proposals:** 3 (opus·A-advocate / sonnet·B-advocate / opus·synthesizer)
**Depth:** deep · **Convergence:** 0.92 (PASS)

## Proposals & stances

| ID | Model | Stance | Pick | Design verdict |
|----|-------|--------|------|----------------|
| A | opus (system-architect) | Advocate threaded-dispatch + main-thread poller | **A** | task-builder |
| B | sonnet (system-architect) | Advocate `callback=` through ParallelExecutor | **A** (conceded) | task-builder |
| C | opus (refactoring-expert) | Synthesizer/skeptic — hybrid vs pure | **A** | task-builder |

## The deciding axis: crash-safety (C2)

The active branch (`chore/crash-recovery-cleanup-20260618`) and commits #181/#182/#184
exist to extinguish a Rich `Live` **cross-thread render crash**: when a thread other than
the Live's owner writes into the Console buffer, the render corrupts (sprint/tui.py:104-126,
"Thread-1 NoneType crash"). The invariant is **exactly one thread may touch Console/Live**.

The synthesizer added the load-bearing fact: **swarm `tui.py:221-226` starts `Live` with
Rich's default `redirect_stdout/stderr=True`** (it does *not* pass `redirect=False` the way
sprint's probe does). So any worker-thread stdout/stderr is silently funneled into the Live
buffer — the trap is armed.

- **A** makes one-thread-touches-Console a *structural property*: workers write only to
  `event-log.jsonl`/state (a filesystem boundary); the main thread is the sole caller of
  `tui.update()`. The crash class is **unreachable by construction.**
- **B**'s callback fires *on worker threads*. To be safe it must merely enqueue (never touch
  Console) — but that discipline now lives inside worker-thread code, the exact configuration
  that crashed, with the redirect still armed. B's own advocate conceded: "B's 'in-process'
  advantage evaporates the moment you make it crash-safe… it has reimplemented A's poll loop
  plus a thread-safe queue plus the signature churn."
- **Hybrid** = A's topology + B's queue feed. Same safety as A, *more* moving parts, *and*
  B's three-layer `callback=` signature churn — for a latency win nobody can perceive
  (event volume = N workers × ~3 events; a 2 Hz tail of a <30-line file is free). Rejected
  as gold-plating by the synthesizer; the disk artifact *is* the seam `tui.py` was designed
  around (dual ISO/Z timestamp parsing, `_parse_timestamp` tui.py:125-142).

## Secondary axes (all favor A)

- **Minimal change / C3 no-regression:** A touches **zero** lines of `dispatch_wave1`
  (dispatch.py:334) / `ParallelExecutor` / `_run_worker`; the non-TUI path runs the existing
  synchronous call verbatim. B adds a `callback=` param to all three (AC-004/NFR-001-protected
  layer) → highest blast radius. A wins.
- **Reuse:** A reuses three proven components — `read_state()` (state.py:178),
  `from_json(EventRecord, line)` (logging_.py:46), and the `status --watch` loop *shape*
  (commands.py ~2545). Only genuinely-new code: a small JSONL tail helper.

## Resolved tensions / converged decisions

1. **Driver:** Pure **A**. Unanimous (B's advocate conceded).
2. **Refresh cadence:** reuse TUI's own `refresh_per_second=2` → 0.5s sleep (more responsive
   than `status --watch`'s 2.0s text cadence; still trivially cheap). Byte-offset tail (A) /
   exactly-once delivery preferred over whole-file re-read.
3. **Exception masking** (raised by all three as the subtle failure): capture worker
   `BaseException`, `tui.stop()` in `finally`, **then** re-raise on main thread with original
   traceback — clean teardown order so a worker crash isn't masked by a tidy dashboard.
4. **Design stage:** **Skip `/sc:design`.** Unanimous — the debate *is* the design stage;
   `tui.py` is built+tested; remaining work is mechanical glue + tests against a fixed
   contract (`SwarmState` + `Iterable[EventRecord]`).

## Residual cautions carried into requirements

- FR-1 (single-writer grep-audit) and FR-5 (thread-exception-not-masked) are the two
  requirements whose violation re-opens the crash class — encode as **non-negotiable gates**.
- The existing `test_inv012_tui_opt_in.py` passes *vacuously* (grep-only) and `test_tui.py`
  is unit-only; a real run→tui integration test is mandatory (FR-7).
