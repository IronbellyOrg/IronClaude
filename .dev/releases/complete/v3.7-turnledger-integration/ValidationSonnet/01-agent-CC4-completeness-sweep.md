# Agent CC4 — Completeness Sweep Report
## v3.3 TurnLedger Validation: Final Safety Net

**Agent**: CC4 (Completeness Sweep)
**Sweep Date**: 2026-03-23
**Inputs**:
- Spec: `v3.3-requirements-spec.md`
- Roadmap: `v3.3-TurnLedger-Validation/roadmap.md`
**Sweep Method**: Systematic cross-reference of all spec sections against roadmap tasks, targeting prior-known gaps, constraint requirements, cross-cutting concerns, and orphan tasks.

---

## Sweep Target 1: Spec Sections Not Mapped to Requirement IDs

### CC4-1: "Code State Snapshot" — Implied Validation Requirement
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: Section "Code State Snapshot (Verified 2026-03-22)" — "All v3.05/v3.1/v3.2 architectural constructs are **verified present and wired** in production code. The prior QA reflections reporting T04 as 'skipped' and T02 as 'incomplete' are **STALE** — both are now fully implemented."
- **Roadmap response**: The roadmap does not contain a task that explicitly validates the "stale" claim. Phase 4 task 4.2 (grep-audit on mocks) is adjacent but does not verify that T04 and T02 are implemented.
- **Severity**: MEDIUM
- **Gap description**: The spec states that the Code State Snapshot is "Verified 2026-03-22" and was the basis for eliminating T04/T02 from the gap list. However, no roadmap task explicitly confirms this verification is repeatable (i.e., there is no test that would fail if T04 or T02 were removed from the codebase). The confirming tests for T02 are addressed in 2D.5 and 2A.3; the confirming test for T04 (task-inventory path) is addressed in 2A.2. These are present but implicitly labeled — the roadmap does not explicitly call out "confirm stale status invalidated" as an acceptance criterion.
- **Impact**: If the implementation later regresses on T02 or T04, there is no explicit test mapped to that stated "verified" claim in the snapshot. The traceability chain is incomplete.
- **Recommended correction**: Add an explicit note to task 2A.2 and 2D.5 in the roadmap that these tests serve as the repeatable verification of the Code State Snapshot's "stale" determination. A one-line acceptance sub-criterion is sufficient: "This test invalidates the stale T04/T02 status by failing if the wiring is removed."

---

### CC4-2: Roadmap Open Questions vs. Spec Implied Resolutions
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: Constraints section — "No mocks on gate functions"; "Baseline: 4894 passed, 3 pre-existing failures"; "UV only"; "Branch from v3.0-v3.2-Fidelity"
- **Roadmap response**: Roadmap Open Questions table contains 8 questions. None of the 8 open questions are in direct conflict with explicit spec constraints. However, **Open Question 7** reads: "Investigate before Phase 3. Run baseline suite, capture the 3 failures, document them. If 2 are wiring-pipeline related (R-5), the FR-5.1 fix may resolve them — reducing pre-existing to 1."
- **Severity**: MEDIUM
- **Gap description**: The spec states definitively "Baseline: 4894 passed, 3 pre-existing failures" — this is a hard constraint, not a recommendation. Roadmap Open Question 7 treats this as partially open ("may resolve them — reducing pre-existing to 1"), but the spec does not authorize changing the pre-existing failure count. The spec says ≤3; if the FR-5.1 fix resolves 2 of the 3, the baseline count changes and SC-4 ("≤3 pre-existing failures") becomes ambiguous: does ≤3 mean "original 3 are still there" or "any count ≤3 is acceptable"?
- **Impact**: If the open question resolves to "FR-5.1 reduces failures to 1," the release could ship with a subtly different baseline count than what the spec declared, which undermines third-party verifiability of the audit trail.
- **Recommended correction**: Clarify in the roadmap (or as a pre-Phase-3 decision gate) that: (a) the 3 pre-existing failures must be documented with their test names before Phase 3 begins; (b) if FR-5.1 resolves any of the 3, the task 4.1 acceptance criterion is updated to reflect the new expected count explicitly, with a note explaining the change. This resolution must be captured in the audit trail.

