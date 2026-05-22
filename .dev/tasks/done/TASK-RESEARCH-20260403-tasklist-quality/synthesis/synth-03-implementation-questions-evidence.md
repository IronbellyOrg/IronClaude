# Synthesis 03 -- Implementation Plan, Open Questions, and Evidence Trail

**Date:** 2026-04-03
**Sources:** Research files 01-06, gaps-and-questions.md
**Sections:** 8 (Implementation Plan), 9 (Open Questions), 10 (Evidence Trail)

---

## Section 8 -- Implementation Plan

### 8.1 Recommended Fix Option Summary

The recommended fix is a **multi-layer guard** approach that addresses both the upstream cause (roadmap phase count under-specification) and the downstream cause (tasklist prompt suppression and protocol merge over-application). The fix targets three files with four categories of change: (1) remove PRD task-suppression language from the tasklist prompt, (2) add anti-consolidation guard to the tasklist prompt, (3) tighten merge criteria and add a task count floor to the SKILL.md protocol, and (4) add phase count guidance to the roadmap generation prompt.

### 8.2 Implementation Steps

| Step | Action | File | Details |
|------|--------|------|---------|
| 1 | **Soften PRD suppression language** | `src/superclaude/cli/tasklist/prompts.py` | Lines 221-223: Replace `"PRD context informs task descriptions and priorities but does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them."` with `"PRD context enriches task descriptions, acceptance criteria, and priorities. PRD-derived requirements that map to an existing roadmap task should be merged into that task. PRD-derived requirements with no roadmap equivalent should generate new tasks."` This preserves the merge-when-overlap intent while removing the blanket suppression of new task creation. |
| 2 | **Add anti-consolidation guard to interaction block** | `src/superclaude/cli/tasklist/prompts.py` | Lines 227-235: Append the following sentence after the existing interaction block (after line 234, before the closing parenthesis on line 235): `"\n\nIMPORTANT: Supplementary documents (TDD, PRD) must only ADD tasks or ADD detail to existing tasks. The total task count with supplementary input must be >= the task count that would be produced from the roadmap alone. Never consolidate or remove roadmap-derived tasks based on supplementary context."` |
| 3 | **Tighten merge criteria in Section 4.4a** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Section 4.4a preamble (line 233): Replace `"Merge rather than duplicate if a generated task duplicates an existing task for the same component."` with `"Merge rather than duplicate ONLY when a generated task has an identical component name AND identical deliverable type as an existing task. When in doubt, keep as separate tasks."` |
| 4 | **Tighten merge criteria in Section 4.4b** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Section 4.4b preamble (line 255): Replace `"Merge rather than duplicate if a generated task duplicates an existing task."` with `"Merge rather than duplicate ONLY when a generated task targets the identical component and deliverable as an existing task."` Also replace `"do NOT generate standalone implementation tasks -- engineering tasks come from the roadmap; PRD enriches them"` with `"PRD-derived requirements that overlap an existing roadmap task enrich that task; PRD-derived requirements with no roadmap equivalent generate new tasks."` |
| 5 | **Add task count floor assertion (new Section 4.4c)** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Insert new section after 4.4b. Content: `"### 4.4c Post-Generation Task Count Floor\n\nAfter Steps 4.4, 4.4a, and 4.4b complete, assert:\n\n    len(all_tasks) >= len(parsed_roadmap_items)\n\nIf this assertion fails, the generator over-merged supplementary tasks into existing roadmap tasks. Re-run Step 4.4 treating each roadmap item as requiring at least one distinct task. Supplementary steps (4.4a, 4.4b) may only increase the task count above this floor, never decrease it."` |
| 6 | **Add Stage 7 validation check for task count** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Stage 7 Structural Quality Gate table (line ~911 area): Add new row 18 after existing row 17: `"18 \| Task count floor: total_tasks >= parsed_roadmap_item_count \| Prevents over-merging from supplementary enrichment \| HIGH"` (Note: existing rows run 1-17; the new row must be numbered 18 to avoid collision with existing row 14 "Clarification Task adjacency".) |
| 7 | **Add testing task minimum rule to Section 4.4a** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Section 4.4a (after the `release_criteria.definition_of_done` row in the task pattern table): Add rule: `"Each test pyramid level (unit, integration, E2E, security) referenced in testing_strategy must produce at least one standalone task per phase that contains implementation tasks. Do not absorb all testing into [VERIFICATION] steps."` This addresses Gap G6 (testing absorption at 5.6:1). |
| 8 | **Reframe Section 3.x enrichment description** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Section 3.x: Replace "more specific, actionable task decomposition" with "enrichment adds specificity to existing tasks AND generates additional tasks from supplementary sources. Enrichment must NEVER reduce the total task count." This addresses Gap G8. |
| 9 | **Soften scope boundary language** | `src/superclaude/cli/tasklist/prompts.py` | Lines 218-219: After "generate explicit 'out of scope' markers where roadmap milestones approach scope edges" append: `" Flag scope-adjacent tasks with a scope-warning marker rather than omitting them."` This addresses Gap G7. |
| 10 | **Add phase count guidance to roadmap generation** | `src/superclaude/cli/roadmap/prompts.py` | Function `build_generate_prompt`, after line 427 (`"6. Timeline estimates per phase\n\n"`): Insert `"Phase count guidance: target 4-6 phases for LOW complexity, 5-8 phases for MEDIUM complexity, 6-10 phases for HIGH complexity. Each phase should represent a shippable increment. Do not consolidate phases below the minimum for the complexity class.\n\n"` This uses the `complexity_class` already available in the extraction frontmatter. |
| 11 | **Sync dev copies** | Shell | Run `make sync-dev` to propagate `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` changes to `.claude/skills/sc-tasklist-protocol/SKILL.md`. Run `make verify-sync` to confirm. |

