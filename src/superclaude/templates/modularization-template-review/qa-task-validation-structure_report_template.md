---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-task-validation-structure"
title: "qa-task-validation-structure_report_template"
description: "Shared report template for the /task-builder A.10 task file validation gate's phase structure/ordering lens (Agent 2): frontmatter, section presence, phase dependencies, and the TB-Add structural gate additions."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.17"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on:
  - "qa-lens_report_template.md"
spec_path: ".claude/skills/task-builder/SKILL.md:1362-1404 (A.10 Agent 2 phase structure/ordering lens)"
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
template_name: "QA Task Validation Structure"
template_version: "1.0.0"
sections: 6
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-task-validation-structure-report"
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
This is the /task-builder A.10 task file validation gate's phase
structure/ordering report, produced by Agent 2 of the 2-agent structural
lens set (both rf-qa). This lens verifies task file frontmatter, mandatory
sections, phase dependency ordering, anti-orphaning, and the TB-Add-1/3-8
structural gate additions (placeholder scan, clarification adjacency,
circular dependency detection, granularity, verification format
consistency, execution-context binding).

SCOPE:
This is a specialization of the qa-lens_report_template.md shape, narrowed
to the same 6 sections used by the A.10 B2-self-containment lens template
(qa-task-validation-b2_report_template.md, its sibling A.10 lens): no
Actions Taken or Recommendations sections; this is a report-only lens,
`fix_authorization: false` per SKILL.md:1365 -- fixes are applied by a
separate serialized fix agent, not by this lens.

THE SECTIONS (fixed order, all 6 required):
1. Overall Verdict -- PASS or FAIL for this lens
2. Items Reviewed -- one row per structure/phase-ordering criterion checked against the task file
3. Summary -- checks passed/total, checks failed, critical issues
4. Issues Found -- one row per finding (e.g. malformed frontmatter, circular dependency), severity and required fix
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

## PART 2: THE QA TASK VALIDATION STRUCTURE SCAFFOLD (copy everything below this line)

# QA Task Validation Structure - {{RF_PLACEHOLDER:PHASE}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** task-validation-structure
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}} / 3

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

## Items Reviewed

<!-- one row per structure/ordering criterion checked, e.g. frontmatter complete, mandatory sections present, phase dependencies acyclic, phase ordering logical, no parent-before-child checkboxes, task completion items inside final phase, Task Log present, gate placement (M3/M4) correct -->

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| {{RF_PLACEHOLDER:ITEM_NUM}} | {{RF_PLACEHOLDER:CHECK}} | {{RF_PLACEHOLDER:RESULT}} | {{RF_PLACEHOLDER:EVIDENCE}} |
{{RF_PLACEHOLDER:ITEM_ROW}}

## Summary

{{RF_PLACEHOLDER:SUMMARY}}

## Issues Found

<!-- canonical issue shape: phase out of logical order, checkbox references a child before its parent phase, gate missing or misplaced, task-completion item stranded outside the final phase, circular phase dependency -->

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|---------------|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:SEVERITY}} | {{RF_PLACEHOLDER:LOCATION}} | {{RF_PLACEHOLDER:ISSUE}} | {{RF_PLACEHOLDER:REQUIRED_FIX}} |
{{RF_PLACEHOLDER:ISSUE_ROW}}

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
