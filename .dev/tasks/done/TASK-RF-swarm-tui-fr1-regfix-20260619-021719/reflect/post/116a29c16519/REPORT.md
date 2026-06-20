# Reflect UC-2 (post-execution) — Tier 2 deep audit

**Task:** `TASK-RF-swarm-tui-fr1-regfix-20260619-021719` — swarm `--tui` FR-1 regression (REG-1) + FR-5 edges (DRIFT-3/DRIFT-4) + FR-1 audit hardening (DRIFT-2)
**Diff:** `git diff 300c06a6d53287893a446db8e859f5f1bc5434d8` (start_commit → working tree), scoped to the swarm surface
**Spec:** `.dev/brainstorms/swarm-tui-wiring/merged-requirements.md`
**Mode:** post · **Tier:** 2 (forced by `--depth deep`) · **Executor:** sonnet (excluded from reviewer pool)
**Status:** `partial` · **Calibrated confidence (verdict):** 0.91

---

## Headline verdict

**The corrective work is COMPLETE and CORRECT. Zero code regressions, zero unauthorized drift.** All four targeted deviations from the parent POST audit — REG-1, DRIFT-2, DRIFT-3, DRIFT-4 — are fixed, and the fixes are (mostly) backed by non-vacuous tests that genuinely fail against pre-fix code (independently re-verified). The full `tests/swarm/` suite is green (**2234 passed, 26 skipped**), the frozen `ParallelExecutor.__init__` signature is preserved, and the 7 task surfaces are ruff-clean.

