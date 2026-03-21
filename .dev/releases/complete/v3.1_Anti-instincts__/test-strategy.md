---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 3
work_milestones: 4
interleave_ratio: "1:1"
major_issue_policy: stop-and-fix
spec_source: anti-instincts-gate-unified.md
generated: "2026-03-20T13:46:59.914265+00:00"
generator: superclaude-roadmap-executor
---

# v3.1 Anti-Instinct Gate — Test Strategy

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

The roadmap defines 4 implementation phases (M1–M4) and 3 validation checkpoints (A, B, C). With HIGH complexity and a 1:1 interleave ratio, every work phase has a paired validation milestone.

| Validation Milestone | Roadmap Phase | Gate Name | Go/No-Go Criteria |
|---------------------|---------------|-----------|-------------------|
| **V1: Implementation Readiness** | After Phase 1 (M1) | Checkpoint A | All unit tests green; existing suite green; SC-006 latency < 1s; no signature/statelessness violations |
| **V2: Pipeline Integration** | After Phase 2 (M2) | Mid-checkpoint (new) | End-to-end roadmap pipeline completes with anti-instinct gate; SC-001 regression proven; audit artifact format correct |
| **V3: Rollout Readiness** | After Phase 3 (M3) | Checkpoint B | Sprint pipeline runs with `gate_rollout_mode=shadow`; SC-008 baseline established; all 4×2 mode/outcome combinations tested |
| **V4: Enforcement Readiness** | During Phase 4 (M4) | Checkpoint C | `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints; false positives reviewed; OQs closed |

---

## 2. Test Categories

### 2.1 Unit Tests (Phase 1)

Pure-function module tests. No I/O, no pipeline context. Real content fixtures, no mocks.

| Test File | Module Under Test | Key Scenarios |
|-----------|-------------------|---------------|
| `test_obligation_scanner.py` | `obligation_scanner.py` | 11 scaffold terms detected; cross-phase discharge matching with verb+component; `# obligation-exempt` parsing; code-block MEDIUM severity demotion; empty input; single-section fallback; cli-portify regression fixture |
| `test_integration_contracts.py` | `integration_contracts.py` | 7-category dispatch detection; 3-line context capture; sequential ID assignment; deduplication by evidence; verb-anchored wiring coverage; named mechanism matching (UPPER_SNAKE, PascalCase); false-coverage rejection (mention ≠ wiring task); cli-portify regression |
| `test_fingerprint.py` | `fingerprint.py` | Three-source extraction (backtick, def/class, ALL_CAPS); `_EXCLUDED_CONSTANTS` filtering; deduplication; coverage ratio calculation; threshold boundary (0.69 fail, 0.70 pass); empty-fingerprint passthrough; cli-portify regression |
| `test_spec_structural_audit.py` | `spec_structural_audit.py` | All 7 indicator counters; ratio comparison against `total_requirements`; warning-only behavior (no exception raised); threshold boundary (0.49 fail, 0.50 pass) |

**Total unit test count estimate**: 45–60 test cases across 4 files.

### 2.2 Integration Tests (Phase 2)

Pipeline-level tests that run the actual executor with the anti-instinct step wired in.

| Test File | Scope | Key Scenarios |
|-----------|-------|---------------|
| `test_anti_instinct_integration.py` | Roadmap pipeline end-to-end | Gate blocks on known-bad roadmap (cli-portify); gate passes on known-good roadmap; `anti-instinct-audit.md` output contains correct YAML frontmatter; structural audit emits warning without blocking; gate positioned between `merge` and `test-strategy` in step order; `_get_all_step_ids()` returns correct ordering |

### 2.3 Sprint Integration Tests (Phase 3)

