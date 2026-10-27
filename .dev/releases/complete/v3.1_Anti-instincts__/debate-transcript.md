---
convergence_score: 0.82
rounds_completed: 2
---

# Adversarial Debate: Opus-Architect (A) vs Haiku-Architect (B)

## Round 1: Initial Positions

### D-01/D-02: Phase Count and Architecture Lock

**Variant A (Opus):**
Four phases is the right granularity. An experienced implementer doesn't need a formal "Phase 0" to resolve open questions — they resolve them as they encounter them during Phase 1. Adding a half-day architecture lock phase creates ceremony without substance. The open questions (OQ-003, OQ-004, OQ-005) have clear recommended resolutions already documented inline. A solo implementer reads the recommendation, confirms or adjusts, and moves on. Phase 0 is project management theater for a feature with a single critical path.

**Variant B (Haiku):**
Phase 0 exists precisely because "resolve as you go" is how mid-implementation pivots happen. OQ-005 (D-03/D-04 coexistence) affects the entire sprint integration architecture. OQ-010 (downstream validation of prompt-required structure) determines whether Phase 2 prompt work has any enforcement teeth. Discovering halfway through Phase 2 that your coexistence decision was wrong costs more than 0.5 days. Phase 0 is cheap insurance. The fact that Opus already has "recommended resolutions" proves the decisions are identifiable — it just refuses to formalize the commitment.

---

### D-03: Timeline Units

**Variant A (Opus):**
Sprint-based estimates align with how this project actually ships. The sprint is the deployment and validation unit. Saying "2–3 sprints" for Phase 1 communicates that this is multiple iteration cycles of build-test-refine, not a continuous coding block. Day-based estimates give false precision — "2–3 days" for four analyzer modules with comprehensive tests is aggressive and likely to slip.

**Variant B (Haiku):**
"Sprint" without defining sprint length is meaningless for planning. Is a sprint 1 day? 3 days? A week? Opus's "6–10 sprints" total range is so wide it's barely an estimate. Day-based estimates force the roadmap author to commit to actual scope. If "2–3 days" for Phase 1 feels aggressive, that's useful information — it means the scope needs scrutiny. Ambiguous estimates hide scope problems.

---

### D-04: Prompt Changes Placement

**Variant A (Opus):**
Prompt changes and gate wiring are a single logical unit. The prompts tell the LLM to produce structure; the gate checks that structure exists. Shipping them together means you can validate the full loop in one integration test cycle. Separating them creates an intermediate state where prompts are updated but the gate checking the prompted output doesn't exist yet — or vice versa. That's a configuration hazard.

**Variant B (Haiku):**
Prompt changes are probability reducers, not enforcement mechanisms — Haiku's own architect recommendation #3 says this explicitly. They deserve independent review because bad prompt wording causes subtle downstream effects that are hard to debug when bundled with gate logic. Isolating Phase 3 means you can validate prompt output quality independently before the gate evaluates it. The "intermediate state" concern is theoretical — prompts that request better structure never make output worse.

---

### D-05: Parallelization

**Variant A (Opus):**
Strict phase sequencing is safer. Phase 1 modules are internally parallelizable — that's where the real time savings are. Cross-phase parallelization between Phase 1 analyzers and Phase 3 prompt changes introduces a subtle coupling: prompt changes affect what the LLM generates, which affects what the analyzers need to detect. If you change prompts while building analyzers, you're building against a moving target.

**Variant B (Haiku):**
The coupling is indirect and manageable. Prompt changes request explicit structure (named wiring sections, integration enumeration). Analyzers detect the absence of that structure. Building both simultaneously is safe because they converge on the same structural expectations. The real parallelization win is unit tests alongside module coding — that's uncontroversial and saves 0.5–1 day. Opus explicitly rules out all cross-phase parallelism, which is unnecessarily conservative.

---

### D-08: `off` Mode Semantics

