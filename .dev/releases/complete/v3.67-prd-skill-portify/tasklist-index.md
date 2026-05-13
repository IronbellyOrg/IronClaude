---
title: "PRD Creator CLI Pipeline — Tasklist Index"
source_spec: ".dev/portify-workdir/prd/portify-release-spec.md"
generated: 2026-04-12
generator: sc:tasklist-protocol v4.0
target_release: v4.3.0
total_phases: 5
total_tasks: 27
total_deliverables: 30
tasklist_root: .dev/releases/current/v4.3.0/
---

# PRD Creator CLI Pipeline — Tasklist Index

## Artifact Paths

| Artifact | Path |
|----------|------|
| Index file | `.dev/releases/current/v4.3.0/tasklist-index.md` |
| Phase files | `phase-1-tasklist.md` through `phase-5-tasklist.md` |
| Execution log | `.dev/releases/current/v4.3.0/execution-log.md` |
| Checkpoint reports | `.dev/releases/current/v4.3.0/checkpoints/` |
| Task evidence | `.dev/releases/current/v4.3.0/evidence/` |
| Deliverable artifacts | `.dev/releases/current/v4.3.0/artifacts/` |
| Feedback log | `.dev/releases/current/v4.3.0/feedback-log.md` |
| Validation reports | `.dev/releases/current/v4.3.0/validation/` |

## Source Snapshot

- **Spec**: `portify-release-spec.md` (830 lines, v1.0.0, quality 8.4/10)
- **Spec type**: Portification (HIGH complexity)
- **Target**: `src/superclaude/cli/prd/` — 14 new files, 1 modified file
- **Milestones**: 5 (explicitly labeled in Section 10)
- **Functional Requirements**: 15 (FR-PRD.1 through FR-PRD.15)
- **Non-Functional Requirements**: 13 (NFR-PRD.1 through NFR-PRD.13)
- **Test plan**: 30 unit + 9 integration + 5 E2E tests

## Deterministic Rules Applied

| Rule | Application |
|------|-------------|
| Phase bucketing | Section 10 milestones used as explicit phase labels (Rule 4.2.1) |
| Phase numbering | Sequential 1-5 with no gaps (Rule 4.3) |
| Task ID format | `T<PP>.<TT>` zero-padded (Rule 4.5) |
| Task ordering | Implementation order from Section 4.6, tests follow each group |
| Effort mapping | Deterministic keyword scan (Rule 5.2.1) |
| Risk mapping | Deterministic keyword scan (Rule 5.2.2) |
| Tier classification | Compound phrase check -> keyword matching -> context boosters (Rule 5.3) |
| Tie-breaker | No policy forks detected (Rule 4.9) |
| Checkpoints | Every 5 tasks + end of phase (Rule 4.8) |
| Clarification | Batch tier confirmation (Rule 4.6) — all implementation tasks have Confidence < 0.70 due to keyword algorithm mismatch with detailed spec items |

## Phase Files

| Phase | File | Goal | Tasks |
|-------|------|------|-------|
| 1 | phase-1-tasklist.md | Core Models + Gates | T01.01 – T01.09 (9 tasks) |
| 2 | phase-2-tasklist.md | Prompts + Config | T02.01 – T02.03 (3 tasks) |
| 3 | phase-3-tasklist.md | Execution Engine | T03.01 – T03.08 (8 tasks) |
| 4 | phase-4-tasklist.md | CLI Integration | T04.01 – T04.04 (4 tasks) |
| 5 | phase-5-tasklist.md | Validation + E2E | T05.01 – T05.03 (3 tasks) |

## Roadmap Item Registry