The `status: partial` is **not** driven by any code defect. It is forced by (1) six **line-number-imprecise citations** in the reviewer cards (the cited *content* is verified-present; only the line refs were stale) and (2) **one human-decision grounding gap** (whether KO-4's repo-wide ruff clause is accepted as out-of-scope). Both are below.

### Three-reviewer convergence (heterogeneous, adversarial)

| Reviewer | Persona | Verdict | Conf | Regressions | Unauthorized drift |
|---|---|---|---|---|---|
| R1 | QA | DEVIATIONS-FOUND | 0.88 | 0 | 0 |
| R2 | analyzer | CLEAN | 0.90 | 0 | 0 |
| R3 | refactorer | CLEAN | 0.96 | 0 | 0 |

All three converge on the load-bearing claim. R1 reverted each fix in-tree and **confirmed the DRIFT-3/DRIFT-4 regression tests genuinely fail pre-fix**. R2 verified the FR-1 single-writer property is **structural across the transitive worker call graph**. R3 verified the change surface is **exactly the declared files** with no gold-plating.

---

## Coverage — Key Objectives

| KO | Objective | Status | Evidence |
|----|-----------|--------|----------|
| KO-1 | REG-1 source fix (tui.py + parallel.py + dispatch.py, frozen sig) | ✅ COVERED | `tui.py:226-227` redirect disarmed; `parallel.py:100` `quiet` class attr + all worker prints gated; `dispatch.py:425` `executor.quiet = True`; `test_frozen_signatures_unchanged` green |
| KO-2 | FR-5 edges DRIFT-3 + DRIFT-4 (commands.py poll loop) | ✅ COVERED | `commands.py:1947-1956` reader `try/except Exception` + last-good retention (no busy-spin `continue`); `exc_box` re-raise reordered **before** `Exit(130)`; guards scoped to `Exception` (FR-6 intact) |
| KO-3 | DRIFT-2 audit hardening + PTY smoke + regression tests | ⚠️ COVERED (1 caveat) | AST detector + 2 mutation guards solid; DRIFT-3/4 regression tests genuine (fail pre-fix); **PTY smoke partially vacuous — see D1** |
| KO-4 | Deterministic verification + POST reflect gate | ⚠️ PARTIAL | swarm suite green (2234), frozen-sig green, **7 task surfaces** ruff-clean; **repo-wide** ruff not clean (pre-existing debt — G1); POST reflect = this run |

`tasklist_completion_pct: 0.875` — Phases 1-3 and Steps 4.1-4.4 are `[x]`; Steps 4.5 (this gate) and 4.6 (status → Done) are pending **by design**.

---

## Deviation taxonomy (4-category)

**Regression: 0.** **Unauthorized drift: 0.**

### Authorized expansion (2)
- **A1 — parallel.py/dispatch.py modified despite spec `unchanged_by_design`.** The original spec listed both under `unchanged_by_design` (C3/AC-004). The REG-1 discovery proved that posture re-armed the #181 crash; the regfix **tasklist** (the gold-standard for this work) authorizes touching them in KO-1. The truly frozen invariant `ParallelExecutor.__init__(self, max_workers=10)` is preserved verbatim via a class-attribute + per-instance flip (verified vs `test_frozen_signatures_unchanged`). R2 central-tension verdict concurs: AUTHORIZED/NECESSARY.
- **A2 — DRIFT-1 (eager TUI import) and NEC-1 (SIGINT Exit 130) deferred** — explicitly documented out-of-scope (`TASK…md:327-328`); not silently actioned.

### Necessary deviation (2)
- **N1 — ruff-format reflow hunks in commands.py** on lines unrelated to the fix. CI-format-parity churn from `ruff format` on the touched file; R3 reproduced the identical reflow on pristine HEAD. No behavior change.
- **N2 — FR-1 main-thread runtime assertion** added caller-side (`assert threading.get_ident() == main_ident` before each `update`) — directly satisfies an FR-1 acceptance clause; placed outside the render-glitch guard so it is never swallowed.

### Drift (3) — all NON-BLOCKING (test-quality / future-proofing)
- **D1 (MED) — Real-PTY smoke is partially vacuous as a REG-1 cause-1 guard.** **Independently verified by reflect:** `test_tui_real_pty_no_crash_under_concurrent_worker_stdout` (`test_run_tui_integration.py:299-372`) **passes 5/5 with the `tui.py` redirect fix reverted** — the cross-thread Rich crash is nondeterministic, so the smoke does not reliably trigger it. **Mitigant:** REG-1 protection does **not** depend on this smoke — the structural AST audit (`test_worker_surfaces_have_zero_tui_reachability`, non-vacuous, 2 mutation guards) plus the redirect disarm itself carry the real coverage (R2 confirmed the property is structural). This is a test-quality finding, not a code defect.
- **D2 (LOW) — DRIFT-3 regression test timing non-determinism** (~1 flake in 95+ runs per R2; fix control flow proven sound). Recommend a deterministic reader-raise seam.
- **D3 (LOW) — FR-1 stdout-write AST detector blind spots:** flags `print()`/`sys.stdout`/`sys.stderr` but not `os.write(1,…)`, `Console().print`, or write-via-aliased-handle. Sufficient for current worker surfaces; optional future-proofing.

---

## Grounding gaps (human decision required)

- **G1 — KO-4 repo-wide ruff clause.** KO-4 literally requires `uv run ruff check src/ tests/` to pass repo-wide; it does not (125 check errors + 102 format files). R3 verified this debt is **pre-existing and disjoint from all 7 task surfaces** (a sample debt file fails identically at start_commit), and the 7 task surfaces themselves pass targeted `ruff check` + `ruff format --check`. The task's own Phase 4 Findings (`TASK…md:317-319`) document it as accepted out-of-scope. **Decision needed:** ACCEPT as pre-existing/out-of-scope (KO-4 satisfied at task-surface level), OR spin a separate repo-wide lint cleanup task before final acceptance.

---

## Evidence-validator gate

74 citations re-Read; **6 dropped**. All 6 are **line-number imprecision on verified-present content** — corrected here:

| Stale citation | Corrected |
|---|---|
| `tui.py:224-225` (redirect) ×2 (card-1) | `tui.py:226-227` |
| `tui.py:225-226` (redirect) (card-3) | `tui.py:226-227` |
| `parallel.py:105-146` (all gated prints) (card-1) | `plan` 112-169, `execute` 180-201, `_execute_group` 235-242 |
| `commands.py:1973-1980` (DRIFT-3 guard) ×2 (card-3) | `commands.py:1947-1956` |

No finding rests on a dropped citation; each underlying fact (redirect disarm, print gating, DRIFT-3 guard) was independently re-verified by reflect against the live diff. Per §11.2, `citations_dropped > 0` forces `status: partial`.

---

## Promotion (Wave 7) — SKIPPED (correctly)

`promotion_action: skipped`, `skip_reason: gate-failed`. Five gate conditions fail: status≠success, completion≠1.0, frontmatter status `🟠 Doing`≠done, citations_dropped>0, grounding-gaps non-empty. This is the intended outcome — this reflect **is** Step 4.5 (the in-loop POST gate); the task is mid-flight under `.dev/tasks/to-do/`, and Step 4.6 (status → Done) follows operator acceptance of this report. **No filesystem mutation performed.**

---

## Recommendation

**Accept the corrective work.** REG-1/DRIFT-2/DRIFT-3/DRIFT-4 are correctly fixed with no regressions and no unauthorized drift. Before flipping the task to Done, resolve **G1** (the only human-decision item) and optionally take the Tier-3 polish for **D1/D2/D3** (test-robustness, all non-blocking). The `--remediate` offer is surfaced separately.
