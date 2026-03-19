---
convergence_score: 0.78
rounds_completed: 3
---

# Adversarial Debate: Wiring Verification Gate v3.0 Roadmap

**Variant A**: Opus Architect (task-oriented, implementation-first)
**Variant B**: Haiku Architect (governance-oriented, architecture-first)

**Shared foundation**: 18 shared assumptions confirmed across both variants. Debate focuses on the 12 divergence points identified in diff analysis.

---

## Round 1: Initial Positions

### D01 — Phase 0: Architecture Confirmation

**Variant A (Opus):**
Phase 0 is unnecessary overhead. The open questions are enumerable and concrete — `provider_dir_names`, `ToolOrchestrator` seam inspection, merge coordination. These are resolvable in a focused 30-minute investigation at the start of T01, not a dedicated phase. Adding a phase-unit of calendar time before any code ships delays value delivery. The spec already identifies exactly what needs resolution and when each question blocks. Treating "confirm assumptions" as a separate phase implies the team doesn't trust the spec — but the spec is already merged and validated through adversarial review.

**Variant B (Haiku):**
Phase 0 is cheap insurance against expensive rework. This initiative touches roadmap execution, sprint enforcement, gate evaluation, audit tooling, and agent extensions simultaneously. A single misaligned assumption — say, `ToolOrchestrator.__init__()` lacking the `analyzer` param — discovered in Phase 3 would cascade into rework across T06, T10–T12, and potentially T08's special-casing logic. Phase 0 costs 0.5–1 phase-unit. Rework from a misaligned seam costs 2–4 phase-units. The ROI is obvious. Furthermore, Phase 0 assigns *owners* to open questions — without that, questions linger because nobody is accountable.

---

### D02 — Phase Structure: 6 vs 7 Phases

**Variant A (Opus):**
Six phases with bundled roadmap+sprint integration (Phase 3, T07–T09) minimizes phase transition overhead. Sprint integration (T09) directly depends on the same `WIRING_GATE` and core analyzer that roadmap integration uses. Separating them into distinct phases creates an artificial boundary — the implementer will naturally build T09 immediately after T08 because the context is warm. Fewer phases = fewer handoff points = fewer places for momentum to stall.

**Variant B (Haiku):**
Seven phases (including Phase 0) with separated roadmap (Phase 3) and sprint (Phase 4) integration provides three concrete benefits: (1) Phase 4 can begin once Phase 1 stabilizes, enabling parallel work before roadmap integration is complete. (2) Sprint integration has distinct performance requirements (<2s) and a distinct control surface (`SprintConfig`) — bundling it with roadmap work obscures these differences. (3) Separated phases give project managers cleaner milestone boundaries for tracking. The "warm context" argument assumes a single implementer in a single session, which may not hold.

---

### D03 — Task Granularity: IDs vs Narrative

**Variant A (Opus):**
T01–T15 with file paths, CREATE/MODIFY annotations, and a dependency DAG is directly consumable by the sprint CLI tasklist generator. This is a roadmap for *execution*, not a PowerPoint for stakeholders. Every task has explicit inputs, outputs, and blockers. The dependency DAG enables automated parallelism detection. Narrative descriptions are pleasant to read but unusable for automated tooling.

**Variant B (Haiku):**
Milestones (M1.1–M1.5, M2.1–M2.3, etc.) provide richer progress decomposition. A task ID tells you what to build; a milestone tells you what "done" looks like at each checkpoint. Both are needed. The narrative format also communicates *architectural rationale* alongside deliverables — why the report emitter separates from the analyzer, why semantic checks must be pure. Task IDs without rationale produce implementers who follow instructions without understanding constraints, leading to subtle violations.

---

### D04 — File Layout: Up-front vs Deferred

**Variant A (Opus):**
Committing to `audit/wiring_config.py` as a separate file for `WiringConfig` is a clear, testable decision. Config is loaded once, referenced everywhere, and has its own validation logic (whitelist loading, `provider_dir_names` defaults). Separating it from `wiring_gate.py` follows single-responsibility and makes unit testing config validation independent of analysis logic. Deferring file layout decisions just means making them later with less time and more pressure.

