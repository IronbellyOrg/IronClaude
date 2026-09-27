---
id: "TMPL-SPEC-qa-consolidated-findings"
title: "qa-consolidated-findings_template"
description: "Shared report template for merged/deduplicated QA findings across multiple lens reports (structural + content), used by /task Step 6 executor merge and /task-builder A.10/A.10.5 consolidation."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.2"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: "SPEC-1-templated-reports-canonical-rule-20260701.md s2 L30"
related_docs:
  - ".claude/skills/task/SKILL.md"
  - ".claude/skills/task-builder/SKILL.md"
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
template_name: "QA Consolidated Findings"
template_version: "1.0.0"
sections: 5
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-consolidated-findings-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task" # status: confirmed
  - "task-builder" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the shared consolidated-findings report template. It is used any time
multiple independent QA lens reports (structural rf-qa lenses + content
rf-qa-qualitative lenses) must be merged into one deduplicated findings set
before a single fix agent acts. Three producing sites use this shape:
/task Step 6 (executor merge of phase-gate lens reports), /task-builder A.10
(merge of the two structural QA reports), and /task-builder A.10.5 (merge of
the two qualitative QA reports).

SCOPE:
This template covers ONLY the consolidation/merge step. It does NOT cover:
- the individual per-lens QA report (that is qa-lens_report_template.md)
- the fix agent's own disposition record (that is qa-fix-summary_template.md,
  which populates the Actions Taken block of a subsequent qa-lens report)
- the source-fidelity cross-check (qa-source-fidelity_template.md)

THE SECTIONS (fixed order, all 5 required; the header/frontmatter block, Topic,
Date, Phase, Fix cycle, precedes the numbered sections and is excluded from the
count, consistent with every sibling template's PART1 convention):
1. Source Lens Reports -- proves every input lens report was actually read
2. Consolidated Findings -- the merged, deduplicated findings table
3. In-Scope vs Out-of-Scope -- which findings the single fix agent will address now
4. Fix Scope -- explicit scope statement for the fix agent
5. Summary -- findings counts before/after dedup, broken out by severity

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row in each table
- Every placeholder MUST use the `RF_PLACEHOLDER` prefix; no other sentinel form

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Tables over prose wherever the source data is tabular
- Deduplication must be explicit: when two lens reports raise the same
  underlying issue, the merged row states so rather than listing it twice
- Every merged finding MUST retain its originating lens attribution
################################################################################ -->

## PART 2: THE QA CONSOLIDATED FINDINGS SCAFFOLD (copy everything below this line)

# QA Consolidated Findings - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** {{RF_PLACEHOLDER:PHASE}}
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}} / 3

## Source Lens Reports

| # | Lens | Agent Type | Report Path | Verdict |
|---|------|-----------|--------------|---------|
| 1 | {{RF_PLACEHOLDER:LENS_NAME}} | {{RF_PLACEHOLDER:AGENT_TYPE}} | {{RF_PLACEHOLDER:REPORT_PATH}} | {{RF_PLACEHOLDER:LENS_VERDICT}} |
{{RF_PLACEHOLDER:SOURCE_LENS_REPORTS_ROW}}

## Consolidated Findings

<!-- Merged and deduplicated across ALL source lens reports above. When two lenses
raise the same underlying issue, merge into ONE row and note both originating
lenses rather than duplicating the row. -->

| # | Severity | Originating Lens | Location | Issue | Required Fix |
|---|----------|-------------------|----------|-------|---------------|
| 1 | {{RF_PLACEHOLDER:SEVERITY}} | {{RF_PLACEHOLDER:ORIGINATING_LENS}} | {{RF_PLACEHOLDER:LOCATION}} | {{RF_PLACEHOLDER:ISSUE}} | {{RF_PLACEHOLDER:REQUIRED_FIX}} |
{{RF_PLACEHOLDER:CONSOLIDATED_FINDINGS_ROW}}

<!-- Severity enum: CRITICAL | IMPORTANT | MINOR -->

## In-Scope vs Out-of-Scope

**In-scope (fix this cycle):**

{{RF_PLACEHOLDER:IN_SCOPE_BODY}}

**Out-of-scope (deferred):**

{{RF_PLACEHOLDER:OUT_OF_SCOPE_BODY}}

## Fix Scope

{{RF_PLACEHOLDER:FIX_SCOPE_BODY}}

## Summary

- **Findings before dedup:** {{RF_PLACEHOLDER:FINDINGS_BEFORE_DEDUP}}
- **Findings after dedup:** {{RF_PLACEHOLDER:FINDINGS_AFTER_DEDUP}}
- **CRITICAL:** {{RF_PLACEHOLDER:CRITICAL_COUNT}}
- **IMPORTANT:** {{RF_PLACEHOLDER:IMPORTANT_COUNT}}
- **MINOR:** {{RF_PLACEHOLDER:MINOR_COUNT}}
