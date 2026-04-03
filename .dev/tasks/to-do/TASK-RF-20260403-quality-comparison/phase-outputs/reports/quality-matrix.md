# Quality Matrix -- Pipeline Input Configuration Comparison

**Date:** 2026-04-03
**Runs:**
- Run A: `test3-spec-baseline/` (spec only -- Baseline)
- Run B: `test2-spec-prd-v2/` (spec + PRD)
- Run C: `test1-tdd-prd-v2/` (TDD + PRD)

---

## 4.1 Master Quality Matrix

| # | Dimension | Key Metric | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) | Winner |
|---|-----------|------------|:----------------:|:-----------------:|:----------------:|--------|
| 1 | Extraction Quality | Total requirements extracted | 8 | 11 | 13 | **Run C** |
| 2 | Roadmap Quality | Lines / Convergence score | 380 / 0.62 | 558 / 0.62 | 746 / 0.72 | **Run C** |
| 3 | Anti-Instinct Audit | fingerprint_coverage | 0.72 (13/18) | 0.72 (13/18) | 0.73 (33/45) | **Run C** (marginal) |
| 4 | Spec Fidelity | File produced / deviations | YES / 7 | NO / N/A | NO / N/A | **N/A** (single-run) |
| 5 | Test Strategy | File produced | YES (280 lines) | NO | NO | **N/A** (single-run) |
| 6 | Tasklist Fidelity | File produced / deviations | YES / 5 (0H/2M/3L) | NO / N/A | NO / N/A | **N/A** (single-run) |
| 7 | Tasklist Quality | Enrichment refs (persona+compliance) | 0 + 3 | N/A (no tasklist) | 40 + 40 | **Run C** |
| 8 | Enrichment Flow | Persona amplification (extraction to tasklist) | 0 (absent) | 10->20 (truncated) | 4->11->40 (10x) | **Run C** |

### Win Summary (excluding N/A dimensions)

| Run | Dimensions Won | Dimensions |
|-----|:--------------:|------------|
| **Run A (Baseline)** | 0 | -- |
| **Run B (Spec+PRD)** | 0 | -- |
| **Run C (TDD+PRD)** | 5 | Extraction Quality, Roadmap Quality, Anti-Instinct Audit (marginal), Tasklist Quality, Enrichment Flow |

**N/A dimensions (3):** Spec Fidelity, Test Strategy, Tasklist Fidelity -- only Run A produced these artifacts. Runs B and C did not reach these pipeline steps; no cross-run comparison is possible.

**Note on Dim 3 (Anti-Instinct):** Run C's win is marginal (0.73 vs 0.72). However, Run C audits 2.5x more fingerprints (45 vs 18), so equivalent coverage over a larger surface area represents stronger performance. Run A has the cleanest audit (0 undischarged obligations, 0 uncovered contracts) but against a simpler input set.

**Note on Dim 7 (Tasklist Quality):** Run B produced no tasklist. Run A has more tasks (87 vs 44) but zero enrichment. Run C has fewer but richer tasks with persona, compliance, tier classification, and test ID traceability.

---

## 4.2 Enrichment Delta Analysis

### 4.2.1 Spec+PRD vs Baseline (Run B - Run A)

| Metric | Run A | Run B | Delta (abs) | Delta (%) | Direction |
|--------|:-----:|:-----:|:-----------:|:---------:|:---------:|
| Extraction lines | 302 | 247 | -55 | -18.2% | DECREASE |
| Extraction total requirements | 8 | 11 | +3 | +37.5% | INCREASE |
| Extraction NFRs | 3 | 6 | +3 | +100.0% | INCREASE |
| Extraction risks | 3 | 7 | +4 | +133.3% | INCREASE |
| Extraction domains detected | 2 | 4 | +2 | +100.0% | INCREASE |
| Extraction persona refs | 0 | 10 | +10 | -- | NEW |
| Extraction compliance refs | 0 | 12 | +12 | -- | NEW |
| Roadmap lines | 380 | 558 | +178 | +46.8% | INCREASE |
| Roadmap persona refs | 0 | 20 | +20 | -- | NEW |
| Roadmap compliance refs | 0 | 22 | +22 | -- | NEW |
| Roadmap business metrics | 0 | 7 | +7 | -- | NEW |
| Roadmap convergence score | 0.62 | 0.62 | 0.00 | 0.0% | FLAT |
| Anti-instinct fingerprint_coverage | 0.72 | 0.72 | 0.00 | 0.0% | FLAT |
| Anti-instinct undischarged | 0 | 2 | +2 | -- | INCREASE |
| Anti-instinct uncovered_contracts | 0 | 3 | +3 | -- | INCREASE |
| Tasklist generated | YES | NO | -- | -- | REGRESSION |

