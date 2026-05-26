# Research: Test Infrastructure
**Topic type:** Test & Verification
**Scope:** tests/pipeline/* + tests/cli_portify/test_process.py + pyproject.toml at HEAD = 2c21279
**Status:** Complete
**Date:** 2026-05-01

---

## 1. NEW FILE Confirmation (refactor-plan claims)

| Path | Exists? | Verification |
|---|---|---|
| `/config/workspace/IronClaude/tests/pipeline/test_prd_process_stdin.py` | NO | `test -f` returned NOT FOUND |
| `/config/workspace/IronClaude/tests/pipeline/test_subclass_terminate_invariant.py` | NO | `test -f` returned NOT FOUND |
| `/config/workspace/IronClaude/tests/pipeline/conftest.py` | YES | 27 lines |
| `/config/workspace/IronClaude/tests/pipeline/test_process_stdin.py` | YES | 394 lines (created in prior delta) |
| `/config/workspace/IronClaude/tests/pipeline/test_process.py` | YES | 234 lines (existing baseline) |

Both refactor-plan "NEW FILE" claims are confirmed accurate. The builder must instruct the executor to create those two new files from scratch.

---

## 2. `tests/pipeline/test_process_stdin.py` — Full Inventory

**Header (lines 1-23):** Module docstring + imports. Uses `from __future__ import annotations`, `logging`, `sys`, `threading`, `time`, `unittest.mock.patch`, `pytest`, and the production imports `PortifyProcess`, `ClaudeProcess`, `PromptTooLargeForArgv`.

**Helper:** `_stdin_echo_argv()` at **lines 31-37**. Module-level function (NOT a method, NOT a fixture). Returns `[sys.executable, "-c", "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())"]`. This is the canonical Python stand-in for the `claude` binary that round-trips stdin to stdout. New tests that need a stdin echo MUST import/use this helper, not redeclare it.

### 2.1 Class & Test Listing (with line ranges)

| Class | Lines | Test | Lines | Fixtures | Patterns Used |
|---|---|---|---|---|---|
| `TestPortifyAnchor` | 45-115 | `test_output_format_flag_and_value_are_adjacent_for_portify_anchor` | 48-68 | `tmp_path` | Plain `build_command()` argv-shape assertions; no mocking |
| `TestPortifyAnchor` | | `test_portify_add_dir_works_for_large_prompt` | 70-97 | `tmp_path` | Phase 1 argv assertions + Phase 2 `patch.object(PortifyProcess, "build_command", return_value=_stdin_echo_argv())` then `proc.run()` and read `out.md` bytes |
| `TestPortifyAnchor` | | `test_portify_anchor_resilient_to_repeated_calls` | 99-115 | `tmp_path` | Idempotency check: two `build_command()` calls returning equal lists |
| `TestPromptMaxBytesGuard` | 123-167 | `test_prompt_max_bytes_guard` | 126-150 | `tmp_path`, `monkeypatch` | `monkeypatch.setattr("superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", 1024)`; `pytest.raises(PromptTooLargeForArgv)`; assert `proc._process is None` and `not out_file.exists()` |
| `TestPromptMaxBytesGuard` | | `test_prompt_under_cap_passes_guard` | 152-167 | `tmp_path`, `monkeypatch` | Same `monkeypatch.setattr` constant override + `patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv())` |
| `TestChunkedStdinWrite` | 175-285 | `test_huge_prompt_400kb_round_trip_via_stdin` | 178-191 | `tmp_path` | `patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv())` + bytes round-trip |
| `TestChunkedStdinWrite` | | `test_huge_utf8_emoji_prompt_round_trip` | 193-207 | `tmp_path` | UTF-8 multibyte payload (`"🦀" * (50 * 1024)`); same patch pattern |
| `TestChunkedStdinWrite` | | `test_terminate_during_stdin_write_no_hang` | 209-243 | `tmp_path` | `threading.Timer(0.5, proc.terminate)` + `time.monotonic()` budget; sleeper stand-in `time.sleep(30); sys.stdin.buffer.read()` |
| `TestChunkedStdinWrite` | | `test_empty_prompt_uses_stdin_with_zero_bytes` | 245-260 | `tmp_path` | Empty payload assertions + `_stdin_echo_argv()` stand-in |
| `TestChunkedStdinWrite` | | `test_broken_pipe_surfaces_via_stdin_error_log` | **262-285** | `tmp_path`, `caplog` | `caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process")` + `early_exit = [sys.executable, "-c", "import sys; sys.exit(0)"]` |
| `TestToolWriteMode` | 293-358 | `test_tool_write_mode_redirects_stdout_to_log_sidecar` | 303-336 | `tmp_path` | Custom stand-in emitting to stdout; assertions on `out_file.with_suffix(".log")` |
| `TestToolWriteMode` | | `test_tool_write_mode_false_keeps_stdout_in_output_file` | 338-358 | `tmp_path` | Same pattern with `tool_write_mode=False` |
| `TestArgvByteSizeInvariant` | 366-393 | `test_argv_total_byte_size_bounded_for_huge_prompt` | 374-393 | `tmp_path` | `max(len(arg.encode("utf-8")) for arg in cmd) < 4 * 1024` invariant |

**Test count in `test_process_stdin.py`: 13 tests across 5 classes.**

### 2.2 Recurring patterns (for builder reference)

- **`tmp_path` is the universal fixture.** Every test takes `tmp_path` and constructs `output_file=tmp_path / "out.txt"` and `error_file=tmp_path / "err.txt"` (or `out.md` for the Portify/tool_write variants).
- **Mocking style:** `patch.object(ClaudeProcess, "build_command", return_value=<argv-list>)` as a `with` block. The argv-list is either `_stdin_echo_argv()` (echo), or an inline `[sys.executable, "-c", "..."]` for special behavior.
- **Constant overrides:** `monkeypatch.setattr("superclaude.cli.pipeline.process.PROMPT_MAX_BYTES", <int>)` — full-dotted-path string form. This is the pattern P-013 should use if it needs to override a constant.
- **Log capture:** `caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process")` is the canonical incantation. T-011 nests it OUTSIDE the `patch.object` block.
- **No helper class for building `ClaudeProcess`.** Every test instantiates `ClaudeProcess(prompt=..., output_file=..., error_file=...)` inline. The builder should NOT instruct the executor to create a fixture/factory — that would diverge from the established style.
- **Lifecycle:** `proc.start()` then `rc = proc.wait()` is the standard sequence (NOT `proc.run()` for ClaudeProcess; `proc.run()` is used for `PortifyProcess` only — see T-009 line 95).
- **Threading guard tests:** `threading.Timer(<delay>, proc.<method>)` with `try/finally: timer.cancel()`. Use `time.monotonic()` not `time.time()` for budgets. T-005 (line 209-243) is the prototype for T-013's terminate-during-write check, and the explicit blueprint for **T-014** (subclass terminate invariant).

---

## 3. T-011 Anchor Detail (for P-013 in-place edit)

**Test class:** `TestChunkedStdinWrite`
**Test function:** `test_broken_pipe_surfaces_via_stdin_error_log`
**Full body line range:** 262-285 (`def test_broken_pipe...` → end of conditional block).
**Conditional block to replace (P-013):** **lines 282-285** inclusive.

Verbatim current body (lines 262-285):

```python
    def test_broken_pipe_surfaces_via_stdin_error_log(self, tmp_path, caplog):
        """T-011: child exits before reading; _stdin_error captured + WARNING log."""
        # Stand-in exits 0 immediately, never reading stdin. With a 1 MB
        # payload the parent's write loop is guaranteed to encounter
        # BrokenPipe somewhere mid-stream (pipe is closed when child exits).
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
```

**The `if proc._stdin_error is not None:` block (lines 282-285)** is the conditional escape hatch. P-013's job is to convert this from "best-effort if it broke" to a deterministic assertion (the refactor plan calls for guaranteeing the broken-pipe path actually fires by sizing the payload large enough or otherwise forcing the race deterministically). The exact rewrite content is owned by Researcher 3 (refactor-plan content lift); the line anchor is **lines 282-285** within this test (whose containing test ends at line 285).

---

## 4. `tests/pipeline/test_process.py` — Baseline Inventory

14 test functions across 4 classes (lines):
- `TestClaudeProcessCommand` (16-108): 8 tests — argv-shape assertions, no subprocess
- `TestClaudeProcessEnv` (111-123): 1 test — `patch.dict("os.environ", ...)` for env scrubbing
- `TestClaudeProcessStreamJsonCompat` (126-153): 1 test — sprint-flag compat
- `TestClaudeProcessStdinDelivery` (156-234): 4 tests — has internal helper `_patch_claude_binary(self, cmd_override)` at line 163-165, used as `with self._patch_claude_binary(stand_in):` — note this is the OLDER helper style; the newer `test_process_stdin.py` switched to module-level `_stdin_echo_argv()` + `patch.object` directly. **New tests should match the newer style** (module-level helper).

---

## 5. `tests/pipeline/conftest.py` — Shared Fixtures

Only 2 fixtures, both thin:
- `tmp_dir(tmp_path)` — alias for `tmp_path` (line 11-14)
- `make_file(tmp_path)` — factory `(name, content) -> Path` that writes UTF-8 (line 17-26)

Neither is used by `test_process_stdin.py`. **The new tests should not introduce new conftest fixtures** — keep with the inline `tmp_path`-only style of the sibling file.

---

## 6. `tests/cli_portify/test_process.py` — Subclass Surface

33 test functions across 9 classes. Key relevance for **T-014 (subclass terminate invariant)**:
- `TestPortifyProcessInheritance` (lines 27-43) — confirms `PortifyProcess` IS-A `ClaudeProcess`
- `TestPortifyProcessRun` (164-237) — uses `@patch.object(PortifyProcess, "wait", ...)` and `@patch.object(PortifyProcess, "start", ...)` decorator-style (older style than the `with` block in `test_process_stdin.py`)
- This file has NO terminate-related tests today — T-014 fills that gap and naturally lives in the **NEW** `test_subclass_terminate_invariant.py` per refactor-plan.

---

## 7. pyproject.toml pytest Configuration

**[tool.pytest.ini_options]** (lines 99-133):
- `testpaths = ["tests"]`
- `python_files = ["test_*.py"]`, `python_classes = ["Test*"]`, `python_functions = ["test_*"]`
- `addopts = ["-v", "--strict-markers", "--tb=short"]` — `--strict-markers` is on; any unregistered `@pytest.mark.X` will fail collection.
- **Registered markers** (line 109-133): `unit`, `integration`, `hallucination`, `performance`, `slow`, `confidence_check`, `self_check`, `reflexion`, `complexity`, `diagnostic`, `diagnostic_l0..l3`, `diagnostic_negative`, `e2e_trailing`, `backward_compat`, `property_based`, `nfr_benchmark`, `gate_performance`, `context_injection_test`, `thread_safety`, `agent_regression`. **None of the existing tests in `test_process_stdin.py` use any markers** — neither should the new ones (no `@pytest.mark.*` decorators required).

**[project.entry-points.pytest11]** (line 67-68):
- `superclaude = "superclaude.pytest_plugin"` — the auto-loaded plugin is active.

**Coverage:** `[tool.coverage.run]` source = `["src/superclaude"]`. Not invoked by the green-baseline command.

---

## 8. Sanity baseline (pre-task green run)

**Pre-task test counts (HEAD = 2c21279):**

| File | `def test_*` count |
|---|---|
| `tests/pipeline/test_process_stdin.py` | 13 |
| `tests/pipeline/test_process.py` | 14 |
| `tests/cli_portify/test_process.py` | 33 |
| **Combined `tests/pipeline tests/cli_portify` baseline subtotal** | **(see uv pytest run below)** |

**Phase 6 sanity gate command** (the exact invocation the task should use to verify green pre/post):

```bash
uv run pytest tests/pipeline tests/cli_portify -v
```

The repo-wide green count of 1294/1294 cited in prior session traces was the full `uv run pytest` (no path filter). The narrower `tests/pipeline tests/cli_portify` slice is the appropriate pre/post gate for the stdin-recon track because the source delta is bounded to `src/superclaude/cli/pipeline/process.py` and `src/superclaude/cli/cli_portify/process.py`. After the new tests land, expect the slice count to grow by 6 (P-007, P-008, T-013, T-014, T-015, T-016) — P-013 is an in-place edit so it does not increase the count.

**Expected post-task delta:** +6 tests in the pipeline+cli_portify slice; full `uv run pytest` count moves from 1294 → 1300.

---

## 9. Patterns the Builder Should Embed in New Test Items

| Item | New file? | Class | Fixture(s) | Helper | Mocking Pattern | Reference test (model after) |
|---|---|---|---|---|---|---|
| **P-007** | NEW: `test_prd_process_stdin.py` | (new — name TBD per refactor plan) | `tmp_path` | Import `_stdin_echo_argv` from sibling OR redeclare locally; consult refactor-plan | `patch.object(ClaudeProcess, "build_command", return_value=_stdin_echo_argv())` | T-002 (line 178-191) |
| **P-008** | NEW: `test_prd_process_stdin.py` (likely) | (new) | `tmp_path` | same as P-007 | `patch.object(...)` `with`-block | T-002 / T-006 |
| **T-013** | NEW: `test_subclass_terminate_invariant.py` | new class, name per plan | `tmp_path` | sleeper stand-in inline | `threading.Timer(0.5, proc.terminate)` + `time.monotonic()` budget; `patch.object(PortifyProcess, "build_command", return_value=sleeper)` | T-005 (line 209-243) |
| **T-014** | NEW: `test_subclass_terminate_invariant.py` | same class | `tmp_path` | sleeper stand-in inline | Same Timer pattern; assert `PortifyProcess` honors the same terminate contract as parent | T-005 + `TestPortifyProcessInheritance` (cli_portify file line 27) |
| **T-015** | NEW (per refactor-plan; check Researcher 3) | per plan | `tmp_path` (+ possibly `caplog` or `monkeypatch`) | per plan | per plan | Likely T-011 or T-005 family — confirm via plan |
| **T-016** | NEW (per refactor-plan; check Researcher 3) | per plan | `tmp_path` (+ possibly `caplog` or `monkeypatch`) | per plan | per plan | Likely T-001 or T-007 family — confirm via plan |
| **P-013** | EDIT: `test_process_stdin.py` lines 282-285 | `TestChunkedStdinWrite::test_broken_pipe_surfaces_via_stdin_error_log` | (existing `tmp_path`, `caplog`) | (none new) | Replace conditional `if proc._stdin_error is not None:` block (lines 282-285) with deterministic assertion per refactor-plan | T-011 itself (rewrite) |

**Universal style rules for the executor (from inventory):**
1. Module-level helpers, NOT methods (follow `_stdin_echo_argv()` precedent).
2. Each test takes `tmp_path` and builds `output_file` + `error_file` inline.
3. `patch.object(ClassName, "build_command", return_value=...)` as a `with` block.
4. `proc.start()` then `rc = proc.wait()` for ClaudeProcess; `proc.run()` only for PortifyProcess argv-shape phase 2 tests.
5. Use `time.monotonic()` for time budgets, never `time.time()`.
6. Use `threading.Timer(delay, callable)` with `try/finally: timer.cancel()` for terminate-during-X tests.
7. Use `monkeypatch.setattr("superclaude.cli.pipeline.process.<NAME>", value)` (full dotted path string form) for constant overrides.
8. Use `caplog.at_level(logging.WARNING, logger="superclaude.pipeline.process")` for warning-log assertions.
9. NO `@pytest.mark.*` decorators (none used in `test_process_stdin.py`; markers are strict-validated).
10. NO new conftest fixtures — match the inline-style of the sibling file.
11. Imports at top: `from __future__ import annotations`, then stdlib (`logging`, `sys`, `threading`, `time`), then `from unittest.mock import patch`, then `pytest`, then production imports `from superclaude.cli.pipeline.process import ClaudeProcess, PromptTooLargeForArgv` (and `PortifyProcess` from `superclaude.cli.cli_portify.process` if needed).

---

## Summary

- Two refactor-plan "NEW FILE" claims confirmed accurate (neither test_prd_process_stdin.py nor test_subclass_terminate_invariant.py exists at HEAD 2c21279).
- T-011 anchor pinned to lines 262-285; the `if`-block to replace is at lines 282-285 inside `TestChunkedStdinWrite::test_broken_pipe_surfaces_via_stdin_error_log`.
- `tests/pipeline/test_process_stdin.py` style is fully canonical: module-level `_stdin_echo_argv()` helper, inline `tmp_path`-based ClaudeProcess construction, `with patch.object(...)` blocks, no markers, no shared factory fixture. New tests must match this style.
- Pyproject pytest config has `--strict-markers` on; new tests should use NO custom markers (consistent with sibling file).
- Sanity gate: `uv run pytest tests/pipeline tests/cli_portify -v`. Pre-task subtotal: 13 + 14 + 33 = 60 across the 3 process-related files (full slice includes more); expect +6 net after task.
