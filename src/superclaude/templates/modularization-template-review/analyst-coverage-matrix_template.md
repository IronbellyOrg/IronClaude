---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-analyst-coverage-matrix"
title: "analyst-coverage-matrix_template"
description: "Shared report template for the rf-analyst Coverage Audit type: the firm coverage-matrix column schema (Required Topic / Covered? / Source File(s) / Coverage Detail / Notes) derived from the underspecified source process."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.23"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/agents/rf-analyst.md:326-338 (Coverage Audit type, underspecified process)"
related_docs:
  - ".claude/agents/rf-analyst.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - analyst-report
  - template
  - coverage-matrix
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Analyst Coverage Matrix"
template_version: "1.0.0"
sections: 2
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-analyst-coverage-matrix-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task-builder" # status: confirmed
  - "rf-analyst" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the canonical schema for the rf-analyst "Coverage Audit" type
(rf-analyst.md:326-338), which is underspecified in its own source agent
(process only: read each file, check off which required topics are
covered, flag zero/insufficient coverage; no matrix column schema, no
verdict format). This template FIRMLY RESOLVES that gap by deriving the
matrix columns from the process description itself.

SCOPE:
Coverage matrix with fixed column order, a Summary line (N/total topics
fully covered), and an Overall Verdict where any NO or PARTIAL row forces
FAIL. No Confidence Gate (this is an rf-analyst type, which carries no
Confidence Gate Protocol machinery, consistent with the other
rf-analyst-only templates in this library).

THE SECTIONS (fixed order, both required):
1. Coverage Matrix -- one row per required topic, FIXED column order
2. Summary -- N/total topics fully covered plus the Overall Verdict line

COLUMN SCHEMA (FIXED order):
Required Topic | Covered? | Source File(s) | Coverage Detail | Notes

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Covered? is EXACTLY one of: YES | PARTIAL | NO
- Overall Verdict is EXACTLY one of: PASS | FAIL
- Any NO or PARTIAL row forces Overall Verdict to FAIL
- A NO or PARTIAL row's Notes should reference the corresponding gap-analysis row when one exists
################################################################################ -->

## PART 2: THE ANALYST COVERAGE MATRIX SCAFFOLD (copy everything below this line)

# Coverage Matrix

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}

## Coverage Matrix

<!-- column order is FIXED -->

| Required Topic | Covered? | Source File(s) | Coverage Detail | Notes |
|-----------------|----------|-----------------|-------------------|-------|
| {{RF_PLACEHOLDER:REQUIRED_TOPIC}} | {{RF_PLACEHOLDER:COVERED}} | {{RF_PLACEHOLDER:SOURCE_FILES}} | {{RF_PLACEHOLDER:COVERAGE_DETAIL}} | {{RF_PLACEHOLDER:NOTES}} |
{{RF_PLACEHOLDER:MATRIX_ROW}}

## Summary

{{RF_PLACEHOLDER:COVERED_COUNT}}/{{RF_PLACEHOLDER:TOTAL_COUNT}} topics fully covered

**Overall Verdict:** {{RF_PLACEHOLDER:VERDICT}} <!-- any NO or PARTIAL row forces FAIL -->
