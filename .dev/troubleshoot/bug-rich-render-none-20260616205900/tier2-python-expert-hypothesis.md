<!-- PROVENANCE (harness-stamped, not author-editable):
agent_type: python-expert
agentId: a8821c2d8fa598ac9
subagent_tokens: 92152
tool_uses: 8
duration_ms: 439236
outcome: completed
persisted: post-hoc, verbatim from the agent's final message (turn 1)
-->

All grounding confirmed. `process.py:190` is the ONLY `preexec_fn`/`os.fork` site in `src/` (non-test). Here is the card.

---

## HYPOTHESIS CARD — H1: Multithreaded `preexec_fn` fork corruption

**Chosen root cause**
`ClaudeProcess.start()` at `src/superclaude/cli/pipeline/process.py:189-190` passes `preexec_fn=os.setpgrp` to `subprocess.Popen`. In CPython, `preexec_fn` forces the slow, fork-unsafe code path: the child runs arbitrary Python (the callback) *between* `fork()` and `exec()`. When the parent is multithreaded — which the sprint runner provably is at a phase boundary — the forked child holds copies of locks (glibc malloc arena lock, CPython internal locks/GIL state) that were held by *other* threads at the instant of `fork()`. The child is a single-threaded copy where those owner threads no longer exist, so any allocator or interpreter operation in the callback window can deadlock or run against a corrupted heap. The `TypeError: expected str ... NoneType found at item 139` in the Rich refresh thread (Thread-1) and the "stalled >300s" precursor are the two canonical surface symptoms of this single defect (heap corruption vs. fork deadlock).

**Evidence (cited)**
- `src/superclaude/cli/pipeline/process.py:189-190` — `if hasattr(os,"setpgrp"): popen_kwargs["preexec_fn"]=os.setpgrp`, then `subprocess.Popen(...)` at `:192`. This is the **only** `preexec_fn`/`os.fork` site in `src/` (non-test) — verified by repo-wide grep.
- Concurrent live threads proven present at spawn time: Rich `Live(refresh_per_second=2)` background refresh thread `src/superclaude/cli/sprint/tui.py:101`; `output-monitor` daemon `src/superclaude/cli/sprint/monitor.py:280-283`; `summary-worker-p{n}` daemon(s) `src/superclaude/cli/sprint/summarizer.py:595-599` whose `_run` forks via `subprocess.run` at `:339`. The monitor and summarizer daemons are heavy `subprocess`/allocation users → the malloc arena lock is hot precisely when `Popen` forks.
- **CPython semantics (Q1):** The `subprocess` docs explicitly warn that `preexec_fn` "is not safe to use in the presence of threads" because between `fork()` and `exec()` only async-signal-safe operations are permitted, yet the callback executes interpreter-level Python (which mallocs, may touch the import lock, GIL state). POSIX `fork()` in a multithreaded process duplicates only the calling thread but **all** mutexes in their current (possibly-locked) state → classic locked-mutex-with-dead-owner. CPython gates `preexec_fn` behind the pure-`fork`+manual-`exec` path in `_posixsubprocess`, *disabling* the vfork/`posix_spawn` fast path that otherwise avoids running Python in the child.
- **Repro (Q2 support):** `repro/boundary_fork_repro.py` reconstructs the exact thread topology (Rich Live + malloc-churn monitor + 3 concurrent-fork summarizer daemons + main-thread `Popen`) and toggles `preexec_fn=os.setpgrp` (`MODE=unsafe`, lines 67-69) vs `start_new_session=True` (`MODE=fixed`, line 71), with `faulthandler` + a 150s deadlock watchdog to capture either failure mode.

**Q2 — parent-side vs child-side corruption (the load-bearing distinction)**
The corruption that crashes Thread-1 is **parent-side**, and it is credible. The mechanism is *not* the child writing the parent's memory (separate address spaces post-fork). It is: at the moment `Popen` calls `fork()`, another parent thread (monitor/summarizer/Rich) holds the glibc malloc arena lock mid-mutation. In a *clean* fork the parent's own copy of that lock and heap is fine. The danger is the **interaction of repeated unsafe forks under contention**: the summarizer daemons themselves fork concurrently, and a fork while *another thread* is inside `malloc`/`free` can leave the **parent's** arena in an inconsistent state if the unsafe path's child manipulates shared glibc state before exec, or if a fork lands mid-arena-update and the `atfork` handlers are bypassed by the raw callback path. The observable result — a `str` object whose internal `ob_sval`/pointer reads back as `None`/garbage at a specific index (139) inside `"".join(output)` in an unrelated thread — is the textbook fingerprint of heap/object corruption rather than any application logic, which the grounding confirms can never emit `None` into a segment. So: **child-side** would manifest as a crash/hang of the spawned `claude` (or the summarizer fork); the **parent-side** Thread-1 `TypeError` is consistent with allocator-state corruption induced by fork-under-lock-contention. Confidence on the *direction of fix* is high; confidence on the precise corruption micro-mechanism is medium (it is inherently nondeterministic).

