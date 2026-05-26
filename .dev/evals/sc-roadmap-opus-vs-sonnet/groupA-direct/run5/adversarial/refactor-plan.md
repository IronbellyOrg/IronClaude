# Refactor Plan: V1 Base → Merged Roadmap

## Overview

- **Base variant**: variant-1-opus-default.md
- **Contributions incorporated from**: variant-2-sonnet-default.md + invariant probe findings
- **Total planned changes**: 17 (11 V2 incorporations + 6 mandatory invariant resolutions)
- **Overall risk**: Medium (additive changes are low-risk; invariant resolutions touch core schema and security)
- **Review status**: Auto-approved (no `--interactive` flag); changes flow directly to merge executor

---

## Planned Changes

### Category A: V2 Strength Incorporations (11 items)

#### Change #1: Adopt versioned API paths

- **Source**: V2 C-018, U-017 (`/api/v1/auth/*` throughout)
- **Target location**: All endpoint definitions in V1 M2 (D2.1–D2.10), M3 (D3.2–D3.4), M4 (D4.2–D4.8), M5 (D5.1–D5.2)
- **Rationale**: Versioning supports future deprecation cycles without breaking clients. Per debate, V1 advocate fully conceded this point. Trivial change, no schedule impact.
- **Integration approach**: Replace all `/auth/*` with `/api/v1/auth/*` and `/me/*` with `/api/v1/me/*`; add deprecation-header policy note to Cross-Cutting Concerns.
- **Risk level**: Low (additive — no breaking change to V1 base)

#### Change #2: Add walking-skeleton login to M1

- **Source**: V2 critique 1 (M1 foundation-only delays integration feedback); V1 advocate R2 concession
- **Target location**: V1 M1 — add new deliverable D1.8 "Walking-skeleton login endpoint"
- **Rationale**: A thin `POST /api/v1/auth/login` returning a stub JWT against the encrypted schema by end of week 2-3 de-risks the foundation against real traffic before M2 expands the surface. Crypto + schema is the long pole; HTTP handler is incremental.
- **Integration approach**: Add D1.8 with acceptance criterion "happy-path login returns RS256 JWT for a seeded user; integration test runs against ephemeral PostgreSQL+Redis stack."
- **Risk level**: Low

#### Change #3: Pin technology stack via week-0 ADR

- **Source**: V2 C-002, V2 critique 2; V1 advocate R2 concession
- **Target location**: New section "## Week-0 Architecture Decision Record" before "## Milestones"; remove "(reference; substitute equivalents if implementing in Python/Go)" from line 7
- **Rationale**: Framework-agnostic wording creates hidden estimation debt. ADR captures the decision + rationale + substitution guide.
- **Integration approach**: Add ADR template recording chosen stack (default: Python 3.11+ / FastAPI / SQLAlchemy / Alembic / pyotp / authlib / OpenTelemetry) with explicit alternative for Node.js 20 LTS. V2's pinned libraries become the reference implementation inside the ADR.
- **Risk level**: Low

#### Change #4: Adopt admin <500ms@50K users performance gate + EXPLAIN ANALYZE CI

- **Source**: V2 U-018, U-020; V1 advocate R2 concession
- **Target location**: V1 M5 — extend D5.2 (admin dashboard) with explicit performance acceptance criterion; add D5.10 "Query-plan CI gate"
- **Rationale**: An admin user list that times out in production is a real incident. EXPLAIN ANALYZE in CI catches missing indexes at PR time.
- **Integration approach**: Add to D5.2 acceptance: "Admin user list loads in <500ms p95 with 50,000 seeded user records." Add D5.10: "CI step runs EXPLAIN ANALYZE on all frequently-used queries; PR fails if any query plan contains a sequential scan on >10K-row table."
- **Risk level**: Low

#### Change #5: Adopt pagination defaults (50 / max 200)

- **Source**: V2 U-019
- **Target location**: V1 M4–M5 list endpoints (admin user list D5.2, audit-log query D5.2, session management)
- **Rationale**: Consistent pagination semantics prevent client-side pagination bugs and over-fetch scenarios.
- **Integration approach**: Add to Cross-Cutting Concerns "API Conventions" subsection: "All list endpoints accept `page` (default 1) and `per_page` (default 50, max 200) query params; responses include `{results: [], total, page, per_page}` envelope."
- **Risk level**: Low

#### Change #6: Adopt Schemathesis contract testing per PR

