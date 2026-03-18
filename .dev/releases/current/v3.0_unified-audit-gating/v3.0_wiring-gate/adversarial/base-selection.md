---
title: "Hybrid Scoring — Base Selection"
timestamp: 2026-03-18T00:00:00Z
step: 3
protocol: adversarial-debate
selected_base: B (spec2.md)
---

# Step 3: Hybrid Scoring — Base Selection

## 1. Quantitative Metrics (50% weight)

### 1.1 Requirement Coverage (30%)

Requirements derived from the combined goals across all three variants:

| Requirement | A | B | C |
|-------------|---|---|---|
| R1: Detect unwired Optional[Callable]=None | Y | Y | Y |
| R2: Detect orphan modules | Y | Y | Y |
| R3: Detect unregistered dispatch entries | Y | Y | Y |
| R4: Emit GateCriteria/SemanticCheck-compatible report | Y | Y | Y |
| R5: Shadow/soft/full rollout | Y | Y | Y |
| R6: Integrate into roadmap _build_steps() | Y | Y | Y |
| R7: Extend audit-analyzer (no new agents) | Y | Y | Y |
| R8: Preserve pipeline/* layering (NFR-007) | Y | Y | Y |
| R9: Deterministic analysis, not LLM | Y | Y | Y |
| R10: Sprint integration (post-task hook) | N | Y | Y |
| R11: ToolOrchestrator AST plugin | N | Y | Y |
| R12: Mode-aware semantic checks (blocking_findings) | Y | Y | N |
| R13: Whitelist/suppression mechanism | Y | Y | Y |
| R14: Pre-activation checklist | N | Y | Y |
| R15: Resume behavior documented | Y | Y | N |
| R16: Deviation count reconciliation | N | N | Y |
| R17: Coordination notes (merge conflict risk) | N | N | Y |
| R18: FPR calibration formula | N | N | Y |
| R19: YAML injection prevention | N | Y | N |
| R20: _get_all_step_ids() update | Y | Y | N |

| Variant | Covered | Total | Score |
|---------|---------|-------|-------|
| A | 14 | 20 | 0.70 |
| B | 17 | 20 | 0.85 |
| C | 16 | 20 | 0.80 |

### 1.2 Internal Consistency (25%)

Evaluated as `1 - (contradictions / total claims)`:

**Variant A**:
- Claims WIRING_VERIFICATION_GATE lives in roadmap/gates.py (Section 5.2) but semantic checks reference audit-specific concepts (rollout_mode, wiring categories) -- creates cohesion tension.
- Uses nested severity_summary YAML block in frontmatter (Section 7.2) but _check_frontmatter() does flat key extraction -- interaction risk (INV-014).
- Contradictions: 2 / ~85 claims = 0.976

**Variant B**:
- report.passed (zero findings) vs gate pass (mode-dependent) semantic gap acknowledged (X-006) but not fully resolved in the spec text.
- Contradictions: 1 / ~110 claims = 0.991

**Variant C**:
- Per-category-zero semantic checks (Section 8) would break shadow mode when grace_period=0 forces BLOCKING (INV-006) -- fundamental design flaw.
- Uses enforcement_mode while B uses rollout_mode -- inconsistent with frontmatter field naming conventions.
- Does not mention _get_all_step_ids() update -- incomplete integration.
- Contradictions: 3 / ~95 claims = 0.968

| Variant | Score |
|---------|-------|
| A | 0.976 |
| B | 0.991 |
| C | 0.968 |

### 1.3 Specificity Ratio (15%)

Counting concrete vs vague statements (code references, line numbers, exact field names, algorithm steps vs "should", "can", "may" without detail):

**Variant A**: Strong on rationale and design reasoning but lighter on implementation specifics. No code-level data models, no algorithm pseudocode for detection. ~62% concrete.

**Variant B**: Provides full data model code, algorithm pseudocode for all three detectors, AST analyzer plugin code, gate definition code, Step definition code, exact line numbers, LOC estimates per file. ~82% concrete.

**Variant C**: Provides data model code, algorithm pseudocode, gate definition code, Step definition code, LOC estimates. Missing ToolOrchestrator implementation detail. ~74% concrete.

| Variant | Score |
|---------|-------|
| A | 0.62 |
| B | 0.82 |
| C | 0.74 |

### 1.4 Dependency Completeness (15%)

Internal references resolved (e.g., when a section references another section, file, or symbol, does the target exist in the spec?):

**Variant A**: References "cleanup-audit infrastructure" and "audit-analyzer" but does not specify which agent files or what fields to add (vague delegation). References config module without specifying its location or content. 3 unresolved / ~25 references = 0.88.

**Variant B**: References ToolOrchestrator with specific file location and injection seam. References all pipeline substrate symbols with exact line numbers. References agent files by name. 1 unresolved / ~35 references (FileAnalysis import path assumes tool_orchestrator.py location) = 0.971.

**Variant C**: References ToolOrchestrator but with less implementation detail. References agent specs. Does not resolve the gate_mode interaction with resolve_gate_mode(). 2 unresolved / ~28 references = 0.929.

| Variant | Score |
|---------|-------|
| A | 0.880 |
| B | 0.971 |
| C | 0.929 |

### 1.5 Section Coverage (15%)

Distinct sections present vs maximum across all three:

Maximum sections (union): Problem, Goals/Non-Goals, Design Constraints, Architecture, Detailed Design/Detection Design, Data Models, Report Format, Gate Definition, Rollout Model, Executor Behavior/Integration, Cleanup-Audit Integration, False Positive Governance, File Manifest, Interface Contracts, Risk Assessment, Testing Strategy, Success Criteria, Tasklist Index, Decisions, Coordination Notes, Appendices = 21

**Variant A**: 15 sections (Problem, Objective, Constraints, Architecture Reality, Proposed Architecture, Detection Design, Report Design, Rollout, Executor Behavior, FP Governance, File Manifest, Success Criteria, Decisions, Out of Scope, Follow-on Tasklist) = 15/21 = 0.714

**Variant B**: 19 sections (Problem, Goals, Constraints, Architecture, Detailed Design, Report Format, Gate Definition, Rollout, Interface Contracts, Risk Assessment, Testing Strategy, Success Criteria, File Manifest, Tasklist Index, Decisions, Cleanup-Audit Integration, Appendix A/B/C) = 19/21 = 0.905

**Variant C**: 18 sections (Problem, Goals, Constraints, Architecture, Detection Design, Data Models, Report Format, Gate Definition, Rollout, Companion, FP Governance, File Manifest, Interface Contracts, Risk Assessment, Testing Strategy, Tasklist Index, Success Criteria, Coordination Notes) = 18/21 = 0.857

| Variant | Score |
|---------|-------|
| A | 0.714 |
| B | 0.905 |
| C | 0.857 |

### 1.6 Quantitative Summary

| Metric | Weight | A | B | C |
|--------|--------|---|---|---|
| Requirement Coverage | 0.30 | 0.700 | 0.850 | 0.800 |
| Internal Consistency | 0.25 | 0.976 | 0.991 | 0.968 |
| Specificity Ratio | 0.15 | 0.620 | 0.820 | 0.740 |
| Dependency Completeness | 0.15 | 0.880 | 0.971 | 0.929 |
| Section Coverage | 0.15 | 0.714 | 0.905 | 0.857 |
| **Weighted Total** | **1.00** | **0.784** | **0.907** | **0.861** |

---

## 2. Qualitative Metrics (50% weight) -- 30-Criterion Binary Rubric

### 2.1 Completeness (5 criteria)

#### Criterion 1: Covers all stated requirements

- **A**: CLAIM: Covers 7 of 8 goals. EVIDENCE: Missing sprint integration, ToolOrchestrator plugin. VERDICT: NOT MET (0)
- **B**: CLAIM: Covers all 8 goals with verification traceability. EVIDENCE: Goals table maps each goal to a success criterion. VERDICT: MET (1)
- **C**: CLAIM: Covers 7 goals. EVIDENCE: Missing mode-aware enforcement, has deviation reconciliation instead. VERDICT: NOT MET (0)

#### Criterion 2: Edge cases identified and addressed

- **A**: CLAIM: Identifies 5 FP noise sources (Section 10.1). EVIDENCE: Lists lifecycle hooks, config-driven registries, re-exports, reflection, test-only seams. VERDICT: MET (1)
- **B**: CLAIM: Identifies FP sources with quantified FPR estimates. EVIDENCE: "30-70% FPR contribution" for alias issue, pre-activation checklist for zero-findings. VERDICT: MET (1)
- **C**: CLAIM: Identifies noise sources with FPR table. EVIDENCE: Table with expected FPR per source, v1.0 mitigation, planned fix column. VERDICT: MET (1)

#### Criterion 3: Dependencies identified

- **A**: CLAIM: Dependencies on pipeline substrate documented. EVIDENCE: Section 3.1 lists exact symbols and paths. VERDICT: MET (1)
- **B**: CLAIM: Full substrate reference with line numbers. EVIDENCE: Section 3.1 table with 7 symbols, exact locations, contracts. Appendix A repeats with 15 symbols. VERDICT: MET (1)
- **C**: CLAIM: Dependencies identified. EVIDENCE: Section 3.1-3.2 list substrate symbols, Section 13.3 dependency direction. VERDICT: MET (1)

#### Criterion 4: Success criteria defined

- **A**: CLAIM: 9 success criteria. EVIDENCE: Section 12 lists SC-1 through SC-9. VERDICT: MET (1)
- **B**: CLAIM: 14 success criteria with verification method. EVIDENCE: Section 11 table with SC-001 through SC-014. VERDICT: MET (1)
- **C**: CLAIM: 12 success criteria. EVIDENCE: Section 17 table with SC-001 through SC-012. VERDICT: MET (1)

#### Criterion 5: Scope boundaries clear (in-scope and out-of-scope)

- **A**: CLAIM: Section 14 lists 6 out-of-scope items. EVIDENCE: Clear list including cross-language, runtime tracing, auto-remediation. VERDICT: MET (1)
- **B**: CLAIM: Section 2 Non-Goals lists 7 items. Appendix C repeats with 7 items. EVIDENCE: Explicit exclusions with rationale. VERDICT: MET (1)
- **C**: CLAIM: Section 2 Non-Goals lists 6 items. EVIDENCE: Clear exclusions. VERDICT: MET (1)

| Criterion | A | B | C |
|-----------|---|---|---|
| 1. Covers requirements | 0 | 1 | 0 |
| 2. Edge cases | 1 | 1 | 1 |
| 3. Dependencies | 1 | 1 | 1 |
| 4. Success criteria | 1 | 1 | 1 |
| 5. Scope boundaries | 1 | 1 | 1 |
| **Subtotal** | **4/5** | **5/5** | **4/5** |

### 2.2 Correctness (5 criteria)

#### Criterion 6: No factual errors

- **A**: CLAIM: Accurate substrate references. EVIDENCE: Line numbers for _build_steps(), gate_passed(), SemanticCheck match code analysis. Minor: places gate in roadmap/gates.py which creates suboptimal dependency direction. VERDICT: MET (1) -- placement is a design choice, not a factual error.
- **B**: CLAIM: Accurate with exact line numbers. EVIDENCE: Cross-verified in debate transcript. R8 risk correctly identifies resolve_gate_mode() interaction. VERDICT: MET (1)
- **C**: CLAIM: Accurate references. EVIDENCE: Line number references match. However, per-category-zero semantic checks would fail under grace_period=0 BLOCKING (INV-006) -- this is a design error with operational consequences. VERDICT: NOT MET (0)

#### Criterion 7: Feasible within stated constraints

- **A**: CLAIM: Feasible, reuses existing substrate. EVIDENCE: No pipeline/* changes, extends existing patterns. VERDICT: MET (1)
- **B**: CLAIM: Feasible, 480-580 LOC. EVIDENCE: LOC estimates per file, all within single-sprint scope. ToolOrchestrator plugin adds risk but is a parallel track. VERDICT: MET (1)
- **C**: CLAIM: Feasible, 360-430 LOC. EVIDENCE: Smaller scope, lower risk. VERDICT: MET (1)

#### Criterion 8: Consistent terminology

- **A**: CLAIM: Uses WIRING_VERIFICATION_GATE naming. EVIDENCE: Consistent throughout but differs from B/C naming convention. Uses "rollout_mode" consistently. VERDICT: MET (1)
- **B**: CLAIM: Uses WIRING_GATE naming. EVIDENCE: Consistent throughout. Uses "rollout_mode" consistently. VERDICT: MET (1)
- **C**: CLAIM: Uses WIRING_GATE naming. EVIDENCE: Uses "enforcement_mode" in frontmatter (Section 7) but "wiring_gate_mode" in config. Two different terms for related concepts without clear distinction. VERDICT: NOT MET (0)

#### Criterion 9: No internal contradictions

- **A**: CLAIM: Internally consistent. EVIDENCE: nested severity_summary block conflicts with flat key extraction (INV-014). VERDICT: NOT MET (0)
- **B**: CLAIM: Internally consistent. EVIDENCE: No contradictions found in debate analysis. VERDICT: MET (1)
- **C**: CLAIM: Internally consistent. EVIDENCE: Per-category-zero checks contradict shadow-mode goal under BLOCKING (INV-006). VERDICT: NOT MET (0)

#### Criterion 10: Claims backed by evidence

- **A**: CLAIM: References generated analysis documents. EVIDENCE: Section 1 cites specific files, Section 4 cites exact source paths. VERDICT: MET (1)
- **B**: CLAIM: References Phase 1 findings with counts. EVIDENCE: "32 unwired symbols across 14 files" with categorized table. Appendix B forensic cross-reference. VERDICT: MET (1)
- **C**: CLAIM: References Phase 1 findings. EVIDENCE: "32 unwired symbols across 14 files" table, specific examples. VERDICT: MET (1)

| Criterion | A | B | C |
|-----------|---|---|---|
| 6. No errors | 1 | 1 | 0 |
| 7. Feasible | 1 | 1 | 1 |
| 8. Consistent terms | 1 | 1 | 0 |
| 9. No contradictions | 0 | 1 | 0 |
| 10. Evidence-backed | 1 | 1 | 1 |
| **Subtotal** | **4/5** | **5/5** | **2/5** |

### 2.3 Structure (5 criteria)

#### Criterion 11: Logical section ordering

- **A**: CLAIM: Problem -> Objective -> Constraints -> Architecture -> Detection -> Report -> Rollout -> Executor. EVIDENCE: Flows from why to what to how. VERDICT: MET (1)
- **B**: CLAIM: Problem -> Goals -> Constraints -> Architecture -> Detailed Design -> Report -> Gate -> Rollout -> Interface -> Risk -> Testing -> Success -> Manifest -> Tasklist. EVIDENCE: Comprehensive flow with appendices. VERDICT: MET (1)
- **C**: CLAIM: Problem -> Goals -> Constraints -> Architecture -> Detection -> Data Models -> Report -> Gate -> Rollout -> Companion -> FP -> Manifest -> Interface -> Risk -> Testing -> Tasklist -> Success -> Coordination. EVIDENCE: Logical but "Companion" (Section 10) breaks the flow of the wiring gate topic with an orthogonal feature. VERDICT: NOT MET (0)

#### Criterion 12: Consistent heading hierarchy

- **A**: CLAIM: H1 -> H2 -> H3 hierarchy. EVIDENCE: Sections use ## for major sections, ### for subsections. Some sections (5, 6, 7, 8) use ## instead of ### for subsections, breaking hierarchy. VERDICT: NOT MET (0)
- **B**: CLAIM: H1 -> H2 -> H3 -> H4 hierarchy. EVIDENCE: Consistent throughout with clear nesting. VERDICT: MET (1)
- **C**: CLAIM: H2 -> H3 hierarchy. EVIDENCE: Consistent section numbering. VERDICT: MET (1)

#### Criterion 13: Separation of concerns

- **A**: CLAIM: Analysis, emission, enforcement separated. EVIDENCE: Section 3.3 explicitly defines three layers. VERDICT: MET (1)
- **B**: CLAIM: Three layers separated, named modes for operation contexts. EVIDENCE: Section 3.3 + Section 4.3 dual-mode. VERDICT: MET (1)
- **C**: CLAIM: Three layers separated. EVIDENCE: Section 3.3 defines layers, architecture diagram shows separation. VERDICT: MET (1)

#### Criterion 14: Navigation aids (tables, diagrams, cross-references)

- **A**: CLAIM: Includes ASCII architecture diagrams. EVIDENCE: Limited tables, no cross-reference appendix. VERDICT: NOT MET (0)
- **B**: CLAIM: Tables, diagrams, appendices, cross-references. EVIDENCE: Substrate reference table, forensic cross-reference appendix, architecture diagrams, goal-to-SC traceability. VERDICT: MET (1)
- **C**: CLAIM: Tables, diagrams, data flow. EVIDENCE: ASCII data flow diagram, multiple tables, dependency direction diagram. VERDICT: MET (1)

#### Criterion 15: Follows spec conventions

- **A**: CLAIM: Follows release spec conventions. EVIDENCE: Has frontmatter, numbered sections, file manifest. Missing risk assessment, testing strategy as dedicated sections. VERDICT: NOT MET (0)
- **B**: CLAIM: Follows release spec conventions. EVIDENCE: Full frontmatter, numbered sections, all standard sections present. VERDICT: MET (1)
- **C**: CLAIM: Follows release spec conventions. EVIDENCE: Full frontmatter, numbered sections, standard sections. VERDICT: MET (1)

| Criterion | A | B | C |
|-----------|---|---|---|
| 11. Logical ordering | 1 | 1 | 0 |
| 12. Consistent hierarchy | 0 | 1 | 1 |
| 13. Separation of concerns | 1 | 1 | 1 |
| 14. Navigation aids | 0 | 1 | 1 |
| 15. Conventions | 0 | 1 | 1 |
| **Subtotal** | **2/5** | **5/5** | **4/5** |

### 2.4 Clarity (5 criteria)

#### Criterion 16: Unambiguous language

- **A**: CLAIM: Clear design language. EVIDENCE: Uses "suggested" and "recommended" in places where decisions should be firm (e.g., "Suggested public surface" in Section 5.1). VERDICT: NOT MET (0)
- **B**: CLAIM: Decisive language. EVIDENCE: Uses "MUST", "CREATE", "MODIFY" consistently. Requirements table uses imperative. VERDICT: MET (1)
- **C**: CLAIM: Clear language. EVIDENCE: Mostly decisive. Some ambiguity around sprint integration details ("..." placeholder in code). VERDICT: MET (1)

#### Criterion 17: Concrete examples

- **A**: CLAIM: Lists known unwired symbols. EVIDENCE: Section 6.1-6.3 list specific files and symbols as initial examples. VERDICT: MET (1)
- **B**: CLAIM: Pattern-matched examples with code. EVIDENCE: Section 5.2.1 shows PortifyExecutor code pattern with actual class/param names. VERDICT: MET (1)
- **C**: CLAIM: Pattern-matched examples. EVIDENCE: Section 5.1-5.3 include code examples and known findings. VERDICT: MET (1)

#### Criterion 18: Purpose stated for each component

- **A**: CLAIM: Responsibilities listed per module. EVIDENCE: Section 5.1 lists module responsibilities. VERDICT: MET (1)
- **B**: CLAIM: Purpose column in file manifest, purpose statements in design. EVIDENCE: Section 12 file manifest has purpose column. Each function has docstring-level purpose. VERDICT: MET (1)
- **C**: CLAIM: Purpose in file manifest and sections. EVIDENCE: Section 12 has purpose column. Architecture sections state purpose per module. VERDICT: MET (1)

#### Criterion 19: Terms defined before use

- **A**: CLAIM: Terms introduced in context. EVIDENCE: "Wiring finding", "wiring report" introduced at point of use in Section 5.1. "Shadow/soft/full" defined in Section 8. VERDICT: MET (1)
- **B**: CLAIM: Formal data model section defines terms. EVIDENCE: Section 5.1 defines WiringFinding, WiringReport with code. Modes defined in Sections 4.3 and 5.5. VERDICT: MET (1)
- **C**: CLAIM: Section 6 defines data models before use. EVIDENCE: Separate Data Models section before Report Format and Gate Definition. VERDICT: MET (1)

#### Criterion 20: Actionable next steps

- **A**: CLAIM: Follow-on tasklist shape provided. EVIDENCE: Section 15 lists 4 implementation tracks with critical path. VERDICT: MET (1)
- **B**: CLAIM: Tasklist index with dependencies and LOC. EVIDENCE: Section 13 table with 12 tasks, dependencies, LOC estimates, critical path. VERDICT: MET (1)
- **C**: CLAIM: Tasklist index with parallel tracks. EVIDENCE: Section 16 table with 13 tasks, dependencies, parallel tracks identified. VERDICT: MET (1)

| Criterion | A | B | C |
|-----------|---|---|---|
| 16. Unambiguous | 0 | 1 | 1 |
| 17. Concrete examples | 1 | 1 | 1 |
| 18. Purpose stated | 1 | 1 | 1 |
| 19. Terms defined | 1 | 1 | 1 |
| 20. Actionable | 1 | 1 | 1 |
| **Subtotal** | **4/5** | **5/5** | **5/5** |

### 2.5 Risk Coverage (5 criteria)

#### Criterion 21: At least 3 risks identified

- **A**: CLAIM: No formal risk section. EVIDENCE: Risks are scattered across sections (FP governance in Section 10, rollout caveats in Section 8). VERDICT: NOT MET (0) -- no consolidated risk assessment.
- **B**: CLAIM: 8 risks in formal table. EVIDENCE: Section 9, R1-R8 with Likelihood/Impact/Mitigation. VERDICT: MET (1)
- **C**: CLAIM: 7 risks in formal table. EVIDENCE: Section 14, R1-R7 with Likelihood/Impact/Mitigation. VERDICT: MET (1)

#### Criterion 22: Mitigations specified

- **A**: CLAIM: Mitigations described in context. EVIDENCE: Whitelist, suppression policy discussed but not linked to specific risk entries. VERDICT: NOT MET (0)
- **B**: CLAIM: Each risk has mitigation column. EVIDENCE: R1: "Whitelist; shadow calibration", R5: "Pre-activation checklist; sanity check", etc. VERDICT: MET (1)
- **C**: CLAIM: Each risk has mitigation column. EVIDENCE: R1: "Whitelist mechanism", R6: "Pre-activation checklist + zero-findings sanity", etc. VERDICT: MET (1)

#### Criterion 23: Failure modes addressed

- **A**: CLAIM: AST parse failures addressed. EVIDENCE: Section 9.1 rejects LLM approach with rationale. Section 10 covers FP governance. No explicit failure mode analysis. VERDICT: NOT MET (0)
- **B**: CLAIM: Graceful degradation for AST failures. EVIDENCE: Section 5.3 shows SyntaxError handling returning empty FileAnalysis. R2: "Graceful degradation: log, skip". VERDICT: MET (1)
- **C**: CLAIM: Parse error handling. EVIDENCE: R2: "Graceful degradation: warn, skip file". Test case 4 validates parse error handling. VERDICT: MET (1)

#### Criterion 24: External dependency risks

- **A**: CLAIM: Cleanup-audit coupling risk noted. EVIDENCE: Section 5.4 authority rule addresses this. No formal external dependency risk list. VERDICT: NOT MET (0)
- **B**: CLAIM: resolve_gate_mode() risk (R8), agent extension regression (R7). EVIDENCE: Formal risk entries with mitigations. VERDICT: MET (1)
- **C**: CLAIM: Registry pattern misses (R5), import alias FPR (R7). EVIDENCE: Formal entries. VERDICT: MET (1)

#### Criterion 25: Monitoring/observability plan

- **A**: CLAIM: Shadow mode collects baseline data. EVIDENCE: Section 8.1 describes shadow findings visibility. No metrics or monitoring plan. VERDICT: NOT MET (0)
- **B**: CLAIM: Phase criteria with FPR/TPR/p95 metrics. EVIDENCE: Section 7 Phase 2/3 criteria tables with specific thresholds. VERDICT: MET (1)
- **C**: CLAIM: Decision criteria table with metrics. EVIDENCE: Section 9 table: FPR < 15%, TPR > 50%, p95 < 5s, whitelist stability. VERDICT: MET (1)

| Criterion | A | B | C |
|-----------|---|---|---|
| 21. 3+ risks | 0 | 1 | 1 |
| 22. Mitigations | 0 | 1 | 1 |
| 23. Failure modes | 0 | 1 | 1 |
| 24. External deps | 0 | 1 | 1 |
| 25. Monitoring | 0 | 1 | 1 |
| **Subtotal** | **0/5** | **5/5** | **5/5** |

### 2.6 Invariant and Edge Case Coverage (5 criteria)

#### Criterion 26: Collection boundaries (empty sets, single element, overflow)

- **A**: CLAIM: No explicit boundary handling. EVIDENCE: Does not discuss zero-file analysis, zero-finding reports, or maximum file count. VERDICT: NOT MET (0)
- **B**: CLAIM: Pre-activation zero-findings sanity check. EVIDENCE: Section 7 Phase 1 checklist: ">50 files must produce >0 findings". `files_analyzed >= 0` in gate contract. VERDICT: MET (1)
- **C**: CLAIM: Zero-findings sanity check. EVIDENCE: Section 9 Phase 1: "zero-findings-on-first-run WARN". VERDICT: MET (1)

#### Criterion 27: State interactions (concurrent access, ordering)

- **A**: CLAIM: Resume behavior discussed. EVIDENCE: Section 9.3 covers deterministic resume. Does not discuss concurrent wiring analysis or ordering with other post-merge steps. VERDICT: NOT MET (0)
- **B**: CLAIM: Step ordering explicit, TrailingGateRunner async handling. EVIDENCE: Section 5.6 shows sequential step ordering, shadow mode uses TrailingGateRunner for async non-blocking. VERDICT: MET (1)
- **C**: CLAIM: Step ordering defined. EVIDENCE: Section 4.4.1 shows post-spec-fidelity insertion, GateMode.TRAILING for non-blocking. VERDICT: MET (1)

#### Criterion 28: Guard gaps (whitelist validation, config errors)

- **A**: CLAIM: Suppression policy requires reason strings. EVIDENCE: Section 10.2 requires target, reason, optional expiry. Does not validate whitelist format. VERDICT: NOT MET (0)
- **B**: CLAIM: Whitelist validation with error handling by phase. EVIDENCE: Section 5.2.1: "entries missing symbol or reason are MALFORMED. In Phase 1, malformed entries are logged as WARNING and skipped. In Phase 2+, malformed entries raise WiringConfigError." VERDICT: MET (1)
- **C**: CLAIM: Whitelist with required reason. EVIDENCE: Section 5.1: schema shown but no validation behavior specified for malformed entries. VERDICT: NOT MET (0)

#### Criterion 29: Count divergence (category sum vs severity sum vs total)

- **A**: CLAIM: Both finding_counts_consistent and severity_summary_consistent checks. EVIDENCE: Section 5.2 defines both semantic checks. However, nested severity_summary block creates extraction risk (INV-014). VERDICT: NOT MET (0) -- the mechanism is undermined by the nested YAML issue.
- **B**: CLAIM: Three-way invariant enforced. EVIDENCE: Section 5.5 shows both semantic checks. INV-008 resolution: single-source computation from typed finding lists. Flat frontmatter avoids extraction issues. VERDICT: MET (1)
- **C**: CLAIM: _total_findings_consistent check only. EVIDENCE: Section 8 has total_findings_consistent but no severity-level consistency check. Only validates category sum. VERDICT: NOT MET (0)

#### Criterion 30: Interaction effects (gate mode + rollout mode + grace_period)

- **A**: CLAIM: Notes resolve_gate_mode() constraint. EVIDENCE: Section 4.3 mentions it but does not show resolution path. VERDICT: NOT MET (0)
- **B**: CLAIM: R8 risk entry + mode-aware semantic check design. EVIDENCE: Section 5.5: blocking_findings computed per mode ensures gate passes even if BLOCKING is forced. R8 explicitly lists resolve_gate_mode() risk with mitigation "Explicit gate_mode on Step". VERDICT: MET (1)
- **C**: CLAIM: Sets GateMode.TRAILING. EVIDENCE: Does not discuss interaction with resolve_gate_mode() or grace_period. Per INV-006 analysis, C's design breaks under grace_period=0. VERDICT: NOT MET (0)

| Criterion | A | B | C |
|-----------|---|---|---|
| 26. Collection boundaries | 0 | 1 | 1 |
| 27. State interactions | 0 | 1 | 1 |
| 28. Guard gaps | 0 | 1 | 0 |
| 29. Count divergence | 0 | 1 | 0 |
| 30. Interaction effects | 0 | 1 | 0 |
| **Subtotal** | **0/5** | **5/5** | **2/5** |

### 2.7 Qualitative Summary

| Dimension | A | B | C |
|-----------|---|---|---|
| Completeness | 4/5 | 5/5 | 4/5 |
| Correctness | 4/5 | 5/5 | 2/5 |
| Structure | 2/5 | 5/5 | 4/5 |
| Clarity | 4/5 | 5/5 | 5/5 |
| Risk Coverage | 0/5 | 5/5 | 5/5 |
| Invariant/Edge | 0/5 | 5/5 | 2/5 |
| **Total** | **14/30** | **30/30** | **22/30** |
| **Normalized** | **0.467** | **1.000** | **0.733** |

---

## 3. Combined Score

```
variant_score = 0.50 * quantitative + 0.50 * qualitative
```

| Component | Weight | A | B | C |
|-----------|--------|---|---|---|
| Quantitative | 0.50 | 0.784 | 0.907 | 0.861 |
| Qualitative | 0.50 | 0.467 | 1.000 | 0.733 |
| **Combined** | **1.00** | **0.626** | **0.954** | **0.797** |

---

## 4. Base Selection

**Selected base: Variant B (spec2.md)**

**Score: 0.954**

Variant B achieves the highest combined score by a significant margin. It scores perfectly on all qualitative dimensions and leads quantitative metrics as well. The key differentiators:

1. **Only variant that survives the INV-006 stress test**: Mode-aware semantic checks with `blocking_findings` computation ensure shadow mode works even when `grace_period=0` forces BLOCKING. This is a correctness requirement, not a preference.

2. **Most complete coverage**: Sprint integration, ToolOrchestrator plugin, and all three operation modes (roadmap, sprint, cleanup-audit) are specified with implementation-level detail.

3. **Strongest invariant coverage**: Three-way count invariant, whitelist validation with phase-dependent behavior, zero-findings sanity check, and gate mode interaction effects are all addressed.

4. **Best structured for implementation**: Tasklist index with LOC estimates, dependencies, and critical path. File manifest with per-file LOC ranges. Interface contracts section with explicit dependency direction.

Variant C (0.797) has valuable contributions (deviation reconciliation, coordination notes, FPR calibration formula) that should be incorporated. Variant A (0.626) provides strong architectural rationale that should be preserved, but its lack of risk assessment, testing strategy, and edge case coverage makes it unsuitable as a base.