---

## Sweep Target 2: Specific Items from Prior Run — Missing FR Coverage

### CC4-3: FR-1.19 (SHADOW_GRACE_INFINITE) — Roadmap Coverage
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: FR-1.19 — "Assert: `SHADOW_GRACE_INFINITE` is defined in models.py with expected sentinel value. Assert: when `wiring_gate_grace_period` is set to `SHADOW_GRACE_INFINITE`, shadow mode never exits grace period (wiring gate always credits back)"
- **Roadmap response**: Phase 2A task table covers FR-1.1–FR-1.18 and FR-1.21 (via 2A.3). FR-1.19 is **absent** from the Phase 2A task table. The 2A.12 task covers FR-1.18 (budget constant). There is no 2A.13 or equivalent task for FR-1.19.
- **Severity**: HIGH
- **Gap description**: FR-1.19 is a named, numbered requirement in the spec (models.py:293, models.py:335-336) with two distinct assertions. The roadmap Phase 2A task table jumps from FR-1.18 (task 2A.12) to FR-1.21 (covered implicitly in 2A.3), skipping FR-1.19 and FR-1.20 entirely. Neither constant value validation (sentinel check) nor behavioral effect testing (grace period never expires) is present in any roadmap task.
- **Impact**: SHADOW_GRACE_INFINITE is a sentinel constant. If its value changes or the grace-period logic is broken, no test will catch it. Shadow mode behavior under infinite grace is untested.
- **Recommended correction**: Add task 2A.13 to the roadmap Phase 2A table:
  - Requirement: FR-1.19
  - Test count: 2 tests — one asserting the sentinel value of `SHADOW_GRACE_INFINITE`, one asserting that shadow mode with infinite grace always credits back (never blocks).
  - File: `tests/v3.3/test_wiring_points_e2e.py`

---

### CC4-4: FR-1.20 (__post_init__ derivation) — Roadmap Coverage
- **Type**: MISSED_EXTRACTION
- **Spec source**: FR-1.20 — "Assert: derived fields (`wiring_gate_enabled`, `wiring_gate_grace_period`, `wiring_analyses_count`) are computed from base config values. Assert: invalid or missing base config values produce sensible defaults."
- **Roadmap response**: FR-1.20 is **absent** from all roadmap phase task tables. The roadmap Phase 2A subtotal of "~21 tests covering SC-1" implies FR-1.1–FR-1.18, but the spec defines requirements through FR-1.21.
- **Severity**: HIGH
- **Gap description**: The `__post_init__()` method derives three config fields that gate logic depends on. If derivation is broken (e.g., `wiring_gate_enabled` not set correctly), gate modes will misbehave silently. This requirement is fully specified in the spec (models.py:338-384) with two distinct assertions. Neither is present in the roadmap.
- **Impact**: Config derivation bugs in `__post_init__()` are invisible without dedicated tests. The entire gate rollout mode matrix (FR-3) depends on correct config derivation.
- **Recommended correction**: Add task 2A.14 to the roadmap Phase 2A table:
  - Requirement: FR-1.20
  - Test count: 2 tests — derived fields correct from valid config; sensible defaults from invalid/missing config.
  - File: `tests/v3.3/test_wiring_points_e2e.py`

---

