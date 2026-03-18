# Deep Analysis: Audit Infrastructure — Wiring Detection & Agent Extensibility

> Generated: 2026-03-18 | Target: `src/superclaude/cli/audit/`, `src/superclaude/skills/sc-cleanup-audit-protocol/`
> Branch: `v3.0-AuditGates`

---

## Executive Summary

The audit infrastructure is **surprisingly mature** — 30+ Python modules in `src/superclaude/cli/audit/` plus a full behavioral protocol in the skill. Wiring detection exists but is **heuristic/shallow**. Of the 5 audit agents, **all can be extended** — none need to be built from scratch. The `test-strategy` pipeline step failed due to **missing provenance frontmatter fields**.

---

## 1. Wiring-Detection Capability Assessment

### What EXISTS today

| Module | Capability | Limitation |
|--------|-----------|------------|
| `dependency_graph.py` | 3-tier directed graph (Tier-A: imports, Tier-B: grep refs, Tier-C: co-occurrence) | Line-based, not AST; no runtime path resolution |
| `tool_orchestrator.py` | Import/export extraction with caching; `AnalysisTool` injection seam | `references` field exists but **never populated** by default analyzer |
| `profile_generator.py` | Coupling metric (heuristic stem-matching) | Not true dependency coupling |
| `dynamic_imports.py` | Detects JS/Python dynamic loading patterns, forces KEEP:monitor | Pattern-matching only |
| `dead_code.py` | Negative wiring: finds exports with zero inbound Tier-A/B edges | Misses framework hooks, DI |
| `evidence_gate.py` | Blocks DELETE without zero-reference proof | No positive wiring validation |
| `env_matrix.py` | Cross-references `.env`-style files against code references | Key-name only, no value analysis |
| `filetype_rules.py` | Type-specific evidence requirements for configs/docs/tests/source | Category-level, not symbol-level |

### What does NOT exist (but is planned)

The backlog spec at `.dev/releases/backlog/v3.0_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md` describes an **AST-based wiring verification gate** that would detect:

- `STEP_REGISTRY` entries without importable step functions
- `Optional[Callable]` constructor params defaulting to `None` never explicitly provided
- Functions in `steps/` never imported by executors
- No-op fallbacks returning success codes (`0`, `True`, `PASS`)

**No source file `wiring_gate.py` exists anywhere under `src/`.** This is entirely unimplemented.

### Gap Summary

```
EXISTING:  Import discovery → Dependency graph → Dead code inference → Dynamic import safety
MISSING:   AST resolution → Symbol-level tracing → Registry validation → DI container checking
           → Framework-aware hooks → Runtime path verification
```

### Key Extension Points for Wiring

1. **`ToolOrchestrator` analyzer injection** (`tool_orchestrator.py`) — constructor accepts `analyzer: AnalysisTool | None`. Swap line-based default for AST-aware analyzer to populate the empty `references` field.
2. **`DependencyGraph` target resolution** (`dependency_graph.py`) — `_resolve_import_target()` currently uses path heuristics. Replace with actual module resolution.
3. **`dynamic-use-checklist.md`** (skill rules) — 5 dynamic patterns defined. Extend with reflection-based loading, DI containers, feature-flag gating.
4. **Classification pipeline** — composable gate chain (`evidence_gate` → `filetype_rules` → `tiered_keep` → `escalation` → `dynamic_imports`) naturally accepts a new wiring-verification gate.

---

## 2. Agent Extensibility Assessment

All 5 agents exist as `.md` definitions in both `src/superclaude/agents/` and `.claude/agents/`. They are behavioral specs for Claude subagents, not Python classes.

### Agent-by-Agent Analysis