**Regression check:** Two regressions detected in Run B vs Run A:
1. **Extraction lines decreased** (-18.2%): Run B produced a shorter extraction despite richer input. The PRD enrichment added content (personas, compliance) but the extraction was more concise overall.
2. **Tasklist not generated**: Run B's pipeline halted after anti-instinct audit (FAIL status with 2 undischarged obligations). This is a pipeline completeness regression -- Run A completed all stages while Run B did not.

### 4.2.2 TDD+PRD vs Baseline (Run C - Run A)

| Metric | Run A | Run C | Delta (abs) | Delta (%) | Direction |
|--------|:-----:|:-----:|:-----------:|:---------:|:---------:|
| Extraction lines | 302 | 660 | +358 | +118.5% | INCREASE |
| Extraction total requirements | 8 | 13 | +5 | +62.5% | INCREASE |
| Extraction NFRs | 3 | 8 | +5 | +166.7% | INCREASE |
| Extraction section count | 8 | 14 | +6 | +75.0% | INCREASE |
| Extraction domains detected | 2 | 5 | +3 | +150.0% | INCREASE |
| Extraction YAML fields | 14 | 21 | +7 | +50.0% | INCREASE |
| Extraction component refs | 12 | 134 | +122 | +1016.7% | INCREASE |
| Extraction persona refs | 0 | 4 | +4 | -- | NEW |
| Extraction compliance refs | 0 | 11 | +11 | -- | NEW |
| Roadmap lines | 380 | 746 | +366 | +96.3% | INCREASE |
| Roadmap component refs | 41 | 111 | +70 | +170.7% | INCREASE |
| Roadmap persona refs | 0 | 11 | +11 | -- | NEW |
| Roadmap compliance refs | 0 | 25 | +25 | -- | NEW |
| Roadmap business metrics | 0 | 7 | +7 | -- | NEW |
| Roadmap convergence score | 0.62 | 0.72 | +0.10 | +16.1% | INCREASE |
| Anti-instinct fingerprint_coverage | 0.72 | 0.73 | +0.01 | +1.4% | INCREASE |
| Anti-instinct fingerprint_total | 18 | 45 | +27 | +150.0% | INCREASE |
| Anti-instinct fingerprint_found | 13 | 33 | +20 | +153.8% | INCREASE |
| Tasklist total tasks | 87 | 44 | -43 | -49.4% | DECREASE |
| Tasklist component refs | 73 | 218 | +145 | +198.6% | INCREASE |
| Tasklist persona refs | 0 | 40 | +40 | -- | NEW |
| Tasklist compliance refs | 0 | 40 | +40 | -- | NEW |
| Tasklist test ID refs | 0 | 8 | +8 | -- | NEW |

**Regression check:** One structural difference (not a quality regression):
1. **Tasklist total tasks decreased** (-49.4%): Run C produces fewer tasks (44 vs 87) but this reflects coarser decomposition, not missing coverage. Run C tasks are richer (3x component density, persona/compliance refs, tier classification). Run C also covers frontend and ops which Run A does not.

No quality regressions detected -- all enriched metrics increase or are newly introduced.

### 4.2.3 TDD+PRD vs Spec+PRD Marginal Delta (Run C - Run B)

This table isolates the marginal contribution of the TDD input by comparing two PRD-enriched runs.