### CC4-5: FR-1.21 (check_wiring_report() Wrapper) — Roadmap Coverage
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: FR-1.21 — "Assert `check_wiring_report()` wrapper (wiring_gate.py:1079) is called within the wiring analysis flow. Assert: the wrapper delegates to the underlying analysis and returns a valid report structure."
- **Roadmap response**: FR-1.21 is referenced in Phase 2A task 2A.3: "2 tests: Post-phase wiring hook fires on per-task and per-phase/ClaudeProcess paths." However, task 2A.3 is mapped to FR-1.7, not FR-1.21. FR-1.21 has a distinct focus — confirming the `check_wiring_report()` wrapper specifically, including its delegation behavior and return structure.
- **Severity**: MEDIUM
- **Gap description**: FR-1.7 tests that `run_post_phase_wiring_hook()` fires. FR-1.21 tests that `check_wiring_report()` (a different, deeper wrapper) is specifically called and returns a valid structure. These are adjacent but not equivalent. The roadmap task 2A.3 may coincidentally cover this if its implementation includes the right assertions, but the roadmap text does not state this explicitly.
- **Impact**: The `check_wiring_report()` wrapper at wiring_gate.py:1079 could be bypassed or broken without FR-1.7 tests detecting it, since FR-1.7 only validates hook invocation at a higher level.
- **Recommended correction**: Explicitly expand the requirements coverage annotation for task 2A.3 to include "FR-1.21" and add a sub-assertion in the task description: "Confirm `check_wiring_report()` is invoked and returns a valid report structure." Alternatively, add a dedicated task 2A.15 for FR-1.21 if the two requirements warrant separate test functions.

---

### CC4-6: FR-2.1a (handle_regression() Reachability) — Roadmap Coverage
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: FR-2.1a — "Assert: when convergence detects a regression (score decreases between runs), `handle_regression()` is invoked. Assert: `handle_regression()` logs the regression event and adjusts budget accordingly."
- **Roadmap response**: Task 2B.1 covers FR-2.1 (convergence path E2E: debit, credit, reimburse). FR-2.1a is **not listed** in task 2B.1's requirement column, nor does any other roadmap task reference FR-2.1a by ID. The wiring manifest (spec section "Wiring Manifest v3.3") includes `handle_regression` with spec_ref "v3.05-FR8," and the roadmap task 1B.4 creates the wiring manifest, but the manifest entry alone does not constitute a behavioral test of FR-2.1a.
- **Severity**: HIGH
- **Gap description**: FR-2.1a requires a behavioral test: inject a regression condition, assert `handle_regression()` fires, assert budget is adjusted. The reachability gate (FR-4.4) will confirm `handle_regression` is statically reachable, but static reachability is not equivalent to behavioral correctness. The FR-2.1a assertions (invocation on regression detection, budget adjustment) require a runtime E2E test, which is absent from the roadmap.
- **Impact**: `handle_regression()` could be wired (reachable) but behaviorally broken (not called on actual regression, or budget logic wrong) without any test detecting it.
- **Recommended correction**: Add FR-2.1a as an explicit sub-task within 2B.1, or as a new task 2B.1a:
  - Requirement: FR-2.1a
  - Description: E2E test injecting a regression condition into convergence; assert `handle_regression()` invoked, budget adjusted.
  - File: `tests/v3.3/test_turnledger_lifecycle.py`

---

## Sweep Target 3: Constraint Requirements Often Missed

### CC4-7: "Branch from v3.0-v3.2-Fidelity" Constraint
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: Release Metadata — "**Branch**: Create from `v3.0-v3.2-Fidelity`"
- **Roadmap response**: The roadmap Resource Requirements section mentions this branch under External Dependencies: "`v3.0-v3.2-Fidelity` branch | All | Medium | Must be stable; any upstream changes require rebase." This IS present in the roadmap.
- **Severity**: LOW
- **Gap description**: The constraint is present. However, no roadmap task explicitly verifies the branch is correctly based (e.g., a Phase 4 check confirming `git merge-base` or equivalent). This is an operational gap, not a test coverage gap.
- **Impact**: Minimal — the resource dependency note is sufficient as documentation. An implementation agent would know to branch correctly.
- **Recommended correction**: No change required. The constraint is adequately represented.

---

### CC4-8: "Baseline: 4894 passed, 3 pre-existing failures" — Task 4.1 Exact Numbers
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: Constraints — "**Baseline**: 4894 passed, 3 pre-existing failures"
- **Roadmap response**: Task 4.1 — "Full test suite run: confirm ≥4894 passed, ≤3 pre-existing failures, 0 new regressions." The roadmap uses ≥4894 and ≤3, which correctly captures the spec's intent.
- **Severity**: LOW (minor note)
- **Gap description**: The spec says exactly "4894 passed, 3 pre-existing failures." The roadmap correctly translates this to ≥4894 and ≤3 (allowing for FR-5.1 potentially resolving some pre-existing failures, as noted in Open Question 7). The numbers match. However, see CC4-2 above for the related concern about the ≤3 ambiguity if FR-5.1 resolves some failures.
- **Impact**: Adequately covered, subject to the CC4-2 concern.
- **Recommended correction**: Address via CC4-2 recommendation. Task 4.1 wording itself is correct.

