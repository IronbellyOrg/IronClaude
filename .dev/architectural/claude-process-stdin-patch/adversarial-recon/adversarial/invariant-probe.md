# Round 2.5 — Invariant Probe / Independent Fault-Finder

**Role**: Independent fault-finder. Not advocating for either side. Probes the EMERGING CONSENSUS between R1-impl and R1-spec for invariant violations.
**Scope**: 5-category invariant checklist applied to the consensus surface.
**Method**: Direct source read of `pipeline/process.py`, `cli_portify/process.py`, `prd/process.py`, plus the test file. No advocate framing trusted.

---

## Method note

Both R1 advocates concede:
- The 5 patches landed mechanically (P-001 through P-005).
- All 11 T-NNN tests exist with structurally correct mocking.
- `4799719` + `39d5100` survived (always-stdin + tool_write_mode preserved).
- The "22 unique-to-B unimplemented" headline is mostly process artefacts.
- U-007 (asymmetric `_stdin_error` defensive read), X-004 (missing log token), X-006 (conditional T-011 assertion) are real drifts.

The probe targets THIS consensus surface. F's STRICT review (`F-strict-review.md`) is read at this stage to identify items F missed (`[NEW vs F]`) and items both probes confirm (`[also F]`).

---

## Findings table

| INV-NNN | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| **INV-001** | State Variables | `self._stdin_error` is reset at every `start()` so successive calls don't carry stale state | ADDRESSED | LOW | `pipeline/process.py:175` sets `self._stdin_error = None` on every `start()` entry, after the size guard but before `_write_prompt_to_stdin`. **`[also F]` LOW-1.** |
| **INV-002** | State Variables | `self._stdin_error` exists as an attribute on instances that have never called `start()` (e.g., `terminate()` after constructor failure) | UNADDRESSED | MEDIUM | `__init__` (`pipeline/process.py:56-90`) does NOT initialize `_stdin_error`. `wait()` at `:240` reads it via `getattr(..., None)` (safe). `terminate()` at `:288` reads it via `getattr(..., None)` (safe). **But** R1's drift U-007 noted that `wait()` previously used direct attribute access — and a *future* refactor that drops the `getattr` defence on either path AttributeErrors. Initializing `self._stdin_error = None` in `__init__` would make this structurally safe. **`[also F]` LOW-1, but elevated to MEDIUM here because the future-refactor risk is real.** |
| **INV-003** | State Variables | `self._prompt_bytes` is always set before any code path reads it | ADDRESSED | LOW | Set unconditionally at `pipeline/process.py:145` before `_write_prompt_to_stdin(self._prompt_bytes)` at `:176`. The size guard at `:140-144` raises BEFORE `:145`, so if it fires neither assignment nor read happens. F Q4 confirms. **`[also F]`.** |
| **INV-004** | State Variables | All subclasses (PrdClaudeProcess, sprint.ClaudeProcess, PortifyProcess, CleanupAuditProcess) inherit P-004's `_stdin_error` surfacing on terminate/wait | UNADDRESSED | HIGH | `prd/process.py:239-279` overrides `terminate()` as a near-clone of pre-P-004 base; missing the `if getattr(self, "_stdin_error", None) is not None: _log.warning(...)` block before `_close_handles()` at `:279`. **`[also F]` MEDIUM-1, but elevated to HIGH** — under SIGTERM-only paths (executor calls `terminate()` then exits without calling `wait()`), PRD silently swallows BrokenPipe. This was the exact failure mode P-004 was authored to fix. |
| **INV-005** | State Variables | `_stdout_fh` and `_stderr_fh` are always closed exactly once, even if `start()` raises mid-flight | UNADDRESSED | MEDIUM | If `_write_prompt_to_stdin` raises an unexpected non-OSError exception (e.g., `MemoryError`, `KeyboardInterrupt`), it propagates out of `start()` because the inner try/except only catches `BrokenPipeError`/`OSError` (`pipeline/process.py:220-224`). The `_stdout_fh`/`_stderr_fh` opened at `:149-152` leak. `_close_handles()` is only called from `wait()`/`terminate()`. **`[NEW vs F]`** — F did not test this path. |
| **INV-006** | Guard Conditions | Pre-spawn size guard runs before any side effect (file open, Popen, fork) | ADDRESSED | LOW | `pipeline/process.py:135` (mkdir) runs first, but mkdir is idempotent and doesn't open file handles. Guard at `:140-144` runs before `open()` at `:149/:151` and before `Popen` at `:163`. T-004 pins this with `not out_file.exists()` assertion. **`[also F]` Strengths.** |
| **INV-007** | Guard Conditions | `_close_handles()` is safe to call when `_stdout_fh` / `_stderr_fh` are still `None` | ADDRESSED | LOW | `pipeline/process.py:319-324` iterates the tuple and `if fh is not None: try: fh.close() except: pass`. Safe under all init paths. |
| **INV-008** | Guard Conditions | `validate_tool_write_output()` is only meaningful after the subprocess exits | ADDRESSED | LOW | Docstring at `:298` documents this; method is read-only and side-effect-free. T-007 calls it after `wait()`. |
| **INV-009** | Guard Conditions | `int(os.environ.get(...))` cap parsing accepts only numeric strings | UNADDRESSED | MEDIUM | `pipeline/process.py:27-29` calls `int(...)` directly. Non-numeric env (e.g. `"16MB"`, `"unlimited"`) raises `ValueError` at module-import time, breaking every consumer. **`[also F]` MEDIUM-2.** |
| **INV-010** | Guard Conditions | `PROMPT_MAX_BYTES = 0` is rejected or documented | UNADDRESSED | LOW | `pipeline/process.py:140` uses `>` not `>=`; with cap=0, empty prompt passes (correctly), any non-empty prompt fails. The semantics "0 means disable non-empty prompts only" are undocumented and surprising. **`[also F]` Q7.** |
| **INV-011** | Guard Conditions | `PROMPT_MAX_BYTES < 0` (negative env value) is rejected | UNADDRESSED | LOW | A negative cap (`SUPERCLAUDE_PROMPT_MAX_BYTES=-1`) parses as `int(-1)` and `len(b"") > -1` is True — every prompt including empty raises `PromptTooLargeForArgv`. Hostile env breaks every call. **`[NEW vs F]`** — F did not consider negative caps. |
| **INV-012** | Count Divergence | Chunk loop `view[offset:offset + _STDIN_CHUNK_SIZE]` correctly handles the final partial chunk | ADDRESSED | LOW | Python slicing clamps to `len(view)`; final chunk is `view[N*chunk:end]` where `end = len(view)`. `os.write` writes the partial bytes; `n` returns the actual written count; `offset += n` advances; outer `while offset < len(view)` exits. Verified by T-002 (400 KB) and T-003 (200 KB UTF-8) round-trips. **`[also F]` Strengths.** |
| **INV-013** | Count Divergence | Partial-write `n < len(chunk)` correctly resumes at offset+n on next iteration | ADDRESSED | LOW | `pipeline/process.py:208-219`: outer while loops on `offset < len(view)`; inner while breaks on first non-EINTR `os.write` return; `offset += n` advances by actual written bytes. Each new outer iteration recomputes `chunk = view[offset:offset+CHUNK]`. Mathematically correct for any `0 < n ≤ len(chunk)`. |
| **INV-014** | Count Divergence | `n == 0` from `os.write` is captured as an error (not silently truncated) | UNADDRESSED | MEDIUM | `pipeline/process.py:216-218`: `if n <= 0: break`. Loop exits silently with prompt half-written, no `_stdin_error` set, child receives truncated prompt + EOF. **`[also F]` LOW-2 — F flagged this as LOW; raised here to MEDIUM** because a truncated prompt arriving at `claude --print` produces a confusing downstream JSON-parse error with no log breadcrumb pointing at the truncation. F's suggested one-line `_stdin_error = OSError("zero-byte write at offset N/M")` would close it. |
| **INV-015** | Count Divergence | T-001's argv ceiling (4 KiB) holds when `extra_args` is large | ADDRESSED | LOW | `pipeline/process.py:113` `cmd.extend(self.extra_args)` — if a caller passes a 4 KB+ `extra_args` element, T-001 fails (correctly). T-001 uses `ClaudeProcess(prompt=huge)` with default `extra_args=[]`, so the test only verifies the prompt-not-in-argv invariant. A future caller passing huge `extra_args` would fail T-001 if re-run; the live code path is unprotected. **`[NEW vs F]`** — F did not probe `extra_args` size invariants. |
| **INV-016** | Collection Boundaries | Empty prompt (`prompt=""`) writes 0 bytes + EOF cleanly | ADDRESSED | LOW | `pipeline/process.py:139` encodes `""` to `b""`; `:140` `len(b"") > PROMPT_MAX_BYTES` is False; `_write_prompt_to_stdin(b"")` enters `view = memoryview(b"")` which has `len == 0`, the outer `while offset < 0` is False, no write occurs, `finally: stdin.close()` delivers immediate EOF. T-006 pins. **`[also F]` Strengths.** |
| **INV-017** | Collection Boundaries | Single-byte prompt is handled correctly (smaller than chunk size) | ADDRESSED | LOW | Single-byte payload: outer while runs once with `chunk = view[0:1]`, `n=1`, `offset=1`, exits. No tests pin this specifically, but T-002 (400 KB) and T-006 (0 bytes) bracket it. |
| **INV-018** | Collection Boundaries | Prompt at exactly `PROMPT_MAX_BYTES` passes the guard | ADDRESSED | LOW | `pipeline/process.py:140` uses `>` not `>=`. T-004's second method `test_prompt_under_cap_passes_guard` exercises exactly-at-cap (1024 bytes when cap=1024) — passes. |
| **INV-019** | Collection Boundaries | NUL bytes (`\x00`) in prompt round-trip via stdin without truncation | UNADDRESSED | LOW | `os.write` is binary-safe; `memoryview` is binary-safe; no test pins it. A future refactor that introduces a string conversion in the chunk path would silently truncate at first NUL. **`[NEW vs F]`** — F's "Edge cases" §6 noted "Missing: prompt with embedded NUL bytes" but rated it 4/5 not as a finding. Raised here as a real mutation-kill gap. |
| **INV-020** | Collection Boundaries | `extra_args` as a single-element list inserts at correct position | ADDRESSED | LOW | `pipeline/process.py:113` `cmd.extend(self.extra_args)` — for a single-element extra_arg, `cmd` ends with that element after `--output-format <value>`. PortifyProcess anchor at `index('--output-format') + 2` lands BEFORE the `extra_args`, which is correct. |
| **INV-021** | Collection Boundaries | Empty `extra_args` (the default) does not break the anchor | ADDRESSED | LOW | `extra_args = []` is the default; `cmd.extend([])` is a no-op; anchor index unchanged. |
| **INV-022** | Collection Boundaries | `_consolidated_dirs` empty list does not break PortifyProcess anchor | ADDRESSED | LOW | `cli_portify/process.py:198-201`: empty `_consolidated_dirs` adds zero `--add-dir` flags; `add_dirs` is just `[work_dir, workflow_path]`; anchor splices 4 elements in (`--add-dir`, path, `--add-dir`, path); T-008 pins the 2-flag count when work_dir == workflow_path is not the case. |
| **INV-023** | Interaction Effects | tool_write_mode + chunked write + BrokenPipe surfaces correctly | UNADDRESSED | MEDIUM | T-007 (`tool_write_mode=True`) does not exercise BrokenPipe; T-011 (BrokenPipe) does not exercise `tool_write_mode=True`. The interaction is mechanically straightforward (the stdin write is invariant w.r.t. tool_write_mode), but no test pins it. A future refactor that opens the `.log` sidecar after the stdin write — and lets a BrokenPipe close the pipe before the sidecar opens — would leak the sidecar fh. **`[NEW vs F]`** — F did not test the tool_write_mode × BrokenPipe combination. |
| **INV-024** | Interaction Effects | PortifyProcess + huge prompt + `extra_args` containing `--output-format` would shift the anchor | UNADDRESSED | LOW | `cli_portify/process.py:215` calls `cmd.index("--output-format")` which returns the FIRST occurrence. If a caller passes `extra_args=["--output-format", "json"]`, the base `build_command()` adds the second `--output-format` AFTER `cmd.extend(self.extra_args)` at `pipeline/process.py:113`. PortifyProcess anchors on the first (correct) occurrence. **But** if a future change reorders `cmd.extend(self.extra_args)` to before `--output-format`, the anchor would land at the *extra_args* `--output-format`, splicing add-dir flags at the wrong position. T-010 idempotency test passes either way; T-008 adjacency only tests `cmd[anchor+1] == "text"`. **`[NEW vs F]`** — F's Q6 only checked the unreachability of the except branch, not the multi-occurrence case. |
| **INV-025** | Interaction Effects | PrdClaudeProcess.terminate() + new `_stdin_error` capture interact correctly | UNADDRESSED | HIGH | Same evidence as INV-004. PRD's terminate at `prd/process.py:239-279` is a clone-without-merge; the `_stdin_error` capture happens in base `_write_prompt_to_stdin` (which PRD inherits via `start()`) but the surfacing in PRD's terminate override is missing. Test gap: no test exercises `PrdClaudeProcess + BrokenPipe + terminate-without-wait`. **`[also F]` MEDIUM-1, elevated to HIGH.** |
| **INV-026** | Interaction Effects | `build_command()` is called exactly once per `start()` (otherwise `extra_args` could be mutated between calls) | UNADDRESSED | LOW | `pipeline/process.py:163` calls `build_command()` for Popen; `:184` calls it again for the debug log slice. T-010 pins idempotency for PortifyProcess but only for back-to-back calls in test code. **`[also F]` NIT-3.** |
| **INV-027** | Interaction Effects | SIGTERM during `_write_prompt_to_stdin` correctly captures the BrokenPipe | UNADDRESSED | MEDIUM | T-005 asserts `_stdin_error` is populated when SIGTERM fires during write, but T-005's timer is scheduled BEFORE `proc.start()` (`test_process_stdin.py:230-234`). If 0.5s timer fires while `_process is None`, terminate is a noop and the test passes via wrong code path. **`[also F]` NIT-2 — F flagged as nit; here the consequence is that the test does not actually pin the stated invariant.** |
| **INV-028** | Interaction Effects | `_stdin_error` capture is lossy if BOTH BrokenPipe AND OSError occur in the loop | UNADDRESSED | LOW | `pipeline/process.py:220-224`: BrokenPipe is checked before OSError. If BrokenPipe is raised first, OSError handler never runs (correct). But if a chained error chain (`__cause__`) attaches, `_stdin_error` records only the outermost. No real-world impact, but the capture is shallow. **`[NEW vs F]`** — F did not consider chained exception paths. |
| **INV-029** | State Variables | `_stdin_error` does not survive a successful re-run (i.e., calling `start()` twice succeeds even if the first call set `_stdin_error`) | ADDRESSED | LOW | `pipeline/process.py:175` resets to `None` at every `start()` entry. F Q4 + F LOW-1. |
| **INV-030** | Guard Conditions | Tests pass on a non-Linux platform where pipe buffer is not 64 KiB | UNADDRESSED | LOW | T-005 asserts pipe-fill happens with 256 KB payload; on a system with >256 KB pipe buffer (some BSDs, macOS with `kern.ipc.maxsockbuf`), the parent write may complete before SIGTERM fires, and the test passes via wrong path. CI is Linux-only per CLAUDE.md so safe in practice. **`[NEW vs F]`** — F did not consider non-Linux pipe-buffer sizes. |

