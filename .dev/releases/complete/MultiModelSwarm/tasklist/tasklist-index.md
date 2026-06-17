---
tasklist_id: TL-MULTIMODEL-SWARM
spec_id: SPEC-MULTIMODEL-SWARM
roadmap_source: /config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/roadmap.md
spec_source: /config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/merged-requirements.compressed.md
spec_kind: TDD
tdd_detected: true
phases: 9
generated: 2026-05-31T19:30:32Z
generator: sc-tasklist-protocol
generator_version: 3.7
status: emitted
---

# Tasklist — Multi-Model Swarm Orchestrator

| Field | Value |
|---|---|
| Tasklist ID | TL-MULTIMODEL-SWARM |
| Spec ID | SPEC-MULTIMODEL-SWARM |
| Spec Kind | Technical Design Document (TDD detected via frontmatter §4.1a) |
| Roadmap | `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/roadmap.md` |
| Spec | `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/merged-requirements.compressed.md` |
| Phases | 9 (M1-M9 → Phase 1-9, no renumbering required) |
| Generated | 2026-05-31T19:30:32Z |
| Generator | sc-tasklist-protocol v3.7 |
| Output dir | `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/tasklist/` |

## Phase Files

| Phase | Milestone | File | Task Count |
|---|---|---|---|
| 1 | M1: Foundation, Module Shape & Data Models | `phase-1-tasklist.md` | 22 + 5 cp |
| 2 | M2: Preflight, Schema, Lens Registry & Injection Guard (Wave 0) | `phase-2-tasklist.md` | 22 + 5 cp |
| 3 | M3: Dispatch & Concurrency (Wave 1) | `phase-3-tasklist.md` | 20 + 5 cp |
| 4 | M4: Normalize & Recipe Registry (Wave 2) | `phase-4-tasklist.md` | 13 + 3 cp |
| 5 | M5: Reduce, Merge, Status & Result Contract (Wave 3) | `phase-5-tasklist.md` | 11 + 3 cp |
| 6 | M6: Resume, Crash Recovery & Manifest | `phase-6-tasklist.md` | 8 + 2 cp |
| 7 | M7: Observability, TUI, Detached & Full CLI Surface | `phase-7-tasklist.md` | 17 + 4 cp |
| 8 | M8: Migration, Test Discipline & Hardening | `phase-8-tasklist.md` | 15 + 4 cp |
| 9 | M9: Operational Handoff | `phase-9-tasklist.md` | 6 + 2 cp |

## Source Snapshot

- Roadmap path (absolute): `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/roadmap.md`
- Spec path (absolute): `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/merged-requirements.compressed.md`
- TDD detection: spec frontmatter contains `spec_id`, `spec_version`, structured TDD-style architecture sections; orchestrator force-flag asserted `type: Technical Design Document`. §4.1a TDD treatment applied; content-driven enrichment per §4.4a fires for all phases.
- Roadmap structure: 9 explicit milestones (`## M1` … `## M9`) → bucketed 1:1, no renumbering required (§4.2).

## Deterministic Rules Applied

- §4.1 Roadmap items = each row in the milestone tables. Risk Assessment / Open Questions / Dependencies / Integration Points / Timeline / Spec Coverage rows are CONTEXT, not work units (skipped). Open Questions surfaced as Clarification Tasks where appropriate.
- §4.1a TDD treatment enabled (force-flag from orchestrator).
- §4.2 Phase = milestone (1:1).
- §4.3 No renumbering required.
- §4.4 1 task per roadmap item; mergers applied to near-duplicate rows (documented in task Notes).
- §4.4a Content-driven enrichment applied to all tasks.
- §4.5 T<PP>.<TT> IDs zero-padded.
- §4.6 Clarification Tasks emitted for unresolved Open Questions and items lacking acceptance criteria.
- §4.7 Each task: 1-5 deliverables; 3-8 numbered steps with phase markers; exactly 4 ACs (first AC = specific artifact, Near-Field rule); exactly 2 Validation bullets.
- §4.8 Mid-phase checkpoints every 5 tasks; mandatory end-of-phase checkpoint as LAST task in each phase file. Numbered as `T<PP>.<NN> -- Checkpoint:` (v3.7 Wave 4 rule). Checkpoint deliverable IDs use D-CP<PP>-* family.
- §4.9 No policy forks introduced; tie-break notes in task Notes.
- §4.10 Verification Method scaled to tier (STRICT → tests + verify-sync; STANDARD → tests; LIGHT → smoke; EXEMPT → manual).
- §4.11 Critical Path Override applied: IMM-3..6, INV-001..016, §11.5 injection guard, merge boundary, schema → STRICT regardless of size.
- §5.1 Deliverable Registry with D-#### IDs (sequential) and D-CP<PP>-* for checkpoints.
- §5.2 Effort + Risk computed from row's Eff column (S/M/L) and Description keywords.
- §5.3 Compliance Tier per algorithm.
- §5.4 Confidence bar `[████████--] 80%` per task.
- §5.5 MCP Tool Requirements per tier.
- §5.6 Sub-Agent Delegation per tier+risk.
- §5.7 Traceability Matrix below.

## Roadmap Item Registry

