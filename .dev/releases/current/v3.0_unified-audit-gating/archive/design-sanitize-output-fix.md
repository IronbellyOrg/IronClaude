# Design Spec: `_sanitize_output` Leading-Whitespace Fix

**Status**: Ready for implementation
**Scope**: `src/superclaude/cli/roadmap/executor.py` -- `_sanitize_output` function
**Related**: Part 1 of Solution C (belt-and-suspenders); Part 2 is hardening `_inject_provenance_fields`

---

## 1. Problem Statement

The `test-strategy` step fails gate validation because `spec_source` is missing from frontmatter. The root cause is a logic gap in `_sanitize_output`:

```
Line 101:  if content.lstrip().startswith("---"):
Line 102:      return 0
```

When LLM output is `\n\n---\ntitle: ...\n---\n...`, `content.lstrip().startswith("---")` evaluates to `True`, so the function returns 0 **without writing the stripped content back to disk**. The file retains the leading blank lines. Downstream, `_inject_provenance_fields` (line 167) checks `content.startswith("---")` (no lstrip), finds it starts with `\n\n`, and silently aborts -- leaving `spec_source` uninjected.

The same silent-abort bug affects `_inject_pipeline_diagnostics` (line 134).

## 2. Exact Code Change

**File**: `src/superclaude/cli/roadmap/executor.py`, function `_sanitize_output` (lines 82-120)

**Current code (lines 100-102)**:
```python
    # Already starts with frontmatter delimiter -- nothing to strip
    if content.lstrip().startswith("---"):
        return 0
```

**Replacement**:
```python
    # Strip leading blank lines (LLM outputs sometimes start with \n)
    stripped = content.lstrip("\n\r")
    if stripped == content:
        # No leading whitespace and no preamble text -- nothing to do
        if content.startswith("---"):
            return 0
    else:
        # Leading blank lines found; check if frontmatter is right after them
        if stripped.startswith("---"):
            import os

            preamble_bytes = len(content.encode("utf-8")) - len(stripped.encode("utf-8"))
            tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
            tmp_file.write_text(stripped, encoding="utf-8")
            os.replace(tmp_file, output_file)
            _log.info("Stripped %d-byte leading whitespace from %s", preamble_bytes, output_file)
            return preamble_bytes
```

Then the existing `re.search` block (lines 104-120) continues to handle the conversational-preamble case as before.

### Simplified alternative (preferred)

Rather than branching, move the lstrip to the top and let the existing logic handle everything uniformly:

**Replace lines 95-120 with**:
```python
    try:
        raw = output_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return 0

    # Normalize: strip leading blank lines that LLMs sometimes emit
    content = raw.lstrip("\n\r")

    # Already starts with frontmatter delimiter -- no preamble text to strip
    if content.startswith("---"):
        if content == raw:
            return 0  # file was already clean
        # Only leading newlines needed stripping; atomic write
        import os
        preamble_bytes = len(raw.encode("utf-8")) - len(content.encode("utf-8"))
        tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
        tmp_file.write_text(content, encoding="utf-8")
        os.replace(tmp_file, output_file)
        _log.info("Stripped %d-byte leading whitespace from %s", preamble_bytes, output_file)
        return preamble_bytes

    # Search for the first ^--- line (conversational preamble case)
    match = re.search(r"^---[ \t]*$", content, re.MULTILINE)
    if match is None:
        # No frontmatter found at all -- but still write back if we stripped newlines
        if content != raw:
            import os
            preamble_bytes = len(raw.encode("utf-8")) - len(content.encode("utf-8"))
            tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
            tmp_file.write_text(content, encoding="utf-8")
            os.replace(tmp_file, output_file)
            _log.info("Stripped %d-byte leading whitespace from %s (no frontmatter)", preamble_bytes, output_file)
            return preamble_bytes
        return 0

    preamble = content[: match.start()]
    cleaned = content[match.start():]
    preamble_bytes = len((raw[:len(raw) - len(content)] + preamble).encode("utf-8"))

    # Atomic write: tmp file + os.replace
    import os
    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(cleaned, encoding="utf-8")
    os.replace(tmp_file, output_file)

    _log.info("Stripped %d-byte preamble from %s", preamble_bytes, output_file)
    return preamble_bytes
```

**Recommendation**: The simplified alternative is more complex than needed. Use the **minimal fix** below instead.

### Minimal fix (recommended)

The smallest correct change: strip leading newlines early, then let existing logic run on the stripped content. Two lines change, one line added.

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
    content = raw.lstrip("\n\r")

    # Already starts with frontmatter delimiter -- no preamble to strip
    if content.startswith("---"):
        if content == raw:
            return 0
        # Leading newlines only -- write back the stripped version
        preamble_bytes = len(raw.encode("utf-8")) - len(content.encode("utf-8"))
        tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
        tmp_file.write_text(content, encoding="utf-8")
        os.replace(tmp_file, output_file)
        _log.info("Stripped %d-byte leading whitespace from %s", preamble_bytes, output_file)
        return preamble_bytes

    # Search for the first ^--- line
    match = re.search(r"^---[ \t]*$", content, re.MULTILINE)
    if match is None:
        # No frontmatter found at all -- leave file unchanged
        return 0

    preamble = content[: match.start()]
    cleaned = content[match.start():]
    # Total bytes stripped = leading newlines + conversational preamble
    preamble_bytes = len(raw.encode("utf-8")) - len(cleaned.encode("utf-8"))

    # Atomic write: tmp file + os.replace
    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(cleaned, encoding="utf-8")
    os.replace(tmp_file, output_file)

    _log.info("Stripped %d-byte preamble from %s", preamble_bytes, output_file)
    return preamble_bytes
