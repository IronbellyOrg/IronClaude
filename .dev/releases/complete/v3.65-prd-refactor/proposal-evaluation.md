# Proposal Evaluation: Meta-Context False Positive Suppression for Obligation Scanner

**Date**: 2026-04-03
**Evaluator**: Independent Agent
**Proposals Evaluated**: brainstorm, design, improve

---

## 1. Per-Proposal Scoring

### Proposal A: Brainstorm (`proposal-brainstorm.md`)

| Criterion | Weight | Score (1-5) | Evidence |
|-----------|--------|-------------|----------|
| **Completeness** | 20% | 5 | Explicitly enumerates all 6 categories in a dedicated table (lines 16-23). Explores 6 alternative solutions (A-F) and recommends the composite. |
| **Correctness** | 20% | 4 | Composite approach (Alt F) is technically sound. Positional negation check is correct. However, the proximity-based "4-word window" refinement (edge case 1, lines 296-309) is introduced mid-document as a patch to the double-negation problem -- it feels ad-hoc rather than integrated into the main design. The chosen window size is arbitrary and not validated. |
| **Minimality** | 15% | 3 | ~160 lines total diff is reasonable, but the recommended composite approach layers three mechanisms (code exemption, negation classifier, manual override). Six alternatives explored is thorough but the document is 366 lines of exploration for an 80-line code change. |
| **Safety** | 15% | 5 | Fail-safe default ("assume obligation-creating") is explicitly stated (line 101, 278). The document identifies the double-negation false-negative edge case AND self-corrects in real-time (lines 296-300). Monotonic improvement stated at line 58: "only suppresses false positives, never blocks new true positives." |
| **Testability** | 10% | 3 | Mentions ~80 lines of tests and provides 10 edge cases with expected outcomes (lines 291-340), but no concrete test code. Edge case analysis is excellent but no parameterized test structure shown. |
| **Backward Compat** | 10% | 5 | Line 353: "Existing roadmaps that pass today will still pass." No API changes, no configuration changes, no migration required. |
| **Maintainability** | 10% | 4 | Layered design (L1 code exemption, L2 negation classifier, L3 manual override) is well-structured and independently testable. The proximity-based refinement adds complexity. |

**Weighted Total**: (5 x 0.20) + (4 x 0.20) + (3 x 0.15) + (5 x 0.15) + (3 x 0.10) + (5 x 0.10) + (4 x 0.10) = 1.00 + 0.80 + 0.45 + 0.75 + 0.30 + 0.50 + 0.40 = **4.20**

---

### Proposal B: Design (`proposal-design.md`)

| Criterion | Weight | Score (1-5) | Evidence |
|-----------|--------|-------------|----------|
| **Completeness** | 20% | 5 | Covers all 6 categories plus two additional ones (completed checklist items, quoted terms in prose) in Section 1.1. 20-item edge case catalog (Section 3) is the most thorough of all proposals. |
| **Correctness** | 20% | 5 | Four-layer classification (L0 code block, L1 structural, L2 negation, L3 command, L4 gate criteria) is technically sound. Introduces INFO severity rather than overloading MEDIUM, which is semantically cleaner. Deliberate decisions on E13 (risk stays HIGH, line 318-323) and E15/E16 (negation-after-term stays HIGH, lines 325-328) are well-reasoned. The `_classify_meta_context()` function signature correctly accepts positional information for per-match classification. |
| **Minimality** | 15% | 3 | ~230 lines total diff (75 core + 155 test). Introduces a new severity level (INFO), a new dataclass field (`classification_reason`), deprecates `_determine_severity()`, and adds 6 new module-level constants. This is the heaviest solution. |
| **Safety** | 15% | 5 | Monotonic improvement explicitly stated (Section 6.1): "can only reduce undischarged_count, never increase it." E13 deliberate decision to keep risk descriptions as HIGH is the safest choice. Acknowledges over-suppression risk (Section 6.4) and identifies the absence of a `# obligation-force` inverse escape hatch. |
| **Testability** | 10% | 5 | Concrete parameterized test code provided (Section 5.1, lines 368-396). Full integration test scenarios with assertions (Section 5.2). Regression suite for existing behavior (Section 5.3). Test coverage matrix (Section 5.4). This is the most testable proposal by a wide margin. |
| **Backward Compat** | 10% | 5 | Section 4 explicitly lists every public API symbol and confirms no breaking changes. New dataclass field has a default value. `undischarged_count` changes are monotonically fewer. Existing `# obligation-exempt` comments become harmless no-ops. |
| **Maintainability** | 10% | 4 | Well-structured with named layers, classification reasons for debuggability, and a clear data flow diagram (Section 2.4). However, the 4-layer classification with 6 module-level compiled regexes and a new severity level is the most complex codebase change. The deprecation of `_determine_severity()` adds transitional burden. |

