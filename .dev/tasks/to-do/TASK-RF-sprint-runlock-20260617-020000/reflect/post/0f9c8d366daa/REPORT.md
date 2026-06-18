# Reflect Report — Sprint Release-Level Run-Lock (UC-2 post-execution)

- **Mode:** post (UC-2) · **Tier reached:** 2 (forced by `--depth deep`; also §5.3 rule 3 regression candidate)
- **Status:** `partial`
- **Diff audited:** `git diff 0f9c8d366daa` — note `0f9c8d366daa` **is HEAD**, so the audited diff is the **uncommitted working-tree** sprint-runlock work (7 files, +531/-54).
- **Spec:** `.dev/brainstorms/20260617-sprint-runlock/merged-requirements.md` (R1–R8 + 5 acceptance criteria)
- **Calibrated confidence:** 0.90 · **Evidence-validator:** ran, 24 citations re-Read, **0 dropped**, 2 `[INFERRED]`
- **Reviewer convergence:** 3/3 independent reviewers converged on the headline finding (~0.94)

> ⚠️ Diversity caveat: Tier-2 heterogeneity was achieved by **persona/scope rotation**, not distinct model vendors (`t2_model_class_diversity: degraded`, `t2_vendor_diversity: single`). Per §11.0 the anti-self-confirmation guarantee is therefore "ensemble pressure applied," not "self-confirmation neutralised."

---

## Verdict

The implementation is **substantially correct and well-tested** — R1 (atomic O_EXCL core + bounded retry), R2 (run lock), R3 (PID-reuse `/proc` mitigation), R4 (executor integration placement/release/refusal), and R6 (rerun-tasks disjoint-path proof) are all **grounded as compliant**, the full R7 13-case matrix is present, and the R8 regression suite is **green** (81 passed incl. the byte-exact e2e abort). **However, one HIGH functional defect (D1) makes the R5 escape hatch non-functional on the default execution path**, and several MED gaps remain. This work should **not** be promoted until D1 is fixed.

---

## 🔴 Headline finding — D1 (HIGH · Regression): `--ignore-run-lock` is silently dropped on the default (tmux) path

`superclaude sprint run` defaults to tmux (`commands.py:410` — `if not no_tmux and is_tmux_available(): launch_in_tmux(config)`). The tmux relaunch rebuilds the inner `--no-tmux` CLI as a **fresh subprocess** via `_build_foreground_command` (`tmux.py:176-210`), which re-emits `--debug` / `--stall-timeout` / `--stall-action` / `--model` / `--state-dir` — **but not `--ignore-run-lock`**. Per R4.3 the run lock is acquired in that inner worker (`executor.py:1688-1689`), whose `config.ignore_run_lock` therefore defaults back to `False`. 

**Consequence:** a user who passes `--ignore-run-lock` to recover from a crashed live-holder lock is **still refused** under the default path. The escape hatch only works with explicit `--no-tmux`. This directly contradicts spec **R5** ("thread it through `SprintConfig`… **so it survives the tmux relaunch config reconstruction**") and the field's own comment at `models.py:591-594` asserts the survival behavior it does not deliver. No test covers flag survival across the relaunch.

**Why the spec intent was defeated:** threading the field onto `SprintConfig` only helps an *in-process* config object; the tmux relaunch is a *new subprocess* that sees only the rebuilt argv. Survival requires re-emission in `_build_foreground_command`, which was missed.

**Fix (≈2 lines):** in `_build_foreground_command`, mirror the sibling blocks:
```python
if config.ignore_run_lock:
    cmd.append("--ignore-run-lock")
```
…plus a tmux-relaunch survival test.

---

## Deviation summary (4-category taxonomy)

| Class | Count | IDs |
|-------|-------|-----|
| Authorized expansion | 1 | D7 (phase-lock payload grew `starttime`) |
| Necessary deviation | 2 | D2 (R1.2 chain-vs-re-raise), D6 (`_acquire_pid_lock` signature expansion) |
| **Drift** | **3** | D3 (fd leak), D4 (R8 assertions not added), D5 (pre-try release window) |
| **Regression** | **1** | **D1 (R5 tmux escape-hatch drop)** |

Full detail: [`deviation-ledger.yaml`](./deviation-ledger.yaml). Grounding gaps: none ([`grounding-gaps.yaml`](./grounding-gaps.yaml) empty).

### Other actionable findings

