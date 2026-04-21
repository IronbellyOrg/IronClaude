---
spec_source: test-tdd-user-auth.compressed.md
generated: 2026-04-20T00:00:00Z
generator: tdd-prd-extraction-agent
functional_requirements: 5
nonfunctional_requirements: 9
total_requirements: 14
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, security, frontend, testing, devops, data, compliance]
risks_identified: 7
dependencies_identified: 6
success_criteria_count: 10
extraction_mode: standard
data_models_identified: 2
api_surfaces_identified: 6
components_identified: 7
test_artifacts_identified: 6
migration_items_identified: 5
operational_items_identified: 7
pipeline_diagnostics: {elapsed_seconds: 152.2, started_at: "2026-04-20T22:03:47.116269+00:00", finished_at: "2026-04-20T22:06:19.306759+00:00"}
---

## Functional Requirements

### FR-AUTH-001 — Login with email and password
`AuthService` authenticates users by validating email/password against bcrypt hashes via `PasswordHasher`.
- Valid credentials: 200 with `AuthToken` (accessToken + refreshToken)
- Invalid credentials: 401 with generic error
- Non-existent email: 401 (no user enumeration)
- Account locked after 5 failed attempts within 15 minutes
- Maps to PRD FR-AUTH.1

### FR-AUTH-002 — User registration with validation
`AuthService` creates user accounts with email uniqueness, password strength enforcement, and `UserProfile` creation.
- Valid registration: 201 with `UserProfile`
- Duplicate email: 409 Conflict
- Weak passwords (<8 chars, no uppercase, no number): 400
- Password stored via `PasswordHasher` bcrypt cost factor 12
- Maps to PRD FR-AUTH.2

### FR-AUTH-003 — JWT token issuance and refresh
`TokenManager` issues JWT access tokens (15-min TTL) and refresh tokens (7-day TTL) via `JwtService`, supporting silent refresh.
- Login returns both tokens with correct TTLs
- POST `/auth/refresh` with valid refreshToken returns new pair
- Expired/revoked refreshToken: 401
- Maps to PRD FR-AUTH.3 (session persistence)

### FR-AUTH-004 — User profile retrieval
`AuthService` returns authenticated user's `UserProfile` via GET `/auth/me`.
- Valid accessToken: returns id, email, displayName, createdAt, updatedAt, lastLoginAt, roles
- Expired/invalid token: 401
- Maps to PRD FR-AUTH.4

### FR-AUTH-005 — Password reset flow
Two-step: request (sends email with token) and confirmation (validates token, updates hash).
- POST `/auth/reset-request`: sends reset email to valid email
- POST `/auth/reset-confirm`: validates token, updates password hash
- Reset tokens expire after 1 hour
- Used reset tokens cannot be reused
- Maps to PRD FR-AUTH.5

## Non-Functional Requirements

### NFR-PERF-001 — API response time
All auth endpoints respond in <200ms at p95, measured via APM tracing on `AuthService` methods.

### NFR-PERF-002 — Concurrent authentication
Support 500 concurrent login requests, validated via k6 load testing.

### NFR-REL-001 — Service availability
99.9% uptime over 30-day rolling windows, monitored via health check endpoint.

### NFR-SEC-001 — Password hashing
`PasswordHasher` uses bcrypt with cost factor 12, verified by unit test asserting cost parameter.

### NFR-SEC-002 — Token signing
`JwtService` signs tokens with RS256 using 2048-bit RSA keys, validated via configuration test.

### NFR-COMPLIANCE-001 — SOC2 audit logging (from PRD)
All auth events logged with user ID, timestamp, IP, outcome; 12-month retention for SOC2 Type II compliance.

### NFR-COMPLIANCE-002 — GDPR consent at registration (from PRD)
Users must consent to data collection at registration; consent recorded with timestamp.

### NFR-COMPLIANCE-003 — NIST password storage (from PRD)
Password storage must comply with NIST SP 800-63B: one-way adaptive hashing; raw passwords never persisted or logged.

### NFR-COMPLIANCE-004 — GDPR data minimization (from PRD)
Only email, hashed password, and display name collected. No additional PII required.

