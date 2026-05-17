# BUILD REQUEST: Pipeline Quality Comparison — PRD/TDD vs Spec-Only Baseline (Full Pipeline)

## GOAL

Build a task file that answers the fundamental question: **Does the PRD/TDD-enriched pipeline produce objectively better output than the original spec-only pipeline?**

This compares the COMPLETE pipeline output (roadmap + generated tasklist + tasklist validation) across three pipeline configurations:
1. **Spec-only baseline** (original repo, master branch) — the original pipeline before any TDD/PRD integration
2. **Spec+PRD enriched** (current branch) — spec input with PRD supplementary enrichment
3. **TDD+PRD enriched** (current branch) — TDD input with PRD supplementary enrichment

All three runs used the same "User Authentication Service" feature. The spec fixture is identical across all runs. The enriched runs add TDD and/or PRD supplementary documents.

**This is NOT a regression test.** This is a quality assessment measuring whether TDD/PRD enrichment produces measurably better pipeline output across every stage: extraction, roadmap, tasklist generation, and tasklist validation.

## WHY

We invested significant effort integrating PRD and TDD documents into the roadmap and tasklist pipelines. We've verified the integration *works* (E2E tests pass, PRD/TDD content appears in outputs, no regressions). But we have never measured whether the output is actually *better*. "It works" is not the same as "it's an improvement." This task provides the evidence.

Without this comparison, we cannot:
- Justify the PRD/TDD integration work to stakeholders
- Know which enrichment dimensions (personas, metrics, compliance, technical depth) actually improve output quality
- Identify which pipeline stages benefit most from enrichment vs which are unaffected
- Set a quality bar for future pipeline enhancements
- Know whether TDD enrichment, PRD enrichment, or both together produces the most value

## PREREQUISITES

**All three result sets exist on disk. DO NOT regenerate any of them.**

| Run | Description | Output Directory | Roadmap | Tasklist | Status |
|-----|------------|------------------|---------|----------|--------|
| **Run A: Spec-only baseline** | Original repo (master), spec fixture only | `.dev/test-fixtures/results/test3-spec-baseline/` | `roadmap.md` EXISTS | `tasklist-index.md` + 5 phase files EXISTS | **EXISTS** |
| **Run B: Spec+PRD enriched** | Current branch, spec + PRD fixtures | `.dev/test-fixtures/results/test2-spec-prd-v2/` | `roadmap.md` EXISTS | May not exist yet — depends on E2E task Phase 6 completing | **PARTIAL** |
| **Run C: TDD+PRD enriched** | Current branch, TDD + PRD fixtures | `.dev/test-fixtures/results/test1-tdd-prd-v2/` | `roadmap.md` EXISTS | `tasklist-index.md` + 3 phase files EXISTS | **EXISTS** |

**NOTE on Run B tasklist:** The E2E task (`TASK-E2E-20260403-full-pipeline`) generates tasklists in Phases 5-6. Phase 5 (TDD+PRD tasklist) is complete. Phase 6 (Spec+PRD tasklist) may not have run yet. If `.dev/test-fixtures/results/test2-spec-prd-v2/tasklist-index.md` does not exist when this task executes, handle gracefully: compare roadmap-level metrics for Run B but mark tasklist-level metrics as "N/A — tasklist not yet generated" rather than blocking the entire comparison.

**Existing fixtures (DO NOT recreate):**
- `.dev/test-fixtures/test-tdd-user-auth.md` — TDD fixture (876 lines)
- `.dev/test-fixtures/test-spec-user-auth.md` — Spec fixture (312 lines)
- `.dev/test-fixtures/test-prd-user-auth.md` — PRD fixture (406 lines)

**Prior comparison data (READ-ONLY reference, may be stale):**
- `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/reports/` — latest E2E reports
- `.dev/tasks/to-do/TASK-E2E-20260402-prd-pipeline-rerun/phase-outputs/reports/` — prior E2E reports

## SCOPE — 8 Dimensions

### Dimension 1: Extraction Quality

Compare `extraction.md` across all three runs.

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Frontmatter field count | Count YAML fields | More fields = richer structured metadata |
| Body section count | Count `## ` headers | More sections = broader coverage |
| Functional requirements extracted | `functional_requirements` field value | Core pipeline metric |
| Non-functional requirements extracted | `nonfunctional_requirements` field value | NFRs often lost in spec-only |
| Risks identified | `risks_identified` field value | Risk coverage = planning quality |
| Dependencies identified | `dependencies_identified` field value | Dependency tracking |
| Success criteria count | `success_criteria_count` field value | Acceptance criteria completeness |
| Data models identified (TDD+PRD only) | `data_models_identified` field value | Technical depth from TDD |
| API surfaces identified (TDD+PRD only) | `api_surfaces_identified` field value | Technical specificity from TDD |
| Persona references | `grep -c 'Alex\|Jordan\|Sam\|persona\|Persona'` | PRD enrichment signal |
| Business metric references | `grep -c 'conversion\|latency\|session.*duration\|registration.*rate'` | PRD enrichment signal |
| Compliance references | `grep -c 'GDPR\|SOC2\|compliance\|Compliance'` | PRD enrichment signal |

