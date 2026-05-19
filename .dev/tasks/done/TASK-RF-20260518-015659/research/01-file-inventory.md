# Research: File Inventory — Sprint Runner 6-Fix Targets
**Topic type:** File Inventory
**Scope:** src/superclaude/cli/sprint/{config,executor,process,logging_,monitor}.py + src/superclaude/cli/pipeline/process.py
**Status:** Complete
**Date:** 2026-05-18
---

## Summary Table

| File | Lines | Purpose | Fix Touchpoints |
|------|-------|---------|-----------------|
| `src/superclaude/cli/sprint/config.py` | 501 | Phase discovery, validation, sprint config loading + tasklist parsing | C1: `stall_timeout=0` default at line 284 |
| `src/superclaude/cli/sprint/executor.py` | 2096 | Core orchestration loop, isolation, gates, task subprocess runner | C2 (output collision @ 1086-1115), C3 (remediation timeout @ 81-87), C1 (watchdog gate @ 1365-1404), C4 (phase_start call @ 1328) |
| `src/superclaude/cli/sprint/process.py` | 385 | Sprint `ClaudeProcess` subclass + signal handler + context injection | C2 contributes to collision (uses `config.output_file(phase)` @ 110-111); C3 timeout formula @ 115 |
| `src/superclaude/cli/sprint/logging_.py` | 235 | Dual JSONL + Markdown sprint execution logger (`SprintLogger`) | C4: `write_phase_start` @ lines 59-69 |
| `src/superclaude/cli/sprint/monitor.py` | 571 | Sidecar daemon thread that tails NDJSON output files | (no direct fix landing — reads `output_path` set by executor; collision side-effect surface) |
| `src/superclaude/cli/pipeline/process.py` | 244 | Generic pipeline `ClaudeProcess` base — argv build, env, lifecycle | C2: `start()` opens `output_file` mode `"w"` @ 122 (truncates); C5/deferred: `--no-session-persistence` @ 84; C3 default `timeout_seconds=6300` @ 46 |

---

## 1. `src/superclaude/cli/sprint/config.py` (501 lines)

**Purpose:** Phase discovery from sprint index + filesystem, validates phase ranges, loads & enriches `SprintConfig`, parses individual tasklist markdown into `TaskEntry` objects.

**Module-internal imports:** `from .models import Phase, SprintConfig, TaskEntry`

**External imports:** `logging`, `re`, `pathlib.Path`, `click`

**Top-level exports (signatures):**
- `count_tasks_in_file(phase_file: Path) -> int` — line 37
- `discover_phases(index_path: Path) -> list[Phase]` — line 52
- `_extract_phase_name(phase_file: Path) -> str` — line 143
- `_extract_phase_prompt_preview(phase_file: Path, phase_name: str) -> str` — line 167
- `validate_phases(...)` — line 207
- `_resolve_release_dir(index_path: Path) -> Path` — line 236
- `load_sprint_config(index_path, start_phase=1, end_phase=0, max_turns=100, model="", dry_run=False, permission_flag="--dangerously-skip-permissions", debug=False, stall_timeout=0, stall_action="warn", shadow_gates=False) -> SprintConfig` — line 275
- `parse_tasklist(content: str, execution_mode: str = "claude") -> list[TaskEntry]` — line 391
- `parse_tasklist_file(path: Path, execution_mode: str = "claude") -> list[TaskEntry]` — line 487

**Fix Touchpoint C1 — `stall_timeout` default (`load_sprint_config` signature, lines 275-286):**
```python
def load_sprint_config(
    index_path: Path,
    start_phase: int = 1,
    end_phase: int = 0,
    max_turns: int = 100,
    model: str = "",
    dry_run: bool = False,
    permission_flag: str = "--dangerously-skip-permissions",
    debug: bool = False,
    stall_timeout: int = 0,
    stall_action: str = "warn",
    shadow_gates: bool = False,
) -> SprintConfig:
```
Line 284 contains `stall_timeout: int = 0`. The `0 = disabled` semantics are baked-in via the watchdog gate (`config.stall_timeout > 0`, executor.py:1367). This is the primary site where the C1 default-on watchdog policy lands. Mirror default also lives in `SprintConfig` dataclass at `models.py:369` (`stall_timeout: int = 0  # 0 = disabled`).

