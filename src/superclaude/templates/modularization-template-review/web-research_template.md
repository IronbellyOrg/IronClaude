---
# --- Identity (MDTM-standard) ---
id: "TMPL-SPEC-web-research"
title: "web-research_template"
description: "Shared report template for /task-builder A.8.5 web research agent output files: per-finding source URL, relevance rating, and provenance."
version: "1.0.0"
status: "draft"
type: "📝 Template"
priority: "🔼 High"
created_date: "2026-07-01"
updated_date: "2026-07-01"
# --- Authoring provenance (MDTM-standard) ---
assigned_to: "TASK-RF-templated-reports-20260701-171419 Step 2.10"
autogen: true
autogen_method: "/task executor, templated-reports retrofit Phase 2"
autogen_source: []
autogen_version: ""
coordinator: "/task executor"
parent_doc: "templates/INDEX.md"
parent_task: "TASK-RF-templated-reports-20260701-171419"
depends_on: []
spec_path: ".claude/skills/task-builder/SKILL.md:930-971 (A.8.5 web research agent)"
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
template_name: "Web Research"
template_version: "1.0.0"
sections: 3
placeholder_prefix: "RF_PLACEHOLDER"
spec_id: "SPEC-web-research-report"
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
This is the /task-builder A.8.5 web research agent output file. 1-2 web
research agents are spawned in parallel, only when the tier allows web agents
AND the quality gate identified external knowledge gaps codebase research
cannot fill.

SCOPE:
This template covers ONLY external (web) research. Codebase research uses
codebase-research_template.md instead.

THE SECTIONS (header block plus 3 required `##` sections):
- header block (Topic, Date, Status) -- prose, not a counted section
1. Findings -- per-finding table, every row carrying Source URL, Relevance, Provenance
2. Key External Findings -- bullet list of the most important discoveries
3. Recommendations from External Research -- how external findings should inform the task file

PROVENANCE VOCABULARY (closed set, mandatory on every finding row):
- tavily -- retrieved via the Tavily MCP tools
- web_search_fallback -- retrieved via WebSearch after Tavily was unavailable
- web_fetch_fallback -- retrieved via WebFetch after Tavily was unavailable

RELEVANCE VOCABULARY (closed set):
- HIGH | MEDIUM | LOW

PLACEHOLDER DISCIPLINE:
- Single-value slots: `{{RF_PLACEHOLDER:NAME}}`
- Repeating-row markers: `{{RF_PLACEHOLDER:NAME_ROW}}` placed on its own line
  directly beneath one filled example row

WRITING DISCIPLINE:
- No em dashes (U+2014) or en-dash ranges (U+2013) anywhere in filled output
- Every finding row MUST carry a Source URL, a Relevance rating, and a Provenance tag
################################################################################ -->

## PART 2: THE WEB RESEARCH SCAFFOLD (copy everything below this line)

# Web Research: {{RF_PLACEHOLDER:TOPIC}}

- **Date:** {{RF_PLACEHOLDER:DATE}}
- **Status:** {{RF_PLACEHOLDER:STATUS}}

---

## Findings

| Finding | Source URL | Relevance | Provenance |
|---------|------------|-----------|------------|
| {{RF_PLACEHOLDER:FINDING_TEXT}} | {{RF_PLACEHOLDER:FINDING_SOURCE_URL}} | {{RF_PLACEHOLDER:FINDING_RELEVANCE}} | {{RF_PLACEHOLDER:FINDING_PROVENANCE}} |
{{RF_PLACEHOLDER:FINDINGS_ROW}}

<!-- Relevance is EXACTLY one of: HIGH | MEDIUM | LOW. Provenance is EXACTLY one of: tavily | web_search_fallback | web_fetch_fallback. -->

## Key External Findings

{{RF_PLACEHOLDER:KEY_EXTERNAL_FINDINGS_BODY}}

## Recommendations from External Research

{{RF_PLACEHOLDER:RECOMMENDATIONS_BODY}}
