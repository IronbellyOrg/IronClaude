---
release: wiring-verification-gate-v1.0
version: 1.0.0
status: draft
date: 2026-03-18
parent_specs:
  - .dev/releases/backlog/v3.0_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md
phase1_findings:
  - docs/generated/audit-wiring-detection-analysis.md
  - docs/generated/cli-unwired-components-audit.md
  - docs/generated/gate-system-deep-analysis.md
priority: P0
estimated_scope: 360-430 lines production, 310-410 lines test
---

# Wiring Verification Gate — Design Specification

## 1. Problem Statement

The pipeline's gate infrastructure validates **documents**, not **code integration**. Components defined in specifications and decomposed into tasks can pass all existing gates while producing code where modules are never connected to their consumers.

Phase 1 findings identified **32 unwired symbols across 14 files** in `src/superclaude/cli/`:

| Category | Count | Example |
|----------|-------|---------|
| `Optional[Callable]=None` never provided | 11 | `PortifyExecutor.step_runner`, `StallDetector.kill_fn` |
| Dispatch registries with zero external consumers | 3 registries | `GATE_REGISTRY`, `PROMPT_BUILDERS`, `FAILURE_HANDLERS` |
| Gate classes defined but never registered | 21 symbols | `SprintGatePolicy`, `evidence_gate()`, 10 `gate_*()` functions |

**Root cause**: Link 3 of the fidelity chain (Tasklist -> Code) has zero programmatic coverage. No gate exists that verifies code-level wiring after implementation.

---

## 2. Goals and Non-Goals

### Goals

| # | Goal | Detection Mechanism |
|---|------|-------------------|
| G1 | Detect unwired injectable dependencies | AST: `Optional[Callable]=None` params never provided at any call site |
| G2 | Detect orphan modules | AST+grep: exported functions in provider directories with zero importers |
| G3 | Detect unregistered dispatch entries | AST: registry dict values referencing unresolvable symbols |
| G4 | Emit structured reports compatible with `GateCriteria`/`SemanticCheck` | YAML frontmatter + Markdown body |
| G5 | Shadow -> soft -> full rollout | Configurable `wiring_gate_mode` field |
| G6 | Integrate with cleanup-audit protocol | Extend existing 5 agents, reuse `ToolOrchestrator` |
| G7 | Fit into roadmap pipeline as post-merge gate step | New `Step` in `_build_steps()` |

### Non-Goals (v1.0)

- No-op fallback detection (deferred to v1.1 pending shadow-mode data)
- Cross-language analysis (Python only)
- Runtime behavioral verification
- Dynamic dispatch resolution (`**kwargs`, `getattr`, `importlib`)
- Modifying the `SemanticCheck` interface (no `pre_checks`)
- Import alias resolution (known FPR source, tracked for v1.1)

---

## 3. Design Constraints

### 3.1 Preserve existing substrate

Zero changes to:
- `pipeline/models.py` -- `SemanticCheck`, `GateCriteria`
- `pipeline/gates.py` -- `gate_passed()`

Checks remain pure `Callable[[str], bool]` over generated report content.

### 3.2 Respect pipeline layering (NFR-007)

- `audit/*` -> may import `pipeline/models.py`
- `roadmap/*` -> may import gate constants from `audit/*`
- `pipeline/*` -> must NOT import `roadmap/*`, `audit/*`, `sprint/*`

### 3.3 Separate analysis from enforcement

- **Analysis engine**: AST/reference analysis over source files -> `WiringReport`
- **Report artifact**: Markdown + YAML frontmatter summarizing findings
- **Gate enforcement**: `gate_passed(report, WIRING_GATE)` on the artifact

Gate validates the **report**, not the repository directly. This preserves the document-first gate model while extending it to code-wiring evidence.

---

## 4. Architecture

### 4.1 Placement Within Existing Infrastructure

