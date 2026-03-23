# Gap Remediation Tasklist: v3.05 Deterministic Fidelity Gates

**Generated**: 2026-03-21
**Source**: `roadmap-gap-analysis-merged.md`
**Branch**: v3.0-AuditGates

---

## Summary

| Metric | Value |
|---|---|
| **Total tasks** | 15 |
| **Waves** | 5 |
| **Source recommendations** | P0 (3 bugs), P1 (2 spec deviations), P2 (3 medium gaps), P3 (3 low gaps) |
| **Critical blockers** | Tasks 1-3 (all convergence-mode execution blocked) |
| **Estimated effort** | Small — bulk of fixes in ~60 lines of `executor.py:560-620` |

---

## Dependency Graph

```
Wave 1 (P0 crash fixes — all independent, same file):
  T01 ──┐
  T02 ──┼──> Wave 2 (P1 budget config)
  T03 ──┘
          T04 ──┐
          T05 ──┼──> Wave 3 (verification + tests)
                │
                ├──> T06 (verify remediation deliverables)
                ├──> T07 (integration test)
                ├──> T08 (fix wiring-verification target)
                │
                └──> Wave 4 (P3 diagnostics)
                      T09 (budget_snapshot field)
                      T10 (progress proof logging)
                      T11 (E2E test artifacts)
                      │
                      └──> Wave 5 (final validation)
                            T12 (smoke test convergence path)
                            T13 (run full test suite)
                            T14 (update wiring-verification)
```

---

## Wave 1: P0 Critical — Fix Runtime Crash Bugs

These three tasks are independent of each other but all must complete before Wave 2. All target `src/superclaude/cli/roadmap/executor.py`.

---

### Task 01: Fix `DeviationRegistry.load_or_create()` call signature
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py` (line 566)
- **Description**:
  1. At line 566, `DeviationRegistry.load_or_create()` is called with 1 positional arg (path only).
  2. The method signature at `convergence.py:100` requires 3: `(path, release_id, spec_hash)`.
  3. `hashlib` is already imported at module level (executor.py line 14). No additional import needed.
  4. Before the `load_or_create` call, compute: `spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()`
  5. Replace line 566 with:
     ```python
     registry = DeviationRegistry.load_or_create(
         config.output_dir / "deviation-registry.json",
         release_id=config.output_dir.name,
         spec_hash=spec_hash,
     )
     ```
  6. Note: `hashlib` is already imported at executor.py line 14 (module-level). No additional import needed.
- **Source recommendation**: P0-1 (Bug B1)
- **Depends on**: none
- **Acceptance criteria**:
  - `DeviationRegistry.load_or_create()` receives all 3 required arguments.
  - No `TypeError` on convergence-mode invocation.
  - `release_id` matches the output directory name (consistent with roadmap convention).
  - `spec_hash` is computed from the actual spec file bytes (enables FR-6 spec-change reset).
- **Risk**: If `config.spec_file` does not exist at call time, `read_bytes()` will raise `FileNotFoundError`. This is acceptable — the spec file must exist for any fidelity run.
- **Wave**: 1

---

### Task 02: Fix `merge_findings()` call arity (structural + semantic split)
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py` (lines 587, 599)
- **Description**:
  1. `merge_findings()` signature at `convergence.py:143` is: `(structural: list[Finding], semantic: list[Finding], run_number: int)`.
  2. Line 587 calls `reg.merge_findings(structural_findings, run_number)` — passes structural as first arg, run_number as second, missing semantic list. Fix to:
     ```python
     reg.merge_findings(structural_findings, [], run_number)
     ```
  3. Line 599 calls `reg.merge_findings(semantic_result.findings, run_number)` — passes semantic as first arg (structural position), run_number as second. Fix to:
     ```python
     reg.merge_findings([], semantic_result.findings, run_number)
     ```
  4. This preserves BF-3 (structural-only monotonic progress) by keeping the structural/semantic split correct in the registry.
