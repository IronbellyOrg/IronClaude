# Design Spec: Solution C -- Leading Whitespace Fix for Frontmatter Provenance Injection

**Bug**: `test-strategy` gate validation fails because `spec_source` frontmatter field is missing.

**Root cause**: `_inject_provenance_fields` (executor.py:167) checks `content.startswith("---")` but the LLM output has leading blank lines (`\n\n---`), causing silent abort. `_sanitize_output` runs first but only strips conversational *text* preamble -- when content is `\n\n---...`, the `.lstrip().startswith("---")` check on line 101 returns True and the function exits with 0, leaving the leading newlines intact.

**Affected pipeline flow** (executor.py:280-292):
```
_sanitize_output(step.output_file)        # line 281
_inject_provenance_fields(...)             # line 292 (test-strategy only)
gate_passed(...)                           # downstream in execute_pipeline
```

---

## 1. Integration Sequence

### Fix 1: `_sanitize_output` -- strip leading blank lines (primary fix)

**File**: `src/superclaude/cli/roadmap/executor.py`, function `_sanitize_output` (line 82-120)

**Change**: After reading file content (line 96), strip leading whitespace before the `startswith("---")` early-return check. When content has leading blank lines but no conversational preamble, rewrite the file with leading whitespace removed.

**Current code** (line 100-102):
```python
# Already starts with frontmatter delimiter -- nothing to strip
if content.lstrip().startswith("---"):
    return 0
```

**Problem**: This returns 0 (no-op) when content is `\n\n---\nkey: val\n---\n`. The file still has leading newlines, so downstream `content.startswith("---")` checks fail.

**Proposed code**:
```python
# Check if content starts with frontmatter after stripping whitespace
stripped = content.lstrip()
if stripped.startswith("---"):
    if stripped == content:
        # Already clean -- no rewrite needed
        return 0
    # Leading whitespace present before frontmatter -- strip it
    preamble_bytes = len(content.encode("utf-8")) - len(stripped.encode("utf-8"))
    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(stripped, encoding="utf-8")
    os.replace(tmp_file, output_file)
    _log.info("Stripped %d-byte leading whitespace from %s", preamble_bytes, output_file)
    return preamble_bytes
```

**Ordering guarantee**: This fix runs at line 281, before `_inject_provenance_fields` at line 292. After this fix, the file on disk will always start with `---` (no leading whitespace), so `_inject_provenance_fields` will find frontmatter correctly.

### Fix 2: `_inject_provenance_fields` -- defensive `.lstrip()` (belt)

**File**: `src/superclaude/cli/roadmap/executor.py`, function `_inject_provenance_fields` (line 155-184)

**Change**: Replace `content.startswith("---")` with `content.lstrip().startswith("---")` on line 167, and adjust the `end_idx` search accordingly.

**Current code** (line 167-168):
```python
if not content.startswith("---"):
    return
```

**Proposed code**:
```python
content = content.lstrip()
if not content.startswith("---"):
    return
```

**Note**: Since `_inject_provenance_fields` rewrites the entire file (line 184), using the lstripped content for the rewrite also removes leading whitespace as a side effect. This means even if Fix 1 regresses, Fix 2 independently handles the problem.

### Why both fixes are needed

| Scenario | Fix 1 only | Fix 2 only | Both |
|---|---|---|---|
| Leading blanks before frontmatter | Fixed by sanitize | Not fixed until provenance inject; `_inject_pipeline_diagnostics` (line 134) also has `.startswith("---")` and would fail for extract step | Fixed at both layers |
| Conversational preamble + leading blanks | Preamble stripped, blanks remain | Blanks stripped at inject time | Clean at both layers |
| No leading blanks | No-op (fast path) | No-op (fast path) | No-op (fast path) |

---

## 2. Regression Test Plan

### 2.1 New test class: `TestSanitizeOutputLeadingWhitespace`

**File**: `tests/roadmap/test_executor.py` (add to existing `TestSanitizeOutput` class or new sibling class)

| Test ID | Fixture content | Expected behavior |
|---|---|---|
| `test_leading_newlines_stripped` | `\n\n---\ntitle: test\n---\n## Content\n` | Returns byte count of `\n\n`; file starts with `---` |
| `test_leading_spaces_and_newlines_stripped` | `  \n \n---\ntitle: test\n---\n## Content\n` | Returns byte count of leading whitespace; file starts with `---` |
| `test_single_leading_newline_stripped` | `\n---\ntitle: test\n---\n## Content\n` | Returns 1; file starts with `---` |
| `test_no_leading_whitespace_unchanged` | `---\ntitle: test\n---\n## Content\n` | Returns 0; file unchanged |
| `test_no_frontmatter_with_leading_whitespace` | `\n\nJust text, no frontmatter.\n` | Returns 0; file unchanged (no `---` found) |
| `test_preamble_with_leading_whitespace` | `\n\nHere is the result:\n\n---\ntitle: test\n---\n` | Returns byte count of `\n\nHere is the result:\n\n`; file starts with `---` |

