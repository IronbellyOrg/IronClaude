## Reviewer 2 (analyzer, adversarial)

### Verdict

**CLEAN (with 1 LOW test-robustness observation; 0 blocking).** The REG-1 cross-thread
`Live`-render crash class is fully and structurally killed. Both co-causes are remediated:
(a) `Live(...)` is now constructed with `redirect_stdout=False, redirect_stderr=False`
(tui.py:226-227), and (b) every `ParallelExecutor` worker-surface `print()` is gated behind
`if not self.quiet:` (parallel.py:112-114,167-169,180-184,190-191,199-200,205-210,235-236,
243-244) with `executor.quiet = True` flipped at the single swarm dispatch call site
(dispatch.py:425). The FR-1 single-writer property is now a *structural* invariant: the full
transitive worker call graph (dispatch.py, logging_.py, state.py, transports/) contains ZERO
`print`/`sys.stdout`/`sys.stderr`/`Console`/`.write` writes — workers' only output channel is
the filesystem Logger. DRIFT-3 and DRIFT-4 are both correctly fixed; the exc_box re-raise is
unconditionally ordered before the SIGINT Exit(130). The frozen `__init__(self, max_workers=10)`
signature is preserved verbatim. I attempted to break each FR via live stress and could not.

### Self-reported confidence

0.9

### Findings

| ID | Severity | Deviation class | file:line | Rationale |
|----|----------|-----------------|-----------|-----------|
| A2-F1 | LOW | test-robustness (not a code deviation; no FR impact) | tests/swarm/test_run_tui_integration.py:435-476 | `test_drift3_reader_error_does_not_mask_worker_crash` failed EXACTLY ONCE on the first invocation of a mixed 6-test selection, with `result.exception == ValueError('boom-DRIFT3-reader')`. I could not reproduce it across 40× isolated runs, 40× the identical 6-selection, 25× PTY→DRIFT3 ordered, and 3× full-suite (2234 passed each). The production control flow makes the asserted masking IMPOSSIBLE — `read_state`'s `ValueError` is caught by the `except Exception: pass` guard at commands.py:1952, so `exc_box['e']` (the worker sentinel) always dominates at 1996-1997. The one-off was almost certainly a first-run import/bytecode-compile timing artifact in the worker-vs-main interleave, NOT a hole in the fix. Recommend (optional, follow-up): the DRIFT-3 test pins `_TUI_POLL_INTERVAL_SEC`/`_TUI_POLL_MAX_ITERATIONS` like the PTY/FR-4 tests do (it currently leaves the production 0.5s/None defaults), to make the worker-death-before-first-poll timing deterministic. Does NOT block — the fix is sound and the suite is green. |

No HIGH/MED findings. No regression. No unauthorized drift.

### Coverage

