# Roadmap: User Authentication Service (merged from opus + sonnet variants)

## Overview

This roadmap delivers the User Authentication Service in 6 milestones (MEDIUM complexity, 1:2 validation interleave). It merges the opus:architect variant's risk-driven trust-primitive discipline with the sonnet:architect variant's pragmatic milestone boundaries.

The organizing principle is **audit and crypto as dependencies, not afterthoughts** (Opus): every later milestone consumes the audit sink, hasher, and JWT signer established in M1. Within that frame, milestone *boundaries* follow Sonnet's incremental phasing — M1+M2 ship a testable Sprint 1 unit, M3 is a dedicated test/security gate, M4 owns external-dependency complexity (reset + audit query API), M5 assembles the full stack with perf validation, and M6 is the rollout gate.

Two architectural disagreements were resolved in favor of the merged plan: (1) the audit_events table ships in M1's schema and M1's AuditLogger contract — but the SOC2 query API + retention enforcement lands in M4 where its external-dep complexity peers (SendGrid, retention archiver) belong; (2) TokenManager lives in M2 alongside refresh/logout/me, not in M1 — because the refresh contract is architecturally inseparable from issuance, and isolating it from registration's issuance path would force a contract break.

## Milestone Summary

| ID | Title | Type | Priority | Effort | Dependencies | Deliverables | Risk |
|----|-------|------|----------|--------|--------------|--------------|------|
| M1 | Trust Foundation + Auth Schema | SECURITY | P0 | M | None | 5 | High |
| M2 | Identity Core + Session Lifecycle | FEATURE | P0 | L | M1 | 6 | High |
| M3 | Integration Tests + Brute-Force Defense | TEST | P1 | M | M2 | 4 | Med |
| M4 | Password Reset + Audit Compliance | SECURITY | P1 | M | M2, M3 | 4 | Med |
| M5 | Frontend Integration + Perf Validation | FEATURE | P1 | L | M3 | 5 | Med |
| M6 | Production Hardening + Phased Rollout | MIGRATION | P0 | M | M4, M5 | 4 | High |

## Dependency Graph

```
M1 (Trust Foundation + Schema)
   └──► M2 (Identity Core + Session Lifecycle)
            └──► M3 (Integration Tests + Brute-Force Defense)
                     ├──► M4 (Password Reset + Audit Compliance) ──┐
                     └──► M5 (Frontend + Perf Validation) ─────────┤
                                                                   ▼
                                                            M6 (Rollout Gate)
```

Critical path: **M1 → M2 → M3 → (M4 || M5) → M6** (5 hops). M4 and M5 run in parallel after M3 ships, shortening overall delivery by one milestone duration.

---

## M1: Trust Foundation + Auth Schema

### Objective

Establish the three trust primitives — hasher, signer, audit sink — that every later milestone consumes, plus the database schema for users, refresh tokens, and audit events. By making audit a *dependency* of M2+ (rather than a cross-cutting afterthought), we eliminate the retrofit cost when FR-007 / NFR-006 SOC2 review lands and isolate RISK-005 (Critical) crypto correctness to a single milestone.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D1.1 | PostgreSQL 15 schema: `users` (id PK, email UNIQUE, displayName, createdAt, updatedAt, lastLoginAt, roles[], gdpr_consent_at), `refresh_tokens` (id, user_id FK, family_id, token_hash, issued_at, expires_at, revoked_at), `audit_events` (id, user_id, event_type, ip, ts, outcome, metadata JSONB) | Migration scripts checked in; soft-delete on users; UNIQUE constraint on lowercased email; audit_events insert-only |
| D1.2 | PasswordHasher service: bcrypt cost=12 default, pluggable cost-factor interface returning `{hash, cost, algo}` envelope | Unit test asserts cost=12; benchmark < 500ms hash time (SC-007); cost-factor migration is a config change, not a schema change |
| D1.3 | JwtService + key management: RSA 2048-bit keypair generation, JWKS endpoint stub, key-id (`kid`) versioning in JWT header, secrets injected via env-var | RS256 signature verified in unit test; multi-key JWKS resolves by `kid`; quarterly rotation procedure documented |
| D1.4 | AuditLogger sink: append-only Postgres writes via D1.1 schema, structured event envelope (user_id, ts, ip, outcome, event_type, metadata), 12-month retention policy stub | Every event emit traced in unit test; retention policy documented (cron archiver lands in M4) |
| D1.5 | Secrets management contract: env-var injection convention, key-id versioning, no plaintext secrets in logs or error messages | Static analysis check rejects `console.log(req.body.password)` patterns; secrets redacted in error stack traces |

