# Research: MDTM Template 02 Rules
**Topic type:** Template & Examples
**Scope:** .claude/templates/workflow/02_mdtm_template_complex_task.md
**Status:** Complete
**Date:** 2026-04-02
---

## 1. Template Overview

Template 02 is the **Complex Task Template**, extending Template 01 with Section L (Intra-Task Handoff Patterns). Use it when tasks require discovery, testing, review, conditional logic, or aggregation between checklist items. The template has two parts:
- **PART 1** (lines 46-870): Builder instructions (never appear in output)
- **PART 2** (lines 894+): The actual task file template to copy and fill

---

## 2. Critical Rules for Task Building (Sections A-C)

### A3 — Complete Granular Breakdown
- Break down EVERY phase into **atomic, verifiable checklist items**
- Create individual items for EVERY file, component, or iteration
- **NO high-level or bulk operations** — everything must be granular
- Include exact file paths, specific requirements, measurable outcomes

### A4 — Iterative Process Structure
For ANY process involving multiple items:
1. Pre-enumerate ALL items in an initial step
2. Create individual checklist item for each specific item
3. Require incremental updates after each item
4. Include consolidation step only after ALL items complete

Pattern:
```markdown
**Step X.1:** Scan and enumerate all [items] in [location]
- [ ] Complete [item] listing generated: [count] items identified

**Step X.2:** Process each [item] individually:
- [ ] [Item 1]: [exact identifier] - [specific action] completed
- [ ] [Item 2]: [exact identifier] - [specific action] completed

**Step X.3:** Consolidate all individual results
- [ ] All [count] items processed and results logged
```

### C1-C4 — Embedding Requirements (NOT Separate Sections)
These are collected during planning but MUST BE EMBEDDED in checklist items:
- **C1 Outputs**: Exact file path, name, content requirements, template — embedded in the item that creates it
- **C2 Success Criteria**: Embedded as "ensuring..." clause
- **C3 Verification**: Embedded in action items, NOT separate verification items
- **C4 Completion**: Only Post-Completion Actions section handles final items

---

## 3. B2 — The Self-Contained Checklist Item Pattern (CRITICAL)

Every checklist item MUST be a complete, self-contained prompt containing these 6 elements:

| # | Element | Description |
|---|---------|-------------|
| 1 | **Context Reference + WHY** | What file(s) to read and why that context is needed for this specific action |
| 2 | **Action + WHY** | What to do with that context and why it needs to be done |
| 3 | **Output Specification** | Exact output file name, location, content to produce, template to follow |
| 4 | **Integrated Verification** | "ensuring..." clause — DO NOT assume/hallucinate, 100% accuracy from sources |
| 5 | **Evidence on Failure Only** | Log to task notes ONLY if blocked (output file itself = success evidence) |
| 6 | **Explicit Completion Gate** | "Once done, mark this item as complete." |

### B3 — Format
Each item is ONE FULL PARAGRAPH (not multiple lines or bullets). Verbose and explanatory — reads like a complete prompt executable independently without prior context.

### B5 — Forbidden Patterns
- Standalone "read context" items with no output
- Missing context reference (no source of truth)
- Multi-line/bulleted checklist items
- Separate verification/confirmation items
- Overly granular items (e.g., "create directory" alone)
- Separate REMINDER blocks between items

---

## 4. Checklist Structure Rules (Section E)

### E1 — Checkbox Format
- EVERY actionable item: `- [ ] Action text`
- NO nested checkboxes (flat structure only)
- NO parent checkboxes summarizing children
- Use **Step X.Y:** headers for grouping, NOT checkboxes
- Exact sequential order — top to bottom only

### E2 — Components First, Summary Last
- Summary/parent checkboxes MUST come AFTER all component items
- NEVER put a parent checkbox before its children

### E4 — Formatting
- NEVER place checkboxes next to step numbers
- Step numbers = bold headings without checkboxes
- DO NOT include separate REMINDER blocks (embed in item)

---

## 5. Section L — Intra-Task Handoff Patterns (L1-L6)

### Handoff File Convention
Items write outputs to: **`.dev/tasks/TASK-NAME/phase-outputs/`**

