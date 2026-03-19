---
release: wiring-verification-gate-v1.0
version: 1.0.0
status: draft
date: 2026-03-17
parent_analysis: cli-portify-executor-noop-forensic-report.md
parent_ranking: proposal-ranking.md
fidelity_link: "Link 3: Tasklist -> Code"
priority: P0
estimated_scope: 300-400 lines production code
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
```

The legacy `class` + `param` split form is accepted as equivalent to
`symbol: "ClassName.param"` and normalized on load.

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
   - directories containing 3+ Python files with a common function prefix
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
enforcement_mode: shadow
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
        "unwired_count",
        "orphan_count",
        "registry_count",
        "total_findings",
        "analysis_complete",
        "enforcement_mode",
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

**Shadow mode flow** (v1.0 default):

```python
# In execute_phase_tasks() or _run_task_subprocess(), after classification:

if config.wiring_gate_mode == "off":
    # Skip wiring analysis entirely; no report emitted
    return

wiring_report_path = work_dir / f"{task_id}-wiring-report.md"
report = run_wiring_analysis(target_dir=config.source_dir)
emit_report(report, wiring_report_path)

if config.wiring_gate_mode == "shadow":
    # Log result but do not affect task status
    logger.info(f"[shadow] Wiring gate: {report.total_findings} findings")
elif config.wiring_gate_mode == "soft":
    # Warn in TUI but do not block
    if not report.passed:
        tui.warn(f"Wiring gate: {report.total_findings} findings")
elif config.wiring_gate_mode == "full":
    # Block task completion
    passed, reason = gate_passed(wiring_report_path, WIRING_GATE)
    if not passed:
        # Trigger remediation via SprintGatePolicy
        ...
```

**Configuration**: New field on `SprintConfig`:

```python
wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

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
| `src/superclaude/cli/sprint/models.py` | MODIFY | +5 | Add `wiring_gate_mode` field to `SprintConfig` |
| `src/superclaude/cli/sprint/executor.py` | MODIFY | +25 | Post-task wiring analysis hook |
| `src/superclaude/cli/roadmap/gates.py` | MODIFY | +40 | `_deviation_counts_reconciled` semantic check |
| `tests/audit/test_wiring_gate.py` | CREATE | 200-250 | Unit tests for all analysis functions |
| `tests/audit/test_deviation_recon.py` | CREATE | 60-80 | Unit tests for deviation count reconciliation |
| `tests/audit/fixtures/` | CREATE | 50-80 | Python fixtures for wiring analysis tests |

**Total new production code**: ~360-430 lines
**Total new test code**: ~310-410 lines

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
    enforcement_mode: str = "shadow",
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

### 6.3 Gate Contract

The `WIRING_GATE` constant conforms to `GateCriteria` and is evaluated by the
existing `gate_passed()` function in `pipeline/gates.py` without modification.

**Frontmatter contract** (must appear in every report):

| Field | Type | Constraint |
|-------|------|-----------|
| `gate` | string | Must be `"wiring-verification"` |
| `target_dir` | string | Non-empty |
| `files_analyzed` | int | >= 0 |
| `unwired_count` | int | Must be 0 for gate pass |
| `orphan_count` | int | Must be 0 for gate pass |
| `registry_count` | int | Must be 0 for gate pass |
| `total_findings` | int | Must equal sum of above three |
| `analysis_complete` | bool | Must be true |
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

---

## 8. Rollout Plan

### Phase 1: Shadow (this release)

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

- Findings block task completion at STRICT tier
- Remediation via `SprintGatePolicy.build_remediation_step()`
- No override without explicit whitelist entry

### Rollout Decision Criteria

| Metric | Shadow -> Soft Threshold | Soft -> Full Threshold |
|--------|--------------------------|------------------------|
| False positive rate | < 15% of findings are whitelisted | < 5% |
| True positive rate | > 50% of findings are genuine bugs | > 80% |
| Analysis time p95 | < 5 seconds | < 3 seconds |
| Whitelist stability | Whitelist unchanged for 2+ sprints | Whitelist unchanged for 5+ sprints |

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
                  sprint/config.py (MODIFY)
                  roadmap/gates.py (MODIFY) -- deviation count recon only
```

**Zero changes to existing gate infrastructure.** The wiring gate is a new consumer
of the existing `GateCriteria`/`SemanticCheck`/`gate_passed()` pattern.

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
| T07 | Sprint integration (shadow mode hook) | `sprint/executor.py` (modify), `sprint/config.py` (modify) | T05 |
| T08 | Deviation count reconciliation | `roadmap/gates.py` (modify) | -- |
| T09 | Unit tests for T08 | `tests/audit/test_deviation_recon.py` | T08 |
| T10 | Integration test: cli-portify fixture | `tests/audit/test_wiring_integration.py` | T06, T07 |
| T11 | Retrospective: run against actual `cli_portify/` | Validation report | T10 |

**Critical path**: T01 -> T02/T03/T04 (parallel) -> T05 -> T06 -> T07 -> T10 -> T11

**Parallel track**: T08 -> T09 (independent of T01-T07)

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
