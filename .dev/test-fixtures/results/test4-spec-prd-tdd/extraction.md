---
spec_source: "test-tdd-user-auth.md"
generated: "2026-04-15T00:00:00Z"
generator: "metadata-extract"
extraction_mode: "metadata-only"
functional_requirements: 10
nonfunctional_requirements: 8
total_requirements: 18
complexity_score: 0.72
complexity_class: "HIGH"
domains_detected: [backend, security, frontend, infrastructure, operations, compliance]
risks_identified: 7
dependencies_identified: 8
success_criteria_count: 10
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 9
test_artifacts_identified: 6
migration_items_identified: 10
operational_items_identified: 12
total_entities: 144
estimated_task_rows: 166
pipeline_diagnostics: {elapsed_seconds: 408.1, started_at: "2026-04-15T01:08:08.228120+00:00", finished_at: "2026-04-15T01:14:56.279965+00:00"}
---

## Section Inventory

### TDD Sections (Primary)

| Section | Heading/Title | Entity Count | Entity Type | IDs Found |
|---------|---------------|--------------|-------------|-----------|
| TDD-FM | Frontmatter / Document Info | 1 | GENERAL | AUTH-001-TDD |
| TDD-1 | Executive Summary | 6 | GENERAL | none |
| TDD-2 | Problem Statement & Context | 3 | GENERAL | none |
| TDD-3.1 | Goals | 5 | GENERAL | G-001, G-002, G-003, G-004, G-005 |
| TDD-3.2 | Non-Goals | 3 | GENERAL | NG-001, NG-002, NG-003 |
| TDD-4 | Success Metrics | 7 | GENERAL | none |
| TDD-5.1 | Functional Requirements | 5 | FR | FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004, FR-AUTH-005 |
| TDD-5.2 | Non-Functional Requirements | 5 | NFR | NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002 |
| TDD-6 | Architecture | 5 | GENERAL | none |
| TDD-7 | Data Models | 2 | DM | none |
| TDD-8 | API Specifications | 6 | API | none |
| TDD-9 | State Management | 0 | N/A | none |
| TDD-10 | Component Inventory | 9 | COMP | none |
| TDD-11 | User Flows & Interactions | 2 | GENERAL | none |
| TDD-12 | Error Handling & Edge Cases | 6 | GENERAL | none |
| TDD-13 | Security Considerations | 7 | GENERAL | none |
| TDD-14 | Observability & Monitoring | 7 | OPS | none |
| TDD-15 | Testing Strategy | 6 | TEST | none |
| TDD-16 | Accessibility Requirements | 0 | N/A | FE-AUTH-001-TDD |
| TDD-17 | Performance Budgets | 3 | NFR | none |
| TDD-18 | Dependencies | 6 | GENERAL | INFRA-DB-001 |
| TDD-19 | Migration & Rollout Plan | 10 | MIG | AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH |
| TDD-20 | Risks & Mitigations | 3 | GENERAL | R-001, R-002, R-003 |
| TDD-21 | Alternatives Considered | 3 | GENERAL | none |
| TDD-22 | Open Questions | 2 | GENERAL | OQ-001, OQ-002 |
| TDD-23 | Timeline & Milestones | 8 | GENERAL | M1, M2, M3, M4, M5 |
| TDD-24 | Release Criteria | 14 | GENERAL | none |
| TDD-25 | Operational Readiness | 9 | OPS | none |
| TDD-26 | Cost & Resource Estimation | 1 | GENERAL | none |
| TDD-27 | References & Resources | 5 | REF | AUTH-PRD-001, SEC-POLICY-001 |
| TDD-28 | Glossary | 5 | GENERAL | none |

### PRD Sections (Supplementary)