**Weighted Total**: (5 x 0.20) + (5 x 0.20) + (3 x 0.15) + (5 x 0.15) + (5 x 0.10) + (5 x 0.10) + (4 x 0.10) = 1.00 + 1.00 + 0.45 + 0.75 + 0.50 + 0.50 + 0.40 = **4.60**

---

### Proposal C: Improve (`proposal-improve.md`)

| Criterion | Weight | Score (1-5) | Evidence |
|-----------|--------|-------------|----------|
| **Completeness** | 20% | 5 | Covers all 6 categories explicitly (Section 1) with root-cause analysis of WHY each is a false positive. The "referenced vs. instantiated" framing is precise. |
| **Correctness** | 20% | 4 | The `_is_meta_context()` function is functional but the single `_NEGATION_PREFIX_RE` mega-regex conflates distinct categories (negation, historical, risk, verification, gate criteria) into one alternation group. Including "verificat\w*" and "gate\s+criteri\w*" alongside negation words is semantically wrong -- these are section-context patterns, not negation patterns. A line like "Verification: create placeholder config" would incorrectly demote a real obligation because "Verificat" precedes "placeholder". |
| **Minimality** | 15% | 5 | ~120-140 lines total diff. Smallest footprint of all three. Two compiled regexes and one function. Reuses existing MEDIUM severity. No new dataclass fields. No deprecations. |
| **Safety** | 15% | 4 | Positional constraint (prefix must appear before term) is correct. However, the mega-regex includes non-positional concepts ("risk", "verification") that, when appearing anywhere before the scaffold term, could cause false negatives. Example from risk table (Section 3): "Over-filters: real obligation demoted to MEDIUM" is rated "Low" likelihood, but the "Verification:" prefix case described above is more likely than acknowledged. |
| **Testability** | 10% | 4 | Test plan (Section 5) lists 10 concrete test cases with expected outcomes. No test code provided but cases are specific and actionable. Missing: parameterized test structure, integration tests, regression tests for existing behavior. |
| **Backward Compat** | 10% | 5 | "No changes to gates.py, pipeline/gates.py, or pipeline/models.py." Change is entirely within the scanner. Only demotes severity, never promotes. |
| **Maintainability** | 10% | 4 | Simple to understand: one function, two regexes. But the mega-regex is hard to modify without risk -- adding or removing a term from the alternation group requires understanding the entire pattern. No per-category breakdown means debugging a specific false positive requires understanding the whole pattern. |

**Weighted Total**: (5 x 0.20) + (4 x 0.20) + (5 x 0.15) + (4 x 0.15) + (4 x 0.10) + (5 x 0.10) + (4 x 0.10) = 1.00 + 0.80 + 0.75 + 0.60 + 0.40 + 0.50 + 0.40 = **4.45**

---

## 2. Summary Comparison

| Criterion (Weight) | Brainstorm | Design | Improve |
|---------------------|-----------|--------|---------|
| Completeness (20%) | 5 | 5 | 5 |
| Correctness (20%) | 4 | **5** | 4 |
| Minimality (15%) | 3 | 3 | **5** |
| Safety (15%) | 5 | 5 | 4 |
| Testability (10%) | 3 | **5** | 4 |
| Backward Compat (10%) | 5 | 5 | 5 |
| Maintainability (10%) | 4 | 4 | 4 |
| **Weighted Total** | **4.20** | **4.60** | **4.45** |

---

## 3. Strengths and Weaknesses

### Brainstorm

**Strengths**:
- Best exploration of the solution space. Six alternatives with honest pros/cons give confidence the recommended approach is well-considered.
- Excellent edge case analysis (10 scenarios) with self-correcting reasoning -- the double-negation realization mid-document (lines 296-300) shows rigorous thinking.
- Layered implementation order (quick win first, full fix second) is pragmatic for incremental delivery.

