# Patch Checklist

Generated: 2026-03-23
Total edits: 22 across 4 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] T01.02: Add `tests/roadmap/conftest.py` to Deliverables section (from M1)
  - [ ] T01.02: Add `tests/roadmap/conftest.py` to Rollback line (from L1)
  - [ ] T01.08: Add known-good/known-bad dual coverage to acceptance criteria (from L2)

- phase-2-tasklist.md
  - [ ] T02.01: Add FR-1.1-1.4 assertion specifics to acceptance criteria (from L3)
  - [ ] T02.02: Change `list[PhaseTask]` to `list[TaskEntry] | None` (from H1)
  - [ ] T02.06: Add `build_kpi_report()` call args and `gate-kpi-report.md` file output assertions (from M3)
  - [ ] T02.09: Expand BLOCKING remediation to 5-part assertion list (from M4)
  - [ ] T02.12: Add "not 46" regression guard to description (from L4)
  - [ ] T02.13: Add grace period behavioral assertion (from M5)
  - [ ] T02.14: Add invalid/missing config defaults assertion (from L5)
  - [ ] T02.15: Expand to 3-part assertion (called, delegates, returns) (from M6)
  - [ ] T02.22: Add per-scenario expected behaviors for 4 exhaustion points (from M7)
  - [ ] T02.24: Add audit_trail fixture retrofit requirement (REQ-078) (from H5)
  - [ ] T02.25: Add audit_trail fixture retrofit requirement (REQ-078) and SC-level assertion count (from H5)
  - [ ] T02.26: Add audit_trail fixture retrofit requirement (REQ-078) (from H5)
  - [ ] T02.28: Add overlap note referencing T02.03 / 2A.3 (from M8)
  - [ ] T02.29: Decompose T17-T22 into 6 individual test scopes (from M9)

- phase-3-tasklist.md
  - [ ] T03.03: Replace "appended (not prepended)" with roadmap-faithful ordering (from H2)
  - [ ] T03.03: Replace "per A.6 architect note" with correct reference (from H3)
  - [ ] T03.07: Add "synthetic test with missing implementation" to negative case (from M10)

- phase-4-tasklist.md
  - [ ] T04.02: Add "or orchestration logic" to title, deliverables, and acceptance criteria (from H4)
  - [ ] T04.03: Change "for third-party verifiability" to "confirm third-party verifiability properties per FR-7.2" (from M11)

## Cross-file consistency sweep

- [ ] Verify all T02.24-T02.26 now reference REQ-078 audit_trail retrofit consistently
- [ ] Verify T02.02 `list[TaskEntry] | None` is consistent with T02.01 construction tests
- [ ] Verify T03.03 checker ordering language is consistent with T03.02 fidelity checker AC

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### T01.02 Deliverables

**A. Add tests/roadmap/conftest.py to Deliverables (M1)**
Current issue: Only `tests/v3.3/conftest.py` listed
Change: Add second deliverable line
Diff intent: After existing deliverable line, add: `- \`tests/roadmap/conftest.py\` — registers \`audit_trail\` fixture for \`tests/roadmap/\` test suite per roadmap integration point`

**B. Fix Rollback (L1)**
Current issue: "Delete `tests/v3.3/conftest.py`"
Change: Add second file
Diff intent: Change to "Delete `tests/v3.3/conftest.py` and `tests/roadmap/conftest.py`"

#### T01.08 Acceptance Criteria

**C. Add dual coverage criterion (L2)**
Current issue: No explicit known-good/known-bad requirement
Change: Add criterion
Diff intent: Add bullet: "Tests cover both known-good reachability (directly called functions) and known-bad unreachability (dead code paths) cases per Validation Checkpoint A"

### 2) phase-2-tasklist.md

#### T02.01 Acceptance Criteria

**D. Add assertion specifics (L3)**
Current issue: "Each test constructs its target class via real orchestration"
Change: Add specific assertions
Diff intent: Expand first AC bullet to include: "including `ledger.initial_budget`, `ledger.reimbursement_rate` for TurnLedger (FR-1.1) and `persist_path` under `results_dir` for DeferredRemediationLog (FR-1.3)"

#### T02.02

**E. Fix return type (H1)**
Current issue: `list[PhaseTask]` throughout
Change: Replace with `list[TaskEntry] | None`
Diff intent: Replace all instances of `list[PhaseTask]` with `list[TaskEntry] | None` in T02.02 deliverables, steps, and acceptance criteria

#### T02.06 Acceptance Criteria

**F. Add missing KPI assertions (M3)**
Current issue: Only field VALUES assertion
Change: Add two more assertions
Diff intent: Expand acceptance criteria to include: "assert `build_kpi_report()` called with `all_gate_results`, `remediation_log`, `ledger`; assert `gate-kpi-report.md` written to `results_dir`"

#### T02.09 Acceptance Criteria

**G. Expand remediation lifecycle (M4)**
Current issue: "format -> debit -> recheck -> restore/fail" shorthand
Change: Enumerate 5 assertions
Diff intent: Replace shorthand with: "(1) `_format_wiring_failure()` produces non-empty prompt, (2) `ledger.debit(config.remediation_cost)` called, (3) `_recheck_wiring()` called, (4) on pass: status=PASS AND wiring turns credited, (5) on fail: status=FAIL persists"

