---
total_diff_points: 12
shared_assumptions_count: 10
---

## Shared Assumptions and Agreements

1. **Stateless JWT + Redis refresh token architecture** — both variants adopt stateless RS256 access tokens (15min TTL) with hashed opaque refresh tokens stored in Redis (7d TTL).
2. **bcrypt cost=12** for password hashing, with abstraction layer enabling future algorithm migration (Argon2).
3. **RS256 signing with 2048-bit RSA keys**, quarterly rotation policy per NFR-SEC-002.
4. **12-month audit retention** — both resolve OQ-003 in favor of PRD SOC2 requirement over TDD's 90-day default.
5. **Phased rollout with feature flags** — alpha → 10% beta → 100% GA using AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH flags with named rollback triggers.
6. **`/v1/auth/*` URL versioning** for the REST API surface.
7. **Account lockout at 5 attempts / 15 minutes** per TDD FR-AUTH-001.
8. **Parallel-run migration strategy** with idempotent upserts and pre-phase backups to mitigate R-003 data loss.
9. **Observability stack**: Prometheus + OpenTelemetry + Alertmanager; structured logs with secret scrubbing.
10. **Complexity classification HIGH (0.72)** with architect as primary persona; same spec source and core external dependencies (PostgreSQL 15, Redis 7, SendGrid, API Gateway, Node.js 20 LTS).

## Divergence Points

### 1. Timeline and Milestone Granularity
- **Opus**: 16 weeks, 8 milestones (M1–M8) with 1–3 week durations, granular phase separation.
- **Haiku**: 8 weeks, 4 milestones (M1–M4) with 1–4 week durations, compressed layered approach.
- **Impact**: Opus provides finer-grained tracking, exit criteria, and risk isolation per phase but doubles calendar time. Haiku risks overloading M4 (4 weeks covering migration + ops + validation) and collapsing security/observability/testing work into overlapping streams.

### 2. Scope of Admin/Logout Functionality
- **Opus**: Treats logout implicitly (COMP-FE-LOGOUT via refresh revoke); OQ-008 (admin audit/lock) flagged as open question — either add FR-AUTH-006 or descope to v1.1.
- **Haiku**: Explicitly adds API-007 (logout), API-008 (admin audit query), API-009/010 (admin lock/unlock), and COMP-011 (AdminAuditPage) as P1 deliverables in M2/M3.
- **Impact**: Haiku closes PRD Jordan persona gap within v1.0 at cost of scope expansion; Opus preserves tighter 4-endpoint surface but leaves PRD/TDD coverage unresolved.

### 3. Testing Pyramid Treatment
- **Opus**: Dedicated M6 (2 weeks) for testing with 12 test deliverables including TEST-IMPLICIT-BCRYPT/RS256/LOAD/AUDIT, TEST-SEC-ENUMERATION, TEST-SEC-LOCKOUT.
- **Haiku**: 6 test deliverables (TEST-001..006) embedded in M3 alongside frontend work; no separate load/security testing phase.
- **Impact**: Opus achieves explicit 80/15/5 pyramid and automates NFR assertions in CI; Haiku relies on validation phase metrics (SC-001..012) rather than dedicated test infrastructure, risking later NFR drift detection.

### 4. Penetration Test and Security Review Positioning
- **Opus**: COMP-PENTEST as explicit M5 deliverable with vendor booking at Week 6, SOC2 auditor preview, 1-week buffer.
- **Haiku**: R-PRD-004 as risk item in M4 with "dedicated security review + pen-test" as release gate; no dedicated vendor booking schedule.
- **Impact**: Opus reduces schedule risk by early vendor booking; Haiku treats pen-test as release blocker without timeline allocation, risking critical-finding remediation slippage.

### 5. Compliance/SOC2 Validation Depth
- **Opus**: SOC2 dry-run at M5 exit; monthly partition-drop job (OPS-RETENTION-JOB); audit field export validated against SOC2 evidence format.
- **Haiku**: R-PRD-002 as risk with QA validation; 12-month retention confirmed; no explicit SOC2 dry-run deliverable.
- **Impact**: Opus front-loads compliance validation before GA; Haiku validates via ongoing observability checks, leaving compliance signoff to release gate.

### 6. Operational Readiness Scope
- **Opus**: Dedicated M8 (1 week) with 8 deliverables including OPS-RSA-ROTATION automation, OPS-POSTMORTEM-TEMPLATE, capacity plan review cadence.
- **Haiku**: Operations folded into M4 as OPS-001..005 alongside migration and validation.
- **Impact**: Opus separates ops handover cleanly with peer review; Haiku couples ops delivery to rollout timeline, compressing runbook validation.

### 7. Milestone Dependency Graph Complexity
- **Opus**: Multi-branched dependency graph with M1→M2→M3→M4 parallel to M1→M5; M3/M4/M5 converge into M6; M5/M6→M7→M8.
- **Haiku**: Linear chain M1→M2→M3→M4 with external dependency prelude.
- **Impact**: Opus enables parallelism (e.g., M4 frontend concurrent with M5 NFR) but increases coordination overhead; Haiku simpler to track but serializes work that could parallelize.

