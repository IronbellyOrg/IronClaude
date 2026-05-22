# Fix Proposal 1 — Inline Authorization Check

## Problem Statement

`GET /api/users/<int:user_id>/profile` accepts any authenticated user's request and returns the requested profile (PII included) regardless of whether the requester owns that profile. This is a textbook IDOR: `@login_required` proves identity but not authorization.

## Proposed Change

Add an authorization guard at the top of `get_user_profile`, *before* the database lookup:

```diff
 @app.route('/api/users/<int:user_id>/profile', methods=['GET'])
 @login_required
 def get_user_profile(user_id: int):
+    if user_id != current_user.id:
+        abort(403)
     user = User.query.get(user_id)
     if user is None:
         abort(404)
     return jsonify({ ... })
```

Two lines. Placement is *before* `User.query.get(...)` so:

- Unauthorized requests don't hit the database (avoids DOS leverage).
- Existence cannot be probed via 404-vs-403 (avoids enumeration).

## Evidence

- `api/users.py:8–11` — endpoint takes `user_id` from URL with no authz check after `@login_required`.
- `api/users.py:3` — `current_user` is imported but never referenced in the function body. Smoking-gun signal that authz was intended.
- `api/users.py:15–20` — response leaks PII (email, phone, address, DOB) to whoever can request the URL.

## Risks

- Single endpoint only — sibling endpoints (if any) are not protected. Requires a follow-up audit task.
- If a stale `current_user` is possible (Flask-Login bug, very unlikely), the comparison could permit access. Mitigated by relying on Flask-Login's invariant.

## Test Plan

- `test_get_user_profile_own_id_returns_200` — user A requests their own profile → 200, payload matches A's data.
- `test_get_user_profile_other_user_id_returns_403` — user A requests user B's profile → 403, response body contains no PII.
- `test_get_user_profile_nonexistent_id_returns_403` — user A requests `user_id=999999` (no such user) → 403, NOT 404 (prevents enumeration).
- Update integration suite to confirm mobile-app's request pattern (own id) still works unchanged.

## Files Changed

- `api/users.py` — +2 lines inside `get_user_profile`.

## Time-to-Ship

Today. No coordination required with other teams. No URL contract change.
