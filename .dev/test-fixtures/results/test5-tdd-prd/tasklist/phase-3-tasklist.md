# Phase 3 -- Profile and Password Management

**Phase Goal:** Deliver GET/PUT /profile, password-change with revoke-all, enumeration-safe password-reset request + confirm flow, reset-token data model, async email dispatcher, and integration tests per M3.

**Task Count:** 13 (T03.01 - T03.13)

---

## T03.01 -- FR-PROF-001 GET /profile

- **Roadmap Item IDs:** R-043
- **Why:** Returns authenticated caller's profile; reuses AuthMiddleware from Phase 2.
- **Effort:** M
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
- **Deliverable IDs:** D-0044
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0044/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0044 `src/routes/profile/get.ts` returning `{user_id, email, display_name, consent_flag, created_at}`; excludes password_hash.

**Steps:**
1. **[PLANNING]** Confirm profile DTO schema.
2. **[EXECUTION]** Implement handler using UserRepo.findById.
3. **[EXECUTION]** Enforce 401 via AuthMiddleware when token absent.
4. **[VERIFICATION]** Contract test for 200/401.
5. **[COMPLETION]** Update OpenAPI.

**Acceptance Criteria:**
- 200 response includes non-sensitive fields only.
- 401 returned if no bearer token.
- Response excludes password_hash and any PII beyond roadmap schema.
- Route documented in docs/openapi/auth.yaml.

**Validation:**
- Manual check: curl GET /profile with/without token.
- Evidence: linkable artifact produced (contract log).

**Dependencies:** T02.10
**Rollback:** Unregister route.
**Notes:** Reused by frontend ProfilePage (T04.03).

---

## T03.02 -- FR-PROF-002 PUT /profile display_name only

- **Roadmap Item IDs:** R-044
- **Why:** v1.0 scope limits profile update to display_name to reduce attack surface.
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
- **Deliverable IDs:** D-0045
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0045/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0045 `src/routes/profile/put.ts` accepting only display_name, returning 200 updated profile.

**Steps:**
1. **[PLANNING]** Schema: reject fields outside display_name.
2. **[EXECUTION]** Implement handler invoking UserRepo.updateProfile.
3. **[EXECUTION]** Emit audit event `profile_updated`.
4. **[VERIFICATION]** Contract test for valid / invalid field cases.

**Acceptance Criteria:**
- Only display_name accepted; extra fields rejected 400.
- 200 response returns updated profile summary.
- Audit event recorded.
- 401 when token missing.

**Validation:**
- Manual check: PUT /profile with extra fields returns 400.
- Evidence: linkable artifact produced (contract log).

**Dependencies:** T03.01
**Rollback:** Unregister route.
**Notes:** Broader update scope deferred to post-GA.

---

## T03.03 -- FR-AUTH-005 Password change + revoke-all

- **Roadmap Item IDs:** R-045
- **Why:** Self-service password change must re-hash password AND revoke every refresh-token family for the user.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** security, auth, rollback
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0046
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0046/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0046 AuthService.changePassword + handler wiring verifying old password, updating hash, calling TokenManager.revokeAll(userId).

**Steps:**
1. **[PLANNING]** Confirm revoke-all semantics (purge all families).
2. **[EXECUTION]** Verify old password then hash new password.
3. **[EXECUTION]** Call TokenManager.revokeAll and emit password_changed audit event.
4. **[EXECUTION]** Return 204 No Content.
5. **[VERIFICATION]** Integration test asserts old tokens no longer verify.
6. **[COMPLETION]** Document flow in runbook.

**Acceptance Criteria:**
- Old password required and verified.
- New password hashed at cost 12.
- All existing refresh tokens revoked.
- password_changed audit event emitted.

**Validation:**
- Manual check: after change, replay old refresh token returns 401.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T01.04, T02.04
**Rollback:** Disable handler via flag.
**Notes:** Access tokens expire naturally within 15m.

---

## T03.04 -- FR-AUTH-006 Password reset-request (enumeration-safe)

