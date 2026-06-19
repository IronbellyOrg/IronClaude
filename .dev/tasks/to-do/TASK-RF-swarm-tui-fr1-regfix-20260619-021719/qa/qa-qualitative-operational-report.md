# QA Report — Task Qualitative (Operational Correctness Lens)

**Topic:** swarm --tui FR-1 REG-1 + DRIFT-2/3/4 corrective remediation
**Date:** 2026-06-19
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A
**fix_authorization:** false (report-only)

---

## Overall Verdict: FAIL

One IMPORTANT finding (F-1): a likely execute-time failure where Step 3.1's
file-level unguarded-`print(` detector flags the 3 legitimate `__main__`
example-block prints in `parallel.py` (lines 331/334/336), making the
Step 3.6 full-suite run RED even after a correct Phase-1 fix — unless the
executor scopes the detector or guards those prints. The task gives the
executor latitude to resolve this ("the executor picks one and documents it")
but does NOT call out the collision, so a naive implementation fails.
Plus one MINOR (F-2): DRIFT-3 `continue`-without-sleep busy-spin /
non-termination edge under a permanently-raising reader.

All 6 pressure-test areas were verified against the LIVE target files. The
mechanical core of the task (REG-1 redirect disarm, frozen-sig-safe `quiet`
gating, DRIFT-3/DRIFT-4 poll-loop edits, regression-test seams, PTY smoke) is
operationally sound and code-accurate. The FAIL is driven by the one IMPORTANT
execute-time hazard per the no-leniency / all-severities-resolved rule.

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | REG-1 cause-1 fits live `Live(...)` constructor | none | PASS | tui.py:221-226 is the SOLE `Live(` (grep: 1 hit); has `console=`,`refresh_per_second=`,`screen=False`, NO `redirect_*`. Adding two kwargs fits cleanly. Research 01 cite (tui.py:218-228) faithful. |
| 2 | REG-1 cause-2 `quiet` class-attr is frozen-sig safe | none | PASS | parallel.py:100 `__init__(self, max_workers: int = 10)`. test_run_tui_integration.py:666-674 pins `inspect.signature(__init__)` params==`["self","max_workers"]` + default 10. A class attr does NOT appear in `__init__` signature → frozen-sig stays green. |
| 3 | All ParallelExecutor prints locatable + guardable | none | PASS | grep: 14 prints inside the class (110,111,164,165,176,177,183,191,196-200,225,232) at method-body / for-block indent — `if not self.quiet:` wraps fit. Matches research 01 table exactly. |
| 4 | dispatch.py flip applies to injected + fresh executor | none | PASS | dispatch.py:424 `executor = parallel_executor or ParallelExecutor(max_workers=workers_requested)`. Flip on next line covers both branches (Step 1.6 correct). `parallel_executor` param at :340. |
| 5 | DRIFT-3: readers genuinely outside the update try/except | none | PASS | commands.py:1944-1945 readers; FR-1 assert :1952; `try: tui_obj.update` :1956-1962. Readers ARE unguarded. read_state (state.py:178-196) raises JSONDecodeError/ValueError — premise TRUE. |
| 6 | DRIFT-3 guard still terminates + reaches exc_box re-raise | drift | FAIL→MINOR (F-2) | Suggested `continue` (research 02:56) skips the `is_alive()` break (1963) AND `time.sleep` (1968). A permanently-raising reader + production `max_iterations=None` ⇒ busy-spin / non-termination. Atomic writes make it unlikely; flagged but resolvable. |
| 7 | DRIFT-4: precedence inversion is real + reorder safe | none | PASS | commands.py:1984-1986 `Exit(130)` BEFORE :1990-1991 `exc_box` re-raise. Reorder keeps `result_box["v"]` rebind (1995) after both checks; SIGINT-only path still raises Exit(130) (no exc) → FR-6 green. |
| 8 | DRIFT-3 regression seam viable (3.4) | none | PASS | dispatch_wave1 patch seeds exc_box via worker `except BaseException` (commands.py:1917-1918) — proven by test_fr5 (:300). read_state is deferred-import (commands.py:1895) → patch SOURCE module (state_mod); Step 3.4 says exactly this. |
| 9 | DRIFT-4 regression seam viable (3.5) | none | PASS | FR-6 SIGINT test (:437-441) drives interrupted=True by patching TUI.update→KeyboardInterrupt (runs at 1957 before is_alive at 1963, deterministic). + dispatch_wave1→sentinel seeds exc_box. Both-set state reachable. |
| 10 | PTY smoke (3.3) viable + CI-bounded | none | PASS | Proven template at test_inv012_tui_opt_in.py:437-562: pty.openpty, subprocess.Popen(stdout=secondary_fd), 64KB drain cap + terminate + wait(timeout=5), win32 skipif. Cannot hang. Step 3.3 mirrors it; asserts crash-absence. |
| 11 | Audit detector guard-awareness (3.1) internally consistent | none | PASS | Step 1.5 guard shape `if not self.quiet:` ↔ Step 3.1 "reachable solely under if not self.quiet: is acceptable". `visit_If` detecting `not self.quiet` + guarded-recursion is implementable. |
| 12 | Audit detector vs `__main__` example prints (3.1↔3.6) | invented-content | FAIL→IMPORTANT (F-1) | parallel.py has 3 UNGUARDED prints OUTSIDE ParallelExecutor (331,334,336 in `if __name__`). A file-level unguarded-print detector (research 03:15 "within parallel.py") flags them → Step 3.6 RED. Task doesn't call out the collision. |
| 13 | Mutation guard (3.2) self-contained + viable | none | PASS | `_TuiSymbolVisitor` already proven callable on synthetic source via ast.parse (existing mutation guard :703-712). Step 3.2 synthetic `print('x')`/`sys.stdout.write('x')` mirrors it; self-contained. |
| 14 | Injected-executor tests won't break on quiet flip | none | PASS | grep: test_imm3_parallel.py + test_dispatch.py have ZERO capsys/capfd/readouterr → no stdout-capture assertions. Flip to quiet=True is safe. Research 01:90 concern resolved. |
| 15 | Tooling + suite collection (UV/ruff/pytest) | none | PASS | `uv run ruff --version` ok; `tests/swarm/` collects 2256 tests. UV-only commands in Steps 1.7/2.3/3.6/4.1/4.2 executable. VIRTUAL_ENV warning is benign. |
| 16 | Step 4.5 `--fix` ordering hazard | none | PASS | `--fix` mutates tree AFTER Step 4.4 summary, but 4.4 documents WORK DONE (not a tree-frozen artifact) and POST reflect is intentionally penultimate (only 4.6 status flip follows). No verification is invalidated. Benign. |
| 17 | click.exceptions.Exit / FR-6 surface intact | none | PASS | commands.py:43 `import click`; Exit(130) at 1986. Reorder preserves Exit(130) on SIGINT-only. result_box rebind at 1995. |

