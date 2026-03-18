---
release: 1
parent-spec: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/evals/files/spec-splittable-auth-system.md
split-proposal: split-proposal-final.md
scope: "Identity & Permission Foundation — unified data model, permission engine, token service, and database schema"
status: draft
validation-gate: null
---

# Release 1 — Identity & Permission Foundation

## Objective

Deliver the foundational unified identity model, centralized permission store, unified token service, and supporting database schema. This release establishes the data model and core engines that all subsequent integration, migration, and consumer components will build on. Its primary purpose is to validate that the unified auth model is structurally correct before dependent systems are built on top.

## Scope

### Included

1. **R1: Unified Identity Model (P0)** — From: original spec Section 3, R1
   - Single `Identity` model representing users across all auth mechanisms
   - Support for multiple credential types per identity (password, API key, OAuth token)
   - Canonical UUID replacing system-specific IDs
   - Credential rotation without identity change
   - Migration path definition from existing `WebUser`, `CLIIdentity`, `OAuthClient` (schema and mapping logic only; execution is Release 2)

2. **R2: Centralized Permission Store (P0)** — From: original spec Section 3, R2
   - Role hierarchy: `viewer < editor < admin < super_admin`
   - Permission scopes: `read`, `write`, `execute`, `admin`
   - Resource-level permissions (not just global roles)
   - Permission inheritance through role hierarchy

3. **R3: Unified Token Service (P0)** — From: original spec Section 3, R3
   - JWT-based tokens with configurable expiry
   - Token refresh mechanism
   - Immediate revocation via token blocklist
   - Token introspection endpoint for services

4. **Database Schema** — From: original spec Section 4.2
   - `identities` table: UUID pk, display_name, email, created_at, status
   - `credentials` table: identity_id FK, type (password|api_key|oauth), credential_data, expires_at
   - `roles` table: role_name, parent_role, description
   - `identity_roles` table: identity_id FK, role_name FK, resource_scope
   - `permissions` table: role_name FK, action, resource_type
   - `tokens` table: jti, identity_id FK, issued_at, expires_at, revoked
   - `audit_log` table: identity_id FK, action, resource, timestamp, source_system

5. **Unit Tests** — From: original spec Section 5, partial
   - Unit tests for identity model
   - Unit tests for permission engine
   - Unit tests for token service

### Excluded (assigned to Release 2)

1. **R4: Auth Middleware Consolidation (P1)** — Deferred to: Release 2, requires R1+R2+R3 as stable foundation
2. **R5: Migration Framework (P1)** — Deferred to: Release 2, requires finalized schema and identity model
3. **R6: Admin Dashboard (P2)** — Deferred to: Release 2, requires R1+R2+R4
4. **R7: Developer SDK Updates (P2)** — Deferred to: Release 2, requires R3+R4 stable
5. **Integration tests for auth middleware** — Deferred to: Release 2 (middleware is R4)
6. **Migration tests with production-like data** — Deferred to: Release 2 (migration is R5)
7. **Security audit / penetration testing** — Deferred to: Release 2 (requires integrated system)
8. **Shadow mode validation** — Deferred to: Release 2 (requires middleware + migration)
9. **Rollout plan steps 1-6** — Deferred to: Release 2 (requires full integration)

## Dependencies

### Prerequisites

None — Release 1 is the foundation release.

### External Dependencies

- Database system supporting the 7-table schema (PostgreSQL assumed from schema design)
- JWT library for token service implementation
- Access to production user data from all three existing systems (WebUser, CLIIdentity, OAuthClient) for validation

## Real-World Validation Requirements

All validation must use actual functionality in production-like conditions. No mocks, no simulated tests.

1. **Identity Merge Validation**: Take a representative sample of production user data from all three existing systems. Run the identity merge mapping logic. Verify:
   - Every existing user across all three systems receives a canonical UUID
   - Users with accounts in multiple systems are correctly identified and merged
   - No identities are lost or incorrectly merged
   - Credential types are correctly mapped

2. **Permission Mapping Validation**: Map existing permissions from all three stores (`web/permissions.py`, `cli/api_keys.py`, `plugins/oauth_store.py`) into the RBAC model. Verify:
   - No permission escalation occurs (specifically: reproduce the Feb 28 incident scenario and confirm it cannot occur under the new model)
   - No permission loss occurs (users retain all access they currently have)
   - Role hierarchy inheritance works correctly with resource-level scoping

3. **Token Lifecycle Validation**: Issue tokens via the new token service, exercise the full lifecycle. Verify:
   - Token issuance, refresh, and introspection work correctly
   - Token revocation propagates and is enforced within 1 second (per success criteria)
   - Revoked tokens cannot be used (specifically: reproduce the Mar 1 incident scenario and confirm revoked keys are immediately invalid)

4. **Schema Correctness Validation**: Load production-scale data into the new schema. Verify:
   - All foreign key constraints hold
   - Query patterns for common operations perform within acceptable bounds
   - The audit_log table supports cross-system correlation via canonical UUID (specifically: reproduce the Mar 10 incident scenario and confirm audit entries are correlatable)

5. **Canonical UUID Correlation**: Verify that audit log entries generated against the new identity model can be correlated across what were previously three separate systems, using the canonical UUID as the join key.

## Success Criteria

- Unified Identity model correctly represents users from all three existing auth mechanisms
- Canonical UUID enables cross-system audit correlation
- Permission engine enforces RBAC hierarchy with resource-level scoping and no escalation paths
- Token revocation propagates within 1 second
- Database schema supports production-scale data with acceptable query performance
- All three cited incidents (Feb 28 permission bypass, Mar 1 revocation delay, Mar 10 audit correlation) are demonstrably resolved at the model/engine level

## Traceability

| Release 1 Item | Original Spec Source |
|----------------|---------------------|
| Unified Identity Model | Section 3, R1 (full) |
| Centralized Permission Store | Section 3, R2 (full) |
| Unified Token Service | Section 3, R3 (full) |
| Database Schema (7 tables) | Section 4.2 (full) |
| Unit tests for model/engine/token | Section 5, line 1 (partial — unit tests only) |
| Identity merge mapping logic | Section 3, R1 bullet 4 (mapping definition, not execution) |
