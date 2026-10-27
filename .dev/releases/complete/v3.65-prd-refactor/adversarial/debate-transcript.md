# Adversarial Debate: Obligation Scanner False Positive Mitigation

**Date**: 2026-04-03
**Topic**: Selecting the optimal approach for reducing false positives in the obligation scanner
**Variants**:
- **Variant A (Brainstorm/Composite)**: 3-layer composite with full exemption
- **Variant B (Design/Classifier)**: 4-layer classifier with INFO severity
- **Variant C (Improve/Minimal)**: 2-regex minimal approach

---

## Round 1: Opening Arguments

### Advocate A (Brainstorm/Composite)

**My Position**: The 3-layer composite approach (Alternative F from the brainstorm document) provides the most comprehensive and defensible solution.

**Core Strengths**:
1. **Layered Defense**: Code context exemption (Layer 1) + Negation-aware classification (Layer 2) + Manual override (Layer 3). Each layer is independently testable.
2. **Full Exemption for Code**: Code blocks and inline code are NEVER obligations. Full exemption is semantically correct.
3. **Positional Awareness**: The negation check requires the negation word to PRECEDE the scaffold term, avoiding over-suppression.
4. **Incremental Deployability**: Layer 1 can ship independently as a quick win (~15 lines), with Layer 2 following.
5. **Fail-Safe Default**: When in doubt, treat as obligation. This prevents false negatives.

**Steelman of B**: The classifier approach with INFO severity is well-structured and provides transparency through `classification_reason`. The 4-layer evaluation order is logical. The edge case catalog is thorough.

**Critique of B**:
- **INFO severity is unnecessary complexity**: We already have HIGH/MEDIUM/exempt. Adding INFO creates a third severity level that complicates the mental model and gate logic.
- **Risk descriptions classified as HIGH**: Your E13 decision classifies "Risk: placeholder data could leak" as HIGH. This contradicts the goal of reducing false positives—risk descriptions are meta-context, not obligations.
- **Dataclass changes**: Adding `classification_reason` field touches the data model when the existing `exempt` boolean suffices.
- **Completed checklist detection**: While useful, this adds complexity for a narrow edge case.

**Steelman of C**: The minimal approach is appealing for its simplicity. Two regex patterns cover the majority of false positives with minimal code.

**Critique of C**:
- **Incomplete coverage**: Categories 2 and 3 (code blocks, inline code) are not addressed. You acknowledge code block demotion exists but don't improve it.
- **No positional awareness**: The negation prefix check doesn't verify the negation precedes the scaffold term, risking over-suppression.
- **Risk descriptions demoted to MEDIUM**: While better than B's HIGH classification, MEDIUM still appears in reports as noise.
- **Missed edge cases**: Double negation, mixed lines, and ambiguous terms are not systematically addressed.

---

### Advocate B (Design/Classifier)

**My Position**: The 4-layer classifier with INFO severity provides the most nuanced and maintainable solution.

**Core Strengths**:
1. **Granular Severity Model**: INFO severity acknowledges meta-context exists on a spectrum—not quite exempt (manual override), not quite MEDIUM (code blocks), but informational.
2. **Transparency**: The `classification_reason` field enables debugging and auditability. Users can see WHY a term was classified a certain way.
3. **Comprehensive Edge Case Coverage**: 20 documented edge cases (E1-E20) with deliberate decisions documented (E13, E15/E16).
4. **Scaffold-Aware Inline Code Detection**: The regex ``_INLINE_CODE_RE = re.compile(r"`[^`]*(?:" + "|".join(SCAFFOLD_TERMS) + r")[^`]*`")`` specifically matches scaffold terms inside backticks.
5. **Completed Checklist Detection**: `- [x]` prefix detection handles a real-world pattern in roadmaps.

**Steelman of A**: The composite approach's layered defense is architecturally sound. The incremental deployment plan is pragmatic. Full exemption for code blocks is semantically defensible.

