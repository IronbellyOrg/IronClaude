# Fix Proposal 2 — Redesign to `/api/users/me/profile`

## Problem Statement

The `<int:user_id>` URL parameter on `GET /api/users/<int:user_id>/profile` has exactly one legitimate value per session (`current_user.id`). Every other value is an error. The parameter is a degree of freedom the API does not need, and that degree of freedom is what enables the IDOR. Closing the bug with an authz check leaves the design smell in place. The structural fix is to remove the parameter.

## Proposed Change

Replace the endpoint:

```python
@app.route('/api/users/me/profile', methods=['GET'])
@login_required
def get_my_profile():
    user = current_user  # already loaded from session
    return jsonify({
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'phone': user.phone,
        'address': user.address,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
    })
```

The old `/api/users/<int:user_id>/profile` endpoint is deprecated and removed over 1–2 mobile-app release cycles.

## Evidence

- `api/users.py:8` — URL accepts a parameter that, per the user's own description, has exactly one valid value per session.
- `api/users.py:11` — DB lookup is redundant: `current_user` is already loaded by Flask-Login.
- Bug-class elimination: with no URL parameter, the IDOR pattern is structurally impossible at this endpoint.

## Risks

- **Coordinated release**: requires mobile app team to update the endpoint URL. Not deployable today.
- **Other clients**: if non-mobile clients (web, admin tools, integrations) use the parameter, the redesign requires more coordination.
- **Deprecation lag**: the old endpoint remains exploitable until it is removed. During the migration window, the IDOR is still open unless Fix 1 is also applied as a bridge.

## Test Plan

- `test_get_my_profile_returns_current_user_data` — single positive test. No negative tests needed (no parameter to abuse).

## Files Changed

- `api/users.py` — new function + new route, deprecated old route.
- Mobile app — URL update.

## Time-to-Ship

1–2 mobile-app release cycles. Bug remains open during migration unless Fix 1 is applied as a bridge.
