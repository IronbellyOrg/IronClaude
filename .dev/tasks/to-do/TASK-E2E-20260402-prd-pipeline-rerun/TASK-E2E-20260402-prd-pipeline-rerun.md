---
id: TASK-E2E-20260402-prd-pipeline-rerun
title: "E2E Pipeline Tests -- PRD Enrichment with TDD and Spec Paths"
status: to-do
completion_date: ""
priority: high
created: 2026-04-02
start_date: ""
updated_date: "2026-04-02"
last_session_note: "Reset from TASK-E2E-20260327-prd-pipeline-e2e for post-QA rerun. Update items to reflect QA fixes before executing."
type: verification
template: complex
estimated_items: 63
estimated_phases: 11
tags: ["e2e", "pipeline", "prd", "tdd", "spec", "verification", "roadmap", "auto-wire", "enrichment"]
handoff_dir: ".dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs"
---

# E2E Pipeline Tests -- PRD Enrichment with TDD and Spec Paths

## Task Overview

This task executes a comprehensive end-to-end verification of the pipeline after PRD integration is complete. It re-runs the two original pipeline tests (TDD path and spec path) with the addition of a `--prd-file` flag pointing to a new PRD fixture, then adds new test phases for auto-wire from `.roadmap-state.json`, tasklist validation enrichment, and cross-run comparison against prior results. Test 1 runs a TDD fixture + PRD fixture through `uv run superclaude roadmap run` and verifies PRD supplementary content appears in extraction, roadmap, fidelity, and test-strategy outputs alongside TDD content. Test 2 runs a spec fixture + PRD fixture through the same pipeline and verifies PRD enrichment works without introducing TDD content leaks. New phases test auto-wire (tasklist validate reads supplementary file paths from `.roadmap-state.json` without explicit CLI flags), tasklist validation enrichment (PRD supplementary validation block produces persona/metric/scenario checks), and cross-run comparison (PRD-enriched outputs vs prior TDD-only and spec-only baseline results).

All pipeline runs use `uv run superclaude` (never bare `superclaude`). Each pipeline run spawns Claude subprocesses and takes 30-60 minutes. The PRD fixture must read like a PM wrote it -- personas with names, "As a [user]..." stories, metric targets, business language throughout.

## Key Objectives

- Verify `--prd-file` flag is accepted on both `roadmap run` and `tasklist validate` CLI commands
- Verify `--tdd-file` flag is accepted on `roadmap run` CLI (wiring the previously dead field)
- Confirm PRD supplementary content appears in TDD extraction (personas, metrics, compliance alongside TDD technical content)
- Confirm PRD supplementary content appears in spec-fidelity output (dimensions 12-15: Persona Coverage, Business Metric Traceability, Compliance/Legal, Scope Boundary)
- Confirm `.roadmap-state.json` stores `tdd_file`, `prd_file`, and `input_type` fields after pipeline run
- Confirm tasklist validate auto-wires `tdd_file` and `prd_file` from `.roadmap-state.json` when CLI flags are absent
- Confirm PRD enrichment does not introduce TDD content into the spec extraction path
- Compare PRD-enriched outputs against prior TDD-only and spec-only baselines to quantify enrichment value
- Verify redundancy guard fires when `--tdd-file` is passed with a TDD primary input
- Document all results in a verification report with cross-run comparison

## Prerequisites and Dependencies

**Branch:** `feat/tdd-spec-merge` (or current working branch with all PRD pipeline integration changes merged)

**Implementation prerequisite:** Task `TASK-RF-20260327-prd-pipeline` must be COMPLETE before execution.

**CLI prerequisites (verify in Phase 1):**
- `uv run superclaude roadmap run --help` must show `--prd-file` and `--tdd-file` flags
- `uv run superclaude tasklist validate --help` must show `--prd-file` flag
- `uv run pytest tests/ -v` must pass with no failures

**Source Templates:**
- `src/superclaude/examples/tdd_template.md` -- TDD template (1274 lines, 28 sections, 30 frontmatter fields)
- `src/superclaude/examples/release-spec-template.md` -- Spec template (265 lines, 12 sections, 16 frontmatter fields)
- `src/superclaude/examples/prd_template.md` -- PRD template (28 sections, Feature PRD tier)

**Existing Fixtures (reuse as-is):**
- `.dev/test-fixtures/test-tdd-user-auth.md` -- TDD fixture (populated, 1000+ lines)
- `.dev/test-fixtures/test-spec-user-auth.md` -- Spec fixture (populated, ~313 lines)

**New Fixture (create in Phase 2):**
- `.dev/test-fixtures/test-prd-user-auth.md` -- PRD for "User Authentication Service" (250-350 lines)

**Prior Results (READ-ONLY comparison data):**
- `.dev/test-fixtures/results/test1-tdd-modified/` -- TDD-only pipeline output
- `.dev/test-fixtures/results/test2-spec-modified/` -- spec-only pipeline output
- `.dev/test-fixtures/results/verification-report-modified-repo.md` -- prior verification report

**New Output Directories:**
- `.dev/test-fixtures/results/test1-tdd-prd/` -- TDD+PRD pipeline output
- `.dev/test-fixtures/results/test2-spec-prd/` -- spec+PRD pipeline output

**Pipeline Code:**
- `src/superclaude/cli/roadmap/executor.py` -- `detect_input_type()`, `_build_steps()`, `_save_state()` (now stores tdd_file/prd_file/input_type), redundancy guard
- `src/superclaude/cli/roadmap/prompts.py` -- 6 of 10 builders accept `tdd_file` and `prd_file` params with PRD supplementary blocks (extract, extract_tdd, generate, score, spec_fidelity, test_strategy); 4 builders do not (diff, debate, merge, wiring_verification). Plus 2 tasklist builders = 8 total with PRD blocks
- `src/superclaude/cli/roadmap/commands.py` -- `--prd-file` and `--tdd-file` Click options
- `src/superclaude/cli/tasklist/commands.py` -- `--prd-file` Click option, auto-wire logic from `.roadmap-state.json`
- `src/superclaude/cli/tasklist/prompts.py` -- `build_tasklist_fidelity_prompt()` with PRD validation block (3 checks: S7, S19, S12/S22)
- `src/superclaude/cli/tasklist/executor.py` -- PRD wiring to inputs and prompt builder

**Known Issues (from prior E2E run):**
- Anti-instinct gate is the primary blocker: both TDD and spec pipelines halt here (pre-existing). PRD pipeline will likely also halt. Test items verify extraction and through-merge artifacts, with anti-instinct as an expected failure point.
- `uv run superclaude` required -- pipx binary is older version without dev changes.
- Click stderr auto-detection messages swallowed in dry-run output (display bug, detection still works).
- `detect_input_type()` threshold fixed to >= 5 with revised signal weights. PRD documents should detect as "spec" (not "tdd") unless PRD has its own detection path.

**Known Limitation -- Tasklist Generation:**
There is NO `superclaude tasklist generate` CLI command. Tasklist generation is inference-only via the `/sc:tasklist` skill. Only `superclaude tasklist validate` is testable as a CLI pipeline. The "Generation Enrichment" phase tests validation enrichment only, not generation.

**Research Files:**
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/research/01-existing-e2e-task-structure.md`
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/research/02-prd-implementation-mapping.md`
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/research/03-prd-fixture-requirements.md`
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/research/04-tasklist-generation-assessment.md`

---

## Phase 1: Preparation and CLI Verification (6 items)

