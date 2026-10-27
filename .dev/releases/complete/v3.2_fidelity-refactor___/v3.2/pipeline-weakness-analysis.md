# Pipeline Weakness Analysis: v3.2 Wiring Verification Gate

**Date**: 2026-03-21
**Source**: Analysis of roadmap CLI pipeline infrastructure vs v3.2 gap analysis findings
**Method**: Pipeline-level root cause identification with adversarial self-debate

---

## Context

The v3.2 merged gap analysis found 62% implementation completeness, 4 critical bugs, and systemic naming divergences. This document identifies 5 pipeline-level weaknesses that caused or failed to catch these issues.

---

## Weakness 1: No Call-Site Wiring Verification in Pipeline Gates

### Description
The roadmap pipeline's gate system validates **output artifacts** (frontmatter fields, heading structure, minimum line counts) but never validates that **implementation call sites are wired correctly**. A function can exist, pass all output-based gates, and still be dead code because no gate checks that it is actually invoked from its intended call site.

### Evidence
- `_resolve_wiring_mode()` (executor.py:420-446) was written, exists in the codebase, and would pass any artifact-based gate -- but is never called from `run_post_task_wiring_hook()` (line 473 reads `config.wiring_gate_mode` directly).
- The wiring-verification step in the roadmap pipeline (`executor.py:424-439`) runs `run_wiring_analysis()` + `emit_report()` and checks the output via `WIRING_GATE`. It validates the **report artifact**, not whether the analysis engine is actually reachable from the sprint production path.

### Mechanism
The pipeline's gate model is: "run step -> produce file -> validate file passes criteria." This model cannot detect dead code because dead code doesn't manifest in output artifacts -- it manifests in the **absence of call edges** in the execution graph. `_resolve_wiring_mode()` produces no output file, so no gate can catch that it's unreachable. The wiring gate itself (`WIRING_GATE`) checks frontmatter fields on the wiring report, not whether the analysis was invoked from the right entry point.

### Severity
**CRITICAL**

### Proposed Fix
Add a **call-graph gate** as a deterministic post-step check in the pipeline: after the wiring-verification step runs, invoke a static analysis pass that verifies declared functions in the spec's dependency map are actually called from their specified call sites. This is analogous to the anti-instinct audit (which checks spec obligations are discharged) but targets code wiring rather than roadmap fidelity.

---

## Weakness 2: Dual Execution Model Not Tested by Pipeline

### Description
The codebase has two distinct execution paths: a phase-level production path (`execute_sprint()` in sprint/executor.py) and a task-level path (`execute_phase_tasks()`). The roadmap pipeline generates and validates a spec targeting the task-level path, but never validates that the production entry point can reach the integration hooks.

### Evidence
- Gap #1 (CRITICAL): `execute_sprint()` never creates a TurnLedger, never calls `execute_phase_tasks()`. It runs phases as monolithic Claude subprocesses, making all per-task hooks (wiring, anti-instinct) unreachable.
- The wiring-verification step in the roadmap pipeline (`executor.py:424-439`) runs wiring analysis against `config.output_dir.parent` -- the roadmap output directory, not the sprint execution codebase. It validates the roadmap artifacts' wiring, not the sprint executor's wiring.

### Mechanism
The pipeline is scoped to roadmap generation artifacts. It validates that the **roadmap** is internally consistent (spec-fidelity) and that the **roadmap's target codebase** has no orphan modules (wiring-verification). But it has no mechanism to verify that the sprint executor -- which is a separate entry point consuming the generated artifacts -- can actually reach the hooks that the spec mandates. The spec-fidelity step compares "spec vs roadmap" but never compares "spec vs production entry point."

### Severity
**CRITICAL**

### Proposed Fix
Extend the pipeline's test-strategy step (or add a new "integration-reachability" step) to emit test cases that specifically exercise the production entry point. Alternatively, add a pipeline-level pre-condition check that asserts the sprint executor's `execute_sprint()` path instantiates a TurnLedger before the wiring-verification step can PASS. This bridges the gap between "roadmap says it should work" and "production path actually wires it."

---

## Weakness 3: Spec-Fidelity Gate Checks Roadmap-vs-Spec but Not Implementation-vs-Spec

