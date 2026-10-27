# Brainstorm: Replace `_parse_frontmatter` with `yaml.safe_load`

## Status: PROPOSAL
## Date: 2026-03-18
## Author: Adversarial Design Review

---

## 1. Problem Recap

The hand-rolled parser at `src/superclaude/cli/roadmap/gates.py:131-151` splits on the first colon and strips whitespace, but does NOT strip YAML quote characters. When the LLM emits `interleave_ratio: "1:1"` (valid YAML -- quotes are needed because the value contains a colon), the parser returns the literal string `"1:1"` (with embedded double-quote chars), which fails the comparison against the expected `1:1` at line 593.

This affects all 22 semantic check functions that consume `_parse_frontmatter`.

## 2. Dependency Check

PyYAML (`pyyaml>=6.0`) is already declared in `pyproject.toml` line 38:

```toml
dependencies = [
    "pytest>=7.0.0",
    "click>=8.0.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
]
```

It is already imported in two production modules:
- `src/superclaude/cli/roadmap/spec_patch.py:36`
- `src/superclaude/cli/cli_portify/executor.py:41`

No new dependency is introduced.

## 3. Proposed Code Change

### 3.1 Replace `_parse_frontmatter` (gates.py:131-151)

**Before:**
```python
def _parse_frontmatter(content: str) -> dict[str, str] | None:
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
            result[key.strip()] = value.strip()
    return result
```

**After:**
```python
def _parse_frontmatter(content: str) -> dict[str, Any] | None:
    """Extract YAML frontmatter key-value pairs from content.

    Uses yaml.safe_load for correct YAML parsing (handles quoted values,
    typed scalars, etc.). All values are converted to strings for backward
    compatibility with existing semantic checks.

    Returns a dict of key -> str(value), or None if no frontmatter found.
    """
    import yaml

    stripped = content.lstrip()
    if not stripped.startswith("---"):
        return None

    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return None

    frontmatter_text = rest[:end_idx]
    if not frontmatter_text.strip():
        return None

    try:
        parsed = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None

    if not isinstance(parsed, dict):
        return None

    # Stringify all values for backward compat with semantic checks
    # that call int(), float(), .lower(), .strip(), etc. on values.
    result: dict[str, str] = {}
    for key, value in parsed.items():
        result[str(key)] = str(value) if value is not None else ""
    return result
```

### 3.2 Also fix `_frontmatter_values_non_empty` (gates.py:102-120)

This function has its own inline frontmatter parsing (does NOT use `_parse_frontmatter`). It should be refactored to delegate to the shared parser for consistency. However, this check specifically tests whether any field has an empty value *as written*, and `yaml.safe_load` will parse `key:` (no value) as `None`. The stringification layer converts `None` to `""`, so the check `if not value.strip()` will still catch empty values correctly.

**After:**
```python
def _frontmatter_values_non_empty(content: str) -> bool:
    """All YAML frontmatter fields have non-empty values."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    for key, value in fm.items():
        if not value.strip():
            return False
    return True
```

### 3.3 Also fix `_convergence_score_valid` (gates.py:279-300)

This function has its own inline frontmatter parsing. Refactor to use `_parse_frontmatter`:

**After:**
```python
def _convergence_score_valid(content: str) -> bool:
    """convergence_score frontmatter value parses as float in [0.0, 1.0]."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("convergence_score")
    if value is None:
        return False
    try:
        score = float(value)
        return 0.0 <= score <= 1.0
    except (ValueError, TypeError):
        return False
```

## 4. Type Coercion Analysis

`yaml.safe_load` returns typed Python values. Our stringification layer (`str(value)`) normalizes them back to strings for the existing check functions. Here is the impact analysis for every value type:

| YAML input | `yaml.safe_load` type | `str()` output | Existing check behavior |
|---|---|---|---|
| `interleave_ratio: "1:1"` | `str` "1:1" | "1:1" | FIXED -- was `"1:1"` with quotes |
| `interleave_ratio: 1:1` | `str` "1:1" (YAML sexagesimal) | "1:1" | Unchanged (was already "1:1") |
| `high_severity_count: 0` | `int` 0 | "0" | `int("0")` works -- unchanged |
| `convergence_score: 0.85` | `float` 0.85 | "0.85" | `float("0.85")` works -- unchanged |
| `certified: true` | `bool` True | "True" | `.lower() == "true"` works -- unchanged |
| `certified: false` | `bool` False | "False" | `.lower() == "true"` correctly fails |
| `tasklist_ready: true` | `bool` True | "True" | `.lower() == "true"` works |
| `complexity_class: HIGH` | `str` "HIGH" | "HIGH" | `.upper()` works -- unchanged |
| `validation_philosophy: continuous-parallel` | `str` | same | unchanged |
| `major_issue_policy: stop-and-fix` | `str` | same | unchanged |
| `routing_fix_roadmap: DEV-001 DEV-002` | `str` | same | `re.split` works -- unchanged |
| `extraction_mode: chunked (3 chunks)` | `str` | same | unchanged |
| `title:` (empty) | `None` | `""` | non-empty check catches it |

