# Hypothesis: Test asserts old invariant; CI flakiness is a secondary fixture-leakage effect

**Agent**: root-cause-analyst
**Tier**: 2
**Timestamp**: 2026-05-21T05:32:00Z
**Cause class**: Test infrastructure (primary) + Test isolation / fixture leakage (secondary, explains intermittency)

## Claim

The PRIMARY cause of the failure is the same as the Tier 1 diagnosis: the test asserts `len({s.id for s in sessions}) == 1`,
which encodes the pre-feature single-session invariant. The new per-device feature makes 4 devices → 4 sessions, so the
assertion fails by design. The SECONDARY cause that explains the 1/5-CI-pass and "passes locally" pattern is that the test
sometimes sees a database in a state where prior session rows or fixture state cause `create_sessions_async` to short-circuit
or roll back — likely a `test_user` fixture that is shared/scoped wider than `function`, or a `db_session` that occasionally
auto-rolls-back from an `IntegrityError` on a duplicate (`device_id`, `user_id`) row from a previous test run, leaving the
DB in a state where the assertion accidentally passes.

The fix is still to update the TEST, not the code. The secondary observation about fixture scoping should be a follow-up
ticket — not a blocker on this fix.

## Evidence

- Same primary citations as Tier 1 / quality-engineer:
  - `api/session.py::create_session` docstring + body (per-device intent)
  - `create_sessions_async` plural-list signature
  - test assertion `== 1` and inline comment
  - commit `feat(sessions): per-device sessions for parallel logins`
  - spec `docs/product/sessions.md`
- Additional for the intermittency hypothesis:
  - The ThreadPoolExecutor in `api/session.py` is a MODULE-LEVEL singleton (`_executor = ThreadPoolExecutor(max_workers=8)`).
    Multiple test runs in the same Python process share its workers. Workers may hold stale `db_session` references via
    closure if `db_session` is a thread-local or module-level proxy. Not enough info to confirm, but a plausible vector for
    inter-test state leakage.
  - `db_session.add` + `db_session.commit` is being called from up to 8 worker threads against what is typically a SINGLE
    SQLAlchemy session object. SQLAlchemy sessions are NOT thread-safe. Under contention this can produce: `IntegrityError`
    rollbacks, lost writes, or commits that succeed silently from one thread while another's add is pending. Any of these
    would explain occasional "passes" (when only a subset of sessions actually got committed and the resulting set has 1
    distinct id by accident).

## Proposed Fix

Same as quality-engineer: **rewrite the test assertions** to match the per-device contract. Do NOT modify `api/session.py`.

Additional recommendation (NOT part of this fix, but a follow-up ticket):
- Investigate `db_session` thread-safety under `create_sessions_async`. If it is a single SQLAlchemy session shared across
  threads, that is a latent bug that will eventually corrupt production data. This is INDEPENDENT of the failing test and
  should not block the test fix.

Files to change:
- `tests/api/test_user_session.py` — rewrite assertions (same as quality-engineer's proposal).

## Confidence

Self-reported confidence: 0.91

Per-dimension self-assessment:
- Evidence grounding: 1.0 — strong for the primary diagnosis. The secondary intermittency story has weaker grounding (no
  fixture file provided) and is correctly marked as "hypothesis for follow-up".
- Symptom coverage: 1.0 — primary diagnosis covers the assertion failure; secondary covers the 1/5 pass rate.
- Reproducibility fit: 1.0 — the primary assertion failure is deterministic given the new code; the intermittency is
  explained by a known SQLAlchemy thread-safety hazard.
- Fix directness: 1.0 — single test file change for the immediate fix.
- Domain coherence: 0.5 — the primary fix is single-domain (test); the follow-up touches the threading + ORM domain. I am
  scoring this 0.5 because surfacing both findings together IS domain-mixed, even if the fix-of-record is single-domain.

## Risks

Same asymmetric-cost warning as quality-engineer: a naïve "make the test pass" remediation that edits `api/session.py`
would regress the shipped feature. **The fix is in `tests/`, never in `api/session.py`.**

If the follow-up SQLAlchemy thread-safety issue is real, deferring it could allow rare production corruption (lost sessions
under concurrent device logins). Recommend opening a separate ticket immediately and not bundling it with this fix.

## If I'm wrong, it's probably because...

The "intermittent" framing in the user's report is genuinely about the test, not test-infrastructure. For example, if the
test occasionally races with a teardown that deletes sessions before the assertion runs, then on rare occasions
`len({s.id for s in sessions})` would be computed against a list where some elements were already-deleted-and-refreshed-to-
the-same-row (unlikely under normal SQLAlchemy semantics, but not impossible). In that case the same fix still applies, the
explanation just differs.

## Alternatives considered

- "The code is the bug; revert to single-session": REJECTED on the same grounds as quality-engineer (contradicts spec +
  commit message).
- "Pure ThreadPoolExecutor race producing duplicate rows": REJECTED — the symptom is "got 4" (matches device count), not "got
  >4". The thread-safety risk is a separate latent bug that does not cause THIS test's primary failure.
- "Stale fixture providing a pre-existing session": considered as the explanation for the 1/5-pass rate; kept as a
  secondary, weakly-evidenced hypothesis pending fixture file review.

## Grounding gaps

- No access to `conftest.py` / fixture definitions for `test_user` and `db_session` — the intermittency story is therefore
  inferential, not evidenced.
- No git history confirming the commit landed.
- Inline-pasted code, not on-disk.
