# F — STRICT-tier Review: stdin-patch delta (7 commits)

| Field | Value |
|---|---|
| Review tier | STRICT (adversarial, read-only) |
| Branch | `fix/claude-process-stdin-large-prompts` |
| HEAD under review | `fde1431` |
| Pre-delta baseline | `142ce15` |
| Reviewer | quality-engineer (sub-agent) |
| Date | 2026-04-30 |

---

## 1. Verdict

**APPROVED-WITH-NITS** — Green-light to merge into `feat/tdd-spec-merge` after acknowledging the two MEDIUM findings below. No BLOCKER or HIGH issues. The delta is tight, well-scoped, and faithful to RECONCILED_DESIGN.md §4-§5.

---

## 2. Strengths

- **Idempotent encode** at `pipeline/process.py:139-145` — `prompt.encode("utf-8")` happens exactly once per `start()` call and is cached on `self._prompt_bytes`, eliminating the double-encode trap that DESIGN.md §4 warned about.
- **Pre-spawn ordering is correct**: size check at `:140-144` runs before file open (`:147-152`), before `Popen` (`:163`), before `_write_prompt_to_stdin` (`:176`). T-004 enforces this with explicit assertions on both `proc._process is None` and `not out_file.exists()` (`test_process_stdin.py:148-150`).
- **`PromptTooLargeForArgv(ValueError)`** subclassing (`pipeline/process.py:32`) is the right backward-compat shape; T-004 pins `isinstance(excinfo.value, ValueError)` at `test_process_stdin.py:146`. Callers catching either ValueError or PromptTooLargeForArgv keep working.
- **EINTR retry loop** (`pipeline/process.py:209-215`) reassigns `chunk` on each outer-while iteration via `view[offset:offset + _STDIN_CHUNK_SIZE]` — the slice is recomputed after each successful partial write, so `chunk` cannot go stale across an EINTR retry.
- **`finally: stdin.close()`** at `pipeline/process.py:225-229` guarantees EOF delivery to `claude --print` even if the os.write loop is broken by an unexpected `OSError`, BrokenPipe, or KeyboardInterrupt.
- **Portify anchor** (`cli_portify/process.py:214-219`) is structurally sound: the base `build_command()` at `pipeline/process.py:108-110` emits `--output-format` unconditionally; T-008 (`test_process_stdin.py:48-68`) pins both adjacency and the `-p`-not-in-cmd invariant.
- **Test-strength layering**: T-008 covers shape, T-009 covers shape + 200 KB round-trip via `_stdin_echo_argv` stand-in, T-010 covers idempotency. Together they kill the obvious regression class (re-introducing `cmd.index("-p")`) and the subtle one (stateful `build_command()` accretion).

---

## 3. Issues found

### MEDIUM-1 — `PrdClaudeProcess.terminate()` does not surface `_stdin_error`

**Citation**: `src/superclaude/cli/prd/process.py:239-279`

`PrdClaudeProcess` overrides `terminate()` (5s grace per F-004 instead of 10s base) but the override is a near-clone of the base method that predates P-004. It does NOT include the `getattr(self, "_stdin_error", None)` log surfacing block that the base added at `pipeline/process.py:288-291`. Result: a PRD pipeline subprocess that hits BrokenPipe during stdin write and then SIGTERMs will silently swallow the stdin error.

**Suggested fix**: Add the same 4-line `if getattr(self, "_stdin_error", None) is not None: _log.warning(...)` block immediately before `if self._on_exit is not None:` at `prd/process.py:277`. Alternatively (preferred), refactor base `terminate()` to factor the surfacing+on_exit+_close_handles tail into a helper and have the override call it. Out of scope for this delta but should be tracked.

**Severity rationale**: PRD pipeline is in active use. Silent BrokenPipe swallowing was the exact failure mode P-004 was meant to fix. MEDIUM not HIGH because base `wait()` still surfaces it if `terminate()` is followed by `wait()` (and `wait()` is not overridden in PRD), so observability is degraded but not lost in the common path.

---

### MEDIUM-2 — `int(os.environ.get(...))` crashes on non-numeric `SUPERCLAUDE_PROMPT_MAX_BYTES`

