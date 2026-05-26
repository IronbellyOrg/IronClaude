# Diff Analysis: User Authentication System Roadmap

> **Timestamp**: 2026-05-22T00:00:00Z
> **Variants compared**: 2 (opus-default, sonnet-default)
> **Total diff count**: 55
> **Counts per category**: S:12  C:18  X:7  U:13  A:5

---

## Structural Differences

| # | Area | Variant 1 (opus) | Variant 2 (sonnet) | Severity |
|---|------|-------------------|---------------------|----------|
| S-001 | Milestone count and range | 10 milestones (M0–M9) | 12 milestones (M1–M12) | Medium |
| S-002 | Pre-implementation foundation milestone | Dedicated M0 "Foundations & Threat Model" (2 weeks): STRIDE threat model, ADRs, Vault, CI/CD skeleton | No equivalent; infrastructure bootstrap in M1 (5 days), no threat model deliverable | High |
| S-003 | Deliverable format | Narrative bullet points with inline rationale (e.g., D-M0.1 describes distroless base, non-root UID) | Structured tables: ID / Deliverable / Acceptance Criteria columns for every deliverable | Low |
| S-004 | H2 section count / organizational model | 17 H2 sections including dedicated "Architectural Philosophy," "Implicit Prerequisites Surfaced," "Risks Created by This Roadmap (Meta-Risks)" | 9 H2 sections; flatter hierarchy with "Milestone Detail" as single H2 containing all milestones as H3 | Medium |
| S-004 | Technology Decisions section | No dedicated section; tech choices embedded in ADR-004 (framework) and individual deliverables | Dedicated "Technology Decisions & Rationale" table (10 rows covering hashing, JWT algo, session store, PII encryption, rate limiting, 2FA, audit storage, email, deployment, migrations) | Low |
| S-006 | Blast Radius Analysis section | No equivalent section | Dedicated section with 6 design-choice justifications (token storage isolation, Redis as cache not authority, OAuth additivity, append-only audit, rate limiter isolation, KMS key separation) | Medium |
| S-007 | RBAC-to-OAuth dependency edge | Explicit hard constraint: M4 (RBAC) before M5 (OAuth) with rationale—"OAuth identity to role mapping has nowhere to land otherwise" | M4 (OAuth) and M5 (RBAC) are parallel branches after M3; no dependency edge between them | High |
| S-008 | Meta-risks section | "Risks Created by This Roadmap" table: M0 scope creep, M6 bundle size, late blockers, provider API changes | No equivalent | Low |
| S-009 | Parallelization detail | Narrative: "M4 can begin midway through M3," "M5 waits on M4 but scaffolding can be prototyped" | Week-by-week table assigning tasks to Backend A, Backend B, and Frontend/DevOps roles across 11 weeks | Medium |
| S-010 | Post-launch ongoing verification | Not covered (roadmap ends at M9 production cutover) | "Ongoing Verification (Post-Launch)" subsection: daily smoke, weekly ZAP, monthly load test, quarterly external pentest, annual GDPR audit | Medium |
| S-011 | Critical path representation | Single ASCII diagram + narrative (~17 weeks) | ASCII diagram + explicit critical-path math (44 days) + week-by-week parallelization schedule showing wall-clock (10-11 weeks) | Low |
| S-012 | Traceability matrix scope | FR table, NFR table, Risks table, Dependencies table, Success Criteria table — five separate sub-tables | FR table, NFR table, Risk Mitigations table, Success Criteria table — four sub-tables; no separate Dependencies table (deps embedded in milestone detail) | Low |

