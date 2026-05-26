# Research: Source Code Verification
**Topic type:** File Inventory + Doc Cross-Validator (hybrid)
**Scope:** src/superclaude/cli/{pipeline,prd,cli_portify}/process.py against HEAD = 2c21279
**Status:** Complete
**Date:** 2026-05-01
**HEAD verified:** `2c2127940bdc6456dc881cde9522b034dd5ef0cb`
**File line counts:** pipeline/process.py=324, prd/process.py=279, cli_portify/process.py=251, tests/pipeline/test_process_stdin.py (T-011 region investigated)
---

## Anchor Verification — Per Item

### P-006 — `prd/process.py:277` (insert before `_close_handles()`)

**Status:** DRIFT — refactor-plan cites L277, actual `_close_handles()` final call site is L279.

**Actual current source (`prd/process.py` L274-279):**
```
274            except (ProcessLookupError, subprocess.TimeoutExpired):
275                pass
276
277        if self._on_exit is not None:
278            self._on_exit(self._process.pid, self._process.returncode)
279        self._close_handles()
```

**Insert anchor (5-line context surrounding the insertion point, BEFORE `_close_handles()` at L279):**
```
275            pass
276
277        if self._on_exit is not None:
278            self._on_exit(self._process.pid, self._process.returncode)
279        self._close_handles()  # ← insert 4-line _stdin_error block IMMEDIATELY BEFORE this line
```

**Builder note:** The `_close_handles()` call is at **L279** (not L277). The refactor-plan's "L277" appears to point to the `if self._on_exit is not None:` line, not the actual `_close_handles()` call. Insertion should be **immediately before L279** (after L278's `self._on_exit(...)` call).

**Reference base block (verified in `pipeline/process.py:288-291`):**
```
288        if getattr(self, "_stdin_error", None) is not None:
289            _log.warning(
290                "stdin_error pid=%s err=%r", self._process.pid, self._stdin_error
291            )
```

**Before (insertion site, currently empty):** N/A — this is a NEW INSERT.

**After (4-line insert at new L279):**
```python
        if getattr(self, "_stdin_error", None) is not None:
            _log.warning(
                "stdin_error pid=%s err=%r", self._process.pid, self._stdin_error
            )
        self._close_handles()
```

---

### P-009 — `pipeline/process.py:27-29` (PROMPT_MAX_BYTES env-var read)

**Status:** VERIFIED at L27-29 (exact match).

**Before (current source verbatim, L24-29):**
```
24    # Default 16 MiB; env-overridable for operators with exotic workflows.
25    # This is a sanity guard, not a kernel limit -- Linux MAX_ARG_STRLEN no
26    # longer applies because the prompt is delivered via stdin (since 4799719).
27    PROMPT_MAX_BYTES: int = int(
28        os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024)
29    )
```

**After (per refactor-plan):** Replace with helper function `_resolve_prompt_max_bytes()` that catches `ValueError` and falls back to default with `_log.warning("ignoring non-numeric SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)`.

---

### P-011 — `pipeline/process.py` `__init__` around L56-90 (init `_stdin_error = None`)

**Status:** VERIFIED — `_stdin_error` is currently NOT initialized in `__init__`. The asymmetric defensive read (U-007) is real.

**Evidence — `__init__` body (L56-90):**
```
56        def __init__(
57            self,
58            *,
59            prompt: str,
60            output_file: Path,
...
74            self.prompt = prompt
...
86            self._extra_env_vars = env_vars
87            self.tool_write_mode = tool_write_mode
88            self._process: Optional[subprocess.Popen] = None
89            self._stdout_fh = None
90            self._stderr_fh = None
```

`_stdin_error` is first assigned at **L175** (inside `start()`):
```
175            self._stdin_error: Optional[BaseException] = None
176            self._write_prompt_to_stdin(self._prompt_bytes)
```

