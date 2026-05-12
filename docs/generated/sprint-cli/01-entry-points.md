---
title: Sprint CLI - Entry Points & Command Structure
generated: 2026-04-03
scope: pyproject.toml, cli/main.py, cli/sprint/commands.py, cli/sprint/config.py
---

# Entry Points & Command Structure

## 1. Package Entry Point

**`pyproject.toml:63-64`**:
```toml
[project.scripts]
superclaude = "superclaude.cli.main:main"
```

## 2. Root CLI Registration

**`src/superclaude/cli/main.py`**:
- Line 18-20: Root Click group `def main()`
- Line 354: `from superclaude.cli.sprint import sprint_group`
- Line 356: `main.add_command(sprint_group, name="sprint")`

**`src/superclaude/cli/sprint/__init__.py:3`**:
```python
from .commands import sprint_group
```

## 3. Sprint Command Group

**`src/superclaude/cli/sprint/commands.py`**:

### `sprint run` (Line 174)

Primary execution command. Arguments and options:

| Option | Lines | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `index_path` | 72 | `Path(exists=True)` | required | Tasklist index file |
| `--start` | 73-79 | `int` | `1` | Start phase number |
| `--end` | 80-86 | `int` | `0` (=all) | End phase number |
| `--max-turns` | 87-92 | `int` | `100` | Max Claude turns per phase |
| `--model` | 93-97 | `str` | `""` | Model override |
| `--dry-run` | 98-102 | `bool` | `False` | Print plan without executing |
| `--no-tmux` | 103-107 | `bool` | `False` | Skip tmux wrapping |
| `--permission-flag` | 108-118 | choice | `skip-permissions` | Permission mode |
| `--debug` | 125-131 | `bool` | `False` | Enable debug logging |
| `--stall-timeout` | 132-137 | `int` | seconds | Stall detection timeout |
| `--stall-action` | 138-143 | choice | `warn\|kill` | Action on stall |
| `--shadow-gates` | 144-149 | `bool` | `False` | Enable shadow gate evaluation |
| `--force-fidelity-fail` | 150-160 | `str` | `None` | Force fidelity gate with justification |
| `--release-dir` | 167-173 | `Path` | `None` | Override release directory |

### Other Subcommands

| Command | Line | Handler | Purpose |
|---------|------|---------|---------|
| `attach` | 253 | `attach_to_sprint()` | Attach to running tmux session |
| `status` | 265 | `read_status_from_log()` | Read current sprint status |
| `logs` | 291 | `tail_log(lines, follow)` | Tail execution logs |
| `kill` | 308 | `kill_sprint(force)` | Stop running sprint |

## 4. Dispatch Flow

**`commands.py:202-250`** — The `run()` handler:

```
run(index_path, start_phase, end_phase, ...)
  |
  +-> load_sprint_config(...)              # lines 206-218
  |     +-> discover_phases(index_path)    # config.py:29
  |     +-> _resolve_release_dir()         # config.py:163
  |     +-> validate files/gaps            # config.py:237-247
  |     +-> SprintConfig(...)              # config.py:248-264
  |
  +-> _check_fidelity(config)             # lines 231-240 (optional block)
  |
  +-> --dry-run?
  |     YES -> _print_dry_run(config)      # line 242-244
  |     NO  -> continue
  |
  +-> tmux available && !--no-tmux?
        YES -> launch_in_tmux(config)      # line 247-248
        NO  -> execute_sprint(config)      # line 249-250
```

## 5. Configuration Loading

**`src/superclaude/cli/sprint/config.py`**:

### Phase Discovery (`discover_phases` — line 29)

1. Reads index markdown file
2. Regex-extracts canonical phase filenames (lines 20-26)
3. Parses optional "Execution Mode" column from markdown table (lines 44-96)
   - Maps each phase file to mode: `claude`, `python`, or `skip`
4. Falls back to directory scan if no phases found in index (lines 105-116)

### Release Directory Resolution (`_resolve_release_dir` — line 163)

Walks up from index path looking for release root pattern:
- If index is under `tasklist/tasklists/tasks`, grandparent is release dir

### Config Assembly (`load_sprint_config` — line 202)

1. Resolves and validates path (216-220)
2. Discovers phases (221)
3. Enriches phase names (228-231)
4. Auto-sets end phase if 0 (233-235)
5. Validates file existence and gaps (237-247)
6. Builds `SprintConfig` dataclass (248-264)
7. Validates active range is non-empty (266-273)

### Task Parsing (`parse_tasklist` — line 306)

Parses phase markdown into `TaskEntry` objects:
- Extracts headings as task boundaries
- Parses dependency annotations (342-349, 389-394)
- Extracts command field (for python-mode enforcement, 382-387)
- Extracts classifier field

## 6. Tmux Relay Path

**`src/superclaude/cli/sprint/tmux.py`**:

- `launch_in_tmux(config)` (line 50): Creates tmux session
- `_build_foreground_command(config)` (line 122): Reconstructs CLI command with `--no-tmux` flag
- Monitors sentinel exit code file for completion
- `attach_to_sprint()` (line 178): Reattach to existing session
- `kill_sprint(force)` (line 187): Terminate session
