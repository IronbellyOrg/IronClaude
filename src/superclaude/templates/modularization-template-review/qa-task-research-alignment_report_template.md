---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-task-research-alignment"
title: "qa-task-research-alignment_report_template"
description: "Shared report template for the /task-builder A.10.25 rf-analyst task-research-alignment lens: cross-validates every task file item against the research files it was built from."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.18"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/skills/task-builder/SKILL.md:1422-1466 (A.10.25 rf-analyst task-research-alignment lens)"
related_docs:
  - ".claude/templates/reports/qa-lens_report_template.md"
  - ".claude/agents/rf-analyst.md"
  - ".claude/skills/task-builder/SKILL.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - qa-report
  - template
  - task-integrity
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "QA Task Research Alignment"
template_version: "1.0.0"
sections: 5
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-task-research-alignment-report"
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
This is the /task-builder A.10.25 task-research-alignment report, produced
by the 5th agent of the combined task-integrity gate (rf-analyst, not
rf-qa). It cross-validates that every significant research finding has a
corresponding task file checklist item, and that no task file item
fabricates actions ungrounded in research.

SCOPE:
This is NOT a specialization of the qa-lens_report_template.md shape.
rf-analyst.md carries no Confidence Gate Protocol (confirmed: grepped
`rf-analyst.md` for "Confidence Gate", zero matches, unlike rf-qa.md and
rf-qa-qualitative.md which share that machinery) and the A.10.25 inline
prompt at SKILL.md:1463-1465 requires only "VERDICT: PASS or FAIL, and
severity-rated issues if FAIL" -- no confidence/tool-engagement fields.
This template therefore has NO Confidence Gate block, by design, matching
its source agent's actual output contract rather than the rf-qa lens
shape used by Steps 2.13-2.17.

THE SECTIONS (fixed order, all 5 required):
1. Overall Verdict -- PASS or FAIL for this lens
2. Alignment Table -- one row per research finding, whether a task file item enacts it
3. Summary -- findings checked, aligned count, fabrication count, critical issues
4. Issues Found -- severity-rated alignment gaps or fabrications (present even on PASS, empty body)
5. QA Complete -- closing marker plus the final VERDICT line

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Verdict is EXACTLY one of: PASS | FAIL
- Aligned? is EXACTLY one of: YES | NO
- Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR
################################################################################ -->

## PART 2: THE QA TASK RESEARCH ALIGNMENT SCAFFOLD (copy everything below this line)

# QA Task Research Alignment - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** task-research-alignment

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

## Alignment Table

<!-- one row per significant research finding (file paths, patterns, requirements, conventions discovered); Aligned = YES only when a corresponding task file item enacts the finding -->

| Item | Research Source | Aligned? | Evidence | Notes |
|------|------------------|----------|----------|-------|
| {{RF_PLACEHOLDER:ITEM}} | {{RF_PLACEHOLDER:RESEARCH_SOURCE}} | {{RF_PLACEHOLDER:ALIGNED}} | {{RF_PLACEHOLDER:EVIDENCE}} | {{RF_PLACEHOLDER:NOTES}} |
{{RF_PLACEHOLDER:ALIGNMENT_ROW}}

## Summary

{{RF_PLACEHOLDER:SUMMARY}}

## Issues Found

<!-- canonical issue shape: research finding with no corresponding task file item, task file item fabricating a file/pattern/requirement absent from all research files, research-identified caveat missing from a verification clause, research-identified dependency not reflected in phase ordering -->

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|---------------|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:SEVERITY}} | {{RF_PLACEHOLDER:LOCATION}} | {{RF_PLACEHOLDER:ISSUE}} | {{RF_PLACEHOLDER:REQUIRED_FIX}} |
{{RF_PLACEHOLDER:ISSUE_ROW}}

## QA Complete

VERDICT: {{RF_PLACEHOLDER:FINAL_VERDICT}}