**Critique of A**:
- **Full exemption is too aggressive**: Some code blocks DO contain scaffolding obligations (e.g., `# TODO: replace mock_db with real DB`). Your Layer 1 would fully exempt these, potentially hiding real obligations.
- **No classification_reason**: Without transparency into WHY a term was classified, debugging misclassifications requires reading code.
- **Risk descriptions exempted**: Your approach would exempt "risk: placeholder data could leak" entirely. A risk statement implies the placeholder EXISTS and is a genuine concern—this should be visible, not suppressed.
- **Shell command detection too broad**: Your `_SHELL_CMD_RE` matches any line with grep/sed/awk, even if the scaffold term is unrelated to the command.

**Steelman of C**: The minimal approach's small diff size (~120-140 lines) means lower review burden and faster implementation.

**Critique of C**:
- **MEDIUM demotion is insufficient**: Meta-context obligations still appear in reports, creating noise. INFO severity is cleaner.
- **No inline code detection**: You don't address inline backtick spans at all.
- **No completed checklist detection**: Misses a common pattern.
- **Single monolithic regex**: `_NEGATION_PREFIX_RE` combines negation, historical, risk, and verification patterns into one massive regex—harder to maintain than separate patterns.

---

### Advocate C (Improve/Minimal)

**My Position**: The minimal 2-regex approach provides the best cost/benefit ratio—solving 80% of the problem with 20% of the code.

**Core Strengths**:
1. **Minimal Complexity**: Only two new regex patterns and one helper function. Easier to review, test, and maintain.
2. **Backward Compatible**: Only demotes HIGH to MEDIUM. No new severity levels, no dataclass changes, no API changes.
3. **Positional Safety**: The negation prefix must appear BEFORE the term (via `line[:term_start_in_line]`), preventing over-suppression when negation follows the scaffold term.
4. **Fast Implementation**: ~120-140 lines vs 160-230 for alternatives. Lower risk, faster time-to-value.
5. **Proven Pattern**: The existing code block demotion to MEDIUM works—extending this pattern is consistent with the codebase.

**Steelman of A**: The composite approach's full exemption for code blocks is elegant. The layered architecture is defensible. The edge case analysis is thorough.

**Critique of A**:
- **Over-engineered**: Three layers for a problem that can be solved with two regex patterns. The 80-line estimated diff is 2x larger than necessary.
- **Full exemption risk**: Exempting code blocks entirely removes visibility. MEDIUM demotion preserves transparency while excluding from gate counts.
- **No incremental deployment evidence**: While you claim Layer 1 can ship independently, your proposal doesn't explicitly structure the implementation this way.
- **Proximity-based negation**: Your "fix" for double negation (4-word window) adds complexity for a rare edge case.

**Steelman of B**: The classifier's 4-layer evaluation order is logical. The edge case catalog is impressive. INFO severity provides granularity.

**Critique of B**:
- **Over-engineered**: 230 lines for a scanner enhancement is excessive. The `classification_reason` field adds API surface area for marginal benefit.
- **INFO severity unnecessary**: MEDIUM already exists and is already excluded from `undischarged_count`. Adding INFO creates confusion—what's the difference between INFO and MEDIUM?
- **E13 decision is wrong**: Classifying risk descriptions as HIGH contradicts the problem statement. Risk descriptions ARE meta-context.
- **Completed checklist overfit**: Detecting `- [x]` is a narrow optimization that adds complexity.

---

## Topic-by-Topic Evaluation

### Topic 1: Severity Model

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Approach** | Exempt (full) for meta-context | INFO (new level) for meta-context | MEDIUM (reuse existing) |
| **Rationale** | Meta-context is not an obligation | Meta-context is informational, not blocking | Consistent with existing code block handling |

**Debate**:
- **A argues**: Full exemption is semantically correct. Meta-context references are NOT obligations—they shouldn't appear in the obligation list at all.
- **B argues**: INFO provides transparency. Users can see meta-context was detected without it blocking the gate. Full exemption hides information.
- **C argues**: MEDIUM already exists and works. No new concepts needed. Consistency with existing code block demotion.

