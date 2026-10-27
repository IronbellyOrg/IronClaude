---
release: wiring-verification-gate-v1.0
version: 1.0.0
status: draft
date: 2026-03-17
parent_analysis: cli-portify-executor-noop-forensic-report.md
parent_ranking: proposal-ranking.md
fidelity_link: "Link 3: Tasklist -> Code"
priority: P0
estimated_scope: 410-500 lines production code
---

# Wiring Verification Gate v1.0 -- Release Specification

## 1. Problem Statement

The cli-portify executor no-op bug (forensic report, 2026-03-17) demonstrated that
Link 3 of the fidelity chain (Tasklist -> Code) has zero programmatic coverage. The
pipeline's gate infrastructure validates documents -- not code integration. Components
defined in specifications and decomposed into tasks can pass all existing gates while
producing code where modules are never connected to their consumers.

**The "defined but not wired" pattern recurs across multiple systems:**

| System | Evidence |
|--------|----------|
| cli-portify executor | `step_runner=None` default; steps exist but are never called |
| DEVIATION_ANALYSIS_GATE | Defined at `roadmap/gates.py:712` but never wired into `_build_steps()` |
| SprintGatePolicy | Exists at `sprint/executor.py:46-89` but `build_remediation_step` is not invoked from the sprint loop |
| Trailing gate framework | `TrailingGateRunner` exists but `execute_sprint()` never calls it |

**This release creates the first code-level gate in the pipeline.**

---

## 2. Goals and Non-Goals

### Goals

1. Detect unwired injectable dependencies (`Optional[Callable] = None` never provided at any call site)
2. Detect orphan modules (exported functions never imported by any consumer)
3. Detect unwired dispatch registries (dictionary entries mapping to non-importable functions)
4. Emit a structured YAML report compatible with the `GateCriteria`/`SemanticCheck` pattern
5. Deploy in shadow mode initially, with a path to soft and full enforcement

### Non-Goals (v1.0)

- No-op fallback detection (deferred to v1.1 pending shadow-mode data)
- Cross-language analysis (Python only)
- Runtime behavioral verification (see Smoke Test Gate proposal)
- Dynamic dispatch resolution (`**kwargs`, `getattr`, `importlib`)
- Modifying the `SemanticCheck` interface (no `pre_checks` in this release)

---

## 3. Architecture

### 3.1 System Context

```
Existing Pipeline Infrastructure          New Component
================================          =============

pipeline/models.py                        audit/wiring_gate.py
  GateCriteria ─────────────────────────>   WIRING_GATE (constant)
  SemanticCheck ────────────────────────>   check functions

pipeline/gates.py
  gate_passed() ────────────────────────>   evaluates WIRING_GATE

sprint/executor.py
  SprintGatePolicy ─────────────────────>   invokes wiring checks post-task

pipeline/trailing_gate.py
  TrailingGateRunner ───────────────────>   deferred evaluation (shadow mode)
  resolve_gate_mode() ──────────────────>   scope-aware enforcement
```

### 3.2 Module Architecture

```
src/superclaude/cli/audit/wiring_gate.py    (NEW -- core analysis)
    |
    |--- WiringFinding (dataclass)
    |--- WiringReport (dataclass)
    |--- analyze_unwired_callables(paths) -> list[WiringFinding]
    |--- analyze_orphan_modules(paths, root) -> list[WiringFinding]
    |--- analyze_unwired_registries(paths) -> list[WiringFinding]
    |--- run_wiring_analysis(target_dir) -> WiringReport
    |--- emit_report(report, output_path) -> None
    |--- check_wiring_report(content: str) -> bool    # SemanticCheck-compatible
    |
    |--- WIRING_GATE = GateCriteria(...)              # gate definition

src/superclaude/cli/audit/wiring_config.py  (NEW -- configuration)
    |
    |--- WiringConfig (dataclass)
    |--- DEFAULT_REGISTRY_PATTERNS
    |--- DEFAULT_WHITELIST
    |--- load_wiring_config(path) -> WiringConfig
```

### 3.3 Data Flow

```
                    +-----------------+
                    | Task completes  |
                    | (sprint runner) |
                    +--------+--------+
                             |
                             v
                    +--------+--------+
                    | Collect changed |
                    | file paths      |
                    | (git diff)      |
                    +--------+--------+
                             |
                             v
                +------------+------------+
                | run_wiring_analysis()   |
                |                         |
                | 1. analyze_unwired_     |
                |    callables()          |
                | 2. analyze_orphan_      |
                |    modules()            |
                | 3. analyze_unwired_     |
                |    registries()         |
                +------------+------------+
                             |
                             v
                +------------+------------+
                | emit_report()           |
                | -> wiring-report.md     |
                | (YAML frontmatter +     |
                |  finding details)       |
                +------------+------------+
                             |
                             v
                +------------+------------+
                | gate_passed(            |
                |   wiring-report.md,     |
                |   WIRING_GATE           |
                | )                       |
                +------------+------------+
                             |
                    +--------+--------+
                    |  shadow: log    |
                    |  soft: warn     |
                    |  full: block    |
                    +--------+--------+
```

---

## 4. Detailed Design

### 4.1 Data Models

```python
# src/superclaude/cli/audit/wiring_gate.py

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from ..pipeline.models import GateCriteria, SemanticCheck


@dataclass
class WiringFinding:
    """A single wiring verification finding."""

    finding_type: Literal["unwired_callable", "orphan_module", "unwired_registry"]
    file_path: str
    symbol_name: str
    line_number: int
    detail: str
    severity: Literal["critical", "major"] = "critical"

    def to_dict(self) -> dict[str, str | int]:
        return {
            "finding_type": self.finding_type,
            "file_path": self.file_path,
            "symbol_name": self.symbol_name,
            "line_number": self.line_number,
            "detail": self.detail,
            "severity": self.severity,
        }


@dataclass
class WiringReport:
    """Aggregate wiring analysis results."""

    target_dir: str
    files_analyzed: int = 0
    unwired_callables: list[WiringFinding] = field(default_factory=list)
    orphan_modules: list[WiringFinding] = field(default_factory=list)
    unwired_registries: list[WiringFinding] = field(default_factory=list)

    @property
    def unwired_count(self) -> int:
        return len(self.unwired_callables)

    @property
    def orphan_count(self) -> int:
        return len(self.orphan_modules)

    @property
    def registry_count(self) -> int:
        return len(self.unwired_registries)

    @property
    def total_findings(self) -> int:
        return self.unwired_count + self.orphan_count + self.registry_count

    @property
    def passed(self) -> bool:
        return self.total_findings == 0
```

#### 4.1.1 TurnLedger Extensions

The TurnLedger class (base definition at `sprint/models.py:488-525`) gains wiring-gate-specific
fields and methods for budget tracking. Generic `debit_gate()`/`credit_gate()` generalization
is deferred to v3.3.

**New fields** (all with defaults — backward-compatible with existing TurnLedger instances):

```python
# On TurnLedger (sprint/models.py)
wiring_gate_cost: int = 0        # Cumulative turns debited for wiring analysis
wiring_gate_credits: int = 0     # Cumulative turns credited back on pass
wiring_gate_scope: GateScope = GateScope.TASK  # Scope at which wiring gate operates
```

