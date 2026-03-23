"""Unit tests for fingerprint.py.

Tests cover:
1. Three-source extraction (backtick, def/class, ALL_CAPS) (FR-MOD3.1)
2. Deduplication by text value (FR-MOD3.2)
3. Coverage ratio computation (FR-MOD3.3)
4. Threshold boundary (0.7 pass/fail edge) (FR-MOD3.4)
5. Empty-fingerprint passthrough (FR-MOD3.4)
6. cli-portify regression case SC-004

All tests use real content fixtures, no mocks.
"""

from superclaude.cli.roadmap.fingerprint import (
    Fingerprint,
    _EXCLUDED_CONSTANTS,
    check_fingerprint_coverage,
    extract_code_fingerprints,
    fingerprint_gate_passed,
)


# --- Real content fixtures ---

SPEC_WITH_BACKTICKS = """\
The executor calls `_run_programmatic_step()` for programmatic tasks
and `_run_claude_step()` for LLM-based tasks. The `_run_convergence_step()`
handles convergence operations. Use `test_programmatic_step_routing` to verify.
"""

SPEC_WITH_CODE_BLOCKS = """\
Implementation:

```python
def _run_programmatic_step(step_id, config):
    pass

class StepExecutor:
    pass

def validate_config(path):
    pass
```
"""

SPEC_WITH_CONSTANTS = """\
The `PROGRAMMATIC_RUNNERS` dictionary maps step IDs.
The `HANDLER_REGISTRY` stores all handlers.
Use `DISPATCH_TABLE` for routing.
"""

SPEC_MIXED = """\
The executor uses `_run_programmatic_step()` for dispatch.

```python
PROGRAMMATIC_RUNNERS = {
    "validate_config": _run_validate_config,
}

def _run_validate_config(config):
    pass

class ExecutorConfig:
    pass
```

The `HANDLER_REGISTRY` provides handler lookup.
Test with `test_programmatic_step_routing`.
"""

GOOD_ROADMAP = """\
## Phase 1: Foundation
Implement `_run_programmatic_step` and `_run_claude_step`.
Set up `_run_convergence_step` for convergence.
Create `PROGRAMMATIC_RUNNERS` dispatch table.
Add `HANDLER_REGISTRY` for handler management.
Write `test_programmatic_step_routing` test.
"""

PARTIAL_ROADMAP = """\
## Phase 1: Foundation
Implement `_run_programmatic_step` for dispatch.
Set up `_run_claude_step` for LLM tasks.
"""

EMPTY_ROADMAP = """\
## Phase 1: Setup
Set up project structure.

## Phase 2: Implementation
Build the executor.
"""

CLI_PORTIFY_SPEC = """\
Three-way dispatch: `_run_programmatic_step()`, `_run_claude_step()`, `_run_convergence_step()`

The `PROGRAMMATIC_RUNNERS` dictionary maps step IDs to Python functions.

Integration test: `test_programmatic_step_routing`

```python
PROGRAMMATIC_RUNNERS = {
    "validate_config": _run_validate_config,
    "parse_spec": _run_parse_spec,
}
```
"""

CLI_PORTIFY_BAD_ROADMAP = """\
## Phase 1: Foundation
Set up project structure and configuration.

## Phase 2: Executor Shell
Implement executor: sequential execution only, `--dry-run`, `--resume`.

## Phase 3: CLI Polish
Add rich output formatting and progress display.
"""


