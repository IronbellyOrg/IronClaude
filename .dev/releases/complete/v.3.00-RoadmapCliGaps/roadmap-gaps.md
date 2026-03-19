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
# Gap #2: `extraction_mode` Enum Mismatch — Implementation Proposal

## Problem Statement

The `extraction_mode` frontmatter field has two contradictory definitions:

| Location | Enum Values | Semantics |
|----------|------------|-----------|
| Source protocol (`refs/templates.md` L414) | `standard\|chunked` | Describes HOW extraction was performed (single-pass vs multi-chunk) |
| CLI extract prompt (`prompts.py` L93) | `full\|partial\|incremental` | Describes HOW MUCH of the spec was extracted (completeness level) |
| CLI extract gate (`gates.py` L537) | (presence only) | Requires field exists but does NOT validate its value |

These are completely different semantic axes. The source protocol tracks extraction **method**, while the CLI prompt requests extraction **completeness**.

## Analysis

### Q1: What does `standard|chunked` mean in the source protocol?

The source protocol defines `extraction_mode` as a **method indicator**:

- **`standard`**: Single-pass extraction used when the spec is under 500 lines (per `SKILL.md` L157 and `extraction-pipeline.md` L185).
- **`chunked`**: Multi-chunk extraction activated when the spec exceeds 500 lines. The value includes chunk count metadata, e.g., `chunked (4 chunks)` (per `extraction-pipeline.md` L357).

This is a well-defined concept tied to a concrete pipeline behavior: the 500-line threshold triggers the chunked extraction protocol, which splits the spec into overlapping chunks, extracts per-chunk, then merges/deduplicates results.

### Q2: Does the CLI pipeline have any chunking logic?

**No.** The CLI roadmap pipeline in `src/superclaude/cli/roadmap/` has no chunking logic whatsoever:

- `prompts.py` builds a single prompt for the extract step with no awareness of spec length.
- `executor.py` invokes Claude once per step with no split/merge machinery.
- There is no 500-line threshold check in the CLI pipeline.

The chunked extraction protocol exists only in the skill-based (interactive) `sc:roadmap` flow defined in `refs/extraction-pipeline.md`. The CLI pipeline always performs a single-pass extraction, making `standard` the only applicable method value for CLI-produced artifacts.

### Q3: Is `full|partial|incremental` used elsewhere in the CLI codebase?

**No** — not as a deliberate enum. The words "full", "partial", and "incremental" appear throughout the CLI codebase in unrelated contexts (e.g., `conflict_detector.py` uses them as completeness heuristic tokens, `cli_portify` has a `PARTIAL` contract status). But `full|partial|incremental` as a defined extraction_mode enum appears **only** in the extract prompt at `prompts.py` L93.

This enum appears to have been invented during the CLI prompt authoring without reference to the source protocol. It has no corresponding validation, no consumer that reads these values, and no documented semantics.

### Q4: What is the correct enum and should the gate validate it?

**The correct enum is `standard|chunked` from the source protocol.** Rationale:

1. **The skill protocol is the source of truth.** The `refs/templates.md` schema is the versioned contract for the extraction.md frontmatter (per NFR-003: "Fields may be added but never removed or renamed"). The CLI is a consumer that should conform to this contract.

2. **`standard` is always correct for CLI-produced extractions.** Since the CLI pipeline has no chunking logic, every CLI extraction is `standard`. The prompt should still communicate the full enum so the LLM understands the field's purpose, but in practice CLI outputs will always be `standard`.

3. **The gate should validate allowed values.** Currently the EXTRACT_GATE only checks presence of the field. Adding a semantic check that validates `extraction_mode` against the allowed enum would catch drift early and enforce contract conformance.

## Proposed Changes

### Change 1: Fix the extract prompt enum (prompts.py L93)

**File**: `src/superclaude/cli/roadmap/prompts.py`
**Line**: 93

**Before**:
```python
"- extraction_mode: (string) one of: full, partial, incremental\n\n"
```

**After**:
```python
"- extraction_mode: (string) one of: standard, chunked — use 'standard' for "
"single-pass extraction, 'chunked (N chunks)' if the spec was processed in chunks\n\n"
```

**Rationale**: Aligns the prompt with the source protocol enum. Provides enough context for the LLM to select correctly. Since the CLI always does single-pass extraction, the LLM should reliably emit `standard`.

### Change 2: Add extraction_mode validation semantic check (gates.py)

**File**: `src/superclaude/cli/roadmap/gates.py`

Add a new semantic check function:

```python
def _extraction_mode_valid(content: str) -> bool:
    """extraction_mode must be 'standard' or start with 'chunked'.

    Accepts: 'standard', 'chunked', 'chunked (N chunks)'.
    Rejects: 'full', 'partial', 'incremental', empty, missing frontmatter.
    """
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    value = fm.get("extraction_mode")
    if value is None:
        return False

    normalized = value.lower().strip()
    if normalized == "standard":
        return True
    if normalized.startswith("chunked"):
        return True
    return False
```