### Dependencies

- None (first milestone)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Wrong bcrypt cost factor shipped | Low | Critical (RISK-005) | Unit test pins cost=12; PasswordHasher envelope makes cost-factor reversible without schema change |
| JWT key compromise without rotation path | Low | High (NFR-005) | JWKS + `kid` versioning lands in M1; rotation drill exercised in M6 before GA |
| Audit emit drift across services | Med | High (RISK-006) | Single AuditLogger contract; every M2+ deliverable has audit-hook line item |

---

## M2: Identity Core + Session Lifecycle

### Objective

Build the identity substrate and complete the session API. Registration must auto-login (issue tokens), so TokenManager — including refresh-token rotation with family tracking — lands here, not in a later milestone. After M2 the backend API is feature-complete for Sprint 1-3 scope: a user can register, log in, refresh, log out, and retrieve their profile.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D2.1 | UserRepo: CRUD over `users` table, email-lowercase normalization, GDPR consent capture at registration | Duplicate email returns 409; consent_at populated on insert; soft-delete preserved (no hard delete) |
| D2.2 | POST /auth/register: validation (email format, password strength), bcrypt via M1.D1.2, audit `REGISTER_*` events | Weak password returns 400; duplicate email returns 409; success returns 201 with auto-login tokens |
| D2.3 | POST /auth/login: timing-safe credential compare, JWT issuance via M1.D1.3, audit `LOGIN_*` events | Invalid credentials return generic 401 (no enumeration); success returns access+refresh token pair; lastLoginAt updated |
| D2.4 | TokenManager service: refresh-token rotation-on-use, family tracking, reuse-detection that revokes entire family on replay (RISK-001 mitigation) | Token replay revokes all sibling tokens; Redis-backed storage with 7-day TTL; family_id propagated |
| D2.5 | POST /auth/refresh + POST /auth/logout + GET /auth/me: exchange refresh for new access token, revoke on logout, return UserProfile from JWT claims | refresh issues new pair + revokes old; logout adds token to revocation list; /auth/me returns 401 for expired/revoked tokens |
| D2.6 | Audit hooks across all M2 endpoints: REGISTER_SUCCESS, REGISTER_FAILED, LOGIN_SUCCESS, LOGIN_FAILED, REFRESH_*, LOGOUT | Every endpoint emits structured event via M1.D1.4 |

### Dependencies

- M1 — schema (D1.1), PasswordHasher (D1.2), JwtService (D1.3), AuditLogger (D1.4)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Token theft via XSS / replay | Med | High (RISK-001) | Refresh-token rotation + reuse detection revokes family; httpOnly cookie option for refresh token (frontend decision deferred to M5) |
| Low registration adoption | Med | High (RISK-004) | Auto-login post-register reduces friction; minimal-friction validation (inline feedback in M5) |
| Account enumeration via login error messages | Low | Med | Generic "Invalid email or password" on all failures; equal-time response via timing-safe compare |

---

## M3: Integration Tests + Brute-Force Defense

### Objective

Lock the M2 API contracts with integration tests, ship brute-force defenses, and validate security baseline. This is a dedicated test/security milestone — not a polish phase — that gates M4 and M5 from building against an unstable surface. Rate limiting is intentionally bundled here because it is both a security control (RISK-002) and an operability concern best validated by the integration test harness being built in the same milestone.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D3.1 | Integration test suite (Supertest + testcontainers) covering all 6 endpoints, happy path + error cases, target ≥90% line coverage on auth modules | All 6 endpoints have positive + negative tests; coverage report ≥90% on AuthService/TokenManager/JwtService/PasswordHasher/UserRepo |
| D3.2 | Account lockout: 5 failed attempts within 15 minutes locks account (FR-001, RISK-002); Redis counter in isolated namespace from session storage | Lockout triggers at attempt #5; lock auto-clears after 15 min; LOGIN_LOCKED audit event emitted; Redis namespace `auth:lockout:*` isolated from `auth:session:*` |
| D3.3 | Rate-limiting middleware: per-IP + per-account throttling on /auth/login (10/min/IP) and /auth/refresh (30/min/user) | 429 returned when limit exceeded; rate-limit headers included; integration test asserts limits |
| D3.4 | Security regression test suite: lockout enforcement, bcrypt cost=12 verification, JWT expiry honored, RS256 signature verification, refresh-token reuse rejection, no plaintext secrets in logs | All 6 security regressions pass in CI; fails the build on regression |

