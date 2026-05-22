---
id: "TASK-RF-20260517-TEST004-FULL"
title: "TEST-004 Fully-populated Execution Context Fixture"
description: "Generated MDTM with a fully-populated `## Execution Context` block — all three DM-001 labeled bullets (References, Source areas, Key constraints) present. Backs T02.09 / TEST-004 (R-043) assertion that the block renders all 3 labeled lines for fully-populated BUILD_REQUEST inputs."
status: "🟡 To Do"
type: "🧪 Test"
priority: "🔼 High"
created_date: "2026-05-17"
updated_date: "2026-05-17"
assigned_to: "tests/audit"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "n/a"
task_type: static
related_docs:
- description: "DM-001 contract-freeze (T01.13 / D-0011)"
- description: "Roadmap rows R-043 (TEST-004 fully-populated assertion)"
tags:
- "test-004"
- "fr-conv-2"
- "fully-populated"
---

# TEST-004 Fully-populated Execution Context Fixture

## Task Overview

Frozen MDTM fixture mirroring a fully-populated `## Execution Context` rollup. Used by `tests/audit/test_execution_context_full.py` to assert all three DM-001 labeled bullets are present in the header block, in order, and that the block sits between the frontmatter section and the first `### T<PP>.<TT>` phase task.

## Key Objectives

- References emitter renders `R-###: <ref-line>` entries from GOAL / WHY / related-doc IDs (R-033).
- Source areas emitter renders module/package names with no file paths (R-034 + NFR-CONV.3).
- Key constraints emitter renders 1–3 entries pulled verbatim from BUILD_REQUEST (R-035).

## Prerequisites & Dependencies

- T02.01 PASS (FR-CONV.2 wrapper landed; D-0016).
- T02.02 PASS (DM-001 emitters wired; D-0017).
- DM-001 contract-freeze ratified (T01.13 / D-0011).

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-001: Implement DM-001 emitters (References, SourceAreas, KeyConstraints); R-002: DM-001 fields populated from BUILD_REQUEST — References as R-### list, Source areas without file paths, Key constraints one to three entries verbatim; R-003: R-033; R-004: R-034; R-005: R-035.
- **Source areas:** rf-task-builder agent prompt, task-builder skill body, MDTM Output Structure template, DM-001 frozen contract.
- **Key constraints:** Header carries no specific path or line citations; References list never blank; Key constraints bounded to one through three entries pulled verbatim from BUILD_REQUEST.

---

### T01.01 — Confirm emitters render the labeled bullets

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | TEST-004 fixture asserts all 3 labeled lines present for fully-populated BUILD_REQUEST. |
| Effort | XS |
| Risk | Low |
| Tier | LIGHT |

**Steps:**

1. **[VERIFICATION]** Extract the byte range between the `## Execution Context` heading and the closing `---`.
2. **[VERIFICATION]** Confirm a `**References:**` bullet line is present in that range.
3. **[VERIFICATION]** Confirm a `**Source areas:**` bullet line is present.
4. **[VERIFICATION]** Confirm a `**Key constraints:**` bullet line is present.

**Acceptance Criteria:**

- Header range contains exactly one of each of the three labeled bullets, in declared order.
- Per-item Context fields (this T01.01 step) remain the evidence venue and may carry `file:line` citations independently of the header.

---

## Task Log / Notes

### Execution Log

(none — frozen fixture)
