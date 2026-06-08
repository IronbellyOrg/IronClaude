# Research: Test Patterns and Seams (M1/M2/M3)

**Status: Complete**
**Date: 2026-06-04**
**Researcher topic:** Test Patterns & Seams — per-fix test seam + setup sketch, new-test-file conventions, verification commands
**Scope (test files read):** `tests/sprint/conftest.py`, `tests/sprint/test_process.py`, `tests/sprint/test_handoff_store.py`, `tests/sprint/test_watchdog.py`, `tests/sprint/test_executor.py` (helpers + the `_run_task_subprocess` seam test), `tests/sprint/test_turn_ledger_concurrency.py` (new-file template).

All citations verified by reading the files at HEAD on branch `SprintCLIWireDead`.

---

## 0. Suite-wide conventions (verified)

### Autouse narrative stub (`conftest.py`)

`tests/sprint/conftest.py:32-55` defines an **autouse** fixture `_stub_phase_narrative` that monkeypatches `superclaude.cli.sprint.summarizer.invoke_sonnet` and `...retrospective.invoke_sonnet` to no-ops for every module EXCEPT `{test_summarizer, test_retrospective, test_backward_compat_regression}` (the `_NARRATIVE_TEST_MODULES` opt-out set, conftest.py:25-29). **Implication for M1/M2/M3 new tests:** any new test module added under `tests/sprint/` automatically inherits this stub — no action needed, and you should NOT add your new module to `_NARRATIVE_TEST_MODULES` (none of M1/M2/M3 exercise the narrative path).

### Markers (registered in `pyproject.toml`)

Registered under `[tool.pytest...] markers = [...]` (pyproject.toml:112+). Pytest runs with `--strict-markers` (pyproject.toml:109), so **an unregistered marker is a hard error**. Relevant registered markers: `unit`, `integration`, `slow`, `performance`, `thread_safety`. Markers actually used across the sprint suite (by count): `unit` (34), `integration` (38), `slow` (5), `property_based` (14), `context_injection_test` (18), `backward_compat` (18). **For M1/M2/M3 prefer `@pytest.mark.unit`** (these are fast, in-process, single-function tests). Do NOT invent a new marker — `--strict-markers` will fail it.

### New-test-file template (model: `test_turn_ledger_concurrency.py`)

`test_turn_ledger_concurrency.py:1-17` is the cleanest recent single-concern new-file model:
- Module docstring explaining the *defect class* the file pins (Stage/RC reference + 1-2 sentences of "what was broken, what this proves").
- `from __future__ import annotations` (line 10).
- Stdlib imports, blank line, `import pytest`, blank line, `from superclaude.cli.sprint.<mod> import <symbol>` (lines 12-16).
- A single decorated test fn with a return type annotation `-> None` and assertion messages that name the regression (lines 19-40). It uses `@pytest.mark.slow` because it spins 400 threads; M1/M2/M3 tests are NOT slow and should use `@pytest.mark.unit`.

---

## M1 — Subprocess file-handle leak on exception during the per-task wait

**Fix site (per Researcher 1):** `executor.py:1514-1520` (`_run_task_subprocess`) — wrap `start()`+`_poll_with_stall_watchdog(...)` so the exception path runs `proc.terminate()` (closes handles, reaps child) then re-raises.

### Seam — direct call of `_run_task_subprocess` with patched base `ClaudeProcess`

The authoritative seam already exists and is proven at **`test_executor.py:1904-1963`** (`test_run_task_subprocess_uses_task_output_file`). Copy its harness. Key mechanics:

