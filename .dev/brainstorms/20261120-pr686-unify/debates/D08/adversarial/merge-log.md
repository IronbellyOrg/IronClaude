# Merge Log (D08)

## Metadata
- Base: Variant 1 (OURS)
- Executor: the D08 debate session (no separate merge-executor agent was spawned; the merge is a short document)
- Changes applied: 6 of 6 planned, plus 5 corrections
- Status: success with notes
- Timestamp: 2026-11-20

## Changes Applied
| # | Status | Result | Provenance tag |
|---|---|---|---|
| 1 | applied | Flags `--wake --hourly --resume --take --sub` under "Command, skill, session, tag" | Variant 2, D:133 |
| 2 | applied | Species table with "person-opened coordinator" and "standing-grant coordinator" | Variant 2, D:799 |
| 3 | applied | Report coordinator, deployed names unchanged | Variant 2 |
| 4 | applied | "Orchestrated issue flow" and "Orchestration" | Variant 2, ADD1 |
| 5 | applied | Nesting table | Variant 2 / Advocate tables |
| 6 | applied | "Persisted names renamed before PR 686 merges" | Variant 2 weakness 7 |
| corrections 1 to 5 | applied | "Corrections carried over" section | Base modified |

## Post-Merge Validation
- Structure: headings H1 then H2 only; no gaps. Pass.
- Internal references: no section references; 0 broken.
- Contradictions: one added by the merge was found and fixed in this pass: the plan kept `IronOrchestrator` and `orchestrator_repo`, but D07 (a separate verdict in the same run, `debates/D07/VERDICT.md` item 2) removes the registry repo. The merged text now says they go too if D07 stands. New contradictions left: 0.
- Added beyond the plan: the invariant resolution (authority from a recorded authorization only) and the branch note `Coordinator` versus `coordinators`, from the probe (INV-001, INV-004).

## Summary
Planned 6, applied 6, failed 0, skipped 0.