**Winner**: **Variant C** (Confidence: 0.75)
- **Evidence**: MEDIUM is already used for code blocks. Adding INFO (B) or full exemption (A) introduces new concepts without clear benefit. The goal is to exclude from `undischarged_count`—MEDIUM already does this.

---

### Topic 2: Function Return Type

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Return Type** | `bool` (`exempt`) | `str` (severity: HIGH/MEDIUM/INFO) | `bool` (is_meta_context) |
| **Integration** | Sets `exempt=True` or severity | Returns severity directly | Demotes HIGH to MEDIUM |

**Debate**:
- **B argues**: Returning severity string is cleaner—direct integration with the severity system.
- **A argues**: `bool` is simpler. The caller decides severity based on context (code block = MEDIUM, meta-context = exempt).
- **C argues**: `bool` keeps the change minimal. The existing severity system handles the rest.

**Winner**: **Variant B** (Confidence: 0.70)
- **Evidence**: Returning severity is more extensible. However, the `bool` approach (A, C) is simpler and sufficient for the current need. B's approach requires the caller to handle 4 severity levels.

---

### Topic 3: Risk Description Handling

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Classification** | Exempt (Layer 2) | HIGH (deliberate decision E13) | MEDIUM (included in negation regex) |
| **Rationale** | Risk describes hypothetical, not commitment | Risk implies placeholder exists and is a concern | Risk is meta-context, not obligation |

**Debate**:
- **B argues**: "Risk: placeholder data could leak" implies the placeholder EXISTS. The author should discharge it or explicitly exempt it. Conservative bias prevents under-filtering.
- **A argues**: Risk descriptions are meta-context by definition. They're describing a potential problem, not creating scaffolding.
- **C argues**: Risk descriptions should be demoted like other meta-context. MEDIUM is appropriate.

**Winner**: **Variant C** (Confidence: 0.80)
- **Evidence**: The problem statement explicitly lists "Risk descriptions" as a false positive category. B's E13 decision contradicts this. C's approach aligns with the stated goal. A's full exemption is too aggressive.

---

### Topic 4: Code Block Handling

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Treatment** | Full exemption (upgrade from MEDIUM) | MEDIUM (retain existing) | MEDIUM (retain existing) |
| **Rationale** | Code examples are never obligations | Some code blocks contain TODO obligations | Consistent with existing behavior |

**Debate**:
- **A argues**: Code blocks show examples, anti-patterns, or commands. They never create obligations. Full exemption is correct.
- **B argues**: Code blocks CAN contain obligations (e.g., `# TODO: replace mock_db`). MEDIUM preserves visibility while excluding from gate.
- **C argues**: Existing behavior works. No change needed.

**Winner**: **Variant B** (Confidence: 0.75)
- **Evidence**: B's caution about TODO comments in code blocks is valid. Full exemption (A) risks hiding real obligations. MEDIUM is the right balance—visible in reports but not blocking.

---

### Topic 5: Inline Code Detection

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Detection** | Generic backtick detection (`_is_inside_inline_code`) | Scaffold-aware regex (matches scaffold terms inside backticks) | Not addressed |
| **Precision** | Position-based check | Pattern-based check | N/A |

**Debate**:
- **B argues**: Scaffold-aware regex is more precise—only matches when scaffold terms appear inside backticks.
- **A argues**: Generic position-based detection is simpler and handles all cases (even non-scaffold terms in backticks are references, not obligations).
- **C argues**: Inline code detection is unnecessary complexity. Most inline code is in verification criteria covered by negation patterns.

**Winner**: **Variant A** (Confidence: 0.65)
- **Evidence**: A's generic approach handles all inline code, not just scaffold terms. However, B's scaffold-aware approach is more explicit about intent. C's omission is a gap.

---

