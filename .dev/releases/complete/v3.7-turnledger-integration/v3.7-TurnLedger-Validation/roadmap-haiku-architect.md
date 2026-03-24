---
spec_source: v3.3-requirements-spec.md
complexity_score: 0.82
primary_persona: architect
---

# 1. Executive summary

This roadmap delivers v3.3 TurnLedger Validation as a high-complexity, test-heavy release focused on proving production-path fidelity across sprint execution, convergence checking, wiring gates, and auditability.

## Architectural priorities

1. **Protect production-path realism**
   - Satisfy `NFR-1` by testing real orchestration and gate behavior end-to-end.
   - Limit injection to `_subprocess_factory` only.

2. **Separate test expansion from production fixes**
   - Most scope is validation and infrastructure.
   - Production changes remain constrained to `FR-5.1`, `FR-5.2`, and `FR-4.3`.

3. **Establish explicit source-of-truth artifacts**
   - Wiring manifest for reachability (`FR-4.1`, `NFR-5`)
   - JSONL audit trail for third-party verification (`FR-7.1`, `FR-7.2`, `FR-7.3`, `NFR-4`)

4. **Sequence by dependency**
   - Foundation artifacts first
   - E2E/integration validation second
   - Static-analysis gates and pipeline fixes third
   - Full regression and acceptance fourth

## Delivery intent

By the end of the roadmap, the release should:
- Prove all required wiring points are reachable and exercised (`FR-1`, `SC-1`)
- Validate TurnLedger lifecycle behavior across all execution paths (`FR-2`, `SC-2`)
- Cover rollout modes and budget exhaustion behavior without mocks (`FR-3`, `SC-3`, `SC-6`)
- Add reachability and fidelity guardrails to the pipeline (`FR-4`, `FR-5`, `SC-7`, `SC-9`, `SC-10`, `SC-11`)
- Produce independently verifiable audit records for every test (`FR-7`, `SC-12`)
- Preserve baseline regression expectations (`NFR-3`, `SC-4`)

---

# 2. Phased implementation plan with milestones

## Phase 0 — Specification lock and architecture decisions

### Objectives
1. Resolve open questions that materially affect implementation shape.
2. Freeze artifact locations, fixture scope, and acceptance boundaries.
3. Establish traceability matrix from requirement IDs to files/tests.

### Key tasks
1. Confirm unresolved requirements:
   - `FR-3.3` signal choice and simulation method
   - `FR-5.2` evidence granularity
   - `FR-7.3` fixture scope
   - `FR-4.1` manifest runtime location
   - `FR-2.4` checkpoint definition
   - `NFR-3` identity of pre-existing failures

2. Produce a requirement-to-deliverable map for:
   - `FR-1.1` through `FR-1.18`
   - `FR-2.1` through `FR-2.4`
   - `FR-3.1a` through `FR-3.3`
   - `FR-4.1` through `FR-4.4`
   - `FR-5.1` through `FR-5.3`
   - `FR-6.1`, `FR-6.2`
   - `FR-7.1` through `FR-7.3`

3. Freeze directory layout consistent with constraints:
   - `tests/v3.3/`
   - `tests/roadmap/`
   - `tests/audit-trail/`

### Milestone
- **M0: Architecture decision record approved**
  - All open questions either resolved or explicitly time-boxed with defaults.
  - Traceability matrix exists for all 13 top-level requirements.

---

## Phase 1 — Foundation artifacts and test infrastructure

### Objectives
1. Build the infrastructure required by later phases.
2. Create authoritative artifacts before feature-specific tests depend on them.
3. Enable independent verification.

### Scope
- `FR-4.1`
- `FR-7.1`
- `FR-7.3`
- `NFR-4`
- `NFR-5`
- `NFR-6`

### Key tasks

#### 1. Wiring manifest foundation (`FR-4.1`, `NFR-5`)
1. Define YAML schema with:
   - `entry_points`
   - `required_reachable`
   - spec references per target
2. Populate initial manifest with all required wiring targets from `FR-1` and `FR-6.2`.
3. Store manifest in a stable, reviewable location adjacent to v3.3 release assets.

