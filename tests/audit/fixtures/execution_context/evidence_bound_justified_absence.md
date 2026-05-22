---
id: "TASK-RF-20260517-TEST003C-ABSENCE"
title: "TEST-003c Justified-absence Per-item Context Fixture (TB-Add-8 must PASS)"
description: "M2 MDTM fixture: a fully-populated `## Execution Context` header is present (FR-CONV.2), and a per-item Context bullet uses an `<!-- evidence-absence: ... -->` justified-absence comment in place of a `file:line` citation (canonical 'pure refactor / new file with no source line yet' branch). TB-Add-8 (rf-qa.md:310; SKILL.md:1073, 1826) MUST classify this item as PASS. Backs T02.10 / D-0024 — NFR-CONV.7 evidence-bound-item preservation re-run against M2-generated MDTM."
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
- "test-003c"
- "tb-add-8"
- "nfr-conv-7"
- "justified-absence-pass"
---

# TEST-003c Justified-absence Per-item Context Fixture

## Task Overview

Frozen M2-style MDTM fixture exercising TB-Add-8's justified-absence
PASS branch on a task file that ALSO carries the FR-CONV.2 `##
Execution Context` header. Used by
`tests/audit/test_evidence_bound_tb_add_8.py` to prove the
justified-absence escape hatch (for net-new files / pure-refactor
items) survives M2 header introduction.

## Key Objectives

- Per-item Context with `<!-- evidence-absence: ... -->` passes TB-Add-8.
- Justified-absence comment is recognised regardless of M2 header.

## Prerequisites & Dependencies

- T01.11 PASS (TB-Add-8 rule wired).
- T02.01..T02.05 PASS (M2 header live).

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-046: NFR-CONV.7 evidence-bound-item invariant preservation; R-015: TB-Add-8 per-item Context citation check.
- **Source areas:** rf-qa agent prompt, task-builder skill body, MDTM Output Structure template.
- **Key constraints:** Per-item Context fields retain file:line citations or justified-absence comments; bare module paths FAIL TB-Add-8; header contains no specific paths.

---

## Phase 1: justified-absence classification

- [ ] **1.1 — Demonstrate justified-absence Context (TB-Add-8 PASS expected)**
  - **Context**: This item introduces a brand-new module that does not yet exist on disk, so no `file:line` citation is available. <!-- evidence-absence: pure refactor / net-new module under src/superclaude/; no source line yet — citation will be added on the first edit landing -->
  - **Action**: Keep the `<!-- evidence-absence: ... -->` comment in place so the TB-Add-8 verifier emits the PASS verdict.
  - **Output**: Per-item Context paragraph carrying a recognisable evidence-absence justification comment.
  - **Verification**: TB-Add-8 verifier classifies this item as PASS; error counter increments by 0 for this item.
  - **Completion gate**: PASS verdict emitted; no TB-Add-8 error references this item.

---

## Task Log / Notes

### Execution Log

(none — frozen fixture)
