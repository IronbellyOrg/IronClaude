

---
validation_milestones: 5
interleave_ratio: '1:1'
---

# Test Strategy — Preflight Executor (v2.25.5)

## 1. Validation Milestones Mapped to Roadmap Phases

### VM-1: Data Model & Parsing (Phase 1)
**Gate:** All dataclass extensions and parser changes round-trip correctly.

| Test ID | Category | What to Test | Acceptance Criteria |
|---------|----------|-------------|---------------------|
| T-1.1 | Unit | `Phase.execution_mode` defaults to `"claude"` | Field present, default correct |
| T-1.2 | Unit | `discover_phases()` reads `Execution Mode` column (claude/python/skip) | Case-insensitive parse, correct assignment |
| T-1.3 | Unit | `discover_phases()` raises `ClickException` on unrecognized mode | `"hybrid"` → exception with actionable message |
| T-1.4 | Unit | `discover_phases()` defaults to `"claude"` when column absent | Existing tasklists unchanged |
| T-1.5 | Unit | `TaskEntry.command` extraction — empty, simple, pipes, quotes | Verbatim preservation, backtick stripping |
| T-1.6 | Unit | `TaskEntry.classifier` extraction | Correct metadata read from `\| Classifier \|` |
| T-1.7 | Unit | `PhaseStatus.PREFLIGHT_PASS` — `is_success=True`, `is_failure=False` | Enum behaves correctly |
| T-1.8 | Unit | Python-mode task with empty command raises `ClickException` | Fail-fast at parse time |
| T-1.9 | Unit | Round-trip: write tasklist-index.md with modes → parse → verify | All fields survive round-trip |

**Quality Gate:** 9/9 tests pass. No changes to `_determine_phase_status()`.

---

### VM-2: Classifier Registry (Phase 2)
**Gate:** Registry loads, built-in classifier returns correct labels, errors handled.

| Test ID | Category | What to Test | Acceptance Criteria |
|---------|----------|-------------|---------------------|
| T-2.1 | Unit | `empirical_gate_v1(0, "ok", "")` → `"pass"` | Correct classification |
| T-2.2 | Unit | `empirical_gate_v1(1, "", "error")` → `"fail"` | Correct classification |
| T-2.3 | Unit | `CLASSIFIERS["nonexistent"]` → `KeyError` | Fail-closed on missing classifier |
| T-2.4 | Unit | Classifier that raises `RuntimeError` → caught, logged WARNING, returns `"error"` | Exception isolation verified |

**Quality Gate:** 4/4 tests pass. VM-1 and VM-2 are independent — run in parallel.

---

### VM-3: Preflight Executor & Artifacts (Phase 3)
**Gate:** Commands execute, evidence files written, result files parseable by existing code.

| Test ID | Category | What to Test | Acceptance Criteria |
|---------|----------|-------------|---------------------|
| T-3.1 | Integration | `execute_preflight_phases()` runs `echo hello`, captures stdout | stdout contains `"hello"`, exit_code=0 |
| T-3.2 | Integration | Command exceeding 120s timeout | `subprocess.TimeoutExpired` caught, task marked FAIL |
| T-3.3 | Integration | Evidence file written to `artifacts/<task_id>/evidence.md` | File exists, contains command/exit_code/stdout/stderr/duration/classification |
| T-3.4 | Unit | stdout truncated at 10KB, stderr at 2KB | Oversized output truncated with marker |
| T-3.5 | Integration | Result file via `AggregatedPhaseReport.to_markdown()` includes `source: preflight` | YAML frontmatter correct |
| T-3.6 | **Compatibility** | Preflight result file → `_determine_phase_status()` returns correct status | Same parse behavior as Claude-origin files |
| T-3.7 | **Compatibility** | Claude-origin fixture → `_determine_phase_status()` unchanged | Regression guard |
| T-3.8 | Integration | Failing command → `EXIT_RECOMMENDATION: HALT` in result | Halt propagation correct |

**Quality Gate:** 8/8 tests pass. T-3.6 and T-3.7 use a **shared compatibility fixture** (RISK-001 mitigation).

---

### VM-4: Sprint Integration & Skip Mode (Phase 4)
**Gate:** Mixed-mode sprint produces correct combined results; skip works; no regression.

