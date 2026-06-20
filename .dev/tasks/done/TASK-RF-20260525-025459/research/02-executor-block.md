# Research 02 — executor.py L286-340 Cosmetic Remediation Block

**Status:** Complete
**Scope:** `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py`
**Goal:** Map M2 fix surface — wrap cosmetic remediation block in try/except, log via `_log.warning`, fall through to FAIL StepResult.

---

## 1. Module-level logger declaration

File: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py`

Line 38 (verbatim):

```
_log = logging.getLogger("superclaude.pipeline.executor")
```

Note: the logger uses a **fixed dotted name**, not `__name__`. The M2 fix must reference `_log.warning(...)` (already imported at L12: `import logging`).

---

## 2. The L286-340 cosmetic remediation block

### 2a. Enclosing function

`_execute_single_step` — defined at **L191-376**.

Signature (L191-199):

```python
def _execute_single_step(
    step: Step,
    config: PipelineConfig,
    run_step: StepRunner,
    cancel_check: Callable[[], bool],
    on_step_start: Callable[[Step], None] = lambda s: None,
    on_step_complete: Callable[[Step, StepResult], None] = lambda s, r: None,
    trailing_runner: TrailingGateRunner | None = None,
) -> StepResult:
```

### 2b. Nesting context — INSIDE a retry-loop

The retry-loop is opened at **L216**:

```python
for attempt in range(1, max_attempts + 1):
```

The cosmetic remediation block at L286-340 sits **inside** this `for attempt in ...` loop. This means:

- A `try/except` wrapper around L286-341 must be at the **loop-body** indent (4 spaces inside the function, i.e. 8 spaces from column 0 at the `try:` keyword) — the same level as the existing `if (...)` at L286.
- On exception, the natural fall-through is to the existing "Gate failed" path at L343-365, which already handles `attempt < max_attempts` (retry via `continue`) vs. exhausted-retries (build FAIL `StepResult`).
- Therefore the M2 fix does **not** need to construct its own FAIL `StepResult` — it only needs to let control fall through to L343.

### 2c. Verbatim L286-341 block

```python
286:        if (
287:            config.allow_cosmetic_remediation
288:            and config.cosmetic_remediator is not None
289:            and step.gate is not None
290:        ):
291:            gate_name = ""
292:            if step.gate.semantic_checks:
293:                # First failing semantic check determines the gate name passed
294:                # to the classifier. ``gate_passed`` already short-circuits on
295:                # the first failure, so this is the right check to report.
296:                for sc in step.gate.semantic_checks:
297:                    sc_result = sc.check_fn(gate_target.read_text(encoding="utf-8"))
298:                    sc_ok = (
299:                        sc_result if isinstance(sc_result, bool) else bool(sc_result)
300:                    )
301:                    if not sc_ok:
302:                        gate_name = sc.name
303:                        break
304:            if not gate_name:
305:                # Frontmatter / line-count failures don't map onto the cosmetic
306:                # remediator's surface; fall through to normal FAIL handling.
307:                gate_name = "non_semantic_gate"
308:
309:            remediated_ok, transforms = config.cosmetic_remediator(
310:                gate_target,
311:                gate_name,
312:                reason or "",
313:                step_id=step.id,
314:            )
315:            if remediated_ok:
316:                # Re-check post-remediation to confirm the fix held.
317:                recheck_passed, recheck_reason = gate_passed(gate_target, step.gate)
318:                if recheck_passed:
319:                    _log.info(
320:                        "Cosmetic remediation succeeded for step '%s' "
321:                        "(attempt %d/%d): %d transform(s) applied",
322:                        step.id,
323:                        attempt,
324:                        max_attempts,
325:                        len(transforms),
326:                    )
327:                    result = StepResult(
328:                        step=step,
329:                        status=StepStatus.PASS,
330:                        attempt=attempt,
331:                        gate_failure_reason=None,
332:                        started_at=result.started_at,
333:                        finished_at=result.finished_at,
334:                        remediated=True,
335:                        remediations=list(transforms),
336:                    )
337:                    on_step_complete(step, result)
338:                    return result
339:                # Remediator claimed success but gate still fails -- fall through
340:                # to the original FAIL path so the operator sees the real reason.
341:                reason = recheck_reason or reason
```

### 2d. Exception-prone call sites inside the block

The block has multiple sites that can throw — the M2 try/except must wrap all of them:

- **L297**: `gate_target.read_text(encoding="utf-8")` — can raise `OSError`, `UnicodeDecodeError`.
- **L297**: `sc.check_fn(...)` — caller-supplied callable, can raise anything.
- **L309-314**: `config.cosmetic_remediator(...)` — caller-supplied callable; the M1 fix in `cosmetic_remediator.py` is exactly to harden its internals, but a defensive wrap here is the second line of defence.
- **L317**: `gate_passed(gate_target, step.gate)` — runs the gate's `check_fn` callables again.

---

## 3. FAIL-path StepResult construction site

After the cosmetic block falls through, the next executed code is L343-365:

```python
343:        # Gate failed
344:        _log.info(
345:            "Gate failed for step '%s' (attempt %d/%d): %s",
346:            step.id,
347:            attempt,
348:            max_attempts,
349:            reason,
350:        )
351:
352:        if attempt < max_attempts:
353:            continue  # retry
354:
355:        # Exhausted retries
356:        result = StepResult(
357:            step=step,
358:            status=StepStatus.FAIL,
359:            attempt=attempt,
360:            gate_failure_reason=reason,
361:            started_at=result.started_at,
362:            finished_at=result.finished_at,
363:        )
364:        on_step_complete(step, result)
365:        return result
```

The `StepStatus.FAIL` constructor at **L356-363** is the landing site the M2 try/except must hand control to. The `gate_failure_reason=reason` field at L360 is fed from the `reason` variable computed at L267 (and potentially mutated at L341).

**Implication for M2:** the `except` clause must NOT `return` or `raise` — it must merely log and let execution drop through to L343. Conveniently this is what bare `except: ... pass` (or `except Exception: _log.warning(...)` with no return) achieves naturally.

---

## 4. `reason` provenance and recheck-path mutation

- **L267**: `passed, reason = gate_passed(gate_target, step.gate)` — `reason` is first assigned here when the initial gate check fails. (`passed=False`, so L268 short-circuits to L286.)
- **L341**: `reason = recheck_reason or reason` — only the *successful-remediation but failed-recheck* path mutates `reason`. The mutation is **monotonic**: it preserves the original `reason` when `recheck_reason` is empty.

**Critical M2 requirement:** the `except` clause must NOT clobber `reason`. If the cosmetic block raises mid-way (e.g. inside `gate_passed` at L317 after `recheck_reason` is unset), `reason` still holds the original L267 value, which is the correct failure cause to surface in the FAIL `StepResult`. The fix should simply log the exception and let `reason` carry through to L360 unchanged — DO NOT do `reason = str(exc)` or similar.

A safer pattern is to log the exception **separately** (so debugging info is captured) while letting the L344 `_log.info` continue to log the original `reason` to operators.

---

## 5. `# noqa: BLE001` precedent and ruff config

