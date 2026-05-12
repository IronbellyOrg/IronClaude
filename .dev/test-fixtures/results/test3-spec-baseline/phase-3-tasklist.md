# Phase 3 -- Integration Layer

**Goal**: Wire services to HTTP routes and middleware. End-to-end flows work against real database.

**Tasks**: T03.01 -- T03.17
**Roadmap Items**: R-034 -- R-050
**Deliverables**: D-0034 -- D-0050

---

### T03.01 -- Implement auth middleware for Bearer token extraction

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | FR-AUTH.4b requires middleware to extract and verify Bearer tokens from Authorization headers for protected routes. |
| Effort | M |
| Risk | High |
| Risk Drivers | auth, security, token |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated tests |
| Deliverable IDs | D-0034 |

**Deliverables:**
- Auth middleware at `src/middleware/auth-middleware.ts` that extracts Bearer token, verifies via JwtService, attaches userId to request context

**Steps:**
1. [PLANNING] Define middleware contract per FR-AUTH.4b
2. [EXECUTION] Implement: extract Authorization header, parse Bearer token, call JwtService.verify(), attach userId
3. [VERIFICATION] Test: valid token passes, invalid rejects with 401

**Acceptance Criteria:**
- Extracts Bearer token from Authorization header
- Verifies token via JwtService.verify()
- Attaches userId to request context on success
- Returns 401 on missing, invalid, or expired tokens

**Validation:**
- Manual check: Send request with valid/invalid Bearer token
- Evidence: Middleware implementation and test committed

**Dependencies:** T01.08

---

### T03.02 -- Cookie extraction for refresh token

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | FR-AUTH.1-IMPL-2 requires reading refresh tokens from httpOnly cookies for the refresh flow. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0035 |

**Deliverables:**
- Cookie parsing utility that extracts refresh_token from httpOnly cookie and validates via TokenManager

**Steps:**
1. [PLANNING] Define cookie name and extraction approach
2. [EXECUTION] Implement cookie parser for refresh_token cookie
3. [VERIFICATION] Test extraction with valid and missing cookies

**Acceptance Criteria:**
- Reads refresh_token from cookie by name
- Passes extracted token to TokenManager for validation
- Returns 401 when cookie is missing or invalid

**Validation:**
- Manual check: Send request with and without refresh cookie
- Evidence: Cookie extraction utility and test committed

**Dependencies:** T02.06

---

### T03.03 -- Reject expired/invalid tokens with 401

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | Consistent 401 responses with sanitized error messages prevent information leakage per FR-AUTH.1b. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | auth, security |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0036 |

**Deliverables:**
- Consistent error response format for all auth failures; sanitized messages (no internal details)

**Steps:**
1. [PLANNING] Define error response schema per FR-AUTH.1b
2. [EXECUTION] Implement standardized 401 response with generic message
3. [VERIFICATION] Test that error messages do not leak implementation details

**Acceptance Criteria:**
- All auth failures return 401 with generic message
- No differentiation between "user not found" and "wrong password"
- No stack traces or internal details in error response
- Error response format is consistent across all endpoints

**Validation:**
- Manual check: Trigger various auth failures, inspect response bodies
- Evidence: Error handler and test committed

**Dependencies:** T03.01

---

### T03.04 -- Unit tests for auth middleware

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | SC-5 requires testing middleware; minimum 3 test cases for valid, invalid, and missing token scenarios. |
| Effort | S |
| Risk | Low |
| Risk Drivers | auth |
| Tier | STRICT |
| Confidence | [█████████-] 93% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0037 |

**Deliverables:**
- Unit test suite: valid token passes, invalid token returns 401, missing token returns 401

**Steps:**
1. [PLANNING] Define 3 test cases per SC-5
2. [EXECUTION] Write tests with mocked JwtService
3. [VERIFICATION] Run tests; confirm all 3 pass

**Acceptance Criteria:**
- Test: valid Bearer token - middleware passes, userId in context
- Test: invalid Bearer token - middleware returns 401
- Test: missing Authorization header - middleware returns 401

**Validation:**
- Manual check: Review test assertions
- Evidence: Test file committed; CI green

**Dependencies:** T03.01, T03.02, T03.03

---

### T03.05 -- POST /auth/login route

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | Login route is the primary authentication entry point; must be rate-limited and set refresh cookie. |
| Effort | M |
| Risk | High |
| Risk Drivers | auth, security |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0038 |

