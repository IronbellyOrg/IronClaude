# Roadmap: User Authentication System (Variant 1 — opus:security)

<!-- Variant produced by opus:security advocate. Approach: threat-modeling-first, defense-in-depth, fine-grained milestone decomposition. -->

## Overview

This roadmap implements a comprehensive user authentication system using a **threat-modeling-first, defense-in-depth** approach. Security boundaries are established before any user-facing feature is coded: STRIDE threat enumeration drives the architecture, and every milestone has an explicit threat-mitigation deliverable. The plan favors fine-grained milestones to enable continuous security review and to keep each release blast-radius small. Two validation gates interleave the work milestones at a 1:2 ratio (MEDIUM complexity, 0.445).

Key decisions:

- **M1 is a security-foundation milestone**, not a feature milestone — threat model, infra hardening, secret/key management, and CI security gates land before any auth code.
- **OAuth2 (M4) is sequenced after core auth (M3)**, not in parallel, so the JWT/session model is locked-in before federated identity is layered on. This eliminates one of the highest-frequency real-world bugs (token-shape drift between local and federated paths).
- **2FA pairs with rate limiting in a single "defense layer" milestone (M6)**, treating both as attack-surface reduction rather than features.

## Milestone Summary

| ID | Title | Type | Priority | Effort | Dependencies | Deliverables | Risk |
|----|-------|------|----------|--------|--------------|--------------|------|
| M1 | Threat Model & Security Foundation | FEATURE | P0 | M | None | 5 | Medium |
| M2 | Identity Core (Registration + Password Reset) | SECURITY | P0 | M | M1 | 5 | Medium |
| M3 | Authentication & Session Management | SECURITY | P0 | M | M2 | 6 | High |
| V1 | Validation Gate — Core Auth | TEST | P1 | S | M3 | 3 | Low |
| M4 | OAuth2 Federated Identity | SECURITY | P1 | M | M3, V1 | 4 | Medium |
| M5 | Authorization (RBAC) & Audit Logging | SECURITY | P0 | M | M3, V1 | 5 | Medium |
| M6 | Defense Layer (Rate Limiting + 2FA) | SECURITY | P1 | M | M3, V1 | 5 | High |
| V2 | Validation Gate — Defense-in-Depth | TEST | P1 | S | M4, M5, M6 | 4 | Low |
| M7 | Admin & Lifecycle Management | FEATURE | P2 | S | M5 | 4 | Low |

## Dependency Graph

```
M1 → M2 → M3 → V1 → { M4, M5, M6 } → V2 → M7
                                       ↘ M5 → M7 (explicit RBAC dep)
```

---

## M1: Threat Model & Security Foundation

### Objective

Establish the security baseline (threat model, infrastructure, secret management, CI gates) before any auth code is written. Eliminates the most common class of late-stage rework: "we need to add X security control everywhere."

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D1.1 | STRIDE threat model for the auth surface | Document covering all OWASP Top 10 categories with specific mitigations mapped to NFR-003 |
| D1.2 | Infrastructure baseline (PostgreSQL 15+, Redis, Docker) | Containerized, TLS-everywhere, secrets via env injection (no plaintext) |
| D1.3 | Secret & key rotation policy | JWT signing key rotation runbook + automated 90-day cycle |
| D1.4 | CI security gates | SAST + dependency scan + secret scan blocking on every PR |
| D1.5 | Encryption-at-rest baseline | Postgres TDE configured; Redis AUTH + TLS; key custody documented (NFR-006) |

### Dependencies

- None (foundation milestone)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Threat model drifts from implementation | Medium | High | Living document; each subsequent milestone updates the threat model |
| Secret management complexity slows delivery | Medium | Medium | Use cloud KMS abstraction; no hand-rolled crypto |

---

## M2: Identity Core (Registration + Password Reset)

### Objective

Implement the user-identity primitives — registration, email verification, password reset — with SendGrid integration. This is a deliberately narrow milestone: no login yet, no sessions yet, just "create and verify an identity."

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D2.1 | Registration endpoint with email verification (FR-001) | Verification token TTL 24h; replay-protected; bcrypt cost ≥ 12 |
| D2.2 | Password reset flow via email (FR-005) | One-time tokens, 15-min TTL, invalidate-on-use |
| D2.3 | PII encryption-at-rest for user records (NFR-006) | Field-level encryption for email + name; PostgreSQL pgcrypto |
| D2.4 | GDPR data-handling primitives (NFR-004) | Delete-cascade for user records; data-export endpoint stub |
| D2.5 | SendGrid integration with deliverability fallback | Configurable retry; DSN bounce handling |