### 5a. Project ruff config (`pyproject.toml` L177-208)

- `select = ["E", "F", "I", "N", "W", "TID"]` (L186)
- `ignore = ["E501", "N818"]` (L187-195)
- **BLE is NOT in the `select` list** — so `except Exception` without `noqa` would NOT trip ruff. Adding `# noqa: BLE001` is therefore **defensive (style precedent)**, not strictly required by the linter.

### 5b. Existing precedent across the codebase

20 sites use `# noqa: BLE001` in `src/superclaude/cli/`. Representative examples:

- `cli/sprint/executor.py:1525`: `except Exception as _cp_exc:  # noqa: BLE001`
- `cli/sprint/executor.py:1586`: `except Exception as _sw_exc:  # noqa: BLE001 - must not abort`
- `cli/sprint/summarizer.py:534`: `except Exception as exc:  # noqa: BLE001 - narrative must never abort`
- `cli/sprint/summarizer.py:606`: `except Exception as exc:  # noqa: BLE001 - sprint-safety boundary`
- `cli/eval/commands.py:157`: `except Exception as exc:  # noqa: BLE001 - probe is a user-supplied callable`

The dominant convention is **`except Exception as exc:  # noqa: BLE001 - <one-line rationale>`**, where the rationale explains why a broad-except is justified at this boundary. M2 should follow this exact form. Suggested rationale: `# noqa: BLE001 - remediator is consumer-supplied; never abort pipeline on its failure`.

