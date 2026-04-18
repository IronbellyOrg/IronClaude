---
spec_source: test-tdd-user-auth.md
complexity_score: 0.72
primary_persona: architect
---

# Executive Summary

The User Authentication Service roadmap should be executed as a layered platform build, not as a UI-first feature sequence. The architecture centers on `AuthService` as the orchestration boundary, with `PasswordHasher`, `TokenManager`, `JwtService`, PostgreSQL, Redis, and frontend consumers (`LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`) integrated in controlled phases.

Architecturally, the critical path is:

1. Establish identity data, cryptography, and persistence foundations.
2. Implement credential and token flows with explicit wiring between `AuthService`, `PasswordHasher`, `TokenManager`, and `JwtService`.
3. Add profile, password reset, frontend session management, and audit/compliance coverage.
4. Harden for performance, reliability, rollout, and operational readiness.
5. Validate end-to-end traceability from TDD implementation details to PRD business outcomes and compliance obligations.

Key architect priorities in this roadmap:

- Preserve clear service boundaries between orchestration, cryptography, persistence, caching, and UI state.
- Make all dispatch/wiring mechanisms explicit rather than implied.
- Sequence compliance and operational readiness before GA, not after.
- Keep v1.0 scope tight: no OAuth, no MFA, no RBAC enforcement.
- Use PRD value drivers to prioritize registration, login, persistence, and auditability early.

## Phased Implementation Plan with Milestones

### Phase 1 — Architecture Foundation, Scope Guardrails, and Persistence Baseline

**Milestone alignment:** M1 foundation toward core `AuthService`

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | AUTH-001-TDD | Baseline the TDD as the implementation control document for v1.0 auth architecture | Architecture governance | None | Engineering plan explicitly references `test-tdd-user-auth.md` as the source spec; implementation scope and downstream work items trace back to this TDD | S | P0 |
| 2 | AUTH-PRD-001 | Baseline the PRD as the business and validation context for roadmap prioritization | Product traceability | AUTH-001-TDD | Roadmap explicitly traces delivery priorities to PRD success metrics, personas, compliance needs, and Q2/Q3 business drivers | S | P0 |
| 3 | G-001 | Establish secure registration and login as the first-value delivery stream | Auth domain planning | AUTH-001-TDD, AUTH-PRD-001 | Phase sequencing puts registration/login on the critical path; delivery plan maps to secure email/password auth with bcrypt hashing | S | P0 |
| 4 | G-002 | Establish stateless token session architecture with refresh lifecycle | Session architecture | AUTH-001-TDD | Architecture plan defines short-lived access token + refresh token model and assigns ownership to `TokenManager` and `JwtService` | S | P0 |
| 5 | G-003 | Reserve platform capability for self-service password reset | Recovery architecture | AUTH-001-TDD | Password reset is included in core scope with request/confirm flow, expiry, and single-use semantics | S | P1 |
| 6 | G-004 | Prioritize authenticated profile retrieval as a first-party identity capability | Profile architecture | AUTH-001-TDD | Roadmap includes authenticated `/auth/me` flow and `UserProfile` read model in core service scope | S | P1 |
| 7 | G-005 | Reserve frontend integration contract for `LoginPage`, `RegisterPage`, and `AuthProvider` | Frontend integration planning | AUTH-001-TDD, AUTH-PRD-001 | Frontend consumers are named in roadmap and phased after backend contracts are stable | S | P1 |
| 8 | NG-001 | Exclude social and OAuth login from v1.0 implementation | Scope governance | AUTH-001-TDD, AUTH-PRD-001 | No roadmap task introduces OAuth providers, social login UI, or third-party identity federation in v1.0 | S | P0 |
| 9 | NG-002 | Exclude MFA from v1.0 implementation | Scope governance | AUTH-001-TDD, AUTH-PRD-001 | No task includes TOTP, SMS, WebAuthn, or second-factor enforcement in v1.0 roadmap | S | P0 |
| 10 | NG-003 | Exclude RBAC enforcement while preserving roles field compatibility | Authorization boundary | AUTH-001-TDD | `roles` is stored and returned but no authorization enforcement logic is introduced in auth service v1.0 | S | P0 |
| 11 | INFRA-DB-001 | Provision PostgreSQL 15+ baseline for user, audit, and auth persistence | Infrastructure / PostgreSQL | AUTH-001-TDD | PostgreSQL 15+ environment exists with connectivity, pooling plan, and schema deployment path for auth workloads | M | P0 |
| 12 | PLATFORM-PRD-001 | Align auth roadmap to platform-level personalization dependency sequencing | Portfolio alignment | AUTH-PRD-001 | Roadmap sequencing explicitly supports platform personalization prerequisites without introducing out-of-scope platform features | S | P1 |
| 13 | COMP-001 | Define `AuthService` as the primary orchestration boundary for all auth flows | Backend service layer | G-001, G-002 | `AuthService` responsibilities are documented: registration, login, profile retrieval, password reset orchestration, token delegation, audit emission | M | P0 |
| 14 | COMP-002 | Define `TokenManager` as the refresh-token lifecycle manager | Backend session layer | G-002, INFRA-DB-001 | `TokenManager` ownership includes refresh issuance, revocation, rotation, Redis storage interaction, and failure behavior | M | P0 |
| 15 | COMP-003 | Define `JwtService` as the access-token signing and verification component | Security / token signing | G-002 | `JwtService` contract specifies RS256 signing, verification, clock skew tolerance, TTL enforcement, and key dependency boundaries | M | P0 |
| 16 | COMP-004 | Define `PasswordHasher` as the password hashing abstraction boundary | Security / credential handling | G-001 | `PasswordHasher` contract specifies bcrypt hash/verify responsibilities, cost factor 12, and algorithm encapsulation for future migration | M | P0 |
| 17 | COMP-005 | Define `UserRepo` persistence abstraction for `UserProfile` and auth reads/writes | Data access layer | INFRA-DB-001, COMP-001 | Persistence layer responsibilities are documented for create, lookup by email/id, update timestamps, and uniqueness enforcement | M | P0 |
| 18 | COMP-006 | Define `LoginPage` contract against backend login API | Frontend / login UI | G-005, COMP-001 | Frontend login contract specifies request payload, success redirect, generic error handling, and no user enumeration behavior | M | P1 |
| 19 | COMP-007 | Define `RegisterPage` contract against registration API | Frontend / registration UI | G-005, COMP-001 | Registration UI contract specifies form fields, client validation expectations, duplicate-email behavior, and redirect/login transition | M | P1 |
| 20 | COMP-008 | Define `AuthProvider` as the session state and silent refresh owner | Frontend / auth state | G-005, COMP-002, COMP-003 | `AuthProvider` responsibilities include token storage strategy, refresh trigger behavior, 401 handling, and user/profile exposure | M | P0 |
| 21 | COMP-009 | Define `ProfilePage` integration contract for authenticated user profile display | Frontend / profile UI | G-004, G-005 | Profile UI contract specifies required fields, auth dependency, and redirect behavior when authentication is absent | S | P1 |
| 22 | DM-001 | Design the `UserProfile` data model and persistence schema | Data model / PostgreSQL | INFRA-DB-001, COMP-005 | Schema includes `id`, `email`, `displayName`, `createdAt`, `updatedAt`, `lastLoginAt`, `roles`; email is unique/indexed; constraints match TDD | M | P0 |
| 23 | DM-002 | Design the `AuthToken` response model for API and client consumption | API contract / token model | COMP-002, COMP-003 | Model includes `accessToken`, `refreshToken`, `expiresIn`, `tokenType`; TTL semantics and Bearer contract are documented | S | P0 |
| 24 | API-001 | Define `POST /auth/login` contract, status codes, and rate-limit envelope | API layer | COMP-001, COMP-004, DM-002 | Request/response schema, 200/401/423/429 behaviors, and no-enumeration guarantee are documented and approved | M | P0 |
| 25 | API-002 | Define `POST /auth/register` contract and uniqueness/validation behavior | API layer | COMP-001, COMP-004, COMP-005, DM-001 | Request/response schema, 201/400/409 behavior, password policy handling, and returned profile fields are documented and approved | M | P0 |
| 26 | API-003 | Define `GET /auth/me` authenticated profile contract | API layer | COMP-001, COMP-003, DM-001 | Authorization requirements, 200/401 behavior, and complete profile field response contract are documented and approved | S | P1 |
| 27 | API-004 | Define `POST /auth/refresh` rotation and revocation contract | API layer | COMP-002, COMP-003, DM-002 | Refresh request/response schema, token rotation semantics, and 401 behavior for expired/revoked refresh tokens are documented and approved | M | P0 |
| 28 | API-005 | Define `POST /auth/reset-request` request semantics and anti-enumeration behavior | API layer | G-003, COMP-001 | API contract specifies generic success response, reset token generation trigger, and unregistered-email privacy behavior | M | P1 |
| 29 | API-006 | Define `POST /auth/reset-confirm` contract with one-hour TTL and single-use semantics | API layer | API-005, COMP-001, COMP-004 | API contract specifies token validation, password replacement, session invalidation dependency, and 400/401 behavior for invalid or expired tokens | M | P1 |