### 8. Integration Points (NTG) Detail
- **Opus**: 5 NTG artifacts per milestone, detailed with types (DI registry, dispatch table, event binding, middleware, strategy pattern).
- **Haiku**: 5 NTG artifacts per milestone with similar typing but fewer cross-milestone references.
- **Impact**: Comparable rigor; Opus tracks more lifecycle references (e.g., CAPTCHA provider, LaunchDarkly SDK) while Haiku emphasizes edge routing and handler maps.

### 9. Success Criteria Enumeration
- **Opus**: 12 success criteria in final summary table, metrics tied to validation milestones.
- **Haiku**: 12 SC-001..012 as explicit M4 deliverables (one per criterion) with ID, metric, target, validation method.
- **Impact**: Haiku treats validation as actionable deliverables; Opus treats them as measurement criteria applied across milestones — Haiku offers clearer ownership but may inflate M4.

### 10. Open Question Handling
- **Opus**: 10 OQs with blocking milestones, resolution owners; OQ-003 escalation required Day 3 of M1.
- **Haiku**: 10 OQs with similar structure but includes 2 PRD gap-fill questions (logout scope, admin deferral tracking) not in Opus.
- **Impact**: Haiku more explicit about PRD/TDD delta tracking; Opus more explicit about resolution deadlines.

### 11. Frontend Component Journey Validation
- **Opus**: Includes PRD-JOURNEY-FIRSTSIGNUP and PRD-JOURNEY-SESSIONPERSIST as M4 deliverables with usability testing (5 users).
- **Haiku**: Usability testing captured as R-PRD-001 risk mitigation in M4 without explicit journey deliverables.
- **Impact**: Opus operationalizes PRD S22 journey validation; Haiku relies on funnel analytics post-launch.

### 12. Decision Summary Breadth
- **Opus**: 11 decisions covering token architecture, hashing, JWT algo, rollout, retention, refresh storage, lockout, CAPTCHA, versioning, migration, observability.
- **Haiku**: 5 decisions covering session architecture, signing, retention, scope guardrail, rollout.
- **Impact**: Opus documents more architectural choices with alternatives considered, aiding future reviewers; Haiku more concise but omits CAPTCHA, lockout thresholds, and migration-safety rationale.

## Areas Where One Variant Is Clearly Stronger

**Opus stronger in:**
- **Risk isolation via phase separation** (M5 NFR/compliance separate from M6 testing separate from M7 rollout) — reduces blast radius of any single phase slippage.
- **Explicit security review scheduling** — pen-test vendor booking by Week 6 with reserved remediation buffer.
- **Testing rigor** — explicit 80/15/5 pyramid with automated NFR assertions, security enumeration timing tests, lockout verification.
- **Decision documentation depth** — 11 decisions with alternatives and rationale enable future audit.
- **Operational automation** — OPS-RSA-ROTATION automated, post-mortem webhook wired, capacity review cadence.

**Haiku stronger in:**
- **PRD/TDD gap closure** — explicitly adds logout (API-007) and admin surface (API-008/009/010, COMP-011) closing Jordan persona coverage.
- **Compact timeline** — 8 weeks vs 16 weeks enables faster feedback loop if the organization can absorb parallelism.
- **Success criteria as deliverables** — SC-001..012 have owners and methods inline with M4 execution, clearer ownership.
- **Scope discipline** — explicit "v1.0 scope guardrail" decision prevents OAuth/MFA/RBAC creep.
- **Simpler dependency graph** — linear M1→M4 reduces coordination complexity.

## Areas Requiring Debate to Resolve

1. **Timeline realism**: Is 8 weeks (Haiku) achievable given parallel frontend/backend/ops/testing work, or is 16 weeks (Opus) conservative? Needs team velocity data and staffing model.
2. **Admin scope inclusion**: Should v1.0 include admin audit query and lock/unlock (Haiku) to close PRD Jordan persona, or defer to v1.1 (Opus implicit) to protect the 4-endpoint API surface?
3. **Testing phase isolation vs integration**: Dedicated M6 testing phase (Opus) with 80/15/5 targets, or embedded testing in M3 (Haiku) with validation-phase NFR checks?
4. **Penetration test scheduling**: Hard-booked vendor slot at Week 6 (Opus) or release-gate only (Haiku)?
5. **Compliance validation approach**: SOC2 dry-run pre-GA (Opus) or ongoing observability validation (Haiku)?
6. **Operational handover timing**: Dedicated post-GA M8 week (Opus) or in-flight with rollout M4 (Haiku)?
7. **CAPTCHA and progressive friction**: Opus specifies "after 3 fails" via COMP-001; Haiku mentions only as R-002 WAF/CAPTCHA contingency — is progressive friction in-scope for v1.0?
8. **Remember-me functionality**: Opus defers to v1.1 explicitly; Haiku leaves OQ-007 open with impact on AuthProvider — decision needed before M3/M4 frontend freeze.
