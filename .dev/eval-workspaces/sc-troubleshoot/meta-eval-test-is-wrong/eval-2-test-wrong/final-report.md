# Troubleshoot Report

**Target**: `tests/api/test_user_session.py::test_concurrent_session_creation` fails 4/5 in CI with "expected 1 session, got 4"
**Type**: test
**Tier reached**: 2
**Confidence**: 0.90
**Status**: partial
**Escalation reason**: intermittent
**Duration**: ~7 min (simulated)
**Date**: 2026-05-21T05:35:00Z

---

## Summary

**The TEST is the bug, not the code.** `api/session.py` correctly implements the new per-device session contract shipped
in `feat(sessions): per-device sessions for parallel logins`. The test still asserts the pre-feature single-session
invariant (`len({s.id for s in sessions}) == 1`) and was not updated alongside the feature. **The fix is to rewrite the
test assertions to match the per-device contract. Do NOT modify `api/session.py` — doing so would regress the shipped
feature.** Status is `partial` only because (a) the cited code was provided inline rather than on disk so evidence
citations could not be filesystem-validated, and (b) the residual 1/5-pass rate in CI suggests a secondary
test-isolation issue worth a follow-up ticket but not blocking the fix.

## Diagnosis

**Root cause**: The test `test_concurrent_session_creation` asserts the OLD single-session-per-user invariant via
`assert len({s.id for s in sessions}) == 1`. The recent commit `feat(sessions): per-device sessions for parallel logins`
intentionally changed production behaviour so each device receives its own session. The test was not updated to track the
new contract. The assertion text "expected 1 session, got 4" is the deterministic consequence of the new code (4 devices →
4 sessions) meeting the old assertion (== 1).

**Cause class**: Test infrastructure — stale test against intentionally-changed production contract.

