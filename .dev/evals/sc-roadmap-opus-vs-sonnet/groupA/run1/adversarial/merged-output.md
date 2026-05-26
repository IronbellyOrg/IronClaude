<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (sonnet:security) -->
<!-- Merged with strengths from Variant A (opus:security) and Round 2.5 invariant probe -->
<!-- Merge date: 2026-05-22T16:27:38+00:00 -->

# Roadmap: User Authentication System

## Overview

<!-- Source: Base (original, modified) — merged threat-model emphasis from Variant A -->

This roadmap implements the user authentication system using a **pragmatic, phased delivery** approach grounded in an explicit STRIDE threat model. Each milestone is a shippable increment — the system is functional and secure after every milestone, just less complete than the next one. Security controls are introduced inline with the features they protect (CSP lands with cookies in M2, not later), while defense-in-depth controls (rate limiting, lockout, 2FA) are grouped together to mitigate brute-force attacks (RISK-002) coherently.

Key decisions:

- **M1 is a foundation milestone** that includes infrastructure, observability, an explicit STRIDE threat model deliverable, and a 90-day key/secret rotation policy. The threat model is a referenceable artifact that each subsequent milestone updates, not a separate milestone (resolves debate point X-002 as hybrid).
- **M2 ships a working email/password auth surface** with CSP + HTTP-only cookies bundled in the same milestone as the JWT-issuing endpoints (resolves X-001 in favor of co-locating cookie + header protections).
- **V1 explicitly locks the JWT shape** before federated identity is layered on (resolves U-002 in favor of preserving Variant A's sequencing rationale, preventing token-shape drift between local and federated paths).
- **M4a (Authorization & Audit)** and **M4b (Defense — Rate Limiting, Lockout, 2FA)** are separated to keep the wide-blast-radius defense milestone smaller and easier to roll back (resolves S-004 as hybrid; concession from Variant B in Round 2).
- **2FA is grouped with rate limiting in M4b** under the defense framing — both mitigate RISK-002 (brute force), not federation (resolves S-003 / X-003 in favor of Variant A's framing).
- **GDPR self-service (data export + right-to-erasure) is a first-class user-facing surface in M5** (preserves Variant B's U-005).

Complexity classification: MEDIUM (score 0.445). Interleave ratio 1:2 (validation milestone per two work milestones).

## Milestone Summary

| ID | Title | Type | Priority | Effort | Dependencies | Deliverables | Risk |
|----|-------|------|----------|--------|--------------|--------------|------|
| M1 | Foundation, Threat Model & Infrastructure | FEATURE | P0 | M | None | 7 | Medium |
| M2 | Core Authentication (Email + Password) | SECURITY | P0 | L | M1 | 7 | High |
| V1 | Validation Gate — Core Auth (JWT Shape Lock) | TEST | P1 | S | M2 | 4 | Low |
| M3 | OAuth2 Federated Identity | SECURITY | P0 | M | M2, V1 | 4 | Medium |
| M4a | Authorization (RBAC) & Audit Logging | SECURITY | P0 | M | M2, V1 | 4 | Medium |
| M4b | Defense — Rate Limiting, Lockout, 2FA | SECURITY | P0 | M | M2, V1 | 4 | High |
| V2 | Validation Gate — Production Readiness | TEST | P1 | S | M3, M4a, M4b | 5 | Low |
| M5 | User & Admin Surface + GDPR Self-Service | FEATURE | P2 | M | M4a | 5 | Low |

**Total**: 6 work + 2 validation = 8 milestones.

## Dependency Graph

```
M1 → M2 → V1 → { M3, M4a, M4b } → V2 → M5
                                  ↘ M4a → M5 (admin requires RBAC + audit)
```

---

## M1: Foundation, Threat Model & Infrastructure

<!-- Source: Variant B M1 (base), extended with Variant A D1.1 (STRIDE) and D1.3 (key rotation) -->

### Objective

Establish the running system AND the security baseline: containerized services, database schema, secret management, observability, an explicit STRIDE threat model, and a 90-day key/secret rotation policy. No auth logic yet, but everything in place to support it safely.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D1.1 | Containerized infrastructure (DEP-001 to DEP-004) | docker-compose brings up Postgres 15+, Redis, app server with TLS |
| D1.2 | User + session schema (Postgres) | Migrations versioned; rollback-safe; field-level encryption columns defined for PII (NFR-006) |
| D1.3 | Secret management baseline | Env-injection; no secrets in repo; cloud-KMS abstraction documented |
| D1.4 | API skeleton + health checks | /health endpoint; OpenAPI 3.0 spec stub; CI pipeline (lint + test + SAST + dependency scan + secret scan) |
| D1.5 | Observability baseline | Structured logs + metrics + tracing for auth endpoints (supports NFR-005 99.9% uptime measurement) |
| D1.6 | STRIDE threat model (incorporated from Variant A D1.1) | Living document covering all OWASP Top 10 categories (NFR-003), mapped to FRs and Risk Register entries; updated by each downstream milestone |
| D1.7 | Secret & JWT key rotation policy (incorporated from Variant A D1.3) | 90-day automated rotation cycle for JWT signing keys; runbook + monitoring + alerting on stale keys |

### Dependencies

- None (foundation milestone)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Infra setup delays downstream work | Medium | Medium | Use docker-compose; defer Kubernetes to post-launch |
| Threat model drifts from implementation | Medium | Medium | Living document; each subsequent milestone updates the relevant STRIDE category |
| Schema-rewrite needed after M2 reveals model gap | Medium | Medium | Keep M1 schema minimal; rely on migrations in M2 |

---

## M2: Core Authentication (Email + Password)

<!-- Source: Base (original) — preserved Variant B M2 in full -->

### Objective

Ship a working email/password login system end-to-end: registration with verification, login with JWT issuance, refresh-token sessions, password reset, and full XSS/CSRF cookie + header protections. After M2 + V1, the product is shippable to early users; everything else is hardening, federation, or admin.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D2.1 | Registration with email verification (FR-001) | bcrypt cost ≥ 12; 24h verification token TTL; SendGrid integration with bounce handling |
| D2.2 | Login + JWT issuance (FR-002) | RS256 access (15 min) + refresh (7 day); standard claims (iss, aud, exp, sub) |
| D2.3 | Refresh-token rotation (FR-006) | Rotate-on-use; Redis-backed session store; logout invalidates server-side |
| D2.4 | Password reset (FR-005) | One-time link; 15-min TTL; invalidate-on-use |
| D2.5 | HTTP-only + Secure + SameSite=Strict cookies + CSP headers (RISK-001) | All four protections ship together; CSP script-src restricts inline scripts |
| D2.6 | PII encryption-at-rest (NFR-006) | Field-level encryption for email/name; PII-aware logging |
| D2.7 | NFR-001 latency budget | P95 < 200ms on auth endpoints in CI load tests |

### Dependencies

- M1 (infrastructure, schema, threat model, key rotation policy in place)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-001: token theft via XSS | Medium | High | HTTP-only + Secure + SameSite + CSP (all in M2) |
| RISK-004: PII data breach | Low | Critical | Field-level encryption + restricted DB access; audit log added in M4a |

---

## V1: Validation Gate — Core Auth (JWT Shape Lock)

<!-- Source: Variant B V1 (base), extended with Variant A's JWT-shape-lock rationale -->

### Objective

Confirm M2 is shippable AND the JWT shape is locked before federated identity is layered on. Acts as the gate that prevents token-shape drift between local and federated paths (incorporated rationale from Variant A).

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| DV1.1 | OWASP ZAP scan against NFR-003 | Zero Critical, ≤1 Medium |
| DV1.2 | Load test: 10K concurrent sessions (NFR-002) | Sustained 30 min; P95 < 200ms (SC-003) |
| DV1.3 | Code review: JWT issuance + cookie handling | No outstanding findings before V1 closes |
| DV1.4 | **JWT shape lock-in** | JWT schema (claims, signing alg, TTL pattern) documented and frozen; any change post-V1 requires explicit ADR — prevents drift between M2 local auth and M3 federated auth |

### Dependencies

- M2

### Stop Criteria

- ANY Critical CVE
- Load test failure to hold 10K sessions
- JWT signing key handling deemed unsafe
- JWT schema not documented/frozen (DV1.4 must pass before M3 begins)

---

## M3: OAuth2 Federated Identity

<!-- Source: Variant B M3, modified — 2FA removed and moved to M4b per S-003/X-003 resolution -->

### Objective

Layer Google + GitHub OAuth2 on top of the locked JWT shape from V1. Federated identities map onto the same user record via the same JWT schema — no parallel session model.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D3.1 | Google OAuth2 (FR-003) | PKCE-enforced; state param signed; identity linking by email; emits JWT conforming to V1-locked schema |
| D3.2 | GitHub OAuth2 (FR-003) | PKCE-enforced; same JWT shape as M2 local login; SC-004 met |
| D3.3 | Federated → local identity linking | Email-based merge with explicit user confirmation |
| D3.4 | OAuth provider downtime fallback (RISK-003) | Graceful local-auth fallback with degraded-mode UI banner |

### Dependencies

- M2 (local auth + JWT)
- V1 (JWT shape locked at DV1.4)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-003: OAuth provider downtime | Low | Medium | Local-auth fallback; degraded-mode UI |
| Federated/local JWT drift | Low (was Medium) | High | V1's DV1.4 JWT-shape-lock prevents drift structurally |

---

## M4a: Authorization (RBAC) & Audit Logging

<!-- Source: Variant B M4 (split half), with INV-009 GDPR-aware retention preserved -->

### Objective

Implement role-based access control (FR-004) and append-only audit log (FR-009). Paired because audit logging is the verification mechanism for RBAC enforcement, and audit retention must coordinate with GDPR right-to-erasure (resolves INV-009).

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D4a.1 | RBAC schema + middleware (FR-004) | Roles + permissions; deny-by-default; integration tests assert deny on every endpoint |
| D4a.2 | Append-only audit log (FR-009) | Tamper-evident (hash chain); SC-005 covered |
| D4a.3 | Audit query API | Filters: actor, time, event type; admin-only |
| D4a.4 | GDPR-aware audit retention (NFR-004) | Retention policy + redaction for deleted users; resolves INV-009 audit-log-vs-erasure interaction |

### Dependencies

- M2 (sessions to attach policy to)
- V1

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RBAC bypass via missing check | Medium | High | Deny-by-default middleware; integration tests assert deny on every endpoint |

---

## M4b: Defense — Rate Limiting, Lockout, 2FA

<!-- Source: Variant B M4 (split half), extended with 2FA from M3 and OAuth-callback rate-limit from INV-008 -->

### Objective

Attack-surface reduction milestone. Rate limiting (FR-008), account lockout, and 2FA (FR-007) are all defenses against RISK-002 (brute force). They share the same conceptual hook ("request enters, defense decides, request proceeds or is rejected") and benefit from being designed together.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D4b.1 | Per-user + per-IP rate limiting (FR-008) | Sliding-window; Redis-backed; configurable thresholds |
| D4b.2 | Account lockout after N failures (RISK-002) | 5 failures → 15 min lock; lockout events logged via audit (M4a) |
| D4b.3 | TOTP-based 2FA (FR-007) | RFC 6238; QR enrollment; backup codes; per-tenant opt-in; required for admin role |
| D4b.4 | OAuth-callback rate limit (incorporated from INV-008) | Rate limit applies to OAuth callback paths — attacker without an account cannot spam FR-003 endpoints |

### Dependencies

- M2 (sessions and login endpoints exist)
- V1

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-002: brute force | High | High | Rate limit + lockout + 2FA stacked defense |
| 2FA enrollment friction | Medium | Low | Backup codes + admin reset; gradual rollout |
| 2FA lockout for legitimate users | Medium | Medium | Backup codes + admin reset workflow |

---

## V2: Validation Gate — Production Readiness

<!-- Source: Variant B V2, extended with INV-002 and INV-006 stop criteria -->

### Objective

Validate M3 + M4a + M4b layered on top of M2 still works end-to-end and meets all success criteria. Include resilience checks for previously-implicit assumptions (Redis outage, empty-role users).

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| DV2.1 | Full OWASP Top 10 re-scan | Zero High/Critical (SC-002) |
| DV2.2 | Brute-force simulation | Lockout + rate-limit thresholds hold; OAuth callback path also rate-limited (INV-008 verification) |
| DV2.3 | RBAC penetration test | Privilege escalation blocked + audited; test covers empty-role users (INV-006 verification) |
| DV2.4 | Audit-log integrity verification | Hash chain intact under tamper attempt; SC-005 |
| DV2.5 | Session-store outage drill (incorporated from INV-002) | Redis outage degrades gracefully (read-only mode or DB-backed fallback) — NFR-005 risk surface |

### Dependencies

- M3, M4a, M4b

### Stop Criteria

- Any High/Critical CVE
- Privilege escalation possible
- Audit log can be tampered without detection
- Session-store outage causes total auth outage (must degrade)
- OAuth callback bypass of rate limiting

---

## M5: User & Admin Surface + GDPR Self-Service

<!-- Source: Variant B M5 (base) — preserves U-005 GDPR self-service strength -->

### Objective

Ship the user-facing and admin surfaces that depend on all prior security primitives. GDPR self-service (data export + right-to-erasure) is first-class, not a compliance footnote.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D5.1 | User profile management (FR-010) | Self-service edit; PII-aware |
| D5.2 | Admin dashboard (FR-011) | Search, view, suspend; all actions audited via M4a |
| D5.3 | Account deactivation (FR-012) | Soft-delete + 30-day grace |
| D5.4 | GDPR data export (NFR-004) | User-initiated; JSON download; logged in audit |
| D5.5 | GDPR right-to-erasure (NFR-004) | Hard-delete on request; cascades + redacts audit log per M4a D4a.4 retention policy |

### Dependencies

- M4a (admin needs RBAC; deactivation logs to audit; GDPR erasure coordinates with audit retention)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Admin dashboard XSS | Low | Medium | CSP headers (inherited from M2 D2.5) + output encoding |

---

## Risk Register

| ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |
|----|------|---------------------|-------------|--------|------------|-------|
| RISK-001 | Token theft via XSS | M2 | Medium | High | HTTP-only + Secure + SameSite + CSP (all in M2 D2.5) | security |
| RISK-002 | Brute force | M4b | High | High | Rate limit + lockout + 2FA stacked (M4b); 2FA required for admins | security |
| RISK-003 | OAuth provider downtime | M3 | Low | Medium | Local-auth fallback (M3 D3.4) | backend |
| RISK-004 | Data breach of PII | M2, M4a, M5 | Low | Critical | Field encryption (M2) + audit log (M4a) + GDPR controls (M5) | security |

## Decision Summary

| Decision | Chosen | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Primary Persona | security | backend (0.193) | Security at 55% dominant domain |
| Template | inline | none discovered | No Tier 1/Tier 2 templates |
| Milestone Count | 6 work + 2 validation (8 total) | Variant A: 7+2; Variant B: 5+2 | Split of original M4 into M4a/M4b per Round 2 hybrid resolution of S-004; keeps shippable-M2 property while reducing defense-milestone blast radius |
| Threat Model | Deliverable in M1 (D1.6), not separate milestone | A: dedicated M1 milestone; B: ongoing activity | Hybrid resolution of X-002: artifact required (per A) but housed in foundation milestone (per B) |
| OAuth & 2FA Placement | OAuth in M3, 2FA in M4b (defense) | B-original: grouped in M3 (strong-auth); A: 2FA in M6 with rate-limit | A's defense framing wins (S-003/X-003 at 72%/70%); B conceded in Round 2 |
| CSP Headers Timing | M2 (D2.5, bundled with cookies) | A: M6 defense layer | B wins X-001/C-002 at 88-90% confidence; A conceded |
| RBAC + Audit + Rate-Limit Decomposition | M4a (RBAC+audit) + M4b (defense) | B-original: combined M4; A: 3 separate milestones | S-004 hybrid: split into 2, not 1 or 3 |
| Adversarial Base Variant | Variant B (sonnet:security) | Variant A (combined 0.937 vs B 0.922; margin 1.5%) | Tiebreaker Level 1 (debate performance): B won 6 clear points, A won 4 |
| 2FA for OAuth-only users | Out of scope (future product decision) | Mandate enrollment | INV-010 LOW UNADDRESSED — edge case, not release blocker |

## Success Criteria

| ID | Criterion | Validates Milestone(s) | Measurable |
|----|-----------|----------------------|------------|
| SC-001 | All FR requirements implemented and tested | M2, M3, M4a, M4b, M5 | Yes |
| SC-002 | OWASP compliance verified via security scan | V1 (DV1.1), V2 (DV2.1) | Yes |
| SC-003 | Load testing confirms 10K concurrent sessions | V1 (DV1.2) | Yes |
| SC-004 | OAuth2 flow works for Google and GitHub | M3 (D3.1, D3.2) | Yes |
| SC-005 | Audit logs capture all auth events | M4a (D4a.2), V2 (DV2.4) | Yes |
