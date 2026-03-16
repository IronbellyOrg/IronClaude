# D-0004 Evidence — TaskEntry.command Field and parse_tasklist() Extension

## Task
T01.03 — Add `command` Field to `TaskEntry` and Extend `parse_tasklist()`

## Change Locations
- `src/superclaude/cli/sprint/models.py` — `TaskEntry` dataclass
- `src/superclaude/cli/sprint/config.py` — `_COMMAND_RE` regex, `parse_tasklist()`, `parse_tasklist_file()`

## Changes Made

### models.py — TaskEntry
Added `command: str = ""` field:
```python
@dataclass
class TaskEntry:
    task_id: str
    title: str
    description: str = ""
    dependencies: list[str] = field(default_factory=list)
    command: str = ""
    classifier: str = ""
```

### config.py — New regex
```python
_COMMAND_RE = re.compile(
    r"\*\*Command:\*\*\s*`?([^`\n]+)`?",
    re.IGNORECASE,
)
```

### config.py — parse_tasklist()
Added extraction logic that:
1. Searches for `**Command:**` pattern in each task block
2. Strips surrounding backtick delimiters (`` ` ``)
3. Preserves all shell metacharacters verbatim (pipes `|`, redirects `>`, quotes)

## Verification
- `uv run pytest tests/sprint/test_preflight.py::TestTaskEntryCommand -v` → **6 passed**
- Command with pipes preserved: `uv run pytest tests/ | grep PASS > results.txt` ✓
- Command with quotes preserved: `cmd "arg with spaces" --flag` ✓
- Backtick stripping: `` `echo hello` `` → `echo hello` ✓
- No command → `""` ✓

## Date
2026-03-16
