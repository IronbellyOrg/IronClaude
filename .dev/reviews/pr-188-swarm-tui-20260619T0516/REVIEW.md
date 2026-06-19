# Code Review: PR #188 — swarm `--tui` wiring + FR-1 regression fix

**Target**: PR #188 (diff `origin/master...HEAD`, code surfaces only)
**Reviewer**: /sc:auggie-review (depth=quick fallback, auggie 0.29.0, model claude-sonnet-4-6)
**Generated**: 2026-06-19
**Base ↔ Head**: master ↔ feat/swarm-tui-wiring-fr1-regfix
**Stats**: 7 code/test files, 1894 diff lines, 13 raw findings (10 + 3 cross-cutting); 1 promoted to fix, rest graded by-design / deferred / test-nit

---

## Summary

The change is sound and well-tested. The single material finding the fallback surfaced — and that the prior deep reflect (3 reviewers) missed — is a **residual FR-5 masking gap**: a Rich `Live` startup exception can bypass the worker-crash re-raise, the same non-negotiable invariant DRIFT-3/DRIFT-4 fixed. That is being remediated in this round (F1). Everything else is either by-design per the task spec, the deliberately-deferred DRIFT-1, or low test-quality nits already recorded by reflect (D1/D2/D3).

## Findings

### 🟠 High / Medium (fix this round)

#### F1. TUI init/start exception bypasses the worker-crash re-raise (FR-5 masking)
- **File**: `src/superclaude/cli/swarm/commands.py:1927-2000`
- **Category**: error-handling / correctness · **Source**: auggie (finding #3) · **Confidence**: high (code-verified)
- **Evidence**: `tui_obj = TUI(); tui_obj.start()` run inside a `try` whose only handler is `except KeyboardInterrupt`. A non-KeyboardInterrupt exception from `Live` startup propagates past the `finally` (which runs `tui_obj.stop()` + `dispatch_thread.join()`) and skips `if "e" in exc_box: raise exc_box["e"]`.
- **Why this matters**: If the dispatch worker crashed (its exception captured in `exc_box`) **and** `tui_obj.start()` raised, the TUI-side error masks the worker crash. FR-5 ("a worker crash must NEVER be masked") is non-negotiable — this is the same class as DRIFT-3 (reader exc) and DRIFT-4 (SIGINT), left uncovered on the TUI-init/start path.
- **Recommendation**: Add `except Exception as exc: tui_exc = exc` to the loop's try; in the post-`finally` block keep the precedence **worker crash → SIGINT → TUI-side error** so the worker exception still dominates and the TUI error is surfaced (never swallowed) only when no worker crash/interrupt occurred. Add a regression test.

### 🟡 Medium → regraded by-design / deferred (report only)

#### F2. `executor.quiet = True` applied on ALL swarm dispatch paths, not just TUI (auggie #2 + CC1/CC2)
- **File**: `src/superclaude/cli/swarm/dispatch.py:425` · regraded **LOW / by-design**.
- The task spec (Step 1.6) directs the unconditional flip; FR-1 intent is "swarm workers emit only to the filesystem" on every path, so the decorative `ParallelExecutor` banner prints are correctly silenced regardless of `--tui`. Full suite (incl. `test_fr2_tui_is_noop_on_non_tty`) green. Behavior note, not a defect.

#### F3. Eager `from ...tui import TUI` on every fresh `run_cmd` (auggie #1 / CC1)
- **File**: `src/superclaude/cli/swarm/commands.py:1881` · regraded **deferred** — this is **DRIFT-1**, explicitly documented out-of-scope in the task and recommended as a separate follow-up. Not actioned here.

#### F4. `dispatch_thread.join()` has no timeout (auggie #4)
- **File**: `src/superclaude/cli/swarm/commands.py:1992` · regraded **LOW / by-design**. The non-daemon worker + unbounded `join()` is the deliberate FR-5 anti-truncation choice (the execution log must flush); the worker is bounded by its own `WorkerSpec` timeout/retry policy. A `join()` timeout would risk truncation.

### 🟢 Low / Nits (report only)

- **F5** `assert threading.get_ident() == main_ident` is a no-op under `python -O` (`commands.py:1961`). Real hardening gap; the redirect-disarm + AST audit carry the actual FR-1 protection. Cheap follow-up: convert to an explicit `raise`. (auggie #5)
- **F6** `--tui` on a TTY without `--output` silently no-ops (`commands.py:1883`) — the documented G2 design decision; could add a one-line operator notice. (auggie #6)
- **F7** `quiet` class-attr + per-instance flip is "untested directly" (`parallel.py:100`) — the frozen-signature-preserving mechanism the task required; covered indirectly by the FR-1 audit + full suite. (auggie #7)
- **F8** FR-4 render-ceiling test is timing-sensitive (`test_run_tui_integration.py`); overlaps reflect **D2**. (auggie #8)
- **F9** `_TuiSymbolVisitor` quiet-guard recognizes only the exact `if not self.quiet:` shape; overlaps reflect **D3**. (auggie #9)
- **F10** render-glitch latch `except Exception: pass` on `tui_obj.update` swallows Rich errors silently (`commands.py:1965`) — intended FR-1 render-glitch latch; could log at debug. (auggie #10)
- **CC3** No unforced real-TUI concurrent-dispatch test; the real-PTY smoke partially covers this; overlaps reflect **D1**. 

## Audit

- Auggie chunks: 1 (retried once: max-turns 8 → 16; the 8-turn pass returned empty).
- Findings dropped during grounding: 0 (all 13 ground in real file:line).
- Security: none (diff touches no auth/secret/trust paths — confirmed).
- Remediation this round (clamp=1): **F1 only** (verified FR-5 defect) + regression test.
