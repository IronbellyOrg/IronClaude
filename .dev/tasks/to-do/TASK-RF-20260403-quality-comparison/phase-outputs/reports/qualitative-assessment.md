# Qualitative Assessment -- Pipeline Input Configuration Comparison

**Date:** 2026-04-03
**Runs Assessed:**
- Run A: `test3-spec-baseline/` (spec only)
- Run B: `test2-spec-prd-v2/` (spec + PRD)
- Run C: `test1-tdd-prd-v2/` (TDD + PRD)

---

## 3.1 Roadmap Qualitative Comparison

### Methodology

Each roadmap was read in full and assessed across four dimensions: milestone ordering, deliverable specificity, business alignment, and risk treatment. Ratings: Weak / Adequate / Strong.

### 3.1.1 Milestone Ordering

**Run A (Spec Baseline) -- Strong**

Run A follows a clean 5-phase linear progression: Foundation (schema + crypto) -> Core Auth Logic (services) -> Integration Layer (routes + middleware) -> Hardening -> Production Readiness. The ordering is driven by technical dependency: "Everything in later phases depends on this layer" (Phase 1 goal). The separation of `PasswordHasher` and `JwtService` from `TokenManager` and `AuthService` is architecturally sound -- no phase references components not yet built. Phases 4 and 5 overlap ("Week 6, overlapping with Phase 4"), which is realistic.

**Run B (Spec + PRD) -- Strong**

Run B uses a 4-phase structure: Foundation & Infrastructure -> Core Authentication -> Profile & Password Reset -> Hardening & Launch. The critical path is explicitly documented: "Infrastructure provisioning -> PasswordHasher + JwtService -> AuthService (login/registration) -> TokenManager (refresh rotation) -> Password reset with email integration -> Compliance hardening." The decision to defer profile and password reset to Phase 3 is justified by epic alignment ("AUTH-E3"). A visual timeline with ASCII art provides clear phase overlap visualization (Section 6).

**Run C (TDD + PRD) -- Strong**

Run C uses a 3-phase structure: Core Authentication Internal Alpha (Weeks 1-2) -> Password Reset, Compliance, and Beta (Weeks 3-4) -> GA Rollout and Stabilization (Weeks 5-6). This is the most aggressive timeline at 6 weeks vs. Run A's 5-6 weeks and Run B's 10 weeks. The phasing merges "the operational completeness of the Haiku Architect variant... with the phasing discipline of the Opus Architect variant." The decision to pack all backend components plus frontend into Phase 1 is ambitious but documented as a deliberate trade-off.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Strong | Clean 5-phase dependency chain; realistic overlaps |
| B   | Strong | 4-phase with explicit critical path; visual timeline |
| C   | Strong | Compressed 3-phase with progressive rollout (alpha -> beta 10% -> GA) |

### 3.1.2 Deliverable Specificity

**Run A (Spec Baseline) -- Strong**

Deliverables are organized in task tables with explicit columns for "Requirements Covered" and "Details." Example: Task "Implement `TokenManager` class" specifies methods: "`issueTokenPair(userId)`, `refreshTokens(refreshToken)`, `revokeAllForUser(userId)`" and explicitly addresses "Refresh token rotation with replay detection" with the detail "On reuse of revoked token: revoke ALL tokens for user." Each phase has numbered sub-sections (e.g., 1.1 through 1.5) with granular task-level specifications.

**Run B (Spec + PRD) -- Strong**

Deliverables include effort estimates and ownership: "Effort: 3 days | Owner: Backend." Each deliverable references specific FR/NFR IDs and debate resolution IDs (e.g., "debate-resolved D3 -- SHA-256 is appropriate for randomly-generated tokens"). Integration points are documented as wiring tables with Named Artifact, Type, Wired Components, Owning Phase, and Consumed By columns. The addition of persona alignment ("Alex persona: registration completes in under 60 seconds") grounds deliverables in user outcomes.

**Run C (TDD + PRD) -- Strong**

Deliverables are the most technically specific, referencing component names from the TDD directly: "`AuthService`, `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo`." API endpoint tables include rate limits per endpoint (e.g., "login: 10/min/IP, register: 5/min/IP, refresh: 30/min/user"). Wiring tasks are called out explicitly (e.g., "Wiring Task 1.2.1: AuthService Facade Dispatch" with mechanism, wired components, and cross-references). The level of implementation detail exceeds both other runs.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Strong | Method signatures, explicit requirement coverage per task |
| B   | Strong | Effort estimates, persona alignment, debate resolution traceability |
| C   | Strong | Component-level wiring tasks, per-endpoint rate limits, implementation mechanisms |

