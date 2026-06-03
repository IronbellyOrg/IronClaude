# Documentation Context Card

**Symptom:** spec-fidelity step FAIL hard-halts the roadmap pipeline; user wants soft-fail-after-N-runs behavior.

## Release context

None found in `.dev/releases/current/` for IronClaude itself (the failure transcript references TUIBBS-scp's v1-MVP release, not an IronClaude release). The change being requested is an IronClaude pipeline-feature change.

## Architectural docs consulted

| Doc | Currency | Notes |
|---|---|---|
| `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` | unknown | Describes the roadmap pipeline at the skill level |
| `src/superclaude/cli/roadmap/prompts.py:580+` | current (touched in HEAD) | References "spec-fidelity deviation" as a category; the gate is a strict-by-design quality bar |
| `src/superclaude/cli/roadmap/convergence.py` (FR-7) | current | Module docstring: "Convergence-controlled fidelity gate (FR-7). Coordinates up to max_runs (default 3) checker/remediation cycles ... Pass condition: registry.get_active_high_count() == 0" |
| `src/superclaude/cli/roadmap/executor.py:2685+` `_derive_fidelity_status` | current | Already enumerates four states: `pass | fail | skipped | degraded` — the 'degraded' bucket EXISTS but is currently only reachable via `generate_degraded_report` (agent-side failure), not via convergence-exhaustion |

## Restrictions / decisions that constrain the fix

1. **FR-7 (convergence contract):** `Pass condition: registry.get_active_high_count() == 0` at `convergence.py:539`. Per the now-merged PR #92 work, this predicate is restriction-locked — must not be relaxed. The soft-fail behavior must live OUTSIDE the convergence loop (at the step-result interpretation layer in `executor.py:roadmap_run_step`), not inside `execute_fidelity_with_convergence`.
2. **`max_runs=3` is a hard default** (`convergence.py:440`, also restriction-locked per `.dev/tasks/.../research/05-restrictions-doc-context.md`). Soft-fail must not increase `max_runs` to mask exhaustion.
3. **Existing `'degraded'` enum is the natural soft-fail target** (`executor.py:2685`): `_derive_fidelity_status` already returns `'degraded'` when `validation_complete: false`. The convergence-mode FAIL report at `executor.py:1497-1499` already writes `validation_complete: false` and `tasklist_ready: false` — so the report shape already matches the degraded contract.
4. **Spec-patch resume cycle** (`_apply_resume_after_spec_patch` at executor.py:3147) exists to attempt automatic recovery on spec-fidelity FAIL. The new soft-fail should be applied AFTER that resume cycle has failed — soft-fail is the last-resort warning, not a replacement for the spec-patch retry.
5. **Backward compatibility:** Default behavior must remain hard-halt (existing users rely on the strict gate). Soft-fail is opt-in only — new RoadmapConfig flag + CLI flag.

## Re-frame signals

- The user's framing ("unsolveable problem") is partially documented behavior: the convergence loop is INTENTIONALLY a hard gate (FR-7). Changing it to soft-fail is a contract change, not a bug fix.
- The infrastructure for soft-fail ALREADY EXISTS via the `'degraded'` enum and `generate_degraded_report`. The change is to extend the trigger surface (current: agent crash; new: convergence exhaustion + opt-in flag).
- The right architectural seam is `roadmap_run_step` at `executor.py:1466` (`status = StepStatus.PASS if result.passed else StepStatus.FAIL`). Promoting convergence-not-reached to PASS-with-warning here is one-line plus a guard.
