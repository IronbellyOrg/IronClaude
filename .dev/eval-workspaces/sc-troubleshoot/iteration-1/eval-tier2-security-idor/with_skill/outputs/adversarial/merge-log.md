# Merge Log

| Source | Idea | Kept | Reason |
|--------|------|------|--------|
| Fix 1 | 2-line inline authz check | YES | Selected as merge base |
| Fix 1 | Place check *before* DB lookup | YES | Avoids enumeration via 404-vs-403 |
| Fix 1 | 3 tests (positive + 2 negatives) | YES | Security-property assertions survive future migration |
| Fix 2 | Redesign to `/api/users/me/profile` | DEFERRED → follow-up task #2 | High-value, low-urgency; can't block IDOR closure on a redesign |
| Fix 2 | Drop the URL parameter entirely | DEFERRED → follow-up task #2 | Same reasoning |
| Fix 2 | Single-test posture (no negative tests needed) | DROPPED | Negative tests are valuable even with the parameter present; they prove the authz check exists in the test suite |
| Fix C (outlier) | `is_admin` bypass | DROPPED | No admin requirement stated; scope creep |
| root-cause-analyst variant | Extract `_can_view_user_profile` helper | DROPPED | Pleasant abstraction, not necessary; can be introduced on next reuse |
| security-engineer | Repo-wide audit recommendation | KEPT as follow-up task #1 | Critical to avoid blind-spot in sibling endpoints |
| quality-engineer | Document API smell as architectural debt | KEPT in refactor-plan + REPORT alternatives section | Keeps Fix 2 on the radar |
| security-engineer | Observability — watch 403 rate after deploy | KEPT in refactor-plan | Detects exploitation + regressions |