**Expected:** TDD+PRD highest, Spec+PRD middle, Spec-only baseline lowest.

### Dimension 2: Roadmap Quality

Compare `roadmap.md` across all three runs.

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Total line count | `wc -l` | Comprehensiveness proxy |
| Milestone count | Count `### ` or milestone headers | Planning granularity |
| Technical identifier coverage | Count backticked names (UserProfile, AuthToken, AuthService, etc.) | Technical specificity |
| Persona references in milestones | `grep -c 'Alex\|Jordan\|Sam\|persona\|end user\|admin\|API consumer'` | Business alignment |
| Business metric traceability | `grep -c 'conversion\|latency\|p95\|session.*duration\|KPI\|metric'` | Measurable outcomes |
| Compliance milestones | `grep -c 'GDPR\|SOC2\|compliance\|audit\|consent'` | Regulatory coverage |
| Phase/epic count | Count top-level phases | Planning structure |
| Risk mitigation items | `grep -c 'risk\|Risk\|mitigation\|fallback\|rollback'` | Defensive planning |
| Testing milestones | `grep -c 'test\|Test\|QA\|validation\|verification'` | Quality coverage |

**Qualitative assessment** (read the roadmaps, not just counts):
- Does TDD+PRD roadmap order milestones by business value?
- Does TDD+PRD roadmap include concrete acceptance criteria per milestone?
- Does spec-only roadmap have vague "complete feature X" milestones?
- Does PRD enrichment produce business rationale alongside technical milestones?

### Dimension 3: Anti-Instinct / Fingerprint Fidelity

Compare `anti-instinct-audit.md` across all three runs.

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| `fingerprint_coverage` | Read from YAML | Roadmap fidelity to input |
| Total fingerprints extracted | Count from audit | Traceability depth |
| Fingerprints found in roadmap | Count from audit | Coverage quality |
| `undischarged_obligations` | Read from YAML | Completeness |
| `uncovered_contracts` | Read from YAML | Faithfulness |
| Gate PASS/FAIL | Read from audit | Ultimate gate |

**Key question:** Does PRD enrichment help or hurt fingerprint coverage?

### Dimension 4: Spec-Fidelity Quality

Compare `spec-fidelity.md` across runs where it exists (may be SKIPPED due to anti-instinct halt in all runs).

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| `high_severity_count` | Read from YAML | Spec adherence |
| `validation_complete` | Read from YAML | Completion |
| Comparison dimensions count | Count dimension headers | Validation thoroughness |
| PRD dimensions (12-15) | `grep -c 'Persona Coverage\|Business Metric\|Compliance.*Legal\|Scope Boundary'` | PRD enrichment |
| TDD dimensions (7-11) | `grep -c 'API Endpoints\|Component Inventory\|Testing Strategy\|Migration.*Rollout\|Operational Readiness'` | TDD enrichment |

### Dimension 5: Test Strategy Quality

Compare `test-strategy.md` across runs where it exists (may be SKIPPED).

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Test categories count | Count major test type headers | Comprehensiveness |
| Persona-based test scenarios | `grep -c 'Alex\|Jordan\|Sam\|persona\|user journey'` | PRD enrichment |
| Compliance test category | `grep -c 'GDPR\|SOC2\|compliance test\|audit test'` | PRD enrichment |
| Edge cases from PRD | `grep -c 'brute force\|expired.*session\|duplicate.*email\|concurrent'` | PRD S23 edge cases |
| KPI validation tests | `grep -c 'conversion.*rate\|latency.*target\|session.*duration\|KPI'` | PRD metrics |

### Dimension 6: Tasklist Validation Fidelity (with Real Tasklists)

Compare tasklist fidelity reports. The enriched runs validated against REAL tasklists (generated in E2E Phases 5-6). The baseline may also have a fidelity report.

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Supplementary TDD validation block | Present/absent | TDD enrichment in validation |
| Supplementary PRD validation block | Present/absent | PRD enrichment in validation |
| TDD validation checks count | Count items in TDD section | TDD validation depth |
| PRD validation checks count | Count items in PRD section | PRD validation depth |
| Deviation count by severity | Read from frontmatter | Validation quality |
| `validation_complete` | Read from YAML | Did validation complete? |
| `tasklist_ready` | Read from YAML | Is tasklist ready for sprint? |

