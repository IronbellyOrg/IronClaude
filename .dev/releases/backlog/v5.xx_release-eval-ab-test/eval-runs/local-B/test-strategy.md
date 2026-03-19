---
complexity_class: MEDIUM
validation_philosophy: continuous-parallel
validation_milestones: 7
work_milestones: 7
interleave_ratio: "1:2"
major_issue_policy: stop-and-fix
spec_source: eval-spec.md
generated: "2026-03-19T17:30:17.458638+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy: Progress Reporting & Dry-Run Gate Summary

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

With MEDIUM complexity and a 1:2 interleave ratio, validation milestones are inserted after every two work phases, plus dedicated validation at critical boundaries.

| Milestone | After Phase(s) | Validation Focus |
|-----------|---------------|------------------|
| **VM-0** | Phase 0 (Spec Closure) | Decision records exist and are internally consistent; schema approved |
| **VM-1** | Phase 1 (Foundation) | Data model correctness, atomic write safety, zero import-time I/O |
| **VM-2** | Phase 2 + 3 (Integration + Gate Summary) | End-to-end CLI integration, dry-run table completeness, parallel step handling |
| **VM-3** | Phase 4 (Advanced Reporting) | Deviation sub-entries, remediation metadata, wiring fields present and correct |
| **VM-4** | Phase 5 (Performance) | All 9 SC-* criteria pass with evidence; latency benchmarks; crash safety |
| **VM-5** | Phase 6 (Release Readiness) | Sync verification, representative run, regression sweep |
| **VM-6** | Post-merge | Smoke test on clean install; no regressions in existing `roadmap run` behavior |

---

## 2. Test Categories

### 2.1 Unit Tests
Scope: Isolated logic in `progress.py` and `gates.py` additions.

| Test | Requirement | Phase |
|------|-------------|-------|
| `StepProgress` serialization round-trip (JSON encode → decode → field equality) | FR-001, SC-002 | 1 |
| `PipelineProgress.to_json()` produces valid JSON for 0, 1, N entries | FR-003 | 1 |
| `PipelineProgress.from_json()` rejects malformed input | FR-003 | 1 |
| `GateCriteria.summary()` returns dict with 4 required keys | FR-012, SC-005 | 3 |
| `summary()` does not modify any existing `GateCriteria` attributes | NFR-005 | 3 |
| Import `progress.py` produces zero filesystem I/O | NFR-003, SC-009 | 1 |

### 2.2 Integration Tests
Scope: Cross-module wiring — callback integration, CLI option parsing, file I/O.

| Test | Requirement | Phase |
|------|-------------|-------|
| `--progress-file /tmp/test.json` accepted by Click; file created after run | FR-005, SC-003 | 2 |
| Omitting `--progress-file` defaults to `{output_dir}/progress.json` | FR-005, SC-004 | 2 |
| Path with nonexistent parent directory → fast failure before pipeline starts | FR-006 | 2 |
| Existing progress file is overwritten on fresh run | FR-007 | 2 |
| Parallel generate steps (A, B) produce independent entries with correct timing | FR-004, NFR-004 | 2 |
| Callback wiring: `progress_callback` invoked alongside `_print_step_complete` | FR-001, FR-002 | 2 |
| Deviation sub-entries appear nested under spec-fidelity parent | FR-009 | 4 |
| Remediation entry includes `trigger_reason` and `finding_count` only when remediation executes | FR-010 | 4 |
| Wiring entry includes `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode` | FR-011, SC-006 | 4 |

### 2.3 End-to-End (CLI) Tests
Scope: Real `superclaude roadmap run` invocations producing real artifacts.

| Test | Requirement | Phase |
|------|-------------|-------|
| Full pipeline run → `progress.json` valid JSON with entries for all executed steps | SC-001 | 5 |
| `--dry-run` → stdout contains Markdown table with 13 gate rows | FR-008, SC-005 | 3 |
| Conditional steps (remediate, certify) marked explicitly in dry-run table | FR-008 | 3 |
| Kill pipeline mid-execution → progress file on disk is valid JSON | NFR-002, SC-008 | 5 |
| Representative spec → progress file + dry-run output match expected structure | Release | 6 |

### 2.4 Performance / Benchmark Tests
Scope: NFR compliance under measurement.

| Test | Requirement | Phase |
|------|-------------|-------|
| 100 sequential `write_progress()` calls: p99 < 50ms | NFR-001, SC-007 | 5 |
| Atomic write under simulated crash (SIGKILL during write) → valid JSON | NFR-002, SC-008 | 5 |

### 2.5 Regression Tests
Scope: Existing behavior is preserved.

