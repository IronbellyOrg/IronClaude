---
spec_source: "test-spec-user-auth.md"
complexity_score: 0.6
primary_persona: architect
---

# User Authentication Service – Comprehensive Project Roadmap

## Executive Summary

The User Authentication Service is a medium-complexity, security-critical identity system that unblocks the platform's Q2 2026 personalization roadmap and enables SOC2 compliance. The service introduces five core user-facing capabilities (FR-AUTH.1 through FR-AUTH.5) supported by seven non-functional requirements spanning performance, reliability, security, and compliance.

### Architectural Profile

**Key Complexity Drivers:**
1. **Stateless JWT architecture with refresh rotation** – Requires careful token lifecycle management and replay detection (FR-AUTH.3c)
2. **Security-critical password and token handling** – bcrypt (NFR-AUTH.3), RS256 signing (architectural constraint), no plain-text logging (NFR-AUTH.7)
3. **Compliance instrumentation** – SOC2 audit logging (NFR-AUTH.5) and GDPR consent (NFR-AUTH.4) must be wired into every auth event
4. **Component integration complexity** – Layered architecture (AuthService → TokenManager → JwtService) with multiple dispatch points

**Architectural Strengths:**
- Dependency injection enables unit testing in isolation
- Stateless design scales horizontally without session affinity
- Token rotation strategy provides defense-in-depth against token theft
- Database schema is straightforward (users + refresh_tokens tables)

**Critical Path:**
TokenManager implementation is a blocking dependency for login (FR-AUTH.1), token refresh (FR-AUTH.3), and password reset (FR-AUTH.5). All three features are blocked until TokenManager and JwtService are functional and integration-tested.

### Strategic Alignment

This roadmap aligns PRD phasing (Phase 1: login/registration/refresh; Phase 2: profile/password reset/audit) with architectural sequencing: foundation→component integration→endpoint delivery→compliance instrumentation.

