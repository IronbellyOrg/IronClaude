# TASKLIST INDEX -- Unified Audit Gating

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Unified Audit Gating |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-03-19 |
| TASKLIST_ROOT | .dev/releases/current/v3.0_unified-audit-gating/ |
| Total Phases | 9 |
| Total Tasks | 43 |
| Total Deliverables | 50 |
| Complexity Class | HIGH |
| Primary Persona | backend |
| Consulting Personas | architect, qa, security |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | .dev/releases/current/v3.0_unified-audit-gating/tasklist-index.md |
| Phase 1 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-1-tasklist.md |
| Phase 2 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-2-tasklist.md |
| Phase 3 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-3-tasklist.md |
| Phase 4 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-4-tasklist.md |
| Phase 5 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-5-tasklist.md |
| Phase 6 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-6-tasklist.md |
| Phase 7 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-7-tasklist.md |
| Phase 8 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-8-tasklist.md |
| Phase 9 Tasklist | .dev/releases/current/v3.0_unified-audit-gating/phase-9-tasklist.md |
| Execution Log | .dev/releases/current/v3.0_unified-audit-gating/execution-log.md |
| Checkpoint Reports | .dev/releases/current/v3.0_unified-audit-gating/checkpoints/ |
| Evidence Directory | .dev/releases/current/v3.0_unified-audit-gating/evidence/ |
| Artifacts Directory | .dev/releases/current/v3.0_unified-audit-gating/artifacts/ |
| Validation Reports | .dev/releases/current/v3.0_unified-audit-gating/validation/ |
| Feedback Log | .dev/releases/current/v3.0_unified-audit-gating/feedback-log.md |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Decision Checkpoint | T01.01 | EXEMPT: 1 |
| 2 | phase-2-tasklist.md | Core Analysis Engine | T02.01-T02.07 | STRICT: 5, STANDARD: 2 |
| 3 | phase-3-tasklist.md | Report Emission and Gate Definition | T03.01-T03.06 | STRICT: 4, STANDARD: 2 |
| 4 | phase-4-tasklist.md | Roadmap Pipeline Integration | T04.01-T04.05 | STRICT: 3, STANDARD: 2 |
| 5 | phase-5-tasklist.md | Sprint Integration | T05.01-T05.04 | STRICT: 3, STANDARD: 1 |
| 6 | phase-6-tasklist.md | Audit Agent Extensions | T06.01-T06.06 | STRICT: 1, STANDARD: 5 |
| 7 | phase-7-tasklist.md | ToolOrchestrator Plugin | T07.01-T07.03 | STRICT: 2, STANDARD: 1 |
| 8 | phase-8-tasklist.md | Shadow Calibration and Readiness | T08.01-T08.06 | STRICT: 2, STANDARD: 3, EXEMPT: 1 |
| 9 | phase-9-tasklist.md | Activation and Hardening | T09.01-T09.05 | STRICT: 2, STANDARD: 2, EXEMPT: 1 |

## Source Snapshot

- Delivers a static wiring verification gate for the SuperClaude pipeline detecting unwired callables, orphan modules, and broken dispatch registries via deterministic AST analysis
- Zero modifications to `pipeline/*` substrate; all new code consumes existing contracts (`GateCriteria`, `SemanticCheck`, `Step`, `GateMode`)
- Three-phase rollout: shadow, soft, full enforcement with statistical FPR calibration gates
- 8 goals (G-001 through G-008), 14 success criteria (SC-001 through SC-014)
- ~480-580 LOC production code, ~420-560 LOC test code across 3 subsystems (roadmap, sprint, audit) plus 5 agent specs
- Phase 5 (ToolOrchestrator Plugin) is conditional with cut criteria: defer to v2.1 if not complete before Phase 6a

## Deterministic Rules Applied

