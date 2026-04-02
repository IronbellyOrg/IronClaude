# Research: Template & Task Patterns
**Status:** Complete
**Researcher:** template-patterns-agent
**Date:** 2026-03-27
**Track Goal:** PRD pipeline integration task file (~14 files, 8 phases)

---

## 1. MDTM Template Availability

The `.gfdoc/templates/` directory containing `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` does **NOT exist** in IronClaude. These templates belong to a different project (GFxAI). This is documented in agent memory at `.claude/agent-memory/rf-task-builder/template-notes.md`.

**Fallback strategy:** When a BUILD_REQUEST specifies TEMPLATE: 02 and the template file is not found, proceed directly to build the task file from the BUILD_REQUEST specifications and existing task file precedents. The MDTM rules are encoded in the task-builder skill (`SKILL.md`) and the `rf-task-builder` agent definition, not only in the template files.

**Key MDTM rules referenced from SKILL.md (lines 759-765):**

- **A3 (Complete Granular Breakdown):** Create individual checklist items for EVERY file, component, or iteration involved. Do NOT create batch items like "document all 14 handlers in a single item." Each file gets its own item. Research files contain per-file detail specifically to enable this granularity.

- **A4 (Iterative Process Structure):** Phase structure must follow logical dependency order with verification at phase boundaries.

- **B2 (Self-Contained Item Pattern):** Every checklist item must be a single paragraph containing: Context + Action + Output + Verification + Completion Gate. No item should assume state from a prior item without explicitly re-reading the relevant file.

---

## 2. YAML Frontmatter — Required Fields

Analyzed two completed task files plus one E2E task file. The union of fields used:

### Minimum Required Fields
```yaml
---
id: TASK-RF-YYYYMMDD-<slug>
title: "Descriptive Title — Subtitle with Scope"
status: to-do                    # lifecycle: to-do → in-progress → done (or done-<qualifier>)
priority: high
created: YYYY-MM-DD
type: implementation             # or: verification, research
template: complex                # or: 02-complex, generic, 01-generic
estimated_items: <integer>
estimated_phases: <integer>
---
```

### Recommended Additional Fields
```yaml
start_date: YYYY-MM-DD           # set when execution begins
updated_date: YYYY-MM-DD         # updated each session
completion_date: YYYY-MM-DD      # set when done
source_research: "TASK-RESEARCH-YYYYMMDD-NNN"  # link to research task
tags: ["pipeline", "prd", "cli"]
targets:                          # list of files to be modified
  - "src/superclaude/cli/roadmap/commands.py"
  - "src/superclaude/cli/roadmap/models.py"
handoff_dir: ".dev/tasks/to-do/TASK-RF-YYYYMMDD-<slug>/phase-outputs"
last_session_note: "Resume at Phase N item N.M"  # for multi-session tasks
```

**Source:** CLI TDD task (`TASK-RF-20260325-cli-tdd.md`), E2E task (`TASK-E2E-20260326-modified-repo.md`), completed task (`TASK-RF-20260325-001.md`).

---

## 3. Phase Organization Pattern

### Phase Progression (consistent across all 3 analyzed tasks)

1. **Phase 1: Setup/Preparation** — Read task file, update status, create output directories, verify prerequisites
2. **Phases 2-N: Core Implementation** — In dependency order, each phase targets a specific subsystem or concern
3. **Final Phase: Integration Testing & Verification** — Backward compatibility, full test suite regression, integration report, status update

### Phase Header Format
Each phase uses this structure:
```markdown
## Phase N: Phase Name (M items)

> **Purpose:** Single sentence describing the phase intent.
> Optional: **Target file(s):** list of files modified in this phase.
> Optional: **Handoff input:** reference to discovery files from earlier phases.

- [ ] **N.1** <item text>
- [ ] **N.2** <item text>

---
```

### Phase Sizing (from precedent tasks)
| Task | Phases | Total Items | Avg Items/Phase |
|------|--------|-------------|-----------------|
| CLI TDD (29 items) | 8 | 29 | 3.6 |
| E2E Modified (42 items) | 7 | 42 | 6.0 |
| Completed 001 (50+ items) | 7 | 50+ | 7+ |

**For our PRD pipeline task (~14 files, 8 phases):** Target 4-6 items per phase, ~35-45 total items.