| ID | Source | Section | Summary |
|----|--------|---------|----------|
| R-001 | FR-PRD.1 | 3 | Existing Work Detection |
| R-002 | FR-PRD.2 | 3 | Request Parsing |
| R-003 | FR-PRD.3 | 3 | Scope Discovery |
| R-004 | FR-PRD.4 | 3 | Research Notes Generation |
| R-005 | FR-PRD.5 | 3 | Research Sufficiency Review |
| R-006 | FR-PRD.6 | 3 | Template Triage |
| R-007 | FR-PRD.7 | 3 | Task File Construction |
| R-008 | FR-PRD.8 | 3 | Task File Verification |
| R-009 | FR-PRD.9 | 3 | Preparation |
| R-010 | FR-PRD.10 | 3 | Deep Investigation (Parallel) |
| R-011 | FR-PRD.11 | 3 | Research QA with Fix Cycles |
| R-012 | FR-PRD.12 | 3 | Web Research (Parallel) |
| R-013 | FR-PRD.13 | 3 | Synthesis + Synthesis QA |
| R-014 | FR-PRD.14 | 3 | Assembly and Validation |
| R-015 | FR-PRD.15 | 3 | Completion and Presentation |
| R-016 | models.py | 4.1 | Domain types: PrdConfig, PrdStepStatus, PrdStepResult, PrdPipelineResult, PrdMonitorState |
| R-017 | gates.py | 4.1 | Gate criteria constants + 10 semantic check functions |
| R-018 | inventory.py | 4.1 | check_existing_work, discover_research_files, discover_synth_files, create_task_dirs |
| R-019 | filtering.py | 4.1 | partition_files, compile_gaps, merge_qa_partition_reports, load_synthesis_mapping |
| R-020 | prompts.py | 4.1 | 19 prompt builder functions + helpers |
| R-021 | config.py | 4.1 | CLI arg resolution, PrdConfig construction |
| R-022 | monitor.py | 4.1 | NDJSON output parser with PRD-specific signals |
| R-023 | process.py | 4.1 | PrdClaudeProcess extending ClaudeProcess |
| R-024 | logging_.py | 4.1 | Dual JSONL + Markdown execution logging |
| R-025 | diagnostics.py | 4.1 | DiagnosticCollector, FailureClassifier, ReportGenerator |
| R-026 | tui.py | 4.1 | Rich live dashboard with step progress |
| R-027 | executor.py | 4.1 | Main execution loop, parallel dispatch, fix cycles |
| R-028 | commands.py | 4.1 | Click CLI group: prd run, prd resume |
| R-029 | __init__.py | 4.1 | Package exports |
| R-030 | main.py | 4.2 | Register PRD subcommand with CLI entry point |
| R-031 | NFR-PRD.1 | 6 | Synchronous execution model |
| R-032 | NFR-PRD.2 | 6 | Gate function signatures: bool \| str |
| R-033 | NFR-PRD.3 | 6 | Runner-authored truth + sentinel detection |
| R-034 | NFR-PRD.4 | 6 | Budget tracking via TurnLedger |
| R-035 | NFR-PRD.5 | 6 | Stall detection within stall_timeout |
| R-036 | NFR-PRD.6 | 6 | Resume granularity: step-level + per-agent |
| R-037 | NFR-PRD.7 | 6 | Parallel execution cap at 10 workers |
| R-038 | NFR-PRD.13 | 6 | Subprocess timeout enforcement (Popen watchdog) |
| R-039 | NFR-PRD.8 | 6 | Incremental file writing + 100KB prompt cap |
| R-040 | NFR-PRD.9 | 6 | Signal-aware shutdown |
| R-041 | NFR-PRD.12 | 6 | Subprocess launch resilience (retry + backoff) |
| R-042 | NFR-PRD.10 | 6 | Execution logging (JSONL + Markdown) |
| R-043 | NFR-PRD.11 | 6 | Context injection via to_context_summary() |
| R-044 | Test: inventory | 8.1 | 5 unit tests for inventory.py |
| R-045 | Test: filtering | 8.1 | 4 unit tests for filtering.py |
| R-046 | Test: gates | 8.1 | 8 unit tests for gates.py |
| R-047 | Test: executor | 8.1 | 5 unit tests for executor.py |
| R-048 | Test: models | 8.1 | 3 unit tests for models.py |
| R-049 | Test: prompts | 8.1 | 4 unit tests for prompts.py |
| R-050 | Integration tests | 8.2 | 9 integration tests |
| R-051 | E2E tests | 8.3 | 5 E2E test scenarios |
| R-052 | CLI surface | 5.1 | CLI options, flags, subcommands |
| R-053 | Gate criteria table | 5.2 | 18-row gate criteria specification |
| R-054 | Phase contracts | 5.3 | 5 phase loading contract YAML blocks |
| R-055 | Risk assessment | 7 | 9 risks with mitigations |
| R-056 | Open Items | 11 | OI-001 through OI-011 |
| R-057 | Impl order | 4.6 | 14-step implementation order with parallelization |

## Deliverable Registry