### 2.2 New test class: `TestInjectProvenanceFieldsLeadingWhitespace`

**File**: `tests/roadmap/test_executor.py` (new class)

| Test ID | Fixture content | Expected behavior |
|---|---|---|
| `test_inject_with_leading_newlines` | `\n\n---\ncomplexity_class: MEDIUM\n---\n## Content\n` | `spec_source`, `generated`, `generator` fields present in output |
| `test_inject_with_clean_frontmatter` | `---\ncomplexity_class: MEDIUM\n---\n## Content\n` | Same -- fields injected (existing behavior, regression guard) |
| `test_inject_no_frontmatter_skipped` | `No frontmatter here.\n` | File unchanged (no injection) |
| `test_inject_no_closing_fence_skipped` | `---\ncomplexity_class: MEDIUM\nno closing fence` | File unchanged (no injection) |

### 2.3 End-to-end integration test: `TestLeadingWhitespaceE2E`

**File**: `tests/roadmap/test_executor.py` (new class within `TestIntegrationMockSubprocess` or sibling)

| Test ID | Description |
|---|---|
| `test_test_strategy_with_leading_blanks_passes_gate` | Mock runner writes test-strategy output with `\n\n---\n...` leading blanks. Verify full pipeline passes including TEST_STRATEGY_GATE. This confirms sanitize + inject + gate all work together. |
| `test_extract_with_leading_blanks_passes_gate` | Mock runner writes extract output with `\n---\n...`. Verify `_inject_pipeline_diagnostics` also works (it has the same `.startswith("---")` pattern at line 134). |

### 2.4 Existing tests that must continue passing (regression guards)

These existing tests in `tests/roadmap/test_executor.py::TestSanitizeOutput` must not change behavior:

- `test_strips_preamble_before_frontmatter` -- conversational preamble still stripped
- `test_no_preamble_unchanged` -- clean files still return 0
- `test_no_frontmatter_unchanged` -- no frontmatter still returns 0
- `test_multi_line_preamble_stripped` -- multi-line preamble still stripped
- `test_atomic_write_uses_tmp_and_replace` -- atomic write pattern preserved

These existing tests in `tests/roadmap/test_gates_data.py::TestTestStrategyGateIntegration` must not change:

- `test_gate_passes_clean_document` -- clean document still passes
- `test_gate_fails_wrong_ratio_for_complexity` -- semantic checks still enforced
- `test_gate_fails_underscore_philosophy` -- semantic checks still enforced

The full pipeline test `test_full_pipeline_all_pass` must continue passing.

---

## 3. End-to-End Verification

### 3.1 Automated verification

```bash
# Run all roadmap executor tests
uv run pytest tests/roadmap/test_executor.py -v

# Run all gate data tests
uv run pytest tests/roadmap/test_gates_data.py -v

# Run pipeline gate tests
uv run pytest tests/pipeline/test_gates.py -v

# Run full test suite to catch cross-cutting regressions
uv run pytest tests/ -v --timeout=120
```

### 3.2 Manual verification

1. Create a test file with leading blank lines:
   ```bash
   printf '\n\n---\ncomplexity_class: MEDIUM\nvalidation_philosophy: continuous-parallel\nvalidation_milestones: 3\nwork_milestones: 6\ninterleave_ratio: 1:2\nmajor_issue_policy: stop-and-fix\n---\n## Test Strategy\n- item 1\n' > /tmp/test-strategy-leading-blanks.md
   ```

2. Run `_sanitize_output` on it via a Python one-liner:
   ```bash
   uv run python -c "
   from pathlib import Path
   from superclaude.cli.roadmap.executor import _sanitize_output
   f = Path('/tmp/test-strategy-leading-blanks.md')
   result = _sanitize_output(f)
   print(f'Stripped {result} bytes')
   content = f.read_text()
   print(f'Starts with ---: {content.startswith(\"---\")}')
   "
   ```