```
EXISTING (unchanged)                    NEW
=====================                   ===

pipeline/models.py                      audit/wiring_gate.py
  GateCriteria ----------------------->   WIRING_GATE (constant)
  SemanticCheck ---------------------->   5 check functions

pipeline/gates.py
  gate_passed() ---------------------->   evaluates WIRING_GATE

roadmap/executor.py                     (MODIFY: add Step to _build_steps())
  _build_steps() --------------------->   Step(gate=WIRING_GATE, ...)

sprint/executor.py                      (MODIFY: post-task shadow hook)
  execute_phase_tasks() -------------->   run_wiring_analysis()

pipeline/trailing_gate.py
  TrailingGateRunner ----------------->   deferred eval in shadow/soft modes
```

### 4.2 Module Architecture

```
src/superclaude/cli/audit/
|-- wiring_gate.py          (NEW -- 250-300 LOC)
|   |-- WiringFinding        dataclass
|   |-- WiringReport         dataclass
|   |-- analyze_unwired_callables(paths) -> list[WiringFinding]
|   |-- analyze_orphan_modules(paths, root) -> list[WiringFinding]
|   |-- analyze_unwired_registries(paths) -> list[WiringFinding]
|   |-- run_wiring_analysis(target_dir, config) -> WiringReport
|   |-- emit_report(report, output_path, mode) -> None
|   |-- _analysis_complete_true(content) -> bool     # SemanticCheck fn
|   |-- _zero_unwired_callables(content) -> bool     # SemanticCheck fn
|   |-- _zero_orphan_modules(content) -> bool        # SemanticCheck fn
|   |-- _zero_unwired_registries(content) -> bool    # SemanticCheck fn
|   |-- _total_findings_consistent(content) -> bool  # SemanticCheck fn
|   '-- WIRING_GATE          GateCriteria constant
|
'-- wiring_config.py        (NEW -- 40-60 LOC)
    |-- WiringConfig         dataclass
    |-- DEFAULT_REGISTRY_PATTERNS
    '-- load_wiring_config(path) -> WiringConfig
```

### 4.3 Data Flow

```
Task completes (sprint runner)
         |
         v
Collect changed file paths (git diff)
         |
         v
+----------------------------+
|  run_wiring_analysis()     |
|                            |
|  1. analyze_unwired_       |
|     callables()            |  AST: find Optional[Callable]=None
|  2. analyze_orphan_        |      with zero call-site provision
|     modules()              |  AST+grep: provider dir functions
|  3. analyze_unwired_       |      with zero importers
|     registries()           |  AST: registry values that don't resolve
+------------+---------------+
             |
             v
+----------------------------+
|  emit_report()             |
|  -> wiring-report.md       |  YAML frontmatter + finding details
|  (yaml.safe_dump for       |  Conforms to GateCriteria pattern
|   string fields)           |
+------------+---------------+
             |
             v
+----------------------------+
|  gate_passed(              |
|    wiring-report.md,       |  Existing function, unmodified
|    WIRING_GATE             |
|  )                         |
+------------+---------------+
             |
     +-------+--------+
     v       v        v
  shadow:  soft:    full:
  log      warn     block
```

### 4.4 Integration Points

#### 4.4.1 Roadmap Pipeline (post-merge gate)

Insert as new `Step` in `roadmap/executor.py:_build_steps()` after `spec-fidelity` (line 473):

```python
Step(
    id="wiring-verification",
    prompt=build_wiring_verification_prompt(spec_path, merge_file),
    output_file=out / "wiring-report.md",
    gate=WIRING_GATE,
    timeout_seconds=120,
    inputs=[merge_file],
    retry_limit=1,
    gate_mode=GateMode.TRAILING,  # non-blocking initially (shadow)
),
```

**Why post-merge**: The merged artifact establishes final intended architecture. The gate validates whether the implementation graph is actually connected. This matches the pattern established by `spec-fidelity` and the three pre-defined but unwired gates (`DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE`, `CERTIFY_GATE`).

**Execution approach**: Deterministic Python analysis runs inside a helper, then roadmap step certifies and summarizes. Gate validates the artifact. This avoids LLM-dependent detection (rejected: too weak for deterministic code-wiring assurance).

#### 4.4.2 Sprint Pipeline (post-task hook)

New field on `SprintConfig`:

```python
wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

Hook in `sprint/executor.py` after task classification:

```python
if config.wiring_gate_mode != "off":
    report = run_wiring_analysis(target_dir=config.source_dir)
    emit_report(report, work_dir / f"{task_id}-wiring-report.md",
                enforcement_mode=config.wiring_gate_mode)
    if config.wiring_gate_mode == "shadow":
        logger.info(f"[shadow] Wiring gate: {report.total_findings} findings")
    elif config.wiring_gate_mode == "soft":
        if not report.passed:
            tui.warn(f"Wiring gate: {report.total_findings} findings")
    elif config.wiring_gate_mode == "full":
        passed, reason = gate_passed(wiring_report_path, WIRING_GATE)
        if not passed:
            # Trigger remediation via SprintGatePolicy
            ...
```

#### 4.4.3 Cleanup-Audit Protocol Integration

**No new agents required.** All 5 existing agents are extended:

| Agent | Extension | Change |
|-------|-----------|--------|
| **audit-scanner** (Haiku) | Add broken-import signals to Pass 1 triage | Behavioral spec update |
| **audit-analyzer** (Sonnet) | Add wiring fields to 8-field profile (`wiring_surfaces`, `registry_symbols`, `effective_references`, `wiring_notes`) | Behavioral spec update |
| **audit-comparator** (Sonnet) | Add "wiring consistency" comparison -- registry/implementation alignment | Behavioral spec update |
| **audit-validator** (Sonnet) | Add Check 5: Wiring Claim Verification -- confirm import/registration resolve | Behavioral spec update |
| **audit-consolidator** (Sonnet) | Add "Wiring Health" rollup section | Behavioral spec update |

**Hybrid mode**: Direct AST analysis remains authoritative. Cleanup-audit artifacts serve as advisory evidence and false-positive suppressors. This avoids coupling correctness to prior audit execution while reusing audit investments.

**ToolOrchestrator extension**: The constructor accepts `analyzer: AnalysisTool | None`. Create an AST-aware analyzer that populates the currently-empty `references` field with symbol-level resolution data, feeding richer data into `dependency_graph.py` Tier-A edges.

---

## 5. Detection Design

### 5.1 Detector A -- Unwired Callable Injections

**Algorithm**:

```
1. AST-parse all Python files in target directory
2. For each class definition:
   a. Find __init__ method
   b. Extract params where annotation matches Callable with None default:
      - Pattern: re.compile(r'\b(typing\.)?Callable\b|collections\.abc\.Callable\b')
      - Must have: isinstance(param.default, ast.Constant) and param.default.value is None
      - ast.unparse() handles all annotation forms (Optional[Callable[...]], Callable | None)
      - from __future__ import annotations does NOT change ast.parse() output
   c. Record as injectable: (class_name, param_name, file_path, line)
3. For each injectable:
   a. Search all Python files for class construction call sites
   b. Check if any call site provides the parameter by keyword
   c. Zero providers -> WiringFinding(unwired_callable)
```

**Known limitation**: Import aliases and re-exports produce false positives (30-70% FPR in codebases using package-level re-exports). Tracked for v1.1 alias pre-pass via `ast.Import`/`ast.ImportFrom` traversal with `__init__.py` chain resolution (max 3 hops).

**Whitelist**: `wiring_whitelist.yaml`:
```yaml
unwired_callables:
  - symbol: "module.path.ClassName.param_name"  # required; dotted path
    reason: "string"                             # required; non-empty
```

Phase 1 (shadow): malformed entries WARNED and skipped, not fatal. Phase 2: malformed entries raise `WiringConfigError`.

**Severity policy**:
- **critical**: injectable controls execution, process dispatch, or enforcement
- **major**: hook with safe in-module fallback
- **info**: explicitly whitelisted observability hook

### 5.2 Detector B -- Orphan Modules

**Algorithm**:

```
1. Identify provider directories by convention:
   steps/, handlers/, validators/, checks/
   (configurable via WiringConfig.provider_dir_names)
2. For each Python file in provider directories:
   a. AST-parse, extract top-level public function definitions (exclude _private)
   b. Search all Python files OUTSIDE provider dir for:
      - import statements referencing the function
      - from ... import statements referencing the function
   c. Zero importers -> WiringFinding(orphan_module)