**Weaknesses**:
- The recommended composite solution (Alt F) is described at a higher level of abstraction than the Design proposal. Key implementation details (exact regex patterns, integration code, severity semantics) are sketched but not fully specified.
- The "4-word proximity window" for negation is introduced as a patch rather than a first-class design decision. No analysis of optimal window size.
- No concrete test code provided. Test plan is implied by edge cases but not formalized.

### Design

**Strengths**:
- Most complete specification. Every detail needed for implementation is present: exact regex patterns, function signatures, data flow, integration code, severity semantics, dataclass changes, deprecation plan.
- 20-item edge case catalog with expected severity and classification layer is the gold standard for testability.
- Introduction of INFO severity is semantically correct -- meta-references are genuinely different from code-block demotions. Conflating them into MEDIUM (as Improve proposes) loses diagnostic information.
- Concrete parameterized test code, integration tests, and regression tests provided in Sections 5.1-5.3.
- Deliberate decisions on E13 and E15/E16 are documented with rationale, preventing future contributors from "fixing" intentional behavior.

**Weaknesses**:
- Largest diff (~230 lines). INFO severity, classification_reason field, and deprecated function add conceptual weight to the codebase.
- The deprecation of `_determine_severity()` creates a transitional period where two severity-classification paths coexist.
- Layer 4 (gate/verification criteria regex) overlaps partially with Layer 2 (negation prefixes). The boundary between "ensure no placeholder" (L2) and "zero placeholder values found" (L4) is not entirely crisp.

### Improve

**Strengths**:
- Smallest diff (~120-140 lines). Achieves the goal with minimal codebase disruption.
- Reuses existing MEDIUM severity rather than introducing new concepts. Zero new abstractions.
- Root cause analysis is the clearest of the three -- the "referenced vs. instantiated" framing is precise and memorable.
- Phase 1 / Phase 2 split correctly defers complexity not needed now.

**Weaknesses**:
- The mega-regex `_NEGATION_PREFIX_RE` conflates six distinct meta-context categories into one pattern. This creates a correctness risk: "verification" and "gate criteria" are not negation patterns and should not share a regex with "no", "never", "removed". A line like "Gate criterion: add placeholder routing" would be incorrectly demoted.
- Demoting to MEDIUM rather than a distinct level means meta-context demotions are indistinguishable from code-block demotions in the report. Reduces debuggability.
- No regression test plan for existing behavior. Only forward-looking test cases.

---

## 4. Overall Ranking

| Rank | Proposal | Score | Rationale |
|------|----------|-------|-----------|
| 1 | **Design** | 4.60 | Most complete, most correct, most testable. The overhead of INFO severity and classification_reason is justified by precision and debuggability gains. |
| 2 | **Improve** | 4.45 | Best minimality. Would rank first if not for the mega-regex correctness concern and loss of debuggability from reusing MEDIUM. |
| 3 | **Brainstorm** | 4.20 | Best exploration document but weakest as an implementation spec. Identifies the right solution (composite approach) but does not specify it with enough precision to implement directly. |

---

## 5. Recommendation

**Implement the Design proposal** with targeted simplifications drawn from Brainstorm and Improve:

1. **From Improve -- reduce diff size**: Skip the `classification_reason` dataclass field for now. It is a debugging convenience, not a functional requirement. Can be added later if debugging meta-context classifications proves difficult.

2. **From Improve -- skip the deprecation**: Instead of retaining `_determine_severity()` alongside `_classify_meta_context()`, replace it outright. The old function is internal (underscore-prefixed) with no external consumers. One severity-classification path is better than two coexisting.

3. **From Brainstorm -- incremental delivery**: Ship Layer 1 (inline code + completed checklist exemption) as a standalone commit that is trivially correct, then Layer 2-4 (negation, command, gate criteria) as a second commit. This gives an immediate quick win and isolates risk.

4. **Fix the Improve mega-regex concern**: Keep the Design proposal's separation of negation patterns, command patterns, and gate-criteria patterns as distinct regexes. Do not merge them into one alternation group. This prevents the "Verification: create placeholder config" false-negative scenario identified above.

5. **Adopt INFO severity from Design**: The semantic distinction between "inside a code block" (MEDIUM) and "meta-context reference" (INFO) is worth the small conceptual cost. It makes the audit report more informative and prevents confusion about why a term was demoted.

The resulting implementation would be approximately 180-200 lines (between Design's 230 and Improve's 140), combining Design's correctness and testability with Improve's scope discipline.