| Test ID | Category | What to Test | Acceptance Criteria |
|---------|----------|-------------|---------------------|
| T-4.1 | Integration | Sprint with python + claude + skip phases | All three modes produce correct statuses |
| T-4.2 | Integration | Python-mode phases: zero `ClaudeProcess` instantiation | SC-002 validated — no API tokens |
| T-4.3 | Integration | Skip-mode phase → `PhaseStatus.SKIPPED`, no subprocess | No execution artifacts created |
| T-4.4 | Integration | Nested `claude --print -p "hello"` via subprocess | No deadlock, completes within timeout (SC-002) |
| T-4.5 | **Regression** | All-Claude tasklist (no python/skip) → identical behavior | Pre-feature baseline preserved |
| T-4.6 | Integration | Remove `execute_preflight_phases()` call → all-Claude works | SC-007 single-line rollback |
| T-4.7 | Integration | `--phases 2,3` filter excludes preflight Phase 1 | OQ-004: selective execution respected |

**Quality Gate:** 7/7 tests pass. T-4.5 is the critical regression gate.

---

### VM-5: Validation & Release (Phase 5)
**Gate:** All success criteria met, lint clean, sync verified.

| Test ID | Category | What to Test | Acceptance Criteria |
|---------|----------|-------------|---------------------|
| T-5.1 | E2E | 5 EXEMPT-tier tasks complete in <30s wall-clock | SC-001 performance threshold |
| T-5.2 | Acceptance | Full test suite: 14 unit + 8 integration pass | SC-004, SC-005 |
| T-5.3 | Acceptance | `make lint && make format` clean | No warnings |
| T-5.4 | Acceptance | `make sync-dev && make verify-sync` pass | Source-of-truth aligned |
| T-5.5 | Acceptance | All 8 success criteria (SC-001–SC-008) verified | Ship-ready |

**Quality Gate:** All criteria met → merge-eligible.

---

## 2. Test Categories

| Category | Count | Scope | Execution |
|----------|-------|-------|-----------|
| **Unit** | 14 | Dataclass fields, enum values, parser extraction, truncation, classifier logic | `uv run pytest -m unit` — fast, no I/O |
| **Integration** | 10 | Subprocess execution, file writing, result parsing, mixed-mode sprints | `uv run pytest -m integration` — requires filesystem |
| **Compatibility** | 2 | Shared fixture: preflight vs Claude result file parsing | Included in integration suite |
| **Regression** | 2 | All-Claude baseline, rollback verification | Included in integration suite |
| **E2E** | 1 | Performance benchmark with real EXEMPT-tier tasks | Manual or CI with timing assertions |
| **Acceptance** | 4 | Lint, sync, full suite, SC criteria | Release gate checks |

**Total: 33 test cases** (14 unit + 12 integration/compat/regression + 1 E2E + 4 acceptance + 2 shared fixtures).

---

## 3. Test-Implementation Interleaving Strategy

The strategy is **1:1 interleaving** — each phase ships with its tests before the next phase begins.

```
Phase 1 code → VM-1 tests (9) → GREEN ──┐
Phase 2 code → VM-2 tests (4) → GREEN ──┤  (parallel)
                                         ▼
Phase 3 code → VM-3 tests (8) → GREEN
                    ▼
Phase 4 code → VM-4 tests (7) → GREEN
                    ▼
Phase 5 validation → VM-5 checks (5) → SHIP
```

**Rules:**
- No phase starts until its predecessor's tests are green (except Phases 1 & 2, which are parallel).
- The compatibility fixture (T-3.6/T-3.7) is written **before** `preflight.py` implementation — test-first for the highest-risk contract.
- Regression test T-4.5 captures the baseline **before** any orchestration changes in Phase 4.

---

## 4. Risk-Based Test Prioritization

| Priority | Risk | Tests | Rationale |
|----------|------|-------|-----------|
| **P0 — Write first** | RISK-001: Result format drift | T-3.6, T-3.7 (compatibility fixture) | Highest severity; if this breaks, sprints halt. Test-first with shared fixture. |
| **P0 — Write first** | RISK-005: Orchestration regression | T-4.5 (all-Claude regression) | Capture baseline before touching `execute_sprint()`. |
| **P1 — With implementation** | RISK-003: Command quoting | T-1.5 (pipes, quotes, redirects) | Medium severity; easy to get wrong silently. |
| **P1 — With implementation** | FR-validation | T-1.8 (empty command fail-fast) | Catches misconfigurations at parse time. |
| **P2 — After implementation** | RISK-002: Environment mismatch | T-3.3 (evidence file completeness) | Diagnostic value; evidence enables debugging. |
| **P2 — After implementation** | RISK-004: Classifier bugs | T-2.1–T-2.4 | Low severity; isolated module. |
| **P3 — Release gate** | Performance | T-5.1 (<30s benchmark) | Non-functional; validate last. |

