# Diff Analysis: Roadmap Comparison

## Metadata

- **Generated**: 2026-05-22T20:36:00Z
- **Variants compared**: 2 (variant-1-opus-default, variant-2-sonnet-default)
- **Source spec**: `/config/workspace/IronClaude/tests/sc-roadmap/fixtures/sample_spec.md`
- **Total differences found**: 38 (5 structural, 20 content, 4 contradictions, 9 unique contributions per variant, 10 shared assumptions)
- **Categories**: structural (5), content (20), contradictions (4), unique (19), shared assumptions (10)

---

## Structural Differences

| # | Area | Variant 1 (opus) | Variant 2 (sonnet) | Severity |
|---|------|------------------|-------------------|----------|
| S-001 | Total duration | 18 weeks across 5 milestones (3+4+3+4+4) | 14 weeks across 5 milestones (3+3+2+2+4) | Medium |
| S-002 | M1 scope philosophy | Foundation-only: infra, crypto, observability, CI, threat model — NO user-facing features ship | Full core auth: registration + login + JWT + refresh + password reset all in M1 | High |
| S-003 | Risk-mitigation placement | R-001 in M2, R-002 in M4, defense-in-depth via M1 foundations | R-001 in M2, R-002 in M2, R-004 in M1/M3/M5 (compressed into M2) | Medium |
| S-004 | Deliverable formatting | Bullet lists with bolded IDs and prose descriptions | Markdown tables (ID/Deliverable/Description) per milestone | Low |
| S-005 | Top-level section structure | Identical: Exec Summary → Milestones → Cross-Cutting → Risk Register → Success Criteria | Identical | Low |

---

## Content Differences

| # | Topic | Variant 1 (opus) Approach | Variant 2 (sonnet) Approach | Severity |
|---|-------|---------------------------|----------------------------|----------|
| C-001 | Password hashing algorithm | Argon2id (m=64MB, t=3, p=4) per OWASP ASVS 4.0 §2.4 | bcrypt cost factor 12 | High |
| C-002 | Language/framework | Framework-agnostic; Node.js 20 LTS as reference only; explicit "substitute equivalents" | Python 3.11+ / FastAPI pinned throughout | Medium |
| C-003 | Refresh token TTL | 30 days, rotated on every refresh, family-revocation on reuse | 7 days, rotated on every refresh | Medium |
| C-004 | OAuth2 flow specification | Explicit Authorization Code + PKCE (RFC 7636, S256) + state in Redis; nightly OIDC discovery contract tests | Library-mediated (google-auth v2.x); no PKCE mention; GitHub uses access_token endpoint | High |
| C-005 | Threat model | STRIDE-style document signed off in M1 (D1.7) | Not present | High |
| C-006 | Audit log retention policy | 13 months hot in PostgreSQL → S3 with object-lock for 7-year retention (SOC2/GDPR) | Append-only PG table; retention not specified | Medium |
| C-007 | SLO instrumentation | Error-budget burn-rate alerts (fast 2%/1h, slow 5%/6h), explicit budget windows | Prometheus alert on p99>200ms for 5min; no burn-rate windows | Medium |
| C-008 | PII encryption strategy | Column-level pgcrypto AES-256-GCM + per-column KMS key references | Application-level AES-256-GCM, env-injected key | Medium |
| C-009 | HA infrastructure target | Kubernetes Helm + HPA on `concurrent_sessions` metric + PodDisruptionBudget min-available=2 | Docker Compose with 2 FastAPI replicas + nginx LB + PG streaming replication + Redis Sentinel | High |
| C-010 | Admin dashboard tech | "Server-rendered or SPA — implementation choice" | React 18 SPA + TypeScript + TanStack Table at `/admin/`, Chrome 120+/Firefox 121+ tested | Low |
| C-011 | 2FA recovery codes | 10 single-use codes (10 chars), Argon2id-hashed | 10 codes (8 chars alphanumeric), bcrypt-hashed | Low |
| C-012 | Account lockout strategy | Progressive: 5 fails → 15min lock; 3 lockout cycles → require password reset | Single tier: 10 fails in 15min → lockout | Medium |
| C-013 | Rate-limiter algorithm | Token-bucket via Redis Lua script (atomicity) | Sliding window via fastapi-limiter | Low |
| C-014 | Account deactivation→erasure | 30-day grace → automatic erasure job UNLESS legal hold flag is set | 30-day window → enters GDPR deletion queue | Low |
| C-015 | Email verification token | 32-byte base64url opaque random, 24h TTL | JWT-signed token, 15min TTL | Medium |
| C-016 | Role taxonomy | `admin`, `user`, `support` (3 functional roles) | `admin`, `user`, `suspended` (status conflated with role) | Medium |
| C-017 | Email-change flow | Re-verification required on new email; behavior of old email not specified | Old email remains active until new email is verified | Low |
| C-018 | API endpoint paths | `/auth/*` (unversioned) | `/api/v1/auth/*` (versioned) | Low |
| C-019 | Contract testing focus | Nightly contract tests vs Google/GitHub published OIDC discovery endpoints | Schemathesis vs own OpenAPI 3.1 spec on every PR | Medium |
| C-020 | Concurrent-sessions load test | k6 30-minute mixed workload at 10K active sessions, NFR-001 + NFR-002 both asserted | k6 5-minute sustained 10K sessions, p99<200ms zero 5xx | Medium |

