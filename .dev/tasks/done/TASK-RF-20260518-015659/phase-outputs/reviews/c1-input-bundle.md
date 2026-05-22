# C1 QA Input Bundle

## Dataclass field
**File:** `src/superclaude/cli/sprint/models.py` (around L369)

Inserted between existing `stall_timeout: int = 0  # 0 = disabled` and `stall_action: str = "warn"  # "warn" or "kill"`:
```python
    startup_stall_timeout: int = 300  # 0 = disabled; fires when no events received yet (process never began streaming)
```

## Loader plumbing
**File:** `src/superclaude/cli/sprint/config.py` (signature L284-286; constructor pass-through L345-347)

Signature gained `startup_stall_timeout: int = 300,` between `stall_timeout` and `stall_action`. SprintConfig(...) constructor call gained `startup_stall_timeout=startup_stall_timeout,` in matching position.

## CLI option
**File:** `src/superclaude/cli/sprint/commands.py`

Three coordinated changes:
1. New `@click.option("--startup-stall-timeout", "startup_stall_timeout", type=int, default=300, show_default=True, help="Seconds to wait for the first event from a subprocess before treating as startup-stall (0 = disabled).")` between `--stall-timeout` and `--stall-action` decorators.
2. New parameter `startup_stall_timeout: int,` in `run(...)` signature between `stall_timeout` and `stall_action`.
3. New `startup_stall_timeout=startup_stall_timeout,` in `load_sprint_config(...)` pass-through.

## Watchdog split
**File:** `src/superclaude/cli/sprint/executor.py` (around L1365-1404 region; expanded after split)

Before: single branch gated on `config.stall_timeout > 0 AND ms.stall_seconds > config.stall_timeout AND ms.events_received > 0 AND not _stall_acted` with `[WATCHDOG] Stall detected (...)` message.

After: TWO branches:
1. **Startup-stall guard** — `if (config.startup_stall_timeout > 0 AND ms.events_received == 0 AND ms.stall_seconds > config.startup_stall_timeout AND not _stall_acted):` → `debug_log(_dbg, "startup_stall_triggered", ...)` + `[WATCHDOG] Startup-stall detected ({ms.stall_seconds:.0f}s > {config.startup_stall_timeout}s, no events received) — killing/warning phase {phase.number}` stderr message.
2. **Mid-stall guard** (renamed from original) — `if (config.stall_timeout > 0 AND ms.stall_seconds > config.stall_timeout AND ms.events_received > 0 AND not _stall_acted):` → `debug_log(_dbg, "watchdog_triggered", ...)` (event name preserved) + `[WATCHDOG] Mid-stall detected (...)` stderr (was `Stall detected`).

The `_stall_acted` single-fire reset clause (`if _stall_acted and ms.stall_seconds == 0.0: _stall_acted = False`) is unchanged — one watchdog actuation per phase across both branches.

## New tests
**Files:** `tests/sprint/test_config.py` + `tests/sprint/test_watchdog.py`

3 config tests (`TestStartupStallTimeoutDefaults`):
- `test_startup_stall_timeout_default_300` — also asserts Q1 invariant (`stall_action == "warn"`) and Q4 invariant (`stall_timeout == 0`)
- `test_startup_stall_timeout_override` — override via `load_sprint_config(startup_stall_timeout=600)`
- `test_startup_stall_timeout_zero_disables`

2 watchdog integration tests (`TestStartupStallWatchdog`):
- `test_startup_stall_fires_when_no_events_received` — config `(startup_stall_timeout=10, stall_timeout=999999, stall_action="kill")`, MonitorState `(stall_seconds=15.0, events_received=0)`, expects `SystemExit(1)` + `result.outcome == HALTED` + `exit_code == 124`.
- `test_mid_stall_unchanged_when_events_received` — config `(startup_stall_timeout=999999, stall_timeout=10, stall_action="kill")`, MonitorState `(stall_seconds=15.0, events_received=5)`, expects mid-stall branch still fires.

Tests use canonical `patch("superclaude.cli.pipeline.process.subprocess.Popen", ...)` pattern with co-patched `os.setpgrp`/`os.getpgid`/`os.killpg`. Fake Popen classes include `self.stdin = MagicMock()` as workaround for pre-existing `AttributeError` from commit 4799719 (this issue is INDEPENDENT of C1; pre-existing 3 watchdog tests fail on baseline too — verified via git stash).

## pytest results summary
**Result:** PASSED (5/5, 0.14s)

Raw: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-5-c1-pytest-output.txt`
Summary: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-5-c1-summary.md`

## QA scope

Only C1 scope — items 5.1-5.7. Phase 3 (C3 executor.py:86), Phase 4 (C4 executor.py per-task branch insertion), and Phase 6 (C2 — not yet started) are NOT in scope. The `_run_task_subprocess` body at executor.py:1086-1115 was NOT modified. The `models.py` `output_file`/`error_file` methods at L469-476 were NOT modified.
