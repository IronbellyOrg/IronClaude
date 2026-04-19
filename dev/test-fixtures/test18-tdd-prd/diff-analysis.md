---
total_diff_points: 12
shared_assumptions_count: 14
---

# Roadmap Variant Comparison: Opus vs Haiku

## Shared Assumptions and Agreements

1. **Total duration: 14 weeks** — both variants converge on the same overall timeline.
2. **Complexity: HIGH (0.72)** — identical scoring and driver narrative (cross-stack orchestration + compliance + migration).
3. **Architectural decisions** — RS256 2048-bit JWTs, bcrypt cost 12, Redis-backed opaque refresh tokens (7d TTL), 15-min access tokens.
4. **Session model** — stateless AuthService + Redis refresh revocation; memory-only access tokens on frontend.
5. **Three-phase rollout** — Alpha → Beta 10% → GA gated on `AUTH_NEW_LOGIN` + `AUTH_TOKEN_REFRESH` flags with legacy fallback.
6. **API contract gap-fill** — both add `API-005`, `API-006`, `API-007` (reset-request, reset-confirm, logout) missing from TDD.
7. **Functional scope** — FR-AUTH-001..005 fully in scope; MFA/OAuth/RBAC explicitly excluded.
8. **Password reset UX** — enumeration-safe 202/generic confirmation, 1h TTL, single-use token, session invalidation on confirm.
9. **External dependencies** — PostgreSQL 15+, Redis 7+, Node.js 20 LTS, SendGrid, K8s + HPA, Prometheus, OpenTelemetry.
10. **Success criteria SC-001..012** — identical metrics and targets.
11. **Risk register core** — R-001 XSS, R-002 brute-force, R-003 migration data loss, R-004 adoption, R-005 compliance, R-006 email delivery.
12. **Capacity baseline** — 3 replicas min / HPA to 10 at CPU>70%; Redis 1GB scaling to 2GB at >70% utilization.
13. **OQ-002 pre-M1 blocker** — both treat `UserProfile.roles` array length as a schema-freeze gate.
14. **Critical path** — foundation → core auth → token management → profile/reset → validation/compliance → rollout.

## Divergence Points

### 1. Milestone count and partitioning
- **Opus (M1-M6, 6 milestones):** separates Security/Compliance/Observability (M5) from Migration/Rollout (M6).
- **Haiku (M1-M5, 5 milestones):** bundles compliance + non-functional validation into M4, rollout into M5.
- **Impact:** Opus gains a dedicated compliance gate before ramp (cleaner SOC2 audit trail); Haiku reduces coordination overhead but couples compliance evidence to general QA.

### 2. M1 scope philosophy
- **Opus:** M1 is **2 weeks of infra + scaffolds only** — primitives, skeletons, DI wiring, no FR logic yet.
- **Haiku:** M1 is **3 weeks and includes all domain FR implementations** (FR-AUTH-001..005 business logic, AuthService facade complete).
- **Impact:** Opus staggers risk and allows earlier contract freeze; Haiku front-loads backend so M2+ can focus on thin contract/UI work but concentrates risk in a single milestone.

### 3. Frontend work placement
- **Opus:** interleaves frontend (LoginPage/RegisterPage in M2, AuthProvider silent-refresh in M3, ProfilePage in M4).
- **Haiku:** dedicates **M3 entirely** to frontend experience (all pages + AuthProvider + route guards + analytics).
- **Impact:** Opus enables vertical feature slices (each flow end-to-end per milestone); Haiku enables parallel frontend/backend teams and a unified UX review.

### 4. Token management scheduling
- **Opus:** dedicated **M3 (2 weeks)** for token lifecycle, silent refresh, key rotation dry-run.
- **Haiku:** token manager implemented in M1, refresh endpoint exposed in M2, silent refresh UX in M3.
- **Impact:** Opus isolates the highest-risk subsystem for focused review; Haiku treats tokens as a transverse concern, risking late discovery of refresh-race issues.

### 5. API-007 Logout framing
- **Opus:** logout is a **core M2 deliverable** alongside login/register.
- **Haiku:** logout is a **P1 gap-fill** in M2 (acknowledged as PRD-implied but not in enumerated TDD).
- **Impact:** Opus treats it as release-critical; Haiku flags it as scope-drift that needs explicit justification.

### 6. Testing concentration
- **Opus:** tests distributed across M2 (TEST-001/002/004), M3 (TEST-003/005), M4 (TEST-006), M5 (security tests), M6 (NFR-PERF validation).
- **Haiku:** **concentrates almost all testing in M4** (TEST-001..010 + NFR-PERF + compliance validation).
- **Impact:** Opus gives continuous coverage per feature; Haiku creates a hard QA gate but risks a 3-week test sprint becoming the bottleneck.

