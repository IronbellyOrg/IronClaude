---
id: TASK-RF-20260402-auto-detection
title: "Multi-File Auto-Detection -- Add PRD detection, nargs=-1 CLI, and routing logic"
status: done
priority: high
created: 2026-04-01
start_date: 2026-04-02
updated_date: 2026-04-02
completion_date: 2026-04-02
type: implementation
template: complex
estimated_items: 25
estimated_phases: 7
task_type: static
---

# Multi-File Auto-Detection -- Add PRD detection, nargs=-1 CLI, and routing logic

## Task Overview

This task adds three-way content detection (PRD vs TDD vs spec) to `detect_input_type()`, changes the CLI positional argument from a single file to `nargs=-1` (accepting 1-3 files), and implements `_route_input_files()` routing logic that auto-detects each file and assigns it to the correct config slot (`spec_file`, `tdd_file`, `prd_file`). After this task, users can run `superclaude roadmap run tdd.md prd.md` in any order and the CLI figures out which is which. This absorbs findings C-19 (content validation), C-53 (input-type vs content), and C-55 (PRD misclassification).

## Key Objectives

1. **PRD Detection Signals:** Extend `detect_input_type()` in `src/superclaude/cli/roadmap/executor.py` with 5 weighted PRD signals (frontmatter type field, 12 PRD-exclusive section headings, user story pattern, JTBD pattern, prd tag) and a threshold of >= 5, running PRD scoring before TDD scoring.
2. **CLI nargs=-1:** Change `@click.argument("spec_file", ...)` in `src/superclaude/cli/roadmap/commands.py` to `@click.argument("input_files", nargs=-1, required=True, ...)` with 1-3 file validation, updated function signature, and "prd" added to `--input-type` choices.
3. **Routing Function:** Implement `_route_input_files()` in `executor.py` that classifies each positional file, validates no duplicate types, detects conflicts with explicit `--tdd-file`/`--prd-file` flags, and returns resolved `spec_file`/`tdd_file`/`prd_file`/`input_type` slots.
4. **Test Coverage:** Add ~18 new tests across 5 test classes (PRD detection, three-way boundary, multi-file routing, backward compat, override priority) in `tests/cli/test_tdd_extract_prompt.py`.
5. **Backward Compatibility:** Single-file invocation (`superclaude roadmap run spec.md`) works identically to current behavior; `--tdd-file` and `--prd-file` flags continue to work.

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** None (standalone feature task)
- **Blocking Dependencies:** None
- **This task blocks:** No downstream tasks

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

- **Research: Detection Signals:** `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/01-detection-signals.md` - PRD signal weights, thresholds, verification against 3 fixture files
- **Research: CLI Click nargs:** `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/02-cli-click-nargs.md` - Click nargs=-1 behavior, code sketches, backward compat analysis
- **Research: Routing Logic:** `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/03-routing-logic.md` - 12-step routing algorithm, 6 edge cases, complete code path map
- **Research: Existing Tests:** `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/04-existing-tests.md` - 45 existing tests cataloged, 18 new tests needed across 5 categories
- **Test Fixtures:** `.dev/test-fixtures/test-prd-user-auth.md`, `.dev/test-fixtures/test-tdd-user-auth.md`, `.dev/test-fixtures/test-spec-user-auth.md` - Real PRD/TDD/spec files for detection verification

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/`**

Subdirectories:
- `discovery/` - Discovery scan results and inventories
- `test-results/` - Test output and summaries
- `plans/` - Fix plans and conditional action outputs

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "in-progress" and `start_date` to current date
- **Upon Completion:** Update `status` to "done" and `completion_date` to current date
- **If Blocked:** Update `status` to "blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Detailed Task Instructions

### Phase 1: Preparation and Setup (2 items)

> **Purpose:** Initialize task tracking and create handoff directory structure for inter-phase outputs.

**Step 1.1:** Update task status

- [x] **1.1** Update the `status` field to "in-progress" and `start_date` to today's date in the frontmatter of this task file at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/TASK-RF-20260402-auto-detection.md`, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "in-progress" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Create handoff directories