---

### CC4-9: "UV only" Constraint
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: Constraints — "**UV only** — `uv run pytest`, not `python -m pytest`"
- **Roadmap response**: Environment Requirements section states: "All Python execution via UV (NFR-2)." NFR-2 is referenced in the roadmap but its definition is embedded only in the spec's constraints section. The roadmap does not include a task to enforce or verify UV usage (e.g., a CI check or a grep for `python -m pytest` in new test files).
- **Severity**: LOW
- **Gap description**: The constraint is documented but there is no enforcement mechanism in the roadmap. Phase 4 task 4.2 performs a grep-audit for mock usage; a parallel grep-audit for UV compliance would be consistent but is absent.
- **Impact**: A developer could inadvertently write `python -m pytest` in a new Makefile target or CI config without the roadmap providing any detection mechanism.
- **Recommended correction**: Add a sub-item to task 4.2 or a new task 4.2a: "Grep-audit: confirm no `python -m pytest` or bare `pip install` in any new test files, Makefile changes, or CI configuration added in this release."

---

## Sweep Target 4: Audit Trail Cross-Cutting Enforcement

### CC4-10: Audit Trail Enforcement for Phase 2D and 3B Tests
- **Type**: CROSS_CUTTING_GAP
- **Spec source**: Constraints — "**Audit trail**: Every test must emit a JSONL record"; FR-7.3 — "A pytest fixture (`audit_trail`) that... Auto-flushes after each test"
- **Roadmap response**: Phase 1A establishes the `audit_trail` fixture. Phase 2A–2C tests implicitly use it (the roadmap states at Validation Checkpoint B: "Audit trail JSONL emitted for every test"). However, **Phase 2D** (QA gap tests) and **Phase 3B** (pipeline fix validation tests) have no explicit statement that these tests must also emit audit trail records.
  - Task 2D.1–2D.6: No mention of `audit_trail` fixture usage.
  - Tasks 3B.1–3B.3: No mention of `audit_trail` fixture usage.
- **Severity**: HIGH
- **Gap description**: The spec constraint is unambiguous: "Every test must emit a JSONL record." This means FR-6 tests (Phase 2D) and FR-5 validation tests (Phase 3B) are subject to the same audit trail requirement as FR-1/FR-2/FR-3 tests. The roadmap's Validation Checkpoint B says "Audit trail JSONL emitted for every test" but this checkpoint covers only Phase 2 (E2E suites). Validation Checkpoint C (Phase 3) makes no equivalent statement.
- **Impact**: Phase 2D and Phase 3B tests could be written without importing the `audit_trail` fixture, producing JSONL gaps in the final audit record. Third-party reviewers would find unverifiable tests in those phases.
- **Recommended correction**:
  1. Add explicit text to tasks 2D.1–2D.6: "Uses `audit_trail` fixture; emits JSONL record per test."
  2. Add explicit text to tasks 3B.1–3B.3: "Uses `audit_trail` fixture; emits JSONL record per test."
  3. Update Validation Checkpoint C to include: "Audit trail JSONL emitted for all Phase 3B tests."

---

## Sweep Target 5: NFR-5 Wiring Manifest Completeness — Task 4.4

