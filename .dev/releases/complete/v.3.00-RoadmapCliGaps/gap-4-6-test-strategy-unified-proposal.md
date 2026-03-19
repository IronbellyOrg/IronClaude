# Gaps #4 + #6 (Merged) — Test-Strategy Prompt & Gate Hardening

## Problem Statement

The source protocol's `test-strategy.md` frontmatter schema (in `refs/templates.md`, lines 432-447) specifies 9 fields:

```yaml
spec_source: <path>
generated: <ISO-8601 timestamp>
generator: sc:roadmap
validation_philosophy: continuous-parallel
validation_milestones: <count>
work_milestones: <count>
interleave_ratio: "<validation>:<work>"
major_issue_policy: stop-and-fix
complexity_class: <LOW|MEDIUM|HIGH>
```

The CLI implementation requests only 2 fields (`validation_milestones`, `interleave_ratio`) and has zero semantic checks with STANDARD enforcement.

**This proposal merges Gap #4 (complexity_class + ratio consistency) and Gap #6 (policy fields) since both rewrite the same prompt function and gate definition.**

Note: Provenance fields (`spec_source`, `generated`, `generator`) are handled separately by Gap #5 via executor injection.

---

## Analysis Summary

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `complexity_class` | Dynamic (from extraction) | Gap #4 | Claude reads from extraction frontmatter |
| `interleave_ratio` | Dynamic (derived from complexity) | Gap #4 | Must match complexity mapping |
| `validation_milestones` | Dynamic (counted by Claude) | Existing | Already in prompt/gate |
| `work_milestones` | Dynamic (counted by Claude) | Gap #6 | Count M# or Phase headings from roadmap |
| `validation_philosophy` | Fixed constant: `continuous-parallel` | Gap #6 | Prompt instructs exact value |
| `major_issue_policy` | Fixed constant: `stop-and-fix` | Gap #6 | Prompt instructs exact value |

### Key Design Decisions

1. **`complexity_class` read from extraction, not re-derived** — prevents inconsistency between artifacts
2. **Constants via prompt instruction** — matches existing pattern (`build_merge_prompt` → `adversarial: true`)
3. **`work_milestones` handles both `M#` and `Phase N` naming** — real outputs use both conventions
4. **`_complexity_class_valid` reuses Gap #1's function** — identical logic, avoid duplication
5. **`_milestone_counts_positive` validates both milestone fields** — subsumes Gap #6's single-field `_work_milestones_positive_int`
6. **Gate upgrade STANDARD → STRICT** — all gates with semantic checks use STRICT (codebase invariant)

---

## Implementation Plan

### Change 1: Rewrite `build_test_strategy_prompt` in `prompts.py`

**File**: `src/superclaude/cli/roadmap/prompts.py`, lines 350-373

```python
def build_test_strategy_prompt(
    roadmap_path: Path,
    extraction_path: Path,
) -> str:
    """Prompt for step 'test-strategy'.

    Instructs Claude to produce a test strategy with all 6 protocol-required
    frontmatter fields (provenance fields are injected by the executor).
    """
    return (
        "You are a test strategy specialist.\n\n"
        "Read the final roadmap and the requirements extraction document. "
        "Produce a comprehensive test strategy.\n\n"
        "IMPORTANT: Read the complexity_class field from the extraction document's "
        "YAML frontmatter. Use it to determine the interleave ratio:\n"
        "- LOW complexity -> 1:3 (one validation per three work milestones)\n"
        "- MEDIUM complexity -> 1:2 (one validation per two work milestones)\n"
        "- HIGH complexity -> 1:1 (one validation per work milestone)\n\n"
        "Your output MUST begin with YAML frontmatter delimited by --- lines containing:\n"
        "- complexity_class: (string) one of: LOW, MEDIUM, HIGH -- copied from extraction\n"
        "- validation_philosophy: continuous-parallel (use this exact value)\n"
        "- validation_milestones: (integer) count of V# validation milestones defined\n"
        "- work_milestones: (integer) count of work milestones (M# or Phase headings) "
        "from the roadmap\n"
        "- interleave_ratio: (string) validation-to-work ratio, e.g. '1:2' -- MUST match "
        "the complexity_class mapping above\n"
        "- major_issue_policy: stop-and-fix (use this exact value)\n\n"
        "After the frontmatter, provide:\n"
        "1. Validation milestones mapped to roadmap phases\n"
        "2. Test categories (unit, integration, E2E, acceptance)\n"
        "3. Test-implementation interleaving strategy with rationale from complexity class\n"
        "4. Risk-based test prioritization\n"
        "5. Acceptance criteria per milestone\n"
        "6. Quality gates between phases\n"
        "7. Issue classification table with severity levels (Critical, Major, Minor, Info) "
        "and stop-and-fix thresholds\n\n"
        "Be specific about what to test at each milestone."
    ) + _OUTPUT_FORMAT_BLOCK
```

