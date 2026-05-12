---
title: "Adversarial Debate: Split-First vs Run-Then-Re-Split vs Hybrid"
generated: 2026-04-03
format: structured adversarial debate
question: "Should the 4-phase Path A refactoring prompt be partitioned per-split-release, or run unified then re-split?"
---

# Adversarial Debate: Process Path A Refactoring Per-Split-Release vs Run-Then-Re-Split

## Preamble

The v3.7 unified spec was split into R1 (Pipeline Reliability & Naming, ~480 LOC) and R2 (Sprint TUI v2, ~800+ LOC) by adversarial validation at 0.83 convergence. Post-split, deep analysis revealed that the ENTIRE spec targets Path B (fallback for malformed files), while Path A (production per-task subprocess path) receives none of the improvements. A merged refactoring recommendation proposes 11 new tasks (PA-01 through PA-08, NEW-DM-04 through DM-06) plus modifications to 16 existing tasks. The question: how does this new dimension interact with the validated split?

---

## OPTION A -- Split-First

**Thesis**: Partition the 4-phase prompt and the broader Path A work to run against each split release independently. R1 absorbs pipeline-layer Path A work; R2 absorbs presentation-layer Path A work.

### Strength Score: 0.62

### Key Arguments

**A1. The split boundary holds under Path A introduction.** The split seam is "data contract vs presentation layer." Path A work decomposes along the same axis:
- **R1 scope**: PA-01/02/03 (prompt enrichment -- pipeline behavior), PA-04/05/06 (TurnLedger bug fixes -- data integrity), PA-06 (gate default -- enforcement policy), NEW-DM-04/05 (token extraction -- data model).
- **R2 scope**: TUI adaptation of F1-F4/F6/F8 for Path A data sources, MonitorState population hooks, PhaseSummarizer dual-input, NEW-DM-06 (aggregation logic for TUI consumption).

This is NOT a forced fit. Prompt enrichment IS pipeline reliability. TUI adaptation IS presentation. The seam survives.

**A2. R1 is potentially in progress; disruption cost is real.** The split report explicitly defines handoff criteria and a planning gate. If R1 work has begun or its roadmap/tasklist has been generated, re-splitting imposes coordination costs: invalidated tasklist indices, regenerated fidelity audits, potential merge conflicts if R1 has a branch. Adding PA-04/05/06 (5 lines total) and PA-01/02/03 (~60 LOC) to R1 is purely additive -- no existing R1 task changes scope.

**A3. TurnLedger fixes in R1 create a clean prerequisite.** PA-04/05/06 fix bugs that zero out the reimbursement system. These are P0 data-integrity fixes. Placing them in R1 means R2 inherits a working TurnLedger. This matches the boundary rationale's principle: "R1 establishes data contract, R2 builds presentation layer." A broken TurnLedger IS a broken data contract.

**A4. Fidelity indices are expensive to reproduce.** The original split achieved 1.00 fidelity (78/78 requirements preserved). Re-running sc:release-split requires re-validating all 78 requirements PLUS the 11 new ones, re-running adversarial agents, re-computing convergence. The "5 minutes" claim for re-splitting understates the cognitive verification overhead.

**A5. Scope contamination risk in R2 is real.** Running the 4-phase prompt against the merged spec produces analysis that spans both releases. The analyst must then mentally partition results. Option A forces the analysis to stay within release boundaries, preventing accidental cross-boundary assumptions.

### Weaknesses (What Option B Gets Right)

- The split was designed for Path B only. The implicit assumption that "the boundary also works for Path A" has not been adversarially validated. It is plausible but unproven.
- The 4-phase prompt was designed as a coherent pipeline. Splitting it requires understanding inter-phase dependencies that may not be obvious until execution.
- executor.py is modified by BOTH releases AND by Path A work. The "different line ranges" argument in the merged recommendation (PA-04: line 1091, PA-05: lines 1017-1025, PA-01: lines 1064-1068) works for isolated tasks but gets murky when you also consider R1's checkpoint hooks (lines 1222-1233) and R2's TUI hooks (lines 978-984, 1042-1048). Running analysis against the full file avoids artificial blind spots.

### Risk If Chosen

- The 4-phase prompt may produce incoherent results when constrained to a single release's context. Phase 2 (OutputMonitor adaptation) inherently analyzes executor.py's full behavior. Artificially scoping it to R2 may miss interactions with R1's checkpoint hooks that modify the same post-phase flow.
- Manual partitioning of PA tasks into R1/R2 could introduce errors that adversarial validation would have caught.

---

## OPTION B -- Run-Then-Re-Split

**Thesis**: Run the 4-phase prompt against the original merged spec, produce a unified plan, then re-run sc:release-split to generate a NEW split that organically incorporates Path A work.

### Strength Score: 0.58

### Key Arguments

**B1. The split was made without material information.** The original split operated on a spec that was 100% Path B. It answered "how to split Path B work into two releases." It did NOT answer "how to split Path B + Path A work into two releases." The convergence score of 0.83 validates a question that is no longer the question being asked. This is not a minor update -- Path A work adds a new dimension (per-task subprocess model) that the split agents never evaluated.

