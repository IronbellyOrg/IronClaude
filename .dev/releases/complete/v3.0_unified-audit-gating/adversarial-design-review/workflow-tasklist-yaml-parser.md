# Workflow Tasklist: Replace `_parse_frontmatter` with `yaml.safe_load`
<!-- compliance: strict -->
<!-- spec: adversarial-design-review/brainstorm-yaml-safe-load.md -->
<!-- executor: sc:task-unified --compliance strict -->

## Metadata
- **Generated**: 2026-03-18
- **Source spec**: `brainstorm-yaml-safe-load.md`
- **Target file**: `src/superclaude/cli/roadmap/gates.py`
- **Test file**: `tests/roadmap/test_gates_data.py`
- **Total tasks**: 9
- **Phases**: 4 (Code → Test → Verify → Sync)
- **Dependencies**: Sequential within phases; Phase N depends on Phase N-1

---

## Phase 1: Code Changes (3 tasks)

### Task 1.1: Replace `_parse_frontmatter` with `yaml.safe_load`
- **Compliance**: STRICT
- **File**: `src/superclaude/cli/roadmap/gates.py`
- **Lines**: 131-151
- **Action**: Replace the hand-rolled parser body with `yaml.safe_load` + stringification layer
- **Key changes**:
  1. Add `import yaml` at the top of the function (inline import, matching codebase style at line 125)
  2. Keep the existing frontmatter extraction logic (find text between `---` delimiters)
  3. Pass extracted text to `yaml.safe_load()`
  4. Catch `yaml.YAMLError` → return `None`
  5. Validate result is `dict` → if not, return `None`
  6. Stringify all values: `str(value) if value is not None else ""`
  7. Handle empty frontmatter (`---\n---`) → return `None`
- **Replacement code**:
  ```python
  def _parse_frontmatter(content: str) -> dict[str, str] | None:
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

      result: dict[str, str] = {}
      for key, value in parsed.items():
          result[str(key)] = str(value) if value is not None else ""
      return result
  ```
- **Acceptance criteria**:
  - [ ] `_parse_frontmatter('---\ninterleave_ratio: "1:1"\n---\n')` returns `{"interleave_ratio": "1:1"}` (no quote chars)
  - [ ] `_parse_frontmatter('---\nhigh_severity_count: 0\n---\n')` returns `{"high_severity_count": "0"}` (stringified int)
  - [ ] `_parse_frontmatter('---\ncertified: true\n---\n')` returns `{"certified": "True"}` (stringified bool)
  - [ ] `_parse_frontmatter('---\ntitle:\n---\n')` returns `{"title": ""}` (None → empty string)
  - [ ] `_parse_frontmatter('---\n---\n')` returns `None` (empty frontmatter)
  - [ ] `_parse_frontmatter('No frontmatter')` returns `None`
  - [ ] Malformed YAML returns `None` (no exception raised)
- **Depends on**: None
- **Rollback**: Revert to hand-rolled parser + add `_strip_yaml_quotes` (Variant A fallback)

---

### Task 1.2: Refactor `_frontmatter_values_non_empty` to use `_parse_frontmatter`
- **Compliance**: STRICT
- **File**: `src/superclaude/cli/roadmap/gates.py`
- **Lines**: 102-120
- **Action**: Replace inline frontmatter parsing with delegation to `_parse_frontmatter`
- **Replacement code**:
  ```python
  def _frontmatter_values_non_empty(content: str) -> bool:
      """All YAML frontmatter fields have non-empty values."""
      fm = _parse_frontmatter(content)
      if fm is None:
          return False
      for _key, value in fm.items():
          if not value.strip():
              return False
      return True
  ```
- **Acceptance criteria**:
  - [ ] `_frontmatter_values_non_empty('---\ntitle: test\n---\n')` returns `True`
  - [ ] `_frontmatter_values_non_empty('---\ntitle:\n---\n')` returns `False` (empty value)
  - [ ] `_frontmatter_values_non_empty('---\ntitle: ""\n---\n')` returns `False` (empty quoted string → empty after YAML parse)
  - [ ] No frontmatter → `False`
