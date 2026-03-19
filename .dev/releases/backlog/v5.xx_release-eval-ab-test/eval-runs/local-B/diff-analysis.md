---
total_diff_points: 12
shared_assumptions_count: 14
---

# Diff Analysis: Opus Architect vs Haiku Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Complexity rating**: Both assign 0.45 (MEDIUM).
2. **Single new file**: Both isolate progress logic in `src/superclaude/cli/roadmap/progress.py`.
3. **Atomic write strategy**: Both specify `tempfile` + `os.replace()`.
4. **No new third-party deps**: Both rely exclusively on Python stdlib.
5. **No observer/thread patterns**: Both reject background writers or async flush.
6. **Sequential callback guarantee**: Both depend on `on_step_complete` sequential invocation as the corruption guard.
7. **`StepProgress` required fields**: Both agree on 5 fields (`step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`).
8. **`summary()` additive-only**: Both mandate no changes to existing `GateCriteria` signatures.
9. **OQ-001/OQ-002 are blockers**: Both flag deviation schema and "significant findings" threshold as blocking.
10. **CLI validation fail-fast**: Both require parent directory existence check before pipeline starts.
11. **Default path**: Both agree on `{output_dir}/progress.json`.
12. **Overwrite-on-exists**: Both specify overwrite (not append) for fresh runs.
13. **50ms write latency target**: Both cite the same NFR benchmark.
14. **Eval-style tests**: Both reject mock-only unit tests in favor of real CLI invocation.

## 2. Divergence Points

### D-01: Phase 0 — Explicit Spec Closure Phase
- **Opus**: No Phase 0. Treats OQ resolution as a prerequisite annotation on Phase 2/4 boundaries.
- **Haiku**: Adds a dedicated **Phase 0** (0.5 day) for specification closure, schema freezing, and acceptance checklist mapping.
- **Impact**: Haiku's approach is more disciplined — it forces explicit sign-off before code starts. Opus risks starting code with unresolved ambiguities and discovering blockers mid-implementation.

### D-02: Phase Count and Structure
- **Opus**: 5 phases (Foundation → Integration → Gate Summary → Advanced Reporting → Performance).
- **Haiku**: 6 phases (Spec Closure → Foundation → Integration → CLI/Dry-Run → Validation → Release Readiness).
- **Impact**: Haiku adds bookend phases (spec closure + release readiness). Opus folds these into implicit prerequisites and post-conditions.

### D-03: Where Advanced Reporting Lives
- **Opus**: Dedicated **Phase 4** for convergence, remediation, and wiring reporting — separated from pipeline integration.
- **Haiku**: Bundles convergence, remediation, and wiring reporting **into Phase 2** (Pipeline Integration).
- **Impact**: Opus's separation is cleaner for incremental delivery and isolates risk from ambiguity-dependent work. Haiku's bundling is more compact but makes Phase 2 significantly larger and harder to gate.

### D-04: Parallelization Opportunity
- **Opus**: Explicitly identifies Phase 3 (Gate Summary) as parallelizable with Phase 2 — they share no code dependencies.
- **Haiku**: Sequences Phase 3 after Phase 2 with no parallelization call-out.
- **Impact**: Opus enables faster delivery through parallel work streams. Haiku's sequencing is conservative but leaves time on the table.

### D-05: Timeline Estimates
- **Opus**: No total estimate; phases labeled "Small" or "Medium" qualitatively.
- **Haiku**: Concrete day estimates totaling **5.5 engineering days**.
- **Impact**: Haiku gives stakeholders a plannable commitment. Opus provides relative sizing but no calendar mapping.

### D-06: Release Readiness Phase
- **Opus**: No explicit release phase. Validation in Phase 5 is the terminal step.
- **Haiku**: Dedicated **Phase 5** for regression checks, sync workflow, release notes, and representative validation runs.
- **Impact**: Haiku is more operationally complete — it accounts for the "last mile" work that often derails releases.

