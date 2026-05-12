---
total_diff_points: 14
shared_assumptions_count: 18
---

# Comparative Diff Analysis: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Complexity rating** — Both assess MEDIUM (0.65)
2. **Stateless JWT with refresh tokens** — RS256, 2048-bit keys, 15-min access / 7-day refresh TTLs
3. **bcrypt cost factor 12** via PasswordHasher abstraction with future algorithm migration path
4. **Refresh tokens hashed in Redis** (not plaintext)
5. **Same 9 components** — COMP-001 through COMP-009 with identical responsibilities
6. **Same 6 API endpoints** — login, register, me, refresh, reset-request, reset-confirm
7. **Same 3 personas** — Alex (end user), Jordan (admin), Sam (API consumer)
8. **Same 3-phase migration** — Alpha → Beta 10% → GA 100% with feature flags AUTH_NEW_LOGIN and AUTH_TOKEN_REFRESH
9. **Same open questions** — OQ-1 through OQ-10 identified, with OQ-6/OQ-7/OQ-9 flagged as highest priority
10. **Same risk registry** — R-001 through R-007 with matching severity/probability ratings
11. **Same success criteria** — 10 quantitative metrics with identical targets
12. **Same external dependencies** — PostgreSQL 15+, Redis 7+, Node.js 20 LTS, bcryptjs, jsonwebtoken, SendGrid
13. **Same testing pyramid** — Unit (TEST-001–003), Integration (TEST-004–005), E2E (TEST-006 via Playwright)
14. **Same operational artifacts** — OPS-001 (AuthService Down), OPS-002 (Token Refresh Failures), OPS-003 (on-call rotation)
15. **Account lockout** — 5 failed attempts within 15 minutes
16. **Rate limiting structure** — 10/min login, 5/min register, 60/min me, 30/min refresh
17. **HPA scaling** — 3 baseline replicas, scale to 10 at CPU > 70%
18. **Rollback triggers** documented with similar thresholds

---

## 2. Divergence Points

### D-01: Phase Structure (5 phases vs 3 phases)

- **Opus:** 5 phases — Data Layer (1w) → Backend Services (2w) → API+Frontend (2w) → Testing+Compliance (2w) → Migration Rollout (4w). Total: **11 weeks**.
- **Haiku:** 3 phases — Backend Foundation (3w) → Frontend+Advanced Flows (3w) → Hardening+GA (3w). Total: **9 weeks**.
- **Impact:** Opus's finer granularity creates clearer exit criteria per phase but adds coordination overhead. Haiku's broader phases allow more intra-phase parallelism but have less precise checkpoints. Opus's 11-week timeline is more conservative; Haiku's 9-week is more aggressive but includes buffer recommendations of 2-3 additional weeks.

### D-02: Task Count (53 vs ~50 but differently structured)

- **Opus:** 53 explicitly numbered task rows across 5 phases with sequential IDs.
- **Haiku:** ~50 task rows across 3 phases, mixing functional requirements (FR-*) and NFR requirements directly into phase task tables.
- **Impact:** Opus treats requirements as already-resolved inputs that produce implementation tasks. Haiku embeds requirement rows alongside implementation tasks, which creates traceability but inflates the task list with non-implementable rows.

### D-03: Testing Phase Isolation

- **Opus:** Dedicates Phase 4 entirely to testing, security review, and compliance validation. Testing is a gated checkpoint before any migration begins.
- **Haiku:** Distributes testing across Phase 1 (unit tests) and Phase 2 (integration + E2E), with security review in Phase 3. No isolated testing phase.
- **Impact:** Opus's approach ensures comprehensive validation before any production exposure. Haiku's shift-left approach catches issues earlier but risks incomplete test coverage if Phase 2 runs behind schedule.

### D-04: Migration Rollout Duration

