---
release: wiring-verification-gate-v2.0
version: 2.0.0
status: draft
date: 2026-03-18
supersedes:
  - wiring-verification-gate-v1.0 (backlog/v3.0_fidelity-refactor___)
  - v3.0_wiring-gate spec.md (prior draft from roadmap pipeline)
branch: v3.0-AuditGates
parent_analysis:
  - docs/generated/audit-wiring-detection-analysis.md
  - docs/generated/cli-unwired-components-audit.md
  - docs/generated/gate-system-deep-analysis.md
  - .dev/releases/backlog/v3.0_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md
priority: P0
estimated_scope: 480-580 lines production code, 370-480 lines test code
---

# Wiring Verification Gate v2.0 — Design Specification

## 1. Problem Statement

The pipeline's gate infrastructure validates **documents, not code integration**. Components defined in specifications and decomposed into tasks can pass every existing gate while producing code where modules are never connected to their consumers.

**Evidence**: 32 unwired symbols across 14 files in 5 subsystems (from `cli-unwired-components-audit.md`):

| System | Pattern | Count |
|--------|---------|-------|
| cli-portify executor | `Optional[Callable]=None` defaults never provided | 11 |
| cli-portify gates | `GATE_REGISTRY` + `gate_*()` with zero callers | 12 |
| sprint executor | `SprintGatePolicy` defined, never instantiated | 4 |
| audit modules | `evidence_gate()`, `manifest_gate()` zero callers | 4 |
| roadmap gates | `DEVIATION_ANALYSIS_GATE` defined, never wired to Step | 1 |

### What changed from v1.0

v1.0 was authored before the Phase 1 deep analysis. This v2.0 spec:

- Adds precise substrate references with exact line numbers
- Adds cleanup-audit agent integration (v1.0 covered sprint only)
- Adds dual-mode operation: roadmap pipeline gate + cleanup-audit pass extension
- Adds `ToolOrchestrator` analyzer plugin for audit infrastructure reuse
- Adds `GateMode.TRAILING` integration via `TrailingGateRunner` for shadow phase
- Adds explicit design constraint: deterministic Python analysis, not LLM synthesis
- Refines rollout plan with `resolve_gate_mode()` scope awareness

---

## 2. Goals and Non-Goals

### Goals

| # | Goal | Verification |
|---|------|-------------|
| G-001 | Detect unwired injectable dependencies (`Optional[Callable]=None` never provided) | SC-001 |
| G-002 | Detect orphan modules (exported functions never imported by any consumer) | SC-002 |
| G-003 | Detect unwired dispatch registries (entries mapping to non-importable functions) | SC-003 |
| G-004 | Emit structured YAML+Markdown report compatible with `GateCriteria`/`SemanticCheck` | SC-004 |
| G-005 | Deploy in shadow mode initially, path to soft and full enforcement | SC-006 |
| G-006 | Plug into roadmap pipeline via `_build_steps()` as post-merge step | SC-005 |
| G-007 | Integrate with cleanup-audit protocol (extend audit-scanner, audit-analyzer, audit-validator) | SC-011, SC-012 |
| G-008 | Reuse `ToolOrchestrator` analyzer injection seam for AST analysis | SC-013 |

### Non-Goals (v2.0)

- No-op fallback detection (deferred to v2.1 pending shadow data)
- Cross-language analysis (Python only)
- Runtime behavioral verification (Smoke Test Gate domain)
- Dynamic dispatch resolution (`**kwargs`, `getattr`, `importlib`)
- Modifying `SemanticCheck` interface: `check_fn: Callable[[str], bool]` preserved
- Modifying `gate_passed()` in `pipeline/gates.py`
- Creating parallel gate infrastructure

---

## 3. Design Constraints

### 3.1 Preserve the existing gate substrate

This release is a **consumer** of:

| Symbol | Location | Contract |
|--------|----------|----------|
| `SemanticCheck` | `pipeline/models.py:58-65` | `check_fn: Callable[[str], bool]` — pure, no I/O |
| `GateCriteria` | `pipeline/models.py:67-75` | `required_frontmatter_fields`, `min_lines`, `enforcement_tier`, `semantic_checks` |
| `Step` | `pipeline/models.py:77-90` | `gate: GateCriteria`, `gate_mode: GateMode` |
| `GateMode` | `pipeline/models.py:46-55` | `BLOCKING`, `TRAILING` |
| `gate_passed()` | `pipeline/gates.py:20-74` | `(Path, GateCriteria) -> tuple[bool, str \| None]` |
| `TrailingGateRunner` | `pipeline/trailing_gate.py:88-213` | `.submit(step, gate_check)` for non-blocking evaluation |
| `DeferredRemediationLog` | `pipeline/trailing_gate.py:489-578` | Persistence for shadow/soft mode failures |

**No signature changes** to any of these.

### 3.2 Preserve layering (NFR-007)

```
audit/*       ──may import──> pipeline/models.py
roadmap/*     ──may import──> audit/*, pipeline/*
sprint/*      ──may import──> audit/*, pipeline/*
pipeline/*    ──MUST NOT import──> roadmap/*, audit/*, sprint/*
```

### 3.3 Separate analysis from enforcement

Three distinct layers, matching existing document-first gate architecture:

1. **Deterministic wiring analysis** — pure Python over source files (no LLM)
2. **Artifact emission** — Markdown report with YAML frontmatter
3. **Gate enforcement** — `gate_passed(report_file, WIRING_GATE)` via existing substrate

### 3.4 Extend, don't duplicate cleanup-audit

- Extend `audit-analyzer` evidence collection, not create new agent types
- Reuse existing audit structural outputs as advisory inputs
- Keep the roadmap wiring step authoritative through direct deterministic analysis
- Use audit evidence as false-positive suppressor, not primary data source

---

## 4. Architecture

### 4.1 System Context

```
EXISTING SUBSTRATE (zero changes)              NEW COMPONENTS
================================              ==============

pipeline/models.py:58-75                      audit/wiring_gate.py (CREATE)
  SemanticCheck ──────────────────────────>      WIRING_GATE constant
  GateCriteria ───────────────────────────>      check_fn implementations

pipeline/gates.py:20-74                       audit/wiring_config.py (CREATE)
  gate_passed() ──────────────────────────>      evaluates WIRING_GATE

pipeline/trailing_gate.py:88-213              audit/wiring_analyzer.py (CREATE)
  TrailingGateRunner ─────────────────────>      ToolOrchestrator AST plugin
  DeferredRemediationLog ─────────────────>      shadow-mode persistence

audit/tool_orchestrator.py
  AnalysisTool injection seam ────────────>    wiring_analyzer.ast_analyze_file()

pipeline/models.py:77-90
  Step(gate=..., gate_mode=...) ──────────>  roadmap/executor.py (MODIFY)
```

### 4.2 Module Map

```
src/superclaude/cli/
├── audit/
│   ├── wiring_gate.py          CREATE  Core analysis + gate definition + report emitter
│   ├── wiring_config.py        CREATE  Configuration, patterns, whitelist loader
│   └── wiring_analyzer.py      CREATE  AST analyzer plugin for ToolOrchestrator
├── roadmap/
│   ├── executor.py             MODIFY  Add wiring-verification step to _build_steps()
│   ├── gates.py                MODIFY  Import WIRING_GATE, add to ALL_GATES
│   └── prompts.py              MODIFY  Add build_wiring_verification_prompt()
├── sprint/
│   ├── executor.py             MODIFY  Post-task wiring analysis hook (shadow mode)
│   └── models.py               MODIFY  Add wiring_gate_mode to SprintConfig
└── pipeline/
    └── (NO CHANGES)
```

### 4.3 Dual-Mode Operation

#### Mode A: Roadmap Pipeline Gate (post-merge deterministic step)

Appends to the post-merge validation chain:

```
Step 6: merge           → MERGE_GATE               (existing)
Step 7: test-strategy   → TEST_STRATEGY_GATE        (existing)
Step 8: spec-fidelity   → SPEC_FIDELITY_GATE        (existing)
Step 9: wiring-verify   → WIRING_GATE               ← NEW
```

**Insertion point**: `roadmap/executor.py:_build_steps()`, after `spec-fidelity` (line 473).

**Critical design choice**: This is a **deterministic Python step**, not an LLM step. The executor special-cases it: runs `run_wiring_analysis()`, emits `wiring-verification.md`, then normal gate validation applies.

#### Mode B: Sprint Post-Task Check

