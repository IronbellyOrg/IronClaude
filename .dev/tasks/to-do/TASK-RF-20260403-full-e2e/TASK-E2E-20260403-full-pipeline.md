---
id: TASK-E2E-20260403-full-pipeline
title: "E2E Pipeline Tests -- Full Roadmap + Tasklist Generation + Validation (TDD+PRD and Spec+PRD)"
status: in-progress
completion_date: ""
priority: high
created: 2026-04-03
start_date: "2026-04-03"
updated_date: "2026-04-03"
last_session_note: ""
type: verification
template: complex
estimated_items: 79
estimated_phases: 12
tags: ["e2e", "pipeline", "prd", "tdd", "spec", "verification", "roadmap", "auto-wire", "enrichment", "tasklist", "generation", "fidelity"]
handoff_dir: ".dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs"
---

# E2E Pipeline Tests -- Full Roadmap + Tasklist Generation + Validation (TDD+PRD and Spec+PRD)

## Task Overview

This task executes the definitive, complete end-to-end verification of the entire IronClaude pipeline: roadmap generation, tasklist generation, and tasklist validation. It re-runs the two original pipeline tests (TDD path and spec path) with `--prd-file` pointing to the existing PRD fixture, generates tasklists from the resulting roadmaps via the `/sc:tasklist` skill, validates those tasklists with `uv run superclaude tasklist validate` enriched by TDD/PRD supplementary files, and compares all results across runs.

The prior E2E task (TASK-E2E-20260402-prd-pipeline-rerun, 67 items, 11 phases) ran the full roadmap pipeline but NEVER generated a tasklist. Phases 6-7 of that task ran `tasklist validate` against directories with no tasklist, so all TDD/PRD enrichment in `build_tasklist_fidelity_prompt` was validating against nothing. This task closes that gap by inserting tasklist generation phases BEFORE validation, ensuring the fidelity validator runs against real tasklists with real content.

All pipeline runs use `uv run superclaude` (never bare `superclaude`). Each pipeline run spawns Claude subprocesses and takes 30-60 minutes. The three test fixtures already exist on disk and MUST NOT be recreated. New output directories (`test1-tdd-prd-v2/`, `test2-spec-prd-v2/`) avoid overwriting prior results.

## Key Objectives

- Verify `--prd-file` flag is accepted on both `roadmap run` and `tasklist validate` CLI commands
- Verify `--tdd-file` flag is accepted on `roadmap run` CLI
- Confirm PRD supplementary content appears in TDD extraction (personas, metrics, compliance alongside TDD technical content)
- Confirm PRD supplementary content appears in spec-fidelity output (dimensions 12-15)
- Confirm `.roadmap-state.json` stores `tdd_file`, `prd_file`, and `input_type` fields after pipeline run
- Confirm tasklist validate auto-wires `tdd_file` and `prd_file` from `.roadmap-state.json`
- Confirm PRD enrichment does not introduce TDD content into the spec extraction path
- Generate tasklists from both TDD+PRD and Spec+PRD roadmaps via `/sc:tasklist` skill
- Verify TDD enrichment flows through to generated tasklists (component names, API endpoints, test IDs, data models)
- Verify PRD enrichment flows through to generated tasklists (personas, metrics, compliance, acceptance criteria)
- Verify NO TDD content leak in Spec+PRD generated tasklist
- Validate generated tasklists with `tasklist validate` and confirm fidelity reports contain REAL findings (not "Cannot validate -- no tasklist")
- Verify supplementary TDD section has 5 checks with actual MEDIUM findings against real task content
- Verify supplementary PRD section has 4 checks (3 MEDIUM, 1 LOW) with actual findings
- Compare PRD-enriched outputs against prior TDD-only and spec-only baselines
- Document all results in a verification report with cross-run and cross-pipeline comparison

## Prerequisites and Dependencies

**Branch:** `feat/tdd-spec-merge` (or current working branch with all PRD pipeline integration changes merged)

**Implementation prerequisite:** Task `TASK-RF-20260327-prd-pipeline` must be COMPLETE before execution.

**CLI prerequisites (verify in Phase 1):**
- `uv run superclaude roadmap run --help` must show `--prd-file` and `--tdd-file` flags
- `uv run superclaude tasklist validate --help` must show `--prd-file` flag
- `uv run pytest tests/ -v` must pass with no failures

**Existing Fixtures (ALL THREE exist -- DO NOT recreate):**
- `.dev/test-fixtures/test-tdd-user-auth.md` -- TDD fixture (876+ lines)
- `.dev/test-fixtures/test-spec-user-auth.md` -- Spec fixture (312+ lines)
- `.dev/test-fixtures/test-prd-user-auth.md` -- PRD fixture (406+ lines)

**Prior Results (READ-ONLY comparison data):**
- `.dev/test-fixtures/results/test1-tdd-modified/` -- TDD-only pipeline output
- `.dev/test-fixtures/results/test2-spec-modified/` -- spec-only pipeline output
- `.dev/test-fixtures/results/test1-tdd-prd/` -- prior TDD+PRD pipeline output (no tasklist)
- `.dev/test-fixtures/results/test2-spec-prd/` -- prior spec+PRD pipeline output (no tasklist)
- `.dev/test-fixtures/results/verification-report-modified-repo.md` -- prior verification report

**New Output Directories (avoid overwriting prior results):**
- `.dev/test-fixtures/results/test1-tdd-prd-v2/` -- TDD+PRD pipeline output WITH tasklist
- `.dev/test-fixtures/results/test2-spec-prd-v2/` -- spec+PRD pipeline output WITH tasklist

**Tasklist Generation (inference-only -- no CLI command):**
- `/sc:tasklist` skill at `.claude/skills/sc-tasklist-protocol/SKILL.md`
- `build_tasklist_generate_prompt` at `src/superclaude/cli/tasklist/prompts.py`
- There is NO `superclaude tasklist generate` CLI. Generation is inference-only via Skill tool.
- Skill invocation: `Skill("sc-tasklist-protocol", args="<roadmap-path> --spec <tdd-path> --output <output-dir>")` or `Skill("sc-tasklist-protocol", args="<roadmap-path> --output <output-dir>")`

**Tasklist Validation:**
- `uv run superclaude tasklist validate` CLI exists and works
- Each validation run OVERWRITES `tasklist-fidelity.md` -- must copy before next run
- `build_tasklist_fidelity_prompt` at `src/superclaude/cli/tasklist/prompts.py`

**Pipeline Code:**
- `src/superclaude/cli/roadmap/executor.py` -- `detect_input_type()` (3-way: prd/tdd/spec), `_route_input_files()`, `_build_steps()`, `_save_state()`
- `src/superclaude/cli/roadmap/prompts.py` -- 8 prompt builders with TDD/PRD blocks
- `src/superclaude/cli/roadmap/gates.py` -- EXTRACT_TDD_GATE (19 fields), EXTRACT_GATE (13 fields)
- `src/superclaude/cli/roadmap/commands.py` -- `--prd-file`, `--tdd-file`, `nargs=-1` multi-file
- `src/superclaude/cli/tasklist/commands.py` -- `--prd-file`, auto-wire from `.roadmap-state.json`
- `src/superclaude/cli/tasklist/prompts.py` -- fidelity (5 TDD + 4 PRD checks) and generate prompt builders
- `src/superclaude/cli/tasklist/executor.py` -- PRD wiring to inputs and prompt builder

**Known Issues:**
- Anti-instinct gate is the primary blocker: both TDD and spec pipelines halt here (pre-existing). Steps through merge should PASS.
- `uv run superclaude` required -- pipx binary is older version without dev changes.
- `detect_input_type()` performs three-way classification: "prd", "tdd", or "spec". PRD scoring runs FIRST.
- CLI `--input-type` Choice is `["auto", "tdd", "spec"]` -- does NOT include "prd". PRD detection is auto-only.

---

## Phase 1: Preparation and CLI Verification (8 items)

> **Purpose:** Read this task, update status, create output directories, verify all fixtures exist, verify all new CLI flags exist (`--prd-file` on roadmap and tasklist, `--tdd-file` on roadmap), verify multi-file CLI support, run unit tests, and confirm `make verify-sync` passes.

