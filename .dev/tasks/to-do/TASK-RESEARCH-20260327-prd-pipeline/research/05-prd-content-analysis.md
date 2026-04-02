# PRD Content Analysis: Pipeline Value Mapping

**Date:** 2026-03-27
**Investigator:** Architecture Analyst
**Status:** Complete
**Source Files:**
- `src/superclaude/skills/prd/SKILL.md` (PRD section definitions, lines 996-1085)
- `src/superclaude/skills/tdd/SKILL.md` (PRD extraction agent, lines 944-978)
- `src/superclaude/examples/tdd_template.md` (TDD template, 28 sections)
- `src/superclaude/cli/roadmap/executor.py` (pipeline step definitions, lines 882-999)
- `src/superclaude/cli/roadmap/prompts.py` (prompt builders)
- `src/superclaude/cli/tasklist/prompts.py` (tasklist fidelity prompt)

---

## Section 1: Full PRD Section Inventory

[DOC-SOURCED: `src/superclaude/skills/prd/SKILL.md` lines 996-1085, verified 2026-03-27]

The PRD template defines 28 numbered sections plus appendices and a document approval block. The table below enumerates each section with its content type and the kind of information it carries.

| # | PRD Section | Content Summary | Content Type |
|---|-------------|-----------------|--------------|
| S1 | Executive Summary | 2-3 paragraph overview + key success metrics | Strategic context |
| S2 | Problem Statement | Core problem, why existing solutions fail, market opportunity | Business rationale |
| S3 | Background & Strategic Fit | Why now, company objective alignment, strategic bets | Business rationale |
| S4 | Product Vision | One-sentence vision statement with expansion | Strategic context |
| S5 | Business Context | Market opportunity (TAM/SAM/SOM), business objectives, KPIs | Business metrics |
| S6 | Jobs To Be Done (JTBD) | Primary jobs in When/I want/So that format, related jobs table | User needs |
| S7 | User Personas | Primary/secondary/tertiary persona tables; anti-personas | User needs |
| S8 | Value Proposition Canvas | Customer profile, value map (pain relievers + gain creators), fit assessment | Business rationale |
| S9 | Competitive Analysis | Landscape table, feature comparison matrix, positioning, response plan | Market intelligence |
| S10 | Assumptions & Constraints | Technical, business, user assumptions with risk-if-wrong; constraints table | Risk/scope |
| S11 | Dependencies | External, internal, cross-team dependency tables | Technical/org |
| S12 | Scope Definition | In scope, out of scope, permanently out of scope | Scope boundaries |
| S13 | Open Questions | Question tracking table with owner, status, resolution | Process |
| S14 | Technical Requirements | Architecture, performance, security, scalability, data & analytics | Technical spec |
| S15 | Technology Stack | Backend, frontend, infrastructure technology tables | Technical spec |
| S16 | User Experience Requirements | Onboarding metrics, core user flows, accessibility, localization | UX/user needs |
| S17 | Legal & Compliance Requirements | Regulatory compliance, data privacy, terms & policies | Compliance |
| S18 | Business Requirements | Monetization, pricing tiers, go-to-market, support requirements | Business spec |
| S19 | Success Metrics & Measurement | Product, business, technical metrics with targets and measurement frequency | Measurable KPIs |
| S20 | Risk Analysis | Technical, business, operational risk matrices with mitigations | Risk |
| S21 | Implementation Plan | Epics/features/stories, user stories with AC, RICE matrix, phasing, release criteria, timeline | Implementation spec |
| S22 | Customer Journey Map | Journey stages table, moments of truth | User needs |
| S23 | Error Handling & Edge Cases | Error categories, edge case scenarios, graceful degradation | Technical spec |
| S24 | User Interaction & Design | Wireframes/mockups table, design system checklist, prototype links | UX/design |
| S25 | API Contract Examples | Key endpoint request/response examples | Technical spec |
| S26 | Contributors & Collaboration | Contributor table, how to contribute guidelines | Process |
| S27 | Related Resources | Customer research, technical docs, design assets, business documents | Reference |
| S28 | Maintenance & Ownership | Document ownership, review cadence, update process | Process |
| App | Appendices | Glossary, acronyms, architecture diagrams, user research data, financial projections | Reference |