**CRITICAL EDGE CASE -- `certified: 1`:**
Currently, `_certified_is_true` correctly rejects `1` because `"1".lower() != "true"`. With `yaml.safe_load`, `certified: 1` parses as `int(1)`, then `str(1)` = `"1"`, then `"1".lower() != "true"` -- still correctly rejected. No regression.

**CRITICAL EDGE CASE -- `certified: yes`:**
`yaml.safe_load` parses `yes` as `bool(True)`, so `str(True)` = `"True"`, then `"True".lower() == "true"` -- this would PASS. Currently it FAILS because `"yes".lower() != "true"`.

This is a **behavioral change**. The current test `test_malformed_yes_fails` (line 747) would break.

### 4.1 Mitigation for `yes`/`no`/`on`/`off` YAML Booleans

PyYAML 6.0+ (with the default FullLoader or SafeLoader) treats `yes`, `no`, `on`, `off`, `y`, `n` as booleans per YAML 1.1 spec. This is actually MORE correct than the hand-rolled parser, but it changes the contract for `_certified_is_true`.

**Option A (recommended): Accept the broader YAML boolean set.** If the LLM writes `certified: yes`, that IS semantically `true` in YAML. The test should be updated. This is more robust against LLM variation.

**Option B: Add explicit rejection after parsing.** Check the raw frontmatter text to reject non-canonical boolean spellings. This preserves the current strict contract but adds complexity.

**Recommendation:** Option A. The purpose of `_certified_is_true` is to verify the document IS certified. If the LLM writes `certified: yes`, that intent is clear. The YAML spec agrees. Update the test.

Similarly for `_validation_complete_true` and `_tasklist_ready_consistent`, which also check `.lower() == "true"`. After stringification, `yaml.safe_load("yes")` becomes `str(True)` = `"True"`, so `.lower() == "true"` passes. Same reasoning applies -- accept it.

## 5. The `generated` Datetime Field

**Input:** `generated: "2026-03-18T00:00:00Z"`

With quotes, `yaml.safe_load` returns the string `"2026-03-18T00:00:00Z"`. Stringified: `"2026-03-18T00:00:00Z"`. No issue.

**Input:** `generated: 2026-03-18T00:00:00Z` (without quotes)

`yaml.safe_load` parses this as a `datetime.datetime` object. `str(datetime(...))` returns `"2026-03-18 00:00:00+00:00"` -- different format from the original. However, no semantic check currently examines the `generated` field's value (it is only checked for presence in the frontmatter field list, at `pipeline/gates.py:54`). The frontmatter presence check happens in `pipeline/gates.py:_check_frontmatter`, which is a SEPARATE code path from `_parse_frontmatter` in `roadmap/gates.py`.

**Risk: NONE.** The `generated` field is never read by any semantic check function. It is only validated for existence by the pipeline gate infrastructure.

**Future-proofing:** If a semantic check is ever added for `generated`, it should handle both string formats or force the frontmatter to use quotes. But that is not a concern for this change.

## 6. Edge Case Analysis

| Scenario | Hand-rolled parser | `yaml.safe_load` | Regression? |
|---|---|---|---|
| No frontmatter | Returns `None` | Returns `None` | No |
| Empty frontmatter (`---\n---`) | Returns `{}` | Returns `None` (explicit check) | **Yes -- stricter** (good) |
| Malformed YAML (bad indent) | Silently produces wrong keys | Returns `None` (YAMLError caught) | **Yes -- stricter** (good) |
| YAML with nested objects | Flat key:value only, ignores nesting | Returns nested dict, stringified | Changed but no check uses nesting |
| YAML with list values | Value is `[item1, item2]` as string | `str(['item1', 'item2'])` | Changed format but no check currently uses list fields |
| Multi-line string values | Drops continuation lines | Correctly parsed | **Better** |
| Colon in value (`"1:1"`) | Includes quote chars | Correctly strips quotes | **FIXED -- this is the bug** |
| Value with trailing comment `# ...` | Includes comment as value | Comment stripped by YAML parser | **Better** |
| Duplicate keys | Last value wins (dict) | Last value wins (YAML spec) | Same |
| Tab indentation | Works (line.strip()) | YAMLError in strict mode | Possible regression for malformed input |

