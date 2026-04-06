# TDD Comparison Review: Task Management System

**Date:** 2026-04-04
**Version A:** Refactored TDD skill (PR feat/v3.65-prd-tdd-Refactor) -- 3,781 lines
**Version B:** Original TDD skill (baseline) -- 2,777 lines
**Source PRD:** PRD_TASK_MANAGEMENT_SYSTEM.md
**Version A Template:** `src/superclaude/examples/tdd_template.md` (new, from PR)
**Version B Template:** `.claude/templates/documents/tdd_template.md` (old, baseline)

---

## Executive Summary

This review compares two TDD outputs produced by different versions of the TDD skill from the same source PRD. Both documents describe the same system -- a PostgreSQL-backed task management layer for AI agents -- and follow nearly identical templates (96% shared content; the diff is 12 frontmatter fields and 13 lines of pipeline guidance).

**Version B is the stronger TDD.** While Version A is more exhaustive (3,781 lines), much of its additional content is at the wrong abstraction level for a Technical Design Document: business KPIs from the PRD (S4.2), enumerated test cases belonging in a test plan (S15), per-phase exit checklists belonging in a sprint plan (S23/S24), and capacity projections belonging in a scaling document (S4.3). Version B is more disciplined (2,777 lines, 89 FRs, 46 NFRs, 5 alternatives, 69 provenance tags, JSON API examples, template-compliant structure with Appendices and Contract Table) and stays more consistently at the design level.

**Template adherence is a primary differentiator.** Version A has 3 template violations (missing Contract Table, missing Appendices, 2 ad-hoc subsections S5.3/S5.4). Version B has 1 minor violation (ad-hoc Document Provenance section) with all required structural elements present. Template compliance is not optional -- it ensures downstream consumers (roadmap generation, task planning, review panels) can reliably parse the document.

Both versions violate their template's own line budget. The templates specify 1,200-1,800 lines for Heavyweight TDDs and flag documents over 2,000 lines as "a code smell" (Template A line 1290; Template B line 1265). Version A exceeds the ceiling by 2.1x. Version B exceeds it by 1.5x.

**A key evaluation principle: more is not better in a TDD.** A TDD tells engineers HOW to build something at the design level. It is not the implementation, the test plan, the sprint backlog, or the PRD. Content that belongs in those other documents creates maintenance burden (it will drift) and obscures the actual technical design decisions. Where this review previously awarded Version A wins for "more metrics," "more test cases," "more open questions," or "more exit criteria," those verdicts have been corrected to evaluate whether the content is at the right abstraction level.

The two previous review attempts (the original review and the corrections document) both contained critical factual errors. This review was written from scratch against the source files without consulting either broken document. Every factual claim cites line numbers from the actual TDD files and templates.

---

## Template Adherence Analysis

### Template Differences

The two templates are 96% identical. Template A (new) adds 12 frontmatter fields (`feature_id`, `spec_type`, `complexity_score`, `complexity_class`, `target_release`, `authors`, `quality_scores` block) and 13 lines of sentinel self-check / pipeline guidance (Template A lines 60-72). All 28 numbered sections, Appendices (A-D), Contract Table, Document History, Completeness Checklist, and the line budget guidance are identical in both templates.

### Version A Against Its Template (Template A)

| Template Element | Present in A? | Adherence | Evidence |
|-----------------|:---:|-----------|----------|
| Extended Frontmatter (12 new fields) | Yes | PASS | Lines 15-26: `feature_id`, `spec_type`, `complexity_class`, etc. |
| WHAT/WHY/HOW | Yes | PASS | Lines 56-58 |
| Document Lifecycle | Yes | PASS | Lines 60-68 |
| Tiered Usage | Yes | PASS | Lines 70-78 |
| Document Information | Yes | PASS | Lines 82-96 |
| Approvers | Yes | PASS | Lines 98-105 |
| Completeness Checklist | Yes | PASS | Lines 107-136 |
| **Contract Table** | **No** | **FAIL** | Template A line 151 requires it. Version A has no "Contract Table" heading (grep verified). |
| Sections 1-28 | Yes | PASS | All 28 present (H2 heading scan verified) |
| **Section 5 subsections** | 5.1, 5.2, **5.3, 5.4** | **DEVIATION** | Template has only 5.1 and 5.2. Version A adds 5.3 "Source Traceability Matrix" (line 513) and 5.4 "Completeness Verification" (line 578) -- neither exists in either template. |
| **Appendices** | **No** | **FAIL** | Template A defines Appendices A-D. Version A has no Appendices section (grep verified). |
| Document History | Yes | PASS | Line 138 |
| Line budget (1,200-1,800) | No | **FAIL** | 3,781 lines = 2.1x the 1,800-line ceiling |