**New methods**:

```python
def debit_wiring(self, turns: int) -> None:
    """Debit turns for wiring analysis execution.

    Called before run_wiring_analysis(). Unconditional — always debits
    regardless of analysis outcome.
    """

def credit_wiring(self, turns: int, rate: float) -> None:
    """Credit turns back after successful wiring analysis.

    Uses int(turns * reimbursement_rate) which floors to 0 when
    turns=1 and rate=0.8. Tests must assert wiring_gate_credits == 0
    for single-turn debits at the default reimbursement rate.

    IMPORTANT: int(turns * reimbursement_rate) floors to 0 when
    turns=1 and rate=0.8 (since int(0.8) = 0). This means single-turn
    wiring debits receive zero credit reimbursement. This is by design —
    the reimbursement_rate is effectively inert for single-turn debits
    unless set to >= 1.0.
    """

def can_run_wiring_gate(self, cost: int) -> bool:
    """Check if budget allows a wiring gate run of the given cost.

    Returns True if remaining budget >= cost. Used as a pre-check
    before debit_wiring() to avoid over-budget execution.
    """
```

### 4.2 Analysis Functions

#### 4.2.1 Unwired Callable Analysis

**Purpose**: Detect constructor parameters typed `Optional[Callable]` (or `Callable | None`)
with default `None` that are never explicitly provided at any call site in the codebase.

**Algorithm**:

```
1. AST-parse all Python files in target directory
2. For each class definition:
   a. Find __init__ method
   b. Extract parameters where annotation references Callable with a None default:

      Normalize annotation to string:
        annotation_str = ast.unparse(param.annotation) if param.annotation else ""

      Match using word-boundary pattern (prevents false positives on names
      containing "Callable" as a substring, e.g., NotCallableType):
        callable_pattern = re.compile(
            r'\b(typing\.)?Callable\b|'
            r'\bcollections\.abc\.Callable\b'
        )

      Record as injectable if:
        callable_pattern.search(annotation_str)
        AND isinstance(param.default, ast.Constant)
        AND param.default.value is None

      Note: ast.unparse() handles all annotation forms correctly, including
      ast.Subscript nodes (Optional[Callable[...]]) and manually-quoted
      forward references ("Callable[...]") which render as quoted literals
      still matchable by the pattern above.
      Note: from __future__ import annotations does NOT change ast.parse()
      output — annotations remain AST nodes in all Python versions.
      No runtime annotation evaluation is required or appropriate here.

   c. Record as injectable: (class_name, param_name, file_path, line)
3. For each injectable found:
   a. Search all Python files for call sites constructing that class
   b. Check if any call site provides the parameter by keyword
   c. If zero call sites provide it -> WiringFinding(unwired_callable)
```

**Known Limitation — Import Aliases and Re-exports (tracked for v1.1)**

The call-site search matches class names as they appear in the defining module.
Classes re-exported through `__init__.py` and consumed via aliases
(e.g., `from package import ClassName` where the package `__init__.py`
re-exports it) will not be resolved. This produces false positives for
re-exported classes.

Expected FPR contribution in codebases using package-level re-exports:
30–70% of unwired-callable findings in shadow mode may be re-export false
positives. Phase 2 thresholds must be calibrated against Phase 1 data with
this in mind (see Section 8 threshold calibration guidance).

Planned fix (v1.1): pre-pass alias map construction via `ast.Import` /
`ast.ImportFrom` traversal with `__init__.py` chain resolution (max 3 hops).

**Pattern matched** (from forensic report):
```python
# This triggers detection:
class PortifyExecutor:
    def __init__(self, ..., step_runner: Optional[Callable] = None):
        ...

# This call site does NOT provide step_runner:
executor = PortifyExecutor(steps=steps, workdir=workdir, ...)
# -> Finding: unwired_callable, PortifyExecutor.step_runner
```

**Whitelist mechanism**: A `wiring_whitelist.yaml` file can list intentionally-optional
callables (event hooks, logging callbacks) excluded from analysis.

**Schema**: each entry must conform to:

```yaml
# wiring_whitelist.yaml
unwired_callables:
  - symbol: "module.path.ClassName.param_name"  # required; dotted path
    reason: "string"                             # required; non-empty
orphan_modules:
  - symbol: "module.path.function_name"          # required; dotted path
    reason: "string"                             # required; non-empty
unwired_registries:
  - symbol: "registry.key.name"                  # required; dotted path
    reason: "string"                             # required; non-empty
```

The legacy `class` + `param` split form is accepted as equivalent to
`symbol: "ClassName.param"` and normalized on load.

All three finding types (`unwired_callables`, `orphan_modules`, `unwired_registries`)
share the same entry schema (`symbol` + `reason`). The `whitelist_entries_applied`
frontmatter field (§4.3.2) counts matched entries across all three types.

**Validation behavior (Phase 1 — shadow mode)**:
- `load_wiring_config()` MUST validate each entry against the schema above.
- Entries missing `symbol` or `reason`, or with an empty `reason`, are MALFORMED.
  Malformed entries MUST be skipped with a WARNING:
    `WARNING: wiring_whitelist.yaml entry [N] malformed (missing: <field>), skipping.`
- `load_wiring_config()` MUST NOT raise `WiringConfigError` for malformed entries
  during Phase 1 shadow mode — the gate must continue running to preserve
  observation data.

**Phase 2 note**: `load_wiring_config()` will be updated to raise `WiringConfigError`
on any malformed entry before Phase 2 activation. Resolve all whitelist warnings
before Phase 2 cutover.

#### 4.2.2 Orphan Module Analysis

**Purpose**: Detect Python files in conventionally-structured directories (`steps/`,
`handlers/`, `validators/`) whose exported functions are never imported by any
consumer module.

**Algorithm**:

```
1. Identify "provider directories" by convention:
   - directories named steps/, handlers/, validators/, checks/
   Note: Heuristic detection (3+ files with common prefix) deferred to v1.1
   pending algorithm specification and test case definition.
2. For each Python file in a provider directory:
   a. AST-parse to extract top-level function definitions (excluding _private)
   b. For each exported function:
      - Search all Python files OUTSIDE the provider directory for:
        * import statements referencing the function
        * from ... import statements referencing the function
   c. If zero importers found -> WiringFinding(orphan_module)
```

**Pattern matched** (from forensic report):
```python
# src/superclaude/cli/cli_portify/steps/validate_config.py
def run_validate_config():  # exported, but never imported by executor.py
    ...

# executor.py never contains:
# from .steps.validate_config import run_validate_config
# -> Finding: orphan_module, steps/validate_config.py::run_validate_config
```

**Exclusions**: `__init__.py`, files matching `conftest.py`, `test_*.py`.

#### 4.2.3 Unwired Registry Analysis

**Purpose**: Detect dictionary constants with naming patterns indicating dispatch
registries (`REGISTRY`, `DISPATCH`, `RUNNERS`, `HANDLERS`, `ROUTER`) whose values
reference functions that cannot be resolved via import.

**Algorithm**:

```
1. AST-parse all Python files
2. For each module-level assignment where:
   a. Target name matches REGISTRY_PATTERNS regex
   b. Value is a Dict literal
3. For each dict entry:
   a. Extract value (expected: function reference or string path)
   b. If value is a Name node: verify the name is importable in scope
   c. If value is a string: verify it resolves to a module.function path
4. Entries with unresolvable values -> WiringFinding(unwired_registry)
```

**Registry patterns** (configurable):
```python
DEFAULT_REGISTRY_PATTERNS = re.compile(
    r"^(STEP_REGISTRY|STEP_DISPATCH|PROGRAMMATIC_RUNNERS|"
    r"\w*_REGISTRY|\w*_DISPATCH|\w*_HANDLERS|\w*_ROUTER)$"
)
```

### 4.3 Report Format

The wiring analysis emits a Markdown file with YAML frontmatter, conforming to
the `GateCriteria` validation pattern used by all existing gates.

```markdown
---
gate: wiring-verification
target_dir: src/superclaude/cli/cli_portify
files_analyzed: 14
unwired_count: 1
orphan_count: 2
registry_count: 0
total_findings: 3
analysis_complete: true
enforcement_scope: task
resolved_gate_mode: shadow
---

# Wiring Verification Report

## Unwired Callables (1)

### WF-001: PortifyExecutor.step_runner

- **File**: src/superclaude/cli/cli_portify/executor.py
- **Line**: 393
- **Type**: unwired_callable
- **Severity**: critical
- **Detail**: Constructor parameter `step_runner: Optional[Callable] = None` is never
  provided at any of 1 call sites. Call sites: `executor.py:1395 (run_portify)`.

## Orphan Modules (2)

### WF-002: steps/validate_config.py::run_validate_config

- **File**: src/superclaude/cli/cli_portify/steps/validate_config.py
- **Line**: 12
- **Type**: orphan_module
- **Severity**: critical
- **Detail**: Exported function `run_validate_config` has 0 importers across 14 files.

### WF-003: steps/discover_components.py::run_discover_components

- **File**: src/superclaude/cli/cli_portify/steps/discover_components.py
- **Line**: 8
- **Type**: orphan_module
- **Severity**: critical
- **Detail**: Exported function `run_discover_components` has 0 importers across 14 files.

## Summary

3 findings (1 unwired callable, 2 orphan modules, 0 unwired registries).
Gate status: FAIL (enforcement: shadow -- logged only).
```

**4.3.1 Frontmatter Serialization Requirements**

The `emit_report` function (T05) MUST serialize all string-valued frontmatter
fields using `yaml.safe_dump()` rather than f-string or `str.format()` interpolation.
This applies to: `target_dir`, `symbol_name`, `detail`.

Boolean and integer fields that are gate-evaluated (`analysis_complete`,
`unwired_count`, `orphan_count`, `registry_count`, `total_findings`) are
serialized as Python literals and are exempt from this requirement.

**Rationale**: f-string interpolation of filesystem paths and symbol names into
YAML produces malformed output when values contain YAML-special characters (`:`,
`|`, `{`, `}`, `[`, `]`). While these cannot appear in Python identifiers, they
can appear in `target_dir` values. Malformed frontmatter causes report parse
errors; defensively handled, these produce gate failures rather than bypasses,
but the failure mode is confusing and avoidable.

**Implementation pattern**:
```python
import yaml
metadata_fields = {
    "target_dir": str(target_dir),
    "symbol_name": finding.symbol_name,
    "detail": finding.detail,
}
frontmatter_str = yaml.safe_dump(metadata_fields, default_flow_style=False)
```

**4.3.2 Whitelist Audit Visibility in Frontmatter**

`emit_report()` MUST include the following field in YAML frontmatter:

```yaml
whitelist_entries_applied: 0   # integer; count of entries that suppressed ≥1 finding
```

This field is required regardless of whether a whitelist file is configured.
If no whitelist is configured or no entries matched, emit `whitelist_entries_applied: 0`.

**Rationale**: reviewers must be able to detect whitelist-based suppression from
the gate report alone, without diffing `wiring_whitelist.yaml` across commits.

### 4.4 Gate Definition

```python
WIRING_GATE = GateCriteria(
    required_frontmatter_fields=[
        "gate",
        "target_dir",
        "files_analyzed",
        "files_skipped",
        "unwired_count",
        "orphan_count",
        "registry_count",
        "total_findings",
        "analysis_complete",
        "enforcement_scope",
        "resolved_gate_mode",
        "whitelist_entries_applied",
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[
        SemanticCheck(
            name="analysis_complete_true",
            check_fn=_analysis_complete_true,
            failure_message="analysis_complete must be true",
        ),
        SemanticCheck(
            name="zero_unwired_callables",
            check_fn=_zero_unwired_callables,
            failure_message="unwired_count must be 0; all injectable callables must be provided",
        ),
        SemanticCheck(
            name="zero_orphan_modules",
            check_fn=_zero_orphan_modules,
            failure_message="orphan_count must be 0; all exported functions must have importers",
        ),
        SemanticCheck(
            name="zero_unwired_registries",
            check_fn=_zero_unwired_registries,
            failure_message="registry_count must be 0; all registry entries must resolve",
        ),
        SemanticCheck(
            name="total_findings_consistent",
            check_fn=_total_findings_consistent,
            failure_message="total_findings must equal unwired_count + orphan_count + registry_count",
        ),
    ],
)
```

The semantic check functions follow the established `(content: str) -> bool` pattern
used by `_high_severity_count_zero`, `_total_analyzed_consistent`, etc. in `roadmap/gates.py`.

### 4.5 Sprint Integration

The wiring gate hooks into the sprint runner at the post-task classification point.

**Hook point**: `sprint/executor.py`, after `_classify_from_result_file()` returns,
before the task status is finalized.

**TurnLedger-aware budget flow** (replaces `wiring_gate_mode` string-switch):

```python
# In execute_phase_tasks() or _run_task_subprocess(), after classification:
# Hook signature: run_post_task_wiring_hook(task, config, ledger=None) -> WiringReport

if not config.wiring_gate_enabled:
    # Skip wiring analysis entirely; no report emitted
    return

# Budget debit (before analysis)
if ledger is not None:
    ledger.debit_wiring(WIRING_ANALYSIS_TURNS)

# Run analysis
wiring_report_path = work_dir / f"{task_id}-wiring-report.md"
report = run_wiring_analysis(target_dir=config.source_dir)

# Resolve enforcement mode via scope-based resolution (replaces string switches)
mode = resolve_gate_mode(config.wiring_gate_scope, config.wiring_gate_grace_period)

emit_report(report, wiring_report_path,
            enforcement_scope=config.wiring_gate_scope,
            resolved_gate_mode=mode)

if report.passed:
    # Credit budget on pass (see Section 4.1.1 for floor-to-zero behavior)
    if ledger is not None:
        ledger.credit_wiring(WIRING_ANALYSIS_TURNS, config.reimbursement_rate)
    return report

# Failure handling based on resolved mode
if mode == GateMode.BLOCKING:
    # NOTE (IE-5): This is the first production instantiation of SprintGatePolicy
    # in the wiring gate path. SprintGatePolicy's constructor requirements and
    # failure modes must be validated against trailing_gate.py's existing usage.
    policy = SprintGatePolicy(config)

    if ledger is not None and ledger.can_run_wiring_gate(REMEDIATION_COST):
        # Remediation path (see Section 4.5.3 for full spec)
        failure_msg = _format_wiring_failure(report)
        remediation_step = policy.build_remediation_step(
            gate_name="wiring-verification",
            failure_message=failure_msg,
            can_remediate=lambda: ledger.can_run_wiring_gate(REMEDIATION_COST),
            debit=lambda cost: ledger.debit_wiring(cost),
        )
        # Execute remediation, then recheck (Section 4.5.3)
    else:
        # No ledger or budget exhausted — direct FAIL (Section 4.5.2)
        logger.error(f"Wiring gate FAIL: {report.total_findings} findings (no remediation)")

elif mode == GateMode.SHADOW:
    # Shadow mode: log and defer (no task status impact)
    logger.info(f"[shadow] Wiring gate: {report.total_findings} findings")
    # DeferredRemediationLog adapter (Gamma IE-4, Section 4.5.3)
    deferred_result = TrailingGateResult(
        step_id=f"{task.task_id}_wiring",
        gate_name="wiring-verification",
        passed=False,
        findings=report.total_findings,
    )
    DeferredRemediationLog.append(deferred_result)

elif mode == GateMode.SOFT:
    # Soft mode: warn in TUI but do not block
    if not report.passed:
        tui.warn(f"Wiring gate: {report.total_findings} findings")

return report
```

