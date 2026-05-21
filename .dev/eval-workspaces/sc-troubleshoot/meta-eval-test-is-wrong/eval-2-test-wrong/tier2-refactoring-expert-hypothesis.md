# Hypothesis: Test is brittle by structure — it encodes a tautology against the OLD invariant; rewrite using contract-style assertions

**Agent**: refactoring-expert
**Tier**: 2
**Timestamp**: 2026-05-21T05:32:00Z
**Cause class**: Test infrastructure (test structure encodes a stale single-value invariant rather than a contract)

## Claim

Beyond "the test asserts the wrong thing", the test is structurally brittle: it collapses 4 independent device-session
records into a single `set`-of-ids count and compares to a magic number. When that magic number ("1") encoded the OLD
invariant, a one-line change to the production code's dedup logic could silently make this test pass even when behaviour
was broken in other ways. The correct refactor is to express the test as a series of CONTRACT ASSERTIONS that name the
properties the system must preserve (one session per device, distinct tokens, all attributable to one user, no extras), not
as a count-vs-magic-number check. Doing so future-proofs the test against the next product pivot.

## Evidence

- Test body (inline): `sessions = api.session.create_sessions_async(test_user, devices)` followed by
  `assert len({s.id for s in sessions}) == 1, f"expected 1 session, got {len({s.id for s in sessions})}"`. ONE assertion
  encoding ONE scalar invariant.
- The error message in the assertion ("expected 1 session, got N") is the user-facing failure text, confirming this is the
  test that fires.
- Inline test comment explicitly acknowledges the test was not updated for the per-device feature.
- The production code (`api/session.py`) has clear contract-shaped intent: per-device, distinct token, plural return — none
  of which the test currently exercises.

## Proposed Fix

Same fix as quality-engineer/root-cause-analyst on the IMMEDIATE failure (update the test), but with a structural
recommendation: replace the single-`==`-assertion with a contract assertion block. Concrete refactor target:

```python
def test_concurrent_session_creation(test_user):
    devices = ['phone', 'laptop', 'tablet', 'desktop']
    sessions = api.session.create_sessions_async(test_user, devices)

    # Contract: one session per device, all belong to the same user, all distinct.
    assert len(sessions) == len(devices)
    assert {s.device_id for s in sessions} == set(devices)
    assert {s.user_id for s in sessions} == {test_user.id}
    assert len({s.id for s in sessions}) == len(devices)
    assert len({s.token for s in sessions}) == len(devices)
```

Files to change:
- `tests/api/test_user_session.py` — replace the brittle scalar assertion with the contract block above.

Do NOT modify `api/session.py`. The code is correct.

## Confidence

Self-reported confidence: 0.88

Per-dimension self-assessment:
- Evidence grounding: 1.0 — the test body and the production-code intent are both quoted from inline.
- Symptom coverage: 0.5 — the contract-rewrite explains why the test failed AND why this same brittleness will recur on the
  next pivot; does not directly explain the 1/5 local-pass rate.
- Reproducibility fit: 1.0 — the primary failure is deterministic.
- Fix directness: 1.0 — single file, ~5 lines.
- Domain coherence: 1.0 — pure test refactor.

## Risks

Same asymmetric-cost warning: any chain that "fixes" the test by fixing the code would regress the feature. Refactoring
the test into a contract block actually REDUCES this risk going forward by making future regressions of the per-device
contract obvious (the contract block will fail loudly on `assert len(sessions) == len(devices)` if dedup ever creeps back in).

## If I'm wrong, it's probably because...

The codebase's testing convention prefers behavioural / scenario-style tests rather than contract blocks, and a contract
block would be a stylistic outlier. In that case fall back to the minimal-rewrite version proposed by quality-engineer.

## Alternatives considered

- "Just flip `== 1` to `== 4`": REJECTED — keeps the brittleness; hard-codes the device count in the assertion.
- "Fix the code": REJECTED — contradicts spec.
- "Delete the test": REJECTED — the test is exercising a real and important code path; it just needs the right contract.

## Grounding gaps

- Test conventions of the broader codebase not surveyed (no auggie sweep on `tests/api/*` to confirm assertion style).
- Inline code only; no on-disk verification.