> **Purpose:** Read this task, update status, create output directories, verify all new CLI flags exist (`--prd-file` on roadmap and tasklist, `--tdd-file` on roadmap), run unit tests, and confirm `make verify-sync` passes after skill layer updates.

- [ ] **1.1** Read this task file in full at `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` to understand all phases, objectives, verification criteria, and known issues. Update the `status` field in this file's YAML frontmatter from `to-do` to `in-progress` and set `start_date` to today's date. If unable to complete due to file access issues, log the specific blocker in the Phase 1 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **1.2** Create the following directory structure for test fixtures and pipeline outputs: `.dev/test-fixtures/results/test1-tdd-prd/`, `.dev/test-fixtures/results/test2-spec-prd/`. Also create the handoff directory structure: `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/` with subdirectories `discovery/`, `test-results/`, `reviews/`, and `reports/`. Skip any directories that already exist. If unable to complete due to filesystem permission issues, log the specific blocker in the Phase 1 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **1.3** Verify that the pipeline CLI supports the new flags by running `uv run superclaude roadmap run --help 2>&1` and confirming the output contains both `--prd-file` and `--tdd-file` options. Also run `uv run superclaude tasklist validate --help 2>&1` and confirm it contains both `--prd-file` and `--tdd-file`. Write a brief prereq-check result to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase1-prereq-check.md` containing the relevant help output snippets and PASS/FAIL for each flag. If any required flag is missing, this is a CRITICAL blocker -- the PRD pipeline implementation task is not complete. Log the specific failure in the Phase 1 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **1.4** Run the full unit test suite by executing `uv run pytest tests/ -v 2>&1 | tail -30` to confirm no regressions were introduced by the PRD pipeline implementation. Write the test summary (last 30 lines showing pass/fail counts) to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase1-unit-tests.md`. If any tests fail, log the specific failures in the Phase 1 Findings section of the Task Log at the bottom of this task file. Failing unit tests are a CRITICAL blocker for E2E testing. Once done, mark this item as complete.

- [ ] **1.5** Verify skill layer sync by running `make verify-sync 2>&1` and confirming the output indicates `src/superclaude/` and `.claude/` are in sync. This confirms that Phase 7 of the implementation task (skill/reference layer updates) was properly synced. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase1-sync-check.md`. If out of sync, run `make sync-dev` first and re-verify. Log any issues in the Phase 1 Findings section. Once done, mark this item as complete.

- [ ] **1.6** Verify the existing TDD and spec fixtures are still present and unchanged by running `wc -l .dev/test-fixtures/test-tdd-user-auth.md .dev/test-fixtures/test-spec-user-auth.md` and confirming both files exist with reasonable line counts (TDD >= 500, spec >= 200). Also verify the PRD template exists at `src/superclaude/examples/prd_template.md`. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase1-fixture-check.md`. If any fixture or template is missing, log in the Phase 1 Findings section. Once done, mark this item as complete.

---

## Phase 2: Create PRD Test Fixture (3 items)

> **Purpose:** Create a PRD fixture for "User Authentication Service" that serves as the product-level precursor to the existing TDD and spec fixtures. The PRD must read like a PM wrote it (personas with names, "As a..." stories, business metrics), use PRD-appropriate frontmatter (`type: "Product Requirements"`, not TDD), and NOT trigger TDD auto-detection. The existing TDD and spec fixtures are reused as-is from the prior E2E run.
>
> **Source template:** `src/superclaude/examples/prd_template.md` (PRD template, 28 sections, Feature PRD tier)
> **Fixture requirements:** `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/research/03-prd-fixture-requirements.md`

- [ ] **2.1** Read the PRD template at `src/superclaude/examples/prd_template.md` in full to understand its 28 sections, YAML frontmatter structure, and Feature PRD scoping rules. Also read the fixture requirements research at `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/research/03-prd-fixture-requirements.md` for exact content specifications. Then create the file `.dev/test-fixtures/test-prd-user-auth.md` by copying the PRD template structure and populating it for "User Authentication Service" with the following requirements. **Frontmatter**: set `id: "AUTH-PRD-001"`, `title: "User Authentication Service - Product Requirements Document (PRD)"`, `description: "Product requirements, user personas, success metrics, and acceptance criteria for the User Authentication Service"`, `version: "1.0"`, `status: "Draft"`, `type: "Product Requirements"` (CRITICAL: NOT "Technical Design Document"), `priority: "Highest"`, `created_date: "2026-03-26"`, `updated_date: "2026-03-26"`, `assigned_to: "product-team"` (NOT "auth-team"), `autogen: false`, `coordinator: "product-manager"` (NOT "test-lead"), `parent_task: ""`, `depends_on: []`, `related_docs: ["SEC-POLICY-001"]`, `tags: [prd, requirements, authentication, user-stories, acceptance-criteria]`. NO `parent_doc` field (that is TDD-specific). NO `approvers` block with engineering roles. **Document Header**: Include WHAT/WHY/HOW callout in product language, Document Lifecycle Position table (this PRD = Requirements phase, TDD = Design phase), Product Type = "Feature PRD". **Section S1 (Executive Summary)**: 2-3 paragraphs product summary with 4 key success metrics (registration conversion > 60%, login p95 < 200ms, session duration > 30min, failed login rate < 5%). **Section S2 (Problem Statement)**: Business problem (no accounts, no personalization, security audit failures), "Why This Feature is Required" subsection. **Section S3 (Background & Strategic Fit)**: Q2 personalization dependency, Q3 compliance deadline, 40% engagement lift projection. **Section S4 (Product Vision)**: North star statement about secure frictionless identity. **Section S5 (Business Context)**: Business justification without market sizing. **Section S6 (Jobs To Be Done)**: 3-4 JTBD in "When I... I want... so I can..." format for account creation, quick login, password recovery, profile management. **Section S7 (User Personas)**: 3 named personas: (1) "Alex the End User" -- quick registration, fast login, frustrated by re-login; (2) "Jordan the Platform Admin" -- audit logs, account management, compliance; (3) "Sam the API Consumer" -- programmatic tokens, stable contracts. Each with Role, Goals, Pain Points, JTBD. **Sections S8-S9**: Mark N/A (Feature PRD rules). **Section S10 (Assumptions & Constraints)**: Email infra exists, PostgreSQL available, no social login v1.0. **Section S11 (Dependencies)**: SendGrid, PostgreSQL 15+, frontend routing. **Section S12 (Scope Definition)**: IN = registration, login, logout, token refresh, profile, password reset. OUT = OAuth/OIDC, MFA, RBAC, social login. Rationale for each exclusion. **Section S13 (Open Questions)**: Reset sync vs async? Max refresh tokens? Lockout policy? **Section S14 (Technical Requirements)**: FRs FR-AUTH.1 through FR-AUTH.5 in product language (dot notation matching spec fixture): login with session, create account, session persistence, profile management, password reset. NFRs NFR-AUTH.1 through NFR-AUTH.3 in user-perceived quality language. **Section S15 (Technology Stack)**: Abbreviated, reference TDD. **Section S16 (User Experience Requirements)**: Feature-specific user flows only: signup flow, login flow, password reset flow. **Section S17 (Legal & Compliance)**: GDPR consent at registration, SOC2 audit logging, password storage compliance. **Section S18**: Mark N/A (Feature PRD rules). **Section S19 (Success Metrics)**: 5 metrics with targets: registration conversion > 60%, login p95 < 200ms, session duration > 30min, failed login < 5%, password reset completion > 80%. Each with measurement method and business rationale. **Section S20 (Risk Analysis)**: 3 business risks. **Section S21 (Implementation Plan)**: 3 epics (AUTH-E1 Login/Registration, AUTH-E2 Token Management, AUTH-E3 Profile & Reset); user stories in "As a [persona], I want [action], so that [outcome]" format with acceptance criteria; phasing (Phase 1: core auth, Phase 2: reset + profile). **Section S22 (Customer Journey Map)**: 4 step-by-step journeys: Signup (5 steps), Login (5 steps), Password Reset (5 steps), Profile Management (3 steps). **Section S23 (Error Handling & Edge Cases)**: 6+ edge cases: expired sessions, duplicate email registration, brute force lockout, unregistered email reset, expired reset token, concurrent multi-device login. **Sections S24-S25**: Abbreviated (no mockups, reference TDD for API specs). **Sections S26-S28**: Brief completeness sections. **CRITICAL LANGUAGE RULE**: The document must read like a PM wrote it. Use "Users can log in" NOT "AuthService authenticates via PasswordHasher". Use "Sessions persist across page refreshes" NOT "TokenManager issues JWT via JwtService". Component names (`AuthService`, `TokenManager`) should appear ONLY in a brief Technical Context subsection within S14, not throughout the document. **CRITICAL ANTI-TDD-DETECTION**: No `type: "Technical Design Document"`, no `parent_doc` field, no engineering-role approvers block, no `coordinator: "test-lead"`, no architecture diagrams, no TypeScript interfaces, no database schemas. If unable to complete due to template access issues or unclear section structure, log the specific blocker in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.2** Verify the PRD fixture by running the following sentinel checks on `.dev/test-fixtures/test-prd-user-auth.md`: (a) `grep -c 'type: "Product Requirements"' .dev/test-fixtures/test-prd-user-auth.md` (must return 1), (b) `grep -c 'Technical Design Document' .dev/test-fixtures/test-prd-user-auth.md` (must return 0 -- no TDD type), (c) `grep -c 'parent_doc:' .dev/test-fixtures/test-prd-user-auth.md` (must return 0 -- no TDD parent_doc field), (d) `grep -c 'coordinator: "product-manager"' .dev/test-fixtures/test-prd-user-auth.md` (must return 1), (e) `grep -c 'Alex the End User' .dev/test-fixtures/test-prd-user-auth.md` (must be > 0 -- persona present), (f) `grep -c 'Jordan the Platform Admin' .dev/test-fixtures/test-prd-user-auth.md` (must be > 0), (g) `grep -c 'Sam the API Consumer' .dev/test-fixtures/test-prd-user-auth.md` (must be > 0), (h) `grep -c 'FR-AUTH' .dev/test-fixtures/test-prd-user-auth.md` (must be > 0), (i) `grep -c '> 60%' .dev/test-fixtures/test-prd-user-auth.md` or similar to verify specific metric targets exist. Write sentinel check results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase2-prd-sentinel-check.md`. If any sentinel fails, the fixture must be corrected before proceeding. Log specific failures in the Phase 2 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **2.3** Verify the PRD fixture does NOT trigger TDD auto-detection by running `uv run superclaude roadmap run .dev/test-fixtures/test-prd-user-auth.md --dry-run 2>&1` and confirming the output does NOT contain "Auto-detected input type: tdd". The PRD should be detected as "spec" (it is a non-TDD document). Write the dry-run output and detection result to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase2-prd-detection-check.md`. If the PRD triggers TDD detection, the fixture has too many TDD-like signals and must be revised -- log in the Phase 2 Findings section. Note: the Click stderr auto-detection message may be swallowed in dry-run (known display bug) -- if so, check the step plan for TDD-specific warnings instead. Once done, mark this item as complete.

