# Adversarial Diff Analysis: 3 Proposals for False Positive Mitigation

**Date**: 2026-04-03  
**Scope**: Comparing Variant A (Brainstorm), Variant B (Design), and Variant C (Improve) for obligation scanner enhancement  
**Output Location**: `/config/workspace/IronClaude/.dev/releases/backlog/prd-skill-refactor/adversarial/diff-analysis.md`

---

## 1. Structural Differences

### 1.1 Document Organization

| Aspect | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|--------|------------------------|--------------------|---------------------|
| **Primary Structure** | Alternatives A-F exploration, then recommendation | Hierarchical design spec (Problem → Design → Edge Cases → API → Tests) | Root cause → Fix recommendation → Risk assessment |
| **Layer Hierarchy** | 3 layers (Code → Negation → Manual) | 4 layers (L0-L4 structural → negation → command → gate) | 2 layers (Negation regex + Shell command regex) |
| **Edge Case Presentation** | 10 edge cases as narrative discussion | 20 edge cases in formal catalog table with IDs (E1-E20) | 10 test cases implied, not enumerated as edge cases |
| **Return Type** | `_is_meta_context() -> bool` | `_classify_meta_context() -> str` (severity) | `_is_meta_context() -> bool` |
| **Code Placement** | Inline sketch in proposal | Full implementation with constants and function signature | Minimal code block (~35 lines) |
| **Test Plan Detail** | Estimated test line counts only | Full parameterized test code with 12+ cases | High-level test descriptions (no code) |
| **Migration Section** | None | Section 6: Migration / Backward Compatibility | None |
| **API Surface Documentation** | None | Section 4: Full API changes table | None |

### 1.2 Severity Rating: Structural Completeness

| Variant | Completeness Score | Rationale |
|---------|-------------------|-----------|
| **A** | MEDIUM | Good exploration of alternatives, but lacks formal API documentation and migration guidance |
| **B** | HIGH | Comprehensive structure with all sections (design, edge cases, API, tests, migration, alternatives considered) |
| **C** | LOW | Minimal structure focused on immediate fix; defers complexity to Phase 2 |

---

## 2. Content Differences

### 2.1 Approach to Meta-Context Detection

| Topic | Variant A | Variant B | Variant C |
|-------|-----------|-----------|-----------|
| **Core Mechanism** | Composite: Code exemption + Negation-aware classifier | 4-layer classifier returning severity directly | 2 compiled regexes + boolean check |
| **Code Block Handling** | Upgrade from MEDIUM demotion to full exemption (Layer 1) | Keep MEDIUM demotion (L0), add INFO for inline code (L1a) | Accepts existing MEDIUM demotion |
| **Inline Code Handling** | Layer 1b: Full exemption via `_is_inside_inline_code()` | L1a: Returns "INFO" severity | Not mentioned |
| **Negation Detection** | Positional: negation must precede term | Positional: prefix check before match position | Positional: prefix check before match position |
| **Proximity Window** | Proposes 4-word window fix for double-negation | Uses 4-5 word window in patterns | Not specified |
| **Past Tense Handling** | Included in `_META_CONTEXT_INDICATORS` | Dedicated pattern in `_NEGATION_PREFIXES[3]` | Included in mega-regex |
| **Risk/Warning Handling** | Pattern matches "risk:" prefix | E13 deliberate decision: risk stays HIGH (conservative) | Included in mega-regex (demoted to MEDIUM) |
| **Shell Commands** | `_SHELL_CMD_RE` separate check | `_COMMAND_LINE_RE` as L3 | `_SHELL_CMD_RE` separate check |
| **Completed Checklist** | Not mentioned | L1b: `- [x]` pattern returns INFO | Not mentioned |
| **Gate Criteria** | Included in meta-context indicators | L4: Dedicated `_GATE_CRITERIA_RE` | Included in mega-regex |

### 2.2 Severity Levels and Classification

