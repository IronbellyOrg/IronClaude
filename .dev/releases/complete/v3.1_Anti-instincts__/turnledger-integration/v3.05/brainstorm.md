# v3.05 TurnLedger Integration Brainstorm

Ranked by disruption, lowest first.

## 1. Proposal: Ledger-Backed Convergence Shim

**Summary**: Keep the existing three-run convergence contract intact, but represent each fidelity run as a `TurnLedger` debit/credit cycle so v3.05 stops owning a separate custom budget model.

### FR sections that change
- **FR-7 Convergence Gate**: Replace the bespoke "hard budget = maximum 3 runs" implementation language with a ledger-backed run budget.
- **FR-7.1 FR-7/FR-8 Interface Contract**: Clarify that regression validation plus its remediation is debited as one ledger unit.
- **FR-10 Run-to-Run Memory**: Add ledger snapshots to the run metadata/reporting so reimbursement decisions are auditable.

### TurnLedger reuse vs extension
**Reused as-is**
- `initial_budget`: becomes the convergence run budget, initialized to `3`.
- `consumed`: increments once per fidelity run attempt.
- `reimbursed`: stores credited run capacity after a successful/clean run.
- `reimbursement_rate`: defines how much of a spent run is returned after success.
- `available()`: replaces bespoke remaining-run arithmetic.
- `debit()`: called when a convergence run starts.
- `credit()`: called when a run earns reimbursement.

**Extended lightly**
- Add a small adapter/helper in roadmap code, e.g. `credit_run_pass(ledger, turns=1)`, to centralize rounding semantics for run-budget reimbursement.
- Optionally add run-oriented aliases or helper docs so roadmap code does not read like task subprocess code.

### Meaning of `reimbursement_rate` in fidelity context
- A run that reaches a **clean convergence outcome** earns credit back.
- With `initial_budget=3` and `reimbursement_rate=0.8`, a passed run that debits `1` would credit back `0` if strict integer flooring is preserved, so this proposal likely needs one of two clarifications:
  - store convergence budget in **tenths** (e.g. budget `30`, each run costs `10`, clean run credits `8`), or
  - define a small roadmap-specific helper that accumulates fractional credit until it rounds to a full run unit.
- In practical terms, the spec meaning would be: **a run that resolves all active HIGHs or completes a remediation/verification cycle without structural regression earns 80% of a run back toward the three-run ceiling**.

### Risk assessment
- **Low disruption**, because FR-7 semantics mostly stay the same and only the accounting substrate changes.
- The main breakage risk is **unit mismatch**: `TurnLedger` today assumes integer turn counts and sprint-style minimum thresholds (`minimum_allocation=5`, `minimum_remediation_budget=3`), which do not map cleanly to three convergence runs.
- If rounding is handled poorly, reimbursement becomes a no-op and the integration looks wired but functionally meaningless.
- Reporting/UI text that currently speaks in "runs" may become confusing if raw ledger numbers leak through.

---

## 2. Proposal: Unified Remediation Economy

**Summary**: Make the fidelity loop and trailing-gate remediation share one `TurnLedger`, so run attempts, regression handling, and deferred remediation all draw from the same reimbursable budget model.

### FR sections that change
- **FR-7 Convergence Gate**: Replace the isolated three-run budget with a shared ledger governing runs plus intra-loop remediation.
- **FR-7.1 FR-7/FR-8 Interface Contract**: Redefine the "regression validation + remediation = 1 budget unit" rule in ledger terms.
- **FR-8 Regression Detection & Parallel Validation**: Specify ledger charging for the parallel validation bundle and its follow-up remediation.
- **FR-9 Edit-Only Remediation with Diff-Size Guard**: Align remediation charging with `attempt_remediation()` semantics instead of a custom convergence-only budget.

### TurnLedger reuse vs extension
**Reused as-is**
- `available()`, `debit()`, `credit()` as the single accounting API.
- `can_remediate()` as the canonical gate before remediation attempts.
- `minimum_remediation_budget` as the threshold for whether the loop can afford another remediation cycle.

**Extended**
- Add a roadmap-specific budget profile, e.g. `TurnLedger(initial_budget=30, minimum_allocation=10, minimum_remediation_budget=10)` so one run maps to `10` units and reimbursement can actually return `8`.
- Extend `attempt_remediation()` call sites, or add a roadmap wrapper, so successful remediation can optionally trigger reimbursement when the associated gate passes.
- Add explicit ledger event logging to `DeferredRemediationLog`/diagnostics so post-failure analysis can explain where budget went.