Then register it on EXTRACT_GATE:

```python
EXTRACT_GATE = GateCriteria(
    required_frontmatter_fields=[
        "spec_source",
        "generated",
        "generator",
        "functional_requirements",
        "nonfunctional_requirements",
        "total_requirements",
        "complexity_score",
        "complexity_class",
        "domains_detected",
        "risks_identified",
        "dependencies_identified",
        "success_criteria_count",
        "extraction_mode",
    ],
    min_lines=50,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="extraction_mode_valid",
            check_fn=_extraction_mode_valid,
            failure_message=(
                "extraction_mode must be 'standard' or 'chunked (N chunks)', "
                "not 'full', 'partial', or 'incremental'"
            ),
        ),
    ],
)
```

**Rationale**: Enforces the contract at the gate level. The failure message explicitly names the incorrect values to help diagnose prompt regressions.

### Change 3: No changes to the generate prompt (prompts.py L150)

Line 150 references `extraction_mode` as "extraction completeness indicator" in the generate prompt's context description. This is a minor imprecision (it is an extraction *method* indicator, not a completeness indicator), but it is only a hint to the LLM, not a contract field. Optionally update to:

```python
"- extraction_mode: extraction method indicator (standard or chunked)\n\n"
```

This is low priority and could be bundled with the L93 fix or deferred.

## Impact Assessment

| Dimension | Impact |
|-----------|--------|
| Breaking change? | No — `extraction_mode` field name is unchanged; only the allowed values change |
| Existing artifacts? | Existing extraction.md files with `full`/`partial`/`incremental` would fail the new gate. This is desirable — they were produced from a non-conformant prompt |
| Source protocol alignment? | Full alignment after changes |
| Test impact? | Any tests mocking extraction output with `extraction_mode: full` need updating to `extraction_mode: standard` |
| Downstream consumers? | The generate prompt (L150) reads extraction_mode as advisory context; it does not branch on the value. No downstream consumer logic is affected |

## Test Plan

1. Unit test `_extraction_mode_valid` with inputs:
   - `"standard"` -> True
   - `"chunked"` -> True
   - `"chunked (4 chunks)"` -> True
   - `"full"` -> False
   - `"partial"` -> False
   - `"incremental"` -> False
   - `""` (empty) -> False
   - Missing field -> False
   - Missing frontmatter -> False
2. Integration test: run extract step with the updated prompt and verify the output frontmatter contains `extraction_mode: standard`.
3. Grep for any test fixtures using `extraction_mode: full` or `extraction_mode: partial` and update them.

## Files to Modify

| File | Change |
|------|--------|
| `src/superclaude/cli/roadmap/prompts.py` | L93: Replace `full\|partial\|incremental` with `standard\|chunked` and add description |
| `src/superclaude/cli/roadmap/gates.py` | Add `_extraction_mode_valid` function; add SemanticCheck to EXTRACT_GATE |
| `src/superclaude/cli/roadmap/prompts.py` | L150 (optional): Update context hint from "completeness indicator" to "method indicator" |

## Recommendation

**Implement Changes 1 and 2 together as a single commit.** Change 3 is optional polish. The semantic check in Change 2 provides a regression safety net — if anyone re-introduces the wrong enum values in the prompt, the gate will catch it during pipeline execution rather than silently producing non-conformant artifacts.

---

## Validation Result

**Status: PASS WITH CORRECTIONS**

Independent review validated the proposal on 2026-03-18 against the actual codebase. The analysis is sound, the line number references are accurate, and the proposed changes are correct. However, the "Files to Modify" table is incomplete -- it omits test files and benchmark fixtures that use the old enum values. Corrections are documented below.

### Verification of Line Number and Code References

All line references checked and confirmed accurate:

| Claim | Actual | Status |
|-------|--------|--------|
| `prompts.py` L93: `full, partial, incremental` | Line 93 confirmed | PASS |
| `prompts.py` L150: `extraction completeness indicator` | Line 150 confirmed | PASS |
| `gates.py` L537: `extraction_mode` in required fields | Line 537 confirmed | PASS |
| `templates.md` L414: `standard\|chunked` | Line 414 confirmed | PASS |
| `SKILL.md` L157: 500-line threshold | Line 157 confirmed | PASS |
| `extraction-pipeline.md` L185: threshold definition | Line 185 confirmed | PASS |
| `extraction-pipeline.md` L357: chunked metadata example | Line 357 confirmed | PASS |
| EXTRACT_GATE has no semantic_checks | Confirmed (L522-541: only `required_frontmatter_fields` and `min_lines`) | PASS |
| `_parse_frontmatter` helper exists for reuse | Confirmed at gates.py L129 | PASS |