Runs `run_wiring_analysis()` after each task completes in the sprint loop.

**Integration point**: `sprint/executor.py`, after task classification, before status finalization.

#### Mode C: Cleanup-Audit Pass Extension

Extends existing 3-pass audit with wiring-aware capabilities via agent behavioral rule additions (see Section 6).

---

## 5. Detailed Design

### 5.1 Data Models

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
    severity: Literal["critical", "major", "info"] = "critical"


@dataclass
class WiringReport:
    """Aggregate wiring analysis results."""

    target_dir: str
    files_analyzed: int = 0
    unwired_callables: list[WiringFinding] = field(default_factory=list)
    orphan_modules: list[WiringFinding] = field(default_factory=list)
    unwired_registries: list[WiringFinding] = field(default_factory=list)

    @property
    def total_findings(self) -> int:
        return (
            len(self.unwired_callables)
            + len(self.orphan_modules)
            + len(self.unwired_registries)
        )

    @property
    def passed(self) -> bool:
        return self.total_findings == 0
```

### 5.2 Analysis Functions

#### 5.2.1 Unwired Callable Analysis

**Purpose**: Detect constructor parameters typed `Optional[Callable]` (or `Callable | None`) with default `None` that are never explicitly provided at any call site.

**Algorithm**:

```
1. AST-parse all Python files in target directory
2. For each class __init__:
   a. Extract params where:
      - ast.unparse(annotation) matches \bCallable\b pattern
      - default is ast.Constant with value None
   b. Record: (class_name, param_name, file_path, line)
3. For each injectable:
   a. Search all Python files for call sites constructing that class
   b. Check if any call site provides the parameter by keyword
   c. Zero providers → WiringFinding(unwired_callable)
```

**Pattern matched** (from forensic report):
```python
class PortifyExecutor:
    def __init__(self, ..., step_runner: Optional[Callable] = None):
        ...

# This call does NOT provide step_runner:
executor = PortifyExecutor(steps=steps, workdir=workdir, ...)
# → Finding: unwired_callable, PortifyExecutor.step_runner
```

**Whitelist**: `wiring_whitelist.yaml` with schema:
```yaml
unwired_callables:
  - symbol: "module.path.ClassName.param_name"
    reason: "Intentional event hook"
```

Validation: entries missing `symbol` or `reason` are MALFORMED. In Phase 1 (shadow), malformed entries are logged as WARNING and skipped. In Phase 2+, malformed entries raise `WiringConfigError`.

**Known limitation (v2.0)**: Import aliases and re-exports not resolved. Expected 30-70% FPR contribution. Planned fix in v2.1: alias pre-pass via `ast.Import`/`ast.ImportFrom` traversal with `__init__.py` chain resolution (max 3 hops).

**Severity policy**:
- **critical**: execution/dispatch/enforcement behavior depends on the seam
- **major**: seam is dead but local fallback exists
- **info**: whitelisted intentional optional

#### 5.2.2 Orphan Module Analysis

**Purpose**: Detect Python files in provider directories whose exported functions are never imported by any consumer.

**Algorithm**:

```
1. Identify provider directories by convention:
   - names matching config.provider_dir_names
   - directories containing 3+ Python files with common function prefix
2. For each Python file in provider directory:
   a. AST-parse, extract top-level def (excluding _private)
   b. Search all Python files OUTSIDE provider dir for imports
   c. Zero importers → WiringFinding(orphan_module)
```

**Pattern matched**:
```python
# src/superclaude/cli/cli_portify/steps/validate_config.py
def run_validate_config():  # never imported by executor.py
    ...
# → Finding: orphan_module, steps/validate_config.py::run_validate_config
```

**Exclusions**: `__init__.py`, `conftest.py`, `test_*.py`

**Evidence rule**: A symbol is orphaned only if BOTH:
1. Direct analysis finds no effective import/call chain
2. Cleanup-audit evidence does not justify dynamic or deferred use

#### 5.2.3 Unwired Registry Analysis

**Purpose**: Detect dispatch registry dictionaries whose values reference non-importable functions.

**Algorithm**:

```
1. AST-parse all Python files
2. For each module-level assignment where:
   a. Target name matches REGISTRY_PATTERNS
   b. Value is a Dict literal
