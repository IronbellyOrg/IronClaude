# Brainstorm 05 -- Link 3: Tasklist-to-Code Fidelity Gate

**Date**: 2026-03-17
**Context**: Forensic report at `docs/generated/cli-portify-executor-noop-forensic-report.md` established that Link 3 (Tasklist -> Code fidelity) does not exist. The pipeline's transitive trust chain is Spec -> Roadmap -> Tasklist -> Code, but the final link has no gate. No programmatic gate verifies that code output satisfies tasklist acceptance criteria.
**Scope**: 10 solutions total -- 5 for gate design, 5 for integration with unified-audit-gating v1.2.1

---

## Section A: Link 3 -- Tasklist-to-Code Fidelity Gate Design

### A1. Acceptance Criteria Extraction Gate

**Summary**: Parse acceptance criteria from tasklist files into a machine-readable checklist and verify each criterion against code artifacts after task completion.

**How it works**:
The gate operates in two phases. At sprint start (preflight), the gate parser extracts acceptance criteria from each task in the tasklist phase files. Criteria are classified as _deterministic_ (file exists, function defined, import present, test passes) or _semantic_ (behavior description requiring LLM evaluation). During task completion, the gate evaluates deterministic criteria via AST parsing, file glob, grep, and test execution. Semantic criteria are evaluated by an LLM prompt that receives the task's acceptance criteria text plus the git diff of changed files, producing a YAML frontmatter report with `criteria_met_count`, `criteria_total`, and `criteria_failures[]`. The gate passes only when `criteria_met_count == criteria_total`.

**What it would catch**:
- The cli-portify no-op bug: acceptance criteria like "Sequential pipeline runs end-to-end" would fail because no step implementation was ever invoked -- the LLM or deterministic check would detect that `run_portify()` never passes `step_runner` to the executor.
- Tasks marked complete when their deliverables are stubs or placeholders.
- Partial implementations where some acceptance criteria pass but others are silently skipped.

**Integration point**:
- New module: `src/superclaude/cli/sprint/gates.py` (or extend `src/superclaude/cli/pipeline/gates.py`).
- Hook location: `sprint/executor.py` post-subprocess, pre-task-status-classification. After the Claude subprocess returns for a task, the gate runs before the task is marked PASS.
- Gate definition follows the `GateCriteria` + `SemanticCheck` pattern from `pipeline/models.py`.

**Limitations**:
- Semantic criteria still depend on LLM judgment, inheriting the same weakness as SPEC_FIDELITY_GATE (LLM can misclassify).
- Acceptance criteria in tasklists are natural language -- parsing them into deterministic checks requires either strict formatting conventions or tolerating ambiguity.
- Runtime cost: running tests or AST analysis after every task adds latency to the sprint loop.
- Does not help if the tasklist itself is already corrupted (Link 2 failure propagating through).

---

### A2. Wiring Verification Gate (Static Import-Chain Analysis)

**Summary**: Statically verify that all registry entries, dispatch tables, and injectable dependencies declared in tasklist deliverables have corresponding import chains and call sites in the produced code.

**How it works**:
After code is generated for a task, the gate performs static analysis on the output files:
1. Parse all `REGISTRY`, `DISPATCH`, `RUNNERS`, or similar dictionary constants from Python modules. For each key, verify that the mapped value (function reference, class, or import path) is importable from the declared module.
2. Parse all `__init__(self, ..., callback: Optional[Callable] = None)` constructor signatures. Flag any `Optional[Callable]` parameter that defaults to `None` and is never explicitly provided in any call site within the codebase.
3. Parse all files in `steps/` or similar directories. Verify each exported function is imported by at least one consumer module.
4. Detect no-op fallbacks: code paths where a `None`-defaulting callable returns a success stub (`0`, `True`, `"SUCCESS"`).

The gate emits a YAML report with `unwired_count`, `noop_fallback_count`, and `orphan_module_count`. It passes only when all three are zero.

**What it would catch**:
- The cli-portify no-op bug directly: `_execute_step()` defaults to no-op when `step_runner is None`, and `run_portify()` never provides `step_runner`. Both patterns would be flagged.
- The DEVIATION_ANALYSIS_GATE "defined but not wired" pattern (Delta 2.2).
- The SprintGatePolicy stub (Delta 2.6).
- Any future "Track A / Track B never joined" integration failures.

