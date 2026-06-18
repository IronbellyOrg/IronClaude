---
status: partial
tier_reached: 2
confidence: 0.25
leading_hypothesis: H-C (Rich redirect-IO shared-Console concurrency) — UNPROVEN
superseded_hypothesis: H-A (unsafe preexec_fn fork) — calibrated 0.25, subordinate
escalation_reason: forced_by_depth_deep; then low_confidence after empirical disconfirmation
type: bug
behavior_is_documented: false
test_is_wrong: false
revised: 2026-06-17 (post-repro + independent calibration)
---

> ⚠️ **REVISED — read this first.** The original diagnosis below (H-A: unsafe
> `preexec_fn=os.setpgrp` fork, confidence 0.86) **did not survive verification.**
> The empirical repro `MODE=unsafe` **SURVIVED** (it was predicted to crash), and
> independent calibration re-graded H-A to **0.25, subordinate to H-C**. The crash
> is a **clean Python `TypeError`** (not a segfault), which argues against heap
> corruption. The current leading hypothesis is **H-C: a Rich concurrency edge from
> the Live display's default `redirect_stdout/stderr=True` causing cross-thread
> writes into one `Console._buffer`** — itself **UNPROVEN** (rich 15.0.0 appears to
> lock-guard it). See `## Revised Diagnosis` at the bottom, plus `repro-result.md`,
> `tier2-quality-engineer-REDISPATCH.md`, and `tier2-python-expert-calibration.md`.
> The `start_new_session=True` change remains a worthwhile fix for a real latent
> hazard, but it is **not confirmed to fix this crash.**

# Troubleshoot REPORT — sprint runner crash: `TypeError … NoneType` in Rich Live thread

**Target:** `superclaude sprint run` crashes in the Rich `Live` auto-refresh thread (Thread-1)
**Tier reached:** 2 (forced by `--depth deep`) · **Calibrated confidence:** 0.86 · **Type:** bug (concurrency / fork-safety)
**Adversarial debate:** skipped — both Tier-2 hypothesis agents reached **consensus on one fix** (no competing proposals to debate).

---

## Summary

The crash is **not a Rich bug and not a logic/`None`-leak bug in the TUI** — every TUI render helper and model property provably returns `str` on every path. The real defect is an **unsafe `preexec_fn=os.setpgrp` fork in a multithreaded process** (`src/superclaude/cli/pipeline/process.py:189-190`). Each task spawn forks a new `claude` subprocess while ≥3 other threads are live (Rich `Live` refresh, `OutputMonitor`, forking `SummaryWorker` daemons). CPython documents `preexec_fn` as **not safe in the presence of threads**: it forces the slow fork path that runs interpreter-level Python *between* `fork()` and `exec()`, while locks held by other threads at fork time (glibc malloc arena lock, CPython internal locks) are cloned in a held-but-ownerless state. The `NoneType` that Rich's `"".join(output)` chokes on at segment index 139 is a **corrupted `str` object** surfaced by whichever thread next touches the heap — here, the 2 Hz Live refresh thread. The `stalled >300s` line just before the crash is the *other* canonical symptom of the same defect (fork-deadlock).

The fix is a one-line, behavior-preserving change: **`start_new_session=True`** instead of `preexec_fn=os.setpgrp`.

## Documentation Context

No project release-doc or architectural-doc constraints govern this surface; the authoritative contract is **CPython's `subprocess` documentation** (the `preexec_fn` thread-safety warning) and POSIX `fork()`/`setsid()` semantics. The observed behavior is a **defect**, not a documented contract — `behavior_is_documented=false`.

## Diagnosis

At a phase/task boundary the runner process holds, simultaneously:

| Thread / actor | Source |
|---|---|
| Rich `Live(refresh_per_second=2)` auto-refresh thread (**Thread-1**) | `src/superclaude/cli/sprint/tui.py:101` |
| `OutputMonitor` daemon poll thread | `src/superclaude/cli/sprint/monitor.py:280-282` |
| `SummaryWorker` daemon-thread pool … | `src/superclaude/cli/sprint/summarizer.py:596-599` |
| … each forking via `subprocess.run` | `src/superclaude/cli/sprint/summarizer.py:339` |
| **Main thread** forking the next subprocess with the unsafe flag | `src/superclaude/cli/pipeline/process.py:189-190,192` |

`preexec_fn=os.setpgrp` forces CPython onto the fork+manual-exec path and runs Python (`os.setpgrp`) in the child between `fork()` and `exec()`. In a multithreaded parent this is the textbook lock-cloned-while-held hazard; the symptom is heap/object corruption observed in an unrelated thread. The chained `&& … --start 5` invocation is a *separate* OS process (each `superclaude sprint run` is a fresh Click command) — it is **not required** for the bug; it merely doubles exposure. A single run accumulates the hazard across every task spawn, which is why the panel shows the crash mid-Phase-4 (`T04.03`).

