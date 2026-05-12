# Phase 3 -- Authentication Service and Endpoints

**Goal:** Compose primitives into AuthService orchestrator and ship all five `/auth/*` endpoints behind the feature flag with middleware, routing, rate-limiting, and email integration wired.

### T03.01 -- AuthService orchestrator (COMP-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | Core orchestrator coordinating login, register, refresh, profile, and reset flows. |
| Effort | L |
| Risk | High |
| Risk Drivers | security, auth |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/spec.md`
- `TASKLIST_ROOT/artifacts/D-0010/evidence.md`

**Deliverables:**
- `src/auth/auth-service.ts` exposing login/register/refresh/getProfile/requestPasswordReset/confirmPasswordReset

**Steps:**
1. **[PLANNING]** Identify FR mappings per roadmap
2. **[PLANNING]** Confirm DI bindings for primitives
3. **[EXECUTION]** Implement orchestrator methods
4. **[EXECUTION]** Wire validators into register/reset flows
5. **[VERIFICATION]** Run integration suite
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Method `login` returns AuthTokenPair on valid credentials
- Each FR-AUTH.* maps to exactly one method
- DI-constructed (no `new` inside the orchestrator)
- Evidence file `D-0010/evidence.md` recorded

**Validation:**
- Manual check: TEST-M3-001 + TEST-M3-002 green
- Evidence: linkable artifact produced

**Dependencies:** T02.01, T02.03, T01.04
**Rollback:** Revert PR
**Notes:** -

### T03.02 -- AuthMiddleware bearer extraction (COMP-005)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | Bearer token extraction and verification in request pipeline. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, auth, token |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/spec.md`
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Deliverables:**
- `src/middleware/auth-middleware.ts`

**Steps:**
1. **[PLANNING]** Read COMP-005 spec
2. **[PLANNING]** Identify request-pipeline integration point
3. **[EXECUTION]** Implement Authorization: Bearer extraction
4. **[EXECUTION]** Verify via JwtService and attach userId to request
5. **[VERIFICATION]** Run TEST-M3-004
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Returns 401 on missing or invalid Bearer token
- Attaches `req.userId` after successful verification
- Rejects expired tokens with 401
- Evidence file `D-0011/evidence.md` recorded

**Validation:**
- Manual check: profile endpoint reaches handler with valid bearer
- Evidence: linkable artifact produced

**Dependencies:** T02.02
**Rollback:** Revert PR
**Notes:** -

### T03.03 -- POST /auth/login endpoint (FR-AUTH.1 + API-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | Authenticate via email/password, return AuthTokenPair. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, auth, password |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0012/spec.md`
- `TASKLIST_ROOT/artifacts/D-0012/evidence.md`

**Deliverables:**
- `src/routes/auth/login.ts` HTTP handler

**Steps:**
1. **[PLANNING]** Confirm request schema
2. **[PLANNING]** Wire into RoutesIndex
3. **[EXECUTION]** Implement handler delegating to AuthService.login
4. **[EXECUTION]** Map outcomes to 200/401/403/429
5. **[VERIFICATION]** Run TEST-M3-001
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Valid credentials → 200 with AuthTokenPair body
- Invalid → 401 with generic body (no enumeration)
- Locked account → 403; rate-limit exceeded → 429
- Evidence file `D-0012/evidence.md` recorded

**Validation:**
- Manual check: TEST-M3-001 negative paths all green
- Evidence: linkable artifact produced

**Dependencies:** T03.01
**Rollback:** Disable route via CFG-002
**Notes:** -

### T03.04 -- POST /auth/register endpoint (FR-AUTH.2 + API-002)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | Register new user with validation and bcrypt hash. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, auth, password |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0013/spec.md`
- `TASKLIST_ROOT/artifacts/D-0013/evidence.md`

**Deliverables:**
- `src/routes/auth/register.ts` HTTP handler

