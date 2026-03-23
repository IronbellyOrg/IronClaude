---
total_diff_points: 12
shared_assumptions_count: 14
---

# Diff Analysis: Haiku-Analyzer vs Haiku-Architect Roadmap Variants

## 1. Shared Assumptions and Agreements

1. **Complexity score**: Both assign 0.85 (HIGH).
2. **Spec source**: Both reference `portify-release-spec.md`.
3. **Strictly sequential FR dependency chain**: FR-PORTIFY-CLI.1 → 7.
4. **Synchronous-only execution**: No `async def`/`await` anywhere in `cli_portify/`.
5. **Base-type extension model**: `PortifyConfig → PipelineConfig`, `PortifyStepResult → StepResult`, `PortifyProcess → ClaudeProcess`.
6. **Additive-only constraint**: No modifications to `pipeline/` or `sprint/`.
7. **18-module architecture**: Both accept the accepted module structure.
8. **Same 8 dependencies**: `pipeline.models`, `pipeline.gates`, `pipeline.process`, `sprint.models`, `sprint.process`, `/sc:brainstorm`, `/sc:spec-panel`, `claude` binary.
9. **Same Python library deps**: `click>=8.0.0`, `rich>=13.0.0`, `pyyaml`, Python ≥3.10.
10. **Same 9 risks identified**: Both map the same risk inventory items.
11. **Same 12 success criteria**: Both treat all 12 as required validation targets.
12. **Real evals over mocks**: Both cite project memory favoring artifact-producing E2E runs.
13. **`@path` references for context management**: Both mandate file references over inline content.
14. **Self-portification as final confidence anchor**: Both treat Success Criterion #12 as a meta-test.

---

## 2. Divergence Points

### D1: Phase Count and Granularity

- **Analyzer**: 6 phases (Phase 0–5). Monitoring, resume, UX bundled into existing phases.
- **Architect**: 7 milestones (M1–M7). Dedicated Milestone 6 for monitoring, resume semantics, UX, and failure recovery.
- **Impact**: Architect's separation makes resume/monitoring a first-class deliverable with its own exit criteria. Analyzer risks treating these as secondary concerns absorbed into other phases.

### D2: Timeline Estimates

- **Analyzer**: 20–28 working days across 6 phases.
- **Architect**: 25–32 working days across 7 milestones.
- **Impact**: 5–4 day delta. Architect's longer estimate reflects the dedicated M6 phase and a more conservative M5 (5–6 days vs 4–6 days). Architect's estimate is likely more realistic given the operational complexity.

### D3: Where Resume Semantics Are Resolved

- **Analyzer**: Lists resume as a must-resolve open question before M5, but does not assign a dedicated phase. Spread across Phase 0 (CLI surface), Phase 4 (convergence), Phase 5 (validation).
- **Architect**: Concentrates resume semantics in dedicated M6 with explicit exit criteria requiring Open Questions 1, 2, 3, and 8 resolved.
- **Impact**: Architect's approach reduces the risk of resume logic being partially implemented across phases without cohesive validation.

### D4: Monitoring and Diagnostics Treatment

- **Analyzer**: Mentions monitor/reporting scaffolding in Phase 0 and lists it as parallelizable work (Stream C), but no dedicated phase or exit gate.
- **Architect**: Assigns M6 with explicit deliverables: monitor/diagnostics module, NDJSON signal vocabulary, warning vs failure classification.
- **Impact**: Architect treats operational observability as a gated deliverable; Analyzer treats it as scaffolding built incrementally.

### D5: Release Governance Gates

- **Analyzer**: Recommends gating Phase 3 and Phase 4 with artifact contract checks. No explicit governance model.
- **Architect**: Proposes 4 explicit governance gates: after M1 (architecture), M3 (runner behavior), M5 (convergence), and M7 (release).
- **Impact**: Architect's governance model is more structured and provides earlier intervention points. The post-M1 gate is particularly valuable for catching architecture drift before code scales.

### D6: Risk Prioritization

- **Analyzer**: Lists all 9 risks at the same level, then separates residual-risk management.
- **Architect**: Explicitly separates high-priority (5 risks) from medium-priority (3 risks), omitting Risk 4 (sequential wall-clock time) from the high tier.
- **Impact**: Architect's tiering provides clearer triage guidance. Analyzer's flat list requires implementers to self-prioritize.

### D7: Parallelizable Work Identification

