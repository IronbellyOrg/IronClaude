# Research Prompt: Tasklist Generation Produces Fewer Tasks from Richer Input

## GOAL

Investigate why the tasklist generation produces 87 tasks (3,380 lines) from a 312-line spec-only input but only 44 tasks (2,407 lines) from 1,282 lines of TDD+PRD input, and determine what needs to change so richer input produces at least as many (and ideally more) tasks with finer decomposition.

## WHY

This is backwards. The TDD has 876 lines of technical design including data models, API specs with exact endpoints, component inventories with exact class names, testing strategies with test IDs, migration plans with rollback procedures, and operational readiness checklists. The PRD adds 406 lines of personas, success metrics, compliance requirements, and customer journeys. The combined input is 4x richer than the spec alone.

Yet the pipeline produces FEWER, COARSER tasks from the richer input:

| Metric | Spec-Only Baseline | TDD+PRD Enriched |
|--------|-------------------|------------------|
| Input lines | 312 | 1,282 (4.1x more) |
| Roadmap lines | 380 | 746 (2.0x more) |
| Tasklist total lines | 3,380 | 2,407 (29% LESS) |
| Tasks | 87 | 44 (49% FEWER) |
| Phases | 5 | 3 (40% FEWER) |
| Lines per task | 38.9 | 54.7 (each task is denser) |