- [x] **1.1** Read this task file in full at `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/TASK-E2E-20260403-full-pipeline.md` to understand all phases, objectives, verification criteria, and known issues. Update the `status` field in this file's YAML frontmatter from `to-do` to `in-progress` and set `start_date` to today's date. If unable to complete due to file access issues, log the specific blocker in the Phase 1 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **1.2** Create the following directory structure for pipeline outputs and handoff files: `.dev/test-fixtures/results/test1-tdd-prd-v2/`, `.dev/test-fixtures/results/test2-spec-prd-v2/`. Also create the handoff directory structure: `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/` with subdirectories `discovery/`, `test-results/`, `reviews/`, and `reports/`. Skip any directories that already exist. If unable to complete due to filesystem permission issues, log the specific blocker in the Phase 1 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **1.3** Verify that all three test fixtures exist and have expected content by running `wc -l .dev/test-fixtures/test-tdd-user-auth.md .dev/test-fixtures/test-spec-user-auth.md .dev/test-fixtures/test-prd-user-auth.md` and confirming: TDD fixture >= 500 lines, spec fixture >= 200 lines, PRD fixture >= 250 lines. Also verify the PRD fixture has correct type by running `grep -c 'type: "Product Requirements"' .dev/test-fixtures/test-prd-user-auth.md` (must return >= 1) and `grep -c 'Technical Design Document' .dev/test-fixtures/test-prd-user-auth.md` (must return 0). Verify PRD personas exist: `grep -c 'Alex the End User' .dev/test-fixtures/test-prd-user-auth.md` (must be > 0), `grep -c 'Jordan the Platform Admin' .dev/test-fixtures/test-prd-user-auth.md` (must be > 0), `grep -c 'Sam the API Consumer' .dev/test-fixtures/test-prd-user-auth.md` (must be > 0). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase1-fixture-verification.md`. If any fixture is missing or malformed, this is a CRITICAL blocker. Log in the Phase 1 Findings section. Once done, mark this item as complete.

- [x] **1.4** Verify that the pipeline CLI supports the new flags and multi-file invocation by running `uv run superclaude roadmap run --help 2>&1` and confirming the output contains: (a) both `--prd-file` and `--tdd-file` options, (b) the positional argument is `INPUT_FILES` (not `SPEC_FILE`) indicating `nargs=-1` multi-file support, (c) `--input-type` shows choices `[auto|tdd|spec]` (must NOT include "prd"), (d) `--input-type` help text mentions PRD auto-detection. Also run `uv run superclaude tasklist validate --help 2>&1` and confirm it contains both `--prd-file` and `--tdd-file`. Verify that `--input-type prd` is NOT accepted by running `uv run superclaude roadmap run --input-type prd .dev/test-fixtures/test-spec-user-auth.md --dry-run 2>&1` and confirming it produces a Click error (invalid choice). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase1-cli-flags.md`. If any required flag is missing, this is a CRITICAL blocker. Log in the Phase 1 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **1.5** Run the full unit test suite by executing `uv run pytest tests/ -v 2>&1 | tail -30` to confirm no regressions. Write the test summary (last 30 lines showing pass/fail counts) to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase1-unit-tests.md`. If any tests fail, log the specific failures in the Phase 1 Findings section. Failing unit tests are a CRITICAL blocker. Once done, mark this item as complete.

- [x] **1.6** Verify skill layer sync by running `make verify-sync 2>&1` and confirming the output indicates `src/superclaude/` and `.claude/` are in sync. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase1-sync-check.md`. If out of sync, run `make sync-dev` first and re-verify. Log any issues in the Phase 1 Findings section. Once done, mark this item as complete.

- [x] **1.7** Run the QA-added unit tests specifically by executing `uv run pytest tests/cli/test_tdd_extract_prompt.py -v 2>&1 | tail -40` to verify all 23 new tests pass (TestPrdDetection 4 tests, TestThreeWayBoundary 4 tests, TestMultiFileRouting 10 tests, TestBackwardCompat 3 tests, TestOverridePriority 2 tests). Also run `uv run pytest tests/cli/ -v -k "prd or routing or detection" 2>&1 | tail -30` to catch additional PRD/routing tests. Write the test summary to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase1-qa-unit-tests.md`. If any new tests fail, log in the Phase 1 Findings section. Once done, mark this item as complete.

- [x] **1.8** Review all Phase 1 results by reading the output files in `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase1-*.md` and determine whether all prerequisites are met. Write a go/no-go summary to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase1-go-nogo.md`. If no-go, subsequent phases cannot proceed until blockers are resolved. Log in the Phase 1 Findings section. Once done, mark this item as complete.

---

## Phase 2: Dry-Run Verification with PRD Flag (8 items)

> **Purpose:** Run fixtures through `uv run superclaude roadmap run --dry-run` with the new `--prd-file` flag to verify flag acceptance, step plan generation, and combined flag behavior BEFORE committing to full pipeline runs. Also test the redundancy guard, multi-file positional invocation (nargs=-1), and backward compatibility.