- **Roadmap Item IDs:** R-046
- **Why:** POST /auth/password/reset-request must return identical 200 whether email exists or not; enumeration-safe.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0047
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0047/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0047 AuthService.requestReset generating SHA-256-hashed reset token, persisting via DM-RESET, enqueuing email; returns 200 regardless.

**Steps:**
1. **[PLANNING]** Confirm token TTL 15m and single-use.
2. **[EXECUTION]** Generate high-entropy token; hash with SHA-256; store in DM-RESET.
3. **[EXECUTION]** Enqueue email via COMP-EMAILQ (T03.07).
4. **[EXECUTION]** Return 200 with generic `{status: 'accepted'}` envelope.
5. **[VERIFICATION]** Integration test compares response time for known/unknown email (timing-safe).

**Acceptance Criteria:**
- Response shape and latency identical for known/unknown email.
- Only hashed token persisted.
- Audit event `password_reset_requested` emitted.
- Email enqueued only when user exists (but response is indistinguishable).

**Validation:**
- Manual check: POST for known + unknown email and diff response.
- Evidence: linkable artifact produced (timing + response log).

**Dependencies:** T03.06, T03.07
**Rollback:** Disable handler via flag.
**Notes:** Enumeration safety is a Phase 3 acceptance gate.

---

## T03.05 -- FR-AUTH-007 Password reset-confirm + session revoke

- **Roadmap Item IDs:** R-047
- **Why:** Confirms new password with single-use token and revokes all sessions.
- **Effort:** M
- **Risk:** High
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 95%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0048
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0048/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0048 AuthService.confirmReset validating hashed reset token, replacing password hash, calling TokenManager.revokeAll.

**Steps:**
1. **[PLANNING]** Confirm hash compare is constant-time.
2. **[EXECUTION]** Lookup reset token by SHA-256 hash; check TTL + not-used.
3. **[EXECUTION]** Hash new password and update UserProfile.
4. **[EXECUTION]** Mark reset token consumed; call TokenManager.revokeAll.
5. **[VERIFICATION]** Integration test TEST-RESET.

**Acceptance Criteria:**
- Invalid/expired token -> 400 envelope.
- Valid token single-use -> 204 No Content.
- All existing refresh tokens revoked.
- Audit events password_reset_confirmed + token_family_revoked emitted.

**Validation:**
- Manual check: rerun with consumed token returns 400.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T03.06, T02.04
**Rollback:** Disable handler via flag.
**Notes:** No password-history requirement in v1.0 scope.

---

Checkpoint: Phase 3 / Tasks 1-5

- **Purpose:** Validate read/update profile and password-change flows before reset machinery and email dispatch.
- **Verification:**
  - GET/PUT /profile contract tests pass.
  - Password change invalidates old refresh tokens.
  - Reset-request returns identical 200 for known/unknown emails.
- **Exit Criteria:**
  - Audit events emitted for profile_updated + password_changed + password_reset_requested.
  - No STRICT failure open.
  - Evidence paths populated.

---

## T03.06 -- DM-RESET Password reset token schema + cleanup

