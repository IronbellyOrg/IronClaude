---
convergence_score: 0.72
rounds_completed: 2
---

# Adversarial Debate: Opus-Architect (A) vs Haiku-Architect (B)

## Round 1 — Initial Positions

### D1 — Phase Structure (4 vs 7 phases)

**Variant A (Opus):** Four phases is the correct granularity. This is a single-implementer project producing ~800-1100 LOC. Seven phases creates artificial coordination overhead — phase transitions become ceremony rather than engineering milestones. Our Phase 1 alone delivers data models, analyzers, report emission, gate definition, *and* unit tests. That's a complete, testable vertical slice. Splitting report/gate into a separate phase (Haiku's Phase 2) creates a phase boundary where none is needed — the report is a direct output of the analyzers.

**Variant B (Haiku):** Seven phases exist because seven distinct engineering concerns exist. Collapsing spec closure into "inline recommendations" is how ambiguity leaks into implementation. Collapsing rollout into "post-merge operational concern" is how production incidents happen. Each phase boundary is a review gate — skip them and you lose the ability to catch problems before they compound. The overhead of phase transitions is trivial compared to the cost of discovering in Phase 4 that a Phase 0 question was answered incorrectly.

### D2 — Specification Closure as Explicit Phase

**Variant A (Opus):** We provide 10 numbered open questions with specific architect recommendations (approve/defer/block). An experienced implementer reads these, makes decisions inline, and starts coding. A separate 1-2 day phase for "spec closure" delays delivery with no proportional risk reduction. The recommendations *are* the closure — they just don't require a calendar milestone.

**Variant B (Haiku):** Recommendations are not decisions. Opus says "recommend deferring import alias resolution" — who approves that? Opus says "blocking for Phase 2" on budget constants — but there's no mechanism to ensure that resolution happens before code depends on it. Phase 0 forces the team to produce *decisions*, not *opinions*. The 1-2 day cost is insurance against building on assumptions that turn out wrong — especially for `SprintGatePolicy` constructor compatibility, which Opus itself flags as a blocking investigation.

### D4 — Testing Strategy Placement

**Variant A (Opus):** Tests belong next to the code they validate. Our Phase 1 includes Milestone 1.4 (14+ unit tests). Phase 2 includes Milestone 2.3 (TurnLedger tests). Integration tests consolidate in Phase 4 because they require all components. This is standard test-alongside-code practice — you catch regressions within the phase that introduced them, not 3-4 phases later.

**Variant B (Haiku):** Consolidating tests in Phase 5 allows the quality engineer to work from stable, complete code. Writing tests against in-flux APIs during Phase 1-3 means rewriting test code when interfaces change. The quality engineer role exists precisely to validate the *integrated* system, not to rubber-stamp each phase. Unit tests can certainly be written during development — but the *validation milestone* belongs after feature completion.

### D5 — Rollout as Explicit Phase

**Variant A (Opus):** Our roadmap delivers code-complete, validated software. Rollout is an operational activity that depends on real-world telemetry from production environments — it cannot be meaningfully planned in a roadmap. Shadow mode is built into the enforcement logic (Goal-5a). The promotion criteria are defined by the spec. Adding a "Phase 6" doesn't make rollout happen; it just adds empty milestones to the roadmap.

**Variant B (Haiku):** Rollout is engineering, not operations. Phase 6 defines measurable criteria: findings volume, whitelist usage, zero-findings anomalies, p95 runtime. It defines three explicit milestones — shadow baseline (M12), soft readiness (M13), blocking authorization (M14). Without this, "when do we turn it on?" becomes an ad-hoc decision with no framework. R6 (provider_dir_names mismatch) — which both variants call the highest risk — can only be validated during rollout. Omitting rollout from the roadmap means the highest-risk item has no planned mitigation.

### D9 — Open Question Treatment

**Variant A (Opus):** We provide per-question recommendations with rationale. Question 1: defer import aliases — whitelist mitigates. Question 5: defer `--skip-wiring-gate` — shadow mode provides non-interference. Question 8: exclude provider heuristic — unspecified and untested. Question 12: extend whitelist to all finding types — 10 LOC, prevents FPR gap. An implementer can start Phase 1 today with these decisions. Haiku absorbs all questions into Phase 0 without individual recommendations — requiring a separate decision session.

**Variant B (Haiku):** Individual recommendations are useful but they are *one architect's opinion*, not *team decisions*. Phase 0 creates the forum for these to be debated and locked. Several of Opus's "recommendations" are actually consequential design choices — extending whitelist scope to all finding types changes the config schema. Deferring the provider heuristic narrows Goal-2a scope. These deserve explicit team alignment, not inline footnotes.

---

## Round 2 — Rebuttals

### D1/D2 — Phase Structure and Spec Closure

**Variant A rebutting B:** Haiku claims phase boundaries are "review gates" — but review gates without reviewers are bureaucracy. If this is a solo implementer (which the ~1000 LOC scope suggests), every phase transition is the implementer reviewing their own work. Our milestone-level acceptance criteria serve the same purpose without the overhead. On spec closure specifically: 6 of our 10 open questions are marked "not a blocker" — only questions 2 and 6 are blocking, and both are scoped to Phase 2. There's no reason to hold Phase 1 work for decisions that don't affect Phase 1.

