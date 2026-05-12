---
total_diff_points: 17
shared_assumptions_count: 17
---

## Shared Assumptions and Agreements

Both variants agree on the following:

1. RS256 asymmetric signing (never HS256) with secrets manager-backed private key
2. bcrypt cost factor 12, targeting ~250ms hash timing (SC-3)
3. Identical 5 functional requirements in scope (FR-AUTH.1–5)
4. Identical 3 NFR targets (NFR-AUTH.1–3) and all 8 success criteria (SC-1–SC-8)
5. Identical implementation dependency order: `password-hasher.ts` → `jwt-service.ts` → `token-manager.ts` → `auth-service.ts` → `auth-middleware.ts` → routes + migration
6. `AuthService` is the sole external-facing orchestrator; internal components not exposed directly via HTTP
7. Refresh tokens stored as hashes in database (FR-AUTH.3 AC-4)
8. Token rotation with replay detection triggers full user-wide revocation (SC-8)
9. `AUTH_SERVICE_ENABLED` feature flag gates all new routes
10. httpOnly cookie delivery for refresh tokens (XSS/CSRF mitigation)
11. Migration `003-auth-tables.ts` must include a working down-migration
12. Sensitive fields (`password_hash`, `refresh_token_hash`) excluded from profile response (FR-AUTH.4 AC-3)
13. 90-day RSA key rotation automation required before production
14. Same blocking OQs identified: OQ-1, OQ-6, OQ-7 (email service, email service contract, secrets manager)
15. `jsonwebtoken` and `bcrypt` libraries require security/maintenance review before adoption
16. k6 + APM tooling required for NFR validation
17. Known tension between SC-1 (p95 < 200ms) and bcrypt cost factor 12 (~250ms) acknowledged as a constraint conflict

---

## Divergence Points

### 1. Phase count and granularity

- **Opus**: 4 phases (Phase 0–4), 8 milestones
- **Haiku**: 7 phases (Phase 0–6), 7 milestones
- **Impact**: Haiku's finer phase breakdown creates clearer separation between NFR validation (Phase 4), release verification (Phase 5), and production rollout (Phase 6). Opus collapses NFR validation, security hardening, and rollout into Phases 3–4, which risks scheduling pressure. Haiku's structure makes scope cuts easier to reason about; Opus is simpler to communicate to stakeholders.

---

### 2. Total timeline

- **Opus**: 21–31 days
- **Haiku**: 25–36 working days
- **Impact**: Haiku's longer estimate reflects the additional dedicated phases for operational hardening and post-launch stabilization. Opus may be optimistic; Haiku may pad unnecessarily for a medium-complexity system.

---

### 3. Reset token ownership in Phase 1

- **Opus**: Reset token TTL (SC-7, FR-AUTH.5 AC-1) is introduced in Phase 2 inside `AuthService`
- **Haiku**: Explicitly includes reset token TTL (1 hour) as a responsibility of `jwt-service.ts` in Phase 1, alongside access and refresh tokens
- **Impact**: Haiku's approach is architecturally cleaner — all token lifetimes are co-located in the JWT service. Opus's approach means reset token logic is not unit-tested until Phase 2 integration tests, creating a later feedback loop.

---

### 4. Emergency key rotation procedure scope

- **Opus**: Lists "emergency key rotation procedure for active breach" as a residual gap deferred to v1.1
- **Haiku**: Explicitly includes "add emergency rotation runbook" as a Phase 4 task, treating it as a v1.0 deliverable
- **Impact**: This is a meaningful security posture difference. RISK-1's blast radius (total auth bypass via forged tokens) makes the lack of an emergency rotation procedure a real operational gap. Haiku is more defensible; Opus explicitly accepts this risk.

---

### 5. Anomaly alerting on rapid token rotation

- **Opus**: Listed under RISK-2 residual gaps, deferred to v1.1
- **Haiku**: Included in Phase 4 as "anomaly signals for rapid repeated refresh attempts"
- **Impact**: Without anomaly alerting, replay attacks may succeed silently before full-revocation logic is triggered. Haiku closes this gap in v1.0; Opus accepts the observability blind spot.

