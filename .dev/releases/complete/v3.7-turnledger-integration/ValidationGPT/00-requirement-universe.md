# Requirement Universe

## Spec File Reference Status (Step 0.1.5)

| Referenced Path | Source | Status | Notes |
|---|---|---|---|
| `src/superclaude/cli/audit/reachability.py` | spec.md:L216, L359-L383 | NOT FOUND | Planned new file |
| `src/superclaude/cli/roadmap/fidelity_checker.py` | spec.md:L403-L414 | NOT FOUND | Planned new file |
| `tests/v3.3/conftest.py` | spec.md:L629-L636 | NOT FOUND | Planned new file |
| `tests/v3.3/test_reachability_eval.py` | spec.md:L635 | NOT FOUND | Planned new file |
| `tests/v3.3/test_wiring_points_e2e.py` | roadmap.md:L76-L93 | NOT FOUND | Planned new file |
| `tests/v3.3/test_turnledger_lifecycle.py` | roadmap.md:L97-L106 | NOT FOUND | Planned new file |
| `tests/v3.3/test_gate_rollout_modes.py` | roadmap.md:L110-L118 | NOT FOUND | Planned new file |
| `tests/v3.3/test_integration_regression.py` | roadmap.md:L129 | NOT FOUND | Planned new file |
| `tests/v3.3/wiring_manifest.yaml` | spec.md:L563-L621 | NOT FOUND | Planned new file |
| `tests/audit-trail/test_audit_writer.py` | roadmap.md:L225 | NOT FOUND | Planned new file |

**Note**: NOT FOUND references are informational only and may represent files to be created by the release.

## Extraction Summary

- Source spec: `v3.3-requirements-spec.md`
- Extraction mode: explicit requirements + key derived constraints
- Minimum extracted universe: **54 requirements**
- Primary domains: wiring-e2e, lifecycle-and-modes, reachability-and-pipeline, audit-and-quality-gates

## Domain Inventory

| Domain | Requirement IDs / Areas |
|---|---|
| Wiring E2E | FR-1.1–FR-1.21, SC-1, SC-5 |
| Lifecycle & Modes | FR-2.1–FR-2.4, FR-2.1a, FR-3.1a–FR-3.3, SC-2, SC-3, SC-6 |
| Reachability & Pipeline | FR-4.1–FR-4.4, FR-5.1–FR-5.3, FR-6.1, FR-6.2, SC-7, SC-8, SC-9, SC-10, SC-11 |
| Audit & Quality Gates | FR-7.1–FR-7.3, NFR-1, NFR-2, NFR-3, NFR-5, NFR-6, SC-4, SC-12 |

## High-Signal Atomic Requirements Extracted

