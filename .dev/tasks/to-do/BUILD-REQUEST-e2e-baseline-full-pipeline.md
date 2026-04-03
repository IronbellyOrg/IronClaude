# BUILD REQUEST: Baseline Complete E2E Pipeline — Spec-Only in Original Repo (Roadmap + Tasklist)

## GOAL

Build a task file that runs the COMPLETE pipeline (roadmap generation → tasklist generation → tasklist validation) using ONLY the spec fixture in the original unmodified repo (master branch, before feat/tdd-spec-merge changes). This is the baseline against which we compare the TDD+PRD enriched pipeline.

**This task mirrors the structure of the enriched E2E task (BUILD-REQUEST-e2e-full-pipeline-with-tasklist.md) but runs in a git worktree on the master branch with only the spec fixture — no TDD, no PRD.**

## WHY

Without a baseline that includes the FULL pipeline (roadmap + tasklist + validation), we cannot answer: "Does the PRD/TDD-enriched pipeline produce better output than the original spec-only pipeline?" We need the same pipeline stages run on the original code to produce comparable artifacts.

## HOW TO BUILD THIS TASK

### Phase 1: Set Up Baseline Environment
- Create git worktree from master: `git worktree add ../IronClaude-baseline master`
- Install the baseline package: `cd ../IronClaude-baseline && make dev`
- Copy the EXISTING spec fixture into the worktree: `cp .dev/test-fixtures/test-spec-user-auth.md ../IronClaude-baseline/.dev/test-fixtures/test-spec-user-auth.md` (create directories as needed). **DO NOT recreate the fixture — it already exists.**
- Verify `superclaude` CLI works in the baseline
- Create output directories

### Phase 2: Run Spec-Only Roadmap Pipeline in Baseline
- Run `superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --output .dev/test-fixtures/results/test3-spec-baseline/` in the worktree
- NOTE: In the baseline code, the CLI uses single `spec_file` positional arg (no nargs=-1), no `--prd-file`, no `--tdd-file`, no PRD auto-detection. This is the original behavior before our changes.
- Verify all pipeline artifacts produced (extraction, roadmap variants, diff, debate, score, merge, anti-instinct, etc.)
- Pipeline may halt at anti-instinct (same pre-existing issue)
- Verify extraction has standard 8 sections, 13 frontmatter fields (no TDD-specific fields)

### Phase 3: Generate Tasklist from Baseline Roadmap
- Generate a tasklist from the baseline roadmap using whatever generation mechanism exists in the baseline code
- If `/sc:tasklist` skill exists in the baseline worktree: use it with the roadmap
- If the skill does NOT exist in baseline (tasklist generation was added after master): document this as a baseline limitation and generate using `build_tasklist_generate_prompt` if it exists, or note the capability doesn't exist
- If NEITHER exists: this is a valid finding — the baseline has no tasklist generation. Document it. The comparison will show "baseline: no tasklist capability" vs "enriched: full tasklist with TDD/PRD content"
- Verify output if generated: tasklist-index.md and phase files

