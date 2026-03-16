# D-0008 Evidence — Python-Mode Empty Command Validation

## Task
T01.06 — Add Validation for Python-Mode Tasks with Empty Commands

## Change Location
- `src/superclaude/cli/sprint/config.py` — `parse_tasklist()` (validation block)

## Change Made
Added validation in `parse_tasklist()` after command extraction, before `tasks.append()`:

```python
# Validate python-mode tasks have a command (fail fast at parse time)
if execution_mode == "python" and not command:
    raise click.ClickException(
        f"Task {task_id} in python-mode phase has no command"
    )
```

## Behavior
- `execution_mode="python"` + empty command → raises `click.ClickException`
- `execution_mode="claude"` + empty command → no error (normal)
- `execution_mode="skip"` + empty command → no error
- Raises on the **first** task found without a command (fail-fast)
- Error message includes task_id for actionable diagnosis

## Verification
- `uv run pytest tests/sprint/test_preflight.py::TestPythonModeEmptyCommandValidation -v` → **5 passed**
- Exception message: `"Task T01.01 in python-mode phase has no command"` ✓
- claude/skip modes unaffected ✓
- Validation at parse time, not execution time ✓

## Date
2026-03-16
