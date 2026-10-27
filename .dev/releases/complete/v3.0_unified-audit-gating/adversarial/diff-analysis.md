---
total_diff_points: 12
shared_assumptions_count: 18
---

## 1. Shared Assumptions and Agreements

Both variants agree on these foundational points:

1. **Three failure classes**: Unwired optional callable injections, orphan provider modules, unregistered dispatch registry entries
2. **Deterministic Python-only analysis** using `ast` module — no LLM synthesis
3. **Zero substrate modifications**: Consume `SemanticCheck`, `GateCriteria`, `gate_passed()` as-is
4. **Shadow → soft → full promotion** with quantitative FPR/TPR thresholds
5. **`WIRING_GATE` as `GateCriteria`** with 5 semantic checks (analysis complete, recognized mode, counts consistent, severity consistent, zero blocking for mode)
6. **Frontmatter regex duplication is intentional** — do not refactor into shared module (NFR-007)
7. **`retry_limit=0`** and `GateMode.TRAILING` for the roadmap step
8. **ToolOrchestrator/T06 is CUT-ELIGIBLE** — defer to v3.1 if needed
9. **Agent extensions are additive-only** — no existing rules or tools removed
10. **Promotion thresholds**: Soft requires FPR <15%, TPR >50%, p95 <5s; Full requires FPR <5%, TPR >80%, whitelist stable 5+ sprints
11. **Minimum 2 release cycles** of shadow before promotion
12. **Coverage ≥90%** on `wiring_gate.py` and `wiring_analyzer.py`; 20+ unit tests, 3+ integration tests
13. **Performance targets**: <5s for 50 files, <2s sprint post-task
14. **`provider_dir_names` misconfiguration** is the highest-priority risk
15. **Merge v3.0 before v3.1** to minimize rebase conflicts in `gates.py`
16. **Whitelist mechanism** with YAML loading and suppression counting
17. **Graceful degradation** on AST parse errors — log, skip, count
18. **cli-portify no-op retrospective** as a validation fixture

---

## 2. Divergence Points

### D01: Phase 0 — Architecture Confirmation Phase

- **Haiku variant**: Includes an explicit **Phase 0** (0.5–1 phase-unit) dedicated to confirming architectural seams, assigning owners for open questions, defining module boundaries, and locking the acceptance contract before any code.
- **Opus variant**: Has no Phase 0. Addresses open questions in a table (Section 4) and recommends resolving them "before implementation" but does not allocate a dedicated phase.
- **Impact**: Haiku's approach reduces rework risk at the cost of a slight schedule delay. Opus's approach gets to code faster but risks discovering misaligned assumptions mid-implementation.

### D02: Phase Structure — 6 vs 7 Phases

- **Opus**: 6 phases — Core Analysis → Gate Definition → Pipeline Integration → Agent Extensions → Testing → Shadow Calibration. Roadmap and sprint integration are bundled into Phase 3.
- **Haiku**: 7 phases (including Phase 0). Roadmap integration (Phase 3) and sprint integration (Phase 4) are separate phases. ToolOrchestrator and agent extensions are bundled into Phase 5.
- **Impact**: Haiku's separation of roadmap and sprint integration provides cleaner milestone boundaries and allows sprint work to start once Phase 1 stabilizes (parallel path). Opus bundles them for fewer phase transitions.

### D03: Task Granularity and Numbering

- **Opus**: Defines 15 explicit tasks (T01–T15) with file-level CREATE/MODIFY/EXTEND annotations and dependency DAG.
- **Haiku**: Describes work items narratively within each phase without formal task IDs. Milestones are sub-numbered (M1.1–M1.5, etc.) with more granular checkpoints.
- **Impact**: Opus is more directly actionable for sprint planning and tasklist generation. Haiku provides richer milestone decomposition for progress tracking.

### D04: File Layout — Separate Config File

- **Opus**: Creates `audit/wiring_config.py` as a separate file for `WiringConfig` (T01), with `WiringFinding` + `WiringReport` in `audit/wiring_gate.py` (T02).
- **Haiku**: Does not prescribe separate config file — lists all core models together in Phase 1 without file-level split decisions.
- **Impact**: Opus's separate config file improves modularity and testability. Haiku defers this decision, which is consistent with its Phase 0 "confirm boundaries first" approach.

### D05: Report Body Section Enumeration

- **Opus**: Does not enumerate the required report body sections.
- **Haiku**: Explicitly lists all 7 required report body sections in exact order (Summary, Unwired Optional Callable Injections, Orphan Modules/Symbols, etc.).
- **Impact**: Haiku provides a more complete implementation contract for the report emitter, reducing ambiguity during coding.

### D06: Whitelist Error Handling Evolution

- **Opus**: Whitelist is loaded in T01 with validation, but no phase-aware error escalation described.
- **Haiku**: Specifies **phase-aware malformed-entry behavior** — warning in Phase 1, `WiringConfigError` in Phase 2+.
- **Impact**: Haiku's approach is more operationally mature, allowing early development flexibility while hardening for production.

### D07: SprintConfig Type Specification