| Test | Scope | Phase |
|------|-------|-------|
| All existing `GateCriteria` consumers unchanged after `summary()` addition | RISK-003 | 5 |
| `superclaude roadmap run` without `--progress-file` behaves identically to pre-change | Release safety | 6 |
| Existing gate validation logic produces same verdicts | NFR-005 | 5 |

---

## 3. Test-Implementation Interleaving Strategy

### Ratio Justification

MEDIUM complexity (0.45) → **1:2 ratio** (one validation milestone per two work milestones).

This is appropriate because:
- The feature is integration-heavy but architecturally straightforward — no novel algorithms requiring exhaustive unit coverage at every step.
- The primary risk vectors (crash safety, parallel step handling, gate regression) are concentrated at integration boundaries, not within individual phases.
- Phase 2 and Phase 3 run in parallel, making a combined validation point natural and efficient.

### Interleaving Schedule

```
Phase 0 (spec closure)     → VM-0: schema + decision review
Phase 1 (foundation)       → VM-1: unit tests green
Phase 2 (integration)  ─┐
                         ├→ VM-2: combined integration + dry-run validation
Phase 3 (gate summary) ─┘
Phase 4 (advanced)         → VM-3: advanced reporting validation
Phase 5 (performance)      → VM-4: full SC-* sweep with evidence
Phase 6 (release)          → VM-5: release readiness gate
Post-merge                 → VM-6: smoke test
```

### Test-First vs Test-After by Phase

| Phase | Strategy | Rationale |
|-------|----------|-----------|
| 0 | Review-only | No code to test; validate decision artifacts |
| 1 | Test-first | Data model and atomic writer are well-specified; write tests from SC-002, SC-008, SC-009 before implementation |
| 2 | Test-after | Integration wiring depends on implementation details of callback shape |
| 3 | Test-first | Gate table output format is fully specified by FR-008; write expected-output tests first |
| 4 | Test-after | Sub-entry schemas depend on Phase 0 decisions; implement then validate |
| 5 | Benchmark-driven | Performance tests define the acceptance envelope; run and measure |
| 6 | Regression-only | No new code; verify existing + new behavior coexists |

---

## 4. Risk-Based Test Prioritization

Ordered by `severity × probability × blast_radius`:

| Priority | Risk | Tests | Rationale |
|----------|------|-------|-----------|
| **P0** | RISK-003: `summary()` breaks gate constants | Regression test all `GateCriteria` consumers; verify no signature changes | HIGH severity — gate breakage blocks entire pipeline |
| **P0** | RISK-004: Ambiguity propagation | VM-0 review gate; verify OQ-001/002/004 resolved before Phase 2 entry | MEDIUM severity × HIGH probability = highest expected impact |
| **P1** | RISK-002: Concurrent write corruption | Assert sequential callback invocation; test parallel step entries | MEDIUM severity — data corruption is hard to detect after the fact |
| **P1** | RISK-005: Resume/overwrite conflict | CLI test: fresh run overwrites, `--resume` appends (or is out-of-scope) | MEDIUM severity — silent data loss if wrong behavior |
| **P2** | RISK-001: Write latency | Benchmark at Phase 5; no action unless p99 > 50ms | LOW severity × VERY LOW probability |
| **P2** | Import path mismatch | Phase 1 import test: `from superclaude.cli.pipeline.models import StepResult` | LOW severity but easy to catch early |

---

## 5. Acceptance Criteria per Milestone

### VM-0: Specification Closure
- [ ] Written decision record for OQ-001 (deviation sub-entry schema shape)
- [ ] Written decision record for OQ-002 ("significant findings" = `severity == "HIGH"` or alternative)
- [ ] Written decision record for OQ-004 (resume appends vs overwrite-only vs deferred)
- [ ] Frozen progress JSON schema document approved
- [ ] No contradictions between decision records and extraction document

### VM-1: Foundation
- [ ] `StepProgress` round-trip serialization passes
- [ ] `PipelineProgress` handles 0, 1, N entries
- [ ] Atomic write test: `write_progress()` produces valid JSON
- [ ] `import superclaude.cli.roadmap.progress` creates zero files (SC-009)
- [ ] All Phase 1 tests green via `uv run pytest tests/roadmap/test_progress.py`

### VM-2: Integration + Gate Summary
- [ ] `superclaude roadmap run --progress-file /tmp/p.json` produces valid progress output
- [ ] Missing parent directory → exit code != 0, error message
- [ ] Default path resolves to `{output_dir}/progress.json`
- [ ] Parallel steps produce independent, correctly-timed entries
- [ ] `--dry-run` outputs Markdown table with exactly 13 rows (one per gate)
- [ ] Conditional steps (remediate, certify) are explicitly marked in table
- [ ] Table columns: Step, Gate Tier, Required Fields, Semantic Checks