---

## Summary

- Checks passed: 15 / 17
- Checks failed: 2 (1 IMPORTANT, 1 MINOR)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F-1 | IMPORTANT | Step 3.1 (test_inv012_tui_opt_in.py detector) ↔ src/superclaude/execution/parallel.py:331,334,336 | The DRIFT-2 stdout-write detector, per Step 3.1 + research 03:15, flags UNGUARDED `print(` "within parallel.py" at file level. But parallel.py has 3 legitimate unguarded prints OUTSIDE `ParallelExecutor` — in the `if __name__ == "__main__":` example block (lines 331,334,336) plus `example_*` convenience functions. A naive file-level detector flags these → `test_worker_surfaces_have_zero_tui_reachability` FAILS even after a 100%-correct Phase-1 fix → Step 3.6 full-suite RED. Step 1.5 deliberately leaves these untouched ("prints OUTSIDE ParallelExecutor are left untouched"), creating a direct 3.1↔1.5/3.6 contradiction the task never reconciles. | Scope the Step 3.1 detector to the worker-surface CALLABLES only (ParallelExecutor methods + dispatch.py worker functions), NOT module-level/`__main__`/example-function prints; OR explicitly exempt the `if __name__ == "__main__"` block + `example_*`/`parallel_file_operations` convenience functions. Add this exemption instruction to Step 3.1 (and note it in Step 1.5) so the executor does not ship a detector that flags the example prints. The "executor picks one and documents it" latitude is insufficient because the collision is not surfaced. |
| F-2 | MINOR | Step 2.1 (commands.py poll loop ~1943-1968) | DRIFT-3's suggested `continue`-on-reader-error (research 02:55-56) skips the `if not dispatch_thread.is_alive(): break` check (1963) AND the `time.sleep(_TUI_POLL_INTERVAL_SEC)` (1968). A reader that raises on EVERY iteration (e.g. worker wrote permanently shape-invalid JSON then crashed) combined with production `max_iterations=None` yields an unbounded busy-spin that never reaches the post-loop exc_box re-raise — the opposite of the FR-5 intent. Atomic `write_state` (os.replace) makes torn reads transient, so this is narrow, and research 02:58 already warns "must guarantee the loop still terminates on worker death." | Step 2.1 should instruct: on a reader exception, keep last-good snapshot and FALL THROUGH to the existing liveness/sleep tail (no bare `continue`) — OR re-check `dispatch_thread.is_alive()` (break if dead) and `time.sleep` before `continue`-ing. Falling through is the safer shape and is the recommended fix. |