- [x] **2.1** Run the TDD fixture with PRD through dry-run by executing `uv run superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --dry-run 2>&1` and capture the full output. Verify: (a) the command accepts the `--prd-file` flag without error, (b) the step plan is complete (all pipeline steps listed), (c) no Python traceback appears, (d) stderr contains `[roadmap] Input type: tdd (spec=` showing the new routing format with all three slots, (e) auto-detection identifies the primary input as "tdd". Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-tdd-prd-dryrun.md`. If `--prd-file` is not recognized, this is a CRITICAL blocker. Log in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **2.2** Run the spec fixture with PRD through dry-run by executing `uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --dry-run 2>&1` and capture the full output. Verify: (a) the command accepts the `--prd-file` flag, (b) the step plan is complete, (c) no Python traceback, (d) stderr contains `[roadmap] Input type: spec (spec=` showing the new routing format, (e) auto-detection identifies primary input as "spec". Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-spec-prd-dryrun.md`. If any check fails, log in the Phase 2 Findings section. Once done, mark this item as complete.

- [x] **2.3** Test the `--tdd-file` flag on roadmap run by executing `uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --tdd-file .dev/test-fixtures/test-tdd-user-auth.md --dry-run 2>&1` and verify the command accepts the flag without error. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-tdd-flag-dryrun.md`. Log any issues in the Phase 2 Findings section. Once done, mark this item as complete.

- [x] **2.4** Test the redundancy guard by executing `uv run superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --tdd-file .dev/test-fixtures/test-tdd-user-auth.md --dry-run 2>&1` and verify. The redundancy guard in `_route_input_files()` step 10 nullifies tdd_file to None when input_type is "tdd" and logs `"Ignoring --tdd-file: primary input is already a TDD document."` via `_log.warning()` to stderr. Expected: (a) the command succeeds (no UsageError), (b) stderr contains `Ignoring --tdd-file` warning, (c) the pipeline proceeds with tdd_file=None. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-redundancy-guard.md`. Log in the Phase 2 Findings section. Once done, mark this item as complete.

- [x] **2.5** Test two-file positional invocation (multi-file CLI) by executing `uv run superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md .dev/test-fixtures/test-prd-user-auth.md --dry-run 2>&1` and capturing the full output. Verify: (a) the command accepts two positional files without error, (b) `_route_input_files()` detects TDD as "tdd" and PRD as "prd", (c) routing assigns spec_file=TDD fixture, prd_file=PRD fixture, tdd_file=None, (d) stderr shows `[roadmap] Input type: tdd (spec=` with prd slot populated. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-multifile-two.md`. Log in the Phase 2 Findings section. Once done, mark this item as complete.

- [x] **2.6** Test three-file positional invocation by executing `uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md .dev/test-fixtures/test-tdd-user-auth.md .dev/test-fixtures/test-prd-user-auth.md --dry-run 2>&1` and capturing the full output. Verify: (a) the command accepts three positional files without error, (b) routing assigns spec_file=spec fixture, tdd_file=TDD fixture, prd_file=PRD fixture, (c) input_type="spec", (d) stderr shows all three slots populated. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-multifile-three.md`. Log in the Phase 2 Findings section. Once done, mark this item as complete.

- [x] **2.7** Test backward compatibility of single-file invocation by executing `uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --dry-run 2>&1` and verifying: (a) no error, (b) spec detected as "spec", (c) tdd_file=None, prd_file=None, (d) step plan is complete. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-backward-compat.md`. Log in the Phase 2 Findings section. Once done, mark this item as complete.

- [x] **2.8** Review all Phase 2 results by reading the output files in `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-*.md` and determine whether all flags are working and fixtures are ready for full pipeline runs. Document the go/no-go decision in `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase2-go-nogo.md`. If no-go, subsequent phases cannot proceed. Note that full pipeline runs will take 30-60 minutes each. Log in the Phase 2 Findings section. Once done, mark this item as complete.

---

## Phase 3: Test 1 -- Full TDD+PRD Pipeline Run (14 items)

> **Purpose:** Execute the full `uv run superclaude roadmap run` pipeline with the TDD fixture as primary input and PRD fixture as supplementary input (`--prd-file`). Verify every output artifact for both existing TDD behavior AND new PRD enrichment. Output goes to `test1-tdd-prd-v2/` to avoid overwriting prior results.
>
> **Handoff input:** TDD fixture at `.dev/test-fixtures/test-tdd-user-auth.md`, PRD fixture at `.dev/test-fixtures/test-prd-user-auth.md`

- [x] **3.1** Run the full TDD+PRD pipeline by executing `set -o pipefail && uv run superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --output .dev/test-fixtures/results/test1-tdd-prd-v2/ 2>&1 | tee .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-tdd-prd-pipeline-log.md; echo "EXIT_CODE=$?"`. This command runs all pipeline steps (extract, generate x2, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification) and writes output to `.dev/test-fixtures/results/test1-tdd-prd-v2/`. The extraction step uses EXTRACT_TDD_GATE (19 fields) when input_type=="tdd". **IMPORTANT**: The pipeline takes 30-60 minutes. You MUST set a timeout of at least 3600000ms (60 minutes). Check the echoed EXIT_CODE: 0 means all gates passed, 1 means a gate failure halted the pipeline. Expected: anti-instinct gate will likely halt (pre-existing). Steps through merge should PASS. If the pipeline fails BEFORE merge, log in the Phase 3 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **3.2** Verify the TDD+PRD extraction output frontmatter by reading `extraction.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/extraction.md`. Check that the YAML frontmatter contains all 13 standard fields (`spec_source`, `generated`, `generator`, `functional_requirements`, `nonfunctional_requirements`, `total_requirements`, `complexity_score`, `complexity_class`, `domains_detected`, `risks_identified`, `dependencies_identified`, `success_criteria_count`, `extraction_mode`) plus all 6 TDD-specific fields (`data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`). Verify `data_models_identified` > 0 and `api_surfaces_identified` > 0. Write field-by-field results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-extraction-frontmatter.md`. Log any failures in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.3** Verify the TDD+PRD extraction body sections by reading `extraction.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/extraction.md`. Verify all 14 body sections are present (8 standard + 6 TDD-specific). Run `grep -c '## ' .dev/test-fixtures/results/test1-tdd-prd-v2/extraction.md` and verify count >= 14. **PRD ENRICHMENT CHECK**: Search for PRD supplementary content: `grep -c 'persona\|Persona\|Alex\|Jordan\|Sam' .dev/test-fixtures/results/test1-tdd-prd-v2/extraction.md` (should be > 0), `grep -c 'GDPR\|SOC2\|compliance' .dev/test-fixtures/results/test1-tdd-prd-v2/extraction.md` (should be > 0). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-extraction-sections.md`. Log findings in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.4** Verify the two roadmap variant files by checking that `roadmap-opus-architect.md` and `roadmap-haiku-architect.md` (or files matching `roadmap-*.md` excluding `roadmap.md`) exist in `.dev/test-fixtures/results/test1-tdd-prd-v2/`. For each, verify: at least 100 lines, YAML frontmatter with `spec_source`/`complexity_score`/`primary_persona`, and at least 2 of the 9 TDD backticked identifiers (`UserProfile`, `AuthToken`, `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `LoginPage`, `RegisterPage`, `AuthProvider`). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-roadmap-variants.md`. Log findings in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.5a** Verify the diff analysis artifact by reading `diff-analysis.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/diff-analysis.md`. Check that the file exists, has at least 30 lines, and its YAML frontmatter contains `total_diff_points` and `shared_assumptions_count`. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-diff-analysis.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.5b** Verify the debate transcript artifact by reading `debate-transcript.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/debate-transcript.md`. Check that the file exists, has at least 50 lines, and its YAML frontmatter contains `convergence_score` and `rounds_completed`. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-debate-transcript.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.5c** Verify the base selection artifact by reading `base-selection.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/base-selection.md`. Check that the file exists, has at least 20 lines, and its YAML frontmatter contains `base_variant` and `variant_scores`. **PRD ENRICHMENT CHECK**: Search for PRD-influenced scoring: `grep -c 'business value\|Business Value\|persona\|Persona\|compliance\|Compliance' .dev/test-fixtures/results/test1-tdd-prd-v2/base-selection.md` (should be > 0). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-base-selection.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.6** Verify the merged roadmap by reading `roadmap.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md`. Check at least 150 lines, YAML frontmatter with `spec_source`, `complexity_score`, `adversarial: true`. Search for at least 3 of the 9 TDD backticked identifiers. **PRD ENRICHMENT CHECK**: Search for business value content: `grep -c 'business value\|Business Value\|persona\|Persona\|compliance\|GDPR\|SOC2\|registration.*rate\|session.*duration' .dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md`. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-merged-roadmap.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.7** Verify the anti-instinct audit by reading `anti-instinct-audit.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/anti-instinct-audit.md`. Check that `fingerprint_coverage` >= 0.7, and note `undischarged_obligations` and `uncovered_contracts`. Expected: anti-instinct will likely fail (pre-existing). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-anti-instinct.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.8** Verify the test strategy output (if produced) by checking if `test-strategy.md` exists at `.dev/test-fixtures/results/test1-tdd-prd-v2/test-strategy.md`. If it exists, check frontmatter for `complexity_class`, `validation_philosophy`. If the file does not exist (expected if anti-instinct halted the pipeline), note "SKIPPED -- anti-instinct halt" and do not treat as failure. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-test-strategy.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.9** Verify the spec-fidelity output (if produced) by checking if `spec-fidelity.md` exists at `.dev/test-fixtures/results/test1-tdd-prd-v2/spec-fidelity.md`. If it exists, check `high_severity_count`, `validation_complete`. For TDD+PRD path where TDD is the primary input, `tdd_file` is null so dims 7-11 should be ABSENT. Only base dims (1-6) plus PRD dims 12-15 should be present. **PRD ENRICHMENT CHECK**: Search for PRD dims 12-15: Persona Coverage, Business Metric Traceability, Compliance/Legal, Scope Boundary. If not produced, note "SKIPPED". Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-spec-fidelity.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.10** Verify the wiring-verification output by reading `wiring-verification.md` at `.dev/test-fixtures/results/test1-tdd-prd-v2/wiring-verification.md`. Check it exists, has at least 10 lines, and frontmatter contains `analysis_complete: true` and `blocking_findings: 0`. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-wiring-verification.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.11** Verify the pipeline state file by reading `.dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json`. Check it contains: `schema_version` (should be 1), `spec_file` (path to TDD fixture), `spec_hash` (non-empty), `agents` (array >= 2), `steps` object. **NEW PRD FIELDS CHECK**: Verify: `tdd_file` (should be null -- TDD is primary, not supplementary), `prd_file` (should be absolute path to PRD fixture), `input_type` (should be "tdd" -- never "auto"). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-state-file.md`. Log in the Phase 3 Findings section. Once done, mark this item as complete.

