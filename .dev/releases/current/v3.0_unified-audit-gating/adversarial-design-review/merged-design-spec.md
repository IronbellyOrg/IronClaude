<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (design-integration-plan.md) — score 0.918 -->
<!-- Incorporated: Variant B (design-provenance-injection-fix.md), Variant C (design-sanitize-output-fix.md) -->
<!-- Merge date: 2026-03-18 -->

# Merged Design Spec: Solution C — Leading Whitespace Fix for Frontmatter Provenance Injection

**Bug**: `test-strategy` gate validation fails because `spec_source` frontmatter field is missing.

**Root cause**: `_inject_provenance_fields` (executor.py:167) checks `content.startswith("---")` but the LLM output has leading blank lines (`\n\n---`), causing silent abort. `_sanitize_output` runs first but only strips conversational *text* preamble — when content is `\n\n---...`, the `.lstrip().startswith("---")` check on line 101 returns True and the function exits with 0, leaving the leading newlines intact.

**Third affected function**: `_inject_pipeline_diagnostics` (line 134) has the identical `content.startswith("---")` guard — could affect the `extract` step.

**Affected pipeline flow** (executor.py:280-292):
```
_sanitize_output(step.output_file)        # line 281
_inject_pipeline_diagnostics(...)         # line 284 (extract only)
_inject_provenance_fields(...)            # line 292 (test-strategy only)
gate_passed(...)                          # downstream in execute_pipeline
```

---

## 1. Integration Sequence

<!-- Source: Base (original, modified) — charset updated per Change #1, code replaced per Change #3 -->

### Fix 1: `_sanitize_output` — strip leading blank lines (primary fix)

**File**: `src/superclaude/cli/roadmap/executor.py`, function `_sanitize_output` (line 82-120)

**Change**: Replace function body with the minimal fix that strips leading whitespace before all downstream processing.

**Current code (lines 100-102)** — THE BUG:
```python
# Already starts with frontmatter delimiter -- nothing to strip
if content.lstrip().startswith("---"):
    return 0
```

**Problem**: Returns 0 (no-op) when content is `\n\n---\nkey: val\n---\n`. The file still has leading newlines, so downstream `content.startswith("---")` checks fail.

**Complete replacement function**:
```python
def _sanitize_output(output_file: Path) -> int:
    """Strip conversational preamble and leading blank lines before YAML
    frontmatter in a step output file.

    Reads the file, strips leading blank lines, finds the first ``^---``
    line, and removes everything before it.  Uses atomic write (write to
    ``.tmp`` then ``os.replace()``) to prevent partial file states.

    Returns the byte count of the stripped content (0 when file already
    starts with ``---`` and has no preamble).
    """
    import os
    import re

    try:
        raw = output_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return 0

    # Strip leading blank lines (LLMs sometimes emit \n\n before ---)
    content = raw.lstrip("\n\r\t ")

    # Already starts with frontmatter delimiter -- no preamble to strip
    if content.startswith("---"):
        if content == raw:
            return 0
        # Leading whitespace only -- write back the stripped version
        preamble_bytes = len(raw.encode("utf-8")) - len(content.encode("utf-8"))
        tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
        tmp_file.write_text(content, encoding="utf-8")
        os.replace(tmp_file, output_file)
        _log.info("Stripped %d-byte leading whitespace from %s", preamble_bytes, output_file)
        return preamble_bytes

    # Search for the first ^--- line (conversational preamble case)
    match = re.search(r"^---[ \t]*$", content, re.MULTILINE)
    if match is None:
        # No frontmatter found at all -- leave file unchanged
        return 0

    preamble = content[: match.start()]
    cleaned = content[match.start():]
    # Total bytes stripped = leading whitespace + conversational preamble
    preamble_bytes = len(raw.encode("utf-8")) - len(cleaned.encode("utf-8"))

    # Atomic write: tmp file + os.replace
    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(cleaned, encoding="utf-8")
    os.replace(tmp_file, output_file)

    _log.info("Stripped %d-byte preamble from %s", preamble_bytes, output_file)
    return preamble_bytes
```

**Ordering guarantee**: This fix runs at line 281, before `_inject_provenance_fields` at line 292. After this fix, the file on disk will always start with `---` (no leading whitespace), so all downstream `content.startswith("---")` checks succeed.

