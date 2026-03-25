# Workflow: Gate-System Remediation (4 Phases)

## Purpose
Create a step-by-step execution guide for a **new agent with no prior context** to remediate outstanding gate-system issues:
1. Unwired roadmap steps: `deviation-analysis`, `remediate`, `certify`
2. Cleanup-audit import inconsistency (absolute vs relative import)

This workflow is planning-first and execution-ready. It includes explicit checkpoints, measurable go/no-go criteria, rollback playbook steps, and a required reflection task after each phase.

---

## Scope and Success Criteria

### In scope
- Roadmap pipeline step wiring and ordering
- Gate contract alignment with produced artifacts
- Resume/state coherence for new steps
- Incremental gate enforcement rollout
- Cleanup import consistency update
- Validation via targeted tests + real CLI pipeline evals

### Out of scope
- Unrelated refactors
- New dynamic registry architecture for all gates
- Broad pipeline redesign

### Final success criteria
- `_build_steps()` includes operational steps for deviation/remediation/certification flow
- Resume logic correctly handles newly wired steps and stale artifacts
- Gate pass/fail behavior is deterministic and documented
- `cleanup_audit/gates.py` import style is consistent with project standard
- All planned tests pass and **real CLI pipeline eval thresholds** are met

---

## Prerequisites (Do Before Phase 1)

1. Confirm working branch is **not** `master`.
2. Confirm Python command policy: use `uv run ...` only.
3. Read and cache context for these files:
   - `src/superclaude/cli/roadmap/executor.py`
   - `src/superclaude/cli/roadmap/gates.py`
   - `src/superclaude/cli/roadmap/prompts.py`
   - `src/superclaude/cli/roadmap/certify_prompts.py`
   - `src/superclaude/cli/roadmap/remediate.py`
   - `src/superclaude/cli/roadmap/remediate_executor.py`
   - `src/superclaude/cli/roadmap/models.py`
   - `src/superclaude/cli/cleanup_audit/gates.py`
4. Lock command source-of-truth before running evals:
   - Primary: `CLAUDE.md` (repo root command policy)
   - Secondary fallback: `Makefile` targets in repo root
   - Rule: if commands disagree, follow repo-root `CLAUDE.md`
5. Create a session checklist tracking each task ID below.

---

## Phase 1 — Contract Lock (No Behavior Change)

### Goal
Freeze artifact contracts and gate expectations before wiring runtime behavior.

### Files to edit (Phase 1)
- `claudedocs/workflow_gate-system-remediation-4phases.md` (this file, contract matrix sections)
- Optional supporting notes file in `claudedocs/` (if needed for matrix tables)

### Tasks

#### P1-T1: Build gate contract matrix
**Primary ownership files:**
- `src/superclaude/cli/roadmap/gates.py`

Actions:
- Extract required frontmatter fields, `min_lines`, semantic checks for:
  - `DEVIATION_ANALYSIS_GATE`
  - `REMEDIATE_GATE`
  - `CERTIFY_GATE`
- Build matrix: `gate -> required field -> producer -> verification path`.

#### P1-T2: Map producers for each required field
**Primary ownership files:**
- `src/superclaude/cli/roadmap/remediate.py`
- `src/superclaude/cli/roadmap/certify_prompts.py`
- `src/superclaude/cli/roadmap/executor.py`

Actions:
- Identify current producer function for every required field.
- Mark missing producers and name exact function(s) to update in later phases.

#### P1-T3: Lock canonical artifact names/paths
**Primary ownership files:**
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/gates.py`

Actions:
- Lock canonical names:
  - `spec-deviations.md` (deviation output, if used)
  - `remediation-tasklist.md`
  - `certification-report.md`
- Document any existing divergence (e.g., `certify.md` vs `certification-report.md`).
- Convert canonical naming to a **hard Phase 1 acceptance rule**:
  - Any runtime reference to non-canonical name is a Phase 1 failure.
  - Explicitly inventory and resolve all `certify.md` references before Phase 2 starts.

#### P1-T4: Define entry/exit invariants per post-fidelity step
**Primary ownership files:**
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/pipeline/gates.py`

Actions:
- Entry invariant: upstream artifacts exist and pass expected gates.
- Exit invariant: output artifact has parseable frontmatter and required content structure.