| Section | Heading/Title | Entity Count | Entity Type | IDs Found |
|---------|---------------|--------------|-------------|-----------|
| PRD-FM | Frontmatter / Document Info | 1 | GENERAL | AUTH-PRD-001 |
| PRD-Exec | Executive Summary | 4 | GENERAL | none |
| PRD-Problem | Problem Statement | 3 | GENERAL | none |
| PRD-Strategic | Background and Strategic Fit | 3 | GENERAL | none |
| PRD-Vision | Product Vision | 1 | GENERAL | none |
| PRD-Business | Business Context | 1 | GENERAL | none |
| PRD-JTBD | Jobs To Be Done | 4 | GENERAL | none |
| PRD-Personas | User Personas | 3 | GENERAL | none |
| PRD-Constraints | Assumptions and Constraints | 7 | GENERAL | none |
| PRD-Deps | Dependencies | 4 | GENERAL | none |
| PRD-Scope | Scope Definition | 4 | GENERAL | none |
| PRD-OQ | Open Questions | 4 | GENERAL | none |
| PRD-FR | Functional Requirements | 5 | FR | FR-AUTH.1, FR-AUTH.2, FR-AUTH.3, FR-AUTH.4, FR-AUTH.5 |
| PRD-NFR | Non-Functional Requirements | 3 | NFR | NFR-AUTH.1, NFR-AUTH.2, NFR-AUTH.3 |
| PRD-UX | User Experience Requirements | 3 | GENERAL | none |
| PRD-Legal | Legal and Compliance Requirements | 4 | GENERAL | none |
| PRD-Metrics | Success Metrics and Measurement | 5 | GENERAL | none |
| PRD-Risks | Risk Analysis | 4 | GENERAL | none |
| PRD-Epics | Implementation Plan — Epics | 3 | GENERAL | AUTH-E1, AUTH-E2, AUTH-E3 |
| PRD-Stories | Implementation Plan — User Stories | 8 | GENERAL | none |
| PRD-Journeys | Customer Journey Map | 4 | GENERAL | none |
| PRD-Errors | Error Handling and Edge Cases | 8 | GENERAL | none |
| PRD-Refs | Related Resources | 3 | REF | PLATFORM-PRD-001, COMPLIANCE-001 |

## Complexity Assessment

**Score: 0.72 — HIGH**

Scoring rationale:

| Factor | Weight | Assessment | Contribution |
|--------|--------|------------|--------------|
| Requirement density | 0.20 | 18 total requirements (10 FR + 8 NFR) with detailed acceptance criteria across two documents | +0.14 |
| Architectural surface | 0.20 | 9 components across backend and frontend; dual data stores (PostgreSQL + Redis); stateless JWT architecture with refresh token lifecycle | +0.16 |
| Cross-domain span | 0.15 | 6 domains detected (backend, security, frontend, infrastructure, operations, compliance); SOC2/GDPR requirements compound security complexity | +0.12 |
| API surface | 0.10 | 6 API endpoints including 2 implied password-reset endpoints not fully specified in section 8 (gap between FR-AUTH-005 and API docs) | +0.07 |
| Migration complexity | 0.15 | 3-phase rollout (alpha → 10% beta → GA); 2 feature flags; rollback procedure with 4 automated trigger criteria | +0.11 |
| Operational burden | 0.10 | 12 operational items: 2 runbook scenarios, 3 monitoring alerts, 4 Prometheus metrics, 3 capacity planning resources; 24/7 on-call rotation post-GA | +0.07 |
| Test coverage | 0.10 | 3-tier test pyramid (unit/integration/E2E) with 6 specified test cases; 3 test environments; 80% unit coverage target | +0.05 |

Entity counts supporting the assessment: 2 data models, 6 API surfaces, 9 components, 6 test artifacts, 10 migration items, 12 operational items, 7 risks across both documents. The two-document structure (TDD + PRD) with overlapping but differently-identified requirements (FR-AUTH-001 ↔ FR-AUTH.1) adds traceability complexity.

## ID Registry