#### 2. Audit trail infrastructure (`FR-7.1`, `FR-7.3`, `NFR-4`)
1. Implement `audit_trail` fixture.
2. Ensure each record includes:
   - `test_id`
   - `spec_ref`
   - `timestamp`
   - `assertion_type`
   - `inputs`
   - `observed`
   - `expected`
   - `verdict`
   - `evidence`
3. Auto-flush records to JSONL during execution.
4. Produce summary report at run end with:
   - total
   - passed
   - failed
   - wiring coverage

#### 3. AST analyzer skeleton and limitations contract (`FR-4.2`, `NFR-6`)
1. Define standalone analyzer module boundary.
2. Document included/excluded behaviors:
   - include lazy imports inside functions
   - exclude `TYPE_CHECKING`
   - document false negatives for dynamic dispatch and `getattr`

### Milestone
- **M1: Foundation artifacts operational**
  - Manifest schema committed and populated.
  - `audit_trail` fixture available and emitting valid JSONL.
  - Reachability analyzer contract documented and testable in isolation.

---

## Phase 2 — E2E and integration validation suites

### Objectives
1. Prove existing production wiring and TurnLedger behavior through real code paths.
2. Close core QA gaps before adding new gate logic.
3. Validate observable outputs written to `results_dir`.

### Scope
- `FR-1.1` through `FR-1.18`
- `FR-2.1` through `FR-2.4`
- `FR-3.1a` through `FR-3.3`
- `FR-6.1`
- `FR-6.2`
- `SC-1`, `SC-2`, `SC-3`, `SC-5`, `SC-6`, `SC-8`, `SC-12`

### Key workstreams

#### 1. Wiring-point E2E suite (`FR-1`)
1. Validate object construction and ordering:
   - `FR-1.1`
   - `FR-1.2`
   - `FR-1.3`
   - `FR-1.4`
2. Validate execution path selection:
   - `FR-1.5`
   - `FR-1.6`
3. Validate hook and return-shape contracts:
   - `FR-1.7`
   - `FR-1.8`
4. Validate accumulation, logging, KPI, and mode resolution:
   - `FR-1.9`
   - `FR-1.10`
   - `FR-1.11`
   - `FR-1.12`
   - `FR-1.13`
5. Validate remediation lifecycle and convergence argument signatures:
   - `FR-1.14`
   - `FR-1.14a`
   - `FR-1.14b`
   - `FR-1.14c`
   - `FR-1.15`
   - `FR-1.16`
   - `FR-1.17`
   - `FR-1.18`

#### 2. TurnLedger lifecycle suites (`FR-2`)
1. Convergence path:
   - `FR-2.1`
2. Sprint per-task path:
   - `FR-2.2`
3. Sprint per-phase path:
   - `FR-2.3`
4. Cross-path coherence path:
   - `FR-2.4`

#### 3. Rollout-mode and exhaustion matrix (`FR-3`)
1. Gate modes for both execution paths:
   - `FR-3.1a`
   - `FR-3.1b`
   - `FR-3.1c`
   - `FR-3.1d`
2. Exhaustion scenarios:
   - `FR-3.2a`
   - `FR-3.2b`
   - `FR-3.2c`
   - `FR-3.2d`
3. Interrupt handling:
   - `FR-3.3`

#### 4. Remaining QA gaps (`FR-6`)
1. v3.05:
   - `FR-6.1` / `T07`
   - `FR-6.1` / `T11`
   - `FR-6.1` / `T12`
   - `FR-6.1` / `T14`
2. v3.2:
   - `FR-6.2` / `T02`
   - `FR-6.2` / `T17-T22`

### Milestone
- **M2: Validation suites green**
  - All required E2E and integration suites exist and run under UV.
  - KPI, remediation, interrupt, and budget assertions are evidence-backed.
  - Audit trail records exist for every test.

---

## Phase 3 — Static-analysis gate and production pipeline fixes

### Objectives
1. Add missing guardrails to detect unreachable or unimplemented behavior.
2. Fix pipeline silent-pass behavior.
3. Integrate new checks into existing pipeline infrastructure with minimal production-surface change.