- **Source recommendation**: P0-2 (Bug B2)
- **Depends on**: none
- **Acceptance criteria**:
  - Both `merge_findings()` calls pass 3 arguments.
  - Structural findings are passed in the `structural` parameter position only.
  - Semantic findings are passed in the `semantic` parameter position only.
  - `run_number` is always the third argument.
  - Registry correctly tracks `source_layer` as "structural" or "semantic" per finding origin.
- **Risk**: If `structural_findings` or `semantic_result.findings` are not `list[Finding]` (e.g., list of dicts), merge_findings may fail on attribute access inside the loop. Verify `run_all_checkers()` return type matches `list[Finding]`.
- **Wave**: 1

---

### Task 03: Fix dict/object attribute access mismatch in remediation
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py` (lines 611-613)
- **Description**:
  1. `get_active_highs()` at `convergence.py:201-206` returns `list[dict]` — registry stores findings as JSON dicts, not `Finding` dataclass instances.
  2. Line 612 uses `finding.files_affected` (attribute access), which raises `AttributeError` on a dict.
  3. Replace the entire `_run_remediation()` function body (lines 603-620) to:
     - Convert registry dicts back to Finding dataclass instances before calling `execute_remediation()`.
     - Use attribute access on Finding objects (which `execute_remediation()` expects).
     ```python
     def _run_remediation(reg: DeviationRegistry) -> None:
         """Run remediation on active HIGH findings."""
         from .models import Finding
         active_highs = reg.get_active_highs()
         if not active_highs:
             return

         # Convert registry dicts to Finding dataclass instances
         # (registry stores JSON dicts, execute_remediation expects Finding objects)
         finding_objects = []
         for d in active_highs:
             finding_objects.append(Finding(
                 id=d.get("stable_id", ""),
                 severity=d.get("severity", "HIGH"),
                 dimension=d.get("dimension", ""),
                 description=d.get("description", ""),
                 location=d.get("location", ""),
                 evidence="",
                 fix_guidance="",
                 files_affected=d.get("files_affected", []),
                 status=d.get("status", "ACTIVE"),
             ))

         # Group by file using Finding objects
         findings_by_file: dict[str, list] = {}
         for finding in finding_objects:
             for f in finding.files_affected:
                 findings_by_file.setdefault(f, []).append(finding)

         execute_remediation(
             findings_by_file=findings_by_file,
             config=config,
             output_dir=config.output_dir,
             allow_regeneration=getattr(config, "allow_regeneration", False),
         )
     ```
  4. **CRITICAL**: `execute_remediation()` at `remediate_executor.py:733` expects `dict[str, list[Finding]]`. Passing raw dicts causes AttributeError crashes downstream (e.g., `finding.files_affected` at remediate_executor.py:172). The dict-to-Finding conversion above is mandatory, not optional.
- **Source recommendation**: P0-3 (Bug B3)
- **Depends on**: none
- **Acceptance criteria**:
  - Dict key access (`finding.get(...)`) replaces attribute access (`finding.files_affected`).
  - Graceful fallback to empty list when `files_affected` key is missing.
  - No `AttributeError` at runtime.
  - `execute_remediation()` receives the correct data structure (list of dicts per file).
- **Risk**: `DeviationRegistry.merge_findings()` does NOT store `files_affected` in registry dicts (see T15). Without T15, `d.get("files_affected", [])` always returns `[]`, making remediation unable to route findings to files. T03 and T15 must both be completed for remediation to function.
- **Wave**: 1

---

## Wave 2: P1 High — Fix Budget Configuration Spec Deviations

Both tasks target the same line region in `executor.py`. They should be applied together.

---

### Task 04: Use `MAX_CONVERGENCE_BUDGET` instead of `STD_CONVERGENCE_BUDGET`
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py` (line 571-572)
- **Description**:
  1. Line 571 imports `STD_CONVERGENCE_BUDGET` from convergence. Change to import `MAX_CONVERGENCE_BUDGET`.
  2. Line 572 constructs `TurnLedger(initial_budget=STD_CONVERGENCE_BUDGET)`. Change to `MAX_CONVERGENCE_BUDGET`.
  3. Update the import at line 571:
     ```python
     from .convergence import MAX_CONVERGENCE_BUDGET
     ```
  4. Update the constructor:
     ```python
     ledger = TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET)
     ```
  5. `MAX_CONVERGENCE_BUDGET = 61` (3 full cycles) per FR-7. `STD_CONVERGENCE_BUDGET = 46` only supports 2 full cycles.