### 8.3 Integration Checklist

| # | Check | Command / Method | Pass Criteria |
|---|-------|-----------------|---------------|
| 1 | Tasklist prompt changes compile | `uv run python -c "from superclaude.cli.tasklist.prompts import build_tasklist_generate_prompt; print('OK')"` | No import errors |
| 2 | Roadmap prompt changes compile | `uv run python -c "from superclaude.cli.roadmap.prompts import build_generate_prompt; print('OK')"` | No import errors |
| 3 | Existing tests pass | `uv run pytest tests/ -v` | All tests green |
| 4 | SKILL.md sync verified | `make verify-sync` | src/ and .claude/ match |
| 5 | Baseline regression test | Run `superclaude roadmap run` with spec-only input, verify task count >= 80 (within 10% of original 87) | No degradation in spec-only pathway |
| 6 | TDD+PRD improvement test | Run `superclaude roadmap run` with TDD+PRD input, verify task count >= 60 (up from 44, target ~73 per file 04 projection) | Task count increases with enriched input |
| 7 | Phase count stability | Verify TDD+PRD roadmap produces >= 4 phases (per complexity guidance) | Phase consolidation prevented |
| 8 | Merge behavior spot-check | In TDD+PRD output, verify no roadmap item lost its 1:1 task mapping | Floor assertion effective |

### 8.4 Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Prompt changes cause task count explosion (too many tasks) | The floor is a minimum, not a target. The "merge when identical component AND deliverable" criteria still permits valid deduplication. Monitor output for first 3 runs. |
| Phase count guidance conflicts with PRD rollout strategy | The guidance says "target" not "require." PRD-driven milestone phasing (Alpha/Beta/GA) can override if the LLM judges it more appropriate, but must justify in frontmatter. |
| SKILL.md changes break non-TDD/PRD workflows | All changes are conditional (4.4a/4.4b only run when --spec or --prd-file flags are present). Base Section 4.4 is untouched. |
| Regression in existing test fixtures | Baseline test fixtures (test3-spec-baseline) do not use TDD/PRD supplementary input, so Steps 1-2 and 3-8 do not affect them. |

---