---

## 4. Checklist Item Format — The B2 Self-Contained Pattern

Every item is a SINGLE paragraph (no line breaks within). Five mandatory components:

### Component Anatomy

**Structure:** `- [ ] **N.M** <Context> <Action> <Output> <Verification> <Completion Gate>`

#### (a) Context — what to read first
> "Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to understand the existing Click option decorators and `run()` function signature"

Rules:
- Exact file path from project root (never relative)
- What to look for in that file (specific function, section, line range)
- References discovery files from earlier phases when needed

#### (b) Action — what to do
> "then add a new `@click.option(...)` decorator to the `run` command"

Rules:
- Exact code/text to add or modify (inline code blocks when possible)
- Placement instructions ("place after the existing `--retrospective` option")
- Constraints on the change ("no existing options are modified")
- For A3 compliance: ONE file per item, ONE concern per item

#### (c) Output — where to write results
> "Write the verification results to `.dev/tasks/.../phase-outputs/test-results/phase2-verification.md`"

Rules:
- Specify full output file path for verification items
- Code modification items don't need an explicit output path (the modified file IS the output)

#### (d) Verification — how to confirm
> "ensuring both print `PASS`"
> "Verify by reading the function back that all 8 sections are present"

Rules:
- Inline assertion or manual check instruction
- For code changes: read-back verification
- For subprocess items: expected output string

#### (e) Completion Gate — ALWAYS present
> "If unable to complete due to unexpected file structure, log the specific blocker in the Phase N Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete."

Rules:
- **Failure path first**: "If unable to complete due to [specific reason], log the specific blocker in the Phase N Findings section..."
- **Success path second**: "Once done, mark this item as complete."
- Items are ALWAYS marked complete regardless of outcome — progress is never blocked

---

## 5. Verification Item Patterns

Three types observed across the analyzed tasks:

### Type A: Inline Python Assertion Scripts
```
uv run python -c "from superclaude.cli.roadmap.models import RoadmapConfig; from pathlib import Path; c = RoadmapConfig(spec_file=Path('.')); assert c.input_type == 'spec'; print('PASS')"
```
- Always uses `uv run python -c "..."` (never bare `python`)
- Self-contained: import → setup → assert → cleanup → print PASS
- Temp files cleaned up (`p.unlink()`)

### Type B: File Content Verification
```
grep -c '{{SC_PLACEHOLDER:' .dev/test-fixtures/test-spec-user-auth.md  # must return 0
```
- Uses `grep -c` for counting occurrences
- Structural property checks

### Type C: Pytest Suite Runs
```
uv run pytest tests/cli/test_tdd_extract_prompt.py -v
uv run pytest tests/ -v --tb=short 2>&1 | head -100
```
- Write results to `phase-outputs/test-results/`
- Distinguish task-related failures from pre-existing failures

All verification outputs go to: `.dev/tasks/<task-id>/phase-outputs/test-results/phaseN-<name>.md`

---

## 6. Task Log / Notes Section Structure

Every task file ends with a `## Task Log / Notes` section containing four subsections:

### 6.1 Execution Log (table — starts empty)
```markdown
### Execution Log

| Timestamp | Phase | Item | Status | Notes |
|-----------|-------|------|--------|-------|
| | | | | |
```

### 6.2 Per-Phase Findings (one subsection per phase)
Simple format:
```markdown
### Phase N Findings

_No findings yet._
```

Or table format (for more complex tasks):
```markdown
### Phase N Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |
```

### 6.3 Open Questions Carried from Research
```markdown
### Open Questions Carried from Research

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| C-1 | Does `semantic_layer.py` read... | OPEN | Investigate before... |
```

### 6.4 Deferred Work Items
```markdown
### Deferred Work Items

| Item | Rationale | Dependency |
|------|-----------|------------|
| Feature X redesign | Out of scope... | None |
```

---

## 7. Handoff Directory Convention

