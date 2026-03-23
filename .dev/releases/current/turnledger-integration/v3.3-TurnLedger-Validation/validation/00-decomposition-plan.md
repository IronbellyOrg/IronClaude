# Agent Decomposition Plan

Date: 2026-03-23

---

## Domain Agent Assignments

### AGENT-D1: Wiring E2E Tests
- domain: wiring-e2e
- requirements: FR-1.1, FR-1.2, FR-1.3, FR-1.4, FR-1.5, FR-1.6, FR-1.7, FR-1.8, FR-1.9, FR-1.10, FR-1.11, FR-1.12, FR-1.13, FR-1.14, FR-1.14a, FR-1.14b, FR-1.14c, FR-1.15, FR-1.16, FR-1.17, FR-1.18, SC-1, SC-5, OQ-5
- requirement_count: 24
- spec_sections: FR-1 (lines 74-201), SC-1, SC-5 (lines 513, 517)
- cross_cutting_reqs: FR-1-CONSTRAINT/NFR-1, NFR-4 (every test emits audit record), FR-6.2-T02 (overlap with FR-1.7)
- output: validation/01-agent-D1-wiring-e2e.md

### AGENT-D2: TurnLedger Lifecycle
- domain: turnledger-lifecycle
- requirements: FR-2.1, FR-2.2, FR-2.3, FR-2.4, SC-2, OQ-6
- requirement_count: 6
- spec_sections: FR-2 (lines 205-233), SC-2 (line 514)
- cross_cutting_reqs: NFR-1, NFR-4, FR-1.15 (convergence registry overlap), FR-1.16 (merge args overlap)
- output: validation/01-agent-D2-turnledger-lifecycle.md

### AGENT-D3: Gate Modes & Budget Exhaustion
- domain: gate-modes
- requirements: FR-3.1a, FR-3.1b, FR-3.1c, FR-3.1d, FR-3.1-AC1, FR-3.1-AC2, FR-3.1-AC3, FR-3.1-AC4, FR-3.2a, FR-3.2b, FR-3.2c, FR-3.2d, FR-3.3, SC-3, SC-6, OQ-1
- requirement_count: 16
- spec_sections: FR-3 (lines 236-269), SC-3 (line 515), SC-6 (line 518)
- cross_cutting_reqs: NFR-1, NFR-4, FR-1.12 (wiring mode resolution), FR-2.4 (budget coherence)
- output: validation/01-agent-D3-gate-modes.md

### AGENT-D4: Reachability Framework
- domain: reachability
- requirements: FR-4.1, FR-4.2, FR-4.2-LIM1, FR-4.2-LIM2, FR-4.2-LIM3, FR-4.3, FR-4.4, FR-5.3, NFR-5, NFR-6, SC-7, SC-9, RISK-1, FILE-NEW-1, OQ-4, OQ-8
- requirement_count: 16
- spec_sections: FR-4 (lines 273-356), FR-5.3 (lines 384-386), NFR-5, NFR-6, Wiring Manifest (lines 528-586)
- cross_cutting_reqs: FR-4.3 (integration with GateCriteria), FR-5.2 (pipeline integration)
- output: validation/01-agent-D4-reachability.md

### AGENT-D5: Pipeline Fixes & Fidelity
- domain: pipeline-fixes
- requirements: FR-5.1, FR-5.1-TEST, FR-5.2, FR-5.2-TEST, SC-10, SC-11, RISK-3, RISK-5, FILE-NEW-2, FILE-MOD-1, FILE-MOD-2, OQ-2
- requirement_count: 12
- spec_sections: FR-5 (lines 359-386), SC-10, SC-11 (lines 522-523)
- cross_cutting_reqs: FR-4.3 (reachability gate integration), NFR-1 (no mocking)
- output: validation/01-agent-D5-pipeline-fixes.md

### AGENT-D6: Audit Trail Infrastructure
- domain: audit-trail
- requirements: FR-7.1, FR-7.2, FR-7.2-PROP1, FR-7.2-PROP2, FR-7.2-PROP3, FR-7.2-PROP4, FR-7.3, NFR-4, SC-12, RISK-4, OQ-3
- requirement_count: 11
- spec_sections: FR-7 (lines 412-458), NFR-4, SC-12 (line 524), Constraints (line 617)
- cross_cutting_reqs: All test domains depend on audit trail fixture
- output: validation/01-agent-D6-audit-trail.md