| Test File | Scope | Key Scenarios |
|-----------|-------|---------------|
| `test_anti_instinct_sprint.py` | Sprint executor with rollout modes | 4 modes × pass/fail = 8 scenarios per rollout matrix; `off` mode: zero computation, no metrics; `shadow` mode: gate evaluates, metrics recorded, task unaffected; `soft` mode: credit on pass, `BUDGET_EXHAUSTED` on fail; `full` mode: credit on pass, `TaskResult.status=FAIL` on fail; `ledger=None` safety (all 4 modes); `ShadowGateMetrics.record()` invocation in shadow/soft/full; no interaction with `wiring_gate_mode`; anti-instinct and wiring-integrity independent evaluation (NFR-010) |

### 2.4 End-to-End / Acceptance Tests (Phase 2–4)

These are pipeline-invocation tests that produce real artifacts and are third-party verifiable.

| Test ID | Description | Acceptance Criterion |
|---------|-------------|---------------------|
| E2E-001 | Run full roadmap pipeline against cli-portify spec | `anti-instinct-audit.md` produced; all 3 semantic checks fail (known-bad input); gate blocks pipeline |
| E2E-002 | Run full roadmap pipeline against known-good spec | All 3 semantic checks pass; pipeline continues to `test-strategy` |
| E2E-003 | Run sprint with `gate_rollout_mode=shadow` against real task | `ShadowGateMetrics` contains recorded data point; task outcome unchanged |
| E2E-004 | Backward compatibility: full existing test suite passes | Zero test failures introduced |

### 2.5 Non-Functional Tests (Cross-cutting)

| NFR | Test Method | Phase |
|-----|-------------|-------|
| NFR-001 (zero LLM) | Static analysis: grep for LLM client imports in new modules; runtime assertion that no HTTP calls made | 1 |
| NFR-002 (latency < 1s) | Timing assertions around combined module invocation on cli-portify fixture | 1, 2 |
| NFR-004 (pure functions) | Verify no file I/O in module functions; all take `str` in, return dataclass out | 1 |
| NFR-007 (backward compat) | Run full existing test suite after each phase | 1, 2, 3 |
| NFR-008 (stateless) | Verify no module-level mutable state; consecutive calls with different inputs produce independent results | 1 |
| NFR-009 (signature invariant) | Assert `gate_passed()` signature unchanged via inspect module | 2 |
| NFR-010 (independent evaluation) | Run both anti-instinct and wiring-integrity gates; verify neither mutates shared input | 3 |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

**1:1** — HIGH complexity (0.72) with:
- Three independent regex engines that can silently produce false results
- Dual execution context (standalone roadmap vs sprint-invoked) with different failure semantics
- Shared-file modifications (`gates.py`, `executor.py`) with merge conflict risk
- Rollout mode matrix (4 modes × 2 outcomes × 2 ledger states = 16 combinations)

A 1:1 ratio ensures no phase advances without validated correctness, preventing compound errors where Phase 2 wiring masks Phase 1 detection bugs.

### Interleaving Schedule

```
Phase 1: Build modules ──┬── Unit tests (parallel within phase)
                         └── Checkpoint A validation
Phase 2: Wire pipeline ──┬── Integration tests
                         └── Mid-checkpoint validation (new)
Phase 3: Sprint wiring ──┬── Sprint integration tests
                         └── Checkpoint B validation
Phase 4: Shadow runs ────┬── E2E acceptance tests
                         └── Checkpoint C validation
```

**Within-phase parallelism** (Phase 1 only): All four modules are independent. Module implementation and its unit tests can proceed in parallel across modules:

```
[obligation_scanner.py + test_obligation_scanner.py]     ─┐
[integration_contracts.py + test_integration_contracts.py] ├─→ Checkpoint A
[fingerprint.py + test_fingerprint.py]                    │
[spec_structural_audit.py + test_spec_structural_audit.py]─┘
```

---

## 4. Risk-Based Test Prioritization

Tests ordered by risk severity and detection value:

### Priority 1 — CRITICAL (blocks release if missed)