**Asymmetry confirmed:**
- `wait()` L240: `if getattr(self, "_stdin_error", None) is not None:` (defensive)
- `terminate()` L288: `if getattr(self, "_stdin_error", None) is not None:` (defensive)
- Both use `getattr` because `_stdin_error` may not exist if `start()` was never called.

**Before (insertion anchor, L88-90):**
```python
        self._process: Optional[subprocess.Popen] = None
        self._stdout_fh = None
        self._stderr_fh = None
```

**After (P-011 insert):**
```python
        self._process: Optional[subprocess.Popen] = None
        self._stdout_fh = None
        self._stderr_fh = None
        self._stdin_error: Optional[BaseException] = None
```

**Note:** P-011 also enables removing the redundant `self._stdin_error = None` at L175 (since `__init__` already set it), but the refactor-plan only mandates the `__init__` add. Both call sites at L240 and L288 can subsequently switch from `getattr(self, "_stdin_error", None)` to plain `self._stdin_error`.

---

### P-012 — `pipeline/process.py:181-186` (spawn debug log)

**Status:** VERIFIED at L181-186 (exact match).

**Before (current source verbatim, L181-186):**
```
181        _log.debug(
182            "spawn pid=%d cmd=%s prompt_bytes=%d",
183            self._process.pid,
184            str(self.build_command()[:3]),
185            len(self._prompt_bytes),
186        )
```

Format string at L182 is exactly `"spawn pid=%d cmd=%s prompt_bytes=%d"` — does NOT contain `prompt_via=stdin`. Refactor-plan's stated Before matches verbatim.

**After (per refactor-plan, format string at L182 only):**
```python
            "spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d",
```

---

### T-012 — `pipeline/process.py:216-218` (n=0 silent break)

**Status:** VERIFIED at L216-218 (exact match).

**Before (current source verbatim, L213-219):**
```
213                    except InterruptedError:
214                        # EINTR from signal delivery -- retry the same chunk.
215                        continue
216                if n <= 0:
217                    # Defensive -- os.write should not return 0 on a pipe.
218                    break
219                offset += n
```

The break at L218 is currently silent — no `_stdin_error` is set.

**After (per refactor-plan; insert capture before `break`):**
```python
                if n <= 0:
                    # Defensive -- os.write should not return 0 on a pipe.
                    self._stdin_error = OSError(
                        f"unexpected zero-byte write at offset {offset}/{len(view)}"
                    )
                    break
```

---

### P-013 — `tests/pipeline/test_process_stdin.py:465-488` (T-011 BrokenPipe assertion)

**Status:** SEVERE DRIFT — refactor-plan cites L465-488, actual T-011 location is **L262-285** (203-line negative drift).

**Actual T-011 test location (L262-285):**
```
262        def test_broken_pipe_surfaces_via_stdin_error_log(self, tmp_path, caplog):
263            """T-011: child exits before reading; _stdin_error captured + WARNING log."""
264            # Stand-in exits 0 immediately, never reading stdin. With a 1 MB
265            # payload the parent's write loop is guaranteed to encounter
266            # BrokenPipe somewhere mid-stream (pipe is closed when child exits).
267            early_exit = [sys.executable, "-c", "import sys; sys.exit(0)"]
268            proc = ClaudeProcess(
269                prompt="c" * (1024 * 1024),
270                output_file=tmp_path / "out.txt",
271                error_file=tmp_path / "err.txt",
272            )
273            with caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process"):
274                with patch.object(ClaudeProcess, "build_command", return_value=early_exit):
275                    # start() must NOT raise even though the write hits BrokenPipe.
276                    proc.start()
277                    rc = proc.wait()
278            assert rc == 0  # child's actual exit code
279            # _stdin_error is only populated if the write actually broke -- on a
280            # very fast race the child may exit cleanly after consuming the buffer.
281            # If it did break, ensure we surfaced it; otherwise nothing to assert.
282            if proc._stdin_error is not None:
283                assert isinstance(proc._stdin_error, (BrokenPipeError, OSError))
284                warnings = [r for r in caplog.records if "stdin_error" in r.message]
285                assert warnings, "BrokenPipe must surface as a WARNING log"
```