| Aspect | Variant A | Variant B | Variant C |
|--------|-----------|-----------|-----------|
| **Severity Levels** | HIGH, MEDIUM (existing) + exempt flag | HIGH, MEDIUM, **INFO** (new) | HIGH, MEDIUM (existing only) |
| **Meta-Context Result** | `exempt = True` (full exemption) | `severity = "INFO"` (new level) | `severity = "MEDIUM"` (reuse existing) |
| **undischarged_count Logic** | Excludes exempt obligations | Excludes both MEDIUM and INFO | Excludes MEDIUM (unchanged) |
| **New Dataclass Fields** | None | `classification_reason: str = ""` | None |

### 2.3 Implementation Scope

| Metric | Variant A | Variant B | Variant C |
|--------|-----------|-----------|-----------|
| **Scanner Lines** | ~80 | ~76 | ~35-40 |
| **Test Lines** | ~80 | ~150 | ~80-100 |
| **Dataclass Changes** | 0 | +1 field | 0 |
| **Total Diff** | ~160 lines | ~230 lines | ~120-140 lines |
| **New Constants** | 3 (`_META_CONTEXT_INDICATORS`, `_SHELL_CMD_RE`, `_INLINE_CODE_RE`) | 5 (`_NEGATION_PREFIXES` list, `_COMMAND_LINE_RE`, `_GATE_CRITERIA_RE`, `_INLINE_CODE_RE`, `_COMPLETED_CHECKLIST_RE`) | 2 (`_NEGATION_PREFIX_RE`, `_SHELL_CMD_RE`) |
| **New Functions** | 2 (`_is_meta_context()`, `_is_inside_inline_code()`) | 1 (`_classify_meta_context()`) | 1 (`_is_meta_context()`) |

### 2.4 Deployment Strategy

| Variant | Strategy |
|---------|----------|
| **A** | Incremental: Layer 1 ships first (~15 lines), Layer 2 follows (~65 lines) |
| **B** | Monolithic: All 4 layers ship together with full test suite |
| **C** | Single phase: Phase 1 only; Phase 2 items explicitly deferred |

### 2.5 Deferred/Future Work

| Variant | Deferred Items |
|---------|----------------|
| **A** | Proximity-based negation (optional ~10 lines) |
| **B** | Multi-line context window (Section 9.4), NLP analysis (Section 9.2) |
| **C** | Semantic scoring, configurable terms, NLP parsing (Phase 2) |

---

## 3. Contradictions

### 3.1 Direct Oppositions

| Subject | Variant A Claim | Variant B Claim | Variant C Claim | Assessment |
|---------|-----------------|-----------------|-----------------|------------|
| **Risk descriptions** | Should be exempted (Layer 2 pattern matches "risk:") | Should stay HIGH (E13 deliberate decision: "risk statement implies placeholder EXISTS") | Should be demoted to MEDIUM (included in mega-regex) | **Fundamental disagreement**: A and C demote risks; B preserves them as HIGH |
| **Code block handling** | Upgrade to full exemption (exempt=True) | Keep MEDIUM demotion, add INFO for other cases | Accept existing MEDIUM demotion | **Tactical difference**: A is more aggressive; B introduces INFO level; C is conservative |
| **Double negation** | "Do not skip the placeholder" would be false negative (bad); proposes 4-word window fix | "Do not remove the mock yet" correctly stays HIGH (E16) because negation check only looks BEFORE term | Not discussed | **A sees problem B solves**: B's positional check handles double negation correctly |
| **Severity for meta-context** | Exempt (full exclusion) | INFO (logged but excluded from count) | MEDIUM (existing level) | **Architectural difference**: A removes from report; B adds transparency; C reuses existing |

### 3.2 Severity Assessment Disagreements