---

## Phase 3: Dry-Run Verification with PRD Flag (5 items)

> **Purpose:** Run fixtures through `uv run superclaude roadmap run --dry-run` with the new `--prd-file` flag to verify flag acceptance, step plan generation, and combined flag behavior BEFORE committing to full pipeline runs. Also test the redundancy guard (`--tdd-file` with TDD primary input).

- [ ] **3.1** Run the TDD fixture with PRD through dry-run by executing `uv run superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --dry-run 2>&1` and capture the full output. Verify: (a) the command accepts the `--prd-file` flag without error, (b) the step plan is complete (all pipeline steps listed), (c) no Python traceback appears, (d) auto-detection identifies the primary input as "tdd" (the PRD is supplementary, not the primary input). Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase3-tdd-prd-dryrun.md`. If `--prd-file` is not recognized, this is a CRITICAL blocker -- the implementation is incomplete. Log in the Phase 3 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **3.2** Run the spec fixture with PRD through dry-run by executing `uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --dry-run 2>&1` and capture the full output. Verify: (a) the command accepts the `--prd-file` flag, (b) the step plan is complete, (c) no Python traceback, (d) auto-detection identifies primary input as "spec". Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase3-spec-prd-dryrun.md`. If any check fails, log in the Phase 3 Findings section. Once done, mark this item as complete.

- [ ] **3.3** Test the `--tdd-file` flag on roadmap run by executing `uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --tdd-file .dev/test-fixtures/test-tdd-user-auth.md --dry-run 2>&1` and verify the command accepts the flag without error. This tests the previously-dead `tdd_file` field is now wired. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase3-tdd-flag-dryrun.md`. Log any issues in the Phase 3 Findings section. Once done, mark this item as complete.

- [ ] **3.4** Test the redundancy guard by executing `uv run superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --tdd-file .dev/test-fixtures/test-tdd-user-auth.md --dry-run 2>&1` and verify that the output contains the warning message `"Ignoring --tdd-file: primary input is already a TDD document"` or similar redundancy guard text. This fires when `input_type == "tdd"` and `--tdd-file` is also provided. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase3-redundancy-guard.md`. If the warning does not appear, the redundancy guard may not be implemented yet -- log as IMPORTANT in the Phase 3 Findings section. Note: the warning may be emitted to stderr which could be swallowed in dry-run (known display bug). Once done, mark this item as complete.

- [ ] **3.5** Review all Phase 3 results by reading the output files in `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase3-*.md` and determine whether all flags are working and fixtures are ready for full pipeline runs. Document the go/no-go decision in `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase3-go-nogo.md`. If no-go, subsequent phases cannot proceed until blockers are resolved. Log in the Phase 3 Findings section of the Task Log at the bottom of this task file. If go, note that full pipeline runs will take 30-60 minutes each. Once done, mark this item as complete.

---

## Phase 4: Test 1 -- Full TDD+PRD Pipeline Run (14 items)

> **Purpose:** Execute the full `uv run superclaude roadmap run` pipeline with the TDD fixture as primary input and PRD fixture as supplementary input (`--prd-file`). Verify every output artifact for both existing TDD behavior AND new PRD enrichment. This is the primary test proving PRD supplementary enrichment works alongside TDD extraction.
>
> **Handoff input:** TDD fixture at `.dev/test-fixtures/test-tdd-user-auth.md`, PRD fixture at `.dev/test-fixtures/test-prd-user-auth.md`