| ID | Type | Source Section | Brief Label (<=10 words) |
|----|------|---------------|--------------------------|
| AUTH-001-TDD | DOC | TDD Frontmatter | TDD document identifier |
| AUTH-PRD-001 | DOC/REF | PRD Frontmatter, TDD-27 | PRD document identifier and parent reference |
| G-001 | GOAL | TDD-3.1 | Secure user registration and login |
| G-002 | GOAL | TDD-3.1 | Stateless token-based sessions |
| G-003 | GOAL | TDD-3.1 | Self-service password reset |
| G-004 | GOAL | TDD-3.1 | Profile management via /auth/me |
| G-005 | GOAL | TDD-3.1 | Frontend integration with AuthProvider |
| NG-001 | NON-GOAL | TDD-3.2 | Social/OAuth login deferred to v1.1 |
| NG-002 | NON-GOAL | TDD-3.2 | MFA deferred to v1.2 |
| NG-003 | NON-GOAL | TDD-3.2 | RBAC enforcement out of scope |
| FR-AUTH-001 | FR | TDD-5.1 | Login with email and password |
| FR-AUTH-002 | FR | TDD-5.1 | User registration with validation |
| FR-AUTH-003 | FR | TDD-5.1 | JWT token issuance and refresh |
| FR-AUTH-004 | FR | TDD-5.1 | User profile retrieval |
| FR-AUTH-005 | FR | TDD-5.1 | Password reset two-step flow |
| NFR-PERF-001 | NFR | TDD-5.2 | API response time < 200ms p95 |
| NFR-PERF-002 | NFR | TDD-5.2 | 500 concurrent login requests |
| NFR-REL-001 | NFR | TDD-5.2 | 99.9% uptime over 30-day windows |
| NFR-SEC-001 | NFR | TDD-5.2 | bcrypt with cost factor 12 |
| NFR-SEC-002 | NFR | TDD-5.2 | RS256 with 2048-bit RSA keys |
| R-001 | RISK | TDD-20 | Token theft via XSS |
| R-002 | RISK | TDD-20 | Brute-force attacks on login endpoint |
| R-003 | RISK | TDD-20 | Data loss during migration |
| OQ-001 | QUESTION | TDD-22 | API key auth for service-to-service calls |
| OQ-002 | QUESTION | TDD-22 | Max UserProfile roles array length |
| M1 | MILESTONE | TDD-23.1 | Core AuthService by 2026-04-14 |
| M2 | MILESTONE | TDD-23.1 | Token Management by 2026-04-28 |
| M3 | MILESTONE | TDD-23.1 | Password Reset by 2026-05-12 |
| M4 | MILESTONE | TDD-23.1 | Frontend Integration by 2026-05-26 |
| M5 | MILESTONE | TDD-23.1 | GA Release by 2026-06-09 |
| AUTH_NEW_LOGIN | FLAG | TDD-19.2 | Gates new LoginPage and AuthService |
| AUTH_TOKEN_REFRESH | FLAG | TDD-19.2 | Enables refresh token flow |
| INFRA-DB-001 | REF | TDD Frontmatter | Database infrastructure dependency |
| SEC-POLICY-001 | REF | TDD-27, PRD-Refs | Security policy for hashing and tokens |
| FE-AUTH-001-TDD | REF | TDD-16 | Frontend auth accessibility TDD |
| FR-AUTH.1 | FR | PRD-FR | Login with persistent session |
| FR-AUTH.2 | FR | PRD-FR | Account creation with email/password |
| FR-AUTH.3 | FR | PRD-FR | Session persistence across refreshes |
| FR-AUTH.4 | FR | PRD-FR | Profile viewing for logged-in users |
| FR-AUTH.5 | FR | PRD-FR | Self-service password reset via email |
| NFR-AUTH.1 | NFR | PRD-NFR | 200ms p95 and 500 concurrent |
| NFR-AUTH.2 | NFR | PRD-NFR | 99.9% availability over 30 days |
| NFR-AUTH.3 | NFR | PRD-NFR | Industry-standard one-way password hashing |
| AUTH-E1 | EPIC | PRD-Epics | Login and Registration |
| AUTH-E2 | EPIC | PRD-Epics | Token Management |
| AUTH-E3 | EPIC | PRD-Epics | Profile and Password Reset |
| PLATFORM-PRD-001 | REF | PRD-Refs | Parent platform requirements document |
| COMPLIANCE-001 | REF | PRD-Refs | SOC2 audit logging requirements |

**Registry totals:** 48 unique IDs (31 implementable TDD, 5 reference, 12 PRD-specific)

**Traceability mapping (TDD FR ↔ PRD FR):**

| TDD ID | PRD ID | Overlap |
|--------|--------|---------|
| FR-AUTH-001 | FR-AUTH.1 | Login flow |
| FR-AUTH-002 | FR-AUTH.2 | Registration flow |
| FR-AUTH-003 | FR-AUTH.3 | Token/session persistence |
| FR-AUTH-004 | FR-AUTH.4 | Profile retrieval |
| FR-AUTH-005 | FR-AUTH.5 | Password reset |

## Estimated Task Row Allocation

### Entity-to-Task Baseline