```

## 3. Edge Cases

| # | Input                                       | Expected behavior                                    | Byte count returned |
|---|---------------------------------------------|------------------------------------------------------|---------------------|
| 1 | `---\ntitle: x\n---\nbody`                  | No change, file untouched                            | 0                   |
| 2 | `\n\n---\ntitle: x\n---\nbody`              | Leading `\n\n` stripped, file rewritten               | 2                   |
| 3 | `\r\n\n---\ntitle: x\n---\nbody`            | Leading `\r\n\n` stripped                             | 3                   |
| 4 | `Here is your output:\n\n---\ntitle: x\n---`| Preamble + leading newlines stripped                  | 22                  |
| 5 | `\n\nHere is output:\n---\ntitle: x\n---`   | Leading newlines stripped, then preamble stripped      | >0                  |
| 6 | `No frontmatter at all\n`                   | No change                                            | 0                   |
| 7 | (empty file)                                | No change                                            | 0                   |
| 8 | (file does not exist)                       | Returns 0, no error                                  | 0                   |
| 9 | (only whitespace: `\n\n\n`)                 | Stripped to empty; no `---` found; written back as-is | *see note below*    |

**Note on case 9**: `raw.lstrip("\n\r")` produces `""`, which does not start with `---` and `re.search` finds no match, so returns 0 and leaves the original whitespace-only file unchanged. This is acceptable behavior -- a whitespace-only file will fail gate validation regardless.

## 4. Impact on Other Pipeline Steps

`_sanitize_output` is called unconditionally for every step output (line 281). The change is safe for all steps because:

- Steps whose output already starts with `---` (no leading newlines): unchanged behavior, returns 0
- Steps whose output has conversational preamble: the existing preamble-stripping logic now also strips any leading newlines before the preamble text, which is strictly more correct
- Steps without frontmatter: unchanged behavior, returns 0

**Downstream consumers that use `content.startswith("---")`** (and would benefit from Part 2 hardening):
- `_inject_provenance_fields` (line 167) -- called for `test-strategy` step
- `_inject_pipeline_diagnostics` (line 134) -- called for `extract` step

After this fix, both will see content starting with `---` as intended. Part 2 (adding `.lstrip()` in those functions) is still recommended as defense-in-depth.

## 5. Test Cases

Add to `tests/roadmap/test_executor.py`, class `TestSanitizeOutput`:

### Test 1: Leading blank lines before frontmatter are stripped
```python
def test_leading_newlines_stripped(self, tmp_path):
    """Leading \\n\\n before --- should be stripped (bug fix)."""
    f = tmp_path / "output.md"
    body = "---\ntitle: test\n---\n## Content\n"
    f.write_text("\n\n" + body, encoding="utf-8")

    result = _sanitize_output(f)

    assert result == 2  # two newline bytes stripped
    assert f.read_text(encoding="utf-8") == body
```

### Test 2: Leading \\r\\n before frontmatter
```python
def test_leading_crlf_stripped(self, tmp_path):
    """Leading \\r\\n before --- should be stripped."""
    f = tmp_path / "output.md"
    body = "---\ntitle: test\n---\n## Content\n"
    f.write_text("\r\n\n" + body, encoding="utf-8")

    result = _sanitize_output(f)

    assert result == 3
    assert f.read_text(encoding="utf-8") == body
```

### Test 3: Leading newlines + conversational preamble
```python
def test_leading_newlines_plus_preamble(self, tmp_path):
    """Leading newlines followed by preamble text should all be stripped."""
    f = tmp_path / "output.md"
    preamble = "Here is the result:\n\n"
    body = "---\ntitle: test\n---\n## Content\n"
    f.write_text("\n\n" + preamble + body, encoding="utf-8")

    result = _sanitize_output(f)

    assert result == len(("\n\n" + preamble).encode("utf-8"))
    assert f.read_text(encoding="utf-8") == body
```

### Test 4: Empty file
```python
def test_empty_file(self, tmp_path):
    """Empty file should return 0 and remain unchanged."""
    f = tmp_path / "output.md"
    f.write_text("", encoding="utf-8")

    result = _sanitize_output(f)

    assert result == 0
    assert f.read_text(encoding="utf-8") == ""
```

### Test 5: Only whitespace
```python
def test_only_whitespace(self, tmp_path):
    """Whitespace-only file: no frontmatter found, returns 0, unchanged."""
    f = tmp_path / "output.md"
    f.write_text("\n\n\n", encoding="utf-8")

    result = _sanitize_output(f)

    assert result == 0
    assert f.read_text(encoding="utf-8") == "\n\n\n"
```

### Test 6: Integration -- sanitize enables provenance injection
```python
def test_sanitize_enables_provenance_injection(self, tmp_path):
    """After sanitize strips leading newlines, _inject_provenance_fields succeeds."""
    f = tmp_path / "output.md"
    content = "\n\n---\ntitle: test\n---\n## Content\n"
    f.write_text(content, encoding="utf-8")

    _sanitize_output(f)
    _inject_provenance_fields(f, "my-spec.md")

    result = f.read_text(encoding="utf-8")
    assert "spec_source: my-spec.md" in result
```

## 6. Implementation Checklist

1. Replace `_sanitize_output` in `src/superclaude/cli/roadmap/executor.py` with the minimal fix version from Section 2
2. Add test cases from Section 5 to `tests/roadmap/test_executor.py`
3. Run `uv run pytest tests/roadmap/test_executor.py -v` to verify all existing + new tests pass
4. (Part 2, separate commit) Harden `_inject_provenance_fields` and `_inject_pipeline_diagnostics` with `content = content.lstrip("\n\r")` after the `read_text` call