- [ ] **4.1** Run the full TDD+PRD pipeline by executing `set -o pipefail && uv run superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --output .dev/test-fixtures/results/test1-tdd-prd/ 2>&1 | tee .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-tdd-prd-pipeline-log.md; echo "EXIT_CODE=$?"`. This command runs all pipeline steps (extract, generate x2, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification) and writes all output artifacts to `.dev/test-fixtures/results/test1-tdd-prd/`. **IMPORTANT**: The pipeline takes 30-60 minutes. You MUST set a timeout of at least 3600000ms (60 minutes). The `set -o pipefail` ensures the exit code reflects the pipeline's exit code. Check the echoed EXIT_CODE: 0 means all gates passed, 1 means a gate failure halted the pipeline. Expected: anti-instinct gate will likely halt the pipeline (pre-existing issue from prior E2E run -- undischarged_obligations and uncovered_contracts). Steps through merge should PASS. If the pipeline fails at any step BEFORE merge, log the failing step in the Phase 4 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **4.2** Verify the TDD+PRD extraction output frontmatter by reading `extraction.md` at `.dev/test-fixtures/results/test1-tdd-prd/extraction.md`. Check that the YAML frontmatter contains all 13 standard fields (`spec_source`, `generated`, `generator`, `functional_requirements`, `nonfunctional_requirements`, `total_requirements`, `complexity_score`, `complexity_class`, `domains_detected`, `risks_identified`, `dependencies_identified`, `success_criteria_count`, `extraction_mode`) plus all 6 TDD-specific fields (`data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`). Verify `data_models_identified` > 0 and `api_surfaces_identified` > 0. Write field-by-field results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-extraction-frontmatter.md`. Log any failures in the Phase 4 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **4.3** Verify the TDD+PRD extraction body sections by reading `extraction.md` at `.dev/test-fixtures/results/test1-tdd-prd/extraction.md`. Verify all 14 body sections are present (8 standard + 6 TDD-specific). Run `grep -c '## ' .dev/test-fixtures/results/test1-tdd-prd/extraction.md` and verify count >= 14. **PRD ENRICHMENT CHECK**: Search the extraction body for PRD supplementary content. The `build_extract_prompt_tdd()` with `prd_file` should include a "Supplementary PRD Context" section with persona references (Alex, Jordan, Sam), business metrics (registration conversion, login latency, session duration), and compliance items (GDPR, SOC2). Search for: `grep -c 'persona\|Persona\|Alex\|Jordan\|Sam' .dev/test-fixtures/results/test1-tdd-prd/extraction.md` (should be > 0 if PRD enrichment flowed through), `grep -c 'GDPR\|SOC2\|compliance' .dev/test-fixtures/results/test1-tdd-prd/extraction.md` (should be > 0). Note: these PRD terms appearing in extraction confirms the PRD supplementary block in the extract prompt influenced the LLM output. If PRD terms are absent, the PRD supplementary content may not have reached the extraction step. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-extraction-sections.md`. Log findings in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.4** Verify the two roadmap variant files by checking that `roadmap-opus-architect.md` and `roadmap-haiku-architect.md` (or files matching `roadmap-*.md` excluding `roadmap.md`) exist in `.dev/test-fixtures/results/test1-tdd-prd/`. For each, verify: at least 100 lines, YAML frontmatter with `spec_source`/`complexity_score`/`primary_persona`, and at least 2 of the 9 TDD backticked identifiers (`UserProfile`, `AuthToken`, `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `LoginPage`, `RegisterPage`, `AuthProvider`). **PRD ENRICHMENT CHECK**: Search each variant for PRD-influenced content: business value ordering (phases ordered by business impact, not just technical dependency), persona references in milestones. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-roadmap-variants.md`. Log findings in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.5a** Verify the diff analysis artifact by reading `diff-analysis.md` at `.dev/test-fixtures/results/test1-tdd-prd/diff-analysis.md`. Check that the file exists, has at least 30 lines, and its YAML frontmatter contains `total_diff_points` and `shared_assumptions_count`. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-diff-analysis.md`. If missing, log in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.5b** Verify the debate transcript artifact by reading `debate-transcript.md` at `.dev/test-fixtures/results/test1-tdd-prd/debate-transcript.md`. Check that the file exists, has at least 50 lines, and its YAML frontmatter contains `convergence_score` and `rounds_completed`. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-debate-transcript.md`. If missing, log in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.5c** Verify the base selection artifact by reading `base-selection.md` at `.dev/test-fixtures/results/test1-tdd-prd/base-selection.md`. Check that the file exists, has at least 20 lines, and its YAML frontmatter contains `base_variant` and `variant_scores`. **PRD ENRICHMENT CHECK**: The `build_score_prompt` includes 3 PRD scoring dimensions (business value alignment, persona coverage, compliance readiness). Search for: `grep -c 'business value\|Business Value\|persona\|Persona\|compliance\|Compliance' .dev/test-fixtures/results/test1-tdd-prd/base-selection.md` (should be > 0 if PRD enrichment influenced scoring). Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-base-selection.md`. If missing, log in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.6** Verify the merged roadmap by reading `roadmap.md` at `.dev/test-fixtures/results/test1-tdd-prd/roadmap.md`. Check at least 150 lines, YAML frontmatter with `spec_source`, `complexity_score`, `adversarial: true`. Search for at least 3 of the 9 TDD backticked identifiers. **PRD ENRICHMENT CHECK**: Search for PRD business value indicators: `grep -c 'business value\|Business Value\|persona\|Persona\|compliance\|GDPR\|SOC2\|registration.*rate\|session.*duration' .dev/test-fixtures/results/test1-tdd-prd/roadmap.md` and note whether PRD enrichment influenced roadmap content (presence of business rationale, persona references, compliance milestones). Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-merged-roadmap.md`. Log findings in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.7** Verify the anti-instinct audit by reading `anti-instinct-audit.md` at `.dev/test-fixtures/results/test1-tdd-prd/anti-instinct-audit.md`. Check that `fingerprint_coverage` >= 0.7, and note `undischarged_obligations` and `uncovered_contracts` values. Expected: anti-instinct will likely fail (pre-existing issue -- same as prior TDD-only run where undischarged_obligations=5, uncovered_contracts=4, fingerprint_coverage=0.76). Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-anti-instinct.md`. Log findings in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.8** Verify the test strategy output (if produced -- may be skipped due to anti-instinct halt) by checking if `test-strategy.md` exists at `.dev/test-fixtures/results/test1-tdd-prd/test-strategy.md`. If it exists, check frontmatter for `complexity_class`, `validation_philosophy`, `interleave_ratio`, `major_issue_policy`. **PRD ENRICHMENT CHECK**: Search for PRD-specific test strategy items: persona-based acceptance testing, customer journey E2E tests, KPI validation tests, compliance test category, edge case coverage from PRD S23. If the file does not exist (expected if anti-instinct halted the pipeline), note "SKIPPED -- anti-instinct halt" and do not treat as a failure. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-test-strategy.md`. Log findings in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.9** Verify the spec-fidelity output (if produced -- may be skipped due to anti-instinct halt) by checking if `spec-fidelity.md` exists at `.dev/test-fixtures/results/test1-tdd-prd/spec-fidelity.md`. If it exists, check `high_severity_count`, `validation_complete`, `tasklist_ready`, and "source-document fidelity analyst" language. **PRD ENRICHMENT CHECK**: Search for PRD-specific fidelity dimensions 12-15: Persona Coverage (S7), Business Metric Traceability (S19), Compliance/Legal (S17, HIGH severity), Scope Boundary (S12). These dimensions should ONLY appear when `--prd-file` was provided. Search for `grep -c 'Persona Coverage\|Business Metric\|Compliance.*Legal\|Scope Boundary' .dev/test-fixtures/results/test1-tdd-prd/spec-fidelity.md`. If the file does not exist (expected if anti-instinct halted), note "SKIPPED" and do not treat as failure. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-spec-fidelity.md`. Log findings in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.9a** Verify the wiring-verification output by reading `wiring-verification.md` at `.dev/test-fixtures/results/test1-tdd-prd/wiring-verification.md`. Check it exists, has at least 10 lines, and frontmatter contains `analysis_complete: true` and `blocking_findings: 0`. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-wiring-verification.md`. Log failures in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.9b** Verify the pipeline state file by reading `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json`. Check it contains: `schema_version` (should be 1), `spec_file` (path to TDD fixture), `spec_hash` (non-empty), `agents` (array >= 2), `steps` object. **NEW PRD FIELDS CHECK**: Verify the state file now contains: `tdd_file` (should be null -- TDD is the primary input, not a supplementary file), `prd_file` (should be the absolute path to `.dev/test-fixtures/test-prd-user-auth.md`), `input_type` (should be "tdd"). These 3 new fields are added by the PRD pipeline implementation. If any are missing, the `_save_state()` changes from Phase 8 of the implementation task are incomplete. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-state-file.md`. Log findings in the Phase 4 Findings section. Once done, mark this item as complete.