| Agent | Model | Current Role | Extend or Build New? | Extension Strategy |
|-------|-------|-------------|---------------------|--------------------|
| **audit-scanner** | Haiku | Pass 1: fast triage (DELETE/REVIEW/KEEP) | **Extend** | Add wiring-aware signals via `ToolOrchestrator` analyzer injection. Surface broken imports and unresolved registrations during triage. |
| **audit-analyzer** | Sonnet | Pass 2: deep 8-field per-file profiles | **Extend** | The 8-field profile already includes "References" and "Verification notes". Add wiring-verification fields (registry consistency, import resolution) as profile extensions. |
| **audit-comparator** | Sonnet | Pass 3: cross-cutting duplication/sprawl | **Extend** | Already does cross-file comparison. Add "wiring consistency" comparison — e.g., does file A's registry match file B's implementation? |
| **audit-validator** | Sonnet | QA: 10% spot-check, 4 verification checks | **Extend** | Add Check 5: "Wiring Claim Verification" — confirm that stated import/registration relationships actually resolve. |
| **audit-consolidator** | Sonnet | Synthesis: merge batch reports, final report | **Extend** | Add "Wiring Health" rollup section to final report template. |

### What Must Be BUILT NEW

1. **`wiring_gate.py`** — AST-based gate evaluator (spec exists in backlog, no code exists)
2. **AST analyzer plugin** for `ToolOrchestrator` — to populate the empty `references` field with real symbol-level resolution
3. **Gate integration** — Wire the new gate into `src/superclaude/cli/roadmap/gates.py` alongside existing `SPEC_FIDELITY_GATE`

---

## 3. CLI Audit Module Inventory

### Core Scanning / Profiling / Schema (Scanner stage)

| File | Purpose |
|------|---------|
| `profiler.py` | Phase-0 repository profiling: domain + risk tier assignment |
| `profile_generator.py` | Rich 8-field per-file profiles (imports, exports, size, complexity, age, churn, coupling, test_coverage) |
| `tool_orchestrator.py` | Shared static-analysis layer with content-hash caching and analyzer injection |
| `scanner_schema.py` | Scanner output contracts: Phase-1 (5 required fields) + Phase-2 (8 profile fields) |
| `manifest_gate.py` | Coverage completeness gate before analysis begins |

### Classification / Evidence / Escalation (Analyzer stage)

| File | Purpose |
|------|---------|
| `classification.py` | Core engine: v2 tier system (tier-1/tier-2) + 7 action types (DELETE/KEEP/INVESTIGATE/REORGANIZE/MODIFY/ARCHIVE/FLAG) |
| `dependency_graph.py` | 3-tier directed dependency graph builder (Tier-A/B/C edges) |
| `dead_code.py` | Cross-boundary dead code candidate detection via missing inbound edges |
| `dynamic_imports.py` | Dynamic-import safety: detects patterns, forces KEEP:monitor |
| `duplication.py` | Structural similarity / duplication matrix with recommendations |
| `env_matrix.py` | Environment key drift detector (code vs `.env` files) |
| `credential_scanner.py` | Secret scanning with placeholder exclusion and redaction |
| `docs_audit.py` | Broken refs, staleness, coverage gaps, orphaned docs, style issues |

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

## 4. Skill Protocol Analysis

### Multi-Pass Architecture

The skill (`sc-cleanup-audit-protocol/SKILL.md`) defines a 5-phase orchestrated audit:

```
Phase 1: Discover  → enumerate files, build inventory, assign batches
Phase 2: Configure → parse args, load pass rules, init output dir
Phase 3: Orchestrate → spawn 7-8 concurrent agents per wave (fan-out)
Phase 4: Validate  → 10% spot-check, schema checks, regenerate failures
Phase 5: Report    → merge batch reports, synthesize final report (fan-in)
```

### 3-Pass Analysis Model

| Pass | Agent | Model | Question | Output |
|------|-------|-------|----------|--------|
| Pass 1: Surface | audit-scanner | Haiku | "Is this file junk?" | DELETE/REVIEW/KEEP |
| Pass 2: Structural | audit-analyzer | Sonnet | "Is this file correct, documented, well-placed?" | 8-field profiles |
| Pass 3: Cross-cutting | audit-comparator | Sonnet | "Does this duplicate/conflict with other files?" | 7-field profiles + duplication matrix |

### Wiring-Related Concepts in Protocol

