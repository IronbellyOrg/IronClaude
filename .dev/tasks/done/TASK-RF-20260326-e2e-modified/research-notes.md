# Research Notes: E2E Tests — TDD + Spec in Modified Repo

**Date:** 2026-03-26
**Scenario:** A (Explicit — BUILD-REQUEST provides all details)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

### Templates (source for test fixtures)
- `src/superclaude/examples/tdd_template.md` — TDD template, 1300+ lines, 28 numbered sections, all frontmatter fields. Must be populated for "User Authentication Service" to create test fixture.
- `src/superclaude/examples/release-spec-template.md` — Spec template with `{{SC_PLACEHOLDER:...}}` sentinels. Must be populated for same feature.

### CLI Pipeline Files (what we're testing)
- `src/superclaude/cli/roadmap/commands.py` — `run` command with `--input-type [auto|tdd|spec]` (default auto), auto-detection feedback, TDD warning
- `src/superclaude/cli/roadmap/executor.py` — `detect_input_type()` with 4 weighted signals, `_build_steps()` branches on effective_input_type, `execute_roadmap()` orchestrates subprocess pipeline
- `src/superclaude/cli/roadmap/prompts.py` — `build_extract_prompt()` (8 sections, 13 fields), `build_extract_prompt_tdd()` (14 sections, 19 fields), `build_spec_fidelity_prompt()` (generalized "source-document")
- `src/superclaude/cli/roadmap/gates.py` — Gate definitions: EXTRACT_GATE, GENERATE_A/B_GATE, DIFF_GATE, DEBATE_GATE, SCORE_GATE, MERGE_GATE, ANTI_INSTINCT_GATE, TEST_STRATEGY_GATE, SPEC_FIDELITY_GATE, DEVIATION_ANALYSIS_GATE
- `src/superclaude/cli/roadmap/models.py` — `RoadmapConfig` with `input_type` and `tdd_file` fields
- `src/superclaude/cli/roadmap/fingerprint.py` — Extracts backtick identifiers ≥4 chars for anti-instinct audit

### Test Files (existing)
- `tests/cli/test_tdd_extract_prompt.py` — 23 unit tests for TDD extraction, auto-detection, config defaults

### Output Directories (to be created)
- `.dev/test-fixtures/test-tdd-user-auth.md` — populated TDD fixture (Test 1 input)
- `.dev/test-fixtures/test-spec-user-auth.md` — populated spec fixture (Test 2 input)
- `.dev/test-fixtures/results/test1-tdd-modified/` — Test 1 pipeline output
- `.dev/test-fixtures/results/test2-spec-modified/` — Test 2 pipeline output

### E2E Test Plan
- `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md` — master test plan
- `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-modified-repo.md` — this build request

## PATTERNS_AND_CONVENTIONS

### Pipeline execution pattern
The `superclaude roadmap run` command:
1. Resolves input type (auto-detect or explicit flag)
2. Builds steps via `_build_steps()` — extract, generate-a, generate-b, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, deviation-analysis
3. Each step runs a `ClaudeProcess` subprocess: `claude --print -p "<prompt>" <files>`
4. After each step, the gate function validates output (YAML frontmatter parsing, field presence/value checks)
5. Gate tiers: EXEMPT, LIGHT, STANDARD, STRICT

