# Final gate, item 14.28 halt: owner decision (2026-11-12)

Status: RESOLVED by the owner. Chosen: approve all three changes.

## Context

Item 14.28 (cycle-1 decision of the final QA gate) halted on its regression rule: six check ids that passed at cycle 0 failed in a cycle-1 verifier report (`qa/final/cycle1-decision.md`, `qa/final/verify-cycle1-rf-qa.md`, `qa/final/verify-cycle1-rf-qa-qualitative.md`). Causes: (1) the FIN-F7 fix made `SKILL.md` step 3 read `orca_available`, against DESIGN 7.6 `:662` and the revision addendum `:29` (finding FIN-N1; checks design-conformance C13 and C22, completeness C4); (2) DESIGN `:491` says the Rule 5 field names were "captured at step 1.0a" (they were not: `phase-outputs/discovery/1.0a-facts.md` rows 6, lines 16 and 35) while DESIGN open item 6 `:996` says Rule 5 cannot match until they are, and DESIGN `:760` still requires the tests to reach every class (finding FIN-N2; checks design-conformance C5 and test-traceability C8); (3) two code comments still said `parse_worker_show` parses the wait time (finding FIN-N3; check maintainability C9).

The orchestrator evaluated lifting the halt against fixing the cause and recommended fixing the cause.

## Owner's words

"All 3 approved" (answering the options: approve all three, approve only 1 and 3, or lift the halt).

## The three approved changes

1. Revert the FIN-F7 edit of `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (step 3 and the step 4 outage and exempt-reply sentences) and move its pins in `tests/commands/test_sweep_command.py` back (the three FIN-F7 tests and the `_OUTAGE_SENTENCE` and `_EXEMPT_ALONE_SENTENCE` constants are removed; the step 3 pin reads `success-parse-takes-only-report-path-and-summary` again). FIN-F7 is then OPEN as a whole, next to FIN-F5, and both go to the follow-up issue.
2. Edit DESIGN `docs/designs/orchestrator-mode.md` line 491 to say that Rule 5 stays inert (returns None, rows fall to the fallback) until open item 6 closes, keeping its four conditions listed, and that the `worker-show` names are not yet captured; edit line 760 (the `test_classify.py` row) to match (the `working` case expects the fallback rule; every class but `working` is reached; the Rule 5 case pins "never matches while uncaptured").
3. Fix the two stale comments (`models.py` `agent_wait_since`, `classify.py` `_rule_waiting_signal`) and mark the three unused model fields as reserved.

## Consequences recorded

- DESIGN is edited by the owner's decision, not by the fix agent. Its sha256 baseline in the cycle-1 fix log is superseded by the sums recorded in the "Halt resolution" section of `qa/final/fix-log-cycle1.md`. The base copy `artifacts/design-base.md` is unchanged.
- DESIGN section 13 is not changed (no deviation row added, so the "Total: 10 deviations" count stays).
- Both cycle-1 verifiers run again over the repaired tree; item 14.28 is evaluated on those re-check reports. The first reports and the halted decision are kept as `qa/final/verify-cycle1-rf-qa.md`, `qa/final/verify-cycle1-rf-qa-qualitative.md` and `qa/final/cycle1-decision-halted.md`.