**Steps:**
1. **[PLANNING]** Confirm request schema (email/password/display_name)
2. **[PLANNING]** Wire into RoutesIndex
3. **[EXECUTION]** Implement handler invoking AuthService.register
4. **[EXECUTION]** Enforce VALID-001/002 + dup check
5. **[VERIFICATION]** Run TEST-M3-002
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Valid input → 201 with public profile
- Duplicate email → 409
- Weak password / bad email → 400
- Evidence file `D-0013/evidence.md` recorded

**Validation:**
- Manual check: TEST-M3-002 covers happy + negative paths
- Evidence: linkable artifact produced

**Dependencies:** T03.01, T02.04
**Rollback:** Disable route via CFG-002
**Notes:** -

### T03.05 -- POST /auth/refresh with rotation (FR-AUTH.3 + API-003)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | Rotate refresh token and issue new access token; revoke-all on replay. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, token, auth |
| Tier | STRICT |
| Confidence | [████████--] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0014/spec.md`
- `TASKLIST_ROOT/artifacts/D-0014/evidence.md`

**Deliverables:**
- `src/routes/auth/refresh.ts` HTTP handler

**Steps:**
1. **[PLANNING]** Confirm cookie scope `path=/auth/refresh`
2. **[PLANNING]** Confirm RotateOnReplay semantics
3. **[EXECUTION]** Implement handler invoking TokenManager.refresh
4. **[EXECUTION]** Set rotated cookie with Secure,HttpOnly,SameSite=Strict
5. **[VERIFICATION]** Run TEST-M3-003 (rotation + replay)
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Valid refresh → 200 + new pair; old token revoked
- Replayed token → revoke-all-user-tokens
- Cookie attributes: Secure,HttpOnly,SameSite=Strict,path=/auth/refresh
- Evidence file `D-0014/evidence.md` recorded

**Validation:**
- Manual check: TEST-M3-003 green
- Evidence: linkable artifact produced

**Dependencies:** T03.01, T02.03
**Rollback:** Disable route via CFG-002
**Notes:** -

### T03.06 -- Checkpoint: M3 Authenticated Flow Verified (Mid-phase)

**Purpose:** Verify the login/register/refresh path before adding profile/reset endpoints — catches replay-detection regressions early.
**Checkpoint Report Path:** `checkpoints/CP-P03-MID-AUTHFLOW.md`

**Verification:**
- TEST-M3-001 (login negative paths) green
- TEST-M3-002 (register dup + policy) green
- TEST-M3-003 (refresh rotation + replay) green

**Exit Criteria:**
- All three core endpoints answer behind feature flag
- Cookie attributes verified for /auth/refresh
- Replay detection revokes all user tokens (SC-7 partial)

### T03.07 -- GET /auth/me profile retrieval (FR-AUTH.4 + API-004)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | Return authenticated user's public profile. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | auth |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0015 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0015/spec.md`
- `TASKLIST_ROOT/artifacts/D-0015/evidence.md`

**Deliverables:**
- `src/routes/auth/me.ts` HTTP handler

**Steps:**
1. **[PLANNING]** Confirm response schema (id/email/display_name/created_at)
2. **[PLANNING]** Wire AuthMiddleware
3. **[EXECUTION]** Implement handler returning whitelisted DTO
4. **[EXECUTION]** Enforce DTO-001 field whitelist
5. **[VERIFICATION]** Run TEST-M3-004
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Valid bearer → 200 with whitelisted profile
- Expired/invalid → 401
- Response excludes password_hash and token_hash
- Evidence file `D-0015/evidence.md` recorded

**Validation:**
- Manual check: TEST-M3-004 + DTO-001 introspection green
- Evidence: linkable artifact produced

**Dependencies:** T03.02
**Rollback:** Disable route via CFG-002
**Notes:** -