**Total: 28 sections + appendices + document approval block.**

Note: For Feature/Component PRDs (vs. Product PRDs), sections S5, S8, S9, S17, S18 are typically N/A or abbreviated, as those are platform-level concerns. [DOC-SOURCED: `prd/SKILL.md` line 192]

---

## Section 2: TDD Extraction Mapping -- What Survives vs. What Is Lost

[DOC-SOURCED: `src/superclaude/skills/tdd/SKILL.md` lines 944-978, verified 2026-03-27]

### 2.1 Extracted Sections (5 of 28)

The TDD PRD Extraction Agent (lines 944-978) extracts exactly 5 sections from the PRD:

| Extraction Section | Source PRD Section(s) | Content Extracted |
|---|---|---|
| 1. Epics | S21 (Implementation Plan -- 21.1) | Epic ID, title, description -- one row per epic |
| 2. User Stories & AC | S21 (Implementation Plan -- 21.1) | User stories with bulleted acceptance criteria, grouped by epic |
| 3. Success Metrics | S19 (Success Metrics & Measurement) | Metric, baseline, target, measurement method |
| 4. Technical Requirements | S14 (Technical Requirements) | Flat list with type labels (functional, non-functional, constraint) |
| 5. Scope Boundaries | S12 (Scope Definition) | In scope / out of scope bulleted lists |

Each extracted item is tagged as `[PRD-VERIFIED]` or `[PRD-INFERRED]`.

### 2.2 Lost Sections (23 of 28)

The following sections are NOT extracted by the TDD PRD extraction agent:

| # | PRD Section | Content Lost | Loss Impact |
|---|-------------|--------------|-------------|
| S1 | Executive Summary | Strategic overview, key success metrics summary | Context for prioritization |
| S2 | Problem Statement | Core problem, why existing solutions fail | Rationale for existence |
| S3 | Background & Strategic Fit | Why now, company alignment, strategic bets | Prioritization context |
| S4 | Product Vision | Vision statement | North star for design decisions |
| S5 | Business Context | TAM/SAM/SOM, business objectives, KPIs | Business value quantification |
| S6 | Jobs To Be Done | Primary jobs in When/I want/So that format | User motivation context |
| S7 | User Personas | Persona tables, anti-personas | Who the system serves |
| S8 | Value Proposition Canvas | Pain relievers, gain creators, fit assessment | Value alignment |
| S9 | Competitive Analysis | Feature comparison, positioning, response plan | Differentiation context |
| S10 | Assumptions & Constraints | Assumptions with risk-if-wrong, constraints | Guard rails for implementation |
| S11 | Dependencies | External, internal, cross-team dependency tables | Dependency awareness |
| S13 | Open Questions | Unresolved questions with owners | Risk awareness |
| S15 | Technology Stack | Backend, frontend, infrastructure tables | Tech constraint context |
| S16 | UX Requirements | Onboarding, user flows, accessibility, localization | UX test criteria |
| S17 | Legal & Compliance | Regulatory, data privacy, terms & policies | Compliance test criteria |
| S18 | Business Requirements | Monetization, pricing, GTM, support | Business constraint context |
| S20 | Risk Analysis | Risk matrices with mitigations | Risk-aware planning |
| S22 | Customer Journey Map | Journey stages, moments of truth | End-to-end test scenarios |
| S23 | Error Handling & Edge Cases | Error categories, edge cases, degradation plan | Test coverage gaps |
| S24 | User Interaction & Design | Wireframes, design system, prototypes | UI validation criteria |
| S25 | API Contract Examples | Endpoint request/response examples | Contract test data |
| S26 | Contributors & Collaboration | Contributor info, guidelines | (Low pipeline value) |
| S27 | Related Resources | Links to research, docs, assets | (Low pipeline value) |
| S28 | Maintenance & Ownership | Ownership, review cadence | (Low pipeline value) |
| App | Appendices | Glossary, diagrams, research data, financials | Reference enrichment |

