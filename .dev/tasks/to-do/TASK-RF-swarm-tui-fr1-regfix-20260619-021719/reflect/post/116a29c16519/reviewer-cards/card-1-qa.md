## Reviewer 1 (QA, adversarial)

### Verdict

DEVIATIONS-FOUND — The four targeted deviations (REG-1, DRIFT-2/3/4) are correctly and non-vacuously fixed and the FR-5 masking holes are genuinely closed; the residual issues are a partially-vacuous PTY smoke (does not actually guard REG-1 cause 1) and an unmet literal KO-4 (repo-wide ruff fails on pre-existing out-of-scope debt). No blocking regression.

### Self-reported confidence

0.88

### Findings

| ID | Severity | Class | file:line evidence | Rationale |
|----|----------|-------|--------------------|-----------|
| F1 | MED | drift | `tests/swarm/test_run_tui_integration.py:299-371` | The PTY smoke `test_tui_real_pty_no_crash_under_concurrent_worker_stdout` PASSES even with the REG-1 cause-1 fix reverted (I removed `redirect_stdout/stderr=False` from `tui.py:224-225` and re-ran it green). It therefore does NOT guard against the redirect being re-armed — it asserts only "no Traceback + clean exit + race text present", and the #181 cross-thread Rich-Live crash is a non-deterministic native/Thread-1 NoneType render fault (cf. `src/superclaude/cli/sprint/tui.py:104-118`, which calls the same crash "suspected"/intermittent) that this harness does not deterministically trip. It still verifies real-PTY + concurrent worker stdout, so it is a partial guard, but its headline REG-1 assertion is effectively vacuous. |
| F2 | LOW | grounding-gap | `TASK…md:86` (KO-4) vs `uv run ruff check src/ tests/` → "Found 125 errors"; `ruff format --check src/ tests/` → "102 files would be reformatted" | KO-4 literally requires `ruff check src/ tests/` AND `ruff format --check src/ tests/` to pass; repo-wide they do NOT. Mitigant: none of the 7 task-modified files appear in either failure list (targeted ruff check + format on all 7 = clean), and the debt is demonstrably pre-existing/out-of-scope (e.g. `tests/troubleshoot/test_hardening_*`). CI's `ruff format --check src/ tests/` gate would be RED on this branch, but it would be RED on master too — this work adds no new breakage. Task Summary disclosed this honestly. |
| F3 | LOW | drift | `tests/swarm/test_inv012_tui_opt_in.py:673-693` | The hardened stdout-write detector flags only literal `print(` (by `ast.Name` id) and `sys.stdout`/`sys.stderr` attribute chains. It would NOT catch a future REG-1-class write via `os.write(1, …)`, an aliased `out = sys.stdout; out.write(…)`, an aliased `p = print; p(…)`, or a `logging` StreamHandler on stdout. Acceptable: the actual REG-1 was a plain `print(`, the audit is documented PER-FILE/non-transitive (register AUTH-note + test docstring 700-705), and these are exotic. Worth noting as a known ceiling. |
| F4 | LOW | none (verified-OK) | `src/superclaude/cli/swarm/commands.py:1961-1964` | FR-1 main-thread runtime guard is an `assert` (stripped under `python -O`) — already pre-classified AUTH-3. Not load-bearing because the structural single-writer topology (workers write only to the filesystem) + AST audit carry FR-1. No action needed; recorded for completeness. |

### Coverage (Key Objectives 1-4)

- **KO-1 (REG-1 source fix, frozen-signature-preserving):** YES. `tui.py:224-225` adds `redirect_stdout=False, redirect_stderr=False`; `parallel.py:100` adds `quiet: bool = False` class attr with `__init__(self, max_workers: int = 10)` UNCHANGED (`parallel.py:102`); `dispatch.py:425` flips `executor.quiet = True`. AST scan I ran confirms ZERO unguarded `print(` in `plan`/`execute`/`_execute_group`; those 3 methods are the COMPLETE `self.`-method surface (class has only `__init__`+3 methods, `execute`→`_execute_group` only), so scoping is not too narrow. Frozen-signature pin `test_frozen_signatures_unchanged` asserts `["self","max_workers"]` + default 10 (`test_run_tui_integration.py:837-845`).
- **KO-2 (FR-5 edges DRIFT-3 + DRIFT-4):** YES. DRIFT-3 readers wrapped in `try/except Exception: pass` with last-good retention and NO busy-spin `continue` (`commands.py:1947-1956`); the `is_alive()` break (`commands.py:1972`) is OUTSIDE the reader guard so a persistently-raising reader still terminates and reaches the `exc_box` re-raise. DRIFT-4 reordered so `if "e" in exc_box: raise` (`commands.py:1996-1997`) precedes `if interrupted: raise Exit(130)` (`commands.py:1998-2000`). All new guards scoped to `Exception`/`OSError`/`(JSONDecodeError, ValueError)` — never BaseException — so FR-6 KeyboardInterrupt propagates.
- **KO-3 (DRIFT-2 audit + PTY smoke + regression tests):** PARTIAL. AST audit extended + guard-aware + mutation-guarded (`test_stdout_write_detector_is_not_a_noop` PASS). DRIFT-3 and DRIFT-4 regression tests are GENUINELY non-vacuous (proven below). PTY smoke present but partially vacuous for REG-1 cause 1 (F1).
- **KO-4 (deterministic verification + POST reflect):** PARTIAL. `tests/swarm/` suite is GREEN (2234 passed, 26 skipped, I re-ran it). Targeted ruff check + format on all 7 modified files: clean. BUT repo-wide `ruff check`/`format --check src/ tests/` FAIL on pre-existing out-of-scope debt (F2) — the literal KO-4 text is unmet.

