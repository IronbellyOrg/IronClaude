# Phase 2 -- Token Management

**Phase Goal:** Deliver stateless JWT RS256 access tokens, opaque Redis-backed refresh tokens with rotation + replay detection, AuthMiddleware for protected routes, feature flag AUTH_TOKEN_REFRESH, token-lifecycle audit logs, and NFR-PERF-003 issuance performance harness -- completing M2.

**Task Count:** 19 (T02.01 - T02.19)

---

## T02.01 -- Clarify: OQ-M1-003 JWT RSA key custody approval

- **Roadmap Item IDs:** -- (Clarification Task)
- **Why:** OQ-M1-003 is the only open question without a committed default; JwtService signing key custody (KMS vs local secret) blocks M2 token issuance.
- **Effort:** XS
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** EXEMPT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Skip verification
- **MCP Required:** None
- **MCP Preferred:** None
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0025
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0025/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0025 Approved decision artifact capturing key-custody choice (KMS vs filesystem secret), rotation cadence, audit owner.

**Steps:**
1. **[PLANNING]** Draft decision options memo citing OQ-M1-003 risks.
2. **[PLANNING]** Circulate to Security, Platform, Compliance stakeholders.
3. **[EXECUTION]** Record signed decision in `TASKLIST_ROOT/artifacts/D-0025/spec.md`.
4. **[COMPLETION]** Update JwtService configuration note in T02.03 to reflect decision.

**Acceptance Criteria:**
- Decision recorded in writing with owner signature date.
- Impacts on T02.03 (JwtService) and T06.09 (OPS-004 retention) identified.
- Artifact lives under TASKLIST_ROOT/artifacts/D-0025/spec.md.
- Decision reviewed with stakeholder(s).

**Validation:**
- Manual check: Reviewed with stakeholder(s).
- Evidence: linkable artifact produced (decision memo).

**Dependencies:** None
**Rollback:** Re-open OQ-M1-003 and halt T02.03.
**Notes:** Stops the M2 bus if unresolved; does not implement code.

---

## T02.02 -- DM-002 RefreshToken Redis data model

- **Roadmap Item IDs:** R-025
- **Why:** Redis hash set keyed by user_id holding refresh-token records; 5-per-user cap with oldest-eviction enforces FR-AUTH-004 rotation policy.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** data, schema
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `models/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0026
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0026/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0026 Redis key schema `rt:<user_id>` -> hash of token_id -> {hash, issued_at, family_id, ua_fingerprint, revoked}; 7-day TTL per record.

**Steps:**
1. **[PLANNING]** Confirm Redis 7 availability + deployment secrets.
2. **[EXECUTION]** Implement Redis adapter with add/get/revoke/list functions.
3. **[EXECUTION]** Enforce 5-entry cap with LRU eviction based on issued_at.
4. **[VERIFICATION]** Unit-test eviction, TTL, revoke paths.
5. **[COMPLETION]** Document key layout in notes.md.

**Acceptance Criteria:**
- Redis hash layout matches roadmap contract.
- 5th insert evicts oldest record.
- Records auto-expire after 7 days.
- Hash adapter isolated via interface for test doubles.

**Validation:**
- Manual check: spin up redis-cli and verify hash layout after programmatic insert.
- Evidence: linkable artifact produced (adapter unit test log).

**Dependencies:** T02.01
**Rollback:** Drop keys `rt:*` and unload adapter.
**Notes:** Cap-eviction policy committed default per CONFLICT-3.

---

## T02.03 -- COMP-JWTSVC JwtService RS256 signer/verifier

- **Roadmap Item IDs:** R-026
- **Why:** Central JWT signing/verification with 2048-bit RSA, quarterly key rotation, 30-sec skew leeway (SEC-CLOCK-SKEW).
- **Effort:** L
- **Risk:** High
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `crypto/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0027
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0027/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0027 `src/services/jwt-service.ts` with `sign(claims)`, `verify(token)`, `rotateKeys()`; supports dual-key verification during rotation.

**Steps:**
1. **[PLANNING]** Load decision artifact D-0025 for key custody.
2. **[EXECUTION]** Implement RS256 sign/verify using node-jose or jose.
3. **[EXECUTION]** Add `kid` header and resolve public key by kid.
4. **[EXECUTION]** Implement rotateKeys() that retains N-1 verify-only key for 30 days.
5. **[VERIFICATION]** Unit tests (see T02.14) for sign/verify/rotation/expiry/skew.
6. **[COMPLETION]** Document rotation runbook path.