## Section 9 -- Open Questions

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|---------------------|
| 1 | What is the correct target task count for TDD+PRD enriched input? File 04 projects ~73 at baseline granularity. Is that the right floor, or should enriched runs produce MORE tasks than baseline (due to additive TDD/PRD content)? | HIGH -- determines the floor value in Section 4.4c and the pass criteria for integration test #6 | Use `parsed_roadmap_items` as the floor (guarantees 1:1 minimum). The ~73 projection is an upper bound estimate. Actual target depends on roadmap content; the floor prevents regression, not mandates expansion. |
| 2 | Should the fix prioritize roadmap phasing (H1 -- fewer phases) or tasklist prompt instructions (H2 -- PRD suppression)? Evidence supports both as contributing factors. | HIGH -- determines implementation sequencing | Fix both. They are independent and non-conflicting. Roadmap phase guidance (Step 7) prevents upstream phase consolidation. Tasklist prompt changes (Steps 1-2) prevent downstream task suppression. Neither alone is sufficient. |
| 3 | Is the consistent ~27-29K output token budget a hard model constraint or soft LLM behavior? (File 06 finding) | MEDIUM -- if hard, task density is bounded regardless of prompt changes | Test empirically: run the modified prompts and measure output token count. If output tokens increase with more tasks, the constraint was soft. If they plateau at ~28K, consider multi-turn generation or explicit "continue generating" prompts. |
| 4 | How should testing tasks be handled? The 5.6:1 testing consolidation (28 standalone test tasks -> 5) is the single biggest driver of task count reduction. Should tests always be standalone tasks? | HIGH -- affects whether the fix includes a "standalone test task" mandate | Do not mandate standalone test tasks in this fix. The embedded [VERIFICATION] pattern in TDD+PRD tasks is a valid decomposition strategy. However, add a Stage 7 validation check: "Each test pyramid level (unit, integration, E2E) must have at least one explicitly named task or subtask." This ensures testing is tracked without forcing the baseline's granularity. |
| 5 | Who calls `build_tasklist_generate_prompt`? The function docstring says the `/sc:tasklist` skill protocol calls it, but the CLI `tasklist validate` does NOT. What is the actual invocation path? | MEDIUM -- if the function is never called in the CLI pathway, prompt changes only affect skill-protocol runs | Trace the call chain from `/sc:tasklist` skill invocation through the CLI executor. If the function is only used in inference-mode (skill protocol), prompt changes apply only to that pathway. CLI pipeline changes would need separate implementation. |
| 6 | Is the 49% reduction measured on the same roadmap? The TDD+PRD pipeline also produces a different (merged) roadmap. The input roadmap to `build_tasklist_generate_prompt` may itself be different, confounding the analysis. | HIGH -- if the roadmaps differ, the reduction is partly input-driven, not prompt-driven | Confirmed by file 03: the roadmaps ARE different (380 lines vs 746 lines, different phase models, different R-item counts). The task count difference is primarily driven by the roadmap having fewer R-items (44 vs 87), which is upstream of the tasklist generator. The prompt changes address downstream suppression; the roadmap phase guidance addresses the upstream cause. |
| 7 | Does the extraction step's `complexity_class` influence phase count in the generate step? | LOW -- the generate prompt references `complexity_class` in frontmatter but gives no phase-count mapping | Step 7 of the implementation plan directly addresses this by adding a `complexity_class` -> phase count mapping to `build_generate_prompt`. After implementation, this question is resolved. |
| 8 | Could the scope boundary instruction (tasklist prompts.py line 218-219) silently drop tasks that approach PRD scope edges? | MEDIUM -- if the LLM interprets "tasks must not exceed defined scope" as "drop tasks near scope edges," task count decreases | Monitor for scope-dropped tasks in integration test #6. If task count does not increase sufficiently after Steps 1-2, add explicit language: "Flag scope-adjacent tasks as warnings but do NOT remove them." |
| 9 | Is the 120KB CLI arg limit (`_EMBED_SIZE_LIMIT`) ever hit in TDD+PRD runs? File 06 calculates ~110KB (90% of limit). | LOW -- only affects CLI pipeline pathway, not skill protocol | For CLI pathway runs, monitor for the size warning log. If hit, consider splitting the prompt or using file references instead of inline embedding. Not blocking for this fix. |

---

## Section 10 -- Evidence Trail

### 10.1 Research Files

