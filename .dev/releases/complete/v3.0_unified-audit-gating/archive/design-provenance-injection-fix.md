# Design Spec: Harden `_inject_provenance_fields` Against Leading Whitespace

**Component**: `src/superclaude/cli/roadmap/executor.py`
**Scope**: Part 2 of Belt-and-Suspenders fix (defensive hardening)
**Status**: Design

---

## 1. Problem Statement

`_inject_provenance_fields` (line 155) silently aborts when LLM output contains
leading blank lines before the `---` frontmatter delimiter. The guard check at
line 167:

```python
if not content.startswith("---"):
    return
```

returns early because content is `"\n\n---\ntitle: ..."` rather than `"---\ntitle: ..."`.

`_sanitize_output` (line 82) runs first but has a matching bug: its guard at
line 101 checks `content.lstrip().startswith("---")` and returns 0 (no-op) when
leading whitespace precedes valid frontmatter, treating the file as "already
clean" without actually stripping the whitespace.

The same vulnerability exists in `_inject_pipeline_diagnostics` (line 134) which
uses an identical `content.startswith("---")` guard.

## 2. Design: Strip-in-Place Before Parsing

**Approach**: Strip leading whitespace from the `content` variable in-memory
before the frontmatter guard check. Do not rewrite the file solely for
whitespace stripping -- the file rewrite happens naturally when injecting
fields.

### 2.1 Changes to `_inject_provenance_fields` (line 155)

Replace:
```python
content = output_file.read_text(encoding="utf-8")
if not content.startswith("---"):
    return
```

With:
```python
content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
if not content.startswith("---"):
    return
```

The stripped content flows through to `output_file.write_text(new_content)` at
line 184, so the rewritten file will also have the leading whitespace removed.
This is correct behavior -- there is no semantic value in leading blank lines
before YAML frontmatter.

### 2.2 Changes to `_inject_pipeline_diagnostics` (line 123)

Apply the same fix for consistency:

Replace:
```python
content = output_file.read_text(encoding="utf-8")
if not content.startswith("---"):
    return
```

With:
```python
content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
if not content.startswith("---"):
    return
```

### 2.3 Why `.lstrip("\n\r\t ")` instead of `.lstrip()` or `.strip()`

- `.lstrip()` strips all Unicode whitespace including form feeds and vertical
  tabs, which is unnecessarily broad.
- `.strip()` would also strip trailing whitespace, which could corrupt content
  after the frontmatter body.
- `.lstrip("\n\r\t ")` targets exactly the characters LLMs prepend: newlines,
  carriage returns, tabs, and spaces.

## 3. Idempotency: Duplicate Provenance Fields

Current code blindly inserts provenance fields without checking whether they
already exist. If `_inject_provenance_fields` is called twice (e.g., retry
logic), the output gets duplicate `spec_source`, `generated`, and `generator`
lines. This produces invalid YAML (duplicate keys).

**Fix**: Before inserting, check whether each field already exists in the
frontmatter block.

```python
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

Apply the same idempotency pattern to `_inject_pipeline_diagnostics` for
`pipeline_diagnostics:`.

## 4. Edge Cases

| Case | Input | Expected Behavior |
|---|---|---|
| **Leading blank lines** | `\n\n---\ntitle: foo\n---\n` | Strip whitespace, inject fields, write clean file |
| **No frontmatter** | `Just plain text` | Return early (no-op), file unchanged |
| **Empty file** | `` | `.lstrip()` produces `""`, `startswith("---")` is False, return early |
| **Frontmatter with existing provenance** | `---\nspec_source: x\ngenerated: ...\n---` | Skip fields that exist, inject only missing ones |
| **All provenance present** | All 3 fields exist | Return early, file unchanged |
| **Unclosed frontmatter** | `---\ntitle: foo\n` (no closing `---`) | `end_idx == -1`, return early (no-op) |
| **Empty frontmatter block** | `---\n---\n` | `end_idx` found at position 3, inject all fields between delimiters |
| **Leading spaces only (no newlines)** | `   ---\ntitle: foo\n---` | `.lstrip()` strips spaces, `startswith("---")` succeeds |
| **CRLF line endings** | `\r\n\r\n---\r\ntitle: foo\r\n---` | `\r` is in the strip set, handled correctly |
| **Frontmatter value containing "spec_source:"** | `---\nnotes: "see spec_source: ..."` | Substring match is a false positive. Acceptable risk: provenance fields are machine-injected names unlikely to appear as substrings in values. If needed, tighten with regex `^spec_source:` (MULTILINE). |

## 5. Test Plan

All tests go in `tests/roadmap/test_executor.py`. Import `_inject_provenance_fields`
and `_inject_pipeline_diagnostics` alongside existing imports.

### 5.1 New Tests for `_inject_provenance_fields`

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

### 5.2 New Tests for `_inject_pipeline_diagnostics`

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

### 5.3 Regression Test for `_sanitize_output`

Add to existing `TestSanitizeOutput`:

```python
def test_strips_leading_whitespace_before_frontmatter(self, tmp_path):
    """Leading blank lines before --- should be stripped (Part 1 fix)."""
    f = tmp_path / "test.md"
    f.write_text("\n\n\n---\ntitle: foo\n---\nbody\n", encoding="utf-8")
    result = _sanitize_output(f)
    content = f.read_text(encoding="utf-8")
    assert content.startswith("---")
    assert result > 0  # bytes were stripped
```

## 6. Implementation Sequence

1. Apply `.lstrip("\n\r\t ")` to both `_inject_provenance_fields` and
   `_inject_pipeline_diagnostics` (2 one-line changes).
2. Add idempotency guards to both functions (field-existence checks before
   insertion).
3. Fix `_sanitize_output` to actually strip leading whitespace instead of
   treating it as "already clean" (change line 101-102 to strip and rewrite).
4. Add all tests from section 5.
5. Run `uv run pytest tests/roadmap/test_executor.py -v` to verify.

## 7. Risk Assessment

- **Risk**: Low. Changes are confined to post-processing helpers that run after
  subprocess completion and before gate validation. No prompt construction or
  subprocess logic is touched.
- **Blast radius**: Only affects files that have leading whitespace before
  frontmatter -- currently broken anyway, so fixing them is strictly better.
- **Backward compatibility**: Files that already start with `---` (no leading
  whitespace) are unaffected by `.lstrip()` since there is nothing to strip.
