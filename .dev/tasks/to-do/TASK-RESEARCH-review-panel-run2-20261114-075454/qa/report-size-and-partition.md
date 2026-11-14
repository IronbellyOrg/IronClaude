# Report size and Gate 3 lens partition (Item 6.02)

Date: 2026-11-14
Report: `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md`

## Size

- Total lines (read-only `wc -l`): **5057** (1,256,814 bytes).
- I19 size tier: **over 3000 lines** (minimum 6 rf-qa structural lenses plus 6 rf-qa-qualitative content lenses = 12; this gate runs 13 lenses: 5 structural rf-qa, 5 content rf-qa-qualitative, 3 domain; every lens runs as two instances).
- Section 8.1 note: the 5,950 value-inventory rows are carried in Appendix A (`synthesis/synth-08-value-inventory.md`, 6,121 lines, checked at Gate 2), not inline; the report holds the 8.1 summary, rules, reconciliation line and the resolved Gate 1 findings. This change was made by the orchestrator at assembly (logged in the task log).

## Mode

**MODE: SPLIT** (more than 3000 lines).

- Half of the total: 2528.5. Nearest section-level heading `## N.`: line 2115 (`## 6. Options Analysis`, 413.5 lines away); next candidates are line 1515 (`## 5.`, 1013.5 away) and line 3544 (`## 7.`, 1015.5 away). **K = 2115.**
- Instance **a** reviews lines **1 to 2114** (Table of Contents, Baseline and Conventions, Sections 1 to 5).
- Instance **b** reviews lines **2115 to 5057** (Sections 6 to 10, Appendix A pointer section and Appendix B).
- The split point falls on a section heading line (line 2115 is `## 6. Options Analysis`).

## Section headings with line numbers (Grep `^## `)

| Line | Heading |
|---|---|
| 10 | Table of Contents |
| 104 | Baseline and Conventions |
| 122 | 1. Problem Statement |
| 137 | 2. Current State Analysis |
| 1110 | 3. Target State |
| 1206 | 4. Gap Analysis |
| 1515 | 5. External Research Findings |
| 2115 | 6. Options Analysis |
| 3544 | 7. Recommendation |
| 4209 | 8. Value Inventory and Inputs for a Later Plan |
| 4648 | 9. Open Questions |
| 4806 | 10. Evidence Trail |
| 5031 | Appendix A: Value Inventory Rows (separate file in the report package) |
| 5035 | Appendix B: Synthesis Notes Carried from synth-01 |

## Gate 3 lenses (13) and output files

| # | Kind | Lens | Agent type | Instance a output | Instance b output |
|---|---|---|---|---|---|
| 1 | structural | template-conformance | rf-qa | `qa/qa-lens-template-conformance-a.md` | `qa/qa-lens-template-conformance-b.md` |
| 2 | structural | internal-consistency | rf-qa | `qa/qa-lens-internal-consistency-a.md` | `qa/qa-lens-internal-consistency-b.md` |
| 3 | structural | evidence-quality | rf-qa | `qa/qa-lens-evidence-quality-a.md` | `qa/qa-lens-evidence-quality-b.md` |
| 4 | structural | completeness | rf-qa | `qa/qa-lens-completeness-a.md` | `qa/qa-lens-completeness-b.md` |
| 5 | structural | report-only-scope | rf-qa | `qa/qa-lens-report-only-scope-a.md` | `qa/qa-lens-report-only-scope-b.md` |
| 6 | content | actionability | rf-qa-qualitative | `qa/qa-lens-actionability-a.md` | `qa/qa-lens-actionability-b.md` |
| 7 | content | numbers-metrics | rf-qa-qualitative | `qa/qa-lens-numbers-metrics-a.md` | `qa/qa-lens-numbers-metrics-b.md` |
| 8 | content | crossref-chain | rf-qa-qualitative | `qa/qa-lens-crossref-chain-a.md` | `qa/qa-lens-crossref-chain-b.md` |
| 9 | content | domain-accuracy | rf-qa-qualitative | `qa/qa-lens-domain-accuracy-a.md` | `qa/qa-lens-domain-accuracy-b.md` |
| 10 | content | claim-tagging-and-independence | rf-qa-qualitative | `qa/qa-lens-claim-tagging-independence-a.md` | `qa/qa-lens-claim-tagging-independence-b.md` |
| 11 | domain | recommendation-feasibility | rf-qa-qualitative | `qa/qa-lens-recommendation-feasibility-a.md` | `qa/qa-lens-recommendation-feasibility-b.md` |
| 12 | domain | finding-reproducibility | rf-qa-qualitative | `qa/qa-lens-finding-reproducibility-a.md` | `qa/qa-lens-finding-reproducibility-b.md` |
| 13 | domain | implementation-plan-concreteness (adapted to Section 8.2) | rf-qa | `qa/qa-lens-implementation-concreteness-a.md` | `qa/qa-lens-implementation-concreteness-b.md` |

Instance a is run by items 6.03 to 6.15; instance b by items 6.16 to 6.28 (they read this file for the mode and the ranges).