**Acceptance Criteria:**
- Tokens signed RS256 with 2048-bit RSA key.
- Verification accepts current and previous key via kid.
- Rotation API hot-swaps keys without verify outage.
- 30-second clock skew tolerated (SEC-CLOCK-SKEW).

**Validation:**
- Manual check: unit test suite TEST-003 green.
- Evidence: linkable artifact produced (jwt-service unit test log).

**Dependencies:** T02.01
**Rollback:** Revert to previous key only.
**Notes:** Access token ttl 15m; quarterly rotation per NFR-SEC-002.

---

## T02.04 -- COMP-TOKMGR TokenManager service

- **Roadmap Item IDs:** R-027
- **Why:** Issues/rotates/revokes refresh tokens using Redis adapter; enforces family revocation on replay.
- **Effort:** L
- **Risk:** High
- **Risk Drivers:** security, auth, rollback
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0028
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0028/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0028 `src/services/token-manager.ts` with `issuePair(userId)`, `rotate(refreshToken)`, `revokeFamily(familyId)`.

**Steps:**
1. **[PLANNING]** Define family_id + token_id generation (ULID).
2. **[EXECUTION]** Implement issuePair: JwtService.sign + Redis insert with SHA-256 hash.
3. **[EXECUTION]** Implement rotate: verify lineage, issue new, mark old revoked.
4. **[EXECUTION]** Detect replay: if presented token already revoked, revoke entire family_id.
5. **[VERIFICATION]** Integration test (see T02.15) covers rotate + replay detection.
6. **[COMPLETION]** Attach sequence diagram in notes.md.

**Acceptance Criteria:**
- Pair issuance stores hashed refresh token, never plaintext.
- Rotation returns new pair and invalidates old in single atomic op.
- Replay of revoked token triggers family-wide revocation.
- revokeFamily removes all entries under family_id.

**Validation:**
- Manual check: integration test TEST-005 assertion for replay -> 401.
- Evidence: linkable artifact produced (token-manager test log).

**Dependencies:** T02.02, T02.03
**Rollback:** Disable feature flag AUTH_TOKEN_REFRESH (T02.11).
**Notes:** Implements FR-AUTH-004 rotation + replay rule.

---

## T02.05 -- NFR-SEC-002 Token security enforcement

