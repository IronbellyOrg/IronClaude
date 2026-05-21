# Refactor Plan — Merged Proposal

## Immediate change (this commit)

Edit `api/users.py`:

```diff
 @app.route('/api/users/<int:user_id>/profile', methods=['GET'])
 @login_required
 def get_user_profile(user_id: int):
+    if user_id != current_user.id:
+        abort(403)
     user = User.query.get(user_id)
     if user is None:
         abort(404)
     return jsonify({
         'id': user.id,
         'email': user.email,
         'full_name': user.full_name,
         'phone': user.phone,
         'address': user.address,
         'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
     })
```

Placement is *before* `User.query.get(user_id)` (line 11) so that unauthorized requests do not hit the database and cannot enumerate user existence via 404-vs-403 timing.

## Tests to add

In `tests/api/test_users.py` (or equivalent):

```python
def test_get_user_profile_own_id_returns_200(client, login_as):
    with login_as(user_id=1):
        r = client.get('/api/users/1/profile')
        assert r.status_code == 200
        assert r.json['id'] == 1

def test_get_user_profile_other_user_id_returns_403(client, login_as, create_user):
    create_user(id=2)
    with login_as(user_id=1):
        r = client.get('/api/users/2/profile')
        assert r.status_code == 403
        # No PII leaks in 403 body
        assert b'email' not in r.data

def test_get_user_profile_nonexistent_id_returns_403_not_404(client, login_as):
    with login_as(user_id=1):
        r = client.get('/api/users/999999/profile')
        assert r.status_code == 403  # NOT 404 — prevents enumeration
```

## Follow-up tasks (not in this commit — file as separate tickets)

1. **Repo-wide audit**: grep for `<int:.*_id>` in all Flask routes and verify each route has an ownership check after `@login_required`. Likely scope: every `api/*.py` file. Owner: security-engineer.
2. **API redesign**: replace `/api/users/<id>/*` endpoints with `/api/users/me/*` where possible. Requires mobile-app coordinated release. Owner: backend + mobile teams.
3. **Coding standard**: document the "every parameter-derived resource access requires an explicit ownership check" rule in the team's API guidelines. Add a CI rule (e.g. a lint that flags `@login_required` directly preceding `Model.query.get(<param>)` without an intervening check) if feasible.

## Rollback

`git revert` of the 2-line change. Single function, single file, no schema changes, no migrations.

## Observability

After deploy, watch logs for 403s on `/api/users/<id>/profile`. A spike indicates either:

- Attacker probing user IDs (the bug was being actively exploited — incident response).
- Mobile-app client bug (using wrong user_id).
- Stale session edge case (Flask-Login bug — unlikely).

Document the expected 403 baseline (near zero) before deploying so the on-call team knows what's anomalous.