**Conditional assertion is at L282-285** (not L482-488 as refactor-plan would imply by `465-488` range). Race-tolerant `if proc._stdin_error is not None:` shape is at **L282**.

**Before (current source verbatim, L278-285):**
```python
        assert rc == 0  # child's actual exit code
        # _stdin_error is only populated if the write actually broke -- on a
        # very fast race the child may exit cleanly after consuming the buffer.
        # If it did break, ensure we surfaced it; otherwise nothing to assert.
        if proc._stdin_error is not None:
            assert isinstance(proc._stdin_error, (BrokenPipeError, OSError))
            warnings = [r for r in caplog.records if "stdin_error" in r.message]
            assert warnings, "BrokenPipe must surface as a WARNING log"
```

**After (per refactor-plan):** Replace race-tolerant shape with `monkeypatch.setattr(os, "write", _raise_broken_pipe)` to inject BrokenPipe deterministically; assert unconditionally.

**Builder note:** The line range cited in refactor-plan (`465-488`) is wrong against current HEAD. Use **L262-285** (test method body) or specifically **L278-285** (the assertion block to be replaced).

---

### `cli_portify/process.py` — `--output-format` anchor logic (P-001 / D-FOLLOW-006 sanity)

**Status:** VERIFIED — anchor logic is in place and stable at L208-219.

**Source verbatim (L208-221):**
```
208            # Anchor: insert --add-dir flags after `--output-format <value>`. The
209            # base build_command() emits `--output-format` unconditionally and the
210            # next element is its value, so the splice point is index+2. The prompt
211            # is delivered via stdin (no `-p` ever in argv since 4799719), so the
212            # legacy `cmd.index("-p")` lookup was dead code that always fell into
213            # the except branch.
214            try:
215                anchor_idx = cmd.index("--output-format")
216                insert_at = anchor_idx + 2  # skip flag + value
217                cmd[insert_at:insert_at] = add_dir_args
218        except ValueError:  # pragma: no cover -- defensive: base contract violated
219                cmd.extend(add_dir_args)
220
221            return cmd
```

P-001 from `526a606` is in place. Lookup is `cmd.index("--output-format")` (first occurrence; D-FOLLOW-006 acknowledges multi-occurrence is a future hazard but is LOW and out of scope).

---

## Drift Summary

| Anchor | Refactor-plan citation | Actual current location | Drift severity |
|---|---|---|---|
| P-006 | `prd/process.py:277` | `prd/process.py:279` (`_close_handles()` call) | **MINOR (+2)** — cited line points at `if self._on_exit` not at `_close_handles()`; insertion point clarified. |
| P-009 | `pipeline/process.py:27-29` | L27-29 | **NONE** — exact match. |
| P-011 | `pipeline/process.py` `__init__` (L56-90) | `__init__` body L56-90; insertion point L88-90 | **NONE** — range still valid. |
| P-012 | `pipeline/process.py:181-186` | L181-186 | **NONE** — exact match. |
| T-012 | `pipeline/process.py:216-218` | L216-218 | **NONE** — exact match. |
| P-013 | `tests/pipeline/test_process_stdin.py:465-488` | L262-285 (specifically L282 for conditional) | **SEVERE (-203)** — test file is much shorter than refactor-plan assumed; actual T-011 is at L262-285. |
| cli_portify P-001 | implicit (L208-219 region) | L208-221 | **NONE** — anchor logic verified intact. |

**Verdict:** 5 of 7 anchors verified at exact cited locations. 1 minor drift (P-006: insertion target is L279, refactor-plan loosely says L277). 1 severe drift (P-013: line range 465-488 is off by ~200 lines; actual T-011 at L262-285).

---

## Builder-Usable Anchors (paste-ready for B2 items)

### P-006 (CODE-FIX, prd/process.py)

