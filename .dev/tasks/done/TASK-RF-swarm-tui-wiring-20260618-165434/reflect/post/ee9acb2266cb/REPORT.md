# Reflect Report — UC-2 Post-Execution Deviation Audit

**Work unit:** `TASK-RF-swarm-tui-wiring-20260618-165434` — Wire `--tui` into `superclaude swarm run` (Approach A)
**Spec:** `.dev/brainstorms/swarm-tui-wiring/merged-requirements.md` (FR-1..FR-7; FR-1 & FR-5 non-negotiable)
**Mode:** post · **Tier reached:** 2 (forced by `--depth deep`; also rule-3 regression escalation)
**Calibrated confidence (work fully + safely satisfies spec):** **0.25**
**Verdict:** ⛔ **REGRESSION on the non-negotiable FR-1 gate — promotion BLOCKED, remediation recommended.**

---

## 0. Input re-targeting (surfaced, not silent)

The supplied `--diff 300c06a6` is the tasklist's **`start_commit`** (frontmatter), **not** the work product — it resolves to PR #180 (TFEP migration), 164 unrelated files. The actual swarm-TUI work is **uncommitted in the working tree**. Nothing in commits #181→HEAD touched the target files, so `diff 300c06a6 -- <target files>` ≡ the working-tree diff. I re-scoped the audit to the working-tree changes of the 4 task target files and proceeded (confidence ≥ 0.90 on intent). If you intended to audit a different commit, stop here and re-run with the correct `--diff`.

**Audited artifacts:** `src/superclaude/cli/swarm/commands.py` (+263), `tests/swarm/test_inv012_tui_opt_in.py` (+202, modified), `tests/swarm/test_run_tui_integration.py` (new, 680L), `tests/swarm/test_tail_events.py` (new, 124L). `dispatch.py`, `parallel.py`, `tui.py` confirmed **unchanged** by this task.

---

## 1. Per-FR Verdict

| FR | Acceptance | Verdict | Evidence |
|----|-----------|---------|----------|
| **FR-1** single-writer Console *(non-negotiable gate)* | TUI symbols reachable from zero worker-side functions; `tui.update` main-thread only | ⛔ **FAIL (regression)** | Worker thread prints to stdout under armed Live redirect — see §2. `commands.py:1880-1995`, `tui.py:221-226`, `parallel.py:110-232`, `dispatch.py:424` |
| **FR-2** INV-012 gate + byte-identical non-TTY | identical exit/log/zero-ANSI w/ & w/o `--tui` on non-TTY | ✅ MET (behavior) / ⚠️ DRIFT (literal) | gate `commands.py:1882`; sync fallback `:1883-1891`; test passes. "No Rich import side effects" clause contradicted — DRIFT-1 |
| **FR-3** scope guards (detached + resume) | both rejected w/ `UsageError`; resume never enters TUI loop | ✅ MET | `:1638-1644` (`--tui --detached`), `:1596-1602` (resume); exploding-TUI sentinel proves no construction (`test_run_tui_integration.py:117-164`) |
| **FR-4** byte-offset tail + anti-spin | exactly-once, partial-line tolerant, bounded spin | ✅ MET | `_tail_events` `commands.py:3043-3105`; offset/skip/exactly-once proven `test_tail_events.py:46-124`; ceiling `test...py:545-614` |
| **FR-5** exception not masked *(non-negotiable gate)* | original traceback re-raised after `stop()`; non-daemon join | ⚠️ **PARTIAL** | Happy path correct (`:1981-1991`, `daemon=False`, `join()` in finally). Two masking edges: DRIFT-3 (read_state exception bypasses re-raise), DRIFT-4 (SIGINT discards `exc_box`) |
| **FR-6** idempotent teardown all paths | `stop()` on clean/exception/SIGINT; idempotent | ✅ MET | `finally: stop()→join()` `:1976-1983`; SIGINT→Exit(130) `:1984-1986`; idempotent `tui.py:230-234`; all 3 paths tested |
| **FR-7** non-vacuous run→tui integration | forced-TTY ≥1 worker row from tailed log; regression guard | ✅ MET (blind to FR-1) | `test_run_tui_integration.py:458-536`; `_tail_events` spy + ≥1 advanced row. Cannot exercise the TTY crash (CliRunner is non-TTY) |

**Frozen signatures (C3/AC-004/NFR-001):** ✅ `dispatch_wave1` + `ParallelExecutor` byte-identical to `start_commit`; pinned by `test_frozen_signatures_unchanged`.

**Test state:** all **26 tests pass** (`26 passed in 3.20s`), independently re-run.

