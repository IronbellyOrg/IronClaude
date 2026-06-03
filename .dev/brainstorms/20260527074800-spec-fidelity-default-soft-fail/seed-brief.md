---
topic: "Make spec-fidelity soft-fail the default behavior in the roadmap pipeline (no opt-in flag)"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-05-27T07:48:00Z
upstream_artifacts:
  - .dev/troubleshoot/spec-fidelity-soft-fail-20260527073000/REPORT.md
  - .dev/troubleshoot/spec-fidelity-soft-fail-20260527073000/tier1-hypothesis.md
  - .dev/troubleshoot/spec-fidelity-soft-fail-20260527073000/doc-context.md
---

# Seed Brief: spec-fidelity default soft-fail

## Problem Statement

The roadmap pipeline currently hard-halts (`sys.exit(1)`) when `execute_fidelity_with_convergence` returns `ConvergenceResult(passed=False)` — i.e., when 3 convergence runs exhaust without driving `active_high_count` to 0. The user has determined that, in practice, residual HIGHs after convergence-exhaustion are typically **structurally unfixable from inside this pipeline** (e.g., genuine missing IDs in the roadmap that the canonicalizer post PR #92 correctly identifies as real phantoms). Hard-halting on these is operator-hostile; the pipeline should log a warning and continue.

The earlier troubleshoot recommended an opt-in flag (`spec_fidelity_soft_fail: bool = False`). The user has REJECTED that framing: the new behavior MUST be the default. No `--allow-…` lane, no operator switch.

## Known Context

- **FR-7 binary pass predicate** at `convergence.py:539` (`active_high_count == 0`) is restriction-locked (per PR #92's restrictions audit). It MUST NOT be relaxed.
- **`max_runs=3` default** at `convergence.py:440` is restriction-locked. It MUST NOT be increased.
- **`'degraded'` status enum** already exists at `executor.py:2685` (`_derive_fidelity_status` returns `pass | fail | skipped | degraded`).
- **Degraded report shape already written** by convergence-mode FAIL path at `executor.py:1497-1499`: `validation_complete: false`, `tasklist_ready: false`.
- **Architectural seam** is the single line at `executor.py:1466`: `status = StepStatus.PASS if result.passed else StepStatus.FAIL`. This is the single line where the FAIL→PASS promotion lives.
- **Discriminator between soft and hard**: `result.halt_reason.startswith("Convergence not reached after")` — only orderly exhaustion is softened; crashes/timeouts retain hard-FAIL semantics.
- **Spec-patch resume cycle** at `executor.py:3147` (`_apply_resume_after_spec_patch`) currently runs BEFORE the hard halt — it tries to recover automatically by patching the spec. This cycle should still run; soft-fail is the LAST resort after resume also fails to drive convergence to 0.
- **Downstream consumers** (anti-instinct, deviation-analysis, remediate, certify) — need to verify they tolerate `tasklist_ready: false` cleanly. Either they short-circuit (acceptable) or they need adaptation.
- **Telemetry / release-gate / retrospective tooling** — anything that filters on `StepStatus.FAIL` to flag pipelines for review needs a NEW marker to distinguish degraded passes from clean passes.

## Constraints

- Default behavior must change to soft-fail-on-convergence-exhaustion (per user mandate).
- FR-7 predicate untouched.
- `max_runs=3` untouched.
- Crashes/timeouts MUST still hard-FAIL.
- Existing tests that asserted hard-halt-on-convergence-fail must be updated, NOT deleted (the assertions should now check for the degraded-PASS shape).
- Telemetry consumers need a discoverable marker for degraded passes (e.g., `gate_failure_reason` prefix, or new `degraded: bool` field on StepResult).
- Spec-patch resume cycle must still run BEFORE soft-fail kicks in (preserves automatic recovery).
- Operator must see the warning clearly in stdout/stderr — soft-fail must not silently mask the residual HIGH count.

## Success Criteria

1. Running `superclaude roadmap run <spec>` against a spec/roadmap pair that produces convergence-exhaustion (e.g., the TUIBBS v1-MVP case with 51 residual HIGHs) results in: spec-fidelity step PASSING-with-warning, pipeline continuing to anti-instinct / deviation-analysis / remediate / certify, and the operator seeing a clearly-marked `[SOFT-FAIL WARNING]` line.
2. Running the same command against a spec/roadmap pair where convergence ACTUALLY succeeds (0 active HIGHs) still results in a clean PASS with no warning.
3. Running the same command against a spec/roadmap pair where the agent CRASHES or TIMES OUT during convergence still results in hard-FAIL and pipeline halt.
4. The 4 downstream steps (anti-instinct, deviation-analysis, remediate, certify) execute without exception when invoked on a `validation_complete: false` / `tasklist_ready: false` fidelity report.
5. `tests/roadmap/test_executor.py` (or new test file) has 3 cases regression-locking the above (soft-pass on exhaustion, hard-FAIL on crash, hard-FAIL on timeout).
6. CLAUDE.md / sc-roadmap-protocol skill documentation reflects the new default behavior.
7. Telemetry consumers can grep for the `[SOFT-FAIL WARNING]` marker to identify degraded passes for review.

## Open Questions

- **Q1**: Should the soft-fail behavior also apply to the `_apply_resume_after_spec_patch` retry? I.e., if the spec-patch retry runs and STILL exhausts convergence, do we soft-fail or hard-FAIL? **Tentative answer**: soft-fail. The retry was a best effort; once it fails, downstream should still run.
- **Q2**: Should the soft-fail StepResult carry a NEW `degraded: bool` field, or is the `gate_failure_reason` prefix sufficient? **Tentative answer**: prefer a new structured field for telemetry, but if StepResult is widely-consumed, a prefix is the lower-risk path. Adversarial debate should resolve.
- **Q3**: How should the spec-patch resume cycle interact with the new soft-fail default? Currently it runs BEFORE the halt. **Tentative answer**: keep the cycle, but on its FINAL failure also soft-fail (not hard-FAIL). This preserves the automatic-recovery attempt while ensuring the pipeline doesn't halt.
- **Q4**: Is there an escape hatch for users who explicitly WANT hard-halt-on-convergence-fail (e.g., CI gates that need to block on residual HIGHs)? **User position**: NO — they explicitly do not want an opt-in flag. So no escape hatch by flag. The remaining option is environment variable (e.g., `SUPERCLAUDE_ROADMAP_STRICT_FIDELITY=1`) which is much less discoverable than a CLI flag and matches the user's "no opt-in" framing in spirit (the default is soft; strict mode is an undocumented power-user knob). Adversarial debate should decide whether this hatch is justified.
- **Q5**: Should the convergence-mode degraded report be enriched (e.g., add a `degraded_reason: "convergence-exhaustion"` field to the frontmatter) to help downstream consumers distinguish degraded-due-to-convergence from degraded-due-to-agent-crash? **Tentative answer**: yes, low-cost and high-value for observability.

## Enrichment Context

The architectural seams are already grounded in `.dev/troubleshoot/spec-fidelity-soft-fail-20260527073000/REPORT.md` (file:line citations verified during Tier 1 grounding). No additional codebase enrichment needed.
