# Reflect PRE Gate — REPORT (UC-1 coverage audit)

**run_id:** 20260619T025149Z-preee9acb22
**mode:** pre · **tier_reached:** 2 (depth=deep forced by TCS O2: frontmatter `type: Refactor`)
**status:** success · **verdict: PASS** · **coverage_pct: 1.00** (floor 0.90)
**tasklist:** TASK-RF-swarm-tui-fr1-regfix-20260619-021719.md
**spec:** .dev/brainstorms/swarm-tui-wiring/merged-requirements.md (FR-1, FR-5)
**reviewed_at:** 2026-06-19T02:51:49Z

## Scope note

This is a SCOPED corrective tasklist built from a reflect UC-2 POST deviation register. Its coverage target is ONLY the four POST-audit deviations (REG-1, DRIFT-2, DRIFT-3, DRIFT-4) against FR-1 (single-writer Console) and FR-5 (worker crash not masked). FR-2/FR-3/FR-4/FR-6/FR-7 were implemented by the parent task (TASK-RF-swarm-tui-wiring-20260618-165434) and are out-of-scope-by-design — NOT counted as unmapped. DRIFT-1 and NEC-1 are explicit out-of-scope follow-ups in the tasklist's Open Questions.

## Coverage matrix (merged from 2 heterogeneous Tier-2 reviewers: sonnet/analyzer + haiku/qa)

| Req | Sub-requirement | Mapped step(s) | Verdict | Evidence |
|-----|-----------------|----------------|---------|----------|
| FR-1.a | stdout/stderr kept off Console (Live redirect disarmed) | 1.3 | COVERED | `tui.py:221-226` `Live(...)` has no redirect args → Step 1.3 adds `redirect_stdout/stderr=False` |
| FR-1.b | workers' only output channel = filesystem (ParallelExecutor prints silenced on dispatch path) | 1.4, 1.5, 1.6 | COVERED | `parallel.py:110-232` unconditional prints → guarded by `if not self.quiet`; `dispatch.py:424` flips `executor.quiet=True` |
| FR-1.c | frozen `ParallelExecutor.__init__(self, max_workers=10)` preserved | 1.4, 1.7 | COVERED | class-attr `quiet` (not a kwarg); Step 1.7 re-runs `test_frozen_signatures_unchanged` (pins `["self","max_workers"]`) |
| FR-1.d (DRIFT-2) | FR-1 audit detects stdout writes, scoped to worker-surface callables, mutation guard | 3.1, 3.2 | COVERED | `test_inv012_tui_opt_in.py:608-643/700-713` only checks import/name symbols → extended with guard-aware stdout-write detector + mutation guard; scope exempts `__main__`/example prints |
| FR-1.e (REG-1 acceptance) | real-PTY smoke that reproduces the cross-thread render crash | 3.3 | **COVERED** (was PARTIAL — closed in-line) | Reviewer flagged the smoke lacked a concrete concurrent-stdout seam after `quiet=True` silences prints; Step 3.3 amended with the mandatory injection seam (monkeypatch `dispatch_wave1` to write concurrent stdout, or inject an un-silenced executor) so the smoke genuinely exercises the #181/#182/#184 path |
| FR-5.a (DRIFT-3) | reader exception cannot bypass `exc_box` re-raise; `Exception`-scoped; no busy-spin | 2.1 | COVERED | Guards `read_state`+`_tail_events`, falls through (no bare `continue`), seeds last-good, loop still reaches `exc_box` re-raise |
| FR-5.b (DRIFT-4) | worker crash dominates concurrent SIGINT; SIGINT-only still Exit(130) | 2.2 | COVERED | Reorders `exc_box` re-raise before `Exit(130)`; preserves FR-6 SIGINT-only path + `finally` teardown |
| FR-5.c | DRIFT-3/DRIFT-4 regression tests (fail pre-fix, pass post-fix) | 3.4, 3.5 | COVERED | Concrete monkeypatch seams (dispatch_wave1→raise seeds exc_box; read_state→ValueError / reader→KeyboardInterrupt) |

**Coverage: 8/8 COVERED, 0 unmapped.** (Pre-remediation: 7 full + 1 partial = 0.94; the PARTIAL FR-1.e was closed in-line per `--remediate`, bringing coverage to 1.00.)

## Reviewer verdicts (calibrated)
- **FR-1 reviewer (sonnet/analyzer):** 4/5 full + 1 partial (FR-1.e seam), 0 unmapped, conf 0.87. PARTIAL closed.
- **FR-5 reviewer (haiku/qa):** 3/3, 0 unmapped, conf 0.92. Noted 2 minor test-writing traps (Step 2.1 `None`-state tolerance; Step 3.4 must raise `ValueError` not `KeyboardInterrupt`) — both already explicit in the amended items; recorded as executor cautions, not coverage gaps.

## Evidence-validator gate
9 citations, all re-Read against live code during scope discovery + reviewer passes; **0 dropped**. No `[INFERRED]` rows.

## Verdict
**PASS** — coverage 1.00 ≥ floor 0.90; no regression/drift/human-decision flags. The tasklist faithfully and completely covers its scoped corrective target. Best-practice grade 5/5 (frozen-signature preservation, FR-5 non-masking invariant, Exception-scoped guards preserving FR-6, CI-parity ruff gates, executor-disjoint POST reflect).
