# Research 05 — Test & Verification Infrastructure

**Researcher:** R5 of 5
**Topic:** Test & Verification — existing pytest patterns for sprint/pipeline; recipes for C1–C4 fixes
**Status:** Complete

---

## 1. Test directory layout

### `tests/sprint/` (sprint runner — primary location for C1, C2, C3, C4 unit + integration tests)

`find tests/ -name "test_*.py" -path "*sprint*"` returns 45 files. Highest-line-count and most relevant:

| File | Lines | Purpose |
|------|-------|---------|
| `tests/sprint/test_executor.py` | 1456 | Executor orchestration; SprintConfig wiring; stall/watchdog integration |
| `tests/sprint/test_preflight.py` | 1209 | Preflight checks (config validation, file existence) |
| `tests/sprint/test_process.py` | 555 | **`ClaudeProcess` command-build, env, stdin, signal handler** (sprint-side) |
| `tests/sprint/test_watchdog.py` | 270 | **Watchdog kill/warn actions + `_stall_acted` reset** (existing C1-adjacent tests) |
| `tests/sprint/test_e2e_success.py` | 259 | E2E with JSONL log assertion incl. `phase_start` events |
| `tests/sprint/test_e2e_halt.py` | — | E2E halt flow + JSONL inspection |
| `tests/sprint/test_e2e_trailing.py` | 621 | Trailing-gate E2E |
| `tests/sprint/test_regression_gaps.py` | 815 | **`SprintLogger.write_phase_start` field assertions** (TestSprintLoggerPhaseStart class, ~L496–523) |
| `tests/sprint/test_models.py` | 1044 | `MonitorState`, `SprintConfig`, including stall-related model behavior |
| `tests/sprint/test_execute_sprint_integration.py` | — | High-level integration test of `execute_sprint()` |
| `tests/sprint/test_checkpoints.py` | 566 | Checkpoint logging assertions |
| `tests/sprint/test_backward_compat_regression.py` | 571 | Backward-compat for `execution_log_jsonl` / `execution_log_md` paths |

### `tests/pipeline/` (the generic `ClaudeProcess` lives here)

`find tests/ -name "test_*.py" -path "*pipeline*"` returns 33 files; most relevant:

| File | Lines | Purpose |
|------|-------|---------|
| `tests/pipeline/test_process.py` | 229 | **`ClaudeProcess` command + stdin + 200KB payload + broken-pipe tests** (pipeline-side — same `ClaudeProcess` class C2 must change) |
| `tests/pipeline/test_executor.py` | 304 | Pipeline executor |
| `tests/pipeline/test_full_flow.py` | 916 | Full pipeline flow |
| `tests/pipeline/test_process_hooks.py` | 173 | Lifecycle hooks `on_spawn` / `on_signal` / `on_exit` |
| `tests/pipeline/test_thread_safety.py` | 322 | Concurrent process invariants |

### `tests/cli/`
No `tests/cli/sprint/` or `tests/cli/pipeline/` exists. Sprint/pipeline tests live at `tests/sprint/` and `tests/pipeline/`. `tests/cli/` contains only `test_install_hooks.py`, `test_tdd_extract_prompt.py`, `test_verify_sync_hooks.py`, `tests/cli/prd/`.

---

## 2. conftest.py inventory

### `tests/conftest.py` (project-wide)
- **collect_ignore:** skips `sprint/test_property_based.py` (optional `hypothesis` dep).
- Fixtures: `sample_context`, `low_confidence_context`, `sample_implementation`, `failing_implementation`, `temp_memory_dir(tmp_path)`. **None are sprint-specific.**

### `tests/pipeline/conftest.py`
```python
@pytest.fixture
def tmp_dir(tmp_path: Path) -> Path: ...
@pytest.fixture
def make_file(tmp_path: Path): ...   # factory: _make(name, content) -> Path
```

### **`tests/sprint/conftest.py` — DOES NOT EXIST.**
Sprint tests rely on `pytest`'s built-in `tmp_path` + a private module-level `_make_config(tmp_path, **overrides)` helper, redefined in nearly every test file (e.g. `test_watchdog.py:24`, `test_process.py:26`, `test_e2e_success.py`, `test_regression_gaps.py`). **No shared sprint conftest.** Builder may add one for C1–C4 tests, but precedent says: define `_make_config()` inline in each new test file.

