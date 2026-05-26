# Diff Analysis: Roadmap Comparison

## Metadata

- Generated: 2026-05-22T16:50:00Z
- Variants compared: 2 (variant-1-opus-default, variant-2-sonnet-default)
- Source spec: `tests/sc-roadmap/fixtures/sample_spec.md`
- Total differences found: 49 (S:6 + C:18 + X:6 + U:14 + A:5)

---

## Structural Differences

| #     | Area                          | Variant 1 (opus)                                                                        | Variant 2 (sonnet)                                                                        | Severity |
|-------|-------------------------------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|----------|
| S-001 | Total duration                | 14 weeks (~7 two-week sprints)                                                          | 17 weeks (~8.5 sprints)                                                                   | Medium   |
| S-002 | Milestone topical grouping    | Foundation/Crypto → Login/JWT → OAuth+2FA → Governance → Hardening                       | Data+Core Auth (combined) → OAuth+Reset → Security+RBAC+Audit → User Mgmt → Perf          | High     |
| S-003 | Where login + registration live | Split: registration in M1, login in M2                                                | Combined: both in M1                                                                       | Medium   |
| S-004 | Where audit scaffolding lives | M1 (D1.5 scaffolds `auth_events` table day-one, called from registration)               | M3 (D3.9 introduces audit table; M1/M2 events captured retroactively)                     | High     |
| S-005 | Where rate limiting lives     | M2 (alongside login, D2.4)                                                              | M3 (after OAuth/reset, alongside RBAC, D3.7)                                              | Medium   |
| S-006 | Deliverable format            | Bulleted per-deliverable narrative + per-milestone tables                               | Tables of (ID, Deliverable, Source Coverage) per milestone — more tabular throughout      | Low      |

---

## Content Differences

| #     | Topic                         | Variant 1 Approach                                                                                       | Variant 2 Approach                                                                                                | Severity |
|-------|-------------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|----------|
| C-001 | Password hashing              | Argon2id, params m=64MB t=3 p=4, calibrated to 250ms (OWASP 2025 recommendation)                         | bcrypt cost factor 12                                                                                              | High     |
| C-002 | Refresh token TTL             | 30 days, opaque, hashed in Redis, family-rotation (IETF OAuth 2.0 Security BCP)                          | 7 days, opaque, stored in Redis, rotated on each use with replay detection                                        | High     |
| C-003 | Access token revocation       | Redis bloom-filter denylist on jti, TTL = access-token TTL (`<0.1%` FP rate target)                      | None for access tokens ("no revocation list needed"); relies on short TTL + refresh revocation                    | High     |
| C-004 | RBAC model                    | Dynamic: roles + permissions + role_permissions + user_roles; perms denormalized into JWT `perms[]` claim | Static 4-role hierarchy: viewer → editor → admin → superadmin                                                     | High     |
| C-005 | Permission propagation        | Role change adds existing tokens to denylist; next refresh re-mints (D4.3)                              | "Immediately reflected in subsequent JWT refreshes" (waits for refresh; no explicit revocation)                   | High     |
| C-006 | Rate-limit algorithm          | Token bucket via `slowapi` + Redis (5/15min for login, IP+email composite key)                          | Sliding-window via Redis (10/min for login)                                                                       | Medium   |
| C-007 | Account lockout policy        | 10 failed logins / 1 hour; HTTP 423 Locked with Retry-After (separate from 429 rate-limit)              | 5 failed / 15-min lockout; admin override unlock                                                                  | Medium   |
| C-008 | Deactivation grace period     | 30-day soft-delete window; admin override for immediate hard-delete                                      | 14-day grace; explicit `/auth/reactivate` endpoint during grace                                                   | Medium   |
| C-009 | 2FA secret storage            | AES-GCM with KMS key DISTINCT from column-encryption key (defense-in-depth)                              | "Stored encrypted in user_2fa table" — no key separation specified                                                | High     |
| C-010 | Recovery codes hashing        | bcrypt-12, 10 codes generated at enrollment, single-use enforced                                         | "Hashed and stored, each usable once" — algorithm unspecified                                                     | Medium   |
| C-011 | JWT library                   | `python-jose[cryptography]` with RS256                                                                   | RS256 specified; library unspecified                                                                              | Low      |
| C-012 | OAuth library                 | `authlib` (named, justified)                                                                              | Unspecified; provider flows described abstractly                                                                  | Low      |
| C-013 | TOTP library                  | `pyotp`                                                                                                  | "pyotp for Python, otp for Go" (language-agnostic mention)                                                        | Low      |
| C-014 | Email verification token      | 32-byte CSPRNG, SHA-256 stored, 24-hour TTL                                                              | Token via SendGrid template (TTL unspecified for verification; password-reset = 15min signed JWT)                  | Medium   |
| C-015 | Pentest                       | External pentest engagement (Cobalt or equivalent), 4-week lead time, gates GA                          | OWASP ZAP full scan only — no external human pentest                                                              | High     |
| C-016 | Chaos engineering             | D5.2 — kill Redis primary mid-traffic, kill API replica, partition DB read-replica                       | Absent — soak test only                                                                                            | High     |
| C-017 | DR runbook + targets          | RTO 1 hour, RPO 5 minutes; tabletop exercise required; key rotation drill                                | "Production deployment runbook" only; no RTO/RPO numbers; no rotation drill                                       | High     |
| C-018 | Soak test duration            | 1 hour sustained @ 10K                                                                                   | 4 hours sustained @ 10K                                                                                            | Medium   |