### VM-3: Advanced Reporting
- [ ] Convergence loop iterations produce sub-entries under spec-fidelity parent
- [ ] Sub-entry count matches actual iteration count
- [ ] Remediation entry appears only when remediation executes
- [ ] Remediation entry contains `trigger_reason` and `finding_count`
- [ ] Certification entry references its associated remediation
- [ ] Wiring entry contains all 4 fields: `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode`

### VM-4: Performance & SC-* Sweep
- [ ] SC-001 through SC-009 all pass with evidence artifacts
- [ ] Write latency benchmark: p99 < 50ms over 100 iterations
- [ ] Crash simulation: SIGKILL during write → valid JSON on disk
- [ ] All existing `GateCriteria` consumers pass regression tests
- [ ] No existing gate verdicts changed by `summary()` addition

### VM-5: Release Readiness
- [ ] `make verify-sync` passes (src/ ↔ .claude/ consistent)
- [ ] Representative roadmap spec produces expected progress file structure
- [ ] Dry-run output matches expected format
- [ ] Full existing test suite green (`make test`)
- [ ] No new warnings or deprecations introduced

### VM-6: Post-Merge Smoke
- [ ] Clean install via `make dev` → `superclaude roadmap run` works without `--progress-file`
- [ ] Adding `--progress-file` produces output without errors
- [ ] `--dry-run` produces gate table
- [ ] No import errors or side effects

---

## 6. Quality Gates Between Phases

### Gate G0 → G1: Spec Closure → Foundation
**Type**: Manual review gate
**Criteria**:
- All 3 blocking OQs have written decision records
- JSON schema document exists and is internally consistent
- No unresolved contradictions between decisions and requirements

**Failure policy**: CRITICAL — cannot proceed to implementation without schema decisions.

### Gate G1 → G2: Foundation → Integration
**Type**: Automated test gate
**Criteria**:
- `uv run pytest tests/roadmap/test_progress.py` — all green
- SC-002 (5 required fields) verified
- SC-009 (zero import-time I/O) verified

**Failure policy**: MAJOR — foundation bugs will cascade into all later phases.

### Gate G2 → G4: Integration → Advanced Reporting
**Type**: Automated test gate + manual verification
**Criteria**:
- CLI option parsing tests pass
- End-to-end progress file generation works
- Parallel step entries are correct
- Phase 0 decisions for OQ-001 and OQ-002 still available (not invalidated)

**Failure policy**: MAJOR — advanced reporting builds directly on integration layer.

### Gate G3 → G5: Gate Summary → Release (via Phase 5)
**Type**: Automated test gate
**Criteria**:
- Dry-run table test passes with 13 gates
- `summary()` regression tests pass
- No existing gate behavior changes

**Failure policy**: MAJOR — gate regression blocks release.

### Gate G4 → G5: Advanced Reporting → Performance
**Type**: Automated test gate
**Criteria**:
- All 12 FRs have at least one passing test
- Deviation, remediation, and wiring entries structurally correct

**Failure policy**: MAJOR — cannot validate performance on incomplete feature.

### Gate G5 → G6: Performance → Release
**Type**: Automated benchmark + full sweep
**Criteria**:
- All 9 SC-* pass with evidence
- p99 write latency < 50ms
- Crash safety test passes
- Full regression suite green

**Failure policy**: CRITICAL — performance or safety failures block release.

### Gate G6 → Merge: Release → Production
**Type**: Manual + automated
**Criteria**:
- `make verify-sync` passes
- Representative run produces expected artifacts
- `make test` fully green
- Release notes prepared

**Failure policy**: CRITICAL — must pass before merge to master.

---

## 7. Test Execution Commands

```bash
# Phase 1 — Foundation tests
uv run pytest tests/roadmap/test_progress.py -v -k "serialization or atomic or import"

# Phase 2 — Integration tests
uv run pytest tests/roadmap/test_progress.py -v -k "cli or pipeline or parallel"

# Phase 3 — Gate summary tests
uv run pytest tests/roadmap/test_progress.py -v -k "dry_run or gate_table or summary"

# Phase 4 — Advanced reporting tests
uv run pytest tests/roadmap/test_progress.py -v -k "deviation or remediation or wiring"

# Phase 5 — Performance + full sweep
uv run pytest tests/roadmap/test_progress.py -v -k "benchmark or crash"
uv run pytest tests/roadmap/ -v  # full regression

# Phase 6 — Release readiness
make verify-sync && make test
```