### 2.3 Extraction Ratio

- **Extracted:** 5 sections (S12, S14, S19, S21 -- note S21 feeds both epics and user stories)
- **Lost:** 23 sections + appendices
- **Coverage:** ~18% of PRD content reaches the TDD, which then feeds the pipeline
- **Critical loss areas:** Business rationale (S1-S5, S8-S9), user context (S6-S7, S16, S22), compliance (S17), risk (S10, S20), edge cases (S23), API contracts (S25)

---

## Section 3: PRD-to-Pipeline Touchpoint Mapping

### 3.1 Pipeline Steps Reference

[DOC-SOURCED: `src/superclaude/cli/roadmap/executor.py` lines 882-999, verified 2026-03-27]

The roadmap pipeline has these steps in order (note: File 01 describes 9 core steps from `_build_steps()` at lines 843-1009; the full pipeline also includes anti-instinct as a non-LLM step and certify as a post-pipeline step, for 11 total entries):

1. **extract** -- Parse spec into structured extraction (FRs, NFRs, dependencies, success criteria, domains)
2. **generate-A / generate-B** -- Two parallel agents produce roadmaps from extraction
3. **diff** -- Compare the two roadmaps for divergences
4. **debate** -- Adversarial debate on divergence points
5. **score** -- Score debate arguments by rubric
6. **merge** -- Produce merged roadmap from scored debate
7. **anti-instinct** -- Deterministic audit (non-LLM)
8. **test-strategy** -- Generate test strategy from merged roadmap + extraction
9. **spec-fidelity** -- Verify merged roadmap covers all spec requirements
10. **wiring-verification** -- Verify integration wiring completeness
11. **certify** -- Final certification [CODE-VERIFIED: `build_certify_step` at executor.py:803, step id "certify" at line 833]

The tasklist pipeline adds:
12. **tasklist-fidelity** -- Verify tasklist covers all roadmap items

### 3.2 PRD Section to Pipeline Touchpoint Matrix

