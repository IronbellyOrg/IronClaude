# Troubleshoot Report — PR #75 Issue 1: coverage_gate UnicodeDecodeError uncaught

**Target**: auggie review #3290878760 on PR #75
**Tier reached**: 1
**Confidence**: 0.97
**Status**: success
**Severity**: medium

## Root Cause

`Path.read_text(encoding="utf-8")` raises `UnicodeDecodeError` when bytes don't decode as UTF-8 (UTF-16 BOM, Latin-1, binary blob, etc.). At `src/superclaude/cli/eval/coverage.py:312-315`:

```python
try:
    data = json.loads(settings_path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    return CoverageResult(parse_error=str(exc))
```

`UnicodeDecodeError` is in the hierarchy `UnicodeDecodeError → UnicodeError → ValueError → Exception`. It is NOT a subclass of `OSError` and NOT a subclass of `json.JSONDecodeError`, so the except tuple misses it. The exception propagates past the handler and crashes `coverage_gate()` — violating the H2 fail-closed contract at line 309 ("corrupt settings.json … MUST fail closed"). `CoverageResult.passed` (lines 156-162) already maps `parse_error is not None → passed=False`, so routing this case through `parse_error` is the correct fail-closed pathway.

## Proposed Fix

**Edit 1 (behavioral, required) — `src/superclaude/cli/eval/coverage.py`** (around line 314):

`old_string`:
```python
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return CoverageResult(parse_error=str(exc))
```

`new_string`:
```python
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return CoverageResult(parse_error=str(exc))
```

**Edit 2 (comment fidelity, optional) — same file, around line 309**:

`old_string`:
```python
    # (b) H2: corrupt settings.json (OSError / JSONDecodeError) MUST fail
```

`new_string`:
```python
    # (b) H2: corrupt settings.json (OSError / UnicodeDecodeError / JSONDecodeError) MUST fail
```

## Risk + Rollback

Very low. Single identifier added to existing except tuple. No control-flow change for inputs that already succeeded or raised the existing exception types. `UnicodeDecodeError` is a leaf class under `ValueError`; catching it does NOT broaden the net to swallow unrelated `ValueError`s. `str(UnicodeDecodeError)` yields a useful diagnostic ("'utf-8' codec can't decode byte 0xff in position 0: invalid start byte").

## Follow-up

Recommended (out of scope for the fix itself): add a unit test that writes `b"\xff\xfe"` to a temp `settings.json`, calls `coverage_gate`, and asserts `parse_error is not None`, `passed is False`, no exception escapes.

## Files that MUST NOT change

- `CoverageResult` dataclass (passed mapping already correct)
- Other except clauses or fail-closed paths elsewhere in the module