#### T02.12

**H. Add regression guard (L4)**
Current issue: "uses 61" without context
Change: Add "not 46"
Diff intent: Change deliverable to: "`TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)` uses 61, not 46 — regression guard against prior wrong constant"

#### T02.13 Acceptance Criteria

**I. Add behavioral assertion (M5)**
Current issue: Only constant value checked
Change: Add grace period behavior
Diff intent: Add AC bullet: "When `wiring_gate_grace_period == SHADOW_GRACE_INFINITE`, shadow mode never exits grace period and wiring gate always credits back"

#### T02.14 Acceptance Criteria

**J. Add defaults assertion (L5)**
Current issue: Only derived fields tested
Change: Add invalid/missing config handling
Diff intent: Add AC bullet: "Invalid or missing base config values produce sensible defaults (not crash or undefined behavior)"

#### T02.15 Acceptance Criteria

**K. Expand to 3-part assertion (M6)**
Current issue: Generic "delegation and return validation"
Change: Enumerate three assertions
Diff intent: Replace with: "(a) `check_wiring_report()` is called within wiring analysis flow, (b) delegates to underlying analysis (not a no-op stub), (c) returns valid report structure with expected fields"

#### T02.22 Deliverables/Acceptance Criteria

**L. Add per-scenario expected behaviors (M7)**
Current issue: "4 budget exhaustion tests" with no decomposition
Change: Enumerate scenarios
Diff intent: Expand deliverables to: "(a) before task launch: SKIPPED + remaining tasks listed, (b) before wiring: hook skipped + status unchanged, (c) before remediation: FAIL + BUDGET_EXHAUSTED logged, (d) mid-convergence: halt + run_count < max_runs"

#### T02.24 Acceptance Criteria

**M. Add REQ-078 audit_trail retrofit (H5)**
Current issue: No mention of audit_trail retrofit
Change: Add retrofit requirement
Diff intent: Add AC bullet: "All existing tests being extended must be retrofitted with `audit_trail` fixture usage per REQ-078 (every test emits JSONL record)"

#### T02.25 Acceptance Criteria

**N. Add REQ-078 + SC assertion count (H5)**
Current issue: No audit_trail retrofit; no assertion count target
Change: Add both
Diff intent: Add AC bullets: "All existing tests retrofitted with `audit_trail` fixture per REQ-078" and "6 SC-level assertions added (one per SC-1 through SC-6)"

#### T02.26 Acceptance Criteria

**O. Add REQ-078 audit_trail retrofit (H5)**
Current issue: No mention of audit_trail retrofit
Change: Add retrofit requirement
Diff intent: Add AC bullet: "All existing tests being extended must be retrofitted with `audit_trail` fixture per REQ-078"

#### T02.28 Notes

**P. Add overlap note (M8)**
Current issue: No overlap flagged
Change: Add overlap reference
Diff intent: Add to Notes: "May overlap T02.03 (FR-1.7 post-phase wiring hook); check 2A.3 coverage first before implementing. Depends on Phase 2A completion."

#### T02.29 Deliverables

**Q. Decompose T17-T22 (M9)**
Current issue: "6 tests covering T17-T22" with no per-test scope
Change: Enumerate all 6
Diff intent: Expand deliverables to list: "T17 (cross-phase ledger coherence), T18 (mode switch mid-sprint), T19 (concurrent gate evaluation), T20 (audit completeness verification), T21 (manifest coverage check), T22 (full pipeline E2E)"

### 3) phase-3-tasklist.md

#### T03.03 Acceptance Criteria

**R. Fix ordering constraint (H2)**
Current issue: "fidelity checker appended (not prepended)"
Change: Use roadmap-faithful language
Diff intent: Replace with "fidelity checker integrated alongside structural and semantic layers per roadmap 3A.3; ordering relative to existing checkers determined by integration contract review"

**S. Fix phantom reference (H3)**
Current issue: "per A.6 architect note"
Change: Correct the reference
Diff intent: Replace with "per the existing structural/semantic checker output shape contract in `_run_checkers()`"

#### T03.07 Deliverables

**T. Add synthetic test qualifier (M10)**
Current issue: "negative case (flags gap)"
Change: Add synthetic qualifier
Diff intent: Change to "negative case: flags gap in synthetic test with missing implementation (per R-3 mitigation strategy)"

### 4) phase-4-tasklist.md

#### T04.02

**U. Add orchestration logic scope (H4)**
Current issue: Only "gate functions" in scope
Change: Add "or orchestration logic"
Diff intent: Change title to "Run grep-audit for mock.patch on gate functions or orchestration logic"; update deliverables and AC similarly

#### T04.03

**V. Strengthen confirmatory verb (M11)**
Current issue: "for third-party verifiability"
Change: Use confirmatory language
Diff intent: Change to "confirm third-party verifiability properties per FR-7.2 (real timestamps, spec-traced, runtime observations, explicit verdicts)"

---

## Suggested execution order

1. phase-2-tasklist.md (17 edits — largest file, most findings, includes sole H1)
2. phase-3-tasklist.md (3 edits — H2, H3, M10)
3. phase-4-tasklist.md (2 edits — H4, M11)
4. phase-1-tasklist.md (3 edits — M1, L1, L2)
