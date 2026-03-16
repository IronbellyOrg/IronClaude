# TASKLIST INDEX -- v2.26 Deviation-Aware Fidelity Pipeline

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | v2.26 Deviation-Aware Fidelity Pipeline |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-03-16 |
| TASKLIST_ROOT | `.dev/releases/current/v2.26-roadmap-v5/` |
| Total Phases | 6 |
| Total Tasks | 45 |
| Total Deliverables | 52 |
| Complexity Class | HIGH |
| Primary Persona | backend |
| Consulting Personas | architect, qa, security |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/releases/current/v2.26-roadmap-v5/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/releases/current/v2.26-roadmap-v5/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/releases/current/v2.26-roadmap-v5/phase-2-tasklist.md` |
| Phase 3 Tasklist | `.dev/releases/current/v2.26-roadmap-v5/phase-3-tasklist.md` |
| Phase 4 Tasklist | `.dev/releases/current/v2.26-roadmap-v5/phase-4-tasklist.md` |
| Phase 5 Tasklist | `.dev/releases/current/v2.26-roadmap-v5/phase-5-tasklist.md` |
| Phase 6 Tasklist | `.dev/releases/current/v2.26-roadmap-v5/phase-6-tasklist.md` |
| Execution Log | `.dev/releases/current/v2.26-roadmap-v5/execution-log.md` |
| Checkpoint Reports | `.dev/releases/current/v2.26-roadmap-v5/checkpoints/` |
| Evidence Directory | `.dev/releases/current/v2.26-roadmap-v5/evidence/` |
| Artifacts Directory | `.dev/releases/current/v2.26-roadmap-v5/artifacts/` |
| Validation Reports | `.dev/releases/current/v2.26-roadmap-v5/validation/` |
| Feedback Log | `.dev/releases/current/v2.26-roadmap-v5/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Pre-Implementation Decisions | T01.01-T01.08 | STRICT: 0, STANDARD: 0, LIGHT: 0, EXEMPT: 8 |
| 2 | phase-2-tasklist.md | Foundation Data Model and Gates | T02.01-T02.08 | STRICT: 5, STANDARD: 2, LIGHT: 0, EXEMPT: 1 |
| 3 | phase-3-tasklist.md | New Pipeline Steps and Prompts | T03.01-T03.11 | STRICT: 8, STANDARD: 2, LIGHT: 0, EXEMPT: 1 |
| 4 | phase-4-tasklist.md | Resume Logic and Recovery | T04.01-T04.08 | STRICT: 4, STANDARD: 2, LIGHT: 1, EXEMPT: 1 |
| 5 | phase-5-tasklist.md | Negative Validation and Verification | T05.01-T05.08 | STRICT: 5, STANDARD: 2, LIGHT: 0, EXEMPT: 1 |
| 6 | phase-6-tasklist.md | Integration Testing and Release | T06.01-T06.08 | STRICT: 2, STANDARD: 4, LIGHT: 0, EXEMPT: 2 |

## Source Snapshot

- v2.26 introduces a deviation-aware fidelity subsystem into the roadmap pipeline
- Solves misclassification of intentional improvements as specification violations
- Adds 2 new pipeline steps: `annotate-deviations` and `deviation-analysis`
- Modifies 3 existing components: `spec-fidelity`, `remediate`, `certify`
- Zero new executor primitives; sprint pipeline completely isolated
- Bounded recovery: max 2 automatic remediation attempts; fail-closed semantics throughout

## Deterministic Rules Applied

