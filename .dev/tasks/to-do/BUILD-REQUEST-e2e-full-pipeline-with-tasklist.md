# BUILD REQUEST: Complete E2E Pipeline — Roadmap + Tasklist Generation + Validation (TDD+PRD and Spec+PRD)

## GOAL

Build a task file that is a COPY of the completed E2E task at `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` with ALL checkboxes reset to unchecked, PLUS new phases added for tasklist generation and tasklist validation with real tasklists.

The prior E2E task (67 items, 11 phases) ran the full roadmap pipeline for both TDD+PRD and Spec+PRD paths, verified all artifacts, tested auto-wire, tested multi-file CLI, and did cross-run comparisons. But it NEVER generated a tasklist — so all the TDD/PRD enrichment work in `build_tasklist_generate_prompt` and `build_tasklist_fidelity_prompt` was never verified end-to-end.

This task runs EVERYTHING the prior task did (full roadmap pipeline runs, artifact verification, auto-wire, multi-file CLI, cross-run comparison) AND THEN generates tasklists from the roadmap outputs and validates them with TDD/PRD enrichment.

**This is the definitive, complete E2E test of the entire pipeline: roadmap generation → tasklist generation → tasklist validation.**

## WHY

The prior E2E task had a fatal gap: Phases 6 and 7 ran `tasklist validate` against directories with no tasklist. The fidelity validator was validating against nothing. We need a single task that tests the FULL pipeline end-to-end without gaps.

## HOW TO BUILD THIS TASK

### Step 1: Copy the existing E2E task
Read the COMPLETED task file at `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md`. Copy ALL of its content — frontmatter, overview, objectives, prerequisites, ALL 11 phases with ALL 67 items, known issues, open questions, deferred work, task log.

**CRITICAL: All three test fixtures already exist on disk and MUST NOT be recreated:**
- `.dev/test-fixtures/test-tdd-user-auth.md` (876 lines, TDD fixture)
- `.dev/test-fixtures/test-spec-user-auth.md` (312 lines, Spec fixture)
- `.dev/test-fixtures/test-prd-user-auth.md` (406 lines, PRD fixture)
Remove the old Phase 2 (Create PRD Test Fixture) entirely. Replace with a verification-only item in Phase 1 that confirms all three fixtures exist.

### Step 2: Reset it
- Change the ID to a new task ID
- Set status to `to-do`, clear start_date, completion_date
- Reset ALL `- [x]` back to `- [ ]`
- Clear all findings tables
- Update all internal path references to use the new task ID
- Update output directories to avoid overwriting prior results (e.g., `test1-tdd-prd-v2/`, `test2-spec-prd-v2/` or similar)

### Step 3: Fix Phases 6 and 7
The existing Phases 6 (Auto-Wire) and 7 (Validation Enrichment) run `tasklist validate` against directories that have no tasklist. These phases need to be MOVED to AFTER tasklist generation so they validate real tasklists.

Restructure:
- Keep Phase 1 (setup) but REMOVE fixture creation items — all three fixtures already exist at `.dev/test-fixtures/test-tdd-user-auth.md`, `.dev/test-fixtures/test-spec-user-auth.md`, `.dev/test-fixtures/test-prd-user-auth.md`. Phase 1 should only VERIFY they exist, not create them.
- **REMOVE old Phase 2 entirely** (Create PRD Test Fixture — 3 items). The PRD fixture already exists. DO NOT recreate it. Add a verification item to Phase 1 instead.
- Keep Phase 3 (dry-runs) renumbered as Phase 2
- Keep Phase 4 (Test 1 TDD+PRD pipeline) renumbered as Phase 3
- Keep Phase 5 (Test 2 Spec+PRD pipeline) renumbered as Phase 4
- **INSERT new Phase 5: Generate Tasklist from Test 1 (TDD+PRD) Roadmap**
- **INSERT new Phase 6: Generate Tasklist from Test 2 (Spec+PRD) Roadmap**
- MOVE old Phase 6 (Auto-Wire) to Phase 7 — NOW auto-wire will find a real tasklist
- MOVE old Phase 7 (Validation Enrichment) to Phase 8 — NOW validation runs against real tasklists
- Keep old Phases 8-11 (cross-run comparison, cross-pipeline analysis, final report, completion) renumbered as Phases 9-12

### Step 4: Add tasklist generation phases
New Phase 6 (Generate Tasklist from TDD+PRD Roadmap):
- Read the roadmap at the Test 1 output directory
- Invoke `/sc:tasklist` skill (or `build_tasklist_generate_prompt` + Claude inference) with both `tdd_file` and `prd_file` params
- Verify output: tasklist-index.md exists, phase files exist, checklist items present
- Verify TDD enrichment in generated tasklist: data model tasks (UserProfile, AuthToken), API endpoint tasks (/auth/login, /auth/register), component tasks (AuthService, TokenManager), test tasks from TDD §15, rollout tasks from TDD §19
- Verify PRD enrichment: persona references (Alex, Jordan, Sam), acceptance criteria tied to success metrics (conversion >60%, login p95 <200ms), compliance tasks (GDPR, SOC2), customer journey verification tasks

