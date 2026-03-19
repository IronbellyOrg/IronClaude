---
convergence_score: 0.72
rounds_completed: 2
---

# Adversarial Debate: Unified Audit Gating Roadmap

## Round 1 — Initial Positions

### D2 — ToolOrchestrator Plugin Sequencing (Highest-impact divergence)

**Variant A (Opus) — Late placement (Phase 5, conditional):**
The ToolOrchestrator plugin is an optimization, not a prerequisite. The core gate must ship independently of whether the plugin lands. Placing it in Phase 5 with explicit cut criteria means the critical path — analyzer, report, gate, pipeline integration — proceeds without risk of a plugin spike blocking everything. If the plugin turns out to be complex (AST edge cases, `FileAnalysis` contract surprises), we've already shipped a working gate. The "reuse benefit" Haiku claims is speculative; the three analyzers need their own AST walks regardless because they look for different patterns. Premature coupling to `ToolOrchestrator` adds integration surface before the core is proven.

**Variant B (Haiku) — Early placement (Phase 2, leverage point):**
The plugin populates `FileAnalysis.references`, `imports`, and `exports` — data that the orphan analyzer and registry checker consume downstream. Building those analyzers without the plugin means they either duplicate AST traversal or operate on incomplete data, then get retrofitted later. Early integration lets Phases 3-6 build on richer evidence. The cut criteria exist precisely to protect the schedule: if the plugin can't be built in 1-1.5 days, defer it cleanly. But attempting it early is strictly better than attempting it late, because late placement means the report and gate phases never benefit from its output in the initial release.

---

### D1 — Phase 0: Architecture Alignment

**Variant A (Opus) — No dedicated phase:**
The spec lists 5 open questions. Opus provides proposed answers for all of them. A half-day "phase" for what amounts to a review meeting is process overhead. These decisions can be confirmed in the first day of Phase 1 implementation without losing time. The proposed defaults (glob for `audit_artifacts_used`, count excludes in `files_skipped`, etc.) are reasonable and unlikely to be overturned. If they are, the rework is localized to dataclass fields and report formatting — not architectural.

**Variant B (Haiku) — Explicit Phase 0 (0.5-1 day):**
Opus's proposed answers are reasonable but unvalidated. The question isn't whether the answers are good — it's whether the team has committed to them. Haiku identifies two additional questions Opus missed entirely: comparator/consolidator extension scope and rollout ownership for `grace_period`. Starting code without resolving these risks building the wrong thing. Phase 0 costs half a day and prevents multi-day rework cycles. The architecture decision log it produces is also a deliverable that downstream phases reference.

---

### D3 — Sprint/Roadmap Integration Bundling

**Variant A (Opus) — Bundled in Phase 3:**
Both integrations touch executor files, share the same `GateMode` contract, and are implemented by the same engineer. The sprint hook is ~30-40 LOC. Splitting this into two phases adds coordination overhead (two review cycles, two merge windows) for what is functionally one integration surface viewed from two entry points. The total work is 2-3 days either way.

**Variant B (Haiku) — Separated into Phase 4 + Phase 5:**
Sprint integration is operationally sensitive — it affects developer workflow on every task execution. Roadmap integration runs once per release cycle. These have fundamentally different blast radii. A bug in the sprint hook causes friction on every sprint task; a bug in the roadmap step causes one failed pipeline run. Separating them allows independent validation: roadmap integration can ship and stabilize before sprint integration activates. The "same engineer" argument assumes single-implementer; for team execution, separation enables parallel ownership.

---

### D4/D5 — Consolidated Validation Phase and Rollout Splitting

**Variant A (Opus) — Tests per phase, single rollout phase:**
Writing tests alongside implementation catches bugs at the lowest cost. A dedicated "validation phase" is often where projects stall — it becomes a catch-all for deferred quality work. Per-phase testing with coverage gates (90% target in Phase 2) ensures quality is continuous, not batched. The rollout phase (Phase 6) combines readiness assessment with activation because the assessment *is* the activation gate — you compute FPR/TPR and either activate or don't.

