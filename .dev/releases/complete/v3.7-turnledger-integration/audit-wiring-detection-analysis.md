# Deep Analysis: Audit Infrastructure — Wiring Detection & Agent Extensibility

> Generated: 2026-03-23 | Regenerated from: 2026-03-18 original (T02.27 / R-036)
> Target: `src/superclaude/cli/audit/`, `src/superclaude/skills/sc-cleanup-audit-protocol/`
> Branch: `v3.7-TurnLedgerWiring`

---

## Executive Summary

The audit infrastructure is **production-ready** — 40+ Python modules in `src/superclaude/cli/audit/` including a fully implemented AST-based wiring verification gate. Since the original analysis (2026-03-18), the three previously-missing components have been built: `wiring_gate.py` (1077 lines, 3 analyzers), `wiring_analyzer.py` (AST plugin for ToolOrchestrator), and `wiring_config.py` (config + whitelist loading). The wiring gate is registered in the roadmap pipeline, integrated with TurnLedger budget accounting in sprint execution, and covered by dedicated test suites in `tests/roadmap/` and `tests/v3.3/`.

### Delta from 2026-03-18 original

| Item | 2026-03-18 Status | 2026-03-23 Status |
|------|-------------------|-------------------|
| `wiring_gate.py` | **Does not exist** | **Implemented** (1077 lines, 3 analyzers, gate definition, report emitter) |
| `wiring_analyzer.py` | **Does not exist** | **Implemented** (AST plugin for ToolOrchestrator `references` field) |
| `wiring_config.py` | **Does not exist** | **Implemented** (WiringConfig, WhitelistEntry, load_whitelist) |
| `wiring_whitelist.yaml` | **Does not exist** | **Implemented** (empty suppression lists, schema documented) |
| `reachability.py` | **Does not exist** | **Implemented** (AST call-chain reachability for manifest validation) |
| Roadmap gate registration | **Not wired** | **Wired** (`gates.py:1087` — `("wiring-verification", WIRING_GATE)`) |
| Sprint executor integration | **Not wired** | **Wired** (debit_wiring → run_wiring_analysis → credit_wiring) |
| TurnLedger budget accounting | **Not wired** | **Wired** (wiring_analysis_turns, wiring_gate_mode, wiring_gate_scope) |
| KPI metrics | **Not wired** | **Wired** (wiring_findings_total, wiring_turns_used, wiring_net_cost, etc.) |
| Test coverage | **None** | **Covered** (test_convergence_wiring.py, test_wiring_points_e2e.py, test_turnledger_lifecycle.py, test_gate_rollout_modes.py) |

---

## 1. Wiring-Detection Capability Assessment

### What EXISTS today

| Module | Capability | Status vs. 2026-03-18 |
|--------|-----------|----------------------|
| `wiring_gate.py` | AST-based gate: G-001 unwired callables, G-002 orphan modules, G-003 broken registries. 16-field frontmatter, 5 semantic checks, 7-section report. Mode-aware blocking (shadow/soft/full). | **NEW** — was entirely unimplemented |
| `wiring_config.py` | WiringConfig dataclass, 6 default registry patterns, WhitelistEntry model, load_whitelist with mode-aware validation | **NEW** |
| `wiring_analyzer.py` | AST-based ToolOrchestrator plugin: `ast_analyze_file()` drop-in + `ast_references_plugin()` enrichment. Populates FileAnalysis.references. | **NEW** — resolves "references field never populated" gap |
| `wiring_whitelist.yaml` | YAML suppression entries by finding type (unwired_callables, orphan_modules, unwired_registries) | **NEW** |
| `reachability.py` | AST call-chain reachability: BFS from entry points, cross-module import resolution, lazy import handling, TYPE_CHECKING exclusion | **NEW** |
| `dependency_graph.py` | 3-tier directed graph (Tier-A: imports, Tier-B: grep refs, Tier-C: co-occurrence) | Unchanged |
| `tool_orchestrator.py` | Import/export extraction with caching; analyzer injection seam; plugin registration | Enhanced — `references` now populated by `wiring_analyzer.py` |
| `dynamic_imports.py` | Detects JS/Python dynamic loading patterns, forces KEEP:monitor | Unchanged |
| `dead_code.py` | Negative wiring: exports with zero inbound Tier-A/B edges | Unchanged |
| `evidence_gate.py` | Blocks DELETE without zero-reference proof | Unchanged |

### Gap Summary (updated)

```
IMPLEMENTED:  AST resolution → Registry validation → Symbol-level tracing (via wiring_analyzer)
              → Orphan module detection → Call-chain reachability → TurnLedger budget integration
REMAINING:    DI container checking → Framework-aware hooks → Runtime path verification
              → No-op fallback detection (planned but not in current analyzers)
```