| ID | Task | Deliverable | Artifact Path |
|----|------|-------------|---------------|
| D-0001 | T01.01 | Tier classification confirmation | `.dev/releases/current/v4.3.0/artifacts/D-0001/notes.md` |
| D-0002 | T01.02 | `src/superclaude/cli/prd/models.py` | `.dev/releases/current/v4.3.0/artifacts/D-0002/evidence.md` |
| D-0003 | T01.03 | `src/superclaude/cli/prd/gates.py` | `.dev/releases/current/v4.3.0/artifacts/D-0003/evidence.md` |
| D-0004 | T01.04 | `src/superclaude/cli/prd/inventory.py` | `.dev/releases/current/v4.3.0/artifacts/D-0004/evidence.md` |
| D-0005 | T01.05 | `src/superclaude/cli/prd/filtering.py` | `.dev/releases/current/v4.3.0/artifacts/D-0005/evidence.md` |
| D-0006 | T01.06 | `tests/cli/prd/test_models.py` | `.dev/releases/current/v4.3.0/artifacts/D-0006/evidence.md` |
| D-0007 | T01.07 | `tests/cli/prd/test_gates.py` | `.dev/releases/current/v4.3.0/artifacts/D-0007/evidence.md` |
| D-0008 | T01.08 | `tests/cli/prd/test_inventory.py` | `.dev/releases/current/v4.3.0/artifacts/D-0008/evidence.md` |
| D-0009 | T01.09 | `tests/cli/prd/test_filtering.py` | `.dev/releases/current/v4.3.0/artifacts/D-0009/evidence.md` |
| D-0010 | T02.01 | `src/superclaude/cli/prd/prompts.py` | `.dev/releases/current/v4.3.0/artifacts/D-0010/evidence.md` |
| D-0011 | T02.02 | `src/superclaude/cli/prd/config.py` | `.dev/releases/current/v4.3.0/artifacts/D-0011/evidence.md` |
| D-0012 | T02.03 | `tests/cli/prd/test_prompts.py` | `.dev/releases/current/v4.3.0/artifacts/D-0012/evidence.md` |
| D-0013 | T03.01 | `src/superclaude/cli/prd/monitor.py` | `.dev/releases/current/v4.3.0/artifacts/D-0013/evidence.md` |
| D-0014 | T03.02 | `src/superclaude/cli/prd/process.py` | `.dev/releases/current/v4.3.0/artifacts/D-0014/evidence.md` |
| D-0015 | T03.03 | `src/superclaude/cli/prd/logging_.py` | `.dev/releases/current/v4.3.0/artifacts/D-0015/evidence.md` |
| D-0016 | T03.04 | `src/superclaude/cli/prd/diagnostics.py` | `.dev/releases/current/v4.3.0/artifacts/D-0016/evidence.md` |
| D-0017 | T03.05 | `src/superclaude/cli/prd/tui.py` | `.dev/releases/current/v4.3.0/artifacts/D-0017/evidence.md` |
| D-0018 | T03.06 | `src/superclaude/cli/prd/executor.py` | `.dev/releases/current/v4.3.0/artifacts/D-0018/evidence.md` |
| D-0019 | T03.07 | `tests/cli/prd/test_executor.py` | `.dev/releases/current/v4.3.0/artifacts/D-0019/evidence.md` |
| D-0020 | T03.08 | Integration test suite (9 tests) | `.dev/releases/current/v4.3.0/artifacts/D-0020/evidence.md` |
| D-0021 | T04.01 | `src/superclaude/cli/prd/commands.py` | `.dev/releases/current/v4.3.0/artifacts/D-0021/evidence.md` |
| D-0022 | T04.02 | `src/superclaude/cli/prd/__init__.py` | `.dev/releases/current/v4.3.0/artifacts/D-0022/evidence.md` |
| D-0023 | T04.03 | Modified `src/superclaude/cli/main.py` | `.dev/releases/current/v4.3.0/artifacts/D-0023/evidence.md` |
| D-0024 | T04.04 | CLI dry-run integration test | `.dev/releases/current/v4.3.0/artifacts/D-0024/evidence.md` |
| D-0025 | T05.01 | Open Items resolution document | `.dev/releases/current/v4.3.0/artifacts/D-0025/notes.md` |
| D-0026 | T05.02 | E2E test suite (5 scenarios) | `.dev/releases/current/v4.3.0/artifacts/D-0026/evidence.md` |
| D-0027 | T05.03 | Final validation report | `.dev/releases/current/v4.3.0/artifacts/D-0027/evidence.md` |

