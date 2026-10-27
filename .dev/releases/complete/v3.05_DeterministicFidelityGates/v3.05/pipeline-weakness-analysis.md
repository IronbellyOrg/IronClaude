# Pipeline Weakness Analysis: v3.05 Deterministic Fidelity Gates

**Date**: 2026-03-21
**Input**: v3.05 Merged Gap Analysis Report
**Scope**: Roadmap CLI pipeline infrastructure weaknesses that allowed or failed to catch B1-B10

---

## Weakness 1: Wiring Verification Targets Wrong Directory (Scans 0 Python Files)

### Description

The wiring-verification step in `executor.py:429` computes `source_dir = config.output_dir.parent`, which resolves to the **parent of the roadmap output directory** (e.g., `.dev/releases/complete/`). The `run_wiring_analysis()` function in `wiring_gate.py:688` collects files via `source_dir.rglob("*.py")`. Since roadmap output directories contain only markdown artifacts, this scan finds zero Python files. The wiring-verification gate becomes a no-op.

### Evidence

- `wiring-verification.md` from the v3.05 run shows `files_analyzed: 0`, `files_skipped: 0`, `total_findings: 0`.
- Gap analysis B9: "Wiring-verification.md scanned 0 files" and "verification step misconfigured."
- executor.py:429: `source_dir = config.output_dir.parent` -- wrong target for Python source analysis.
- wiring_gate.py:155: `source_dir.rglob("*.py")` -- correct method but pointed at wrong directory.

### Mechanism

The wiring-verification step was designed to detect unwired callables (G-001), orphan modules (G-002), and broken registries (G-003) in the **source code being modified** by the roadmap pipeline. Because it scans the output directory's parent instead of `src/superclaude/`, it never inspects the actual Python modules where B1-B3 (call signature mismatches) live. Had it scanned `executor.py` against the `convergence.py` API, the `DeviationRegistry.load_or_create()` arity mismatch (B1) and `merge_findings()` arity mismatch (B2) would have been flagged as unwired callables.

### Severity

**CRITICAL** -- This is the pipeline's primary integration verification gate, and it is entirely non-functional for its intended purpose.

### Proposed Fix

Change `source_dir` resolution to target the actual Python source tree. The wiring step should scan the `src/superclaude/cli/roadmap/` directory (derivable from the package installation path or a config field), not the markdown output directory. Add a validation guard: if `files_analyzed == 0`, the gate should WARN rather than silently PASS.

---

## Weakness 2: Convergence Mode Disables the Spec-Fidelity Gate

### Description

When `convergence_enabled=True`, the spec-fidelity step is constructed with `gate=None` (executor.py:869). This means the `execute_pipeline()` gate evaluation layer is bypassed entirely for the convergence code path. The `_run_convergence_spec_fidelity()` function returns a `StepResult` directly, and the only validation on that result is a boolean `result.passed` check (executor.py:638). There is no external gate that validates the output report's frontmatter, structure, or consistency.

### Evidence

- executor.py:869: `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE`
- Gap analysis root cause: "Executor wiring was written without end-to-end integration testing against the real DeviationRegistry API."
- The `SPEC_FIDELITY_GATE` validates frontmatter fields (`high_severity_count`, `validation_complete`, `tasklist_ready`) and structural requirements. In convergence mode, these checks are skipped.

### Mechanism

Setting `gate=None` means `execute_pipeline()` unconditionally trusts the `StepResult` returned by `_run_convergence_spec_fidelity()`. Since that function crashes at runtime (B1-B3), the pipeline would halt with an unhandled exception rather than producing a structured gate failure diagnostic. More importantly, during development, the absence of a gate meant there was no automated check that the convergence wiring produced valid output -- the developer could mark the task "complete" without the pipeline ever validating the end-to-end path.

### Severity

**CRITICAL** -- Disabling the gate for the most complex code path removes the pipeline's primary quality signal.

### Proposed Fix

Create a `CONVERGENCE_SPEC_FIDELITY_GATE` that validates convergence-mode output (frontmatter fields, structural progress log presence, budget state). Apply it even when `convergence_enabled=True`. The convergence engine's `result.passed` boolean can inform the `StepStatus`, but the gate should independently validate the written report file.

---