### CC4-11: Task 4.4 Wording vs. NFR-5 Scope
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: FR-1 (all sub-requirements) — 21 wiring points enumerated across FR-1.1 through FR-1.21. Wiring Manifest (v3.3) section — authoritative 13-entry manifest with required_reachable entries.
- **Roadmap response**: Task 4.4 — "Validate wiring manifest completeness: every known wiring point from FR-1 has a manifest entry."
- **Severity**: MEDIUM
- **Gap description**: Task 4.4 says "every known wiring point from FR-1 has a manifest entry." The spec's Wiring Manifest has **13 entries** in `required_reachable`. However, FR-1 enumerates **21 wiring points** (FR-1.1 through FR-1.21). Not all FR-1 wiring points are represented as manifest entries — some FR-1 items (e.g., FR-1.1 TurnLedger construction, FR-1.2 ShadowGateMetrics construction) are behavioral tests, not reachability tests. The manifest correctly covers only functions that need static reachability proof.

  The gap is: task 4.4's phrasing ("every known wiring point from FR-1 has a manifest entry") is **over-broad** — it implies a 1:1 mapping between FR-1 items and manifest entries that the spec does not require. This could cause task 4.4 to fail validation if interpreted literally (since FR-1.1–FR-1.4 are construction tests, not reachability-manifest candidates).
- **Impact**: Task 4.4 could be interpreted incorrectly during Phase 4, either causing false failures (if a validator expects 21 manifest entries) or being silently misexecuted (if the validator only checks the 13 existing entries without cross-checking completeness against FR-1).
- **Recommended correction**: Revise task 4.4 wording to: "Validate wiring manifest completeness: every *function-level* wiring point from FR-1 (those requiring static reachability proof) has a corresponding manifest entry; confirm the 13-entry manifest covers all declared `required_reachable` targets from the spec's Wiring Manifest (v3.3) section." Add a count assertion: "Manifest contains exactly 13 `required_reachable` entries, matching the spec."

---

## Sweep Target 6: audit_trail Fixture Integration with tests/roadmap/conftest.py

### CC4-12: FR-6 Tests in tests/roadmap/ Missing conftest Integration
- **Type**: CROSS_CUTTING_GAP
- **Spec source**: FR-7.3 — "A pytest fixture (`audit_trail`) that... [provides `record()` method, auto-flushes after each test]"; Test File Layout — `tests/roadmap/test_convergence_wiring.py` and `tests/roadmap/test_convergence_e2e.py`
- **Roadmap response**: Phase 1A task 1A.2 — "Integration point: The `audit_trail` fixture registers as a `conftest.py` plugin at `tests/v3.3/conftest.py` **and `tests/roadmap/conftest.py`**." This is correctly stated in the roadmap. However, no Phase 2D task (2D.1–2D.3) explicitly references the `tests/roadmap/conftest.py` integration point, and no task confirms that the existing `tests/roadmap/conftest.py` does not conflict with the new `audit_trail` fixture.
- **Severity**: MEDIUM
- **Gap description**: The `tests/roadmap/` directory already exists with existing tests. Introducing the `audit_trail` fixture via `conftest.py` into an existing test directory carries integration risk: (a) existing conftest.py fixtures might conflict with the new `audit_trail` fixture; (b) existing tests in `tests/roadmap/` that were written before v3.3 will now be expected to emit JSONL records (per the "Every test must emit a JSONL record" constraint), but they were not written with that fixture — this could cause them to silently produce no JSONL output.
- **Impact**: Existing `tests/roadmap/` tests may fail to emit audit records, breaking SC-12 (third-party verifiability) silently. Conftest conflicts could cause test collection errors in Phase 2D.
- **Recommended correction**: Add a sub-task to task 1A.2 or a new task 1A.5: "Audit existing `tests/roadmap/conftest.py` for conflicts with the `audit_trail` fixture; determine whether existing roadmap tests must be retrofitted to call `audit_trail.record()` or whether the fixture auto-records at session level for all tests including pre-existing ones." Clarify the spec intent: does "every test" in the constraints mean every v3.3-authored test, or every test in the entire suite?

---

## Sweep Target 7: Orphan Tasks (No Spec Backing)

### CC4-13: Orphan task: 4.5
- **Type**: ORPHAN_TASK
- **Roadmap location**: Phase 4 task table
- **Roadmap text**: "4.5 | — | Generate final wiring-verification artifact (FR-6.1 T14)"
- **Has spec backing**: PARTIAL — FR-6.1 T14 in the spec says "Regenerate wiring-verification artifact | Generate + validate." The task exists in the spec as a gap closure item. However, the roadmap table uses "—" in the Requirement column, which is the same notation as task 4.6. This appears to be a notational error: task 4.5 has spec backing (FR-6.1 T14, SC-8), but the roadmap's requirement column is blank.
- **Severity**: LOW
- **Recommended correction**: Update the Requirement column for task 4.5 from "—" to "FR-6.1 T14, SC-8."

