# Validation Report

Generated: 2026-03-23
Roadmap: `.dev/releases/current/turnledger-integration/v3.3-TurnLedger-Validation/roadmap.md`
Phases validated: 4
Agents spawned: 8
Total findings: 22 (High: 5, Medium: 11, Low: 6)

---

## Findings

### High Severity

#### H1. T02.02 — `_parse_phase_tasks()` return type is wrong

- **Severity**: High
- **Affects**: phase-2-tasklist.md / T02.02
- **Problem**: Task asserts return type is `list[PhaseTask]` but the spec Code State Snapshot documents `_parse_phase_tasks()` as returning `list[TaskEntry] | None`. `PhaseTask` does not exist in the codebase. Note: this error originates in the roadmap itself (2A.2) and propagated to the tasklist.
- **Roadmap evidence**: Roadmap 2A.2: "assert `_parse_phase_tasks()` return type is `list[PhaseTask]`"
- **Tasklist evidence**: T02.02 deliverables and acceptance criteria reference `list[PhaseTask]`
- **Exact fix**: Change all references from `list[PhaseTask]` to `list[TaskEntry] | None` in T02.02

#### H2. T03.03 — Invented ordering constraint for fidelity checker

- **Severity**: High
- **Affects**: phase-3-tasklist.md / T03.03
- **Problem**: Acceptance criterion says "fidelity checker appended (not prepended)" but the roadmap specifies only "wire fidelity_checker into `_run_checkers()` alongside structural and semantic layers" with no ordering constraint. The invented "append" constraint may be architecturally wrong depending on the existing checker dispatch structure.
- **Roadmap evidence**: Roadmap 3A.3: "alongside structural and semantic layers" — no ordering specified
- **Tasklist evidence**: T03.03 Acceptance Criteria bullet 2: "fidelity checker appended (not prepended)"
- **Exact fix**: Replace with "fidelity checker integrated alongside structural and semantic layers; ordering determined by integration contract review"

#### H3. T03.03 — Phantom A.6 architect note reference

- **Severity**: High
- **Affects**: phase-3-tasklist.md / T03.03
- **Problem**: Acceptance criterion references "per A.6 architect note" which does not exist in the roadmap. The roadmap appendix labels are A.1 through A.9 for Integration Point Registry entries, not architect notes.
- **Roadmap evidence**: No "A.6 architect note" exists. A.6 is the `_run_checkers()` Checker Registry entry in the Integration Point Registry.
- **Tasklist evidence**: T03.03 Acceptance Criteria bullet 3: "per A.6 architect note"
- **Exact fix**: Replace with "per the existing structural/semantic checker contract in `_run_checkers()`"

#### H4. T04.02 — Grep-audit scope narrowed: orchestration logic dropped

- **Severity**: High
- **Affects**: phase-4-tasklist.md / T04.02
- **Problem**: Roadmap requires auditing mock.patch on "gate functions or orchestration logic" but the tasklist drops "or orchestration logic", narrowing the audit scope and partially weakening NFR-1.
- **Roadmap evidence**: Roadmap 4.2: "confirm no `mock.patch` on gate functions **or orchestration logic** across all v3.3 test files"
- **Tasklist evidence**: T04.02 title and acceptance criteria reference only "gate functions"
- **Exact fix**: Add "or orchestration logic" to T04.02 title, deliverables, and acceptance criteria

#### H5. T02.24/T02.25/T02.26 — audit_trail fixture retrofit (REQ-078) omitted for 2D.1-2D.3

- **Severity**: High
- **Affects**: phase-2-tasklist.md / T02.24, T02.25, T02.26
- **Problem**: Roadmap explicitly states "Tasks 2D.1-2D.3 must retrofit `audit_trail` fixture usage into all existing tests being extended, per constraint REQ-078." This retrofit requirement is absent from all three tasks' deliverables and acceptance criteria.
- **Roadmap evidence**: Roadmap line 141: "Tasks 2D.1-2D.3 must retrofit..."
- **Tasklist evidence**: T02.24, T02.25, T02.26 — no mention of audit_trail retrofit
- **Exact fix**: Add to each of T02.24, T02.25, T02.26 acceptance criteria: "All existing tests being extended must be retrofitted with `audit_trail` fixture usage per REQ-078"

