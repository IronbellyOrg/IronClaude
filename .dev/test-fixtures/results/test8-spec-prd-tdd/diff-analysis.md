---
total_diff_points: 18
shared_assumptions_count: 14
---

# Roadmap Variant Diff Analysis
**Opus-Architect (A)** vs **Haiku-Architect (B)**

## Shared Assumptions

1. **5-phase structure** — Foundation → Core Logic → Integration → Hardening → Production Readiness, identical phase names and ordering
2. **Complexity assessment** — Both score 0.6 MEDIUM with identical rationale (security surface elevates, bounded scope constrains)
3. **Cryptographic choices** — JWT RS256 2048-bit, bcrypt cost 12, dual-token (access in memory, refresh rotated)
4. **Layered dependency chain** — PasswordHasher + JwtService → TokenManager → AuthService → auth-middleware → routes → frontend
5. **Phase 1-3 durations** — 1.5w, 2w, 2w respectively — no disagreement
6. **Phase 4 duration** — Both 1.5 weeks
7. **Infrastructure stack** — PostgreSQL 15+, Redis 7+, Node.js 20 LTS, SendGrid, Kubernetes/HPA
8. **NFR targets** — p95 < 200ms, 99.9% uptime, >80% coverage, <500ms hash, >60% registration conversion
9. **Feature-flagged rollout** — AUTH_NEW_LOGIN + AUTH_TOKEN_REFRESH flags, alpha → beta (10%) → GA (100%)
10. **Risk count and categories** — Both identify 10 risks covering key compromise, replay, brute-force, Redis outage, SOC2, migration, UX, scope drift
11. **Open question overlap** — 8 of 10 questions match: sync vs queued reset email, max refresh tokens, API-key auth, roles length, remember-me, audit schema, token cascade on deletion, logout scope
12. **Rollback requirement** — Both mandate tested rollback with flag-toggle to legacy auth
13. **Monitoring stack** — Grafana dashboards, Prometheus/OpenTelemetry, PagerDuty alerting
14. **SEC-POLICY-001 dependency** — Both block Phase 1 on policy finalization

## Divergence Points

### 1. Task Granularity
- **A**: 104 task rows — sub-tasks for each FR acceptance criterion (e.g., FR-AUTH.1a through FR-AUTH.1f as separate rows)
- **B**: 64 task rows — consolidates sub-acceptance-criteria into parent task AC fields
- **Impact**: A provides finer sprint tracking and PR sizing; B reduces backlog overhead and is faster to scan but harder to assign individual ACs to developers

### 2. Phase 5 Duration
- **A**: 4 weeks (1w alpha + 2w beta + 1w GA) → **11 weeks total**
- **B**: 2 weeks (compressed alpha/beta/GA) → **~10 weeks total**
- **Impact**: A's longer beta window gives more production signal before GA; B assumes faster validation but risks insufficient soak time for 99.9% uptime proof (needs 7 days minimum per A's exit criteria)

### 3. Test Task Distribution
- **A**: Tests distributed in-phase — unit tests in Phase 1-2, integration in Phase 3, E2E in Phase 4
- **B**: All test tasks consolidated in Phase 4 (TEST-001 through TEST-010)
- **Impact**: A enforces shift-left testing with phase exit gates; B risks late discovery of integration defects and creates a testing bottleneck in Phase 4

### 4. Repository Abstractions
- **A**: No explicit UserRepo or RefreshTokenRepo components — data access implied within AuthService/TokenManager
- **B**: Introduces COMP-013 (UserRepo) in Phase 1 and COMP-014 (RefreshTokenRepo) in Phase 2 as first-class components
- **Impact**: B's explicit repos improve testability (mock boundaries) and separation of concerns; A couples data access to service logic, making unit testing harder

### 5. Contract Freeze Task
- **A**: No explicit contract alignment task — assumes refresh token transport is resolved (httpOnly cookie)
- **B**: Introduces COMP-017 "Freeze refresh-token contract" to resolve cookie-vs-body and DB-vs-Redis drift between spec and TDD
- **Impact**: B catches a real specification ambiguity that A silently assumes away; skipping this risks mid-build rework when the discrepancy surfaces

### 6. API Specification Timing
- **A**: API wiring tasks (API-001 through API-006) appear in Phase 3 as integration work
- **B**: API specification tasks appear in Phase 2 alongside core logic implementation
- **Impact**: B's approach is safer — defining the HTTP contract before wiring catches shape mismatches earlier; A's deferred approach risks AuthService methods not aligning with route handler expectations

### 7. Business Impact Quantification
- **A**: Cites specific figures — $2.4M ARR, SOC2 Q3 deadline, 25% churn correlation
- **B**: Qualitative only — "unblocks Q2 personalization revenue," "closes security gaps"
- **Impact**: A provides stronger stakeholder justification for prioritization; B lacks persuasive specifics for executive buy-in

### 8. Persona Integration
- **A**: Personas appear only in open questions (Sam, Jordan) — not woven into task definitions
- **B**: Explicitly references Alex, Sam, Jordan personas in executive summary, integration points, and success criteria
- **Impact**: B ties delivery to user value more concretely, making acceptance criteria more meaningful; A treats personas as an afterthought

### 9. DTO Definition Timing
- **A**: All DTOs (DM-001 through DM-006) defined in Phase 1 — contracts settled upfront
- **B**: Core models (DM-001, DM-002, DM-003, DM-006) in Phase 1; UserProfile DTO (DM-004) and AuthToken DTO (DM-005) deferred to Phase 3
- **Impact**: A's upfront definition enables earlier API contract reviews; B's deferral is pragmatic (DTOs not consumed until Phase 3) but delays contract visibility