Exclusions: __init__.py, conftest.py, test_*.py
```

**Evidence layering**: AST/import evidence is authoritative. Cleanup-audit dynamic-import evidence (from `dynamic_imports.py` 5-pattern check) serves as suppression signal -- a symbol flagged for dynamic retention is not orphaned.

### 5.3 Detector C -- Unregistered Dispatch Entries

**Algorithm**:

```
1. AST-parse all Python files
2. For each module-level Dict assignment matching registry pattern:
   Pattern: re.compile(r'^(STEP_REGISTRY|STEP_DISPATCH|PROGRAMMATIC_RUNNERS|
                         \w*_REGISTRY|\w*_DISPATCH|\w*_HANDLERS|\w*_ROUTER|\w*_BUILDERS)$')
3. For each dict entry:
   a. If value is Name node: verify importable in scope
   b. If value is string: verify resolves to module.function
   c. If value is None: flag as explicit no-op entry
4. Unresolvable entries -> WiringFinding(unwired_registry)
5. Registries where accessor has zero external callers -> WiringFinding(unwired_registry)
```

**Classification**:
- **critical**: unresolved entry (function reference doesn't exist)
- **major**: registry/accessor entirely unused externally
- **major**: explicit `None` entry without proven alternate handling

---

## 6. Data Models

```python
@dataclass
class WiringFinding:
    """A single wiring verification finding."""
    finding_type: Literal["unwired_callable", "orphan_module", "unwired_registry"]
    file_path: str
    symbol_name: str
    line_number: int
    detail: str
    severity: Literal["critical", "major"] = "critical"


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
        return len(self.unwired_callables) + len(self.orphan_modules) + len(self.unwired_registries)

    @property
    def passed(self) -> bool:
        return self.total_findings == 0


@dataclass
class WiringConfig:
    registry_patterns: re.Pattern = DEFAULT_REGISTRY_PATTERNS
    provider_dir_names: frozenset[str] = frozenset({
        "steps", "handlers", "validators", "checks",
    })
    whitelist_path: Path | None = None
    exclude_patterns: list[str] = field(default_factory=lambda: [
        "test_*.py", "conftest.py", "__init__.py",
    ])
