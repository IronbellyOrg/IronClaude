---
id: "TMPL-SPEC-qa-fix-summary"
title: "qa-fix-summary_template"
description: "Shared sub-template that populates the Actions Taken block of a fix agent's qa-lens report with a per-finding disposition record. Not a standalone output path (GAP-4 Option b)."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.3"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on:
  - ".claude/templates/reports/qa-lens_report_template.md"
spec_path: "SPEC-1-templated-reports-canonical-rule-20260701.md s2 L31"
related_docs:
  - ".claude/agents/rf-qa-qualitative.md"
  - ".claude/agents/rf-qa.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - qa-report
  - template
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "QA Fix Summary"
template_version: "1.0.0"
sections: 2
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-fix-summary-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task" # status: confirmed
  - "rf-qa" # status: confirmed
  - "rf-qa-qualitative" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is NOT a standalone report file. It is the shape of the `## Actions Taken`
section inside a fix agent's qa-lens_report_template.md output, extended with a
per-finding disposition sub-block (GAP-4 firm resolution, Option b). A
fix_authorization:true rf-qa or rf-qa-qualitative agent fills THIS shape into the
Actions Taken section of its own qa-lens report rather than writing a separate file.

SCOPE:
Use this template's PART 2 content as the literal body of `## Actions Taken` in a
qa-lens report when fix_authorization was true. Do NOT create a sibling file next
to the qa-lens report for this content.

THE SECTIONS (fixed order, both required):
1. Actions Taken -- per-finding disposition table plus the fix cycle line
2. Residual / Unfixed Rollup -- findings not fixed this cycle and why

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row in each table

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Disposition MUST be one of: fixed, deferred, not-reproduced, out-of-scope
- Every deferred/not-reproduced/out-of-scope disposition MUST carry a reason
################################################################################ -->

## PART 2: THE QA FIX SUMMARY SCAFFOLD (copy everything below this line)

## Actions Taken

| Finding ID | Severity | File:Location | Disposition | Fix applied (what) | Verification method |
|------------|----------|----------------|--------------|----------------------|-----------------------|
| {{RF_PLACEHOLDER:FINDING_ID}} | {{RF_PLACEHOLDER:SEVERITY}} | {{RF_PLACEHOLDER:FILE_LOCATION}} | {{RF_PLACEHOLDER:DISPOSITION}} | {{RF_PLACEHOLDER:FIX_APPLIED}} | {{RF_PLACEHOLDER:VERIFICATION_METHOD}} |
{{RF_PLACEHOLDER:ACTIONS_TAKEN_ROW}}

<!-- Disposition enum: fixed | deferred | not-reproduced | out-of-scope -->

Fix cycle: {{RF_PLACEHOLDER:FIX_CYCLE}} / 3

## Residual / Unfixed Rollup

| Finding ID | Severity | Reason not fixed | Escalation status |
|------------|----------|--------------------|----------------------|
| {{RF_PLACEHOLDER:RESIDUAL_FINDING_ID}} | {{RF_PLACEHOLDER:RESIDUAL_SEVERITY}} | {{RF_PLACEHOLDER:RESIDUAL_REASON}} | {{RF_PLACEHOLDER:RESIDUAL_ESCALATION_STATUS}} |
{{RF_PLACEHOLDER:RESIDUAL_ROLLUP_ROW}}

<!-- Feeds the max-3-cycle escalation: if a finding remains unfixed at Fix cycle 3/3,
escalation_status MUST read "escalate to user" per the Serialized Fix Protocol. -->