**Variant A (Opus):**
`off` means off. Zero computation. Zero overhead. Zero risk. If you want metrics collection, use `shadow` — that's literally what shadow mode is for. Haiku's "off but still evaluating for metrics policy" blurs the semantics and makes `off` a misnomer. An operator setting `off` expects no gate code to execute. Violating that expectation is a trust problem.

**Variant B (Haiku):**
`off` meaning "no behavior change" is distinct from `shadow` meaning "actively recording metrics for promotion decisions." The `off` mode evaluation is conditional — only if a metrics policy requires it. This allows background data collection without any sprint behavior change, accelerating the time to shadow promotion. The distinction matters for operators who want to collect baseline data before formally entering shadow mode. `shadow` implies intentional observation; `off` with conditional metrics is passive.

---

### D-09: Validation Strategy Structure

**Variant A (Opus):**
Phase-aligned testing is simpler to execute and verify. When you finish Phase 1, you run Phase 1 tests. When you finish Phase 2, you run Phase 2 tests. The validation mirrors the build sequence. Cross-cutting taxonomies look clean in a document but create ambiguity about when tests should run and what they block.

**Variant B (Haiku):**
Cross-cutting taxonomy (A: unit, B: integration, C: sprint-mode, D: regression, E: non-functional) exists for coverage analysis, not execution ordering. You still run tests phase by phase — but the taxonomy lets you verify that all five validation dimensions are covered across all phases. Phase-aligned testing makes it easy to miss that you never wrote a non-functional latency test for Phase 3 prompt changes because "Phase 3 tests" doesn't decompose by type.

---

## Round 2: Rebuttals

### A rebuts B on Phase 0

**Variant A:**
Haiku argues Phase 0 prevents mid-implementation pivots, but every OQ in the Opus roadmap already has a recommended resolution with rationale. The decisions aren't unresolved — they're documented with defaults. A formal architecture lock adds latency and creates a false sense of completeness. What actually prevents pivots is good defaults with escape hatches, not committee sign-off. If the solo implementer encounters a case where the default is wrong, they adjust — that's faster than pre-committing to a decision without implementation evidence.

**Variant B responds:**
"Good defaults" only work for a solo implementer who wrote the defaults. OQ-005 (coexistence) affects whether the sprint executor runs one gate or two. That's not a "adjust as you go" decision — it's a structural choice that determines file organization, test strategy, and operator documentation. Opus's recommended resolution (Option B, defense-in-depth) is probably right, but "probably right" should become "confirmed right" before code is written. The cost is half a day. The risk of not doing it is rework across Phases 2 and 3.

---

### B rebuts A on Timeline Units

**Variant B:**
Opus claims sprint-based estimates communicate iteration cycles, but the diff analysis identifies the core problem: "Opus's 6–10 sprints vs Haiku's 8–12 days suggest fundamentally different scope interpretations unless Opus sprints are 1-day sprints." If Opus sprints are multi-day, the total estimate is 2–5x larger than Haiku's. If they're 1-day sprints, they're just days with extra words. Either way, the unit doesn't communicate clearly.

**Variant A responds:**
Fair criticism on the unit ambiguity. However, Haiku's day estimates assume continuous focused development time, which is rarely available. Sprint-based estimates account for context switching, review cycles, and integration overhead. The actual calendar time will be closer to Opus's range regardless of which unit you use. That said, defining sprint length explicitly would resolve this — recommend adding "1-day sprint" clarification.

---

### A rebuts B on `off` Mode

**Variant A:**
Haiku's conditional metrics in `off` mode creates a hidden dependency: now `off` mode requires the metrics infrastructure to be initialized and functional. If `ShadowGateMetrics` has a bug, `off` mode is affected. True `off` means the gate code path is never entered. This is the simplest, safest, most debuggable semantics. The acceleration benefit of passive data collection is marginal — shadow mode is one config change away.