- **Source**: V2 U-013; V1 advocate R2 concession ("add as addition, not replacement")
- **Target location**: V1 Cross-Cutting Concerns "Testing Strategy"
- **Rationale**: PR-level contract testing catches API regressions at the commit that introduces them.
- **Integration approach**: Add row to testing table: "Contract (own) | Schemathesis v3+ | API conformance vs OpenAPI 3.1 spec | Every PR (CI)". Coexists with existing nightly OIDC discovery contract tests against external providers (V1 D3.8).
- **Risk level**: Low

#### Change #7: Adopt email-change-keeps-old-email-valid (with INV-001 resolution)

- **Source**: V2 C-017, U-015; INV-001 resolution
- **Target location**: V1 D5.1 profile endpoints; V1 D1.1 schema
- **Rationale**: Eliminates lockout window if new-email verification fails.
- **Integration approach**: See "Mandatory Change #M1" below — coupled with INV-001 schema fix.
- **Risk level**: Medium (touches schema)

#### Change #8: Adopt Redis Sentinel (dev/test) + managed Redis (prod)

- **Source**: V2 U-016; V1 advocate R2 concession with scope split
- **Target location**: V1 D1.2 Redis configuration; V1 D5.4 production manifests
- **Rationale**: Sentinel is the standard Redis HA pattern for self-hosted; managed Redis (ElastiCache, Memorystore) is the production answer at k8s scale.
- **Integration approach**: Update D1.2: "Redis 7.2 cluster with Sentinel-based failover in dev/test docker-compose; production uses managed Redis (ElastiCache / Memorystore) referenced from Kubernetes Service." D5.4 inherits this.
- **Risk level**: Low

#### Change #9: Adopt markdown table deliverable format

- **Source**: V2 S-004; sprint-planning readability
- **Target location**: All V1 milestones (M1–M5 deliverable lists)
- **Rationale**: Scannable for sprint planning and status reviews.
- **Integration approach**: Convert V1's bullet-list deliverable sections to `| ID | Deliverable | Description |` tables. Preserve all content; only formatting changes.
- **Risk level**: Low (cosmetic)

#### Change #10: Add STRIDE-row revalidation to each milestone gate

- **Source**: V1 advocate R2 partial concession to V2 critique 4 (STRIDE unvalidated until M5)
- **Target location**: V1 M2, M3, M4, M5 acceptance criteria
- **Rationale**: Threat model assumptions validated incrementally, not deferred.
- **Integration approach**: Add to each milestone acceptance: "STRIDE threat model rows mapped to milestone scope are re-tested and signed off by named security reviewer within 2 business days of milestone completion." Name the reviewer role in M1 D1.7.
- **Risk level**: Low

#### Change #11: Adopt V2's spec-aligned role taxonomy (admin/user) with status separation