```yaml
file: src/superclaude/cli/prd/process.py
location: insert before line 279 (_close_handles() final call in terminate())
verified_at_line: 279
before:
  - 'L277:        if self._on_exit is not None:'
  - 'L278:            self._on_exit(self._process.pid, self._process.returncode)'
  - 'L279:        self._close_handles()'
after:
  - 'L277:        if self._on_exit is not None:'
  - 'L278:            self._on_exit(self._process.pid, self._process.returncode)'
  - 'L279:        if getattr(self, "_stdin_error", None) is not None:'
  - 'L280:            _log.warning('
  - 'L281:                "stdin_error pid=%s err=%r", self._process.pid, self._stdin_error'
  - 'L282:            )'
  - 'L283:        self._close_handles()'
note: "Refactor-plan cites L277 but the actual _close_handles() call is at L279."
```

### P-009 (CODE-FIX, pipeline/process.py)

```yaml
file: src/superclaude/cli/pipeline/process.py
location: L27-29 (module-level PROMPT_MAX_BYTES assignment)
verified_at_line: "27-29"
before: |
  PROMPT_MAX_BYTES: int = int(
      os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES", 16 * 1024 * 1024)
  )
after: |
  def _resolve_prompt_max_bytes() -> int:
      raw = os.environ.get("SUPERCLAUDE_PROMPT_MAX_BYTES")
      default = 16 * 1024 * 1024
      if raw is None:
          return default
      try:
          value = int(raw)
      except ValueError:
          _log.warning("ignoring non-numeric SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)
          return default
      if value < 0:
          _log.warning("ignoring negative SUPERCLAUDE_PROMPT_MAX_BYTES=%r", raw)
          return default
      return value

  PROMPT_MAX_BYTES: int = _resolve_prompt_max_bytes()
```

### P-011 (CODE-FIX, pipeline/process.py)

```yaml
file: src/superclaude/cli/pipeline/process.py
location: end of __init__ body (after L90)
verified_at_line: 90
before:
  - 'L88:        self._process: Optional[subprocess.Popen] = None'
  - 'L89:        self._stdout_fh = None'
  - 'L90:        self._stderr_fh = None'
after:
  - 'L88:        self._process: Optional[subprocess.Popen] = None'
  - 'L89:        self._stdout_fh = None'
  - 'L90:        self._stderr_fh = None'
  - 'L91:        self._stdin_error: Optional[BaseException] = None'
note: "Confirmed _stdin_error is currently first set at L175 inside start(). U-007 asymmetric defensive read is real (wait() L240 and terminate() L288 both use getattr)."
```

### P-012 (CODE-FIX, pipeline/process.py)

```yaml
file: src/superclaude/cli/pipeline/process.py
location: L182 (debug format string)
verified_at_line: "181-186"
before: |
  _log.debug(
      "spawn pid=%d cmd=%s prompt_bytes=%d",
      self._process.pid,
      str(self.build_command()[:3]),
      len(self._prompt_bytes),
  )
after: |
  _log.debug(
      "spawn pid=%d cmd=%s prompt_via=stdin prompt_bytes=%d",
      self._process.pid,
      str(self.build_command()[:3]),
      len(self._prompt_bytes),
  )
```

### T-012 (CODE-FIX, pipeline/process.py)

```yaml
file: src/superclaude/cli/pipeline/process.py
location: L216-218 (n<=0 silent break)
verified_at_line: "216-218"
before: |
  if n <= 0:
      # Defensive -- os.write should not return 0 on a pipe.
      break
after: |
  if n <= 0:
      # Defensive -- os.write should not return 0 on a pipe.
      self._stdin_error = OSError(
          f"unexpected zero-byte write at offset {offset}/{len(view)}"
      )
      break
```

### P-013 (CODE-FIX, tests/pipeline/test_process_stdin.py)