### Topic 6: Edge Case Depth

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Count** | 10 edge cases | 20 edge cases (E1-E20) | 10 test cases |
| **Coverage** | Double negation, mixed lines, headings, ambiguous terms | Comprehensive catalog with deliberate decisions | Basic categories |

**Debate**:
- **B argues**: 20 documented edge cases with expected classifications and rationale. E13 and E15/E16 decisions are explicitly justified.
- **A argues**: 10 edge cases cover the key scenarios. Double negation mitigation with proximity window.
- **C argues**: Test cases demonstrate coverage. Edge case analysis is implicit.

**Winner**: **Variant B** (Confidence: 0.90)
- **Evidence**: B's edge case catalog is significantly more thorough. Documented deliberate decisions (E13, E15/E16) demonstrate careful consideration. This reduces implementation risk.

---

### Topic 7: Dataclass Changes

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Changes** | None | `classification_reason` field added | None |
| **Rationale** | Existing fields sufficient | Debuggability and auditability | Minimal change |

**Debate**:
- **B argues**: `classification_reason` enables debugging. Users can see WHY a term was classified.
- **A argues**: The `exempt` boolean and `severity` string suffice. Adding fields expands API surface.
- **C argues**: No changes needed. Keep it simple.

**Winner**: **Variant C** (Confidence: 0.80)
- **Evidence**: The `classification_reason` field is nice-to-have, not essential. Both A and C avoid dataclass changes. C's minimal approach is preferable.

---

### Topic 8: Complexity/Diff Size

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Estimated Lines** | ~160 lines | ~230 lines | ~120-140 lines |
| **New Functions** | `_is_meta_context()`, `_is_inside_inline_code()` | `_classify_meta_context()` | `_is_meta_context()` |
| **New Constants** | 4-5 regex patterns | 5-6 regex patterns | 2 regex patterns |

**Debate**:
- **C argues**: 120-140 lines is the sweet spot—solves the problem without over-engineering.
- **A argues**: 160 lines is reasonable for comprehensive coverage. Layered defense requires more code.
- **B argues**: 230 lines includes extensive tests. The core logic is ~75 lines.

**Winner**: **Variant C** (Confidence: 0.75)
- **Evidence**: C's estimate is 50% smaller than B's. While B includes more tests, the core logic difference is significant (35-40 lines vs 65-75 lines). For a scanner enhancement, minimal complexity is preferable.

---

### Topic 9: Completed Checklist Detection

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Detection** | Not addressed | `- [x]` prefix regex | Not addressed |
| **Rationale** | N/A | Completed items are not obligations | N/A |

**Debate**:
- **B argues**: `- [x] All mock services replaced` is a completed item, not an obligation. Detecting this reduces false positives.
- **A argues**: Completed checklists are rare. The existing discharge mechanism handles "replaced" verbs.
- **C argues**: Out of scope for minimal fix. Can be added later if needed.

**Winner**: **Variant B** (Confidence: 0.60)
- **Evidence**: B's detection is useful but narrow. It's a nice-to-have feature, not essential. Both A and C omit this without significant impact.

---

### Topic 10: Incremental Deployability

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Explicit Plan** | Yes (Layer 1, then Layer 2) | No (implicit) | No (implicit) |
| **Quick Win** | Code block exemption (~15 lines) | N/A | N/A |

**Debate**:
- **A argues**: Explicit 3-phase implementation. Layer 1 (code exemption) ships first as a quick win.
- **B argues**: Implementation sequence is documented (Section 8), but not framed as incremental deployment.
- **C argues**: Single-phase implementation. The fix is small enough to ship complete.

**Winner**: **Variant A** (Confidence: 0.85)
- **Evidence**: A explicitly structures implementation as incremental. This reduces risk and provides early value. B and C don't emphasize this.

---

## Topic Summary Table

