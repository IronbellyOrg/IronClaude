# Anchor Verification Map — Step 1.4 (Anti-Drift Gate)

**Task:** TASK-RF-per-phase-turn-budget-20260618-160752
**Verified:** 2026-06-18, worktree `perPhaseturnBudget` (HEAD = origin/master)
**Spec:** `.dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md` (spec_version 3.0), §4 Requirements + §7 Blast-Radius

**Overall verdict: ALL ANCHORS MATCH — NO DRIFT DETECTED.** Downstream edit items (Phase 2/3) use the spec's original line numbers verbatim; no corrections required.

## `src/superclaude/cli/sprint/executor.py`

| Spec anchor | Expected | Actual line(s) | Verdict | Current code excerpt |
|---|---|---|---|---|
| 1777-1780 | global `ledger = TurnLedger(initial_budget=config.max_turns * len(config.active_phases), reimbursement_rate=0.8)` | 1777-1780 | MATCH | `ledger = TurnLedger(` @1777 / `initial_budget=config.max_turns * len(config.active_phases),` @1778 / `reimbursement_rate=0.8,` @1779 / `)` @1780 |
| 1782 | `shadow_metrics = ShadowGateMetrics()` | 1782 | MATCH | `shadow_metrics = ShadowGateMetrics()` |
| 1786-1788 | `remediation_log = DeferredRemediationLog(...)` | 1786-1788 | MATCH | `remediation_log = DeferredRemediationLog(` @1786 / `persist_path=config.results_dir / "remediation.json",` @1787 / `)` @1788 |
| 1793 | `SprintGatePolicy(config)` | 1793 | MATCH | `SprintGatePolicy(config)` |
| 1796 | `all_gate_results: list[TrailingGateResult] = []` | 1796 | MATCH | `all_gate_results: list[TrailingGateResult] = []` |
| 1813 | `for phase in config.active_phases:` | 1813 | MATCH | `for phase in config.active_phases:` |
| 1819-1820 | python `continue` | 1819-1820 | MATCH | `if phase.execution_mode == "python":` @1819 / `continue` @1820 |
| 1823-1834 | skip `continue` | 1823-1834 | MATCH | `if phase.execution_mode == "skip":` @1823 … `continue` @1834 |
| 1838 | `tasks = _parse_phase_tasks(phase, config)` | 1838 | MATCH | `tasks = _parse_phase_tasks(phase, config)` |
| 1839 | `if tasks:` | 1839 | MATCH | `if tasks:` |
| 1856-1867 (`ledger=` @1860) | `execute_phase_tasks(... ledger=ledger ...)` | 1856-1867, `ledger=ledger` @1860 | MATCH | `task_results, remaining, phase_gate_results = execute_phase_tasks(` @1856 / `ledger=ledger,` @1860 |
| 1911-1917 | task-path wiring hook `run_post_phase_wiring_hook(..., ledger=ledger, ...)` | 1911-1917, `ledger=ledger` @1915 | MATCH | `phase_result = run_post_phase_wiring_hook(` @1911 / `ledger=ledger,` @1915 / `)` @1917 — accumulator add-site = after 1917 |
| 2281-2287 (`ledger=ledger` @2285) | legacy-path wiring hook | 2281-2287, `ledger=ledger` @2285 | MATCH | `phase_result = run_post_phase_wiring_hook(` @2281 / `ledger=ledger,` @2285 / `)` @2287 — accumulator add-site = after 2287 |
| 2414-2418 (`turn_ledger=ledger` @2417) | post-loop `build_kpi_report(..., turn_ledger=ledger)` | 2414-2418, `turn_ledger=ledger` @2417 | MATCH | `kpi_report = build_kpi_report(` @2414 / `gate_results=all_gate_results,` @2415 / `remediation_log=remediation_log,` @2416 / `turn_ledger=ledger,` @2417 / `)` @2418 |
| 2419-2420 | `gate-kpi-report.md` write | 2419-2420 | MATCH | `kpi_path = config.results_dir / "gate-kpi-report.md"` @2419 / `kpi_path.write_text(kpi_report.format_report())` @2420 |
| 1125-1132 | reconciliation (debit/credit on actual) | 1125-1132 | MATCH | `with guard:` @1125 / `pre_allocated = ledger.minimum_allocation` @1128 / `ledger.debit(actual - pre_allocated)` @1130 / `ledger.credit(pre_allocated - actual)` @1132 |
| 1231-1235 | parallel gate `if ledger is not None and not ledger.try_launch():` → SKIPPED | 1231-1235 | MATCH | `if ledger is not None and not ledger.try_launch():` @1231 / `status=TaskStatus.SKIPPED,` @1235 |
| 1424-1430 | sequential gate → remaining + SKIPPED | 1424-1430 | MATCH | `if ledger is not None and not ledger.try_launch():` @1424 / `remaining = [t.task_id for t in tasks[i:]]` @1425 / `status=TaskStatus.SKIPPED,` @1430 |
| 1158 | `def _execute_phase_tasks_parallel(` | 1158 | MATCH | `def _execute_phase_tasks_parallel(` |
| 1206 | worker `def _worker(` | 1206 | MATCH | `def _worker(task, prior_context):` |
| 1288-1289 | wave join `with ThreadPoolExecutor(...) as pool` | 1288-1289 | MATCH | `with ThreadPoolExecutor(max_workers=k) as pool:` @1288 / `wave_out = list(pool.map(lambda t: _worker(t, prior_context), wave_tasks))` @1289 |
| 1300 | parallel return | 1300 | MATCH | `return results, remaining, gate_results` @1300 |

