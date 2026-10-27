---
total_diff_points: 14
shared_assumptions_count: 18
---

## 1. Shared Assumptions and Agreements

Both variants agree on these foundational positions:

1. **Hybrid architecture**: 5 structural checkers (~70%) + residual semantic layer (~30%)
2. **Critical path**: FR-2 → FR-1 → FR-4 → FR-7
3. **Legacy byte-identity**: `convergence_enabled=false` must reproduce commit `f4d9035` exactly
4. **Single dispatch gate**: `convergence_enabled` boolean as the sole legacy/convergence boundary
5. **DeviationRegistry as sole authority** in convergence mode; `SPEC_FIDELITY_GATE` excluded
6. **TurnLedger consumed, not modified** — conditional import, convergence-only
7. **Stable finding ID tuple**: `(dimension, rule_id, spec_location, mismatch_type)`
8. **≤3 convergence runs** with budget accounting
9. **Monotonic progress on structural HIGHs only** — semantic HIGH increases are warnings, not regressions
10. **No git worktrees** for FR-8 temp isolation
11. **Per-patch diff-size guard** at 30% threshold with `--allow-regeneration` override
12. **Same 6 risks** identified with consistent severity ratings
13. **Same file creation/modification/deletion plan** (spec_parser.py create, fidelity.py delete, etc.)
14. **Same 5 open questions** requiring resolution
15. **Debate protocol**: prosecutor/defender parallel, deterministic Python judge, conservative tiebreak
16. **30,720-byte prompt budget** with proportional allocation and truncation markers
17. **Parser graceful degradation** via `ParseWarning` rather than hard failure
18. **Real-spec validation** required (not synthetic fixtures only)

---

## 2. Divergence Points

### D1: Phase 0 — Baseline Verification Phase
- **Opus**: Jumps directly into Phase 1 (parser + data model) with no explicit baseline verification phase
- **Haiku**: Adds a dedicated Phase 0 (2–3 days) for baseline verification, interface lock, and acceptance-test matrix mapping
- **Impact**: Haiku's Phase 0 reduces ambiguity risk but adds 2–3 days upfront. Opus implicitly assumes baseline is understood and starts building immediately.

### D2: Phase Count and Granularity
- **Opus**: 6 phases (Foundation → Checkers → Convergence → Semantic → Regression/Remediation → Integration)
- **Haiku**: 8 phases (Phase 0 baseline + separates registry from convergence + separates remediation from regression + final integration)
- **Impact**: Haiku's finer decomposition creates more milestone gates but may slow delivery. Opus's coarser phases are faster but have larger blast radius per phase failure.

### D3: Registry and Convergence Coupling
- **Opus**: Phase 3 bundles deviation registry, convergence gate, TurnLedger integration, legacy dispatch, and FR-7.1 interface contract into one phase (Days 10–15)
- **Haiku**: Phase 3 covers only registry + run memory (FR-6, FR-10); convergence engine and regression are deferred to Phase 5 (separate phase)
- **Impact**: Opus's bundling is more efficient but riskier — registry bugs discovered during convergence wiring are harder to isolate. Haiku's separation validates the registry independently before convergence depends on it.

### D4: Semantic Layer vs. Convergence Ordering
- **Opus**: Semantic layer (Phase 4) precedes regression/remediation (Phase 5); convergence engine is in Phase 3
- **Haiku**: Registry (Phase 3) → Semantic (Phase 4) → Convergence+Regression (Phase 5) → Remediation (Phase 6)
- **Impact**: Haiku's ordering ensures the semantic layer is validated before convergence consumes it. Opus's ordering builds the convergence shell first, then plugs semantic into it — potentially requiring rework if semantic output format doesn't match convergence expectations.

### D5: FR-10 Run-to-Run Memory Placement
- **Opus**: Places FR-10 in Phase 4 (alongside semantic layer)
- **Haiku**: Places FR-10 in Phase 3 (alongside deviation registry)
- **Impact**: Haiku's placement is architecturally cleaner — run-to-run memory is fundamentally a registry concern, not a semantic concern. Opus treats it as a semantic feature because the semantic prompt consumes it.

### D6: Data Model Extensions Timing
- **Opus**: Phase 1 includes partial FR-3 (severity rule table definition) and partial FR-6 (Finding dataclass extension) alongside the parser
- **Haiku**: Phase 1 is strictly FR-2 + FR-5; data model extensions are implicit in Phase 2/3 when consumed
- **Impact**: Opus front-loads data model work, reducing churn in later phases. Haiku keeps Phase 1 focused but may require more model iteration later.

### D7: Timeline Estimates
- **Opus**: 32 working days total (fixed point estimates per phase)
- **Haiku**: 36–49 working days total (range estimates per phase)
- **Impact**: Opus is 11–34% more aggressive. Haiku's ranges are more honest about uncertainty, especially for phases with LLM integration (semantic, convergence).