- **Roadmap Item IDs:** R-048
- **Why:** Persistent hashed reset tokens with 15m TTL and cleanup job.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** data, schema
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `models/`, `migrations/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0049
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0049/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0049 Migration creating `password_reset_tokens` (token_hash PK, user_id, expires_at, consumed_at) + cron cleanup script.

**Steps:**
1. **[PLANNING]** Confirm cleanup frequency (hourly).
2. **[EXECUTION]** Write migration with indices (user_id, expires_at).
3. **[EXECUTION]** Commit cron job `scripts/cleanup-reset-tokens.sql`.
4. **[VERIFICATION]** Integration test cleans expired tokens.

**Acceptance Criteria:**
- Schema matches TDD; PK is token_hash.
- Cleanup removes rows where expires_at < now() - 7 days.
- Down migration reverses schema.
- Cleanup runnable via cron.

**Validation:**
- Manual check: insert expired tokens and run cleanup job.
- Evidence: linkable artifact produced (cleanup log).

**Dependencies:** None
**Rollback:** Reverse migration.
**Notes:** Row count metric in Phase 5 observability.

---

## T03.07 -- COMP-EMAILQ Async email dispatcher

- **Roadmap Item IDs:** R-049
- **Why:** BullMQ-backed queue prevents blocking HTTP path; retries on SMTP failure.
- **Effort:** M
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
- **Deliverable IDs:** D-0050
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0050/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0050 `src/email/email-queue.ts` BullMQ worker + send API with template rendering and retry policy.

**Steps:**
1. **[PLANNING]** Confirm BullMQ + Redis capacity; align with refresh-token Redis keyspace.
2. **[EXECUTION]** Implement queue + worker with 3x retry exponential backoff.
3. **[EXECUTION]** Render reset email template with token link.
4. **[VERIFICATION]** Integration test enqueue + process stub.

**Acceptance Criteria:**
- Queue accepts reset email jobs.
- Retries up to 3 times on SMTP failure.
- Template renders user-specific link.
- Metric emitted for queue depth.

**Validation:**
- Manual check: drop SMTP; confirm retries.
- Evidence: linkable artifact produced (queue worker log).

**Dependencies:** None (email server address wired later in T06.10)
**Rollback:** Disable worker process.
**Notes:** Prod SMTP credentials wired by OPS-005 in Phase 6.

---

## T03.08 -- API-005 GET/PUT /profile OpenAPI contract

- **Roadmap Item IDs:** R-050
- **Why:** OpenAPI contract for /profile endpoints to support client generation.
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
- **Deliverable IDs:** D-0051
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0051/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0051 OpenAPI entries for GET and PUT /profile including error envelope schema.

**Steps:**
1. **[PLANNING]** Reuse component schemas from /auth/login.
2. **[EXECUTION]** Author OpenAPI snippets and register in docs/openapi/auth.yaml.
3. **[VERIFICATION]** Run OpenAPI linter + contract tests.

**Acceptance Criteria:**
- Both endpoints documented with 200/400/401 cases.
- Schema references unified error envelope.
- Linter passes with no warnings.
- docs/openapi/auth.yaml version bumped.

**Validation:**
- Manual check: `npx @redocly/cli lint docs/openapi/auth.yaml` clean.
- Evidence: linkable artifact produced (lint log).

**Dependencies:** T03.01, T03.02
**Rollback:** Revert OpenAPI entries.
**Notes:** Required for frontend type generation.

---

## T03.09 -- API-006 POST /auth/password/change contract

- **Roadmap Item IDs:** R-051
- **Why:** HTTP contract for self-service password change.
- **Effort:** S
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
- **Deliverable IDs:** D-0052
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0052/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0052 `/auth/password/change` route + contract test 204 on success, 400 on weak password, 401 on missing token.

**Steps:**
1. **[PLANNING]** Align request body schema (old_password, new_password).
2. **[EXECUTION]** Add validator for password complexity.
3. **[EXECUTION]** Wire AuthService.changePassword.
4. **[VERIFICATION]** Contract test suite.

**Acceptance Criteria:**
- 204 on success.
- 400 on weak new password.
- 401 on missing/expired bearer.
- Audit event emitted once.

**Validation:**
- Manual check: run contract tests.
- Evidence: linkable artifact produced (contract log).

**Dependencies:** T03.03
**Rollback:** Unregister route.
**Notes:** Requires AuthMiddleware protection.

---

## T03.10 -- API-RESET-REQ POST /auth/password/reset-request

- **Roadmap Item IDs:** R-052
- **Why:** Enumeration-safe contract; response identical regardless of email existence.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0053
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0053/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0053 /auth/password/reset-request route returning 200 for all inputs, with rate-limit and enumeration safeguards.

**Steps:**
1. **[PLANNING]** Align response envelope.
2. **[EXECUTION]** Bind handler + rate limiter (3/hour per email + 10/hour per IP).
3. **[VERIFICATION]** Contract test + timing equality.

**Acceptance Criteria:**
- 200 response for every request.
- Identical response latency profile for known/unknown email.
- 429 after 3 requests per email per hour or 10 requests per IP per hour.
- OpenAPI updated.

**Validation:**
- Manual check: curl with known + unknown email, diff response.
- Evidence: linkable artifact produced (timing log).

**Dependencies:** T03.04
**Rollback:** Unregister route.
**Notes:** Timing-safe comparison is a must for enumeration protection.

---

Checkpoint: Phase 3 / Tasks 6-10

- **Purpose:** Validate reset infra (DM-RESET + email queue + routes) before confirm + tests.
- **Verification:**
  - DM-RESET schema + cleanup job run.
  - Email queue processes test jobs.
  - Reset-request and change contracts pass.
- **Exit Criteria:**
  - No STRICT failure open.
  - Enumeration test passes (timing + shape parity).
  - OpenAPI version bumped.

---

## T03.11 -- API-RESET-CONF POST /auth/password/reset-confirm

- **Roadmap Item IDs:** R-053
- **Why:** Confirms password reset with single-use token and revokes sessions.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0054
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0054/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0054 /auth/password/reset-confirm route; 204 on success, 400 on invalid/expired token.

**Steps:**
1. **[PLANNING]** Align request body (token, new_password).
2. **[EXECUTION]** Bind handler invoking AuthService.confirmReset.
3. **[VERIFICATION]** Contract tests for success/expired/used paths.

**Acceptance Criteria:**
- 204 on success (no body).
- 400 on invalid, expired, or consumed token.
- Audit event emitted once.
- Sessions revoked post-confirm.

**Validation:**
- Manual check: confirm with consumed token returns 400.
- Evidence: linkable artifact produced (contract log).

**Dependencies:** T03.05
**Rollback:** Unregister route.
**Notes:** Ties to E2E reset flow.

---

## T03.12 -- TEST-PROFILE Profile integration E2E

- **Roadmap Item IDs:** R-054
- **Why:** E2E verifier: register -> login -> update profile -> assert updated values persist.
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
- **Deliverable IDs:** D-0055
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0055/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0055 `tests/integration/profile.e2e.spec.ts` exercising register + login + GET/PUT /profile.

**Steps:**
1. **[PLANNING]** Seed fresh user.
2. **[EXECUTION]** Register -> login -> call GET -> PUT display_name -> GET.
3. **[VERIFICATION]** Assert display_name persisted.

**Acceptance Criteria:**
- Full flow green.
- Audit events present.
- No secrets in logs.
- Test file path recorded.

**Validation:**
- Manual check: run E2E suite.
- Evidence: linkable artifact produced (E2E log).

**Dependencies:** T03.01, T03.02
**Rollback:** Remove test file.
**Notes:** Companion to T02.16 me.spec.ts.

---

## T03.13 -- TEST-RESET Password reset integration E2E

- **Roadmap Item IDs:** R-055
- **Why:** E2E verifier for reset flow including consumed-token rejection and session revoke.
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
- **Deliverable IDs:** D-0056
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0056/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0056 `tests/integration/password-reset.e2e.spec.ts` covering request -> confirm -> reuse-token rejection.

**Steps:**
1. **[PLANNING]** Stub email worker to capture token.
2. **[EXECUTION]** Call reset-request then reset-confirm with captured token.
3. **[EXECUTION]** Retry confirm with same token -> expect 400.
4. **[VERIFICATION]** Assert old refresh tokens invalid.

**Acceptance Criteria:**
- Reset flow succeeds once.
- Second confirm with same token returns 400.
- Old refresh tokens rejected post-reset.
- Audit entries for request + confirm + family_revoked present.

**Validation:**
- Manual check: run E2E suite.
- Evidence: linkable artifact produced (E2E log).

**Dependencies:** T03.10, T03.11
**Rollback:** Remove test file.
**Notes:** Relies on email queue stubbing.

---

Checkpoint: End of Phase 3

- **Purpose:** M3 password + profile features demo-ready before frontend.
- **Verification:**
  - Profile GET/PUT green.
  - Password change revokes sessions.
  - Password reset request + confirm enumeration-safe.
- **Exit Criteria:**
  - M3 DoD satisfied.
  - OpenAPI current.
  - No STRICT defect open.