### Phase 1 Integration Points

1. **Named Artifact:** `auth_component_registry`
   - **Wired Components:** `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`
   - **Owning Phase:** Phase 1
   - **Cross-Reference:** Consumed in Phases 2, 3, 4, and 5 to assemble runtime flows and tests

2. **Named Artifact:** `auth_api_contract_map`
   - **Wired Components:** API-001 through API-006 mapped to backend handlers and frontend consumers
   - **Owning Phase:** Phase 1
   - **Cross-Reference:** Consumed in Phases 2 and 3 for implementation; Phase 4 for test coverage

3. **Named Artifact:** `frontend_auth_integration_contract`
   - **Wired Components:** `LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`
   - **Owning Phase:** Phase 1
   - **Cross-Reference:** Consumed in Phase 3 for frontend buildout and Phase 6 for PRD journey validation

---

### Phase 2 — Core Backend Authentication, Credential Handling, and Registration/Login Delivery

**Milestone alignment:** M1 core `AuthService`

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH-001 | Implement email/password login orchestration in `AuthService` | Backend / AuthService | COMP-001, COMP-004, COMP-005, API-001 | Valid credentials return 200 with `AuthToken`; invalid/non-existent email returns generic 401; failed-attempt tracking supports lockout rule | L | P0 |
| 2 | FR-AUTH-002 | Implement registration flow with validation and `UserProfile` creation | Backend / AuthService | COMP-001, COMP-004, COMP-005, DM-001, API-002 | Valid registration returns 201 with profile; duplicate email returns 409; weak passwords return 400; stored password uses bcrypt cost 12 | L | P0 |
| 3 | FR-AUTH.1 | Validate PRD login requirement against persistent-session architecture decisions | Product-to-tech traceability | FR-AUTH-001, API-001 | Login flow satisfies PRD expectation for successful authentication and session establishment with at least 15-minute access continuity | S | P1 |
| 4 | FR-AUTH.2 | Validate PRD registration requirement against account creation workflow | Product-to-tech traceability | FR-AUTH-002, API-002 | Registration workflow supports unique email, valid password, display name, and post-registration session start path per PRD intent | S | P1 |
| 5 | NFR-SEC-001 | Implement bcrypt hashing with cost factor 12 inside `PasswordHasher` | Security / password handling | COMP-004 | Hash and verify paths use bcrypt cost 12; raw passwords are never persisted or logged | M | P0 |
| 6 | NFR-AUTH.3 | Validate one-way password storage and no-plaintext logging across the registration/login path | Security compliance | NFR-SEC-001, FR-AUTH-001, FR-AUTH-002 | Credential handling path demonstrates one-way hashing, redacted logs, and no plaintext persistence in storage or telemetry | M | P0 |
| 7 | API-001 | Implement login handler and response mapping for `POST /auth/login` | Backend / HTTP handlers | FR-AUTH-001 | Handler accepts email/password payload, emits consistent error format, enforces status mapping, and delegates business logic to `AuthService` | M | P0 |
| 8 | API-002 | Implement registration handler and response mapping for `POST /auth/register` | Backend / HTTP handlers | FR-AUTH-002 | Handler accepts registration payload, returns created profile shape, and maps validation/conflict failures to documented responses | M | P0 |
| 9 | DM-001 | Implement `UserProfile` table, indexes, and repository mappings | Persistence / PostgreSQL | INFRA-DB-001, COMP-005 | PostgreSQL schema enforces UUID primary key, unique normalized email, timestamps, nullable `lastLoginAt`, and default `roles` | M | P0 |
| 10 | TEST-001 | Create unit tests for successful login token issuance orchestration | Unit tests / AuthService | FR-AUTH-001, API-001 | Test proves `AuthService.login()` verifies password, updates state as needed, and requests token issuance on valid credentials | S | P0 |
| 11 | TEST-002 | Create unit tests for invalid credential handling and generic unauthorized errors | Unit tests / AuthService | FR-AUTH-001, API-001 | Test proves wrong password and unknown email return generic 401 behavior without user enumeration leakage | S | P0 |
| 12 | TEST-004 | Create integration test for registration persistence through API, hasher, and PostgreSQL | Integration tests | FR-AUTH-002, API-002, DM-001 | End-to-end registration test persists user record, enforces unique email behavior, and verifies stored hash characteristics | M | P0 |
| 13 | AUTH-E1 | Deliver the login and registration epic as the first implementation increment | Epic delivery | FR-AUTH-001, FR-AUTH-002, API-001, API-002, TEST-001, TEST-002, TEST-004 | Login and registration flows are functionally complete, test-backed, and aligned to PRD epic scope | M | P0 |
| 14 | R-002 | Implement brute-force mitigation controls at the login boundary | Security / abuse prevention | FR-AUTH-001, API-001 | Account locks after 5 failed attempts in 15 minutes; login endpoint cooperates with gateway rate limiting; mitigation is observable | M | P0 |
| 15 | COMPLIANCE-001 | Define audit-log field requirements for auth events needed for SOC2 readiness | Compliance / audit logging design | AUTH-PRD-001, NFR-AUTH.2 | Required fields include user ID when known, timestamp, IP, event type, and outcome; retention and query needs are documented | M | P1 |
| 16 | SEC-POLICY-001 | Reconcile implementation-level password and token decisions with security policy constraints | Security governance | NFR-SEC-001, COMP-003, COMP-004 | Bcrypt and token strategy are verified against policy; no policy contradiction remains unresolved before wider implementation | S | P0 |
| 17 | OQ-002 | Bound the `roles` array contract without introducing RBAC enforcement | Data contract governance | DM-001, NG-003 | A documented maximum or deferred decision exists for `roles` cardinality; storage and response contract remain stable | S | P2 |
| 18 | M1 | Achieve the M1 deliverable for core `AuthService`, password hashing, schema, and register/login endpoints | Milestone governance | FR-AUTH-001, FR-AUTH-002, NFR-SEC-001, DM-001, API-001, API-002, AUTH-E1 | M1 exit criteria are met: login/register core works, unit/integration tests pass, and foundational architecture is stable for token work | M | P0 |
| 19 | RISK-PRD-001 | Mitigate low registration adoption risk through low-friction registration architecture | UX-informed architecture | FR-AUTH-002, AUTH-E1 | Registration collects only in-scope fields, supports inline validation, and avoids unnecessary friction inconsistent with PRD conversion goals | S | P1 |
| 20 | JTBD-001 | Support first-time user account creation as the primary onboarding job to be done | User job validation | FR-AUTH-002, AUTH-E1 | Registration architecture and UX contract support quick account creation without unnecessary prerequisites | S | P1 |
| 21 | PERSONA-001 | Design registration/login flows around Alex the End User’s low-friction needs | Persona-driven sequencing | FR-AUTH-001, FR-AUTH-002 | Core flows optimize for fast signup, simple login, and seamless transition into authenticated use | S | P1 |
| 22 | STORY-001 | Implement the PRD story for self-service account creation with duplicate-email handling | User story validation | FR-AUTH-002, API-002 | Registration behavior matches story acceptance criteria, including helpful duplicate handling and successful account creation path | S | P1 |
| 23 | STORY-002 | Implement the PRD story for generic-error login without user enumeration | User story validation | FR-AUTH-001, API-001 | Incorrect credentials surface a generic error and do not disclose account existence | S | P1 |
| 24 | ERROR-001 | Handle duplicate-email registration race conditions safely | Backend validation / persistence | FR-AUTH-002, DM-001 | Concurrent duplicate registrations resolve via unique constraint and return deterministic conflict response without inconsistent state | S | P1 |
| 25 | ERROR-002 | Handle wrong-password attempts below lock threshold with generic feedback | Backend error handling | FR-AUTH-001, API-001 | Fewer than 5 failed attempts return generic invalid-credentials errors and increment failure counters correctly | S | P1 |
| 26 | ERROR-003 | Handle wrong-password lockout threshold and notify downstream observability hooks | Backend security handling | FR-AUTH-001, R-002 | Fifth failed attempt triggers locked-state response and emits auditable lockout event metadata | M | P0 |
| 27 | LEG-001 | Incorporate GDPR consent capture requirement into registration contract | Compliance / registration flow | FR-AUTH-002, API-002 | Registration architecture includes consent capture point and timestamp persistence requirement before production readiness | M | P1 |
| 28 | JOURNEY-001 | Validate first-time signup journey against architecture and API sequencing | Journey validation | FR-AUTH-002, API-002, STORY-001 | Journey supports CTA -> form -> validation -> account creation -> session start/redirect path consistent with PRD | S | P1 |

### Phase 2 Integration Points

1. **Named Artifact:** `auth_service_dependency_graph`
   - **Wired Components:** `AuthService` -> `PasswordHasher`, `UserRepo`, login/register handlers
   - **Owning Phase:** Phase 2
   - **Cross-Reference:** Consumed in Phase 4 tests and Phase 5 operational diagnostics