- **Source**: V2 C-016; V1 advocate R2 concession ("admin/user/support" is spec-unsupported)
- **Target location**: V1 D3.5 RBAC engine
- **Rationale**: Spec FR-004 names "role-based access control" without specifying role inventory; admin + user is the minimal spec-aligned set. Status (active/suspended/deactivated) lives on `users.status` orthogonal to role.
- **Integration approach**: Update D3.5: "roles: admin, user (default). users.status: active, suspended, deactivated (orthogonal to role). RBAC middleware checks role; lockout/suspension middleware checks status."
- **Risk level**: Low (simplifies V1's design)

### Category B: Mandatory Invariant Probe Resolutions (6 HIGH items)

These changes are NOT optional. The merged output must address each HIGH invariant finding directly OR document explicit accept-the-risk rationale.

#### Mandatory Change #M1: Resolve INV-001 (pending-email state representation)

- **Issue**: V1 schema has unique `email` column; adopting V2's "keep old email active until new verified" creates ambiguity about which email is in the `email` field during the pending window.
- **Resolution**: Add `pending_email` (nullable) and `pending_email_token_hash` (nullable) columns to `users` schema in D1.1. Login lookup keys on `email` (the current/old value). On verification of `pending_email`, transactionally update `email = pending_email` and clear pending fields, simultaneously revoking all refresh-token families to force re-login under the new email. Reset-password flow keys on `email` (not `pending_email`) — preventing account-takeover via reset to the pending address.
- **Target location**: V1 D1.1 schema; V1 D5.1 email-change endpoint
- **Risk level**: Medium (schema migration + transaction logic)

#### Mandatory Change #M2: Resolve INV-003 (admin promotion 2FA enrollment gate)

- **Issue**: Promoting a user to `admin` while they are logged in without 2FA bypasses the mandatory-2FA-for-admin invariant.
- **Resolution**: Role-change to `admin` triggers a server-side `pending_2fa_enrollment` flag on the user record AND revokes all refresh-token families. The user's next authenticated request returns HTTP 403 with `{"error": "admin_2fa_required", "next_step": "/api/v1/auth/2fa/enroll"}`. The 2FA-enroll endpoint is the only route allowed under this flag; on successful enrollment, the flag is cleared. For the first-admin bootstrap, define a one-shot bootstrap CLI command that creates the initial admin user WITH 2FA pre-provisioned via an out-of-band TOTP secret printed to the operator console (D1.8 acceptance criterion).
- **Target location**: V1 D3.5/D3.6 RBAC, D4.2 2FA enrollment, D1.8 bootstrap procedure
- **Risk level**: Medium (touches auth flow and operator UX)

#### Mandatory Change #M3: Resolve INV-010 (encrypted email + unique btree)

- **Issue**: Column-level AES-256-GCM with proper random IV is non-deterministic and cannot back a unique btree. Login `WHERE email = ?` requires either deterministic encryption (security antipattern) or a blind-index.
- **Resolution**: Add `email_blind_index BYTEA NOT NULL UNIQUE` column = HMAC-SHA256(lower(email), blind_index_key). Login and lookup queries key on `email_blind_index`; the encrypted `email_ciphertext` column is returned for display/audit only. Blind-index key is rotated separately from data-encryption key and is itself stored in KMS. Update D1.1 schema, D2.1 registration, D2.4 login, D5.1 email-change to use blind-index for lookup.
- **Target location**: V1 D1.1 schema; D2.1, D2.4, D5.1 lookup queries
- **Risk level**: Medium-High (cryptographic design; must be reviewed by security)

#### Mandatory Change #M4: Resolve INV-011 (S3 object-lock vs GDPR erasure)

- **Issue**: Object-lock 7-year retention is immutable by design; GDPR Art. 17 erasure 30-day flow cannot reach into already-archived audit events containing PII inside `metadata_jsonb`.
- **Resolution**: Two changes:
  (a) Audit-log writes redact PII from `metadata_jsonb` at write-time. Only stable references survive: `user_id` (UUID, opaque), `actor_id`, `request_id`, `event_type`, `result`, `ip_hash` (HMAC of IP, not raw IP), `user_agent_hash`. Email, name, phone, raw IP, raw user agent — NEVER written to `metadata_jsonb`.
  (b) Document the GDPR Art. 17(3)(b) legal-basis-for-retention rationale: "audit records retained for the establishment, exercise, or defense of legal claims." Place in V1 D4.8 erasure flow and D5.8 GDPR runbook.
  Result: erasure removes the `users` row's PII; audit `user_id` references survive without dragging PII into the immutable archive.
- **Target location**: V1 D4.6 audit logging, D4.7 retention, D4.8 erasure, D5.8 runbook
- **Risk level**: Medium (changes audit schema; requires legal review of retention basis)

#### Mandatory Change #M5: Resolve INV-013 (NFR-001 latency sufficiency)

- **Issue**: NFR-001 (<200ms p95) gates measure latency without accounting for Argon2id cold-process tax, RBAC permission-cache cold misses, and decryption overhead. Necessity-only proof; sufficiency not shown.
- **Resolution**: Three changes:
  (a) Argon2id parameters: re-validate `m=64MB, t=3, p=4` against the target deployment instance class. If cold-process exceeds 200ms on the chosen instance, reduce to `m=46MB, t=2, p=2` (still OWASP-acceptable per ASVS 4.0 §2.4.1 Tier 2 recommendation) and document in week-0 ADR.
  (b) RBAC cache warm-on-deploy: add cache pre-warming step to deployment runbook (D5.4). Pod readiness probe `/health/ready` only returns 200 after permission cache is loaded for the top-100 active users (rolling window).
  (c) Latency gate scope: M2 acceptance updated to measure p95 with cold-Redis (cache flushed at test start) for the first 60 seconds of load, then warm-cache p95 for the remainder. Both must satisfy NFR-001.
- **Target location**: V1 D1.4 crypto utility, D3.5 RBAC cache, D5.4 deployment, M2 acceptance, M5 D5.6 load test
- **Risk level**: Medium (touches multiple components; explicit performance budget)

#### Mandatory Change #M6: Resolve INV-015 (NFR-005 SLO sufficiency)

- **Issue**: 99.9% uptime claim assumes HPA+PDB are sufficient. Serial dependency availability product (own + SendGrid + Google + GitHub + PG + Redis) is unbounded; SLO scope (which endpoints count, which deps excluded) is undefined.
- **Resolution**: Add explicit SLO definition document as D5.5 sub-deliverable:
  (a) **In scope**: `/api/v1/auth/login`, `/api/v1/auth/refresh`, `/api/v1/auth/oauth/callback`, RBAC-protected `/api/v1/me/*` reads.
  (b) **Excluded from SLO** (delivery-dependent endpoints with documented graceful degradation): `/api/v1/auth/register` (depends on SendGrid), `/api/v1/auth/password-reset/request` (depends on SendGrid), `/api/v1/auth/oauth/start` (depends on OAuth providers — already has fallback per D3.7).
  (c) **Dependency exclusion policy**: When an excluded dependency is degraded, the affected endpoints continue to count in observability but are excluded from SLO until restored. Burn-rate alerts target only in-scope endpoints.
  (d) **Documented MTBF/MTTR per dependency**: SendGrid 99.95% / 30min, Google OIDC 99.95% / 60min, GitHub OAuth 99.9% / 90min, managed PG 99.99% / 30s, managed Redis 99.99% / 30s. The product of in-scope dependencies (PG × Redis × own) = 99.97% × 99.97% × HPA-mitigated own = exceeds 99.9% with headroom.
- **Target location**: V1 D5.5 SLO instrumentation
- **Risk level**: Medium (documentation + observability scope changes)

---

## Changes NOT Being Made (Rejected Alternatives)

| Diff Point | Non-base Approach | Rationale for Rejection |
|-----------|-------------------|------------------------|
| C-001 password hashing | V2's bcrypt cost-12 | OWASP ASVS 4.0 §2.4.1 ranks Argon2id first; V2 advocate conceded this in R1 |
| C-004 OAuth | V2's library-mediated (no PKCE in deliverable) | RFC 9700 §2.1.1 mandates PKCE for public clients; V2 advocate conceded |
| C-009 HA | V2's Docker Compose for production | Single-host blast radius incompatible with NFR-002 + NFR-005 + rolling deploys; V2 advocate conceded |
| C-012 lockout | V2's single-tier 10 fails / 15min | V1's progressive (5 fails → 15min; 3 cycles → reset) is more resilient to slow brute force; V2 advocate conceded |
| C-013 rate limiter | V2's fastapi-limiter without Lua atomicity | Non-atomic INCR+EXPIRE races at 10K concurrent; V2 advocate conceded |
| C-015 email token | V2's JWT-signed verification token + 15-min TTL | Opaque 32-byte random with 24h TTL eliminates signing-key blast radius and accommodates email-delivery delays; V2 advocate conceded |
| C-002 stack (full pin to Python) | V2's full hard pin without ADR alternative | Spec is language-agnostic; week-0 ADR captures the choice + alternative implementation guide |
| Audit retention policy | V2's silence (no retention policy) | GDPR Art. 5(1)(e) requires defined retention; V2 advocate explicitly conceded V1's 13mo+7yr policy |
| Roles | V2's `admin/user/suspended` enum | `suspended` is status, not role; status moved to orthogonal `users.status` column (Change #11) |
| V1 30-day refresh TTL | V2's 7-day TTL | V1's family-revocation-on-reuse mitigates blast radius; longer TTL is better UX |
| Threat model | Defer to M5 (V2 implicit) | Foundation-stage threat model catches design flaws before code; cheap insurance |
| OWASP A01-A10 mapping | Omit (V2 doesn't have one) | NFR-003 compliance demands an audit-ready mapping artifact |

---

## Risk Summary

| Change ID | Risk Level | Impact if Wrong | Rollback |
|-----------|-----------|-----------------|----------|
| #1–#11 (V2 incorporations) | Low | Cosmetic or additive features; reversible | Revert deliverable changes |
| #M1 (pending-email) | Medium | Email-change UX breakage; account-takeover risk if wrong | Schema migration is reversible; logic guards with feature flag |
| #M2 (admin 2FA gate) | Medium | First-admin lockout if bootstrap missed | Bootstrap CLI documented; restore via DB-level role flip |
| #M3 (blind-index) | Medium-High | Login broken if blind-index key misconfigured | Schema migration is reversible; deploy behind feature flag with dual-read fallback |
| #M4 (audit redaction) | Medium | Audit schema change; legal-review-required | Schema change is forward-only; redaction is at write-time so historical events unaffected |
| #M5 (latency budget) | Medium | Argon2id param change reduces hash cost; explicit performance budget breakage signals real issue | ADR documents both parameter tiers |
| #M6 (SLO scope) | Medium | Burn-rate alerts retargeted; observability scope change | Documentation change; reverts cleanly |

**Overall**: Medium aggregate risk. The 6 mandatory invariant resolutions are non-trivial but each is bounded, documented, and reversible.

---

## Review Status

- **Default**: Auto-approved (no `--interactive` flag passed)
- **Approval timestamp**: 2026-05-22T20:36:00Z
- **Approver**: sc:adversarial-protocol orchestrator (debate-orchestrator role)
- **User-override**: None