Subdirectories:
| Directory | Purpose |
|-----------|---------|
| `discovery/` | Discovery scan results, inventories |
| `test-results/` | Test output, summaries |
| `reviews/` | Quality review verdicts |
| `plans/` | Fix plans, conditional action outputs |
| `reports/` | Aggregated reports, summaries |

Files persist across all batches and session rollovers.

### L1 — Discovery Item Pattern
**When:** Explore codebase/environment/data and produce structured findings for later items.
**Key rule:** The discovery file IS the deliverable. Must be well-structured, machine-readable.

### L2 — Build-From-Discovery Pattern
**When:** Create output based on a previous discovery item's findings.
**Key rule:** Always reference BOTH the discovery file path AND the source file path.

### L3 — Test/Execute Pattern
**When:** Run a command, script, or test suite and capture results.
**Key rule:** Capture BOTH raw output AND a structured summary. Raw preserves detail; summary enables quick assessment.

### L4 — Review/QA Pattern
**When:** Assess quality of a previous item's output against source materials.
**Key rule:** Produce a structured verdict (PASS/FAIL) with specific findings. Never "looks good."

### L5 — Conditional-Action Pattern
**When:** Item behavior depends on result of a previous item (test/review).
**Key rule:** MUST handle BOTH branches (success AND failure). Output file always created.

### L6 — Aggregation Pattern
**When:** Consolidate multiple previous outputs into a single report.
**Key rule:** Use Glob to find files dynamically. Don't hardcode file lists.

### L7 — Common Phase Structures
| Structure | Pattern Sequence |
|-----------|-----------------|
| Discovery -> Build -> Review | L1 -> L2 -> L4 -> L6 |
| Build -> Test -> Fix | K1/K2 -> L3 -> L5 |
| Full Lifecycle | L1 -> L2 -> L3 -> L5 -> L4 -> L6 |
| With QA Gates | L1 -> L2 -> M1(QA) -> L3 -> L5 -> L4 -> L6 -> M1(QA) |

---

## 6. Phase-Gate QA (Sections I15-I17, M1)

### I15 — Phase-Gate Enforcement
Every task with 2+ execution phases MUST include at least one phase-gate QA checkpoint. A phase-gate consists of:
1. Aggregation item (collect outputs from preceding phase)
2. QA agent spawn item (rf-qa or rf-qa-qualitative)
3. Conditional-action item (proceed on PASS, fix cycle on FAIL)

### I16 — Fix Cycle Limits
| Gate Type | Max Cycles | After Max |
|-----------|-----------|-----------|
| research-gate | 3 | HALT and escalate |
| synthesis-gate | 2 | Open Questions |
| report-validation | 3 | HALT and escalate |
| task-integrity | 2 | Open Questions |
| qualitative gate | 3 | HALT and escalate |

### I17 — Post-Completion Validation
Before setting status to Done, verify:
1. All `- [ ]` items marked `- [x]`
2. All output files exist on disk (Glob)
3. Any blocker entries have resolution notes
4. If code modified: all relevant tests pass

### I18 — Testing for Code-Modifying Tasks
Must include test items specifying: command to run, pass criteria, where results captured, follows B2 pattern.

---

## 7. Task File Structure (PART 2 Template)

Required sections in order:

```
---
[Frontmatter: id, title, status, priority, created, type, template, etc.]
---

# [Task Title]

## Task Overview
[Description of what task accomplishes]

## Key Objectives
1. **[Objective 1]:** ...
2. **[Objective 2]:** ...

## Prerequisites & Dependencies
### Parent Task & Dependencies
### Previous Stage Outputs (MANDATORY INPUTS)  ← INFORMATIONAL ONLY, no checkboxes
### Handoff File Convention
### Frontmatter Update Protocol

## Detailed Task Instructions

### Phase 1: Preparation and Setup
- [ ] 1.1 Update task status...
- [ ] 1.2 Create handoff directories...

### Phase 2: [Main Work Phase] (N items)
> **Purpose:** [What this phase accomplishes]
- [ ] 2.1 ... (B2 self-contained pattern)
- [ ] 2.2 ...

### Phase N: Post-Completion Actions
- [ ] N.1 Verify all outputs exist (I17)
- [ ] N.2 Confirm tests passed (if code modified)
- [ ] N.3 Create Task Summary
- [ ] N.4 Update frontmatter to "done"

## Task Log / Notes

### Task Summary
[Filled at completion]

### Execution Log
| Timestamp | Phase | Item | Status | Notes |

### Phase 2 Findings
_No findings yet._

### Follow-Up Items
_No follow-up items yet._
```

