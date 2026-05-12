# Phase 2 -- Core Auth Logic

**Goal**: Implement TokenManager and AuthService -- the stateful and orchestration layers -- integrated against real database tables from Phase 1.

**Tasks**: T02.01 -- T02.17
**Roadmap Items**: R-017 -- R-033
**Deliverables**: D-0017 -- D-0033

---

### T02.01 -- Implement TokenManager class

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | TokenManager orchestrates token lifecycle (issue, refresh, revoke) which is central to the auth system's security model. |
| Effort | L |
| Risk | High |
| Risk Drivers | token, security, auth |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Automated tests + security review |
| Deliverable IDs | D-0017 |

**Deliverables:**
- `TokenManager` class with methods: `issueTokenPair(userId)`, `refreshTokens(refreshToken)`, `revokeAllForUser(userId)`

**Steps:**
1. [PLANNING] Design TokenManager interface per FR-AUTH.3; define database interaction patterns
2. [EXECUTION] Implement issueTokenPair, refreshTokens, and revokeAllForUser with atomic transactions
3. [VERIFICATION] Unit test each method with mocked dependencies

**Acceptance Criteria:**
- issueTokenPair returns access token + refresh token pair
- refreshTokens validates existing token, issues new pair, revokes old
- revokeAllForUser invalidates all refresh tokens for a user
- All database operations use transactions

**Validation:**
- Manual check: Inspect database state after each operation
- Evidence: Class implementation and test file committed

**Dependencies:** T01.08, T01.14

---

### T02.02 -- Refresh token rotation with replay detection

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018 |
| Why | FR-AUTH.3a and FR-AUTH.3c mandate rotation on refresh and full revocation on replay, preventing token theft escalation. |
| Effort | XL |
| Risk | High |
| Risk Drivers | token, security, auth, crypto |
| Tier | STRICT |
| Confidence | [███████---] 80% |
| Critical Path Override | Yes |
| Verification Method | Automated tests + adversarial testing |
| Deliverable IDs | D-0018 |

**Deliverables:**
- Replay detection logic: reuse of revoked token triggers full token revocation for the user
- Atomic transaction wrapping rotation + revocation

**Steps:**
1. [PLANNING] Design state machine: active -> rotated -> revoked; define replay detection trigger
2. [EXECUTION] Implement rotation in refreshTokens: issue new pair, mark old as revoked (atomic)
3. [EXECUTION] Implement replay detection: if presented token is already revoked, revoke ALL user tokens
4. [VERIFICATION] Test: normal rotation, replay attempt triggers full revocation

**Acceptance Criteria:**
- Normal refresh: old token revoked, new pair issued, atomic transaction
- Replay attempt: revoked token presented triggers revokeAllForUser
- Race condition: concurrent refresh attempts handled safely via DB transaction isolation
- Replay detection is logged for security monitoring

**Validation:**
- Manual check: Simulate replay attack and verify all tokens revoked
- Evidence: Test suite with rotation and replay scenarios committed

**Dependencies:** T02.01

---

### T02.03 -- Refresh token hash storage (SHA-256)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-019 |
| Why | FR-AUTH.3d requires storing only the hash of refresh tokens; raw tokens must never be persisted. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | token, crypto, security |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Automated test + database audit |
| Deliverable IDs | D-0019 |

**Deliverables:**
- SHA-256 hashing of refresh tokens before database storage
- Lookup by hash for token validation

**Steps:**
1. [PLANNING] Define hashing approach (SHA-256 of raw token)
2. [EXECUTION] Hash tokens before INSERT; lookup by hash on refresh/revoke
3. [VERIFICATION] Test that raw token never appears in database; lookup by hash works

**Acceptance Criteria:**
- Raw refresh tokens are never stored in the database
- token_hash column contains SHA-256 hex digest
- Token validation works by hashing presented token and looking up hash

**Validation:**
- Manual check: Query refresh_tokens table and confirm no raw tokens
- Evidence: Hash utility and database audit test committed

