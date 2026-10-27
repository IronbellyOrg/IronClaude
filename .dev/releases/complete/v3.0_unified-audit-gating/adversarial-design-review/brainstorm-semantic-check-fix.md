# Brainstorm: Semantic Check Quote-Tolerance Fix

## Problem Statement

The hand-rolled YAML frontmatter parser (`_parse_frontmatter` in `gates.py:131-151`) does not strip quote characters from parsed values. When the LLM generates `interleave_ratio: "1:1"`, the parser returns the string `"1:1"` (with literal `"` characters). The semantic check `_interleave_ratio_consistent` then compares `"1:1"` against expected `1:1` and fails.

This is not limited to `_interleave_ratio_consistent`. Every semantic check that reads string values from `_parse_frontmatter` is vulnerable. The LLM may quote any value at any time -- YAML permits it, and LLMs are non-deterministic about quoting.

## Approach: Fix at the Parser Layer, Not the Semantic Checks

### Recommended: Single-point fix in `_parse_frontmatter`

**Core argument**: The parser is the single chokepoint. Every semantic check calls `_parse_frontmatter`. Fixing the parser once eliminates the bug for all current and future semantic checks. Fixing each semantic check individually creates N fix-points, each of which must be maintained and tested.

**The fix** -- add quote stripping to `_parse_frontmatter`:

```python
def _strip_yaml_quotes(value: str) -> str:
    """Strip matching YAML quote characters from a parsed value.

    Handles: "value", 'value', and unquoted value.
    Does NOT strip mismatched quotes (e.g., "value' is returned as-is).
    """
    if len(value) >= 2:
        if (value[0] == '"' and value[-1] == '"') or \
           (value[0] == "'" and value[-1] == "'"):
            return value[1:-1]
    return value
```

Applied in `_parse_frontmatter`:

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
            result[key.strip()] = _strip_yaml_quotes(value.strip())  # FIX HERE
    return result
```

### Why NOT fix at the semantic check layer

The brainstorm prompt asks about fixing semantic checks to be quote-tolerant. Here is the honest analysis of that approach:

**Option A: Per-check stripping** -- each semantic check strips quotes from values before comparison.

- **Pro**: Zero risk to other code paths; each fix is locally verifiable.
- **Con**: 13+ semantic checks read from `_parse_frontmatter`. Every one needs the fix. Future checks will forget it. The bug is in the parser, not the checks -- the checks are correct as written; they receive wrong data.
- **Con**: `_frontmatter_values_non_empty` directly parses frontmatter inline (lines 102-120) without using `_parse_frontmatter` at all, creating a second code path that also needs fixing.
- **Con**: Violates DRY. The quoting problem is a data-cleaning concern, not a business-logic concern.

**Option B: Shared `_normalize_fm_value()` helper** -- a utility function called by each semantic check.

- **Pro**: Better than Option A; avoids repeating the stripping logic.
- **Con**: Still requires every semantic check to remember to call it. New checks can forget.
- **Con**: The helper does the same thing as fixing the parser, but at the wrong abstraction layer.

**Option C: Fix the parser (recommended)** -- strip quotes in `_parse_frontmatter`.

- **Pro**: Single fix point. All 13+ semantic checks are fixed automatically.
- **Pro**: Future semantic checks are automatically quote-tolerant.
- **Pro**: `_convergence_score_valid` (lines 279-300) parses frontmatter inline and would also need fixing -- but fixing `_parse_frontmatter` plus refactoring `_convergence_score_valid` to use it covers both paths.
- **Pro**: Aligns with YAML semantics -- `"1:1"` and `1:1` are the same value in YAML.
- **Con**: Marginally higher blast radius (all callers affected), but the change is strictly narrowing (removing extraneous characters).

## Detailed Code Changes

### Change 1: Add `_strip_yaml_quotes` helper

Insert after line 130 (before `_parse_frontmatter`):

```python
def _strip_yaml_quotes(value: str) -> str:
    """Strip matching YAML quote characters from a parsed value.

    Handles double quotes ("value") and single quotes ('value').
    Mismatched quotes are preserved (e.g., "value' -> "value').
    Empty quoted strings ("" or '') return empty string.
    """
    if len(value) >= 2:
        if (value[0] == '"' and value[-1] == '"') or \
           (value[0] == "'" and value[-1] == "'"):
            return value[1:-1]
    return value
```

### Change 2: Apply in `_parse_frontmatter`

Line 150, change:
```python
result[key.strip()] = value.strip()
```
to:
```python
result[key.strip()] = _strip_yaml_quotes(value.strip())
```

### Change 3: Refactor `_convergence_score_valid` to use `_parse_frontmatter`

This function (lines 279-300) duplicates the frontmatter parsing inline. Refactor it to use `_parse_frontmatter` so it also benefits from quote stripping:

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
    except ValueError:
        return False
```