### D8: Milestone Gate Formalization
- **Opus**: Exit criteria per phase, but no named cross-phase gates
- **Haiku**: 6 named milestone gates (A–F) spanning phases, each with explicit exit criteria tied to SC criteria
- **Impact**: Haiku's gates provide clearer go/no-go decision points. Opus relies on per-phase exit criteria which don't aggregate well for stakeholder reporting.

### D9: Staffing Model
- **Opus**: No staffing model; assumes single-track development
- **Haiku**: Explicit 4-wave staffing model with capability roles (backend, CLI, LLM workflow, QA)
- **Impact**: Haiku is more useful for team coordination. Opus is more appropriate for a single-developer workflow.

### D10: Requirement-ID Preservation Guidance
- **Opus**: No explicit guidance on ID preservation in artifacts
- **Haiku**: Dedicated section requiring exact ID preservation (no aliasing/renumbering) in code, registry, and reports
- **Impact**: Haiku's guidance prevents ID drift during implementation — a real risk in long-running projects.

### D11: Architectural Priorities Section
- **Opus**: Key decisions embedded in executive summary narrative
- **Haiku**: Explicit numbered "Architectural priorities" section with 5 ranked principles
- **Impact**: Haiku's explicit prioritization is easier to reference when resolving implementation ambiguities.

### D12: "Architect Emphasis" Annotations
- **Opus**: Phase descriptions are task-focused (what to build)
- **Haiku**: Each phase has an "Architect emphasis" block explaining the *why* behind ordering and constraints
- **Impact**: Haiku's annotations help implementers make correct judgment calls when they encounter edge cases not covered by the spec.

### D13: Additional Risks Identified
- **Opus**: Identifies 2 additional risks (Risk 7: pre-v3.05 registry migration, Risk 8: convergence pass credit asymmetry) beyond the shared 6
- **Haiku**: Identifies the same core 6 plus 5 "open-question risks" but does not surface Risks 7–8 as distinct entries
- **Impact**: Opus's explicit Risk 7/8 entries are more visible; Haiku subsumes them into open questions where they may receive less attention.

### D14: Success Criteria Traceability
- **Opus**: SC criteria mapped to phases in a summary table
- **Haiku**: SC criteria mapped to specific requirement IDs with a layered validation strategy (unit → integration → E2E → non-functional)
- **Impact**: Haiku's traceability is more rigorous — each SC criterion links back to supporting FRs and forward to test layers. Opus's table is sufficient but less auditable.

---

## 3. Areas Where One Variant is Clearly Stronger

### Opus is stronger in:
- **Implementation detail density**: Milestones specify exact function names, cost constants (`CHECKER_COST=10`, `REMEDIATION_COST=8`), field lists, and error behaviors. Ready for direct implementation.
- **Additional risk identification**: Risks 7–8 are substantive and worth tracking independently.
- **Timeline aggressiveness**: 32 days is achievable for a single experienced developer already familiar with the codebase.
- **File-level specificity**: Explicitly names files to create, modify, and delete with line counts.

### Haiku is stronger in:
- **Phase 0 baseline verification**: Prevents building on unvalidated assumptions — a cheap insurance phase.
- **Architectural rationale**: "Architect emphasis" blocks explain *why*, not just *what*.
- **Milestone gates**: Named gates (A–F) with SC-linked exit criteria are operationally superior for progress tracking.
- **Registry isolation**: Separating registry validation from convergence engine reduces debugging complexity.
- **Test-layer stratification**: Explicit unit → integration → E2E → non-functional validation layers.
- **Team-scalable structure**: Staffing model and wave plan support multi-developer execution.
- **ID preservation guidance**: Prevents requirement drift across artifacts.
- **FR-10 placement**: Architecturally correct — run memory belongs with the registry, not the semantic layer.

---

## 4. Areas Requiring Debate to Resolve

1. **Phase 0: Yes or no?** — Is 2–3 days of baseline verification worth the delay, or does the team already have sufficient confidence in the existing codebase state?

2. **Registry + Convergence bundling vs. separation** — Opus's 6-phase approach delivers faster but concentrates risk. Haiku's 8-phase approach is safer but slower. The right answer depends on team size and risk tolerance.

3. **FR-10 placement** — Should run-to-run memory be built with the registry (Haiku, architecturally purer) or with the semantic layer that consumes it (Opus, pragmatically simpler)?

4. **Timeline: 32 days vs. 36–49 days** — Opus's point estimate assumes minimal rework; Haiku's range assumes realistic uncertainty. Need calibration against team velocity data.

5. **Semantic-before-convergence vs. convergence-before-semantic** — Opus builds the convergence shell first; Haiku builds registry → semantic → convergence. The debate is whether convergence should consume a validated semantic layer, or whether semantic should plug into a pre-built convergence framework.

6. **Data model front-loading** — Opus's approach of defining severity rules and Finding extensions in Phase 1 reduces later churn but couples foundation work to downstream design decisions that may shift. Haiku's just-in-time approach is more agile but risks repeated model iteration.
