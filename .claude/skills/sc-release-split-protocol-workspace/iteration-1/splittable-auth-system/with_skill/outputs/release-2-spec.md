---
release: 2
parent-spec: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/evals/files/spec-splittable-auth-system.md
split-proposal: split-proposal-final.md
scope: "Integration, Migration & Consumer Layers — middleware consolidation, migration framework, admin dashboard, SDK updates, and full system rollout"
status: draft
validation-gate: "blocked until R1 real-world validation passes"
---

# Release 2 — Integration, Migration & Consumer Layers

## Objective

Integrate the unified identity and permission foundation (delivered in Release 1) into the running system. Replace the three legacy auth middleware stacks with a single enforcement layer, migrate all existing users and permissions, deliver an admin dashboard for management, and update developer SDKs. Complete the full rollout plan including shadow mode and system switchover.

## Scope

### Included

1. **R4: Auth Middleware Consolidation (P1)** — From: original spec Section 3, R4
   - Request authentication (identity extraction from any credential type)
   - Permission checking against centralized store (Release 1)
   - Rate limiting per identity (not per credential)
   - Audit logging with canonical identity (Release 1 UUID)

2. **R5: Migration Framework (P1)** — From: original spec Section 3, R5
   - Automated identity merging for users with accounts in multiple systems
   - Conflict resolution for incompatible permissions
   - Rollback capability during migration window
   - Shadow mode: run unified system in parallel, compare results, don't enforce

3. **R6: Admin Dashboard (P2)** — From: original spec Section 3, R6
   - User search and identity management
   - Role assignment and permission grants
   - Audit log viewer with cross-system correlation
   - Active session management and forced logout

4. **R7: Developer SDK Updates (P2)** — From: original spec Section 3, R7
   - Python SDK: new `authenticate()` and `check_permission()` methods
   - JavaScript SDK: updated OAuth flow
   - CLI tool: new `auth login` and `auth token` commands
   - Backward-compatible wrappers for old auth methods (deprecated, removed in v4.0)

5. **Integration Tests** — From: original spec Section 5
   - Integration tests for auth middleware with each credential type
   - Migration tests with production-like data sets
   - R3 (Token Service) integration validation with R4 middleware (deferred from Release 1)

6. **Security Audit** — From: original spec Section 5
   - Penetration testing of new auth endpoints

7. **Shadow Mode Validation** — From: original spec Section 5
   - Compare old and new system decisions for 2 weeks

8. **Full Rollout Plan** — From: original spec Section 6
   - Deploy unified service in shadow mode (2 weeks)
   - Migrate identity data with rollback capability
   - Switch Web UI to unified auth (with kill switch)
   - Switch CLI to unified auth
   - Switch plugins to unified auth
   - Remove legacy auth systems (v4.0)

### Excluded

None — all original spec items not in Release 1 are in Release 2. Combined, Release 1 and Release 2 cover 100% of original scope.

## Dependencies

### Prerequisites (from Release 1)

All Release 1 deliverables must be complete and validated before Release 2 proceeds:

| Dependency | Release 1 Deliverable | Required For |
|-----------|----------------------|-------------|
| Unified Identity Model | R1 — stable, validated schema and model | R4 (identity extraction), R5 (identity merging), R6 (identity management), R7 (SDK auth methods) |
| Centralized Permission Store | R2 — stable RBAC engine with role hierarchy | R4 (permission checking), R5 (permission conflict resolution), R6 (role assignment) |
| Unified Token Service | R3 — stable token issuance/validation/revocation | R4 (token-based auth in middleware), R7 (SDK token commands) |
| Database Schema | 7 tables validated at production scale | R5 (migration target), R6 (dashboard queries) |

### External Dependencies

- Production environment for shadow mode deployment
- Security testing tools/team for penetration testing
- SDK distribution infrastructure (PyPI, npm, CLI release pipeline)
- Operations team for rollout coordination

## Real-World Validation Requirements

All validation must use actual functionality in production-like conditions. No mocks, no simulated tests.

