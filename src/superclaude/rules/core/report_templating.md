---
title: Templated Reports Canonical Rule
description: Defines the mandatory stub-first procedure for every report produced by any agent, skill, gate, or human in this harness, generalizing the task-file-only Template Usage Protocol to all reports.
id: "report-templating"
sidebar_position: 3
created_date: "2026-07-01"
last_updated: "2026-07-01"
version: 1.0.0
draft: false
content_status: Published
tags:
- "report-templating"
- "quality-gates"
- validation
- standards
content_type: CoreConcept
target_audience:
- Developer
- ComponentDeveloper
- SystemDesigner
- SystemArchitect
- QAEngineer
- AI
- Machine
owner: "qa-team"
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
source_references:
- path: ".dev/tasks/to-do/skill-eval-harness/SPEC-1-templated-reports-canonical-rule-20260701.md"
  type: spec_doc
  version_hash: ""
  description: "SPEC-1 section 1, the canonical rule, reproduced verbatim below."
related_links:
- text: IB Agent Core
  link: ~/.claude/rules/core/ib_agent_core.md
- text: Quality Gates
  link: ~/.claude/rules/core/quality_gates.md
- text: File Conventions
  link: ~/.claude/rules/core/file_conventions.md
related_task_id:
- "TASK-RF-templated-reports-20260701-171419"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
---

# Templated Reports Canonical Rule

## 1. The canonical rule (NON-NEGOTIABLE)

Every report of every kind, produced by any agent, skill, gate, or human anywhere in this harness, MUST be created by the STUB-FIRST procedure:
1. **READ** the governing template.
2. **STUB** immediately: write the report file with the template's frontmatter/header + full section skeleton + explicit `{{RF_PLACEHOLDER:*}}` (or `<!-- TODO -->`) placeholders, BEFORE gathering content.
3. **POPULATE** incrementally in place, replacing each placeholder as that section's work completes. Never accumulate the whole report for one terminal write.
4. **NO FREEFORM REPORTS.** A report whose structure does not derive from a registered template FAILS its gate like a missing output.

"Report" = any produced artifact whose purpose is to communicate findings, status, verification, inventory, or results (the 41 in the audit). Generalizes the task-file-only Template Usage Protocol to ALL reports.