```

---

## 7. Report Format

YAML frontmatter + Markdown body. All string-valued fields serialized via `yaml.safe_dump()`.

**Frontmatter contract**:

| Field | Type | Constraint |
|-------|------|-----------|
| `gate` | string | `"wiring-verification"` |
| `target_dir` | string | Non-empty |
| `files_analyzed` | int | >= 0 |
| `unwired_count` | int | Must be 0 for pass |
| `orphan_count` | int | Must be 0 for pass |
| `registry_count` | int | Must be 0 for pass |
| `total_findings` | int | Must equal sum of above three |
| `analysis_complete` | bool | Must be true |
| `enforcement_mode` | string | `shadow`/`soft`/`full` |
| `whitelist_entries_applied` | int | >= 0 |
| `audit_artifacts_used` | bool | Whether cleanup-audit evidence was available |

---

## 8. Gate Definition

```python
WIRING_GATE = GateCriteria(
    required_frontmatter_fields=[
        "gate", "target_dir", "files_analyzed",
        "unwired_count", "orphan_count", "registry_count",
        "total_findings", "analysis_complete", "enforcement_mode",
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
            failure_message="unwired_count must be 0",
        ),
        SemanticCheck(
            name="zero_orphan_modules",
            check_fn=_zero_orphan_modules,
            failure_message="orphan_count must be 0",
        ),
        SemanticCheck(
            name="zero_unwired_registries",
            check_fn=_zero_unwired_registries,
            failure_message="registry_count must be 0",
        ),
        SemanticCheck(
            name="total_findings_consistent",
            check_fn=_total_findings_consistent,
            failure_message="total_findings must equal sum of category counts",
        ),
    ],
)
```

Semantic check functions follow the established `(content: str) -> bool` pattern used throughout `roadmap/gates.py`.

---

## 9. Rollout Model

### Phase 1: Shadow (this release)

**Pre-activation checklist** (blocking):

1. **Provider directory validation**: At least one directory matching `provider_dir_names` must exist with Python files. Zero matches -> update config before proceeding. A misconfigured run produces silent null results indistinguishable from genuinely clean codebases.

2. **Zero-findings sanity check**: First run on repos with >50 Python files producing zero findings across ALL analyzers -> `WARN: zero-findings-on-first-run`, halt baseline collection until config verified.

**Behavior**:
- Wiring analysis runs after every sprint task
- Results logged to `.sprint-state/wiring/`
- No impact on task status or pipeline flow
- In roadmap pipeline: `GateMode.TRAILING` (non-blocking)
- Collects baseline: FPR, finding distribution, analysis time

### Phase 2: Soft (release +1)

- Findings surfaced as warnings in sprint TUI
- Findings recorded in `DeferredRemediationLog`
- Block only at release scope (per `resolve_gate_mode()`)
- Override via `--skip-wiring-gate`
- In roadmap pipeline: `GateMode.BLOCKING` with `enforcement_tier="STANDARD"`

**FPR calibration**: Set thresholds at `measured_FPR + 2 sigma` above re-export noise floor. Phase 2 MUST NOT activate if unwired-callable FPR cannot be separated from noise.

### Phase 3: Full (release +2)

- Findings block task completion at STRICT tier
- Remediation via `SprintGatePolicy.build_remediation_step()`
- No override without explicit whitelist entry
- In roadmap pipeline: `GateMode.BLOCKING` with `enforcement_tier="STRICT"`

### Decision Criteria

| Metric | Shadow -> Soft | Soft -> Full |
|--------|---------------|-------------|
| False positive rate | < 15% whitelisted | < 5% |
| True positive rate | > 50% genuine bugs | > 80% |
| Analysis time p95 | < 5 seconds | < 3 seconds |
| Whitelist stability | Unchanged 2+ sprints | Unchanged 5+ sprints |

### Unified Audit Gating Integration

This rollout adopts the Unified Audit Gating infrastructure (SS7.1/SS7.2 profiles, override governance, rollback triggers). Values above serve as initial configuration within that framework.

---

## 10. Companion: Deviation Count Reconciliation

Single function added to `SPEC_FIDELITY_GATE.semantic_checks` in `roadmap/gates.py`:

```python
def _deviation_counts_reconciled(content: str) -> bool:
    """Verify frontmatter severity counts match body deviation entries."""
    # 1. Parse frontmatter for high/medium/low_severity_count
    # 2. Regex-scan body for DEV-\d{3} entries, extract severity
    # 3. Compare counts -> fail on mismatch