### Gate Semantic Check Validation

The proposed `_extraction_mode_valid` function correctly handles the "chunked (N chunks)" variant via `startswith("chunked")`. This approach is robust because:
- `"chunked"` alone passes (bare value)
- `"chunked (4 chunks)"` passes (variant with metadata)
- `"chunked (12 chunks)"` passes (any chunk count)
- No false positives from unrelated strings beginning with "chunked" are realistic in this domain

### CLI Chunking Logic Confirmation

Confirmed: no chunking logic exists in `src/superclaude/cli/roadmap/`. The 500-line threshold and multi-chunk extraction protocol exist only in the skill-based flow (`refs/extraction-pipeline.md`). CLI-produced artifacts will always be `standard`.

## Refactoring Notes

### CORRECTION 1: Missing Test Files in "Files to Modify"

The proposal's test plan (item 3) correctly instructs to "grep for any test fixtures using `extraction_mode: full`", but the "Files to Modify" table omits the specific files. Three test files contain `extraction_mode: "full"` in mock data and must be updated:

| File | Line | Current Value | Required Change |
|------|------|---------------|-----------------|
| `tests/roadmap/test_executor.py` | 107 | `"extraction_mode": "full"` | Change to `"extraction_mode": "standard"` |
| `tests/roadmap/test_pipeline_integration.py` | 91 | `"extraction_mode": "full"` | Change to `"extraction_mode": "standard"` |
| `tests/roadmap/test_integration_v5_pipeline.py` | 96 | `"extraction_mode": "full"` | Change to `"extraction_mode": "standard"` |

These are **required** changes, not optional -- if the new semantic check is added to EXTRACT_GATE and the test fixtures still emit `"full"`, any integration test that validates extraction output through the gate will fail.

### CORRECTION 2: Missing Benchmark Fixtures

13 benchmark extraction.md files under `.dev/benchmarks/v2.20-baseline/outputs/` contain `extraction_mode: full`. These are historical pipeline output snapshots. The proposal should document a decision on these:

- **Option A (recommended)**: Update them to `extraction_mode: standard` so benchmark re-runs against the new gate pass.
- **Option B**: Leave them as-is and accept that benchmark comparisons against the new gate will show regressions (the regressions are expected and correct).

The proposal's impact assessment row "Existing artifacts?" covers this conceptually but does not enumerate the specific benchmark files.

### CORRECTION 3: Existing Release Artifact

One existing release artifact uses the correct protocol value: `.dev/releases/complete/unified-audit-gating-v1.2.1/extraction.md` contains `extraction_mode: "chunked (4 chunks)"`. This confirms the skill-based flow already produces correct values. No change needed for this file, but it serves as a positive control for the `startswith("chunked")` check.

### NOTE: Sister Proposal Coordination

A parallel proposal exists at `docs/generated/gap-1-complexity-class-enum-proposal.md` addressing the `complexity_class` enum mismatch in the same file (`prompts.py` L88). Both proposals modify the extract prompt in `prompts.py` and add semantic checks to `gates.py`. Implementers should apply both proposals in the same commit or consecutive commits to avoid merge conflicts.

### Updated Files to Modify (Complete)

| File | Change | Priority |
|------|--------|----------|
| `src/superclaude/cli/roadmap/prompts.py` | L93: Replace `full\|partial\|incremental` with `standard\|chunked` and add description | Required |
| `src/superclaude/cli/roadmap/gates.py` | Add `_extraction_mode_valid` function; add SemanticCheck to EXTRACT_GATE | Required |
| `tests/roadmap/test_executor.py` | L107: `"full"` -> `"standard"` | Required |
| `tests/roadmap/test_pipeline_integration.py` | L91: `"full"` -> `"standard"` | Required |
| `tests/roadmap/test_integration_v5_pipeline.py` | L96: `"full"` -> `"standard"` | Required |
| `src/superclaude/cli/roadmap/prompts.py` | L150: Update context hint from "completeness indicator" to "method indicator" | Optional |
| `.dev/benchmarks/v2.20-baseline/outputs/*/extraction.md` (13 files) | `extraction_mode: full` -> `extraction_mode: standard` | Recommended |
# Gap #3: `domains_detected` Type Change -- Implementation Proposal

## Problem Statement

The source protocol in `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` (line 408) defines `domains_detected` as a **YAML array of domain names**:

```yaml
domains_detected: [<domain1>, <domain2>]
```

The CLI extract prompt in `src/superclaude/cli/roadmap/prompts.py` (line 89) requests it as an **integer count**:

```
- domains_detected: (integer) count of distinct technical domains identified
```

The generate prompt (line 146) references it ambiguously as:

```
- domains_detected: number of technical domains to address
```

This means domain identity is lost at extraction time, which has downstream consequences.

