# Synthesis Mapping Reference

> Output Structure reference and Synthesis Mapping Table, loaded during Stage A.7 by the builder subagent.

---

## Output Structure

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

The final TDD follows the template at `src/superclaude/examples/tdd_template.md`. The synthesis agents produce sections that are assembled into this format.

```markdown
---
[frontmatter from template]
---

# [Component Name] - Technical Design Document (TDD)

**Document Type:** Technical Design Document (Engineering Specification)
**Purpose:** [one-sentence purpose]
**Date:** [today]
**Tier:** [Lightweight / Standard / Heavyweight]
**Parent PRD:** [link to Product PRD, if applicable]

---

## Document Information
Component metadata table and Approvers table.

## Table of Contents
[Generated from section headers]

---

## 1. Executive Summary
Key deliverables, high-level scope, 2-3 paragraph overview.

## 2. Problem Statement & Context
Background, problem statement, business context, PRD reference.

## 3. Goals & Non-Goals
Goals with success criteria, explicit non-goals with rationale, future considerations.

## 4. Success Metrics
Technical metrics and business KPIs with baselines, targets, and measurement methods.

## 5. Technical Requirements
Functional requirements (FR-001 numbering), non-functional requirements (performance, scalability, reliability, SLOs, security).

## 6. Architecture
High-level architecture, component diagram, system boundaries, key design decisions, multi-tenancy (if applicable).

## 7. Data Models
Data entities with field tables, data flow diagrams, storage strategy.

## 8. API Specifications
Endpoint overview, detailed endpoint specs, error response format, API governance & versioning.

## 9. State Management (if applicable — frontend)
State architecture, state shape, state transitions.

## 10. Component Inventory (if applicable — frontend)
Page/route structure, shared components, component hierarchy.

## 11. User Flows & Interactions
Sequence diagrams, step-by-step flows, success criteria, error scenarios.

## 12. Error Handling & Edge Cases
Error categories, edge cases, graceful degradation, retry strategies.

## 13. Security Considerations
Threat model, security controls, sensitive data handling, data governance & compliance.

## 14. Observability & Monitoring
Logging, metrics, tracing, alerts, dashboards, business metric instrumentation.

## 15. Testing Strategy
Test pyramid, test cases (unit/integration/E2E), test environments.

## 16. Accessibility Requirements
WCAG 2.1 AA requirements and testing tools.

## 17. Performance Budgets
Frontend performance, backend performance, performance testing.

## 18. Dependencies
External, internal, and infrastructure dependencies.

## 19. Migration & Rollout Plan
Migration strategy, feature flags & progressive delivery, rollout stages, rollback procedure.

## 20. Risks & Mitigations
Risk table with probability, impact, mitigation, and contingency.

## 21. Alternatives Considered
Alternative 0: Do Nothing (mandatory), plus additional alternatives with pros/cons.

## 22. Open Questions
Question tracking table with owner, target date, status, resolution.

## 23. Timeline & Milestones
High-level timeline and implementation phases with exit criteria.

## 24. Release Criteria
Definition of Done checklist, release checklist.

## 25. Operational Readiness
Runbook, on-call expectations, capacity planning.

## 26. Cost & Resource Estimation (if applicable)
Infrastructure costs, cost scaling model, optimization opportunities.

## 27. References & Resources
Related documents and external references.

## 28. Glossary
Term definitions.

## Document History
Version table.

## Appendices
A: Detailed API Specifications, B: Database Schema, C: Wireframes, D: Performance Test Results.
```

---

## Synthesis Mapping Table

> **Note:** This section is reference documentation. The BUILD_REQUEST phases (Stage A) are authoritative for task file construction.

Maps synth files to TDD template sections and their source research files. Synthesis agents use this mapping to know which template sections they are responsible for and which research files to draw from.

| Synth File | Template Sections | Source Research Files |
|------------|-------------------|----------------------|
| `synth-01-exec-problem-goals.md` | 1. Executive Summary, 2. Problem Statement & Context, 3. Goals & Non-Goals, 4. Success Metrics | PRD extraction, architecture overview, existing docs |
| `synth-02-requirements.md` | 5. Technical Requirements | PRD extraction, architecture overview, all subsystem research |
| `synth-03-architecture.md` | 6. Architecture | architecture overview, integration points, subsystem research, 00-prd-extraction.md (Section 4: Technical Requirements — architectural constraints) |
| `synth-04-data-api.md` | 7. Data Models, 8. API Specifications | data models research, API surface research, web research (API standards, schema patterns), 00-prd-extraction.md (Section 2: User Stories and ACs — data model traceability) |
| `synth-05-state-components.md` | 9. State Management, 10. Component Inventory, 11. User Flows | state management research, subsystem research, 00-prd-extraction.md (Section 2: User Stories and ACs — interaction flows; Section 5: Scope Boundaries) |
| `synth-06-error-security.md` | 12. Error Handling & Edge Cases, 13. Security Considerations | security research, all subsystem research, web research (security patterns, threat models), 00-prd-extraction.md (Section 4: Technical Requirements — security and error-handling constraints) |
| `synth-07-observability-testing.md` | 14. Observability & Monitoring, 15. Testing Strategy | architecture overview, integration points, web research (SLO benchmarks, testing patterns), 00-prd-extraction.md (Section 3: Success Metrics — KPIs to translate into observability targets; Section 2: ACs — acceptance criteria driving test coverage) |
| `synth-08-perf-deps-migration.md` | 16. Accessibility, 17. Performance Budgets, 18. Dependencies, 19. Migration & Rollout | PRD extraction, architecture overview, all subsystem research, web research (performance benchmarks) |
| `synth-09-risks-alternatives-ops.md` | 20. Risks, 21. Alternatives Considered, 22. Open Questions, 23. Timeline, 24. Release Criteria, 25. Operational Readiness, 26. Cost | PRD extraction, all research files, web research (industry practices), gaps log |

**PRD extraction fallback:** When `00-prd-extraction.md` is absent (no PRD provided), synthesis agents skip PRD-sourced content for that mapping row and note "PRD source unavailable -- requirements derived from feature description and codebase research" in the synthesis file. Do not fail or block on the missing file.

Adjust the mapping based on component complexity. Backend components skip Section 9 (State Management) and Section 10 (Component Inventory). Small components can combine more sections per synth file.
