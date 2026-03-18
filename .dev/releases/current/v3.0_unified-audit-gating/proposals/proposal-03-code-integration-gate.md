---
schema_version: "1.0"
proposal_id: "PROP-03"
title: "Code Integration Gate — Static Analysis for Orphaned Implementations and No-Op Fallbacks"
status: "draft"
date: "2026-03-17"
author: "forensic-analysis / v3.0-AuditGates"
parent_spec: "unified-audit-gating-v1.2.1-release-spec.md"
incident_reference: "cli-portify-executor-noop-forensic-report.md"
scoring_framework: "proposals/scoring-framework.md"
---

# Proposal 03: Code Integration Gate

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Proposed Solution](#2-proposed-solution)
3. [Detection Algorithm Suite](#3-detection-algorithm-suite)
4. [Integration with `audit/dead_code.py`](#4-integration-with-auditdead_codepy)
5. [Implementation Plan](#5-implementation-plan)
6. [Acceptance Criteria](#6-acceptance-criteria)
7. [Risk Assessment](#7-risk-assessment)
8. [Estimated Effort](#8-estimated-effort)

---

## 1. Problem Statement

### The "Defined but Not Wired" Pattern

The cli-portify executor shipped across three releases (v2.24, v2.24.1, v2.25) with every step returning
`(exit_code=0, stdout="", timed_out=False)`. The entire 12-step pipeline completed in milliseconds, wrote
a `return-contract.yaml` reporting `outcome: SUCCESS`, and exited. No real work was performed.

The root defect is structural: two development tracks were built independently and never joined.

**Track A** (executor infrastructure): `PortifyExecutor.__init__` accepts
`step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]] = None`. When `step_runner is None`,
`_execute_step()` falls through to:

```python
# executor.py:397-399
else:
    # Default: no-op (real subprocess invocation belongs in process.py)
    exit_code, stdout, timed_out = 0, "", False
```

**Track B** (step implementations): Eight modules in `cli_portify/steps/` plus standalone `execute_*`
functions inside `executor.py` itself (e.g., `execute_protocol_mapping_step()` at line 494).

`run_portify()` at `executor.py:1395-1401` constructs `PortifyExecutor` without ever passing `step_runner`:

```python
executor = PortifyExecutor(
    steps=steps,
    workdir=workdir,
    dry_run=config.dry_run,
    resume_from=getattr(config, "resume_from", "") or "",
    turn_budget=config.max_turns,
)
# step_runner is never provided — Track B is permanently bypassed
return executor.run()
```

The comment `"real subprocess invocation belongs in process.py"` documents an intention that was never
tasked, never implemented, and never detected by any gate.

### Three Known Instances of the Same Pattern

The forensic investigation identified this as a **recurring systemic pattern** across the codebase, not an
isolated accident:

| Instance | Defined | Where | Wired? | Effect |
|----------|---------|-------|--------|--------|
| `step_runner` / `_execute_step()` | `executor.py:323, 393-415` | `cli_portify/executor.py` | Never | All 12 portify steps no-op with exit code 0 |
| `DEVIATION_ANALYSIS_GATE` | `roadmap/gates.py:712-758` | `roadmap/gates.py` | `_build_steps()` in `roadmap/executor.py` never adds a `deviation-analysis` step | Gate object exists; `ALL_GATES` references it; roadmap pipeline never runs it |
| `SprintGatePolicy` / `TrailingGateRunner` | `sprint/executor.py:47-90`, `pipeline/trailing_gate.py` | Both modules imported | `execute_sprint()` never instantiates `TrailingGateRunner` or `SprintGatePolicy` | Trailing gate infrastructure silently inactive for all sprint runs |

These three instances share a structural fingerprint: a fully implemented component exists in the codebase,
is syntactically correct, passes any linter, but is never invoked from its intended caller in the
production code path.

### Why Existing Gates Do Not Catch This

Every gate in the pipeline follows one of two signatures:

```python
# Document content validation
(content: str) -> bool

# Artifact validation
(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]
```

They validate that **generated documents have correct structure**. The pipeline treats everything as a
document generation problem. Code is generated, but code requires wiring — and wiring is invisible to
document-level gates.

The `audit/dead_code.py` module detects files with **zero cross-boundary importers**, which catches
entirely unused modules. It does not catch the harder case: a module that *is* imported (e.g., for type
annotations or constants) but whose primary functions are never called from the production entry point.
It also cannot detect constructor parameters that are always passed `None`, or no-op fallback branches
that permanently masquerade as real execution.

The `DEVIATION_ANALYSIS_GATE` case is the purest example: `roadmap/gates.py` is imported by
`roadmap/executor.py` (Tier-A importer). Dead code detection would exclude it. But the `DEVIATION_ANALYSIS_GATE`
constant and its semantic check functions are never exercised because `_build_steps()` does not include a
`deviation-analysis` step.

---

## 2. Proposed Solution

A new static analysis module — `audit/integration_gate.py` — implements four deterministic checks using
Python's `ast` module to inspect source files without executing them. The checks produce structured
findings that integrate with the existing `GateCriteria` / `gate_passed()` infrastructure via a new
`INTEGRATION_GATE` constant in `pipeline/gates.py`.

The four checks are designed to be **falsifiable**: each produces a specific finding with file path, line
number, and a human-readable explanation of what is defined versus what is wired.

### Design Constraints

- **No subprocess invocation** — pure AST analysis, no imports of the target code (NFR-003 compliant).
- **No LLM dependency** — all checks are deterministic, reproducible across runs.
- **Conservative by default** — uncertain cases are reported as warnings, not hard failures. Only
  patterns where the evidence is unambiguous produce ERROR-severity findings that block a gate.
- **Escape hatch via annotation** — any parameter or fallback can be annotated with a structured
  comment to suppress a finding (see Section 7).

---

## 3. Detection Algorithm Suite

### Check 1 — Constructor Parameter Coverage (CPC)

**What it detects**: Constructor parameters typed `Optional[Callable[...]]` that default to `None`
and are never passed a non-`None` value at any production call site within the codebase.

**Archetypal case**: `PortifyExecutor.__init__` has `step_runner: Optional[Callable[...]] = None`.
`run_portify()` constructs `PortifyExecutor(steps=..., workdir=..., ...)` — `step_runner` is absent
from every keyword argument list at every non-test call site.

**AST Pattern**:

```
FunctionDef(name="__init__")
  args.defaults: contains NameConstant(value=None)
  args.annotations: contains Subscript(value=Name(id="Optional"), ...)
                    where inner type is Callable or similar
```

Cross-referenced against all `Call` nodes targeting the class constructor anywhere outside
`tests/` directories. A finding is emitted when:
- The parameter is absent from all non-test call sites, AND
- The class body contains a conditional branch `if self.<param> is not None: <work>` with an `else`
  branch that returns a success value.

**Implementation sketch**:

```python
@dataclass
class CpcFinding:
    class_name: str
    file_path: str
    param_name: str
    param_line: int
    noop_branch_line: int
    call_sites: list[str]   # file:line for each constructor call found
    all_call_sites_omit_param: bool

def check_constructor_parameter_coverage(
    source_root: Path,
    exclude_dirs: list[str] | None = None,
) -> list[CpcFinding]:
    ...
```

**Failure output** (as it would appear in a gate report):

```
[CPC-001] ERROR: Optional callable parameter never provided at production call sites
  Class:      PortifyExecutor (cli_portify/executor.py:315)
  Parameter:  step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]] = None
  No-op at:   executor.py:397 — else branch returns (0, "", False)
  Call sites searched: 1 non-test call site found
    - executor.py:1395 — PortifyExecutor(steps=..., workdir=..., dry_run=...) — step_runner ABSENT
  Verdict: step_runner is never provided in production. Every call dispatches to the no-op branch.
```

---

### Check 2 — Import Reachability from Entry Points (IRE)

**What it detects**: Python files in designated implementation directories (e.g., `steps/`) whose
public functions are not reachable via any transitive import chain from the module's declared entry
point.

**Archetypal case**: `cli_portify/steps/validate_config.py`, `discover_components.py`,
`analyze_workflow.py`, etc. are never imported by `cli_portify/executor.py`, `commands.py`, or
`cli.py`. The entry point `commands.py → run_portify() → PortifyExecutor.run()` has no path to
any of these modules.

**Algorithm**:

1. Parse all `import` and `from ... import` statements across the source tree using AST (Tier-A
   edges, same confidence tier as `audit/dependency_graph.py`).
2. Build a directed reachability graph: `{module: set_of_transitively_imported_modules}`.
3. For each file in a configured "must-be-reachable" directory pattern (e.g., `**/steps/*.py`),
   walk the graph from the declared entry point. If the module is not reachable, emit a finding.
4. Exclude `__init__.py`, `conftest.py`, test files, and files matching framework hook patterns
   (same exclusion logic as `dead_code.py`).

**Configuration** (per-package, stored in `pyproject.toml` or a `integration_gate.toml`):

```toml
[[integration_gate.reachability_rules]]
entry_point = "src/superclaude/cli/cli_portify/commands.py"
must_reach   = "src/superclaude/cli/cli_portify/steps/"
label        = "portify-steps"
```

**Implementation sketch**:

```python
@dataclass
class IreFinding:
    unreachable_module: str   # e.g., "cli_portify/steps/validate_config.py"
    entry_point: str
    rule_label: str
    exported_symbols: list[str]

def check_import_reachability(
    entry_points: list[Path],
    must_reach_dirs: list[Path],
    source_root: Path,
) -> list[IreFinding]:
    ...
```

**Failure output**:

```
[IRE-001] ERROR: Implementation module unreachable from entry point
  Entry point: cli_portify/commands.py → run_portify() → PortifyExecutor.run()
  Unreachable: cli_portify/steps/validate_config.py
  Exports:     run_validate_config, ValidateConfigResult
  Impact:      run_validate_config is never called; validate-config step uses no-op fallback
  (8 modules affected: validate_config, discover_components, analyze_workflow, design_pipeline,
   synthesize_spec, brainstorm_gaps, panel_review, gates)
```

---

### Check 3 — No-Op Fallback Detection (NOPF)

**What it detects**: Code patterns where a callable or value is tested for `None`, and the `None`
branch silently returns a success indicator (exit code 0, `True`, `"SUCCESS"`, a named success enum
member, or an empty tuple matching `(0, "", False)`).

This is the **most direct detector** of the cli-portify bug class. The pattern is:

```python
if self._step_runner is not None:
    exit_code, stdout, timed_out = self._step_runner(step)
else:
    exit_code, stdout, timed_out = 0, "", False   # <- no-op returning success
```

**AST Pattern** (both forms):

```
If(
  test=Compare(left=Attribute(...), ops=[IsNot()], comparators=[NameConstant(None)]),
  body=[<real work>],
  orelse=[<assignment of success tuple/value>]
)

Or equivalently:

If(
  test=Compare(left=Attribute(...), ops=[Is()], comparators=[NameConstant(None)]),
  body=[<assignment of success tuple/value>],   # None branch first
  orelse=[<real work>]
)
```

**Success indicator heuristics**: The `else` branch is classified as a no-op success fallback when
it assigns any of:
- An integer literal `0` to a variable named `exit_code`, `rc`, `returncode`, or `code`
- A boolean `True` to a variable named `passed`, `ok`, `success`, or `result`
- A string literal matching known success strings (`"SUCCESS"`, `"PASS"`, `"OK"`, `""`)
- A tuple `(0, ...)` where the first element is the integer `0`

**Implementation sketch**:

```python
@dataclass
class NopfFinding:
    file_path: str
    line_number: int
    guarded_attr: str         # e.g., "self._step_runner"
    noop_return_value: str    # e.g., "(0, '', False)"
    severity: str             # "ERROR" if in production path; "WARNING" if only in test helpers

def check_noop_fallbacks(
    source_files: list[Path],
    test_path_patterns: list[str] | None = None,
) -> list[NopfFinding]:
    ...
```

**Failure output**:

```
[NOPF-001] ERROR: No-op fallback returning success detected
  File:    cli_portify/executor.py:397-399
  Pattern: if self._step_runner is not None: <real work> else: (0, "", False)
  Risk:    The None branch unconditionally reports success. If _step_runner is never
           provided, all invocations silently succeed with zero work performed.
  Also at: executor.py:408-411 (retry path — same pattern)
```

---

### Check 4 — Registry Completeness (REGC)

**What it detects**: Dictionary or list constants that function as step/plugin registries — where
each entry has a string identifier and configuration metadata — but where one or more IDs have no
corresponding importable function in any module reachable from the entry point.

**Archetypal case**: `STEP_REGISTRY` in `executor.py` is a `dict[str, dict]` mapping step IDs to
metadata (`phase_type`, `timeout_s`, `retry_limit`). None of its 12 entries contains a function
reference or import. The registry provides step configuration for the executor loop but does not
wire step IDs to their implementations.

**Heuristic for "registry-like" constants**:
- Module-level assignment to an ALL_CAPS name
- Value is a `dict` or `list` literal
- At least one entry contains a key named `"step_id"`, `"id"`, `"name"`, or `"type"`
- Entries have a consistent structure (same key set across multiple entries)

**Cross-reference check**: For each string ID found in the registry, search the reachability graph
for a function or class whose name contains or matches the ID (with normalization: `"validate-config"` →
`validate_config`, `run_validate_config`, `ValidateConfig`, etc.). If no match is found in any
reachable module, emit a finding.

**Implementation sketch**:

```python
@dataclass
class RegcFinding:
    registry_name: str       # e.g., "STEP_REGISTRY"
    registry_file: str
    step_id: str
    matched_functions: list[str]   # empty if none found
    verdict: str             # "no_implementation" | "implementation_unreachable"

def check_registry_completeness(
    source_files: list[Path],
    entry_points: list[Path],
    registry_patterns: list[str] | None = None,
) -> list[RegcFinding]:
    ...
```

**Failure output**:

```
[REGC-001] WARNING: Registry step has no reachable implementation
  Registry: STEP_REGISTRY (cli_portify/executor.py)
  Step ID:  "validate-config"
  Searched: all modules reachable from cli_portify/commands.py
  Found:    cli_portify/steps/validate_config.py::run_validate_config
            BUT this module is unreachable from the entry point (see IRE-001)
  Verdict:  implementation_unreachable
  (12 of 12 STEP_REGISTRY entries have this status)
```

Note: REGC findings are `WARNING` severity by default when the implementation exists but is
unreachable (that is already an `IRE` ERROR). They escalate to `ERROR` when no matching
implementation exists anywhere in the codebase.

---

## 4. Integration with Existing `audit/dead_code.py`

### What `dead_code.py` Already Does

`audit/dead_code.py` implements T03.07 / D-0023 using the 3-tier dependency graph from
`audit/dependency_graph.py`. It classifies a file as a dead code candidate when:

- The file has exports (`analysis.exports` is non-empty)
- It is not an entry point (`__main__`, `main.py`, `cli.py`, etc.)
- It is not a framework hook (`pytest_*`, `conftest`, `plugin`, etc.)
- Tier-A importers count is 0 AND Tier-B references count is 0

This catches files that are **entirely disconnected** from the import graph. The `steps/` modules
in cli-portify are not caught by this check because they *may* be imported somewhere (even if only
in test files or for type references), and dead code detection has no concept of "imported but
never called in production path."

### Gap Between Dead Code Detection and Integration Checking

The two checks are complementary and address different points on the reachability spectrum:

| Condition | Dead Code Detection | Integration Gate |
|-----------|--------------------|--------------------|
| Module never imported anywhere | **Catches** (zero Tier-A/B importers) | Also catches (IRE) |
| Module imported only in tests | Does not catch (test importer counts) | **Catches** (IRE: production unreachable) |
| Module imported by executor but functions never called | Does not catch | **Catches** (REGC, CPC) |
| Constructor parameter always `None` in production | Does not catch | **Catches** (CPC) |
| No-op fallback returning success | Does not catch | **Catches** (NOPF) |

### Reuse Strategy

`audit/integration_gate.py` should reuse the following directly from existing modules:

**From `audit/dependency_graph.py`**:
- `DependencyEdge`, `EdgeTier`, `DependencyGraph` — the IRE check builds on Tier-A edges
- `TIER_CONFIDENCE` — same confidence scoring applies to reachability assertions

**From `audit/dead_code.py`**:
- `_is_entry_point()` — same entry point exclusion logic (do not duplicate)
- `_is_framework_hook()` — same framework hook exclusion patterns

**From `audit/tool_orchestrator.py`**:
- `FileAnalysis` — the existing analysis data structure includes `exports` lists that can seed
  the REGC implementation check

The integration gate does **not** subclass or extend `DeadCodeReport`. It produces its own
`IntegrationReport` dataclass with four finding lists (one per check). Both reports can be
emitted independently and combined at the gate enforcement layer.

### Shared Infrastructure Candidates

Two pieces of new infrastructure are useful to both `dead_code.py` and `integration_gate.py` and
should be extracted to a shared module `audit/ast_utils.py`:

1. **`build_import_graph(source_root) -> dict[str, set[str]]`** — resolves all `import` and
   `from ... import` statements across a source tree into a module adjacency map. Currently each
   module that needs import information re-implements this. The IRE check requires a full
   transitive closure; extracting this into a shared utility prevents duplication.

2. **`iter_ast_files(source_root, exclude_patterns) -> Iterator[tuple[Path, ast.Module]]`** —
   yields `(path, parsed_ast)` for all `.py` files matching inclusion/exclusion rules. Handles
   `SyntaxError` gracefully (skip with warning). Used by CPC, NOPF, and REGC checks.

---

## 5. Implementation Plan

### New Files

| File | Purpose |
|------|---------|
| `src/superclaude/cli/audit/integration_gate.py` | Four detection checks: CPC, IRE, NOPF, REGC; `IntegrationReport` dataclass; `run_integration_checks()` entry point |
| `src/superclaude/cli/audit/ast_utils.py` | Shared `build_import_graph()` and `iter_ast_files()` utilities |
| `tests/audit/test_integration_gate.py` | Unit tests with fixture source trees covering all four checks |

### Modified Files

| File | Change |
|------|--------|
| `src/superclaude/cli/pipeline/gates.py` | Add `INTEGRATION_GATE` constant (new `GateCriteria` with `enforcement_tier="STRICT"` and semantic checks that call `run_integration_checks()`) |
| `src/superclaude/cli/pipeline/models.py` | Add `IntegrationCheckResult` to `SemanticCheck` payload type if needed |
| `src/superclaude/cli/audit/__init__.py` | Export `IntegrationReport`, `run_integration_checks` |
| `src/superclaude/cli/roadmap/executor.py` | Wire `INTEGRATION_GATE` into `_build_steps()` as a new step after `spec-fidelity` (also resolves the DEVIATION_ANALYSIS_GATE wiring gap if that step is added simultaneously) |

### Integration Gate Placement in Pipeline

The integration gate is a **pre-release static analysis step**, not a per-artifact content gate.
It runs against the codebase rather than a generated document. Two insertion points are appropriate:

**Option A — As a roadmap pipeline step** (preferred for catching "defined but not wired" before
a release is planned):
- Add as step 9 in `_build_steps()` after `spec-fidelity`
- Input: the source root directory
- Output: `integration-report.md` with structured findings
- Gate: `INTEGRATION_GATE` validates the report's frontmatter (`error_count == 0`)

**Option B — As a sprint pre-flight check** (catches wiring gaps at implementation time):
- Run in the preflight executor before any sprint step begins
- Block sprint execution if ERROR-severity findings exist
- Provides faster feedback loop: the gate fires during development, not post-release

Both options are compatible; Option A provides release-tier enforcement and Option B provides
development-time feedback. The proposal recommends implementing Option A first (simpler integration
path) with Option B as a follow-on.

### `INTEGRATION_GATE` Definition

```python
# In pipeline/gates.py or pipeline/models.py

from superclaude.cli.audit.integration_gate import run_integration_checks, IntegrationReport

def _integration_gate_check(content: str) -> bool:
    """content is the integration-report.md frontmatter; check error_count == 0."""
    import yaml, re
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False
    meta = yaml.safe_load(match.group(1))
    return int(meta.get("error_count", 1)) == 0

INTEGRATION_GATE = GateCriteria(
    required_frontmatter_fields=[
        "schema_version",
        "source_root",
        "entry_points_checked",
        "error_count",
        "warning_count",
        "checks_run",
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="zero_error_findings",
            check_fn=_integration_gate_check,
            failure_message="Integration gate found ERROR-severity findings; pipeline blocked",
        ),
    ],
)
```

---

## 6. Acceptance Criteria

### Would This Gate Have Caught the `step_runner=None` Bug?

**Answer: Yes — three of four checks would independently fire.**

| Check | Finding | Severity | Would Block? |
|-------|---------|----------|-------------|
| CPC | `step_runner` is `Optional[Callable]` defaulting to `None`; `run_portify()` never passes it | ERROR | Yes |
| IRE | `cli_portify/steps/*.py` (8 modules) unreachable from `commands.py` | ERROR | Yes |
| NOPF | `executor.py:397-399` and `executor.py:408-411` — no-op returning `(0, "", False)` | ERROR | Yes |
| REGC | 12 of 12 `STEP_REGISTRY` entries have implementations unreachable from entry point | WARNING (escalated from IRE ERROR) | Via IRE |

Any single one of CPC, IRE, or NOPF would have blocked the pipeline before a release was cut.
All three firing simultaneously provides redundancy: fixing one does not clear the gate unless the
underlying wiring is actually completed.

### Would This Gate Have Caught the Other Two Known Instances?

**`DEVIATION_ANALYSIS_GATE` unwired from `_build_steps()`**:
- REGC applies: `ALL_GATES` in `roadmap/gates.py` is a list constant (registry-like). The entry
  `("deviation-analysis", DEVIATION_ANALYSIS_GATE)` references a gate for which there is no step
  in `_build_steps()` with `id="deviation-analysis"`. This yields a REGC WARNING.
- IRE does not directly apply (gate objects are not functions to be called from steps).
- The REGC finding would not be ERROR severity without a supplementary check that cross-references
  gate IDs against step IDs in `_build_steps()` output. This is a reasonable extension of REGC
  for gate-heavy codebases (add as REGC variant: "gate defined but no step uses it").

**`SprintGatePolicy` / `TrailingGateRunner` unwired in `execute_sprint()`**:
- IRE applies: `SprintGatePolicy` is defined in `sprint/executor.py` and `TrailingGateRunner` is
  defined in `pipeline/trailing_gate.py`. Both are imported at the module level. However,
  `execute_sprint()` never instantiates either. This is a "imported but never instantiated in
  production path" case — subtler than "not imported at all."
- This requires a REGC variant: scan for classes that implement a named Protocol
  (`TrailingGatePolicy`) and verify that at least one production call site instantiates them.
- Without this variant, the sprint gate unwiring produces a WARNING (potential issue flagged)
  rather than an ERROR.

### Formal Acceptance Tests

The following test cases must pass before the gate is marked ready:

1. **CPC test**: A fixture class with `Optional[Callable] = None` parameter + a call site omitting
   the parameter + a no-op `else` branch → CPC finds exactly one ERROR finding.
2. **IRE test**: A fixture `steps/` directory with two modules, neither imported by the entry
   point → IRE finds exactly two ERROR findings.
3. **NOPF test**: Source text containing the exact `executor.py:397-399` pattern → NOPF finds
   exactly one ERROR finding at the correct line number.
4. **REGC test**: A `STEP_REGISTRY`-style dict with three entries; one has a reachable
   implementation, two do not → REGC finds two `implementation_unreachable` findings.
5. **Suppression test**: A finding suppressed with `# integration-gate: ignore(CPC-001) reason=dry-run`
   comment → the finding is demoted to INFO and does not contribute to `error_count`.
6. **False positive test (dry-run)**: A class with `runner: Optional[Callable] = None` where the
   only non-test call site uses `runner=DryRunRunner()` → CPC produces zero findings.
7. **False positive test (test doubles)**: A class constructor call in `tests/` with
   `step_runner=mock_runner` should not count as a production call site and should not prevent
   CPC from finding the production omission.

---

## 7. Risk Assessment

### Risk 1 — Intentional Optional Callables (Dry-Run Patterns)

**Description**: Some `Optional[Callable]` parameters are genuinely optional by design. Dry-run
modes, feature-flagged behaviors, and extensibility hooks all use `None` defaults where `None`
means "do nothing" and that is the correct production behavior in specific conditions (e.g.,
`--dry-run` flag).

**Distinguishing heuristic**: The cli-portify no-op is pathological because:
- The `None` branch returns a **success** code, not a neutral/no-op result
- The parameter was intended for test injection, per its docstring ("Used for testing")
- No production call site ever passes a non-`None` value

A genuinely optional callback typically:
- Has a docstring or comment explaining when `None` is the correct value
- Has call sites that **conditionally** pass `None` based on a flag (e.g., `runner=None if dry_run else real_runner`)
- Returns a neutral sentinel rather than a success code

**Mitigation**: CPC severity should be downgraded from ERROR to WARNING when any non-test call
site passes `None` **conditionally** (i.e., in a branch), as that indicates intentional use of
the `None` path. ERROR severity applies only when every production call site is missing the
parameter entirely or always passes `None` unconditionally.

**Suppression annotation** (structured comment, co-located with the parameter):
```python
step_runner: Optional[Callable[[PortifyStep], tuple[int, str, bool]]] = None,
# integration-gate: ignore(CPC-001) reason=dry-run-design
```
This requires explicit documentation of intent, which is itself a code quality improvement.

### Risk 2 — Test Double Injection

**Description**: Dependency injection via constructor parameters is a standard testability pattern.
Many classes are designed with `Optional[Callable]` parameters specifically so tests can inject
mock implementations. The gate should not flag classes that are correctly designed for testing.

**Distinguishing heuristic**: The key question is whether **production** call sites (outside
`tests/`) always omit or always pass `None`. If production call sites pass real implementations
and test call sites pass mocks, the gate produces zero findings — this is the correct and
desirable pattern.

**Mitigation**: The CPC check already scopes call site search to non-test paths. The test double
risk is specifically that a class is used **only** in tests (meaning `dead_code.py` might catch
it first) or that no production call site exists at all (which is a legitimate finding, not a
false positive).

### Risk 3 — Dynamic Construction and Factories

**Description**: Some call sites construct objects via factory functions, configuration-driven
dispatch, or `importlib`-based dynamic loading. AST analysis cannot resolve these paths.

**Example**: `executor = ExecutorFactory.create(config)` where the factory internally passes
`step_runner`. The direct `PortifyExecutor(...)` call site analysis would not see this.

**Mitigation**: The `audit/dynamic_imports.py` module already exists in the codebase and handles
dynamic import patterns. CPC should check `audit/dynamic_imports.py`'s output before emitting
a finding: if the class is constructed via a detected dynamic factory, downgrade to WARNING.
Additionally, the suppression annotation mechanism handles cases the heuristic misses.

### Risk 4 — False Negatives in IRE (Conditional Imports)

**Description**: Some modules use conditional imports (`try: import X except ImportError: ...`
or `if TYPE_CHECKING: from X import Y`). AST-level import analysis may miss these, causing IRE
to incorrectly report a module as unreachable.

**Mitigation**: Parse both `import` statements and `ImportFrom` nodes regardless of whether they
appear in `if TYPE_CHECKING:` blocks. Flag `TYPE_CHECKING`-only imports as Tier-C confidence
edges (consistent with `audit/dependency_graph.py` tier semantics) so they count as reachability
evidence at lower confidence but do not produce Tier-A reachability assertions.

### Risk 5 — Noisy Findings at Scale

**Description**: In a large codebase, IRE and REGC may produce many findings for legitimately
isolated modules (e.g., standalone utility scripts, migration files, one-off analysis tools).

**Mitigation**: The `integration_gate.toml` configuration allows per-package scoping: the
`must_reach` rules apply only to explicitly configured directories. By default, only directories
whose names contain `steps`, `handlers`, `runners`, or `implementations` are checked. All other
modules are excluded from IRE unless explicitly configured.

---

## 8. Estimated Effort

### Implementation (Coding)

| Component | Estimate | Notes |
|-----------|----------|-------|
| `audit/ast_utils.py` — shared AST traversal utilities | 1 day | `iter_ast_files()`, `build_import_graph()`, `_resolve_module_path()` |
| `audit/integration_gate.py` — CPC check | 2 days | AST pattern matching for `Optional[Callable]`, call site traversal, no-op branch detection |
| `audit/integration_gate.py` — IRE check | 2 days | Transitive reachability graph, entry point → module set computation |
| `audit/integration_gate.py` — NOPF check | 1 day | If/else AST pattern; success indicator heuristics |
| `audit/integration_gate.py` — REGC check | 1.5 days | Registry constant detection; ID normalization; implementation lookup |
| `INTEGRATION_GATE` wiring in `pipeline/gates.py` | 0.5 days | GateCriteria definition, frontmatter schema |
| `_build_steps()` integration in `roadmap/executor.py` | 0.5 days | New step definition, output path, gate assignment |
| Suppression annotation parser | 0.5 days | Structured comment `# integration-gate: ignore(...)` |

**Total implementation**: ~9 days

### Testing

| Component | Estimate |
|-----------|----------|
| Fixture source trees (synthetic Python files for each check) | 1 day |
| Unit tests for all 7 acceptance criteria cases | 1.5 days |
| Integration test against actual `cli_portify/` source tree | 0.5 days |
| False positive validation (dry-run, test double, factory patterns) | 1 day |

**Total testing**: ~4 days

### Review and Hardening

| Component | Estimate |
|-----------|----------|
| Configuration schema and documentation | 0.5 days |
| Edge case hardening (syntax errors, encoding issues, circular imports) | 1 day |
| Performance profiling on full source tree (target: < 10s on `src/`) | 0.5 days |

**Total review**: ~2 days

### Overall Estimate

**~15 developer-days** for a production-ready implementation covering all four checks with tests
and documentation. A minimum viable implementation (CPC + NOPF only, covering the archetypal
bug) could be delivered in **~5 days**.

### Priority Ordering

If resources are constrained, implement in this order (each stage independently valuable):

1. **Stage 1** (5 days): NOPF + CPC — directly targets the archetypal bug class; highest catch
   rate for the specific incident.
2. **Stage 2** (4 days): IRE — catches unreachable implementations; broader generalizability.
3. **Stage 3** (4 days): REGC + configuration framework — registry completeness; useful for
   all future step-registry-based components.
4. **Stage 4** (2 days): Suppression annotations + dynamic factory handling — reduces false
   positives; required for sustainable adoption.

---

*Proposal prepared: 2026-03-17. Status: draft — pending scoring against `proposals/scoring-framework.md`.*