**Version A template violations:** 3 (missing Contract Table, missing Appendices, ad-hoc S5.3/5.4)

### Version B Against Its Template (Template B)

| Template Element | Present in B? | Adherence | Evidence |
|-----------------|:---:|-----------|----------|
| Standard Frontmatter | Yes | PASS | Lines 1-40 |
| WHAT/WHY/HOW | Yes | PASS | Lines 45-47 |
| Document Lifecycle | Yes | PASS | Lines 49-57 |
| Tiered Usage | Yes | PASS | Lines 59-67 |
| Document Information | Yes | PASS | Lines 71-82 |
| Approvers | Yes | PASS | Lines 84-91 |
| Completeness Checklist | Yes | PASS | Lines 95-127 |
| Contract Table | Yes | PASS | Line 129 |
| Sections 1-28 | Yes | PASS | All 28 present (H2 heading scan verified) |
| Section 5 subsections | 5.1, 5.2 only | PASS | Matches template exactly (lines 308, 401) |
| Appendices | Yes (A, B, C) | PASS | Line 2723. Missing Appendix D (Performance Test Results) but has placeholder table in Appendix C area (line 2752). |
| Document History | Yes | PASS | Line 2767 |
| **Document Provenance** | Yes | **DEVIATION** | Line 2775: ad-hoc 3-line section not in template |
| Line budget (1,200-1,800) | No | **FAIL** | 2,777 lines = 1.5x the 1,800-line ceiling |

**Version B template violations:** 1 (ad-hoc Document Provenance section), plus line budget overage

**Template adherence winner: Version B.** Version B has 1 minor ad-hoc addition and includes all required structural elements (Contract Table, Appendices). Version A is missing 2 required elements and adds 2 ad-hoc subsections.

---

## Section-by-Section Comparison

