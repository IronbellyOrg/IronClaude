# C2 QA Input Bundle

## New helpers
**File:** `src/superclaude/cli/sprint/models.py` (inserted between `error_file` (L473) and `result_file` (L478))

```python
    def task_output_file(self, phase: Phase, task: "TaskEntry") -> Path:
        return self.results_dir / f"phase-{phase.number}-task-{task.task_id}-output.txt"

    def task_error_file(self, phase: Phase, task: "TaskEntry") -> Path:
        return self.results_dir / f"phase-{phase.number}-task-{task.task_id}-errors.txt"
```

Uses forward-reference string `"TaskEntry"` because `TaskEntry` is defined later in the same module (at L25-37) — this is a defensive measure even though Python typically resolves dataclass annotations lazily.

## Executor migration
**File:** `src/superclaude/cli/sprint/executor.py` inside `_run_task_subprocess` (L1086-1115)

Three line changes:
1. L1101: `output_file=config.output_file(phase),` → `output_file=config.task_output_file(phase, task),`
2. L1102: `error_file=config.error_file(phase),` → `error_file=config.task_error_file(phase, task),`
3. L1114: `output_path = config.output_file(phase)` → `output_path = config.task_output_file(phase, task)`

The `timeout_seconds=config.max_turns * 120 + 300` at L1106 (C3 canonical) is preserved unchanged.

## Per-phase reference unchanged
**File:** `src/superclaude/cli/sprint/executor.py:1323` (in `execute_sprint`'s per-phase branch)
```python
proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
```
This is the sprint `ClaudeProcess` SUBCLASS at `src/superclaude/cli/sprint/process.py:108-122` which calls `super().__init__(output_file=config.output_file(phase), error_file=config.error_file(phase), ...)`. **This path was NOT modified** — the per-phase fallback continues to use phase-scoped paths.

## Existing output_file unchanged
**File:** `src/superclaude/cli/sprint/models.py` lines 472-476

```python
    def output_file(self, phase: Phase) -> Path:
        return self.results_dir / f"phase-{phase.number}-output.txt"

    def error_file(self, phase: Phase) -> Path:
        return self.results_dir / f"phase-{phase.number}-errors.txt"
```

Unmodified. The 17 existing callers identified by Researcher 3 IP-2 are not affected (additive helpers — Q2 mandate).

## New tests (5 total)

### tests/sprint/test_models.py — `TestTaskOutputFileHelpers` (3 tests)
- `test_task_output_file_generates_per_task_path` — asserts `.name == "phase-2-task-T02.05-output.txt"` and parent equals `config.results_dir`
- `test_distinct_tasks_get_distinct_paths` — asserts T02.05 ≠ T02.06 paths
- `test_legacy_output_file_unchanged` — Q2 invariant: `output_file(phase).name == "phase-2-output.txt"` still works

### tests/pipeline/test_process.py — `TestClaudeProcessOutputFileCollision` (1 test — LOAD-BEARING on C2)
- `test_two_starts_distinct_output_files_preserve_both_outputs` — derives paths via `config.task_output_file()`, asserts up-front `out_a != out_b` and `err_a != err_b`, spawns 2 real subprocesses via `sys.executable -c "stdin echo"` stand-in pattern from `tests/pipeline/test_process.py:158-160`, asserts: (a) both return 0, (b) `text_a == "AAA"`, (c) `text_b == "BBB"`, (d) cross-contamination guards `"BBB" not in text_a` and `"AAA" not in text_b`.

### tests/sprint/test_executor.py — module-level `test_run_task_subprocess_uses_task_output_file` (1 test)
- Patches `superclaude.cli.pipeline.process.ClaudeProcess.__init__` to capture kwargs and pre-populate `_process = MagicMock(returncode=0)` + `_stdout_fh=None` + `_stderr_fh=None`
- Patches `.start` and `.wait` to no-op
- Pre-creates `config.task_output_file(phase, task)` so the post-subprocess `.stat()` doesn't crash
- Asserts: (a) `captured["output_file"] == config.task_output_file(phase, task)`, (b) `captured["error_file"] == config.task_error_file(phase, task)`, (c) NOT equal to phase-scoped paths (negative), (d) `captured["timeout_seconds"] == config.max_turns * 120 + 300` (C3 consistency preserved)

## pytest results summary

**Result:** PASSED (5/5, 0.15s)

Raw: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-6-c2-pytest-output.txt`
Summary: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-6-c2-summary.md`

## QA scope

Only C2 scope — items 6.1-6.6. C3 (Phase 3), C4 (Phase 4), C1 (Phase 5) are PRIOR work and not in C2 scope. Specifically: do NOT re-verify C1 watchdog split or new field, C3 formula change at L86, or C4 phase_start emission at per-task branch — those have already passed their own gates G1/G2/G3.