- [x] **3.12** Write a Phase 3 summary by reading all phase-outputs files matching `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase3-*.md` and compiling a pass/fail table. Write the summary to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/test1-tdd-prd-v2-summary.md` with: (1) pass/fail table with columns: Artifact, Gate, Check, Result (PASS/FAIL), Notes, (2) "PRD Enrichment Results" table, (3) count of total checks passed vs failed, (4) "Critical Findings" from Phase 3 Findings table, (5) "Follow-Up Actions". Log in the Phase 3 Findings section if unable to compile. Once done, mark this item as complete.

---

## Phase 4: Test 2 -- Full Spec+PRD Pipeline Run (9 items)

> **Purpose:** Execute the full `uv run superclaude roadmap run` pipeline with the spec fixture as primary input and PRD fixture as supplementary input. Verify key output artifacts for existing spec behavior (no TDD leaks) AND new PRD enrichment. Output goes to `test2-spec-prd-v2/`.
>
> **Handoff input:** Spec fixture at `.dev/test-fixtures/test-spec-user-auth.md`, PRD fixture at `.dev/test-fixtures/test-prd-user-auth.md`

- [x] **4.1** Run the full spec+PRD pipeline by executing `set -o pipefail && uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --output .dev/test-fixtures/results/test2-spec-prd-v2/ 2>&1 | tee .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-spec-prd-pipeline-log.md; echo "EXIT_CODE=$?"`. This runs the standard spec extraction path with PRD supplementary enrichment. **IMPORTANT**: 30-60 minute timeout required (3600000ms). Expected: anti-instinct will likely halt. Steps through merge should PASS. If the pipeline fails BEFORE merge, log in the Phase 4 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [x] **4.2** Verify the spec+PRD extraction frontmatter by reading `extraction.md` at `.dev/test-fixtures/results/test2-spec-prd-v2/extraction.md`. Check that the YAML frontmatter contains ONLY the 13 standard fields and does NOT contain any of the 6 TDD-specific fields (`data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`). **CRITICAL**: TDD fields must be ABSENT -- the spec+PRD path must not introduce TDD content. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-extraction-frontmatter.md`. If any TDD field is present, add a CRITICAL finding. Once done, mark this item as complete.

- [x] **4.3** Verify the spec+PRD extraction body sections by reading `extraction.md` at `.dev/test-fixtures/results/test2-spec-prd-v2/extraction.md`. Verify ONLY the 8 standard sections are present. Search for the 6 TDD-specific sections -- all must be ABSENT. **PRD ENRICHMENT CHECK**: Search for PRD content: `grep -c 'persona\|Persona\|Alex\|Jordan\|Sam' .dev/test-fixtures/results/test2-spec-prd-v2/extraction.md`, `grep -c 'GDPR\|SOC2\|compliance' .dev/test-fixtures/results/test2-spec-prd-v2/extraction.md`. PRD content may appear alongside standard spec extraction (expected and desirable). TDD content must NOT appear. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-extraction-sections.md`. Log in the Phase 4 Findings section. Once done, mark this item as complete.

- [x] **4.4** Verify the spec+PRD merged roadmap by reading `roadmap.md` at `.dev/test-fixtures/results/test2-spec-prd-v2/roadmap.md`. Check at least 150 lines, YAML frontmatter with `spec_source`, `complexity_score`, `adversarial: true`. **PRD ENRICHMENT CHECK**: Search for business value content, persona references, compliance milestones. **TDD LEAK CHECK**: Search for TDD-specific identifiers (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `LoginPage`, `RegisterPage`, `AuthProvider`) -- these should be ABSENT or minimal. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-merged-roadmap.md`. Log in the Phase 4 Findings section. Once done, mark this item as complete.

- [x] **4.5** Verify the spec+PRD anti-instinct audit by reading `anti-instinct-audit.md` at `.dev/test-fixtures/results/test2-spec-prd-v2/anti-instinct-audit.md`. Check `fingerprint_coverage` >= 0.7, note `undischarged_obligations` and `uncovered_contracts`. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-anti-instinct.md`. Log in the Phase 4 Findings section. Once done, mark this item as complete.

- [x] **4.6** Verify the spec+PRD spec-fidelity output (if produced) by checking if `spec-fidelity.md` exists at `.dev/test-fixtures/results/test2-spec-prd-v2/spec-fidelity.md`. If it exists, check `high_severity_count` is 0, `validation_complete` is true. **PRD ENRICHMENT CHECK**: Search for dimensions 12-15. **TDD LEAK CHECK**: TDD-specific dimensions 7-11 must be ABSENT (C-03 fix excludes when tdd_file is None). If not produced, note "SKIPPED". Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-spec-fidelity.md`. Log in the Phase 4 Findings section. Once done, mark this item as complete.

- [x] **4.7** Verify the spec+PRD state file by reading `.dev/test-fixtures/results/test2-spec-prd-v2/.roadmap-state.json`. Check for standard fields plus: `tdd_file` (should be null), `prd_file` (absolute path to PRD fixture), `input_type` (should be "spec" -- never "auto"). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-state-file.md`. Log in the Phase 4 Findings section. Once done, mark this item as complete.

- [x] **4.8** Verify all gates passed for the spec+PRD pipeline by reading the pipeline log at `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-spec-prd-pipeline-log.md` and the `.roadmap-state.json` step-by-step status. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-pipeline-status.md`. Log any unexpected failures in the Phase 4 Findings section. Once done, mark this item as complete.

- [x] **4.9** Write a Phase 4 summary by reading all `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase4-*.md` files. Write to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/test2-spec-prd-v2-summary.md` with: (1) pass/fail table, (2) "PRD Enrichment Results" table, (3) "TDD Leak Check" table confirming zero TDD content, (4) key success criteria, (5) Critical Findings, (6) Follow-Up Actions. Once done, mark this item as complete.

---

## Phase 5: Generate Tasklist from Test 1 TDD+PRD Roadmap (6 items)

> **Purpose:** Generate a tasklist from the Test 1 (TDD+PRD) roadmap using the `/sc:tasklist` skill. This is the first time a tasklist is generated in the E2E pipeline. The generated tasklist will be used by Phases 7-8 for auto-wire and validation enrichment testing. Verify TDD enrichment (component names, API endpoints, test IDs, data models) and PRD enrichment (personas, metrics, compliance) flow through to the generated tasklist.
>
> **Handoff input:** Test 1 roadmap at `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md`, TDD fixture at `.dev/test-fixtures/test-tdd-user-auth.md`, PRD fixture at `.dev/test-fixtures/test-prd-user-auth.md`
>
> **Generation mechanism:** There is NO `superclaude tasklist generate` CLI command. Generation is inference-only via the `/sc:tasklist` skill invoked through the Skill tool. The skill reads the roadmap, optional `--spec` (TDD) and `--prd-file` (PRD) files, and produces `tasklist-index.md` + `phase-N-tasklist.md` files in the output directory.

- [ ] **5.1** Read the Test 1 TDD+PRD roadmap at `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md` to confirm it exists and has at least 150 lines. Also read `.dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json` to confirm `input_type` is "tdd" and `prd_file` is populated. Then invoke the `/sc:tasklist` skill to generate a tasklist from this roadmap by calling `Skill("sc-tasklist-protocol", args=".dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md --spec .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --output .dev/test-fixtures/results/test1-tdd-prd-v2/")`. The `--spec` flag passes the TDD fixture as the supplementary TDD file (the skill uses `--spec` for TDD input). The `--prd-file` flag passes the PRD fixture. NOTE: The skill's argument-hint in SKILL.md frontmatter does not list `--prd-file`, but section 4.1b of the skill protocol supports it. The skill will produce `tasklist-index.md` and `phase-N-tasklist.md` files in the output directory. **IMPORTANT**: Tasklist generation via skill invocation may take 10-30 minutes depending on roadmap size. If the skill fails or produces no output, log the specific error in the Phase 5 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **5.2** Verify tasklist output structure for Test 1 by checking that `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` exists and has at least 50 lines. Run `ls -la .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md 2>&1` and verify at least 2 phase files exist. For each phase file, verify it has at least 20 lines and contains `### T` (task heading pattern). Run `grep -c '- \[' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` to verify checklist items exist across phase files. Write structural verification results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase5-tasklist-structure.md` with file inventory table (File, Lines, Task Count). If tasklist-index.md is missing, this is a CRITICAL blocker for Phases 7-8. Log in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.3** Verify TDD enrichment in the generated Test 1 tasklist by reading `tasklist-index.md` and all `phase-*-tasklist.md` files in `.dev/test-fixtures/results/test1-tdd-prd-v2/`. Run the following grep checks against all tasklist files: (a) `grep -rl 'UserProfile\|AuthToken' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md .dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` -- data model entities from TDD S7 should appear, (b) `grep -rl 'AuthService\|TokenManager' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- component names from TDD S10 should appear, (c) `grep -rl '/auth/login\|/auth/register' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- API endpoints from TDD S8 should appear, (d) `grep -rl 'UT-001\|IT-001\|E2E-001' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- test artifact IDs from TDD S15 should appear, (e) `grep -rl 'rollback\|rollout\|migration' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- migration/rollout tasks from TDD S19 should appear. Write a TDD enrichment verification table to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase5-tdd-enrichment.md` with columns: Category, Grep Pattern, Files Found, Assessment (ENRICHED/NOT-ENRICHED). If no TDD content appears, the skill's TDD enrichment is not working. Log in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.4** Verify PRD enrichment in the generated Test 1 tasklist by running grep checks against all tasklist files in `.dev/test-fixtures/results/test1-tdd-prd-v2/`: (a) `grep -rl 'Alex\|Jordan\|Sam' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md .dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` -- persona references from PRD S7 should appear, (b) `grep -rl 'GDPR\|SOC2' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- compliance mandates from PRD S17 should appear, (c) `grep -rl 'conversion\|> 60%\|60%' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- success metric targets from PRD S19, (d) `grep -rl '< 200ms\|200ms\|latency' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- performance targets from PRD S19, (e) `grep -rl 'acceptance\|journey\|scenario' .dev/test-fixtures/results/test1-tdd-prd-v2/phase-*-tasklist.md` -- customer journey verification from PRD S22. Write a PRD enrichment verification table to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase5-prd-enrichment.md` with columns: Category, Grep Pattern, Files Found, Assessment. Log in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.5** Verify the tasklist-index.md contains required structural elements by reading `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` and checking for: (a) `## Phase Files` section listing all phase files, (b) `## Roadmap Item Registry` with R-### entries, (c) `## Deliverable Registry` with D-#### entries, (d) `## Traceability Matrix` linking roadmap items to tasks to deliverables. Count R-### entries (should be > 0) and D-#### entries (should be > 0). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase5-index-structure.md`. Log in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.6** Write a Phase 5 summary by reading all `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase5-*.md` files. Write to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/test1-tasklist-generation-summary.md` with: (1) Generation result (SUCCESS/FAILURE), (2) File inventory table, (3) TDD enrichment results table, (4) PRD enrichment results table, (5) Index structure verification results, (6) Critical Findings from Phase 5 Findings. This summary confirms whether tasklist generation produced a real, enriched tasklist for Phases 7-8 to validate against. Once done, mark this item as complete.

