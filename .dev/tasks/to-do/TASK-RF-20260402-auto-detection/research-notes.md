# Research Notes: C-122 Multi-File Auto-Detection and Routing

**Date:** 2026-04-02
**Scenario:** A (Explicit — build request provides detailed spec)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

### Primary modification targets:
- `src/superclaude/cli/roadmap/executor.py` (2719 lines) — Contains `detect_input_type()` at L63-133 (TDD vs spec only), `_route_input_files()` does not exist yet, `execute_roadmap()` at L2078+ handles auto-resolution and guards
- `src/superclaude/cli/roadmap/commands.py` (347 lines) — CLI command definitions, single positional `spec_file` arg at L33, `--tdd-file` at L112, `--prd-file` at L123, `--input-type` at L106
- `src/superclaude/cli/roadmap/models.py` (133 lines) — `RoadmapConfig` dataclass at L94, `input_type: Literal["auto", "tdd", "spec"]` at L114

### Test files:
- `tests/cli/test_tdd_extract_prompt.py` (499 lines) — Existing detection tests: `TestAutoDetection` (6 tests), `TestDetectionThresholdBoundary` (4 tests), `TestTddInputValidation` (5 tests)

### Reference files (detection signal analysis):
- `.dev/test-fixtures/test-prd-user-auth.md` (406 lines) — Real PRD with frontmatter `type: "Product Requirements"`, tags: [prd, ...], sections: User Personas, Jobs To Be Done, Customer Journey Map, etc.
- `.dev/test-fixtures/test-tdd-user-auth.md` (876 lines) — Real TDD with `parent_doc`, `coordinator`, 28 numbered sections
- `.dev/test-fixtures/test-spec-user-auth.md` (312 lines) — Real spec with `spec_type`, 12 sections, no TDD/PRD signals
- `src/superclaude/examples/tdd_template.md` (1334 lines) — TDD template with all frontmatter fields
- `src/superclaude/examples/release-spec-template.md` (264 lines) — Spec template

### Downstream consumers (should NOT be modified):
- `src/superclaude/cli/roadmap/prompts.py` — All 7 prompt builders already accept tdd_file/prd_file
- `src/superclaude/cli/roadmap/gates.py` — EXTRACT_GATE and EXTRACT_TDD_GATE already route by input_type
- `src/superclaude/cli/tasklist/commands.py` — Tasklist auto-wire already reads state file

## PATTERNS_AND_CONVENTIONS

- Detection uses weighted scoring with threshold (see executor.py L63-133)
- CLI uses Click decorators for args/options
- Config uses frozen-ish dataclass with `dataclasses.replace()` for mutations
- Tests use pytest with `tmp_path` fixture for file creation
- `_log.info/warning/error` for logging decisions

## GAPS_AND_QUESTIONS

- What PRD detection threshold should be? (Need researcher to analyze PRD fixture signals)
- How does `nargs=-1` interact with Click options that follow? (Need researcher to verify Click behavior)
- Should PRD-only input (1 file detected as PRD) error or warn? (Build request says error — PRD can't be primary)
- Does the tasklist CLI also need multi-positional args? (Build request only mentions roadmap)

## RECOMMENDED_OUTPUTS

1. `01-detection-signals.md` — Analysis of PRD vs TDD vs spec signals from all 3 fixtures + 2 templates
2. `02-cli-click-nargs.md` — Click nargs=-1 behavior, interaction with options, backward compat
3. `03-routing-logic.md` — Routing rules, edge cases, error messages
4. `04-existing-tests.md` — Current test coverage, what needs extending, test patterns used
5. `05-template-conventions.md` — MDTM template rules, task file structure for this scope

## SUGGESTED_PHASES

- Researcher 1 (File Inventory + Detection Signals): Analyze all 3 fixtures + 2 templates for PRD/TDD/spec signal differentiation. Count signals, propose thresholds.
  - Scope: `.dev/test-fixtures/*.md`, `src/superclaude/examples/*.md`, `src/superclaude/skills/prd/SKILL.md`
  - Output: `research/01-detection-signals.md`

- Researcher 2 (Integration Points): Click nargs=-1 behavior, how it interacts with existing options, backward compatibility with single positional arg.
  - Scope: `src/superclaude/cli/roadmap/commands.py`, Click documentation
  - Output: `research/02-cli-click-nargs.md`

- Researcher 3 (Patterns & Conventions): Current detection code, routing in execute_roadmap, guards, state file handling. Map exact code paths that need changes.
  - Scope: `src/superclaude/cli/roadmap/executor.py` (detection + execute_roadmap sections)
  - Output: `research/03-routing-logic.md`

- Researcher 4 (Test & Verification): Current test coverage for detection, what patterns are used, what new tests are needed.
  - Scope: `tests/cli/test_tdd_extract_prompt.py`
  - Output: `research/04-existing-tests.md`

- Researcher 5 (Template & Examples): MDTM template conventions for the task file.
  - Scope: `.gfdoc/templates/`, `.dev/tasks/to-do/` examples
  - Output: `research/05-template-conventions.md`

## TEMPLATE_NOTES

Template 02 (Complex Task) — this involves discovery (PRD signal analysis), implementation (code changes), and testing (new tests). Multiple phases with different activities.

## AMBIGUITIES_FOR_USER

None — intent is clear from the build request and codebase context.

**Status:** Complete