- **Source recommendation**: P1-4 (Bug B4)
- **Depends on**: T01, T02, T03 (crash bugs must be fixed first to verify budget behavior)
- **Acceptance criteria**:
  - `TurnLedger.initial_budget` is set to 61 (MAX_CONVERGENCE_BUDGET).
  - Full 3-cycle convergence (catch/verify/backup) is possible without budget exhaustion.
  - FR-7 compliance verified.
- **Risk**: Higher budget means more turns consumed if convergence takes all 3 runs. This is the intended spec behavior.
- **Wave**: 2

---

### Task 05: Add missing TurnLedger constructor parameters
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py` (line 572)
- **Description**:
  1. The TurnLedger constructor at `sprint/models.py:530-538` accepts `minimum_allocation` (default 5) and `minimum_remediation_budget` (default 3).
  2. FR-7 requires `minimum_allocation=CHECKER_COST` (10) and `minimum_remediation_budget=REMEDIATION_COST` (8).
  3. Default `minimum_allocation=5` is less than `CHECKER_COST=10`, creating a guard hole where `can_launch()` returns True when budget is insufficient.
  4. Also add `reimbursement_rate=0.8` explicitly to match spec.
  5. Import the cost constants alongside `MAX_CONVERGENCE_BUDGET`:
     ```python
     from .convergence import MAX_CONVERGENCE_BUDGET, CHECKER_COST, REMEDIATION_COST
     ```
  6. Replace the TurnLedger construction (combined with T04):
     ```python
     ledger = TurnLedger(
         initial_budget=MAX_CONVERGENCE_BUDGET,
         minimum_allocation=CHECKER_COST,
         minimum_remediation_budget=REMEDIATION_COST,
         reimbursement_rate=0.8,
     )
     ```
- **Source recommendation**: P1-4 (Bug B5)
- **Depends on**: T04 (applied together as a single edit)
- **Acceptance criteria**:
  - `can_launch()` correctly rejects runs when `available() < CHECKER_COST`.
  - `minimum_remediation_budget` matches `REMEDIATION_COST` (8).
  - `reimbursement_rate` is explicitly 0.8.
  - No budget guard holes: every `can_launch() == True` guarantees enough budget for a full checker run.
- **Risk**: None — these are correct parameterizations of existing constructor args.
- **Wave**: 2

---

## Wave 3: P2 Medium — Verification and Integration Tests

These tasks can run in parallel after Waves 1-2 are complete.

---

### Task 06: Verify `remediate_executor.py` v3.05 deliverables
- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/roadmap/remediate_executor.py`
- **Description**:
  1. Confirm `RemediationPatch` dataclass exists (line 63 — VERIFIED in analysis, present).
  2. Confirm per-patch 30% diff-size threshold is implemented (line 312 — VERIFIED, `ratio > 0.30`).
  3. Confirm `fallback_apply()` exists (line 640 — VERIFIED, present).
  4. Confirm `check_morphllm_available()` exists (line 711 — VERIFIED, present).
  5. Read each function body to verify correctness against FR-9, D-0038, D-0039, D-0048:
     - `RemediationPatch` must have fields: `target_file`, `anchor_text`, `replacement_text`, `patch_original_lines`.
     - `check_patch_diff_size()` must compute `changed_lines / patch_original_lines` and reject if > 0.30.
     - `fallback_apply()` must perform deterministic text replacement using anchor matching.
     - `check_morphllm_available()` must probe MCP runtime and return bool.
  6. Document verification results (pass/fail per item) in the task output.
- **Source recommendation**: P2-5 (Bug B8)
- **Depends on**: none (read-only verification)
- **Acceptance criteria**:
  - All four deliverables confirmed present with correct behavior.
  - Any deviations from FR-9 spec documented for follow-up.
- **Risk**: Low — this is a verification task, not a code change.
- **Wave**: 3

---

