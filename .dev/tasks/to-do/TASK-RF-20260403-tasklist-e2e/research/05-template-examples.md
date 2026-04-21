# R05: Template & Prior Task Examples

**Status:** Complete
**Researcher:** r05
**Track Goal:** Build a task file that generates and validates tasklists with TDD/PRD enrichment
**Sources:**
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` (MDTM template 02)
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` (prior E2E task)

---

## 1. MDTM Template 02 Structure

Template 02 is the "complex task" template. It extends template 01 with Section L (Intra-Task Handoff Patterns) for tasks requiring discovery, testing, review, conditional logic, or aggregation between checklist items.

### 1.1 Two-Part Architecture

The template file has two distinct parts:
- **Part 1 (lines 46-893):** Builder instructions -- rules, principles, patterns. This content is NEVER included in the output task file.
- **Part 2 (lines 894-end):** The actual task file template to copy and populate.

### 1.2 Required Frontmatter Fields

```yaml
---
id: "TASK-[AGENT]-[TASKTYPE]-YYYYMMDD-HHMMSS"
title: "[Clear, Action-Oriented Task Title]"
description: "[Detailed description]"
status: "To Do"
type: "Documentation"       # or verification, implementation, etc.
priority: "High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "[agent-name]"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: "[PARENT-TASK-ID]"
depends_on: []
related_docs: []
tags: []
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static           # or "dynamic" for discovery tasks
---
```

**Note from prior E2E task:** The actual task used a simplified frontmatter with different field names (e.g., `status: done` not emoji, `type: verification`, `template: complex`, `estimated_items: 67`, `estimated_phases: 11`, `handoff_dir`). The builder should follow the prior task's actual frontmatter pattern, not the template's placeholder pattern, since that is what the executor expects.

### 1.3 Required Body Sections (Part 2 Output Structure)

The output task file MUST contain these sections in order:

1. **`# [Task Title]`** -- H1 heading matching frontmatter title
2. **`## Task Overview`** -- Comprehensive description (one paragraph, dense)
3. **`## Key Objectives`** -- Numbered list of specific outcomes
4. **`## Prerequisites & Dependencies`** -- Parent task, blocking deps, previous stage outputs, handoff file convention, frontmatter update protocol
5. **`## Detailed Task Instructions`** -- Contains all phases with checklist items
   - `### Phase 1: Preparation and Setup` -- always first
   - `### Phase 2: [Main Execution Phase]` -- domain-specific
   - `### Phase Gate: Quality Verification` -- between phases when outputs chain
   - `### Phase N: [Additional Phases]`
6. **`## Post-Completion Actions`** -- 4 standard items (verify outputs, run tests if code changed, write task summary, update frontmatter)
7. **`## Task Log / Notes`** -- Contains Task Summary template, Execution Log, Phase Findings sections, Follow-Up Items, Deviations

### 1.4 Sections That Must NOT Exist

- No separate "Outputs & Deliverables" section (embed in items per C1)
- No separate "Success Criteria" section (embed as "ensuring..." clauses per C2)
- No separate "Verification Checklist" section (embed in items per C3)
- No separate "Task Completion and Handoff Protocol" section (per C4)
- No checklist items before Phase 1 begins (per D3)

---

## 2. Checklist Item Format Rules

### 2.1 A3 Granularity Rule

> Break down EVERY workflow phase into atomic, verifiable checklist items. Create individual checklist items for EVERY file, component, or iteration. NO high-level or bulk operations -- everything must be granular. Include exact file paths, specific requirements, and measurable outcomes.

### 2.2 B2 Self-Contained Rule (CRITICAL)

Every checklist item must be a complete, self-contained prompt containing ALL 6 elements:

1. **Context Reference + WHY** -- What file(s) to read and why
2. **Action + WHY** -- What to do with that context and why
3. **Output Specification** -- Exact file path, content requirements, template
4. **Integrated Verification** -- "ensuring..." clause (no fabrication, 100% accuracy from source)
5. **Evidence on Failure Only** -- Log to task notes ONLY if blocked (output file IS the success evidence)
6. **Explicit Completion Gate** -- "Once done, mark this item as complete."