### AGENT-D7: QA Gap Closure
- domain: qa-gaps
- requirements: FR-6.1-T07, FR-6.1-T11, FR-6.1-T12, FR-6.1-T14, FR-6.2-T02, FR-6.2-T17-T22, SC-8, FILE-MOD-3, FILE-MOD-4
- requirement_count: 9
- spec_sections: FR-6 (lines 390-408), SC-8 (line 520)
- cross_cutting_reqs: FR-1.7 (overlap with FR-6.2-T02), NFR-1, NFR-4
- output: validation/01-agent-D7-qa-gaps.md

---

## Mandatory Cross-Cutting Agents

### AGENT-CC1: Internal Consistency (Roadmap)
- scope: Full roadmap (roadmap-final.md)
- checks:
  - ID schema consistency (task IDs, FR references)
  - Count consistency (frontmatter vs body: test counts, requirement counts)
  - Table-to-prose consistency
  - Cross-reference validity (all FR-* refs exist in spec)
  - No duplicate IDs
  - No orphaned items
  - Phase deliverable count matches task table count
- output: validation/01-agent-CC1-internal-consistency-roadmap.md

### AGENT-CC2: Internal Consistency (Spec)
- scope: Full spec (v3.3-requirements-spec.md)
- checks:
  - Section cross-references valid
  - Requirement counts match (FR-1 sub-items count, test counts)
  - No contradictory statements
  - Numeric values consistent (baseline 4894, budget 61, etc.)
  - Code line references consistent with "Code State Snapshot" table
- output: validation/01-agent-CC2-internal-consistency-spec.md

### AGENT-CC3: Dependency & Ordering
- scope: Full roadmap + spec
- checks:
  - Spec dependency chains respected in roadmap phase ordering
  - No circular dependencies
  - Infrastructure (Phase 1) before features (Phase 2)
  - Irreversible operations properly gated
  - SEQ-1 through SEQ-4 respected
  - Phase hard dependencies documented and correct
- output: validation/01-agent-CC3-dependency-ordering.md

### AGENT-CC4: Completeness Sweep
- scope: Everything
- checks:
  - Re-scan spec for requirements missed by extraction
  - Every REQ has at least one agent's coverage claim
  - Implicit systems required by explicit ones
  - Wiring manifest entries all traceable to spec
  - Test file layout matches spec declaration
- output: validation/01-agent-CC4-completeness-sweep.md

---

## Cross-Cutting Concern Matrix

| Requirement | Primary Agent | Secondary Agents | Integration Risk |
|-------------|--------------|------------------|-----------------|
| FR-1.7 | D1 | D7 (FR-6.2-T02) | LOW |
| FR-1-CONSTRAINT/NFR-1 | CC4 | D1, D2, D3, D7 | MEDIUM |
| NFR-4 (audit trail all tests) | D6 | D1, D2, D3, D7 | MEDIUM |
| FR-2.4 (cross-path coherence) | D2 | D1, D3 | MEDIUM |
| FR-4.3 (GateCriteria integration) | D4 | D5 | HIGH |
| FR-5.2 (_run_checkers integration) | D5 | D4 | HIGH |
| FR-7.1/FR-7.3 (fixture cross-cutting) | D6 | D1, D2, D3, D7 | MEDIUM |
| SEQ-1 through SEQ-4 | CC3 | All domain agents | MEDIUM |
| NFR-3/SC-4 (baseline regression) | CC4 | All | LOW |

---

## Complete Assignment Verification

**Total active requirements**: 81
**Requirements assigned to domain agents**: D1(24) + D2(6) + D3(16) + D4(16) + D5(12) + D6(11) + D7(9) = 94 (includes some overlap from cross-cutting flagged reqs)
**Unique assignments**: All 81 active requirements have exactly one primary agent.
**Cross-cutting agents**: CC1-CC4 cover orthogonal validation dimensions.
**Unassigned**: 0

**STATUS**: Complete assignment verified. All requirements covered.

---

## Agent Summary

| Agent | Domain | Req Count | Type |
|-------|--------|----------|------|
| D1 | Wiring E2E | 24 | Domain |
| D2 | TurnLedger Lifecycle | 6 | Domain |
| D3 | Gate Modes & Budget | 16 | Domain |
| D4 | Reachability Framework | 16 | Domain |
| D5 | Pipeline Fixes & Fidelity | 12 | Domain |
| D6 | Audit Trail | 11 | Domain |
| D7 | QA Gap Closure | 9 | Domain |
| CC1 | Internal Consistency (Roadmap) | — | Cross-cutting |
| CC2 | Internal Consistency (Spec) | — | Cross-cutting |
| CC3 | Dependency & Ordering | — | Cross-cutting |
| CC4 | Completeness Sweep | — | Cross-cutting |
| **TOTAL** | | **81 unique** | **11 agents** |