### Change 4: Refactor `_frontmatter_values_non_empty` to use `_parse_frontmatter`

This function (lines 102-120) also duplicates frontmatter parsing inline. Refactor:

```python
def _frontmatter_values_non_empty(content: str) -> bool:
    """All YAML frontmatter fields have non-empty values."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    for _key, value in fm.items():
        if not value:
            return False
    return True
```

**Note**: This changes behavior slightly -- `_parse_frontmatter` returns `None` when there is no frontmatter, but the original returns `False`. Both are equivalent. After quote stripping, a value of `""` (empty quoted string) would correctly be treated as empty since `_strip_yaml_quotes('""')` returns `""` which is empty-string, and `not ""` is `True` -> returns `False`. This is correct behavior.

## Edge Cases

| Input | `_strip_yaml_quotes` output | Notes |
|---|---|---|
| `1:1` | `1:1` | Unquoted, no change |
| `"1:1"` | `1:1` | Double-quoted, stripped |
| `'1:1'` | `1:1` | Single-quoted, stripped |
| `"1:1'` | `"1:1'` | Mismatched, preserved |
| `""` | (empty string) | Empty double-quoted |
| `''` | (empty string) | Empty single-quoted |
| `"` | `"` | Single char, no strip |
| `continuous-parallel` | `continuous-parallel` | Unquoted, no change |
| `"continuous-parallel"` | `continuous-parallel` | Quoted, stripped |
| `"true"` | `true` | Boolean-like, stripped correctly |
| `"0"` | `0` | Numeric-like, stripped; `int("0")` still works |
| `"DEV-001 DEV-002"` | `DEV-001 DEV-002` | Multi-value, stripped correctly |
| `"stop-and-fix"` | `stop-and-fix` | Hyphenated, stripped correctly |

### Important: `int()` and `float()` tolerance

Python's `int("0")` and `float("0.85")` already work on unquoted strings. After stripping, `int(_strip_yaml_quotes('"0"'))` becomes `int("0")` = `0`. No breakage.

### Important: Boolean comparisons

`_certified_is_true` compares `value.lower() == "true"`. If the LLM writes `certified: "true"`, after stripping we get `true`, and the comparison works. Without stripping, `"true".lower()` = `"true"` != `true`. This is a latent bug in `_certified_is_true` that this fix also resolves.

## Affected Semantic Checks (all benefit from parser fix)

| Check function | Value compared | Vulnerable to quoting? |
|---|---|---|
| `_interleave_ratio_consistent` | `ratio.strip() == expected_ratio` | YES -- reported bug |
| `_validation_philosophy_correct` | `value.strip() == "continuous-parallel"` | YES -- latent |
| `_major_issue_policy_correct` | `value.strip() == "stop-and-fix"` | YES -- latent |
| `_certified_is_true` | `value.lower() == "true"` | YES -- latent |
| `_validation_complete_true` | `value.lower() == "true"` | YES -- latent |
| `_complexity_class_valid` | `value.strip().upper() in (...)` | YES -- latent |
| `_extraction_mode_valid` | `normalized.startswith("chunked")` | YES -- latent |
| `_high_severity_count_zero` | `int(value)` | YES -- `int('"0"')` raises ValueError |
| `_no_ambiguous_deviations` | `int(value)` | YES -- same |
| `_milestone_counts_positive` | `int(value)` | YES -- same |
| `_tasklist_ready_consistent` | `value.lower() == "true"` + `int(...)` | YES -- both |
| `_convergence_score_valid` | `float(value)` | YES -- `float('"0.85"')` raises ValueError |
| `_slip_count_matches_routing` | `int(slip_str)` | YES -- same |
| `_total_analyzed_consistent` | `int(raw)` | YES -- same |
| `_total_annotated_consistent` | `int(total_str)` | YES -- same |

**15 out of 15** semantic checks that use frontmatter values are vulnerable. Fixing each individually would require 15 changes. Fixing the parser requires 1.

## Test Plan

### Unit tests for `_strip_yaml_quotes`

```python
class TestStripYamlQuotes:
    def test_unquoted_unchanged(self):
        assert _strip_yaml_quotes("1:1") == "1:1"

    def test_double_quoted_stripped(self):
        assert _strip_yaml_quotes('"1:1"') == "1:1"

    def test_single_quoted_stripped(self):
        assert _strip_yaml_quotes("'1:1'") == "1:1"

    def test_mismatched_preserved(self):
        assert _strip_yaml_quotes("\"1:1'") == "\"1:1'"

    def test_empty_double_quoted(self):
        assert _strip_yaml_quotes('""') == ""

    def test_empty_single_quoted(self):
        assert _strip_yaml_quotes("''") == ""

    def test_single_char_preserved(self):
        assert _strip_yaml_quotes('"') == '"'

    def test_empty_string_unchanged(self):
        assert _strip_yaml_quotes("") == ""

    def test_boolean_true_quoted(self):
        assert _strip_yaml_quotes('"true"') == "true"

    def test_numeric_quoted(self):
        assert _strip_yaml_quotes('"0"') == "0"

    def test_hyphenated_quoted(self):
        assert _strip_yaml_quotes('"stop-and-fix"') == "stop-and-fix"
```