---

## Phase 6: Generate Tasklist from Test 2 Spec+PRD Roadmap (6 items)

> **Purpose:** Generate a tasklist from the Test 2 (Spec+PRD) roadmap using the `/sc:tasklist` skill with PRD enrichment only (no TDD). Verify PRD enrichment flows through, and critically verify NO TDD content leak -- the Spec+PRD path should produce tasklists with business context (personas, compliance, metrics) but NOT technical implementation detail from the TDD.
>
> **Handoff input:** Test 2 roadmap at `.dev/test-fixtures/results/test2-spec-prd-v2/roadmap.md`, PRD fixture at `.dev/test-fixtures/test-prd-user-auth.md`

- [ ] **6.1** Read the Test 2 Spec+PRD roadmap at `.dev/test-fixtures/results/test2-spec-prd-v2/roadmap.md` to confirm it exists and has at least 150 lines. Also read `.dev/test-fixtures/results/test2-spec-prd-v2/.roadmap-state.json` to confirm `input_type` is "spec" and `prd_file` is populated. Then invoke the `/sc:tasklist` skill to generate a tasklist from this roadmap by calling `Skill("sc-tasklist-protocol", args=".dev/test-fixtures/results/test2-spec-prd-v2/roadmap.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --output .dev/test-fixtures/results/test2-spec-prd-v2/")`. Note: NO `--spec` flag is passed because this is the Spec+PRD path (no supplementary TDD). The skill will produce `tasklist-index.md` and `phase-N-tasklist.md` files in the output directory. **IMPORTANT**: Generation may take 10-30 minutes. If the skill fails, log in the Phase 6 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **6.2** Verify tasklist output structure for Test 2 by checking that `.dev/test-fixtures/results/test2-spec-prd-v2/tasklist-index.md` exists and has at least 50 lines. Run `ls -la .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md 2>&1` and verify at least 2 phase files exist. For each phase file, verify it has at least 20 lines and contains `### T` (task heading pattern). Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase6-tasklist-structure.md`. If tasklist-index.md is missing, this is a CRITICAL blocker. Log in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.3** Verify PRD enrichment in the generated Test 2 tasklist by running grep checks against all tasklist files in `.dev/test-fixtures/results/test2-spec-prd-v2/`: (a) `grep -rl 'Alex\|Jordan\|Sam' .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md .dev/test-fixtures/results/test2-spec-prd-v2/tasklist-index.md` -- persona references, (b) `grep -rl 'GDPR\|SOC2' .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md` -- compliance mandates, (c) `grep -rl 'conversion\|> 60%\|60%' .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md` -- success metrics, (d) `grep -rl '< 200ms\|200ms\|latency' .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md` -- performance targets, (e) `grep -rl 'acceptance\|journey\|scenario' .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md` -- customer journeys. Write a PRD enrichment verification table to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase6-prd-enrichment.md`. Log in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.4** Verify NO TDD content leak in the generated Test 2 tasklist by running negative grep checks against all tasklist files in `.dev/test-fixtures/results/test2-spec-prd-v2/`: (a) `grep -rl 'AuthService\|TokenManager\|JwtService\|PasswordHasher' .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md` -- TDD component names should be ABSENT or minimal (these come from TDD S10, not from the spec or PRD), (b) `grep -rl 'UT-001\|IT-001\|E2E-001' .dev/test-fixtures/results/test2-spec-prd-v2/phase-*-tasklist.md` -- TDD test IDs should be ABSENT (these come from TDD S15), (c) `grep -c 'UserProfile\|AuthToken' .dev/test-fixtures/results/test2-spec-prd-v2/tasklist-index.md` -- TDD data model names: check if present. Note: some component names like AuthService may appear in the spec roadmap organically (from the spec fixture itself), so a few matches are tolerable. The key check is that TDD-SPECIFIC content (test IDs like UT-001, detailed data model field types, API endpoint request/response schemas) does NOT appear. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase6-tdd-leak-check.md` with columns: Pattern, Files Matched, Count, Assessment (CLEAN/LEAK). If significant TDD content appears, flag as IMPORTANT. Log in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.5** Verify the Test 2 tasklist-index.md contains required structural elements by reading `.dev/test-fixtures/results/test2-spec-prd-v2/tasklist-index.md` and checking for: (a) `## Phase Files` section, (b) `## Roadmap Item Registry`, (c) `## Deliverable Registry`, (d) `## Traceability Matrix`. Count R-### and D-#### entries. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase6-index-structure.md`. Log in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.6** Write a Phase 6 summary by reading all `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase6-*.md` files. Write to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/test2-tasklist-generation-summary.md` with: (1) Generation result (SUCCESS/FAILURE), (2) File inventory table, (3) PRD enrichment results table, (4) TDD leak check results table (CRITICAL -- must be CLEAN), (5) Index structure verification, (6) Critical Findings. Once done, mark this item as complete.

---

## Phase 7: Auto-Wire from .roadmap-state.json (6 items)

> **Purpose:** Test that `uv run superclaude tasklist validate` can auto-wire `tdd_file` and `prd_file` from the `.roadmap-state.json` saved by the roadmap pipeline, without requiring explicit CLI flags. NOW validates against directories WITH real tasklists (generated in Phases 5-6), so fidelity reports should contain REAL findings with actual severity ratings -- not "Cannot validate -- no tasklist".
>
> **Handoff input:** Test 1 output at `.dev/test-fixtures/results/test1-tdd-prd-v2/` (contains `.roadmap-state.json`, roadmap.md, AND generated tasklist files)
>
> **KNOWN BEHAVIOR:** `_collect_tasklist_files` at `tasklist/executor.py:44` uses `glob("*.md")` to collect ALL markdown files in the output directory — not just tasklist files. This means validation embeds extraction.md, roadmap.md, diff-analysis.md, etc. alongside the actual tasklist files. This is existing pipeline behavior. The validator LLM should still produce meaningful fidelity results focused on roadmap→tasklist alignment despite the extra files in context. If fidelity reports reference non-tasklist files (e.g., extraction.md) as downstream artifacts, note this as a pipeline behavior finding.