---

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|---------------------|---------------------|----------|
| C-001 | Account lockout threshold | 10 failed login attempts per email in 15 min -> 15 min lockout (D-M6.3, line ~313); also 50 failed per IP in 1h -> 1h IP block | 5 failures in 15 min -> lockout; auto-unlocks after 30 min (D-M3.9, line ~237) | High |
| C-002 | Refresh token TTL | 30 days (D-M2.4, line ~141: "opaque refresh token (30d)") | 7 days (D-M3.4, line ~232: "refresh token (7d TTL)") | High |
| C-003 | Password strength enforcement | zxcvbn score >=3, minimum length 12, HIBP k-anonymity check against top-1M breached passwords (D-M2.1, line ~127) | Rule-based: >=12 chars, mixed case, digit, symbol (D-M3.1, line ~229); password history: cannot reuse last 5 passwords (D-M7.5, line ~361) | Medium |
| C-004 | Audit log retention period | 7 years — "financial-services bar; covers most compliance regimes including GDPR's reasonable retention" (D-M6.4, line ~323) | 2 years configurable (D-M8.5, line ~414) | High |
| C-005 | GDPR erasure mechanism | Cryptographic erasure: rotate column-encryption DEK so historical ciphertext is undecryptable; PII pseudonymized to `deleted-{uuid}@deleted.invalid` (D-M4.4, line ~228-229) | Anonymization: replace PII with `anonymized_<uuid>`; retain audit events with nullified actor_id; schedule hard deletion after 30 days (D-M8.4, line ~413) | High |
| C-006 | Secrets management | HashiCorp Vault dev mode locally; AWS Secrets Manager reference architecture for staging/prod; pepper stored in Vault applied as HMAC pre-hash (D-M0.2, line ~47; D-M1.3, line ~97) | 12-factor environment variable loading; KMS envelope encryption for PII; no Vault mention (D-M1.3, line ~94; D-M2.3, line ~200) | Medium |
| C-007 | Audit tamper evidence | Hash chain: each event includes hash of previous event_id+payload; daily Merkle root anchored to immutable log (D-M6.4, line ~322) | No tamper-evidence mechanism; audit is append-only with no UPDATE/DELETE permissions for app user (Blast Radius Analysis item 4, line ~717) | Medium |
| C-008 | Rate limiting algorithm | Token-bucket in Redis with atomic Lua script; burst allowance 2x for 10s (D-M6.2, line ~305-306) | Sliding-window backed by Redis sorted sets (D-M6.5, line ~326) | Low |
| C-009 | RBAC cache invalidation | Redis pub/sub: "Permission changes invalidate cache immediately via Redis pub/sub" (D-M4.2, line ~220) | TTL-based 5-min cache in Redis; exit criteria says "cache invalidation works within one request cycle" (D-M5.2, line ~295) | Medium |
| C-010 | Provider health check interval | Every 60s (D-M5.5, line ~269) | Every 5 minutes (D-M4.5, line ~267: "Periodic (5min) check") | Low |
| C-011 | GDPR export HTTP method | `GET /api/v1/users/me/data-export` (D-M8.3, line ~420) | `POST /auth/gdpr/export` (D-M8.3, line ~413) | Low |
| C-012 | Admin role taxonomy | `user`, `admin`, `support`, `auditor` (read-only audit log access) (D-M4.1, line ~214) | `admin` (all permissions), `moderator` (users:read, users:suspend), `user` (self:read, self:write) (D-M5.1, line ~293) | Medium |
| C-013 | JWT storage delivery | HTTP-only Secure SameSite=Strict cookies only; no mention of Bearer header alternative (D-M2.4, line ~141) | HTTP-only Secure SameSite=Strict cookie (`__Host-auth-token`) as default; API clients can opt into `Authorization: Bearer` header via `Accept: application/json` (D-M6.7, line ~328) | Medium |
| C-014 | Admin impersonation | Listed as dashboard action: "impersonate (with full audit trail and time-limited 1h impersonation tokens)" (D-M7.1, line ~353) | Not mentioned | Medium |
| C-015 | Chaos / resilience testing | Dedicated deliverable D-M8.5: kill PostgreSQL replica, kill Redis node, SendGrid 503 injection (line ~428-430) | No explicit chaos testing | Medium |
| C-016 | Password hash benchmark target | "<300ms p95" (D-M1 exit criteria, line ~107; D-M2.4, line ~155) | "<500ms on target hardware" (D-M3.2, line ~230) | Low |
| C-017 | Backup tooling | pgBackRest with WAL archiving, RPO 1min, quarterly restore drill (D-M7.6, line ~376) | Daily pg_dump + PITR WAL archiving; restore test on staging (D-M12.5, line ~531) | Medium |
| C-018 | Security alert emails | Dedicated deliverable D-M6.5: triggered on new-device login, password change, 2FA disabled, multiple failed logins; includes "wasn't me" link (line ~325-326) | Mentioned as part of email template system (D-M3.6: "verification, password reset, 2FA codes") but no dedicated security-alert mechanism | Low |

---

## Contradictions