#### P1-T5: Create objective contract verification checklist
**Primary ownership files:**
- `claudedocs/workflow_gate-system-remediation-4phases.md`

Actions:
- Add checklist rows with pass/fail assertions for each gate contract.

### Phase 1 checkpoint
- Contract matrix complete.
- Each strict gate field has known producer or explicit implementation target.

### Go/No-Go (Phase 1 → Phase 2)
- **GO** if all 3 gate contracts are fully mapped and artifact names are canonicalized with zero non-canonical runtime references.
- **NO-GO** if any gate has unknown producer ownership or any `certify.md` reference remains in runtime paths.

### Required reflection task (after Phase 1)
- Run:
  - `/sc:reflect --type completion`

---

## Phase 2 — Safe Wiring (Observability-First)

### Goal
Wire new steps into runtime with low blast radius and strong observability.

### Files to edit (Phase 2)
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/prompts.py` (or dedicated prompt module if applicable)
- `src/superclaude/cli/roadmap/certify_prompts.py` (if prompt contract changes)
- `tests/roadmap/` relevant step-order and wiring tests

### Tasks

#### P2-T1a: Add step-runner dispatch branches (PREREQUISITE)
**Complexity:** 4 | **Adversarial-reviewed**
**Primary ownership file:** `src/superclaude/cli/roadmap/executor.py` (`roadmap_run_step`)

Mechanical steps:
1. In `roadmap_run_step()`, add `if step.id == "deviation-analysis":` dispatch branch (same pattern as `anti-instinct` at line ~403). This branch calls `_run_deviation_analysis(step, config, started_at)` and returns a `StepResult` directly, never reaching `ClaudeProcess`.
2. Add `if step.id == "remediate":` dispatch branch. This branch calls `_run_remediate_step(step, config, started_at)` and returns a `StepResult` directly.
3. Both handler functions are stubs initially (write gate-compliant output with placeholder data) — full implementation in P2-T3.

Verification: `uv run pytest tests/roadmap/test_executor.py -v`
**Must complete before P2-T1.**

#### P2-T1: Add runtime step wiring in `_build_steps()`
**Complexity:** 5 | **Adversarial-reviewed, REFACTORED**
**Primary ownership file:** `src/superclaude/cli/roadmap/executor.py` (`_build_steps`)

Mechanical steps:
1. Add imports: `DEVIATION_ANALYSIS_GATE`, `REMEDIATE_GATE` to the `.gates` import block (line 27-39). `CERTIFY_GATE` already imported.
2. Add output path variables after `spec_fidelity_file` (line 796):
   - `deviation_file = out / "spec-deviations.md"`
   - `remediation_file = out / "remediation-tasklist.md"`
   - `certification_file = out / "certification-report.md"`
3. Insert after wiring-verification Step (line 927), before `return steps`:
   - Step 10 `deviation-analysis`: `prompt=""`, `gate=DEVIATION_ANALYSIS_GATE`, `timeout_seconds=300`, `inputs=[spec_fidelity_file, merge_file]`, `retry_limit=0`, `gate_mode=GateMode.TRAILING`
   - Step 11 `remediate`: `prompt=""`, `gate=REMEDIATE_GATE`, `timeout_seconds=600`, `inputs=[deviation_file, spec_fidelity_file, merge_file]`, `retry_limit=0`, `gate_mode=GateMode.TRAILING`
   - Step 12 `certify`: **Do NOT add statically.** Certify is constructed dynamically after remediate completes using `build_certify_step(config, findings=actual_findings)`. Add a placeholder comment: `# Step 12 (certify) constructed dynamically by roadmap_run_step after remediate`
4. Fix `certify.md` reference at line 1037: change to `certification-report.md`.

Verification: `uv run pytest tests/roadmap/test_eval_gate_ordering.py tests/roadmap/test_executor.py -v`

#### P2-T2: Align ordered step IDs
**Complexity:** 2
**Primary ownership file:** `src/superclaude/cli/roadmap/executor.py` (`_get_all_step_ids`)

Mechanical steps:
1. Add `"deviation-analysis"` between `"wiring-verification"` and `"remediate"` (line 1007).
2. Result: `..., "wiring-verification", "deviation-analysis", "remediate", "certify"`.
3. Verify: assert length of `_get_all_step_ids(config)` equals flattened `_build_steps(config)` length + 1 (certify is dynamic, counted in IDs but not in static step list).