<!-- Source: Base (original, modified) — expanded per Change #2 with idempotency from Variant B -->

### Fix 2: `_inject_provenance_fields` — defensive lstrip + idempotency (belt)

**File**: `src/superclaude/cli/roadmap/executor.py`, function `_inject_provenance_fields` (line 155-184)

**Change 2a — lstrip hardening**: Replace `content.startswith("---")` with lstripped content:

```python
content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
if not content.startswith("---"):
    return
```

**Change 2b — idempotency guards**: Replace the unconditional provenance injection with field-existence checks to prevent duplicate YAML keys on retry:

```python
# Find end of frontmatter
end_idx = content.find("\n---", 3)
if end_idx == -1:
    return

frontmatter = content[3:end_idx]  # text between opening --- and closing ---

fields_to_inject = []
if "spec_source:" not in frontmatter:
    fields_to_inject.append(f"spec_source: {spec_source}")
if "generated:" not in frontmatter:
    generated = datetime.now(timezone.utc).isoformat()
    fields_to_inject.append(f'generated: "{generated}"')
if "generator:" not in frontmatter:
    fields_to_inject.append("generator: superclaude-roadmap-executor")

if not fields_to_inject:
    return  # All fields already present

provenance_block = "\n".join(fields_to_inject)
new_content = content[:end_idx] + "\n" + provenance_block + content[end_idx:]
output_file.write_text(new_content, encoding="utf-8")
```

**Why both fixes are needed**:
- Even if Fix 1 regresses, Fix 2 independently handles leading whitespace via lstrip
- Even if Fix 2's lstrip were removed, Fix 1 ensures the file is clean before injection
- Idempotency guards prevent duplicate YAML keys regardless of which fix strips whitespace

<!-- Source: Base (original, modified) — expanded per Change #4 -->

### Fix 3: `_inject_pipeline_diagnostics` — same hardening

**File**: `src/superclaude/cli/roadmap/executor.py`, line 134

Apply the same defensive lstrip:
```python
content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
if not content.startswith("---"):
    return
```

Apply idempotency guard for `pipeline_diagnostics:`:
```python
frontmatter = content[3:end_idx]
if "pipeline_diagnostics:" in frontmatter:
    return  # Already injected
```

### Why `.lstrip("\n\r\t ")` instead of `.lstrip()` or `.lstrip("\n\r")`

<!-- Source: Variant B, Section 2.3 — merged per Change #1 -->

- `.lstrip()` strips all Unicode whitespace including form feeds and vertical tabs — unnecessarily broad
- `.lstrip("\n\r")` only strips newlines — misses tabs and spaces that LLMs may prepend
- `.lstrip("\n\r\t ")` targets exactly the characters LLMs prepend: newlines, carriage returns, tabs, and spaces

### Fix interaction matrix

| Scenario | Fix 1 only | Fix 2 only | Both |
|---|---|---|---|
| Leading blanks before frontmatter | Fixed by sanitize | Fixed by lstrip in inject | Fixed at both layers |
| Conversational preamble + leading blanks | Preamble stripped, blanks remain | Blanks stripped at inject time | Clean at both layers |
| No leading blanks | No-op (fast path) | No-op (fast path) | No-op (fast path) |
| Retry with existing provenance fields | N/A | Idempotency prevents duplicates | Safe |

---

<!-- Source: Variant C, Section 3 + Variant B, Section 4 — merged per Change #5 -->

## 2. Edge Cases

| # | Input | Expected behavior (`_sanitize_output`) | Byte count |
|---|-------|----------------------------------------|------------|
| 1 | `---\ntitle: x\n---\nbody` | No change, file untouched | 0 |
| 2 | `\n\n---\ntitle: x\n---\nbody` | Leading `\n\n` stripped, file rewritten | 2 |
| 3 | `\r\n\n---\ntitle: x\n---\nbody` | Leading `\r\n\n` stripped | 3 |
| 4 | `Here is your output:\n\n---\ntitle: x\n---` | Preamble + leading newlines stripped | 22 |
| 5 | `\n\nHere is output:\n---\ntitle: x\n---` | Leading newlines stripped, then preamble stripped | >0 |
| 6 | `No frontmatter at all\n` | No change | 0 |
| 7 | (empty file) | No change | 0 |
| 8 | (file does not exist) | Returns 0, no error | 0 |
| 9 | (only whitespace: `\n\n\n`) | No `---` found; file unchanged | 0 |
| 10 | `   ---\ntitle: x\n---` | Leading spaces stripped; `---` found | >0 |
| 11 | `\r\n\r\n---\r\ntitle: x\r\n---` | CRLF line endings; `\r` in strip set | >0 |