## Actions Taken

None — `fix_authorization: false`. All findings documented for the executor / orchestrator.

## Five Adversarial Axes — application notes

- **AX-1 drift:** Fired on check #6 (DRIFT-3 termination): the suggested `continue` quietly drops the loop's own termination/throttle guarantees — a behavioral drift from the FR-5 intent. MINOR.
- **AX-2 contradictions:** F-1 is fundamentally a contradiction (AX-2 also load-bearing) between Step 1.5 ("leave non-class prints untouched") and Step 3.1's file-level detector ("flag unguarded prints in parallel.py"). Recorded under AX-5 invented-content because the deeper root is the detector asserting a property (zero unguarded file-level prints) that the source does not and is not meant to satisfy; the AX-2 contradiction is the surface symptom. Either annotation is defensible; AX-5 chosen as most-specific to the failure mechanism.
- **AX-3 omissions:** No QA_GATE/VALIDATION/TESTING requirement omitted; all 4 Key Objectives map to checklist items. The DRIFT-1/NEC-1 out-of-scope items are correctly notes-only.
- **AX-4 weakened-criteria:** None — acceptance criteria (ruff check + ruff format --check + full tests/swarm/ + frozen-sig + POST reflect exit 0) are unconditional and observable; no permissive "or"/"may" softening detected.
- **AX-5 invented-content:** F-1. The detector (as specified) would assert a structural property unguarded-prints-absent across the whole of parallel.py that the file's own `__main__`/example prints violate by design — effectively inventing a constraint the source was never written to meet.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa B2 self-containment PASS (22/22) — did NOT re-verify per-item self-containment / anchor-uniqueness phrasing.
- Relied on rf-qa Phase-structure PASS — did NOT re-verify section numbering, frontmatter shape, phase ordering, anti-orphaning, POST-reflect-penultimate, or frozen-sig tripwire presence.
- Relied on rf-qa Research-alignment PASS (10/10) — did NOT re-audit the finding→item mapping count.

