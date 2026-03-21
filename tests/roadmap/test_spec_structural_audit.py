"""Unit tests for spec_structural_audit.py.

Tests cover:
1. All 7 structural indicator counters (FR-MOD4.1)
2. Ratio comparison against total_requirements (FR-MOD4.2)
3. Warning-only behavior (FR-MOD4.3)
4. SC-005 regression: flags extraction inadequacy when ratio < 0.5

All tests use real content fixtures, no mocks.
"""

from superclaude.cli.roadmap.spec_structural_audit import (
    SpecStructuralAudit,
    audit_spec_structure,
    check_extraction_adequacy,
)


# --- Real content fixtures ---

RICH_SPEC = """\
# Executor Design Specification

The executor MUST support three-way dispatch. It SHALL handle errors
gracefully. All runners are REQUIRED to implement the base protocol.

```python
def _run_programmatic_step(step_id, config):
    if step_id in PROGRAMMATIC_RUNNERS:
        runner = PROGRAMMATIC_RUNNERS[step_id]
        return runner(config)
    raise ValueError(f"Unknown step: {step_id}")

def _run_claude_step(step_id, prompt):
    pass

class StepExecutor:
    pass

class RunnerRegistry:
    pass
```

Tests:
- `test_programmatic_step_routing`
- `test_claude_step_fallback`
- `test_executor_error_handling`

```python
PROGRAMMATIC_RUNNERS = {
    "validate_config": _run_validate_config,
    "parse_spec": _run_parse_spec,
}

HANDLER_MAP = {
    "default": DefaultHandler,
}
```
"""

MINIMAL_SPEC = """\
# Simple Feature

Add a button to the UI.
"""

PSEUDOCODE_SPEC = """\
Algorithm:

```
if condition:
    do_something()
elif other:
    do_other()
else:
    fallback()

for item in items:
    process(item)
```
"""

MIXED_SPEC = """\
# Feature Spec

The system MUST validate all inputs. It SHALL reject invalid data.

```python
def validate_input(data):
    pass

class InputValidator:
    pass
```

Run `test_validation` to verify.

```python
CONFIG_MAP = {
    "key": "value",
}
```
"""

REPEATED_TEST_NAMES_SPEC = """\
# Feature with Repeated Test References

The system MUST handle repeated test references correctly.

## Acceptance Criteria
- Run `test_foo` to verify input handling
- Run `test_bar` to verify output handling

## Dependencies
- Requires `test_foo` passing before integration
- Requires `test_bar` passing before deployment

## Exit Criteria
- `test_foo` passes in CI

```python
def setup_fixture():
    pass
```
"""


class TestStructuralIndicatorCounters:
    """FR-MOD4.1: All 7 structural indicator counters."""

    def test_code_block_count(self):
        audit = audit_spec_structure(RICH_SPEC)
        assert audit.code_block_count == 2

    def test_must_shall_count(self):
        audit = audit_spec_structure(RICH_SPEC)
        # MUST, SHALL, REQUIRED
        assert audit.must_shall_count == 3

    def test_function_signature_count(self):
        audit = audit_spec_structure(RICH_SPEC)
        # _run_programmatic_step, _run_claude_step in first block
        assert audit.function_signature_count >= 2

    def test_class_definition_count(self):
        audit = audit_spec_structure(RICH_SPEC)
        # StepExecutor, RunnerRegistry
        assert audit.class_definition_count >= 2

    def test_test_name_count(self):
        audit = audit_spec_structure(RICH_SPEC)
        # test_programmatic_step_routing, test_claude_step_fallback,
        # test_executor_error_handling
        assert audit.test_name_count >= 3

    def test_registry_pattern_count(self):
        audit = audit_spec_structure(RICH_SPEC)
        # PROGRAMMATIC_RUNNERS = {, HANDLER_MAP = {
        assert audit.registry_pattern_count >= 2

    def test_pseudocode_blocks(self):
        audit = audit_spec_structure(PSEUDOCODE_SPEC)
        assert audit.pseudocode_blocks >= 1

    def test_total_is_sum_of_all(self):
        audit = audit_spec_structure(RICH_SPEC)
        expected_total = (
            audit.code_block_count
            + audit.must_shall_count
            + audit.function_signature_count
            + audit.class_definition_count
            + audit.test_name_count
            + audit.registry_pattern_count
            + audit.pseudocode_blocks
        )
        assert audit.total_structural_indicators == expected_total

    def test_minimal_spec_low_indicators(self):
        audit = audit_spec_structure(MINIMAL_SPEC)
        assert audit.total_structural_indicators == 0

    def test_mixed_spec_moderate_indicators(self):
        audit = audit_spec_structure(MIXED_SPEC)
        assert audit.code_block_count == 2
        assert audit.must_shall_count == 2
        assert audit.function_signature_count >= 1
        assert audit.class_definition_count >= 1


