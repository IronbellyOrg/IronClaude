# D-0018: Loading Declarations in SKILL.md per FR-TDD-R.6

**Task:** T04.02 -- Insert Loading Declarations in SKILL.md per FR-TDD-R.6
**Date:** 2026-04-03

---

## Changes Made

### 1. Stage A.7 Loading Declaration (FR-TDD-R.6a)

**Location:** `src/superclaude/skills/tdd/SKILL.md`, lines 345-350 (Section A.7)

Inserted explicit `Read refs/build-request-template.md` directive for the orchestrator at Stage A.7, before builder spawn. Clarifies that no other refs files are loaded by the orchestrator at this phase.

### 2. Builder Load Dependencies (FR-TDD-R.6b)

**Location:** `src/superclaude/skills/tdd/SKILL.md`, lines 352-361 (Section A.7)

Inserted explicit `Read` directives for 4 builder refs files:
- `refs/agent-prompts.md`
- `refs/synthesis-mapping.md`
- `refs/validation-checklists.md`
- `refs/operational-guidance.md`

Clarifies these are loaded by the builder (not the orchestrator) and are used to embed content into task file B2 items.

### 3. Phase Contract Conformance Table (FR-TDD-R.6c)

**Location:** `src/superclaude/skills/tdd/SKILL.md`, lines 408-427 (new section after Stage B)

Inserted full phase loading contract table covering all 6 phases:
- Invocation, Stage A.1-A.6, Stage A.7 (orchestrator), Stage A.7 (builder), Stage A.8, Stage B
- Each row declares: Phase, Actor, Declared Loads, Forbidden Loads
- Table matches D-0006 (Phase Loading Contract Matrix) exactly

### 4. Contract Validation Rules (FR-TDD-R.6d)

Included two contract validation rules below the table:
1. Set intersection: `declared_loads ∩ forbidden_loads = ∅` for every phase
2. Runtime containment: `runtime_loaded_refs ⊆ declared_loads` for every phase

---

## Validation

### Set Intersection Check (SC-9)

| Phase | declared_loads ∩ forbidden_loads | Result |
|---|---|---|
| Invocation | {SKILL.md} ∩ {5 refs} = ∅ | PASS |
| Stage A.1-A.6 | {SKILL.md} ∩ {5 refs} = ∅ | PASS |
| Stage A.7 (orchestrator) | {refs/build-request-template.md} ∩ {} = ∅ | PASS |
| Stage A.7 (builder) | {4 refs} ∩ {} = ∅ | PASS |
| Stage A.8 | {SKILL.md} ∩ {4 refs} = ∅ | PASS |
| Stage B | {task file + task skill} ∩ {5 refs} = ∅ | PASS |

**Result: All 6 phases PASS the set intersection rule.**

### Refs Declaration Count

```
grep 'refs/' src/superclaude/skills/tdd/SKILL.md | wc -l
```
Returns: 12 lines containing `refs/` references (5 explicit Read directives + 7 table entries covering all 5 refs files)

All 5 refs files are declared:
1. `refs/build-request-template.md` -- Stage A.7 orchestrator load
2. `refs/agent-prompts.md` -- Stage A.7 builder load
3. `refs/synthesis-mapping.md` -- Stage A.7 builder load
4. `refs/validation-checklists.md` -- Stage A.7 builder load
5. `refs/operational-guidance.md` -- Stage A.7 builder load

### Line Count

- Before: 388 lines
- After: 428 lines (+40 lines for loading declarations and contract table)
- Still under 500-line budget: PASS

---

## Acceptance Criteria Verification

| Criterion | Status |
|---|---|
| Stage A.7 loading declaration for `refs/build-request-template.md` explicit (FR-TDD-R.6a) | PASS |
| Builder load dependencies for 4 refs files explicit (FR-TDD-R.6b) | PASS |
| Phase contract conformance table present matching D-0006 baseline (FR-TDD-R.6c) | PASS |
| `declared_loads ∩ forbidden_loads = ∅` for every phase (SC-9 / FR-TDD-R.6d) | PASS |
