# Base Selection: Obligation Scanner False Positive Mitigation

**Date**: 2026-04-03
**Evaluated Variants**:
- **Variant A (Brainstorm/Composite)**: 3-layer composite with full exemption
- **Variant B (Design/Classifier)**: 4-layer classifier with INFO severity
- **Variant C (Improve/Minimal)**: 2-regex minimal approach

---

## Scoring Framework

### Quantitative Criteria (50% weight)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Requirement Coverage | 0.30 | How many of the 6 false positive categories does each cover? |
| Internal Consistency | 0.25 | Are there contradictions within the proposal? |
| Specificity Ratio | 0.15 | Concrete code vs vague descriptions? |
| Dependency Completeness | 0.15 | Are all internal references resolved? |
| Section Coverage | 0.15 | How complete is the proposal across all expected sections? |

### Qualitative Criteria (50% weight)

| Category | Criteria | Description |
|----------|----------|-------------|
| **Completeness** (5 criteria) | Problem statement | Clear articulation of the false positive problem |
| | Solution | Well-defined technical approach |
| | Edge cases | Systematic handling of edge cases |
| | Tests | Comprehensive test plan |
| | Migration | Backward compatibility and migration path |
| **Correctness** (5 criteria) | Regex correctness | Patterns are valid and match intended cases |
| | Positional logic | Negation-before-term logic is sound |
| | Backward compat | No breaking changes to public API |
| | API safety | New functions have appropriate signatures |
| | No regressions | Existing behavior preserved |
| **Structure** (5 criteria) | Organization | Logical flow and section ordering |
| | Flow | Smooth transitions between sections |
| | Headings | Consistent and descriptive headings |
| | Code blocks | Properly formatted and explained code |
| | Tables | Effective use of tables for comparison |
| **Clarity** (5 criteria) | Naming | Clear function and variable names |
| | Explanations | Rationale provided for decisions |
| | Rationale | Design decisions justified |
| | Examples | Concrete examples illustrate concepts |
| | Decisions documented | Explicit decisions with trade-offs |
| **Risk Coverage** (5 criteria) | Over-suppression | Mitigation for filtering real obligations |
| | Under-filtering | Handling of novel meta-context patterns |
| | Performance | Regex performance considerations |
| | Compatibility | Backward compatibility assurance |
| | Escape hatches | Manual override mechanisms preserved |
| **Invariant & Edge Case Coverage** (5 criteria) | Double negation | "Do not skip the placeholder" handling |
| | Mixed lines | Lines with both obligation and meta-context |
| | Positional edge | Term at line start, negation at end |
| | Ambiguous terms | "temporary workaround" classification |
| | Cross-line | Multi-line context limitations |

---

## Quantitative Scoring

### Variant A (Brainstorm/Composite)

| Criterion | Score (0-1) | Weighted | Notes |
|-----------|-------------|----------|-------|
| Requirement Coverage | 1.00 | 0.300 | Covers all 6 categories (verification, shell commands, code blocks, negation, historical, risk) |
| Internal Consistency | 0.85 | 0.213 | Layered approach is consistent; risk exemption conflicts with conservative bias stated elsewhere |
| Specificity Ratio | 0.90 | 0.135 | Concrete code for all layers; proximity window "fix" is vague |
| Dependency Completeness | 0.90 | 0.135 | References existing FR-MOD1.8; assumes code block ranges available |
| Section Coverage | 0.85 | 0.128 | Missing explicit test plan section; has edge cases but not formal test matrix |
| **Quantitative Subtotal** | | **0.911** | |

### Variant B (Design/Classifier)

| Criterion | Score (0-1) | Weighted | Notes |
|-----------|-------------|----------|-------|
| Requirement Coverage | 1.00 | 0.300 | Covers all 6 categories + completed checklist (bonus) |
| Internal Consistency | 0.75 | 0.188 | E13 decision (risk=HIGH) contradicts problem statement; INFO severity adds complexity without clear benefit |
| Specificity Ratio | 0.95 | 0.143 | Highly concrete; every edge case has expected classification |
| Dependency Completeness | 0.95 | 0.143 | Explicit data flow diagram; clear integration points |
| Section Coverage | 0.95 | 0.143 | Complete: problem, design, edge cases, API, tests, migration, alternatives |
| **Quantitative Subtotal** | | **0.917** | |

### Variant C (Improve/Minimal)

