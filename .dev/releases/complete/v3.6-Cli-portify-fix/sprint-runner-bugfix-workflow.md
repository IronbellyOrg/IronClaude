# Sprint Runner Bug Fix Workflow — TUI Freeze + Path Resolution

> **Self-contained execution brief.** An agent with no prior context can execute each task
> using `/sc:task-unified`. All file paths, line numbers, field names, and code patterns
> are provided inline.

## Project Context

- **Repo**: `/config/workspace/IronClaude`
- **Package**: `superclaude` (Python, UV-only — use `uv run pytest` for all tests)
- **Module under fix**: `src/superclaude/cli/sprint/`
- **Branch**: `feature/v3.6-cli-portify-fix`

### Key Files

| File | Purpose | Approx Lines |
|------|---------|-------------|
| `src/superclaude/cli/sprint/executor.py` | Main orchestration loop, `execute_sprint()`, `execute_phase_tasks()` | ~1300 |
| `src/superclaude/cli/sprint/tui.py` | Rich Live TUI dashboard, `SprintTUI` class | ~280 |
| `src/superclaude/cli/sprint/models.py` | Dataclasses: `SprintConfig`, `MonitorState`, `Phase`, `TaskEntry`, etc. | ~600 |
| `src/superclaude/cli/sprint/config.py` | Phase discovery, tasklist parsing, `load_sprint_config()` | ~376 |
| `src/superclaude/cli/sprint/commands.py` | Click CLI commands, `_check_fidelity()`, `run()` | ~316 |
| `tests/sprint/test_executor.py` | Existing executor tests | ~400 |
| `tests/sprint/test_config.py` | Existing config/parser tests | ~300 |

### Architecture Summary

The sprint runner (`superclaude sprint run <index>`) discovers phase files from a tasklist
index, then executes each phase sequentially. There are two execution paths inside
`execute_sprint()`:

1. **Task-inventory path** — phase files with `### Txx.xx -- Title` headings trigger
   `execute_phase_tasks()`, which runs one subprocess per task via `_run_task_subprocess()`.
2. **Freeform path** — phase files without task headings run as a single `ClaudeProcess`
   with a polling loop that updates the TUI every 0.5 seconds.

---

## Phase 1: Bug Fix — TUI Frozen at "Waiting..." During Task-Inventory Execution

### Root Cause

In `executor.py`, the task-inventory branch (lines 1183–1208) calls `execute_phase_tasks()`
but **never calls `tui.update()`** before, during, or after. The `SprintTUI.current_phase`
stays `None`, so `_build_active_panel()` (tui.py line 232) renders "Waiting..." forever.
The progress bar (tui.py line 223) also says "tasks" but actually tracks phases.

Compare with the freeform path (lines 1238+) which has:
```python
tui.update(sprint_result, monitor.state, phase)  # line 1238
while proc_manager._process.poll() is None:      # polling loop
    ms = monitor.state
    tui.update(sprint_result, ms, phase)          # every 0.5s
```

### Task T01.01 — Add TUI updates to task-inventory branch in `execute_sprint()`

**File**: `src/superclaude/cli/sprint/executor.py`

**What to do**: Find the `if tasks:` block starting at line 1184. Add TUI update calls
at two points:

**Point 1 — Before `execute_phase_tasks()` call (after line 1185):**

Insert between `started_at = datetime.now(timezone.utc)` and the `execute_phase_tasks()` call:

```python
# Signal TUI that this phase is now active
tui.update(sprint_result, MonitorState(), phase)
```

**Point 2 — After `logger.write_phase_result(phase_result)` (after line 1207, before `continue`):**

```python
# Refresh TUI with completed phase (current_phase=None resets active panel)
tui.update(sprint_result, MonitorState(), None)
```

**Import needed**: `MonitorState` is already imported at line 21 from `.models`.

