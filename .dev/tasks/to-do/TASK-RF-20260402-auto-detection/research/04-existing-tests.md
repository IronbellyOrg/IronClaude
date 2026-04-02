# Research Track 4: Existing Test Coverage and Test Patterns

**Researcher**: researcher-4
**Scope**: `tests/cli/test_tdd_extract_prompt.py` and related test files
**Focus**: Document what's tested today, patterns used, new tests needed for multi-file auto-detection
**Date**: 2026-04-01

---

## 1. Test File Inventory

### Primary file: `tests/cli/test_tdd_extract_prompt.py` (500 lines)

**Imports** (lines 9-16):
- `build_extract_prompt`, `build_extract_prompt_tdd`, `build_merge_prompt`, `_OUTPUT_FORMAT_BLOCK` from `superclaude.cli.roadmap.prompts`
- `RoadmapConfig` from `superclaude.cli.roadmap.models`
- `TasklistValidateConfig` from `superclaude.cli.tasklist.models`

**Fixtures** (lines 19-23):
- `dummy_path(tmp_path)`: Creates `tmp_path / "test.md"` with content `"# Test"`. Used by most prompt-content tests.

### Other files with detection/input_type tests:
- `tests/roadmap/test_prd_prompts.py` lines 215-254: `TestRedundancyGuard` (2 tests)
- `tests/roadmap/test_validate_cli.py` line 204-209: Verifies `input_type` resolved from "auto" to "spec"

**No other test files test `detect_input_type` or multi-file routing.** The `tests/v3.3/test_wiring_points_e2e.py` mention of "auto-detect" is for sprint phase detection (unrelated). The `tests/audit/test_eval_wiring_multifile.py` is for audit wiring analyzer (unrelated).

---

## 2. Complete Test Catalog

### Class: `TestBuildExtractPromptTdd` (lines 26-85)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 1 | `test_has_all_14_sections` | All 14 TDD sections present in prompt | `dummy_path` | `assert section in result` loop |
| 2 | `test_has_tdd_frontmatter_fields` | 6 TDD frontmatter fields present | `dummy_path` | `assert field in result` loop |
| 3 | `test_has_output_format_block` | `_OUTPUT_FORMAT_BLOCK` constant present | `dummy_path` | `assert constant in result` |
| 4 | `test_preserves_spec_source` | `spec_source` field present | `dummy_path` | `assert "spec_source" in result` |
| 5 | `test_with_retrospective` | Retrospective content injected into prompt | `dummy_path` | Pass `retrospective_content=`, assert text present |
| 6 | `test_neutralized_framing` | New framing present, old framing absent | `dummy_path` | `assert X in` + `assert Y not in` |

### Class: `TestBuildExtractPromptUnchanged` (lines 87-98)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 7 | `test_no_tdd_sections_in_original` | Original `build_extract_prompt` has no TDD sections | `dummy_path` | `assert section not in result` |
| 8 | `test_original_has_spec_language` | Original prompt uses spec language | `dummy_path` | `assert "specification" in result.lower()` |

### Class: `TestRoadmapConfigDefaults` (lines 101-110)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 9 | `test_input_type_defaults_to_auto` | `RoadmapConfig.input_type` defaults to `"auto"` | none | Direct model instantiation |
| 10 | `test_tdd_file_defaults_to_none` | `RoadmapConfig.tdd_file` defaults to `None` | none | Direct model instantiation |

### Class: `TestTasklistValidateConfigDefaults` (lines 113-118)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 11 | `test_tdd_file_defaults_to_none` | `TasklistValidateConfig.tdd_file` defaults to `None` | none | Direct model instantiation |

### Class: `TestAutoDetection` (lines 121-182)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 12 | `test_detects_tdd_from_numbered_headings` | 24 numbered headings -> "tdd" | `tmp_path` | Write synthetic file, call `detect_input_type()` directly |
| 13 | `test_detects_spec_from_no_numbered_headings` | No numbered headings, no TDD signals -> "spec" | `tmp_path` | Same pattern |
| 14 | `test_detects_tdd_from_frontmatter_fields` | TDD-exclusive frontmatter + section names -> "tdd" | `tmp_path` | Same pattern |
| 15 | `test_detects_tdd_from_section_names` | TDD-specific section names alone -> "tdd" | `tmp_path` | Same pattern |
| 16 | `test_detects_tdd_from_real_template` | Real `tdd_template.md` detected as "tdd" | none | Reads actual file from `src/superclaude/examples/tdd_template.md` |
| 17 | `test_detects_spec_from_numbered_spec_template` | 12 numbered headings (spec-like) -> "spec" | `tmp_path` | Synthetic file with spec-like frontmatter |
| 18 | `test_detects_spec_from_empty_file` | Empty file -> "spec" | `tmp_path` | Edge case |
| 19 | `test_missing_file_defaults_to_spec` | Nonexistent file -> "spec" | `tmp_path` | Edge case |

