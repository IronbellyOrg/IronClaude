# Base Variant Selection — Hybrid Scoring

## Quantitative Scoring (50% weight)

### Metric Breakdown

| Metric (weight)                       | Variant 1 (opus:architect) | Variant 2 (sonnet:analyzer) | Notes                                                                                              |
|---------------------------------------|----------------------------|------------------------------|----------------------------------------------------------------------------------------------------|
| RC: Requirement Coverage (0.30)       | 0.95                       | 0.97                         | Both cite all FRs/NFRs by ID. V2 wins via explicit NG-001/002/003 Out-of-Scope table.              |
| IC: Internal Consistency (0.25)       | 0.975                      | 0.967                        | V1: INV-007 self-contradiction (2-day buffer vs 2-week remediation). V2: revokeAll API gap + compressed-Beta-vs-gates contradiction. Both ~2 contradictions; V2 has smaller claim base. |
| SR: Specificity Ratio (0.15)          | 0.84                       | 0.93                         | V2's tabular discipline dominates concrete signals. V1's prose includes more rhetorical "deliberately"-class phrasing. |
| DC: Dependency Completeness (0.15)    | 0.94                       | 0.90                         | V1 has explicit Dependency Graph section. V2 has silent revokeAll → TokenManager unresolved reference (penalty). |
| SC: Section Coverage (0.15)           | 0.91 (10/11)               | 1.00 (11/11)                 | V2 has 11 top-level sections (max); V1 has 10.                                                     |

### Quant Formula Calculation

- V1 quant = (0.95×0.30) + (0.975×0.25) + (0.84×0.15) + (0.94×0.15) + (0.91×0.15)
  = 0.285 + 0.244 + 0.126 + 0.141 + 0.137
  = **0.933**
- V2 quant = (0.97×0.30) + (0.967×0.25) + (0.93×0.15) + (0.90×0.15) + (1.00×0.15)
  = 0.291 + 0.242 + 0.140 + 0.135 + 0.150
  = **0.958**

**Quant winner**: V2 by 0.025 margin.

---

## Qualitative Scoring (50% weight) — 30-Criterion Additive Binary Rubric

Each criterion is MET (1) or NOT MET (0). Evidence cited per Claim-Evidence-Verdict (CEV) protocol.

### Completeness (5 criteria)

| # | Criterion                                                  | V1 Evidence                                                                | V1 | V2 Evidence                                                              | V2 |
|---|------------------------------------------------------------|-----------------------------------------------------------------------------|----|--------------------------------------------------------------------------|----|
| 1 | Covers all explicit requirements                            | Cites FR-AUTH-001..005, NFR-PERF/SEC/REL by ID across milestones           | 1  | Cites all FRs/NFRs in §Success Metrics + §Validation Strategy tables    | 1  |
| 2 | Addresses edge cases and failure scenarios                  | M2 §Architectural Risks (timing-leak, concurrent reg); M3 (atomic rotation, clock skew); M4 (audit-log latency, SendGrid degrade) | 1  | R-LATENCY ack only via connection pooling; no atomic rotation/dummy-verify/clock-skew | 0  |
| 3 | Includes dependencies and prerequisites                     | §Dependency Graph with explicit edges                                       | 1  | §Sprint-Level Breakdown with owner column + per-milestone Sprint Alloc  | 1  |
| 4 | Defines success/completion criteria                         | Per-milestone Exit Criteria + Per-milestone Gates section                   | 1  | Per-milestone Validation + Metrics + §Performance & Reliability Gates table | 1  |
| 5 | Specifies what is explicitly out of scope                   | Objective 4 prose mentions extension seams; OQ #5 defers "remember me"; no dedicated table | 0  | §Out-of-Scope explicit table mapping NG-001/002/003 to v1.1/v1.2/v2.0   | 1  |

**Completeness: V1 = 4/5; V2 = 4/5**

### Correctness (5 criteria)

