# Technical Research Report: Tasklist Generation Quality — Why Richer Input Produces Fewer Tasks

**Date:** 2026-04-03
**Depth:** Standard
**Research files:** 6 codebase + 0 web research
**Scope:** src/superclaude/cli/tasklist/prompts.py, src/superclaude/skills/sc-tasklist-protocol/SKILL.md, src/superclaude/cli/roadmap/prompts.py, .dev/test-fixtures/results/

---

## Table of Contents

1. [Problem Statement](#section-1----problem-statement)
2. [Current State Analysis](#section-2----current-state-analysis)
3. [Target State](#section-3----target-state)
4. [Gap Analysis](#section-4----gap-analysis)
5. [External Research](#section-5----external-research)
6. [Options Analysis](#section-6----options-analysis)
7. [Recommendation](#section-7----recommendation)
8. [Implementation Plan](#section-8----implementation-plan)
9. [Open Questions](#section-9----open-questions)
10. [Evidence Trail](#section-10----evidence-trail)

---

## Section 1 -- Problem Statement

### 1.1 Research Question

Why does the tasklist generation pipeline produce 49% fewer tasks from 4.1x richer input?

The `/sc:tasklist` skill generates 87 tasks from a 312-line spec-only input but only 44 tasks from 1,282 lines of combined TDD+PRD input. Enrichment content IS present in the 44 tasks (persona references, compliance markers, component cross-references), but the pipeline produces fewer, coarser tasks instead of more, finer-grained ones.
(`RESEARCH-PROMPT-tasklist-generation-quality.md`, lines 1-21)

### 1.2 Why It Matters

The TDD provides 876 lines of technical design: data models, API endpoint schemas, component inventories with class names, testing strategies with test IDs, migration rollback procedures, and operational readiness checklists. The PRD adds 406 lines of personas, success metrics, compliance requirements, and customer journeys. A pipeline that converts richer input into coarser output defeats the purpose of supplementary document support.
(`RESEARCH-PROMPT-tasklist-generation-quality.md`, lines 8-14)

### 1.3 Trigger

Comparison of two test-fixture runs on the same functional domain (user authentication):

- **Baseline** (`test3-spec-baseline/`): generated on `master` branch via `/sc:tasklist` from a spec-only roadmap.
- **TDD+PRD** (`test1-tdd-prd-v2/`): generated on `feat/tdd-spec-merge` branch via `/sc:tasklist` from a roadmap with TDD and PRD supplementary files.

(`RESEARCH-PROMPT-tasklist-generation-quality.md`, lines 26-42)

### 1.4 Evidence Table

| Metric | Spec-Only Baseline | TDD+PRD Enriched | Delta |
|--------|-------------------|------------------|-------|
| Input lines | 312 | 1,282 | +4.1x |
| Roadmap lines | 380 | 746 | +2.0x |
| Roadmap phases | 5 | 3 | -2 phases |
| Roadmap subsections (####) | 20 | 24 | +4 subsections |
| Roadmap work items (table rows) | ~87 | ~112 | +25 items |
| Roadmap item registry (R-###) | 87 | 44 | -43 items |
| Tasklist total lines | 3,380 | 2,407 | -29% |
| Total tasks | 87 | 44 | -49% |
| Total deliverables | 87 | 52 | -35 |
| Lines per task | ~27 | ~38 | +41% |
| R-item-to-task ratio | 1:1 | 1:1 | Same |
| Task-to-deliverable ratio | 1:1 | 1:1.18 | TDD+PRD splits deliverables |
| Persona references | 0 | 30 | Enrichment present |
| Compliance references | 0 | 35 | Enrichment present |
| Component references | 73 | 124 | +70% |
| Output bytes | 108,867 | 114,339 | +5% (denser) |
| Estimated output tokens | ~27,217 | ~28,585 | Near-identical |

Sources: `research/03-roadmap-phases.md` lines 145-164; `research/06-context-analysis.md` lines 117-126; `RESEARCH-PROMPT-tasklist-generation-quality.md` lines 15-21.

### 1.5 The Paradox

The TDD+PRD roadmap is nearly 2x longer (746 vs 380 lines) with MORE subsections (24 vs 20) and significantly MORE discrete work items (~112 vs 87), yet it produces fewer roadmap registry items (44 vs 87) and therefore fewer tasks. The enrichment is demonstrably present in the output (denser tasks, persona/compliance annotations, +70% component references), but the pipeline compresses rather than expands.
(`research/03-roadmap-phases.md`, lines 170-178; `research/04-task-decomposition.md`, lines 240-253)

---

## Section 2 -- Current State Analysis

### 2.1 Pipeline Architecture

The tasklist generation pipeline has two pathways:

| Pathway | Mechanism | When Used |
|---------|-----------|-----------|
| **Skill Protocol** (`/sc:tasklist`) | Interactive Claude Code session; SKILL.md loaded into context alongside user files | Both test-fixture runs used this pathway |
| **CLI Pipeline** (`superclaude roadmap run`) | `claude -p` subprocess; prompt passed as CLI argument | Not used for the test fixtures under analysis |

The skill protocol loads the full `SKILL.md` (63,273 bytes, ~15,818 tokens) into the session context. The CLI pipeline uses `build_tasklist_generate_prompt()` from `src/superclaude/cli/tasklist/prompts.py` (237 lines) to construct a much smaller prompt (~2,760 bytes when both TDD+PRD are present).
(`research/06-context-analysis.md`, lines 14-24, 29-56)

### 2.2 Protocol Decomposition Rules (SKILL.md)

The core decomposition algorithm lives in Section 4 of `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (1,273 lines on branch). The key rules, unchanged between `master` and `feat/tdd-spec-merge`:

| Step | Rule | Location |
|------|------|----------|
| 4.1 | Parse roadmap: extract phases, subsections, R-items | SKILL.md Section 4.1 |
| 4.2 | Phase bucketing: use explicit phase labels from roadmap headings, OR top-level `##` headings, OR default 3-bucket split | SKILL.md Section 4.2 (UNCHANGED between branches) |
| 4.4 | Core decomposition: 1 task per roadmap item by default; split only when item contains 2+ independently deliverable outputs | SKILL.md Section 4.4 (UNCHANGED between branches) |

(`research/01-protocol-diff.md`, lines 109-115)

The branch adds +122 net new lines in a single commit (`a9cf7ee`), all purely additive -- no lines removed or modified from master. Four new sections were inserted:

| New Section | Lines Added | Purpose | Behavioral Impact |
|-------------|------------|---------|-------------------|
| 3.x Source Document Enrichment | +20 | Conceptual framing for TDD/PRD enrichment | Descriptive only; no generation rules |
| 4.1a/4.1b/4.1c Data Extraction | +44 | Extract structured context keys from TDD (6 keys) and PRD (6 keys); auto-wire from `.roadmap-state.json` | Data extraction only; populates variables consumed downstream |
| 4.4a Supplementary TDD Task Generation | +25 (of 45) | 8 task patterns from TDD context keys (component inventory, migration stages, test pyramid, observability, DoD) | Additive: should INCREASE task count |
| 4.4b Supplementary PRD Task Generation | +20 (of 45) | 3 task patterns from PRD context keys (user stories, success metrics, acceptance scenarios) | Mixed: merge-first strategy may suppress net creation |
| Stage 7 TDD Validation Extension | +13 | 4 new validation checks when `--spec` was provided | Validation-only; no generation impact |

(`research/01-protocol-diff.md`, lines 29-104)

### 2.3 Merge Instructions -- The Consolidation Mechanism

The branch additions contain five explicit merge/consolidation instructions that create a strong LLM-behavioral incentive to consolidate rather than expand:

| Location | Instruction Text | Risk |
|----------|-----------------|------|
| 4.4a header | "Merge rather than duplicate if a generated task duplicates an existing task for the same component" | MEDIUM -- could cause aggressive merging |
| 4.4b header | "Merge rather than duplicate if a generated task duplicates an existing task" | HIGH -- broader scope than 4.4a |
| 4.4b user_stories row | "merge with existing feature task if one covers the same goal" | HIGH -- vague "same goal" matching |
| 4.4b success_metrics row | "add as subtask or validation step on existing implementation tasks" | LOW -- adds to existing |
| 4.4b preamble | "do NOT generate standalone implementation tasks -- engineering tasks come from the roadmap; PRD enriches them" | HIGH -- explicitly suppresses task creation |

(`research/01-protocol-diff.md`, lines 149-159)

The protocol has **no minimum task count enforcement** and **no guard against over-merging**. The merge instructions are one-directional (merge when duplicate) with no floor to prevent the LLM from producing fewer tasks than roadmap items.
(`research/01-protocol-diff.md`, lines 163-176, 180-181)

### 2.4 Prompt-Level Handling of TDD/PRD

The `build_tasklist_generate_prompt()` function (`src/superclaude/cli/tasklist/prompts.py`, lines 151-237) follows this structure:

| Block | Lines | Task Creation Stance |
|-------|-------|---------------------|
| Base prompt (always included) | 171-184 | Expansive: "Each roadmap item should produce **one or more** tasks" |
| TDD enrichment block (conditional) | 187-202 | Additive: 5 dimensions, each says "each X should map to a task" |
| PRD enrichment block (conditional) | 204-224 | **Suppressive**: lines 221-223 say "PRD context ... does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them." |
| TDD+PRD interaction block (conditional) | 227-235 | Hierarchy: TDD = structural detail, PRD = context overlay that "shapes" existing tasks |
| Output format block (always) | imported | Formatting only; no task-count language |

(`research/02-tasklist-prompts.md`, lines 19-98, 100-145)

The PRD suppression language at lines 221-223 is the **only task-creation suppressor** in the entire prompt file. When combined with the interaction block (lines 229-234) that frames PRD as a "shaping" influence, the net effect is conflicting signals: TDD says create tasks for each artifact, PRD says do NOT create standalone tasks.
(`research/02-tasklist-prompts.md`, lines 69-79, 129-134)

No explicit consolidation words (`consolidate`, `merge`, `combine`, `group`, `high-level`) appear in the prompt file. The suppression is indirect -- constraining PRD's role to enrichment-only.
(`research/02-tasklist-prompts.md`, lines 101-109)

### 2.5 Roadmap Phase Structure and Its Downstream Effect

The tasklist generator exhibits **strict phase fidelity** -- it preserves roadmap phase count, names, and ordering with 1:1 accuracy and does not create its own phases.
(`research/03-roadmap-phases.md`, lines 83-109)

The two runs have fundamentally different phasing models because their input documents drove different adversarial debate outcomes:

| Dimension | Baseline (spec-only) | TDD+PRD (enriched) |
|-----------|---------------------|---------------------|
| Phase model | Technical layers (Foundation / Logic / Integration / Hardening / Production) | Delivery milestones (Internal Alpha / Beta 10% / GA 100%) |
| Phase count driver | No rollout strategy in spec; debate defaulted to build-up-the-stack layers | PRD provides rollout strategy; debate adopted progressive delivery |
| Debate metadata | Not recorded | `base_variant: "B (Haiku Architect)"`, `variant_scores: "A:71 B:79"`, convergence 0.72 |

(`research/03-roadmap-phases.md`, lines 64-79)

The roadmap generation prompt (`src/superclaude/cli/roadmap/prompts.py`, `build_generate_prompt()`, lines 380-483) provides **zero guidance** on phase count: no minimum, no maximum, no complexity-to-phase mapping, no consolidation instruction. Phase count is entirely determined by LLM inference.
(`research/05-roadmap-prompts.md`, lines 58-80, 226-232)

The PRD supplementary block in the roadmap prompt introduces value-based prioritization ("prioritize phases that deliver measurable business value earliest", line 471) which may push toward delivery-milestone phasing with fewer, broader phases.
(`research/05-roadmap-prompts.md`, lines 96-103)

### 2.6 Task Decomposition Patterns

Three functional areas were compared between the baseline (87 tasks) and TDD+PRD (44 tasks) tasklists:

| Area | Baseline Tasks | TDD+PRD Tasks | Consolidation Ratio | Primary Pattern |
|------|---------------|---------------|---------------------|-----------------|
| Login/authentication | 12 | 5 | 2.4:1 | Vertical integration: service logic + route handler + config + tests bundled into single component task |
| Password reset | 5 | 3 | 1.7:1 | Vertical integration: service layer + route handler merged into single endpoint task |
| Testing/QA | 28 standalone | 5 standalone | 5.6:1 | Testing absorption: tests embedded as `[VERIFICATION]` steps within implementation tasks instead of standalone tasks |

(`research/04-task-decomposition.md`, lines 56-65, 99-107, 167-176)

The testing/QA consolidation is the single largest driver of the task count difference. The baseline creates 28 standalone test tasks (unit tests per component, integration tests per flow, security tests per vector, coverage enforcement). The TDD+PRD version embeds testing within implementation tasks and creates only 5 standalone QA tasks (security checkpoint, manual testing, compliance audit, load testing, penetration testing).
(`research/04-task-decomposition.md`, lines 149-165)

If the TDD+PRD tasks were decomposed to baseline granularity, the projected count is ~73 tasks -- fewer than 87 because of genuine scope differences (frontend tasks in TDD+PRD with no baseline equivalent; production readiness tasks in baseline with no TDD+PRD equivalent).
(`research/04-task-decomposition.md`, lines 179-208)

### 2.7 Context Window and Output Budget

Context window saturation is **ruled out** as a contributing factor. The TDD+PRD scenario uses ~49K input tokens (24.5% of the 200K context window), leaving over 150K tokens available.
(`research/06-context-analysis.md`, lines 99-144)

Both scenarios produce approximately the same total output tokens (~27-29K), suggesting a consistent output budget. The model distributes this budget differently:
- **Without enrichment**: more tasks, less detail per task (~27 lines/task)
- **With enrichment**: fewer tasks, more detail per task (~38 lines/task, +41%)

(`research/06-context-analysis.md`, lines 147-157)

### 2.8 Where the Task Count Drops

The task count is determined by the **Roadmap Item Registry** (R-### items), not by subsection count, table row count, or line count. Both runs exhibit a perfect 1:1 mapping from R-items to tasks.

| Step | Baseline | TDD+PRD | Where Loss Occurs |
|------|----------|---------|-------------------|
| Input lines | 312 | 1,282 | TDD+PRD has 4.1x more |
| Roadmap lines | 380 | 746 | TDD+PRD has 2.0x more |
| Roadmap work items (~table rows) | ~87 | ~112 | TDD+PRD has ~29% more |
| **Roadmap R-### items** | **87** | **44** | **TDD+PRD has 49% FEWER -- loss occurs HERE** |
| Tasks | 87 | 44 | Mirrors R-items exactly (1:1 rule) |

(`research/03-roadmap-phases.md`, lines 116-139)

The loss is at the **roadmap generation** stage, not the tasklist generation stage. The TDD+PRD roadmap bundles more implementation detail per R-item (wiring tasks, integration docs, compliance checklists) and counts fewer discrete R-items despite having more total content. The tasklist generator then faithfully converts each R-item to exactly one task.
(`research/03-roadmap-phases.md`, lines 170-178)

The tasklist generator's consolidation mechanisms (SKILL.md 4.4a/4.4b merge instructions, prompt PRD suppression) may further reduce task count when supplementary tasks would have been additive, but the primary 49% reduction is inherited from the roadmap's coarser R-item registry.
(`research/01-protocol-diff.md`, lines 136-146; `research/03-roadmap-phases.md`, lines 186-192)

---

## Section 3 -- Target State

### 3.1 Principle

Richer input (TDD + PRD supplementary documents) should produce task output that is **at least as numerous** as the baseline (spec-only) while achieving **finer decomposition** -- more specific titles, embedded test scenarios, persona-tagged acceptance criteria, and TDD-traced deliverable IDs. Input enrichment must be additive: more detail in, more (or equal) tasks out, never fewer.

### 3.2 Success Criteria

| Criterion | Metric | Threshold | Rationale |
|-----------|--------|-----------|-----------|
| Task count floor | `total_tasks` (TDD+PRD) >= `total_tasks` (baseline) | >= 87 tasks | Baseline spec-only produces 87 from 312 input lines; 1,282 input lines must not produce fewer (research/03, Section 5) |
| Enrichment additionality | Tasks generated by 4.4a/4.4b supplementary rules | > 0 net new tasks | Protocol sections 4.4a (8 patterns) and 4.4b (3 patterns) are designed to ADD tasks; net-zero or net-negative violates intent (research/01, Section 2.3) |
| Phase count reflects content breadth | `total_phases` (TDD+PRD) >= `total_phases` (baseline) | >= 5 phases | TDD+PRD roadmap has 24 subsections and ~112 work items vs baseline's 20 subsections and 87 items; fewer phases contradicts content density (research/03, Section 2) |
| Testing task coverage | Standalone test/QA tasks | >= 15 standalone | Baseline produces 28 standalone test tasks; TDD+PRD produces 5 (5.6:1 consolidation). Floor of 15 preserves granular test tracking (research/04, Area C) |
| Roadmap item fidelity | `total_tasks` >= `roadmap_item_count` | 1:1 minimum | Both runs already exhibit 1:1 R-item-to-task ratio; the problem is that the TDD+PRD roadmap itself has only 44 R-items from ~112 work items (research/03, Section 5) |
| Deliverable richness | `total_deliverables` / `total_tasks` | >= 1.0 | TDD+PRD already achieves 1.18:1 (52 deliverables from 44 tasks); maintain or improve (research/03, Section 5) |

### 3.3 Projected Target Numbers

| Dimension | Current Baseline | Current TDD+PRD | Target TDD+PRD |
|-----------|-----------------|-----------------|----------------|
| Input lines | 312 | 1,282 | 1,282 (unchanged) |
| Roadmap R-items | 87 | 44 | >= 87 |
| Tasklist tasks | 87 | 44 | >= 87 |
| Phases | 5 | 3 | >= 5 |
| Standalone test tasks | 28 | 5 | >= 15 |
| Avg lines per task | 27 | 38 | 30-40 (richer is fine) |
| Deliverables | 87 | 52 | >= 87 |

---

## Section 4 -- Gap Analysis

### 4.1 Hypothesis Key

| ID | Hypothesis | Primary Evidence |
|----|-----------|-----------------|
| H1 | Roadmap phasing paradigm: PRD rollout strategy causes fewer, broader phases | research/03, Section 3 |
| H2 | PRD suppression language: "does NOT generate standalone implementation tasks" constrains task creation | research/02, Section 4 (lines 221-223) |
| H3 | Testing consolidation: 5.6:1 absorption of test tasks into implementation [VERIFICATION] steps | research/04, Area C |
| H4 | Protocol merge directives: "merge rather than duplicate" instructions cause aggressive consolidation | research/01, Section 4 |
| H5 | Roadmap granularity: TDD+PRD roadmap bundles ~112 work items into only 44 R-items | research/03, Section 7 |

### 4.2 Gap Table

| # | Gap | Current State | Target State | Severity | Hypothesis | Source |
|---|-----|--------------|--------------|----------|------------|--------|
| G1 | PRD suppression language in tasklist prompt | Lines 221-223 of `prompts.py`: "PRD context... does NOT generate standalone implementation tasks. Engineering tasks come from the roadmap; PRD enriches them." | PRD enrichment should ADD tasks (acceptance verification, metric instrumentation, persona-specific flows) and ANNOTATE existing tasks, but never suppress creation | **HIGH** | H2 | research/02, Section 4 |
| G2 | Protocol "merge rather than duplicate" directives (5 instances) | SKILL.md sections 4.4a/4.4b contain 5 merge/consolidation instructions with vague matching criteria ("same goal", "same component") | Merge only when task has identical component name AND identical deliverable type; all other cases keep separate | **HIGH** | H4 | research/01, Section 4 |
| G3 | No task count floor in protocol or prompts | Neither SKILL.md nor `prompts.py` asserts `total_tasks >= roadmap_items`; no post-generation validation check | Assert `len(all_tasks) >= len(roadmap_items)` after Steps 4.4/4.4a/4.4b; validation check in Stage 7 | **HIGH** | H4, H2 | research/01, Section 5 |
| G4 | No phase count guidance in roadmap generate prompt | `build_generate_prompt` says "Phased implementation plan with milestones" with zero count/minimum/maximum/complexity-mapping | Add complexity-to-phase-count heuristic (e.g., HIGH complexity -> 6-12 phases, MEDIUM -> 4-8) | **MEDIUM** | H1 | research/05, Section 3 |
| G5 | Roadmap R-item granularity not controlled | TDD+PRD roadmap bundles ~112 discrete work items into 44 R-items (2.5:1 bundling); baseline maps 87 items to 87 R-items (1:1) | R-items should map 1:1 to independently deliverable work items; bundling ratio should not exceed 1.5:1 | **HIGH** | H5 | research/03, Section 7 |
| G6 | Testing tasks absorbed into [VERIFICATION] steps | TDD+PRD produces 5 standalone test tasks vs baseline's 28 (5.6:1 ratio); coverage enforcement and security tests have no standalone tracking | Test pyramid levels (unit, integration, security, E2E) must each produce at least 1 standalone task per phase | **MEDIUM** | H3 | research/04, Area C |
| G7 | PRD scope boundary acts as task suppressor | `prompts.py` line 218-219: "tasks must not exceed defined scope; generate explicit 'out of scope' markers" may cause silent task dropping | Scope boundary should flag tasks, not drop them; tasks near scope edge produce warnings, not omissions | **MEDIUM** | H2 | research/02, Gap 5 |
| G8 | Section 3.x framing primes consolidation | SKILL.md Section 3.x describes enrichment as producing "more specific, actionable task decomposition" -- LLM may conflate "more specific" with "fewer" | Reframe: "enrichment adds specificity to existing tasks AND generates additional tasks from supplementary sources" | **LOW** | H2, H4 | research/01, Gap 5 |
| G9 | No anti-consolidation guard in prompts | No instruction in `prompts.py` says "supplementary documents should only ADD tasks or ADD detail, never reduce the number of tasks" | Add explicit anti-consolidation guard to base prompt and all supplementary blocks | **HIGH** | H2, H4 | research/02, Gap 4 |
| G10 | TDD+PRD interaction block amplifies suppression | Lines 229-234 of `prompts.py` frame PRD as "shapes task descriptions, acceptance criteria, and priority ordering" -- reinforces PRD as annotation-only | Reframe interaction block: TDD adds implementation tasks, PRD adds verification/acceptance tasks, both are generative | **MEDIUM** | H2 | research/02, Gap 2 |
| G11 | Output token ceiling causes redistribution | Both runs produce ~27-29K output tokens; model allocates fixed budget as fewer-denser (TDD+PRD) vs more-thinner (baseline) tasks | Not directly fixable; mitigate by splitting generation across phases (one LLM call per phase) or raising output token limit | **LOW** | -- | research/06, Section 5 |
| G12 | "Same goal" merge criterion is subjective | SKILL.md 4.4b user_stories: "merge with existing feature task if one covers the same goal" -- LLM-judgment-dependent, non-deterministic | Replace with structural matching: merge only when task title contains the same component name AND same verb (Implement/Configure/Verify) | **MEDIUM** | H4 | research/01, Gap 3 |

### 4.3 Gap-to-Hypothesis Heat Map

| Gap | H1 (Phasing) | H2 (PRD Suppression) | H3 (Test Consolidation) | H4 (Merge Directives) | H5 (R-item Granularity) |
|-----|:---:|:---:|:---:|:---:|:---:|
| G1  |     | **P** |     |     |     |
| G2  |     |     |     | **P** |     |
| G3  |     | S   |     | **P** |     |
| G4  | **P** |     |     |     |     |
| G5  |     |     |     |     | **P** |
| G6  |     |     | **P** |     |     |
| G7  |     | **P** |     |     |     |
| G8  |     | S   |     | S   |     |
| G9  |     | **P** |     | **P** |     |
| G10 |     | **P** |     |     |     |
| G11 |     |     |     |     |     |
| G12 |     |     |     | **P** |     |

**P** = primary mapping, S = secondary mapping

### 4.4 Severity Distribution

| Severity | Count | Gaps |
|----------|-------|------|
| HIGH | 5 | G1, G2, G3, G5, G9 |
| MEDIUM | 5 | G4, G6, G7, G10, G12 |
| LOW | 2 | G8, G11 |

---

## Section 5 -- External Research

N/A -- this investigation is codebase-only. All evidence was gathered from source files (`src/superclaude/cli/tasklist/prompts.py`, `src/superclaude/cli/roadmap/prompts.py`, `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`), test fixture outputs (`.dev/test-fixtures/results/`), and git history. No external documentation, academic literature, or third-party tool analysis was required.

---

## Section 6 -- Options Analysis

### 6.1 Option A: Fix Tasklist Prompt (`prompts.py` only)

**Scope:** Modify `src/superclaude/cli/tasklist/prompts.py` to remove suppression language and add anti-consolidation guards.

**Changes:**

| Change | File | Lines | Description |
|--------|------|-------|-------------|
| A1 | `prompts.py` | 221-223 | Remove or rewrite PRD suppression: "does NOT generate standalone implementation tasks" -> "PRD-derived acceptance scenarios, metric instrumentation tasks, and persona-specific verification tasks are generated as NEW tasks in addition to roadmap-derived tasks" |
| A2 | `prompts.py` | 229-234 | Rewrite TDD+PRD interaction block: remove "shapes task descriptions" framing; replace with "TDD generates implementation tasks, PRD generates verification and acceptance tasks, both are additive" |
| A3 | `prompts.py` | after 184 | Add anti-consolidation guard to base prompt: "Supplementary documents (TDD, PRD) must only ADD tasks or ADD detail to existing tasks. They must NEVER reduce the total task count below what the roadmap alone would produce." |
| A4 | `prompts.py` | 218-219 | Soften scope boundary: "Flag tasks near scope edges with a scope-warning marker rather than omitting them" |

| Dimension | Assessment |
|-----------|-----------|
| Effort | **Small** -- 4 edits in 1 file (~20 lines changed) |
| Risk | **Low** -- prompt changes are non-breaking; worst case is over-generation (too many tasks, easily trimmed) |
| Gaps addressed | G1, G7, G9, G10 (4 of 12) |
| Gaps NOT addressed | G2, G3, G4, G5, G6, G8, G11, G12 (8 of 12) -- protocol merge directives, task count floor, phase count, R-item granularity, testing consolidation, SKILL.md framing |
| Pros | Minimal code change; directly addresses the strongest root cause (H2 PRD suppression); easy to A/B test |
| Cons | Does not fix protocol-level merge directives (H4); does not address roadmap-level R-item bundling (H5); does not add task count floor (G3) |

---

### 6.2 Option B: Fix Protocol (`SKILL.md` only)

**Scope:** Modify `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` to add task count floor, tighten merge criteria, and add testing task minimums.

**Changes:**

| Change | File | Section | Description |
|--------|------|---------|-------------|
| B1 | SKILL.md | new 4.4c | Add post-generation floor: "After Steps 4.4, 4.4a, and 4.4b, assert: `len(all_tasks) >= len(roadmap_items)`. If violated, re-run Step 4.4 without merge instructions." |
| B2 | SKILL.md | 4.4a header | Tighten merge criterion: "Merge ONLY when two tasks share identical component name AND identical deliverable type (Implement/Configure/Verify). When in doubt, keep separate." |
| B3 | SKILL.md | 4.4b header | Replace broad "merge rather than duplicate" with: "PRD-derived tasks are ALWAYS created as new tasks. Merge is permitted ONLY for user_stories when an existing task has an identical actor AND identical goal verb." |
| B4 | SKILL.md | 4.4b preamble | Remove "do NOT generate standalone implementation tasks" and replace with: "PRD generates acceptance and verification tasks alongside roadmap-derived implementation tasks." |
| B5 | SKILL.md | Stage 7 | Add validation check: "Total task count must be >= 1.0x parsed roadmap item count. Finding level: HIGH if violated." |
| B6 | SKILL.md | 4.4a | Add testing task rule: "Each test pyramid level (unit, integration, E2E, security) referenced in `testing_strategy` must produce at least one standalone task per phase that contains implementation tasks." |
| B7 | SKILL.md | 3.x | Reframe enrichment description: "Enrichment adds specificity to existing tasks AND generates additional tasks from supplementary sources. Enrichment must NEVER reduce the total task count." |

| Dimension | Assessment |
|-----------|-----------|
| Effort | **Medium** -- 7 edits in 1 file (~60 lines changed), requires `make sync-dev` after |
| Risk | **Medium** -- protocol changes affect all skill-protocol-based generation; if over-specified, could cause task inflation or formatting issues |
| Gaps addressed | G2, G3, G6, G8, G12 (5 of 12) |
| Gaps NOT addressed | G1, G4, G5, G7, G9, G10, G11 (7 of 12) -- tasklist prompt suppression (H2), anti-consolidation guard in prompts (G9), roadmap phase count (H1), R-item granularity (H5) |
| Pros | Adds structural guardrails (task count floor, validation check) that are harder for LLM to ignore; tightens merge criteria with objective matching rules; addresses testing consolidation |
| Cons | Does not fix the tasklist prompt's PRD suppression language (the single strongest root cause per research/02); protocol is advisory to LLM, not enforced programmatically; does not fix roadmap-level issues (H1, H5) |

---

### 6.3 Option C: Fix Both + Add Roadmap Phase Count Guidance

**Scope:** Apply all changes from Options A and B, plus add phase count guidance to the roadmap generation prompt.

**Changes:**

All changes from Option A (A1-A4) + all changes from Option B (B1-B7) + the following:

| Change | File | Section | Description |
|--------|------|---------|-------------|
| C1 | `roadmap/prompts.py` | `build_generate_prompt`, after line 427 | Add phase count heuristic: "Target phase count based on complexity: LOW -> 3-5 phases, MEDIUM -> 4-8 phases, HIGH -> 6-12 phases. When TDD and/or PRD supplementary documents are present, phase count should be >= the count that the roadmap would produce from the spec alone." |
| C2 | `roadmap/prompts.py` | `build_generate_prompt`, TDD block | Add: "Each TDD category (Data Models, API Specs, Components, Testing, Migration, Operations) that contains substantive content should map to at least one phase or sub-phase." |
| C3 | `roadmap/prompts.py` | `build_merge_prompt`, after line 626 | Add: "The merged roadmap must have at least as many phases as the variant with MORE phases. Do not collapse phases during merge." |

| Dimension | Assessment |
|-----------|-----------|
| Effort | **Large** -- 14 total edits across 3 files (~100 lines changed), requires `make sync-dev`, testing across both pathways (CLI + skill protocol) |
| Risk | **Medium** -- highest coverage but more moving parts; phase count heuristic may need tuning per complexity class; roadmap prompt changes affect the upstream pipeline (roadmap affects tasklist downstream) |
| Gaps addressed | G1, G2, G3, G4, G6, G7, G8, G9, G10, G12 (10 of 12) |
| Gaps NOT addressed | G5 (R-item granularity -- requires roadmap decomposition rule changes, out of scope for prompt/protocol fix), G11 (output token ceiling -- model constraint, not fixable via prompts) |
| Pros | Comprehensive fix across all three root cause layers (prompt, protocol, roadmap); addresses 10 of 12 gaps; adds both soft guidance and hard guardrails |
| Cons | Largest change surface; risk of over-specification causing rigid behavior; roadmap prompt changes are upstream and affect all downstream artifacts (not just tasklists); requires more thorough testing |

---

### 6.4 Comparison Table

| Dimension | Option A (Prompt) | Option B (Protocol) | Option C (Both + Roadmap) |
|-----------|:-----------------:|:-------------------:|:-------------------------:|
| Files changed | 1 | 1 | 3 |
| Lines changed | ~20 | ~60 | ~100 |
| Effort | Small | Medium | Large |
| Risk | Low | Medium | Medium |
| Gaps addressed | 4/12 | 6/12 | 10/12 |
| H1 (Phasing) addressed | No | No | **Yes** |
| H2 (PRD Suppression) addressed | **Yes** | Partial | **Yes** |
| H3 (Test Consolidation) addressed | No | **Yes** | **Yes** |
| H4 (Merge Directives) addressed | No | **Yes** | **Yes** |
| H5 (R-item Granularity) addressed | No | No | No* |
| Strongest root cause (H2) fixed | **Yes** | No | **Yes** |
| Task count floor added | No | **Yes** | **Yes** |
| Phase count guidance added | No | No | **Yes** |
| Requires `make sync-dev` | No | Yes | Yes |
| A/B testable in isolation | **Yes** | **Yes** | Requires staged rollout |

*G5 (R-item granularity) requires changes to the roadmap decomposition algorithm, which is outside the scope of prompt/protocol fixes. It would require a separate investigation into roadmap generation rules.

---

## Section 7 -- Recommendation

### 7.1 Selected Option: **Option C (Fix Both + Roadmap Phase Count Guidance)**

### 7.2 Rationale

**Option C is recommended** despite being the largest change because the research demonstrates the problem is multi-layered, not single-cause:

1. **The strongest single root cause is H2 (PRD suppression in `prompts.py`)**, identified in research/02 as lines 221-223. Option A alone would fix this, but research/01 shows the protocol's 5 merge directives (H4) independently cause consolidation even if the prompt is fixed. Fixing only the prompt leaves the protocol-level merge problem intact.

2. **The task count floor (G3) is essential and only exists in Options B and C.** Without a programmatic assertion that `total_tasks >= roadmap_items`, the LLM can still under-generate due to emergent consolidation behavior. The floor is the single most important guardrail because it catches the symptom regardless of which root cause triggers it.

3. **Phase count guidance (G4) addresses the upstream problem.** Research/03 shows the TDD+PRD roadmap has only 3 phases (from ~112 work items) while the baseline has 5 phases (from 87 work items). Research/05 confirms zero phase-count guidance exists in `build_generate_prompt`. Since the tasklist generator exhibits strict phase fidelity (1:1 roadmap-to-tasklist phase mapping, per research/03 Section 4), fixing phase count at the roadmap level propagates downstream automatically. This is only available in Option C.

4. **Testing consolidation (G6) drives the largest single category of task loss.** The 5.6:1 testing absorption (28 standalone test tasks -> 5) accounts for 23 of the 43 missing tasks -- over half the deficit. Option B's testing task rule (B6) directly addresses this. Option A does not.

5. **The two unaddressed gaps (G5, G11) are acceptable residual risk.** G5 (R-item granularity) requires deeper changes to roadmap decomposition rules and warrants a separate investigation. G11 (output token ceiling) is a model constraint that cannot be fixed via prompts; the mitigation (per-phase generation) is an architectural change outside this scope.

### 7.3 Implementation Sequence

Option C should be implemented in two stages to enable incremental A/B testing:

| Stage | Changes | Files | Test Method |
|-------|---------|-------|-------------|
| Stage 1 | A1-A4 (prompt fixes) + B1-B7 (protocol fixes) | `prompts.py`, SKILL.md | Re-run TDD+PRD test fixture; compare task count against baseline 87 |
| Stage 2 | C1-C3 (roadmap phase count guidance) | `roadmap/prompts.py` | Re-run full pipeline (roadmap + tasklist) from same TDD+PRD inputs; compare phase count and downstream task count |

Stage 1 addresses 10/12 gaps at the tasklist level. Stage 2 addresses the remaining upstream phase count gap. If Stage 1 alone raises task count to >= 87, Stage 2 can be deferred.

### 7.4 Expected Outcome

| Metric | Current TDD+PRD | After Stage 1 | After Stage 2 |
|--------|----------------|---------------|---------------|
| Total tasks | 44 | >= 70 (est.) | >= 87 |
| Phases | 3 | 3 (unchanged -- roadmap not re-run) | >= 5 |
| Standalone test tasks | 5 | >= 15 | >= 15 |
| PRD-derived new tasks | 0 | > 0 (acceptance, metrics, persona flows) | > 0 |
| TDD-derived new tasks | 0 net (all merged) | > 0 net (stricter merge criteria) | > 0 net |

### 7.5 Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Over-generation (too many trivial tasks) | Task count floor is a MINIMUM, not a target; quality review in Stage 7 validation still applies |
| Phase count heuristic too rigid | Use ranges (6-12 for HIGH), not exact targets; "at least as many as spec-only" is a floor, not a ceiling |
| Protocol changes cause formatting regressions | Run existing test fixtures through both pathways (CLI + skill protocol) before and after changes; compare YAML frontmatter structure |
| Staged rollout creates partial-fix confusion | Document Stage 1 as a standalone improvement; Stage 2 is additive and independent |

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
| PRD scope expansion (inverse problem) | Removing PRD suppression language could cause PRD-derived requirements to generate tasks that expand beyond the roadmap's defined scope -- the inverse of the current under-generation problem. Mitigation: the scope boundary instruction at prompts.py lines 218-219 (softened per Step 9 but not removed) still flags scope-adjacent tasks. Additionally, the Stage 7 validation checks roadmap-to-tasklist alignment and would flag tasks with no corresponding roadmap item as HIGH severity deviations. Monitor first 3 TDD+PRD runs for tasks that lack R-item traceability. |

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
| 01 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/01-protocol-diff.md` | SKILL.md protocol diff (master vs feat/tdd-spec-merge) | Code Tracer | 205 | +122 additive lines in commit a9cf7ee. Core decomposition rules (4.4) and phase bucketing (4.2) unchanged. New sections 4.4a/4.4b add "merge rather than duplicate" instructions that incentivize consolidation. No task count floor exists. |
| 02 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/02-tasklist-prompts.md` | Tasklist generation prompt analysis | Code Tracer | 177 | Lines 221-223 of `prompts.py` contain the only task-suppression language: "PRD does NOT generate standalone implementation tasks." TDD block is purely additive. PRD block suppresses. Interaction block amplifies suppression. |
| 03 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/03-roadmap-phases.md` | Roadmap phase structure comparison | Pattern Investigator | 202 | 3 phases (TDD+PRD) vs 5 phases (baseline) driven by PRD rollout strategy (Alpha/Beta/GA) vs technical-layer decomposition. Tasklist generator has strict 1:1 phase fidelity. Both runs show perfect 1:1 R-item-to-task ratio. |
| 04 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/04-task-decomposition.md` | Task decomposition granularity comparison | Pattern Investigator | 282 | TDD+PRD operates at 2-3x coarser granularity for implementation (vertical integration pattern) and 5-6x coarser for testing (absorption pattern: 28 standalone -> 5). Projected ~73 tasks if decomposed to baseline granularity. |
| 05 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/05-roadmap-prompts.md` | Roadmap prompt phase count analysis | Code Tracer | 234 | Zero phase count guidance in `build_generate_prompt`. No minimum, maximum, complexity mapping, or consolidation instructions. Phase count is entirely LLM-inferred. PRD prioritization language may cause emergent consolidation. |
| 06 | `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/research/06-context-analysis.md` | Context window saturation analysis | Architecture Analyst | 197 | Context saturation ruled out (24.5% utilization, 150K+ tokens remaining). Both scenarios produce ~28K output tokens. Output token ceiling is the binding constraint, not context window. Fewer tasks with more detail per task = output budget reallocation. |

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
| `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/qa/qa-synthesis-gate-report.md` | QA gate for synthesis phase |
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
