---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-qa-qualitative-sufficiency"
title: "qa-qualitative-sufficiency_report_template"
description: "Shared report template for the /task-builder A.10.5 Agent 2 rf-qa-qualitative QA-gate-sufficiency lens: verifies a generated task file encodes the required QA-gate agent floors, validation items, and testing items."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.20"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on:
  - "qa-lens_report_template.md"
  - "qa-qualitative-operational_report_template.md"
spec_path: ".claude/skills/task-builder/SKILL.md:1475-1492 (A.10.5 Agent 2 QA-gate-sufficiency lens), .claude/agents/rf-qa-qualitative.md:819-891 (Output Format), 914-967 (Confidence Gate Protocol)"
related_docs:
  - ".claude/templates/reports/qa-lens_report_template.md"
  - ".claude/templates/reports/qa-qualitative-operational_report_template.md"
  - ".claude/agents/rf-qa-qualitative.md"
  - ".claude/skills/task-builder/SKILL.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - qa-report
  - template
  - task-integrity
  - task-qualitative
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "QA Qualitative Sufficiency"
template_version: "1.0.0"
sections: 9
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-qa-qualitative-sufficiency-report"
family: "templated-reports"
component_type: "template"
externalize_status: "ANTICIPATORY"
consumers:
  - "task-builder" # status: confirmed
  - "task" # status: confirmed
---

<!-- ################################################################################
##  PART 1: AUTHORING / FILL INSTRUCTIONS
##  (this comment block is never copied into a filled-out report; it exists only
##  to guide whoever or whatever fills the template)
################################################################################

WHAT THIS IS:
This is the sibling of qa-qualitative-operational_report_template.md,
consumed by /task-builder A.10.5 Agent 2 (QA-gate-sufficiency lens).
Where Agent 1 checks whether the task file would operationally succeed
if executed, Agent 2 checks whether the task file's OWN QA gates are
adequate: too few agents at a gate, missing lens-based QA patterns,
missing source fidelity gates. This is the enforcement mechanism that
closes the QA hardening loop (SKILL.md:1482) -- the reason the
min-6-agents floor and I19 intermediate-gate floors are actually upheld
in generated task files.

SCOPE:
Identical section shape and placeholder discipline to
qa-qualitative-operational_report_template.md (same rf-qa-qualitative
task-qualitative Output Format, same AX-1..AX-5 axes, same Self-Audit
INV-019 obligation, same Confidence Gate Protocol) -- both agents share
one unified output format per rf-qa-qualitative.md:819-891. Only the
CONTENT of the Items Reviewed checks and Issues Found rows differs:
this lens checks gate agent counts, lens coverage, and fidelity-gate
presence rather than operational correctness.

THE SECTIONS (fixed order, all 9 required):
1. Overall Verdict -- PASS or FAIL for this lens
2. Items Reviewed -- one row per QA-gate-sufficiency check, WITH the axis column
3. Summary -- pass/fail counts, critical issues, PLUS the Axis lens status bullet
4. Issues Found -- one row per finding, severity and required fix
5. Actions Taken -- fixes applied in-place, only if fix_authorization is true
6. Self-Audit -- (a) Reliance list + (b) Independent semantic checks (>=1 required, INV-019); heading may alternatively read "Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)"
7. Recommendations -- actions needed before the next phase/step can proceed
8. Confidence Gate -- the MANDATORY computed-confidence block (never self-assessed)
9. QA Complete -- closing marker plus the final VERDICT line

AXIS COLUMN VOCABULARY (closed set, PR-07 canonical annotation rules):
`AX-1` (drift) | `AX-2` (contradictions) | `AX-3` (omissions) |
`AX-4` (weakened-criteria) | `AX-5` (invented-content) | `none`.
`none` = the axis lens was applied and nothing fired (used on PASS rows).
One of AX-1..AX-5 = that axis fired (used on FAIL rows). N/A is FORBIDDEN
in this column. `drift-axis-inactive` is a Summary-block annotation only,
never a value in the axis column itself.

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Verdict is EXACTLY one of: PASS | FAIL
- Severity is EXACTLY one of: CRITICAL | IMPORTANT | MINOR
- Self-Audit category (b) MUST have at least 1 entry (INV-019); zero entries
  is a violation regardless of category (a) contents
