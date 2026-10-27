# Domain Taxonomy — v3.3 TurnLedger Validation

**Generated**: 2026-03-23
**Total domains**: 7
**Total requirements**: 84

## Domains

### D1: Wiring E2E (wiring-e2e)
- **Boundary**: FR-1.x wiring point tests, construction validation, hook invocation, lifecycle assertions
- **Requirements**: REQ-001 through REQ-023, REQ-062, REQ-066, REQ-085
- **Count**: 25
- **Primary roadmap sections**: Phase 2A

### D2: TurnLedger Lifecycle (turnledger-lifecycle)
- **Boundary**: FR-2.x debit/credit/reimbursement cycles across all 4 execution paths
- **Requirements**: REQ-024 through REQ-029, REQ-063
- **Count**: 7
- **Primary roadmap sections**: Phase 2B

### D3: Gate Modes (gate-modes)
- **Boundary**: FR-3.x rollout mode matrix, budget exhaustion scenarios, interrupted sprint
- **Requirements**: REQ-030 through REQ-040, REQ-064, REQ-067
- **Count**: 13
- **Primary roadmap sections**: Phase 2C

### D4: Reachability (reachability)
- **Boundary**: FR-4.x AST analyzer, wiring manifest, reachability gate, regression test
- **Requirements**: REQ-041 through REQ-046, REQ-068, REQ-070, REQ-079, REQ-084
- **Count**: 10
- **Primary roadmap sections**: Phase 1B, Phase 3A.4, Phase 3B.2

### D5: Pipeline Fixes (pipeline-fixes)
- **Boundary**: FR-5.x 0-files assertion, impl-vs-spec fidelity checker
- **Requirements**: REQ-047 through REQ-052, REQ-071, REQ-072, REQ-086, REQ-088
- **Count**: 10
- **Primary roadmap sections**: Phase 3A.1–3A.3, Phase 3B.1, Phase 3B.3

### D6: Audit Trail (audit-trail)
- **Boundary**: FR-7.x JSONL writer, pytest fixture, verifiability, audit constraint
- **Requirements**: REQ-059 through REQ-061, REQ-073, REQ-078, REQ-087
- **Count**: 6
- **Primary roadmap sections**: Phase 1A

### D7: QA Gaps (qa-gaps)
- **Boundary**: FR-6.x remaining test gaps from v3.05 and v3.2, plus regression baseline
- **Requirements**: REQ-053 through REQ-058, REQ-065, REQ-069
- **Count**: 8
- **Primary roadmap sections**: Phase 2D, Phase 4

### Cross-Cutting (not a domain — assigned to CC agents)
- **Requirements**: REQ-002, REQ-035, REQ-065, REQ-074, REQ-075, REQ-076, REQ-077, REQ-078, REQ-080 through REQ-083, REQ-089
- **Count**: 13 (overlap with domain assignments — primary domain takes precedence)

## Assignment Verification

| Domain | Primary Count | Cross-Cut Touch |
|--------|--------------|----------------|
| D1: Wiring E2E | 25 | REQ-002, REQ-075, REQ-085 |
| D2: TurnLedger | 7 | — |
| D3: Gate Modes | 13 | REQ-035 |
| D4: Reachability | 10 | REQ-079 |
| D5: Pipeline Fixes | 10 | REQ-086, REQ-088 |
| D6: Audit Trail | 6 | REQ-078, REQ-087 |
| D7: QA Gaps | 8 | REQ-065 |
| **Subtotal** | **79** | — |
| Sequencing-only | 4 | REQ-080–083 |
| Layout constraint | 1 | REQ-089 |
| **Grand total** | **84** | — |

All 84 requirements assigned. Zero unassigned.
