---
total_diff_points: 12
shared_assumptions_count: 14
---

# Shared Assumptions and Agreements

Both variants converge on a security-first, foundation-before-execution architecture with strong consensus on core design decisions:

1. **Complexity classification**: HIGH (0.72), architect persona, Linux-only v1, local-only scope
2. **Critical path ordering**: Loader/schema/security guards → isolation → PTY runner → orchestration → reporter → eval bodies
3. **Concurrency primitive**: `ThreadPoolExecutor + as_completed`, default 8 workers, max 15 (clamped)
4. **Isolation strategy**: Extend (not replace) existing `IsolationLayers`; add HOME, session_id, time-offset layers
5. **Security boundary**: Defense-in-depth — eval_id regex validation BEFORE filesystem writes, re-validated inside HomeIsolation
6. **Reporter contract**: `len(outcomes) == counts.expanded_n_prime`; mismatch raises `ReporterContractViolation` with exit 2
7. **Dependency discipline**: Vendor ptytest under `cli/eval/pty/`; pin pexpect>=4.9; zero new external Python deps
8. **Capability tiers**: HARD / SOFT-SKIP / SOFT-XFAIL with `--no-mcp` escape hatch
9. **Retry policy**: No default retry; deterministic single-pass; MCP retry-once gated on OQ-10
10. **Artifact layout**: `.dev/eval-runs/<ISO>/<run-id>/` with summary.{md,json}, optional junit.xml, per-eval transcripts
11. **Hook matcher coverage gate**: v1 covers `mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*`
12. **CLI surface**: `superclaude eval` Click group with run/list/describe/doctor subcommands
13. **Disk budget**: `--max-disk-mb 1024` default, 5s polling, exit 2 on breach
14. **Source-of-truth**: Edits in `src/superclaude/` → `make sync-dev` → `.claude/`; `make verify-sync` as CI gate

# Numbered Divergence Points

## 1. Milestone count and granularity
- **Opus**: 6 milestones (M1 Foundation, M2 Isolation/Process, M3 Execution/Reporter, M4 DSL/CLI, M5 Evals/Coverage, M6 Hardening) — 28 working days
- **Haiku**: 5 milestones (M1 Decisions/Schema/CLI, M2 Isolation/Capability, M3 PTY/Orchestration, M4 Reporting/Sync, M5 Suite/Release) — 6 weeks
- **Impact**: Opus separates ExpectDSL+CLI (M4) from Reporter (M3) and gives docs/hardening its own milestone (M6); Haiku folds CLI contract into M1 and merges hardening into M5. Opus offers finer review checkpoints; Haiku reduces transition overhead.

## 2. CLI contract placement
- **Opus**: CLI Click group + all flags land in M4, AFTER reporter/orchestrator exist
- **Haiku**: CLI surface (FR-CLI1-4, COMP-001) lands in M1 as foundation contract
- **Impact**: Haiku front-loads the public contract for early review/sign-off; Opus defers CLI until backing components are real, avoiding stub-flag drift. Haiku's approach risks flag churn if reporter/runner reveal contract gaps; Opus's risks late discovery of CLI usability issues.

## 3. Expect DSL milestone placement
- **Opus**: ExpectDSL primitives land in M4 alongside CLI, AFTER runner/reporter
- **Haiku**: ExpectDSL interface (COMP-010) lands in M1 as foundation; primitives in M3
- **Impact**: Haiku enables manifest authoring earlier; Opus waits until EvalContext/EvalRunner are concrete, reducing rework on assertion shape.

## 4. Number of P0 deliverables
- **Opus**: 99 deliverables across 6 milestones
- **Haiku**: 80 deliverables across 5 milestones
- **Impact**: Opus enumerates each Expect primitive (COMP-010.1-6) and each eval (E1, E2.1-3, E3-E15) as separate deliverables; Haiku batches Expect primitives into FR-EXP1 and groups evals into TEST-010/011/012/015. Opus offers stricter tracking granularity; Haiku reduces ledger overhead.

## 5. Open question resolution sequencing
- **Opus**: Distributes OQ resolutions per-milestone (OQ-1/2/7 → M1, OQ-3/8 → M2, OQ-5 → M4, OQ-10 → M5)
- **Haiku**: Concentrates 6 OQ items (OQ-1, OQ-3, OQ-4, OQ-7, OQ-8, OQ-10) as M1 entry blockers
- **Impact**: Haiku enforces decisive early closure but risks blocking M1 start; Opus permits parallel resolution alongside implementation but risks contract churn mid-milestone.

## 6. NOTICE/license handling timing
- **Opus**: OQ-4-res scheduled in M6 hardening
- **Haiku**: OQ-4 listed as M1 entry blocker (gates ptytest vendoring in M2)
- **Impact**: Haiku correctly identifies license attribution as a precondition to vendoring code; Opus's deferral to M6 risks vendored ptytest sitting in M2 without complete attribution. **Haiku stronger here.**

## 7. Effort sizing semantics
- **Opus**: Uses S/M/L/XL with explicit duration mapping (4-7 day milestones)
- **Haiku**: Uses S/M/L/XL with weekly granularity (1-2 week milestones)
- **Impact**: Opus's day-level scheduling supports tighter project tracking; Haiku's week-level abstraction is more honest about estimation uncertainty.

