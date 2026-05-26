# Sonnet:Architect Variant — Roadmap Proposal

> Captured verbatim from the sonnet:architect sub-agent during multi-roadmap adversarial generation. Preserved for traceability.

## Architectural Stance

Ship working slices to production fast. Layer thin vertical slices, align phasing with the PRD's Sprint 1-3 / Sprint 4-6 structure. Ship the minimum testable auth loop first so wrong-design discovery happens in week 2, not week 8.

## Milestones

### M1: Core Auth Loop (Login + Register + JWT)

- Type: FEATURE | Priority: P0 | Effort: L | Risk: High
- Dependencies: none
- Deliverables: User table schema (users, refresh_tokens, audit_events from day 1); POST /auth/register; POST /auth/login with lockout; JwtService + PasswordHasher + UserRepo modules
- Objective: Ship the minimum auth loop end-to-end. By including audit_events table in initial schema (not later retrofit), every subsequent milestone inherits compliance-grade logging. Internal alpha can begin immediately after M1.

### M2: Session Lifecycle (Refresh + Logout + Profile)

- Type: FEATURE | Priority: P0 | Effort: M | Risk: Med
- Dependencies: M1
- Deliverables: POST /auth/refresh (7-day TTL, Redis token family, rotation-on-use); POST /auth/logout (token invalidation, Redis blacklist); GET /auth/me; TokenManager module (family tracking + reuse detection)
- Objective: Complete the session API surface. After M2 the backend API is feature-complete for Sprint 1-3 scope. Beta rollout (Phase 2) can begin.

### M3: Auth Integration Tests + Security Baseline

- Type: TEST | Priority: P1 | Effort: M | Risk: Low
- Dependencies: M2
- Deliverables: Integration test suite (all 6 endpoints, >90% coverage); security regression tests (lockout, bcrypt cost, JWT expiry, RS256 sig, refresh reuse rejection); rate-limiting middleware (per-IP + per-account)
- Note: Rate limiting is folded into the test milestone — both a security control (RISK-002) and an operability concern best validated by the integration harness being built in the same milestone.

### M4: Password Reset + Audit Compliance

- Type: SECURITY | Priority: P1 | Effort: M | Risk: Med
- Dependencies: M2, M3
- Deliverables: POST /auth/reset-request (1hr TTL token, SendGrid); POST /auth/reset-confirm (rehash + invalidate sessions); audit log query API + 12-month retention enforcement (cron archiver); SendGrid retry queue + DLQ
- Objective: Reset flow end-to-end. Audit compliance completed here because the schema existed from M1 but the query interface + retention enforcement + structured export needed for SOC2 evidence require dedicated work.

### M5: Frontend Integration + Performance Validation

- Type: IMPROVEMENT | Priority: P2 | Effort: L | Risk: Med
- Dependencies: M3
- Deliverables: React AuthProvider (httpOnly cookies + CSRF pairing); LoginPage + RegisterPage + ProfilePage; perf load test suite (k6/Artillery — login p95<200ms, refresh p95<100ms, 500 concurrent)
- Objective: User-facing layer + validate all perf NFRs before GA. Building UI against a stable, tested API (post-M3) eliminates contract churn.

### M6: Production Hardening + Phased Rollout

- Type: MIGRATION | Priority: P1 | Effort: M | Risk: High
- Dependencies: M4, M5
- Deliverables: Feature-flag infrastructure (AUTH_NEW_LOGIN, AUTH_TOKEN_REFRESH); data migration scripts with checksums + rollback; JWT key-rotation automation (quarterly RS256 + grace overlap + kid migration); rollout runbook (Phase 1→2→3 with rollback criteria + monitoring alerts)
- Objective: Ship to production with controlled rollout. Each rollout phase corresponds to a concrete, testable artifact.

## Critical Path

M1 → M2 → M3 → M4 → M6 (5 sequential). M5 branches off M3, runs parallel to M4, shortening overall timeline by ~1 milestone duration.

## Decision Rationale (key points)

- Core auth in M1 ships highest-risk surface first — discovering wrong design in week 2 cheaper than week 8
- Token refresh folded into M2 — refresh is architecturally inseparable from JWT issuance contract
- Frontend deferred past test baseline (M3) — building UI against unstable API wastes effort on contract churn
- Password reset separate milestone — external SendGrid dep with own failure modes shouldn't block core auth
- Audit logging split: schema in M1, compliance tooling in M4 — never an unlogged period, but no delay for SOC2 query API
- Rollout phases map to milestones, not sprints — each phase corresponds to a concrete artifact
