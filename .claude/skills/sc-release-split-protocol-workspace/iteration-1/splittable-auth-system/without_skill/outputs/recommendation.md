# Release Split Recommendation: v3.2 Unified Auth System

## Recommendation: SPLIT into Two Releases

**Confidence: HIGH** — The spec has a clean dependency boundary, the priority tiers already encode the split, and the risk profile strongly favors incremental delivery.

---

## Proposed Release Structure

### Release A: v3.2.0 — Unified Auth Foundation

**Scope:** R1 (Identity Model) + R2 (Permission Store) + R3 (Token Service) + R4 (Auth Middleware)

**What ships:**
- `Identity` model with multi-credential support and canonical UUID
- RBAC permission engine with role hierarchy and resource-level scoping
- JWT token service with issuance, refresh, revocation, and introspection
- Unified auth middleware replacing the three separate middleware stacks
- Shadow mode deployment: new system runs alongside old, compares decisions, does not enforce
- Database schema: `identities`, `credentials`, `roles`, `identity_roles`, `permissions`, `tokens`, `audit_log`

**Estimated scope:** ~1200-1500 lines production code (60-65% of total)

**Testing:**
- Unit tests for identity model, permission engine, token service
- Integration tests for middleware with all three credential types
- Security audit of new auth endpoints
- Shadow mode begins (2-week validation window)

**Success criteria for this release:**
- Unified service deployed in shadow mode
- All three auth mechanisms produce consistent identity resolution in shadow mode
- Token revocation propagates within 1 second
- Zero permission escalation paths detected during shadow validation
- Audit log produces canonical UUIDs for all auth events

**Rollout:**
1. Deploy unified service in shadow mode
2. Monitor for 2 weeks: compare old vs new auth decisions
3. Fix any discrepancies found
4. Gate: shadow mode shows <0.1% decision divergence before Release B proceeds

---

### Release B: v3.2.1 (or v3.3.0) — Migration, Management & SDK Adoption

**Scope:** R5 (Migration Framework) + R6 (Admin Dashboard) + R7 (SDK Updates)

**What ships:**
- Automated identity merging tool with conflict resolution
- Rollback capability during migration window
- Admin dashboard for identity/role/permission management and audit log viewer
- Updated Python SDK, JavaScript SDK, and CLI tool
- Backward-compatible wrappers for deprecated old auth methods
- Cutover from shadow mode to enforcement

**Estimated scope:** ~700-1000 lines production code (35-40% of total)

**Prerequisites (from Release A):**
- Shadow mode validation passed
- Core auth service stable in production for >= 2 weeks
- No critical issues in shadow mode comparison

**Testing:**
- Migration tests with production-like data sets
- Dashboard integration tests
- SDK compatibility tests (new + backward-compat wrappers)
- End-to-end: migrate test environment, switch to enforcement, validate all flows

**Success criteria for this release:**
- Identity migration completes without user-facing downtime
- Cross-system audit correlation works via canonical UUID
- SDKs authenticate successfully through new endpoints
- Old auth methods work through backward-compatible wrappers

**Rollout:**
1. Migrate identity data (with rollback capability)
2. Switch Web UI to unified auth (kill switch available)
3. Switch CLI to unified auth
4. Switch plugins to unified auth
5. Legacy auth removal deferred to v4.0 (as original spec states)

---

## Why This Split Works

### 1. Clean dependency boundary
R1-R4 form a self-contained foundation. R5-R7 consume that foundation. There are no circular dependencies across the boundary.

### 2. Priority tiers match the split
The spec already marks R1-R3 as P0 and R5-R7 as P1/P2. The split follows the spec's own priority judgment.

### 3. Shadow mode is the natural gate
The spec calls for 2 weeks of shadow mode validation. This is a natural release boundary — ship the service, validate it, then ship the migration and adoption tooling. Cramming everything into one release wastes the shadow mode signal.

### 4. Risk reduction is substantial
The biggest risk in this project is breaking auth for all users simultaneously. Splitting ensures the core engine is production-validated before any user migration occurs. If the permission engine has a flaw, you discover it in shadow mode — not during live migration.

### 5. Independent team velocity
Backend/security engineers build Release A. Frontend engineers (dashboard), developer relations (SDKs), and platform engineers (migration) build Release B. These teams can start Release B work in parallel with Release A's shadow mode validation period.

---

## Timeline Estimate

| Phase | Duration | Notes |
|-------|----------|-------|
| Release A development | 3-4 weeks | Identity model, permission engine, token service, middleware |
| Release A shadow mode | 2 weeks | As specified in original rollout plan |
| Release B development | 2-3 weeks | Can overlap with shadow mode period |
| Release B rollout | 1-2 weeks | Staged cutover per system |
| **Total** | **6-8 weeks** | vs. estimated 5-7 weeks for monolithic (but with higher risk) |

The split adds roughly 1 week of overhead (two deployments, gate validation) but substantially reduces the risk of a catastrophic auth failure affecting all users.

---

## What NOT to Split Further

Splitting below two releases would be counterproductive:

- **R1/R2/R3 should not ship separately.** They are tightly coupled through R4 (middleware). Shipping the identity model without the permission engine creates a half-built system with no value.
- **R5/R6/R7 could theoretically ship separately** but the overhead of three additional releases outweighs the benefit. They are all "adoption layer" work of moderate size.

---

## Summary

| Aspect | Single Release | Split (Recommended) |
|--------|---------------|---------------------|
| Releases | 1 | 2 |
| Max blast radius | All auth for all users | Limited to shadow mode (Release A) or staged cutover (Release B) |
| Shadow mode utility | Compressed | Full 2-week validation gate |
| Rollback complexity | High (7 components) | Low (3-4 components per release) |
| Team parallelism | Blocked on single train | Independent after Release A |
| Total timeline | 5-7 weeks | 6-8 weeks (+1 week for safety) |
| Risk profile | HIGH | MEDIUM-LOW |