class TestThreeSourceExtraction:
    """FR-MOD3.1: Three-source extraction."""

    def test_backtick_identifiers_extracted(self):
        fps = extract_code_fingerprints(SPEC_WITH_BACKTICKS)
        texts = {fp.text for fp in fps}
        assert "_run_programmatic_step" in texts
        assert "_run_claude_step" in texts
        assert "_run_convergence_step" in texts
        assert "test_programmatic_step_routing" in texts

    def test_backtick_category(self):
        fps = extract_code_fingerprints(SPEC_WITH_BACKTICKS)
        backtick_fps = [fp for fp in fps if fp.category == "identifier"]
        assert len(backtick_fps) >= 4

    def test_short_identifiers_excluded(self):
        content = "Use `foo` and `bar` for testing. Also `ab` and `xyz`."
        fps = extract_code_fingerprints(content)
        texts = {fp.text for fp in fps}
        # < 4 chars should be excluded
        assert "foo" not in texts
        assert "bar" not in texts
        assert "ab" not in texts
        assert "xyz" not in texts

    def test_code_block_definitions_extracted(self):
        fps = extract_code_fingerprints(SPEC_WITH_CODE_BLOCKS)
        texts = {fp.text for fp in fps}
        assert "_run_programmatic_step" in texts
        assert "StepExecutor" in texts
        assert "validate_config" in texts

    def test_code_block_category(self):
        fps = extract_code_fingerprints(SPEC_WITH_CODE_BLOCKS)
        def_fps = [fp for fp in fps if fp.category == "definition"]
        assert len(def_fps) >= 3

    def test_all_caps_constants_extracted(self):
        fps = extract_code_fingerprints(SPEC_WITH_CONSTANTS)
        texts = {fp.text for fp in fps}
        assert "PROGRAMMATIC_RUNNERS" in texts
        assert "HANDLER_REGISTRY" in texts
        assert "DISPATCH_TABLE" in texts

    def test_all_caps_category(self):
        # Use bare ALL_CAPS without backticks so they're found as constants
        content = "The system uses PROGRAMMATIC_RUNNERS for dispatch and HANDLER_REGISTRY for lookup."
        fps = extract_code_fingerprints(content)
        const_fps = [fp for fp in fps if fp.category == "constant"]
        assert len(const_fps) >= 1

    def test_excluded_constants_filtered(self):
        content = "Use TRUE, FALSE, NONE, YAML, JSON, STRICT in config."
        fps = extract_code_fingerprints(content)
        texts = {fp.text for fp in fps}
        for excluded in ["TRUE", "FALSE", "NONE", "YAML", "JSON", "STRICT"]:
            assert excluded not in texts

    def test_excluded_constants_frozenset(self):
        assert isinstance(_EXCLUDED_CONSTANTS, frozenset)
        assert "TRUE" in _EXCLUDED_CONSTANTS
        assert "FALSE" in _EXCLUDED_CONSTANTS


class TestDeduplication:
    """FR-MOD3.2: Deduplication by text value."""

    def test_duplicate_backtick_deduplicated(self):
        content = "Use `_run_step` here and `_run_step` there and `_run_step` again."
        fps = extract_code_fingerprints(content)
        texts = [fp.text for fp in fps]
        assert texts.count("_run_step") == 1

    def test_cross_source_dedup(self):
        content = """\
Use `_run_programmatic_step` in the executor.

```python
def _run_programmatic_step(config):
    pass
```
"""
        fps = extract_code_fingerprints(content)
        texts = [fp.text for fp in fps]
        assert texts.count("_run_programmatic_step") == 1


class TestCoverageRatio:
    """FR-MOD3.3: Case-insensitive coverage check returning 4-tuple."""

    def test_full_coverage(self):
        total, found, missing, ratio = check_fingerprint_coverage(
            SPEC_WITH_BACKTICKS, GOOD_ROADMAP
        )
        assert total >= 4
        assert ratio >= 0.7

    def test_partial_coverage(self):
        total, found, missing, ratio = check_fingerprint_coverage(
            SPEC_WITH_BACKTICKS, PARTIAL_ROADMAP
        )
        assert total >= 4
        assert 0.0 < ratio < 1.0
        assert len(missing) > 0

    def test_zero_coverage(self):
        total, found, missing, ratio = check_fingerprint_coverage(
            SPEC_WITH_BACKTICKS, EMPTY_ROADMAP
        )
        assert total >= 4
        assert found == 0
        assert ratio == 0.0

    def test_returns_4_tuple(self):
        result = check_fingerprint_coverage(SPEC_WITH_BACKTICKS, GOOD_ROADMAP)
        assert len(result) == 4
        total, found, missing, ratio = result
        assert isinstance(total, int)
        assert isinstance(found, int)
        assert isinstance(missing, list)
        assert isinstance(ratio, float)

    def test_case_insensitive_matching(self):
        spec = "Use `MyFunction` in the executor."
        roadmap = "Implement myfunction for dispatch."
        total, found, missing, ratio = check_fingerprint_coverage(spec, roadmap)
        assert found >= 1
        assert ratio >= 0.5


