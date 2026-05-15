# Solution S4 — TurnLedger Observability & Refund Rules (Refactored)

> **Status after adversarial review:** the original S4 was largely
> misdiagnosed. The observed `available=35` is *not* an anomaly — it is
> `61 - 46 + 20` where the 20 is a `reimburse_for_progress` credit that
> already fires on Run 3 (delta=5 structural HIGHs, rate=0.8,
> `CONVERGENCE_PASS_CREDIT=5` → `int(5 * 5 * 0.8) = 20`). Budget is **not
> the binding constraint** of the failing run; `max_runs=3` is. This
> refactor narrows the scope accordingly.

## Target root cause (corrected)

**Not** "budget too small." **Not** "no refund on rollback."

The actual contributions S4 can defensibly make:

1. **Observability defect:** the per-run `budget_snapshot` written to
   `deviation-registry.json` is captured immediately after the checker
   debit (convergence.py:469-475) and **before** `reimburse_for_progress`
   at line 560. Readers cannot reconstruct the final ledger from the
   registry alone. The halt message (`available=35`) and the structural
   progress log (`available=15`) disagree by exactly the credit amount,
   which makes the system look broken when it isn't.
2. **Refund policy gap:** `REMEDIATION_COST=8` is debited unconditionally
   even when the validator forces a *full rollback*. Today this is a
   non-issue (validator rollbacks are rare on this codepath), but the
   policy is the wrong default and will bite when regression validation
   becomes more aggressive.
3. **`MAX_CONVERGENCE_BUDGET=61` is misnamed.** The three-cycle minimum
   cost path is `10+8+10+8+10 = 46`. 61 is the comfortable budget that
   leaves room for *one* `REGRESSION_VALIDATION_COST=15` excursion, not
   three full cycles. The constant name lies to its readers.

## Reconciled math

| Step | consumed | reimbursed | available |
|------|----------|------------|-----------|
| Start | 0 | 0 | 61 |
| Run 1 checker | 10 | 0 | 51 |
| Run 1 remediation | 18 | 0 | 43 |
| Run 2 checker | 28 | 0 | 33 |
| Run 2 remediation | 36 | 0 | 25 |
| Run 3 checker | 46 | 0 | 15 |
| Run 3 progress credit (delta=5) | 46 | 20 | **35** |

`int(CONVERGENCE_PASS_CREDIT * delta * reimbursement_rate)`
= `int(5 * 5 * 0.8)` = `20`. Matches the printed halt value exactly.

## Proposal (narrowed)

### 1. Dual budget snapshot per run

Capture **both** snapshots in `DeviationRegistry.runs[-1]`:

```python
registry.runs[-1]["budget_snapshot"] = { ... }            # post-debit
# ... after reimburse_for_progress ...
registry.runs[-1]["budget_snapshot_final"] = {            # post-credit
    "consumed": ledger.consumed,
    "reimbursed": ledger.reimbursed,
    "available": ledger.available(),
}
```

Halt-message and registry then tell the same story.

### 2. Refund on **full-rollback only**

Extend the remediation callback contract:

```python
class RemediationOutcome(IntEnum):
    NOOP = 0           # nothing to do
    PARTIAL = 1        # some patches applied
    FULL_APPLY = 2     # all patches applied
    FULL_ROLLBACK = 3  # patches generated but rejected by validator
```

Refund rule:

```python
if outcome == RemediationOutcome.FULL_ROLLBACK:
    ledger.credit(REMEDIATION_COST)
    refunds_this_run += 1
```

**Hard cap:** at most one refund per convergence run, to block any
adversarial remediator that could otherwise loop on rollbacks.

**Explicitly rejected:**

- Refunding on NOOP — pays the remediator for doing nothing.
- Linear refund on PARTIAL — rewards trying, not succeeding.

### 3. Rename and re-derive budget constants

```python
# Minimum cost of 3-cycle convergence (no regression validation):
MIN_CONVERGENCE_BUDGET = 28   # 1 checker + 1 remediate + 1 regression-check
STD_CONVERGENCE_BUDGET = 46   # 3 full cycles, no regression validation
MAX_CONVERGENCE_BUDGET = 76   # 46 + 2*15 (room for two regression passes)
```

If `initial_budget < STD_CONVERGENCE_BUDGET` emit a config warning at
loop entry. Current `61` becomes a cushion value, not a "max."

## Risks / downsides

- **Adds a field to `budget_snapshot`** — readers that depend on the
  exact shape need migration. Schema bump from 1 → 2.
- **Remediator contract change** — every caller of `run_remediation`
  must return a `RemediationOutcome`. Mitigated by a default-to-`NOOP`
  shim for legacy callers.
- **Refund cap=1** is arbitrary; if rollbacks become routine we may
  need to tune it.

## Expected impact on the failing case

**Zero on convergence pass/fail.** The 10 stuck HIGHs are spec-manifest
mismatches that no budget logic addresses. S4 alone does not fix the
failing run.

**What S4 does fix:**

- Operators reading the deviation-registry see the post-credit ledger
  state, removing the "consumed=46 yet available=35" confusion.
- When a real fix (S1/S2/S3 etc.) lands and rollbacks become possible,
  the budget accounts honestly.
- Constant names match what the code actually allows.

S4 is a **complement** to whatever solution addresses the real
remediation-target gap. Without that fix, S4 changes diagnostics only.

## Estimated effort

- Code: ~30 LOC in `convergence.py` + ~15 LOC in remediator call sites
- Tests: 4 new tests (dual-snapshot, refund-only-on-rollback,
  refund-cap-enforcement, constant warning)
- Time: 60 min

## Files touched

- `src/superclaude/cli/roadmap/convergence.py`
- `src/superclaude/cli/roadmap/remediate_executor.py`
- `tests/cli/roadmap/test_convergence.py`

## Confidence scores

- **Standalone confidence S4 fixes the failing run:** 25%
  (it doesn't — it fixes observability and a latent refund bug)
- **Combined with real fix (S1/S2/S3):** 70%
  (improves diagnostics, prevents budget false-halts under regression
  validation, makes the constants honest)
