# D-0008: Requirement Traceability Matrix, Module Ownership Map, and Test Plan

**Task:** T01.07
**Date:** 2026-03-16
**Status:** COMPLETE

---

## Part 1: Requirement Traceability Matrix

| Requirement | Description | Source File(s) | Test File(s) | Milestone | OQ/Decision |
|-------------|-------------|----------------|--------------|-----------|-------------|
| FR-033 | Executor injects pipeline_diagnostics into extract frontmatter | `roadmap/executor.py:_inject_pipeline_diagnostics()` | `tests/cli/roadmap/` | Phase 2 | OQ-H (D-0003) |
| FR-077 | Dual-budget-exhaustion halt handling | `sprint/executor.py:_print_terminal_halt()` (placeholder) | `tests/cli/sprint/` | Phase 4 T04.07 | OQ-J (D-0004) |
| FR-079 | GateCriteria supplemental routing data | Frontmatter fields in step outputs; sprint executor layer | `tests/cli/sprint/` | Phase 2 | OQ-A (D-0001) |
| FR-088 | Extended validation via frontmatter | Step output frontmatter; existing `required_frontmatter_fields` | `tests/cli/pipeline/` | Phase 3 | OQ-B (D-0001) |
| NFR-007 | No cross-layer imports (pipeline ↔ sprint/roadmap) | All `pipeline/` modules (enforced via docstring + import guard) | `tests/cli/pipeline/` | All phases | D-0005 |
| NFR-024 | Token count best-effort fallback | `roadmap/executor.py:StepResult` | `tests/cli/roadmap/` | Phase 3 | OQ-I (D-0003) |

### Fidelity Requirements (OQ-E/OQ-F)

| Requirement | Description | Source File(s) | Test File(s) | Milestone |
|-------------|-------------|----------------|--------------|-----------|
| OQ-E impl | `_extract_fidelity_deviations()` | `roadmap/fidelity.py` (to create) | `tests/cli/roadmap/test_fidelity.py` | Phase 2 |
| OQ-F impl | `_extract_deviation_classes()` | `roadmap/fidelity.py` (to create) | `tests/cli/roadmap/test_fidelity.py` | Phase 2 |

### Executor Interface Requirements (OQ-G/OQ-H)

| Requirement | Description | Source File(s) | Test File(s) | Milestone |
|-------------|-------------|----------------|--------------|-----------|
| OQ-G impl | `build_remediate_step()` | `roadmap/remediate.py` (to create) | `tests/cli/roadmap/test_remediate.py` | Phase 2 |
| OQ-H impl | roadmap_hash injection post-step | `roadmap/executor.py` (conditional block after sanitize) | `tests/cli/roadmap/test_executor.py` | Phase 3 |

---

## Part 2: Module Ownership Map

### `src/superclaude/cli/pipeline/` — Generic Pipeline Layer (READ-ONLY for v2.26)

| Module | Owner | v2.26 Modification | Notes |
|--------|-------|-------------------|-------|
| `models.py` | Platform | **NONE** | AC-1 constraint; GateCriteria unchanged |
| `executor.py` | Platform | **NONE** | AC-1 constraint; execute_pipeline unchanged |
| `gates.py` | Platform | **NONE** | gate_passed unchanged |
| `trailing_gate.py` | Platform | **NONE** | TrailingGateRunner unchanged |
| `process.py` | Platform | **NONE** | ClaudeProcess unchanged |

### `src/superclaude/cli/roadmap/` — Roadmap Layer (MODIFIED in v2.26)

| Module | Owner | v2.26 Modification | Notes |
|--------|-------|-------------------|-------|
| `fidelity.py` | Roadmap | **ADD** `_extract_fidelity_deviations()`, `_extract_deviation_classes()` | OQ-E, OQ-F |
| `remediate.py` | Roadmap | **ADD** `build_remediate_step()`, `_parse_routing_list()` | OQ-G, D-0006 |
| `executor.py` | Roadmap | **ADD** roadmap_hash injection block | OQ-H |
| `gates.py` | Roadmap | **ADD** new sprint-related GateCriteria instances | Phase 2 |
| `models.py` | Roadmap | No modification expected | Stable |
| `spec_patch.py` | Roadmap | No modification expected | Stable |

### `src/superclaude/cli/sprint/` — Sprint Layer (MODIFIED in v2.26)

| Module | Owner | v2.26 Modification | Notes |
|--------|-------|-------------------|-------|
| `executor.py` | Sprint | **MODIFY** `_print_terminal_halt()` in Phase 4 | FR-077 placeholder → full |
| `models.py` | Sprint | No modification expected | TurnLedger, ShadowGateMetrics stable |