---

### Medium Severity

#### M1. T01.02 — `tests/roadmap/conftest.py` missing from Deliverables

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.02
- **Problem**: Roadmap integration point requires fixture registration at both `tests/v3.3/conftest.py` and `tests/roadmap/conftest.py`. T01.02 deliverables list only the former. The creation appears in Step 5 but not in Deliverables.
- **Roadmap evidence**: Roadmap line 52: "registers as a conftest.py plugin at tests/v3.3/conftest.py and tests/roadmap/conftest.py"
- **Tasklist evidence**: T01.02 Deliverables lists only `tests/v3.3/conftest.py`
- **Exact fix**: Add `tests/roadmap/conftest.py` to T01.02 Deliverables section

#### M2. T01.06 — AST analyzer algorithmic requirements stripped from summary

- **Severity**: Medium
- **Affects**: phase-1-tasklist.md / T01.06 (Roadmap Item Registry in index)
- **Problem**: The Roadmap Item Registry entry for R-006 and the task summary omit the specific algorithmic requirements: `ast.parse()` -> call graph -> BFS/DFS reachability, cross-module import resolution, lazy import handling. These are in the task's Steps and Acceptance Criteria but should also be surfaced in the registry.
- **Roadmap evidence**: Roadmap 1B.2: "ast.parse() -> call graph construction -> BFS/DFS reachability; cross-module import resolution; lazy import handling"
- **Tasklist evidence**: Task body covers this but the Roadmap Item Registry truncates to "AST call-chain analyzer module"
- **Exact fix**: No change needed to phase file (already covered in Steps/AC). Registry entry is truncated by the 20-word rule — acceptable.

#### M3. T02.06 — KPI test missing call args and file output assertions

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.06
- **Problem**: Task only asserts field VALUES but spec FR-1.11 requires 3 assertions: (a) `build_kpi_report()` called with correct args, (b) `gate-kpi-report.md` written to `results_dir`, (c) field VALUES match. Task covers only (c).
- **Roadmap evidence**: Roadmap 2A.6 covers only VALUES assertion; spec FR-1.11 adds (a) and (b)
- **Tasklist evidence**: T02.06 acceptance criteria reference only VALUE assertions
- **Exact fix**: Add to T02.06 acceptance criteria: "assert `build_kpi_report()` called with `all_gate_results`, `remediation_log`, `ledger`; assert `gate-kpi-report.md` written to `results_dir`"

#### M4. T02.09 — BLOCKING remediation lifecycle assertions incomplete

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.09
- **Problem**: Task uses shorthand "format -> debit -> recheck -> restore/fail" but spec FR-1.14 enumerates 5 discrete assertions. "Restore/fail" collapses two distinct outcomes: restore requires BOTH status=PASS AND wiring turns credited; fail means status remains FAIL.
- **Roadmap evidence**: Roadmap 2A.9 and OQ-5
- **Tasklist evidence**: T02.09 collapses assertions
- **Exact fix**: Expand T02.09 to enumerate: (1) format produces non-empty prompt, (2) debit occurs, (3) _recheck_wiring() called, (4) pass: status=PASS + turns credited, (5) fail: status=FAIL persists

#### M5. T02.13 — SHADOW_GRACE_INFINITE behavioral assertion dropped

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.13
- **Problem**: Spec FR-1.19 requires two assertions: (a) constant value and (b) grace period behavior (shadow mode never exits grace, gate always credits back). Task description collapses to just the constant check.
- **Roadmap evidence**: Roadmap 2A.13: "constant value and grace period behavior under shadow mode"
- **Tasklist evidence**: T02.13 acceptance criteria reference only constant value
- **Exact fix**: Add to T02.13: "assert when `wiring_gate_grace_period == SHADOW_GRACE_INFINITE`, shadow mode never exits grace period and wiring gate always credits back"

