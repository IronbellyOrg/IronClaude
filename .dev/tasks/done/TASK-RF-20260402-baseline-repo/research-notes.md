# Research Notes: E2E Test 3 — Spec in Baseline Repo

**Date:** 2026-04-02
**Scenario:** A (explicit BUILD_REQUEST with detailed phases, commands, verification)
**Depth Tier:** Standard
**Track Count:** 1

---

## EXISTING_FILES

### Test Fixtures (verified)
- `.dev/test-fixtures/test-spec-user-auth.md` — 312 lines, spec fixture for User Auth Service
- `.dev/test-fixtures/test-tdd-user-auth.md` — TDD fixture (used in Test 1)

### Test 2 Output (verified at `.dev/test-fixtures/results/test2-spec-modified/`)
- `.roadmap-state.json` — pipeline state
- `extraction.md` — 17KB, spec extraction output
- `roadmap-haiku-architect.md` — 26KB, agent A roadmap
- `roadmap-opus-architect.md` — 21KB, agent B roadmap
- `roadmap.md` — 31KB, merged roadmap
- `anti-instinct-audit.md` — 1KB, fingerprint coverage
- `base-selection.md` — 10KB, base selection output
- `debate-transcript.md` — 23KB, adversarial debate
- `diff-analysis.md` — 13KB, diff analysis
- `wiring-verification.md` — 3KB, wiring verification
- Plus `.err` files for each step

### Test 1 Output (exists at `.dev/test-fixtures/results/test1-tdd-modified/`)
- Same artifact set as Test 2 (needed for Phase 4b full comparison)

### Master Branch
- Commit `4e0c621` — "Merge pull request #19 from IronbellyOrg/v3.7-TurnLedgerWiring"
- This is the pre-change baseline

### Build Request and Test Plan
- `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md`
- `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/E2E-TEST-PLAN.md`

## PATTERNS_AND_CONVENTIONS

### Roadmap Pipeline Artifacts
The `superclaude roadmap run` command produces these artifacts in the output directory:
- `extraction.md` — spec extraction (8 sections for spec, 14 for TDD)
- `roadmap-{agent-a}.md`, `roadmap-{agent-b}.md` — two parallel roadmaps
- `roadmap.md` — merged final roadmap
- `diff-analysis.md` — diff between two roadmaps
- `debate-transcript.md` — adversarial debate
- `base-selection.md` — base roadmap selection
- `anti-instinct-audit.md` — fingerprint coverage check
- `test-strategy.md` — testing strategy
- `spec-fidelity.md` — fidelity check (may use "specification fidelity analyst" in baseline)
- `wiring-verification.md` — wiring verification
- `.roadmap-state.json` — pipeline state tracking
- `.err` files for each step

### CLI Command
```bash
superclaude roadmap run <spec-file> --output <output-dir>
```
- Auto-detects input type (spec vs TDD)
- No `--input-type` flag needed for spec files
- In baseline (master), `--input-type` flag may not exist (it was added in our changes)

### Key Difference: Fidelity Prompt Language
- Modified repo: "source-document fidelity analyst" (generalized)
- Baseline repo: "specification fidelity analyst" (original)
- This is the ONE expected difference between Test 2 and Test 3

## GAPS_AND_QUESTIONS

1. Does the baseline `superclaude` CLI at master have a `spec-fidelity` step? (Need to verify — it should, as fidelity was added in v3.7 TurnLedger merge)
2. Does the baseline pipeline produce all the same artifacts? (Likely yes, minus any new steps added in our feature branch)
3. What happens if the baseline `superclaude roadmap run` command doesn't have `--output` flag? (Need to verify — it should exist)
4. The baseline may not have a `wiring-verification` step — need to check what steps exist in master

## RECOMMENDED_OUTPUTS

| # | Topic | Output File |
|---|-------|-------------|
| 01 | Test 2 artifact inventory | `research/01-test2-artifact-inventory.md` |
| 02 | Baseline pipeline capabilities | `research/02-baseline-pipeline-capabilities.md` |
| 03 | MDTM template 02 rules | `research/03-template-rules.md` |
| 04 | Git worktree and cross-repo operations | `research/04-worktree-operations.md` |

## SUGGESTED_PHASES

### Researcher 1 — File Inventory (Test 2 artifacts)
- **Topic type:** File Inventory
- **Scope:** `.dev/test-fixtures/results/test2-spec-modified/` and `.dev/test-fixtures/results/test1-tdd-modified/`
- **Focus:** Catalog every artifact with section counts, frontmatter field counts, gate pass/fail status — this is the comparison baseline
- **Output:** `research/01-test2-artifact-inventory.md`
- **Others cover:** baseline pipeline (R2), template rules (R3), worktree ops (R4)

### Researcher 2 — Integration Points (Baseline Pipeline)
- **Topic type:** Integration Points
- **Scope:** `src/superclaude/cli/roadmap/` — specifically checking what exists at master commit `4e0c621`
- **Focus:** Verify what pipeline steps exist in the baseline, what CLI flags are available, whether `--output` works, what artifacts the original pipeline produces
- **Output:** `research/02-baseline-pipeline-capabilities.md`
- **Others cover:** Test 2 artifacts (R1), template rules (R3), worktree ops (R4)

### Researcher 3 — Template & Examples
- **Topic type:** Template & Examples
- **Scope:** `.claude/templates/workflow/02_mdtm_template_complex_task.md` and `.dev/tasks/to-do/` existing task examples
- **Focus:** MDTM template 02 rules, item format, phase structure requirements
- **Output:** `research/03-template-rules.md`
- **Others cover:** Test 2 artifacts (R1), baseline pipeline (R2), worktree ops (R4)

### Researcher 4 — Data Flow Tracer (Worktree Operations)
- **Topic type:** Data Flow Tracer
- **Scope:** Git worktree mechanics, cross-repo file operations
- **Focus:** How to create a worktree from master, install the baseline, run the pipeline, copy results back, clean up
- **Output:** `research/04-worktree-operations.md`
- **Others cover:** Test 2 artifacts (R1), baseline pipeline (R2), template rules (R3)

## TEMPLATE_NOTES

**Template:** 02 (Complex Task) — This task involves:
- Environment setup (git worktree creation, package installation)
- Pipeline execution (subprocess management, waiting for completion)
- Cross-repo file operations (copying fixtures in, copying results out)
- Multi-artifact comparison (Test 2 vs Test 3, Test 1 vs Test 3)
- Conditional cleanup (keep worktree on failure)

**Tier:** Standard — moderate complexity, known files, explicit phases

**QA Gate Requirements:** FINAL_ONLY — single QA gate after all phases complete
**Validation Requirements:** Pipeline completes without Python errors; all comparison criteria met
**Testing Requirements:** NONE — this IS the test (E2E pipeline test, not code implementation)

## AMBIGUITIES_FOR_USER

None — intent is clear from the BUILD_REQUEST and E2E test plan. The request provides explicit phases, commands, verification criteria, and comparison tables.

**Status:** Complete