### `_parse_routing_list()` Placement (from D-0006)

**Location:** `src/superclaude/cli/roadmap/remediate.py`
**Reason:** Natural home, no new dependencies, no new file, tie-breaker applied.

---

## Part 3: Test Plan — SC-1 through SC-10 Alignment

### SC-1: Gate Criteria Correctness

**Description:** Sprint-layer GateCriteria instances pass appropriate fields for step output validation
**Test file:** `tests/cli/roadmap/test_gates.py`
**Verification method:** Unit test — instantiate each GateCriteria, verify field values, assert no aux_inputs reference
**Phase:** 2

### SC-2: Fidelity Deviation Extraction

**Description:** `_extract_fidelity_deviations()` correctly parses 7-column deviation report markdown
**Test file:** `tests/cli/roadmap/test_fidelity.py`
**Verification method:** Unit test — provide sample deviation markdown, assert returned FidelityDeviation list matches expected count and field values
**Phase:** 2

### SC-3: Deviation Class Grouping

**Description:** `_extract_deviation_classes()` correctly groups FidelityDeviation by Severity
**Test file:** `tests/cli/roadmap/test_fidelity.py`
**Verification method:** Unit test — provide list of FidelityDeviation with mixed severities, assert dict keys = {HIGH, MEDIUM, LOW} with correct grouping
**Phase:** 2

### SC-4: Remediate Step Construction

**Description:** `build_remediate_step()` returns a valid `Step` with correct prompt, output_file, gate, and timeout
**Test file:** `tests/cli/roadmap/test_remediate.py`
**Verification method:** Unit test — call with mock findings, assert Step fields are populated correctly
**Phase:** 2

### SC-5: Routing List Parsing

**Description:** `_parse_routing_list()` correctly parses routing list strings to task ID lists
**Test file:** `tests/cli/roadmap/test_remediate.py`
**Verification method:** Unit test — provide sample content strings, assert returned list matches expected task IDs; test empty, single, and multi-item cases
**Phase:** 2

### SC-6: roadmap_hash Post-Step Injection

**Description:** `roadmap_run_step()` injects roadmap_hash into output frontmatter after step completion
**Test file:** `tests/cli/roadmap/test_executor.py`
**Verification method:** Integration test — run a dry-run step, mock output file with frontmatter, verify hash field injected
**Phase:** 3

### SC-7: Token Count Fallback

**Description:** Token count field in diagnostic output is None when subprocess model used; no exception raised
**Test file:** `tests/cli/roadmap/test_executor.py`
**Verification method:** Unit test — assert token_count Optional[int] field defaults to None; assert no AttributeError on access
**Phase:** 3

### SC-8: Dual-Budget-Exhaustion Placeholder

**Description:** `_print_terminal_halt()` handles TURN_BUDGET_EXHAUSTED and TOKEN_BUDGET_EXHAUSTED without crashing; does not emit DUAL_BUDGET_EXHAUSTED in Phase 2-3
**Test file:** `tests/cli/sprint/test_executor.py`
**Verification method:** Unit test — call _print_terminal_halt with each status enum, assert output contains expected message
**Phase:** 4

### SC-9: Architecture Constraint Enforcement — No Cross-Layer Imports

**Description:** No module in `pipeline/` imports from `sprint/` or `roadmap/`
**Test file:** `tests/cli/pipeline/test_import_constraints.py` (or static check)
**Verification method:** Import analysis test — for each pipeline module, assert `sprint` and `roadmap` do not appear in `__import__` or `sys.modules` after import
**Phase:** All (CI gate)

### SC-10: PRE_APPROVED Extraction from Frontmatter

**Description:** Sprint executor correctly extracts PRE_APPROVED IDs from step output frontmatter
**Test file:** `tests/cli/sprint/test_executor.py`
**Verification method:** Unit test — provide mock step output with `pre_approved_ids` frontmatter field, assert correct extraction and gating behavior
**Phase:** 3

---

## Part 4: Artifact Cross-Reference

| Artifact | Content | Task |
|----------|---------|------|
| D-0001 | OQ-A/OQ-B/OQ-C resolutions | T01.01 |
| D-0002 | OQ-E/OQ-F fidelity.py signatures | T01.02 |
| D-0003 | OQ-G/OQ-H/OQ-I executor interfaces | T01.03 |
| D-0004 | OQ-J FR-077 dual-budget handling | T01.04 |
| D-0005 | Architecture constraint verification | T01.05 |
| D-0006 | _parse_routing_list() placement | T01.06 |
| D-0007 | Consolidated decision log | T01.07 |
| D-0008 | This file — traceability matrix, module map, test plan | T01.07 |
| D-0009 | Phase 1 exit criteria checklist | T01.08 |