---

## 2. `src/superclaude/cli/sprint/models.py` (relevant subset — NOT in fix scope but contains `output_file()`)

**Critical helper for C2 collision diagnosis** — `SprintConfig.output_file()` / `error_file()` defined in `models.py`, NOT in the fix-scope files:

```python
# models.py lines 469-476
def output_file(self, phase: Phase) -> Path:
    return self.results_dir / f"phase-{phase.number}-output.txt"

def error_file(self, phase: Phase) -> Path:
    return self.results_dir / f"phase-{phase.number}-errors.txt"

def result_file(self, phase: Phase) -> Path:
    return self.results_dir / f"phase-{phase.number}-result.md"
```
**Key finding:** Both helpers accept ONLY a `Phase` argument. There is NO per-task variant. Every per-task subprocess in `_run_task_subprocess` therefore shares the same `phase-N-output.txt` path → fix C2 must either (a) add a `task: TaskEntry | None = None` parameter, or (b) introduce a new helper like `task_output_file(phase, task)`. No prior helper exists.

---

## 3. `src/superclaude/cli/sprint/executor.py` (2096 lines)

**Purpose:** Sprint orchestration loop. Houses `SprintGatePolicy` (trailing-gate plug-in), isolation setup, per-phase task execution, wiring/anti-instinct/checkpoint hooks, and the main `execute_sprint()` entrypoint.

**External pipeline imports:**
```python
from superclaude.cli.pipeline.models import Step, StepResult
from superclaude.cli.pipeline.trailing_gate import DeferredRemediationLog, TrailingGateResult
```

**Internal sprint imports:** `.debug_logger`, `.diagnostics`, `.logging_.SprintLogger`, `.models` (many), `.monitor` (`OutputMonitor`, `detect_error_max_turns`, `detect_prompt_too_long`), `.notify`, `.process.ClaudeProcess`/`SignalHandler`, `.tmux`, `.tui.SprintTUI`.

**Top-level exports (selected):**
- `class SprintGatePolicy` — line 56
- `class IsolationLayers` — line 107
- `setup_isolation(config) -> IsolationLayers` — line 150
- `class AggregatedPhaseReport` — line 191
- `aggregate_task_results(...)` — line 296
- `check_budget_guard(ledger)` — line 338
- `run_wiring_safeguard_checks(...)` — line 354
- `_resolve_wiring_mode(config) -> str` — line 427
- `run_post_task_wiring_hook(...)` — line 458
- `run_post_phase_wiring_hook(...)` — line 748
- `run_post_task_anti_instinct_hook(...)` — line 803
- `execute_phase_tasks(...)` — line 927
- `_run_task_subprocess(task, config, phase) -> tuple[int,int,int]` — line 1076
- `_parse_phase_tasks(phase, config) -> list[TaskEntry] | None` — line 1118
- `execute_sprint(config)` — line 1135  ← MAIN orchestration
- `_classify_from_result_file(...)` — line 1722
- `_verify_checkpoints(...)` — line 1759
- `_check_checkpoint_pass(config, phase) -> bool` — line 1842
- `_check_contamination(config, phase) -> list[str]` — line 1856
- `_write_crash_recovery_log(...)` — line 1875
- `_write_preliminary_result(...)` — line 1902
- `_write_executor_result_file(...)` — line 1968
- `_determine_phase_status(...)` — line 2015

### Fix Touchpoint C3 — remediation Step timeout formula (lines 81-87, inside `SprintGatePolicy.build_remediation_step`):
```python
        return Step(
            id=f"{gate_result.step_id}_remediation",
            prompt=prompt,
            output_file=output_dir / f"{gate_result.step_id}_remediation.md",
            gate=None,
            timeout_seconds=self._config.max_turns * 60,
        )
```
Synthesis report flags this `max_turns * 60` formula as inconsistent with the main subprocess construction (which uses `max_turns * 120 + 300`). Reconciliation must pick one canonical formula.

