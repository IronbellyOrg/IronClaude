---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-analyst-cross-validation"
title: "analyst-cross-validation_report_template"
description: "Shared report template for the rf-analyst Cross-Validation Report: a single claim-by-claim table verifying research claims against actual source code."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.12"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/agents/rf-analyst.md:227-238 (Cross-Validation Report output format)"
related_docs:
  - ".claude/agents/rf-analyst.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - analyst-report
  - template
  - research-gate
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Analyst Cross-Validation"
template_version: "1.0.0"
sections: 1
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-analyst-cross-validation-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task-builder" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the rf-analyst Cross-Validation Report, the output of the
Cross-Validation analysis type: for each research claim, read the actual
source code at the referenced path and compare what the code shows vs what
the claim states.

SCOPE:
This template covers ONLY the Cross-Validation analysis type. Other
rf-analyst analysis types (Research Completeness Verification, Synthesis
Quality Review, Gap Analysis, Coverage Audit) use their own templates.

THE SECTIONS (header block plus 1 required table, no `##` heading wraps it in
the source schema):
- header block (Date, Claims verified) -- prose, not a counted section
1. the single validation table -- one row per claim, columns
   `# | Claim | Source | Code Path Checked | Verdict | Notes`

VERDICT VOCABULARY (closed set, mandatory on every row):
- VERIFIED -- the code matches the claim
- CONTRADICTED -- the code conflicts with the claim
- UNVERIFIED -- the claim could not be checked against the code

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Notes column documents what the code actually shows, especially for
  CONTRADICTED rows
################################################################################ -->

## PART 2: THE ANALYST CROSS-VALIDATION SCAFFOLD (copy everything below this line)

# Cross-Validation Report

- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Claims verified:** {{RF_PLACEHOLDER:CLAIMS_VERIFIED_COUNT}}

## Validation Results

| # | Claim | Source | Code Path Checked | Verdict | Notes |
|---|-------|--------|-------------------|---------|-------|
| {{RF_PLACEHOLDER:CLAIM_NUM}} | {{RF_PLACEHOLDER:CLAIM_TEXT}} | {{RF_PLACEHOLDER:CLAIM_SOURCE}} | {{RF_PLACEHOLDER:CLAIM_CODE_PATH}} | {{RF_PLACEHOLDER:CLAIM_VERDICT}} | {{RF_PLACEHOLDER:CLAIM_NOTES}} |
{{RF_PLACEHOLDER:VALIDATION_RESULTS_ROW}}

<!-- Verdict is EXACTLY one of: VERIFIED | CONTRADICTED | UNVERIFIED -->