## Weakness 3: No Integration Smoke Test for New Wiring Code Paths

### Description

The pipeline has no mechanism to verify that newly wired code paths (like `_run_convergence_spec_fidelity()`) can execute without runtime errors. The pipeline validates **output artifacts** via gates (frontmatter fields, line counts, semantic checks) but never validates that the **code itself** can be imported, instantiated, and called with correct argument types. Unit tests in `test_convergence.py` test the convergence engine in isolation but never exercise the executor-to-engine boundary.

### Evidence

- Gap analysis finding 10: "Root cause is the same -- Executor wiring was written without end-to-end integration testing against the real DeviationRegistry API."
- B1: `DeviationRegistry.load_or_create()` called with 1 arg, requires 3 -- a call signature that could be caught by any test that imports and calls the function.
- B2: `merge_findings()` called with 2 args, requires 3 -- same class of error.
- B3: `finding.files_affected` attribute access on dict -- type mismatch catchable by any test that exercises the return value.
- Gap analysis B10: "No persistent E2E test artifacts for SC-1 through SC-6."

### Mechanism

The sprint executor runs tasks via Claude subprocess (gap analysis contributing factor 3), meaning the Python code paths may not have been invoked during sprint execution. Tasks were marked complete based on Claude's implementation within the subprocess, not runtime verification. The pipeline has no "cold start" smoke test that imports `_run_convergence_spec_fidelity` and calls it with minimal valid inputs to detect TypeError/AttributeError crashes.

### Severity

**HIGH** -- This is the root cause of all three CRITICAL bugs (B1-B3). A single integration smoke test would have caught all of them.

### Proposed Fix

Add a pipeline post-wiring validation step: after any sprint that modifies executor wiring, run `uv run python -c "from superclaude.cli.roadmap.executor import _run_convergence_spec_fidelity"` as a minimum import check. Better: add `test_convergence_wiring_e2e.py` that constructs minimal valid inputs and calls `_run_convergence_spec_fidelity()` through to the first registry call, verifying no TypeError or AttributeError is raised.

---

## Weakness 4: Budget Constants Not Validated Against Spec at Pipeline Construction Time

### Description

The pipeline constructs the TurnLedger at runtime inside `_run_convergence_spec_fidelity()` with hardcoded constant references (executor.py:571-572). There is no validation that the chosen constant (`STD_CONVERGENCE_BUDGET`) matches the spec requirement (`MAX_CONVERGENCE_BUDGET`), and no validation that constructor parameters (`minimum_allocation`, `minimum_remediation_budget`, `reimbursement_rate`) are provided. The spec's FR-7 explicitly lists all four constructor parameters, but the pipeline has no assertion or gate that checks the constructed TurnLedger's configuration.

### Evidence

- B4: `STD_CONVERGENCE_BUDGET` (46) used instead of `MAX_CONVERGENCE_BUDGET` (61). The spec-fidelity report from v3.05 shows 0 HIGH findings (the convergence path never ran due to B1-B3, so this was never tested).
- B5: Missing `minimum_allocation=CHECKER_COST`, `minimum_remediation_budget=REMEDIATION_COST`, `reimbursement_rate=0.8`. Defaults create a budget guard hole.
- The spec-fidelity step itself (when running in legacy LLM mode) would theoretically catch this deviation, but in convergence mode it IS the code being validated -- creating a self-referential gap.

### Mechanism

The spec-fidelity step is meant to validate the roadmap against the spec. But when the spec-fidelity step itself is the subject of the spec (as in v3.05, which modifies the fidelity pipeline), the pipeline cannot validate its own wiring. The budget constant choice was a judgment call made during implementation ("conservative default"), and no automated check enforced the spec's explicit requirement. The `_build_steps()` function does not validate config parameters against spec requirements.

### Severity

**HIGH** -- Budget miscalibration causes silent behavioral deviations (runs terminate early, `can_launch()` permits invalid runs) without any gate failure signal.

### Proposed Fix

Add a `validate_convergence_config()` function called at the top of `_run_convergence_spec_fidelity()` that asserts: (1) ledger initial_budget == MAX_CONVERGENCE_BUDGET, (2) minimum_allocation >= CHECKER_COST, (3) minimum_remediation_budget >= REMEDIATION_COST, (4) reimbursement_rate == 0.8. These are compile-time-checkable invariants that should fail fast with a clear error message rather than silently using wrong values.

