---
total_diff_points: 18
shared_assumptions_count: 15
---

# Roadmap Variant Diff Analysis

## Shared Assumptions and Agreements

Both variants converge on the core architecture and compliance posture:

1. Stateless JWT access tokens (RS256, 2048-bit RSA, 15-min TTL) paired with opaque refresh tokens hashed at rest in Redis (7-day TTL).
2. bcrypt cost factor 12 via a `PasswordHasher` abstraction; reject argon2id/scrypt for v1.0.
3. Self-hosted `AuthService`; reject Auth0/Firebase for vendor-lock reasons.
4. URL-versioned REST API (`/v1/auth/*`) with unified error envelope `{error:{code,message,status}}`.
5. Audit-log retention resolved to **12 months** (both apply the precedence rule: compliance authority overrides TDD §7.2's 90-day default).
6. 5-milestone structure culminating in staged rollout (Alpha → 10% Beta → 100% GA) gated by `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` flags.
7. GA target date preserved at 2026-06-09.
8. Account lockout: 5 failed attempts within 15 minutes, 15-minute auto-unlock.
9. Access token stored in frontend memory only; refresh token delivered via HttpOnly + Secure + SameSite=Strict cookie.
10. GDPR consent capture at registration with versioned consent text and data minimization.
11. Infrastructure baseline: PostgreSQL 15+, Redis 7+, Node.js 20 LTS, SendGrid for reset email, Kubernetes with HPA (3 replicas → 10).
12. Performance SLOs: login p95 <200ms, refresh p95 <100ms, bcrypt hash <500ms, 500 concurrent login capacity.
13. 99.9% availability SLO over 30-day rolling windows.
14. Complexity classification: HIGH (0.72), architect persona primary.
15. Observability stack: structured JSON logs (with password/token redaction), Prometheus metrics, OpenTelemetry spans `AuthService → PasswordHasher → TokenManager → JwtService`, Grafana dashboards, alertmanager → PagerDuty.

## Divergence Points

### 1. Schedule Realism / Slip Acknowledgment

- **Opus:** Explicitly acknowledges M1 TDD target (2026-04-14) has already passed relative to today (2026-04-20); starts M1 on 2026-04-20, compresses M4/M5 overlap to preserve GA 2026-06-09; tracks as `R-M1-SCHED` and `OQ-M1-001`.
- **Haiku:** Schedules M1 at 2026-03-31 → 2026-04-14 with no slip acknowledgment; treats TDD dates as still achievable.
- **Impact:** Opus plan is defensible given current date but front-loads compression risk; Haiku plan is cleaner on paper but internally inconsistent with extraction's "today = 2026-04-20" reality.

### 2. Milestone Layering Strategy

- **Opus:** Foundation → Token → Compliance/Reset → Frontend → Production (pure technical-layer decomposition).
- **Haiku:** Foundation/Contracts → Core Logic/APIs → User Journeys/Frontend → Hardening/Compliance/Admin → Rollout (theme-based with hardening as its own phase).
- **Impact:** Opus keeps each milestone narrow and parallelizable but spreads hardening across milestones; Haiku concentrates hardening in one large M4 (26 deliverables) which simplifies sign-off but creates a bottleneck.

### 3. Logout Endpoint Decision

- **Opus:** Tracks as open question `OQ-M4-001`; no deliverable row until approved.
- **Haiku:** Closes the gap by adding `API-007` + `COMP-016` (LogoutControl) as committed deliverables in M3.
- **Impact:** Haiku delivers a complete authenticated session lifecycle; Opus defers a PRD-implied capability and leaves stolen-token TTL exposure unresolved until post-M4 decision.

### 4. Admin Operations Coverage

- **Opus:** Defers admin UI and APIs to v1.1; `OQ-M5-002` open; suggests raw SQL access for GA.
- **Haiku:** Closes the Jordan-persona gap with `API-008` (GET /admin/auth-events), `API-009/010` (lock/unlock), `COMP-018/019` (backend services) in M4.
- **Impact:** Haiku fully satisfies PRD persona coverage pre-GA; Opus ships lighter but leaves incident response dependent on DB access.

### 5. Registration Auto-Login Conflict

- **Opus:** Does not surface the PRD-vs-TDD conflict on registration response behavior.
- **Haiku:** Identifies `CONFLICT-2` (PRD says auto-login on register, TDD says 201 + redirect); resolves to TDD contract, flags for v1.1 review.
- **Impact:** Haiku documents a real conversion-relevant product decision; Opus silently implements the TDD behavior without acknowledging the product expectation gap.

### 6. Open-Question Resolution Style

- **Opus:** Leaves 8 open questions across milestones (refresh token cap, remember-me, email sync/async, admin UI, JTBD cross-device, etc.).
- **Haiku:** Closes 11 of its open questions with committed defaults (5 tokens/user cap, async reset email, v1.1 deferrals, etc.); only 2 remain open.
- **Impact:** Haiku reduces pre-M1 decision backlog and is more immediately actionable; Opus preserves optionality but risks blocking downstream work waiting for resolution.

### 7. Automated Rollback Triggers

- **Opus:** Four dedicated automated rollback deliverables: `ROLLBACK-AUTO-LATENCY`, `ROLLBACK-AUTO-ERR`, `ROLLBACK-AUTO-REDIS`, `ROLLBACK-AUTO-DATA`; watchers auto-disable flag on threshold breach.
- **Haiku:** One rollback drill (`TEST-012`) plus go/no-go gate (`OPS-011`); relies on human-gated response to alerts.
- **Impact:** Opus converts TDD §19.4 "automatic conditions" language into literal automation — stronger mean-time-to-mitigate but more infrastructure to build; Haiku is lighter but accepts human-in-the-loop latency during incidents.

### 8. Observability Placement

- **Opus:** Distributes observability across milestones (`METRIC-*`, `NFR-PERF-*` in M1/M2; `OPS-004`, `SUCC-SLO-BOARD` in M5).
- **Haiku:** Concentrates observability in M4 as a dedicated OBS-001..007 series (7 distinct deliverables).
- **Impact:** Opus gets telemetry online earlier (metrics exist as each feature ships); Haiku offers clearer M4 observability contract but risks late-discovered instrumentation gaps.

### 9. M4 Scope Definition

- **Opus:** M4 = Frontend only (16 items: LoginPage, RegisterPage, ProfilePage, AuthProvider, silent refresh, HttpOnly cookie, E2E tests).
- **Haiku:** M4 = Hardening + Compliance + Admin Ops (26 items: performance validation, observability, runbooks, admin APIs, security review).
- **Impact:** Opus M4 is focused and parallelizable with M5 setup; Haiku M4 is the heaviest milestone and creates a single hardening chokepoint before rollout.

### 10. Consent Capture Timing

- **Opus:** GDPR consent lands in M3 as `NFR-GDPR-CONSENT`/`NFR-GDPR-MIN` (after registration is already live in M1).
- **Haiku:** Consent wired at M1 via `NFR-COMP-001`, `COMP-013` (ConsentRecorder), with wiring task `COMP-020` in M2.
- **Impact:** Haiku avoids a schema-change window for consent columns; Opus has registration operating without consent capture during M1-M2 which could create a compliance gap if M1/M2 is ever externally exposed.

### 11. Performance Load Testing Placement

- **Opus:** `NFR-PERF-002` (k6 500-concurrent) in M1, co-located with login.
- **Haiku:** `NFR-PERF-002` + `TEST-009` in M4, grouped with other hardening.
- **Impact:** Opus validates capacity early when fixing is cheap; Haiku runs load tests against a more complete system but later in the schedule.

### 12. Capacity Planning Location

- **Opus:** `OPS-005` in M5 as single deliverable.
- **Haiku:** `OPS-005..010` in M4 (separate runbooks for pod/Postgres/Redis scaling).
- **Impact:** Haiku's decomposition provides clearer operator playbooks; Opus is more compact but treats capacity as a single production concern.

### 13. Health Endpoint Treatment

- **Opus:** Implicit via `NFR-REL-001` blackbox probes on `/health`.
- **Haiku:** Explicit `API-011` GET /health deliverable with documented dependency checks.
- **Impact:** Haiku makes the release-gating contract explicit; Opus assumes the endpoint exists without specifying its shape.

### 14. Success Criteria Dashboard

- **Opus:** Dedicated `SUCC-SLO-BOARD` deliverable in M5 binding every numeric success target to a Grafana panel.
- **Haiku:** `OBS-006`/`OBS-007` rollout dashboard in M4/M5, less explicit about mapping business KPIs to panels.
- **Impact:** Opus makes success-criteria traceability a first-class artifact; Haiku covers similar ground but lower visibility.

### 15. Refresh Token Quota Decision

- **Opus:** `OQ-M2-001` open — storage sizing and multi-device UX unresolved.
- **Haiku:** Closed — capped at 5 per user, evict oldest on sixth issuance.
- **Impact:** Haiku commits to a concrete Redis-sizing number and TokenManager contract; Opus preserves flexibility.

### 16. Risk Register Depth

- **Opus:** 13 risks including schedule risk (`R-M1-SCHED`), key rotation (`R-M2-KEY`), router loop (`R-M4-ROUTER`), rollout destabilization (`R-M5-ROLLOUT`), alert misrouting (`R-M5-ALERT`).
- **Haiku:** 10 risks; omits explicit schedule risk and key rotation risk; adds admin-persona coverage risk (`R-005`) and contract drift (`R-004`).
- **Impact:** Opus is more pessimistic about execution risk; Haiku is more focused on capability-coverage risk.

### 17. Programmatic Auth / API Key Scope

- **Opus:** Closed — `OQ-M5-001` defers API key auth to v1.1.
- **Haiku:** Closed — `OQ-001` defers API key; `JTBD-gap-1` explicitly notes refresh flow satisfies Sam persona for v1.0.
- **Impact:** Same outcome reached, but Haiku documents the JTBD coverage reasoning more clearly.

### 18. Overall Deliverable Count and Granularity

- **Opus:** ~90 deliverables (M1=22, M2=18, M3=14, M4=16, M5=20); granular security and metric tasks.
- **Haiku:** ~84 deliverables (M1=17, M2=16, M3=15, M4=26, M5=10); fewer but larger-scoped line items, especially in M4.
- **Impact:** Opus offers finer-grained tracking and parallelization; Haiku offers clearer milestone themes at the cost of chunkier deliverables that are harder to assign independently.

## Areas Where One Variant Is Clearly Stronger

### Opus stronger

- **Schedule realism:** Only Opus acknowledges the M1 slip; Haiku's start date is internally inconsistent with the stated current date.
- **Automated rollback:** Opus literally implements the TDD §19.4 "automatic conditions" contract; Haiku leaves them as drills.
- **Success traceability:** `SUCC-SLO-BOARD` binds business targets to observable panels as a committed artifact.
- **Early performance gates:** Load testing in M1 catches scalability issues before dependent milestones compound cost.
- **Execution risk coverage:** Richer risk register captures schedule, key rotation, router-loop, and alert-routing failure modes.

### Haiku stronger

- **PRD capability completeness:** Logout (`API-007`), admin event query (`API-008`), admin lock/unlock (`API-009/010`), and admin services (`COMP-018/019`) fully satisfy PRD personas Jordan and authenticated-user scenarios.
- **Decision closure rate:** Resolves more open questions upfront (refresh quota, email async, remember-me, registration auto-login conflict) reducing pre-execution decision debt.
- **Explicit conflict surfacing:** Identifies `CONFLICT-2` (registration auto-login) that Opus missed entirely.
- **Earlier compliance wiring:** Consent capture at M1 instead of M3 avoids compliance gap window.
- **Clearer contract artifacts:** Explicit `API-011` /health endpoint and dedicated runbooks per component (OPS-007..010) give operators better playbooks.

## Areas Requiring Debate to Resolve

1. **Calendar anchoring:** Should the roadmap accept the current-date reality (Opus) or preserve the original TDD calendar on paper (Haiku)? Directly affects executive commitment and downstream dependency chains.
2. **v1.0 admin scope:** Ship admin APIs pre-GA (Haiku) or defer to v1.1 (Opus)? Trade-off between GA scope creep and PRD persona coverage / SOC2 operational readiness.
3. **Logout endpoint:** Deliverable now (Haiku) or deferred pending decision (Opus)? Affects security posture for stolen refresh tokens and PRD user-story completeness.
4. **Registration success UX:** Accept TDD 201-redirect-to-login contract (Haiku explicit) or investigate auto-login per PRD? Has measurable conversion impact against the >60% success metric.
5. **Rollback automation depth:** Build automated metric-driven flag-flippers (Opus) or rely on drilled runbooks (Haiku)? Engineering cost vs. MTTR trade-off.
6. **Open-question policy:** Resolve-by-default with committed values (Haiku) or preserve optionality with tracked open questions (Opus)? Reflects organizational preference for decision velocity vs. stakeholder alignment.
7. **Hardening concentration:** One dedicated hardening milestone (Haiku M4) or hardening distributed across technical layers (Opus)? Affects parallelization and the shape of the pre-GA chokepoint.
8. **Consent timing:** At M1 (Haiku, compliance-safe) or M3 (Opus, lighter M1)? Only matters if M1 is ever externally exposed, which both roadmaps' flag gating intends to prevent.