- Import the internal fn directly: `from superclaude.cli.sprint.executor import _run_task_subprocess` (test_executor.py:1912). It IS importable and already imported by tests (test_executor.py is in the `_run_task_subprocess`-importing set).
- Build config + phase + task with the module helper `_make_config(tmp_path, num_phases=1)` (test_executor.py:35-54) and `TaskEntry(task_id=..., title=..., description=...)` (test_executor.py:1916).
- Patch the **base** class methods (the real spawn point), NOT the sprint subclass:
  - `patch("superclaude.cli.pipeline.process.ClaudeProcess.__init__", new=capture_init)` where `capture_init` sets `self._process`, `self._stdout_fh = None`, `self._stderr_fh = None` (test_executor.py:1920-1925). This is required because `_run_task_subprocess` calls `_Base.__init__(proc, ...)` via `from superclaude.cli.pipeline.process import ClaudeProcess as _Base` (executor.py:1496-1513).
  - `patch("superclaude.cli.pipeline.process.ClaudeProcess.start", return_value=None)` (test_executor.py:1939-1942).
  - For M1 you do NOT patch `wait` to a clean return — instead you force the **poll watchdog to raise** (below).
- Pre-create the output file: `config.results_dir.mkdir(parents=True, exist_ok=True); config.task_output_file(phase, task).write_text("")` (test_executor.py:1931-1932) so the post-wait `.stat()` path is benign.

### M1 setup sketch — force the wait to raise, assert cleanup ran

The fix wraps the call to `_poll_with_stall_watchdog`. The cleanest injection point is to patch **`superclaude.cli.sprint.executor._poll_with_stall_watchdog`** to raise (e.g. `KeyboardInterrupt`), and spy `terminate`/`_close_handles` on the base class:

```python
import pytest
from unittest.mock import MagicMock, patch
from superclaude.cli.sprint.executor import _run_task_subprocess
from superclaude.cli.sprint.models import TaskEntry

@pytest.mark.unit
def test_run_task_subprocess_closes_handles_when_poll_raises(tmp_path):
    config = _make_config(tmp_path, num_phases=1)   # reuse test_executor helper
    phase = config.phases[0]
    task = TaskEntry(task_id="T01.01", title="x", description="d")

    def capture_init(self, **kwargs):
        self._process = MagicMock(returncode=None)   # still "running"
        self._stdout_fh = None
        self._stderr_fh = None

    config.results_dir.mkdir(parents=True, exist_ok=True)
    config.task_output_file(phase, task).write_text("")

    terminate_called = []
    with (
        patch("superclaude.cli.pipeline.process.ClaudeProcess.__init__", new=capture_init),
        patch("superclaude.cli.pipeline.process.ClaudeProcess.start", return_value=None),
        patch("superclaude.cli.pipeline.process.ClaudeProcess.terminate",
              side_effect=lambda self=None: terminate_called.append(True)),
        patch("superclaude.cli.sprint.executor._poll_with_stall_watchdog",
              side_effect=KeyboardInterrupt),
    ):
        with pytest.raises(KeyboardInterrupt):     # exception MUST re-propagate (no swallow)
            _run_task_subprocess(task, config, phase)

    assert terminate_called, "cleanup (terminate/_close_handles) did not run on the exception path"
```

Two assertions pin the M1 contract precisely:
1. **`pytest.raises(KeyboardInterrupt)`** — the fix must re-raise (Researcher 1 (d): swallowing would regress KeyboardInterrupt-aborts-sprint). If the builder chose `proc._close_handles()` instead of `proc.terminate()`, patch/spy `ClaudeProcess._close_handles` instead.
2. **`terminate_called`** — cleanup actually fired.

**Note on `terminate` patching shape:** the existing C2 test patches unbound base methods via `patch(".../ClaudeProcess.<m>", new=...)`. `terminate`/`_close_handles` are bound instance methods on the constructed `proc`; patching the class attribute with a `side_effect` recorder is the matching idiom. If the recorder signature is awkward, an alternative is a real (un-patched) `terminate` plus asserting `self._stdout_fh`/`self._stderr_fh` became closed — but since `capture_init` sets them to `None`, the spy-on-terminate approach is cleaner and matches the fix's recommended `except BaseException: proc.terminate(); raise` shape.

### M1 — placement

