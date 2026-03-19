---
total_diff_points: 12
shared_assumptions_count: 14
---

## 1. Shared Assumptions and Agreements

Both variants agree on the following foundational points:

1. **Three detection classes**: Unwired optional callable injections, orphan provider modules, broken dispatch registries
2. **Zero pipeline substrate modifications**: All new code consumes existing contracts (`GateCriteria`, `SemanticCheck`, `Step`, `GateMode`)
3. **Deterministic AST-only analysis**: No LLM, no subprocesses
4. **Three-phase rollout**: Shadow → soft → full enforcement with statistical gates between phases
5. **Same core dataclasses**: `WiringFinding`, `WiringReport`, `WiringConfig`
6. **Same gate definition**: `WIRING_GATE` with 5 semantic checks and 17 frontmatter fields
7. **Same rollout thresholds**: FPR <15% for soft, <5% for full; TPR >50%/80%; whitelist stable 5+ sprints
8. **Same performance targets**: <5s for 50 files; 90% coverage on core modules; 20+ unit / 3+ integration tests
9. **Additive-only agent extensions**: No new agent types, no removal of existing rules (NFR-013)
10. **Same internal/external dependency set**: Identical files to modify and consume
11. **ToolOrchestrator plugin has explicit cut criteria**: Defer to v2.1 if late
12. **Merge coordination required**: `roadmap/gates.py` shared modification point needs sequencing
13. **Same open questions**: `audit_artifacts_used`, `files_skipped`, whitelist strictness, `SprintConfig.source_dir`
14. **v2.1 alias pre-pass**: Both defer import alias/re-export handling as a future enhancement

---

## 2. Divergence Points

### D1 — Phase 0: Explicit Architecture Alignment Phase

- **Opus**: Jumps directly into Phase 1 (Core Engine). Open questions listed in Section 7 as blockers but no dedicated resolution phase.
- **Haiku**: Introduces Phase 0 (0.5–1 day) to resolve all spec ambiguities, lock architectural rules, and define phase-exit criteria before any code.
- **Impact**: Haiku's approach reduces rework risk by front-loading decisions. Opus's approach saves calendar time if open questions are resolved informally. For a project with 5+ unresolved questions, Phase 0 is likely the safer choice.

### D2 — ToolOrchestrator Plugin Sequencing

- **Opus**: Places ToolOrchestrator plugin as Phase 5 (late, Sprint 4, conditional). Treats it as an enhancement after pipeline integration.
- **Haiku**: Places it as Phase 2 (early, right after core engine). Argues it's a "leverage point" that improves reuse and reduces duplicated scanning.
- **Impact**: Early placement (Haiku) means the plugin informs the report and gate phases, potentially improving quality. Late placement (Opus) de-risks the critical path by ensuring core gate functionality ships first regardless of plugin status. This is the most consequential structural disagreement.

### D3 — Sprint and Roadmap Integration: Bundled vs. Separated

- **Opus**: Phase 3 bundles roadmap pipeline integration AND sprint hook into a single phase.
- **Haiku**: Separates them into Phase 4 (roadmap) and Phase 5 (sprint), treating sprint as operationally sensitive enough to warrant its own phase.
- **Impact**: Haiku's separation allows independent validation of each integration surface. Opus's bundling is more efficient if both are straightforward. Given that sprint affects developer workflow directly, separation is arguably safer.

### D4 — Validation and Testing: Distributed vs. Consolidated

- **Opus**: Tests are written within each phase (Phase 1 includes 200–250 LOC of tests; Phase 2 includes 100–130 LOC).
- **Haiku**: Includes per-phase tests but also adds a dedicated Phase 7 (Validation, Benchmarking, Rollout Readiness) for consolidated validation, benchmark runs, and retrospective analysis.
- **Impact**: Opus catches issues earlier with in-phase testing. Haiku provides a formal validation gate before shadow deployment. Best practice: both — write tests per phase AND have a final validation sweep. The consolidated phase also covers cross-cutting concerns like retrospective known-bug detection.

### D5 — Rollout as Separate Phase

- **Opus**: Phase 6 combines shadow calibration with soft/full activation in a single phase.
- **Haiku**: Splits into Phase 7 (readiness assessment) and Phase 8 (actual rollout progression), with explicit activation gates at each transition.
- **Impact**: Haiku's two-phase rollout provides clearer decision points. The separation between "are we ready?" and "activate it" reduces the risk of premature activation.

### D6 — LOC Estimates and Task Granularity

- **Opus**: Provides detailed LOC estimates per task (e.g., "60-80 LOC", "80-100 LOC") and maps specific requirement IDs to tasks.
- **Haiku**: Uses narrative descriptions without LOC estimates. Groups work by concern rather than by file.
- **Impact**: Opus is more actionable for sprint planning and progress tracking. Haiku is more readable for architectural review. For tasklist generation, Opus's format is directly convertible.

### D7 — Total Phase Count

