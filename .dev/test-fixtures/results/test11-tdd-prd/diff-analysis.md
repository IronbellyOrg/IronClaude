---
total_diff_points: 12
shared_assumptions_count: 10
---

# Comparative Analysis: Roadmap Variants

## Shared Assumptions and Agreements

Both variants converge on the following foundational decisions:

1. **Complexity rating** — HIGH (0.72), architect-led, single-generator (no adversarial debate).
2. **Architecture primitives** — PostgreSQL for user/audit persistence; Redis for hashed refresh tokens only; RS256/2048 JWT; bcrypt cost 12; 15-min access / 7-day refresh TTLs.
3. **Fail-closed posture** — `TokenManager` forces re-login on Redis outage rather than silently extending sessions.
4. **Retention rule** — PRD's 12-month audit retention overrides TDD's 90-day figure.
5. **Risk catalog** — Both enumerate R-001 through R-007 with identical severity/likelihood ratings and core mitigations.
6. **Rollout model** — Alpha (internal) → Beta (10%) → GA (100%), gated by feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH`.
7. **Success criteria** — p95 < 200ms login, 99.9% uptime, >80% unit coverage, >60% registration conversion, <5% failed login rate.
8. **External dependency set** — PostgreSQL 15, Redis 7, Node 20 LTS, bcryptjs, jsonwebtoken, SendGrid, API Gateway, SEC-POLICY-001, K8s+HPA.
9. **Gap acknowledgment** — Both surface the admin audit/unlock gap (Jordan persona) as PRD-required but TDD-omitted.
10. **Critical-path ordering** — Security/data primitives → backend contracts → frontend session UX → compliance/admin → phased rollout.

## Divergence Points

### 1. Timeline Compression
- **Opus:** 16 weeks across 8 phases (2 weeks each).
- **Haiku:** 12 weeks across 5 phases (2-3 weeks each).
- **Impact:** Opus provides more buffer for Phase 0 infrastructure and a dedicated observability/compliance phase (Phase 6). Haiku front-loads infra into Phase 1 and compresses backend into a single 3-week phase, increasing execution density and rework risk if Redis/JWT primitives are wrong.

### 2. Phase Granularity
- **Opus:** 8 phases with discrete Phase 0 (Infrastructure) and Phase 6 (Compliance/Observability/Admin).
- **Haiku:** 5 phases that bundle infrastructure into the data/security baseline and admin tooling into a combined hardening phase.
- **Impact:** Opus isolates infrastructure provisioning as a gating concern (better parallelism for SRE); Haiku reduces coordination overhead but couples security primitives to infra readiness.

### 3. Task Row Density
- **Opus:** 112 task rows with fine-grained decomposition (e.g., `OPS-005` split into `.metrics`, `.trace`, `.dash`, `.alert`).
- **Haiku:** 67 task rows with coarser bundling (observability in one `OPS-005` row).
- **Impact:** Opus gives estimators and reviewers sharper acceptance criteria per unit; Haiku is more digestible but leaves more interpretation to implementers.

### 4. Open Questions Handling
- **Opus:** 7 open questions; OQ-005 is elevated to a blocking Phase 1 gate (`PRE-OQ-005`).
- **Haiku:** 11 open questions (OQ-008 through OQ-011 are net-new: retention conflict, multi-device policy, admin unlock scoping, logout requirement gap); several are resolution tasks within Phase 5.
- **Impact:** Haiku surfaces more ambiguity for stakeholder resolution but defers several to late phases, risking late rework. Opus pre-resolves fewer questions but gates the critical one upfront.

### 5. Risk Catalog Breadth
- **Opus:** 9 risks — adds R-008 (RSA key compromise) and R-009 (refresh-rotation race).
- **Haiku:** 7 risks — limited to the base set.
- **Impact:** Opus anticipates cryptographic and concurrency failure modes that Haiku leaves implicit. Haiku's leaner list is easier to track but may miss operational edge cases.

### 6. Integration Points Depth
- **Opus:** Per-phase integration tables with explicit DI bindings, route registrations, and middleware chains (~30 rows across phases).
- **Haiku:** Per-phase integration tables at a higher abstraction level (~20 rows).
- **Impact:** Opus's integration tables function as implementation contracts; Haiku's read more like narrative summaries.

### 7. Password Reset Phase Positioning
- **Opus:** Phase 4 (weeks 9-10) — isolated before frontend integration.
- **Haiku:** Phase 3 (weeks 6-8) — bundled with frontend session UX.
- **Impact:** Opus lets backend reset flow stabilize before UI wiring; Haiku enables earlier end-to-end user journey testing at the cost of concurrent backend+frontend debugging.

### 8. Compliance Validation
- **Opus:** Explicit `SOC2-VALIDATION` gate task in Phase 6 with compliance dry-run against CC6.1/CC6.6/CC7.2 controls.
- **Haiku:** Compliance evidence assembly mentioned in Phase 4 integration points without a formal gate task.
- **Impact:** Opus creates an auditable signoff checkpoint; Haiku risks compliance discovery happening during GA rather than before.

### 9. Observability Instrumentation
- **Opus:** Four dedicated rows (metrics, traces, dashboards, alerts) plus APM/SLO/synthetic tasks in Phase 6.
- **Haiku:** Single `OPS-005` row encompassing logs/metrics/traces/alerts in Phase 1.
- **Impact:** Opus treats observability as a first-class phase gate; Haiku front-loads the baseline but may under-invest in dashboard/alert tuning.

### 10. Rollback Procedure Formalization
- **Opus:** Explicit `ROLLBACK-PROC`, `ROLLBACK-TRIG`, `BACKUP-PRE`, `POST-GA-VERIFY`, `FLAG-CLEANUP` tasks in Phase 7.
- **Haiku:** Rollback referenced via flag-flip in MIG-001/002/003 acceptance criteria without dedicated drill tasks.
- **Impact:** Opus enforces rehearsed rollback with drill tasks; Haiku treats rollback as configuration rather than practiced procedure.

### 11. Frontend Security Hardening
- **Opus:** Dedicated rows for `ACCESS-MEMORY`, `REFRESH-COOKIE` (HttpOnly+SameSite), `FE-401-INTERCEPT` (single-inflight), `FE-A11Y`.
- **Haiku:** Silent refresh and 401 handling specified at the `COMP-004` AuthProvider level without separate hardening rows.
- **Impact:** Opus makes XSS/R-001 mitigations reviewable as discrete deliverables; Haiku embeds them in the AuthProvider contract.

### 12. Admin Tooling Scope
- **Opus:** `API-008` audit query + `ADMIN-UNLOCK` treated as in-scope for v1.0 in Phase 6.
- **Haiku:** `COMP-013`/`COMP-014`/`API-008`/`API-009` included but paired with `OQ-010` asking whether unlock is v1.0 or v1.1.
- **Impact:** Opus commits to admin completeness; Haiku defers the scope decision, which could shrink Phase 4 if unlock is descoped.

## Areas Where One Variant Is Clearly Stronger

**Opus stronger on:**
- Cryptographic risk coverage (R-008/R-009).
- Compliance auditability (SOC2 dry-run gate).
- Rollback rigor (drill tasks, backup pre-stage, triggers as alerts).
- Implementation specificity (112 granular acceptance criteria).
- Frontend security hardening as discrete deliverables.

**Haiku stronger on:**
- Ambiguity surfacing (11 vs 7 open questions; catches retention conflict, logout gap, multi-device policy, admin unlock scoping explicitly).
- Timeline aggressiveness (12 weeks vs 16) — closer to PRD Q2 2026 target with more slack against Q3 SOC2 deadline.
- Reduced coordination overhead (5 phases vs 8).
- Readability for stakeholder review.

## Areas Requiring Debate to Resolve

1. **Timeline vs rigor trade-off** — Is the 4-week delta (16 vs 12 weeks) justified by Opus's observability/compliance phase, or does Haiku's compression deliver acceptable risk given the Q3 SOC2 buffer?
2. **Phase count** — Does an isolated Phase 0 (infra) pay for itself, or should infra be bundled into the security/data baseline as Haiku does?
3. **Password reset sequencing** — Should reset ship before frontend (Opus) to stabilize backend first, or alongside frontend (Haiku) to enable earlier E2E coverage?
4. **Admin unlock v1.0 scope** — Opus commits; Haiku defers via OQ-010. Which matches product intent for Jordan persona?
5. **Open question resolution timing** — Should retention/logout/multi-device policy questions (Haiku's OQ-008/009/011) gate Phase 1 or be resolved during rollout?
6. **Observability investment shape** — Is a dedicated compliance/observability phase (Opus Phase 6) necessary, or does baseline instrumentation in Phase 1 (Haiku) suffice if tuned during beta?
7. **Rollback formality** — Do drill tasks and dedicated backup pre-stages warrant explicit roadmap rows, or is flag-flip rollback sufficient?
8. **Risk catalog completeness** — Are R-008 (RSA compromise) and R-009 (refresh race) material enough to track formally, or is Haiku's 7-risk list adequate coverage?
