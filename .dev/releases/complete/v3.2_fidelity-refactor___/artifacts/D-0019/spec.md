# D-0019: KPI Report Extensions (T03.01)

## Implementation Summary

All 6 wiring KPI fields implemented in `src/superclaude/cli/sprint/kpi.py`:

1. `wiring_findings_total` — populated from `WiringReport.total_findings`
2. `wiring_findings_by_type` — dict built from `WiringReport.all_findings` by `finding_type`
3. `wiring_turns_used` — populated from `TurnLedger.wiring_turns_used`
4. `wiring_turns_credited` — populated from `TurnLedger.wiring_turns_credited` with floor-to-zero (R7)
5. `whitelist_entries_applied` — count of suppressed findings from `WiringReport.all_findings`
6. `files_skipped` — populated from `WiringReport.files_skipped`

## Signature Update

`build_kpi_report()` accepts optional `turn_ledger: TurnLedger | None` and `wiring_report: WiringReport | None` parameters. Existing callers are unaffected (backward-compatible defaults to `None`).

## Floor-to-Zero Credit (R7)

`wiring_turns_credited` uses `max(0, turn_ledger.wiring_turns_credited)` ensuring credits never go negative.

## Verification

- **SC-015 validated**: All 6 fields present and correctly populated
- **Tests**: 24/24 passed (`tests/sprint/test_kpi_report.py`)
- **Test class**: `TestWiringKPIFields` covers all 6 fields, floor-to-zero, combined data, and format output