- Phase renumbering: roadmap phases 0, 1, 2, 3a, 3b, 4, 5, 6a, 6b renumbered to sequential 1-9 with no gaps
- Task IDs: zero-padded T<PP>.<TT> format (e.g., T01.01)
- Checkpoint cadence: every 5 tasks within a phase plus mandatory end-of-phase checkpoint
- Clarification tasks: inserted when roadmap item lacks actionable specifics
- Deliverable registry: D-0001 through D-0050 assigned in task order
- Effort mapping: deterministic scoring from text keywords (XS/S/M/L/XL)
- Risk mapping: deterministic scoring from text keywords (Low/Medium/High)
- Tier classification: STRICT > EXEMPT > LIGHT > STANDARD priority with keyword matching and context boosters
- Verification routing: STRICT -> sub-agent, STANDARD -> direct test, LIGHT -> sanity check, EXEMPT -> skip
- MCP requirements: STRICT requires Sequential + Serena; others optional
- Traceability matrix: R-### -> T<PP>.<TT> -> D-#### with artifact paths
- Multi-file output: one index + 9 phase files for Sprint CLI compatibility
- Roadmap task 1.5 (whitelist) merged into T02.01 per roadmap note "(included in 1.1a)"

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | 1 | Zero modifications to the pipeline substrate. All new code consumes existing contracts |
| R-002 | 1 | Three-phase shadow soft full enforcement with statistical FPR calibration gates between phases |
| R-003 | 1 | Commit to answers for all open questions before code begins. Documented review producing decision log |
| R-004 | 2 | Define WiringConfig dataclass, DEFAULT_REGISTRY_PATTERNS, whitelist loading in cli/audit/wiring_config.py |
| R-005 | 2 | Define WiringFinding, WiringReport dataclasses in cli/audit/wiring_gate.py |
| R-006 | 2 | Implement unwired callable analysis in cli/audit/wiring_gate.py per G-001 |
| R-007 | 2 | Implement orphan module analysis in cli/audit/wiring_gate.py per G-002 |
| R-008 | 2 | Implement registry analysis in cli/audit/wiring_gate.py per G-003 |
| R-009 | 2 | Implement whitelist loading and suppression in cli/audit/wiring_config.py (included in 1.1a) |
| R-010 | 2 | Implement ast_analyze_file() utility in cli/audit/wiring_analyzer.py per G-008 |
| R-011 | 2 | Unit tests for all three analyzers plus whitelist in tests/audit/ |
| R-012 | 2 | Validation: all 3 detection types correct, whitelist works, performance less than 5s for 50 files |
| R-013 | 3 | Implement report emitter frontmatter plus 7 Markdown sections using yaml.safe_dump() per G-004 |
| R-014 | 3 | Implement _extract_frontmatter_values() helper with duplicate _FRONTMATTER_RE preserving NFR-007 layering |
| R-015 | 3 | Define WIRING_GATE as GateCriteria with 16 required frontmatter fields |
| R-016 | 3 | Implement 5 semantic check functions for WIRING_GATE |
| R-017 | 3 | Implement blocking_for_mode() logic for mode-aware enforcement |
| R-018 | 3 | Unit tests for report plus gate plus semantic checks in tests/audit/ |
| R-019 | 3 | Validation: 16 frontmatter fields, gate_passed evaluates correctly, mode-aware semantics, 90% coverage |
| R-020 | 4 | Add build_wiring_verification_prompt stub to roadmap/prompts.py |
| R-021 | 4 | Add wiring-verification Step to _build_steps() and update _get_all_step_ids() |
| R-022 | 4 | Special-case roadmap_run_step() for wiring-verification calling run_wiring_analysis() and emit_report() |
| R-023 | 4 | Register WIRING_GATE in ALL_GATES in roadmap/gates.py |
| R-024 | 4 | Integration tests for roadmap pipeline including resume behavior validation |
| R-025 | 4 | Validation: step IDs correct, pipeline end-to-end, no NFR-007 violations |
| R-026 | 5 | Add wiring_gate_mode field to SprintConfig in sprint/models.py |
| R-027 | 5 | Implement sprint post-task wiring hook in sprint/executor.py per G-005 |
| R-028 | 5 | Pre-activation safeguards: greater than 50 files must produce greater than 0 findings |
| R-029 | 5 | Integration tests for sprint hook testing off/shadow/soft/full modes |
| R-030 | 5 | Validation: shadow logs without affecting status, soft warns, full blocks |
| R-031 | 6 | Extend audit-scanner with REVIEW:wiring signal in agents/audit-scanner.md per SC-011 |
| R-032 | 6 | Extend audit-analyzer with 9th field plus finding types in agents/audit-analyzer.md per SC-012 |
| R-033 | 6 | Extend audit-validator with Check 5 in agents/audit-validator.md |
| R-034 | 6 | Extend audit-comparator with cross-file wiring check in agents/audit-comparator.md per G-007 |
| R-035 | 6 | Extend audit-consolidator with Wiring Health section in agents/audit-consolidator.md per G-007 |
| R-036 | 6 | Agent regression tests in tests/audit/ per SC-011 SC-012 |
| R-037 | 6 | Validation: extensions additive, scanner classifies correctly, analyzer 9-field, validator catches DELETE |
| R-038 | 7 | Implement AST plugin for ToolOrchestrator in cli/audit/wiring_analyzer.py per G-008 |
| R-039 | 7 | Wire dual evidence rule using plugin output for orphan detection |
| R-040 | 7 | Unit tests for plugin integration in tests/audit/ per SC-013 |
| R-041 | 8 | Run shadow mode across 2+ release cycles to collect findings data |
| R-042 | 8 | Compute FPR, TPR, p95 latency from shadow data per SC-008 |
| R-043 | 8 | Run retrospective validation with cli-portify known-bug fixture per SC-009 |
| R-044 | 8 | Characterize alias/re-export noise floor per R6 mitigation |
| R-045 | 8 | Validate measured_FPR + 2 sigma less than 15% threshold |
| R-046 | 8 | Produce readiness report with explicit recommendation for shadow to soft transition |
| R-047 | 9 | Activate soft mode if 6a criteria met via config change |
| R-048 | 9 | Monitor soft mode for 5+ sprints for stability tracking |
| R-049 | 9 | Validate full-mode criteria: FPR less than 5%, TPR greater than 80% |
| R-050 | 9 | Activate full mode if criteria met via config change |
| R-051 | 9 | Schedule v2.1 improvements if blocked by alias noise: import alias pre-pass |
| R-052 | All | Success criteria SC-001 through SC-014 cross-cutting validation requirements |
| R-053 | All | Risk mitigations R1 through R9 cross-cutting risk management |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-003 | Architecture decision log with 7 committed answers | EXEMPT | Skip verification | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0001/spec.md | XS | Low |
| D-0002 | T02.01 | R-004, R-009 | WiringConfig dataclass with DEFAULT_REGISTRY_PATTERNS and whitelist loading | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0002/spec.md | M | Medium |
| D-0003 | T02.02 | R-005 | WiringFinding and WiringReport dataclasses | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0003/spec.md | S | Low |
| D-0004 | T02.03 | R-006 | Unwired callable analyzer in wiring_gate.py | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0004/spec.md | M | Medium |
| D-0005 | T02.04 | R-007 | Orphan module analyzer in wiring_gate.py | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0005/spec.md | M | Medium |
| D-0006 | T02.05 | R-008 | Registry analyzer in wiring_gate.py | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0006/spec.md | M | Medium |
| D-0007 | T02.06 | R-010 | ast_analyze_file() utility function | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0007/spec.md | S | Low |
| D-0008 | T02.07 | R-011, R-012 | Unit test suite for analyzers and whitelist (>=20 tests) | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0008/evidence.md | M | Low |
| D-0009 | T02.07 | R-011, R-012 | Performance benchmark test (<5s for 50 files) | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0009/evidence.md | M | Low |
| D-0010 | T03.01 | R-013 | Report emitter with YAML frontmatter and 7 Markdown sections | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0010/spec.md | M | Medium |
| D-0011 | T03.02 | R-014 | _extract_frontmatter_values() helper function | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0011/spec.md | S | Low |
| D-0012 | T03.03 | R-015 | WIRING_GATE GateCriteria definition with 16 fields | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0012/spec.md | S | Medium |
| D-0013 | T03.04 | R-016 | 5 semantic check functions for gate validation | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0013/spec.md | M | Medium |
| D-0014 | T03.05 | R-017 | blocking_for_mode() enforcement logic | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0014/spec.md | S | Medium |
| D-0015 | T03.06 | R-018, R-019 | Unit tests for report, gate, and semantic checks | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0015/evidence.md | M | Low |
| D-0016 | T03.06 | R-019 | Coverage report showing >=90% on wiring_gate.py and wiring_analyzer.py | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0016/evidence.md | M | Low |
| D-0017 | T04.01 | R-020 | build_wiring_verification_prompt() function in roadmap/prompts.py | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0017/spec.md | S | Low |
| D-0018 | T04.02 | R-021 | Wiring-verification Step in _build_steps() with correct ordering | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0018/spec.md | M | Medium |
| D-0019 | T04.03 | R-022 | roadmap_run_step() special-case for wiring-verification | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0019/spec.md | M | Medium |
| D-0020 | T04.04 | R-023 | WIRING_GATE registered in ALL_GATES | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0020/spec.md | XS | Medium |
| D-0021 | T04.05 | R-024, R-025 | Integration test suite for roadmap pipeline (>=3 tests) | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0021/evidence.md | M | Medium |
| D-0022 | T04.05 | R-024 | Resume behavior validation test | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0022/evidence.md | M | Medium |
| D-0023 | T05.01 | R-026 | wiring_gate_mode field on SprintConfig | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0023/spec.md | S | Medium |
| D-0024 | T05.02 | R-027 | Sprint post-task wiring hook implementation | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0024/spec.md | M | Medium |
| D-0025 | T05.03 | R-028 | Pre-activation safeguard checks in sprint executor | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0025/spec.md | S | Medium |
| D-0026 | T05.04 | R-029, R-030 | Integration tests for sprint hook (4 mode tests) | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0026/evidence.md | M | Low |
| D-0027 | T06.01 | R-031 | Updated audit-scanner.md with REVIEW:wiring signal | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0027/spec.md | S | Medium |
| D-0028 | T06.02 | R-032 | Updated audit-analyzer.md with 9th field and finding types | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0028/spec.md | S | Medium |
| D-0029 | T06.03 | R-033 | Updated audit-validator.md with Check 5 | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0029/spec.md | S | Low |
| D-0030 | T06.04 | R-034 | Updated audit-comparator.md with cross-file wiring check | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0030/spec.md | S | Medium |
| D-0031 | T06.05 | R-035 | Updated audit-consolidator.md with Wiring Health section | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0031/spec.md | S | Low |
| D-0032 | T06.06 | R-036, R-037 | Agent regression test suite with prior-output comparison | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0032/evidence.md | M | Medium |
| D-0033 | T07.01 | R-038 | AST plugin for ToolOrchestrator in wiring_analyzer.py | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0033/spec.md | M | Medium |
| D-0034 | T07.02 | R-039 | Dual evidence rule wiring for orphan detection | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0034/spec.md | S | Medium |
| D-0035 | T07.03 | R-040 | Unit tests for AST plugin (>=3 tests) | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0035/evidence.md | S | Low |
| D-0036 | T08.01 | R-041 | Shadow mode findings dataset from 2+ release cycles | EXEMPT | Skip verification | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0036/evidence.md | L | Medium |
| D-0037 | T08.02 | R-042 | FPR, TPR, and p95 latency computation results | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0037/evidence.md | M | Medium |
| D-0038 | T08.03 | R-043 | Retrospective validation result confirming step_runner detection | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0038/evidence.md | S | Medium |
| D-0039 | T08.04 | R-044 | Alias/re-export noise floor characterization report | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0039/evidence.md | M | Medium |
| D-0040 | T08.05 | R-045 | FPR threshold validation (measured_FPR + 2sigma < 15%) | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0040/evidence.md | S | Medium |
| D-0041 | T08.06 | R-046 | Readiness report with explicit shadow-to-soft recommendation | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0041/spec.md | S | Medium |
| D-0042 | T09.01 | R-047 | Soft mode activation config change applied | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0042/evidence.md | S | Medium |
| D-0043 | T09.02 | R-048 | Soft mode stability tracking data from 5+ sprints | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0043/evidence.md | L | Medium |
| D-0044 | T09.03 | R-049 | Full-mode criteria validation (FPR<5%, TPR>80%) | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0044/evidence.md | S | Medium |
| D-0045 | T09.04 | R-050 | Full mode activation config change applied | STANDARD | Direct test execution | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0045/evidence.md | S | Medium |
| D-0046 | T09.05 | R-051 | v2.1 improvement schedule or confirmation that alias noise is resolved | EXEMPT | Skip verification | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0046/spec.md | S | Low |
| D-0047 | T02.01 | R-004 | wiring_whitelist.yaml suppression config file | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0047/spec.md | M | Medium |
| D-0048 | T04.02 | R-021 | Updated _get_all_step_ids() with wiring-verification ordering | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0048/spec.md | M | Medium |
| D-0049 | T05.02 | R-027 | Sprint hook mode-aware behavior (shadow/soft/full semantics) | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0049/spec.md | M | Medium |
| D-0050 | T08.02 | R-042 | Performance benchmark evidence (<5s p95 for 50 files) | STRICT | Sub-agent (quality-engineer) | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0050/evidence.md | M | Medium |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | EXEMPT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0001/ |
| R-002 | T01.01 | D-0001 | EXEMPT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0001/ |
| R-003 | T01.01 | D-0001 | EXEMPT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0001/ |
| R-004 | T02.01 | D-0002, D-0047 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0002/, D-0047/ |
| R-005 | T02.02 | D-0003 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0003/ |
| R-006 | T02.03 | D-0004 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0004/ |
| R-007 | T02.04 | D-0005 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0005/ |
| R-008 | T02.05 | D-0006 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0006/ |
| R-009 | T02.01 | D-0002, D-0047 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0002/, D-0047/ |
| R-010 | T02.06 | D-0007 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0007/ |
| R-011 | T02.07 | D-0008, D-0009 | STANDARD | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0008/, D-0009/ |
| R-012 | T02.07 | D-0008, D-0009 | STANDARD | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0008/, D-0009/ |
| R-013 | T03.01 | D-0010 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0010/ |
| R-014 | T03.02 | D-0011 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0011/ |
| R-015 | T03.03 | D-0012 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0012/ |
| R-016 | T03.04 | D-0013 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0013/ |
| R-017 | T03.05 | D-0014 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0014/ |
| R-018 | T03.06 | D-0015, D-0016 | STANDARD | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0015/, D-0016/ |
| R-019 | T03.06 | D-0015, D-0016 | STANDARD | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0015/, D-0016/ |
| R-020 | T04.01 | D-0017 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0017/ |
| R-021 | T04.02 | D-0018, D-0048 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0018/, D-0048/ |
| R-022 | T04.03 | D-0019 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0019/ |
| R-023 | T04.04 | D-0020 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0020/ |
| R-024 | T04.05 | D-0021, D-0022 | STANDARD | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0021/, D-0022/ |
| R-025 | T04.05 | D-0021, D-0022 | STANDARD | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0021/, D-0022/ |
| R-026 | T05.01 | D-0023 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0023/ |
| R-027 | T05.02 | D-0024, D-0049 | STRICT | 90% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0024/, D-0049/ |
| R-028 | T05.03 | D-0025 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0025/ |
| R-029 | T05.04 | D-0026 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0026/ |
| R-030 | T05.04 | D-0026 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0026/ |
| R-031 | T06.01 | D-0027 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0027/ |
| R-032 | T06.02 | D-0028 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0028/ |
| R-033 | T06.03 | D-0029 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0029/ |
| R-034 | T06.04 | D-0030 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0030/ |
| R-035 | T06.05 | D-0031 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0031/ |
| R-036 | T06.06 | D-0032 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0032/ |
| R-037 | T06.06 | D-0032 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0032/ |
| R-038 | T07.01 | D-0033 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0033/ |
| R-039 | T07.02 | D-0034 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0034/ |
| R-040 | T07.03 | D-0035 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0035/ |
| R-041 | T08.01 | D-0036 | EXEMPT | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0036/ |
| R-042 | T08.02 | D-0037, D-0050 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0037/, D-0050/ |
| R-043 | T08.03 | D-0038 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0038/ |
| R-044 | T08.04 | D-0039 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0039/ |
| R-045 | T08.05 | D-0040 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0040/ |
| R-046 | T08.06 | D-0041 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0041/ |
| R-047 | T09.01 | D-0042 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0042/ |
| R-048 | T09.02 | D-0043 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0043/ |
| R-049 | T09.03 | D-0044 | STRICT | 85% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0044/ |
| R-050 | T09.04 | D-0045 | STANDARD | 80% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0045/ |
| R-051 | T09.05 | D-0046 | EXEMPT | 75% | .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0046/ |
| R-052 | T02.07, T03.06, T04.05, T05.04, T06.06 | D-0008, D-0015, D-0021, D-0026, D-0032 | STANDARD | 80% | (distributed across test tasks) |
| R-053 | T02.01, T05.03, T08.04 | D-0002, D-0025, D-0039 | STRICT | 85% | (distributed across mitigation tasks) |

