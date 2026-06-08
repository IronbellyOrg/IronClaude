---
fixture: skipped_verification_step_case
failure_class: dispatch_reachability
contract: 2
master_recurrence_row: 14
---

# Recurrence #14 — Verification / Certify Terminal Step Silently Skipped

> **Documented incident** (master:§Recurrence Matrix row #14):
> *"Verification / Wave-3 / certify tasks silently skipped — pipeline does not
> gate on verification completion."*
> Partition findings: `A2b:F-A2b-003`, `A11:F-A11-011`.

## What happened

The terminal verification work (Wave-3 / T11-T14 / certify) was **silently
skippable**: the pipeline reached `remediate` and stopped, never dispatching the
verification/certify terminal steps, and **did not gate on verification
completion**. Verbatim:

`A2b:F-A2b-003`:

> "v3.1 T11-T14 skipped — verification wave silently skipped; pipeline does not
> gate on verification completion."

`A11:F-A11-011`:

> "certify still dead code — `build_certify_step()` defined but never called."

This is the same structural class as Recurrence #2 ("written but not wired"):
a terminal step that exists in code but is unreachable from the production
dispatch path, so the pipeline ships without ever running it. The distinguishing
emphasis here is that the *verification* link — the step that confirms the
implementation actually matches the roadmap — was the one silently dropped, so
the pipeline had **no terminal verification link from Tasklist→Code**.

## The anti-pattern (pre-fix)

```python
# executor.py — pre-fix shape
def execute_roadmap(config):
    steps = _build_steps(config)
    execute_pipeline(steps)          # ends at remediate
    # verify-implementation / certify terminal steps NEVER dispatched
    # no gate asserts verification completion -> silent skip
```

## The invariant (post-fix — Contract #2)

The terminal verification/certify steps MUST be reachable from a production
dispatch path. Verified the same way as Recurrence #2 via `assert_step_reachable`
(the AST dispatch-reachability assertion over the live `executor.py`): the
`certify` step is reachable through the dynamic shape (`build_certify_step()` has
a production caller), AND the `verify-implementation` terminal step is dispatched
through `_run_verify_implementation()`, which has a production caller inside
`execute_roadmap()` (the post-`execute_pipeline` terminal-step chain, design doc
§7.3 / R1.5).

**This fixture's test does NOT parse this `.md` as scanner input** — it documents
the incident verbatim, then asserts the post-fix dispatch-reachability invariant
against the live `executor.py` (`expected_dispatch_reachable: true`).