### 3.1.3 Business Alignment

**Run A (Spec Baseline) -- Adequate**

Run A is a purely technical roadmap. There is no mention of business value, revenue impact, personas, or PRD-derived success metrics. The "Executive Summary" references "five core capabilities" and the "key architectural decisions" but frames everything in engineering terms. Success criteria (SC-1 through SC-9) are all technical validations -- no business KPIs like conversion rate or session duration. This is expected given spec-only input, but it limits stakeholder communication value.

**Run B (Spec + PRD) -- Strong**

Run B opens with business context: "$2.4M projected annual revenue impact" and "Q3 2026 SOC2 Type II audit deadline." Success criteria include both technical launch blockers (S1: p95 < 200ms, S7: E2E lifecycle) and business metrics (S3: "> 60% registration conversion rate," S6: "> 80% password reset completion rate"). Persona references appear throughout deliverables ("Alex persona: registration completes in under 60 seconds"). The scope guardrails section (Section 8) links exclusions to PRD Section S12.

**Run C (TDD + PRD) -- Strong**

Run C matches Run B on business alignment, citing the same "$2.4M projected annual revenue" and SOC2 deadline. It goes further on operational detail: alert thresholds with specific actions ("auth_login_duration_seconds p95 > 500ms -> Page on-call, investigate"), automatic rollback triggers ("p95 latency > 1000ms for > 5 minutes"), and cost estimates ("SendGrid ~$100/month at scale"). The persona coverage matrix (Section final) explicitly tracks coverage vs. gaps for Alex, Jordan, and Sam.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Adequate | Technically complete but zero business context or KPIs |
| B   | Strong | Revenue impact, compliance deadlines, persona-grounded metrics |
| C   | Strong | Same business context plus operational cost estimates and alert thresholds |

### 3.1.4 Risk Treatment

**Run A (Spec Baseline) -- Strong**

Six risks documented with Severity, Probability, Phase Addressed, Mitigation Strategy, and Residual Risk columns. The residual risk column is notable -- e.g., RISK-1 residual: "Key rotation gap window (max 90 days); compromised secrets manager." RISK-4 (email dependency) acknowledges "no fallback in spec" as a known gap. Risk-to-phase mapping is explicit.

**Run B (Spec + PRD) -- Strong**

Nine risks with validation methods: "Phase 4: adversarial replay test in pentest" for R2. The risk sequencing rationale is explicitly documented: "R1, R2, and R6 are addressed early (Phases 1-2) because they are structural -- retrofitting security primitives and audit logging is far more expensive than building them in." Post-launch monitoring thresholds are tied to risks (e.g., "p95 latency > 250ms -> early warning before SLA breach"). The compressed timeline alternative (Section 6) explicitly addresses schedule risk.

**Run C (TDD + PRD) -- Strong**

Seven risks split across Technical, Business/Product, and Architectural categories. Unique additions include R-003 (data loss during migration: "Parallel run during Phase 1-2. Idempotent upsert operations"), R-004 (low registration UX: "Extend beta by 1 week if conversion < 40%"), and architectural risks (Redis SPOF: "graceful degradation -- users re-login if unavailable"). The Risk Mitigation Roadmap section provides a temporal sequencing across Immediate, Pre-Beta, and Pre-GA stages.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Strong | Residual risk tracking; honest "no fallback" acknowledgment |
| B   | Strong | Risk sequencing rationale; monitoring thresholds tied to risks |
| C   | Strong | Three-category taxonomy; migration risk and UX risk unique additions |

---

## 3.2 Tasklist Qualitative Comparison (Run A vs Run C)

**Run B: N/A** -- No tasklist artifacts were produced in the spec+PRD run.

### Methodology

Compared `tasklist-index.md` and `phase-1-tasklist.md` from Runs A and C. Assessed: task specificity, decomposition quality, coverage, and enrichment integration. Representative tasks quoted below.

### 3.2.1 Task Specificity

**Run A (Spec Baseline)**

Tasks follow a consistent format with Effort, Risk, Risk Drivers, Tier, Confidence, and Critical Path Override fields. Steps use phase tags like `[PLANNING]`, `[EXECUTION]`, `[VERIFICATION]`. Example task T01.01:

> "Migration file creating `users` table with columns: id (UUID v4 PK), email (unique index), display_name, password_hash, is_locked (boolean default false), created_at, updated_at"

Acceptance criteria are concrete and testable: "Migration is idempotent (running up twice does not error)." Validation includes both manual checks ("Run `\d users` in psql") and CI evidence.

**Run C (TDD + PRD)**

