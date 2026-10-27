# D-0006: Phase Loading Contract Matrix

**Task:** T01.06 -- Document Phase Loading Contract Matrix from Spec Section 5.3
**Source:** `tdd-refactor-spec.md` Section 5.3 (`phase_contracts` YAML, lines 228-271)
**Date:** 2026-04-03

---

## Phase Loading Contract Matrix

| Phase | Actor | Declared Loads | Forbidden Loads |
|---|---|---|---|
| Invocation (SKILL.md load) | Claude Code | `SKILL.md` | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage A.1-A.6 | Orchestrator | `SKILL.md` | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage A.7 (orchestrator) | Orchestrator | `refs/build-request-template.md` | _(none)_ |
| Stage A.7 (builder) | `rf-task-builder` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` | _(none)_ |
| Stage A.8 | Orchestrator | `SKILL.md` | `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |
| Stage B | `/task` execution | Generated task file + task skill | `refs/build-request-template.md`, `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` |

---

## Phase Constraints (from spec Section 5.3)

| Phase | Constraint |
|---|---|
| Invocation | Behavioral protocol only |
| Stage A.1-A.6 | No refs pre-load |
| Stage A.7 | Build request template loaded before builder spawn; Builder reads refs before task file generation; Contract rule: if loaded_ref not in declared loads, phase fails |
| Stage A.8 | Task-file structural verification only |
| Stage B | No direct refs load required during checklist execution |

---

## Contract Validation Rules

From spec `contract_validation_rule` (lines 268-270):

1. **Set intersection rule:** `declared_loads intersect forbidden_loads = empty set` for every phase
2. **Runtime containment rule:** `runtime_loaded_refs subset_of declared_loads` for every phase

---

## Validation: Set Intersection Check

| Phase | declared_loads intersect forbidden_loads | Result |
|---|---|---|
| Invocation | {SKILL.md} intersect {all 5 refs} = empty set | PASS |
| Stage A.1-A.6 | {SKILL.md} intersect {all 5 refs} = empty set | PASS |
| Stage A.7 (orchestrator) | {refs/build-request-template.md} intersect {} = empty set | PASS |
| Stage A.7 (builder) | {4 refs} intersect {} = empty set | PASS |
| Stage A.8 | {SKILL.md} intersect {4 refs} = empty set | PASS |
| Stage B | {task file + task skill} intersect {all 5 refs} = empty set | PASS |

All 6 phases pass the set intersection validation rule.

---

## Cross-Check: Roadmap Phase 1 Task 6 Table

The roadmap (lines 40-47) provides a summary table. Comparison against spec Section 5.3:

| Roadmap Column | Spec Source | Match |
|---|---|---|
| Invocation: "None (SKILL.md only)" as Declared Loads | Spec: `loads: [SKILL.md]` | MATCH (roadmap simplifies to "None" since SKILL.md is implicit) |
| Stage A.1-A.6: "None" as Declared Loads | Spec: `loads: [SKILL.md]` | MATCH (same simplification) |
| Stage A.7 (orchestrator): `refs/build-request-template.md` | Spec: `orchestrator_loads: [refs/build-request-template.md]` | MATCH |
| Stage A.7 (builder): 4 refs files | Spec: `builder_loads: [4 refs files]` | MATCH |
| Stage A.8: "None (SKILL.md only)" | Spec: `loads: [SKILL.md]`, forbidden excludes `refs/build-request-template.md` | MATCH (roadmap adds `refs/build-request-template.md` to A.8 forbidden per omission from spec forbidden list -- note: spec does NOT forbid `refs/build-request-template.md` in A.8, roadmap does not forbid it either) |
| Stage B: "Generated task file + task skill" | Spec: `loads: [task skill + generated task file]` | MATCH |

**Discrepancy noted:** The roadmap table lists Stage A.8 Forbidden Loads as only the 4 builder refs (excluding `refs/build-request-template.md`), which matches the spec exactly. The spec forbids only `refs/agent-prompts.md`, `refs/synthesis-mapping.md`, `refs/validation-checklists.md`, `refs/operational-guidance.md` for A.8 -- `refs/build-request-template.md` is neither declared nor forbidden in A.8 per spec.

---

## Summary

- **6 phases** documented: Invocation, A.1-A.6, A.7 (orchestrator), A.7 (builder), A.8, Stage B
- **Contract validation:** All phases pass `declared_loads intersect forbidden_loads = empty set`
- **Cross-check:** Matrix matches roadmap table with one noted nuance (A.8 treatment of `refs/build-request-template.md`)
- **Source fidelity:** All entries transcribed from spec Section 5.3 YAML (lines 228-271)