**Deliverables:**
- Route handler for POST /auth/login: rate-limited, calls AuthService.login(), sets refresh token cookie, returns access_token in body

**Steps:**
1. [PLANNING] Define route, request/response schema per FR-AUTH.1
2. [EXECUTION] Implement handler with rate limiter middleware, AuthService integration, cookie setting
3. [VERIFICATION] Test: valid login, invalid credentials, rate limit exceeded

**Acceptance Criteria:**
- Returns 200 with access_token in JSON body on success
- Sets refresh_token as httpOnly cookie
- Returns 401 on invalid credentials
- Returns 429 after 5 attempts in 1 minute
- Rate limiter is applied to this route

**Validation:**
- Manual check: Login via curl, inspect response body and Set-Cookie header
- Evidence: Route handler and test committed

**Dependencies:** T02.08, T02.13, T02.06

---

> **CHECKPOINT 7** (after T03.05): Verify T03.01--T03.05 pass. Auth middleware works. Login route functional with rate limiting and cookie delivery.

---

### T03.06 -- POST /auth/register route

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Registration route creates new user accounts with full validation per FR-AUTH.2. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | auth |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0039 |

**Deliverables:**
- Route handler for POST /auth/register: calls AuthService.register(), returns 201 with user profile

**Steps:**
1. [PLANNING] Define route, request/response schema per FR-AUTH.2
2. [EXECUTION] Implement handler calling AuthService.register()
3. [VERIFICATION] Test: valid registration (201), duplicate email (409), weak password (400)

**Acceptance Criteria:**
- Returns 201 with user profile (id, email, display_name, created_at) on success
- Returns 409 on duplicate email
- Returns 400 on invalid input (weak password, bad email format)

**Validation:**
- Manual check: Register via curl, inspect response
- Evidence: Route handler and test committed

**Dependencies:** T02.09

---

### T03.07 -- POST /auth/refresh route

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | Token refresh route enables session continuation via cookie-based refresh token rotation per FR-AUTH.3. |
| Effort | M |
| Risk | High |
| Risk Drivers | auth, security, token |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0040 |

**Deliverables:**
- Route handler for POST /auth/refresh: reads refresh token from cookie, calls TokenManager.refreshTokens(), sets new cookie, returns new access_token

**Steps:**
1. [PLANNING] Define route flow per FR-AUTH.3
2. [EXECUTION] Implement handler: extract cookie, call refreshTokens, set new cookie, return access_token
3. [VERIFICATION] Test: valid refresh, expired token, replayed token

**Acceptance Criteria:**
- Returns 200 with new access_token on valid refresh
- Sets new refresh_token cookie
- Returns 401 on expired or invalid refresh token
- Replay triggers full token revocation

**Validation:**
- Manual check: Refresh via curl with cookie, inspect new cookie
- Evidence: Route handler and test committed

**Dependencies:** T02.01, T03.02

---

### T03.08 -- GET /auth/profile route

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | Profile route is a protected endpoint demonstrating auth middleware integration per FR-AUTH.4. |
| Effort | S |
| Risk | Low |
| Risk Drivers | auth |
| Tier | STRICT |
| Confidence | [█████████-] 93% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0041 |

**Deliverables:**
- Route handler for GET /auth/profile: protected by auth middleware, calls AuthService.getProfile()

**Steps:**
1. [PLANNING] Define route with auth middleware per FR-AUTH.4
2. [EXECUTION] Implement handler: auth middleware, call getProfile(userId)
3. [VERIFICATION] Test: valid token returns profile, invalid token returns 401

**Acceptance Criteria:**
- Protected by auth middleware (requires valid access token)
- Returns 200 with user profile (no sensitive fields)
- Returns 401 without valid token

**Validation:**
- Manual check: Request profile with and without Bearer token
- Evidence: Route handler and test committed

**Dependencies:** T02.10, T03.01

---

### T03.09 -- POST /auth/password-reset/request route

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Password reset request route must always return 200 to prevent email enumeration per FR-AUTH.5a. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | auth, security |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0042 |

**Deliverables:**
- Route handler for POST /auth/password-reset/request: calls AuthService.requestPasswordReset(), always returns 200

**Steps:**
1. [PLANNING] Define route per FR-AUTH.5a
2. [EXECUTION] Implement handler calling requestPasswordReset()
3. [VERIFICATION] Test: valid email returns 200, invalid email returns 200 (same response)