class TestRatioComparison:
    """FR-MOD4.2: Ratio comparison against total_requirements."""

    def test_adequate_extraction_passes(self):
        audit = audit_spec_structure(RICH_SPEC)
        total_indicators = audit.total_structural_indicators
        # Extraction reports a reasonable number of requirements
        passed, result = check_extraction_adequacy(
            RICH_SPEC, int(total_indicators * 0.6)
        )
        assert passed

    def test_inadequate_extraction_fails(self):
        audit = audit_spec_structure(RICH_SPEC)
        # Extraction reports very few requirements relative to indicators
        passed, result = check_extraction_adequacy(RICH_SPEC, 2)
        assert not passed

    def test_threshold_boundary_pass(self):
        audit = audit_spec_structure(RICH_SPEC)
        total = audit.total_structural_indicators
        # At threshold (0.5) — use ceiling to ensure ratio >= 0.5
        req_count = -(-total // 2)  # ceiling division of total/2
        passed, _ = check_extraction_adequacy(RICH_SPEC, req_count)
        assert passed

    def test_threshold_boundary_fail(self):
        audit = audit_spec_structure(RICH_SPEC)
        total = audit.total_structural_indicators
        # Just below threshold
        req_count = int(total * 0.5) - 1
        if total > 0 and req_count >= 0:
            passed, _ = check_extraction_adequacy(RICH_SPEC, req_count)
            assert not passed

    def test_zero_indicators_passes(self):
        passed, audit = check_extraction_adequacy(MINIMAL_SPEC, 0)
        assert passed
        assert audit.total_structural_indicators == 0

    def test_custom_threshold(self):
        passed, _ = check_extraction_adequacy(RICH_SPEC, 1, threshold=0.01)
        assert passed


class TestWarningOnlyBehavior:
    """FR-MOD4.3: Warning-only enforcement."""

    def test_never_raises_exception(self):
        # check_extraction_adequacy should never raise, even with bad inputs
        passed, audit = check_extraction_adequacy(RICH_SPEC, 0)
        assert not passed  # Returns False, but does NOT raise

    def test_returns_result_object(self):
        passed, audit = check_extraction_adequacy(RICH_SPEC, 0)
        assert isinstance(passed, bool)
        assert isinstance(audit, SpecStructuralAudit)

    def test_empty_spec_no_exception(self):
        passed, audit = check_extraction_adequacy("", 0)
        assert passed  # No indicators = passes

    def test_large_requirement_count_no_exception(self):
        passed, audit = check_extraction_adequacy(RICH_SPEC, 10000)
        assert passed  # High ratio = passes


class TestSC005Regression:
    """SC-005: Flags extraction inadequacy when ratio < 0.5."""

    def test_flags_low_extraction(self):
        audit = audit_spec_structure(RICH_SPEC)
        total = audit.total_structural_indicators
        assert total > 10  # Rich spec should have many indicators

        # Extraction reports only 2 requirements for a rich spec
        passed, result = check_extraction_adequacy(RICH_SPEC, 2)
        assert not passed
        assert result.total_structural_indicators == total

    def test_passes_adequate_extraction(self):
        audit = audit_spec_structure(RICH_SPEC)
        total = audit.total_structural_indicators
        # Report a reasonable fraction
        passed, _ = check_extraction_adequacy(RICH_SPEC, int(total * 0.7))
        assert passed


class TestSpecStructuralAuditDataclass:
    """Test SpecStructuralAudit dataclass fields."""

    def test_all_fields_present(self):
        audit = audit_spec_structure(RICH_SPEC)
        assert hasattr(audit, "code_block_count")
        assert hasattr(audit, "must_shall_count")
        assert hasattr(audit, "function_signature_count")
        assert hasattr(audit, "class_definition_count")
        assert hasattr(audit, "test_name_count")
        assert hasattr(audit, "registry_pattern_count")
        assert hasattr(audit, "pseudocode_blocks")
        assert hasattr(audit, "total_structural_indicators")

    def test_all_counts_non_negative(self):
        audit = audit_spec_structure(RICH_SPEC)
        assert audit.code_block_count >= 0
        assert audit.must_shall_count >= 0
        assert audit.function_signature_count >= 0
        assert audit.class_definition_count >= 0
        assert audit.test_name_count >= 0
        assert audit.registry_pattern_count >= 0
        assert audit.pseudocode_blocks >= 0
        assert audit.total_structural_indicators >= 0


class TestDeduplication:
    """Verify test_name_count deduplicates repeated test name references."""

    def test_repeated_test_names_counted_uniquely(self):
        audit = audit_spec_structure(REPEATED_TEST_NAMES_SPEC)
        # test_foo appears 3x, test_bar appears 2x — but only 2 unique names
        assert audit.test_name_count == 2

    def test_total_indicators_not_inflated_by_repeats(self):
        audit = audit_spec_structure(REPEATED_TEST_NAMES_SPEC)
        expected_total = (
            audit.code_block_count
            + audit.must_shall_count
            + audit.function_signature_count
            + audit.class_definition_count
            + audit.test_name_count
            + audit.registry_pattern_count
            + audit.pseudocode_blocks
        )
        assert audit.total_structural_indicators == expected_total
