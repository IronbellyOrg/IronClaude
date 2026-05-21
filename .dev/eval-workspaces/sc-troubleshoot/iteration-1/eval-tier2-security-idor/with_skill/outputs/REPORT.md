# Troubleshoot Report — IDOR in `/api/users/<user_id>/profile`

**Command**: `/sc:troubleshoot --type security` (NEW protocol skill)
**Tier reached**: 2 (escalated under `security_caution` rule) | **Confidence**: 0.93 | **Status**: success
**Source**: subagent inline output (REPORT.md write blocked; sibling artifacts written: audit.log, 4 hypothesis cards, candidate-fixes.md, fix-proposals/, adversarial/)

## Summary

Real IDOR vulnerability. `@login_required` authenticates the caller but never authorizes them against the URL `user_id`. `current_user` is imported but never referenced. The "mobile app only sends own ID" defense is irrelevant — the server is the trust boundary.

## Diagnosis

**Root cause**: missing authorization between `@login_required` and the database lookup. The handler accepts a caller-supplied `user_id` from the URL, loads that user, and returns PII (email, phone, address, DOB) with no check that the caller is allowed to view that user's profile.

## Evidence

1. `api/users.py:7` — `from flask_login import login_required, current_user` (imported)
2. `api/users.py:10-12` — `@login_required` runs; `current_user` populated
3. `api/users.py:13` — `user = User.query.get(user_id)` — load by URL-supplied ID, never compared to `current_user.id`
4. `api/users.py:16-22` — returns PII unconditionally
5. **Missing**: any `if user_id != current_user.id` check or role-based authorization

## Proposed Fix (winner of adversarial debate — Fix A)

Insert an authorization check **before** the database lookup:

```python
@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
@login_required
def get_user_profile(user_id: int):
    if user_id != current_user.id:
        abort(403)
    user = User.query.get(current_user.id)
    if user is None:
        abort(404)
    return jsonify({ ... })
```

Why before the DB lookup: (a) avoids unnecessary DB hit on rejected requests; (b) returns 403 (authorization failure) instead of 404, which prevents user-enumeration via timing/response differences. (Note: some IDOR guidance prefers 404 for both unauth and not-found to avoid existence leaks — the team should pick a consistent policy; the merged fix uses 403 with a follow-up to standardize.)

## Test Plan

Three regression tests:

1. Own ID → 200 with profile body
2. Another user's ID → 403 (no PII leaked)
3. Nonexistent ID → 403 (not 404 — same response shape as unauthorized to prevent enumeration)

## Alternative Fixes Considered

- **Fix B — Redesign to `/users/me/profile`**: drops the URL parameter entirely; server reads `current_user.id`. Eliminates the IDOR class at the API-shape level. Rejected as the immediate fix (requires client coordination) but **retained as a follow-up** task `T-IDOR-redesign`.
- **Fix C — Role-based authorization (admins can read any user)**: dropped as outlier — premature generalization; no requirement was stated for admin reads.

## Risk + Rollback

- **Likelihood of regression**: Low. 2-line addition to a single handler.
- **Test coverage**: Currently partial; the 3 new tests close the gap.
- **Rollback**: `git revert` returns to the vulnerable state. The regression tests will fail and surface the revert.

## Follow-ups (separate tickets)

1. Repo-wide audit of `<int:.*_id>` routes for the same defect class.
2. Structural redesign to `/users/me/*` (Fix B).
3. Adopt a coding-standard rule: handlers with `<int:user_id>` URL parameters must include an explicit authorization assertion.

## Tier 2 Process

- Tier 1 confidence: 0.82 → escalated under `security_caution` (security type + confidence < 0.95).
- Agents (inline simulation): security-engineer, root-cause-analyst, quality-engineer.
- Wave 4 adversarial debate (`--depth quick`) selected Fix A; Fix B retained as follow-up; Fix C dropped.
- Self-review PASS.

## Audit

- Hypothesis cards: `tier1-hypothesis.md`, `tier2-security-engineer-hypothesis.md`, `tier2-root-cause-analyst-hypothesis.md`, `tier2-quality-engineer-hypothesis.md`
- Candidate fixes: `candidate-fixes.md`
- Fix proposals: `fix-proposals/fix-{A,B}.md`
- Adversarial artifacts: `adversarial/merged-output.md` (+ debate-transcript, base-selection)
- Audit log: `audit.log`
