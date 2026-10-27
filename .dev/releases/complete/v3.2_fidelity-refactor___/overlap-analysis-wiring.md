# Overlap Analysis: Wiring Verification Gate (Primary)

**Date**: 2026-03-17
**Primary file**: `v3.0_fidelity-refactor_/wiring-verification-gate-v1.0-release-spec.md`
**Compared against**:
- `v3.05_Anti-instincts_/anti-instincts-gate-unified.md`
- `v3.1_unified-audit-gating-v1.2.1/spec-refactor-plan-merged.md`

---

## 3x3 Overlap Matrix

| | **Wiring Verification** | **Anti-Instincts** | **Unified Audit Gating** |
|---|---|---|---|
| **Wiring Verification** | N/A (self) | **6/10 (60%)** | **3/10 (30%)** |
| **Anti-Instincts** | **6/10 (60%)** | N/A (self) | **4/10 (40%)** |
| **Unified Audit Gating** | **3/10 (30%)** | **4/10 (40%)** | N/A (self) |

---

## Detailed Overlap Justification

---

### Wiring Verification <-> Anti-Instincts: 6/10 (60%)

This is the highest overlap pair. Both specs were born from the same cli-portify forensic report and attack overlapping detection targets, though through different mechanisms and at different pipeline stages.

#### Overlap Instance 1: Unwired Registry Detection vs. Integration Contract Extraction

**Wiring Verification** (Section 4.2.3):
> "Detect dictionary constants with naming patterns indicating dispatch registries (`REGISTRY`, `DISPATCH`, `RUNNERS`, `HANDLERS`, `ROUTER`) whose values reference functions that cannot be resolved via import."

**Anti-Instincts** (Section 5, `integration_contracts.py`):
> "An integration contract is any place where a data structure maps identifiers to callables, a constructor accepts injectable dependencies, an explicit wiring step is described, or a lookup/dispatch mechanism is defined."

The Anti-Instincts `DISPATCH_PATTERNS` regex list (Section 5) includes `RUNNERS`, `HANDLERS`, `DISPATCH`, `routing_table`, `command_map`, `step_map`, `plugin_registry` -- these overlap heavily with Wiring Verification's `DEFAULT_REGISTRY_PATTERNS` which matches `STEP_REGISTRY`, `STEP_DISPATCH`, `PROGRAMMATIC_RUNNERS`, `*_REGISTRY`, `*_DISPATCH`, `*_HANDLERS`, `*_ROUTER`.

**Why redundant**: Both detect the same class of artifact (dispatch table / registry dictionaries). If both ship, a registry like `PROGRAMMATIC_RUNNERS` would be flagged by Wiring Verification's `analyze_unwired_registries()` (code-level AST analysis checking whether dict values resolve) AND by Anti-Instincts' `extract_integration_contracts()` + `check_roadmap_coverage()` (document-level regex checking whether the roadmap has an explicit wiring task).

**Why not fully redundant**: They operate at different levels. Wiring Verification does AST-level analysis on actual Python code (checks whether dict values are importable functions). Anti-Instincts does text-level analysis on spec/roadmap documents (checks whether the roadmap plans for wiring). Wiring Verification catches bugs after code is written; Anti-Instincts catches omissions before code is generated. These are complementary pipeline stages, but the detection target is the same artifact class.

**Which is more complete**: Anti-Instincts covers a broader taxonomy of integration mechanisms (7 categories: dict dispatch, plugin registry, callback injection, strategy pattern, middleware chain, event binding, DI container). Wiring Verification covers a narrower set (registries, optional callables, orphan modules) but with deeper code-level analysis (AST parsing, actual import resolution). For the specific case of dispatch registries, Anti-Instincts is broader; for verifying actual code wiring, Wiring Verification is authoritative.

#### Overlap Instance 2: Unwired Callable Detection vs. Callback Injection Contract Detection

**Wiring Verification** (Section 4.2.1):
> "Detect constructor parameters typed `Optional[Callable]` (or `Callable | None`) with default `None` that are never explicitly provided at any call site in the codebase."

**Anti-Instincts** (Section 5, `DISPATCH_PATTERNS` Category 3):
> Pattern: `r'\b(?:accepts?|takes?|requires?|expects?)\s+(?:a\s+)?(?:Callable|Protocol|ABC|Interface|Factory|Provider|Registry)\b'`
> And: `r'\b(?:Dict|Mapping|dict)\s*\[\s*str\s*,\s*(?:Callable|Awaitable|Coroutine)\b'`