The protocol addresses wiring under different names:
- **Dynamic loading checks** (`rules/dynamic-use-checklist.md`) — 5 patterns: env-based, string-built, plugin registries, glob/readdir, config-driven
- **Import chain tracing** — Serena MCP role for symbol-level understanding
- **Cross-reference verification** — 7 reference source categories checked
- **CI/runtime/build reference tracing** — part of structural audit

No explicit "wiring verification" pass or gate exists in the protocol.

---

## 5. Test-Strategy Pipeline Failure

### Roadmap Pipeline State

From `.dev/releases/current/v3.0_unified-audit-gating/.roadmap-state.json`:

| Step | Status | Attempts |
|------|--------|----------|
| extract | PASS | 1 |
| generate-opus-architect | PASS | 1 |
| generate-haiku-architect | PASS | 1 |
| diff | PASS | 1 |
| debate | PASS | 1 |
| score | PASS | 1 |
| merge | PASS | 2 |
| **test-strategy** | **FAIL** | **2** |

### Root Cause

**Gate requirements** (`src/superclaude/cli/roadmap/gates.py:763-774`):

```python
TEST_STRATEGY_GATE = GateCriteria(
    required_frontmatter_fields=[
        "spec_source",            # ← MISSING from output
        "generated",              # ← MISSING from output
        "generator",              # ← MISSING from output
        "complexity_class",       # ✓ present
        "validation_philosophy",  # ✓ present
        "validation_milestones",  # ✓ present
        "work_milestones",        # ✓ present
        "interleave_ratio",       # ✓ present
        "major_issue_policy",     # ✓ present
    ],
    enforcement_tier="STRICT",
)
```

**Actual frontmatter in `test-strategy.md`**:
```yaml
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 5
work_milestones: 5
interleave_ratio: "1:1"
major_issue_policy: stop-and-fix
```

The 3 provenance fields (`spec_source`, `generated`, `generator`) are missing. The executor has `_inject_test_strategy_provenance()` at `executor.py:159` that should inject these **post-subprocess**, but:
- The `.err` file is empty — no subprocess crash
- The gate evaluated **before** or **instead of** injection succeeding
- This is a **sequencing/post-processing bug** in the roadmap pipeline executor

### Fix Path

Either:
1. Ensure `_inject_test_strategy_provenance()` runs and completes **before** the gate evaluator fires
2. Or include the 3 provenance fields in the LLM prompt so the model generates them directly

---

## 6. Architecture Diagram

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
   ┌──────────────────────────────────────────────┐
   │ dependency_graph.py  ← CORE WIRING (3-tier)  │
   │ tool_orchestrator.py ← ANALYZER PLUGIN SEAM  │
   │ dynamic_imports.py   ← DYNAMIC SAFETY        │
   │ dead_code.py         ← NEGATIVE WIRING       │
   │ evidence_gate.py     ← DELETE SAFETY GATE     │
   │ [wiring_gate.py]     ← DOES NOT EXIST YET    │
   └──────────────────────────────────────────────┘
```

---

## 7. Recommendations

### Priority 1 — Fix test-strategy pipeline failure
- Debug `_inject_test_strategy_provenance()` sequencing in `executor.py`
- Ensure provenance injection completes before gate evaluation

### Priority 2 — Build `wiring_gate.py`
- Use existing backlog spec as requirements
- AST-based analysis for registry/dispatch table validation
- Plug into gate chain in `roadmap/gates.py`

### Priority 3 — Extend `ToolOrchestrator` analyzer
- Implement AST analyzer plugin to populate `references` field
- Feed richer data into `dependency_graph.py` Tier-A edges

### Priority 4 — Extend agent profiles
- Scanner: add broken-import signals to Pass 1 triage
- Analyzer: add wiring-verification fields to 8-field profile
- Validator: add Check 5 (Wiring Claim Verification)
- Consolidator: add Wiring Health rollup section

### No New Agents Required
All 5 existing agents cover the needed roles. Wiring verification is an **extension** of existing capabilities, not a new audit dimension.