**Acceptance Criteria:**
- Always returns 200 regardless of email existence
- Response body is identical for existing and non-existing emails
- No timing difference between existing and non-existing emails

**Validation:**
- Manual check: Request reset for real and fake emails, compare responses
- Evidence: Route handler and test committed

**Dependencies:** T02.11

---

### T03.10 -- POST /auth/password-reset/confirm route

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | Password reset confirmation completes the reset flow per FR-AUTH.5b. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | auth, security, password |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Critical Path Override | Yes |
| Verification Method | Automated test |
| Deliverable IDs | D-0043 |

**Deliverables:**
- Route handler for POST /auth/password-reset/confirm: calls AuthService.resetPassword(), returns 200 on success

**Steps:**
1. [PLANNING] Define route per FR-AUTH.5b
2. [EXECUTION] Implement handler calling resetPassword()
3. [VERIFICATION] Test: valid reset (200), expired token (400), invalid token (400)

**Acceptance Criteria:**
- Returns 200 on successful password reset
- Returns 400 on expired or invalid token
- Returns 400 on weak new password

**Validation:**
- Manual check: Complete reset flow via curl
- Evidence: Route handler and test committed

**Dependencies:** T02.12

---

> **CHECKPOINT 8** (after T03.10): Verify T03.06--T03.10 pass. All 6 route handlers functional. Request/response schemas correct.

---

### T03.11 -- Modify route registration for feature flag gating

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | FR-AUTH.1-IMPL-4 requires auth routes to be conditionally registered based on AUTH_SERVICE_ENABLED flag. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | — |
| Tier | STANDARD |
| Confidence | [█████████-] 95% |
| Critical Path Override | No |
| Verification Method | Automated test |
| Deliverable IDs | D-0044 |

**Deliverables:**
- Modified `src/routes/index.ts` with conditional auth route registration

**Steps:**
1. [PLANNING] Define conditional registration per FR-AUTH.1-IMPL-4
2. [EXECUTION] Wrap auth route registration in feature flag check
3. [VERIFICATION] Test: flag on = routes registered, flag off = routes absent

**Acceptance Criteria:**
- Auth routes only registered when AUTH_SERVICE_ENABLED is true
- Non-auth routes unaffected by flag state
- Route table is clean when flag is disabled

**Validation:**
- Manual check: Toggle flag, list registered routes
- Evidence: Modified route registration and test committed

**Dependencies:** T02.15, T03.05, T03.06, T03.07, T03.08, T03.09, T03.10

---

### T03.12 -- Integration test: full login flow

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045 |
| Why | SC-6 requires integration tests against real database; login flow validates the complete auth chain. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | auth |
| Tier | STRICT |
| Confidence | [████████--] 88% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0045 |

**Deliverables:**
- Integration test: register user, login, verify returned access token works for profile endpoint

**Steps:**
1. [PLANNING] Define test flow per SC-6
2. [EXECUTION] Write test: POST /register -> POST /login -> GET /profile with access token
3. [VERIFICATION] Run against test database; confirm full flow passes

**Acceptance Criteria:**
- Register returns 201 with user data
- Login returns 200 with valid access token
- Profile request with access token returns user data
- All against real database (no mocks)

**Validation:**
- Manual check: Run test, inspect database state
- Evidence: Integration test committed; CI green

**Dependencies:** T03.05, T03.06, T03.08

---

### T03.13 -- Integration test: token refresh with rotation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-046 |
| Why | SC-6 requires validation that token rotation works end-to-end: new token valid, old token rejected. |
| Effort | M |
| Risk | High |
| Risk Drivers | token, security |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0046 |

**Deliverables:**
- Integration test: login, refresh, verify new token works, verify old refresh token is rejected

**Steps:**
1. [PLANNING] Define rotation test flow per SC-6, FR-AUTH.3a, FR-AUTH.3c
2. [EXECUTION] Write test: login -> refresh -> use new token -> attempt old refresh token
3. [VERIFICATION] Verify new token works, old token returns 401

**Acceptance Criteria:**
- After refresh, new access token is valid
- After refresh, new refresh token cookie is set
- Old refresh token returns 401 on reuse
- Validates FR-AUTH.3a (rotation) and FR-AUTH.3c (replay)

**Validation:**
- Manual check: Inspect database for revoked token records
- Evidence: Integration test committed; CI green

**Dependencies:** T03.07

---

### T03.14 -- Integration test: password reset lifecycle

