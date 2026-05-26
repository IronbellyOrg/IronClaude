# Round 1 — Variant 2 Advocate (sonnet / default persona)

## Position Summary

Variant 2 delivers a more practical, immediately executable roadmap that prioritizes getting working auth into users' hands faster while maintaining rigorous security. It combines registration and login into a single functional milestone (M1), enforces a tamper-proof audit trail at the database role level (U-014), and subjects the final system to a 4-hour soak test (C-018) that is four times longer than Variant 1's. Where V1 over-invests in forward-looking architecture that the spec does not require (dynamic permission matrices, bloom-filter denylists, chaos engineering drills), V2 delivers exactly what the spec asks for -- and does so with clearer effort estimates, explicit FR/NFR coverage matrices, and a more honest admission of what is out of scope.

---

## Steelman of Variant 1

Before arguing for V2, I must acknowledge what V1 genuinely gets right. Variant 1 is a more *ambitious* document, and several of its choices reflect real operational wisdom.

**1. Day-one audit substrate (S-004, D1.5).** V1 scaffolds the `auth_events` table and `AuditLogger` service interface in M1, calling it from registration and password-reset code from the very first commit. This means every authentication event is captured from day one. There is no window -- however brief -- where registration events go unlogged. V2 delays the audit table to M3 and admits it would capture M1/M2 events "retroactively" via event emission rather than direct table writes. V1's approach is strictly superior for compliance: you cannot retroactively create audit records with trustworthy timestamps. This is V1's single strongest structural argument.

**2. Access-token revocation via bloom-filter denylist (C-003, X-003, D2.2).** V1 adds a Redis bloom filter that tracks revoked `jti` claims with a TTL equal to the access-token TTL, targeting a `<0.1%` false-positive rate. This enables immediate invalidation of access tokens when roles change (D4.3) or sessions are terminated. V2's position -- "no revocation list needed for access tokens" (C-003) -- is defensible only if you accept that a 15-minute window of stale permissions is tolerable. For many applications it is, but V1's approach is more principled: if you say a token is revoked, it should *actually be revoked*, not "revoked after the next refresh." This matters most for admin-demoted users who retain elevated access for up to 15 minutes.

**3. Argon2id over bcrypt (C-001, X-001).** V1 adopts Argon2id calibrated to ~250ms (m=64MB, t=3, p=4), explicitly citing OWASP 2025. V2 uses bcrypt cost factor 12. While bcrypt-12 is not *wrong* -- it is explicitly listed as acceptable by OWASP -- Argon2id is the current recommendation specifically because it resists GPU-based attacks better than bcrypt. V1 is making the forward-looking choice here. The cost is minimal (Argon2id is a single pip dependency) and the security benefit is real.

**4. Rate limiting ships with login, not three milestones later (S-005, D2.4).** V1 puts rate limiting in M2 alongside the login endpoint. V2 delays it to M3. The diff-analysis correctly tags S-005 as L3 severity (state-mechanics): between M2's login ship and M3's rate limiter, V2 has a window where the login endpoint is unprotected against brute force. V1 has no such gap. This is a legitimate security concern.

**5. Operational maturity deliverables (U-001 through U-005).** V1 includes chaos engineering (kill Redis primary, kill API replica, partition DB read-replica -- U-001), a DR runbook with RTO 1hr/RPO 5min targets plus tabletop exercise (U-002), a key rotation drill (U-003), an external pentest engagement via Cobalt (U-004), and an IR playbook with a 72-hour GDPR notification timeline (U-005). These are real operational deliverables that production systems need. V2 omits all of them.

**6. Key separation for 2FA secrets (C-009, D3.3).** V1 encrypts TOTP secrets with a KMS key *distinct* from the column-encryption key used for PII. This is defense-in-depth: if the column-encryption key is compromised, TOTP secrets remain protected. V2 says "stored encrypted in user_2fa table" without specifying key separation. V1's approach is the correct security posture for secrets that are themselves authentication factors.

