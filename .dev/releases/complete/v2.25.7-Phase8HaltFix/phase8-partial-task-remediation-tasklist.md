# Tasklist — Remediation of Partially Completed Phase 8 Tasks

**Intended Executor:** `sc:task-unified --compliance strict`
**Objective:** Bring the 4 partially completed tasks to **fully complete, to spec**, based on the current Phase 8 tasklist and verified gaps.

---

## Context Summary

The following Phase 8 tasks were verified as **partial**, not fully complete to their own acceptance criteria:

1. **T04.02** — `DiagnosticBundle` config wiring / `FailureClassifier` canonical path usage
2. **T05.04** — full validation sequence did not exactly match required commands / pass conditions
3. **T06.01** — smoke evidence used simulation/tests rather than a true triggered context-exhaustion run
4. **T06.02** — isolation enforcement evidence is strong but relies heavily on simulation/tests and lacks strict practical/sub-agent-grade verification

This tasklist is narrowly scoped to complete those four tasks only.

---

# Task 1 — Complete T04.02 runtime wiring for `DiagnosticBundle` / `FailureClassifier`

**Task ID:** RT-01
**Maps to original:** `T04.02`
**Tier:** STRICT

## Goal
Finish the runtime integration so `FailureClassifier.classify()` uses `bundle.config.output_file(...)` through the **normal collection path**, not only in manually constructed test cases.

## Required context
Current implementation partially satisfies the task:

- `DiagnosticBundle` has `config: SprintConfig | None = None`
  `src/superclaude/cli/sprint/diagnostics.py:30-50`
- `FailureClassifier.classify()` uses `bundle.config.output_file(...)` if config exists
  `src/superclaude/cli/sprint/diagnostics.py:193-204`
- But `DiagnosticCollector.collect()` currently constructs `DiagnosticBundle` **without passing config**
  `src/superclaude/cli/sprint/diagnostics.py:88-92`

This leaves the normal runtime path on the deprecated fallback branch.

## Instructions
1. Read:
   - `src/superclaude/cli/sprint/diagnostics.py`
   - `tests/sprint/test_phase8_halt_fix.py`
2. Update `DiagnosticCollector.collect()` so it constructs `DiagnosticBundle(..., config=self.config)`.
3. Audit all `DiagnosticBundle(` construction sites in the repo.
4. Preserve backward compatibility where needed, but ensure the active runtime path uses config-driven resolution.
5. Add or update tests to prove:
   - normal collection path injects config
   - `FailureClassifier.classify()` uses `bundle.config.output_file(...)` in that path
   - deprecated fallback remains covered only for explicit `config=None` cases
6. Do not broaden scope beyond this task.

## Acceptance criteria
- `DiagnosticCollector.collect()` passes `config=self.config` into `DiagnosticBundle`
- Normal runtime classification no longer depends on the legacy hardcoded-path fallback
- Existing backward-compatible `config=None` behavior still works
- Tests explicitly cover both:
  - config-present runtime path
  - config-none deprecated fallback path
- Evidence doc for D-0014/D-0015 reflects full completion, not partial completion

## Required validation
- `uv run pytest tests/sprint/test_phase8_halt_fix.py -v`
- If there are diagnostics-specific tests elsewhere, run the narrowest relevant set too
- Record exact evidence showing runtime-path config wiring is now complete

---

# Task 2 — Re-run T05.04 to exact spec and produce compliant evidence

**Task ID:** RT-02
**Maps to original:** `T05.04`
**Tier:** STRICT

## Goal
Bring the validation task to full completion by executing the **exact intended validation sequence**, or by resolving blockers until the exact sequence passes.

## Required context
The prior evidence for D-0020 was only partial because it did **not** match the tasklist exactly:

- Full suite command used `--ignore=tests/cli_portify`
- Full suite had `1 failed`, not exit 0
- Ruff commands were run only on the new test file, not at the requested scope

Original required acceptance criteria:
- `uv run pytest tests/sprint/test_phase8_halt_fix.py -v` exits 0
- `uv run pytest tests/ -v --tb=short` exits 0 with zero failures
- `uv run ruff check` exits 0
- `uv run ruff format --check` exits 0

See:
- `.dev/releases/complete/v2.25.7-Phase8HaltFix/phase-5-tasklist.md:207-215`
- `.dev/releases/complete/v2.25.7-Phase8HaltFix/artifacts/D-0020/evidence.md`

## Instructions
1. Read the original T05.04 requirements in the phase tasklist.
2. Run the exact required commands, using UV only:
   - `uv run pytest tests/sprint/test_phase8_halt_fix.py -v`
   - `uv run pytest tests/ -v --tb=short`
   - `uv run ruff check`
   - `uv run ruff format --check`
3. If any command fails:
   - determine whether the failure is caused by the Phase 8 changes
   - if yes, fix only the directly relevant issue
   - if no, document why it is unrelated **but do not claim the acceptance criterion is met unless the exact command passes**
4. Update the evidence artifact so it reflects the true outcome against the exact criteria.
5. If necessary, explicitly mark any remaining blocker instead of overstating success.