- [ ] **4.10** Write a Phase 4 summary by reading all phase-outputs files matching `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase4-*.md` and compiling a pass/fail table for each artifact check. Write the summary to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/test1-tdd-prd-summary.md` with: (1) a pass/fail table with columns: Artifact, Gate, Check, Result (PASS/FAIL), Notes, (2) a separate "PRD Enrichment Results" table with columns: Artifact, PRD Content Expected, PRD Content Found, Assessment (ENRICHED/NOT-ENRICHED/SKIPPED), (3) count of total checks passed vs failed, (4) "Critical Findings" from Phase 4 Findings table, (5) "Follow-Up Actions" for each failure. This summary must contain enough detail for a future executor to understand what passed, what failed, and what PRD enrichment was observed. Log in the Phase 4 Findings section if unable to compile. Once done, mark this item as complete.

---

## Phase 5: Test 2 -- Full Spec+PRD Pipeline Run (9 items)

> **Purpose:** Execute the full `uv run superclaude roadmap run` pipeline with the spec fixture as primary input and PRD fixture as supplementary input. Verify key output artifacts for existing spec behavior (no TDD leaks) AND new PRD enrichment. This test proves PRD enrichment works for the spec path without introducing TDD content contamination.
>
> **Scope note:** Phase 5 focuses on extraction, merged roadmap, anti-instinct, spec-fidelity, and state file verification. Intermediate artifacts (roadmap variants, diff-analysis, debate-transcript, base-selection, wiring-verification) are verified thoroughly in Phase 4 for the TDD+PRD path and are not re-checked here. If the executor suspects PRD enrichment causes regressions in intermediate artifacts for the spec path, these should be spot-checked and logged in Phase 5 Findings.
>
> **Handoff input:** Spec fixture at `.dev/test-fixtures/test-spec-user-auth.md`, PRD fixture at `.dev/test-fixtures/test-prd-user-auth.md`

- [ ] **5.1** Run the full spec+PRD pipeline by executing `set -o pipefail && uv run superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md --output .dev/test-fixtures/results/test2-spec-prd/ 2>&1 | tee .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-spec-prd-pipeline-log.md; echo "EXIT_CODE=$?"`. This runs the standard spec extraction path with PRD supplementary enrichment. **IMPORTANT**: 30-60 minute timeout required (3600000ms). Expected: anti-instinct will likely halt the pipeline (pre-existing). Steps through merge should PASS. If the pipeline fails BEFORE merge, log in the Phase 5 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **5.2** Verify the spec+PRD extraction frontmatter by reading `extraction.md` at `.dev/test-fixtures/results/test2-spec-prd/extraction.md`. Check that the YAML frontmatter contains ONLY the 13 standard fields and does NOT contain any of the 6 TDD-specific fields (`data_models_identified`, `api_surfaces_identified`, `components_identified`, `test_artifacts_identified`, `migration_items_identified`, `operational_items_identified`). **CRITICAL**: TDD fields must be ABSENT -- the spec+PRD path must not introduce TDD content. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-extraction-frontmatter.md`. If any TDD field is present, add a CRITICAL finding to the Phase 5 Findings section -- PRD enrichment is causing TDD content leak. Once done, mark this item as complete.

- [ ] **5.3** Verify the spec+PRD extraction body sections by reading `extraction.md` at `.dev/test-fixtures/results/test2-spec-prd/extraction.md`. Verify ONLY the 8 standard sections are present. Search for the 6 TDD-specific sections ("Data Models and Interfaces", "API Specifications", "Component Inventory", "Testing Strategy", "Migration and Rollout Plan", "Operational Readiness") -- all must be ABSENT. **PRD ENRICHMENT CHECK**: Search for PRD supplementary content in the extraction: `grep -c 'persona\|Persona\|Alex\|Jordan\|Sam' .dev/test-fixtures/results/test2-spec-prd/extraction.md`, `grep -c 'GDPR\|SOC2\|compliance' .dev/test-fixtures/results/test2-spec-prd/extraction.md`. PRD content (persona references, compliance items) may appear alongside standard spec extraction -- this is expected and desirable. TDD content (data models, API specs, component inventory) must NOT appear. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-extraction-sections.md`. Log findings in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.4** Verify the spec+PRD merged roadmap by reading `roadmap.md` at `.dev/test-fixtures/results/test2-spec-prd/roadmap.md`. Check at least 150 lines, YAML frontmatter with `spec_source`, `complexity_score`, `adversarial: true`. **PRD ENRICHMENT CHECK**: Search for business value content, persona references, and compliance milestones (same grep patterns as Phase 4 item 4.6). **TDD LEAK CHECK**: Search for TDD-specific identifiers (`AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `LoginPage`, `RegisterPage`, `AuthProvider`) -- these should be ABSENT or minimal in the spec+PRD path. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-merged-roadmap.md`. Log findings in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.5** Verify the spec+PRD anti-instinct audit by reading `anti-instinct-audit.md` at `.dev/test-fixtures/results/test2-spec-prd/anti-instinct-audit.md`. Check `fingerprint_coverage` >= 0.7, note `undischarged_obligations` and `uncovered_contracts`. Expected: same pre-existing failure pattern as prior spec-only run (uncovered_contracts=3). Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-anti-instinct.md`. Log findings in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.6** Verify the spec+PRD spec-fidelity output (if produced -- may be skipped due to anti-instinct halt) by checking if `spec-fidelity.md` exists at `.dev/test-fixtures/results/test2-spec-prd/spec-fidelity.md`. If it exists, check `high_severity_count` is 0, `validation_complete` is true, uses "source-document fidelity analyst" language. **PRD ENRICHMENT CHECK**: Search for dimensions 12-15 (Persona Coverage, Business Metric Traceability, Compliance/Legal, Scope Boundary). **TDD LEAK CHECK**: The TDD-specific dimensions (API Endpoints, Component Inventory, Testing Strategy, Migration & Rollout, Operational Readiness) should be absent or empty for a spec+PRD run. If the file does not exist, note "SKIPPED". Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-spec-fidelity.md`. Log findings in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.7** Verify the spec+PRD state file by reading `.dev/test-fixtures/results/test2-spec-prd/.roadmap-state.json`. Check for standard fields plus the 3 new fields: `tdd_file` (should be null -- no --tdd-file was passed), `prd_file` (should be the absolute path to the PRD fixture), `input_type` (should be "spec"). Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-state-file.md`. Log findings in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.8** Verify all gates passed for the spec+PRD pipeline by reading the pipeline log at `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-spec-prd-pipeline-log.md` and the `.roadmap-state.json` step-by-step status. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-pipeline-status.md` with step-by-step table. Log any unexpected failures in the Phase 5 Findings section. Once done, mark this item as complete.

- [ ] **5.9** Write a Phase 5 summary by reading all `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase5-*.md` files and compiling a pass/fail table. Write to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/test2-spec-prd-summary.md` with: (1) pass/fail table, (2) "PRD Enrichment Results" table, (3) "TDD Leak Check" table confirming zero TDD content in spec+PRD path, (4) key success criteria: no TDD leaks, standard 8 sections only, PRD enrichment observed, (5) Critical Findings from Phase 5 Findings table, (6) Follow-Up Actions. Once done, mark this item as complete.