**Expected:** Baseline has NO supplementary sections (old code). TDD+PRD has TDD (5 checks) + PRD (4 checks). Spec+PRD has PRD (4 checks) only.

### Dimension 7: Tasklist Generation Quality (NEW)

Compare the GENERATED TASKLIST content across all three runs. This is the critical new dimension that was completely missing from prior comparisons.

| Metric | How to Measure | Why It Matters |
|--------|---------------|----------------|
| Total tasks generated | Count `### T` headers across all phase files | Planning granularity |
| Phase count | Count phase files | Planning structure |
| Deliverable count | Count `D-####` in tasklist-index.md | Output specificity |
| Data model tasks | `grep -c 'UserProfile\|AuthToken\|schema\|data model'` across phase files | TDD §7 enrichment |
| API endpoint tasks | `grep -c '/auth/login\|/auth/register\|/auth/refresh\|/auth/me\|/auth/logout\|/auth/reset'` across phase files | TDD §8 enrichment |
| Component implementation tasks | `grep -c 'AuthService\|PasswordHasher\|TokenManager\|JwtService\|UserRepo'` across phase files | TDD §10 enrichment |
| Test artifact references | `grep -c 'UT-001\|IT-001\|E2E-001'` across phase files | TDD §15 enrichment |
| Rollout/migration tasks | `grep -c 'rollback\|rollout\|migration\|feature flag\|AUTH_NEW_LOGIN\|AUTH_TOKEN_REFRESH'` | TDD §19 enrichment |
| Persona references in tasks | `grep -c 'Alex\|Jordan\|Sam\|persona'` across phase files | PRD S7 enrichment |
| Compliance tasks | `grep -c 'GDPR\|SOC2\|compliance\|consent\|audit'` across phase files | PRD S17 enrichment |
| Success metric references | `grep -c 'conversion\|> 60%\|< 200ms\|99.9%\|> 30 min\|> 80%'` across phase files | PRD S19 enrichment |
| Customer journey verification tasks | `grep -c 'journey\|acceptance\|scenario\|signup\|login flow\|password reset flow'` across phase files | PRD S22 enrichment |
| Acceptance criteria specificity | Sample 5 tasks per run: count criteria referencing specific artifacts vs generic "it works" | Quality of task definition |

**Expected:**
- Baseline (spec-only): Generic tasks, no TDD component names, no PRD personas/compliance/metrics
- Spec+PRD: PRD enrichment present (personas, compliance, metrics) but no TDD detail (no component names, no test IDs)
- TDD+PRD: Maximum enrichment — TDD component names, API endpoints, test IDs, data models AND PRD personas, compliance, metrics

This dimension answers: **"Does the generated tasklist actually contain richer, more actionable content when TDD/PRD enrichment is provided?"**

### Dimension 8: Cross-Stage Enrichment Flow

Trace whether enrichment that appears in extraction also flows through to roadmap, then to tasklist, then to validation. This measures enrichment PERSISTENCE across pipeline stages.

| Enrichment Element | In Extraction? | In Roadmap? | In Tasklist? | In Validation? |
|-------------------|---------------|-------------|-------------|---------------|
| Persona Alex | Check | Check | Check | Check |
| Persona Jordan | Check | Check | Check | Check |
| Persona Sam | Check | Check | Check | Check |
| GDPR compliance | Check | Check | Check | Check |
| SOC2 compliance | Check | Check | Check | Check |
| Success metrics (>60%, <200ms) | Check | Check | Check | Check |
| Component names (AuthService, etc.) | Check | Check | Check | N/A (spec path) |
| Data models (UserProfile, AuthToken) | Check | Check | Check | N/A (spec path) |
| Test IDs (UT-001, etc.) | Check | Check | Check | N/A (spec path) |

For each element, grep across extraction.md, roadmap.md, all phase-*-tasklist.md files, and tasklist-fidelity.md. An element that appears in extraction but disappears in the tasklist indicates enrichment is being LOST during generation.

**Expected:** TDD+PRD should show full persistence across all stages. Any enrichment that appears in extraction but not in the tasklist is a gap.

## PHASES

### Phase 1: Prerequisite Verification (3 items)
- Verify all three result directories exist and contain the expected artifacts
- Catalog which artifacts exist in each directory (roadmap, extraction, anti-instinct, tasklist-index, phase files, fidelity report)
- If Run B tasklist doesn't exist, note as limitation but proceed with roadmap-level comparison