Add to **`tests/sprint/test_executor.py`** as a sibling of `test_run_task_subprocess_uses_task_output_file` (right after test_executor.py:1963). It reuses that module's `_make_config` and import idiom verbatim — a new file is unnecessary and would duplicate the helper.

---

## M2 — Per-task stall watchdog spins unbounded in default `warn` mode

**Fix site (per Researcher 1):** `executor.py:1436-1465` (`_poll_with_stall_watchdog`) — add an absolute wall-clock ceiling `getattr(proc, "timeout_seconds", <fallback>)` to the `while` guard so the loop falls through to the bounded `proc.wait()` at executor.py:1465.

### Seam — call `_poll_with_stall_watchdog` directly with a fake duck-typed `proc`

`_poll_with_stall_watchdog(proc, config, *, output_path=None, on_stall=None, poll_interval=0.5)` (executor.py:1402-1409) is a free function that reads only:
- `getattr(config, "startup_stall_timeout", 0)` and `getattr(config, "stall_action", "warn")`,
- `getattr(proc, "_process", None)` → `.poll()` / `.terminate()`,
- `getattr(proc, "timeout_seconds", ...)` (the NEW ceiling read),
- `proc.wait()` at the tail (executor.py:1465).

So the cleanest M2 test is a **pure unit test with a hand-rolled fake `proc`** — no `ClaudeProcess` patching, no `execute_sprint`. This is strictly simpler than the `test_watchdog.py` integration style (which drives the whole `execute_sprint` with a fake `Popen`). The watchdog tests in `test_watchdog.py` test the OLD phase-level monitor stall path (`MonitorState`/`OutputMonitor`), NOT `_poll_with_stall_watchdog` — they are the wrong seam for M2. The right seam is direct.

### M2 setup sketch — pin the liveness guarantee in `warn` mode

The defect: a child that never produces output and never exits, with `stall_action="warn"`, spins forever (Researcher 1 M2(a)). The test must prove the loop now **terminates** and reaches `proc.wait()` within the ceiling. Patch `executor.time.sleep` to a no-op and `executor.time.monotonic` to an advancing clock so the ceiling trips deterministically without wall-time.

```python
import pytest
from unittest.mock import patch
from superclaude.cli.sprint.executor import _poll_with_stall_watchdog

class _NeverExitsProc:
    """A child that NEVER exits and NEVER produces output -> the pre-fix infinite spin."""
    def __init__(self, timeout_seconds):
        self.timeout_seconds = timeout_seconds
        self._process = self
        self._waited = False
    def poll(self):
        return None              # never exits on its own
    def terminate(self):
        pass
    def wait(self):
        self._waited = True      # the bounded tail wait (executor.py:1465)

@pytest.mark.unit
def test_warn_mode_poll_loop_is_bounded_by_proc_timeout(tmp_path):
    # warn mode (default), startup_stall_timeout enabled so the watch loop is active
    config = _make_config(tmp_path, num_phases=1)   # reuse helper; set fields below
    config.startup_stall_timeout = 1
    config.stall_action = "warn"
    proc = _NeverExitsProc(timeout_seconds=10)

    out = tmp_path / "task-out.txt"                  # never grows -> stall fires once

    # Deterministic clock: monotonic advances 5s per call so the ceiling (10s) trips fast.
    ticks = iter(float(i) * 5 for i in range(1000))
    with (
        patch("superclaude.cli.sprint.executor.time.sleep"),
        patch("superclaude.cli.sprint.executor.time.monotonic", side_effect=lambda: next(ticks)),
    ):
        _poll_with_stall_watchdog(proc, config, output_path=out)   # MUST return, not hang

    assert proc._waited, "loop did not fall through to the bounded proc.wait() (executor.py:1465)"
```