**Why the competing hypotheses were rejected:**
- **Genuine `None`-leak in the TUI** — refuted by exhaustive audit: `_truncate` (`tui.py:620-629`), `_format_bytes` (`583-591`), `_format_tokens` (`568-580`), `_render_bar` (`594-601`), `_render_percent` (`604-609`), `_render_activity_stream` (`416-439`), `_build_active_panel` (`362-414`), and the `MonitorState.stall_status`/`output_size_display` properties (`models.py:877-890,893-898`) return `str` on **every** branch (f-strings / `str()` / `"-"` / `"—"` guards). No path puts a raw `None` into a segment. A real leak would reproduce deterministically at a fixed logical field — not at a drifting interior index (139) of Rich's internal buffer, inside a background thread.
- **Plain Rich threading race (no corruption)** — Rich serializes `live.update()` against its refresh thread internally and `update()` is try/except-wrapped (`tui.py`); a benign race yields a stale frame, not a `NoneType` inside `_render_buffer`, and cannot explain the co-occurring `stalled >300s` fork-deadlock signature.

## Evidence (verified `file:line`)

- `src/superclaude/cli/pipeline/process.py:189-190` — `if hasattr(os, "setpgrp"): popen_kwargs["preexec_fn"] = os.setpgrp` (the defect); `:192` `subprocess.Popen(...)`. **Sole** `preexec_fn`/`os.fork` site in `src/` (repo-wide grep).
- `src/superclaude/cli/pipeline/process.py:284-304` — `terminate()` kills via `os.getpgid(self._process.pid)` → `os.killpg(pgid, SIGTERM/SIGKILL)` (the kill path the fix must preserve).
- `src/superclaude/cli/pipeline/process.py:75` — docstring "Uses process groups (os.setpgrp) so we can kill the entire child tree" (update on fix).
- `src/superclaude/cli/pipeline/process.py:178-186` — child stdout/stderr go to **file handles**, prompt via **stdin pipe** (no controlling TTY → `setsid()` terminal-detach is benign).
- `src/superclaude/cli/sprint/tui.py:101`, `monitor.py:280-282`, `summarizer.py:339,596-599` — the live thread topology.
- `repro/boundary_fork_repro.py` — reconstructs the exact topology; `MODE=unsafe` (`preexec_fn=os.setpgrp`, lines 67-69) vs `MODE=fixed` (`start_new_session=True`, line 71), with `faulthandler` + 150 s deadlock watchdog.
- Tests: ~40 sites `patch("…process.os.setpgrp")` (harmless no-ops after fix); `tests/sprint/test_process.py:213` asserts `"preexec_fn" not in kwargs` (still holds). **No test guards fork-safety.**

## Proposed Fix (recommended)

In `src/superclaude/cli/pipeline/process.py:189-190`, replace:

```python
if hasattr(os, "setpgrp"):
    popen_kwargs["preexec_fn"] = os.setpgrp
```

with:

```python
# Detach into a new session/process-group WITHOUT running Python in the
# fork child. start_new_session=True runs setsid() in C inside
# _posixsubprocess (no preexec_fn callback), so it is fork-safe in a
# multithreaded process. setsid() makes the child a process-group leader
# (pgid == pid), so os.getpgid()/os.killpg() in terminate() are unchanged.
popen_kwargs["start_new_session"] = True
```

- **Preserves process-group kill semantics: YES.** `setsid()` ⇒ child pgid == child pid, so `os.getpgid(pid)` → `os.killpg(pgid, …)` at `process.py:284-304` targets the same child tree as before.
- **`os.setpgrp` vs `setsid` difference:** both yield pgid == pid; `setsid` *additionally* detaches the controlling terminal — irrelevant here (child uses pipes + files, not a TTY). The load-bearing difference is the **delivery mechanism**: `start_new_session=True` runs in C with no Python in the fork child; `preexec_fn` runs Python in the child (the hazard).
- Drop the `hasattr(os, "setpgrp")` guard — `start_new_session` is accepted on all POSIX and ignored where unsupported.
- Update the `process.py:75` docstring to say `setsid()` via `start_new_session`.

**Companion changes (low blast radius):** update `tests/sprint/test_process.py` to assert `start_new_session=True`; the ~40 `patch(os.setpgrp)` sites need no change. **Add a regression test** asserting `preexec_fn` is never set and `start_new_session is True` (there is currently none).

## Alternative Fixes Considered

- **Defensive `str()` coercion in TUI rendering** — *rejected as the primary fix.* It would mask the corruption symptom in one thread while leaving the heap-corruption root cause live (it can resurface as a SIGSEGV, a summarizer fork hang, or corruption elsewhere). Acceptable only as belt-and-suspenders *alongside* the fork fix, never instead of it.
- **Pause/stop the Live display during spawn** — does not address the root cause (the monitor/summarizer threads still fork under contention) and is more invasive.

## Risk + Rollback

