# R1: Existing Test Results Inventory

**Status**: Complete
**Researcher**: r1
**Date**: 2026-04-02
**Scope**: `.dev/test-fixtures/results/` -- all test output directories

---

## Summary

5 test directories exist, all containing roadmap pipeline artifacts. **Zero directories contain actual tasklist output** (tasklist-index.md, phase-*-tasklist.md). Two directories (test1-tdd-prd, test2-spec-prd) have a `tasklist-fidelity.md` file, but both confirm the tasklist was never generated -- they are fidelity stubs documenting the absence.

---

## Directory Inventory

### 1. test1-tdd-modified (roadmap only)

Source: TDD input, run against modified repo. Date: Apr 2 09:45.

| File | Size |
|------|------|
| .roadmap-state.json | 3,218 |
| anti-instinct-audit.md | 1,651 |
| base-selection.md | 12,733 |
| debate-transcript.md | 12,614 |
| diff-analysis.md | 10,627 |
| extraction.md | 27,999 |
| roadmap-haiku-architect.md | 22,966 |
| roadmap-opus-architect.md | 23,222 |
| roadmap.md | 38,850 |
| wiring-verification.md | 3,064 |
| *.err (7 files) | 0 each |

**Tasklist artifacts**: NONE
**Total content files**: 10 (all roadmap pipeline)

---

### 2. test1-tdd-prd (roadmap + fidelity stub)

Source: TDD+PRD input, run against original repo. Date: Apr 2 21:33--22:48.

| File | Size |
|------|------|
| .roadmap-state.json | 3,307 |
| anti-instinct-audit.md | 1,224 |
| base-selection.md | 12,831 |
| debate-transcript.md | 19,338 |
| diff-analysis.md | 11,294 |
| extraction.md | 28,864 |
| roadmap-haiku-architect.md | 43,460 |
| roadmap-opus-architect.md | 21,864 |
| roadmap.md | 32,640 |
| tasklist-fidelity.md | 4,223 |
| wiring-verification.md | 3,064 |
| *.err (8 files, incl tasklist-fidelity.err) | 0 each |

**Tasklist artifacts**: NONE (tasklist-fidelity.md confirms "No tasklist artifact exists in the output directory")
**Total content files**: 11 (10 roadmap pipeline + 1 fidelity stub)

---

### 3. test2-spec-modified (roadmap only)

Source: Spec input, run against modified repo. Date: Apr 2 09:45.

| File | Size |
|------|------|
| .roadmap-state.json | 3,228 |
| anti-instinct-audit.md | 1,013 |
| base-selection.md | 10,431 |
| debate-transcript.md | 23,072 |
| diff-analysis.md | 12,674 |
| extraction.md | 17,129 |
| roadmap-haiku-architect.md | 26,041 |
| roadmap-opus-architect.md | 21,216 |
| roadmap.md | 31,096 |
| wiring-verification.md | 3,064 |
| *.err (7 files) | 0 each |

**Tasklist artifacts**: NONE
**Total content files**: 10 (all roadmap pipeline)

---

### 4. test2-spec-prd (roadmap + fidelity stub)

Source: Spec+PRD input, run against original repo. Date: Apr 2 22:07--22:49.

| File | Size |
|------|------|
| .roadmap-state.json | 3,318 |
| anti-instinct-audit.md | 1,037 |
| base-selection.md | 8,450 |
| debate-transcript.md | 18,765 |
| diff-analysis.md | 10,343 |
| extraction.md | 14,671 |
| roadmap-haiku-architect.md | 27,184 |
| roadmap-opus-architect.md | 21,223 |
| roadmap.md | 27,698 |
| tasklist-fidelity.md | 883 |
| wiring-verification.md | 3,064 |
| *.err (8 files, incl tasklist-fidelity.err) | 0 each |

**Tasklist artifacts**: NONE (tasklist-fidelity.md confirms "the downstream tasklist artifact does not exist")
**Total content files**: 11 (10 roadmap pipeline + 1 fidelity stub)

---

### 5. test3-spec-baseline (roadmap only)

Source: Spec input, baseline run. Date: Apr 2 21:30.

| File | Size |
|------|------|
| .roadmap-state.json | 3,318 |
| anti-instinct-audit.md | 673 |
| base-selection.md | 13,379 |
| debate-transcript.md | 15,250 |
| diff-analysis.md | 9,831 |
| extraction.md | 13,775 |
| roadmap-haiku-architect.md | 62,518 |
| roadmap-opus-architect.md | 18,407 |
| roadmap.md | 27,192 |
| wiring-verification.md | 3,064 |
| *.err (7 files) | 0 each |

**Tasklist artifacts**: NONE
**Total content files**: 10 (all roadmap pipeline)

---

## Top-Level Comparison/Report Files

| File | Size | Date |
|------|------|------|
| comparison-test2-vs-test3.md | 5,408 | Apr 3 07:22 |
| e2e-test3-verdict.md | 2,119 | Apr 3 07:22 |
| full-artifact-comparison.md | 8,671 | Apr 3 07:22 |
| verification-report-modified-repo.md | 7,848 | Apr 2 09:45 |
| verification-report-prd-integration.md | 17,080 | Apr 2 23:31 |

---

## Key Findings for Baseline E2E Task

1. **No tasklist generation has ever been run** against any of these roadmaps. All 5 directories contain only roadmap pipeline output (extraction through wiring-verification).

2. **Two fidelity stubs exist** (test1-tdd-prd, test2-spec-prd) that explicitly document the missing tasklist and recommend running the tasklist pipeline as a next step.

3. **All error files are 0 bytes** -- every roadmap pipeline stage completed without errors across all 5 runs.

4. **Standard roadmap artifact set** across all directories (10 files):
   - .roadmap-state.json
   - extraction.md
   - roadmap-opus-architect.md
   - roadmap-haiku-architect.md
   - diff-analysis.md
   - debate-transcript.md
   - base-selection.md
   - roadmap.md (final merged)
   - anti-instinct-audit.md
   - wiring-verification.md

5. **Best candidates for full E2E testing** (roadmap already exists, just need tasklist generation):
   - `test1-tdd-prd/roadmap.md` (32,640 bytes) -- TDD+PRD enriched input
   - `test2-spec-prd/roadmap.md` (27,698 bytes) -- Spec+PRD enriched input
   - `test3-spec-baseline/roadmap.md` (27,192 bytes) -- baseline spec-only input

6. **Missing artifacts that a full E2E run must produce**:
   - `tasklist-index.md` -- master index of all phase tasklists
   - `phase-N-tasklist.md` -- per-phase task breakdowns
   - `tasklist-fidelity.md` -- re-run with actual tasklist to validate (not the current stubs)
