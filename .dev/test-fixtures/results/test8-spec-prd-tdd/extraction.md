---
spec_source: "test-tdd-user-auth.md"
generated: "2026-04-15T00:00:00Z"
generator: "metadata-extract"
extraction_mode: "metadata-only"
functional_requirements: 10
nonfunctional_requirements: 8
total_requirements: 18
complexity_score: 0.64
complexity_class: "MEDIUM"
domains_detected: [backend, security, frontend, infrastructure]
risks_identified: 7
dependencies_identified: 9
success_criteria_count: 12
data_models_identified: 2
api_surfaces_identified: 4
components_identified: 10
test_artifacts_identified: 6
migration_items_identified: 6
operational_items_identified: 12
total_entities: 101
estimated_task_rows: 117
---

## Section Inventory

### TDD (AUTH-001-TDD)

| Section | Heading/Title | Entity Count | Entity Type | IDs Found |
|---|---|---|---|---|
| 1 | Executive Summary | 0 | GENERAL | none |
| 2 | Problem Statement & Context | 0 | GENERAL | none |
| 3 | Goals & Non-Goals | 8 | GENERAL | G-001..G-005, NG-001..NG-003 |
| 4 | Success Metrics | 7 | GENERAL | none |
| 5.1 | Functional Requirements | 5 | FR | FR-AUTH-001..FR-AUTH-005 |
| 5.2 | Non-Functional Requirements | 5 | NFR | NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002 |
| 6 | Architecture | 6 | COMP | none (synthetic COMP-001..006 assigned) |
| 7 | Data Models | 2 | DM | none (synthetic DM-001..002 assigned) |
| 8 | API Specifications | 4 | API | none (synthetic API-001..004 assigned) |
| 9 | State Management | 0 | N/A | none |
| 10 | Component Inventory | 4 | COMP | none (synthetic COMP-006..009 assigned) |
| 11 | User Flows & Interactions | 0 | GENERAL | none |
| 12 | Error Handling & Edge Cases | 0 | GENERAL | none |
| 13 | Security Considerations | 0 | GENERAL | none |
| 14 | Observability & Monitoring | 7 | OPS | none (synthetic OPS-MET/ALT assigned) |
| 15 | Testing Strategy | 6 | TEST | none (synthetic TEST-001..006 assigned) |
| 16 | Accessibility Requirements | 0 | N/A | none |
| 17 | Performance Budgets | 0 | GENERAL | none |
| 18 | Dependencies | 6 | GENERAL | none |
| 19 | Migration & Rollout Plan | 6 | MIG | none (synthetic MIG-001..003, MIG-FF-001..002, MIG-RB-001 assigned) |
| 20 | Risks & Mitigations | 3 | GENERAL | R-001, R-002, R-003 |
| 21 | Alternatives Considered | 0 | GENERAL | none |
| 22 | Open Questions | 2 | GENERAL | OQ-001, OQ-002 |
| 23 | Timeline & Milestones | 5 | GENERAL | M1..M5 |
| 24 | Release Criteria | 0 | GENERAL | none |
| 25 | Operational Readiness | 5 | OPS | none (synthetic OPS-RB/CAP assigned) |
| 26 | Cost & Resource Estimation | 0 | GENERAL | none |
| 27 | References & Resources | 0 | GENERAL | none |
| 28 | Glossary | 0 | GENERAL | none |

### PRD (AUTH-PRD-001)

| Section | Heading/Title | Entity Count | Entity Type | IDs Found |
|---|---|---|---|---|
| PRD-1 | Executive Summary | 0 | GENERAL | none |
| PRD-2 | Problem Statement | 0 | GENERAL | none |
| PRD-3 | Background and Strategic Fit | 0 | GENERAL | none |
| PRD-4 | Jobs To Be Done | 4 | GENERAL | none |
| PRD-5 | User Personas | 3 | GENERAL | none |
| PRD-6 | Assumptions and Constraints | 0 | GENERAL | none |
| PRD-7 | Dependencies | 4 | GENERAL | none |
| PRD-8 | Scope Definition | 0 | GENERAL | none |
| PRD-9 | Open Questions | 4 | GENERAL | none |
| PRD-10 | Functional Requirements | 5 | FR | FR-AUTH.1..FR-AUTH.5 |
| PRD-11 | Non-Functional Requirements | 3 | NFR | NFR-AUTH.1..NFR-AUTH.3 |
| PRD-12 | Legal and Compliance | 4 | GENERAL | none (synthetic LEGAL-001..004 assigned) |
| PRD-13 | Success Metrics | 5 | GENERAL | none |
| PRD-14 | Risk Analysis | 4 | GENERAL | none |
| PRD-15 | Epics | 3 | GENERAL | AUTH-E1, AUTH-E2, AUTH-E3 |
| PRD-16 | User Stories | 8 | FR | none (synthetic US-E*-* assigned) |
| PRD-17 | Customer Journey Map | 4 | GENERAL | none |
| PRD-18 | Error Handling and Edge Cases | 8 | GENERAL | none |