| FR / KO | Spec acceptance | Implementation | Test | Status |
|---------|-----------------|----------------|------|--------|
| FR-1 (single-writer Console) | tui/Live/Console reachable from zero worker fns; main-thread-only update | tui.py:226-227 redirect disarmed; parallel.py gated prints; dispatch.py:425 quiet flip; commands.py:1961 `get_ident()` main-thread assert | test_inv012::test_worker_surfaces_have_zero_tui_reachability (now flags stdout writes); test_stdout_write_detector_is_not_a_noop (mutation guard); test_fr1_tui_update_only_runs_on_main_thread; test_tui_real_pty_no_crash_under_concurrent_worker_stdout (real PTY, concurrent worker stdout, asserts no Traceback) | COVERED |
| FR-2 (INV-012 gate + non-TUI no-regression) | non-TTY → synchronous path, zero ANSI | commands.py:1883-1892 `_tui_active` gate + byte-identical fallback | test_fr2_tui_is_noop_on_non_tty; test_gate_* | COVERED |
| FR-5 (worker crash never masked) | reader exception + concurrent SIGINT must not mask | DRIFT-3: commands.py:1947-1956 reader guard (no busy-spin continue, last-good snapshot seeded 1930-1932); DRIFT-4: commands.py:1996-2000 exc_box re-raise BEFORE Exit(130) | test_drift3_reader_error_does_not_mask_worker_crash; test_drift4_sigint_does_not_mask_worker_crash; test_fr5_worker_exception_reraised_unmasked_after_stop | COVERED |
| FR-6 (idempotent teardown + SIGINT) | stop() on all 3 exit paths; SIGINT-only → Exit(130) | commands.py:1985-1992 finally(stop+join); 1998-2000 Exit(130) only when exc_box empty; all new guards scoped to `Exception` so KeyboardInterrupt (BaseException) propagates | test_fr6_stop_runs_on_all_three_exit_paths (asserts exit_code==130 on SIGINT-only) | COVERED — NEC-1 (Exit 130) preserved, not regressed |
| KO-1 (REG-1 source fix, frozen sig) | redirect disarm + quiet gate w/o touching `__init__` | tui.py + parallel.py + dispatch.py as above; parallel.py:100 `quiet` is a CLASS attribute, 102 `__init__(self, max_workers=10)` unchanged | test_frozen_signatures_unchanged (asserts init params == [self, max_workers], default 10) | COVERED |
| KO-2 (FR-5 edges) | DRIFT-3+DRIFT-4 | see FR-5 row | see FR-5 row | COVERED |
| KO-3 (DRIFT-2 audit + PTY) | flag unguarded stdout writes, scoped, mutation guard, PTY smoke | test_inv012 `_TuiSymbolVisitor` extended (visit_Call/visit_Attribute/visit_If quiet-guard awareness), scoped to ParallelExecutor methods for parallel.py | test_stdout_write_detector_is_not_a_noop + PTY smoke | COVERED |
| KO-4 (deterministic verify + POST reflect) | ruff + tests/swarm green | targeted ruff check + format clean on all 7 modified files | 2234 passed, 26 skipped (tmux) | COVERED |

### Central-tension classification

**Verdict: AUTHORIZED / NECESSARY deviation — NOT an unauthorized Drift or Regression.**

The original spec frontmatter (merged-requirements.md:19-22) lists `dispatch.py` and
`parallel.py` under `unchanged_by_design` (C3/AC-004/NFR-001). This regfix modified both
(parallel.py +42 quiet-gating, dispatch.py +1 quiet flip). I classify this as authorized for
three converging reasons, all evidence-verified:

1. **A later authorizing artifact explicitly mandates it.** The regfix TASKLIST Key Objective 1
   (task file lines 83, 117-119) directly instructs touching parallel.py (quiet class-attribute
   + gated prints) and dispatch.py (executor.quiet flip). The tasklist post-dates and supersedes
   the original spec's "untouched" assumption for the corrective scope.

