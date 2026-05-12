# Research: Existing E2E Task Structure Inventory

**Status**: Complete
**Source**: `.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/TASK-E2E-20260326-modified-repo.md`
**Researcher**: researcher-01
**Purpose**: Full structural extraction for task cloning into PRD pipeline E2E task

---

## 1. YAML Frontmatter (Lines 1-16)

```yaml
---
id: TASK-E2E-20260326-modified-repo
title: "E2E Pipeline Tests — TDD and Spec Paths in Modified Repo"
status: done
priority: high
created: 2026-03-26
start_date: "2026-03-27"
updated_date: "2026-03-27"
last_session_note: "Phase 5 item 5.1 complete. Resume at 5.2. MUST use 'uv run superclaude' not bare 'superclaude'. Both pipelines halted at anti-instinct (pre-existing issue). TDD extraction works (14 sections, 19 fields). Spec extraction clean (8 sections, 0 TDD leak)."
type: verification
template: complex
estimated_items: 42
estimated_phases: 7
tags: ["e2e", "pipeline", "tdd", "spec", "verification", "roadmap"]
handoff_dir: ".dev/tasks/to-do/TASK-RF-20260326-e2e-modified/phase-outputs"
---
```

**Fields to clone and modify for PRD task:**
- `id` -> new task ID
- `title` -> PRD pipeline title
- `status` -> `to-do`
- `start_date` / `updated_date` -> clear
- `last_session_note` -> clear
- `estimated_items` -> recount
- `estimated_phases` -> likely same 7
- `tags` -> replace tdd/spec with prd
- `handoff_dir` -> new task path

---

## 2. Task Overview (Lines 18-23)

Single paragraph describing:
- What the task does (two E2E pipeline tests using `superclaude roadmap run`)
- What it verifies (TDD extraction path works, spec extraction path unbroken)
- How tests work (Test 1 = TDD fixture, Test 2 = spec fixture, same feature)
- Context (all prior testing was unit-level, first CLI pipeline exercise)
- Runtime note (pipeline spawns Claude subprocesses, 30-60 min each)

**For PRD task**: Replace with PRD pipeline description. Two tests: (1) PRD fixture through roadmap pipeline, (2) PRD fixture through tasklist pipeline (if CLI exists).

---

## 3. Key Objectives (Lines 26-33)

Seven bullet objectives:
1. Verify `detect_input_type()` correctly identifies TDD vs spec
2. Confirm `build_extract_prompt_tdd()` produces extraction.md with 14 sections/19 fields
3. Confirm all pipeline gates pass for TDD-derived output
4. Confirm spec path produces standard 8-section extraction with no TDD leaks
5. Confirm both pipelines produce valid roadmaps with fingerprint_coverage >= 0.7
6. Compare Test 1 and Test 2 outputs for structural differences
7. Document all results in verification report

---

## 4. Prerequisites and Dependencies (Lines 36-62)

Sections:
- **Branch**: working branch name
- **Source Templates**: paths to template files with stats (line count, sections, fields)
- **Pipeline Code**: 4 key source files with function names and descriptions
- **Known Issues**: 3 known bugs (B-1, TS-1, FP-1) with descriptions
- **Research Files**: 4 research file paths
- **E2E Test Plan**: reference to test plan file

---

## 5. Phase Structure (Complete Inventory)

### Phase 1: Preparation (3 items, Lines 65-74)

> **Purpose:** Read this task, update status, and create all output directories needed by subsequent phases.

| Item | Summary | Output Path | Verification |
|------|---------|-------------|-------------|
| 1.1 | Read task file, update YAML status to in-progress, set start_date | (modifies self) | status field updated |
| 1.2 | Create directory structure: test-fixtures/, results/test1-*/, results/test2-*/, phase-outputs/{discovery,test-results,reviews,reports}/ | (directories only) | dirs exist |
| 1.3 | Verify CLI available (`superclaude roadmap run --help`), verify templates exist | `phase-outputs/test-results/phase1-prereq-check.md` | CLI output contains "Usage", files readable |

### Phase 2: Create Test Fixtures (4 items, Lines 77-89)

> **Purpose:** Create two populated test fixtures from templates. TDD fixture triggers auto-detection as TDD (score >= 3). Spec fixture triggers auto-detection as spec.
> **Source templates:** TDD template, spec template