**Configuration**: Three fields on `SprintConfig` (replaces `wiring_gate_mode`, see Section 6.2):

```python
wiring_gate_enabled: bool = True
wiring_gate_scope: GateScope = GateScope.TASK
wiring_gate_grace_period: int = 0
```

#### 4.5.1 TurnLedger Budget Flow

**Budget flow diagram** (complete debit-before-analysis, credit-on-pass path):

```
+-------------------+
| Task completes    |
| (sprint runner)   |
+--------+----------+
         |
         v
+--------+----------+
| if ledger is not  |
| None:             |
|   ledger.debit_   |
|   wiring(WIRING_  |
|   ANALYSIS_TURNS) |
+--------+----------+
         |
         v
+--------+----------+
| run_wiring_       |
| analysis()        |
+--------+----------+
         |
         v
+--------+----------+
| mode = resolve_   |
| gate_mode(scope,  |
| grace_period)     |
+--------+----------+
         |
    +----+----+
    |         |
    v         v
  PASS      FAIL
    |         |
    v         +-------+-------+
+---+-------+ |               |
| if ledger | v               v
| is not    | BLOCKING        SHADOW/SOFT
| None:     | |               |
|  credit_  | v               v
|  wiring(  | attempt_        DeferredRemediation
|  turns,   | remediation()   Log.append()
|  rate)    | |               (synthetic
+---+-------+ v               TrailingGateResult)
    |         budget debit
    v         for retry
  DONE        |
              v
            _recheck_wiring()
```

**Budget accounting table**:

| Outcome | Debit | Credit | Net cost |
|---------|-------|--------|----------|
| Pass (single-turn, rate=0.8) | `WIRING_ANALYSIS_TURNS` (1) | `int(1 * 0.8)` = **0** | 1 turn |
| Pass (multi-turn, rate=0.8) | N turns | `int(N * 0.8)` | ~0.2N turns |
| Fail (BLOCKING, remediation succeeds) | N + remediation turns | credit on recheck pass | variable |
| Fail (BLOCKING, remediation fails) | N + remediation turns | 0 | N + remediation |
| Fail (shadow/soft) | N turns | 0 | N turns |
| Ledger is None | 0 (skipped) | 0 (skipped) | 0 (no tracking) |

**Hook signature**:

```python
def run_post_task_wiring_hook(
    task: Task,
    config: SprintConfig,
    ledger: TurnLedger | None = None,
) -> WiringReport:
    """Post-task wiring analysis with optional budget tracking.

    All budget operations gated by `if ledger is not None`.
    """
```

**BC-5 cross-release ordering note**: The wiring gate budget flow applies per-task within a
release. Cross-release ordering (e.g., v3.1 → v3.2 migration) preserves existing TurnLedger
state — `wiring_gate_cost` and `wiring_gate_credits` fields have zero defaults that accumulate
from first use. If v3.1 lands first and establishes `reimbursement_rate` activation, v3.2
becomes the second consumer. If v3.2 lands first, the `ledger is None` path provides
self-sufficient operation.

#### 4.5.2 Backward Compatibility — TurnLedger is None

**Null-ledger behavioral matrix**: When `ledger is None`, wiring analysis runs without budget
tracking. This preserves phase-level execution (pre-TurnLedger sprints).

| Operation | `ledger is not None` | `ledger is None` |
|-----------|----------------------|-------------------|
| Budget debit | `ledger.debit_wiring(turns)` | Skip (no tracking) |
| Budget credit | `ledger.credit_wiring(turns, rate)` | Skip (no tracking) |
| Analysis | `run_wiring_analysis()` — runs normally | `run_wiring_analysis()` — runs normally |
| Mode resolution | `resolve_gate_mode(scope, grace_period)` | `resolve_gate_mode(scope, grace_period)` — same |
| Blocking failure | `attempt_remediation()` with budget tracking | Direct FAIL (no retry without budget tracking) |
| Shadow failure | `DeferredRemediationLog.append()` | `DeferredRemediationLog.append()` — same |

**Key difference**: When `ledger is None` and a BLOCKING failure occurs, the gate issues a
direct FAIL with no remediation attempt. Remediation requires budget tracking to debit the
retry cost. Without a ledger, the system cannot account for remediation turns and must fail
immediately.

#### 4.5.3 Remediation Path on Wiring Gate Failure

**1. `attempt_remediation()` integration (BLOCKING mode)**:

Uses a callable-based interface to avoid direct TurnLedger import in `trailing_gate.py`:

```python
# Callable-based interface for remediation
can_remediate: Callable[[], bool]  # checks budget availability
debit: Callable[[int], None]       # debits remediation cost

# In executor hook:
if can_remediate():
    debit(REMEDIATION_COST)
    # ... run remediation subprocess
```

**2. `_format_wiring_failure()` helper spec**:

```python
def _format_wiring_failure(report: WiringReport) -> str:
    """Format wiring findings into human-readable failure message for remediation step.

    Returns a structured string listing each finding with file, line, and detail.
    Used as input to the remediation subprocess.
    """
```

**3. `_recheck_wiring()` helper spec**:

```python
def _recheck_wiring(target_dir: Path, config: WiringConfig) -> WiringReport:
    """Re-run wiring analysis after remediation attempt.

    Returns a fresh WiringReport. If the recheck passes, the remediation
    is considered successful and credits are issued.
    """
```

**4. `DeferredRemediationLog` adapter** (Gamma IE-4):

Shadow mode deferred logging requires constructing a synthetic `TrailingGateResult` from
wiring findings, since `DeferredRemediationLog.append()` takes `TrailingGateResult`, not
`WiringReport`:

```python
# Adapter: WiringReport -> TrailingGateResult
deferred_result = TrailingGateResult(
    step_id=f"{task.task_id}_wiring",
    gate_name="wiring-verification",
    passed=False,
    findings=report.total_findings,
)
DeferredRemediationLog.append(deferred_result)
```

