# TASKLIST INDEX -- Deterministic Fidelity Gates v3.05

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Deterministic Fidelity Gates v3.05 |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-03-20 |
| TASKLIST_ROOT | `.dev/releases/current/v3.05_DeterministicFidelityGates/` |
| Total Phases | 6 |
| Total Tasks | 34 |
| Total Deliverables | 48 |
| Complexity Class | HIGH |
| Primary Persona | backend |
| Consulting Personas | architect, qa, refactorer |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/phase-5-tasklist.md` |
| Phase 6 Tasklist | `TASKLIST_ROOT/phase-6-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/artifacts/` |
| Validation Reports | `TASKLIST_ROOT/validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Foundation -- Parser, Data Model & Interface Verification | T01.01-T01.07 | STRICT: 3, STANDARD: 4 |
| 2 | phase-2-tasklist.md | Structural Checkers & Severity Engine | T02.01-T02.05 | STRICT: 3, STANDARD: 2 |
| 3 | phase-3-tasklist.md | Deviation Registry & Run-to-Run Memory | T03.01-T03.04 | STRICT: 3, STANDARD: 1 |
| 4 | phase-4-tasklist.md | Semantic Layer & Adversarial Debate | T04.01-T04.06 | STRICT: 4, STANDARD: 2 |
| 5 | phase-5-tasklist.md | Convergence Engine, TurnLedger & Regression | T05.01-T05.09 | STRICT: 6, STANDARD: 3 |
| 6 | phase-6-tasklist.md | Remediation & Integration | T06.01-T06.08 | STRICT: 5, STANDARD: 3 |

## Source Snapshot

- Replaces monolithic LLM fidelity comparison with hybrid deterministic/semantic architecture
- Five parallel structural checkers produce ~70% deterministic findings
- Residual semantic layer with adversarial debate handles ~30% judgment-dependent checks
- Convergence engine (<=3 runs) with TurnLedger budget accounting
- DeviationRegistry as single source of truth for gate pass/fail in convergence mode
- Legacy mode (`convergence_enabled=false`) byte-identical to commit `f4d9035`

## Deterministic Rules Applied

