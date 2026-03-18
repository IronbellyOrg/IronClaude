# Gap #1: `complexity_class` Enum Mismatch -- Implementation Proposal

## Problem Statement

The `complexity_class` field uses two incompatible enum sets across the codebase:

| Location | Enum Values | Role |
|----------|-------------|------|
| `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` (source protocol) | `LOW \| MEDIUM \| HIGH` | Source of truth for milestone count selection, interleave ratios, effort mapping |
| `src/superclaude/cli/roadmap/prompts.py` line 88 (CLI extract prompt) | `simple \| moderate \| complex \| enterprise` | Instructs the LLM what values to emit in extraction frontmatter |
| `src/superclaude/examples/release-spec-template.md` line 28 | `simple_or_moderate_or_high` | Placeholder hint for spec authors (itself a third variant -- mixes both sets) |
| Test fixtures (3 files) | `moderate` | Hardcoded test values using the CLI enum |

The source protocol's milestone count table maps `LOW`, `MEDIUM`, `HIGH` to specific milestone ranges (3-4, 5-7, 8-12). When the CLI prompt tells the LLM to emit `simple`, `moderate`, `complex`, or `enterprise`, no downstream code or template logic can match those values to the protocol's decision tables. The gate (`EXTRACT_GATE` in `gates.py`) only checks that `complexity_class` is present in frontmatter -- it does not validate the value itself.

## Inventory of All Touchpoints

### 1. CLI Extract Prompt (prompts.py:88) -- THE BUG

```python
"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"
```

This is the single line that introduces the wrong enum. It tells the LLM extraction agent to emit values from a 4-value set that does not exist anywhere in the source protocol.

### 2. Extract Gate (gates.py:523-541) -- MISSING VALIDATION

`EXTRACT_GATE` requires `complexity_class` as a frontmatter field but performs no value validation. The field passes the gate regardless of whether its value is `LOW`, `moderate`, `banana`, or empty string (as long as it is present).

### 3. Source Protocol Templates (templates.md) -- SOURCE OF TRUTH

Three YAML frontmatter schemas (roadmap.md, extraction.md, test-strategy.md) all define:
```yaml
complexity_class: <LOW|MEDIUM|HIGH>
```

The milestone count selection table explicitly maps:
- `LOW (< 0.4)` --> 3-4 milestones, base = 3
- `MEDIUM (0.4-0.7)` --> 5-7 milestones, base = 5
- `HIGH (> 0.7)` --> 8-12 milestones, base = 8

Validation milestone interleaving also keys on `LOW`, `MEDIUM`, `HIGH`.

### 4. Release Spec Template (release-spec-template.md:28) -- SECONDARY INCONSISTENCY

```yaml
complexity_class: {{SC_PLACEHOLDER:simple_or_moderate_or_high}}
```

This placeholder hint mixes terminology from both sets (`simple` from CLI, `high` from protocol). It should align with whichever canonical set is chosen.

### 5. Test Fixtures (3 files) -- WILL NEED UPDATE

- `tests/roadmap/test_pipeline_integration.py:86` -- `"complexity_class": "moderate"`
- `tests/roadmap/test_executor.py:102` -- `"complexity_class": "moderate"`
- `tests/roadmap/test_integration_v5_pipeline.py:91` -- `"complexity_class": "moderate"`

All use `"moderate"` (CLI enum). These must be updated to match whichever canonical set is chosen.

### 6. Generate Prompt (prompts.py:145) -- PASSTHROUGH ONLY

The generate prompt references `complexity_class` as context for the roadmap generation agent but does not specify valid values. It simply says "complexity_class: complexity assessment". This line needs no change -- it just passes through whatever the extraction emitted.

### 7. No Python Enum or Validation Code Exists

There is no Python `Enum` class, no validation function, and no mapping logic in the CLI codebase that parses `complexity_class` string values. The only consumer is the source protocol's markdown tables (interpreted by the LLM during generation). This means the mismatch is currently "silent" -- no code crashes, but the LLM generation agent receives values it cannot map to the protocol's decision tables.

## Analysis: Which Enum Set Wins?

**The protocol's `LOW|MEDIUM|HIGH` must win.** Rationale:

1. **Source of truth**: `templates.md` is the canonical reference document loaded during Waves 2-3. It defines the decision tables that consume `complexity_class`.

2. **Downstream coupling**: Milestone count selection, interleave ratios, and effort estimation all key on `LOW|MEDIUM|HIGH`. The CLI's `simple|moderate|complex|enterprise` set has zero downstream consumers.

3. **Score-to-class mapping**: The protocol maps `complexity_score` ranges to classes (`< 0.4` = LOW, `0.4-0.7` = MEDIUM, `> 0.7` = HIGH). A 4-value set would require new range boundaries that don't exist.