| R-ID | Phase | Roadmap Source ID | Title | Mapped Task |
|---|---|---|---|---|
| R-001 | 1 | AC-001 | Python ≥3.10 + UV mandate | T01.01 |
| R-002 | 1 | AC-002 | New `superclaude swarm` CLI verb | T01.02 |
| R-003 | 1 | AC-003 | Mirror sprint module shape | T01.03 |
| R-004 | 1 | AC-006 | Click ≥8.0.0 CLI group | T01.04 |
| R-005 | 1 | AC-019 | Source-of-truth discipline | T01.05 |
| R-006 | 1 | NFR-015 | Module shape mirror verification | T01.07 |
| R-007 | 1 | COMP-001 | swarm_group entry point | T01.08 |
| R-008 | 1 | COMP-003 | SwarmConfig dataclass | T01.09 |
| R-009 | 1 | COMP-004 | models module aggregator | T01.10 |
| R-010 | 1 | COMP-031 | Transport Protocol interface | T01.11 |
| R-011 | 1 | DM-001 | JobSpec dataclass | T01.13 |
| R-012 | 1 | DM-002 | WorkerSpec dataclass | T01.14 |
| R-013 | 1 | DM-003 | TargetSpec dataclass | T01.15 |
| R-014 | 1 | DM-004 | TransportSpec dataclass | T01.16 |
| R-015 | 1 | DM-005 | PromptSpec dataclass | T01.17 |
| R-016 | 1 | DM-006 | NormalizationSpec dataclass | T01.19 |
| R-017 | 1 | DM-007 | OutputSpec dataclass | T01.20 |
| R-018 | 1 | DM-008 | StatusPolicy dataclass | T01.21 |
| R-019 | 1 | DM-009 | RuntimeSpec dataclass | T01.22 |
| R-020 | 1 | DM-010 | LensEntry dataclass | T01.23 |
| R-021 | 1 | DM-011 | ResolvedLensEntry dataclass | T01.24 |
| R-022 | 1 | DM-012 | ResultContract dataclass | T01.25 |
| R-023 | 1 | DM-013 | WorkerResult dataclass | T01.26 (merged) |
| R-024 | 1 | DM-014 | SwarmState dataclass | T01.26 (merged) |
| R-025 | 1 | DM-015 | EventRecord dataclass | T01.26 (merged) |
| R-026 | 1 | DM-016 | Manifest dataclass | T01.27 |
| R-027 | 1 | DM-017 | DoneSentinel dataclass | T01.28 |
| R-028 | 1 | DM-018 | Artifacts dataclass | T01.28 (merged) |
| R-029 | 1 | DM-019 | CallerInfo dataclass | T01.28 (merged) |
| R-030 | 2 | COMP-005 | schema module | T02.01 |
| R-031 | 2 | COMP-006 | preflight (Wave 0) | T02.02 |
| R-032 | 2 | FR-019 | Job spec JSON Schema validation | T02.03 |
| R-033 | 2 | FR-020 | Lens-driven defaults expansion | T02.04 |
| R-034 | 2 | FR-021 | Custom-prompt-dir escape hatch | T02.05 |
| R-035 | 2 | §11.5 | Prompt-injection guard | T02.07 |
| R-036 | 2 | INV-003 | Custom-prompt-dir identical guard | T02.08 |
| R-037 | 2 | INV-014 | Escape-hatch isomorphism | T02.09 |
| R-038 | 2 | INV-005 | Worker-count vs model-pool guard | T02.10 |
| R-039 | 2 | INV-007 | Empty-pool failure contract | T02.11 |
| R-040 | 2 | IMM-4 | Empty-target guard | T02.13 |
| R-041 | 2 | COMP-022 | LENSES dict + helpers | T02.14 |
| R-042 | 2 | COMP-023 | _validate (lens validator) | T02.15 |
| R-043 | 2 | U-008 | swarm validate-lenses logic | T02.16 |
| R-044 | 2 | FR-009 | Lens registry (8 entries) | T02.17 |
| R-045 | 2 | FR-007 | swarm validate subcommand | T02.19 |
| R-046 | 2 | FR-008 | swarm validate-lenses subcommand | T02.20 |
| R-047 | 2 | FR-LENSREG.NS | normalizer_strategy field | T02.21 |
| R-048 | 2 | FR-024 | --auto-inject-guard flag | T02.22 |
| R-049 | 2 | COMP-024 | bare_review lens | T02.23 |
| R-050 | 2 | COMP-025 | refactor_find lens | T02.23 (merged) |
| R-051 | 2 | COMP-026 | edge_case_hunt lens | T02.23 (merged) |
| R-052 | 2 | COMP-027 | spec_completeness lens | T02.23 (merged) |
| R-053 | 2 | COMP-028 | feasibility_probe lens | T02.23 (merged) |
| R-054 | 2 | COMP-029 | troubleshoot_hypothesis lens | T02.23 (merged) |
| R-055 | 2 | COMP-030 | doc_completeness lens | T02.23 (merged) |
| R-056 | 2 | DM-020 | CallerMetadata (output) | T02.25 |
| R-057 | 2 | NFR-003 | Security: prompt-injection enforcement | T02.26 |
| R-058 | 2 | NFR-012 | Lens-registry PR review discipline | T02.27 |
| R-059 | 2 | AC-013 | No Claude-Code-isms | T02.28 |
| R-060 | 3 | COMP-002 | commands module | T03.01 |
| R-061 | 3 | COMP-007 | dispatch (Wave 1) | T03.02 |
| R-062 | 3 | COMP-011 | state module | T03.03 |
| R-063 | 3 | COMP-012 | logging_ module | T03.04 |
| R-064 | 3 | COMP-032 | openai_compat transport | T03.05 |
| R-065 | 3 | COMP-033 | deterministic-fixture transport | T03.07 |
| R-066 | 3 | FR-001 | swarm run subcommand | T03.08 |
| R-067 | 3 | FR-017 | Per-worker timeout + retry policy | T03.09 |
| R-068 | 3 | FR-022 | openai_compat transport (httpx) | T03.05 (merged) |
| R-069 | 3 | FR-023 | deterministic-fixture transport | T03.07 (merged) |
| R-070 | 3 | FR-026 | Dual-format log emission | T03.10 |
| R-071 | 3 | IMM-3 | True-parallel dispatch | T03.11 |
| R-072 | 3 | IMM-6 | Atomic-write idempotency | T03.13 |
| R-073 | 3 | INV-002 | Python-only concurrency | T03.14 |
| R-074 | 3 | NFR-001 | Concurrency via ParallelExecutor | T03.15 |
| R-075 | 3 | NFR-002 | Atomicity of state transitions | T03.16 |
| R-076 | 3 | NFR-010 | Per-worker hard timeout | T03.09 (merged) |
| R-077 | 3 | NFR-011 | Retry policy | T03.09 (merged) |
| R-078 | 3 | NFR-013 | Filesystem constraint | T03.17 |
| R-079 | 3 | NFR-014 | No cross-invocation caching | T03.19 |
| R-080 | 3 | AC-004 | ParallelExecutor invocation mandate | T03.15 (merged) |
| R-081 | 3 | AC-005 | httpx transport library | T03.05 (merged) |
| R-082 | 3 | AC-010 | No routing to Anthropic models | T03.20 |
| R-083 | 3 | AC-014 | No writes outside --output | T03.17 (merged) |
| R-084 | 3 | AC-015 | No cross-invocation response caching | T03.19 (merged) |
| R-085 | 3 | AC-017 | T2 proxy endpoint env contract | T03.21 |
| R-086 | 4 | COMP-008 | normalize (Wave 2) | T04.01 |
| R-087 | 4 | COMP-015 | Recipe Protocol + REGISTRY | T04.02 |
| R-088 | 4 | COMP-016 | bare_review_v1 recipe | T04.03 |
| R-089 | 4 | COMP-017 | findings_table_v1 recipe | T04.04 |
| R-090 | 4 | COMP-018 | hypothesis_table_v1 recipe | T04.05 |
| R-091 | 4 | COMP-019 | verdict_only_v1 recipe | T04.07 |
| R-092 | 4 | COMP-020 | passthrough recipe | T04.08 |
| R-093 | 4 | COMP-021 | custom (custom-py loader) | T04.09 |
| R-094 | 4 | FR-010 | Recipe Protocol registry (6 normalizers) | T04.10 |
| R-095 | 4 | FR-028 | Parse-error salvage promotion | T04.11 |
| R-096 | 4 | COMP-034 | bare-review output template | T04.12 |
| R-097 | 4 | COMP-035 | Per-lens output templates | T04.13 |
| R-098 | 4 | AC-011 | No scoring/dedup/reorder in recipes | T04.14 |
| R-099 | 5 | COMP-009 | reduce (Wave 3) | T05.01 |
| R-100 | 5 | COMP-010 | merge module | T05.02 |
| R-101 | 5 | IMM-5 | Success-first status determination | T05.03 |
| R-102 | 5 | FR-011 | Three amalgamation modes | T05.04 |
| R-103 | 5 | FR-012 | Mechanical merge module (4 guards) | T05.05 |
| R-104 | 5 | FR-018 | Result contract emission | T05.07 |
| R-105 | 5 | NFR-008 | Merge module ≤30 LOC | T05.08 |
| R-106 | 5 | NFR-009 | Boundary enforcement test | T05.09 |
| R-107 | 5 | AC-012 | No new merge/diff/scoring engine | T05.10 |
| R-108 | 5 | AC-018 | merge.py body ≤30 LOC | T05.08 (merged) |
| R-109 | 5 | AC-011 | No scoring/dedup/reorder/rewrite/filter (merge) | T05.11 |
| R-110 | 6 | INV-001 | Resume rehydrates lens from manifest | T06.01 |
| R-111 | 6 | INV-010 | Resume regenerates merged.md | T06.02 |
| R-112 | 6 | INV-016 | Manifest as durable source-of-truth | T06.03 |
| R-113 | 6 | FR-015 | Resume + crash recovery | T06.04 |
| R-114 | 6 | FR-016 | Manifest emission | T06.05 |
| R-115 | 6 | FR-025 | --force-relens flag | T06.07 |
| R-116 | 6 | NFR-005 | Crash recovery semantics | T06.08 |
| R-117 | 6 | NFR-006 | Schema evolution forward-compat | T06.09 |
| R-118 | 7 | COMP-013 | tui module | T07.01 |
| R-119 | 7 | COMP-014 | tmux module | T07.02 |
| R-120 | 7 | INV-012 | TUI opt-in via --tui | T07.03 |
| R-121 | 7 | FR-002 | swarm status subcommand | T07.04 |
| R-122 | 7 | FR-003 | swarm logs subcommand | T07.05 |
| R-123 | 7 | FR-004 | swarm attach subcommand | T07.07 |
| R-124 | 7 | FR-005 | swarm kill subcommand | T07.08 |
| R-125 | 7 | FR-006 | swarm scaffold subcommand | T07.09 |
| R-126 | 7 | FR-013 | Three monitoring patterns | T07.10 |
| R-127 | 7 | FR-014 | Detached mode via tmux | T07.11 |
| R-128 | 7 | FR-027 | Done sentinel emission | T07.13 |
| R-129 | 7 | NFR-004 | Observability three-layer | T07.14 |
| R-130 | 7 | NFR-016 | Contract surface non-precluding | T07.15 |
| R-131 | 7 | AC-007 | Rich ≥13.0.0 for --tui | T07.16 |
| R-132 | 7 | AC-008 | tmux for detached mode | T07.17 |
| R-133 | 7 | AC-009 | No external framework integration | T07.19 |
| R-134 | 7 | AC-016 | No streaming/function-calling/vision (Phase 1) | T07.20 |
| R-135 | 8 | FR-029 | SKILL.md migration | T08.01 |
| R-136 | 8 | FR-030 | Non-Claude caller compatibility | T08.02 |
| R-137 | 8 | NFR-007 | Test coverage (per-IMM + per-INV) | T08.03 |
| R-138 | 8 | MIG-001 | Source-first sync workflow | T08.04 |
| R-139 | 8 | MIG-002 | Package entry registration | T08.05 |
| R-140 | 8 | MIG-003 | Legacy shell retirement | T08.07 |
| R-141 | 8 | MIG-004 | Release notes + operator migration note | T08.08 |
| R-142 | 8 | TEST-001 | IMM acceptance suite | T08.09 |
| R-143 | 8 | TEST-002 | INV remediation suite | T08.10 |
| R-144 | 8 | TEST-003 | Bare-review parity test | T08.11 |
| R-145 | 8 | TEST-004 | Bundled lens validation gate | T08.13 |
| R-146 | 8 | TEST-005 | Non-Claude caller integration | T08.14 |
| R-147 | 8 | TEST-006 | Mechanical merge boundary test | T08.15 |
| R-148 | 8 | TEST-007 | Resume crash recovery E2E | T08.16 |
| R-149 | 8 | TEST-008 | Wire deterministic-fixture transport | T08.17 |
| R-150 | 9 | OPS-001 | Operator runbook | T09.01 |
| R-151 | 9 | OPS-002 | Environment readiness check | T09.02 |
| R-152 | 9 | OPS-003 | Observability procedure | T09.03 |
| R-153 | 9 | OPS-004 | Rollback procedure | T09.05 |
| R-154 | 9 | OPS-005 | Lens contribution policy | T09.06 |
| R-155 | 9 | OPS-006 | Post-release metrics review | T09.07 |

