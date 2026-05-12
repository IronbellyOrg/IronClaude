# R04: Existing Roadmap Artifacts

- **Status**: Complete
- **Researcher**: r04
- **Track**: tasklist-e2e
- **Date**: 2026-04-02

## Scope

Analysis of existing roadmap outputs in:
- `.dev/test-fixtures/results/test1-tdd-prd/`
- `.dev/test-fixtures/results/test2-spec-prd/`

Focus: What do the roadmaps contain? What will the tasklist generator consume? What content should appear in generated tasklists?

---

## 1. Directory Inventory

Both directories contain identical file sets (same pipeline, different inputs):

| File | test1 Size | test2 Size | Purpose |
|------|-----------|-----------|---------|
| `.roadmap-state.json` | 3.3 KB | 3.3 KB | Pipeline state tracker |
| `extraction.md` | 28.9 KB | 14.7 KB | Requirements extraction |
| `roadmap-opus-architect.md` | 21.9 KB | 21.2 KB | Opus variant roadmap |
| `roadmap-haiku-architect.md` | 43.5 KB | 27.2 KB | Haiku variant roadmap |
| `diff-analysis.md` | 11.3 KB | 10.3 KB | Variant comparison |
| `debate-transcript.md` | 19.3 KB | 18.8 KB | Adversarial debate |
| `base-selection.md` | 12.8 KB | 8.5 KB | Variant scoring |
| `roadmap.md` | **32.6 KB (523 lines)** | **27.7 KB (330 lines)** | **Final merged roadmap** |
| `anti-instinct-audit.md` | 1.2 KB | 1.0 KB | Anti-instinct check (FAIL) |
| `wiring-verification.md` | 3.1 KB | 3.1 KB | Codebase wiring scan |
| `tasklist-fidelity.md` | 4.2 KB | 0.9 KB | Fidelity check (NO TASKLIST) |
| `*.err` files | 0 bytes each | 0 bytes each | Stderr capture (all empty) |

**Key observation**: Both `tasklist-fidelity.md` files confirm `tasklist_ready: false` and `downstream_file: "[NO TASKLIST GENERATED]"`. This is the gap the task file must close.

---

## 2. State JSON Analysis

### test1-tdd-prd `.roadmap-state.json`

| Field | Value |
|-------|-------|
| `input_type` | `"tdd"` |
| `spec_file` | `test-tdd-user-auth.md` |
| `prd_file` | `test-prd-user-auth.md` |
| `tdd_file` | `null` |
| Pipeline steps | extract, generate-opus-architect, generate-haiku-architect, diff, debate, score, merge, anti-instinct, wiring-verification |
| All steps PASS? | All PASS except `anti-instinct` (FAIL) |
| Final output | `roadmap.md` |

### test2-spec-prd `.roadmap-state.json`

| Field | Value |
|-------|-------|
| `input_type` | `"spec"` |
| `spec_file` | `test-spec-user-auth.md` |
| `prd_file` | `test-prd-user-auth.md` |
| `tdd_file` | `null` |
| Pipeline steps | Same as test1 |
| All steps PASS? | All PASS except `anti-instinct` (FAIL) |
| Final output | `roadmap.md` |

**Critical distinction**: test1 uses `input_type: "tdd"` (Technical Design Document as primary spec), test2 uses `input_type: "spec"` (generic specification). Both pair with the same PRD. The `tdd_file` field is null in both -- the `spec_file` field holds the TDD/spec path regardless of type.

---

## 3. Roadmap Content Analysis

### test1-tdd-prd/roadmap.md (523 lines, TDD+PRD input)

**Frontmatter fields**: `spec_source`, `complexity_score` (0.55), `adversarial` (true), `base_variant` ("Haiku (Variant B)"), `variant_scores` ("A:71 B:81"), `convergence_score` (0.72), `debate_rounds` (2), `prd_source`

**Structure: 4 phases**
- Phase 0: Design and Foundation (Weeks 1-2) -- architecture review, OQ resolution, infra setup, compliance
- Phase 1: Core Auth, Registration, Token Lifecycle (Weeks 3-7) -- FR-AUTH-001 through FR-AUTH-004
- Phase 2: Password Reset, Audit Logging, Observability (Weeks 8-10) -- FR-AUTH-005, compliance
- Phase 3: Production GA and Stabilization (Weeks 10.5-12.5) -- beta, GA, deprecation

**TDD-specific content present**:
- 5 backend components with exact names: `AuthService`, `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo`
- 4 frontend components: `LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider`
- Data models: `UserProfile` (7 fields), `AuthToken` (4 fields)
- 6 API endpoints: `POST /v1/auth/login`, `POST /v1/auth/register`, `GET /v1/auth/me`, `POST /v1/auth/refresh`, `POST /v1/auth/reset-request`, `POST /v1/auth/reset-confirm`
- Test artifacts: UT-001, UT-002, UT-003, IT-001, IT-002, E2E-001
- Migration plan: 3-phase rollout (Alpha -> Beta 10% -> GA 100%)
- Feature flags: `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH`
- Rate limiting table: 6 endpoint-specific limits
- Library dependencies: bcryptjs, jsonwebtoken, Jest, Supertest, testcontainers, Playwright, k6
- Infrastructure: PostgreSQL 15+, Redis 7+ (1 GB), Kubernetes (3 replicas, HPA to 10)
- OQ resolution table: OQ-001 through OQ-008 resolved

