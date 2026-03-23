---
convergence_score: 0.78
rounds_completed: 3
---

# Adversarial Debate: Opus-Architect vs Haiku-Architect Roadmaps

## Round 1: Initial Positions

### D-1: Phase 0 — Specification Lock

**Variant A (Opus):** Phase 0 is unnecessary overhead. The 8 open questions have clear architectural answers that can be stated inline. For a single-agent sprint CLI execution context, spending 0.5–1 day on a formal decision gate before writing any code is pure calendar waste. The implementer *is* the architect — there's no handoff to protect against. Every hour in Phase 0 is an hour not building the audit trail fixture that everything else depends on.

**Variant B (Haiku):** At complexity 0.82 with 13 top-level requirements and 12 success criteria, skipping a specification lock is reckless. Opus's "inline resolutions" are architect *opinions* embedded in a roadmap — they haven't been validated against the spec or the codebase. The traceability matrix alone justifies Phase 0: without it, you discover mid-Phase-2 that FR-1.14a maps to code that was refactored in v3.2, and you lose a day backtracking. The 0.5-day investment prevents 1–2 day surprises later.

### D-2: Documentation Depth — Inline vs Standalone

**Variant A (Opus):** Line-number precision (`executor.py:735`, `wiring_gate.py:673`) is directly actionable. An implementer can jump to the exact location. Haiku's standalone Section 3 is architecturally elegant but forces context-switching — you read the integration point, then hunt through phases to find where it's actually built and tested. For sprint execution, inline cross-references eliminate navigation overhead.

**Variant B (Haiku):** Line numbers are fragile — they break on the first rebase or upstream merge from `v3.0-v3.2-Fidelity`. A standalone integration section is reviewable independently: an architect can audit wiring completeness without reading every phase task. Haiku also identifies 8 mechanisms vs Opus's 6, catching `merge_findings()` and the registry constructor as distinct boundaries. That granularity matters when Phase 3 extends upstream checker production.

### D-3: Test Count Specificity

**Variant A (Opus):** SC-1 requires "≥20 wiring point tests." Without explicit counts per task, you can't track progress against that threshold during implementation. The ~53 enumerated tests map directly to requirement sub-IDs, enabling automated SC-1 validation via audit trail counts. Deferring count decisions to the implementer is how you end up at 18 tests on the last day and scrambling.

**Variant B (Haiku):** Committing to exact counts (e.g., "2A.1: 4 tests") forces artificial test splitting. If FR-1.1 through FR-1.4 are naturally validated by 2 well-structured tests instead of 4, Opus's roadmap creates pressure to split them for count compliance. The roadmap should specify *coverage*, not *count*. The implementer determines granularity based on what the code actually requires.

### D-6: Reachability Analyzer Phasing

**Variant A (Opus):** Full AST implementation in Phase 1B, parallel with audit trail. This front-loads the highest-risk component (R-1) and enables Phase 2 test authors to reference reachability results if needed. Deferring to Phase 3 — which already carries FR-5.1 and FR-5.2 — concentrates risk in a phase that's already scope-heavy. Phase 1B parallelism with 1A means no calendar cost.

**Variant B (Haiku):** Phase 1 should deliver a skeleton and limitations contract only. The full AST implementation requires understanding which code paths actually need analysis — knowledge that emerges from writing Phase 2 tests. Building the full analyzer before writing the E2E suites risks building the wrong thing. Phase 3's scope is manageable precisely because the production changes are constrained.

### D-9: Open Question Resolution

**Variant A (Opus):** Pre-resolved questions with explicit rationale eliminate blocking dependencies. "Test SIGINT only," "session-scoped fixture," "exact name matching" — these are defensible architectural decisions that don't need a formal gate. Every unresolved question is a decision that will be made anyway, just later and under time pressure.

**Variant B (Haiku):** Opus's resolutions are one architect's opinions without validation against the codebase. What if session-scoped fixtures conflict with parallel test execution? What if SIGINT handling differs on the CI runner's platform? Phase 0 isn't about making different decisions — it's about *verifying* decisions against reality before committing to them in code.

---

## Round 2: Rebuttals

### Opus rebuts Haiku

**On Phase 0:** Haiku claims the traceability matrix "justifies" Phase 0, but Opus *delivers* the matrix inline (Section: Success Criteria Validation Matrix, 12 rows). Haiku promises it as a Phase 0 deliverable — meaning it doesn't exist yet. Which is more useful: a matrix you have now, or one you'll produce tomorrow? The "0.5 day" estimate is also optimistic; decision-by-committee on 8 open questions with 13 requirements easily balloons to a full day of spec review without a single line of code written.

**On integration point count:** Haiku separates `merge_findings()` and the registry constructor as distinct integration points (7 and 8). But these are consumed in a single Phase 2 task (FR-1.15 and FR-1.16) — they're not independently testable boundaries. Opus bundles them under 2A.10 because that's how they'll actually be implemented. Haiku's finer granularity is architectural over-modeling that doesn't translate to implementation utility.

**On test counts:** Haiku warns about "artificial test splitting," but this conflates test *functions* with test *assertions*. Four construction validation tests (FR-1.1–1.4) are four distinct objects with four distinct constructors — there's nothing artificial about testing them separately. Opus's counts aren't arbitrary; they're derived from the requirement structure.

**On reachability timing:** Haiku argues Phase 2 tests inform what the analyzer needs. But the analyzer's scope is already defined by the wiring manifest (FR-4.1), not by test outcomes. The manifest specifies entry points and required reachable targets. The analyzer's job is graph traversal — it doesn't need E2E test results to know what to traverse.

