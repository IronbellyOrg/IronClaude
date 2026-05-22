# Hypothesis: Real IDOR. Authz check is necessary but insufficient — the durable fix is removing the parameter (`/users/me/profile`); authz check is the bridge

**Agent**: quality-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:01:00Z
**Cause class**: Security — IDOR + API design smell (unnecessary parameter)

## Claim

The SAST finding is correct, but framing it purely as "missing authz check" misses the testability / maintainability dimension. The endpoint accepts a parameter it has no legitimate reason to vary on — the only valid value of `user_id` is `current_user.id`. Every other value is an error. The most robust fix is to remove the degree of freedom: replace `/api/users/<int:user_id>/profile` with `/api/users/me/profile` that reads from `current_user` directly. The authz check (security-engineer's fix) is the right *immediate* patch, but the API itself should change so the bug class becomes impossible to reintroduce.

## Evidence

- `api/users.py:8` — URL declares `<int:user_id>` as a parameter, but per the user's description "mobile app only ever passes the current user's own ID." This is a parameter with exactly one valid value per session — a classic API design smell.
- `api/users.py:11` — `User.query.get(user_id)` performs a DB lookup that is entirely redundant when the only valid `user_id` is `current_user.id` (Flask-Login already loaded `current_user` from the session).
- Test-coverage angle: an authz check requires *negative* tests (other user → 403, nonexistent → 403) to prove correctness; removing the parameter requires only *positive* tests (own profile → 200). Fewer tests, smaller blast radius for regressions.
- Quality smell: parameters that have exactly one valid value are dead weight — they invite bugs (this one), confuse API consumers (does the parameter mean something? can I pass another value?), and make API documentation lie.

## Proposed Fix

**Preferred (medium-term, requires mobile app coordination)**: replace the endpoint entirely.

```python
@app.route('/api/users/me/profile', methods=['GET'])
@login_required
def get_my_profile():
    user = current_user  # already loaded by Flask-Login from session
    return jsonify({
        'id': user.id,
        'email': user.email,
        'full_name': user.full_name,
        'phone': user.phone,
        'address': user.address,
        'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
    })
```

No URL parameter → no IDOR class possible. No DB lookup (saves a query per request). The mobile app team updates the endpoint URL in their next release.

**Bridge (immediate, ships today)**: keep the existing endpoint and add the authz check (security-engineer's Fix A) so the bug is closed *now*. Deprecate the parameterized endpoint over the next two mobile-app release cycles.

Files to change (preferred):

- `api/users.py` — new function `get_my_profile`, decorator points to `/api/users/me/profile`.
- Mobile app: update endpoint URL (separate repo / team).

Files to change (bridge):

- `api/users.py` — 2-line authz check (same as security-engineer).

Tests (preferred):

- `test_get_my_profile_returns_current_user_data` — single positive test, no negative tests needed because the bug class is impossible.

Tests (bridge):

- Three tests as in security-engineer's proposal.

## Confidence

Self-reported: 0.88

Per-dimension:

- Evidence grounding: 1.0 — direct citations.
- Symptom coverage: 1.0 — both proposals close the IDOR; the redesign also eliminates the bug class.
- Reproducibility fit: 1.0 — IDOR deterministically exploitable today.
- Fix directness: 0.5 — preferred fix is a redesign (not directly minimal); bridge fix is 2 lines.
- Domain coherence: 0.5 — primarily security, but the recommendation is also about API design / testability.

**Calibrated: (1.0 + 1.0 + 1.0 + 0.5 + 0.5) / 5 = 0.80**

## Risks

- **Coordinated release dependency**: removing the parameter requires the mobile app team to update. Until they ship, both endpoints must coexist OR the old endpoint must continue to work with the authz patch in place. Recommend running both endpoints in parallel during the migration window.
- **Sticky old endpoint**: experience shows deprecated endpoints linger. If the parameterized endpoint stays around, the authz check (the bridge) is permanent, not temporary. That's OK — defense in depth.
- **Backwards-compat assumption**: if there are non-mobile clients (web app, admin tools, third-party integrations) that legitimately use the parameter, the redesign cannot proceed without first auditing them. The bridge fix has no such dependency.

## If I'm wrong, it's probably because

…the redesign is judged out-of-scope for a "fix the SAST finding" task. In that case ship the bridge (Fix A) and file the redesign as a separate ticket. The bridge is sufficient to close the SAST finding.

## Alternatives considered

- **Fix A (security-engineer)**: the bridge. Strongly endorsed as the immediate fix; I differ only in advocating that the redesign be tracked as the eventual replacement.
- **Fix C (role-based)**: out of scope without a stated admin requirement.

## Grounding gaps

- Don't know the full list of API consumers — can't confirm whether the redesign is safe to plan.
- Don't know the mobile app release cadence — can't estimate migration timeline.