**5. Budget flow during remediation**:

- Additional debit of `REMEDIATION_COST` turns before remediation attempt
- Credit issued only if `_recheck_wiring()` passes
- Net cost on successful remediation: `WIRING_ANALYSIS_TURNS + REMEDIATION_COST - credit`
- Net cost on failed remediation: `WIRING_ANALYSIS_TURNS + REMEDIATION_COST` (no credit)

**6. Edge cases**:

- **Budget exhaustion mid-remediation**: `can_remediate()` returns False → skip remediation,
  issue direct FAIL. Log `WARN: budget-exhausted-skipping-remediation`.
- **Subprocess failure**: Remediation subprocess exits non-zero → treat as failed remediation,
  no credit, log error with subprocess exit code.
- **Gate re-evaluation**: After remediation, full `_recheck_wiring()` runs. If new findings
  appear (remediation introduced new issues), the recheck FAIL is final — no recursive
  remediation attempts.

#### 4.5.4 KPI Report Extensions

**New `GateKPIReport` fields** (6 wiring-specific fields):

```python
# On GateKPIReport (sprint/kpi.py)
wiring_total_debits: int       # Sum of all wiring gate debits
wiring_total_credits: int      # Sum of all wiring gate credits
wiring_net_cost: int           # wiring_total_debits - wiring_total_credits
wiring_analyses_run: int       # Count of wiring analyses executed
wiring_findings_total: int     # Sum of total_findings across all analyses
wiring_remediations_attempted: int  # Count of remediation attempts
```

**`build_kpi_report()` signature update**:

```python
def build_kpi_report(
    ...,
    wiring_ledger: TurnLedger | None = None,
) -> GateKPIReport:
    """Build KPI report with optional wiring metrics from TurnLedger."""
```

**New file entry**: `sprint/kpi.py` MODIFY +15-20 LOC.

**Note**: Generalization to generic `gate_family_counts: dict[str, int]` is deferred to v3.3
(per brainstorm.md Proposal B).

### 4.6 Companion: Deviation Count Reconciliation

This release also includes the Deviation Count Reconciliation Gate (Proposal 4 from
the ranking), as a zero-cost companion that strengthens existing Link 1 gates.

**Implementation**: Single function `_deviation_counts_reconciled(content: str) -> bool`
added to `SPEC_FIDELITY_GATE.semantic_checks` in `roadmap/gates.py`.

**Algorithm**:
1. Parse frontmatter for `high_severity_count`, `medium_severity_count`, `low_severity_count`
2. Regex-scan body for `DEV-\d{3}` entries, extract severity from `**Severity**: X` lines
3. Compare body counts to frontmatter counts
4. Fail on any mismatch

**Estimated LOC**: 35-50 lines.

---

## 5. File Manifest

| File | Action | Estimated LOC | Purpose |
|------|--------|---------------|---------|
| `src/superclaude/cli/audit/wiring_gate.py` | CREATE | 250-300 | Core analysis engine, report emitter, gate definition |
| `src/superclaude/cli/audit/wiring_config.py` | CREATE | 40-60 | Configuration dataclass, patterns, whitelist loader |
| `src/superclaude/cli/sprint/models.py` | MODIFY | +30-35 | TurnLedger extensions (3 fields, 3 methods) + SprintConfig scope-based fields |
| `src/superclaude/cli/sprint/executor.py` | MODIFY | +50-70 | TurnLedger-aware wiring hook, resolve_gate_mode(), remediation path |
| `src/superclaude/cli/sprint/kpi.py` | MODIFY | +15-20 | GateKPIReport wiring extensions |
| `src/superclaude/cli/roadmap/gates.py` | MODIFY | +40 | `_deviation_counts_reconciled` semantic check |
| `tests/audit/test_wiring_gate.py` | CREATE | 200-250 | Unit tests for all analysis functions |
| `tests/audit/test_deviation_recon.py` | CREATE | 60-80 | Unit tests for deviation count reconciliation |
| `tests/audit/fixtures/` | CREATE | 50-80 | Python fixtures for wiring analysis tests |
| `tests/pipeline/test_full_flow.py` | MODIFY | +80-100 | Budget integration test scenarios 5-8 |

**Total new production code**: ~410-500 lines
**Total new test code**: ~400-520 lines

---

## 6. Interface Contracts

### 6.1 Public API

```python
# Entry point for wiring analysis
def run_wiring_analysis(
    target_dir: Path,
    config: WiringConfig | None = None,
) -> WiringReport:
    """Analyze a directory for wiring verification issues.

    Args:
        target_dir: Root directory to analyze (e.g., src/superclaude/cli/cli_portify/).
        config: Optional configuration overriding defaults.

    Returns:
        WiringReport with all findings.
    """

# Report emitter (Markdown + YAML frontmatter)
def emit_report(
    report: WiringReport,
    output_path: Path,
    enforcement_scope: GateScope = GateScope.TASK,
    resolved_gate_mode: GateMode = GateMode.SHADOW,
) -> None:
    """Write wiring report as Markdown with YAML frontmatter.

    The output conforms to the GateCriteria validation pattern:
    frontmatter fields match WIRING_GATE.required_frontmatter_fields.
    """

# SemanticCheck-compatible function
def check_wiring_report(content: str) -> bool:
    """Validate a wiring report passes all criteria.

    Used as check_fn in SemanticCheck instances on WIRING_GATE.
    """
```

### 6.2 Configuration Contract

```python
@dataclass
class WiringConfig:
    """Configuration for wiring verification analysis."""

    # Patterns identifying dispatch registries
    registry_patterns: re.Pattern = DEFAULT_REGISTRY_PATTERNS

    # Directories treated as "provider" directories for orphan analysis.
    # IMPORTANT: must be set to match the target repository's actual provider
    # directory conventions before shadow mode activation.
    # The default value {"steps", "handlers", "validators", "checks"} reflects
    # common framework conventions and will produce zero orphan findings (a false
    # clean result) in codebases using different naming (e.g., "audit/",
    # "execution/", "pm_agent/"). This field is not optional for production deployments.
    # See Section 8 pre-activation checklist.
    provider_dir_names: frozenset[str] = frozenset({
        "steps", "handlers", "validators", "checks",
    })

    # Path to wiring_whitelist.yaml. Entries suppress gate findings for matched symbols.
    # See Section 4.2.1 for entry schema and validation behavior.
    # Count of applied entries is reported in gate output frontmatter (Section 4.3.2).
    whitelist_path: Path | None = None

    # File exclusion patterns
    exclude_patterns: list[str] = field(default_factory=lambda: [
        "test_*.py", "conftest.py", "__init__.py",
    ])
```

**SprintConfig wiring gate fields** (replaces `wiring_gate_mode`):

```python
# On SprintConfig (sprint/models.py)
SHADOW_GRACE_INFINITE: int = 999_999  # Named constant for shadow phase grace period

wiring_gate_enabled: bool = True
wiring_gate_scope: GateScope = GateScope.TASK
wiring_gate_grace_period: int = 0
```

**Old-to-new mapping** (`wiring_gate_mode` → scope-based fields):

