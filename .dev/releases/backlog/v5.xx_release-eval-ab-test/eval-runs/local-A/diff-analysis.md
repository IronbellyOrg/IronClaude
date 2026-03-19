---
total_diff_points: 12
shared_assumptions_count: 14
---

# Diff Analysis: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Complexity rating**: Both assign 0.45 (MEDIUM)
2. **Single new module**: `progress.py` as the sole new file
3. **Atomic writes**: `os.replace()` for crash safety
4. **Callback-based architecture**: No threads, no file watchers, no observer pattern
5. **Sequential callback invocation**: Even for parallel steps — no concurrent writes
6. **Dependency direction**: `progress.py` depends on `models.py`/`gates.py`, never reverse
7. **`--progress-file` CLI option**: `click.Path`, default `{output_dir}/progress.json`
8. **No new third-party deps**: Python stdlib only (`json`, `os`, `tempfile`, `dataclasses`)
9. **NFR-003 compliance**: Zero import-time side effects
10. **`summary()` on `GateCriteria`**: Purely additive, no existing interface changes
11. **Performance target**: < 50ms per-step write overhead
12. **OQ-001 and OQ-004 as blockers**: Both identify these as pre-implementation decisions
13. **In-memory aggregation + atomic replace**: Not incremental append
14. **Same integration surface**: `executor.py`, `commands.py`, `gates.py`, `convergence.py`, `wiring_gate.py`

## 2. Divergence Points

### D-01: Phase Structure — 6 phases (both) but different decomposition

- **Opus**: Phases are implementation-centric: Foundation → CLI → Gates → Metadata → Convergence → Validation
- **Haiku**: Phases front-load design: Requirements Closure → Architecture Design → Core Implementation → Special Cases → Validation → Release Readiness
- **Impact**: Haiku's Phase 1 (requirements closure) forces OQ resolution before any code. Opus defers OQs to the phases where they block, risking late discovery if resolution stalls.

### D-02: Explicit Requirements Closure Phase

- **Opus**: No dedicated requirements phase; OQs are noted inline as blockers per-phase
- **Haiku**: Dedicates Phase 1 entirely to resolving all open questions and freezing the implementation contract
- **Impact**: Haiku reduces rework risk but adds 0.5–1 day before any code is written. Opus allows parallel progress on non-blocked phases.

### D-03: Explicit Architecture/Design Phase

- **Opus**: Jumps directly to implementation (Phase 1 = data models + writer code)
- **Haiku**: Phase 2 is a design-only phase — schema finalization, architectural decisions documented before code
- **Impact**: Haiku provides a reviewable design artifact; Opus moves faster but relies on implicit design-in-code.

### D-04: Release Readiness Phase

- **Opus**: No explicit release phase; ends at validation
- **Haiku**: Phase 6 covers `make sync-dev`, `make verify-sync`, regression suite, artifact review
- **Impact**: Haiku accounts for the project's sync discipline (`src/` → `.claude/`). Opus omits this, which could cause a sync gap at merge time.

### D-05: Timeline Estimates

- **Opus**: 6–10 working days
- **Haiku**: 4.5–7.5 working days
- **Impact**: ~1.5–2.5 day delta. Haiku is more aggressive. The difference largely comes from Opus allocating more buffer to Phase 4 (special-step metadata) and Phase 6 (validation).

### D-06: Gate Summary + Dry-Run Placement

- **Opus**: Standalone Phase 3, parallelizable with Phase 2
- **Haiku**: Bundled into Phase 4 alongside all special-case work
- **Impact**: Opus enables earlier dry-run validation as a parallel workstream. Haiku treats it as contract work co-located with the features it describes, ensuring consistency.

### D-07: Convergence Sub-Reporting Isolation

- **Opus**: Dedicated Phase 5 solely for convergence sub-reporting, with explicit OQ-001 prerequisite
- **Haiku**: Rolled into Phase 4 alongside remediation, certification, and wiring
- **Impact**: Opus's isolation makes convergence independently testable and deferrable. Haiku's bundling is more efficient but creates a larger, harder-to-review phase.

### D-08: Staffing/Resource Model

- **Opus**: No staffing guidance
- **Haiku**: Explicitly recommends 1 implementer + 1 reviewer + 1 validation pass
- **Impact**: Haiku provides actionable resource planning; Opus assumes a single-developer context.

### D-09: Resume Semantics Handling

- **Opus**: Notes OQ-004 as blocking Phase 2 edge case; proposes "fresh=overwrite, resume=append" as two distinct modes
- **Haiku**: Elevates resume semantics to Phase 1 blocker; flags it should block release if unresolved
- **Impact**: Haiku is stricter — won't ship ambiguous behavior. Opus proposes a default and moves on.

### D-10: Eval Philosophy

- **Opus**: Validation is test-centric (unit + integration + performance benchmarks)
- **Haiku**: Explicitly calls out "real CLI-driven evals" and "third-party verifiability" per project memory preferences
- **Impact**: Haiku aligns with the project's documented preference (see `feedback_real_evals_not_unit_tests.md`). Opus's validation is thorough but doesn't emphasize this distinction.

### D-11: Risk Contingency Depth

- **Opus**: Risks have mitigation column but no contingency plans
- **Haiku**: Each risk includes both mitigation AND explicit contingency (fallback if mitigation fails)
- **Impact**: Haiku provides better operational resilience planning.

### D-12: Critical Path Analysis

- **Opus**: Explicit critical path: P1→P2→P4→P5→P6, with P3 parallel to P2
- **Haiku**: Sequential critical path through all phases; notes "dominated by ambiguity resolution"
- **Impact**: Opus identifies parallelism opportunity. Haiku's linear path is simpler but potentially slower.

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Parallel phase identification**: Explicitly marks Phase 3 as parallelizable with Phase 2
- **Requirements traceability**: Every phase lists specific FR/NFR/SC requirements covered
- **Success criteria matrix**: Clean table mapping each SC to its validation phase and method
- **Convergence isolation**: Separating convergence into its own phase reduces blast radius

### Haiku is stronger in:
- **Requirements closure discipline**: Dedicated phase prevents building on ambiguity
- **Project workflow compliance**: Includes `make sync-dev` / `make verify-sync` in release phase
- **Eval philosophy alignment**: Explicitly honors the project's "real evals, not unit tests" preference
- **Risk contingency planning**: Every risk has a fallback, not just a mitigation
- **Resource planning**: Concrete staffing recommendation
- **Tighter timeline**: More efficient phase bundling without sacrificing coverage

## 4. Areas Requiring Debate to Resolve

1. **Design-first vs code-first**: Should OQs be resolved in a dedicated phase (Haiku) or inline as they block (Opus)? Tradeoff: speed vs rework risk.

2. **Convergence isolation vs bundling**: Dedicated phase (Opus) gives cleaner testing but adds calendar time. Bundling (Haiku) is efficient but creates a large Phase 4.

3. **Dry-run as parallel workstream vs co-located contract**: Opus enables earlier validation; Haiku ensures dry-run output is always consistent with the features it describes.

4. **Timeline realism**: Haiku's 4.5–7.5 day estimate assumes fast OQ resolution. If Phase 1 stalls, the entire schedule shifts. Opus's wider range (6–10 days) may be more honest.

5. **Release phase necessity**: Is an explicit sync/release phase needed, or is it assumed as part of normal workflow? Given the project's documented sync discipline, Haiku's inclusion seems warranted.