### Fix Touchpoint C2 — `_run_task_subprocess` per-task output collision (lines 1076-1115):
```python
def _run_task_subprocess(
    task: TaskEntry,
    config: SprintConfig,
    phase,
) -> tuple[int, int, int]:
    """Run a single task in a subprocess. Returns (exit_code, turns, output_bytes).

    This is the real implementation that spawns a ClaudeProcess. For testing,
    callers of execute_phase_tasks pass _subprocess_factory instead.
    """
    # Build a task-specific prompt
    prompt = (
        f"Execute task {task.task_id}: {task.title}\n"
        f"From phase file: {phase.file}\n"
        f"Description: {task.description}\n"
    )

    proc = ClaudeProcess.__new__(ClaudeProcess)
    proc.config = config
    proc.phase = phase
    from superclaude.cli.pipeline.process import ClaudeProcess as _Base

    _Base.__init__(
        proc,
        prompt=prompt,
        output_file=config.output_file(phase),        # ← COLLIDES across tasks
        error_file=config.error_file(phase),          # ← COLLIDES across tasks
        max_turns=config.max_turns,
        model=config.model,
        permission_flag=config.permission_flag,
        timeout_seconds=config.max_turns * 120 + 300, # ← C3 reference formula
        output_format="stream-json",
    )
    proc.start()
    proc.wait()
    exit_code = proc._process.returncode if proc._process else -1
    output_path = config.output_file(phase)
    output_bytes = output_path.stat().st_size if output_path.exists() else 0
```
**Bug surface:** Every task within a phase calls `config.output_file(phase)` and `config.error_file(phase)`, which return only phase-scoped paths. Because `pipeline/process.py:122` opens the file in `"w"` mode, each task TRUNCATES the prior task's output for that phase. The C2 fix must thread `task.task_id` into a new path (e.g. `phase-{n}-task-{id}-output.txt`).

### Fix Touchpoint C4 — phase_start call site (executor.py:1328, inside main `execute_sprint` loop):
```python
            proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
            proc_manager.start()
            started_at = datetime.now(timezone.utc)
            # Use monotonic clock for deadline enforcement to be immune to NTP adjustments
            deadline = time.monotonic() + proc_manager.timeout_seconds
            logger.write_phase_start(phase, started_at)        # ← C4 emit site
```
`logger.write_phase_start(phase, started_at)` is the SINGLE call site invoking the `SprintLogger.write_phase_start` method. The JSONL emit logic lives in logging_.py (see §5).

### Fix Touchpoint C1 — watchdog gate (lines 1365-1404, inside the poll loop):
```python
                    # --- Watchdog: stall timeout check ---
                    if (
                        config.stall_timeout > 0
                        and ms.stall_seconds > config.stall_timeout
                        and ms.events_received > 0  # don't trigger during startup
                        and not _stall_acted
                    ):
                        _stall_acted = True
                        debug_log(
                            _dbg,
                            "watchdog_triggered",
                            phase=phase.number,
                            action=config.stall_action,
                            stall_seconds=round(ms.stall_seconds, 1),
                            pid=proc_manager._process.pid,
                        )
                        if config.stall_action == "kill":
                            import sys

                            print(
                                f"[WATCHDOG] Stall detected ({ms.stall_seconds:.0f}s > "
                                f"{config.stall_timeout}s) — killing phase {phase.number}",
                                file=sys.stderr,
                            )
                            _timed_out = True
                            proc_manager.terminate()
                            break
                        else:
                            # warn action: log and continue
                            import sys

                            print(
                                f"[WATCHDOG] Stall detected ({ms.stall_seconds:.0f}s > "
                                f"{config.stall_timeout}s) — warning for phase {phase.number}",
                                file=sys.stderr,
                            )

                    # Reset single-fire guard when output resumes
                    if _stall_acted and ms.stall_seconds == 0.0:
                        _stall_acted = False
```
This gate is exercised once `stall_timeout > 0`. C1 fix is the policy change at the default (config.py:284), which then enables this existing gate without code surgery here. C1 has TWO sub-fixes per the track goal: (a) `stall_timeout` default policy; (b) watchdog split — the synthesis suggests separating "warn-only watchdog default-on" from "kill watchdog opt-in", which may require restructuring this branch.

