---
spec_source: "test-spec-user-auth.md"
generated: "2026-04-15T00:00:00Z"
generator: "requirements-extraction-agent"
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.6
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, database, infrastructure]
risks_identified: 9
dependencies_identified: 8
success_criteria_count: 11
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 188.0, started_at: "2026-04-15T20:12:20.943669+00:00", finished_at: "2026-04-15T20:15:28.967309+00:00"}
---

## Functional Requirements

### FR-AUTH.1: User Login

**Description**: The system shall authenticate users via email and password, returning a valid JWT access token and a refresh token upon successful credential verification.

**Endpoints**: `POST /auth/login` (spec §2.2 workflow diagram, TDD §8.2)

**Acceptance Criteria**:
- Valid email and password → 200 with access_token (15min TTL) and refresh_token (7d TTL)
- Invalid credentials → 401; must not reveal whether email or password was incorrect
- Locked account → 403 indicating account suspension
- Rate-limit login attempts to 5 per minute per IP address

**Sub-decomposition (from TDD)**:
- FR-AUTH.1a: Account lockout after 5 failed attempts within 15 minutes (TDD §5.1 FR-AUTH-001 AC #4; spec GAP-1 notes this is partially addressed)
- FR-AUTH.1b: TDD specifies 10 req/min per IP rate limit (TDD §8.1) vs. spec's 5/min; **conflict noted**
- FR-AUTH.1c: 423 Locked response for locked accounts (TDD §8.2)

**Dependencies**: PasswordHasher, TokenManager, User database table

### FR-AUTH.2: User Registration

**Description**: The system shall register new users with input validation, creating a user record with a securely hashed password and returning confirmation of successful registration.

**Endpoints**: `POST /auth/register` (TDD §8.1, §8.2)

**Acceptance Criteria**:
- Valid registration data (email, password, display name) → 201 with user profile
- Already-registered email → 409 conflict
- Password policy: minimum 8 characters, at least one uppercase, one lowercase, one digit
- Email format validated before registration

**Sub-decomposition (from TDD)**:
- FR-AUTH.2a: Email normalized to lowercase by AuthService (TDD §7.1)
- FR-AUTH.2b: PasswordHasher stores bcrypt hash with cost factor 12 (TDD §5.1 FR-AUTH-002 AC #4)
- FR-AUTH.2c: Response includes full UserProfile (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles) per TDD §8.2

**Dependencies**: PasswordHasher, User database table

### FR-AUTH.3: Token Refresh

**Description**: The system shall issue and refresh JWT tokens, allowing clients to obtain a new access token using a valid refresh token without re-entering credentials.

**Endpoints**: `POST /auth/refresh` (TDD §8.1, §8.2)

**Acceptance Criteria**:
- Valid refresh token → new access_token + rotated refresh_token
- Expired refresh token → 401 requiring re-authentication
- Previously-rotated (revoked) refresh token → invalidate all tokens for that user (replay detection)
- Refresh token hashes stored in database for revocation support

**Sub-decomposition (from TDD)**:
- FR-AUTH.3a: TokenManager stores refresh tokens in Redis with 7-day TTL (TDD §7.2)
- FR-AUTH.3b: Rate limit 30 req/min per user on refresh endpoint (TDD §8.1)

**Dependencies**: TokenManager, JwtService, RefreshToken database table

### FR-AUTH.4: Profile Retrieval

**Description**: The system shall provide authenticated user profile retrieval, returning the current user's profile data when presented with a valid access token.

**Endpoints**: `GET /auth/me` (spec §2.2 workflow diagram, TDD §8.1, §8.2)

**Acceptance Criteria**:
- Valid Bearer access_token → user profile (id, email, display_name, created_at)
- Expired or invalid token → 401
- Must not return sensitive fields (password_hash, refresh_token_hash)

**Sub-decomposition (from TDD)**:
- FR-AUTH.4a: Response includes additional fields: updatedAt, lastLoginAt, roles (TDD §7.1, §8.2)
- FR-AUTH.4b: Rate limit 60 req/min per user (TDD §8.1)

**Dependencies**: TokenManager, User database table

### FR-AUTH.5: Password Reset

**Description**: The system shall support a secure password reset flow, allowing users to request a reset link and set a new password using a time-limited token.

**Endpoints**: `POST /auth/reset-request`, `POST /auth/reset-confirm` (TDD §8 implied by FR-AUTH-005)

**Acceptance Criteria**:
- Registered email → generate password reset token (1-hour TTL) and dispatch reset email
- Valid reset token → allow setting new password and invalidate reset token
- Expired or invalid reset token → 400 with appropriate error
- Invalidate all existing sessions (refresh tokens) upon successful password reset

**Sub-decomposition (from TDD)**:
- FR-AUTH.5a: Used reset tokens cannot be reused (TDD §5.1 FR-AUTH-005 AC #4)
- FR-AUTH.5b: Same confirmation response regardless of email registration status to prevent enumeration (PRD §Error Handling)

**Dependencies**: TokenManager, PasswordHasher, Email service (external)

## Non-Functional Requirements

### Spec-defined NFRs

| ID | Requirement | Target | Measurement |
|---|---|---|---|
| NFR-AUTH.1 | Authentication endpoint response time | < 200ms p95 under normal load | Load testing with k6; production APM p95 monitoring |
| NFR-AUTH.2 | Service availability | 99.9% uptime (< 8.76 hours downtime/year) | Health check endpoint; PagerDuty alerting |
| NFR-AUTH.3 | Password hashing security | bcrypt cost factor 12 (~250ms per hash) | Unit test verifying cost factor; benchmark test |

### TDD-supplementary NFRs

| ID | Requirement | Target | Measurement |
|---|---|---|---|
| NFR-PERF-002 | Concurrent authentication capacity | 500 concurrent login requests | Load testing with k6 (TDD §5.2) |
| NFR-SEC-002 | Token signing algorithm | RS256 using 2048-bit RSA keys | Configuration validation test (TDD §5.2) |

### PRD-supplementary NFRs (Legal & Compliance — PRD §Legal and Compliance)

| ID | Requirement | Target | Measurement |
|---|---|---|---|
| NFR-001 | GDPR consent at registration | Consent recorded with timestamp at account creation | Audit of registration flow; consent field in UserProfile |
| NFR-002 | SOC2 Type II audit logging | All auth events logged with user ID, timestamp, IP, outcome; 12-month retention | Log query verification; retention policy audit |
| NFR-003 | NIST SP 800-63B password storage | One-way adaptive hashing; raw passwords never persisted or logged | Code review; security scan; penetration test |
| NFR-004 | GDPR data minimization | Only email, hashed password, display name collected | Schema review; no additional PII fields |

## Complexity Assessment

**Score**: 0.6 / 1.0 — **MEDIUM**

**Scoring Rationale**:

| Factor | Score | Justification |
|---|---|---|
| Scope breadth | 0.5 | 5 functional requirements covering standard auth flows; well-bounded scope |
| Integration surface | 0.6 | 3 external dependencies (PostgreSQL, Redis, SendGrid); 4 internal components |
| Security sensitivity | 0.8 | Password hashing, JWT signing, token rotation, replay detection — errors have high impact |
| Architectural complexity | 0.5 | Layered architecture with clear separation; no distributed transactions |
| Data model complexity | 0.4 | 3 data models with straightforward relationships |
| Rollout risk | 0.6 | Phased rollout with feature flags; migration from legacy auth; rollback plan defined |
| Novelty | 0.4 | Standard authentication patterns; well-documented industry practices |

**Weighted average**: 0.6. The elevated security sensitivity is offset by the bounded scope and standard architectural patterns.

## Architectural Constraints

| # | Constraint | Source |
|---|---|---|
| 1 | JWT tokens signed with RS256 using 2048-bit RSA keys; no symmetric signing | Spec §2.1, TDD §5.2 |
| 2 | bcrypt with cost factor 12 for password hashing; configurable for future migration | Spec §2.1, TDD §6.4 |
| 3 | Access token stored in memory only (not localStorage); refresh token in httpOnly cookie | Spec §2.1, TDD §20 R-001 |
| 4 | Stateless JWT — no server-side session store required for access token validation | Spec §2.1, TDD §9 |
| 5 | Refresh tokens stored as hashed values in Redis with 7-day TTL | TDD §7.2 |
| 6 | PostgreSQL 15+ for UserProfile persistence; Redis 7+ for TokenManager | TDD §18, §7.2 |
| 7 | Node.js 20 LTS runtime | TDD §18 |
| 8 | API versioned via URL prefix (`/v1/auth/*` in production) | TDD §8.4 |
| 9 | Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` control rollout phases | TDD §19.2 |
| 10 | Layered architecture: AuthService → TokenManager/PasswordHasher → JwtService | Spec §4.4 |
| 11 | Implementation order: PasswordHasher + JwtService (parallel) → TokenManager → AuthService → middleware → routes/migrations | Spec §4.6 |
| 12 | TLS 1.3 enforced on all endpoints | TDD §13 |
| 13 | CORS restricted to known frontend origins | TDD §13 |
| 14 | **Persona-driven**: Alex (end user) requires < 60s registration, seamless session persistence; Sam (API consumer) requires programmatic token refresh; Jordan (admin) requires audit log visibility | PRD §User Personas |
| 15 | Password policy must comply with NIST SP 800-63B | PRD §Assumptions and Constraints |
| 16 | All auth events must be logged for SOC2 audit trail | PRD §Assumptions and Constraints |

## Component Inventory

### Services & Modules (COMP-xxx)

| ID | Name | Path | Role | Dependencies | Source |
|---|---|---|---|---|---|
| COMP-001 | AuthService | `src/auth/auth-service.ts` | Core authentication orchestrator; coordinates login, register, refresh, reset flows | COMP-002, COMP-004, COMP-010 | Spec §4.1, TDD §6.1 |
| COMP-002 | TokenManager | `src/auth/token-manager.ts` | JWT lifecycle management; issues, refreshes, revokes token pairs; stores refresh tokens in Redis | COMP-003 | Spec §4.1, TDD §6.1 |
| COMP-003 | JwtService | `src/auth/jwt-service.ts` | Low-level JWT signing (RS256) and verification | jsonwebtoken library, RSA key pair | Spec §4.1, TDD §6.1 |
| COMP-004 | PasswordHasher | `src/auth/password-hasher.ts` | bcrypt password hashing and comparison with configurable cost factor | bcryptjs library | Spec §4.1, TDD §6.1 |
| COMP-005 | AuthMiddleware | `src/middleware/auth-middleware.ts` | Bearer token extraction and verification in request pipeline | COMP-002 | Spec §4.2, TDD §6.2 |
| COMP-006 | LoginPage | frontend (path unspecified) | Email/password login form; calls POST `/auth/login`; stores AuthToken via AuthProvider | COMP-008 | TDD §10.1, §10.2 |
| COMP-007 | RegisterPage | frontend (path unspecified) | Registration form with client-side password validation; calls POST `/auth/register` | COMP-008 | TDD §10.1, §10.2 |
| COMP-008 | AuthProvider | frontend (path unspecified) | React context provider managing AuthToken state; handles silent refresh; exposes UserProfile | COMP-002 (via API) | TDD §10.2, §10.3 |
| COMP-009 | ProfilePage | frontend (path unspecified) | Displays UserProfile data; calls GET `/auth/me` | COMP-008 | TDD §10.1 |
| COMP-010 | UserRepo | database layer (path unspecified) | PostgreSQL repository for UserProfile CRUD operations | PostgreSQL | TDD §6.1 |
| COMP-011 | Routes | `src/routes/index.ts` | Registers `/auth/*` route group | COMP-001 | Spec §4.2 |
| COMP-012 | AuthMigration | `src/database/migrations/003-auth-tables.ts` | Database migration: creates users and refresh_tokens tables | PostgreSQL | Spec §4.2 |

### Data Models (DM-xxx)

| ID | Name | Role | Fields | Source |
|---|---|---|---|---|
| DM-001 | UserRecord / UserProfile | Persistent user account data | `id: string (UUID v4)`, `email: string (unique, indexed)`, `display_name/displayName: string`, `password_hash: string (bcrypt)`, `is_locked: boolean`, `created_at/createdAt: Date/string (ISO 8601)`, `updated_at/updatedAt: Date/string (ISO 8601)`, `lastLoginAt: string (ISO 8601, nullable)` [TDD], `roles: string[]` [TDD] | Spec §4.5, TDD §7.1 |
| DM-002 | RefreshTokenRecord | Persistent refresh token for revocation support | `id: string (UUID v4)`, `user_id: string (FK → UserRecord.id)`, `token_hash: string (SHA-256)`, `expires_at: Date`, `revoked: boolean`, `created_at: Date` | Spec §4.5 |
| DM-003 | AuthTokenPair / AuthToken | Token pair returned to clients | `access_token/accessToken: string (JWT, 15-min TTL)`, `refresh_token/refreshToken: string (opaque, 7-day TTL)`, `expiresIn: number (900)` [TDD], `tokenType: string ("Bearer")` [TDD] | Spec §4.5, TDD §7.1 |

**Note**: The spec uses `UserRecord` with `snake_case` fields; the TDD uses `UserProfile` with `camelCase` fields and adds `lastLoginAt` and `roles`. The TDD's `AuthToken` adds `expiresIn` and `tokenType` fields not present in the spec's `AuthTokenPair`. These differences should be reconciled during implementation.

## Risk Inventory

| # | Risk | Severity | Source | Mitigation |
|---|---|---|---|---|
| 1 | JWT secret key compromise allows forged tokens | High | Spec §7 | RS256 asymmetric keys; private key in secrets manager; key rotation every 90 days |
| 2 | Refresh token replay attack after token theft | High | Spec §7 | Refresh token rotation with replay detection; revoke all user tokens on suspicious reuse |
| 3 | bcrypt cost factor too low for future hardware | Medium | Spec §7 | Configurable cost factor; annual review against OWASP; migration path to Argon2id |
| 4 | Token theft via XSS enables session hijacking | High | TDD §20 R-001 | Access token in memory only; httpOnly cookies for refresh; 15-min access expiry; AuthProvider clears tokens on tab close |
| 5 | Brute-force attacks on login endpoint | Medium | TDD §20 R-002 | Rate limiting at API Gateway (10 req/min/IP); account lockout after 5 failed attempts; bcrypt cost factor 12 |
| 6 | Data loss during migration from legacy auth | High | TDD §20 R-003 | Parallel run during Phase 1-2; idempotent upsert operations; full database backup before each phase |
| 7 | Low registration adoption due to poor UX | High | PRD §Risk Analysis | Usability testing before launch; iterate based on funnel data |
| 8 | Compliance failure from incomplete audit logging | High | PRD §Risk Analysis | Define log requirements early; validate against SOC2 controls in QA |
| 9 | Email delivery failures blocking password reset | Medium | PRD §Risk Analysis | Delivery monitoring and alerting; fallback support channel |

## Dependency Inventory

| # | Dependency | Type | Version | Purpose | Impact if Unavailable |
|---|---|---|---|---|---|
| 1 | PostgreSQL | Infrastructure | 15+ | UserProfile persistence, audit logs | No user storage; service non-functional |
| 2 | Redis | Infrastructure | 7+ | Refresh token storage and revocation by TokenManager | Token refresh blocked; users must re-login on access token expiry |
| 3 | Node.js | Runtime | 20 LTS | Application runtime | Service cannot run |
| 4 | bcryptjs | Library | — | Password hashing in PasswordHasher | Registration and login blocked |
| 5 | jsonwebtoken | Library | — | JWT signing/verification in JwtService | Token issuance blocked |
| 6 | SendGrid API | External service | — | Password reset email delivery | Password reset flow blocked (FR-AUTH.5) |
| 7 | Frontend routing framework | Internal | — | Client-side routing for LoginPage, RegisterPage, ProfilePage | Auth pages cannot render |
| 8 | SEC-POLICY-001 | Policy document | — | Defines password and token security requirements | Password and token policies undefined |

## Success Criteria

| # | Criterion | Target | Source | Measurement |
|---|---|---|---|---|
| 1 | Login response time (p95) | < 200ms | Spec NFR-AUTH.1, TDD §4.1 | APM on AuthService.login() |
| 2 | Registration success rate | > 99% | TDD §4.1 | Successful registrations / total attempts |
| 3 | Token refresh latency (p95) | < 100ms | TDD §4.1 | APM on TokenManager.refresh() |
| 4 | Service availability | 99.9% uptime (30-day rolling) | Spec NFR-AUTH.2, TDD §4.1 | Health check monitoring |
| 5 | Password hash time | < 500ms | TDD §4.1 | Benchmark of PasswordHasher.hash() |
| 6 | Registration conversion rate | > 60% | TDD §4.2, PRD §Success Metrics | Funnel: landing → register → confirmed |
| 7 | Daily active authenticated users | > 1000 within 30 days of GA | TDD §4.2 | AuthToken issuance counts |
| 8 | Average session duration | > 30 minutes | PRD §Success Metrics | Token refresh event analytics |
| 9 | Failed login rate | < 5% of attempts | PRD §Success Metrics | Auth event log analysis |
| 10 | Password reset completion rate | > 80% | PRD §Success Metrics | Funnel: reset requested → new password set |
| 11 | Unit test coverage | > 80% for AuthService, TokenManager, JwtService, PasswordHasher | TDD §24.1 | Jest coverage report |

## Open Questions

| # | Question | Source | Owner | Impact |
|---|---|---|---|---|
| 1 | Should password reset emails be sent synchronously or via a message queue? | Spec §11 OI-1, PRD §Open Questions | Engineering | Affects latency of reset endpoint and system resilience |
| 2 | Maximum number of active refresh tokens per user? | Spec §11 OI-2, PRD §Open Questions | Product | Affects storage requirements and multi-device support |
| 3 | Should AuthService support API key authentication for service-to-service calls? | TDD §22 OQ-001 | test-lead | Deferred to v1.1; may affect AuthMiddleware interface |
| 4 | Maximum allowed UserProfile roles array length? | TDD §22 OQ-002 | auth-team | Pending RBAC design review |
| 5 | Account lockout policy after N consecutive failed attempts? | PRD §Open Questions, Spec §12 GAP-1 | Security | Spec rate-limits at 5/min/IP but lacks progressive lockout; TDD defines 5 attempts in 15 minutes |
| 6 | Should "remember me" option extend session duration? | PRD §Open Questions | Product | Affects refresh token TTL and UX |
| 7 | **Rate limit conflict**: Spec FR-AUTH.1 says 5 req/min/IP; TDD §8.1 says 10 req/min/IP for login | Spec §3 vs TDD §8.1 | Engineering | Must reconcile before implementation |
| 8 | **Data model divergence**: Spec uses `UserRecord` (snake_case) vs TDD uses `UserProfile` (camelCase); TDD adds `lastLoginAt`, `roles` fields not in spec | Spec §4.5 vs TDD §7.1 | Engineering | Schema must be finalized before migration |
| 9 | **Logout not specified**: PRD scope includes logout; PRD user stories include explicit logout AC; but spec has no FR for logout | PRD §Scope Definition, §User Stories (AUTH-E1) | Product/Engineering | JTBD #2 and persona "Alex" expect logout; missing functional requirement |
| 10 | **Admin audit logging not specified**: PRD persona "Jordan" and user story require auth event log querying; no corresponding FR in spec | PRD §User Personas (Jordan), §User Stories (AUTH-E3) | Product/Engineering | SOC2 compliance (NFR-002) depends on this; spec GAP-2 acknowledges the gap but defers to v1.1 |
| 11 | **Refresh token storage divergence**: Spec §4.5 stores refresh tokens in PostgreSQL (RefreshTokenRecord); TDD §7.2 stores them in Redis | Spec §4.5 vs TDD §7.2 | Engineering | Architectural decision must be finalized; affects revocation strategy |