| Item | Summary | Output Path | Verification |
|------|---------|-------------|-------------|
| 2.1 | Create TDD fixture from template (populated for "User Authentication Service") — VERY LONG item (~3500 chars) specifying every frontmatter field, every section's content | `.dev/test-fixtures/test-tdd-user-auth.md` | All brackets replaced, key identifiers backticked |
| 2.2 | Sentinel checks on TDD fixture: grep for remaining placeholders, verify key identifiers | `phase-outputs/test-results/phase2-tdd-sentinel-check.md` | `[FEATURE-ID]`=0, `[version]`=0, `feature_id: "AUTH-001"`=1, UserProfile>0, AuthToken>0 |
| 2.3 | Create spec fixture from template (same feature) — VERY LONG item (~2500 chars) | `.dev/test-fixtures/test-spec-user-auth.md` | All `{{SC_PLACEHOLDER:...}}` replaced |
| 2.4 | Sentinel checks on spec fixture | `phase-outputs/test-results/phase2-spec-sentinel-check.md` | `{{SC_PLACEHOLDER:`=0, FR-AUTH>0, NFR-AUTH>0 |

### Phase 3: Dry-Run Verification (4 items, Lines 92-104)

> **Purpose:** Run both fixtures through `--dry-run` to verify auto-detection, step plan, flag behavior BEFORE full runs.

| Item | Summary | Output Path | Verification |
|------|---------|-------------|-------------|
| 3.1 | TDD dry-run: `superclaude roadmap run <fixture> --dry-run` | `phase-outputs/test-results/phase3-tdd-dryrun.md` | stderr: "Auto-detected input type: tdd", TDD warning present, step plan complete, no traceback |
| 3.2 | Spec dry-run: same command with spec fixture | `phase-outputs/test-results/phase3-spec-dryrun.md` | stderr: "Auto-detected input type: spec", NO TDD warning, step plan complete, no traceback |
| 3.3 | Compare two dry-run step plans | `phase-outputs/test-results/phase3-dryrun-comparison.md` | Step lists identical; only auto-detection msg and TDD warning differ |
| 3.4 | Go/no-go decision | `phase-outputs/test-results/phase3-go-nogo.md` | All critical checks pass |

### Phase 4: Test 1 — Full TDD Pipeline Run (12 items, Lines 107-140)

> **Purpose:** Execute full pipeline with TDD fixture, verify every output artifact. Primary test proving TDD extraction works E2E.
> **Handoff input:** TDD fixture path

| Item | Summary | Output Path | Checks |
|------|---------|-------------|--------|
| 4.1 | Run full pipeline with tee to log, capture EXIT_CODE | `phase-outputs/test-results/phase4-tdd-pipeline-log.md` | EXIT_CODE=0 or note gate failure |
| 4.2 | Verify extraction.md frontmatter: 13 standard + 6 TDD-specific fields | `phase-outputs/test-results/phase4-extraction-frontmatter.md` | Each field: name, expected type, actual value, PASS/FAIL |
| 4.3 | Verify extraction.md body: 14 sections (8 standard + 6 TDD) | `phase-outputs/test-results/phase4-extraction-sections.md` | grep count `## ` >= 14; each section FOUND/MISSING with line number |
| 4.4 | Verify roadmap variants (roadmap-opus-architect.md, roadmap-haiku-architect.md) | `phase-outputs/test-results/phase4-roadmap-variants.md` | >=100 lines, frontmatter fields, >=2 TDD identifiers |
| 4.5a | Verify diff-analysis.md | `phase-outputs/test-results/phase4-diff-analysis.md` | >=30 lines, `total_diff_points`, `shared_assumptions_count` |
| 4.5b | Verify debate-transcript.md | `phase-outputs/test-results/phase4-debate-transcript.md` | >=50 lines, `convergence_score`, `rounds_completed` |
| 4.5c | Verify base-selection.md | `phase-outputs/test-results/phase4-base-selection.md` | >=20 lines, `base_variant`, `variant_scores` |
| 4.6 | Verify merged roadmap.md | `phase-outputs/test-results/phase4-merged-roadmap.md` | >=150 lines, frontmatter, >=3 of 9 backticked identifiers |
| 4.7 | Verify anti-instinct-audit.md | `phase-outputs/test-results/phase4-anti-instinct.md` | fingerprint_coverage>=0.7, undischarged_obligations==0, uncovered_contracts==0 |
| 4.8 | Verify test-strategy.md | `phase-outputs/test-results/phase4-test-strategy.md` | complexity_class, validation_philosophy, interleave_ratio, major_issue_policy, work/validation_milestones |
| 4.9 | Verify spec-fidelity.md | `phase-outputs/test-results/phase4-spec-fidelity.md` | high_severity_count==0, validation_complete, tasklist_ready, "source-document fidelity analyst" language |
| 4.9a | Verify wiring-verification.md | `phase-outputs/test-results/phase4-wiring-verification.md` | >=10 lines, analysis_complete=true, blocking_findings=0 |
| 4.9b | Verify .roadmap-state.json | `phase-outputs/test-results/phase4-state-file.md` | schema_version=1, spec_file, spec_hash, agents>=2, steps object |
| 4.10 | Phase 4 summary report | `phase-outputs/reports/test1-tdd-summary.md` | Compile pass/fail table, critical findings, follow-up actions |