| # | Criterion                                                  | V1 Evidence                                                                | V1 | V2 Evidence                                                              | V2 |
|---|------------------------------------------------------------|-----------------------------------------------------------------------------|----|--------------------------------------------------------------------------|----|
| 1 | No factual errors or hallucinated claims                    | Architecture details match TDD §6.1-§7; AuthService/TokenManager/JwtService/PasswordHasher consistent | 1  | M3 D3.5 references `TokenManager.revokeAll()` which is NOT among V2's M2 TokenManager deliverables (silent dependency on undefined API) | 0  |
| 2 | Technical approaches feasible with stated constraints       | Bcrypt 12 + horizontal scaling contingency (Risk row 1)                    | 1  | R-LATENCY mitigations (connection pooling, JwtService <5ms, Redis <10ms) do not reduce per-hash CPU cost; no scaling plan | 0  |
| 3 | Terminology used consistently and accurately                 | AuthService/TokenManager/JwtService/PasswordHasher used consistently        | 1  | Same — used consistently                                                 | 1  |
| 4 | No internal contradictions                                   | INV-007: 2-day buffer (line 183) contradicts 2-week remediation window (line 214) inside M5 11-day calendar | 0  | Compressed Beta (line 248) contradicts "quality gates non-negotiable" (line 262); revokeAll API gap | 0  |
| 5 | Claims supported by evidence or rationale                    | Heavy citation of TDD sections, FR/NFR IDs, PRD edge cases                  | 1  | Heavy citation of TDD sections, FR/NFR IDs                               | 1  |

**Correctness: V1 = 4/5; V2 = 3/5**

### Structure (5 criteria)

| # | Criterion                                                  | V1 Evidence                                                                | V1 | V2 Evidence                                                              | V2 |
|---|------------------------------------------------------------|-----------------------------------------------------------------------------|----|--------------------------------------------------------------------------|----|
| 1 | Logical section ordering                                   | Exec → Objectives → Milestones → Workstreams → Cross-Cutting → Risk → Deps → Gates → OQ | 1  | Exec → Metrics → Milestones → Sprint → Validation → Risk → Perf Gates → Rollout → Out-of-Scope → OQ | 1  |
| 2 | Consistent hierarchy depth                                 | H1 → H2 → H3 → H4 (uniform per milestone)                                  | 1  | H1 → H2 → H3 (slightly flatter)                                          | 1  |
| 3 | Clear separation of concerns                               | Milestones/Workstreams/Cross-Cutting clearly partitioned                    | 1  | Milestones/Validation/Risk/Rollout clearly partitioned                   | 1  |
| 4 | Navigation aids (TOC, cross-refs, index)                   | No TOC; intra-doc cross-refs ("per Objective 4")                            | 0  | No TOC; intra-doc cross-refs ("per TDD §15.1")                           | 0  |
| 5 | Follows conventions of the artifact type                   | Milestone → Deliverables → Exit Criteria → Risks → Deps is standard roadmap shape | 1  | Milestone → Goal → Deliverables → Validation → Metrics → Sprint is standard sprint-roadmap shape | 1  |

**Structure: V1 = 4/5; V2 = 4/5**

### Clarity (5 criteria)

| # | Criterion                                                  | V1 Evidence                                                                | V1 | V2 Evidence                                                              | V2 |
|---|------------------------------------------------------------|-----------------------------------------------------------------------------|----|--------------------------------------------------------------------------|----|
| 1 | Unambiguous language                                       | Some rhetorical phrasing ("deliberately backend-heavy"); most claims concrete | 1  | Tabular discipline minimizes vague language                              | 1  |
| 2 | Concrete rather than abstract                              | Specific deliverables with owners, dates, exit criteria                     | 1  | Specific deliverables with sprint windows, owners, validation methods    | 1  |
| 3 | Each section has clear purpose (one-sentence summary possible) | Yes per section                                                          | 1  | Yes per section                                                          | 1  |
| 4 | Acronyms and domain terms defined on first use             | ADR, SLO, RPS not defined; ADR is industry-common but should be defined     | 0  | Same: SOC2, OQ, NG not explained at first use                            | 0  |
| 5 | Actionable next steps or decision points clearly identified | Deliverables with owners + Open Questions with recommended positions       | 1  | Deliverables with sprint windows + Open Questions with target dates      | 1  |

**Clarity: V1 = 4/5; V2 = 4/5**

### Risk Coverage (5 criteria)

| # | Criterion                                                  | V1 Evidence                                                                | V1 | V2 Evidence                                                              | V2 |
|---|------------------------------------------------------------|-----------------------------------------------------------------------------|----|--------------------------------------------------------------------------|----|
| 1 | Identifies at least 3 risks with probability and impact    | §Risk Register with 10 rows incl. P/I/Mitigation/Contingency               | 1  | §Risk Matrix with 7 rows incl. Probability/Impact/Inherent/Residual      | 1  |
| 2 | Provides mitigation strategy for each                      | Yes for all 10                                                              | 1  | Yes for all 7                                                            | 1  |
| 3 | Addresses failure modes and recovery procedures            | Per-milestone Architectural Risks + Risk Register contingencies             | 1  | §Rollout Plan rollback triggers + Risk Matrix mitigations                | 1  |
| 4 | External dependencies and their failure scenarios          | Risk Register row 2 (Redis), row 5 (SendGrid); per-milestone deps           | 1  | R-EMAIL, R-REDIS, R-COMPLIANCE rows                                      | 1  |
| 5 | Monitoring/validation mechanism for risk detection         | D4.6 Prometheus + OTel; D5.5 alerts; D4.8 log scrubber                     | 1  | D5.5 dashboards; D5.6 alerts; mention of telemetry per metric            | 1  |

