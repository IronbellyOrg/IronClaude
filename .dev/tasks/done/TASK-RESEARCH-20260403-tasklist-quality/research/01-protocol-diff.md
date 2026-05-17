# Protocol Diff: Tasklist Generation SKILL.md (master vs feat/tdd-spec-merge)

**Status**: Complete
**Date**: 2026-04-02
**Investigation Type**: Code Tracer
**Research Question**: What changed in the tasklist generation protocol between master and the current feature branch, and how do those changes affect decomposition rules, phase bucketing, and task conversion?
**Files Investigated**:
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (source of truth, 1273 lines on branch)
- `.claude/skills/sc-tasklist-protocol/SKILL.md` (active copy -- confirmed identical to source of truth)

---

## 1. Commit History

Single commit touches the SKILL.md:

```
a9cf7ee feat: add --prd-file supplementary input to roadmap and tasklist pipelines
```

This commit wires PRD as integrated business context across both CLI pipelines. The SKILL.md changes are part of a larger 17+ file commit that also modifies CLI flags, executors, prompt builders, and state files.

---

## 2. Diff Analysis

The diff adds **+122 net new lines** across four insertion points. No lines were removed or modified from the master version. All changes are purely additive.

### 2.1 Insertion Point 1: Section 3.x (after line 121 on master)

**New section: `### 3.x Source Document Enrichment`** (+20 lines)

Added between the directory structure section (end of Section 3) and the start of the Deterministic Generation Algorithm (Section 4).

**Content**: Defines the conceptual framework for TDD/PRD enrichment:
- Scoping note: Enrichment is a **skill-protocol behavior** (inference-time), NOT triggered by CLI `tasklist validate` command
- Distinguishes `build_tasklist_generate_prompt` (skill path) from `build_tasklist_fidelity_prompt` (CLI validate path)
- Lists six enrichment dimensions when source docs are available: function/class names from TDD, test case refs from TDD, persona-tagged ACs from PRD, metric instrumentation from PRD, migration contingency from TDD, scope boundary enforcement from PRD
- Establishes precedence rule: TDD for implementation specifics, PRD for descriptions/priorities/acceptance criteria

**Behavioral impact**: This section is **descriptive framing** only. It sets expectations for the LLM but does not contain generation rules. The actual generation rules live in 4.4a/4.4b.

### 2.2 Insertion Point 2: Sections 4.1a, 4.1b, 4.1c (after line 137 on master, after Step 4.1)

**New sections: `### 4.1a Supplementary TDD Context`**, **`### 4.1b Supplementary PRD Context`**, **`### 4.1c Auto-Wire from .roadmap-state.json`** (+44 lines)

**Content**:
- **4.1a**: Defines how to detect a TDD-format file and extract six structured context keys: `component_inventory`, `migration_phases`, `testing_strategy`, `observability`, `release_criteria`, `api_surface`
- **4.1b**: Defines how to extract six structured context keys from PRD: `user_personas`, `user_stories`, `success_metrics`, `release_strategy`, `stakeholder_priorities`, `acceptance_scenarios`
- **4.1c**: Defines auto-wire behavior from `.roadmap-state.json` so users don't have to re-pass flags

**Behavioral impact on decomposition**: None directly. These sections define data extraction, not task generation. They populate `supplementary_context` and `prd_context` variables that are consumed downstream in 4.4a/4.4b.

### 2.3 Insertion Point 3: Sections 4.4a and 4.4b (after line 164 on master, after Step 4.4)

**New sections: `### 4.4a Supplementary Task Generation`**, **`### 4.4b Supplementary PRD Task Generation`** (+45 lines)

This is the **primary behavioral change** affecting task count and decomposition.

#### Section 4.4a (TDD-conditional)

Runs **after** standard Step 4.4. Defines a table of 8 task patterns generated from TDD context keys:

| Source | Pattern | Net effect on task count |
|--------|---------|--------------------------|
| `component_inventory.new` | `Implement [name]` | **+N tasks** (but merge if duplicate) |
| `component_inventory.modified` | `Update [name]` | **+N tasks** (but merge if duplicate) |
| `component_inventory.deleted` | `Migrate/Remove [name]` | **+N tasks** (but merge if duplicate) |
| `migration_phases.stages` | One task per rollout stage in new phase | **+N tasks in new phase** |
| `testing_strategy.test_pyramid` | `Write [level] test suite` | **+N tasks** |
| `observability.metrics` | `Instrument metric: [name]` | **+N tasks** |
| `observability.alerts` | `Configure alert: [name]` | **+N tasks** |
| `release_criteria.definition_of_done` | `Verify DoD: [item]` | **+N tasks** (EXEMPT tier) |

**Critical instruction**: "Merge rather than duplicate if a generated task duplicates an existing task for the same component."