```

Estimated: 35-50 LOC. Independent of wiring gate (parallel track).

---

## 11. False Positive Governance

### Known noise sources

| Source | Expected FPR | v1.0 Mitigation | Planned Fix |
|--------|-------------|-----------------|-------------|
| Re-exported classes (import aliases) | 30-70% of unwired-callable findings | Raise Phase 2 threshold; document noise floor | v1.1 alias pre-pass |
| `provider_dir_names` misconfiguration | 100% of orphan findings (silent) | Pre-activation checklist | Config validation |
| Intentional lifecycle hooks | Variable | Whitelist with required reason | N/A -- by design |
| Dynamic/plugin loading | Low | Cleanup-audit dynamic-import evidence as suppressor | v1.1 `dynamic_imports.py` integration |

### Suppression policy

- Explicit whitelist file with required reason string
- `whitelist_entries_applied` count in report frontmatter for audit visibility
- Cleanup-audit dynamic-import evidence downgrades equivalent orphan findings

---

## 12. File Manifest

| File | Action | Est. LOC | Purpose |
|------|--------|----------|---------|
| `src/superclaude/cli/audit/wiring_gate.py` | CREATE | 250-300 | Core analysis, report emitter, gate definition |
| `src/superclaude/cli/audit/wiring_config.py` | CREATE | 40-60 | Configuration, patterns, whitelist loader |
| `src/superclaude/cli/sprint/models.py` | MODIFY | +5 | `wiring_gate_mode` field on SprintConfig |
| `src/superclaude/cli/sprint/executor.py` | MODIFY | +25 | Post-task wiring analysis hook |
| `src/superclaude/cli/roadmap/executor.py` | MODIFY | +15 | New Step in `_build_steps()` |
| `src/superclaude/cli/roadmap/gates.py` | MODIFY | +40 | Deviation count reconciliation check |
| `src/superclaude/agents/audit-scanner.md` | MODIFY | +10 | Wiring signal additions |
| `src/superclaude/agents/audit-analyzer.md` | MODIFY | +10 | Wiring profile fields |
| `src/superclaude/agents/audit-comparator.md` | MODIFY | +8 | Wiring consistency check |
| `src/superclaude/agents/audit-validator.md` | MODIFY | +8 | Check 5 addition |
| `src/superclaude/agents/audit-consolidator.md` | MODIFY | +10 | Wiring Health rollup |
| `tests/audit/test_wiring_gate.py` | CREATE | 200-250 | Unit tests (14 minimum) |
| `tests/audit/test_deviation_recon.py` | CREATE | 60-80 | Deviation recon tests |
| `tests/audit/fixtures/` | CREATE | 50-80 | Python fixtures for wiring tests |

**Total new production**: ~360-430 LOC | **Total new test**: ~310-410 LOC | **Agent spec mods**: ~46 lines

---

## 13. Interface Contracts

### 13.1 Public API

```python
def run_wiring_analysis(
    target_dir: Path,
    config: WiringConfig | None = None,
) -> WiringReport:
    """Analyze a directory for wiring verification issues."""

def emit_report(
    report: WiringReport,
    output_path: Path,
    enforcement_mode: str = "shadow",
) -> None:
    """Write wiring report as Markdown with YAML frontmatter.
    String fields serialized via yaml.safe_dump()."""