---

## 2. The regression (REG-1) — FR-1 single-writer topology is false

FR-1 is the spec's **raison d'être**: Approach A was selected *specifically* because "workers' only output channel is the filesystem," making "exactly one thread touches the Console" a **structural** property that kills the Rich `Live` cross-thread render crash (PRs #181/#182/#184). That premise is **false**:

**Verified chain (each re-Read / re-run):**
1. `tui.py:221-226` — `Live(...)` is built with `console`, `refresh_per_second`, `screen=False` and **omits `redirect_stdout`/`redirect_stderr`** → Rich default `True`. The redirect is armed.
2. `parallel.py:110-232` — `ParallelExecutor.plan()`/`.execute()`/`_execute_group()` make **unconditional `print()`** to stdout.
3. `dispatch.py:424` — `dispatch_wave1` constructs `ParallelExecutor` by default; the `run_cmd --tui` path injects none → uses the printing one, **on the `swarm-wave1` worker thread**.
4. **Reproduced live:** a real `run_cmd --tui` run (gate forced open) emits `⚡ Parallel Executor: Planning 3 tasks` and `🚀 Executing 3 tasks` to stdout from the worker thread while the dashboard is active.

On a real TTY, Rich's armed redirect funnels those cross-thread stdout writes through the `Live`/`Console` machinery — **the precise #181/#182/#184 mechanism**. The non-negotiable gate is not actually satisfied.

**Why it shipped green:** the FR-1 audit (`test_inv012_tui_opt_in.py:655-713`) checks symbol **imports** (`rich`/`TUI`/`Live`/`Console`), not `print`/stdout writes — the *wrong invariant*. Every `--tui` integration test runs on a non-TTY CliRunner stream that structurally cannot reproduce the TTY-only cross-thread race. "26 tests pass" provides near-zero assurance about the one property that matters most.

**This is exactly what the heterogeneous ensemble caught:** the qa reviewer (conf 0.86) rated FR-1 *met* by reasoning from the green test suite; the analyzer reviewer (conf 0.18) reproduced the crash mechanism. Independent re-run confirmed the analyzer. Single-model self-review would have shipped this.

---

## 3. Deviation summary

| Class | Count | Items |
|-------|-------|-------|
| **Regression** | 1 | REG-1 (FR-1 cross-thread crash re-armed) |
| **Drift** | 4 | DRIFT-1 (eager Rich import vs FR-2 "no side effects"), DRIFT-2 (FR-1 audit checks wrong invariant / per-file only), DRIFT-3 (read_state exception bypasses FR-5 re-raise), DRIFT-4 (SIGINT discards worker `exc_box`) |
| **Necessary** | 1 | NEC-1 (SIGINT→Exit(130), documented) |
| **Authorized** | 3 | poll ceiling, render-glitch latch, runtime main-thread assert (FR-1-mandated) |

Full evidence + remediations: `deviation-register.yaml`.

---

## 4. Promotion gate — BLOCKED (`gate-failed`)

Failed conditions: `status_success` (partial), `tasklist_completion_pct_1_0` (0.86), `no_drift_no_regression` (1 reg + 4 drift), `frontmatter_status_matches` (frontmatter `status: 🟠 Doing`). The work-unit is **not** moved to `done/`.

---

## 5. Recommended remediation (the surgical fix)

1. **Kill the redirect** — pass `redirect_stdout=False, redirect_stderr=False` to `Live(...)` in `tui.py:221` (mirrors the sprint `SUPERCLAUDE_SPRINT_RENDER_DIAG` fix), **AND**
2. **Silence the worker prints** — gate `ParallelExecutor`'s `print()`s (or route them through the filesystem Logger) on the swarm dispatch path. Disabling the redirect alone lets worker prints corrupt the live dashboard (the PR #181 medium), so both are needed.
3. **Fix the audit** — extend `test_inv012_tui_opt_in.py` to flag `print(`/`sys.stdout`/`sys.stderr` writes on `dispatch.py` + `parallel.py`, and add a **real-PTY** `--tui` smoke asserting no crash under concurrent worker output.
4. **FR-5 edges** — guard `read_state`/`_tail_events` in the poll loop (DRIFT-3); check `exc_box` before `raise Exit(130)` (DRIFT-4).
5. **FR-2 literal** — defer the `TUI` import into the `_tui_active` branch; add a `sys.modules`-absence assertion (DRIFT-1).

Note: items 1-3 touch `tui.py` (marked "unchanged by design") and `parallel.py` (a frozen-surface caller) — the fix necessarily reaches beyond the task's original target files because the root cause lives there.