4. **`enterprise` has no definition**: The 4th value `enterprise` has no score range, no milestone count, and no interleave ratio. It is undefined behavior.

5. **Consistency**: Three frontmatter schemas in `templates.md` all use `LOW|MEDIUM|HIGH`. The CLI prompt is the sole outlier.

## Proposed Changes

### Change 1: Fix the extract prompt enum (prompts.py:88)

**File**: `src/superclaude/cli/roadmap/prompts.py`
**Line**: 88

Replace:
```python
"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"
```
With:
```python
"- complexity_class: (string) one of: LOW, MEDIUM, HIGH\n"
```

**Risk**: LOW. This only changes the LLM instruction. The LLM will now emit values that match the protocol's decision tables.

### Change 2: Add enum validation semantic check to EXTRACT_GATE (gates.py)

**File**: `src/superclaude/cli/roadmap/gates.py`

Add a new semantic check function:

```python
_VALID_COMPLEXITY_CLASSES = frozenset({"LOW", "MEDIUM", "HIGH"})

def _complexity_class_valid(content: str) -> bool:
    """complexity_class frontmatter value must be one of LOW, MEDIUM, HIGH."""
    fm = _parse_frontmatter(content)
    if fm is None:
        return False
    value = fm.get("complexity_class")
    if value is None:
        return False
    return value.upper() in _VALID_COMPLEXITY_CLASSES
```

Register it on `EXTRACT_GATE`:

```python
EXTRACT_GATE = GateCriteria(
    required_frontmatter_fields=[...],  # unchanged
    min_lines=50,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="complexity_class_valid",
            check_fn=_complexity_class_valid,
            failure_message="complexity_class must be one of: LOW, MEDIUM, HIGH",
        ),
    ],
)
```

**Design decision -- case sensitivity**: The check uses `.upper()` so that `low`, `Low`, and `LOW` all pass. This is forgiving toward LLM output variance while still rejecting invalid values like `moderate` or `enterprise`. The canonical form in the protocol is uppercase, but LLMs occasionally emit title-case.

**Risk**: LOW. This adds a gate that catches the exact bug we are fixing. If an older extraction artifact with `moderate` is re-validated, it will now correctly fail the gate, which is the desired behavior.

### Change 3: Fix the release-spec-template placeholder (release-spec-template.md:28)

**File**: `src/superclaude/examples/release-spec-template.md`
**Line**: 28

Replace:
```yaml
complexity_class: {{SC_PLACEHOLDER:simple_or_moderate_or_high}}
```
With:
```yaml
complexity_class: {{SC_PLACEHOLDER:LOW_or_MEDIUM_or_HIGH}}
```

**Risk**: NONE. This is a documentation template placeholder.

### Change 4: Update test fixtures (3 files)

Replace `"complexity_class": "moderate"` with `"complexity_class": "MEDIUM"` in:

- `tests/roadmap/test_pipeline_integration.py:86`
- `tests/roadmap/test_executor.py:102`
- `tests/roadmap/test_integration_v5_pipeline.py:91`

**Risk**: LOW. Tests should reflect the canonical enum. If any test was specifically validating that `moderate` passes the gate, that test was testing the wrong invariant.

### Change 5 (optional): Add a gate-level test for the new semantic check

Add a test in `tests/roadmap/test_gates_data.py` that verifies:
- `_complexity_class_valid` returns `True` for `LOW`, `MEDIUM`, `HIGH`, `low`, `Medium`
- `_complexity_class_valid` returns `False` for `moderate`, `simple`, `complex`, `enterprise`, empty string, missing field

## Migration Safety Assessment

| Concern | Assessment |
|---------|------------|
| **Does changing the prompt break existing artifacts?** | No. Existing artifacts are already generated. The prompt only affects future extractions. |
| **Does the new gate reject old artifacts?** | Yes, intentionally. Old artifacts with `moderate` will fail re-validation. This is correct behavior -- they were always misaligned with the protocol. |
| **Can downstream LLM agents handle the change?** | Yes. The generate prompt (line 145) passes `complexity_class` as context without specifying valid values. The LLM roadmap agent reads `templates.md` which already uses `LOW\|MEDIUM\|HIGH`. |
| **Are there any Python consumers that parse the string value?** | No. No Python code in the CLI parses `complexity_class` values. The gate checks presence only (until Change 2 adds value validation). |
| **Does `enterprise` need a replacement?** | No. The protocol's 3-tier system (`LOW < 0.4`, `MEDIUM 0.4-0.7`, `HIGH > 0.7`) covers the full score range. There is no gap that `enterprise` was filling. |

