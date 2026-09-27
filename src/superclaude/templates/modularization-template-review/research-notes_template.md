---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-research-notes"
title: "research-notes_template"
description: "Shared report template for the /task-builder A.4 scope-discovery research notes file, the fixed 7-category skeleton the builder reads before spawning researchers."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.8"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/skills/task-builder/SKILL.md:410-450 (A.4 Research Notes)"
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
template_name: "Research Notes"
template_version: "1.0.0"
sections: 7
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-research-notes-report"
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
This is the /task-builder A.4 scope-discovery research notes file. It is the
ONLY input the builder reads for scope discovery -- NOT inline content in the
BUILD_REQUEST. It is written BEFORE researchers are spawned (A.5-A.8).

SCOPE:
This template covers ONLY the fixed 7-category scope-discovery skeleton
(task-builder/SKILL.md:414-450). It does NOT cover the per-researcher output
files those researchers produce afterward (that is
codebase-research_template.md / web-research_template.md).

THE SECTIONS (fixed order, all 7 required, include every category even if
marking it "N/A" for an empty category):
1. EXISTING_FILES -- key source files/directories/stubs found during scope discovery
2. PATTERNS_AND_CONVENTIONS -- naming/architecture/design patterns observed
3. GAPS_AND_QUESTIONS -- unknowns and ambiguities requiring investigation
4. RECOMMENDED_OUTPUTS -- research files to create, topics and output paths
5. SUGGESTED_PHASES -- per-researcher assignment detail
6. TEMPLATE_NOTES -- MDTM template + tier selection reasoning
7. AMBIGUITIES_FOR_USER -- genuine ambiguities that cannot be resolved from the codebase

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Categories with no findings are filled with the literal string "N/A", never left blank

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- All 7 categories MUST appear in the filled output, in the fixed order above
################################################################################ -->

## PART 2: THE RESEARCH NOTES SCAFFOLD (copy everything below this line)

# Research Notes: {{RF_PLACEHOLDER:GOAL}}

- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Scenario:** {{RF_PLACEHOLDER:SCENARIO}}
- **Depth Tier:** {{RF_PLACEHOLDER:DEPTH_TIER}}
- **Track Count:** {{RF_PLACEHOLDER:TRACK_COUNT}}

---

## EXISTING_FILES

{{RF_PLACEHOLDER:EXISTING_FILES_BODY}}

## PATTERNS_AND_CONVENTIONS

{{RF_PLACEHOLDER:PATTERNS_AND_CONVENTIONS_BODY}}

## GAPS_AND_QUESTIONS

{{RF_PLACEHOLDER:GAPS_AND_QUESTIONS_BODY}}

## RECOMMENDED_OUTPUTS

{{RF_PLACEHOLDER:RECOMMENDED_OUTPUTS_BODY}}

## SUGGESTED_PHASES

{{RF_PLACEHOLDER:SUGGESTED_PHASES_BODY}}

## TEMPLATE_NOTES

{{RF_PLACEHOLDER:TEMPLATE_NOTES_BODY}}

## AMBIGUITIES_FOR_USER

{{RF_PLACEHOLDER:AMBIGUITIES_FOR_USER_BODY}}