**Dependencies:** T02.01

---

### T02.04 -- Refresh token TTL configuration (7 days)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020 |
| Why | FR-AUTH.1a specifies 7-day refresh token TTL; configurable for operational flexibility. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | token |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0020 |

**Deliverables:**
- Configuration entry for refresh token TTL, default 7 days, environment variable override

**Steps:**
1. [PLANNING] Define config key and env var
2. [EXECUTION] Add config; wire into TokenManager.issueTokenPair()
3. [VERIFICATION] Test that refresh tokens expire at configured TTL

**Acceptance Criteria:**
- Default TTL is 7 days (604800 seconds)
- Configurable via environment variable
- TokenManager uses config value for refresh token expiration

**Validation:**
- Manual check: Inspect expires_at in database after token issuance
- Evidence: Config and test committed

**Dependencies:** T02.01

---

### T02.05 -- Enforce max 5 active refresh tokens per user

| Field | Value |
|---|---|
| Roadmap Item IDs | R-021 |
| Why | OI-2 resolution caps active tokens at 5 per user to limit token sprawl and reduce attack surface. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0021 |

**Deliverables:**
- Token cap enforcement: revoke oldest active token when issuing 6th

**Steps:**
1. [PLANNING] Define cap logic: count active (non-revoked, non-expired) tokens per user
2. [EXECUTION] On issueTokenPair, check count; if >= 5, revoke oldest before issuing new
3. [VERIFICATION] Test with 5 active tokens, issue 6th, verify oldest revoked

**Acceptance Criteria:**
- User can have at most 5 active refresh tokens
- 6th token issuance revokes the oldest active token
- Revoked and expired tokens do not count toward cap

**Validation:**
- Manual check: Issue 6 tokens for same user, query database
- Evidence: Cap enforcement logic and test committed

**Dependencies:** T02.01

---

> **CHECKPOINT 4** (after T02.05): Verify T02.01--T02.05 pass. TokenManager issues, rotates, and caps tokens correctly. Replay detection works against real database.

---

### T02.06 -- Refresh token delivery via httpOnly cookie

| Field | Value |
|---|---|
| Roadmap Item IDs | R-022 |
| Why | FR-AUTH.1-IMPL-2 and OQ-5 resolution require httpOnly cookie transport to prevent XSS token theft. |
| Effort | M |
| Risk | High |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Automated test + header inspection |
| Deliverable IDs | D-0022 |

**Deliverables:**
- Cookie setting utility: httpOnly, Secure, SameSite=Strict attributes
- Refresh token excluded from JSON response body

**Steps:**
1. [PLANNING] Define cookie attributes per security requirements
2. [EXECUTION] Implement cookie setting with httpOnly, Secure, SameSite=Strict
3. [EXECUTION] Ensure refresh token is NOT included in JSON response body
4. [VERIFICATION] Test cookie attributes and verify absence from response body

**Acceptance Criteria:**
- Cookie has HttpOnly flag set
- Cookie has Secure flag set
- Cookie has SameSite=Strict
- Refresh token does not appear in any JSON response body

**Validation:**
- Manual check: Inspect Set-Cookie header in response
- Evidence: Cookie utility and test committed

**Dependencies:** T02.01

---

### T02.07 -- Unit tests for TokenManager

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023 |
| Why | SC-5 requires comprehensive testing; TokenManager is the highest-risk component with 6+ distinct behaviors. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0023 |

**Deliverables:**
- Unit test suite with minimum 6 test cases: issue, rotate, replay detection, expiry, cap enforcement, cookie delivery

**Steps:**
1. [PLANNING] List all test cases per SC-5 requirements
2. [EXECUTION] Write tests for each TokenManager behavior
3. [VERIFICATION] Run all tests; confirm minimum 6 cases pass

**Acceptance Criteria:**
- Test: issueTokenPair produces valid pair
- Test: refreshTokens rotates correctly
- Test: replay detection triggers full revocation
- Test: expired token rejected
- Test: 6th token revokes oldest
- Test: cookie attributes correct