**Variant B rebutting A:** Opus assumes a solo implementer — but the roadmap should be *robust to team size*, not optimized for one case. If a second engineer joins, Opus's roadmap gives them no entry point. More critically: Opus's own Phase 2 starts with "2.0 [BLOCKER] Validate SprintGatePolicy constructor (OQ-6)" — this is literally spec closure happening mid-implementation. We make it Phase 0; Opus makes it a surprise blocker in Phase 2. Which is more honest about the dependency?

### D4 — Testing Strategy

**Variant A rebutting B:** Haiku's "quality engineer works from stable code" argument assumes APIs change between phases. But our Phase 1 API surface (WiringFinding, WiringReport, analyze_* functions) is spec-driven and stable — it implements a defined contract. Tests written in Phase 1 validate that contract. If the API changes in Phase 2, that's a regression the Phase 1 tests *should* catch. Deferring all testing to Phase 5 means a 3-4 day delay before discovering that a Phase 1 analyzer has an off-by-one error in its AST traversal.

**Variant B rebutting A:** We don't prohibit writing tests during development — we say the *validation milestone* is Phase 5. Developers can and should write tests as they go. But the formal exit criterion "14+ unit tests passing, ≥90% coverage" belongs after all feature code is stable. Opus's Milestone 1.4 claims 14+ tests for Phase 1 alone — but Phase 2 changes to TurnLedger may require updating Phase 1 fixtures (e.g., if WiringConfig gains sprint-related fields). Consolidation avoids this churn.

### D5 — Rollout Phase

**Variant A rebutting B:** Haiku's Phase 6 milestones (M12-M14) are not implementable in a code roadmap — they require production telemetry over release cycles. "Collect findings volume" is an operational runbook item, not a code milestone. Including it in the roadmap conflates two different planning artifacts. Our shadow/soft/blocking mode logic is *implemented* in Phase 2 — the *activation decision* is genuinely operational.

**Variant B rebutting A:** The activation decision requires engineering judgment, not just operational monitoring. M14 (blocking authorization) requires verifying "budget constants and recursion protections" — that's code verification, not dashboards. Opus leaves R6 (the highest risk) without a planned validation step after code-complete. Our Phase 6 explicitly validates provider_dir_names against real repositories. The distinction between "engineering" and "operations" is a false boundary when the risk profile demands both.

### D8 — Timeline Estimates

**Variant A rebutting B:** We deliberately omit timeline estimates because the project instructions say "avoid giving time estimates." Haiku's "13-20 engineering days" creates a commitment that may not reflect reality — scope changes, blocked questions, and merge conflicts with Anti-Instincts work can all invalidate these numbers. A roadmap should define *what* and *in what order*, not *when*.

**Variant B rebutting A:** The project instruction about time estimates applies to *the agent's responses to users*, not to roadmap artifacts consumed by stakeholders. A roadmap without timeline estimates cannot be used for resource planning or coordination with the Anti-Instincts work that both variants identify as a merge-conflict risk. Our estimates are ranges (e.g., "3-4 days"), not commitments — they communicate expected magnitude.

---

## Convergence Assessment

### Areas of Agreement (Strong)
- Core technical architecture: identical (AST-only, 3 analyzers, whitelist-first, phased enforcement)
- NFR-006 non-negotiable: both treat pipeline file immutability as a hard constraint
- R6 as highest risk: both identify provider_dir_names mismatch as the critical risk
- Retrospective validation (T11): both require detection of the original no-op bug
- Floor-to-zero credit semantics: both treat as by-design requiring explicit tests
- `roadmap/gates.py` coordination: both flag Anti-Instincts merge-conflict risk

### Areas of Partial Convergence
- **Testing**: Both actually want tests alongside code *and* a final validation pass. The disagreement is about where the *milestone* sits, not whether tests are written early. A hybrid approach (unit tests per phase as acceptance criteria, integration test milestone consolidated) is effectively what Opus already describes.
- **Open questions**: Both agree questions must be resolved. The disagreement is mechanism (inline recommendations vs. formal phase). A compromise: adopt Opus's per-question recommendations but make the two blocking items (budget constants, SprintGatePolicy) explicit prerequisites for Phase 2 start.

### Remaining Disputes (Unresolved)
1. **Rollout as roadmap phase vs. operational concern**: Fundamental disagreement on whether rollout belongs in the implementation roadmap. Haiku's argument is stronger for R6 mitigation; Opus's argument is stronger for roadmap clarity. Resolution depends on whether a separate rollout runbook exists.
2. **Phase granularity**: 4 vs 7 phases reflects different assumptions about team size. Neither variant is wrong — they optimize for different contexts. A merged roadmap should state the assumption explicitly.
3. **Timeline estimates**: Governance question, not technical. Depends on whether stakeholders consume this roadmap for scheduling.