---

## Phase 6: Auto-Wire from .roadmap-state.json (6 items)

> **Purpose:** Test that `uv run superclaude tasklist validate` can auto-wire `tdd_file` and `prd_file` from the `.roadmap-state.json` saved by the roadmap pipeline, without requiring explicit `--tdd-file` or `--prd-file` CLI flags. Also test explicit flag precedence and graceful degradation.
>
> **Handoff input:** Test 1 output at `.dev/test-fixtures/results/test1-tdd-prd/` (contains `.roadmap-state.json` with `prd_file` and `input_type` fields)

- [ ] **6.1** Run tasklist validate on Test 1 output WITHOUT explicit supplementary file flags by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd/ 2>&1 | tee .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-autowire-basic.md; echo "EXIT_CODE=$?"`. Check the output for auto-wire info messages: (a) `grep -c 'Auto-wired.*prd' .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-autowire-basic.md` -- should find the `[tasklist validate] Auto-wired --prd-file from .roadmap-state.json` message, (b) check if `tdd_file` was auto-wired (depends on whether the state file stored it for TDD primary input). The tasklist validation should proceed with the auto-wired supplementary files and produce a fidelity report. If auto-wire messages are absent, the auto-wire logic from Phase 8 of the implementation task is not implemented. Log findings in the Phase 6 Findings section of the Task Log at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

- [ ] **6.2** Verify auto-wired tasklist fidelity output includes PRD supplementary validation by reading the tasklist fidelity report produced by item 6.1. The report should be in `.dev/test-fixtures/results/test1-tdd-prd/` (the output directory). Check for: (a) "Supplementary PRD Validation" section in the fidelity report, (b) 3 PRD validation checks: persona coverage (S7), success metrics (S19), acceptance scenarios (S12/S22), (c) all PRD checks flagged as MEDIUM severity. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-autowire-fidelity.md`. Log findings in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.3** Test explicit flag precedence over auto-wire by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd/ --prd-file .dev/test-fixtures/test-spec-user-auth.md 2>&1 | head -20` (deliberately passing the SPEC fixture as `--prd-file` to test that the explicit flag overrides the auto-wired PRD path). Verify: (a) no auto-wire info message for `prd_file` (explicit flag takes precedence), (b) the command does not error. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-autowire-precedence.md`. Log findings in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.4** Test graceful degradation when auto-wired file path does not exist on disk. First, create a modified `.roadmap-state.json` for this test: read `.dev/test-fixtures/results/test1-tdd-prd/.roadmap-state.json`, copy it to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-state-modified.json` with the `prd_file` value changed to a non-existent path (e.g., `/tmp/nonexistent-prd.md`). Then create a temporary test directory at `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-degradation-test/`, copy the modified state file there as `.roadmap-state.json`, copy the Test 1 roadmap.md there, and run `uv run superclaude tasklist validate .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-degradation-test/ 2>&1 | head -20`. Verify: (a) a warning is emitted about the missing file, (b) the command does not crash, (c) the field is left as None (validation proceeds without PRD enrichment). Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-autowire-degradation.md`. Log findings in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.5** Test auto-wire with no `.roadmap-state.json` present. Run `uv run superclaude tasklist validate .dev/test-fixtures/ 2>&1 | head -20` (a directory that has no state file). Verify: (a) no auto-wire messages, (b) no error or crash, (c) the command either proceeds normally (with no supplementary files) or fails gracefully because no roadmap.md is found in that directory. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-autowire-no-state.md`. Log findings in the Phase 6 Findings section. Once done, mark this item as complete.

- [ ] **6.6** Write a Phase 6 summary by reading all `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase6-*.md` files. Write to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/auto-wire-summary.md` with: (1) Auto-wire test results table (Scenario, Expected Behavior, Actual Behavior, PASS/FAIL), (2) PRD fidelity enrichment validation results, (3) Critical Findings from Phase 6 Findings, (4) Overall auto-wire assessment. Once done, mark this item as complete.

---

## Phase 7: Tasklist Validation Enrichment Testing (6 items)

> **Purpose:** Test that `uv run superclaude tasklist validate` produces enriched fidelity reports when supplementary TDD and PRD files are provided via explicit CLI flags. Compare enriched validation against baseline (no supplementary files) to quantify the value added by PRD enrichment.
>
> **KNOWN LIMITATION**: There is NO `superclaude tasklist generate` CLI command. Tasklist generation is inference-only via the `/sc:tasklist` skill. This phase tests validation enrichment only.
>
> **Handoff input:** Test 1 output at `.dev/test-fixtures/results/test1-tdd-prd/` (roadmap + state file)

- [ ] **7.1** Run tasklist validate with explicit TDD+PRD flags on Test 1 output by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd/ --tdd-file .dev/test-fixtures/test-tdd-user-auth.md --prd-file .dev/test-fixtures/test-prd-user-auth.md 2>&1 | tee .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase7-validate-enriched.md; echo "EXIT_CODE=$?"`. This exercises the full enrichment path: both TDD and PRD supplementary validation blocks should appear in the fidelity report. If the command fails, log in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.2** Run tasklist validate WITHOUT any supplementary flags (baseline) on the same output by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test1-tdd-prd/ --tdd-file /dev/null --prd-file /dev/null 2>&1 | tee .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase7-validate-baseline.md; echo "EXIT_CODE=$?"` OR if /dev/null triggers Click validation error (exists=True check), run the baseline by temporarily using a minimal dummy file. The goal is to compare output with vs without supplementary enrichment. Note: if baseline run is not feasible due to Click path validation, skip this item and log the limitation. If the auto-wire from Phase 6 interferes (auto-wiring from state), explicitly override with dummy paths. Log in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.3** Compare the enriched and baseline tasklist fidelity reports. Read the fidelity outputs from items 7.1 and 7.2. Check for the presence/absence of: (a) "Supplementary TDD Validation" section with 3 checks (test cases from TDD S15, rollback from TDD S19, components from TDD S10), (b) "Supplementary PRD Validation" section with 3 checks (persona coverage S7, success metrics S19, acceptance scenarios S12/S22), (c) all supplementary checks flagged as MEDIUM severity. In the enriched report, both sections should be present. In the baseline report, neither should appear. Write comparison to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase7-enrichment-comparison.md` with columns: Section, Enriched Report (PRESENT/ABSENT), Baseline Report (PRESENT/ABSENT), Expected. Log findings in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.4** Run tasklist validate on Test 2 (spec+PRD) output to verify PRD-only enrichment by executing `uv run superclaude tasklist validate .dev/test-fixtures/results/test2-spec-prd/ --prd-file .dev/test-fixtures/test-prd-user-auth.md 2>&1 | tee .dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase7-validate-spec-prd.md; echo "EXIT_CODE=$?"`. The fidelity report should contain the "Supplementary PRD Validation" section but NOT the "Supplementary TDD Validation" section (since no `--tdd-file` was provided). This confirms PRD-only enrichment works independently. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase7-validate-spec-prd-fidelity.md`. Log findings in the Phase 7 Findings section. Once done, mark this item as complete.