- **Risk:** minimal. The change is C-path-equivalent for grouping and strictly safer for forking. Only semantic delta (TTY detach) is inert given the pipe/file I/O model.
- **Validate before/after:**
  `MODE=unsafe ITERS=20000 uv run python repro/boundary_fork_repro.py` → expect SIGSEGV/`TypeError`/deadlock;
  `MODE=fixed  ITERS=20000 uv run python repro/boundary_fork_repro.py` → expect `SURVIVED`.
  This repro **is** the runtime-entrypoint negative-witness (fix-reverted ⇒ FAIL).
- **Rollback:** revert the one-line change; behavior returns to the unsafe baseline.

## Next Steps

This was a diagnosis-only run (no `--fix`). To authorize the remediation chain (task-builder → `/task` → validate), re-invoke:

```
/sc:troubleshoot --depth deep --fix "TypeError sequence item NoneType in rich _render_buffer — unsafe preexec_fn=os.setpgrp fork in sprint runner"
```

Or apply the one-line change above directly and run the repro both ways plus `uv run pytest tests/sprint/test_process.py`.

## Grounding Gaps

- Tier-2 quality-engineer agent died on a 429 rate-limit; its falsification angle (process-model + test-coverage audit) was recovered inline by the orchestrator (each run is a fresh process; no fork-safety regression test exists).
- The exact corruption micro-mechanism (CoW page vs. lock-held-ownerless vs. fork-deadlock-adjacent partial read) is inherently nondeterministic; the *fix direction* does not depend on which it is. Running the repro both ways closes this gap empirically.

---

## Revised Diagnosis (2026-06-17 — after empirical repro + independent calibration)

**What changed:** the original H-A diagnosis was tested and did not hold up.

| Step | Result |
|------|--------|
| Ran `repro/boundary_fork_repro.py` MODE=unsafe (the exact `preexec_fn=os.setpgrp` path) | **SURVIVED, exit 0** — 20000 spawns + 67k forks, no crash. Prediction was "crash". |
| Ran MODE=fixed (`start_new_session=True`) | SURVIVED, exit 0 |
| Independent `confidence-calibrator` (`ae7ec4e928acec562`) re-graded H-A | **0.88 → 0.25**, verdict ESCALATE, H-A subordinate to H-C |
| Re-dispatched `quality-engineer` (`aeb78b0b30aa38f6d`) | found a verified competing mechanism (H-C) |

**New leading hypothesis — H-C (Rich redirect-IO shared-Console concurrency), UNPROVEN ~0.30-0.35:**
The TUI builds `Live(...)` with Rich's default `redirect_stdout/stderr=True` (`src/superclaude/cli/sprint/tui.py:101-106`). While Live is active, `sys.stderr` is a Rich `FileProxy` onto the TUI Console. Concurrently:
- the stall-watcher loop emits `_stall_logger.warning("Per-task subprocess stalled…")` (`executor.py:1458-1463`) — **the exact line that precedes the crash**;
- the main loop calls `print(…, file=sys.stderr)` (`executor.py:1876,1889,1915,1927,1944`) and `tui.update()` → `self._live.update(self._render())` (`executor.py:1940`, `tui.py:132`);
- the Rich refresh thread (Thread-1) renders the Console at 2 Hz.

→ multiple threads writing one `Console._buffer`. This explains the clean Python `TypeError`, the temporal coupling with the stall line, and why the repro (which never does redirected cross-thread writes) didn't reproduce. **Caveat:** rich 15.0.0 (`uv.lock:1019`, loose `>=13.0.0` floor in `pyproject.toml:37`) appears to lock-guard the buffer op, so H-C is not proven either.

**Why the clean traceback matters:** the crash is a normal Python `TypeError` through `live.py:38 → refresh → _render_buffer`, not a SIGSEGV / faulthandler C-dump. Heap corruption from an unsafe fork typically segfaults or yields garbage — not a clean `None` in a list. This is the single strongest signal, and it points at concurrency/logic, not corruption.

**Recommended next steps (in priority order):**
1. **Decisive diagnostic** — add `faulthandler.enable()` / `PYTHONFAULTHANDLER=1` to the sprint entrypoint so the *next real crash* produces a definitive Python-vs-C stack. (The existing traceback already leans Python/H-C.)
2. **Cheap fix + probe for H-C** — construct the Live with `redirect_stdout=False, redirect_stderr=False` at `tui.py:101` (route watchdog/stall output through the Console's own `print`, or a queue, instead of redirected stderr). If the crash stops, H-C is confirmed.
3. **Still do, but on principle (not as the proven fix)** — `start_new_session=True` at `process.py:189-190`. It removes a genuine documented fork-safety hazard and is behavior-preserving for `os.killpg`, but the repro shows it is **not** demonstrated to fix this crash.

**Honest status:** no hypothesis is proven. Leading = H-C (~0.30-0.35, unproven), H-A subordinate (0.25). This is a `partial` result recommending the two diagnostics above before any fix is called "the fix".