## Complexity Assessment

**complexity_score: 0.65 — MEDIUM**

Scoring rationale:
- **Scope (0.15/0.20):** 5 functional requirements, 4 core API endpoints, 2 data models, 3 frontend components. Bounded but multi-surface.
- **Integration (0.18/0.25):** PostgreSQL + Redis + SMTP email + 2 external libraries (bcryptjs, jsonwebtoken); managed by `TokenManager`, `PasswordHasher`, `JwtService` specialized components.
- **Security (0.18/0.20):** Defense-in-depth required: bcrypt cost 12, RS256 2048-bit keys, TLS 1.3, CORS, rate limiting, account lockout, hashed refresh tokens, quarterly key rotation.
- **Operational (0.08/0.15):** Three-phase rollout with feature flags, runbook scenarios, HPA scaling, on-call rotation.
- **Compliance (0.06/0.10):** SOC2 + GDPR + NIST constraints materially shape design.
- **UI (0.00/0.10):** Minimal — 3 React components consuming API; backend-weighted TDD.

Total complexity falls in MEDIUM band (0.50-0.75). Risk drivers: cryptographic correctness, session hijacking, and migration from legacy auth without data loss.

## Architectural Constraints

1. **Runtime:** Node.js 20 LTS (mandated)
2. **Persistence:** PostgreSQL 15+ for `UserProfile` and audit log; Redis 7+ for refresh tokens
3. **Session mechanism:** JWT (stateless) — server-side sessions rejected (D6.4 decision); must remain stateless for horizontal scaling
4. **Signing algorithm:** RS256 with 2048-bit RSA, quarterly key rotation
5. **Hashing algorithm:** bcrypt cost factor 12 (argon2id/scrypt rejected); `PasswordHasher` abstraction for future migration
6. **Transport:** TLS 1.3 enforced on all endpoints
7. **API surface:** RESTful, versioned via URL prefix (`/v1/auth/*`); JSON only
8. **Rate limiting enforcement:** At API Gateway (not in `AuthService`)
9. **CORS:** Restricted to known frontend origins
10. **Email delivery:** SendGrid (external dependency)
11. **Frontend context:** React `AuthProvider` wraps all routes; accessToken in-memory only, refreshToken via HttpOnly cookie
12. **Persona-driven (from PRD):** Alex (end user — <60s registration, seamless session); Jordan (admin — centralized user visibility, audit log access); Sam (API consumer — programmatic refresh, clear error codes)
13. **Scope boundary (from PRD):** Email/password only in v1.0; no OAuth, no MFA, no RBAC enforcement
14. **Log hygiene:** Passwords and tokens excluded from all application logs

## Risk Inventory

1. **R-001 (High severity)** — Token theft via XSS allows session hijacking. *Mitigation:* accessToken in memory only; HttpOnly cookies for refreshToken; 15-min access token expiry. *Contingency:* Immediate revocation via `TokenManager`; force password reset.
2. **R-002 (Medium severity)** — Brute-force attacks on login endpoint. *Mitigation:* Gateway rate limiting (10 req/min/IP); account lockout after 5 failed attempts; bcrypt cost 12. *Contingency:* WAF IP block; CAPTCHA on `LoginPage` after 3 failures.
3. **R-003 (High severity)** — Data loss during migration from legacy auth. *Mitigation:* Parallel run in Phase 1/2; idempotent upserts; full backup before each phase. *Contingency:* Rollback to legacy; restore from backup.
4. **R-PRD-001 (High severity, from PRD)** — Low registration adoption due to poor UX. *Mitigation:* Usability testing before launch; funnel iteration.
5. **R-PRD-002 (Critical severity, from PRD)** — Security breach from implementation flaws. *Mitigation:* Dedicated security review; penetration testing pre-production.
6. **R-PRD-003 (High severity, from PRD)** — Compliance failure from incomplete SOC2 audit logging. *Mitigation:* Define log requirements early; validate against SOC2 controls in QA.
7. **R-PRD-004 (Medium severity, from PRD)** — Email delivery failures blocking password reset. *Mitigation:* Delivery monitoring/alerting; fallback support channel.