**Variant B (Haiku):**
Deferring file-level layout to Phase 0 is consistent with architecture-first philosophy. The right module boundary depends on how `WiringConfig` actually interacts with `WiringReport` and `WiringFinding` — if config validation needs to reference finding types, a separate file creates circular import risk. Phase 0's job is precisely to confirm these boundaries with evidence from the actual codebase, not from abstract design principles.

---

### D05 — Report Body Section Enumeration

**Variant A (Opus):**
The spec defines the report contract. The roadmap's job is to sequence implementation, not re-specify the artifact. Enumerating all 7 body sections in the roadmap is redundant with the spec and creates a maintenance burden — if the spec changes a section name, the roadmap must also be updated.

**Variant B (Haiku):**
The roadmap is the implementer's primary reference during coding. Requiring them to cross-reference the spec for section names during `emit_report()` implementation adds friction and error risk. Listing the 7 sections costs 7 lines and eliminates ambiguity. The maintenance concern is theoretical — the spec is locked before implementation begins.

---

### D06 — Whitelist Error Escalation

**Variant A (Opus):**
Strict validation from day one. A malformed whitelist entry is a configuration error. Logging a warning and continuing means the implementer might not notice the error during development, leading to silent data quality issues. Fail fast, fix fast.

**Variant B (Haiku):**
Phase-aware escalation (warn in Phase 1, error in Phase 2+) is operationally mature. During initial development, the whitelist format is still being defined — strict errors would block iteration on the whitelist schema itself. Once the schema stabilizes (Phase 2+), strict validation is appropriate. This is standard practice for configuration systems under active development.

---

### D07–D09 — SprintConfig Type, Staffing, Operational Dependencies

**Variant A (Opus):**
D07: The type system is an implementation detail, not a roadmap concern. D08: A staffing model for 4 engineers is irrelevant when the implementer is a Claude Code session. D09: Operational dependencies like "whitelist governance owner" are organizational concerns that belong in a project plan, not a technical roadmap.

**Variant B (Haiku):**
D07: `Literal["off", "shadow", "soft", "full"]` with explicit `"off"` is a design decision, not an implementation detail — it determines the API contract. D08: Even in a single-implementer scenario, the staffing model communicates which *expertise domains* are involved, helping the implementer context-switch appropriately. D09: Operational dependencies that block rollout belong in the roadmap because they're on the critical path to value delivery. A technically complete gate that can't be promoted because nobody owns whitelist governance delivers zero value.

---

### D10–D12 — Risk Framework, Deliverable Framing, Critical Path

**Variant A (Opus):**
D10: A compact risk table with Impact/Mitigation is directly actionable. A 4-layer meta-framework is academic overhead. D11: "Shadow mode is the primary deliverable" is a crisp, unambiguous statement of scope. D12: Task-level critical path (T01→T02→T03→T05→T08) tells the implementer exactly what to work on next.

**Variant B (Haiku):**
D10: The 4-layer model (Prevent→Detect→Contain→Recover) ensures no risk mitigation category is overlooked — it's a checklist, not academic theory. D11: "Controlled architecture rollout" frames v3.0 correctly for stakeholders who might otherwise expect enforcement on day one. D12: Phase-level critical path with explicit parallelism opportunities (Phase 4 after Phase 1) is more useful for scheduling than a task chain that doesn't show parallel tracks.

---

## Round 2: Rebuttals

### Variant A rebuts Variant B

**On Phase 0:** Haiku claims rework from misaligned seams costs 2–4 phase-units. But the *specific* open questions are already identified. Inspecting `ToolOrchestrator.__init__()` takes 5 minutes with a `grep`. Confirming `provider_dir_names` takes one directory listing. These are not architectural mysteries requiring a dedicated phase — they're concrete lookups. The risk of "lingering questions without owners" is solved by the open question priority table in Section 4, which assigns blocking relationships. Phase 0 solves a coordination problem that doesn't exist for a single-implementer workflow.