3. For each dict entry:
   a. If value is Name node: verify importable in scope
   b. If value is string: verify resolves to module.function
   c. If value is None: flag as explicit null handler
4. Unresolvable → WiringFinding(unwired_registry)
```

**Registry patterns** (configurable):
```python
DEFAULT_REGISTRY_PATTERNS = re.compile(
    r"^(STEP_REGISTRY|STEP_DISPATCH|PROGRAMMATIC_RUNNERS|"
    r"\w*_REGISTRY|\w*_DISPATCH|\w*_HANDLERS|\w*_ROUTER|\w*_BUILDERS)$"
)
```

Three detection classes:
1. **entry unresolved** — mapped target does not resolve → critical
2. **registry unused** — registry or accessor has zero external consumers → major
3. **explicit None** — entry maps to None with no alternate handler → major

### 5.3 ToolOrchestrator AST Analyzer Plugin

```python
# src/superclaude/cli/audit/wiring_analyzer.py

from __future__ import annotations

import ast
from pathlib import Path

from .tool_orchestrator import FileAnalysis


def ast_analyze_file(file_path: Path, content: str) -> FileAnalysis:
    """AST-based file analyzer for ToolOrchestrator injection.

    Populates the `references` field that the default line-based
    analyzer leaves empty.

    Usage: ToolOrchestrator(analyzer=ast_analyze_file)
    """
    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError:
        return FileAnalysis(
            imports=[], exports=[], references=[], metadata={}
        )

    imports = _extract_imports(tree)
    exports = _extract_exports(tree)
    references = _extract_references(tree, file_path)

    return FileAnalysis(
        imports=imports,
        exports=exports,
        references=references,
        metadata={
            "has_dispatch_registry": _has_registry(tree),
            "injectable_callables": _count_injectable_callables(tree),
        },
    )
```

**Integration**: Pass as `analyzer` parameter to `ToolOrchestrator.__init__()`. This populates the empty `references` field, improving:
- `dependency_graph.py` Tier-A edges (actual imports vs line-based)
- `dead_code.py` detection (symbol-level vs file-level)
- `profile_generator.py` coupling metric (real deps vs stem-matching)

### 5.4 Report Format

YAML frontmatter + Markdown body, conforming to `GateCriteria` validation:

```yaml
---
gate: wiring-verification
target_dir: src/superclaude/cli/cli_portify
files_analyzed: 14
rollout_mode: shadow
analysis_complete: true
audit_artifacts_used: 0
unwired_callable_count: 1
orphan_module_count: 2
unwired_registry_count: 0
critical_count: 3
major_count: 0
info_count: 0
total_findings: 3
blocking_findings: 3
whitelist_entries_applied: 0
severity_summary:
  critical: 3
  major: 0
  info: 0
---
```

**Serialization**: All string-valued frontmatter fields MUST use `yaml.safe_dump()` to prevent YAML injection. Integer/boolean gate-evaluated fields are exempt.

**Whitelist visibility**: `whitelist_entries_applied` is ALWAYS present. Zero if no whitelist configured.

### 5.5 Gate Definition

```python
WIRING_GATE = GateCriteria(
    required_frontmatter_fields=[
        "gate",
        "target_dir",
        "files_analyzed",
        "rollout_mode",
        "analysis_complete",
        "unwired_callable_count",
        "orphan_module_count",
        "unwired_registry_count",
        "critical_count",
        "major_count",
        "total_findings",
        "blocking_findings",
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
            name="recognized_rollout_mode",
            check_fn=_recognized_rollout_mode,
            failure_message="rollout_mode must be shadow, soft, or full",
        ),
        SemanticCheck(
            name="finding_counts_consistent",
            check_fn=_finding_counts_consistent,
            failure_message=(
                "total_findings must equal "
                "unwired_callable_count + orphan_module_count + unwired_registry_count"
            ),
        ),
        SemanticCheck(
            name="severity_summary_consistent",
            check_fn=_severity_summary_consistent,
            failure_message=(
                "critical_count + major_count + info_count must equal total_findings"
            ),
        ),
        SemanticCheck(
            name="zero_blocking_findings_for_mode",
            check_fn=_zero_blocking_findings_for_mode,
            failure_message="blocking_findings must be 0 for gate pass at current rollout_mode",
        ),
    ],
)
```

**Mode-aware enforcement** (key design decision):

The `_zero_blocking_findings_for_mode` check reads `rollout_mode` and `blocking_findings` from frontmatter:
- **shadow**: always returns `True` (findings logged, never block)
- **soft**: returns `True` if `blocking_findings == 0` (only critical block)
- **full**: returns `True` if `blocking_findings == 0` (all findings block)

The `blocking_findings` field is computed by the emitter based on rollout mode:
- shadow: `blocking_findings = 0` always
- soft: `blocking_findings = critical_count`
- full: `blocking_findings = critical_count + major_count`

This encodes rollout policy into the report artifact, keeping semantic checks as pure content validators per the `SemanticCheck` contract.

### 5.6 Roadmap Pipeline Integration

**5-step process** (per gate-system-deep-analysis Section 8):

**Step 1**: Define `WIRING_GATE` in `audit/wiring_gate.py`

**Step 2**: Define prompt in `roadmap/prompts.py`:
```python
def build_wiring_verification_prompt(merge_file: Path, spec_source: str) -> str:
    """Prompt for wiring-verification step (deterministic, not LLM)."""
    return ""  # Non-LLM step; prompt unused but required by Step contract