The enrichment IS present in the 44 tasks (30 persona refs, 35 compliance refs, 124 component refs vs baseline's 0/0/73). But there should be MORE tasks decomposing MORE of the rich content, not fewer.

## EVIDENCE

### Baseline Tasklist (87 tasks, 5 phases)
**Directory:** `.dev/test-fixtures/results/test3-spec-baseline/`
- `tasklist-index.md` — 66 lines
- `phase-1-tasklist.md` — 617 lines, 16 tasks
- `phase-2-tasklist.md` — 656 lines, 17 tasks
- `phase-3-tasklist.md` — 649 lines, 17 tasks
- `phase-4-tasklist.md` — 823 lines, 22 tasks
- `phase-5-tasklist.md` — 569 lines, 15 tasks
- Generated on master branch by `/sc:tasklist` skill from a 380-line roadmap

### TDD+PRD Tasklist (44 tasks, 3 phases)
**Directory:** `.dev/test-fixtures/results/test1-tdd-prd-v2/`
- `tasklist-index.md` — 219 lines
- `phase-1-tasklist.md` — 1,325 lines, 27 tasks
- `phase-2-tasklist.md` — 455 lines, 9 tasks
- `phase-3-tasklist.md` — 408 lines, 8 tasks
- Generated on current branch by `/sc:tasklist` skill from a 746-line roadmap with TDD+PRD supplementary files

### The Roadmap Phase Structure Difference
The baseline roadmap has a different phase structure than the TDD+PRD roadmap. Check:
- How many phases does the baseline roadmap define?
- How many phases does the TDD+PRD roadmap define? (We know it has 3 explicit phases: Core Auth, Password Reset + Beta, GA + Stabilization)
- Did the tasklist generator follow the roadmap's phase structure, or did it create its own?
- Did the baseline's `/sc:tasklist` (on master) use a different version of the skill protocol than our branch?

## WHAT TO INVESTIGATE

### 1. The /sc:tasklist Skill Protocol
- `.claude/skills/sc-tasklist-protocol/SKILL.md` — Read the FULL protocol. How does it determine phase count? How does it determine task granularity? What are the decomposition rules (Section 4.4)?
- Key question: Does the protocol say "1 task per roadmap item by default"? If so, does the roadmap's structure (3 phases with subsections vs 5 phases) drive the task count?
- Does the protocol differ between master branch and current branch? Check git history: `git log --oneline -- .claude/skills/sc-tasklist-protocol/SKILL.md` and `git diff master..HEAD -- src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

### 2. The build_tasklist_generate_prompt Function
- `src/superclaude/cli/tasklist/prompts.py` — Read `build_tasklist_generate_prompt`. Does the TDD/PRD supplementary block change the decomposition instructions? Does it tell the LLM to consolidate tasks?
- Key question: Does the PRD block say something like "PRD does not generate standalone implementation tasks" that could cause the LLM to produce fewer tasks?

### 3. The Roadmap Content Structure
- Read both roadmaps and count the number of independently actionable items in each:
  - `.dev/test-fixtures/results/test3-spec-baseline/roadmap.md` — Count subsections, bullet items, table rows that represent discrete work items
  - `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md` — Same count
- The TDD+PRD roadmap at 746 lines should have MORE discrete work items than the 380-line baseline. If it doesn't, the roadmap generation is the problem (compressing content instead of expanding it). If it does, the tasklist generation is the problem (not decomposing those items into tasks).

### 4. Phase Count Driver
- The TDD+PRD roadmap has 3 explicit phases. The baseline roadmap may have 5. If the tasklist generator follows the roadmap's phase count, then the 3-vs-5 phase difference comes from the ROADMAP, not the tasklist generator.
- Check: does the baseline roadmap define more phases? Why would the enriched roadmap (with more content) produce fewer phases?

### 5. Task Decomposition Comparison
- Pick 3 equivalent areas covered by both roadmaps (e.g., "implement login endpoint", "password reset", "testing/QA") and compare how each tasklist decomposes them:
  - Does the baseline break "implement login" into 3 separate tasks while TDD+PRD does it in 1?
  - Does the TDD+PRD version have a single task "Implement AuthService facade" that covers what the baseline splits into "Implement login handler", "Implement registration handler", "Implement auth middleware"?

### 6. Root Cause Hypotheses
- **H1: Roadmap phase count drives tasklist phase count.** The TDD+PRD roadmap has 3 phases; the baseline has 5. The tasklist follows suit. Fix: roadmap generation should produce finer phasing for richer inputs.
- **H2: The PRD supplementary block suppresses task creation.** The `build_tasklist_generate_prompt` PRD block says "PRD does not generate standalone implementation tasks" which may cause the LLM to consolidate tasks. Fix: reword the PRD instruction.
- **H3: Richer task descriptions substitute for task count.** The LLM puts more content INTO each task instead of creating MORE tasks. Each TDD+PRD task is 54.7 lines vs 38.9 for baseline. Fix: add decomposition guidance that maintains granularity regardless of content richness.
- **H4: The skill protocol version differs between branches.** The master branch may have a different decomposition algorithm. Fix: diff the protocols and align.
- **H5: Context window saturation.** The 746-line roadmap + TDD + PRD supplementary content fills more of the context window, leaving less room for task generation output. Fix: optimize prompt size or use chunked generation.

## OUTPUT

A research report answering:
1. Exactly why the TDD+PRD path produces fewer tasks (which hypothesis is correct)
2. Whether the issue is in the roadmap generation (fewer phases/items) or tasklist generation (coarser decomposition)
3. Specific code or prompt changes needed to fix the decomposition
4. Whether the fix is in `build_tasklist_generate_prompt`, the `/sc:tasklist` skill protocol, or the roadmap generation prompts
5. Expected impact: how many tasks should the TDD+PRD path produce, and what decomposition granularity is correct?

## CONTEXT FILES

| File | Why |
|------|-----|
| `.claude/skills/sc-tasklist-protocol/SKILL.md` | Tasklist generation algorithm, decomposition rules, phase bucketing |
| `src/superclaude/cli/tasklist/prompts.py` | `build_tasklist_generate_prompt` — TDD/PRD supplementary blocks |
| `.dev/test-fixtures/results/test3-spec-baseline/roadmap.md` | Baseline roadmap (380 lines, potentially 5 phases) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md` | TDD+PRD roadmap (746 lines, 3 phases) |
| `.dev/test-fixtures/results/test3-spec-baseline/tasklist-index.md` | Baseline tasklist index (87 tasks, 5 phases) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` | TDD+PRD tasklist index (44 tasks, 3 phases) |
| `.dev/test-fixtures/results/test3-spec-baseline/phase-1-tasklist.md` | Baseline phase 1 (16 tasks, for decomposition comparison) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-1-tasklist.md` | TDD+PRD phase 1 (27 tasks, for decomposition comparison) |
| `src/superclaude/cli/roadmap/prompts.py` | Roadmap generation prompts (may influence phase structure) |