- **Roadmap Item IDs:** R-028
- **Why:** Guardrails ensuring access tokens are RS256-only and refresh tokens are SHA-256 hashed at rest.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `security/`, `crypto/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0029
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0029/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0029 Config guard `token-policy.ts` rejecting any non-RS256 alg and any plaintext refresh persistence; runtime assertion + tests.

**Steps:**
1. **[PLANNING]** Enumerate forbidden algorithms (HS256, none, etc.).
2. **[EXECUTION]** Add runtime assertion in JwtService.sign/verify paths.
3. **[EXECUTION]** Add adapter guard rejecting plaintext refresh token write.
4. **[VERIFICATION]** Unit test attempts HS256 sign -> throws.
5. **[COMPLETION]** Document policy in notes.md.

**Acceptance Criteria:**
- Non-RS256 signatures rejected at sign and verify.
- Refresh adapter refuses writes lacking sha256Hash field.
- Guard violation produces INVARIANT_VIOLATED error and audit entry.
- Policy file referenced from NFR-SEC-002.

**Validation:**
- Manual check: alg swap test returns guard error.
- Evidence: linkable artifact produced (policy test log).

**Dependencies:** T02.03, T02.04
**Rollback:** Policy disabled only via explicit break-glass flag.
**Notes:** Pairs with T02.18 SEC-RT-HASH.

---

Checkpoint: Phase 2 / Tasks 1-5

- **Purpose:** Confirm decision and foundational token infrastructure before wiring endpoints.
- **Verification:**
  - D-0025 decision artifact recorded.
  - JwtService RS256 sign/verify operational.
  - Redis refresh-token adapter enforces cap + TTL.
- **Exit Criteria:**
  - No STRICT components missing DI bindings.
  - Token policy guard rejects HS256 and plaintext writes.
  - Evidence paths populated for T02.01-T02.05.

---

## T02.06 -- FR-AUTH-003 Login token issuance path

- **Roadmap Item IDs:** R-029
- **Why:** AuthService.login now issues access+refresh pair after credential check; completes Phase 1 stub.
- **Effort:** L
- **Risk:** High
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0030
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0030/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0030 AuthService.login extension wiring TokenManager.issuePair; response shape `{access_token, refresh_token, expires_in}`.

**Steps:**
1. **[PLANNING]** Confirm response schema per TDD Section 8.2.
2. **[EXECUTION]** Invoke TokenManager.issuePair after credential verification.
3. **[EXECUTION]** Update /auth/login route to return new shape.
4. **[VERIFICATION]** Update TEST-001 to assert access_token + refresh_token present.
5. **[COMPLETION]** Remove Phase 1 stub TODO.

**Acceptance Criteria:**
- Valid login returns both tokens and expires_in=900 (15m).
- Tokens satisfy NFR-SEC-002 guards.
- Audit event login_success now includes token_id + family_id.
- Failed login still returns 401 without tokens.

**Validation:**
- Manual check: login integration test asserts non-empty tokens.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T02.04, T02.05, T01.07
**Rollback:** Feature flag AUTH_TOKEN_REFRESH (T02.11) disables new path.
**Notes:** Completes the token issuance stub left in Phase 1.

---

## T02.07 -- FR-AUTH-004 Token refresh with rotation + replay

- **Roadmap Item IDs:** R-030
- **Why:** POST /auth/refresh implements token rotation + replay detection per security model.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0031
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0031/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0031 `/auth/refresh` handler + TokenManager.rotate wiring; 401 on invalid/replay with family revocation.

**Steps:**
1. **[PLANNING]** Confirm replay trigger fires revokeFamily exactly once.
2. **[EXECUTION]** Implement handler: validate refresh token, call rotate.
3. **[EXECUTION]** Map replay error to 401 + unified envelope.
4. **[VERIFICATION]** Integration test TEST-005 covers rotate + replay.
5. **[COMPLETION]** Record audit events for rotation and family revocation.

**Acceptance Criteria:**
- Valid refresh returns new pair and invalidates old.
- Replay returns 401 and revokes full family.
- Audit events `token_rotated` and `token_family_revoked` emitted.
- Route registered under AUTH_TOKEN_REFRESH flag (T02.11).

**Validation:**
- Manual check: replay a previously-rotated token -> 401.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T02.04, T02.06
**Rollback:** Feature flag disable.
**Notes:** Connected to metric METRIC-REFRESH (T02.13).

---

## T02.08 -- API-003 POST /auth/login HTTP contract

- **Roadmap Item IDs:** R-031
- **Why:** Finalizes login HTTP contract: 200 tokens, 401 invalid, 423 locked, unified envelope.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0032
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0032/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0032 Updated /auth/login route contract test ensuring 200/401/423 + tokens response shape.

**Steps:**
1. **[PLANNING]** Enumerate all response codes and payload shape.
2. **[EXECUTION]** Update OpenAPI yaml for /auth/login.
3. **[EXECUTION]** Extend contract tests to cover 423 lock path.
4. **[VERIFICATION]** Run contract suite and capture diff.
5. **[COMPLETION]** Update notes.md with OpenAPI hash.

**Acceptance Criteria:**
- 200 response shape equals `{access_token, refresh_token, expires_in}`.
- 401 and 423 both use unified envelope with distinct codes.
- OpenAPI committed under `docs/openapi/auth.yaml`.
- Contract test suite green.

**Validation:**
- Manual check: run contract tests.
- Evidence: linkable artifact produced (OpenAPI diff + test log).

**Dependencies:** T02.06, T01.11
**Rollback:** Revert route contract commit.
**Notes:** Ties together Phase 1 lockout with Phase 2 tokens.

---

## T02.09 -- API-004 POST /auth/refresh HTTP contract

- **Roadmap Item IDs:** R-032
- **Why:** Finalizes refresh contract: 200 new pair, 401 invalid/replay, 429 rate limit.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0033
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0033/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0033 /auth/refresh OpenAPI entry + contract tests covering 200/401/429.

**Steps:**
1. **[PLANNING]** Draft refresh rate-limit policy (60/min per refresh token).
2. **[EXECUTION]** Add OpenAPI entry for /auth/refresh.
3. **[EXECUTION]** Wire rate limiter + 429 envelope response.
4. **[VERIFICATION]** Contract test suite green for all codes.
5. **[COMPLETION]** Update notes.md with policy.

**Acceptance Criteria:**
- 200 response returns new pair.
- 401 returned for expired, replayed, or unknown token.
- 429 returned if > 60 refresh attempts per token per minute.
- OpenAPI committed alongside login.

**Validation:**
- Manual check: run contract tests.
- Evidence: linkable artifact produced (OpenAPI + test log).

**Dependencies:** T02.07
**Rollback:** Disable /auth/refresh route.
**Notes:** 429 path relies on standalone limiter for refresh.

---

## T02.10 -- COMP-AUTHMW AuthMiddleware

- **Roadmap Item IDs:** R-033
- **Why:** Express middleware extracts bearer token, verifies via JwtService, attaches req.user; foundation for protected routes.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0034
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0034/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0034 `src/middleware/auth.ts` verifying Authorization: Bearer header, handling 401 for invalid tokens.

**Steps:**
1. **[PLANNING]** Enumerate protected route catalog (profile, password, logout, admin).
2. **[EXECUTION]** Implement extract + verify flow with JwtService.
3. **[EXECUTION]** Attach `req.user = {user_id, roles}` on success.
4. **[EXECUTION]** Map all auth-middleware errors to 401 envelope.
5. **[VERIFICATION]** Fixture test via TEST-ME (T02.16).
6. **[COMPLETION]** Document usage pattern in notes.md.

**Acceptance Criteria:**
- Missing Authorization header returns 401 envelope.
- Expired/invalid token returns 401 envelope.
- Valid token attaches req.user with sub + roles claims.
- Middleware respects SEC-CLOCK-SKEW (T02.19).

**Validation:**
- Manual check: curl protected route with/without token.
- Evidence: linkable artifact produced (middleware unit test log).

**Dependencies:** T02.03
**Rollback:** Apply middleware only after feature-flag check.
**Notes:** Required by Phase 3 profile endpoints.

---

Checkpoint: Phase 2 / Tasks 6-10

- **Purpose:** Validate login/refresh end-to-end and middleware-protected route surface before flag rollout.
- **Verification:**
  - /auth/login returns tokens + 423 when locked.
  - /auth/refresh rotates token and rejects replay.
  - AuthMiddleware attaches req.user on valid bearer token.
- **Exit Criteria:**
  - Contract tests for /auth/login and /auth/refresh green.
  - Audit events token_issued, token_rotated, token_family_revoked emitted.
  - req.user populated on /profile fixture test.

---

## T02.11 -- FEAT-REFRESH-FLAG AUTH_TOKEN_REFRESH feature flag

- **Roadmap Item IDs:** R-034
- **Why:** LaunchDarkly gate controlling new refresh flow; required for phased rollout + automatic rollback.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0035
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0035/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0035 LaunchDarkly flag AUTH_TOKEN_REFRESH + runtime gate wrapping refresh handler.

**Steps:**
1. **[PLANNING]** Confirm LaunchDarkly SDK + env keys.
2. **[EXECUTION]** Add flag in LaunchDarkly dashboard and source config.
3. **[EXECUTION]** Wrap /auth/refresh handler with flag check; off -> 404 Not Found.
4. **[VERIFICATION]** Toggle flag on/off in staging and observe behavior.
5. **[COMPLETION]** Document flag rollout plan in notes.md.

**Acceptance Criteria:**
- Flag `AUTH_TOKEN_REFRESH` exists in LaunchDarkly.
- Off state causes /auth/refresh to return 404.
- Flag change reflected within SDK polling interval.
- Config documented in notes.md.

**Validation:**
- Manual check: toggle flag in staging and hit /auth/refresh.
- Evidence: linkable artifact produced (LD dashboard screenshot + test log).

**Dependencies:** T02.09
**Rollback:** Flag off disables new path.
**Notes:** Rollout cadence drives Phase 6 ROLLBACK-AUTO.

---

## T02.12 -- NFR-PERF-003 Token issuance performance harness

- **Roadmap Item IDs:** R-035
- **Why:** p95 < 100ms at 100 RPS sustained 5 min; gates Phase 2 completion.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** performance
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0036
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0036/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0036 `tests/load/token-issuance.js` k6 script with 100 RPS 5m stage + threshold `p(95)<100ms`.

**Steps:**
1. **[PLANNING]** Confirm staging env token issuance capacity.
2. **[EXECUTION]** Author k6 script covering /auth/login + /auth/refresh.
3. **[EXECUTION]** Register threshold and custom tag per endpoint.
4. **[VERIFICATION]** Run script; attach report.
5. **[COMPLETION]** Record baseline in evidence path.

**Acceptance Criteria:**
- p95 under 100ms at 100 RPS 5m.
- Error rate < 1%.
- Report committed as baseline.
- Threshold assertions cause exit code 1 on regression.

**Validation:**
- Manual check: `k6 run tests/load/token-issuance.js`.
- Evidence: linkable artifact produced (k6 report).

**Dependencies:** T02.06, T02.07
**Rollback:** Remove script.
**Notes:** Distinct from login script T01.18.

---

## T02.13 -- METRIC-REFRESH Metrics for refresh flow

- **Roadmap Item IDs:** R-036
- **Why:** Prometheus counters + histogram for refresh operations; feeds ALERT-LATENCY and ROLLBACK-AUTO-ERR.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0037
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0037/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0037 `auth_refresh_total{outcome}` counter + `auth_refresh_duration_ms` histogram.

**Steps:**
1. **[PLANNING]** Define outcome labels success|invalid|replay|rate_limited.
2. **[EXECUTION]** Instrument /auth/refresh handler.
3. **[VERIFICATION]** Scrape /metrics and assert counter + histogram present.

**Acceptance Criteria:**
- Counter increments with correct outcome.
- Histogram bucket boundaries aligned to SLO (100ms p95).
- Metrics exposed at /metrics.
- Low-cardinality labels only.

**Validation:**
- Manual check: curl /metrics | grep auth_refresh.
- Evidence: linkable artifact produced (metrics snapshot).

**Dependencies:** T02.07
**Rollback:** Remove instrumentation.
**Notes:** Enables ROLLBACK-AUTO-ERR signal in Phase 6.

---

## T02.14 -- TEST-003 JwtService unit suite >= 90% coverage

- **Roadmap Item IDs:** R-037
- **Why:** Regression gate for JwtService sign/verify/rotation/expiry/skew.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0038
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0038/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0038 `tests/unit/jwt-service.spec.ts` covering sign, verify, rotateKeys, expired token, wrong kid, clock skew edges.

**Steps:**
1. **[PLANNING]** Enumerate coverage targets (>=90% statements).
2. **[EXECUTION]** Author unit cases for each branch.
3. **[EXECUTION]** Use fake clock to exercise expiry + skew.
4. **[VERIFICATION]** Run coverage report and assert >=90%.

**Acceptance Criteria:**
- Statement coverage >=90% for jwt-service.ts.
- Rotation path produces verify against both keys.
- 30-sec skew test passes.
- Coverage report stored at evidence path.

**Validation:**
- Manual check: `pytest --cov` report for jwt-service module.
- Evidence: linkable artifact produced (coverage report).

**Dependencies:** T02.03
**Rollback:** Revert new test file.
**Notes:** Coverage gate enforced in CI.

---

## T02.15 -- TEST-005 Refresh rotation integration test

- **Roadmap Item IDs:** R-038
- **Why:** Integration regression for login + refresh + replay -> 401 with family revocation.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0039
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0039/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0039 `tests/integration/refresh.spec.ts` login -> refresh -> replay -> family revoke; assertions on 200/401/audit.

**Steps:**
1. **[PLANNING]** Seed user and obtain token pair.
2. **[EXECUTION]** Rotate once; attempt rotate with original token; assert 401 + revokeFamily.
3. **[EXECUTION]** Query audit log for token_rotated + token_family_revoked.
4. **[VERIFICATION]** Assert Redis entries for family are cleared.

**Acceptance Criteria:**
- Legitimate rotation returns 200 new pair.
- Replay attempt returns 401 envelope.
- All tokens in family are revoked/deleted.
- Audit trail recorded.

**Validation:**
- Manual check: run integration test file.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T02.07
**Rollback:** Remove test file.
**Notes:** Critical replay test; do not reduce assertions.

---

Checkpoint: Phase 2 / Tasks 11-15

- **Purpose:** Confirm observability + flag + performance verified before security hardening tail.
- **Verification:**
  - AUTH_TOKEN_REFRESH flag toggles behavior.
  - k6 token issuance threshold green.
  - TEST-003 + TEST-005 green.
- **Exit Criteria:**
  - METRIC-REFRESH metrics visible.
  - Coverage >=90% for JwtService.
  - No open STRICT defect.

---

## T02.16 -- TEST-ME GET /profile protected-route fixture

- **Roadmap Item IDs:** R-039
- **Why:** Standing integration test for AuthMiddleware behavior; used to pin Phase 3 profile routes.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0040
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0040/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0040 `tests/integration/me.spec.ts` hitting GET /profile with/without token; asserts 200/401.

**Steps:**
1. **[PLANNING]** Prepare seeded user + token.
2. **[EXECUTION]** Call GET /profile without Authorization -> assert 401.
3. **[EXECUTION]** Call with valid bearer -> assert 200 profile body.
4. **[VERIFICATION]** Confirm req.user.sub equals user_id in response.

**Acceptance Criteria:**
- 401 path emits unified envelope.
- 200 path returns profile fields (no password_hash).
- Middleware verifies token via JwtService.
- Test runs under 5 seconds.

**Validation:**
- Manual check: run integration test file.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T02.10
**Rollback:** Remove test file.
**Notes:** Fixture used by Phase 3 tests (T03.12, T03.13).

---

## T02.17 -- OPS-LOG-M2 Token-lifecycle audit logs

- **Roadmap Item IDs:** R-040
- **Why:** Extend DM-AUDIT event_type enum with token-lifecycle events; required by OPS-004 12-month retention.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0041
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0041/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0041 Migration adding token_issued, token_rotated, token_revoked, token_family_revoked to enum; service wiring.

**Steps:**
1. **[PLANNING]** Audit enum current values and confirm migration strategy.
2. **[EXECUTION]** Write additive enum migration.
3. **[EXECUTION]** Wire TokenManager emits for the four events.
4. **[VERIFICATION]** Integration test asserts audit entries on rotation.

**Acceptance Criteria:**
- Enum expanded non-destructively.
- Each TokenManager operation emits exactly one audit event.
- Audit payload includes family_id + token_id (hashed).
- Migration reversible.

**Validation:**
- Manual check: query auth_audit_log post-rotation.
- Evidence: linkable artifact produced (log query output).

**Dependencies:** T01.02, T02.04
**Rollback:** Reverse enum migration (rename values).
**Notes:** Feeds OPS-004 archival.

---

## T02.18 -- SEC-RT-HASH Refresh token hashing at rest

- **Roadmap Item IDs:** R-041
- **Why:** SHA-256 stored in Redis; plaintext never persisted; enforces NFR-SEC-002.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** security, data
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `security/`, `crypto/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0042
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0042/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0042 `src/security/token-hash.ts` computing SHA-256 hash of refresh token string; adapter enforces hash presence.