```yaml
file: tests/pipeline/test_process_stdin.py
location: L262-285 (T-011 test body), specifically L278-285 (race-tolerant assertion)
verified_at_line: "262-285"
drift_warning: "Refactor-plan cites L465-488, actual is L262-285 (drift ~200 lines)."
before: |
  # tail of test_broken_pipe_surfaces_via_stdin_error_log (L267-285)
  early_exit = [sys.executable, "-c", "import sys; sys.exit(0)"]
  proc = ClaudeProcess(
      prompt="c" * (1024 * 1024),
      output_file=tmp_path / "out.txt",
      error_file=tmp_path / "err.txt",
  )
  with caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process"):
      with patch.object(ClaudeProcess, "build_command", return_value=early_exit):
          # start() must NOT raise even though the write hits BrokenPipe.
          proc.start()
          rc = proc.wait()
  assert rc == 0  # child's actual exit code
  # _stdin_error is only populated if the write actually broke -- on a
  # very fast race the child may exit cleanly after consuming the buffer.
  # If it did break, ensure we surfaced it; otherwise nothing to assert.
  if proc._stdin_error is not None:
      assert isinstance(proc._stdin_error, (BrokenPipeError, OSError))
      warnings = [r for r in caplog.records if "stdin_error" in r.message]
      assert warnings, "BrokenPipe must surface as a WARNING log"
after: |
  # Inject BrokenPipe deterministically via monkeypatch
  def _raise_broken_pipe(*args, **kwargs):
      raise BrokenPipeError("injected for T-011 mutation-kill")

  proc = ClaudeProcess(
      prompt="c" * (1024 * 1024),
      output_file=tmp_path / "out.txt",
      error_file=tmp_path / "err.txt",
  )
  monkeypatch.setattr(os, "write", _raise_broken_pipe)
  with caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process"):
      with patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv()):
          proc.start()
          rc = proc.wait()
  # Unconditional assertions (no race tolerance):
  assert proc._stdin_error is not None
  assert isinstance(proc._stdin_error, BrokenPipeError)
  warnings = [r for r in caplog.records if "stdin_error" in r.message]
  assert warnings, "BrokenPipe must surface as a WARNING log"
```

### cli_portify P-001 sanity (D-FOLLOW-006 reference only)

```yaml
file: src/superclaude/cli/cli_portify/process.py
location: L208-221 (--output-format anchor lookup in build_command override)
verified_at_line: "208-221"
status: VERIFIED — P-001 from 526a606 in place; no action required for this task. D-FOLLOW-006 (multi-occurrence hazard) is deferred.
```

---

## Items NOT Verified by This Researcher (out of scope)

The following 11 items in refactor-plan are NEW-TEST/NEW-FILE/SPEC-AMENDMENT and have no current source anchors to verify:

- P-007 (NEW-FILE: `tests/pipeline/test_prd_process_stdin.py`)
- P-008 (NEW-FILE: `tests/pipeline/test_subclass_terminate_invariant.py`)
- P-010 (SPEC-AMENDMENT: `RECONCILED_DESIGN.md` §4 P-004)
- P-014 (NEW-FILE: `BEAT_2_BACKLOG.md`)
- P-015 (NEW-FILE: `TRACEABILITY.md`)
- P-016 (Makefile target — `Makefile` exists; out of scope per researcher 1 boundary)
- T-013, T-014, T-015, T-016 (NEW tests appended to `test_process_stdin.py`)

These belong to other researchers (R2 for test infra, R3 for refactor-plan metadata, R4 for spec docs).

---

## Summary

**Verdict:** 5 of 7 in-scope source-code anchors VERIFIED at exact cited line numbers. 1 minor drift (P-006: insertion target is L279 not L277, off by 2). 1 severe drift (P-013: T-011 test is at L262-285 not L465-488, off by ~200 lines because the test file is shorter than refactor-plan assumed).

The Before/After snippets in this document are paste-ready for the task builder. P-006's insertion anchor must be relocated to **before L279** (`_close_handles()` call), and P-013's checklist item must reference **L262-285** (or the assertion block at L278-285) rather than the obsolete `465-488` range.

**Status:** Complete