| ID | Type | Priority | Domain | Source |
|---|---|---|---|---|
| REQ-001 | TEST | P0 | Wiring E2E | FR-1.1 TurnLedger construction validation |
| REQ-002 | TEST | P0 | Wiring E2E | FR-1.2 ShadowGateMetrics construction |
| REQ-003 | TEST | P0 | Wiring E2E | FR-1.3 DeferredRemediationLog construction |
| REQ-004 | TEST | P0 | Wiring E2E | FR-1.4 SprintGatePolicy construction |
| REQ-005 | TEST | P0 | Wiring E2E | FR-1.5 task-inventory delegation |
| REQ-006 | TEST | P0 | Wiring E2E | FR-1.6 freeform fallback path |
| REQ-007 | TEST | P0 | Wiring E2E | FR-1.7 both post-phase wiring hook call sites |
| REQ-008 | TEST | P0 | Wiring E2E | FR-1.8 anti-instinct hook tuple return |
| REQ-009 | TEST | P0 | Wiring E2E | FR-1.9 all_gate_results accumulation |
| REQ-010 | TEST | P0 | Wiring E2E | FR-1.10 failed gate to remediation log |
| REQ-011 | TEST | P0 | Wiring E2E | FR-1.11 KPI report values validated |
| REQ-012 | TEST | P0 | Wiring E2E | FR-1.12 _resolve_wiring_mode indirection |
| REQ-013 | TEST | P0 | Wiring E2E | FR-1.13 shadow findings logged with `[shadow]` |
| REQ-014 | TEST | P0 | Wiring E2E | FR-1.14 blocking remediation lifecycle |
| REQ-015 | TEST | P0 | Wiring E2E | FR-1.15 registry load_or_create 3-arg contract |
| REQ-016 | TEST | P0 | Wiring E2E | FR-1.16 merge_findings 3-arg contract |
| REQ-017 | TEST | P0 | Wiring E2E | FR-1.17 dict-to-Finding remediation conversion |
| REQ-018 | TEST | P0 | Wiring E2E | FR-1.18 MAX_CONVERGENCE_BUDGET = 61 |
| REQ-019 | TEST | P0 | Wiring E2E | FR-1.19 SHADOW_GRACE_INFINITE semantics |
| REQ-020 | TEST | P0 | Wiring E2E | FR-1.20 __post_init__ config derivation |
| REQ-021 | TEST | P0 | Wiring E2E | FR-1.21 check_wiring_report wrapper call |
| REQ-022 | INTEGRATION | P0 | Lifecycle & Modes | FR-2.1 convergence debit/credit/reimburse path |
| REQ-023 | INTEGRATION | P0 | Lifecycle & Modes | FR-2.1a handle_regression reachability |
| REQ-024 | INTEGRATION | P0 | Lifecycle & Modes | FR-2.2 sprint per-task path |
| REQ-025 | INTEGRATION | P0 | Lifecycle & Modes | FR-2.3 sprint per-phase path |
| REQ-026 | INTEGRATION | P0 | Lifecycle & Modes | FR-2.4 cross-path ledger coherence |
| REQ-027 | FUNCTIONAL | P0 | Lifecycle & Modes | FR-3.1a off mode |
| REQ-028 | FUNCTIONAL | P0 | Lifecycle & Modes | FR-3.1b shadow mode |
| REQ-029 | FUNCTIONAL | P0 | Lifecycle & Modes | FR-3.1c soft mode |
| REQ-030 | FUNCTIONAL | P0 | Lifecycle & Modes | FR-3.1d full mode |
| REQ-031 | TEST | P0 | Lifecycle & Modes | FR-3.2a budget exhausted before task launch |
| REQ-032 | TEST | P0 | Lifecycle & Modes | FR-3.2b before wiring analysis |
| REQ-033 | TEST | P0 | Lifecycle & Modes | FR-3.2c before remediation |
| REQ-034 | TEST | P0 | Lifecycle & Modes | FR-3.2d mid-convergence |
| REQ-035 | TEST | P1 | Lifecycle & Modes | FR-3.3 interrupted sprint persistence |
| REQ-036 | INTEGRATION | P0 | Reachability & Pipeline | FR-4.1 spec-driven 13-entry wiring manifest |
| REQ-037 | FUNCTIONAL | P0 | Reachability & Pipeline | FR-4.2 AST analyzer with documented limitations |
| REQ-038 | INTEGRATION | P0 | Reachability & Pipeline | FR-4.3 GateCriteria-compatible reachability gate |
| REQ-039 | TEST | P0 | Reachability & Pipeline | FR-4.4 broken wiring regression test |
| REQ-040 | QUALITY_GATE | P0 | Reachability & Pipeline | FR-5.1 0-files-analyzed must FAIL |
| REQ-041 | QUALITY_GATE | P0 | Reachability & Pipeline | FR-5.2 impl-vs-spec checker in _run_checkers() |
| REQ-042 | DEPENDENCY | P1 | Reachability & Pipeline | FR-6.1 close v3.05 gaps T07/T11/T12/T14 |
| REQ-043 | DEPENDENCY | P1 | Reachability & Pipeline | FR-6.2 confirming T02 and T17-T22 suite |
| REQ-044 | DATA_MODEL | P0 | Audit & Quality Gates | FR-7.1 audit-trail JSONL schema includes duration_ms |
| REQ-045 | ACCEPTANCE_CRITERION | P0 | Audit & Quality Gates | FR-7.2 four third-party verifiability properties |
| REQ-046 | PROCESS | P0 | Audit & Quality Gates | FR-7.3 audit_trail fixture semantics and auto-flush |
| REQ-047 | NON_FUNCTIONAL | P0 | Audit & Quality Gates | NFR-1 no mocks on gate/core orchestration logic |
| REQ-048 | CONSTRAINT | P0 | Audit & Quality Gates | NFR-2 UV-only execution |
| REQ-049 | SUCCESS_CRITERION | P0 | Audit & Quality Gates | SC-4 baseline regression threshold |
| REQ-050 | SUCCESS_CRITERION | P0 | Reachability & Pipeline | SC-7 reachability eval catches known-bad state |
| REQ-051 | SUCCESS_CRITERION | P0 | Reachability & Pipeline | SC-9 gate catches unreachable code |
| REQ-052 | SUCCESS_CRITERION | P0 | Reachability & Pipeline | SC-10 0-files analyzed FAIL |
| REQ-053 | SUCCESS_CRITERION | P0 | Reachability & Pipeline | SC-11 fidelity checker flags missing implementation |
| REQ-054 | SUCCESS_CRITERION | P0 | Audit & Quality Gates | SC-12 audit trail is third-party verifiable |
