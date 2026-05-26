# Base Selection: Hybrid Scoring Analysis

## Quantitative Scoring (50% weight)

5 deterministic metrics computed from artifact text.

| Metric | Weight | Variant A (opus:security) | Variant B (sonnet:security) |
|--------|--------|---------------------------|------------------------------|
| Requirement Coverage (RC) | 0.30 | 1.00 (18/18 FRs+NFRs) | 1.00 (18/18 FRs+NFRs) |
| Internal Consistency (IC) | 0.25 | 1.00 (no contradictions) | 1.00 (no contradictions) |
| Specificity Ratio (SR) | 0.15 | 0.83 (concrete: bcrypt ≥12, 24h TTL, RS256, etc.) | 0.85 (concrete + observability metrics) |
| Dependency Completeness (DC) | 0.15 | 1.00 (all M#, V# references resolve) | 1.00 (all M#, V# references resolve) |
| Section Coverage (SC) | 0.15 | 1.00 (9 sections = max) | 0.78 (7/9 sections) |
| **quant_score** | | **0.9745** | **0.9445** |

### Per-Metric Computation Notes

- **RC**: Both variants explicitly tag every FR (FR-001..FR-012) and NFR (NFR-001..NFR-006) to at least one deliverable. Coverage tie.
- **IC**: Neither variant contains an internal contradiction. Note that Variant A's CSP-deferred-to-M6 design weakens RISK-001 mitigation timing — but this is not an internal contradiction (it's a debate point, X-001).
- **SR**: Both heavily concrete; Variant B's observability baseline (D1.5) adds specific metric/tracing artifacts, edging SR slightly higher.
- **DC**: Both have fully-resolved internal references; no broken M# or V# pointers.
- **SC**: Variant A's 9 milestones (7 work + 2 validation) is the max across variants → SC=1.00. Variant B's 7 (5 work + 2 validation) normalizes to 0.78.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

30-criterion rubric across 6 dimensions. CEV (Claim-Evidence-Verdict) protocol applied to each criterion. No partial credit.

### Completeness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Covers all explicit requirements from source | MET (all 12 FRs + 6 NFRs tagged to deliverables) | MET (all 12 FRs + 6 NFRs tagged) |
| 2 | Addresses edge cases and failure scenarios | MET (V1+V2 stop criteria explicit; RISK-003 fallback) | MET (V1+V2 stop criteria; OAuth fallback) |
| 3 | Includes dependencies and prerequisites | MET (DEP-001..DEP-004 all in M1) | MET (DEP-001..DEP-004 all in M1) |
| 4 | Defines success/completion criteria | MET (SC-001..SC-005 mapped) | MET (SC-001..SC-005 mapped) |
| 5 | Specifies what is explicitly out of scope | NOT MET (no "Out of Scope" section in roadmap body — inherits from spec implicitly) | NOT MET (same — inherits from spec) |

**A: 4/5 | B: 4/5**

### Correctness (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | No factual errors or hallucinated claims | MET | MET |
| 2 | Technical approaches feasible | MET (bcrypt, RS256, OAuth2/PKCE all real) | MET (same) |
| 3 | Consistent terminology | MET | MET |
| 4 | No internal contradictions | MET | MET |
| 5 | Claims supported by evidence | MET (each deliverable cites FR/NFR/RISK) | MET (each deliverable cites FR/NFR/RISK) |

**A: 5/5 | B: 5/5**

### Structure (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Logical section ordering | MET (deps before dependents) | MET (deps before dependents) |
| 2 | Consistent hierarchy depth | MET | MET |
| 3 | Clear separation of concerns | MET (security primitives separated) | MET (policy-enforcement grouped) |
| 4 | Navigation aids | MET (Milestone Summary table + Dependency Graph) | MET (same) |
| 5 | Follows roadmap conventions | MET | MET |

**A: 5/5 | B: 5/5**

### Clarity (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Unambiguous language | MET (no "should consider" / "might") | MET (same) |
| 2 | Concrete rather than abstract | MET (specific TTLs, bcrypt cost, etc.) | MET (same) |
| 3 | Each section has clear purpose | MET | MET |
| 4 | Acronyms defined on first use | MET (STRIDE, RBAC, JWT, OAuth2 all clear from context) | MET (same) |
| 5 | Actionable next steps | MET (deliverables with acceptance criteria) | MET (same) |

**A: 5/5 | B: 5/5**

### Risk Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Identifies ≥3 risks w/ prob+impact | MET (4 risks: RISK-001..RISK-004) | MET (same 4 risks) |
| 2 | Mitigation strategy per risk | MET | MET |
| 3 | Failure modes and recovery | MET (V1+V2 stop criteria) | MET (V1+V2 stop criteria) |
| 4 | External dependencies + failures | MET (RISK-003 OAuth downtime) | MET (same) |
| 5 | Monitoring/validation mechanism | NOT MET (no observability deliverable; relies on V1+V2 only) | MET (D1.5 observability baseline: structured logs + metrics + tracing) |