**Citation**: `src/superclaude/cli/pipeline/process.py:27-29`

```python
PROMPT_MAX_BYTES: int = int(
    os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024)
)
```

If an operator sets `SUPERCLAUDE_PROMPT_MAX_BYTES=16MB` (or any non-numeric), `int()` raises `ValueError` at module import — every `from superclaude.cli.pipeline.process import …` in the codebase blows up before any code can run. This is a fail-shut footgun. RECONCILED_DESIGN.md §4 P-002 spec did not require try/except, but operator hostility argues for one.

**Suggested fix**:
```python
def _resolve_prompt_max_bytes() -> int:
    raw = os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")
    if raw is None:
        return 16 * 1024 * 1024
    try:
        return int(raw)
    except ValueError:
        _log.warning("ignoring non-numeric SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)
        return 16 * 1024 * 1024
PROMPT_MAX_BYTES: int = _resolve_prompt_max_bytes()
```

**Severity rationale**: The 16 MiB default ships unchanged for 100% of users today. Only operators who deliberately set the env var hit this. MEDIUM not LOW because a typo in a Dockerfile or systemd unit silently breaks the entire pipeline at import time, which is hostile.

---

### LOW-1 — `_stdin_error` not reset between successive `start()` calls on a reused instance

**Citation**: `src/superclaude/cli/pipeline/process.py:175`

`self._stdin_error: Optional[BaseException] = None` is set inside `start()` *after* the size guard and right before `_write_prompt_to_stdin`. This means it IS reset on every `start()` — so the worry is unfounded for that path. **However**, if a caller happens to read `proc._stdin_error` between `start()` calls (unlikely but technically possible — `wait()`/`terminate()` already log it), they would see stale state from the prior call until the next `start()` runs. No current caller does this. Note for the record only.

**Suggested fix**: Optionally move `self._stdin_error = None` into `__init__` so the attribute exists from construction. Would simplify the `getattr(..., None)` defensive read at `:240` and `:288` to a plain attribute access.

---

### LOW-2 — `n == 0` from `os.write` breaks the loop silently with no error

**Citation**: `src/superclaude/cli/pipeline/process.py:216-218`

```python
if n <= 0:
    # Defensive -- os.write should not return 0 on a pipe.
    break
```

Per POSIX, `write(2)` returning 0 on a pipe is "should not happen" but if it ever does, the current code exits the while loop silently with the prompt half-written and no `_stdin_error` set. The child gets a truncated prompt + EOF and would likely fail with a confusing "couldn't parse JSON" error. The `n < 0` case cannot occur (Python raises OSError instead), so the `<=` is defensive-but-unreachable for the negative branch.

**Suggested fix**: Set `self._stdin_error = OSError(f"unexpected zero-byte write at offset {offset}/{len(view)}")` before the `break`. The probability is near-zero but the cost of capturing it is one line.

---

### NIT-1 — T-011 risks being a silent no-op on fast machines

**Citation**: `tests/pipeline/test_process_stdin.py:280-285`. The soft `if proc._stdin_error is not None` shape is correct (avoids flake), but if the 1 MB buffer fits before the child exits, neither branch fires and the test passes without exercising anything. **Fix**: assert that either `_stdin_error` is set OR `out_file` consumed all 1 MB.

### NIT-2 — T-005 timer fires before `start()`

**Citation**: `tests/pipeline/test_process_stdin.py:230-234`. Timer is scheduled before `proc.start()` runs Popen. If the 0.5s timer fires while `_process is None`, `terminate()` is a noop and `wait()` falls through to its 18s timeout. Pipe-fill happens in <100ms in practice so this is theoretical. **Fix**: `start()` first, then schedule timer.

### NIT-3 — `build_command()` called twice per `start()`

**Citation**: `pipeline/process.py:163` and `:184`. Once for Popen, once for the debug log slice. For PortifyProcess this re-runs the dual-`--add-dir` logic. Idempotent (T-010 confirms) but wasted work. **Fix**: cache once, reuse.

---

## 4. Pre-existing issues observed (NOT regressions)

### 4.1 — Sprint test fixtures broken since `4799719`