```

**Step 3**: Import into `roadmap/executor.py`

**Step 4**: Add to `_build_steps()` after `spec-fidelity` (line 473):
```python
Step(
    id="wiring-verification",
    prompt=build_wiring_verification_prompt(merge_file, spec_source),
    output_file=out / "wiring-verification.md",
    gate=WIRING_GATE,
    timeout_seconds=60,
    inputs=[merge_file, spec_fidelity_file],
    retry_limit=0,                         # Deterministic; retry won't help
    gate_mode=GateMode.TRAILING,           # Shadow: non-blocking
),
```

**Step 5**: Update `_get_all_step_ids()` (line 538) and `ALL_GATES` (line 933)

**Executor special-casing**: In `roadmap_run_step()`, detect `step.id == "wiring-verification"`:
```python
if step.id == "wiring-verification":
    report = run_wiring_analysis(target_dir=config.source_dir)
    emit_report(report, step.output_file, enforcement_mode=config.wiring_rollout_mode)
    return StepResult(step=step, status=StepStatus.PASS)
```

**Shadow**: `GateMode.TRAILING` uses `TrailingGateRunner` for async non-blocking evaluation. Failures persist to `DeferredRemediationLog`.

**Full**: Switch to `GateMode.BLOCKING`. `resolve_gate_mode()` forces release scope to BLOCKING regardless.

### 5.7 Sprint Integration

```python
# sprint/models.py
wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"

# sprint/executor.py — after task classification
if config.wiring_gate_mode != "off":
    wiring_report_path = work_dir / f"{task_id}-wiring-report.md"
    report = run_wiring_analysis(target_dir=config.source_dir)
    emit_report(report, wiring_report_path,
                enforcement_mode=config.wiring_gate_mode)

    if config.wiring_gate_mode == "shadow":
        logger.info(f"[shadow] Wiring gate: {report.total_findings} findings")
    elif config.wiring_gate_mode == "soft":
        if not report.passed:
            tui.warn(f"Wiring gate: {report.total_findings} findings")
    elif config.wiring_gate_mode == "full":
        passed, reason = gate_passed(wiring_report_path, WIRING_GATE)
        if not passed:
            ...  # Trigger SprintGatePolicy.build_remediation_step()
