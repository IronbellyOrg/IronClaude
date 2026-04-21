---
total_diff_points: 18
shared_assumptions_count: 20
---

# Roadmap Variant Diff Analysis: Opus vs Haiku

## Shared Assumptions and Agreements

1. Complexity class MEDIUM (0.65), architect persona, 10-week total duration ending 2026-06-09.
2. Five technical-layer milestones (Foundation → Core → Tokens/Session → Hardening → GA).
3. Stateless JWT (15-min access) + Redis-backed refresh tokens (7-day TTL, hashed).
4. bcrypt cost factor 12 via `PasswordHasher` abstraction; <500ms hash budget.
5. RS256 with 2048-bit RSA keys, quarterly rotation, 5s clock skew.
6. OQ-CONFLICT-001 / OQ-CFLT-001 resolved to **12-month audit retention** (PRD precedence over TDD's 90 days).
7. Six API endpoints: login, register, me, refresh, reset-request, reset-confirm.
8. Account lockout: 5 attempts / 15-minute sliding window.
9. accessToken in-memory; refreshToken via HttpOnly+Secure+SameSite=Strict cookie.
10. Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` gate phased rollout.
11. Three-phase rollout: Internal Alpha → Beta 10% → GA 100%.
12. Infra: PostgreSQL 15, Redis 7, Node.js 20 LTS, SendGrid for reset emails.
13. Automated rollback triggers (latency, error rate, Redis failures, data corruption) with no human-confirmation gate.
14. NFR-PERF-001 (<200ms p95), NFR-PERF-002 (500 concurrent), NFR-REL-001 (99.9% uptime).
15. v1.0 scope: email/password only; OAuth, MFA, RBAC enforcement deferred.
16. Same core risk taxonomy (R-001 XSS, R-002 brute-force, R-003 migration, R-PRD-001..004).
17. Enumeration-safe 401 on login; enumeration-safe response on reset-request.
18. Gateway-enforced rate limits (10/5/60/30 req/min at login/register/me/refresh).
19. Prometheus metrics (`auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`, `auth_registration_total`), OTel tracing, structured logs with secret scrubbing.
20. TDD↔Roadmap milestone mapping table preserved; technical-layer phasing retained (OQ-CONFLICT-002).

## Divergence Points

### 1. Deliverable Count and Granularity
- **Opus:** 102 deliverables (17+18+24+27+16). Heavier decomposition; separate rows for every metric, trigger, and AC.
- **Haiku:** 77 deliverables (22+13+15+22+5). Consolidates related work into broader components (e.g., COMP-026 RollbackAutomation bundles all triggers).
- **Impact:** Opus offers finer-grained traceability and task-planning primitives; Haiku is easier to scan but risks hiding sub-work during execution.

### 2. Logout Endpoint (PRD Gap)
- **Opus:** No logout endpoint or `LogoutHandler`. Silent on PRD "in-scope" logout.
- **Haiku:** Adds API-007 POST /auth/logout + COMP-015 LogoutHandler in M3.
- **Impact:** Haiku closes a real PRD scope gap for shared-device safety; Opus may leave a user-visible behavior missing at GA.

### 3. Password Reset UI Pages
- **Opus:** Backend reset endpoints only; no dedicated frontend pages for reset flows.
- **Haiku:** Adds COMP-016 ResetRequestPage (/forgot-password) and COMP-017 ResetConfirmPage (/reset-password) in M3.
- **Impact:** Haiku delivers the user-facing recovery journey end-to-end; Opus implicitly assumes another team or future scope owns reset UI.

### 4. Registration-to-Login UX (OQ-CFLT-002)
- **Opus:** Does not surface the PRD/TDD conflict. API-002 returns `UserProfile`; frontend chain unstated.
- **Haiku:** Explicitly identifies conflict (PRD wants immediate login; TDD returns `UserProfile`) and resolves via COMP-002 chaining POST /register → POST /login.
- **Impact:** Haiku reconciles contract vs UX; Opus leaves a potential onboarding friction point unaddressed.

### 5. Admin JTBD Coverage (Jordan persona)
- **Opus:** JTBD-GAP-001 admin CLI over audit_log in M4 (P1), with OQ flagging v1.1 full UI deferral.
- **Haiku:** COMP-010 `AuthEventQuery` service in M4 (queryable audit surface); OQ-JTBD-001 defers lock/unlock UI entirely.
- **Impact:** Opus ships a usable admin surface; Haiku ships query capability only, explicitly not lock/unlock controls.

### 6. CAPTCHA Deliverable
- **Opus:** COMP-CAPTCHA-001 as explicit M4 deliverable (3-failure trigger, P1).
- **Haiku:** CAPTCHA mentioned only in R-002 risk mitigation; no deliverable row.
- **Impact:** Opus schedules the work; Haiku relies on future escalation without a scheduled commitment.

### 7. Rollback Trigger Decomposition
- **Opus:** Four distinct deliverables (OPS-ROLLBACK-T1 latency, T2 error rate, T3 Redis, T4 data corruption) with verbatim thresholds.
- **Haiku:** Single COMP-026 RollbackAutomation deliverable enumerating all triggers in one AC bundle.
- **Impact:** Opus eases per-trigger ownership and dry-run tracking; Haiku risks a trigger slipping during implementation.

### 8. Refresh-Token Transport Strategy
- **Opus:** HttpOnly cookie only (COMP-HTTPONLY-001).
- **Haiku:** Dual-mode — HttpOnly cookie for browsers AND request-body refreshToken for API-consumer (Sam persona).
- **Impact:** Haiku better serves API-consumer contract; Opus is more XSS-restrictive but constrains non-browser clients.

### 9. Penetration Test Commitment
- **Opus:** SEC-PENTEST-001 in M4 with external vendor, 5-business-day triage, Critical/High gate before M5.
- **Haiku:** Pentest appears only in risk mitigation (R-PRD-002); no scheduled deliverable.
- **Impact:** Opus makes pentest a release gate; Haiku risks soft commitment.

### 10. GDPR Article 15 Data Export
- **Opus:** OPS-GDPR-EXPORT (P1) in M5 for user data export.
- **Haiku:** No explicit GDPR export deliverable.
- **Impact:** Opus closes a concrete compliance capability; Haiku leaves it implicit in NFR-COMPLIANCE-002.

### 11. Cost Tracking
- **Opus:** OPS-COST-001 baselines $450/mo and monthly tracking.
- **Haiku:** Mentions cost envelope in infra notes; no deliverable.
- **Impact:** Opus treats cost as an ongoing obligation; Haiku stops at rough sizing.

### 12. Production Key Rotation Dry-Run
- **Opus:** OPS-VULN-001 executes first quarterly rotation in production at M5.
- **Haiku:** Rotation procedure only; no production-rotation deliverable.
- **Impact:** Opus validates the runbook under real conditions; Haiku leaves first production rotation untracked.

### 13. Reset-Request Rate Limit
- **Opus:** Not explicitly defined.
- **Haiku:** OQ-RESET-RL-001 proposes 5/min/IP initial policy.
- **Impact:** Haiku prevents a gap in abuse-resistance policy; Opus leaves a gateway config unaddressed.

### 14. Success Metric Wiring
- **Opus:** Six discrete rows (SUCC-METRIC-001..006) with verbatim targets, in M4.
- **Haiku:** Four analytics components (COMP-022..025).
- **Impact:** Opus enumerates DAU, hash time, failed-login, and session-duration as separate measurable items; Haiku bundles more densely.

### 15. Test Pyramid Coverage
- **Opus:** TEST-001..006 mapped to TDD S15.2.
- **Haiku:** Adds TEST-007 performance/resilience suite for k6 + rollback threshold validation.
- **Impact:** Haiku makes perf/rollback testing explicit; Opus relies on NFR-PERF-002 + OPS-ROLLBACK-T* to cover.

### 16. Compliance Deliverable Distribution
- **Opus:** NFR-COMPLIANCE-001..004 distributed across M1/M2/M4 with per-milestone ACs (COMP-AUDIT-001, COMP-CONSENT-001, COMP-POLICY-001, COMP-LOGHYG-001..002).
- **Haiku:** Compliance mostly anchored in M1 baseline + M4 verification bundles.
- **Impact:** Opus creates milestone-local compliance traceability; Haiku reduces row count but delays verification visibility.

### 17. Decision-Precedence Framing
- **Opus:** Stated rule: Non-Goals never relitigated in milestone ACs; TDD/PRD resolution logged per conflict.
- **Haiku:** Stated rule: PRD precedence for user/compliance outcomes; TDD precedence for API shapes.
- **Impact:** Haiku's rule is more action-guiding during execution; Opus's rule emphasizes scope protection.

### 18. Refresh-Token Per-User Ceiling (OQ-PRD-002)
- **Opus:** Open; unbounded concurrent devices permitted.
- **Haiku:** Open; sizing explicitly marked TBD-pending-OQ-PRD-002 (propagated to OPS-006).
- **Impact:** Haiku threads the open question into capacity planning; Opus leaves implication uncaptured.

## Areas Where One Variant Is Clearly Stronger

**Opus clearly stronger on:**
- Operational release gating (pentest, GDPR export, cost tracking, production key rotation, per-trigger rollback rows).
- Metric/alert decomposition and release-evidence thoroughness (102 deliverables).
- Explicit gate checklists (OPS-SIGNOFF-001, OPS-AUDIT-QA) with verification mechanics.

**Haiku clearly stronger on:**
- PRD scope fidelity: logout endpoint, reset UI pages, registration-immediate-login chain, reset-request rate limit.
- Explicit identification and resolution of inter-source conflicts (OQ-CFLT-002, OQ-JTBD-001).
- API-consumer (Sam persona) path via dual-mode refresh-token transport.
- Propagating open questions into capacity planning (OQ-PRD-002 → OPS-006).

## Areas Requiring Debate to Resolve

1. **Logout endpoint inclusion** — PRD marks in-scope; TDD omits. Ship in v1.0 (Haiku) or defer (Opus)?
2. **Dedicated reset pages** — Are `/forgot-password` and `/reset-password` part of v1.0 frontend scope, or handled elsewhere?
3. **Registration response contract** — Preserve TDD `UserProfile` body and chain login (Haiku), or revisit API-002 shape for seamless UX?
4. **Refresh-token transport** — Browser-only HttpOnly cookie (Opus) vs dual browser + API-consumer body (Haiku)?
5. **Admin surface** — Interim CLI (Opus JTBD-GAP-001) vs query service without lock controls (Haiku COMP-010)?
6. **Pentest, GDPR export, cost tracking, first production key rotation** — Explicit deliverables in M4/M5, or assumed-process items?
7. **CAPTCHA** — Scheduled P1 deliverable (Opus) or risk-register contingency only (Haiku)?
8. **Reset-request rate limit** — Adopt Haiku's proposed 5/min/IP or leave to gateway defaults?
9. **Refresh-token-per-user ceiling (OQ-PRD-002)** — Unbounded (Opus) or bounded before GA (Haiku's sizing implication)?
10. **Granularity preference** — Opus's 102-row decomposition vs Haiku's 77-row consolidation for execution tracking.
