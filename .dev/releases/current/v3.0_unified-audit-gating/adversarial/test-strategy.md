---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 6
work_milestones: 6
interleave_ratio: "1:1"
major_issue_policy: stop-and-fix
spec_source: merged-spec.md
generated: "2026-03-18T17:43:17.308285+00:00"
generator: superclaude-roadmap-executor
---

# Wiring Verification Gate v3.0 — Test Strategy

## Issue Classification

| Severity | Action | Gate Impact |
|----------|--------|-------------|
| CRITICAL | Stop-and-fix immediately | Blocks current phase |
| MAJOR | Stop-and-fix before next phase | Blocks next phase |
| MINOR | Track and fix in next sprint | No gate impact |
| COSMETIC | Backlog | No gate impact |

---

## 1. Validation Milestones Mapped to Roadmap Phases

| Validation Milestone | Roadmap Phase | What Is Validated | Entry Condition |
|---------------------|---------------|-------------------|-----------------|
| **VM-0** | Phase 0: Architecture Confirmation | All 5 confirmation items resolved; T06 go/no-go decided; `provider_dir_names` confirmed | Branch created, spec reviewed |
| **VM-1** | Phase 1: Core Analysis Engine (T01–T04) | `WiringConfig`, `WiringReport`, `run_wiring_analysis()`, `emit_report()` produce correct output against fixtures | VM-0 green |
| **VM-2** | Phase 2: Gate Definition (T05–T06) | `WIRING_GATE` passes `gate_passed()`, all 5 semantic checks correct independently | VM-1 green |
| **VM-3** | Phase 3: Roadmap Integration (T07–T08) | Full roadmap pipeline completes with wiring-verification step in shadow/TRAILING mode | VM-2 green |
| **VM-4** | Phase 4: Sprint Integration (T09) | Sprint executor logs wiring findings without affecting task status; per-task artifacts emitted | VM-1 green (parallel track) |
| **VM-5** | Phase 5: Agent Extensions (T10–T12) | Cleanup-audit produces wiring-aware 9-field profiles; existing audit fixtures still pass | VM-1 green |
| **VM-6** | Phase 6: Testing + Calibration (T13–T15) | ≥90% coverage, all SC-001–SC-014 pass, pre-activation checklist green | VM-1 through VM-5 green |

---

## 2. Test Categories

### 2.1 Unit Tests (Target: 20+ tests)

| Area | Tests | SC Criteria | Phase |
|------|-------|-------------|-------|
| `WiringConfig` validation + whitelist loading | 3 tests: valid config, malformed whitelist warning, missing file handling | — | 1 |
| `WiringFinding` construction + severity | 2 tests: all finding types, severity assignment | SC-001, SC-002, SC-003 | 1 |
| `WiringReport` derived properties | 3 tests: `total_findings` derivation, `blocking_for_mode()` for shadow/soft/full | SC-014 | 1 |
| Unwired callable detection | 3 tests: single unwired param, multiple params, whitelisted exclusion | SC-001, SC-007 | 1 |
| Orphan module detection | 3 tests: true orphan, used module, excluded files (`__init__.py`, `test_*.py`) | SC-002 | 1 |
| Registry detection | 3 tests: unresolvable entry, unused registry, explicit None mapping | SC-003 | 1 |
| `emit_report()` output | 2 tests: YAML frontmatter validity (15 fields), 7 body sections present | SC-004 | 1 |
| Semantic checks (5 functions) | 5 tests: one per check, positive and negative cases | SC-005, SC-014 | 2 |
| `_extract_frontmatter_values()` | 2 tests: valid extraction, malformed frontmatter | — | 2 |
| AST parse error handling | 1 test: unparseable file logged and skipped, counted in `files_skipped` | — | 1 |
| Determinism | 1 test: same input → identical output across 3 runs | NFR-003 | 1 |
| Performance benchmark | 1 test: 50-file fixture completes in < 5s | SC-008, NFR-001 | 6 |
| ToolOrchestrator plugin (if T06 kept) | 2 tests: `FileAnalysis.references` populated, `has_dispatch_registry` set | SC-013 | 2 |

### 2.2 Integration Tests (Target: 3+ tests)

