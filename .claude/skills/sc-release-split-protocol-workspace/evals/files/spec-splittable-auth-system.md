---
title: "v3.2 — Unified Authentication & Authorization System"
version: "3.2.0"
status: draft
date: 2026-03-15
complexity_class: HIGH
domain_distribution:
  backend: 60
  security: 25
  frontend: 15
estimated_scope: 2000-2500 lines production code
---

# v3.2 Release Spec: Unified Authentication & Authorization System

## 1. Executive Summary

The current authentication system uses three separate mechanisms: session-based auth for the web UI, API key auth for CLI integrations, and OAuth2 for third-party plugins. Each has its own user model, permission store, and validation logic. This creates duplication, inconsistent permission enforcement, and makes auditing impossible.

This release unifies all three into a single identity and permission system with a shared user model, centralized permission store, and consistent enforcement layer.

## 2. Problem Statement

### Evidence

| System | Auth Mechanism | Permission Store | User Model |
|--------|---------------|-----------------|------------|
| Web UI | Session cookies + CSRF | `web/permissions.py` | `WebUser` |
| CLI | API keys + HMAC | `cli/api_keys.py` | `CLIIdentity` |
| Plugins | OAuth2 bearer tokens | `plugins/oauth_store.py` | `OAuthClient` |

**Incidents**:
- 2026-02-28: Plugin OAuth token granted `admin` scope but `web/permissions.py` didn't recognize it — plugin could bypass web permission checks entirely
- 2026-03-01: CLI API key revocation didn't propagate to active sessions — revoked keys remained valid for up to 24h
- 2026-03-10: Audit log showed 3 different user ID formats, making cross-system correlation impossible

### Root Cause

No shared identity layer. Each system evolved independently with its own user model and permission semantics.

## 3. Requirements

### R1: Unified Identity Model (P0)
Create a single `Identity` model that represents users across all auth mechanisms.
- Must support multiple credential types per identity (password, API key, OAuth token)
- Must include a canonical UUID that replaces system-specific IDs
- Must support credential rotation without identity change
- Migration path from existing `WebUser`, `CLIIdentity`, `OAuthClient`

### R2: Centralized Permission Store (P0)
Replace three separate permission stores with a single RBAC permission system.
- Role hierarchy: `viewer < editor < admin < super_admin`
- Permission scopes: `read`, `write`, `execute`, `admin`
- Resource-level permissions (not just global roles)
- Permission inheritance through role hierarchy

### R3: Unified Token Service (P0)
Single token issuance and validation service for all auth flows.
- JWT-based tokens with configurable expiry
- Token refresh mechanism
- Immediate revocation via token blocklist
- Token introspection endpoint for services

### R4: Auth Middleware Consolidation (P1)
Replace three auth middleware stacks with a single enforcement layer.
- Request authentication (identity extraction from any credential type)
- Permission checking against centralized store
- Rate limiting per identity (not per credential)
- Audit logging with canonical identity

### R5: Migration Framework (P1)
Tooling to migrate existing users and permissions to the unified system.
- Automated identity merging for users with accounts in multiple systems
- Conflict resolution for incompatible permissions
- Rollback capability during migration window
- Shadow mode: run unified system in parallel, compare results, don't enforce

### R6: Admin Dashboard (P2)
Web interface for managing identities, roles, and permissions.
- User search and identity management
- Role assignment and permission grants
- Audit log viewer with cross-system correlation
- Active session management and forced logout

### R7: Developer SDK Updates (P2)
Update client SDKs to use the new auth endpoints.
- Python SDK: new `authenticate()` and `check_permission()` methods
- JavaScript SDK: updated OAuth flow
- CLI tool: new `auth login` and `auth token` commands
- Backward-compatible wrappers for old auth methods (deprecated, removed in v4.0)

## 4. Architecture

### 4.1 System Context

```
┌──────────────────────────────────────────────────────────────┐
│                     Unified Auth Service                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │  Identity    │  │  Permission  │  │  Token Service      │ │
│  │  Store       │  │  Engine      │  │  (Issue/Validate)   │ │
│  └─────────────┘  └──────────────┘  └─────────────────────┘ │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Auth Middleware (unified)                    │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
          ▲                ▲                 ▲
          │                │                 │
     Web UI           CLI Tool          Plugin System
```

### 4.2 Database Schema

- `identities` table: UUID pk, display_name, email, created_at, status
- `credentials` table: identity_id FK, type (password|api_key|oauth), credential_data, expires_at
- `roles` table: role_name, parent_role, description
- `identity_roles` table: identity_id FK, role_name FK, resource_scope
- `permissions` table: role_name FK, action, resource_type
- `tokens` table: jti, identity_id FK, issued_at, expires_at, revoked
- `audit_log` table: identity_id FK, action, resource, timestamp, source_system

## 5. Testing Strategy

- Unit tests for identity model, permission engine, token service
- Integration tests for auth middleware with each credential type
- Migration tests with production-like data sets
- Security audit: penetration testing of new auth endpoints
- Shadow mode validation: compare old and new system decisions for 2 weeks

## 6. Rollout Plan

1. Deploy unified service in shadow mode (2 weeks)
2. Migrate identity data with rollback capability
3. Switch Web UI to unified auth (with kill switch)
4. Switch CLI to unified auth
5. Switch plugins to unified auth
6. Remove legacy auth systems (v4.0)

## 7. Success Criteria

- All three auth mechanisms use the same identity model
- Cross-system audit correlation achievable via canonical UUID
- Token revocation propagates within 1 second
- Zero permission escalation paths between systems
- Migration completes without user-facing downtime