### Scope
- `FR-4.2`
- `FR-4.3`
- `FR-4.4`
- `FR-5.1`
- `FR-5.2`
- `FR-5.3`
- `SC-7`, `SC-9`, `SC-10`, `SC-11`

### Key tasks

#### 1. Reachability analyzer implementation (`FR-4.2`)
1. Build AST parse pipeline using stdlib `ast`.
2. Implement call graph extraction.
3. Implement cross-module import resolution.
4. Support lazy imports inside functions.
5. Preserve explicit documented limitations per `NFR-6`.

#### 2. Reachability gate integration (`FR-4.3`, `FR-5.3`)
1. Load manifest from `FR-4.1`.
2. Run graph traversal from declared entry points.
3. Emit structured PASS/FAIL output through `GateCriteria`.
4. Ensure spec references are surfaced in failures.

#### 3. Reachability regression proof (`FR-4.4`)
1. Remove or simulate missing `run_post_phase_wiring_hook()` linkage in regression test.
2. Verify detection references `v3.2-T02`.

#### 4. Silent-pass fix (`FR-5.1`)
1. Detect `files_analyzed == 0` with non-empty source directory.
2. Return FAIL with `failure_reason`.
3. Verify existing failing tests are not destabilized beyond intended change.

#### 5. Impl-vs-spec fidelity checker (`FR-5.2`)
1. Add checker module.
2. Search for implementation evidence against spec requirements.
3. Integrate into `_run_checkers()`.
4. Validate with synthetic missing-implementation scenario.

### Milestone
- **M3: Pipeline guardrails active**
  - Reachability gate runs within existing gate infrastructure.
  - Silent-pass condition is converted to deterministic FAIL.
  - Impl-vs-spec fidelity checker participates in convergence checker orchestration.

---

## Phase 4 — Full-system validation and release readiness

### Objectives
1. Validate aggregate behavior under real suite conditions.
2. Confirm baseline regression guardrails.
3. Produce release evidence suitable for external review.

### Scope
- `NFR-2`
- `NFR-3`
- `SC-4`
- cross-phase acceptance

### Key tasks
1. Run all targeted suites with `uv run pytest`.
2. Run full regression baseline validation:
   - `SC-4`
3. Validate all generated artifacts under `results_dir`:
   - KPI report
   - remediation log
   - audit trail JSONL
4. Perform manual third-party verifiability review:
   - `FR-7.2`
   - `SC-12`
5. Confirm branch and release constraints remain satisfied.

### Milestone
- **M4: Release acceptance complete**
  - Full-suite thresholds met.
  - No prohibited production edits beyond allowed items.
  - Evidence package is reviewable without tribal knowledge.

---

# 3. Integration points

Below are the required explicit wiring mechanisms and how they are phased.

## 1. Dependency injection mechanism

### `_subprocess_factory`
- **Named Artifact**: `_subprocess_factory`
- **Wired Components**:
  - deterministic subprocess replacement for external `claude` binary
  - real internal orchestration path remains untouched
- **Owning Phase**: Phase 1 defines common usage pattern; Phase 2 consumes it in all E2E/integration suites
- **Cross-Reference**: Consumed by Phase 2 tests for `FR-1`, `FR-2`, `FR-3`, `FR-6`
- **Architect note**: This is the sole allowed injection seam under `NFR-1`; all test harnesses must standardize on it.

## 2. Execution-path dispatch mechanism

### Phase execution routing inside sprint executor
- **Named Artifact**: executor phase delegation branch (`execute_phase_tasks()` vs `ClaudeProcess` fallback)
- **Wired Components**:
  - task inventory path for phases with `### T01.01` headings
  - freeform path via `ClaudeProcess`
- **Owning Phase**: Phase 2 validates both branches via `FR-1.5`, `FR-1.6`, `FR-2.2`, `FR-2.3`, `FR-2.4`
- **Cross-Reference**: Phase 3 reachability analysis must prove both routes remain reachable where declared in manifest
- **Architect note**: This is a critical branch point, not just a code branch; it is a platform-level dispatch seam and must remain explicitly covered.

## 3. Callback wiring mechanism

