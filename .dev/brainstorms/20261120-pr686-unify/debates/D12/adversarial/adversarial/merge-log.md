# Merge Log: D12

## Metadata
- Base: Variant 1 (OURS), `variant-1-original.md`
- Executor: `merge-executor` agent (Agent tool), plan `refactor-plan.md`
- Merged output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D12/adversarial/merged-d12-position.md` (137 lines)
- Changes planned: 9; applied: 9; failed: 0; skipped: 0 (C6 and C7 are applied as recorded deferrals, C8 as an owner decision)
- Status: partial (five HIGH invariant findings carried as safeguards S1 to S5, not debated further at depth standard)
- Timestamp: 2026-11-20

## Changes Applied

| # | Change | Status | Provenance tag in the merged file | Note |
|---|---|---|---|---|
| C1 | Claim reads the plan sections (rule with S1 to S5) | Applied | Base (original, modified); Variant 2 points 2 and 3 | Widens the base's one-line concession |
| C2 | Keep PR 661 | Applied | Base (original, modified) | No change to PR 661 |
| C3 | Keep-adapt PR 690 | Applied | Variant 2, Mechanism and Cited facts 4 to 6 | Overrides the base's "hold back `--remaining`"; base risk kept as residual risk |
| C4 | `--mode other` and forms as a separate PR | Applied | Variant 2, Cited facts 7 | |
| C5 | Split refusal guard | Applied | Base (original, modified) | Base's flat refusal rejection softened |
| C6 | Higher create tier for medium and complex | Applied as deferral | Variant 2, Cited facts 7 | Needs a cost baseline |
| C7 | Defer rename | Applied as deferral | Variant 2, Cited facts 8 | |
| C8 | Brainstorm and design at create is an owner decision | Applied | Base (original, modified) | "Ruling of 2026-11-20" marked UNVERIFIED |
| C9 | Chain tests move with C1 | Applied | Base (original, modified) | |

Merge-executor judgment calls recorded: fact 10's `create.md:61` quote was taken from the plan (the orchestrator then confirmed it on master: line 61 reads "so an issue arrives with its plan already written and whoever picks it up only executes"); fact 13's "design partly unpushed" comes from the transcript's U-007 row; facts 12 and 14 carry Variant 2 material (sandbox run, tier and label asymmetries) that the plan did not list; INV, C- and U- identifiers were not re-checked by the executor (the orchestrator checked them against `invariant-probe.md` and `diff-analysis.md`).

## Post-Merge Validation

- Structural integrity: pass. One H1, H2 sections in the base order (Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right, Resulting disposition), H3 only under "Resulting disposition".
- Internal references: pass. Points 1 to 15 exist; the "point N" references (points 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15) all resolve; change ids C1 to C9 and S1 to S5 resolve.
- Contradiction re-scan: no new contradiction against the plan. One conflict was found and reconciled in the document: the base held `--remaining` back, the plan keeps it (C3).
- Dashes: no em or en dashes (orchestrator grep, 0 matches in the merged file and all artifacts).
- Placeholders: none left in the merged file.

## Summary
- Planned 9, applied 9, failed 0, skipped 0.
- Residual: five HIGH invariant findings (INV-001, INV-002, INV-004, INV-005, INV-006) are conditions of C1, not resolved by a further debate round.
