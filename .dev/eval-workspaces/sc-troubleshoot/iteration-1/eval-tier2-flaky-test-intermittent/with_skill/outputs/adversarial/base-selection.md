# Base Selection

**Selected base**: **Fix-2 (DB UNIQUE constraint + `IntegrityError`-handled insert)**

## Rationale

Fix-2 is selected as the merge base because it is the only proposal that:

1. **Closes both the immediate test and the production invariant** in one ship. Fix-1 closes only the test (single-process); Fix-4 also does both but at significantly higher diff cost.
2. **Surfaces the latent multi-process bug** that Fix-1 leaves unaddressed.
3. **Has a clear, well-known migration path** (UNIQUE constraint + IntegrityError handling) that is database-agnostic and reversible.
4. **Forces product confirmation** of the "one session per user" invariant before shipping — that confirmation is required eventually regardless of which fix lands, so making it a blocker on Fix-2 is correct.

Fix-1 is **integrated as a layered short-term mitigation** to stop the bleeding while Fix-2's migration is coordinated.

Fix-4's structural improvements (deleting `_session_cache`, switching to `SessionLocal()` context) are **integrated as forward-looking follow-ups** in the merged plan — they are good ideas that do not need to ship in the same PR.

The `db_session` thread-safety question is **integrated as a pre-flight blocker** that must be answered *before* any of the three fixes lands.

## What this base inherits from the other proposals

- **From Fix-1**: the same-PR short-term mitigation (process-local lock) to land alongside Fix-2's schema migration in the unusual case where the migration cannot land within one deploy window.
- **From Fix-4**: the test improvement (DB-readback assertion), the test-cleanup (remove `_session_cache.clear()`) deferred to a follow-up, and the implicit `db_session` lifecycle improvement deferred to a follow-up.

## What this base explicitly does **not** inherit

- **From Fix-5 (performance-engineer)**: per-key locking. Deferred to a follow-up if profiling shows the global lock contention is a real problem; not needed for correctness.
- **From Fix-3 (root-cause-analyst Tier 2)**: full `scoped_session` migration as a same-PR change. Confirmed as a pre-flight; the *audit* lands now, the *migration* (if needed) lands in a follow-up.