| Criterion | Score (0-1) | Weighted | Notes |
|-----------|-------------|----------|-------|
| Requirement Coverage | 0.85 | 0.255 | Covers categories 1, 2, 4, 5, 6; acknowledges category 3 already handled; misses inline code |
| Internal Consistency | 0.90 | 0.225 | Consistent with existing MEDIUM demotion pattern; no contradictions |
| Specificity Ratio | 0.85 | 0.128 | Concrete code provided; less detailed than B |
| Dependency Completeness | 0.90 | 0.135 | Assumes existing severity system; clear integration point |
| Section Coverage | 0.80 | 0.120 | Missing formal edge case catalog; has test plan but not as structured |
| **Quantitative Subtotal** | | **0.863** | |

**Quantitative Rankings**:
1. Variant B: 0.917
2. Variant A: 0.911
3. Variant C: 0.863

---

## Qualitative Scoring

### Variant A (Brainstorm/Composite)

| Category | Criteria | Score | Notes |
|----------|----------|-------|-------|
| **Completeness** | Problem statement | 1.0 | Excellent: 6 categories with examples |
| | Solution | 0.9 | Layered approach well-defined |
| | Edge cases | 0.9 | 10 edge cases with mitigations |
| | Tests | 0.7 | Mentions tests but no explicit test plan section |
| | Migration | 0.9 | Incremental deployment plan |
| **Correctness** | Regex correctness | 0.9 | Patterns look valid |
| | Positional logic | 0.9 | Negation-before-term is correct |
| | Backward compat | 1.0 | Explicitly backward compatible |
| | API safety | 0.9 | `bool` return is safe |
| | No regressions | 0.9 | Fail-safe default |
| **Structure** | Organization | 0.9 | Logical flow: problem → alternatives → recommendation |
| | Flow | 0.9 | Smooth transitions |
| | Headings | 0.9 | Consistent markdown headings |
| | Code blocks | 0.9 | Well-formatted |
| | Tables | 0.9 | Good use of comparison tables |
| **Clarity** | Naming | 0.9 | `_is_meta_context()`, `_is_inside_inline_code()` |
| | Explanations | 0.9 | Clear rationale for each layer |
| | Rationale | 0.9 | Design decisions justified |
| | Examples | 0.9 | Concrete examples throughout |
| | Decisions documented | 0.8 | Some decisions implicit |
| **Risk Coverage** | Over-suppression | 0.8 | Proximity window mentioned but not detailed |
| | Under-filtering | 0.8 | `# obligation-exempt` fallback |
| | Performance | 0.9 | Pure function, no I/O |
| | Compatibility | 0.9 | Backward compatible |
| | Escape hatches | 0.9 | Manual override preserved |
| **Invariant & Edge Case Coverage** | Double negation | 0.8 | Proximity window fix is vague |
| | Mixed lines | 0.9 | Per-match classification handles this |
| | Positional edge | 0.9 | Explicit handling |
| | Ambiguous terms | 0.9 | "temporary workaround" example |
| | Cross-line | 0.8 | Acknowledged as limitation |
| **Category Average** | | **0.885** | |

**Completeness Subtotal**: 4.4/5 = 0.88
**Correctness Subtotal**: 4.6/5 = 0.92
**Structure Subtotal**: 4.5/5 = 0.90
**Clarity Subtotal**: 4.4/5 = 0.88
**Risk Coverage Subtotal**: 4.3/5 = 0.86
**Invariant Coverage Subtotal**: 4.3/5 = 0.86

**Variant A Qualitative Average**: (0.88 + 0.92 + 0.90 + 0.88 + 0.86 + 0.86) / 6 = **0.883**

---

### Variant B (Design/Classifier)