**Validation:**
- Manual check: Review test coverage report for TokenManager
- Evidence: Test file committed; CI green

**Dependencies:** T02.01, T02.02, T02.03, T02.04, T02.05, T02.06

---

### T02.08 -- Implement AuthService.login()

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | Login is the primary authentication flow; must handle credential verification, locked accounts, and generic error messages. |
| Effort | M |
| Risk | High |
| Risk Drivers | auth, security, password |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated tests |
| Deliverable IDs | D-0024 |

**Deliverables:**
- `AuthService.login()` method: verify credentials, issue token pair, return 401 on failure (FR-AUTH.1b), return 403 on locked account (FR-AUTH.1c)

**Steps:**
1. [PLANNING] Define login flow per FR-AUTH.1
2. [EXECUTION] Implement: lookup user by email, verify password, check locked status, issue tokens
3. [VERIFICATION] Test happy path, wrong password (401), locked account (403)

**Acceptance Criteria:**
- Valid credentials return access token and set refresh cookie
- Invalid credentials return 401 with generic message (no email/password differentiation)
- Locked account returns 403
- No timing side-channel between valid/invalid email

**Validation:**
- Manual check: Attempt login with valid and invalid credentials
- Evidence: Login implementation and test committed

**Dependencies:** T02.01, T01.04

---

### T02.09 -- Implement AuthService.register()

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025 |
| Why | User registration must enforce email format, uniqueness, and password policy before creating an account. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | auth, security, password |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Critical Path Override | Yes |
| Verification Method | Automated tests |
| Deliverable IDs | D-0025 |

**Deliverables:**
- `AuthService.register()` method: validate email (FR-AUTH.2d), check uniqueness (FR-AUTH.2b), enforce password policy (FR-AUTH.2c), hash password, create user

**Steps:**
1. [PLANNING] Define registration flow per FR-AUTH.2
2. [EXECUTION] Implement validation chain: email format -> uniqueness -> password policy -> hash -> insert
3. [VERIFICATION] Test happy path, duplicate email (409), weak password (400), invalid email (400)

**Acceptance Criteria:**
- Valid registration creates user and returns profile (201)
- Duplicate email returns 409
- Weak password returns 400 with policy description
- Invalid email format returns 400
- Password stored as bcrypt hash, never plaintext

**Validation:**
- Manual check: Register user, query database for hash
- Evidence: Registration implementation and test committed

**Dependencies:** T01.04, T01.05

---

### T02.10 -- Implement AuthService.getProfile()

| Field | Value |
|---|---|
| Roadmap Item IDs | R-026 |
| Why | Profile retrieval must return only safe fields, explicitly excluding sensitive data per FR-AUTH.4c and SC-8. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | auth, security |
| Tier | STRICT |
| Confidence | [█████████-] 93% |
| Critical Path Override | Yes |
| Verification Method | Automated test + response audit |
| Deliverable IDs | D-0026 |

**Deliverables:**
- `AuthService.getProfile()` method returning only: id, email, display_name, created_at

**Steps:**
1. [PLANNING] Define allowed fields per FR-AUTH.4, FR-AUTH.4c, SC-8
2. [EXECUTION] Implement query selecting only safe fields
3. [VERIFICATION] Test response contains only allowed fields; no password_hash or token data

**Acceptance Criteria:**
- Response includes: id, email, display_name, created_at
- Response excludes: password_hash, refresh_token_hash, updated_at, is_locked
- Non-existent user returns 404

**Validation:**
- Manual check: Inspect response JSON for field list
- Evidence: Profile implementation and test committed

**Dependencies:** T01.14

---

> **CHECKPOINT 5** (after T02.10): Verify T02.06--T02.10 pass. Cookie delivery works. Login, register, and profile methods functional.

---