**Steps:**
1. **[PLANNING]** Select Node crypto subtle SHA-256.
2. **[EXECUTION]** Implement hash helper with constant-time compare.
3. **[EXECUTION]** Enforce hash write in TokenManager/Redis adapter.
4. **[VERIFICATION]** Unit test hash output + constant-time compare.

**Acceptance Criteria:**
- Only SHA-256 hash written to Redis.
- No plaintext refresh token appears in logs or metrics.
- Adapter throws if called with plaintext.
- Unit tests cover equal/different paths.

**Validation:**
- Manual check: inspect Redis value and confirm 64 hex chars.
- Evidence: linkable artifact produced (redis-cli capture).

**Dependencies:** T02.02, T02.04
**Rollback:** Policy disabled only via break-glass flag.
**Notes:** Paired with NFR-SEC-002 guard.

---

## T02.19 -- SEC-CLOCK-SKEW ±30s tolerance config

- **Roadmap Item IDs:** R-042
- **Why:** JwtService configured with 30-sec leeway to absorb NTP drift across services.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0043
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0043/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0043 JwtService config exposing `leewaySeconds = 30`; unit test rejecting tokens older than leeway + 15m.

**Steps:**
1. **[PLANNING]** Confirm target JWT library leeway API.
2. **[EXECUTION]** Set leeway in verify options.
3. **[VERIFICATION]** Unit test tokens at +/-29s, +/-31s boundaries.

**Acceptance Criteria:**
- Tokens within +/-30s of issuer clock accepted.
- Tokens beyond tolerance rejected with TOKEN_EXPIRED.
- Leeway exposed as config constant.
- Referenced by NFR-SEC-002 docs.

**Validation:**
- Manual check: run skew unit test matrix.
- Evidence: linkable artifact produced (unit test log).

**Dependencies:** T02.03
**Rollback:** Reset leeway to 0.
**Notes:** Closes NFR-SEC-002 token security requirements for M2.

---

Checkpoint: End of Phase 2

- **Purpose:** Confirm M2 token management is GA-quality before Phase 3 password & profile work.
- **Verification:**
  - End-to-end login + refresh + replay demo green.
  - AUTH_TOKEN_REFRESH flag verified in staging.
  - Audit events for token lifecycle observed in auth_audit_log.
- **Exit Criteria:**
  - M2 DoD satisfied per roadmap.
  - No open STRICT task.
  - Clarification task T02.01 decision published.