### Task 07: Write integration test for `_run_convergence_spec_fidelity()`
- **Type**: test
- **Target file(s)**:
  - New: `tests/roadmap/test_convergence_wiring.py`
  - Reference: `tests/roadmap/test_convergence.py` (existing pattern)
  - Reference: `src/superclaude/cli/roadmap/executor.py` (function under test)
- **Description**:
  1. Create `tests/roadmap/test_convergence_wiring.py`.
  2. Test the full wiring path from `_run_convergence_spec_fidelity()` entry through to `ConvergenceResult`:
     - **Test 1**: `test_registry_construction` — Verify `load_or_create()` receives correct args (path, release_id, spec_hash). Use a mock spec file and config.
     - **Test 2**: `test_merge_findings_structural_only` — Verify structural checkers pass findings via `merge_findings(structural, [], run_number)`.
     - **Test 3**: `test_merge_findings_semantic_only` — Verify semantic results pass via `merge_findings([], semantic, run_number)`.
     - **Test 4**: `test_remediation_dict_access` — Verify `get_active_highs()` return (list of dicts) is consumed with dict key access, not attribute access.
     - **Test 5**: `test_turnledger_budget_params` — Verify ledger is constructed with `MAX_CONVERGENCE_BUDGET`, `minimum_allocation=CHECKER_COST`, `minimum_remediation_budget=REMEDIATION_COST`.
     - **Test 6**: `test_end_to_end_convergence_pass` — Full path: config -> registry -> checkers (mock returning 0 highs) -> convergence result with `passed=True`.
     - **Test 7**: `test_end_to_end_convergence_fail` — Full path with persistent HIGHs -> `passed=False`.
  3. Use `pytest.fixture` for `tmp_path`-based config, mock spec/roadmap files.
  4. Mock `run_all_checkers` and `run_semantic_layer` to return controlled findings.
  5. Follow existing test patterns from `test_convergence.py`.
- **Source recommendation**: P2-7 (Bug B10, root cause analysis)
- **Depends on**: T01, T02, T03, T04, T05 (tests validate the fixes)
- **Acceptance criteria**:
  - All 7 tests pass with `uv run pytest tests/roadmap/test_convergence_wiring.py -v`.
  - Tests would have caught B1-B5 if they existed before the sprint.
  - No mocking of the registry or ledger internals (test the real objects).
- **Risk**: May need to mock Claude subprocess calls in `run_semantic_layer`. Ensure mocks are targeted, not overly broad.
- **Wave**: 3

---

### Task 08: Fix wiring-verification target directory
- **Type**: fix
- **Target file(s)**: Wiring verification step configuration (investigate location)
- **Description**:
  1. The wiring-verification artifact at `.dev/releases/complete/v3.05_DeterministicFidelityGates/wiring-verification.md` shows `files_analyzed: 0` and `target_dir: /config/workspace/IronClaude/.dev/releases/current`.
  2. The target directory points to `.dev/releases/current` which is a directory of release folders, not source code. The wiring verification should scan `src/superclaude/cli/roadmap/` (the actual implementation directory).
  3. Investigate how `target_dir` is set:
     - Check the roadmap executor's wiring-verification step configuration.
     - Search for `wiring-verification` or `target_dir` in `executor.py` and related config files.
  4. Fix the target directory to point to `src/superclaude/cli/roadmap/` or the appropriate source directory.
  5. Re-run wiring verification to confirm it scans >0 files and produces meaningful results.
- **Source recommendation**: P2-6 (Bug B9)
- **Depends on**: none
- **Acceptance criteria**:
  - Wiring verification scans the correct directory containing `executor.py`, `convergence.py`, etc.
  - `files_analyzed > 0` in the output.
  - Any real wiring issues are surfaced.
- **Risk**: The target directory misconfiguration may be in the roadmap pipeline config rather than source code. Investigation step is needed.
- **Wave**: 3

---

## Wave 4: P3 Low — Diagnostics and Logging

These are non-blocking improvements. Can run in parallel.

---