- **D2 (MED · Necessary):** the R1.2 signal handler **chains** to the previous handler (`recovery.py:236-241`) rather than "restore default disposition and re-raise" (spec line 34). In-sprint this is correct (chains to the sprint `SignalHandler` per R4.1). But when `_prev` is non-callable (`SIG_DFL`/`SIG_IGN` — phase-lock / bare-invocation case), the handler releases then **returns normally → the signal is swallowed and the exit code is not 130/143**. R7 cases 7/8 stub `getsignal→SIG_DFL`, so they neither fire the chain branch nor assert exit codes. *Adjudicate:* re-raise when `_prev` is non-callable, or document the deliberate divergence.
- **D3 (MED · Drift):** `os.write(fd, …); os.close(fd)` in the success branch has **no `try/finally`** (`recovery.py:329-330`). If `os.write` raises (ENOSPC/EIO), the fd leaks and the just-created lockfile is left on disk. Low probability; fix = wrap in `try/finally`.
- **D4 (MED · Drift):** R8 explicitly required **new acquire-at-entry / release-on-exit assertions in resume/tmux launch tests**; neither `test_resume.py` nor `test_tmux.py` received them. The `execute_sprint` wiring is covered only at the unit level.
- **D5 (LOW · Drift):** the acquire site (`executor.py:1685-1713`) is **outside** the main `try` (starts at 1727); an exception in `tui.start()` / orphan `rmtree` / `execute_preflight_phases` (1715-1725) skips the finally's release and relies on the `atexit` backstop. The inline comment "the finally block below is the authoritative release" is slightly inaccurate for that window. (R4.1 mandates acquire-before-preflight, so the window is inherent.)

### Test-quality notes (non-blocking)

- All **13 R7 cases present and named** (`test_recovery.py:529-738`); 29 tests pass.
- Weak/over-stubbed assertions: case 5 (`:591`) drives the bounded-retry **exhaustion** path, not a single-loser race; cases 7/8 (`:621`/`:641`) stub `getsignal→SIG_DFL` so the chain branch never fires; case 2 (`:543`) uses `starttime:None` so the starttime-match-alive liveness branch is untested with the PID-naming surface.

---

## Verification triangle (default-on, UC-2)

| Suite | Result |
|-------|--------|
| `test_recovery.py` (13 new + phase-lock round-trip) | **29 passed** |
| R8 set: `test_recovery + test_rerun_tasks + test_resume + test_rerun_tasks_failure_modes` | **81 passed** |
| e2e `test_e2e_lock_and_retry_cap.py` (incl. byte-exact `test_concurrent_lock_aborts_with_pid`) | **3 passed** |
| Broad `tests/sprint/` (−`e2e_real`) | **1168 passed, 2 failed** |

The **2 broad-suite failures** (`test_rerun_tasks_e2e.py` — `Rerun failed (fileno)`) were **proven pre-existing**: they reproduce identically at clean HEAD via a reversible `git stash`, are environmental (CliRunner/TUI `.fileno()`), and are **not attributable to this diff**. `verification_regressions_detected: 0`.

---

## Compliant / refuted-concern register (grounded as PASS)

- **R4.1** acquire placement: after `SignalHandler.install()` (1605) + claude preflight (1598), before orphan cleanup (1718) + `execute_preflight_phases` (1725). ✓
- **R4.2** release before `signal_handler.uninstall()` in finally (2284-2294). ✓
- **R4.3** live-holder refusal → `_write_exit_sentinel(config, 1)` + `SystemExit(1)`; acquire is outside the try so **no double-uninstall / double-sentinel**. ✓
- **R6** disjoint-path assertion cannot false-fire: `bundle = results_dir/rerun-<ts>` ⇒ `sub_config.results_dir` strictly nested below `config.results_dir`. ✓
- **R1.1** `os.open(O_CREAT|O_EXCL|O_WRONLY,0o644)` replaces TOCTOU; bounded `max_attempts=3`, no livelock. ✓ (except D3 write-path)
- **R3** `/proc` field-22 = post-comm index 19 (empirically verified, paren/space comm handled); PID-only degrade when `starttime is None`. ✓
- **R8 byte-exact** phase-lock abort message preserved (`held_message=None`). ✓
- Closure capture (`_prev=prev, _lp=lock_path`) avoids the late-binding loop trap. ✓

---

## Promotion gate (Wave 7) — **SKIPPED (gate-failed)**

Adapter `task` resolved (tasklist under `.dev/tasks/to-do/TASK-*`), but the §14.5.2 strict gate fails on:
`status_success` (partial) · `tasklist_completion_pct_1_0` (R5 acceptance unmet) · `no_drift_no_regression` (drift=3, regression=1) · `frontmatter_status_matches` (frontmatter is `🟠 Doing`) · `no_user_decision_pending` (D1 remediation pending). No filesystem mutation performed.

---

## Recommended next step

Fix **D1** (re-emit `--ignore-run-lock` in `_build_foreground_command` + survival test), then address **D2/D3/D4**, re-run the validation commands, and re-reflect against the new diff. To author a corrective MDTM task automatically, re-run with `--remediate`:

```
/sc:reflect --mode post --diff <new-diff> --tasklist .dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/TASK-RF-sprint-runlock-20260617-020000.md --spec .dev/brainstorms/20260617-sprint-runlock/merged-requirements.md --depth deep --remediate
```

### `[INFERRED]` claims (non-load-bearing)
1. D2 exit-code consequence (130/143 not emitted when `_prev` non-callable) — reasoned from the handler control flow; no R7 test asserts the post-signal exit code.
2. D5 leak-window — inferred from the acquire-site-vs-try boundary; the `atexit` backstop mitigates in practice.