**Why redundant**: Both detect `Optional[Callable]` / injectable callable patterns. The `PortifyExecutor.step_runner: Optional[Callable] = None` bug would be flagged by both: Wiring Verification finds it through AST analysis of actual code; Anti-Instincts finds it through spec text pattern matching.

**Why not fully redundant**: Same stage distinction as above. Wiring Verification operates on code; Anti-Instincts operates on spec/roadmap text. If the spec mentions "accepts Callable" but the code was never written, only Anti-Instincts catches it. If the code exists but the spec didn't mention it, only Wiring Verification catches it.

**Which is more complete**: Wiring Verification is more precise for code-level detection (it verifies zero call sites provide the parameter). Anti-Instincts is more useful as an upstream guard (catches the planning omission before code is generated).

#### Overlap Instance 3: Deviation Count Reconciliation vs. Spec Structural Audit

**Wiring Verification** (Section 4.6):
> "Deviation count reconciliation: Parse frontmatter for `high_severity_count`, `medium_severity_count`, `low_severity_count`. Regex-scan body for `DEV-\d{3}` entries, extract severity. Compare body counts to frontmatter counts. Fail on any mismatch."

**Anti-Instincts** (Section 7, `spec_structural_audit.py`):
> "Counts structural requirement indicators in the raw spec (code blocks, MUST/SHALL clauses, function signatures, test names, registry patterns) and compares against the extraction's total_requirements frontmatter value."