2. **Named Artifact:** `login_abuse_control_chain`
   - **Wired Components:** API Gateway rate limiting, failed-attempt counter, account lockout logic, audit event emitter
   - **Owning Phase:** Phase 2
   - **Cross-Reference:** Consumed in Phase 5 monitoring/alerts and Phase 6 compliance validation

3. **Named Artifact:** `registration_contract_binding`
   - **Wired Components:** `RegisterPage`, `POST /auth/register`, `AuthService`, `PasswordHasher`, `UserRepo`
   - **Owning Phase:** Phase 2
   - **Cross-Reference:** Consumed in Phase 3 frontend implementation and Phase 6 signup-journey validation

---

### Phase 3 — Token Lifecycle, Profile Retrieval, Password Reset, and Frontend Session Integration

**Milestone alignment:** M2, M3, M4

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | FR-AUTH-003 | Implement JWT issuance, refresh rotation, and revocation through `TokenManager` and `JwtService` | Backend / token lifecycle | COMP-002, COMP-003, API-004, DM-002 | Login and refresh return access/refresh token pairs; refresh rotation revokes old tokens; expired/revoked tokens return 401 | L | P0 |
| 2 | FR-AUTH-004 | Implement authenticated profile retrieval via `/auth/me` | Backend / profile access | COMP-001, COMP-003, API-003, DM-001 | Valid access token returns complete `UserProfile`; expired/invalid token returns 401 | M | P0 |
| 3 | FR-AUTH-005 | Implement two-step password reset with token expiry, single-use semantics, and password update | Backend / recovery flow | API-005, API-006, COMP-001, COMP-004 | Reset request triggers email flow; valid token updates password; token expires in 1 hour; used tokens cannot be reused | L | P0 |
| 4 | FR-AUTH.3 | Validate PRD session persistence requirement against refresh-token implementation | Product-to-tech traceability | FR-AUTH-003, API-004 | Active sessions can continue across refreshes/page reloads inside the 7-day refresh window; session expiration behavior is explicit | S | P1 |
| 5 | FR-AUTH.4 | Validate PRD profile-view requirement against authenticated profile endpoint and UI contract | Product-to-tech traceability | FR-AUTH-004, API-003, COMP-009 | Logged-in users can access account details through the designed profile integration path | S | P1 |
| 6 | FR-AUTH.5 | Validate PRD self-service password reset requirement including session invalidation | Product-to-tech traceability | FR-AUTH-005, API-005, API-006 | Password reset flow is email-driven, time-limited, self-service, and invalidates existing sessions after successful password change | M | P1 |
| 7 | NFR-SEC-002 | Implement RS256 token signing with 2048-bit RSA keys and verification path | Security / token signing | COMP-003, FR-AUTH-003 | Tokens are signed/verified with RS256 using 2048-bit keys; configuration validation and rotation dependency are documented | M | P0 |
| 8 | NFR-PERF-001 | Design token and profile flows to meet sub-200ms p95 response budget | Performance engineering | FR-AUTH-003, FR-AUTH-004, COMP-002, COMP-003 | Path analysis and implementation choices keep critical endpoint latency within target under expected load | M | P0 |
| 9 | NFR-PERF-002 | Design login and token infrastructure to sustain 500 concurrent authentication requests | Scalability engineering | FR-AUTH-001, FR-AUTH-003, INFRA-DB-001 | Connection pooling, Redis usage, and stateless token verification support target concurrency without architectural bottlenecks | M | P1 |
| 10 | NFR-REL-001 | Architect auth service availability for 99.9% uptime over rolling 30-day windows | Reliability engineering | FR-AUTH-003, FR-AUTH-004, INFRA-DB-001 | Redundancy assumptions, health-check strategy, failure isolation, and rollout gates support stated uptime target | M | P1 |
| 11 | NFR-AUTH.1 | Validate combined p95 and concurrency PRD target against endpoint design and testing strategy | Product NFR validation | NFR-PERF-001, NFR-PERF-002 | Auth request path and planned tests explicitly cover both latency and concurrency targets from PRD | S | P1 |
| 12 | NFR-AUTH.2 | Validate service availability target against operational design and rollout safeguards | Product NFR validation | NFR-REL-001 | Reliability design, health checks, and rollout/rollback criteria support 99.9% availability commitment | S | P1 |
| 13 | API-003 | Implement authenticated `GET /auth/me` handler and authorization middleware integration | Backend / HTTP handlers | FR-AUTH-004, NFR-SEC-002 | Handler requires Bearer token, validates token via `JwtService`, and returns documented profile response | M | P0 |
| 14 | API-004 | Implement `POST /auth/refresh` handler with rotation and revoked-token rejection | Backend / HTTP handlers | FR-AUTH-003, NFR-SEC-002 | Handler exchanges valid refresh token for new pair, revokes old token, and rejects expired/revoked tokens | M | P0 |
| 15 | API-005 | Implement `POST /auth/reset-request` handler and email dispatch initiation | Backend / HTTP handlers | FR-AUTH-005, COMP-001 | Handler accepts email, emits generic success response, and creates reset dispatch workflow without account enumeration | M | P1 |
| 16 | API-006 | Implement `POST /auth/reset-confirm` handler and password replacement flow | Backend / HTTP handlers | FR-AUTH-005, API-005, NFR-SEC-001 | Handler validates reset token, updates password hash, invalidates sessions, and rejects invalid/expired/reused tokens | M | P1 |
| 17 | DM-002 | Implement `AuthToken` response assembly and serialization for login/refresh consumers | Token model / API | FR-AUTH-003, API-001, API-004 | Login and refresh responses consistently emit `accessToken`, `refreshToken`, `expiresIn=900`, and `tokenType=Bearer` | S | P0 |
| 18 | COMP-002 | Implement `TokenManager` runtime logic for issuance, storage, rotation, and revocation | Backend / TokenManager | FR-AUTH-003, API-004, DM-002 | Refresh tokens are stored in Redis, rotation is atomic, revocation is enforced, and degraded-Redis behavior is explicit | L | P0 |
| 19 | COMP-003 | Implement `JwtService` runtime logic for signing, verification, expiry, and skew tolerance | Backend / JwtService | NFR-SEC-002, API-003, API-004 | Service signs valid access tokens, verifies Bearer tokens, honors 15-minute expiry, and allows 5-second skew tolerance | M | P0 |
| 20 | COMP-006 | Implement `LoginPage` UI flow against login API and success redirect behavior | Frontend / LoginPage | API-001, FR-AUTH-001, COMP-008 | Page submits email/password, handles generic failures, and redirects on successful login | M | P1 |
| 21 | COMP-007 | Implement `RegisterPage` UI flow with inline validation and registration integration | Frontend / RegisterPage | API-002, FR-AUTH-002, LEG-001 | Page validates required fields, shows unmet password requirements, handles duplicate email, and starts/continues session flow | M | P1 |
| 22 | COMP-008 | Implement `AuthProvider` token storage, silent refresh, and 401 interception logic | Frontend / AuthProvider | API-004, FR-AUTH-003, FR-AUTH-004 | Provider stores access token in memory, coordinates refresh flow, handles expired sessions, and exposes auth state/profile to children | L | P0 |
| 23 | COMP-009 | Implement `ProfilePage` authenticated profile rendering | Frontend / ProfilePage | API-003, FR-AUTH-004, COMP-008 | Page renders display name, email, and account creation details for authenticated users and redirects otherwise | M | P1 |
| 24 | AUTH-E2 | Deliver the token management epic including silent session continuity | Epic delivery | FR-AUTH-003, API-004, COMP-002, COMP-003, COMP-008 | Token issuance, refresh, rotation, and client-side continuity are functionally complete and traceable to PRD epic intent | M | P0 |
| 25 | AUTH-E3 | Deliver the profile and password reset epic | Epic delivery | FR-AUTH-004, FR-AUTH-005, API-003, API-005, API-006, COMP-009 | Profile retrieval and self-service password reset are functionally complete and aligned to PRD epic scope | M | P0 |
| 26 | TEST-003 | Create unit tests for `TokenManager.refresh()` validation, rotation, and re-issuance | Unit tests / TokenManager | FR-AUTH-003, COMP-002 | Unit tests prove valid refresh succeeds, old token is revoked, and invalid/expired/revoked tokens fail cleanly | S | P0 |
| 27 | TEST-005 | Create integration tests for expired refresh-token rejection and Redis TTL behavior | Integration tests | FR-AUTH-003, API-004, COMP-002 | Integration tests verify Redis-backed TTL expiry and rejected refresh behavior under expired token conditions | M | P0 |
| 28 | TEST-006 | Create E2E test for register -> login -> profile journey with `AuthProvider` refresh support | E2E tests | COMP-006, COMP-007, COMP-008, COMP-009 | End-to-end flow covers registration/login/profile and validates background refresh behavior from client perspective | L | P1 |
| 29 | AUTH_TOKEN_REFRESH | Implement and wire the `AUTH_TOKEN_REFRESH` feature flag for controlled refresh rollout | Rollout controls | FR-AUTH-003, COMP-002, COMP-008 | Refresh flow can be enabled/disabled cleanly; OFF state yields access-token-only behavior as specified | M | P1 |
| 30 | FE-AUTH-001-TDD | Validate backend contracts against the frontend auth accessibility/design dependency | Cross-team interface | COMP-006, COMP-007, COMP-008, COMP-009 | Backend API and error semantics are documented for frontend team consumption without contradicting frontend TDD ownership | S | P2 |
| 31 | OQ-001 | Resolve or explicitly defer API key authentication for service-to-service use | Scope governance | AUTH-001-TDD, NG-001, NG-002, NG-003 | A documented decision exists that API-key auth is deferred beyond v1.0 and does not disturb user-auth architecture | S | P2 |
| 32 | M2 | Achieve token management milestone readiness | Milestone governance | FR-AUTH-003, FR-AUTH-004, API-003, API-004, COMP-002, COMP-003 | M2 exit criteria are met: token lifecycle and `/auth/me` are implemented and validated | M | P0 |
| 33 | M3 | Achieve password reset milestone readiness | Milestone governance | FR-AUTH-005, API-005, API-006, AUTH-E3 | M3 exit criteria are met: password reset request/confirm path works with email dependency and token controls | M | P0 |
| 34 | M4 | Achieve frontend integration milestone readiness | Milestone governance | COMP-006, COMP-007, COMP-008, COMP-009, TEST-006 | M4 exit criteria are met: frontend consumers are integrated against backend contracts and E2E coverage exists | M | P1 |
| 35 | PERSONA-003 | Support Sam the API Consumer with clear auth and refresh contracts | Persona-driven validation | FR-AUTH-003, API-004 | API auth contract is stable, programmatic, and returns clear failure semantics needed for integrations | S | P1 |
| 36 | STORY-004 | Implement the PRD story for session persistence across page refreshes | User story validation | FR-AUTH-003, COMP-008 | Active sessions remain usable across page loads inside refresh window without unnecessary re-login prompts | S | P1 |
| 37 | STORY-005 | Implement the PRD story for programmatic token refresh | User story validation | API-004, FR-AUTH-003 | Valid refresh token can be exchanged programmatically; expired token behavior returns clear error contract | S | P1 |
| 38 | STORY-006 | Implement the PRD story for profile viewing | User story validation | FR-AUTH-004, COMP-009 | Profile view shows expected account fields for authenticated users | S | P1 |
| 39 | STORY-007 | Implement the PRD story for self-service password reset | User story validation | FR-AUTH-005, API-005, API-006 | Reset email is initiated, link expires after 1 hour, and new password invalidates existing sessions | M | P1 |
| 40 | JOURNEY-002 | Validate returning-user login journey with silent refresh continuity | Journey validation | FR-AUTH-001, FR-AUTH-003, COMP-008 | Journey supports login, navigation across page loads, background refresh, and clear session-expired re-login prompt after inactivity | M | P1 |
| 41 | JOURNEY-003 | Validate password reset journey from request through relogin | Journey validation | FR-AUTH-005, API-005, API-006 | Journey supports request form, generic confirmation, reset link, password update, session invalidation, and redirect to login | M | P1 |
| 42 | JOURNEY-004 | Validate authenticated profile-management journey | Journey validation | FR-AUTH-004, COMP-009 | Authenticated user can navigate to profile and view current account details without breaking session state | S | P2 |
| 43 | ERROR-004 | Handle reset request for unregistered email without enumeration | Backend error handling | API-005, FR-AUTH-005 | Unregistered email returns same success response as registered email and does not leak account existence | S | P1 |
| 44 | ERROR-005 | Handle expired reset-link submissions with recovery guidance | Backend error handling | API-006, FR-AUTH-005 | Expired token produces clear invalid/expired response and supports requesting a new reset flow | S | P1 |
| 45 | ERROR-006 | Preserve multi-device session support while enforcing token validity | Session management | FR-AUTH-003, COMP-002 | Concurrent login across devices remains supported unless explicitly invalidated by password reset/security action | M | P1 |
| 46 | ERROR-007 | Handle token expiry during active usage via silent refresh fallback or re-authentication | Frontend session resilience | COMP-008, FR-AUTH-003 | Silent refresh occurs when possible; otherwise session-expired path is clear and does not corrupt client state | M | P1 |
| 47 | ERROR-008 | Enforce password policy feedback before registration submission | Frontend validation | COMP-007, FR-AUTH-002 | Inline validation communicates unmet password requirements before request submission | S | P2 |
| 48 | JTBD-002 | Support returning-user login and resume workflow | User job validation | FR-AUTH-001, FR-AUTH-003 | Auth architecture allows users to log in and continue use without repeatedly re-entering preferences during active session window | S | P1 |
| 49 | JTBD-003 | Support self-service password recovery without support intervention | User job validation | FR-AUTH-005, API-005, API-006 | Users can regain access through reset flow without manual assistance in normal cases | S | P1 |
| 50 | JTBD-004 | Support programmatic integration authentication and refresh | User job validation | FR-AUTH-003, API-004 | Integration users can authenticate and refresh tokens without interactive user flows | S | P1 |

