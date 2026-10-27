---
convergence_score: 0.72
rounds_completed: 2
---

# Adversarial Debate: Opus Architect vs. Haiku Architect

## Round 1 — Initial Positions

### D1: Phase 0 — Baseline Verification

**Variant A (Opus):** Phase 0 is unnecessary overhead. The baseline is commit `f4d9035` — it's a git hash, not an ambiguity. Interface contracts can be defined inline in Phase 1 as they're needed. Adding 2-3 days of "verification" before writing any code is a planning trap: you learn more by building the parser than by documenting what you think the parser should do. The acceptance-test matrix is useful but belongs in Phase 6 where it's validated, not Phase 0 where it's speculative.

**Variant B (Haiku):** Building without verifying assumptions is how projects accumulate 2-week rework cycles. Phase 0 costs 2-3 days; discovering in Phase 5 that your interface contract doesn't match TurnLedger's actual API costs 5-10 days. The interface lock (M0.1) is specifically about FR-7.1 — the `handle_regression()` contract that bridges convergence and regression. If you get that wrong, Phase 3 and Phase 5 both need rework. The acceptance-test matrix (M0.3) isn't speculative — it's the definition of done that prevents scope creep during implementation.

---

### D2/D3: Phase Count, Registry-Convergence Coupling

**Variant A (Opus):** Six phases with coarser boundaries deliver faster. Bundling the registry with convergence in Phase 3 is pragmatic — the registry exists *to serve* convergence. Testing it in isolation proves it works in a vacuum; testing it under convergence proves it works in reality. The finer you decompose, the more inter-phase handoff overhead you create. For a single developer (the likely staffing model), 8 phases means 8 context switches and 8 sets of exit criteria to satisfy before moving on.

**Variant B (Haiku):** The registry serves convergence, but it also serves remediation (SC-3), run-to-run memory (FR-10), and regression detection (FR-8). Validating it independently means those three downstream consumers can trust it. When Opus bundles registry + convergence + TurnLedger + legacy dispatch + FR-7.1 into one phase, a registry bug discovered during convergence wiring forces you to debug across all five concerns simultaneously. Separation costs a phase boundary; bundling costs debugging time that is harder to predict. Even for a single developer, isolated validation reduces cognitive load per phase.

---

### D4: Semantic-Before-Convergence vs. Convergence-Before-Semantic

**Variant A (Opus):** The convergence engine is a control loop — it doesn't care what produces findings, only that findings arrive with stable IDs and severity levels. Building the convergence shell first (Phase 3) means the semantic layer (Phase 4) plugs into an already-tested loop. If semantic output format needs adjustment, you adjust the semantic layer to match the loop, not the other way around. The loop is simpler and should be stabilized first.

**Variant B (Haiku):** The convergence engine consumes semantic findings, passes them to the registry, and makes pass/fail decisions based on their severity. If you build the convergence shell before the semantic layer exists, you're testing it with mock findings. When real semantic findings arrive with debate verdicts and source-layer tags, you discover integration gaps. Building registry → semantic → convergence means each layer is validated with real outputs from its predecessor. Mock-based testing was explicitly rejected in this project's memory.

---

### D5: FR-10 Run-to-Run Memory Placement

**Variant A (Opus):** FR-10 is placed in Phase 4 because the semantic prompt is its primary consumer. The prompt builder needs prior findings to construct context. Building run-to-run memory alongside the semantic layer means you can test the full prompt construction pipeline — memory retrieval, truncation at 50 findings, and prompt budget interaction — in one phase.

**Variant B (Haiku):** Run-to-run memory is a registry capability, not a semantic capability. The registry tracks `first_seen_run` and `last_seen_run`. It stores and retrieves prior findings. The semantic layer merely *reads* this data. Placing FR-10 in Phase 3 with the registry means the data layer is complete before any consumer depends on it. It also means convergence (Phase 5 in Haiku) has memory available from day one, not retroactively wired in.

---

### D6: Data Model Front-Loading

