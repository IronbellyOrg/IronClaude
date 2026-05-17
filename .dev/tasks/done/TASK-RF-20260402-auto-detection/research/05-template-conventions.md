# 05 - MDTM Template Conventions Research

**Researcher**: researcher-5 (template conventions)
**Date**: 2026-04-01
**Goal**: Document template 02 (complex task) structure for the task builder to create C-122 auto-detection task file

---

## 1. Template Availability in IronClaude

The `.gfdoc/templates/` directory does NOT exist in IronClaude. However, the templates ARE available at:
- `.claude/templates/workflow/01_mdtm_template_generic_task.md` (simple tasks)
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` (complex tasks)

Source: `.claude/agent-memory/rf-task-builder/template-notes.md` (lines 9-13) documents this situation and provides a fallback strategy.

---

## 2. Template 02 Structure: PART 1 (Building Instructions)

Template 02 is a two-part document. PART 1 (lines 46-830) contains instructions for the task BUILDER. PART 2 (lines 882+) is the actual task file template. PART 1 is enclosed in an HTML comment block and NEVER appears in the output task file.

### 2.1 Key Rules from PART 1

**A3 — Complete Granular Breakdown** (lines 91-95):
- Break down EVERY phase into atomic, verifiable checklist items
- Create individual items for EVERY file, component, or iteration
- NO high-level or bulk operations
- Include exact file paths, specific requirements, and measurable outcomes

**A4 — Iterative Process Structure** (lines 97-116):
- Pre-enumerate ALL items in initial step
- Create individual checklist item for each specific item
- Require incremental updates after each item
- Include consolidation step only after all items complete

**B2 — Self-Contained Item Pattern** (lines 142-148):
Every checklist item MUST contain these 6 elements in ONE PARAGRAPH:
1. **Context Reference with WHY** — What file(s) to read and why
2. **Action with WHY** — What to do with that context and why
3. **Output Specification** — Exact output file name, location, content, template
4. **Integrated Verification** — "ensuring..." clause (no fabrication, 100% accuracy from sources)
5. **Evidence on Failure Only** — Log to task notes ONLY if blocked
6. **Explicit Completion Gate** — "Once done, mark this item as complete."

**B5 — Forbidden Patterns** (lines 164-184):
- Standalone "read context" items that don't produce output
- Missing context references
- Multi-line/bulleted checklist items (must be single paragraph)
- Separate verification/confirmation items
- Overly granular items (e.g., "create directory" alone)
- Separate REMINDER blocks between checklist items

---

## 3. YAML Frontmatter Requirements

From template 02 (lines 1-44) and existing task files:

### Minimum Required Fields (from precedent analysis)
```yaml
---
id: TASK-RF-YYYYMMDD-<slug>
title: "Descriptive Title -- Subtitle with Scope"
status: to-do
priority: high
created: YYYY-MM-DD
type: implementation
template: complex
estimated_items: <integer>
estimated_phases: <integer>
---
```

### Optional Fields (present in template, used when applicable)
```yaml
completion_date: ""
start_date: ""
updated_date: ""
assigned_to: ""
parent_task: ""
depends_on: []
related_docs: []
tags: []
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
blocker_reason: ""
task_type: static   # or "dynamic"
```

### Frontmatter Update Protocol (lines 447-454, 946-954):
- On start: `status` -> "in-progress" (or emoji form), set `start_date`
- On completion: `status` -> "done" (or qualified like `done-cli-layer`), set `completion_date`
- If blocked: `status` -> "blocked", populate `blocker_reason`
- After each session: update `updated_date`

---

## 4. PART 2: Task File Structure (Output Template)

From lines 882-1096, the actual task file structure is:

```markdown
# [Task Title]

## Task Overview
[Comprehensive description]

## Key Objectives
1. **[Objective 1]:** [Specific outcome]
2. **[Objective 2]:** [Specific outcome]

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** [ID]
- **Blocking Dependencies:** [list]

### Previous Stage Outputs (MANDATORY INPUTS)
[Informational only - no checklist items here]

### Handoff File Convention
[Describes .dev/tasks/TASK-NAME/phase-outputs/ subdirectories]

### Frontmatter Update Protocol
[Standard protocol description]

## Detailed Task Instructions

### Phase 1: Preparation and Setup
- [ ] **1.1** Update status and start_date...
- [ ] **1.2** Create handoff directory structure...

### Phase 2: [Main Execution Phase]
- [ ] **2.1** [Discovery item - L1 pattern]
- [ ] **2.2** [Build item - L2 pattern]
- [ ] **2.3** [Test item - L3 pattern]
- [ ] **2.4** [Assess item - L5 pattern]

### Phase Gate: Quality Verification
- [ ] [QA gate item]

### Phase N: [Subsequent phases...]

## Post-Completion Actions
- [ ] Post-completion validation items (I17)
- [ ] Frontmatter update to done

## Task Log / Notes

### Execution Log
| Timestamp | Phase | Item | Status | Notes |

### Phase 2 Findings
_No findings yet._