### Description
The spec-fidelity gate (`SPEC_FIDELITY_GATE` + the convergence engine) compares the **roadmap** against the **spec** for deviations. It catches cases where the roadmap diverges from the spec (e.g., DEV-001 through DEV-011 in the fidelity report). But once the roadmap is approved, no pipeline gate verifies that the **implementation** matches the spec's naming contracts, field definitions, or interface signatures.

### Evidence
- Gap #7 (MEDIUM): KPI field names diverge -- `wiring_net_cost`, `wiring_analyses_run`, `wiring_remediations_attempted` are all missing. The implementation uses different names.
- Gap #8 (MEDIUM): TurnLedger fields use `wiring_turns_used` vs spec's `wiring_gate_cost`.
- Gap #6 (HIGH): SprintConfig scope-based fields (`wiring_gate_enabled`, `wiring_gate_grace_period`) not adopted.
- RCA-4: Naming divergence cascaded from OQ decisions that were never reconciled back to spec contracts.

### Mechanism
The pipeline's fidelity loop is: spec -> extraction -> roadmap -> spec-fidelity (roadmap vs spec). The implementation phase happens **after** the pipeline completes. By the time code is written, the pipeline has already exited. There is no "implementation-fidelity" gate that compares the actual Python field names, class signatures, and interface contracts against the spec. The naming divergences accumulated during implementation with no automated check to catch them.

### Severity
**HIGH**

### Proposed Fix
Add a post-implementation verification step (could be triggered by `superclaude sprint validate` or a separate `superclaude roadmap verify-implementation`) that parses the spec's field name contracts and checks them against the actual codebase using AST inspection. The wiring gate already does AST analysis for callable detection -- extending it to verify naming contracts is a natural evolution.

---

## Weakness 4: Remediation Lifecycle Has No Integration Test in Pipeline

### Description
The pipeline's remediation path (spec-fidelity FAIL -> remediation tasklist -> remediate -> certify) tests the **remediation artifact flow** (does the tasklist exist? does it have frontmatter?). But it never tests the **remediation execution mechanics** -- whether `_format_wiring_failure()`, `_recheck_wiring()`, or `SprintGatePolicy.build_remediation_step()` are implemented and callable.

### Evidence
- Gap #4 (CRITICAL): BLOCKING path debits budget but performs no actual remediation -- `_format_wiring_failure()`, `_recheck_wiring()`, `SprintGatePolicy.build_remediation_step()` all absent.
- Gap #5 (CRITICAL): `attempt_remediation()` from trailing_gate.py not called.
- The roadmap executor's remediation path (`_check_remediation_budget()`, `_print_terminal_halt()`) handles the **pipeline's own** remediation budget for spec-fidelity failures. But the sprint executor's BLOCKING wiring mode remediation is a completely separate code path that the pipeline never exercises.

### Mechanism
The pipeline treats remediation as an artifact-generation problem: "produce a remediation-tasklist.md that passes REMEDIATE_GATE." The gate checks the tasklist's structure and completeness. But the actual remediation *execution* (spawning a subprocess to fix code, then rechecking) is sprint-level logic that the pipeline never invokes or validates. The pipeline's `build_certify_step()` certifies findings from the remediation tasklist, not from actual remediation execution. So the entire remediation lifecycle can be stubbed (debit-only) and the pipeline will never detect it.

### Severity
**HIGH**

### Proposed Fix
Add a "remediation smoke test" gate that the test-strategy step must include: at minimum, verify that the spec's remediation functions (`_format_wiring_failure`, `_recheck_wiring`, `build_remediation_step`) exist as importable callables with correct signatures. This is a weaker check than full integration testing but catches the "function doesn't exist" class of bugs deterministically.

---

## Weakness 5: Shadow Mode Treated as Logging-Only, No Evidence Chain Gate

### Description
The pipeline defines shadow mode (GateMode.TRAILING) as a deferred, non-blocking evaluation. The wiring-verification step runs in this mode and always returns PASS from `roadmap_run_step()` (executor.py:433). The trailing gate runner collects results at the end but only logs warnings on failure. There is no gate that verifies shadow mode produces **evidence artifacts** (DeferredRemediationLog entries) required for rollout promotion.