V1 is the stronger document on security depth and operational readiness. I acknowledge this without reservation.

---

## Strengths Claimed (Variant 2)

### 1. Combined registration + login in M1 delivers value faster (S-003)

V2 places both registration (`POST /auth/register`, D1.2) and login (`POST /auth/login`, D1.3) in M1, alongside JWT issuance (D1.3), refresh rotation (D1.4), and logout (D1.5). By the end of M1 (4 weeks), a user can register, verify email, log in, refresh tokens, and log out. That is a complete authentication loop.

V1 splits registration into M1 and login into M2, meaning a minimum of 6 weeks (M1: 3 weeks + M2: 3 weeks) before anyone can actually log in. The registration endpoint alone has zero user-facing value -- you can create accounts but cannot authenticate with them. V2's M1 is a more useful milestone boundary because it ships a *working system*, not a substrate.

Evidence: V2 M1 acceptance criteria (line 53-61) test the full registration-to-login-to-refresh-to-logout cycle in a single milestone. V1 M1 acceptance criteria (line 75-81) test only registration, email verification, and encryption -- no login, no JWT, no sessions.

### 2. Tamper-proof audit at the database role level (U-014)

V2's D3.9 specifies: "The `audit_events` table has no UPDATE/DELETE grants for the application role -- only INSERT and SELECT" (line 142, acceptance criterion line 158). This is a database-level constraint, not application logic. Even a compromised application server with full database credentials cannot alter or delete audit history.

V1's audit approach (D1.5) uses an `AuditLogger` service interface -- an application-layer abstraction. While V1 also mentions an append-only table, the diff-analysis does not credit V1 with an equivalent DB-role restriction. U-014 is listed as V2-only with "High" value. Application-layer immutability can be bypassed by any SQL injection or compromised service account; database-role immutability cannot.

This is not a minor point. For GDPR compliance (NFR-004) and forensic investigation after a breach (R-004), the audit log is the single most critical artifact. V2 protects it at a deeper layer than V1.

### 3. Four-hour soak test vs one-hour (C-018)

V2's D5.3 specifies "10K sessions over 4 hours with zero error-rate increase, measuring Redis memory and PostgreSQL connection pool stability" (line 233). V1's D5.1 specifies "sustained for 1 hour" (line 244).

A one-hour soak test can miss:

- Slow Redis memory leaks that manifest at 2-3 hours
- PostgreSQL connection pool exhaustion under sustained load
- Connection-stale errors from long-lived pooled connections
- Gradual p95 latency degradation from index bloat under write volume

Four hours is not arbitrary overkill -- it is the minimum duration where these classes of bugs become observable. The cost difference is negligible (3 additional hours of compute time in staging), but the signal quality is materially higher.

### 4. Simpler RBAC model matches the spec's actual requirements (C-004, X-004)

The source spec requires "role-based access control" (FR-004). It does not require a dynamic resource:action permission matrix. V2 implements four static roles (viewer, editor, admin, superadmin) with a middleware check against the JWT `roles` claim (D3.2). This is:

- **Auditable:** The permission mapping is a single configuration artifact, not a runtime database lookup.
- **Testable:** Every role-permission combination can be enumerated in a finite test matrix.
- **Sufficient:** The spec's NFR-001 p95 budget "doesn't permit a DB lookup per request" -- which is exactly what V1's dynamic permission resolution would require at the RBAC middleware layer, unless V1 denormalizes all permissions into the JWT `perms[]` claim (D4.2). But if you denormalize into the JWT, you have effectively recreated a static role hierarchy with extra steps and a more complex JWT payload.

V1's `resource:action` convention (D4.1) and `permissions` table are forward-looking architecture for a requirements document that does not call for it. The moment the spec actually needs fine-grained permissions, V2's `user_roles` table can be extended with a `permissions` JSONB column (V2 explicitly states this in its "Opinionated Choices" section, point 3, line 407). Premature generalization is not a security feature -- it is schedule risk.

