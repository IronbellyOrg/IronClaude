---
title: "P3: cli_portify Gate Enforcement — Unified Proposal"
date: 2026-03-25
status: approved
origin: adversarial evaluation of Proposal A (Shadow-First) vs Proposal B (Per-Gate Opt-In)
winner: Proposal A (Shadow-First Graduated Enforcement)
---

# P3: cli_portify Gate Enforcement — Unified Proposal

## Adversarial Evaluation

### Proposal A (Shadow-First Graduated Enforcement): Strengths

1. **Proven pattern.** `SprintGatePolicy` in `sprint/executor.py` already implements shadow/soft/full graduation. Reusing the same three-mode shape means operators and tests speak one vocabulary across both pipelines.

2. **Blast-radius control.** Shadow mode evaluates every gate without halting anything. This produces real pass/fail telemetry from production runs before a single pipeline is blocked --- the only safe way to calibrate STRICT-tier semantic checks like `section_count >= 5` or `convergence_terminal`.

3. **Single CLI knob (`--gate-mode`).** One flag controls all gates. Easy to document, easy to override in CI, easy to grep for in logs.

4. **Soft mode is a missing middle.** Proposal B has no equivalent of "warn but do not block." Soft mode lets teams observe gate failures in TUI output and diagnostics without pipeline disruption --- critical for the transition period where borderline artifacts are common.

5. **Clean diagnostics path.** In `full` mode, `GateFailure` flows directly into `DiagnosticsCollector.record_gate_failure()`, which already exists and is tested. No new wiring needed.

### Proposal A: Weaknesses

1. **Graduation is manual and global.** Promoting from shadow to soft to full is an operator decision with no per-gate granularity. A single flaky STRICT gate (e.g., `has_step_count_consistency`) forces the entire pipeline to stay in soft mode.

2. **Log noise in shadow mode.** Every gate evaluation is logged even when no enforcement occurs. Without filtering, this clutters execution logs for operators who only care about failures.

3. **No fast-lane for trivially safe gates.** EXEMPT and LIGHT tier gates could be enforced from day one with near-zero risk, but Proposal A treats them identically to STRICT gates under the global mode.

---

### Proposal B (Inline Enforcement with Per-Gate Opt-In): Strengths

1. **Per-gate granularity.** Each `GateCriteria` carries its own `enforce: bool`, so EXEMPT/LIGHT gates can be enforced immediately while STRICT gates remain advisory. This is the correct risk model: enforcement should track the gate's confidence, not a global switch.

2. **Simpler initial implementation.** No new policy class; the enforcement check is a four-line `if gate.enforce` block in the executor. Fewer moving parts, fewer test fixtures.

3. **Auditability at definition site.** Reading `GATE_REGISTRY` tells you exactly which gates enforce and which do not. No need to cross-reference a runtime mode flag.

### Proposal B: Weaknesses

1. **Mutating `GateCriteria` in `pipeline/models.py` is a cross-pipeline risk.** `GateCriteria` is consumed by sprint, roadmap, and cleanup_audit. Adding `enforce: bool` with a default of `False` is backward-compatible, but any future consumer that sets `enforce=True` at the model level leaks enforcement into all pipelines unless guarded.

2. **No warn mode.** Gates are binary: enforced (halt on failure) or silent (not even logged as a warning). There is no intermediate state where operators can see failures without pipeline disruption.

3. **Scattered decision surface.** When 11 gates each carry their own `enforce` flag, auditing the overall enforcement posture requires scanning the entire registry. A global mode is immediately queryable.

4. **No graduation telemetry.** Without shadow-mode data, the decision to flip `enforce=True` on a STRICT gate is based on gut feel rather than observed pass rates.

---

## Winner Selection

**Winner: Proposal A (Shadow-First Graduated Enforcement)**

Reasoning:

- The decisive factor is **soft mode**. Proposal B's binary enforce/silent model has no answer for the transition period where operators need to see gate failures without halting pipelines. Soft mode is not a luxury; it is the mechanism that makes STRICT-tier enforcement safe to enable.

- Proposal A's main weakness (no per-gate granularity) is straightforward to fix by absorbing Proposal B's `enforce` flag as a per-gate override. This creates a two-layer system: a global mode sets the floor, and per-gate flags can promote individual gates above the floor.

- Proposal B's main weakness (cross-pipeline model mutation) has no clean fix within its own architecture. Moving `enforce` out of `GateCriteria` and into a portify-specific wrapper re-invents the policy class that Proposal A already provides.

---

## Unified Final Proposal

