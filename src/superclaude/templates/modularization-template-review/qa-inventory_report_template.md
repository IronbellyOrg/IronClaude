---
id: "TMPL-SPEC-qa-inventory-report"
title: "qa-inventory_report_template"
description: "Shared report template for the /task executor's phase-gate setup inventory, enumerating output files under QA, governing requirements, the lens plan, and acceptance criteria before lens agents are spawned."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.4"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: "SPEC-1-templated-reports-canonical-rule-20260701.md s2 L32"
related_docs:
  - ".claude/skills/task/SKILL.md"
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
template_name: "QA Inventory Report"
template_version: "1.0.0"
sections: 4
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-inventory-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the /task executor's phase-gate setup inventory. It is produced BEFORE
lens agents are spawned for a phase-gate QA cycle, enumerating what is under
review, what requirements govern the gate, which lenses will run, and what
counts as passing.

SCOPE:
This template covers ONLY the pre-gate inventory/planning step. It does NOT
cover the lens reports themselves (qa-lens_report_template.md) or their merge
(qa-consolidated-findings_template.md).

THE SECTIONS (fixed order, all 4 required):
1. Output Files Under QA -- every file the gate will review
2. Governing Requirements -- the QA_GATE / VALIDATION / TESTING requirements
3. Lens Plan -- the structural and content lenses to be applied
4. Acceptance Criteria -- the concrete pass conditions for the phase

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row in each table

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- The inventory MUST enumerate every output file the gate covers; a gate that
  omits a modified file from its own inventory cannot claim to have reviewed it
################################################################################ -->

## PART 2: THE QA INVENTORY REPORT SCAFFOLD (copy everything below this line)

# QA Inventory Report - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** {{RF_PLACEHOLDER:PHASE}}

## Output Files Under QA

| File | Path | Type |
|------|------|------|
| {{RF_PLACEHOLDER:FILE_NAME}} | {{RF_PLACEHOLDER:FILE_PATH}} | {{RF_PLACEHOLDER:FILE_TYPE}} |
{{RF_PLACEHOLDER:OUTPUT_FILES_ROW}}

## Governing Requirements

| Requirement Type | Requirement | Source |
|-------------------|-------------|--------|
| {{RF_PLACEHOLDER:REQUIREMENT_TYPE}} | {{RF_PLACEHOLDER:REQUIREMENT_TEXT}} | {{RF_PLACEHOLDER:REQUIREMENT_SOURCE}} |
{{RF_PLACEHOLDER:GOVERNING_REQUIREMENTS_ROW}}

<!-- Requirement Type enum: QA_GATE | VALIDATION | TESTING -->

## Lens Plan

| Lens | Agent Type | Focus |
|------|-----------|-------|
| {{RF_PLACEHOLDER:LENS_NAME}} | {{RF_PLACEHOLDER:LENS_AGENT_TYPE}} | {{RF_PLACEHOLDER:LENS_FOCUS}} |
{{RF_PLACEHOLDER:LENS_PLAN_ROW}}

## Acceptance Criteria

{{RF_PLACEHOLDER:ACCEPTANCE_CRITERIA_BODY}}
