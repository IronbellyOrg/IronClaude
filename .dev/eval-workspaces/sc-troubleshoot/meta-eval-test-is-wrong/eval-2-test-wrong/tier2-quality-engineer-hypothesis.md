# Hypothesis: The test encodes a stale contract; production behaviour is correct per spec; the test is the defect

**Agent**: quality-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:32:00Z
**Cause class**: Test infrastructure (spec drift between test and implementation)

## Claim

The test under investigation is a CONTRACT TEST for the old single-session-per-user invariant. Product shipped a deliberate
change — "feat(sessions): per-device sessions for parallel logins" — that flipped that invariant. The implementation in
`api/session.py` correctly realises the new contract. The test was not updated to track the contract change. From a QA
perspective this is a missed-update test-maintenance defect, not a logic bug. The proper remediation is to rewrite the test
assertions to validate the NEW contract.

## Evidence

- `api/session.py::create_session` body assigns a fresh `uuid4().hex` token per invocation and unconditionally calls
  `db_session.add(session); db_session.commit()`. There is no branch that returns an existing session for the same user — by
  construction the function always creates. This is the design.
- Function name and signature: `create_sessions_async(user, device_ids) -> list[Session]`. Plural, list-returning. A
  function whose contract was "one session per user" would be named `get_or_create_session` and return a single `Session`.
- Test assertion: `assert len({s.id for s in sessions}) == 1`. The error message format `f"expected 1 session, got
  {len({s.id for s in sessions})}"` matches verbatim the user's reported failure ("expected 1 session, got 4"). Confirms this
  assertion is the firing one.
- Inline comment in the test file: explicitly notes the test was not updated for the per-device feature.
- Spec: `docs/product/sessions.md` — "Each device or browser tab MUST receive its own session. Multiple concurrent sessions
  per user are required." This is the SOURCE OF TRUTH the test should validate against.

## Proposed Fix

**Rewrite the test assertions** to match the new contract:

```python
def test_concurrent_session_creation(test_user):
    devices = ['phone', 'laptop', 'tablet', 'desktop']
    sessions = api.session.create_sessions_async(test_user, devices)
    # New contract: per-device sessions
    assert len(sessions) == len(devices), "should return one Session per device"
    assert len({s.id for s in sessions}) == len(devices), "all session IDs distinct"
    assert len({s.token for s in sessions}) == len(devices), "all tokens distinct"
    assert {s.device_id for s in sessions} == set(devices), "each device represented"
    assert {s.user_id for s in sessions} == {test_user.id}, "all belong to test_user"
```

Files to change:
- `tests/api/test_user_session.py` — replace the failing test body as above. **Do NOT touch `api/session.py`.**

Add a follow-up test for the regression direction (to catch any future change that re-introduces dedup-by-user):
- `test_concurrent_session_creation_does_not_dedup_by_user`

Test that proves the fix: the rewritten test itself. Expected to pass deterministically.

## Confidence

Self-reported confidence: 0.93

Per-dimension self-assessment:
- Evidence grounding: 1.0 — docstring, function signature, return type, assertion text, test comment, commit message, spec all align.
- Symptom coverage: 0.5 — explains the assertion failure perfectly; does not explain the 1/5 local-pass rate. That residual
  is real and I cannot account for it from this evidence alone — see "If I'm wrong".
- Reproducibility fit: 1.0 — given the new code, 4 devices deterministically produce 4 distinct sessions; the assertion
  deterministically fires.
- Fix directness: 1.0 — single test file change.
- Domain coherence: 1.0 — pure test-contract drift.

## Risks

**The dominant risk is the asymmetric-cost failure mode**: any agent or automated chain that interprets "test failing" as
"fix the code" will silently regress the shipped per-device feature. The fix MUST be flagged as "update test, not code" in
any handoff. If `--fix` is later passed and a remediation task is generated, the task brief must explicitly forbid
modifications to `api/session.py`.

Secondary: the 1/5 local-pass mystery (see quality-engineer hypothesis from the symptom-coverage axis) likely indicates DB
state from previous test runs is masking the failure in CI 1/5 times — possibly because the test fixture does not reliably
reset between runs, and an empty DB happens to produce 0 sessions on retrieval (which `{s.id for s}` would render as
`len(set()) == 0`, not 1, so that's not quite right either). This warrants a follow-up but does not change the primary
diagnosis.

## If I'm wrong, it's probably because...

The 4/5-CI-fail-rate may indicate the test is exercising something I'm not seeing — possibly a fixture that occasionally
provides a `test_user` with pre-existing sessions, or a `db_session` that occasionally rolls back the writes. Investigating
the fixture chain would resolve this, but it is orthogonal to the primary fix.

## Alternatives considered

- "Fix the code to dedup by user_id": REJECTED — directly contradicts the shipped product spec and the commit message. This
  is the dangerous wrong answer the report must warn against.
- "Add a `unique` constraint on (user_id) in the Session model": REJECTED — same reason; would also break the new feature.
- "Race condition produces duplicates": REJECTED — 4-device input produces exactly 4 output sessions every time the test
  fails (not a varying count). Race would produce variable counts.

## Grounding gaps

- Same as Tier 1 — code is inline-pasted, not on disk; spec is quoted in the prompt, not verifiable in the filesystem.
- The 1/5 local-pass mystery is not fully explained by this hypothesis alone; flagged for the third agent or a follow-up.