### Adversarial probes

1. **FR-5 masking holes (poll-loop):** Could not break it. Traced the loop with readers raising every iteration: `except Exception` (1952) keeps last-good and falls through to the `is_alive()` break (1972, outside the guard) + `time.sleep` — no busy-spin under `max_iterations=None`, loop terminates on worker death, post-loop `exc_box` re-raise reached. A non-KI BaseException from `tui_obj.update` escapes the inner `Exception` guard (1967), skips `except KeyboardInterrupt`, runs `finally` (stop+join), and STILL hits `if "e" in exc_box: raise` (1996) — so a co-occurring worker crash still dominates. `dispatch_thread.join()` has no timeout, but that is spec-mandated (FR-5: non-daemon + explicit join so the log is never truncated; per-worker timeout lives in the fan-out) — not a regression introduced here.
2. **Vacuous tests:** REFUTED vacuity for both FR-5 regression tests by reverting the fix in-tree. DRIFT-4: inverting the precedence → test FAILS with `exit=130 exception=SystemExit(130)` masking the worker `RuntimeError` (exactly the FR-5 failure mode). DRIFT-3: removing the reader `try/except` → test FAILS with the `ValueError` escaping and masking the worker `RuntimeError`. Both PASS post-fix. PTY smoke: BROKE its REG-1 guarantee — reverting `tui.py` redirect args left it GREEN (F1).
3. **DRIFT-2 audit completeness:** Partially broke it (F3) — `os.write`, aliased stdout, aliased `print`, `logging`-to-stdout are blind spots. Scoping parallel.py to 3 methods is NOT too narrow (verified the class has exactly those 3 + `__init__`, and the only `self.`-method call is `execute→_execute_group`).
4. **FR-6 / KeyboardInterrupt:** Could not break it. Every new guard is `Exception`/`OSError`/`(JSONDecodeError, ValueError)` — none catch BaseException. `_tail_events` (`commands.py:3083, 3108`) likewise. `test_fr6_stop_runs_on_all_three_exit_paths` PASSES — SIGINT-only still yields Exit(130) and stop() is idempotent.
5. **Frozen signature:** Could not break it. `parallel.py:102` is `def __init__(self, max_workers: int = 10):` verbatim; `quiet` is a class attr not a kwarg; `test_frozen_signatures_unchanged` pins names+default. Targeted ruff + full suite green.

### Citations

- `src/superclaude/cli/swarm/tui.py:218-229` (Live constructor with redirect_stdout/stderr=False)
- `src/superclaude/cli/sprint/tui.py:103-128` (sprint redirect rationale / crash described as suspected+intermittent)
- `src/superclaude/execution/parallel.py:100` (quiet class attr), `:102` (frozen __init__), `:105-146` (gated prints in plan/execute/_execute_group)
- `src/superclaude/cli/swarm/dispatch.py:425` (executor.quiet = True)
- `src/superclaude/cli/swarm/commands.py:1946-1977` (poll loop + DRIFT-3 reader guard), `:1996-2004` (DRIFT-4 reordered exc_box-before-interrupted), `:1961-1964` (FR-1 assert), `:1599-1604` + `:1633-1644` (FR-3 resume/detached guards), `:3083` + `:3108` (`_tail_events` except clauses)
- `tests/swarm/test_run_tui_integration.py:299-371` (PTY smoke), `:435-476` (DRIFT-3 test), `:479-514` (DRIFT-4 test), `:536` (FR-6 test), `:793-851` (frozen-signature pin)
- `tests/swarm/test_inv012_tui_opt_in.py:600-721` (extended visitor + per-file scope), `:724-757` (audit test)
- `tests/swarm/test_tail_events.py:46-124` (FR-4 tailer tests)
- `TASK-RF-swarm-tui-fr1-regfix-20260619-021719.md:83-86` (KO-1..KO-4), `:275` (KO-4 ruff-debt disclosure)
