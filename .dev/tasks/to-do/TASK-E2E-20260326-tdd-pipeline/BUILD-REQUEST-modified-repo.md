# BUILD REQUEST: E2E Tests — TDD + Spec in Modified Repo

## GOAL

Build a task file that executes two end-to-end pipeline tests in the modified IronClaude repo (feat/tdd-spec-merge branch):

**Test 1 — TDD path:** Create a populated TDD from the template at `src/superclaude/examples/tdd_template.md`, run it through `superclaude roadmap run` (auto-detection should route to TDD extraction), and verify every output artifact.

**Test 2 — Spec path:** Create a populated spec from the template at `src/superclaude/examples/release-spec-template.md` covering the same feature, run it through `superclaude roadmap run` (auto-detection should route to spec extraction), and verify every output artifact. This proves our changes didn't break the existing spec pipeline.

Both tests use the same "User Authentication Service" feature so roadmap output is comparable.

## WHY

All testing so far was unit-level (individual functions, string assertions, config defaults). We have never run the actual `superclaude roadmap run` CLI end-to-end with a real document. We need to confirm:
- Auto-detection (`detect_input_type()`) correctly identifies TDD vs spec at runtime
- `build_extract_prompt_tdd()` produces extraction.md with all 14 sections
- All pipeline gates (EXTRACT_GATE, GENERATE_A/B_GATE, DIFF_GATE, DEBATE_GATE, SCORE_GATE, MERGE_GATE, ANTI_INSTINCT_GATE, TEST_STRATEGY_GATE, SPEC_FIDELITY_GATE) pass for TDD-derived output
- The spec path is completely unaffected by our changes — standard 8-section extraction, no TDD content leaks

## TEST PLAN

Read the full test plan at `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md` for detailed fixture specifications, verification criteria per artifact, and success criteria.

## OUTPUTS

| Output | Path |
|---|---|
| Populated TDD fixture | `.dev/test-fixtures/test-tdd-user-auth.md` |
| Populated spec fixture | `.dev/test-fixtures/test-spec-user-auth.md` |
| Test 1 pipeline output | `.dev/test-fixtures/results/test1-tdd-modified/` |
| Test 2 pipeline output | `.dev/test-fixtures/results/test2-spec-modified/` |
| Verification report | `.dev/test-fixtures/results/verification-report-modified-repo.md` |

## PHASES

### Phase 1: Create Test Fixtures
- Copy `src/superclaude/examples/tdd_template.md` → `.dev/test-fixtures/test-tdd-user-auth.md` and populate all 28 sections for "User Authentication Service" per the E2E test plan Fixture 1 specification. Replace ALL `[placeholder]` brackets. Populate §5, §6, §7, §8, §10, §15, §19, §20, §24, §25 with real content. All key identifiers as backticked names for fingerprint coverage.
- Copy `src/superclaude/examples/release-spec-template.md` → `.dev/test-fixtures/test-spec-user-auth.md` and populate for the same "User Authentication Service" per the E2E test plan Fixture 2 specification. Replace ALL `{{SC_PLACEHOLDER:...}}` sentinels. Use behavioral "shall/must" requirements.

### Phase 2: Dry-Run Verification
- Run `superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --dry-run` and verify: auto-detects as TDD, TDD warning printed, step plan correct, no errors.
- Run `superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --dry-run` and verify: auto-detects as spec, NO TDD warning, step plan correct, no errors.

### Phase 3: Test 1 — Full TDD Pipeline Run
- Run `superclaude roadmap run .dev/test-fixtures/test-tdd-user-auth.md --output .dev/test-fixtures/results/test1-tdd-modified/`
- After completion: verify every artifact per E2E test plan Test 1 verification table (extraction.md has 14 sections + 6 new frontmatter fields, roadmap references TDD content, anti-instinct fingerprint_coverage ≥ 0.7, spec-fidelity uses generalized language)

### Phase 4: Test 2 — Full Spec Pipeline Run
- Run `superclaude roadmap run .dev/test-fixtures/test-spec-user-auth.md --output .dev/test-fixtures/results/test2-spec-modified/`
- After completion: verify every artifact per E2E test plan Test 2 verification table (extraction.md has 8 sections only, NO TDD content, full pipeline completes including deviation-analysis)

### Phase 5: Comparison + Verification Report
- Compare Test 1 and Test 2 outputs per E2E test plan comparison table
- Write verification report to `.dev/test-fixtures/results/verification-report-modified-repo.md`
- Report pass/fail for each success criterion

## TEMPLATE

02 (complex — multi-phase, subprocess execution, artifact verification, comparison analysis)

## CONTEXT FILES

- `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md` — full test plan with fixture specs and verification criteria
- `src/superclaude/examples/tdd_template.md` — TDD template to populate
- `src/superclaude/examples/release-spec-template.md` — spec template to populate
- `src/superclaude/cli/roadmap/executor.py` — `detect_input_type()` function and extract step branching
- `src/superclaude/cli/roadmap/gates.py` — gate definitions for artifact verification