| # | Section | Version A Lines | Version B Lines | Winner | Rationale |
|---|---------|:-:|:-:|:------:|-----------|
| -- | Frontmatter | 1-52 | 1-40 | **Tie** | Each follows its own template. A has 12 additional fields because Template A requires them (lines 15-26). This is template compliance, not innovation. |
| -- | Document Information | 82-106 | 71-92 | **Tie** | Both fill out the standard table. A adds "Architecture Pattern" and "Primary Consumer" rows not in template (useful but ad-hoc). |
| -- | Completeness Status | 107-137 | 95-138 | **B** | B includes Contract Table (line 129) per template. A omits it entirely. |
| 1 | Executive Summary | 179-196 | 177-191 | **Tie** | Both provide clear 2-3 paragraph summaries with key deliverables. A is slightly more detailed on phase breakdown. |
| 2 | Problem Statement | 197-231 | 192-217 | **Tie** | Both cover background, problem statement, and business context adequately. |
| 3 | Goals & Non-Goals | 232-280 | 218-263 | **Tie** | A has 8 goals, 5 non-goals, 7 future considerations. B has 8 goals, 7 non-goals, 6 future considerations. B marks each with `[RESEARCH-VERIFIED]` tags (lines 226-259). |
| 4 | Success Metrics | 281-335 | 264-305 | **B** | A has Section 4.2 "Business Metrics with Engineering Proxies" (lines 306-321) containing PRD-level KPIs: "Feature Adoption" (% of projects using feature at 3/6 months), "Enterprise Pipeline Conversion" (CRM tag rate), "Support Ticket Reduction" (40% reduction target), "Gate Pass Rate." These are product/business metrics that belong in the PRD, not a TDD. A TDD's success metrics should be technical SLOs and engineering instrumentation. B's Section 4.2 stays at the engineering instrumentation level (Prometheus counters, dashboard panels) without importing business KPIs. B also includes 3 metrics A lacks (tool definition token budget, invalid transition rejection rate, cross-tenant data leakage) which are directly engineering-verifiable. A's Section 4.3 "Throughput and Scale Targets" includes "Tasks platform-wide: ~50,000,000" and "Audit events monthly: ~200,000,000" -- these are capacity planning projections, not design-level success criteria. B wins for staying at the correct abstraction level. |
| 5 | Technical Requirements | 336-594 (259 lines) | 306-489 (184 lines) | **B** | Both templates define Section 5 with exactly two subsections: 5.1 (Functional Requirements) and 5.2 (Non-Functional Requirements). Version A adds S5.3 "Source Traceability Matrix" (line 513) and S5.4 "Completeness Verification" (line 578) -- neither exists in either template. These are ad-hoc additions that violate template structure. While a traceability matrix has value, adding it as unauthorized subsections is a template deviation, not a win. Version B follows the template exactly (S5.1 at line 308, S5.2 at line 401) with no ad-hoc additions. B also has 89 FRs vs A's 37, providing more fine-grained requirements coverage. B wins for template compliance and requirements granularity. |
| 6 | Architecture | 595-902 (308 lines) | 490-733 (244 lines) | **B** | Both cover the same architectural patterns (Domain Facade, shared service layer, CQRS read models). B includes MCP Compatibility subsection with `result_context` disambiguation (design-appropriate forward thinking). B's 244 lines are tighter. A has 308 lines with more repetition. |
| 7 | Data Models | 903-1532 (630 lines) | 734-1235 (502 lines) | **Tie** | A uses tabular constraint documentation (design-level). B contains `__table_args__` SQLAlchemy ORM blocks at lines 778 and 829 (implementation-level code). A has 0 `__table_args__` instances (grep verified). B has more entity fields (32 vs ~26 on main entity). Both have ER diagrams. A's constraint tables are more appropriate for a TDD; B's ORM blocks cross into implementation. B's field coverage is broader. Wash. |
| 8 | API Specifications | 1533-2175 (643 lines) | 1236-1527 (292 lines) | **Split** | A lists 21 REST endpoints + 5 facade tools with parameter tables (breadth). B lists 5 REST endpoints + 5 facade tools with JSON request/response examples (depth). A's breadth is useful for sprint planning. B's JSON examples are directly testable. Neither approach is strictly better. A at 643 lines is the single largest contributor to its line count overage (35% of the delta per QA Report 2). |
| 9 | State Management | 2176-2425 (250 lines) | 1528-1641 (114 lines) | **A** | A centralizes the full 5-state machine with transition matrix (9.1), terminal state semantics (9.1.2), transition rules table (9.1.3), guard conditions, side effects, and CHECK constraint alignment in one dedicated section. B documents the same state machine but distributes some content across FRs and architecture. Centralized is better for implementers. |
| 10 | Component Inventory | 2426-2513 (88 lines) | 1642-1649 (8 lines) | **B** | B marks this "N/A -- Backend System" with a brief rationale (line 1644). The template's Section 10 is designed for frontend component hierarchies. A repurposes it as a "Backend Service Inventory" (line 2428) listing 22 file paths -- useful context, but this is implementation project structure, not component design. B's honest N/A is more template-appropriate. |
| 11 | User Flows | 2514-2627 (114 lines) | 1650-1868 (219 lines) | **B** | B has 219 lines of detailed agent workflow sequences (11.1-11.5) covering bulk create, status transitions, gate readiness checks, audit queries, and semantic search flows. A has 114 lines with less workflow detail. For a system where "users" are primarily AI agents, B's agent workflow depth is more useful. |
| 12 | Error Handling | 2628-2694 (67 lines) | 1869-1934 (66 lines) | **Tie** | Similar coverage. Both define error response formats and error code tables. |
| 13 | Security | 2695-2799 (105 lines) | 1935-1988 (54 lines) | **A** | A has more detailed RLS policy documentation, security verification checklist, and JWT claim specifications. B is adequate but less thorough. |
| 14 | Observability | 2800-2910 (111 lines) | 1989-2086 (98 lines) | **Tie** | A lists more Prometheus metrics (25 vs 14), but a TDD should specify monitoring STRATEGY and key metrics, not enumerate every counter. B's 14 metrics cover all critical operational concerns (tool call latency, query duration by zoom level, status transitions, audit events, vectorization lag, RLS overhead, concurrent modification retries) at the design level. B also uses SLO error budget burn rate alerting (Section 14.4) which is a more mature monitoring approach than A's threshold-based alerts. Both cover logging, tracing, alerts, and dashboards adequately. More metrics is not better in a TDD -- the implementation team will define the full metric set. |
| 15 | Testing Strategy | 2911-3022 (112 lines) | 2087-2207 (121 lines) | **B** | A enumerates ~45 individual test cases across 6 subsystem tables (15.2.1-15.2.6). B enumerates ~25 test cases but adds a full Load Test Specification (S15.4, lines 2157-2204) with workload profiles, agent behavior models, concurrency parameters, and 10 quantitative success criteria -- plus CI/CD gate behavior per phase (lines 2150-2155). A's approach conflates the TDD with a test plan: listing every test case belongs in the test plan derived from the TDD, not in the TDD itself. A TDD should specify testing STRATEGY (pyramid, coverage targets, environments, key scenarios), not serve as the test case catalog. B covers strategy, environments, CI/CD gates, and load testing methodology at the design level. B wins for correct abstraction level. |
| 16 | Accessibility | 3023-3028 (6 lines) | 2208-2215 (8 lines) | **Tie** | Both correctly mark N/A for backend system. |
| 17 | Performance Budgets | 3029-3101 (73 lines) | 2216-2272 (57 lines) | **Tie** | A has per-endpoint p95/p99 targets. B has consolidated performance targets covering the same operations. Both define the same core latency budgets (CRUD <200ms, dashboard <50ms, list <100ms, bulk <5s, semantic search <500ms). A's per-endpoint granularity (73 lines vs 57) is marginally more specific but the core budgets are equivalent. A TDD should specify performance budgets for key operation categories, not enumerate every endpoint -- the implementation team will instrument and tune per-endpoint during development. |
| 18 | Dependencies | 3102-3143 (42 lines) | 2273-2308 (36 lines) | **Tie** | Both list the same core dependencies. |
| 19 | Migration & Rollout | 3144-3224 (81 lines) | 2309-2357 (49 lines) | **A** | A has per-phase rollback procedures with specific steps and time estimates. B has phase-level rollback notes but less operational detail. Migration rollback is a legitimate TDD concern -- this is design-level content about how to safely deploy and revert schema changes. A wins for covering a real engineering concern more thoroughly. |
| 20 | Risks & Mitigations | 3225-3256 (32 lines) | 2358-2374 (17 lines) | **Tie** | A: 9 risks (R1-R9) with heat map summary and top-3 prioritization (line 3241). B: 10 risks (R1-R10) at line 2358. B has MORE risks (10 > 9). A has better visual formatting (heat map). Both include Probability, Impact, Mitigation, and Contingency columns. Neither is clearly better -- B has breadth, A has presentation. |
| 21 | Alternatives | 3257-3303 (47 lines) | 2375-2428 (54 lines) | **B** | A: 5 alternatives (Alternative 0 at line 3259, Option B at 3268, Option D at 3277, Fixed Agile at 3286, Offset Pagination at 3295). B: 5 alternatives (Alternative 0-4 at lines 2379-2427). B uses consistent naming (Alternative 0-4). A uses inconsistent naming (Alternative 0, then Option B, then Option D, then descriptive titles). B includes Alternative 1 (Pure Relational/Option A) which A omits entirely. Both have "Do Nothing" as Alternative 0. Both templates mark it mandatory. B's `[RESEARCH-VERIFIED]` tags on alternatives provide claim confidence. |
| 22 | Open Questions | 3306-3356 (51 lines) | 2431-2444 (14 lines) | **Tie** | A has 18 questions + 8 research gaps (26 total). B has 9 questions. More questions is not inherently better -- the question is whether BETTER questions are asked. A includes several questions that are PRD-scope, not TDD-scope: Q27 (educational pricing tier), Q28 (user research validation), Q31 (Pixel Streaming hour caps), Q32 (LLM token usage caps), Q34 (free tier design), Q38 (enterprise pricing display). These are product decisions, not technical design questions. A's 8 research gaps (I1-I8) are genuinely useful for implementation. B's 9 questions are tightly scoped to technical implementation concerns (organization model, genre-conditional modeling, gate item IDs, enum values, dynamic content markers, tool communication paths). B also resolves 2 of its 9 in-document (Q2, Q8), showing active question management. Both have strengths: A's phase organization is useful; B's tight scoping is more TDD-appropriate. |
| 23 | Timeline & Milestones | 3357-3476 (120 lines) | 2447-2520 (74 lines) | **Tie** | A has per-phase exit criteria as detailed checklists (6-7 items per phase, lines 3387-3473). B has per-phase deliverables with concise exit criteria paragraphs (lines 2466-2517). A's exit criteria are more detailed, but this level of detail -- verifiable checklists with specific items like "Alembic migration runs cleanly on fresh database and is idempotent" -- belongs in the tasklist/sprint plan derived from the TDD, not in the TDD itself. A TDD should specify timeline, phase dependencies, deliverables, and high-level exit gates. Both versions cover the same 5 phases with the same dependency structure and timeline (11-15 weeks). B covers this at the appropriate design level. A's extra 46 lines are sprint-planning content. |
| 24 | Release Criteria | 3477-3555 (79 lines) | 2521-2571 (51 lines) | **Tie** | A has per-phase Definition of Done checklists (24.1-24.5, 12-14 items each). B has a feature-level DoD (24.1) plus per-phase release criteria as concise paragraphs (24.2) plus a release checklist (24.3) plus rollback/contingency table (24.4). A's per-phase checklists largely duplicate content from S23 exit criteria (same items restated). This level of checklist granularity belongs in sprint/tasklist planning. B's structure (general DoD + phase summaries + release checklist + rollback) is more appropriate for a TDD. B's rollback/contingency table (24.4) with specific recovery times is genuinely useful design-level content that A lacks in this section. |
| 25 | Operational Readiness | 3556-3623 (68 lines) | 2572-2607 (36 lines) | **Tie** | Both cover runbooks, alerts, and on-call procedures. A has more detail but the additional content is borderline implementation. |
| 26 | Cost & Resource | 3624-3702 (79 lines) | 2608-2657 (50 lines) | **Tie** | Both provide cost estimates. A is more granular. |
| 27 | References | 3703-3753 (51 lines) | 2658-2697 (40 lines) | **Tie** | Both list relevant source documents. |
| 28 | Glossary | 3754-3781 (28 lines) | 2698-2722 (25 lines) | **Tie** | Both define key terms. |
| -- | Appendices | Absent | 2723-2765 (43 lines) | **B** | Version A omits Appendices entirely (template violation). Version B has Appendices A (API reference), B (Database schema), C (Performance test results placeholder). |
| -- | Document History | 138-143 | 2767-2773 | **Tie** | Both present. |
| -- | Document Provenance | Absent | 2775-2777 | **B** | B tracks assembly metadata. Minor ad-hoc addition but useful for traceability. |