| Test | Description | SC Criteria | Phase |
|------|-------------|-------------|-------|
| Full roadmap pipeline with shadow gate | End-to-end roadmap run; wiring-verification step executes as TRAILING; pipeline completes successfully | SC-005, SC-006 | 3 |
| Sprint post-task hook | Sprint task with wiring analysis; shadow mode logs but does not alter task status | SC-006 | 4 |
| `gate_passed()` with `WIRING_GATE` | Feed valid and invalid reports to `gate_passed(report_path, WIRING_GATE)`; verify correct `(bool, str|None)` | SC-005 | 2 |
| Pre-activation sanity check | Run against codebase with >50 files; verify >0 findings or warning emitted | SC-010 | 6 |

### 2.3 Agent Tests

| Test | Description | SC Criteria | Phase |
|------|-------------|-------------|-------|
| audit-scanner `REVIEW:wiring` | Run scanner on fixture with wiring indicators; verify classification | SC-011 | 5 |
| audit-analyzer 9-field profile | Run analyzer on fixture; verify 9th "Wiring path" field present and populated | SC-012 | 5 |
| audit-validator Check 5 | Run validator with wiring claims; verify verification logic | — | 5 |

### 2.4 Retrospective / Acceptance Tests

| Test | Description | SC Criteria | Phase |
|------|-------------|-------------|-------|
| cli-portify no-op detection | Run analysis against known cli-portify executor fixtures; verify ≥1 finding | SC-009 | 6 |
| `provider_dir_names` validation | Confirm configured names match actual repository directory structure | FR-041 | 6 |

---

## 3. Test-Implementation Interleaving Strategy

**Ratio**: 1:1 (HIGH complexity → one validation milestone per work milestone)

**Justification**: This release touches the roadmap executor hot path (T08), introduces a new gate type into a statically-wired gate substrate, and integrates across three execution surfaces (roadmap, sprint, audit agents). The 0.82 complexity score with HIGH integration surface (0.90) and coordination risk (0.80) demands validation at every phase boundary to catch regressions before they compound.

### Interleaving Schedule

```
Phase 0 (work) → VM-0 (validate) → 
Phase 1 (work) → VM-1 (validate: unit tests for T01–T04 run) →
Phase 2 (work) → VM-2 (validate: semantic check tests, gate_passed integration test) →
Phase 3 (work) → VM-3 (validate: pipeline integration test) →
Phase 4 (work) → VM-4 (validate: sprint integration test) →
Phase 5 (work) → VM-5 (validate: agent fixture tests) →
Phase 6 (work) → VM-6 (validate: coverage gate, full SC criteria sweep, benchmark)
```

**Parallel testing track**: Unit tests for T01–T04 (Phase 1 code) begin as soon as Phase 1 completes and continue running alongside Phases 2–5. This means test authoring for the core engine is not blocked by downstream integration work.

**Critical constraint**: VM-3 (roadmap integration) is the highest-risk gate. T08 modifies the executor hot path. If VM-3 reveals issues, stop-and-fix before proceeding to Phase 4 or 5.

---

## 4. Risk-Based Test Prioritization

### Priority 1 — Test First (Blocks everything downstream)

| Risk | Test Focus | Why |
|------|-----------|-----|
| RISK-005: `provider_dir_names` misconfiguration | Sanity check test: >50 files → >0 findings | Misconfigured directory names silently produce zero findings — complete gate failure |
| T08 executor hot path | Integration test: roadmap completes with wiring step | Regression here breaks all roadmap runs, not just wiring |
| NFR-005: Substrate signature preservation | Import/signature verification test | Any substrate change breaks all existing gates |

### Priority 2 — Test Early (High likelihood risks)

| Risk | Test Focus | Why |
|------|-----------|-----|
| RISK-001: False positives from Optional[Callable] | Whitelist exclusion tests + FPR measurement | High likelihood; must validate whitelist works before shadow |
| RISK-006: Import alias FPR | Fixture with re-exports; measure FPR baseline | 30–70% FPR is acceptable in shadow but must be measured |
| NFR-007: Layering violation | Static import analysis (no `pipeline/*` → `audit/*` imports) | Layering violations are silent and compound |

### Priority 3 — Test Alongside (Medium risks)

| Risk | Test Focus | Why |
|------|-----------|-----|
| RISK-007: Agent regression | Existing audit fixtures still pass after extensions | Additive-only constraint must be verified |
| RISK-004: Sprint performance | Benchmark: < 2s for post-task hook | Low likelihood but measurable |
| NFR-003: Determinism | Same-input reproducibility test | Core architectural requirement |

### Priority 4 — Test Last (Low risks, low impact)

| Risk | Test Focus | Why |
|------|-----------|-----|
| RISK-002: AST parse errors | Graceful degradation on malformed Python | Low impact — logged and skipped |
| RISK-008: `resolve_gate_mode()` override | Explicit `gate_mode` on Step construction | Low likelihood with explicit mode |