### Phase N Findings
_No findings yet._
```

---

## 5. Section L: Intra-Task Handoff Patterns (Template 02 Differentiator)

Template 02 extends Template 01 with Section L (lines 711-830). These patterns enable complex inter-item data flow via persisted handoff files.

### Handoff File Convention (lines 718-730)
All outputs go to `.dev/tasks/TASK-NAME/phase-outputs/` with subdirectories:
- `discovery/` — Scan results, inventories, findings
- `test-results/` — Test output, summaries
- `reviews/` — Quality review verdicts
- `plans/` — Fix plans, conditional action outputs
- `reports/` — Aggregated reports, summaries

### Pattern Catalog

| Pattern | ID | When to Use | Output Location |
|---------|-----|------------|-----------------|
| Discovery | L1 | Explore codebase/data, produce structured findings | `discovery/` |
| Build-from-Discovery | L2 | Create output based on L1 findings | varies |
| Test/Execute | L3 | Run commands, capture raw + summary | `test-results/` |
| Review/QA | L4 | Assess quality against sources | `reviews/` |
| Conditional-Action | L5 | Branch behavior based on L3/L4 results | `plans/` |
| Aggregation | L6 | Consolidate multiple outputs into report | `reports/` |

### Common Phase Structures (line 823-829)
- **Discovery -> Build -> Review:** L1 -> L2 (per item) -> L4 (per item) -> L6
- **Build -> Test -> Fix:** build items -> L3 -> L5

---

## 6. Checklist Structure Rules (Section E, lines 274-388)

- EVERY actionable item is a checkbox: `- [ ] Action text`
- NO nested checkboxes (flat structure only)
- NO parent checkboxes that summarize children
- Each checkbox is ONE atomic, verifiable action
- Use **Step X.Y:** headers for grouping
- Checkboxes MUST appear in exact execution order
- Summary/parent items come AFTER component items, never before
- Phase numbering: `X.Y` where X=phase, Y=item within phase
- Format in existing tasks: `- [ ] **X.Y** [action text as single paragraph]`

---

## 7. Phase-Gate QA Enforcement (Section I15-I16, lines 599-624)

Every task with 2+ execution phases MUST include phase-gate QA checkpoints. A checkpoint consists of:
1. Aggregation item collecting all outputs from preceding phase
2. QA agent spawn item (rf-qa or rf-qa-qualitative)
3. Conditional-action item: proceed on PASS, fix cycle on FAIL

Fix cycle limits:
| Gate Type | Max Cycles | After Max |
|-----------|-----------|-----------|
| research-gate | 3 | HALT and escalate |
| synthesis-gate | 2 | Open Questions |
| report-validation | 3 | HALT and escalate |
| task-integrity | 2 | Open Questions |

---

## 8. Post-Completion Validation (Section I17, lines 626-635)

Before status is set to Done, MUST verify:
1. All `- [ ]` items have been marked `- [x]`
2. All output files specified in checklist items exist on disk
3. Any blocker entries in Task Log have resolution notes
4. If task modified source code: all relevant tests pass

---

## 9. Item Numbering Convention from Existing Tasks

From `TASK-RF-20260325-cli-tdd.md` (the most recent precedent):

- Items use bold numbering: `- [x] **2.1** [action text]`
- Phase headers: `## Phase N: [Name] (M items)`
- Phase purpose blocks: `> **Purpose:** [explanation]`
- Horizontal rules (`---`) separate phases
- Task Log sections use `### Phase N Findings` format with `_No findings yet._` placeholder
- Execution Log is a markdown table: `| Timestamp | Phase | Item | Status | Notes |`

---

## 10. Estimation for C-122 Auto-Detection Task

Based on the BUILD_REQUEST scope (auto-detection of `--input-type` via heuristic analysis of the input file, replacing the manual flag), and the precedent task file which had 29 items across 8 phases for a comparable scope:

### Recommended Phase Structure

| Phase | Name | Pattern | Est. Items |
|-------|------|---------|------------|
| 1 | Setup and Handoff Directory Creation | Standard | 2 |
| 2 | Detection Heuristic Implementation | L1 Discovery + Build | 4-5 |
| 3 | CLI Integration (remove manual flag, wire auto-detect) | Build | 3-4 |
| 4 | Executor Routing Update | Build | 2-3 |
| 5 | Testing and Verification | L3 Test + L5 Conditional | 4-5 |
| 6 | Backward Compatibility Verification | L3 Test | 2-3 |
| 7 | Post-Completion Actions | Standard | 2 |

**Estimated totals:** ~20-24 items across 6-7 phases

### Rationale
- C-122 is narrower than the CLI-TDD task (29 items, 8 phases) because it modifies fewer files
- The core change is: create a detection function, call it from executor, remove/deprecate the manual flag
- Testing is proportional: unit tests for the heuristic, integration test for routing, backward compat check

---

## 11. Key Template-Specific Features for C-122

### Features to USE:
- **L1 Discovery pattern**: For scanning existing `--input-type` usage patterns across CLI before modifying
- **L3 Test/Execute pattern**: For running pytest and capturing results
- **B2 self-contained items**: Every item must embed context + action + output + verification + gate
- **Phase-outputs directory**: `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/`

### Features NOT needed for C-122:
- **L4 Review/QA pattern**: Not needed unless multiple output files require cross-validation
- **L6 Aggregation pattern**: Scope is narrow enough that no multi-file aggregation is needed
- **Dynamic content markers (I6)**: All items are known upfront; use `task_type: static`

---

## Sources

| Finding | Source File | Lines |
|---------|------------|-------|
| Template availability | `.claude/agent-memory/rf-task-builder/template-notes.md` | 9-13 |
| A3 granular breakdown | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 91-95 |
| B2 self-contained pattern | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 142-148 |
| B5 forbidden patterns | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 164-184 |
| Section E checklist rules | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 274-388 |
| Section L handoff patterns | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 711-830 |
| PART 2 template structure | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 882-1096 |
| I15-I16 phase-gate QA | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 599-624 |
| I17 post-completion validation | `.claude/templates/workflow/02_mdtm_template_complex_task.md` | 626-635 |
| Precedent task structure | `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md` | 1-199 |
| Previous template research | `.dev/tasks/to-do/TASK-RF-20260327-prd-pipeline/research/04-template-and-task-patterns.md` | 1-40 |