**Verification**: `uv run pytest tests/sprint/test_executor.py -v` — all existing tests must pass
(they don't use TUI so should be unaffected).

---

### Task T01.02 — Add per-task TUI updates inside `execute_phase_tasks()`

**File**: `src/superclaude/cli/sprint/executor.py`

**Step 1 — Add parameters to function signature (line 912):**

Current signature:
```python
def execute_phase_tasks(
    tasks: list[TaskEntry],
    config: SprintConfig,
    phase,
    ledger: TurnLedger | None = None,
    *,
    _subprocess_factory=None,
    shadow_metrics: ShadowGateMetrics | None = None,
    remediation_log: DeferredRemediationLog | None = None,
) -> tuple[list[TaskResult], list[str], list[TrailingGateResult]]:
```

Add two new keyword-only parameters after `remediation_log`:
```python
    tui: "SprintTUI | None" = None,
    sprint_result: "SprintResult | None" = None,
```

Use string annotation for `SprintTUI` to avoid circular import. Add a comment:
```python
    # TUI params are optional for backward compat with tests.
    # When provided, per-task progress is shown in the dashboard.
```

**Step 2 — Add update BEFORE subprocess launch (inside the `for i, task` loop, ~line 974):**

Insert just before the `if _subprocess_factory is not None:` block:

```python
# Per-task TUI update: show which task is about to launch
if tui is not None and sprint_result is not None:
    _tui_state = MonitorState()
    _tui_state.events_received = i
    _tui_state.last_event_time = time.monotonic()
    _tui_state.last_task_id = task.task_id
    tui.update(sprint_result, _tui_state, phase)
```

**Step 3 — Add update AFTER result is appended (~line 1028, after `results.append(result)`):**

```python
# Per-task TUI update: show task completion
if tui is not None and sprint_result is not None:
    _tui_state = MonitorState()
    _tui_state.events_received = i + 1
    _tui_state.last_event_time = time.monotonic()
    _tui_state.last_task_id = task.task_id
    tui.update(sprint_result, _tui_state, phase)
```

**Step 4 — Update the call site in `execute_sprint()` (~line 1186):**

Change:
```python
task_results, remaining, phase_gate_results = execute_phase_tasks(
    tasks=tasks, config=config, phase=phase,
    ledger=ledger, shadow_metrics=shadow_metrics,
    remediation_log=remediation_log,
)
```

To:
```python
task_results, remaining, phase_gate_results = execute_phase_tasks(
    tasks=tasks, config=config, phase=phase,
    ledger=ledger, shadow_metrics=shadow_metrics,
    remediation_log=remediation_log,
    tui=tui, sprint_result=sprint_result,
)
```

**Import needed**: `time` is already imported at line 7. `MonitorState` at line 21.

**Why `last_event_time` matters**: The `MonitorState.stall_status` property (models.py
line 522–535) compares `time.monotonic()` against `last_event_time`. Without setting it,
the TUI would show "STALLED" after 120 seconds even when tasks are completing normally.

**Why `last_task_id` matters**: The active panel (tui.py line 252) renders
`ms.last_task_id or '-'`. Without it, the user sees "-" instead of "T01.03".

**Verification**: `uv run pytest tests/sprint/test_executor.py -v`

---

### Task T01.03 — Fix progress bar label from "tasks" to "phases"

**File**: `src/superclaude/cli/sprint/tui.py`

**What to change**: Line 223 currently reads:
```python
TextColumn("[dim]{task.completed}/{task.total} tasks[/]"),
```

The values come from lines 225–226:
```python
total = len(self.config.active_phases)    # ← this is phase count
done = self.sprint_result.phases_passed   # ← this is phases passed
```

Change line 223 to:
```python
TextColumn("[dim]{task.completed}/{task.total} phases[/]"),
```

**Verification**: `uv run pytest tests/sprint/ -v`

---

### Task T01.04 — Write test for per-task TUI updates

**File**: Create `tests/sprint/test_tui_task_updates.py`

**Test pattern** (follows existing pattern in `tests/sprint/test_executor.py`):

```python
"""Tests for TUI integration with per-task execution path."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from superclaude.cli.sprint.executor import execute_phase_tasks
from superclaude.cli.sprint.models import (
    MonitorState,
    Phase,
    SprintConfig,
    SprintResult,
    TaskEntry,
    TaskStatus,
    TurnLedger,
)


def _make_config(tmp_path: Path) -> SprintConfig:
    """Create a minimal SprintConfig for testing."""
    pf = tmp_path / "phase-1-tasklist.md"
    pf.write_text("# Phase 1\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")
    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=[Phase(number=1, file=pf, name="Phase 1")],
        start_phase=1,
        end_phase=1,
        max_turns=5,
        wiring_gate_mode="off",
        wiring_gate_scope="none",
    )


def _make_tasks(count: int = 3) -> list[TaskEntry]:
    """Create N dummy task entries."""
    return [
        TaskEntry(
            task_id=f"T01.{i:02d}",
            title=f"Task {i}",
            description=f"Description {i}",
        )
        for i in range(1, count + 1)
    ]


class TestTUITaskUpdates:
    """Verify that execute_phase_tasks() calls tui.update() per task."""

    def test_update_called_twice_per_task(self, tmp_path):
        """TUI.update() should be called before and after each task."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(3)
        phase = config.phases[0]
        mock_tui = MagicMock()
        mock_result = MagicMock(spec=SprintResult)

        def factory(task, cfg, ph):
            return (0, 5, 100)  # exit_code, turns, bytes

        results, remaining, gates = execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            tui=mock_tui,
            sprint_result=mock_result,
        )

        # 2 calls per task (before + after) = 6 total for 3 tasks
        assert mock_tui.update.call_count == 2 * len(tasks)

    def test_last_task_id_set_correctly(self, tmp_path):
        """MonitorState passed to tui.update() should have last_task_id set."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(2)
        phase = config.phases[0]
        mock_tui = MagicMock()
        mock_result = MagicMock(spec=SprintResult)

        def factory(task, cfg, ph):
            return (0, 5, 100)

        execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            tui=mock_tui,
            sprint_result=mock_result,
        )

        # Check that each call's MonitorState has a task ID
        for call_args in mock_tui.update.call_args_list:
            monitor_state = call_args[0][1]  # second positional arg
            assert isinstance(monitor_state, MonitorState)
            assert monitor_state.last_task_id.startswith("T01.")

    def test_no_tui_no_error(self, tmp_path):
        """When tui=None (default), no errors occur."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(2)
        phase = config.phases[0]

        def factory(task, cfg, ph):
            return (0, 5, 100)

        results, remaining, gates = execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            # tui not passed — defaults to None
        )

        assert len(results) == 2
        assert all(r.status == TaskStatus.PASS for r in results)

    def test_events_received_increments(self, tmp_path):
        """events_received should be i before launch, i+1 after."""
        config = _make_config(tmp_path)
        tasks = _make_tasks(3)
        phase = config.phases[0]
        mock_tui = MagicMock()
        mock_result = MagicMock(spec=SprintResult)

        def factory(task, cfg, ph):
            return (0, 5, 100)

        execute_phase_tasks(
            tasks=tasks,
            config=config,
            phase=phase,
            _subprocess_factory=factory,
            tui=mock_tui,
            sprint_result=mock_result,
        )

        events = [
            call_args[0][1].events_received
            for call_args in mock_tui.update.call_args_list
        ]
        # Expected: [0, 1, 1, 2, 2, 3] — (before task 0, after task 0, before task 1, ...)
        assert events == [0, 1, 1, 2, 2, 3]
```

**Verification**: `uv run pytest tests/sprint/test_tui_task_updates.py -v`

---

## Phase 2: Bug Fix — Path Resolution When Tasklist Is in Subdirectory

### Root Cause

The `sc:tasklist` command generates files inside a `tasklist/` subdirectory. The sprint
runner sets `release_dir = index_path.parent` (config.py line 209) and
`sprint_dir = index_path.parent` (commands.py line 42). When the index is inside
`tasklist/`, both resolve to the wrong directory:

```
v3.3-TurnLedger-Validation/           ← actual release dir
├── .roadmap-state.json                ← fidelity state is HERE
├── requirements-spec.md               ← spec is HERE
└── tasklist/                          ← index_path.parent resolves HERE (wrong)
    ├── tasklist-index.md
    └── phase-1-tasklist.md
```

**Consequence 1**: `_check_fidelity()` looks for `.roadmap-state.json` in `tasklist/`,
doesn't find it, returns `(False, "")` — fidelity gate silently passes when it should block.

**Consequence 2**: `results/`, `execution-log.jsonl`, `execution-log.md` are written
inside `tasklist/` instead of alongside the spec and roadmap.

**CRITICAL**: `discover_phases()` (config.py line 35) uses `index_dir = index_path.parent`
to find phase files. This MUST NOT change — phase files live alongside the index inside
`tasklist/`.

---

### Task T02.01 — Add `_resolve_release_dir()` helper in `config.py`

**File**: `src/superclaude/cli/sprint/config.py`

**Where**: Insert BEFORE `load_sprint_config()` (line 161), AFTER the `_logger` definition
(line 262... note: logger is `_logger = logging.getLogger("superclaude.sprint.config")`).

Actually, `_logger` is at line 262 which is after `load_sprint_config`. Place the new
function between `validate_phases()` (ends line 158) and `load_sprint_config()` (line 161):

```python
def _resolve_release_dir(index_path: Path) -> Path:
    """Resolve the release directory from a tasklist index path.

    The tasklist index may live directly in the release directory, or inside
    a ``tasklist/`` subdirectory created by ``sc:tasklist``. This function
    detects the subdirectory case by checking:

    1. Is the parent directory named ``tasklist``, ``tasklists``, or ``tasks``?
    2. Does the grandparent contain ``.roadmap-state.json`` or a spec file?

    When both conditions are met, the grandparent is the true release directory.
    Otherwise, falls back to ``index_path.parent`` (backward-compatible default).

    Note: Phase file discovery (``discover_phases``) always uses
    ``index_path.parent`` regardless of this function's output, because
    phase files live alongside the index.
    """
    parent = index_path.parent
    _known_subdir_names = {"tasklist", "tasklists", "tasks"}

    if parent.name.lower() in _known_subdir_names:
        grandparent = parent.parent
        # Check for release-directory indicators in the grandparent
        has_state_file = (grandparent / ".roadmap-state.json").exists()
        has_spec_files = bool(
            list(grandparent.glob("*spec*.md"))
            or list(grandparent.glob("*requirements*.md"))
        )
        if has_state_file or has_spec_files:
            _logger.info(
                "Resolved release_dir to grandparent: %s (index inside %s/)",
                grandparent,
                parent.name,
            )
            return grandparent

    return parent
```

**Import needed**: `logging` is already imported (line 5). The `_logger` instance already
exists at line 262. However, `_logger` is defined AFTER line 161 where we need it.

**FIX**: Move the `_logger = logging.getLogger(...)` line from line 262 to just before
the new function. Or use a module-level logger. Check: the logger at line 262 is:
```python
_logger = logging.getLogger("superclaude.sprint.config")
```
Move this line to right after the imports section (after line 24 or so), before any
function definitions. This is a safe refactor — the logger is only used in `parse_tasklist()`
(line 288) and now the new function.

**Verification**: `uv run pytest tests/sprint/test_config.py -v`

---

### Task T02.02 — Use `_resolve_release_dir()` in `load_sprint_config()`

**File**: `src/superclaude/cli/sprint/config.py`

**Note**: After T02.01 inserts `_resolve_release_dir()` and moves `_logger`, line numbers
in this file will have shifted by ~20 lines. Search for `release_dir=index_path.parent`
inside `load_sprint_config()` rather than relying on the original line number.

**What to change**: Find `release_dir=index_path.parent` inside `load_sprint_config()`
(originally line 209, shifted after T02.01):

Current:
```python
    config = SprintConfig(
        index_path=index_path,
        release_dir=index_path.parent,
```

Change to:
```python
    config = SprintConfig(
        index_path=index_path,
        # Resolves grandparent when index is inside tasklist/ subdir;
        # phase discovery still uses index_path.parent via discover_phases().
        release_dir=_resolve_release_dir(index_path),
```

**Verification**: `uv run pytest tests/sprint/test_config.py -v`

---

### Task T02.03 — Use `_resolve_release_dir()` in `_check_fidelity()`

**File**: `src/superclaude/cli/sprint/commands.py`

**What to change**: Find `sprint_dir = index_path.parent` inside `_check_fidelity()`
(line 42 — this file is not affected by T02.01's changes):

Current:
```python
    sprint_dir = index_path.parent
    state_file = sprint_dir / ".roadmap-state.json"
```

Change to:
```python
    from .config import _resolve_release_dir

    sprint_dir = _resolve_release_dir(index_path)
    state_file = sprint_dir / ".roadmap-state.json"
```

**Note**: The import is placed inside the function to match the existing pattern in
`commands.py` (line 192 imports `load_sprint_config` inside `run()`). This avoids
circular import risk.

**Verification**: `uv run pytest tests/sprint/ -v`

---

### Task T02.04 — Add `--release-dir` CLI escape hatch

**File**: `src/superclaude/cli/sprint/commands.py`

**Step 1 — Add Click option to `run()` command (~line 159, before the function def):**

Add after the `--force-fidelity` option (line 163):
```python
@click.option(
    "--release-dir",
    "release_dir_override",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Explicit release directory (overrides auto-detection from index path).",
)
```

**Step 2 — Add parameter to `run()` function signature (line 179):**

Add `release_dir_override: Path | None,` to the parameter list.

**Step 3 — Thread through to `load_sprint_config()`:**

In the `run()` function body, after `config = load_sprint_config(...)` (line 196–208),
add an override:

```python
    # Override release_dir if explicitly provided
    if release_dir_override is not None:
        resolved = Path(release_dir_override).resolve()
        object.__setattr__(config, "release_dir", resolved)
        object.__setattr__(config, "work_dir", resolved)
```

We use `object.__setattr__` for consistency with the existing pattern in
`SprintConfig.__post_init__` (models.py line 343).

**No fidelity check change needed.** After T02.03, `_check_fidelity()` already calls
`_resolve_release_dir()`, which handles the common `tasklist/` subdirectory case
automatically. The `--release-dir` flag is primarily for controlling where sprint
artifacts (results/, logs) are written.

**Verification**: `uv run pytest tests/sprint/ -v` and manual test:
`superclaude sprint run path/to/tasklist-index.md --release-dir /some/dir --dry-run`

---

### Task T02.05 — Write tests for `_resolve_release_dir()`

**File**: Create `tests/sprint/test_resolve_release_dir.py`

```python
"""Tests for _resolve_release_dir — tasklist subdirectory detection."""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.sprint.config import _resolve_release_dir


class TestResolveReleaseDir:
    """Test release directory resolution heuristic."""

    def test_index_in_release_dir_directly(self, tmp_path):
        """When index is directly in release dir, return parent as-is."""
        index = tmp_path / "tasklist-index.md"
        index.write_text("index")
        assert _resolve_release_dir(index) == tmp_path

    def test_tasklist_subdir_with_roadmap_state(self, tmp_path):
        """When index is in tasklist/ and grandparent has .roadmap-state.json."""
        tasklist_dir = tmp_path / "tasklist"
        tasklist_dir.mkdir()
        index = tasklist_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        assert _resolve_release_dir(index) == tmp_path

    def test_tasklist_subdir_with_spec_file(self, tmp_path):
        """When index is in tasklist/ and grandparent has *spec*.md."""
        tasklist_dir = tmp_path / "tasklist"
        tasklist_dir.mkdir()
        index = tasklist_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / "v3.3-requirements-spec.md").write_text("spec")

        assert _resolve_release_dir(index) == tmp_path

    def test_tasklist_subdir_no_indicators(self, tmp_path):
        """When index is in tasklist/ but grandparent has no indicators, fall back."""
        tasklist_dir = tmp_path / "tasklist"
        tasklist_dir.mkdir()
        index = tasklist_dir / "tasklist-index.md"
        index.write_text("index")
        # No .roadmap-state.json, no spec files

        assert _resolve_release_dir(index) == tasklist_dir

    def test_tasks_subdir_variant(self, tmp_path):
        """'tasks' directory name is also recognized."""
        tasks_dir = tmp_path / "tasks"
        tasks_dir.mkdir()
        index = tasks_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        assert _resolve_release_dir(index) == tmp_path

    def test_tasklists_subdir_variant(self, tmp_path):
        """'tasklists' directory name is also recognized."""
        tl_dir = tmp_path / "tasklists"
        tl_dir.mkdir()
        index = tl_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / "my-spec.md").write_text("spec")

        assert _resolve_release_dir(index) == tmp_path

    def test_unrelated_subdir_name(self, tmp_path):
        """Arbitrary subdir name is not resolved to grandparent."""
        other_dir = tmp_path / "sprints"
        other_dir.mkdir()
        index = other_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        # "sprints" is not in the known set, so returns parent (= other_dir)
        assert _resolve_release_dir(index) == other_dir

    def test_case_insensitive(self, tmp_path):
        """Directory name matching is case-insensitive."""
        tl_dir = tmp_path / "Tasklist"
        tl_dir.mkdir()
        index = tl_dir / "tasklist-index.md"
        index.write_text("index")
        (tmp_path / ".roadmap-state.json").write_text("{}")

        assert _resolve_release_dir(index) == tmp_path
```

**Verification**: `uv run pytest tests/sprint/test_resolve_release_dir.py -v`

---

## Phase 3: Integration Verification

### Task T03.01 — Run full test suite and verify no regressions

```bash
uv run pytest tests/sprint/ -v
```

All existing tests in `test_executor.py`, `test_config.py`, `test_anti_instinct_sprint.py`,
`test_execute_sprint_integration.py` must continue to pass. The new tests in
`test_tui_task_updates.py` and `test_resolve_release_dir.py` must also pass.

### Task T03.02 — Dry-run verification

```bash
superclaude sprint run /config/workspace/IronClaude/.dev/releases/current/turnledger-integration/v3.3-TurnLedger-Validation/tasklist/tasklist-index.md --dry-run
```

Verify that the dry-run output shows the correct release directory (the grandparent
`v3.3-TurnLedger-Validation/`, not `tasklist/`).

---

## Dependency Map

```
T01.01 ──┐
T01.02 ──┤── T01.04 (test depends on code changes)
T01.03 ──┘
                    ├── T03.01 (full suite)
T02.01 ──┐          │
T02.02 ──┤── T02.05 ┘
T02.03 ──┤
T02.04 ──┘
                    └── T03.02 (dry-run check)
```

- Phase 1 (T01.x) and Phase 2 (T02.x) are **independent** — can be executed in parallel.
- T01.04 depends on T01.01 + T01.02 being complete (needs new params to exist).
- T02.05 depends on T02.01 being complete (needs `_resolve_release_dir` to exist).
- T03.01 depends on all code tasks being complete.

---

## Known Limitations (out of scope)

1. **Within-task TUI freeze**: During each individual task's `proc.wait()`, the TUI cannot
   update. A poll loop inside `_run_task_subprocess()` would fix this but is a larger
   refactor. The per-task boundary updates are a significant improvement over zero updates.

2. **`_check_fidelity` "not found = OK" design**: When `.roadmap-state.json` doesn't exist,
   the fidelity gate silently passes. This is a broader design question beyond path
   resolution.