## Deliverable Registry

| D-ID | Phase | Title | Owning Task | Artifact Path |
|---|---|---|---|---|
| D-0001 | 1 | UV-enforcement CI rule + docs note | T01.01 | `tests/swarm/test_uv_enforcement.py`, `docs/swarm/runbook.md` |
| D-0002 | 1 | `superclaude swarm` top-level verb registration | T01.02 | `src/superclaude/cli/main.py` |
| D-0003 | 1 | `cli/swarm/` directory mirroring `cli/sprint/` | T01.03 | `src/superclaude/cli/swarm/` |
| D-0004 | 1 | Click ≥8.0.0 group declaration | T01.04 | `src/superclaude/cli/swarm/__init__.py` |
| D-0005 | 1 | `make verify-sync` gate doc + pre-commit binding | T01.05 | `docs/dev/sync-discipline.md` |
| D-0006 | 1 | Module-shape parity test | T01.07 | `tests/swarm/test_module_shape.py` |
| D-0007 | 1 | swarm_group Click entry point | T01.08 | `src/superclaude/cli/swarm/__init__.py` |
| D-0008 | 1 | SwarmConfig dataclass + tests | T01.09 | `src/superclaude/cli/swarm/config.py` |
| D-0009 | 1 | models module aggregator | T01.10 | `src/superclaude/cli/swarm/models.py` |
| D-0010 | 1 | Transport Protocol interface | T01.11 | `src/superclaude/cli/swarm/transports/__init__.py` |
| D-0011 | 1 | JobSpec dataclass + JSON round-trip | T01.13 | `src/superclaude/cli/swarm/models.py::JobSpec` |
| D-0012 | 1 | WorkerSpec dataclass | T01.14 | `src/superclaude/cli/swarm/models.py::WorkerSpec` |
| D-0013 | 1 | TargetSpec dataclass | T01.15 | `src/superclaude/cli/swarm/models.py::TargetSpec` |
| D-0014 | 1 | TransportSpec dataclass | T01.16 | `src/superclaude/cli/swarm/models.py::TransportSpec` |
| D-0015 | 1 | PromptSpec dataclass | T01.17 | `src/superclaude/cli/swarm/models.py::PromptSpec` |
| D-0016 | 1 | NormalizationSpec dataclass | T01.19 | `src/superclaude/cli/swarm/models.py::NormalizationSpec` |
| D-0017 | 1 | OutputSpec dataclass | T01.20 | `src/superclaude/cli/swarm/models.py::OutputSpec` |
| D-0018 | 1 | StatusPolicy dataclass | T01.21 | `src/superclaude/cli/swarm/models.py::StatusPolicy` |
| D-0019 | 1 | RuntimeSpec dataclass | T01.22 | `src/superclaude/cli/swarm/models.py::RuntimeSpec` |
| D-0020 | 1 | LensEntry dataclass | T01.23 | `src/superclaude/cli/swarm/models.py::LensEntry` |
| D-0021 | 1 | ResolvedLensEntry dataclass | T01.24 | `src/superclaude/cli/swarm/models.py::ResolvedLensEntry` |
| D-0022 | 1 | ResultContract dataclass | T01.25 | `src/superclaude/cli/swarm/models.py::ResultContract` |
| D-0023 | 1 | WorkerResult+SwarmState+EventRecord (merged) | T01.26 | `src/superclaude/cli/swarm/models.py` |
| D-0024 | 1 | Manifest dataclass | T01.27 | `src/superclaude/cli/swarm/models.py::Manifest` |
| D-0025 | 1 | DoneSentinel+Artifacts+CallerInfo (merged) | T01.28 | `src/superclaude/cli/swarm/models.py` |
| D-CP1-1 | 1 | Phase 1 checkpoint reports (5 × checkpoint review packets) | T01.06, T01.12, T01.18, T01.24a (mid), T01.29 (end) | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-1-cp*.md` |
| D-0026 | 2 | schema module (JSON Schema + cross-field validators) | T02.01 | `src/superclaude/cli/swarm/schema.py` |
| D-0027 | 2 | preflight module (Wave 0) | T02.02 | `src/superclaude/cli/swarm/preflight.py` |
| D-0028 | 2 | Schema cross-field + §11.5 substring validator | T02.03 | `src/superclaude/cli/swarm/schema.py` |
| D-0029 | 2 | Lens-driven defaults expansion logic | T02.04 | `src/superclaude/cli/swarm/preflight.py::expand_lens_defaults` |
| D-0030 | 2 | Custom-prompt-dir escape hatch reader | T02.05 | `src/superclaude/cli/swarm/preflight.py::read_custom_prompt_dir` |
| D-0031 | 2 | §11.5 injection guard (3-path enforcement) | T02.07 | `src/superclaude/cli/swarm/preflight.py::enforce_injection_guard` |
| D-0032 | 2 | INV-003 custom-prompt-dir guard parity test | T02.08 | `tests/swarm/test_custom_prompt_dir_injection_guard.py` |
| D-0033 | 2 | INV-014 escape-hatch isomorphism test | T02.09 | `tests/swarm/test_escape_hatch_guard_parity.py` |
| D-0034 | 2 | INV-005 worker-vs-pool guard | T02.10 | `src/superclaude/cli/swarm/preflight.py::check_pool_size` |
| D-0035 | 2 | INV-007 empty-pool failure contract | T02.11 | `src/superclaude/cli/swarm/preflight.py::emit_env_missing_contract` |
| D-0036 | 2 | IMM-4 empty-target guard | T02.13 | `src/superclaude/cli/swarm/preflight.py::guard_empty_target` |
| D-0037 | 2 | LENSES dict + accessors | T02.14 | `src/superclaude/cli/swarm/lenses/__init__.py` |
| D-0038 | 2 | _validate (lens validator) | T02.15 | `src/superclaude/cli/swarm/lenses/_validate.py` |
| D-0039 | 2 | validate-lenses logic | T02.16 | `src/superclaude/cli/swarm/lenses/_validate.py::validate_all` |
| D-0040 | 2 | 8-entry lens registry (bare + 7) | T02.17 | `src/superclaude/cli/swarm/lenses/` |
| D-0041 | 2 | swarm validate subcommand | T02.19 | `src/superclaude/cli/swarm/commands.py::validate_cmd` |
| D-0042 | 2 | swarm validate-lenses subcommand | T02.20 | `src/superclaude/cli/swarm/commands.py::validate_lenses_cmd` |
| D-0043 | 2 | normalizer_strategy lens field | T02.21 | `src/superclaude/cli/swarm/lenses/registry.py` |
| D-0044 | 2 | --auto-inject-guard flag | T02.22 | `src/superclaude/cli/swarm/preflight.py::auto_inject_guard` |
| D-0045 | 2 | 7 non-custom lens entry files | T02.23 | `src/superclaude/cli/swarm/lenses/{bare_review,refactor_find,edge_case_hunt,spec_completeness,feasibility_probe,troubleshoot_hypothesis,doc_completeness}.py` |
| D-0046 | 2 | CallerMetadata (DM-020) | T02.25 | `src/superclaude/cli/swarm/models.py::CallerMetadata` |
| D-0047 | 2 | NFR-003 prompt-injection enforcement test (end-marker neutralization) | T02.26 | `tests/swarm/test_prompt_injection_neutralization.py` |
| D-0048 | 2 | Lens-registry PR review checklist | T02.27 | `docs/dev/lens-contribution-policy.md` |
| D-0049 | 2 | Claude-ism grep audit CI gate | T02.28 | `tests/swarm/test_no_claude_isms.py` |
| D-CP2-1 | 2 | Phase 2 checkpoint reports (5) | T02.06, T02.12, T02.18, T02.24, T02.29 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-2-cp*.md` |
| D-0050 | 3 | commands module (Click subcommands) | T03.01 | `src/superclaude/cli/swarm/commands.py` |
| D-0051 | 3 | dispatch module (Wave 1) | T03.02 | `src/superclaude/cli/swarm/dispatch.py` |
| D-0052 | 3 | state module | T03.03 | `src/superclaude/cli/swarm/state.py` |
| D-0053 | 3 | logging_ module (dual JSONL+md, lock-coordinated) | T03.04 | `src/superclaude/cli/swarm/logging_.py` |
| D-0054 | 3 | openai_compat transport (httpx) | T03.05 | `src/superclaude/cli/swarm/transports/openai_compat.py` |
| D-0055 | 3 | deterministic-fixture (stub) transport | T03.07 | `src/superclaude/cli/swarm/transports/stub.py` |
| D-0056 | 3 | swarm run subcommand | T03.08 | `src/superclaude/cli/swarm/commands.py::run_cmd` |
| D-0057 | 3 | Per-worker timeout + retry policy | T03.09 | `src/superclaude/cli/swarm/dispatch.py::retry_policy` |
| D-0058 | 3 | Dual-format log emission | T03.10 | `src/superclaude/cli/swarm/logging_.py` |
| D-0059 | 3 | IMM-3 true-parallel dispatch test (stub overlap) | T03.11 | `tests/swarm/test_imm3_parallel.py` |
| D-0060 | 3 | IMM-6 atomic-write test (mid-write kill) | T03.13 | `tests/swarm/test_imm6_atomic_write.py` |
| D-0061 | 3 | INV-002 Python-only dispatch test | T03.14 | `tests/swarm/test_concurrency_python_only.py` |
| D-0062 | 3 | ParallelExecutor integration assertion | T03.15 | `tests/swarm/test_parallel_executor_routing.py` |
| D-0063 | 3 | NFR-002 atomicity test (state + jsonl lock) | T03.16 | `tests/swarm/test_nfr002_atomicity.py` |
| D-0064 | 3 | NFR-013 output-dir confinement guard | T03.17 | `src/superclaude/cli/swarm/state.py::confine_path` |
| D-0065 | 3 | NFR-014 no-cache assertion | T03.19 | `tests/swarm/test_no_response_cache.py` |
| D-0066 | 3 | AC-010 no-Anthropic-endpoint guard | T03.20 | `tests/swarm/test_no_anthropic_routing.py` |
| D-0067 | 3 | T2 proxy env contract reader | T03.21 | `src/superclaude/cli/swarm/transports/openai_compat.py::read_env` |
| D-CP3-1 | 3 | Phase 3 checkpoint reports (5) | T03.06, T03.12, T03.18, T03.18a, T03.22 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-3-cp*.md` |
| D-0068 | 4 | normalize module (Wave 2) | T04.01 | `src/superclaude/cli/swarm/normalize.py` |
| D-0069 | 4 | Recipe Protocol + REGISTRY | T04.02 | `src/superclaude/cli/swarm/recipes/__init__.py` |
| D-0070 | 4 | bare_review_v1 recipe | T04.03 | `src/superclaude/cli/swarm/recipes/bare_review_v1.py` |
| D-0071 | 4 | findings_table_v1 recipe | T04.04 | `src/superclaude/cli/swarm/recipes/findings_table_v1.py` |
| D-0072 | 4 | hypothesis_table_v1 recipe | T04.05 | `src/superclaude/cli/swarm/recipes/hypothesis_table_v1.py` |
| D-0073 | 4 | verdict_only_v1 recipe | T04.07 | `src/superclaude/cli/swarm/recipes/verdict_only_v1.py` |
| D-0074 | 4 | passthrough recipe | T04.08 | `src/superclaude/cli/swarm/recipes/passthrough.py` |
| D-0075 | 4 | custom-py loader | T04.09 | `src/superclaude/cli/swarm/recipes/custom.py` |
| D-0076 | 4 | 6-recipe REGISTRY registration test | T04.10 | `tests/swarm/test_recipe_registry.py` |
| D-0077 | 4 | Parse-error salvage promotion | T04.11 | `src/superclaude/cli/swarm/normalize.py::salvage_parse_error` |
| D-0078 | 4 | bare-review output template | T04.12 | `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md` |
| D-0079 | 4 | Per-lens output templates (6 non-custom) | T04.13 | `src/superclaude/cli/swarm/lenses/templates/<lens>-output.md` |
| D-0080 | 4 | AC-011 recipe-no-judging boundary test | T04.14 | `tests/swarm/test_recipe_no_judging.py` |
| D-CP4-1 | 4 | Phase 4 checkpoint reports (3) | T04.06, T04.12a, T04.15 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-4-cp*.md` |
| D-0081 | 5 | reduce module (Wave 3) | T05.01 | `src/superclaude/cli/swarm/reduce.py` |
| D-0082 | 5 | merge module (≤30 LOC) | T05.02 | `src/superclaude/cli/swarm/merge.py` |
| D-0083 | 5 | IMM-5 status determination + parametrized test | T05.03 | `tests/swarm/test_imm5_status.py` |
| D-0084 | 5 | Three amalgamation modes dispatch | T05.04 | `src/superclaude/cli/swarm/reduce.py::select_mode` |
| D-0085 | 5 | Mechanical merge module (4 guards) | T05.05 | `src/superclaude/cli/swarm/merge.py` |
| D-0086 | 5 | Result contract emitter (`return-contract.yaml`) | T05.07 | `src/superclaude/cli/swarm/reduce.py::emit_contract` |
| D-0087 | 5 | merge.py ≤30 LOC CI assertion | T05.08 | `tests/swarm/test_merge_loc_ceiling.py` |
| D-0088 | 5 | Boundary enforcement test (3-worker concat) | T05.09 | `tests/swarm/test_merge_mechanical_only.py` |
| D-0089 | 5 | AC-012 no-scoring-engine guard | T05.10 | `tests/swarm/test_no_scoring_engine.py` |
| D-0090 | 5 | AC-011 merge-no-transforms boundary test (variant) | T05.11 | `tests/swarm/test_merge_no_transforms.py` |
| D-CP5-1 | 5 | Phase 5 checkpoint reports (3) | T05.06, T05.10a, T05.12 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-5-cp*.md` |
| D-0091 | 6 | INV-001 resume-from-manifest test | T06.01 | `tests/swarm/test_resume_uses_manifest_lens.py` |
| D-0092 | 6 | INV-010 merge regen on resume test | T06.02 | `tests/swarm/test_resume_regenerates_merge.py` |
| D-0093 | 6 | INV-016 manifest-immunity-to-mutation test | T06.03 | `tests/swarm/test_manifest_durable.py` |
| D-0094 | 6 | swarm run --resume implementation | T06.04 | `src/superclaude/cli/swarm/commands.py::resume_cmd` |
| D-0095 | 6 | Manifest emission at preflight | T06.05 | `src/superclaude/cli/swarm/preflight.py::emit_manifest` |
| D-0096 | 6 | --force-relens flag | T06.07 | `src/superclaude/cli/swarm/commands.py::resume_cmd` |
| D-0097 | 6 | Crash recovery semantics test (E2E) | T06.08 | `tests/swarm/test_crash_recovery_e2e.py` |
| D-0098 | 6 | Schema forward-compat (spec_version) test | T06.09 | `tests/swarm/test_schema_forward_compat.py` |
| D-CP6-1 | 6 | Phase 6 checkpoint reports (2) | T06.06, T06.10 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-6-cp*.md` |
| D-0099 | 7 | tui module (Rich Live, --tui gated) | T07.01 | `src/superclaude/cli/swarm/tui.py` |
| D-0100 | 7 | tmux detached-run wrapper | T07.02 | `src/superclaude/cli/swarm/tmux.py` |
| D-0101 | 7 | INV-012 TUI opt-in test (non-TTY plain output) | T07.03 | `tests/swarm/test_inv012_tui_opt_in.py` |
| D-0102 | 7 | swarm status subcommand | T07.04 | `src/superclaude/cli/swarm/commands.py::status_cmd` |
| D-0103 | 7 | swarm logs subcommand | T07.05 | `src/superclaude/cli/swarm/commands.py::logs_cmd` |
| D-0104 | 7 | swarm attach subcommand | T07.07 | `src/superclaude/cli/swarm/commands.py::attach_cmd` |
| D-0105 | 7 | swarm kill subcommand | T07.08 | `src/superclaude/cli/swarm/commands.py::kill_cmd` |
| D-0106 | 7 | swarm scaffold subcommand | T07.09 | `src/superclaude/cli/swarm/commands.py::scaffold_cmd` |
| D-0107 | 7 | Three monitoring patterns doc + demo | T07.10 | `docs/swarm/monitoring-patterns.md` |
| D-0108 | 7 | --detached flag + tmux wrap | T07.11 | `src/superclaude/cli/swarm/commands.py::run_cmd` |
| D-0109 | 7 | done.json sentinel emission | T07.13 | `src/superclaude/cli/swarm/reduce.py::emit_done_sentinel` |
| D-0110 | 7 | Three-layer observability artifact set | T07.14 | `src/superclaude/cli/swarm/` (state+logging_+done) |
| D-0111 | 7 | Contract surface non-precluding (grep audit) | T07.15 | `tests/swarm/test_contract_surface.py` |
| D-0112 | 7 | Rich-version pin doc | T07.16 | `pyproject.toml` (rich>=13.0.0) |
| D-0113 | 7 | tmux-optional doc + fallback | T07.17 | `docs/swarm/runbook.md` |
| D-0114 | 7 | No-external-framework dep audit | T07.19 | `tests/swarm/test_no_external_frameworks.py` |
| D-0115 | 7 | Phase-1 transport limits (no streaming/etc.) doc | T07.20 | `docs/swarm/transport-limits.md` |
| D-CP7-1 | 7 | Phase 7 checkpoint reports (4) | T07.06, T07.12, T07.18, T07.21 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-7-cp*.md` |
| D-0116 | 8 | SKILL.md thin caller (~60 LOC) | T08.01 | `src/superclaude/skills/sc-bare-review/SKILL.md` |
| D-0117 | 8 | Non-Claude caller test (subprocess) | T08.02 | `tests/swarm/test_non_claude_caller.py` |
| D-0118 | 8 | Test-coverage CI matrix (per-IMM, per-INV) | T08.03 | `tests/swarm/conftest.py`, `pytest.ini` |
| D-0119 | 8 | Source-first sync migration record | T08.04 | `docs/dev/migration-skill.md` |
| D-0120 | 8 | Package entry point registration | T08.05 | `pyproject.toml` (entry_points/console_scripts) |
| D-0121 | 8 | Legacy `scripts/*.sh` retirement PR | T08.07 | `src/superclaude/skills/sc-bare-review/scripts/` (deleted) |
| D-0122 | 8 | Release notes + operator migration note | T08.08 | `docs/swarm/release-notes-v1.md` |
| D-0123 | 8 | TEST-001 IMM acceptance suite | T08.09 | `tests/swarm/test_imm_suite.py` |
| D-0124 | 8 | TEST-002 INV remediation suite | T08.10 | `tests/swarm/test_inv_suite.py` |
| D-0125 | 8 | TEST-003 bare-review parity A/B | T08.11 | `tests/swarm/test_bare_review_parity.py` |
| D-0126 | 8 | TEST-004 bundled lens validation CI gate | T08.13 | `tests/swarm/test_validate_lenses_ci.py` |
| D-0127 | 8 | TEST-005 non-Claude caller integration test | T08.14 | `tests/swarm/test_subprocess_caller.py` |
| D-0128 | 8 | TEST-006 mechanical-merge boundary test | T08.15 | `tests/swarm/test_merge_mechanical_only.py` (final hardened) |
| D-0129 | 8 | TEST-007 resume crash-recovery E2E | T08.16 | `tests/swarm/test_resume_crash_recovery.py` |
| D-0130 | 8 | TEST-008 fixture transport wired into integration suite | T08.17 | `tests/swarm/integration/conftest.py` |
| D-CP8-1 | 8 | Phase 8 checkpoint reports (4) | T08.06, T08.12, T08.15a, T08.18 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-8-cp*.md` |
| D-0131 | 9 | OPS-001 operator runbook | T09.01 | `docs/swarm/operator-runbook.md` |
| D-0132 | 9 | OPS-002 env readiness check + script | T09.02 | `scripts/swarm_env_readiness.sh`, `docs/swarm/env-readiness.md` |
| D-0133 | 9 | OPS-003 observability procedure | T09.03 | `docs/swarm/observability-procedure.md` |
| D-0134 | 9 | OPS-004 rollback procedure (rehearsed) | T09.05 | `docs/swarm/rollback-procedure.md` |
| D-0135 | 9 | OPS-005 lens contribution policy | T09.06 | `docs/swarm/lens-contribution-policy.md` |
| D-0136 | 9 | OPS-006 post-release metrics review framework | T09.07 | `docs/swarm/post-release-metrics.md` |
| D-CP9-1 | 9 | Phase 9 checkpoint reports (2) | T09.04, T09.08 | `.dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-9-cp*.md` |

## Traceability Matrix

| Spec/Invariant Anchor | Roadmap IDs | Task IDs | Deliverables |
|---|---|---|---|
| IMM-3 (true-parallel dispatch) | IMM-3, AC-004, NFR-001 | T03.11, T03.15, T08.09 | D-0059, D-0062, D-0123 |
| IMM-4 (empty-target guard) | IMM-4 | T02.13, T08.09 | D-0036, D-0123 |
| IMM-5 (success-first status) | IMM-5, DM-008 | T05.03, T08.09 | D-0083, D-0123 |
| IMM-6 (atomic-write idempotency) | IMM-6, NFR-002, FR-027 | T03.13, T03.16, T07.13, T08.09 | D-0060, D-0063, D-0109, D-0123 |
| §11.5 (prompt-injection guard) | §11.5, INV-003, INV-014, NFR-003, FR-019, FR-024 | T02.03, T02.07, T02.08, T02.09, T02.22, T02.26, T08.09 | D-0028, D-0031, D-0032, D-0033, D-0044, D-0047, D-0123 |
| INV-001 (resume from manifest) | INV-001, INV-016, FR-015, FR-025 | T06.01, T06.03, T06.04, T06.07, T08.10 | D-0091, D-0093, D-0094, D-0096, D-0124 |
| INV-002 (Python-only concurrency) | INV-002 | T03.14, T08.10 | D-0061, D-0124 |
| INV-005 (worker-vs-pool guard) | INV-005 | T02.10, T08.10 | D-0034, D-0124 |
| INV-007 (empty-pool failure) | INV-007 | T02.11, T08.10 | D-0035, D-0124 |
| INV-010 (resume merge regen) | INV-010 | T06.02, T08.10, T08.16 | D-0092, D-0124, D-0129 |
| INV-012 (TUI opt-in) | INV-012 | T07.03 | D-0101 |
| §8.3 (merge boundary, 4 guards) | FR-012, NFR-008, NFR-009, AC-011, AC-012, AC-018 | T05.02, T05.05, T05.08, T05.09, T05.10, T05.11, T08.15 | D-0082, D-0085, D-0087, D-0088, D-0089, D-0090, D-0128 |
| §1.4 (caller agnosticism) | AC-013, NFR-016, FR-030 | T02.28, T07.15, T08.02, T08.14 | D-0049, D-0111, D-0117, D-0127 |
| §7.4 (parse-error salvage) | FR-028 | T04.11 | D-0077 |
| §6.4 (lens registry) | FR-009, U-008, FR-LENSREG.NS | T02.16, T02.17, T02.21, T08.13 | D-0039, D-0040, D-0043, D-0126 |
| §13 (skill migration) | FR-029, MIG-001..004, TEST-003 | T08.01, T08.04, T08.05, T08.07, T08.08, T08.11 | D-0116, D-0119, D-0120, D-0121, D-0122, D-0125 |
| §10 (observability) | NFR-004, FR-026, FR-013, FR-027 | T03.10, T07.10, T07.13, T07.14 | D-0058, D-0107, D-0109, D-0110 |
| §6 (schema + cross-field) | FR-019, NFR-006 | T02.03, T06.09 | D-0028, D-0098 |
| §7 (transport + retry) | FR-017, FR-022, FR-023, NFR-010, NFR-011, AC-005 | T03.05, T03.07, T03.09 | D-0054, D-0055, D-0057 |
| §8 (amalgamation modes) | FR-011 | T05.04 | D-0084 |

## Execution Log Template

```yaml
# .dev/releases/Current/MultiModelSwarm/tasklist/execution-log.yaml
log_format: v1
tasks:
  - id: T01.01
    started: <ISO-8601>
    finished: <ISO-8601>
    status: pending|in_progress|done|blocked
    deliverables: [D-0001]
    notes: ""
```

## Checkpoint Report Template

```yaml
# .dev/releases/Current/MultiModelSwarm/tasklist/checkpoints/phase-<N>-cp<M>.md
checkpoint_id: P<N>-CP<M>
phase: <N>
covers_tasks: [T<NN>.<TT>, ...]
artifacts_verified: []
status: pass|fail|warn
findings: []
next_action: ""
```

## Feedback Collection Template

```yaml
# .dev/releases/Current/MultiModelSwarm/tasklist/feedback/<id>.md
feedback_id: FB-001
source: human|tool|agent
target: T<NN>.<TT> | phase-<N> | bundle
category: gap|defect|enhancement|clarification
severity: low|med|high|critical
description: ""
proposed_action: ""
```