## Execution Order

1. **Change 1** (prompts.py) -- fix the source of wrong values
2. **Change 2** (gates.py) -- add validation to catch future regressions
3. **Change 3** (release-spec-template.md) -- align documentation
4. **Change 4** (test fixtures) -- align tests with canonical enum
5. **Change 5** (test_gates_data.py) -- add regression test for the new check

Changes 1-4 should be a single atomic commit. Change 5 can be the same commit or a follow-up.

## Files Modified

| File | Change Type |
|------|-------------|
| `src/superclaude/cli/roadmap/prompts.py` | Bug fix (line 88) |
| `src/superclaude/cli/roadmap/gates.py` | Enhancement (new semantic check + registration) |
| `src/superclaude/examples/release-spec-template.md` | Documentation alignment (line 28) |
| `tests/roadmap/test_pipeline_integration.py` | Test fixture update (line 86) |
| `tests/roadmap/test_executor.py` | Test fixture update (line 102) |
| `tests/roadmap/test_integration_v5_pipeline.py` | Test fixture update (line 91) |
| `tests/roadmap/test_gates_data.py` | New test cases (optional Change 5) |

## Validation Result

**Reviewed**: 2026-03-18 | **Verdict**: PASS with minor clarifications noted below.

### Line Numbers and Code References

All line numbers verified against current source:

- `prompts.py:88` -- confirmed: `"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"`
- `gates.py:523-541` -- confirmed: `EXTRACT_GATE` definition with no `semantic_checks` field
- `release-spec-template.md:28` -- confirmed: `complexity_class: {{SC_PLACEHOLDER:simple_or_moderate_or_high}}`
- `tests/roadmap/test_pipeline_integration.py:86` -- confirmed: `"complexity_class": "moderate"`
- `tests/roadmap/test_executor.py:102` -- confirmed: `"complexity_class": "moderate"`
- `tests/roadmap/test_integration_v5_pipeline.py:91` -- confirmed: `"complexity_class": "moderate"`

### Completeness Assessment

The change set is **complete**. Exhaustive codebase search for `complexity_class` in `src/superclaude/` found exactly the touchpoints listed in the proposal. No additional Python consumers parse the string value. The `executor.py` file has zero references to `complexity_class`.

Historical artifacts in `.dev/releases/complete/` confirm the bug in practice: `v2.24.2` emitted `moderate`, `v2.26` emitted `enterprise`, while `v2.05`/`v2.07`/`v2.08` correctly emitted `MEDIUM`. These are archived outputs and require no changes.

The tasklist protocol (`sc-tasklist-protocol`) references `Complexity Class | LOW|MEDIUM|HIGH` in its templates, confirming alignment with the proposed canonical set.

### Technical Feasibility of Change 2

- `_parse_frontmatter` exists at `gates.py:129` and is used by 10+ existing semantic check functions in the same module.
- `GateCriteria.semantic_checks` field exists at `pipeline/models.py:74` as `list[SemanticCheck] | None = None`.
- The `SemanticCheck` pattern (name + check_fn + failure_message) is well-established with 6+ existing registrations on other gates (e.g., `GENERATE_A_GATE`, `MERGE_GATE`, `SPEC_FIDELITY_GATE`).
- The `.upper()` case-insensitivity approach matches the existing `_certified_is_true` pattern which accepts `True`/`true`.

### Minor Clarifications (not blocking)

1. **Import in test file**: Change 5 mentions adding tests to `tests/roadmap/test_gates_data.py` but does not note that `_complexity_class_valid` must be added to the import block at lines 7-36 of that file. This is implicit but should be called out explicitly in implementation.

2. **Gate-structure test**: After Change 2 adds `semantic_checks` to `EXTRACT_GATE`, a test analogous to `test_generate_gates_have_semantic_checks` (line 70-74) should be added asserting `EXTRACT_GATE.semantic_checks is not None` and `len(EXTRACT_GATE.semantic_checks) == 1`. The proposal's Change 5 covers the semantic check function but not the gate registration assertion.

3. **Gap-4 proposal overlap**: `docs/generated/gap-4-test-strategy-complexity-proposal.md` independently identifies the same enum mismatch and proposes an identical `_complexity_class_valid` function for `TEST_STRATEGY_GATE`. If both proposals are implemented, the function should be defined once and shared across both gates. This is not a problem for Gap-1 alone but should be noted for sequencing.

### Risk Assessment

No risks identified beyond what the proposal already documents. The execution order is correct: fix the source of wrong values first, then add validation, then align docs and tests.

### Verdict

The proposal is accurate, complete, and ready for implementation as written. The three minor clarifications above are implementation details that do not affect the proposal's correctness or scope.