### Evidence
- Gap #3 (CRITICAL): DeferredRemediationLog not used in shadow mode. Shadow branch only logs via `_wiring_logger.info()`, does not construct `TrailingGateResult` or append to `DeferredRemediationLog`.
- RCA-5: Shadow mode was implemented as a logging-only path, missing the spec's adapter (Gamma IE-4) that feeds findings into the trailing gate pipeline.
- The pipeline executor's trailing gate sync point (`executor.py:158-170`) drains results and logs warnings but never checks whether shadow findings were persisted to `DeferredRemediationLog`.

### Mechanism
The pipeline's trailing gate infrastructure (`TrailingGateRunner`, `GateResultQueue`, `DeferredRemediationLog`) exists in `pipeline/trailing_gate.py` but the wiring-verification step in `roadmap/executor.py:424-439` bypasses it entirely -- it calls `run_wiring_analysis()` and `emit_report()` directly without constructing a `TrailingGateResult` or writing to `DeferredRemediationLog`. The pipeline executor creates a `TrailingGateRunner` when `grace_period > 0` but the roadmap executor's direct execution of the wiring step short-circuits this path. The result: shadow findings are emitted to a report file but never enter the deferred remediation pipeline.

### Severity
**CRITICAL**

### Proposed Fix
Add a gate criterion to the wiring-verification step that checks: if `rollout_mode` is shadow, then `DeferredRemediationLog` at `output_dir/deferred-remediation.jsonl` must exist and contain entries matching the wiring report's findings. This closes the evidence chain: shadow findings -> deferred log -> trailing gate -> rollout promotion decision.

---

## Adversarial Self-Debate

### Weakness 1: No Call-Site Wiring Verification

**Challenge**: Is this really a pipeline weakness, or a testing gap? The pipeline generates roadmaps, not code. Expecting it to verify call-site wiring is scope creep.

**Rebuttal**: The pipeline already includes a wiring-verification step (step 9) that runs AST analysis on the codebase. The infrastructure exists; the gap is that it checks the *roadmap output directory* for orphan modules rather than the *sprint executor* for dead code. This is a pipeline weakness because the pipeline claims to verify wiring but verifies the wrong target.

**Could the pipeline reasonably have caught this?** Yes -- the wiring gate already does AST-based call graph analysis. Extending it to verify that spec-declared functions have at least one call site is a modest extension of existing capability.

**Is the fix practical?** Medium complexity. Requires a spec-to-call-site mapping and AST traversal. The existing wiring_gate.py infrastructure (unwired callable detection) does 80% of this already.

**Confidence**: HIGH

---

### Weakness 2: Dual Execution Model

**Challenge**: The pipeline generates roadmaps. Whether `execute_sprint()` can reach hooks is a sprint-executor concern, not a roadmap-pipeline concern.

**Rebuttal**: The pipeline includes a test-strategy step that generates test cases for the implementation. If the test strategy doesn't include "verify production entry point reaches per-task hooks," that's a pipeline output quality gap. Additionally, the wiring-verification step explicitly targets integration correctness -- it should catch that the production path has no integration point.

**Could the pipeline reasonably have caught this?** Partially. The wiring gate could detect that `execute_sprint()` never calls `run_post_task_wiring_hook()` if it analyzed the sprint executor's call graph. But the current target directory is `config.output_dir.parent`, not the sprint executor codebase.

**Is the fix practical?** Yes, but requires expanding the wiring gate's target scope. The hard part is determining *which* call paths to verify -- this needs a spec-derived dependency map.

**Confidence**: MEDIUM -- this is partially a spec/architecture issue (two execution models), not purely a pipeline weakness. The pipeline couldn't fully prevent this without the sprint executor also being designed for testability.

---

### Weakness 3: Implementation-vs-Spec Not Checked

**Challenge**: The pipeline runs *before* implementation. Checking implementation fidelity is a post-implementation concern. This is blaming the hammer for not being a screwdriver.

**Rebuttal**: Fair point. However, the pipeline already has a `superclaude roadmap validate` subcommand that runs post-generation. The same infrastructure could support a `verify-implementation` step. The weakness is that the pipeline has no *lifecycle hook* for post-implementation fidelity, leaving a gap where naming divergences accumulate unchecked.