### 2.3 Format Requirements

- Each item is ONE FULL PARAGRAPH (not multi-line/bulleted)
- Items use `- [ ]` checkbox format with bold numbering: `- [ ] **X.Y**`
- No nested checkboxes (flat structure only)
- No parent checkboxes summarizing children
- Summary items come AFTER component items, never before
- No standalone "read context" items (context must be embedded in action items)
- No separate verification/confirmation items
- No REMINDER blocks between items (embed reminders in the item itself)

### 2.4 Error Handling Pattern

Every item ends with: "If unable to complete due to [specific failure modes], log the specific blocker using the templated format in the ### Phase N Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete."

---

## 3. Section L: Intra-Task Handoff Patterns (Template 02 Exclusive)

Template 02 adds 6 handoff patterns for complex cross-item data flow:

| Pattern | Code | Use Case | Output Directory |
|---------|------|----------|-----------------|
| Discovery | L1 | Explore codebase/data, produce structured findings | `phase-outputs/discovery/` |
| Build-from-Discovery | L2 | Create output using discovered info | varies |
| Test/Execute | L3 | Run commands, capture raw + summary output | `phase-outputs/test-results/` |
| Review/QA | L4 | Assess quality against source materials | `phase-outputs/reviews/` |
| Conditional-Action | L5 | Branch based on previous results (handle BOTH paths) | `phase-outputs/plans/` |
| Aggregation | L6 | Consolidate multiple outputs into single report | `phase-outputs/reports/` |

**Common phase structures:**
- Discovery -> Build -> Review: L1 -> L2 -> L4 -> L6
- Build -> Test -> Fix: Build -> L3 -> L5
- Full lifecycle: L1 -> L2 -> L3 -> L5 -> L4 -> L6

**Handoff directory:** `.dev/tasks/TASK-NAME/phase-outputs/` with subdirectories `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/`.

---

## 4. Phase Pattern from Prior E2E Task

The prior E2E task (TASK-E2E-20260402) had 11 phases, 67 items, and demonstrates the actual pattern in practice:

| Phase | Name | Items | Pattern Type |
|-------|------|-------|-------------|
| 1 | Preparation and CLI Verification | 7 | L3 (test/execute) |
| 2 | Create PRD Test Fixture | 3 | Build + L3 (verify) |
| 3 | Dry-Run Verification with PRD Flag | 8 | L3 (test) + L6 (aggregate go/no-go) |
| 4 | Test 1 -- Full TDD+PRD Pipeline Run | 14 | L3 (execute) + L4 (review each artifact) + L6 (summary) |
| 5 | Test 2 -- Full Spec+PRD Pipeline Run | 9 | Same as Phase 4, narrower scope |
| 6 | Auto-Wire from .roadmap-state.json | 6 | L3 (test) + L6 (summary) |
| 7 | Tasklist Validation Enrichment Testing | 6 | L3 (test) + L6 (summary) |
| 8 | TDD+PRD vs TDD-Only Comparison | 5 | L4 (review/compare) + L6 (summary) |
| 9 | Cross-Pipeline Comparison | 4 | L6 (aggregate) |
| 10 | Final Verification Report | 3 | L6 (aggregate) |
| 11 | Completion | 2 | Post-completion |

### 4.1 Phase Header Pattern

Each phase has:
```markdown
## Phase N: [Name] (X items)

> **Purpose:** [Dense description of what this phase accomplishes]
>
> **Handoff input:** [What prior phase outputs feed into this phase]
> **Known limitation:** [If applicable]

- [x] **N.1** [Self-contained item text...]
- [x] **N.2** [Self-contained item text...]
```

### 4.2 Item Numbering

Items use `**N.M**` bold numbering (phase.item). The prior task occasionally used letter suffixes for inserted items (e.g., `4.5a`, `4.5b`, `4.5c`, `4.9a`, `4.9b`). The last item in each phase is typically a summary/aggregation item.

---

## 5. Lessons from Prior E2E Task