### Phase 3 Integration Points

1. **Named Artifact:** `token_lifecycle_registry`
   - **Wired Components:** `AuthService`, `TokenManager`, `JwtService`, Redis token store, `AUTH_TOKEN_REFRESH`
   - **Owning Phase:** Phase 3
   - **Cross-Reference:** Consumed in Phase 4 performance/security tests and Phase 5 rollout controls

2. **Named Artifact:** `frontend_session_binding`
   - **Wired Components:** `LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`, API-001/002/003/004
   - **Owning Phase:** Phase 3
   - **Cross-Reference:** Consumed in Phase 4 E2E validation and Phase 6 customer-journey traceability

3. **Named Artifact:** `password_reset_workflow_map`
   - **Wired Components:** `POST /auth/reset-request`, email service, reset token store/validator, `POST /auth/reset-confirm`, session invalidation path
   - **Owning Phase:** Phase 3
   - **Cross-Reference:** Consumed in Phase 5 operational readiness and Phase 6 compliance/risk validation

---

### Phase 4 — Observability, Security Hardening, Performance, Reliability, and Test Expansion

**Milestone alignment:** hardening before GA

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | OPS-001 | Implement `auth_login_total` metric emission | Observability / metrics | FR-AUTH-001, COMPLIANCE-001 | Counter records login attempts/outcomes in a way suitable for dashboards and alerting | S | P1 |
| 2 | OPS-002 | Implement `auth_login_duration_seconds` histogram emission | Observability / metrics | FR-AUTH-001, NFR-PERF-001 | Histogram captures login latency suitable for p95 tracking and alert thresholds | S | P1 |
| 3 | OPS-003 | Implement `auth_token_refresh_total` metric emission | Observability / metrics | FR-AUTH-003, API-004 | Counter captures refresh success/failure volumes for runtime visibility | S | P1 |
| 4 | OPS-004 | Implement `auth_registration_total` metric emission | Observability / metrics | FR-AUTH-002, API-002 | Counter captures registration attempts and outcomes for funnel and failure analysis | S | P1 |
| 5 | OPS-005 | Implement structured logging for login success, login failure, registration, refresh, and reset events | Observability / logging | FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-005, COMPLIANCE-001 | Structured logs include event type, timestamp, outcome, correlation fields, and sensitive-field redaction | M | P0 |
| 6 | OPS-006 | Implement distributed tracing across `AuthService`, `PasswordHasher`, `TokenManager`, and `JwtService` | Observability / tracing | COMP-001, COMP-002, COMP-003, COMP-004 | Request traces span core auth components and allow latency attribution across service boundaries | M | P1 |
| 7 | OPS-007 | Configure alert for login failure rate above 20% over 5 minutes | Operations / alerting | OPS-001, OPS-005, R-002 | Alert fires on sustained abnormal failure rate and links to runbook/diagnostic context | S | P1 |
| 8 | OPS-008 | Configure alert for p95 latency above 500ms | Operations / alerting | OPS-002, NFR-PERF-001 | Alert fires when latency exceeds hardening threshold and supports response before SLA breach | S | P1 |
| 9 | OPS-009 | Configure alert for `TokenManager` Redis connection failures | Operations / alerting | COMP-002, OPS-003 | Alert fires on Redis connection degradation affecting refresh path | S | P0 |
| 10 | OPS-010 | Define auth service capacity target for pod scaling from 3 to 10 replicas | Capacity planning / compute | NFR-REL-001, NFR-PERF-002 | Scaling target and trigger assumptions are documented and validated against expected auth load | M | P1 |
| 11 | OPS-011 | Validate PostgreSQL connection-pool scaling assumptions for auth workload | Capacity planning / database | INFRA-DB-001, NFR-PERF-002 | Pool sizing and expansion thresholds are documented and tested against expected concurrent query patterns | M | P1 |
| 12 | OPS-012 | Validate Redis memory and token-retention capacity assumptions | Capacity planning / cache | COMP-002, FR-AUTH-003 | Redis memory usage projections support expected token volume and scaling threshold decisions | M | P1 |
| 13 | R-001 | Implement token-theft mitigation posture across frontend storage and refresh handling | Security hardening | COMP-008, AUTH_TOKEN_REFRESH, FR-AUTH-003 | Access token stays in memory, refresh handling minimizes theft exposure, and incident revocation path is defined | M | P0 |
| 14 | R-003 | Implement migration/data-protection safeguards for legacy coexistence and recovery | Migration safety | DM-001, AUTH_NEW_LOGIN | Backup, idempotent migration assumptions, and rollback data-protection controls are defined before rollout | M | P0 |
| 15 | RISK-PRD-002 | Schedule dedicated security review and penetration validation before production | Security assurance | FR-AUTH-001, FR-AUTH-003, FR-AUTH-005, SEC-POLICY-001 | Security review scope covers auth flows, token handling, reset workflow, and client storage assumptions before GA | M | P0 |
| 16 | RISK-PRD-003 | Validate audit logging completeness against compliance controls before rollout | Compliance assurance | COMPLIANCE-001, OPS-005 | Audit logging is reviewed against SOC2-oriented requirements and no critical field gaps remain | M | P0 |
| 17 | RISK-PRD-004 | Implement email-delivery monitoring and fallback support guidance for reset flow | Operations / email dependency | API-005, FR-AUTH-005 | Password reset email delivery is observable; operational fallback guidance exists if delivery fails | M | P1 |
| 18 | TEST-001 | Expand login unit tests to cover lockout, timestamp updates, and boundary conditions | Unit tests / AuthService | TEST-001, R-002 | Unit coverage includes lockout threshold, `lastLoginAt` update, and generic failure semantics | M | P1 |
| 19 | TEST-002 | Expand invalid-credential tests to cover no-enumeration and edge timing paths | Unit tests / AuthService | TEST-002 | Tests verify consistent unauthorized output and no branching that leaks account existence | S | P1 |
| 20 | TEST-003 | Expand token unit tests to cover rotation failure and revoked-token behavior | Unit tests / TokenManager | TEST-003, COMP-002 | Unit coverage includes revoked token, double-use rejection, and Redis-degraded decision paths | M | P1 |
| 21 | TEST-004 | Expand registration integration coverage for duplicate email, consent capture, and role defaults | Integration tests | TEST-004, LEG-001, DM-001 | Integration tests prove duplicate conflict handling, consent persistence expectations, and default roles behavior | M | P1 |
| 22 | TEST-005 | Expand refresh integration coverage for expiry, revocation, and key-validation failures | Integration tests | TEST-005, NFR-SEC-002 | Integration tests cover refresh expiry, revoked token, and token-signature validation outcomes | M | P1 |
| 23 | TEST-006 | Expand E2E coverage for password reset and expired-session recovery | E2E tests | TEST-006, FR-AUTH-005, ERROR-007 | E2E tests cover password reset, session expiration, silent refresh fallback, and forced relogin behavior | L | P1 |
| 24 | PERSONA-002 | Support Jordan the Platform Admin with auth visibility and incident response hooks | Persona-driven operations | OPS-001, OPS-005, OPS-007, OPS-009 | Admin-relevant telemetry enables investigation of failed logins, lockouts, and auth incidents | S | P1 |
| 25 | STORY-008 | Implement the PRD story for queryable authentication event logs | User story validation / admin operations | COMPLIANCE-001, OPS-005 | Auth logs contain user ID when known, event type, timestamp, IP, and outcome and are queryable by relevant dimensions | M | P1 |
| 26 | LEG-002 | Implement SOC2 Type II audit log retention and event completeness design | Compliance / audit logging | COMPLIANCE-001, OPS-005 | Auth events include required fields and retention strategy supports 12-month compliance need | M | P0 |
| 27 | LEG-003 | Verify password-storage design against NIST SP 800-63B constraints | Compliance / password policy | NFR-SEC-001, NFR-AUTH.3, SEC-POLICY-001 | Password storage and handling align with one-way adaptive hashing expectations and avoid prohibited raw-password storage | S | P0 |
| 28 | LEG-004 | Enforce data minimization in auth data collection and storage | Compliance / privacy | FR-AUTH-002, DM-001 | Collected fields remain limited to email, hashed password, display name, consent metadata, and required timestamps | S | P1 |
| 29 | ALT-001 | Reconfirm rejection of the do-nothing option with measurable delivery checkpoints | Architecture governance | AUTH-PRD-001 | Roadmap remains anchored to delivering identity capability rather than deferring security and personalization prerequisites | S | P2 |
| 30 | ALT-002 | Reconfirm rejection of third-party auth provider for v1.0 | Architecture governance | AUTH-001-TDD, AUTH-PRD-001 | No roadmap item substitutes managed auth SaaS for self-hosted `AuthService`; rationale remains documented | S | P2 |
| 31 | ALT-003 | Reconfirm rejection of session-cookie architecture for horizontally scalable v1.0 | Architecture governance | G-002, COMP-002, COMP-003 | JWT + refresh design remains the approved architecture; no server-side session store is introduced for primary auth | S | P2 |
| 32 | SUCCESS-001 | Validate login p95 target with instrumentation and pre-GA performance evidence | Success metric validation | NFR-PERF-001, OPS-002 | Measured pre-GA evidence shows login path p95 below 200ms or issues are documented with remediation before rollout | M | P0 |
| 33 | SUCCESS-002 | Validate registration conversion instrumentation path | Success metric validation | OPS-004, JOURNEY-001 | Funnel instrumentation exists from registration start to account confirmation/success path | S | P1 |
| 34 | SUCCESS-003 | Validate average session duration measurement path | Success metric validation | OPS-003, FR-AUTH-003 | Refresh/session analytics enable measurement of average session duration target | S | P1 |
| 35 | SUCCESS-004 | Validate failed-login rate measurement path | Success metric validation | OPS-001, OPS-005, R-002 | Telemetry supports measuring failed login rate as a share of attempts | S | P1 |
| 36 | SUCCESS-005 | Validate password-reset completion funnel instrumentation | Success metric validation | API-005, API-006, OPS-005 | Funnel captures reset requested -> email delivered -> reset confirmed outcomes for completion tracking | M | P1 |