| Metric | Run B | Run C | Marginal Delta | Delta (%) | Direction |
|--------|:-----:|:-----:|:--------------:|:---------:|:---------:|
| Extraction lines | 247 | 660 | +413 | +167.2% | INCREASE |
| Extraction total requirements | 11 | 13 | +2 | +18.2% | INCREASE |
| Extraction NFRs | 6 | 8 | +2 | +33.3% | INCREASE |
| Extraction section count | 8 | 14 | +6 | +75.0% | INCREASE |
| Extraction extra TDD sections | 0 | 6 | +6 | -- | NEW |
| Extraction domains detected | 4 | 5 | +1 | +25.0% | INCREASE |
| Extraction component refs | 16 | 134 | +118 | +737.5% | INCREASE |
| Extraction persona refs | 10 | 4 | -6 | -60.0% | DECREASE |
| Extraction compliance refs | 12 | 11 | -1 | -8.3% | DECREASE |
| Roadmap lines | 558 | 746 | +188 | +33.7% | INCREASE |
| Roadmap persona refs | 20 | 11 | -9 | -45.0% | DECREASE |
| Roadmap compliance refs | 22 | 25 | +3 | +13.6% | INCREASE |
| Roadmap business metrics | 7 | 7 | 0 | 0.0% | FLAT |
| Roadmap convergence score | 0.62 | 0.72 | +0.10 | +16.1% | INCREASE |
| Anti-instinct fingerprint_coverage | 0.72 | 0.73 | +0.01 | +1.4% | INCREASE |
| Anti-instinct fingerprint_total | 18 | 45 | +27 | +150.0% | INCREASE |
| Tasklist generated | NO | YES | -- | -- | IMPROVEMENT |

**Marginal TDD contribution summary:**
- **Structural expansion**: +6 extraction sections (Data Models, API Specs, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness), +6 extraction section headers, +167% extraction lines
- **Component density**: +737.5% component refs at extraction, reflecting TDD's implementation-level detail
- **Convergence improvement**: +16.1% roadmap convergence (0.62 to 0.72), suggesting richer input reduces architectural disagreement
- **Pipeline completion**: TDD+PRD produced a tasklist; Spec+PRD did not

**Marginal regression check -- persona dilution:**
- Extraction persona refs: Run B=10, Run C=4 (-60%)
- Roadmap persona refs: Run B=20, Run C=11 (-45%)