### Per-phase ClaudeProcess construction (line 1323, surrounding context for C2 phase-level path use):
```python
                _phase_env_vars = {
                    "CLAUDE_WORK_DIR": str(isolation_dir),
                }
                proc_manager = ClaudeProcess(config, phase, env_vars=_phase_env_vars)
```
The main per-phase process (a `sprint.process.ClaudeProcess`) is constructed here without a `task` parameter. It also receives `config.output_file(phase)` via the subclass `__init__` (sprint/process.py:110-111).

---

## 4. `src/superclaude/cli/sprint/process.py` (385 lines)

**Purpose:** Sprint-specific subclass of pipeline `ClaudeProcess` with `/sc:task` prompt builder + signal handler + prior-task context injection helpers.

**External imports:** `logging`, `signal`, `subprocess as _subprocess`, `typing.TYPE_CHECKING`
**Project imports:** `from superclaude.cli.pipeline.process import ClaudeProcess as _PipelineClaudeProcess`, `.debug_logger.debug_log`, `.models.Phase`, `.models.SprintConfig`, `.models.TaskResult` (TYPE_CHECKING)

**Top-level exports:**
- `_make_spawn_hook(phase, config)` — line 30
- `_make_signal_hook(phase, config)` — line 58
- `_make_exit_hook(phase, config)` — line 70
- `class ClaudeProcess(_PipelineClaudeProcess)` — line 88
- `class SignalHandler` — line 219
- `build_task_context(prior_results, *, start_commit="", compress_threshold=3) -> str` — line 257
- `get_git_diff_context(start_commit) -> str` — line 322
- `compress_context_summary(results, *, keep_recent=3) -> str` — line 347

### Sprint ClaudeProcess `__init__` (lines 97-121) — C2/C3 surface:
```python
    def __init__(
        self,
        config: SprintConfig,
        phase: Phase,
        *,
        env_vars: dict[str, str] | None = None,
    ):
        self.config = config
        self.phase = phase
        self._extra_env_vars = env_vars
        prompt = self.build_prompt()
        super().__init__(
            prompt=prompt,
            output_file=config.output_file(phase),
            error_file=config.error_file(phase),
            max_turns=config.max_turns,
            model=config.model,
            permission_flag=config.permission_flag,
            timeout_seconds=config.max_turns * 120 + 300,  # ← C3 canonical formula
            output_format="stream-json",
            on_spawn=_make_spawn_hook(phase, config),
            on_signal=_make_signal_hook(phase, config),
            on_exit=_make_exit_hook(phase, config),
            env_vars=env_vars,
        )
```
**Note:** This subclass is invoked ONLY from `execute_sprint` (executor.py:1323) for the per-phase process. The per-task subprocess in `_run_task_subprocess` does NOT use this subclass — it manually `__new__`'s the class and calls `_PipelineClaudeProcess.__init__` directly.

The `_make_spawn_hook` (line 30-55) closure captures `config.output_file(phase)` and `config.error_file(phase)` once at construction; if C2 reworks paths to be per-task, the hook factory will need updating too.

---

## 5. `src/superclaude/cli/sprint/logging_.py` (235 lines)

**Purpose:** Dual-format JSONL + Markdown sprint execution logger.

**External imports:** `json`, `datetime`, `rich.console.Console`
**Project imports:** `from .models import PhaseResult, PhaseStatus, SprintConfig, SprintResult`