- **Opus**: Adds `wiring_gate_mode` to `SprintConfig` without specifying the type system.
- **Haiku**: Specifies `wiring_gate_mode: Literal["off", "shadow", "soft", "full"]` with an explicit `"off"` option.
- **Impact**: Haiku's `"off"` mode provides a clean disable mechanism. Opus implicitly handles this through mode semantics but doesn't call it out.

### D08: Resource/Staffing Model

- **Opus**: Does not define engineering roles or staffing requirements.
- **Haiku**: Defines 4 explicit engineering roles (backend/static analysis, pipeline/architecture, QA/quality, agent/tooling).
- **Impact**: Haiku is more useful for project planning and resource allocation. Opus treats this as an implementation-focused roadmap without organizational concerns.

### D09: Operational Dependencies

- **Opus**: Lists compute/tooling requirements (stdlib, PyYAML, test fixtures).
- **Haiku**: Lists 5 **operational dependencies** (confirmed `provider_dir_names`, whitelist governance owner, promotion review owner, merge coordination plan, shadow telemetry collection process).
- **Impact**: Haiku surfaces non-code prerequisites that could block rollout. Opus assumes these will be resolved as part of open question resolution.

### D10: Risk Handling Framework

- **Opus**: Traditional risk table with Impact/Mitigation columns, organized by priority tier.
- **Haiku**: Adds a **4-layer risk handling model** (Prevent → Detect → Contain → Recover) as a meta-framework on top of individual risk descriptions. Also elevates "rollout ambiguity and governance gaps" as a top-5 risk.
- **Impact**: Haiku's layered model provides a systematic approach to risk management. Opus is more compact and directly actionable.

### D11: Scope of "Primary Deliverable" Framing

- **Opus**: Frames shadow mode as "the primary deliverable" (Recommendation #4) — enforcement is a future promotion decision.
- **Haiku**: Frames the entire initiative as a "controlled architecture rollout, not just a feature build" — the right success condition is "trusted shadow visibility with stable integration."
- **Impact**: Both arrive at the same conclusion but Haiku's framing more explicitly manages stakeholder expectations about what v3.0 means.

### D12: Critical Path Definition

- **Opus**: Critical path: T01 → T02 → T03 → T05 → T08 (task-level).
- **Haiku**: Critical path: Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 6 (phase-level), with Phase 4 starting after Phase 1 stabilizes and Phase 5 explicitly off critical path.
- **Impact**: Opus gives implementers a concrete task chain. Haiku gives project managers a phase-level view with explicit parallelism opportunities.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Task-level actionability**: T01–T15 with file paths, CREATE/MODIFY annotations, and dependency DAG — directly convertible to a sprint tasklist
- **Parallelism identification**: Explicitly calls out Wave 1 (T01 ∥ T02), T06 ∥ T07, T10–T12 ∥ T13
- **Architectural recommendations section**: 5 crisp, numbered recommendations with specific rationale (especially #3 on frontmatter regex duplication)
- **Scope quantification**: "7 new files, 7 modified files, ~500 LOC production, ~400 LOC test"
- **Cut decision clarity**: Both T06 and Phase 4 explicitly marked as deferrable with clear criteria

### Haiku is stronger in:
- **Phase 0 governance**: Dedicated architecture confirmation phase prevents costly rework
- **Report specification completeness**: Enumerates all 7 body sections in order; specifies 15-field frontmatter
- **Operational maturity**: Staffing model, operational dependencies, governance ownership, whitelist error escalation
- **Risk framework**: 4-layer Prevent/Detect/Contain/Recover model provides systematic coverage
- **Delivery strategy**: Three-tranche model (implementation → optional extension → operational readiness) with explicit exit criteria per phase
- **Sprint integration specifics**: `Literal["off", "shadow", "soft", "full"]` type, per-task artifact emission, governance compatibility checks

---

## 4. Areas Requiring Debate to Resolve

1. **Phase 0: Yes or No?** — Does a dedicated architecture confirmation phase add enough value to justify delaying code? Or are the open questions resolvable inline during T01 development? The answer depends on team familiarity with the codebase.

2. **Roadmap + Sprint bundled vs. separated** — Opus bundles both into Phase 3 (T07–T09). Haiku separates them (Phase 3 roadmap, Phase 4 sprint). The right choice depends on whether sprint integration genuinely depends on validated roadmap integration or can proceed independently from the core analyzer.

3. **Task IDs vs. narrative phases** — For tasklist generation, Opus's T01–T15 scheme is directly consumable. For roadmap communication, Haiku's milestone-heavy narrative is more readable. Should the final roadmap include both?

4. **File layout decisions up-front or deferred** — Opus commits to `wiring_config.py` as a separate file now. Haiku defers file-level decisions to Phase 0. The trade-off is early clarity vs. flexibility to discover the right boundaries.

5. **Staffing model inclusion** — Haiku's 4-role model is useful for resource planning but may over-specify for a single-implementer scenario (Claude Code sessions). Should it be kept, simplified, or dropped?

6. **Whitelist error escalation timing** — Haiku's phase-aware behavior (warn → error) adds operational safety but also implementation complexity. Is this warranted for v3.0 or should strict validation be the default from the start?
