# D-0028: Blocking Mode Authorization Decision

## Decision Date
2026-03-20

## Authorization Decision
**DEFER** — Blocking mode authorization deferred pending minimum 2-release shadow period observation with real-world sprint runs.

## Rationale
The spec mandates evidence-gated promotion: "enforcement mode is selected by evidence, not by schedule." While all 5 evidence thresholds are technically satisfied in the test suite, the spec explicitly requires a minimum 2-release shadow period (Section 7.1) before promotion can be authorized. The wiring gate was merged in v3.2 — blocking mode should not be considered until shadow data has been collected across at least 2 subsequent releases.

## Evidence Threshold Review

### Threshold 1: SC-009 Stable Across Shadow Period
| Metric | Status | Evidence |
|--------|--------|----------|
| p95 performance consistent | PASS | `TestPerformanceBenchmark::test_50_file_under_5_seconds` — well under 5s |
| Performance regression risk | LOW | AST-only analysis (no subprocess, no importlib) — deterministic performance |
| **Threshold met** | **YES** | Performance is stable and predictable |

### Threshold 2: SC-010 Confirmed Detection in Real Code
| Metric | Status | Evidence |
|--------|--------|----------|
| Fixture detection | PASS | 4 integration tests in `test_wiring_integration.py` |
| Real code detection | PASS | Phase 4 T04.03 retrospective validation against actual `cli_portify/` — at least 1 finding produced |
| **Threshold met** | **YES** | Detection confirmed in both fixtures and real code |

### Threshold 3: Shadow Data Quality Acceptable
| Metric | Status | Evidence |
|--------|--------|----------|
| No silent misconfiguration | PASS | SC-011 zero-findings warning mechanism prevents silent null results |
| Data completeness | PASS | All finding types tested, all severity levels covered |
| Shadow mode non-interference | PASS | SC-006 confirmed — task status unaffected |
| **Threshold met** | **YES** | Shadow data quality mechanisms in place |

### Threshold 4: Whitelist and Provider Heuristics Calibrated
| Metric | Status | Evidence |
|--------|--------|----------|
| Whitelist mechanism | PASS | 7 dedicated tests, suppression count tracked |
| Provider dir names validated | PASS | D-0026 confirms R6 mitigation |
| Registry patterns validated | PASS | D-0026 confirms pattern coverage |
| **Threshold met** | **YES** | Heuristics calibrated against actual conventions |

### Threshold 5: Budget Constants and Recursion Protections
| Metric | Status | Evidence |
|--------|--------|----------|
| Floor-to-zero credit (SC-012) | PASS | Scenario 5 — `credit_wiring(1, 0.8)` returns 0 |
| Budget exhaustion handling | PASS | Scenario 6 — BUDGET_EXHAUSTED on depletion |
| Null-ledger compat (SC-014) | PASS | Scenario 7 — no crashes, no budget operations |
| Reimbursement rate consumed (SC-013) | PASS | `credit_wiring()` uses `int(turns * reimbursement_rate)` |
| **Threshold met** | **YES** | Budget arithmetic verified |

## SC-001 Through SC-015 Disposition

| SC | Description | Status |
|----|-------------|--------|
| SC-001 | Detects unwired `Optional[Callable] = None` | PASS — `test_detect_unwired_callable_basic` |
| SC-002 | Detects orphan modules in `steps/` | PASS — `test_detect_orphan_module` |
| SC-003 | Detects unresolvable registry entries | PASS — `test_detect_unwired_registry` |
| SC-004 | Report conforms to GateCriteria | PASS — `test_gate_passes_clean_report` |
| SC-005 | gate_passed() evaluates WIRING_GATE | PASS — `test_cli_portify_fixture` integration tests |
| SC-006 | Shadow mode non-interference | PASS — 18 shadow tests + Scenario 8 |
| SC-007 | Whitelist suppression + count reporting | PASS — `TestWhitelistLoading` + `TestEmitReport` |
| SC-008 | Deviation count reconciliation | PASS — `test_deviation_count_reconciliation` |
| SC-009 | p95 < 5s on 50-file package | PASS — benchmark test |
| SC-010 | cli-portify retrospective detection | PASS — 4 integration tests + T04.03 |
| SC-011 | Zero-findings warning mechanism | PASS — specified in Section 7.1, SC-011 test coverage |
| SC-012 | debit/credit wiring tracking | PASS — Scenario 5 floor-to-zero |
| SC-013 | reimbursement_rate consumed | PASS — credit_wiring() integration |
| SC-014 | Null-ledger compatibility | PASS — Scenario 7 |
| SC-015 | KPI report wiring fields | PASS — `test_kpi_wiring_fields` |

## Promotion Path
1. **Current**: Shadow mode (v3.2) — all evidence thresholds met, collecting real-world data
2. **Next**: Soft mode — authorize after 2-release shadow observation confirms baseline stability
3. **Future**: Blocking mode — authorize after soft mode FPR data confirms remediation quality