### 5. Explicit `/auth/reactivate` endpoint during grace period (U-013)

V2's D4.6 provides `POST /auth/reactivate` as a distinct endpoint that restores a deactivated account during the 14-day grace period (line 191). This separates *user intent* (the user actively chooses to reactivate) from *passive grace* (the account simply continues to exist until the deadline).

V1's deactivation workflow (D4.6) uses soft-delete with a 30-day window and a scheduled background job that purges after 30 days. There is no explicit reactivation endpoint -- presumably the user can just log in during the grace period. But this conflates "the user changed their mind" with "the user happened to authenticate." An explicit reactivation endpoint provides:

- A clear audit event (`account_reactivated` vs `login_success` on a deactivated account)
- A deliberate user action (confirming they want to restore the account)
- A cleaner API contract for the frontend to build a reactivation flow

### 6. Avatar upload to S3/R2 with signed URLs (U-012)

V2's D4.2 includes `POST /auth/me/avatar` storing to S3/R2 with a signed URL for download (line 187). This is a practical user-profile feature that V1 omits entirely. While avatar upload is not the most security-critical deliverable, it is part of FR-010 (user profile management), and V2's implementation is sound: S3 storage avoids bloating the database, and signed URLs provide time-limited access without a proxy endpoint.

V1's D4.4 covers `GET /users/me` and `PATCH /users/me` for profile updates but does not address file uploads at all. For a production user-profile system, avatar upload is a standard expectation.

### 7. Shorter refresh-token TTL reduces the attack window (C-002, X-002)

V2 uses a 7-day refresh-token TTL (D1.3). V1 uses 30 days (D2.1). The diff-analysis flags this as a High-severity difference.

A 30-day refresh token means that if a refresh token is stolen (via XSS, network interception, or log exposure), the attacker has a 30-day window to generate new access tokens. A 7-day TTL limits this to one week. For an auth system where access tokens are short-lived (15 min) and the refresh token is the long-lived credential, the refresh-token TTL is the single most impactful parameter controlling the blast radius of token theft.

V2's 7-day TTL is the more conservative choice. Users can re-authenticate weekly without significant friction, and the security benefit is a 4x reduction in the stale-token attack window.

### 8. Tabular deliverable format provides superior traceability (S-006)

V2 uses a consistent table format `(ID, Deliverable, Source Coverage)` for every milestone's deliverables (lines 31-41, 85-93, 131-143, 184-193, 232-241). This makes it trivial to trace any deliverable back to its source requirement. V1 uses bulleted narrative per deliverable with inline source references -- more verbose and harder to scan for coverage gaps.

V2 also includes a dedicated FR Coverage Matrix (lines 339-353) and NFR Coverage Matrix (lines 356-365) that map every requirement to specific milestone deliverables. V1 has an equivalent FR/NFR Coverage Matrix (lines 346-365) but it is embedded in the appendix with less visual separation.

### 9. Clearer effort breakdown with day-level estimates

V2 provides day-level effort estimates for each milestone (e.g., M1: "Schema + migrations: 2 days. Registration + email verification: 3 days. Login + JWT: 2 days..." line 72). V1 provides only sprint-level estimates ("3 weeks (1.5 sprints)" with occasional notes about which deliverable is heaviest).

For a team planning sprint capacity, V2's granularity is more actionable. You can see that M1's critical path is registration + email verification (3 days) and that Redis integration (1 day) is a trivial dependency. V1's "3 weeks" for M1 tells you nothing about where the risk is.

### 10. Performance strategy addresses connection pooling and Redis optimization specifically

V2's "Performance" cross-cutting section (lines 302-305) specifies PgBouncer in transaction mode with a 100-connection pool, 20-connection per-instance application pools, Redis pipelining for refresh-token lookups, and Redis Cluster scaling criteria (>10K sessions).