**PRD-specific content present**:
- Business drivers: $2.4M revenue, SOC2 Q3 2026, 25% churn reduction
- 3 personas: Alex (end user), Sam (API consumer), Jordan (admin)
- 10 success criteria with numeric targets (login p95 < 200ms, conversion > 60%, DAU > 1000, session > 30 min, etc.)
- Compliance mandates: NFR-COMP-001 through NFR-COMP-004 (GDPR, SOC2, NIST, data minimization)
- Rollback criteria: 4 conditions (latency > 1000ms, error > 5%, Redis failures > 10/min, data loss)
- Risk table: R-001 through R-007 with severity/probability/impact/mitigation/contingency

**Key sections for tasklist consumption**:
- Phase-by-phase task breakdowns with week-by-week granularity
- Exit criteria per phase (explicit checklists)
- Integration Points and Dispatch Mechanisms section
- Feature Flag Registry table
- Rate Limiting Configuration table

### test2-spec-prd/roadmap.md (330 lines, Spec+PRD input)

**Frontmatter fields**: `spec_source`, `complexity_score` (0.6), `adversarial` (true), `base_variant` ("B (Haiku Architect)"), `convergence_score` (0.72), `debate_rounds` (2)

**Structure: 2 phases + buffer**
- Phase 1: Authentication Core (Weeks 1-4) -- 3 milestones (M1, M2, M3)
- Phase 2: Recovery, Compliance, and Hardening (Weeks 5-7) -- 3 milestones (M4, M5, M6)
- Buffer (Weeks 8-10)