---

## Analysis of the Four Key Questions

### 1. Does the CLI pipeline currently do any template matching that needs domain names?

**No -- not in the Python CLI code.** The CLI pipeline (`prompts.py`, `gates.py`, executor) does not perform template compatibility scoring in Python. The template matching logic lives entirely in the skill protocol (`refs/scoring.md`, `refs/templates.md`) and is executed by the LLM as part of the sc:roadmap skill's Wave 2 (Planning & Template Selection).

However, the **source protocol's template compatibility scoring** uses domain names directly. From `refs/scoring.md` line 69:

> `domain_match` (weight 0.40): Jaccard similarity between template's `domains` field and spec's detected domains

This is the highest-weighted factor in template scoring. It requires actual domain names (e.g., `[backend, security]`) to compute Jaccard similarity against a template's `domains: [backend, performance]` field. An integer count cannot participate in set intersection/union.

The **milestone count formula** in `refs/templates.md` line 93 also uses domain count:

> `base + floor(domain_count / 2)`

This only needs a count, but the domain-specific milestone mapping (lines 99-109) needs domain names to determine milestone types (e.g., "security" domain generates a SECURITY-type milestone).

**Conclusion**: The skill protocol needs domain names. The CLI pipeline currently only validates field presence, not content, so it is agnostic to type.

### 2. Would changing from integer to array break the gate's frontmatter validation?

**No.** The `EXTRACT_GATE` in `gates.py` (line 523-541) lists `domains_detected` in `required_frontmatter_fields`. The gate validation in `src/superclaude/cli/pipeline/gates.py` only checks **field presence** -- it looks for `domains_detected:` as a key in the YAML frontmatter and verifies the key exists. It does not parse or validate the value type.

The `_check_frontmatter` function (pipeline `gates.py` lines 78-108) splits on `:` and checks if the key name appears. Both formats produce a valid `key: value` line:

- `domains_detected: 3` -- key `domains_detected` found
- `domains_detected: [backend, security, frontend]` -- key `domains_detected` found

The `_frontmatter_values_non_empty` semantic check (roadmap `gates.py` line 101-119) splits on `:` and checks that the value portion is non-empty. Both `3` and `[backend, security, frontend]` are non-empty strings after the colon.

**No existing semantic check inspects the value of `domains_detected`.**

**Conclusion**: Changing the type will not break any gate.

### 3. How does the generate prompt reference domains_detected -- does it expect a count or names?

The generate prompt (`build_generate_prompt`, line 146) says:

```
- domains_detected: number of technical domains to address
```

This is informational context for the LLM generating the roadmap. It tells the LLM "here is what this field means" so it can reference the extraction frontmatter. If `domains_detected` becomes an array, the LLM can still count it and additionally use the domain names for richer roadmap generation (e.g., creating domain-specific sections).

The generate prompt does not parse the value programmatically -- it just passes the extraction document as a `--file` input to Claude, which reads the frontmatter natively.

**Conclusion**: The generate prompt's description should be updated to match, but the LLM will handle either format gracefully.

### 4. What's the right balance between fidelity and simplicity for the CLI context?

**Recommendation: Change to array format, matching the source protocol.**

Rationale:

- **Fidelity to source of truth**: The protocol spec (`templates.md`) is the contract. The CLI is a consumer. The consumer should match the contract.
- **Zero gate breakage**: As analyzed above, no gate validation inspects the value type.
- **Domain identity enables richer downstream use**: Even in CLI-only mode (no skill protocol), domain names let the generate step produce domain-aware roadmaps. An integer `3` tells the LLM nothing about *which* domains matter.
- **Existing precedent**: Historical extraction outputs already use array format in many releases (v2.01 through v2.13, unified-audit-gating, v4.xx-SprintReportScaffolding). The integer format only appeared after the v2.17 reliability release introduced the CLI prompts.
- **Benchmark evidence**: The v2.20 baseline test-3-cascade validation explicitly flagged this as a defect: `"FR-006 requires a domain list. Found domains_detected: 7 (a count, not a list)."` (line 44 of full grep results).
- **Test impact is minimal**: Only 3 test files use integer format for `domains_detected` and need updating.

---

## Implementation Plan

### Change 1: Update extract prompt (prompts.py line 89)

**File**: `src/superclaude/cli/roadmap/prompts.py`

**Current** (line 89):
```python
"- domains_detected: (integer) count of distinct technical domains identified\n"
```

**Proposed**:
```python
"- domains_detected: (list) array of distinct technical domain names identified, e.g. [backend, security, frontend]\n"
```

### Change 2: Update generate prompt (prompts.py line 146)

**File**: `src/superclaude/cli/roadmap/prompts.py`

**Current** (line 146):
```python
"- domains_detected: number of technical domains to address\n"
```