---

### CC4-14: Orphan task: 4.6
- **Type**: ORPHAN_TASK
- **Roadmap location**: Phase 4 task table
- **Roadmap text**: "4.6 | — | Update `docs/memory/solutions_learned.jsonl` with v3.3 patterns"
- **Has spec backing**: NO — The spec contains no requirement, success criterion, or NFR that mandates updating `docs/memory/solutions_learned.jsonl`.
- **Severity**: LOW (informational)
- **Gap description**: Task 4.6 is a housekeeping/institutional-knowledge task with no spec-level requirement. It appears to be a team practice carried forward from prior releases.
- **Impact**: None on spec compliance. The task is beneficial but unvalidated by any success criterion.
- **Recommended correction**: Either add a note clarifying this is a process task (not a spec requirement), or remove it from the spec-governed roadmap and track it separately as a team practice item.

---

## Sweep Target 8: Open Questions vs. Spec Requirements

Analysis of all 8 roadmap Open Questions against spec requirements:

| OQ # | Question Summary | Spec Requirement? | Assessment |
|------|-----------------|-------------------|------------|
| 1 | Signal handling for FR-3.3 (SIGINT vs SIGTERM) | FR-3.3 spec says "Simulate signal interrupt" — method unspecified | OQ-1 is an implementation detail recommendation, not a blocked spec requirement. The spec requires the *behavior* (KPI written, log persisted, INTERRUPTED outcome), not the signal mechanism. **No spec gap.** |
| 2 | Impl-vs-spec checker granularity | FR-5.2 says "searches codebase for evidence" — method unspecified | OQ-2 is an implementation recommendation. The spec requires the checker exists and works; the matching algorithm is an implementation choice. **No spec gap.** |
| 3 | Audit trail fixture scope (session vs function) | FR-7.3 says "session-scoped" is implied by "one JSONL per invocation" and "auto-flushes after each test" | The spec's FR-7.3 implies session-scoped (single JSONL, summary at session end). OQ-3 aligns with spec intent. **No spec gap; OQ-3 correctly resolves to session-scoped.** |
| 4 | Wiring manifest location (.yaml vs embedded markdown) | FR-4.1 says "wiring_manifest section" but Test File Layout shows `tests/v3.3/wiring_manifest.yaml` | OQ-4 resolves a minor ambiguity. The spec's Test File Layout section explicitly places the manifest at `tests/v3.3/wiring_manifest.yaml`. This is a spec constraint, not just an architectural recommendation. **Low severity gap**: the roadmap treats this as a recommendation when it should treat it as a constraint. |
| 5 | `attempt_remediation()` boundary | Spec OUT OF SCOPE: "`attempt_remediation()` full integration (noted as v3.3 deferral in code)" | OQ-5 correctly aligns with the spec's out-of-scope declaration. **No spec gap.** |
| 6 | FR-2.4 checkpoint frequency | FR-2.4 says "Assert: `available()` = `initial_budget - consumed + reimbursed` holds at every checkpoint" — frequency unspecified | OQ-6 is an implementation recommendation. The spec's "every checkpoint" is vague; OQ-6 reasonably interprets it as "after each phase." **No spec gap.** |
| 7 | Pre-existing 3 failures | Spec constraint: "Baseline: 4894 passed, 3 pre-existing failures" | See CC4-2 — this IS a spec constraint and the open question treatment introduces ambiguity. **Covered in CC4-2.** |
| 8 | Reachability gate CI placement | FR-4.3 says gate "integrates with existing GateCriteria infrastructure" — placement unspecified | OQ-8 is an implementation recommendation. The spec requires integration but not specific placement. **No spec gap.** |

