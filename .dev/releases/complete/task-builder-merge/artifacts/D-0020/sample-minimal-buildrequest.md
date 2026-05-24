---
id: "TASK-RF-20260517-MINIMAL-FIXTURE"
title: "Minimal-BUILD_REQUEST Degradation Sample (T02.05 evidence)"
description: "Sample MDTM demonstrating the References-only degraded form of the Execution Context block under a minimal (GOAL-only) BUILD_REQUEST. Used by T02.05 to validate R-038 degradation rule and R-039 header-wide hidden-input guard."
status: "🟡 To Do"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-05-17"
updated_date: "2026-05-17"
assigned_to: "orchestrator"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "1h"
task_type: static
related_docs: []
tags:
- "dm-001"
- "fr-conv-2"
- "degradation"
- "minimal-buildrequest"
---

# Minimal-BUILD_REQUEST Degradation Sample (T02.05 evidence)

## Task Overview

Sample MDTM rendered by the task-builder under a minimal BUILD_REQUEST whose only populated rollup-signal field is GOAL. WHY is empty; related_docs is empty; QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS / TESTING_REQUIREMENTS are absent; research/ contains a single one-page note that surfaces fewer than three distinct source areas. Per the R-038 degradation rule, the `## Execution Context` block degenerates to a single `**References:**` bullet — the Source areas and Key constraints bullets are physically absent from the rendered block. This file is the artifact T02.05's grep and absence assertions scan.

## Key Objectives

- Confirm the degraded References-only block omits Source areas and Key constraints bullets (R-038).
- Confirm the header-wide hidden-input guard satisfies `grep -cE "src/|/.*:[0-9]+"` returning 0 across the block range (R-039).
- Confirm TB-Add-7 emits the `tb-add-7-degraded-tolerated` verdict against this fixture (no FAIL).

## Prerequisites & Dependencies

- T02.01 PASS (FR-CONV.2 wrapper landed; D-0016).
- T02.02 PASS (DM-001 emitters wired; D-0017).
- DM-001 contract-freeze ratified (T01.13 / D-0011).
- TB-Add-7 / TB-Add-8 cross-validators from M1 active.

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-001: Wire the minimal-BUILD_REQUEST degradation sample so the References-only form is rendered with Source areas and Key constraints bullets absent (not blank).

---

## Phase 1: Verify degraded form

- [ ] **1.1 — Assert Source areas bullet is absent**
  - **Context**: The R-038 degradation rule requires the Source areas bullet to be physically removed under minimal BUILD_REQUEST, not rendered as a blank or stub bullet. See the EXECUTION CONTEXT BLOCK narrative in the task-builder skill body for the rule text and the header-wide guard specification.
  - **Action**: Extract the block range and run `grep -c "Source areas:" <range>`.
  - **Output**: Grep count captured in `evidence.md`.
  - **Verification**: Count is 0.
  - **Completion gate**: Once grep returns 0, mark complete.

- [ ] **1.2 — Assert Key constraints bullet is absent**
  - **Context**: The R-038 degradation rule requires the Key constraints bullet to be physically removed under minimal BUILD_REQUEST. See the EXECUTION CONTEXT BLOCK narrative in the task-builder skill body.
  - **Action**: Extract the block range and run `grep -c "Key constraints:" <range>`.
  - **Output**: Grep count captured in `evidence.md`.
  - **Verification**: Count is 0.
  - **Completion gate**: Once grep returns 0, mark complete.

- [ ] **1.3 — Run header-wide hidden-input guard**
  - **Context**: The R-039 header-wide guard requires `grep -cE "src/|/.*:[0-9]+"` against the entire block range (heading line through closing `---`) to return 0, applied uniformly to the fully-populated and degraded forms. See the task-builder skill body for the guard rule text.
  - **Action**: Extract the block range and run `grep -cE "src/|/.*:[0-9]+"` against it.
  - **Output**: Grep count captured in `evidence.md`.
  - **Verification**: Count is 0.
  - **Completion gate**: Once grep returns 0, mark complete.

---

## Phase 2: Final

- [ ] **2.1 — Update task status to Done**
  - **Context**: All phases complete; this fixture is consumed by the T02.05 evidence file.
  - **Action**: Update frontmatter status, set completion_date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows Done.
  - **Completion gate**: Task marked complete.

---

## Task Log / Notes

### Execution Log

### Phase Findings

### Follow-Up Items