**Top-level exports:**
- `class SprintLogger` — line 13
  - `__init__(config: SprintConfig)` — line 23
  - `write_header(sprint: SprintResult)` — line 28
  - `write_phase_start(phase, started_at)` — line 59  ← **C4 target**
  - `write_phase_interrupt(phase, started_at, finished_at, exit_code)` — line 71
  - `write_phase_result(result: PhaseResult)` — line 89
  - `write_checkpoint_verification(phase, expected, found, missing)` — line 159
  - `write_summary(sprint: SprintResult)` — line 190
  - `_jsonl(data)` / `_screen_info` / `_screen_warn` / `_screen_error` (private helpers)
- `read_status_from_log()` — line 224 (stub)
- `tail_log(lines=50, follow=False)` — line 231 (stub)

### Fix Touchpoint C4 — `write_phase_start` body (lines 59-69):
```python
    def write_phase_start(self, phase, started_at):
        """Log phase start transition (RUNNING)."""
        self._jsonl(
            {
                "event": "phase_start",
                "phase": phase.number,
                "phase_name": phase.display_name,
                "phase_file": str(phase.file),
                "timestamp": started_at.isoformat(),
            }
        )
```
**Current state:** The method writes a JSONL `phase_start` event with `event/phase/phase_name/phase_file/timestamp`. Pair counterpart `write_phase_interrupt` (line 71) also emits a balancing event. C4 fix per synthesis: confirm/repair JSONL emission. Possible gap: `started_at` typed loosely (no isoformat guard for naive datetimes); could also need additional fields (e.g. `phase_index`, `total_phases`, `max_turns`). The exact required JSONL schema must be derived from the synthesis.

---

## 6. `src/superclaude/cli/sprint/monitor.py` (571 lines)

**Purpose:** Sidecar daemon thread (`OutputMonitor`) that watches the NDJSON output file emitted by `claude --print --output-format stream-json` and updates the live `MonitorState` used by the TUI and watchdog gate.

**External imports:** `json`, `logging`, `re`, `threading`, `time`, `pathlib.Path`
**Project imports:** `from .config import count_tasks_in_file`, `from .debug_logger import debug_log`, `from .models import MonitorState`

**Top-level exports:**
- `detect_error_max_turns(output_path) -> bool` — line 37
- `detect_prompt_too_long(...)` — line 64
- `_shorten_tool_name(name)` — line 135
- `_flatten_tool_result_content(raw)` — line 148
- `_has_nonzero_exit_code(text)` — line 170
- `_condense_tool_input(tool_name, tool_input)` — line 199
- `count_turns_from_output(output_path)` — line 223
- `class OutputMonitor` — line 253

**Relation to fixes:** No direct fix lands here. However, monitor.py is the consumer side of the collision risk in C2 — it tails `output_path` set via `monitor.reset(output_path, phase_file=phase.file)` from executor.py:1312. If C2 widens output to per-task files, the monitor reset / tailing strategy may need accompanying changes (single-tail vs. per-task tails). For scope of this 4-fix track, the synthesis indicates monitor remains untouched.

---

## 7. `src/superclaude/cli/pipeline/process.py` (244 lines)

**Purpose:** Generic provider-agnostic `ClaudeProcess` for both sprint and roadmap pipelines. Builds argv, builds env, opens output/error files, spawns subprocess, handles graceful shutdown with SIGTERM → SIGKILL escalation.

**External imports only:** `logging`, `os`, `signal`, `subprocess`, `pathlib.Path`, `typing.Callable/Optional`
**Project imports:** NONE (NFR-007 enforces no sprint/roadmap imports).

**Top-level exports:**
- `class ClaudeProcess` — line 24
  - `__init__(*, prompt, output_file, error_file, max_turns=100, model="", permission_flag="--dangerously-skip-permissions", timeout_seconds=6300, output_format="stream-json", extra_args=None, on_spawn=None, on_signal=None, on_exit=None, env_vars=None, tool_write_mode=False)` — line 37
  - `build_command() -> list[str]` — line 73
  - `build_env(*, env_vars=None) -> dict[str,str]` — line 97
  - `start() -> subprocess.Popen` — line 114
  - `wait() -> int` — line 159
  - `terminate() -> None` — line 173
  - `validate_tool_write_output() -> bool` — line 216
  - `_close_handles() -> None` — line 238

