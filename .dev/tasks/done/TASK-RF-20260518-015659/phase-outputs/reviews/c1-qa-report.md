# QA Report — C1 Task Integrity

**Topic:** C1 — `startup_stall_timeout` field + watchdog split + 5 new tests
**Date:** 2026-05-18
**Phase:** task-integrity (C1 scope-confined)
**Fix cycle:** 1 (PASS, no fixes needed)

## Overall Verdict: **PASS**

## Items Reviewed (11/11 PASS)

| # | Check | Result |
|---|-------|--------|
| 1 | Inline `#`-sentinel convention on dataclass field | PASS — `models.py:370` matches surrounding style |
| 2 | Loader signature default matches dataclass default (both 300) | PASS — `config.py:285` + `models.py:370` |
| 3 | Click option help + decorator order matches `run()` parameter order | PASS — `commands.py:138-145` + L193-195 + L225 |
| 4 | Two watchdog branches syntactically mutually exclusive | PASS — `events_received == 0` vs `> 0` partition |
| 5 | `[WATCHDOG]` stderr format with `Startup-stall` vs `Mid-stall` disambiguation | PASS — both kill+warn arms in both branches |
| 6 | `_stall_acted` single-fire reset clause unchanged | PASS — `executor.py:1443-1444` |
| 7 | Tests use canonical `_make_config` + `patch(Popen)` + `os.setpgrp/getpgid/killpg` | PASS — `MagicMock()` stdin workaround documented |
| 8 | `stall_action` default unchanged (`"warn"` per Q1) | PASS — confirmed 4 sites |
| 9 | `stall_timeout` default unchanged (`0` per Q4) | PASS — confirmed 4 sites |
| 10 | No scope creep — `_run_task_subprocess` body L1086-1115 + `output_file/error_file` L470-474 unchanged | PASS — only L1106 acknowledged C3 + L1264 acknowledged C4 |
| 11 | `pytest TestStartupStallTimeoutDefaults TestStartupStallWatchdog -v` → 5/5 pass | PASS — `5 passed in 0.13s` confirmed live |

## Adversarial findings probe
- Decorator-vs-parameter Click ordering: verified correct (decorator-application order matches positional).
- Mutual exclusion is logical, not just textual.
- Help text and 0=disabled semantics accurate.
- Warn-path message symmetry preserved.
- Test independence from C3 work confirmed.
- Pre-existing `.stdin` issue (commit 4799719) is INDEPENDENT of C1.

## Recommendations
C1 is complete and ready. Green light to proceed to C2 (Phase 6).

**VERDICT: PASS** (11/11 checks, 5/5 tests, 100% confidence)

(Report file written manually by the orchestrator; findings verbatim from the rf-qa agent response.)