| Category | Count | Source |
|----------|-------|--------|
| FR (TDD) | 5 | FR-AUTH-001 through FR-AUTH-005 |
| FR (PRD) | 5 | FR-AUTH.1 through FR-AUTH.5 |
| NFR (TDD) | 5 | NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002 |
| NFR (PRD) | 3 | NFR-AUTH.1, NFR-AUTH.2, NFR-AUTH.3 |
| Data Models | 2 | UserProfile, AuthToken |
| API Surfaces | 6 | 4 specified + 2 implied (reset-request, reset-confirm) |
| Components | 9 | 4 frontend + 5 backend |
| Test Artifacts | 6 | 3 unit + 2 integration + 1 E2E |
| Migration Items | 10 | 3 phases + 2 flags + 1 rollback procedure + 4 rollback criteria |
| Operational Items | 12 | 2 runbook + 3 alerts + 4 metrics + 3 capacity |
| **Subtotal (frontmatter categories)** | **63** | |
| Goals | 5 | G-001 through G-005 |
| Non-Goals | 3 | NG-001 through NG-003 |
| Risks | 7 | 3 TDD + 4 PRD |
| Dependencies | 8 | 6 technical + 2 policy/infrastructure |
| Success Criteria | 10 | 7 TDD + 5 PRD (2 overlap) |
| Open Questions | 6 | 2 TDD + 4 PRD |
| Milestones | 5 | M1 through M5 |
| Epics (PRD) | 3 | AUTH-E1, AUTH-E2, AUTH-E3 |
| User Stories (PRD) | 8 | 3 AUTH-E1 + 2 AUTH-E2 + 3 AUTH-E3 |
| Personas (PRD) | 3 | Alex, Jordan, Sam |
| JTBD (PRD) | 4 | 4 jobs-to-be-done |
| Customer Journeys (PRD) | 4 | Signup, Login, Reset, Profile |
| Error Scenarios (PRD) | 8 | 8 edge case behaviors |
| Legal/Compliance (PRD) | 4 | GDPR consent, SOC2 audit, NIST hashing, data minimization |
| Alternatives | 3 | Do nothing, Auth0, sessions |
| **Total entities** | **144** | |

### Per-Phase Allocation

Based on TDD milestones (M1–M5) and PRD phasing (Sprint 1–3, Sprint 4–6):

| Phase | Scope | Implementable Entities | Wiring/Integration (+15%) | Task Rows |
|-------|-------|----------------------|--------------------------|-----------|
| Phase 1: Core Auth (M1) | AuthService, PasswordHasher, UserProfile schema, /auth/register, /auth/login | FR-AUTH-001, FR-AUTH-002, NFR-SEC-001, UserProfile DM, 2 APIs, 3 backend components | 18 + 3 | **21** |
| Phase 2: Token Mgmt (M2) | TokenManager, JwtService, AuthToken model, /auth/refresh, /auth/me | FR-AUTH-003, FR-AUTH-004, NFR-PERF-001, NFR-PERF-002, NFR-SEC-002, NFR-REL-001, AuthToken DM, 2 APIs, 2 backend components | 22 + 4 | **26** |
| Phase 3: Reset & Frontend (M3–M4) | Password reset flow, LoginPage, RegisterPage, AuthProvider, email integration | FR-AUTH-005, G-005, 2 implied APIs, 4 frontend components, 3 user stories | 20 + 3 | **23** |
| Phase 4: Testing & Validation | Unit/integration/E2E tests, security review, performance testing | 6 test artifacts, 5 NFR validations, security review | 14 + 2 | **16** |
| Phase 5: Migration & Rollout (M5) | 3-phase rollout, feature flags, monitoring, runbooks | 10 migration items, 12 operational items, 7 risk mitigations | 32 + 5 | **37** |
| Phase 6: PRD Traceability | PRD requirement coverage verification, acceptance scenario validation | 5 PRD FRs, 3 PRD NFRs, 8 user stories, 8 error scenarios, 4 legal items, 4 customer journeys | 38 + 6 | **44** |
| **Total** | | | | **167** |

**Note:** PRD FRs (FR-AUTH.1–.5) trace 1:1 to TDD FRs (FR-AUTH-001–005). Phase 6 rows validate PRD acceptance criteria against TDD implementation — they are verification tasks, not duplicate implementation. The generate step should collapse overlapping PRD/TDD rows where the task is identical and add traceability annotations instead.

**Formula check:** total_entities (144) × 1.15 = 165.6 → **166** (rounded up). Allocation total of 167 is within 1% of the formula estimate, confirming coverage.