| # | Claim A | Claim B | Nature | Severity |
|---|---------|---------|--------|----------|
| X-001 | **V1 internal**: "2FA (FR-007) precedes OAuth" because "TOTP is a self-contained crypto primitive while OAuth has external-provider blast-radius risk" (Architectural Philosophy, line ~11) | **V1 internal**: M5 = OAuth (line ~24), M6 = 2FA (line ~25). Soft sequencing note acknowledges: "chosen sequence puts OAuth first because it unblocks more user-facing demos" (line ~563). The milestone ordering directly contradicts the philosophical claim. | Intra-variant: philosophy vs. milestone ordering | Medium |
| X-002 | **V2 internal**: "Total estimated duration: ~77 days on the critical path" (Milestone Summary, line ~24) | **V2 internal**: Critical path calculation = M1->M2->M3->M6->M8->M11->M12 = 5+5+10+8+6+5+5 = **44 days** (Sequencing section, line ~628). 77 days is the sum of ALL milestones, not the critical path. | Intra-variant: summary contradicts own calculation | High |
| X-003 | **V2 internal**: "Realistic wall-clock with parallelization: 8-9 weeks for a 3-person team" (Milestone Summary, line ~24) | **V2 internal**: Parallelization schedule shows "~10-11 weeks with parallelization" (line ~647). The summary claims 8-9 weeks but the detailed schedule shows 10-11. | Intra-variant: summary understates own schedule | Medium |
| X-004 | **V1**: Account lockout after **10** failed attempts in 15 min, then **15 min** lockout (D-M6.3) | **V2**: Account lockout after **5** failed attempts in 15 min, then **30 min** lockout (D-M3.9). These are opposing thresholds for the same brute-force defense. | Cross-variant: conflicting security parameter | High |
| X-005 | **V1**: Refresh token TTL = **30 days** (D-M2.4) | **V2**: Refresh token TTL = **7 days** (D-M3.4). 30-day tokens have significantly longer theft windows than 7-day tokens. | Cross-variant: conflicting security parameter | High |
| X-006 | **V1**: Audit retention = **7 years** with hash-chain tamper evidence (D-M6.4) | **V2**: Audit retention = **2 years** configurable, no tamper evidence (D-M8.5). These target fundamentally different compliance tiers. | Cross-variant: conflicting compliance scope | High |
| X-007 | **V1**: GDPR erasure via cryptographic erasure — rotate DEK so all ciphertext becomes undecryptable (D-M4.4) | **V2**: GDPR erasure via anonymization — replace PII with placeholder text, retain data structure (D-M8.4). Cryptographic erasure destroys data; anonymization preserves structure. These are opposing data-elimination strategies. | Cross-variant: conflicting erasure approach | High |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | V1 | **M0 Foundations & Threat Model**: STRIDE threat model, Architecture Decision Records (4 ADRs), Vault integration, CI/CD skeleton — all before any auth code. Establishes security posture at day zero. | High |
| U-002 | V1 | **Hash-chain + Merkle root tamper-evident audit trail**: Each event chains to previous via hash; daily Merkle root anchored to immutable log. Enables forensic detection of audit-log tampering. | High |
| U-003 | V1 | **Cryptographic erasure for GDPR (DEK rotation)**: Rotating the column-encryption key renders all historical PII ciphertext undecryptable without deleting the audit log rows. Novel approach that satisfies both GDPR erasure and audit-integrity retention. | High |
| U-004 | V1 | **HMAC pepper from Vault for password hashing**: Pepper applied pre-hash and stored in Vault, not the database. Adds a secret layer beyond the per-user salt. | Medium |
| U-005 | V1 | **Admin impersonation feature**: Time-limited 1h impersonation tokens with full audit trail. Useful for support but introduces privilege-escalation risk. | Medium |
| U-006 | V1 | **DPIA (Data Protection Impact Assessment) deliverable**: Required under GDPR Article 35 for high-risk processing. V2 omits this entirely. | Medium |
| U-007 | V1 | **Chaos / resilience testing**: Dedicated deliverable (D-M8.5) killing PostgreSQL replicas, Redis nodes, and injecting SendGrid 503s to verify graceful degradation. | Medium |
| U-008 | V1 | **zxcvbn + HIBP k-anonymity password checking**: Probabilistic password-strength scoring plus real-world breach-database lookup. More sophisticated than character-class rules. | Medium |
| U-009 | V1 | **SRE error budgets and burn-rate alerts**: Google SRE multi-window multi-burn-rate pattern for SLO tracking. 43.8 min/month error budget calculated from 99.9% SLO. | Medium |
| U-010 | V2 | **Blast Radius Analysis section**: 6 named design choices that limit failure impact (token storage isolation, Redis as cache not authority, OAuth additivity, append-only audit, rate limiter isolation, KMS key separation). Makes architectural trade-offs explicit. | High |
| U-011 | V2 | **CSRF protection via double-submit cookie pattern**: Dedicated deliverable (D-M6.8) with `__Host-csrf-token` cookie + matching header validation on state-changing requests. V1 mentions SameSite=Strict as CSRF mitigation but has no dedicated CSRF deliverable. | Medium |
| U-012 | V2 | **Password history enforcement**: Cannot reuse last 5 passwords (D-M7.5). V1 has no password-history check. | Medium |
| U-013 | V2 | **Pre-launch verification checklist**: 15-item structured checklist with checkboxes covering auth smoke test, OAuth E2E, load test baseline, OWASP scan, GDPR export/delete, monitoring, alerting, backup restore, rollback, rate limiting, lockout, token theft detection, CSP, PII encryption. | Medium |