### Phase 4: Validate Baseline Tasklist
- If a tasklist was generated in Phase 3:
  - Run `superclaude tasklist validate` on the output (NO --tdd-file, NO --prd-file — original behavior)
  - The fidelity report should have NO Supplementary TDD or PRD sections (those code paths didn't exist in master)
  - This is the clean baseline: roadmap→tasklist alignment only
- If no tasklist was generated: skip validation and document as limitation

### Phase 5: Copy Results Back to Main Repo
- Copy ALL baseline results from worktree to main repo: `cp -r ../IronClaude-baseline/.dev/test-fixtures/results/test3-spec-baseline/ .dev/test-fixtures/results/test3-spec-baseline/`
- Verify all files copied successfully

### Phase 6: Roadmap Comparison — Enriched vs Baseline
Compare the enriched E2E results against the baseline. Per the original E2E test plan:

**Spec+PRD (modified) vs Spec-only (baseline) roadmap comparison:**

| Point | Spec+PRD (Modified) | Spec-Only (Baseline) | Expected |
|-------|--------------------|--------------------|----------|
| extraction.md section count | 8 | 8 | Same |
| extraction.md frontmatter fields | 13 | 13 | Same |
| extraction.md has TDD sections | No | No | Same |
| Fidelity prompt language | "source-document fidelity analyst" | "specification fidelity analyst" | Different — ONE expected diff |
| PRD enrichment in extraction | Yes (personas, compliance, metrics) | No | New enrichment |
| PRD enrichment in roadmap | Yes (business value, personas) | No | New enrichment |

**TDD+PRD (modified) vs Spec-only (baseline) comparison:**
This is the big comparison — the TDD+PRD pipeline should produce dramatically richer output than the spec-only baseline across every dimension.

### Phase 7: Tasklist Comparison — Enriched vs Baseline
Compare generated tasklists (if baseline tasklist exists):

| Metric | Spec-Only Baseline | TDD+PRD Enriched | Spec+PRD Enriched |
|--------|-------------------|------------------|-------------------|
| Total tasks | | | |
| Data model tasks | 0 (no TDD) | Expected >0 | 0 (no TDD) |
| API endpoint tasks | 0 (no TDD) | Expected >0 | 0 (no TDD) |
| Component tasks | Generic | Specific names | Generic |
| Persona references | 0 (no PRD) | Expected >0 | Expected >0 |
| Compliance tasks | 0 (no PRD) | Expected >0 | Expected >0 |
| Success metric tasks | 0 (no PRD) | Expected >0 | Expected >0 |
| Fidelity: supplementary sections | 0 (old code) | TDD 5 + PRD 4 | PRD 4 |

If baseline has no tasklist capability, document: "Baseline cannot generate tasklists — the entire tasklist pipeline is new functionality added by our TDD/PRD integration work."

### Phase 8: Final Report and Cleanup
- Write comprehensive comparison report answering: "Does TDD/PRD enrichment produce measurably better pipeline output across the FULL pipeline?"
- Include both roadmap-level and tasklist-level comparisons
- Clean up worktree: `git worktree remove ../IronClaude-baseline` (or keep for debugging)
- Update task status to done

## PREREQUISITES

**Existing fixtures (DO NOT recreate ANY of them):**
- `.dev/test-fixtures/test-spec-user-auth.md` — already on disk (312 lines). Copy into worktree, do not regenerate.
- `.dev/test-fixtures/test-tdd-user-auth.md` — already on disk (876 lines). NOT used in baseline run but exists for reference.
- `.dev/test-fixtures/test-prd-user-auth.md` — already on disk (406 lines). NOT used in baseline run but exists for reference.

**Enriched E2E results (must exist for comparison in Phases 6-7):**
- `.dev/test-fixtures/results/test1-tdd-prd/` — TDD+PRD pipeline output (from enriched E2E task)
- `.dev/test-fixtures/results/test2-spec-prd/` — Spec+PRD pipeline output (from enriched E2E task)
- Generated tasklists in those directories (from the enriched E2E task's tasklist generation phases)

**NOTE:** Phase 6-7 comparisons require the enriched E2E task to have completed first. Phases 1-5 (baseline run) can execute independently.

**Prior build request for reference:**
- `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md` — original baseline build request (roadmap only). This task EXTENDS it with tasklist phases.

## QA FOCUS GUIDANCE

**QA gates MUST focus on IronClaude pipeline code and behavior — NOT on executor/agent report quality.**

What QA should verify:
- Does the baseline pipeline produce valid artifacts?
- Does the baseline `tasklist validate` produce fidelity WITHOUT supplementary TDD/PRD sections?
- If baseline can generate tasklists, do they lack TDD/PRD enrichment?
- Are structural differences between baseline and enriched attributable to the TDD/PRD code changes?

What QA should NOT spend time on:
- Accuracy of prose in comparison reports
- Exact grep counts in summary tables

## IMPORTANT NOTES

1. The baseline repo may NOT have tasklist generation capability at all. Phase 3 MUST handle this gracefully.
2. The worktree runs ORIGINAL code. Check whether `superclaude` or `uv run superclaude` is the correct invocation.
3. The spec fixture is IDENTICAL in both baseline and enriched runs. Same file, same content.
4. **DO NOT recreate the spec fixture. It exists. Copy it.**

## TEMPLATE

02 (complex — worktree setup, full pipeline execution, tasklist generation, cross-repo comparison)

## CONTEXT FILES

| File | Why |
|------|-----|
| `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` | The enriched E2E task — baseline mirrors this structure |
| `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md` | Original test plan with Test 3 spec |
| `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md` | Prior baseline build request (roadmap only) |
| `.dev/test-fixtures/test-spec-user-auth.md` | The spec fixture (ALREADY EXISTS) |
| `src/superclaude/cli/tasklist/prompts.py` | Current tasklist prompts (baseline won't have TDD/PRD blocks) |
| `.claude/skills/sc-tasklist-protocol/SKILL.md` | Tasklist generation skill (may not exist in baseline) |
| `.dev/tasks/to-do/TASK-RF-20260403-tasklist-e2e/research/` | Prior research on tasklist subsystem |