3. Verify the `_inject_provenance_fields` path by calling it on a file with leading blanks:
   ```bash
   uv run python -c "
   from pathlib import Path
   from superclaude.cli.roadmap.executor import _inject_provenance_fields
   f = Path('/tmp/test-strategy-leading-blanks.md')
   _inject_provenance_fields(f, 'test-spec.md')
   content = f.read_text()
   print(f'Has spec_source: {\"spec_source\" in content}')
   print(f'Has generated: {\"generated\" in content}')
   print(f'Has generator: {\"generator\" in content}')
   "
   ```

---

## 4. Rollback Plan

### If Fix 1 (`_sanitize_output`) causes unexpected behavior

**Symptom**: Files are being incorrectly rewritten, losing content or corrupting output.

**Rollback**: Revert the `_sanitize_output` change to the original code. Fix 2 (`_inject_provenance_fields`) independently handles the test-strategy case, so the gate failure is still resolved for the primary failing step.

**Risk assessment**: LOW. The change only adds a new code path for the case where `content.lstrip().startswith("---")` is True but `content.startswith("---")` is False (i.e., leading whitespace exists). The existing preamble-stripping path is unchanged.

### If Fix 2 (`_inject_provenance_fields`) causes unexpected behavior

**Symptom**: Provenance fields are injected into files that should not have them, or injection corrupts frontmatter.

**Rollback**: Revert the `.lstrip()` addition in `_inject_provenance_fields`. Fix 1 ensures the file is clean before this function runs, so the gate failure is still resolved.

**Risk assessment**: VERY LOW. The function already only runs for `step.id == "test-strategy"` (line 288). Adding `.lstrip()` only affects files that have leading whitespace, and the rewrite via `output_file.write_text(new_content)` already replaces the entire file.

### If both fixes cause issues

**Full rollback**: Revert both changes. The pipeline returns to its current (broken) state. File a new issue with diagnostic output from the failing case.

---

## 5. Implementation Checklist

### Phase 1: Fix implementation

- [ ] **Fix 1**: Edit `src/superclaude/cli/roadmap/executor.py` lines 100-102
  - Replace the early-return block in `_sanitize_output` with whitespace-stripping logic
  - Preserve atomic write pattern (`.tmp` + `os.replace()`)
  - Add `import os` is already present at line 92 (inside function)

- [ ] **Fix 2**: Edit `src/superclaude/cli/roadmap/executor.py` line 167
  - Add `content = content.lstrip()` before the `startswith("---")` check in `_inject_provenance_fields`

- [ ] **Audit sibling function**: Check `_inject_pipeline_diagnostics` (line 134) for the same bug
  - Line 134: `if not content.startswith("---"):` -- same vulnerability
  - Apply same defensive `.lstrip()` fix

### Phase 2: Test implementation

- [ ] Add `TestSanitizeOutputLeadingWhitespace` class to `tests/roadmap/test_executor.py`
  - 6 test cases per section 2.1

- [ ] Add `TestInjectProvenanceFieldsLeadingWhitespace` class to `tests/roadmap/test_executor.py`
  - 4 test cases per section 2.2
  - Requires importing `_inject_provenance_fields` (already imported pattern in file: see line 28)

- [ ] Add E2E integration test for leading-blanks scenario to `tests/roadmap/test_executor.py`
  - 2 test cases per section 2.3

### Phase 3: Verification

- [ ] Run `uv run pytest tests/roadmap/test_executor.py -v` -- all pass
- [ ] Run `uv run pytest tests/roadmap/test_gates_data.py -v` -- all pass
- [ ] Run `uv run pytest tests/pipeline/test_gates.py -v` -- all pass
- [ ] Run `uv run pytest tests/ -v` -- full suite passes
- [ ] Manual verification per section 3.2

### Phase 4: Sync and commit

- [ ] Run `make sync-dev` (if executor.py is under src/)
- [ ] Run `make verify-sync`
- [ ] Commit with message: `fix: strip leading whitespace before frontmatter provenance injection`

---

## 6. Files Modified

| File | Lines | Change |
|---|---|---|
| `src/superclaude/cli/roadmap/executor.py` | 100-102 | `_sanitize_output`: strip leading whitespace when frontmatter present |
| `src/superclaude/cli/roadmap/executor.py` | 134 | `_inject_pipeline_diagnostics`: add defensive `.lstrip()` |
| `src/superclaude/cli/roadmap/executor.py` | 167 | `_inject_provenance_fields`: add defensive `.lstrip()` |
| `tests/roadmap/test_executor.py` | (append) | 12 new test cases across 3 new test classes |