Guardrails:
- **Pre-fix this test hangs** (the `while underlying.poll() is None` loop never breaks in warn mode), which is exactly the regression-pinning behavior. To keep CI safe even if run against pre-fix code, wrap with a timeout marker or rely on the patched `monotonic` iterator exhausting (`StopIteration`) — but the cleaner statement is: the test PASSES only when the ceiling is present.
- Use the existing `executor.time.*` patch idiom — `test_executor.py:480-483` and `test_watchdog.py:100` both `patch("superclaude.cli.sprint.executor.time.sleep")` / `...time.monotonic`, confirming `time` is module-bound in `executor` and patchable there.
- Add a **companion kill-mode test** asserting `stall_action="kill"` still `underlying.terminate()`+`break`s (executor.py:1459-1464) unchanged — model the kill expectation on `test_watchdog.py:46-119` but at the direct-call level: give the fake `poll()` a flag flipped by `terminate()`.
- Optionally pin the **disabled path** (`startup_stall_timeout<=0` → plain `proc.wait()`, executor.py:1424-1426) stays a single bare wait.

### M2 — placement

New file **`tests/sprint/test_poll_watchdog_ceiling.py`** modeled on `test_turn_ledger_concurrency.py` (docstring naming the RC/finding, `from __future__ import annotations`, `import pytest`, `from superclaude.cli.sprint.executor import _poll_with_stall_watchdog`). A new file is justified because no existing module owns the *direct* `_poll_with_stall_watchdog` seam (`test_watchdog.py` owns the phase-level monitor seam, a different surface). Pull `_make_config` either by importing from `test_executor` is discouraged (cross-module helper import) — instead inline a tiny local `_make_config` copy (the `test_watchdog.py:24-43` / `test_executor.py:35-54` shape) so the new file is self-contained.

---

## M3 — Corrupted handoff file raises an unhandled exception on resume

**Fix site (per Researcher 1):** `handoff.py:62-71` (`FileHandoffStore.read`) — wrap the parse in `try/except (json.JSONDecodeError, ValueError): return None`.

### Seam — `FileHandoffStore` round-trip harness (`test_handoff_store.py`)

`test_handoff_store.py` is the exact module to extend. Its helpers:
- `_config(tmp_path)` (test_handoff_store.py:17-29): builds a `SprintConfig` with a written phase file + index. Reuse verbatim.
- `_record()` (test_handoff_store.py:32-46): a valid `HandoffRecord`. Not needed for the corrupt case (we write raw bytes), but useful for the "valid still round-trips after fix" guard.
- Pattern: `store = FileHandoffStore(config)`, write via `store.write(rec, phase=phase, task=task)`, read via `store.read(phase=phase, task=task)` (test_handoff_store.py:54-55). The on-disk path is `config.handoff_file(phase, task)` == `config.results_dir / "handoff" / "phase-1-task-T01.01.json"` (test_handoff_store.py:78-80) — write corrupt bytes there directly.

### M3 setup sketch — corrupt file degrades to `None` (== absent)

```python
from __future__ import annotations
from pathlib import Path
import pytest
from superclaude.cli.sprint.handoff import FileHandoffStore
from superclaude.cli.sprint.models import Phase, SprintConfig, TaskEntry

# reuse _config(tmp_path) from test_handoff_store.py (copy into the same module)

@pytest.mark.unit
def test_read_corrupt_json_returns_none(tmp_path: Path) -> None:
    config = _config(tmp_path)
    phase, task = config.phases[0], TaskEntry(task_id="T01.01", title="t")
    store = FileHandoffStore(config)

    path = config.handoff_file(phase, task)            # phase-1-task-T01.01.json
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"task_id": "T01.01", "phase": 1, ')   # truncated -> JSONDecodeError

    assert store.read(phase=phase, task=task) is None  # corrupt == absent (no raise)
```