**Variant B (Haiku) — Per-phase tests PLUS Phase 7 validation PLUS Phase 8 rollout:**
Per-phase tests validate individual components. They do not validate cross-cutting concerns: retrospective known-bug detection (cli-portify), alias/re-export noise characterization, or benchmark runs under realistic load. Phase 7 covers genuinely new work that no individual phase produces. Separating "are we ready?" (Phase 7) from "activate it" (Phase 8) prevents the psychological pressure of a combined phase where readiness assessment is biased toward the activation decision. These are different cognitive tasks requiring different rigor.

---

### D6 — LOC Estimates and Task Granularity

**Variant A (Opus):**
LOC estimates, file paths, and requirement traceability per task are directly convertible to sprint tasklists. This is a roadmap's primary downstream consumer. Abstract narrative requires a translation step that introduces interpretation error.

**Variant B (Haiku):**
Narrative descriptions explain *why* decisions are made, providing context for implementers to make judgment calls when edge cases arise. LOC estimates create false precision — "60-80 LOC" is a guess that becomes a commitment. Grouping by concern rather than file enables architectural reasoning about dependencies.

---

### D12 — Agent Regression Risk Level

**Variant A (Opus) — R7 as MEDIUM:**
Agent specs are behavioral — they're Markdown read by LLMs. The extensions are strictly additive (no rules removed, no tools changed). The risk of regression from *adding* a field or classification is low. MEDIUM with "strictly additive" mitigation is proportionate.

**Variant B (Haiku) — R7 as HIGH:**
Behavioral specs are *harder* to test than code, not easier. Adding a 9th mandatory field to the analyzer could change how the LLM prioritizes the other 8 fields. Adding `REVIEW:wiring` to the scanner could shift classification distributions. These are emergent effects that unit tests don't catch. Staged independent validation of each agent and regression tests against prior audit outputs are necessary precisely because the failure mode is subtle.

---

## Round 2 — Rebuttals

### D2 — ToolOrchestrator Plugin (continued)

**Variant A rebuts Variant B:**
Haiku claims the analyzers "consume" plugin data, but the spec defines three independent detection algorithms — unwired callables use `ast.walk()` for `Optional[Callable]` annotations, orphan detection uses directory scanning against `__init__.py` imports, and registry checks use pattern matching. None of these *require* `FileAnalysis.references`. The plugin enhances the "dual evidence" rule for orphan detection (FR-017), but that's one sub-check in one analyzer. Building the entire plugin early to improve one check is poor ROI when it risks blocking three phases of work. The cut criteria prove even the spec authors considered this non-essential.

**Variant B rebuts Variant A:**
Opus conflates "required" with "valuable." The plugin isn't required for minimum viability, but it reduces false positives in orphan detection — precisely the risk (R6) both variants rate as HIGH. Early FP reduction means better shadow data, which means faster soft-mode activation. Late placement means shadow data includes noise that could have been filtered, potentially extending the observation period by an entire release cycle. The schedule risk is bounded (1-1.5 days with explicit cut criteria); the data quality risk of late placement is unbounded.

---

### D1 — Phase 0 (continued)

**Variant A rebuts Variant B:**
The two "additional questions" Haiku identifies are not blockers. Comparator/consolidator scope is explicitly scoped in the spec as additive extensions — the answer is "add wiring sections, don't restructure." Rollout ownership for `grace_period` is an operational question resolved by team assignment, not architecture. A Phase 0 that resolves non-blocking questions is process theater. If a genuinely blocking question surfaces during implementation, stopping to resolve it takes the same time whether or not Phase 0 existed.

**Variant B rebuts Variant A:**
Opus's "proposed answers" are one architect's defaults, not team decisions. The point of Phase 0 isn't that the answers are unknown — it's that they're uncommitted. In a multi-role project (Haiku identifies 4 roles), the audit workflow owner may disagree with the architect's default on whitelist strictness semantics. Resolving this during Phase 1 implementation means the backend engineer has already coded one interpretation. Phase 0 costs 0.5 days; a wrong assumption discovered in Phase 3 costs 2+ days of rework across multiple files.

---

### D3 — Bundling (continued)

**Variant A rebuts Variant B:**
Haiku's "different blast radius" argument assumes bugs ship to production. Both integrations deploy in shadow mode — the sprint hook logs findings without affecting task status. The blast radius in shadow is identical: a log line. Separating them for "independent validation" is only meaningful if shadow mode isn't the first deployment target, which both variants agree it is.