- **Depends on**: Task 1.1

---

### Task 1.3: Refactor `_convergence_score_valid` to use `_parse_frontmatter`
- **Compliance**: STRICT
- **File**: `src/superclaude/cli/roadmap/gates.py`
- **Lines**: 279-300
- **Action**: Replace inline frontmatter parsing with delegation to `_parse_frontmatter`
- **Replacement code**:
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
- **Acceptance criteria**:
  - [ ] `_convergence_score_valid('---\nconvergence_score: 0.85\n---\n')` returns `True`
  - [ ] `_convergence_score_valid('---\nconvergence_score: "0.85"\n---\n')` returns `True` (quoted float)
  - [ ] `_convergence_score_valid('---\nconvergence_score: 1.5\n---\n')` returns `False` (out of range)
  - [ ] No frontmatter → `False`
- **Depends on**: Task 1.1

---

## Phase 2: Test Implementation (3 tasks)

### Task 2.1: Add `_parse_frontmatter` YAML parsing tests
- **Compliance**: STRICT
- **File**: `tests/roadmap/test_gates_data.py`
- **Action**: Add `TestParseFrontmatterYaml` class with 14 tests
- **Tests**:
  1. `test_quoted_colon_value_stripped` — `"1:1"` → `1:1` (THE BUG)
  2. `test_unquoted_colon_value` — `1:1` stays `1:1`
  3. `test_single_quoted_value` — `'1:1'` → `1:1`
  4. `test_integer_value_stringified` — `0` → `"0"`
  5. `test_float_value_stringified` — `0.85` → `"0.85"`
  6. `test_boolean_true_stringified` — `true` → `"True"`
  7. `test_boolean_false_stringified` — `false` → `"False"`
  8. `test_yaml_yes_parsed_as_bool_true` — `yes` → `"True"`
  9. `test_empty_value_becomes_empty_string` — `title:` → `""`
  10. `test_no_frontmatter_returns_none`
  11. `test_empty_frontmatter_returns_none` — `---\n---`
  12. `test_malformed_yaml_returns_none`
  13. `test_quoted_string_preserved` — `"my-spec.md"` → `my-spec.md`
  14. `test_single_quoted_string_preserved` — `'my-spec.md'` → `my-spec.md`
- **Acceptance criteria**:
  - [ ] All 14 tests pass
  - [ ] Imports `_parse_frontmatter` from `superclaude.cli.roadmap.gates`
- **Depends on**: Task 1.1

---

### Task 2.2: Add regression tests for quoted frontmatter in semantic checks
- **Compliance**: STRICT
- **File**: `tests/roadmap/test_gates_data.py`
- **Action**: Add test classes verifying quoted values pass all vulnerable semantic checks
- **Tests** (7 classes, 10 tests total):
  1. `TestInterleaveRatioQuotedValues::test_quoted_high_1_1_passes` — THE EXACT BUG
  2. `TestInterleaveRatioQuotedValues::test_quoted_medium_1_2_passes`
  3. `TestInterleaveRatioQuotedValues::test_quoted_low_1_3_passes`
  4. `TestInterleaveRatioQuotedValues::test_single_quoted_high_1_1_passes`
  5. `TestValidationPhilosophyQuoteTolerance::test_quoted_value_passes`
  6. `TestMajorIssuePolicyQuoteTolerance::test_quoted_value_passes`
  7. `TestHighSeverityCountQuoteTolerance::test_quoted_zero_passes`
  8. `TestConvergenceScoreQuoteTolerance::test_quoted_float_passes`
  9. `TestCertifiedIsTrueQuoteTolerance::test_quoted_true_passes`
  10. `TestCertifiedIsTrueQuoteTolerance::test_yaml_yes_accepted` (replaces `test_malformed_yes_fails`)
