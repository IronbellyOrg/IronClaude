# Decomposition Plan
**Extraction date**: 2026-03-23

---

## Domain Agent Assignments

### AGENT-D1: Wiring Point E2E Tests
- **Domain**: wiring_e2e_tests
- **Requirements**: REQ-001–REQ-023, REQ-SC1, REQ-SC5, REQ-RISK2 (25 requirements)
- **Spec sections**: FR-1.1–FR-1.21, SC-1, SC-5
- **Roadmap sections**: Phase 2A tasks 2A.1–2A.12
- **Cross-cutting**: REQ-002 (no-mock constraint), REQ-NFR4 (audit trail)
- **Output**: 01-agent-D1-wiring-e2e-tests.md

### AGENT-D2: TurnLedger Lifecycle
- **Domain**: turnledger_lifecycle
- **Requirements**: REQ-024–REQ-028, REQ-SC2 (6 requirements)
- **Spec sections**: FR-2.1, FR-2.1a, FR-2.2, FR-2.3, FR-2.4, SC-2
- **Roadmap sections**: Phase 2B tasks 2B.1–2B.4
- **Cross-cutting**: REQ-NFR4 (audit trail)
- **Output**: 01-agent-D2-turnledger-lifecycle.md

### AGENT-D3: Gate Rollout Modes
- **Domain**: gate_rollout_modes
- **Requirements**: REQ-029–REQ-038, REQ-SC3, REQ-SC6 (12 requirements)
- **Spec sections**: FR-3.1a–d, FR-3.2a–d, FR-3.3, SC-3, SC-6
- **Roadmap sections**: Phase 2C tasks 2C.1–2C.3
- **Cross-cutting**: REQ-NFR4 (audit trail)
- **Output**: 01-agent-D3-gate-rollout-modes.md

### AGENT-D4: Reachability Framework
- **Domain**: reachability_framework
- **Requirements**: REQ-039–REQ-043, REQ-NFR5, REQ-NFR6, REQ-SC7, REQ-SC9, REQ-RISK1 (9 requirements)
- **Spec sections**: FR-4.1–FR-4.4, NFR-5, NFR-6, SC-7, SC-9
- **Roadmap sections**: Phase 1B tasks 1B.1–1B.5, Phase 3A.4, Phase 3B.2, Phase 4.4
- **Output**: 01-agent-D4-reachability-framework.md

### AGENT-D5: Pipeline Fixes
- **Domain**: pipeline_fixes
- **Requirements**: REQ-044–REQ-049, REQ-SC10, REQ-SC11, REQ-RISK3 (9 requirements)
- **Spec sections**: FR-5.1, FR-5.2, FR-5.3, SC-10, SC-11
- **Roadmap sections**: Phase 3A.1–3A.3, Phase 3B.1, Phase 3B.3
- **Output**: 01-agent-D5-pipeline-fixes.md

### AGENT-D6: QA Gaps
- **Domain**: qa_gaps
- **Requirements**: REQ-050–REQ-055, REQ-SC8 (7 requirements)
- **Spec sections**: FR-6.1 T07/T11/T12/T14, FR-6.2 T02/T17-T22, SC-8
- **Roadmap sections**: Phase 2D tasks 2D.1–2D.6
- **Output**: 01-agent-D6-qa-gaps.md

### AGENT-D7: Audit Trail
- **Domain**: audit_trail
- **Requirements**: REQ-056–REQ-058, REQ-NFR4, REQ-SC12 (5 requirements)
- **Spec sections**: FR-7.1, FR-7.2, FR-7.3, NFR-4, SC-12
- **Roadmap sections**: Phase 1A tasks 1A.1–1A.4
- **Output**: 01-agent-D7-audit-trail.md

---

## Mandatory Cross-Cutting Agent Assignments

### CC1: Internal Consistency (Roadmap)
- **Scope**: Full roadmap.md
- **Focus**: ID schema consistency, count consistency (frontmatter vs body), table-to-prose consistency, cross-reference validity, no duplicate IDs, no orphaned items
- **Output**: 01-agent-CC1-roadmap-consistency.md

### CC2: Internal Consistency (Spec)
- **Scope**: Full v3.3-requirements-spec.md
- **Focus**: Section cross-references valid, requirement counts match, no contradictory statements, numeric values consistent
- **Output**: 01-agent-CC2-spec-consistency.md

### CC3: Dependency & Ordering
- **Scope**: Roadmap + spec
- **Focus**: Spec dependency chains respected in roadmap ordering, no circular deps, infrastructure before features, one-way-door operations gated
- **Output**: 01-agent-CC3-dependency-ordering.md

### CC4: Completeness Sweep
- **Scope**: Everything
- **Focus**: Re-scan full spec for missed requirements, verify every REQ has coverage claim, check for implicit systems required by explicit ones
- **Output**: 01-agent-CC4-completeness-sweep.md

---

## Cross-Cutting Concern Matrix

| Requirement | Primary Agent | Secondary Agents | Integration Risk |
|-------------|--------------|------------------|-----------------|
| REQ-002 (no-mock constraint) | D1 | D2, D3, D6 | HIGH |
| REQ-NFR1 (no-mock NFR) | Constraints/CC | D1, D2, D3 | HIGH |
| REQ-NFR4 (every test → JSONL) | D7 | D1, D2, D3, D6 | HIGH |
| REQ-NFR3 (≥4894 baseline) | CC3 | All | MEDIUM |
| REQ-049 (FR-5.3 = FR-4 xref) | D5 | D4 | LOW |
| REQ-SC4 (zero regressions) | CC3 | All | MEDIUM |

---

## Completeness Verification

Union of all agent requirement assignments:
- D1: REQ-001–023 + SC1, SC5, RISK2 = 25
- D2: REQ-024–028 + SC2 = 6
- D3: REQ-029–038 + SC3, SC6 = 12
- D4: REQ-039–043 + NFR5, NFR6, SC7, SC9, RISK1 = 9
- D5: REQ-044–049 + SC10, SC11, RISK3 = 9
- D6: REQ-050–055 + SC8 = 7
- D7: REQ-056–058 + NFR4, SC12 = 5
- Constraints (CC3): NFR1–3, PROC1–3, SC4 = 8

**Total assigned**: 81
**Total requirement universe**: 76 in-scope (+ 5 P3 out-of-scope)
**Status**: All in-scope requirements assigned ✓
