# Research: Sprint Executor Path Routing

**Investigation type:** Code Tracer
**Scope:** executor.py, process.py, config.py
**Status:** Complete
**Date:** 2026-04-03

---

## 1. Entry Point: `execute_sprint()` — Path Divergence

**File:** `src/superclaude/cli/sprint/executor.py`
**Function:** `execute_sprint()` (line 1112)
**Divergence point:** lines 1201-1233

The main orchestration loop iterates over `config.active_phases`. For each phase with `execution_mode == "claude"`, it calls `_parse_phase_tasks()` at line 1203:

```python
tasks = _parse_phase_tasks(phase, config)
if tasks:
    # PATH A: Per-task execution
    ...
    task_results, remaining, phase_gate_results = execute_phase_tasks(...)
    ...
    continue

# PATH B: Whole-phase ClaudeProcess (lines 1236+)
isolation_dir = config.results_dir / ".isolation" / f"phase-{phase.number}"
...
proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
```

**Decision logic:** `_parse_phase_tasks()` returns `list[TaskEntry]` if the phase file contains `### T<PP>.<TT>` headings, or `None` if none are found. The truthiness of the returned list determines the path.

**Path A (per-task):** Entered when `tasks` is non-empty. Delegates to `execute_phase_tasks()`.
**Path B (whole-phase):** Entered when `tasks` is `None` (no task headings found). Launches a single `ClaudeProcess` for the entire phase.

---

## 2. `_parse_phase_tasks()` — The Gate Function

**File:** `src/superclaude/cli/sprint/executor.py`, line 1095
**Delegates to:** `config.parse_tasklist()` from `src/superclaude/cli/sprint/config.py`

```python
def _parse_phase_tasks(phase: Phase, config: SprintConfig) -> list[TaskEntry] | None:
    from .config import parse_tasklist
    if not phase.file.exists():
        return None
    content = phase.file.read_text(encoding="utf-8", errors="replace")
    tasks = parse_tasklist(content, execution_mode=phase.execution_mode)
    return tasks if tasks else None
```

Reads the phase file, passes it to `parse_tasklist()`. Returns `None` for empty results, triggering Path B.

---

## 3. `parse_tasklist()` and `_TASK_HEADING_RE` — Task Inventory Parser

**File:** `src/superclaude/cli/sprint/config.py`, line 306
**Regex:** `_TASK_HEADING_RE` at line 281

```python
_TASK_HEADING_RE = re.compile(
    r"^###\s+(T\d{2}\.\d{2})\s*(?:--|-\u2014|\u2014)\s*(.+)",
    re.MULTILINE,
)
```

This regex matches `### T01.01 -- Task Title` headings (with `--`, em-dash, or mixed dash variants). For each match, the parser extracts:

- **task_id** (group 1): e.g., `T01.01`
- **title** (group 2): e.g., `Task Title`
- **description**: From `**Deliverables:**` section within the task block
- **dependencies**: From `**Dependencies:**` field, parsed as `T<PP>.<TT>` references
- **command**: From `**Command:**` field (required for `python` mode)
- **classifier**: From `| Classifier | value |` table row

Returns a `list[TaskEntry]` dataclass instances. Returns empty list if no headings found.

**TaskEntry dataclass** (`src/superclaude/cli/sprint/models.py`, line 26):
```
task_id: str, title: str, description: str = "", dependencies: list[str] = [],
command: str = "", classifier: str = ""
```

---

## 4. Path A: Per-Task Execution via `execute_phase_tasks()`

**File:** `src/superclaude/cli/sprint/executor.py`, line 912
**Subprocess spawner:** `_run_task_subprocess()` at line 1053

### 4a. The Orchestration Loop (`execute_phase_tasks`)

Iterates over `tasks`, for each task:
1. Budget check via `TurnLedger.can_launch()` -- skips remaining tasks if exhausted
2. Debits `minimum_allocation` upfront
3. Calls `_subprocess_factory(task, config, phase)` if provided (testing), otherwise `_run_task_subprocess(task, config, phase)`
4. Determines `TaskStatus` from exit code (0=PASS, 124=INCOMPLETE, else FAIL)
5. Reconciles actual turn consumption against pre-allocation
6. Runs post-task wiring hook and anti-instinct hook

### 4b. `_run_task_subprocess()` — The Minimal Prompt (CRITICAL FINDING)

**File:** `src/superclaude/cli/sprint/executor.py`, line 1053