- [x] **1.2** Create the phase-outputs directory structure at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/` with subdirectories `discovery/`, `test-results/`, and `plans/` to enable intra-task handoff between items, ensuring all directories are created successfully. If the parent directory does not exist, create it first. Once done, mark this item as complete.

---

### Phase 2: PRD Detection in detect_input_type() (3 items)

> **Purpose:** Extend the existing `detect_input_type()` function in `executor.py` to recognize PRD documents using 5 weighted signals, running PRD scoring before TDD scoring with a threshold of >= 5. This is the core detection capability that all downstream routing depends on.

**Step 2.1:** Add PRD scoring block to detect_input_type()

- [x] **2.1** Read the file `executor.py` at `src/superclaude/cli/roadmap/executor.py` lines 63-133 to understand the existing `detect_input_type()` function structure and its TDD scoring pattern (numbered headings, frontmatter fields, section names, type field — each with weights, threshold >= 5), then read the research file `01-detection-signals.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/01-detection-signals.md` sections 6-10 to extract the 5 proposed PRD signals with their exact weights (Signal 1: frontmatter `type` contains "Product Requirements" weight +3, Signal 2: 12 PRD-exclusive section headings weight +1 each, Signal 3: user story regex `As .+, I want` weight +2, Signal 4: JTBD regex `When I .+ I want to` weight +2, Signal 5: prd tag in frontmatter weight +2), then edit `detect_input_type()` in `src/superclaude/cli/roadmap/executor.py` to add a PRD scoring block BEFORE the existing TDD scoring block that: (a) initializes `prd_score = 0`, (b) adds +3 if `"Product Requirements"` appears in `content[:1000]`, (c) iterates over the 12 PRD-exclusive section heading strings (`"User Personas"`, `"Jobs To Be Done"`, `"Product Vision"`, `"Customer Journey"`, `"Value Proposition"`, `"Competitive Analysis"`, `"User Stories"`, `"User Experience Requirements"`, `"Legal and Compliance"`, `"Success Metrics and Measurement"`, `"Maintenance and Ownership"`, `"Background and Strategic Fit"`) adding +1 each, (d) adds +2 if `re.search(r"As .+, I want", content)` matches, (e) adds +2 if `re.search(r"When I .+ I want to", content)` matches, (f) adds +2 if `re.search(r"tags:.*\bprd\b", content[:2000])` matches, (g) returns `"prd"` if `prd_score >= 5`, ensuring the `import re` statement exists at the top of the file, the PRD block runs before TDD scoring so that PRD files are caught first, the existing TDD scoring logic is unchanged, and spec remains the fallback when neither PRD nor TDD threshold is met. If unable to complete due to unexpected function structure or missing file, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** Verify PRD detection against real fixture files

- [x] **2.2** Read the PRD fixture file at `.dev/test-fixtures/test-prd-user-auth.md` to confirm it contains the expected PRD signals (frontmatter `type: "Product Requirements"`, section headings like "User Personas" and "Jobs To Be Done", user story patterns, prd tag), then read the TDD fixture at `.dev/test-fixtures/test-tdd-user-auth.md` and the spec fixture at `.dev/test-fixtures/test-spec-user-auth.md` to confirm they lack PRD signals, then use the Bash tool to run `cd /Users/cmerritt/GFxAI/IronClaude && uv run python -c "from superclaude.cli.roadmap.executor import detect_input_type; from pathlib import Path; print('PRD:', detect_input_type(Path('.dev/test-fixtures/test-prd-user-auth.md'))); print('TDD:', detect_input_type(Path('.dev/test-fixtures/test-tdd-user-auth.md'))); print('Spec:', detect_input_type(Path('.dev/test-fixtures/test-spec-user-auth.md')))"` to verify the three-way detection produces PRD=prd, TDD=tdd, Spec=spec, then write the verification results to the file `detection-verification.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/discovery/detection-verification.md` containing the command output, pass/fail status for each fixture, and any discrepancies found, ensuring all three fixture files are tested and results accurately reflect the actual command output. If any fixture is misclassified, note the exact score and signals in the output file so the detection can be tuned. If unable to complete due to missing fixtures or import errors, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** Update models.py input_type Literal and --input-type Choice

- [x] **2.3** Read the file `models.py` at `src/superclaude/cli/roadmap/models.py` to find the `input_type` field on the `RoadmapConfig` dataclass (currently `Literal["auto", "tdd", "spec"]` per research file `02-cli-click-nargs.md` section 7), then read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to find the `--input-type` option declaration (currently `click.Choice(["auto", "tdd", "spec"])` per research section 7), then edit `models.py` to change the `input_type` type hint to `Literal["auto", "tdd", "spec", "prd"]`, and edit `commands.py` to change the `--input-type` Click.Choice to `["auto", "tdd", "spec", "prd"]` and update its help text to mention PRD detection, ensuring the Literal type and Click.Choice list match exactly and the default remains `"auto"`. If unable to complete due to unexpected field locations, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

### Phase 3: CLI Multi-File Argument (2 items)

> **Purpose:** Change the Click positional argument from a single `spec_file` to variadic `input_files` accepting 1-3 files, update the function signature, and add file count validation. This enables users to pass multiple files positionally.

**Step 3.1:** Change @click.argument to nargs=-1

- [x] **3.1** Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to find the `@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))` decorator (line 33 per research file `02-cli-click-nargs.md` section 1), then edit `commands.py` to replace this decorator with `@click.argument("input_files", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path))`, ensuring `required=True` is set so Click raises an error when zero files are provided, the `type=click.Path(exists=True, path_type=Path)` is preserved to validate each file individually, and the argument name is `input_files` to match the function parameter name that will be updated in step 3.2. If unable to complete due to unexpected decorator structure, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.2:** Update function signature and add file count validation

- [x] **3.2** Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to find the `run()` function signature (lines 134-151 per research file `02-cli-click-nargs.md` section 4), then edit `commands.py` to: (a) change the parameter `spec_file: Path` to `input_files: tuple[Path, ...]`, (b) add file count validation at the top of the function body: `if len(input_files) > 3: raise click.UsageError(f"Expected 1-3 input files, got {len(input_files)}. Provide at most one spec, one TDD, and one PRD.")`, (c) update the function docstring to describe multi-file usage with examples (`superclaude roadmap run spec.md`, `superclaude roadmap run spec.md tdd.md`, `superclaude roadmap run spec.md tdd.md prd.md`), ensuring the parameter name `input_files` exactly matches the `@click.argument` name from step 3.1, the type annotation is `tuple[Path, ...]` (not list), and `click.UsageError` is used for the validation error. If unable to complete due to unexpected function structure, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

### Phase 4: Routing Function in executor.py (4 items)

> **Purpose:** Implement `_route_input_files()` in executor.py that classifies each positional file via `detect_input_type()`, validates no duplicate types, detects conflicts with explicit flags, and returns resolved config slots. Also update `execute_roadmap()` and `_apply_resume_after_spec_patch()` to use the new routing function.

**Step 4.1:** Implement _route_input_files() function

- [x] **4.1** Read the file `executor.py` at `src/superclaude/cli/roadmap/executor.py` to understand the existing `detect_input_type()` function (lines 63-133) and the `execute_roadmap()` function structure (lines 2061-2222), then read the research file `03-routing-logic.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/03-routing-logic.md` sections 7-8 to extract the complete 12-step routing algorithm and 6 edge cases, then add a new function `_route_input_files(input_files: tuple[Path, ...], explicit_tdd: Path | None, explicit_prd: Path | None, explicit_input_type: str) -> dict` in `executor.py` (placed after `detect_input_type()` and before `execute_roadmap()`) that: (1) validates len >= 1 (raise `click.UsageError` if 0), (2) validates len <= 3 (raise `click.UsageError` if >3), (3) classifies each file via `detect_input_type()` which now returns "prd", "tdd", or "spec", (4) if `explicit_input_type != "auto"` and `len(input_files) == 1`, overrides the classification of the single file, (5) if `explicit_input_type != "auto"` and `len(input_files) > 1`, logs a warning that `--input-type` is ignored for multi-file mode, (6) validates no duplicate types (no two files classified as same type -- raise `click.UsageError` with disambiguation guidance), (7) validates that a lone PRD is not the only file (raise `click.UsageError("PRD cannot be the sole primary input")`), (8) assigns slots: spec_file = file classified as "spec" or first TDD if no spec; tdd_file = file classified as "tdd" if a spec exists (supplementary); prd_file = file classified as "prd", (9) checks conflicts: if positional detected TDD and explicit_tdd both set, raise `click.UsageError`; same for PRD, (10) merges explicit flags: tdd_file = explicit_tdd or positional tdd; prd_file = explicit_prd or positional prd, (11) determines input_type: "tdd" if spec_file was classified as TDD, else "spec" (or "prd" if user forced via single-file override), (12) applies redundancy guard: if input_type == "tdd" and tdd_file is not None, warn and null tdd_file, (13) applies same-file guard on all pairs, (14) returns `{"spec_file": ..., "tdd_file": ..., "prd_file": ..., "input_type": ...}`, ensuring the function imports `click` for `UsageError`, uses `_log` for warnings (the module-level logger already exists), handles the single-file backward-compatible path (len==1 with explicit_input_type override), and every edge case from research section 8 is covered. If unable to complete due to unexpected executor structure, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.2:** Update config_kwargs construction in commands.py to use routing

- [x] **4.2** Read the file `commands.py` at `src/superclaude/cli/roadmap/commands.py` to find the `config_kwargs` dictionary construction block (lines 194-207 per research file `03-routing-logic.md` section 1.1) where `spec_file` is assigned from the positional argument, then read the research file `03-routing-logic.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/03-routing-logic.md` section 7 and the research file `02-cli-click-nargs.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/02-cli-click-nargs.md` section 8 to understand the routing call pattern, then edit `commands.py` to: (a) import `_route_input_files` from `.executor`, (b) before `config_kwargs` construction, call `routing = _route_input_files(input_files, explicit_tdd=tdd_file, explicit_prd=prd_file, explicit_input_type=input_type)`, (c) update `config_kwargs` to use `"spec_file": routing["spec_file"].resolve()`, `"tdd_file": routing["tdd_file"].resolve() if routing["tdd_file"] else None`, `"prd_file": routing["prd_file"].resolve() if routing["prd_file"] else None`, `"input_type": routing["input_type"]`, (d) update the output_dir default to use `input_files[0].parent` instead of `spec_file.parent`, ensuring the import is added at the function level (inside the function body alongside the existing `from .executor import execute_roadmap, detect_input_type`), the routing dict keys match exactly what `_route_input_files` returns (`spec_file`, `tdd_file`, `prd_file`, `input_type`), and existing options like `--resume`, `--dry-run`, `--model` etc. are NOT modified. If unable to complete due to unexpected config_kwargs structure, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.3:** Replace inline routing in execute_roadmap() with _route_input_files() call

- [x] **4.3** Read the file `executor.py` at `src/superclaude/cli/roadmap/executor.py` to find the inline auto-resolution block in `execute_roadmap()` (lines 2113-2144 per research file `03-routing-logic.md` section 9.1) which contains: the auto-resolve `if config.input_type == "auto"` block, TDD/PRD file logging, same-file guard, and redundancy guard, then edit `executor.py` to replace that entire block (lines 2113-2144) with a call to `_route_input_files()`: `routing = _route_input_files(input_files=(config.spec_file,), explicit_tdd=config.tdd_file, explicit_prd=config.prd_file, explicit_input_type=config.input_type)` followed by `config = dataclasses.replace(config, spec_file=routing["spec_file"], tdd_file=routing["tdd_file"], prd_file=routing["prd_file"], input_type=routing["input_type"])` and a log line `_log.info("Routing: spec=%s tdd=%s prd=%s type=%s", config.spec_file, config.tdd_file, config.prd_file, config.input_type)`, ensuring `dataclasses` is already imported (it is, per existing code), the replacement preserves the same behavior for single-file invocations, and no other code in `execute_roadmap()` is modified. If unable to complete due to line number drift or unexpected code structure, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.4:** Update _apply_resume_after_spec_patch() auto-resolution

- [x] **4.4** Read the file `executor.py` at `src/superclaude/cli/roadmap/executor.py` to find the duplicate auto-resolution block in `_apply_resume_after_spec_patch()` (lines 2362-2364 per research file `03-routing-logic.md` section 9.2) which contains `if config.input_type == "auto": resolved = detect_input_type(config.spec_file); config = dataclasses.replace(config, input_type=resolved)`, then edit `executor.py` to replace that 3-line block with a `_route_input_files()` call: `routing = _route_input_files(input_files=(config.spec_file,), explicit_tdd=config.tdd_file, explicit_prd=config.prd_file, explicit_input_type=config.input_type)` followed by `config = dataclasses.replace(config, spec_file=routing["spec_file"], tdd_file=routing["tdd_file"], prd_file=routing["prd_file"], input_type=routing["input_type"])`, ensuring the replacement is minimal (only the 3 auto-resolution lines are changed), the surrounding code in `_apply_resume_after_spec_patch()` is not modified, and the function still returns the updated config. If unable to complete due to the code not matching expected structure, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

### Phase 5: Test Implementation (8 items)

> **Purpose:** Add ~18 new tests across 5 test classes covering PRD detection, three-way boundary scoring, multi-file routing scenarios, backward compatibility, and override priority. All tests go in `tests/cli/test_tdd_extract_prompt.py` following the existing Pattern C (synthetic file via tmp_path + detect function call + assert result).

**Step 5.1:** Add TestPrdDetection class -- real fixture detection test

- [x] **5.1** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py` to understand the existing test patterns (particularly `TestAutoDetection` class at lines 121-182 which uses Pattern C: create synthetic file via `tmp_path`, call `detect_input_type()`, assert result) and the real-file pattern (test 16: `test_detects_tdd_from_real_template` which reads `src/superclaude/examples/tdd_template.md`), then read the research file `04-existing-tests.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/04-existing-tests.md` section 5.1 for the 4 PRD detection tests needed, then add a new test class `TestPrdDetection` after the existing `TestAutoDetection` class in `tests/cli/test_tdd_extract_prompt.py` containing the test `test_detects_prd_from_real_fixture` which reads the real PRD fixture at `.dev/test-fixtures/test-prd-user-auth.md` using `Path(".dev/test-fixtures/test-prd-user-auth.md")`, calls `detect_input_type()` on it, and asserts the result is `"prd"` (with a conditional `if path.exists()` guard like test 16), ensuring the import `from superclaude.cli.roadmap.executor import detect_input_type` is present (it can be inside the test method following existing convention), and the test follows the exact same pattern as `test_detects_tdd_from_real_template`. If unable to complete due to missing fixture or unexpected test file structure, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.2:** Add TestPrdDetection -- synthetic PRD signal tests

