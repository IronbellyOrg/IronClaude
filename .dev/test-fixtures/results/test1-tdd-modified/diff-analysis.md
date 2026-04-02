---
total_diff_points: 12
shared_assumptions_count: 14
---

## 1. Shared Assumptions and Agreements

Both variants agree on these foundational elements:

1. **Complexity rating** — 0.65 (MEDIUM), driven primarily by security surface area
2. **Core component set** — `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`, `AuthProvider`
3. **Technology stack** — PostgreSQL 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid
4. **JWT architecture** — RS256 with 2048-bit RSA keys, 15-min access tokens, 7-day refresh tokens in Redis, 5s clock skew tolerance
5. **Security model** — In-memory access tokens (not localStorage), HttpOnly cookies for refresh tokens, bcrypt cost factor 12
6. **API versioning** — All routes under `/v1/auth/*`
7. **Account lockout** — 5 failed attempts in 15 minutes
8. **Rollout strategy** — Three-phase: Internal Alpha → 10% Beta → GA with feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH`
9. **Same six external dependencies** with identical provisioning concerns
10. **Risk identification** — Both identify R-001 (XSS token theft), R-002 (brute-force), R-003 (migration data loss) as the primary risks
11. **Success criteria** — Identical seven metrics (p95 < 200ms, registration > 99%, refresh < 100ms, 99.9% uptime, hash < 500ms, conversion > 60%, > 1000 DAU)
12. **Rollback mechanism** — Feature-flag-based cutover with legacy auth kept alive until GA acceptance
13. **Open questions** — Both track OQ-001 through OQ-006 with similar dispositions
14. **Observability stack** — Same Prometheus metrics, OpenTelemetry tracing, Grafana dashboards, and alert thresholds

---

## 2. Divergence Points

### D-01: Phase 0 — Architecture Baseline Phase
- **Opus:** Jumps directly into Phase 1 (infrastructure + primitives). Architecture decisions are implicit in Phase 1 deliverables.
- **Haiku:** Inserts a dedicated **Phase 0** (3–5 working days) for ADRs, API contract freeze, and open-question triage before any implementation begins.
- **Impact:** Haiku's approach adds 3–5 days but reduces rework risk from ambiguous requirements. Opus's approach is faster to first code but assumes the team can resolve OQs in flight.

### D-02: Total Phase Count
- **Opus:** 4 phases (Phase 1–4, with Phase 4 subdivided into 4a/4b/4c for rollout).
- **Haiku:** 6 phases (Phase 0–5), with rollout as a fully separate Phase 5.
- **Impact:** Haiku's separation gives clearer milestone ownership. Opus bundles observability and rollout into one phase, which risks observability being shortchanged under rollout pressure.

### D-03: Total Timeline Estimate
- **Opus:** ~7–9 weeks.
- **Haiku:** ~9–11 weeks (adds Phase 0 and gives wider range estimates per phase).
- **Impact:** Haiku is ~2 weeks more conservative. The difference is primarily Phase 0 overhead and wider buffers on implementation phases (e.g., Phase 2 is "2 weeks" in Opus vs "1.5–2 weeks" in Haiku, but Haiku's Phase 1 scope is narrower since `UserRepo` moves to Phase 2).

### D-04: `UserRepo` Phase Assignment
- **Opus:** Implements `UserRepo` in **Phase 1** alongside security primitives.
- **Haiku:** Defers `UserRepo` to **Phase 2** alongside `AuthService` and the API surface.
- **Impact:** Opus's approach allows end-to-end unit testing of the data layer in Phase 1. Haiku treats `UserRepo` as a domain service rather than infrastructure, which is architecturally cleaner but means Phase 1 can't fully validate persistence flows.

### D-05: Rate Limiting Phase Assignment
- **Opus:** Implements rate limiting in **Phase 2** as middleware alongside API endpoints.
- **Haiku:** Defers API Gateway rate-limit configuration to **Phase 4** (operational readiness).
- **Impact:** Opus tests rate limits earlier in the pipeline. Haiku separates application-level lockout (Phase 2) from gateway-level rate limiting (Phase 4), which is a cleaner separation of concerns but means integration testing in Phase 2 won't cover gateway behavior.

### D-06: Integration Points Documentation Style
- **Opus:** Embeds integration/wiring tables **inline within each phase**, showing dispatch mechanisms as they're created.
- **Haiku:** Consolidates all integration points into a **dedicated Section 3** with categories (DI, middleware, frontend, feature flags, abstractions).
- **Impact:** Opus's approach is more actionable per-phase (developers see wiring in context). Haiku's approach provides a better cross-cutting reference for architects reviewing the full system topology.

### D-07: Security Review as Explicit Role
- **Opus:** Lists Backend, Frontend, QA, and DevOps/SRE roles. No explicit security review role.
- **Haiku:** Adds an explicit **Security review** role responsible for RS256 key lifecycle, token handling model, and brute-force/XSS controls.
- **Impact:** Haiku recognizes that security expertise is distinct from backend engineering for an auth system. Opus assumes backend engineers handle security concerns.

### D-08: Environment Readiness Gates
- **Opus:** Defines validation gates between phases as test-result criteria (e.g., "all unit tests pass, benchmark < 500ms").
- **Haiku:** Defines explicit **environment readiness gates** (e.g., "Before Phase 2: DB schema deployed, Redis available, key material loading tested") in addition to test-based gates.
- **Impact:** Haiku's gates catch infrastructure provisioning delays before they block development. Opus's gates are purely functional, which could miss environment readiness issues.

### D-09: Risk Treatment — Architect-Identified Risks
- **Opus:** Proactively identifies **three additional risks** not in the spec: R-004 (RSA key compromise), R-005 (Redis SPOF), R-006 (SendGrid outage).
- **Haiku:** Stays strictly within the three spec-defined risks (R-001, R-002, R-003) but provides deeper per-risk analysis with explicit "Roadmap controls" mapping risks to phase deliverables.
- **Impact:** Opus demonstrates broader threat awareness. Haiku provides more actionable risk-to-phase traceability for the risks it does cover.

### D-10: Observability as Separate Phase vs. Bundled
- **Opus:** Bundles observability setup, migration, deployment config, and rollout into a single **Phase 4**.
- **Haiku:** Separates observability/operational readiness (**Phase 4**) from migration/rollout (**Phase 5**).
- **Impact:** Haiku's separation ensures observability is validated before any production traffic. Opus's bundling risks observability instrumentation being incomplete when alpha traffic begins.

### D-11: Recommended Sequencing Decisions
- **Opus:** Does not include explicit sequencing recommendations — ordering is implicit in phase structure.
- **Haiku:** Includes a dedicated **Section 8** with five explicit sequencing constraints (e.g., "Do not start frontend token orchestration before `JwtService` is stable").
- **Impact:** Haiku's explicit constraints prevent common implementation missteps. Opus relies on phase dependencies being self-evident.

### D-12: Validation Structure
- **Opus:** Maps success criteria to a table with validation phase and method columns. Gates are between numbered phases.
- **Haiku:** Defines a four-stage validation framework (Stage A–D) that maps to milestones, with separate functional and NFR validation sections.
- **Impact:** Haiku's staged validation is more systematic and audit-friendly. Opus's table format is more compact and scannable.

---

## 3. Areas Where One Variant is Clearly Stronger

### Opus is stronger in:
- **Actionable detail per phase** — Each phase includes specific checklist items with requirement traceability (e.g., "— satisfies NFR-SEC-001, AC-003"). A developer can work directly from the roadmap.
- **Inline wiring tables** — Integration points shown in-context where they're built, reducing cross-referencing.
- **Proactive risk identification** — Three additional risks (R-004, R-005, R-006) beyond spec requirements show architectural maturity.
- **Parallelization opportunities** — Explicitly calls out what can be developed concurrently within and across phases.
- **Open questions with recommended defaults** — OQ table includes actionable fallback decisions, not just questions.

### Haiku is stronger in:
- **Phase 0 architecture freeze** — Prevents implementation starting before key decisions are locked. Critical for multi-team coordination.
- **Separation of observability from rollout** — Ensures monitoring is validated before production traffic begins.
- **Explicit security review role** — Recognizes auth systems need dedicated security oversight.
- **Environment readiness gates** — Catches infrastructure blockers before they stall development.
- **Sequencing constraints section** — Prevents common implementation ordering mistakes.
- **Cross-cutting integration reference** — Section 3's categorized wiring inventory is superior for architectural review.
- **Conservative timeline estimates** — Range-based estimates (e.g., "1.5–2 weeks") are more realistic for planning.

---

## 4. Areas Requiring Debate to Resolve

1. **Phase 0: Include or skip?** — Is the 3–5 day upfront architecture freeze worth the delay, or can OQs be resolved concurrently with Phase 1 implementation? Depends on team maturity and whether OQ-002/OQ-005/OQ-006 are truly blocking.

2. **`UserRepo` timing** — Should the repository layer land in Phase 1 (enabling earlier integration testing) or Phase 2 (cleaner architectural separation)? The answer depends on whether the team prioritizes early vertical integration or clean layering.

3. **Rate limiting phase** — Should gateway-level rate limiting be implemented alongside endpoints (Phase 2, Opus) or deferred to operational readiness (Phase 4, Haiku)? Early implementation catches rate-limit bugs in integration tests; deferred implementation separates concerns.

4. **Observability + rollout bundling** — Should observability and rollout be one phase (Opus) or two (Haiku)? A single phase is faster but risks observability gaps during alpha. Two phases add a week but guarantee monitoring is validated first.

5. **Timeline commitment** — 7–9 weeks (Opus) vs 9–11 weeks (Haiku). The team must decide whether to commit to an aggressive timeline or build in explicit buffers. The ~2-week gap is almost entirely Phase 0 + the observability/rollout split.

6. **Integration point documentation format** — Inline-per-phase (Opus) vs cross-cutting catalog (Haiku). Consider maintaining both: inline for developer execution, cross-cutting for architectural review. The merged roadmap should include both views.
