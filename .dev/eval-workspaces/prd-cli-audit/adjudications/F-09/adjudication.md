# F-09 Adjudication — `_handle_shutdown` accesses non-populated `step` on PrdStepResult

**Finding source**: `.dev/eval-workspaces/prd-cli-audit/findings/F-09-handle-shutdown-nonexistent-step-attr.md`
**Code under review**:
- `src/superclaude/cli/prd/executor.py:957-970` (`_handle_shutdown`)
- `src/superclaude/cli/prd/models.py:219-233` (`PrdStepResult`)
- `src/superclaude/cli/pipeline/models.py:102-115` (`StepResult` base)

---

## Re-verification (ground truth)

1. **`_handle_shutdown` body** (`src/superclaude/cli/prd/executor.py:957-970`) — confirmed accesses `last.step` and `last.step.name`:
   ```python
   completed = [r for r in self._step_results if r.status.is_terminal]
   if completed:
       last = completed[-1]
       last_step = (
           getattr(last.step, "name", "unknown") if last.step else "unknown"
       )
       result.halt_step = last_step
   ```

2. **`PrdStepResult` declared fields** (`src/superclaude/cli/prd/models.py:219-233`) — confirmed it declares only `exit_code`, `output_bytes`, `error_bytes`, `artifacts_produced`, `agent_type`, `fix_cycle`, `qa_verdict`. **No `step` field is added.**

3. **Base class `StepResult`** (`src/superclaude/cli/pipeline/models.py:102-115`) — confirmed `step: Optional[Step] = None` is declared on the base dataclass and inherited.

   **=> `last.step` does NOT raise AttributeError. It evaluates to `None`.** The finding's "Outcome B" (AttributeError crash) is ruled out.

4. **Is `step` ever populated on a PrdStepResult?** Grepped all 9 `PrdStepResult(...)` constructors in `src/superclaude/cli/prd/executor.py` (lines 434, 479, 506, 548, 797, 829, 902, 914, 923) — none pass `step=...`. Grepped for `.step\s*=` assignment patterns inside `prd/executor.py` — zero hits. **The field is structurally present but never populated by the PRD module.**

5. **SIGINT plumbing** confirmed at `src/superclaude/cli/prd/executor.py:179-200` (signal handler installs SIGINT/SIGTERM) and `:373` (loop calls `self._handle_shutdown(result)` when `shutdown_requested`). So this code path is real on Ctrl-C during a long run.

**Verdict on the dual-outcome question:** Outcome A (silent `"unknown"`), not Outcome B (crash). The `getattr(..., "name", "unknown") if last.step else "unknown"` is double-defensive — the `if last.step` short-circuits because `last.step is None`, returning `"unknown"`.

---

## Persona 1 — Analyzer (reproducibility)

**Scenario:** User sends SIGINT mid-pipeline after several steps have completed terminally.

**Trace:**
- `_signal_handler.shutdown_requested` flips True.
- Main loop at `executor.py:373` calls `_handle_shutdown(result)`.
- `result.outcome = "interrupted"`, `finished_at` stamped.
- `completed` list is non-empty (terminal steps have accumulated).
- `last = completed[-1]` — a real `PrdStepResult` with valid status, exit_code, etc.
- `last.step` resolves via inherited `StepResult.step` default → `None`.
- `if last.step` → False → `last_step = "unknown"`.
- `result.halt_step = "unknown"`, `result.halt_reason = "Signal-interrupted shutdown"`.

**Reproducibility:** Deterministic. Every SIGINT during PRD execution writes `halt_step="unknown"` regardless of which step was actually executing. **No crash, no AttributeError**, no exception that would mask further shutdown work. The shutdown handler completes "successfully" with wrong data.

**Caveat to the finding:** the finding's stated confidence 0.85 hedged on whether base class has `step`. Now confirmed: base has it. Outcome is purely silent wrong-data, not partial crash.

---

## Persona 2 — Refactorer (blast radius)

**Other `.step` accesses on `PrdStepResult` instances within the PRD module:**
- `grep -nE '\bresult\.step\b|\blast\.step\b|\.step\.name' src/superclaude/cli/prd/executor.py` returns exactly one hit — `:967`. The defect is isolated.