### 5.1 What Worked Well

1. **Dense self-contained items** -- Each item was a full paragraph with context refs, action, output path, verification, and completion gate. This enabled session-independent execution.
2. **Phase-output handoff files** -- Every test result was written to `phase-outputs/test-results/phaseN-*.md`, enabling later comparison phases to read structured results.
3. **Go/No-Go gates** -- Phase 3 ended with a go/no-go decision item before committing to 30-60 minute pipeline runs.
4. **Per-phase summary items** -- Each phase ended with a summary/aggregation item writing to `phase-outputs/reports/`.
5. **Known issues documented upfront** -- The Task Overview explicitly called out expected failures (anti-instinct gate) and limitations (no `tasklist generate` CLI).
6. **Sentinel checks for fixtures** -- Phase 2 included grep-based sentinel checks to validate fixture content before using it.

### 5.2 What Went Wrong -- Critical Lesson for New Task

**Phase 6/7 ran `tasklist validate` with no tasklist to validate.**

The prior E2E task's Phases 6 and 7 tested `uv run superclaude tasklist validate` against pipeline output directories. The `tasklist validate` command validates a *tasklist* against a roadmap for fidelity. However, the pipeline output directories contained roadmap artifacts (extraction.md, roadmap.md, etc.) but NO generated tasklist. There is no `superclaude tasklist generate` CLI command -- tasklist generation is inference-only via the `/sc:tasklist` skill.

This means:
- Phase 6 auto-wire tests ran `tasklist validate` against directories that had no tasklist
- Phase 7 enrichment tests compared "enriched" vs "baseline" fidelity on nonexistent tasklists
- The "enrichment" being tested was the fidelity prompt's supplementary blocks, not actual tasklist content

**Lesson for the new task:** The new task MUST generate tasklists FIRST (via the `/sc:tasklist` skill or the `build_tasklist_generate_prompt` function) before running `tasklist validate`. The sequence must be:

1. Run roadmap pipeline to produce roadmap artifacts
2. Generate tasklist from roadmap (using the generate prompt or skill)
3. THEN validate the generated tasklist with `tasklist validate`

### 5.3 Known Limitation: No `tasklist generate` CLI

The prior task documented this explicitly:

> There is NO `superclaude tasklist generate` CLI command. Tasklist generation is inference-only via the `/sc:tasklist` skill. Only `superclaude tasklist validate` is testable as a CLI pipeline.

The new task must work around this by either:
- Using the `build_tasklist_generate_prompt` function directly (tested in prior task item 7.5)
- Using the `/sc:tasklist` skill to generate a tasklist
- Or testing only the validation path with a pre-created tasklist fixture

### 5.4 QA Focus: Pipeline Behavior, Not Report Prose

The build request specifies: **QA should focus on pipeline behavior, not report prose.** This means:
- Test that commands run without errors (exit codes, no tracebacks)
- Test that output files are created at expected paths
- Test that frontmatter fields contain expected values
- Test that enrichment blocks appear/don't appear based on flags
- Do NOT spend items on prose quality review of generated content
- Do NOT create review items that assess writing quality of pipeline outputs

---

## 6. Template Compliance Checklist for Builder

When building the new task file, verify:

- [ ] Frontmatter has all required fields (follow prior task pattern, not raw template placeholders)
- [ ] Task Overview is a single dense paragraph
- [ ] Key Objectives are numbered with specific outcomes
- [ ] Prerequisites section lists all dependencies and handoff conventions
- [ ] No checklist items appear before Phase 1
- [ ] Every item follows B2 six-element self-contained pattern
- [ ] Every item is one paragraph (no multi-line bullets)
- [ ] Phase headers include item count and Purpose blockquote
- [ ] Last item per phase is a summary/aggregation item
- [ ] Post-Completion Actions section has the 4 standard items
- [ ] Task Log has Phase Findings sections for every phase
- [ ] Tasklist generation happens BEFORE tasklist validation (fix prior task's sequencing error)
- [ ] QA items focus on pipeline behavior (exit codes, file existence, field values), not prose quality