| Risk | Test Focus | Why First |
|------|-----------|-----------|
| A-009 (mention ≠ coverage) | Verb-anchored wiring patterns in `test_integration_contracts.py`; false-coverage rejection tests | Core correctness — a false pass defeats the entire gate |
| A-002 (unparseable NL) | Boundary cases in obligation scanner: mixed formatting, non-standard headings, fallback parser | Silent false negatives make the gate useless |
| NFR-001 (zero LLM) | Static + runtime verification of no LLM calls | Architectural invariant — violation is a design failure |

### Priority 2 — HIGH (blocks phase advancement)

| Risk | Test Focus |
|------|-----------|
| A-008 (unvalidated thresholds) | Threshold boundary tests at 0.69/0.70 (fingerprint) and 0.49/0.50 (structural audit) |
| Merge conflict (gates.py) | Integration test verifying `ALL_GATES` ordering after insertion |
| NFR-009 (signature invariant) | `gate_passed()` signature assertion |
| SC-006 (latency) | Timing assertion: combined execution < 1s |

### Priority 3 — MEDIUM (blocks sprint integration)

| Risk | Test Focus |
|------|-----------|
| A-011 (TurnLedger None) | All ledger call paths with `ledger=None` |
| A-014 (SprintGatePolicy None) | Mode-matrix tests with policy absent |
| D-03/D-04 overlap | Independent evaluation test (NFR-010) |
| A-004 (non-vocabulary terms) | `# obligation-exempt` escape hatch; expandable vocabulary design |

### Priority 4 — LOW (backlog-safe)

| Risk | Test Focus |
|------|-----------|
| A-001 (no requirement IDs) | Fingerprint extraction without IDs |
| A-012 (default mode) | Assert `SprintConfig().gate_rollout_mode == "off"` |
| OQ-011 (regex/exclusion alignment) | Verify excluded constants cannot match the 4-char regex |

---

## 5. Acceptance Criteria per Milestone

### Checkpoint A: Implementation Readiness (after Phase 1)

| ID | Criterion | Evidence |
|----|-----------|----------|
| A.1 | All 4 module unit test files pass | `uv run pytest tests/roadmap/test_obligation_scanner.py tests/roadmap/test_integration_contracts.py tests/roadmap/test_fingerprint.py tests/roadmap/test_spec_structural_audit.py -v` — all green |
| A.2 | SC-002 satisfied | `test_obligation_scanner.py::test_cli_portify_regression` passes — detects "mocked steps" without discharge |
| A.3 | SC-003 satisfied | `test_integration_contracts.py::test_cli_portify_regression` passes — detects `PROGRAMMATIC_RUNNERS` without wiring |
| A.4 | SC-004 satisfied | `test_fingerprint.py::test_cli_portify_regression` passes — detects missing fingerprints |
| A.5 | SC-005 satisfied | `test_spec_structural_audit.py::test_inadequacy_flagged` passes |
| A.6 | SC-006 satisfied | Combined module latency < 1s (timing assertion in test) |
| A.7 | SC-007 satisfied | Full existing test suite passes: `uv run pytest` — zero failures |
| A.8 | NFR-001 verified | No LLM imports in new modules (grep verification) |
| A.9 | NFR-004 verified | All module functions are pure (no I/O, no side effects) |
| A.10 | NFR-008 verified | No module-level mutable state; consecutive calls independent |

**Gate decision**: ALL criteria must pass. Any MAJOR or CRITICAL failure → stop-and-fix before Phase 2.

### Mid-Checkpoint: Pipeline Integration (after Phase 2)