**Risk Coverage: V1 = 5/5; V2 = 5/5**

### Invariant & Edge Case Coverage (5 criteria) — FLOOR-GATED DIMENSION

| # | Criterion                                                  | V1 Evidence                                                                | V1 | V2 Evidence                                                              | V2 |
|---|------------------------------------------------------------|-----------------------------------------------------------------------------|----|--------------------------------------------------------------------------|----|
| 1 | Boundary conditions for collections (empty, single, max)    | No explicit empty-token-set coverage; no max-tokens-per-user cap            | 0  | No coverage                                                              | 0  |
| 2 | State variable interactions across component boundaries     | Redis unavailability impact on JwtService validation; audit-log impact on pg-pool acknowledged (line 154) | 1  | No cross-component interaction analysis                                  | 0  |
| 3 | Guard condition gaps identified                             | Constant-time + dummy-verify for unknown emails (M2 risks); atomic Redis rotation (M3 risks); kid header handling | 1  | No guard analysis                                                        | 0  |
| 4 | Count divergence scenarios (off-by-one, range bounds)       | No explicit off-by-one analysis; 5-min k6 duration assumed valid            | 0  | No off-by-one analysis                                                   | 0  |
| 5 | Interaction effects when features combine                   | Lockout-as-DoS interaction (Risk row 4); audit-log + bcrypt latency interaction (line 154) | 1  | No interaction-effect analysis                                           | 0  |

**Invariant & Edge Case: V1 = 2/5; V2 = 0/5**

### Edge Case Floor Check

Per protocol `edge_case_floor` rule:

- Threshold: 1/5
- Rule: Variants scoring <1/5 on Invariant & Edge Case Coverage are INELIGIBLE as base variant
- Suspension: When ALL variants score 0/5, suspend floor with warning

**Result**:

- V1: 2/5 → MEETS floor (≥1/5)
- V2: 0/5 → FAILS floor (<1/5)
- Not all variants at 0/5 → floor STANDS

**V2 IS INELIGIBLE AS BASE VARIANT** per the edge-case-floor rule.

### Qualitative Summary

| Dimension                          | V1 | V2 |
|------------------------------------|----|----|
| Completeness                       | 4  | 4  |
| Correctness                        | 4  | 3  |
| Structure                          | 4  | 4  |
| Clarity                            | 4  | 4  |
| Risk Coverage                      | 5  | 5  |
| Invariant & Edge Case Coverage     | 2  | 0  |
| **Total**                          | **23/30** | **20/30** |
| **qual_score**                     | **0.767** | **0.667** |

---

## Position-Bias Mitigation

| Criterion                          | Variant | Pass 1 (A→B order) | Pass 2 (B→A order) | Agreement | Final  |
|------------------------------------|---------|--------------------|---------------------|-----------|--------|
| Correctness #1 (no fact errors)    | V2      | NOT MET            | NOT MET             | Agree     | NOT MET |
| Correctness #2 (feasibility)       | V2      | NOT MET            | NOT MET             | Agree     | NOT MET |
| Invariant #2 (state interactions)  | V1      | MET                | MET                 | Agree     | MET    |
| Invariant #3 (guard gaps)          | V1      | MET                | MET                 | Agree     | MET    |
| All other 26 criteria              | both    | Agreement          | Agreement           | Agree     | (no change) |

**Disagreements found**: 0
**Verdicts changed**: 0

Dual-pass evaluation produced identical results in both orderings. No re-evaluation required.

---

## Combined Scoring

| Variant            | quant_score (×0.50) | qual_score (×0.50) | Combined | Rank |
|--------------------|---------------------|---------------------|----------|------|
| V1 opus:architect  | 0.4665              | 0.3835              | **0.850** | 1    |
| V2 sonnet:analyzer | 0.4790              | 0.3335              | **0.8125** | 2   |