---

## Summary

**Total findings**: 30.

**Counts by status × severity:**

| | HIGH | MEDIUM | LOW |
|---|---|---|---|
| **ADDRESSED** | 0 | 0 | 14 |
| **UNADDRESSED** | 2 | 6 | 8 |

**HIGH UNADDRESSED items (BLOCK convergence per protocol):**

1. **INV-004 — PrdClaudeProcess.terminate() does not surface `_stdin_error`.** Subclass propagation gap. PRD silently swallows BrokenPipe under SIGTERM-only paths. (`[also F]` MEDIUM-1, elevated.)
2. **INV-025 — PrdClaudeProcess + BrokenPipe + terminate-without-wait combination has zero test coverage.** Same root as INV-004; counted separately because the gap is "no test exercises this path" vs INV-004's "subclass override is missing the surfacing block."

**Both HIGH UNADDRESSED items are the same underlying issue (PrdClaudeProcess.terminate + _stdin_error)** approached from two angles (code gap + test gap). Convergence is BLOCKED until either (a) PRD's terminate is fixed in this delta, or (b) it is filed as a tracked follow-up issue with explicit deferral and a test pinning the regression in PRD subsystem.

---

## CRUCIAL: Things F missed

**Items F found that I confirm `[also F]`**: 8
- INV-001 (LOW-1, _stdin_error not in __init__)
- INV-002 (LOW-1, future-refactor risk — elevated)
- INV-003 (Q4)
- INV-004 (MEDIUM-1, elevated to HIGH)
- INV-006 (Strengths, pre-spawn ordering)
- INV-009 (MEDIUM-2, env parser)
- INV-010 (Q7, cap=0)
- INV-012 (Strengths, chunk slicing)
- INV-014 (LOW-2, n==0 silent break — elevated)
- INV-016 (Strengths, empty prompt)
- INV-018 (T-004 second method)
- INV-026 (NIT-3, build_command twice)
- INV-027 (NIT-2, T-005 timer-before-start)

