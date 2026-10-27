---
title: v3.0 Unified Audit Gating — Eval Suite Design
type: component-design
status: ready-for-execution
version: 1.0
date: 2026-03-19
eval_count: 168
mock_count: 0
priority_breakdown: "P0: 110, P1: 40, P2: 18 (deferred)"
---

# v3.0 Unified Audit Gating — Eval Suite Design

## 1. Architecture Overview

```
eval-runner.py (orchestrator)
├── Local Run (current branch v3.0-AuditGates)
│   ├── Run A: pytest -x --tb=short --junit-xml=local-A.xml
│   └── Run B: pytest -x --tb=short --junit-xml=local-B.xml
├── Global Run (master baseline via git worktree)
│   ├── Run A: pytest -x --tb=short --junit-xml=global-A.xml
│   └── Run B: pytest -x --tb=short --junit-xml=global-B.xml
└── Comparison Report
    ├── Pass/Fail delta
    ├── Duration delta
    ├── New test coverage (tests in local not in global)
    └── Regression detection (tests passing in global, failing in local)
```

### Design Principles
1. **Zero mocks** — every test exercises real implementation code
2. **Deterministic** — no network, no LLM, no randomness; identical runs produce identical results
3. **Parallel-safe** — all tests use `tmp_path` fixtures; no shared state
4. **A/B comparable** — JUnit XML output enables diff between local/global and run-to-run

## 2. Eval Inventory

### P0: Gate Rejection Fidelity
- **File**: `tests/roadmap/test_eval_gate_rejection.py`
- **Test count**: ~80
- **What it validates**: Every gate in the 13-gate pipeline correctly rejects malformed output through the composed `gate_passed()` path
- **Failure modes tested per gate**:
  - Missing each required frontmatter field individually
  - Below minimum line count
  - Empty file
  - Missing file (nonexistent path)
  - Each semantic check violation individually (STRICT tier only)
- **Specific gate coverage**:
  - Certify: missing per-finding table, missing data rows
  - Remediate: PENDING actionable findings
  - Wiring: invalid rollout mode, analysis_complete=false
  - Deviation: pre-approved IDs in fix roadmap, invalid routing ID format
  - Tier behavior: STANDARD skips semantic checks, STRICT runs them
- **Why not mocked**: Tests the real `gate_passed()` function with real file I/O via `tmp_path`

### P0: Finding Lifecycle Chain
- **File**: `tests/roadmap/test_eval_finding_lifecycle.py`
- **Test count**: ~30
- **What it validates**: Finding objects flow correctly across all 4 pipeline stages
- **Scenarios**:
  - A: Zero deviations → clean passthrough
  - B: SLIPs only → block at spec-fidelity → route through deviation → remediate → certify
  - C: Mixed SLIP+INTENTIONAL+PRE_APPROVED → only SLIPs enter remediation
  - D: AMBIGUOUS deviation → blocks deviation-analysis gate
  - E: Remediation budget exhaustion → FAILED is terminal, PENDING blocks
- **Data integrity checks**:
  - Finding.status transitions: PENDING→ACTIVE→FIXED/FAILED/SKIPPED
  - Finding.deviation_class preserved through lifecycle
  - Finding.source_layer preserved through status changes
  - Spec-fidelity consistency: tasklist_ready=true requires high=0 AND validation_complete=true
  - Deviation routing: slip_count must match routing_fix_roadmap ID count
  - Deviation routing: total_analyzed must equal sum of categories

### P1: Convergence Multi-Run Regression
- **File**: `tests/roadmap/test_eval_convergence_multirun.py`
- **Test count**: ~14
- **What it validates**: DeviationRegistry correctly detects structural regressions across multiple runs
- **Sequence tested**: Run 1 (baseline) → Run 2 (improvement) → Run 3 (regression)
- **Key invariants**:
  - Structural HIGH increase = regression
  - Semantic HIGH increase = NOT regression (informational only)
  - Registry persistence survives save/reload
  - Spec hash change resets registry
  - Corrupted JSON creates fresh registry
  - Stable IDs are deterministic (SHA256-based, 16 chars, hex)
  - Debate verdicts can downgrade severity

### P1: Gate Ordering Invariants
- **File**: `tests/roadmap/test_eval_gate_ordering.py`
- **Test count**: ~17
- **What it validates**: `_build_steps()` structural properties
- **Ordering invariants**:
  - 10 total steps (extract + 2 parallel generate + 7 sequential)
  - Extract first, generate parallel, then diff→debate→score→merge→test-strategy→spec-fidelity→wiring
  - spec-fidelity after test-strategy (FR-008)
  - wiring after spec-fidelity
