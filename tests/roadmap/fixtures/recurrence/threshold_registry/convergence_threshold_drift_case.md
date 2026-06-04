---
fixture: convergence_threshold_drift_case
failure_class: threshold_registry
contract: 8
master_recurrence_row: 7
---

# Recurrence #7 — Convergence-Threshold Drift Across Sibling Skills

> **Documented incident** (master:§Recurrence Matrix row #7):
> *"Convergence-threshold drift / advisory-not-enforcing (gate validates score
> parses; releases ship at 0.72 below 0.80; sibling skills use 0.6/0.5 vs
> 0.7/0.5)."*
> Partition findings: `A1b:F-A1b-002`, `A10:F-A10-003`.

## What happened

Sibling skills carried **divergent local copies** of the convergence threshold
pair. `A10:F-A10-003`:

> "release-split used 0.7/0.5, sc:roadmap uses 0.6/0.5" — the same nominal
> `(high, low)` convergence pair was defined as a literal in two different
> modules and drifted apart, so two skills that should converge on the same
> bar silently enforced different ones.

Because each module re-declared the pair as an in-module literal, there was no
single source of truth: editing one did not propagate to the other, and the
drift was invisible until a release shipped at a threshold one skill considered
passing and the other considered failing.

## The anti-pattern (pre-fix)

A module **outside** `superclaude.contracts` re-declares the
`CONVERGENCE_THRESHOLDS` constant as its own local literal:

```python
# sibling-skill module — local re-declaration (DRIFT: 0.6/0.5 here vs 0.7/0.5 elsewhere)
CONVERGENCE_THRESHOLDS = {
    "sc:roadmap": (0.6, 0.5),
}
```

## The invariant (post-fix — Contract #8 / arch-lint Rule 1)

The convergence threshold pair lives in exactly one place:
`superclaude.contracts.CONVERGENCE_THRESHOLDS`. Any module that **rebinds** that
name (or redefines a contracts-owned constant) outside the contracts module is an
arch-lint `name-rebind` violation. The post-fix shape imports the canonical
constant instead of re-declaring it:

```python
from superclaude.contracts import CONVERGENCE_THRESHOLDS

high, low = CONVERGENCE_THRESHOLDS["sc:roadmap"]
```

**This fixture's test feeds the pre-fix snippet (the first fenced block above) to
`superclaude.tools.arch_lint.scan_file` and asserts exactly one `name-rebind`
violation on `CONVERGENCE_THRESHOLDS`; it feeds the post-fix snippet and asserts
zero violations.** See `.expected.json` for the verified values.
