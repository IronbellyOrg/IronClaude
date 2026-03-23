# v3.3 Domain Taxonomy

Built from requirement universe and roadmap structure.
Date: 2026-03-23

---

## Domain Detection

Requirements cluster into 6 natural domains based on spec section headers, technology referenced, and system boundaries.

---

## Domains

### D1: Wiring E2E Tests
**Requirements**: FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5, FR-1.6, FR-1.7, FR-1.8, FR-1.9, FR-1.10, FR-1.11, FR-1.12, FR-1.13, FR-1.14, FR-1.14a, FR-1.14b, FR-1.14c, FR-1.15, FR-1.16, FR-1.17, FR-1.18, SC-1, SC-5, OQ-5
**Count**: 24
**Primary spec sections**: FR-1 (all sub-items), SC-1, SC-5
**Roadmap phases**: 2A
**Rationale**: All relate to E2E validation of executor wiring points. Largest coherent domain.

### D2: TurnLedger Lifecycle
**Requirements**: FR-2.1, FR-2.2, FR-2.3, FR-2.4, SC-2, OQ-6
**Count**: 6
**Primary spec sections**: FR-2, SC-2
**Roadmap phases**: 2B
**Rationale**: All relate to TurnLedger debit/credit/reimbursement lifecycle across execution paths.

### D3: Gate Modes & Budget Exhaustion
**Requirements**: FR-3.1a, FR-3.1b, FR-3.1c, FR-3.1d, FR-3.1-AC1, FR-3.1-AC2, FR-3.1-AC3, FR-3.1-AC4, FR-3.2a, FR-3.2b, FR-3.2c, FR-3.2d, FR-3.3, SC-3, SC-6, OQ-1
**Count**: 16
**Primary spec sections**: FR-3, SC-3, SC-6
**Roadmap phases**: 2C
**Rationale**: Gate rollout mode behavior and budget exhaustion are tightly coupled.

### D4: Reachability Framework
**Requirements**: FR-4.1, FR-4.2, FR-4.2-LIM1, FR-4.2-LIM2, FR-4.2-LIM3, FR-4.3, FR-4.4, FR-5.3, NFR-5, NFR-6, SC-7, SC-9, RISK-1, FILE-NEW-1, OQ-4, OQ-8
**Count**: 16
**Primary spec sections**: FR-4, FR-5.3, NFR-5, NFR-6
**Roadmap phases**: 1B, 3A.4, 3B.2
**Rationale**: AST analyzer, wiring manifest, and reachability gate form a single technical domain.

### D5: Pipeline Fixes & Fidelity
**Requirements**: FR-5.1, FR-5.1-TEST, FR-5.2, FR-5.2-TEST, SC-10, SC-11, RISK-3, RISK-5, FILE-NEW-2, FILE-MOD-1, FILE-MOD-2, OQ-2
**Count**: 12
**Primary spec sections**: FR-5, SC-10, SC-11
**Roadmap phases**: 3A.1–3A.3, 3B.1, 3B.3
**Rationale**: 0-files-analyzed assertion and impl-vs-spec fidelity checker are both pipeline hardening.

### D6: Audit Trail Infrastructure
**Requirements**: FR-7.1, FR-7.2, FR-7.2-PROP1, FR-7.2-PROP2, FR-7.2-PROP3, FR-7.2-PROP4, FR-7.3, NFR-4, SC-12, RISK-4, OQ-3
**Count**: 11
**Primary spec sections**: FR-7, NFR-4, SC-12
**Roadmap phases**: 1A
**Rationale**: JSONL writer, fixture, verifiability properties form a cohesive infrastructure domain.

### D7: QA Gap Closure
**Requirements**: FR-6.1-T07, FR-6.1-T11, FR-6.1-T12, FR-6.1-T14, FR-6.2-T02, FR-6.2-T17-T22, SC-8, FILE-MOD-3, FILE-MOD-4
**Count**: 9
**Primary spec sections**: FR-6, SC-8
**Roadmap phases**: 2D
**Rationale**: Gap closure tests for v3.05 and v3.2 outstanding items.

---

## Cross-Cutting / Shared Requirements (assigned to primary domain but flagged)

| Requirement | Primary Domain | Secondary Domains | Reason |
|-------------|---------------|-------------------|--------|
| FR-1-CONSTRAINT / NFR-1 | Testing Constraints (cross-cutting) | D1, D2, D3, D7 | No-mock constraint applies to all test domains |
| NFR-2 | Testing Constraints (cross-cutting) | All | UV-only applies globally |
| NFR-3 / SC-4 | Testing Constraints (cross-cutting) | All | Baseline regression applies to all |
| FR-1.7 | D1 | D7 (FR-6.2-T02) | Post-phase wiring hook is also a QA gap closure item |
| FR-2.4 | D2 | D1, D3 | Cross-path coherence touches wiring and gate modes |
| FR-4.3 / FR-5.2 | D4, D5 | D6 (audit trail cross-cutting) | Pipeline integration points |
| FR-7.1 / NFR-4 | D6 | All test domains | Every test must emit audit record |
| SEQ-1 through SEQ-4 | Sequencing (cross-cutting) | All | Phase ordering applies globally |

---

## Domain Count Validation

| Domain | Req Count | Notes |
|--------|----------|-------|
| D1: Wiring E2E | 24 | Largest; within 20-cap, thematically tight |
| D2: TurnLedger Lifecycle | 6 | Focused |
| D3: Gate Modes & Budget | 16 | Could split but modes/budget are inseparable |
| D4: Reachability Framework | 16 | Includes manifest + analyzer + gate |
| D5: Pipeline Fixes & Fidelity | 12 | 0-files + fidelity checker |
| D6: Audit Trail | 11 | Infrastructure |
| D7: QA Gap Closure | 9 | Gap closure tests |
| **TOTAL domain agents** | **7** | Below 16-cap |
| **Cross-cutting agents** | **4** | Mandatory |
| **TOTAL agents** | **11** | Below 20-cap |

---

## Excluded Requirements

The following are tagged P3 (out-of-scope) and excluded from coverage calculations:

- SCOPE-OUT-1 through SCOPE-OUT-5
- RISK-2 (mitigation: already handled by _subprocess_factory constraint in NFR-1)
- OQ-7 (investigation task, not a coverage item)
- FILE-NEW-3 (structural/organizational, not a functional requirement)

**Active requirement count for validation**: 89 total - 8 excluded = **81 active requirements**