**On separated phases:** Haiku's argument that Phase 4 can start after Phase 1 is theoretically true but practically irrelevant. Sprint integration (T09) is a single task that adds `wiring_gate_mode` to `SprintConfig` and hooks the analyzer into post-task flow. It takes one session. Creating a separate phase for one session of work adds organizational overhead without enabling meaningful parallelism.

**On narrative milestones:** Milestones are useful for tracking but they're orthogonal to task IDs. The Opus variant's tasks *include* milestones (M1–M5). The difference is that Opus's milestones are tied to concrete deliverables (M1: "`run_wiring_analysis()` returns correct `WiringReport` for test fixtures") rather than sub-numbered checkpoints on narrative paragraphs. Both formats can coexist — the question is which is the primary organizational unit.

**On operational dependencies:** Haiku surfaces valid concerns (whitelist governance, promotion ownership) but locating them in the roadmap conflates *what to build* with *how to deploy*. A roadmap that includes staffing models and governance ownership becomes a project plan — a different document with a different audience. The roadmap should remain focused on technical sequencing.

### Variant B rebuts Variant A

**On Phase 0 cost:** Opus dismisses Phase 0 as "overhead" but the cost is 0.5–1 phase-unit — less than a single implementation phase. The return is *certainty* that all architectural seams hold before committing to file layouts, import structures, and API shapes across 7 new files. Opus's own roadmap recommends "Resolve Open Question #7 early" and "Resolve Open Question #1 before T01" — that *is* Phase 0 work, just without the discipline of a named phase and explicit exit criteria. Naming it makes it accountable.

**On bundled integration:** Opus argues sprint integration is "one session of work." But the diff analysis identifies distinct concerns: `SprintConfig` type design (D07), performance requirements (<2s), governance compatibility, and per-task artifact emission. These are not trivial additions — they're design decisions that benefit from being evaluated after the core analyzer is validated, not rushed as the tail end of roadmap integration. Bundling them risks sprint-specific concerns being treated as afterthoughts.

**On task IDs as primary unit:** Opus's T01–T15 are excellent for sprint tooling but they encode *one particular decomposition*. If Phase 0 reveals that `WiringConfig` should not be a separate file (D04), the entire T01/T02 split changes. Task IDs create rigidity. Phases with milestones create structure while preserving flexibility to adjust decomposition based on what's learned. The final tasklist should be generated *after* architectural decisions are locked, not before.

**On scope of the roadmap:** Opus argues operational dependencies belong in a "project plan, not a roadmap." But in practice, roadmaps that ignore deployment prerequisites produce technically complete features that sit unshipped. The wiring gate in shadow mode is useless without a telemetry collection process. The promotion to soft mode is blocked without a governance owner. These are first-class delivery risks, not administrative footnotes.

---

## Round 3: Concessions and Remaining Disagreements

### Variant A concessions

1. **Phase 0 as lightweight gate**: A named checkpoint (not a full phase) before T01 to confirm `provider_dir_names`, inspect `ToolOrchestrator` seam, and assign governance owners is reasonable. It should be timeboxed to one session maximum and should not delay T01 if the answers are available.

2. **Report body sections**: Including the 7 section names in the roadmap costs nothing and eliminates a cross-reference step. Conceded.

3. **`Literal["off", "shadow", "soft", "full"]`**: The explicit `"off"` mode is a genuine design decision that should be in the roadmap, not deferred to implementation. Conceded.

4. **Operational dependencies as appendix**: Whitelist governance and promotion ownership are legitimate delivery prerequisites. They can be included as an appendix or "deployment readiness" section without inflating the core phase structure.

### Variant B concessions

1. **Task IDs are necessary for tooling**: The sprint CLI requires formal task identifiers. Phase narratives alone are insufficient for automated tasklist generation. The final roadmap should include task IDs, even if they're generated after Phase 0 locks architectural decisions.

