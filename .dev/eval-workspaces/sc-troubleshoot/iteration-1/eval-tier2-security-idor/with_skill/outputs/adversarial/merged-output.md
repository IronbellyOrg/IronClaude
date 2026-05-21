# Merged Fix Proposal — IDOR closure for `get_user_profile`

## Diagnosis (consensus)

`GET /api/users/<int:user_id>/profile` is a real IDOR. `@login_required` authenticates the requester but the function does not authorize them against the `user_id` URL parameter. Any authenticated user can fetch any other user's PII (email, phone, address, DOB) by changing the integer in the URL. The mobile-app-only-passes-own-id argument is irrelevant: the server is the security boundary, not the client.

## Recommended Fix (chosen)

Add a 2-line authorization check at the top of `get_user_profile`, *before* the database lookup:

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

**Why before the DB lookup**: avoids leaking user existence via 404-vs-403 timing, and avoids hitting the database for unauthorized requests.

## Tests

Three new tests:

1. `test_get_user_profile_own_id_returns_200` — mobile-app pattern still works.
2. `test_get_user_profile_other_user_id_returns_403` — attacker pattern blocked with no PII in body.
3. `test_get_user_profile_nonexistent_id_returns_403_not_404` — enumeration prevention.

## Follow-up tasks (separate tickets — do not block this fix)

1. **Repo-wide IDOR audit** — grep all `<int:.*_id>` Flask routes for missing ownership checks.
2. **Structural redesign** — migrate `/api/users/<id>/*` to `/api/users/me/*` over the next 1–2 mobile-app release cycles. This eliminates the IDOR bug class at the API design level.
3. **Coding standard** — document and (if possible) lint-enforce the rule "every parameter-derived resource access requires an explicit ownership check after `@login_required`."

## Risks

- **Likelihood of regression**: low. Single comparison against a Flask-Login invariant.
- **Test coverage of changed code**: good after the three new tests are added.
- **Rollback**: `git revert` the 2-line change.
- **Blast radius blindspot**: this fix protects ONE endpoint. Follow-up task #1 is essential.

## Self-Review (post-merge)

- Tests cover the fix? ✓ (3 tests, both positive and negative paths)
- Edge cases handled? ✓ (own/other/nonexistent ids all tested)
- Requirements satisfied? ✓ (closes the SAST finding; preserves mobile-app contract)
- Follow-up captured? ✓ (3 follow-up tasks documented)
- Self-review verdict: **OK — no blocker. Proceed to Wave 5.**