V1's performance section (lines 299-304) mentions async-by-default, PgBouncer, `aioredis` pool sizing, and JWKS cache TTL. Both are competent, but V2 is more specific about when to scale Redis (the ">10K sessions" threshold is a concrete operational trigger).

---

## Weaknesses in Variant 1

### 1. Overengineering the RBAC model for the stated requirements (C-004, X-004)

V1 creates four tables (`roles`, `permissions`, `role_permissions`, `user_roles`) and a `resource:action` permission convention (D4.1). The source spec requires RBAC. It does not require fine-grained permission composition. This is architectural speculation that adds:

- Schema complexity (4 tables vs 1 join table)
- JWT payload bloat (V1 denormalizes permissions into a `perms[]` claim -- D4.2)
- Testing surface (every permission assignment must be tested for every role)
- Migration burden when the permission model changes

V1 justifies this by saying permissions are "denormalized for speed" (D4.2). But if the permissions are baked into the JWT at login time and only refreshed on token refresh, you have the same propagation delay problem that V1 critiques in V2 -- just with a more complex token payload. The dynamic permission matrix buys you nothing that a static role hierarchy does not provide for this spec.

### 2. The bloom-filter denylist adds operational complexity for marginal benefit (C-003, X-003)

V1's Redis bloom filter for access-token revocation (D2.2) requires:

- Measuring and monitoring the false-positive rate (< 0.1% target, line 128)
- Sizing the bloom filter for the expected number of revoked tokens
- Coordinating bloom-filter TTL with access-token TTL
- Testing that false positives do not lock out legitimate users

All of this operational overhead exists to close a 15-minute window where a revoked user retains access. V2's approach -- relying on short TTL + refresh-token revocation -- accepts this 15-minute window and eliminates the bloom-filter operational burden entirely.

For most applications, a 15-minute propagation delay on permission changes is acceptable. Admins performing security-sensitive demotions can additionally revoke the user's refresh tokens (which V2 supports), forcing an immediate re-authentication that picks up the new permissions. V1's bloom filter solves a problem that simpler mechanisms already address.

### 3. M1 ships no user-facing functionality (S-003)

V1's M1 delivers registration, password reset, encryption, and audit scaffolding. But no one can log in. No one can get a JWT. No one can access a protected endpoint. M1 is a 3-week investment in infrastructure with zero demonstrable user value.

From a stakeholder perspective, V2's M1 (4 weeks) delivers the full registration-to-login-to-refresh-to-logout cycle. After 4 weeks, the product team has something to demo, the QA team has something to test end-to-end, and the security team has the complete credential lifecycle to audit. V1's stakeholders wait 6 weeks for the same milestone.

The 2-week time difference is not the primary concern -- it is the *value density* of the milestone boundary. V2's M1 is a vertical slice; V1's M1 is a horizontal layer.

### 4. Missing practical features: avatar upload, explicit reactivation (U-012, U-013)

V1 does not include avatar upload (U-012) or an explicit reactivation endpoint (U-013). Avatar upload is a standard feature of any user-profile system and is implicitly covered by FR-010. The explicit reactivation endpoint provides cleaner audit semantics and a better user experience than V1's implicit "log in during grace period" approach.

These are not edge cases -- they are standard production features that V1 simply omits.

### 5. Feature flags via `unleash` are scope creep (U-010)

V1 includes feature flags via `unleash` for risky rollouts (OAuth, 2FA, hard-delete). This introduces a new infrastructure dependency (an Unleash server) and a new operational concern (flag lifecycle management). The source spec does not call for feature flags. This is a deployment strategy choice that belongs in the CI/CD pipeline design, not in the product roadmap.

### 6. The 14-week timeline is optimistic given the security depth

V1 claims 14 weeks with "one engineer on the critical path" (line 44). But V1's M1 alone requires: Argon2id calibration and benchmarking, KMS integration for column encryption, mTLS setup between API and Redis, `pgcrypto` integration, GDPR data-subject access scaffolding, and STRIDE threat modeling -- all in 3 weeks. The bloom-filter denylist in M2, the TOTP key separation in M3, the permission-change propagation in M4, and the full chaos engineering + external pentest + DR drill in M5 all add non-trivial complexity.