| PRD Section | Pipeline Touchpoint | Value Added | Priority |
|---|---|---|---|
| **S1: Executive Summary** | extract, generate | Provides strategic framing for requirement prioritization; helps agents understand the "big picture" when generating milestones | MEDIUM |
| **S2: Problem Statement** | extract, spec-fidelity | Anchors requirement extraction to the core problem; spec-fidelity can verify the roadmap addresses root problems, not just symptoms | HIGH |
| **S3: Background & Strategic Fit** | generate | Informs phasing decisions -- "why now" context helps agents sequence milestones by strategic urgency | LOW |
| **S4: Product Vision** | generate, debate | Vision statement resolves tie-breaking in debate when two approaches are equally valid technically | LOW |
| **S5: Business Context** | generate, score | TAM/SAM/SOM and business KPIs inform prioritization -- features targeting larger market segments rank higher | MEDIUM |
| **S6: JTBD** | extract, generate, spec-fidelity | JTBD maps directly to functional requirements the pipeline should extract; spec-fidelity can verify every job has roadmap coverage | HIGH |
| **S7: User Personas** | generate, test-strategy, spec-fidelity | Personas inform milestone ordering (primary persona features first); test-strategy uses personas to define test user profiles and scenarios | HIGH |
| **S8: Value Proposition Canvas** | generate, debate | Pain relievers and gain creators help agents prioritize features by user value delivered; enriches debate scoring | MEDIUM |
| **S9: Competitive Analysis** | generate | Feature comparison matrix highlights competitive must-haves (P0) vs. differentiators (P1); informs phasing | LOW |
| **S10: Assumptions & Constraints** | extract, generate, spec-fidelity | Constraints are requirements the extraction should capture; assumptions with risk-if-wrong become guard rails for the roadmap; spec-fidelity verifies constraints are met | HIGH |
| **S11: Dependencies** | extract | Dependency tables feed directly into the extraction pipeline's Step 5 (dependency extraction); currently only captured if in the TDD | HIGH |
| **S12: Scope Definition** | extract, spec-fidelity | **ALREADY EXTRACTED.** In-scope/out-of-scope boundaries prevent scope creep in roadmap and provide spec-fidelity negative test | -- |
| **S13: Open Questions** | generate, debate | Unresolved questions should surface as explicit risk items in the roadmap; debate can address them | MEDIUM |
| **S14: Technical Requirements** | extract | **ALREADY EXTRACTED.** FRs and NFRs feed directly into the extraction pipeline | -- |
| **S15: Technology Stack** | generate | Tech stack constraints inform milestone ordering (infra before features) and agent persona selection | LOW |
| **S16: UX Requirements** | test-strategy, spec-fidelity | Onboarding metrics, accessibility requirements, and user flows define testable acceptance criteria the test strategy should reference | HIGH |
| **S17: Legal & Compliance** | extract, test-strategy, spec-fidelity | Compliance requirements are non-functional requirements the extraction should capture; test-strategy needs compliance test scenarios; spec-fidelity verifies compliance coverage | HIGH |
| **S18: Business Requirements** | generate | Monetization and pricing constraints affect milestone scope and phasing | LOW |
| **S19: Success Metrics** | extract, test-strategy, spec-fidelity | **ALREADY EXTRACTED.** Metrics define measurable validation criteria for test-strategy and spec-fidelity | -- |
| **S20: Risk Analysis** | generate, debate, score | Risk matrices inform milestone ordering (mitigate high risks early); debate scoring weighs risk-aware arguments higher; enriches the score rubric | HIGH |
| **S21: Implementation Plan** | extract | **ALREADY EXTRACTED.** Epics, user stories, AC, phasing, and timeline feed the extraction pipeline directly | -- |
| **S22: Customer Journey Map** | test-strategy | Journey stages define end-to-end test scenarios; moments of truth identify critical test points | HIGH |
| **S23: Error Handling & Edge Cases** | test-strategy, spec-fidelity | Error categories and edge case scenarios are direct test-strategy input; spec-fidelity verifies error handling coverage in the roadmap | HIGH |
| **S24: User Interaction & Design** | test-strategy | Wireframes and design system checklists define UI validation criteria for the test strategy | MEDIUM |
| **S25: API Contract Examples** | test-strategy, spec-fidelity | Request/response examples are direct contract test inputs; spec-fidelity can verify API coverage | HIGH |
| **S26: Contributors & Collaboration** | (none) | Process metadata, no pipeline value | NONE |
| **S27: Related Resources** | (none) | Reference links, no direct pipeline value | NONE |
| **S28: Maintenance & Ownership** | (none) | Process metadata, no pipeline value | NONE |
| **App: Appendices** | extract, test-strategy | Glossary standardizes terminology for extraction; architecture diagrams inform generate; research data enriches test strategy | LOW |

### 3.3 Pipeline Touchpoint Summary (by pipeline step)