---

## 2. Wiring Gate Implementation Details

### Three Analyzers (G-001, G-002, G-003)

**G-001: Unwired Callable Analysis** (`analyze_unwired_callables`)
- Scans all Python files for `Optional[Callable]` constructor parameters with `None` defaults
- Cross-references all call sites for keyword argument matches
- Handles both `Optional[Callable]` and `Callable | None` annotation forms
- Severity: `critical`

**G-002: Orphan Module Analysis** (`analyze_orphan_modules`)
- Finds provider directories by naming convention (`steps/`, `handlers/`, `validators/`, `checks/`)
- Checks each module for inbound imports from outside provider directory
- Dual evidence rule: also checks FileAnalysis.references when AST plugin loaded
- Severity: `major`

**G-003: Registry Analysis** (`analyze_registries`)
- Matches module-level dict assignments against 6 registry patterns (`*REGISTRY`, `*DISPATCH`, `*HANDLERS`, `*ROUTER`, `*BUILDERS`, `PROGRAMMATIC_RUNNERS`)
- Resolves dict values as Name references (in-scope lookup) or string dotted paths
- Reports unresolvable entries as `unwired_registry`
- Severity: `critical`

### Gate Definition (WIRING_GATE)

```python
WIRING_GATE = GateCriteria(
    required_frontmatter_fields=[  # 16 fields
        "gate", "target_dir", "files_analyzed", "rollout_mode",
        "analysis_complete", "unwired_callable_count", "orphan_module_count",
        "unwired_registry_count", "critical_count", "major_count", "info_count",
        "total_findings", "blocking_findings", "whitelist_entries_applied",
        "files_skipped", "audit_artifacts_used",
    ],
    min_lines=10,
    enforcement_tier="STRICT",
    semantic_checks=[  # 5 checks
        analysis_complete_true,
        recognized_rollout_mode,
        finding_counts_consistent,       # total == uc + om + ur
        severity_summary_consistent,     # total == critical + major + info
        zero_blocking_findings_for_mode, # blocking_findings == 0
    ],
)
```

### Mode-Aware Blocking (blocking_for_mode)

| Mode | Blocking Behavior |
|------|------------------|
| `shadow` | Never blocks (blocking_count always 0) |
| `soft` | Blocks on unsuppressed critical findings only |
| `full` | Blocks on unsuppressed critical + major findings |

### Report Emission (emit_report)

Produces YAML frontmatter (16 fields) + 7 Markdown sections:
1. Summary
2. Unwired Optional Callable Injections
3. Orphan Modules / Symbols
4. Unregistered Dispatch Entries
5. Suppressions and Dynamic Retention
6. Recommended Remediation
7. Evidence and Limitations

---

## 3. Pipeline Integration Points

### Roadmap Pipeline

- **Gate registration**: `src/superclaude/cli/roadmap/gates.py:1087` — `("wiring-verification", WIRING_GATE)`
- **Pipeline step order**: `test-strategy` → `spec-fidelity` → `wiring-verification` → `deviation-analysis` → `remediate`
- **Step properties**: trailing position, zero retries

### Sprint Executor

- **Pre-analysis**: `ledger.debit_wiring(config.wiring_analysis_turns)` — debits turns before analysis
- **Analysis**: `run_wiring_analysis(wiring_config, source_dir)` — runs all 3 analyzers
- **Post-analysis**: `ledger.credit_wiring(turns, rate)` — credits turns in shadow/soft or successful remediation
- **Safeguards**: `run_wiring_safeguard_checks()` — zero-match warning, whitelist validation

### TurnLedger Integration

`SprintConfig` fields (from `src/superclaude/cli/sprint/models.py`):

| Field | Default | Purpose |
|-------|---------|---------|
| `wiring_gate_mode` | `"soft"` | Controls analysis behavior (off/shadow/soft/full) |
| `wiring_gate_scope` | `"task"` | Scope for resolve_gate_mode() |
| `wiring_analysis_turns` | `1` | Turns allocated per analysis |
| `wiring_gate_enabled` | `True` | Master enable flag |
| `wiring_gate_grace_period` | `0` | Grace period turns |

`TurnLedger` methods:

| Method | Purpose |
|--------|---------|
| `debit_wiring(turns)` | Debit turns before analysis; sets wiring_budget_exhausted if depleted |
| `credit_wiring(turns, rate)` | Credit turns back with floor-to-zero arithmetic |

### KPI Metrics (SprintKPI)

