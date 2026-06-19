# QA Report — KPI-telemetry / Numbers Lens (Wiring Accumulator)

**Topic:** R-10 sprint-cumulative wiring-telemetry accumulator + TM-13 test
**Date:** 2026-06-18
**Phase:** task-qualitative (KPI/numbers lens, final QA gate)
**Fix authorization:** false (REPORT ONLY — no edits made)

---

## Scope of this lens

The wiring-telemetry accumulation chain (R-10):
1. `_SprintWiringTotals` dataclass construction (`executor.py:335-357`)
2. Pre-loop instance `sprint_wiring_totals` near `shadow_metrics` (`executor.py:1832-1842`)
3. Task-path add-site after the wiring hook (`executor.py:2003-2015`)
4. Legacy-path add-site after the wiring hook (`executor.py:2395-2406`)
5. Arg swap into `build_kpi_report(..., turn_ledger=sprint_wiring_totals)` (`executor.py:2533-2544`)
6. Reader (`kpi.py:192-197`) + format labels (`kpi.py:140-143`)
7. TM-13 test (`tests/sprint/test_per_phase_budget.py:613-669`)

Adversarial mandate: assume >=5 errors. Each finding cites file:line.

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Attribute names match `kpi.py:193/195/197` reads | AX-2 | PASS | Accumulator exposes `wiring_turns_used`/`wiring_turns_credited`/`wiring_analyses_count` (`executor.py:355-357`); kpi reads same three names (`kpi.py:193,195,197`), writing `wiring_analyses_count`→`report.wiring_analyses_run` (report-side rename only, `kpi.py:197`). No mismatch. |
| 2 | Summation is read-only (per-phase ledger never mutated) | AX-5 | PASS | Both add-sites do `sprint_wiring_totals.X += ledger.X` (`executor.py:2009-2015`, `2400-2406`). RHS reads `ledger.X`; LHS is the accumulator. Ledger is never written. |
| 3 | Accumulator introduces no shared budget pool | none | PASS | `_SprintWiringTotals` is a plain 3-int dataclass (`executor.py:355-357`) with no `available()`/`try_launch()`/`can_run_wiring_gate()`. Cannot be consulted as a budget pool; R-3/R-4 per-phase independence preserved. |
| 4 | BOTH add-sites contribute (task AND legacy) | AX-3 | PASS | Task path `executor.py:2009-2015` after hook `2003`; legacy path `executor.py:2400-2406` after hook `2388`. Identical 3-field summation in both. |
| 5 | Arg swap passes accumulator, not last-phase ledger | none | PASS | `build_kpi_report(..., turn_ledger=sprint_wiring_totals)` (`executor.py:2543`), not the post-loop `ledger`. |
| 6 | TM-13 expects sprint-cumulative 5 (3+2), not last-phase 2 | AX-4 | PASS | Asserts `Analyses run == 5` (`test:657`), `used == 5` + `used != 2` (`test:664-665`), `credited == 20` + `credited != 8` (`test:666-669`). Number trace: ph1 used3/cred12/cnt3, ph2 used2/cred8/cnt2 → cum 5/20/5. credit = `int(5*0.8)=4`/analysis (rate default 0.8 `models.py:1035`; `int()` floor `models.py:1121`). |
| 7 | Per-task wiring path cannot pollute count | none | PASS | `wiring_gate_mode="off"` (`test _make_task_config:96`) → `run_post_task_wiring_hook` returns at `executor.py:551-552` BEFORE `debit_wiring` (`564`). Phase-level hook fully replaced by stub (`test:636-645,647-649`). Only the stub writes wiring counters. |
| 8 | Test reads ACTUAL persisted gate-kpi-report.md | none | PASS | `kpi_path = config.results_dir / "gate-kpi-report.md"`; `kpi_path.exists()` then `kpi_path.read_text()` (`test:652-654`). Same path executor writes (`executor.py:2545-2546`). Not the in-memory report object. |
| 9 | KPI format labels match test parser substrings | AX-2 | PASS | `format_report` emits `"  Turns used:       {..}"` (`kpi.py:140`), `"  Turns credited:   {..}"` (`141`), `"  Analyses run:     {..}"` (`143`). Parser matches substrings `"Turns used:"`/`"Turns credited:"`/`"Analyses run:"` and `rsplit(maxsplit=1)[-1]` (`test:605-610`). Each label unique; no collision. |
| 10 | TM-13 executes green | none | PASS | `uv run pytest ...::test_kpi_wiring_totals_accumulate_across_phases` → 1 passed in 0.16s. |

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