`tests/sprint/diagnostic/conftest.py` exists but scoped to diagnostic L0–L3 tests, not relevant here.

---

## 3. Subprocess-mock pattern (the project's canonical recipe)

**The pattern**: `patch("superclaude.cli.pipeline.process.subprocess.Popen", side_effect=factory)` where `factory` returns a hand-rolled fake class.

### Verbatim example 1 — `tests/sprint/test_watchdog.py:49–117`
```python
def test_stall_kill_action(self, tmp_path):
    config = _make_config(tmp_path, stall_timeout=10, stall_action="kill")
    poll_calls = [0]
    terminated = [False]

    class _KillPopen:
        def __init__(self):
            self.returncode = None
            self.pid = 9999
        def poll(self):
            poll_calls[0] += 1
            if terminated[0]:
                self.returncode = 1
                return 1
            return None
        def wait(self, timeout=None):
            self.returncode = 1
            return 1

    def _factory(*args, **kwargs):
        phase = config.phases[0]
        config.results_dir.mkdir(parents=True, exist_ok=True)
        config.output_file(phase).write_text("some output\n")
        return _KillPopen()

    stalled_state = MonitorState(stall_seconds=15.0, events_received=5)

    with (
        patch("superclaude.cli.sprint.executor.shutil.which", return_value="/usr/bin/claude"),
        patch("superclaude.cli.pipeline.process.subprocess.Popen", side_effect=_factory),
        patch("superclaude.cli.pipeline.process.os.setpgrp"),
        patch("superclaude.cli.pipeline.process.os.getpgid", return_value=9999),
        patch("superclaude.cli.pipeline.process.os.killpg",
              side_effect=lambda *a, **k: terminated.__setitem__(0, True)),
        patch("superclaude.cli.sprint.notify._notify"),
        patch("superclaude.cli.sprint.executor.SprintLogger") as logger_cls,
        patch("superclaude.cli.sprint.executor.time.sleep"),
        patch("superclaude.cli.sprint.executor.OutputMonitor") as monitor_cls,
    ):
        monitor_mock = MagicMock()
        monitor_mock.state = stalled_state
        monitor_cls.return_value = monitor_mock
        ...
        with pytest.raises(SystemExit) as exc:
            execute_sprint(config)
```

**Key invariants this pattern enforces:**
- Patch path is **`superclaude.cli.pipeline.process.subprocess.Popen`** (NOT `subprocess.Popen` directly, NOT the sprint module).
- Always patch `os.setpgrp` alongside it (sprint code calls `os.setpgrp` in `preexec_fn`).
- For kill paths: also patch `os.getpgid` + `os.killpg`.
- Mock `executor.SprintLogger`, `executor.time.sleep`, `executor.OutputMonitor` to isolate executor logic.
- Patch `executor.shutil.which` so the `claude` binary check passes.

### Verbatim example 2 — real subprocess stand-in (`tests/pipeline/test_process.py:176–193`)
For tests that need genuine end-to-end subprocess behavior without mocking `Popen`, the project uses a Python interpreter stand-in via `patch.object(ClaudeProcess, "build_command", ...)`:
```python
def test_start_writes_prompt_to_stdin(self, tmp_path):
    prompt = "Hello from stdin!\nLine 2."
    stand_in = [sys.executable, "-c", "import sys; sys.stdout.write(sys.stdin.read())"]
    p = ClaudeProcess(prompt=prompt, output_file=tmp_path / "out.txt", error_file=tmp_path / "err.txt")
    with patch.object(ClaudeProcess, "build_command", return_value=stand_in):
        p.start()
        rc = p.wait()
    assert rc == 0
    assert (tmp_path / "out.txt").read_text(encoding="utf-8") == prompt
```
**This is the pattern C2 should reuse** (two real subprocesses each emit a known line, verify both lines remain in their respective files).

---

## 4. JSONL output assertion pattern

The canonical recipe used in `test_e2e_success.py`, `test_e2e_halt.py`, `test_regression_gaps.py`:

```python
import json
events = [
    json.loads(line)
    for line in config.execution_log_jsonl.read_text().strip().split("\n")
    if line.strip()
]
phase_start_events = [e for e in events if e["event"] == "phase_start"]
assert len(phase_start_events) == 3
assert [e["phase"] for e in phase_start_events] == [1, 2, 3]
```