Standard directory tree created in Phase 1:
```
.dev/tasks/to-do/TASK-RF-YYYYMMDD-<slug>/
├── TASK-RF-YYYYMMDD-<slug>.md          # Task file itself
├── research-notes.md                    # Scope discovery notes
├── research/                            # Codebase research files
│   ├── 01-<topic>.md
│   ├── 02-<topic>.md
│   └── ...
├── qa/                                  # QA validation reports
│   ├── analyst-completeness-report.md
│   └── qa-research-gate-report.md
├── phase-outputs/                       # Execution artifacts
│   ├── discovery/                       # Setup phase discoveries
│   ├── test-results/                    # Verification outputs per phase
│   │   ├── phase2-verification.md
│   │   └── phase8-pytest-results.md
│   ├── reviews/                         # Review/audit documents
│   └── reports/                         # Summary reports
│       └── final-integration-report.md
└── reviews/                             # Optional: QA phase reports
```

---

## 8. Common Pitfalls to Avoid

Based on analysis of the task-builder SKILL.md and the pattern divergences observed:

1. **Batch items violating A3**: "Modify all 5 prompt builder files" — MUST be split into one item per file.

2. **Missing completion gate**: Every item MUST end with the two-part gate (failure path + success path). Omitting it blocks execution flow.

3. **Assumed context**: Items must NOT assume state from prior items without explicitly stating "Read the file at..." or "Read the discovery file at...". Each item re-reads what it needs.

4. **Line breaks within items**: Items must be single paragraphs. Multi-line items break markdown checklist rendering.

5. **Missing phase purpose blockquote**: Every phase needs `> **Purpose:**` describing intent.

6. **No verification at phase boundaries**: Each phase should end with a verification item confirming the phase's work.

7. **Vague placement instructions**: "Add the field to the model" is insufficient. Must specify: "add after the existing `allow_regeneration` field" with exact placement context.

8. **Missing `uv run` prefix**: All Python/pytest commands MUST use `uv run`. Never bare `python` or `pytest`.

9. **One-shot task file writing**: Large task files MUST be written incrementally (Write for header, then Edit for each phase). One-shotting hits token output limits.

10. **Status field not updated**: Phase 1 item 1 must always include "Update the `status` field in this file's YAML frontmatter from `to-do` to `in-progress`."

---

## 9. PRD Pipeline Task — Recommended Structure

Based on the CLI TDD task precedent (closest match: CLI integration work, 8 phases, 29 items):

### Recommended Phase Layout
| Phase | Name | Est. Items | Purpose |
|-------|------|------------|---------|
| 1 | Setup & Prerequisites | 2-3 | Read task, create dirs, verify research |
| 2 | PRD Skill & Template Foundation | 4-5 | PRD SKILL.md, template, refs |
| 3 | Pipeline CLI Integration | 4-5 | CLI commands, models, config |
| 4 | PRD Extraction Prompt | 5-6 | Prompt builder for PRD-specific extraction |
| 5 | Executor & Routing | 3-4 | Route PRD inputs through pipeline |
| 6 | Gate & Fidelity Updates | 3-4 | Gate compatibility, fidelity prompt |
| 7 | TDD Handoff Integration | 3-4 | PRD-to-TDD handoff pathway |
| 8 | Integration Testing & Verification | 5-6 | Backward compat, pytest, regression, report |

**Total estimate: ~32-40 items across 8 phases.**

### Key Conventions to Follow
- Item numbering: `**N.M**` format (Phase.Item)
- Phase headers: `## Phase N: Name (M items)` with `> **Purpose:**` blockquote
- Horizontal rules `---` between phases
- All file paths from project root (e.g., `src/superclaude/cli/roadmap/commands.py`)
- Commands use `uv run` prefix
- Final phase includes backward compatibility check + full test regression + integration report + status update

---

## Source Files Analyzed

| File | Path | Relevance |
|------|------|-----------|
| CLI TDD Task | `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md` | Primary precedent — 29 items, 8 phases, CLI integration work |
| E2E Modified Task | `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/TASK-E2E-20260326-modified-repo.md` | Secondary precedent — 42 items, 7 phases, E2E verification |
| Prior Pattern Research | `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/research/04-task-patterns.md` | Existing analysis of MDTM patterns (reused findings) |
| Task Builder SKILL.md | `.claude/skills/task-builder/SKILL.md` | MDTM rules A3, A4, B2 definitions |
| Agent Definition | `.claude/agents/rf-task-builder.md` | Template usage rules, workflow steps |
| Template Notes Memory | `.claude/agent-memory/rf-task-builder/template-notes.md` | Template availability in IronClaude |