---

## Weakness 5: Sprint Subprocess Execution Model Prevents Runtime Verification

### Description

The roadmap pipeline executes tasks via Claude subprocesses (`ClaudeProcess` in executor.py:461-471). The sprint executor follows the same pattern. This means implementation tasks are completed by an LLM writing Python code, but the LLM's output is accepted based on file existence and gate checks on the **written text**, not on whether the code can actually **execute**. The pipeline trusts that syntactically valid-looking Python code is semantically correct.

### Evidence

- Gap analysis contributing factor 3: "The sprint executor runs tasks via Claude subprocess, meaning the actual Python code paths may not have been invoked during sprint execution. Tasks were marked complete based on Claude's implementation within the subprocess, not runtime verification."
- The `roadmap_run_step()` function (executor.py:379-536) returns PASS if exit_code == 0 and the output file passes its gate. It does not import or execute the code that was written.
- B1-B3 are all runtime errors (TypeError, AttributeError) that would be caught by any execution of the code path, but the pipeline never executes newly written code.

### Mechanism

During v3.05 sprint execution, Phase 6 tasks involved writing `_run_convergence_spec_fidelity()` in executor.py. The Claude subprocess wrote the function body, the gate checked that executor.py was modified and syntactically valid, and the task was marked complete. But the function was never called with real arguments. The dict/object mismatch (B3) is particularly telling: it requires knowledge of the registry's **runtime return type** (list[dict]), which is not visible from the API signature alone. An LLM reasonably assumed `Finding` dataclass instances would be returned.

### Severity

**MEDIUM** -- This is an architectural limitation of the subprocess execution model rather than a specific pipeline bug. The fix requires adding a new pipeline capability.

### Proposed Fix

Add a "wiring validation" post-sprint step that runs `uv run pytest tests/roadmap/test_convergence_wiring.py -x` after any sprint that modifies files in `src/superclaude/cli/roadmap/`. This test file should exercise all cross-module call sites with minimal valid inputs. The sprint executor should treat test failure as a blocking gate for task completion.

---

## Adversarial Self-Debate

### Challenge 1 (Weakness 1): Is the wiring-verification misconfiguration really a pipeline weakness, or just a bug?

**Critique**: The `source_dir = config.output_dir.parent` line is a straightforward implementation bug -- it points at the wrong directory. Is this a "pipeline weakness" or just a coding error that happened to be in the pipeline?

**Response**: It is both. The coding error exists because the pipeline has no self-check that validates the wiring-verification step's output. A gate that checked `files_analyzed > 0` (or at least warned) would have surfaced this immediately. The absence of that guard is the pipeline weakness; the wrong directory is the symptom. The wiring-verification gate definition (`WIRING_GATE`) does not include a semantic check for `files_analyzed > 0`.

**Confidence**: HIGH. The evidence is concrete (0 files in the output), the mechanism is clear (wrong directory + no guard), and the fix is practical.

### Challenge 2 (Weakness 2): Is gate=None for convergence mode a design choice or a weakness?

**Critique**: Setting `gate=None` may be intentional -- the convergence engine has its own internal validation (convergence pass/fail), so an external gate might be redundant or interfere.

**Response**: The convergence engine validates its own *logic* (did HIGH counts converge?), but it does not validate the *output report format* that downstream steps consume. The gap analysis shows that `_write_convergence_report()` writes frontmatter fields, but no gate validates those fields match what downstream consumers expect. Moreover, `gate=None` means the pipeline framework's retry logic, diagnostic logging, and state management for gate failures are all bypassed. The convergence engine's boolean result is a different kind of check than a format-validating gate.

**Confidence**: HIGH. The spec explicitly defines gate criteria for spec-fidelity output. Bypassing them in the most complex mode is a genuine weakness.

### Challenge 3 (Weakness 3): Could the pipeline reasonably have caught B1-B3?

**Critique**: Expecting the pipeline to run integration tests after code generation is a significant capability addition. Current pipelines validate artifacts, not code correctness.

