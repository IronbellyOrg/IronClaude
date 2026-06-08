# rf-qa Task-Integrity Gate Verdict — Stage 0 (TASK-RF-20260603-024610)

**Phase:** task-integrity (Stage 0 — isolation env injection + real turn counting)
**Date:** 2026-06-03
**Stance:** ADVERSARIAL / zero-trust. Every claim re-derived from files on disk; test suite + lint re-run independently.
**Fix authorization:** true (no fixes were required).

---

## OVERALL VERDICT: **PASS**

All 8 criteria PASS with file:line evidence. Independent re-run reproduces `5 failed, 112 passed`; the 5 failures are verbatim pre-existing baseline `.stdin` harness failures on Path A (NOT regressions). Lint clean. No issues of any severity found; no fixes applied.

---

## Per-Criterion Checklist

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Path A merge (H1): keeps phase-scoped `CLAUDE_WORK_DIR`, adds only SETTINGS+PLUGIN | **PASS** | `executor.py:1376-1381` — `_layers = setup_isolation(config, scope=f"phase-{phase.number}")`; `_phase_env_vars` re-pins `CLAUDE_WORK_DIR=str(isolation_dir)` (isolation_dir = `config.results_dir/.isolation/phase-{N}` @ `executor.py:1353`), and merges ONLY `CLAUDE_SETTINGS_DIR` + `CLAUDE_PLUGIN_DIR` from `_layers.env_vars`. setup_isolation's own release-dir `CLAUDE_WORK_DIR` is deliberately NOT merged (comment `executor.py:1373-1375`). |
| 2 | Path B inject (H1): full 4-key env via `_task_env` into `_Base.__init__` | **PASS** | `executor.py:1149` — `env_vars=_task_env(task, config, phase)` passed to `_Base.__init__(...)` inside `_run_task_subprocess`. `_task_env` (`executor.py:1097-1110`) returns `setup_isolation(config, scope=f"task-{task.task_id}").env_vars` (the full 4-key set: WORK/GIT/PLUGIN/SETTINGS via `IsolationLayers.env_vars` @ `executor.py:127-134`). |
| 3 | IsolationLayers field-order unchanged; signature pin re-pinned to `("config","scope")`, scope KEYWORD_ONLY default `""` | **PASS** | Dataclass field order `scoped_work_dir, git_boundary, plugin_dir, settings_dir` intact (`executor.py:121-124`). Probe field-order asserts intact (`test_isolation_layers_probe.py:58-78`). Signature pin re-pinned: `tuple(params.keys()) == ("config","scope")`, `params["config"].kind == POSITIONAL_OR_KEYWORD`, `params["scope"].kind == KEYWORD_ONLY`, `params["scope"].default == ""` (`test_isolation_layers_probe.py:131-134`). Deliberate H1 extension, not a regression. |
| 4 | scope="" byte-equivalence: same plugins/settings dirs as before | **PASS** | `executor.py:179-185` — `plugin_dir = base/"plugins"`, `settings_dir = base/"settings"`; `if scope:` (line 181) appends `/scope` ONLY when non-empty. With `scope==""` the guard is falsy → no subdir, identical to pre-H1. Existing default-scope tests confirm green: `test_executor.py:750-803` (`test_setup_isolation_creates_all_dirs`, `test_isolation_env_vars`, `test_isolation_no_cross_task_leakage`, `test_isolation_idempotent`) all call `setup_isolation(config)` and pass in the re-run. |
| 5 | Real turn count: `max(count_turns_from_stream_json(...), 0)`, stale T02.06 comment replaced, parser robust, monitor.count_turns_from_output unchanged | **PASS** | `executor.py:1160` — `turns = max(count_turns_from_stream_json(output_path), 0)` (NOT hard-coded 0). Stale `# Turn counting is wired separately in T02.06` replaced with supersede comment (`executor.py:1156-1159`); only remaining T02.06 mention is that explanatory comment. Import present (`executor.py:40`). Parser (`process.py:32-76`): finds terminal `{"type":"result"}` event's `num_turns` (keeps LAST, line 69), returns 0 on missing file (52-53)/OSError (56-57)/no-result (71-72)/non-int (76), tolerates malformed lines without raising (62-67). Distinct contract documented in docstring (process.py:42-50). `monitor.count_turns_from_output` UNCHANGED — still counts `"type":"assistant"` lines via `_TURN_INDICATOR_PATTERN` (`monitor.py:112, 223-247`). |
| 6 | Exact-turn-count e2e asserts `== N` (not `!= 0`) | **PASS** | `test_e2e_turn_count.py:30,49-52` — `known_n = 7`; shim driven via `FAKE_CLAUDE_NUM_TURNS=7`; asserts `tr["turns_consumed"] == known_n` EXACTLY, with comment that it would fail against pre-change `0`. Real-spawn path via `claude_shim`+`real_release` (not `_subprocess_factory`). Passes individually in re-run. |
| 7 | `_env_capture` seam: inert when None, once per launched task, orthogonal to `_subprocess_factory` | **PASS** | `execute_phase_tasks` signature adds keyword-only `_env_capture: list | None = None` (`executor.py:944`) as sibling to `_subprocess_factory` (943). Capture guarded `if _env_capture is not None:` (1017) → inert when None. Appends `_task_env(task, config, phase)` (1018) inside the per-task loop, after budget check, BEFORE spawn, regardless of factory vs real path (1020-1026). Per launched task (skipped tasks break out at 998 before capture). |
| 8 | No-regression: 5 failing tests are pre-existing `.stdin` baseline failures; lint clean | **PASS** | Independent re-run of the exact Step-2.11 command → `5 failed, 112 passed in 0.66s`. All 5 (`test_execute_sprint_pass`, `_halt`, `_timeout_exit_code_124`, `_interrupted`, `test_backward_compat_sprint_pass_grace_period_zero`) appear verbatim on `pre-change-baseline.md` lines 58-62, all failing with `AttributeError: '<Popen-double>' object has no attribute 'stdin'` at `pipeline/process.py:141` on the Path A single-session fallback — NOT the Path B code Stage-0 wired. All 5 new Stage-0 tests PASS individually (incl. negative-control contention detected, not xfailed). `make lint` → "All checks passed!" (exit 0), re-run independently. |