```python
def _run_task_subprocess(task, config, phase):
    prompt = (
        f"Execute task {task.task_id}: {task.title}\n"
        f"From phase file: {phase.file}\n"
        f"Description: {task.description}\n"
    )
```

**This is the 3-line prompt.** It contains:
1. Task ID and title
2. Phase file path
3. Task description (from `**Deliverables:**` section, often empty or brief)

**What is MISSING from this prompt:**
- No `/sc:task-unified` command invocation
- No Sprint Context block (sprint name, phase number, artifact root, prior-phase dirs)
- No Execution Rules (tier-based behavior: STRICT/STANDARD/LIGHT/EXEMPT)
- No Scope Boundary instructions
- No Result File instructions
- No prior task context (from `build_task_context()`)
- No compliance mode or strategy flags
- No instruction to stop after completing the task

### 4c. ClaudeProcess Construction in `_run_task_subprocess()` — Bypass Pattern

Lines 1070-1085 reveal an unusual construction pattern:

```python
proc = ClaudeProcess.__new__(ClaudeProcess)   # Skip __init__
proc.config = config
proc.phase = phase
from superclaude.cli.pipeline.process import ClaudeProcess as _Base
_Base.__init__(
    proc,
    prompt=prompt,
    output_file=config.output_file(phase),
    error_file=config.error_file(phase),
    ...
)
```

This uses `__new__` to create the sprint `ClaudeProcess` instance but then calls the **pipeline base** `_Base.__init__()` directly, bypassing the sprint `ClaudeProcess.__init__()` entirely. This means:
- The sprint-specific `build_prompt()` method is **never called**
- No lifecycle hooks (`on_spawn`, `on_signal`, `on_exit`) are wired
- No `env_vars` isolation is passed to the base constructor

The `_Base.__init__()` stores the raw 3-line prompt and passes it through `build_command()` which constructs:
```
claude --print --verbose --dangerously-skip-permissions --no-session-persistence
       --tools default --max-turns <N> --output-format stream-json -p <prompt>
```

### 4d. Output File Collision

Both `_run_task_subprocess()` and Path B use `config.output_file(phase)` and `config.error_file(phase)`. Since per-task mode runs **multiple tasks per phase**, each task overwrites the previous task's output and error files. This means only the last task's output survives on disk.

---

## 5. Path B: Whole-Phase Execution via `ClaudeProcess`

**File:** `src/superclaude/cli/sprint/executor.py`, lines 1236-1489
**Prompt builder:** `src/superclaude/cli/sprint/process.py`, `ClaudeProcess.build_prompt()` line 123

### 5a. ClaudeProcess Construction

```python
proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
```

This calls the sprint `ClaudeProcess.__init__()` (line 97 of `process.py`), which:
1. Calls `self.build_prompt()` to construct the full prompt
2. Passes it to the pipeline base `__init__()` with all lifecycle hooks wired
3. Includes `env_vars` for isolation

### 5b. `build_prompt()` — The Rich Prompt

**File:** `src/superclaude/cli/sprint/process.py`, line 123

The prompt includes:
1. **Command invocation:** `/sc:task-unified Execute all tasks in @{phase_file} --compliance strict --strategy systematic`
2. **Sprint Context block:** sprint name, phase number, artifact root, results dir, prior-phase dirs
3. **Execution Rules:** tier-based behavior (STRICT stops on fail, others log and continue)
4. **Scope Boundary:** "After completing all tasks, STOP immediately"
5. **Important notes:** multi-phase awareness, no re-execution of prior work
6. **Result File instructions:** exact path and content format (`EXIT_RECOMMENDATION: CONTINUE/HALT`)

### 5c. Isolation and Monitoring

Path B also sets up:
- Per-phase isolation directory with `CLAUDE_WORK_DIR` env var
- OutputMonitor thread for progress tracking
- Poll loop with TUI updates at ~2 Hz
- Stall watchdog with configurable timeout/action
- Phase result file checking and crash recovery

---

## 6. `build_task_context()` — Confirmed Dead Code

**File:** `src/superclaude/cli/sprint/process.py`, line 245

Grep confirms zero callers across the entire `src/` tree. The function is defined and documented but never invoked. It was designed to inject prior task results into prompts for cross-task context, but `_run_task_subprocess()` does not call it. Neither does `execute_phase_tasks()`.

Related dead code:
- `get_git_diff_context()` (line 310) — only called by `build_task_context()`
- `compress_context_summary()` (line 335) — only called by `build_task_context()`

All three functions form a dead context-injection subsystem.

---

## 7. Pipeline Base: `ClaudeProcess.build_command()`

