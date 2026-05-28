# Roadmap: User Authentication System (Variant 2 — sonnet:security)

<!-- Variant produced by sonnet:security advocate. Approach: pragmatic phased delivery, fewer larger milestones, federated identity grouped with strong-auth, GDPR self-service treated as feature. -->

## Overview

This roadmap implements the user authentication system using a **pragmatic, phased delivery** approach. Each milestone is a shippable increment — the system is functional and secure after every milestone, just less complete than the next one. Security controls (encryption, audit, rate limiting, 2FA) are introduced inline with the features they protect rather than separated into a dedicated "defense" milestone. The result is fewer, larger milestones (5 work + 2 validation) at the low end of the MEDIUM-complexity range, with broader scope per milestone but stronger end-to-end coherence.

Key decisions:

- **M1 is a foundation milestone**, not a threat-model milestone — threat modeling is treated as an ongoing activity owned by the security persona, not a discrete milestone. Skipping the dedicated threat-model phase gets the team to working auth ~1 sprint sooner.
- **Federated identity (M3) pairs OAuth2 with 2FA** under the banner "strong authentication" — both serve the same goal (reduce reliance on passwords) and share UX patterns (challenge-response flows).
- **RBAC + Rate Limiting + Audit collapse into M4** because they're all "policy enforcement" concerns and benefit from being designed together (you want your audit log to record rate-limit decisions, etc.).
- **GDPR self-service is a first-class feature in M5**, not a compliance footnote — the data-export and account-deactivation flows are user-facing.

## Milestone Summary

| ID | Title | Type | Priority | Effort | Dependencies | Deliverables | Risk |
|----|-------|------|----------|--------|--------------|--------------|------|
| M1 | Foundation & Infrastructure | FEATURE | P0 | M | None | 5 | Medium |
| M2 | Core Authentication | SECURITY | P0 | L | M1 | 7 | High |
| V1 | Validation Gate — Core Auth | TEST | P1 | S | M2 | 3 | Low |
| M3 | Federated Identity & Strong Auth | SECURITY | P0 | M | M2, V1 | 5 | Medium |
| M4 | Authorization, Audit & Rate Limiting | SECURITY | P0 | L | M2, V1 | 6 | High |
| V2 | Validation Gate — Production Readiness | TEST | P1 | S | M3, M4 | 4 | Low |
| M5 | User & Admin Surface | FEATURE | P2 | M | M4 | 5 | Low |

## Dependency Graph

```
M1 → M2 → V1 → { M3, M4 } → V2 → M5
```

---

## M1: Foundation & Infrastructure

### Objective

Establish the running system: containerized services, database schema, secret management, and the bare API skeleton with health checks. No auth logic yet, but everything in place to support it.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D1.1 | Containerized infrastructure (DEP-001 to DEP-004) | docker-compose brings up Postgres 15+, Redis, app server with TLS |
| D1.2 | User + session schema (Postgres) | Migrations versioned; rollback-safe; field-level encryption columns defined for PII (NFR-006) |
| D1.3 | Secret management baseline | Env-injection; no secrets in repo; rotation procedure documented |
| D1.4 | API skeleton + health checks | /health endpoint; OpenAPI 3.0 spec stub; CI pipeline (lint + test + SAST) |
| D1.5 | Observability baseline | Structured logs + metrics; tracing for auth endpoints (supports NFR-005 99.9% uptime measurement) |

### Dependencies

- None (foundation milestone)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Infra setup delays downstream work | Medium | Medium | Use docker-compose; defer Kubernetes to post-launch |
| Schema-rewrite needed after M2 reveals model gap | Medium | Medium | Keep M1 schema minimal; rely on migrations in M2 |

---

## M2: Core Authentication

### Objective

Ship a working email/password login system end-to-end: registration with verification, login with JWT issuance, refresh-token sessions, and password reset. After M2, the product is shippable to early users; everything else is hardening, federation, or admin.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D2.1 | Registration with email verification (FR-001) | bcrypt cost ≥ 12; 24h verification token TTL; SendGrid integration |
| D2.2 | Login + JWT issuance (FR-002) | RS256 access (15 min) + refresh (7 day); standard claims (iss, aud, exp) |
| D2.3 | Refresh-token rotation (FR-006) | Rotate-on-use; Redis-backed session store; logout invalidates server-side |
| D2.4 | Password reset (FR-005) | One-time link; 15-min TTL; invalidate-on-use |
| D2.5 | HTTP-only, Secure cookies + CSP headers (RISK-001) | Mitigates token theft via XSS in same milestone the tokens are issued |
| D2.6 | PII encryption-at-rest (NFR-006) | Field-level encryption for email/name; PII-aware logging |
| D2.7 | NFR-001 latency budget | P95 < 200ms on auth endpoints in CI load tests |

### Dependencies

- M1

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-001: token theft via XSS | Medium | High | HTTP-only + Secure + SameSite cookies; CSP headers (in same milestone) |
| RISK-004: PII data breach | Low | Critical | Field-level encryption + restricted DB access; audit log added in M4 |

---

## V1: Validation Gate — Core Auth

### Objective

Confirm M2 is shippable: OWASP scan clean, load test passes, security review by independent advocate.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| DV1.1 | OWASP ZAP scan against NFR-003 | Zero Critical, ≤1 Medium |
| DV1.2 | Load test: 10K concurrent sessions (NFR-002) | Sustained 30 min; P95 < 200ms (SC-003) |
| DV1.3 | Code review: JWT issuance + cookie handling | No findings, or all findings resolved before V1 close |

### Dependencies

- M2

### Stop Criteria

- ANY Critical CVE
- Load test failure to hold 10K sessions
- JWT signing key handling deemed unsafe

---

