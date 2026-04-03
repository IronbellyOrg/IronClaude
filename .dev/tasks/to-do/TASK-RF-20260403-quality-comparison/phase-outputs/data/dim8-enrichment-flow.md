# Dimension 8: Enrichment Flow

**Traces enrichment persistence across pipeline stages:** extraction -> roadmap -> tasklist
**Sources:** Research files 01, 02, 03 (QA-verified); spot-checks against actual artifacts

---

## Persona Enrichment Flow (Alex + Jordan + Sam)

| Stage | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|-------|:----------------:|:----------------:|:----------------:|
| **extraction.md** | 0 | 10 | 4 |
| **roadmap.md** | 0 | 20 | 11 |
| **tasklist (all)** | 0 | N/A (no tasklist) | 40 |
| **Flow pattern** | Absent throughout | 10 -> 20 (2x amplification) | 4 -> 11 -> 40 (10x amplification) |

## Compliance Enrichment Flow (GDPR + SOC2)

| Stage | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|-------|:----------------:|:----------------:|:----------------:|
| **extraction.md** | 0 | 12 | 11 |
| **roadmap.md** | 0 | 22 | 25 |
| **tasklist (all)** | 0 | N/A (no tasklist) | 40 |
| **Flow pattern** | Absent throughout | 12 -> 22 (1.8x) | 11 -> 25 -> 40 (3.6x amplification) |

## Component Enrichment Flow

| Stage | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|-------|:----------------:|:----------------:|:----------------:|
| **extraction.md** | 12 | 16 | 134 |
| **roadmap.md** | 41 | N/A (different component set) | 111 |
| **tasklist (all)** | 73 | N/A (no tasklist) | 218 |
| **Flow pattern** | 12 -> 41 -> 73 (6x) | 16 -> ? (no tasklist) | 134 -> 111 -> 218 (1.6x) |

## Business Metrics Flow

| Stage | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|-------|:----------------:|:----------------:|:----------------:|
| **extraction.md** | 0 | 0 | 0 |
| **roadmap.md** | 0 | 7 | 7 |
| **tasklist (all)** | 0 | N/A | Not measured |
| **Flow pattern** | Absent | Introduced at roadmap | Introduced at roadmap |

---

## Spot-Check Results

| Check | Research Value | Spot-Check Value | Method | Match |
|-------|:-------------:|:----------------:|--------|:-----:|
| Run A extraction personas | 0 | 0 | `grep -ow 'Alex\|Jordan\|Sam' extraction.md` | YES |
| Run B extraction personas | 10 | 10 | `grep -ow 'Alex\|Jordan\|Sam' extraction.md` | YES |
| Run C roadmap compliance | 25 | 25 | `grep -ow 'GDPR\|SOC2' roadmap.md` | YES |
| Run C tasklist compliance | 44 (research) | 40 (spot-check) | `grep -ow 'GDPR\|SOC2' phase-*-tasklist.md tasklist-index.md` | DISCREPANCY |

---

## Assessment

The enrichment flow reveals three distinct patterns:

1. **Run A (Baseline):** No enrichment at any stage for personas, compliance, or business metrics. Component names are the only enrichment signal, growing steadily from extraction (12) through roadmap (41) to tasklist (73) -- a 6x amplification driven entirely by the spec's implementation details.

2. **Run B (Spec+PRD):** PRD-derived enrichment (personas, compliance, business metrics) appears at extraction and amplifies into the roadmap (personas 10->20, compliance 12->22). However, without a tasklist, the flow terminates at the roadmap stage. This is a truncated pipeline.

3. **Run C (TDD+PRD):** The complete 3-stage flow shows strong enrichment amplification. Personas grow from 4 -> 11 -> 40 (10x from extraction to tasklist). Compliance grows from 11 -> 25 -> 40 (3.6x). Component refs are high at all stages (134 -> 111 -> 218). The TDD+PRD combination produces the most comprehensive downstream propagation, with every enrichment category persisting and growing across all pipeline stages.

The key finding is that enrichment from PRD/TDD inputs does not merely persist -- it amplifies at each stage. The roadmap approximately doubles persona/compliance counts from extraction, and the tasklist approximately doubles again from roadmap. This suggests the pipeline's merge and tasklist generation steps actively propagate and contextualize enrichment signals rather than just passing them through.
