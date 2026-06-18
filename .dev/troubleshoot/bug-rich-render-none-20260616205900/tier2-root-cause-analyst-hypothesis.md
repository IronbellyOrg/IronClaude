<!-- PROVENANCE (harness-stamped, not author-editable):
agent_type: root-cause-analyst
agentId: afe966873b7470410
subagent_tokens: 100572
tool_uses: 11
duration_ms: 290325
outcome: completed
persisted: post-hoc, verbatim from the agent's final message (turn 1)
-->

## HYPOTHESIS CARD

**(1) Chosen root cause — H-A: unsafe `preexec_fn=os.setpgrp` fork in a multithreaded process.**
At a phase boundary, `ClaudeProcess.start()` calls `subprocess.Popen(..., preexec_fn=os.setpgrp)` (`src/superclaude/cli/pipeline/process.py:189-190`). `preexec_fn` forces CPython down the slow fork path: the child runs arbitrary Python (`os.setpgrp` + interpreter teardown via `_posixsubprocess`) *between* `fork()` and `execvp()`. In a multithreaded parent, `fork()` clones only the calling (main) thread but copies the entire address space — including any locks held by *other* threads at the fork instant. The `None` Rich joins at segment index 139 (`rich/console.py:2153`, `"".join(output)`) is a corrupted object surfacing in the 2 Hz Live refresh thread — a non-deterministic, index-specific manifestation of heap/interpreter corruption, not a value any code path legitimately produced.

**(2) Evidence:**
- `process.py:189-190`: `if hasattr(os, "setpgrp"): popen_kwargs["preexec_fn"] = os.setpgrp` — the unsafe primitive. CPython's `subprocess` docs explicitly warn `preexec_fn` "is not safe to use in the presence of threads."
- Concurrent fork pressure: `summarizer.py:339` (`subprocess.run([claude...])`) runs inside daemon pool threads spawned at `summarizer.py:596-602`; the `OutputMonitor` daemon (`monitor.py:280-285`) polls/allocs continuously. Multiple threads contend the glibc malloc arena lock and CPython internal locks precisely when the main thread forks. A fork while another thread holds the arena lock leaves that lock *held-with-no-owner* in the child; the slow `preexec_fn` path then allocates (setpgrp wrapper, error pipe handling) → child can wedge or corrupt shared CoW pages observed by the parent.
- Negative evidence ruling out a logic bug: every TUI render helper (`tui.py` `_truncate` 620-629, `_format_bytes` 583-591, `_render_bar` 594-601, `_render_percent` 604-609, `_render_activity_stream` 416-439, `_build_active_panel` 362-414) and both `MonitorState` properties (`stall_status` models.py:877-890, `output_size_display` models.py:893-898) return `str` on *every* branch — f-strings / `str()` / `"-"` / `"—"`. No path injects raw `None` into a Rich renderable. `_render()` builds `parts` from these str-only helpers (tui.py:154-197). The `None` therefore cannot originate in app logic.
- Symptom signature matches corruption: failure is intermittent (only after long chained runs), thread-local to the Live refresh thread, and pinned to a specific buffer index (139) — deterministic logic bugs reproduce at fixed inputs, not at a drifting interior index of an internal Rich buffer.

**(3) Rejecting competitors:**
- **H-B (genuine None-leak in TUI):** Refuted by exhaustive branch inspection above — no str-typed render path returns/embeds `None`. A real leak would reproduce deterministically and would surface at the *same* logical field, not at an arbitrary join index inside Rich's segment list.
- **H-C (plain Rich threading race, no corruption):** Rich `Live` already serializes `live.update()` (main thread) against its refresh thread via an internal lock; `update()` is additionally wrapped in try/except (`tui.py:130-152`). A benign race would yield a stale/duplicated frame, not a `NoneType` inside `_render_buffer`. H-C also cannot explain why this only emerges under the chained-sprint fork load. The unsafe fork (H-A) is the necessary added ingredient that turns Rich's normally-safe threading into a corruption surface.

**(4) Confidence: 0.74.** The unsafe pattern is unambiguously present and the negative evidence cleanly excludes a logic bug; the residual uncertainty is whether the observed `None` is *strictly* CoW/lock corruption vs. a fork-deadlock-adjacent partial-state read — both are H-A failure modes, so the root cause holds even if the exact corruption mechanism differs.

**(5) If I'm wrong, it's probably because…** the `None` comes from a Rich-version-specific internal bug (e.g., a `Segment.text=None` produced by Rich's own optimizer under concurrent `update()`), making H-C the true cause and the fork merely a load amplifier rather than the corruptor.

**(6) Recommended fix:** Replace `preexec_fn=os.setpgrp` with `start_new_session=True` in `process.py:189-190`. This achieves the identical goal (child becomes a process-group/session leader, detached from the parent's pgid) but does it in the post-fork C path *without* running interpreter-level Python between fork and exec — eliminating the multithreaded-fork corruption window. **It preserves the `os.killpg` semantics in `terminate()` (`process.py:284-304`):** `start_new_session=True` makes the child a session leader whose PGID equals its PID, so `os.getpgid(child_pid)` → `os.killpg(pgid, SIG…)` still targets the whole child process group exactly as before. Validate with the existing `repro/boundary_fork_repro.py` (MODE=unsafe must fault/deadlock; MODE=fixed must survive ITERS).