## Complexity Assessment

**Score: 0.64 — MEDIUM**

Scoring rationale:
- **Scope breadth (0.60):** Well-bounded single service, but spans backend, frontend, and infrastructure domains. 10 components, 4 API endpoints, 2 data models.
- **Technical depth (0.65):** JWT/RS256 signing, bcrypt hashing, Redis token management, PostgreSQL persistence — all well-understood but require precise implementation. 10 FR + 8 NFR across two documents.
- **Security sensitivity (0.75):** Authentication is security-critical. 2 dedicated NFR-SEC requirements, 3 risks with high-impact mitigations, compliance constraints (SOC2, NIST, GDPR).
- **Operational complexity (0.65):** 3-phase migration with feature flags, 12 operational items (runbooks, alerts, metrics, capacity), rollback procedure with 4 trigger criteria.
- **Integration complexity (0.55):** Few external integrations (SendGrid only). Frontend integration is straightforward (4 components). Internal service boundaries are clean.

The overall MEDIUM classification reflects a well-scoped authentication service with clear requirements, moderate technical depth, and a comprehensive operational footprint. The 3-phase rollout and security-critical nature push complexity above LOW, but the single-service boundary and standard tech stack keep it below HIGH.

## ID Registry

### TDD — Explicit IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| FR-AUTH-001 | FR | 5.1 | Login with email and password |
| FR-AUTH-002 | FR | 5.1 | User registration with validation |
| FR-AUTH-003 | FR | 5.1 | JWT token issuance and refresh |
| FR-AUTH-004 | FR | 5.1 | User profile retrieval |
| FR-AUTH-005 | FR | 5.1 | Password reset flow |
| NFR-PERF-001 | NFR | 5.2 | API response time < 200ms p95 |
| NFR-PERF-002 | NFR | 5.2 | 500 concurrent login requests |
| NFR-REL-001 | NFR | 5.2 | 99.9% uptime over 30-day windows |
| NFR-SEC-001 | NFR | 5.2 | bcrypt with cost factor 12 |
| NFR-SEC-002 | NFR | 5.2 | RS256 with 2048-bit RSA keys |
| G-001 | GOAL | 3.1 | Secure registration and login |
| G-002 | GOAL | 3.1 | Stateless token-based sessions |
| G-003 | GOAL | 3.1 | Self-service password reset |
| G-004 | GOAL | 3.1 | Profile management via /auth/me |
| G-005 | GOAL | 3.1 | Frontend integration components |
| NG-001 | NON-GOAL | 3.2 | Social/OAuth login deferred to v1.1 |
| NG-002 | NON-GOAL | 3.2 | MFA deferred to v1.2 |
| NG-003 | NON-GOAL | 3.2 | RBAC enforcement out of scope |
| R-001 | RISK | 20 | Token theft via XSS |
| R-002 | RISK | 20 | Brute-force attacks on login |
| R-003 | RISK | 20 | Data loss during migration |
| OQ-001 | OPEN-Q | 22 | API key auth for service-to-service |
| OQ-002 | OPEN-Q | 22 | Max UserProfile roles array length |
| M1 | MILESTONE | 23 | Core AuthService (2026-04-14) |
| M2 | MILESTONE | 23 | Token Management (2026-04-28) |
| M3 | MILESTONE | 23 | Password Reset (2026-05-12) |
| M4 | MILESTONE | 23 | Frontend Integration (2026-05-26) |
| M5 | MILESTONE | 23 | GA Release (2026-06-09) |