### T02.11 -- Implement AuthService.requestPasswordReset()

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027 |
| Why | Password reset initiation must generate secure tokens and prevent email enumeration per FR-AUTH.5a. |
| Effort | L |
| Risk | High |
| Risk Drivers | auth, security, token |
| Tier | STRICT |
| Confidence | [████████--] 82% |
| Critical Path Override | Yes |
| Verification Method | Automated tests |
| Deliverable IDs | D-0027 |

**Deliverables:**
- `AuthService.requestPasswordReset()`: generate reset token (1hr TTL), dispatch email synchronously, always return 200

**Steps:**
1. [PLANNING] Define reset token format, TTL, email dispatch per FR-AUTH.5a, OI-1
2. [EXECUTION] Implement: generate cryptographically random token, store hash, send email, return 200
3. [VERIFICATION] Test: valid email sends email, invalid email still returns 200 (no enumeration)

**Acceptance Criteria:**
- Reset token has 1-hour TTL
- Email dispatched synchronously per OI-1 resolution
- Always returns 200 regardless of email existence (anti-enumeration)
- Reset token stored as hash, not plaintext

**Validation:**
- Manual check: Request reset for non-existent email, verify 200 response
- Evidence: Reset request implementation and test committed

**Dependencies:** T01.14

---

### T02.12 -- Implement AuthService.resetPassword()

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | Password reset completion must validate token, update password, invalidate token, and revoke all refresh tokens per FR-AUTH.5b-d. |
| Effort | L |
| Risk | High |
| Risk Drivers | auth, security, password, token |
| Tier | STRICT |
| Confidence | [████████--] 82% |
| Critical Path Override | Yes |
| Verification Method | Automated tests |
| Deliverable IDs | D-0028 |

**Deliverables:**
- `AuthService.resetPassword()`: validate reset token, update password hash, invalidate reset token, revoke all refresh tokens

**Steps:**
1. [PLANNING] Define reset flow per FR-AUTH.5b, FR-AUTH.5c, FR-AUTH.5d
2. [EXECUTION] Implement: validate token -> hash new password -> update user -> invalidate token -> revoke all refresh tokens (atomic)
3. [VERIFICATION] Test: valid reset, expired token, already-used token, refresh tokens revoked

**Acceptance Criteria:**
- Valid token: password updated, token invalidated, all refresh tokens revoked
- Expired token: returns 400
- Already-used token: returns 400
- New password meets policy requirements
- All operations within single transaction

**Validation:**
- Manual check: Reset password, verify old refresh tokens no longer work
- Evidence: Reset implementation and test committed

**Dependencies:** T02.01, T01.04, T01.05

---

### T02.13 -- Rate limiter for login endpoint

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029 |
| Why | FR-AUTH.1d mandates rate limiting at 5 attempts/min/IP to mitigate brute-force attacks. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | security, auth |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0029 |

**Deliverables:**
- Rate limiter middleware/service: 5 attempts per minute per IP, in-memory store for single-instance MVP

**Steps:**
1. [PLANNING] Define rate limiting strategy per FR-AUTH.1d
2. [EXECUTION] Implement in-memory rate limiter with sliding window
3. [VERIFICATION] Test: 5 requests pass, 6th returns 429

**Acceptance Criteria:**
- First 5 login attempts within 1 minute succeed
- 6th attempt returns 429 Too Many Requests
- Rate limit resets after window expires
- In-memory store is acceptable for MVP

**Validation:**
- Manual check: Send 6 rapid login requests, verify 429 on 6th
- Evidence: Rate limiter implementation and test committed

**Dependencies:** None

---

### T02.14 -- Unit tests for AuthService (all 5 flows)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-030 |
| Why | SC-5 requires minimum 15 test cases covering all 5 AuthService flows with happy and error paths. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | auth, security |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0030 |

**Deliverables:**
- Unit test suite with minimum 15 test cases across login, register, getProfile, requestPasswordReset, resetPassword

**Steps:**
1. [PLANNING] List all test cases: 3+ per flow (happy path, error paths)
2. [EXECUTION] Write tests for each flow with mocked dependencies
3. [VERIFICATION] Run all tests; confirm minimum 15 cases pass