New Phase 7 (Generate Tasklist from Spec+PRD Roadmap):
- Same as Phase 6 but for the Test 2 output directory
- Generation with `prd_file` only (no `tdd_file` — spec path)
- Verify PRD enrichment present
- Verify NO TDD content leak (no data model tasks, no API endpoint tasks from TDD sections)
- This is critical: the spec+PRD path should produce tasklists with business context (personas, compliance, metrics) but NOT technical implementation detail from the TDD

### Step 5: Update validation phases to use real tasklists
The moved Phase 8 (Auto-Wire) and Phase 9 (Validation Enrichment) items that run `tasklist validate` will now execute against directories that HAVE real tasklists. Update the items' expected behavior:
- Fidelity reports should contain REAL findings with actual severity ratings (not "Cannot validate — no tasklist")
- Supplementary TDD Validation should have 5 checks with MEDIUM severity findings against actual task content
- Supplementary PRD Validation should have 4 checks (3 MEDIUM, 1 LOW) with actual findings
- The enriched vs baseline comparison should show meaningful differences (supplementary sections with real content vs no supplementary sections)

### Step 6: Add tasklist comparison items to cross-run phases
Update the cross-run comparison phases (old 8-9, now 10-11) to also compare generated tasklists:
- TDD+PRD tasklist vs Spec+PRD tasklist: data model tasks present in TDD+PRD but absent in Spec+PRD
- Enriched fidelity vs baseline fidelity: supplementary sections with real findings vs no supplementary sections

### Step 7: Update the final verification report
The final report (old Phase 10, now Phase 12) should include tasklist generation results and tasklist validation results in its success criteria checklist. Add criteria:
- Tasklist generated from TDD+PRD roadmap (yes/no)
- Tasklist generated from Spec+PRD roadmap (yes/no)
- TDD enrichment in generated tasklist (yes/no)
- PRD enrichment in generated tasklist (yes/no)
- No TDD leak in spec+PRD tasklist (yes/no)
- Fidelity validation produces REAL findings with actual tasklist (yes/no)
- Supplementary TDD section has 5 checks with real content (yes/no)
- Supplementary PRD section has 4 checks with real content (yes/no)

## PREREQUISITES

**Source task file (READ — this is what you copy and extend):**
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` — 67 items, 11 phases, status=done

**Tasklist generation mechanism:**
- `/sc:tasklist` inference skill at `.claude/skills/sc-tasklist-protocol/SKILL.md`
- `build_tasklist_generate_prompt` at `src/superclaude/cli/tasklist/prompts.py`
- There is NO `superclaude tasklist generate` CLI. Generation is inference-only.

**Tasklist validation:**
- `uv run superclaude tasklist validate` CLI exists and works
- `build_tasklist_fidelity_prompt` at `src/superclaude/cli/tasklist/prompts.py`
- Each validation run OVERWRITES `tasklist-fidelity.md` — must copy before next run

**Research from prior task-builder run (use as reference):**
- `.dev/tasks/to-do/TASK-RF-20260403-tasklist-e2e/research/01-tasklist-prompts.md` — both prompt builders documented
- `.dev/tasks/to-do/TASK-RF-20260403-tasklist-e2e/research/02-sc-tasklist-skill.md` — /sc:tasklist protocol documented
- `.dev/tasks/to-do/TASK-RF-20260403-tasklist-e2e/research/03-tasklist-executor-cli.md` — validation pipeline documented
- `.dev/tasks/to-do/TASK-RF-20260402-e2e-update/research/` — QA fix research from prior E2E update

## QA FOCUS GUIDANCE

**QA gates MUST focus on IronClaude pipeline code and behavior — NOT on executor/agent report quality.**

What QA should verify:
- Does the roadmap pipeline produce correct output with TDD/PRD enrichment? (Phases 4-5)
- Does tasklist generation produce tasklists with TDD/PRD enriched content? (Phases 6-7)
- Does `tasklist validate` with real tasklists produce fidelity reports with REAL findings? (Phase 9)
- Are supplementary TDD/PRD sections populated with actual content, not "Cannot validate"? (Phase 9)
- Zero TDD content leak in spec+PRD path across both roadmap AND tasklist? (Phases 5, 7, 9)

What QA should NOT spend time on:
- Whether summary reports have exact grep counts
- Whether prose accurately cross-references earlier phases
- Report compilation accuracy

## TEMPLATE

02 (complex — full pipeline E2E with generation, validation, comparison, multi-phase)

## CONTEXT FILES

| File | Why |
|------|-----|
| `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` | **THE SOURCE — copy this entire task and extend it** |
| `src/superclaude/cli/tasklist/prompts.py` | Both prompt builders being tested |
| `src/superclaude/cli/tasklist/executor.py` | Validation pipeline |
| `src/superclaude/cli/tasklist/commands.py` | CLI flags, auto-wire |
| `.claude/skills/sc-tasklist-protocol/SKILL.md` | How tasklist generation works |
| `.dev/tasks/to-do/TASK-RF-20260403-tasklist-e2e/research/` | Prior research on tasklist subsystem |
| `.dev/tasks/to-do/TASK-RF-20260402-e2e-update/research/` | Prior research on QA fixes and auto-detection |
