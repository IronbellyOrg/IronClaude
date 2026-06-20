# Evidence-validator gate report

**citations_total:** 74 · **citations_verified:** 68 · **citations_dropped:** 6
**Policy:** full_reread. Per §11.2, `citations_dropped > 0` → `status: partial`.

## Dropped citations (all line-number imprecision on verified-PRESENT content)

| Card | Stale citation | Reality | Corrected |
|---|---|---|---|
| card-1-qa | `tui.py:224-225` (redirect) | 224-225 are `refresh_per_second`/`screen=False` | `tui.py:226-227` |
| card-1-qa | `tui.py:224-225` (KO-1 repeat) | same | `tui.py:226-227` |
| card-1-qa | `parallel.py:105-146` (all gated prints) | range covers only start of `plan`; `execute`@173, `_execute_group`@214 | `plan` 112-169 / `execute` 180-201 / `_execute_group` 235-242 |
| card-3-refactorer | `tui.py:225-226` (redirect) | 225 `screen=False`, 226 only `redirect_stdout` | `tui.py:226-227` |
| card-3-refactorer | `commands.py:1973-1980` (DRIFT-3 guard) | 1973-1980 = break/iteration/KeyboardInterrupt | `commands.py:1947-1956` |
| card-3-refactorer | `commands.py:1973-1980` (DRIFT-3 repeat) | same | `commands.py:1947-1956` |

No finding rests on a dropped citation — each underlying fact (redirect disarm, print gating, DRIFT-3 reader guard) was independently re-verified by the reflect orchestrator against the live `git diff`. The drops are citation-precision only.

## PTY-smoke revert experiment (orchestrator-run; the validator agent lacked Bash/Edit)

Reviewer 1 finding F1 claimed the real-PTY smoke passes even with the `tui.py` redirect fix reverted. **Independently executed by the orchestrator:**

- Backed up working-tree `tui.py`, removed ONLY the `redirect_stdout=False`/`redirect_stderr=False` lines.
- Ran `test_tui_real_pty_no_crash_under_concurrent_worker_stdout` **5×** → **1 passed** every time (`5/5 pass-with-revert`).
- Restored `tui.py`; `git diff --stat 300c06a6 -- tui.py` = `2 ++` (redirect lines back at 226-227). Tree clean.

**Result: pass-with-revert → R1's claim is TRUE.** The smoke is partially vacuous as a REG-1 cause-1 guard (the cross-thread crash is nondeterministic). Recorded as deviation **D1 (MED, drift)**. REG-1 protection is carried by the structural AST audit + the redirect disarm, not this smoke.

**tui.py restored:** confirmed — `redirect_stdout=False`/`redirect_stderr=False` present at lines 226-227.
