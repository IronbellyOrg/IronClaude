# Cycle-2 decision (item 14.32)

Inputs: `cycle1-decision.md` (F_1 = {FIN-F5, FIN-F7}), `verify-cycle2-rf-qa.md` (Verdict: FAIL, Blocking count: 1), `verify-cycle2-rf-qa-qualitative.md` (Verdict: FAIL, Blocking count: 1), `fix-log-cycle1.md`, `fix-log-cycle2.md` and `cycle-ledger.md` (the cycle-1 PASS set: the re-check row, 238 ids).

## F_2 and the cycle-2 PASS set

- Marked OPEN by either cycle-2 verifier: FIN-F7 (both). FIN-F5 is RESOLVED in both. New BLOCKING or MAJOR findings: none.
- `F_2` = {FIN-F7}
- `|F_2|` = 1
- Cycle-2 PASS set: 238 check ids, every check id of the cycle-1 PASS set, each marked PASS by both cycle-2 verifiers; listed in the cycle-2 row of `cycle-ledger.md`.

## Checks, in order

- (a) Regression: no check id of the cycle-1 PASS set is FAIL in either cycle-2 report (0 FAIL rows; all 238 ids present in both). Does not apply.
- (b) Monotonicity: `|F_2|` is 1, below `|F_1|` of 2. Does not apply.
- (c) `|F_2|` is not 0, so `Final gate: PASS at cycle 2` does not apply.
- (d) Hard cap (two fix cycles used): applies.

## Outcome

Final gate: HALT after 2 fix cycles, open findings: FIN-F7
## Resolution

The hard-cap halt was resolved by the owner's ruling of 2026-11-12 on FIN-F7 (`phase-outputs/plans/FINAL-GATE-FIN-F7-ruling.md`): a documented limitation. See `gate-decision.md`.