Tasks include all Run A fields plus: Requires Confirmation, MCP Requirements, Fallback Allowed, Sub-Agent Delegation, and Artifacts (Intended Paths). Example task T01.01:

> "PostgreSQL 15+ instance with `UserProfile` table (id, email, displayName, createdAt, updatedAt, lastLoginAt, roles, consent_given, consent_timestamp, password_hash)"

Note the schema is significantly richer -- 10 columns vs Run A's 7, including GDPR fields. The "Why" field provides architectural justification: "Database is the foundation for all user data persistence. GDPR consent fields (GAP-004) and 12-month audit retention (GAP-001) must be configured from Day 1."

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Strong | Clean structure, testable acceptance criteria, psql validation commands |
| C   | Strong | All of Run A's qualities plus MCP requirements, sub-agent delegation, artifact paths |

### 3.2.2 Decomposition Quality

**Run A:** 87 tasks across 5 phases. Phase 1 has 16 tasks focused purely on foundation (schema, crypto, DI). The decomposition is fine-grained -- separate tasks for `users` table migration (T01.01), `refresh_tokens` table migration (T01.02), and migration reversibility verification (T01.03). This is appropriate granularity for a STRICT-tier workflow.

**Run C:** 44 tasks across 3 phases. Phase 1 has 27 tasks covering infrastructure, backend, frontend, API gateway, monitoring, and security review -- essentially merging what Run A spreads across Phases 1-3. The task-per-roadmap-item ratio is closer to 1:1. Run C's T01.01 combines both the users table and the audit log table into a single task with two deliverables (D-0001, D-0002), whereas Run A separates them.

Representative decomposition comparison for the same logical work:

**Run A (3 separate tasks):**
- T01.01: Create users table migration (M effort)
- T01.02: Create refresh_tokens table migration (M effort)
- T01.03: Verify all migrations are reversible (S effort)

**Run C (1 combined task):**
- T01.01: Provision PostgreSQL with UserProfile Schema and GDPR Fields (L effort) -- produces D-0001 (UserProfile table) and D-0002 (Audit log table)

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Strong | Finer granularity; each task is atomic and independently testable |
| C   | Adequate | Coarser grouping; some tasks bundle multiple concerns (infra + schema + compliance in one) |

### 3.2.3 Coverage

**Run A:** 87 tasks cover all 5 spec-derived phases. Tier distribution: 55% STRICT, 31% STANDARD, 14% EXEMPT, 0% LIGHT. The high STRICT percentage reflects the security-critical nature of auth. No frontend tasks exist (spec-only input has no frontend requirements).

**Run C:** 44 tasks cover 3 phases plus produce 52 deliverables. Tier distribution: Phase 1 alone has "STRICT: 12, STANDARD: 10, LIGHT: 2, EXEMPT: 3." Coverage extends to frontend (LoginPage, RegisterPage, AuthProvider, ProfilePage), monitoring (Prometheus metrics, Grafana dashboards), and operational readiness (runbooks, on-call rotation). The broader coverage reflects the TDD+PRD input providing frontend component specifications and operational requirements.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Adequate | Thorough backend coverage; no frontend or ops tasks (input limitation) |
| C   | Strong | Full-stack coverage: backend, frontend, monitoring, compliance, operational readiness |

### 3.2.4 Enrichment Integration

**Run A:** Tasks reference spec requirement IDs (FR-AUTH.*, NFR-AUTH.*, SC-*) consistently. No persona references, no business metrics, no compliance callouts beyond what the spec provides. The Deliverable Registry maps R-### to D-#### but without PRD traceability.

**Run C:** Tasks reference both TDD sections ("Review TDD $7 Data Models") and PRD requirements ("PRD S17 for GDPR consent requirements"). Persona references appear in acceptance criteria: "per PRD persona Alex's registration journey." Gap resolutions are tracked per-task: "resolves GAP-004," "resolves GAP-001." The traceability matrix includes confidence scores per roadmap item (ranging from 65% to 95%). The Roadmap Item Registry provides a 20-word summary per item for quick scanning.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Adequate | Spec-only traceability; no enrichment beyond spec IDs |
| C   | Strong | Dual-source traceability (TDD + PRD), persona references, gap resolution tracking, confidence scores |

---

## 3.3 Extraction Qualitative Comparison

### Methodology

Read `extraction.md` from all three runs. Assessed: breadth (concern areas covered), depth (detail per area), and enrichment fidelity (how well PRD/TDD content was integrated).

### 3.3.1 Breadth (Concern Areas)

**Run A (Spec Baseline)**