- Confidence and coverage figures are COMPUTED per the Confidence Gate
  Protocol (rf-qa-qualitative.md:914-967), never self-assessed
################################################################################ -->

## PART 2: THE QA QUALITATIVE SUFFICIENCY SCAFFOLD (copy everything below this line)

# QA Report - {{RF_PLACEHOLDER:PHASE}} - {{RF_PLACEHOLDER:LENS}}

- **Topic:** {{RF_PLACEHOLDER:TOPIC}}
- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Phase:** {{RF_PLACEHOLDER:PHASE}}
- **Lens:** qa-gate-sufficiency
- **Fix cycle:** {{RF_PLACEHOLDER:FIX_CYCLE}}
- **fix_authorization:** {{RF_PLACEHOLDER:FIX_AUTHORIZATION}}

## Overall Verdict: {{RF_PLACEHOLDER:VERDICT}}

## Items Reviewed

<!-- one row per QA-gate-sufficiency check: does every phase-gate/intermediate-gate meet its minimum agent floor (6 at phase gates, 5 at intermediate gates per I19), does every gate mix the required lens types (structural + qualitative, plus analyst at intermediate gates), does every phase-producing-output gate include the source-document fidelity gate (M4) where the phase reads a spec/PRD/research file, does every phase include the required validation items (ensuring clauses) and testing items (grep/wc verification steps); axis is REQUIRED on every row -->

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| {{RF_PLACEHOLDER:ITEM_NUM}} | {{RF_PLACEHOLDER:CHECK}} | {{RF_PLACEHOLDER:AXIS}} | {{RF_PLACEHOLDER:RESULT}} | {{RF_PLACEHOLDER:EVIDENCE}} |
{{RF_PLACEHOLDER:ITEM_ROW}}

## Summary

- **Checks passed / total:** {{RF_PLACEHOLDER:CHECKS_PASSED}} / {{RF_PLACEHOLDER:CHECKS_TOTAL}}
- **Checks failed:** {{RF_PLACEHOLDER:CHECKS_FAILED}}
- **Critical issues:** {{RF_PLACEHOLDER:CRITICAL_COUNT}}
- **Issues fixed in-place:** {{RF_PLACEHOLDER:FIXED_COUNT}}
- **Axis lens status:** {{RF_PLACEHOLDER:AXIS_LENS_STATUS}} <!-- note drift-axis-inactive here (not in the axis column) if the AX-1 drift baseline is absent -->

## Issues Found

<!-- canonical issue shape: a phase-gate or intermediate gate below its minimum agent floor, a gate missing a required lens type (e.g. no rf-qa-qualitative at an intermediate gate), a phase reading a spec/PRD/research file with no M4 fidelity gate, a checklist item missing its verification (ensuring) clause, a QA gate missing the Serialized Fix Protocol step -->

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|---------------|
| {{RF_PLACEHOLDER:ISSUE_NUM}} | {{RF_PLACEHOLDER:SEVERITY}} | {{RF_PLACEHOLDER:LOCATION}} | {{RF_PLACEHOLDER:ISSUE}} | {{RF_PLACEHOLDER:REQUIRED_FIX}} |
{{RF_PLACEHOLDER:ISSUE_ROW}}

## Actions Taken

{{RF_PLACEHOLDER:ACTIONS_TAKEN}} <!-- only populated when fix_authorization is true; otherwise state "None (report-only lens)" -->

## Self-Audit

<!-- alternate heading permitted: "Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)" -->

**(a) Reliance list (rf-qa PASS items skipped for re-checking):**

- {{RF_PLACEHOLDER:RELIANCE_ITEM}}
{{RF_PLACEHOLDER:RELIANCE_ROW}}

**(b) Independent semantic checks (at least 1 required, INV-019):**

- {{RF_PLACEHOLDER:SEMANTIC_CHECK}}
{{RF_PLACEHOLDER:SEMANTIC_CHECK_ROW}}

## Recommendations

{{RF_PLACEHOLDER:RECOMMENDATIONS}}

## Confidence Gate

<!-- MANDATORY section (rf-qa-qualitative.md:914-967 Confidence Gate Protocol, same COMPUTED
     confidence machinery as rf-qa). Confidence is COMPUTED as VERIFIED / (TOTAL - UNVERIFIABLE) * 100,
     NEVER self-assessed. Omitting this section breaks the gate. -->

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