- **Opus**: 6 phases (Phases 1–6)
- **Haiku**: 9 phases (Phases 0–8)
- **Impact**: Haiku's finer granularity provides more checkpoints but increases coordination overhead. Opus's fewer phases move faster but have larger blast radius per phase.

### D8 — Resource Requirements: Roles vs. Files

- **Opus**: Focuses on files (new files, modified files, external dependencies) without naming engineering roles.
- **Haiku**: Explicitly defines 4 engineering roles (architect, backend engineer, QA, audit workflow owner) and assigns accountability areas.
- **Impact**: Haiku's role definitions are valuable for team coordination. Opus assumes a single implementer or doesn't prescribe team structure.

### D9 — Performance Target in Phase 1

- **Opus**: Sets an aggressive Phase 1 checkpoint of "<2s for 50-file fixture" (NFR-001), with <5s as the hard budget.
- **Haiku**: Uses only the <5s target throughout, without an intermediate tighter target.
- **Impact**: Opus's tighter early target catches performance issues before integration adds overhead. Haiku relies on the final benchmark phase to validate performance.

### D10 — Open Questions Treatment

- **Opus**: Lists 5 open questions in a dedicated Section 7, with proposed answers and phase-blocking annotations.
- **Haiku**: Embeds the same questions into Phase 0 actions without proposed resolutions, plus adds 2 additional items (comparator/consolidator scope, rollout ownership for `grace_period`).
- **Impact**: Opus's proposed answers accelerate decision-making. Haiku's broader question set is more thorough. Best approach: combine both — Haiku's question scope with Opus's proposed defaults.

### D11 — Architectural Priorities Section

- **Opus**: No dedicated architectural priorities section; constraints are embedded in the executive summary.
- **Haiku**: Includes a "Recommended architectural priorities" section with 5 explicit principles (correctness over breadth, protect dependency boundaries, rollout as architecture, design for auditability, explicit deferral).
- **Impact**: Haiku's explicit priorities serve as a decision framework for edge cases during implementation.

### D12 — Risk Assessment: Additional Detail on R7

- **Opus**: Treats R7 (agent regression) as MEDIUM with one-line mitigation.
- **Haiku**: Elevates R7 to HIGH priority, adds staged independent validation of scanner/analyzer/validator, and regression tests against prior audit outputs.
- **Impact**: Given that audit agents are behavioral specs read by LLMs, Haiku's caution is warranted — regressions in agent behavior are harder to detect than code regressions.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Task-level granularity**: File paths, LOC estimates, requirement traceability per task — directly usable for tasklist generation
- **Concreteness**: Named functions (`run_wiring_analysis()`, `_extract_frontmatter_values()`), specific file locations, exact line counts
- **Sprint mapping**: Tasks explicitly mapped to Sprints 1–5
- **Proposed answers to open questions**: Provides default resolutions instead of just listing questions
- **Parallelization annotation**: Explicitly marks Phase 4 as parallelizable with Phase 3

### Haiku is stronger in:
- **Process discipline**: Phase 0 decision closure, Phase 7 consolidated validation, Phase 8 rollout progression
- **Architectural reasoning**: Explains *why* decisions are made, not just what to do
- **Role accountability**: Defines who owns what
- **Risk elevation**: More conservative on agent regression risk (R7 as HIGH)
- **Decision framework**: Explicit architectural priorities section for edge-case guidance
- **ToolOrchestrator leverage argument**: Makes the case for early integration clearly

---

## 4. Areas Requiring Debate to Resolve

1. **ToolOrchestrator plugin timing (D2)**: This is the highest-impact structural disagreement. Early (Haiku) risks blocking the critical path if the plugin is complex. Late (Opus) risks building the report/gate phases without the reuse benefits. **Resolution approach**: Timeboxed spike — if plugin can be built in 1 day, do it early; if not, defer.

2. **Phase 0 necessity (D1)**: Is a formal decision-closure phase worth 0.5–1 day, or can open questions be resolved as implementation proceeds? **Resolution approach**: If all 5+ open questions have proposed answers (Opus provides these), Phase 0 can be compressed to a review meeting rather than a full phase.

3. **Sprint/roadmap bundling (D3)**: Should pipeline and sprint integration share a phase? **Resolution approach**: If the same engineer does both and sprint hook is <40 LOC, bundling is fine. If different owners or sprint has operational sensitivity, separate.

4. **Consolidated validation phase (D4/D5)**: Is Phase 7 redundant if tests are written per phase? **Resolution approach**: The retrospective validation (cli-portify known bug, noise characterization) is genuinely new work not covered by per-phase tests. A lightweight validation phase (1 day) is justified; 2–3 days may be excessive.

5. **Agent regression risk level (D12)**: MEDIUM (Opus) vs. HIGH (Haiku). **Resolution approach**: Check how many downstream consumers depend on current agent specs. If cleanup-audit is actively used in production workflows, HIGH is appropriate.