- [ ] **7.1** Run tasklist validate on Test 1 output WITHOUT explicit supplementary file flags by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd-v2/ 2>&1 | tee .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-autowire-basic.md; echo "EXIT_CODE=$?"`. Check for auto-wire info messages: (a) `grep -c 'Auto-wired.*prd' .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-autowire-basic.md` -- should find the auto-wire message, (b) check if `tdd_file` was auto-wired (for TDD primary input, `tdd_file` is null in state but `input_type=tdd` triggers fallback to `spec_file`). The validation now runs against a REAL tasklist (generated in Phase 5) so the fidelity report should contain actual DEV-NNN findings with real severity ratings. Verify `input_type` is correctly restored from state (C-91 fix). If auto-wire messages are absent, log in the Phase 7 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **7.2** Verify the auto-wired fidelity report contains REAL findings by reading the tasklist fidelity report at `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-fidelity.md`. Because a real tasklist now exists (generated in Phase 5), the report should contain: (a) `downstream_file` referencing actual tasklist files (NOT `[NO TASKLIST GENERATED]`), (b) `validation_complete: true`, (c) actual DEV-NNN deviation entries with real severity ratings (HIGH, MEDIUM, LOW) based on comparing the roadmap against the generated tasklist, (d) "Supplementary TDD Validation" section with 5 checks evaluating real task content (test cases S15, rollback S19, components S10, data models S7, API endpoints S8), (e) "Supplementary PRD Validation" section with 4 checks evaluating real task content (persona coverage S7, success metrics S19, acceptance scenarios S12/S22, priority ordering S5), (f) first 3 PRD checks should report MEDIUM severity, 4th (priority ordering) should report LOW severity. IMPORTANT: The prior E2E run's fidelity report said "Cannot validate -- no tasklist". This time it must have REAL content. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-autowire-fidelity.md`. Log in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.3** IMPORTANT: Before proceeding, copy the fidelity report to preserve it because the next validation run will OVERWRITE it. Execute `cp .dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-fidelity.md .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-fidelity-autowired-backup.md`. Then test explicit flag precedence over auto-wire by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd-v2/ --prd-file .dev/test-fixtures/test-spec-user-auth.md 2>&1 | head -20` (deliberately passing the SPEC fixture as `--prd-file`). Verify: (a) no auto-wire info message for `prd_file`, (b) the command does not error, (c) if both paths differ, a log message noting the override should appear. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-autowire-precedence.md`. Log in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.4** Test graceful degradation when auto-wired file path does not exist on disk. Create a modified `.roadmap-state.json`: read `.dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json`, copy to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-state-modified.json` with `prd_file` changed to `/tmp/nonexistent-prd.md`. Create a temporary test directory at `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-degradation-test/`, copy the modified state file there as `.roadmap-state.json`, copy the Test 1 roadmap.md and all tasklist files there, and run `uv run superclaude tasklist validate .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-degradation-test/ 2>&1 | head -20`. Verify: (a) a warning is emitted, (b) no crash, (c) validation proceeds without PRD enrichment. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-autowire-degradation.md`. Log in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.5** Test auto-wire with no `.roadmap-state.json` present. Run `uv run superclaude tasklist validate .dev/test-fixtures/ 2>&1 | head -20` (a directory that has no state file). Verify: (a) no auto-wire messages, (b) no error or crash, (c) command either proceeds normally or fails gracefully because no roadmap.md is found. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-autowire-no-state.md`. Log in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.6** Write a Phase 7 summary by reading all `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase7-*.md` files. Write to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/auto-wire-summary.md` with: (1) Auto-wire test results table (Scenario, Expected Behavior, Actual Behavior, PASS/FAIL), (2) CRITICAL: Fidelity report now has REAL findings (compare with prior E2E where it said "no tasklist"), (3) PRD fidelity enrichment validation results, (4) Critical Findings. Once done, mark this item as complete.

---

## Phase 8: Tasklist Validation Enrichment Testing (6 items)

> **Purpose:** Test that `uv run superclaude tasklist validate` produces enriched fidelity reports when supplementary TDD and PRD files are provided. NOW validates against REAL tasklists (generated in Phases 5-6). Compare enriched validation against baseline to quantify the value added by TDD/PRD enrichment. Supplementary TDD should have 5 checks with actual MEDIUM findings against real task content. Supplementary PRD should have 4 checks (3 MEDIUM, 1 LOW) with actual findings.
>
> **Handoff input:** Test 1 output at `.dev/test-fixtures/results/test1-tdd-prd-v2/` (roadmap + tasklist + state file), Test 2 output at `.dev/test-fixtures/results/test2-spec-prd-v2/` (roadmap + tasklist + state file)

- [ ] **8.1** Run tasklist validate with explicit TDD+PRD flags on Test 1 output by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd-v2/ --tdd-file .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md 2>&1 | tee .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-validate-enriched.md; echo "EXIT_CODE=$?"`. This exercises the full enrichment path with a REAL tasklist. Both TDD and PRD supplementary validation blocks should appear in the fidelity report with REAL findings against actual task content. The report should show: (a) Supplementary TDD Validation with 5 checks (S15 test cases, S19 rollback, S10 components, S7 data models, S8 API endpoints) each with MEDIUM severity findings against real tasks, (b) Supplementary PRD Validation with 4 checks (S7 persona coverage, S19 success metrics, S12/S22 acceptance scenarios, S5 priority ordering) with 3 MEDIUM + 1 LOW severity findings. IMPORTANT: Copy the fidelity report immediately after this run: `cp .dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-fidelity.md .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-fidelity-enriched-backup.md`. Log in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.2** Run tasklist validate WITHOUT any supplementary enrichment (baseline) on the same output. To prevent auto-wire from `.roadmap-state.json` injecting tdd_file/prd_file, temporarily rename the state file: `mv .dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json .dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json.bak`. Then run `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd-v2/ 2>&1 | tee .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-validate-baseline.md; echo "EXIT_CODE=$?"`. Without the state file, no auto-wire occurs and no --tdd-file or --prd-file flags are passed — producing a clean baseline with no supplementary enrichment. After the run completes, restore the state file: `mv .dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json.bak .dev/test-fixtures/results/test1-tdd-prd-v2/.roadmap-state.json`. IMPORTANT: Copy the baseline fidelity report: `cp .dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-fidelity.md .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-fidelity-baseline-backup.md`. The goal is to compare enriched (8.1) vs baseline (this item) to prove supplementary TDD/PRD sections only appear when the flags are provided. Log in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.3** Compare the enriched and baseline fidelity reports by reading the backup copies at `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-fidelity-enriched-backup.md` and `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-fidelity-baseline-backup.md`. Check for: (a) "Supplementary TDD Validation" section with 5 checks -- PRESENT in enriched, ABSENT in baseline, (b) "Supplementary PRD Validation" section with 4 checks -- PRESENT in enriched, ABSENT in baseline, (c) TDD checks flagged as MEDIUM severity with actual findings referencing real task content (not "Cannot validate"), (d) first 3 PRD checks flagged as MEDIUM severity, 4th (priority ordering) flagged as LOW severity, all with actual findings. Write comparison to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-enrichment-comparison.md` with columns: Section, Enriched Report (PRESENT/ABSENT), Baseline Report (PRESENT/ABSENT), Finding Quality (REAL/EMPTY), Expected. Log in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.4** Run tasklist validate on Test 2 (spec+PRD) output to verify PRD-only enrichment with a real tasklist by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test2-spec-prd-v2/ --prd-file .dev/test-fixtures/test-prd-user-auth.md 2>&1 | tee .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-validate-spec-prd.md; echo "EXIT_CODE=$?"`. The fidelity report should contain "Supplementary PRD Validation" with 4 checks with REAL findings but NOT "Supplementary TDD Validation" (no --tdd-file). Copy fidelity report: `cp .dev/test-fixtures/results/test2-spec-prd-v2/tasklist-fidelity.md .dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-fidelity-spec-prd-backup.md`. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-validate-spec-prd-fidelity.md`. Log in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.5** Verify the `build_tasklist_generate_prompt` function directly by running `uv run python -c "from superclaude.cli.tasklist.prompts import build_tasklist_generate_prompt; from pathlib import Path; p = Path('.'); r_none = build_tasklist_generate_prompt(p); r_tdd = build_tasklist_generate_prompt(p, tdd_file=p); r_prd = build_tasklist_generate_prompt(p, prd_file=p); r_both = build_tasklist_generate_prompt(p, tdd_file=p, prd_file=p); checks = []; checks.append(('no_supplements', 'Supplementary' not in r_none)); checks.append(('tdd_only', 'TDD' in r_tdd and 'PRD' not in r_tdd)); checks.append(('prd_only', 'PRD' in r_prd and 'PRD context informs' in r_prd)); checks.append(('both', 'TDD' in r_both and 'PRD' in r_both and 'When both TDD and PRD' in r_both)); [print(f'{n}: {\"PASS\" if v else \"FAIL\"}') for n, v in checks]; print('ALL PASS' if all(v for _, v in checks) else 'SOME FAILED')"`. This tests all 4 scenarios for the generation prompt. Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-generate-prompt-verification.md`. Log in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.6** Write a Phase 8 summary by reading all `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-*.md` files. Write to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/validation-enrichment-summary.md` with: (1) Enrichment test results table, (2) Enriched vs Baseline comparison (CRITICAL: both now have REAL findings, not "no tasklist"), (3) PRD-only enrichment results, (4) Generate prompt function verification, (5) Key finding: supplementary TDD has 5 checks with REAL MEDIUM findings, supplementary PRD has 4 checks (3 MEDIUM + 1 LOW) with REAL findings, (6) Critical Findings. Once done, mark this item as complete.