**Evidence**: 64 tests in `tests/sprint/` fail with `AttributeError: '_KillPopen' object has no attribute 'stdin'`. Verified to fail identically against pre-delta baseline `142ce15`. The mock surface in sprint tests was not updated when `4799719` (Apr 20, 2026) added `subprocess.PIPE` for stdin — a missing-mock bug that has been silently broken for ~10 days. **Not caused by this delta**, but worth filing as a follow-up.

**Recommendation**: Open a separate issue: "sprint test `_KillPopen` mock missing `stdin` attribute (regressed in 4799719)". Out of scope for this PR.

### 4.2 — `cleanup_audit/executor.py` calls non-existent `is_running()` / `stop()`

**Evidence**: `src/superclaude/cli/cleanup_audit/executor.py:91` calls `process.is_running()` and analogous `stop()` calls elsewhere. `CleanupAuditProcess` (`cleanup_audit/process.py:22`) extends `_PipelineClaudeProcess` which has neither method. RECONCILED_DESIGN.md §3.2 explicitly marks this as out-of-scope ("orthogonal bug"). Will fail at runtime when cleanup_audit is invoked, but the codepath is rarely exercised.

**Recommendation**: Already tracked as task #15 in this session's task list ("file GH issue").

---

## 5. Adversarial questions answered

### Q1 — Could `_write_prompt_to_stdin` busy-loop on `n == 0`?

**A**: No. Lines `pipeline/process.py:216-218` break the outer while when `n <= 0`. There is no spin. See LOW-2 above for the orthogonal observability concern.

### Q2 — What happens if `os.write` raises `BlockingIOError` (non-blocking FD)?