| Edge Case | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| "Risk: placeholder data could leak" | Exempt (Layer 2) | HIGH (E13 deliberate) | MEDIUM (mega-regex) |
| "The placeholder should not be committed" | Would check position | HIGH (E15 deliberate: negation AFTER term) | Not discussed |
| "Never deploy with hardcoded credentials" | Exempt | INFO (E20: L2 negation) | MEDIUM (mega-regex includes "never") |
| Inline code `` `placeholder` `` | Exempt (Layer 1b) | INFO (L1a) | Not mentioned |
| Completed checklist `- [x] mock replaced` | Not mentioned | INFO (L1b) | Not mentioned |

### 3.3 Implementation Approach Tensions

| Tension | Description |
|---------|-------------|
| **A vs B on complexity** | A argues for layered defense with incremental deployment; B argues for comprehensive 4-layer classifier with full test coverage upfront |
| **B vs C on new severity level** | B introduces INFO level for transparency; C explicitly avoids new levels to minimize change surface |
| **A vs C on regex strategy** | A uses multiple focused patterns; C uses "mega-regex" combining all patterns |
| **A vs B on risk handling** | A prioritizes reducing false positives (exempt risks); B prioritizes conservative safety (keep risks as HIGH) |

---

## 4. Unique Contributions

### 4.1 Ideas Unique to Variant A (Brainstorm)

| Contribution | Value | Assessment |
|--------------|-------|------------|
| **Alternatives A-E exploration** | Documents 5 rejected approaches with pros/cons | HIGH - Shows due diligence and prevents circular discussion |
| **Incremental deployment plan** | Layer 1 (15 lines) quick win, Layer 2 (65 lines) follow-up | HIGH - Reduces risk, enables faster shipping |
| **Double-negation edge case identification** | "Do not skip the placeholder" as false negative risk | MEDIUM - B solves this via positional check |
| **4-word proximity window proposal** | Refinement to handle negation distance | MEDIUM - Addresses real edge case |
| **Discharge verb recognition** | Suggests adding discharge verbs to meta-context indicators | LOW - Not fully developed |

### 4.2 Ideas Unique to Variant B (Design)

| Contribution | Value | Assessment |
|--------------|-------|------------|
| **INFO severity level** | New level below MEDIUM for meta-context transparency | HIGH - Enables reporting without gate blocking |
| **`classification_reason` field** | Debuggability enhancement on Obligation dataclass | HIGH - Critical for understanding scanner decisions |
| **20-case edge case catalog (E1-E20)** | Comprehensive test coverage specification | HIGH - Ensures no regressions, documents decisions |
| **Deliberate decisions documented** | E13 (risk stays HIGH), E15/E16 (negation-after-term stays HIGH) | HIGH - Shows principled trade-offs |
| **API surface changes table** | Section 4 documents all public API impacts | HIGH - Critical for backward compatibility assessment |
| **Migration / backward compatibility section** | Section 6 addresses zero migration, over-suppression risk | HIGH - Production readiness |
| **4-layer classifier architecture** | L0-L4 with clear precedence rules | MEDIUM - More structured than A's 3 layers |
| **Completed checklist detection** | `- [x]` pattern as L1b | MEDIUM - Handles real use case others miss |
| **Deprecation plan for `_determine_severity()`** | Explicit migration path for old function | LOW - Nice to have |

### 4.3 Ideas Unique to Variant C (Improve)

| Contribution | Value | Assessment |
|--------------|-------|------------|
| **Minimal line count** | ~120-140 total vs ~160 (A) vs ~230 (B) | MEDIUM - Faster review, less risk |
| **Mega-regex approach** | Single `_NEGATION_PREFIX_RE` combining all patterns | LOW - Less maintainable than separate patterns |
| **Explicit Phase 1/Phase 2 separation** | Clear scope boundary with deferred items listed | MEDIUM - Helps focus implementation |
| **Risk assessment table** | Likelihood/Impact/Mitigation for 4 risks | MEDIUM - Good for review, others lack this |
| **"Key safety property" statement** | Fix can only REDUCE false positives | LOW - Implicit in other proposals |

### 4.4 Value Assessment Summary

