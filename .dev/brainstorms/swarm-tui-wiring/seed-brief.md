---
topic: "Finish T07.01 — wire the --tui flag into `superclaude swarm run`"
domain: code
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-06-18T16:43:40+00:00
---

# Seed Brief: swarm-tui-wiring

## Problem Statement

`src/superclaude/cli/swarm/tui.py` (316 LOC) is fully built and unit-tested — a Rich
`Live` dashboard (`TUI.start/update/stop/render`), an INV-012 opt-in gate
(`should_enable_tui()`), and an `EventRecord`-stream→per-worker projection
(`_project_workers`). But it is **unreachable from the CLI**: `commands.py` has zero
imports of `tui`/`TUI`/`should_enable_tui`, `run_cmd` (commands.py:1471) exposes no
`--tui` option, and `--tui` has never appeared in `commands.py` git history. T07.01 is
the **only open code gap** in the otherwise-complete MultiModelSwarm release
(PHASE-STATUS-AUDIT-20260618.md).

The blocker is architectural, not a missing flag. `run_cmd` makes a **single blocking
call** `worker_results = dispatch_wave1(...)` (commands.py:1807) that returns all
results at once; `dispatch_wave1` (dispatch.py:334) exposes **no callback/observer/
progress** parameter. The TUI is a live-polling consumer (`start → repeated update() →
stop`), so a naive `start()/stop()` wrapped around line 1807 renders an empty, frozen
dashboard for the whole run.

## Known Context (verified this session against the code)

- **tui.py contract**: `TUI.update(state, events)` consumes a `SwarmState` snapshot +
  an `Iterable[EventRecord]`. `should_enable_tui(flag, stream)` = `--tui` AND
  `stream.isatty()` (INV-012, conservative on non-TTY). Default `refresh_per_second=2`.
- **Existing on-disk seam**: `dispatch` writes events incrementally via
  `logger.log_event()` → `event-log.jsonl` (dispatch.py:302/312/432/496) and `SwarmState`
  via `write_state`. **`from_json(EventRecord, line)` already exists** (logging_.py:46;
  generic `from_json` at models.py:1711) and **`read_state()` already exists**
  (state.py:178). So both readers needed by a poller are already built — the only new
  code is a JSONL *tail* (open → read lines → `from_json` each).
- **`status --watch`** (status_cmd, commands.py ~2545) is a working poll loop:
  `while not terminal: emit; sleep(watch_interval, default 2.0s)`, with a
  `watch_max_iterations` ceiling. **It reads STATE ONLY, not events** — so it donates the
  *loop shape* (terminal-detection, interval, iteration ceiling, test lever) but not an
  event reader.
- **dispatch call sites**: primary `dispatch_wave1(...)` at commands.py:1807 (fresh run);
  resume branch `_run_resume_branch` at 2048 calls its own `dispatch_wave1` at 2264.
- **detached**: `--detached` option at 1453-1463; the detached branch **returns early at
  1606** (launches a child tmux session) *before* the inline dispatch path. `resume +
  --detached` is already rejected as mutually exclusive at 1547-1550.
- **Sprint peer (critical precedent)**: `src/superclaude/cli/sprint/tui.py` documents a
  **Rich `Live` cross-thread render crash** ("Thread-1 NoneType render crash",
  sprint/tui.py:104-119) — the fix disables Rich's stdout-redirect because *other threads
  writing into the Live console buffer* corrupt the render. The active branch is
  `chore/crash-recovery-cleanup-20260618`; recent commits (#181/#182 faulthandler + Live
  redirect-disable, #184 run-lock vs concurrent-run SIGSEGV) are all about this crash
  class. **This is the dominant risk constraint for any threaded approach.**

## Candidate Approaches

- **A — Threaded dispatch + main-thread file-tailing poller**: run `dispatch_wave1` in a
  background thread; main thread does `should_enable_tui()` → `TUI.start()` → loop
  `read_state()` + tail `event-log.jsonl` → `tui.update()` until the worker thread joins →
  `stop()` → continue to `normalize_wave2`/`reduce_wave3`. **No change to
  `dispatch_wave1` signature.** (analysis-preferred)
- **B — `callback=` param threaded through `dispatch_wave1` → ParallelExecutor →
  `_run_worker`** so the TUI updates in-process. (more invasive; changes the parallel
  layer)
- **C — Render-once-at-end**: rejected — defeats the purpose of a `Live` dashboard.

## Constraints

- **C1 (INV-012)**: No ANSI / Rich control sequences may reach a non-TTY stream. The
  `should_enable_tui()` gate must be the sole entry to any Rich `Live`.
- **C2 (crash-safety)**: Given the sprint Rich-`Live`-cross-thread crash history, **only
  one thread may ever touch the `Console`/`Live`.** Approach A satisfies this *only if*
  the background dispatch thread never writes to the Console (it writes JSONL + state to
  disk, which is already the case).
- **C3 (no regression)**: The default (no `--tui`) code path must be byte-for-byte
  unchanged — `dispatch_wave1` signature and the synchronous result flow must be preserved
  for the non-TUI path.
- **C4 (test discipline)**: `test_inv012_tui_opt_in.py` currently passes *vacuously*
  (nothing wired); `test_tui.py` is unit-only. A real TTY-path integration test is
  required.

## Resolved Scope Decisions (user, this session)

- **D1 — Resume scope**: `--tui` wires the **fresh-run path only (v1)**. The resume
  branch (2264) runs without TUI; a follow-up task may add it. Rationale: smallest
  surface, fewer integration points, resume branch is more state-sensitive.
- **D2 — `--tui` + `--detached`**: **hard UsageError**, mirroring the existing
  resume+detached rejection at 1547. A passed flag must never silently do nothing.

## Success Criteria

- `swarm run --tui` on a TTY renders a live, *updating* dashboard for the duration of
  Wave 1 dispatch, then yields cleanly to Wave 2/3 output.
- `swarm run --tui` piped to a file/non-TTY emits **zero** Rich/ANSI bytes (INV-012).
- `swarm run` (no flag) is behaviourally identical to today.
- `swarm run --tui --detached` exits with a clear UsageError.
- A non-vacuous integration test exercises the real TTY render+update path.

## Open Questions for the Debate

1. **A vs B vs hybrid** — which driver mechanism, given C2 (crash-safety) is the
   dominant constraint?
2. **Refresh cadence / reader reuse** — reuse `read_state()` + a new JSONL tail at
   `refresh_per_second`/poll cadence 2/s (matching both peers)? How to bound the tail
   (re-read whole file vs offset)?
3. **Thread lifecycle & error propagation** — if the background dispatch thread raises,
   how does the main thread surface it after `stop()` (so a worker crash isn't masked by
   a clean dashboard)?
4. **Design stage?** — does a `/sc:design` component-spec stage add value for this
   single-module wiring, or go straight to task-builder?
