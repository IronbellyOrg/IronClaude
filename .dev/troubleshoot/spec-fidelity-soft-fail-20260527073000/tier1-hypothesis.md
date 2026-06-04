# Hypothesis Card — Tier 1

**Symptom:** Roadmap pipeline halts at `spec-fidelity` step with `Convergence not reached after 3 runs. Remaining active HIGHs: 51`. User wants step to soft-fail (warn + continue) after `max_runs=3` exhausts, not hard-halt.

## Claim

The "hard-halt on convergence-not-reached" behavior is **documented contract**, not a bug — `convergence.py:451` literally says "Pass condition: `registry.get_active_high_count() == 0`" and `executor.py:1466` translates `result.passed=False` into `StepStatus.FAIL`, which `execute_roadmap` at executor.py:3137-3164 promotes to `sys.exit(1)` after the spec-patch resume cycle fails. The user is requesting a **behavior change**: add an opt-in soft-fail path that converts convergence-exhaustion (specifically, NOT crashes/timeouts) into a `StepStatus.PASS` with a warning, allowing downstream steps to run on a `validation_complete: false` / degraded fidelity report.

## Evidence (file:line cited)

- **`src/superclaude/cli/roadmap/convergence.py:539`** — `if active_highs == 0:` is the binary pass predicate; restriction-locked post PR #92.
- **`src/superclaude/cli/roadmap/convergence.py:653-668`** — `# All runs exhausted without convergence` returns `ConvergenceResult(passed=False, halt_reason="Convergence not reached after {max_runs} runs. ...")`. This is the exact failure-mode the user hit.
- **`src/superclaude/cli/roadmap/executor.py:1466-1478`** — `roadmap_run_step` for spec-fidelity converts `ConvergenceResult` → `StepResult`: `status = StepStatus.PASS if result.passed else StepStatus.FAIL`. **This is the single line where the soft-fail promotion needs to live.**
- **`src/superclaude/cli/roadmap/executor.py:3137-3164`** — `execute_roadmap` checks for any `StepStatus.FAIL`, attempts `_apply_resume_after_spec_patch` (the spec-patch retry cycle), then halts with `sys.exit(1)` if no resume.
- **`src/superclaude/cli/roadmap/executor.py:2685-2700`** — `_derive_fidelity_status` already enumerates four states: `pass | fail | skipped | degraded`. The `'degraded'` bucket is reachable only via `validation_complete: false` in the report. The convergence-mode failure report at `executor.py:1497-1499` already writes `validation_complete: false`. So the report shape ALREADY matches the degraded contract — the missing piece is JUST the StepStatus mapping.
- **`src/superclaude/cli/roadmap/models.py:111-126`** — `RoadmapConfig` precedent flags: `convergence_enabled`, `allow_regeneration`, `compress_enabled` — clean dataclass-bool slots; the soft-fail flag fits the established pattern.

## Diagnosis