---

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | OWASP-recommended password hashing | Argon2id is the OWASP ASVS 4.0 §2.4 current recommendation | bcrypt cost 12 is acceptable but inferior; OWASP allows it as fallback | High — V2 ships a verifiably weaker default while both claim NFR-003 (OWASP) compliance |
| X-002 | NFR-002 + NFR-005 realizability with stated infra | k8s HPA + PDB designed for sustained 10K with rolling deploys without SLO breach | Docker Compose with 2 app replicas + nginx LB; no HPA; manual scaling | High — V2's stated infra cannot meet 99.9% uptime + 10K sessions + rolling deploys simultaneously (single-host failure = >50% capacity loss) |
| X-003 | OAuth 2.0 BCP (RFC 9700) compliance | PKCE explicit with S256 (BCP §2.1.1 mandates PKCE for public clients) | No PKCE mention; library may or may not enable PKCE by default for google-auth; explicit code-for-token exchange for GitHub | High — V2 claims OWASP/auth compliance but does not surface PKCE as a deliverable; risk of misconfiguration |
| X-004 | Internal V1: refresh-token TTL vs revocation guarantees | 30-day refresh tokens + cookie SameSite=Strict + family revocation on reuse | (N/A — internal V1 only) | Medium — long TTL trades convenience for incident-blast-radius; mitigated by family-revocation but not by token-lifetime |

---

## Unique Contributions

### From Variant 1 (opus)

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | Explicit OWASP Top 10 (2021) A01–A10 mapping table with per-control milestone reference | High |
| U-002 | V1 | Refresh-token family revocation on reuse detection per RFC 9700 §2.2.2 | High |
| U-003 | V1 | STRIDE threat model as M1 deliverable D1.7, signed off by security reviewer | High |
| U-004 | V1 | Audit log retention policy: 13-month hot + S3 object-lock 7-year (SOC2/GDPR-aligned) | Medium |
| U-005 | V1 | SLO error-budget burn-rate alerts (fast 2%/1h, slow 5%/6h) | Medium |
| U-006 | V1 | HIBP k-anonymity API (or local bloom filter) for breached-password denylist on registration | Medium |
| U-007 | V1 | Mandatory 2FA for `admin` role (not just opt-in) | Medium |
| U-008 | V1 | Chaos-engineering acceptance tests: OAuth-provider-outage (M3), Redis failover (M4), DB failover (M5) | Medium |
| U-009 | V1 | GA readiness sign-off gate: security, SRE, product, legal/privacy (D5.9) | Medium |
| U-010 | V1 | GDPR 72h breach-notification runbook (Art. 33) (D5.8) | Medium |
| U-011 | V1 | mTLS between auth-api and PostgreSQL/Redis "where deployment topology supports it" | Low |

### From Variant 2 (sonnet)

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-012 | V2 | Concrete Python library pinning: pyotp v2.x, google-auth v2.x, fastapi-limiter, Alembic, Schemathesis | Medium |
| U-013 | V2 | Schemathesis API contract conformance against OpenAPI 3.1 in CI on every PR | Medium |
| U-014 | V2 | React 18 + TanStack Table admin SPA with explicit browser-compat targets (Chrome 120+/Firefox 121+) | Medium |
| U-015 | V2 | Email-change flow keeps old email valid until new email is verified (eliminates lockout window) | Medium |
| U-016 | V2 | Explicit Redis Sentinel for Redis automatic failover | Medium |
| U-017 | V2 | Versioned API paths (`/api/v1/auth/*`) — supports future deprecation cycles | Medium |
| U-018 | V2 | Database query-plan CI test (EXPLAIN ANALYZE asserts index scans, no seq scans) | Medium |
| U-019 | V2 | Explicit pagination semantics (default 50, max 200) on all list endpoints | Low |
| U-020 | V2 | Admin user list performance gate: <500ms with 50K users (operational-realism criterion) | Medium |

---

## Shared Assumptions