2. **It was forced by the REG-1 discovery.** The parent deviation register
   (deviation-register.yaml:44-50) records that disabling the `Live` redirect ALONE is
   insufficient — un-silenced worker prints still corrupt the dashboard (the PR#181 "medium").
   The spec's own rationale (merged-requirements.md:40-47) anticipated this: the "untouched"
   approach assumed worker output never reaches the Console, which the armed-redirect default
   falsified. Modifying the two files is the necessary remediation of a HIGH regression, not
   scope creep.

3. **The invariant that actually matters is preserved.** The load-bearing frozen invariant is
   `ParallelExecutor.__init__(self, max_workers=10)`, pinned by
   test_frozen_signatures_unchanged (test_run_tui_integration.py:837-844, asserting
   `init_names == ["self", "max_workers"]` and `max_workers` default == 10). VERIFIED against
   live parallel.py:102 — `def __init__(self, max_workers: int = 10):` is byte-unchanged. The
   silencing is a CLASS attribute `quiet: bool = False` (parallel.py:100), NOT a constructor
   kwarg. The `dispatch_wave1` signature is likewise untouched (git diff is a single
   `executor.quiet = True` instance-attribute assignment at dispatch.py:425, no signature
   change). Default `quiet=False` preserves byte-identical behavior for all non-swarm callers.

This is the textbook shape of a Necessary deviation: a frozen-by-design surface had to change to
kill a non-negotiable-gate regression, the change is minimal, the spec's *true* frozen contract
(the public signatures) is intact, and a later authorizing artifact sanctioned it.

### Adversarial probes

1. **Residual cross-thread write paths — REFUTED (FR-1 is structural).** Grepped the full
   transitive worker call graph for `print(`/`sys.stdout`/`sys.stderr`/`Console`/`.write(`:
   - dispatch.py: ZERO matches (entire file).
   - logging_.py: ZERO. state.py: ZERO. transports/{stub,openai_compat,__init__}.py: ZERO.
   - `_run_worker` (dispatch.py:279-333): only `logger.log_event(...)` → filesystem.
   - parallel.py: every `ParallelExecutor` print is now under `if not self.quiet:`; module-level
     example fns + `__main__` block still print but are NOT reachable from dispatch_wave1 (and the
     audit correctly exempts them). No other path writes to the Console while `Live` is active.

2. **redirect disarm correctness — REFUTED (correctly disarmed).** `redirect_stdout=False,
   redirect_stderr=False` are on the ACTUAL dashboard `Live` (tui.py:221-228, the only `Live(`
   in the file — sole construction site in `start()`). Only one `Console(` (tui.py:207, default
   ctor in `TUI.__init__`); no other `Live`/`Console` re-arms a redirect. `should_enable_tui`
   (tui.py:74-95) + the `_tui_active` gate (commands.py:1883) correctly route non-TTY to the
   synchronous no-thread path (verified by test_fr2_tui_is_noop_on_non_tty, green).

3. **DRIFT-4 precedence — REFUTED (unconditional, no early-return).** Read commands.py:1985-2004.
   After the `finally` (stop+join, 1985-1992), the post-loop block is linear: `if "e" in exc_box:
   raise exc_box["e"]` (1996-1997) executes BEFORE `if interrupted: raise Exit(130)` (1998-2000).
   There is NO `return`, `break`, or early exit between the loop and the re-raise. A worker crash
   therefore dominates a concurrent SIGINT unconditionally. SIGINT-only (empty exc_box) still
   reaches Exit(130) — confirmed by test_fr6...::(c) asserting exit_code==130 (line 614, green).
   `worker_results = result_box["v"]` (2004) only runs when both raises are skipped (no-exception
   path), preserving the synchronous-path contract.

4. **Spec FR coverage — REFUTED (no orphan FR).** Every FR-1/2/5/6 acceptance maps to real code
   AND a real test (see Coverage table). The DRIFT-2 audit now checks the RIGHT invariant
   (unguarded stdout writes), with guard-awareness (visit_If tracks `if not self.quiet:` depth,
   test_inv012:660-671) and a mutation guard proving it is not a no-op (test_inv012:788-821, which
   I ran green in isolation). The PTY smoke genuinely exercises the TTY-only race by injecting a
   concurrent worker-thread `print` over a real `os.openpty()` fd (test:308-317) and asserting
   `"Traceback" not in output` (test:368) — the exact gap a non-TTY CliRunner could not reach.

5. **DRIFT-1 / NEC-1 scope — CONFIRMED genuinely deferred, not silently actioned/regressed.**
   - DRIFT-1: the eager `from ...tui import TUI, should_enable_tui` is STILL at commands.py:1881
     (TUI used only in the `else` branch at 1928). The task explicitly lists it out-of-scope
     (task file line 131). Not fixed, not worsened — correctly deferred.
   - NEC-1: SIGINT-only still surfaces as deterministic Exit(130) (commands.py:1998-2000),
     preserved verbatim and still asserted green by test_fr6...::(c). DRIFT-4's reorder does NOT
     regress it because the precedence only re-raises exc_box when non-empty. Correctly preserved.

### Citations

- src/superclaude/cli/swarm/tui.py:221-228 — `Live(...)` with `redirect_stdout=False, redirect_stderr=False` (only Live ctor in file)
- src/superclaude/cli/swarm/tui.py:207 — sole `Console()` (default ctor, no redirect re-arm)
- src/superclaude/cli/swarm/tui.py:74-95 — `should_enable_tui` gate
- src/superclaude/execution/parallel.py:100 — `quiet: bool = False` CLASS attribute
- src/superclaude/execution/parallel.py:102 — `def __init__(self, max_workers: int = 10):` (frozen, unchanged)
- src/superclaude/execution/parallel.py:112-114,167-169,180-184,190-191,199-200,205-210,235-236,243-244 — all prints gated by `if not self.quiet:`
- src/superclaude/cli/swarm/dispatch.py:425 — `executor.quiet = True` instance flip (single swarm dispatch site)
- src/superclaude/cli/swarm/dispatch.py:279-333 — `_run_worker` writes only via `logger.log_event` (no Console)
- src/superclaude/cli/swarm/dispatch.py — entire file has ZERO print/stdout/stderr/Console/.write
- src/superclaude/cli/swarm/commands.py:1881 — eager TUI import (DRIFT-1 deferred)
- src/superclaude/cli/swarm/commands.py:1883-1892 — `_tui_active` gate + synchronous fallback
- src/superclaude/cli/swarm/commands.py:1930-1932 — last-good snapshot seeded before loop (state=None/events=[]/offset=0)
- src/superclaude/cli/swarm/commands.py:1947-1956 — DRIFT-3 reader guard (try/except Exception: pass, no busy-spin continue)
- src/superclaude/cli/swarm/commands.py:1961-1964 — FR-1 main-thread get_ident() assert
- src/superclaude/cli/swarm/commands.py:1965-1971 — render-glitch latch (except Exception, KeyboardInterrupt propagates)
- src/superclaude/cli/swarm/commands.py:1985-1992 — finally: stop() then join()
- src/superclaude/cli/swarm/commands.py:1996-2000 — DRIFT-4 fix: exc_box re-raise BEFORE Exit(130), no early-return between
- src/superclaude/cli/swarm/commands.py:3050-3112 — `_tail_events` (byte-offset, exactly-once, partial-line tolerant; returns list, no stdout)
- src/superclaude/cli/swarm/logging_.py — ZERO Console/stdout writes
- src/superclaude/cli/swarm/state.py — ZERO Console/stdout writes
- src/superclaude/cli/swarm/transports/{stub,openai_compat,__init__}.py — ZERO Console/stdout writes
- tests/swarm/test_inv012_tui_opt_in.py:599-693 — extended `_TuiSymbolVisitor` (visit_Call/visit_Attribute/visit_If quiet-guard awareness)
- tests/swarm/test_inv012_tui_opt_in.py:696-721 — `_scan_tui_symbols` scopes parallel.py to ParallelExecutor methods
- tests/swarm/test_inv012_tui_opt_in.py:724-785 — worker-surfaces audit (import/name/stdout hits + vacuity + mutation guards)
- tests/swarm/test_inv012_tui_opt_in.py:788-821 — `test_stdout_write_detector_is_not_a_noop` (guarded vs unguarded)
- tests/swarm/test_run_tui_integration.py:295-371 — real-PTY concurrent-worker-stdout smoke
- tests/swarm/test_run_tui_integration.py:435-476 — DRIFT-3 regression (1× flake, 0/95+ reproductions; see A2-F1)
- tests/swarm/test_run_tui_integration.py:479-514 — DRIFT-4 regression (worker crash dominates SIGINT, exit != 130)
- tests/swarm/test_run_tui_integration.py:597-621 — FR-6 SIGINT-only asserts exit_code == 130 (NEC-1 preserved)
- tests/swarm/test_run_tui_integration.py:793-850 — `test_frozen_signatures_unchanged` (init params == [self, max_workers], default 10)
- Live run evidence: `uv run pytest tests/swarm/` → 2234 passed, 26 skipped (3× consecutive); targeted ruff check + format clean on all 7 modified files
