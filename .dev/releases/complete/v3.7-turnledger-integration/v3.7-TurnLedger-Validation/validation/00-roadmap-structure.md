# Roadmap Structure — v3.3 TurnLedger Validation

**Source**: `roadmap.md`
**Parsed**: 2026-03-23

## Top-Level Sections

| Section | Line Range | Type |
|---------|-----------|------|
| Executive Summary | L9-33 | Overview |
| Phase 1: Foundation | L38-64 | Phase |
| Phase 2: Core E2E Test Suites | L68-133 | Phase |
| Phase 3: Pipeline Fixes + Reachability Gate | L137-160 | Phase |
| Phase 4: Regression Validation + Final Audit | L164-179 | Phase |
| Risk Assessment | L183-193 | Governance |
| Resource Requirements | L197-240 | Governance |
| Success Criteria Validation Matrix | L244-259 | Governance |
| Timeline Summary | L263-275 | Governance |
| Open Questions | L279-290 | Governance |
| Appendix A: Integration Point Registry | L294-367 | Reference |

## Task Inventory

### Phase 1A: Audit Trail (FR-7)
| Task ID | Requirement | Description |
|---------|-------------|-------------|
| 1A.1 | FR-7.1 | JSONL audit writer with 9-field schema |
| 1A.2 | FR-7.3 | audit_trail pytest fixture |
| 1A.3 | FR-7.3 | Summary report at session end |
| 1A.4 | FR-7.2 | Verification test for 4 properties |

### Phase 1B: AST Reachability (FR-4)
| Task ID | Requirement | Description |
|---------|-------------|-------------|
| 1B.1 | FR-4.1 | Wiring manifest YAML schema |
| 1B.2 | FR-4.2 | AST call-chain analyzer module |
| 1B.3 | FR-4.2 | Documented limitations |
| 1B.4 | FR-4.1 | Initial wiring manifest YAML |
| 1B.5 | FR-4.4 | Unit tests for AST analyzer |

### Phase 2A: Wiring Point E2E (FR-1)
| Task ID | Requirements | Test Count |
|---------|-------------|------------|
| 2A.1 | FR-1.1–FR-1.4 | 4 |
| 2A.2 | FR-1.5–FR-1.6 | 2 |
| 2A.3 | FR-1.7 | 2 |
| 2A.4 | FR-1.8 | 1 |
| 2A.5 | FR-1.9–FR-1.10 | 2 |
| 2A.6 | FR-1.11 | 1 |
| 2A.7 | FR-1.12 | 1 |
| 2A.8 | FR-1.13 | 1 |
| 2A.9 | FR-1.14, FR-1.14a-c | 3 |
| 2A.10 | FR-1.15–FR-1.16 | 2 |
| 2A.11 | FR-1.17 | 1 |
| 2A.12 | FR-1.18 | 1 |

### Phase 2B: TurnLedger Lifecycle (FR-2)
| Task ID | Requirement | Description |
|---------|-------------|-------------|
| 2B.1 | FR-2.1 | Convergence path E2E |
| 2B.2 | FR-2.2 | Sprint per-task path |
| 2B.3 | FR-2.3 | Sprint per-phase path |
| 2B.4 | FR-2.4 | Cross-path coherence |

### Phase 2C: Gate Rollout Modes (FR-3)
| Task ID | Requirement | Test Count |
|---------|-------------|------------|
| 2C.1 | FR-3.1a–FR-3.1d | 8 |
| 2C.2 | FR-3.2a–FR-3.2d | 4 |
| 2C.3 | FR-3.3 | 1 |

### Phase 2D: QA Gaps (FR-6)
| Task ID | Requirement | Description |
|---------|-------------|-------------|
| 2D.1 | FR-6.1 T07 | Convergence wiring tests |
| 2D.2 | FR-6.1 T11 | Convergence E2E tests |
| 2D.3 | FR-6.1 T12 | Smoke test |
| 2D.4 | FR-6.1 T14 | Wiring-verification artifact |
| 2D.5 | FR-6.2 T02 | Confirming test |
| 2D.6 | FR-6.2 T17-T22 | Integration + regression |

### Phase 3A: Production Changes
| Task ID | Requirement | File Modified |
|---------|-------------|---------------|
| 3A.1 | FR-5.1 | wiring_gate.py |
| 3A.2 | FR-5.2 | NEW: fidelity_checker.py |
| 3A.3 | FR-5.2 | executor.py (_run_checkers) |
| 3A.4 | FR-4.3 | reachability.py |

### Phase 3B: Validation Tests
| Task ID | Requirement | Description |
|---------|-------------|-------------|
| 3B.1 | FR-5.1, SC-10 | 0-files test |
| 3B.2 | FR-4.4, SC-7, SC-9 | Regression test |
| 3B.3 | FR-5.2, SC-11 | Fidelity checker test |

### Phase 4: Final Validation
| Task ID | Requirement | Description |
|---------|-------------|-------------|
| 4.1 | NFR-3, SC-4 | Full suite regression |
| 4.2 | NFR-1 | No-mock grep audit |
| 4.3 | FR-7.2, SC-12 | Audit trail review |
| 4.4 | NFR-5 | Manifest completeness |
| 4.5 | — | Wiring-verification artifact |
| 4.6 | — | Solutions learned update |

## Gates / Checkpoints

| Checkpoint | Phase | Pass Criteria |
|-----------|-------|---------------|
| A | 1 | Audit trail produces valid JSONL; AST analyzer resolves imports |
| B | 2 | All E2E tests pass; SC-1–6, SC-8, SC-12 validated |
| C | 3 | Production fixes shipped; SC-7, SC-9, SC-10, SC-11 validated |
| D (Release) | 4 | Zero regressions; all 12 SC green; evidence package complete |

## Dependencies

- Phase 1A → Phase 2 (audit fixture required)
- Phase 1B → Phase 3 (AST analyzer required)
- Phase 1A ∥ Phase 1B (can run in parallel)
- Phase 2 → Phase 4
- Phase 3 → Phase 4
- Critical path: 1A → 2 → 4