Variants worth adding (cheap, same harness):
- **Empty file** (`path.write_text("")`) → `json.loads("")` raises `JSONDecodeError` → `None`.
- **Garbage bytes** (`path.write_text("not json at all")`) → `None`.
- **Valid-but-not-success degrade-to-rerun integration** (optional, stronger): assert resume re-runs the task. Researcher 1 M3(c) verified both call sites guard `if _prior is not None and is_validated_success(_prior):` (executor.py:1104, :1278), so a `None` read ⇒ task runs. A focused integration form can reuse `execute_phase_tasks` with a handoff dir pre-seeded with a corrupt file and a counting `_subprocess_factory` (the factory idiom at test_executor.py:632-638 / test_handoff_crash_consistency.py which already imports `execute_phase_tasks`) to assert the task is NOT skipped. Keep this as a second test if the unit-level `read() is None` is the primary regression pin.

### M3 — placement

Add the unit test(s) **inside `tests/sprint/test_handoff_store.py`** (reuses `_config`, the natural owner of `FileHandoffStore.read`). The optional resume-rerun integration test belongs in `tests/sprint/test_handoff_crash_consistency.py` (already imports `execute_phase_tasks` and owns the corrupt/crash-consistency theme) or alongside, marked `@pytest.mark.integration`.

---

## Verification commands (`uv run pytest`)

Per CLAUDE.md (UV only — never `python -m pytest`). Run from repo/worktree root.

Per-fix focused runs:

```bash
# M1 — new test added to test_executor.py
uv run pytest tests/sprint/test_executor.py -k "closes_handles or run_task_subprocess" -v

# M2 — new file
uv run pytest tests/sprint/test_poll_watchdog_ceiling.py -v

# M3 — handoff store
uv run pytest tests/sprint/test_handoff_store.py -v
```

Regression sweep (ensure existing watchdog/handoff/process behavior is unchanged):

```bash
uv run pytest tests/sprint/test_watchdog.py tests/sprint/test_process.py \
              tests/sprint/test_handoff_store.py tests/sprint/test_executor.py -q
```

Full sprint suite + lint/format gate (CLAUDE.md: `make lint` ≠ CI ruff format — run the format check explicitly):

```bash
uv run pytest tests/sprint/ -q
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
```

---

## Seam summary table

| Fix | Primary seam (file:line) | Test placement | Marker | Setup essence |
|---|---|---|---|---|
| **M1** | direct `_run_task_subprocess`, patch base `ClaudeProcess.__init__/start/terminate`; force `_poll_with_stall_watchdog` to raise (model: test_executor.py:1904-1963) | append to `tests/sprint/test_executor.py` | `unit` | patch `executor._poll_with_stall_watchdog` → `KeyboardInterrupt`; assert `pytest.raises` + `terminate` spy fired |
| **M2** | direct `_poll_with_stall_watchdog(fake_proc, config, output_path=...)` (executor.py:1402-1465); patch `executor.time.sleep`/`monotonic` | new file `tests/sprint/test_poll_watchdog_ceiling.py` (template: test_turn_ledger_concurrency.py) | `unit` | fake `proc` whose `poll()` never exits + non-growing output; assert loop returns and `proc.wait()` reached; companion kill-mode test |
| **M3** | `FileHandoffStore.read(phase=, task=)` over a corrupt file at `config.handoff_file(phase, task)` (model: test_handoff_store.py:49-92) | append to `tests/sprint/test_handoff_store.py` (+ optional integration in test_handoff_crash_consistency.py) | `unit` (+ `integration` for resume-rerun) | write truncated/empty/garbage bytes to handoff path; assert `read(...) is None` |

**Cross-cutting conventions confirmed:** autouse narrative stub (conftest.py:32-55) covers all new sprint modules automatically; `--strict-markers` (pyproject.toml:109) means use only registered markers — `unit`/`integration`/`slow` are the right choices; new files follow the `test_turn_ledger_concurrency.py` header shape (`from __future__ import annotations`, defect-class docstring, `-> None` typed tests, regression-naming assert messages); all three fixes are testable with `uv run pytest tests/sprint/...`.

**Nothing left Unverified.** Every file:line cited above was read at HEAD on `SprintCLIWireDead`.

Status: Complete