---

## 5. Acceptance Criteria per Milestone

### VM-0: Architecture Confirmation
- [ ] All 5 confirmation items have documented resolutions
- [ ] `provider_dir_names` default set confirmed against actual codebase directories
- [ ] T06 go/no-go decision made with evidence (ToolOrchestrator source inspected)
- [ ] No CRITICAL or MAJOR issues open

### VM-1: Core Analysis Engine
- [ ] `run_wiring_analysis()` returns correct `WiringReport` for ≥3 test fixtures (unwired callable, orphan module, bad registry)
- [ ] `emit_report()` produces valid YAML frontmatter with all 15 fields
- [ ] Report body contains all 7 sections in correct order
- [ ] `WiringReport.blocking_for_mode()` returns correct counts for all 3 modes
- [ ] Whitelist exclusion works; `whitelist_entries_applied` accurate
- [ ] AST parse errors handled gracefully (no crash, `files_skipped` incremented)
- [ ] Determinism verified: identical output across 3 runs
- [ ] ≥12 unit tests passing

### VM-2: Gate Definition + Semantic Checks
- [ ] `WIRING_GATE` instantiated as `GateCriteria` with correct fields
- [ ] All 5 semantic checks pass on valid report content
- [ ] All 5 semantic checks fail on crafted invalid content
- [ ] `gate_passed(report_path, WIRING_GATE)` returns `(True, None)` for valid shadow report
- [ ] `gate_passed()` returns `(False, reason)` for report with blocking findings in full mode
- [ ] `_extract_frontmatter_values()` correctly parses frontmatter
- [ ] No imports from `pipeline/*` into `audit/*` (layering verified)
- [ ] ≥17 unit tests passing

### VM-3: Roadmap Integration
- [ ] `"wiring-verification"` present in `_get_all_step_ids()` between `"spec-fidelity"` and `"remediate"`
- [ ] `WIRING_GATE` present in `ALL_GATES`
- [ ] `build_wiring_verification_prompt()` returns empty string
- [ ] Step constructed with `retry_limit=0` and `gate_mode=GateMode.TRAILING`
- [ ] `roadmap_run_step()` special-cases `"wiring-verification"` for deterministic execution
- [ ] Full roadmap pipeline completes without error with shadow gate active
- [ ] Existing roadmap steps unaffected (regression check)
- [ ] ≥1 integration test passing

### VM-4: Sprint Integration
- [ ] `SprintConfig` has `wiring_gate_mode` field with default `"shadow"`
- [ ] Post-task hook runs analysis and emits per-task report artifact
- [ ] Shadow mode: findings logged, task status unchanged
- [ ] Analysis completes in < 2s (NFR-002)
- [ ] `wiring_gate_mode: "off"` disables hook entirely
- [ ] ≥1 integration test passing

### VM-5: Agent Extensions
- [ ] audit-scanner classifies files with wiring indicators as `REVIEW:wiring`
- [ ] audit-analyzer produces 9-field profile with "Wiring path" field
- [ ] audit-validator Check 5 verifies wiring claims
- [ ] All existing audit fixtures produce identical results (no regression)
- [ ] Changes are additive only — no existing rules or tools modified

### VM-6: Full Validation + Calibration
- [ ] `wiring_gate.py` line coverage ≥ 90%
- [ ] `wiring_analyzer.py` line coverage ≥ 90% (if T06 not cut)
- [ ] ≥20 unit tests + ≥3 integration tests passing
- [ ] All SC-001 through SC-014 verified (SC-013 skipped if T06 cut)
- [ ] Pre-activation sanity check passes on real codebase
- [ ] cli-portify retrospective produces ≥1 finding (SC-009)
- [ ] Performance: p95 < 5s for 50-file analysis (SC-008)
- [ ] No CRITICAL or MAJOR issues open
- [ ] Shadow mode ready for deployment

---

## 6. Quality Gates Between Phases