### Design: Two-Layer Gate Enforcement

Combine Proposal A's three-mode global policy with Proposal B's per-gate promotion capability.

**Layer 1 — Global mode** (`--gate-mode shadow|soft|full`, default `shadow`):
Sets the baseline behavior for all gates.

- `shadow`: Evaluate every gate, log results, never warn, never block.
- `soft`: Evaluate every gate, log + emit TUI warning on failure, never block.
- `full`: Evaluate every gate, block on failure, emit `GateFailure` to diagnostics.

**Layer 2 — Per-gate promotion** (`min_enforce_mode` on `GATE_REGISTRY` entries):
Individual gates can declare a minimum enforcement mode that overrides the global mode upward (never downward). This allows EXEMPT/LIGHT gates to enforce at `full` even when the global mode is `shadow`, without forcing STRICT gates to follow.

Resolution rule: `effective_mode = max(global_mode, gate.min_enforce_mode)` where `shadow < soft < full`.

### Implementation Plan

#### 1. Add `PortifyGateMode` enum and `PortifyGatePolicy` to `cli_portify/executor.py`

```python
from enum import IntEnum

class PortifyGateMode(IntEnum):
    """Gate enforcement modes, ordered by severity."""
    SHADOW = 0
    SOFT = 1
    FULL = 2

@dataclass
class GateEvaluation:
    """Result of evaluating a single gate."""
    step_id: str
    gate_id: str
    tier: str
    passed: bool
    reason: str | None
    effective_mode: PortifyGateMode
    blocked: bool
    failure: GateFailure | None = None

class PortifyGatePolicy:
    """Two-layer gate enforcement for the portify pipeline."""

    def __init__(self, global_mode: PortifyGateMode = PortifyGateMode.SHADOW) -> None:
        self._global_mode = global_mode

    def evaluate(
        self,
        step_id: str,
        output_file: Path | None,
        min_enforce_mode: PortifyGateMode = PortifyGateMode.SHADOW,
    ) -> GateEvaluation:
        effective = max(self._global_mode, min_enforce_mode)

        try:
            criteria = get_gate_criteria(step_id)
        except KeyError:
            return GateEvaluation(
                step_id=step_id, gate_id=step_id, tier="NONE",
                passed=True, reason=None, effective_mode=effective, blocked=False,
            )

        tier = getattr(criteria, "enforcement_tier", "STANDARD")
        gate_id = getattr(criteria, "gate_id", step_id)

        if output_file is None:
            passed, reason = True, None
        else:
            passed, reason = gate_passed(output_file, criteria)

        blocked = (not passed) and (effective == PortifyGateMode.FULL)

        failure = None
        if not passed:
            failure = GateFailure(
                gate_id=gate_id,
                check_name="gate_passed",
                diagnostic=reason or "",
                artifact_path=str(output_file) if output_file else "",
                tier=tier,
            )

        return GateEvaluation(
            step_id=step_id, gate_id=gate_id, tier=tier,
            passed=passed, reason=reason,
            effective_mode=effective, blocked=blocked, failure=failure,
        )
```

#### 2. Add `min_enforce_mode` to portify gate registry entries

Do NOT modify `GateCriteria` in `pipeline/models.py`. Instead, add a parallel portify-local mapping in `cli_portify/gates.py`:

```python
# Per-gate minimum enforcement overrides (Layer 2).
# Gates not listed here default to SHADOW (no override).
from superclaude.cli.cli_portify.executor import PortifyGateMode

GATE_MIN_ENFORCE: dict[str, PortifyGateMode] = {
    # EXEMPT/LIGHT gates: safe to enforce immediately
    "validate-config": PortifyGateMode.FULL,
    # STANDARD gates: promote to soft (warn) by default
    "discover-components": PortifyGateMode.SOFT,
    "brainstorm-gaps": PortifyGateMode.SOFT,
    "models-gates-design": PortifyGateMode.SOFT,
    # STRICT gates: no override, follow global mode
    # "analyze-workflow": PortifyGateMode.SHADOW,  (implicit default)
    # "panel-review": PortifyGateMode.SHADOW,       (implicit default)
}
```

This keeps `GateCriteria` untouched and confines the enforcement decision to the portify pipeline.

#### 3. Replace the consultation block in `executor.py:500-511`

Replace the current lightweight consultation block:

```python
# --- Gate enforcement (two-layer) ---
gate_min = GATE_MIN_ENFORCE.get(step.step_id, PortifyGateMode.SHADOW)
gate_eval = self._gate_policy.evaluate(step.step_id, step.output_file, gate_min)

self._execution_log.gate_eval(
    step.step_id,
    gate_id=gate_eval.gate_id,
    tier=gate_eval.tier,
)

if not gate_eval.passed:
    if gate_eval.effective_mode == PortifyGateMode.SOFT:
        self._tui.gate_warning(step.step_id, gate_eval.reason)
    elif gate_eval.effective_mode == PortifyGateMode.FULL:
        self._diagnostics.record_gate_failure(gate_eval.failure)
        return PortifyStatus.HALT
# Shadow mode: result logged above, no further action

gate_result = "pass" if gate_eval.passed else gate_eval.effective_mode.name.lower()
```

#### 4. Wire `--gate-mode` CLI flag

In `cli_portify/commands.py`, add:

```python
@click.option(
    "--gate-mode",
    type=click.Choice(["shadow", "soft", "full"], case_sensitive=False),
    default="shadow",
    help="Gate enforcement mode: shadow (log only), soft (warn), full (block).",
)
```

Pass through to `PortifyConfig` and into the executor constructor, which instantiates `PortifyGatePolicy(global_mode=...)`.

#### 5. Add `gate_warning()` to `PortifyTUI`

A single new method on the existing TUI class:

```python
def gate_warning(self, step_id: str, reason: str | None) -> None:
    """Emit a visible warning for a soft-mode gate failure."""
    self._console.print(f"[yellow]GATE WARNING[/yellow] {step_id}: {reason or 'unknown'}")
```

#### 6. Preserve `step_runner` test seam

The `step_runner` code path (executor.py lines 472-485) is untouched. Gate evaluation only occurs in the production dispatch path (post line 498). Tests using `step_runner` bypass gate evaluation entirely, preserving all 7+ existing test contracts.

To test gate enforcement itself, add a dedicated `test_gate_policy.py` that instantiates `PortifyGatePolicy` directly --- no executor needed.

#### 7. Graduation criteria (operational, not code)

| Transition | Trigger | Validation |
|---|---|---|
| shadow -> soft | 3+ pipeline runs with gate telemetry collected | Review `execution-log.yaml` for false-positive rate |
| soft -> full | Zero false-positive gate warnings over 5+ runs | Confirm no borderline STRICT failures in diagnostics |
| Per-gate STRICT promotion | Individual gate shows 100% pass rate in soft mode | Flip entry in `GATE_MIN_ENFORCE` to `FULL` |

### Files Modified

| File | Change |
|---|---|
| `src/superclaude/cli/cli_portify/executor.py` | Add `PortifyGateMode`, `GateEvaluation`, `PortifyGatePolicy`; replace consultation block; accept `gate_mode` in constructor |
| `src/superclaude/cli/cli_portify/gates.py` | Add `GATE_MIN_ENFORCE` mapping |
| `src/superclaude/cli/cli_portify/commands.py` | Add `--gate-mode` CLI option |
| `src/superclaude/cli/cli_portify/tui.py` | Add `gate_warning()` method |
| `src/superclaude/cli/cli_portify/models.py` | Add `HALT` to `PortifyStatus` if not present |
| `tests/cli_portify/test_gate_policy.py` | New: unit tests for `PortifyGatePolicy` across all mode combinations |

### What is NOT modified

| File | Reason |
|---|---|
| `src/superclaude/cli/pipeline/models.py` | `GateCriteria` stays unchanged; no `enforce` field added. Cross-pipeline safety preserved. |
| `src/superclaude/cli/pipeline/gates.py` | `gate_passed()` signature unchanged. It remains a pure evaluation function with no enforcement semantics. |
| `src/superclaude/cli/cli_portify/diagnostics.py` | `DiagnosticsCollector.record_gate_failure()` already accepts `GateFailure`. Zero changes needed. |
| Existing executor tests using `step_runner` | Test seam path bypasses gate evaluation. All 7+ tests pass without modification. |

### Risk Summary

| Risk | Mitigation |
|---|---|
| STRICT gates halt pipelines on borderline artifacts | Default mode is `shadow`; STRICT gates have no `min_enforce_mode` override. Enforcement only activates after explicit promotion. |
| Cross-pipeline contamination from model changes | `GateCriteria` is untouched. `GATE_MIN_ENFORCE` is portify-local. |
| Graduation stalls (nobody promotes) | `GATE_MIN_ENFORCE` pre-promotes EXEMPT to `FULL` and STANDARD to `SOFT`, giving immediate value even if global mode stays `shadow`. |
| Test breakage | `step_runner` seam preserved. New gate policy tests are isolated. |