**Why partially redundant**: Both detect frontmatter/body inconsistencies, which is the same class of fidelity failure (LLM-generated summaries that don't match the actual content). However, they check different documents at different pipeline stages: Wiring Verification checks deviation analysis reports; Anti-Instincts checks extraction output against spec input.

**Which is more complete**: These are genuinely different checks on different artifacts. The overlap is in the detection pattern (frontmatter-body reconciliation), not the specific target. Neither subsumes the other.

#### Overlap Instance 4: Common Motivating Bug

Both specs cite the identical cli-portify executor no-op bug as their primary motivating evidence. Wiring Verification Section 1 and Anti-Instincts Section 2 describe the same defect: `step_runner=None` default, orphaned step implementations, missing `PROGRAMMATIC_RUNNERS` wiring.

**Why this matters**: Both specs propose to prevent the recurrence of the same bug. If both ship, the same bug would be caught by multiple overlapping mechanisms. This is defense-in-depth (valuable) but also development cost duplication if budget is constrained.

#### Overlap Instance 5: Gate Infrastructure Pattern

Both define new `GateCriteria` constants consumed by the existing `gate_passed()` function:
- Wiring Verification: `WIRING_GATE` with 5 `SemanticCheck` instances (Section 4.4)
- Anti-Instincts: `ANTI_INSTINCT_GATE` with 3 `SemanticCheck` instances (Section 8)

**Why not contradictory**: Both are additive consumers of the same gate infrastructure. They do not modify `GateCriteria` or `SemanticCheck` interfaces. They can coexist without conflict.

#### Overlap Instance 6: Shadow Mode Rollout Pattern

Both spec shadow -> soft -> full rollout phases:
- Wiring Verification: Section 8 (shadow mode with pre-activation checklist, Phase 1/2/3)
- Anti-Instincts: Section 7 (spec_structural_audit starts as warning-only Phase 1, STRICT in Phase 2)

**Why not redundant**: These are independent rollout tracks for different gates. The pattern is shared but the enforcement timelines are independent.

---

### Wiring Verification <-> Unified Audit Gating: 3/10 (30%)

The overlap here is moderate and mostly indirect. Unified Audit Gating is primarily about the audit workflow state machine (transition states, leases, retries, profiles), while Wiring Verification is a specific code-level analysis gate.

#### Overlap Instance 1: Defect Fix Prerequisites (P0-A)

**Wiring Verification** (Section 1):
> "`step_runner=None` default; steps exist but are never called" listed as the motivating defect. The entire spec is a gate to prevent recurrence.

**Unified Audit Gating** (SS10.1, Phase 0, P0-A):
> "Fix Defect 1 (`run_portify()` must pass `step_runner` to `PortifyExecutor`) and Fix Defect 2 (`commands.py` must call `validate_portify_config()` before `run_portify()`). These are independent of v1.2.1 spec infrastructure."

**Why partially redundant**: Both reference the same defect. Unified Audit Gating schedules the direct fix (P0-A); Wiring Verification builds a gate to prevent recurrence. These are complementary (fix + prevention), not truly redundant, but there is wasted analysis effort if one spec is unaware of the other's existence.

**Which is more complete**: Unified Audit Gating addresses the direct fix. Wiring Verification addresses systematic prevention. Both are needed.

#### Overlap Instance 2: Spec Fidelity Gate Extension -- Deviation Count Reconciliation

**Wiring Verification** (Section 4.6):
> "Deviation Count Reconciliation Gate... Single function `_deviation_counts_reconciled(content: str) -> bool` added to `SPEC_FIDELITY_GATE.semantic_checks` in `roadmap/gates.py`."

**Unified Audit Gating** (SS10.2, P0-C):
> "Add `_check_dispatch_tables_preserved(content: str, inventory: SpecInventory) -> bool`. Add `_check_dispatch_functions_preserved(content: str, inventory: SpecInventory) -> bool`. Extend `SPEC_FIDELITY_GATE.semantic_checks`."

**Why partially redundant**: Both modify the same file (`roadmap/gates.py`) and extend the same gate (`SPEC_FIDELITY_GATE.semantic_checks`). The specific checks are different (deviation count reconciliation vs. dispatch table/function preservation), but concurrent modification of the same gate's `semantic_checks` list creates a merge conflict risk.

**Why not contradictory**: The checks are additive. Both can be appended to the same `semantic_checks` list without conflict, provided the implementations are aware of each other during merge.

**Which is more complete**: Different checks entirely. Wiring Verification adds body-frontmatter count consistency; Unified Audit Gating adds dispatch table/function name preservation. Neither subsumes the other.

#### Overlap Instance 3: Sprint Integration Hook Point

**Wiring Verification** (Section 4.5):
> "Hook point: `sprint/executor.py`, after `_classify_from_result_file()` returns, before the task status is finalized."

**Unified Audit Gating** (SS10.2, Phase 2):
> "Wire `SprintGatePolicy` into `execute_sprint()` at post-subprocess, pre-classification boundary; phase scope only."

**Why partially redundant**: Both modify `sprint/executor.py` to add post-task gate evaluation. Wiring Verification hooks after classification; Unified Audit Gating hooks before classification. These are adjacent but not identical hook points. However, both introduce gate evaluation in the sprint loop, and an implementation that satisfies one may need coordination with the other.

**Which is more complete**: Unified Audit Gating's integration is broader (full audit workflow state machine with lease/heartbeat/retry). Wiring Verification's integration is narrower (shadow-mode logging of wiring analysis results). If both ship, the Wiring Verification gate would likely become a gate evaluated within the Unified Audit Gating framework rather than a parallel hook.

---

### Anti-Instincts <-> Unified Audit Gating: 4/10 (40%)

#### Overlap Instance 1: D-03/D-04 Dispatch Table Preservation vs. Integration Contract Coverage

**Anti-Instincts** (Section 5, `integration_contracts.py`):
> `extract_integration_contracts()` uses `DISPATCH_PATTERNS` to find dispatch tables, registries, injection points in spec text, then `check_roadmap_coverage()` verifies the roadmap explicitly addresses each.

**Unified Audit Gating** (SS10.2, P0-C, `fidelity_inventory.py`):
> "`_DISPATCH_TABLE_PATTERN` regex finds `UPPER_CASE_NAME = {` or `dict(` in spec; verifies each found name appears anywhere in roadmap text."
> "`_STEP_DISPATCH_CALL` regex finds `_run_*()` or `step_result = ` patterns in spec code fences; verifies at least one found function name appears in roadmap."

**Why redundant**: Both extract dispatch table names from spec text and verify they appear in the roadmap. The specific regex patterns differ (Anti-Instincts uses a 7-category taxonomy; Unified Audit Gating uses `_DISPATCH_TABLE_PATTERN` for UPPER_CASE constants), but the detection target for dispatch tables is the same: "does the roadmap mention `PROGRAMMATIC_RUNNERS`?"

**Why not fully redundant**: Anti-Instincts goes further -- it requires not just mention but an explicit *wiring task* (verb-anchored check via `WIRING_TASK_PATTERNS`). Unified Audit Gating D-03/D-04 only checks name presence. Anti-Instincts also covers 7 mechanism categories vs. D-03/D-04's 2 pattern types.

**Which is more complete**: Anti-Instincts is substantially more complete for this detection concern. D-03/D-04 are explicitly described as a quick-deploy subset ("deployable in ~6h") while Anti-Instincts is the full solution. If Anti-Instincts ships, D-03/D-04 become redundant for dispatch table detection, though D-04's pseudocode function name check (`_run_*()` patterns) has no direct equivalent in Anti-Instincts' integration_contracts.py (it is partially covered by fingerprint.py instead).

#### Overlap Instance 2: Motivating Bug and Evidence Chain

Both specs cite the cli-portify no-op bug:
- Anti-Instincts Section 2: "What the spec defined... What the roadmap produced... How existing gates failed"
- Unified Audit Gating SS1.1 (Plan A addition): "three validated behavioral gate extensions from the forensic analysis of the cli-portify no-op incident"

Both use the same forensic evidence to justify their additions.

#### Overlap Instance 3: Gate Infrastructure (roadmap/gates.py Modification)

**Anti-Instincts** (Section 8):
> Adds `ANTI_INSTINCT_GATE` to `gates.py` with 3 `SemanticCheck` functions. Inserts into `ALL_GATES` between `merge` and `test-strategy`.

**Unified Audit Gating** (SS10.2, P0-C):
> Extends `SPEC_FIDELITY_GATE.semantic_checks` in `gates.py` with 2 new check functions.

**Why partially redundant**: Both modify `roadmap/gates.py`. Anti-Instincts adds a new gate; Unified Audit Gating extends an existing gate. The fingerprint coverage check in Anti-Instincts (`_fingerprint_coverage_check`) partially overlaps with D-03/D-04's dispatch name preservation check -- both verify that spec identifiers appear in the roadmap.

**Which is more complete**: Anti-Instincts' `ANTI_INSTINCT_GATE` is a more comprehensive solution. Unified Audit Gating's D-03/D-04 are a narrower, faster-to-deploy subset.

#### Overlap Instance 4: Prompt Modifications for Integration Wiring

**Anti-Instincts** (Section 10):
> Adds `INTEGRATION_ENUMERATION_BLOCK` to `build_generate_prompt()` and `INTEGRATION_WIRING_DIMENSION` to `build_spec_fidelity_prompt()` in `prompts.py`.

**Unified Audit Gating**: Does not modify `prompts.py`. However, the Unified Audit Gating spec's SS13.4 (D-03/D-04) and SS2.2 (non-goals) reference the same integration wiring concern without addressing it at the prompt level.

**Why not redundant**: This is unique to Anti-Instincts. The prompt-level prevention layer has no equivalent in Unified Audit Gating. No overlap here, but noted because Anti-Instincts' prompt changes address the same root cause that Unified Audit Gating's D-03/D-04 detect post-hoc.

---

## Summary

| Pair | Score | Key Finding |
|---|---|---|
| Wiring Verification <-> Anti-Instincts | 6/10 | Highest overlap. Both detect unwired registries and injectable callables, but at different pipeline stages (code-level vs. document-level). Defense-in-depth value exists, but development effort overlaps significantly on dispatch/registry detection. |
| Wiring Verification <-> Unified Audit Gating | 3/10 | Moderate overlap. Shared defect motivation, both modify `gates.py` and `sprint/executor.py`, but for different purposes. Wiring Verification is a specific gate; Unified Audit Gating is the framework those gates run within. Coordination needed at merge time. |
| Anti-Instincts <-> Unified Audit Gating | 4/10 | D-03/D-04 in Unified Audit Gating is a quick-deploy subset of what Anti-Instincts' integration_contracts.py + fingerprint.py provide more completely. If Anti-Instincts ships, D-03/D-04 become largely redundant for dispatch table detection. |

**Recommendation for the Wiring Verification spec author**: The primary risk is developing registry/dispatch detection logic in Wiring Verification's `analyze_unwired_registries()` that duplicates what Anti-Instincts' `integration_contracts.py` already handles at the document level. The Wiring Verification spec's unique value is its code-level AST analysis (unwired callables, orphan modules) -- these have no equivalent in Anti-Instincts or Unified Audit Gating. The registry analysis has the most overlap and should be explicitly scoped relative to Anti-Instincts if both proceed.