2. **Staffing model is over-specified**: For a Claude Code single-implementer scenario, 4 named engineering roles add noise. The expertise domains can be noted as annotations on phases rather than a standalone staffing section.

3. **Separate `wiring_config.py` is likely correct**: Config with whitelist loading and validation logic is substantial enough to warrant its own file. This can be confirmed in Phase 0 but the default assumption should be separation, not co-location.

4. **Whitelist error escalation adds complexity**: Phase-aware warn→error behavior requires tracking which "phase" the system is in at runtime, which is non-trivial. Strict validation from the start with a clear error message is simpler and sufficient if the whitelist schema is defined before coding begins.

### Remaining disagreements

1. **Phase 0 as dedicated phase vs lightweight gate**: Variant A accepts a checkpoint; Variant B insists on a named phase with exit criteria. The disagreement is about formality, not substance. Variant A believes naming it a "phase" creates unnecessary ceremony; Variant B believes the ceremony is what makes it accountable.

2. **Phase structure (6 vs 7)**: Variant A maintains that bundling roadmap+sprint integration is appropriate given the single-implementer context. Variant B maintains that separation enables parallelism and cleaner milestone tracking. Neither has conceded.

3. **Risk framework granularity**: Variant A considers the 4-layer model academic; Variant B considers the flat table incomplete. Both acknowledge the individual risks are the same — the disagreement is about the organizational meta-structure.

4. **Roadmap scope boundary**: Variant A draws the line at technical sequencing; Variant B includes operational prerequisites. This is a philosophical difference about what a "roadmap" is — project plan or implementation plan.

---

## Convergence Assessment

### Areas of full agreement (18 shared + 4 concessions = 22 points)

- All 18 shared assumptions from diff analysis remain uncontested
- Report body sections should be enumerated in the roadmap (D05 resolved → Haiku)
- `Literal["off", "shadow", "soft", "full"]` type should be specified (D07 resolved → Haiku)
- Task IDs are necessary alongside milestone narratives (D03 resolved → both formats needed)
- Separate `wiring_config.py` is the default file layout (D04 resolved → Opus, confirmable in Phase 0)
- Whitelist error handling should be strict from the start (D06 resolved → Opus)
- Staffing model should be reduced to phase annotations (D08 resolved → compromise)

### Areas of partial agreement (3 points)

- **Phase 0**: Both agree the work must happen; disagree on whether it's a named phase or a pre-T01 checkpoint (D01)
- **Operational dependencies**: Both agree they matter; disagree on whether they belong in the roadmap body or an appendix (D09)
- **Critical path**: Both views are useful at different abstraction levels; a merged roadmap can include both (D12)

### Areas of genuine disagreement (2 points)

- **Phase count (D02)**: 6 bundled phases vs 7 separated phases — depends on implementer context (single vs multi-session, single vs multiple contributors)
- **Risk framework meta-structure (D10)**: Flat table vs 4-layer model — stylistic difference with no functional impact on risk mitigation

### Recommendation for merge

The merged roadmap should:
1. Include a **Phase 0 checkpoint** (Haiku's substance, Opus's brevity) — timeboxed, with exit criteria, but not inflated into a full implementation phase
2. Use **Opus's task ID scheme** (T01–T15) as the primary organizational unit, augmented with **Haiku's milestone sub-numbering** for progress tracking
3. **Separate roadmap and sprint integration** into distinct phases (Haiku) but note they can be combined in single-implementer scenarios
4. Include **report body section enumeration** and **`Literal` type specification** (Haiku)
5. Use **Opus's compact risk table** augmented with **Haiku's 4-layer summary** as a one-paragraph framing
6. Include **operational dependencies as an appendix** (compromise)
7. Default to **strict whitelist validation** (Opus) — simpler, no phase-tracking complexity
8. Include both **task-level and phase-level critical paths** for different audiences