### Gate G0→1: Architecture Lock
- **Required**: VM-0 all items checked
- **Blocks on**: Unresolved P0 open questions (#1, #7)
- **CRITICAL if**: `provider_dir_names` cannot be confirmed → blocks all detection logic
- **MAJOR if**: T06 decision deferred without explicit cut timeline

### Gate G1→2: Core Engine Stable
- **Required**: VM-1 all items checked, ≥12 unit tests green
- **Blocks on**: Any detection type (unwired/orphan/registry) producing incorrect results
- **CRITICAL if**: `run_wiring_analysis()` crashes or hangs on valid input
- **MAJOR if**: `emit_report()` produces invalid YAML frontmatter
- **Enables parallel**: T13 (unit test expansion) can begin

### Gate G2→3: Gate Substrate Compatible
- **Required**: VM-2 all items checked, `gate_passed()` integration test green
- **Blocks on**: Any semantic check producing incorrect result; layering violation detected
- **CRITICAL if**: `gate_passed()` requires modification to handle `WIRING_GATE`
- **MAJOR if**: Semantic check functions have I/O side effects (violates NFR-006)

### Gate G3→4: Pipeline Safe
- **Required**: VM-3 all items checked, roadmap integration test green
- **Blocks on**: Roadmap pipeline failure with wiring step active; existing steps regressed
- **CRITICAL if**: Wiring step breaks pipeline resume behavior
- **CRITICAL if**: Existing roadmap steps fail or produce different output
- **MAJOR if**: Step ordering incorrect (not between spec-fidelity and remediate)

### Gate G4→5: Sprint Safe
- **Required**: VM-4 all items checked
- **Blocks on**: Sprint task status affected in shadow mode; performance > 2s
- **MAJOR if**: Post-task hook errors are not gracefully handled

### Gate G5→6: Extensions Non-Regressive
- **Required**: VM-5 all items checked
- **Blocks on**: Existing audit fixture regression; non-additive agent changes
- **MAJOR if**: Any existing agent rule or tool modified rather than extended

### Gate G6→Ship: Release Ready
- **Required**: VM-6 all items checked
- **Blocks on**: Coverage < 90%; any SC criterion failing; pre-activation sanity check failing
- **CRITICAL if**: Shadow mode affects task/pipeline outcomes (violates core safety property)
- **Ship requirement**: Shadow mode only. Soft/full promotion are post-ship decisions requiring calibration data.

---

## Test Fixture Strategy

### Fixture Design (50–80 LOC each per NFR-012)

| Fixture | Purpose | Contents |
|---------|---------|----------|
| `fixture_unwired_callable.py` | SC-001 | Class with `Optional[Callable]=None` param, no call site provides it |
| `fixture_wired_callable.py` | Negative case | Class with `Optional[Callable]=None`, call site provides by keyword |
| `fixture_orphan_module.py` | SC-002 | Module in provider dir, exported function never imported |
| `fixture_used_module.py` | Negative case | Module in provider dir, function imported by consumer |
| `fixture_bad_registry.py` | SC-003 | Registry dict with non-importable function reference |
| `fixture_good_registry.py` | Negative case | Registry dict with all resolvable references |
| `fixture_whitelisted.py` | SC-007 | Unwired callable that matches whitelist entry |
| `fixture_parse_error.py` | Edge case | Syntactically invalid Python (graceful degradation) |
| `fixture_empty_dir/` | Edge case | Provider dir with no Python files |
| `fixture_cli_portify_noop.py` | SC-009 | Reproduction of known cli-portify executor no-op pattern |
| `wiring_whitelist_valid.yaml` | Config | Valid whitelist with symbol+reason entries |
| `wiring_whitelist_malformed.yaml` | Config | Malformed whitelist for error handling test |

### Report Fixtures

| Fixture | Purpose |
|---------|---------|
| `report_valid_shadow.md` | Valid report in shadow mode — `gate_passed()` should return True |
| `report_valid_full_clean.md` | Valid report in full mode, zero findings — should pass |
| `report_valid_full_blocking.md` | Valid report in full mode with critical findings — should fail |
| `report_invalid_frontmatter.md` | Missing required frontmatter fields — semantic checks should fail |
| `report_inconsistent_counts.md` | `total_findings` doesn't match sum — consistency check fails |

---

## Continuous Validation Approach

Testing is not a terminal phase — it runs continuously:

1. **Phase 1 onward**: Every new function gets a unit test before the phase gate review
2. **Every commit**: Existing test suite runs (no regressions tolerated)
3. **Phase 3 (highest risk)**: Roadmap executor changes require running the full existing roadmap test suite before and after
4. **Shadow calibration (post-ship)**: FPR/TPR metrics collected every release; promotion decisions data-driven

**Stop-and-fix triggers**:
- Any existing test breaks → CRITICAL, stop immediately
- New unit test for new code fails → MAJOR, fix before phase gate
- Integration test fails on pipeline path → CRITICAL, stop immediately
- Coverage drops below 90% on core modules → MAJOR, add tests before next phase