### Dependencies

- M2 — full API surface to test against

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Brute-force attacks on login | High | Med (RISK-002) | D3.2 lockout + D3.3 rate limiting; isolated Redis namespace prevents session-store partition from disabling defense |
| Security regression slipping past review | Low | Critical (RISK-005) | D3.4 regression suite runs in CI; fails build on cost-factor or algorithm drift |

---

## M4: Password Reset + Audit Compliance

### Objective

Deliver the self-service password-reset flow and harden audit logging to SOC2 compliance. Reset is bundled with audit compliance because both ship after core auth + tests, both depend on external infrastructure (SendGrid for reset, archiver for retention), and both have failure modes that are independent of the core auth loop.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D4.1 | POST /auth/reset-request: generate single-use reset token (1-hour TTL), dispatch via SendGrid; rate-limited per email AND per IP | Same 200 response regardless of email registration (no enumeration); reset email delivered within 60s (SC observed); audit `RESET_REQUESTED` emitted |
| D4.2 | POST /auth/reset-confirm: validate token, rehash password via PasswordHasher, invalidate ALL active sessions for user (FR-005) | Used tokens rejected on second use; expired tokens (>1hr) return clear error; all refresh-token families for user revoked; audit `RESET_COMPLETED` |
| D4.3 | Audit log query API + 12-month retention enforcement: GET /audit/events (admin only, paginated, filterable by user/event_type/date range); cron archiver moves events >12mo to cold storage | Admin can query Jordan-persona use case; retention policy validated; archiver runs nightly; SOC2 evidence export format documented |
| D4.4 | SendGrid integration with retry queue + dead-letter handling (RISK-007): 3-retry exponential backoff, DLQ alert on permanent failure | Transient SendGrid failures auto-retry; permanent failures alert auth-team within 5 min; queue depth metric exposed |

### Dependencies

- M2 — needs TokenManager for session invalidation, audit hooks from M1.D1.4
- M3 — integration test harness pattern reused for reset endpoints

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Compliance failure from incomplete audit logging | Med | High (RISK-006) | D4.3 retention enforcement + SOC2 evidence export; M1+M2 audit hooks already cover event capture |
| Email delivery failures blocking password reset | Low | Med (RISK-007) | D4.4 retry queue + DLQ; runbook fallback to support-channel reset |
| Reset token leakage via email forwarding | Low | High | Single-use enforcement (D4.2); 1-hour TTL; audit RESET_TOKEN_USED includes IP |

---

## M5: Frontend Integration + Performance Validation

### Objective

Assemble the user-facing layer against the stable, tested API and validate all performance NFRs before the rollout gate. The AuthProvider's token-storage decision (httpOnly cookies preferred over localStorage to mitigate RISK-001) is made now — *after* the backend refresh contract is concrete — not during a parallel build that risks premature commitment.

M5 runs in parallel with M4 because frontend components depend on M3's stable API contract but not on the reset endpoints (reset UI is a small addition to M5 if M4 lands first; otherwise it ships in M6 polish).

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D5.1 | React AuthProvider context: token storage in httpOnly cookies + CSRF token pairing; silent refresh scheduler; 401 retry interceptor | Tokens never accessible to JS (RISK-001 mitigation); silent refresh fires 60s before access-token expiry; 401 triggers refresh-then-retry once |
| D5.2 | LoginPage + RegisterPage with inline validation, generic error messaging (no enumeration), feature-flag-gated by `AUTH_NEW_LOGIN` | Form validation client-side before submit; success redirects to dashboard; failure shows generic error |
| D5.3 | ProfilePage: GET /auth/me display; inline edit for non-sensitive fields (displayName) | Page renders in < 1s; data matches registration; edits persist via API |
| D5.4 | Password-reset UI: request page + confirm page (only if M4 has shipped; otherwise deferred to M6 polish) | Reset request shows confirmation regardless of email registration; confirm page validates new password client-side before submit |
| D5.5 | Performance load test suite (k6): validate login p95 < 200ms (SC-002, NFR-001), refresh p95 < 100ms (SC-006), 500 concurrent users (NFR-002), hash time < 500ms (SC-007) | All four perf SCs green; report archived; baseline established for regression detection |