#### M6. T02.15 — check_wiring_report() delegation assertion dropped

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.15
- **Problem**: Spec FR-1.21 requires 3 assertions: called, delegates, returns valid report. Task collapses all three.
- **Roadmap evidence**: Roadmap 2A.15: "wrapper is called, delegates, returns valid report"
- **Tasklist evidence**: T02.15 acceptance criteria lack assertion specificity
- **Exact fix**: Expand T02.15 acceptance criteria to: "(a) wrapper is called, (b) delegates to underlying analysis (not no-op), (c) returns valid report structure"

#### M7. T02.22 — Budget exhaustion scenario expected behaviors missing

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.22
- **Problem**: Four distinct scenarios have distinct expected behaviors but the task collapses them to "4 budget exhaustion tests." Developers cannot implement without knowing per-scenario expected outcomes.
- **Roadmap evidence**: Roadmap 2C.2: 4 named scenarios with distinct outcomes
- **Tasklist evidence**: T02.22 provides only group label
- **Exact fix**: Add per-scenario expected behaviors: (a) SKIPPED+remaining listed, (b) hook skipped+status unchanged, (c) FAIL+BUDGET_EXHAUSTED logged, (d) halt+run_count<max_runs

#### M8. T02.28 — 2A.3 overlap not flagged

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.28
- **Problem**: Roadmap flags potential overlap with 2A.3 (FR-1.7). Tasklist does not carry this forward.
- **Roadmap evidence**: Roadmap 2D.5: "(may overlap 2A.3)"
- **Tasklist evidence**: T02.28 has no overlap note
- **Exact fix**: Add note to T02.28: "May overlap T02.03 (FR-1.7); check 2A.3 coverage first before implementing"

#### M9. T02.29 — T17-T22 not decomposed into individual test scopes

- **Severity**: Medium
- **Affects**: phase-2-tasklist.md / T02.29
- **Problem**: Six tests collapsed to "T17-T22" without per-test scope descriptions.
- **Roadmap evidence**: Roadmap 2D.6 enumerates: T17 (cross-phase ledger), T18 (mode switch), T19 (concurrent gate), T20 (audit completeness), T21 (manifest coverage), T22 (full pipeline E2E)
- **Tasklist evidence**: T02.29 provides only "T17-T22"
- **Exact fix**: Expand deliverables to enumerate all 6 test scopes

#### M10. T03.07 — Negative case missing "synthetic test" qualification

- **Severity**: Medium
- **Affects**: phase-3-tasklist.md / T03.07
- **Problem**: Roadmap specifies negative case must use "synthetic test with missing implementation" per R-3 mitigation. Task drops this qualifier.
- **Roadmap evidence**: Roadmap 3B.3: "(b) negative case: flags gap in synthetic test with missing implementation"
- **Tasklist evidence**: T03.07: "negative case (flags gap)" — no synthetic qualifier
- **Exact fix**: Expand to "negative case: flags gap in synthetic test with missing implementation"

#### M11. T04.03 — Confirmatory verb weakened

- **Severity**: Medium
- **Affects**: phase-4-tasklist.md / T04.03
- **Problem**: Roadmap says "confirm third-party verifiability properties" (action with pass/fail outcome). Tasklist weakens to "for third-party verifiability" (purpose clause, no outcome).
- **Roadmap evidence**: Roadmap 4.3: "Manual review of JSONL audit trail: confirm third-party verifiability properties"
- **Tasklist evidence**: T04.03 title: "Manual JSONL audit trail review for third-party verifiability"
- **Exact fix**: Change to "confirm third-party verifiability properties per FR-7.2"

---

### Low Severity

#### L1. T01.02 — Rollback omits tests/roadmap/conftest.py

- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.02
- **Problem**: Rollback mentions only `tests/v3.3/conftest.py` but task also creates `tests/roadmap/conftest.py`.
- **Exact fix**: Add `tests/roadmap/conftest.py` to rollback

#### L2. T01.08 — Known-good/known-bad dual coverage not in acceptance criteria