**Edge cases for `_inject_provenance_fields`**:

| # | Input | Expected behavior |
|---|-------|-------------------|
| 1 | `\n\n---\ntitle: foo\n---\nbody` | Strip whitespace, inject fields, write clean file |
| 2 | `Just plain text` | Return early (no-op), file unchanged |
| 3 | `""` (empty) | Return early, file unchanged |
| 4 | `---\nspec_source: x\ngenerated: ...\n---` | Skip fields that exist, inject only missing ones |
| 5 | All 3 provenance fields present | Return early, file unchanged |
| 6 | `---\ntitle: foo\n` (no closing `---`) | Return early (no-op) |
| 7 | `---\n---\nbody` (empty frontmatter) | Inject all fields between delimiters |

---

<!-- Source: Base (original, modified) — tests expanded per Change #6 -->

## 3. Regression Test Plan

### 3.1 New test class: `TestSanitizeOutputLeadingWhitespace`

**File**: `tests/roadmap/test_executor.py`

| Test ID | Fixture content | Expected behavior |
|---|---|---|
| `test_leading_newlines_stripped` | `\n\n---\ntitle: test\n---\n## Content\n` | Returns byte count of `\n\n`; file starts with `---` |
| `test_leading_crlf_stripped` | `\r\n\n---\ntitle: test\n---\n## Content\n` | Returns 3; file starts with `---` |
| `test_single_leading_newline_stripped` | `\n---\ntitle: test\n---\n## Content\n` | Returns 1; file starts with `---` |
| `test_no_leading_whitespace_unchanged` | `---\ntitle: test\n---\n## Content\n` | Returns 0; file unchanged |
| `test_no_frontmatter_with_leading_whitespace` | `\n\nJust text, no frontmatter.\n` | Returns 0; file unchanged |
| `test_leading_newlines_plus_preamble` | `\n\nHere is result:\n\n---\ntitle: test\n---\n` | Returns total bytes stripped; file starts with `---` |
| `test_empty_file` | `""` | Returns 0; file unchanged |
| `test_only_whitespace` | `\n\n\n` | Returns 0; file unchanged |

### 3.2 New test class: `TestInjectProvenanceFields`

<!-- Source: Variant B, Section 5.1 — merged per Change #6 -->

**File**: `tests/roadmap/test_executor.py`

```python
class TestInjectProvenanceFields:
    """Unit tests for _inject_provenance_fields whitespace and idempotency."""

    def test_injects_into_clean_frontmatter(self, tmp_path):
        """Baseline: fields injected when frontmatter starts at byte 0."""
        f = tmp_path / "test.md"
        f.write_text("---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert "spec_source: spec.md" in content
        assert "generator: superclaude-roadmap-executor" in content
        assert content.startswith("---")

    def test_injects_with_leading_blank_lines(self, tmp_path):
        """THE BUG: leading \\n\\n before --- must not prevent injection."""
        f = tmp_path / "test.md"
        f.write_text("\n\n---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert "spec_source: spec.md" in content
        assert content.startswith("---")  # leading whitespace stripped

    def test_noop_without_frontmatter(self, tmp_path):
        """Plain text file is left unchanged."""
        f = tmp_path / "test.md"
        original = "Just text, no frontmatter"
        f.write_text(original, encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        assert f.read_text(encoding="utf-8") == original

    def test_noop_empty_file(self, tmp_path):
        """Empty file is left unchanged."""
        f = tmp_path / "test.md"
        f.write_text("", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        assert f.read_text(encoding="utf-8") == ""

    def test_noop_unclosed_frontmatter(self, tmp_path):
        """Unclosed frontmatter (no closing ---) is left unchanged."""
        f = tmp_path / "test.md"
        original = "---\ntitle: foo\nbody\n"
        f.write_text(original, encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        assert f.read_text(encoding="utf-8") == original

    def test_idempotent_double_call(self, tmp_path):
        """Calling twice does not duplicate provenance fields."""
        f = tmp_path / "test.md"
        f.write_text("---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert content.count("spec_source:") == 1
        assert content.count("generator:") == 1

    def test_partial_provenance_present(self, tmp_path):
        """Only missing fields are injected when some already exist."""
        f = tmp_path / "test.md"
        f.write_text(
            '---\ntitle: foo\nspec_source: other.md\n---\nbody\n',
            encoding="utf-8",
        )
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert content.count("spec_source:") == 1  # not overwritten
        assert "spec_source: other.md" in content   # original preserved
        assert "generator:" in content               # missing field added

    def test_empty_frontmatter_block(self, tmp_path):
        """Empty frontmatter (just --- / ---) gets fields injected."""
        f = tmp_path / "test.md"
        f.write_text("---\n---\nbody\n", encoding="utf-8")
        _inject_provenance_fields(f, "spec.md")
        content = f.read_text(encoding="utf-8")
        assert "spec_source: spec.md" in content
```

