# Refactoring Plan: Hybrid Merge for Obligation Scanner False Positive Mitigation

**Date**: 2026-04-03
**Base Variant**: A (Brainstorm/Composite)
**Donor Variants**: B (Design/Classifier), C (Improve/Minimal)
**Output**: Merged proposal integrating selected strengths from all variants

---

## Non-Base Strengths Being Incorporated

### 1. Severity Model: MEDIUM for Meta-Context
- **Source Variant**: C (Improve/Minimal)
- **Target Location in Base**: Integration point in `scan_obligations()`, Layer 2 classification result handling
- **Rationale**: Variant A proposed full exemption (`exempt=True`) for meta-context, which would hide obligations from reports entirely. Variant C's MEDIUM demotion is more conservative—meta-context obligations are still visible in reports but excluded from `undischarged_count`. This maintains transparency while solving the false positive blocking issue.
- **Integration Approach**: Change Layer 2 result from `exempt=True` to `severity="MEDIUM"`. Update `ObligationReport.undischarged_count` property to exclude MEDIUM (already the case—no change needed).

### 2. Scaffold-Aware Inline Code Regex
- **Source Variant**: B (Design/Classifier)
- **Target Location in Base**: Layer 1b (inline code detection)
- **Rationale**: Variant A proposed a generic `_is_inside_inline_code()` function using `_INLINE_CODE_RE = re.compile(r"`[^`]+`")` and positional checks. Variant B's scaffold-aware regex `_INLINE_CODE_RE = re.compile(r"`[^`]*(?:" + "|".join(SCAFFOLD_TERMS) + r")[^`]*`", re.IGNORECASE)` is more precise—it only matches backtick spans that actually contain scaffold terms, reducing false positives from unrelated inline code.
- **Integration Approach**: Replace A's generic inline code detection with B's scaffold-aware regex pattern. Remove the need for positional span calculation.

### 3. Edge Case Catalog Structure (E1-E20)
- **Source Variant**: B (Design/Classifier)
- **Target Location in Base**: New "Edge Case Catalog" section in merged proposal
- **Rationale**: Variant A has 10 edge cases discussed narratively. Variant B provides a structured table format (E1-E20) with explicit inputs, expected outputs, and classification layers. This format is more testable and reviewable.
- **Integration Approach**: Adapt B's E1-E20 catalog to the hybrid approach. Update severity expectations from INFO (in B) to MEDIUM (per hybrid decision). Add provenance annotations showing which cases changed.

### 4. Parameterized Test Format
- **Source Variant**: B (Design/Classifier)
- **Target Location in Base**: Test plan section, unit tests for `_is_meta_context()`
- **Rationale**: Variant A describes tests narratively. Variant B provides concrete `@pytest.mark.parametrize` code showing exactly how to test each edge case. This reduces implementation ambiguity.
- **Integration Approach**: Adopt B's parameterized test style for `_is_meta_context()` unit tests. Use the adapted E1-E20 catalog as the test matrix.

### 5. Completed Checklist Detection
- **Source Variant**: B (Design/Classifier)
- **Target Location in Base**: Layer 1 (structural exclusions)
- **Rationale**: Variant B identified completed checklist items (`- [x]`) as a distinct meta-context category not explicitly covered in Variant A. This is a valuable addition for gate criteria sections.
- **Integration Approach**: Add `_COMPLETED_CHECKLIST_RE` regex to Layer 1. When matched, set severity to MEDIUM.

### 6. Integration Test Class Structure
- **Source Variant**: B (Design/Classifier)
- **Target Location in Base**: Test plan section
- **Rationale**: Variant B's `TestMetaContextFalsePositiveSuppression` class provides a clear pattern for integration testing. Variant A lacks this structure.
- **Integration Approach**: Include B's integration test class, adapted for MEDIUM severity expectations.

### 7. Consolidated Negation Regex
- **Source Variant**: C (Improve/Minimal) with patterns from A
- **Target Location in Base**: Layer 2 negation patterns
- **Rationale**: Variant C uses a single consolidated `_NEGATION_PREFIX_RE` instead of A's list of separate patterns. This is more maintainable. However, C's pattern is monolithic and harder to read. The hybrid approach uses a single compiled regex but with clear pattern structure borrowed from A's categorization.
- **Integration Approach**: Create a single `_NEGATION_PREFIX_RE` that combines all negation patterns from A's `_META_CONTEXT_INDICATORS` with C's shell command detection, organized by comment blocks for readability.

---

## Base Weaknesses Being Fixed

### 1. Full Exemption for Meta-Context (Too Aggressive)
- **Issue**: Variant A proposed setting `exempt=True` for meta-context matches, which would hide them entirely from reports.
- **Better Variant Reference**: C (MEDIUM demotion)
- **Fix Approach**: Change Layer 2 to set `severity="MEDIUM"` instead of `exempt=True`. This preserves visibility in reports while excluding from `undischarged_count`.

### 2. Vague Proximity Window Fix
- **Issue**: Variant A mentions a "4-word proximity window" fix for double negation but doesn't provide concrete implementation.
- **Better Variant Reference**: B (explicit 4-word window in `_NEGATION_PREFIXES`)
- **Fix Approach**: Adopt B's explicit `(?:\w+\s+){0,4}` pattern structure for word-window limiting. This is concrete and testable.

### 3. Risk Description Handling Contradiction
- **Issue**: Variant A's edge case #7 says "Risk: placeholder data could leak" should be exempted, but the composite approach doesn't explicitly include risk patterns in `_META_CONTEXT_INDICATORS`.
- **Better Variant Reference**: C (explicit risk/warning patterns in `_NEGATION_PREFIX_RE`)
- **Fix Approach**: Include risk/warning patterns in the consolidated negation regex. Per hybrid decision, risk descriptions are demoted to MEDIUM (not HIGH as in B, not exempt as in A).

### 4. Missing Completed Checklist Category
- **Issue**: Variant A's 6 categories don't include completed checklist items (`- [x]`), which are clearly meta-context.
- **Better Variant Reference**: B (Layer 1b: Completed checklist)
- **Fix Approach**: Add `_COMPLETED_CHECKLIST_RE` to Layer 1.

### 5. Generic Inline Code Detection
- **Issue**: Variant A's `_is_inside_inline_code()` uses generic backtick matching, which could match unrelated inline code.
- **Better Variant Reference**: B (scaffold-aware inline code regex)
- **Fix Approach**: Use B's scaffold-aware pattern that only matches backtick spans containing scaffold terms.

### 6. Missing Formal Test Plan
- **Issue**: Variant A discusses tests narratively but lacks a formal test plan section with concrete test cases.
- **Better Variant Reference**: B (comprehensive test plan with parameterized tests, integration tests, regression tests)
- **Fix Approach**: Adopt B's test plan structure, adapted to the hybrid approach.

### 7. No Data Flow Diagram
- **Issue**: Variant A describes the integration point but lacks a visual data flow diagram.
- **Better Variant Reference**: B (Section 2.4 Data Flow with ASCII diagram)
- **Fix Approach**: Include an adapted data flow diagram showing the 2-layer hybrid approach.

---

## Changes NOT Being Made (With Rationale)

### 1. INFO Severity Level (from B)
- **Rationale**: Variant B introduced a new `INFO` severity level below `MEDIUM`. This expands the API surface and requires changes to `undischarged_count` logic. The hybrid approach uses the existing `MEDIUM` level for all meta-context, maintaining consistency with the current severity model. No new levels needed.

### 2. `classification_reason` Dataclass Field (from B)
- **Rationale**: Variant B added an optional `classification_reason: str = ""` field to the `Obligation` dataclass. While useful for debugging, this is technically an API change. The hybrid approach prioritizes zero API changes (from C). Debug information can be added via logging if needed.

### 3. Deprecation of `_determine_severity()` (from B)
- **Rationale**: Variant B proposed deprecating `_determine_severity()` because it was "subsumed" by the new classifier. However, `_determine_severity()` still handles code block detection (MEDIUM demotion for code blocks). The hybrid approach keeps `_determine_severity()` for code block checks and adds `_is_meta_context()` as an additional check AFTER it. Both functions have clear, non-overlapping responsibilities.

### 4. Risk Descriptions as HIGH (from B's E13 Decision)
- **Rationale**: Variant B deliberately classified risk descriptions as HIGH (E13: "Risk: placeholder data could leak" → HIGH). The adversarial debate overruled this decision—risk descriptions are meta-references describing hypothetical concerns, not actual obligations. The hybrid demotes them to MEDIUM (from A/C consensus).

### 5. Full Exemption for Code Blocks (from A)
- **Rationale**: Variant A proposed upgrading code block handling from MEDIUM demotion to full exemption. The hybrid keeps MEDIUM demotion for code blocks (same as current behavior) to maintain consistency. Code block obligations are still visible in reports, just not counted as undischarged.

### 6. 4-Layer Classification (from B)
- **Rationale**: Variant B had 4 layers: L0 (code block), L1 (structural), L2 (negation), L3 (command), L4 (gate). The hybrid simplifies to 2 layers: Layer 1 (inline code + completed checklist), Layer 2 (negation/meta-context covering all 6 categories). This reduces complexity while maintaining coverage. Shell commands and gate criteria are handled by the consolidated negation regex in Layer 2.

### 7. Multi-Line Context Analysis (deferred from A/B)
- **Rationale**: Both A and B acknowledged multi-line negation contexts as a limitation but deferred it. The hybrid also defers this—single-line analysis covers >95% of observed false positives per Variant B's analysis. Multi-line can be added as a future enhancement if needed.

### 8. NLP-Based Classification (from B's Alternatives Considered)
- **Rationale**: Variant B considered and rejected NLP-based approaches. The hybrid maintains this rejection—regex-based classification is sufficient for the pattern set and avoids heavy dependencies.

---

## Implementation Phases (from Base A)

### Phase 1: Quick Win (~20 lines)
- Inline code exemption (scaffold-aware regex from B)
- Completed checklist detection (from B)
- Risk: Low, immediate value

### Phase 2: Full Fix (~50 lines)
- Negation-aware classification (consolidated regex from C + patterns from A)
- Shell command detection (included in consolidated regex)
- Gate criteria detection (included in consolidated regex)
- Integration into `scan_obligations()`
- Tests (parameterized format from B)

---

## Files Modified

| File | Change Type | Lines (Approx) |
|------|-------------|----------------|
| `obligation_scanner.py` | Add constants + `_is_meta_context()` + integration | ~70 |
| `test_obligation_scanner_meta_context.py` | New file with parameterized tests | ~120 |
| **Total** | | **~190 lines** |

---

## Provenance Summary

| Element | Primary Source | Adaptations |
|---------|---------------|-------------|
| 2-Layer architecture | A | Simplified from 3 layers |
| MEDIUM severity for meta-context | C | Applied to all meta-context |
| Scaffold-aware inline code regex | B | Used as-is |
| Completed checklist detection | B | Added to Layer 1 |
| Edge case catalog (E1-E20) | B | Severity changed to MEDIUM |
| Parameterized test format | B | Adapted severity expectations |
| Consolidated negation regex | C + A | C's structure, A's patterns |
| `_is_meta_context()` signature | A/C | `bool` return (not severity) |
| Incremental deployment plan | A | Kept as-is |
| No dataclass changes | C | Rejected B's `classification_reason` |
| Risk demoted to MEDIUM | A/C consensus | Rejected B's HIGH decision |