- [ ] **7.5** Verify the `build_tasklist_generate_prompt` function directly (no CLI command exists, but the function was implemented). Run `uv run python -c "from superclaude.cli.tasklist.prompts import build_tasklist_generate_prompt; from pathlib import Path; p = Path('.'); r_none = build_tasklist_generate_prompt(p); r_tdd = build_tasklist_generate_prompt(p, tdd_file=p); r_prd = build_tasklist_generate_prompt(p, prd_file=p); r_both = build_tasklist_generate_prompt(p, tdd_file=p, prd_file=p); checks = []; checks.append(('no_supplements', 'Supplementary' not in r_none)); checks.append(('tdd_only', 'TDD' in r_tdd and 'PRD' not in r_tdd)); checks.append(('prd_only', 'PRD' in r_prd and 'PRD context informs' in r_prd)); checks.append(('both', 'TDD' in r_both and 'PRD' in r_both and 'When both TDD and PRD' in r_both)); [print(f'{n}: {\"PASS\" if v else \"FAIL\"}') for n, v in checks]; print('ALL PASS' if all(v for _, v in checks) else 'SOME FAILED')"`. This tests all 4 scenarios (none, TDD-only, PRD-only, both) for the new generation enrichment function. Note: the function signature is `build_tasklist_generate_prompt(roadmap_file, tdd_file=None, prd_file=None)` -- only `roadmap_file` is positional; `tdd_file` and `prd_file` must use keyword arguments. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase7-generate-prompt-verification.md`. If any check fails, add a row to the Phase 7 Findings table with the specific scenario that failed and what was expected vs actual. Once done, mark this item as complete.

- [ ] **7.6** Write a Phase 7 summary by reading all `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase7-*.md` files. Write to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/validation-enrichment-summary.md` with: (1) Enrichment test results table, (2) Enriched vs Baseline comparison, (3) PRD-only enrichment results, (4) Generate prompt function verification results, (5) Limitation note about tasklist generate being inference-only (generation prompt exists as a function but has no CLI entry point), (6) Critical Findings. Once done, mark this item as complete.

---

## Phase 8: TDD+PRD vs TDD-Only Comparison (5 items)

> **Purpose:** Compare Test 1 (TDD+PRD) results against the prior TDD-only results at `.dev/test-fixtures/results/test1-tdd-modified/` to quantify the value PRD enrichment adds to the TDD pipeline path. Also compare Test 2 (spec+PRD) against prior spec-only results.
>
> **Handoff input:** New results at `.dev/test-fixtures/results/test1-tdd-prd/` and `.dev/test-fixtures/results/test2-spec-prd/`. Prior results at `.dev/test-fixtures/results/test1-tdd-modified/` and `.dev/test-fixtures/results/test2-spec-modified/` (READ-ONLY).

- [ ] **8.1** Compare Test 1 extraction: TDD+PRD vs TDD-only by reading `extraction.md` from both `.dev/test-fixtures/results/test1-tdd-prd/extraction.md` and `.dev/test-fixtures/results/test1-tdd-modified/extraction.md`. Compare: (a) frontmatter field counts (both should have 19 TDD fields), (b) body section counts (both should have >= 14), (c) PRD-specific content in the new extraction that is absent in the old: persona references, business metrics, compliance items. Write a side-by-side comparison to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase8-extraction-tdd-comparison.md` with columns: Dimension, TDD-Only (prior), TDD+PRD (new), Delta, Assessment. Log findings in the Phase 8 Findings section of the Task Log at the bottom of this task file. Once done, mark this item as complete.

- [ ] **8.2** Compare Test 1 roadmap: TDD+PRD vs TDD-only by reading `roadmap.md` from both `.dev/test-fixtures/results/test1-tdd-prd/roadmap.md` and `.dev/test-fixtures/results/test1-tdd-modified/roadmap.md`. Compare: (a) line counts (PRD-enriched may be longer), (b) TDD identifier presence (both should reference auth components), (c) PRD-specific content in new roadmap: business value ordering, persona references, compliance milestones. Quantify enrichment: count instances of PRD-specific terms in each roadmap. Write comparison to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase8-roadmap-tdd-comparison.md`. Log findings in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.3** Compare Test 2 extraction: spec+PRD vs spec-only by reading `extraction.md` from both `.dev/test-fixtures/results/test2-spec-prd/extraction.md` and `.dev/test-fixtures/results/test2-spec-modified/extraction.md`. Compare: (a) both should have exactly 13 frontmatter fields (no TDD fields in either), (b) both should have exactly 8 body sections, (c) PRD-specific content in the new extraction. **CRITICAL**: Verify no TDD content leaked into either version. Write comparison to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase8-extraction-spec-comparison.md`. Log findings in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.4** Compare Test 2 roadmap: spec+PRD vs spec-only by reading `roadmap.md` from both `.dev/test-fixtures/results/test2-spec-prd/roadmap.md` and `.dev/test-fixtures/results/test2-spec-modified/roadmap.md`. Compare: (a) line counts, (b) PRD-specific content, (c) **CROSS-CONTAMINATION CHECK**: PRD content should appear in the new roadmap but TDD-specific component names should NOT appear (since TDD was not provided as input). Write comparison to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase8-roadmap-spec-comparison.md`. Log findings in the Phase 8 Findings section. Once done, mark this item as complete.

- [ ] **8.5** Write a Phase 8 summary by reading all `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase8-*.md` files. Write to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-run-comparison-summary.md` with: (1) TDD+PRD vs TDD-Only comparison matrix (extraction, roadmap, fidelity), (2) spec+PRD vs spec-only comparison matrix, (3) Cross-contamination matrix: where PRD content appeared vs where TDD content leaked, (4) Enrichment value assessment: did PRD enrichment add meaningful content? (5) Critical Findings. Once done, mark this item as complete.

---

## Phase 9: Cross-Pipeline Comparison and Anti-Instinct Analysis (4 items)

> **Purpose:** Compare anti-instinct results across all four runs (TDD-only, spec-only, TDD+PRD, spec+PRD), compare pipeline completion status, and analyze whether PRD enrichment affects gate pass rates.
>
> **Handoff input:** Anti-instinct and state files from all four result directories.

- [ ] **9.1** Compare anti-instinct results across all four runs by reading `anti-instinct-audit.md` from: (a) `.dev/test-fixtures/results/test1-tdd-modified/anti-instinct-audit.md` (TDD-only prior), (b) `.dev/test-fixtures/results/test1-tdd-prd/anti-instinct-audit.md` (TDD+PRD new), (c) `.dev/test-fixtures/results/test2-spec-modified/anti-instinct-audit.md` (spec-only prior), (d) `.dev/test-fixtures/results/test2-spec-prd/anti-instinct-audit.md` (spec+PRD new). For each, extract `fingerprint_coverage`, `undischarged_obligations`, `uncovered_contracts`. Write a 4-way comparison table to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase9-anti-instinct-4way.md` with columns: Run, fingerprint_coverage, undischarged_obligations, uncovered_contracts, PASS/FAIL. Analyze: did PRD enrichment improve or degrade anti-instinct results? Log findings in the Phase 9 Findings section of the Task Log at the bottom of this task file. Once done, mark this item as complete.