| Topic | Winner | Confidence | Key Evidence |
|-------|--------|------------|--------------|
| 1. Severity Model | C | 0.75 | MEDIUM already works, no new concepts needed |
| 2. Function Return Type | B | 0.70 | Severity return is cleaner, though bool is simpler |
| 3. Risk Description Handling | C | 0.80 | Aligns with problem statement (false positive category) |
| 4. Code Block Handling | B | 0.75 | Preserves visibility for TODO comments in code |
| 5. Inline Code Detection | A | 0.65 | Generic approach handles all cases |
| 6. Edge Case Depth | B | 0.90 | 20 documented cases vs 10 |
| 7. Dataclass Changes | C | 0.80 | Minimal API surface changes |
| 8. Complexity/Diff Size | C | 0.75 | 120-140 lines vs 160-230 |
| 9. Completed Checklist Detection | B | 0.60 | Useful but narrow feature |
| 10. Incremental Deployability | A | 0.85 | Explicit phased plan reduces risk |

**Win Count**:
- Variant A: 2 wins (Topics 5, 10)
- Variant B: 4 wins (Topics 2, 4, 6, 9)
- Variant C: 4 wins (Topics 1, 3, 7, 8)

---

## Round 2: Rebuttals

### Advocate A Rebuttal

I concede B's edge case depth (Topic 6) and C's severity model (Topic 1) are well-reasoned. However, my incremental deployability (Topic 10) is a decisive advantage for risk management.

On code block handling (Topic 4), B's TODO concern is overstated. TODO comments in code blocks are themselves meta-context—comments about code, not executable obligations. My full exemption is correct.

On risk descriptions (Topic 3), C's MEDIUM demotion is safer than B's HIGH classification, but my full exemption is semantically correct. A risk description is never an obligation.

**Revised Position**: Adopt my incremental deployment structure, C's severity model (MEDIUM), and B's edge case analysis.

---

### Advocate B Rebuttal

I concede C's minimal diff size (Topic 8) and dataclass approach (Topic 7) are pragmatic. However, my edge case depth (Topic 6) is critical for correctness.

On severity model (Topic 1), INFO provides value beyond MEDIUM. MEDIUM implies "less important obligation"; INFO implies "not an obligation at all." This semantic distinction matters for report clarity.

On risk descriptions (Topic 3), my conservative bias is intentional. Risk statements imply existing scaffolding that needs addressing. C's MEDIUM demotion hides this; my HIGH classification surfaces it.

**Revised Position**: Adopt my edge case catalog and classification function structure, C's dataclass approach (no `classification_reason`), and A's incremental deployment plan.

---

### Advocate C Rebuttal

I concede B's edge case depth (Topic 6) and A's incremental deployability (Topic 10) are valuable. However, my minimal approach solves the core problem without over-engineering.

On severity model (Topic 1), INFO (B) and full exemption (A) are solutions looking for problems. MEDIUM works and is consistent.

On risk descriptions (Topic 3), B's HIGH classification contradicts the problem statement. My MEDIUM demotion is the correct balance.

On inline code detection (Topic 5), A's generic approach adds complexity for marginal benefit. Most inline code is in verification criteria covered by my negation patterns.

**Revised Position**: Adopt B's edge case analysis methodology, A's incremental deployment structure, and my minimal implementation approach.

---

## Final Consensus Points

All advocates agree on:
1. **Positional negation checking**: Negation must precede the scaffold term on the same line.
2. **Fail-safe default**: When uncertain, treat as obligation (HIGH severity).
3. **Backward compatibility**: No breaking changes to public API.
4. **Shell command detection**: Grep/find/sed/awk lines are meta-context.
5. **Test coverage**: Parameterized tests for each false positive category.

Key disagreements:
1. **Severity for meta-context**: Exempt (A) vs INFO (B) vs MEDIUM (C)
2. **Risk description handling**: Exempt (A) vs HIGH (B) vs MEDIUM (C)
3. **Code block handling**: Full exemption (A) vs MEDIUM (B, C)
4. **Implementation size**: Comprehensive (A, B) vs minimal (C)