| Metric | Description |
|--------|-------------|
| `wiring_findings_total` | Total unsuppressed findings |
| `wiring_findings_by_type` | Dict breakdown by finding_type |
| `wiring_turns_used` | Turns consumed by wiring analysis |
| `wiring_turns_credited` | Turns credited back |
| `wiring_net_cost` | Computed: used - credited |
| `wiring_analyses_run` | Count of analysis executions |
| `wiring_remediations_attempted` | Count of remediation attempts |
| `whitelist_entries_applied` | Count of suppressed findings |

---

## 4. CLI Audit Module Inventory (Updated)

### Core Scanning / Profiling / Schema (Scanner stage)

| File | Purpose |
|------|---------|
| `profiler.py` | Phase-0 repository profiling: domain + risk tier assignment |
| `profile_generator.py` | Rich 8-field per-file profiles (imports, exports, size, complexity, age, churn, coupling, test_coverage) |
| `tool_orchestrator.py` | Shared static-analysis layer with content-hash caching, analyzer injection, and plugin registration |
| `scanner_schema.py` | Scanner output contracts: Phase-1 (5 required fields) + Phase-2 (8 profile fields) |
| `manifest_gate.py` | Coverage completeness gate before analysis begins |

### Classification / Evidence / Escalation (Analyzer stage)

| File | Purpose |
|------|---------|
| `classification.py` | Core engine: v2 tier system (tier-1/tier-2) + 7 action types |
| `dependency_graph.py` | 3-tier directed dependency graph builder (Tier-A/B/C edges) |
| `dead_code.py` | Cross-boundary dead code candidate detection via missing inbound edges |
| `dynamic_imports.py` | Dynamic-import safety: detects patterns, forces KEEP:monitor |
| `duplication.py` | Structural similarity / duplication matrix with recommendations |
| `env_matrix.py` | Environment key drift detector (code vs `.env` files) |
| `credential_scanner.py` | Secret scanning with placeholder exclusion and redaction |
| `docs_audit.py` | Broken refs, staleness, coverage gaps, orphaned docs, style issues |

### Wiring Verification (NEW — post-2026-03-18)

| File | Purpose |
|------|---------|
| `wiring_gate.py` | AST-based wiring gate: G-001/G-002/G-003 analyzers, WiringReport, emit_report, WIRING_GATE, blocking_for_mode |
| `wiring_config.py` | WiringConfig dataclass, WhitelistEntry, load_whitelist with mode-aware validation |
| `wiring_analyzer.py` | AST-based ToolOrchestrator plugin: populates FileAnalysis.references field |
| `wiring_whitelist.yaml` | YAML suppression entries by finding type |
| `reachability.py` | AST call-chain reachability analyzer for manifest validation (FR-4.2) |

### Validation / Evidence Gates (Validator stage)

| File | Purpose |
|------|---------|
| `evidence_gate.py` | Blocks DELETE without zero-reference evidence, KEEP without reference evidence |
| `filetype_rules.py` | File-type-specific verification requirements (source/config/docs/test/binary) |
| `tiered_keep.py` | Graduated KEEP evidence: low=1 ref, medium=2, high=3 |
| `escalation.py` | Ambiguity escalation on low confidence / conflicting evidence / INVESTIGATE |
| `validation.py` | Pre-consolidation consistency: stratified 10% sample, re-runs classification |
| `spot_check.py` | Post-consolidation validation over `ConsolidatedFinding`s |
| `validation_output.py` | Formats validation results with calibration notes |
| `report_completeness.py` | Verifies report contains mandated sections and directory assessments |
| `anti_lazy.py` | Detects suspiciously uniform outputs (e.g., almost all KEEP) |

### Consolidation / Reporting (Consolidator stage)

| File | Purpose |
|------|---------|
| `consolidation.py` | Cross-phase dedup by `file_path`, highest-confidence-wins conflict resolution |
| `coverage.py` | Classification coverage tracking by tier |
| `dir_assessment.py` | Aggregates findings into directory-level assessment blocks |
| `report_depth.py` | Report rendering by depth: summary / standard / detailed |
| `report_limitations.py` | Known limitations/non-determinism section |
| `already_tracked.py` | ALREADY_TRACKED section for suppressed known issues |
| `artifact_emitter.py` | Emits coverage and validation JSON artifacts |

### Orchestration / Execution Control

| File | Purpose |
|------|---------|
| `batch_decomposer.py` | Monorepo-aware batch planner with segment isolation |
| `checkpoint.py` | Batch progress persistence and resume (atomic temp-file/rename) |
| `resume.py` | Resume-point detection and result merging for interrupted runs |
| `batch_retry.py` | Retry wrapper with minimum-viable-report fallback |
| `budget.py` | Token budget accounting with progressive degradation policy |
| `budget_caveat.py` | Caveats/variance for budget estimates |
| `dry_run.py` | Cost-estimation-only mode |
| `auto_config.py` | Cold-start config generation from repository profile |
| `known_issues.py` | Persistent known-issues registry with suppression, TTL, LRU eviction |
| `gitignore_checker.py` | Tracked files vs `.gitignore` drift detection |

