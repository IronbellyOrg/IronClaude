---
base_variant: "Haiku (Variant B)"
variant_scores: "A:71 B:77"
---

## Scoring Criteria

Derived from debate convergence points, PRD requirements, and roadmap quality dimensions:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| 1 | Spec coverage completeness | 15% | PRD FR/NFR traceability |
| 2 | Architectural integration clarity | 15% | Debate D3, D4, D7 — wiring explicitness |
| 3 | Risk mitigation timing | 10% | Debate D4 — security review placement |
| 4 | Compliance alignment | 10% | PRD S17 (GDPR, SOC2, NIST) |
| 5 | Business value delivery speed | 10% | PRD Success Metrics S19 |
| 6 | Persona coverage | 10% | PRD S7 (Alex, Jordan, Sam) |
| 7 | Timeline realism | 10% | Debate D1/D2 convergence |
| 8 | Open question resolution quality | 10% | Debate convergence on OQs |
| 9 | Scope discipline | 5% | PRD scope definition; guardrails |
| 10 | Actionability (can a team execute from this?) | 5% | Milestone granularity, acceptance criteria |

---

## Per-Criterion Scores

### 1. Spec Coverage Completeness (15%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 7/10 | Covers all FR-AUTH.1–5 and NFR-AUTH.1–7. However, logout is listed as Open Question #10 rather than a milestone. No dedicated password_reset_tokens table — reset tokens implied to share refresh_tokens infrastructure. |
| B (Haiku) | 9/10 | Covers all FR/NFR with explicit milestones. Logout gets its own milestone (1.4.4). Dedicated `password_reset_tokens` table (Milestone 2.3.1). Explicit sub-requirement traceability (FR-AUTH.1a–d mapped to specific milestones). Per-endpoint acceptance criteria reference FR IDs directly. |

**Haiku wins.** The per-sub-requirement traceability (FR-AUTH.1a, 1b, 1c, 1d each called out) is significantly more auditable. The dedicated reset token table was flagged in the debate as architecturally superior.

### 2. Architectural Integration Clarity (15%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 7/10 | Integration Points tables per phase are useful but describe components at a high level. No explicit registry/dispatch patterns. The Phase 4 table acknowledges "retroactive wiring into Phase 2–3 handlers" — the debate identified this as a weakness. |
| B (Haiku) | 9/10 | Five explicit integration points with named artifacts (TokenTypeStrategy, AuthErrorRegistry, MiddlewareChain, AuditEventRegistry, ResetTokenDispatch). Each has Wired Components, Owning Phase, and Consumed By. Appendix summarizes all dispatch mechanisms. This is directly executable. |

**Haiku wins.** The named artifact pattern with explicit wiring phases is materially better for engineering handoff. Opus's integration tables are informative but lack the dispatch/registry specificity that prevents integration bugs.

### 3. Risk Mitigation Timing (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 5/10 | Single security review in Phase 4.3. Debate Round 2 conceded that mid-stream review for primitives is high-value. Audit wiring deferred to Phase 4 creates the "Week 12 discovery" risk the debate flagged. |
| B (Haiku) | 8/10 | Mid-stream security review at Milestone 1.5.2 (Week 3) plus pre-production review. Audit events wired incrementally from Phase 1. Debate convergence explicitly favored Haiku's approach on both D3 and D4. |

**Haiku wins.** The debate reached "High" confidence convergence that incremental audit wiring and early security review are lower-risk. Opus's own rebuttal acknowledged the risks but argued they were manageable — the debate judge (convergence assessment) disagreed.

### 4. Compliance Alignment (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 7/10 | GDPR consent in Phase 2.1. SOC2 audit logging in Phase 4.1. Compliance validation exists but is late (Week 12+). Risk #6 correctly flags this but mitigation is "resolve before Phase 4" — reactive. |
| B (Haiku) | 8/10 | Audit_logs table pre-provisioned in Phase 1 Week 1. GDPR consent has dedicated milestone (2.4.3). SOC2 validation milestone (2.5.1). NIST validation milestone (2.5.2). Compliance checkpoints are earlier and more granular. |

