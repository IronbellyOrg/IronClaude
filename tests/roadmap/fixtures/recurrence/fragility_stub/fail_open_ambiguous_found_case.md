---
fixture: fail_open_ambiguous_found_case
failure_class: fragility_stub
contract: 5
master_recurrence_row: 22
---

# Recurrence #22 — "Silent Skip on Uncertainty" / Fail-Open Ambiguous=Found

> **Documented incident** (master:§Recurrence Matrix row #22):
> *"'Silent skip on uncertainty' institutionalised as design (`--no-codebase`,
> `--no-validate`, MEDIUM-non-blocking, fail-open ambiguous=found,
> false-negative-preferred)."*
> Partition findings: `A2a:F-A2a-008`, `A9:F-A9-002`.

## What happened

"Silent-skip is institutionalized as design intent" (master:§merge analysis,
verbatim). Two cited manifestations:

`A9:F-A9-002`:

> `/sc:brainstorm` smart-detection explicitly says "If uncertain, do NOT trigger.
> False negatives preferred over token waste."

`A2a:F-A2a-008` (Stage 9 deviation): an ambiguity check that, when it could not
decide, **resolved the ambiguous case as already-found / already-satisfied**
(fail-open ambiguous=found) rather than fail-closed. Combined with
`fidelity_checker.py` failing open with `found=True` for any FR whose names
cannot be extracted (A4:F-A4-012), the pattern is a check that converts
uncertainty into a silent pass.

## The anti-pattern (pre-fix)

A check that, on the *uncertain* branch, returns the passing value with a
fragility/false-negative-preferred rationale in a comment:

```python
def _ambiguous_resolved(content: str) -> bool:
    if _cannot_decide(content):
        return True  # fail-open: if uncertain treat as found — false negatives preferred for now
    return _strict_check(content)
```

## The invariant (post-fix — Contract #5)

R1.6 made the gates fail-closed: an uncertain/ambiguous branch must NOT return
the passing value. The Contract #5 lint (`test_no_fragility_stubs.py`) forbids any
`return True` carrying a fragility marker (`fragile` / `too hard` / `for now`), so
a fail-open-on-uncertainty stub of the shape above is caught, and the live
`src/superclaude/cli` tree carries ZERO such stubs. (The companion deterministic
gates `_no_ambiguous_deviations` and `_spec_fidelity_validation_complete_true` are
fail-closed by construction: a missing/non-integer/ambiguous value returns False,
not True.)

**This fixture's test feeds the pre-fix snippet (the fenced block above) to the
Contract #5 regex `_FRAGILITY_STUB_RE` and asserts it MATCHES, then asserts the
live `src/superclaude/cli` tree contains ZERO fail-open fragility stubs.** See
`.expected.json` for the verified values.
