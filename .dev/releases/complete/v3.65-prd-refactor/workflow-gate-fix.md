# Workflow: Section-Scoped Duplicate Heading Gate Fix

**Source**: `proposal-merged.md` (same directory)
**Optimized for**: `/sc:task-unified` execution
**Estimated diff**: ~115 lines across 5 files

---

## Task 1: Update type annotation in `pipeline/models.py`

**File**: `src/superclaude/cli/pipeline/models.py`
**Line**: 63
**Depends on**: nothing
**Blocked by**: nothing

### Change

```python
# Before (line 63):
check_fn: Callable[[str], bool]

# After:
check_fn: Callable[[str], bool | str]
```

### Verification

- `uv run pytest tests/roadmap/ -v --co` (collect-only, no runtime -- confirms no import errors)

---

## Task 2: Rewrite `_no_duplicate_headings` in `roadmap/gates.py`

**File**: `src/superclaude/cli/roadmap/gates.py`
**Lines**: 92-107
**Depends on**: Task 1 (type annotation must accept `bool | str` before function returns it)
**Blocked by**: Task 1

### Change

Replace the entire `_no_duplicate_headings` function (lines 92-107) with the section-scoped version from `proposal-merged.md` Section 1a. Key points:
- Return type changes from `bool` to `bool | str`
- H2 tracked globally via `seen_h2: set[str]`
- H3 tracked per-section via `h3_by_section: dict[str | None, set[str]]`
- H3s before any H2 scoped to `None` key (preamble)
- Returns `True` on pass, descriptive `str` on failure (with line number and section label)
- Uses `enumerate(content.splitlines(), start=1)` for line tracking

### Also update (same file, line ~916)

Update the `failure_message` in the `MERGE_GATE` `SemanticCheck` registration:

```python
# Before (line 916):
failure_message="Duplicate H2 or H3 heading text detected",

# After:
failure_message="Duplicate H2 (global) or H3 (within same H2 section) heading detected",
```

### Verification

- Function should be importable: `uv run python -c "from superclaude.cli.roadmap.gates import _no_duplicate_headings; print('OK')"`

---

## Task 3: Update consumer in `pipeline/gates.py`

**File**: `src/superclaude/cli/pipeline/gates.py`
**Lines**: 66-72
**Depends on**: Task 1 (type annotation), Task 2 (function now returns `str` on failure)
**Blocked by**: Task 1, Task 2

### Change

Replace the semantic check loop body (lines 66-72) with the `result is not True` dispatch pattern from `proposal-merged.md` Section 1b:

```python
    # STRICT: semantic checks
    if criteria.semantic_checks:
        for check in criteria.semantic_checks:
            result = check.check_fn(content)
            if result is not True:
                detail = result if isinstance(result, str) else check.failure_message
                return (
                    False,
                    f"Semantic check '{check.name}' failed: {detail}",
                )
```

### Backward compatibility note

Existing `bool`-returning checks return `False` on failure. `False is not True` is `True` (enters the branch). `isinstance(False, str)` is `False`, so `check.failure_message` is used as fallback. No change in behavior for other checks.

### Verification

- `uv run python -c "from superclaude.cli.pipeline.gates import gate_passed; print('OK')"`

---

## Task 4: Update existing test assertions (`is False` -> `is not True`)

**File 1**: `tests/roadmap/test_gates_data.py`
**Lines**: 171, 175
**File 2**: `tests/roadmap/test_validate_defects.py`
**Lines**: 50, 63
**Depends on**: Tasks 1-3 (code changes must be in place)
**Blocked by**: Task 2

### Changes in `test_gates_data.py`

```python
# test_no_duplicate_headings_h2_dup (line 171):
# Before:
assert _no_duplicate_headings(content) is False
# After:
assert _no_duplicate_headings(content) is not True

# test_no_duplicate_headings_h3_dup (line 175):
# Before:
assert _no_duplicate_headings(content) is False
# After:
assert _no_duplicate_headings(content) is not True
```

### Changes in `test_validate_defects.py`

```python
# test_duplicate_h2_headings_detected (line 50):
# Before:
assert _no_duplicate_headings(content) is False
# After:
assert _no_duplicate_headings(content) is not True

# test_duplicate_h3_headings_detected (line 63):
# Before:
assert _no_duplicate_headings(content) is False
# After:
assert _no_duplicate_headings(content) is not True
```

**Important**: Only change these 4 assertions. All other `is False` assertions in these files are for different functions and must remain unchanged.

### Verification