### Haiku rebuts Opus

**On pre-resolved questions:** Opus recommends "session-scoped" fixtures and "SIGINT only" without investigating whether these choices interact with the existing test infrastructure. The project already has `conftest.py` files at multiple levels — has Opus verified that a session-scoped fixture at `tests/v3.3/conftest.py` doesn't conflict with existing session fixtures? Pre-resolving without verification creates confident-but-wrong decisions.

**On line numbers:** Opus cites `executor.py:735` and `wiring_gate.py:673` — but the git status shows both files have uncommitted modifications on this branch. Those line numbers may already be stale. Haiku's architectural descriptions ("executor phase delegation branch") survive rebases; Opus's line references don't.

**On timeline honesty:** Opus claims ~11 days with fixed estimates. Haiku's range (7.5–14 days) better reflects reality at 0.82 complexity. Opus's Phase 2 at "~5 days" for ~53 tests is 10+ tests per day — achievable for repetitive patterns, but one unexpected wiring issue in FR-1.14 (blocking remediation lifecycle) could consume an entire day. Fixed estimates create false precision that undermines planning credibility.

**On team model:** Opus assumes single-agent execution and calls Haiku's roles unrealistic. But Haiku's roles map directly to sprint CLI agent delegation — architect validates, backend implements, QA writes tests. Even in single-agent mode, the role separation provides a mental checklist: "Am I wearing the QA hat or the architect hat right now?" This prevents scope bleed where implementation decisions are made without architectural review.

---

## Round 3: Concessions and Remaining Disagreements

### Opus concedes

1. **Line numbers are fragile.** Given uncommitted modifications on the branch, specific line references will drift. A hybrid approach — architectural description plus approximate location — would be more durable. Haiku's point about rebase survival is valid.

2. **Range estimates are more honest.** Fixed estimates are more plannable but less truthful. For a roadmap consumed by a sprint runner, ranges with a "plan to the pessimistic case" note would serve better than false precision.

3. **`merge_findings()` deserves explicit tracking.** While Opus bundles it under 2A.10, the merge signature stability is load-bearing for Phase 3. Calling it out as a distinct integration boundary — even if tested in the same task — improves Phase 3 risk visibility.

### Haiku concedes

1. **Phase 0 is overkill for single-agent execution.** If the implementer is the architect (which the sprint CLI context implies), a formal decision gate adds ceremony without adding safety. Opus's inline resolutions, while imperfect, are sufficient when the decision-maker and implementer are the same entity.

2. **Test counts enable SC-1 tracking.** Without enumerated counts, there's no way to validate "≥20 wiring point tests" during implementation. The risk of artificial splitting is real but manageable — the roadmap can specify minimum counts while allowing the implementer to merge tests where natural.

3. **Front-loading the AST analyzer reduces Phase 3 risk.** Haiku's skeleton-first approach defers the highest-risk component to the most scope-heavy phase. Opus's parallel execution in Phase 1B is a better risk profile, provided the wiring manifest is frozen first (which both agree on).

### Remaining disagreements

1. **Integration point documentation location.** Opus maintains inline-with-phases is more actionable; Haiku maintains standalone-section is more auditable. Neither fully concedes. A merged approach (standalone section with phase back-references) is acknowledged as optimal by both but not present in either variant.

2. **Open question verification depth.** Opus accepts its resolutions may need codebase verification but argues this happens naturally during Phase 1 implementation. Haiku argues verification should precede implementation. The disagreement is about *when* verification happens, not *whether*.

3. **Team role modeling.** Opus sees roles as unnecessary abstraction for single-agent execution. Haiku sees them as cognitive scaffolding even for a single implementer. This is a genuine philosophical difference about roadmap audience.

---

## Convergence Assessment

### Areas of agreement (strong convergence)

- **4-phase structure** with foundation → E2E → pipeline fixes → regression is the correct sequencing
- **Audit trail as Phase 1 prerequisite** is non-negotiable
- **AST analyzer should be front-loaded** (Haiku conceded to Opus's Phase 1B approach)
- **Test counts should be explicit** for SC-1 tracking (Haiku conceded with the caveat of minimum-not-exact)
- **Phase 0 is unnecessary** for single-agent sprint CLI execution (Haiku conceded)
- **Risk identification and severity** is identical across both variants
- **FR-5.2 conservatism** (exact matching, no NLP) is unanimously endorsed
- **`_subprocess_factory` as sole injection seam** is absolute

### Areas of partial convergence

- **Timeline**: Both agree ranges are more honest; Opus's fixed estimates are acceptable as planning targets with Haiku's ranges as contingency bounds
- **Integration point granularity**: 8 mechanisms (Haiku's count) is more complete, but inline documentation (Opus's style) is more actionable — a merged format would capture both

### Remaining disputes

- **Documentation format**: Inline cross-references vs standalone section — genuinely different tradeoffs for different audiences
- **Verification timing**: Pre-implementation (Haiku) vs during-implementation (Opus) — depends on implementer confidence and codebase familiarity
- **Role modeling**: Cognitive scaffolding (Haiku) vs unnecessary abstraction (Opus) — philosophical, not resolvable by evidence

### Recommended merge strategy

The optimal roadmap takes **Opus as the base** (implementation-ready, pre-resolved, enumerated) and incorporates three Haiku elements:

1. **Haiku's 8 integration points** as a standalone appendix (not replacing Opus's inline references, but supplementing them)
2. **Haiku's range-based timeline** alongside Opus's point estimates (e.g., "~5 days (range: 3–7)")
3. **Haiku's validation checkpoints A–D** layered onto Opus's milestone structure for finer-grained progress tracking