---

## Phase 9: Cross-Run Comparison (7 items)

> **Purpose:** Compare Test 1 (TDD+PRD) results against prior TDD-only results to quantify PRD enrichment value. Compare Test 2 (Spec+PRD) against prior spec-only results. NEW: compare generated tasklists between TDD+PRD and Spec+PRD paths.
>
> **Handoff input:** New results at `.dev/test-fixtures/results/test1-tdd-prd-v2/` and `.dev/test-fixtures/results/test2-spec-prd-v2/`. Prior results at `.dev/test-fixtures/results/test1-tdd-modified/` and `.dev/test-fixtures/results/test2-spec-modified/` (READ-ONLY).

- [ ] **9.1** Compare Test 1 extraction: TDD+PRD (v2) vs TDD-only (prior) by reading `extraction.md` from both `.dev/test-fixtures/results/test1-tdd-prd-v2/extraction.md` and `.dev/test-fixtures/results/test1-tdd-modified/extraction.md`. Compare: (a) frontmatter field counts (both should have 19 TDD fields), (b) body section counts (both >= 14), (c) PRD-specific content in the new extraction that is absent in the old. Write side-by-side comparison to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase9-extraction-tdd-comparison.md` with columns: Dimension, TDD-Only (prior), TDD+PRD-v2 (new), Delta, Assessment. Log in the Phase 9 Findings section of the Task Log at the bottom of this task file. Once done, mark this item as complete.

- [ ] **9.2** Compare Test 1 roadmap: TDD+PRD (v2) vs TDD-only (prior) by reading `roadmap.md` from both `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md` and `.dev/test-fixtures/results/test1-tdd-modified/roadmap.md`. Compare: (a) line counts, (b) TDD identifier presence, (c) PRD-specific content in new roadmap. Quantify enrichment: count instances of PRD-specific terms in each. Write comparison to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase9-roadmap-tdd-comparison.md`. Log in the Phase 9 Findings section. Once done, mark this item as complete.

- [ ] **9.3** Compare Test 2 extraction: spec+PRD (v2) vs spec-only (prior) by reading `extraction.md` from both `.dev/test-fixtures/results/test2-spec-prd-v2/extraction.md` and `.dev/test-fixtures/results/test2-spec-modified/extraction.md`. Compare: (a) both should have exactly 13 frontmatter fields, (b) both should have exactly 8 body sections, (c) PRD-specific content in the new extraction. **CRITICAL**: Verify no TDD content leaked into either version. Write comparison to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase9-extraction-spec-comparison.md`. Log in the Phase 9 Findings section. Once done, mark this item as complete.

- [ ] **9.4** Compare Test 2 roadmap: spec+PRD (v2) vs spec-only (prior) by reading `roadmap.md` from both `.dev/test-fixtures/results/test2-spec-prd-v2/roadmap.md` and `.dev/test-fixtures/results/test2-spec-modified/roadmap.md`. Compare: (a) line counts, (b) PRD-specific content, (c) **CROSS-CONTAMINATION CHECK**: TDD component names should NOT appear. Write comparison to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase9-roadmap-spec-comparison.md`. Log in the Phase 9 Findings section. Once done, mark this item as complete.

- [ ] **9.5** Compare generated tasklists between TDD+PRD and Spec+PRD paths by reading tasklist-index.md and phase files from both `.dev/test-fixtures/results/test1-tdd-prd-v2/` and `.dev/test-fixtures/results/test2-spec-prd-v2/`. Compare: (a) phase count (TDD+PRD roadmap has 4 phases vs Spec+PRD has 2 phases + buffer, so tasklist phase counts may differ), (b) task count (TDD+PRD should have more granular technical tasks), (c) TDD content in test1 that is ABSENT in test2: count instances of `AuthService`, `TokenManager`, `UT-001`, `UserProfile` in each, (d) PRD content in BOTH: count instances of `Alex`, `Jordan`, `GDPR`, `SOC2`, `conversion` in each (should be present in both since both have PRD), (e) Spec-specific content in test2: count instances of milestone references (M1-M6), task table format (Task 1.1, Task 2.1). Write a cross-tasklist comparison to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase9-tasklist-comparison.md` with columns: Content Category, TDD+PRD Count, Spec+PRD Count, Expected Pattern, Assessment. Log in the Phase 9 Findings section. Once done, mark this item as complete.

- [ ] **9.6** Compare enriched fidelity reports between TDD+PRD and Spec+PRD by reading the backup fidelity reports at `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-fidelity-enriched-backup.md` (TDD+PRD, enriched) and `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase8-fidelity-spec-prd-backup.md` (Spec+PRD, PRD-only). Compare: (a) TDD supplementary section present in TDD+PRD, absent in Spec+PRD, (b) PRD supplementary section present in BOTH (both runs provided --prd-file), (c) deviation counts and severity distributions, (d) quality of findings now that both validate against REAL tasklists. Write comparison to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase9-fidelity-comparison.md`. Log in the Phase 9 Findings section. Once done, mark this item as complete.

- [ ] **9.7** Write a Phase 9 summary by reading all `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase9-*.md` files. Write to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/cross-run-comparison-summary.md` with: (1) TDD+PRD vs TDD-Only comparison matrix (extraction, roadmap), (2) Spec+PRD vs Spec-Only comparison matrix, (3) Cross-contamination matrix, (4) NEW: Tasklist comparison matrix (TDD+PRD tasklist vs Spec+PRD tasklist), (5) Fidelity report comparison, (6) Enrichment value assessment, (7) Critical Findings. Once done, mark this item as complete.

---

## Phase 10: Cross-Pipeline Comparison and Anti-Instinct Analysis (4 items)

> **Purpose:** Compare anti-instinct results across all four runs (TDD-only, spec-only, TDD+PRD-v2, spec+PRD-v2), compare pipeline completion status, and analyze whether PRD enrichment affects gate pass rates.
>
> **Handoff input:** Anti-instinct and state files from all four result directories.

- [ ] **10.1** Compare anti-instinct results across all four runs by reading `anti-instinct-audit.md` from: (a) `.dev/test-fixtures/results/test1-tdd-modified/anti-instinct-audit.md` (TDD-only prior), (b) `.dev/test-fixtures/results/test1-tdd-prd-v2/anti-instinct-audit.md` (TDD+PRD-v2 new), (c) `.dev/test-fixtures/results/test2-spec-modified/anti-instinct-audit.md` (spec-only prior), (d) `.dev/test-fixtures/results/test2-spec-prd-v2/anti-instinct-audit.md` (spec+PRD-v2 new). For each, extract `fingerprint_coverage`, `undischarged_obligations`, `uncovered_contracts`. Write a 4-way comparison table to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase10-anti-instinct-4way.md`. Analyze: did PRD enrichment improve or degrade anti-instinct results? Log in the Phase 10 Findings section. Once done, mark this item as complete.

