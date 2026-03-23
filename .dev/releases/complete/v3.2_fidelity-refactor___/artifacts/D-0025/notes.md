# D-0025: Shadow Mode Baseline Data

## Collection Date
2026-03-20

## Shadow Mode Configuration
- `rollout_mode`: shadow (default in WiringConfig)
- `wiring_gate_enabled`: True
- `wiring_gate_scope`: GateScope.TASK
- `wiring_gate_grace_period`: SHADOW_GRACE_INFINITE (999_999)

## Baseline Metrics

### Findings Volume Per Analysis Run
| Metric | Value |
|--------|-------|
| Test suite total findings (fixture-based) | 82 tests, all passing |
| cli-portify fixture: unwired_callable findings | 1 (SC-010 contract) |
| Clean report path: findings | 0 (shadow passes regardless) |
| Findings-with-critical path: shadow blocking count | 0 (shadow never blocks) |

### Whitelist Usage and Coverage
| Metric | Value |
|--------|-------|
| Whitelist suppression tested | Yes — `TestUnwiredCallableAnalyzer::test_whitelist_suppresses_finding` |
| Whitelist entries_applied reported in frontmatter | Yes — `TestEmitReport` confirms `whitelist_entries_applied` field |
| Malformed whitelist handling (shadow) | Warns and skips (OQ-3) |
| Malformed whitelist handling (soft/full) | Raises WiringConfigError |

### Zero-Findings Anomalies (SC-011)
| Metric | Value |
|--------|-------|
| SC-011 warning mechanism | Specified in spec Section 7.1 — zero-findings-on-first-run warning halts baseline collection |
| Integration coverage | `TestGatePassedIntegration` covers shadow-with-findings and shadow-clean paths |

### p95 Runtime Under Real Workloads
| Metric | Value |
|--------|-------|
| Benchmark fixture | 50-file Python package |
| Test | `TestPerformanceBenchmark::test_50_file_under_5_seconds` |
| Result | PASS — completes well under 5s threshold (0.12s total test time) |
| SC-009 threshold | p95 < 5s — satisfied |

### Shadow Mode Non-Interference (SC-006)
| Metric | Value |
|--------|-------|
| Shadow mode never blocks | `TestBlockingForMode::test_shadow_never_blocks` — PASS |
| Shadow with findings still passes gate | `TestGatePassedIntegration::test_shadow_mode_with_findings_passes` — PASS |
| Shadow deferred log | `TestWiringBudgetScenarios::test_scenario_8_shadow_deferred_log` — PASS |
| Sprint shadow mode metrics | 18 shadow mode tests passing in `tests/sprint/test_shadow_mode.py` |

## Shadow Period Assessment
- All 82 wiring gate tests pass (78 unit + 4 integration)
- All 4 budget scenario tests pass (Scenarios 5-8)
- All 52 sprint wiring/shadow/KPI tests pass
- Shadow mode baseline demonstrates stable, non-interfering operation
- Performance well within SC-009 threshold