- Phase renumbering: roadmap Phase 0-5 renumbered to output Phase 1-6 (sequential, no gaps)
- Task ID scheme: `T<PP>.<TT>` zero-padded 2-digit phase and task numbers
- Checkpoint cadence: after every 5 tasks within phase + end-of-phase checkpoint
- Clarification task rule: no clarification tasks required (roadmap is fully specified)
- Deliverable registry: D-0001 through D-0052, global appearance order
- Effort mapping: computed from roadmap item text length, split status, keyword matches, dependency words
- Risk mapping: computed from security, migration, auth, performance, cross-cutting keyword categories
- Tier classification: STRICT/STANDARD/LIGHT/EXEMPT computed via keyword matching with compound phrase overrides
- Verification routing: tier-determined (STRICT -> sub-agent, STANDARD -> direct test, LIGHT -> sanity, EXEMPT -> skip)
- MCP requirements: STRICT tasks require Sequential + Serena; others optional
- Traceability matrix: every R-### mapped to task(s), deliverable(s), tier, confidence
- Multi-file output: 1 index + 6 phase files = 7 files total
- Critical path override: applied to tasks affecting models.py (T02.01), remediate.py routing (T03.09), freshness/state (T04.01, T04.02)

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | 1 | OQ-A / OQ-B: Does GateCriteria.aux_inputs exist? This decision cascades to FR-079 implementation |
| R-002 | 1 | OQ-C: How are PRE_APPROVED IDs extracted for gate validation? Depends on OQ-A resolution |
| R-003 | 1 | OQ-E: Confirm or define _extract_fidelity_deviations() signature |
| R-004 | 1 | OQ-F: Confirm or define _extract_deviation_classes() signature |
| R-005 | 1 | OQ-G: Confirm build_remediate_step() module location from v2.24.2 codebase |
| R-006 | 1 | OQ-H: Confirm roadmap_run_step() interface for the post-step hook needed for roadmap_hash injection |
| R-007 | 1 | OQ-I: Confirm token-count field availability in Claude subprocess API response |
| R-008 | 1 | OQ-J: Document v2.26 handling for FR-077 dual-budget-exhaustion note behavior |
| R-009 | 1 | Verify against codebase: no modifications to generic pipeline layer, no new executor primitives |
| R-010 | 1 | fidelity.py must appear explicitly; confirm _extract_fidelity_deviations() and _extract_deviation_classes() |
| R-011 | 1 | Resolve circular import risk and module boundary for _parse_routing_list() placement |
| R-012 | 1 | Implementation decision log (all OQs resolved or deferred with fallback documented) |
| R-013 | 1 | Requirement traceability matrix (requirement -> file(s) -> test(s) -> milestone) |
| R-014 | 1 | Confirmed module ownership map including fidelity.py disposition |
| R-015 | 1 | Test plan aligned to SC-1 through SC-10 |
| R-016 | 1 | Phase 0 Exit Criteria: all 8 open questions resolved, fidelity.py inspected |
| R-017 | 2 | Add deviation_class: str = "UNCLASSIFIED" field to Finding dataclass |
| R-018 | 2 | Add VALID_DEVIATION_CLASSES frozenset: SLIP, INTENTIONAL, AMBIGUOUS, PRE_APPROVED, UNCLASSIFIED |
| R-019 | 2 | Add __post_init__ validation of deviation_class against VALID_DEVIATION_CLASSES |
| R-020 | 2 | Verify backward compatibility: all existing Finding constructors continue to work |
| R-021 | 2 | Rename _parse_frontmatter() to parse_frontmatter() — grep all callers; single atomic commit |
| R-022 | 2 | Implement _parse_routing_list(): split on comma, strip whitespace, validate against regex |
| R-023 | 2 | Integer-parsing checks must distinguish missing / malformed / failing values with distinct log |
| R-024 | 2 | _certified_is_true() — FR-028 semantic check |
| R-025 | 2 | _validation_complete_true() — FR-053 semantic check |
| R-026 | 2 | _no_ambiguous_deviations() — FR-026 semantic check |
| R-027 | 2 | _routing_consistent_with_slip_count() — FR-056 semantic check |
| R-028 | 2 | _pre_approved_not_in_fix_roadmap() — FR-079 semantic check |
| R-029 | 2 | _slip_count_matches_routing() — FR-081 semantic check |
| R-030 | 2 | _total_annotated_consistent() — FR-085 semantic check |
| R-031 | 2 | _total_analyzed_consistent() — FR-086 semantic check |
| R-032 | 2 | _routing_ids_valid() — FR-074 semantic check |
| R-033 | 2 | Define ANNOTATE_DEVIATIONS_GATE — STANDARD tier, roadmap_hash required, _total_annotated_consistent check |
| R-034 | 2 | Define DEVIATION_ANALYSIS_GATE — STRICT tier, 6 semantic checks in order |
| R-035 | 2 | Modify SPEC_FIDELITY_GATE: downgrade STRICT to STANDARD, remove deprecated checks |
| R-036 | 2 | Modify CERTIFY_GATE: append certified_true semantic check |
| R-037 | 2 | Update ALL_GATES registry with both new gate entries |
| R-038 | 2 | Retain deprecated semantic check functions with [DEPRECATED v2.26] docstrings |
| R-039 | 2 | Phase 1 Exit Criteria: Finding constructs, semantic checks pass, gates defined |
| R-040 | 3 | build_annotate_deviations_prompt() — new function with anti-laundering rules |
| R-041 | 3 | build_deviation_analysis_prompt() — new function with routing table and blast radius |
| R-042 | 3 | Modify build_spec_fidelity_prompt() — add spec_deviations_path parameter |
| R-043 | 3 | Add annotate-deviations step between merge and test-strategy in _build_steps() |
| R-044 | 3 | Add deviation-analysis step after spec-fidelity in _build_steps() |
| R-045 | 3 | Update _get_all_step_ids() to include both new steps — verify 13 steps |
| R-046 | 3 | Pass spec-deviations.md as additional input to spec-fidelity step |
| R-047 | 3 | Add roadmap_hash injection: SHA-256 of roadmap.md, atomic write pattern |
| R-048 | 3 | Record started_at, completed_at, token_count for new steps in _save_state() |
| R-049 | 3 | When annotate-deviations produces total_annotated: 0, log INFO and continue pipeline |
| R-050 | 3 | Print routing_update_spec summary in CLI output when non-empty |
| R-051 | 3 | deviations_to_findings() — new function converting classified deviations to Finding objects |
| R-052 | 3 | Update remediation step to use deviation-analysis.md routing table as primary input |
| R-053 | 3 | Update remediation prompt with deviation-class awareness: fix only SLIPs |
| R-054 | 3 | Phase 2 Exit Criteria: prompts produce well-formed contracts, 13 steps, hash injection |
| R-055 | 4 | _check_annotate_deviations_freshness() — compare roadmap_hash, fail-closed |
| R-056 | 4 | Integrate freshness check into _apply_resume() before skipping annotate-deviations |
| R-057 | 4 | Add remediation_attempts counter to .roadmap-state.json |
| R-058 | 4 | _check_remediation_budget() — max 2 attempts, coerce to int, return False on exhaustion |
| R-059 | 4 | _print_terminal_halt() — stderr with attempt count, findings, manual-fix instructions |
| R-060 | 4 | Caller logic: on third --resume attempt (budget exhausted), sys.exit(1) |
| R-061 | 4 | Atomic state writes: .tmp + os.replace() for .roadmap-state.json |
| R-062 | 4 | _save_state() coerces existing_attempts to int before incrementing |
| R-063 | 4 | Existing .roadmap-state.json without remediation_attempts defaults to 0 gracefully |
| R-064 | 4 | Retire _apply_resume_after_spec_patch() from active execution |
| R-065 | 4 | Retain _apply_resume_after_spec_patch() and _spec_patch_cycle_count as dormant |
| R-066 | 4 | Ensure spec-patch and remediation budgets remain independent counters |
| R-067 | 4 | FR-077 placeholder: dual-budget-exhaustion note in _print_terminal_halt() |
| R-068 | 4 | Phase 3 Exit Criteria: freshness passes 9 cases, budget caps, spec-patch retired |
| R-069 | 5 | Refuse bogus intentional claims: INTENTIONAL_IMPROVEMENT without valid citation rejected |
| R-070 | 5 | Refuse stale deviation artifacts: roadmap_hash mismatch triggers rerun |
| R-071 | 5 | Refuse ambiguous continuation: ambiguous_count > 0 causes STRICT gate failure |
| R-072 | 5 | Refuse false certification: certified: false causes CERTIFY_GATE failure |
| R-073 | 5 | Refuse third remediation attempt: budget exhaustion triggers terminal halt |
| R-074 | 5 | Certify behavior alignment: _certified_is_true() blocks, manual-fix recovery works |
| R-075 | 5 | Roadmap diff verification: changed sections map exclusively to SLIP-classified IDs |
| R-076 | 5 | Phase 4 Exit Criteria: 5 refusal behaviors verified, no prohibited modifications |
| R-077 | 6 | test_gates_data.py: all 10 semantic check functions with boundary inputs |
| R-078 | 6 | test_models.py: Finding with deviation_class (existing + new field, default compatibility) |
| R-079 | 6 | test_remediate.py: deviations_to_findings() and _parse_routing_list() |
| R-080 | 6 | test_executor.py: freshness 9 cases, budget check, terminal halt stderr |
| R-081 | 6 | test_integration_v5_pipeline.py: complete v2.24 scenario SC-1 through SC-6 |
| R-082 | 6 | NFR-009/NFR-010: pipeline/executor.py and pipeline/models.py zero modifications |
| R-083 | 6 | Manual validation run: execute full pipeline against v2.24 spec file |
| R-084 | 6 | Artifact inspection: spec-deviations.md, deviation-analysis.md, spec-fidelity.md |
| R-085 | 6 | Pipeline completion: verify SC-1 pipeline completes without fidelity halt |
| R-086 | 6 | SC-7: no new classes in pipeline/models.py or pipeline/executor.py |
| R-087 | 6 | Release readiness checklist: SC-1 through SC-10 verified with evidence |
| R-088 | 6 | Phase 5 Exit Criteria: all tests pass, SC-1 through SC-10 verified |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001, R-002 | OQ-A/OQ-B resolution decision | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0001/evidence.md` | XS | Low |
| D-0002 | T01.02 | R-003, R-004, R-010 | fidelity.py function signatures | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0002/evidence.md` | S | Low |
| D-0003 | T01.03 | R-005, R-006, R-007 | Executor interface confirmations | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0003/evidence.md` | S | Low |
| D-0004 | T01.04 | R-008 | FR-077 dual-budget documentation | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0004/notes.md` | XS | Low |
| D-0005 | T01.05 | R-009 | Architecture constraint verification | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0005/evidence.md` | S | Low |
| D-0006 | T01.06 | R-011 | Module placement decision | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0006/notes.md` | S | Medium |
| D-0007 | T01.07 | R-012, R-013, R-014 | Implementation decision log | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0007/spec.md` | M | Low |
| D-0008 | T01.07 | R-013, R-014, R-015 | Traceability matrix + module map + test plan | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0008/spec.md` | M | Low |
| D-0009 | T01.08 | R-016 | Phase 1 exit criteria verification | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0009/evidence.md` | XS | Low |
| D-0010 | T02.01 | R-017, R-018, R-019, R-020 | Finding.deviation_class + validation | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0010/spec.md` | M | Medium |
| D-0011 | T02.02 | R-021 | parse_frontmatter() rename | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0011/evidence.md` | S | Low |
| D-0012 | T02.03 | R-022, R-023 | _parse_routing_list() implementation | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0012/spec.md` | M | Medium |
| D-0013 | T02.04 | R-024-R-032 | 9 semantic check functions | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` | L | Medium |
| D-0014 | T02.05 | R-033, R-034 | New gate definitions | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0014/spec.md` | M | Medium |
| D-0015 | T02.06 | R-035, R-036 | Modified gates | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0015/spec.md` | M | Medium |
| D-0016 | T02.07 | R-037, R-038 | ALL_GATES registry + deprecated retention | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0016/evidence.md` | S | Low |
| D-0017 | T02.08 | R-039 | Phase 2 exit criteria verification | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0017/evidence.md` | XS | Low |
| D-0018 | T03.01 | R-040 | annotate-deviations prompt builder | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0018/spec.md` | L | Medium |
| D-0019 | T03.02 | R-041 | deviation-analysis prompt builder | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0019/spec.md` | L | Medium |
| D-0020 | T03.03 | R-042 | Modified spec-fidelity prompt | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0020/spec.md` | M | Medium |
| D-0021 | T03.04 | R-043, R-046 | annotate-deviations step wiring | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0021/spec.md` | M | High |
| D-0022 | T03.05 | R-044 | deviation-analysis step wiring | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0022/spec.md` | M | High |
| D-0023 | T03.06 | R-045 | 13-step pipeline order | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0023/evidence.md` | S | Medium |
| D-0024 | T03.07 | R-047, R-048 | roadmap_hash injection + state recording | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0024/spec.md` | M | Medium |
| D-0025 | T03.08 | R-049, R-050 | Graceful degradation + CLI output | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0025/evidence.md` | S | Low |
| D-0026 | T03.09 | R-051 | deviations_to_findings() function | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0026/spec.md` | M | Medium |
| D-0027 | T03.10 | R-052, R-053 | Updated remediation step + prompt | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0027/spec.md` | M | Medium |
| D-0028 | T03.11 | R-054 | Phase 3 exit criteria verification | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0028/evidence.md` | XS | Low |
| D-0029 | T04.01 | R-055, R-056 | Freshness detection function | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0029/spec.md` | L | High |
| D-0030 | T04.02 | R-057, R-063 | remediation_attempts counter | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0030/spec.md` | M | Medium |
| D-0031 | T04.03 | R-058, R-060 | Budget enforcement function | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0031/spec.md` | M | Medium |
| D-0032 | T04.04 | R-059 | Terminal halt function | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0032/spec.md` | M | Low |
| D-0033 | T04.05 | R-061, R-062 | Atomic writes + coercion | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0033/spec.md` | M | Medium |
| D-0034 | T04.06 | R-064, R-065, R-066 | Spec-patch retirement | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0034/evidence.md` | S | Medium |
| D-0035 | T04.07 | R-067 | Dual-budget placeholder | LIGHT | Sanity check | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0035/notes.md` | XS | Low |
| D-0036 | T04.08 | R-068 | Phase 4 exit criteria verification | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0036/evidence.md` | XS | Low |
| D-0037 | T05.01 | R-069 | Bogus intentional refusal evidence | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0037/evidence.md` | M | Medium |
| D-0038 | T05.02 | R-070 | Stale artifact refusal evidence | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0038/evidence.md` | M | Medium |
| D-0039 | T05.03 | R-071 | Ambiguous continuation refusal evidence | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0039/evidence.md` | M | Medium |
| D-0040 | T05.04 | R-072 | False certification refusal evidence | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0040/evidence.md` | M | Medium |
| D-0041 | T05.05 | R-073 | Third remediation refusal evidence | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0041/evidence.md` | M | Medium |
| D-0042 | T05.06 | R-074 | Certify behavior alignment evidence | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0042/evidence.md` | S | Low |
| D-0043 | T05.07 | R-075 | SLIP-only remediation diff evidence | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0043/evidence.md` | M | Low |
| D-0044 | T05.08 | R-076 | Phase 5 exit criteria verification | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0044/evidence.md` | XS | Low |
| D-0045 | T06.01 | R-077 | Semantic check unit tests | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0045/evidence.md` | L | Low |
| D-0046 | T06.02 | R-078 | Finding model unit tests | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0046/evidence.md` | S | Low |
| D-0047 | T06.03 | R-079 | Remediation unit tests | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0047/evidence.md` | M | Low |
| D-0048 | T06.04 | R-080 | Executor unit tests | STANDARD | Direct test | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0048/evidence.md` | L | Low |
| D-0049 | T06.05 | R-081 | Integration tests | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0049/spec.md` | L | Medium |
| D-0050 | T06.06 | R-082 | Static diff evidence | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0050/evidence.md` | XS | Low |
| D-0051 | T06.07 | R-083, R-084, R-085, R-086 | Manual validation evidence | STRICT | Sub-agent | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0051/evidence.md` | L | Medium |
| D-0052 | T06.08 | R-087, R-088 | Release readiness checklist | EXEMPT | Skip | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0052/spec.md` | S | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0001/evidence.md` |
| R-002 | T01.01 | D-0001 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0001/evidence.md` |
| R-003 | T01.02 | D-0002 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0002/evidence.md` |
| R-004 | T01.02 | D-0002 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0002/evidence.md` |
| R-005 | T01.03 | D-0003 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0003/evidence.md` |
| R-006 | T01.03 | D-0003 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0003/evidence.md` |
| R-007 | T01.03 | D-0003 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0003/evidence.md` |
| R-008 | T01.04 | D-0004 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0004/notes.md` |
| R-009 | T01.05 | D-0005 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0005/evidence.md` |
| R-010 | T01.02 | D-0002 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0002/evidence.md` |
| R-011 | T01.06 | D-0006 | EXEMPT | 80% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0006/notes.md` |
| R-012 | T01.07 | D-0007 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0007/spec.md` |
| R-013 | T01.07 | D-0007, D-0008 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0007/spec.md`, `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0008/spec.md` |
| R-014 | T01.07 | D-0007, D-0008 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0007/spec.md`, `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0008/spec.md` |
| R-015 | T01.07 | D-0008 | EXEMPT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0008/spec.md` |
| R-016 | T01.08 | D-0009 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0009/evidence.md` |
| R-017 | T02.01 | D-0010 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0010/spec.md` |
| R-018 | T02.01 | D-0010 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0010/spec.md` |
| R-019 | T02.01 | D-0010 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0010/spec.md` |
| R-020 | T02.01 | D-0010 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0010/spec.md` |
| R-021 | T02.02 | D-0011 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0011/evidence.md` |
| R-022 | T02.03 | D-0012 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0012/spec.md` |
| R-023 | T02.03 | D-0012 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0012/spec.md` |
| R-024 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-025 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-026 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-027 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-028 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-029 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-030 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-031 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-032 | T02.04 | D-0013 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0013/spec.md` |
| R-033 | T02.05 | D-0014 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0014/spec.md` |
| R-034 | T02.05 | D-0014 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0014/spec.md` |
| R-035 | T02.06 | D-0015 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0015/spec.md` |
| R-036 | T02.06 | D-0015 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0015/spec.md` |
| R-037 | T02.07 | D-0016 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0016/evidence.md` |
| R-038 | T02.07 | D-0016 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0016/evidence.md` |
| R-039 | T02.08 | D-0017 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0017/evidence.md` |
| R-040 | T03.01 | D-0018 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0018/spec.md` |
| R-041 | T03.02 | D-0019 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0019/spec.md` |
| R-042 | T03.03 | D-0020 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0020/spec.md` |
| R-043 | T03.04 | D-0021 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0021/spec.md` |
| R-044 | T03.05 | D-0022 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0022/spec.md` |
| R-045 | T03.06 | D-0023 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0023/evidence.md` |
| R-046 | T03.04 | D-0021 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0021/spec.md` |
| R-047 | T03.07 | D-0024 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0024/spec.md` |
| R-048 | T03.07 | D-0024 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0024/spec.md` |
| R-049 | T03.08 | D-0025 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0025/evidence.md` |
| R-050 | T03.08 | D-0025 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0025/evidence.md` |
| R-051 | T03.09 | D-0026 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0026/spec.md` |
| R-052 | T03.10 | D-0027 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0027/spec.md` |
| R-053 | T03.10 | D-0027 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0027/spec.md` |
| R-054 | T03.11 | D-0028 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0028/evidence.md` |
| R-055 | T04.01 | D-0029 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0029/spec.md` |
| R-056 | T04.01 | D-0029 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0029/spec.md` |
| R-057 | T04.02 | D-0030 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0030/spec.md` |
| R-058 | T04.03 | D-0031 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0031/spec.md` |
| R-059 | T04.04 | D-0032 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0032/spec.md` |
| R-060 | T04.03 | D-0031 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0031/spec.md` |
| R-061 | T04.05 | D-0033 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0033/spec.md` |
| R-062 | T04.05 | D-0033 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0033/spec.md` |
| R-063 | T04.02 | D-0030 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0030/spec.md` |
| R-064 | T04.06 | D-0034 | STANDARD | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0034/evidence.md` |
| R-065 | T04.06 | D-0034 | STANDARD | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0034/evidence.md` |
| R-066 | T04.06 | D-0034 | STANDARD | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0034/evidence.md` |
| R-067 | T04.07 | D-0035 | LIGHT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0035/notes.md` |
| R-068 | T04.08 | D-0036 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0036/evidence.md` |
| R-069 | T05.01 | D-0037 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0037/evidence.md` |
| R-070 | T05.02 | D-0038 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0038/evidence.md` |
| R-071 | T05.03 | D-0039 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0039/evidence.md` |
| R-072 | T05.04 | D-0040 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0040/evidence.md` |
| R-073 | T05.05 | D-0041 | STRICT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0041/evidence.md` |
| R-074 | T05.06 | D-0042 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0042/evidence.md` |
| R-075 | T05.07 | D-0043 | STANDARD | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0043/evidence.md` |
| R-076 | T05.08 | D-0044 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0044/evidence.md` |
| R-077 | T06.01 | D-0045 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0045/evidence.md` |
| R-078 | T06.02 | D-0046 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0046/evidence.md` |
| R-079 | T06.03 | D-0047 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0047/evidence.md` |
| R-080 | T06.04 | D-0048 | STANDARD | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0048/evidence.md` |
| R-081 | T06.05 | D-0049 | STRICT | 85% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0049/spec.md` |
| R-082 | T06.06 | D-0050 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0050/evidence.md` |
| R-083 | T06.07 | D-0051 | STRICT | 80% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0051/evidence.md` |
| R-084 | T06.07 | D-0051 | STRICT | 80% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0051/evidence.md` |
| R-085 | T06.07 | D-0051 | STRICT | 80% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0051/evidence.md` |
| R-086 | T06.07 | D-0051 | STRICT | 80% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0051/evidence.md` |
| R-087 | T06.08 | D-0052 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0052/spec.md` |
| R-088 | T06.08 | D-0052 | EXEMPT | 90% | `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0052/spec.md` |

## Execution Log Template

**Intended Path:** `.dev/releases/current/v2.26-roadmap-v5/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run (verbatim cmd or "Manual") | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| | | | | | | | |