**B2. The 4-phase prompt has cross-phase dependencies.** The prompt sequence is: Phase 1 (architecture analysis) -> Phase 2 (OutputMonitor adaptation design) -> Phase 3 (implementation plan) -> Phase 4 (validation). Phase 2's OutputMonitor analysis examines executor.py's FULL execution flow, including how `_run_task_subprocess()` interacts with post-phase hooks that both R1 and R2 modify. Constraining Phase 2 to R2's context blinds it to R1's checkpoint hook insertions at the same code locations.

**B3. The merged recommendation proposes a unified Wave 0 that precedes the split boundary.** The implementation order places PA-04/05/06 and PA-01 in "Phase 0: Foundation" -- work that MUST complete before either R1 or R2's Wave 1. This is a new dependency that the original split does not account for. Force-fitting Wave 0 into R1 works pragmatically but was not what the recommendation designed for.

**B4. sc:release-split is idempotent and fast.** The tool is designed for exactly this: ingesting a revised spec and producing a validated split. It re-runs adversarial agents, computes fidelity, and produces boundary rationale. The 5-minute cost is accurate for tool execution. The "cognitive overhead" argument from Option A conflates human review time (which is required regardless) with tool execution cost.

**B5. executor.py's 3-domain conflict risk is the elephant in the room.** The file impact matrix rates executor.py as HIGH conflict risk because 3 domains modify it. Analyzing all 3 domains together produces a coherent hook-ordering specification. Splitting the analysis fragments this: R1's analyst sees checkpoint hooks only, R2's analyst sees TUI hooks only, neither sees the interaction. The merged recommendation's Section 6.4 specifically calls out that post-phase hook insertion "must happen in BOTH Path A block (lines 1222-1233) AND Path B block (lines 1432-1454)" -- this insight requires full-spec awareness.

### Weaknesses (What Option A Gets Right)

- Re-splitting discards validated work. The fidelity audit (78/78 preserved) and adversarial convergence (0.83) represent real analytical effort. The new split may produce a WORSE boundary if the Path A dimension complicates the seam.
- If R1 work has begun, re-splitting introduces disruption. The "before R1 ships" reversal cost is zero only if R1 implementation has not started.
- The argument that "the question has changed" overstates the impact. Path A work is ~120 LOC across 11 tasks. The original 78 tasks are unchanged. The split boundary's validity for those 78 tasks is not affected by adding 11 new ones. The real question is narrower: "where do the 11 new tasks land?"

### Risk If Chosen

- The new split may produce a DIFFERENT boundary that is less clean than the current one. The current seam (infrastructure/presentation) is a classic layered architecture pattern. Adding Path A work might cause the splitter to propose a different cut (e.g., Path A/Path B) that is architecturally worse.
- Re-splitting after Phase 2 is already in progress wastes the current analytical momentum. The Phase 2 designer is deep in executor.py's behavior; pausing to re-split interrupts flow.

---

## OPTION C -- Hybrid: Complete Then Partition

**Thesis**: Complete the 4-phase prompt as-is (it is already on Phase 2), then manually partition the RESULTS into the two existing split releases, then validate each release spec independently.

### Strength Score: 0.78

### Key Arguments

**C1. Preserves analytical coherence of the 4-phase prompt.** The prompt was designed to analyze the OutputMonitor adaptation against executor.py's full behavior. Phase 2 is already in progress. Letting it complete avoids artificial constraints and produces the most thorough analysis.

**C2. Preserves the validated split boundary.** The R1/R2 split at 0.83 convergence with 1.00 fidelity is NOT discarded. It remains the organizing frame. The new Path A tasks are partitioned INTO this frame, not used to generate a new one.

**C3. The partitioning step is straightforward.** The merged recommendation already classifies every task by domain (prompt enrichment, TurnLedger, data model, TUI adaptation). The mapping to R1/R2 follows directly from the boundary rationale:
- R1 absorbs: PA-01/02/03 (prompt enrichment = pipeline reliability), PA-04/05/06 (TurnLedger = data contract fixes), PA-06 (gate default = enforcement policy), NEW-DM-04/05 (token extraction = data model foundation).
- R2 absorbs: F1-F4/F6/F8 Path A adaptations (TUI = presentation), NEW-DM-06 (aggregation = feeds TUI), MonitorState population hooks, PhaseSummarizer dual-input.
- PA-07/PA-08 are P2/optional and can land in either release or be deferred.

**C4. Avoids BOTH costs.** Does not re-run sc:release-split (avoids re-validation overhead). Does not fragment the 4-phase analysis (avoids incoherent results). The only new cost is a manual partitioning step with independent validation -- which is less work than either alternative's downside.

**C5. Independent validation catches partitioning errors.** After partitioning, each release spec is validated against its own fidelity index. This catches any tasks that were mis-assigned. The validation is lightweight because it is incremental: only the 11 new tasks need checking, not the original 78.

### Weaknesses