**Acceptance Criteria:**
- Login: valid credentials, invalid password, locked account (3+ tests)
- Register: valid, duplicate email, weak password, invalid email (4+ tests)
- GetProfile: valid user, non-existent user (2+ tests)
- RequestPasswordReset: valid email, invalid email both return 200 (2+ tests)
- ResetPassword: valid, expired token, used token, refresh tokens revoked (4+ tests)

**Validation:**
- Manual check: Review test count and coverage per flow
- Evidence: Test file committed; CI green

**Dependencies:** T02.08, T02.09, T02.10, T02.11, T02.12

---

### T02.15 -- Implement AUTH_SERVICE_ENABLED feature flag

| Field | Value |
|---|---|
| Roadmap Item IDs | R-031 |
| Why | FR-AUTH.1-IMPL-4 requires a feature flag for safe rollout and rollback capability. |
| Effort | S |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 95% |
| Critical Path Override | No |
| Verification Method | Automated test |
| Deliverable IDs | D-0031 |

**Deliverables:**
- Feature flag reading from environment variable `AUTH_SERVICE_ENABLED`
- Gates auth route registration

**Steps:**
1. [PLANNING] Define flag behavior per FR-AUTH.1-IMPL-4
2. [EXECUTION] Read flag from environment; default to false for safety
3. [VERIFICATION] Test flag enabled/disabled behavior

**Acceptance Criteria:**
- Flag reads from AUTH_SERVICE_ENABLED env var
- Default is false (safe by default)
- When false, auth routes are not registered

**Validation:**
- Manual check: Set flag to false, verify no auth routes available
- Evidence: Flag implementation and test committed

**Dependencies:** None

---

> **CHECKPOINT 6** (after T02.15): Verify T02.11--T02.15 pass. Password reset flows work. Rate limiter enforces 5/min/IP. Feature flag gates routes.

---

### T02.16 -- Feature flag disabled behavior (503/404)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032 |
| Why | SC-9 requires defined behavior when auth is disabled; prevents confusing error responses. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 93% |
| Critical Path Override | No |
| Verification Method | Automated test |
| Deliverable IDs | D-0032 |

**Deliverables:**
- Defined response when flag is disabled: 503 with Retry-After for internal, 404 for external

**Steps:**
1. [PLANNING] Define disabled response strategy per SC-9
2. [EXECUTION] Implement conditional response based on consumer type
3. [VERIFICATION] Test both response codes when flag is disabled

**Acceptance Criteria:**
- Internal consumers receive 503 with Retry-After header
- External/public consumers receive 404
- Response is clean and informative

**Validation:**
- Manual check: Request auth endpoint with flag disabled
- Evidence: Disabled behavior implementation and test committed

**Dependencies:** T02.15

---

### T02.17 -- Verify rollback: flag=false restores pre-auth behavior

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033 |
| Why | SC-9 mandates that disabling the flag completely restores the system to pre-auth state. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 92% |
| Critical Path Override | No |
| Verification Method | Integration test |
| Deliverable IDs | D-0033 |

**Deliverables:**
- Integration test verifying pre-auth behavior is fully restored when flag is disabled

**Steps:**
1. [PLANNING] Define pre-auth behavior expectations
2. [EXECUTION] Write integration test: enable flag, register routes, disable flag, verify routes gone
3. [VERIFICATION] Run test; confirm no auth routes or middleware active

**Acceptance Criteria:**
- With flag disabled, no auth routes respond
- Existing (non-auth) functionality is unaffected
- No auth middleware intercepts requests

**Validation:**
- Manual check: Toggle flag and exercise existing endpoints
- Evidence: Integration test committed; CI green

**Dependencies:** T02.15, T02.16

---

> **END-OF-PHASE CHECKPOINT** (Phase 2 Gate): All unit tests pass for TokenManager and AuthService. Replay detection works against real database. Rate limiter enforces limits. Feature flag toggles correctly. SC-5 complete (all 4 services tested). All deliverables D-0017 through D-0033 produced and verified.