- **Analyzer**: Identifies 3 explicit parallel streams (A: core implementation, B: validation harness, C: review/diagnostics) with specific work items.
- **Architect**: Does not explicitly identify parallel streams; work is organized strictly by milestone dependency chain.
- **Impact**: Analyzer's parallel stream identification enables better resource utilization if multiple contributors are available.

### D8: Phase 4 / M5 Duration and Scope

- **Analyzer**: Phase 4 (Panel Review + Convergence + Release Readiness) estimated at 4–6 days.
- **Architect**: M5 (Panel Review + Convergence Engine + Quality Gates) estimated at 5–6 days, and explicitly calls it "the highest-risk part of the release."
- **Impact**: Architect's tighter lower bound (5 vs 4) and explicit risk callout better reflects the complexity. Analyzer bundles "Release Readiness" into this phase which the Architect separates into M6+M7.

### D9: Additive-Only Enforcement Strategy

- **Analyzer**: Recommends "structural comparison or section hashing rather than trusting model behavior" for NFR-008 enforcement.
- **Architect**: Mentions additive-only validation but does not prescribe a specific mechanism.
- **Impact**: Analyzer provides a concrete, implementable strategy. Architect leaves the mechanism as an implementation decision.

### D10: Open Question Resolution Timing

- **Analyzer**: Treats medium-impact open questions as must-resolve before M5, explicitly lists: resume from Phase 3, NDJSON signal vocabulary, resume from Phase 4, `--resume`/`--start` CLI flags.
- **Architect**: Resolves Open Question 9 in M1 exit criteria, and Open Questions 1, 2, 3, 8 in M6 exit criteria.
- **Impact**: Architect maps questions to specific milestones with exit-gate enforcement. Analyzer sets a deadline (before M5) but doesn't assign ownership to a phase.

### D11: Architect Priority Framework

- **Analyzer**: No explicit priority ordering for tradeoff resolution.
- **Architect**: Provides a ranked 5-point priority framework for tradeoffs: (1) Deterministic runner control, (2) STRICT gate integrity, (3) Base-module immutability, (4) Skill reuse with safe fallbacks, (5) Operational resilience.
- **Impact**: Architect's framework gives implementers clear guidance when competing concerns conflict. This is absent from the Analyzer variant.

### D12: Framing and Narrative Emphasis

- **Analyzer**: Frames the project around "control integrity" — ensuring gates, contracts, and failure paths are correct.
- **Architect**: Frames the project as a "control-plane-first system" — keeping Claude subordinate to Python execution.
- **Impact**: Both framings are compatible but emphasize different aspects. Analyzer focuses on verification; Architect focuses on architectural dominance hierarchy.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Architect is stronger in:
- **Governance model**: 4 explicit gates vs ad-hoc gating recommendations
- **Resume/monitoring isolation**: Dedicated M6 prevents these critical concerns from being diluted across phases
- **Tradeoff resolution**: Ranked priority framework gives implementers a decision tool
- **Risk tiering**: High/medium separation provides actionable triage
- **Requirement traceability**: Explicit NFR-to-milestone mapping table at the end

### Analyzer is stronger in:
- **Parallel work identification**: 3 named streams with concrete work assignments enable multi-contributor execution
- **Additive-only enforcement**: Prescribes structural comparison/section hashing — a concrete, testable mechanism
- **Validation ordering**: Explicit 5-step validation sequence (static → structural → review → E2E → self-portification)
- **Performance gate emphasis**: Calls out FR-PORTIFY-CLI.1f and 2f as real performance gates that precede expensive work
- **Open question urgency**: Treats medium-impact questions as schedule threats, not just documentation items

---

## 4. Areas Requiring Debate to Resolve

1. **6 phases vs 7 milestones**: Should monitoring/resume/UX get a dedicated phase (Architect) or be absorbed into existing phases (Analyzer)? The dedicated phase adds ~3-4 days but provides clearer exit criteria.

2. **Parallel streams vs sequential milestones**: Can the project benefit from the Analyzer's 3-stream parallelism, or does the Architect's strict milestone chain better prevent integration issues?

3. **Additive-only enforcement mechanism**: Should the roadmap prescribe structural comparison/section hashing (Analyzer) or leave this as an implementation decision (Architect)?

4. **Timeline realism**: Is the Analyzer's 20–28 day estimate achievable without a dedicated monitoring/resume phase, or is the Architect's 25–32 days the honest range?

5. **Governance gate count**: Are 4 gates (Architect) necessary, or do 2 gates at Phase 3/4 boundaries (Analyzer) suffice without adding ceremony overhead?