- [ ] **9.2** Compare pipeline completion status across all four runs by reading `.roadmap-state.json` from all four result directories. For each run, extract the status of every pipeline step. Write a 4-way step comparison table to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase9-pipeline-4way.md` with columns: Step, TDD-Only, TDD+PRD, Spec-Only, Spec+PRD. Analyze: did PRD enrichment cause any new step failures or resolve any existing ones? Log findings in the Phase 9 Findings section. Once done, mark this item as complete.

- [ ] **9.3** Compare fidelity results between TDD+PRD and spec+PRD runs. If spec-fidelity.md exists in either new result directory, read both and compare: (a) severity counts, (b) PRD-specific dimensions 12-15 presence, (c) TDD-specific dimensions presence/absence. If spec-fidelity was skipped in both (anti-instinct halt), note "SKIPPED in both -- anti-instinct pre-existing blocker" and do not treat as failure. Write results to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase9-fidelity-comparison.md`. Log findings in the Phase 9 Findings section. Once done, mark this item as complete.

- [ ] **9.4** Write a Phase 9 summary by reading all `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/test-results/phase9-*.md` files. Write to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-pipeline-analysis.md` with: (1) 4-way anti-instinct comparison table, (2) 4-way pipeline step comparison table, (3) Fidelity comparison results, (4) PRD impact assessment: positive (enrichment observed, no regressions), neutral (no observable difference), or negative (regressions introduced). Once done, mark this item as complete.

---

## Phase 10: Final Verification Report (3 items)

> **Purpose:** Produce the final comprehensive verification report covering all test runs, cross-run comparisons, auto-wire testing, validation enrichment, and PRD enrichment assessment.
>
> **Handoff input:** All phase summaries and comparison results from Phases 4-9.

- [ ] **10.1** Compile the final verification report by reading all phase summaries in `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/` and all Phase Findings tables from the Task Log at the bottom of this task file. Create the file `.dev/test-fixtures/results/verification-report-prd-integration.md` containing: (1) **Executive Summary** with overall PASS/FAIL verdict and 1-paragraph summary of PRD enrichment impact, (2) **Test 1 Results (TDD+PRD)** pass/fail table with PRD enrichment column, (3) **Test 2 Results (Spec+PRD)** pass/fail table with TDD leak check and PRD enrichment column, (4) **Auto-Wire Test Results** table from Phase 6, (5) **Validation Enrichment Results** table from Phase 7, (6) **Cross-Run Comparison** (TDD+PRD vs TDD-only, spec+PRD vs spec-only) with enrichment delta, (7) **Anti-Instinct 4-Way Comparison** from Phase 9, (8) **Success Criteria Checklist** evaluating each criterion: PRD flag accepted (yes/no), PRD enrichment in extraction (yes/no), PRD enrichment in roadmap (yes/no), PRD fidelity dimensions 12-15 (yes/no), state file stores prd_file/input_type (yes/no), auto-wire works (yes/no), tasklist validation enrichment (yes/no), no TDD leak in spec+PRD path (yes/no), no regressions from PRD (yes/no), (9) **Known Issues** documenting expected failures, (10) **Findings** with any unexpected issues. If unable to compile, log in the Phase 10 Findings section. Once done, mark this item as complete.

- [ ] **10.2** Compare the new verification report against the prior verification report by reading both `.dev/test-fixtures/results/verification-report-prd-integration.md` (new) and `.dev/test-fixtures/results/verification-report-modified-repo.md` (prior). Summarize what changed: new success criteria added, any criteria that regressed, any criteria that improved. Write a delta report to `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/verification-delta.md`. Once done, mark this item as complete.

- [ ] **10.3** Write consolidated follow-up action items by reading the ENTIRE Task Log at the bottom of this task file (all Phase Findings tables, Open Questions, Deferred Work). Create `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` containing: (1) **Bugs Found** -- every CRITICAL/IMPORTANT finding with item number, failure description, root cause hypothesis, file+function to investigate, (2) **Known Issues Confirmed** -- pre-existing issues (anti-instinct, Click stderr) confirmed by this run, (3) **PRD Enrichment Assessment** -- did enrichment achieve its goals? What was missing?, (4) **Auto-Wire Assessment** -- did auto-wire work? Gaps?, (5) **Validation Enrichment Assessment** -- did tasklist validation enrichment work? Gaps?, (6) **Deferred Work** -- items from Deferred Work table plus any new, (7) **Recommended Next Steps** -- prioritized list. This file must be self-contained for a future developer who has never seen these test runs. Once done, mark this item as complete.

---

## Phase 11: Completion (2 items)

> **Purpose:** Final deliverable verification and task status update.

- [ ] **11.1** Verify all deliverables exist by checking the following files: `.dev/test-fixtures/test-prd-user-auth.md` (PRD fixture), `.dev/test-fixtures/results/test1-tdd-prd/extraction.md` (Test 1 output), `.dev/test-fixtures/results/test2-spec-prd/extraction.md` (Test 2 output), `.dev/test-fixtures/results/verification-report-prd-integration.md` (final report), `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/follow-up-action-items.md` (follow-up actions), `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/cross-run-comparison-summary.md` (comparison), `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/auto-wire-summary.md` (auto-wire), `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/validation-enrichment-summary.md` (enrichment). List any missing deliverables. If all present, note "All deliverables confirmed." Log any missing items in the Phase 11 Findings section of the Task Log at the bottom of this task file. Once done, mark this item as complete.

- [ ] **11.2** Update the `status` field in this task file's YAML frontmatter from `in-progress` to `done` and set `updated_date` to today's date. If unable to complete, log in the Phase 11 Findings section. Once done, mark this item as complete.

---

## Task Log / Notes

### Execution Log

| Timestamp | Phase | Item | Status | Notes |
|-----------|-------|------|--------|-------|
| | | | | |

### Phase 1 Findings

_No findings yet._

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

_No findings yet._

### Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| AI-1 | Anti-instinct gate halts both TDD and spec pipelines (pre-existing). Will PRD enrichment improve or degrade anti-instinct pass rates? | OPEN | Investigate in Phase 9 item 9.1 with 4-way comparison. |
| TG-1 | Tasklist generation enrichment cannot be tested via CLI (no `superclaude tasklist generate` command). Only validation enrichment is testable. | EXPECTED | Phase 7 tests validation enrichment only. Document limitation in verification report. |
| AW-1 | Auto-wire from `.roadmap-state.json` -- does the implementation save `tdd_file` as null when TDD is the primary input, or does it store the primary input path? | OPEN | Investigate in Phase 4 item 4.9b and Phase 6 item 6.1. |
| RG-1 | Redundancy guard warning may be swallowed by Click stderr in dry-run mode (same display bug as auto-detection messages). | EXPECTED | Test in Phase 3 item 3.4. If swallowed, note as known limitation. |

### Deferred Work Items

| Item | Rationale | Dependency |
|------|-----------|------------|
| Tasklist generation enrichment E2E test | No CLI command exists. Requires `/sc:tasklist` skill invocation testing or future `tasklist generate` CLI. | `superclaude tasklist generate` command creation |
| PRD auto-detection path | PRD documents currently detect as "spec". Future: dedicated PRD detection type. | PRD pipeline Phase 2+ future work |
| Anti-instinct gate fix | Pre-existing issue blocking post-merge pipeline steps. Not caused by PRD changes. | Independent work item |
