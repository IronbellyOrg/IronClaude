# QA Report — Phase 2 Fix Verification (Content/Semantics)

**Topic:** troubleshoot-hardening-evals — git-replay helper Phase 2 fixes (P2-1, P2-2, P2-3)
**Date:** 2026-06-12
**Phase:** fix-cycle (content/semantics fix-VERIFICATION; report-only)
**Fix cycle:** verification of cycle 1 (3 findings from seam-teardown lens)
**Fix authorization:** false (modified NO file)

---

## Overall Verdict: PASS

All 3 Phase 2 findings are genuinely fixed (not cosmetic), the collision boundary is intact,
the no-caret (G1) rule holds, the unit-test mock seam is preserved, and the tests still assert
real behavior. 6 of 6 tests pass (4 unit + 2 integration against real git, not skipped).

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | P2-1 teardown robustness is genuine, not cosmetic | PASS | `git_replay.py:148-178` — each teardown `_subprocess.run` wrapped in its OWN `try/except (_subprocess.TimeoutExpired, FileNotFoundError, OSError): pass` (155-165 remove, 168-178 prune); `rmtree` between them uses `ignore_errors=True` (166). No raise can escape `finally`. |
| 2 | A timeout/missing-git in `remove` cannot prevent `prune` nor mask the body exception | PASS | remove's except clause swallows the 3 raising types (164-165) → control falls through to `rmtree` (166) → `prune` (169) unconditionally. `finally` never re-raises ⇒ body exception propagates unmasked. Unit test asserts `excinfo.value is sentinel` (`test_git_replay_unit.py:49`) AND both remove+prune fired (52-57). |
| 3 | P2-1 mirror claim accurate (matches process.py seam) | PASS | `src/superclaude/cli/sprint/process.py:392` catches exactly `(FileNotFoundError, _subprocess.TimeoutExpired, OSError)` — the same triple the fix uses. Claim in comment (`git_replay.py:154`) is truthful. |
| 4 | P2-2 anchoring does NOT break the unit mock seam (argv-slice shape) | PASS | `cwd=anchor` passed as a KEYWORD arg (145, 163, 176); `_argvs` reads `call.args[0]` (positional only, `test_git_replay_unit.py:21`). Slices `a[:4]/a[-1]/a[-2]/a[:3]` operate on the unchanged argv list. NO `-C` flag in any argv (grep: none). |
| 5 | P2-2 `_repo_anchor` stays under the mock seam | PASS | `_repo_anchor()` routes through `_subprocess.run` (`git_replay.py:82`), not `-C`. On the mock path `stdout=""` → returns `None` → `cwd=None` (inherit CWD = prior behavior). Extra `rev-parse` call does not match any argv filter prefix, so `add_calls len==1` and remove/prune filters stay correct. |
| 6 | P2-2 real-git isolation works end-to-end | PASS | Integration tests run REAL git (not skipped — full-depth clone): `test_backtest_real_worktree_checkout_lands_on_prefix_parent` + `test_backtest_replay_leaves_no_leaked_worktree` both PASS with `cwd=anchor` (2.65s). G3 no-leak (byte-identical porcelain before/after a raising body) holds. |
| 7 | P2-3 mkdir redundancy resolved | PASS | `base.mkdir(parents=True, exist_ok=True)` now INSIDE `if scratch_root is not None:` branch (`git_replay.py:127-131`); the `mkdtemp` else-branch (133) already creates the dir. Intent annotated (129-130). |
| 8 | G1 no-caret rule preserved | PASS | grep `^`: 5 hits, ALL in docstrings/comments (lines 10-13, 34, 45, 113); ZERO in any runtime argv. `commitish` passed through verbatim (140). Unit test asserts `"^" not in add[-1]` (`test_git_replay_unit.py:37`) + all 5 `prefix_parent_sha` caret-free (71-74). |
| 9 | Collision boundary intact | PASS | `git status --porcelain` on protected paths (`src/superclaude/skills/`, `.claude/`, `commands/troubleshoot.md`, `tests/troubleshoot/test_hardening_*`) = EMPTY. Only `tests/troubleshoot/backtest/` files present (git_replay.py + 2 test files + __init__). No impl-owned files touched. |
| 10 | No oversell / no new vacuity; tests assert real behavior | PASS | teardown test checks identity of propagated exception + actual remove/prune argv (not just "did not raise"); no-caret test checks the literal argv tail; no-leak test compares real porcelain output. No tautological/non-empty-stub assertions introduced. |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; verified an external fix agent's edits)
- Tests: 6/6 pass (unit 4/4 in 0.02s; integration 2/2 in 2.65s, real git, not skipped)

## Issues Found
None.

## Per-Finding Verdicts

**P2-1 (CRITICAL → FIXED, genuine).** Each `finally` teardown subprocess call now has its own
`try/except (_subprocess.TimeoutExpired, FileNotFoundError, OSError): pass`. A `TimeoutExpired`
or `FileNotFoundError` from the `remove` call — which `check=False` does NOT suppress — is caught
locally, so `rmtree` and the MANDATORY `prune` still run, and the `finally` block cannot raise and
therefore cannot mask a body exception. This is real control-flow robustness, not a comment-only
change, and it faithfully mirrors `process.py:392`.

**P2-2 (IMPORTANT → FIXED, seam preserved).** Repo anchoring is implemented via
`_repo_anchor()` (`git rev-parse --show-toplevel` through the mocked `_subprocess.run`) and passed
as `cwd=anchor` to add/remove/prune/list. Because `cwd=` is a keyword argument and the unit test
inspects only positional `args[0]` argv lists, the mock seam and all argv-slice assertions are
untouched. The implementation deliberately uses `cwd=` rather than `-C` precisely to avoid
altering argv shape — and there is no `-C` token anywhere. Anchor failure degrades safely to
`None` (inherit CWD), so the helper never raises and unit tests stay green.

**P2-3 (MINOR → FIXED).** `base.mkdir(...)` moved inside the `scratch_root is not None` branch;
the redundant no-op on the `mkdtemp` branch is gone.

## Self-Audit
1. Independently verified claims against source: 10 checks, all tool-backed — process.py seam
   (grep line 392), no-caret grep (5 doc-only hits), no `-C` grep (zero), `cwd=` keyword vs
   positional argv-slice analysis, collision-boundary `git status` on protected paths, and a full
   6/6 test run (unit + REAL-git integration).
2. Files read: `git_replay.py`, `test_git_replay_unit.py`, `test_git_replay_integration.py`,
   `qa-consolidated-findings-phase2.md`; grepped `src/superclaude/cli/sprint/process.py`.
3. Why trust a PASS here: the verdict is not "looks fine" — it rests on (a) the integration suite
   exercising the real teardown path against actual git including the raising-body no-leak case,
   (b) a positional-vs-keyword argument analysis proving `cwd=` cannot perturb the argv slices the
   unit test asserts on, and (c) an exact `git status` boundary check showing zero protected-path
   changes. Each finding maps to a specific cited line.
4. No web research was required (all verification was local-file/source/test-bound); Tavily-first
   N/A.

## Confidence
Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 4 | Grep: 4 | Glob: 0 | Bash: 5 (status + 4 grep/test runs)

## Recommendation
Green light. All 3 Phase 2 findings are genuinely resolved, the collision boundary and G1
no-caret rule hold, the mock seam is intact, and tests assert real behavior. The Phase 2
seam-teardown FAIL can be cleared.

## QA Complete