| ID | Criterion | Evidence |
|----|-----------|----------|
| B.1 | SC-001 satisfied | End-to-end pipeline: 3 semantic checks fail on cli-portify, pass on good input |
| B.2 | `anti-instinct-audit.md` correct | Output contains valid YAML frontmatter with all 3 fields; markdown report present |
| B.3 | Gate ordering correct | `_get_all_step_ids()` returns `anti-instinct` between `merge` and `test-strategy` |
| B.4 | Structural audit warning-only | Audit runs, logs warning, does not block pipeline |
| B.5 | SC-006 confirmed | Latency < 1s in pipeline context |
| B.6 | SC-007 confirmed | Existing tests still pass |
| B.7 | NFR-009 confirmed | `gate_passed()` signature unchanged |
| B.8 | Prompt blocks present | `INTEGRATION_ENUMERATION_BLOCK` and `INTEGRATION_WIRING_DIMENSION` in prompt output |

### Checkpoint B: Rollout Readiness (after Phase 3)

| ID | Criterion | Evidence |
|----|-----------|----------|
| C.1 | Rollout matrix complete | 8 mode×outcome tests pass (4 modes × pass/fail) |
| C.2 | None-safe ledger | All 4 modes function with `ledger=None` |
| C.3 | Shadow metrics recording | `ShadowGateMetrics.record()` called in shadow/soft/full modes |
| C.4 | SC-008 baseline | Shadow mode produces metrics data point on real sprint run |
| C.5 | SC-009 satisfied | No merge conflicts with TurnLedger (verified by clean merge) |
| C.6 | NFR-010 satisfied | Anti-instinct and wiring-integrity gates evaluated independently |
| C.7 | SC-007 confirmed | Existing tests still pass |
| C.8 | Default mode correct | `SprintConfig().gate_rollout_mode == "off"` |

### Checkpoint C: Enforcement Readiness (during Phase 4)

| ID | Criterion | Evidence |
|----|-----------|----------|
| D.1 | SC-008 satisfied | `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprint runs |
| D.2 | False positive rate acceptable | Documented review of all gate failures in shadow mode; false positive rate < 10% |
| D.3 | False negatives documented | All known misses catalogued with vocabulary/pattern expansion plan |
| D.4 | Thresholds calibrated | Fingerprint (0.7) and structural audit (0.5) thresholds validated or adjusted based on shadow data |
| D.5 | OQs resolved | OQ-002, OQ-008, OQ-007 closed with documented decisions |

---

## 6. Quality Gates Between Phases

### Gate Structure

Each gate is binary: **PASS** (all criteria met) or **FAIL** (any MAJOR/CRITICAL issue found).

```
Phase 1 ──→ [Checkpoint A] ──→ Phase 2 ──→ [Mid-Checkpoint] ──→ Phase 3 ──→ [Checkpoint B] ──→ Phase 4 ──→ [Checkpoint C]
               │                                │                                │                                │
               └─ FAIL → stop-and-fix           └─ FAIL → stop-and-fix          └─ FAIL → stop-and-fix           └─ FAIL → remain in shadow
```

### Gate Definitions

| Gate | Required Passes | Blocking Issues | Escape Hatch |
|------|----------------|-----------------|--------------|
| **Checkpoint A** | A.1–A.10 | Any unit test failure; latency > 1s; existing test breakage | None — must pass all |
| **Mid-Checkpoint** | B.1–B.8 | Gate ordering wrong; audit artifact malformed; signature changed | None — must pass all |
| **Checkpoint B** | C.1–C.8 | Any rollout mode test failure; None-safety failure; merge conflict | None — must pass all |
| **Checkpoint C** | D.1–D.5 | Pass rate < 0.90; unreviewed false positives | Extend shadow observation period (do not skip to enforcement) |

### Regression Policy

At every gate, the full existing test suite (`uv run pytest`) must pass with zero failures. This is SC-007 and is non-negotiable at every checkpoint.

### Stop-and-Fix Protocol

When a MAJOR or CRITICAL issue is found:

1. **Stop** — no new implementation work begins
2. **Classify** — assign severity per the issue classification table
3. **Fix** — implement fix with targeted test covering the failure
4. **Re-validate** — re-run the full checkpoint criteria, not just the failing test
5. **Document** — record the issue and fix in the phase validation report
6. **Resume** — only after all checkpoint criteria pass