---

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep/Bash-grep: 5 | Bash (pytest/lint re-run): 4
  - Tool calls (16) > checklist items (8): each criterion backed by direct source Read + independent re-run, not report reliance.
- Every criterion marked VERIFIED cites specific file:line or test output above.

## Issues Found / Fixes Applied

**None.** Zero issues at any severity (formatting, missing assertion, incorrect merge, broken invariant). No fixes applied (fix_authorization was true but unneeded).

Adversarial deep-checks that could have surfaced issues but did not:
- Confirmed no leftover hard-coded `turns_consumed=0` / `return (..., 0, output_bytes)` in Path B (grep clean).
- Confirmed `isolation_dir` (Path A work-dir) resolves to the phase-scoped copy dir, not `config.release_dir`.
- Confirmed `monitor.count_turns_from_output` was NOT modified (assistant-line semantics preserved per H-B supersede-by-addition).
- Confirmed scope="" guard makes the default path byte-identical to pre-H1; existing default-scope tests stay green.
- Confirmed the negative-control test detected real contention on this runner (passed, not xfail) — the corruption-detection harness is genuinely exercised.

## No-Regression Note (final)

The no-regression claim in `stage0-tests.md` / `stage0-gate-input.md` is **independently confirmed accurate**. I re-ran the exact Step-2.11 pytest command and `make lint` from the worktree root rather than trusting the summary. Result matched byte-for-byte on counts (`5 failed, 112 passed`) and on the failing-test identity (all 5 are the pre-existing Path A `.stdin` harness doubles, on the baseline already-failing list, failing for the same root cause). Stage-0 touched only Path B (`execute_phase_tasks`/`_run_task_subprocess`/`_task_env`) plus the additive `setup_isolation` scope param and the parser in `process.py`; none of those are exercised by the 5 failing Path A integration tests. Lint is clean.

## QA Complete