These are implicit preconditions both variants depend on. UNSTATED items are promoted to synthetic [SHARED-ASSUMPTION] diff points for debate consideration.

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|-------|------------|------------------|----------------|----------|
| A-001 | "10K concurrent sessions" (NFR-002) means 10K **steady-state active sessions**, not 10K logins/sec or 10K req/sec | Both variants size capacity (V1 HPA targets, V2 Redis 4GB) against active-session count, not request rate | **UNSTATED** | [SHARED-ASSUMPTION] |
| A-002 | RBAC is sufficient for FR-004; no need for ABAC (attribute-based access control) | Both ship role+permission tables with role-on-JWT; neither considers attribute predicates | **UNSTATED** | [SHARED-ASSUMPTION] |
| A-003 | The system is single-tenant; no organization/workspace partitioning of users | Neither variant introduces `tenant_id` columns or scope-by-org middleware | **UNSTATED** | [SHARED-ASSUMPTION] |
| A-004 | OAuth2 providers are limited to {Google, GitHub} for the foreseeable future | Both hard-code the two providers; neither builds a provider-plugin abstraction | **STATED** (in spec FR-003) | No |
| A-005 | Password reset via email is acceptable even though a compromised email = compromised account | Both ship password reset flows without requiring 2FA-bypass-prevention on reset | **UNSTATED** | [SHARED-ASSUMPTION] |
| A-006 | SendGrid email delivery is reliable enough that registration/password-reset/2FA-enrollment do not need fallback delivery paths | Both treat SendGrid as the sole email channel; no fallback to SMTP/SES/etc. | **STATED** (in spec dependencies) | No |
| A-007 | Refresh tokens are session-scoped, not device-scoped; the system does not distinguish "logout from this device" vs "logout everywhere" until M5 admin features | V1 mentions family_id (OAuth reuse-detection); V2 has token_id but no device fingerprint | **UNSTATED** | [SHARED-ASSUMPTION] |
| A-008 | Audit log immutability is enforced at the database layer (PG triggers / restricted grants) — application-layer enforcement is not sufficient | Both reach for DB-level append-only enforcement | **STATED** (in both variants' D4.6 / D3.4) | No |
| A-009 | The 12 FRs and 6 NFRs are complete; no additional implicit requirements (e.g., SSO/SAML for enterprise, federation outside OAuth2) emerge during build | Both treat the spec as closed; neither schedules requirements-refresh checkpoints | **UNSTATED** | [SHARED-ASSUMPTION] |
| A-010 | The audit log retention requirement is implicit (V1 assumes 7-year SOC2/GDPR; V2 leaves unspecified) | Disagreement classifies as **CONTRADICTED** — V1 commits to 7yr S3 lock, V2 has no policy | **CONTRADICTED** | [SHARED-ASSUMPTION] |

**Promoted shared-assumption diff points** (added to denominator for convergence calculation):

| A-NNN | Assumption | Impact | Status |
|-------|------------|--------|--------|
| A-001 | 10K = sessions, not req/sec | Mis-sized capacity plan if interpretation wrong | UNSTATED |
| A-002 | RBAC suffices over ABAC | Permission-grid explosion if multi-axis perms needed | UNSTATED |
| A-003 | Single-tenant deployment | Tenant retrofit is invasive (schema + every query) | UNSTATED |
| A-005 | Email-reset blast radius | Account takeover via email compromise; 2FA-on-reset would help | UNSTATED |
| A-007 | Session ≠ device scope | Device-list UX & per-device logout require non-trivial refactor | UNSTATED |
| A-009 | Spec is closed | Mid-build SSO/SAML requirement = major scope shift | UNSTATED |
| A-010 | Audit retention period | Retention drives storage cost + legal-hold posture | CONTRADICTED |

---

## Summary

- **Total structural differences**: 5 (1 High, 2 Medium, 2 Low)
- **Total content differences**: 20 (4 High, 9 Medium, 7 Low)
- **Total contradictions**: 4 (3 High cross-variant, 1 Medium intra-variant)
- **Total unique contributions**: 20 (11 from V1, 9 from V2)
- **Total shared assumptions surfaced**: 10 (7 UNSTATED → promoted, 2 STATED, 1 CONTRADICTED → promoted)
- **Total diff points (for convergence denominator)**: 5 + 20 + 4 + 20 + 7 = **56 points** (the 3 STATED/non-promoted A items are excluded)

**Highest-severity items**: S-002, C-001, C-004, C-005, C-009, X-001, X-002, X-003, U-001, U-002, U-003

**Similarity check**: 56 / ~140 comparable items ≈ 40% diff density — well above the 10% similarity threshold; full adversarial pipeline proceeds.