**Haiku wins marginally.** Both address compliance, but Haiku's early table provisioning and dedicated compliance milestones are more aligned with the PRD's SOC2 Q3 2026 deadline pressure.

### 5. Business Value Delivery Speed (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 5/10 | First user-facing value (registration + login) at Week 7. Full auth surface at Week 11. Production at Week 14. PRD targets Q2 2026 — 14 weeks may not fit depending on start date. |
| B (Haiku) | 8/10 | Registration + login + logout by Week 3. Full surface by Week 5. Production-ready by Week 6. Delivers against PRD Success Metrics (registration conversion, login p95) much earlier. |

**Haiku wins.** The debate acknowledged timeline depends on staffing, but Haiku delivers user-facing value in half the time. The PRD's Success Metrics (S19) require post-launch measurement — earlier launch means earlier data.

### 6. Persona Coverage (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 6/10 | Alex persona referenced in Phase 2 (frontend forms). Sam mentioned once (Phase 3.1 silent refresh). Jordan mentioned once in Phase 4.1 (admin UI out of scope). No systematic persona mapping. |
| B (Haiku) | 7/10 | Alex, Sam, and Jordan referenced in context. Auth-E1/E2/E3 user stories mapped to milestones. However, Jordan's admin capabilities are still largely deferred. Sam's API consumer needs are addressed via token refresh but not with dedicated API documentation milestones. |

**Haiku wins marginally.** Neither variant is strong on persona-driven design, but Haiku's user story mapping provides better traceability to PRD personas.

### 7. Timeline Realism (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 6/10 | 14 weeks / 4 phases. Debate exposed this assumes ~1 FTE throughput. Convergence suggested 8-10 weeks with ~2 FTE is realistic. Opus's timeline has slack but may exceed Q2 window. |
| B (Haiku) | 7/10 | 6 weeks / 2 phases with 2.8 FTE. Debate noted this is achievable with parallel execution but tight. Haiku provides week-by-week owner assignments and FTE breakdown. Convergence point of 8-10 weeks is closer to Haiku. |

**Haiku wins marginally.** Neither timeline is perfect — the truth is likely 8-10 weeks. But Haiku's FTE breakdown and week-level scheduling is more actionable for project planning, and is closer to the convergence estimate.

### 8. Open Question Resolution Quality (10%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 8/10 | Clean table with 10 OQs, blocking phase, recommended resolution, and decision owner. Architect's recommendation paragraph prioritizes #5, #7, #10. Analysis is concise and decisive. |
| B (Haiku) | 7/10 | More verbose OQ treatment split across PRD-Spec Conflicts, Engineering Clarifications, Compliance Clarifications, and Product Clarifications. More thorough but harder to scan. Some recommendations are hedged ("v1.0 rate limits at IP level; v1.1 adds account-level lockout") where Opus is more decisive. |

**Opus wins.** The single table format with blocking-phase linkage is more actionable. Opus's architect notes on prioritization are sharper.

### 9. Scope Discipline (5%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 9/10 | Dedicated "Scope Guardrails" section (Section 8) with explicit out-of-scope table and redirect guidance. Clean and decisive. |
| B (Haiku) | 7/10 | Scope managed through open questions and inline notes rather than a dedicated section. No explicit guardrails table. |

**Opus wins.** The guardrails section is a valuable artifact for scope creep prevention during execution.

### 10. Actionability (5%)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 6/10 | Milestones have checkbox items but acceptance criteria are at the phase level (exit criteria paragraphs). No per-milestone acceptance criteria. No owner assignments per milestone. |
| B (Haiku) | 9/10 | Every milestone has explicit Acceptance Criteria, Dependencies, and Architect Notes. Week-level owner assignments. Pre-Phase 1 checklist. Critical path blocker chain. Immediately executable. |

**Haiku wins decisively.** The per-milestone acceptance criteria and owner assignments make Haiku directly executable without further decomposition.

---

## Overall Scores