## Checkpoint Report Template

**Template:**

```
# Checkpoint Report -- <Checkpoint Title>
**Checkpoint Report Path:** .dev/releases/current/v2.26-roadmap-v5/checkpoints/<deterministic-name>.md
**Scope:** <tasks covered>
## Status
Overall: Pass | Fail | TBD
## Verification Results
- <bullet 1>
- <bullet 2>
- <bullet 3>
## Exit Criteria Assessment
- <bullet 1>
- <bullet 2>
- <bullet 3>
## Issues & Follow-ups
- <list blocking issues referencing T<PP>.<TT> and D-####>
## Evidence
- <bullet list of evidence paths under .dev/releases/current/v2.26-roadmap-v5/evidence/>
```

## Feedback Collection Template

**Intended Path:** `.dev/releases/current/v2.26-roadmap-v5/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
| | | | | | | |

## Generation Notes

- Phase renumbering: roadmap Phase 0 through Phase 5 mapped to output Phase 1 through Phase 6 (sequential, no gaps)
- No clarification tasks were needed: the roadmap is fully specified with concrete deliverables, acceptance criteria, and success criteria
- TASKLIST_ROOT derived from version token `v2.26` (first match in roadmap text at line 7)
- Critical path overrides applied to T02.01 (models.py), T03.09 (remediate.py), T04.01 (freshness), T04.02 (state schema)
- All Phase 1 tasks classified EXEMPT: entirely investigation/planning with no code modifications
- Tie-breaker applied for T01.06 module placement: prefer no new external dependencies (remain in remediate.py) unless circular import detected
