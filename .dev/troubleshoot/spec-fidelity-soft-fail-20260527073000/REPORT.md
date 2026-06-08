---
status: success
tier_reached: 1
confidence: 0.93
escalation_reason: none (single-domain, high confidence, contract-extension request)
behavior_is_documented: true
test_is_wrong: false
fix_authorized: false
---

# Troubleshoot Report — spec-fidelity hard-halt → opt-in soft-fail

**Target:** Roadmap pipeline halts at `spec-fidelity` step with `Convergence not reached after 3 runs`; user wants soft-fail-after-N-runs behavior.
**Tier reached:** 1
**Confidence:** 0.93 (calibrated)
**Output dir:** `.dev/troubleshoot/spec-fidelity-soft-fail-20260527073000/`

## Summary

The reported "halt" is **documented behavior, not a bug**: `convergence.py:451` defines the pass condition as `registry.get_active_high_count() == 0`, and `executor.py:1466` translates `ConvergenceResult.passed=False` into `StepStatus.FAIL`, which `execute_roadmap` (executor.py:3137-3164) promotes to `sys.exit(1)` after the spec-patch resume cycle fails. The user is requesting a **contract extension**: an opt-in soft-fail path that converts convergence-exhaustion (but NOT crashes/timeouts) into a `StepStatus.PASS` with a warning, allowing downstream steps to run on a `validation_complete: false` / degraded fidelity report. The infrastructure for this already exists (`'degraded'` enum in `_derive_fidelity_status`, `generate_degraded_report`) — only the trigger surface needs widening. Recommended seam: a new `RoadmapConfig.spec_fidelity_soft_fail: bool = False` flag + a one-line guard in `roadmap_run_step`.

## Documentation Context

- **FR-7 (convergence contract):** `Pass condition: registry.get_active_high_count() == 0` at `convergence.py:539`. **Restriction-locked** per the recently-merged PR #92 audit; the soft-fail must NOT relax this predicate.
- **`max_runs=3` is a hard default** at `convergence.py:440`. Also restriction-locked; soft-fail must NOT increase the limit to mask exhaustion.
- **`'degraded'` enum already exists** at `executor.py:2685` (`_derive_fidelity_status` returns `pass | fail | skipped | degraded`). Convergence-mode FAIL reports already write `validation_complete: false` (`executor.py:1497-1499`), so the report shape already matches the degraded contract.
- **Backward compatibility:** Default behavior must remain hard-halt. New behavior is opt-in only.

## Diagnosis

The current "halt on convergence-not-reached" behavior is the contracted behavior of the FR-7 fidelity gate. The change being requested is a behavioral extension that the user has authorized. The smallest correct change introduces a new `spec_fidelity_soft_fail` flag and consumes it at exactly one architectural seam.

## Evidence

| File:Line | What it shows |
|---|---|
| `src/superclaude/cli/roadmap/convergence.py:539` | `if active_highs == 0:` — restriction-locked binary pass predicate |
| `src/superclaude/cli/roadmap/convergence.py:440` | `max_runs: int = 3,` — restriction-locked default |
| `src/superclaude/cli/roadmap/convergence.py:653-668` | "All runs exhausted without convergence" → `ConvergenceResult(passed=False, halt_reason="Convergence not reached after {max_runs} runs. ...")` |
| `src/superclaude/cli/roadmap/executor.py:1466` | `status = StepStatus.PASS if result.passed else StepStatus.FAIL` — **the single architectural seam for the soft-fail promotion** |
| `src/superclaude/cli/roadmap/executor.py:1497-1499` | Degraded report already writes `validation_complete: false`, `tasklist_ready: false` |
| `src/superclaude/cli/roadmap/executor.py:2685-2700` | `_derive_fidelity_status` already returns `'degraded'` for `validation_complete: false` reports |
| `src/superclaude/cli/roadmap/executor.py:3137-3164` | `execute_roadmap` halts (`sys.exit(1)`) when `StepStatus.FAIL` survives the spec-patch resume cycle |
| `src/superclaude/cli/roadmap/models.py:111-126` | `RoadmapConfig` has clean dataclass-bool slots (`convergence_enabled`, `allow_regeneration`, `compress_enabled`) — soft-fail flag fits the established pattern |

## Proposed Fix

**1. `src/superclaude/cli/roadmap/models.py:RoadmapConfig`** — add the opt-in flag (additive, no behavior change for existing users):

```python
spec_fidelity_soft_fail: bool = (
    False  # opt-in: when True, convergence-exhaustion after max_runs is
           # demoted from StepStatus.FAIL (pipeline halt) to StepStatus.PASS
           # with a SOFT-FAIL WARNING gate_failure_reason. Only applies to
           # convergence-not-reached; crashes/timeouts still hard-FAIL.
)
```

**2. `src/superclaude/cli/roadmap/executor.py:roadmap_run_step` (around line 1466)** — guard the FAIL→PASS promotion on (a) flag set, (b) `result.run_count == max_runs`, (c) `halt_reason` starts with `"Convergence not reached after"` (distinguishes orderly exhaustion from crash/timeout):