### Phase 2: Quantitative Data Collection (8 items)
- For each of the 8 dimensions, collect all metrics from all available runs
- Write raw data to structured markdown tables — one file per dimension
- Use `grep -c`, `wc -l`, YAML field reads — no subjective assessment yet
- Handle missing artifacts gracefully ("N/A — anti-instinct halted" or "N/A — tasklist not generated")

### Phase 3: Qualitative Assessment (4 items)
- Read actual roadmap and tasklist content from all three runs
- Assess milestone ordering, specificity, acceptance criteria quality, business alignment
- Assess tasklist task quality: are TDD+PRD tasks more specific and actionable than baseline tasks?
- Write qualitative findings with specific examples quoted from each run

### Phase 4: Cross-Pipeline Quality Matrix (3 items)
- Build master comparison matrix combining all 8 dimensions
- Calculate enrichment deltas: (TDD+PRD) minus (Baseline) and (Spec+PRD) minus (Baseline) for each metric
- Identify which dimensions show largest improvement and which show no change or regression

### Phase 5: Verdict and Report (3 items)
- Write final quality comparison report at `.dev/test-fixtures/results/quality-comparison-prd-tdd-vs-spec.md`
- **Executive verdict**: Is the PRD/TDD pipeline objectively better? By how much? In which dimensions?
- **Enrichment ROI by source**: Does TDD enrichment, PRD enrichment, or both together contribute most?
- **Tasklist quality verdict**: Do enriched tasklists contain materially more actionable content?
- **Enrichment persistence**: Does enrichment flow through all pipeline stages or get lost?
- **Regression check**: Did any dimension get WORSE with enrichment?
- **Recommendations**: Which enrichment combinations should be the default pipeline configuration?
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
| Dimension 7 data (tasklist generation) | `phase-outputs/data/dim7-tasklist-generation-comparison.md` |
| Dimension 8 data (enrichment flow) | `phase-outputs/data/dim8-enrichment-flow-comparison.md` |
| Qualitative assessment | `phase-outputs/reports/qualitative-assessment.md` |
| Master quality matrix | `phase-outputs/reports/quality-matrix.md` |
| **Final quality comparison report** | `.dev/test-fixtures/results/quality-comparison-prd-tdd-vs-spec.md` |

## QA FOCUS GUIDANCE

**QA gates MUST focus on whether the comparison accurately reflects actual pipeline output — NOT on report prose quality.**

What QA should verify:
- Do the metric values in comparison tables match the actual files they claim to measure?
- Are grep counts accurate against the actual artifact files?
- Does the verdict follow logically from the data collected?
- Are any claims made without supporting evidence?

What QA should NOT spend time on:
- Whether prose summaries are well-written
- Whether section cross-references are correct
- Formatting consistency

## TEMPLATE

02 (complex — 8-dimensional analysis, cross-run comparison, quantitative + qualitative, blocking dependencies)

## CONTEXT FILES

| File | Why |
|------|-----|
| `.dev/test-fixtures/results/test3-spec-baseline/` | **Run A** — spec-only baseline (roadmap + tasklist + all artifacts) |
| `.dev/test-fixtures/results/test2-spec-prd-v2/` | **Run B** — spec+PRD enriched (roadmap exists, tasklist may not yet) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/` | **Run C** — TDD+PRD enriched (roadmap + tasklist + all artifacts) |
| `.dev/test-fixtures/results/test1-tdd-modified/` | Prior TDD-only run (reference for TDD-without-PRD comparison if useful) |
| `.dev/test-fixtures/results/test2-spec-modified/` | Prior spec-only run on modified branch (reference) |
| `.dev/tasks/to-do/TASK-RF-20260403-full-e2e/phase-outputs/` | Latest E2E reports |
| `.dev/tasks/to-do/TASK-RF-20260403-tasklist-e2e/research/` | Tasklist subsystem research |

## DEPENDENCY CHAIN

```
TASK-E2E-20260403-full-pipeline (enriched E2E)  ──┐
  - test1-tdd-prd-v2/ (roadmap + tasklist)         │
  - test2-spec-prd-v2/ (roadmap + maybe tasklist)  ├──→ THIS TASK (quality comparison)
                                                    │         ↓
Baseline task (already completed)  ────────────────┘   Final verdict:
  - test3-spec-baseline/ (roadmap + tasklist)           Is PRD/TDD better?
```

This task can execute as soon as the enriched E2E task has produced roadmap artifacts for both tests. Tasklist-level comparison for Run B is optional (if tasklist doesn't exist, skip those metrics for Run B).
