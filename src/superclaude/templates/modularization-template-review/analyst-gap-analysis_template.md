---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-analyst-gap-analysis"
title: "analyst-gap-analysis_template"
description: "Shared report template for the rf-analyst Gap Analysis type: the firm gap table schema (Gap / Current State / Target State / Severity / Notes) that rf-qa validates against."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.22"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/agents/rf-analyst.md:310-323 (Gap Analysis type, underspecified), .claude/agents/rf-qa.md:189 (the gap table column schema rf-qa validates against)"
related_docs:
  - ".claude/agents/rf-analyst.md"
  - ".claude/agents/rf-qa.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - analyst-report
  - template
  - gap-analysis
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Analyst Gap Analysis"
template_version: "1.0.0"
sections: 2
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-analyst-gap-analysis-report"
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
This is the canonical schema for the rf-analyst "Gap Analysis" type
(rf-analyst.md:310-323), which is underspecified in its own source agent
(no column schema, no verdict format). This template FIRMLY RESOLVES that
gap by adopting the column shape rf-qa already validates against at
rf-qa.md:189, so gap-analysis producers and consumers agree on structure.

SCOPE:
Gap table with fixed column order, a Summary rollup by severity, and an
Overall Verdict where any CRITICAL gap forces FAIL. No Confidence Gate
(this is an rf-analyst type, which carries no Confidence Gate Protocol
machinery, consistent with the other rf-analyst-only templates in this
library).

THE SECTIONS (fixed order, both required):
1. Gap Table -- one row per gap, FIXED column order
2. Summary -- rollup by severity plus the Overall Verdict line

COLUMN SCHEMA (FIXED order, rf-qa validates structure against this):
Gap | Current State (file:line evidence) | Target State | Severity | Notes

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR
- Overall Verdict is EXACTLY one of: PASS | FAIL
- Any CRITICAL-severity gap row forces Overall Verdict to FAIL
################################################################################ -->

## PART 2: THE ANALYST GAP ANALYSIS SCAFFOLD (copy everything below this line)

# Gap Analysis

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}

## Gap Table

<!-- column order is FIXED: rf-qa validates structure against this exact order -->

| Gap | Current State (file:line evidence) | Target State | Severity | Notes |
|-----|--------------------------------------|---------------|----------|-------|
| {{RF_PLACEHOLDER:GAP}} | {{RF_PLACEHOLDER:CURRENT_STATE}} | {{RF_PLACEHOLDER:TARGET_STATE}} | {{RF_PLACEHOLDER:SEVERITY}} | {{RF_PLACEHOLDER:NOTES}} |
{{RF_PLACEHOLDER:GAP_ROW}}

## Summary

- **Critical gaps:** {{RF_PLACEHOLDER:CRITICAL_COUNT}}
- **Important gaps:** {{RF_PLACEHOLDER:IMPORTANT_COUNT}}
- **Minor gaps:** {{RF_PLACEHOLDER:MINOR_COUNT}}
- **Total gaps:** {{RF_PLACEHOLDER:TOTAL_COUNT}}

**Overall Verdict:** {{RF_PLACEHOLDER:VERDICT}} <!-- any CRITICAL gap forces FAIL -->