**Integration point**:
- New module: `src/superclaude/cli/audit/wiring_gate.py`.
- Can run as a semantic check function registered on a `GateCriteria` instance (STRICT tier), following the pattern in `roadmap/gates.py`.
- Hook: post-task-completion in the sprint runner, or as a standalone audit invocable via `/sc:audit-gate`.

**Limitations**:
- Static analysis cannot detect all wiring failures -- dynamic dispatch, monkey-patching, or runtime registration would evade it.
- Python's dynamic nature means import-chain analysis produces false positives (e.g., intentional lazy imports, plugin architectures).
- Requires maintained heuristics for recognizing "registry" and "dispatch" patterns -- brittle if naming conventions change.
- Scoped to Python only; does not cover shell scripts, configuration files, or cross-language boundaries.

---

### A3. Smoke Test Gate (Minimal Execution Verification)

**Summary**: After code is produced for a task, run the actual CLI command or function against a minimal test fixture and verify that real work occurs (non-trivial output, non-zero execution time, actual artifacts produced).

**How it works**:
The gate defines a `SmokeTestSpec` per task or per milestone that specifies:
- A CLI command or Python function to invoke.
- A minimal input fixture (test config, sample files).
- Expected output assertions: at least N files produced, at least M lines of content, execution time > T seconds (to catch instant no-op returns), specific strings or patterns present in output.

The sprint runner executes the smoke test in a sandboxed temporary directory after the task's Claude subprocess completes. The gate passes only if all assertions hold. The smoke test spec can be embedded in the tasklist acceptance criteria using a fenced code block convention (e.g., ` ```smoke-test ... ``` `).

**What it would catch**:
- The cli-portify no-op bug: `run_portify()` completes in milliseconds and produces only `return-contract.yaml` with no real content. A smoke test asserting "at least 3 output files" or "execution time > 5 seconds" would fail.
- Silent success bugs where exit code is 0 but no meaningful work was performed.
- Missing artifact generation (pipeline claims success but output directory is empty or trivial).

**Integration point**:
- New module: `src/superclaude/cli/sprint/smoke_gate.py`.
- Hook: post-task or post-milestone in the sprint runner. Could also serve as a release-tier gate.
- Smoke test specs live in tasklist phase files or in a companion `smoke-tests/` directory within the release bundle.

**Limitations**:
- Requires authoring smoke test specs for each task -- adds burden to tasklist generation (or requires the LLM to generate them, introducing its own fidelity risk).
- Sandboxed execution may not reproduce the full environment (missing dependencies, different paths).
- Time-based assertions are fragile across different hardware.
- Cannot catch semantic correctness -- only detects "nothing happened" or "too little happened," not "the wrong thing happened."

---

### A4. Deliverable-ID Cross-Reference Gate (Deterministic Traceability)

**Summary**: Parse all deliverable IDs (D-NNNN), requirement IDs (R-NNN, FR-NNN), and task IDs (T-NN.NN) from the tasklist, then verify each has a corresponding artifact, code symbol, or test in the produced code output.

**How it works**:
1. At sprint preflight, extract all deliverable IDs from the tasklist index and phase files using regex (`D-\d{4}`, `R-\d{3}`, `FR-\d{3}`, `T\d{2}\.\d{2}`).
2. Build a mapping: each ID maps to its acceptance criteria and expected output file pattern.
3. After each task completes, verify:
   - The expected output file exists and is non-empty.
   - The output file contains a back-reference to the task/deliverable ID (traceability marker).
   - If the deliverable specifies a code module, verify the module is importable.
   - If the deliverable specifies a test, verify the test file exists and passes.
4. At milestone boundary, verify all IDs scoped to that milestone have been resolved.
5. Gate emits YAML frontmatter: `deliverables_expected`, `deliverables_resolved`, `deliverables_missing[]`.

**What it would catch**:
- Tasks completed without producing their declared deliverables.
- Deliverables that exist as files but contain no real content (empty stubs).
- Missing traceability -- code produced without any reference to the requirement it implements.
- Scope creep detection: code artifacts produced that map to no declared deliverable.

**Integration point**:
- New module: `src/superclaude/cli/sprint/traceability_gate.py`.
- Reuses the `_parse_frontmatter()` utility from `roadmap/gates.py`.
- Hook: post-task for individual deliverable checks, post-milestone for aggregate coverage checks.
- Extends the existing `TASKLIST_FIDELITY_GATE` pattern in `tasklist/gates.py`.