---

### 6. OQ default handling when stakeholders are unavailable

- **Opus**: Lists OQs to resolve; no fallback behavior documented
- **Haiku**: Explicitly states decisions should have "approved defaults if stakeholders do not decide in time"
- **Impact**: Haiku is more operationally pragmatic. Without defaults, a delayed OQ-7 decision (secrets manager) blocks Phase 1 implementation entirely under Opus's model.

---

### 7. Account lockout (OQ-3) framing

- **Opus**: Treats OQ-3 as a conditional scope item — if v1.0, add progressive lockout to Phase 2.1; if v1.1, document the gap
- **Haiku**: Defaults to explicit deferral: "minimum v1 behavior remains IP rate limiting; architecture should leave room for account-centric lockout extension"
- **Impact**: Haiku pre-decides the deferral (reducing ambiguity), while Opus leaves it open. Haiku's approach prevents scope creep during Phase 2; Opus's approach preserves the option to include it without team alignment.

---

### 8. Latency/bcrypt tension — when to surface it

- **Opus**: Recommends running a full-path benchmark in Phase 1.1 (as early as possible), not just the isolated hash operation
- **Haiku**: Addresses the bcrypt contribution analysis in Phase 4 performance validation
- **Impact**: Opus surfaces this risk 3–4 weeks earlier. If the latency target is infeasible, discovering it in Phase 1 vs. Phase 4 changes the cost of course correction substantially. Opus is stronger here.

---

### 9. OQ-8 concurrency handling recommendation

- **Opus**: Says "document accepted behavior" — treats concurrency race as a policy decision, not an implementation prescription
- **Haiku**: Prescribes "transactional rotation logic" as the default implementation approach
- **Impact**: Haiku commits to a concrete implementation decision; Opus defers to stakeholders. Transactional rotation is the correct technical approach to OQ-8, but the choice should be confirmed by the OQ-8 decision owner.

---

### 10. Staffing model detail

- **Opus**: 3 roles (1 backend engineer, 1 part-time security reviewer, 1 part-time DevOps engineer)
- **Haiku**: 5 roles (backend engineer, security engineer, platform/DevOps engineer, QA/test engineer, product/architecture owner)
- **Impact**: Haiku explicitly identifies QA as a distinct role and adds a product/architecture owner responsible for OQ resolution. Opus's model may underestimate coordination overhead, especially for blocking OQs.

---

### 11. NFR validation timing relative to security hardening

- **Opus**: NFR validation and security hardening co-located in Phase 3
- **Haiku**: NFR validation in Phase 4; security validation in Phase 5
- **Impact**: Opus risks de-prioritizing one domain if time is tight — security and performance testing often compete for the same engineering attention. Haiku's separation creates clearer accountability but extends the timeline.

---

### 12. Post-launch review and next-scope decisions

- **Opus**: Ends at Phase 4 (deployment, feature flag removal); no structured post-launch review
- **Haiku**: Phase 6 includes explicit review of OQ-3, OQ-4, OQ-5, OQ-8 based on observed production behavior, feeding into the next release scope
- **Impact**: Haiku closes the PDCA loop. Opus leaves deferred items in an informal state. For a security-critical service, a structured post-launch assessment of deferred risks is operationally valuable.

---

### 13. Release gates — consolidated vs. distributed

- **Opus**: Exit criteria defined per phase; no consolidated release gate list
- **Haiku**: Provides 5 explicit, numbered release gates including "RISK-1 and RISK-2 mitigations are implemented, not merely documented"
- **Impact**: Haiku's consolidated list provides a clear launch checklist for a go/no-go decision. The "implemented, not merely documented" qualifier is particularly strong and prevents security theater.

---

### 14. Operational validation drills

- **Opus**: Validates key rotation automation (Phase 3.2) and down-migration correctness (Phase 4.2)
- **Haiku**: Explicitly includes "key rotation drill" and "rollback exercise using migration down path" as named validation tasks in Phase 5
- **Impact**: Naming these as drills (not just verifications) implies rehearsed operational procedures, which is more meaningful for incident readiness than a one-time automated check.