## Dependency Inventory

1. **PostgreSQL 15+** — `UserProfile` persistence and audit log
2. **Redis 7+** — `TokenManager` refresh token storage with 7-day TTL
3. **Node.js 20 LTS** — Runtime
4. **bcryptjs** — Password hashing library inside `PasswordHasher`
5. **jsonwebtoken** — JWT signing/verification inside `JwtService`
6. **SendGrid API** — SMTP/API for password reset emails (external SaaS)

Internal upstream: AUTH-PRD-001, INFRA-DB-001, SEC-POLICY-001. Downstream consumers: frontend (`LoginPage`, `RegisterPage`, `AuthProvider`), platform-team.

## Success Criteria

1. **Login p95 latency <200ms** (APM on `AuthService.login()`)
2. **Registration success rate >99%** (success/attempt ratio)
3. **Token refresh p95 latency <100ms** (APM on `TokenManager.refresh()`)
4. **Service availability 99.9%** over 30-day windows
5. **Password hash time <500ms** (benchmark `PasswordHasher.hash()` cost 12)
6. **User registration conversion >60%** (funnel `RegisterPage` → confirmed account)
7. **Daily active authenticated users >1000** within 30 days of GA (`AuthToken` issuance counts)
8. **Average session duration >30 minutes** — PRD success metric (token refresh event analytics)
9. **Failed login rate <5% of attempts** — PRD success metric (auth event log analysis)
10. **Password reset completion >80%** — PRD success metric (funnel: reset requested → new password set)

## Open Questions

1. **OQ-001** — Should `AuthService` support API key authentication for service-to-service calls? *Owner:* test-lead. *Target:* 2026-04-15. *Status:* Open — deferred to v1.1 scope.
2. **OQ-002** — Maximum allowed `UserProfile.roles` array length? *Owner:* auth-team. *Target:* 2026-04-01. *Status:* Open — pending RBAC design review.
3. **OQ-PRD-001** — Password reset emails sent synchronously or asynchronously? *Owner:* Engineering.
4. **OQ-PRD-002** — Maximum number of refresh tokens per user across devices? *Owner:* Product.
5. **OQ-PRD-003** — Account lockout policy exact threshold (TDD says 5 attempts / 15 min; PRD does not confirm)? *Owner:* Security.
6. **OQ-PRD-004** — Support "remember me" to extend session duration? *Owner:* Product.
7. **JTBD coverage gap** — PRD JTBD "see who attempted access and lock compromised accounts" (Jordan admin persona) has no corresponding FR in TDD; admin console / lockout UI is implicit only via logs. Needs FR or explicit out-of-scope note.

## Data Models and Interfaces

### DM-001 — UserProfile

TypeScript interface backing PostgreSQL table.

```ts
interface UserProfile {
  id: string;            // UUID v4
  email: string;         // unique, indexed, lowercase normalized
  displayName: string;   // 2-100 chars
  createdAt: string;     // ISO 8601
  updatedAt: string;     // ISO 8601
  lastLoginAt: string;   // ISO 8601, nullable
  roles: string[];       // default ["user"]
}
```

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | string (UUID) | PRIMARY KEY, NOT NULL | Unique user identifier |
| email | string | UNIQUE, NOT NULL, indexed | Normalized lowercase |
| displayName | string | NOT NULL, 2-100 chars | UI display name |
| createdAt | string (ISO 8601) | NOT NULL, DEFAULT now() | Creation timestamp |
| updatedAt | string (ISO 8601) | NOT NULL, auto-updated | Last modification |
| lastLoginAt | string (ISO 8601) | NULLABLE | Updated on successful login |
| roles | string[] | NOT NULL, DEFAULT ["user"] | Authorization roles (enforced downstream) |

Relationships: 1:N with refresh tokens (Redis, keyed by user id); 1:N with audit log entries.

### DM-002 — AuthToken

```ts
interface AuthToken {
  accessToken: string;   // JWT, 15-min expiry
  refreshToken: string;  // opaque, Redis-stored
  expiresIn: number;     // 900
  tokenType: string;     // "Bearer"
}
```

