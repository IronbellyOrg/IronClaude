# Hypothesis: IDOR is real; root cause is conflating authentication with authorization. Fix with an explicit ownership predicate, future-proofed for role-based exceptions

**Agent**: root-cause-analyst
**Tier**: 2
**Timestamp**: 2026-05-21T05:01:00Z
**Cause class**: Security — Broken Access Control (IDOR)

## Claim

The root cause is a single missing check, but it is symptomatic of a deeper misunderstanding: `@login_required` is a *who is this?* gate, not a *what may they do?* gate. The function imports `current_user` (line 3) but never uses it — strong evidence that the author *intended* to compare ownership but forgot, or that an earlier version had the check and it was removed in a refactor. Either way, the fix is the same: an explicit ownership predicate. I recommend writing it in a way that admits a future `is_admin` exception without further refactoring, because nearly every production app eventually grows a customer-support need.

## Evidence

- `api/users.py:3` — `from flask_login import login_required, current_user` — `current_user` is imported but unused in this function. This is the smoking gun: unused-import-of-authz-primitive almost always means "authz was meant to be here."
- `api/users.py:9–11` — `@login_required` (auth) is followed directly by `User.query.get(user_id)` (lookup by URL parameter) with no intervening authz check. Standard IDOR shape.
- `api/users.py:15–20` — response exposes PII (email, phone, address, DOB). High-impact disclosure.
- Pattern-matching: this is the OWASP IDOR canonical example. The fix pattern (`if resource.owner_id != current_user.id: abort(403)`) is standard.

## Proposed Fix

A single authorization guard that is **extensible** (admits future role-based exceptions cleanly) and **placed before the DB lookup** (avoids enumeration via timing or 404-vs-403):

```python
def _can_view_user_profile(viewer, target_user_id: int) -> bool:
    """Authorization predicate — extracted for testability + future admin/staff exceptions."""
    return viewer.id == target_user_id  # extend here: "or viewer.is_admin"

@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
@login_required
def get_user_profile(user_id: int):
    if not _can_view_user_profile(current_user, user_id):
        abort(403)
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return jsonify({ ... })
```

Extracting the predicate into `_can_view_user_profile` adds 3 lines but pays for itself the first time an admin/staff exception is needed, and makes the authz logic *unit-testable* without spinning up Flask.

Files to change:

- `api/users.py` — add `_can_view_user_profile` helper + 2-line guard at top of function.

Tests:

- `test_can_view_user_profile_predicate` — unit-test the predicate directly (own id → True, other id → False).
- `test_get_user_profile_own_id_returns_200`.
- `test_get_user_profile_other_id_returns_403`.
- `test_get_user_profile_nonexistent_id_returns_403_not_404` (enumeration prevention).

## Confidence

Self-reported: 0.92

Per-dimension:

- Evidence grounding: 1.0 — direct citation including the smoking-gun `current_user` unused import.
- Symptom coverage: 1.0 — fix addresses the SAST finding and the inferred root cause (auth/authz confusion).
- Reproducibility fit: 1.0 — IDOR is deterministically exploitable.
- Fix directness: 0.5 — extracting the helper is slightly more than the minimum 2-line fix. Justified by testability but it is *not* the most direct possible change.
- Domain coherence: 1.0 — single-domain security fix.

**Calibrated: (1.0 + 1.0 + 1.0 + 0.5 + 1.0) / 5 = 0.90**

## Risks

- **Over-engineering risk**: the extracted helper is an extra abstraction. If the project values minimum-diff over testability, the inline check (security-engineer's fix) is preferable.
- **Helper drift**: if more endpoints copy/paste the helper instead of importing it, the abstraction loses its value. Mitigation: document the helper as the canonical pattern.
- **Same as security-engineer**: this fix does not protect sibling endpoints; repo-wide audit required.

## If I'm wrong, it's probably because

…the project's coding standards prefer flat, inline checks over extracted helpers (common in small Flask apps). In that case the security-engineer's 2-line fix is the better answer for this codebase.

## Alternatives considered

- **Fix A: inline 2-line check (security-engineer's proposal)** — Simpler. Equivalent security posture. Loses unit-testability of the predicate. Strong alternative.
- **Fix B: redesign to `/users/me/profile`** — Best long-term answer; should be a follow-up task, not the immediate fix.

## Grounding gaps

- No view of the project's coding standards / preference between inline checks vs extracted helpers.
- No view of sibling endpoints to confirm whether the predicate would be reused.