### D-07: Resume Behavior Treatment
- **Opus**: Lists OQ-004 (resume contradiction) as non-blocking with a recommended default: `--resume` appends, fresh run overwrites.
- **Haiku**: Elevates resume semantics to **Risk 5** (Medium severity) and requires explicit rule establishment in Phase 0.
- **Impact**: Haiku treats this more seriously. Opus's "defer" approach could produce inconsistent behavior if resume is used before the question is resolved.

### D-08: `StepResult` Import Path
- **Opus**: Explicitly flags that `StepResult` lives in `cli/pipeline/models.py`, not `cli/roadmap/models.py`, and calls out the extraction document's misleading dependency entry.
- **Haiku**: References `cli/roadmap/models.py` for `StepResult` compatibility without noting the discrepancy.
- **Impact**: Opus catches a potential integration error that Haiku misses. This is a concrete correctness advantage.

### D-09: Risk Count and Granularity
- **Opus**: 5 risks including the implicit `StepResult` import risk.
- **Haiku**: 5 risks, adding resume semantics conflict (Risk 5) that Opus omits as a risk.
- **Impact**: Complementary coverage. Opus has better technical risk identification; Haiku has better process risk identification.

### D-10: Resource/Staffing Model
- **Opus**: No staffing model. Implicitly single-engineer.
- **Haiku**: Explicitly calls for 3 roles: primary engineer, QA/validation support, architect/reviewer.
- **Impact**: Haiku is more realistic about what's needed for evidence-backed validation at the level both roadmaps describe.

### D-11: Task Granularity
- **Opus**: Fine-grained numbered tasks (1.1–5.3) with explicit requirement traceability per task.
- **Haiku**: Prose-style work descriptions without per-task requirement mapping.
- **Impact**: Opus is more traceable and sprint-ready. Haiku requires a tasklist generation step to become actionable.

### D-12: Dry-Run Table Renderer Location
- **Opus**: Notes uncertainty: "executor.py or commands.py" for the renderer.
- **Haiku**: Does not specify the exact file for the renderer.
- **Impact**: Minor. Neither commits to a location, but Opus at least acknowledges the decision is open.

## 3. Areas Where One Variant is Clearly Stronger

### Opus is stronger in:
- **Requirement traceability**: Every task maps to specific FR/NFR/SC identifiers.
- **Task decomposition**: Numbered, sprint-ready tasks vs prose descriptions.
- **Technical precision**: Catches the `StepResult` import path issue, identifies exact line numbers in `executor.py` (~1325, ~1535).
- **Parallelization**: Explicitly identifies the Phase 2/3 parallel opportunity.
- **Open question taxonomy**: More complete (6 OQs vs Haiku's implicit 3).

### Haiku is stronger in:
- **Process discipline**: Phase 0 spec closure prevents premature coding.
- **Release completeness**: Phase 5 covers sync, regression, and release notes.
- **Staffing realism**: Names 3 distinct roles needed.
- **Timeline concreteness**: Day-level estimates that stakeholders can plan against.
- **Resume risk elevation**: Treats a real ambiguity as a named risk rather than deferring it.

## 4. Areas Requiring Debate to Resolve

1. **Should advanced reporting (convergence/remediation/wiring) be a separate phase or bundled into pipeline integration?** Opus's separation is cleaner for gating; Haiku's bundling reduces phase count. The answer depends on whether OQ-001/OQ-002 can be resolved before integration starts.

2. **Is a formal Phase 0 worth the overhead?** If the team already has a spec review process, Haiku's Phase 0 is redundant ceremony. If not, it prevents costly mid-implementation pivots.

3. **Should resume behavior be resolved now or deferred?** Opus defers; Haiku blocks on it. The right answer depends on whether `--resume` is in scope for this release.

4. **Day estimates vs qualitative sizing**: Opus avoids committing to days (less risky for the estimator, less useful for the planner). A hybrid approach — Opus's task structure with Haiku's day estimates — would serve both audiences.