1. **Middleware Integration Test**: Route real HTTP requests through the unified middleware with each credential type (session cookie, API key, OAuth bearer token). Verify:
   - Identity is correctly extracted regardless of credential type
   - Permission checks enforce the RBAC model from Release 1
   - Rate limiting applies per identity across credential types
   - Audit log entries use the canonical UUID

2. **Token-Middleware Integration Test** (deferred from Release 1): Verify:
   - Tokens issued by R3 are correctly validated by R4 middleware
   - Token revocation is enforced by the middleware within 1 second
   - Token refresh works end-to-end through the middleware

3. **Shadow Mode Validation**: Run the unified auth system in parallel with the legacy systems for 2 weeks. Verify:
   - Decision parity: unified system makes the same auth/deny decisions as legacy systems
   - No permission escalation: unified system never grants access that legacy denies
   - Performance parity: unified system responds within acceptable latency bounds

4. **Migration Validation**: Execute identity migration against production data. Verify:
   - All users across all three systems are migrated with correct identity merging
   - Permission conflicts are resolved without escalation
   - Rollback returns to pre-migration state with zero data loss

5. **Admin Dashboard Validation**: Operations team uses the dashboard for real identity management tasks. Verify:
   - User search returns correct results across unified identities
   - Role assignment and permission grants take effect immediately
   - Audit log viewer correctly correlates entries across original systems
   - Forced logout terminates all active sessions for the target identity

6. **SDK Validation**: Developers use updated SDKs against the unified auth endpoints. Verify:
   - Python SDK `authenticate()` and `check_permission()` work correctly
   - JavaScript SDK updated OAuth flow completes successfully
   - CLI `auth login` and `auth token` commands function end-to-end
   - Backward-compatible wrappers for old auth methods work during transition period

7. **End-to-End Switchover Validation**: Switch each system (Web UI, CLI, Plugins) to unified auth with kill switch. Verify:
   - Each system functions correctly with unified auth
   - Kill switch reverts to legacy auth without user-facing disruption

## Success Criteria

- All three auth mechanisms use the same identity model (from original spec Section 7)
- Cross-system audit correlation achievable via canonical UUID (from original spec Section 7)
- Token revocation propagates within 1 second end-to-end through middleware (from original spec Section 7)
- Zero permission escalation paths between systems (from original spec Section 7)
- Migration completes without user-facing downtime (from original spec Section 7)
- Shadow mode shows decision parity for 2 weeks
- All SDKs updated with backward-compatible wrappers

## Planning Gate

> **Release 2 roadmap and tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.**
>
> **Validation criteria**: All 5 Release 1 real-world validation requirements must pass:
> 1. Identity merge validation — zero data loss, correct merging
> 2. Permission mapping validation — no escalation, no loss, Feb 28 incident resolved
> 3. Token lifecycle validation — revocation within 1 second, Mar 1 incident resolved
> 4. Schema correctness validation — production-scale performance, constraint integrity
> 5. Canonical UUID correlation — Mar 10 incident resolved
>
> **Review process**: Engineering lead and security lead review validation results. Both must approve before Release 2 planning proceeds.
>
> **If validation fails**:
> - Minor issues: Remediate within Release 1 scope, re-validate, then proceed
> - Schema design issues: Revise schema, re-run all validations, potentially adjust Release 2 scope
> - Fundamental model issues: Merge Release 1 and Release 2 back into a single release with revised approach

## Traceability

| Release 2 Item | Original Spec Source |
|----------------|---------------------|
| Auth Middleware Consolidation | Section 3, R4 (full) |
| Migration Framework | Section 3, R5 (full) |
| Admin Dashboard | Section 3, R6 (full) |
| Developer SDK Updates | Section 3, R7 (full) |
| Integration tests (middleware) | Section 5, line 2 |
| Migration tests | Section 5, line 3 |
| Security audit / pen testing | Section 5, line 4 |
| Shadow mode validation | Section 5, line 5 |
| Rollout plan (steps 1-6) | Section 6 (full) |
| R3 integration validation | Deferred from R1 — R3 + R4 integration semantics |