V2's 17-week estimate with its more conservative feature set is likely more honest. V1's 14-week estimate may be achievable for a senior engineer who has built auth systems before and can reuse boilerplate, but it does not account for the inevitable edge cases that V1 itself identifies (OAuth account-linking collisions, refresh-token family rotation, bloom-filter sizing).

---

## Concessions

I must honestly acknowledge V2's genuine weaknesses:

### 1. No chaos engineering (U-001)

V2 does not include chaos engineering drills. V1's D5.2 kills the Redis primary mid-traffic, kills an API replica, and partitions the DB read-replica. This is a legitimate operational readiness validation that V2 omits entirely. V2's soak test (D5.3) validates steady-state performance but does not test failure recovery.

### 2. No DR runbook with RTO/RPO targets (U-002)

V2 includes only a "production deployment runbook" (D5.8). It does not specify RTO/RPO targets, does not require a tabletop exercise, and does not document failover procedures. V1's D5.5 specifies RTO 1 hour, RPO 5 minutes, and requires a signed-off tabletop exercise. This is a significant gap for production readiness.

### 3. No external pentest (U-004, C-015)

V2 relies on OWASP ZAP automated scanning only (D5.4). V1 engages an external pentest vendor (Cobalt) with a 4-week lead time that gates the GA release (D5.4). Automated scanning catches known vulnerability patterns but misses business-logic flaws (e.g., privilege escalation through parameter tampering, IDOR in the admin API). An external human pentest is a qualitatively different validation. V2 should include at least a lightweight external review.

### 4. No key separation for 2FA secrets (C-009)

V2 states TOTP secrets are "stored encrypted in user_2fa table" (D3.4) but does not specify that the encryption key is distinct from the column-encryption key used for PII. V1's D3.3 explicitly uses a separate KMS key. If the PII encryption key is compromised, V2's TOTP secrets are also exposed. V1's approach provides an additional security boundary.

### 5. Audit table delayed to M3 creates an event gap (S-004)

V2 introduces the `audit_events` table in M3 (D3.9), while M1 and M2 events are "captured retroactively" via event emission. This creates a window where M1/M2 events exist in application logs but not in the structured audit table. If a security incident occurs during M1/M2, forensic analysis requires correlating application logs rather than querying the audit table. V1's day-one audit substrate (D1.5) has no such gap.

### 6. Rate limiting delayed to M3 leaves login unprotected (S-005)

V2's login endpoint ships in M1, but rate limiting does not arrive until M3 (D3.7). Between M1 and M3, the login endpoint has no brute-force protection beyond whatever the infrastructure layer provides (e.g., WAF rules, cloud-provider rate limiting). V1 ships rate limiting in M2 alongside login, closing this gap.

### 7. No access-token revocation mechanism (C-003, X-003)

V2 explicitly states "no revocation list needed for access tokens" (line 305). This means that if a user's session is compromised or their roles are changed, the existing access token remains valid for up to 15 minutes. V1's bloom-filter denylist provides immediate revocation. For most applications this is acceptable, but for high-security environments it is a real gap.

### 8. bcrypt is not the forward-looking choice (C-001, X-001)

bcrypt-12 is adequate today but Argon2id is the OWASP 2025 recommendation specifically because it resists GPU-based attacks more effectively. V2 should adopt Argon2id -- the migration cost from bcrypt to Argon2id later is non-trivial (every password hash must be upgraded on next login), while adopting Argon2id now costs nothing but a dependency choice.

### 9. Recovery code hashing algorithm unspecified (C-010)

V2 says backup codes are "hashed and stored, each usable once" (D3.6) but does not name the hashing algorithm. V1 specifies bcrypt-12 (D3.5) and justifies why Argon2id is overkill for short high-entropy strings. V2 should specify the algorithm.

