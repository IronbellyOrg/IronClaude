<!-- PROVENANCE (harness-stamped):
agent_type: quality-engineer (re-dispatch of the failed a0b5d14a0ce7ca95d)
agentId: aeb78b0b30aa38f6d
subagent_tokens: 114786
tool_uses: 20
duration_ms: 487933
outcome: completed
persisted: verbatim from the agent's final message (turn 4); fed the repro non-reproduction result
-->

## VERDICT — Re-assessment after the repro came back inconclusive

### 1. Confidence in H-A (unsafe-fork → heap corruption)
**Plausible-but-unconfirmed, not refuted. Revised ~0.30** (down from 0.86). The repro's failure is weak evidence (`/bin/true` children, 2-row table, 42s vs the real ~27-min crash), so non-reproduction doesn't refute a corruption hypothesis. But the diagnosis overweighted H-A on an uncorroborated "it's corrupted memory" theory. H-A → background hazard.

### 2. Re-opened hypotheses
**H-C "shared mutated renderable" sub-form: REFUTED.** `tui.py:132` calls `self._live.update(self._render())`; `_render()` (`tui.py:154-197`) builds a fresh tree every call. The refresh thread never sees a half-built/mutated renderable.

**H-C credible form: redirect-IO dual-writer on one Console — SUPPORTED.** `Live.start()` enables `_enable_redirect_io()` (`rich/live.py:129`); the TUI Live uses Rich defaults `redirect_stdout/stderr=True` (`tui.py:101-106`). Watchdog `print(..., file=sys.stderr)` (`executor.py:1876-1947`) routes from the main thread into the SAME Console the refresh thread renders → two threads, one `Console._buffer` — the structural condition for a `Segment(text=None)` reaching `_render_buffer` (`rich/console.py:2141-2153`, the failing `"".join(output)`).

**Not a slam-dunk:** rich 15.0.0 guards it — `_RefreshThread.run` holds `live._lock` (`live.py:36`); `Console._check_buffer` renders+clears under `with self._lock` (`console.py:2062-2130`); `FileProxy.write` goes through `with console:`. Every writer serializes. Residual risk: `Live._lock` and `Console._lock` are different locks, but the buffer op is atomic under `Console._lock`. No proven gap — but the surface most worth instrumenting.

**No genuine None in sprint data** — re-confirmed: `MonitorState` fields (`models.py:847-874`) non-None; `_truncate` returns `""` (`tui.py:620-629`); markup is f-strings. The None is produced INSIDE Rich's buffer → consistent with H-A OR H-C, inconsistent with a plain sprint logic bug.

### 3. Rich version
**Pinned 15.0.0** (`uv.lock:1019`); floor only `>=13.0.0` (`pyproject.toml:37`). No named CVE-class Live bug known to me, but a 6-major gap between floor and lock means any `uv lock` refresh changes threading internals under this code with zero guard.

### 4. Most decisive next diagnostic
1. **Decisive:** `PYTHONFAULTHANDLER=1` / `faulthandler.enable()` in the sprint entrypoint. A C-level dump on the real crash distinguishes H-A (segfault/corrupt C state) from H-C (clean Python `TypeError` through `live.py:38 → refresh → _render_buffer`). A synthetic repro can't settle this. (Note: the user's actual traceback is already a CLEAN Python traceback — which itself leans H-C.)
2. **Cheap mitigation + probe:** build the Live with `redirect_stdout=False, redirect_stderr=False` (`tui.py:101`). Crash gone → H-C confirmed; persists → H-C eliminated, H-A regains weight.

### Bottom line
- H-A ~0.30 (latent hazard; `start_new_session=True` still worth doing on principle, unproven as cause).
- H-C co-equal (~0.30-0.35); specific form = redirect-IO dual-writer (`live.py:129`, `console.py:2062-2153`), apparently lock-guarded in rich 15.0.0.
- Verified risk surface: TUI Live default `redirect_stdout/stderr=True` (`tui.py:101-106`) + main-thread watchdog prints (`executor.py:1876-1947`).
- Decisive next step: faulthandler on the real runner + flip `redirect_*=False` at `tui.py:101`.