**Limitations**:
- Requires tasklist files to use consistent ID formatting -- any deviation in naming conventions causes false negatives.
- Traceability markers in code (comments referencing D-NNNN) are a convention that must be enforced by prompt engineering in the sprint prompts, not by the gate itself.
- Does not verify semantic correctness of the deliverable content -- only that it exists and is non-trivial.
- Would NOT have caught the cli-portify bug if the tasklist itself never assigned a deliverable ID to "wire executor to step dispatch" (which it did not).

---

### A5. Differential Behavior Gate (Before/After Execution Comparison)

**Summary**: Capture a behavioral snapshot of the codebase before and after a task's code changes, then verify that the delta matches expected behavioral changes declared in the tasklist.

**How it works**:
1. Before the task's Claude subprocess runs, capture a baseline: run the project's test suite (or a specified subset), record pass/fail counts, collect import graphs for modified modules, and snapshot public API signatures.
2. After the subprocess completes, capture the same measurements.
3. Compare the deltas:
   - New tests added: count must match tasklist's "Tests required" field.
   - Test pass rate: must not decrease (no regressions).
   - New public API symbols: must match tasklist's declared interfaces.
   - Import graph changes: new edges must correspond to declared integration points.
4. Gate emits: `tests_added`, `tests_regressed`, `api_symbols_added`, `api_symbols_removed`, `import_edges_added`. Passes when deltas are consistent with declared expectations.

**What it would catch**:
- The cli-portify no-op bug: the task "implement executor dispatch" would declare new import edges (`executor.py -> steps/*.py`) and new tests. The differential gate would detect zero import edges added and zero tests added.
- Regressions introduced during implementation (test pass rate drops).
- Missing integration wiring: the import graph delta shows no new connections between modules that were supposed to be connected.
- "Cosmetic-only" changes that modify comments or formatting but add no behavioral difference when the task requires functional changes.

**Integration point**:
- New module: `src/superclaude/cli/sprint/diff_gate.py`.
- Hook: wraps the task execution in the sprint runner -- snapshot before, execute, snapshot after, compare.
- Requires access to the project's test runner (integrates with the existing `uv run pytest` convention).
- Baseline/delta data stored in `.sprint-state.json` alongside existing sprint state.

**Limitations**:
- Significant runtime overhead: running the test suite twice per task (before and after).
- Requires the project to have a functioning test suite -- cannot operate on projects with no tests.
- Import graph analysis is Python-specific and would need language-specific adapters for other languages.
- Behavioral equivalence is undecidable in general -- the gate catches structural changes, not semantic correctness.
- The "expected delta" must be declared in the tasklist, adding authoring burden.

---

## Section B: Link 3 -- Integration with Unified Audit Gating v1.2.1

### B1. Task-Scope Audit Gate as Link 3 Carrier

**Summary**: Implement Link 3 as the task-scope audit gate (Tier 1) defined in the unified-audit-gating v1.2.1 spec, making code fidelity verification a first-class check within the audit gate's deterministic evaluator.

**How it works**:
The v1.2.1 spec already defines a task-scope gate that blocks `audit_task_passed -> completed` transition unless the gate passes. This solution adds code-fidelity checks to the task gate's check catalog (`gate-check-catalog.yaml`):
- `CHECK_CODE_ACCEPTANCE_CRITERIA`: verify acceptance criteria from tasklist are satisfied in code output.
- `CHECK_CODE_WIRING`: verify no unwired dispatch tables, no-op fallbacks, or orphan modules.
- `CHECK_CODE_SMOKE`: run a minimal smoke test if a smoke spec is declared.

These checks are registered as deterministic checks (not LLM-dependent) with severity `critical` -- any failure blocks the task completion transition per the spec's state machine (`audit_task_running -> audit_task_failed`). The `GateResult` schema (spec section 6.1) captures evidence for each check, including file paths and line numbers.

The audit gate evaluator in `sc-audit-gate-protocol/SKILL.md` gains a new section: "Code Fidelity Checks" that defines the check functions, severity classification, and evidence format.

**What it would catch**:
All failure modes from Section A solutions A1-A5, but scoped per-task and integrated into the audit workflow state machine. The task cannot transition to `completed` without passing code fidelity.