**A: 4/5 | B: 5/5**

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Variant A | Variant B |
|---|-----------|-----------|-----------|
| 1 | Boundary conditions for collections (empty/single/max) | NOT MET (no explicit empty-roles or single-permission handling) | NOT MET (same gap) |
| 2 | State variable interactions across boundaries | MET (JWT-shape-lock sequencing M3→V1→M4 explicit) | NOT MET (V1 gates but no JWT-shape-lock rationale documented) |
| 3 | Guard condition gaps | MET (deny-by-default RBAC; account lockout) | MET (deny-by-default RBAC; CSP+cookies bundled) |
| 4 | Count divergence (off-by-one, ranges) | MET (per-user + per-IP rate limit explicit) | MET (same) |
| 5 | Interaction effects when features combine | MET (V2 validates M4+M5+M6 composition) | MET (V2 validates M3+M4 composition) |

**A: 4/5 | B: 3/5**

**Edge Case Floor Check**: Both variants score ≥1/5 → both eligible as base.

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 |
| Correctness | 5/5 | 5/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 4/5 | 5/5 |
| Invariant & Edge Case | 4/5 | 3/5 |
| **Total** | **27/30 = 0.900** | **27/30 = 0.900** |

## Position-Bias Mitigation

| Pass | Order | Result |
|------|-------|--------|
| Pass 1 | A → B | A: 27/30; B: 27/30 |
| Pass 2 | B → A | A: 27/30; B: 27/30 |
| **Agreement** | | **Yes — both passes produce identical verdicts** |

No disagreements detected; no re-evaluation triggered.

## Combined Scoring

| | Variant A | Variant B |
|---|-----------|-----------|
| quant_score | 0.9745 | 0.9445 |
| qual_score | 0.900 | 0.900 |
| combined = 0.50×quant + 0.50×qual | 0.937 | 0.922 |
| **Final Score** | **0.937** | **0.922** |

**Margin**: |0.937 − 0.922| = **0.015 (1.5%)** — within 5% threshold → **tiebreaker triggered**.

## Tiebreaker Application

### Level 1: Debate Performance

Points won in Step 2 scoring matrix (clear winners only, hybrids and ties excluded):

| Variant | Diff points won | IDs |
|---------|----------------|-----|
| A | 4 | S-003, C-003, X-003, A-008 |
| B | 6 | S-001, S-005, S-006, C-002, C-005, X-001 |

**Level 1 winner: Variant B** (6 > 4)

Tiebreaker resolved at Level 1; Levels 2 and 3 not needed.

## Selected Base: Variant B (sonnet:security)

**Selection rationale**: Variant B wins by tiebreaker Level 1 (debate performance, 6 vs 4 clear points). Variant A wins on aggregate combined-score margin (0.015), but the margin is below the 5% threshold that would have made it decisive. Debate-performance tiebreaker reflects that Variant B's high-severity contested wins (S-006 shippable-M2, C-002 / X-001 CSP-in-M2) were stronger arguments than Variant A's wins (S-003 / X-003 2FA-as-defense).

**Strengths to preserve from Variant B (base)**:

- 5-milestone shape at low end of MEDIUM range (M1, M2, M3, M4, M5 + V1, V2)
- M2 as shippable email/password auth (S-006)
- CSP headers in M2 alongside cookies (X-001, C-002)
- Observability baseline in M1 (U-004, D1.5)
- GDPR self-service deliverables in M5 (U-005, D5.4 + D5.5)
- GDPR-aware audit retention (D4.6)

**Strengths to incorporate from Variant A (non-base)**:

- STRIDE threat-model deliverable (U-001) — added as a deliverable inside M1 Foundation (not a separate milestone, per Round 2 hybrid resolution of X-002)
- JWT-shape-lock sequencing rationale (U-002) — make M2 → V1 → M3 ordering explicit with "JWT shape locked at V1" gate
- Secret/key rotation policy at foundation (U-003) — add as deliverable in M1
- 2FA framing as defense (mitigates RISK-002) — move 2FA out of M3 (per B's Round 2 concession); pair with rate-limit in M4 split

**Structural change from B's original shape (per B's Round 2 concession on S-004)**:

- Split M4 (Authorization, Audit & Rate Limiting) into two milestones:
  - M4a: Authorization (RBAC) & Audit Logging
  - M4b: Rate Limiting + Lockout + 2FA (Defense)
- Result: 6 work + 2 validation = 8 total milestones (one more than B's original 5+2; one less than A's 7+2). Middle ground at MEDIUM range top.

**Additional invariant-probe items to incorporate (from Round 2.5)**:

- INV-002: V2 stop criterion — session-store outage degrades gracefully
- INV-006: V2 deliverable — RBAC test covers empty-role users
- INV-008: Explicit deliverable — rate limit applies to OAuth callback paths
- INV-009: Preserved (already in B's D4.6 → carry into merged M4a)
- INV-010: Document as out-of-scope / future product decision