---

### 15. Integration point documentation format

- **Opus**: Uses a structured table (Named Artifact / Wired Components / Owning Phase / Consumed By)
- **Haiku**: Uses named artifact blocks with descriptive bullet list format
- **Impact**: Opus's table format is more scannable for dependency tracking. Haiku's prose blocks are easier to read but harder to cross-reference when tracing a component through multiple phases. Preference is stylistic but Opus's table has better operational utility.

---

### 16. Deferred items tracking

- **Opus**: Maintains an explicit "Items Deferred to v1.1" section with a numbered list
- **Haiku**: Deferred items are distributed across risk entries and OQ resolution guidance; no consolidated deferral list
- **Impact**: Opus's deferral section is more useful for backlog management and handoff documentation. Haiku requires cross-referencing risk and OQ sections to reconstruct the full deferral list.

---

### 17. Phase 0 duration estimate

- **Opus**: 3–5 days for Phase 0
- **Haiku**: 2–3 days for Phase 0
- **Impact**: Given 8 OQs to resolve (several requiring external stakeholder decisions including email provider selection and secrets manager platform), Opus's estimate is likely more realistic. Decision cycles involving third-party providers rarely resolve in 2–3 days.

---

## Areas Where One Variant is Clearly Stronger

**Opus is stronger on:**
- Early risk surfacing — recommending the bcrypt/latency benchmark in Phase 1 rather than Phase 4
- Integration point documentation — the table format is operationally superior for dependency tracing
- Consolidated deferral list — explicit v1.1 section is better for backlog and handoff management
- Phase 0 realism — 3–5 days is a more credible estimate for OQ resolution involving external vendor decisions

**Haiku is stronger on:**
- Emergency key rotation — treating it as a v1.0 deliverable rather than a residual gap
- Anomaly alerting for RISK-2 — closing the observability blind spot in v1.0
- Post-launch governance — Phase 6 with explicit review criteria closes the PDCA loop
- Release gates — the consolidated numbered list with "implemented, not documented" qualifier is the strongest launch governance mechanism in either variant
- OQ default handling — the pragmatic fallback for delayed stakeholder decisions prevents implementation blockage
- Staffing model — explicitly identifying QA and product/architecture owner as distinct roles better reflects real project dynamics
- Operational drills — naming key rotation and rollback as drills (not just checks) implies better incident readiness

---

## Areas Requiring Debate to Resolve

1. **Emergency rotation procedure scope** — The security argument for including it in v1.0 (Haiku) is strong given RISK-1 severity, but it adds scope and requires stakeholder alignment on incident response process ownership.

2. **Anomaly alerting scope** — Whether rapid-rotation anomaly alerting belongs in v1.0 or v1.1 depends on the threat model and available observability infrastructure. Neither variant provides a risk-based threshold for the deferral decision.

3. **OQ-8 implementation approach** — Haiku's prescription of transactional rotation is technically sound, but Opus is correct that the policy decision (idempotency window vs. accepted false-positive invalidation) belongs to the OQ-8 decision owner. The implementation approach follows from the policy, not the reverse.

4. **Phase structure trade-off** — 4 phases (Opus) vs. 7 phases (Haiku) represents a meaningful trade-off between simplicity and separation of concerns. Teams with dedicated QA and security engineers benefit from Haiku's structure; smaller teams may find it introduces unnecessary coordination overhead.

5. **Latency profiling timing** — Opus's Phase 1 benchmark recommendation is lower risk, but Haiku's Phase 4 placement keeps Phase 1 focused on correctness. The right answer depends on how confident the team is that the 200ms target is achievable given the bcrypt budget — if there is any doubt, Opus's approach is correct.

6. **Account lockout (OQ-3) default** — Haiku pre-decides deferral; Opus leaves it open. Neither approach is wrong, but the team should explicitly align on which default assumption drives Phase 2 planning to avoid mid-implementation scope changes.
