---
id: "TASK-RF-20260518-T0704-STRIPPED"
title: "NFR-CONV.6 Field-Stripped Composite Fixture (TB-Add-1 FAIL expected)"
description: "Composite fixture exercising the Q-DM-1 resolved 5-field per-item schema {Context, Action, Output, Verification, Completion gate} with one field deliberately stripped on item 1.1 (the **Output** field is removed). TB-Add-1 (placeholder scan / 5-field schema enforcement) MUST FAIL on item 1.1 and name the missing field. Backs T07.04 / D-0086 — NFR-CONV.6 self-contained-item invariant negative path."
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
- "negative-path"
---

# NFR-CONV.6 Field-Stripped Composite Fixture

## Task Overview

Frozen MDTM fixture proving TB-Add-1's fail-closed behavior under the
Q-DM-1 resolved 5-field per-item schema. Item 1.1 has the **Output**
field deliberately removed; TB-Add-1 must detect the absence and emit
a FAIL verdict naming the missing field. Used by
`tests/audit/test_nfr_conv_6_self_contained.py` to assert the negative
path of the self-contained-item invariant.

## Key Objectives

- Stripping any one of the five fields from a checklist item MUST cause
  TB-Add-1 to FAIL.
- The FAIL message MUST name the affected item-ID and the missing field
  label, so a downstream operator can resolve the violation deterministically.

## Prerequisites & Dependencies

- T01.02..T01.11 PASS (TB-Add-1..8 rules wired).
- Q-DM-1 resolved: per-item schema is {Context, Action, Output, Verification, Completion gate}.

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-143: NFR-CONV.6 self-contained-item invariant fixture; Q-DM-1 resolution recording the 5-field per-item schema.
- **Source areas:** rf-qa agent prompt, task-builder skill body, MDTM output structure template.
- **Key constraints:** Item 1.1 is missing the **Output** field; TB-Add-1 must FAIL with the item-ID and field label named.

---

## Phase 1: Self-contained item enforcement (negative path)

- [ ] **1.1 — Stripped 5-field schema (TB-Add-1 FAIL expected — Output missing)**
  - **Context**: The Q-DM-1 resolved per-item schema is defined at `src/superclaude/agents/rf-qa.md:296` and mirrored at `src/superclaude/skills/task-builder/SKILL.md:1134`. This item INTENTIONALLY omits the **Output** field to exercise TB-Add-1's fail-closed behavior.
  - **Action**: Do not re-introduce the **Output** field. The negative path requires the field to remain absent.
  - **Verification**: TB-Add-1 verifier enumerates this item, detects the missing **Output** label, and emits a FAIL verdict that names both `1.1` and `Output`.
  - **Completion gate**: FAIL verdict emitted; downstream operator can act on the deterministic error message.

- [ ] **1.2 — Cross-validate per-item Context citation (TB-Add-8 PASS expected)**
  - **Context**: TB-Add-8 at `src/superclaude/agents/rf-qa.md:310` requires every per-item Context paragraph that references a code surface to include at least one file:line citation. This item references `src/superclaude/skills/task-builder/SKILL.md:1134` (the TB-Add-1 mirror).
  - **Action**: Preserve the explicit file:line citation in the Context paragraph.
  - **Output**: Per-item Context paragraph carrying at least one file:line token.
  - **Verification**: TB-Add-8 verifier classifies this item as PASS; no evidence-binding error is emitted.
  - **Completion gate**: PASS verdict emitted; the per-item Context citation survives the gate.

- [ ] **1.3 — Cross-validate header source-areas reappearance (TB-Add-7 PASS expected)**
  - **Context**: TB-Add-7 at `src/superclaude/agents/rf-qa.md:308` requires every named source area in the `## Execution Context` `**Source areas:**` line to reappear in at least one item Context field. Items 1.1 and 1.2 name the rf-qa agent prompt and task-builder skill body, and this item names the MDTM output structure template per the rf-qa.md:296 mirror.
  - **Action**: Keep every header source area present in at least one item Context body.
  - **Output**: All three source-area phrases appear in items 1.1..1.3.
  - **Verification**: TB-Add-7 verifier finds every header source area in at least one item Context; cross-validation emits PASS.
  - **Completion gate**: PASS verdict emitted; header-to-item drift count is zero.

---

## Task Log / Notes

### Execution Log

(none — frozen fixture)