### Phase 5: Test 2 — Full Spec Pipeline Run (8 items, Lines 143-164)

> **Purpose:** Execute full pipeline with spec fixture, verify outputs. Proves modifications did not break spec path.
> **Handoff input:** Spec fixture path

| Item | Summary | Output Path | Checks |
|------|---------|-------------|--------|
| 5.1 | Run full spec pipeline | `phase-outputs/test-results/phase5-spec-pipeline-log.md` | EXIT_CODE, no TDD warnings |
| 5.2 | Verify extraction frontmatter: 13 standard ONLY, 6 TDD fields ABSENT | `phase-outputs/test-results/phase5-extraction-frontmatter.md` | Each standard field PRESENT, each TDD field ABSENT |
| 5.3 | Verify extraction body: 8 sections ONLY, 6 TDD sections ABSENT | `phase-outputs/test-results/phase5-extraction-sections.md` | Each standard FOUND, each TDD ABSENT |
| 5.4 | Verify merged roadmap | `phase-outputs/test-results/phase5-merged-roadmap.md` | >=150 lines, frontmatter, auth content |
| 5.5 | Verify anti-instinct | `phase-outputs/test-results/phase5-anti-instinct.md` | fingerprint_coverage>=0.7, obligations==0, contracts==0 |
| 5.6 | Verify spec-fidelity (cross-contamination check) | `phase-outputs/test-results/phase5-spec-fidelity.md` | high_severity_count==0, "source-document fidelity analyst", TDD dimensions absent/minimal |
| 5.7 | Verify all gates passed | `phase-outputs/test-results/phase5-pipeline-status.md` | .roadmap-state.json step-by-step table |
| 5.8 | Phase 5 summary report | `phase-outputs/reports/test2-spec-summary.md` | Compile pass/fail table, no TDD leaks confirmed |

### Phase 6: Comparison Analysis + Verification Report (5 items, Lines 167-184)

> **Purpose:** Compare Test 1 (TDD) and Test 2 (spec) outputs, check cross-contamination, produce final report.
> **Handoff input:** Both result dirs + phase summaries

| Item | Summary | Output Path | Checks |
|------|---------|-------------|--------|
| 6.1 | Compare extraction section counts (TDD>=14 vs Spec=8) and field counts (TDD>=19 vs Spec=13) | `phase-outputs/test-results/phase6-extraction-comparison.md` | Side-by-side table |
| 6.2 | TDD leak check: grep 6 TDD sections + 1 TDD field in spec extraction | `phase-outputs/test-results/phase6-tdd-leak-check.md` | All 7 grep counts = 0 |
| 6.2a | Compare anti-instinct results | `phase-outputs/test-results/phase6-anti-instinct-comparison.md` | Both >=0.7, both obligations/contracts==0 |
| 6.3 | Compare fidelity prompt language | `phase-outputs/test-results/phase6-fidelity-comparison.md` | Both use "source-document fidelity analyst" |
| 6.4 | Compare pipeline completion (step-by-step from .roadmap-state.json) | `phase-outputs/test-results/phase6-pipeline-comparison.md` | Step, Test1 Status, Test2 Status, Expected, Match |
| 6.5 | Final verification report | `.dev/test-fixtures/results/verification-report-modified-repo.md` | Executive Summary, Test 1/2 tables, Comparison, Success Criteria Checklist (11 items), Known Issues, Findings |

### Phase 7: Completion (3 items, Lines 187-196)

> **Purpose:** Update task status and confirm all deliverables in place.