**Variant A (Opus):** Defining `SEVERITY_RULES`, extending `Finding`, and creating `RunMetadata` in Phase 1 prevents downstream churn. Every checker in Phase 2 needs `Finding` extensions. The registry in Phase 3 needs `RunMetadata`. Front-loading these definitions means Phases 2-3 consume stable interfaces rather than defining them ad-hoc. The data model is the contract between phases; it should be established early.

**Variant B (Haiku):** Front-loading data models couples Phase 1 to downstream design decisions that haven't been validated yet. If Phase 2 checker development reveals that `Finding` needs an additional field, Phase 1's model is wrong. Just-in-time definition means models evolve with their consumers. Phase 1 stays focused on parsing (FR-2 + FR-5), which is complex enough to warrant full attention.

---

### D7: Timeline

**Variant A (Opus):** 32 days is aggressive but achievable for a developer familiar with the codebase. ~60% of infrastructure is pre-built from v3.0. Point estimates signal commitment and create urgency. Range estimates invite padding — "36-49 days" means 49 days in practice.

**Variant B (Haiku):** Ranges acknowledge uncertainty honestly. Phases involving LLM integration (semantic layer, debate protocol, convergence with remediation) have inherently variable timelines. 32 days assumes zero rework, zero blocked dependencies, and zero parser surprises on real specs. The range of 36-49 days reflects that some phases compress (parser may be fast) while others expand (debate calibration may be slow). Honest estimates build trust; point estimates build pressure.

---

### D8/D10/D11/D12/D14: Operational Structure

**Variant A (Opus):** Implementation density beats organizational overhead. Named milestone gates, staffing models, architect emphasis blocks, and ID preservation guidance are project management artifacts, not engineering artifacts. A roadmap should tell you *what to build* and *in what order*. Opus provides function names, cost constants, field lists, and file-level specificity — ready for direct implementation. The implementer doesn't need a "why" block; they have the spec.

**Variant B (Haiku):** A roadmap that only says "what" without "why" produces implementations that satisfy the letter of each requirement while violating their intent. Architect emphasis blocks prevent judgment errors at decision points the spec doesn't cover. Named gates (A-F) with SC-linked exit criteria give stakeholders clear go/no-go checkpoints. ID preservation guidance prevents requirement drift over a 36-49 day project. These aren't overhead — they're the difference between a roadmap that survives contact with reality and one that becomes stale by Phase 3.

---

## Round 2 — Rebuttals

### Opus Rebuts Haiku

**On Phase 0:** Haiku claims Phase 0 prevents rework, but interface contracts defined before implementation are hypotheses, not contracts. The FR-7.1 interface — `handle_regression() → RegressionResult` — is already fully specified in the requirements document. "Locking" it in Phase 0 adds no information. If TurnLedger's API doesn't match expectations, you discover that the moment you write the import in Phase 3 — with or without Phase 0. The acceptance-test matrix is valuable but is a 2-hour task, not a 2-3 day phase.

**On Registry Separation:** Haiku argues the registry serves multiple consumers, but in practice, those consumers are built in sequence. The registry is never used by remediation *without* going through convergence first. Testing the registry under convergence is testing it under its actual operating conditions. Haiku's "isolated validation" tests the registry in conditions it never experiences in production.

**On Mock-Based Testing Concern:** Haiku invokes the project memory about real evals, but this applies to *final validation*, not intermediate development. Building the convergence shell with mock findings during development, then validating with real findings in integration, is standard practice. The memory says "evals must invoke actual CLI pipeline" — that's Phase 6/7, not Phase 3.

**On Timeline:** Haiku's 36-49 day range has a 36% spread. That's not honesty; that's imprecision. If you can't estimate tighter than ±36%, you don't understand the scope well enough. The right response to uncertainty is to decompose further, not to widen the range.

### Haiku Rebuts Opus

**On Data Model Front-Loading:** Opus front-loads `SEVERITY_RULES` in Phase 1, but the severity rules depend on the 5 checker dimensions (Phase 2) and 19 mismatch types that emerge from implementing the checkers. Defining the rule table before implementing what it classifies is premature. If checker development reveals a 20th mismatch type, Phase 1's "stable" model needs revision. Front-loading creates the illusion of stability.