Frontmatter: `domains_detected: [backend, security]`. Covers 7 sections: Functional Requirements (5 FRs + 5 implicit FRs), Non-Functional Requirements (3 NFRs + 4 implicit NFRs), Complexity Assessment, Architectural Constraints (10 items), Risk Inventory (4 risks), Dependency Inventory, Success Criteria (9 items), and Open Questions (10 items including 5 gaps). Two domains only -- no frontend, infrastructure, or compliance domains detected.

**Run B (Spec + PRD)**

Frontmatter: `domains_detected: [backend, security, frontend, infrastructure]`. Same core sections as Run A but with 6 NFRs (3 PRD-derived additions: GDPR consent, SOC2 audit logging, GDPR data minimization), 7 risks (added: low registration UX, security breach, compliance failure, email delivery), and 7 success criteria blending technical and business metrics. Eight open questions including PRD-derived items (OQ-4: "remember me," OQ-7: headless auth, OQ-8: Jordan admin persona).

**Run C (TDD + PRD)**

Frontmatter: `domains_detected: [backend, security, frontend, testing, devops]`. Five domains -- the broadest coverage. Adds three entirely new sections not present in Runs A or B: Data Models and Interfaces (with TypeScript interface definitions and field-level constraint tables), API Specifications (6 endpoints with request/response schemas and error code tables), Component Inventory (9 components split backend/frontend with dependency graphs), Testing Strategy (test pyramid with coverage targets), Migration and Rollout Plan (3-phase with feature flags and rollback criteria), and Operational Readiness (runbook scenarios, on-call expectations, capacity planning, observability). Total requirements: 13 (vs. 8 for Run A, 11 for Run B).

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Adequate | Core requirements well-extracted; limited to spec's own scope |
| B   | Strong | PRD enrichment adds compliance, personas, business risks |
| C   | Strong | Most comprehensive -- adds data models, API specs, component inventory, testing strategy, operational readiness |

### 3.3.2 Depth (Detail per Area)

**Run A:** Functional requirements include acceptance criteria with specific HTTP codes and behaviors. Example from FR-AUTH.3: "FR-AUTH.3c: Given a previously-rotated (revoked) refresh token, invalidate all tokens for that user (replay detection)." Risks include residual risk assessment. Open questions include recommendations with rationale.

**Run B:** Adds per-requirement complexity assessment ("Complexity: High -- token rotation with replay detection is the most complex auth flow") and PRD trace ("PRD Trace: FR-AUTH.3 (PRD), AUTH-E2 epic, Sam persona token refresh story"). Compliance requirements have explicit source attribution: "Note: Not present in spec; surfaced from PRD Section S17." This provenance tracking is unique to Run B.

**Run C:** The deepest detail. Data models include TypeScript interfaces with field constraints: "`email: string; // unique, indexed, lowercase normalized`." API specifications include error response formats with error codes: "`AUTH_INVALID_CREDENTIALS`." The testing strategy section provides a test pyramid with specific coverage targets: "Unit: 80%, Integration: 15%, E2E: 5%." Operational readiness includes runbook scenarios with symptoms, diagnosis, resolution, escalation, and prevention for each failure mode.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Adequate | Solid requirement detail; gaps in operational and testing depth |
| B   | Strong | Provenance tracking for PRD-derived items; complexity per requirement |
| C   | Strong | Implementation-ready detail: TypeScript interfaces, error codes, runbook scenarios |

### 3.3.3 Enrichment Fidelity

**Run A:** No enrichment source -- spec only. All content is faithfully extracted from the spec with clear distinction between explicit requirements and "Implicit Functional Requirements" (e.g., "FR-AUTH.1-IMPL-1 (from Evidence table)"). The implicit requirements section is a strength -- it surfaces requirements buried in non-requirement sections of the spec.

**Run B:** PRD enrichment is clean and well-attributed. Three new NFRs are explicitly marked: "NFR-AUTH.4: GDPR Registration Consent (PRD-derived)" with "Note: Not present in spec; surfaced from PRD Section S17." Success criteria blend spec and PRD sources with explicit source columns. The open questions section merges spec and PRD questions with clear ownership. No fabrication detected -- all PRD references map to actual PRD content.

**Run C:** TDD + PRD enrichment is the most aggressive. Five extraction-identified gaps (GAP-001 through GAP-005) show genuine conflicts between TDD and PRD: "GAP-001: Audit log retention conflict: TDD specifies 90-day retention (Section 7.2); PRD requires 12-month retention for SOC2 (Section S17). PRD wins on compliance intent." The JTBD Coverage Gaps section maps Jobs-to-be-Done to functional requirements with gap identification. Component names from the TDD are preserved throughout ("`AuthService`," "`TokenManager`"), maintaining implementation-level fidelity.

