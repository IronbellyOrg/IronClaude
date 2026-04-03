---
base_variant: "roadmap-opus-architect"
variant_scores: "A:81 B:73"
---

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced 9 divergence points and 9 convergence assessments. I derive these weighted criteria:

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Architectural correctness** | 20% | Schema timing, DI wiring, integration sequencing |
| **Security posture** | 15% | Debate confirmed equivalent outcomes; scoring differentiates on *when* controls are validated |
| **Testing strategy** | 15% | Central debate topic (embedded vs consolidated) |
| **Spec fidelity** | 15% | How precisely the roadmap traces to FR/NFR/SC requirements |
| **Pragmatic execution** | 15% | Team sizing realism, timeline credibility, infrastructure overhead |
| **Production readiness** | 10% | Deployment, monitoring, documentation completeness |
| **Risk management** | 10% | Risk identification, mitigation timing, residual risk clarity |

## 2. Per-Criterion Scores

### Architectural Correctness (20%)

| | Variant A (Opus) | Variant B (Haiku) |
|--|--|--|
| Score | **88** | **68** |

**Justification**: The debate's sharpest unresolved dispute (D-4) favors Opus. As Opus argued and the convergence assessment confirmed: "the spec is unusually precise about data models" — FR-AUTH.2 defines the exact user fields, FR-AUTH.3d defines refresh token storage. Haiku's service-first approach builds 3 weeks of mocks for a schema that's already determined by the spec. Opus's Phase 1 database-first eliminates mock-to-real integration risk entirely. Haiku's Phase 3.4 DI container setup coming *after* database integration (Week 5) means the DI graph isn't fully wired until halfway through the project — Opus wires DI in Phase 1.

### Security Posture (15%)

| | Variant A (Opus) | Variant B (Haiku) |
|--|--|--|
| Score | **80** | **82** |

**Justification**: Near-parity. Both implement identical controls (RS256, bcrypt-12, httpOnly cookies, replay detection). Haiku edges slightly ahead with explicit Phase 0 crypto code review gate and named security engineer ownership per phase. Opus validates security in Phase 4 but doesn't have a dedicated crypto review gate before services consume the crypto layer. The debate confirmed "security posture is equivalent" (convergence point 3) — the difference is organizational, not technical.

### Testing Strategy (15%)

| | Variant A (Opus) | Variant B (Haiku) |
|--|--|--|
| Score | **78** | **76** |

**Justification**: The debate's convergence assessment (point 4) is definitive: "The strongest plan takes both: test within each phase (Opus) and add a final validation phase with explicit coverage targets (Haiku). Neither approach alone is sufficient." Opus scores higher because its embedded testing catches defects cheaper (the "10x cost" argument was not rebutted). Haiku's Phase 5 coverage targets (90% line, 85% branch) are valuable but come after 6+ weeks of code — context-switching cost is real. Haiku's rebuttal that Opus Phase 1 has "only unit tests for 2 services" mischaracterizes Opus's Phase 2 (15+ test cases) and Phase 3 (5 integration test suites).

### Spec Fidelity (15%)

| | Variant A (Opus) | Variant B (Haiku) |
|--|--|--|
| Score | **85** | **78** |

**Justification**: Opus maps every task to specific requirement IDs (FR-AUTH.x, NFR-AUTH.x, SC-x) with a validation matrix (Section 6). Haiku also traces requirements but introduces scope creep: a `reset_tokens` table not in the spec, a `PasswordResetService` as a separate service (spec implies it's part of AuthService per FR-AUTH.5), and Argon2 migration planning (no spec basis). Opus's OQ resolution table is cleaner — 7 items with recommended resolutions and blocking phases. Haiku resolves OQs inline across phases, making traceability harder.

### Pragmatic Execution (15%)

| | Variant A (Opus) | Variant B (Haiku) |
|--|--|--|
| Score | **85** | **62** |

**Justification**: Largest gap. Opus: 5-6 weeks, 2 engineers + 1 reviewer. Haiku: 8-9 weeks, 9 named roles. The debate exposed this clearly — Opus's "36 communication channels" argument (Brooks's Law) was not effectively rebutted. Haiku's counter ("bus factor of 1") is valid but doesn't justify 9 roles for 6 routes and 2 tables. Haiku's "consolidatable to 5-6" concession undermines its own staffing map. Timeline: Haiku's Phase 3 database integration in Weeks 4-5 means no real integration testing until Week 6+ — that's late discovery of integration bugs. Opus integrates against real tables from Week 1.

### Production Readiness (10%)

| | Variant A (Opus) | Variant B (Haiku) |
|--|--|--|
| Score | **68** | **85** |

