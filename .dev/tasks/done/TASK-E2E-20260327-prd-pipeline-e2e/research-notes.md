# Research Notes: E2E Test Task for PRD Pipeline Integration

**Date:** 2026-03-27
**Scenario:** A (Explicit — BUILD_REQUEST provides exact phase structure, source files, and test scenarios)
**Depth Tier:** Deep
**Track Count:** 1

---

## EXISTING_FILES

### Source 1: Existing E2E test task (clone template)
- `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/TASK-E2E-20260326-modified-repo.md` — 42 items, 7 phases, status: done. Tests TDD + spec paths. MUST be cloned with all boxes unchecked.

### Source 2: PRD implementation task (derive new test items)
- `.dev/tasks/to-do/TASK-RF-20260327-prd-pipeline/TASK-RF-20260327-prd-pipeline.md` — 61 items, 10 phases. Adds `--prd-file`, fixes dead `tdd_file`, auto-wire, tasklist generation enrichment.

### Existing test fixtures (reuse)
- `.dev/test-fixtures/test-tdd-user-auth.md` — TDD fixture, 1000+ lines
- `.dev/test-fixtures/test-spec-user-auth.md` — Spec fixture

### Prior test results (read-only comparison data)
- `.dev/test-fixtures/results/test1-tdd-modified/` — TDD-only pipeline output
- `.dev/test-fixtures/results/test2-spec-modified/` — Spec-only pipeline output
- `.dev/test-fixtures/results/verification-report-modified-repo.md` — Prior verification report
- `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/reviews/qa-qualitative-tdd-vs-spec.md` — Prior qualitative QA

### Pipeline code (verify during execution)
- `src/superclaude/cli/roadmap/commands.py` — Should have `--prd-file` and `--tdd-file` after implementation
- `src/superclaude/cli/roadmap/executor.py` — Auto-wire, state file, redundancy guard
- `src/superclaude/cli/roadmap/prompts.py` — PRD supplementary blocks
- `src/superclaude/cli/tasklist/commands.py` — Should have `--prd-file`
- `src/superclaude/cli/tasklist/executor.py` — Auto-wire from state

## PATTERNS_AND_CONVENTIONS

The existing E2E task file follows these patterns:
- YAML frontmatter with id, title, status, priority, type, template, estimated_items, estimated_phases, tags, handoff_dir
- Phase structure with `> Purpose:` blockquote, `> Handoff input:` where applicable
- Items use `- [ ] **N.N**` format with B2 self-contained paragraphs
- Verification items run grep/count commands and write results to `phase-outputs/test-results/`
- Summary items compile results to `phase-outputs/reports/`
- Task Log at bottom with Phase Findings tables, Open Questions, Deferred Work Items
- ALL pipeline commands use `uv run superclaude` (not bare `superclaude`)
- Pipeline runs use `set -o pipefail && uv run superclaude roadmap run ... 2>&1 | tee ...; echo "EXIT_CODE=$?"`

## GAPS_AND_QUESTIONS

- Need to determine exact PRD fixture structure (what sections, what frontmatter) — PRD skill at `src/superclaude/skills/prd/SKILL.md` defines the template
- Need to determine exact tasklist generate command syntax (does `superclaude tasklist generate` exist as CLI command or is it inference-only?)
- Need to understand what auto-wire info messages look like (implementation task Phase 8 item 8.3 defines them)
- Need to understand what PRD supplementary blocks look like in prompt output (implementation task Phase 4 items 4.1-4.7 define them)

## RECOMMENDED_OUTPUTS

| # | Topic | File | Researcher Focus |
|---|-------|------|-----------------|
| 01 | Existing E2E task structure | `research/01-existing-e2e-task-structure.md` | Read the existing E2E task in full. Extract: phase structure, item numbering, verification patterns, command templates, output paths. This is what gets cloned. |
| 02 | PRD implementation task mapping | `research/02-prd-implementation-mapping.md` | Read the PRD implementation task in full. Map each phase to test scenarios. Extract: what changes each phase makes, what new CLI flags/behaviors to test, what new state file fields, what auto-wire behavior. |
| 03 | PRD fixture requirements | `research/03-prd-fixture-requirements.md` | Read the PRD skill template. Determine section structure, frontmatter fields, content patterns. Define what the PRD fixture needs to cover for the "User Authentication Service" feature. |
| 04 | Tasklist generation assessment | `research/04-tasklist-generation-assessment.md` | Read tasklist CLI code. Determine if `superclaude tasklist generate` exists as a CLI command. Identify generation prompt builder. Understand how TDD/PRD enrichment would work in generation context. |

## SUGGESTED_PHASES

4 researchers in parallel:

- **Researcher 1 (File Inventory — existing E2E task)**: Read `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/TASK-E2E-20260326-modified-repo.md` in full. Extract phase structure, item count per phase, every item's verification pattern, command templates, output directory structure. This researcher provides the CLONE TEMPLATE.
- **Researcher 2 (Integration Points — PRD implementation mapping)**: Read `.dev/tasks/to-do/TASK-RF-20260327-prd-pipeline/TASK-RF-20260327-prd-pipeline.md` in full. Map each of 10 phases to specific E2E test scenarios. Extract new CLI flags, new state file fields, new prompt behaviors, auto-wire logic, redundancy guard behavior.
- **Researcher 3 (Patterns & Conventions — PRD fixture)**: Read `src/superclaude/skills/prd/SKILL.md` and existing fixtures. Determine PRD section structure. Define fixture content requirements aligned with the TDD fixture's "User Authentication Service" scope.
- **Researcher 4 (Data Flow Tracer — tasklist generation)**: Read `src/superclaude/cli/tasklist/` code. Determine if tasklist generate CLI exists. Trace how TDD/PRD files flow into generation prompts. Understand auto-wire from `.roadmap-state.json`.

## TEMPLATE_NOTES

Template 02 (complex) — the task involves:
- Discovery phase (verify CLI flags, fixtures exist)
- Fixture creation (PRD fixture)
- Multi-pipeline execution (30-60 min each)
- Multi-artifact verification per pipeline
- Cross-run comparison (enriched vs non-enriched vs prior results)
- Qualitative QA
- Follow-up reporting

## AMBIGUITIES_FOR_USER

None — intent is clear from the BUILD_REQUEST and conversation context. The user wants:
1. Clone the existing E2E task, uncheck all boxes
2. Modify each phase to also test PRD enrichment
3. Add new phases for auto-wire, generation enrichment, cross-run comparison
4. The PRD fixture must be a product-perspective precursor to the existing TDD fixture

**Status:** Complete