**Spec-specific content present**:
- Milestone-based structure (M1-M6) with task tables (Task 1.1, 1.2, etc.)
- Each task row has: Task, Requirement ID, Details
- Integration Points tables per phase with Named Artifact, Type, Wired Components, Owning Phase, Consumed By
- Explicit dependency gates (e.g., "Frontend routing framework (D8) must be available by Week 3")
- Requirement IDs use dot notation: FR-AUTH.1, FR-AUTH.2 (vs test1's dash notation FR-AUTH-001)
- Components: same names but described differently
- OQ resolution table: OQ1 through OQ9 (one more than test1)
- Scope Guardrails section (explicitly lists out-of-scope items)
- Persona Coverage table mapping personas to requirements and phases

**PRD-specific content present**:
- Same business drivers ($2.4M, SOC2 Q3 2026)
- Same personas (Alex, Sam, Jordan) but with different coverage table format
- Success criteria: 7 criteria (fewer than test1's 10)
- Compliance conflict resolution noted (spec defers audit to v1.1, PRD requires for SOC2)
- Risk table: R1-R7 (similar but formatted differently)
- Team composition table with FTE breakdown per phase

**Structural differences from test1**:
- 2 phases vs 4 phases
- Uses milestone numbering (M1-M6) within phases
- Task tables with structured columns vs narrative task lists
- 330 lines vs 523 lines (shorter, more structured)
- No Phase 0 (design baked into Phase 1 M1)
- No Phase 3 (GA/stabilization in buffer)

---

## 4. What the Tasklist Generator Must Consume

Based on both roadmaps, the tasklist generator needs to parse:

### From `roadmap.md`:
1. **Frontmatter** -- `spec_source`, `prd_source`, `complexity_score`, `adversarial`, `base_variant`
2. **Phase structure** -- Phase headers with objectives and week ranges
3. **Task items** -- Either narrative bullet lists (test1) or structured tables (test2)
4. **Requirement IDs** -- FR-AUTH-001/FR-AUTH.1 style references
5. **Component names** -- AuthService, PasswordHasher, TokenManager, etc.
6. **Exit criteria** -- Per-phase validation gates
7. **Risk items** -- R-001 through R-007
8. **Success criteria** -- Numbered metrics with targets
9. **Integration points** -- Named artifacts with wiring

### From `.roadmap-state.json`:
1. `input_type` -- determines which enrichment to expect (TDD vs spec)
2. `spec_file` / `prd_file` -- for traceability back to source documents
3. Step statuses -- confirms merge step completed successfully

---

## 5. Verification Content for E2E Tests

### What to grep for in generated tasklists to verify TDD enrichment flowed through (test1):

| Category | Grep Pattern | Rationale |
|----------|-------------|-----------|
| Components | `AuthService`, `PasswordHasher`, `TokenManager`, `JwtService`, `UserRepo` | TDD component inventory |
| Frontend | `LoginPage`, `RegisterPage`, `ProfilePage`, `AuthProvider` | TDD frontend components |
| Data models | `UserProfile`, `AuthToken` | TDD data model names |
| API endpoints | `/v1/auth/login`, `/v1/auth/register`, `/v1/auth/me`, `/v1/auth/refresh` | TDD API surface |
| Test IDs | `UT-001`, `IT-001`, `E2E-001` | TDD test artifacts |
| Feature flags | `AUTH_NEW_LOGIN`, `AUTH_TOKEN_REFRESH` | TDD migration/rollout |
| Libraries | `bcryptjs`, `jsonwebtoken` | TDD dependencies |
| Infrastructure | `PostgreSQL 15`, `Redis 7` | TDD infrastructure |

### What to grep for in generated tasklists to verify PRD enrichment flowed through (both):

| Category | Grep Pattern | Rationale |
|----------|-------------|-----------|
| Personas | `Alex`, `Sam`, `Jordan` | PRD user personas |
| Business | `$2.4M`, `SOC2` | PRD business context |
| Compliance | `NFR-COMP-001`, `GDPR`, `data minimization` | PRD compliance mandates |
| Metrics | `> 60%`, `< 200ms`, `99.9%` | PRD success thresholds |
| Risk IDs | `R-001`, `R-002` (or `R1`, `R2`) | Risk traceability |

### What to grep for to verify Spec enrichment flowed through (test2):

| Category | Grep Pattern | Rationale |
|----------|-------------|-----------|
| Milestones | `M1:`, `M2:`, `M3:`, `M4:`, `M5:`, `M6:` | Spec milestone structure |
| Task numbering | `Task 1.1`, `Task 2.1`, `Task 3.1` | Spec task table format |
| Requirement IDs | `FR-AUTH.1`, `FR-AUTH.2`, `FR-AUTH.3` | Spec requirement notation |
| Dependency IDs | `D1`, `D2`, `D3`, `D4`, `D5` | Spec dependency tracking |
| NFR IDs | `NFR-AUTH.1`, `NFR-AUTH.2` | Spec NFR notation |
| Scope guards | `Out of scope`, `OAuth/OIDC`, `Multi-factor` | Spec scope guardrails |
| OQ IDs | `OQ1`, `OQ2`, `OQ3` through `OQ9` | Spec open question resolution |

---

## 6. Structural Differences Impacting Tasklist Generation

| Dimension | test1 (TDD+PRD) | test2 (Spec+PRD) |
|-----------|-----------------|------------------|
| Phase count | 4 (Phase 0-3) | 2 + buffer |
| Task format | Narrative bullets by week | Structured tables by milestone |
| Requirement ID format | `FR-AUTH-001` (dashes) | `FR-AUTH.1` (dots) |
| Line count | 523 | 330 |
| Milestone labels | None (weeks only) | M1-M6 |
| Frontmatter has `prd_source`? | Yes | No |
| Rollback criteria | Explicit section | Not present |
| Feature flag table | Yes | Not present |
| Rate limiting table | Yes | Not present |
| Scope guardrails section | Not present | Yes |
| Persona coverage table | In risk/validation text | Dedicated section |

**Implication for tasklist generator**: The generator must handle both narrative and tabular task formats, variable phase counts, and different requirement ID notation styles. It cannot assume a fixed roadmap structure.

---

## 7. Existing tasklist-fidelity.md Analysis

### test1 tasklist-fidelity.md (4.2 KB)
Contains a detailed DEV-001 HIGH severity deviation documenting EVERYTHING that should be in a tasklist but is missing:
- 4 phases, 5 FRs, 9 NFRs, 4 compliance mandates
- 7 risks, 10 success criteria, 5 integration points
- 6 rate-limiting rules, 2 feature flags, rollback criteria
- Supplementary TDD Validation: lists specific test IDs, component inventory, data models, API endpoints
- Supplementary PRD Validation: lists personas, success metrics, customer journeys, business context

**This file is effectively a CHECKLIST of what the generated tasklist must contain.**

### test2 tasklist-fidelity.md (0.9 KB)
Minimal -- just states no tasklist exists. Less detail than test1.

---

## 8. Summary for Task File Builder

### Primary input for tasklist generation:
- **File**: `roadmap.md` in each result directory
- **Metadata**: `.roadmap-state.json` for `input_type`, source file paths
- **No other files needed** from the results directory

### What the tasklist generator must produce per roadmap:
1. Task items traceable to requirement IDs (FR-AUTH-xxx or FR-AUTH.x)
2. Phase/milestone grouping matching roadmap structure
3. Component-level tasks (AuthService, PasswordHasher, etc.)
4. Testing tasks referencing test IDs (UT-001, IT-001, E2E-001)
5. Compliance tasks referencing NFR-COMP-xxx or NFR-AUTH.x
6. Risk mitigation tasks referencing R-001 through R-007
7. Success criteria validation tasks with numeric targets
8. Persona coverage verification

### The E2E test should:
1. Run tasklist generation on both `test1-tdd-prd/roadmap.md` and `test2-spec-prd/roadmap.md`
2. Verify generated tasklist files exist in the output directory
3. Grep for TDD-specific content in test1 output (component names, API endpoints, test IDs)
4. Grep for PRD-specific content in both outputs (personas, business metrics, compliance)
5. Grep for Spec-specific content in test2 output (milestones, task tables, dependency IDs)
6. Verify `tasklist-fidelity.md` updates to `tasklist_ready: true` after generation