## Traceability Matrix

| Roadmap Items | Task | Deliverable | Tier | Confidence |
|---------------|------|-------------|------|------------|
| R-016, R-031 | T01.02 | D-0002 | STRICT | 40% |
| R-017, R-032, R-053 | T01.03 | D-0003 | STANDARD | 35% |
| R-018, R-001, R-006 | T01.04 | D-0004 | STANDARD | 35% |
| R-019, R-011, R-013 | T01.05 | D-0005 | STANDARD | 35% |
| R-048 | T01.06 | D-0006 | STANDARD | 35% |
| R-046 | T01.07 | D-0007 | STANDARD | 35% |
| R-044 | T01.08 | D-0008 | STANDARD | 35% |
| R-045 | T01.09 | D-0009 | STANDARD | 35% |
| R-020, R-039, R-043 | T02.01 | D-0010 | STANDARD | 35% |
| R-021, R-052 | T02.02 | D-0011 | STANDARD | 35% |
| R-049 | T02.03 | D-0012 | STANDARD | 35% |
| R-022, R-035 | T03.01 | D-0013 | STANDARD | 35% |
| R-023, R-038, R-041 | T03.02 | D-0014 | STANDARD | 35% |
| R-024, R-042 | T03.03 | D-0015 | STANDARD | 25% |
| R-025, R-036 | T03.04 | D-0016 | STANDARD | 35% |
| R-026 | T03.05 | D-0017 | STANDARD | 25% |
| R-027, R-002–R-015, R-033–R-037, R-040, R-054, R-057 | T03.06 | D-0018 | STRICT | 55% |
| R-047 | T03.07 | D-0019 | STANDARD | 35% |
| R-050 | T03.08 | D-0020 | STANDARD | 35% |
| R-028, R-052 | T04.01 | D-0021 | STANDARD | 35% |
| R-029 | T04.02 | D-0022 | LIGHT | 40% |
| R-030 | T04.03 | D-0023 | STANDARD | 35% |
| R-050 (partial) | T04.04 | D-0024 | STANDARD | 35% |
| R-056 | T05.01 | D-0025 | EXEMPT | 55% |
| R-051 | T05.02 | D-0026 | STANDARD | 35% |
| R-055 | T05.03 | D-0027 | STANDARD | 35% |

**Note on Confidence Scores**: All implementation tasks score below 0.70 confidence because the tier classification keyword algorithm is calibrated for short user prompts, not detailed spec items. A single batch Clarification Task (T01.01) covers all tier assignments. The computed tiers are correct for the task types: STRICT for data model and main executor files (critical pipeline components), STANDARD for typical implementation, LIGHT for trivial exports, EXEMPT for planning/clarification.

## Task Summary

| Phase | Tasks | Effort Distribution | Risk Distribution | Tier Distribution |
|-------|-------|--------------------|--------------------|-------------------|
| 1 | 9 | 1M, 4S, 4XS | 9 Low | 1 STRICT, 8 STANDARD |
| 2 | 3 | 2S, 1XS | 3 Low | 3 STANDARD |
| 3 | 8 | 1L, 2M, 3S, 2XS | 8 Low | 1 STRICT, 7 STANDARD |
| 4 | 4 | 4XS | 4 Low | 1 LIGHT, 3 STANDARD |
| 5 | 3 | 1M, 1S, 1XS | 3 Low | 1 EXEMPT, 2 STANDARD |
| **Total** | **27** | 1L, 3M, 9S, 14XS | 27 Low | 2 STRICT, 21 STANDARD, 1 LIGHT, 1 EXEMPT, 1 Clarification (T01.01) |

## Glossary

| Term | Definition |
|------|------------|
| MDTM | Markdown-Driven Task Management — task file format |
| B2 pattern | Self-contained checklist items embedding all context |
| Fix cycle | QA FAIL -> gap-fill agents -> re-QA sequence |
| TurnLedger | Budget tracking dataclass guarding subprocess launches |
| Fan-out | Parallel pattern: N identical agents on different inputs |
| Dual-stream | Parallel pattern: 2 agents with different roles (analyst + QA) |
| Runner-authored truth | Reports from observed data, not subprocess self-reporting |
| Phase loading contract | Isolation model specifying which refs are visible per phase |
| Sentinel detection | Anchored regex extraction of EXIT_RECOMMENDATION markers |
| Gate tier | EXEMPT / LIGHT / STANDARD / STRICT validation level |