- [ ] **10.2** Compare pipeline completion status across all four runs by reading `.roadmap-state.json` from all four result directories. For each run, extract the status of every pipeline step. Write a 4-way step comparison table to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase10-pipeline-4way.md` with columns: Step, TDD-Only, TDD+PRD-v2, Spec-Only, Spec+PRD-v2. Analyze: did PRD enrichment cause any new step failures or resolve any? Log in the Phase 10 Findings section. Once done, mark this item as complete.

- [ ] **10.3** Compare fidelity results between TDD+PRD-v2 and spec+PRD-v2 runs. If spec-fidelity.md exists in either new result directory, read both and compare: (a) severity counts, (b) PRD-specific dimensions 12-15 presence, (c) TDD-specific dimensions 7-11 absence (C-03 conditional). If spec-fidelity was skipped in both (anti-instinct halt), note "SKIPPED in both -- anti-instinct pre-existing blocker". Write results to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase10-fidelity-comparison.md`. Log in the Phase 10 Findings section. Once done, mark this item as complete.

- [ ] **10.4** Write a Phase 10 summary by reading all `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/test-results/phase10-*.md` files. Write to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/cross-pipeline-analysis.md` with: (1) 4-way anti-instinct comparison table, (2) 4-way pipeline step comparison table, (3) Fidelity comparison results, (4) PRD impact assessment: positive, neutral, or negative. Once done, mark this item as complete.

---

## Phase 11: Final Verification Report (3 items)

> **Purpose:** Produce the final comprehensive verification report covering all test runs, tasklist generation, cross-run comparisons, auto-wire testing, validation enrichment, and PRD enrichment assessment.
>
> **Handoff input:** All phase summaries and comparison results from Phases 3-10.

- [ ] **11.1** Compile the final verification report by reading all phase summaries in `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/` and all Phase Findings tables from the Task Log at the bottom of this task file. Create the file `.dev/test-fixtures/results/verification-report-full-pipeline.md` containing: (1) **Executive Summary** with overall PASS/FAIL verdict and 1-paragraph summary of full pipeline (roadmap + tasklist + validation) results, (2) **Test 1 Results (TDD+PRD)** pass/fail table with PRD enrichment column, (3) **Test 2 Results (Spec+PRD)** pass/fail table with TDD leak check and PRD enrichment column, (4) **Tasklist Generation Results** table: Test 1 generation (SUCCESS/FAILURE, file count, TDD enrichment, PRD enrichment), Test 2 generation (SUCCESS/FAILURE, file count, PRD enrichment, TDD leak check), (5) **Auto-Wire Test Results** from Phase 7, (6) **Validation Enrichment Results** from Phase 8 (CRITICAL: now with REAL findings), (7) **Cross-Run Comparison** from Phase 9 including tasklist comparison, (8) **Anti-Instinct 4-Way Comparison** from Phase 10, (9) **Success Criteria Checklist**: PRD flag accepted (yes/no), PRD enrichment in extraction (yes/no), PRD enrichment in roadmap (yes/no), PRD fidelity dimensions 12-15 (yes/no), state file stores prd_file/input_type (yes/no), auto-wire works (yes/no), tasklist validation enrichment with REAL findings (yes/no), no TDD leak in spec+PRD path (yes/no), no regressions from PRD (yes/no), EXTRACT_TDD_GATE used for TDD primary (yes/no), multi-file CLI works (yes/no), backward compat single-file works (yes/no), **Tasklist generated from TDD+PRD roadmap (yes/no)**, **Tasklist generated from Spec+PRD roadmap (yes/no)**, **TDD enrichment in generated TDD+PRD tasklist (yes/no)**, **PRD enrichment in generated tasklists (yes/no)**, **No TDD leak in Spec+PRD tasklist (yes/no)**, **Fidelity validation produces REAL findings with actual tasklist (yes/no)**, **Supplementary TDD has 5 checks with real MEDIUM findings (yes/no)**, **Supplementary PRD has 4 checks (3 MEDIUM, 1 LOW) with real findings (yes/no)**, (10) **Known Issues**, (11) **Findings**. If unable to compile, log in the Phase 11 Findings section. Once done, mark this item as complete.

- [ ] **11.2** Compare the new verification report against the prior verification report by reading both `.dev/test-fixtures/results/verification-report-full-pipeline.md` (new) and `.dev/test-fixtures/results/verification-report-modified-repo.md` (prior). Summarize what changed: new success criteria added (tasklist generation, tasklist validation with real findings), any criteria that regressed, any criteria that improved. Write a delta report to `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/verification-delta.md`. Once done, mark this item as complete.

- [ ] **11.3** Write consolidated follow-up action items by reading the ENTIRE Task Log at the bottom of this task file (all Phase Findings tables, Open Questions, Deferred Work). Create `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/follow-up-action-items.md` containing: (1) **Bugs Found** -- every CRITICAL/IMPORTANT finding, (2) **Known Issues Confirmed** -- pre-existing issues confirmed, (3) **PRD Enrichment Assessment**, (4) **Tasklist Generation Assessment** -- did generation produce enriched tasklists? What was missing?, (5) **Auto-Wire Assessment**, (6) **Validation Enrichment Assessment** -- did fidelity reports have REAL findings?, (7) **Deferred Work**, (8) **Recommended Next Steps**. This file must be self-contained for a future developer. Once done, mark this item as complete.

---

## Phase 12: Completion (2 items)

> **Purpose:** Final deliverable verification and task status update.

- [ ] **12.1** Verify all deliverables exist by checking the following files: `.dev/test-fixtures/results/test1-tdd-prd-v2/extraction.md` (Test 1 output), `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md` (Test 1 tasklist), `.dev/test-fixtures/results/test2-spec-prd-v2/extraction.md` (Test 2 output), `.dev/test-fixtures/results/test2-spec-prd-v2/tasklist-index.md` (Test 2 tasklist), `.dev/test-fixtures/results/verification-report-full-pipeline.md` (final report), `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/follow-up-action-items.md` (follow-up actions), `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/cross-run-comparison-summary.md` (comparison), `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/auto-wire-summary.md` (auto-wire), `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/validation-enrichment-summary.md` (enrichment), `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/test1-tasklist-generation-summary.md` (Test 1 tasklist gen), `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/test2-tasklist-generation-summary.md` (Test 2 tasklist gen). List any missing deliverables. If all present, note "All deliverables confirmed." Log any missing items in the Phase 12 Findings section. Once done, mark this item as complete.

- [ ] **12.2** Update the `status` field in this task file's YAML frontmatter from `in-progress` to `done`, set `completion_date` to today's date, and set `updated_date` to today's date. Log the total item count completed and any final notes in the Phase 12 Findings section. Once done, mark this item as complete.

---

## Task Log / Notes

### Execution Log

| Timestamp | Phase | Item | Status | Notes |
|-----------|-------|------|--------|-------|
| | | | | |

### Phase 1 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 2 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 3 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 4 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 5 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 6 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 7 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 8 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 9 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 10 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 11 Findings

| Item | Finding | Severity | Resolution |
|------|---------|----------|------------|
| | | | |

### Phase 12 Findings

_No findings yet._

### Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| AI-1 | Anti-instinct gate halts both TDD and spec pipelines (pre-existing). Will PRD enrichment improve or degrade anti-instinct pass rates? | OPEN | Investigate in Phase 10 item 10.1 with 4-way comparison. |
| TG-1 | Tasklist generation via /sc:tasklist skill -- will it handle both TDD+PRD and Spec+PRD roadmaps correctly? | OPEN | Test in Phases 5-6. |
| TG-2 | Will the skill's TDD enrichment produce component names, API endpoints, test IDs in the generated tasklist? | OPEN | Verify in Phase 5 items 5.3-5.4. |
| VE-1 | With real tasklists, will supplementary TDD/PRD fidelity checks produce REAL findings (not "Cannot validate")? | OPEN | Verify in Phase 8 items 8.1-8.3. |

### Deferred Work Items

| Item | Rationale | Dependency |
|------|-----------|------------|
| `superclaude tasklist generate` CLI command | No CLI command exists. Generation is inference-only via /sc:tasklist skill. | Future CLI implementation |
| Anti-instinct gate fix | Pre-existing issue blocking post-merge pipeline steps. Not caused by PRD changes. | Independent work item |
| CLI --input-type "prd" choice | `models.py` Literal includes "prd" but CLI `click.Choice` is `["auto", "tdd", "spec"]`. | Design decision pending |