| Item | Summary | Output Path | Checks |
|------|---------|-------------|--------|
| 7.1 | Verify all deliverables exist (5 key files) | (logs to task) | All present |
| 7.2 | Write consolidated follow-up action items | `phase-outputs/reports/follow-up-action-items.md` | Bugs Found, Known Issues Confirmed, Unexpected Behaviors, Deferred Work, Next Steps |
| 7.3 | Update YAML status to done | (modifies self) | status=done, updated_date set |

---

## 6. Task Log Structure (Lines 199-260)

The Task Log at the bottom of the task file contains these sections:

### 6.1 Execution Log Table
```
| Timestamp | Phase | Item | Status | Notes |
```

### 6.2 Phase Findings Tables (one per phase, Phases 1-7)
```
| Item | Finding | Severity | Resolution |
```

Severity values used: CRITICAL, IMPORTANT, MINOR
Special value for no-findings phases: `_No findings yet._` or prose "All deliverables confirmed."

### 6.3 Open Questions Table
```
| ID | Question | Status | Resolution |
```
IDs use format: B-1, TS-1, FP-1 (bug/issue shortcodes)
Status values: EXPECTED, OPEN, MITIGATED

### 6.4 Deferred Work Items Table
```
| Item | Rationale | Dependency |
```

---

## 7. Output Directory Structure

```
.dev/tasks/to-do/TASK-RF-20260326-e2e-modified/
  phase-outputs/
    discovery/
    test-results/
      phase1-prereq-check.md
      phase2-tdd-sentinel-check.md
      phase2-spec-sentinel-check.md
      phase3-tdd-dryrun.md
      phase3-spec-dryrun.md
      phase3-dryrun-comparison.md
      phase3-go-nogo.md
      phase4-tdd-pipeline-log.md
      phase4-extraction-frontmatter.md
      phase4-extraction-sections.md
      phase4-roadmap-variants.md
      phase4-diff-analysis.md
      phase4-debate-transcript.md
      phase4-base-selection.md
      phase4-merged-roadmap.md
      phase4-anti-instinct.md
      phase4-test-strategy.md
      phase4-spec-fidelity.md
      phase4-wiring-verification.md
      phase4-state-file.md
      phase5-spec-pipeline-log.md
      phase5-extraction-frontmatter.md
      phase5-extraction-sections.md
      phase5-merged-roadmap.md
      phase5-anti-instinct.md
      phase5-spec-fidelity.md
      phase5-pipeline-status.md
      phase6-extraction-comparison.md
      phase6-tdd-leak-check.md
      phase6-anti-instinct-comparison.md
      phase6-fidelity-comparison.md
      phase6-pipeline-comparison.md
    reports/
      test1-tdd-summary.md
      test2-spec-summary.md
      follow-up-action-items.md
    reviews/
  research/
    01-pipeline-data-flow.md
    02-template-structure.md
    03-gate-verification.md
    04-task-patterns.md

.dev/test-fixtures/
  test-tdd-user-auth.md
  test-spec-user-auth.md
  results/
    test1-tdd-modified/
      extraction.md
      roadmap-opus-architect.md
      roadmap-haiku-architect.md
      diff-analysis.md
      debate-transcript.md
      base-selection.md
      roadmap.md
      anti-instinct-audit.md
      test-strategy.md
      spec-fidelity.md
      wiring-verification.md
      .roadmap-state.json
    test2-spec-modified/
      (same artifacts)
    verification-report-modified-repo.md
```

---

## 8. Known Issues from Completed Run (Phase Findings Summary)

These become **expected behaviors** in the new PRD pipeline E2E task:

### 8.1 Anti-Instinct Gate is Primary Blocker (Pre-existing)
- **Test 1 (TDD)**: `undischarged_obligations=5` (skeleton pattern refs), `uncovered_contracts=4`. fingerprint_coverage=0.76 PASSES.
- **Test 2 (Spec)**: `uncovered_contracts=3` (middleware_chain). fingerprint_coverage=0.72 PASSES.
- **Impact**: Both pipelines halt at anti-instinct, skipping test-strategy and spec-fidelity steps.
- **For PRD task**: Expect same behavior. PRD pipeline will likely also halt at anti-instinct. Design test items to verify extraction and through-merge artifacts, with anti-instinct as an expected failure point.

### 8.2 `uv run superclaude` Required (Not Bare `superclaude`)
- pipx binary is older version without dev changes
- All pipeline runs MUST use `uv run superclaude`

### 8.3 Click stderr Swallowed in Dry-Run
- Auto-detection messages (`click.echo(..., err=True)`) not visible in dry-run output
- Detection still works; display-only bug

