# TurnLedger Integration Brainstorm for Unified Audit Gating v3.1

## Ranking Summary

1. **Gate-Coupled Reimbursement Ledger** — highest ROI
2. **Ledger-Bounded Deferred Remediation Loop**
3. **Result-Derived Gate KPI Pipeline**

---

## 1. Gate-Coupled Reimbursement Ledger

### Summary
Refactor the audit gating flow so `TurnLedger` becomes the source of truth for gate economics rather than just launch gating. Today `execute_phase_tasks()` debits minimum allocation, then credits back any unused pre-allocation, but it never applies the intended pass-based reimbursement model. The highest-value change is to move reimbursement to the gate decision boundary: task subprocess exits debit actual turns, trailing gate resolves, and only then does the ledger credit `floor(actual_turns * reimbursement_rate)` for PASS outcomes.

This directly activates the currently unused `reimbursement_rate=0.8` field and makes gate evaluation budget-bounded in a meaningful way. Budget would stop being just a launch throttle and become a quality-aware control loop: passing work earns partial budget back, failed work drains budget faster, and repeated poor-quality output naturally halts the sprint earlier.

### Why this is highest ROI
- It closes the clearest production/spec gap: `TurnLedger.reimbursement_rate` exists but is not consumed by production code.
- It aligns current code with the unified spec’s intended economics: debit on execution, credit on gate PASS, no credit on fail.
- It improves boundedness without adding much orchestration complexity.
- It makes later KPI and remediation work far more meaningful because budget reflects real gate outcomes.

### TurnLedger fields reused
- `initial_budget`
- `consumed`
- `reimbursed`
- `reimbursement_rate`
- `minimum_allocation`
- `available()`
- `debit()`
- `credit()`
- `can_launch()`

### Proposed refactor shape
- Keep pre-launch `can_launch()` and minimum allocation behavior from `execute_phase_tasks()`.
- Replace current reconciliation logic that credits `pre_allocated - actual` as a pure allocation correction with a two-stage accounting model:
  1. debit actual task turns after subprocess exit
  2. credit reimbursement only after gate PASS
- Store gate outcome and reimbursed turns on `TaskResult` so runner-constructed reports reflect actual economics.
- If gates are blocking, reimbursement happens inline.
- If gates are trailing, reimbursement happens at the sync point after `TrailingGateRunner.wait_for_pending()` resolves.

### What gate evaluation looks like when budget-bounded via TurnLedger
- A task can launch only if `ledger.can_launch()` is true.
- After execution, actual turns are debited.
- If the gate passes, credit `floor(actual_turns * reimbursement_rate)`.
- If the gate fails, do not credit.
- This makes poor quality more expensive than good quality and creates a mathematically bounded loop without inventing another budget model.

### Risk assessment
**Low to medium risk.**
- Main risk is behavior change in existing sprint budget expectations because today the code effectively refunds unused allocation rather than applying quality-conditioned reimbursement.
- Test risk is manageable because `tests/pipeline/test_full_flow.py` already models the desired reimbursement behavior, so the refactor mostly brings production into line with test/spec intent.
- Requires careful handling so `credit()` receives already-computed reimbursed turns, or `TurnLedger.credit()` is upgraded to apply `reimbursement_rate` internally consistently.

---

## 2. Ledger-Bounded Deferred Remediation Loop

### Summary
Refactor gate failure handling so sprint-side remediation uses the existing `attempt_remediation()` state machine from `src/superclaude/cli/pipeline/trailing_gate.py`, backed by `TurnLedger.can_remediate()` and persisted in `DeferredRemediationLog`. This would replace ad-hoc or fragmented failure handling with a single retry-once contract shared between pipeline and sprint orchestration.

The core idea is to stop treating remediation as a sprint-specific special case and instead make it a first-class continuation of gate evaluation. A failed gate appends a `DeferredRemediationLog` entry, then the executor uses `SprintGatePolicy.build_remediation_step()` plus `attempt_remediation()` to consume bounded remediation budget, retry once, and produce a canonical result. This gives sprint a reusable failure model instead of bespoke glue.

### Why this is second-highest ROI
- The remediation state machine is already implemented and budget-aware.
- `DeferredRemediationLog` already provides a durable structure for pending/resolved remediation state and resume support.
- It removes duplicated concepts: failed gate tracking, retry status, and pending remediation inventory.
- It turns the current trailing gate module from an isolated utility into the central enforcement path the spec envisioned.

### TurnLedger fields reused
- `minimum_remediation_budget`
- `available()`
- `debit()`
- `can_remediate()`
- `consumed`
- `reimbursed` indirectly if remediation PASS is later tied into proposal #1

### Proposed refactor shape
- On gate failure, append the failure to `DeferredRemediationLog` rather than relying on scattered in-memory tracking.
- Use `SprintGatePolicy.build_remediation_step()` to generate the focused remediation step.
- Invoke `attempt_remediation()` with:
  - `can_remediate=ledger.can_remediate`
  - `debit=ledger.debit`
  - sprint-specific `run_step`
  - sprint-specific gate checker returning `TrailingGateResult`
- On PASS, mark the log entry remediated.
- On persistent failure, halt with diagnostic/resume output.
- On budget exhaustion before remediation, halt immediately with the budget-specific branch already modeled in tests.