| Category | Criteria | Score | Notes |
|----------|----------|-------|-------|
| **Completeness** | Problem statement | 1.0 | Excellent: 8 categories (includes completed checklist, quoted terms) |
| | Solution | 0.95 | 4-layer classifier well-defined |
| | Edge cases | 1.0 | 20 edge cases (E1-E20) with expected classifications |
| | Tests | 0.95 | Comprehensive test plan with parameterized tests |
| | Migration | 0.9 | Zero migration required section |
| **Correctness** | Regex correctness | 0.9 | Patterns look valid; scaffold-aware inline code regex is clever |
| | Positional logic | 0.9 | Negation-before-term with 4-word window |
| | Backward compat | 0.9 | Claims compatibility but adds dataclass field |
| | API safety | 0.85 | Severity return is less safe than bool; new dataclass field |
| | No regressions | 0.85 | E13 decision (risk=HIGH) may cause regressions |
| **Structure** | Organization | 0.95 | Excellent: problem, design, edge cases, API, tests, migration |
| | Flow | 0.9 | Logical progression |
| | Headings | 0.95 | Consistent, descriptive |
| | Code blocks | 0.95 | Well-formatted with syntax highlighting |
| | Tables | 0.95 | Extensive use of tables |
| **Clarity** | Naming | 0.9 | `_classify_meta_context()` is clear |
| | Explanations | 0.9 | Detailed rationale |
| | Rationale | 0.85 | E13 decision contradicts problem statement |
| | Examples | 0.95 | Every edge case has example |
| | Decisions documented | 0.9 | E13, E15/E16 explicitly justified |
| **Risk Coverage** | Over-suppression | 0.85 | 4-word window mitigation |
| | Under-filtering | 0.85 | `# obligation-exempt` fallback |
| | Performance | 0.9 | Pure function |
| | Compatibility | 0.85 | Dataclass change is technically breaking |
| | Escape hatches | 0.9 | Manual override preserved |
| **Invariant & Edge Case Coverage** | Double negation | 0.9 | E16 explicitly addressed |
| | Mixed lines | 0.9 | E18 explicitly addressed |
| | Positional edge | 0.9 | E15 explicitly addressed |
| | Ambiguous terms | 0.9 | E14 example |
| | Cross-line | 0.8 | Acknowledged as future enhancement |
| **Category Average** | | **0.900** | |

**Completeness Subtotal**: 4.8/5 = 0.96
**Correctness Subtotal**: 4.4/5 = 0.88
**Structure Subtotal**: 4.7/5 = 0.94
**Clarity Subtotal**: 4.5/5 = 0.90
**Risk Coverage Subtotal**: 4.35/5 = 0.87
**Invariant Coverage Subtotal**: 4.5/5 = 0.90

**Variant B Qualitative Average**: (0.96 + 0.88 + 0.94 + 0.90 + 0.87 + 0.90) / 6 = **0.908**

---

### Variant C (Improve/Minimal)

| Category | Criteria | Score | Notes |
|----------|----------|-------|-------|
| **Completeness** | Problem statement | 0.9 | Good: 6 categories with examples |
| | Solution | 0.85 | Well-defined but minimal |
| | Edge cases | 0.7 | No formal catalog; implicit in test plan |
| | Tests | 0.85 | Test plan with 10 cases |
| | Migration | 0.9 | Backward compatibility addressed |
| **Correctness** | Regex correctness | 0.85 | Patterns look valid; monolithic regex harder to verify |
| | Positional logic | 0.9 | Negation-before-term correct |
| | Backward compat | 1.0 | No API changes |
| | API safety | 0.95 | `bool` return is safe |
| | No regressions | 0.9 | Fail-safe default |
| **Structure** | Organization | 0.85 | Logical: root cause → fix → risk → tests |
| | Flow | 0.85 | Adequate transitions |
| | Headings | 0.85 | Consistent |
| | Code blocks | 0.85 | Well-formatted |
| | Tables | 0.8 | Risk table good; fewer tables than B |
| **Clarity** | Naming | 0.85 | `_is_meta_context()` is clear |
| | Explanations | 0.85 | Good rationale |
| | Rationale | 0.85 | Decisions justified |
| | Examples | 0.85 | Good examples |
| | Decisions documented | 0.8 | Some decisions implicit |
| **Risk Coverage** | Over-suppression | 0.85 | Positional constraint mitigates |
| | Under-filtering | 0.85 | `# obligation-exempt` fallback |
| | Performance | 0.9 | Single regex, checked once per match |
| | Compatibility | 0.95 | Fully backward compatible |
| | Escape hatches | 0.9 | Manual override preserved |
| **Invariant & Edge Case Coverage** | Double negation | 0.7 | Not explicitly addressed |
| | Mixed lines | 0.8 | Implied by per-match check |
| | Positional edge | 0.85 | Handled |
| | Ambiguous terms | 0.8 | Implicit |
| | Cross-line | 0.8 | Acknowledged as limitation |
| **Category Average** | | **0.847** | |

**Completeness Subtotal**: 4.2/5 = 0.84
**Correctness Subtotal**: 4.6/5 = 0.92
**Structure Subtotal**: 4.2/5 = 0.84
**Clarity Subtotal**: 4.2/5 = 0.84
**Risk Coverage Subtotal**: 4.45/5 = 0.89
**Invariant Coverage Subtotal**: 3.95/5 = 0.79

