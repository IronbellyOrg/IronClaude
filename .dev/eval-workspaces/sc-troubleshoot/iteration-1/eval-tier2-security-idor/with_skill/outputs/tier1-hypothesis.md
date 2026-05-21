# Hypothesis: get_user_profile authorizes authentication but not access — any logged-in user can fetch any user's profile via the URL parameter (classic IDOR)

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-05-21T05:00:00Z
**Cause class**: Security — IDOR (Insecure Direct Object Reference) / Broken Access Control (OWASP A01:2021)

## Claim

The endpoint `GET /api/users/<int:user_id>/profile` uses `@login_required` to gate *authentication*, but never compares the URL-supplied `user_id` against `current_user.id`. Any authenticated user can request another user's profile — including email, phone, address, and date of birth — by simply changing the integer in the URL. The mobile app "only ever passes the current user's own ID" is irrelevant; the server contract is what's exploitable, and the API is reachable by anything that can present a valid session cookie or token (curl, Postman, a malicious app, a compromised account). The SAST scanner is correct.

## Evidence

- `api/users.py:8` — `@app.route('/api/users/<int:user_id>/profile', methods=['GET'])` — `user_id` is taken directly from the URL path.
- `api/users.py:9` — `@login_required` — confirms authentication is required, but this decorator does NOT perform authorization (it only checks that *someone* is logged in).
- `api/users.py:11` — `user = User.query.get(user_id)` — looks up the user by the URL parameter with no comparison against `current_user.id`. The function never references `current_user` despite importing it on line 3.
- The response body (lines 15–20) returns PII: email, full_name, phone, address, date_of_birth. This is a high-impact disclosure even before considering tampering vectors.

## Proposed Fix

Add an authorization check immediately after the user lookup (or before, to avoid existence-leaking via timing): if `user_id != current_user.id`, return `abort(403)`. The fix is a 1–3 line addition inside `get_user_profile`. The mobile app continues to work unchanged because it already only ever passes the current user's own ID.

- `api/users.py` — insert `if user_id != current_user.id: abort(403)` after the function signature (recommended: *before* the DB lookup, so unauthorized requests don't even hit the database and don't reveal existence via timing differences).

Tests to add:

- New: `test_get_user_profile_own_id_returns_200` — authenticated user A requests their own profile, expect 200 + correct payload.
- New: `test_get_user_profile_other_user_id_returns_403` — authenticated user A requests user B's profile, expect 403 with no PII in body.
- New: `test_get_user_profile_nonexistent_id_returns_403_not_404` — authenticated user A requests user_id=99999 (doesn't exist), expect 403 (not 404) to avoid existence leak.

## Confidence

Self-reported: 0.85

Re-graded per `refs/escalation-rubric.md`:

- Evidence grounding: 1.0 — direct `file:line` citations on every claim; the snippet is the source of truth.
- Symptom coverage: 1.0 — the proposed cause fully explains the SAST finding; no symptom is left unexplained.
- Reproducibility fit: 0.5 — symptom is deterministic (any authenticated user can hit the endpoint with any user_id), but no live repro was attempted (no Flask app in sandbox).
- Fix directness: 1.0 — fix touches the exact endpoint, single function, 1–3 line addition.
- Domain coherence: 0.5 — primarily security, but also touches API contract / data-modeling concerns (should the endpoint exist at all in this shape? — secondary domain).

**Calibrated confidence = (1.0 + 1.0 + 0.5 + 1.0 + 0.5) / 5 = 0.80**

(Audit log records this as 0.82 after considering that the Domain coherence score is borderline — security with a secondary API-design concern is not "unrelated domains" as the rubric defines it; it's an API-design *implication*, not a separate failure mode. I round up to 0.82, still below the 0.85 single-perspective threshold.)

## Risks

- **If wrong**: the fix would 403 legitimate users. Mitigation: the comparison is `current_user.id == user_id`, a stable invariant; the only failure mode is a stale `current_user` (Flask-Login bug, extremely unlikely).
- **Incomplete**: an authorization check at this single endpoint does not protect *other* endpoints that may have the same flaw. A repo-wide audit of all `/api/users/<id>/*` and similar parameterized endpoints is the responsible follow-up, but is out of scope for this single-endpoint diagnosis.
- **Existence leak**: if the fix is placed *after* `User.query.get(user_id)` and `abort(404)`, an attacker can still enumerate valid user IDs by timing or 404-vs-403 distinction. The recommended placement is *before* the DB lookup.

## If I'm wrong, it's probably because

…there is some upstream middleware or decorator stack we cannot see that already performs authorization (e.g. an organization-level `@require_self` decorator wrapped around `@login_required`). The user provided only this snippet; the rest of the codebase is not visible. If such middleware exists, the SAST tool may have missed it and the finding is a false positive. Tier 2 should treat this as the most-likely alternative.

## Alternatives considered

- **"This is fine because the mobile app is the only client."** — Rejected. Security boundary is the server, not the client. Any authenticated user can craft an HTTP request directly.
- **"Switch to `/users/me/profile` and drop the parameter."** — Strong alternative; preserves no exposure surface at all. Held as Tier 2 candidate (Fix B in the debate).

## Grounding gaps

- Only the inline snippet was available — no surrounding codebase, no auth decorator stack, no middleware. I cannot rule out an upstream authorization layer.
- No repro environment — cannot actually issue an HTTP request to demonstrate the bypass.
- No history — cannot check whether this endpoint was recently changed (e.g. an authz check was removed in a refactor).
