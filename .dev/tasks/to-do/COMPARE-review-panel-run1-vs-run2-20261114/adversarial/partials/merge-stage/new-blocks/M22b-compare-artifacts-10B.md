<!-- Source: new text — merged per Change #M-22 -->

### 10.B Compare artifacts

The compare of run 1's and run 2's reports and this merge were produced by `/sc:adversarial` (depth `standard`). Their artifacts live in `.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/`; every path below is relative to that folder.

**Inputs and main artifacts**

| Path | Purpose |
|---|---|
| `adversarial/variant-1-original.md` | Byte-identical copy of run 1's report (4,476 lines); the target of every `V1:<n>` citation in new text |
| `adversarial/variant-2-original.md` | Byte-identical copy of run 2's report (5,098 lines), the base; the target of every `V2:<n>` citation in new text |
| `adversarial/diff-analysis.md` | Diff of the two reports: 56 structural (S), 97 content (C), 63 contradiction (X), 124 unique (U) and 59 shared-assumption (A) rows, plus the section "Orchestrator Verification of Contradictions" (read-only re-checks of 14 contradiction groups) |
| `adversarial/debate-points.md` | The 234 debate points (S + C + X + 18 promoted A) and the clusters CL-01 to CL-26 they were debated in |
| `adversarial/debate-transcript.md` | Round 1 and Round 2 of the advocates, the Round 2.5 invariant probe, the scoring matrix and the convergence assessment |
| `adversarial/invariant-probe.md` | The fault-finder's 32 invariant rows (cited `R25-INV-nnn` in this document; Appendix D) |
| `adversarial/base-selection.md` | Quantitative and qualitative scoring of both reports and the choice of run 2 as the base (debate tiebreaker) |
| `adversarial/refactor-plan.md` | The merge plan, changes M-00 to M-30, and its review status |
| `adversarial/merge-log.md` | Per-change record of what the merge applied, with before/after summaries and validation results |

**Working files (`adversarial/partials/`)**

| Path | Purpose |
|---|---|
| `adversarial/partials/diff-partial-A.md` to `diff-partial-D.md` | The four analysts' diff partials (A: ToC and Sections 1, 3, 4; B: Sections 2 and 5; C: Section 6; D: Sections 7 to 10 and appendices) |
| `adversarial/partials/id-map.json` | Map from the partials' own ids to the `diff-analysis.md` ids |
| `adversarial/partials/orchestrator-verification.md` | The orchestrator's independent re-check of contradictions (copied into `diff-analysis.md`) |
| `adversarial/partials/point-cluster.json` | Map from each debate point to its cluster |
| `adversarial/partials/r1-advocate-V1.md`, `r1-advocate-V2.md` | Round 1 positions of the run 1 and run 2 advocates, with cluster verdicts and point exceptions |
| `adversarial/partials/r2-advocate-V1.md`, `r2-advocate-V2.md` | Round 2 rebuttals: final verdicts on the 38 disputed points, corrections found, must-carry lists |
| `adversarial/partials/convergence-r1.md`, `convergence-r2.md`, `r2-state.json`, `consensus-summary.md` | Convergence snapshots after each round and the computed verdict state (see Merge Notes (a) on the inheritance artefacts in `r2-state.json`) |
| `adversarial/partials/r25-fault-finder-notes.md` | The fault-finder's long-form notes: 31 re-derived numbers (section 1) and the corrections the merge must apply |
| `adversarial/partials/scoring-matrix.md`, `matrix.json` | Per-point winners with confidence, the tally and the list of unresolved points |
| `adversarial/partials/quant-section.md`, `quant.json` | Quantitative scoring layer of the base selection |
| `adversarial/partials/qual-pass1.md`, `qual-pass2.md`, `qual-reeval.md`, `qual-parse.json` | Qualitative scoring passes of the base selection and one re-evaluation |
| `adversarial/partials/plan-review.md`, `plan-review-2.md`, `plan-review-3.md` | The three independent reviews of the merge plan |
| `adversarial/partials/merge-scripts/` | Scripts of the compare (`cmp_*.py`) and of the merge executors (extraction, base corrections, new blocks) |
| `adversarial/partials/merge-stage/` | The merge's intermediate outputs: run 1 blocks after the id pass (`v1-blocks/`), new-text blocks (`new-blocks/`) and the executors' logs |