### Dependencies

- M3 — stable API contracts; integration test patterns
- M4 (optional) — reset UI deferred if M4 not yet shipped

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Token theft via XSS | Med | High (RISK-001) | D5.1 httpOnly cookies + CSRF token pairing eliminates JS-accessible tokens |
| Low registration adoption due to poor UX | Med | High (RISK-004) | D5.2 inline validation + minimal friction; success funnel measured against SC-001 (>60%) |
| Performance regression discovered post-GA | Low | High | D5.5 load tests run in CI before M6; baseline locked for regression detection |

---

## M6: Production Hardening + Phased Rollout

### Objective

Promote the authentication service to production via the PRD's three-phase rollout (internal alpha → beta 10% → GA 100%). This milestone is a *gate*, not a polish phase: no production traffic until feature flags, migration scripts, and key-rotation automation are in place. The quarterly key-rotation drill is exercised pre-GA so the operational muscle exists when needed under stress, not after an incident demands it.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D6.1 | Feature-flag infrastructure: `AUTH_NEW_LOGIN` gates new login surface; `AUTH_TOKEN_REFRESH` gates refresh-token flow; per-flag percentage-rollout control | Flags toggleable without deploy; per-flag rollout percentage configurable; flag state observable in monitoring |
| D6.2 | Data migration scripts: UserProfile migration with checksums, rollback procedures, dry-run mode against staging snapshot (RISK-003) | Migration is idempotent (re-run safe); checksum mismatch aborts and rolls back; runbook documents rollback steps |
| D6.3 | JWT key-rotation automation: quarterly RS256 keypair generation, grace-period overlap (old + new keys both valid for 30 days), `kid` header migration via JWKS | Key rotation completes with zero downtime in staging drill; old keys remain valid during grace period; metrics expose key-id usage distribution |
| D6.4 | Rollout runbook: Phase 1 (internal alpha, 1 week, all FRs pass + zero P0/P1) → Phase 2 (beta 10%, 2 weeks, p95 < 200ms + error rate < 0.1%) → Phase 3 (GA 100%, 1 week, 99.9% uptime over 7 days); rollback criteria + monitoring alerts | Runbook signed off by test-lead + eng-manager; rollback procedure tested in staging; on-call alerts wired to PagerDuty |

### Dependencies

- M4 — reset + audit compliance feature-complete
- M5 — frontend + perf validation feature-complete

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data loss during migration from legacy auth | Low | High (RISK-003) | D6.2 checksummed scripts + rollback; UserRepo soft-delete from M1; full backup before each phase |
| Implementation security flaws discovered post-GA | Low | Critical (RISK-005) | M1+M3 security regression suite + D6.4 phased rollout limits blast radius to 10% in Phase 2 |
| Compliance failure at SOC2 audit | Med | High (RISK-006) | M4 audit query API + retention enforcement; D6.4 monitoring dashboards include audit event volume |

---

## Risk Register

| ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |
|----|------|---------------------|-------------|--------|------------|-------|
| R-001 | Token theft via XSS allowing session hijacking | M2, M5 | Med | High | Refresh-token rotation + family reuse-detection (M2.D2.4); httpOnly cookies + CSRF pairing (M5.D5.1); 15-min access TTL | security |
| R-002 | Brute-force attacks on login endpoint | M3 | High | Med | Account lockout 5×/15min in isolated Redis namespace (M3.D3.2); rate-limiting middleware (M3.D3.3) | security |
| R-003 | Data loss during migration from legacy auth | M6 | Low | High | Checksummed migration scripts + rollback (M6.D6.2); UserRepo soft-delete (M1.D1.1); full backup pre-phase | devops |
| R-004 | Low registration adoption due to poor UX | M2, M5 | Med | High | Auto-login post-register (M2.D2.2); inline validation + minimal friction (M5.D5.2); funnel measured vs SC-001 | frontend |
| R-005 | Implementation security flaws | M1, M3, M6 | Low | Critical | Trust primitives isolated in M1; security regression suite in M3.D3.4; phased rollout limits blast radius (M6.D6.4) | security |
| R-006 | Compliance failure from incomplete audit logging | M1, M4 | Med | High | Audit as M1 dependency (D1.4); SOC2 query API + retention enforcement in M4.D4.3 | security |
| R-007 | Email delivery failures blocking password reset | M4 | Low | Med | SendGrid retry queue + DLQ alerting (M4.D4.4); runbook fallback to support-channel reset | backend |

## Decision Summary

| Decision | Chosen | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Primary Persona | architect | backend (confidence 0.294), security (0.216) | No persona exceeded the 0.3 confidence floor; multi-domain security-critical service → architect is the safe default. Backend + security selected as consulting personas. |
| Template | inline | No Tier 1/Tier 2 templates discovered (`tier1_templates_found: 0`); Tier 3 plugin marketplace not yet available | 4-tier discovery yielded zero candidates ≥ 0.6 compatibility; inline generation applied per `refs/templates.md` Tier 4. |
| Milestone Count | 6 | 5–7 range from MEDIUM complexity formula | `base(5) + floor(domain_count(4) / 2) = 5 + 2 = 7`, capped at 6 because validation interleave (1:2) is absorbed by M3 (dedicated TEST milestone) and M6 (gate) rather than separate V# milestones — yielding 6 work-shaped milestones with validation woven in. |
| Adversarial Mode | multi-roadmap | none (single-spec single-roadmap was the alternative if `--multi-roadmap` absent) | `--multi-roadmap --agents opus,sonnet` explicitly provided. |
| Adversarial Base Variant | opus:architect | sonnet:architect (highest convergence contribution: 0.78) | Opus's foundation-first framing organizes M1; Sonnet's pragmatic boundaries adopted for M2–M6 milestone shapes. See `adversarial/diff-analysis.md`. |
| TokenManager placement | M2 (with session lifecycle) | M1 (with trust foundation, per Opus); M3 (with auth endpoints) | Refresh contract architecturally inseparable from issuance; bundling with session lifecycle is the cleanest seam (Sonnet's argument). |
| Audit logging split | Schema + sink in M1; query API + retention in M4 | M1 only (Opus); M4 only (would create unlogged period) | Sonnet's split: never an unlogged period, but no delay for SOC2 tooling. |
| Frontend timing | M5 parallel to M4 (after M3) | M5 strictly after M3 (Opus); M5 parallel to M3 (would race contract) | M3 locks API contract; M5 builds against stable surface; parallelizing with M4 shortens delivery by ~1 milestone. |

## Success Criteria

| ID | Criterion | Validates Milestone(s) | Measurable |
|----|-----------|-----------------------|-----------|
| SC-001 | Registration conversion rate > 60% | M2, M5 | Yes — funnel analytics from RegisterPage to confirmed account |
| SC-002 | Login response time (p95) < 200ms | M2, M5 | Yes — APM on /auth/login; validated in M5.D5.5 load test |
| SC-003 | Average session duration > 30 min | M2 | Yes — TokenManager refresh event analytics |
| SC-004 | Failed login rate < 5% of attempts | M3 | Yes — audit_events query: LOGIN_FAILED / LOGIN_TOTAL |
| SC-005 | Password reset completion rate > 80% | M4 | Yes — funnel: RESET_REQUESTED → RESET_COMPLETED |
| SC-006 | Token refresh latency (p95) < 100ms | M2, M5 | Yes — APM on TokenManager.refresh; validated in M5.D5.5 |
| SC-007 | Password hash time < 500ms | M1, M5 | Yes — bcrypt benchmark at cost=12; validated in M5.D5.5 |
| SC-008 | > 1000 DAU within 30 days of GA | M6 | Yes — AuthToken issuance counts post-Phase 3 |