### `run_post_phase_wiring_hook()`
- **Named Artifact**: `run_post_phase_wiring_hook()`
- **Wired Components**:
  - per-task completion path
  - per-phase / `ClaudeProcess` completion path
- **Owning Phase**: Phase 2 proves both call sites through `FR-1.7`; Phase 3 uses `FR-4.4` to detect broken reachability
- **Cross-Reference**: Consumed by audit expectations, KPI accuracy (`FR-1.11`), and reachability regression gate (`FR-4.4`)
- **Architect note**: This is the highest-value wiring callback because it connects execution, gating, logging, and downstream metrics.

## 4. Strategy-resolution mechanism

### `_resolve_wiring_mode()`
- **Named Artifact**: `_resolve_wiring_mode()`
- **Wired Components**:
  - mode `off`
  - mode `shadow`
  - mode `soft`
  - mode `full`
- **Owning Phase**: Phase 2 validates resolver usage and mode semantics via `FR-1.12`, `FR-3.1a`, `FR-3.1b`, `FR-3.1c`, `FR-3.1d`
- **Cross-Reference**: Phase 4 acceptance uses mode matrix outcomes as release evidence
- **Architect note**: Treat this as the authoritative strategy selector; direct config reads are architectural drift.

## 5. Gate infrastructure registry

### `GateCriteria` infrastructure
- **Named Artifact**: `GateCriteria` infrastructure
- **Wired Components**:
  - existing structural checks
  - existing semantic checks
  - new reachability gate from `FR-4.3`
- **Owning Phase**: Phase 3 integrates reachability gate
- **Cross-Reference**: Phase 4 validates end-to-end gate outputs and regression thresholds
- **Architect note**: New checks must join the existing framework, not bypass it, to preserve consistent diagnostics and rollout semantics.

## 6. Checker orchestration registry

### `_run_checkers()`
- **Named Artifact**: `_run_checkers()`
- **Wired Components**:
  - structural checker layer
  - semantic checker layer
  - new impl-vs-spec fidelity checker from `FR-5.2`
- **Owning Phase**: Phase 3
- **Cross-Reference**: Consumed by `FR-2.1`, `FR-5.2`, `SC-11`
- **Architect note**: This is the convergence checker dispatch table in practice; additions must preserve ordering, output shape, and failure aggregation.

## 7. Convergence findings merge registry

### `registry.merge_findings()`
- **Named Artifact**: `registry.merge_findings()`
- **Wired Components**:
  - structural findings list
  - semantic findings list
  - `run_number`
- **Owning Phase**: Phase 2 validates invocation contract under `FR-1.16`
- **Cross-Reference**: Phase 3 relies on this merge path remaining stable when new checker output is added
- **Architect note**: Signature stability matters because Phase 3 extends upstream checker production.

## 8. Convergence registry constructor

### convergence registry initialization
- **Named Artifact**: convergence registry constructor `(path, release_id, spec_hash)`
- **Wired Components**:
  - artifact path
  - release identifier
  - spec hash
- **Owning Phase**: Phase 2 validates argument contract under `FR-1.15`
- **Cross-Reference**: Supports Phase 3 checker/gate output integrity and Phase 4 artifact verification
- **Architect note**: This is an integration boundary between release identity and convergence state.

---

# 4. Risk assessment and mitigation strategies

## R-1 (HIGH): Reachability analyzer misses lazy-import paths
### Impact
False negatives weaken `FR-4.2`, `FR-4.3`, `FR-4.4`, `SC-7`, and `SC-9`.

### Mitigation
1. Implement function-scope import extraction first, before broader graph features.
2. Add known-good executor-path fixtures that exercise lazy import patterns.
3. Keep manifest entries narrow and explicit to reduce ambiguity.
4. Document exclusions per `NFR-6` so failures are interpretable.

### Exit criteria
- Analyzer correctly resolves at least one representative lazy-import case from target code paths.

## R-2 (MEDIUM): E2E flakiness from subprocess timing
### Impact
Undermines confidence in `FR-1`, `FR-2`, `FR-3`, and `SC-12`.