| # | File Path | Topic | Agent Type | Lines | Key Finding |
|---|-----------|-------|-----------|-------|-------------|
| 01 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/01-protocol-diff.md` | SKILL.md protocol diff (master vs feat/tdd-spec-merge) | Code Tracer | 206 | +122 additive lines in commit a9cf7ee. Core decomposition rules (4.4) and phase bucketing (4.2) unchanged. New sections 4.4a/4.4b add "merge rather than duplicate" instructions that incentivize consolidation. No task count floor exists. |
| 02 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/02-tasklist-prompts.md` | Tasklist generation prompt analysis | Code Tracer | 178 | Lines 221-223 of `prompts.py` contain the only task-suppression language: "PRD does NOT generate standalone implementation tasks." TDD block is purely additive. PRD block suppresses. Interaction block amplifies suppression. |
| 03 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/03-roadmap-phases.md` | Roadmap phase structure comparison | Pattern Investigator | 203 | 3 phases (TDD+PRD) vs 5 phases (baseline) driven by PRD rollout strategy (Alpha/Beta/GA) vs technical-layer decomposition. Tasklist generator has strict 1:1 phase fidelity. Both runs show perfect 1:1 R-item-to-task ratio. |
| 04 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/04-task-decomposition.md` | Task decomposition granularity comparison | Pattern Investigator | 283 | TDD+PRD operates at 2-3x coarser granularity for implementation (vertical integration pattern) and 5-6x coarser for testing (absorption pattern: 28 standalone -> 5). Projected ~73 tasks if decomposed to baseline granularity. |
| 05 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/05-roadmap-prompts.md` | Roadmap prompt phase count analysis | Code Tracer | 234 | Zero phase count guidance in `build_generate_prompt`. No minimum, maximum, complexity mapping, or consolidation instructions. Phase count is entirely LLM-inferred. PRD prioritization language may cause emergent consolidation. |
| 06 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/06-context-analysis.md` | Context window saturation analysis | Architecture Analyst | 198 | Context saturation ruled out (24.5% utilization, 150K+ tokens remaining). Both scenarios produce ~28K output tokens. Output token ceiling is the binding constraint, not context window. Fewer tasks with more detail per task = output budget reallocation. |

### 10.2 Synthesis Files

| # | File Path | Sections Covered | Sources |
|---|-----------|-----------------|---------|
| synth-01 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/synthesis/synth-01-problem-current-state.md` | 1 (Problem Statement), 2 (Current State) | Research 01-06 |
| synth-02 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/synthesis/synth-02-gaps-rootcause-options.md` | 3-5 (Gap Analysis), 6 (Root Cause), 7 (Options) | Research 01-06 |
| synth-03 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/synthesis/synth-03-implementation-questions-evidence.md` | 8 (Implementation Plan), 9 (Open Questions), 10 (Evidence Trail) | Research 01-06, gaps-and-questions.md |

### 10.3 Gaps Log

| File Path | Content | Date |
|-----------|---------|------|
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/gaps-and-questions.md` | Consolidated gaps from analyst completeness report + QA research gate. 3 resolved gaps (task count discrepancy, missing headers, CODE-VERIFIED tags). 4 open questions carried forward to Section 9. | 2026-04-03 |

### 10.4 QA and Review Files

| File Path | Purpose |
|-----------|---------|
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/qa/analyst-completeness-report.md` | Cross-agent completeness verification |
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/qa/qa-research-gate-report.md` | QA gate for research phase |
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/qa/qa-task-validation-report.md` | Task validation against requirements |
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/qa/qa-qualitative-review.md` | Qualitative review of research quality |

### 10.5 Source Files Referenced

| File Path | Role in Investigation |
|-----------|----------------------|
| `src/superclaude/cli/tasklist/prompts.py` | Primary fix target -- contains PRD suppression language (lines 221-223) and interaction block (lines 227-235) |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Primary fix target -- contains merge directives (Sections 4.4a, 4.4b) and validation rules (Stage 7) |
| `src/superclaude/cli/roadmap/prompts.py` | Secondary fix target -- missing phase count guidance in `build_generate_prompt` (line 427 area) |
| `src/superclaude/cli/roadmap/commands.py` | Context -- input routing and flag handling |
| `.dev/test-fixtures/results/test3-spec-baseline/` | Baseline comparison data (87 tasks, 5 phases) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/` | TDD+PRD comparison data (44 tasks, 3 phases) |