No miscount, last-phase-only collapse, or attribute-mismatch defect found. The
adversarial mandate ("assume >=5 errors") was discharged by tracing each of the
five demanded failure modes to its source and confirming each is correctly
guarded — see Adversarial Trace below.

---

## Adversarial Trace (the five demanded failure modes, each cleared)

1. **Attribute mismatch** — `kpi.py:197` reads `.wiring_analyses_count` and the
   accumulator defines `wiring_analyses_count` (`executor.py:357`), NOT
   `wiring_analyses_run`. The `_run` name lives only on the report field
   (`kpi.py:57`, assigned at `kpi.py:197`). A naive author could have named the
   accumulator field `wiring_analyses_run` to "match" the report and broken the
   read — they did not. CLEARED.
2. **Last-phase-only collapse** — the arg swap (`executor.py:2543`) passes
   `sprint_wiring_totals`, not the post-loop `ledger`. Passing `ledger` would
   yield used=2/credited=8/count=2; TM-13 explicitly asserts `!= 2` and `!= 8`
   (`test:665,669`). CLEARED.
3. **Only one add-site contributes** — both task (`executor.py:2009-2015`) and
   legacy (`executor.py:2400-2406`) fold counters identically. CLEARED.
4. **Per-task path pollutes count** — `mode=="off"` early-return at
   `executor.py:551-552` precedes `debit_wiring` at `564`; stub fully owns the
   counts. CLEARED.
5. **Test reads stale/in-memory data** — reads the persisted file at
   `config.results_dir/gate-kpi-report.md` (`test:652-654`), matching the write
   site (`executor.py:2545-2546`). CLEARED.

---

## Observations (non-defects, no remediation required)

- **O-1 (coverage, MINOR-info):** TM-13's two phases are both task phases, so it
  exercises the task-path add-site (`executor.py:2009`) numerically but NOT the
  legacy-path add-site (`executor.py:2400`). The legacy add-site's *invocation*
  is structurally covered by TM-8's wiring-hook assertion (`test:415-416`), but
  no test numerically sums legacy-phase wiring counters into the accumulator.
  This is a coverage gap, not a logic defect — the legacy add-site is
  byte-identical to the verified task add-site. Not a blocker.
- **O-2:** `kpi.py:195` floors credited to `max(0, ...)`; in TM-13 credited=20 is
  positive, so the floor is inert here. Correct behavior, noted for completeness.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on structural QA for section-numbering / cross-ref existence; this lens
  re-verified only the numeric/attribute semantics.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Attribute-name contract verified by Grep of `kpi.py:193/195/197` reads against
  `executor.py:355-357` definitions — not by trusting a prior report.
- Number trace (3+2=5; `int(5*0.8)=4`; 12+8=20) recomputed from `models.py:1095-1126`
  `debit_wiring`/`credit_wiring` bodies and `reimbursement_rate=0.8` (`models.py:1035`).
- Read-only summation verified by reading both add-site bodies
  (`executor.py:2009-2015`, `2400-2406`) — LHS/RHS confirmed.
- Per-task no-pollution verified by reading the `mode=="off"` guard
  (`executor.py:551-552`) sitting above `debit_wiring` (`564`).
- TM-13 executed live (`uv run pytest` → 1 passed) — behavior, not assumption.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 7 | Grep/Bash: 5 | Glob: 0

---

## Overall Verdict: PASS — wiring-telemetry accumulation logic and TM-13 are numerically correct, attribute-aligned, read-only, both-add-site complete, sprint-cumulative (5=3+2 not 2), and read from the actual persisted gate-kpi-report.md. No CRITICAL/IMPORTANT/MINOR defect. One non-blocking coverage observation (O-1: legacy add-site not numerically exercised by TM-13).