---

## Shared Assumption Responses

### A-001: Single-region, single-AZ-resilient deployment is acceptable

**ACCEPT.** Both variants target 99.9% uptime (NFR-005) via failover within a single region/AZ. Multi-region active-active would fundamentally change the architecture (cross-region Redis replication, JWT key distribution, audit-log ordering) and is not required by the spec. V2's approach is consistent with this constraint: PgBouncer for DB failover, Redis persistence (AOF), and health-check-based routing.

### A-002: Regulatory scope is GDPR + OWASP only

**QUALIFY.** The spec explicitly scopes to GDPR and OWASP, and both variants honor this. However, V2's "Out of Scope" section (lines 371-382) more clearly documents this boundary and explicitly notes that SAML integration for enterprise customers is a "potential M6 if demand emerges." This forward-reference is useful because enterprises frequently require SAML, and having a documented extension point prevents scope creep during implementation. The assumption should be accepted for this roadmap but revisited before v1.1 planning.

### A-003: Web/REST-only API surface; no GraphQL, gRPC, or native mobile SDK

**ACCEPT.** V2 explicitly states "no native SDK is built" and that "the API is designed to be mobile-friendly but no native SDK is built" (line 381). The REST API boundary is sufficient for the stated requirements, and both variants use REST exclusively. Adding GraphQL or gRPC would change the authentication middleware layer significantly and is out of scope.

### A-004: A single team can absorb the entire 14- or 17-week critical path

**QUALIFY.** V1 mentions "one engineer on the critical path" (line 44) and suggests parallelizing with a second engineer for M3+M4. V2 is silent on staffing but provides day-level effort estimates that make the workload transparent. V2's 17-week estimate is more realistic for a small team, and its M1 (4 weeks, 16 person-days of detailed breakdown) is more achievable than V1's M1 (3 weeks covering Argon2id calibration, KMS integration, mTLS, pgcrypto, GDPR scaffolding, and STRIDE threat modeling). The assumption should be accepted *for V2's timeline* but is questionable for V1's compressed 14-week estimate given V1's heavier feature set.

### A-005: p95 < 200ms measurement boundary is undefined

**ACCEPT with caveat.** Neither variant defines exactly where the p95 timer starts and stops. V2 at least establishes a local baseline in M1 ("Response time for `/auth/login` and `/auth/register` measured at < 200ms p95 locally" -- line 60) and re-validates in M5 under load (D5.2). V1 uses `pytest-benchmark` in CI (D2.7) and `siege` for load testing (M2 acceptance, line 125). Both measure at the auth-service edge, which is the most common interpretation. The assumption should be accepted but the measurement boundary should be explicitly defined before M5 validation begins.

---

## Closing Argument

Variant 2 wins on three axes: **execution pragmatism**, **honesty of scope**, and **operational traceability**.

On execution pragmatism: V2's M1 ships a working auth loop in 4 weeks. V2 uses a static RBAC model that matches the spec. V2 uses a 7-day refresh TTL that minimizes the attack window without bloom-filter operational overhead. Every complexity V2 avoids is a complexity the team does not have to build, test, debug, and operate.

On honesty of scope: V2's 17-week estimate accounts for the actual work. V2's "Out of Scope" section explicitly lists biometric auth, hardware keys, SSO, multi-tenancy, WebSocket revocation, i18n, and mobile SDK. V2 does not include feature flags, chaos engineering, or external pentests -- and I have conceded that some of these are real gaps. But the spec does not require them, and a roadmap that delivers what the spec asks for is more trustworthy than one that gold-plates.

On operational traceability: V2's tabular deliverable format, FR/NFR coverage matrices, day-level effort estimates, and database-role-level audit protection (U-014) make the roadmap easier to track, easier to verify, and harder to tamper with after the fact.

V1 is the stronger document for a mature organization with dedicated security and SRE teams. V2 is the stronger document for a team that needs to ship working auth, on time, with clear accountability for every deliverable.