## M3: Federated Identity & Strong Authentication

### Objective

Reduce reliance on passwords by adding OAuth2 (Google, GitHub) and TOTP-based 2FA. These are grouped together as **strong authentication** — both add stronger or alternative identity proofs and share challenge-response UX patterns.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D3.1 | Google OAuth2 (FR-003) | PKCE-enforced; state param signed; identity linking by email |
| D3.2 | GitHub OAuth2 (FR-003) | Same JWT shape as M2 local login (no parallel session model) |
| D3.3 | TOTP-based 2FA (FR-007) | RFC 6238; QR enrollment; backup codes; per-tenant opt-in |
| D3.4 | OAuth provider downtime fallback (RISK-003) | Graceful local-auth fallback with UI banner |
| D3.5 | Strong-auth enforcement policy | 2FA optional → required for admins (role-aware) |

### Dependencies

- M2 (JWT shape established)
- V1 (core auth validated)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-003: OAuth provider downtime | Low | Medium | Local-auth fallback; degraded-mode UI |
| 2FA enrollment friction | Medium | Low | Backup codes + admin reset; gradual rollout policy |

---

## M4: Authorization, Audit & Rate Limiting

### Objective

Policy-enforcement milestone: who can do what (RBAC), what was done (audit), and how often it can be done (rate limit). Grouped because they share the same conceptual hook — "request enters, policy decides, decision is recorded."

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D4.1 | RBAC schema + middleware (FR-004) | Roles + permissions; deny-by-default; integration tests assert deny |
| D4.2 | Append-only audit log (FR-009) | Tamper-evident (hash chain); SC-005 covered |
| D4.3 | Audit query API | Filters: actor, time, event type; admin-only |
| D4.4 | Per-user + per-IP rate limiting (FR-008) | Sliding-window; Redis-backed; configurable thresholds |
| D4.5 | Account lockout after N failures (RISK-002) | 5 failures → 15 min lock; lockout events logged via audit |
| D4.6 | GDPR-aware audit retention (NFR-004) | Retention policy + redaction for deleted users |

### Dependencies

- M2 (sessions to attach policy to)
- V1

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-002: brute force | High | High | Rate limit + lockout (in this milestone) + 2FA (M3) |
| RBAC bypass via missing check | Medium | High | Deny-by-default middleware; tests assert deny on every endpoint |

---

## V2: Validation Gate — Production Readiness

### Objective

Validate M3 + M4 layered on top of M2 still works end-to-end and meets all success criteria.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| DV2.1 | Full OWASP Top 10 re-scan | Zero High/Critical (SC-002) |
| DV2.2 | Brute-force simulation | Lockout + rate-limit thresholds hold; OAuth path not bypassable |
| DV2.3 | RBAC penetration test | Privilege escalation blocked + audited |
| DV2.4 | Audit-log integrity verification | Hash chain intact under tamper attempt; SC-005 |

### Dependencies

- M3, M4

### Stop Criteria

- Any High/Critical CVE
- Privilege escalation possible
- Audit log can be tampered without detection

---

## M5: User & Admin Surface

### Objective

Ship the user-facing and admin surfaces that depend on all prior security primitives.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D5.1 | User profile management (FR-010) | Self-service edit; PII-aware |
| D5.2 | Admin dashboard (FR-011) | Search, view, suspend; all actions audited |
| D5.3 | Account deactivation (FR-012) | Soft-delete + 30-day grace |
| D5.4 | GDPR data export (NFR-004) | User-initiated; JSON download; logged in audit |
| D5.5 | GDPR right-to-erasure (NFR-004) | Hard-delete on request; cascades + redacts audit log per retention policy |

### Dependencies

- M4 (admin needs RBAC; deactivation logs to audit)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Admin dashboard XSS | Low | Medium | CSP headers (inherited from M2) + output encoding |

---

## Risk Register

| ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |
|----|------|---------------------|-------------|--------|------------|-------|
| RISK-001 | Token theft via XSS | M2 | Medium | High | HTTP-only + Secure cookies + CSP (all in M2) | security |
| RISK-002 | Brute force | M4 | High | High | Rate limit + lockout + 2FA (M3) | security |
| RISK-003 | OAuth provider downtime | M3 | Low | Medium | Local-auth fallback | backend |
| RISK-004 | Data breach of PII | M2, M5 | Low | Critical | Field encryption + audit log (M4) + GDPR controls (M5) | security |

## Decision Summary

| Decision | Chosen | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Primary Persona | security | backend (0.193) | Security at 55% dominant domain |
| Template | inline | none discovered | No Tier 1/Tier 2 templates |
| Milestone Count | 5 work + 2 validation | 5–7 (MEDIUM range) | Low end of range; pragmatic shippable increments preferred over fine-grained decomposition |
| Threat Model | Ongoing activity | Dedicated M1 milestone | Threat-model-as-document quickly drifts; treated as continuous security-persona responsibility |
| OAuth & 2FA Grouping | Combined in M3 (strong-auth) | Separate milestones | Both reduce password reliance; share UX patterns |
| RBAC + Audit + Rate-Limit Grouping | Combined in M4 (policy) | Three separate milestones | All policy-enforcement concerns; benefit from shared design |

## Success Criteria

| ID | Criterion | Validates Milestone(s) | Measurable |
|----|-----------|----------------------|------------|
| SC-001 | All FR requirements implemented and tested | M2–M5 | Yes |
| SC-002 | OWASP compliance verified via security scan | V1, V2 | Yes |
| SC-003 | Load testing confirms 10K concurrent sessions | V1 | Yes |
| SC-004 | OAuth2 flow works for Google and GitHub | M3 | Yes |
| SC-005 | Audit logs capture all auth events | M4, V2 | Yes |