**Integration point**:
- `src/superclaude/cli/sprint/models.py` -- `AuditWorkflowState` enum (new, per spec section 4.1).
- `src/superclaude/cli/sprint/executor.py:668-717` -- post-subprocess hook where `SprintGatePolicy` triggers the audit gate evaluation.
- `src/superclaude/skills/sc-audit-gate-protocol/SKILL.md` -- check catalog definition.
- `gate-check-catalog.yaml` -- new code-fidelity check entries.

**Limitations**:
- Depends on the full v1.2.1 implementation (state machine, GateResult model, SprintGatePolicy wiring) -- cannot ship incrementally without those prerequisites.
- The v1.2.1 spec has 3 open NO-GO blockers (D1.2 profile thresholds, D1.3 rollback triggers, D1.4 owner/deadline assignments) that must be resolved before any implementation proceeds.
- Task-scope gate runs at high frequency; code-fidelity checks (especially smoke tests) add latency to every task.

---

### B2. Trailing Gate Pattern for Non-Blocking Code Fidelity

**Summary**: Use the existing `TrailingGateRunner` infrastructure from `pipeline/trailing_gate.py` to run code fidelity checks asynchronously after task completion, blocking only at milestone boundaries.

**How it works**:
The v1.2.1 delta analysis (section 3.2) identifies the trailing gate pattern as a natural fit for task-scope gates. This solution:
1. After each task's Claude subprocess completes, the sprint runner submits code-fidelity checks to `TrailingGateRunner` as a deferred evaluation.
2. The task transitions to a new state: `audit_task_deferred` (added to the state machine between `audit_task_running` and `audit_task_passed`).
3. The trailing gate evaluates asynchronously while the next task begins execution.
4. At milestone boundary, `resolve_gate_mode()` (which already returns BLOCKING for release scope) blocks until all deferred task gates have resolved.
5. Any failed deferred gate triggers `DeferredRemediationLog` entry and the sprint halts at the milestone boundary with a remediation prompt.

The `SprintGatePolicy` stub at `sprint/executor.py:47-90` is completed to implement this flow, consuming `resolve_gate_mode()` for scope-aware blocking decisions.

**What it would catch**:
Same failure modes as B1, but with deferred detection -- failures surface at milestone boundaries rather than immediately after each task. This means a task's code fidelity failure is caught before the milestone is marked complete, but other tasks in the same milestone may execute against a known-bad foundation.

**Integration point**:
- `src/superclaude/cli/pipeline/trailing_gate.py` -- already provides `TrailingGateRunner`, `DeferredRemediationLog`, `attempt_remediation()`.
- `src/superclaude/cli/sprint/executor.py:47-90` -- `SprintGatePolicy` completion.
- `src/superclaude/cli/sprint/executor.py:736-787` -- post-classification, pre-halt decision point for milestone boundary checks.
- State machine extension: add `audit_task_deferred` as a legal intermediate state.

**Limitations**:
- Deferred evaluation means downstream tasks may build on code that later fails the fidelity gate -- wasted work.
- Adds a new state (`audit_task_deferred`) not in the v1.2.1 spec's state machine -- requires a spec amendment.
- The trailing gate infrastructure is itself unwired (Delta 2.6) -- this solution requires completing that wiring first.
- Complexity: the interaction between deferred gates, milestone boundaries, and the remediation retry loop creates state machine complexity that increases the risk of stuck states.

---

### B3. Phase 0 Prerequisite: Deviation Analysis as Code Fidelity Precursor

**Summary**: Wire the already-defined `DEVIATION_ANALYSIS_GATE` into roadmap execution (resolving Delta 2.2) and extend its deviation model to cover code-level deviations, creating a foundation that the audit gate can consume for Link 3 checks.

