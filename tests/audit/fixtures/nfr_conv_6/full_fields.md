---
id: "TASK-RF-20260518-T0704-FULLFIELDS"
title: "NFR-CONV.6 Full-Fields Composite Fixture (TB-Add-1..8 all PASS)"
description: "Composite fixture exercising the Q-DM-1 resolved 5-field per-item schema {Context, Action, Output, Verification, Completion gate}. Every checklist item is fully populated, so TB-Add-1 (placeholder scan / 5-field schema enforcement) and the remaining TB-Add-2..8 checks all emit PASS. Backs T07.04 / D-0086 — NFR-CONV.6 self-contained-item invariant."
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
- description: "TB-Add-1 rule text in rf-qa.md (placeholder scan / 5-field schema)"
- description: "NFR-CONV.6 roadmap row (self-contained-item invariant)"
- description: "Q-DM-1 resolution: per-item schema {Context, Action, Output, Verification, Completion gate} (rf-qa.md:296)"
tags:
- "t07-04"
- "tb-add-1"
- "nfr-conv-6"
- "q-dm-1"
- "self-contained"
---

# NFR-CONV.6 Full-Fields Composite Fixture

## Task Overview

Frozen MDTM fixture exercising every TB-Add-1..8 structural gate on the
Q-DM-1 resolved 5-field per-item schema. Each checklist item carries
all five fields — Context, Action, Output, Verification, Completion
gate — so the self-contained-item invariant holds. Used by
`tests/audit/test_nfr_conv_6_self_contained.py` to assert the full-fields
variant produces only PASS verdicts across the TB-Add-1..8 catalogue.

## Key Objectives

- All checklist items carry the 5-field schema (Context, Action, Output, Verification, Completion gate).
- No item contains TBD/TODO/FIXME tokens.
- Per-item Context fields cite file:line or carry justified-absence comments.
- Header source areas re-appear in per-item Context fields.

## Prerequisites & Dependencies

- T01.02..T01.11 PASS (TB-Add-1..8 rules wired).
- Q-DM-1 resolved: per-item schema is {Context, Action, Open Question 1 references resolved}.

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-143: NFR-CONV.6 self-contained-item invariant fixture; Q-DM-1 resolution recording the 5-field per-item schema.
- **Source areas:** rf-qa agent prompt, task-builder skill body, MDTM output structure template.
- **Key constraints:** Each item populates Context, Action, Output, Verification, Completion gate; TB-Add-1 fails when any of these five fields is absent.

---

## Phase 1: Self-contained item enforcement

- [ ] **1.1 — Demonstrate 5-field schema (TB-Add-1 PASS expected)**
  - **Context**: The Q-DM-1 resolved per-item schema is defined at `src/superclaude/agents/rf-qa.md:296` and mirrored at `src/superclaude/skills/task-builder/SKILL.md:1134`. Every item must populate all five field labels — Context, Action, Output, Verification, Completion gate — to satisfy the self-contained-item invariant (NFR-CONV.6).
  - **Action**: Keep every field populated; reject placeholder substitutes in any field body.
  - **Output**: A checklist item that visibly carries every one of the five fields and contains no placeholder tokens.
  - **Verification**: TB-Add-1 enumerates this item and emits PASS; the 5-field schema check finds Context, Action, Output, Verification, Completion gate all present.
  - **Completion gate**: PASS verdict emitted; no TB-Add-1 placeholder or title-only error references this item.

- [ ] **1.2 — Cross-validate per-item Context citation (TB-Add-8 PASS expected)**
  - **Context**: TB-Add-8 at `src/superclaude/agents/rf-qa.md:310` requires every per-item Context paragraph that references a code surface to include at least one file:line citation. This item references `src/superclaude/skills/task-builder/SKILL.md:1134` (the TB-Add-1 mirror).
  - **Action**: Preserve the explicit file:line citation in the Context paragraph.
  - **Output**: Per-item Context paragraph carrying at least one file:line token.
  - **Verification**: TB-Add-8 verifier classifies this item as PASS; no evidence-binding error is emitted.
  - **Completion gate**: PASS verdict emitted; the per-item Context citation survives the gate.

- [ ] **1.3 — Cross-validate header source-areas reappearance (TB-Add-7 PASS expected)**
  - **Context**: TB-Add-7 at `src/superclaude/agents/rf-qa.md:308` requires every named source area in the `## Execution Context` `**Source areas:**` line to reappear in at least one item Context field. The header lists "rf-qa agent prompt, task-builder skill body, MDTM output structure template". Items 1.1 and 1.2 both name the rf-qa agent prompt and task-builder skill body in their Context fields, and this item names the MDTM output structure template per the rf-qa.md:296 mirror.
  - **Action**: Keep every header source area present in at least one item Context body.
  - **Output**: All three source-area phrases appear in items 1.1..1.3.
  - **Verification**: TB-Add-7 verifier finds every header source area in at least one item Context; cross-validation emits PASS.
  - **Completion gate**: PASS verdict emitted; header-to-item drift count is zero.

---

## Task Log / Notes

### Execution Log
(none — frozen fixture)
