# Decisions gate decision (item 7.37)

Inputs: `qa/decisions/fix-log-cycle1.md` (a fix log was written, not SKIPPED), `qa/decisions/cycle1-decision.md` (outcome line `PASS at cycle 1`, line 29) and `qa/decisions/cycle-ledger.md` (cycle-1 row, outcome `PASS at cycle 1`).

The cycle-1 outcome is `PASS at cycle 1`, so the cycle-2 branch (F_2, regression, monotonicity and hard-cap checks) is not run, and items 7.34 to 7.36 are marked complete as SKIPPED.

Decisions gate: PASS

Records that stay on the books for later items (none blocks the gate):
- The DEC-F5 remainder (stale Orca build suffix `780594c521aa` at DESIGN `docs/designs/orchestrator-mode.md:30` and `:761` and in the text of item 10.5 at task file line 1812; item 8.12 does not carry the string but has no pointer to the facts-file version rule) was accepted by the owner as a minor note on 2026-11-12 (Ryan Wiancko, owner, "Accept as a minor note (Recommended)", recorded in `fix-log-cycle1.md`, last section). The follow-up for the builders of items 8.12 and 10.5 is at `phase-outputs/discovery/1.0a-facts.md:46-48`.
- OQ-1 (R5) was confirmed directly by the owner on 2026-11-12 (`phase-outputs/plans/OQ-1-agent-wait-decision.md:23`).
- The two cycle-1 checks that stay FAIL (`qa-completeness:C21`, `qa-readonly-safety:C20`) are MINOR-only and were FAIL at cycle 0.