**Detailed explanation**: The production function `api.session.create_session` (per its docstring "Create a new session
per device. Each call gets a fresh session — this is the requirement.") always creates a new `Session` row with a fresh
`uuid4().hex` token. The wrapper `create_sessions_async` (note the plural name and `list[Session]` return type) submits
one task per device to a `ThreadPoolExecutor` and returns all results. Given 4 input devices the function returns 4
distinct sessions by design. The product spec (`docs/product/sessions.md`: "Each device or browser tab MUST receive its
own session.") and the commit message both confirm the per-device behaviour is the intended product behaviour, not a
regression. The test, which predates the feature, was not updated. Fixing the code to satisfy the test would silently
regress the per-device feature — this is the asymmetric-cost failure mode and is the primary risk this report flags.

The residual 1/5-pass rate in CI is NOT explained by the stale-test diagnosis alone (which predicts 5/5 failures). The
most plausible secondary explanation is `db_session` / `test_user` fixture state leakage between tests in the CI runner,
where occasionally the DB is in a state that produces a different observed session count. This is flagged as a
non-blocking follow-up; see "Risk + Rollback".

## Evidence

1. `api/session.py::create_session` (provided inline) — docstring states
   `"""Create a new session per device. Each call gets a fresh session — this is the requirement."""`. The body unconditionally
   constructs `Session(user_id=user.id, device_id=device_id, token=uuid4().hex)`, calls `db_session.add(session)` and
   `db_session.commit()`. No dedup-by-user branch exists.
2. `api/session.py::create_sessions_async` (provided inline) — signature
   `def create_sessions_async(user: User, device_ids: list[str]) -> list[Session]`. Plural name, list return type, one
   `executor.submit(create_session, user, did)` per device, returns all `f.result()`. The shape encodes multi-session intent.
3. `tests/api/test_user_session.py::test_concurrent_session_creation` (provided inline) — body contains
   `assert len({s.id for s in sessions}) == 1, f"expected 1 session, got {len({s.id for s in sessions})}"`. The error
   message in the assertion is verbatim the user's reported failure ("expected 1 session, got 4"), confirming this is the
   firing assertion.
4. Inline test comment (provided in the test source) — `# Note: this test was written BEFORE the per-device feature and
   asserts the OLD single-session-per-user invariant. The team's recent commit "feat(sessions): per-device sessions" did
   NOT update this test.` The team has effectively self-documented the gap.
5. Authoritative spec excerpt (provided as authoritative context in the invocation): `docs/product/sessions.md` — "Each
   device or browser tab MUST receive its own session. Multiple concurrent sessions per user are required."
6. Commit message (provided as context): `feat(sessions): per-device sessions for parallel logins` — confirms the
   production change was intentional product work.

## Proposed Fix

**Update the test, not the code.** Rewrite the assertion block in `tests/api/test_user_session.py` to validate the
per-device contract:

```python
def test_concurrent_session_creation(test_user):
    devices = ['phone', 'laptop', 'tablet', 'desktop']
    sessions = api.session.create_sessions_async(test_user, devices)
    # Per-device contract (per docs/product/sessions.md)
    assert len(sessions) == len(devices), "one Session per device"
    assert len({s.id for s in sessions}) == len(devices), "all session IDs distinct"
    assert len({s.token for s in sessions}) == len(devices), "all tokens distinct"
    assert {s.device_id for s in sessions} == set(devices), "each device represented exactly once"
    assert {s.user_id for s in sessions} == {test_user.id}, "all belong to test_user"
```

**Files to change**:
- `tests/api/test_user_session.py` — replace the assertion as above. Single test, ~5 line diff.

**Files that MUST NOT change** (asymmetric-cost guard):
- `api/session.py` — the code correctly implements the shipped per-device contract. Any modification here that makes the
  CURRENT test pass would regress the feature.

**Test to verify**:
- The rewritten `test_concurrent_session_creation` itself should pass deterministically against the existing
  `api/session.py`.

**Apply with**: re-run `/sc:troubleshoot --fix ...` to authorize the Tier 3 task-builder chain. The handoff brief MUST
explicitly forbid edits to `api/session.py`. Or apply the test rewrite manually (faster, lower-risk for a 5-line
change).

## Alternative Fixes Considered

(Tier 2 ran but produced a single consensus fix; the adversarial debate was skipped per the Wave 3 exit criteria. The
losing direction below is the one the user / a downstream automation must be steered AWAY from.)

- **Fix A — "Make the test pass by deduplicating sessions in `api/session.py`"**
  - Rejected because: directly contradicts the shipped spec, the deliberate commit, and the function's docstring +
    signature. This is the DANGEROUS wrong answer and is the entire reason this report explicitly flags the
    asymmetric-cost risk in the Summary and Risk sections.
- **Fix B — "Add a unique constraint on (user_id) in the Session model"**
  - Rejected because: same regression as A; would also begin throwing `IntegrityError` on every second device login in
    production.
- **Fix C — "Race condition in ThreadPoolExecutor"**
  - Rejected because: the failure produces exactly 4 sessions (matches device count), not a varying count. A race would
    produce variable results across runs.

## Risk + Rollback

- **Asymmetric-cost risk (PRIMARY)**: the largest risk in this diagnosis is that a downstream agent, automated
  remediation chain, or contributor treats the failing test as evidence the code is broken and "fixes" the code. Any
  modification to `api/session.py` that satisfies the CURRENT `== 1` assertion will silently regress the per-device
  feature in production. Any handoff (Tier 3 task brief, manual instruction, code review) MUST explicitly state: "Fix
  is in tests/ only. api/session.py must not change."
- **Likelihood of regression** (of the fix itself): **low**. The change is in a single test file and only changes
  assertions. No production code path is touched.
- **Test coverage of the changed code**: the test IS the coverage; the rewrite improves coverage (5 contract assertions
  vs. 1 scalar). Good.
- **Secondary — residual intermittency**: the 1/5 CI-pass rate is not fully explained by the stale-test diagnosis. After
  the test is rewritten, monitor CI for 5–10 runs to confirm the rewritten test is 5/5 stable. If it is not, open a
  follow-up to investigate `conftest.py` fixture scoping for `test_user` / `db_session` and SQLAlchemy thread-safety in
  `create_sessions_async` (see Out-of-Scope Follow-ups below).
- **Rollback**: `git revert` the single-test-file commit; the previous (still-failing) assertion returns. Trivial.

## Grounding Gaps

- **Inline code, not disk-resident.** All `file:line` citations refer to the code provided inline in the user's
  invocation, not files the skill could open with `Read`. The evidence-validator pass cannot filesystem-verify these
  citations against `api/session.py` and `tests/api/test_user_session.py` because those files do not exist at the
  expected paths in this sandbox. The semantic content of each citation IS verified against the inline text. **Status
  is set to `partial` because of this.**
- **Spec excerpt is treated as authoritative per the invocation**, but `docs/product/sessions.md` was not Read from
  disk.
- **Commit history not verified.** The skill did not run `git log` to confirm `feat(sessions): per-device sessions for
  parallel logins` exists; it is treated as authoritative per the invocation.
- **Failing test not executed.** No live pytest run; relying on the user's reported observation ("expected 1 session,
  got 4") which matches the assertion text in the inline source exactly.
- **Fixture / conftest files not surveyed.** The 1/5-pass rate hypothesis is correspondingly weakly evidenced (flagged
  as secondary / follow-up, not used as the basis for the fix).

## Out-of-Scope Follow-ups (do not bundle with this fix)

1. **SQLAlchemy thread-safety**: `create_sessions_async` submits up to 8 concurrent `db_session.add` + `commit` calls
   against what is typically a single SQLAlchemy session object. SQLAlchemy sessions are not thread-safe. Latent risk
   of `IntegrityError`, lost writes, or silent inconsistencies under high-concurrency device-login bursts. Open as a
   separate ticket; could explain the 1/5 CI-pass-rate; do not bundle with the test fix.
2. **Fixture scoping audit**: confirm `test_user` and `db_session` fixtures are function-scoped and teardown reliably.
   Possibly the actual explanation for the 1/5 pass rate.

## Next Steps

Re-run with `--fix` added to your previous invocation to enter the remediation chain — `/sc:troubleshoot --fix --type
test "..."`. **When you do, the task brief MUST forbid edits to `api/session.py`.** Or apply the 5-line test rewrite
manually; given the scope it is faster than the full remediation chain.

## Audit

- **Hypothesis cards**:
  - `tier1-hypothesis.md`
  - `tier2-quality-engineer-hypothesis.md`
  - `tier2-root-cause-analyst-hypothesis.md`
  - `tier2-refactoring-expert-hypothesis.md`
- **Calibrations**:
  - `tier1-calibration.md`, `tier2-quality-engineer-calibration.md`,
    `tier2-root-cause-analyst-calibration.md`, `tier2-refactoring-expert-calibration.md`
- **Adversarial artifacts**: Not invoked — consensus on a single fix-of-record.
- **Self-review**: Not invoked (no adversarial merge to review).
- **Task file** (Tier 3): not generated; `--fix` was not set.
- **Audit log**: `audit.log`
- **Evidence validation**: `evidence-validation.md`