| Old `wiring_gate_mode` | `wiring_gate_enabled` | `wiring_gate_scope` | `wiring_gate_grace_period` |
|-------------------------|-----------------------|----------------------|----------------------------|
| `"off"` | `False` | (ignored) | (ignored) |
| `"shadow"` | `True` | `GateScope.TASK` | `SHADOW_GRACE_INFINITE` |
| `"soft"` | `True` | `GateScope.TASK` | `0` |
| `"full"` | `True` | `GateScope.TASK` | `0` |

**Migration note** (`__post_init__`): Defensive only — `wiring_gate_mode` is v3.2-new code,
not yet shipped. Only `run_post_task_wiring_hook()` and `run_wiring_safeguard_checks()` read
this field. Emit deprecation warning if `wiring_gate_mode` is set. Remove after 1 release.

### 6.3 Gate Contract

The `WIRING_GATE` constant conforms to `GateCriteria` and is evaluated by the
existing `gate_passed()` function in `pipeline/gates.py` without modification.

**Frontmatter contract** (must appear in every report):

| Field | Type | Constraint |
|-------|------|-----------|
| `gate` | string | Must be `"wiring-verification"` |
| `target_dir` | string | Non-empty |
| `files_analyzed` | int | >= 0 |
| `files_skipped` | int | >= 0; count of Python files that failed AST parsing |
| `unwired_count` | int | Must be 0 for gate pass |
| `orphan_count` | int | Must be 0 for gate pass |
| `registry_count` | int | Must be 0 for gate pass |
| `total_findings` | int | Must equal sum of above three |
| `analysis_complete` | bool | Must be true |
| `enforcement_scope` | string | GateScope value; derived from `resolve_gate_mode()` at report generation |
| `resolved_gate_mode` | string | GateMode value; derived from `resolve_gate_mode()` output |
| `whitelist_entries_applied` | int | >= 0; count of whitelist entries that suppressed findings |

---

## 7. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| R1: False positives from intentional `Optional[Callable]` hooks | High | Medium | Whitelist mechanism (`wiring_whitelist.yaml`) |
| R2: AST parsing fails on complex Python patterns | Medium | Low | Graceful degradation: log warning, skip file, do not fail gate |
| R3: Shadow mode collects insufficient data | Low | Medium | Shadow mode runs for minimum 2 releases before enforcement decision |
| R4: Performance impact on sprint loop | Low | Medium | Wiring analysis is AST-only, no subprocess; expected < 2s for 50-file packages |
| R5: Naming convention heuristics miss new registry patterns | Medium | Low | Configurable `registry_patterns` regex; log when no registries found |
| R6: `provider_dir_names` mismatch with actual codebase conventions | High | High | Pre-activation validation checklist (Section 8 Phase 1); zero-findings sanity check required on first run |
| R7: `int(turns * reimbursement_rate)` floors to zero at `WIRING_ANALYSIS_TURNS=1` | High | Medium | Tests explicitly assert `wiring_gate_credits == 0` (see Section 4.1.1 floor behavior documentation); `reimbursement_rate` effectively inert for single-turn debits unless set to 1.0 |
| R8: SprintConfig field rename (`wiring_gate_mode` → 3 fields) breaks development branch configs | Medium | Low | `__post_init__` migration shim with deprecation warning; v3.2-new code only (no production consumers per Section 6.2) |

---

## 8. Rollout Plan

### Phase 1: Shadow (this release)

**SprintConfig profile**:
```python
wiring_gate_enabled = True
wiring_gate_scope = GateScope.TASK
wiring_gate_grace_period = SHADOW_GRACE_INFINITE  # 999_999 (Section 6.2)
```

**Pre-activation checklist (blocking — shadow mode must not start until both pass):**

1. **Provider directory validation**: Confirm that at least one directory matching
   `provider_dir_names` exists in the target repository and contains at least one
   Python file. If zero matches are found, update `provider_dir_names` in
   `WiringConfig` before proceeding. A shadow run against a misconfigured
   `provider_dir_names` produces a silent null result indistinguishable from a
   genuinely clean codebase and corrupts baseline data.

2. **Zero-findings sanity check**: If the first shadow run produces zero findings
   across ALL analyzers on a repository with >50 Python files, treat this as a
   configuration error requiring investigation, not a passing result.
   Log `WARN: zero-findings-on-first-run` and halt baseline collection until
   the configuration is verified.

- Wiring analysis runs after every task in sprint execution
- Results logged to `.sprint-state/wiring/` directory
- No impact on task status or pipeline flow
- Collect baseline: false positive rate, finding distribution, analysis time

### Phase 2: Soft (release +1, pending shadow data review)

**SprintConfig profile** (transition from Phase 1: change `wiring_gate_grace_period`):
```python
wiring_gate_enabled = True
wiring_gate_scope = GateScope.TASK
wiring_gate_grace_period = 0
```

- Findings surfaced as warnings in sprint TUI
- Findings recorded in `DeferredRemediationLog`
- Block only at release scope (per `resolve_gate_mode()` which returns BLOCKING for release)
- Override available via `--skip-wiring-gate` flag

**Threshold calibration for known FPR sources**:

When setting Phase 2 activation thresholds from Phase 1 baseline data,
explicitly account for the following known false-positive sources:

| Source | Expected FPR contribution | v1.0 mitigation | Planned fix |
|---|---|---|---|
| Re-exported classes (import aliases) | 30–70% of unwired-callable findings | Raise Phase 2 unwired-callable threshold; document noise floor | v1.1 alias pre-pass |
| `provider_dir_names` misconfiguration | 100% of orphan-module findings (silent) | Pre-activation validation checklist (Section 8 Phase 1) | N/A — config |

**Decision rule**: Phase 2 MUST NOT be activated if Phase 1 unwired-callable
FPR cannot be separated from the re-export noise floor. Document the estimated
noise floor in the Phase 1 report. Set Phase 2 thresholds at
`measured_FPR + 2σ` above the noise floor estimate, not above zero.

### Phase 3: Full (release +2, pending soft data review)

**SprintConfig profile** (transition from Phase 2: change `wiring_gate_scope`):
```python
wiring_gate_enabled = True
wiring_gate_scope = GateScope.RELEASE
wiring_gate_grace_period = 0
```

- Findings block task completion at STRICT tier
- Remediation via `SprintGatePolicy.build_remediation_step()`
- No override without explicit whitelist entry

### Rollout Decision Criteria

| Metric | Shadow → Soft Threshold | Soft → Full Threshold | Debit on analysis | Credit on pass |
|--------|--------------------------|------------------------|-------------------|----------------|
| False positive rate | < 15% of findings are whitelisted | < 5% | Yes (WIRING_ANALYSIS_TURNS) | Yes (if pass) |
| True positive rate | > 50% of findings are genuine bugs | > 80% | Yes | No (fail path) |
| Analysis time p95 | < 5 seconds | < 3 seconds | Yes | Conditional |
| Whitelist stability | Whitelist unchanged for 2+ sprints | Whitelist unchanged for 5+ sprints | Yes | Conditional |

### Rollout Transition Checklist