The TDD input appears to dilute persona density in early-stage artifacts. The TDD's technical focus produces more component-centric content, reducing the relative density of PRD-derived persona references. However, Run C's tasklist recovers with 40 persona refs (vs Run B's N/A), demonstrating that persona content persists through the full pipeline even when diluted at extraction.

---

## 4.3 Enrichment Flow Summary

### Stage-Transition Table

This table traces each enrichment category across pipeline stages (extraction -> roadmap -> tasklist) per run.

#### Persona Refs (Alex + Jordan + Sam)

| Transition | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|------------|:----------------:|:-----------------:|:----------------:|
| Extraction | 0 | 10 | 4 |
| Roadmap | 0 | 20 | 11 |
| Tasklist | 0 | N/A (no tasklist) | 40 |
| Extraction -> Roadmap multiplier | -- | 2.0x | 2.75x |
| Roadmap -> Tasklist multiplier | -- | N/A | 3.6x |
| End-to-end multiplier | -- | N/A (truncated) | 10.0x |

#### Compliance Refs (GDPR + SOC2)

| Transition | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|------------|:----------------:|:-----------------:|:----------------:|
| Extraction | 0 | 12 | 11 |
| Roadmap | 0 | 22 | 25 |
| Tasklist | 0 | N/A (no tasklist) | 40 |
| Extraction -> Roadmap multiplier | -- | 1.83x | 2.27x |
| Roadmap -> Tasklist multiplier | -- | N/A | 1.60x |
| End-to-end multiplier | -- | N/A (truncated) | 3.64x |

#### Component Refs

| Transition | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|------------|:----------------:|:-----------------:|:----------------:|
| Extraction | 12 | 16 | 134 |
| Roadmap | 41 | N/A (different set) | 111 |
| Tasklist | 73 | N/A (no tasklist) | 218 |
| Extraction -> Roadmap multiplier | 3.42x | N/A | 0.83x |
| Roadmap -> Tasklist multiplier | 1.78x | N/A | 1.96x |
| End-to-end multiplier | 6.08x | N/A | 1.63x |

#### Business Metrics (revenue + conversion)

| Transition | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|------------|:----------------:|:-----------------:|:----------------:|
| Extraction | 0 | 0 | 0 |
| Roadmap | 0 | 7 | 7 |
| Tasklist | 0 | N/A | Not measured |
| Flow pattern | Absent | Introduced at roadmap | Introduced at roadmap |

### Persistence Score

Persistence Score measures how well enrichment survives from extraction to tasklist: **(tasklist refs / extraction refs)** where both values are available.

| Category | Run A | Run B | Run C |
|----------|:-----:|:-----:|:-----:|
| Persona refs | N/A (0/0) | N/A (no tasklist) | **10.0** (40/4) |
| Compliance refs | N/A (0/0) | N/A (no tasklist) | **3.64** (40/11) |
| Component refs | **6.08** (73/12) | N/A (no tasklist) | **1.63** (218/134) |

**Interpretation:** A persistence score > 1.0 means the pipeline amplifies enrichment signals. Scores < 1.0 indicate attrition. Only Run C has full 3-stage data for all PRD-derived categories. Run A has component data only.

### Sticky vs Lossy Enrichment Categories

| Category | Classification | Evidence |
|----------|:--------------:|----------|
| **Persona refs** | **STICKY (amplifying)** | Run C: 4 -> 11 -> 40 (10x end-to-end). Each stage approximately doubles or triples the count. The pipeline contextualizes persona references into phase-specific and task-specific mentions. Persistence score: 10.0. |
| **Compliance refs** | **STICKY (amplifying)** | Run C: 11 -> 25 -> 40 (3.6x end-to-end). Steady growth at each stage. GDPR and SOC2 references are added per-phase in the roadmap and per-task in the tasklist as compliance requirements are decomposed into actionable items. Persistence score: 3.64. |
| **Component refs** | **MIXED** | Run A: 12 -> 41 -> 73 (6x, sticky). Run C: 134 -> 111 -> 218 (1.6x overall, with a dip at roadmap stage). The extraction-to-roadmap decrease in Run C (134 -> 111) suggests the roadmap narrative consolidates some component mentions. Roadmap-to-tasklist is amplifying (111 -> 218, 1.96x). Classification: sticky overall but with mid-pipeline attrition when extraction density is very high. |
| **Business metrics** | **LOSSY (partial)** | Not present at extraction in any run. Introduced at roadmap stage (7 refs in both B and C). Not measured at tasklist stage for Run C. Business metrics appear to be roadmap-stage introductions rather than extraction-propagated signals. They may not persist into tasklist task-level content. |

### Key Findings

1. **PRD-derived categories (persona, compliance) are strongly sticky** -- they amplify at every pipeline stage, with persistence scores well above 1.0.
2. **Component refs are sticky but show mid-pipeline compression** when extraction density is very high (Run C: 134 -> 111 at roadmap). The roadmap narrative consolidates implementation detail into architectural groupings.
3. **Business metrics are roadmap-stage introductions**, not extraction-propagated. They emerge during the adversarial roadmap merge process when PRD context is available, but are not extracted as structured data.
4. **Run B's truncated pipeline** (no tasklist) prevents measuring full enrichment flow for the Spec+PRD configuration. The extraction-to-roadmap transitions show healthy amplification (2.0x persona, 1.83x compliance), but the terminal persistence score cannot be calculated.
5. **Enrichment amplification is a pipeline property**, not just an input property. The same PRD content produces different amplification rates depending on whether a TDD is also present (Run C's persona amplification is 10x vs Run B's 2x at the roadmap stage alone).
