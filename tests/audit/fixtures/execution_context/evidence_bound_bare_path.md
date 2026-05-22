---
id: "TASK-RF-20260517-TEST003A-BARE"
title: "TEST-003a Bare-path Per-item Context Fixture (TB-Add-8 must FAIL)"
description: "M2 MDTM fixture: a fully-populated `## Execution Context` header is present (FR-CONV.2), and a per-item Context bullet references a code surface using a BARE module path with no `:N` line anchor and no `<!-- evidence-absence: ... -->` justified-absence comment. TB-Add-8 (rf-qa.md:310; SKILL.md:1073, 1826) MUST classify this item as FAIL. Backs T02.10 / D-0024 — NFR-CONV.7 evidence-bound-item preservation re-run against M2-generated MDTM."
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
- "test-003a"
- "tb-add-8"
- "nfr-conv-7"
- "bare-path-fail"
---

# TEST-003a Bare-path Per-item Context Fixture

## Task Overview

Frozen M2-style MDTM fixture exercising TB-Add-8's bare-path FAIL branch
against a task file that ALSO carries the FR-CONV.2 `## Execution
Context` header. Used by `tests/audit/test_evidence_bound_tb_add_8.py`
to prove that introducing the M2 header does NOT relax per-item
evidence binding (NFR-CONV.7).

## Key Objectives

- Per-item Context fields remain the evidence venue post-M2.
- TB-Add-8 classifies bare module paths as FAIL even when the header is
  present.
- TB-Add-8 error citations refer to the per-item Context line, not the
  header range.

## Prerequisites & Dependencies

- T01.11 PASS (TB-Add-8 rule wired into rf-qa.md / SKILL.md).
- T02.01..T02.05 PASS (M2 Execution Context header live).

## Execution Context

<!-- OPTIONAL header — emit when BUILD_REQUEST yields enough rollup signal. Block is a task-level READING aid; per-item Context fields remain the evidence venue with file colon line citations. The block contains NO specific path references. Omit any sub-bullet that lacks data; omit the whole block when BUILD_REQUEST is GOAL-only. -->

- **References:** R-046: NFR-CONV.7 evidence-bound-item invariant preservation; R-015: TB-Add-8 per-item Context citation check.
- **Source areas:** rf-qa agent prompt, task-builder skill body, MDTM Output Structure template.
- **Key constraints:** Per-item Context fields retain file:line citations or justified-absence comments; bare module paths FAIL TB-Add-8; header contains no specific paths.

---

## Phase 1: Bare-path classification

- [ ] **1.1 — Demonstrate bare-path Context (TB-Add-8 FAIL expected)**
  - **Context**: Item references the code surface `src/superclaude/skills/task-builder/SKILL.md` without any line anchor. The bullet deliberately omits both an explicit anchor and any justification marker so the TB-Add-8 verifier observes the canonical bare-path shape (INV-015 scope-confinement violation at the body level).
  - **Action**: Leave the Context bullet in its bare form so the TB-Add-8 verifier emits the FAIL verdict.
  - **Output**: Per-item Context paragraph carrying a bare module path.
  - **Verification**: TB-Add-8 verifier classifies this item as FAIL with an error citing `Item 1.1 Context` (NOT the header byte range).
  - **Completion gate**: FAIL verdict emitted; error message names the per-item Context location.

---

## Task Log / Notes

### Execution Log

(none — frozen fixture)
