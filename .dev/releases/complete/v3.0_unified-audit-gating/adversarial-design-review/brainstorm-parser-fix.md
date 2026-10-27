# Design: Fix `_parse_frontmatter` Quote Stripping

**Status**: PROPOSED
**Author**: Brainstorm (adversarial design review)
**Date**: 2026-03-18
**Scope**: `src/superclaude/cli/roadmap/gates.py` -- `_parse_frontmatter` function

---

## 1. Problem Statement

The hand-rolled YAML frontmatter parser in `gates.py:131-151` does not strip quote characters from parsed values. When an LLM generates frontmatter like:

```yaml
---
complexity_class: HIGH
interleave_ratio: "1:1"
---
```

the parser returns `{"interleave_ratio": '"1:1"'}` (value includes literal `"` characters). The semantic check `_interleave_ratio_consistent` at line 593 compares this against the bare string `"1:1"` and fails.

This affects **16 call sites** that consume `_parse_frontmatter` output. Any frontmatter value that an LLM wraps in quotes will carry literal quote characters into downstream comparisons, `int()` casts, `float()` casts, and string equality checks.

## 2. Proposed Solution: Add `_strip_yaml_quotes` Helper

### 2.1 Design Choice: Targeted Quote Stripping (Not a Real YAML Parser)

Three options were evaluated:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Replace with `yaml.safe_load` | Use stdlib/PyYAML | Handles all YAML | New dependency (PyYAML not in deps), changes return types (values become int/float/bool, not str), 16 callers need type updates |
| B. Add `_strip_yaml_quotes` to `_parse_frontmatter` | Strip matching outer quotes after `.strip()` | Minimal change, fixes the bug, no new deps | Still not a real YAML parser |
| C. Normalize at each call site | Each semantic check strips quotes itself | No parser change | 16 call sites to modify, easy to miss one, violates DRY |

**Recommendation: Option B** -- add a `_strip_yaml_quotes` helper called inside `_parse_frontmatter`. This fixes the root cause centrally with minimal blast radius. Option A is the "right" long-term answer but requires a larger refactor (tracked as RC-3 in the adversarial debate).

### 2.2 Exact Code Change

**New helper** (insert before `_parse_frontmatter`, around line 131):

```python
def _strip_yaml_quotes(value: str) -> str:
    """Strip matching outer YAML quotes (single or double) from a value.

    Handles the common case where LLMs wrap values in quotes:
      '"1:1"'  -> '1:1'
      "'1:1'"  -> '1:1'
      '"hello"' -> 'hello'

    Does NOT strip if quotes are unmatched or nested:
      '"1:1'   -> '"1:1'   (unmatched -- leave as-is)
      '""'     -> ''       (empty quoted string)
      '"he said \"hi\""' -> 'he said \"hi\"'  (outer quotes stripped, inner preserved)
    """
    if len(value) >= 2:
        if (value[0] == '"' and value[-1] == '"') or \
           (value[0] == "'" and value[-1] == "'"):
            return value[1:-1]
    return value
```

**Modified `_parse_frontmatter`** (change line 150):

```python
def _parse_frontmatter(content: str) -> dict[str, str] | None:
    """Extract YAML frontmatter key-value pairs from content.

    Returns a dict of key->value strings, or None if no frontmatter found.
    Values are stripped of whitespace and matching outer YAML quotes.
    """
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return None

    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return None

    result: dict[str, str] = {}
    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = _strip_yaml_quotes(value.strip())
    return result
```

The only change in the body is: `value.strip()` becomes `_strip_yaml_quotes(value.strip())`.

**Also fix `_frontmatter_values_non_empty`** (lines 102-120) and `_convergence_score_valid` (lines 279-300). These two functions do their own inline frontmatter parsing and do NOT call `_parse_frontmatter`. They have the same bug independently:

- `_frontmatter_values_non_empty` line 118: `if not value.strip()` -- should also strip quotes, otherwise `'""'` (empty quoted string) would appear non-empty. Change to: `if not _strip_yaml_quotes(value.strip())`.
- `_convergence_score_valid` line 295: `value = line.split(":", 1)[1].strip()` -- should also strip quotes. Change to: `value = _strip_yaml_quotes(line.split(":", 1)[1].strip())`.

### 2.3 Scope of Fix

After this change, the pipeline of effects is:

1. `_parse_frontmatter` strips quotes on ALL values at parse time.
2. All 16 call sites get clean values without any changes.
3. The two inline parsers (`_frontmatter_values_non_empty`, `_convergence_score_valid`) also get the fix.
4. No downstream callers need modification -- they already compare against bare strings.

## 3. Edge Cases and Risks

### 3.1 Edge Cases for `_strip_yaml_quotes`