## 7. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| `yes`/`no` boolean change | MEDIUM | LOW | Update 1 test; behavior is actually more correct |
| `datetime` auto-parsing | LOW | NONE | No semantic check reads `generated` |
| Tab-indented frontmatter rejected | LOW | LOW | LLMs don't emit tab-indented YAML frontmatter |
| Nested YAML structures | LOW | NONE | No semantic check expects nested values |
| Performance regression (yaml import) | NEGLIGIBLE | NONE | `yaml` already imported elsewhere; parsing is ~microseconds |
| Breaking existing tests | MEDIUM | LOW | 1 test needs update (`test_malformed_yes_fails`) |

**Overall risk: LOW. Reward: HIGH.**

The fix eliminates an entire class of quoting bugs across all 22 semantic checks, not just `interleave_ratio`. Any future frontmatter field with a colon, bracket, or other YAML-special character in its value would also be correctly handled.

## 8. Test Plan

### 8.1 New Tests for `_parse_frontmatter` Directly

```python
class TestParseFrontmatterYaml:
    """Tests for yaml.safe_load-based _parse_frontmatter."""

    def test_quoted_colon_value_stripped(self):
        """The original bug: quoted '1:1' must not retain quote chars."""
        content = '---\ninterleave_ratio: "1:1"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm is not None
        assert fm["interleave_ratio"] == "1:1"  # NOT '"1:1"'

    def test_unquoted_colon_value(self):
        """Unquoted colon value (YAML sexagesimal) parsed correctly."""
        content = "---\ninterleave_ratio: 1:1\n---\n"
        fm = _parse_frontmatter(content)
        assert fm is not None
        # yaml.safe_load parses 1:1 as string "1:1" (not sexagesimal in safe mode)
        assert fm["interleave_ratio"] == "1:1"

    def test_integer_value_stringified(self):
        content = "---\nhigh_severity_count: 0\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["high_severity_count"] == "0"

    def test_float_value_stringified(self):
        content = "---\nconvergence_score: 0.85\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["convergence_score"] == "0.85"

    def test_boolean_true_stringified(self):
        content = "---\ncertified: true\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["certified"] == "True"  # str(True)

    def test_boolean_false_stringified(self):
        content = "---\ncertified: false\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["certified"] == "False"  # str(False)

    def test_empty_value_becomes_empty_string(self):
        content = "---\ntitle:\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["title"] == ""

    def test_no_frontmatter_returns_none(self):
        assert _parse_frontmatter("No frontmatter here.") is None

    def test_empty_frontmatter_returns_none(self):
        assert _parse_frontmatter("---\n---\n") is None

    def test_malformed_yaml_returns_none(self):
        content = "---\n  bad:\n    - [unclosed\n---\n"
        assert _parse_frontmatter(content) is None

    def test_yaml_yes_parsed_as_bool_true(self):
        """YAML 1.1 'yes' is boolean True; stringified to 'True'."""
        content = "---\ncertified: yes\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["certified"] == "True"

    def test_quoted_string_preserved(self):
        """Double-quoted strings have quotes stripped by YAML parser."""
        content = '---\nspec_source: "my-spec.md"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm["spec_source"] == "my-spec.md"

    def test_single_quoted_string_preserved(self):
        content = "---\nspec_source: 'my-spec.md'\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["spec_source"] == "my-spec.md"
```

### 8.2 Regression Test for the Original Bug

```python
class TestInterleaveRatioQuotedValues:
    """Regression tests for the quoted-value bug (RC-1)."""

    def test_quoted_high_1_1_passes(self):
        """The exact failure case from production."""
        content = '---\ncomplexity_class: HIGH\ninterleave_ratio: "1:1"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_quoted_medium_1_2_passes(self):
        content = '---\ncomplexity_class: MEDIUM\ninterleave_ratio: "1:2"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_quoted_low_1_3_passes(self):
        content = '---\ncomplexity_class: LOW\ninterleave_ratio: "1:3"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_single_quoted_high_1_1_passes(self):
        content = "---\ncomplexity_class: HIGH\ninterleave_ratio: '1:1'\n---\n"
        assert _interleave_ratio_consistent(content) is True
```