### 8.4 detect_input_type() Threshold Was Fixed During This Run
- Original threshold >=3 was too low (spec with 12 numbered headings scored 6-8)
- Fixed to >=5 with revised signal weights
- **For PRD task**: Need to verify PRD documents trigger correct detection (probably "spec" unless PRD has its own path)

### 8.5 Known Bugs Not Reached
- B-1: DEVIATION_ANALYSIS_GATE TDD field mismatch — never reached (post-pipeline step)
- TS-1: TEST_STRATEGY_GATE prompt/gate mismatch (6 vs 9 fields) — skipped due to anti-instinct halt
- FP-1: Fingerprint empty-set passthrough — mitigated (both fixtures had real fingerprints)

---

## 9. Verification Report Success Criteria Checklist (from verification-report-modified-repo.md)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | TDD auto-detected | YES | dry-run detected "tdd", extraction has TDD fields |
| 2 | 14-section extraction produced | YES | 14 H2 headings in Test 1 extraction |
| 3 | 6 TDD-specific fields present | YES | data_models=2, api_surfaces=4, etc. |
| 4 | Roadmap references TDD content | YES | 7/9 TDD identifiers found in roadmap |
| 5 | All gates pass through merge | YES | Steps 1-7 all PASS for both tests |
| 6 | Anti-instinct passes | NO | Pre-existing issue, both tests fail |
| 7 | Spec auto-detected | YES | dry-run detected "spec", extraction_mode=standard |
| 8 | Standard 8-section extraction | YES | 8 H2 headings in Test 2 extraction |
| 9 | No TDD content leaks | YES | 0/6 TDD fields, 0/6 TDD sections in spec |
| 10 | Full pipeline completes for spec | NO | Halted at anti-instinct (pre-existing) |
| 11 | No Python errors | YES | No tracebacks in either pipeline log |

**Result: 9/11 criteria met. 2 failures are pre-existing.**

---

## 10. Verification Report Artifact Tables (for comparison baseline)

### Test 1 Pass/Fail Summary
| Result | Count | Items |
|--------|-------|-------|
| PASS | 12 | extraction frontmatter, extraction sections, 2x roadmap variants, diff, debate, score, merged roadmap, fingerprint_coverage, wiring, state file |
| FAIL | 2 | anti-instinct undischarged_obligations=5, anti-instinct uncovered_contracts=4 |
| SKIPPED | 2 | test-strategy, spec-fidelity (halted at anti-instinct) |

### Test 2 Pass/Fail Summary
| Result | Count | Items |
|--------|-------|-------|
| PASS | 8 | extraction frontmatter (13 standard), extraction TDD-absent (0/6), extraction sections (8), TDD sections absent (0/6), merged roadmap, fingerprint_coverage=0.72, obligations=0 |
| FAIL | 1 | anti-instinct uncovered_contracts=3 |
| SKIPPED | 1 | spec-fidelity (halted at anti-instinct) |

---

## 11. Structural Patterns for Cloning

### Item Writing Pattern
Each item follows this structure:
```
- [x] **N.M** <action verb> <what to do> by <method>. Check/verify <criteria>. Write results to `<output-path>`. If <failure condition>, log in Phase N Findings section of Task Log at bottom of this task file, then mark this item complete. Once done, mark this item as complete.
```

### Key Patterns to Preserve in Clone:
1. Every item has explicit output file path
2. Every item has failure logging instructions pointing to Task Log
3. Phase blockquotes describe purpose + handoff input
4. Items reference specific files by absolute path within repo
5. Verification items use specific grep commands with expected counts
6. Pipeline run items use `set -o pipefail && uv run superclaude ... 2>&1 | tee <log>; echo "EXIT_CODE=$?"`
7. Summary items compile from all `phase-outputs/test-results/phaseN-*.md` files
8. Comparison items read from both test result dirs side-by-side

### Clone Checklist:
- [ ] Replace all checkbox `[x]` with `[ ]`
- [ ] Replace TDD/spec fixture paths with PRD fixture paths
- [ ] Replace test1-tdd-modified/test2-spec-modified with PRD test result dirs
- [ ] Replace TDD-specific field names with PRD-specific field names
- [ ] Replace TDD section names with PRD section names
- [ ] Update known issues to include anti-instinct as expected failure
- [ ] Add PRD-specific test scenarios (researcher-02 provides these)
- [ ] Update fixture creation items to use PRD template (researcher-03 provides spec)
- [ ] Update or remove tasklist generation items based on researcher-04 findings