**How it works**:
The v1.2.1 delta analysis identifies `DEVIATION_ANALYSIS_GATE` wiring as a Phase 0 prerequisite. This solution extends that work:
1. Add `deviation-analysis` step to `_build_steps()` in `roadmap/executor.py:343-440`, positioned after `spec-fidelity` (as already recommended in Delta 2.2).
2. Extend the deviation model to include a new deviation class: `code_deviation` alongside the existing `slip`, `intentional`, `pre_approved`, `ambiguous` classifications.
3. At sprint time, after code is produced, generate a `code-deviations.md` report that compares tasklist acceptance criteria against code artifacts, using the same deviation classification taxonomy.
4. The audit gate's task-scope check consumes `code-deviations.md` and applies the same routing rules: `routing_fix_code` (must remediate), `routing_update_tasklist` (acceptance criteria were wrong), `routing_no_action` (deviation is acceptable), `routing_human_review`.
5. The gate passes only when `code_ambiguous_count == 0` and `code_slip_count == 0`, mirroring `DEVIATION_ANALYSIS_GATE`'s `_no_ambiguous_deviations` semantic check.

**What it would catch**:
- Spec-to-code deviations that survive the roadmap and tasklist layers (the full chain failure).
- Code that deviates from tasklist intent but in ways that might be intentional (the classification model forces explicit acknowledgment).
- The cli-portify no-op bug would be classified as a `code_slip` deviation: the tasklist said "execute each step" and the code executes nothing.

**Integration point**:
- `src/superclaude/cli/roadmap/executor.py:343-440` -- add `deviation-analysis` step (Phase 0 prerequisite).
- `src/superclaude/cli/roadmap/gates.py:712-758` -- `DEVIATION_ANALYSIS_GATE` already defined with strong semantic checks.
- New: `src/superclaude/cli/sprint/code_deviation.py` -- code-level deviation analysis module.
- Sprint prompts gain a `code-deviation-analysis` step at task completion.

**Limitations**:
- Deviation analysis at code level is inherently more complex than at document level -- code semantics are harder to compare than document content.
- Depends on completing the roadmap-level `DEVIATION_ANALYSIS_GATE` wiring first -- blocks on Phase 0.
- The deviation classification model (`slip` vs `intentional` vs `pre_approved`) requires human judgment for borderline cases -- the `ambiguous` category forces a halt, which may be overly conservative for routine code changes.
- Adding a deviation analysis step to the sprint loop significantly increases sprint execution time.

---

### B4. Rollout-Safe Shadow Mode for Code Fidelity Gates

**Summary**: Follow the v1.2.1 spec's mandatory phased rollout (shadow -> soft -> full) to introduce code fidelity gates incrementally, collecting baseline data before enforcement.

**How it works**:
The v1.2.1 spec (section 7, Delta Summary G) mandates phased rollout. This solution defines the rollout specifically for code fidelity gates:

**Shadow phase**: Code fidelity checks run after every task but results are logged only -- never block. The gate emits `GateResult` with `enforcement_mode: shadow`. Sprint runner logs the result to `.sprint-audit-shadow.json` but does not alter the task's status transition. This phase collects baseline data: how many tasks would fail, what types of failures are most common, false positive rate.

**Soft phase**: Code fidelity check failures emit warnings in the TUI (`GateDisplayState` rendering at `sprint/tui.py:174-203`) and are recorded in the `DeferredRemediationLog`, but do not block task completion. They block only at release scope (per `resolve_gate_mode()` which already returns BLOCKING for release scope). Human review of soft-phase results tunes thresholds and check definitions.

**Full phase**: Code fidelity failures block task completion per the audit state machine. `audit_task_failed` prevents `completed` transition. Override requires `OverrideRecord` with reason.

Phase transitions are controlled by a `code_fidelity_rollout_phase` field in sprint configuration, defaulting to `shadow` on initial deployment.

**What it would catch**:
In shadow/soft phases: nothing is blocked, but failure data is collected for tuning. In full phase: all failure modes from Section A solutions, with enforcement.

**Integration point**:
- `src/superclaude/cli/sprint/executor.py` -- phase-aware gate invocation.
- Sprint configuration model gains `code_fidelity_rollout_phase: shadow | soft | full`.
- `src/superclaude/cli/sprint/tui.py:174-203` -- phase table row extension for soft-mode warnings.
- `src/superclaude/cli/pipeline/trailing_gate.py` -- `resolve_gate_mode()` already has scope-aware enforcement; extend with rollout phase awareness.
- `.sprint-audit-shadow.json` -- new state file for shadow-phase data collection.