**`pipeline/executor.py` itself has zero `except Exception` clauses today** — `grep "except Exception" /config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py` returns empty. M2 will be the first such clause in this file; the style choice should match the project-wide pattern above.

---

## 6. Unguarded remediator-callable call sites

### 6a. In `pipeline/executor.py`

`grep "cosmetic_remediator(" /config/workspace/IronClaude/src/superclaude/cli/pipeline/executor.py`:

- **L309 only**: `remediated_ok, transforms = config.cosmetic_remediator(` — this is the single call site, and it is the target of the M2 wrap. No other unguarded invocations.

### 6b. In `cli/roadmap/executor.py` (the adapter)

The adapter at L3090-3120 wires the roadmap's `_roadmap_cosmetic_remediator` closure into `config.cosmetic_remediator`. The closure itself has **two unguarded callable invocations**:

- **L3107**: `classification = classify_gate_failure(content, gate_name, failure_reason, step_id=step_id)` — unguarded.
- **L3112**: `new_content, transforms = apply_cosmetic_remediations(content, classification)` — unguarded.

These live *inside* a function whose only existing `try/except` is the narrow `OSError` guard on `output_file.read_text(...)` at L3103-3106.

**Implication for the M2 scope decision:** even after the M1 fix to `cosmetic_remediator.py` hardens `classify_gate_failure`/`apply_cosmetic_remediations` internals, any new exception type leaking out of those functions would still propagate up to `_execute_single_step` and abort the pipeline. The M2 wrap at `pipeline/executor.py:L286-341` is therefore the **correct safety boundary** — it sits at the architectural seam between the generic pipeline (which must never crash) and the consumer-supplied remediator callable (which is "best effort"). The roadmap-side adapter does NOT need its own try/except as long as M2 catches at the call site in the generic executor.

### 6c. No other call sites

`grep -rn "cosmetic_remediator(" /config/workspace/IronClaude/src/superclaude/cli/` returns only the two sites above (L309 in `pipeline/executor.py`, L3096 closure definition in `roadmap/executor.py`). No tests or other modules invoke it directly.

---

## Summary (for the task-file author)

1. **Logger**: `_log = logging.getLogger("superclaude.pipeline.executor")` at L38 — use `_log.warning(...)` in the `except` clause.
2. **Wrap boundary**: `try:` at L286 indent (8 spaces), wrapping L286-341 (the entire `if (config.allow_cosmetic_remediation and ...)` block including the L341 `reason = recheck_reason or reason` mutation); `except Exception as exc:  # noqa: BLE001 - remediator is consumer-supplied; never abort pipeline on its failure` followed by a `_log.warning(...)` call; fall through (no `return`/`raise`) so execution lands at the existing L343 "Gate failed" path which already handles retry vs. exhausted-FAIL via the L356-363 `StepResult(status=StepStatus.FAIL, gate_failure_reason=reason, ...)` constructor.
3. **Preserve `reason`**: do NOT overwrite the `reason` variable in the `except` clause — the L267 value (or L341 mutation if it ran) must reach L360 unchanged so the operator sees the real gate failure, not the remediator-internal exception. Log the exception text separately via `_log.warning("Cosmetic remediation raised %s for step '%s'; falling through to FAIL", exc, step.id)`.