### Task 09: Add `budget_snapshot` field to `RunMetadata`
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/convergence.py` (lines 72-84)
- **Description**:
  1. FR-10 specifies a `budget_snapshot` field in `RunMetadata` for diagnostic purposes.
  2. Add to the `RunMetadata` dataclass at line 84:
     ```python
     budget_snapshot: dict | None = None
     ```
  3. Populate the field in `execute_fidelity_with_convergence()` when creating/updating run metadata. After `registry.begin_run()` and `ledger.debit()`, store:
     ```python
     # In the convergence loop, after debit:
     if registry.runs:
         registry.runs[-1]["budget_snapshot"] = {
             "consumed": ledger.consumed,
             "reimbursed": ledger.reimbursed,
             "available": ledger.available(),
             "initial": ledger.initial_budget,
         }
     ```
  4. Ensure `save()` persists the snapshot (already handled by JSON serialization of runs list).
- **Source recommendation**: P3-8 (Bug B6)
- **Depends on**: T04, T05 (budget params must be correct for meaningful snapshots)
- **Acceptance criteria**:
  - `RunMetadata` dataclass includes `budget_snapshot: dict | None = None`.
  - Each run in the registry's `runs` list includes a `budget_snapshot` dict.
  - Snapshot contains `consumed`, `reimbursed`, `available`, `initial` keys.
- **Risk**: Low. Adding a defaulted field to a dataclass is backward-compatible.
- **Wave**: 4

---

### Task 10: Add budget state to progress proof log messages
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/convergence.py` (convergence loop, ~line 487-490)
- **Description**:
  1. FR-10 requires progress proof logs to include budget state in format: `"budget: consumed={c}, reimbursed={r}, available={a}"`.
  2. Currently, `progress_msg` at line 487-489 only logs structural counts.
  3. Append budget state to the progress message:
     ```python
     progress_msg = (
         f"Run {run_idx + 1} ({run_label}): "
         f"structural {prev_structural_highs} -> {curr_structural}, "
         f"budget: consumed={ledger.consumed}, reimbursed={ledger.reimbursed}, "
         f"available={ledger.available()}"
     )
     ```
  4. Also add budget info to the PASS log message at line 474-477 for completeness.
- **Source recommendation**: P3-9 (Bug B7)
- **Depends on**: T04, T05 (budget params must be correct for accurate logging)
- **Acceptance criteria**:
  - Every progress proof log line includes `budget: consumed=N, reimbursed=N, available=N`.
  - Log format matches FR-10 specification.
  - Existing `structural_progress` list entries include budget state.
- **Risk**: Low. Log message format change only.
- **Wave**: 4

---

### Task 11: Create persistent E2E verification test artifacts
- **Type**: test
- **Target file(s)**:
  - New: `tests/roadmap/test_convergence_e2e.py`
  - Reference: `src/superclaude/cli/roadmap/convergence.py` (SC-1 through SC-6)
- **Description**:
  1. The merged analysis notes no persistent E2E test artifacts for success criteria SC-1 through SC-6.
  2. Create `tests/roadmap/test_convergence_e2e.py` with tests mapped to each success criterion:
     - **SC-1**: Registry persistence — write registry, reload, verify findings survive.
     - **SC-2**: Monotonic progress — run 3 cycles, verify structural HIGHs never increase (or regression handler triggers).
     - **SC-3**: Budget exhaustion — set initial_budget to CHECKER_COST+1, verify halt after 1 run.
     - **SC-4**: Regression handling — inject increasing structural HIGHs, verify `handle_regression` is called.
     - **SC-5**: Convergence pass — inject 0 HIGHs on run 2, verify `passed=True` and CONVERGENCE_PASS_CREDIT applied.
     - **SC-6**: Semantic fluctuation tolerance — vary semantic HIGHs between runs, verify no halt (warning only).
  3. These tests use the real `DeviationRegistry` and `execute_fidelity_with_convergence()` with mock checkers/remediation.
  4. Mark all tests with `@pytest.mark.integration`.
- **Source recommendation**: P3-10 (Bug B10)
- **Depends on**: T01-T05 (all fixes applied), T07 (wiring tests pass)
- **Acceptance criteria**:
  - All 6 E2E tests pass.
  - Tests exercise the full convergence loop, not just individual components.
  - Each test name clearly maps to its success criterion (e.g., `test_sc1_registry_persistence`).
