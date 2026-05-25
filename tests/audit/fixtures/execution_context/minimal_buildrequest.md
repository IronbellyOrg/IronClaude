---
id: "TASK-RF-20260517-TEST005-MINIMAL"
title: "TEST-005 Minimal-BUILD_REQUEST Degradation Fixture"
description: "Generated MDTM whose `## Execution Context` block has degraded to the References-only form because BUILD_REQUEST is minimal (GOAL is the only populated rollup-signal field). Source areas and Key constraints bullets are PHYSICALLY ABSENT — not blank, not stub-bulleted. Backs T02.09 / TEST-005 (R-044)."
status: "🟡 To Do"
type: "🧪 Test"
priority: "🔼 High"
created_date: "2026-05-17"
updated_date: "2026-05-17"
assigned_to: "tests/audit"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "n/a"
task_type: static
related_docs: []
tags:
- "test-005"
- "fr-conv-2"
- "degradation"
- "minimal-buildrequest"
---

# TEST-005 Minimal-BUILD_REQUEST Degradation Fixture

## Task Overview

Frozen MDTM fixture mirroring the R-038 degraded form of the `## Execution Context` block. Used by `tests/audit/test_execution_context_minimal_buildrequest.py` to assert (a) the `**References:**` bullet remains, and (b) the `**Source areas:**` and `**Key constraints:**` bullets are absent from the rendered block (not present-and-blank, not stub-bulleted).

## Key Objectives

- References-only block emitted under minimal BUILD_REQUEST (R-038).
- Source areas bullet physically removed (R-038 — absence, not blanking).
- Key constraints bullet physically removed (R-038 — absence, not blanking).

## Prerequisites & Dependencies

- T02.01 / T02.02 / T02.05 PASS.
- DM-001 contract-freeze ratified (T01.13 / D-0011).

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-001: Wire the minimal-BUILD_REQUEST degradation sample so the References-only form is rendered with Source areas and Key constraints bullets absent (not blank).

---

### T01.01 — Verify degraded form

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | TEST-005 fixture asserts References-only degradation under minimal BUILD_REQUEST. |
| Effort | XS |
| Risk | Low |
| Tier | LIGHT |

**Steps:**

1. **[VERIFICATION]** Extract the byte range between the `## Execution Context` heading and the closing `---`.
2. **[VERIFICATION]** Confirm a `**References:**` bullet line is present in that range.
3. **[VERIFICATION]** Confirm no `Source areas:` bullet line is present in that range.
4. **[VERIFICATION]** Confirm no `Key constraints:` bullet line is present in that range.

**Acceptance Criteria:**

- Header range contains exactly one labeled bullet (`**References:**`).
- `Source areas:` and `Key constraints:` literal substrings are absent from the header range.

---

## Task Log / Notes

### Execution Log

(none — frozen fixture)