- **Opus:** 4 weeks dedicated to migration (Alpha 1w → Beta 2w → GA 1w), plus post-GA flag cleanup.
- **Haiku:** Migration embedded within phases — Alpha end of Phase 1 (week 3), Beta during Phase 2 (weeks 5-6), GA at Phase 3 end (week 9). No separate migration phase.
- **Impact:** Opus provides more soak time at each migration stage. Haiku overlaps migration with development, which is faster but riskier — a Phase 2 bug could affect beta users already on the new system.

### D-05: Audit Log Retention — Assumed Resolution

- **Opus:** Explicitly resolves OQ-6 in favor of PRD (12 months) and implements it in Phase 1 task NFR-COMP-002 with partition-based retention.
- **Haiku:** Flags OQ-6 as blocking Phase 2 but does **not** assume a resolution. Defers to stakeholder decision.
- **Impact:** Opus is execution-ready but makes an assumption that could be wrong. Haiku is more conservative but leaves Phase 1 schema design ambiguous.

### D-06: GDPR Consent Field — Implementation Timing

- **Opus:** Adds `consentTimestamp` to DM-001 (Phase 1, task #1) and creates a separate NFR-COMP-001 task (#3) for validation.
- **Haiku:** Lists OQ-9 as blocking Phase 2, recommends adding the field before Phase 1 ends, but doesn't include it in the Phase 1 DM-001 task definition.
- **Impact:** Opus avoids a schema migration mid-project. Haiku risks a Phase 1 rework if the field isn't added until the OQ is formally resolved.

### D-07: Logout Endpoint Treatment

- **Opus:** Identifies OQ-7 as blocking, recommends scoping it, but does **not** include a task for it.
- **Haiku:** Identifies OQ-7 and explicitly recommends implementing `POST /auth/logout` in Phase 2, while documenting the v1.0 debt of no backend session termination.
- **Impact:** Haiku provides a clearer path for the logout user story from PRD. Opus leaves a gap that could surface as a Phase 3 blocker.

### D-08: Team Sizing and FTE Estimates

- **Opus:** Provides a qualitative team allocation table (which team leads which phase) but no FTE counts.
- **Haiku:** Provides detailed FTE estimates — 6 FTE Phase 1, 11 FTE Phase 2, 7 FTE Phase 3. Total ~22 FTE-weeks with post-GA on-call. Also flags frontend-team availability as a critical-path staffing risk.
- **Impact:** Haiku's resource model enables budget planning and capacity conversations. Opus's omission requires follow-up estimation.

### D-09: Confidence Levels per Deliverable

- **Opus:** No per-deliverable confidence estimates.
- **Haiku:** Provides weekly confidence ratings (90% → 65%) with explicit buffer recommendations (1-2 weeks contingency).
- **Impact:** Haiku gives stakeholders a clearer picture of schedule risk. Opus's timeline reads as deterministic, which may create false certainty.

### D-10: Integration Points Documentation Style

- **Opus:** Provides per-phase "Integration Points" tables with Named Artifact, Type, Wired Components, Owning Phase, Consumed By columns. Very structured.
- **Haiku:** Documents integration points in a centralized "Architecture Integration Points" section with dependency injection strategy and error propagation patterns.
- **Impact:** Opus's distributed approach makes it easy to verify completeness phase-by-phase. Haiku's centralized approach provides better architectural overview but could miss phase-specific wiring gaps.

### D-11: Load Testing Scope

- **Opus:** Explicitly defines k6 load test (NFR-PERF-002) as 500 concurrent logins, p95 < 200ms, in Phase 4.
- **Haiku:** Defines same load test but spreads validation across Phase 2 beta (real traffic) and Phase 3 (formal validation).
- **Impact:** Opus tests in isolation before real users. Haiku validates with real traffic, which is more realistic but riskier.

### D-12: Revenue Impact Framing

- **Opus:** No mention of revenue or business impact in executive summary.
- **Haiku:** Opens with "$2.4M revenue impact" from Q2 2026 personalization roadmap, framing authentication as a business enabler.
- **Impact:** Haiku's framing is more compelling for executive stakeholders. Opus is more technically focused.

### D-13: Post-GA Monitoring and Retrospective

- **Opus:** Mentions alerting rules and feature flag cleanup but no formal post-launch review cadence.
- **Haiku:** Defines daily/weekly/monthly/quarterly monitoring cadence and explicitly schedules a post-launch retrospective.
- **Impact:** Haiku's operational maturity model is more complete for handoff to support teams.

### D-14: Architectural Debt Acknowledgment

- **Opus:** Implicitly carries debt (no logout, no admin query API) but doesn't call it out as such.
- **Haiku:** Explicitly lists "Architectural Debt Incurred" — no logout endpoint, no admin audit query API, no social login/MFA — with v1.1 deferral plan.
- **Impact:** Haiku's transparency reduces surprise scope requests post-GA and sets clearer v1.1 expectations.

---

## 3. Areas Where One Variant is Clearly Stronger

### Opus is stronger in:

| Area | Why |
|------|-----|
| **Phase granularity** | 5 phases with explicit entry/exit criteria per phase make go/no-go decisions clearer |
| **Task-level precision** | 53 sequentially numbered tasks with explicit dependency chains; easier to convert to sprint backlog |
| **Integration wiring tables** | Per-phase artifact tables make dependency verification auditable |
| **Testing isolation** | Dedicated Phase 4 prevents "testing gets squeezed" syndrome |
| **Schema completeness** | Resolves OQ-6 and OQ-9 proactively in Phase 1, avoiding rework |

### Haiku is stronger in:

| Area | Why |
|------|-----|
| **Stakeholder communication** | Revenue framing, FTE estimates, confidence ratings, and buffer recommendations |
| **Resource planning** | Detailed FTE-per-phase breakdown enables capacity and budget conversations |
| **Risk management** | Confidence levels per week surface schedule risk honestly |
| **Operational maturity** | Post-GA monitoring cadence (daily/weekly/monthly/quarterly) plus scheduled retrospective |
| **Debt transparency** | Explicit "Architectural Debt Incurred" section sets v1.1 expectations |
| **Logout endpoint** | Acknowledges PRD gap and provides a concrete recommendation |
| **Timeline aggressiveness** | 9 weeks (with buffers to ~11-12) vs Opus's flat 11 weeks — more ambitious but pragmatic |

---

## 4. Areas Requiring Debate to Resolve

| # | Topic | Opus Position | Haiku Position | Resolution Criteria |
|---|-------|---------------|----------------|---------------------|
| 1 | **Phase count** | 5 fine-grained phases | 3 broad phases | Team size and coordination overhead. Smaller teams benefit from fewer phases; larger teams benefit from tighter gates. |
| 2 | **Testing phase isolation vs shift-left** | Dedicated Phase 4 testing gate | Testing distributed across Phases 1-2 | Historical defect escape rate. If the team has strong TDD discipline, shift-left works. If not, a testing gate is safer. |
| 3 | **OQ-6 resolution timing** | Assume PRD wins (12 months), implement in Phase 1 | Leave unresolved, block Phase 2 | Stakeholder availability. If compliance team can decide within a week, Opus's assumption is safe. If not, Haiku's gate is prudent. |
| 4 | **Migration overlap with development** | Strict sequential: all dev done → then migrate | Migration phases overlap with development | Risk appetite. Overlapping is faster but means beta users hit unfinished features. |
| 5 | **FTE estimates in roadmap** | Omitted (defer to project planning) | Included (22 FTE-weeks) | Audience. If the roadmap feeds directly into resource allocation, include them. If it feeds into a separate capacity planning process, omit. |
| 6 | **Confidence ratings** | Not included | Per-week confidence (90% → 65%) | Organizational culture. Teams comfortable with uncertainty benefit from transparency. Teams prone to scope cuts under pressure may use low confidence as justification to cut corners. |
| 7 | **Logout endpoint scope** | Flag as open question only | Recommend Phase 2 implementation | PRD commitment level. If the logout user story is in v1.0 scope, it must be tasked. If it's aspirational, deferral is acceptable. |