**Field-shape assertion (verbatim from `test_regression_gaps.py:499–523`):**
```python
def test_write_phase_start_fields(self, tmp_path):
    config = _make_config(tmp_path, num_phases=1)
    logger = SprintLogger(config)
    phase = config.phases[0]
    started_at = datetime.now(timezone.utc)
    logger.write_phase_start(phase, started_at)
    events = [
        json.loads(line)
        for line in config.execution_log_jsonl.read_text().strip().split("\n")
        if line.strip()
    ]
    assert len(events) == 1
    ev = events[0]
    assert ev["event"] == "phase_start"
    assert ev["phase"] == phase.number
    assert ev["phase_name"] == phase.display_name
    assert "timestamp" in ev
    assert "phase_file" in ev
```

**Path:** `config.execution_log_jsonl` resolves to `<release_dir>/execution-log.jsonl` (asserted at `test_executor.py:1364`, `test_backward_compat_regression.py:570`).

---

## 5. Key code sites (for the 4 fixes)

| Site | File:Line | Code | Relevance |
|------|-----------|------|-----------|
| Pipeline `ClaudeProcess.start` opens stdout truncating | `src/superclaude/cli/pipeline/process.py:120,122` | `self._stdout_fh = open(self.output_file, "w")` | **C2** — second `start()` truncates the first's file |
| Executor timeout site #1 | `src/superclaude/cli/sprint/executor.py:86` | `timeout_seconds=self._config.max_turns * 60,` | **C3** — formula A |
| Executor timeout site #2 | `src/superclaude/cli/sprint/executor.py:1106` | `timeout_seconds=config.max_turns * 120 + 300,` | **C3** — formula B (sprint's canonical, matches `ClaudeProcess` default 6300) |
| Stall watchdog check | `src/superclaude/cli/sprint/executor.py:1367–1398` | `if config.stall_timeout > 0 and ms.stall_seconds > config.stall_timeout` | **C1** — current single-timeout logic; needs split into startup_stall vs idle_stall |
| `write_phase_start` emitter | `src/superclaude/cli/sprint/logging_.py:59–69` | Emits `{event:"phase_start", phase, phase_name, phase_file, timestamp}` | **C4** — already exists; C4 is about CALLING it at the right point or adding field |
| `write_phase_start` call site | `src/superclaude/cli/sprint/executor.py:1328` | `logger.write_phase_start(phase, started_at)` | **C4** — invocation point |
| `MonitorState` (phase_started_at, events_received) | `src/superclaude/cli/sprint/models.py:609,639` | Already tracks `events_received` and 120s startup grace | **C1** — model already supports the split; needs config knob |
| `SprintConfig.stall_timeout` default | `src/superclaude/cli/sprint/models.py:369` | `stall_timeout: int = 0  # 0 = disabled` | **C1** — current default is OFF |

---

## 6. Test recipes for the 4 fixes (C1–C4)

### C1 — `stall_timeout` default + watchdog split (startup vs idle)

**Unit test** (extend `SprintConfig` defaults + new `startup_stall_timeout` field):

- **File:** `tests/sprint/test_config.py` (existing) and `tests/sprint/test_models.py` (existing)
- **Test functions:**
  - `test_startup_stall_timeout_default_value` — assert `SprintConfig().startup_stall_timeout == <new default>`
  - `test_stall_timeout_default_changed` — confirm new default (was 0; assert new non-zero value)
- **Assertions (3–5):**
  1. `SprintConfig(...).startup_stall_timeout == EXPECTED_DEFAULT`
  2. `SprintConfig(...).stall_timeout == EXPECTED_IDLE_DEFAULT`
  3. Override accepted via kwarg: `SprintConfig(..., startup_stall_timeout=300).startup_stall_timeout == 300`
  4. `0` still means disabled for both knobs.

**Integration test** (watchdog split behavior):

