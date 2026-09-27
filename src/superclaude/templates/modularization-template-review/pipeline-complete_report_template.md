---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-pipeline-complete-report"
title: "pipeline-complete_report_template"
description: "Optional orchestration-summary template modeling rf-team-lead's RIGORFLOW PIPELINE COMPLETE fenced block, emitted on EXECUTION_COMPLETE at Phase 7 (Report Results)."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔽 Low"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.30"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/agents/rf-team-lead.md:251-265 (RIGORFLOW PIPELINE COMPLETE fenced block, Phase 7 Report Results)"
related_docs:
  - ".claude/agents/rf-team-lead.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - rf-team-lead
  - template
  - pipeline-complete
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Pipeline Complete Summary"
template_version: "1.0.0"
sections: 4
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-pipeline-complete-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "rf-team-lead" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This template models the EXACT human-facing plain-text block rf-team-lead
emits on `EXECUTION_COMPLETE` at Phase 7 (Report Results), per
`.claude/agents/rf-team-lead.md:251-265`. This is an OPTIONAL orchestration
summary, not a gated QA/analyst document. Like the ab-report template, the
PART 2 body is a literal reproduction of the plain-text block, wrapped in a
minimal set of `##` section markers ONLY so the `sections` frontmatter
integer and template-conformance checks apply consistently across the
library. The `##` headings are NOT part of the emitted text.

SCOPE:
Byte-order-exact reproduction of the RIGORFLOW PIPELINE COMPLETE block:
the header line, the `Task File` / `Status` / `Items Completed` fields, the
`OUTPUTS CREATED` list, the `ISSUES (if any)` list, and the `FOLLOW-UP
NEEDED` line, per rf-team-lead.md:254-268.

THE SECTIONS (fixed order, all 4 required, wrapper-only, not emitted text):
1. Header -- the banner line plus Task File / Status / Items Completed
2. Outputs Created -- the OUTPUTS CREATED list
3. Issues -- the ISSUES (if any) list
4. Follow-Up -- the closing FOLLOW-UP NEEDED line

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row
- Two distinct repeat markers apply: `{{RF_PLACEHOLDER:OUTPUT_ROW}}` (one
  per output file) and `{{RF_PLACEHOLDER:ISSUE_ROW}}` (one per issue)

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- `Status` is EXACTLY one of: Success | Partial | Failed
- `FOLLOW-UP NEEDED` is EXACTLY one of: Yes | No
- `Items Completed` renders as `X of Y` (both integers)
################################################################################ -->

## PART 2: THE PIPELINE COMPLETE SCAFFOLD (copy everything below this line)

<!-- this scaffold reproduces rf-team-lead's literal RIGORFLOW PIPELINE COMPLETE
     text output exactly; the ## headings below are wrapper-only structure for
     the sections convention and are NOT part of the emitted report text -->

## Header

<!-- banner plus the three fixed fields, in fixed order, per rf-team-lead.md:255-259 -->

RIGORFLOW PIPELINE COMPLETE
===========================
Task File: {{RF_PLACEHOLDER:TASK_FILE_PATH}}
Status: {{RF_PLACEHOLDER:STATUS}}
Items Completed: {{RF_PLACEHOLDER:ITEMS_COMPLETED}}

## Outputs Created

<!-- one bullet per created file, per rf-team-lead.md:261-262 -->

OUTPUTS CREATED:
- {{RF_PLACEHOLDER:OUTPUT_FILE}}
{{RF_PLACEHOLDER:OUTPUT_ROW}}

## Issues

<!-- one bullet per issue; omit the list body (keep only the "ISSUES (if any):" line) when there are none, per rf-team-lead.md:264-265 -->

ISSUES (if any):
- {{RF_PLACEHOLDER:ISSUE}}
{{RF_PLACEHOLDER:ISSUE_ROW}}

## Follow-Up

<!-- closing line, always present, per rf-team-lead.md:267 -->

FOLLOW-UP NEEDED: {{RF_PLACEHOLDER:FOLLOW_UP_NEEDED}}
