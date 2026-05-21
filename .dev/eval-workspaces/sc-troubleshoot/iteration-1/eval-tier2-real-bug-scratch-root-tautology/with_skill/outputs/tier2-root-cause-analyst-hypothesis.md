# Hypothesis: same root cause; mechanism preference is to defensively reject same-path tautology in `resolve_scratch_root` itself

**Agent**: root-cause-analyst
**Tier**: 2
**Timestamp**: 2026-05-21T05:02:30Z
**Cause class**: Security gate bypass via parameter aliasing

## Claim

Agreed on the root cause (eval_run passes the same path as candidate and as the allowlist-extending kwarg). Mechanism preference: rather than (or in addition to) fixing the call site, make `resolve_scratch_root` itself refuse to honor an `output_dir=` kwarg whose resolved form equals the candidate's resolved form. That defensive check would have caught this bug at the API boundary regardless of caller mistakes.

## Evidence

- Same evidence as security-engineer (call site + helper internals + policy doc).
- Snapshot `config.py:237-238` — the extension step does not compare against the candidate; a 2-line guard there closes the entire class of caller bug.

## Proposed Fix

Two-part:

1. (Same as Fix-1) Drop `output_dir=output_dir` from the `eval_run` call at snapshot `commands.py:1473-1477`.
2. In `resolve_scratch_root` (`config.py:217-238`), after computing the resolved candidate, raise `ScratchRootViolation` (or a `ValueError`) if any allowlist entry contributed by `output_dir=` equals the resolved candidate. Anti-tautology guard.

Tests:

- Regression test for `/etc/foo` rejection at the `eval_run` boundary.
- Unit test: `resolve_scratch_root(p, output_dir=p)` raises.

## Confidence

Self-reported: 0.88

Per-dimension:

- Evidence grounding: 1.0
- Symptom coverage: 1.0
- Reproducibility fit: 1.0
- Fix directness: 0.5 (two-part fix; the helper change is wider surface than strictly necessary)
- Domain coherence: 0.5 (security)

## Risks

- Helper-level guard could break legitimate `containment_guard` re-check semantics: when the guard re-validates a previously-validated path, the candidate is the same as the `output_dir=` extension by design. The guard would need an `allow_tautology=True` opt-in, which leaks API complexity.
- This risk is why Fix-1 (call-site only) is preferable.

## If I'm wrong, it's probably because

The helper-level guard breaks `containment_guard` and the test suite catches it — proving Fix-1 (call-site only) is the right shape.

## Alternatives considered

- Remove the `output_dir=` parameter entirely — too wide; legitimate callers use it.
- Type the `output_dir=` argument as a *different* type (`PreValidatedPath`) so the type system encodes "this must already have been validated" — cleaner long-term but out of scope for this fix.

## Grounding gaps

- Did not check `containment_guard` test coverage for the same-path case.