### Phase 4 Integration Points

1. **Named Artifact:** `auth_observability_pipeline`
   - **Wired Components:** metrics emitters, structured logger, tracing spans, alert rules
   - **Owning Phase:** Phase 4
   - **Cross-Reference:** Consumed in Phase 5 runbooks/rollout and Phase 6 success-metric validation

2. **Named Artifact:** `security_control_matrix`
   - **Wired Components:** bcrypt policy, RS256 keys, token storage strategy, lockout controls, privacy/logging controls
   - **Owning Phase:** Phase 4
   - **Cross-Reference:** Consumed in Phase 5 release criteria and Phase 6 compliance traceability

3. **Named Artifact:** `auth_test_coverage_matrix`
   - **Wired Components:** TEST-001..006 mapped to FR/NFR/API/component coverage
   - **Owning Phase:** Phase 4
   - **Cross-Reference:** Consumed in Phase 5 go/no-go gates and Phase 6 PRD/TDD traceability

---

### Phase 5 — Migration, Rollout, Operational Readiness, and Release Governance

**Milestone alignment:** M5 GA release

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | MIG-001 | Execute Phase 1 internal alpha rollout plan in staging | Release / rollout | M4, OPS-005, TEST-006 | Staging deployment exposes auth flows behind feature control; auth-team and QA can exercise all core FRs with zero unresolved P0/P1 defects | M | P0 |
| 2 | MIG-002 | Execute Phase 2 beta rollout plan for 10% traffic exposure | Release / rollout | MIG-001, AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH, OPS-001, OPS-008, OPS-009 | 10% traffic rollout is gated, observable, and meets latency/error/Redis stability expectations before expansion | M | P0 |
| 3 | MIG-003 | Execute Phase 3 general-availability rollout to 100% traffic | Release / rollout | MIG-002, NFR-REL-001, SUCCESS-001 | Full traffic cutover occurs only after beta gates pass and production monitoring is green | M | P0 |
| 4 | MIG-004 | Implement and validate `AUTH_NEW_LOGIN` feature flag control for new login path | Release controls | API-001, COMP-006, MIG-001 | Flag cleanly gates new login UI/backend path and supports rollback to legacy auth routing | M | P0 |
| 5 | MIG-005 | Validate staged removal criteria for `AUTH_NEW_LOGIN` after GA stability | Release controls | MIG-003, MIG-004 | Removal criteria are documented and include post-GA stability period and rollback confidence | S | P1 |
| 6 | MIG-006 | Validate staged removal criteria for `AUTH_TOKEN_REFRESH` after GA + stabilization | Release controls | MIG-003, AUTH_TOKEN_REFRESH | Removal criteria are documented and include refresh-path stability evidence | S | P1 |
| 7 | MIG-007 | Implement rollback procedure to disable new auth path and restore legacy routing | Rollback readiness | MIG-004, MIG-001 | Rollback can disable new login path rapidly, verify legacy flow, and initiate incident response workflow | M | P0 |
| 8 | MIG-008 | Define and validate latency-triggered rollback criterion | Rollback criteria | OPS-008, MIG-007 | Rollback threshold of p95 > 1000ms for 5 minutes is encoded in operational decision logic and tested in staging drills | S | P1 |
| 9 | MIG-009 | Define and validate error-rate-triggered rollback criterion | Rollback criteria | OPS-005, MIG-007 | Rollback threshold of >5% error rate for 2 minutes is operationally measurable and tested in staging drills | S | P1 |
| 10 | MIG-010 | Define and validate Redis-failure and data-corruption rollback criteria | Rollback criteria | OPS-009, R-003, MIG-007 | Redis failure frequency and any data-loss/corruption signal are treated as immediate rollback triggers with documented response path | S | P0 |
| 11 | AUTH_NEW_LOGIN | Activate controlled rollout path for new login and registration experience | Release controls | MIG-004, COMP-006, COMP-007 | Feature flag is operationally manageable per environment and used during staged rollout | S | P0 |
| 12 | OPS-013 | Publish runbook for `AuthService` full outage diagnosis and recovery | Operations / runbook | OPS-005, OPS-006, MIG-001 | Runbook covers symptoms, diagnosis, PostgreSQL checks, pod recovery, and escalation path | M | P0 |
| 13 | OPS-014 | Publish runbook for token-refresh failure diagnosis and recovery | Operations / runbook | OPS-009, COMP-002, AUTH_TOKEN_REFRESH | Runbook covers Redis connectivity, signing-key availability, feature-flag checks, and escalation path | M | P0 |
| 14 | OPS-015 | Formalize first-two-weeks post-GA 24/7 on-call expectations for auth-team | Operations / staffing | MIG-003, OPS-013, OPS-014 | On-call coverage, response expectations, tooling access, and escalation chain are documented and acknowledged | S | P1 |
| 15 | OPS-016 | Validate HPA and deployment topology for `AuthService` production capacity | Operations / compute readiness | OPS-010, MIG-002 | Production deployment configuration supports planned scaling thresholds and replica growth behavior | M | P1 |
| 16 | OPS-017 | Validate PostgreSQL operational tooling and admin access for auth incidents | Operations / database readiness | OPS-011, OPS-013 | Required admin access and dashboards exist for diagnosing auth persistence incidents | S | P1 |
| 17 | OPS-018 | Validate Redis operational tooling and admin access for refresh incidents | Operations / cache readiness | OPS-012, OPS-014 | Required operational access exists for diagnosing token-store degradation during rollout | S | P1 |
| 18 | M5 | Achieve GA release milestone with production rollout, observability, and rollback readiness | Milestone governance | MIG-001, MIG-002, MIG-003, OPS-013, OPS-014 | M5 exit criteria are met: staged rollout completed, feature controls managed, monitoring green, rollback tested, and operational ownership established | M | P0 |
| 19 | RELEASE-001 | Validate definition-of-done coverage for all FR-AUTH-001 through FR-AUTH-005 | Release governance | FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004, FR-AUTH-005, TEST-001, TEST-002, TEST-003, TEST-004, TEST-005, TEST-006 | All TDD functional requirements are implemented and backed by passing tests and acceptance evidence | M | P0 |
| 20 | RELEASE-002 | Validate unit coverage target above 80% for auth core components | Release governance | TEST-001, TEST-002, TEST-003 | Coverage report shows auth core components exceed 80% unit coverage target or release is blocked pending remediation | M | P1 |
| 21 | RELEASE-003 | Validate integration coverage against real PostgreSQL and Redis instances | Release governance | TEST-004, TEST-005 | Integration evidence demonstrates endpoint and token-store behavior against real backing services | M | P0 |
| 22 | RELEASE-004 | Validate security review completion for hashing, keys, and session controls | Release governance | RISK-PRD-002, LEG-003, NFR-SEC-002 | Security review is completed with no unresolved critical findings blocking GA | M | P0 |
| 23 | RELEASE-005 | Validate performance testing against <200ms p95 and 500 concurrent users | Release governance | SUCCESS-001, NFR-PERF-002, NFR-AUTH.1 | Pre-release performance evidence demonstrates target attainment or blocks expansion beyond staged rollout | M | P0 |
| 24 | RELEASE-006 | Validate staging smoke tests for backend and frontend auth paths | Release governance | MIG-001, COMP-006, COMP-007, COMP-008, COMP-009 | Staging smoke suite confirms login, registration, refresh, profile, and reset behaviors before production expansion | M | P0 |
| 25 | RELEASE-007 | Validate production feature-flag configuration for both auth rollout controls | Release governance | AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH | Production environment has correct default values, rollback procedures, and owner accountability for both flags | S | P0 |
| 26 | RELEASE-008 | Validate monitoring dashboards and alert routing before GA cutover | Release governance | OPS-001, OPS-002, OPS-003, OPS-004, OPS-007, OPS-008, OPS-009 | Dashboards and alert routes are live, readable, and linked to runbooks before 100% rollout | M | P0 |
| 27 | RELEASE-009 | Validate rollback drill execution in staging | Release governance | MIG-007, MIG-008, MIG-009, MIG-010 | Staging rollback drill succeeds and demonstrates timing, control ownership, and recovery confidence | M | P0 |
| 28 | RELEASE-010 | Validate data migration script and production-like dataset behavior | Release governance | R-003, MIG-001 | Migration/reconciliation logic is tested against production-like data and shows idempotent, recoverable behavior | M | P1 |