- [x] **5.2** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py` to find the `TestPrdDetection` class added in step 5.1, then add 3 additional test methods to that class: (a) `test_detects_prd_from_prd_signals` which creates a synthetic file via `tmp_path` containing frontmatter with `type: "Product Requirements"` and sections "User Personas", "Jobs To Be Done", "Product Vision", "User Stories", "Success Metrics and Measurement" (5 headings = +5 plus type field = +3 = score 8, well above threshold 5), calls `detect_input_type()`, and asserts `"prd"`; (b) `test_prd_not_confused_with_tdd` which creates a synthetic file with PRD signals (type field + 5 PRD sections + user story pattern = score 10) but NO TDD signals, calls `detect_input_type()`, and asserts `"prd"` not `"tdd"`; (c) `test_prd_not_confused_with_spec` which creates a file with PRD type field (+3) and 3 PRD section headings (+3) totaling score 6 (above threshold), no TDD signals, calls `detect_input_type()`, and asserts `"prd"` not `"spec"`, ensuring each test method constructs its synthetic file content as a string written to `tmp_path / "doc.md"` following the pattern in existing tests like `test_detects_tdd_from_numbered_headings`, and each test clearly documents its expected score in a comment. If unable to complete, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.3:** Add TestThreeWayBoundary class -- exact score boundary tests

- [x] **5.3** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py` to find the existing `TestDetectionThresholdBoundary` class (lines 351-383, tests TDD score 4=spec, 5=tdd, 6=tdd, 0=spec), then add a new test class `TestThreeWayBoundary` after `TestPrdDetection` containing 4 tests: (a) `test_prd_score_below_threshold_is_spec` which creates a file with only 3 PRD section headings (score 3, below threshold 5) and no TDD signals, asserts `"spec"`; (b) `test_prd_score_at_threshold_is_prd` which creates a file with `type: "Product Requirements"` (+3) and 2 PRD section headings (+2) totaling score 5, no TDD signals, asserts `"prd"`; (c) `test_tdd_signals_only_is_tdd` which creates a file with TDD signals (parent_doc +2, coordinator +2, Data Models section +1 = score 5) and no PRD signals, asserts `"tdd"`; (d) `test_both_prd_and_tdd_signals_prd_wins` which creates a file that has both PRD signals (type field +3, 3 PRD sections +3 = prd_score 6) AND some TDD signals (coordinator +2 = tdd_score 2), verifies that PRD wins because PRD check runs first and prd_score >= 5, asserts `"prd"`, ensuring each test constructs content with precisely calculated scores documented in comments, follows Pattern C, and uses `tmp_path`. If unable to complete, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.4:** Add TestMultiFileRouting class -- single file routing tests