| Field | Type | Constraints | Description |
|---|---|---|---|
| accessToken | string (JWT) | NOT NULL | RS256-signed; payload contains user id, roles |
| refreshToken | string | NOT NULL, unique | Opaque; hashed Redis storage, 7-day TTL |
| expiresIn | number | NOT NULL | Always 900 |
| tokenType | string | NOT NULL | Always "Bearer" (OAuth2 compat) |

### Data Flow
1. `AuthService.login()` → `PasswordHasher.verify()` against PostgreSQL hash
2. On success → `TokenManager.issueTokens()` → `JwtService.sign()` + opaque refresh token
3. Refresh token hashed and stored in Redis with 7-day TTL keyed by user id
4. Client re-auth → `TokenManager.refresh()` validates Redis, revokes old, issues new pair

### Storage Strategy
| Store | Technology | Purpose | Retention |
|---|---|---|---|
| Users | PostgreSQL 15 | `UserProfile` + bcrypt hashes | Indefinite |
| Refresh tokens | Redis 7 | `TokenManager` storage / revocation | 7-day TTL |
| Audit log | PostgreSQL 15 | Login attempts, password resets (SOC2) | 90 days (TDD); 12 months required by PRD — CONFLICT |

**Note:** TDD states 90-day audit retention; PRD compliance section requires 12-month SOC2 retention. PRD business intent wins → target 12 months.

## API Specifications

Versioning: URL prefix `/v1/auth/*`. Breaking changes require major version. Non-breaking additions permitted. All error responses use consistent envelope.

### API-001 — POST /auth/login
| Aspect | Value |
|---|---|
| Auth | No |
| Rate limit | 10 req/min per IP |
| Request | `{email, password}` |
| Response 200 | `AuthToken` (accessToken, refreshToken, expiresIn=900, tokenType=Bearer) |
| 401 | Invalid credentials (generic) |
| 423 | Account locked (5 failed attempts) |
| 429 | Rate limit exceeded |

### API-002 — POST /auth/register
| Aspect | Value |
|---|---|
| Auth | No |
| Rate limit | 5 req/min per IP |
| Request | `{email, password, displayName}` |
| Response 201 | `UserProfile` |
| 400 | Validation errors (weak password, invalid email) |
| 409 | Email already registered |

### API-003 — GET /auth/me
| Aspect | Value |
|---|---|
| Auth | Yes (Bearer) |
| Rate limit | 60 req/min per user |
| Headers | `Authorization: Bearer <jwt>` |
| Response 200 | `UserProfile` |
| 401 | Missing, expired, or invalid token |

### API-004 — POST /auth/refresh
| Aspect | Value |
|---|---|
| Auth | No (refresh token in body) |
| Rate limit | 30 req/min per user |
| Request | `{refreshToken}` |
| Response 200 | New `AuthToken` pair (old refresh revoked) |
| 401 | Expired or revoked refresh token |

### API-005 — POST /auth/reset-request
| Aspect | Value |
|---|---|
| Auth | No |
| Rate limit | Not explicitly specified — needs determination |
| Request | `{email}` |
| Response | Generic confirmation (enumeration-safe) |
| Behavior | Sends reset email with 1-hour TTL token via SendGrid |

### API-006 — POST /auth/reset-confirm
| Aspect | Value |
|---|---|
| Auth | No (token in body) |
| Request | `{resetToken, newPassword}` |
| Response 200 | Password updated; all sessions invalidated |
| 401 | Token expired or already used |
| 400 | New password fails policy |

### API Governance
Standard error envelope:
```json
{"error": {"code": "AUTH_INVALID_CREDENTIALS", "message": "...", "status": 401}}
```
Deprecation: legacy auth endpoints deprecated at Phase 3 GA.

## Component Inventory

### COMP-001 — LoginPage (route `/login`)
Type: React page component. Auth required: No. Props: `onSuccess: () => void, redirectUrl?: string`. Calls POST `/auth/login`. Stores `AuthToken` via `AuthProvider`.