**(b) Independent semantic checks where structural PASS was INSUFFICIENT (≥1 required, INV-019):**
- **Frozen-signature MECHANISM correctness** (not just "tripwire present"): rf-qa confirmed the frozen-sig tripwire exists; I independently Read test_run_tui_integration.py:666-674 AND parallel.py:100 to verify that a CLASS-ATTRIBUTE `quiet: bool = False` genuinely does not alter `inspect.signature(ParallelExecutor.__init__)` — i.e. the proposed mechanism actually survives the pin. Structural PASS could not establish this; it required reading both the test assertion and the constructor.
- **Detector ↔ source collision (F-1)**: rf-qa's "research faithfully mapped" PASS does not catch that the faithfully-mapped detector, applied to the REAL parallel.py, flags 3 legitimate `__main__` example prints (grep of parallel.py:331/334/336 outside the class). This required reading the actual source file's full print inventory + scope, not the task↔research alignment.
- **DRIFT-3 termination edge (F-2)**: required tracing the LIVE poll-loop control flow (commands.py:1956-1968) to see that `continue` skips both the `is_alive` break and the `time.sleep` — a runtime-path property invisible to structural/anchor checks.

## Self-Audit (Confidence Gate)

1. **Factual claims independently verified against source:** 17 checklist items, each tied to a tool-verified anchor (line numbers, grep counts, signature pins, import idioms).
2. **Files read to verify claims:** the task file (full); src/superclaude/cli/swarm/tui.py (Live constructor); src/superclaude/execution/parallel.py (full — all 17 prints, __init__, class scope); src/superclaude/cli/swarm/dispatch.py (executor bind region); src/superclaude/cli/swarm/commands.py (poll loop 1870-2003, deferred-import map); src/superclaude/cli/swarm/state.py (full — read_state contract); tests/swarm/test_inv012_tui_opt_in.py (visitor 590-713 + PTY template 433-562); tests/swarm/test_run_tui_integration.py (header, FR-5 290-344, FR-6 365-451, FR-7 458-483, frozen-sig 600-681); all 3 research files (01/02/03 full). Plus 4 Bash grep/collect verifications.
3. **Why trust the FAIL:** The FAIL is not speculative — F-1 is backed by a concrete grep showing 3 unguarded prints at parallel.py:331/334/336 outside ParallelExecutor that a file-level detector (research 03:15 wording) flags; F-2 is backed by reading the exact loop tail (1963-1968) the `continue` skips. I traced both runtime paths, not just the task prose.
4. **Web research:** None performed — this review is entirely local-file-bound. (No Tavily/fallback needed.)

- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep/Bash: 4 | Glob: 0 (Read+Grep ≥ 17 checklist items — engagement floor met)
- UNCHECKED items: none
- UNVERIFIABLE items: none

## Recommendations (before execution)

1. **Resolve F-1 (IMPORTANT):** Amend Step 3.1 to scope the unguarded-stdout detector to worker-surface CALLABLES (ParallelExecutor methods + dispatch.py worker fns), explicitly exempting `if __name__ == "__main__"` and the `example_*`/`parallel_file_operations` convenience functions — OR have Step 1.5 additionally note these are exempt so the executor does not let the detector flag them. Without this, Step 3.6 goes RED on an otherwise-correct fix.
2. **Resolve F-2 (MINOR):** Amend Step 2.1 to FALL THROUGH to the existing `is_alive()`/`time.sleep` tail on a reader exception (keep last-good snapshot, no bare `continue`) so a permanently-raising reader cannot busy-spin or bypass the exc_box re-raise.
3. After both amendments, the task is operationally GREEN: every other mechanism (REG-1 redirect disarm, frozen-sig-safe quiet gating, dispatch flip, DRIFT-4 reorder, all 4 regression/PTY/mutation seams, injected-executor safety) is verified correct against the live tree.

## QA Complete

VERDICT: FAIL

Unfixable-without-task-amendment issues:
- F-1 (IMPORTANT): Step 3.1 detector flags the 3 legitimate `__main__` example
  prints in parallel.py (331/334/336) → Step 3.6 RED unless the detector is
  scoped to worker-surface callables or those prints are exempted.
- F-2 (MINOR): DRIFT-3 `continue`-on-reader-error skips the loop's
  is_alive break + time.sleep → busy-spin / non-termination edge under a
  permanently-raising reader; fall-through is the safer shape.