- [ ] Verify Phase N baseline data meets threshold criteria
- [ ] Update `wiring_gate_scope` and/or `wiring_gate_grace_period` in SprintConfig
- [ ] Confirm all whitelisted entries have valid `reason` fields
- [ ] Run single-sprint dry run with new config profile
- [ ] Review budget impact (debit/credit totals from GateKPIReport)
- [ ] Announce transition to team; document in release notes

**BC-5 cross-release ordering**: Phase transitions across releases preserve TurnLedger state.
When upgrading from v3.1 → v3.2, existing `wiring_gate_cost` and `wiring_gate_credits` fields
have zero defaults and accumulate from first use. Config field compatibility is maintained
via `__post_init__` migration (Section 6.2).

### Rollout Framework Integration

This rollout plan SHOULD adopt the Unified Audit Gating rollout infrastructure (SS7.1/SS7.2 profiles, override governance, rollback triggers) rather than defining independent thresholds. The thresholds in this section serve as initial values to be configured within that framework.

### Implementation Coordination

When modifying `roadmap/gates.py`, coordinate with:
- Anti-Instincts (`ANTI_INSTINCT_GATE` addition)
- Unified Audit Gating (D-03/D-04 `SPEC_FIDELITY_GATE` extensions)

Preferred approach: single coordinated PR or sequenced PRs with explicit rebase points to avoid merge conflicts.

---

## 9. Testing Strategy

### 9.1 Coverage Requirements

The test suite shall validate the wiring analysis gate across two layers.

#### Unit Tests (minimum 14 tests, across 4 analyzer functions)

**analyze_unwired_callables** (minimum 4 tests):
- Positive: detects a callable parameter with `Optional[Callable] = None` that
  has zero call sites providing it — produces 1 `WiringFinding(unwired_callable)`
- Negative: same class, call site provides the parameter by keyword —
  produces 0 findings
- Whitelist: parameter matches a whitelist entry — produces 0 findings
- Parse error: source file with a Python syntax error — gate does not crash;
  logs a warning; `analysis_complete` field reflects degraded state
- **Out of scope** (dynamic dispatch exclusion, Section 2): alias-based
  injection and `**kwargs`-forwarded injection do not require test cases

**analyze_orphan_modules** (minimum 5 tests):
- Positive: function in a provider directory with zero importers —
  produces 1 `WiringFinding(orphan_module)`
- Negative (direct import): same function, explicitly imported by consumer —
  produces 0 findings
- Negative (`__init__.py` re-export): function re-exported via package
  `__init__.py` and consumed transitively — produces 0 findings
- Private function (`_name` prefix): excluded from analysis — produces 0 findings
- `conftest.py`: pytest infrastructure files excluded — produces 0 findings

**analyze_unwired_registries** (minimum 2 tests):
- Positive: registry entry whose value symbol cannot be resolved —
  produces 1 `WiringFinding(unwired_registry)`
- Negative: registry entry whose value symbol resolves correctly —
  produces 0 findings

**TurnLedger model tests** (in `test_models.py`):
- `test_debit_wiring`: verify `wiring_gate_cost` increments correctly
- `test_credit_wiring`: verify `wiring_gate_credits` uses `int(turns * rate)` floor behavior
- `test_can_run_wiring_gate`: verify budget check returns correct boolean

**emit_report / gate** (minimum 3 tests):
- Findings present → `gate_passed()` returns `(False, reason)`; report
  frontmatter has non-zero count fields
- No findings → `gate_passed()` returns `(True, None)`; report frontmatter
  has all count fields == 0
- YAML-safe serialization: a report emitted when `target_dir` contains a
  YAML-special character (e.g., colon) and `symbol_name` contains a block
  indicator character must parse without `yaml.YAMLError`; `gate_passed()`
  must return the expected result based on finding counts

### 9.2 Integration Tests (minimum 2 tests)

**SC-010: cli-portify fixture integration**

A dedicated fixture module set shall exist under `tests/audit/fixtures/`.
The fixture must contain:
- A source file defining a class with a constructor parameter typed
  `Optional[Callable]` with a `None` default
- A second source file that instantiates that class without providing the
  callable parameter

Behavioral contract (non-negotiable): `run_wiring_analysis()` on the fixture
directory MUST produce exactly 1 `WiringFinding` of type `"unwired_callable"`
identifying the specific class and parameter. Zero findings or more than 1
finding constitutes test failure.

The fixture file structure, class names, parameter names, and module layout
are implementation decisions finalized at T06. Only the behavioral contract
above is fixed by this specification.

**SC-006: sprint shadow mode non-interference**

When the wiring gate executes in shadow mode within a sprint run, the following
must hold after gate execution regardless of gate outcome:
- Task status fields (state, assignee, priority) in the sprint manifest are
  unchanged
- No exception is propagated to the sprint runner
- A `logger.info(...)` or equivalent trace is emitted with finding count

### 9.3 Test Infrastructure

**Fixture directory**: `tests/audit/fixtures/` (existing in file manifest)
**Size budget**: 50–80 LOC total (unchanged)
**Coverage target**: ≥ 90% line coverage on `src/superclaude/cli/audit/wiring_gate.py`

All WiringFinding `finding_type` values (`"unwired_callable"`, `"orphan_module"`,
`"unwired_registry"`) must appear in at least one test assertion.
Gate exit paths (pass and fail) must each appear in at least one test assertion.

### 9.4 Budget Integration Tests

Budget integration tests in `tests/pipeline/test_full_flow.py` (+80-100 LOC).
Existing scenarios 1-4 are unchanged. New scenarios are additive.

**Scenario 5 — Wiring pass budget credit**:
Sprint task completes, wiring analysis passes. Verify `ledger.wiring_gate_credits` reflects
credit. **Critical**: assert `wiring_gate_credits == 0` (not `== 1`) due to
`int(1 * 0.8) = 0` floor behavior (Section 4.1.1). Only multi-turn analyses at rate < 1.0
produce non-zero credits.

**Scenario 6 — Wiring fail remediation (BLOCKING)**:
Wiring analysis fails in BLOCKING mode. `attempt_remediation()` called. Verify:
- Remediation step created via `SprintGatePolicy.build_remediation_step()`
- Budget debited for both analysis and remediation attempt
- `_recheck_wiring()` called after remediation

**Scenario 7 — Ledger=None backward compatibility**:
Wiring analysis runs without budget tracking when `ledger is None`. Verify:
- No exceptions raised
- Task status unaffected
- Analysis runs and report emitted normally
- No `debit_wiring()` or `credit_wiring()` calls

**Scenario 8 — Shadow deferred log**:
Wiring analysis fails in shadow mode. Verify:
- `DeferredRemediationLog.append()` called with synthetic `TrailingGateResult`
- `TrailingGateResult.step_id` equals `f"{task.task_id}_wiring"`
- `TrailingGateResult.gate_name` equals `"wiring-verification"`
- Task status unaffected (shadow mode is non-blocking)

**Updated test LOC estimate**: 400-520 lines total (previously 310-410).

---

## 10. Success Criteria