### Dependencies

- M1: requires threat model + infra + secret management

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-001 partial: token theft via email-link XSS | Medium | High | Tokens are opaque random IDs (not JWTs); links use one-time hash |
| SendGrid downtime | Low | Medium | Retry queue with exponential backoff; mark accounts as pending |

---

## M3: Authentication & Session Management

### Objective

Implement login (FR-002), JWT issuance, and refresh-token session management (FR-006). This is the security-critical milestone — JWT shape is locked here and all downstream auth paths must conform.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D3.1 | Login endpoint with JWT issuance (FR-002) | RS256 signed; 15-min access, 7-day refresh; iss/aud/sub claims required |
| D3.2 | Refresh-token rotation (FR-006) | Rotate-on-use; old token revoked; Redis session store |
| D3.3 | HTTP-only, Secure, SameSite=Strict cookies | Mitigates RISK-001 (token theft via XSS) |
| D3.4 | Logout & session invalidation | Server-side revocation list; Redis TTL aligned with refresh expiry |
| D3.5 | Latency budget enforcement (NFR-001) | P95 < 200ms via load tests in CI |
| D3.6 | Concurrent-session capacity test (NFR-002) | 10K concurrent sessions sustained for 30 min |

### Dependencies

- M2: requires user identity exists before login can succeed

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-001: token theft via XSS | Medium | High | HTTP-only cookies + CSP headers (deferred to M6 hardening); no token in localStorage |
| JWT shape drift between local + federated paths | Medium | High | Lock JWT schema in M3 before OAuth in M4 |

---

## V1: Validation Gate — Core Auth

### Objective

Independent validation that M1–M3 work end-to-end before federated identity is layered on. Stop-and-fix gate.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| DV1.1 | Penetration test on auth endpoints | Zero Critical, ≤1 Medium |
| DV1.2 | OWASP ZAP automated scan against NFR-003 | All Top 10 categories covered |
| DV1.3 | Load test: 10K concurrent sessions (NFR-002) | Sustained for 30 min; P95 < 200ms |

### Dependencies

- M3

### Stop Criteria

- ANY Critical CVE
- P95 > 250ms under target load
- Token-reuse possible (refresh rotation broken)

---

## M4: OAuth2 Federated Identity

### Objective

Layer Google + GitHub OAuth2 on top of the locked JWT/session model. Federated identities map onto the same user record, no parallel user table.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D4.1 | Google OAuth2 flow (FR-003) | PKCE-enforced; state param signed; SC-004 met |
| D4.2 | GitHub OAuth2 flow (FR-003) | PKCE-enforced; same JWT shape as local login |
| D4.3 | Federated → local identity linking | Email-based merge with explicit confirmation |
| D4.4 | OAuth provider downtime fallback (RISK-003) | Surface "use email/password" UI when provider returns 5xx |

### Dependencies

- M3 (JWT shape locked)
- V1 (core auth validated)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-003: OAuth provider downtime | Low | Medium | Fallback to local auth; degraded mode banner |

---

## M5: Authorization (RBAC) & Audit Logging

### Objective

Implement role-based access control (FR-004) and append-only audit log (FR-009). These are paired because audit logging is the verification mechanism for RBAC enforcement.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D5.1 | RBAC schema + middleware (FR-004) | Roles + permissions; deny-by-default; explicit grant model |
| D5.2 | Append-only audit log (FR-009) | Every auth event logged; tamper-evident (hash chain); SC-005 met |
| D5.3 | Audit log query API | Time-range + actor + event-type filters |
| D5.4 | Role assignment workflow | Admin-only; logged in audit trail |
| D5.5 | GDPR audit-trail compliance (NFR-004) | Audit log retention policy + redaction for deleted users |

### Dependencies

- M3, V1

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RBAC bypass via missing middleware | Medium | High | Deny-by-default; integration tests assert deny on every endpoint |

---

## M6: Defense Layer (Rate Limiting + 2FA)