**Variant C Qualitative Average**: (0.84 + 0.92 + 0.84 + 0.84 + 0.89 + 0.79) / 6 = **0.853**

---

## Combined Scoring

| Variant | Quantitative (50%) | Qualitative (50%) | **Combined** |
|---------|-------------------|-------------------|--------------|
| A (Brainstorm/Composite) | 0.911 | 0.883 | **0.897** |
| B (Design/Classifier) | 0.917 | 0.908 | **0.913** |
| C (Improve/Minimal) | 0.863 | 0.853 | **0.858** |

**Final Rankings**:
1. **Variant B (Design/Classifier)**: 0.913
2. **Variant A (Brainstorm/Composite)**: 0.897 (1.6% behind)
3. **Variant C (Improve/Minimal)**: 0.858 (5.5% behind)

---

## Tiebreaker Analysis

The top two variants (B and A) are within 5% (1.6% difference). Per the evaluation framework, a tiebreaker is required.

### Tiebreaker Criteria

| Criterion | Variant A | Variant B | Winner |
|-----------|-----------|-----------|--------|
| **Implementation Risk** | Lower (incremental deployment) | Higher (monolithic change) | A |
| **Maintenance Burden** | Medium (3 layers to understand) | Higher (4 layers + INFO severity) | A |
| **Edge Case Coverage** | 10 cases | 20 cases | B |
| **API Surface Changes** | None | New dataclass field | A |
| **Problem Alignment** | Full exemption aligns with "false positive" goal | E13 contradicts problem statement | A |
| **Testability** | Layered testing | Comprehensive test matrix | B |
| **Review Burden** | ~160 lines | ~230 lines | A |

**Tiebreaker Score**: Variant A wins 4 of 6 criteria.

---

## Base Selection Decision

### Selected Base: **Variant A (Brainstorm/Composite)**

**Rationale**:

While Variant B scored higher in the quantitative and qualitative analysis, the 1.6% difference is within the tiebreaker threshold. Variant A wins on practical implementation concerns:

1. **Incremental Deployability**: Variant A's explicit 3-phase implementation plan reduces risk. Layer 1 (code block exemption) can ship as a quick win.

2. **API Stability**: Variant A makes no dataclass changes. Variant B's `classification_reason` field, while useful, expands the API surface.

3. **Problem Alignment**: Variant A's full exemption for meta-context aligns with the stated goal of eliminating false positives. Variant B's E13 decision (risk=HIGH) contradicts the problem statement.

4. **Review Efficiency**: Variant A's ~160 lines vs Variant B's ~230 lines means faster review and lower cognitive load.

### Hybrid Elements to Incorporate

From **Variant B**:
- Edge case catalog structure (adapt E1-E20 to A's approach)
- Scaffold-aware inline code detection (more precise than generic position check)
- Test plan format (parameterized tests)

From **Variant C**:
- MEDIUM severity for meta-context (instead of full exemption or INFO)
- No dataclass changes
- Minimal regex count (consolidate patterns where possible)

### Final Implementation Profile

| Aspect | Decision |
|--------|----------|
| **Base Variant** | A (Brainstorm/Composite) |
| **Severity Model** | MEDIUM (from C, instead of exempt/INFO) |
| **Layers** | 2 layers (code context + negation classification) |
| **Dataclass Changes** | None (from C) |
| **Edge Cases** | 15-20 cases (structure from B, content from A) |
| **Diff Size** | ~140-160 lines |
| **Incremental Deployment** | Yes (explicit phases from A) |

---

## Risk Acceptance

| Risk | Mitigation |
|------|------------|
| Over-suppression of real obligations | Positional negation check + fail-safe default |
| Under-filtering of novel patterns | `# obligation-exempt` escape hatch preserved |
| Code block TODOs hidden | Acceptable risk—TODOs in code blocks are comments, not executable obligations |
| Double negation edge case | 4-word proximity window (from A's refinement) |

---

## Next Steps

1. Create hybrid specification combining Variant A's structure with elements from B and C
2. Define explicit implementation phases:
   - Phase 1: Code block full exemption + inline code detection
   - Phase 2: Negation-aware meta-context classification
3. Adapt Variant B's edge case catalog to the hybrid approach
4. Write parameterized tests covering 15-20 edge cases
5. Implement with no dataclass changes (MEDIUM severity for meta-context)