### Class: `TestTddInputValidation` (lines 185-229)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 20 | `test_valid_tdd_file_no_extra_warning` | File with "Technical Design Document" in first 500 bytes | `tmp_path` | Read bytes[:500], assert string present |
| 21 | `test_non_tdd_file_triggers_warning_condition` | File without marker triggers warning | `tmp_path` | Assert string absent |
| 22 | `test_empty_file_triggers_warning_condition` | Empty file triggers warning | `tmp_path` | Assert string absent |
| 23 | `test_tdd_marker_beyond_500_bytes_triggers_warning` | Marker at byte 501+ still triggers warning | `tmp_path` | Assert string absent in [:500] |
| 24 | `test_read_bytes_handles_binary_gracefully` | Binary content doesn't raise | `tmp_path` | Write binary, decode with errors='replace' |

### Class: `TestExtractPromptTddWithPrd` (lines 232-264)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 25 | `test_prd_block_present_when_prd_file_given` | PRD block injected when `prd_file=` set | `dummy_path` | Assert strings present |
| 26 | `test_prd_block_absent_when_no_prd_file` | No PRD block without `prd_file` | `dummy_path` | Assert string absent |
| 27 | `test_tdd_block_present_when_tdd_file_given` | TDD supplementary block injected | `dummy_path` | Assert string present |
| 28 | `test_both_tdd_and_prd_blocks` | Both blocks present together | `dummy_path` | Assert both strings present |
| 29 | `test_prd_block_in_standard_extract` | PRD block works in `build_extract_prompt` too | `dummy_path` | Assert strings present |
| 30 | `test_prd_guardrail` | Priority guardrail text present | `dummy_path` | Assert priority text present |

### Class: `TestMergePromptTddPrd` (lines 267-296)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 31 | `test_merge_baseline_no_tdd_prd` | Merge prompt without TDD/PRD has no blocks | `dummy_path` | Assert strings absent |
| 32 | `test_merge_with_tdd` | Merge prompt with TDD file has TDD block | `dummy_path` | Assert strings present |
| 33 | `test_merge_with_prd` | Merge prompt with PRD file has PRD block | `dummy_path` | Assert strings present |
| 34 | `test_merge_with_both` | Merge prompt with both has both blocks | `dummy_path` | Assert strings present |

### Class: `TestOldSchemaStateBackwardCompat` (lines 299-348)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 35 | `test_state_without_tdd_prd_fields` | Old state without tdd/prd/input_type loads OK | `tmp_path` | Write JSON state, call `read_state()`, assert `.get()` is None |
| 36 | `test_restore_from_old_state_no_crash` | `_restore_from_state` handles old state | `tmp_path` | Write JSON state, call `_restore_from_state()`, assert fields None |

### Class: `TestDetectionThresholdBoundary` (lines 351-383)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 37 | `test_score_4_is_spec` | Score exactly 4 -> "spec" (coordinator+parent_doc = 4) | `tmp_path` | Construct doc with known score, assert result |
| 38 | `test_score_5_is_tdd` | Score exactly 5 -> "tdd" (4 + Data Models section = 5) | `tmp_path` | Same |
| 39 | `test_score_6_is_tdd` | Score 6 -> "tdd" (4 + 2 sections = 6) | `tmp_path` | Same |
| 40 | `test_zero_score_is_spec` | Score 0 -> "spec" (no TDD signals) | `tmp_path` | Same |

### Class: `TestSameFileGuard` (lines 386-424)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 41 | `test_same_file_raises_system_exit` | Same tdd_file and prd_file -> SystemExit | `tmp_path` | `pytest.raises(SystemExit)`, call `execute_roadmap()` |
| 42 | `test_different_files_no_error` | Different tdd/prd files -> no error (dry_run) | `tmp_path` | `execute_roadmap()` with `dry_run=True` |

### Class: `TestPrdFileOverrideOnResume` (lines 427-460)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 43 | `test_explicit_prd_not_overwritten_by_state` | CLI --prd-file overrides state prd_file | `tmp_path` | Write state JSON, call `_restore_from_state()`, assert CLI value wins |

### Class: `TestRedundancyGuardStatePersistence` (lines 463-499)
| # | Method | Tests | Fixture | Pattern |
|---|--------|-------|---------|---------|
| 44 | `test_tdd_primary_nullifies_tdd_file` | input_type=tdd + tdd_file -> guard nullifies | `tmp_path` | `execute_roadmap()` with `dry_run=True` |
| 45 | `test_tdd_primary_no_tdd_file_no_warning` | input_type=tdd + no tdd_file -> no warning | `tmp_path` | Same |