### Objective

Attack-surface reduction milestone. Rate limiting (FR-008) and 2FA (FR-007) are both treated as defenses, not features — they exist to mitigate RISK-002 (brute force).

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D6.1 | Per-user + per-IP rate limiting (FR-008) | Sliding-window; Redis-backed; configurable thresholds |
| D6.2 | Account lockout after N failures | 5 failures → 15 min lock; mitigates RISK-002 |
| D6.3 | TOTP-based 2FA (FR-007) | RFC 6238 compliant; QR enrollment; backup codes |
| D6.4 | 2FA enforcement policy | Optional → required for admins; per-tenant policy |
| D6.5 | CSP headers + browser-side hardening | Completes RISK-001 mitigation started in M3 |

### Dependencies

- M3, V1

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| RISK-002: brute force | High | High | Rate limit + lockout + 2FA stacked defense |
| 2FA lockout for legitimate users | Medium | Medium | Backup codes + admin reset workflow |

---

## V2: Validation Gate — Defense-in-Depth

### Objective

Validate that M4 + M5 + M6 compose correctly without weakening core auth from M3.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| DV2.1 | OWASP Top 10 re-scan (full surface) | Zero High/Critical (SC-002) |
| DV2.2 | Brute-force simulation | Account locks at expected threshold; no bypass via OAuth |
| DV2.3 | RBAC penetration test | Privilege-escalation attempts all blocked + logged |
| DV2.4 | Audit-log integrity test | Tamper-detection works; SC-005 met |

### Dependencies

- M4, M5, M6

### Stop Criteria

- Any privilege-escalation vector
- Any unaudited auth event
- Any rate-limit bypass

---

## M7: Admin & Lifecycle Management

### Objective

Surface user-facing features that depend on prior security primitives. Profile management, admin dashboard, account deactivation.

### Deliverables

| ID | Description | Acceptance Criteria |
|----|-------------|---------------------|
| D7.1 | User profile management (FR-010) | View/edit own profile; PII-aware |
| D7.2 | Admin dashboard (FR-011) | Search, view, suspend; all actions audited |
| D7.3 | Account deactivation workflow (FR-012) | Soft-delete + 30-day grace; GDPR hard-delete option |
| D7.4 | Self-service GDPR data export | NFR-004 compliance |

### Dependencies

- M5 (admin features require RBAC)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Admin dashboard XSS | Low | Medium | CSP + output encoding inherited from M6 |

---

## Risk Register

| ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |
|----|------|---------------------|-------------|--------|------------|-------|
| RISK-001 | Token theft via XSS | M3, M6 | Medium | High | HTTP-only cookies (M3) + CSP (M6) | security |
| RISK-002 | Brute force | M6 | High | High | Rate limit + lockout + 2FA | security |
| RISK-003 | OAuth provider downtime | M4 | Low | Medium | Local-auth fallback | backend |
| RISK-004 | Data breach of PII | M2, M5 | Low | Critical | Field-level encryption + audit + access controls | security |

## Decision Summary

| Decision | Chosen | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Primary Persona | security | backend (0.193) | Security domain at 55% — clear primary |
| Template | inline | none discovered | No Tier 1/Tier 2 templates present |
| Milestone Count | 7 work + 2 validation | 5–7 (MEDIUM complexity range) | High-end of MEDIUM range justified by 4 risks at High/Critical impact |
| Threat Model First | M1 = foundation | parallel with feature work | Eliminates late-stage rework on security controls |
| OAuth Sequencing | After core auth (M4) | Parallel with M3 | Lock JWT shape before federated identity layered on |
| 2FA Placement | Defense layer (M6) | Federated identity (with OAuth) | 2FA mitigates brute force (RISK-002), not federation |

## Success Criteria

| ID | Criterion | Validates Milestone(s) | Measurable |
|----|-----------|----------------------|------------|
| SC-001 | All FR requirements implemented and tested | M2–M7 | Yes |
| SC-002 | OWASP compliance verified via security scan | V2 | Yes |
| SC-003 | Load testing confirms 10K concurrent sessions | V1 | Yes |
| SC-004 | OAuth2 flow works for Google and GitHub | M4 | Yes |
| SC-005 | Audit logs capture all auth events | M5, V2 | Yes |