### COMP-002 — RegisterPage (route `/register`)
Type: React page component. Auth required: No. Props: `onSuccess: () => void, termsUrl: string`. Client-side password strength validation before POST `/auth/register`.

### COMP-003 — ProfilePage (route `/profile`)
Type: React page component. Auth required: Yes. Calls GET `/auth/me`; displays `UserProfile`.

### COMP-004 — AuthProvider
Type: React context provider. Props: `children: ReactNode`. Wraps app; manages `AuthToken` state; handles silent refresh via `TokenManager`; intercepts 401s; redirects unauthenticated users to `LoginPage`.

### COMP-005 — AuthService (backend orchestrator)
Type: Backend facade. Receives gateway requests; delegates to `PasswordHasher`, `TokenManager`, `UserRepo`. Exposes login, register, me, refresh, reset-request, reset-confirm.

### COMP-006 — TokenManager (backend)
Type: Token lifecycle service. Wraps `JwtService`. Issues/revokes tokens. Stores hashed refresh tokens in Redis with 7-day TTL. Distinguishes expired vs revoked.

### COMP-007 — PasswordHasher (backend)
Type: bcrypt abstraction. Cost factor 12. Supports hash and verify; abstraction permits future algorithm migration.

### Component Hierarchy (frontend)
```
App
└── AuthProvider
    ├── PublicRoutes { LoginPage, RegisterPage }
    └── ProtectedRoutes { ProfilePage }
```

### Backend Composition
`AuthService` → { `TokenManager` → `JwtService`, `PasswordHasher`, `UserRepo` (PostgreSQL) }

State stores: none server-side beyond Redis refresh token cache and PostgreSQL. Frontend state lives in `AuthProvider` context (in-memory `AuthToken`, current `UserProfile`).

## Testing Strategy

Test pyramid: 80% unit / 15% integration / 5% E2E.

| Level | Target | Tools | Focus |
|---|---|---|---|
| Unit | 80% | Jest, ts-jest | `AuthService`, `PasswordHasher`, `JwtService`, `TokenManager`, `UserProfile` validation |
| Integration | 15% | Supertest, testcontainers | API cycles, DB ops, Redis, full `AuthService`→`PasswordHasher`→DB flow |
| E2E | 5% | Playwright | Login/registration/refresh/full journey |

### TEST-001 — Login with valid credentials returns AuthToken (Unit)
Component: `AuthService`. Validates FR-AUTH-001. `AuthService.login()` calls `PasswordHasher.verify()`, then `TokenManager.issueTokens()`, returns valid `AuthToken`.

### TEST-002 — Login with invalid credentials returns error (Unit)
Component: `AuthService`. Validates FR-AUTH-001. Returns 401 when `PasswordHasher.verify()` returns false; no `AuthToken` issued.

### TEST-003 — Token refresh with valid refresh token (Unit)
Component: `TokenManager`. Validates FR-AUTH-003. Validates refresh token, revokes old, issues new pair via `JwtService`.

### TEST-004 — Registration persists UserProfile to database (Integration)
Scope: `AuthService` + PostgreSQL. Validates FR-AUTH-002. Full flow API → `PasswordHasher` → DB insert.

### TEST-005 — Expired refresh token rejected by TokenManager (Integration)
Scope: `TokenManager` + Redis. Validates FR-AUTH-003. Redis TTL expiration invalidates refresh tokens.

### TEST-006 — User registers and logs in (E2E)
Flow: `RegisterPage` → `LoginPage` → `ProfilePage`. Validates FR-AUTH-001 + FR-AUTH-002 end-to-end through `AuthProvider`.

### Test Environments
| Environment | Purpose | Data |
|---|---|---|
| Local | Developer testing | Docker Compose (PostgreSQL + Redis) |
| CI | Automated pipeline | testcontainers ephemeral DBs |
| Staging | Pre-production | Seeded test accounts, isolated |

## Migration and Rollout Plan

### MIG-001 — Phase 1: Internal Alpha
Duration: 1 week. Deploy `AuthService` to staging. auth-team + QA test all endpoints. `LoginPage`/`RegisterPage` behind flag `AUTH_NEW_LOGIN`. Exit: all FR-AUTH-001–005 pass manual testing; zero P0/P1 bugs.