**Proposed**:
```python
"- domains_detected: list of technical domain names to address\n"
```

### Change 3: Update test fixtures (3 files)

**File**: `tests/roadmap/test_integration_v5_pipeline.py` (line 92)
```python
# Current
"domains_detected": "3",
# Proposed
"domains_detected": "[backend, security, frontend]",
```

**File**: `tests/roadmap/test_pipeline_integration.py` (line 87)
```python
# Current
"domains_detected": "2",
# Proposed
"domains_detected": "[backend, frontend]",
```

**File**: `tests/roadmap/test_executor.py` (line 103)
```python
# Current
"domains_detected": "2",
# Proposed
"domains_detected": "[backend, frontend]",
```

### No changes needed

- **`gates.py`**: `EXTRACT_GATE` lists `domains_detected` in `required_frontmatter_fields` -- this is correct for both types (presence-only check).
- **Pipeline `gates.py`**: `_check_frontmatter` is type-agnostic. No change needed.
- **`_frontmatter_values_non_empty`**: Works with both types (checks non-empty string after colon).
- **Source protocol `templates.md`**: Already correct -- it defines the array format.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| LLM produces integer instead of array despite prompt change | LOW | The prompt explicitly shows example format `[backend, security, frontend]`. LLMs follow examples well. If it does produce an integer, gates still pass (presence-only). |
| Downstream consumer expects integer | LOW | The generate prompt is the only downstream consumer, and it's updated in Change 2. No Python code parses the value. |
| Test breakage from fixture changes | LOW | Exactly 3 test files need updating. Changes are straightforward string replacements. |
| YAML parsing of inline arrays | LOW | YAML natively supports `[a, b, c]` flow sequence syntax. The frontmatter parser in `gates.py` treats all values as strings after the colon, so `[backend, security, frontend]` is valid. |

---

## Scope

- **Files modified**: 4 (1 source, 3 tests)
- **Lines changed**: ~6
- **Risk level**: Low
- **Breaking changes**: None
- **Gate impact**: None

---

## Validation Plan

1. Run `uv run pytest tests/roadmap/test_gates_data.py -v` -- confirms `domains_detected` still in EXTRACT_GATE required fields
2. Run `uv run pytest tests/roadmap/test_integration_v5_pipeline.py -v` -- confirms updated fixtures pass
3. Run `uv run pytest tests/roadmap/test_pipeline_integration.py -v` -- confirms updated fixtures pass
4. Run `uv run pytest tests/roadmap/test_executor.py -v` -- confirms updated fixtures pass
5. Run `make test` -- full suite regression

---

## Validation Result

**Status: PASS -- proposal is sound, with minor clarifications added below.**

Validated 2026-03-18 by automated review against source files at HEAD of `v3.0-AuditGates`.

### 1. Line numbers and code references: ACCURATE

All line references verified against source:

| Claim | File | Claimed Line | Actual Line | Match |
|-------|------|-------------|-------------|-------|
| Extract prompt `domains_detected` | `src/superclaude/cli/roadmap/prompts.py` | 89 | 89 | Yes |
| Generate prompt `domains_detected` | `src/superclaude/cli/roadmap/prompts.py` | 146 | 146 | Yes |
| `EXTRACT_GATE` definition | `src/superclaude/cli/roadmap/gates.py` | 523-541 | 523-541 | Yes |
| `_check_frontmatter` function | `src/superclaude/cli/pipeline/gates.py` | 78-108 | 78-108 | Yes |
| `_frontmatter_values_non_empty` | `src/superclaude/cli/roadmap/gates.py` | 101-119 | 101-119 | Yes |
| Test fixture `test_integration_v5_pipeline.py` | `tests/roadmap/` | 92 | 92 | Yes |
| Test fixture `test_pipeline_integration.py` | `tests/roadmap/` | 87 | 87 | Yes |
| Test fixture `test_executor.py` | `tests/roadmap/` | 103 | 103 | Yes |
| Protocol `templates.md` `domains_detected` | `src/superclaude/skills/sc-roadmap-protocol/refs/` | 408 | 408 | Yes |
| Protocol `scoring.md` `domain_match` | `src/superclaude/skills/sc-roadmap-protocol/refs/` | 69 | 69 | Yes |

### 2. Frontmatter parser handling of YAML arrays: SAFE

The `_check_frontmatter` function in `src/superclaude/cli/pipeline/gates.py` (lines 78-108) uses regex `_FRONTMATTER_RE` to extract frontmatter, then splits each line on `:` taking `key = line.split(":", 1)[0]`. For `domains_detected: [backend, security, frontend]`, this correctly extracts key `domains_detected`. The value portion is never inspected for type.

The `_parse_frontmatter` function in `src/superclaude/cli/roadmap/gates.py` (lines 129-149) similarly splits on `:` with `line.split(":", 1)` and stores the value as a string. For `[backend, security, frontend]`, the string value is non-empty and no code attempts `int()` conversion on it.