**Generation-time enrichment block**: Cross-references existing roadmap-derived tasks against TDD to add specificity (component classes, test cases, rollback steps, endpoint paths, field names). This enriches existing tasks rather than creating new ones.

#### Section 4.4b (PRD-conditional)

Runs **after** 4.4 and 4.4a. Defines a table of 3 task patterns:

| Source | Pattern | Net effect on task count |
|--------|---------|--------------------------|
| `user_stories` | `Implement user story: [actor] [goal]` -- **merge with existing** | **0 to +N** (merge-first) |
| `success_metrics` | `Validate metric: [name]` -- **add as subtask** | **0 to +N** (subtask-first) |
| `acceptance_scenarios` | `Verify acceptance: [scenario]` | **+N tasks** |

**Critical instruction**: "PRD-derived tasks enrich task descriptions and acceptance criteria but do NOT generate standalone implementation tasks -- engineering tasks come from the roadmap; PRD enriches them."

**Enrichment block**: Annotates existing tasks with persona tags, success metrics, stakeholder priorities, and scope boundary markers. This modifies existing tasks, not creating new ones.

### 2.4 Insertion Point 4: Supplementary TDD Validation (after Stage 7, line ~908 on master)

**New block in Stage 7 validation** (+13 lines)

Adds four validation checks when `--spec` was provided:
- Every new component in TDD has a corresponding task (HIGH)
- Migration stages reflected in phase names or task titles (MEDIUM)
- Each test pyramid level has at least one task (MEDIUM)
- Each DoD item appears as a verification task (LOW)

**Behavioral impact**: Validation-only. Does not affect task generation count, but could trigger patch plan generation in Stage 8 if findings are found.

---

## 3. Behavioral Impact Assessment

### 3.1 Impact on Decomposition Rules (Section 4.4)

**The core decomposition rule in Section 4.4 is UNCHANGED.** The master rule remains:
- 1 task per roadmap item by default
- Split only when the item contains 2+ independently deliverable outputs

The new sections 4.4a/4.4b add supplementary tasks **after** the core decomposition. They do not modify the 1:1 roadmap-to-task mapping.

**However**, the "merge rather than duplicate" instruction in both 4.4a and 4.4b is the **key mechanism that could reduce task count**. When the LLM is told to "merge" a supplementary task with an existing task, it may interpret this as folding what would have been a separate task into enrichment of an existing task. This is particularly acute for:

1. **4.4b user_stories**: "merge with existing feature task if one covers the same goal" -- this explicitly tells the LLM to NOT create a new task when an existing roadmap-derived task already covers the goal
2. **4.4b success_metrics**: "add as subtask or validation step on existing implementation tasks" -- folds into existing tasks
3. **4.4a component_inventory**: "Merge rather than duplicate" -- if roadmap already has tasks for these components (likely), they merge

### 3.2 Impact on Phase Bucketing (Section 4.2)

**Section 4.2 is UNCHANGED.** Phase bucketing logic remains purely roadmap-driven:
- Explicit phase labels from roadmap headings, OR
- Top-level `##` headings, OR
- Default 3-bucket split (Foundations / Build / Stabilize)

**However**, Section 4.4a introduces one new phase:
- `migration_phases.stages` creates a "Deployment & Rollout" phase appended at the end

This means the enriched pipeline should produce **roadmap_phases + 1** phases (if TDD has migration stages), not fewer. The observed 3 phases vs 5 phases difference is therefore NOT explained by the protocol additions, which would only add phases, never remove them. The phase count difference likely comes from the roadmap content itself or how the LLM interprets the roadmap when enrichment context is present.

### 3.3 Impact on Task Conversion

The enriched pipeline's 44 tasks (vs baseline 87) is **not directly explained by these protocol additions**. The additions should, if anything, ADD tasks (supplementary generation) rather than reduce them. The reduction must be caused by one of:

1. **LLM behavioral shift due to enrichment context**: When the LLM receives TDD/PRD context alongside the roadmap, it may produce more consolidated, higher-specificity tasks rather than splitting broadly. The enrichment instructions emphasize merging and annotation over creation.

2. **"Merge rather than duplicate" over-application**: The LLM may be aggressively merging roadmap-derived tasks when it sees that TDD components cover the same ground, collapsing what would have been multiple roadmap tasks into single enriched tasks.

3. **Scope boundary enforcement**: The PRD enrichment instruction "Tasks must not exceed `release_strategy.in_scope` boundaries" could cause the LLM to drop tasks it considers out-of-scope.

4. **Different roadmap interpretation with context**: The presence of structured TDD/PRD context may cause the LLM to parse the roadmap more conservatively, treating related items as a single roadmap item when they map to the same TDD component.

---

## 4. Consolidation / Merge Instructions Found

The following explicit merge/consolidation instructions exist in the new sections:

| Location | Instruction | Risk Level |
|----------|------------|------------|
| 4.4a header | "Merge rather than duplicate if a generated task duplicates an existing task for the same component" | MEDIUM -- could cause aggressive merging |
| 4.4b header | "Merge rather than duplicate if a generated task duplicates an existing task" | HIGH -- broader scope than 4.4a |
| 4.4b user_stories row | "merge with existing feature task if one covers the same goal" | HIGH -- vague "same goal" matching |
| 4.4b success_metrics row | "add as subtask or validation step on existing implementation tasks" | LOW -- adds to existing rather than creating |
| 4.4b preamble | "do NOT generate standalone implementation tasks -- engineering tasks come from the roadmap; PRD enriches them" | HIGH -- explicitly suppresses task creation |

---

## 5. Minimum Task Count Enforcement Points

The protocol currently has **no minimum task count enforcement**. Potential insertion points for a floor:

1. **Section 4.4 (after the split rule)**: Add a post-generation assertion: "The total task count MUST be >= the number of parsed roadmap items (from Step 4.1). If fewer tasks exist than roadmap items, the generator has incorrectly merged tasks and must re-decompose."

2. **Section 4.4a (after the merge instruction)**: Add: "Merge is permitted only when two tasks have identical component names AND identical deliverable types. When in doubt, keep separate."

3. **Section 4.4b (after the merge instruction)**: Add: "PRD enrichment MUST NOT reduce the task count below the count produced by Steps 4.4 + 4.4a. If a merge would cause net task reduction, annotate instead of merging."

4. **Stage 7 validation**: Add a validation check: "Total task count must be >= 1.0x the parsed roadmap item count. Finding level: HIGH if violated."

5. **New Section 4.4c (post-generation floor)**: "After Steps 4.4, 4.4a, and 4.4b complete, assert: `len(all_tasks) >= len(roadmap_items)`. If this assertion fails, the generator over-merged. Re-run Step 4.4 without merge instructions."

---

## Gaps and Questions

1. **No task count floor**: The protocol has no mechanism to prevent the LLM from producing fewer tasks than roadmap items. The merge instructions are one-directional (merge when duplicate) with no guard against over-merging.

2. **Phase count not controlled**: The protocol does not enforce that enriched runs produce at least as many phases as non-enriched runs for the same roadmap. If the LLM re-interprets the roadmap with enrichment context, it could collapse phases.

3. **"Same goal" is subjective**: The user_stories merge instruction uses "if one covers the same goal," which is LLM-judgment-dependent. Two different LLM runs could produce different merge decisions, violating the "deterministic" claim.

4. **No A/B comparison in validation**: Stage 7 validation does not compare enriched output against a baseline (non-enriched) run. It only validates against the source documents, not against what the baseline would have produced.

5. **3.x framing may prime consolidation**: The Section 3.x framing ("more specific, actionable task decomposition") implicitly encourages the LLM to consolidate vague tasks into fewer specific ones. "More specific" and "fewer" are not the same thing, but LLMs may conflate them.

6. **Scope boundary as task suppressor**: The instruction "Tasks must not exceed `release_strategy.in_scope` boundaries; flag violations as scope warnings" could cause the LLM to silently drop tasks that approach scope edges rather than flagging them.

7. **Unanswered**: Does the CLI `build_tasklist_generate_prompt` actually pass the full enrichment instructions to the LLM, or does it pass a simplified subset? If the prompt builder truncates/summarizes, the SKILL.md protocol may not be fully realized in practice.

---

## Summary

The protocol diff consists of **+122 additive lines** in a single commit (a9cf7ee), adding four new sections: 3.x (enrichment framing), 4.1a/4.1b/4.1c (data extraction from TDD/PRD), 4.4a/4.4b (supplementary task generation), and a Stage 7 validation extension.

**Core finding**: The additions do NOT modify the base decomposition rules (Section 4.4) or phase bucketing rules (Section 4.2). They are purely additive supplementary generation and enrichment. However, the repeated "merge rather than duplicate" instructions and the PRD section's explicit "do NOT generate standalone implementation tasks" create a strong LLM-behavioral incentive to consolidate rather than expand. This is the most likely protocol-level explanation for the observed 44-task (enriched) vs 87-task (baseline) discrepancy.

**Root cause hypothesis**: The task count reduction is not caused by the protocol removing decomposition rules, but by the enrichment context causing the LLM to produce denser, more consolidated tasks. The merge instructions act as a soft ceiling, and the enrichment context shifts the LLM's decomposition strategy from "broad coverage" to "precise coverage." The protocol lacks a hard floor to prevent this.

**Recommended fix**: Add a post-generation task count assertion (Section 4.4c or Stage 7 validation) requiring `total_tasks >= parsed_roadmap_items`, and tighten merge criteria to require identical component names + identical deliverable types before merging.