#### P2-T3: Wire executable producers with JSON sidecar strategy
**Complexity:** 5 | **Adversarial-reviewed, REFACTORED**
**Primary ownership files:**
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/remediate.py`
- `src/superclaude/cli/roadmap/certify_prompts.py`

**P2-T3-sub0: JSON sidecar design decision (locked)**
- When writing `spec-deviations.md`, also write `spec-deviations.json` (full findings as list of dicts).
- When writing `remediation-tasklist.md`, also write `remediation-tasklist.json` (Finding dicts).
- Rationale: eliminates fragile markdown-to-Finding parsing. Pattern exists: `DeviationRegistry` already serializes to `deviation-registry.json`.

**P2-T3a: deviation-analysis producer**
- Create `_write_deviation_analysis_output(registry: DeviationRegistry, output_file: Path)` in `executor.py`.
- Aggregates from `registry.findings` by `deviation_class`: count `SLIP` -> `slip_count`, `INTENTIONAL` -> `intentional_count`, `PRE_APPROVED` -> `pre_approved_count`, `AMBIGUOUS` -> `ambiguous_count`.
- Builds `routing_fix_roadmap` = comma-separated stable_ids where class=SLIP.
- Builds `routing_no_action` = comma-separated stable_ids where class=PRE_APPROVED.
- Computes `total_analyzed = sum of all class counts`.
- Validates cross-field consistency BEFORE writing (fail-fast).
- Writes `.md` (gate-compliant YAML frontmatter) AND `.json` (machine-readable sidecar).
- Wire into `_run_deviation_analysis()` dispatch branch from P2-T1a.

**P2-T3b: remediate producer**
- `_run_remediate_step()` reads `spec-deviations.json` (not markdown), converts to `Finding` objects.
- Calls `generate_remediation_tasklist(findings, source_report_path, source_report_content)`.
- Writes result to `step.output_file` (`.md`) AND `remediation-tasklist.json` sidecar.

**P2-T3c: certify producer (dynamic construction)**
- After remediate step completes, `roadmap_run_step()` reads `remediation-tasklist.json` to populate `Finding` objects.
- Calls `build_certify_step(config, findings=actual_findings, context_sections=...)`.
- Executes the certify Step via standard LLM pipeline path (prompt is non-empty with real findings).

Verification: `uv run pytest tests/roadmap -k "producer or deviation or remediate or certify" -v`

#### P2-T4: Lock observability-first control path
**Complexity:** 2 | **Decision locked:** `GateMode.TRAILING`
**Primary ownership file:** `src/superclaude/cli/roadmap/executor.py`

Mechanical steps:
- Already specified in P2-T1: all new steps use `gate_mode=GateMode.TRAILING`.
- Mechanism: `TrailingGateRunner` evaluates asynchronously; failures logged but non-blocking.
- Add assertion in P2-T5 tests confirming TRAILING mode for new steps.

#### P2-T5: Add targeted wiring tests
**Complexity:** 3
**Primary ownership files:**
- `tests/roadmap/test_executor.py`
- `tests/roadmap/test_eval_gate_ordering.py`

Mechanical steps:
1. `test_eval_gate_ordering.py::TestStepOrdering::test_step_count`: Change `assert len(flat) == 11` to `assert len(flat) == 13` (certify is dynamic, not in static step list).
2. `test_sequential_order_after_generate`: Add `"deviation-analysis", "remediate"` to `expected_order` after `"wiring-verification"`.
3. Add `test_deviation_analysis_after_wiring`, `test_remediate_after_deviation_analysis` ordering assertions.
4. Add `TestInputDependencies` tests: deviation-analysis inputs fidelity+merge; remediate inputs deviation+fidelity+merge.
5. Add `test_new_steps_trailing_gate_mode` asserting TRAILING for deviation-analysis and remediate.
6. `test_executor.py::test_step_ids_in_order`: Add `assert ids[11] == "deviation-analysis"`, `assert ids[12] == "remediate"`.
7. `test_executor.py::test_build_steps_returns_correct_count`: Update count to 12 entries (13 steps including parallel pair).

Verification: `uv run pytest tests/roadmap/test_eval_gate_ordering.py tests/roadmap/test_executor.py -v`

#### P2-T6: Run targeted tests (explicit commands)
Run:
```bash
uv run pytest tests/roadmap -k "step or wiring or resume" -v
uv run pytest tests/roadmap -k "gate" -v
```

Flake policy (applies to all phases):
- Do not loop-retry blindly.
- On first flaky-looking failure: rerun once to classify.
- If still failing: treat as real failure, capture logs, open blocker, and do not advance phase.

### Phase 2 checkpoint
- Runtime includes all three new steps in intended order.
- Targeted wiring tests pass.

### Go/No-Go (Phase 2 → Phase 3)
- **GO** if targeted wiring tests pass and artifact naming is canonical in runtime.
- **NO-GO** if new steps are present but unreachable or produce non-gate-compliant output.

### Required reflection task (after Phase 2)
- Run:
  - `/sc:reflect --type completion`

---

## Phase 3 — Resume/State Hardening + Incremental Enforcement

### Goal
Make resume deterministic and enforce gates progressively without destabilizing pipeline runs.

### Files to edit (Phase 3)
- `src/superclaude/cli/roadmap/executor.py` (resume checks, stale detection, state transitions)
- `src/superclaude/cli/roadmap/gates.py` (if gate semantic expectations need alignment)
- `src/superclaude/cli/roadmap/models.py` (state schema fields if required)
- `tests/roadmap/` (resume and failure-path tests)

### Tasks

#### P3-T1: Audit resume logic by function ownership
**Primary ownership sections (`executor.py`):**
- `_apply_resume`
- `_step_needs_rerun`
- `check_remediate_resume`
- `check_certify_resume`
- `_check_tasklist_hash_current`
- `_check_annotate_deviations_freshness`

**Complexity:** 4 | **Adversarial-reviewed, REFACTORED**

Mechanical steps:
1. Verify `_apply_resume()` (line 2166) iterates generic step list — confirm no step-ID hardcoding (except `"extract"`). **Expected: no changes needed.**
2. Verify `_step_needs_rerun()` (line 2115) is gate-mode-agnostic — checks `step.gate` regardless of `gate_mode`. **Expected: no changes needed.**
3. **Triage dead code (P3-T1a):** `check_remediate_resume()` (line 2019) and `check_certify_resume()` (line 2053) are defined and tested but NEVER called from production code. Decision required:
   - **Option A (recommended):** Wire `check_remediate_resume()` into the remediate step's resume check inside `_apply_resume()` for hash-freshness validation that the generic path doesn't provide. Wire `check_certify_resume()` similarly.
   - **Option B:** Delete both functions and their tests as dead code.
   - Document chosen option before proceeding.
4. Verify `_check_annotate_deviations_freshness()` (line 1084) references `spec-deviations.md` — matches canonical name. **Expected: no changes needed.**

Verification: Read each function body and confirm step ID references match canonical names. Document audit results.

#### P3-T2: Fix stale-artifact invalidation rules
**Complexity:** 4 | **Adversarial-reviewed, ACCEPTED with caveat**
**Primary ownership section:** `executor.py` freshness/hash checks

Mechanical steps:
1. Verify `dirty_outputs` propagation in `_apply_resume()` (line 2206): if spec-fidelity reruns, its output enters `dirty_outputs`. Deviation-analysis has `spec_fidelity_file` as input -> triggers rerun. Cascade continues to remediate and certify.
2. **No code changes needed.** The generic mechanism handles all steps.
3. **Caveat (document):** This chain only works AFTER P2-T1 wires the steps. Before P2-T1, deviation-analysis/remediate/certify don't exist in the pipeline and dirty_outputs doesn't reach them. This assessment applies to the post-P2-T1 state.

Verification: Confirmed by P3-T4 scenario tests.

#### P3-T3: Align `.roadmap-state.json` metadata writing/reading
**Complexity:** 3
**Primary ownership sections:** state write/read functions in `executor.py`

Mechanical steps:
1. `_save_state()` (line 1273): writes `steps` dict keyed by `r.step.id`. New steps produce `StepResult` with correct IDs. **No change needed.**
2. `build_remediate_metadata()` (line 1452) and `build_certify_metadata()` (line 1481): already exist with correct field names. **No change needed.**
3. State schema documentation (add to appendix):
   - `steps["deviation-analysis"]`: `{status, attempt, output_file, started_at, completed_at}`
   - `steps["remediate"]`: same structure
   - `steps["certify"]`: same structure
   - Top-level `"remediate"`: metadata from `build_remediate_metadata()`
   - Top-level `"certify"`: metadata from `build_certify_metadata()`
   - No top-level `"deviation-analysis"` key (uses generic `steps` path only)

Verification: P3-T4 test inspects state file after mock pipeline run.

#### P3-T4: Add resume scenario tests
**Complexity:** 3
**Primary ownership file:** `tests/roadmap/test_resume_restore.py` (existing test patterns)

Mechanical steps — add 4 new test functions:
1. **Scenario 2: Fail at deviation-analysis, resume.** Create state file with steps 1-9 PASS, deviation-analysis FAIL. Mock gate_fn returns False for deviation-analysis. Call `_step_needs_rerun()`. Assert: deviation-analysis needs rerun, prior steps skipped.
2. **Scenario 3: Fail at remediate, resume.** Same pattern, deviation-analysis PASS, remediate FAIL.
3. **Scenario 4: Fail at certify, resume.** Same pattern, remediate PASS, certify FAIL.
4. **Scenario 5: Stale spec-fidelity cascades.** Mark `spec_fidelity_file` in `dirty_outputs`. Assert all 3 new steps are marked for rerun via input dependency.

Follow existing pattern in `test_resume_restore.py`: use `_step_needs_rerun()` directly with mock `gate_fn`.

Verification: `uv run pytest tests/roadmap/test_resume_restore.py -v`

#### P3-T5-pre1: Analyze TRAILING-mode failure logs (MANDATORY PREREQUISITE)
**Complexity:** 2 | **Adversarial-reviewed, NEW TASK**

Mechanical steps:
1. After P3-T6 eval runs complete, collect gate evaluation log output for deviation-analysis, remediate, certify gates.
2. Document per-gate: failure rate, most common failure reason, whether `ambiguous_count > 0` occurred.
3. **Gate for proceeding to enforcement:** If any gate fails in >20% of observed runs, document root cause and resolution path BEFORE enforcing.

No code changes. Analysis only.

#### P3-T5: Enforce gates incrementally
**Complexity:** 5 | **Adversarial-reviewed, REFACTORED**
**Primary ownership file:** `src/superclaude/cli/roadmap/executor.py`

**Prerequisites:** P3-T4 (resume tests pass) AND P3-T5-pre1 (failure log analysis complete with <20% failure rate).

**Stage A: Enforce deviation-analysis gate**
- In `_build_steps()`, remove `gate_mode=GateMode.TRAILING` from deviation-analysis Step (defaults to `GateMode.BLOCKING`).
- Update test `test_new_steps_trailing_gate_mode` to expect BLOCKING for deviation-analysis.
- Verification: `uv run pytest tests/roadmap -k "deviation" -v`
- **Do NOT proceed to Stage B until Stage A tests pass.**

**Stage B: Enforce remediate gate**
- Same pattern: remove `gate_mode=GateMode.TRAILING` from remediate Step.
- Update test expectations.
- Verification: `uv run pytest tests/roadmap -k "remediate or remediation" -v`

**Stage C: Enforce certify gate**
- Same pattern for certify (dynamic step, so enforcement is in `build_certify_step()` — confirm it already uses `GateMode.BLOCKING` by default, which it does since `gate_mode` defaults to `BLOCKING`).
- Verification: `uv run pytest tests/roadmap -k "certify or certification" -v`

Each stage is an independent commit point.

#### P3-T6: Run tests + real evals (explicit commands)
Run targeted resume/enforcement tests:
```bash
uv run pytest tests/roadmap -k "resume or remediation or certify or deviation" -v
```
Run broader roadmap tests:
```bash
uv run pytest tests/roadmap -v
```

Pre-eval CLI verification (mandatory before first eval run):
```bash
uv run superclaude roadmap run --help
```
- Confirm `--output` (or equivalent current flag) from actual help output.
- If help output differs from this workflow, update this workflow first, then proceed.

Run at least two real CLI evals:
```bash
uv run superclaude roadmap run <SPEC_PATH_1> --output <OUT_DIR_1>
uv run superclaude roadmap run <SPEC_PATH_2> --output <OUT_DIR_2>
```

> CLI command source-of-truth:
> 1. Repo-root `CLAUDE.md` command guidance (authoritative)
> 2. `Makefile` targets as executable fallback
> 3. Actual `--help` output at execution time
> 4. If still ambiguous, pause and resolve command source before running evals
>
> Always keep UV wrapper for Python commands.

### Acceptance thresholds for real evals (mandatory)
To pass Phase 3, all must hold:
1. **2/2 real eval runs succeed** (no terminal halt)
2. Each run emits artifacts:
   - `roadmap.md`
   - `spec-fidelity.md`
   - `remediation-tasklist.md`
   - `certification-report.md`
3. Gate outputs show deterministic pass/fail reasons when failing.
4. Resume from an induced failure succeeds in at least 1 run.

### Phase 3 checkpoint
- Resume behavior deterministic across failure points.
- Incremental enforcement stages promoted with evidence.

### Go/No-Go (Phase 3 → Phase 4)
- **GO** if all acceptance thresholds above are met.
- **NO-GO** if any threshold fails.

### Required reflection task (after Phase 3)
- Run:
  - `/sc:reflect --type completion`

---

## Phase 4 — Import Consistency + Final Validation + Rollout Readiness

### Goal
Resolve import inconsistency and complete final validation package with rollback readiness.

### Files to edit (Phase 4)
- `src/superclaude/cli/cleanup_audit/gates.py`
- `tests/cleanup_audit/` or lint checks covering import style
- `docs/generated/gate-system-deep-analysis.md` (status update)
- `claudedocs/workflow_gate-system-remediation-4phases.md` (if final notes needed)

### Tasks

#### P4-T1: Normalize cleanup-audit import style
**Primary ownership file:**
- `src/superclaude/cli/cleanup_audit/gates.py`

Actions:
- Convert absolute import to project-consistent relative import.

#### P4-T2: Add regression guard for import-style drift
**Primary ownership files:**
- Relevant test/lint config + test file

Actions:
- Add a lightweight check that gate modules follow agreed import style.

#### P4-T3: Run targeted + broader tests (explicit commands)
First, discover valid cleanup-audit test targets (path-safe fallback required):
```bash
uv run pytest tests/roadmap -v
```
Then use one of the following based on what exists in repo:
- If cleanup-audit test directory exists:
```bash
uv run pytest tests/cleanup_audit -v
```
- Else fallback to keyword selection across existing tests:
```bash
uv run pytest tests -k "cleanup_audit or cleanup-audit" -v
```
Finally run broader suite:
```bash
uv run pytest -v
```

#### P4-T4: Final real pipeline validation (explicit commands)
Pre-run command check (mandatory):
```bash
uv run superclaude roadmap run --help
```
Then run:
```bash
uv run superclaude roadmap run <SPEC_PATH_3> --output <OUT_DIR_3>
```
Validate artifacts in output dir:
- `roadmap.md`
- `spec-fidelity.md`
- `remediation-tasklist.md`
- `certification-report.md`
- `.roadmap-state.json`

#### P4-T5: Update status docs and operator notes
**Primary ownership files:**
- `docs/generated/gate-system-deep-analysis.md`

Actions:
- Mark findings remediated/partial with evidence paths.
- Include residual caveats if any.

#### P4-T6: Execute rollback playbook dry-run checklist
**Primary ownership files:**
- `claudedocs/workflow_gate-system-remediation-4phases.md`
- Git branch state

Actions:
1. Identify last known-good commit SHA before wiring work.
2. Verify branch-only rollback path (no destructive commands unless explicitly approved).
3. Confirm reversible unit:
   - Step wiring changes
   - Resume/state changes
   - Import normalization
4. Run rollback simulation on paper:
   - Which files revert first
   - Which tests rerun to confirm restored state
5. Document exact rollback verification tests with path fallback:
```bash
uv run pytest tests/roadmap -k "step or wiring or resume" -v
```
If `tests/cleanup_audit` exists:
```bash
uv run pytest tests/cleanup_audit -v
```
Else:
```bash
uv run pytest tests -k "cleanup_audit or cleanup-audit" -v
```

#### P4-T7: Prepare final go/no-go handoff summary
Include:
- What changed
- What passed
- Residual risks
- Rollback readiness status
- Clear recommendation: GO or NO-GO

### Phase 4 checkpoint
- Import inconsistency resolved.
- Full validation and rollback readiness documented.

### Go/No-Go (release recommendation)
**GO requires all:**
1. All roadmap + cleanup_audit targeted tests pass.
2. Full test suite passes (or approved known failures documented).
3. Final real pipeline validation run passes with required artifacts.
4. Rollback checklist completed and verified.

If any fail: **NO-GO** and open follow-up remediation tasks.

### Required reflection task (after Phase 4)
- Run:
  - `/sc:reflect --type completion`

---

## Execution Order and Dependencies

1. Phase 1 must complete before runtime wiring.
2. Phase 2 wiring must complete before resume/state hardening.
3. Phase 3 enforcement must stabilize before final rollout checks.
4. Reflection task is mandatory after each phase and acts as gate.

---

## Agent Handoff Template (Use Between Sessions)

When handing to a new agent, include:
- Current phase + last completed task ID
- Reflection output from latest `/sc:reflect --type completion`
- Open blockers
- Exact failed tests and logs
- Next immediate task ID
- Current go/no-go status

---

## Appendix A — Exact Commands to Run (UV-only)

### Targeted roadmap wiring tests
```bash
uv run pytest tests/roadmap -k "step or wiring" -v
```

### Targeted resume/enforcement tests
```bash
uv run pytest tests/roadmap -k "resume or remediation or certify or deviation" -v
```

### Roadmap test suite
```bash
uv run pytest tests/roadmap -v
```

### Cleanup-audit tests (path-aware)
If directory exists:
```bash
uv run pytest tests/cleanup_audit -v
```
Else fallback:
```bash
uv run pytest tests -k "cleanup_audit or cleanup-audit" -v
```

### Full suite
```bash
uv run pytest -v
```

### Real CLI eval runs (replace placeholders)
First verify current CLI signature:
```bash
uv run superclaude roadmap run --help
```
Then execute:
```bash
uv run superclaude roadmap run <SPEC_PATH_1> --output <OUT_DIR_1>
uv run superclaude roadmap run <SPEC_PATH_2> --output <OUT_DIR_2>
uv run superclaude roadmap run <SPEC_PATH_3> --output <OUT_DIR_3>
```

---

## Minimal Deliverables Checklist

- [ ] Contract matrix completed (Phase 1)
- [ ] Step-runner dispatch branches added (Phase 2, P2-T1a)
- [ ] Runtime steps wired and ordered (Phase 2)
- [ ] JSON sidecar producers implemented (Phase 2, P2-T3)
- [ ] Resume/state hardened + staged enforcement complete (Phase 3)
- [ ] TRAILING-mode failure logs analyzed (Phase 3, P3-T5-pre1)
- [ ] Import consistency fixed + final validations complete (Phase 4)
- [ ] Real eval thresholds met (Phase 3 and Phase 4)
- [ ] Rollback playbook completed
- [ ] Four reflection runs completed (one per phase)
- [ ] Final go/no-go summary prepared

---

## Appendix B — Decision Record (Phase 0 Adversarial Review)

| Task | Complexity | Adversarial Verdict | Final Decision | Key Reasoning |
|------|-----------|-------------------|----------------|---------------|
| P2-T1 | 5 | **REFACTOR** | Add dispatch branches first; dynamic certify; expanded remediate inputs; 300s timeout | Empty-prompt steps would invoke Claude CLI with no instruction. Certify needs actual findings, not empty list. |
| P2-T3 | 5 | **REFACTOR** | JSON sidecar strategy for inter-step data; no fragile markdown parsing | `generate_remediation_tasklist()` needs structured Finding objects; markdown round-trip is brittle. Registry aggregation is ~40 lines, not a thin adapter. |
| P3-T1 | 4 | **REFACTOR** | Audit confirmed generic resume works; dead code triage added for `check_remediate_resume`/`check_certify_resume` | Both functions exist and are tested but never called from production. Must wire or remove. |
| P3-T2 | 4 | **ACCEPT** (caveat) | No code changes; dirty_outputs propagation is generic and correct | Chain only valid after P2-T1 wires the steps. Assessment reframed to post-wiring state. |
| P3-T5 | 5 | **REFACTOR** | Added mandatory P3-T5-pre1 (analyze failure logs before enforcement) | No observability data before TRAILING->BLOCKING promotion risks routine halts from structural gate failures. |

Full adversarial debate transcripts: `claudedocs/workflow_gate-remediation-phase0-decisions.md` § Phase 0.5