---

## 5. Acceptance Criteria per Milestone

### VM-1 Acceptance
- [ ] `Phase.execution_mode` field exists with correct default
- [ ] Three valid modes parsed case-insensitively; invalid modes raise exceptions
- [ ] `TaskEntry.command` preserves shell metacharacters verbatim
- [ ] Empty-command validation catches python-mode misconfigurations
- [ ] Existing tasklists without `Execution Mode` column parse unchanged

### VM-2 Acceptance
- [ ] `CLASSIFIERS` dict is importable and contains `empirical_gate_v1`
- [ ] Classifier exceptions are caught, logged, and treated as failure
- [ ] Missing classifier key raises `KeyError`

### VM-3 Acceptance
- [ ] Preflight executes real subprocesses and captures output
- [ ] Evidence artifacts contain all six required fields
- [ ] Result files parse identically to Claude-origin files via `_determine_phase_status()`
- [ ] Timeout enforcement works (120s default)
- [ ] SC-003, SC-008 validated

### VM-4 Acceptance
- [ ] Mixed python/claude/skip sprint produces correct combined outcome
- [ ] Zero `ClaudeProcess` instantiation for python-mode phases (SC-002)
- [ ] Skip phases produce `SKIPPED` status with no side effects
- [ ] All-Claude regression test passes (SC-007 prerequisite)
- [ ] Single-line rollback demonstrated (SC-007)

### VM-5 Acceptance
- [ ] SC-001 through SC-008 all pass
- [ ] `make lint && make format` clean
- [ ] `make sync-dev && make verify-sync` clean
- [ ] 14 unit + 8+ integration tests green

---

## 6. Quality Gates Between Phases

```
┌─────────┐     ┌─────────┐
│ Phase 1  │     │ Phase 2  │
│ Parsing  │     │ Classif. │
└────┬─────┘     └────┬─────┘
     │  GATE-1        │  GATE-2
     │  9/9 unit      │  4/4 unit
     │  pass           │  pass
     ▼                 ▼
┌──────────────────────────┐
│        Phase 3           │
│   Preflight Executor     │
│   (depends on 1 + 2)     │
└────────────┬─────────────┘
             │  GATE-3
             │  8/8 tests pass
             │  Compatibility fixture GREEN
             │  No changes to _determine_phase_status()
             ▼
┌──────────────────────────┐
│        Phase 4           │
│   Sprint Integration     │
└────────────┬─────────────┘
             │  GATE-4
             │  7/7 tests pass
             │  Regression baseline preserved
             │  Rollback verified
             ▼
┌──────────────────────────┐
│        Phase 5           │
│   Release Validation     │
└────────────┬─────────────┘
             │  GATE-5 (RELEASE)
             │  All SC-001–SC-008 pass
             │  Lint + sync clean
             │  <30s benchmark met
             ▼
          🚀 MERGE
```

**Gate enforcement rules:**
- **GATE-1/2:** Unit tests only. Fast. Must be green before Phase 3 starts.
- **GATE-3:** Compatibility fixture is the hard gate — if preflight results don't parse identically, block until fixed. Do **not** patch `_determine_phase_status()` as a workaround.
- **GATE-4:** Regression test (T-4.5) is a hard gate. If all-Claude behavior changes, block and investigate.
- **GATE-5:** Ship only when all success criteria are met. No partial releases.

---

## Test File Organization

```
tests/cli/sprint/
├── test_preflight.py          # All preflight tests (unit + integration)
├── fixtures/
│   ├── tasklist_with_modes.md # Tasklist fixture with execution modes
│   ├── claude_result.md       # Claude-origin result file (compatibility baseline)
│   └── preflight_result.md    # Preflight-origin result file (compatibility target)
```

**Markers used:**
- `@pytest.mark.unit` — no I/O, no subprocess
- `@pytest.mark.integration` — filesystem or subprocess required
- `@pytest.mark.regression` — baseline preservation checks

**Execution commands:**
```bash
uv run pytest tests/cli/sprint/test_preflight.py -m unit -v        # Fast feedback
uv run pytest tests/cli/sprint/test_preflight.py -m integration -v  # Full validation
uv run pytest tests/cli/sprint/test_preflight.py -v                 # Everything
```
