---
total_diff_points: 16
shared_assumptions_count: 16
---

# Structured Diff: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions & Agreements

Both variants agree on these foundational decisions:

1. **RS256 asymmetric JWT signing** — stateless access tokens, stateful refresh tokens
2. **bcrypt cost factor 12** with ~250ms timing target
3. **httpOnly/Secure/SameSite=Strict cookies** for refresh token transport
4. **Layered service architecture** with dependency injection for testability
5. **Feature flag** `AUTH_SERVICE_ENABLED` for zero-downtime rollback
6. **Refresh token rotation** with SHA-256 hash storage and replay detection (revoke-all-on-reuse)
7. **Medium complexity** rating (0.6/1.0)
8. **UUID v4** for all entity identifiers
9. **15-minute access token TTL**, 7-day refresh token TTL
10. **Rate limiting** at 5 attempts/min/IP on login
11. **Password policy**: 8+ chars, 1 uppercase, 1 lowercase, 1 digit
12. **Generic error messages** to prevent email/password enumeration
13. **Reversible migrations** required for rollback capability
14. **k6** as the load testing tool
15. **p95 < 200ms** latency target under normal load
16. **Same deferred items**: OAuth, MFA, RBAC, audit logging, account lockout all pushed to v1.1+

---

## 2. Divergence Points

### D-1: Phase Structure
- **Opus**: 4 phases (Foundation → Core Logic → Integration → Hardening)
- **Haiku**: 6 phases (Crypto → Services → Routes → Database → Advanced → Testing/Deploy)
- **Impact**: Opus's compact structure reduces coordination overhead and gate ceremonies. Haiku's granularity provides more checkpoints but adds ~3 additional gate reviews that may slow velocity on a small team.

### D-2: Timeline Estimate
- **Opus**: 5–6 weeks with 2 engineers + 1 security reviewer
- **Haiku**: 8–9 weeks (6-week critical path + slack) with 5–9 roles
- **Impact**: 50–60% longer timeline in Haiku. The extra time is largely consumed by dedicated testing/deployment phases and more conservative slack estimates. For a startup-pace team, Opus is more realistic; for enterprise delivery with formal gates, Haiku's padding is prudent.

### D-3: Team Sizing
- **Opus**: 2 backend engineers + 1 security reviewer (3 people)
- **Haiku**: 9 named roles (crypto specialist, services architect, API specialist, DB engineer, QA, perf engineer, DevOps, security, tech writer) consolidated to 5–6
- **Impact**: Opus assumes cross-skilled engineers; Haiku assumes role specialization. Opus's lean model is viable for a senior team but creates bus-factor risk. Haiku's model is more realistic for organizations with role boundaries.

### D-4: Database Schema Timing
- **Opus**: Phase 1 (Week 1–2) — schema and migrations are the first deliverable
- **Haiku**: Phase 3 (Weeks 4–5) — schema comes after services are built with mocked DB
- **Impact**: This is the most architecturally significant divergence. Opus's approach means services are built against real tables from the start, catching schema-service mismatches early. Haiku's approach allows service interfaces to stabilize before committing to schema, but risks late-stage integration surprises when mocks are replaced with real DB calls.

### D-5: DI Container Timing
- **Opus**: Phase 1 — set up alongside foundation services
- **Haiku**: Phase 3.4 — set up after database integration
- **Impact**: Opus wires DI early, making all subsequent phases composable from day one. Haiku defers it, meaning Phase 1–2 services use ad-hoc instantiation patterns that must be refactored into the container later.

### D-6: Testing Strategy
- **Opus**: Tests are integrated into each phase (unit tests in Phases 1–2, integration tests in Phase 3, hardening in Phase 4)
- **Haiku**: Dedicated Phase 5 for all comprehensive testing (unit, integration, e2e, security, performance)
- **Impact**: Opus catches bugs earlier by testing within the phase that produces the code. Haiku risks a "testing backlog" where defects found in Phase 5 require rework of Phase 0–4 code. However, Haiku's consolidated phase makes coverage measurement and quality gates more formal.

### D-7: Password Reset Architecture
- **Opus**: Part of `AuthService` (methods on existing service)
- **Haiku**: Separate `PasswordResetService` with its own `reset_tokens` table
- **Impact**: Haiku's separation is cleaner from a single-responsibility perspective and supports independent scaling. Opus's approach is simpler and avoids an extra table, reusing the refresh token infrastructure. For MVP scope, Opus is sufficient; for long-term extensibility, Haiku's separation pays off.

### D-8: Email Dispatch Strategy
- **Opus**: Synchronous for MVP (explicitly defers async to v1.1)
- **Haiku**: Async via message queue (OI-1 resolution favors async)
- **Impact**: Sync dispatch is simpler and eliminates queue infrastructure dependency but blocks the HTTP response on email delivery. Async is production-grade but adds infrastructure complexity (message queue dependency). For MVP, sync is pragmatic.