---

## 5. Architecture Diagram (Updated)

```
                    SKILL.md (Behavioral Protocol)
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   Pass 1 Rules       Pass 2 Rules       Pass 3 Rules
        │                  │                  │
   ┌────▼────┐        ┌───▼────┐        ┌────▼─────┐
   │ scanner │        │analyzer│        │comparator│
   │ (Haiku) │        │(Sonnet)│        │ (Sonnet) │
   └────┬────┘        └───┬────┘        └────┬─────┘
        │                  │                  │
        └──────────┬───────┘──────────────────┘
                   │
            ┌──────▼──────┐
            │  validator  │  ← 10% spot-check, 4 checks
            │  (Sonnet)   │
            └──────┬──────┘
                   │
           ┌───────▼───────┐
           │ consolidator  │  ← merge + final report
           │   (Sonnet)    │
           └───────────────┘

   Python Library (cli/audit/) — Wiring-Related:
   ┌───────────────────────────────────────────────────────────┐
   │ dependency_graph.py   ← CORE WIRING (3-tier)             │
   │ tool_orchestrator.py  ← ANALYZER PLUGIN SEAM             │
   │ wiring_analyzer.py    ← AST PLUGIN (populates refs) ★NEW │
   │ dynamic_imports.py    ← DYNAMIC SAFETY                   │
   │ dead_code.py          ← NEGATIVE WIRING                  │
   │ evidence_gate.py      ← DELETE SAFETY GATE               │
   │ wiring_gate.py        ← AST WIRING GATE (G-001/2/3) ★NEW│
   │ wiring_config.py      ← CONFIG + WHITELIST           ★NEW│
   │ reachability.py       ← CALL-CHAIN REACHABILITY      ★NEW│
   └───────────────────────────────────────────────────────────┘

   Pipeline Integration:
   ┌───────────────────────────────────────────────────────────┐
   │ roadmap/gates.py      ← WIRING_GATE registered at #1087  │
   │ sprint/executor.py    ← debit → analyze → credit cycle   │
   │ sprint/models.py      ← TurnLedger.debit_wiring/credit   │
   │ sprint/kpi.py         ← SprintKPI wiring metrics         │
   └───────────────────────────────────────────────────────────┘
```

---

## 6. Test Coverage

### Roadmap Tests (`tests/roadmap/`)

| Test File | Coverage Area |
|-----------|--------------|
| `test_convergence_wiring.py` | Convergence executor wiring integration |
| `test_eval_gate_rejection.py` | Gate rejection using WIRING_GATE |
| `test_eval_gate_ordering.py` | Wiring gate ordering after spec-fidelity |

### v3.3 Tests (`tests/v3.3/`)

| Test File | Coverage Area |
|-----------|--------------|
| `test_wiring_points_e2e.py` | End-to-end wiring verification points |
| `test_turnledger_lifecycle.py` | TurnLedger debit → analysis → credit lifecycle |
| `test_gate_rollout_modes.py` | Gate rollout mode behavior (shadow/soft/full) |
| `test_reachability_eval.py` | Reachability analyzer evaluation |
| `wiring_manifest.yaml` | Manifest test fixture |
| `wiring_manifest_schema.yaml` | Manifest schema validation fixture |

---

## 7. Remaining Gaps and Recommendations

### Resolved (since 2026-03-18)

- ~~Build `wiring_gate.py`~~ — **Done**: 1077-line implementation with 3 analyzers
- ~~Extend `ToolOrchestrator` analyzer~~ — **Done**: `wiring_analyzer.py` AST plugin
- ~~Wire gate into `roadmap/gates.py`~~ — **Done**: registered at position after spec-fidelity
- ~~TurnLedger integration~~ — **Done**: debit/credit cycle in sprint executor

### Still Open

1. **DI container checking** — Current analyzers detect `Optional[Callable]` parameters but not general dependency injection containers (e.g., `inject`, `dependency_injector` patterns)
2. **Framework-aware hooks** — Framework lifecycle hooks (pytest plugins, Click decorators, entry points) are not recognized as wiring; may produce false-positive orphan findings
3. **No-op fallback detection** — The original spec mentioned detecting no-op fallbacks returning `0`/`True`/`PASS`; this is not implemented in any current analyzer
4. **Runtime path verification** — All analysis is static AST; no runtime trace integration

### No New Agents Required

All 5 existing agents cover the needed roles. Wiring verification is an **extension** of existing capabilities, not a new audit dimension.