### MIG-002 — Phase 2: Beta (10% traffic)
Duration: 2 weeks. Enable `AUTH_NEW_LOGIN` for 10%. Monitor `AuthService` latency, error rates, `TokenManager` Redis usage. Exit: p95 <200ms, error rate <0.1%, no Redis connection failures.

### MIG-003 — Phase 3: General Availability (100%)
Duration: 1 week. Remove `AUTH_NEW_LOGIN`. All users on new `AuthService`. Legacy deprecated. `AUTH_TOKEN_REFRESH` enabled. Exit: 99.9% uptime over 7 days; all dashboards green.

### MIG-004 — Feature flag AUTH_NEW_LOGIN
Purpose: Gates new `LoginPage` and `AuthService` login endpoint. Default: OFF. Cleanup: after Phase 3 GA. Owner: auth-team.

### MIG-005 — Feature flag AUTH_TOKEN_REFRESH
Purpose: Enables refresh token flow in `TokenManager`; when OFF, only access tokens issued. Default: OFF. Cleanup: Phase 3 + 2 weeks. Owner: auth-team.

### Rollback Procedure (sequential)
1. Disable `AUTH_NEW_LOGIN` to route traffic to legacy auth
2. Verify legacy login via smoke tests
3. Investigate `AuthService` root cause via structured logs + traces
4. If `UserProfile` data corruption detected, restore from last known-good backup
5. Notify auth-team + platform-team via incident channel
6. Post-mortem within 48 hours

### Rollback Criteria
Triggered if any: p95 >1000ms for >5 min; error rate >5% for >2 min; Redis failures >10/min; any `UserProfile` data loss or corruption.

## Operational Readiness

### OPS-001 — Runbook: AuthService down
Symptoms: 5xx on all `/auth/*`; `LoginPage`/`RegisterPage` error state.
Diagnosis: Check `AuthService` pod health in Kubernetes; PostgreSQL connectivity; `PasswordHasher`/`TokenManager` init logs.
Resolution: Restart pods; failover to PostgreSQL read replica; if Redis down, users must re-login.
Escalation: auth-team on-call → 15 min unresolved → platform-team.

### OPS-002 — Runbook: Token refresh failures
Symptoms: Unexpected logouts; `AuthProvider` redirect loop to `LoginPage`; `auth_token_refresh_total` error spike.
Diagnosis: Redis connectivity from `TokenManager`; `JwtService` signing key access; `AUTH_TOKEN_REFRESH` flag state.
Resolution: Scale Redis; remount secrets; enable flag if OFF.
Escalation: auth-team on-call → Redis cluster issue → platform-team.

### OPS-003 — On-Call Expectations
P1 acknowledge ≤15 min. 24/7 rotation (auth-team) first 2 weeks post-GA. Tooling: K8s dashboards, Grafana, Redis CLI, PostgreSQL admin. Escalation: on-call → test-lead → eng-manager → platform-team.

### OPS-004 — Capacity Plan: AuthService pods
Current: 3 replicas. Expected: 500 concurrent users. Scaling: HPA to 10 replicas at CPU >70%.

### OPS-005 — Capacity Plan: PostgreSQL connections
Current pool: 100. Avg concurrent: 50. Scaling: pool → 200 if wait time >50ms.

### OPS-006 — Capacity Plan: Redis memory
Current: 1 GB. Expected: ~100K refresh tokens (~50 MB). Scaling: → 2 GB if >70% utilized.

### OPS-007 — Observability
Structured logs for login success/failure, registration, refresh, password reset.
Prometheus metrics: `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter).
OpenTelemetry distributed tracing spanning `AuthService` → `PasswordHasher` / `TokenManager` → `JwtService`.
Alerts: login failure rate >20% over 5 min; p95 latency >500ms; Redis connection failures from `TokenManager`.
SOC2 audit log (12-month retention per PRD): user id, event type, timestamp, IP, outcome; queryable by date range + user.