- **File:** `tests/sprint/test_watchdog.py` (existing — extend with new `TestStartupStallWatchdog` class)
- **Test function:** `test_startup_watchdog_fires_when_no_events_received`
- **Pattern:** Copy `TestWatchdogKillAction.test_stall_kill_action` structure (verbatim recipe above).
- **Differences:** Use `MonitorState(stall_seconds=<startup_timeout+5>, events_received=0, phase_started_at=time.monotonic() - <startup_timeout+5>)` to simulate "process never emitted anything." Configure `config = _make_config(tmp_path, startup_stall_timeout=10, stall_timeout=999999)` so only startup branch can trigger.
- **Assertions (5):**
  1. `pytest.raises(SystemExit)` with `exc.value.code == 1`.
  2. `result.outcome == SprintOutcome.HALTED`.
  3. `result.phase_results[0].exit_code == 124` (timeout sentinel — matches existing watchdog test).
  4. Exactly one event in JSONL with `event` indicating startup stall (`stall_kill` / new event name from C1 spec).
  5. Companion test: `events_received > 0` and `stall_seconds > startup_stall_timeout` does NOT trigger startup branch (idle branch governs).

---

### C2 — Output-file collision (`open(output_file, "w")` truncates)

**Unit test** — two `ClaudeProcess.start()` calls with the SAME `output_file` must not clobber each other (or, if same path is the bug, the fix must enforce unique paths and tests must catch).

- **File:** `tests/pipeline/test_process.py` (existing — add `TestClaudeProcessOutputFileCollision` class)
- **Test function:** `test_two_starts_same_output_file_do_not_clobber` (assuming fix appends or refuses) OR `test_two_starts_distinct_output_files` (assuming fix mandates unique paths).
- **Pattern:** Reuse the **stdin stand-in** pattern from `tests/pipeline/test_process.py:176–193` — two real subprocesses, each echoes a known marker line. Use `patch.object(ClaudeProcess, "build_command", return_value=stand_in)`.
- **Assertions (4):**
  1. Both subprocesses exit with `rc == 0`.
  2. Marker line from process A is present in process A's output file (`"AAA" in (tmp_path / "out_a.txt").read_text()`).
  3. Marker line from process B is present in process B's output file (`"BBB" in (tmp_path / "out_b.txt").read_text()`).
  4. Neither file contains both markers (no cross-contamination), OR if the contract is "same file gets appended": file contains BOTH markers in order.

**Integration test** — multi-phase sprint where two phases write distinct outputs without collision.

- **File:** `tests/sprint/test_executor.py` (existing — add to `TestExecuteSprintOutputFiles` or new class)
- **Test function:** `test_multi_phase_output_files_isolated`
- **Pattern:** `_popen_factory_all_pass(config)` with 2+ phases (see `test_e2e_success.py:114`).
- **Assertions (4):**
  1. After `execute_sprint(config)`, `config.output_file(phase_1).exists()` and `config.output_file(phase_2).exists()`.
  2. `config.output_file(phase_1).read_text()` contains phase-1-specific marker only.
  3. `config.output_file(phase_2).read_text()` contains phase-2-specific marker only.
  4. JSONL log shows `output_bytes > 0` for both phases (asserts `phase_complete` events).

---

### C3 — Timeout reconciliation (`executor.py:86` vs `executor.py:1106`)

The two formulas:
- L86: `max_turns * 60` (one minute per turn, no startup pad)
- L1106: `max_turns * 120 + 300` (two minutes per turn + 5 minute startup pad)
- `ClaudeProcess.__init__` default: `timeout_seconds=6300` = `50 * 120 + 300` (matches L1106 with `max_turns=50`).

The L1106 formula is canonical (matches `ClaudeProcess` default and the sprint contract docs).

**Unit test** — the formula constants are centralized and identical at both call sites.

- **File:** `tests/sprint/test_executor.py` (existing — add `TestTimeoutFormulaConsistency` class)
- **Test functions:**
  - `test_timeout_formula_identical_at_both_callsites`
  - `test_timeout_formula_matches_claudeprocess_default_for_max_turns_50`
- **Pattern:** Either (a) call the new shared helper `_compute_timeout(max_turns)` from both sites and assert equality, OR (b) build a `ClaudeProcess` via the L86 path and one via the L1106 path with same `max_turns` and assert `.timeout_seconds` is equal.
- **Assertions (4):**
  1. `compute_timeout(50) == 6300` (matches L1106 + ClaudeProcess default).
  2. `compute_timeout(100) == 12300` (matches `test_process.py:test_timeout_calculation_custom`).
  3. The L86 callsite, after refactor, yields the same value as the L1106 callsite for `max_turns ∈ {1, 50, 100, 500}`.
  4. The formula constants `60` and `300` (or whatever names they get) are sourced from a single module-level constant (assertion: `executor.TURN_TIMEOUT_SECONDS == 120` AND `executor.STARTUP_PAD_SECONDS == 300`).

