---
fixture: unwired_certify_step_case
failure_class: dispatch_reachability
contract: 2
master_recurrence_row: 2
---

# Recurrence #2 — Gate/Step "Written but Not Wired" (certify defined, never dispatched)

> **Documented incident** (master:§Recurrence Matrix row #2 / §Top-3 driver #2):
> *"Gate / step 'written but not wired' — function defined, never invoked from
> production path (cert step, `_resolve_wiring_mode`, `_format_wiring_failure`,
> T04 sprint bridge, `tasklist generate` CLI subcommand)."*
> Partition findings: `A10:F-A10-019`, `A11:F-A11-011`.

## What happened

`build_certify_step()` existed at `executor.py` as a fully-formed builder
function — it constructed a `Step(id="certify", ...)` with a `CERTIFY_GATE` and a
prompt parser — but **no production caller ever invoked it**. The v3.66
`_build_steps()` dispatch map ended at `remediate`; there was no
`Step(id="certify", ...)` literal inside `_build_steps`, and `execute_roadmap`
never called `build_certify_step()`. The only invocation lived in a test file.

Verbatim from `A11:F-A11-011`:

> "A 13th step (certify) has a builder function `build_certify_step()` at
> executor.py:1259, but is never called — confirmed dead code."

And `A10:F-A10-019`:

> "v3.66 `_build_steps()` ends at remediate; no `step.id == 'certify'` dispatch."

The pipeline therefore **silently ended at `remediate`** while passing every
artifact-shape gate, shipping a terminal certification step that was dead in
production. This is the canonical "anti-instinct gate's own bug" — infrastructure
built complete with tests while the production entry-point never reaches it.

## The anti-pattern (pre-fix)

```python
# executor.py — pre-fix shape (master:§Flaw 1 condition)
def build_certify_step(...):
    return Step(id="certify", gate=CERTIFY_GATE, ...)   # builder exists

def _build_steps(config):
    return [extract_step, ..., remediate_step]           # NO certify in dispatch

def execute_roadmap(config):
    steps = _build_steps(config)
    execute_pipeline(steps)                              # build_certify_step() NEVER called
    # pipeline ends at remediate — certify is dead code
```

## The invariant (post-fix — Contract #2)

`assert_step_reachable` (an AST dispatch-reachability assertion over the real
`executor.py`) requires `certify` to be reachable from a production dispatch
path via EITHER:

1. **Static shape** — a `Step(id="certify", ...)` literal inside `_build_steps`; OR
2. **Dynamic shape** — `build_certify_step()` is *called* inside `execute_roadmap`
   (directly or via a helper it invokes) post-`execute_pipeline` (design doc §7.3
   option a), keeping `_build_steps` at the 14-step budget while guaranteeing the
   step ships wired.

The assertion FAILS only when `certify` is unreachable by both — the pre-R1.3
state above. Post-fix, the dynamic shape is present: `build_certify_step()` has a
production caller in `executor.py`, so `assert_step_reachable` returns `None`
(PASS).

**This fixture's test does NOT parse this `.md` as scanner input** — it documents
the incident verbatim, then asserts the post-fix invariant `every built Step.id is
reachable from the dispatch graph` by running `assert_step_reachable` against the
live `executor.py` (see `.expected.json` `expected_dispatch_reachable: true`).
