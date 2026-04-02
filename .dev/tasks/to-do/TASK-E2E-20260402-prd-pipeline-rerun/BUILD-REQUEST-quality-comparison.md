# BUILD REQUEST: Pipeline Quality Comparison — PRD/TDD vs Spec-Only Baseline

## GOAL

Build a task file that answers the fundamental question: **Does the PRD/TDD-enriched pipeline produce objectively better output than the original spec-only pipeline?**

This is not a regression test (that's Test 2 vs Test 3). This is a quality assessment: given the same feature ("User Authentication Service"), does feeding a TDD + PRD through the updated pipeline produce a roadmap, test strategy, fidelity report, and tasklist validation that is more complete, more specific, and more business-aligned than what the original spec-only pipeline produced?

## WHY

We invested significant effort integrating PRD and TDD documents into the roadmap pipeline. We've verified the integration *works* (E2E tests pass, PRD content appears in outputs, no regressions). But we have never measured whether the output is actually *better*. "It works" is not the same as "it's an improvement." This task provides the evidence.

Without this comparison, we cannot:
- Justify the PRD/TDD integration work to stakeholders
- Know which enrichment dimensions (personas, metrics, compliance, technical depth) actually improve output quality
- Identify which pipeline stages benefit most from enrichment vs which are unaffected
- Set a quality bar for future pipeline enhancements

## PREREQUISITES

This task requires pipeline output artifacts from multiple prior runs. **All four result sets must exist before this task can execute.**

| Run | Source Task | Output Directory | Status |
|-----|-----------|------------------|--------|
| **Run A: Spec-only baseline** | `BUILD-REQUEST-baseline-repo.md` → task TBD | `.dev/test-fixtures/results/test3-spec-baseline/` | **BLOCKING — must be built and executed first** |
| **Run B: Spec+PRD enriched** | `TASK-E2E-20260402-prd-pipeline-rerun` Phase 5 | `.dev/test-fixtures/results/test2-spec-prd/` (or rerun equivalent) | Depends on rerun completion |
| **Run C: TDD-only** | `TASK-E2E-20260326-modified-repo` Phase 4 | `.dev/test-fixtures/results/test1-tdd-modified/` | EXISTS |
| **Run D: TDD+PRD enriched** | `TASK-E2E-20260402-prd-pipeline-rerun` Phase 4 | `.dev/test-fixtures/results/test1-tdd-prd/` (or rerun equivalent) | Depends on rerun completion |

**If Run A does not exist yet**, Phase 1 of this task must block and document the dependency. Do not fabricate or approximate baseline results.

## SCOPE

### Dimension 1: Extraction Quality

Compare `extraction.md` across all four runs. Measure:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Frontmatter field count | Count YAML fields | More fields = richer structured metadata for downstream consumers |
| Body section count | Count `## ` headers | More sections = broader coverage of the input document |
| Functional requirements extracted | `functional_requirements` field value | Core pipeline metric — are we capturing more requirements? |
| Non-functional requirements extracted | `nonfunctional_requirements` field value | NFRs often lost in spec-only extraction |
| Risks identified | `risks_identified` field value | Risk coverage = planning quality |
| Dependencies identified | `dependencies_identified` field value | Dependency tracking = execution quality |
| Success criteria count | `success_criteria_count` field value | Acceptance criteria completeness |
| Data models identified (TDD paths only) | `data_models_identified` field value | Technical depth from TDD |
| API surfaces identified (TDD paths only) | `api_surfaces_identified` field value | Technical specificity from TDD |
| Persona references | `grep -c 'Alex\|Jordan\|Sam\|persona\|Persona'` | PRD enrichment signal |
| Business metric references | `grep -c 'conversion\|latency\|session.*duration\|registration.*rate'` | PRD enrichment signal |
| Compliance references | `grep -c 'GDPR\|SOC2\|compliance\|Compliance'` | PRD enrichment signal |

**Expected outcome**: TDD+PRD should score highest across all dimensions. Spec-only baseline should score lowest. The delta quantifies enrichment value.

### Dimension 2: Roadmap Quality

Compare `roadmap.md` across all four runs. Measure:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Total line count | `wc -l` | Proxy for comprehensiveness |
| Milestone count | Count `### ` or milestone headers | More milestones = finer-grained planning |
| Technical identifier coverage | Count backticked identifiers (`UserProfile`, `AuthToken`, etc.) | Technical specificity — does the roadmap reference actual implementation artifacts? |
| Persona references in milestones | `grep -c 'Alex\|Jordan\|Sam\|persona\|end user\|admin\|API consumer'` | Business alignment — are milestones tied to user value? |
| Business metric traceability | `grep -c 'conversion\|latency\|p95\|session.*duration\|KPI\|metric'` | Are milestones tied to measurable outcomes? |
| Compliance milestones | `grep -c 'GDPR\|SOC2\|compliance\|audit\|consent'` | Regulatory coverage |
| Phase/epic structure | Count top-level phases or epics | Planning granularity |
| Risk mitigation items | `grep -c 'risk\|Risk\|mitigation\|fallback\|rollback'` | Defensive planning quality |
| Testing milestones | `grep -c 'test\|Test\|QA\|validation\|verification'` | Quality assurance coverage |

**Qualitative assessment** (must be performed by reading the roadmaps, not just counting):
- Does the TDD+PRD roadmap order milestones by business value (user-facing first, infrastructure second)?
- Does the spec-only roadmap order milestones more generically?
- Does the TDD+PRD roadmap include concrete acceptance criteria per milestone?
- Does the spec-only roadmap have vague "complete feature X" milestones?

### Dimension 3: Anti-Instinct / Fingerprint Fidelity

Compare `anti-instinct-audit.md` across all four runs. Measure:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| `fingerprint_coverage` | Read from YAML | Does the roadmap faithfully represent the input document's technical content? |
| Total fingerprints extracted | Count from audit | More fingerprints = richer technical traceability |
| Fingerprints found in roadmap | Count from audit | Higher found = better roadmap fidelity |
| `undischarged_obligations` | Read from YAML | Fewer = more complete roadmap |
| `uncovered_contracts` | Read from YAML | Fewer = more faithful roadmap |
| Gate PASS/FAIL | Read from audit | Ultimate quality gate |

**Key question**: Does PRD enrichment help or hurt fingerprint coverage? The original run showed a regression (0.76 → 0.69). Has this been fixed by QA?

### Dimension 4: Spec-Fidelity Quality

Compare `spec-fidelity.md` across runs where it exists. Measure:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| `high_severity_count` | Read from YAML | Fewer high-severity = better spec adherence |
| `validation_complete` | Read from YAML | Did fidelity check complete? |
| Comparison dimensions count | Count dimension headers | More dimensions = more thorough validation |
| PRD dimensions present (12-15) | `grep -c 'Persona Coverage\|Business Metric\|Compliance.*Legal\|Scope Boundary'` | PRD enrichment produces additional fidelity checks |
| TDD dimensions present | `grep -c 'API Endpoints\|Component Inventory\|Testing Strategy\|Migration.*Rollout\|Operational Readiness'` | TDD enrichment produces additional fidelity checks |

### Dimension 5: Test Strategy Quality

Compare `test-strategy.md` across runs where it exists. Measure:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Test categories count | Count major test type headers | More categories = more comprehensive testing plan |
| Persona-based test scenarios | `grep -c 'Alex\|Jordan\|Sam\|persona\|user journey'` | PRD enrichment should produce persona-driven acceptance tests |
| Compliance test category | `grep -c 'GDPR\|SOC2\|compliance test\|audit test'` | PRD enrichment should produce compliance-specific tests |
| Edge cases from PRD | `grep -c 'brute force\|expired.*session\|duplicate.*email\|concurrent'` | PRD S23 edge cases should flow through to test strategy |
| KPI validation tests | `grep -c 'conversion.*rate\|latency.*target\|session.*duration\|KPI'` | PRD success metrics should generate KPI validation tests |

### Dimension 6: Tasklist Validation Enrichment

Compare tasklist fidelity reports across enriched vs baseline runs. Measure:

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Supplementary TDD validation block | Present/absent | TDD enrichment produces additional validation checks |
| Supplementary PRD validation block | Present/absent | PRD enrichment produces additional validation checks |
| PRD validation checks (persona, metrics, scenarios) | Count individual checks | Quantify PRD validation depth |
| TDD validation checks (test cases, rollback, components) | Count individual checks | Quantify TDD validation depth |
| Total validation severity items | Count by severity | More checks at appropriate severity = better quality gate |

## PHASES

### Phase 1: Prerequisite Verification (3 items)
- Verify all four result directories exist and contain the expected artifacts
- If Run A (spec-only baseline) does not exist, document as BLOCKING dependency and halt — do not proceed without the baseline
- Catalog which artifacts exist in each result directory (some may be missing due to anti-instinct gate halts)

### Phase 2: Quantitative Data Collection (6 items)
- For each of the 6 dimensions above, collect all metrics from all available runs
- Write raw data to structured markdown tables — one file per dimension
- Use `grep -c`, `wc -l`, YAML field reads — no subjective assessment yet
- Handle missing artifacts gracefully (note "N/A — anti-instinct halted pipeline" rather than treating as zero)

### Phase 3: Qualitative Assessment (4 items)
- Read the actual roadmap content (not just counts) from all four runs
- Assess milestone ordering, specificity, acceptance criteria quality, business alignment
- Assess whether PRD personas appear as stakeholder references in roadmap milestones (not just keyword matches)
- Assess whether TDD technical content produces more concrete implementation milestones vs generic "build feature X" items
- Write qualitative findings with specific examples quoted from each roadmap

### Phase 4: Cross-Pipeline Quality Matrix (3 items)
- Build the master comparison matrix combining all quantitative metrics from Phase 2
- Add qualitative ratings (Strong / Moderate / Weak / N/A) per dimension per run
- Calculate enrichment deltas: (TDD+PRD) minus (Spec-only baseline) for each metric
- Identify which dimensions show the largest improvement and which show no change or regression

### Phase 5: Verdict and Report (3 items)
- Write the final quality comparison report at `.dev/test-fixtures/results/quality-comparison-prd-tdd-vs-spec.md`
- **Executive verdict**: Is the PRD/TDD pipeline objectively better? By how much? In which dimensions?
- **Enrichment ROI**: Which enrichment source (PRD, TDD, or both) contributes most to quality improvement?
- **Regression check**: Did any dimension get WORSE with enrichment? (e.g., fingerprint coverage regression from original run)
- **Recommendations**: Based on evidence, which enrichment combinations should be the default pipeline configuration?
- **Evidence table**: Every claim backed by specific metric values from specific runs

## OUTPUT ARTIFACTS

| Artifact | Path |
|----------|------|
| Dimension 1 data (extraction) | `phase-outputs/data/dim1-extraction-comparison.md` |
| Dimension 2 data (roadmap) | `phase-outputs/data/dim2-roadmap-comparison.md` |
| Dimension 3 data (anti-instinct) | `phase-outputs/data/dim3-anti-instinct-comparison.md` |
| Dimension 4 data (spec-fidelity) | `phase-outputs/data/dim4-spec-fidelity-comparison.md` |
| Dimension 5 data (test-strategy) | `phase-outputs/data/dim5-test-strategy-comparison.md` |
| Dimension 6 data (tasklist validation) | `phase-outputs/data/dim6-tasklist-validation-comparison.md` |
| Qualitative assessment | `phase-outputs/reports/qualitative-assessment.md` |
| Master quality matrix | `phase-outputs/reports/quality-matrix.md` |
| **Final quality comparison report** | `.dev/test-fixtures/results/quality-comparison-prd-tdd-vs-spec.md` |

## TEMPLATE

02 (complex — multi-dimensional analysis, cross-run comparison, quantitative + qualitative assessment, blocking dependencies)

## CONTEXT FILES

| File | Why |
|------|-----|
| `.dev/test-fixtures/results/test3-spec-baseline/` | Run A artifacts (spec-only baseline) — **must exist** |
| `.dev/test-fixtures/results/test2-spec-prd/` | Run B artifacts (spec+PRD) |
| `.dev/test-fixtures/results/test1-tdd-modified/` | Run C artifacts (TDD-only) |
| `.dev/test-fixtures/results/test1-tdd-prd/` | Run D artifacts (TDD+PRD) |
| `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/TASK-E2E-20260402-prd-pipeline-rerun.md` | Rerun task (produces Runs B and D) |
| `.dev/tasks/to-do/TASK-E2E-20260326-tdd-pipeline/BUILD-REQUEST-baseline-repo.md` | Build request for Run A (baseline) |
| `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/phase-outputs/reports/cross-run-comparison-summary.md` | Prior cross-run comparison (reference, may be stale after QA fixes) |
| `.dev/tasks/to-do/TASK-E2E-20260327-prd-pipeline-e2e/phase-outputs/reports/follow-up-action-items.md` | Known issues and follow-ups from original run |

## DEPENDENCY CHAIN

```
BUILD-REQUEST-baseline-repo.md  →  [task-builder]  →  TASK: Run A (spec-only baseline)
                                                            ↓
TASK-E2E-20260402-prd-pipeline-rerun  →  [execute]  →  Runs B + D (PRD-enriched outputs)
                                                            ↓
                                                    THIS TASK (quality comparison)
                                                            ↓
                                              Final verdict: Is PRD/TDD better?
```

This task CANNOT execute until both the baseline task AND the rerun task have completed.