| Field | Value |
|---|---|
| Roadmap Item IDs | R-047 |
| Why | SC-6 requires end-to-end password reset validation: request, reset, login with new password, old tokens invalidated. |
| Effort | L |
| Risk | High |
| Risk Drivers | auth, security, password, token |
| Tier | STRICT |
| Confidence | [████████--] 82% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0047 |

**Deliverables:**
- Integration test: request reset, confirm reset, login with new password, verify old refresh tokens invalidated

**Steps:**
1. [PLANNING] Define full reset lifecycle per FR-AUTH.5
2. [EXECUTION] Write test: register -> login -> request reset -> confirm reset -> login with new password -> verify old tokens invalid
3. [VERIFICATION] Run against test database; confirm full lifecycle

**Acceptance Criteria:**
- Password reset request returns 200
- Password reset confirm updates password
- Login with new password succeeds
- Old refresh tokens are revoked after reset
- Login with old password fails

**Validation:**
- Manual check: Run test, verify database state at each step
- Evidence: Integration test committed; CI green

**Dependencies:** T03.09, T03.10, T03.05

---

### T03.15 -- Integration test: sensitive field filtering

| Field | Value |
|---|---|
| Roadmap Item IDs | R-048 |
| Why | SC-8 mandates that no password_hash or refresh_token_hash appears in any API response. |
| Effort | XS |
| Risk | Medium |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 92% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0048 |

**Deliverables:**
- Integration test scanning all endpoint responses for sensitive field names

**Steps:**
1. [PLANNING] Define sensitive field list per SC-8
2. [EXECUTION] Write test: call all endpoints, scan response bodies for password_hash, token_hash, password
3. [VERIFICATION] Confirm no sensitive fields in any response

**Acceptance Criteria:**
- No response body contains password_hash
- No response body contains token_hash or refresh_token_hash
- No response body contains plaintext password
- Covers all 6 endpoint responses

**Validation:**
- Manual check: Grep response bodies for sensitive strings
- Evidence: Integration test committed; CI green

**Dependencies:** T03.05, T03.06, T03.07, T03.08, T03.09, T03.10

---

> **CHECKPOINT 9** (after T03.15): Verify T03.11--T03.15 pass. Integration tests pass against real database. Sensitive fields filtered. Route gating works.

---

### T03.16 -- Integration test: rate limiting enforcement

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | FR-AUTH.1d rate limiting must be verified end-to-end; timing-sensitive test confirms 429 response. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0049 |

**Deliverables:**
- Integration test: send 6 login attempts within 1 minute, verify 6th returns 429

**Steps:**
1. [PLANNING] Define timing-sensitive test approach
2. [EXECUTION] Write test: 5 login attempts succeed, 6th returns 429 within same window
3. [VERIFICATION] Run test; confirm rate limit triggers

**Acceptance Criteria:**
- First 5 login attempts return expected responses (200 or 401)
- 6th attempt within 1 minute returns 429
- Rate limit window resets after expiry

**Validation:**
- Manual check: Execute rapid requests, verify 429 response
- Evidence: Integration test committed; CI green

**Dependencies:** T03.05, T02.13

---

### T03.17 -- E2E lifecycle test: full user journey

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050 |
| Why | SC-7 requires a complete end-to-end lifecycle: register, login, profile, refresh, reset, re-login. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | auth |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Critical Path Override | Yes |
| Verification Method | Test execution |
| Deliverable IDs | D-0050 |

**Deliverables:**
- E2E test covering full user journey: register -> login -> profile -> refresh -> password reset -> re-login

**Steps:**
1. [PLANNING] Define full lifecycle per SC-7
2. [EXECUTION] Write test exercising all 6 endpoints in sequence
3. [VERIFICATION] Run against test database; confirm complete journey passes

**Acceptance Criteria:**
- Register: creates user (201)
- Login: returns access token (200)
- Profile: returns user data with access token (200)
- Refresh: returns new access token (200)
- Password reset: request + confirm (200)
- Re-login: succeeds with new password (200)
- All within single test run against real database

**Validation:**
- Manual check: Run test, verify each step succeeds
- Evidence: E2E test committed; CI green

**Dependencies:** T03.05, T03.06, T03.07, T03.08, T03.09, T03.10

---

> **END-OF-PHASE CHECKPOINT** (Phase 3 Gate): All integration tests pass. E2E lifecycle completes. SC-6, SC-7, SC-8 validated. Route table gated by feature flag. All deliverables D-0034 through D-0050 produced and verified.