**Margin**: 0.0375 (3.75% absolute, 4.4% relative)

---

## Tiebreaker Application

Margin 0.0375 < 0.05 → tiebreaker triggers.

### Level 1: Debate Performance

From `debate-transcript.md` Scoring Matrix:

- V1 won 19 of 35 diff points
- V2 won 10 of 35 diff points
- TIE: 5; QUALIFIED: 1

**Level 1 winner: V1** (decisive — 19 vs 10).

Tiebreaker resolved at Level 1; Levels 2-3 not invoked.

### Edge Case Floor Override

Independent of combined score and tiebreaker: **V2 is ineligible as base** per the edge-case-floor rule (V2 scored 0/5 on Invariant & Edge Case Coverage). Even if V2 had won the combined score, V2 could not be selected as base.

**Convergent verdict**: V1 wins on combined score, V1 wins on Level 1 tiebreaker, V2 is floor-ineligible. All three signals point to V1.

---

## Selected Base: Variant 1 (opus:architect)

### Selection Rationale

V1 is the stronger spine for the merged roadmap on three independent dimensions:

1. **Architectural depth** — V1 covers extension seams (MFA/OAuth), `kid` rotation, atomic Redis rotation, constant-time + dummy-verify, log-scrubber gate, email+IP composite lockout, pen-test, OpenTelemetry spans, audit-log impact analysis. V2 elides every one of these.

2. **API surface coherence** — V1's `TokenManager` API (`issue/refresh/revoke/revokeAll`) is internally consistent. V2's M3 D3.5 references `revokeAll` which V2's M2 never introduces — a silent integration defect.

3. **Edge case awareness** — V1 scores 2/5 on the Invariant & Edge Case dimension (above floor); V2 scores 0/5 (below floor → ineligible).

V2 wins decisively on **format and traceability**: Success Metrics table, FR×validation matrix, Performance & Reliability Gates table, Sprint-Level Breakdown, Out-of-Scope explicit table, Open Questions with target dates. These are the artifacts that make a roadmap audit-ready and operationally executable.

### Strengths to Preserve (from V1 Base)

- Foundations milestone (M1) with explicit ADR + OpenAPI freeze + RSA-key provisioning + SendGrid setup deliverables
- Critical-path dependency graph
- Cross-Cutting Concerns section (Observability, Security, Performance Budgets, Data Integrity)
- Workstreams model (5 parallel streams) — replace with merged Sprint+Workstream hybrid
- Pen-test as D5.1 deliverable
- `kid` header strategy + key rotation procedure
- Log-scrubber automated gate (D4.8)
- `TokenManager.issue/refresh/revoke/revokeAll` API surface from M2
- OpenTelemetry spans (D4.6)
- Bcrypt horizontal-scaling contingency

### Strengths to Incorporate (from V2)

- Success Metrics table at top (V2 §Success Metrics, 12 metrics with target/baseline/method/source)
- Per-FR Validation Strategy table (V2 §Validation Strategy, FR × Unit/Integration/E2E)
- Performance & Reliability Gates table (V2 §Performance & Reliability Gates)
- Sprint-Level Breakdown table (V2 §Sprint-Level Breakdown, S1-S6 with dates/owners)
- Out-of-Scope explicit table (V2 §Out-of-Scope, NG mapped to v1.1/v1.2/v2.0)
- Open Questions with target resolution dates (V2 §Open Questions)
- TDD §19.4 rollback trigger thresholds quoted verbatim (V2 §Performance & Reliability Gates)

### Required Additions from R2.5 Invariant Probe (HIGH-severity items)

These are NOT in either variant but MUST be added to merged output:

- **INV-001**: Frontend-team capacity confirmation as M1 precondition with named contact
- **INV-002**: SOC2 compliance reviewer named + booked for M4 control-mapping sign-off
- **INV-004**: Per-email backstop counter on lockout (in addition to email+IP composite) so IP-rotating attackers cannot bypass FR-AUTH-001 AC4
- **INV-005**: Atomic Redis rotation promoted from risk note to D3.2 acceptance test (LUA script or transaction verified)
- **INV-007**: M5 calendar resequenced — pen-test moves to end-M4 / start-M5 for 7-10 day remediation runway; GA buffer extended
- **INV-011**: pg-pool sizing reconciled with PostgreSQL max connections (200); PgBouncer or read-replica added as M1 deliverable
- **INV-013**: Rollback procedure reconciles `revokeAll` semantics — either stage-specific tokens are flushed on rollback, or rollback is forward-only after revokeAll events