### Auto-detection
`detect_input_type()` scores 4 signals: numbered headings (## N.), TDD frontmatter fields, TDD section names, "Technical Design Document" text. Score ≥3 = TDD.

### Fixture requirements
- TDD fixture: Must have all 28 sections populated with real content (not placeholders). Key identifiers as backticked names for fingerprint coverage ≥0.7.
- Spec fixture: Must use release-spec-template structure with `{{SC_PLACEHOLDER:...}}` sentinels replaced. Behavioral "shall/must" requirements.

### Pipeline output artifacts
Each pipeline run produces: extraction.md, roadmap-{agent1}.md, roadmap-{agent2}.md, diff-analysis.md, debate-transcript.md, base-selection.md, roadmap.md, anti-instinct-audit.md, test-strategy.md, spec-fidelity.md (and optionally deviation-analysis.md)

## GAPS_AND_QUESTIONS

- `.gfdoc/templates/` directory does not exist in this repo. The MDTM template reference path in the builder's STEPS section won't work. The builder should NOT attempt to read that path.
- The `superclaude roadmap run` pipeline takes 30-60 minutes per run (Claude subprocesses). The task executor will need to run these as Bash commands and wait.
- DEVIATION_ANALYSIS_GATE is known TDD-incompatible — Test 1 may fail at this step (expected, warning printed).
- No prior `.dev/test-fixtures/` directory exists — needs creation.

## RECOMMENDED_OUTPUTS

### Research files
1. `01-pipeline-data-flow.md` — How the pipeline flows from input to output, what each step produces, what gates check
2. `02-template-structure.md` — TDD and spec template structures, what sections to populate, frontmatter fields
3. `03-gate-verification.md` — Gate definitions, field requirements, pass/fail criteria for each artifact
4. `04-template-examples.md` — MDTM task file patterns from existing tasks in `.dev/tasks/to-do/`

### Task file
- `TASK-RF-20260326-e2e-modified.md` — MDTM task file with phases for fixture creation, dry-run, Test 1, Test 2, comparison

## SUGGESTED_PHASES

### Researcher 1 (Data Flow Tracer): Pipeline data flow
- Scope: `src/superclaude/cli/roadmap/executor.py`, `commands.py`, `models.py`
- Focus: Trace how `superclaude roadmap run` processes input through all steps, what CLI flags are needed, what output directory structure is created
- Output: `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/research/01-pipeline-data-flow.md`
- Other researchers cover: template structures (02), gate criteria (03), MDTM patterns (04)

### Researcher 2 (File Inventory): Template structures
- Scope: `src/superclaude/examples/tdd_template.md`, `src/superclaude/examples/release-spec-template.md`
- Focus: Full structure of both templates — every section, every frontmatter field, placeholder patterns, what needs to be populated for a realistic "User Authentication Service" fixture
- Output: `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/research/02-template-structure.md`
- Other researchers cover: pipeline flow (01), gate criteria (03), MDTM patterns (04)

### Researcher 3 (Test & Verification): Gate verification criteria
- Scope: `src/superclaude/cli/roadmap/gates.py`, `prompts.py`, `fingerprint.py`
- Focus: Every gate definition, required YAML fields, semantic check functions, pass/fail thresholds. What does `extraction.md` need to have for EXTRACT_GATE? What does `anti-instinct-audit.md` need for ANTI_INSTINCT_GATE?
- Output: `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/research/03-gate-verification.md`
- Other researchers cover: pipeline flow (01), template structures (02), MDTM patterns (04)

### Researcher 4 (Template & Examples): MDTM task patterns
- Scope: `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/`, `.dev/tasks/done/TASK-RF-20260325-001/`
- Focus: How existing MDTM task files are structured, B2 self-contained item patterns, phase organization, how subprocess execution items are written
- Output: `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/research/04-task-patterns.md`
- Other researchers cover: pipeline flow (01), template structures (02), gate criteria (03)

## TEMPLATE_NOTES

**Template selection:** 02 (Complex Task) — multi-phase (fixture creation → dry-run → Test 1 execution → Test 2 execution → comparison), subprocess execution, artifact verification, conditional flows (DEVIATION_ANALYSIS may fail for TDD).

**CRITICAL NOTE:** The `.gfdoc/templates/` directory does NOT exist in this repo. The builder MUST NOT attempt to read `02_mdtm_template_complex_task.md` from that path. Instead, the builder should use the existing task files at `.dev/tasks/to-do/TASK-RF-20260325-cli-tdd/TASK-RF-20260325-cli-tdd.md` as a structural example, and follow the B2 self-contained pattern visible there.

**Tier reasoning:** Standard — 4 researchers, no web agents. The scope is well-defined (specific CLI files, known templates, documented gate criteria). No broad discovery needed.

## AMBIGUITIES_FOR_USER

None — intent is clear from the BUILD-REQUEST file and codebase context. The BUILD-REQUEST specifies every phase, output path, and verification criterion.

**Status:** Complete