**Section winners tally:**
- Version A: 3 (State Management, Security, Migration & Rollout)
- Version B: 10 (Completeness Status, Success Metrics, Tech Requirements, Architecture, Component Inventory, User Flows, Testing Strategy, Alternatives, Appendices, Document Provenance)
- Tie/Split: 21 (Frontmatter, Doc Info, S1 Exec Summary, S2 Problem Statement, S3 Goals, S7 Data Models, S8 API Specs [Split], S12 Error Handling, S14 Observability, S16 Accessibility, S17 Perf Budgets, S18 Dependencies, S20 Risks, S22 Open Questions, S23 Timeline, S24 Release Criteria, S25 Operational Readiness, S26 Cost, S27 References, S28 Glossary, Doc History)

---

## Scope Appropriateness

A TDD specifies WHAT to build and the technical HOW at a design level. It should not contain copy-pasteable implementation code. Both templates include this guidance: "Show key interfaces and data models" (Do) vs "Reproduce full implementations" (Don't).

### Version A Scope Issues

1. **RLS SQL DDL statements** -- Multiple `CREATE POLICY` and `ALTER TABLE` SQL blocks. The POLICY design belongs in a TDD; the exact DDL syntax is borderline.
2. **FastAPI router registration snippet** (line 2122) -- Python code showing how to register the router. Implementation detail.
3. **Named CHECK constraint SQL expressions** -- e.g., `NOT (status = 'doing' AND start_date IS NULL)`. The constraint RULE is design-level; the SQL expression is borderline.
4. **22-file service inventory** (Section 10, lines 2430-2455) -- Listing exact file paths like `backend/app/models/task_instance.py` is project structure, not component design.

### Version B Scope Issues

1. **`__table_args__` SQLAlchemy ORM blocks** (lines 778-796, 829-833) -- Copy-pasteable Python ORM code with `PrimaryKeyConstraint`, `UniqueConstraint`, `ForeignKeyConstraint`, `CheckConstraint`, and `Index` definitions. This is implementation-level code.
2. **`get_tenant_session()` Python function** (line 658) -- An actual implementation function for setting tenant context via `SET LOCAL`. The pattern design belongs in the TDD; the Python function does not.
3. **14 `SET LOCAL` references** -- Some are design-level (explaining the RLS pattern); some cross into implementation.

### Assessment

Both versions cross the design/implementation boundary. The critical distinction is:

- Version B's `__table_args__` blocks (lines 778, 829) are the most clear-cut implementation code in either document -- they are copy-pasteable ORM model configuration.
- Version A's constraint tables are the same information expressed at the right level of abstraction for a TDD (tabular constraint documentation rather than Python code).
- Version B's JSON request/response examples in Section 8 are the RIGHT kind of detail for a TDD -- they define API contracts that engineers can test against.
- Version A's 22-file path inventory in Section 10 is the WRONG kind of detail -- it locks in project structure decisions that belong in implementation.

**IMPORTANT NOTE:** Both previous reviews incorrectly attributed the `__table_args__` code to Version A. Grep verification confirms: Version A has 0 instances of `__table_args__`. Version B has 2 instances (lines 778, 829).

**Scope winner: Marginal wash.** Both cross the line in different ways. Version B's ORM blocks are more clearly implementation-level. Version A's file path inventory is more clearly project-structure-level. Neither is clean.

---

## Content Quality

| Criterion | Version A (1-5) | Version B (1-5) | Evidence |
|-----------|:-:|:-:|----------|
| Template compliance | 2 | 4 | A: missing Contract Table, missing Appendices, 2 ad-hoc subsections (S5.3/5.4) = 3 violations. B: 1 ad-hoc section (Doc Provenance), all required elements present. |
| Design-level abstraction | 2 | 3 | A: business KPIs in S4.2 (PRD leakage), file path inventory (S10), FastAPI snippet, ~45 enumerated test cases (test plan leakage), per-phase exit criteria checklists (tasklist leakage), capacity projections to 500M tasks (planning leakage). B: `__table_args__` ORM blocks (lines 778, 829), `get_tenant_session()` function (line 658). Both cross the line but A crosses it more often and in more directions (PRD, test plan, sprint plan). |
| Provenance / traceability | 3 | 5 | B: 69 provenance tags (43 `[RESEARCH-VERIFIED]` + 26 `[CODE-VERIFIED]`). A: 0 provenance tags. A has a traceability matrix (S5.3) mapping requirements to PRD sections -- structurally useful but an unauthorized template addition, and a different mechanism than claim-level provenance. |
| Completeness (sections present) | 3 | 5 | A: all 28 numbered sections, but missing Appendices and Contract Table. B: all 28 numbered sections + Appendices (A-C) + Contract Table + Document Provenance. |
| Technical depth (at correct abstraction) | 3 | 4 | A is thorough but much of its depth is at the wrong level: test case enumeration, business KPIs, capacity projections, sprint checklists. B's depth is more consistently at the design level: 89 FRs, detailed user flows, load test methodology, CI/CD gate behavior, SLO burn-rate alerting. |
| API documentation quality | 4 | 4 | A: breadth (21 endpoints). B: depth (JSON examples). Both are useful; neither is complete on its own. |
| Maintainability | 2 | 3 | A: 3,781 lines (2.1x template ceiling) = significant maintenance burden, exacerbated by content that belongs in other documents and will drift. B: 2,777 lines (1.5x template ceiling) = still over but more manageable. Template says >2,000 is "a code smell." |

---

## Key Differences

Verified factual differences only:

- **Line count:** A = 3,781; B = 2,777. Delta = 1,004 lines (A is 36% larger).
- **Template line budget:** Both templates set Heavyweight ceiling at 1,800 lines. A exceeds by 2.1x; B by 1.5x. Both templates flag >2,000 as "a code smell."
- **Functional requirements:** A = 37 FRs; B = 89 FRs. B has 2.4x more fine-grained requirements.
- **Non-functional requirements:** A = 47 NFRs; B = 46 NFRs. Comparable.
- **Provenance tags:** A = 0; B = 69 (43 RESEARCH-VERIFIED + 26 CODE-VERIFIED).
- **`__table_args__` ORM code:** A = 0 instances; B = 2 instances (lines 778, 829).
- **Contract Table:** A = absent; B = present (line 129).
- **Appendices:** A = absent; B = present with 3 appendices (line 2723).
- **Section 5 ad-hoc subsections:** A has S5.3 (Source Traceability Matrix, line 513) and S5.4 (Completeness Verification, line 578). Neither exists in either template. B has only S5.1 and S5.2 per template.
- **Alternatives:** Both have 5. A: Alternative 0 + Option B + Option D + Fixed Agile + Offset Pagination (lines 3259-3302). B: Alternative 0-4 (lines 2379-2427). B uses consistent numbering. A uses inconsistent naming. B includes Pure Relational (Option A) which A omits.
- **Risks:** A = 9 risks (R1-R9) + heat map + top-3 callout (lines 3225-3253). B = 10 risks (R1-R10) without heat map (lines 2358-2371). B has more risks.
- **State management:** A centralizes in 250 lines (lines 2176-2425). B distributes across 114 lines (lines 1528-1641) with some content in FRs and architecture.
- **User flows:** A = 114 lines (lines 2514-2627). B = 219 lines (lines 1650-1868). B has nearly 2x the agent workflow detail.
- **Component inventory:** A repurposes as 88-line service inventory with file paths (lines 2426-2513). B marks N/A in 8 lines (lines 1642-1649).
- **Open questions:** A = 18 questions + 8 research gaps, phase-organized (lines 3306-3353). B = 9 questions in single table (lines 2431-2443).
- **API endpoints:** A lists 21 REST endpoints + 5 facade tools (643 lines). B lists 5 REST endpoints + 5 facade tools with JSON examples (292 lines).
- **Document Provenance:** A = absent. B = present (line 2775), 3 lines tracking assembly metadata.

---

## Verdict

**Version B is the stronger TDD.** It wins 10 sections to A's 3 (with 21 ties/splits). More importantly, B consistently operates at the correct abstraction level for a Technical Design Document, while A repeatedly imports content from adjacent document types (PRD, test plan, sprint plan).

### Where Version A is genuinely stronger:

1. **Centralized state machine** (S9, lines 2176-2425): Having the full transition matrix, guard conditions, and side effects in one place is better than distributing them. This is Version A's best organizational decision.
2. **Security detail** (S13): More detailed RLS policy documentation and JWT claim specifications.
3. **Migration rollback procedures** (S19): Per-phase rollback steps with time estimates. This is legitimate TDD content -- migration safety is a design concern.

### Where Version A was previously over-credited (corrections applied):

1. **Success Metrics (S4):** Previously awarded to A for "more granular SLO targets." Corrected: A's S4.2 "Business Metrics with Engineering Proxies" contains PRD-level KPIs (Feature Adoption rates, Enterprise Pipeline Conversion, Support Ticket Reduction). These are product metrics, not technical design metrics. B wins.
2. **Technical Requirements (S5):** Previously awarded to A for traceability matrix. Corrected: S5.3 and S5.4 are ad-hoc additions not in either template. B follows the template and has 89 FRs vs 37. B wins.
3. **Observability (S14):** Previously awarded to A for "more Prometheus metrics." Corrected: A TDD specifies monitoring strategy, not every counter. B's 14 metrics cover all critical concerns; B's SLO burn-rate alerting is more mature. Tie.
4. **Testing (S15):** Previously a tie. Corrected: A enumerates ~45 test cases (test plan content). B specifies testing strategy with load test methodology and CI/CD gates. B wins.
5. **Open Questions (S22):** Previously awarded to A for "18 questions vs 9." Corrected: 7 of A's questions are PRD-scope (pricing, user research, Pixel Streaming caps). B's questions are tightly scoped to technical implementation. Tie.
6. **Timeline (S23):** Previously awarded to A for "per-phase exit criteria." Corrected: Detailed exit checklists belong in the tasklist/sprint plan. Both cover the same phases and dependencies. Tie.
7. **Release Criteria (S24):** Previously marginally awarded to A. Corrected: A's per-phase DoD checklists duplicate S23 content and belong in sprint planning. B's structure (general DoD + rollback table) is more TDD-appropriate. Tie.
8. **Performance Budgets (S17):** Previously awarded to A. Corrected: Both define the same core latency budgets. Per-endpoint p95/p99 granularity is implementation-level detail. Tie.

### Where Version B is genuinely stronger:

1. **Template compliance**: Contract Table present (line 129). Appendices present (line 2723). Consistent section naming. 1 minor ad-hoc addition vs A's 3 violations.
2. **Provenance tags** (69 tags): Engineers know which claims are verified versus speculative. Zero tags in Version A.
3. **JSON API examples** (S8): Directly testable contract specifications. Engineers can write integration tests from these immediately.
4. **User flow depth** (S11, 219 lines): Detailed agent workflow sequences for the primary use case (AI agents).
5. **Component inventory honesty** (S10): 8-line N/A with rationale is more appropriate than 88 lines repurposing a frontend section for backend file paths.
6. **Alternative analysis consistency** (S21): 5 alternatives with consistent numbering (0-4). Includes Pure Relational (Option A) that Version A omits. All tagged with `[RESEARCH-VERIFIED]`.
7. **Risk section completeness** (S20): 10 risks versus A's 9.
8. **Correct abstraction level**: B's depth is concentrated where it matters for a TDD (FRs, user flows, API contracts, load test methodology). A's depth is scattered across adjacent document types.
9. **Shorter and closer to template budget**: 2,777 lines (1.5x ceiling) vs 3,781 lines (2.1x ceiling). 1,004 fewer lines without losing essential design content -- the delta is largely PRD/test-plan/sprint-plan leakage.
10. **Testing strategy** (S15): Load test specification with agent behavior model, CI/CD gate behavior per phase -- design-level content that guides implementation without being the implementation.

### Overall assessment:

**If choosing one to hand to an engineering team:** Version B is clearly the better starting point. It is shorter, more maintainable, more template-compliant, stays at the design level, and its provenance tags and JSON examples provide immediate utility. Its depth is concentrated where a TDD should be deep (requirements, user flows, API contracts) rather than where other documents should be deep (metrics enumeration, test case catalogs, sprint checklists).

**Version A's best contributions should be merged into B:** The centralized state machine (S9) is a better organizational pattern. The traceability matrix concept (S5.3) should be proposed as a standard template addition. The research gaps (I1-I8 in S22.4) are genuinely useful. The migration rollback detail (S19) adds real value. These specific contributions can be integrated without importing A's abstraction-level problems.

**Both versions need trimming.** Neither meets the template's own line budget. Both contain implementation-level code that should be moved to Appendices or linked documents. The ideal TDD takes Version B's structure, compliance, and provenance, then integrates Version A's centralized state machine and migration detail -- and cuts both down toward the template's 1,800-line ceiling.

---

## Verification Log

Every factual claim in this review was verified against the source files. Key verifications:

| Claim | Verification Method | Result |
|-------|-------------------|--------|
| `__table_args__` location | `grep -n "__table_args__"` on both TDDs | A: 0 matches. B: lines 778, 829. |
| Provenance tag counts | `grep -cn "RESEARCH-VERIFIED\|CODE-VERIFIED"` on both TDDs | A: 0. B: 69 (43 + 26). |
| Section 20 existence in B | `grep -n "^## 20"` on Version B | Line 2358: `## 20. Risks & Mitigations` with 10 risks (R1-R10). |
| Alternative counts | `grep -n "^### Alternative\|^### Option"` on both TDDs | A: 5 (lines 3259, 3268, 3277, 3286, 3295). B: 5 (lines 2379, 2389, 2399, 2409, 2419). |
| Contract Table presence | `grep -n "Contract Table"` on both TDDs | A: 0 matches. B: line 129. |
| Appendices presence | `grep -n "Appendix\|Appendices"` on Version A | 0 matches. Version B: line 2723. |
| Line budget guidance | `grep -n "code smell\|2,000 lines"` on both templates | Template A line 1290, Template B line 1265: identical wording. |
| FR counts | `grep -c "^| FR-"` on both TDDs | A: 37. B: 89. |
| NFR counts | `grep -c "^| NFR-"` on both TDDs | A: 47. B: 46. |
| Line counts | `wc -l` on both TDDs | A: 3,781. B: 2,777. |
| Template diff | QA Report 2 verified: 96% identical, 25-line diff in frontmatter and pipeline guidance | Confirmed. |