- **Risk**: E2E tests may be slower due to file I/O and multi-cycle convergence. Use `tmp_path` to avoid side effects.
- **Wave**: 4

---

## Wave 5: Final Validation

All implementation and test tasks must complete before this wave.

---

### Task 12: Smoke test convergence path end-to-end
- **Type**: verify
- **Target file(s)**: `src/superclaude/cli/roadmap/executor.py`
- **Description**:
  1. After all fixes (T01-T05), run a manual smoke test of the convergence path.
  2. Create a minimal test spec and roadmap in `tmp_path`.
  3. Invoke `_run_convergence_spec_fidelity()` with a real `RoadmapConfig` pointing to test files.
  4. Verify no `TypeError`, `AttributeError`, or other runtime exceptions.
  5. Verify the convergence result is a valid `ConvergenceResult` (not None, has expected fields).
  6. Verify the deviation registry JSON file is written to disk with correct structure.
  7. This can be a pytest test or a manual script execution.
- **Source recommendation**: Root cause analysis (no integration testing was performed)
- **Depends on**: T01, T02, T03, T04, T05
- **Acceptance criteria**:
  - `_run_convergence_spec_fidelity()` completes without runtime exceptions.
  - Returns a `StepResult` with valid status.
  - Deviation registry file exists on disk after execution.
- **Risk**: May require mocking Claude API calls if `run_semantic_layer` attempts real LLM calls.
- **Wave**: 5

---

### Task 13: Run full test suite
- **Type**: verify
- **Target file(s)**: All test files
- **Description**:
  1. Run `uv run pytest tests/ -v` to verify no regressions.
  2. Specifically ensure:
     - `tests/roadmap/test_convergence.py` — all existing tests still pass.
     - `tests/roadmap/test_convergence_wiring.py` — new wiring tests pass (T07).
     - `tests/roadmap/test_convergence_e2e.py` — new E2E tests pass (T11).
  3. Fix any failures introduced by T01-T05 changes.
- **Source recommendation**: General validation
- **Depends on**: T01-T11
- **Acceptance criteria**:
  - Zero test failures.
  - No new warnings related to convergence or executor imports.
- **Risk**: Existing tests may have been written assuming the buggy behavior (unlikely but possible). If so, update those tests.
- **Wave**: 5

---

### Task 14: Regenerate wiring-verification artifact
- **Type**: verify
- **Target file(s)**: `.dev/releases/complete/v3.05_DeterministicFidelityGates/wiring-verification.md`
- **Description**:
  1. After T08 fixes the target directory, re-run the wiring verification step.
  2. Verify the new artifact shows `files_analyzed > 0`.
  3. Review any findings for additional wiring issues not caught by the gap analysis.
  4. Archive the old artifact (0-files version) for audit trail.
- **Source recommendation**: P2-6 follow-up
- **Depends on**: T08
- **Acceptance criteria**:
  - `files_analyzed > 0` in the regenerated wiring-verification.md.
  - No CRITICAL or MAJOR findings (or all are addressed).
  - Artifact correctly reflects the post-fix state of the codebase.
- **Risk**: Wiring verification may surface additional issues beyond the 10 known bugs. These would need to be triaged and potentially added as follow-up tasks.
- **Wave**: 5

---

## Quick Reference: Task-to-Bug Mapping

| Task | Bug(s) | Severity | File | Lines |
|---|---|---|---|---|
| T01 | B1 | CRITICAL | executor.py | 566 |
| T02 | B2 | CRITICAL | executor.py | 587, 599 |
| T03 | B3 | CRITICAL | executor.py | 611-613 |
| T04 | B4 | HIGH | executor.py | 571-572 |
| T05 | B5 | HIGH | executor.py | 572 |
| T06 | B8 | MEDIUM | remediate_executor.py | (verify only) |
| T07 | B10 | MEDIUM | (new test file) | — |
| T08 | B9 | MEDIUM | wiring-verification config | — |
| T09 | B6 | LOW | convergence.py | 72-84 |
| T10 | B7 | LOW | convergence.py | 487-490 |
| T11 | B10 | MEDIUM | (new test file) | — |
| T12 | — | — | executor.py | (smoke test) |
| T13 | — | — | all tests | (regression check) |
| T14 | B9 | MEDIUM | wiring-verification.md | (regenerate) |
| T15 | (reflection) | CRITICAL | convergence.py | 168-180 |

