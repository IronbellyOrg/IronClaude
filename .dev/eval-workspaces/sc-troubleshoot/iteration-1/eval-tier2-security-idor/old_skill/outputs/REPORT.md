# REPORT.md — IDOR in `/api/users/<user_id>/profile`

**Command**: `/sc:troubleshoot` (old, snapshot baseline) | **Mode**: diagnose-only (no `--fix`)
**Source**: subagent inline output (harness blocked direct file write)

## 1. Analyze

SAST flagged `GET /api/users/<int:user_id>/profile` as IDOR. Endpoint requires login but takes the target user_id from the URL and returns PII (email, full_name, phone, address, DOB).

## 2. Investigate

IDOR (OWASP A01:2021, CWE-639) requires: caller-supplied object ID + missing per-request authorization.

| Check | Present? |
|---|---|
| Caller-supplied object id in URL | YES (`<int:user_id>`) |
| Authentication (`@login_required`) | YES |
| **Authorization (user_id vs current_user.id)** | **NO** |
| Returns sensitive PII | YES |

`current_user` is imported but never read. No equality check, no role check, no ACL.

The "mobile app only sends its own ID" claim is the canonical IDOR rationalization: the mobile client is outside the trust boundary. Any holder of a valid session can call `GET /api/users/<any_id>/profile` and receive PII.

**Verdict: SAST is correct — true-positive IDOR. Severity High (horizontal privilege escalation, PII disclosure; GDPR Art. 5/32 relevance).**

## 3. Propose — ranked solutions

### Option A (Recommended hotfix) — Identity-equality check

```python
@app.route('/api/users/<int:user_id>/profile', methods=['GET'])
@login_required
def get_user_profile(user_id: int):
    if user_id != current_user.id:
        abort(404)  # 404 not 403 — don't confirm the row exists
    user = User.query.get(current_user.id)
    if user is None:
        abort(404)
    return jsonify({...})
```

Risk: Low. ≤5-line diff.

### Option B (Durable design fix) — Drop the path param

Replace with `GET /api/users/me/profile`; read `current_user.id` server-side.

### Option C — Centralized authorization layer

Introduce `@authorize_self_or_role('admin')` or a policy library.

### Rejected

- Trust the mobile client (the root cause).
- UUIDs instead of ints (obscurity, not authorization).
- Rate-limiting alone.

**Ranking:** A (today) → B (next sprint) → C (if class-wide).

## 4. Resolve — gated

`--fix` not supplied. No files modified.

**Verification plan once fixed:**

- User A → `/api/users/<B.id>/profile` → 404, no PII.
- User A → `/api/users/<A.id>/profile` → 200.
- Re-run SAST; grep for other `<int:user_id>` / `<uuid:user_id>` routes with the same defect class.
