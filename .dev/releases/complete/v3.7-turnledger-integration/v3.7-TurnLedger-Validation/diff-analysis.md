---
total_diff_points: 12
shared_assumptions_count: 14
---

# Comparative Analysis: Opus-Architect vs Haiku-Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Spec source and complexity**: Both derive from `v3.3-requirements-spec.md` with complexity 0.82
2. **Validation-focused release**: Agreement that v3.3 is primarily test authoring with three constrained production changes (FR-5.1, FR-5.2, FR-4.3)
3. **`_subprocess_factory` as sole injection seam**: Both enforce NFR-1 identically
4. **4-phase structure**: Foundation → E2E suites → Pipeline fixes/gates → Regression/acceptance
5. **Audit trail as cross-cutting prerequisite**: Both place FR-7 infrastructure in Phase 1 as a dependency for all tests
6. **AST reachability analyzer risk**: Both flag dynamic dispatch/lazy imports as the highest technical risk (R-1)
7. **FR-5.2 conservatism**: Both recommend exact symbol matching over fuzzy/semantic approaches
8. **Same 5 risk items**: Identical risk identification (R-1 through R-5) with aligned severity ratings
9. **Same technical dependencies**: `ast` stdlib, pytest >=7.0, `GateCriteria`, `_run_checkers()`, `v3.0-v3.2-Fidelity` branch
10. **Same SC mapping**: All 12 success criteria mapped to the same phases
11. **Same file modification targets**: `wiring_gate.py`, `roadmap/executor.py`, convergence test files
12. **JSONL-per-run audit strategy**: Both use timestamped JSONL with identical 8-field schema
13. **Session-scoped audit fixture**: Agreement on scope and flush behavior
14. **Phase 2 as largest workstream**: Both estimate 3-5 days for E2E suite authoring

## 2. Divergence Points

### D-1: Phase 0 — Specification Lock Phase

- **Opus**: No Phase 0. Jumps directly into implementation. Open questions are addressed in an appendix (8 items) with architect recommendations inline.
- **Haiku**: Adds an explicit Phase 0 (0.5–1 day) for specification lock, architecture decisions, and traceability matrix production before any code is written.
- **Impact**: Haiku's approach reduces ambiguity risk at the cost of calendar time. Opus assumes decisions can be made just-in-time during Phase 1. For a high-coupling release (0.82), Haiku's upfront lock is defensively stronger. Opus's approach is faster if the implementer is the architect.

### D-2: Dispatch/Wiring Mechanism Documentation Depth

- **Opus**: Enumerates 6 named artifacts inline within Phase 2/3 with file locations, line numbers, cross-references, and owning phases. Each has an explicit "Wired Components" and "Cross-Reference" block.
- **Haiku**: Separates integration points into a dedicated Section 3 with 8 named mechanisms, each with architect notes, but without line-number precision.
- **Impact**: Opus provides higher implementer utility (line numbers enable direct navigation). Haiku provides better architectural documentation (standalone section, easier to review without reading phase details). Opus is better for a single implementer; Haiku is better for team handoffs.

### D-3: Test Count Specificity

- **Opus**: Provides exact test counts per task (e.g., "2A.1: 4 tests", "2C.1: 8 tests") totaling ~53 explicitly enumerated tests across Phase 2.
- **Haiku**: Lists requirement coverage without committing to specific test counts. References "all FR-1.1 through FR-1.18" but doesn't say how many test functions each maps to.
- **Impact**: Opus enables precise progress tracking and SC-1 validation ("≥20 wiring point tests"). Haiku defers count decisions to the implementer, which is riskier for SC-1 compliance but allows flexibility in test granularity.

### D-4: New File Inventory

- **Opus**: Explicitly lists 10 new files with phase assignments and purposes in a dedicated table.
- **Haiku**: Mentions directory layout (`tests/v3.3/`, `tests/roadmap/`, `tests/audit-trail/`) but does not enumerate individual files.
- **Impact**: Opus provides a concrete implementation scaffold. Haiku leaves file organization to the implementer. For sprint execution, Opus's inventory is directly actionable.

### D-5: Timeline Precision

- **Opus**: Fixed estimates: Phase 1 ~3d, Phase 2 ~5d, Phase 3 ~2d, Phase 4 ~1d. Total: ~11 days. Critical path identified.
- **Haiku**: Range estimates: Phase 0 0.5–1d, Phase 1 1–2d, Phase 2 3–5d, Phase 3 2–4d, Phase 4 1–2d. Total: 7.5–14 days. Milestone cadence with day ranges.
- **Impact**: Opus's fixed estimates are more plannable but less honest about uncertainty. Haiku's ranges better reflect the 0.82 complexity score. Haiku's inclusion of Phase 0 makes its pessimistic case (14d) notably longer.

### D-6: Reachability Analyzer Phasing

