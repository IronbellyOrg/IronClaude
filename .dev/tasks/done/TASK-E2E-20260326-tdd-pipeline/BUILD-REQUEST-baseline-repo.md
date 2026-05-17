# BUILD REQUEST: E2E Test — Spec in Original Unmodified Repo

## GOAL

Build a task file that executes one end-to-end pipeline test in the ORIGINAL IronClaude repo (master branch, commit `4e0c621`, before any feat/tdd-spec-merge changes):

**Test 3 — Spec in baseline:** Run the same spec fixture (`.dev/test-fixtures/test-spec-user-auth.md`) through `superclaude roadmap run` in the unmodified codebase. This produces the baseline output to compare against Test 2 (same spec in modified repo).

## WHY

Test 2 runs the spec through our modified pipeline. Test 3 runs the SAME spec through the original pipeline. Comparing Test 2 vs Test 3 output proves our changes didn't alter spec-path behavior. The ONLY expected difference is the fidelity prompt language ("source-document fidelity analyst" vs "specification fidelity analyst"). Any other structural difference means we broke something.

## TEST PLAN

Read the full test plan at `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md` — specifically the "Test 3: Spec in Original Unmodified Repo" section and the "Comparison: Test 2 vs Test 3" table.

## PREREQUISITES

- Test 2 must have completed first (spec fixture `.dev/test-fixtures/test-spec-user-auth.md` must exist — created by the modified-repo task)
- Test 2 output must exist at `.dev/test-fixtures/results/test2-spec-modified/` for comparison

## OUTPUTS

| Output | Path |
|---|---|
| Baseline pipeline output | `.dev/test-fixtures/results/test3-spec-baseline/` (in worktree or baseline checkout) |
| Comparison report | `.dev/test-fixtures/results/comparison-test2-vs-test3.md` |

## PHASES

### Phase 1: Set Up Baseline Environment
- Create a git worktree from master (pre-change commit): `git worktree add ../IronClaude-baseline master`
- Install the baseline package: `cd ../IronClaude-baseline && make dev`
- Copy the spec fixture into the baseline: `cp .dev/test-fixtures/test-spec-user-auth.md ../IronClaude-baseline/.dev/test-fixtures/test-spec-user-auth.md` (create directories as needed)
- Verify `superclaude` CLI works in the baseline: `cd ../IronClaude-baseline && superclaude --version`

### Phase 2: Test 3 — Full Spec Pipeline Run in Baseline
- `cd ../IronClaude-baseline && superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --output .dev/test-fixtures/results/test3-spec-baseline/`
- After completion: verify every artifact per E2E test plan Test 3 verification table (extraction.md has 8 sections, 13 frontmatter fields, full pipeline completes)

### Phase 3: Copy Baseline Results Back
- Copy Test 3 output from the worktree back to the main repo for comparison: `cp -r ../IronClaude-baseline/.dev/test-fixtures/results/test3-spec-baseline/ .dev/test-fixtures/results/test3-spec-baseline/`

### Phase 4: Comparison — Test 2 vs Test 3
- Read Test 2 output from `.dev/test-fixtures/results/test2-spec-modified/`
- Read Test 3 output from `.dev/test-fixtures/results/test3-spec-baseline/`
- Compare per E2E test plan comparison table:

| Point | Test 2 (Modified) | Test 3 (Baseline) | Expected |
|---|---|---|---|
| extraction.md section count | 8 | 8 | Same |
| extraction.md frontmatter field count | 13 | 13 | Same |
| extraction.md has TDD sections | No | No | Same |
| Prompt used | `build_extract_prompt()` | `build_extract_prompt()` | Same (unmodified function) |
| Fidelity prompt language | "source-document fidelity analyst" | "specification fidelity analyst" | Different — ONE expected diff |
| Anti-instinct passes | Yes | Yes | Same |
| Pipeline completes fully | Yes | Yes | Same |

- Write comparison report to `.dev/test-fixtures/results/comparison-test2-vs-test3.md`
- Flag ANY unexpected differences as failures

### Phase 4b: Full Artifact Comparison — All Three Tests
- Read ALL artifacts from all three test output directories
- Produce a comprehensive comparison report at `.dev/test-fixtures/results/full-artifact-comparison.md` covering:

**Test 2 vs Test 3 (spec-to-spec — proves we didn't break anything):**
For EACH artifact (extraction.md, roadmap.md, anti-instinct-audit.md, test-strategy.md, spec-fidelity.md, etc.):
- Same YAML frontmatter fields? Same field count?
- Same body section structure?
- Same gate pass/fail behavior?
- Flag every structural difference. Only expected diff: fidelity prompt language.

**Test 1 vs Test 3 (TDD vs spec — proves TDD expands the pipeline):**
For EACH artifact:
- extraction.md: Test 1 should have 14 sections + 19 frontmatter fields. Test 3 should have 8 sections + 13 fields. The 6 extra sections and 6 extra fields are the TDD expansion.
- roadmap.md: Test 1 should reference TDD-specific content (data models, API endpoints, component names, test cases, migration phases, runbook scenarios) that Test 3 does NOT contain — because the spec doesn't have that content.
- anti-instinct-audit.md: Compare fingerprint counts. Test 1 should have MORE fingerprints (TDD has more backticked identifiers). Compare coverage ratios.
- test-strategy.md: Both should have valid test strategies but Test 1's should reference TDD §15 testing content.
- spec-fidelity.md: Both should pass. Test 1 uses generalized comparison dimensions (11 including API, Components, Testing, Migration, Ops). Test 3 uses original dimensions (6).

This comparison is the definitive proof that:
1. The spec path works exactly as before (Test 2 ≈ Test 3)
2. The TDD path produces everything the spec path does PLUS expanded content from TDD sections (Test 1 ⊃ Test 3)

### Phase 5: Cleanup
- Remove the worktree: `git worktree remove ../IronClaude-baseline` (or keep for debugging if failures found)
- Write final pass/fail verdict

## TEMPLATE

02 (complex — worktree setup, subprocess execution, cross-repo comparison)

## CONTEXT FILES

- `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md` — full test plan
- `.dev/test-fixtures/test-spec-user-auth.md` — spec fixture (must exist from modified-repo task)
- `.dev/test-fixtures/results/test2-spec-modified/` — Test 2 output (must exist from modified-repo task)
