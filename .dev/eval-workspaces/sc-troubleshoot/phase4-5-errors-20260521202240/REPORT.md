---
status: success
tier_reached: 1
confidence: 0.95
test_is_wrong: false
test_file_path: null
---

# Troubleshoot Report — sprint run Phase 4/5 ERROR

**Target:** `superclaude sprint run .dev/releases/current/cliEval/tasklist-index.md`
**Symptoms:** Phase 4 (Expect Primitives and CLI Surface) ERROR exit 1 @ 200m 0s; Phase 5 (Eval Bodies Coverage Gate Rollout) ERROR exit 1 @ 282m 0s.
**Sprint run timestamp:** 2026-05-20 (per `checkpoints/CP-P04-END.md`, `checkpoints/CP-P05-END.md`).
**Tier reached:** 1 (single-domain, single root cause, fixes verifiable in-tree).
**Calibrated confidence:** 0.95.

## Summary

Both phase failures share **one root cause**: the `eval_run` body in
`src/superclaude/cli/eval/commands.py` referenced **eleven undefined
symbols** (`_new_run_id`, `_default_output_dir`, `_resolve_executor_factory`,
`_run_one_spec`, `_utc_iso_now`, `_can_install_signal_handler`,
`_compute_run_stats`, `_format_run_summary_line`,
`RUN_INTERRUPTED_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`,
`RUN_CLEAN_EXIT_CODE`). At runtime this raised
`NameError: name '_new_run_id' is not defined` at `commands.py:1418`. A
secondary Click 8.3.2 regression (`CliRunner.__init__()` no longer accepts
`mix_stderr`) broke `tests/cli/eval/test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr`,
and `ruff check src/superclaude/cli/eval/` had regressed to 23 errors
(11 F401 unused-imports + 12 F821 undefined names — the F821s being the
same eleven missing helpers).

**All three blockers are fixed in the current tree.** Re-running the
sprint is safe to proceed with for Phase 4 and Phase 5.

## Diagnosis (evidence-cited)

### Original blockers from the failed run

| # | Blocker | Source of failure | Cited file:line |
|---|---------|---------------------|-----------------|
| 1 | `eval_run` body NameErrors (11 helpers + 3 exit-code constants) | Production code | `src/superclaude/cli/eval/commands.py:1418` (per `checkpoints/CP-P05-END.md` extracted traceback) |
| 2 | Click 8.3.2 `mix_stderr` regression in test | Test | `tests/cli/eval/test_eval_group.py:114` (per `CP-P04-END.md` §1) |
| 3 | `uv run ruff check src/superclaude/cli/eval/` returns 23 errors (11 F401 + 12 F821) | Production code | Same `commands.py` source as #1 + stale imports |

P5 is downstream of P1 — `eval run` could not execute at all, so 2/6 T05.25 cases (`test_run_exits_2_when_settings_has_uncovered_matcher`, `test_run_writes_coverage_missing_artifact_under_output_dir`) and 1 T05.26 end-to-end SKIP all observed the same NameError. Per-eval determinism captures (`run-<Ei>.log`) for E1..E15 were therefore impossible.

### Fixes that have landed since 2026-05-20

