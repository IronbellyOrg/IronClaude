# ISS-010: Remediation ownership conflict — Proposals

## Issue Summary

The v3.05 spec describes remediation as happening **within** the convergence loop (FR-7 says up to 3 runs: catch -> verify -> backup, with remediation between runs to fix findings). The current codebase implements remediation as a **post-pipeline** step (step 10 of 10 in `_build_steps()`, after spec-fidelity and wiring-verification). The functions `_check_remediation_budget()` and `_print_terminal_halt()` in `executor.py` assume remediation is external to the fidelity gate — they track attempts via `.roadmap-state.json` and print manual-fix instructions, not loop-back instructions.

**Affected spec sections**: FR-7 (convergence gate, lines 335-367), FR-9 (remediation, lines 411-467)
**Compatibility Report source**: Section 7b

## CRITICAL Dependency Check

**ISS-001** (convergence.py CREATE->MODIFY): YES, must be applied first or concurrently. ISS-001 establishes that convergence.py is an existing module being extended, not created. ISS-010 adds `execute_fidelity_with_convergence()` to convergence.py — the function that would contain the convergence loop with embedded remediation. If ISS-001 is not resolved, the spec still implies creating convergence.py from scratch, which would make the remediation-inside-loop design ambiguous about where the loop even lives.

**ISS-003** (remediate_executor.py CREATE->MODIFY): YES, must be applied first or concurrently. ISS-003 establishes that remediate_executor.py exists (563 lines). ISS-010 proposes that `execute_remediation()` be called from within the convergence loop — this requires understanding what already exists in remediate_executor.py. If ISS-003 is not resolved, implementers might try to create a new remediation module and wire it into the convergence loop, duplicating existing code.

**Both CRITICAL resolutions are prerequisites.** ISS-001's recommended Proposal #1/#2 adds baseline/delta framing to FR-7 and identifies `execute_fidelity_with_convergence()` as new code. ISS-003's recommended Proposal #1 adds baseline/delta framing to FR-9. ISS-010 builds on both by specifying how the convergence loop orchestrator calls remediation between runs.

## Codebase Ground Truth

### Pipeline step ordering (`executor.py:396-620`)

The pipeline is a 10-step linear sequence:
```
1. extract -> 2a. generate-A / 2b. generate-B (parallel) -> 3. diff ->
4. debate -> 5. score -> 6. merge -> 7. test-strategy -> 8. spec-fidelity ->
9. wiring-verification -> 10. remediate -> (11. certify, conditional)
```

Remediate is step 10, **after** spec-fidelity (step 8) and wiring-verification (step 9). It runs once, post-pipeline, not inside any loop.

### Remediation budget checking (`executor.py:786-830`)

`_check_remediation_budget()` reads `remediation_attempts` from `.roadmap-state.json` and compares against `max_attempts=2`. When budget is exhausted, it calls `_print_terminal_halt()` which outputs manual-fix instructions to stderr. This design assumes:
- Remediation is an external step, not loop-internal
- Budget tracking is via persistent state file, not in-memory loop counter
- Terminal halt means "user must fix manually and `--resume`", not "loop to next convergence run"

### Convergence loop (`convergence.py`)

`convergence.py` has the infrastructure (DeviationRegistry, ConvergenceResult, `_check_regression()`, temp dirs) but **no orchestrator function exists**. There is no `execute_fidelity_with_convergence()` — this is identified in ISS-001 and Compatibility Report Section 4 as new code to build. The convergence loop that would call remediation between runs does not exist yet.

### Remediation execution (`remediate_executor.py:476-563`)

`execute_remediation()` is a standalone function that takes `findings_by_file`, runs parallel ClaudeProcess agents, and returns `("PASS"/"FAIL", findings)`. It has no awareness of convergence loops, run numbers, or registry state. It operates on raw findings, not registry entries.

### Key tension points