- `uv run pytest tests/roadmap/test_gates_data.py::TestSemanticChecks::test_no_duplicate_headings_h2_dup tests/roadmap/test_gates_data.py::TestSemanticChecks::test_no_duplicate_headings_h3_dup tests/roadmap/test_validate_defects.py::TestDuplicateDIDDetection -v`

---

## Task 5: Add `TestNoDuplicateHeadingsScoped` test class

**File**: `tests/roadmap/test_gates_data.py`
**Location**: After existing `test_no_duplicate_headings_h3_dup` test (after line ~175)
**Depends on**: Tasks 1-4 (code changes and assertion fixes in place)
**Blocked by**: Task 4

### Change

Add the complete `TestNoDuplicateHeadingsScoped` class from `proposal-merged.md` Section 3c. Contains 10 tests:

1. `test_h3_same_name_different_h2_parents_passes` -- the core false-positive fix
2. `test_h3_same_name_same_h2_parent_fails` -- same-section duplicates still caught
3. `test_h2_global_duplicate_still_fails` -- H2 global uniqueness preserved
4. `test_h3_before_any_h2_duplicate_fails` -- preamble scope duplicates caught
5. `test_h3_preamble_then_same_under_h2_passes` -- preamble vs H2 scope are distinct
6. `test_case_insensitive_h3_within_section_fails` -- case normalization
7. `test_empty_content_passes` -- edge case
8. `test_no_headings_passes` -- edge case
9. `test_failure_contains_line_number` -- diagnostic string validation
10. `test_real_roadmap_structure_passes` -- mirrors the actual failing roadmap

Copy the test code verbatim from `proposal-merged.md` Section 3c.

### Verification

- `uv run pytest tests/roadmap/test_gates_data.py::TestNoDuplicateHeadingsScoped -v`

---

## Task 6: Add regression test against real roadmap artifact

**File**: `tests/roadmap/test_gates_data.py`
**Location**: After `TestNoDuplicateHeadingsScoped` class
**Depends on**: Task 5
**Blocked by**: Task 5

### Change

Add the regression test from `proposal-merged.md` Section 3d:

```python
def test_prd_refactor_roadmap_passes_duplicate_gate():
    """Regression: the actual roadmap that exposed this bug should pass."""
    roadmap = Path(".dev/releases/backlog/prd-skill-refactor/roadmap.md")
    if not roadmap.exists():
        pytest.skip("roadmap file not present")
    content = roadmap.read_text()
    assert _no_duplicate_headings(content) is True
```

Ensure `Path` is imported from `pathlib` at the top of the file (add import if not present).

### Verification

- `uv run pytest tests/roadmap/test_gates_data.py::test_prd_refactor_roadmap_passes_duplicate_gate -v`

---

## Task 7: Full test suite validation

**Depends on**: Tasks 1-6
**Blocked by**: Task 6

### Run

1. **Targeted test run** (should be green before proceeding):
   ```bash
   uv run pytest tests/roadmap/test_gates_data.py tests/roadmap/test_validate_defects.py -v
   ```

2. **Full suite** (verify no regressions anywhere):
   ```bash
   uv run pytest
   ```

3. **Manual verification** (confirm the actual failing roadmap passes):
   ```bash
   uv run python -c "
   from pathlib import Path
   from superclaude.cli.roadmap.gates import _no_duplicate_headings
   content = Path('.dev/releases/backlog/prd-skill-refactor/roadmap.md').read_text()
   result = _no_duplicate_headings(content)
   assert result is True, f'Expected True, got: {result}'
   print('Regression check PASSED')
   "
   ```

### Expected outcome

- All existing tests pass (with updated assertions)
- All 10 new scoped tests pass
- Regression test passes (or skips if roadmap file absent)
- Full suite has zero new failures

---

## Dependency Graph

```
Task 1 (models.py type hint)
  |
  v
Task 2 (gates.py core rewrite)
  |
  v
Task 3 (pipeline/gates.py consumer) ---+
  |                                     |
  v                                     v
Task 4 (update existing assertions)
  |
  v
Task 5 (add scoped test class)
  |
  v
Task 6 (add regression test)
  |
  v
Task 7 (full validation)
```

## Files Summary

| File | Tasks | Type of change |
|------|-------|----------------|
| `src/superclaude/cli/pipeline/models.py` | 1 | 1 line: type annotation |
| `src/superclaude/cli/roadmap/gates.py` | 2 | ~30 lines: function rewrite + failure_message update |
| `src/superclaude/cli/pipeline/gates.py` | 3 | ~6 lines: consumer dispatch pattern |
| `tests/roadmap/test_gates_data.py` | 4, 5, 6 | 2 assertions updated + ~90 lines added (10 new tests + regression) |
| `tests/roadmap/test_validate_defects.py` | 4 | 2 assertions updated |
