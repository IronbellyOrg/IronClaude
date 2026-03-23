# Domain Taxonomy
**Extraction date**: 2026-03-23

---

## Domain Definitions

7 requirement domains identified from spec + roadmap analysis. Capped to allow 4 cross-cutting agent slots.

| Domain | Slug | Requirement Count | Primary Agent | Description |
|--------|------|-------------------|---------------|-------------|
| Wiring Point E2E Tests | wiring_e2e_tests | 23 (REQ-001–023, SC1, SC5, RISK2) | AGENT-D1 | FR-1 tests: all 21 wiring point validation tests + constraint + SC |
| TurnLedger Lifecycle | turnledger_lifecycle | 6 (REQ-024–028, SC2) | AGENT-D2 | FR-2 tests: 5 lifecycle paths + SC-2 |
| Gate Rollout Modes | gate_rollout_modes | 9 (REQ-029–038, SC3, SC6) | AGENT-D3 | FR-3 tests: mode matrix, budget exhaustion, interrupt |
| Reachability Framework | reachability_framework | 7 (REQ-039–043, NFR5, NFR6, SC7, SC9, RISK1) | AGENT-D4 | FR-4: AST analyzer, manifest, gate integration, regression test |
| Pipeline Fixes | pipeline_fixes | 7 (REQ-044–049, SC10, SC11, RISK3) | AGENT-D5 | FR-5: 0-files assertion, impl-vs-spec checker |
| QA Gaps | qa_gaps | 7 (REQ-050–055, SC8) | AGENT-D6 | FR-6: convergence wiring tests, e2e tests, QA gap closure |
| Audit Trail | audit_trail | 5 (REQ-056–058, NFR4, SC12) | AGENT-D7 | FR-7: JSONL writer, fixture, verifiability |
| Constraints/Process | constraints | 8 (REQ-NFR1–3, PROC1–3, SC4) | Cross-cutting | NFRs, sequencing, baseline, branch |

---

## Cross-Cutting Requirements Matrix

| Requirement | Primary Domain | Secondary Domains | Rationale |
|-------------|---------------|-------------------|-----------|
| REQ-002 (no mocking constraint) | wiring_e2e_tests | ALL | Applies to every test in every domain |
| REQ-NFR1 (no mocking NFR) | constraints | wiring_e2e_tests, turnledger_lifecycle, gate_rollout_modes | Universal injection rule |
| REQ-NFR4 (every test emits JSONL) | audit_trail | wiring_e2e_tests, turnledger_lifecycle, gate_rollout_modes, qa_gaps | Audit trail required for all test domains |
| REQ-NFR3 (≥4894 passed) | constraints | ALL | Release gate applies to all domains |
| REQ-056 (FR-7.1 schema) | audit_trail | wiring_e2e_tests | Every wiring test must emit this schema |
| REQ-049 (FR-5.3 = FR-4) | pipeline_fixes | reachability_framework | Cross-reference requirement |

---

## Agent Allocations

| Agent | Domain | Requirement IDs |
|-------|--------|----------------|
| AGENT-D1 | wiring_e2e_tests | REQ-001, REQ-002, REQ-003–REQ-023, REQ-SC1, REQ-SC5, REQ-RISK2 |
| AGENT-D2 | turnledger_lifecycle | REQ-024–028, REQ-SC2 |
| AGENT-D3 | gate_rollout_modes | REQ-029–038, REQ-SC3, REQ-SC6 |
| AGENT-D4 | reachability_framework | REQ-039–043, REQ-NFR5, REQ-NFR6, REQ-SC7, REQ-SC9, REQ-RISK1 |
| AGENT-D5 | pipeline_fixes | REQ-044–049, REQ-SC10, REQ-SC11, REQ-RISK3 |
| AGENT-D6 | qa_gaps | REQ-050–055, REQ-SC8 |
| AGENT-D7 | audit_trail | REQ-056–058, REQ-NFR4, REQ-SC12 |
| CC1 | Internal Consistency (Roadmap) | Full roadmap |
| CC2 | Internal Consistency (Spec) | Full spec |
| CC3 | Dependency & Ordering | Sequencing constraints |
| CC4 | Completeness Sweep | All unassigned requirements |

**Total domain agents**: 7
**Total cross-cutting agents**: 4
**Total agents**: 11 (within max-agents=20 limit)