| Variant | Highest Value Unique Contribution | Overall Innovation |
|---------|-----------------------------------|-------------------|
| **A** | Incremental deployment plan | MEDIUM - Good process, conservative technical approach |
| **B** | INFO severity + classification_reason + edge case catalog | HIGH - Most comprehensive and production-ready |
| **C** | Minimal scope discipline | LOW - Conservative, defers complexity |

---

## 5. Shared Assumptions

### 5.1 Explicit Agreement Points

| Assumption | Evidence |
|------------|----------|
| **Positional negation check** | All three use negation word position relative to scaffold term (before/after) |
| **Prefix-based analysis** | All three check `line[:term_start_in_line]` for negation patterns |
| **Shell command detection** | All three include grep/find/sed/awk/rg patterns |
| **Backward compatibility** | All three state changes only demote severity, never increase |
| **`# obligation-exempt` preservation** | All three keep existing manual escape hatch |
| **Code block awareness** | All three acknowledge existing code block handling |
| **Single-line analysis** | All three focus on the line containing the match (no multi-line context) |
| **Fail-safe default** | All three treat unmatched cases as obligations (conservative) |
| **Regex-based solution** | All three reject NLP/heavy dependencies |
| **Past-tense handling** | All three include removed/replaced/eliminated patterns |

### 5.2 Implicit Preconditions

| Precondition | Evidence | Risk if Violated |
|--------------|----------|------------------|
| **Scanner is regex-based** | All proposals use regex constants | Would need complete rewrite if scanner changes architecture |
| **`undischarged_count` excludes MEDIUM** | B explicitly mentions this; A/C rely on it | If this changes, all severity demotion logic breaks |
| **Roadmap format is markdown** | All examples use markdown syntax | Would not work with other formats |
| **Scaffold terms are in SCAFFOLD_TERMS constant** | All proposals reference this | Assumes centralized term list |
| **Obligation dataclass can be extended** | B adds field; A/C assume no changes | C's minimal approach assumes frozen dataclass |
| **Test file location is `tests/roadmap/`** | All specify this path | Assumes existing test structure |
| **Performance is not a concern** | None discuss regex optimization | Mega-regex (C) could have edge case performance issues |
| **English language content** | All patterns are English-specific | Would not work for localized roadmaps |

### 5.3 Consensus on Problem Scope

| Aspect | Consensus |
|--------|-----------|
| **Primary problem** | False positives when scaffold terms appear in meta-contexts |
| **Six categories** | All identify: verification, shell commands, code examples, negation, historical, risk |
| **Root cause** | Flat regex matching without semantic context |
| **Solution type** | Context-aware classification before severity assignment |
| **Safety priority** | Conservative bias: better to have false positive than false negative |

---

## 6. Summary Matrix

| Dimension | Variant A (Brainstorm) | Variant B (Design) | Variant C (Improve) |
|-----------|------------------------|--------------------|---------------------|
| **Philosophy** | Layered defense, incremental | Comprehensive, production-ready | Minimal, focused |
| **Complexity** | Medium (~160 lines) | High (~230 lines) | Low (~120-140 lines) |
| **Innovation** | Incremental deployment plan | INFO level + classification_reason + edge case catalog | Minimal scope |
| **Risk handling** | Exempt (aggressive) | HIGH (conservative) | MEDIUM (moderate) |
| **New severity level** | No | Yes (INFO) | No |
| **Dataclass changes** | No | Yes (classification_reason) | No |
| **Test coverage** | Good (~80 lines) | Excellent (~150 lines, 20 cases) | Adequate (~80-100 lines) |
| **Documentation** | Good (alternatives explored) | Excellent (API, migration, edge cases) | Minimal |
| **Deployment** | Incremental (2 phases) | Monolithic | Single phase |
| **Best for** | Risk-averse rollout | Production systems requiring transparency | Quick fix, limited review bandwidth |

---

*Analysis completed: Step 1 of adversarial protocol*
