# Diff Analysis: Roadmap Comparison

## Metadata

- Generated: 2026-05-22T20:04Z
- Variants compared: 2 (variant-1-opus-default, variant-2-sonnet-default)
- Source spec: tests/sc-roadmap/fixtures/sample_spec.md (62 lines, FR-001..FR-012, NFR-001..NFR-006, R-001..R-004)
- Depth: standard
- Total differences found: 30 (S: 3, C: 13, X: 5, U: 9, A: 8)
- Mode B agents: opus (default), sonnet (default) — neither persona-specified

## Variant Metadata

| Variant | File | Lines | Words | H2 sections | Milestones | Total weeks | Risks | Open Qs |
|---------|------|------:|------:|------------:|-----------:|------------:|------:|--------:|
| V1 (opus) | variant-1-opus-default.md | 262 | 2785 | 9 | 7 | 22 | 12 | 12 |
| V2 (sonnet) | variant-2-sonnet-default.md | 261 | 3669 | 9 | 7 | 18 | 8 | 10 |

## Structural Differences

| # | Area | Variant 1 (opus) | Variant 2 (sonnet) | Severity |
|---|------|------------------|---------------------|----------|
| S-001 | Milestone separators | Uses `---` horizontal rule between milestones for visual demarcation | No separators; relies on `###` heading only | Low |
| S-002 | Edge-case coverage placement | Distributed per-milestone via `**Edge Cases Covered**` blocks inside M2, M3, M5 | Centralized in M7 D7.1 as one explicit edge-case validation test suite | Medium |
| S-003 | Goals table grouping | Single goals table grouped by G1..G7 with one row per goal (semantic axes) | Single goals table with one row per scope-area (mixes goals and metrics) | Low |

All H2 sections appear in the same order: Executive Summary → Goals → Milestones → Dependency Graph → Risk Register → Open Questions → Out of Scope → Success Criteria. Hierarchy depth identical at 3 levels (H1/H2/H3). Heading-level gaps: zero in both variants.

## Content Differences

