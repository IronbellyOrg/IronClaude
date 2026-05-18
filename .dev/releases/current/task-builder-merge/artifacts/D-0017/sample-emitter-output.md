---
id: "TASK-RF-20260517-DM001-EMITTERS"
title: "DM-001 Emitter Sample (T02.02 evidence)"
description: "Sample MDTM demonstrating References / Source areas / Key constraints emitters rendered for a fully-populated BUILD_REQUEST."
status: "🟡 To Do"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-05-17"
updated_date: "2026-05-17"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "1h"
task_type: static
related_docs:
- description: "DM-001 contract-freeze (T01.13 / D-0011)"
- description: "Roadmap rows R-033 / R-034 / R-035 (DM-001.References / SourceAreas / KeyConstraints)"
tags:
- "dm-001"
- "fr-conv-2"
---

# DM-001 Emitter Sample (T02.02 evidence)

## Task Overview

Sample MDTM rendered against the post-T02.02 emitter rules in the task-builder SKILL.md EXECUTION CONTEXT BLOCK narrative. Demonstrates the three DM-001 emitters producing a fully-populated `## Execution Context` block. The header range below is the artifact that the T02.02 grep acceptance test scans.

## Key Objectives

- References emitter renders `R-###: <ref-line>` entries from GOAL / WHY / related-doc IDs.
- Source areas emitter renders module/package names with no file paths (NFR-CONV.3).
- Key constraints emitter renders 1–3 entries pulled verbatim from BUILD_REQUEST.

## Prerequisites & Dependencies

- T02.01 PASS (FR-CONV.2 wrapper landed; D-0016).
- DM-001 contract-freeze ratified (T01.13 / D-0011).

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-001: Implement DM-001 emitters (References, SourceAreas, KeyConstraints); R-002: DM-001 fields populated from BUILD_REQUEST — References as R-### list, Source areas without file paths, Key constraints one to three entries verbatim; R-003: R-033; R-004: R-034; R-005: R-035.
- **Source areas:** rf-task-builder agent prompt, task-builder skill body, MDTM Output Structure template, DM-001 frozen contract.
- **Key constraints:** Header carries no specific path or line citations; References list never blank; Key constraints bounded to one through three entries pulled verbatim from BUILD_REQUEST.

---

## Phase 1: Confirm emitters render under grep

- [ ] **1.1 — Run hidden-input grep against header range**
  - **Context**: Block sits between the `## Execution Context` heading and the next horizontal rule. See the task-builder skill body for the EXECUTION CONTEXT BLOCK narrative containing the three named emitters.
  - **Action**: Extract the header range and run `grep -cE "src/|/.*:[0-9]+"`.
  - **Output**: Grep count captured in `evidence.md`.
  - **Verification**: Count is 0.
  - **Completion gate**: Once grep returns 0, mark complete.

---

## Phase 2: Final

- [ ] **2.1 — Update task status to Done**
  - **Context**: All phases complete.
  - **Action**: Update frontmatter status, set completion_date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows Done.
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log

### Phase Findings

### Follow-Up Items