### Mitigation
1. Standardize on `_subprocess_factory` for deterministic external command replacement.
2. Keep real subprocess smoke checks isolated from core regression suites.
3. Capture durations and runtime values into audit records to distinguish flake from logic regressions.

### Exit criteria
- Core validation suites run deterministically without timing-based retries.

## R-3 (MEDIUM): Impl-vs-spec checker over-reports gaps
### Impact
Causes noisy failures in `FR-5.2` and weakens credibility of `SC-11`.

### Mitigation
1. Start with explicit evidence rules:
   - exact symbol matches
   - declared spec references where present
   - stable class/function identifiers
2. Avoid semantic inference in v3.3.
3. Add synthetic positive and negative tests before enabling broad assertions.

### Exit criteria
- Checker passes known-good synthetic cases and flags known-bad synthetic cases with low ambiguity.

## R-4 (LOW): Audit trail growth becomes operationally noisy
### Impact
Affects usability of `FR-7.1`-`FR-7.3`, not correctness.

### Mitigation
1. Use one JSONL per run.
2. Rotate by timestamp.
3. Keep summary output compact and deterministic.

### Exit criteria
- Artifacts remain bounded per run and easy to inspect.

## R-5 (LOW): Silent-pass fix destabilizes existing pipeline expectations
### Impact
Could violate `NFR-3` and `SC-4`.

### Mitigation
1. Identify pre-existing failures before patching.
2. Add targeted regression tests around `FR-5.1`.
3. Land the assertion as an additive failure condition with explicit `failure_reason`.

### Exit criteria
- Full suite shows only intended behavior change; no unexpected regression expansion.

---

# 5. Resource requirements and dependencies

## Team roles

1. **Architect / technical lead**
   - owns Phase 0 decisions
   - validates integration boundaries
   - approves manifest schema and checker integration

2. **Backend / pipeline engineer**
   - implements `FR-4.2`, `FR-4.3`, `FR-5.1`, `FR-5.2`

3. **QA / test engineer**
   - owns `FR-1`, `FR-2`, `FR-3`, `FR-6`, `FR-7`

4. **Release verifier**
   - validates `NFR-3`, `SC-4`, `SC-12`

## Technical dependencies

1. **`ast` stdlib**
   - required for `FR-4.2`

2. **`pytest >= 7.0.0`**
   - required for `FR-7.3` and all suite work

3. **`_subprocess_factory`**
   - required for `NFR-1`, `FR-1`, `FR-2`, `FR-3`

4. **`GateCriteria` infrastructure**
   - required for `FR-4.3`

5. **`_run_checkers()`**
   - required for `FR-5.2`

6. **`wiring_gate.py:run_wiring_analysis()`**
   - required for `FR-5.1`

7. **`v3.0-v3.2-Fidelity` branch**
   - required architectural baseline

8. **JSONL schema contract**
   - required for `FR-7.1`, `FR-7.2`, `FR-7.3`

## Environment requirements

1. All Python execution via UV (`NFR-2`)
2. Output artifacts written under `results_dir`
3. No production edits beyond:
   - `FR-5.1`
   - `FR-5.2`
   - `FR-4.3`

---

# 6. Success criteria and validation approach

## Requirement-level validation strategy

### E2E and integration fidelity
1. Validate all wiring points with production-path tests:
   - `FR-1.1` through `FR-1.18`
2. Validate all ledger lifecycle paths:
   - `FR-2.1` through `FR-2.4`
3. Validate all rollout modes and exhaustion states:
   - `FR-3.1a` through `FR-3.3`

### Static-analysis and pipeline guardrails
1. Validate manifest-driven reachability:
   - `FR-4.1`
   - `FR-4.2`
   - `FR-4.3`
   - `FR-4.4`
2. Validate pipeline correctness fixes:
   - `FR-5.1`
   - `FR-5.2`
   - `FR-5.3`

### QA closure and auditability
1. Close gap suites:
   - `FR-6.1`
   - `FR-6.2`
2. Prove third-party verifiability:
   - `FR-7.1`
   - `FR-7.2`
   - `FR-7.3`

## Success criteria mapping