The `_frontmatter_values_non_empty` semantic check (lines 101-119) checks `if not value.strip()` -- `[backend, security, frontend]` is non-empty, so this passes.

The `EXTRACT_GATE` has `enforcement_tier="STRICT"` but defines **no `semantic_checks`**, so no value-type inspection runs on extraction output.

**Risk note**: The `_FRONTMATTER_RE` regex requires each frontmatter line to match `\w[\w\s]*:.*` (key-colon-value on a single line). The YAML block-sequence format (multiline with `- item` per line) would break this regex. However, the proposed prompt explicitly instructs inline/flow-sequence format (`e.g. [backend, security, frontend]`) which stays on one line, mitigating this risk. This is consistent with how the proposal already handles it.

### 3. Generate prompt reference: CONFIRMED needs updating

The generate prompt at line 146 says `"number of technical domains to address"` which implies integer semantics. The proposal correctly identifies this as needing an update to `"list of technical domain names to address"`.

### 4. Downstream consumers parsing as integer: NONE FOUND

Searched all files under `src/` and `tests/` for `domains_detected`. No code path calls `int()` on the `domains_detected` value. The only consumers are:

- **Gate presence check** (`_check_frontmatter`): type-agnostic, checks key existence only.
- **`_frontmatter_values_non_empty`**: checks non-empty string, type-agnostic.
- **Generate prompt description** (line 146): informational text for LLM, no parsing.
- **Test fixtures** (3 files): string values in dicts, used to construct frontmatter for gate tests. These need updating as proposed.
- **`test_gates_data.py`** (line 57): asserts `"domains_detected" in EXTRACT_GATE.required_frontmatter_fields` -- checks field name presence, not value. No change needed.

### 5. YAML array format parseability: CONFIRMED SAFE

The simple `:` split in `_parse_frontmatter` (`line.split(":", 1)`) handles `domains_detected: [backend, security, frontend]` correctly because it splits only on the first colon. The value `[backend, security, frontend]` is stored as-is as a string. No downstream code attempts to parse it as YAML or convert to a Python list.

### Additional finding: `test_gates_data.py`

The proposal lists 3 test files needing changes. A 4th test file (`tests/roadmap/test_gates_data.py`, line 57) references `domains_detected` but only checks field name presence in `EXTRACT_GATE.required_frontmatter_fields` -- no value change needed. The proposal correctly omits this file from the change list.

### Conclusion

The proposal is complete, accurate, and safe to implement as written. No corrections required.
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
# Gap #5 — Test-Strategy Missing Provenance Fields: Implementation Proposal

## Problem Statement

The source protocol's `test-strategy.md` frontmatter schema (defined in `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md`) specifies three provenance fields:

```yaml
spec_source: <path>
generated: <ISO-8601 timestamp>
generator: sc:roadmap
```

The CLI's `build_test_strategy_prompt()` in `prompts.py` only requests `validation_milestones` and `interleave_ratio`. The `TEST_STRATEGY_GATE` in `gates.py` likewise only validates those two fields. The provenance triple (`spec_source`, `generated`, `generator`) is entirely absent from both the prompt and the gate.

**Severity**: LOW -- these are metadata fields that do not affect correctness of the test strategy content itself. However, they are important for artifact traceability and audit trails.

---

## Analysis

### Question 1: Claude-produced vs. executor-injected?

**Recommendation: Executor-injected.** Three reasons:

1. **Precedent exists.** The executor already injects `pipeline_diagnostics` into the extraction step's frontmatter post-subprocess via `_inject_pipeline_diagnostics()` (lines 123-157 of `executor.py`). The pattern is proven. **Note**: The existing function uses plain `write_text()`, not atomic write (see Refactoring Notes).

2. **The LLM cannot reliably produce these values.** `generated` requires the real wall-clock timestamp of when the step completed (not when Claude "thinks" it is). `generator` is a fixed string (`sc:roadmap`) that the LLM might hallucinate variants of. `spec_source` is the original spec filename, which the executor already tracks as `config.spec_file`.

3. **Prompt simplicity.** Adding three more frontmatter instructions to the prompt increases token cost (~80 tokens) on every invocation for fields that are deterministic and known to the executor. The extract step already asks Claude to produce `spec_source`/`generated`/`generator`, and that works because Claude has direct access to the spec file content. For test-strategy, Claude doesn't see the original spec -- it sees the roadmap and extraction, so it would have to parrot a `spec_source` value from nested frontmatter, introducing a propagation-error risk.

### Question 2: Where in the pipeline code would injection happen?

In `roadmap_run_step()` in `executor.py`, immediately after the existing extract-step injection block (lines 256-258). The pattern would be:

```python
# Inject executor-populated fields into extract step frontmatter (FR-033)
if step.id == "extract" and step.output_file.exists():
    _inject_pipeline_diagnostics(step.output_file, started_at, finished_at)

# Inject provenance fields into test-strategy frontmatter
if step.id == "test-strategy" and step.output_file.exists():
    _inject_provenance_fields(
        step.output_file,
        spec_source=config.spec_file.name if hasattr(config, "spec_file") else "unknown",
        finished_at=finished_at,
    )
```

A new function `_inject_provenance_fields()` would:
1. Read the output file
2. Verify it starts with `---` (frontmatter present)
3. Find the closing `---` delimiter
4. Insert the three provenance lines before the closing delimiter
5. Write back to the file (plain `write_text()`, matching the existing `_inject_pipeline_diagnostics()` pattern)

This mirrors `_inject_pipeline_diagnostics()` exactly. **Note**: The existing pattern uses non-atomic `write_text()`. The proposed implementation below upgrades to atomic write (tmp + `os.replace()`), which is an improvement over the precedent but not strictly necessary for consistency. Either approach is acceptable; see Refactoring Notes.

### Question 3: Should the gate validate these fields regardless of who produces them?

**Yes.** The gate should validate presence of provenance fields regardless of their source. This is the defense-in-depth principle: if executor injection fails silently (e.g., file write error, frontmatter parsing edge case), the gate catches it.

However, since the gap is LOW severity and the test-strategy gate is `STANDARD` tier (not `STRICT`), adding the fields to `required_frontmatter_fields` is sufficient. No semantic checks are needed -- the existing `_frontmatter_values_non_empty` check can be optionally added but is not strictly necessary given that the executor produces deterministic non-empty values.

### Question 4: Tradeoff between prompt complexity and artifact completeness

| Approach | Prompt tokens | Reliability | Traceability |
|----------|--------------|-------------|--------------|
| Prompt-only | +~80 tokens/call | Medium (LLM may hallucinate `generator`, get `generated` wrong) | Full (if LLM complies) |
| Executor-only | +0 tokens | High (deterministic values) | Full |
| Both (prompt + executor override) | +~80 tokens/call | Highest (redundant) | Full |

**Winner: Executor-only.** Zero prompt overhead, highest reliability, and the precedent is already established in the codebase.

---

## Implementation Plan

### Changes Required

#### 1. `src/superclaude/cli/roadmap/executor.py`

Add a new function `_inject_provenance_fields()` and call it from `roadmap_run_step()`.

```python
def _inject_provenance_fields(
    output_file: Path,
    spec_source: str,
    finished_at: datetime,
) -> None:
    """Inject spec_source, generated, and generator into step frontmatter.

    These provenance fields are deterministic metadata the executor knows
    but the LLM cannot reliably produce. Uses atomic write.
    """
    import os

    content = output_file.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return

    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return

    provenance_lines = (
        f"spec_source: {spec_source}\n"
        f"generated: \"{finished_at.isoformat()}\"\n"
        f"generator: sc:roadmap"
    )

    new_content = (
        content[:end_idx]
        + "\n"
        + provenance_lines
        + content[end_idx:]
    )

    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(new_content, encoding="utf-8")
    os.replace(tmp_file, output_file)
```

In `roadmap_run_step()`, after line 258:

```python
# Inject provenance fields into test-strategy frontmatter
if step.id == "test-strategy" and step.output_file.exists():
    _inject_provenance_fields(
        step.output_file,
        spec_source=config.spec_file.name if hasattr(config, "spec_file") else "unknown",
        finished_at=finished_at,
    )
```

**Note on `config` type**: `roadmap_run_step` receives `config: PipelineConfig`, but at runtime it is always a `RoadmapConfig` (which has `spec_file`). The `hasattr` guard is defensive. Alternatively, the function signature could accept `RoadmapConfig` directly, but that would change the `StepRunner` protocol. The safer approach is the `hasattr` guard or a downcast with `isinstance`.

#### 2. `src/superclaude/cli/roadmap/gates.py`

Update `TEST_STRATEGY_GATE` to include the provenance fields:

```python
TEST_STRATEGY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "spec_source",
        "generated",
        "generator",
        "validation_milestones",
        "interleave_ratio",
    ],
    min_lines=40,
    enforcement_tier="STANDARD",
)
```

#### 3. No prompt changes needed

`build_test_strategy_prompt()` remains unchanged. The provenance fields are not requested from Claude.

### Additional Template Fields Not Addressed

The template schema also includes fields not in the current gate or prompt:

- `validation_philosophy: continuous-parallel` -- fixed value, could be executor-injected
- `work_milestones: <count>` -- content-dependent, would need prompt addition
- `major_issue_policy: stop-and-fix` -- fixed value, could be executor-injected
- `complexity_class: <LOW|MEDIUM|HIGH>` -- available from extraction, could be executor-injected