**Integration test** — both callsites in real execution produce a `ClaudeProcess` with the canonical timeout.

- **File:** `tests/sprint/test_executor.py` (existing)
- **Test function:** `test_remediation_step_uses_canonical_timeout` (L86 is in remediation Step construction)
- **Pattern:** Spy on `ClaudeProcess.__init__` (or the `Step.timeout_seconds` field), trigger the remediation path with a known `max_turns`, assert the timeout matches the canonical formula.
- **Assertions (3):**
  1. Spy captures `timeout_seconds` from the remediation `Step`.
  2. Captured value `== max_turns * 120 + 300`.
  3. Same `max_turns` in the main execution path (L1106) yields the same captured value.

---

### C4 — `phase_start` JSONL event shape

A `write_phase_start` emitter already exists (`logging_.py:59`) and is called from `executor.py:1328`; a field-shape test already exists in `test_regression_gaps.py:499–523`. **C4 is presumably about adding a NEW field (e.g., `expected_timeout_seconds`, `startup_stall_timeout`, or `tasks`) OR ensuring the event fires for a previously-uncovered path** — confirm exact intent from C4 spec before writing tests.

**Unit test** — extend the existing `TestSprintLoggerPhaseStart` class:

- **File:** `tests/sprint/test_regression_gaps.py` (existing class `TestSprintLoggerPhaseStart` at L496)
- **Test function:** `test_write_phase_start_includes_<new_field>` (or `test_write_phase_start_emitted_for_<new_path>`)
- **Pattern:** Copy the existing `test_write_phase_start_fields` recipe verbatim (verbatim above in §4).
- **Assertions (5):**
  1. Exactly one event in the JSONL file.
  2. `ev["event"] == "phase_start"`.
  3. `ev["phase"] == phase.number`.
  4. `ev["phase_name"] == phase.display_name` and `ev["phase_file"] == str(phase.file)`.
  5. **New field per C4 spec** is present with the right type, e.g. `assert isinstance(ev["<new_field>"], <type>)` and matches the value derived from `config`/`phase`.

**Integration test** — `phase_start` event emitted by full `execute_sprint` for every phase, in order.

- **File:** `tests/sprint/test_e2e_success.py` (existing — already asserts at L144–147; add an assertion or a new test alongside).
- **Test function:** `test_phase_start_event_emitted_for_each_phase_with_<new_field>`
- **Pattern:** Verbatim from `test_jsonl_events_for_each_phase` at L114–163.
- **Assertions (5):**
  1. `phase_start_events = [e for e in events if e["event"] == "phase_start"]; len(...) == NUM_PHASES`.
  2. `[e["phase"] for e in phase_start_events] == [1, 2, 3]` (ordered).
  3. Each event precedes its corresponding `phase_complete` in line-order (`events.index(start) < events.index(complete)`).
  4. The new field from C4 is present in EVERY `phase_start` event.
  5. JSONL line count is consistent with C4's contract (e.g. `len(events) == 1 + 2*N + 1` for `sprint_start` + N×(phase_start, phase_complete) + `sprint_complete`).

---

## 7. Test commands & markers

### Commands (from CLAUDE.md, verified against `pyproject.toml`)
- `uv run pytest tests/sprint/ -v` — sprint suite (replaces non-existent `tests/cli/sprint/`)
- `uv run pytest tests/pipeline/ -v` — pipeline suite
- `uv run pytest tests/sprint/test_watchdog.py tests/sprint/test_executor.py tests/pipeline/test_process.py -v` — narrow loop for C1–C4
- `make test` — full suite
- `make lint && make format` — gates before commit

### Markers (`pyproject.toml:109–133`) registered with `--strict-markers`
- **Relevant to C1–C4:** `unit`, `integration`. The pytest_plugin auto-marks `tests/sprint/` files as `integration` (anything under `/integration/`) — but `tests/sprint/` is NOT under `/integration/`, so the plugin's auto-mark probably does NOT apply. Verify with `uv run pytest --collect-only -q tests/sprint/test_watchdog.py` if uncertain. For C1–C4 new tests: no marker required.
- `confidence_check`, `self_check`, `reflexion` — PM Agent markers; **not needed** for sprint runner fixes.
- `slow`, `performance`, `nfr_benchmark` — only if a test runs >1s wallclock.