### Change 2: Add semantic check functions in `gates.py`

**File**: `src/superclaude/cli/roadmap/gates.py`

Add 4 new semantic check functions. Note: `_complexity_class_valid` is defined once and shared with `EXTRACT_GATE` (from Gap #1).

```python
# --- Semantic check functions for test-strategy ---

# NOTE: _complexity_class_valid is defined by Gap #1 for EXTRACT_GATE.
# Reuse it here — do NOT define a second copy.

_COMPLEXITY_RATIO_MAP = {
    "LOW": "1:3",
    "MEDIUM": "1:2",
    "HIGH": "1:1",
}


def _interleave_ratio_consistent(content: str) -> bool:
    """interleave_ratio must match complexity_class mapping.

    LOW -> 1:3, MEDIUM -> 1:2, HIGH -> 1:1.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    cc = fm.get("complexity_class")
    ratio = fm.get("interleave_ratio")
    if cc is None or ratio is None:
        return False
    expected = _COMPLEXITY_RATIO_MAP.get(cc.upper())
    if expected is None:
        return False
    # Strip quotes that YAML may leave
    return ratio.strip("\"'") == expected


def _milestone_counts_positive(content: str) -> bool:
    """validation_milestones and work_milestones must be positive integers."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    for field in ("validation_milestones", "work_milestones"):
        value = fm.get(field)
        if value is None:
            return False
        try:
            if int(value) <= 0:
                return False
        except (ValueError, TypeError):
            return False
    return True


def _validation_philosophy_correct(content: str) -> bool:
    """validation_philosophy must equal 'continuous-parallel' exactly."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("validation_philosophy")
    if value is None:
        return False
    return value == "continuous-parallel"


def _major_issue_policy_correct(content: str) -> bool:
    """major_issue_policy must equal 'stop-and-fix' exactly."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("major_issue_policy")
    if value is None:
        return False
    return value == "stop-and-fix"
```

### Change 3: Rewrite `TEST_STRATEGY_GATE` in `gates.py`

**File**: `src/superclaude/cli/roadmap/gates.py`, lines 627-631

```python
TEST_STRATEGY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "complexity_class",
        "validation_philosophy",
        "validation_milestones",
        "work_milestones",
        "interleave_ratio",
        "major_issue_policy",
    ],
    min_lines=40,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="complexity_class_valid",
            check_fn=_complexity_class_valid,  # Reused from Gap #1
            failure_message="complexity_class must be one of: LOW, MEDIUM, HIGH",
        ),
        SemanticCheck(
            name="interleave_ratio_consistent",
            check_fn=_interleave_ratio_consistent,
            failure_message="interleave_ratio must match complexity_class: LOW->1:3, MEDIUM->1:2, HIGH->1:1",
        ),
        SemanticCheck(
            name="milestone_counts_positive",
            check_fn=_milestone_counts_positive,
            failure_message="validation_milestones and work_milestones must be positive integers",
        ),
        SemanticCheck(
            name="validation_philosophy_correct",
            check_fn=_validation_philosophy_correct,
            failure_message="validation_philosophy must be 'continuous-parallel'",
        ),
        SemanticCheck(
            name="major_issue_policy_correct",
            check_fn=_major_issue_policy_correct,
            failure_message="major_issue_policy must be 'stop-and-fix'",
        ),
    ],
)
```

**Final field count**: 6 required fields, 5 semantic checks (after deduplication).

When Gap #5 (provenance injection) is also applied, the gate gains 3 more required fields (`spec_source`, `generated`, `generator`) for a total of 9 required fields and 5 semantic checks.

### Change 4: Update tests in `test_gates_data.py`

**File**: `tests/roadmap/test_gates_data.py`

Update the existing STANDARD tier test and add comprehensive semantic check tests:

```python
# --- Replace existing test_test_strategy_gate_standard ---

def test_test_strategy_gate_strict(self):
    """Gate upgraded from STANDARD to STRICT with semantic checks."""
    assert TEST_STRATEGY_GATE.enforcement_tier == "STRICT"


class TestTestStrategyGateStructure:
    """Structural assertions for the merged TEST_STRATEGY_GATE."""

    def test_required_fields_count(self):
        assert len(TEST_STRATEGY_GATE.required_frontmatter_fields) == 6

    def test_required_fields_completeness(self):
        expected = {
            "complexity_class", "validation_philosophy", "validation_milestones",
            "work_milestones", "interleave_ratio", "major_issue_policy",
        }
        assert set(TEST_STRATEGY_GATE.required_frontmatter_fields) == expected

    def test_semantic_checks_count(self):
        assert TEST_STRATEGY_GATE.semantic_checks is not None
        assert len(TEST_STRATEGY_GATE.semantic_checks) == 5

    def test_min_lines(self):
        assert TEST_STRATEGY_GATE.min_lines == 40


class TestComplexityClassValid:
    """Tests for _complexity_class_valid (shared with EXTRACT_GATE via Gap #1)."""

    def test_valid_low(self):
        assert _complexity_class_valid("---\ncomplexity_class: LOW\n---\n")

    def test_valid_medium(self):
        assert _complexity_class_valid("---\ncomplexity_class: MEDIUM\n---\n")

    def test_valid_high(self):
        assert _complexity_class_valid("---\ncomplexity_class: HIGH\n---\n")

    def test_case_insensitive(self):
        assert _complexity_class_valid("---\ncomplexity_class: low\n---\n")
        assert _complexity_class_valid("---\ncomplexity_class: Medium\n---\n")

    def test_invalid_enterprise(self):
        assert not _complexity_class_valid("---\ncomplexity_class: enterprise\n---\n")

    def test_invalid_simple(self):
        assert not _complexity_class_valid("---\ncomplexity_class: simple\n---\n")

    def test_missing(self):
        assert not _complexity_class_valid("---\nother: value\n---\n")

    def test_no_frontmatter(self):
        assert not _complexity_class_valid("No frontmatter here")


class TestInterleaveRatioConsistent:

    def test_low_1_3(self):
        fm = "---\ncomplexity_class: LOW\ninterleave_ratio: 1:3\n---\n"
        assert _interleave_ratio_consistent(fm)

    def test_medium_1_2(self):
        fm = "---\ncomplexity_class: MEDIUM\ninterleave_ratio: 1:2\n---\n"
        assert _interleave_ratio_consistent(fm)

    def test_high_1_1(self):
        fm = "---\ncomplexity_class: HIGH\ninterleave_ratio: 1:1\n---\n"
        assert _interleave_ratio_consistent(fm)

    def test_mismatch_low_1_1(self):
        fm = "---\ncomplexity_class: LOW\ninterleave_ratio: 1:1\n---\n"
        assert not _interleave_ratio_consistent(fm)

    def test_mismatch_high_1_3(self):
        fm = "---\ncomplexity_class: HIGH\ninterleave_ratio: 1:3\n---\n"
        assert not _interleave_ratio_consistent(fm)

    def test_quoted_ratio(self):
        fm = '---\ncomplexity_class: MEDIUM\ninterleave_ratio: "1:2"\n---\n'
        assert _interleave_ratio_consistent(fm)


class TestMilestoneCountsPositive:

    def test_both_positive(self):
        fm = "---\nvalidation_milestones: 3\nwork_milestones: 6\n---\n"
        assert _milestone_counts_positive(fm)

    def test_validation_zero(self):
        fm = "---\nvalidation_milestones: 0\nwork_milestones: 6\n---\n"
        assert not _milestone_counts_positive(fm)

    def test_work_zero(self):
        fm = "---\nvalidation_milestones: 3\nwork_milestones: 0\n---\n"
        assert not _milestone_counts_positive(fm)

    def test_negative(self):
        fm = "---\nvalidation_milestones: -1\nwork_milestones: 6\n---\n"
        assert not _milestone_counts_positive(fm)

    def test_non_integer(self):
        fm = "---\nvalidation_milestones: many\nwork_milestones: 6\n---\n"
        assert not _milestone_counts_positive(fm)

    def test_missing_field(self):
        fm = "---\nvalidation_milestones: 3\n---\n"
        assert not _milestone_counts_positive(fm)


class TestValidationPhilosophyCorrect:

    def test_correct(self):
        assert _validation_philosophy_correct("---\nvalidation_philosophy: continuous-parallel\n---\n")

    def test_underscore_variant_rejected(self):
        assert not _validation_philosophy_correct("---\nvalidation_philosophy: continuous_parallel\n---\n")

    def test_wrong_value(self):
        assert not _validation_philosophy_correct("---\nvalidation_philosophy: batch-sequential\n---\n")

    def test_missing(self):
        assert not _validation_philosophy_correct("---\nother: value\n---\n")

    def test_no_frontmatter(self):
        assert not _validation_philosophy_correct("No frontmatter")


class TestMajorIssuePolicyCorrect:

    def test_correct(self):
        assert _major_issue_policy_correct("---\nmajor_issue_policy: stop-and-fix\n---\n")

    def test_wrong_value(self):
        assert not _major_issue_policy_correct("---\nmajor_issue_policy: continue-and-log\n---\n")

    def test_halt_variant_rejected(self):
        assert not _major_issue_policy_correct("---\nmajor_issue_policy: halt-and-fix\n---\n")

    def test_missing(self):
        assert not _major_issue_policy_correct("---\nother: value\n---\n")


class TestBuildTestStrategyPrompt:

    def test_prompt_mentions_complexity_class(self):
        prompt = build_test_strategy_prompt(Path("roadmap.md"), Path("extraction.md"))
        assert "complexity_class" in prompt

    def test_prompt_contains_ratio_mapping(self):
        prompt = build_test_strategy_prompt(Path("roadmap.md"), Path("extraction.md"))
        assert "LOW complexity -> 1:3" in prompt
        assert "MEDIUM complexity -> 1:2" in prompt
        assert "HIGH complexity -> 1:1" in prompt

    def test_prompt_instructs_reading_from_extraction(self):
        prompt = build_test_strategy_prompt(Path("roadmap.md"), Path("extraction.md"))
        assert "extraction" in prompt.lower()

    def test_prompt_has_policy_constants(self):
        prompt = build_test_strategy_prompt(Path("roadmap.md"), Path("extraction.md"))
        assert "continuous-parallel" in prompt
        assert "stop-and-fix" in prompt

    def test_prompt_requests_work_milestones(self):
        prompt = build_test_strategy_prompt(Path("roadmap.md"), Path("extraction.md"))
        assert "work_milestones" in prompt
        assert "M# or Phase" in prompt
```

---

## Files Changed

| File | Change | From |
|------|--------|------|
| `src/superclaude/cli/roadmap/prompts.py` | Rewrite `build_test_strategy_prompt` | Gap #4 + #6 |
| `src/superclaude/cli/roadmap/gates.py` | Add 4 semantic checks; rewrite `TEST_STRATEGY_GATE` (6 fields, 5 checks, STRICT) | Gap #4 + #6 |
| `tests/roadmap/test_gates_data.py` | Replace STANDARD test; add 8 test classes (~35 test cases) | Gap #4 + #6 |

---

## Dependencies and Ordering

| Dependency | Reason |
|------------|--------|
| **Gap #1 must land first** | Defines `_complexity_class_valid` which this proposal reuses |
| **Gap #5 is independent** | Executor injection; can land before or after this proposal |
| **Gap #5 gate fields** | When Gap #5 adds `spec_source`, `generated`, `generator` to the gate, update `test_required_fields_count` from 6 to 9 and update `test_required_fields_completeness` |

---

## Deduplication Record

| Original Proposal | What Was Dropped | Why |
|-------------------|-----------------|-----|
| Gap #4 Section 3C | Extract prompt enum fix | Duplicated by Gap #1 Change 1 |
| Gap #4 `_complexity_class_valid` | Separate function definition | Reuses Gap #1's definition |
| Gap #6 `_work_milestones_positive_int` | Single-field milestone check | Subsumed by `_milestone_counts_positive` (validates both fields) |
| Gap #6 `test_test_strategy_gate_fields` | Standalone field assertions | Merged into `TestTestStrategyGateStructure` class |

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Existing pipeline outputs fail new gate | LOW | Gate only applies to new runs; old outputs not re-validated |
| LLM ignores ratio mapping instruction | LOW | `_interleave_ratio_consistent` catches at gate time; retry handles it |
| LLM emits wrong constant value | LOW | Exact-match semantic checks catch; historical `continuous_parallel` confirms this risk is real |
| STRICT enforcement causes more retries | LOW | Acceptable — incorrect ratios silently degrade validation quality |
| `work_milestones` miscounted for Phase-style roadmaps | LOW | Prompt explicitly says "M# or Phase headings"; gate validates positive integer |

---

## Validation Result

**Date**: 2026-03-18
**Verdict**: PASS — this merged proposal incorporates all corrections identified by both reflection agents:
- Gap #4 Section 3C removed (deferred to Gap #1)
- `_complexity_class_valid` reuses Gap #1's function
- `_work_milestones_positive_int` replaced by `_milestone_counts_positive`
- `work_milestones` prompt handles both M# and Phase naming
- Case-insensitive test added for `_complexity_class_valid`
- Semantic check count corrected to 5 (after deduplication)
- Existing `test_test_strategy_gate_standard` test flagged for update
