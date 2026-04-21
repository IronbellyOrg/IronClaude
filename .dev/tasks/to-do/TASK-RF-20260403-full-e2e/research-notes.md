# Research Notes: Complete E2E Pipeline — Roadmap + Tasklist Generation + Validation

**Date:** 2026-04-03
**Scenario:** A (Explicit — detailed build request with copy/restructure instructions)
**Depth Tier:** Deep (80+ item task file, multiple subsystems)
**Track Count:** 1

---

## EXISTING_FILES

### Source Task File (COPY THIS — the primary input)
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` — 67 items, 11 phases, status=done. This is the completed E2E task to copy, reset, restructure, and extend.

### Existing Fixtures (DO NOT RECREATE — verify only)
- `.dev/test-fixtures/test-tdd-user-auth.md` — 876 lines, TDD fixture
- `.dev/test-fixtures/test-spec-user-auth.md` — 312 lines, Spec fixture
- `.dev/test-fixtures/test-prd-user-auth.md` — 406 lines, PRD fixture

### Prior Research (REUSE — already QA'd)
**Tasklist subsystem research (from TASK-RF-20260403-tasklist-e2e):**
- `01-tasklist-prompts.md` — Both prompt builders (generate + fidelity), TDD/PRD conditional blocks, 4 enrichment scenarios
- `02-sc-tasklist-skill.md` — /sc:tasklist protocol, 10-stage pipeline, output format
- `03-tasklist-executor-cli.md` — tasklist validate CLI, auto-wire, fidelity gate
- `04-existing-artifacts.md` — Roadmap content from test dirs, grep targets for enrichment verification
- `05-template-examples.md` — MDTM template 02, prior E2E patterns

**QA fix and auto-detection research (from TASK-RF-20260402-e2e-update):**
- `01-qa-fix-inventory.md` — All 26 FIXED QA findings
- `02-auto-detection-changes.md` — PRD detection, multi-file CLI, routing
- `03-cli-gate-changes.md` — EXTRACT_TDD_GATE, CLI options
- `04-prompt-tasklist-changes.md` — PRD authority language, fidelity checks
- `05-item-impact-mapping.md` — Per-item impact assessment

## PATTERNS_AND_CONVENTIONS

Per prior research. Key for builder:
- `uv run superclaude` for all CLI operations
- `tasklist validate` overwrites `tasklist-fidelity.md` — must copy before next run
- `/sc:tasklist` is inference-only — invoked via Skill tool
- `build_tasklist_generate_prompt(roadmap_file, tdd_file=None, prd_file=None)` — generates prompt text
- All fixtures exist. DO NOT recreate.

## GAPS_AND_QUESTIONS

None — all research from prior builds covers everything needed. The build request provides explicit restructuring instructions.

## RECOMMENDED_OUTPUTS

No new researchers needed. The builder should:
1. Read the source task file
2. Read the build request for restructuring instructions
3. Read the prior tasklist research for new phase content
4. Produce the complete task file

## SUGGESTED_PHASES

Skip researchers — go directly to builder with all existing research referenced.

## TEMPLATE_NOTES

Template 02. The builder copies the source task file structure and extends it per the build request's 7 steps.

## AMBIGUITIES_FOR_USER

None.

**Status:** Complete