| # | Topic | Variant 1 (opus) Approach | Variant 2 (sonnet) Approach | Severity |
|---|-------|---------------------------|------------------------------|----------|
| C-001 | Total delivery duration | 22 weeks (7 milestones, weeks 1-22) | 18 weeks (7 milestones, weeks 1-18) | High |
| C-002 | Milestone sequencing | M1 Foundation → M2 Core Identity → **M3 Sessions+RateLimiting → M4 OAuth → M5 RBAC+2FA → M6 Reset+Profile+Audit → M7 Admin+Hardening+Launch** | M1 Foundation+CoreAuth → M2 Tokens → **M3 OAuth → M4 RBAC+RateLimiting+Security → M5 Reset+2FA+Profile+Lifecycle → M6 Audit+Dashboard+Compliance → M7 Production Hardening** | High |
| C-003 | RBAC role taxonomy | 4 seed roles: `admin`, `user`, `auditor`, `support` (operational/duty-based) | 4 seed roles: `admin`, `editor`, `viewer`, `unverified` (CRUD-capability + verification-state) | Medium |
| C-004 | Latency percentile for NFR-001 | p95 < 200ms (looser; tolerates a long tail) | p99 < 200ms (stricter; 1-in-100 worst-case bounded) | Medium |
| C-005 | Concurrent session policy | 10K aggregate concurrency target; no per-user session cap | 10K aggregate AND per-user default cap of 5 sessions, oldest-eviction on overflow | Medium |
| C-006 | Audit tamper-evidence | Hash-chain rows (each row contains SHA-256 of prior row's canonicalized payload) + daily S3 export with object-lock | Append-only PG table with sync write + async fan-out to read replica; no cryptographic chain or external lock | High |
| C-007 | Password policy source | zxcvbn strength check + Argon2id (mem 64MB, par 2) + last-5 history check + HIBP k-anonymity at register/reset | 12-char minimum, mixed case, digit, symbol + Argon2id (params unspecified) | Medium |
| C-008 | JWT signature algorithm | RS256 (asymmetric) with JWKS endpoint `/.well-known/jwks.json` + key rotation runbook | Algorithm unspecified; "JWT" generic; multi-key support mentioned in R-007 mitigation | Medium |
| C-009 | Email verification token | HS256 24h TTL signed token (separate from access JWT) | JWT 24h TTL (no algorithm specified) | Low |
| C-010 | Production deployment topology | Multi-AZ ≥2 AZs, RDS multi-AZ, Redis replication group, chaos test for AZ kill (<30s RTO) | Kubernetes (3-10 HPA pods, CPU 70% target), PgBouncer connection pool, Redis Sentinel for HA | High |
| C-011 | Refresh-token reuse detection | Family-tracking model: rotation creates token family; reuse of any family member invalidates the entire family + alerts user | Reuse detection at single-token granularity: reuse triggers revocation of all sessions for the user | Medium |
| C-012 | Tech-stack decision | Deferred: Node.js 20 LTS **or** Python 3.12 — pushed to Open Q #1 for team decision | Decided: Python 3.12-slim base image specified in D1.3 | Medium |
| C-013 | GDPR deletion ↔ audit retention conflict | Explicitly modeled: tokenize `user_id` in audit table, crypto-shred PII fields at erasure while audit references survive; legal sign-off gated in D7.8 (R-010) | Implicitly handled: 30-day grace, then hard delete that "removes PII, retains anonymized audit records" — but the de-anonymization vector via audit `actor_user_id` indexing is not addressed | High |

## Contradictions

| # | Point of Conflict | Variant 1 (opus) Position | Variant 2 (sonnet) Position | Impact |
|---|-------------------|---------------------------|------------------------------|--------|
| X-001 | NFR-001 latency percentile interpretation | Commits to **p95 < 200ms** as the target metric across `/login`, `/register`, `/refresh`, `/oauth/*` (Goals G1, M2 exit, M3 exit) | Commits to **p99 < 200ms** for `/auth/login`, `/auth/refresh`, `/auth/profile` (Goals row 9, M6 D6.6 exit) | High — Spec wording "< 200ms" is ambiguous; a system that passes p95 may fail p99. Must be resolved before contracts/SLOs are signed |
| X-002 | RBAC role naming and semantics | Seeded roles `admin / user / auditor / support` represent functional duties (auditor reads audit log, support assists users) | Seeded roles `admin / editor / viewer / unverified` represent capability tiers (editor=write, viewer=read, unverified=pre-email-verification) | Medium — Both claim to satisfy FR-004; both are valid RBAC models; the chosen taxonomy is a product/UX decision but the two cannot coexist as defaults |
| X-003 | Total project duration | 22 weeks (M1=2 + M2=3 + M3=2 + M4=3 + M5=4 + M6=3 + M7=5) | 18 weeks (M1=3 + M2=2 + M3=2 + M4=3 + M5=3 + M6=3 + M7=2) | High — A 4-week delta is ~22% of V2's schedule; resource planning, headcount, and dependency commitments differ materially. Cannot both be the plan |
| X-004 | What lives inside M1 | M1 = Foundation **only** (infrastructure, schema, CI/CD, observability — no auth code shipped) | M1 = Foundation **and** core auth (registration + login + email verification + JWT issuance all delivered in M1) | High — V1 reserves M1 as pure scaffolding so M2 starts on a hardened base; V2 ships user-facing flows in M1 to demo value sooner. Risk profile and review gates differ |
| X-005 | Rate-limit / brute-force milestone | Lives in M3 (Weeks 6-7) — sessions and rate limiting bundled because both rely on Redis sliding-window infrastructure | Lives in M4 (Weeks 8-10) — bundled with RBAC and security headers because the team treats it as a security-hardening concern | Medium — Both are defensible groupings but they imply different team specialization (V1: distributed-systems engineer; V2: security engineer). Affects who is on the critical path |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|-------------------|
| U-001 | V1 | Hash-chain audit log (SHA-256 of prior row's canonicalized payload) + daily S3 export with object-lock for tamper evidence (D6.5) | High — Adds cryptographic forensic guarantee. Audit integrity is a Critical-impact compliance control (R-004); V2's append-only table is insufficient against privileged-insider tampering |
| U-002 | V1 | Explicit JWT signing-key compromise risk (R-005) with quarterly rotation runbook (D7.7), JWKS `kid` zero-downtime rotation, 15-min access-TTL bounds blast radius | High — V2's R-007 references rotation but lacks the JWKS + kid mechanism and the blast-radius reasoning |
| U-003 | V1 | Email provider failover plan: secondary SMTP (AWS SES) configured as SendGrid failover, with degraded-mode SLA documented (R-006) | Medium — V2's mitigation is queue + retry on a single provider; V1's plan tolerates full provider outage |
| U-004 | V1 | Crypto-shred on PII deletion (D7.3) + tokenize `user_id` in audit table so audit references survive GDPR erasure (R-010) | High — Resolves the GDPR-vs-audit-retention conflict explicitly; V2 has the conflict but doesn't model the resolution |
| U-005 | V1 | First-user / empty-database bootstrap path (M2 edge cases: bootstrap admin script in D2.7) | Medium — V2 covers "empty database" in D7.1 edge tests but doesn't ship a bootstrap path; cold-start admin creation is a real operational gap |
| U-006 | V2 | Per-user concurrent session cap (default 5) with oldest-eviction on overflow (D2.5) | Medium — Limits credential-stuffing harvest size and unbounded session sprawl; V1 has no per-user cap |
| U-007 | V2 | Kubernetes deployment specifics: HPA min 3 / max 10 / CPU 70%, PgBouncer for connection pooling, Redis Sentinel for HA, k8s manifests (D7.4) | High — V1 says "multi-AZ" but does not specify the orchestrator; V2's k8s + PgBouncer combination is materially more shippable as a runbook |
| U-008 | V2 | Refresh-token race-condition handling: Redis WATCH/MULTI/EXEC for atomic invalidation + issuance + explicit race-condition test (D7.1, R-008) | High — Concurrent refresh from the same client is a real bug class; V1 mentions "idempotency token" but doesn't specify the atomicity primitive |
| U-009 | V2 | Email-column encryption via pgcrypto (D6.8) — column-level encryption, not just at-rest disk encryption | Medium — V1 relies on RDS at-rest encryption only, which doesn't protect against compromised DB credentials; pgcrypto column encryption adds defense-in-depth for PII (NFR-006, R-004) |

## Shared Assumptions

UNSTATED preconditions surfaced from agreement points and promoted to [SHARED-ASSUMPTION] diff points:

| # | Assumption | Source Agreement | Classification | Status |
|---|------------|------------------|----------------|--------|
| A-001 | The frontend and the API share a registrable domain (required for SameSite=Strict refresh cookies to be sent on cross-page navigation) — i.e., browser is the primary client | Both variants use HTTP-only + SameSite=Strict cookie for refresh token | UNSTATED | Promoted — debate must determine whether native mobile / SPA on separate origin is supported |
| A-002 | Email is the canonical user identifier; no username field is exposed | Both variants treat `email` as unique key for accounts and never reference a username | UNSTATED | Promoted — debate must determine if username login is needed or explicitly deferred |
| A-003 | Synchronous audit writes are acceptable at 10K-concurrent-session scale | Both variants emit audit events synchronously from auth endpoints, on the request hot path | UNSTATED | Promoted — debate must determine whether write amplification (login + refresh + logout = 3+ audit writes per session) keeps p95/p99 within the latency budget |
| A-004 | OAuth callback URIs are stable, public, HTTPS-only endpoints under team's control | Both variants implement OAuth Authorization Code flow but neither addresses callback-URI cert lifecycle or domain validation | UNSTATED | Promoted |
| A-005 | Single-region deployment satisfies NFR-005 99.9% uptime | V1 says "multi-AZ"; V2 says "k8s + Sentinel". Neither addresses region failure or cross-region failover | UNSTATED | Promoted — 99.9% (43min/month) tolerates a regional outage statistically; debate must confirm |
| A-006 | Database migrations are forward-only and zero-downtime-compatible with rolling deploys | Both variants use migration scripts (Flyway/Alembic in V1; `/migrations/` in V2) but neither addresses the schema-compatibility window needed for rolling deploys | UNSTATED | Promoted |
| A-007 | One-time tokens (email verification, password reset) are validated by a one-time-use check before signature/expiry checks | Both variants describe single-use tokens but neither specifies the ordering (token-binding race: if signature verified first then DB-marked, two concurrent uses can both pass) | UNSTATED | Promoted — auto-tagged L3 (state-mechanics) per AC-AD5-3 |
| A-008 | All FR scope can be delivered within a single team's bandwidth in the proposed weeks (no team-size or skill-mix dependencies) | Both variants commit to 18-22-week delivery without modeling team composition, parallelism limits, or contractor needs | UNSTATED | Promoted — debate must determine whether the schedule assumes 1 team, multiple teams, or undefined |

## Taxonomy Auto-Tagging (AD-5)

Diff points auto-tagged per the three-level debate taxonomy:

| ID | Level | Rationale |
|----|-------|-----------|
| S-001 | L1 surface | Formatting / presentation |
| S-002 | L2 structural | Organization of edge-case coverage |
| S-003 | L1 surface | Table layout |
| C-001 | L2 structural | Project timeline / planning |
| C-002 | L2 structural | Milestone organization |
| C-003 | L2 structural | RBAC role / interface design |
| C-004 | L3 state-mechanics | Boundary condition (percentile interpretation = validation rule) |
| C-005 | L3 state-mechanics | State management (session limit = guard condition) |
| C-006 | L3 state-mechanics | Invariant (tamper-evidence chain = cryptographic state invariant) |
| C-007 | L2 structural | Password policy interface |
| C-008 | L2 structural | Crypto algorithm choice |
| C-009 | L1 surface | Token TTL / configuration |
| C-010 | L2 structural | Deployment architecture |
| C-011 | L3 state-mechanics | State transition (token family invalidation) |
| C-012 | L2 structural | Tech-stack decision |
| C-013 | L3 state-mechanics | Invariant (audit-survives-erasure as cryptographic+schema invariant) |
| X-001 | L3 state-mechanics | Validation rule (p95 vs p99 is a boundary condition) |
| X-002 | L2 structural | Interface / role-model design |
| X-003 | L2 structural | Schedule structure |
| X-004 | L2 structural | Milestone scope |
| X-005 | L2 structural | Organization |
| U-001 | L3 state-mechanics | Cryptographic invariant (hash chain) |
| U-002 | L3 state-mechanics | State (key rotation) |
| U-003 | L2 structural | Architecture (failover provider) |
| U-004 | L3 state-mechanics | Invariant (audit references survive PII erasure) |
| U-005 | L3 state-mechanics | State (empty-DB bootstrap) |
| U-006 | L3 state-mechanics | Guard condition (session cap) |
| U-007 | L2 structural | Deployment architecture |
| U-008 | L3 state-mechanics | Concurrency / race condition |
| U-009 | L3 state-mechanics | Boundary (column-level encryption) |
| A-001 | L2 structural | Interface assumption (client model) |
| A-002 | L2 structural | Interface assumption (identifier) |
| A-003 | L3 state-mechanics | State / performance invariant |
| A-004 | L2 structural | Interface |
| A-005 | L3 state-mechanics | Availability boundary |
| A-006 | L3 state-mechanics | Schema state invariant |
| A-007 | L3 state-mechanics | Guard condition + race |
| A-008 | L2 structural | Schedule |

Coverage: L1=3, L2=15, L3=20. All three levels are covered; taxonomy coverage gate will NOT trigger forced rounds.

## Summary

- Total structural differences: 3
- Total content differences: 13
- Total contradictions: 5 (3 High, 2 Medium)
- Total unique contributions: 9 (5 V1, 4 V2)
- Total shared assumptions surfaced: 8 (UNSTATED: 8, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-006, C-010, C-013, X-001, X-003, X-004, U-001, U-002, U-004, U-007, U-008
- Similarity: differences > 10% threshold — debate proceeds (NOT short-circuited)