**Variant B responds:**
The implementation cost of conditional metrics in `off` is one `if` statement. The initialization concern is valid but addressable with lazy initialization. The real question is operational: how long does it take to accumulate 5 sprints of shadow data? If passive collection in `off` mode shaves 2 sprints off that window, it's worth the one `if` statement. But this is a judgment call, not a structural disagreement.

---

### B rebuts A on Prompt Bundling

**Variant B:**
Opus argues prompts and gates are "a single logical unit," but this conflates two different concerns: (1) what the LLM is asked to produce and (2) what the deterministic gate checks. The gate checks frontmatter values written by the executor, not raw LLM output. The prompt affects LLM output quality, which affects whether the executor's analysis produces passing frontmatter values. These are related but separable. Independent prompt review catches wording issues that would cause systematic false negatives across all future gate evaluations.

**Variant A responds:**
The separation is technically valid but practically unnecessary for this scope. There are exactly two prompt additions — one block and one dimension. They can be reviewed in the same PR as the gate wiring. If there were dozens of prompt changes or if prompts needed stakeholder review beyond the implementer, separation would make sense. For two additions by the same engineer, bundling is more efficient.

---

## Convergence Assessment

### Areas of Agreement (Strong Convergence)

1. **Core technical approach**: Both agree on identical modules, dataclasses, file structure, gate semantics, and rollout mode enum. Zero divergence on what gets built.

2. **Defense-in-depth for D-03/D-04**: Both recommend Option B (independent evaluation). Confirmed.

3. **Shadow validation before enforcement**: Both require 5+ sprints at ≥0.90 pass rate. No dispute.

4. **Phase 1 internal parallelism**: Both agree the four analyzer modules can be built concurrently. Opus just didn't extend parallelism further.

5. **Backward compatibility**: Both enforce `gate_passed()` signature preservation and zero existing test breakage.

6. **Prompt changes as support, not enforcement**: Both explicitly state deterministic checks are authoritative.

### Areas of Partial Convergence

7. **Phase 0**: Opus concedes OQ-005 should be resolved before sprint integration (Phase 3), but argues it doesn't need a formal phase. Compromise: resolve OQ-005 and OQ-010 as a pre-implementation task within Phase 1's first day, without creating a separate phase. This captures Haiku's risk reduction without Haiku's ceremony.

8. **Timeline units**: Opus acknowledges the ambiguity. Compromise: use day-based estimates for build phases, sprint-based for observation phases. This matches Haiku's approach.

9. **Prompt bundling**: Both agree the scope is small (2 additions). Opus's bundling is acceptable for this scope; Haiku's separation is acceptable for reviewability. Low-stakes divergence — implementer's choice.

10. **Cross-phase parallelism**: Both agree unit tests can parallel module coding. Dispute is limited to whether Phase 1 analyzers can overlap with Phase 3 prompts. Mild risk, mild reward — implementer's judgment call.

### Remaining Disputes (Low Convergence)

11. **`off` mode semantics (D-08)**: Genuine design disagreement. Opus's "zero computation" is simpler and safer. Haiku's "conditional metrics" is more operationally flexible. This needs a spec-level decision, not a roadmap-level resolution. **Recommend: adopt Opus's strict `off` semantics for v3.1; revisit passive collection as a v3.2 enhancement if shadow ramp-up proves slow.**

12. **Validation taxonomy**: Haiku's cross-cutting taxonomy (A–E) is strictly more informative than Opus's phase-aligned approach, with no implementation cost. **Recommend: adopt Haiku's taxonomy as a documentation overlay on Opus's phase-aligned execution order.**

### Synthesis Recommendation

The merged roadmap should use **Opus's 4-phase structure** (avoiding Phase 0 ceremony) with **Haiku's additions**: requirement coverage matrix, cross-cutting validation taxonomy, resource/staffing section, explicit checkpoints (A/B/C), and day-based timeline estimates for build phases. Adopt Opus's strict `off` semantics. Resolve OQ-005 and OQ-010 as day-1 tasks within Phase 1, not as a separate phase.