```

---

## 6. Cleanup-Audit Agent Integration

### 6.1 Agent Extension Summary

All 5 agents are behavioral specs (`.md` files in `src/superclaude/agents/`). Extensions are additive — no tools change, no existing rules removed.

| Agent | Tools | Change |
|-------|-------|--------|
| audit-scanner (Haiku) | Read, Grep, Glob | Add `REVIEW:wiring` classification signal |
| audit-analyzer (Sonnet) | Read, Grep, Glob | Add 9th mandatory field: "Wiring path" |
| audit-comparator (Sonnet) | Read, Grep, Glob | Add cross-file wiring consistency check |
| audit-validator (Sonnet) | Read, Grep, Glob | Add Check 5: Wiring Claim Verification |
| audit-consolidator (Sonnet) | Read, Grep, Glob, Write | Add "Wiring Health" section to report |

### 6.2 audit-scanner: REVIEW:wiring Signal

For Python source files, check:
- File contains `Optional[Callable]` parameter with `= None` default
- File defines module-level dict matching `*_REGISTRY`, `*_DISPATCH`, `*_HANDLERS`
- File is in a provider directory (`steps/`, `handlers/`, `validators/`, `checks/`)

Files with wiring indicators get `REVIEW:wiring`, proceeding to Pass 2 even if otherwise `KEEP`.

### 6.3 audit-analyzer: 9th Mandatory Field

For `REVIEW:wiring` files, add:

| Field | Description |
|-------|-------------|
| Wiring path | Declaration → Registration → Invocation chain. Each link stated or "MISSING" |

New finding types:
- `UNWIRED_DECLARATION` — symbol declared but never registered/invoked
- `BROKEN_REGISTRATION` — registry entry references non-importable function

### 6.4 audit-validator: Check 5

**Wiring Claim Verification**:
1. Verify declared callable parameters against call site arguments
2. Verify registry entries resolve to importable symbols
3. Verify "Wiring path" field chain is complete

**Critical fail**: DELETE recommendation on a file with a live wiring path.

### 6.5 ToolOrchestrator Integration

```python
orchestrator = ToolOrchestrator(analyzer=ast_analyze_file)
```

Populates `FileAnalysis.references`, improving `dependency_graph.py`, `dead_code.py`, `profile_generator.py`.

### 6.6 Authority Rule

**Hybrid mode**: Direct deterministic analysis is authoritative. Cleanup-audit evidence acts as false-positive suppressor. Correctness does not depend on prior audit runs.

---

## 7. Rollout Plan

### Phase 1: Shadow (this release)

**Pre-activation checklist** (blocking):
1. Confirm `provider_dir_names` matches at least one real directory
2. First-run zero-findings sanity check (>50 files must produce >0 findings)

**Behavior**: Roadmap `GateMode.TRAILING` + Sprint `shadow` + Cleanup-audit `REVIEW:wiring`

### Phase 2: Soft (release +1)

**Criteria**: FPR < 15%, TPR > 50%, p95 < 5s

**Behavior**: `rollout_mode=soft`, `blocking_findings = critical_count`

### Phase 3: Full (release +2)

**Criteria**: FPR < 5%, TPR > 80%, whitelist stable 5+ sprints

**Behavior**: `GateMode.BLOCKING`, `rollout_mode=full`, `blocking_findings = critical + major`

---

## 8. Interface Contracts

### 8.1 Public API

```python
def run_wiring_analysis(target_dir: Path, config: WiringConfig | None = None) -> WiringReport
def emit_report(report: WiringReport, output_path: Path, enforcement_mode: str = "shadow") -> None
def ast_analyze_file(file_path: Path, content: str) -> FileAnalysis
```

### 8.2 Gate Contract

| Frontmatter Field | Type | Pass Condition |
|-------------------|------|----------------|
| `gate` | string | `"wiring-verification"` |
| `target_dir` | string | Non-empty |
| `files_analyzed` | int | >= 0 |
| `rollout_mode` | string | `shadow` / `soft` / `full` |
| `analysis_complete` | bool | `true` |
| `unwired_callable_count` | int | Present |
| `orphan_module_count` | int | Present |
| `unwired_registry_count` | int | Present |
| `critical_count` | int | Present |
| `major_count` | int | Present |
| `total_findings` | int | = sum of type counts |
| `blocking_findings` | int | Must be 0 |
| `whitelist_entries_applied` | int | >= 0 |

### 8.3 Dependency Direction

```
audit/wiring_gate.py    ──> pipeline/models.py     (GateCriteria, SemanticCheck)
audit/wiring_analyzer.py ──> audit/tool_orchestrator.py (FileAnalysis)
audit/wiring_config.py  ──> (stdlib only)
roadmap/executor.py     ──> audit/wiring_gate.py
sprint/executor.py      ──> audit/wiring_gate.py
pipeline/*              ──> NOTHING from audit/roadmap/sprint
```

---

## 9. Risk Assessment

| Risk | L | I | Mitigation |
|------|---|---|-----------|
| R1: FP from intentional Optional[Callable] hooks | H | M | Whitelist; shadow calibration |
| R2: AST parsing fails on complex patterns | M | L | Graceful degradation: log, skip |
| R3: Shadow data insufficient | L | M | Min 2-release shadow period |
| R4: Sprint performance impact | L | M | AST-only, no subprocess; < 2s |
| R5: provider_dir_names misconfiguration | H | H | Pre-activation checklist; sanity check |
| R6: Re-export aliases cause FPR | H | M | v2.1 alias pre-pass; noise floor documented |
| R7: Agent extension regression | M | M | Additive only; existing rules unchanged |
| R8: resolve_gate_mode() forces BLOCKING | L | L | Explicit gate_mode on Step |

---

## 10. Testing Strategy

### 10.1 Unit Tests (minimum 20)

| Function | Tests | Key Assertions |
|----------|-------|---------------|
| `analyze_unwired_callables` | 5 | Detection, negative, whitelist, parse error, multi-class |
| `analyze_orphan_modules` | 5 | Detection, direct import, re-export, private, conftest |
| `analyze_unwired_registries` | 3 | Unresolvable, resolvable, explicit None |
| `emit_report` + gate | 4 | Fail, pass, YAML-safe, mode-aware blocking |
| `ast_analyze_file` | 3 | References populated, registry metadata, syntax error |

### 10.2 Integration Tests (minimum 3)

- SC-010: cli-portify fixture produces exactly 1 unwired_callable finding
- SC-006: Sprint shadow mode non-interference
- SC-013: ToolOrchestrator(analyzer=ast_analyze_file) populates references

### 10.3 Infrastructure

- Fixtures: `tests/audit/fixtures/` (50-80 LOC)
- Coverage: >= 90% on `wiring_gate.py`, `wiring_analyzer.py`

---

## 11. Success Criteria

| SC | Description | Verification |
|----|-------------|-------------|
| SC-001 | Detects Optional[Callable]=None never provided | Unit test |
| SC-002 | Detects orphan modules in provider directories | Unit test |
| SC-003 | Detects unresolvable registry entries | Unit test |
| SC-004 | Report conforms to GateCriteria validation | Unit test |
| SC-005 | gate_passed() evaluates WIRING_GATE unmodified | Integration |
| SC-006 | Shadow mode logs without affecting task status | Integration |
| SC-007 | Whitelist excludes + reports suppression count | Unit test |
| SC-008 | Analysis < 5s for 50 files | Benchmark |
| SC-009 | Catches cli-portify executor no-op bug | Retrospective |
| SC-010 | Pre-activation warns on zero matches | Integration |
| SC-011 | audit-scanner flags REVIEW:wiring | Agent test |
| SC-012 | audit-analyzer 9-field profile with Wiring path | Agent test |
| SC-013 | ToolOrchestrator AST plugin populates references | Unit test |
| SC-014 | Mode-aware: shadow passes, full blocks | Unit test |

---

## 12. File Manifest

### New Files

| File | LOC | Purpose |
|------|-----|---------|
| `src/superclaude/cli/audit/wiring_gate.py` | 280-320 | Core analysis + gate + emitter |
| `src/superclaude/cli/audit/wiring_config.py` | 50-70 | Config, patterns, whitelist |
| `src/superclaude/cli/audit/wiring_analyzer.py` | 140-180 | AST analyzer for ToolOrchestrator |
| `tests/audit/test_wiring_gate.py` | 240-300 | Unit tests |
| `tests/audit/test_wiring_analyzer.py` | 80-100 | AST analyzer tests |
| `tests/audit/test_wiring_integration.py` | 50-80 | Integration tests |
| `tests/audit/fixtures/` | 50-80 | Python test fixtures |

### Modified Files

| File | Delta | Change |
|------|-------|--------|
| `roadmap/executor.py` | +20 | _build_steps() + special-case |
| `roadmap/gates.py` | +5 | Import WIRING_GATE, ALL_GATES |
| `roadmap/prompts.py` | +10 | build_wiring_verification_prompt() |
| `sprint/models.py` | +3 | wiring_gate_mode field |
| `sprint/executor.py` | +25 | Post-task hook |
| `agents/audit-scanner.md` | +15 | REVIEW:wiring signal |
| `agents/audit-analyzer.md` | +20 | 9th field |
| `agents/audit-validator.md` | +15 | Check 5 |

**Total**: ~480-580 new prod + ~420-560 test + ~113 modified

---

## 13. Tasklist Index

| Task | Description | Deps | LOC |
|------|-------------|------|-----|
| T01 | Data models (WiringFinding, WiringReport, WiringConfig) | -- | 100 |
| T02 | Unwired callable analysis | T01 | 80 |
| T03 | Orphan module analysis | T01 | 70 |
| T04 | Unwired registry analysis | T01 | 60 |
| T05 | Report emitter + WIRING_GATE + semantic checks | T01 | 100 |
| T06 | AST analyzer plugin for ToolOrchestrator | T01 | 160 |
| T07 | Unit tests + fixtures | T02-T06 | 400 |
| T08 | Roadmap pipeline integration | T05 | 35 |
| T09 | Sprint integration (shadow hook) | T05 | 28 |
| T10 | Audit agent extensions | T01 | 50 |
| T11 | Integration tests | T07-T10 | 80 |
| T12 | Retrospective: run against cli_portify/ | T11 | -- |

**Critical path**: T01 → T02/T03/T04/T06 (parallel) → T05 → T07 → T08/T09/T10 (parallel) → T11 → T12

---

## 14. Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Enforcement is artifact-based | Fits SemanticCheck contract |
| D2 | Deterministic Python, not LLM | Wiring needs precision |
| D3 | Extend audit-analyzer, no new agent | Reuse 8-field profile |
| D4 | Insert via _build_steps() after spec-fidelity | Static wiring pattern |
| D5 | Shadow/soft/full via rollout_mode frontmatter | No parallel infra |
| D6 | GateMode.TRAILING for shadow phase | Existing TrailingGateRunner |
| D7 | AST analyzer as ToolOrchestrator plugin | Reuses existing seam |

---

## Appendix A: Substrate Reference

| Symbol | Location | Contract |
|--------|----------|----------|
| `SemanticCheck` | `pipeline/models.py:58-65` | `check_fn: Callable[[str], bool]` |
| `GateCriteria` | `pipeline/models.py:67-75` | frontmatter + min_lines + tier + checks |
| `Step` | `pipeline/models.py:77-90` | gate + gate_mode fields |
| `GateMode` | `pipeline/models.py:46-55` | BLOCKING, TRAILING |
| `gate_passed()` | `pipeline/gates.py:20-74` | `(Path, GateCriteria) -> tuple[bool, str\|None]` |
| `_FRONTMATTER_RE` | `pipeline/gates.py:77-80` | YAML extraction regex |
| `TrailingGateRunner` | `trailing_gate.py:88-213` | `.submit()`, `.wait_for_pending()` |
| `DeferredRemediationLog` | `trailing_gate.py:489-578` | `.append()`, `.pending_remediations()` |
| `resolve_gate_mode()` | `trailing_gate.py:593-628` | scope-aware mode resolution |
| `TrailingGatePolicy` | `trailing_gate.py:226-259` | Protocol |
| `SprintGatePolicy` | `sprint/executor.py:50-93` | Concrete policy |
| `ToolOrchestrator` | `audit/tool_orchestrator.py` | analyzer injection seam |
| `FileAnalysis` | `audit/tool_orchestrator.py` | imports, exports, references, metadata |
| `_build_steps()` | `roadmap/executor.py:344-476` | Step list builder |
| `_get_all_step_ids()` | `roadmap/executor.py:538-554` | Ordered ID list |
| `ALL_GATES` | `roadmap/gates.py:933-947` | list[tuple[str, GateCriteria]] |

## Appendix B: Forensic Cross-Reference

| Finding | Section | Task |
|---------|---------|------|
| `step_runner=None` no-op | 5.2.1 | T02 |
| Steps never imported | 5.2.2 | T03 |
| STEP_REGISTRY metadata-only | 5.2.3 | T04 |
| Link 3 zero coverage | 5.6 | T08 |
| Documents validated, not code | 3.3 | All |
| 32 symbols / 14 files | 1 | SC-009 |

## Appendix C: Out of Scope (v2.0)

- Cross-language wiring verification
- Runtime execution tracing
- Deep reflection/dynamic dispatch resolution
- Auto-remediation of findings
- Full program-wide symbol graph replacement
- Generic gate-registration refactor
- SemanticCheck interface modification
