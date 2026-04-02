# Research: MDTM Task File Patterns

**Researcher**: researcher-templates-tasks
**Status**: Complete
**Scope**: .dev/tasks/to-do/TASK-RF-20260325-cli-tdd/, .dev/tasks/done/
**Track Goal**: Document structural patterns from existing MDTM task files for building an E2E pipeline test task file.

---

## Findings

### 1. YAML Frontmatter Fields

Two task files were analyzed. Both use YAML frontmatter delimited by `---`.

**CLI TDD Task** (`TASK-RF-20260325-cli-tdd.md`) uses these fields:
```yaml
id: TASK-RF-20260325-cli-tdd
title: "CLI TDD Integration — Dual Extract Prompt with --input-type Flag"
status: done-cli-layer          # lifecycle: to-do → in-progress → done-cli-layer → done
completion_date: 2026-03-26
start_date: 2026-03-26
updated_date: 2026-03-26
priority: high
created: 2026-03-25
type: implementation
template: complex
estimated_items: 29
estimated_phases: 8
```

**Completed Task** (`TASK-RF-20260325-001.md`) uses additional fields:
```yaml
id: "TASK-RF-20260325-001"
title: "Implement Option 3: TDD Template + Pipeline Upgrades..."
type: "implementation"
status: "done"
start_date: "2026-03-26"
updated_date: "2026-03-26"
priority: "high"
created: "2026-03-25"
source_research: "TASK-RESEARCH-20260324-001"
template: "02-complex"
tags: ["pipeline", "tdd", "sc-roadmap", ...]
targets:                          # list of files to be modified
  - "src/superclaude/examples/tdd_template.md"
  - ...
handoff_dir: ".dev/tasks/to-do/TASK-RF-20260325-001/phase-outputs"
```

**Key differences**: The completed task includes `source_research`, `tags`, `targets` (list of files), and `handoff_dir`. Both omit `completion_date` when quoting strings. The E2E task should include: `id`, `title`, `status`, `type`, `priority`, `created`, `start_date`, `template`, `estimated_items`, `estimated_phases`, and optionally `tags` and `targets`.

---

### 2. Phase Organization

**CLI TDD Task** — 8 phases, 29 items:
| Phase | Name | Items | Purpose |
|-------|------|-------|---------|
| 1 | Setup and Handoff Directory Creation | 2 | Read task file, create output dirs |
| 2 | CLI and Config Layer | 5 | Wire CLI flags, config models |
| 3 | TDD Extract Prompt — Critical Path | 6 | Create new prompt function (core logic) |
| 4 | Executor Branching | 3 | Route TDD to new prompt |
| 5 | Fidelity Prompt Update | 2 | Generalize existing prompt |
| 6 | Gate Schema Review and Pipeline Guardrail | 4 | Review compatibility, add warnings |
| 7 | Tasklist Validate TDD Enrichment — Optional | 2 | Optional feature |
| 8 | Integration Testing and Final Verification | 5 | Backward compat, pytest, regression |

**Completed Task** — 7 phases (Phase 0-6), ~50+ items:
| Phase | Name | Items | Purpose |
|-------|------|-------|---------|
| 0 | Preparation and Setup | 9 | Verify all target files, create dirs |
| 1 | TDD Template Frontmatter Additions | 4 | Edit template file |
| 2 | Extraction Pipeline and Scoring Upgrades | 10 | Extend pipeline docs |
| 3 | spec-panel Additions | 4 | Add TDD input detection |
| 4 | sc-tasklist --spec Implementation | 5 | Implement feature flag |
| 5 | PRD-to-TDD Handoff Improvements | 5 | Add agent prompt, mapping |
| 6 | Integration Verification and Completion | 18 | Sync, 14 integration checks, status |

**Pattern**: Phases follow a consistent progression:
1. **Setup/Prep** phase first (read task, create directories, verify prerequisites)
2. **Core implementation** phases in dependency order (each phase has a `> Purpose:` blockquote)
3. **Verification/Integration** phase last (run tests, check backward compat, update status)

Each phase has a blockquote header with:
- `> **Purpose:**` or `> **Goal:**` describing the phase intent
- Optional `> **Target file(s):**` listing files modified
- Optional `> **Evidence:**` citing research sources
- Optional `> **Handoff input:**` citing discovery files from earlier phases

---

### 3. Checklist Item Format — B2 Self-Contained Pattern

Every checklist item follows a dense, self-contained format. Here is the anatomy:

**Structure**: `- [ ] **N.M** <Context + Action + Output + Verification + Completion gate>`

All in a SINGLE paragraph (no line breaks within the item). Components:

#### Context (what to read first)
> "Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to understand the existing Click option decorators and `run()` function signature"

Always specifies:
- Exact file path (not relative, includes full path from project root)
- What to look for in that file (specific function, section, line range)
- Sometimes references discovery files from earlier phases

#### Action (what to do)
> "then add a new `@click.option(...)` decorator to the `run` command"

Specifies:
- Exact code/text to add or modify
- Placement instructions (e.g., "place after the existing `--retrospective` option")
- Constraints on the change (e.g., "no existing options are modified")

#### Output (where to write results)
> "Write the verification results to `.dev/tasks/.../phase-outputs/test-results/phase2-verification.md`"

For verification items, specifies an output file path.

#### Verification (how to confirm)
> "ensuring both print `PASS`"
> "Verify by reading the function back that all 8 sections are present"

Inline assertion or manual check instruction.

#### Completion Gate
> "If unable to complete due to unexpected file structure, log the specific blocker in the Phase N Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete."

EVERY item ends with this two-part gate:
1. **Failure path**: "If unable to complete due to [specific reason], log the specific blocker in the Phase N Findings section of the Task Log..., then mark this item complete."
2. **Success path**: "Once done, mark this item as complete."

This ensures items are ALWAYS marked complete regardless of outcome — progress is never blocked.

---

### 4. Subprocess Execution Items

Items that run CLI commands follow this pattern:

**Example (item 2.5 from CLI TDD task)**:
> "Verify Phase 2 completion by running the following two commands: `uv run python -c "..."` and `uv run python -c "..."`, ensuring both print `PASS`. Write the verification results to `.dev/tasks/.../phase-outputs/test-results/phase2-verification.md` containing the command outputs and pass/fail status."

**Pattern for subprocess items**:
1. State what is being verified
2. Provide the EXACT command to run (backtick-wrapped, copy-paste ready)
3. State the expected output (e.g., "ensuring it prints `PASS`")
4. Specify output file for results
5. Include the standard completion gate

**Example (item 8.2 — pytest creation + execution)**:
> "Create a pytest test file at `tests/cli/test_tdd_extract_prompt.py`... Run the tests with `uv run pytest tests/cli/test_tdd_extract_prompt.py -v` and write results to `.dev/tasks/.../phase-outputs/test-results/phase8-pytest-results.md`."

**Example (item 8.3 — regression test run)**:
> "Run the existing test suite with `uv run pytest tests/ -v --tb=short 2>&1 | head -100` to verify no regressions..."

**Key observations**:
- Commands use `uv run` prefix (never bare `python` or `pytest`)
- Inline Python verification scripts use `-c "..."` with assertions
- Commands are self-contained: import, setup, assert, cleanup, print PASS/FAIL
- Pipe to `head -100` for long outputs to control output size

---

### 5. Verification Items

Verification items check the output of prior phases. Two types observed:

**Type A: Inline Python assertion scripts** (items 2.5, 3.5, 3.6, 5.2, 8.4)
- Run `uv run python -c "..."` with embedded assertions
- Assert specific strings/values in output
- Print `PASS` on success
- Clean up temp files (`p.unlink()`)

**Type B: File content verification** (items 6.2-6.15 in completed task)
- Run `grep -c` to count occurrences
- Read file and verify structural properties
- Append results to a running integration checklist file

**Type C: Pytest suite runs** (items 8.2, 8.3)
- Run `uv run pytest <path> -v`
- Write results to phase-outputs
- Distinguish between task-related failures and pre-existing failures

All verification items write results to `.dev/tasks/<task-id>/phase-outputs/test-results/` directory.

---

### 6. Task Log / Notes Section Structure

Both task files end with a `## Task Log / Notes` section containing:

#### Execution Log (table)
```markdown
### Execution Log

| Timestamp | Phase | Item | Status | Notes |
|-----------|-------|------|--------|-------|
| | | | | |
```
Starts empty; filled during execution.

#### Per-Phase Findings (one subsection per phase)
```markdown
### Phase N Findings

_Use this section to log blockers discovered during Phase N [description]._

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |
```
OR the simpler variant:
```markdown
### Phase N Findings

_No findings yet._
```

The CLI TDD task uses the simpler format; the completed task uses the table format with column headers (Item, Finding, Severity, Resolution).

