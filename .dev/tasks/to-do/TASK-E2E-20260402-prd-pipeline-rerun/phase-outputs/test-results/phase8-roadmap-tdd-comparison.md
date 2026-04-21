# Phase 8.2 -- TDD+PRD vs TDD-Only Roadmap Comparison

**Date:** 2026-04-02
**Files Compared:**
- NEW: `.dev/test-fixtures/results/test1-tdd-prd/roadmap.md` (TDD+PRD enriched)
- PRIOR: `.dev/test-fixtures/results/test1-tdd-modified/roadmap.md` (TDD-only)

---

## Structural Comparison

| Dimension | TDD-Only | TDD+PRD | Delta | Assessment |
|-----------|----------|---------|-------|------------|
| Total lines | 634 | 523 | -111 (-17.5%) | TDD+PRD is more concise despite richer content |
| `prd_source` frontmatter field | absent | `"test-prd-user-auth.md"` | Added | PRD provenance tracked in metadata |

---

## TDD Identifier Preservation

| TDD Component | TDD-Only | TDD+PRD | Delta | Assessment |
|---------------|----------|---------|-------|------------|
| `UserProfile` | 14 | 4 | -10 | Reduced but still present; content consolidated |
| `AuthToken` | 6 | 6 | 0 | Identical count in both |
| `AuthService` | 17 | 26 | +9 | Expanded -- more integration wiring |
| `TokenManager` | 23 | 19 | -4 | Present in both |
| `JwtService` | 20 | 11 | -9 | Reduced but still present |
| `PasswordHasher` | 21 | 15 | -6 | Present in both |
| `LoginPage` | 15 | 8 | -7 | Reduced but still present |
| `RegisterPage` | 13 | 8 | -5 | Reduced but still present |
| `AuthProvider` | 14 | 14 | 0 | Identical |
| **Total TDD identifiers** | **143** | **111** | -32 | All 9 identifiers present in both |

All 9 backticked TDD component names are present in both roadmaps. Count variations reflect different narrative structures (4-phase vs 6-phase), not missing coverage.

---

## PRD-Specific Content Analysis

| PRD Signal | TDD-Only | TDD+PRD | Delta | Assessment |
|------------|----------|---------|-------|------------|
| "persona" | 0 | 6 | +6 | Persona-driven validation section added |
| "compliance" | 0 | 14 | +14 | Compliance gates and controls throughout |
| "GDPR" | 0 | 7 | +7 | GDPR consent and data minimization |
| "SOC2" | 0 | 8 | +8 | SOC2 Type II audit logging and controls |
| "conversion" | 5 | 4 | -1 | Both reference conversion; slight difference |
| "session duration" | 0 | 3 | +3 | PRD business metric integrated |
| "Alex" (persona) | 0 | 2 | +2 | End user persona referenced |
| "Jordan" (persona) | 0 | 3 | +3 | Admin persona referenced |
| "Sam" (persona) | 3 | 4 | +1 | API consumer persona; both mention Sam |
| "business value" | 0 | 0 | 0 | Neither uses this exact phrase |

---

## Roadmap Architecture Differences

| Aspect | TDD-Only | TDD+PRD |
|--------|----------|---------|
| Phase count | 6 phases (0-5) | 4 phases (0-3) |
| Timeline | ~9-11 weeks | ~12.5 weeks |
| Executive summary | Technical-only | Includes business drivers ($2.4M revenue, SOC2 deadline, competitive positioning) |
| Compliance gates | None | Phase 1 compliance gate, Phase 2 SOC2 validation |
| Persona validation | None | Explicit Alex/Jordan/Sam validation section in Phase 2 |
| Success criteria | 7 metrics | 10 metrics (3 PRD-sourced additions) |
| Open questions | 6 (OQ-001 to OQ-006) | 8 (OQ-001 to OQ-008, including PRD gap analysis) |

---

## Key Findings

1. **All TDD component names preserved**: Every backticked identifier from the TDD (UserProfile, AuthToken, AuthService, TokenManager, JwtService, PasswordHasher, LoginPage, RegisterPage, AuthProvider) appears in both roadmaps.

2. **PRD enrichment adds compliance layer**: GDPR (7 mentions), SOC2 (8 mentions), and compliance (14 mentions) are entirely absent from TDD-only and substantial in TDD+PRD.

3. **Persona-driven validation is new**: The TDD+PRD roadmap includes explicit persona validation for Alex, Jordan, and Sam -- absent in TDD-only.

4. **Business context added**: The executive summary in TDD+PRD includes revenue projections, competitive positioning, and compliance deadlines that give strategic justification absent from TDD-only.

5. **More concise despite richer content**: TDD+PRD is 111 lines shorter, suggesting better content organization with the enriched pipeline.

**Assessment: PASS** -- PRD enrichment adds significant compliance, persona, and business context while preserving all TDD technical identifiers.