### 3.3 New test class: `TestInjectPipelineDiagnostics`

<!-- Source: Variant B, Section 5.2 — merged per Change #4 -->

```python
class TestInjectPipelineDiagnostics:
    """Whitespace hardening tests for _inject_pipeline_diagnostics."""

    def test_injects_with_leading_blank_lines(self, tmp_path):
        """Leading whitespace before --- must not prevent injection."""
        f = tmp_path / "test.md"
        f.write_text("\n\n---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        t0 = datetime(2025, 1, 1, tzinfo=timezone.utc)
        t1 = datetime(2025, 1, 1, 0, 1, tzinfo=timezone.utc)
        _inject_pipeline_diagnostics(f, t0, t1)
        content = f.read_text(encoding="utf-8")
        assert "pipeline_diagnostics:" in content
        assert content.startswith("---")

    def test_idempotent_double_call(self, tmp_path):
        """Calling twice does not duplicate diagnostics."""
        f = tmp_path / "test.md"
        f.write_text("---\ntitle: foo\n---\nbody\n", encoding="utf-8")
        t0 = datetime(2025, 1, 1, tzinfo=timezone.utc)
        t1 = datetime(2025, 1, 1, 0, 1, tzinfo=timezone.utc)
        _inject_pipeline_diagnostics(f, t0, t1)
        _inject_pipeline_diagnostics(f, t0, t1)
        content = f.read_text(encoding="utf-8")
        assert content.count("pipeline_diagnostics:") == 1
```

### 3.4 E2E integration tests

<!-- Source: Base (original) -->

| Test ID | Description |
|---|---|
| `test_test_strategy_with_leading_blanks_passes_gate` | Mock runner writes test-strategy output with `\n\n---\n...` leading blanks. Verify full pipeline passes including TEST_STRATEGY_GATE. |
| `test_extract_with_leading_blanks_passes_gate` | Mock runner writes extract output with `\n---\n...`. Verify `_inject_pipeline_diagnostics` also works. |
| `test_sanitize_enables_provenance_injection` | After sanitize strips leading newlines, `_inject_provenance_fields` succeeds (from Variant C). |

### 3.5 Existing tests that must continue passing (regression guards)

<!-- Source: Base (original) -->

In `tests/roadmap/test_executor.py::TestSanitizeOutput`:
- `test_strips_preamble_before_frontmatter`
- `test_no_preamble_unchanged`
- `test_no_frontmatter_unchanged`
- `test_multi_line_preamble_stripped`
- `test_atomic_write_uses_tmp_and_replace`

In `tests/roadmap/test_gates_data.py::TestTestStrategyGateIntegration`:
- `test_gate_passes_clean_document`
- `test_gate_fails_wrong_ratio_for_complexity`
- `test_gate_fails_underscore_philosophy`

Full pipeline test: `test_full_pipeline_all_pass`

---

## 4. End-to-End Verification

<!-- Source: Base (original) -->

### 4.1 Automated verification

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

### 4.2 Manual verification

