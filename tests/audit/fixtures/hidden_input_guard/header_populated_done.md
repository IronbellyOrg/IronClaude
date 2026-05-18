---
id: "TASK-RF-20260518-T0708-HIDDEN-INPUT-POPULATED-DONE"
title: "TEST-023 Hidden-input Determinism Fixture — Populated done/ Twin"
description: "Frozen synthetic Execution Context block representing what rf-task-builder emits for the SAME controlled BUILD_REQUEST as `header_empty_done.md` when `.dev/tasks/done/` carries ≥10 prior TASK-RF-* directories spanning ≥3 distinct task_types (the OPEN-PR05 re-evaluation threshold). The `## Execution Context` byte range and the structural per-item fields MUST be byte-identical to the empty-done baseline (TEST-023 contract). Backs T07.08 / D-0089."
status: "🟡 To Do"
type: "🧪 Test"
priority: "🔼 High"
created_date: "2026-05-18"
updated_date: "2026-05-18"
assigned_to: "tests/audit"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "n/a"
task_type: static
related_docs:
- description: "NFR-CONV.3 hidden-input determinism (release-spec NFR row 9 — R-148)"
- description: "TEST-023 fixture row (release-spec test row — R-149)"
- description: "PR-05 Tier-History Advisory — DEFERRED to Phase-2 (release-spec §2.1)"
- description: "OPEN-PR05 re-evaluation trigger — `.dev/tasks/done/` ≥10 of ≥3 task_types"
tags:
- "t07-08"
- "test-023"
- "nfr-conv-3"
- "hidden-input"
- "populated-done"
---

# TEST-023 Hidden-input Determinism — Populated done/ Twin

## Task Overview

Frozen MDTM fixture mirroring the structural output rf-task-builder
emits when `.dev/tasks/done/` is populated with ≥10 prior TASK-RF-*
directories spanning ≥3 distinct task_types (the OPEN-PR05
re-evaluation trigger). This is the populated arm of the NFR-CONV.3
hidden-input determinism contract: the `empty-done` baseline
(`header_empty_done.md`) MUST be byte-identical in its structural
output to this file. Any byte drift between the two indicates that
hidden-input has leaked into structural emission — which would be
an NFR-CONV.3 violation and a PR-05 (Tier-History Advisory)
reactivation signal.

## Key Objectives

- Execution Context block emits the three labeled bullets per DM-001 (References, Source areas, Key constraints) in declared order.
- No file path or `file:line` citation appears inside the `## Execution Context` byte range (R-039 / NFR-CONV.3).
- The `## Execution Context` byte range is byte-identical to `header_empty_done.md` byte-for-byte (TEST-023 primary assertion).

## Execution Context

<!-- OPTIONAL header — frozen fixture for TEST-023 hidden-input determinism. The block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. -->

- **References:** R-147: NFR-CONV-R1 first-cycle PASS rate baseline; R-148: NFR-CONV.3 hidden-input determinism guard; R-149: TEST-023 hidden-input fixture; R-039: header no-file-paths invariant.
- **Source areas:** rf-task-builder agent prompt, task-builder skill body, DM-001 frozen contract, hidden-input determinism guard.
- **Key constraints:** Header carries no specific path or line citations; References list is never blank; Key constraints bounded to one through three entries pulled verbatim from BUILD_REQUEST.

---

### T01.01 — Confirm structural output is independent of done/ state

| Field | Value |
|---|---|
| Roadmap Item IDs | R-148 |
| Why | TEST-023 fixture asserts byte-identical structural output across populated-done and empty-done states. |
| Effort | XS |
| Risk | Low |
| Tier | LIGHT |

**Steps:**
1. **[VERIFICATION]** Read both fixtures.
2. **[VERIFICATION]** Compare byte sequences.
3. **[VERIFICATION]** Assert equality.

**Acceptance Criteria:**
- Both fixtures yield identical bytes.
- Per-item Context fields remain the evidence venue and may carry `file:line` citations independently of the header (NFR-CONV.7 scope confinement).

---

## Task Log / Notes

### Execution Log
(none — frozen fixture)
