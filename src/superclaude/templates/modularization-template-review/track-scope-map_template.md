---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-track-scope-map"
title: "track-scope-map_template"
description: "Optional orchestration-summary template modeling rf-team-lead's TRACK [T] SCOPE MAP fenced block, produced per track at Phase 2c Scope Discovery before spawning researchers."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔽 Low"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.31"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/agents/rf-team-lead.md:148-155 (TRACK [T] SCOPE MAP fenced block, Phase 2c Scope Discovery)"
related_docs:
  - ".claude/agents/rf-team-lead.md"
related_prd: ""
related_tdd: ""
tags:
  - templated-reports
  - rf-team-lead
  - template
  - track-scope-map
template_schema_doc: ".claude/templates/workflow/03_component_authoring_template.md"
ai_model: "claude-sonnet-5"
model_settings: "default effort"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
template_name: "Track Scope Map"
template_version: "1.0.0"
sections: 1
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-track-scope-map"
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
emits per track during Phase 2c (Scope Discovery), before spawning
researchers, per `.claude/agents/rf-team-lead.md:148-155`. This is an
OPTIONAL orchestration summary, not a gated QA/analyst document. Like the
pipeline-complete template, the PART 2 body is a literal reproduction of
the plain-text block, wrapped in a single `##` section marker ONLY so the
`sections` frontmatter integer and template-conformance checks apply
consistently across the library. The `##` heading is NOT part of the
emitted text.

SCOPE:
Byte-order-exact reproduction of the TRACK [T] SCOPE MAP block: the
banner line plus its 5 indented fields (Relevant directories, Key files
found, Patterns/classes identified, Existing docs/templates, Estimated
complexity), per rf-team-lead.md:148-155. The block is a single flat
5-field map with no internally distinct sub-groups, unlike the
pipeline-complete block (which has 3 distinct list/closing-line groups);
it is therefore modeled as ONE wrapper section.

THE SECTIONS (fixed order, single wrapper section, wrapper-only, not emitted text):
1. Track Scope Map -- the banner line plus its 5 indented fields, in fixed order

PLACEHOLDER DISCIPLINE:
- All 6 slots (`TRACK_ID`, `RELEVANT_DIRECTORIES`, `KEY_FILES_FOUND`,
  `PATTERNS_IDENTIFIED`, `EXISTING_DOCS_TEMPLATES`, `ESTIMATED_COMPLEXITY`)
  are single-value `{{RF_PLACEHOLDER:NAME}}` markers; there are no
  repeating-row markers in this template

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- `Estimated complexity` (`ESTIMATED_COMPLEXITY`) is EXACTLY one of: low | medium | high
################################################################################ -->

## PART 2: THE TRACK SCOPE MAP SCAFFOLD (copy everything below this line)

<!-- this scaffold reproduces rf-team-lead's literal TRACK [T] SCOPE MAP
     text output exactly; the ## heading above is wrapper-only structure for
     the sections convention and is NOT part of the emitted report text -->

## Track Scope Map

<!-- one field per line, fixed order, per rf-team-lead.md:148-155 -->

TRACK {{RF_PLACEHOLDER:TRACK_ID}} SCOPE MAP:
  Relevant directories: {{RF_PLACEHOLDER:RELEVANT_DIRECTORIES}}
  Key files found: {{RF_PLACEHOLDER:KEY_FILES_FOUND}}
  Patterns/classes identified: {{RF_PLACEHOLDER:PATTERNS_IDENTIFIED}}
  Existing docs/templates: {{RF_PLACEHOLDER:EXISTING_DOCS_TEMPLATES}}
  Estimated complexity: {{RF_PLACEHOLDER:ESTIMATED_COMPLEXITY}}