### Phase 5 Integration Points

1. **Named Artifact:** `auth_rollout_control_plane`
   - **Wired Components:** `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`, staged environment configs, rollback toggles
   - **Owning Phase:** Phase 5
   - **Cross-Reference:** Consumed by Phase 6 final business/compliance validation and operational handoff

2. **Named Artifact:** `incident_response_runbook_set`
   - **Wired Components:** outage runbook, refresh-failure runbook, alerts, escalation paths
   - **Owning Phase:** Phase 5
   - **Cross-Reference:** Consumed during GA operations and post-launch compliance/security review

3. **Named Artifact:** `release_gate_matrix`
   - **Wired Components:** FR/NFR evidence, test evidence, performance evidence, security review, rollback drill
   - **Owning Phase:** Phase 5
   - **Cross-Reference:** Consumed in Phase 6 for final traceability and success-metric closure

---

### Phase 6 — PRD Traceability, Compliance Closure, Business Validation, and Open-Item Resolution

**Milestone alignment:** post-hardening pre/post GA validation closure

| # | ID | Task | Component | Dependencies | Acceptance Criteria | Effort | Priority |
|---|---|---|---|---|---|---|---|
| 1 | PRD-FR-TRACE-001 | Cross-verify TDD and PRD login requirement traceability | Requirements traceability | FR-AUTH-001, FR-AUTH.1 | Traceability record shows implementation and tests satisfy both TDD and PRD login intents without gap | S | P1 |
| 2 | PRD-FR-TRACE-002 | Cross-verify TDD and PRD registration requirement traceability | Requirements traceability | FR-AUTH-002, FR-AUTH.2 | Traceability record shows implementation and tests satisfy both TDD and PRD registration intents without gap | S | P1 |
| 3 | PRD-FR-TRACE-003 | Cross-verify TDD and PRD session persistence requirement traceability | Requirements traceability | FR-AUTH-003, FR-AUTH.3 | Traceability record shows refresh/session behavior fulfills PRD persistence expectations | S | P1 |
| 4 | PRD-FR-TRACE-004 | Cross-verify TDD and PRD profile requirement traceability | Requirements traceability | FR-AUTH-004, FR-AUTH.4 | Traceability record shows authenticated profile behavior fulfills PRD profile expectations | S | P1 |
| 5 | PRD-FR-TRACE-005 | Cross-verify TDD and PRD password reset requirement traceability | Requirements traceability | FR-AUTH-005, FR-AUTH.5 | Traceability record shows reset behavior fulfills PRD recovery expectations including session invalidation | S | P1 |
| 6 | PRD-NFR-TRACE-001 | Cross-verify TDD and PRD latency/concurrency requirements | Requirements traceability | NFR-PERF-001, NFR-PERF-002, NFR-AUTH.1 | Traceability record shows both TDD and PRD performance commitments are measured and satisfied | S | P1 |
| 7 | PRD-NFR-TRACE-002 | Cross-verify TDD and PRD availability requirements | Requirements traceability | NFR-REL-001, NFR-AUTH.2 | Traceability record shows reliability design and operations support both TDD and PRD availability commitments | S | P1 |
| 8 | PRD-NFR-TRACE-003 | Cross-verify TDD and PRD password security requirements | Requirements traceability | NFR-SEC-001, NFR-AUTH.3 | Traceability record shows bcrypt/one-way hashing implementation fulfills both TDD and PRD security commitments | S | P1 |
| 9 | PERSONA-001 | Validate released auth flows against Alex the End User outcomes | Persona validation | JOURNEY-001, JOURNEY-002, JOURNEY-003 | Registration, login, persistence, and reset flows align to Alex’s goals and pain-point relief in PRD | S | P1 |
| 10 | PERSONA-002 | Validate released observability/admin flows against Jordan the Platform Admin needs | Persona validation | STORY-008, OPS-013, OPS-014 | Admin-facing operations support incident investigation and account-event visibility needs identified in PRD | S | P1 |
| 11 | PERSONA-003 | Validate released token/API flows against Sam the API Consumer needs | Persona validation | STORY-005, JTBD-004 | Programmatic auth contract supports stable, refreshable integration use cases identified in PRD | S | P1 |
| 12 | JTBD-001 | Validate first-time signup job-to-be-done completion against funnel behavior | Business validation | SUCCESS-002, JOURNEY-001 | Evidence shows first-time signup path is coherent, measurable, and aligned with rapid onboarding objective | S | P1 |
| 13 | JTBD-002 | Validate returning-user resume job-to-be-done completion against session continuity | Business validation | SUCCESS-003, JOURNEY-002 | Evidence shows users can return and resume within active session window without unnecessary friction | S | P1 |
| 14 | JTBD-003 | Validate self-service recovery job-to-be-done completion against reset funnel outcomes | Business validation | SUCCESS-005, JOURNEY-003 | Evidence shows reset path works without support intervention in normal scenarios | S | P1 |
| 15 | JTBD-004 | Validate programmatic integration job-to-be-done completion against API refresh contract | Business validation | STORY-005, PRD-FR-TRACE-003 | Evidence shows integrations can maintain auth continuity without manual user action | S | P1 |
| 16 | STORY-001 | Validate released registration experience against PRD acceptance criteria | Story closure | FR-AUTH-002, COMP-007 | Registration supports required fields, duplicate handling, and successful first-session behavior as promised | S | P1 |
| 17 | STORY-002 | Validate released login experience against PRD acceptance criteria | Story closure | FR-AUTH-001, COMP-006 | Correct credentials succeed; incorrect credentials return generic error with no enumeration leakage | S | P1 |
| 18 | STORY-003 | Validate logout/session-end design expectations even if logout is not a dedicated TDD endpoint | Story closure / scope note | FR-AUTH-003, AUTH_TOKEN_REFRESH, NG-003 | Session end behavior is documented via token invalidation/client clear strategy; any deferred logout endpoint work is explicitly scoped | S | P2 |
| 19 | STORY-004 | Validate session persistence story closure | Story closure | FR-AUTH-003, COMP-008 | Session remains active across refreshes/page loads within refresh window and expires clearly afterward | S | P1 |
| 20 | STORY-005 | Validate token refresh story closure | Story closure | API-004, COMP-002, COMP-008 | Refresh tokens support programmatic renewal and clear error responses on invalidity/expiry | S | P1 |
| 21 | STORY-006 | Validate profile-view story closure | Story closure | FR-AUTH-004, COMP-009 | Profile page displays required account details accurately for authenticated users | S | P1 |
| 22 | STORY-007 | Validate password-reset story closure | Story closure | FR-AUTH-005, API-005, API-006 | Reset email delivery target, TTL, and session invalidation behavior are validated against story expectations | M | P1 |
| 23 | STORY-008 | Validate auth-event-log story closure | Story closure | OPS-005, LEG-002 | Auth event logs satisfy admin and auditor investigation requirements described in PRD | S | P1 |
| 24 | LEG-001 | Validate registration consent capture and timestamp retention | Compliance closure | FR-AUTH-002, TEST-004 | Consent is captured at registration and retained in a form suitable for compliance evidence | S | P1 |
| 25 | LEG-002 | Validate audit logging against SOC2 Type II control expectations | Compliance closure | OPS-005, STORY-008 | Auth events are complete, retained appropriately, and queryable for audit and incident review | M | P0 |
| 26 | LEG-003 | Validate one-way password storage and raw-secret exclusion from logs/storage | Compliance closure | NFR-SEC-001, NFR-AUTH.3 | No raw passwords are stored or logged; hashing implementation remains compliant with stated requirements | S | P0 |
| 27 | LEG-004 | Validate data minimization across collected auth fields | Compliance closure | DM-001, FR-AUTH-002 | Stored auth data remains limited to minimum required fields and does not drift beyond PRD scope | S | P1 |
| 28 | SUCCESS-001 | Close login performance success metric with measured evidence | Success closure | SUCCESS-001, RELEASE-005 | Final evidence package shows login p95 target attainment or documented approved exception/remediation path | S | P0 |
| 29 | SUCCESS-002 | Close registration conversion instrumentation readiness | Success closure | SUCCESS-002 | Final evidence package shows registration funnel instrumentation is production-ready and reviewable by product | S | P1 |
| 30 | SUCCESS-003 | Close average-session-duration measurement readiness | Success closure | SUCCESS-003 | Final evidence package shows session duration can be measured from token/refresh events | S | P1 |
| 31 | SUCCESS-004 | Close failed-login-rate measurement readiness | Success closure | SUCCESS-004 | Final evidence package shows failed login rate can be reliably measured for UX/security monitoring | S | P1 |
| 32 | SUCCESS-005 | Close password-reset completion measurement readiness | Success closure | SUCCESS-005 | Final evidence package shows reset funnel can be measured end-to-end for product review | S | P1 |
| 33 | DEP-001 | Validate SendGrid/email-service dependency readiness for password reset reliability | External dependency validation | API-005, RISK-PRD-004 | Email delivery dependency is available, monitored, and acceptable for production reset flow | M | P1 |
| 34 | DEP-002 | Validate PostgreSQL dependency readiness for production auth persistence | Infrastructure dependency validation | INFRA-DB-001, OPS-017 | Database dependency is production-ready for auth workload, migration, backup, and incident response needs | M | P0 |
| 35 | DEP-003 | Validate frontend-routing dependency readiness for auth pages and redirects | Internal dependency validation | COMP-006, COMP-007, COMP-009 | Frontend routing supports login, register, profile, and post-auth redirect flows without blocking release | S | P1 |
| 36 | DEP-004 | Validate security-policy dependency closure for token and password settings | Policy dependency validation | SEC-POLICY-001, RELEASE-004 | Security policy dependencies are resolved and reflected in final operational configuration | S | P0 |
| 37 | DEP-005 | Validate Node.js 20 LTS runtime readiness and deployment compatibility | Runtime dependency validation | COMP-001, COMP-002, COMP-003 | Production runtime baseline meets TDD dependency expectations without compatibility blockers | S | P1 |
| 38 | DEP-006 | Validate Redis 7+ dependency readiness for refresh token management | Infrastructure dependency validation | COMP-002, OPS-018 | Redis dependency is production-ready for token storage, TTL behavior, and incident handling | M | P0 |
| 39 | DEP-007 | Validate frontend token-based auth support assumptions | Internal dependency validation | COMP-008, FE-AUTH-001-TDD | Frontend stack supports in-memory access token handling, silent refresh triggers, and route protection | S | P1 |
| 40 | DEP-008 | Validate compliance-reference dependencies and evidence linkage | Governance dependency validation | COMPLIANCE-001, SEC-POLICY-001, AUTH-PRD-001 | Required reference documents and evidence links are available for audit/review handoff | S | P1 |
| 41 | REF-001 | Link final implementation and roadmap evidence back to AUTH-PRD-001 | Documentation traceability | AUTH-PRD-001, RELEASE-001 | Final traceability package references PRD for business scope, personas, and success metrics | S | P2 |
| 42 | REF-002 | Link final security evidence back to SEC-POLICY-001 | Documentation traceability | SEC-POLICY-001, LEG-003, DEP-004 | Final security evidence package references governing policy for hashing and token controls | S | P2 |
| 43 | REF-003 | Link final compliance evidence back to COMPLIANCE-001 | Documentation traceability | COMPLIANCE-001, LEG-002 | Final compliance evidence package references audit-log requirements and retention expectations | S | P2 |
| 44 | COST-001 | Validate production cost/resource estimate against actual deployment design | Cost governance | OPS-016, OPS-017, OPS-018 | Final infrastructure design is reconciled against estimated monthly cost and scaling assumptions before steady-state operation | S | P2 |