- **Severity**: Low
- **Affects**: phase-1-tasklist.md / T01.08
- **Problem**: Validation Checkpoint A requires both known-good and known-bad reachability cases. Task body covers this in Steps but acceptance criteria don't enforce it.
- **Exact fix**: Add to acceptance criteria: "Tests cover both known-good reachability and known-bad unreachability cases"

#### L3. T02.01 — FR-1.1-1.4 assertion specifics stripped

- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.01
- **Problem**: Spec requires specific assertions (ledger.initial_budget, ledger.reimbursement_rate, DeferredRemediationLog persist_path) that are collapsed to "construction validation."
- **Exact fix**: Add assertion specifics to T02.01 acceptance criteria

#### L4. T02.12 — "not 46" regression guard dropped

- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.12
- **Problem**: Spec includes "(not 46)" as regression guard against prior wrong value. Task drops this context.
- **Exact fix**: Add "not 46" to T02.12 description

#### L5. T02.14 — Invalid/missing config defaults assertion dropped

- **Severity**: Low
- **Affects**: phase-2-tasklist.md / T02.14
- **Problem**: Spec requires testing both (a) derived fields and (b) invalid/missing config defaults. Task covers only (a).
- **Exact fix**: Add "invalid or missing base config values produce sensible defaults" to T02.14

#### L6. T04.05 — Invented output path "in docs/generated/"

- **Severity**: Low
- **Affects**: phase-4-tasklist.md / T04.05
- **Problem**: Roadmap Phase 4 row 4.5 specifies no output path. "docs/generated/" is referenced only in Phase 2D.4 context.
- **Exact fix**: Remove "in docs/generated/" or note it as inherited from Phase 2D.4 convention

---

## Verification Results

Verified: 2026-03-23
Findings resolved: 22/22

| Finding | Status | Notes |
|---------|--------|-------|
| H1 | RESOLVED | `list[PhaseTask]` fully replaced with `list[TaskEntry] \| None` across T02.02; zero remaining occurrences |
| H2 | RESOLVED | "appended (not prepended)" removed; replaced with roadmap-faithful integration language |
| H3 | RESOLVED | "per A.6 architect note" removed; replaced with correct `_run_checkers()` contract reference |
| H4 | RESOLVED | "or orchestration logic" added to T04.02 title, deliverables, and all acceptance criteria |
| H5 | RESOLVED | REQ-078 audit_trail retrofit added to T02.24 deliverables, T02.25 AC, T02.26 AC |
| M1 | RESOLVED | `tests/roadmap/conftest.py` added to T01.02 Deliverables section |
| M2 | RESOLVED | Registry truncation is 20-word rule; task body already complete — no change needed |
| M3 | RESOLVED | `build_kpi_report()` call args and file output assertions added to T02.06 |
| M4 | RESOLVED | 5-part assertion list added to T02.09; OQ-5 scope deferral explicit |
| M5 | RESOLVED | Grace period behavioral assertion added to T02.13 |
| M6 | RESOLVED | 3-part assertion (called, delegates, returns) added to T02.15 |
| M7 | RESOLVED | Per-scenario expected behaviors added to T02.22 |
| M8 | RESOLVED | Overlap note with T02.03 / 2A.3 added to T02.28 |
| M9 | RESOLVED | T17-T22 decomposed into 6 individual test scopes in T02.29 |
| M10 | RESOLVED | "synthetic test with missing implementation" qualifier added to T03.07 |
| M11 | RESOLVED | T04.03 title changed to "confirm third-party verifiability properties" |
| L1 | RESOLVED | `tests/roadmap/conftest.py` added to T01.02 Rollback |
| L2 | RESOLVED | Already present in T01.08 AC at line 408 — no change needed |
| L3 | RESOLVED | FR-1.1-1.4 assertion specifics added to T02.01 AC |
| L4 | RESOLVED | "not 46" regression guard added to T02.12 deliverables |
| L5 | RESOLVED | Invalid/missing config defaults assertion added to T02.14 |
| L6 | ACCEPTED | `docs/generated/` has roadmap backing from Phase 2D.4 row — left as-is |