### TDD — Synthetic Component IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| COMP-001 | COMP | 6.1 | AuthService orchestrator |
| COMP-002 | COMP | 6.1 | TokenManager token lifecycle |
| COMP-003 | COMP | 6.1 | JwtService RS256 sign/verify |
| COMP-004 | COMP | 6.1 | PasswordHasher bcrypt abstraction |
| COMP-005 | COMP | 6.1 | UserRepo PostgreSQL data access |
| COMP-006 | COMP | 10.1 | LoginPage frontend component |
| COMP-007 | COMP | 10.1 | RegisterPage frontend component |
| COMP-008 | COMP | 10.1 | ProfilePage frontend component |
| COMP-009 | COMP | 10.2 | AuthProvider context wrapper |
| COMP-010 | COMP | 6.1 | API Gateway rate limiting and CORS |

### TDD — Synthetic Data Model IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| DM-001 | DM | 7.1 | UserProfile entity (7 fields) |
| DM-002 | DM | 7.1 | AuthToken response interface (4 fields) |

### TDD — Synthetic API IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| API-001 | API | 8.2 | POST /auth/login |
| API-002 | API | 8.2 | POST /auth/register |
| API-003 | API | 8.2 | GET /auth/me |
| API-004 | API | 8.2 | POST /auth/refresh |

### TDD — Synthetic Test IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| TEST-001 | TEST | 15.2 | Unit: login valid credentials returns AuthToken |
| TEST-002 | TEST | 15.2 | Unit: login invalid credentials returns error |
| TEST-003 | TEST | 15.2 | Unit: token refresh with valid token |
| TEST-004 | TEST | 15.2 | Integration: registration persists to database |
| TEST-005 | TEST | 15.2 | Integration: expired refresh token rejected |
| TEST-006 | TEST | 15.2 | E2E: user registers and logs in |

### TDD — Synthetic Migration IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| MIG-001 | MIG | 19.1 | Phase 1 Internal Alpha (1 week) |
| MIG-002 | MIG | 19.1 | Phase 2 Beta 10% traffic (2 weeks) |
| MIG-003 | MIG | 19.1 | Phase 3 GA 100% traffic (1 week) |
| MIG-FF-001 | MIG | 19.2 | Feature flag AUTH_NEW_LOGIN |
| MIG-FF-002 | MIG | 19.2 | Feature flag AUTH_TOKEN_REFRESH |
| MIG-RB-001 | MIG | 19.3 | Rollback procedure (6 steps) |

### TDD — Synthetic Operational IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| OPS-RB-001 | OPS | 25.1 | Runbook: AuthService down |
| OPS-RB-002 | OPS | 25.1 | Runbook: token refresh failures |
| OPS-ALT-001 | OPS | 14 | Alert: login failure rate > 20% |
| OPS-ALT-002 | OPS | 14 | Alert: p95 latency > 500ms |
| OPS-ALT-003 | OPS | 14 | Alert: Redis connection failures |
| OPS-MET-001 | OPS | 14 | Metric: auth_login_total counter |
| OPS-MET-002 | OPS | 14 | Metric: auth_login_duration_seconds histogram |
| OPS-MET-003 | OPS | 14 | Metric: auth_token_refresh_total counter |
| OPS-MET-004 | OPS | 14 | Metric: auth_registration_total counter |
| OPS-CAP-001 | OPS | 25.3 | Capacity: AuthService pods HPA scaling |
| OPS-CAP-002 | OPS | 25.3 | Capacity: PostgreSQL connection pool |
| OPS-CAP-003 | OPS | 25.3 | Capacity: Redis memory for tokens |

### PRD — Explicit IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| FR-AUTH.1 | FR | PRD-10 | Login with persistent session |
| FR-AUTH.2 | FR | PRD-10 | Registration with email and password |
| FR-AUTH.3 | FR | PRD-10 | Session persistence across refreshes |
| FR-AUTH.4 | FR | PRD-10 | Profile viewing for logged-in users |
| FR-AUTH.5 | FR | PRD-10 | Self-service password reset via email |
| NFR-AUTH.1 | NFR | PRD-11 | Performance: 200ms p95, 500 concurrent |
| NFR-AUTH.2 | NFR | PRD-11 | Reliability: 99.9% over 30 days |
| NFR-AUTH.3 | NFR | PRD-11 | Security: one-way password hashing |
| AUTH-E1 | EPIC | PRD-15 | Epic: Login and Registration |
| AUTH-E2 | EPIC | PRD-15 | Epic: Token Management |
| AUTH-E3 | EPIC | PRD-15 | Epic: Profile and Password Reset |