### Phase 6 Integration Points

1. **Named Artifact:** `auth_traceability_matrix`
   - **Wired Components:** TDD FR/NFR/API/components/tests mapped to PRD FR/NFR/stories/personas/journeys/legal items
   - **Owning Phase:** Phase 6
   - **Cross-Reference:** Consumes artifacts from all prior phases and becomes the final audit/review package

2. **Named Artifact:** `compliance_evidence_bundle`
   - **Wired Components:** consent evidence, audit-log evidence, password-handling evidence, data-minimization evidence
   - **Owning Phase:** Phase 6
   - **Cross-Reference:** Consumes Phase 4 controls and Phase 5 runbooks/release gates; supports Q3 audit preparation

3. **Named Artifact:** `business_metric_readiness_pack`
   - **Wired Components:** registration funnel, login latency, session duration, failed-login rate, reset completion
   - **Owning Phase:** Phase 6
   - **Cross-Reference:** Consumes Phase 4 instrumentation and Phase 5 production rollout data

---

# Risk Assessment and Mitigation Strategies

## 1. Architectural Risks

1. **Token theft via client-side compromise**
   - **Risk:** Access token exposure or refresh-token misuse could enable session hijacking.
   - **Mitigation:**
     - Keep access tokens in memory only.
     - Minimize refresh-token exposure path.
     - Enforce short access-token TTL.
     - Maintain revocation path in `TokenManager`.
   - **Validation:** Security review, threat walkthrough, and revocation drill before GA.