- **Acceptance criteria**:
  - [ ] All 10 tests pass
  - [ ] The `test_yaml_yes_accepted` test asserts `True` (behavioral change documented)
- **Depends on**: Tasks 1.1, 1.2, 1.3

---

### Task 2.3: Update `test_malformed_yes_fails` → `test_yaml_yes_accepted`
- **Compliance**: STRICT
- **File**: `tests/roadmap/test_gates_data.py`
- **Line**: 746-747
- **Action**: Change existing test from asserting `False` to asserting `True`, rename
- **Current code**:
  ```python
  def test_malformed_yes_fails(self):
      assert _certified_is_true("---\ncertified: yes\n---\n") is False
  ```
- **New code**:
  ```python
  def test_yaml_yes_accepted(self):
      """YAML 1.1 'yes' is boolean True; certified check accepts it."""
      assert _certified_is_true("---\ncertified: yes\n---\n") is True
  ```
- **Acceptance criteria**:
  - [ ] Test passes with new assertion
  - [ ] Old test name no longer exists
- **Depends on**: Task 1.1

---

## Phase 3: Verification (2 tasks)

### Task 3.1: Run gate data tests + executor tests
- **Compliance**: STRICT
- **Action**: Verify no regressions in gate system
- **Commands**:
  ```bash
  uv run pytest tests/roadmap/test_gates_data.py -v
  uv run pytest tests/roadmap/test_executor.py -v
  ```
- **Acceptance criteria**:
  - [ ] All existing gate data tests pass (minus the renamed `yes` test)
  - [ ] All executor tests pass (including our Solution C whitespace tests)
  - [ ] All new tests from Phase 2 pass
  - [ ] Zero failures, zero errors
- **Depends on**: All Phase 2 tasks

---

### Task 3.2: Run full test suite
- **Compliance**: STRICT
- **Action**: Full regression sweep
- **Commands**:
  ```bash
  uv run pytest tests/ -v
  ```
- **Acceptance criteria**:
  - [ ] Full suite passes (same or fewer failures than baseline of 1 pre-existing `test_credential_scanner` failure)
  - [ ] No new warnings related to YAML parsing
- **Depends on**: Task 3.1

---

## Phase 4: Sync & Commit (1 task)

### Task 4.1: Sync, verify, and commit
- **Compliance**: STRICT
- **Action**: Sync and commit both fixes (Solution C whitespace + YAML parser)
- **Steps**:
  1. `make sync-dev`
  2. `make verify-sync`
  3. Stage files:
     - `src/superclaude/cli/roadmap/gates.py`
     - `tests/roadmap/test_gates_data.py`
  4. Commit: `fix: replace hand-rolled frontmatter parser with yaml.safe_load for quote tolerance`
- **Acceptance criteria**:
  - [ ] `make verify-sync` exits 0
  - [ ] Only the 2 expected files staged
  - [ ] Commit follows conventional commits format
- **Depends on**: Tasks 3.1, 3.2

---

## Dependency Graph

```
Phase 1 (sequential):
  Task 1.1 → Task 1.2 → Task 1.3

Phase 2 (parallel where possible):
  Task 2.1 (depends: 1.1) ─┐
  Task 2.3 (depends: 1.1) ─┼─→ Task 2.2 (depends: 1.1, 1.2, 1.3)
                            │
Phase 3 (sequential):
  Task 3.1 → Task 3.2

Phase 4:
  Task 4.1 (depends: 3.1, 3.2)
```

## Rollback Plan

If `yaml.safe_load` causes unexpected behavior:
1. Revert `_parse_frontmatter` to the hand-rolled version
2. Add `_strip_yaml_quotes` helper (Variant A from brainstorm-parser-fix.md) as fallback
3. Both fixes are independently viable — Variant A requires zero behavioral changes