| Pipeline Step | PRD Sections That Add Value | Enrichment Category |
|---|---|---|
| **extract** | S2, S6, S10, S11, S17 (+ already: S12, S14, S19, S21) | Broader requirement capture -- JTBD, constraints, compliance, dependencies |
| **generate** | S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S13, S15, S18, S20 | Prioritization, phasing, strategic context |
| **diff** | (indirect -- benefits from richer generate output) | N/A |
| **debate** | S4, S8, S13, S20 | Tie-breaking context, risk-aware argumentation |
| **score** | S5, S20 | Business value weighting, risk severity weighting |
| **merge** | (indirect -- benefits from richer debate/score) | N/A |
| **test-strategy** | S7, S16, S17, S22, S23, S24, S25 | Personas, UX criteria, compliance, journeys, edge cases, API contracts |
| **spec-fidelity** | S2, S6, S7, S10, S12, S16, S17, S23, S25 | Problem coverage, JTBD coverage, constraint verification, compliance, edge cases |
| **tasklist-fidelity** | S10, S11, S17 | Constraint and dependency verification in tasklist items |

---

## Section 4: Minimal PRD Section Set Recommendation

### 4.1 Tiered Recommendation

The 23 lost PRD sections can be grouped into three tiers of pipeline enrichment value:

**Tier 1 -- High Value (should always be extracted when PRD exists):**

| PRD Section | Primary Pipeline Consumers | Rationale |
|---|---|---|
| S6: JTBD | extract, generate, spec-fidelity | Maps directly to functional requirements; verifiable coverage |
| S7: User Personas | generate, test-strategy, spec-fidelity | Defines test profiles and prioritization order |
| S10: Assumptions & Constraints | extract, generate, spec-fidelity | Constraints are implicit requirements; assumptions are risk items |
| S11: Dependencies | extract | Direct feed to dependency extraction step |
| S17: Legal & Compliance | extract, test-strategy, spec-fidelity | NFRs the pipeline currently misses entirely |
| S20: Risk Analysis | generate, debate, score | Risk matrices inform milestone ordering and debate quality |
| S22: Customer Journey Map | test-strategy | Defines E2E test scenarios from user perspective |
| S23: Error Handling & Edge Cases | test-strategy, spec-fidelity | Direct test coverage input |
| S25: API Contract Examples | test-strategy, spec-fidelity | Contract test data |

**Tier 2 -- Medium Value (extract for standard/heavyweight specs):**

| PRD Section | Primary Pipeline Consumers | Rationale |
|---|---|---|
| S2: Problem Statement | extract, spec-fidelity | Root problem anchors requirement validity |
| S5: Business Context | generate, score | Business KPIs inform prioritization |
| S8: Value Proposition Canvas | generate, debate | Pain/gain mapping enriches debate scoring |
| S13: Open Questions | generate, debate | Surfaces unresolved risks |
| S16: UX Requirements | test-strategy, spec-fidelity | Accessibility and onboarding test criteria |
| S24: User Interaction & Design | test-strategy | UI validation criteria |

**Tier 3 -- Low Value (optional, contextual enrichment):**

| PRD Section | Primary Pipeline Consumers | Rationale |
|---|---|---|
| S1: Executive Summary | extract, generate | General framing (often redundant with S2+S4) |
| S3: Background & Strategic Fit | generate | "Why now" context -- useful but not structurally impactful |
| S4: Product Vision | generate, debate | Tie-breaking only |
| S9: Competitive Analysis | generate | Competitive must-haves (often reflected in S14 already) |
| S15: Technology Stack | generate | Tech constraints (often in S14) |
| S18: Business Requirements | generate | Monetization/pricing constraints |

**No Pipeline Value (skip):**

S26 (Contributors), S27 (Related Resources), S28 (Maintenance & Ownership)

### 4.2 Minimal Viable Set

For maximum enrichment with minimum extraction cost, the pipeline should reference **9 additional PRD sections** (Tier 1) beyond the current 5. This raises extraction coverage from ~18% to ~50% of PRD content.

**Recommended extraction expansion:**
- Current 5: S12, S14, S19, S21 (epics + stories)
- Add 9 Tier 1: S6, S7, S10, S11, S17, S20, S22, S23, S25
- **Total: 14 sections extracted** (from 28)

### 4.3 Supplementary Prompt Block Organization

PRD content should NOT be dumped wholesale into prompts. Instead, organize as labeled supplementary blocks injected only into the pipeline steps that need them:

```
<!-- PRD-SUPPLEMENT: extract -->
## PRD Context: Requirements Enrichment
### Jobs To Be Done (from PRD S6)
[JTBD content]
### Assumptions & Constraints (from PRD S10)
[constraints content]
### Dependencies (from PRD S11)
[dependency tables]
### Compliance Requirements (from PRD S17)
[compliance content]

<!-- PRD-SUPPLEMENT: generate -->
## PRD Context: Prioritization & Phasing
### Business Context (from PRD S5)
[KPIs, objectives]
### User Personas (from PRD S7)
[persona summaries -- primary persona first]
### Risk Analysis (from PRD S20)
[risk matrix summary]

<!-- PRD-SUPPLEMENT: test-strategy -->
## PRD Context: Test Enrichment
### User Personas (from PRD S7)
[test user profiles]
### Customer Journey Map (from PRD S22)
[journey stages for E2E scenarios]
### Error Handling & Edge Cases (from PRD S23)
[error categories and edge case scenarios]
### API Contract Examples (from PRD S25)
[request/response examples for contract tests]
### Compliance Requirements (from PRD S17)
[compliance test scenarios]

<!-- PRD-SUPPLEMENT: spec-fidelity -->
## PRD Context: Fidelity Verification
### Problem Statement (from PRD S2)
[root problem -- verify roadmap addresses it]
### Jobs To Be Done (from PRD S6)
[JTBD -- verify each job has roadmap coverage]
### Assumptions & Constraints (from PRD S10)
[constraints -- verify roadmap respects them]
### Compliance Requirements (from PRD S17)
[compliance -- verify roadmap covers them]
```

**Key design decisions for prompt blocks:**
1. Each block is labeled with its source PRD section number for traceability
2. Content is summarized/condensed, not copied verbatim (token efficiency)
3. Blocks are injected only into steps that need them (no blanket injection)
4. The `extract` step gets the most structural content (requirements, dependencies, constraints)
5. The `generate` step gets the most strategic content (personas, risks, business context)
6. The `test-strategy` step gets the most scenario content (journeys, edge cases, contracts)
7. The `spec-fidelity` step gets verification anchors (problem, JTBD, constraints, compliance)

### 4.4 What Enriches Each Pipeline Step (Detailed)

**Extract enrichment (S6, S10, S11, S17):**
- S6 JTBD: Each "When... I want... So that..." statement is a candidate functional requirement the extraction should capture. Currently the extraction only finds requirements explicitly stated in the TDD, missing implicit requirements from JTBD.
- S10 Constraints: "Risk-if-wrong" assumptions and hard constraints (budget, timeline, regulatory) are non-functional requirements the extraction currently misses.
- S11 Dependencies: External and cross-team dependency tables feed directly into extraction Step 5 (dependency extraction). Without these, the pipeline can only infer dependencies from the TDD text.
- S17 Compliance: Regulatory and data privacy requirements are NFRs that should be extracted alongside performance and security requirements.

**Generate enrichment (S5, S7, S20):**
- S5 Business KPIs: When two features compete for the same milestone, business KPIs (revenue impact, user adoption targets) provide an objective prioritization signal.
- S7 Personas: Primary persona features should appear in earlier milestones. Anti-personas help agents avoid scope creep by identifying who the product is NOT for.
- S20 Risk matrices: High-risk items should be addressed in early milestones (de-risk early). The risk severity directly maps to milestone ordering.

**Spec-fidelity enrichment (S2, S6, S10, S17):**
- S2 Problem Statement: Spec-fidelity currently checks "does the roadmap cover all spec requirements?" but cannot check "does the roadmap solve the actual problem?" Without S2, the pipeline can produce a roadmap that covers all technical requirements but misses the business intent.
- S6 JTBD: Each job should have at least one roadmap milestone that addresses it. This is a coverage check the pipeline currently cannot perform.
- S10 Constraints: Spec-fidelity should verify that no milestone violates stated constraints (e.g., a constraint says "must work offline" but no milestone addresses offline capability).
- S17 Compliance: Spec-fidelity should verify compliance requirements have roadmap coverage.