- **Dependency invariants**:
  - Each step's `inputs` reference prior step outputs
  - Generate steps input extraction output
  - Diff inputs both roadmaps
  - Wiring inputs merge + spec-fidelity outputs
- **Gate invariants**:
  - All steps have gates (except convergence-mode spec-fidelity)
  - All STRICT gates have semantic checks
  - Wiring has TRAILING gate mode and 0 retries
  - All output files are unique

### P1: Wiring Multi-File Fixtures
- **File**: `tests/audit/test_eval_wiring_multifile.py`
- **Test count**: ~9
- **What it validates**: Wiring analyzer against real multi-file Python projects
- **Fixture projects**:
  - Clean (0 expected unwired callables)
  - Known-issues (planted: unwired callables, orphan module, broken registry)
  - Edge-cases (aliased imports, inheritance, kwargs passthrough)
- **Report consistency**: category totals == total_findings

## 3. Execution Design

### Runner Script: `scripts/eval_runner.py`

```python
# Orchestrates 4 parallel pytest runs:
# - 2 local (current branch, same code, consistency check)
# - 2 global (master via worktree, baseline comparison)
#
# Produces JUnit XML + JSON summary for A/B comparison
```

### Run Modes

| Mode | What | How |
|------|------|-----|
| `local` | 2 runs on current branch | `pytest --junit-xml` × 2 |
| `global` | 2 runs on master worktree | `git worktree add` + `pytest --junit-xml` × 2 |
| `full` | All 4 runs + comparison | Both modes + diff report |

### Consistency Validation
- Two local runs must produce **identical** pass/fail results
- Duration variance should be < 20% between runs
- Any non-determinism (flaky test) is a P0 bug

### A/B Comparison Output
```
v3.0 Eval Results — 2026-03-19
================================
Local (v3.0-AuditGates): 168 passed / 0 failed
Global (master):          N/A (new tests) or M passed / N failed

New Coverage (local only):
  - test_eval_gate_rejection: 80 tests (NEW)
  - test_eval_finding_lifecycle: 30 tests (NEW)
  - test_eval_convergence_multirun: 14 tests (NEW)
  - test_eval_gate_ordering: 17 tests (NEW)
  - test_eval_wiring_multifile: 9 tests (NEW — partially applicable to master)

Regressions (pass→fail): 0
Improvements (fail→pass): 0
Duration: local 0.24s, global N/A
```

## 4. Parallel Execution Strategy

### pytest-xdist Compatibility
All tests use `tmp_path` (pytest's per-test temp dir), so they are safe for `-n auto`:
```bash
uv run pytest tests/roadmap/test_eval_*.py tests/audit/test_eval_*.py -n auto
```

### Agent Orchestration (via /sc:spawn)
```
Spawn 4 agents:
  Agent 1: local run A  — pytest eval files --junit-xml=results/local-A.xml
  Agent 2: local run B  — pytest eval files --junit-xml=results/local-B.xml
  Agent 3: global run A — worktree master, pytest eval files --junit-xml=results/global-A.xml
  Agent 4: global run B — worktree master, pytest eval files --junit-xml=results/global-B.xml
```

## 5. Success Criteria

| Metric | Threshold |
|--------|-----------|
| All evals pass | 168/168 |
| Zero mocks | `grep -r mock` returns 0 hits |
| Run-to-run consistency | Local A == Local B (identical pass/fail) |
| Duration | < 1 second total |
| Coverage gap filled | 5 new eval dimensions not in prior 1724 tests |

## 6. Files Modified/Created

### Created (eval tests)
- `tests/roadmap/test_eval_gate_rejection.py` — P0 gate rejection
- `tests/roadmap/test_eval_finding_lifecycle.py` — P0 finding lifecycle
- `tests/roadmap/test_eval_convergence_multirun.py` — P1 convergence
- `tests/roadmap/test_eval_gate_ordering.py` — P1 gate ordering
- `tests/audit/test_eval_wiring_multifile.py` — P1 wiring multifile

### Created (infrastructure)
- `scripts/eval_runner.py` — orchestrator for local+global parallel runs
- `.dev/releases/current/v3.0_unified-audit-gating/eval-design.md` — this document

### Not Modified
- Zero changes to source code under `src/`
- Zero changes to existing tests
- Zero changes to CI configuration