## 8. Decision summary depth
- **Opus**: 8 decisions covering subprocess model, parallelism, isolation, ptytest, reporter, capability tiers, retry, output sink
- **Haiku**: 8 decisions covering execution, concurrency, isolation, validation order, reporter, scope, MCP behavior, dependency
- **Impact**: Opus emphasizes implementation primitive choices (output sink path, retry semantics); Haiku emphasizes contract-shaping choices (validation order, scope boundary). Complementary framings.

## 9. Risk register structure
- **Opus**: 9 risks (R1-R9) with cross-milestone risk IDs reused per-milestone
- **Haiku**: 15 risks (RR-001 to RR-015) one-per-discovery with no consolidation
- **Impact**: Opus consolidates duplicate risks (R3 MCP flakiness appears once); Haiku double-lists similar risks (RR-008 RAM/disk, RR-011 disk alone). Opus more maintainable; Haiku more granular tracing.

## 10. Validation infrastructure
- **Opus**: Implicit test references inside AC fields per deliverable
- **Haiku**: Explicit TEST-001 through TEST-016 as standalone deliverables with milestone placement
- **Impact**: Haiku surfaces test coverage as first-class trackable artifacts; Opus embeds them in deliverable AC. **Haiku stronger for QA audit trail.**

## 11. SuiteLoader effort estimate
- **Opus**: COMP-002 = Large effort
- **Haiku**: COMP-002 = Medium effort
- **Impact**: Opus accounts for schema+regex+capability orchestration overhead; Haiku assumes the orchestration cost is bounded once schema and regex are in place.

## 12. Timeline anchor
- **Opus**: 28 working days (~5.5 calendar weeks single-engineer)
- **Haiku**: 6 calendar weeks (M5 spans 2 weeks for eval authoring)
- **Impact**: Opus assumes evals can be authored in 7 days (Day 20-26); Haiku allocates a full 2 weeks for E1-E15. Haiku's allocation is more realistic given OQ-2 (eval bodies undefined) and per-eval hook coverage assertions. **Haiku stronger.**

# Areas Where One Variant Is Clearly Stronger

**Opus stronger:**
- **Milestone granularity** (D1): 6-milestone breakdown isolates Reporter contract enforcement (M3) from CLI surface (M4), enabling earlier reporter contract validation independent of CLI flag churn
- **Deliverable enumeration** (D4): Each Expect primitive and each eval body tracked separately; provides clearer per-batch DoD
- **Risk consolidation** (D9): R1-R9 with cross-milestone reuse avoids inflation; cleaner project status surface
- **Schema-loader effort sizing** (D11): L for COMP-002 better reflects coupled validation responsibilities
- **Dependency graph specificity**: Explicit intra-milestone ordering (e.g., "Within M2: HomeIsolation → path-containment → PtyDriver → PtyStream") aids implementer sequencing

**Haiku stronger:**
- **License precondition** (D6): Correctly gates ptytest vendoring on NOTICE/LICENSE resolution; Opus defers to M6 hardening creating ordering hazard
- **Test deliverable surfacing** (D10): TEST-001..016 as enumerable artifacts improves QA auditability
- **Decision concentration in M1** (D5): Treating all blocking OQs as M1 entry criteria reduces mid-milestone contract churn
- **Realistic eval-authoring window** (D12): 2-week M5 better matches uncertainty in OQ-2 (E3-E15 bodies TBD)
- **CLI contract early** (D2): Establishes public surface in M1 for stakeholder review before implementation cost

# Areas Requiring Debate to Resolve

1. **CLI placement (M1 vs M4)**: Trade-off between early stakeholder sign-off (Haiku) vs avoiding stub-flag drift (Opus). Resolution depends on whether OQ-7 (--junit) and OQ-3 (--no-pty exclusion set) can be closed before M1 starts.

2. **License/NOTICE timing**: Haiku's M1-block approach is technically correct but may delay M1 entry if OQ-4 ownership is unclear. Opus's M6 placement creates audit risk. **Recommend: Adopt Haiku's M1 gating but allow parallel resolution thread.**

3. **Milestone count (5 vs 6)**: Opus's docs/hardening as standalone M6 provides explicit sign-off checkpoint but adds transition overhead. Haiku folds hardening into M5 release validation, risking exit criteria conflation. Resolution depends on whether maintainer wants distinct "harness ready" vs "release ready" gates.

4. **OQ resolution timing**: Whether contract-shaping OQs (OQ-1, OQ-7, OQ-8) must be closed before M1 entry (Haiku) or can resolve in parallel (Opus). Resolution depends on maintainer availability and risk tolerance for late-discovered contract changes.

5. **Test deliverable enumeration**: Whether tests should be first-class deliverables (Haiku TEST-001..016) or embedded in feature AC (Opus implicit). Resolution depends on whether QA tracking system is roadmap-driven or PR-driven.

6. **Expect DSL granularity**: Whether each primitive (file, jsonl, settings_json, exit_code, stderr, stdout, duration) deserves its own deliverable line (Opus) or batches under FR-EXP1 (Haiku). Resolution depends on whether per-primitive testing is checkpointed separately.

7. **Eval body authoring duration**: 7-day allocation (Opus) vs 14-day allocation (Haiku). Resolution depends on OQ-2 resolution and depth of E3-E15 specification at M5 entry.