**Could the pipeline reasonably have caught this?** Not during generation, but the pipeline *does* have a validate phase. The validate phase checks roadmap internal consistency, not implementation naming. Adding implementation fidelity to validate is reasonable.

**Is the fix practical?** Yes. Field-name contract verification via AST is straightforward. The question is when to trigger it -- likely as part of `superclaude sprint validate` rather than `superclaude roadmap validate`.

**Confidence**: MEDIUM -- valid weakness but attribution to the roadmap pipeline specifically is debatable. This might belong to a sprint-validation pipeline instead.

---

### Weakness 4: Remediation Lifecycle Not Tested

**Challenge**: The pipeline generates remediation *tasklists*, not remediation *execution*. Testing that remediation functions exist is a unit test concern.

**Rebuttal**: The pipeline's test-strategy step generates test cases. If those test cases don't include "verify remediation functions are importable and have correct signatures," that's a test-strategy generation gap. The pipeline could also include a deterministic import check (like the anti-instinct audit does for obligations) that verifies spec-declared functions exist.

**Could the pipeline reasonably have caught this?** Indirectly -- through better test-strategy generation. The test-strategy step should have produced test cases that exercise the remediation path. The fact that it didn't means the test strategy was incomplete.

**Is the fix practical?** Yes. An importability check is trivial. The larger fix (verifying remediation actually works) requires integration tests, which is beyond the pipeline's scope but within the test-strategy's scope to *specify*.

**Confidence**: MEDIUM -- the pipeline's role is to specify tests, not execute them. But specifying better tests is a valid pipeline improvement.

---

### Weakness 5: Shadow Mode Evidence Chain

**Challenge**: This is an implementation bug (shadow mode doesn't write to DeferredRemediationLog), not a pipeline weakness.

**Rebuttal**: The pipeline defines the wiring-verification step's behavior. In `roadmap/executor.py:424-439`, the step directly calls `run_wiring_analysis()` + `emit_report()` and returns PASS. This is pipeline code -- the pipeline *chose* to short-circuit the trailing gate infrastructure. The implementation bug is in the pipeline itself, not in downstream code.

**Could the pipeline reasonably have caught this?** Yes -- this IS the pipeline. The roadmap executor wrote the wiring-verification step handler, and it chose to bypass DeferredRemediationLog. A self-test or structural check on the executor could verify that TRAILING-mode steps produce deferred log entries.

**Is the fix practical?** Very practical. The DeferredRemediationLog class already exists in `pipeline/trailing_gate.py`. Wiring it into the step handler is a small code change. Adding a gate check that TRAILING steps produce log entries is straightforward.

**Confidence**: HIGH -- this is clearly a pipeline weakness, not an external concern.

---

## Final Validated Set

| # | Weakness | Severity | Confidence | Retained? |
|---|----------|----------|------------|-----------|
| 1 | No Call-Site Wiring Verification in Gates | CRITICAL | HIGH | Yes |
| 2 | Dual Execution Model Not Tested | CRITICAL | MEDIUM | Yes (with caveat: partially architectural) |
| 3 | Implementation-vs-Spec Not Checked | HIGH | MEDIUM | Yes (with caveat: may belong to sprint pipeline) |
| 4 | Remediation Lifecycle Not Tested | HIGH | MEDIUM | Yes (scoped to test-strategy generation gap) |
| 5 | Shadow Mode Evidence Chain Bypassed | CRITICAL | HIGH | Yes |

### Key Observations

1. **Weaknesses 1, 2, and 5 are the strongest findings** -- they represent gaps where the pipeline *already has infrastructure* to catch the bug but fails to use it correctly. These are high-confidence pipeline weaknesses.

2. **Weaknesses 3 and 4 sit on the boundary** between pipeline responsibility and downstream validation responsibility. They are valid weaknesses in the overall development lifecycle, but attributing them specifically to the roadmap pipeline requires acknowledging that the pipeline's scope should expand to include post-implementation verification hooks.

3. **Common thread**: The pipeline validates *artifact structure* (frontmatter, heading levels, field presence) but not *behavioral correctness* (call reachability, naming contract adherence, evidence chain completeness). All 5 weaknesses stem from this artifact-centric validation model.