---

## Contradictions

| #     | Point of Conflict                  | Variant 1 Position                                                                          | Variant 2 Position                                                                            | Impact |
|-------|------------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|--------|
| X-001 | Password hashing algorithm         | Argon2id is OWASP 2025 recommendation; bcrypt is acceptable but Argon2id is forward choice  | bcrypt cost 12 is sufficient                                                                  | High   |
| X-002 | Refresh-token lifetime             | 30-day refresh TTL                                                                           | 7-day refresh TTL                                                                              | High   |
| X-003 | Access-token revocability model    | Bloom-filter denylist enables instant access-token revocation                                | "No revocation list needed for access tokens" — incompatible with rapid role-change response  | High   |
| X-004 | RBAC architecture                  | Dynamic resource:action permissions matrix, perms claim denormalized into JWT                | Static role hierarchy, no permission composition                                              | High   |
| X-005 | Audit storage establishment timing | Audit substrate ships in M1 day-one (D1.5) before any login surface exists                  | Audit table introduced in M3 alongside RBAC; M1/M2 events captured by event emission, not table | High   |
| X-006 | Deactivation grace window          | 30 days                                                                                      | 14 days                                                                                        | Medium |

---

## Unique Contributions

| #     | Variant | Contribution                                                                                                              | Value  |
|-------|---------|---------------------------------------------------------------------------------------------------------------------------|--------|
| U-001 | V1      | Chaos engineering drill (D5.2): kill Redis primary, kill API replica, partition DB read-replica                          | High   |
| U-002 | V1      | DR runbook with RTO 1hr / RPO 5min targets + tabletop exercise (D5.5)                                                    | High   |
| U-003 | V1      | Key rotation drill (D5.6) — JWT signing key + column-encryption key, exercised in staging                                | High   |
| U-004 | V1      | External pentest engagement (Cobalt) with 4-week lead, gates GA (D5.4)                                                   | High   |
| U-005 | V1      | IR playbook for PII breach with 72-hr GDPR notification timeline (D5.7)                                                  | High   |
| U-006 | V1      | STRIDE threat-modeling pass at start of M2/M3/M4 (each new surface)                                                       | Medium |
| U-007 | V1      | Refresh-token family-rotation per IETF OAuth 2.0 Security BCP (replay detection within 100ms)                            | High   |
| U-008 | V1      | Permission-change propagation via denylist (D4.3) — next request after role change yields 401 within 1s                  | High   |
| U-009 | V1      | Trusted-device 30-day cookie bound to UA + IP /24 (D3.6)                                                                  | Medium |
| U-010 | V1      | Feature flags via `unleash` for risky rollouts (OAuth, 2FA, hard-delete)                                                  | Medium |
| U-011 | V1      | mTLS between API and Redis (D1.4)                                                                                          | Medium |
| U-012 | V2      | Avatar upload to S3/R2 with signed URL for download (D4.2)                                                                | Medium |
| U-013 | V2      | Explicit `/auth/reactivate` endpoint during grace period (D4.6) — separates intent from passive grace                    | Medium |
| U-014 | V2      | `audit_events` DB role granted only INSERT + SELECT — application-tamper-resistant at DB-role level                       | High   |