```python
# Existing line:
# status = StepStatus.PASS if result.passed else StepStatus.FAIL

# Replacement:
if result.passed:
    status = StepStatus.PASS
    gate_reason = None
elif (
    config.spec_fidelity_soft_fail
    and result.run_count == 3  # use config.max_runs once that's pluggable
    and result.halt_reason
    and result.halt_reason.startswith("Convergence not reached after")
):
    status = StepStatus.PASS
    gate_reason = (
        "[SOFT-FAIL WARNING] Convergence did not reach 0 active HIGHs after "
        f"{result.run_count} runs (remaining: {result.final_high_count}); "
        "downstream steps continue per spec_fidelity_soft_fail=True. "
        "The degraded fidelity report is at the step's output_file."
    )
    _log.warning(gate_reason)
else:
    status = StepStatus.FAIL
    gate_reason = result.halt_reason or "Convergence did not pass"
```

**3. CLI** — expose `--allow-spec-fidelity-soft-fail` on `superclaude roadmap run`. Emit a one-line warning to stdout at pipeline startup when set, so the operator is reminded they're in degraded-allowed mode.

**4. Tests (`tests/roadmap/test_executor.py` or new sibling)** — three new cases:

- `test_spec_fidelity_hard_fail_is_default` — regression-lock: default `RoadmapConfig` + convergence-not-reached → `StepStatus.FAIL`.
- `test_spec_fidelity_soft_fail_promotes_to_pass` — flag ON + convergence-not-reached → `StepStatus.PASS`, `gate_failure_reason` contains `"SOFT-FAIL WARNING"`.
- `test_spec_fidelity_soft_fail_still_fails_on_crash` — flag ON + agent crash / timeout (not convergence-exhaustion) → `StepStatus.FAIL` (do NOT silently swallow real crashes).

**5. Docs** — update the roadmap skill (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md`) and CLI help text to describe the new flag and when to use it.

**Estimated change size:** ~5 LOC in `models.py`, ~10 LOC in `executor.py`, ~50 LOC of tests, ~20 LOC of doc updates. Single-file production-code patch.

## Alternative Fixes Considered (and rejected)

- **Raise `max_runs` from 3 to N** — restriction-locked per the recent task audit (`convergence.py:440`); doesn't address the structural case where the spec genuinely has unmatched canonical IDs the canonicalizer can't collapse (post PR #92).
- **Relax the pass predicate to `active_high_count <= K`** — restriction-locked per `convergence.py:539`; would silently change the semantics of FR-7 for every consumer of the gate, not just the operator who wants soft-fail.
- **Move the soft-fail policy inside `execute_fidelity_with_convergence`** — spreads the policy decision across the convergence module and tangles "convergence determinism" with "operator policy"; the right seam is at the StepResult-mapping layer in `executor.py`.

## Risk + Rollback

| Risk | Mitigation |
|---|---|
| Soft-fail masks real spec/roadmap drift that should block release | Flag is opt-in (default OFF); degraded report still records the genuine HIGH count + `validation_complete: false`; release-gate and retrospective tooling can grep for the `"SOFT-FAIL WARNING"` marker |
| Crash/timeout promoted to PASS | Promotion guard requires `halt_reason.startswith("Convergence not reached after")` — only the orderly-exhaustion case is soft-failed; crashes/timeouts still surface as FAIL with their original halt_reason |
| Downstream steps assume `tasklist_ready: true` | The degraded report already writes `tasklist_ready: false`; a Phase-1 sanity check should grep for `tasklist_ready` consumers under `src/superclaude/cli/roadmap/` to confirm they short-circuit cleanly on `false` |
| Telemetry hides degraded passes | The new `gate_failure_reason` contains `"SOFT-FAIL WARNING"` — observable from logs and from the StepResult contract |

**Rollback:** Set `spec_fidelity_soft_fail=False` (the default) or omit the new CLI flag. The patch is fully additive — no existing user is affected without explicit opt-in.

## Next Steps

This run did NOT use `--fix`, so this report stands as diagnosis-only. To proceed:

- **Re-run with `--fix`** if you want the protocol to scaffold an MDTM task file via `task-builder` and offer the Tier 3 remediation chain.
- **OR run `/task`-like work directly** by implementing the 5 atoms above on a new feature branch.

If you do want the task-builder handoff, the natural BUILD_REQUEST shape would be:

- GOAL: "Add opt-in `spec_fidelity_soft_fail` flag to RoadmapConfig + CLI; demote convergence-exhaustion from StepStatus.FAIL to StepStatus.PASS-with-warning when the flag is set."
- WHY: "Operator wants downstream pipeline steps to continue running when spec-fidelity convergence cannot reach 0 active HIGHs — e.g., when the spec genuinely has unmatched IDs the canonicalizer (post PR #92) can't collapse."
- WHERE: `src/superclaude/cli/roadmap/models.py`, `src/superclaude/cli/roadmap/executor.py:1466`, `src/superclaude/cli/roadmap/cli.py` (CLI wiring), `tests/roadmap/test_executor.py`, `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`.
- TEMPLATE: generic (template 01) — change is < 100 LOC across 4-5 files.

## Grounding Gaps

None for the diagnosis itself. One open question for the remediation phase: a 5-minute grep for `spec-fidelity` consumers in the post-step pipeline (anti-instinct, deviation-analysis, remediate, certify) to confirm they short-circuit cleanly on `tasklist_ready: false`. This is a phase-1 sanity check, not a diagnosis blocker.