### T03.08 -- Password reset request + confirm endpoints (FR-AUTH.5 + API-005/006)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | Two-step flow: request reset email, confirm new password; revoke all sessions on success. |
| Effort | L |
| Risk | High |
| Risk Drivers | security, auth, password |
| Tier | STRICT |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0016 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0016/spec.md`
- `TASKLIST_ROOT/artifacts/D-0016/evidence.md`

**Deliverables:**
- `src/routes/auth/password-reset.ts` for request + confirm

**Steps:**
1. **[PLANNING]** Confirm OI-10 vendor selection for COMP-010
2. **[PLANNING]** Confirm reset-token TTL = 1h, single-use
3. **[EXECUTION]** Implement request endpoint (always 202)
4. **[EXECUTION]** Implement confirm endpoint that revokes all sessions
5. **[VERIFICATION]** Run TEST-M3-005
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- Request endpoint returns 202 regardless of email existence
- Confirm with valid token → 204 + all refresh tokens revoked
- Reset token reused → 400
- Evidence file `D-0016/evidence.md` recorded

**Validation:**
- Manual check: TEST-M3-005 covers dispatch + confirm + session-invalidation
- Evidence: linkable artifact produced

**Dependencies:** T03.01
**Rollback:** Disable routes via CFG-002
**Notes:** Risk drivers include `security`, `auth`, `password` so STRICT.

### T03.09 -- Login rate-limit middleware (RATE-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Enforce 5-attempts-per-minute-per-IP on login endpoint. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | security, performance |
| Tier | STRICT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0017 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0017/spec.md`
- `TASKLIST_ROOT/artifacts/D-0017/evidence.md`

**Deliverables:**
- `src/middleware/rate-limit.ts` (login + reset configurations)

**Steps:**
1. **[PLANNING]** Confirm shared store (Redis vs in-memory) per CFG-001
2. **[PLANNING]** Identify exempt routes (health-checks)
3. **[EXECUTION]** Implement IP-keyed counter for login
4. **[EXECUTION]** Implement per-email throttle for reset
5. **[VERIFICATION]** Run SC-4 burst test
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- 6th login attempt within 1 minute returns 429
- Counter resets after 1 minute window
- Health-check paths bypass the middleware
- Evidence file `D-0017/evidence.md` recorded

**Validation:**
- Manual check: SC-4 burst test triggers 429 on attempt 6
- Evidence: linkable artifact produced

**Dependencies:** T03.03
**Rollback:** Disable middleware in app config
**Notes:** -

### T03.10 -- Uniform auth error contract (ERR-001 + DTO-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | Standardized error envelope + DTO whitelist preventing user enumeration and PII leak. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | security, auth |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0018 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0018/spec.md`
- `TASKLIST_ROOT/artifacts/D-0018/evidence.md`

**Deliverables:**
- `src/auth/errors.ts` and `src/auth/dto/whitelist.ts`

**Steps:**
1. **[PLANNING]** Read ERR-001 + DTO-001 acceptance criteria
2. **[PLANNING]** Identify all auth response surfaces
3. **[EXECUTION]** Implement error envelope with generic 401
4. **[EXECUTION]** Implement DTO whitelist serializer
5. **[VERIFICATION]** Run TEST-M3-006
6. **[COMPLETION]** Append evidence path

**Acceptance Criteria:**
- 401 body identical for invalid email vs invalid password
- 403 only emitted on locked account
- DTO whitelist excludes password_hash, token_hash, reset_hash
- Evidence file `D-0018/evidence.md` recorded

**Validation:**
- Manual check: TEST-M3-006 negative tests green
- Evidence: linkable artifact produced

**Dependencies:** T03.01
**Rollback:** Revert PR
**Notes:** -

### T03.11 -- Checkpoint: M3 Endpoints Verified (End of Phase)

**Purpose:** Verify all `/auth/*` endpoints integrate cleanly behind CFG-002 and pass integration tests TEST-M3-001..006.
**Checkpoint Report Path:** `checkpoints/CP-P03-END.md`

**Verification:**
- TEST-M3-004 (profile retrieval) green
- TEST-M3-005 (password reset flow) green
- TEST-M3-006 (error contract) green

**Exit Criteria:**
- All five `/auth/*` endpoints live behind CFG-002
- Rate-limit middleware enforced on login + reset request
- Uniform error contract verified by negative tests
