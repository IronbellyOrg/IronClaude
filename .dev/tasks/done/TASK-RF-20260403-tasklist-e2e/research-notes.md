# Research Notes: Tasklist Generation + Validation E2E with TDD/PRD Enrichment

**Date:** 2026-04-03
**Scenario:** A (Explicit — build request has full detail)
**Depth Tier:** Standard (5-6 key source files, focused tasklist subsystem)
**Track Count:** 1

---

## EXISTING_FILES

### Prerequisites (ALL EXIST — READ-ONLY, DO NOT REGENERATE)
- `.dev/test-fixtures/results/test1-tdd-prd/roadmap.md` — 32640 bytes, TDD+PRD merged roadmap
- `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json` — 3307 bytes, state with prd_file, input_type=tdd
- `.dev/test-fixtures/results/test2-spec-prd/roadmap.md` — 27698 bytes, Spec+PRD merged roadmap
- `.dev/test-fixtures/results/test2-spec-prd/.roadmap-state.json` — 3318 bytes, state with prd_file, input_type=spec
- `.dev/test-fixtures/test-tdd-user-auth.md` — 44148 bytes, TDD fixture
- `.dev/test-fixtures/test-spec-user-auth.md` — 17400 bytes, Spec fixture
- `.dev/test-fixtures/test-prd-user-auth.md` — 19619 bytes, PRD fixture

### Source Files Under Test
- `src/superclaude/cli/tasklist/prompts.py` — 237 lines: `build_tasklist_generate_prompt`, `build_tasklist_fidelity_prompt`
- `src/superclaude/cli/tasklist/executor.py` — 273 lines: validation pipeline, step construction
- `src/superclaude/cli/tasklist/commands.py` — 185 lines: CLI flags, auto-wire logic
- `.claude/skills/sc-tasklist-protocol/SKILL.md` — 1273 lines: `/sc:tasklist` skill definition

## PATTERNS_AND_CONVENTIONS
- All CLI commands use `uv run superclaude` (never bare `superclaude`)
- `tasklist validate` writes to `tasklist-fidelity.md` in the output dir — OVERWRITES on each run
- `/sc:tasklist` is inference-only (no CLI subprocess) — generates tasklist-index.md + phase files
- `build_tasklist_generate_prompt` signature: `(roadmap_file, tdd_file=None, prd_file=None) -> str`
- `build_tasklist_fidelity_prompt` signature: `(roadmap_file, tasklist_dir, tdd_file=None, prd_file=None) -> str`

## GAPS_AND_QUESTIONS
1. How exactly does `/sc:tasklist` invoke tasklist generation? Need researcher to read SKILL.md and trace the flow.
2. Does `/sc:tasklist` use `build_tasklist_generate_prompt` internally, or does it have its own prompt construction?
3. What output format does `/sc:tasklist` produce? tasklist-index.md + phase-N.md files? Or a single file?
4. Can the task executor invoke `/sc:tasklist` via the Skill tool, or must it use `build_tasklist_generate_prompt` directly?
5. Auto-wire in `commands.py` — does it wire tdd_file/prd_file for validation correctly? (Confirmed in prior E2E Phase 6)

## RECOMMENDED_OUTPUTS

| # | Researcher Topic | Output File | Scope |
|---|-----------------|-------------|-------|
| 01 | Tasklist Prompts & Generation Code | `research/01-tasklist-prompts.md` | prompts.py: both prompt builders, their params, conditional blocks |
| 02 | sc:tasklist Skill Protocol | `research/02-sc-tasklist-skill.md` | SKILL.md: how generation works, output format, integration points |
| 03 | Tasklist Executor & CLI | `research/03-tasklist-executor-cli.md` | executor.py + commands.py: validation pipeline, auto-wire, CLI flags |
| 04 | Existing Roadmap Artifacts | `research/04-existing-artifacts.md` | Read roadmap.md and state.json from both test dirs to understand what the tasklist generator will consume |
| 05 | Template & Prior Task Examples | `research/05-template-examples.md` | MDTM template 02, prior E2E task patterns |

## SUGGESTED_PHASES
- Researcher 1 (File Inventory + Patterns): prompts.py — both builders, conditional blocks, all 4 enrichment scenarios
- Researcher 2 (Data Flow Tracer): sc-tasklist skill — trace generation flow, output format, how it uses prompt builders
- Researcher 3 (Integration Points): executor.py + commands.py — validation pipeline, auto-wire, CLI flag handling
- Researcher 4 (Doc Cross-Validator): roadmap.md + state.json from test1-tdd-prd and test2-spec-prd — what the generator consumes
- Researcher 5 (Template & Examples): MDTM template 02 + prior task examples

## TEMPLATE_NOTES
- Template 02 (complex): multi-phase with generation, validation, comparison
- QA focus: pipeline behavior, not report prose accuracy
- Key challenge: `/sc:tasklist` is inference-only — task items must describe how to invoke it

## AMBIGUITIES_FOR_USER
None — intent is clear from the build request.

**Status:** Complete