- Manual partitioning introduces human judgment where sc:release-split provides automated adversarial validation. A mistake in assignment (e.g., putting NEW-DM-06 aggregation in R1 instead of R2) would not be caught automatically.
- The "independent validation" step is hand-waved. Who performs it? With what rigor? If it is just a quick review, it is weaker than sc:release-split's adversarial agents.
- This option assumes the 4-phase prompt's output is cleanly partitionable. If the unified analysis produces tightly coupled recommendations (e.g., "PA-04 fix AND F2 TUI wiring should be done atomically"), partitioning may force artificial separation.

### Risk If Chosen

- The manual partitioning step becomes a single point of failure. If the partitioner does not deeply understand both the split boundary rationale AND the Path A analysis, tasks may be mis-assigned.
- The lack of formal adversarial validation on the partitioned result means lower confidence than either Option A (which constrains analysis to release scope) or Option B (which re-validates from scratch).

---

## Verdict

### Winner: OPTION C -- Hybrid: Complete Then Partition

### Convergence Score: 0.65

The debate was moderately close. Options A and B both have legitimate concerns, but they represent opposite overreactions to the same situation:

- **Option A overreacts** by fragmenting a coherent analytical pipeline to fit a boundary that was designed without knowledge of the work being analyzed.
- **Option B overreacts** by discarding a validated split to accommodate ~120 LOC of new work that maps cleanly onto the existing boundary.

Option C recognizes two independent truths:

1. **The 4-phase prompt should complete as designed.** It is already on Phase 2. Its cross-phase dependencies are real. Constraining it to a single release's context produces worse analysis. This favors B's argument about analytical coherence.

2. **The split boundary is correct and should not be re-derived.** The infrastructure/presentation seam holds for Path A work just as it holds for Path B work. Prompt enrichment IS infrastructure. TUI adaptation IS presentation. The 11 new tasks map cleanly. This favors A's argument about preserving validated work.

The hybrid resolves the tension: unified analysis, existing boundary, incremental validation.

### Key Decision Factors

| Factor | Weight | Favors |
|--------|--------|--------|
| Phase 2 already in progress | High | C (do not interrupt) |
| executor.py 3-domain conflict risk | High | B/C (holistic analysis needed) |
| Split boundary validity for Path A | Medium | A/C (boundary holds) |
| R1 implementation status unknown | Medium | A/C (avoid disruption) |
| Cost of re-splitting | Low | C (avoids it entirely) |
| 4-phase cross-phase dependencies | High | B/C (coherent pipeline) |
| Manual partitioning risk | Medium | B (automated is better) |

### Dissent Note

Option B's argument that "the split was made without material information" is the strongest individual argument in the debate. If the Path A analysis were being started fresh (Phase 1 not yet begun), Option B would be the correct choice. The hybrid wins primarily because Phase 2 is in progress and the partitioning is mechanically straightforward.

---

## Recommended Action

**Immediate (today)**:

1. Complete Phase 2 of the 4-phase prompt as currently scoped (full executor.py analysis, both paths, no release-scope constraint).
2. Complete Phases 3 and 4 in sequence.

**After Phase 4 completes**:

3. Produce a **Path A Partition Document** that assigns each of the 11 new tasks (PA-01 through PA-08, NEW-DM-04 through DM-06) to R1 or R2, using the existing boundary rationale as the governing principle. Proposed assignment:

   **R1 additions** (pipeline reliability + data contracts):
   - PA-01, PA-02, PA-03 (prompt enrichment)
   - PA-04, PA-05, PA-06 (TurnLedger bug fixes + gate default)
   - NEW-DM-04, NEW-DM-05 (token extraction, TaskResult fields)
   - Modified T02.04 (reframe checkpoint gate as Path A primary defense)
   - Modified T02.05 (extend tests for Path A flow)

   **R2 additions** (TUI presentation + data aggregation):
   - NEW-DM-06 (TaskResult -> PhaseResult aggregation for TUI)
   - Modified F1, F2, F3, F4, F6, F8 (Path A adaptations)
   - Modified 7.1, 7.2 (MonitorState + PhaseResult Path A population)
   - PA-07, PA-08 (optional, can defer to v3.8 if scope pressure)

4. Run **incremental fidelity validation** on both release specs: verify the 11 new tasks are assigned, verify no original task changed scope, verify cross-release dependencies are documented.

5. If validation surfaces a task that does not cleanly partition (e.g., a tightly coupled recommendation spanning both releases), escalate to a targeted adversarial micro-debate on that specific task rather than re-splitting the entire release.

---

## Appendix: Scoring Methodology

Strength scores reflect overall viability considering both argumentation quality and practical fitness for the current situation (Phase 2 in progress, split validated, R1 status unknown):

| Option | Argument Quality | Practical Fitness | Combined |
|--------|-----------------|-------------------|----------|
| A (Split-First) | 0.65 | 0.58 | 0.62 |
| B (Run-Then-Re-Split) | 0.72 | 0.45 | 0.58 |
| C (Hybrid) | 0.68 | 0.88 | 0.78 |

Option B has the strongest theoretical arguments but the weakest practical fitness (disrupts in-progress work, discards validated artifacts). Option C has the best practical fitness by threading the needle between the two extremes.