**Variant B rebuts Variant A:**
Shadow mode reduces blast radius for *findings*, not for *integration bugs*. A malformed sprint hook could throw exceptions, corrupt task state, or add latency to every task execution — none of which are mitigated by shadow mode. The sprint executor is a hot path; the roadmap executor runs infrequently. Testing the sprint hook in isolation before merging it with the roadmap integration reduces the chance of a sprint-blocking regression that's masked by the roadmap integration's test coverage.

---

### D4/D5 — Validation and Rollout (continued)

**Variant A rebuts Variant B:**
The "genuinely new work" in Phase 7 — retrospective validation, noise characterization — can be tasks within Phase 6 without needing a dedicated phase. A phase boundary implies a review gate, merge window, and coordination overhead. The cli-portify retrospective is a single test case. Noise characterization is a shadow-mode analysis task. Neither justifies phase-level granularity. As for separating readiness from activation: the FPR/TPR thresholds are numeric. There's no "psychological pressure" — either `measured_FPR + 2σ < 15%` or it doesn't.

**Variant B rebuts Variant A:**
Numeric thresholds don't eliminate judgment. The question isn't just "does FPR meet the threshold?" but "is the measurement methodology sound, is the sample representative, are there confounders?" A dedicated readiness phase forces these questions to be asked and documented before anyone touches the activation config. Opus's combined phase creates a natural incentive to rationalize marginal data ("close enough, let's activate") because the next action is right there. Separation enforces deliberation.

---

## Convergence Assessment

### Areas of Agreement (Strong Convergence)

1. **Core engine first**: Both agree the analyzer, dataclasses, and AST primitives must be built and validated before any integration work. No dispute on Phase 1 content or sequencing.

2. **Gate contract compliance**: Both agree the report must pass `gate_passed()` unchanged, with identical frontmatter fields and semantic checks. No dispute on the gate definition.

3. **Shadow-first rollout**: Both agree shadow mode is mandatory before any blocking enforcement, with statistical gates for phase transitions. Identical thresholds.

4. **Agent extensions are additive-only**: Both agree NFR-013 is non-negotiable. Dispute is on risk *level*, not risk *existence*.

5. **ToolOrchestrator has cut criteria**: Both agree the plugin is deferrable. Dispute is on *when to attempt it*, not whether it's optional.

6. **Merge coordination needed**: Both identify `roadmap/gates.py` as a contention point requiring sequencing.

### Areas of Partial Convergence

7. **Phase 0 can be compressed**: Opus's proposed answers + Haiku's broader question set could yield a lightweight "decision review" (2-4 hours) rather than a full phase-day. This satisfies Haiku's commitment concern without Opus's process overhead objection.

8. **Per-phase testing is necessary but not sufficient**: Both agree tests should be written alongside implementation. The dispute is whether a final validation sweep adds value. A compromise: include retrospective validation and noise characterization as Phase 6 tasks rather than a separate phase, but require explicit sign-off before activation.

### Remaining Disputes (Low Convergence)

9. **ToolOrchestrator timing (D2)**: This remains the most consequential unresolved disagreement. The tradeoff is real: early placement improves data quality but risks schedule; late placement protects schedule but accepts noisier shadow data. A timeboxed spike (as the diff analysis suggests) is the only resolution that satisfies both perspectives.

10. **Sprint/roadmap separation (D3)**: Haiku's point about integration bugs (vs. finding bugs) in the sprint hot path is substantive and not fully addressed by Opus's shadow-mode rebuttal. This leans toward separation unless a single implementer owns both surfaces.

11. **Phase count and granularity (D7)**: Fundamentally a team-size and coordination-model question. Solo implementer favors Opus's 6 phases; multi-role team favors Haiku's 9. Neither is objectively superior without knowing the team structure.

12. **R7 risk level (D12)**: Haiku's argument about emergent LLM behavioral effects from spec changes is technically sound but empirically unvalidated. The pragmatic resolution is: implement Haiku's staged validation approach (the mitigation) while keeping Opus's MEDIUM rating (the assessment), since the mitigation matters more than the label.