### D-9: Feature Flag Disabled Behavior
- **Opus**: Auth routes return **404** when flag is false
- **Haiku**: Auth routes return **503** when flag is false
- **Impact**: 404 implies routes don't exist (cleaner for API consumers); 503 implies temporary unavailability (more informative for ops teams). 503 leaks the existence of auth endpoints even when disabled. 404 is the more secure choice.

### D-10: Open Question Resolution Strategy
- **Opus**: All 7 open questions resolved in a pre-Phase 1 decision document (1–2 days)
- **Haiku**: Open questions addressed inline within their relevant phases
- **Impact**: Opus's upfront resolution prevents mid-sprint ambiguity and design thrash. Haiku's deferred approach risks blocked work when a question surfaces mid-phase with no pre-agreed answer.

### D-11: Max Active Refresh Tokens
- **Opus**: Resolves immediately — cap at 5, revoke oldest on overflow
- **Haiku**: Defers to v1.1 (OI-2) as architectural review item
- **Impact**: Without a cap, a compromised account can accumulate unlimited active sessions. Opus's approach is safer for MVP. Haiku's deferral creates a security gap.

### D-12: Reset Token Storage
- **Opus**: Reuses the `refresh_tokens` table pattern (no separate table for reset tokens)
- **Haiku**: Creates a dedicated `reset_tokens` table with `is_used` flag
- **Impact**: Haiku's dedicated table is cleaner and supports distinct lifecycle management (TTL, usage tracking). Opus's implicit approach is less explicit but avoids schema proliferation.

### D-13: Deployment & CI/CD Coverage
- **Opus**: Brief section on rollback verification and monitoring setup
- **Haiku**: Full Phase 6 with CI pipeline, staged rollout (10% → 50% → 100%), Docker artifacts, and deployment documentation
- **Impact**: Haiku provides a production-ready deployment playbook. Opus assumes deployment infrastructure exists or is out of scope. For a greenfield service, Haiku's coverage is necessary.

### D-14: Monitoring & Alerting Detail
- **Opus**: Health check endpoint + APM + PagerDuty integration (3 line items)
- **Haiku**: Detailed metrics catalog, security metrics, alerting thresholds (5% error rate → critical, p95 > 300ms → warning), dashboards
- **Impact**: Haiku's specificity makes monitoring actionable from day one. Opus's brevity requires follow-up work to define what "APM integration" actually means.

### D-15: Risk Coverage
- **Opus**: 5 risks (RISK-1 through RISK-5, with RISK-5 being cookie/body confusion)
- **Haiku**: 6 risks (adds RISK-5 brute-force and RISK-6 password entropy; omits cookie confusion)
- **Impact**: Haiku identifies brute-force and entropy risks that Opus doesn't, though Opus covers a spec-specific ambiguity (OQ-5) that Haiku handles differently. Neither is strictly superior.

### D-16: Documentation Scope
- **Opus**: Rollback runbook mentioned; no comprehensive docs phase
- **Haiku**: Full documentation phase with API docs (OpenAPI), architecture diagrams, operational runbooks, security docs, and developer guide
- **Impact**: Haiku's documentation deliverables support team onboarding and incident response. Opus assumes documentation is organic or out of scope.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Decision velocity**: Open questions resolved upfront; no ambiguity during implementation
- **Lean execution**: Realistic for a 2-person team; avoids process bloat
- **Early integration**: Database schema in Phase 1 catches mismatches sooner
- **Security defaults**: Resolves max refresh token cap immediately (D-11); 404 on disabled flag (D-9)
- **Conciseness**: Every section earns its space; no speculative infrastructure

### Haiku is stronger in:
- **Production readiness**: CI/CD pipeline, staged rollout, monitoring thresholds, and comprehensive documentation
- **Separation of concerns**: Dedicated `PasswordResetService` and `reset_tokens` table
- **Operational visibility**: Detailed metrics, alerting thresholds, and runbooks
- **Risk analysis**: Identifies brute-force and entropy risks
- **Architectural diagrams**: Request flow diagrams and dependency trees aid team alignment
- **Scalability of process**: Phase gates and role assignments work for larger organizations

---

## 4. Areas Requiring Debate to Resolve

1. **Database-first vs service-first** (D-4): The fundamental architectural sequencing question. Should schema be committed before services are built (Opus), or should service interfaces stabilize first with mocks (Haiku)? This depends on schema stability confidence and team's preference for early vs. late integration.

2. **Integrated vs dedicated testing** (D-6): Does testing within each phase (Opus) or a consolidated testing phase (Haiku) better serve quality? Teams with strong TDD culture favor Opus; teams with QA specialists favor Haiku.

3. **Sync vs async email** (D-8): Infrastructure availability is the deciding factor. If a message queue already exists, async is better. If not, the added dependency for MVP is questionable.

4. **Team sizing** (D-3): Depends entirely on org context. A 2-person senior team can deliver Opus's plan. An org with role boundaries needs Haiku's staffing model. Neither is wrong — they target different delivery contexts.

5. **Documentation scope** (D-16): Is comprehensive documentation a Phase 1 deliverable or a post-launch activity? For a service others will operate and extend, Haiku's investment is warranted. For an internal MVP with the authors on-call, Opus's minimalism is fine.
