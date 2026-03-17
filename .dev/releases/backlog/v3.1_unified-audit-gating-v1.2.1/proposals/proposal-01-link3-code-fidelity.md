# Proposal 01: Link 3 — Tasklist-to-Code Fidelity Gate

**Proposal ID**: P01
**Target release**: unified-audit-gating v1.2.1
**Date**: 2026-03-17
**Status**: Draft — ready for review
**Author**: forensic investigation synthesis (6-agent parallel + manual validation)

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Proposed Solution](#2-proposed-solution)
3. [Programmatic vs LLM-Assisted Split](#3-programmatic-vs-llm-assisted-split)
4. [Implementation Plan](#4-implementation-plan)
5. [Acceptance Criteria](#5-acceptance-criteria)
6. [Risk Assessment](#6-risk-assessment)
7. [Estimated Effort](#7-estimated-effort)

---

## 1. Problem Statement

### 1.1 The Missing Link

The pipeline fidelity chain is:

```
Spec --[SPEC_FIDELITY_GATE]--> Roadmap --[TASKLIST_FIDELITY_GATE]--> Tasklist --[???]--> Code
```

Links 1 and 2 have gate infrastructure. Link 3 does not exist. No programmatic gate at any point in the pipeline verifies that code output satisfies tasklist acceptance criteria.

This is documented in the forensic report (`docs/generated/cli-portify-executor-noop-forensic-report.md`, Section 5) and confirmed by the delta analysis (`delta-analysis-post-v2.26.md`, Delta 2.11).

### 1.2 The Failure Mode Link 3 Allows

The cli-portify executor bug is a concrete production instance of the class of failures Link 3 would catch:

- `executor.py:393-415`: `_execute_step()` has a no-op fallback — when `self._step_runner is None`, it returns `(exit_code=0, stdout="", timed_out=False)` and the pipeline records every step as completed.
- `executor.py:1395-1401`: `run_portify()` constructs `PortifyExecutor` without passing `step_runner=`, so the no-op path is always taken.
- Eight step implementations exist in `src/superclaude/cli/cli_portify/steps/` (`validate_config.py`, `discover_components.py`, `analyze_workflow.py`, `design_pipeline.py`, `synthesize_spec.py`, `brainstorm_gaps.py`, `panel_review.py`) plus `execute_protocol_mapping_step()` at `executor.py:494`. None are ever called.

The tasklist for v2.25 (T03.04 Step 4: "Sequential loop: iterate STEP_REGISTRY; execute each step") defined acceptance criteria that checked sequential flow, resume behavior, and interrupt handling — but did not require that steps perform real work. The code satisfied the tasklist's acceptance criteria while doing nothing. A Link 3 gate that validated those specific criteria would have passed for the same reason: the criteria were insufficient.

This reveals two distinct problems:

**Problem A (structural)**: No gate verifies that code output satisfies tasklist acceptance criteria at all. This is the direct absence of Link 3.

**Problem B (semantic)**: Even when a Link 3 gate is introduced, it can only be as good as the acceptance criteria it validates. The v2.25 tasklist acceptance criteria for T03.04 were silent on dispatch wiring. A purely mechanical gate would have passed them.

Both problems must be addressed. A Link 3 gate that validates weak acceptance criteria provides false confidence — a different form of the same failure.

### 1.3 Scope of This Proposal

This proposal addresses the design and implementation of Link 3: a code-fidelity gate that:
1. Translates tasklist acceptance criteria into checkable assertions.
2. Executes those assertions against code output after each sprint task completes.
3. Blocks the `audit_task_passed -> completed` transition unless assertions pass.
4. Integrates with the `audit_task_*` state machine defined in the v1.2.1 spec (Section 4.1).

It also addresses strengthening acceptance criteria at tasklist generation time to prevent the Problem B failure mode.

### 1.4 What Link 3 Does NOT Address

- The no-op bug itself (Fix 1 and Fix 2 in the forensic report, Section 10 — immediate hotfixes independent of this proposal).
- Links 1-2 weakness (LLM-only semantic comparison without programmatic ID cross-reference checks). That is a separate proposal scope.
- Release-scope gate enforcement. This proposal focuses on task-scope gating (Tier-1 in the v1.2.1 spec, Section 1.1).

---

## 2. Proposed Solution

### 2.1 Core Design

Link 3 is a two-phase check executed after each sprint task completes and before the task is allowed to transition to `completed`:

**Phase A — Programmatic checks** (deterministic, run first, fast):
- File-existence checks for declared deliverables.
- Import-reachability checks for declared code symbols.
- Wiring-completeness checks for constructor/registry patterns.
- Artifact-content checks (non-empty, minimum structure).

**Phase B — LLM-assisted checks** (semantic, run only if Phase A passes):
- Acceptance criteria text interpretation.
- Behavioral intent verification (does the code do what the criterion describes?).
- No-op / stub detection for non-trivial criterion types.

Both phases produce a `CodeFidelityResult` that feeds the `audit_task_*` state machine.

### 2.2 Acceptance Criteria Taxonomy

To make acceptance criteria checkable, the tasklist generator must emit structured assertions alongside natural-language descriptions. The taxonomy has three assertion types:

**Type 1: DELIVERABLE** — A file, directory, or artifact must exist and be non-empty.
```yaml
- type: DELIVERABLE
  path: "src/superclaude/cli/cli_portify/steps/validate_config.py"
  required_symbols: ["run_validate_config"]
  min_lines: 50
```

**Type 2: WIRING** — A symbol must be imported and referenced in a specified context.
```yaml
- type: WIRING
  consumer: "src/superclaude/cli/cli_portify/executor.py"
  provider_symbol: "run_validate_config"
  provider_module: "superclaude.cli.cli_portify.steps.validate_config"
  context: "STEP_DISPATCH or step_runner assignment"
```

**Type 3: BEHAVIORAL** — An LLM-evaluated assertion about what the code does.
```yaml
- type: BEHAVIORAL
  criterion: "Each STEP_REGISTRY entry routes to a distinct callable that performs real work when invoked"
  evidence_required: ["import chain", "call site"]
  llm_evaluation: true
```

These structured assertions are emitted as YAML frontmatter in the generated phase files alongside the natural-language acceptance criteria already present.

### 2.3 Gate Execution Flow

```
Task completes (sprint subprocess exits 0)
    |
    v
CodeFidelityGate.evaluate(task_id, phase_file, code_dir)
    |
    +-- Phase A: ProgrammaticChecker.run(assertions)
    |       |
    |       +-- DELIVERABLE checks --> pass/fail per file
    |       +-- WIRING checks --> AST import scan + reference scan
    |       +-- Fail-fast: any Phase A failure --> CodeFidelityResult(passed=False, phase="A", ...)
    |
    +-- Phase B (only if Phase A passes): LLMAssistantChecker.run(behavioral_assertions, code_context)
    |       |
    |       +-- For each BEHAVIORAL assertion: LLM evaluates with code snippets as evidence
    |       +-- Result: passed/failed with evidence refs
    |
    v
CodeFidelityResult
    |
    v
AuditStateMachine.transition(task_id, result)
    |
    +-- result.passed=True  --> audit_task_passed  --> completed (allowed)
    +-- result.passed=False --> audit_task_failed  --> retry or blocked
```

### 2.4 Interface Definitions

#### CodeFidelityResult

```python
@dataclass
class CodeFidelityResult:
    gate_run_id: str          # UUID
    task_id: str
    phase_file: Path
    passed: bool
    failure_phase: str | None  # "A" | "B" | None
    failure_class: str         # "policy" | "transient" | "system" | "timeout" | "unknown"
    checks: list[CodeFidelityCheck]
    evidence_refs: list[str]   # "file:line" or file path strings
    llm_evaluated: bool
    duration_seconds: float
    schema_version: str = "1.0"
```

#### CodeFidelityCheck

```python
@dataclass
class CodeFidelityCheck:
    check_id: str              # e.g., "DEL-001", "WIRE-002", "BEH-001"
    assertion_type: str        # "DELIVERABLE" | "WIRING" | "BEHAVIORAL"
    passed: bool
    evidence: str | None       # file:line or description
    failure_message: str | None
```

#### CodeFidelityGate (main interface)

```python
class CodeFidelityGate:
    def evaluate(
        self,
        task_id: str,
        phase_file: Path,
        code_root: Path,
        profile: str = "standard",  # "strict" | "standard" | "legacy_migration"
    ) -> CodeFidelityResult:
        """Parse assertions from phase_file, run Phase A then Phase B, return result."""
        ...
```

### 2.5 Structured Assertion Extraction

The gate parses assertions from the phase file's YAML frontmatter. The extraction contract:

```
Phase file frontmatter field: code_fidelity_assertions: list[AssertionSpec]
```

If the field is absent and profile is `strict`: gate fails with `failure_class="policy"` (no assertions declared is a policy violation).
If the field is absent and profile is `standard`: gate emits a warning and runs LLM-only evaluation.
If the field is absent and profile is `legacy_migration`: gate passes with a warning (backward compatibility).

This three-way behavior mirrors the rollout philosophy in the v1.2.1 spec (Section 7.1: shadow → soft → full).

### 2.6 Integration with audit_task_* State Machine

The v1.2.1 spec (Section 4.1) defines these task-scope transitions:

```
in_progress -> ready_for_audit_task
ready_for_audit_task -> audit_task_running
audit_task_running -> audit_task_passed | audit_task_failed
audit_task_passed -> completed
audit_task_failed -> ready_for_audit_task  (retry)
audit_task_failed -> completed             (only with approved task override)
```

Link 3 is the implementation of the `audit_task_running -> audit_task_passed | audit_task_failed` transition logic. The gate evaluator is invoked when the state machine enters `audit_task_running`. Its `CodeFidelityResult.passed` field determines which terminal state is reached.

Integration point in `sprint/executor.py`: the `execute_sprint()` mainline loop at lines 668-787. The delta analysis (NR-7, `delta-analysis-post-v2.26.md`) is explicit that audit hooks must live in `execute_sprint()`, not in `execute_phase_tasks()`. Specifically:
- After the Claude subprocess exits (`executor.py:668-717`, post-subprocess pre-classification) is where the gate must be invoked.
- The existing `SprintGatePolicy` stub (`sprint/executor.py:47-90`) is the correct integration hook once completed.

### 2.7 Tasklist Generator Changes (Preventing Problem B)

The tasklist generator (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:622-637`) must be extended to emit structured `code_fidelity_assertions` in generated phase files. Without this, the gate has nothing programmatic to validate.

The generator must apply assertion derivation rules:

| Acceptance criterion text pattern | Assertion type emitted |
|---|---|
| "File X exists" / "Module X is importable" | DELIVERABLE |
| "Function X is called from Y" / "X is wired into Y" / "X routes to Y" | WIRING |
| "Step X calls implementation Y" | WIRING |
| "Registry entry X has a corresponding callable" | WIRING |
| "Output of X contains ..." / behavioral description | BEHAVIORAL |
| Anything not matched | BEHAVIORAL (fallback) |

A WIRING assertion must be emitted any time the acceptance criterion describes a connection between two code components. This is the assertion type that would have caught the cli-portify no-op: "each STEP_REGISTRY entry must route to a callable" is a WIRING assertion.

---

## 3. Programmatic vs LLM-Assisted Split

### 3.1 Rationale for the Split

The existing gate infrastructure (`pipeline/gates.py:20-69`, `tasklist/gates.py:20-43`) uses a pattern where deterministic Python checks run first, and LLM-generated reports provide semantic judgment. The same principle applies here, but the subject is code rather than documents.

Deterministic checks are fast (< 1 second each), replayable, and produce exact file:line evidence. LLM checks are slow (seconds to minutes), non-deterministic across temperature, and produce evidence that is hard to reproduce exactly. The v1.2.1 spec (Section 2.2) explicitly identifies LLM/agent heuristics as non-authoritative for pass/fail. Therefore: LLM checks should only run after deterministic checks pass, and LLM failure alone should not block unless `profile=strict`.

### 3.2 Programmatic Checks (Phase A)

All Phase A checks are implemented in pure Python, no subprocess, no LLM:

| Check | Implementation | What it detects |
|---|---|---|
| DELIVERABLE: file exists | `Path.exists()` | Missing output files |
| DELIVERABLE: non-empty | `path.stat().st_size > 0` | Zero-byte stub files |
| DELIVERABLE: min lines | `len(content.splitlines()) >= N` | Minimal stub files |
| DELIVERABLE: required symbols | AST parse (`ast.parse`) + walk for `FunctionDef`/`ClassDef` names | Declared but not implemented functions |
| WIRING: import present | `ast.parse` + walk for `Import`/`ImportFrom` nodes matching provider module | Missing imports in consumer |
| WIRING: reference present | `ast.parse` + walk for `Name`/`Attribute` nodes matching provider symbol | Imported but never referenced |
| WIRING: no-op fallback pattern | AST scan for `if callable is None: return (0, "", False)` or equivalent | The exact cli-portify defect pattern |

The no-op fallback pattern detector deserves explicit specification. The defect in `executor.py:397-399` takes the form:

```python
if self._step_runner is not None:
    exit_code, stdout, timed_out = self._step_runner(step)
else:
    exit_code, stdout, timed_out = 0, "", False
```

This is an `if ... is not None: ... else: (success_tuple)` pattern where the else branch returns a success indicator. The programmatic check scans for this pattern in any file that declares an `Optional[Callable]` parameter in its `__init__` or function signature. Matching: AST walk for `If` nodes where `test` is `IsNot(Name, None)` or `Is(Name, None)` and the else branch assigns `(0, ...)` or `True` or a constant that maps to the project's success codes.

### 3.3 LLM-Assisted Checks (Phase B)

Phase B runs only if Phase A passes. LLM checks address assertion types that cannot be reduced to AST analysis:

| Check | Why LLM is needed |
|---|---|
| BEHAVIORAL: "step performs real work" | "Real work" is semantically defined; AST cannot distinguish a stub that happens to call a function from a genuine implementation |
| BEHAVIORAL: "output satisfies criterion X" | Natural language acceptance criteria require interpretation |
| BEHAVIORAL: "wiring is semantically correct" | AST confirms a name is referenced but not that it is called with the right arguments in the right context |

The LLM check prompt must include:
1. The exact BEHAVIORAL assertion text from the phase file.
2. The relevant code sections (file content, not just file paths) — providing actual code as context, not asking the LLM to fetch it.
3. An explicit instruction to produce YAML-fronted output with `passed: bool` and `evidence_refs: list[str]` in the frontmatter, followed by reasoning.

The gate enforces the same frontmatter contract as `TASKLIST_FIDELITY_GATE` (`tasklist/gates.py:20-43`): Python parses the frontmatter fields `passed` and `evidence_refs`. If the LLM fails to produce valid frontmatter, the check fails with `failure_class="system"`.

### 3.4 Profile-Based Behavior

| Profile | Phase A failure | Phase B failure |
|---|---|---|
| `strict` | Blocks (`audit_task_failed`) | Blocks (`audit_task_failed`) |
| `standard` | Blocks | Warns (does not block by itself) |
| `legacy_migration` | Warns | Skipped |

Under `standard` profile, Phase B LLM failures produce a warning in the `CodeFidelityResult` but do not cause `audit_task_failed` unless combined with a Phase A partial failure. This is consistent with the v1.2.1 spec's non-goal: "LLM/agent heuristics as source of truth for pass/fail" (Section 2.2).

---

## 4. Implementation Plan

### 4.1 New Files

#### `src/superclaude/cli/audit/code_fidelity.py` (~350 lines)

Core gate implementation. Contains:

- `AssertionSpec` dataclass (parsed from phase file frontmatter)
- `CodeFidelityCheck` dataclass
- `CodeFidelityResult` dataclass
- `ProgrammaticChecker` class (~120 lines):
  - `check_deliverable(spec: AssertionSpec, code_root: Path) -> CodeFidelityCheck`
  - `check_wiring(spec: AssertionSpec, code_root: Path) -> CodeFidelityCheck`
  - `_scan_ast_for_symbol(file: Path, symbol: str) -> list[int]` (returns line numbers)
  - `_scan_ast_for_noop_fallback(file: Path, param_names: list[str]) -> list[int]`
- `LLMAssistantChecker` class (~80 lines):
  - `check_behavioral(spec: AssertionSpec, code_context: str) -> CodeFidelityCheck`
  - `_build_prompt(spec: AssertionSpec, code_context: str) -> str`
  - `_parse_llm_result(output: str) -> tuple[bool, list[str]]`
- `CodeFidelityGate` class (~80 lines):
  - `evaluate(task_id, phase_file, code_root, profile) -> CodeFidelityResult`
  - `_extract_assertions(phase_file: Path) -> list[AssertionSpec]`
  - `_collect_code_context(assertions: list[AssertionSpec], code_root: Path) -> str`

NFR: No subprocess imports. No sprint/roadmap imports (mirrors `pipeline/gates.py:9-10` NFR-003, NFR-007). The gate is a pure library: it receives all inputs as arguments.

#### `src/superclaude/cli/audit/assertion_parser.py` (~120 lines)

Parses `code_fidelity_assertions` YAML from phase file frontmatter into `AssertionSpec` instances. Separate from the gate to allow the tasklist generator to import only the parser for validation without importing the full gate.

Functions:
- `parse_assertions(phase_file: Path) -> list[AssertionSpec]`
- `validate_assertion_spec(spec: dict) -> tuple[bool, str | None]` (schema check)

#### `src/superclaude/cli/audit/noop_detector.py` (~80 lines)

Standalone AST-based no-op fallback detector. Separated from `code_fidelity.py` so it can be used as a standalone check in CI without loading the full gate.

Functions:
- `scan_for_noop_fallbacks(file: Path) -> list[NoopFinding]`
- `NoopFinding` dataclass: `{file: Path, line: int, param_name: str, fallback_value: str, severity: str}`

This implements the detection rule for the exact cli-portify defect class: `Optional[Callable]` parameters that default to `None` and whose `None` branch returns a success constant.

#### `tests/audit/test_code_fidelity.py` (~250 lines)

- `test_deliverable_check_missing_file()`: DELIVERABLE check fails when file absent.
- `test_deliverable_check_missing_symbol()`: DELIVERABLE check fails when required symbol not in AST.
- `test_wiring_check_missing_import()`: WIRING check fails when provider not imported in consumer.
- `test_wiring_check_import_present_but_unreferenced()`: WIRING check fails when imported but never used.
- `test_noop_fallback_detection()`: Detector finds the `executor.py:397-399` pattern in a fixture.
- `test_phase_a_blocks_before_phase_b()`: Phase B does not run when Phase A fails.
- `test_profile_standard_phase_b_warn_only()`: Under `standard`, Phase B failure warns but does not block.
- `test_profile_strict_phase_b_blocks()`: Under `strict`, Phase B failure blocks.
- `test_legacy_migration_no_assertions_passes()`: `legacy_migration` with no `code_fidelity_assertions` field passes.

#### `tests/audit/test_noop_detector.py` (~80 lines)

- Unit tests for `scan_for_noop_fallbacks()` against fixture code.

### 4.2 Modified Files

#### `src/superclaude/cli/sprint/executor.py` — SprintGatePolicy completion (lines 47-90, ~+60 lines)

Currently a stub. Must be extended to:
1. Invoke `CodeFidelityGate.evaluate()` after each Claude subprocess completes.
2. Drive the `audit_task_*` state transitions based on `CodeFidelityResult.passed`.
3. Write `CodeFidelityResult` to a JSON artifact in the sprint work directory for persistence.

Integration hook: `execute_sprint()` mainline at lines 668-787, specifically the post-subprocess pre-classification block at lines 668-717. As documented in `delta-analysis-post-v2.26.md` NR-7, this is the correct insertion point. The task-level `execute_phase_tasks()` helper does not drive the primary phase lifecycle and must not be the sole integration point.

Concrete change: after the Claude subprocess result is captured at approximately line 717, insert:

```python
if task.audit_gate_required:  # field from phase file frontmatter (NR-1 in delta analysis)
    gate = CodeFidelityGate()
    fidelity_result = gate.evaluate(
        task_id=task.task_id,
        phase_file=task.phase_file,
        code_root=self._config.work_dir,
        profile=self._config.audit_profile,
    )
    _drive_audit_state(task, fidelity_result)
    if not fidelity_result.passed:
        # audit_task_failed transition — may retry or block depending on budget
        return _handle_audit_failure(task, fidelity_result, attempt_budget)
```

Estimated addition: ~60 lines including `_drive_audit_state()` and `_handle_audit_failure()` helpers.

#### `src/superclaude/cli/sprint/models.py` — audit_gate_required field (~+15 lines)

Add `audit_gate_required: bool = False` to the task model that sprint uses when reading phase files. This field is populated from the phase file frontmatter (per `delta-analysis-post-v2.26.md` NR-1 and §10.2 replacement language for Phase 3).

The field derivation — already specified in the delta analysis — is: `audit_gate_required = true` when `Tier == STRICT or Risk == High or Critical Path Override == Yes`.

#### `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — assertion derivation rules (~+80 lines in the generation section at lines 622-637)

Extend the template generation logic to emit `code_fidelity_assertions` in phase file frontmatter. The extension must:
1. Apply the assertion-type classification rules from Section 2.7 of this proposal.
2. Emit at minimum one WIRING assertion for any task whose acceptance criteria describe two code components being connected.
3. Emit `audit_gate_required: bool` field.

This is the key change that addresses Problem B: the tasklist generator becomes responsible for producing checkable assertions, not just natural-language text.

After this change, `make sync-dev` must be run to propagate the updated SKILL.md to `.claude/skills/sc-tasklist-protocol/SKILL.md`.

#### `src/superclaude/cli/pipeline/models.py` — AssertionSpec registration (~+20 lines)

Register `code_fidelity_assertions` as a known frontmatter field type in the pipeline model layer, to avoid the field being treated as unknown during validation. Add `AssertionType` enum: `DELIVERABLE | WIRING | BEHAVIORAL`.

### 4.3 File Change Summary

| File | Change type | Approx lines |
|---|---|---|
| `src/superclaude/cli/audit/code_fidelity.py` | New | ~350 |
| `src/superclaude/cli/audit/assertion_parser.py` | New | ~120 |
| `src/superclaude/cli/audit/noop_detector.py` | New | ~80 |
| `tests/audit/test_code_fidelity.py` | New | ~250 |
| `tests/audit/test_noop_detector.py` | New | ~80 |
| `src/superclaude/cli/sprint/executor.py` | Modify | +60 |
| `src/superclaude/cli/sprint/models.py` | Modify | +15 |
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` | Modify | +80 |
| `src/superclaude/cli/pipeline/models.py` | Modify | +20 |

Total: ~880 new lines + ~175 modified lines.

---

## 5. Acceptance Criteria

### 5.1 Link 3 is Structurally Present

- A `CodeFidelityGate` class exists at `src/superclaude/cli/audit/code_fidelity.py` with a callable `evaluate()` method.
- `SprintGatePolicy` at `sprint/executor.py:47-90` is no longer a stub: it invokes `CodeFidelityGate.evaluate()` after each task subprocess completes.
- The `execute_sprint()` mainline at lines 668-787 drives `audit_task_*` state transitions based on `CodeFidelityResult.passed`.

### 5.2 Programmatic Checks Catch the cli-portify Defect Class

Given a fixture file containing the exact pattern from `executor.py:397-399`:
```python
if self._step_runner is not None:
    exit_code, stdout, timed_out = self._step_runner(step)
else:
    exit_code, stdout, timed_out = 0, "", False
```
...`noop_detector.scan_for_noop_fallbacks()` returns at least one `NoopFinding` with `severity="HIGH"`.

Given a phase file with a WIRING assertion for `step_runner` as provider and `PortifyExecutor.__init__` as consumer, and a code directory where `run_portify()` does not pass `step_runner=` to `PortifyExecutor`, the WIRING check fails (reference check finds no call site with `step_runner=` keyword).

### 5.3 Deterministic Replay Stability

Running `CodeFidelityGate.evaluate()` on the same inputs twice produces `CodeFidelityResult` instances with identical `passed`, `failure_phase`, and `checks[].passed` values. LLM-assisted checks may produce different `evidence_refs` text but must not flip `passed` on Phase A results.

(This satisfies the v1.2.1 spec M4 determinism requirement, Section 8.3.)

### 5.4 State Machine Integration

- A task with `audit_gate_required: true` in its phase file cannot transition to `completed` until `CodeFidelityGate.evaluate()` returns `passed=True`.
- The illegal transition `audit_task_failed -> completed` (without approved override) is enforced per v1.2.1 spec Section 4.2, item 4.
- A task with `audit_gate_required: false` or absent (under `legacy_migration`) is not blocked.

### 5.5 Tasklist Generator Emits Structured Assertions

Running `superclaude tasklist run` against a roadmap that contains executor dispatch requirements produces phase files with at least one WIRING assertion in `code_fidelity_assertions` for any task whose acceptance criteria include the words "routes", "wires", "calls", "dispatches", or equivalent.

### 5.6 Evidence Requirements

Every failed check in `CodeFidelityResult.checks` includes a non-empty `evidence` field containing a `file:line` reference or a file path. A check may not fail with `evidence=None` unless `failure_class="system"` (gate runner error).

(This satisfies v1.2.1 spec Section 5.3 evidence requirements.)

---

## 6. Risk Assessment

### 6.1 False Positive Risk: WIRING Checks on Dynamic Dispatch

**Scenario**: A codebase uses dynamic dispatch (`getattr`, dictionary lookup, `importlib`) instead of static imports. The AST-based WIRING check scans for `Import`/`ImportFrom` nodes and `Name`/`Attribute` references. Dynamic dispatch produces no static import nodes; the check would report WIRING failure even though the wiring is present.

**Mitigation**: The WIRING check must include a secondary scan for dictionary literals with string keys matching the provider symbol name (e.g., `{"validate-config": run_validate_config}` dispatch maps). This covers the `STEP_REGISTRY`/`STEP_DISPATCH` dictionary pattern that any correct fix to the cli-portify executor would use. If neither static import nor dictionary reference is found, the check falls through to a BEHAVIORAL assertion for LLM evaluation.

**Residual risk**: If the codebase uses fully dynamic dispatch (`module = importlib.import_module(name); fn = getattr(module, fn_name)()`), no AST check will catch missing wiring. This case should be flagged as a `standard`-warning rather than a `strict`-block, with the developer expected to add a BEHAVIORAL assertion that the LLM can evaluate.

### 6.2 False Negative Risk: Acceptance Criteria That Don't Require WIRING Assertions

**Scenario**: The tasklist generator (after this proposal's changes) fails to classify an acceptance criterion as requiring a WIRING assertion. The criterion is written as "the executor should invoke each step" (passive voice, no explicit connection language), so the generator emits only a BEHAVIORAL assertion. The LLM evaluates the behavioral assertion and (incorrectly) passes it on a no-op implementation.

**Mitigation**: The tasklist generator classification rules must include passive-voice patterns ("should invoke", "must call", "will execute") as WIRING triggers, not just active patterns ("calls", "routes to"). This is a content expansion of the classification table in Section 2.7. Additionally, any task in a `Tier=STRICT` phase that produces code files must have at least one WIRING assertion generated, even if no explicit connection language is present — this is a minimum density requirement.

**Residual risk**: Acceptance criteria that are fundamentally behavioral without naming a connection (e.g., "the pipeline produces correct output") cannot be reduced to WIRING assertions. These remain LLM-evaluated and retain the LLM reliability ceiling.

### 6.3 False Positive Risk: Accepting Stub Implementations That Pass AST Checks

**Scenario**: A developer implements a function that is correctly imported and referenced but whose body is a stub (`return (0, "", False)` without actually invoking the intended logic). DELIVERABLE and WIRING checks both pass. BEHAVIORAL check may pass if the LLM is not provided enough context.

**Mitigation**: The DELIVERABLE check's `min_lines` threshold provides partial protection (a one-line stub function fails the minimum line requirement for a non-trivial implementation). The `noop_detector` module specifically scans for constant-return stubs in `Optional[Callable]` fallback branches. For deeper stubs, the BEHAVIORAL assertion must include explicit evidence requirements (`evidence_required: ["call_site", "return_path_not_constant"]`) and the LLM prompt must instruct Claude to check whether the function body is a constant-return stub.

### 6.4 Integration Risk: SprintGatePolicy Stub Completion May Break Existing Tests

**Scenario**: `SprintGatePolicy` at `sprint/executor.py:47-90` is currently a stub. Completing it changes the behavior of `execute_sprint()` for any test that exercises the sprint mainline. Existing tests that mock `SprintGatePolicy` or test sprint execution without audit fields in phase files may fail.

**Mitigation**: The `legacy_migration` profile behavior (gate passes with warning when no assertions declared) ensures backward compatibility. Tests written against pre-Link-3 phase files will exercise the `legacy_migration` path and continue to pass. New test fixtures must include `code_fidelity_assertions` to exercise the full gate. The `audit_gate_required: false` default in the task model (when the field is absent from phase frontmatter) provides a second backward-compatibility layer.

### 6.5 Scope Risk: Problem B Is Harder Than Problem A

**Scenario**: This proposal implements the structural gate (Problem A) but the acceptance criteria strengthening (Problem B, tasklist generator changes) is treated as lower priority or deferred. The gate is deployed with no `code_fidelity_assertions` in existing tasklist bundles. Under `legacy_migration` profile, every task passes. The gate provides false confidence.

**Mitigation**: The tasklist generator changes are a prerequisite for Link 3 providing meaningful protection, not an optional enhancement. The v1.2.1 spec (Section 1.2, Primary goals) requires "deterministic pass/fail gating with evidence-backed outputs." A gate that always passes under `legacy_migration` is not providing deterministic gating. The rollout sequence must enforce: `legacy_migration` only for bundles generated before the tasklist generator update; `standard` for all bundles generated after; `strict` at full enforcement. This mirrors the profile promotion criteria in spec Section 7.2.

---

## 7. Estimated Effort

### 7.1 Phase Mapping

The v1.2.1 spec (Section 10.1) defines a Phase 0–4 plan. Link 3 implementation maps across Phases 1–3 as a parallel track to the core audit gate work.

**Phase 0** (prerequisite — already specified in delta analysis):
- No Link 3 deliverables. Phase 0 focuses on retiring `_apply_resume_after_spec_patch()` and wiring `DEVIATION_ANALYSIS_GATE` into `_build_steps()`. These are not blocking for Link 3 development but are required before Phase 1 GO.

**Phase 1** (deterministic contracts):

| Deliverable | Effort |
|---|---|
| `code_fidelity.py` — `ProgrammaticChecker` + `CodeFidelityGate` skeleton | Medium (~1 sprint session) |
| `assertion_parser.py` | Small (~0.5 sprint session) |
| `noop_detector.py` | Small (~0.5 sprint session) |
| `tests/audit/test_code_fidelity.py` Phase A tests | Medium (~1 sprint session) |
| `tests/audit/test_noop_detector.py` | Small (~0.5 sprint session) |
| `pipeline/models.py` AssertionType enum | Trivial |

Phase 1 acceptance: `ProgrammaticChecker` deterministically catches the cli-portify defect class from a fixture. Phase A checks replay identically for same input. Phase 1 total: ~3.5 sprint sessions.

**Phase 2** (runtime controls + sprint integration):

| Deliverable | Effort |
|---|---|
| `LLMAssistantChecker` in `code_fidelity.py` | Medium (~1 sprint session) |
| `sprint/executor.py` — `SprintGatePolicy` completion | Medium (~1 sprint session) |
| `sprint/models.py` — `audit_gate_required` field | Small (~0.5 sprint session) |
| `tests/audit/test_code_fidelity.py` Phase B and integration tests | Medium (~1 sprint session) |

Phase 2 acceptance: `execute_sprint()` mainline invokes `CodeFidelityGate.evaluate()` after each task subprocess; `audit_task_*` state transitions are driven by result. Phase 2 total: ~3.5 sprint sessions.

**Phase 3** (tasklist generator + full integration):

| Deliverable | Effort |
|---|---|
| `sc-tasklist-protocol/SKILL.md` — assertion derivation rules | Medium-Large (~2 sprint sessions, requires validation against real roadmaps) |
| `make sync-dev` to `.claude/skills/sc-tasklist-protocol/SKILL.md` | Trivial |
| End-to-end integration test: tasklist → sprint → Link 3 gate | Medium (~1 sprint session) |

Phase 3 acceptance: running the full pipeline on a roadmap that includes executor dispatch requirements produces tasklist bundles with WIRING assertions; sprint execution against those bundles invokes Link 3 and blocks on wiring failures. Phase 3 total: ~3 sprint sessions.

**Phase 4** (rollout):
- Shadow mode: all existing sprint runs collect `CodeFidelityResult` artifacts but do not enforce.
- Soft mode: enforce for new bundles with `code_fidelity_assertions` present.
- Full mode: enforce for all bundles; `legacy_migration` only by explicit override.

### 7.2 Total Estimate

| Phase | Sprint sessions | Primary risk |
|---|---|---|
| Phase 1 | ~3.5 | AST analysis edge cases in dynamic dispatch |
| Phase 2 | ~3.5 | SprintGatePolicy integration breaking existing sprint tests |
| Phase 3 | ~3.0 | Tasklist generator classification accuracy |
| Phase 4 | ~1.0 | Rollout coordination |
| **Total** | **~11 sprint sessions** | |

### 7.3 Dependency on Other v1.2.1 Work

| Dependency | Blocking? |
|---|---|
| `AuditWorkflowState` enum in `sprint/models.py` (spec §4.1, delta Phase 1) | Yes — Link 3 drives these state transitions; they must exist before Phase 2 integration |
| `GateResult` dataclass (spec §6.1, delta Phase 1) | Partially — `CodeFidelityResult` is a specialization; the base `GateResult` should be defined first |
| `SprintGatePolicy` wiring (delta Phase 2 prerequisite) | Yes — Link 3 uses `SprintGatePolicy` as its integration hook |
| `audit_gate_required` in tasklist bundle (delta NR-1) | Yes — sprint executor uses this field to decide whether to invoke the gate |
| `DEVIATION_ANALYSIS_GATE` wiring (delta Phase 0 prerequisite) | No — independent pipeline stage |

The critical path is: Phase 0 cleanup → `AuditWorkflowState` + `GateResult` (spec Phase 1) → `SprintGatePolicy` completion (spec Phase 2) → Link 3 Phase 2 integration.

Link 3 Phase 1 (`ProgrammaticChecker`, `noop_detector`, unit tests) can begin in parallel with spec Phase 1 since it has no runtime dependencies — it is pure library code with no sprint imports.

---

## Appendix A: Concrete Assertion Examples for the cli-portify Defect

The following shows what `code_fidelity_assertions` should have looked like in the v2.25 tasklist for T03.04 (executor step dispatch task). Had this existed, Link 3 would have caught the defect.

```yaml
---
task_id: T03.04
audit_gate_required: true
code_fidelity_assertions:
  - type: WIRING
    id: WIRE-001
    description: "Each STEP_REGISTRY key must have a corresponding callable in a dispatch map"
    consumer: "src/superclaude/cli/cli_portify/executor.py"
    provider_symbol: "run_validate_config"
    provider_module: "superclaude.cli.cli_portify.steps.validate_config"
    context: "STEP_DISPATCH dictionary or equivalent dispatch map"

  - type: WIRING
    id: WIRE-002
    description: "run_portify() must pass step_runner= argument to PortifyExecutor constructor"
    consumer: "src/superclaude/cli/cli_portify/executor.py"
    provider_symbol: "step_runner"
    context: "PortifyExecutor constructor call in run_portify()"
    pattern: "keyword_argument"

  - type: DELIVERABLE
    id: DEL-001
    description: "steps/ directory must contain importable step modules"
    path: "src/superclaude/cli/cli_portify/steps/"
    required_symbols: ["run_validate_config", "run_discover_components", "run_analyze_workflow"]
    min_lines: 50

  - type: BEHAVIORAL
    id: BEH-001
    description: "Sequential executor loop calls a real step implementation for each STEP_REGISTRY entry, not a constant return"
    criterion: "When _execute_step() is called with any PortifyStep, it must invoke a function that performs filesystem, subprocess, or Claude invocation — not return (0, empty_string, False) unconditionally"
    evidence_required: ["call_site", "non_constant_return_path"]
    llm_evaluation: true
---
```

The WIRE-002 assertion would have failed the programmatic check: scanning `executor.py` for a call to `PortifyExecutor(` with a `step_runner=` keyword argument would find no such call site in the v2.25 code (line 1395-1401 shows the constructor call without `step_runner=`).

---

## Appendix B: Relation to Existing Gate Infrastructure

Link 3 follows the same pattern as `TASKLIST_FIDELITY_GATE` (`src/superclaude/cli/tasklist/gates.py:20-43`) and the `GateCriteria` infrastructure (`src/superclaude/cli/pipeline/gates.py`):

| Aspect | TASKLIST_FIDELITY_GATE | CodeFidelityGate (Link 3) |
|---|---|---|
| Subject | A document (tasklist vs roadmap) | Code output (files vs acceptance criteria) |
| Deterministic check | `high_severity_count == 0` in frontmatter | AST-based DELIVERABLE + WIRING checks |
| LLM check | LLM-generated deviation report | LLM-evaluated BEHAVIORAL assertions |
| Python enforcement | `_high_severity_count_zero`, `_tasklist_ready_consistent` | `passed` field in `CodeFidelityResult` |
| Blocking behavior | `enforcement_tier="STRICT"` | Profile-dependent (strict/standard/legacy) |
| Evidence requirement | `high_severity_count` integer | `evidence_refs: list[str]` per check |

The key difference: `TASKLIST_FIDELITY_GATE` validates a document; `CodeFidelityGate` validates code behavior. The document gate can rely entirely on LLM-generated YAML frontmatter because the subject is text. The code gate must rely on AST analysis first because code structure is deterministically parseable.