These are out of scope for this gap but noted for future alignment work.

### Test Plan

1. **Unit test for `_inject_provenance_fields()`**: Create a temp file with valid frontmatter, call the function, verify `spec_source`, `generated`, and `generator` are present in the output.
2. **Unit test for missing frontmatter**: Verify function is a no-op when file has no `---` delimiters.
3. **Unit test for gate**: Verify `TEST_STRATEGY_GATE.required_frontmatter_fields` includes all five fields.
4. **Integration test**: Run a dry-run pipeline step and verify the gate definition includes provenance fields.

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Injection fails silently (no frontmatter in output) | Low | Low | Gate catches missing fields |
| `config` lacks `spec_file` attribute | Very Low | Low | `hasattr` guard with fallback |
| Existing tests break due to gate field additions | Medium | Low | Update test fixtures to include provenance fields |
| Atomic write fails (disk full, permissions) | Very Low | Medium | Exception propagates, step fails, retry handles it |

### Effort Estimate

- Implementation: ~30 minutes (one new function, two line changes)
- Tests: ~20 minutes (three unit tests)
- Total: ~50 minutes

---

## Decision Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Who produces provenance? | Executor | Deterministic values, zero prompt overhead, existing precedent |
| Injection point | `roadmap_run_step()` after sanitize | Mirrors existing `_inject_pipeline_diagnostics` pattern |
| Gate validation? | Yes, add to `required_frontmatter_fields` | Defense-in-depth; catches injection failures |
| Semantic checks needed? | No | Values are deterministic; field-presence check is sufficient |
| Prompt changes? | None | Avoids token waste and LLM hallucination risk |

---

## Refactoring Notes

The following corrections were applied during code-level validation (2026-03-18):

### RN-1: Atomic write claim is inaccurate for the precedent function

**Issue**: The proposal stated that `_inject_pipeline_diagnostics()` is "atomic-write-safe" and uses tmp + `os.replace()`. This is incorrect. The actual implementation at line 157 of `executor.py` uses plain `output_file.write_text(new_content, encoding="utf-8")` -- a non-atomic write. Only `_sanitize_output()` (line 82) uses the atomic tmp + `os.replace()` pattern.

**Impact**: Low. The claim that the new function "mirrors `_inject_pipeline_diagnostics()` exactly" was misleading. The proposed `_inject_provenance_fields()` implementation actually upgrades to atomic write, which is a minor improvement over the precedent. Both approaches are acceptable since the file is not read concurrently during this phase.

**Resolution**: Updated the Analysis section (Questions 1 and 2) to accurately describe the existing write pattern. The proposed implementation retains atomic write as an improvement, but implementers may also use plain `write_text()` for strict consistency with the precedent.

### RN-2: Question 2 call-site signature mismatch (corrected)

**Issue**: The inline code in Question 2 showed `_inject_provenance_fields(step.output_file, config, finished_at)` but the function signature takes `spec_source: str`, not `config`. The Implementation Plan section had the correct call with `spec_source=config.spec_file.name`.

**Impact**: Cosmetic. Would cause confusion for implementers reading the Analysis section before the Implementation Plan.

**Resolution**: Updated the Question 2 code block to match the Implementation Plan's correct call-site pattern with `spec_source=` keyword argument and `hasattr` guard.

### RN-3: Execution order validation -- injection before gate is confirmed correct

**Verified**: The proposal's injection point (inside `roadmap_run_step()` at line 258, before the function returns `StepResult` with `StepStatus.PASS` at line 261) is correct. Gate checks run AFTER `roadmap_run_step()` returns, in `execute_pipeline._execute_step_with_retry()` at line 210 of `pipeline/executor.py`. Therefore:

1. `roadmap_run_step()` runs the subprocess, sanitizes output, injects fields, returns PASS
2. `_execute_step_with_retry()` receives the result, then calls `gate_passed()` on the output file

Adding `spec_source`, `generated`, and `generator` to `TEST_STRATEGY_GATE.required_frontmatter_fields` will NOT cause gate failures, because the fields are injected before the gate runs.

### RN-4: All line number references verified accurate

- `_inject_pipeline_diagnostics()`: lines 123-157 -- confirmed
- `roadmap_run_step()`: line 160 -- confirmed
- Extract injection block: lines 256-258 -- confirmed
- `RoadmapConfig.spec_file`: line 94 of `models.py` -- confirmed

## Validation Result

**PASS** -- The proposal is structurally sound. The core architectural decisions (executor-injected provenance, injection point after sanitize/before gate return, gate field additions) are all correct and verified against the actual source code. The four issues identified above (RN-1 through RN-4) are minor: one factual inaccuracy about atomic writes, one cosmetic signature mismatch, and two confirmations of correctness. All corrections have been applied inline.