### Regression tests for `_parse_frontmatter` with quoted values

```python
class TestParseFrontmatterQuoteTolerance:
    def test_unquoted_value(self):
        fm = _parse_frontmatter("---\nkey: value\n---\n")
        assert fm["key"] == "value"

    def test_double_quoted_value(self):
        fm = _parse_frontmatter('---\nkey: "value"\n---\n')
        assert fm["key"] == "value"

    def test_single_quoted_value(self):
        fm = _parse_frontmatter("---\nkey: 'value'\n---\n")
        assert fm["key"] == "value"

    def test_colon_value_quoted(self):
        fm = _parse_frontmatter('---\nratio: "1:1"\n---\n')
        assert fm["ratio"] == "1:1"

    def test_colon_value_unquoted(self):
        fm = _parse_frontmatter("---\nratio: 1:1\n---\n")
        assert fm["ratio"] == "1:1"
```

### Integration tests: quoted frontmatter passes semantic checks

```python
class TestInterleaveRatioQuoteTolerance:
    def test_high_quoted_ratio_passes(self):
        content = '---\ncomplexity_class: HIGH\ninterleave_ratio: "1:1"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_low_quoted_ratio_passes(self):
        content = '---\ncomplexity_class: LOW\ninterleave_ratio: "1:3"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_quoted_complexity_and_ratio_passes(self):
        content = '---\ncomplexity_class: "HIGH"\ninterleave_ratio: "1:1"\n---\n'
        assert _interleave_ratio_consistent(content) is True

class TestValidationPhilosophyQuoteTolerance:
    def test_quoted_value_passes(self):
        content = '---\nvalidation_philosophy: "continuous-parallel"\n---\n'
        assert _validation_philosophy_correct(content) is True

class TestMajorIssuePolicyQuoteTolerance:
    def test_quoted_value_passes(self):
        content = '---\nmajor_issue_policy: "stop-and-fix"\n---\n'
        assert _major_issue_policy_correct(content) is True

class TestHighSeverityCountQuoteTolerance:
    def test_quoted_zero_passes(self):
        content = '---\nhigh_severity_count: "0"\n---\n'
        assert _high_severity_count_zero(content) is True

class TestConvergenceScoreQuoteTolerance:
    def test_quoted_float_passes(self):
        content = '---\nconvergence_score: "0.85"\n---\n'
        assert _convergence_score_valid(content) is True

class TestCertifiedIsTrueQuoteTolerance:
    def test_quoted_true_passes(self):
        content = '---\ncertified: "true"\n---\n'
        assert _certified_is_true(content) is True
```

### Full gate integration test (the original failing scenario)

```python
class TestTestStrategyGateQuoteTolerance:
    def test_gate_passes_with_quoted_ratio(self, tmp_path):
        from superclaude.cli.pipeline.gates import gate_passed

        content = (
            "---\n"
            "spec_source: test-spec.md\n"
            "generated: 2026-03-18T00:00:00Z\n"
            "generator: superclaude-roadmap-executor\n"
            'complexity_class: HIGH\n'
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

## Tradeoff Summary

| Criterion | Parser fix (recommended) | Per-check fix | Shared helper |
|---|---|---|---|
| Fix points | 1 | 15+ | 15+ (calls) + 1 (helper) |
| Future-proof | Yes (automatic) | No (must remember) | No (must remember) |
| Blast radius | All `_parse_frontmatter` callers | Per-check only | Per-check only |
| Risk | Low (strictly narrowing) | Very low | Low |
| DRY | Yes | No | Partial |
| Correct abstraction | Yes (data cleaning at data layer) | No (cleaning in business logic) | Partial |
| Lines changed | ~10 + refactor 2 inline parsers | ~30 across 15 functions | ~20 + 15 call sites |

## Recommendation

Fix the parser. Add `_strip_yaml_quotes`. Apply it in `_parse_frontmatter`. Refactor the two inline-parsing functions (`_convergence_score_valid`, `_frontmatter_values_non_empty`) to use `_parse_frontmatter`. Write the test suite above. This is the minimal-touch, maximum-coverage fix.

## Files to Modify

- `src/superclaude/cli/roadmap/gates.py` -- add `_strip_yaml_quotes`, modify `_parse_frontmatter`, refactor `_convergence_score_valid` and `_frontmatter_values_non_empty`
- `tests/roadmap/test_gates_data.py` -- add quote-tolerance test classes
