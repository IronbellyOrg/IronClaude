---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-research-gap"
title: "qa-research-gap_report_template"
description: "Shared report template for the /task-builder A.8 research quality gate's gap-detection lens (Agent 4, +round2): finds areas the researchers missed entirely."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.14"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on:
  - "qa-lens_report_template.md"
spec_path: ".claude/skills/task-builder/SKILL.md:795-826 (A.8 Agent 4 gap-detection lens)"
related_docs:
  - ".claude/templates/reports/qa-lens_report_template.md"
  - ".claude/skills/task-builder/SKILL.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - qa-report
  - template
  - research-gate
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "QA Research Gap"
template_version: "1.0.0"
sections: 6
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-research-gap-report"
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
This is the /task-builder A.8 research quality gate's gap-detection report,
produced by Agent 4 of the 5-agent research-gate lens set (2 rf-analyst + 2
rf-qa + 1 rf-qa-qualitative). This lens finds coverage gaps: areas the
researchers missed entirely, findings too vague to act on, missing
integration points, missing test/verification coverage. Also used for the
round-2 gap-fill re-check (SKILL.md:795-826).

SCOPE:
This is a specialization of the qa-lens_report_template.md shape, narrowed to
the 6 sections used by qa-research-evidence_report_template.md's sibling
lens (no Actions Taken or Recommendations sections; this is a report-only
research-gate lens, not a fix-authorized gate). The generic Issues Found
table is replaced by a gap-specific table (Gap | Where Expected | Severity |
Notes) per this template's build item.

THE SECTIONS (fixed order, all 6 required):
1. Overall Verdict -- PASS or FAIL for this lens
2. Items Reviewed -- one row per scope area/research file checked for coverage
3. Summary -- checks passed/total, checks failed, critical issues
4. Issues Found -- the gap table: Gap | Where Expected | Severity | Notes
5. Confidence Gate -- the MANDATORY computed-confidence block (never self-assessed)
6. QA Complete -- closing marker plus the final VERDICT line

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Verdict is EXACTLY one of: PASS | FAIL
- Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR
- Confidence and coverage figures are COMPUTED per the Confidence Gate
  Protocol (rf-qa.md:471-521), never self-assessed
################################################################################ -->

## PART 2: THE QA RESEARCH GAP SCAFFOLD (copy everything below this line)

# QA Research Gap - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** research-gap
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}} / 3

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

<!-- Verdict enum: PASS | FAIL -->

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| {{RF_PLACEHOLDER:ITEM_NUM}} | {{RF_PLACEHOLDER:ITEM_CHECK}} | {{RF_PLACEHOLDER:ITEM_RESULT}} | {{RF_PLACEHOLDER:ITEM_EVIDENCE}} |
{{RF_PLACEHOLDER:ITEMS_REVIEWED_ROW}}

<!-- One row per scope area/research file checked for coverage; Check names the scope area, Evidence cites the research file/section verified against. -->

## Summary

- **Checks passed:** {{RF_PLACEHOLDER:CHECKS_PASSED}} / {{RF_PLACEHOLDER:CHECKS_TOTAL}}
- **Checks failed:** {{RF_PLACEHOLDER:CHECKS_FAILED}}
- **Critical issues:** {{RF_PLACEHOLDER:CRITICAL_ISSUES_COUNT}}

## Issues Found

| # | Gap | Where Expected | Severity | Notes |
|---|-----|-----------------|----------|-------|
| {{RF_PLACEHOLDER:GAP_NUM}} | {{RF_PLACEHOLDER:GAP_DESCRIPTION}} | {{RF_PLACEHOLDER:GAP_WHERE_EXPECTED}} | {{RF_PLACEHOLDER:GAP_SEVERITY}} | {{RF_PLACEHOLDER:GAP_NOTES}} |
{{RF_PLACEHOLDER:ISSUES_FOUND_ROW}}

<!-- Severity enum: CRITICAL | IMPORTANT | MINOR. Canonical gap shape: missed coverage area, findings too vague to act on, missing integration point, missing test/verification coverage. -->

## Confidence Gate

<!-- MANDATORY section (rf-qa.md:471-521 Confidence Gate Protocol). Confidence is
     COMPUTED as VERIFIED / (TOTAL - UNVERIFIABLE) * 100, NEVER self-assessed.
     Omitting this section breaks the gate. -->

- **Confidence:** "Verified: {{RF_PLACEHOLDER:CONF_VERIFIED}}/{{RF_PLACEHOLDER:CONF_TOTAL}} | Unverifiable: {{RF_PLACEHOLDER:CONF_UNVERIFIABLE}} | Unchecked: {{RF_PLACEHOLDER:CONF_UNCHECKED}} | Confidence: {{RF_PLACEHOLDER:CONF_PERCENT}}%"
- **Tool engagement:** "Read: {{RF_PLACEHOLDER:TOOL_READ_COUNT}} | Grep: {{RF_PLACEHOLDER:TOOL_GREP_COUNT}} | Glob: {{RF_PLACEHOLDER:TOOL_GLOB_COUNT}} | Bash: {{RF_PLACEHOLDER:TOOL_BASH_COUNT}}"

**Unchecked items (with reason):**
- {{RF_PLACEHOLDER:UNCHECKED_ITEM}} (reason: {{RF_PLACEHOLDER:UNCHECKED_ITEM_REASON}})
{{RF_PLACEHOLDER:UNCHECKED_ITEM_ROW}}

**Unverifiable items (with blocker):**
- {{RF_PLACEHOLDER:UNVERIFIABLE_ITEM}} (blocker: {{RF_PLACEHOLDER:UNVERIFIABLE_ITEM_BLOCKER}})
{{RF_PLACEHOLDER:UNVERIFIABLE_ITEM_ROW}}

## QA Complete

VERDICT: {{RF_PLACEHOLDER:FINAL_VERDICT}}
