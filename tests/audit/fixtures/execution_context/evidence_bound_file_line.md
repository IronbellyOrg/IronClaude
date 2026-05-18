---
id: "TASK-RF-20260517-TEST003B-FILELINE"
title: "TEST-003b file:line Per-item Context Fixture (TB-Add-8 must PASS)"
description: "M2 MDTM fixture: a fully-populated `## Execution Context` header is present (FR-CONV.2), and a per-item Context bullet references a code surface using a valid `file:line` citation. TB-Add-8 (rf-qa.md:310; SKILL.md:1073, 1826) MUST classify this item as PASS. Backs T02.10 / D-0024 — NFR-CONV.7 evidence-bound-item preservation re-run against M2-generated MDTM."
status: \"🟡 To Do\"
type: \"🧪 Test\"
priority: \"🔼 High\"
created_date: "2026-05-17"
updated_date: "2026-05-17"
assigned_to: "tests/audit"
template_schema_doc: ".claude/templates/workflow/01_mdtm_template_generic_task.md"
estimation: "n/a"
task_type: static
related_docs:
- description: "TB-Add-8 rule text in rf-qa.md (per-item Context evidence binding)"
- description: "NFR-CONV.7 roadmap row (evidence-bound-item invariant preservation)"
tags:
- "test-003b"
- "tb-add-8"
- "nfr-conv-7"
- "file-line-pass"
---

# TEST-003b file:line Per-item Context Fixture

## Task Overview

Frozen M2-style MDTM fixture exercising TB-Add-8's `file:line`-cited
PASS branch on a task file that ALSO carries the FR-CONV.2 `##
Execution Context` header. Used by
`tests/audit/test_evidence_bound_tb_add_8.py` to prove the canonical
PASS shape survives M2 header introduction.

## Key Objectives

- Per-item Context with a `file:line` citation passes TB-Add-8.
- M2 header presence is orthogonal to per-item evidence binding.

## Prerequisites & Dependencies

- T01.11 PASS (TB-Add-8 rule wired).
- T02.01..T02.05 PASS (M2 header live).

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-046: NFR-CONV.7 evidence-bound-item invariant preservation; R-015: TB-Add-8 per-item Context citation check.
- **Source areas:** rf-qa agent prompt, task-builder skill body, MDTM Output Structure template.
- **Key constraints:** Per-item Context fields retain file:line citations or justified-absence comments; bare module paths FAIL TB-Add-8; header contains no specific paths.

---

## Phase 1: file:line classification

- [ ] **1.1 — Demonstrate file:line Context (TB-Add-8 PASS expected)**
  - **Context**: TB-Add-8 rule is defined at `src/superclaude/agents/rf-qa.md:310` and mirrored at `src/superclaude/skills/task-builder/SKILL.md:1073` and `src/superclaude/skills/task-builder/SKILL.md:1826`. This Context paragraph carries an explicit `file:line` citation per INV-015 scope-confinement at the body level.
  - **Action**: Keep the citation intact so the TB-Add-8 verifier emits the PASS verdict.
  - **Output**: Per-item Context paragraph carrying at least one `file:line` token.
  - **Verification**: TB-Add-8 verifier classifies this item as PASS; error counter increments by 0 for this item.
  - **Completion gate**: PASS verdict emitted; no TB-Add-8 error references this item.

---

## Task Log / Notes

### Execution Log
(none — frozen fixture)
