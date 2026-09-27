---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-task-validation-b2"
title: "qa-task-validation-b2_report_template"
description: "Shared report template for the /task-builder A.10 task file validation gate's B2 self-containment lens (Agent 1): every checklist item must embed context, action, output, verification, and completion gate."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.16"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on:
  - "qa-lens_report_template.md"
spec_path: ".claude/skills/task-builder/SKILL.md:1317-1360 (A.10 Agent 1 B2 self-containment lens)"
related_docs:
  - ".claude/templates/reports/qa-lens_report_template.md"
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
template_name: "QA Task Validation B2"
template_version: "1.0.0"
sections: 6
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-task-validation-b2-report"
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
This is the /task-builder A.10 task file validation gate's B2
self-containment report, produced by Agent 1 of the 2-agent structural
lens set (both rf-qa). This lens verifies every checklist item in the
generated task file is self-contained per MDTM B2: context, action,
output, verification, and completion gate, with no "see above" references.

SCOPE:
This is a specialization of the qa-lens_report_template.md shape, narrowed
to the same 6 sections used by the A.8 research-gate lens templates (no
Actions Taken or Recommendations sections; this is a report-only lens,
`fix_authorization: false` per SKILL.md:1331 -- fixes are applied by a
separate serialized fix agent, not by this lens).

THE SECTIONS (fixed order, all 6 required):
1. Overall Verdict -- PASS or FAIL for this lens
2. Items Reviewed -- one row per B2 checklist criterion checked against the task file
3. Summary -- checks passed/total, checks failed, critical issues
4. Issues Found -- one row per finding (e.g. non-self-contained item), severity and required fix
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

## PART 2: THE QA TASK VALIDATION B2 SCAFFOLD (copy everything below this line)

# QA Task Validation B2 - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** task-validation-b2
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}} / 3

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

<!-- Verdict enum: PASS | FAIL -->

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| {{RF_PLACEHOLDER:ITEM_NUM}} | {{RF_PLACEHOLDER:ITEM_CHECK}} | {{RF_PLACEHOLDER:ITEM_RESULT}} | {{RF_PLACEHOLDER:ITEM_EVIDENCE}} |
{{RF_PLACEHOLDER:ITEMS_REVIEWED_ROW}}

<!-- One row per B2 checklist criterion checked against the task file (e.g. "every item has all 5 B2 components", "no item references prior context without restating it"); Evidence cites the task-file step number verified against. -->

## Summary

- **Checks passed:** {{RF_PLACEHOLDER:CHECKS_PASSED}} / {{RF_PLACEHOLDER:CHECKS_TOTAL}}
- **Checks failed:** {{RF_PLACEHOLDER:CHECKS_FAILED}}
- **Critical issues:** {{RF_PLACEHOLDER:CRITICAL_ISSUES_COUNT}}

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|---------------|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:ISSUE_SEVERITY}} | {{RF_PLACEHOLDER:ISSUE_LOCATION}} | {{RF_PLACEHOLDER:ISSUE_DESCRIPTION}} | {{RF_PLACEHOLDER:ISSUE_REQUIRED_FIX}} |
{{RF_PLACEHOLDER:ISSUES_FOUND_ROW}}

<!-- Severity enum: CRITICAL | IMPORTANT | MINOR. Canonical issue shape: item missing a B2 component, item says "see above"/"continue from previous", batch item covering multiple files, non-measurable verification criteria. -->

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