**Items I found that F did NOT `[NEW vs F]`**: **8 distinct findings**

| INV | Finding | Why F missed |
|---|---|---|
| **INV-005** | `_stdout_fh`/`_stderr_fh` leak if non-OSError exception raises mid-flight in `_write_prompt_to_stdin` | F focused on the inner try/except behavior; did not trace what happens if `MemoryError`/`KeyboardInterrupt` propagates between `:149-152` (file open) and `:176` (chunked write). The handles open before the chunked write but `_close_handles()` only runs in wait()/terminate() paths. |
| **INV-011** | `PROMPT_MAX_BYTES < 0` (negative env) breaks every call | F's Q7 considered cap=0 only. Negative caps (e.g., `=-1` from a config-template substitution failure) make every prompt over-cap. |
| **INV-015** | T-001's argv 4 KiB ceiling does not exercise `extra_args` size; live caller path unprotected | F's "Mutation kill rate" §6 noted that argv invariants are well-pinned but did not check whether the test exercises the extension path that callers actually use. |
| **INV-019** | NUL-byte prompt round-trip not pinned | F's §6 mentioned NUL bytes as a missing edge case but rated 4/5 not as a finding. Probe elevates to a structural mutation-kill gap. |
| **INV-023** | tool_write_mode × BrokenPipe combination not tested | F examined T-007 and T-011 separately; did not flag the cross-product. |
| **INV-024** | PortifyProcess anchor `cmd.index('--output-format')` returns FIRST occurrence; multi-occurrence (caller passes `--output-format` in `extra_args`) lands anchor at wrong position under future code reorder | F's Q6 verified the except branch is unreachable; did not check what happens with multiple occurrences. |
| **INV-028** | Chained `__cause__` exception captured shallowly in `_stdin_error` | F did not consider exception-chain depth. |
| **INV-030** | Non-Linux pipe-buffer-size invalidates T-005's pipe-fill assumption | F's §6 considered Linux-blocking-FD only. Cross-platform pipe-buffer variance not probed. |

**Headline metric: `[NEW vs F]` count = 8.**

Of these 8, the highest-impact is **INV-005** (file handle leak on unexpected mid-flight exception) — MEDIUM severity, completely missed by F. The rest are LOW-MEDIUM and largely test-gap or future-refactor risks.

**Combined with F's findings, the residual surface is:**
- 2 HIGH (both INV-004 / MEDIUM-1 family).
- 6 MEDIUM (INV-002, INV-005, INV-009, INV-014, INV-023, INV-027).
- 8 LOW (assorted).
- Plus all 14 ADDRESSED items confirmed against direct source read.

The probe finds the consensus surface "approved-with-nits" is correctly characterized but undercounts the residual by ~50% (F: 2 MEDIUM + 4 LOW/NIT = 6; probe: 2 HIGH + 6 MEDIUM + 8 LOW = 16). Most of the gap is test-coverage and future-refactor-resistance, not active bugs.

---

**End of invariant-probe.md**
