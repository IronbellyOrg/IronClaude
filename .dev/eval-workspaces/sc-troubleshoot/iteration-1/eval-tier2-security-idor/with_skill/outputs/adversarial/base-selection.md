# Base Selection

## Selected base: Fix 1 (Inline Authorization Check)

## Rationale

Selecting Fix 1 as the merge base because:

1. **Ships today** — closes a high-severity PII disclosure immediately. Fix 2 cannot match this without itself relying on Fix 1 as a bridge.
2. **Zero coordination cost** — no mobile-app release, no API contract change, no audit of other API consumers required to deploy.
3. **Reversibility** — single `git revert` removes the change. Fix 2 is much harder to roll back once the mobile app has migrated.
4. **Test value** — the negative-path tests written for Fix 1 (other user → 403, nonexistent → 403) are valuable security-property assertions that *survive* a later migration to Fix 2.
5. **Adversarial consensus** — both advocates and all 3 hypothesis agents endorse Fix 1 as the immediate answer; only the framing of "should Fix 2 be the followup" differs.

## What gets borrowed from Fix 2

Even though Fix 1 is the base, the merged proposal incorporates two ideas from Fix 2:

- Recommend Fix 2 as an explicit follow-up task (structural redesign) — keep it on the radar instead of letting it die as an "alternative considered."
- Document that the underlying API smell (parameter with one valid value) is the architectural debt. Fix 1 closes the bug; Fix 2 retires the smell.

## What gets dropped

- Fix C (role-based with `is_admin` bypass) — no admin requirement was stated. Adding it now is scope creep. Drop entirely; engineers can add it if/when an admin requirement is documented.
- The extracted-helper variant (root-cause-analyst's `_can_view_user_profile`) — pleasant abstraction but not necessary for a single-endpoint fix. Drop from the merge; engineers can introduce it the first time the predicate is reused.
