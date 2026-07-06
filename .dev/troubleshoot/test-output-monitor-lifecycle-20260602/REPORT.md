# /sc:troubleshoot REPORT — test_output_monitor_lifecycle

- **Type:** test · **Tier reached:** 1 (grounded, single-domain, confirmed empirically) · **Status:** success
- **Confidence:** 0.92 · **Escalation:** none (single-domain test-isolation defect, root cause reproduced)
- **`test_is_wrong`: true** · **remediation target:** `tests/sprint/test_tui_monitor.py` (production code is correct)
- **Diagnosability:** sufficient (exact traceback + reproduced fix; no instrumentation needed)

## Summary

The failure is **not** what the surface symptoms suggested (phase-indexing bug / missing context-manager protocol). Both symptoms share **one root cause: a test-isolation leak.** The test patches `subprocess.Popen` at the **shared module object** (`patch("superclaude.cli.pipeline.process.subprocess.Popen")` mutates the global `subprocess.Popen`), but does **not** stub the phase-summarizer's narrative path. Because `claude` **is on PATH in this dev environment** (`/config/.local/bin/claude`), the summarizer's `invoke_sonnet()` runs a real `subprocess.run(...)` during phase 1's post-phase summary — which calls the **patched** `Popen` (the test's `_factory`), consuming an **extra** `_factory` invocation.

## Diagnosis (root cause, evidence-grounded)

The test's `_factory` increments `phase_counter` and indexes `config.phases[phase_counter-1]` (config has `num_phases=2`). Expected call sequence = 2 (one `start()` per phase). Actual:

1. Phase 1 `ClaudeProcess.start()` → `Popen` → `_factory` **call #1** (counter=1 → `phases[0]` ✓)
2. Phase 1 post-phase summary → `PhaseSummarizer.narrate()` → `invoke_sonnet()` → `subprocess.run()` → `with Popen(...) as p:` → **patched** `_factory` **call #2** (counter=2 → `phases[1]` ✓), returns `_Popen()` which lacks `__enter__` → `AttributeError` swallowed by `summarize()`'s `except Exception` → logged as the **"_Popen does not support the context manager protocol for phase 1"** warning
3. Phase 2 `ClaudeProcess.start()` → `_factory` **call #3** (counter=3 → `config.phases[2]`) → **`IndexError: list index out of range`** at `test_tui_monitor.py:215`

### Evidence
- `tests/sprint/test_tui_monitor.py:215` — `phase = config.phases[phase_counter[0] - 1]` (strict call-count indexing; the only one of the 8 fakes that indexes by call count → the only hard failure).
- Test patches `superclaude.cli.sprint.executor.shutil.which` but **not** `superclaude.cli.sprint.summarizer.shutil.which` — so the summarizer's PATH lookup hits the real `claude`.
- `src/superclaude/cli/sprint/summarizer.py:305` `invoke_sonnet` → `subprocess.run` (uses `with Popen(...)` internally); `summarizer.py:532-540` swallows the resulting exception as the observed warning.
- **`which claude` → `/config/.local/bin/claude`** — the environmental trigger is present (this is why it fails on the dev box but would pass in CI where `claude` is absent and `invoke_sonnet` returns early).
- **Reproduced fix:** adding `patch("superclaude.cli.sprint.summarizer.invoke_sonnet", return_value="")` to the test's `with`-block → **`1 passed`** (validated in a throwaway worktree, since discarded).

## Proposed Fix

**Primary (minimal, targeted):** stub the summarizer narrative in `test_output_monitor_lifecycle` so the daemon narrative subprocess never spawns and cannot consume a patched-`Popen` call:
```python
patch("superclaude.cli.sprint.summarizer.invoke_sonnet", return_value=""),
```
added to the test's `with (...)` context-manager block.

**Recommended hardening (broader, removes the latent leak from ALL sprint tests):** add an `autouse` fixture to `tests/sprint/conftest.py` that stubs `superclaude.cli.sprint.summarizer.invoke_sonnet` → `""` for the whole sprint suite. The narrative is always best-effort/swallowed, so stubbing it in tests is safe — and it eliminates the same latent leak (currently emitting swallowed context-manager warnings) from the other 7 fakes too.

## Alternatives considered
- *Make `_factory` tolerant of extra calls (clamp the index)* — **rejected**: masks the leak rather than fixing it; the extra call is a real test-isolation defect.
- *Patch `Popen` more narrowly instead of the shared module object* — valid but larger blast radius across all sprint tests; the narrative stub is the smaller correct fix.

## Risk + Rollback
Test-only change; zero production impact. If the conftest autouse fixture is chosen, the only behavioral change is that sprint tests never invoke the real `claude` narrative subprocess — which is the intended hermetic-test posture. Rollback = revert the test/conftest edit.