**Test-strategy enrichment (S7, S22, S23, S25):**
- S7 Personas: Define test user profiles -- the test strategy should include scenarios for each persona type.
- S22 Customer Journey: Journey stages map directly to end-to-end test scenarios. "Moments of truth" are critical test assertions.
- S23 Edge Cases: Error categories and edge case scenarios are direct test case inputs the pipeline currently has no access to.
- S25 API Contracts: Request/response examples are contract test data. Without these, the test strategy can only describe API testing abstractly.

---

## Gaps and Questions

1. **PRD file path passing mechanism:** The pipeline currently accepts a single `--spec` file (the TDD). How should the PRD path be provided? Options: (a) `--prd <path>` flag, (b) `parent_doc` frontmatter field in the TDD, (c) auto-discovery from `.dev/tasks/` folder structure. The TDD template already has a `parent_doc` frontmatter field [DOC-SOURCED: `tdd_template.md` line 14] -- this is the natural place.

2. **Extraction timing:** Should PRD supplementary content be extracted once (at the `extract` step) and cached, or re-read at each pipeline step? Single extraction is more efficient; per-step extraction allows step-specific summarization.

3. **Token budget impact:** Adding 9 more PRD sections to the pipeline increases prompt sizes. Each supplementary block should be capped (e.g., 500 tokens for extract, 300 for generate, 400 for test-strategy, 300 for spec-fidelity). Total additional cost: ~1,500 tokens across the pipeline.

4. **Feature PRD vs. Product PRD:** For Feature PRDs, sections S5, S8, S9, S17, S18 are typically N/A. The pipeline should handle absent sections gracefully (skip the corresponding supplement block rather than injecting empty content).

5. **PRD staleness:** The PRD may be out of date relative to the TDD. Should the pipeline include a lightweight PRD-TDD consistency check, or trust both documents as-is?

6. **Tasklist pipeline integration:** The tasklist-fidelity step currently checks roadmap-to-tasklist coverage only. Adding PRD constraint verification (S10, S11, S17) to tasklist-fidelity would catch constraint violations that survive through roadmap generation.

---

## Stale Documentation Found

No stale documentation detected. All source file line references were verified against current file contents on 2026-03-27. The PRD SKILL.md section inventory (lines 996-1085) matches the described 28-section structure. The TDD extraction agent (lines 944-978) confirms the 5-section extraction scope.

One potential staleness risk: the TDD template `parent_doc` field (line 14) says "[link to Product PRD that this TDD implements]" -- this is a placeholder instruction, not a live link. If a real TDD has this field populated with an actual path, the pipeline could use it for PRD discovery.

---

## Summary

The TDD PRD extraction agent extracts 5 of 28 PRD sections (~18% coverage), capturing epics, user stories, success metrics, technical requirements, and scope boundaries. The remaining 23 sections contain business rationale, user context, compliance requirements, risk analysis, customer journeys, edge cases, and API contracts that the pipeline currently cannot access.

**Key finding:** 9 additional PRD sections (Tier 1) would raise extraction coverage to ~50% and provide high-value enrichment to 4 pipeline steps: extract (broader requirement capture), generate (prioritization context), test-strategy (scenario enrichment), and spec-fidelity (coverage verification). The highest-impact additions are S6 (JTBD), S7 (Personas), S10 (Constraints), S17 (Compliance), S22 (Customer Journey), and S23 (Edge Cases).

**Recommended implementation:** Use the TDD `parent_doc` frontmatter field for PRD discovery, extract supplementary content once at pipeline start, organize into step-specific labeled prompt blocks, and cap each block at 300-500 tokens for budget control.

**Status:** Complete