#### Open Questions Carried from Research (table)
```markdown
### Open Questions Carried from Research

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| C-1 | Does `semantic_layer.py` read... | OPEN | Investigate before... |
```

#### Deferred Work Items (table)
```markdown
### Deferred Work Items

| Item | Rationale | Dependency |
|------|-----------|------------|
| DEVIATION_ANALYSIS_GATE redesign | Structurally incompatible... | None — independent... |
```

---

### 7. Parallel Spawning Instructions

No explicit parallel spawning instructions were found in the checklist items themselves. However:

- The completed task's item 0.8 notes: "Execute item 0.9 BEFORE this item if running items in parallel."
- Phase blockquotes sometimes note dependencies: "Depends on Phase 2 (config layer) being complete."
- Items within a phase are generally sequential (item N+1 depends on item N).
- Phases themselves can sometimes be parallelized when independent.

The task structure implies serial execution by default, with occasional notes about ordering constraints when items could theoretically be parallelized.

---

### 8. Directory Structure for Task Outputs

Both tasks use a standardized handoff directory:
```
.dev/tasks/<location>/TASK-<id>/
├── TASK-<id>.md                    # The task file itself
├── research-notes.md               # Optional research context
├── phase-outputs/
│   ├── discovery/                  # Files read/created during setup phases
│   │   ├── extraction-pipeline-insertion-points.md
│   │   └── ...
│   ├── test-results/               # Verification outputs per phase
│   │   ├── phase2-verification.md
│   │   ├── phase3-tdd-template-test.md
│   │   ├── phase8-pytest-results.md
│   │   └── integration-checklist.md
│   ├── reviews/                    # Review/audit documents
│   │   └── gate-compatibility-review.md
│   └── reports/                    # Summary reports
│       └── final-integration-report.md
├── qa/                             # QA validation reports (completed task)
│   └── qa-task-validation-report.md
└── reviews/                        # QA phase reports (completed task)
    ├── qa-phase-1-report.md
    └── ...
```

---

### 9. Effective Patterns for E2E Test Task File

Based on analysis of both task files, the E2E pipeline test task should follow these patterns:

1. **Phase 1 must be Setup**: Read the task file, create `phase-outputs/` directory tree with `discovery/`, `test-results/`, `reviews/`, `reports/` subdirectories, verify prerequisites.

2. **First item in Phase 1**: "Read this task file in full to understand all phases, objectives, and open questions. Update the `status` field in this file's YAML frontmatter from `to-do` to `in-progress`. Once done, mark this item as complete."

3. **Self-contained items**: Every item must include Context + Action + Output + Verification + Completion gate. No item should assume state from a prior item without explicitly re-reading the relevant file.

4. **Subprocess items**: Provide exact commands with `uv run` prefix. Use inline Python `-c "..."` scripts for quick assertions. Use `uv run pytest` for test suite runs. Always specify expected output.

5. **Verification items at phase boundaries**: Each phase should end with a verification item that confirms the phase's work. Write results to `phase-outputs/test-results/phaseN-<name>.md`.

6. **Final phase must include**: Backward compatibility check, full test suite regression run, integration summary report, status update to `done`.

7. **Failure paths in every item**: "If unable to complete due to [specific reason], log the specific blocker in the Phase N Findings section of the Task Log at the bottom of this task file, then mark this item complete."

8. **Task Log section**: Include Execution Log table, per-phase Findings subsections, Open Questions table, and Deferred Work Items table.

9. **Item numbering**: Use `Phase.Item` format (e.g., `1.1`, `2.3`, `8.5`). Bold the number: `**N.M**`.

10. **Phase header blockquotes**: Include `> **Purpose:**` describing intent. For code phases, include `> **Target file(s):**` and `> **Handoff input:**`.

---

## Status: Complete

### Summary

Analyzed two MDTM task files:
- `/Users/cmerritt/GFxAI/IronClaude/.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md` (29 items, 8 phases, status: done-cli-layer)
- `/Users/cmerritt/GFxAI/IronClaude/.dev/tasks/done/TASK-RF-20260325-001/TASK-RF-20260325-001.md` (50+ items, 7 phases, status: done)

Documented 9 structural patterns: YAML frontmatter fields, phase organization with purpose blockquotes, the B2 self-contained checklist item format (Context + Action + Output + Verification + Completion gate), subprocess execution patterns using `uv run`, verification item types (inline assertions, grep checks, pytest runs), Task Log section structure with per-phase findings tables, parallel spawning notes, handoff directory tree conventions, and 10 effective patterns the E2E test task file should follow.