- [x] **5.4** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py` to understand existing patterns, then read the research file `04-existing-tests.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/research/04-existing-tests.md` section 5.3 for the 7 multi-file routing scenarios, then add a new test class `TestMultiFileRouting` containing 3 single-file routing tests: (a) `test_route_single_spec_file` which creates a spec-like file (no TDD/PRD signals) via `tmp_path`, calls `_route_input_files((spec_path,), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")`, and asserts `result["spec_file"] == spec_path`, `result["tdd_file"] is None`, `result["prd_file"] is None`, `result["input_type"] == "spec"`; (b) `test_route_single_tdd_file` which creates a TDD-like file (frontmatter with `parent_doc`, `coordinator`, and TDD section names to reach score >= 5), calls `_route_input_files`, and asserts `result["spec_file"] == tdd_path`, `result["input_type"] == "tdd"`, `result["tdd_file"] is None` (TDD as primary means no supplementary TDD); (c) `test_route_single_prd_raises` which creates a PRD-like file (type: Product Requirements + 3 PRD sections), calls `_route_input_files`, and asserts it raises `click.UsageError` with "PRD cannot be the sole primary input", ensuring `_route_input_files` is imported from `superclaude.cli.roadmap.executor` inside the test methods, `click` is imported for the UsageError check, and `pytest.raises` is used for the error case. If unable to complete, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.5:** Add TestMultiFileRouting -- multi-file routing tests

- [x] **5.5** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py` to find the `TestMultiFileRouting` class added in step 5.4, then add 4 multi-file routing tests: (a) `test_route_spec_plus_tdd` which creates a spec file and a TDD file (both synthetic via `tmp_path`), calls `_route_input_files((spec_path, tdd_path), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")`, asserts `result["spec_file"] == spec_path`, `result["tdd_file"] == tdd_path`, `result["input_type"] == "spec"`; (b) `test_route_spec_plus_prd` which creates a spec file and a PRD file, calls routing, asserts `result["spec_file"] == spec_path`, `result["prd_file"] == prd_path`, `result["tdd_file"] is None`; (c) `test_route_tdd_plus_prd` which creates a TDD file and a PRD file, calls routing, asserts `result["spec_file"] == tdd_path` (TDD becomes primary), `result["prd_file"] == prd_path`, `result["input_type"] == "tdd"`; (d) `test_route_all_three_files` which creates spec + TDD + PRD files, calls routing, asserts `result["spec_file"] == spec_path`, `result["tdd_file"] == tdd_path`, `result["prd_file"] == prd_path`, `result["input_type"] == "spec"`, ensuring each synthetic file has sufficient signals to be classified correctly (spec: plain markdown, TDD: parent_doc + coordinator + Data Models, PRD: type + 5 PRD sections), and the order of files in the tuple should not matter (files are classified by content, not position). If unable to complete, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.6:** Add TestMultiFileRouting -- error case tests

- [x] **5.6** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py` to find the `TestMultiFileRouting` class, then add 3 error case tests: (a) `test_route_duplicate_type_raises` which creates two spec-like files (both with no TDD/PRD signals), calls `_route_input_files((spec1, spec2), ...)`, and asserts `pytest.raises(click.UsageError)` with message containing "Multiple files detected as spec"; (b) `test_route_too_many_files_raises` which creates 4 files, calls `_route_input_files`, and asserts `pytest.raises(click.UsageError)` with message containing "at most" or "1-3"; (c) `test_route_conflict_positional_tdd_and_explicit_tdd_raises` which creates a TDD file and a spec file, calls `_route_input_files((spec_path, tdd_path), explicit_tdd=another_tdd_path, ...)`, and asserts `pytest.raises(click.UsageError)` with message containing "conflict" (case insensitive), ensuring all error tests use `pytest.raises(click.UsageError)` as the assertion mechanism, and each test documents the edge case number from research (8.2, 8.3, 8.4). If unable to complete, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.7:** Add TestBackwardCompat class

- [x] **5.7** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py` to understand existing backward-compat tests (class `TestOldSchemaStateBackwardCompat` lines 299-348), then add a new test class `TestBackwardCompat` containing 3 tests: (a) `test_single_positional_routes_like_before` which creates a spec file via `tmp_path`, calls `_route_input_files((spec_path,), explicit_tdd=None, explicit_prd=None, explicit_input_type="auto")`, asserts `result["spec_file"] == spec_path` and `result["input_type"] == "spec"` (same behavior as old `detect_input_type` + config assignment); (b) `test_explicit_input_type_overrides_detection` which creates a file that auto-detects as "spec", calls `_route_input_files((path,), ..., explicit_input_type="tdd")`, asserts `result["input_type"] == "tdd"` (explicit override works); (c) `test_explicit_tdd_file_flag_works_with_positional` which creates a spec file as the positional and a separate TDD file, calls `_route_input_files((spec_path,), explicit_tdd=tdd_path, explicit_prd=None, explicit_input_type="auto")`, asserts `result["spec_file"] == spec_path` and `result["tdd_file"] == tdd_path` (explicit flag supplements positional), ensuring all tests verify the exact same behavior that existed before the multi-file change. If unable to complete, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.8:** Add TestOverridePriority class

- [x] **5.8** Read the file `test_tdd_extract_prompt.py` at `tests/cli/test_tdd_extract_prompt.py`, then add a new test class `TestOverridePriority` containing 2 tests: (a) `test_input_type_ignored_for_multifile` which creates a spec file and a TDD file, calls `_route_input_files((spec_path, tdd_path), ..., explicit_input_type="prd")`, asserts that `--input-type` is ignored (the files are classified by content, not forced to "prd") -- the result should have `result["spec_file"] == spec_path` and `result["tdd_file"] == tdd_path` based on content detection, not the explicit_input_type value; (b) `test_explicit_prd_flag_works_with_multifile` which creates a spec file and a TDD file as positionals plus a PRD file as explicit flag, calls `_route_input_files((spec_path, tdd_path), explicit_tdd=None, explicit_prd=prd_path, explicit_input_type="auto")`, asserts all three slots are filled correctly (`result["prd_file"] == prd_path`), ensuring both tests demonstrate that explicit flags and content detection coexist correctly in multi-file mode. If unable to complete, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

### Phase 6: Test Execution and Fix Cycle (2 items)

> **Purpose:** Run the full test suite to verify all new and existing tests pass, capture results, and fix any failures. This is the L3 (Test/Execute) + L5 (Conditional-Action) pattern.

**Step 6.1:** Run full test suite and capture results

- [x] **6.1** Use the Bash tool to run the command `cd /Users/cmerritt/GFxAI/IronClaude && uv run pytest tests/cli/test_tdd_extract_prompt.py tests/roadmap/ tests/tasklist/ -v --tb=short 2>&1` to execute all detection-related tests (the new tests from Phase 5 plus all 45 existing tests plus roadmap and tasklist tests for regression), then write the raw output to the file `test-run-raw.txt` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/test-results/test-run-raw.txt` preserving the exact output, then create a structured summary file `test-run-summary.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/test-results/test-run-summary.md` containing: overall result (PASSED/FAILED), total tests run, passed, failed, skipped, a table of any failures with columns: Test Name, Error Type, Brief Message, and the pytest summary line, ensuring the summary accurately reflects the raw output with no fabricated results and all failures are listed. If the command fails to execute (not test failures -- execution failures like import errors), log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 6.2:** Fix failures and re-run (conditional)

- [x] **6.2** Read the test summary at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/test-results/test-run-summary.md` to determine the overall result and any failures. IF the result is PASSED (0 failures), create the file `test-verdict.md` at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/plans/test-verdict.md` containing confirmation that all tests passed with the total count and no further action needed. IF the result is FAILED, read the raw output at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/test-results/test-run-raw.txt` for full error details, then for each failure: read the relevant source file referenced in the error to identify the root cause, apply the fix to the source file (in `src/superclaude/cli/roadmap/executor.py`, `commands.py`, `models.py`, or the test file itself), then re-run the test suite using the same command from step 6.1 and update the summary file with the new results. Repeat the fix-and-rerun cycle up to 3 times. If failures persist after 3 cycles, create `test-verdict.md` documenting the remaining failures with root cause analysis and proposed fixes, then log the blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

---

### Phase 7: Post-Completion Actions (4 items)

> **Purpose:** Final validation, task summary, and status update.

- [x] **7.1** Verify all task outputs by using Glob to confirm every output file specified in checklist items exists on disk: the modified `src/superclaude/cli/roadmap/executor.py` (containing `_route_input_files()` and PRD detection), the modified `src/superclaude/cli/roadmap/commands.py` (containing nargs=-1 and routing call), the modified `src/superclaude/cli/roadmap/models.py` (containing updated Literal type), the modified `tests/cli/test_tdd_extract_prompt.py` (containing 5 new test classes), and the phase-outputs files (`detection-verification.md`, `test-run-summary.md`, `test-verdict.md`), ensuring no expected deliverables are missing. If any files are missing, check the Task Log for blockers explaining the absence. If files are missing without documented reason, log the gap in ### Follow-Up Items below, then mark this item complete. Once done, mark this item as complete.

- [x] **7.2** If source code was modified (it was -- executor.py, commands.py, models.py), confirm tests were verified in Phase 6 by reading the test verdict at `.dev/tasks/to-do/TASK-RF-20260402-auto-detection/phase-outputs/plans/test-verdict.md`. If the verdict is PASSED, note "Tests verified in Phase 6" in the Execution Log. If the verdict documents remaining failures, log them as follow-up items. Once done, mark this item as complete.

- [x] **7.3** Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file, documenting: work completed (PRD detection added to `detect_input_type()`, CLI changed to `nargs=-1`, `_route_input_files()` implemented, ~18 new tests added), challenges encountered during execution, any deviations from the planned process and their rationale, and blockers logged during execution with their resolution status. Once the summary is complete, mark this item as complete.

- [x] **7.4** Update `completion_date` and `updated_date` to today's date and update task status to "done" in the frontmatter of this task file, then add an entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes

### Task Summary

**Work completed:**
- Added PRD detection (5 weighted signals, threshold >= 5) to `detect_input_type()` in executor.py, running before TDD scoring
- Changed CLI positional argument from single `spec_file` to `input_files` with `nargs=-1` accepting 1-3 files
- Implemented `_route_input_files()` routing function with full 12-step algorithm (classification, validation, slot assignment, conflict detection, redundancy guards)
- Replaced inline routing in `execute_roadmap()` and `_apply_resume_after_spec_patch()` with centralized `_route_input_files()` calls
- Added "prd" to `input_type` Literal in models.py and Click.Choice in commands.py
- Added 22 new tests across 5 test classes (TestPrdDetection, TestThreeWayBoundary, TestMultiFileRouting, TestBackwardCompat, TestOverridePriority)
- Updated 2 existing tests (TestSameFileGuard) to expect click.UsageError instead of SystemExit

**Challenges:** 2 existing tests (TestSameFileGuard) broke because the same-file guard moved from inline SystemExit to click.UsageError via _route_input_files(). Fixed in fix cycle 1.

**Deviations:** QA Phase 3 found 2 stale `spec_file` references in commands.py (should have been `input_files[0]`). Fixed in-place by QA agent.

**Blockers:** None.

### Execution Log

| Timestamp | Phase | Item | Status | Notes |
|-----------|-------|------|--------|-------|
| 2026-04-02 | 1 | 1.1 | Done | Task started: Updated status to "in-progress" and start_date |
| 2026-04-02 | 7 | 7.4 | Done | Task completed: Updated status to "done" and completion_date |

### Phase 2 Findings
_No findings yet._

### Phase 3 Findings
_No findings yet._

### Phase 4 Findings
_No findings yet._

### Phase 5 Findings
_No findings yet._

### Phase 6 Findings
_No findings yet._

### Follow-Up Items
_No follow-up items yet._