## Acceptance criteria
- All 4 required commands have been run exactly as specified
- Their outputs are captured in the evidence artifact
- No ignored directories or narrowed Ruff scope unless the tasklist itself allows it
- T05.04 is only marked complete if the exact acceptance criteria are satisfied
- Evidence clearly distinguishes:
  - exact compliance
  - any residual unrelated repo-wide blockers

## Required validation
- The 4 exact commands above
- Updated D-0020 evidence with raw outputs and a truthful pass/fail conclusion

---

# Task 3 — Perform a true T06.01 context-exhaustion smoke run

**Task ID:** RT-03
**Maps to original:** `T06.01`
**Tier:** STRICT

## Goal
Replace simulation-heavy proof with a real, reproducible smoke test where a phase actually approaches or triggers context exhaustion and the operator-visible outcome is verified.

## Required context
Current D-0021 evidence is strong for routing logic, but partial relative to spec because it relies on:
- unit test
- targeted test selection
- functional output capture

The original task required:
- trigger context exhaustion on a phase approaching prompt limits
- capture operator screen output
- verify `PASS_RECOVERED`, not `ERROR`

See:
- `.dev/releases/complete/v2.25.7-Phase8HaltFix/phase-6-tasklist.md:32-47`
- `.dev/releases/complete/v2.25.7-Phase8HaltFix/artifacts/D-0021/evidence.md`

## Instructions
1. Design the smallest safe reproducible scenario that causes the sprint system to hit the intended recovery path under realistic execution.
2. Use the actual sprint execution flow, not only direct unit invocation.
3. Capture:
   - the triggering setup
   - output/error artifacts
   - operator-visible output
   - resulting phase status
4. Verify the observed visible status is `PASS_RECOVERED` routed as INFO, not ERROR.
5. Document the exact reproduction steps and cleanup steps.
6. Do not fabricate a live run from simulated logger calls.

## Acceptance criteria
- A real sprint/phase execution path was exercised
- Context exhaustion or the intended prompt-too-long recovery path was actually triggered in that execution
- Operator-visible output capture shows `PASS_RECOVERED`
- Evidence includes enough detail for another engineer to reproduce the scenario
- D-0021 is updated from simulation-heavy proof to true smoke-test proof

## Required validation
- Execute the real scenario
- Preserve or capture the actual output artifacts
- Update D-0021 with:
  - scenario setup
  - executed command(s)
  - observed operator output
  - conclusion tied directly to SC-004

---

# Task 4 — Perform strict practical verification for T06.02 isolation enforcement

**Task ID:** RT-04
**Maps to original:** `T06.02`
**Tier:** STRICT

## Goal
Upgrade T06.02 from simulation/test-backed evidence to fully strict, practical execution evidence aligned with the original task’s verification bar.

## Required context
Current D-0022 evidence strongly supports correctness, but partial relative to spec because it leans on:
- simulation
- unit tests
- reasoning from mechanism

Original task required practical verification that:
1. `tasklist-index.md` is not resolvable by the isolated subprocess
2. ~14K token reduction per phase is confirmed
3. no stale `.isolation/phase-*` directories remain after execution
4. evidence is reviewed under strict verification expectations

See:
- `.dev/releases/complete/v2.25.7-Phase8HaltFix/phase-6-tasklist.md:80-100`
- `.dev/releases/complete/v2.25.7-Phase8HaltFix/artifacts/D-0022/evidence.md`

## Instructions
1. Use actual sprint execution behavior to verify isolation in practice.
2. Construct a practical verification approach that demonstrates:
   - subprocess gets only the isolated phase file context
   - `tasklist-index.md` cannot be resolved from that isolated context
3. Capture concrete evidence from real filesystem state during execution:
   - isolation dir contents before subprocess launch
   - absence of `tasklist-index.md` in effective subprocess scope
   - cleanup state after completion/failure
4. Reconfirm the token-reduction claim with explicit calculation tied to the actual tasklist files used by this release bundle.
5. If possible within the tool/task framework, include an independent review pass or clearly documented second-pass verification.
6. Keep the work focused on strict evidence, not redesign.

## Acceptance criteria
- Practical execution evidence demonstrates `tasklist-index.md` is unreachable from the isolated subprocess context
- Evidence shows the isolation directory contains only the intended phase file at launch time
- Evidence shows no stale `.isolation/phase-*` directories remain after execution
- ~14K token reduction claim is confirmed with explicit file-based calculation
- D-0022 is updated so the result is based on practical strict verification, not mostly simulation

## Required validation
- Real execution-based verification, not unit tests alone
- Updated D-0022 evidence artifact with:
  - commands / scenario
  - observed directory state
  - observed cleanup state
  - token calculation
  - final conclusion tied directly to SC-005

---

## Execution order

1. **RT-01** — finish runtime wiring gap
2. **RT-02** — exact validation rerun
3. **RT-03** — true smoke run
4. **RT-04** — strict practical isolation verification

## Completion rule

Do **not** mark this remediation complete unless each of the 4 mapped tasks can now be truthfully classified as:

- **Complete**
- **to spec**
- **supported by direct evidence matching the original acceptance criteria**