| SC | Description | Verification |
|----|-------------|-------------|
| SC-001 | Wiring gate detects `Optional[Callable] = None` never provided at call site | Unit test: `test_detect_unwired_callable_basic` |
| SC-002 | Wiring gate detects orphan modules in `steps/` directories | Unit test: `test_detect_orphan_module` |
| SC-003 | Wiring gate detects unresolvable registry entries | Unit test: `test_detect_unwired_registry` |
| SC-004 | Report conforms to `GateCriteria` validation pattern | Unit test: `test_gate_passes_clean_report` |
| SC-005 | `gate_passed()` evaluates `WIRING_GATE` without modification | Integration test: `test_cli_portify_fixture` |
| SC-006 | Shadow mode logs findings without affecting task status | Integration test in sprint context |
| SC-007 | Whitelist mechanism excludes intentional optionals and records suppression count | Unit test: whitelist positive case (per Section 9.1 — whitelist test); AND `emit_report()` frontmatter includes `whitelist_entries_applied: 1` |
| SC-008 | Deviation count reconciliation catches body/frontmatter mismatch | Unit test: `test_deviation_count_reconciliation` |
| SC-009 | Analysis completes in < 5s for packages up to 50 files | Performance benchmark |
| SC-010 | Retrospective: would catch the cli-portify executor no-op bug | Run against actual `cli_portify/` directory |
| SC-011 | `provider_dir_names` pre-activation validation emits `WARN: zero-findings-on-first-run` when zero provider dirs match | Integration: shadow run against target with no matching provider dirs emits warning and halts baseline collection |
| SC-012 | `debit_wiring`/`credit_wiring` correctly track wiring-specific costs | Unit test: `test_debit_credit_wiring_tracking` |
| SC-013 | `reimbursement_rate` consumed in production via `credit_wiring()` | Integration test: verify `credit_wiring()` calls `int(turns * reimbursement_rate)` |
| SC-014 | Wiring gate operates correctly when `ledger is None` | Integration test: `test_wiring_gate_null_ledger` |
| SC-015 | KPI report includes wiring-specific debit/credit totals | Unit test: `test_kpi_wiring_fields` |

---

## 11. Dependency Map

```
                  EXISTING (no changes)
                  =====================
                  pipeline/models.py
                    GateCriteria
                    SemanticCheck
                         |
                  pipeline/gates.py
                    gate_passed()
                         |
                  pipeline/trailing_gate.py
                    resolve_gate_mode()
                    TrailingGateRunner

                  NEW
                  ===
                  audit/wiring_gate.py -------> pipeline/models.py (import)
                    |                                   |
                    v                                   v
                  audit/wiring_config.py        pipeline/gates.py (consumed by)
                    |
                    v
                  sprint/executor.py (MODIFY) -> audit/wiring_gate.py (import)
                    |                     \
                    v                      \---> pipeline/trailing_gate.py (CONSUME)
                  sprint/models.py (MODIFY)       resolve_gate_mode()
                    TurnLedger extensions          attempt_remediation()
                    SprintConfig scope fields      GateScope, GateMode
                    |
                    v
                  sprint/kpi.py (MODIFY)
                    GateKPIReport wiring extensions
                  sprint/config.py (MODIFY)
                  roadmap/gates.py (MODIFY) -- deviation count recon only
```

**Zero changes to existing gate infrastructure.** The wiring gate is a new consumer
of the existing `GateCriteria`/`SemanticCheck`/`gate_passed()` pattern.
`pipeline/trailing_gate.py` functions (`resolve_gate_mode()`, `attempt_remediation()`,
`GateScope`, `GateMode`) are consumed but not modified.

---

## 12. Tasklist Index (for sprint execution)

| Task | Description | Deliverables | Deps |
|------|-------------|-------------|------|
| T01 | Data models (`WiringFinding`, `WiringReport`, `WiringConfig`) | `wiring_gate.py` (partial), `wiring_config.py` | -- |
| T02 | Unwired callable analysis (`analyze_unwired_callables`) | `wiring_gate.py` (partial) | T01 |
| T03 | Orphan module analysis (`analyze_orphan_modules`) | `wiring_gate.py` (partial) | T01 |
| T04 | Unwired registry analysis (`analyze_unwired_registries`) | `wiring_gate.py` (partial) | T01 |
| T05 | Report emitter and `WIRING_GATE` constant | `wiring_gate.py` (complete) | T01 |
| T06 | Unit tests for T02-T04 + test fixtures | `tests/audit/test_wiring_gate.py` (minimum 14 unit tests per Section 9.1), `tests/audit/fixtures/` (SC-010 fixture structure per Section 9.2 behavioral contract) | T02, T03, T04 |
| T07a | TurnLedger model extensions | `sprint/models.py` (MODIFY): add 3 fields + 3 methods to TurnLedger, add 3 new fields to SprintConfig | T01 |
| T07b | Sprint integration: ledger threading, `resolve_gate_mode()` replacement, remediation path | `sprint/executor.py` (MODIFY) | T05, T07a |
| T07c | KPI extensions | `sprint/kpi.py` (MODIFY): 6 new GateKPIReport fields, `build_kpi_report()` signature update | T07a |
| T08 | Deviation count reconciliation | `roadmap/gates.py` (modify) | -- |
| T09 | Unit tests for T08 | `tests/audit/test_deviation_recon.py` | T08 |
| T10 | Integration test: cli-portify fixture | `tests/audit/test_wiring_integration.py` | T06, T07b |
| T11 | Retrospective: run against actual `cli_portify/` | Validation report | T10 |
| T12 | Budget integration test scenarios 5-8 | `tests/pipeline/test_full_flow.py` (MODIFY +80-100 LOC) | T07b |

**Critical path**: T01 → T02/T03/T04/T07a (parallel) → T05 → T06 → T07b → T10 → T11

**Parallel tracks**:
- T07a parallels T02-T04 (no cross-dependency)
- T07c depends on T07a only (can parallel T07b)
- T12 depends on T07b
- T08 → T09 (independent of T01-T07)

---

## Appendix A: Forensic Report Cross-Reference

| Forensic Finding | Section | Addressed By |
|-----------------|---------|-------------|
| `step_runner=None` no-op default | Section 1, Defect 1 | T02: unwired callable analysis |
| Steps exist but never imported | Section 1, orphaned step implementations | T03: orphan module analysis |
| `STEP_REGISTRY` is metadata-only, no function refs | Section 4 | T04: unwired registry analysis |
| Link 3 does not exist | Section 5 | T05+T07: gate definition + sprint integration |
| Gate infrastructure validates documents, not code | Section 7 | Entire release scope |
| "Defined but not wired" recurring pattern | Section 9, systemic | T02+T03+T04: three detection mechanisms |
| LLM fidelity report body/frontmatter inconsistency | Section 5, Appendix B | T08: deviation count reconciliation |

## Appendix B: Naming Convention Reference

The analysis functions use the following naming conventions to identify targets:

| Convention | Pattern | Used By |
|------------|---------|---------|
| Injectable callable | `Optional[Callable]`, `Callable \| None` with `= None` | T02 |
| Provider directory | `steps/`, `handlers/`, `validators/`, `checks/` | T03 |
| Dispatch registry | `*_REGISTRY`, `*_DISPATCH`, `*_RUNNERS`, `*_HANDLERS` | T04 |
| Export function | Top-level `def` not prefixed with `_` | T03 |
| Excluded file | `__init__.py`, `conftest.py`, `test_*.py` | T03 |
