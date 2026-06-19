# K-3 Pre-Merge Consumer Grep — Structured Summary (Step 3.2)

**Task:** TASK-RF-per-phase-turn-budget-20260618-160752
**Date:** 2026-06-18
**Command:** `grep -rn "\.wiring_turns\|\.wiring_analyses\|turn_ledger=" src/superclaude/cli/sprint`
**Raw output:** `phase-outputs/discovery/k3-premerge-grep.txt`

**Spec D-2 inventory (review-time baseline):** the ONLY post-loop ledger-wiring consumer is `kpi.py:192-197`, reached via the post-loop `build_kpi_report(..., turn_ledger=...)` call at `executor.py:2417` (now `2543` after Phase 2 edits). Known in-function `ledger`-param readers `executor.py:390`/`949` take the ledger as a parameter and do NOT match this grep pattern (no `.wiring_turns`/`.wiring_analyses`/`turn_ledger=` token), so their absence here is expected.

## Classification (22 hits)

| File:line | Match | Classification | Rationale |
|---|---|---|---|
| kpi.py:63 | `return self.wiring_turns_used - self.wiring_turns_credited` | EXPECTED | `GateKPIReport` internal `net` computation reading the REPORT's OWN fields (`self.`), not a `TurnLedger`. Downstream of the report, not a ledger consumer. |
| kpi.py:140 | `f"  Turns used:       {self.wiring_turns_used}"` | EXPECTED | Report `format_report()` rendering the report's own field. Not a ledger consumer. |
| kpi.py:141 | `f"  Turns credited:   {self.wiring_turns_credited}"` | EXPECTED | Report `format_report()` rendering. Not a ledger consumer. |
| kpi.py:143 | `f"  Analyses run:     {self.wiring_analyses_run}"` | EXPECTED | Report `format_report()` rendering. Not a ledger consumer. |
| kpi.py:193 | `report.wiring_turns_used = turn_ledger.wiring_turns_used` | EXPECTED | THE D-2 post-loop reader (`kpi.py:192-197`), reached via `executor.py:2543`. Now fed the sprint accumulator (R-10). |
| kpi.py:195 | `report.wiring_turns_credited = max(0, turn_ledger.wiring_turns_credited)` | EXPECTED | Same D-2 post-loop reader. |
| kpi.py:197 | `report.wiring_analyses_run = turn_ledger.wiring_analyses_count` | EXPECTED | Same D-2 post-loop reader. |
| models.py:1105 | `self.wiring_turns_used += turns` | EXPECTED | `TurnLedger.debit_wiring` — the model's OWN WRITER (source of the wiring fields), not a consumer. Unchanged by this task. |
| models.py:1106 | `self.wiring_analyses_count += 1` | EXPECTED | `TurnLedger.debit_wiring` writer. Unchanged. |
| models.py:1125 | `self.wiring_turns_credited += credit_amount` | EXPECTED | `TurnLedger.credit_wiring` writer. Unchanged. |
| executor.py:352 | `... build_kpi_report(..., turn_ledger=...)` (docstring) | EXPECTED | Docstring text of the `_SprintWiringTotals` accumulator (Step 2.2). Comment/docstring, not executable consumer. |
| executor.py:2009 | `sprint_wiring_totals.wiring_turns_used += ledger.wiring_turns_used` | EXPECTED | R-10 task-path add-site (Step 2.6). Read-only summation INTO the accumulator. |
| executor.py:2010-2011 | `sprint_wiring_totals.wiring_turns_credited += (ledger.wiring_turns_credited)` | EXPECTED | R-10 task-path add-site (Step 2.6). |
| executor.py:2013-2014 | `sprint_wiring_totals.wiring_analyses_count += (ledger.wiring_analyses_count)` | EXPECTED | R-10 task-path add-site (Step 2.6). |
| executor.py:2400 | `sprint_wiring_totals.wiring_turns_used += ledger.wiring_turns_used` | EXPECTED | R-10 legacy-path add-site (Step 2.6). |
| executor.py:2401-2402 | `sprint_wiring_totals.wiring_turns_credited += (ledger.wiring_turns_credited)` | EXPECTED | R-10 legacy-path add-site (Step 2.6). |
| executor.py:2404-2405 | `sprint_wiring_totals.wiring_analyses_count += (ledger.wiring_analyses_count)` | EXPECTED | R-10 legacy-path add-site (Step 2.6). |
| executor.py:2543 | `turn_ledger=sprint_wiring_totals` | EXPECTED | R-10 arg-swap (Step 2.7). Passes the accumulator (not last-phase ledger) to `build_kpi_report`. |

## Verdict

**K-3 clean — only expected consumers present.** Every one of the 22 grep hits is accounted for against the spec's D-2 inventory:
- The single post-loop ledger-wiring consumer remains `kpi.py:192-197` (via `executor.py:2543`), now correctly fed the R-10 sprint accumulator.
- kpi.py:63/140/141/143 are the `GateKPIReport`'s own internal field reads (net + formatting), not ledger consumers.
- models.py:1105/1106/1125 are the `TurnLedger`'s own writers (`debit_wiring`/`credit_wiring`), unchanged by this task.
- executor.py:2009–2014 / 2400–2405 are the two R-10 add-sites this task added; executor.py:2543 is the R-10 arg-swap; executor.py:352 is the accumulator docstring.

**No UNEXPECTED-NEW-CONSUMER found.** No new ledger-wiring consumer has been added since the review that the R-10 accumulator does not feed. No K-3 blocker. (Per K-3 guidance, this grep must be re-run immediately before the actual merge to catch any consumer added between now and merge time.)