## Execution Log Template

**Intended Path:** .dev/releases/current/v3.0_unified-audit-gating/execution-log.md

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| | | | | | | | |

## Checkpoint Report Template

**Template:**

# Checkpoint Report -- <Checkpoint Title>

**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/<deterministic-name>.md

**Scope:** <tasks covered>

## Status
Overall: Pass | Fail | TBD

## Verification Results
- <verification bullet 1>
- <verification bullet 2>
- <verification bullet 3>

## Exit Criteria Assessment
- <exit criterion 1>
- <exit criterion 2>
- <exit criterion 3>

## Issues & Follow-ups
- <blocking issues referencing T<PP>.<TT> and D-####>

## Evidence
- .dev/releases/current/v3.0_unified-audit-gating/evidence/<task-related-evidence>

## Feedback Collection Template

**Intended Path:** .dev/releases/current/v3.0_unified-audit-gating/feedback-log.md

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| | | | | | | |

## Generation Notes

- Roadmap phases 0, 1, 2, 3a, 3b, 4, 5, 6a, 6b renumbered to sequential 1-9
- Roadmap task 1.5 (whitelist loading) merged into T02.01 per roadmap note "(included in 1.1a)"
- Phase 7 (ToolOrchestrator Plugin) marked conditional per roadmap cut criteria section 5.3.1
- Phase 8 and 9 contain operational/observational tasks that cannot be fully automated
- Cross-cutting roadmap items R-052 (success criteria) and R-053 (risk mitigations) distributed across relevant test and implementation tasks