**A**: `subprocess.PIPE` produces a blocking FD by default on POSIX (Python's `subprocess` does not call `fcntl.F_SETFL O_NONBLOCK`). `BlockingIOError` would only arise if a future change adds non-blocking somewhere, in which case it would propagate out of `_write_prompt_to_stdin` since `BlockingIOError` is a subclass of `OSError` — caught at `:223` and stored in `_stdin_error`. Tolerable. Not a hot issue.

### Q3 — Does the `finally: stdin.close()` run even on `KeyboardInterrupt`?

**A**: Yes. Python's `try/finally` semantics guarantee `finally` runs on any exception including BaseException subclasses (KeyboardInterrupt, SystemExit). Verified by reading the loop at `pipeline/process.py:204-229`. The only escape that skips `finally` is a hard segfault or `os._exit`, neither relevant.

### Q4 — Is `_prompt_bytes` always set before `_write_prompt_to_stdin` reads it?

**A**: Yes, mechanically. `_prompt_bytes` is set at `pipeline/process.py:145`, *before* `_write_prompt_to_stdin(self._prompt_bytes)` at `:176`. The size guard at `:140-144` raises before the assignment, so if the guard fires, neither the assignment nor the write happens — and `start()` returns via exception. No reuse-instance hazard: every `start()` re-encodes and re-assigns.

### Q5 — Sprint subclass — does it call `super().start()`?

**A**: It does not override `start()` at all. `sprint/process.py:88-121` only defines `__init__` and `build_prompt`. All lifecycle methods are inherited from base `ClaudeProcess`. Confirmed by `grep -n "def start" sprint/process.py` returning nothing. PrdClaudeProcess overrides `terminate()` but not `start()` (see MEDIUM-1). PortifyProcess overrides `build_command()` but not `start()`. Net: P-003 + P-004 take effect for every concrete subclass.

### Q6 — Does the Portify anchor's `except ValueError` branch ever execute?

**A**: It is unreachable in practice. Base `build_command()` at `pipeline/process.py:108-110` emits `"--output-format"` unconditionally. The `# pragma: no cover` annotation on the except branch (`cli_portify/process.py:218`) acknowledges this. T-008 (`test_process_stdin.py:63-68`) pins `--output-format` adjacency. The only way to break this is to remove `--output-format` from the base, which T-008 would catch.

### Q7 — If `PROMPT_MAX_BYTES` is set to 0 by a hostile env var, can a 0-byte prompt still pass?

**A**: Edge case. At `pipeline/process.py:140`: `if len(prompt_bytes) > PROMPT_MAX_BYTES`. With `PROMPT_MAX_BYTES=0` and `prompt=""`, `len(b"") > 0` is False — passes. With `prompt="x"`, fails (raises). Behavior is "0 means disable empty prompts only," which is non-obvious but not a bug. T-006 (`test_process_stdin.py:245-260`) covers the empty-prompt path with the default cap.

---

## 6. Test strength assessment

| Dimension | Score (1-5) | Notes |
|---|---|---|
| **Thoroughness** | 4 | All 5 patches have at least one test. T-002/T-003 round-trip, T-004 pre-spawn, T-005 SIGTERM safety, T-006 empty, T-007 dual mode, T-008-T-010 anchor, T-011 BrokenPipe. T-001 is the load-bearing argv invariant. |
| **Edge cases** | 4 | Empty (T-006), 4-byte UTF-8 (T-003), 1 MB BrokenPipe (T-011), exact-cap boundary (T-004 second method asserts `1024` exactly equals cap not raises). Missing: prompt with embedded NUL bytes; prompt with stdin pre-closed by parent. Both very theoretical. |
| **Mutation kill rate** | 4 | A reviewer regressing `cmd.index("-p")` is caught by T-008. Removing `finally: close()` would not fail any current test (the EOF expectation only matters for live `claude` not the echo stand-in) — gap. Removing the EINTR retry would not fail any current test either — pytest doesn't reliably deliver signals during the os.write window. Both are low-likelihood regressions. |
| **Determinism** | 4 | T-005 has the timer-before-start race (NIT-2) but it's <0.1% flake odds. T-011's soft assertion is correctly defended. No sleep-based polls in tests. |
| **Overall** | **4 / 5** | Strong. Could be 5/5 with a NUL-byte test, a `--no-finally-close` mutation-kill test, and the T-005 reorder. |

---

## 7. Final recommendation

**MERGE INTO `feat/tdd-spec-merge`** as-is. The two MEDIUMs are real but neither is a blocker:

- **MEDIUM-1** (PrdClaudeProcess.terminate observability gap) is pre-existing degradation amplified by P-004. Track as a follow-up issue scoped to PRD subsystem.
- **MEDIUM-2** (env var crash on non-numeric) is a footgun for ~3 operators. Trivial 5-line fix; can land in a follow-up commit on the same branch before merge if desired.

### Pre-merge requirements (none blocking)

1. **Optional**: harden `PROMPT_MAX_BYTES` parsing per MEDIUM-2.
2. **Optional**: add LOW-1 reset-in-`__init__` for `_stdin_error`.
3. **Required for record**: open follow-up issues for §4.1 (sprint mock) and §4.2 (cleanup_audit). Already tracked as task #15.

### What this delta does NOT need before merge

- No additional tests (4/5 strength is appropriate for the risk profile).
- No PRD subsystem changes (out of scope; tracked separately).
- No documentation beyond the existing DESIGN.md banner and reconciliation matrix.

The delta is **APPROVED-WITH-NITS**. Ship it.

---

## Appendix — Commit-by-commit verdict

| SHA | Patch | Verdict | Notes |
|---|---|---|---|
| `526a606` | P-001 Portify anchor | ✓ APPROVED | Tight 4-line change. T-008/T-009/T-010 are sufficient. |
| `c42139b` | P-002 constants + exception | ✓ APPROVED-WITH-NIT | See MEDIUM-2 (env parse). |
| `be46520` | P-003 pre-spawn guard | ✓ APPROVED | T-004 pins ordering correctly. |
| `5a8e5e7` | P-004 chunked write | ✓ APPROVED-WITH-NITS | See LOW-1, LOW-2; MEDIUM-1 is in PrdProcess not this commit. |
| `01cf2ef` | T-007 tool_write_mode | ✓ APPROVED | Pins both branches; correct cleanup-via-`with_suffix`. |
| `dda68d9` | T-001 argv invariant | ✓ APPROVED | Strong load-bearing test. |
| `fde1431` | DESIGN.md banner | ✓ APPROVED | Documentation only. |
