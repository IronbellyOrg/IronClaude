# NFR4 Escalation Decision — PR3

**Trigger:** Step 2.2 NFR4 token-budget gate
**Total renames:** 79 (exceeds 40 threshold)
**Reference:** Task file Step 2.2 line 158 and Task Overview line 71

## Discovery breakdown (47 unique files)

| Rule | Count | Mechanical action |
|------|------:|-------------------|
| F841 | 45 | Delete unused local; if RHS is a side-effect call, drop the `result =` assignment but keep the call |
| N806 | 20 | UPPERCASE → lowercase_with_underscores |
| E741 | 11 | `l` → `level` (per brainstorm spec) for budget.py; case-by-case elsewhere |
| N811 | 3 | `from X import lc as UPPER` → `from X import lc` (drop alias) |

(F811 originally 2, now 0 — cleared by PR2's ruff format sweep.)

## Why we exceeded the threshold

The original task spec projected ~36 manual edits. F841 (45 violations) was routed to PR3 at PR1 execution time per user decision (PR1 ruff `--fix` could not safely auto-remove the F841 instances because of side-effect risk). The amended description/title at the top of this task file reflects the projected ~81, and the actual count from discovery is 79.

## Options for user

**A. Bundle (recommended given pre-decision context)** — Override NFR4, proceed with all 79 renames in one PR3. Rationale: the user pre-decided F841 routing knowing scope would expand. F841 deletions are mechanical (delete one line per violation) and inflate the count without proportionally inflating reviewer cognitive load. Estimated token cost: high but bounded by mechanical nature.

**B. Split PR3a (E741+N806+N811 = 34) and PR3b (F841 = 45)** — Honor NFR4. PR3a stays under the threshold and ships the rename work. PR3b ships the F841 deletions separately. Cleaner per-rule history but adds one more PR to the sequence (now 6 PRs total).

**C. Split PR3a (E741 = 11) and PR3b (N806+N811+F841 = 68)** — Isolate the budget.py-heavy E741 work that requires per-rename behavioral verification. Less attractive because N806/N811/F841 mix doesn't have a clean conceptual boundary.

**D. Continue with stricter strategy: skip F841 for now, defer to PR3c after PR4** — Reduces this PR to 34 (under threshold). Defers the F841 work past PR4 (test fixture repair). Risk: leaves AC1 incomplete after PR3.

## Recommendation: Option A

User has already made the macro-decision (route F841 to PR3 knowing scope would grow). NFR4's 40-threshold was set when projected scope was ~36 — the threshold is now stale. Override is principled, not lazy. F841 mechanical-deletion adds ~5min execution time, not the human-judgment cost the threshold was protecting against.

Awaiting user direction.