| Run | Rating | Notes |
|-----|--------|-------|
| A   | Adequate | Faithful spec extraction; good implicit requirement surfacing |
| B   | Strong | Clean PRD attribution; no fabrication; provenance tracking |
| C   | Strong | Cross-document conflict resolution (GAP-001); JTBD mapping; component-level fidelity |

---

## 3.4 Overall Qualitative Ranking

### Per-Artifact Rankings (1 = best)

#### Roadmap

| Dimension | Run A (Spec) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|-----------|:---:|:---:|:---:|
| Milestone Ordering | 2 | 1 | 1 |
| Deliverable Specificity | 3 | 2 | 1 |
| Business Alignment | 3 | 1 | 1 |
| Risk Treatment | 2 | 1 | 1 |
| **Overall Roadmap** | **3** | **2** | **1** |

**Rationale:** Run C edges out Run B on deliverable specificity due to component-level wiring tasks and per-endpoint rate limit tables. Run B and Run C tie on business alignment and risk treatment. Run A is technically sound but lacks the business context that PRD enrichment provides.

> **Ranking note:** Where multiple runs share the same text rating (e.g., all "Strong"), the per-dimension rank reflects relative advantage within that tier as documented in the sub-section narratives. For Milestone Ordering, Runs B and C earn rank 1 for explicit critical path documentation (Run B) and progressive rollout strategy (Run C); Run A's ordering is sound but less explicitly justified. For Risk Treatment, Runs B and C earn rank 1 for validation methods, risk sequencing rationale (Run B), and multi-category taxonomy with migration/UX risk additions (Run C).

#### Tasklist

| Dimension | Run A (Spec) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|-----------|:---:|:---:|:---:|
| Task Specificity | 1 | N/A | 1 |
| Decomposition Quality | 1 | N/A | 2 |
| Coverage | 2 | N/A | 1 |
| Enrichment Integration | 2 | N/A | 1 |
| **Overall Tasklist** | **2** | **N/A** | **1** |

**Rationale:** Run C's broader coverage (frontend, ops, monitoring) and enrichment integration (persona references, gap tracking, confidence scores) give it the edge despite coarser decomposition. Run A's finer granularity (87 tasks vs. 44) is a strength for execution but reflects a narrower scope (no frontend or ops).

#### Extraction

| Dimension | Run A (Spec) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|-----------|:---:|:---:|:---:|
| Breadth | 3 | 2 | 1 |
| Depth | 3 | 2 | 1 |
| Enrichment Fidelity | 3 | 1 | 1 |
| **Overall Extraction** | **3** | **2** | **1** |

**Rationale:** Run C extracts the most content from the richest input source. The TDD provides data models, API specs, component inventories, and operational readiness details that neither the spec nor the spec+PRD combination can match. Run B's enrichment fidelity ties with Run C due to its clean provenance tracking.

### Aggregate Summary

| Artifact | 1st Place | 2nd Place | 3rd Place |
|----------|-----------|-----------|-----------|
| Roadmap | Run C (TDD+PRD) | Run B (Spec+PRD) | Run A (Spec) |
| Tasklist | Run C (TDD+PRD) | Run A (Spec) | Run B (N/A) |
| Extraction | Run C (TDD+PRD) | Run B (Spec+PRD) | Run A (Spec) |

### Narrative Summary

The TDD+PRD input configuration (Run C) consistently produces the highest-quality artifacts across all three artifact types. The technical design document provides implementation-level detail (component names, data models, API specifications, deployment strategy) that directly translates into more specific roadmap deliverables, richer extraction content, and broader tasklist coverage. The PRD adds business alignment, persona grounding, and compliance requirements that elevate both Run B and Run C above the spec-only baseline.

Run B (Spec+PRD) occupies a clear middle ground. The PRD enrichment adds substantial value -- particularly in business alignment (revenue impact, conversion metrics), risk treatment (UX and compliance risks), and extraction breadth (compliance NFRs). However, without the TDD's implementation-level detail, Run B cannot match Run C's deliverable specificity or extraction depth.

Run A (Spec Baseline) demonstrates that a well-written spec alone can produce a technically sound roadmap with strong milestone ordering and risk treatment. Its primary limitation is the absence of business context and the narrower scope that results from having only a single input source. Notably, Run A's tasklist has the finest granularity (87 tasks), suggesting that the pipeline's decomposition algorithm works well even without enrichment -- it simply has less content to decompose.

The key finding is that **input richness compounds**: each additional input source (PRD atop spec, TDD atop PRD) adds value that is reflected across all downstream artifacts, not just the artifact most directly informed by that source.