**Limitations**:
- Shadow and soft phases provide no protection -- bugs like the cli-portify no-op can ship during these phases.
- Adds configuration complexity: users must understand and manage rollout phase transitions.
- Data collection during shadow phase may be noisy if code fidelity checks are not yet well-calibrated.
- The rollout timeline delays full enforcement -- the gap between "gate exists" and "gate blocks" may span multiple releases.
- Requires the full audit state machine (v1.2.1 Phase 1) to be implemented before even shadow mode can produce `GateResult` objects.

---

### B5. Tasklist-Emitted Audit Metadata as Gate Input Contract

**Summary**: Extend the tasklist generator to emit `audit_gate_required` and `code_fidelity_checks[]` metadata per task, giving the audit gate a declarative contract for what to verify at code completion time.

**How it works**:
The v1.2.1 delta analysis (section 5, NR-1) identifies that tasklists currently emit zero audit-awareness fields. This solution addresses both NR-1 and Link 3 by extending the tasklist protocol:

1. `sc-tasklist-protocol/SKILL.md:622-637` gains new derivation rules:
   - `audit_gate_required: true` when `Tier == STRICT` or `Risk == High` or `Critical Path Override == Yes`.
   - `code_fidelity_checks[]`: an array of check specifications derived from the task's acceptance criteria and deliverable type. Each check has `type` (one of: `file_exists`, `import_chain`, `smoke_test`, `test_passes`, `symbol_defined`, `semantic_review`), `target` (file path, module name, or test pattern), and `severity` (`critical` or `major`).

2. The tasklist phase template (`phase-template.md:26-42`) gains a new section per task: `Audit Gate Contract` containing the derived `audit_gate_required` and `code_fidelity_checks[]` fields.

3. The sprint runner reads these fields at preflight and registers them with `SprintGatePolicy`. For each task where `audit_gate_required == true`, the policy schedules the declared `code_fidelity_checks[]` to run post-task.

4. The audit gate evaluator consumes the check list, runs each check, and produces a `GateResult`. The task cannot transition to `completed` unless all `critical`-severity checks pass.

**What it would catch**:
- The cli-portify no-op bug: the tasklist generator would derive `code_fidelity_checks` including `{type: "import_chain", target: "executor.py -> steps/*.py", severity: "critical"}` from the acceptance criteria. This check would fail when the import chain does not exist.
- Tasks with `Tier == STRICT` or `Risk == High` that skip audit entirely (currently possible since no audit fields exist).
- Inconsistency between what the tasklist declares and what the code delivers, because the checks are specified at tasklist generation time with full context about the task's purpose.

**Integration point**:
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:622-637` -- derivation rules for new fields.
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md:26-42` -- template extension.
- `src/superclaude/cli/sprint/executor.py:47-90` -- `SprintGatePolicy` consumes check specs from tasklist.
- `src/superclaude/cli/sprint/models.py` -- `CodeFidelityCheck` dataclass.
- `src/superclaude/cli/tasklist/gates.py` -- extend `TASKLIST_FIDELITY_GATE` to verify that tasks with `Tier == STRICT` have non-empty `code_fidelity_checks[]`.

**Limitations**:
- The quality of `code_fidelity_checks[]` depends on the LLM's ability to derive appropriate checks from acceptance criteria during tasklist generation -- this is a new LLM task with its own fidelity risk.
- Adds complexity to the already-complex tasklist protocol (SKILL.md is already 637+ lines).
- Requires tasklist schema versioning (NR-2) to prevent old bundles without audit fields from silently passing.
- Check types like `import_chain` and `symbol_defined` require language-specific analysis tools that may not exist for all target languages.
- The derivation rules are heuristic (keyword-based tier classification) -- edge cases where a task should have audit gates but does not match the keyword patterns will be missed.

---

## Cross-Reference: Solution Complementarity

The 10 solutions are not mutually exclusive. A practical implementation path would combine elements:

| Layer | Recommended Combination |
|---|---|
| Deterministic checks (cheap, fast) | A2 (wiring verification) + A4 (deliverable ID cross-refs) |
| Behavioral verification (expensive, high-signal) | A3 (smoke test) at milestone/release tier only |
| Audit integration | B1 (task-scope carrier) + B5 (tasklist-emitted metadata) |
| Rollout safety | B4 (shadow -> soft -> full) |
| Foundation | B3 (deviation analysis wiring as Phase 0) |

The critical dependency chain is: B3 (Phase 0) -> B5 (tasklist metadata) -> B1 (task gate carrier) -> B4 (rollout phases).