1. **`SC-1`**
   - Validate coverage matrix maps all `FR-1` wiring points to passing tests.

2. **`SC-2`**
   - Validate four TurnLedger lifecycle paths pass and preserve accounting invariants.

3. **`SC-3`**
   - Validate 4 rollout modes × 2 execution paths.

4. **`SC-4`**
   - Run full suite and confirm `≥ 4894 passed`, `≤ 3 pre-existing failures`.

5. **`SC-5`**
   - Compare KPI fields in produced report against expected runtime values.

6. **`SC-6`**
   - Validate all four budget exhaustion scenarios.

7. **`SC-7`**
   - Break known wiring path and confirm eval framework detects it.

8. **`SC-8`**
   - Confirm all listed v3.05 and v3.2 QA gap tests are green.

9. **`SC-9`**
   - Confirm reachability gate flags intentionally broken wiring with correct spec ref.

10. **`SC-10`**
    - Confirm 0-files-analyzed returns FAIL with explicit reason.

11. **`SC-11`**
    - Confirm impl-vs-spec checker detects at least one synthetic gap.

12. **`SC-12`**
    - Manual review confirms audit trail supports independent verification.

## Validation checkpoints

1. **Checkpoint A — after Phase 1**
   - schema validity
   - fixture output validity
   - analyzer contract completeness

2. **Checkpoint B — after Phase 2**
   - all runtime-path assertions evidence-backed
   - QA gaps materially closed

3. **Checkpoint C — after Phase 3**
   - new gates integrated, not standalone
   - synthetic regressions caught deterministically

4. **Checkpoint D — after Phase 4**
   - full-suite acceptance and artifact review complete

---

# 7. Timeline estimates per phase

## Overall estimate
Given `complexity_score: 0.82` and high coupling, this should be planned as a **4-phase delivery with explicit checkpoints**, not a single implementation burst.

## Phase estimates

### Phase 0 — Specification lock and architecture decisions
- **Estimate**: 0.5-1 day
- **Outputs**:
  - decision log
  - traceability matrix
  - resolved defaults for open questions

### Phase 1 — Foundation artifacts and test infrastructure
- **Estimate**: 1-2 days
- **Outputs**:
  - manifest schema and initial contents
  - `audit_trail` fixture
  - analyzer contract and isolated tests

### Phase 2 — E2E and integration validation suites
- **Estimate**: 3-5 days
- **Outputs**:
  - wiring-point suites
  - ledger lifecycle suites
  - rollout-mode and exhaustion suites
  - QA gap closure suites

### Phase 3 — Static-analysis gate and production pipeline fixes
- **Estimate**: 2-4 days
- **Outputs**:
  - AST reachability analyzer
  - reachability gate integration
  - 0-files-analyzed fix
  - impl-vs-spec checker integration

### Phase 4 — Full-system validation and release readiness
- **Estimate**: 1-2 days
- **Outputs**:
  - full regression run
  - acceptance evidence package
  - third-party verifiability review

## Recommended milestone cadence
1. **M0** at end of Day 1
2. **M1** by Day 2-3
3. **M2** by Day 5-8
4. **M3** by Day 7-11
5. **M4** by Day 8-13

---

# 8. Final architect recommendations

1. **Do not start `FR-4.2` before `FR-4.1` is frozen**
   - The manifest is the contract; otherwise reachability work will drift.

2. **Treat `FR-1.7` and `FR-4.4` as architectural sentinels**
   - They validate the most important callback seam in the system.

3. **Land Phase 2 before broadening Phase 3**
   - Existing-path proof should precede new analysis logic.

4. **Keep `FR-5.2` intentionally conservative**
   - v3.3 needs reliable evidence-based checking, not ambitious semantic matching.

5. **Use audit trail outputs as release evidence, not just test exhaust**
   - `FR-7.2` and `SC-12` are release-trust features, not bookkeeping.

6. **Enforce requirement-ID traceability in every artifact**
   - Preserve exact IDs such as `FR-1.14a`, `FR-3.1d`, `SC-11`, and gap IDs `T07`, `T11`, `T02`, `T17-T22` unchanged throughout implementation and reporting.