### CC4-15: OQ-4 Wiring Manifest Location — Implied Spec Constraint
- **Type**: INADEQUATE_COVERAGE
- **Spec source**: Test File Layout section — "tests/v3.3/wiring_manifest.yaml" appears explicitly in the file tree. Constraints section — "Spec-driven manifest: Wiring manifest is the source of truth for reachability gate."
- **Roadmap response**: Open Question 4 recommends "Standalone `.yaml` file in the release directory (`tests/v3.3/wiring_manifest.yaml`)." This correctly aligns with the spec layout, but the roadmap treats the location as a recommendation (Open Questions section) rather than as a constraint derived from the spec.
- **Severity**: LOW
- **Gap description**: The spec's Test File Layout explicitly includes `tests/v3.3/wiring_manifest.yaml`. This is not an open question — the spec answers it. The roadmap's OQ-4 recommendation happens to be correct, but treating it as an open question (rather than a spec-derived constraint) risks a developer choosing a different location without realizing it violates the spec.
- **Impact**: Low — the recommendation is correct. Risk only arises if the open question is resolved differently than recommended.
- **Recommended correction**: Close OQ-4 in the roadmap by replacing it with a statement: "Manifest location: `tests/v3.3/wiring_manifest.yaml` — per spec Test File Layout section (not an open question)."

---

## Summary

### Gaps Found: 12

| ID | Title | Type | Severity |
|----|-------|------|----------|
| CC4-1 | Code State Snapshot — no repeatable verification task | INADEQUATE_COVERAGE | MEDIUM |
| CC4-2 | Open Question 7 treats baseline failure count as negotiable | INADEQUATE_COVERAGE | MEDIUM |
| CC4-3 | FR-1.19 (SHADOW_GRACE_INFINITE) absent from roadmap task table | INADEQUATE_COVERAGE | HIGH |
| CC4-4 | FR-1.20 (__post_init__ derivation) absent from roadmap task table | MISSED_EXTRACTION | HIGH |
| CC4-5 | FR-1.21 (check_wiring_report wrapper) inadequately covered in 2A.3 | INADEQUATE_COVERAGE | MEDIUM |
| CC4-6 | FR-2.1a (handle_regression() behavioral test) absent from roadmap | INADEQUATE_COVERAGE | HIGH |
| CC4-7 | Branch constraint present — no gap | — | (CLOSED) |
| CC4-8 | Baseline numbers in task 4.1 correct — no gap | — | (CLOSED) |
| CC4-9 | UV-only constraint undocumented enforcement | INADEQUATE_COVERAGE | LOW |
| CC4-10 | Audit trail enforcement not stated for Phase 2D and 3B tests | CROSS_CUTTING_GAP | HIGH |
| CC4-11 | Task 4.4 wording over-broad vs. actual manifest scope | INADEQUATE_COVERAGE | MEDIUM |
| CC4-12 | tests/roadmap/conftest.py integration risk not addressed | CROSS_CUTTING_GAP | MEDIUM |
| CC4-15 | OQ-4 treats spec-defined manifest location as open question | INADEQUATE_COVERAGE | LOW |

**Total actionable gaps: 11** (CC4-7 and CC4-8 closed with no action needed)

### Orphan Tasks Found: 2

| ID | Task | Has Spec Backing | Severity |
|----|------|-----------------|----------|
| CC4-13 | Task 4.5 — "—" in requirement column, but FR-6.1 T14 exists | PARTIAL (notational error) | LOW |
| CC4-14 | Task 4.6 — Update solutions_learned.jsonl | NO | LOW |

**Total orphan tasks: 2** (1 notational error, 1 true orphan)

### Critical Findings Summary (HIGH severity)

The three HIGH-severity gaps require immediate roadmap remediation before implementation begins:

1. **CC4-3** (FR-1.19): SHADOW_GRACE_INFINITE has no roadmap task. Add task 2A.13.
2. **CC4-4** (FR-1.20): __post_init__ derivation has no roadmap task. Add task 2A.14.
3. **CC4-6** (FR-2.1a): handle_regression() behavioral test is absent. Add to task 2B.1 or add task 2B.1a.
4. **CC4-10** (Audit trail): Phase 2D and 3B tests have no explicit audit trail mandate. Update task descriptions and Checkpoint C.
