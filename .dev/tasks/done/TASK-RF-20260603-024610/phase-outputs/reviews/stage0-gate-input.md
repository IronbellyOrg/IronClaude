# Stage 0 — Phase-Gate Input Inventory (Step PG0.1)

All entries verified to exist on disk (ls/Read). No fabricated entries.

## Source files modified in Phase 2

- `src/superclaude/cli/sprint/executor.py`
  - `setup_isolation(config, *, scope="")` — added keyword-only `scope` (H1 per-slot dirs)
  - Path A `_phase_env_vars` — merge keeps phase-scoped `CLAUDE_WORK_DIR`, adds settings+plugin keys
  - `_task_env(task, config, phase)` — new helper (single source of per-task env)
  - `_run_task_subprocess` — `env_vars=_task_env(...)` injected (Path B); `turns_consumed` now `max(count_turns_from_stream_json(output_path), 0)` (was hard-coded 0)
  - `execute_phase_tasks` — added `_env_capture: list | None = None` seam
  - import line — added `count_turns_from_stream_json`
- `src/superclaude/cli/sprint/process.py`
  - `count_turns_from_stream_json(output_path)` — new authoritative per-task turn parser
  - added `import json`, `from pathlib import Path`

## Test files modified / added

- `tests/cli/eval/test_isolation_layers_probe.py` (modified) — `test_setup_isolation_signature_pin` re-pinned to `("config","scope")` + kind/default assertions; IsolationLayers 4-field-order asserts unchanged
- `tests/sprint/e2e_real/fake_claude.py` (modified, additive) — `env_log` per-task env recording + optional `num_turns` from `FAKE_CLAUDE_NUM_TURNS`
- `tests/sprint/test_per_task_env_isolation.py` (new) — 3 assertions (env-uniqueness, concurrent-spawn repro, negative control)
- `tests/sprint/e2e_real/test_e2e_isolation_smoke.py` (new) — H2 gate 1 serial isolation smoke (real spawn)
- `tests/sprint/e2e_real/test_e2e_turn_count.py` (new) — exact turn-count e2e (turns_consumed == N)

## Discovery / result artifacts

- `phase-outputs/discovery/symbol-anchors.md`
- `phase-outputs/test-results/stage0-tests.txt` (raw pytest + lint)
- `phase-outputs/test-results/stage0-tests.md` (structured summary)

## Pass/fail/lint state (from stage0-tests.md)

- Pytest: **112 passed, 5 failed, 0 skipped** (exit 1).
- The 5 failures are ALL pre-existing baseline `.stdin` harness failures (verbatim
  on the Phase-1 already-failing list) — **ZERO regressions**.
- Lint: **PASS** (`ruff check .` → All checks passed).