### 8.3 Integration Test with Full Gate

```python
class TestTestStrategyGateQuotedValues:
    """Integration test: full gate pass with quoted frontmatter values."""

    def test_gate_passes_with_quoted_ratio(self, tmp_path):
        from superclaude.cli.pipeline.gates import gate_passed

        content = (
            "---\n"
            "spec_source: test-spec.md\n"
            'generated: "2026-03-18T00:00:00Z"\n'
            "generator: superclaude-roadmap-executor\n"
            "complexity_class: HIGH\n"
            "validation_philosophy: continuous-parallel\n"
            "validation_milestones: 3\n"
            "work_milestones: 6\n"
            'interleave_ratio: "1:1"\n'
            "major_issue_policy: stop-and-fix\n"
            "---\n"
        ) + "\n".join([f"- test strategy line {i}" for i in range(45)])
        doc = tmp_path / "test-strategy.md"
        doc.write_text(content, encoding="utf-8")
        passed, reason = gate_passed(doc, TEST_STRATEGY_GATE)
        assert passed is True, f"Expected pass, got reason: {reason}"
```

### 8.4 Updated Test

```python
# CHANGE: test_malformed_yes_fails -> test_yaml_yes_accepted
def test_yaml_yes_accepted(self):
    """YAML 1.1 'yes' is boolean True; certified check accepts it."""
    assert _certified_is_true("---\ncertified: yes\n---\n") is True
```

## 9. Files Changed

| File | Change |
|---|---|
| `src/superclaude/cli/roadmap/gates.py` | Replace `_parse_frontmatter`, refactor `_frontmatter_values_non_empty`, refactor `_convergence_score_valid` |
| `tests/roadmap/test_gates_data.py` | Add `TestParseFrontmatterYaml`, `TestInterleaveRatioQuotedValues`, `TestTestStrategyGateQuotedValues`; update `test_malformed_yes_fails` |

No other files affected. The `pipeline/gates.py:_check_frontmatter` function (which checks field PRESENCE) is separate and does not need changes -- it uses its own regex-based extraction.

## 10. Implementation Sequence

1. Add `import yaml` to `roadmap/gates.py` (module-level, not inline)
2. Replace `_parse_frontmatter` body with `yaml.safe_load` version
3. Refactor `_frontmatter_values_non_empty` to use `_parse_frontmatter`
4. Refactor `_convergence_score_valid` to use `_parse_frontmatter`
5. Update `test_malformed_yes_fails` to `test_yaml_yes_accepted`
6. Add new test classes
7. Run full test suite: `uv run pytest tests/roadmap/test_gates_data.py -v`
8. Run broader suite: `uv run pytest -v`

## 11. Alternative Approaches Considered and Rejected

### A. Strip Quotes Only (Minimal Fix)

```python
result[key.strip()] = value.strip().strip("'\"")
```

**Pro:** One-line change. **Con:** Does not fix other YAML edge cases (comments, multi-line, booleans). Band-aid that will need revisiting. Does not handle nested quoting like `"it's"`. Does not handle `value: "quoted: colon"` where the colon is inside quotes.

### B. Full YAML Library for All Frontmatter Parsing (Including pipeline/gates.py)

Replace both `roadmap/gates.py:_parse_frontmatter` AND `pipeline/gates.py:_check_frontmatter`. **Con:** Larger change surface, higher risk. The pipeline gate only checks field presence, not values -- the regex approach is fine for that use case.

### C. Use `yaml.safe_load` But Do NOT Stringify Values

Let semantic checks handle native Python types directly. **Con:** Requires rewriting all 22 semantic check functions. `int(True)` == 1, `float(True)` == 1.0 -- type confusion hazards. Much larger change with many regression risks.

## 12. Conclusion

Replacing `_parse_frontmatter` with `yaml.safe_load` plus a stringification layer is the correct fix. It:

- Eliminates the immediate bug (quoted `"1:1"`)
- Prevents the entire class of quoting-related failures
- Uses an already-declared dependency (PyYAML 6.0)
- Preserves backward compatibility via `str()` coercion
- Requires updating exactly 1 existing test (`yes` boolean)
- Has LOW risk and HIGH reward
- Consolidates 3 separate inline parsers into 1 shared function

The stringification layer is key: it lets us swap the parser without rewriting every semantic check function. Checks that call `int(value)` or `float(value)` or `value.lower()` all continue to work because they receive strings, just as before -- but now correctly unquoted strings.