**Q3 — `start_new_session=True` is the correct fork-SAFE replacement (yes)**
- CPython implements `start_new_session=True` **in C inside `_posixsubprocess.fork_exec`**: it calls `setsid()` in the child after fork, before exec, with **no Python callback** — it does not force the `preexec_fn` slow path and remains compatible with the vfork/`posix_spawn`-style hardened path. No arbitrary Python runs in the child window.
- Termination semantics are **preserved identically**: `setsid()` makes the child a new **session and process-group leader**, so its **pgid == child pid**. The existing path `os.getpgid(self._process.pid)` → `os.killpg(pgid, SIGTERM/SIGKILL)` (`process.py:284-308`) therefore targets exactly the child's own group and its descendants — the same tree `os.setpgrp` produced. (`os.setpgrp()` no-arg on Linux == `setpgrp(0,0)` == `setpgid(0,0)`: new **process group** in the *same session*, pgid==pid. `setsid()`: new **session + process group**, pgid==pid, **and detaches the controlling terminal**.) For pgid-based killing the two are equivalent; `killpg` works the same.
- **Semantic difference that matters here and is actually benign:** `setsid()` additionally drops the controlling terminal. The runner redirects child stdout/stderr to real **file handles** (`process.py:178-181, 185-186`) and feeds the prompt via **stdin pipe** (`:184, :205`), not a TTY — so losing the controlling terminal has no functional effect. The only theoretical risk (a child that wants TTY/job-control signals) does not apply to `claude --print` driven over pipes+files.

**Q4 — other unsafe fork sites: none**
- `summarizer.py:339` `subprocess.run([...], stdin=DEVNULL, stdout=PIPE, stderr=PIPE, ...)` sets **no `preexec_fn`** → it uses CPython's safe C-level fork/exec (no Python in child). It is *not* a corruption source itself, but it is a **contention amplifier**: as a concurrently-forking daemon it keeps the arena lock hot, raising the probability that the `process.py:190` unsafe fork lands at a bad moment.
- Repo-wide grep confirms `process.py:190` is the **sole** `preexec_fn`/`os.fork` occurrence in `src/` (non-test). All other `subprocess.run`/`Popen` sites (tmux.py, notify.py, preflight.py, prd/process.py, etc.) use the safe C path with no callback.

**Confidence: 0.88**
High on the fix direction and CPython semantics; the residual 0.12 is the nondeterministic corruption mechanism (Q2) — I cannot deterministically prove the specific `str`→`None` corruption derives from this fork vs. a coincident Rich/threading bug without the repro's `MODE=unsafe` actually reproducing a SIGSEGV/`TypeError` and `MODE=fixed` surviving.

**If I'm wrong, it's because…**
the `TypeError` originates in Rich's own `Live` auto-refresh racing with `live.update()` from the main thread (a Rich thread-safety issue independent of fork) — in which case `start_new_session=True` would silence the *stall* but the Thread-1 `TypeError` would persist. The discriminator is the repro: if `MODE=fixed` still throws the `TypeError`, the root cause is Rich concurrency, not fork safety. The "stalled >300s" precursor (a fork-deadlock signature) argues against the pure-Rich explanation.

**Fix recommendation (precise)**
In `src/superclaude/cli/pipeline/process.py:189-190`, replace the `preexec_fn` block with:
```python
popen_kwargs["start_new_session"] = True
```
(drop the `if hasattr(os,"setpgrp")` guard; `start_new_session` is accepted on all POSIX and silently ignored on platforms without `setsid`, and is harmless on Windows where `os.setpgrp` was absent anyway). Update the docstring at `process.py:75` ("Uses process groups (os.setpgrp)…") to say `setsid()` via `start_new_session`.
- **Preserves process-group kill semantics: YES** — child becomes pgid==pid group/session leader; `os.getpgid`/`os.killpg` at `:284-308` are unchanged and target the same tree.
- **`os.setpgrp` (no-arg) vs `os.setsid` difference here:** functionally equivalent for pgid-based group kill (both yield pgid==pid); `setsid` additionally creates a new session and detaches the controlling terminal — irrelevant because the child uses pipes+files, not a TTY. The decisive difference is **not** the syscall's grouping behavior but the **delivery mechanism**: `start_new_session=True` runs `setsid()` in C with no Python in the fork child, eliminating the multithread-fork hazard, whereas `preexec_fn=os.setpgrp` forces the unsafe Python-in-child path.

**Validate with:** `MODE=unsafe ITERS=20000 uv run python repro/boundary_fork_repro.py` (expect SIGSEGV/`TypeError`/deadlock) vs `MODE=fixed ITERS=20000 uv run python repro/boundary_fork_repro.py` (expect SURVIVED).