**Total: 45 tests across 13 classes.**

---

## 3. Test Pattern Analysis

### Pattern A: Prompt Content Assertion (tests 1-8, 25-34)
```python
def test_X(self, dummy_path):
    result = build_extract_prompt_tdd(dummy_path, optional_kwarg=value)
    assert "expected string" in result
```
- Uses `dummy_path` fixture (minimal `# Test` file)
- Calls prompt builder directly (not through CLI)
- Asserts substring presence/absence in returned string

### Pattern B: Model Default Assertion (tests 9-11)
```python
def test_X(self):
    config = RoadmapConfig(spec_file=Path("."))
    assert config.field == expected_default
```
- No fixture needed
- Direct dataclass instantiation, check field defaults

### Pattern C: Detection via Synthetic File (tests 12-19, 37-40)
```python
def test_X(self, tmp_path):
    from superclaude.cli.roadmap.executor import detect_input_type
    doc = tmp_path / "doc.md"
    doc.write_text("---\nfrontmatter...\n---\n## Headings\nContent.")
    assert detect_input_type(doc) == "tdd"  # or "spec"
```
- Uses `tmp_path` to create synthetic markdown files
- Imports `detect_input_type` inside the test method (not at module level)
- Writes carefully constructed content with known signal scores
- Asserts detection result directly

### Pattern D: Validation Logic (tests 20-24)
```python
def test_X(self, tmp_path):
    f = tmp_path / "file.md"
    f.write_text(content)
    head = f.read_bytes()[:500].decode("utf-8", errors="replace")
    assert "marker" in head  # or not in
```
- Replicates inline validation logic from commands.py
- Does NOT call Click runner -- tests the logic pattern, not the CLI wiring

### Pattern E: State/Executor Integration (tests 35-36, 41-45)
```python
def test_X(self, tmp_path):
    from superclaude.cli.roadmap.executor import read_state, _restore_from_state, execute_roadmap
    # Write state JSON, construct config, call function
    state = read_state(state_file)
    assert state.get("field") is None
```
- Uses `tmp_path` to write JSON state files
- Tests internal executor functions directly
- Some tests call `execute_roadmap()` with `dry_run=True` to test guards

### Pattern F: Real Template Test (test 16)
```python
def test_X(self):
    tdd = Path("src/superclaude/examples/tdd_template.md")
    if tdd.exists():
        assert detect_input_type(tdd) == "tdd"
```
- Reads an actual repo file (not synthetic)
- Conditional execution (`if tdd.exists()`)

---

## 4. What Is NOT Tested Today

### 4a. No PRD Detection Tests
The current `detect_input_type()` returns only `"tdd"` or `"spec"`. There is **zero** test coverage for PRD detection because the function doesn't support it yet. No test creates a PRD-like file and checks the result.

### 4b. No Multi-File Input Tests
There are **zero** tests for:
- Passing multiple files to a Click command via `nargs=-1`
- Routing logic that maps multiple files to `spec_file`, `tdd_file`, `prd_file`
- Any `classify_files()` or equivalent multi-file dispatcher

### 4c. No Click CLI Runner Tests
**No test in `tests/cli/test_tdd_extract_prompt.py` uses `CliRunner` or `invoke()`.** All tests call Python functions directly. This means CLI argument parsing (Click `nargs=-1`, `--input-type`, etc.) is untested in this file.