1. `_check_remediation_budget()` uses `max_attempts=2`, but FR-7 says max 3 convergence runs — these are different budgets with different semantics
2. `_print_terminal_halt()` tells users to fix manually and `--resume`; convergence mode should instead halt with a diagnostic report (FR-7 AC: "halt, write diagnostic report, exit non-zero")
3. `execute_remediation()` has no hook for registry updates — after remediation, findings need to be marked FIXED/FAILED in the DeviationRegistry, but the current function only updates Finding.status on the in-memory objects

## Proposal A: Convergence Loop Wraps Existing Remediation (Integration Approach)

### Approach

Keep `execute_remediation()` in remediate_executor.py unchanged. The new `execute_fidelity_with_convergence()` function in convergence.py calls it between convergence runs. Add spec text to FR-7 that explicitly describes the intra-loop remediation call. Deprecate (but don't remove) `_check_remediation_budget()` and `_print_terminal_halt()` for convergence mode — they remain active in legacy mode only.

The convergence loop owns the budget (3 runs max). Remediation is called between runs as a "fix attempt" step. The loop structure becomes:
```
Run 1: scan -> merge findings -> registry
  -> if 0 HIGHs: PASS
  -> else: remediate (call execute_remediation) -> Run 2
Run 2: scan -> merge findings -> registry
  -> if 0 HIGHs: PASS
  -> regression? -> FR-8 parallel validation
  -> else: remediate -> Run 3
Run 3: scan -> merge findings -> registry
  -> PASS or HALT (no more remediation)
```

### Before (Current Spec Text)

FR-7 Description (lines 337-343):
```
**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED) — includes both structural AND semantic HIGHs
- **Monotonic progress**: Each run must have ≤ **structural** HIGHs than previous run. Semantic HIGH fluctuations are logged as warnings but do NOT constitute regression.
- **Hard budget**: Maximum 3 runs (catch → verify → backup)
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, trigger parallel validation (see FR-8)
```

FR-7 Acceptance Criteria (lines 354-366) — excerpt:
```
- [ ] If budget exhausted without convergence: halt, write diagnostic report, exit non-zero
```

### After (Proposed Spec Text)

FR-7 Description:
```
**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED) — includes both structural AND semantic HIGHs
- **Monotonic progress**: Each run must have ≤ **structural** HIGHs than previous run. Semantic HIGH fluctuations are logged as warnings but do NOT constitute regression.
- **Hard budget**: Maximum 3 runs (catch → verify → backup)
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, trigger parallel validation (see FR-8)
- **Intra-loop remediation**: Between convergence runs, the loop invokes `execute_remediation()` (from `remediate_executor.py`) on active HIGH findings. Remediation occurs WITHIN the convergence loop, not as a separate post-pipeline step. The convergence loop is the sole budget authority (3 runs); the legacy `_check_remediation_budget()` in `executor.py` is NOT used in convergence mode.
```

FR-7 Acceptance Criteria — add:
```
- [ ] Between runs, `execute_fidelity_with_convergence()` calls `execute_remediation()` on active HIGH findings from the registry
- [ ] Remediation results are reflected in the DeviationRegistry (FIXED/FAILED) before the next scan run
- [ ] In convergence mode, `_check_remediation_budget()` and `_print_terminal_halt()` are NOT invoked; the convergence loop manages its own budget
- [ ] In legacy mode (convergence_enabled=false), `_check_remediation_budget()` and `_print_terminal_halt()` operate exactly as pre-v3.05
- [ ] If budget exhausted without convergence: halt, write diagnostic report to `{output_dir}/convergence-halt-report.md`, exit non-zero (replaces `_print_terminal_halt()` behavior in convergence mode)
```

FR-9 — add to description (after ISS-003 baseline/delta framing is applied):
```
**Convergence integration**: In convergence mode, `execute_remediation()` is
called by the convergence loop (`execute_fidelity_with_convergence()` in
convergence.py) between fidelity runs. The function's interface remains
unchanged — it takes findings, runs agents, returns (status, findings). The
convergence loop is responsible for translating remediation results back into
DeviationRegistry status updates (FIXED/FAILED).
```

### Trade-offs

**Pros**:
- Minimal code change to remediate_executor.py — it stays a pure execution engine
- Clean separation: convergence.py owns the loop + budget, remediate_executor.py owns execution
- Legacy mode is completely unaffected — `_check_remediation_budget()` / `_print_terminal_halt()` remain for non-convergence pipelines
- Natural alignment with ISS-001 (convergence.py as the orchestrator) and ISS-003 (remediate_executor.py as the engine)

**Cons**:
- Requires convergence.py to bridge between DeviationRegistry entries and the Finding-based interface that `execute_remediation()` expects — a translation layer
- The convergence loop becomes a complex orchestrator (scan + remediate + check regression + budget management)
- Two different halt mechanisms coexist (legacy `_print_terminal_halt()` vs convergence `convergence-halt-report.md`)

---

## Proposal B: Remediation-Aware Convergence with Registry Callback (Callback Approach)

### Approach

Modify `execute_remediation()` in remediate_executor.py to accept an optional `registry_callback` parameter. When provided (convergence mode), remediation updates the DeviationRegistry directly after each file is processed. The convergence loop still owns the budget, but remediation is self-reporting rather than requiring the loop to translate results.

This tightens the interface: remediation knows about the registry in convergence mode but remains backward-compatible when no callback is provided (legacy mode).

### Before (Current Spec Text)

FR-9 Acceptance Criteria (lines 435-445):
```
**Acceptance Criteria**:
- [ ] Remediation agents output MorphLLM-compatible lazy edit snippets per finding
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] MorphLLM (when available) applies patches via semantic merging
- [ ] Fallback applicator (when MorphLLM unavailable): deterministic Python text replacement using original_code as anchor (minimum anchor: 5 lines or 200 chars)
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file (not all-or-nothing)
- [ ] Existing snapshot/restore mechanism retained for per-file rollback
```

### After (Proposed Spec Text)

FR-9 Acceptance Criteria:
```
**Acceptance Criteria**:
- [ ] Remediation agents output MorphLLM-compatible lazy edit snippets per finding
- [ ] Each patch includes: target_file, finding_id, original_code, instruction, update_snippet, rationale
- [ ] MorphLLM (when available) applies patches via semantic merging
- [ ] Fallback applicator (when MorphLLM unavailable): deterministic Python text replacement using original_code as anchor (minimum anchor: 5 lines or 200 chars)
- [ ] Per-patch diff-size guard: reject individual patch if `changed_lines / total_file_lines > threshold` (default 30%)
- [ ] Rejected patches logged with reason; finding status set to FAILED in registry
- [ ] Valid patches for the same file are applied sequentially (not batched)
- [ ] Full regeneration only with explicit user consent (`--allow-regeneration` flag)
- [ ] Rollback is per-file (not all-or-nothing)
- [ ] Existing snapshot/restore mechanism retained for per-file rollback
- [ ] `execute_remediation()` accepts optional `registry: DeviationRegistry` parameter
- [ ] When `registry` is provided: after each finding is remediated (FIXED or FAILED), `registry.update_finding_status()` is called immediately
- [ ] When `registry` is None: behavior is identical to pre-v3.05 (legacy mode)
```

FR-7 Description — add:
```
- **Intra-loop remediation**: Between convergence runs, the loop calls `execute_remediation()` with the active DeviationRegistry. Remediation updates the registry directly via callback, eliminating the need for post-hoc result translation. The convergence budget (3 runs) supersedes the legacy `_check_remediation_budget()` which is NOT used in convergence mode.
```

FR-7 Acceptance Criteria — add:
```
- [ ] `execute_fidelity_with_convergence()` passes the DeviationRegistry to `execute_remediation()` between runs
- [ ] In convergence mode, `_check_remediation_budget()` and `_print_terminal_halt()` are NOT invoked
- [ ] In legacy mode, both functions operate unchanged
```

### Trade-offs

**Pros**:
- Tighter coupling eliminates the translation layer between convergence and remediation
- Registry is always in sync after remediation — no risk of stale registry state
- Backward-compatible: `registry=None` preserves legacy behavior exactly
- Smaller orchestrator in convergence.py — less logic to coordinate

**Cons**:
- Introduces a dependency from remediate_executor.py to convergence.py (importing DeviationRegistry)
- Modifies `execute_remediation()` signature — any existing callers must be updated or given `registry=None` default
- Mixes concerns: remediate_executor.py now knows about the registry lifecycle, not just execution
- More code changes in remediate_executor.py than Proposal A

---

## Proposal C: Replace Post-Pipeline Remediation with Convergence-Only Mode (Full Redesign)

### Approach

The most radical option: in convergence mode, there is no separate "remediate" pipeline step at all. Step 10 (remediate) is skipped. All remediation happens inside `execute_fidelity_with_convergence()` as part of step 8 (spec-fidelity). The spec explicitly states that convergence mode subsumes the remediation step, and the step ordering table is updated.

`_check_remediation_budget()` and `_print_terminal_halt()` are scoped as legacy-only in the spec. The convergence halt report replaces terminal halt entirely in convergence mode.

### Before (Current Spec Text)

Appendix A "Proposed (to-be)" (lines 587-599):
```
Spec + Roadmap → Parser extracts structured data per section
  → 5 Structural Checkers (parallel) → Typed findings (source_layer="structural")
  → Residual Semantic Layer (chunked, budget-enforced ≤30KB) → Semantic findings (source_layer="semantic")
    → If any semantic HIGH: lightweight debate (prosecutor/defender + deterministic judge) → verdict
  → All findings → Deviation Registry (append/update, split structural/semantic counts)
  → Convergence Gate reads registry (sole authority in convergence mode)
    → Pass: 0 active HIGHs (structural + semantic)
    → Structural regression detected: 3 parallel agents in temp dirs → merge → debate
    → Semantic fluctuation: log warning, continue (not regression)
    → Fail + budget remaining: structured patch remediation (diff-size guarded, --allow-regeneration opt-in)
    → Fail + budget exhausted: halt with diagnostic report
```

FR-7 Description (lines 337-343) — same as Proposal A "Before"

### After (Proposed Spec Text)

Appendix A "Proposed (to-be)":
```
Spec + Roadmap → Parser extracts structured data per section
  → 5 Structural Checkers (parallel) → Typed findings (source_layer="structural")
  → Residual Semantic Layer (chunked, budget-enforced ≤30KB) → Semantic findings (source_layer="semantic")
    → If any semantic HIGH: lightweight debate (prosecutor/defender + deterministic judge) → verdict
  → All findings → Deviation Registry (append/update, split structural/semantic counts)
  → Convergence Gate reads registry (sole authority in convergence mode)
    → Pass: 0 active HIGHs (structural + semantic) → proceed to step 9 (wiring-verification)
    → Structural regression detected: 3 parallel agents in temp dirs → merge → debate
    → Semantic fluctuation: log warning, continue (not regression)
    → Fail + budget remaining: remediate within loop (call execute_remediation() on active HIGHs,
      update registry, re-scan) — step 10 (remediate) is NOT executed separately
    → Fail + budget exhausted: halt with diagnostic report (convergence-halt-report.md), exit non-zero

Legacy mode (convergence_enabled=false):
  Step 8 (spec-fidelity) → Step 9 (wiring-verification) → Step 10 (remediate, post-pipeline)
  → _check_remediation_budget() + _print_terminal_halt() operate as pre-v3.05
```

FR-7 Description:
```
**Description**: The fidelity gate evaluates convergence based on registry
state with these criteria:
- **Pass**: Zero HIGH findings in registry (all FIXED or SKIPPED) — includes both structural AND semantic HIGHs
- **Monotonic progress**: Each run must have ≤ **structural** HIGHs than previous run. Semantic HIGH fluctuations are logged as warnings but do NOT constitute regression.
- **Hard budget**: Maximum 3 runs (catch → verify → backup)
- **Regression detection**: If run N+1 has MORE **structural** HIGHs than run N, trigger parallel validation (see FR-8)

**Remediation ownership**: In convergence mode, remediation is INTERNAL to
the convergence loop (step 8). The separate post-pipeline remediate step
(step 10) is SKIPPED. The convergence loop calls `execute_remediation()`
between scan runs and updates the DeviationRegistry with results. This
resolves the ownership conflict: convergence owns the full
scan→remediate→rescan cycle, using remediate_executor.py as an execution
engine.

In legacy mode (`convergence_enabled=false`), step 10 (remediate) runs as a
separate post-pipeline step with `_check_remediation_budget()` enforcing its
own 2-attempt budget. `_print_terminal_halt()` provides terminal halt output.
These functions are NOT used in convergence mode.
```

FR-7 Acceptance Criteria — add:
```
- [ ] In convergence mode, pipeline step 10 (remediate) is skipped — `_build_steps()` excludes it or `roadmap_run_step()` short-circuits it
- [ ] `execute_fidelity_with_convergence()` calls `execute_remediation()` between convergence runs on active HIGH findings
- [ ] After each remediation call, registry is updated (FIXED/FAILED) before the next scan run
- [ ] In convergence mode, `_check_remediation_budget()` and `_print_terminal_halt()` are NOT invoked
- [ ] In legacy mode, step 10 runs with full pre-v3.05 behavior including `_check_remediation_budget()` and `_print_terminal_halt()`
- [ ] Convergence halt report written to `{output_dir}/convergence-halt-report.md` (not stderr terminal halt)
```

FR-9 — add to description:
```
**Pipeline integration**: In convergence mode, `execute_remediation()` is
invoked by the convergence loop (FR-7) between fidelity scan runs. The
separate pipeline step 10 (remediate) is NOT executed. In legacy mode,
remediation runs as step 10 post-pipeline, unchanged from pre-v3.05.
```

### Trade-offs

**Pros**:
- Cleanest separation of concerns: convergence mode has one authority (the convergence loop), legacy mode has another (the linear pipeline)
- No dual-budget confusion — convergence mode has 3 runs, legacy mode has 2 remediation attempts, and they never overlap
- Eliminates the ambiguity entirely — the spec explicitly says step 10 is skipped in convergence mode
- Most complete resolution — addresses both the spec text and the architectural diagram

**Cons**:
- Largest spec edit surface — modifies FR-7, FR-9, Appendix A, and potentially the step list
- Requires code changes in `_build_steps()` or `roadmap_run_step()` to conditionally skip step 10
- Certify step (step 11) currently depends on `remediation-tasklist.md` as input — if remediation moves inside convergence, the tasklist output path may need adjustment
- Risk of breaking `--resume` logic which tracks step completion state in `.roadmap-state.json`

---

## Recommended Proposal

**Proposal A (Integration Approach)** is recommended, with elements of Proposal C's Appendix A diagram update.

**Rationale**:

1. **Minimal code disruption**: remediate_executor.py stays unchanged. The new `execute_fidelity_with_convergence()` function (already identified as needed by ISS-001) is the natural place to wire remediation into the loop.

2. **Clean dependency chain**: ISS-001 adds the baseline/delta framing to FR-7 and identifies `execute_fidelity_with_convergence()` as new code. ISS-003 adds the baseline framing to FR-9. Proposal A layers on top of both by specifying the interface between them — it does not contradict or duplicate either resolution.

3. **Legacy mode is completely untouched**: `_check_remediation_budget()` and `_print_terminal_halt()` remain exactly as they are for non-convergence pipelines. No risk of breaking existing behavior.

4. **Avoids Proposal B's coupling problem**: remediate_executor.py should not import from convergence.py. The remediation engine should be registry-agnostic — the convergence loop does the translation.

5. **Takes Proposal C's key insight without the blast radius**: The step 10 skip (Proposal C) is powerful but risky for `--resume` and certify. Proposal A achieves the same effect by having the convergence loop call remediation internally, while step 10 can still exist as a no-op or skip in convergence mode. The Appendix A diagram clarification from Proposal C should be adopted regardless.

**Prerequisite**: Apply ISS-001 and ISS-003 CRITICAL resolutions before or concurrently with this change. Specifically, ISS-001's recommended approach (Proposals #1+#2+#3 combined) establishes the baseline framing and identifies `execute_fidelity_with_convergence()` as new code, which is the function that implements the intra-loop remediation call specified here.