---

## 8. Existing Task Examples Analyzed

### TASK-RF-20260402-auto-detection (Best Reference)
**Path:** `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/TASK-RF-20260402-auto-detection.md`
**Structure:** 7 phases, 25 items, status=done, template=complex, task_type=static

Key patterns observed:
- **Frontmatter** uses simplified fields (`status: done`, `priority: high`) without emoji prefixes — diverges from template but works
- **Research inputs** listed as "Previous Stage Outputs (MANDATORY INPUTS)" with exact paths
- **Phase-outputs/** directory with `discovery/`, `test-results/`, `plans/` subdirectories
- **Every checklist item** follows B2 pattern: one paragraph, context reference + action + output + ensuring clause + failure logging + completion gate
- **Phase 6** uses L3 (Test/Execute) + L5 (Conditional-Action) patterns
- **Phase 7** is Post-Completion: verify outputs, confirm tests, task summary, frontmatter update
- **Task Log** has sections per phase for findings, plus Execution Log table and Follow-Up Items

### Folder Structure Observed
```
TASK-RF-20260402-auto-detection/
├── TASK-RF-20260402-auto-detection.md    ← Main task file
├── research/                             ← Research inputs (from prior research task)
│   ├── 01-detection-signals.md
│   ├── 02-cli-click-nargs.md
│   ├── 03-routing-logic.md
│   └── 04-existing-tests.md
├── phase-outputs/                        ← Handoff outputs (created during execution)
│   ├── discovery/
│   ├── test-results/
│   └── plans/
├── qa/                                   ← QA reports
├── reviews/                              ← Review outputs
└── research-notes.md
```

### Other Task Folder Examples
| Task | Type | Contents |
|------|------|----------|
| TASK-E2E-20260326-tdd-pipeline | E2E test | BUILD-REQUEST files, E2E-TEST-PLAN.md |
| TASK-E2E-20260327-prd-pipeline-e2e | E2E test | Similar BUILD-REQUEST structure |
| TASK-RF-20260325-cli-tdd | Implementation | Standard RF task folder |

---

## 9. Pitfalls and Anti-Patterns to Avoid

1. **Standalone read items** — "Read file X and log findings" is useless; context is lost by next batch
2. **Separate verification items** — Verification goes in the "ensuring..." clause of the action item
3. **Multi-line checklist items** — Must be one paragraph, not bullets
4. **Parent checkboxes before children** — Summary checkboxes go LAST
5. **Checklist items before Phase 1** — No checkboxes allowed in Prerequisites/Overview sections
6. **Backward references** — Never "go back and update" or "see below"
7. **Missing failure handling** — Every item needs the "If unable to complete..." clause
8. **Hardcoded file lists in aggregation** — Use Glob to discover files dynamically
9. **Optional items** — Everything in the task is required; no "nice-to-haves"
10. **Skipping phase-gate QA** — Required between phases for tasks with 2+ execution phases

---

## 10. Relevance to E2E Test 3 Task (Worktree Pipeline Comparison)

For the baseline-repo E2E test task, the following patterns are most relevant:

| Phase Need | Recommended Pattern |
|-----------|-------------------|
| Setup worktree + clone repos | Phase 1 setup items (standard) |
| Run pipeline in each repo | L3 (Test/Execute) — capture raw output + summary |
| Compare outputs across repos | L1 (Discovery) to inventory outputs, then L4 (Review/QA) to compare |
| Conditional pass/fail | L5 (Conditional-Action) based on comparison results |
| Aggregate comparison report | L6 (Aggregation) to consolidate all comparisons |

The task should be `task_type: static` since all items are known upfront (we know the two repos and the pipeline to run).

Phase structure recommendation:
1. Preparation (status update, directory creation)
2. Worktree/Repo Setup (clone/checkout operations)
3. Pipeline Execution (L3 in both repos)
4. Output Comparison (L1 discover outputs + L4 review/compare)
5. Test Verdict (L5 conditional + L6 aggregate)
6. Post-Completion (I17 validation, summary, frontmatter)