- **Opus**: Full AST analyzer implementation in Phase 1B (parallel with audit trail). Gate integration deferred to Phase 3A.4.
- **Haiku**: Phase 1 only builds "skeleton and limitations contract." Full implementation deferred to Phase 3.
- **Impact**: Opus front-loads technical risk, enabling earlier detection of R-1 issues. Haiku reduces Phase 1 scope but concentrates risk in Phase 3, which already carries FR-5.1 and FR-5.2. Opus's approach is architecturally safer for the critical path.

### D-7: Team Role Assumptions

- **Opus**: Implicitly assumes a single implementer (no role assignments).
- **Haiku**: Defines 4 team roles: architect/lead, backend/pipeline engineer, QA/test engineer, release verifier.
- **Impact**: Haiku's role separation enables parallel workstreams but assumes team availability. Opus is realistic for the likely single-agent execution context. For sprint CLI execution, Opus's model is more appropriate.

### D-8: Traceability Matrix

- **Opus**: Provides a Success Criteria Validation Matrix (12 rows) mapping SC-ID → method → phase → automated flag.
- **Haiku**: Calls for a traceability matrix in Phase 0 covering all 13 top-level requirements mapped to files/tests, but doesn't provide one.
- **Impact**: Opus delivers the artifact inline. Haiku defers it as a Phase 0 deliverable. Opus is immediately actionable; Haiku treats it as a first task.

### D-9: Open Question Resolution Style

- **Opus**: 8 numbered open questions with explicit architect recommendations and rationale.
- **Haiku**: References the same questions but resolves them as Phase 0 tasks rather than providing answers.
- **Impact**: Opus unblocks implementation immediately. Haiku creates a formal decision gate. For autonomous execution, Opus's pre-resolved approach eliminates a blocking dependency.

### D-10: Integration Point Count and Granularity

- **Opus**: 6 integration points documented inline within phases.
- **Haiku**: 8 integration points in a dedicated section, adding convergence registry constructor and convergence findings merge as separate items.
- **Impact**: Haiku's separation of `merge_findings()` and the registry constructor as distinct integration points provides finer-grained tracking. Opus bundles these under Phase 2A.10 tasks. Haiku's model is more precise for wiring verification.

### D-11: Validation Checkpoint Structure

- **Opus**: 4 milestones (end of each phase) with specific deliverable criteria.
- **Haiku**: 4 milestones plus 4 intermediate checkpoints (A–D) with distinct validation focus areas.
- **Impact**: Haiku's dual-layer structure (milestones + checkpoints) provides more granular progress gates. Opus's single-layer milestones are sufficient but less structured for team coordination.

### D-12: Final Recommendations Focus

- **Opus**: 8 operational recommendations (signal handling, checker granularity, fixture scope, etc.) — implementation-focused.
- **Haiku**: 6 strategic recommendations (sequencing discipline, architectural sentinels, audit-as-evidence) — governance-focused.
- **Impact**: Opus's recommendations directly unblock coding decisions. Haiku's recommendations guide project management and quality gates. Both are valuable; they address different audiences.

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Implementation readiness**: Exact test counts, file inventories, line numbers, pre-resolved open questions — directly executable by a sprint runner
- **Wiring mechanism traceability**: Inline cross-references with file:line precision
- **Critical path analysis**: Explicit identification of Phase 1A → Phase 2 → Phase 4 as the critical path with Phase 1B parallelizable
- **Risk mitigation specificity**: R-3 mitigation includes concrete "allowlist of known FR→function mappings" recommendation

### Haiku is stronger in:
- **Architectural documentation**: Dedicated integration points section (Section 3) is reviewable independently of implementation phases
- **Governance structure**: Phase 0 lock, team roles, checkpoint/milestone layering — better for auditable delivery
- **Honest uncertainty**: Range-based timeline estimates better reflect complexity
- **Integration point completeness**: 8 mechanisms vs 6, with finer granularity on convergence registry boundaries

## 4. Areas Requiring Debate to Resolve

1. **Phase 0 necessity**: Is a formal specification lock phase worth 0.5–1 day, or are Opus's inline resolutions sufficient? Depends on whether the implementer is also the architect.

2. **Reachability analyzer timing**: Should the full AST implementation land in Phase 1 (Opus) or Phase 3 (Haiku)? Front-loading reduces Phase 3 risk but increases Phase 1 scope. The answer depends on whether Phase 2 tests need reachability results.

3. **Test count commitment**: Should the roadmap commit to exact test counts (Opus: ~53) or leave granularity to the implementer (Haiku)? Exact counts enable SC-1 tracking but may force artificial test splitting.

4. **Team model**: Single-agent execution (Opus) vs multi-role (Haiku)? The sprint CLI context strongly favors Opus's model, but Haiku's roles map well if parallel agent delegation is available.

5. **Integration point documentation location**: Inline with phases (Opus) vs standalone section (Haiku)? A merged approach — standalone section with phase back-references — would capture both benefits.
