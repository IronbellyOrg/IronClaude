# Research Notes: PRD Pipeline Integration Implementation

**Date:** 2026-03-27
**Scenario:** A (explicit — comprehensive research report already exists)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

### Source of Truth: Prior Research

This implementation task is built from a completed tech-research investigation. All findings are verified, QA-gated, and documented:

| Artifact | Path | Purpose |
|----------|------|---------|
| Research report | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/RESEARCH-REPORT-prd-pipeline-integration.md` | Full 10-section report with 8-phase implementation plan |
| Synth implementation plan | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/synthesis/synth-05-implementation-plan.md` | Granular per-step tables with file paths and line numbers |
| Research: roadmap CLI | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/01-roadmap-cli-integration-points.md` | Exact integration points, dead tdd_file discovery |
| Research: prompt mapping | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/02-prompt-enrichment-mapping.md` | Drafted supplementary blocks for all 10 builders |
| Research: tasklist CLI | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/03-tasklist-integration-points.md` | 4-layer wiring pattern traced end-to-end |
| Research: skill layer | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/04-skill-reference-layer.md` | PRD-conditional additions for 4 skill/ref docs |
| Research: PRD content | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/05-prd-content-analysis.md` | 28-section PRD inventory, pipeline touchpoint mapping |
| Research: web | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/research/web-01-prd-driven-roadmapping.md` | External patterns, WSJF scoring, dual-track agile |
| Gaps log | `.dev/tasks/to-do/TASK-RESEARCH-20260327-prd-pipeline/gaps-and-questions.md` | 8 open questions, 4 resolved |

### Target Files (will be modified)

**Roadmap CLI:**

| Path | Purpose | Key Exports | Changes Needed |
|------|---------|-------------|----------------|
| `src/superclaude/cli/roadmap/models.py` | RoadmapConfig dataclass | `RoadmapConfig` | Add `prd_file: Path \| None = None` |
| `src/superclaude/cli/roadmap/commands.py` | Click CLI commands | `roadmap_group`, `run` | Add `--tdd-file`, `--prd-file` flags, wire to config |
| `src/superclaude/cli/roadmap/executor.py` | Pipeline orchestration | `execute_roadmap`, `detect_input_type` | Wire tdd_file+prd_file to steps, redundancy guard, state file |
| `src/superclaude/cli/roadmap/prompts.py` | 10 prompt builders | `build_extract_prompt`, etc. | Refactor 7 builders to base-pattern, add prd_file+tdd_file params, supplementary blocks |
| `src/superclaude/cli/roadmap/gates.py` | Gate definitions | Gate constants | Document PRD compatibility (no structural changes) |

**Tasklist CLI:**

| Path | Purpose | Key Exports | Changes Needed |
|------|---------|-------------|----------------|
| `src/superclaude/cli/tasklist/models.py` | TasklistValidateConfig | `TasklistValidateConfig` | Add `prd_file: Path \| None = None` |
| `src/superclaude/cli/tasklist/commands.py` | Click CLI commands | `tasklist_group`, `validate` | Add `--prd-file` flag |
| `src/superclaude/cli/tasklist/executor.py` | Validation execution | `execute_tasklist_validate` | Wire prd_file, auto-wire from state |
| `src/superclaude/cli/tasklist/prompts.py` | Fidelity + generation prompts | `build_tasklist_fidelity_prompt` | Add prd_file param, PRD validation block, generation enrichment blocks |

**Skill/Reference Layer:**