## Wave Execution Summary

| Wave | Tasks | Parallelism | Gate |
|---|---|---|---|
| **Wave 1** | T01, T02, T03, T15 | All 4 in parallel | All pass; no new test failures |
| **Wave 2** | T04, T05 | Together (same edit region) | Budget params verified correct |
| **Wave 3** | T06, T07, T08 | All 3 in parallel | Verification complete; new tests pass |
| **Wave 4** | T09, T10, T11 | All 3 in parallel | Low-severity fixes applied; E2E tests pass |
| **Wave 5** | T12, T13, T14 | Sequential (T12 -> T13 -> T14) | Zero failures; wiring-verification scans >0 files |

---

## Post-Reflection Amendments

**Applied**: 2026-03-21 by reflection agent

### Amendment 1: T03 expanded to include dict-to-Finding conversion (CRITICAL)

**Reason**: T03 originally only fixed the immediate `AttributeError` at executor.py:612 by switching from attribute access to dict key access. However, `execute_remediation()` at `remediate_executor.py:733` expects `dict[str, list[Finding]]` -- passing raw dicts causes downstream crashes at `remediate_executor.py:172` and other sites that use `finding.files_affected` attribute access.

**Change**: Replaced the T03 code fix with a full `_run_remediation()` rewrite that converts registry dicts back to Finding dataclass instances before calling `execute_remediation()`.

### Amendment 2: T01 hashlib import note corrected

**Reason**: T01 notes 3 and 6 suggested adding `import hashlib` to `executor.py`. Verified that `hashlib` is already imported at module level (executor.py line 14). Notes updated to reflect this.

### Amendment 3: T15 added -- Store `files_affected` in registry (CRITICAL, Wave 1)

**Reason**: `DeviationRegistry.merge_findings()` at convergence.py:168-180 does NOT store `files_affected` from Finding objects into the registry dict. This means `get_active_highs()` returns dicts without `files_affected`, causing `finding.get("files_affected", [])` to always return `[]`. Remediation cannot route findings to target files without this data.

**New task added below.**

---

### Task 15: Store `files_affected` in DeviationRegistry finding dicts
- **Type**: fix
- **Target file(s)**: `src/superclaude/cli/roadmap/convergence.py` (lines 168-180)
- **Description**:
  1. In `DeviationRegistry.merge_findings()`, the dict created for new findings at line 168 does not include `files_affected`.
  2. The `Finding` dataclass at `models.py:40` has `files_affected: list[str]`.
  3. Add `files_affected` to the stored dict:
     ```python
     self.findings[stable_id] = {
         "stable_id": stable_id,
         "dimension": f.dimension,
         "severity": f.severity,
         "description": f.description,
         "location": f.location,
         "source_layer": source,
         "status": "ACTIVE",
         "first_seen_run": run_number,
         "last_seen_run": run_number,
         "debate_verdict": None,
         "debate_transcript": None,
         "files_affected": list(f.files_affected) if hasattr(f, 'files_affected') else [],
     }
     ```
  4. Also update existing findings when re-seen (line 165-166) to refresh `files_affected`:
     ```python
     self.findings[stable_id]["last_seen_run"] = run_number
     self.findings[stable_id]["status"] = "ACTIVE"
     if hasattr(f, 'files_affected'):
         self.findings[stable_id]["files_affected"] = list(f.files_affected)
     ```
- **Source recommendation**: Discovered during reflection (not in original gap analysis)
- **Depends on**: none
- **Acceptance criteria**:
  - Registry JSON includes `files_affected` for each finding.
  - `get_active_highs()` returns dicts with populated `files_affected` lists.
  - Remediation can route findings to target files.
- **Risk**: Low. Adding a field to the dict is backward-compatible. Existing registries will have findings without `files_affected`; the T03 `dict.get("files_affected", [])` fallback handles this gracefully.
- **Wave**: 1