### Can the remediation loop use `attempt_remediation()`?
Yes. It is already designed exactly for this integration point:
- takes a remediation `Step`
- consumes budget through injected `debit`
- checks affordability through injected `can_remediate`
- runs step logic through injected `run_step`
- evaluates success through injected `check_gate`

That makes it a strong fit for sprint-side orchestration without violating separation of concerns.

### Can `DeferredRemediationLog` replace ad-hoc failure tracking?
Yes, likely with good payoff.

Current sprint-side structures are fragmented:
- `TaskResult.gate_outcome` is summarized into aggregated reports
- `build_resume_output()` reconstructs halt state from remaining tasks and ledger
- `SprintGatePolicy.build_remediation_step()` currently only consumes a bare `TrailingGateResult`
- `build_kpi_report()` already expects `DeferredRemediationLog`

`DeferredRemediationLog` can centralize:
- which task failed gate
- failure reason
- remediation pending vs remediated
- serialized gate result payload for `--resume`

The main gap is that the current log schema is minimal. For full sprint value it would likely need modest enrichment, such as task ID, phase number, remediation attempts, and maybe file/change metadata.

### Risk assessment
**Medium risk.**
- Main risk is orchestration complexity: sprint executor currently does not appear to wire trailing gate runner, remediation log, and KPI generation into one end-to-end lifecycle.
- `DeferredRemediationLog`’s current payload is thinner than the richer spec version, so some schema expansion may be needed.
- Conflict review integration may still need extra sprint-owned file tracking because `SprintGatePolicy.files_changed()` currently just returns the output file, which is probably too weak for robust overlap detection.

---

## 3. Result-Derived Gate KPI Pipeline

### Summary
Refactor reporting so `GateKPIReport` is populated from actual runtime gate/remediation artifacts rather than synthetic or manually assembled inputs. The runner should accumulate real `TrailingGateResult` objects, real `DeferredRemediationLog` entries, and real conflict-review counts during execution, then call `build_kpi_report()` once at sprint completion.

This proposal is lower ROI than the first two because it mostly improves observability rather than core correctness, but it becomes very valuable once reimbursement and remediation are wired properly. It gives a real answer to “how well is unified audit gating working?” instead of only “did the sprint halt?”

### TurnLedger fields reused
- `consumed`
- `reimbursed`
- `available()`
- `reimbursement_rate`

These are not currently part of `GateKPIReport`, but they should be incorporated or at least cross-referenced to relate quality outcomes to budget outcomes.

### What `GateKPIReport` should look like if populated from actual gate results
At minimum, the existing report would become authoritative rather than speculative:
- `total_gates_evaluated` from all real `TrailingGateResult`s
- `gates_passed` / `gates_failed` from real outcomes
- `gate_latency_ms` from actual `evaluation_ms`
- `total_remediations` / `resolved` / `pending` from `DeferredRemediationLog`
- `total_conflict_reviews` / `conflicts_detected` from actual conflict review operations

For v3.1, the more useful shape would extend the report with economics tied to real results:
- `turns_consumed_total`
- `turns_reimbursed_total`
- `net_budget_drain`
- `avg_reimbursed_turns_per_pass`
- `failed_gate_budget_loss`
- `persistent_failure_count`
- `budget_exhausted_gate_failures`
- `first_attempt_remediation_pass_rate`
- `second_attempt_remediation_pass_rate`

That would finally connect gate quality, remediation behavior, and budget burn in one report.

### Proposed refactor shape
- During execution, accumulate every `TrailingGateResult` into a sprint-level collection.
- Persist every failed gate to `DeferredRemediationLog`.
- Count every conflict review invocation and whether overlap was detected.
- At sprint end, build KPI once from those real collections.
- Optionally extend `GateKPIReport` to include ledger-derived economic metrics.

### Risk assessment
**Low risk.**
- Mostly additive and reporting-focused.
- The main risk is misleading KPIs if upstream wiring remains incomplete; for example, if gate results are not collected consistently, the report will look precise but be partial.
- Best implemented after or alongside proposals #1 and #2 so KPIs reflect actual system behavior rather than placeholder flows.

---

## Recommendation

If only one refactor is funded, choose **Gate-Coupled Reimbursement Ledger**. It activates the dormant `reimbursement_rate` field, makes gate evaluation truly budget-bounded, and aligns production with the intended v3.0/v3.1 economic model.

If two are funded, pair it with **Ledger-Bounded Deferred Remediation Loop**. Together they create a coherent control system:
- task execution debits budget
- gate success partially reimburses budget
- gate failure enters a persisted remediation queue
- remediation consumes bounded budget through `attempt_remediation()`
- persistent failure halts cleanly with resume context

**Result-Derived Gate KPI Pipeline** should follow immediately after, because once the first two are in place the KPI report becomes genuinely decision-useful instead of just decorative.

---

## Key Evidence Anchors

- `TurnLedger` exists but `reimbursement_rate` is never consumed by production code: `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py`
- Current task execution only refunds unused pre-allocation, not gate-conditioned reimbursement: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py`
- Reusable remediation state machine already exists: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py`
- Persistent remediation tracking already exists and is serialization-ready: `/config/workspace/IronClaude/src/superclaude/cli/pipeline/trailing_gate.py`
- KPI builder is ready but depends on real gate/remediation inputs being wired through: `/config/workspace/IronClaude/src/superclaude/cli/sprint/kpi.py`
- Full-flow test already expresses the intended economic/remediation behavior: `/config/workspace/IronClaude/tests/pipeline/test_full_flow.py`
