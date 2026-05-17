# Synthesis Report: Sections 1-2

**Date:** 2026-04-03
**Source files:** research/01 through 06, gaps-and-questions.md, RESEARCH-PROMPT-tasklist-generation-quality.md
**Scope:** Problem statement and current-state analysis of the tasklist generation pipeline

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