| Criterion | Weight | A (Opus) | B (Haiku) |
|-----------|--------|----------|-----------|
| Spec coverage | 15% | 7 | 9 |
| Integration clarity | 15% | 7 | 9 |
| Risk mitigation timing | 10% | 5 | 8 |
| Compliance alignment | 10% | 7 | 8 |
| Business value speed | 10% | 5 | 8 |
| Persona coverage | 10% | 6 | 7 |
| Timeline realism | 10% | 6 | 7 |
| OQ resolution quality | 10% | 8 | 7 |
| Scope discipline | 5% | 9 | 7 |
| Actionability | 5% | 6 | 9 |

**Weighted totals:**
- **Variant A (Opus): 6.55 → 71/100** (scaled)
- **Variant B (Haiku): 7.95 → 77/100** (scaled)

---

## Base Variant Selection Rationale

**Haiku (Variant B) is selected as the base** for three reasons:

1. **Structural superiority for execution.** Haiku's per-milestone acceptance criteria, named integration artifacts, owner assignments, and week-level scheduling make it directly executable. Opus would require significant decomposition before a team could start work.

2. **Debate-validated architectural decisions.** The debate reached "High" confidence convergence favoring Haiku on audit wiring (D3) and security review timing (D4) — two of the most consequential architectural divergences. Using Haiku as the base preserves these decisions without rework.

3. **Faster value delivery against PRD metrics.** The PRD's Success Metrics require post-launch measurement. Haiku's faster delivery timeline means earlier access to registration conversion and session duration data, enabling faster iteration.

---

## Improvements to Incorporate from Opus (Variant A)

The following specific elements from Opus should be merged into the Haiku base:

### Must Include

1. **Scope Guardrails section (Opus Section 8).** Haiku lacks a dedicated scope boundary table. Adopt Opus's Section 8 verbatim — it provides explicit out-of-scope items with redirect guidance that prevents scope creep during sprints.

2. **Open Questions table format (Opus Section 7).** Replace Haiku's fragmented OQ sections with Opus's single table format (Question / Blocks Phase / Recommended Resolution / Decision Owner). Add Opus's architect recommendation paragraph prioritizing #5, #7, #10.

3. **Feature flag strategy.** Opus's `AUTH_SERVICE_ENABLED` flag with gradual rollout (Phase 4.3) is a production safety mechanism Haiku lacks. Add feature flag provisioning to Haiku's Milestone 1.1.2 and rollout gating to Phase 2 completion.

4. **Risk commentary on replay detection atomicity.** Opus's architect note on database-level compare-and-swap for token rotation (Risk #2) is a critical implementation detail. Add as an architect note to Haiku's Milestone 1.2.3.

### Should Include

5. **Password policy enforcement at both layers (debate convergence on D7).** Haiku enforces policy in PasswordHasher; Opus enforces at the endpoint. Debate converged on both: endpoint for UX errors, PasswordHasher guard as backstop. Add endpoint-level validation to Haiku's Milestone 1.4.2 while keeping PasswordHasher enforcement in 1.2.1.

6. **Account lockout schema provisioning (debate convergence on D11).** Add a `failed_attempts` counter and `locked_until` timestamp to the users table in Milestone 1.1.1, with a note that full lockout logic is deferred to v1.1. This captures data without adding endpoint scope.

7. **Timeline adjustment toward convergence estimate.** Adjust Haiku's 6-week timeline to 8-10 weeks with a note that the exact duration depends on team capacity (the debate's convergence point). Consider a 3-phase structure: Foundation (weeks 1-3) → Core+Session (weeks 4-7) → Compliance+Launch (weeks 8-10).

### Nice to Have

8. **Opus's success criteria pre-launch/post-launch split.** Opus cleanly separates pre-launch gates (#2, #6, #7, #8) from post-launch monitoring (#1, #3, #4, #5). Add this categorization to Haiku's success metrics section.

9. **Opus's email dispatch recommendation.** Opus pragmatically notes "sync acceptable for v1.0 given low volume" while recommending async. Add this nuance to Haiku's Milestone 2.3.2 rather than Haiku's harder stance on async-only.
