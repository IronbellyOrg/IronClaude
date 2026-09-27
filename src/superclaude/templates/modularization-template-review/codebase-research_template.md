---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-codebase-research"
title: "codebase-research_template"
description: "Shared report template for /task-builder A.7 researcher output files: evidence-based codebase findings, every claim carrying a closed-vocabulary verification tag plus a file:line citation."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.9"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/skills/task-builder/SKILL.md:545-554 (A.7 researcher header)"
related_docs:
  - ".claude/skills/task-builder/SKILL.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - research-report
  - template
  - task-builder
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Codebase Research"
template_version: "1.0.0"
sections: 3
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-codebase-research-report"
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
This is the /task-builder A.7 researcher output file. Each of the 3-8 parallel
researcher agents spawned per build creates one of these, writing findings
incrementally as it explores its assigned scope.

SCOPE:
This template covers ONLY codebase (file-system) research. Web research uses
web-research_template.md instead.

THE SECTIONS (header block plus 3 required `##` sections):
- header block (Topic, Topic type, Scope, Status, Date) -- prose, not a counted section
1. Findings -- the evidence-based body, every claim tagged
2. Gaps -- unresolved unknowns requiring further investigation
3. Key Takeaways -- closing summary

VERIFICATION-TAG VOCABULARY (closed set, mandatory on every claim):
- [CODE-VERIFIED] -- the claim was confirmed by directly reading the cited file:line
- [CODE-CONTRADICTED] -- the claim conflicts with what the cited file:line actually shows
- [UNVERIFIED] -- the claim could not be confirmed against the codebase

Every finding cites actual file paths, line numbers, function/class names. No
assumptions, no inferences, no guessing -- if it cannot be verified, tag it
[UNVERIFIED] rather than presenting it as fact.

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Every findings claim MUST carry exactly one tag from the closed vocabulary above
################################################################################ -->

## PART 2: THE CODEBASE RESEARCH SCAFFOLD (copy everything below this line)

# Research: {{RF_PLACEHOLDER:TOPIC}}

- **Topic type:** {{RF_PLACEHOLDER:TOPIC_TYPE}}
- **Scope:** {{RF_PLACEHOLDER:SCOPE}}
- **Status:** {{RF_PLACEHOLDER:STATUS}}
- **Date:** {{RF_PLACEHOLDER:DATE}}

---

## Findings

{{RF_PLACEHOLDER:FINDING_TAG}} {{RF_PLACEHOLDER:FINDING_CLAIM}} (`{{RF_PLACEHOLDER:FINDING_FILE_LINE}}`)
{{RF_PLACEHOLDER:FINDINGS_ROW}}

<!-- FINDING_TAG is EXACTLY one of: [CODE-VERIFIED] | [CODE-CONTRADICTED] | [UNVERIFIED]. Every claim cites a file:line. -->

## Gaps

{{RF_PLACEHOLDER:GAPS_BODY}}

## Key Takeaways

{{RF_PLACEHOLDER:KEY_TAKEAWAYS_BODY}}