### 4d. No Override Tests
There is no test verifying that `--input-type=tdd` overrides auto-detection. The `test_input_type_defaults_to_auto` (test #9) only checks the default value, not that an explicit value wins.

---

## 5. New Tests Needed for Multi-File Auto-Detection

### 5.1 PRD Detection Tests (Pattern C -- synthetic file)
| Test | Description | Pattern |
|------|-------------|---------|
| `test_detects_prd_from_real_fixture` | Real PRD fixture file detected as "prd" | Pattern F (real file) |
| `test_detects_prd_from_prd_signals` | Synthetic PRD content (user personas, success metrics, business context, no TDD signals) -> "prd" | Pattern C |
| `test_prd_not_confused_with_tdd` | PRD signals (high PRD score) when TDD score is low -> "prd" not "tdd" | Pattern C |
| `test_prd_not_confused_with_spec` | PRD signals clearly differentiate from spec default | Pattern C |

### 5.2 Three-Way Boundary Tests (Pattern C -- exact score construction)
| Test | Description | Pattern |
|------|-------------|---------|
| `test_three_way_boundary_prd_not_tdd_not_spec` | File with PRD signals but not TDD signals -> "prd" | Pattern C |
| `test_three_way_boundary_tdd_not_prd_not_spec` | File with TDD signals but not PRD signals -> "tdd" | Pattern C |
| `test_three_way_boundary_spec_no_signals` | File with neither PRD nor TDD signals -> "spec" | Pattern C |
| `test_ambiguous_prd_tdd_signals` | File with both PRD and TDD signals -> whichever wins by score | Pattern C |

### 5.3 Multi-File Routing Tests (7 scenarios)
These will need a new pattern -- either testing a `classify_files()` function directly (Pattern C style) or using `CliRunner` (new Pattern G).

| Test | Input Files | Expected Routing | Pattern |
|------|-------------|-----------------|---------|
| `test_single_spec_file` | 1 spec | `spec_file=spec` | Backward compat |
| `test_single_tdd_file` | 1 TDD | `spec_file=tdd, input_type="tdd"` | Backward compat |
| `test_single_prd_file` | 1 PRD | `spec_file=prd, input_type="prd"` | New |
| `test_spec_plus_tdd` | spec + TDD | `spec_file=spec, tdd_file=tdd` | New |
| `test_spec_plus_prd` | spec + PRD | `spec_file=spec, prd_file=prd` | New |
| `test_tdd_plus_prd` | TDD + PRD | `spec_file=tdd, prd_file=prd, input_type="tdd"` | New |
| `test_all_three_files` | spec + TDD + PRD | `spec_file=spec, tdd_file=tdd, prd_file=prd` | New |

### 5.4 Backward Compatibility Tests
| Test | Description | Pattern |
|------|-------------|---------|
| `test_single_positional_still_works` | Existing `superclaude roadmap run spec.md` still works | Pattern E or new CLI runner test |
| `test_explicit_input_type_overrides_detection` | `--input-type=tdd` overrides auto-detection result | Pattern E |
| `test_explicit_tdd_file_flag_still_works` | `--tdd-file=X` still accepted alongside positional | Pattern E |
| `test_explicit_prd_file_flag_still_works` | `--prd-file=X` still accepted alongside positional | Pattern E |

### 5.5 Override Priority Tests
| Test | Description | Pattern |
|------|-------------|---------|
| `test_explicit_flag_wins_over_auto_detection` | `--input-type=spec` on a TDD file -> "spec" | Pattern C + E |
| `test_explicit_tdd_file_wins_over_positional_routing` | `--tdd-file=X` not overridden by positional auto-routing | Pattern E |

---

## 6. Recommended Test Structure for New Tests

### New Test Class Placement
All new tests should go in `tests/cli/test_tdd_extract_prompt.py` (or a new `tests/cli/test_multi_file_detection.py` if scope warrants separation).

### Recommended New Classes
```
class TestPrdDetection:           # 5.1 -- PRD detection
class TestThreeWayBoundary:       # 5.2 -- PRD vs TDD vs spec boundaries
class TestMultiFileRouting:       # 5.3 -- multi-file dispatch
class TestBackwardCompat:         # 5.4 -- single positional, explicit flags
class TestOverridePriority:       # 5.5 -- explicit wins over detection
```

### Fixture Needs
- Existing `dummy_path` covers prompt tests
- Existing `tmp_path` covers synthetic file tests
- **New needed**: A `prd_fixture_path` fixture pointing to a real PRD fixture file (e.g., in `.dev/test-fixtures/` or `tests/fixtures/`)
- **New needed**: A `classify_files` or routing function to test (depends on implementation design -- researcher-3's territory)

---

## 7. Cross-File Test Coverage Summary

| File | Detection Tests | Routing Tests | CLI Runner Tests |
|------|----------------|---------------|-----------------|
| `tests/cli/test_tdd_extract_prompt.py` | 12 (TDD vs spec only) | 0 | 0 |
| `tests/roadmap/test_prd_prompts.py` | 0 (redundancy guard only) | 0 | 0 |
| `tests/roadmap/test_validate_cli.py` | 1 (input_type resolved) | 0 | 0 |
| **Total** | **13** | **0** | **0** |

### Key Gap: No CLI-Level Tests
None of the existing tests invoke the Click CLI. All tests call Python functions directly. This means:
- Click argument parsing is untested
- `nargs=-1` behavior will be completely new test territory
- Error messages from Click validation are untested

---

## 8. Summary of Findings

1. **45 existing tests** in `test_tdd_extract_prompt.py` across 13 classes
2. **Detection is binary** (TDD vs spec) with score threshold at 5 -- no PRD detection exists
3. **All tests use direct function calls** -- zero Click CliRunner tests
4. **Dominant pattern**: synthetic file via `tmp_path` + `detect_input_type()` call + assert result
5. **Zero multi-file routing tests** exist anywhere in the codebase
6. **~18 new tests needed** across 5 new test classes for PRD detection, three-way boundary, multi-file routing (7 scenarios), backward compat, and override priority
7. **New test infrastructure needed**: PRD fixture file, possible `classify_files()` function tests, and potentially first CLI runner tests for argument parsing validation