**File:** `src/superclaude/cli/pipeline/process.py`, line 71

```python
def build_command(self) -> list[str]:
    cmd = [
        "claude", "--print", "--verbose",
        self.permission_flag,
        "--no-session-persistence",
        "--tools", "default",
        "--max-turns", str(self.max_turns),
        "--output-format", self.output_format,
        "-p", self.prompt,
    ]
    if self.model:
        cmd.extend(["--model", self.model])
    cmd.extend(self.extra_args)
    return cmd
```

The prompt string (whether 3-line or rich) is passed verbatim as the `-p` argument. The `build_env()` method (line 93) strips `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` to prevent nested session detection.

---

## Gaps and Questions

### Critical Gaps

1. **Path A prompt is severely underspecified.** The 3-line prompt in `_run_task_subprocess()` gives the worker subprocess no behavioral instructions, no compliance tier guidance, no scope boundaries, and no result file instructions. The worker is essentially told "execute task T01.01: Some Title" with nothing else. This is a significant functional gap compared to Path B.

2. **`build_task_context()` is dead code.** The entire context injection subsystem (3 functions, ~130 lines) was built but never wired into the execution path. Per-task workers have no visibility into what prior tasks accomplished.

3. **Output file collision in Path A.** All tasks in a phase write to the same `config.output_file(phase)` and `config.error_file(phase)`. Only the last task's output persists. This prevents post-mortem analysis of earlier tasks.

4. **`_run_task_subprocess()` bypasses sprint ClaudeProcess.__init__().** The `__new__` + base `__init__` pattern is a workaround to avoid calling `build_prompt()`, but it also skips lifecycle hooks and env_vars isolation. This is tech debt.

5. **No lifecycle hooks in Path A.** The `_make_spawn_hook`, `_make_signal_hook`, and `_make_exit_hook` factories are only wired in Path B via the sprint `ClaudeProcess.__init__()`. Path A subprocesses have no debug logging for spawn/signal/exit events.

### Design Questions

1. Should Path A use `build_prompt()` (or a task-scoped variant) to generate richer prompts per task?
2. Should `build_task_context()` be wired into `_run_task_subprocess()` to give each task visibility into prior results?
3. Should per-task output files use task-specific paths (e.g., `config.output_file(phase, task_id)`) to avoid collision?
4. Is the `__new__` bypass pattern intentional or a temporary expedient? Should `_run_task_subprocess()` construct a proper sprint `ClaudeProcess` with hooks?

### Integration Opportunities

1. **Prompt enrichment hook:** `_run_task_subprocess()` is the natural injection point for enriched per-task prompts. A `build_task_prompt(task, phase, config, prior_results)` function could combine the task metadata with Sprint Context, Execution Rules, and prior task context.

2. **Context injection wiring:** `build_task_context()` already exists and is well-designed. Wiring it into `execute_phase_tasks()` requires passing accumulated `task_results` to `_run_task_subprocess()` and calling `build_task_context(prior_results)` to prepend context to the prompt.

3. **Per-task output paths:** The `SprintConfig` model could be extended with a `task_output_file(phase, task_id)` method to generate unique output paths per task.

4. **Proper ClaudeProcess construction:** `_run_task_subprocess()` could construct the sprint `ClaudeProcess` normally (calling `__init__`) but with a task-scoped `build_prompt()` override or parameter.

---

## Summary

The sprint executor pipeline has a clean two-path architecture routed by the presence of `### T<PP>.<TT>` headings in phase files:

- **Path A (per-task):** `execute_sprint()` -> `_parse_phase_tasks()` -> `execute_phase_tasks()` -> `_run_task_subprocess()`. Sends a **minimal 3-line prompt** (`Execute task T01.01: Title / From phase file: /path / Description: ...`) to `claude --print -p` workers. No behavioral instructions, no context injection, no lifecycle hooks, no output isolation.

- **Path B (whole-phase):** `execute_sprint()` -> `ClaudeProcess(config, phase)` -> `build_prompt()`. Sends a **rich ~40-line prompt** with `/sc:task-unified` invocation, Sprint Context, Execution Rules, Scope Boundary, and Result File instructions. Full lifecycle hooks and env var isolation.

The gap between paths is significant. Path A workers operate blind -- they have no compliance tier awareness, no prior task context, no result file contract, and no scope boundaries. The `build_task_context()` subsystem (3 functions, ~130 lines) was purpose-built for cross-task context injection but has zero callers and is confirmed dead code. Additionally, all per-task outputs collide on the same file path, destroying earlier task artifacts.

