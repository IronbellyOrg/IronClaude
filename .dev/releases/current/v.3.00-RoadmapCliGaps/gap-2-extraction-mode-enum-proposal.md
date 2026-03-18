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