The current behavior is correct per the documented contract (`behavior_is_documented=true` in Case A semantics from the protocol's derivation rule). The change being requested is a **contract extension**, not a bug fix. The user is the contract owner and has explicitly authorized the extension via this request.

**The smallest change that meets the user's stated goal:**

1. **`models.py:RoadmapConfig`** — add `spec_fidelity_soft_fail: bool = False` flag (additive, default off → no behavior change for existing users).
2. **`executor.py:roadmap_run_step` for spec-fidelity (around line 1466)** — when `result.passed == False` AND `result.run_count == max_runs` AND `result.halt_reason` starts with `"Convergence not reached after"` (distinguishing convergence-exhaustion from crash/timeout) AND `config.spec_fidelity_soft_fail == True` → return `StepStatus.PASS` with `gate_failure_reason="[SOFT-FAIL WARNING] Convergence did not reach 0 active HIGHs after {max_runs} runs; downstream steps continue per spec_fidelity_soft_fail=True"`. The existing `_write_convergence_report` already emits `validation_complete: false`, which `_derive_fidelity_status` already maps to `'degraded'`.
3. **CLI** — expose flag as `--allow-spec-fidelity-soft-fail` on the `superclaude roadmap run` command. The flag should also surface a one-line warning to stdout at pipeline startup when set, so the operator is reminded they're running in degraded-allowed mode.
4. **Tests** — three new tests in `tests/roadmap/test_executor.py` (or test_convergence.py):
   - Default behavior: convergence-not-reached → StepStatus.FAIL, pipeline halts (regression-lock current contract).
   - `spec_fidelity_soft_fail=True` + convergence exhaustion → StepStatus.PASS, `gate_failure_reason` contains "SOFT-FAIL WARNING".
   - `spec_fidelity_soft_fail=True` + actual crash (e.g., agent timeout, not convergence exhaustion) → StepStatus.FAIL (do NOT silently swallow real crashes).
5. **Doc update** — surface the flag in the roadmap skill / CLI help text and in the SOP doc that explains the spec-fidelity gate.

## Risks

| Risk | Mitigation |
|---|---|
| Soft-fail masks real spec/roadmap drift that should block release | Flag is opt-in (default OFF); when ON, the degraded report still records `total_deviations: N` so downstream tooling (release-gate, retrospective) can see the genuine HIGH count |
| Soft-fail accidentally promotes crash/timeout to PASS | Guard the promotion on `halt_reason.startswith("Convergence not reached after")` so only the orderly exhaustion case is soft-failed; crashes (agent timeout, internal exception) still surface as FAIL |
| Downstream steps (anti-instinct, deviation-analysis, remediate, certify) may assume `tasklist_ready: true` | The degraded report already writes `tasklist_ready: false`; downstream consumers that depend on tasklist_ready will naturally short-circuit or run in degraded mode. Worth a quick grep for `tasklist_ready` consumers as a Phase-1 verification of any forthcoming PR. |
| Telemetry / observability dashboards count FAILs to flag pipelines for review — soft-fail hides this signal | The new gate_failure_reason explicitly contains `"SOFT-FAIL WARNING"`; dashboards can grep this marker and surface degraded passes separately from clean passes |

## Confidence (self-reported, before calibrator)

**0.92** — single-domain (pipeline orchestration); existing 'degraded' enum infrastructure to reuse; the architectural seam (executor.py:1466) is unambiguous; restriction-locked elements (convergence.py:539, max_runs=3) are not touched by the proposed fix; user has explicitly authorized the contract change.

## If I'm wrong, it's probably because...

...there's a downstream consumer (in `_apply_resume_after_spec_patch`, `_auto_invoke_validate`, or one of the post-spec-fidelity steps like `anti-instinct` / `deviation-analysis`) that treats spec-fidelity FAIL as a load-bearing signal beyond "the pipeline halts" — meaning the soft-fail StepStatus promotion would let the pipeline run but produce nonsensical or empty downstream outputs. A 5-minute grep for `spec-fidelity` consumers under `src/superclaude/cli/roadmap/` is the minimum diligence before writing the patch.

## consistency_with_docs

**aligned** — the proposed fix EXTENDS the documented contract (adds an opt-in flag), it does not contradict it. The current behavior remains the default. The semantic restrictions (FR-7 binary pass predicate at `convergence.py:539`, `max_runs=3` at `convergence.py:440`) remain untouched.

## test_is_wrong

**false** — there is no failing test; the symptom is operator-reported pipeline behavior, not a test assertion.

## behavior_is_documented

**true** — but with a critical caveat: the user is the contract owner and has authorized the contract extension. Per the protocol's Case A semantics, the remediation is normally a spec/doc change or stakeholder discussion. Here, both apply: the code change implements the new contract AND the docs need updating to describe the new opt-in flag. This is NOT a case where the protocol should refuse to recommend a code fix — the user IS the stakeholder, and the discussion has happened in this prompt.
