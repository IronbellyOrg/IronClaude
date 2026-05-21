# Hypothesis: Confirmed IDOR — fix is an explicit authorization check, ideally combined with a longer-term API redesign to `/users/me/profile`

**Agent**: security-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:01:00Z
**Cause class**: Security — IDOR (OWASP A01:2021 Broken Access Control)

## Claim

This is a textbook IDOR. `@login_required` proves the requester has *a* valid session; it does not prove they are entitled to *this* `user_id`. The mobile-app-only-sends-own-id argument is a category error: it treats the client as a security boundary. It is not. Anyone with a session token (legitimate user, attacker who phished a token, attacker who XSS'd the mobile app's webview, attacker with a stolen device) can iterate `user_id` from 1..N and exfiltrate every user's PII — email, phone, full address, DOB. That is a GDPR / CCPA reportable incident at scale.

The fix is an authorization check. The *better* fix is also dropping the parameter — but that's a refactor, and we should not block the IDOR closure on a refactor.

## Evidence

- `api/users.py:8–11` — route declares `<int:user_id>` as a URL parameter, `@login_required` decorator (line 9) does authentication only, `User.query.get(user_id)` (line 11) uses the parameter directly without authorization.
- `api/users.py:3` — `from flask_login import login_required, current_user` — `current_user` is imported but the function body never references it. This is a strong signal that authorization was forgotten, not factored out elsewhere.
- `api/users.py:15–20` — response payload includes PII (email, full_name, phone, address, date_of_birth). Sensitivity classification: **High**. Disclosure scope at risk: **all users**.
- OWASP Top 10 2021 — A01:2021 Broken Access Control is the #1 web app risk. IDOR via URL parameter manipulation is the canonical example.

## Proposed Fix

**Immediate (commit today)**: insert an authorization guard at the top of `get_user_profile`, *before* the database lookup:

```python
@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
@login_required
def get_user_profile(user_id: int):
    if user_id != current_user.id:
        abort(403)
    user = User.query.get(user_id)
    if user is None:
        abort(404)  # only reachable for own user — no enumeration risk
    return jsonify({ ... })
```

Place the check **before** the DB lookup so unauthorized requests:

1. Don't hit the database (DOS resistance).
2. Don't leak existence via 404-vs-403 timing.

**Follow-up (separate task, not blocking)**: deprecate `/api/users/<user_id>/profile` in favor of `/api/users/me/profile` that reads from `current_user` only. This eliminates the IDOR class of bug at this endpoint forever — there is no parameter to manipulate. Coordinate with mobile app team for a versioned rollout.

**Repo-wide audit (separate task, not blocking)**: grep for `/api/users/<` and `/api/.+/<int:` to find sibling endpoints with the same pattern. This single fix does not protect them.

Files to change:

- `api/users.py` — add 2 lines (`if user_id != current_user.id: abort(403)`).

Tests:

- `test_get_user_profile_own_id` — user A → 200 with A's data.
- `test_get_user_profile_other_id_returns_403` — user A → user_id=B → 403, response body contains no PII.
- `test_get_user_profile_nonexistent_id_returns_403` — user A → user_id=99999 → 403 (not 404), to prevent enumeration.

## Confidence

Self-reported: 0.97

Per-dimension:

- Evidence grounding: 1.0 — direct citations to the vulnerable lines.
- Symptom coverage: 1.0 — fix addresses the entire SAST finding.
- Reproducibility fit: 1.0 — exploit is trivial to demonstrate (`curl -H "Cookie: session=..." /api/users/2/profile` as user 1).
- Fix directness: 1.0 — 2-line addition to the exact vulnerable function.
- Domain coherence: 1.0 — pure security fix in a single function.

**Calibrated: 0.97**

## Risks

- **Existence leak via 404**: if the authz check is placed *after* the DB lookup + `abort(404)`, attackers can still distinguish "user exists" from "user doesn't exist." The fix above places the check *before* the lookup specifically to prevent this.
- **Repo-wide blindspot**: this fix protects ONE endpoint. The same bug pattern may exist on `/api/users/<id>/settings`, `/api/users/<id>/orders`, etc. The follow-up audit task is essential.
- **Permission middleware drift**: if a future engineer adds new fields to the response without re-reading this check, the IDOR could regress in the response body if the response is composed in a different function. Low risk given the current single-function structure.

## If I'm wrong, it's probably because

…there is undisclosed admin-portal logic that legitimately needs to fetch other users' profiles (e.g. customer support tool). In that case the fix should be `if user_id != current_user.id and not current_user.is_admin: abort(403)` — but this should be confirmed with the application team before generalizing.

## Alternatives considered

- **Fix B: drop the `<user_id>` parameter, use `/users/me/profile`** — Architecturally cleaner; eliminates the bug class. Rejected as the *immediate* fix because: (1) it requires a mobile-app coordinated release, (2) it doesn't help any other client of the API, (3) the authz check is a 2-line change that closes the bug today. Strong candidate as a follow-up.
- **Fix C: role-based access (`is_admin` short-circuit)** — Rejected as the *initial* fix because there is no current admin requirement in the snippet; adding it now is scope creep. Should be added only if the application has admin users.

## Grounding gaps

- Cannot see middleware / decorator stack — assumed `@login_required` is the only auth-related decoration.
- Cannot run the Flask app to demonstrate the exploit live.
- No access to the broader `api/` directory to perform the repo-wide audit recommended in the follow-up.