1. Create a test file with leading blank lines:
   ```bash
   printf '\n\n---\ncomplexity_class: MEDIUM\nvalidation_philosophy: continuous-parallel\nvalidation_milestones: 3\nwork_milestones: 6\ninterleave_ratio: 1:2\nmajor_issue_policy: stop-and-fix\n---\n## Test Strategy\n- item 1\n' > /tmp/test-strategy-leading-blanks.md
   ```

2. Run `_sanitize_output` on it:
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

3. Verify `_inject_provenance_fields` works on the sanitized file:
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

## 5. Rollback Plan

<!-- Source: Base (original) -->

### If Fix 1 (`_sanitize_output`) causes unexpected behavior

**Symptom**: Files are being incorrectly rewritten, losing content or corrupting output.

**Rollback**: Revert the `_sanitize_output` change to the original code. Fix 2 (`_inject_provenance_fields`) independently handles the test-strategy case via its own lstrip, so the gate failure is still resolved for the primary failing step.

**Risk assessment**: LOW. The change only adds a new code path for the case where leading whitespace exists before frontmatter. The existing preamble-stripping path is unchanged.

### If Fix 2 (`_inject_provenance_fields` / idempotency) causes unexpected behavior

**Symptom**: Provenance fields not injected, or injection corrupts frontmatter.

**Rollback**: Revert the lstrip + idempotency changes in `_inject_provenance_fields`. Fix 1 ensures the file is clean before this function runs, so the gate failure is still resolved.

**Risk assessment**: VERY LOW. The function already only runs for `step.id == "test-strategy"` (line 288). Idempotency guards only skip injection when fields already exist.

### If both fixes cause issues

**Full rollback**: Revert both changes. The pipeline returns to its current (broken) state.

---

## 6. Implementation Checklist

### Phase 1: Fix implementation

- [ ] **Fix 1**: Replace `_sanitize_output` in `src/superclaude/cli/roadmap/executor.py`
  - Use the complete function body from Section 1 (Fix 1)
  - Charset: `.lstrip("\n\r\t ")`
  - Preserve atomic write pattern (`.tmp` + `os.replace()`)

- [ ] **Fix 2**: Update `_inject_provenance_fields` in `src/superclaude/cli/roadmap/executor.py`
  - Add `.lstrip("\n\r\t ")` to `read_text` call (line 167)
  - Add idempotency guards (field-existence checks before insertion)

- [ ] **Fix 3**: Update `_inject_pipeline_diagnostics` in `src/superclaude/cli/roadmap/executor.py`
  - Add `.lstrip("\n\r\t ")` to `read_text` call (line 134)
  - Add idempotency guard for `pipeline_diagnostics:`

### Phase 2: Test implementation

- [ ] Add `TestSanitizeOutputLeadingWhitespace` — 8 test cases per Section 3.1
- [ ] Add `TestInjectProvenanceFields` — 8 test cases per Section 3.2
- [ ] Add `TestInjectPipelineDiagnostics` — 2 test cases per Section 3.3
- [ ] Add E2E integration tests — 3 test cases per Section 3.4

### Phase 3: Verification

- [ ] Run `uv run pytest tests/roadmap/test_executor.py -v` — all pass
- [ ] Run `uv run pytest tests/roadmap/test_gates_data.py -v` — all pass
- [ ] Run `uv run pytest tests/pipeline/test_gates.py -v` — all pass
- [ ] Run `uv run pytest tests/ -v` — full suite passes
- [ ] Manual verification per Section 4.2

### Phase 4: Sync and commit

- [ ] Run `make sync-dev`
- [ ] Run `make verify-sync`
- [ ] Commit: `fix: strip leading whitespace before frontmatter provenance injection`

---

## 7. Files Modified

| File | Lines | Change |
|---|---|---|
| `src/superclaude/cli/roadmap/executor.py` | 82-120 | `_sanitize_output`: full function replacement with leading-whitespace stripping |
| `src/superclaude/cli/roadmap/executor.py` | 134 | `_inject_pipeline_diagnostics`: add `.lstrip("\n\r\t ")` + idempotency guard |
| `src/superclaude/cli/roadmap/executor.py` | 155-184 | `_inject_provenance_fields`: add `.lstrip("\n\r\t ")` + idempotency guards |
| `tests/roadmap/test_executor.py` | (append) | 21 new test cases across 3 new test classes + 3 E2E tests |