### Meaning of `reimbursement_rate` in fidelity context
- `reimbursement_rate=0.8` means **a successful gate pass reimburses 80% of the run/remediation bundle that produced the pass**.
- Example: debit `10` for a verify run, then if that run leaves the registry at zero active HIGHs or validates a monotonic clean state, credit `8`.
- A clean convergence run therefore behaves like a mostly refundable verification pass, while failed runs remain fully consumed.
- Persistent failures in `attempt_remediation()` still consume both attempts with **no reimbursement**, matching current trailing-gate semantics.

### Risk assessment
- **Medium disruption** because it changes not just FR-7 accounting but also the contract around remediation and regression handling.
- The good news is that it matches existing test intent: `tests/pipeline/test_full_flow.py` already models "pass gate -> credit 80%" while production code never applies that reimbursement.
- The biggest breakage risk is policy confusion: v3.05 currently states that convergence mode and legacy remediation budgeting **must never overlap**. This proposal deliberately collapses those two worlds, so the spec language in FR-7 would need rewriting rather than a small patch.
- Trailing-gate code currently only **debits** in `attempt_remediation()`; adding reimbursement changes failure analysis, diagnostics, and potentially test expectations across sprint/pipeline code.

---

## 3. Proposal: TurnLedger as Registry Currency

**Summary**: Promote `TurnLedger` from a budget helper into the canonical convergence accounting object, with registry updates, regression handling, and pass/fail authority all expressed in reimbursable ledger events instead of bespoke run counters.

### FR sections that change
- **FR-6 Deviation Registry**: Add ledger state or ledger event history to run metadata so budget and findings are tracked together.
- **FR-7 Convergence Gate**: Rewrite the hard-budget model around ledger state rather than a fixed custom three-run controller.
- **FR-7.1 FR-7/FR-8 Interface Contract**: Make FR-8 return ledger impact alongside validated findings.
- **FR-8 Regression Detection & Parallel Validation**: Charge the whole validation swarm as a ledger event, with reimbursement tied to validated regression outcomes.
- **FR-9 Edit-Only Remediation with Diff-Size Guard**: Make patch application success/failure feed ledger reimbursement rules.
- **FR-10 Run-to-Run Memory**: Prior runs now carry both finding history and economic history.

### TurnLedger reuse vs extension
**Reused as-is**
- Core accounting primitives: `debit()`, `credit()`, `available()`.
- `reimbursement_rate` remains the policy knob for earned credit.

**Extended heavily**
- Add ledger serialization support or an adjacent `LedgerEvent` dataclass for registry persistence.
- Add named debit/credit reasons, e.g. `run_start`, `regression_validation`, `clean_pass`, `semantic_high_downgraded`, `persistent_failure`.
- Add roadmap-specific helper methods such as `charge_run()`, `charge_regression_bundle()`, and `credit_clean_convergence()`.
- Potentially split thresholds away from sprint defaults so `minimum_allocation` / `minimum_remediation_budget` can be expressed in fidelity-native units.

### Meaning of `reimbursement_rate` in fidelity context
- `reimbursement_rate` becomes the **trust coefficient** for convergence evidence.
- A clean convergence run, or a regression-validation cycle that proves the system did not truly regress, earns back 80% of its debit because it produced reusable certainty rather than wasted exploration.
- Failed remediation, confirmed regressions, or semantic HIGHs that survive debate consume full cost with no refund.
- This reframes reimbursement as "confidence earned by deterministic fidelity evidence," not just "unused turns returned."

### Risk assessment
- **Highest disruption** because it touches the core mental model of FR-6 through FR-10, not just budget plumbing.
- The benefit is conceptual consistency: one model explains sprint task budgets, remediation retries, convergence passes, and reimbursement.
- The breakage risk is broad:
  - registry schema changes,
  - migration concerns for pre-v3.05 data,
  - more coupling between sprint and roadmap subsystems,
  - possible overfitting of roadmap semantics onto a class originally designed for subprocess budgeting.
- This is the strongest long-term unification story, but the least safe if the goal is a contained v3.05 refactor.

---

## Recommendation

If the goal is **minimum rewrite with real production wiring**, choose **Proposal 1**.

If the goal is **true behavioral unification with the already-written reimbursement tests**, choose **Proposal 2**.

If the goal is **architectural convergence on one accounting model across sprint and roadmap**, choose **Proposal 3**, but expect spec and schema churn.

## Evidence used
- v3.05 convergence spec: `/config/workspace/IronClaude/.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`
- TurnLedger definition: `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py`
- Sprint execution budget hooks: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`
- Trailing gate remediation flow: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py`
- Reimbursement-loop tests: `/config/workspace/IronClaude/tests/pipeline/test_full_flow.py`