**Justification**: Haiku wins decisively. Phase 6 covers secrets management, monitoring/alerting with specific thresholds, CI/CD with gradual rollout (10%→50%→100%), comprehensive documentation (API, architecture, runbooks, security, developer guide), and post-deployment validation. Opus's Phase 4 covers monitoring and rollback but lacks deployment pipeline detail, gradual rollout strategy, and documentation deliverables. The debate's convergence point 9 confirmed: "Haiku's production readiness coverage is objectively more complete."

### Risk Management (10%)

| | Variant A (Opus) | Variant B (Haiku) |
|--|--|--|
| Score | **78** | **80** |

**Justification**: Near-parity. Haiku identifies 6 risks vs Opus's 5, adding RISK-5 (brute-force) and RISK-6 (password entropy). Haiku includes probability assessments and residual risk columns. Opus's risk table is more concise but equally actionable. Haiku's async email dispatch (D-8) was debated — Opus's traffic analysis ("reset = <1% of requests") was "quantitatively persuasive for MVP" per the convergence assessment, but Haiku's resilience argument has merit for production.

## 3. Overall Scores

| Criterion | Weight | Variant A | Variant B |
|-----------|--------|-----------|-----------|
| Architectural correctness | 20% | 88 | 68 |
| Security posture | 15% | 80 | 82 |
| Testing strategy | 15% | 78 | 76 |
| Spec fidelity | 15% | 85 | 78 |
| Pragmatic execution | 15% | 85 | 62 |
| Production readiness | 10% | 68 | 85 |
| Risk management | 10% | 78 | 80 |
| **Weighted Total** | | **81.2** | **73.4** |

**Variant A: 81 | Variant B: 73**

## 4. Base Variant Selection Rationale

**Selected base: Variant A (Opus-Architect)**

Three factors drive this:

1. **Architectural sequencing is correct**: Database-first for a spec-determined schema eliminates a class of integration bugs. This is the debate's sharpest technical disagreement (D-4), and the convergence assessment sided with Opus: "Opus's argument is stronger for this specific project because the spec is unusually precise about data models."

2. **Execution realism**: 5-6 weeks with 2-3 people vs 8-9 weeks with 9 roles. For an auth service with 6 endpoints and 2 tables, Opus's team model is credible. Haiku's staffing map, while thorough as documentation, inflates coordination overhead.

3. **Embedded testing catches bugs cheaper**: The 10x cost multiplier for late-found defects is well-established. Opus tests in every phase. The merge should *add* Haiku's coverage targets and dedicated security/performance test suites, not replace Opus's embedded approach.

## 5. Specific Improvements from Variant B to Incorporate in Merge

### Must incorporate:

1. **Explicit coverage targets from Phase 5**: Add Haiku's "90% line coverage, 85% branch coverage" targets as exit criteria for Opus's Phase 4 hardening gate. Don't create a separate testing phase — embed the targets into the existing gates.

2. **Production readiness content (Phase 6)**: Add a Phase 5 (or extend Phase 4) with Haiku's:
   - Secrets management details (key rotation on 90-day schedule, grace period)
   - Monitoring thresholds (login error rate > 5% → critical, p95 > 300ms → warning, replay → security alert)
   - Gradual rollout strategy (10% → 50% → 100% with monitoring windows)
   - Documentation deliverables (OpenAPI spec, sequence diagrams, runbooks)

3. **Security test suites from Phase 5.4**: Add Haiku's named security tests (replay detection, XSS prevention, information leakage, JWT validation) as specific deliverables in Opus's Phase 4.2 security review. Opus's Phase 4 lists review activities but not executable test suites.

4. **RISK-5 and RISK-6**: Add brute-force and password entropy risks to Opus's risk table. Both are real and Opus omits them.

5. **Crypto review gate**: Add a Phase 0/Phase 1 boundary gate for crypto code review (from Haiku's Phase 0 Gate) before services consume the crypto layer.

### Consider incorporating:

6. **503 for disabled feature flag (D-9)**: The debate was inconclusive. Add a note recommending 503 with `Retry-After` header for internal consumers and 404 for external/public APIs, letting the team decide based on operational maturity.

7. **Async email dispatch note**: Keep Opus's sync-for-MVP decision but add Haiku's resilience argument as a documented trade-off, with the note that if queue infrastructure already exists, prefer async.

### Do not incorporate:

8. **Service-first/mock-first development** (Haiku's Phase 0-1 approach): The spec determines the schema. Mocks add maintenance cost with no design freedom benefit for this project.

9. **9-role staffing map**: Organizational overhead disproportionate to project scope. Opus's 2+1 model is sufficient. Mention Haiku's role checklist as a "responsibility coverage checklist" in an appendix rather than a staffing plan.

10. **Separate PasswordResetService**: Spec groups password reset under FR-AUTH.5 alongside other auth operations. Keep it in AuthService per Opus's design.