### 10. Edge Case Handling
- **A**: Three explicit edge-case tasks — EDGE-001 (concurrent registration race), EDGE-002 (JWT clock skew), EDGE-003 (Redis unavailability)
- **B**: No dedicated edge-case tasks — relies on integration test coverage to catch these
- **Impact**: A makes edge cases visible and trackable; B may miss them if test cases aren't explicitly written for these scenarios

### 11. Locked Account Status Code
- **A**: Uses 403 for locked accounts without flagging ambiguity
- **B**: Explicitly flags 403 vs 423 as a risk (Risk #4) and pre-build decision
- **Impact**: B is more thorough — the spec/TDD disagreement is real and ignoring it (as A does) causes client-side contract breakage

### 12. Refresh Token Transport Ambiguity
- **A**: Assumes httpOnly cookie throughout without noting spec/TDD drift
- **B**: Calls out spec (httpOnly cookie + DB) vs TDD (request body + Redis) as a blocking pre-Phase-1 risk
- **Impact**: B surfaces a critical architectural decision that could cascade through 20+ tasks; A's assumption may prove wrong

### 13. Runbook Granularity
- **A**: Two specific runbooks — OPS-RUNBOOK-001 (service down) and OPS-RUNBOOK-002 (token refresh failure), each with symptoms/diagnosis/resolution/escalation
- **B**: One general runbook OPS-001 covering both scenarios
- **Impact**: A's specificity is better for on-call engineers under pressure; B's consolidation saves effort but may slow incident response

### 14. Monitoring Detail
- **A**: Explicit metric names (auth_login_total, auth_login_duration_seconds, etc.), OpenTelemetry spans per component, alert thresholds (20% failure rate, p95 > 500ms, Redis failures > 10/min)
- **B**: References same metrics but doesn't specify alert thresholds
- **Impact**: A is production-ready as written; B requires a follow-up task to define thresholds

### 15. Email Verification Question
- **A**: Not raised
- **B**: Open question #10 — "Do we need optional email verification before full activation?"
- **Impact**: B identifies a compliance-adjacent gap that could affect registration semantics and GDPR interpretation

### 16. Capacity Planning Specificity
- **A**: Explicit numbers — HPA 3→10 pods at CPU >70%, pg-pool 100→200, Redis 1GB→2GB at 70%
- **B**: Same targets but stated as bullet points without thresholds for scaling triggers
- **Impact**: A is directly implementable; B requires an engineer to derive the trigger thresholds

### 17. Success Criteria Breadth
- **A**: 11 criteria including DAU >1000 within 30d and session duration >30min
- **B**: 11 criteria including "API consumer refresh clarity" tied to Sam persona
- **Impact**: A includes adoption KPIs; B includes developer-experience metrics — both miss what the other has

### 18. Infrastructure Provisioning Tasks
- **A**: Explicit MIG-001 (PostgreSQL), MIG-002 (Redis), MIG-003 (RSA keys) as separate Phase 1 tasks
- **B**: Bundles infrastructure into dependency table without discrete provisioning tasks
- **Impact**: A makes provisioning trackable and assignable; B risks provisioning falling through cracks

## Areas Where One Variant Is Clearly Stronger

### Variant A (Opus) strengths
- **Granular task decomposition** — every FR sub-criterion is a trackable row, enabling precise sprint planning and PR scoping
- **Quantified business case** — $2.4M ARR, 25% churn, SOC2 Q3 deadline
- **Explicit infrastructure provisioning tasks** — MIG-001/002/003 are assignable and trackable
- **Edge case visibility** — EDGE-001/002/003 prevent "assumed handled" gaps
- **Alert threshold specificity** — directly implementable monitoring config
- **Longer rollout window** — 4 weeks gives realistic soak time for uptime proof
- **Runbook specificity** — two targeted runbooks vs one general

### Variant B (Haiku) strengths
- **Specification ambiguity detection** — COMP-017 contract freeze, 403/423 resolution, refresh transport drift are real risks that A silently ignores
- **Repository abstraction** — UserRepo and RefreshTokenRepo as first-class components improve testability and modularity
- **Persona-driven delivery** — Alex/Sam/Jordan woven into tasks and success criteria, not afterthoughts
- **API-first sequencing** — specifying HTTP contracts in Phase 2 before wiring catches shape mismatches earlier
- **Leaner backlog** — 64 tasks is easier to manage without losing coverage
- **Email verification question** — surfaces a compliance gap A misses
- **Compact timeline** — 10 weeks may be realistic if team is experienced

## Areas Requiring Debate to Resolve

| # | Topic | A Position | B Position | Resolution Needed |
|---|---|---|---|---|
| 1 | **Test timing** | Shift-left: tests co-located with implementation phases | Consolidated: all tests in Phase 4 | Does the team have QA bandwidth in every sprint, or is testing a dedicated phase? |
| 2 | **Task granularity** | 104 rows — one row per AC sub-item | 64 rows — ACs consolidated | Team size and sprint tracking tool matter — 104 rows may be noise for a 3-person team |
| 3 | **Phase 5 duration** | 4 weeks (conservative) | 2 weeks (aggressive) | Can 99.9% uptime be proven in <7 days of GA? B's timeline may not allow it |
| 4 | **Refresh token transport** | httpOnly cookie assumed | Flagged as unresolved | This must be resolved before either roadmap can proceed — B is correct to flag it |
| 5 | **DTO timing** | All upfront in Phase 1 | Split across Phase 1 and 3 | Early contract review vs YAGNI — depends on whether API consumers need early visibility |
| 6 | **Repository layer** | Implicit in services | Explicit COMP-013/014 | Architecture preference — explicit repos add ~2 tasks but improve test isolation |
| 7 | **Locked status code** | 403 assumed | 403 vs 423 flagged as risk | Spec ambiguity is real — must be resolved regardless of which roadmap is chosen |
