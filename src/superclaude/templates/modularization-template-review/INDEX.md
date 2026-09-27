# Report Template Library Index

Catalog of the report-template artifacts authored under `.claude/templates/reports/` (`TASK-RF-templated-reports-20260701-171419`, Phase 2) and set aside here for review, plus the 2 acceptance-proof templates authored directly into this directory by `TASK-RF-acceptance-proof-20260805-154602` Phase 6. Each row is one authored artifact: 26 `_template.md` files following the standard report-template convention (MDTM frontmatter, PART 1 fill instructions, PART 2 scaffold with `RF_PLACEHOLDER` slots) plus 1 `.contract` file (a byte-exact no-paraphrase reproduction, not a fill-in-the-blank template).

> `ab-report_template.md` was originally authored alongside these but has since GRADUATED to the eval skill: it is now an eval-skill output template at `.claude/skills/skill-eval/templates/ab-report_template.md`, registered in `.claude/skills/skill-eval/templates/INDEX.md`. It is intentionally NOT listed below (removed 2026-07-04 by `TASK-RF-eval-output-templates-20260703-082721`). The `.claude/templates/reports/` directory was removed at the same time.

The 4 engine JSON schemas (`junit-xml-report.schema.json`, `ab-summary-yaml.schema.json`, `accepted-marker.schema.json`, `advisory-sidecar.schema.json`) are NOT listed below: they live under `evals/engine/suites/` beside `run-record.schema.json`, not under this directory.

| Template File | Report Type | Primary Consumer(s) | Storage |
|---|---|---|---|
| `analyst-completeness_report_template.md` | Analyst Completeness | task-builder | `.claude/templates/reports/analyst-completeness_report_template.md` |
| `analyst-coverage-matrix_template.md` | Analyst Coverage Matrix | task-builder, rf-analyst | `.claude/templates/reports/analyst-coverage-matrix_template.md` |
| `analyst-cross-validation_report_template.md` | Analyst Cross-Validation | task-builder | `.claude/templates/reports/analyst-cross-validation_report_template.md` |
| `analyst-gap-analysis_template.md` | Analyst Gap Analysis | task-builder, rf-analyst | `.claude/templates/reports/analyst-gap-analysis_template.md` |
| `analyst-synthesis-review_report_template.md` | Analyst Synthesis Review | task-builder, rf-analyst | `.claude/templates/reports/analyst-synthesis-review_report_template.md` |
| `claim-evidence-matrix_template.md` | Claim-to-Evidence Matrix | run4-harness matrix generator, acceptance-methodology auditor | `.claude/templates/modularization-template-review/claim-evidence-matrix_template.md` |
| `codebase-research_template.md` | Codebase Research | task-builder | `.claude/templates/reports/codebase-research_template.md` |
| `pipeline-complete_report_template.md` | Pipeline Complete Summary | rf-team-lead | `.claude/templates/reports/pipeline-complete_report_template.md` |
| `qa-acceptance-methodology-audit_template.md` | QA Acceptance Methodology Audit | acceptance-methodology auditor agent | `.claude/templates/modularization-template-review/qa-acceptance-methodology-audit_template.md` |
| `qa-consolidated-findings_template.md` | QA Consolidated Findings | task, task-builder | `.claude/templates/reports/qa-consolidated-findings_template.md` |
| `qa-cross-source-contradictions_template.md` | QA Cross-Source Contradictions | task | `.claude/templates/reports/qa-cross-source-contradictions_template.md` |
| `qa-fix-summary_template.md` | QA Fix Summary | task, rf-qa, rf-qa-qualitative | `.claude/templates/reports/qa-fix-summary_template.md` |
| `qa-inventory_report_template.md` | QA Inventory Report | task | `.claude/templates/reports/qa-inventory_report_template.md` |
| `qa-lens_report_template.md` | QA Lens Report | task, task-builder, rf-qa, rf-qa-qualitative | `.claude/templates/reports/qa-lens_report_template.md` |
| `qa-qualitative-operational_report_template.md` | QA Qualitative Operational | task-builder, task | `.claude/templates/reports/qa-qualitative-operational_report_template.md` |
| `qa-qualitative-sufficiency_report_template.md` | QA Qualitative Sufficiency | task-builder, task | `.claude/templates/reports/qa-qualitative-sufficiency_report_template.md` |
| `qa-research-depth_report_template.md` | QA Research Depth | task-builder | `.claude/templates/reports/qa-research-depth_report_template.md` |
| `qa-research-evidence_report_template.md` | QA Research Evidence | task-builder | `.claude/templates/reports/qa-research-evidence_report_template.md` |
| `qa-research-gap_report_template.md` | QA Research Gap | task-builder | `.claude/templates/reports/qa-research-gap_report_template.md` |
| `qa-source-fidelity_template.md` | QA Source Fidelity | task | `.claude/templates/reports/qa-source-fidelity_template.md` |
| `qa-task-research-alignment_report_template.md` | QA Task Research Alignment | task-builder | `.claude/templates/reports/qa-task-research-alignment_report_template.md` |
| `qa-task-validation-b2_report_template.md` | QA Task Validation B2 | task-builder | `.claude/templates/reports/qa-task-validation-b2_report_template.md` |
| `qa-task-validation-structure_report_template.md` | QA Task Validation Structure | task-builder | `.claude/templates/reports/qa-task-validation-structure_report_template.md` |
| `research-notes_template.md` | Research Notes | task-builder | `.claude/templates/reports/research-notes_template.md` |
| `track-scope-map_template.md` | Track Scope Map | rf-team-lead | `.claude/templates/reports/track-scope-map_template.md` |
| `web-research_template.md` | Web Research | task-builder | `.claude/templates/reports/web-research_template.md` |
| `synthetic-dnsp-finding.contract` | Synthetic DNSP Finding Contract (byte-exact, no paraphrase) | task-builder (DM-003 merge step A.8/A.10); produced by rf-analyst, rf-qa, rf-qa-qualitative | `.claude/templates/reports/synthetic-dnsp-finding.contract` |

**Notes:**
- 26 rows are `_template.md` files (standard report-template convention); 1 row (`synthetic-dnsp-finding.contract`) is a distinct byte-exact reproduction contract, not a fill-in template, per its own PART 1 note.
- These 27 artifacts (26 `.md` + 1 `.contract`) are the files physically set aside in this `modularization-template-review/` directory, one row each. `ab-report_template.md` was also authored under the original Phase 2 but has graduated to the eval skill (see the note above) and is deliberately NOT listed.
- 2 of the 26 (`claim-evidence-matrix_template.md` and `qa-acceptance-methodology-audit_template.md`) were authored later, by `TASK-RF-acceptance-proof-20260805-154602` Phase 6, and were placed directly in this directory because that is where the registered templates physically live. Their Storage column therefore records their real path here, unlike the Phase-2 rows whose Storage column still records the removed `.claude/templates/reports/` path (the known Storage-column defect left to its owning workstream).
- The 4 engine JSON schemas live under `evals/engine/suites/` beside `run-record.schema.json`, not under this directory (see note above).