### 7. Open questions handling
- **Opus:** lists OQ-001 (API key auth) in M3, OQ-003 (sync/async email) in M4, OQ-007 (admin UI) in M5 — each with target dates.
- **Haiku:** clusters OQ-003, OQ-004, OQ-007, OQ-001 all in M2 (contracts milestone).
- **Impact:** Opus distributes resolution owners across phases; Haiku forces contract-phase decisions but risks stalling M2 on product questions.

### 8. Deliverable granularity
- **Opus:** ~95 numbered deliverables across 6 milestones (17/18/14/14/16/16).
- **Haiku:** 67 deliverables across 5 milestones (17/14/12/14/10).
- **Impact:** Opus offers finer tracking and clearer PR scoping; Haiku reduces roadmap overhead but combines related work into larger tickets.

### 9. Observability strategy
- **Opus:** OPS-005 observability stack lands in **M5** as a cross-cutting milestone with alerts, dashboards, tracing, log redaction.
- **Haiku:** observability package in **M4** (alongside validation) then **deployed** in M5 via OPS-005.
- **Impact:** Opus treats observability as an engineered deliverable with its own design phase; Haiku couples it to test instrumentation, potentially reducing dashboard polish.

### 10. Migration risk rituals
- **Opus:** explicit **Backup-001** (pre-phase PG snapshots), **Rollback-001** (game-day exercise), **Postmortem-001** (48h SLA template), **GAExit-001** (SC-001..012 checklist), **LegacyDeprec-001** (sunset headers, 4-week deprecation).
- **Haiku:** rollback via COMP-027 wiring; runbooks (OPS-001/002); no explicit game-day, backup automation, or postmortem template as deliverables.
- **Impact:** Opus produces stronger release discipline and audit artifacts; Haiku relies on existing org processes for these concerns.

### 11. Key rotation operationalization
- **Opus:** AC-009 quarterly key rotation with kid-overlap procedure dry-run in **M3**.
- **Haiku:** COMP-028 quarterly rotation operations path scheduled in **M5 (post-launch)** as a P1 item.
- **Impact:** Opus validates rotation before GA (catches kid-resolution bugs early); Haiku defers to operations, accepting post-launch risk.

### 12. Convergence / provenance metadata
- **Opus:** `adversarial: false`, `convergence_score: none`.
- **Haiku:** `convergence_score: 1.0` (claims full convergence).
- **Impact:** Opus is presented as an independent first draft; Haiku signals it considers itself aligned with (or converged toward) a reference variant — downstream reconciliation should treat this difference explicitly.

## Areas Where One Variant Is Clearly Stronger

**Opus is clearly stronger in:**
- Migration/operations rigor (Backup-001, Rollback-001 game-day, Postmortem-001 template, GAExit-001 checklist, legacy sunset headers).
- Integration point documentation (per-milestone artifact/type/wired tables are more detailed).
- Risk mitigation granularity (timing-side-channel R-008 called out, refresh replay R-009 called out, tail-latency R-010 called out — absent in Haiku).
- Pre-GA key rotation validation.

**Haiku is clearly stronger in:**
- Narrative clarity — milestones align to lifecycle phases (foundation / contracts / UX / validation / rollout), easier for stakeholders to reason about.
- Explicit PRD-gap-fill reasoning with architect ownership for contract completeness.
- Concision — 30% fewer deliverables conveying essentially the same plan.
- Parallelization affordance — dedicated frontend milestone enables clean team-split.

## Areas Requiring Debate to Resolve

1. **Vertical-slice vs horizontal-layer structure** — should each milestone deliver one flow end-to-end (Opus), or should the roadmap partition by layer (backend / contracts / frontend / validation / rollout per Haiku)?
2. **Test timing** — continuous per-milestone (Opus) vs a dedicated hardening sprint (Haiku M4)?
3. **Compliance gate separation** — is SOC2/GDPR its own milestone (Opus M5) or subsumed into the validation sprint (Haiku M4)?
4. **Token subsystem isolation** — dedicated milestone warranted by complexity (Opus M3) or treated as transverse code (Haiku)?
5. **Operational artifact scope** — are Backup-001, Rollback-001 game-day, Postmortem-001 inside the roadmap (Opus M6) or outside in platform/SRE standards (Haiku)?
6. **Key rotation timing** — pre-GA dry-run (Opus) vs post-launch ops (Haiku)?
7. **Duration of M1** — 2 weeks of scaffolding (Opus) vs 3 weeks that include FR business logic (Haiku)?
8. **Logout priority** — release-critical P0 (Opus) vs acknowledged gap-fill P1 (Haiku)?