```

### 13.2 Gate Contract

`WIRING_GATE` conforms to `GateCriteria` and is evaluated by existing `gate_passed()` in `pipeline/gates.py` **without modification**.

### 13.3 Dependency Direction

```
audit/wiring_gate.py ------> pipeline/models.py   (import GateCriteria, SemanticCheck)
audit/wiring_config.py                             (standalone)
sprint/executor.py ---------> audit/wiring_gate.py (import run_wiring_analysis, emit_report)
roadmap/executor.py --------> audit/wiring_gate.py (import WIRING_GATE)
roadmap/gates.py                                   (self-contained deviation check)
```

Strictly unidirectional. `pipeline/` has zero imports from domain modules (NFR-007 preserved).

---

## 14. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| R1: FP from intentional `Optional[Callable]` hooks | High | Medium | Whitelist mechanism |
| R2: AST parsing fails on complex patterns | Medium | Low | Graceful degradation: warn, skip file |
| R3: Shadow mode insufficient data | Low | Medium | Minimum 2 releases before enforcement |
| R4: Performance impact on sprint loop | Low | Medium | AST-only, no subprocess; < 2s for 50 files |
| R5: Registry pattern misses new conventions | Medium | Low | Configurable regex |
| R6: `provider_dir_names` mismatch | High | High | Pre-activation checklist + zero-findings sanity |
| R7: Import alias FPR corrupts baseline | High | Medium | Document noise floor; threshold calibration |

---

## 15. Testing Strategy

### Unit Tests (minimum 14)

**analyze_unwired_callables** (4):
1. Positive: `Optional[Callable]=None` with zero providers -> 1 finding
2. Negative: call site provides param by keyword -> 0 findings
3. Whitelist: parameter matches whitelist -> 0 findings
4. Parse error: syntax error file -> warn, skip, no crash

**analyze_orphan_modules** (5):
1. Positive: function in provider dir with zero importers -> 1 finding
2. Negative (direct import): function imported -> 0 findings
3. Negative (`__init__.py` re-export): transitive import -> 0 findings
4. Private function: `_name` excluded -> 0 findings
5. `conftest.py`: excluded -> 0 findings

**analyze_unwired_registries** (2):
1. Positive: unresolvable registry value -> 1 finding
2. Negative: resolvable value -> 0 findings

**emit_report / gate** (3):
1. Findings present -> `gate_passed()` returns `(False, reason)`
2. No findings -> `gate_passed()` returns `(True, None)`
3. YAML-safe: path with colon -> parses without error

### Integration Tests (2)

**SC-010**: cli-portify fixture -- `run_wiring_analysis()` on fixture dir produces exactly 1 `unwired_callable` finding.

**SC-006**: Sprint shadow mode -- wiring gate in shadow mode does not alter task status, does not raise, emits log trace.

### Retrospective Validation

Run against actual `src/superclaude/cli/cli_portify/`. Must detect the 11 `Optional[Callable]=None` params and 3 unwired registries from Phase 1.

---

## 16. Tasklist Index

| Task | Description | Deliverables | Deps |
|------|-------------|-------------|------|
| T01 | Data models (WiringFinding, WiringReport, WiringConfig) | `wiring_gate.py` (partial), `wiring_config.py` | -- |
| T02 | Unwired callable analysis | `wiring_gate.py` (partial) | T01 |
| T03 | Orphan module analysis | `wiring_gate.py` (partial) | T01 |
| T04 | Unwired registry analysis | `wiring_gate.py` (partial) | T01 |
| T05 | Report emitter + WIRING_GATE constant | `wiring_gate.py` (complete) | T01 |
| T06 | Unit tests + fixtures | `tests/audit/test_wiring_gate.py`, `tests/audit/fixtures/` | T02, T03, T04 |
| T07 | Sprint integration (shadow hook) | `sprint/executor.py`, `sprint/models.py` | T05 |
| T08 | Deviation count reconciliation | `roadmap/gates.py` | -- |
| T09 | Unit tests for T08 | `tests/audit/test_deviation_recon.py` | T08 |
| T10 | Roadmap pipeline Step wiring | `roadmap/executor.py` | T05 |
| T11 | Agent behavioral spec updates | 5 agent `.md` files | T05 |
| T12 | Integration test: cli-portify fixture | `tests/audit/test_wiring_integration.py` | T06, T07 |
| T13 | Retrospective: run against actual cli_portify/ | Validation report | T12 |

**Critical path**: T01 -> T02/T03/T04 (parallel) -> T05 -> T06 -> T07 -> T10 -> T12 -> T13

**Parallel track A**: T08 -> T09 (independent)

**Parallel track B**: T11 (after T05)

---

## 17. Success Criteria

| SC | Description | Verification |
|----|-------------|-------------|
| SC-001 | Detects `Optional[Callable]=None` never provided | Unit test |
| SC-002 | Detects orphan modules in provider dirs | Unit test |
| SC-003 | Detects unresolvable registry entries | Unit test |
| SC-004 | Report conforms to GateCriteria pattern | Unit test |
| SC-005 | `gate_passed()` evaluates WIRING_GATE unmodified | Integration test |
| SC-006 | Shadow mode: no task status impact | Integration test |
| SC-007 | Whitelist suppresses + records count | Unit test |
| SC-008 | Deviation count reconciliation catches mismatch | Unit test |
| SC-009 | Analysis < 5s for 50-file packages | Benchmark |
| SC-010 | Catches cli-portify no-op bug retrospectively | Run against actual dir |
| SC-011 | Zero-findings sanity check fires on misconfig | Integration test |
| SC-012 | Agent specs updated with wiring signals | Review |

---

## 18. Coordination Notes

**Merge conflict risk** when modifying `roadmap/gates.py` -- coordinate with:
- Anti-Instincts (`ANTI_INSTINCT_GATE` in v3.05)
- Unified Audit Gating (D-03/D-04 `SPEC_FIDELITY_GATE` extensions in v3.0)

Preferred: single coordinated PR or sequenced PRs with explicit rebase points.

**Existing dead code**: Phase 1 identified 32 unwired symbols. This gate **detects** them going forward but does **not** clean them up. Cleanup tracked separately in v3.6-Cli-portify-fix.