### PRD — Synthetic User Story IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| US-E1-001 | US | PRD-16 | Alex registers with email/password |
| US-E1-002 | US | PRD-16 | Alex logs in with credentials |
| US-E1-003 | US | PRD-16 | Alex logs out on shared device |
| US-E2-001 | US | PRD-16 | Alex session persists across refreshes |
| US-E2-002 | US | PRD-16 | Sam refreshes token programmatically |
| US-E3-001 | US | PRD-16 | Alex views profile details |
| US-E3-002 | US | PRD-16 | Alex resets forgotten password |
| US-E3-003 | US | PRD-16 | Jordan views auth event logs |

### PRD — Synthetic Legal/Compliance IDs

| ID | Type | Source Section | Brief Label |
|---|---|---|---|
| LEGAL-001 | LEGAL | PRD-12 | GDPR consent at registration |
| LEGAL-002 | LEGAL | PRD-12 | SOC2 audit logging (12-month retention) |
| LEGAL-003 | LEGAL | PRD-12 | NIST SP 800-63B password storage |
| LEGAL-004 | LEGAL | PRD-12 | GDPR data minimization |

**Registry total: 91 IDs** (28 TDD explicit + 40 TDD synthetic + 11 PRD explicit + 12 PRD synthetic)

## Estimated Task Row Allocation

**Formula applied:** total_entities (101) x 1.15 = 117 task rows (rounded up)

Note: TDD milestones (M1–M5) define the phase structure. PRD FRs and user stories overlap with TDD FRs and are mapped to the same phases for traceability. Goals, non-goals, open questions, and milestones are informational markers — they appear in the registry for traceability but do not generate standalone task rows.

| Phase | Milestone | Duration | Exit Criteria | Allocated Rows |
|---|---|---|---|---|
| **1: Core Auth** | M1 (2026-04-14) | 2 weeks | FR-AUTH-001, FR-AUTH-002 pass; unit + integration tests green | 24 |
| **2: Token Management** | M2 (2026-04-28) | 2 weeks | FR-AUTH-003, FR-AUTH-004 pass; NFR-SEC-002 verified; Redis integration tested | 26 |
| **3: Password Reset** | M3 (2026-05-12) | 2 weeks | FR-AUTH-005 pass; email integration functional; reset token TTL enforced | 12 |
| **4: Frontend Integration** | M4 (2026-05-26) | 2 weeks | LoginPage, RegisterPage, AuthProvider functional; E2E tests pass | 18 |
| **5: Migration, Ops & GA** | M5 (2026-06-09) | 2 weeks | 3-phase rollout complete; 99.9% uptime over 7 days; all OPS items deployed | 37 |

| Category | Rows |
|---|---|
| Phase 1–5 subtotal | 117 |
| Integration/wiring (~15%) | included in phase totals |

**Phase 1 breakdown (24):** COMP-001..005 (5), DM-001..002 (2), API-001..002 (2), FR-AUTH-001..002 (2), NFR-SEC-001, NFR-PERF-001 (2), TEST-001..002, TEST-004 (3), FR-AUTH.1..2 (2), US-E1-001..002 (2), LEGAL-003 (1), integration wiring (3).

**Phase 2 breakdown (26):** COMP-002..003 (2), DM-002 (1), API-003..004 (2), FR-AUTH-003..004 (2), NFR-SEC-002, NFR-PERF-002, NFR-REL-001 (3), TEST-003, TEST-005 (2), FR-AUTH.3..4, NFR-AUTH.1..3 (5), US-E2-001..002 (2), LEGAL-002 (1), R-001 mitigation (1), integration wiring (3).

**Phase 3 breakdown (12):** FR-AUTH-005 (1), FR-AUTH.5 (1), US-E3-002 (1), US-E3-003 (1), LEGAL-001 (1), LEGAL-004 (1), R-003 mitigation (1), AUTH-E3 epic validation (1), integration wiring (2), email service integration (2).

**Phase 4 breakdown (18):** COMP-006..010 (5), TEST-006 (1), US-E1-003, US-E3-001 (2), AUTH-E1..E2 epic validation (2), COMP-010 API Gateway config (1), R-002 mitigation (1), frontend auth flow wiring (3), cross-component integration (3).

**Phase 5 breakdown (37):** MIG-001..003 (3), MIG-FF-001..002 (2), MIG-RB-001 (1), OPS-RB-001..002 (2), OPS-ALT-001..003 (3), OPS-MET-001..004 (4), OPS-CAP-001..003 (3), success criteria instrumentation (5), release criteria validation (4), smoke test + rollback drill (3), documentation + runbook publish (3), go/no-go gate (1), feature flag cleanup (2), post-GA stabilization (1).
