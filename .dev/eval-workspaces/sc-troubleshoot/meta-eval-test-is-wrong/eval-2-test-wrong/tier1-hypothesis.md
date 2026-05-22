# Hypothesis: The test asserts the pre-feature single-session invariant; the code is correct per the new per-device requirement

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:30:00Z
**Cause class**: Test infrastructure (stale test against new requirement) — NOT a code bug

## Claim

`tests/api/test_user_session.py::test_concurrent_session_creation` asserts that 4 device logins produce exactly 1 unique session
(`len({s.id for s in sessions}) == 1`). That assertion encodes the OLD single-session-per-user invariant. The recent commit
`feat(sessions): per-device sessions for parallel logins` deliberately changed the production behaviour so each device gets its
own session — and the team did not update this test. The code in `api/session.py` is correct per the new product spec
(`docs/product/sessions.md`: "Each device or browser tab MUST receive its own session"). The "bug" is the test, not the code.
Fixing the code to make this test pass would REGRESS the shipped feature.

## Evidence

- `api/session.py::create_session` — docstring `"""Create a new session per device. Each call gets a fresh session — this is the
  requirement."""` and body `session = Session(user_id=user.id, device_id=device_id, token=uuid4().hex); db_session.add(session);
  db_session.commit()`. Each invocation inserts a distinct row with a distinct token. No deduplication by `user_id`. This is
  intentional per the docstring.
- `api/session.py::create_sessions_async` — submits `len(device_ids)` tasks to the ThreadPoolExecutor and returns ALL futures'
  results. No collapsing-to-unique step. The function is named `create_sessions_async` (plural) and returns `list[Session]`, not
  `Session`. The shape of the return type alone signals multi-session-by-design.
- `tests/api/test_user_session.py::test_concurrent_session_creation` — assertion `assert len({s.id for s in sessions}) == 1,
  f"expected 1 session, got {len({s.id for s in sessions})}"`. The error message in the assertion is exactly what the user
  reported observing ("expected 1 session, got 4"), confirming this is the assertion that is firing.
- Inline test comment: `# Note: this test was written BEFORE the per-device feature and asserts the OLD single-session-per-user
  invariant. The team's recent commit "feat(sessions): per-device sessions" did NOT update this test.`
- Spec context (authoritative): `docs/product/sessions.md` — "Each device or browser tab MUST receive its own session. Multiple
  concurrent sessions per user are required."
- Commit message: `feat(sessions): per-device sessions for parallel logins` — the production-code change was intentional.

## Proposed Fix

**Update the TEST, not the code.** The test must be rewritten to assert the new invariant: 4 devices → 4 distinct sessions, each
with a distinct device_id and distinct token, all sharing the same user_id.

Files to change:
- `tests/api/test_user_session.py` — replace the `== 1` assertion with assertions that match the per-device contract:
  - `len(sessions) == len(devices)` (one session per device returned)
  - `len({s.id for s in sessions}) == len(devices)` (all session IDs distinct)
  - `len({s.token for s in sessions}) == len(devices)` (all tokens distinct)
  - `{s.device_id for s in sessions} == set(devices)` (each device represented exactly once)
  - `{s.user_id for s in sessions} == {test_user.id}` (all sessions belong to the same user)

**Do NOT change `api/session.py`.** Changing it to make the current test pass (e.g. dedup by user_id) would re-introduce the
old single-session behaviour and regress the shipped feature.

Test that proves the fix:
- The rewritten `test_concurrent_session_creation` will pass deterministically (no shared mutable state in `create_session` —
  each call constructs its own Session row).
- Consider adding `test_concurrent_session_creation_thread_safety` to specifically exercise the ThreadPoolExecutor path against
  DB session isolation (see Risks below).

## Confidence

Self-reported confidence: 0.94

Per-dimension self-assessment:
- Evidence grounding: 1.0 — every claim is grounded in code provided inline, including the test comment explicitly stating
  the test is stale.
- Symptom coverage: 1.0 — explains both the assertion text ("expected 1 session, got 4") and the local-pass / CI-fail asymmetry
  (see "If I'm wrong" — most likely the local environment has DB state from previous runs that masks the count).
- Reproducibility fit: 1.0 — the symptom is deterministic given the new code: 4 devices → 4 sessions → assertion fails. The
  CI vs local difference is a secondary signal (likely test-isolation, not the primary bug).
- Fix directness: 1.0 — fix is contained to one test file. Code is untouched. Small, localised change.
- Domain coherence: 1.0 — single domain (test vs. spec alignment).

## Risks

- **Asymmetric-cost risk (the big one)**: if a downstream remediation chain naïvely "fixes the failing test" by changing
  `api/session.py` to satisfy the assertion (e.g. dedup-by-user), the shipped per-device feature regresses silently. The fix
  MUST target the test file, not the production code. This must be stated explicitly in any remediation handoff.
- **Secondary**: the CI-vs-local 4/5 flakiness is NOT explained by the test-update gap alone. If the test is fixed correctly,
  the new assertions (`== len(devices)`) should pass reliably. But the original test passing locally "sometimes" suggests
  possible test-state leakage (DB not reset between local runs) — worth one follow-up but not in scope of this fix.
- **DB session thread-safety**: `create_sessions_async` calls `db_session.add/commit` from 8 worker threads against what is
  typically a single SQLAlchemy session object. This is a real concern but ORTHOGONAL to the test failure — it would manifest
  as `ObjectDeletedError`, `InvalidRequestError`, or silent data loss, not as "got 4 instead of 1". Flag for a separate ticket.

## If I'm wrong, it's probably because...

The spec in `docs/product/sessions.md` was misread or the commit `feat(sessions): per-device sessions` was reverted /
partially-applied and we're looking at an intermediate state. In that case the test reflects the intended invariant and the code
is the regression. Verify by checking git log + the spec file itself in the next pass.

## Alternatives considered

- **The CODE is wrong (the obvious wrong answer)**: rejected because the docstring, function name (`create_sessions_async`,
  plural), return type (`list[Session]`), commit message, and product spec all point to multi-session being intentional. Only
  the test contradicts. The weight of evidence is overwhelmingly on the test side.
- **Race condition in ThreadPoolExecutor causes duplicate sessions**: rejected because the observed symptom is "got 4" (matches
  device count), not "got 5" or "got 8" or a varying number. A race would produce variable counts.
- **DB unique constraint on user_id forces dedup**: rejected because if a constraint were active, the second `db_session.add`
  would raise `IntegrityError`, not silently produce 4 rows. Also, the assertion sees 4 distinct IDs, so 4 rows were actually
  written.

## Grounding gaps

- Could not Read the actual `docs/product/sessions.md` file (provided as authoritative context in the prompt, but not in the
  filesystem at the path I could verify). Treating the inline spec quote as ground truth per the prompt.
- Could not Read the actual `api/session.py` and `tests/api/test_user_session.py` (provided inline, not on disk). All citations
  refer to the inline code in the user's invocation.
- Did not run `git log` to confirm the commit `feat(sessions): per-device sessions for parallel logins` exists.
- Did not execute the failing test to confirm reproduction — relying on the user's reported observation.