### Pytest fixture availability for new tests
- `tmp_path` (built-in pytest) — used by every sprint test.
- No `sprint`-specific conftest fixtures; reuse the inline `_make_config(tmp_path, **overrides)` helper pattern (verbatim from `test_watchdog.py:24–43`).

---

## 8. `make sync-dev` / `make verify-sync` — does NOT apply to C1–C4

From `Makefile` and `CLAUDE.md`:
> `make sync-dev` — `src/superclaude/{skills,agents,commands}` → `.claude/`

The C1–C4 fixes touch **Python source** in:
- `src/superclaude/cli/sprint/` (executor.py, logging_.py, models.py, config.py)
- `src/superclaude/cli/pipeline/` (process.py)

These directories are **NOT under** `{skills,agents,commands}` and therefore are **NOT synced to `.claude/`**. They are installed via `make dev` (editable install) and imported directly by `pytest`.

**Builder MUST NOT include `make sync-dev` or `make verify-sync` items in the C1–C4 checklist.** Including them would be wasted work and would confuse the gate sequence.

`make verify-sync` IS appropriate ONLY if the fix also edits a skill/agent/command file (e.g. updating a `task-builder` or sprint-related skill to reference the new behavior). For pure executor/process/logger code, skip.

---

## Summary

**Existing infrastructure is rich and the patterns are clear:**

1. **No sprint conftest** — each new test redefines `_make_config(tmp_path, **overrides)` inline (verbatim recipe in `test_watchdog.py:24`).
2. **Canonical subprocess mock**: `patch("superclaude.cli.pipeline.process.subprocess.Popen", side_effect=factory)` with a hand-rolled fake `Popen` class providing `poll()` / `wait()` / `pid` / `returncode`; always co-patch `os.setpgrp` and (for kill paths) `os.getpgid` + `os.killpg`.
3. **Real-subprocess pattern** for collision testing (C2): `patch.object(ClaudeProcess, "build_command", return_value=[sys.executable, "-c", ...])` — verbatim in `tests/pipeline/test_process.py:176–193`.
4. **JSONL assertion**: `[json.loads(line) for line in config.execution_log_jsonl.read_text().strip().split("\n") if line.strip()]`, then filter by `e["event"] == "phase_start"`.
5. **Existing tests to extend**:
   - C1 → `tests/sprint/test_watchdog.py` (add `TestStartupStallWatchdog`) + `tests/sprint/test_config.py` / `test_models.py` for defaults.
   - C2 → `tests/pipeline/test_process.py` (add `TestClaudeProcessOutputFileCollision`) + `tests/sprint/test_executor.py` integration.
   - C3 → `tests/sprint/test_executor.py` (add `TestTimeoutFormulaConsistency`).
   - C4 → `tests/sprint/test_regression_gaps.py` (extend `TestSprintLoggerPhaseStart`) + `tests/sprint/test_e2e_success.py` integration.
6. **Run loop**: `uv run pytest tests/sprint/ tests/pipeline/ -v`; `make test` for full validation; `make lint && make format` before commit.
7. **`make sync-dev` / `make verify-sync` are NOT needed** for these Python source changes — only `.claude/{skills,agents,commands}` artifacts require sync.

**Key code citations** (file:line) re-verified this turn:
- `src/superclaude/cli/pipeline/process.py:120,122` — `open(self.output_file, "w")` truncating mode (C2 root cause).
- `src/superclaude/cli/sprint/executor.py:86` — `max_turns * 60` (C3 wrong formula).
- `src/superclaude/cli/sprint/executor.py:1106` — `max_turns * 120 + 300` (C3 canonical formula).
- `src/superclaude/cli/sprint/executor.py:1367–1398` — single-formula stall check (C1 needs split).
- `src/superclaude/cli/sprint/logging_.py:59–69` — existing `write_phase_start` emitter (C4 baseline).
- `src/superclaude/cli/sprint/models.py:369` — `stall_timeout: int = 0` (C1 current default).