| Input | Output | Rationale |
|-------|--------|-----------|
| `'"1:1"'` | `'1:1'` | Standard case -- LLM double-quoted a colon value |
| `"'1:1'"` | `'1:1'` | Single-quoted variant |
| `'1:1'` | `'1:1'` | No quotes -- unchanged (current behavior preserved) |
| `'"1:1'` | `'"1:1'` | Unmatched quotes -- leave as-is (fail-safe) |
| `'""'` | `''` | Empty quoted string -- stripped to empty |
| `"''"` | `''` | Empty single-quoted string |
| `'"he said \\"hi\\""'` | `'he said \\"hi\\"'` | Only outer quotes stripped |
| `'"'` | `'"'` | Single char is length 1, < 2, unchanged |
| `''` | `''` | Empty string, unchanged |
| `'"true"'` | `'true'` | Boolean-like value in quotes -- correctly stripped |
| `'"42"'` | `'42'` | Numeric value in quotes -- stripped, `int("42")` still works |
| `"' spaced '"` | `" spaced "` | Note: `.strip()` runs BEFORE `_strip_yaml_quotes`, so leading/trailing spaces inside quotes are preserved only if the LLM generated `value: ' spaced '` literally. In practice, `.strip()` on `" ' spaced '"` yields `"' spaced '"` which then strips to `" spaced "`. This is acceptable. |

### 3.2 Risk: Values That Legitimately Start and End with Quotes

Could a frontmatter value legitimately be `"something"` where the quotes are part of the value? In this codebase, **no**. All frontmatter values are:
- Enums: `LOW`, `MEDIUM`, `HIGH`, `standard`, `chunked`, `continuous-parallel`, `stop-and-fix`
- Booleans: `true`, `false`
- Numbers: `0`, `42`, `0.85`
- Ratios: `1:1`, `1:2`, `1:3`
- IDs: `DEV-001`, `DEV-002`
- Free text: file paths, dates, generator names

None of these legitimately carry outer quotes. The risk of false-positive stripping is effectively zero for this codebase.

### 3.3 Risk: Mixed Quotes

Input like `"'1:1'"` (double then single) -- the helper checks if `value[0]` and `value[-1]` are the SAME quote character. `'"...'` has `[0]='"'` and `[-1]="'"` -- mismatch, so no stripping occurs. This is correct behavior.

### 3.4 Risk: Breaking Existing Behavior

The fix is additive: values that had no quotes are unchanged (the helper is a no-op for them). All 340+ existing test assertions continue to pass because their fixture data uses unquoted values.

### 3.5 Non-Risk: YAML Arrays, Flow Mappings, Multi-line Values

The parser already ignores these. Adding quote stripping does not make the parser handle `[a, b]` or `{k: v}` -- nor should it. Those are out of scope for this minimal fix. If the LLM generates array-valued frontmatter, the existing parser already misparses it (and has done so since inception). That is tracked under RC-3 ("not a real YAML parser") for a future release.

## 4. Test Plan

### 4.1 Unit Tests for `_strip_yaml_quotes`

Add to `tests/roadmap/test_gates_data.py`:

```python
from superclaude.cli.roadmap.gates import _strip_yaml_quotes

class TestStripYamlQuotes:
    """Unit tests for the _strip_yaml_quotes helper."""

    def test_double_quoted_value(self):
        assert _strip_yaml_quotes('"1:1"') == "1:1"

    def test_single_quoted_value(self):
        assert _strip_yaml_quotes("'1:1'") == "1:1"

    def test_unquoted_value_unchanged(self):
        assert _strip_yaml_quotes("1:1") == "1:1"

    def test_unmatched_double_quote_start(self):
        assert _strip_yaml_quotes('"1:1') == '"1:1'

    def test_unmatched_double_quote_end(self):
        assert _strip_yaml_quotes('1:1"') == '1:1"'

    def test_mixed_quotes_not_stripped(self):
        assert _strip_yaml_quotes("\"1:1'") == "\"1:1'"

    def test_empty_double_quoted(self):
        assert _strip_yaml_quotes('""') == ""

    def test_empty_single_quoted(self):
        assert _strip_yaml_quotes("''") == ""

    def test_empty_string(self):
        assert _strip_yaml_quotes("") == ""

    def test_single_char(self):
        assert _strip_yaml_quotes('"') == '"'

    def test_nested_quotes_only_outer_stripped(self):
        assert _strip_yaml_quotes('"he said \\"hi\\""') == 'he said \\"hi\\"'

    def test_numeric_in_quotes(self):
        assert _strip_yaml_quotes('"42"') == "42"

    def test_boolean_in_quotes(self):
        assert _strip_yaml_quotes('"true"') == "true"
```

### 4.2 Integration Tests: Quoted Frontmatter Through `_parse_frontmatter`

Add to `tests/roadmap/test_gates_data.py`:

```python
from superclaude.cli.roadmap.gates import _parse_frontmatter

class TestParseFrontmatterQuoteStripping:
    """Verify _parse_frontmatter strips quotes from values."""

    def test_double_quoted_ratio(self):
        content = '---\ncomplexity_class: HIGH\ninterleave_ratio: "1:1"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm["interleave_ratio"] == "1:1"

    def test_single_quoted_ratio(self):
        content = "---\ncomplexity_class: HIGH\ninterleave_ratio: '1:1'\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["interleave_ratio"] == "1:1"

    def test_unquoted_value_unchanged(self):
        content = "---\ncomplexity_class: HIGH\ninterleave_ratio: 1:1\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["interleave_ratio"] == "1:1"

    def test_quoted_boolean(self):
        content = '---\ncertified: "true"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm["certified"] == "true"

    def test_quoted_integer(self):
        content = '---\nhigh_severity_count: "0"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm["high_severity_count"] == "0"

    def test_quoted_float(self):
        content = '---\nconvergence_score: "0.85"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm["convergence_score"] == "0.85"
```