| Path | Purpose | Changes Needed |
|------|---------|----------------|
| `src/superclaude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | Extraction step reference | PRD-supplementary extraction context section |
| `src/superclaude/skills/sc-roadmap-protocol/refs/scoring.md` | Scoring reference | PRD scoring guidance, `product` type |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Tasklist protocol | Sections 4.1b (PRD context), 4.4b (PRD generation), source doc enrichment |
| `src/superclaude/commands/spec-panel.md` | Spec-panel command | Steps 6c-6d (PRD detection + frontmatter) |

**Tests:**

| Path | Purpose | Changes Needed |
|------|---------|----------------|
| `tests/roadmap/` | Roadmap test suite | CLI flag parsing, prompt builder output, refactoring regression |
| `tests/tasklist/` | Tasklist test suite | CLI flag parsing, fidelity output, generation enrichment |

## PATTERNS_AND_CONVENTIONS

### TDD Supplementary Input Pattern (established — replicate for PRD)

Traced end-to-end in research file 03:
1. Model field: `tdd_file: Path | None = None` on config dataclass
2. CLI flag: `--tdd-file` with `type=click.Path(exists=True, path_type=Path)`
3. Executor wiring: `if config.tdd_file is not None: all_inputs.append(config.tdd_file)` + `tdd_file=config.tdd_file` kwarg to prompt builder
4. Prompt builder: `def build_tasklist_fidelity_prompt(..., tdd_file: Path | None = None)` with conditional block `if tdd_file is not None: base += "..."`

### Prompt Builder Refactoring Pattern

7 of 10 roadmap builders need conversion from single-return-expression to base-variable pattern before conditional blocks can be appended. Mechanical refactoring: `return "..."` → `base = "..."; return base`.

### State File Pattern

`.roadmap-state.json` already records `spec_file`. Adding `tdd_file` and `prd_file` follows the same pattern.

## GAPS_AND_QUESTIONS

From gaps-and-questions.md (8 items, 1 resolved during this session):
- Q1: RESOLVED — wire dead tdd_file alongside prd_file
- Q2: 7 builders need refactoring (included in implementation plan Phase 2)
- Q3-Q8: Minor/deferred — documented in research report Section 9

## RECOMMENDED_OUTPUTS

### Research files (4 focused researchers)

Since comprehensive research already exists, researchers do **verification and gap-fill** against the implementation plan, not full re-investigation.

| File | Topic | Type | Focus |
|------|-------|------|-------|
| `research/01-implementation-verification.md` | Verify implementation plan steps against current code | Code Tracer | Read each target file, confirm line numbers, function signatures, and insertion points are still accurate |
| `research/02-prompt-block-drafts.md` | Compile all drafted supplementary PRD blocks | Code Tracer + Doc Analyst | Extract drafted blocks from research 02, verify they reference correct PRD sections |
| `research/03-state-file-and-auto-wire.md` | Verify .roadmap-state.json schema and auto-wire feasibility | Code Tracer | Read executor state handling, confirm schema, plan auto-wire integration points |
| `research/04-template-and-task-patterns.md` | Read MDTM templates and existing task files for patterns | Template & Examples | Read template 02, check existing TASK-RF examples for phase structure |

## SUGGESTED_PHASES

### Research Phase (4 parallel agents)

**Researcher 1 — Implementation Plan Verification**
- Type: Code Tracer
- Scope: All 9 target Python files + 4 skill/reference docs
- Focus: Verify line numbers, function signatures, insertion points from synth-05 are still accurate. Flag any drift since the research was conducted.
- Output: `research/01-implementation-verification.md`

**Researcher 2 — Prompt Block Compilation**
- Type: Code Tracer + Doc Analyst
- Scope: `research/02-prompt-enrichment-mapping.md` from prior research + `src/superclaude/cli/roadmap/prompts.py` + `src/superclaude/cli/tasklist/prompts.py`
- Focus: Extract all drafted supplementary PRD blocks. Verify PRD section references (§N) match actual PRD skill structure. Compile complete list of blocks per builder.
- Output: `research/02-prompt-block-drafts.md`

**Researcher 3 — State File and Auto-Wire**
- Type: Code Tracer
- Scope: `src/superclaude/cli/roadmap/executor.py` (state handling), `src/superclaude/cli/tasklist/executor.py` (config resolution)
- Focus: Find where `.roadmap-state.json` is written/read. Document current schema. Plan where tdd_file/prd_file fields go. Plan auto-wire logic in tasklist executor.
- Output: `research/03-state-file-and-auto-wire.md`

**Researcher 4 — Template & Task Patterns**
- Type: Template & Examples
- Scope: MDTM template 02, existing TASK-RF folders in `.dev/tasks/to-do/`
- Focus: Read template 02 PART 1 rules. Find existing task file examples for implementation patterns. Document required sections, item format, phase structure.
- Output: `research/04-template-and-task-patterns.md`

## TEMPLATE_NOTES

Template 02 (Complex Task) — this implementation has 8 phases with discovery (state file schema), build (code changes), refactoring (prompt builders), testing, and skill doc updates. Not a simple sequential creation.

## AMBIGUITIES_FOR_USER

None — the research report provides a complete implementation plan with all decisions made. The 8 open questions from gaps-and-questions.md are all minor/deferred and documented in the report's Section 9.