class TestThresholdGate:
    """FR-MOD3.4: Threshold gate logic."""

    def test_passes_above_threshold(self):
        assert fingerprint_gate_passed(SPEC_WITH_BACKTICKS, GOOD_ROADMAP, 0.7)

    def test_fails_below_threshold(self):
        assert not fingerprint_gate_passed(SPEC_WITH_BACKTICKS, EMPTY_ROADMAP, 0.7)

    def test_boundary_at_exactly_0_7(self):
        # Create spec with exactly 10 fingerprints, roadmap covering exactly 7
        spec = """\
Use `func_aaaa`, `func_bbbb`, `func_cccc`, `func_dddd`, `func_eeee`,
`func_ffff`, `func_gggg`, `func_hhhh`, `func_iiii`, `func_jjjj`.
"""
        roadmap = """\
Implement func_aaaa, func_bbbb, func_cccc, func_dddd, func_eeee,
func_ffff, func_gggg.
"""
        total, found, missing, ratio = check_fingerprint_coverage(spec, roadmap)
        assert total == 10
        assert found == 7
        assert abs(ratio - 0.7) < 0.01
        assert fingerprint_gate_passed(spec, roadmap, 0.7)

    def test_fails_just_below_threshold(self):
        spec = """\
Use `func_aaaa`, `func_bbbb`, `func_cccc`, `func_dddd`, `func_eeee`,
`func_ffff`, `func_gggg`, `func_hhhh`, `func_iiii`, `func_jjjj`.
"""
        roadmap = "Implement func_aaaa, func_bbbb, func_cccc, func_dddd, func_eeee, func_ffff."
        total, found, missing, ratio = check_fingerprint_coverage(spec, roadmap)
        assert total == 10
        assert found == 6
        assert ratio < 0.7
        assert not fingerprint_gate_passed(spec, roadmap, 0.7)


class TestEmptyFingerprintPassthrough:
    """FR-MOD3.4: Empty-fingerprint passthrough."""

    def test_empty_spec_passes(self):
        total, found, missing, ratio = check_fingerprint_coverage("", EMPTY_ROADMAP)
        assert total == 0
        assert ratio == 1.0

    def test_empty_spec_gate_passes(self):
        assert fingerprint_gate_passed("", EMPTY_ROADMAP, 0.7)

    def test_no_identifiers_passes(self):
        spec = "This spec has no code identifiers or backtick terms."
        assert fingerprint_gate_passed(spec, EMPTY_ROADMAP, 0.7)


class TestCliPortifyRegression:
    """SC-004: Detects missing identifiers at >= 95% confidence."""

    def test_detects_missing_identifiers(self):
        total, found, missing, ratio = check_fingerprint_coverage(
            CLI_PORTIFY_SPEC, CLI_PORTIFY_BAD_ROADMAP
        )
        # Should detect missing: _run_programmatic_step, PROGRAMMATIC_RUNNERS,
        # test_programmatic_step_routing
        missing_lower = [m.lower() for m in missing]
        assert "_run_programmatic_step" in missing_lower
        assert "programmatic_runners" in missing_lower
        assert "test_programmatic_step_routing" in missing_lower

    def test_gate_fails_on_bad_roadmap(self):
        assert not fingerprint_gate_passed(
            CLI_PORTIFY_SPEC, CLI_PORTIFY_BAD_ROADMAP, 0.7
        )

    def test_low_coverage_ratio(self):
        total, found, missing, ratio = check_fingerprint_coverage(
            CLI_PORTIFY_SPEC, CLI_PORTIFY_BAD_ROADMAP
        )
        assert ratio < 0.5  # Very low coverage expected