## `src/superclaude/cli/sprint/models.py`

| Spec anchor | Expected | Actual line(s) | Verdict | Current code excerpt |
|---|---|---|---|---|
| 1011-1124 | `TurnLedger` class span | 1011-1124 | MATCH | `@dataclass` @1011 / `class TurnLedger:` @1012 … `can_run_wiring_gate` ends @1124 |
| 1011-1022 | class docstring (R-7 touch-up target) | 1013-1022 | MATCH | docstring `"""Economic model for subprocess turn budget tracking. …"""` @1013-1022 |
| 1024-1034 | field defaults | 1024-1034 | MATCH | `initial_budget: int` @1024 … `wiring_analyses_count: int = 0` @1034 |
| 1036-1042 | `__post_init__` RLock | 1036-1042 | MATCH | `def __post_init__` @1036 / `self._lock = threading.RLock()` @1042 |
| 1044-1046 | `available()` | 1044-1046 | MATCH | `return self.initial_budget - self.consumed + self.reimbursed` @1046 |
| 1048-1053 | `debit` monotonicity | 1048-1053 | MATCH | `def debit(self, turns: int)` @1048 / `self.consumed += turns` @1053 |
| 1066-1081 | `try_launch` | 1066-1081 | MATCH | `def try_launch(self, allocation: int | None = None) -> bool:` @1066 / `self.debit(debit_amount)` @1080 / `return True` @1081 |
| 1120-1124 | `can_run_wiring_gate` | 1120-1124 | MATCH | `def can_run_wiring_gate(self) -> bool:` @1120 / `return self.available() >= self.minimum_remediation_budget` @1124 |
| (R-7/TM-6) | NO `reset` / NO `reallocate` method | n/a | MATCH (absent) | Methods present: `__post_init__`, `available`, `debit`, `credit`, `can_launch`, `try_launch`, `can_remediate`, `debit_wiring`, `credit_wiring`, `can_run_wiring_gate`. No `reset`/`reallocate`. |

## `src/superclaude/cli/sprint/kpi.py`

| Spec anchor | Expected | Actual line(s) | Verdict | Current code excerpt |
|---|---|---|---|---|
| 151-158 (`turn_ledger` @156) | `build_kpi_report` signature | 151-158, `turn_ledger` @156 | MATCH | `def build_kpi_report(` @151 / `turn_ledger: TurnLedger | None = None,` @156 / `) -> GateKPIReport:` @158 |
| 192-197 | wiring reader | 192-197 | MATCH | `if turn_ledger is not None:` @192 / `report.wiring_turns_used = turn_ledger.wiring_turns_used` @193 / `report.wiring_turns_credited = max(0, turn_ledger.wiring_turns_credited)` @195 / `report.wiring_analyses_run = turn_ledger.wiring_analyses_count` @197 |

**Accumulator read contract (R-10):** the object passed as `turn_ledger=` to `build_kpi_report` MUST expose attributes `wiring_turns_used`, `wiring_turns_credited`, `wiring_analyses_count` (read at kpi.py:193/195/197). The Step 2.2 accumulator is shaped to exactly these three names.

## `src/superclaude/cli/sprint/commands.py`

| Spec anchor | Expected | Actual line(s) | Verdict | Current code excerpt |
|---|---|---|---|---|
| ~88-92 | `--max-turns` help "Max agent turns per phase" (C1 — UNCHANGED) | 88-93, help @92 | MATCH | `@click.option(` @88 / `"--max-turns",` @89 / `help="Max agent turns per phase (default: 100)",` @92 |

## Summary

All 30 spec anchors across the four source files MATCH their spec-described locations and code shape as of 2026-06-18 in the `perPhaseturnBudget` worktree. **No anchor is DRIFTED.** No corrected line numbers are needed; Phase 2/3 edit items proceed against the spec's original anchors. Per Critical Rule, each edit item will still re-Read its anchor immediately before editing.