**Other places that consume `halt_step`:**
- The `halt_step` field on `PrdPipelineResult` (`src/superclaude/cli/prd/models.py:250`) is set in several legitimate places (`executor.py:836`, etc.) with real `qa_step_id` strings. Only the shutdown path injects `"unknown"`. Downstream consumers (resume logic, telemetry, TUI summary) will see `"unknown"` mixed in with real step IDs, but they will not crash on it — it's a free-form `Optional[str]`.

**Pattern check — could other code rely on a populated `step` attribute on PrdStepResult?** Grepped — no other reader uses `result.step` on PRD step results. The base `Step` object would normally be the canonical link back to the schedule entry, but the PRD pipeline does not carry `Step` instances forward into results (steps are identified by string `step_id` instead). So the contract is implicitly "step_id is the identifier; the dataclass `step` field is unused" — which is fine as a design choice, but `_handle_shutdown` violates it by reaching for `last.step.name`.

**Blast radius:** Narrow. One call site, one bug. No corruption of other state; downstream just gets a misleading `halt_step` value.

---

## Persona 3 — Architect (severity calibration)

**Preliminary severity:** HIGH (assumed crash possibility).

**Recalibration:**
- Crash path is ruled out (StepResult.step exists, defaults to None).
- Real impact: resume / telemetry / post-mortem all see `halt_step="unknown"` for every signal-interrupted run, regardless of which step was actually mid-flight. The information is structurally lost.
- The shutdown handler is specifically called out by NFR-PRD.9 ("preserve state for resume") at `executor.py:954`. The whole point of this code is to record which step the user can resume from. It silently fails its single job.
- Severity floor: this is wrong-data in the artifact the user/automation will look at to resume. Not a crash, not a security issue, not data loss in the artifacts already written — but a direct violation of the NFR the function exists to satisfy.
- Severity ceiling: not catastrophic — the run's actual artifacts persist; only the resume hint is wrong. Operators can recover by inspecting the `step_results` list directly.

**Calibrated severity: MEDIUM.** Silent wrong-data defeating the documented NFR-PRD.9 contract, narrow blast radius, no crash, deterministic, and the correct value (`step_id`) is trivially recoverable from `_step_results` — but operators acting on `halt_step` get garbage.

---

## Convergence

**Verdict:** VALID DEFECT, RE-CALIBRATED.

| Dimension | Value |
|---|---|
| Reproducible | Yes, deterministic on every SIGINT during PRD run |
| Manifests as | Silent `halt_step="unknown"` (Outcome A), not AttributeError (Outcome B ruled out) |
| Blast radius | One call site (`executor.py:967`), no cascading corruption |
| NFR violated | NFR-PRD.9 (preserve state for resume) |
| Final severity | **MEDIUM** (down-graded from HIGH) |
| Fix difficulty | **TRIVIAL** — replace `getattr(last.step, "name", "unknown") if last.step else "unknown"` with the step_id that was used to build that result. The PRD pipeline already tracks step identity by string at every call site that constructs a `PrdStepResult`; the easiest fix is to also store that string on the result (e.g. add `step_id: str = ""` to `PrdStepResult` and populate at construction). Alternatively, replace the dereference with a lookup against the step schedule by index. ~5-15 LOC. |
| Convergence score | **0.95** — three personas agree the defect is real and isolated; the only disagreement is whether severity is HIGH or MEDIUM, and that is resolved by confirming Outcome A is what actually fires. |

**Synthesis:**

The finding is real but the severity-driving assumption (potential AttributeError crash, Outcome B) is incorrect. The inherited `StepResult.step: Optional[Step] = None` field at `src/superclaude/cli/pipeline/models.py:106` guarantees `last.step` evaluates to `None`, and the existing `if last.step else "unknown"` guard handles that branch deterministically. So `_handle_shutdown` always records `halt_step="unknown"` after a SIGINT, silently defeating NFR-PRD.9's resume guarantee. Blast radius is one line — no other PRD code reads `PrdStepResult.step`. Severity MEDIUM (not HIGH), fix is trivial: the PRD pipeline tracks step identity via `step_id` strings everywhere; either persist that string on `PrdStepResult` at construction, or look it up from the schedule using the result's index in `_step_results`.

**Recommended fix sketch (not applied — read-only adjudication):**
1. Add `step_id: str = ""` to `PrdStepResult` (`src/superclaude/cli/prd/models.py:219`).
2. Pass `step_id=step_id` at each construction site in `executor.py` where the id is already in scope.
3. Replace lines 966-968 in `_handle_shutdown` with `last_step = last.step_id or "unknown"`.