- Phase buckets derived from roadmap's 6 explicit phase headings; renumbered sequentially 1-6 (no gaps)
- Task IDs: `T<PP>.<TT>` format (zero-padded, 2-digit phase + 2-digit task)
- Checkpoints inserted after every 5 tasks and at end of each phase
- Clarification tasks inserted when roadmap leaves implementation specifics ambiguous
- Deliverable Registry: globally unique `D-####` IDs in appearance order
- Effort computed via keyword scoring: security/auth/db/migration/pipeline/performance terms
- Risk computed via keyword scoring: security/compliance/migration/breaking/cross-cutting terms
- Tier classification via `/sc:task-unified` algorithm: STRICT for security/database/refactor/multi-file, STANDARD for implement/add/create
- Verification routing: STRICT -> quality-engineer sub-agent, STANDARD -> direct test execution
- MCP requirements: STRICT requires Sequential + Serena; STANDARD prefers Sequential + Context7
- Traceability: every task traces to R-### roadmap items and D-#### deliverables
- Multi-file output: 1 index + 6 phase files for Sprint CLI compatibility

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | 1 | Verify `TurnLedger` API from `superclaude.cli.sprint.models`: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate` |
| R-002 | 1 | Verify `DeviationRegistry` current surface in `convergence.py:50-225` |
| R-003 | 1 | Confirm `convergence_enabled` default false and step 8-only scope |
| R-004 | 1 | Confirm `fidelity.py` has zero imports (deletion candidate) |
| R-005 | 1 | Lock `handle_regression() -> RegressionResult` callable signature (FR-7.1) |
| R-006 | 1 | Map acceptance-test matrix to SC-1 through SC-6 |
| R-007 | 1 | Create `src/superclaude/cli/roadmap/spec_parser.py` |
| R-008 | 1 | Implement YAML frontmatter extraction with graceful degradation |
| R-009 | 1 | Implement markdown table extraction keyed by heading path |
| R-010 | 1 | Implement fenced code block extraction with language annotation |
| R-011 | 1 | Implement requirement ID regex extraction |
| R-012 | 1 | Implement Python function signature extraction from fenced blocks |
| R-013 | 1 | Implement `Literal[...]` enum value extraction |
| R-014 | 1 | Implement numeric threshold expression extraction |
| R-015 | 1 | Implement file path extraction from manifest tables |
| R-016 | 1 | Validation gate: Run parser against real spec |
| R-017 | 1 | Define `SpecSection` dataclass |
| R-018 | 1 | Implement `split_into_sections(content: str) -> list[SpecSection]` in `spec_parser.py` |
| R-019 | 1 | Handle YAML frontmatter as special section and preamble content |
| R-020 | 1 | Define dimension-to-section mapping for checker routing |
| R-021 | 1 | Extend `Finding` dataclass with `rule_id`, `spec_quote`, `roadmap_quote` fields |
| R-022 | 1 | Define `SEVERITY_RULES` structure and `get_severity()` function |
| R-023 | 1 | Define `ParseWarning`, `RunMetadata`, `RegressionResult`, `RemediationPatch` types |
| R-024 | 2 | Define checker callable interface and registry |
| R-025 | 2 | Implement Signatures checker |
| R-026 | 2 | Implement Data Models checker |
| R-027 | 2 | Implement Gates checker |
| R-028 | 2 | Implement CLI Options checker |
| R-029 | 2 | Implement NFRs checker |
| R-030 | 2 | Implement all 19 canonical severity rules across 5 dimensions |
| R-031 | 2 | Verify determinism: same inputs -> identical output across runs |
| R-032 | 3 | Extend `DeviationRegistry` class in `convergence.py` |
| R-033 | 3 | Add `source_layer` field, stable ID computation, cross-run comparison |
| R-034 | 3 | Add run metadata with split HIGH counts |
| R-035 | 3 | Implement spec version change detection -> registry reset |
| R-036 | 3 | Handle pre-v3.05 registries with backward-compatible defaults |
| R-037 | 3 | Add `first_seen_run` and `last_seen_run` tracking per finding |
| R-038 | 3 | Prior findings summary for semantic prompts (max 50, oldest-first truncation) |
| R-039 | 4 | Extend `semantic_layer.py` for residual semantic pass |
| R-040 | 4 | Implement prompt budget enforcement (30,720 bytes) |
| R-041 | 4 | Implement `validate_semantic_high()` lightweight debate protocol |
| R-042 | 4 | Implement 4-criterion rubric scoring and deterministic judge |
| R-043 | 4 | Implement debate YAML output per finding |
| R-044 | 5 | Import TurnLedger and implement budget guards |
| R-045 | 5 | Implement `execute_fidelity_with_convergence()` |
| R-046 | 5 | Implement legacy/convergence dispatch |
| R-047 | 5 | Implement regression detection and parallel validation (FR-8) |
| R-048 | 5 | Validate FR-7/FR-8 interface contract (FR-7.1) |
| R-049 | 6 | Extend `remediate_executor.py` with structured patches |
| R-050 | 6 | Implement `--allow-regeneration` flag (FR-9.1) |
| R-051 | 6 | Pipeline integration: wire all components in step 8 |
| R-052 | 6 | Dead code removal: delete `fidelity.py` |
| R-053 | 6 | End-to-end verification: SC-1 through SC-6, NFR-1 through NFR-7 |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001, R-002, R-003, R-004, R-005, R-006 | Interface verification report documenting API surfaces, defaults, and acceptance-test mapping | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0001/evidence.md` | M | Medium |
| D-0002 | T01.02 | R-007, R-008, R-009, R-010, R-011 | `spec_parser.py` with YAML frontmatter, table, code block, and ID extraction | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0002/spec.md` | L | Medium |
| D-0003 | T01.02 | R-012, R-013, R-014, R-015 | Function signature, Literal enum, threshold, and file path extraction in `spec_parser.py` | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0003/evidence.md` | L | Medium |
| D-0004 | T01.03 | R-016 | Parser validation against real spec with zero crashes and populated `ParseWarning` list | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0004/evidence.md` | S | Low |
| D-0005 | T01.04 | R-017, R-018, R-019 | `SpecSection` dataclass and `split_into_sections()` function with frontmatter/preamble handling | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0005/spec.md` | M | Low |
| D-0006 | T01.04 | R-020 | Dimension-to-section mapping for checker routing | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0006/spec.md` | M | Low |
| D-0007 | T01.05 | R-021 | Extended `Finding` dataclass with `rule_id`, `spec_quote`, `roadmap_quote` (backward-compatible defaults) | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0007/spec.md` | S | Medium |
| D-0008 | T01.05 | R-022 | `SEVERITY_RULES` dict and `get_severity()` function with KeyError on unknown combos | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0008/spec.md` | S | Medium |
| D-0009 | T01.05 | R-023 | `ParseWarning`, `RunMetadata`, `RegressionResult`, `RemediationPatch` dataclass definitions | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0009/spec.md` | S | Medium |
| D-0010 | T01.06 | R-016 | Unit tests for `spec_parser.py` validated against real spec | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0010/evidence.md` | M | Low |
| D-0011 | T01.07 | R-006 | Checkpoint A verification: all Phase 1 exit criteria confirmed | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0011/evidence.md` | S | Low |
| D-0012 | T02.01 | R-024 | Checker callable interface and registry mapping dimension names to callables | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0012/spec.md` | M | Medium |
| D-0013 | T02.02 | R-025, R-026 | Signatures checker and Data Models checker implementations | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0013/spec.md` | L | Medium |
| D-0014 | T02.03 | R-027, R-028, R-029 | Gates, CLI Options, and NFRs checker implementations | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0014/spec.md` | L | Medium |
| D-0015 | T02.04 | R-030 | All 19 canonical severity rules implemented with `KeyError` on unknown combos | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0015/evidence.md` | M | Low |
| D-0016 | T02.05 | R-031 | Determinism proof: two runs on identical input produce byte-identical findings | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0016/evidence.md` | M | Medium |
| D-0017 | T03.01 | R-032, R-033 | Extended `DeviationRegistry` with `source_layer`, stable ID computation, cross-run comparison | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0017/spec.md` | L | High |
| D-0018 | T03.01 | R-034 | RunMetadata with run_number, timestamp, spec_hash, roadmap_hash, structural_high_count, semantic_high_count, total_high_count | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0018/spec.md` | L | High |
| D-0019 | T03.02 | R-035, R-036 | Spec version change detection and pre-v3.05 registry backward compatibility | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0019/evidence.md` | M | Medium |
| D-0020 | T03.03 | R-037, R-038 | Run-to-run memory: `first_seen_run`/`last_seen_run` tracking, prior findings summary (max 50) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0020/spec.md` | M | Medium |
| D-0021 | T03.04 | R-032, R-037 | Registry tracks findings across 3 simulated runs; stable IDs collision-free | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0021/evidence.md` | S | Low |
| D-0022 | T04.01 | R-039 | Extended `semantic_layer.py` receiving only non-structural dimensions, chunked input, structural context | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0022/spec.md` | L | Medium |
| D-0023 | T04.02 | R-040 | Prompt budget enforcement: 30,720 byte total, proportional allocation, truncation markers | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0023/spec.md` | M | Medium |
| D-0024 | T04.03 | R-041, R-042 | `validate_semantic_high()` with prosecutor/defender parallel execution and deterministic judge | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0024/spec.md` | L | High |
| D-0025 | T04.04 | R-043 | Debate YAML output per finding with rubric scores, margin, verdict; registry updated | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0025/evidence.md` | M | Medium |
| D-0026 | T04.05 | R-039, R-040 | Prior findings from registry correctly influence semantic layer behavior end-to-end | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0026/evidence.md` | M | Medium |
| D-0027 | T04.06 | R-039 | >=70% findings from structural rules (SC-4 intermediate check) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0027/evidence.md` | S | Low |
| D-0028 | T05.01 | R-044 | TurnLedger import, construction, budget guards (`can_launch()`, `can_remediate()`) | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0028/spec.md` | M | High |
| D-0029 | T05.01 | R-044 | Cost constants module-level in `convergence.py`; `reimburse_for_progress()` helper | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0029/spec.md` | M | High |
| D-0030 | T05.02 | R-045 | `execute_fidelity_with_convergence()` with pass condition, monotonic progress, 3-run limit | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0030/spec.md` | XL | High |
| D-0031 | T05.03 | R-046 | Legacy/convergence dispatch via `convergence_enabled` boolean; mutual exclusion verified | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0031/spec.md` | M | High |
| D-0032 | T05.04 | R-046 | `_check_remediation_budget()` and `_print_terminal_halt()` NOT invoked in convergence mode | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0032/evidence.md` | M | High |
| D-0033 | T05.05 | R-047 | Regression detection trigger on structural HIGH count increase | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0033/spec.md` | L | High |
| D-0034 | T05.06 | R-047 | 3 parallel agents in isolated temp dirs, merged by stable ID, consolidated report | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0034/spec.md` | L | High |
| D-0035 | T05.07 | R-047 | Temp directory cleanup: try/finally + atexit; no orphaned dirs after failure simulation | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0035/evidence.md` | M | Medium |
| D-0036 | T05.08 | R-048 | FR-7.1 interface contract validated: `handle_regression()` signature, `RegressionResult` return | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0036/evidence.md` | S | Medium |
| D-0037 | T05.09 | R-044, R-045 | Dual budget mutual exclusion integration test (Risk #5 release blocker) | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0037/evidence.md` | M | High |
| D-0038 | T06.01 | R-049 | Extended `remediate_executor.py` with `RemediationPatch`, per-patch diff-size guard at 30% | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0038/spec.md` | L | High |
| D-0039 | T06.01 | R-049 | `fallback_apply()` deterministic text replacement (min anchor: 5 lines or 200 chars) | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0039/spec.md` | L | High |
| D-0040 | T06.02 | R-050 | `--allow-regeneration` Click flag, config field, guard override with WARNING log | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0040/evidence.md` | S | Low |
| D-0041 | T06.03 | R-051 | Step 8 pipeline wiring: structural -> semantic -> convergence -> remediation | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0041/spec.md` | M | High |
| D-0042 | T06.04 | R-052 | `fidelity.py` deleted; zero remaining references confirmed | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0042/evidence.md` | XS | Low |
| D-0043 | T06.05 | R-053 | SC-1 verified: byte-identical structural findings on identical inputs | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0043/evidence.md` | M | Medium |
| D-0044 | T06.06 | R-053 | SC-2, SC-3, SC-5 verified: convergence budget, edit preservation, legacy compat | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0044/evidence.md` | L | High |
| D-0045 | T06.07 | R-053 | SC-4 and SC-6 verified: >=70% structural, no prompt >30,720 bytes | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0045/evidence.md` | M | Medium |
| D-0046 | T06.08 | R-053 | Open questions OQ-1 through OQ-5 documented with decisions | STANDARD | Direct test execution | `TASKLIST_ROOT/artifacts/D-0046/notes.md` | M | Low |
| D-0047 | T05.02 | R-045 | Convergence result mapped to `StepResult` for pipeline compatibility | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0047/spec.md` | XL | High |
| D-0048 | T06.01 | R-049 | `check_morphllm_available()` MCP runtime probe (future migration prep) | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0048/spec.md` | L | High |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-002 | T01.01 | D-0001 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-003 | T01.01 | D-0001 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-004 | T01.01 | D-0001 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-005 | T01.01 | D-0001 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0001/` |
| R-006 | T01.01, T01.07 | D-0001, D-0011 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0001/`, `TASKLIST_ROOT/artifacts/D-0011/` |
| R-007 | T01.02 | D-0002 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-008 | T01.02 | D-0002 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-009 | T01.02 | D-0002 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-010 | T01.02 | D-0002 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-011 | T01.02 | D-0002 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0002/` |
| R-012 | T01.02 | D-0003 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-013 | T01.02 | D-0003 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-014 | T01.02 | D-0003 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-015 | T01.02 | D-0003 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0003/` |
| R-016 | T01.03, T01.06 | D-0004, D-0010 | STANDARD | 82% | `TASKLIST_ROOT/artifacts/D-0004/`, `TASKLIST_ROOT/artifacts/D-0010/` |
| R-017 | T01.04 | D-0005 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0005/` |
| R-018 | T01.04 | D-0005 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0005/` |
| R-019 | T01.04 | D-0005 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0005/` |
| R-020 | T01.04 | D-0006 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0006/` |
| R-021 | T01.05 | D-0007 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0007/` |
| R-022 | T01.05 | D-0008 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0008/` |
| R-023 | T01.05 | D-0009 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0009/` |
| R-024 | T02.01 | D-0012 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0012/` |
| R-025 | T02.02 | D-0013 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0013/` |
| R-026 | T02.02 | D-0013 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0013/` |
| R-027 | T02.03 | D-0014 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0014/` |
| R-028 | T02.03 | D-0014 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0014/` |
| R-029 | T02.03 | D-0014 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0014/` |
| R-030 | T02.04 | D-0015 | STANDARD | 82% | `TASKLIST_ROOT/artifacts/D-0015/` |
| R-031 | T02.05 | D-0016 | STANDARD | 85% | `TASKLIST_ROOT/artifacts/D-0016/` |
| R-032 | T03.01, T03.04 | D-0017, D-0021 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0017/`, `TASKLIST_ROOT/artifacts/D-0021/` |
| R-033 | T03.01 | D-0017 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0017/` |
| R-034 | T03.01 | D-0018 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0018/` |
| R-035 | T03.02 | D-0019 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0019/` |
| R-036 | T03.02 | D-0019 | STRICT | 85% | `TASKLIST_ROOT/artifacts/D-0019/` |
| R-037 | T03.03, T03.04 | D-0020, D-0021 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0020/`, `TASKLIST_ROOT/artifacts/D-0021/` |
| R-038 | T03.03 | D-0020 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0020/` |
| R-039 | T04.01, T04.05, T04.06 | D-0022, D-0026, D-0027 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0022/`, `TASKLIST_ROOT/artifacts/D-0026/`, `TASKLIST_ROOT/artifacts/D-0027/` |
| R-040 | T04.02, T04.05 | D-0023, D-0026 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0023/`, `TASKLIST_ROOT/artifacts/D-0026/` |
| R-041 | T04.03 | D-0024 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0024/` |
| R-042 | T04.03 | D-0024 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0024/` |
| R-043 | T04.04 | D-0025 | STANDARD | 82% | `TASKLIST_ROOT/artifacts/D-0025/` |
| R-044 | T05.01, T05.09 | D-0028, D-0029, D-0037 | STRICT | 92% | `TASKLIST_ROOT/artifacts/D-0028/`, `TASKLIST_ROOT/artifacts/D-0029/`, `TASKLIST_ROOT/artifacts/D-0037/` |
| R-045 | T05.02, T05.09 | D-0030, D-0037, D-0047 | STRICT | 92% | `TASKLIST_ROOT/artifacts/D-0030/`, `TASKLIST_ROOT/artifacts/D-0037/`, `TASKLIST_ROOT/artifacts/D-0047/` |
| R-046 | T05.03, T05.04 | D-0031, D-0032 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0031/`, `TASKLIST_ROOT/artifacts/D-0032/` |
| R-047 | T05.05, T05.06, T05.07 | D-0033, D-0034, D-0035 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0033/`, `TASKLIST_ROOT/artifacts/D-0034/`, `TASKLIST_ROOT/artifacts/D-0035/` |
| R-048 | T05.08 | D-0036 | STANDARD | 82% | `TASKLIST_ROOT/artifacts/D-0036/` |
| R-049 | T06.01 | D-0038, D-0039, D-0048 | STRICT | 92% | `TASKLIST_ROOT/artifacts/D-0038/`, `TASKLIST_ROOT/artifacts/D-0039/`, `TASKLIST_ROOT/artifacts/D-0048/` |
| R-050 | T06.02 | D-0040 | STANDARD | 80% | `TASKLIST_ROOT/artifacts/D-0040/` |
| R-051 | T06.03 | D-0041 | STRICT | 90% | `TASKLIST_ROOT/artifacts/D-0041/` |
| R-052 | T06.04 | D-0042 | STANDARD | 78% | `TASKLIST_ROOT/artifacts/D-0042/` |
| R-053 | T06.05, T06.06, T06.07, T06.08 | D-0043, D-0044, D-0045, D-0046 | STRICT | 88% | `TASKLIST_ROOT/artifacts/D-0043/`, `TASKLIST_ROOT/artifacts/D-0044/`, `TASKLIST_ROOT/artifacts/D-0045/`, `TASKLIST_ROOT/artifacts/D-0046/` |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|

## Checkpoint Report Template

**Template:**
- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
- `**Scope:** <tasks covered>`
- `## Status`
  - `Overall: Pass | Fail | TBD`
- `## Verification Results` (exactly 3 bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets)
- `## Issues & Follow-ups`
- `## Evidence`

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|

## Generation Notes

- All 6 roadmap phases mapped 1:1 to output phases (no renumbering needed)
- ~60% infrastructure pre-built in v3.0 per spec Section 1.3; tasks reflect MODIFY not CREATE where applicable
- T05.02 (`execute_fidelity_with_convergence()`) scored XL effort and was the only task meeting the XL threshold; subtasks defined as step decomposition within the task
- Roadmap explicitly labels Risk #5 (dual budget mutual exclusion) as "release blocker" -- captured as dedicated integration test task T05.09