| Commit | Subject | Addresses |
|--------|---------|------------|
| `e6368db8` | fix(cliEval): implement missing eval_run helpers + exit codes (PR #66 review) | Blocker #1 (all 11 helpers + 3 exit-code constants now defined) |
| `dce3c3cb` | fix(cliEval): PR #66 review remediation — NameError in eval_run + scratch-root allowlist tautology (#68) | Blocker #1 closure + adjacent fix |
| `08183738` | fix(cliEval): clear residual F401 + Click 8.3.2 mix_stderr + delete stale T04.09 skeleton tests/constants | Blockers #2 and #3 |

### Verification (re-tested live in this session)

1. **All 11 previously-undefined symbols now defined:**
   - `_utc_iso_now` → `commands.py:1308`
   - `_new_run_id` → `commands.py:1322`
   - `_default_output_dir` → `commands.py:1335`
   - `_can_install_signal_handler` → `commands.py:1346`
   - `_resolve_executor_factory` → `commands.py:1390`
   - `_run_one_spec` → `commands.py:1405`
   - `_compute_run_stats` → `commands.py:1477`
   - `_format_run_summary_line` → `commands.py:1526`
   - `RUN_CLEAN_EXIT_CODE` → `commands.py:570`
   - `RUN_FAILURES_EXIT_CODE` → `commands.py:573`
   - `RUN_INTERRUPTED_EXIT_CODE` → `commands.py:577`
2. **mix_stderr removed from tests:** `grep -n "mix_stderr" tests/cli/eval/test_eval_group.py` → no matches; all `CliRunner()` calls are zero-arg.
3. **Ruff clean:** `uv run ruff check src/superclaude/cli/eval/` → `All checks passed!`
4. **P5 previously-failing tests pass:** `tests/cli/eval/test_coverage_gate_integration.py::test_run_exits_2_when_settings_has_uncovered_matcher` and `::test_run_writes_coverage_missing_artifact_under_output_dir` → **2 passed**.
5. **Full cli/eval test suite:** `uv run pytest tests/cli/eval/` → **1343 passed, 4 skipped, 0 failed** (vs the failed-run state of 1267 passed, 2 failed).
6. **OQ-2 process gate cleared:** Per `decisions.md` line 18 (R12 entry, 2026-05-20): "OQ-2 sign-off table flipped 🟠 PROPOSED → 🟢 RESOLVED in lockstep with the ledger row."

## Proposed Fix

**No code change required.** All three code-level blockers identified in `CP-P04-END.md` / `CP-P05-END.md` are already in master at HEAD `5d71ae5e`.

**Recommended next step:** Re-run the sprint, optionally scoped to Phase 4 and Phase 5 only to save the ~9 hours of P1..P3 + P6 re-execution.

Paste-ready commands (single-line each):

```
superclaude sprint run /config/workspace/IronClaude/.dev/releases/current/cliEval/tasklist-index.md --phases 4,5
```

If the sprint runner does not support `--phases` selection, the safe fallback is the full run:

```
superclaude sprint run /config/workspace/IronClaude/.dev/releases/current/cliEval/tasklist-index.md
```

## Residual concerns (non-blocking, surface to user)

1. **Missing per-task evidence/artifact directories** (D-0070, D-0071, D-0072, D-0077 and their `evidence/T04.08`, `T04.09`, `T04.10`, `T04.16` siblings) were enumerated as outstanding in `CP-P04-END.md` §3. These are **runtime outputs** of the sprint — re-running the sprint will materialize them. They are not a precondition to re-run.
2. **`.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/`** task folder still sits under `to-do/`, but its code-level remit (the eleven helpers) has clearly landed. This is stale paperwork rather than missing work — archive after the re-run confirms P4/P5 pass.

## Risk + Rollback

- **Risk:** None on the diagnosis. The verifying evidence (full suite green + ruff clean + symbols present) is reproducible in <30s.
- **Re-run risk:** ~9-hour wall clock for a full sprint replay; ~8 hours for P4+P5 only. No destructive side-effects from a re-run — sprint outputs land under `TASKLIST_ROOT/results/`, `checkpoints/`, `evidence/`, `artifacts/` and are content-addressed by phase/task.
- **Rollback:** N/A — no changes proposed by this report.

## Next Steps

1. (User) Re-run the sprint per the paste-ready command above.
2. (Post-run) Verify `checkpoints/CP-P04-END.md` and `CP-P05-END.md` flip to `status: PASS`.
3. (Post-run) Archive `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/` to `.dev/tasks/done/`.
4. If P4 or P5 fail again, re-invoke this skill with `--depth deep` and include the new `CP-P0{4,5}-END.md` content in the prompt.