### 4.3 End-to-End Test: The Exact Failing Scenario

```python
from superclaude.cli.roadmap.gates import _interleave_ratio_consistent

class TestInterleaveRatioQuotedValues:
    """Regression tests for the quoted-value gate failure."""

    def test_double_quoted_high_ratio(self):
        """The exact failing case from production."""
        content = '---\ncomplexity_class: HIGH\ninterleave_ratio: "1:1"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_double_quoted_low_ratio(self):
        content = '---\ncomplexity_class: LOW\ninterleave_ratio: "1:3"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_double_quoted_medium_ratio(self):
        content = '---\ncomplexity_class: MEDIUM\ninterleave_ratio: "1:2"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_single_quoted_ratio(self):
        content = "---\ncomplexity_class: HIGH\ninterleave_ratio: '1:1'\n---\n"
        assert _interleave_ratio_consistent(content) is True

    def test_quoted_complexity_class(self):
        content = '---\ncomplexity_class: "HIGH"\ninterleave_ratio: 1:1\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_both_quoted(self):
        content = '---\ncomplexity_class: "HIGH"\ninterleave_ratio: "1:1"\n---\n'
        assert _interleave_ratio_consistent(content) is True
```

### 4.4 Tests for Other Affected Semantic Checks

```python
from superclaude.cli.roadmap.gates import (
    _certified_is_true,
    _high_severity_count_zero,
    _convergence_score_valid,
    _frontmatter_values_non_empty,
    _validation_philosophy_correct,
    _major_issue_policy_correct,
)

class TestQuotedValuesAcrossChecks:
    """Verify quote stripping works for all semantic check types."""

    def test_certified_quoted_true(self):
        content = '---\ncertified: "true"\n---\n'
        assert _certified_is_true(content) is True

    def test_high_severity_quoted_zero(self):
        content = '---\nhigh_severity_count: "0"\n---\n'
        assert _high_severity_count_zero(content) is True

    def test_convergence_score_quoted(self):
        content = '---\nconvergence_score: "0.85"\n---\n'
        assert _convergence_score_valid(content) is True

    def test_validation_philosophy_quoted(self):
        content = '---\nvalidation_philosophy: "continuous-parallel"\n---\n'
        assert _validation_philosophy_correct(content) is True

    def test_major_issue_policy_quoted(self):
        content = '---\nmajor_issue_policy: "stop-and-fix"\n---\n'
        assert _major_issue_policy_correct(content) is True

    def test_frontmatter_values_non_empty_with_empty_quotes(self):
        """'""' should be treated as empty after stripping."""
        content = '---\nfield: ""\n---\n'
        assert _frontmatter_values_non_empty(content) is False
```

### 4.5 Regression: All Existing Tests Must Pass

Run `uv run pytest tests/roadmap/test_gates_data.py -v` -- all existing tests must continue to pass unchanged, since the fix is additive (no-op for unquoted values).

## 5. Implementation Checklist

1. [ ] Add `_strip_yaml_quotes` helper to `gates.py` (before `_parse_frontmatter`)
2. [ ] Modify `_parse_frontmatter` line 150 to call `_strip_yaml_quotes`
3. [ ] Modify `_frontmatter_values_non_empty` line 118 to call `_strip_yaml_quotes`
4. [ ] Modify `_convergence_score_valid` line 295 to call `_strip_yaml_quotes`
5. [ ] Add unit tests for `_strip_yaml_quotes` (section 4.1)
6. [ ] Add integration tests for `_parse_frontmatter` (section 4.2)
7. [ ] Add regression test for the exact failing scenario (section 4.3)
8. [ ] Add cross-check tests for other semantic checks (section 4.4)
9. [ ] Run full test suite to verify no regressions
10. [ ] Update `_parse_frontmatter` docstring to note quote stripping

## 6. What This Does NOT Fix

- **RC-3 (Not a real YAML parser)**: Arrays (`[a, b]`), flow mappings (`{k: v}`), multi-line values, anchors/aliases -- all remain unsupported. Tracked for future release.
- **RC-2 (LLM non-determinism)**: The LLM may still quote or not quote values. This fix makes the parser tolerant of either form.
- **RC-5 (No normalization layer)**: A proper normalization layer between parsing and semantic checks would be a larger refactor. This fix is a targeted normalization at the parse boundary.

## 7. Lines Changed Summary

| File | Lines Changed | Nature |
|------|--------------|--------|
| `src/superclaude/cli/roadmap/gates.py` | +18 new, ~3 modified | New helper + 3 one-line call-site changes |
| `tests/roadmap/test_gates_data.py` | +~80 new | New test classes |
| **Total** | ~100 lines | Minimal, focused |