**On Implementation Density:** Opus's function names and cost constants are impressive detail, but detail is not the same as correctness. Specifying `CHECKER_COST=10` before the convergence engine exists assumes the cost model is right. If convergence testing reveals that checker cost should be 15 (because checkers are more expensive than estimated), every downstream budget calculation is wrong. Haiku's approach — define constants when the consuming system is built — avoids premature commitment.

**On Convergence Shell First:** Opus says the convergence engine "doesn't care what produces findings." But it does care about `source_layer` tags, because monotonic progress checks apply only to structural HIGHs. It cares about debate verdicts, because they change severity. Building the shell before the semantic layer means building the shell's conditional logic (`if source_layer == "semantic"`) without the system that produces semantic findings. That's speculative branching.

**On Phase 0 Duration:** Opus calls Phase 0 a "2-hour task." If interface verification, baseline confirmation, and acceptance-test mapping are 2 hours, then Phase 0 is 2 hours, not 2-3 days. But Opus's own Phase 1 includes data model work that Haiku puts in Phase 0 — the time isn't saved, it's relocated. The question is whether "verify then build" or "build then verify" catches errors cheaper. For interface contracts consumed by 4 downstream phases, early verification is cheaper.

**On Timeline Precision:** A 36% spread is honest because the semantic and debate phases have genuine uncertainty. Opus's 32-day point estimate for a system involving LLM integration, adversarial debate calibration, and multi-agent regression validation assumes no phase takes longer than planned. Any project manager who has shipped LLM-dependent features knows that "same inputs, consistent outputs" (SC-1) is harder to achieve than it sounds. Point estimates on LLM work are aspirational, not predictive.

**On Risks 7-8:** Opus deserves credit for surfacing pre-v3.05 registry migration and convergence pass credit asymmetry as distinct risks. Haiku subsumes these into open questions where they receive less visibility. This is a genuine gap in Haiku's risk treatment.

---

## Convergence Assessment

### Areas of Agreement

1. **Critical path is settled:** FR-2 → FR-1 → FR-4 → FR-7. No dispute.
2. **Registry before convergence:** Both agree the registry must be functional before the convergence engine consumes it. They differ on *how much* before.
3. **Real-spec validation is non-negotiable:** Both require parser testing against the actual spec, not synthetic fixtures.
4. **Risk 7-8 should be visible:** Haiku concedes these deserve explicit tracking, not burial in open questions.
5. **Architect emphasis adds value for multi-developer teams but is overhead for solo execution:** The right level of documentation depends on staffing, which is a project decision, not an architectural one.

### Remaining Disputes (Unresolved)

1. **Phase 0: 2-3 days or collapse into Phase 1?** Opus sees it as overhead; Haiku sees it as insurance. The resolution depends on team confidence in existing interface knowledge — if the team has recently worked with TurnLedger and the registry, Phase 0 can compress to hours. If not, it's worth days.

2. **Registry+Convergence bundling vs. separation.** Opus optimizes for speed; Haiku optimizes for debuggability. For a single experienced developer, Opus's bundling is likely fine. For a team or a developer new to the codebase, Haiku's separation is safer. Neither is architecturally wrong.

3. **FR-10 placement.** Haiku's argument (registry concern, not semantic concern) is architecturally stronger. Opus's argument (test alongside consumer) is pragmatically valid. The merge should favor Haiku's placement with Opus's testing approach — build memory in the registry phase, validate it end-to-end in the semantic phase.

4. **Data model timing.** Genuinely unresolvable without knowing whether the 19 mismatch types are stable. If the spec is authoritative on mismatch types, front-loading is correct. If checker implementation may reveal new types, just-in-time is safer.

5. **Timeline.** 32 days is achievable best-case; 36-49 is the realistic range. The merge should use Opus's phase structure with Haiku's range estimates.

6. **Semantic-before-convergence ordering.** Haiku's argument about `source_layer` conditional logic is substantive. Building convergence logic that branches on semantic tags before the semantic system exists invites untested code paths. This favors Haiku's ordering: registry → semantic → convergence.