### Fix Touchpoint C5/Deferred — `build_command` `--no-session-persistence` (lines 73-95):
```python
    def build_command(self) -> list[str]:
        """Build the claude CLI command.

        Prompt is delivered via stdin in start(), not as a -p argv value,
        to bypass the Linux MAX_ARG_STRLEN = 128 KB per-argument ceiling.
        """
        cmd = [
            "claude",
            "--print",
            "--verbose",
            self.permission_flag,
            "--no-session-persistence",   # ← C5 (deferred): remove this flag
            "--tools",
            "default",
            "--max-turns",
            str(self.max_turns),
            "--output-format",
            self.output_format,
        ]
        if self.model:
            cmd.extend(["--model", self.model])
        cmd.extend(self.extra_args)
        return cmd
```
Synthesis flags `--no-session-persistence` (line 84) as the C5 target. Per track goal, C5 is DEFERRED; this finding documents the location for completeness.

### Fix Touchpoint C2 — `start()` opens output_file mode "w" (lines 114-134):
```python
    def start(self) -> subprocess.Popen:
        """Launch the claude process."""
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        if self.tool_write_mode:
            # LLM writes output_file via Write tool; stdout goes to .log
            self._stdout_fh = open(self.output_file.with_suffix(".log"), "w")
        else:
            self._stdout_fh = open(self.output_file, "w")    # ← TRUNCATES
        self._stderr_fh = open(self.error_file, "w")         # ← TRUNCATES

        popen_kwargs = {
            "stdin": subprocess.PIPE,
            "stdout": self._stdout_fh,
            "stderr": self._stderr_fh,
            "env": self.build_env(env_vars=self._extra_env_vars),
        }
```
**Root cause of C2 collision:** Lines 122-123 open with mode `"w"`. Combined with phase-scoped paths from `SprintConfig.output_file`, multi-task phases overwrite earlier task output. The C2 fix can land here (e.g. switch to mode `"a"` AND/OR use per-task path), but the cleanest fix is per-task path (config-layer change) rather than touching this base class.

### C3 reference — default `timeout_seconds=6300` (line 46):
```python
        timeout_seconds: int = 6300,
```
The base class default is `6300` (≈ 100 turns × 60 + 300). Sprint/per-phase passes `max_turns * 120 + 300`. Remediation passes `max_turns * 60`. The C3 reconciliation must select one formula and apply consistently.

---

## Cross-cutting Findings for Task Builder

1. **`output_file()` / `error_file()` live in `models.py` (NOT in fix-scope listed files).** These accept only `Phase`, no `task_id`. Any C2 fix that adds a per-task variant must edit `models.py` as well — please flag this if the task builder is to scope the change accurately.
2. **`_run_task_subprocess` (executor.py:1076-1115) bypasses the `sprint.process.ClaudeProcess` subclass** and calls the base class via `_PipelineClaudeProcess.__init__` directly. This means lifecycle hooks (`_make_spawn_hook` etc.) are NOT wired for per-task subprocesses — only for per-phase ones. C2 fix scope must clarify whether to fix the bypass too.
3. **Three different timeout formulas in the codebase right now:**
   - `pipeline/process.py:46` default `6300`
   - `executor.py:86` remediation `max_turns * 60`
   - `executor.py:1106` + `sprint/process.py:115` main `max_turns * 120 + 300`
   C3 reconciliation should standardise.
4. **`write_phase_start` is invoked at exactly ONE site** (executor.py:1328). If C4 changes its signature or required arguments, that lone call site is the only place to update.
5. **Watchdog C1 has two coupled changes:** the default `stall_timeout=0` in BOTH `config.py:284` AND `models.py:369`; if the default flips, both must move together (and any test fixtures referencing the old default).
6. **Monitor (`monitor.py`) is untouched by the 4-fix track** but consumes the very paths that C2 collides — verify in implementation that single-tail behavior remains correct after C2.