---

## Shared Assumptions

| # | Assumption | Source Agreement | Impact if Violated | Status |
|---|-----------|-----------------|-------------------|--------|
| A-001 | **PostgreSQL 15+ is the relational data store** and will not change to MySQL, DynamoDB, or another engine. Both roadmaps design schemas, partitioning, and queries specific to PostgreSQL features (CITEXT, RANGE partitioning, UUID v7, JSONB, INET types). | Both agree (V1 line ~80; V2 line ~108) | All schema designs, migration scripts, and query-optimization strategies would need rewriting. | UNSTATED |
| A-002 | **SendGrid is the transactional email provider** and will remain available at required volumes. Both design email templates, circuit breakers, and webhook integrations specifically for SendGrid. | Both agree (V1 D-M2.3; V2 D-M1.7) | Email verification, password reset, security alerts, and 2FA codes all depend on email delivery. Switching providers requires template migration and integration rewrite. | STATED (in dependency tables) |
| A-003 | **The system is greenfield with no legacy auth system** to migrate from. Neither roadmap accounts for data migration, user import, backward-compatible token formats, or coexistence with an existing auth provider. | Both implicitly agree (neither mentions migration) | If a legacy system exists, both roadmaps need additional migration milestones, dual-write periods, and user-communication plans not accounted for in the schedule. | UNSTATED |
| A-004 | **The team has security-review authority available** (security lead for V1 sign-offs, someone qualified to run OWASP ZAP and review pentest findings for V2). Both require sign-offs that presuppose existing security expertise on the team or accessible externally. | Both agree (V1: "reviewed by >=2 engineers," "security lead sign-off"; V2: "sign-off from security lead") | If the team lacks security expertise, M0 threat model (V1), M11 security audit (V2), and all OWASP-compliance gates cannot be completed on schedule. | UNSTATED |
| A-005 | **Redis is acceptable for session storage and rate limiting** despite its volatility. Both assume Redis persistence (AOF) is sufficient for session durability, and both treat Redis as a cache that can fail without catastrophic auth failure. | Both agree (V1: "Redis failure degrades to 'no new logins'"; V2: "Redis as session cache, not session authority") | If the organization mandates database-only session storage (no Redis), both roadmaps require significant re-architecture of session management and rate-limiting subsystems. | STATED (in exit criteria / blast radius) |

---

## Summary

**Totals**: S:12  C:18  X:7  U:13  A:5 = **55 diff points**

### Highest-Severity Items

**Structural (High):**

- S-002: V1 dedicates a full 2-week M0 to threat modeling, ADRs, and secrets infrastructure; V2 has no equivalent.
- S-007: V1 enforces RBAC-before-OAuth as a hard constraint; V2 runs them in parallel, creating a potential authorization vacuum.

**Content (High):**

- C-001: Account lockout thresholds diverge by 2x (10 vs. 5 failures) and lockout duration by 2x (15 vs. 30 min).
- C-005: GDPR erasure strategies are fundamentally different — cryptographic key destruction vs. field anonymization.

**Contradictions (High):**

- X-002: V2 summary claims 77-day critical path; own calculation shows 44 days.
- X-004: Account lockout: 10 failures/15min lockout (V1) vs. 5 failures/30min lockout (V2).
- X-005: Refresh token TTL: 30 days (V1) vs. 7 days (V2) — a 4x security-posture difference.
- X-006: Audit retention: 7 years (V1) vs. 2 years (V2) — different compliance tiers entirely.
- X-007: Erasure approach: cryptographic destruction (V1) vs. anonymization (V2) — opposing data-elimination strategies.

**Unique Contributions (High):**

- U-001: V1's M0 threat-model/ADR foundation.
- U-002: V1's hash-chain tamper-evident audit trail.
- U-003: V1's cryptographic erasure via DEK rotation.
- U-010: V2's Blast Radius Analysis making failure-isolation trade-offs explicit.