Success hinges on **early security review** (Risk #5) and **compliance specification** (Open Question #5, #7, #9) before implementation begins.

---

## Phased Implementation Plan with Milestones

### Phase 1: Foundation & Core Authentication Flows (Sprints 1–3, 3 weeks)

**Business Outcome:** Users can register and log in with persistent session management across page refreshes (FR-AUTH.1, FR-AUTH.2, FR-AUTH.3).

#### 1.1 Infrastructure & Dependency Injection Foundation (Week 1)

**Milestone 1.1.1: Database Schema & Migrations**
- Create `users` table (id, email, display_name, password_hash, created_at, updated_at)
- Create `refresh_tokens` table (id, user_id, token_hash, expires_at, revoked_at, created_at)
- Create `audit_logs` table (id, user_id, event_type, timestamp, ip_address, outcome) — pre-provision for NFR-AUTH.5 (SOC2)
- Write down-migrations for rollback capability (architectural constraint)
- Execute schema validation against PostgreSQL 15+ (dependency #4)

**Dependencies:** Database access, migration tooling

**Acceptance Criteria:**
- Schema created and tested on PostgreSQL 15+
- Down-migrations execute without data loss
- Audit log schema supports all fields required by NFR-AUTH.5 (user_id, event_type, timestamp, ip_address, outcome)

**Architect Notes:**
- Pre-provision `audit_logs` in v1.0 schema even though audit event *dispatch* may be deferred (resolves Open Question #5 scope ambiguity)
- Use surrogate keys (id) for all tables; no natural keys
- Ensure refresh_token_hash is indexed for revocation lookups (perf requirement NFR-AUTH.1)

---

**Milestone 1.1.2: Configuration & Secrets Management**
- Define configuration schema: bcrypt cost factor (default 12), JWT algorithm (RS256), token TTLs (access 15min, refresh 7d), rate limit (5 per min per IP)
- Provision RSA key pair (public + private) for RS256 signing; store private key in secrets manager
- Load configuration from environment and policy document (SEC-POLICY-001 dependency #7)
- Implement configuration validation at startup (fail-fast principle)

**Dependencies:** Secrets manager access, SEC-POLICY-001 policy document

**Acceptance Criteria:**
- Configuration loads from environment variables
- RSA private key is never logged or exposed in error messages
- Configuration validation prevents deployment with invalid values (e.g., cost factor < 10)
- Cost factor is configurable without code changes (mitigates Risk #3)

**Architect Notes:**
- Make `JWT_ALGORITHM` configurable (not hardcoded RS256) to future-proof against algorithm migration
- Store bcrypt cost factor as a revisable configuration, not a constant, to support OWASP recommendation reviews

---

**Milestone 1.1.3: Dependency Injection Container**
- Create injectable interface definitions: `PasswordHasher`, `JwtService`, `TokenManager`, `UserRepository`, `RefreshTokenRepository`
- Implement DI container (e.g., TypeScript IoC library or custom factory pattern) that wires all components
- Register all service implementations (concrete PasswordHasher, JwtService, etc.)
- Ensure all services are independently testable (no static initialization)

**Dependencies:** DI framework selection

**Acceptance Criteria:**
- All core services are injectable interfaces
- Container resolves and initializes all dependencies without circular references
- Unit tests can mock any service without instantiating the full container
- Startup logs show successful DI initialization

**Architect Notes:**
- Use constructor injection, not property injection, to make dependencies explicit
- Avoid service locator pattern; inject container into limited bootstrap code only

---

#### 1.2 Core Security Components (Week 1–2)

**Milestone 1.2.1: PasswordHasher Implementation (Password-Hasher.ts)**
- Implement password hashing using bcrypt library (dependency #2) with configurable cost factor
- Implement password verification (comparison-safe to prevent timing attacks)
- Enforce password policy at hash time: validate 8-char min, 1 uppercase, 1 lowercase, 1 digit (FR-AUTH.2c)
- Add benchmark test confirming ~250ms hash time per NFR-AUTH.3
- Add unit tests for edge cases: empty password, oversized password, special characters

**Dependencies:** `bcrypt` NPM package (dependency #2), password policy from SEC-POLICY-001

**Acceptance Criteria:**
- All passwords hashed with bcrypt cost 12 (configurable)
- Password never appears in logs, error messages, or test output
- Hash operation takes ~250ms (NFR-AUTH.3 benchmark test passes)
- Verification is constant-time (no timing-attack vulnerability)
- Policy validation (8-char, uppercase, lowercase, digit) enforced before hashing

**Architect Notes:**
- Use bcrypt.hash() and bcrypt.compare() directly; do not re-implement
- Add logging hook for failed policy validation (helpful for debugging) but never log the password itself
- Unit test should verify `cost` parameter is passed correctly

---

**Milestone 1.2.2: JwtService Implementation (Jwt-Service.ts)**
- Implement JWT signing using `jsonwebtoken` library (dependency #1) with RS256 algorithm
- Implement JWT verification with public key
- Define JWT payload schema: `{ sub: user_id, iat, exp, type: "access" | "refresh" }`
- Support configurable token TTLs from configuration (15min for access, 7d for refresh)
- Add unit tests: valid token verification, expired token rejection, tampered payload rejection, algorithm mismatch rejection

**Dependencies:** `jsonwebtoken` NPM package (dependency #1), RSA key pair from Milestone 1.1.2

**Acceptance Criteria:**
- JwtService signs tokens with RS256 and private key
- Verification succeeds for valid tokens, fails for expired/tampered/misaligned tokens
- Token expiration is enforced strictly (no grace period)
- Payload includes user ID (sub), issue time (iat), expiration (exp), and token type (type)
- No logging of token contents in error messages

**Architect Notes:**
- Store RSA public key in environment for verification; private key in secrets manager
- Token type field (access vs refresh) is critical for TokenManager dispatch (see 1.2.3)
- Unit tests should cover algorithm confusion attacks (e.g., HS256 with public key)

---

**Milestone 1.2.3: TokenManager Implementation (Token-Manager.ts)**

**INTEGRATION POINT: Token Dispatch Registry**
- **Artifact Name:** `TokenTypeStrategy` interface + registry
- **Wired Components:** 
  - `AccessTokenStrategy`: 15min TTL, no refresh capability, for stateless API calls
  - `RefreshTokenStrategy`: 7d TTL, rotation on use, triggers token hash storage and revocation checks
- **Owning Phase:** Phase 1, Milestone 1.2.3 (this milestone)
- **Consumed By:** FR-AUTH.1 (login), FR-AUTH.3 (refresh), FR-AUTH.5 (logout invalidation)

**Implementation:**
- Implement `TokenTypeStrategy` interface: `issue(userId, ttl)`, `verify(token)`, `revoke(token)`
- Create `AccessTokenStrategy` and `RefreshTokenStrategy` implementations
- Register both in a dispatcher keyed by token type
- Implement `TokenManager.issueTokenPair(userId)` → returns {accessToken, refreshToken}
- Implement `TokenManager.verifyAccessToken(token)` → userId or throws 401
- Implement `TokenManager.rotateRefreshToken(oldToken)` → new {accessToken, refreshToken} or throws 401

**Refresh Token Rotation & Replay Detection (FR-AUTH.3c):**
- On `rotateRefreshToken()`: 
  1. Verify oldToken is valid and not previously rotated
  2. Check refresh_token_hash in database for revocation status (replayed tokens have `revoked_at` set)
  3. If `revoked_at` is set and differs from this rotation, all user tokens are immediately invalidated (replay detected)
  4. If valid, hash newToken and store in database with old token ID marked `revoked_at`
  5. Return new token pair

**Dependencies:** JwtService (Milestone 1.2.2), RefreshTokenRepository, configuration

**Acceptance Criteria:**
- `issueTokenPair()` returns opaque string tokens (no sensitive data in JWT payload visible to client)
- Access tokens are short-lived (15min); refresh tokens are long-lived (7d)
- Refresh token rotation increments a version/chain; old token hash is stored with revocation timestamp
- Replay attack detection: reusing an already-rotated token invalidates all user sessions
- Unit tests verify dispatch registry routes access vs refresh strategies correctly
- Integration tests verify token expiration and rotation end-to-end with database

**Architect Notes:**
- Refresh token hash is stored, not the raw token (one-way storage, cannot be leaked to expose active tokens)
- Dispatch registry is extensible (future MFA tokens, API key tokens can be added to registry)
- Rotation is atomic: failure at any step leaves database state unchanged

---

#### 1.3 User Repository & Authentication Service (Week 2)

**Milestone 1.3.1: UserRepository Implementation (User-Repository.ts)**
- Implement CRUD for User table
- Implement `findByEmail()`, `findById()`, `create()`, `updatePassword()`
- Add unique constraint validation on email (FR-AUTH.2b: duplicate email returns 409)
- All queries parameterized (SQL injection prevention)

**Acceptance Criteria:**
- All queries use prepared statements (no string concatenation)
- Duplicate email insert raises ConstraintError (mapped to 409 by controller)
- `create()` returns created user record without password_hash
- Database transactions ensure atomicity on user creation

**Architect Notes:**
- User password_hash field is never selected in queries except for login verification
- Created_at timestamp is set by database, not application

---

**Milestone 1.3.2: AuthService Implementation (Auth-Service.ts)**
- Orchestrate registration (FR-AUTH.2): validate input, hash password, create user record, issue token pair
- Orchestrate login (FR-AUTH.1): lookup user, verify password, issue token pair, enforce rate limit (FR-AUTH.1d), return 401 for invalid creds (no enumeration), return 403 for locked account
- Orchestrate logout: invalidate refresh token (set revoked_at)
- Log authentication events to audit_logs table (user_id, event_type, timestamp, ip_address, outcome)

**INTEGRATION POINT: Error Code Dispatch**
- **Artifact Name:** `AuthErrorRegistry` map
- **Wired Components:**
  - `InvalidCredentials` → 401 "Invalid email or password"
  - `UserAlreadyExists` → 409 "Email already registered"
  - `AccountLocked` → 403 "Account is locked"
  - `RateLimitExceeded` → 429 "Too many login attempts"
  - `InvalidToken` → 401 "Token expired or invalid"
- **Owning Phase:** Phase 1, Milestone 1.3.2 (this milestone)
- **Consumed By:** API endpoint layer, client error handling

**Audit Logging:**
- Log all auth events: `register`, `login`, `logout`, `refresh_token`, `password_reset`
- Schema: user_id, event_type, ip_address, outcome (success/failure), timestamp
- Pre-populate for SOC2 (NFR-AUTH.5) even if admin audit log retrieval is deferred

**Rate Limiting (FR-AUTH.1d):**
- Implement in-memory or Redis-backed rate limiter: 5 attempts per minute per IP
- On rate limit exceeded: return 429, log event, optionally set account lockout flag for manual admin review (deferred scope per Open Question #3)

**Dependencies:** UserRepository, TokenManager, PasswordHasher, audit log sink

**Acceptance Criteria:**
- Registration validates email format, password policy, and email uniqueness before hashing
- Login is constant-time (no information leak on whether email exists)
- Failed login attempts are counted and rate-limited per IP
- All auth events logged with required fields (user_id, event_type, timestamp, ip_address, outcome)
- Audit log tests verify logging happens for both success and failure cases
- Error codes are registered in AuthErrorRegistry; controllers use registry to map exceptions to HTTP status

---

#### 1.4 API Endpoints & Middleware (Week 2–3)

**Milestone 1.4.1: Authentication Middleware (Auth-Middleware.ts)**

**INTEGRATION POINT: Middleware Chain**
- **Artifact Name:** `MiddlewareChain` (request pipeline)
- **Wired Components:**
  - AuthMiddleware (extract Bearer token, verify with TokenManager, attach user context)
  - RateLimitMiddleware (enforce 5 per minute per IP on login endpoint)
  - AuditLoggingMiddleware (log all auth endpoint calls with IP, user_id, outcome)
- **Owning Phase:** Phase 1, Milestone 1.4.1 (this milestone)
- **Consumed By:** All endpoints in Phase 1 and Phase 2

**Implementation:**
- Extract JWT from Authorization header (Bearer token)
- Call TokenManager.verifyAccessToken()
- On success: attach user context (user_id, email) to request object
- On failure: return 401 with error from AuthErrorRegistry
- On missing token: return 401 (required for profile, optional for public endpoints)

**Dependencies:** TokenManager

**Acceptance Criteria:**
- Middleware extracts Bearer token from Authorization header
- Verification failures return 401 with standardized error
- User context is available to downstream handlers
- Tests verify both success and failure paths

---

**Milestone 1.4.2: POST /register (User Registration Endpoint)**
- **Implements:** FR-AUTH.2
- **Input:** { email, password, display_name }
- **Validation:**
  - Email format (RFC 5322 or simplified)
  - Password policy (8-char min, 1 uppercase, 1 lowercase, 1 digit) — FR-AUTH.2c
  - Display name non-empty
- **Processing:**
  - Call AuthService.register()
  - On success: return 201 with user profile (no password_hash) and tokens
  - On duplicate email: return 409 from AuthErrorRegistry (FR-AUTH.2b)
  - On policy failure: return 400 with unmet requirements (inline validation hint)
- **Rate Limit:** Optional (deferred to risk mitigation if registration spam becomes issue)

**Acceptance Criteria:**
- Valid registration data creates user and returns 201 with access + refresh tokens
- Duplicate email returns 409
- Invalid password policy returns 400 with policy hint (non-blocking for user)
- User password_hash never included in response
- Audit log entry created for registration event

---

**Milestone 1.4.3: POST /login (User Login Endpoint)**
- **Implements:** FR-AUTH.1
- **Input:** { email, password }
- **Processing:**
  - Call AuthService.login()
  - On success: return 200 with tokens (access + refresh) — FR-AUTH.1a
  - On invalid credentials: return 401 generic error (no user enumeration) — FR-AUTH.1b
  - On locked account: return 403 from AuthErrorRegistry (FR-AUTH.1c, deferred if lockout is not implemented in v1.0)
  - Enforce rate limit: 5 per minute per IP — FR-AUTH.1d
- **Token Strategy:**
  - Access token: httpOnly cookie or Authorization header (product decision pending)
  - Refresh token: httpOnly cookie with Secure + SameSite=Strict flags

**Acceptance Criteria:**
- Valid credentials return 200 with tokens in < 200ms p95 (NFR-AUTH.1)
- Invalid credentials return 401 without revealing email existence
- Rate limit enforced at 5 per minute per IP; return 429 on exceeded
- Tokens are issued via TokenManager and include correct TTLs

---

**Milestone 1.4.4: POST /logout (User Logout Endpoint)**
- **Implements:** FR-AUTH.0 (logout is not in spec but is in PRD; open question #10)
- **Requires:** Authenticated (bearer token or cookie)
- **Processing:**
  - Extract refresh token from request
  - Call AuthService.logout() → invalidates refresh token (sets revoked_at in database)
  - Return 204 (No Content) or 200 with success message
- **Note:** This endpoint resolves Open Question #10 (PRD has logout user story, spec does not). **Recommend including logout in v1.0 scope** to match user story AUTH-E1.

**Acceptance Criteria:**
- Authenticated users can logout
- Refresh token is invalidated in database
- Subsequent attempts to use invalidated token return 401
- Audit log entry created for logout event

---

#### 1.5 Integration Testing & Component Wiring Validation (Week 3)

**Milestone 1.5.1: Integration Test Suite (Test Phase 1)**
- End-to-end tests: register → login → verify token → logout
- Token expiration tests: access token expires after 15min; refresh works within 7d window
- Rate limiting tests: 6th login attempt within 1min returns 429
- Duplicate email handling: second registration with same email returns 409
- Audit logging validation: all events logged with correct fields
- Token rotation validation: rotate refresh token, old token becomes invalid

**Dependencies:** Test database (PostgreSQL), test fixtures

**Acceptance Criteria:**
- All Phase 1 user stories (AUTH-E1 partial: register, login, logout) pass integration tests
- Token expiration and rotation are validated end-to-end
- Audit logs are created and queryable for all events
- No sensitive data (password, token) appears in logs or error messages

---

**Milestone 1.5.2: Security Review (Checkpoint)**
- Code review by security engineer: password hashing, JWT signing, token storage, rate limiting
- Check: no hard-coded secrets, no logging of sensitive data, no SQL injection vectors
- Verify: bcrypt cost factor, RS256 key handling, constant-time comparisons
- Approve proceeding to Phase 2

**Dependencies:** Security engineer availability

**Acceptance Criteria:**
- No critical or high-severity security findings
- Password handling passes security review
- Token management passes security review
- Secrets management approach approved

---

**Phase 1 Completion Criteria:**
- All Milestones 1.1–1.5 complete
- FR-AUTH.1, FR-AUTH.2, FR-AUTH.3a, FR-AUTH.3b passing acceptance criteria
- Token dispatch registry functional (access vs refresh strategies wired)
- Error code registry functional (error mapping to HTTP status codes)
- Middleware chain functional (auth middleware in request pipeline)
- Integration tests passing
- Security review passed
- **Estimated Effort:** 3 weeks (18 engineer-days)

---

### Phase 2: Session Persistence, Profile, Password Reset & Compliance Instrumentation (Sprints 4–6, 3 weeks)

**Business Outcome:** Users can maintain persistent sessions, view profiles, self-serve password reset, and system is audit-compliant for SOC2 (FR-AUTH.3c, FR-AUTH.4, FR-AUTH.5, NFR-AUTH.5).

#### 2.1 Session Persistence & Token Refresh (Week 4)

**Milestone 2.1.1: POST /refresh (Token Refresh Endpoint)**
- **Implements:** FR-AUTH.3
- **Input:** { refresh_token } (from httpOnly cookie or body, depending on Phase 1 token storage decision)
- **Processing:**
  - Call TokenManager.rotateRefreshToken(refresh_token)
  - On success: return 200 with new access + refresh tokens — FR-AUTH.3a
  - On expired refresh: return 401 (require re-login) — FR-AUTH.3b
  - On replayed/revoked refresh: invalidate all user tokens (replay detection) — FR-AUTH.3c
  - Ensure refresh token hash is stored in database — FR-AUTH.3d
- **Rate Limit:** None (users should be able to refresh at will)

**Acceptance Criteria:**
- Valid refresh token returns new token pair
- Expired token returns 401 with "Token expired" message
- Replayed token (previously rotated) triggers user-wide token invalidation
- Refresh token hash is stored in database (not plain token)
- Audit log entry created for token refresh

**Architect Notes:**
- Refresh endpoint is called silently by client on access token expiration (transparent to user)
- Rotation atomic: if any step fails, database state is unchanged

---

**Milestone 2.1.2: Client-Side Token Persistence Strategy**
- **Architectural Decision:** How are tokens stored on client?
  - **Option A:** Access token in memory, refresh token in httpOnly cookie
  - **Option B:** Both tokens in httpOnly cookies
  - **Constraint:** Spec says "Access token in memory (client-side), refresh token in httpOnly cookie. No localStorage or sessionStorage for tokens."
- **Implementation:** Align frontend token storage with architectural constraint
- **Testing:** Verify session persistence across page refresh without automatic logout

**Dependencies:** Frontend framework decision

**Acceptance Criteria:**
- Tokens are not stored in localStorage or sessionStorage
- Access token is in memory (lost on page refresh, requires silent refresh from refresh token)
- Refresh token persists in httpOnly cookie with Secure + SameSite=Strict
- Silent refresh is transparent to user (no login prompt on page refresh within 7d window)

---

#### 2.2 User Profile & Data Retrieval (Week 4)

**Milestone 2.2.1: GET /profile (User Profile Endpoint)**
- **Implements:** FR-AUTH.4
- **Requires:** Authenticated (bearer token)
- **Processing:**
  - Call TokenManager.verifyAccessToken()
  - Lookup user by ID from token.sub
  - Return user profile (id, email, display_name, created_at) — FR-AUTH.4a
  - Verify password_hash and refresh_token_hash are never included — FR-AUTH.4c
- **Response:** 200 with profile object

**Acceptance Criteria:**
- Authenticated users can retrieve their profile
- Profile includes id, email, display_name, created_at
- Password_hash is never included in response
- Expired or invalid token returns 401 — FR-AUTH.4b
- Audit log entry created for profile access

---

#### 2.3 Password Reset Flow (Week 4–5)

**Milestone 2.3.1: Password Reset Token Service (Password-Reset-Service.ts)**

**INTEGRATION POINT: Reset Token Dispatch Registry**
- **Artifact Name:** `ResetTokenGenerator` and `ResetTokenValidator`
- **Wired Components:**
  - Email-based reset: generate 1-hour TTL token, dispatch email
  - SMS-based reset: (deferred to v2.0)
- **Owning Phase:** Phase 2, Milestone 2.3.1 (this milestone)
- **Consumed By:** FR-AUTH.5 (password reset)

**Implementation:**
- Generate cryptographically secure reset token (base64url-encoded random bytes)
- Store token hash (not plain) in a new `password_reset_tokens` table with TTL and user_id
- Create `ResetTokenValidator`: verify token is valid, not expired, not already used
- Create `ResetTokenGenerator`: create token, store hash, return plain token for email dispatch

**Dependencies:** Email service (SendGrid or equivalent, dependency #3)

**Acceptance Criteria:**
- Reset token is generated and hashed before storage
- Token is valid for 1 hour (configurable)
- Token can be validated against hash in database
- Expired or invalid tokens are rejected with 400 "Invalid or expired reset token"

---

**Milestone 2.3.2: POST /password-reset/request (Request Password Reset)**
- **Implements:** FR-AUTH.5a
- **Input:** { email }
- **Processing:**
  - Do NOT validate whether email exists (prevents user enumeration)
  - If email exists: generate reset token, store hash, dispatch email
  - Always return 200 success response (even if email not found)
  - Email should be delivered within 60 seconds
- **Email Content:** Include reset link with 1-hour TTL token
- **Rate Limit:** 3 per hour per email (prevent spam)

**Acceptance Criteria:**
- Valid email receives reset link within 60 seconds
- Non-existent email returns success (no enumeration)
- Reset link expires after 1 hour
- Rate limit: 3 per hour per email (returns 429 on exceeded)

---

**Milestone 2.3.3: POST /password-reset/confirm (Set New Password with Reset Token)**
- **Implements:** FR-AUTH.5b, FR-AUTH.5d
- **Input:** { reset_token, new_password }
- **Processing:**
  - Validate reset_token (check against hash, TTL, not already used)
  - On invalid: return 400 "Invalid or expired reset token" — FR-AUTH.5c
  - On valid: hash new password, update user record, invalidate all refresh tokens for user (all sessions end)
  - Mark reset token as used (consumed)
  - Return 200 with success message (optional: auto-login user)
- **Audit Logging:** Log password reset event with user_id, timestamp, outcome

**Acceptance Criteria:**
- Valid reset token allows setting new password
- Expired or invalid token returns 400
- All existing sessions (refresh tokens) are invalidated after password reset — FR-AUTH.5d
- Reset token cannot be reused (marked consumed)
- Audit log entry created for password reset event

---

#### 2.4 Audit Logging & Compliance (Week 5–6)

**Milestone 2.4.1: Audit Log Sink & Event Dispatch**

**INTEGRATION POINT: Audit Event Registry**
- **Artifact Name:** `AuditEventType` enum + `AuditEventDispatcher`
- **Wired Components:**
  - `register`: user registration
  - `login`: successful login
  - `login_failed`: failed login attempt
  - `logout`: user logout
  - `refresh_token`: token refresh
  - `password_reset_requested`: password reset request
  - `password_reset_confirmed`: password reset completed
  - `profile_accessed`: profile retrieval
  - (Future) `account_locked`: account lockout (deferred)
- **Owning Phase:** Phase 2, Milestone 2.4.1 (this milestone)
- **Consumed By:** All endpoints (Phase 1 + Phase 2)

**Implementation:**
- Define `AuditEvent` record: user_id, event_type, ip_address, outcome, timestamp
- Create `AuditEventDispatcher`: registers event types, dispatches events to sink
- Implement sink: writes to `audit_logs` table (pre-provisioned in Phase 1, Milestone 1.1.1)
- Make dispatcher injectable so all services can log events
- Ensure atomic logging: if audit write fails, transaction rolls back (fail-secure)

**Dependencies:** Audit log table (Phase 1), configuration

**Acceptance Criteria:**
- All auth event types registered in dispatcher
- All endpoints (register, login, logout, refresh, password-reset) emit audit events
- Audit logs include user_id, event_type, ip_address, outcome, timestamp
- Logging failures trigger error handling (alert, alert monitoring)

---

**Milestone 2.4.2: Audit Log Retention & Query Interface**
- Implement query interface for audit logs: filter by user_id, date range, event_type
- Set database retention policy: 12-month minimum (NFR-AUTH.5)
- Add retention validation test: confirm logs older than 12 months are archived/deleted per policy

**Acceptance Criteria:**
- Audit logs queryable by user_id, date range, event_type
- Logs retained for minimum 12 months
- Database retention policy enforced

**Architect Notes:**
- Query interface is intentionally deferrable to Phase 2, Milestone 2.4.2 (admin audit log access is deferred per Open Question #9)
- Pre-provisioning the table in Phase 1 ensures events are captured immediately upon deployment

---

**Milestone 2.4.3: GDPR Consent Capture (NFR-AUTH.4)**
- **Scope Clarification:** PRD specifies consent required at registration (NFR-AUTH.4); spec does not mention this. **Recommend including in v1.0.**
- **Implementation:**
  - Add `consents` table: user_id, consent_type, timestamp, version
  - Registration flow: present GDPR data processing consent checkbox
  - Only proceed to account creation if consent is checked
  - Store consent record with timestamp (auditable proof of consent)
- **Testing:** Verify consent cannot be bypassed; record is created for all registered users

**Acceptance Criteria:**
- Consent checkbox presented at registration
- Registration blocked if consent is not checked
- Consent record stored with timestamp for all registered users
- Test verifies no users can be created without consent record

---

#### 2.5 Compliance Validation & E2E Testing (Week 6)

**Milestone 2.5.1: SOC2 Compliance Validation (NFR-AUTH.5)**
- Audit log field completeness: all events include user_id, event_type, timestamp, ip_address, outcome
- Retention policy: logs retained for 12+ months
- Log access control: only authorized personnel can query logs (deferred if admin interface deferred)
- Audit trail sample: generate sample logs showing complete lifecycle (register → login → refresh → logout)

**Dependencies:** Compliance review, audit template

**Acceptance Criteria:**
- Audit logs meet SOC2 control requirements
- 12-month retention policy is enforced
- Compliance checklist signed off by security/legal

---

**Milestone 2.5.2: NIST SP 800-63B Validation (NFR-AUTH.7)**
- Verify: passwords hashed with one-way adaptive hashing (bcrypt) — ✓ (Phase 1)
- Verify: raw passwords never persisted or logged — ✓ (audit code)
- Verify: password comparison is constant-time — ✓ (bcrypt.compare)

**Acceptance Criteria:**
- Security review confirms NIST compliance
- No raw password leaks in logs or error messages
- Hash implementation is approved by security team

---

**Milestone 2.5.3: E2E Test Suite (Phase 2)**
- End-to-end test: register → login → refresh token → access profile → password reset flow
- Load test: NFR-AUTH.1 validation (< 200ms p95 under 500 concurrent requests)
- Availability test: 99.9% uptime SLO (health check monitoring setup)
- Audit trail test: all events logged and queryable

**Dependencies:** Load testing tool (k6), monitoring infrastructure

**Acceptance Criteria:**
- All Phase 2 user stories passing E2E tests
- Performance: login < 200ms p95, 500 concurrent requests
- Availability: uptime monitoring configured, SLO tracking
- Audit logs complete and queryable

---

**Phase 2 Completion Criteria:**
- All Milestones 2.1–2.5 complete
- FR-AUTH.3, FR-AUTH.4, FR-AUTH.5 passing acceptance criteria
- Token dispatch registry extended (if needed)
- Error registry complete (error handling fully mapped)
- Audit event registry functional (all auth events logged)
- GDPR consent (NFR-AUTH.4) implemented
- SOC2 audit logging (NFR-AUTH.5) validated
- NIST compliance (NFR-AUTH.7) verified
- E2E tests passing
- Load testing validated (NFR-AUTH.1: < 200ms p95)
- **Estimated Effort:** 3 weeks (18 engineer-days)

---

## Risk Assessment and Mitigation Strategies

### Risk Inventory

| # | Risk | Severity | Probability | Impact | Mitigation Strategy | Owner | Validation |
|---|------|----------|-------------|--------|---------------------|-------|-----------|
| 1 | JWT private key compromise allows forged tokens | High | Low | Attacker can forge any token; all sessions compromised | RS256 asymmetric keys; store private key in secrets manager; implement key rotation every 90 days; audit key access logs | Security Engineer | Annual key rotation ceremony; secrets audit log review |
| 2 | Refresh token replay attack after token theft | High | Medium | Attacker reuses stolen refresh token; user's sessions are compromised | Refresh token rotation with replay detection (FR-AUTH.3c); revoke all user tokens on suspicious reuse; store token hash (not plain) | Backend Lead | Integration test: replayed token invalidates all sessions |
| 3 | bcrypt cost factor insufficient for future hardware | Medium | Low | Hashing becomes feasible to brute-force within months; passwords no longer secure | Make cost factor configurable; review annually against OWASP recommendations; migration path to Argon2id (v2.0) | Security Engineer | Annual review cycle; config audit |
| 4 | Low registration adoption due to poor UX | High | Medium | Registration conversion < 60%; personalization roadmap blocked | Usability testing with real users before launch (target: 5+ users); iterate based on funnel data; inline validation feedback | Product Manager | Funnel analytics; usability testing report |
| 5 | Security breach from implementation flaws | Critical | Low | Credential theft, token forgery, user account takeover | Dedicated security review (Phase 1, Milestone 1.5.2); penetration testing before production; code review by security engineer | Security Engineer | Security review checklist; pen test report |
| 6 | Compliance failure from incomplete audit logging | High | Medium | SOC2 audit failed; non-compliant event logging leaves no trace of incidents | Define log requirements early (Phase 1, Milestone 1.1.1); validate against SOC2 controls in QA (Phase 2, Milestone 2.4.1); compliance review checkpoint | Compliance Officer | SOC2 audit readiness checklist |
| 7 | Email delivery failures blocking password reset | Medium | Low | Users cannot recover passwords; support tickets increase; user churn | Delivery monitoring and alerting (CloudWatch, PagerDuty); fallback support channel; retry logic with exponential backoff; test email delivery in staging | DevOps | Email delivery SLA monitoring; failover testing |

---

### Risk Mitigation Timeline

| Checkpoint | Actions | Owner | When |
|-----------|---------|-------|------|
| **Pre-implementation** | Security review of architecture; define audit logging schema; finalize password/token policies (SEC-POLICY-001) | Security Engineer, Compliance Officer | Before Phase 1, Week 1 |
| **Phase 1, Week 3** | Code review for password hashing, JWT signing, secrets management; security sign-off on TokenManager implementation | Security Engineer | End of Phase 1 |
| **Phase 1, Milestone 1.5.2** | Dedicated security review: no hard-coded secrets, no logging of sensitive data, constant-time comparisons, bcrypt cost factor verified | Security Engineer | Week 3, Phase 1 |
| **Phase 2, Week 5** | Compliance review of audit logging completeness; SOC2 control validation | Compliance Officer | Mid Phase 2 |
| **Pre-production** | Penetration testing; load testing (validate NFR-AUTH.1: < 200ms p95); email delivery failover testing | Security Engineer, QA | After Phase 2 |

---

## Resource Requirements and Dependencies

### Human Resources

| Role | FTE | Duration | Responsibilities | Notes |
|------|-----|----------|------------------|-------|
| **Backend Engineer (Lead)** | 1.0 | 6 weeks | Implement core services (AuthService, TokenManager, JwtService, PasswordHasher), API endpoints, token dispatch registry, error registry, middleware chain, integration tests | Critical path; security-sensitive; deep expertise required |
| **Backend Engineer (Support)** | 0.5 | 6 weeks | API endpoints (register, login, refresh, profile), password reset flow, unit tests, documentation | Can parallelize endpoint work after core services are ready |
| **Security Engineer** | 0.3 | 6 weeks | Security architecture review (Phase 1, Milestone 1.5.2); code review for password hashing, JWT signing, secrets management; penetration testing scoping | Pre-implementation + Phase 1 review + pre-production testing |
| **QA Engineer** | 0.5 | 6 weeks | Integration and E2E test suite, performance/load testing (NFR-AUTH.1), audit log validation, compliance testing | Can start test planning in Week 1 and parallelize test writing after Phase 1 APIs available |
| **DevOps / Infrastructure** | 0.2 | 6 weeks | Database provisioning (PostgreSQL 15+), secrets manager setup, email delivery service setup (SendGrid), monitoring/alerting (CloudWatch, PagerDuty), deployment pipeline | Needed for dependency setup (Phase 1, Week 1) and production deployment |
| **Compliance / Legal** | 0.1 | 6 weeks | GDPR consent requirements (NFR-AUTH.4), SOC2 audit readiness, audit log retention policy | Minimal time; checkpoint reviews at Phase 2, Week 5 |
| **Product Manager** | 0.2 | 6 weeks | Scope clarification (open questions), phasing prioritization, success metrics tracking, funnel analytics | Addresses Open Questions #2, #3, #4, #7; post-launch metric monitoring |

**Total Allocation:** ~2.8 FTE over 6 weeks (16.8 engineer-weeks)

---

### Technical Dependencies

| Dependency | Type | Status | Impact | Mitigation |
|-----------|------|--------|--------|-----------|
| `jsonwebtoken` NPM package (dependency #1) | Library | Stable | Required for JWT signing/verification | Vendor-lock acceptable; pin version; monitor for security updates |
| `bcrypt` NPM package (dependency #2) | Library | Stable | Required for password hashing | Vendor-lock acceptable; pin version; monitor for security updates |
| Email service (SendGrid or equivalent, dependency #3) | External Service | Must procure | Required for password reset (FR-AUTH.5); blocks phase 2 | Procure and test in Phase 1, Week 1; set up API credentials in Phase 1, Milestone 1.1.2 |
| PostgreSQL 15+ (dependency #4) | Infrastructure | Must provision | Required for user + refresh_token + audit_logs tables | Provision in Phase 1, Week 1; ensure high-availability replication and automated backups |
| RSA key pair + secrets manager (dependency #5) | Infrastructure | Must procure | Required for RS256 JWT signing; stores private key | Generate in Phase 1, Week 1; use AWS Secrets Manager, HashiCorp Vault, or equivalent; set up key rotation process |
| Frontend routing framework (dependency #6) | Internal | Assumed in place | Required for auth pages (login, register, reset forms) | Confirm availability before Phase 1; may require frontend feature work (out of scope, engineering will coordinate) |
| Security policy (SEC-POLICY-001, dependency #7) | Policy Document | Must define | Required for password policy, token TTL, bcrypt cost factor, audit logging requirements | Finalize SEC-POLICY-001 before Phase 1, Week 1; unblock engineering with explicit values |

---

### External Service SLAs

| Service | SLA Target | Monitoring | Alerting |
|---------|-----------|-----------|----------|
| Email delivery (password reset) | 99.9% delivery within 60s | CloudWatch metrics from SendGrid API | PagerDuty alert on delivery failures > 5% per hour |
| PostgreSQL availability | 99.9% (managed RDS or equivalent) | Health checks; failover monitoring | PagerDuty alert on replica lag > 1s or failover events |
| Secrets manager (RSA key storage) | 99.99% availability | API response time monitoring | PagerDuty alert on key retrieval failures |

---

### Critical Path

The critical path is: **TokenManager → AuthService → API Endpoints**

1. **TokenManager implementation (Milestone 1.2.3)** is a blocker for:
   - AuthService.login() (Milestone 1.3.2)
   - POST /register endpoint (Milestone 1.4.2)
   - POST /login endpoint (Milestone 1.4.3)
   - POST /refresh endpoint (Milestone 2.1.1)

2. **AuthService implementation (Milestone 1.3.2)** is a blocker for:
   - All API endpoints

3. **Security review (Milestone 1.5.2)** is a checkpoint before Phase 2 begins

**Recommendation:** Assign Backend Engineer (Lead) to TokenManager + AuthService; assign Backend Engineer (Support) to API endpoints in parallel. Security Engineer reviews concurrently to identify issues early.

---

## Success Criteria and Validation Approach

### Functional Validation

| Requirement ID | Success Criterion | Validation Method | Phase | Owner |
|---|---|---|---|---|
| FR-AUTH.1 | Valid email + password returns 200 with tokens (access 15min, refresh 7d); Invalid creds return 401 (generic); Locked account returns 403; Rate limit 5/min/IP enforced | Integration test: valid/invalid/locked/rate-limited scenarios | Phase 1 | QA |
| FR-AUTH.1a | Access token has 15min TTL; Refresh token has 7d TTL | Token inspection test: decode JWT, verify exp claim | Phase 1 | QA |
| FR-AUTH.1b | Invalid credentials return 401 without revealing email status | Negative test: compare error messages for valid vs invalid email; no enumeration | Phase 1 | QA |
| FR-AUTH.1c | Locked account returns 403 | Conditional: if lockout implemented; else defer to v1.1 | Phase 1 | QA |
| FR-AUTH.1d | Rate limit: 5 attempts per minute per IP; 6th returns 429 | Load test: 6 login requests within 60s from same IP | Phase 1 | QA |
| FR-AUTH.2 | Valid registration creates user; Duplicate email returns 409; Password policy enforced (8-char, 1 upper, 1 lower, 1 digit); Email format validated | Registration test: valid/duplicate/invalid-policy/invalid-email scenarios | Phase 1 | QA |
| FR-AUTH.2a | Valid data returns 201 with user profile (no password_hash) | Integration test: POST /register with valid input | Phase 1 | QA |
| FR-AUTH.2b | Duplicate email returns 409 | Negative test: register twice with same email | Phase 1 | QA |
| FR-AUTH.2c | Password policy enforced: 8-char, 1 upper, 1 lower, 1 digit | Unit test: PasswordHasher policy validation | Phase 1 | QA |
| FR-AUTH.2d | Email format validated | Unit test: email regex or RFC 5322 validator | Phase 1 | QA |
| FR-AUTH.3 | Valid refresh token returns new access + refresh tokens (rotated); Expired refresh returns 401; Replayed refresh invalidates all user tokens; Refresh token hash stored in database | Integration test: valid/expired/replayed token scenarios; database audit | Phase 2 | QA |
| FR-AUTH.3a | Valid refresh returns new access + refresh tokens | Integration test: POST /refresh with valid token | Phase 2 | QA |
| FR-AUTH.3b | Expired refresh returns 401 | Integration test: wait for token expiry, attempt refresh | Phase 2 | QA |
| FR-AUTH.3c | Replayed (previously-rotated) refresh invalidates all user tokens | Integration test: rotate token, attempt reuse; verify all user tokens are revoked | Phase 2 | QA |
| FR-AUTH.3d | Refresh token hash stored in database (not plain token) | Database audit: query refresh_tokens table, verify token_hash column contains hash (not plain token) | Phase 2 | QA |
| FR-AUTH.4 | Authenticated user retrieves profile (id, email, display_name, created_at); Expired/invalid token returns 401; Password_hash never included in response | Integration test: valid/invalid token scenarios; response payload audit | Phase 2 | QA |
| FR-AUTH.4a | Bearer access_token returns profile with id, email, display_name, created_at | Integration test: GET /profile with valid token | Phase 2 | QA |
| FR-AUTH.4b | Expired/invalid token returns 401 | Negative test: GET /profile with expired/invalid token | Phase 2 | QA |
| FR-AUTH.4c | Response never includes password_hash or refresh_token_hash | Response payload audit: JSON schema validation | Phase 2 | QA |
| FR-AUTH.5 | Registered email triggers reset token (1-hour TTL) + email dispatch; Valid reset token allows new password; Expired/invalid token returns 400; All existing sessions invalidated | Integration test: request/confirm reset flow; session invalidation audit | Phase 2 | QA |
| FR-AUTH.5a | Email triggers reset token generation and dispatch within 60s | Integration test: POST /password-reset/request, email delivery monitoring | Phase 2 | QA |
| FR-AUTH.5b | Valid reset token allows setting new password; Invalidates reset token after use | Integration test: POST /password-reset/confirm with valid token; reuse attempt fails | Phase 2 | QA |
| FR-AUTH.5c | Expired/invalid token returns 400 | Negative test: POST /password-reset/confirm with expired/invalid token | Phase 2 | QA |
| FR-AUTH.5d | All existing sessions (refresh tokens) invalidated after password reset | Session invalidation test: verify old refresh tokens return 401 after reset | Phase 2 | QA |

---

### Non-Functional Validation

| Requirement ID | Success Criterion | Target | Validation Method | Phase | Owner |
|---|---|---|---|---|---|
| NFR-AUTH.1 | Authentication endpoint response time (p95) under normal load; sustain 500 concurrent requests | < 200ms p95; 500 concurrent | Load test with k6: hammer login endpoint with 500 concurrent clients; measure p95 latency | Phase 2 | QA |
| NFR-AUTH.2 | Service availability over rolling 30-day window | ≥ 99.9% (< 8.76 hours downtime/year) | Health check monitoring (PagerDuty); SLO tracking dashboard | Phase 2+ | DevOps |
| NFR-AUTH.3 | Password hashing security: bcrypt cost 12 (~250ms); passwords never plain-text in logs | Cost factor = 12; no plain-text | Unit test: verify cost factor in bcrypt.hash(); audit logs for password leakage | Phase 1 | Security |
| NFR-AUTH.4 | GDPR consent at registration recorded with timestamp | 100% of new users have consent record | Consent table audit: count users without consent records; should be 0 | Phase 2 | Compliance |
| NFR-AUTH.5 | SOC2 audit logging: all events logged with user_id, timestamp, ip_address, outcome; 12-month retention | 100% event capture; 12-month retention | Audit log schema audit; SOC2 control validation checklist | Phase 2 | Compliance |
| NFR-AUTH.6 | GDPR data minimization: only email, password_hash, display_name collected | No additional PII | Schema audit: confirm user table columns | Phase 2 | Compliance |
| NFR-AUTH.7 | NIST SP 800-63B: one-way adaptive hashing, no plain-text storage/logging | bcrypt implementation verified | Security review: code audit for NIST compliance; no password leakage in logs | Phase 1 | Security |

---

### Success Metrics (PRD Alignment)

| Metric | Target | How Measured | Validation Phase | Owner |
|--------|--------|----------|---|---|
| Registration conversion rate | > 60% | Funnel: landing → register → confirmed account | Post-launch (Week 1-2) | Product |
| Login endpoint response time (p95) | < 200ms | APM on login endpoint during load testing | Phase 2, E2E testing | QA |
| Average session duration | > 30 minutes | Token refresh event analytics | Post-launch (Week 2+) | Product |
| Failed login rate | < 5% of attempts | Auth event log analysis | Post-launch (Week 1+) | Product |
| Password reset completion rate | > 80% | Funnel: reset requested → new password set | Post-launch (Week 2+) | Product |
| Service availability (30-day rolling window) | ≥ 99.9% | Health check monitoring | Post-launch (ongoing) | DevOps |
| All tests passing | 100% pass rate | Unit + integration + E2E test suite | Phase 2 completion | QA |
| Audit log completeness | All auth events captured; 12-month retention | SOC2 audit checklist | Phase 2 completion | Compliance |

---

## Timeline Estimates per Phase

### Phase 1: Foundation & Core Authentication Flows (3 weeks)

| Week | Milestones | Owner | Deliverables | Completion Criteria |
|------|-----------|-------|---------------|--------------------|
| **Week 1** | 1.1.1 (Schema), 1.1.2 (Config), 1.2.1 (PasswordHasher) | Backend Lead + DevOps | Database schema, RSA keys, PasswordHasher implementation | Schema validated on PostgreSQL; PasswordHasher unit tests passing |
| **Week 2** | 1.1.3 (DI), 1.2.2 (JwtService), 1.2.3 (TokenManager), 1.3.1 (UserRepository) | Backend Lead + Backend Support | DI container, JwtService, TokenManager, UserRepository, token dispatch registry | TokenManager integration tests passing; token rotation validated |
| **Week 3** | 1.3.2 (AuthService), 1.4.1-1.4.4 (Middleware + Endpoints), 1.5.1-1.5.2 (Integration tests + Security review) | Backend Lead + Backend Support + Security | AuthService orchestration, POST /register/login/logout, auth middleware, integration tests, security review | Phase 1 acceptance criteria met; security review signed off |

**Phase 1 Effort: 18 engineer-days (3 weeks × 1.0 FTE lead + 0.5 FTE support + 0.3 FTE security)**

---

### Phase 2: Session Persistence, Profile, Password Reset & Compliance (3 weeks)

| Week | Milestones | Owner | Deliverables | Completion Criteria |
|------|-----------|-------|---------------|--------------------|
| **Week 4** | 2.1.1 (POST /refresh), 2.1.2 (Client token strategy), 2.2.1 (GET /profile), 2.3.1 (Password reset service) | Backend Lead + Backend Support + Frontend | Token refresh endpoint, client-side token handling, profile endpoint, reset token generator | Refresh token rotation validated; profile endpoint returning correct schema |
| **Week 5** | 2.3.2-2.3.3 (Password reset endpoints), 2.4.1 (Audit event registry) | Backend Support + QA | Password reset request/confirm endpoints, audit event dispatch, GDPR consent capture | Password reset flow E2E; audit events logged for all endpoints |
| **Week 6** | 2.4.2-2.4.3 (Audit log retention, GDPR consent), 2.5.1-2.5.3 (Compliance validation, E2E tests, load testing) | QA + Security + Compliance + Backend | Audit log query interface, compliance checklists, E2E test suite, load testing, penetration testing scoping | All Phase 2 acceptance criteria met; E2E tests passing; load testing validated (< 200ms p95) |

**Phase 2 Effort: 18 engineer-days (3 weeks × 1.0 FTE lead + 0.5 FTE support + 0.5 FTE QA + 0.3 FTE security)**

---

### Critical Path (Blocker Chain)

1. **Phase 1, Week 1:** Database schema provisioning (blocker for all subsequent phases)
2. **Phase 1, Week 2:** TokenManager + JwtService (blocker for AuthService, API endpoints)
3. **Phase 1, Week 2–3:** AuthService + API endpoints (blocker for integration testing)
4. **Phase 1, Week 3:** Security review (gate before Phase 2 begins)
5. **Phase 2, Week 4:** Token refresh + password reset service (blocker for Phase 2 endpoints)
6. **Phase 2, Week 6:** E2E testing + load testing (gate before production deployment)

**Recommendation:** Use critical path to define sprint dependencies and status checkpoints. If TokenManager slips, all dependent work is blocked.

---

### Post-Launch Timeline (Production Support)

| Period | Activities | Owner |
|--------|-----------|-------|
| **Week 1 after launch** | Monitor funnel metrics (registration conversion, login success rate); daily standup on auth incident response | Product + Backend |
| **Week 2+ after launch** | Weekly metric reviews (session duration, reset completion, failed login rate); SLO tracking | Product + DevOps |
| **Week 4+ after launch** | Post-launch retrospective; iterate on UX based on funnel data | Product + Design |
| **Month 2-3 after launch** | SOC2 audit readiness validation; annual bcrypt cost factor review | Compliance + Security |
| **Month 6 after launch** | Key rotation cycle (RSA keys); dependency security update review | Security + DevOps |

---

## Open Questions & Scope Clarifications

### PRD-Specification Conflicts

**Open Question #7 (Scope):** Is GDPR consent collection (NFR-AUTH.4) a v1.0 hard requirement or deferred?
- **Spec Status:** No mention of GDPR consent in spec §3-§6
- **PRD Status:** NFR-AUTH.4 explicitly requires consent at registration
- **Recommendation:** **Include GDPR consent in v1.0 scope** (Milestone 2.4.3). Missing this creates compliance risk and may force costly v1.0.1 patch.
- **Roadmap Action:** Add GDPR consent checkbox to registration flow; store consent record with timestamp.

**Open Question #9 (Scope):** Is admin audit log *access* (user story AUTH-E3) in v1.0 scope?
- **Spec Status:** GAP-2 defers audit logging infrastructure to v1.1
- **PRD Status:** User story AUTH-E3 includes "As Jordan (admin), I want to view authentication event logs"
- **Extraction Status:** Extraction flags this as a scope conflict
- **Recommendation:** **Split scope into v1.0 + v1.1:**
  - **v1.0:** Pre-provision audit_logs table; emit audit events for all auth operations; 12-month retention policy
  - **v1.1:** Implement admin audit log query interface and API; authorization controls for log access
- **Roadmap Action:** Phase 2, Milestone 2.4.1 emits events; Phase 2, Milestone 2.4.2 adds query interface (can be deferred if timeline pressure).

**Open Question #10 (Spec Gap):** PRD includes logout user story; spec has no corresponding FR.
- **Spec Status:** No FR-AUTH.0 or logout endpoint specified
- **PRD Status:** "As Alex, I want to log out so I can secure my session on a shared device"
- **Recommendation:** **Include logout in v1.0 scope** (Milestone 1.4.4). Logout is table-stakes for a auth service and prevents user frustration with logout via browser back-button.
- **Roadmap Action:** Implement POST /logout endpoint; invalidates refresh token in database.

---

### Engineering Clarifications (Required Before Phase 1 Begins)

| Open Question | Source | Owner | Impact | Recommendation |
|---|---|---|---|---|
| How should password reset emails be sent: synchronously or asynchronously? | PRD OQ-1 | Engineering | Affects reset endpoint latency; if sync, email delivery failure blocks endpoint | **Use message queue** (e.g., Celery, Bull, SQS) for async dispatch; return 200 to user immediately; retry delivery in background |
| Maximum number of active refresh tokens per user across devices? | PRD OQ-2 | Product | Affects multi-device support and storage; impacts session revocation complexity | **Recommend:** No limit; track all active devices; allow user to view and revoke by device. If limit needed (e.g., 5 devices), set in config |
| Account lockout policy after N consecutive failed login attempts? | PRD OQ-3, Spec GAP-1 | Security | Rate limiting (FR-AUTH.1d: 5/min/IP) is in place; progressive lockout is undefined | **Recommend:** v1.0 rate limits at IP level; v1.1 adds account-level lockout after 10 failed attempts in 1 hour; admin unlock capability |
| Should "remember me" extend refresh token TTL beyond 7 days? | PRD OQ-4 | Product | Affects token lifetime and re-authentication burden | **Recommend:** v1.0 uses fixed 7d refresh TTL; v1.1 adds "remember me" option to extend to 30d if user opts in |

---

### Compliance & Legal Clarifications (Required Before Phase 2 Begins)

| Question | Owner | Impact | Resolution |
|---|---|---|---|
| What specific audit logging fields are required for SOC2? | Compliance | Determines audit_logs schema | Finalize list: user_id, event_type, timestamp, ip_address, outcome, http_method, endpoint, response_status |
| What data categories require GDPR data subject request support (Right to Erasure)? | Legal | Affects user deletion flow (out of v1.0 scope, but impacts future roadmap) | Document which fields are user-identifiable (email, display_name) vs system data; plan user deletion flow for v1.1 |
| Is GDPR consent revocation in scope (right to withdraw consent)? | Legal | Affects registration flow | **v1.0:** Capture consent at registration; v1.1 adds revocation interface if user requests |

---

### Product & UX Clarifications (Required Before Phase 1 Begins)

| Question | Owner | Impact | Resolution |
|---|---|---|---|
| Should access token be stored in memory or in httpOnly cookie? | Product + Frontend | Affects token exposure surface; impacts silent refresh UX | **Recommend:** Access token in memory (lost on page refresh; requires silent refresh); refresh token in httpOnly + Secure + SameSite=Strict cookie (persists across refreshes) |
| What should the password reset email contain? | Product + Design | Affects user recovery experience | **Minimum:** Reset link (1-hour TTL), password policy requirements, support contact if link is suspicious |
| Should users be auto-logged in after successful registration? | Product + UX | Affects onboarding flow | **Recommend:** Yes; auto-issue token pair after registration; redirect to dashboard; smoother onboarding |
| Should password reset expire the user's current session (mid-flow logout)? | Product + Security | Affects UX after password reset | **Recommend:** Yes; invalidate all refresh tokens on successful reset (FR-AUTH.5d); require re-login; prevents attacker from maintaining access |

---

## Appendix: Architectural Integration Points Summary

**Dispatch/Registry mechanisms that require explicit wiring in the roadmap:**

1. **Token Type Strategy Registry (Milestone 1.2.3)**
   - Routes access vs refresh token handling
   - Components: AccessTokenStrategy, RefreshTokenStrategy
   - Consumed by: TokenManager, POST /refresh

2. **Error Code Registry (Milestone 1.3.2)**
   - Maps error scenarios to HTTP status codes
   - Components: InvalidCredentials→401, UserAlreadyExists→409, AccountLocked→403, RateLimitExceeded→429, etc.
   - Consumed by: All API endpoints

3. **Audit Event Registry (Milestone 2.4.1)**
   - Routes auth events to audit log sink
   - Components: register, login, login_failed, logout, refresh_token, password_reset_requested, password_reset_confirmed, profile_accessed
   - Consumed by: All endpoints (Phase 1 + Phase 2)

4. **Middleware Chain (Milestone 1.4.1)**
   - Request pipeline: Auth → RateLimit → AuditLogging → Handler
   - Components wired in order; auth middleware extracts token; audit logs all calls
   - Consumed by: All protected endpoints

5. **Reset Token Dispatch Registry (Milestone 2.3.1)**
   - Routes reset token generation/validation
   - Components: Email-based reset (v1.0), SMS-based reset (v2.0)
   - Consumed by: POST /password-reset/request, POST /password-reset/confirm

**Key insight:** These registries are **not** implicit in the component design; they require explicit factory/wiring code. The roadmap calls out the creation phase and consumption phases for each mechanism to prevent integration bugs where components exist but are not wired together.

---

**Roadmap Status: READY FOR EXECUTION**

This roadmap balances security-critical implementation (Phase 1 foundation) with user-facing features (Phase 2 endpoints) and compliance instrumentation (Phase 2 audit). The critical path is clear, blockers are identified, and open questions are flagged for resolution before work begins.

**Pre-Phase 1 Checklist:**
- [ ] Finalize SEC-POLICY-001 (password policy, token TTLs, bcrypt cost factor)
- [ ] Resolve Open Questions #2, #3, #4, #7, #9, #10 with Product, Security, Compliance
- [ ] Provision PostgreSQL 15+, RSA key pair, email service (SendGrid), secrets manager
- [ ] Assign Backend Lead, Backend Support, Security Engineer
- [ ] Schedule security review checkpoint (Phase 1, Week 3)