**Response**: Fair point -- this is asking the pipeline to do something it was never designed to do. However, the gap analysis identifies this as the root cause, and the fix (adding a test file that the sprint gate requires to pass) is practical and proportionate. The pipeline already runs `pytest` in other contexts. The weakness is not that the pipeline *should have* caught it with existing capabilities, but that the pipeline *architecture lacks the capability class* needed to catch this category of bug.

**Confidence**: MEDIUM. The weakness is real but the "pipeline weakness" framing is somewhat strained -- it is more accurately an "infrastructure gap" than a weakness in existing pipeline logic.

### Challenge 4 (Weakness 4): Is budget constant validation proportionate?

**Critique**: Adding hardcoded assertions for specific constant values is brittle. If the spec changes, the assertions break. This is the kind of thing the spec-fidelity step should catch.

**Response**: Partially valid. Hardcoding `assert initial_budget == 61` is indeed brittle. However, the core weakness is sound: the pipeline has no mechanism to validate that constructor parameters match spec requirements. A better fix might be: derive the budget constant from a config file or spec-linked constant, and assert `initial_budget == MAX_CONVERGENCE_BUDGET` (the symbolic name, not the literal value). The self-referential problem (spec-fidelity validating its own wiring) is a genuine architectural gap that the spec-fidelity step cannot solve for itself.

**Confidence**: MEDIUM. The weakness is valid but the proposed fix needs refinement to avoid brittleness.

### Challenge 5 (Weakness 5): Is the subprocess model really a pipeline weakness?

**Critique**: This is describing a fundamental architectural choice (LLM subprocesses write code, gates check artifacts) not a weakness in the pipeline. Every CI pipeline that checks linting but not integration tests has this "weakness."

**Response**: Partially valid. However, the v3.05 gap analysis explicitly calls this out as a contributing factor, and the pipeline already has the capability to run `pytest` (via `ClaudeProcess` or direct subprocess). The weakness is that the pipeline does not use its existing capabilities to validate code correctness after code-writing tasks. It is analogous to a CI pipeline that has a test runner but does not add the new module's tests to the test suite.

**Confidence**: LOW. This is more of an architectural observation than a specific pipeline weakness. It overlaps significantly with Weakness 3 and could be merged. However, Weakness 3 focuses on the *absence of tests* while Weakness 5 focuses on the *execution model* that makes tests necessary.

**Decision**: Retain Weakness 5 but downgrade confidence. It provides useful architectural context even if it is not as actionable as Weaknesses 1-4.

---

## Final Validated Set

| # | Weakness | Severity | Confidence | Bugs Explained |
|---|----------|----------|------------|----------------|
| W1 | Wiring Verification Targets Wrong Directory | CRITICAL | HIGH | B9, indirectly B1-B3 (would have caught if pointed correctly) |
| W2 | Convergence Mode Disables Spec-Fidelity Gate | CRITICAL | HIGH | B1-B5 (no gate validation on convergence output path) |
| W3 | No Integration Smoke Test for New Wiring | HIGH | MEDIUM | B1, B2, B3 (direct root cause of all three crash bugs) |
| W4 | Budget Constants Not Validated Against Spec | HIGH | MEDIUM | B4, B5 (spec deviation undetectable by pipeline) |
| W5 | Subprocess Execution Model Prevents Runtime Verification | MEDIUM | LOW | B1-B3, B10 (architectural enabler of wiring bugs) |

### Coverage of v3.05 Gap Analysis Findings

- **B1** (load_or_create arity): W1 + W2 + W3 + W5
- **B2** (merge_findings arity): W1 + W2 + W3 + W5
- **B3** (dict/object mismatch): W2 + W3 + W5
- **B4** (STD vs MAX budget): W2 + W4
- **B5** (missing constructor params): W2 + W4
- **B6** (budget_snapshot field): Not a pipeline weakness -- this is a spec implementation omission
- **B7** (progress proof format): Not a pipeline weakness -- diagnostics-only gap
- **B8** (remediation unverified): W3 (no integration test coverage)
- **B9** (wiring-verification 0 files): W1 (direct cause)
- **B10** (no E2E tests): W3 + W5 (infrastructure gap)
- **Phase 6 incomplete**: W2 + W3 (no gate to detect non-functional wiring + no test to verify it)