2. **Brute-force pressure on login path**
   - **Risk:** Credential stuffing or repeated password attempts could degrade security and performance.
   - **Mitigation:**
     - API gateway rate limits.
     - Lockout after 5 failed attempts in 15 minutes.
     - Audit and alert on failure-rate spikes.
   - **Validation:** Unit/integration coverage and alert test drill.

3. **Data loss or corruption during migration/cutover**
   - **Risk:** Legacy coexistence or rollback may create record drift or restore complexity.
   - **Mitigation:**
     - Idempotent migration strategy.
     - Backup before each rollout phase.
     - Staging rollback drill on production-like data.
   - **Validation:** `RELEASE-010`, `MIG-007`, `MIG-010`.

## 2. Delivery Risks

1. **Password reset API gap**
   - The extraction identified two implied APIs not fully specified in the TDD API section.
   - **Mitigation:** Explicitly create and validate API-005 and API-006 before implementation proceeds.

2. **Frontend/backend contract drift**
   - `LoginPage`, `RegisterPage`, `AuthProvider`, and `ProfilePage` depend on stable backend semantics.
   - **Mitigation:** Freeze contracts in Phase 1 and consume them in later phases only through named bindings.

3. **Compliance work being deferred too late**
   - GDPR/SOC2/NIST concerns often slip toward release.
   - **Mitigation:** Consent capture, audit logging, and password-handling validation are integrated in Phases 2, 4, and 6.

## 3. Operational Risks

1. **Redis instability impacting refresh**
   - **Mitigation:** Dedicated alerting, runbook, fallback behavior, and rollback trigger.

2. **Email delivery failures blocking recovery**
   - **Mitigation:** Delivery monitoring, explicit dependency validation, and fallback support path.

3. **Insufficient observability during beta**
   - **Mitigation:** Metrics, logs, traces, and runbooks must exist before beta traffic expansion.

---

# Resource Requirements and Dependencies

## 1. Engineering Resources

1. **Backend engineering**
   - `AuthService`
   - `TokenManager`
   - `JwtService`
   - `PasswordHasher`
   - PostgreSQL and Redis integration
   - Reset flow and audit logging

2. **Frontend engineering**
   - `LoginPage`
   - `RegisterPage`
   - `AuthProvider`
   - `ProfilePage`
   - Session continuity and expired-session UX

3. **Platform / infrastructure**
   - PostgreSQL 15+
   - Redis 7+
   - deployment/scaling config
   - monitoring/alerting
   - secrets management for RSA keys

4. **Security / compliance**
   - Security review
   - policy alignment with `SEC-POLICY-001`
   - audit-log completeness validation
   - GDPR consent and data-minimization verification

5. **QA**
   - unit, integration, and E2E test coverage
   - performance testing
   - rollback drill support
   - staging validation

## 2. External and Internal Dependencies

1. **Infrastructure**
   - `INFRA-DB-001` PostgreSQL
   - Redis 7+
   - Node.js 20 LTS runtime

2. **External systems**
   - Email delivery service (SendGrid or equivalent)

3. **Governance / policy**
   - `SEC-POLICY-001`
   - `COMPLIANCE-001`
   - `AUTH-PRD-001`
   - `PLATFORM-PRD-001`

4. **Cross-team dependency**
   - `FE-AUTH-001-TDD` for frontend accessibility/design ownership

## 3. Explicit Wiring Dependencies

1. `AuthService` must be wired to:
   - `PasswordHasher`
   - `UserRepo`
   - `TokenManager`
   - audit/metrics emitters

2. `TokenManager` must be wired to:
   - Redis token store
   - `JwtService`
   - rotation/revocation flow
   - `AUTH_TOKEN_REFRESH`

3. `AuthProvider` must be wired to:
   - login/register/refresh/profile APIs
   - in-memory token state
   - 401 intercept path
   - redirect behavior

---

# Success Criteria and Validation Approach

## 1. Technical Success Criteria

1. Registration, login, refresh, profile, and password reset all work per TDD acceptance criteria.
2. Token lifecycle is secure, revocable, and observable.
3. Auth endpoints meet:
   - p95 latency < 200ms
   - 500 concurrent request target
   - 99.9% availability design target
4. Password handling satisfies:
   - bcrypt cost factor 12
   - no plaintext persistence
   - no sensitive secret leakage in logs
5. Rollout is reversible through validated feature flags and rollback drills.

## 2. Business and Product Validation

1. Registration funnel instrumentation is present for >60% conversion measurement.
2. Session analytics support average session duration measurement.
3. Failed-login rate can be monitored as a UX/security signal.
4. Password reset completion funnel is measurable.
5. Personas and JTBD outcomes are explicitly verified in Phase 6.

## 3. Validation Approach

1. **Unit validation**
   - Auth orchestration
   - hashing
   - token issuance/rotation
   - error semantics

2. **Integration validation**
   - PostgreSQL persistence
   - Redis TTL/revocation
   - API contract fidelity

3. **E2E validation**
   - signup
   - login
   - profile
   - password reset
   - session expiry and refresh

4. **Operational validation**
   - alerts
   - dashboards
   - runbooks
   - rollback drill
   - staging smoke tests

5. **Traceability validation**
   - TDD-to-PRD FR/NFR mapping
   - story/journey/persona closure
   - compliance evidence bundle

---

# Timeline Estimates per Phase

## Phase 1 — Architecture Foundation
- **Focus:** scope controls, component boundaries, data/API contracts, wiring artifacts
- **Estimated duration:** 1 sprint
- **Exit criteria:**
  - architecture frozen for v1.0
  - all primary IDs and contracts mapped
  - explicit wiring mechanisms defined

## Phase 2 — Core Backend Authentication
- **Focus:** registration/login, hashing, persistence, abuse controls
- **Estimated duration:** 1–2 sprints
- **Exit criteria:**
  - M1 complete
  - register/login implemented
  - database-backed registration validated
  - lockout and password security in place

## Phase 3 — Token, Profile, Reset, Frontend Integration
- **Focus:** token lifecycle, profile retrieval, reset flow, frontend session integration
- **Estimated duration:** 2 sprints
- **Exit criteria:**
  - M2, M3, M4 readiness
  - refresh/profile/reset working
  - frontend integrated
  - E2E path operational

## Phase 4 — Hardening and Validation
- **Focus:** observability, alerts, performance, security, expanded tests
- **Estimated duration:** 1 sprint
- **Exit criteria:**
  - monitoring in place
  - security controls validated
  - performance evidence collected
  - test matrix complete

## Phase 5 — Migration and GA Readiness
- **Focus:** rollout phases, feature flags, rollback drills, runbooks, release gates
- **Estimated duration:** 1 sprint plus controlled rollout windows
- **Exit criteria:**
  - staged rollout completed
  - GA gate passed
  - rollback tested
  - operations ownership active

## Phase 6 — Traceability and Compliance Closure
- **Focus:** PRD/TDD traceability, persona/journey closure, compliance evidence, metric readiness
- **Estimated duration:** parallel with late Phase 5 and immediate post-GA validation window
- **Exit criteria:**
  - full evidence bundle complete
  - success metrics measurable
  - audit/compliance handoff prepared
  - roadmap closure package approved

## Overall Roadmap Milestone View

1. **M1:** Core `AuthService`, `PasswordHasher`, `UserProfile`, login/register
2. **M2:** `TokenManager`, `JwtService`, `AuthToken`, refresh/profile
3. **M3:** Password reset and email integration
4. **M4:** Frontend integration (`LoginPage`, `RegisterPage`, `AuthProvider`, `ProfilePage`)
5. **M5:** General availability with staged rollout, observability, rollback, and operational ownership

## Recommended Architect Sign-Off Gates

1. **Gate A — Architecture freeze:** end of Phase 1
2. **Gate B — Security/runtime correctness:** end of Phase 3
3. **Gate C — Hardening complete:** end of Phase 4
4. **Gate D — Production cutover approval:** before MIG-003
5. **Gate E — Audit/business readiness closure:** end of Phase 6