---

## Shared Assumptions

| #     | Assumption                                                                                                | Source Agreement                                       | Impact   | Status        |
|-------|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------|----------|---------------|
| A-001 | Single-region, single-AZ-resilient deployment is acceptable (no multi-region active-active)               | Both: NFR-005 99.9% addressed via failover only        | Medium   | UNSTATED      |
| A-002 | Regulatory scope is GDPR + OWASP only (no HIPAA, PCI-DSS, CCPA, SOC2)                                     | Both: only GDPR + OWASP cited                          | High     | UNSTATED      |
| A-003 | Web/REST-only API surface; no GraphQL, gRPC, or native mobile SDK in scope                                | Both: API described as REST only; V2 calls out no SDK   | Medium   | STATED (V2)   |
| A-004 | A single team can absorb the entire 14- or 17-week critical path with available skills                   | Both: V1 mentions "1 engineer on critical path"; V2 silent on staffing | High | UNSTATED |
| A-005 | "p95 < 200ms" (NFR-001) measurement boundary is the auth service edge (after TLS termination, before downstream calls) — neither variant pins the measurement point | Both: report p95 against k6/Locust without defining where the timer starts | Medium | CONTRADICTED |

---

## Summary

- Total structural differences: 6
- Total content differences: 18
- Total contradictions: 6
- Total unique contributions: 14
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 1)
- Highest-severity items: S-002, S-004, C-001, C-002, C-003, C-004, C-005, C-009, C-015, C-016, C-017, X-001, X-002, X-003, X-004, X-005, U-001, U-002, U-003, U-004, U-005, U-007, U-008, U-014, A-002, A-004
- Similarity check: differences ≥ 10% of comparable items → debate REQUIRED (no skip)

---

## Taxonomy Auto-Tagging (AD-5)

| Diff Point | Level | Rationale |
|------------|-------|-----------|
| S-001 (duration) | L1 | Surface — estimation difference, no state mechanics |
| S-002 (milestone grouping) | L2 | Structural — organization model |
| S-003 (login+reg split) | L2 | Structural — module boundaries |
| S-004 (audit timing) | L3 | State-mechanics — when state-recording substrate becomes available affects every prior event's observability |
| S-005 (rate limit timing) | L3 | State-mechanics — guard condition for R-002, gap between login ship and rate limit |
| S-006 (format) | L1 | Surface — presentation |
| C-001 (Argon2 vs bcrypt) | L3 | State-mechanics — cryptographic invariant choice |
| C-002 (refresh TTL) | L3 | State-mechanics — token-lifetime guard |
| C-003 (access revocation) | L3 | State-mechanics — revocation invariant |
| C-004 (RBAC model) | L2 | Structural — authorization architecture |
| C-005 (perm propagation) | L3 | State-mechanics — propagation guard condition |
| C-006 (rate-limit algo) | L3 | State-mechanics — boundary semantics (sliding vs bucket) |
| C-007 (lockout policy) | L3 | State-mechanics — guard threshold |
| C-008 (deactivation grace) | L2 | Structural — workflow length |
| C-009 (2FA key separation) | L3 | State-mechanics — boundary between encryption domains |
| C-010 (recovery code hash) | L2 | Structural — choice of algorithm class |
| C-011–C-013 (library names) | L1 | Surface |
| C-014 (email verify token) | L3 | State-mechanics — token entropy + TTL guard |
| C-015 (pentest) | L2 | Structural — validation methodology |
| C-016 (chaos eng) | L2 | Structural — validation methodology |
| C-017 (DR targets) | L2 | Structural — operational readiness scope |
| C-018 (soak duration) | L1 | Surface — test parameter |
| X-001–X-006 | L3 | State-mechanics (all are guard/invariant conflicts) |
| A-001–A-005 (shared assumptions, state/guard terms) | L3 | State-mechanics (per AC-AD5-3) |

**Coverage check:** L1=6 points, L2=11 points, L3=23+ points. All three taxonomy levels covered → no forced round trigger needed.
