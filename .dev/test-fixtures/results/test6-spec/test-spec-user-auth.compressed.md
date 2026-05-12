---
title: "User Authentication Service"
version: "1.0.0"
status: draft
feature_id: AUTH-001
parent_feature: null
spec_type: new_feature
complexity_score: 0.6
complexity_class: MEDIUM
target_release: "v1.0"
authors: [test-engineer, claude]
created: "2026-03-26"
quality_scores:
  clarity: 8.0
  completeness: 7.5
  testability: 8.5
  consistency: 8.0
  overall: 8.0
---

# User Authentication Service

## 1. Problem Statement

The application currently lacks a centralized, secure authentication mechanism. Users cannot create accounts, log in, or manage sessions in a consistent way. Without a dedicated authentication service, each component implements its own credential handling, leading to security vulnerabilities, inconsistent user experiences, and duplicated logic across the codebase.

A purpose-built authentication service is needed to provide secure, scalable identity management with JWT-based session handling, proper password hashing, and token refresh capabilities.

### 1.1 Evidence

|Evidence|Source|Impact|
|----------|--------|--------|
|Password stored in plaintext in 2 modules|Security audit Q1 2026|Critical vulnerability; potential data breach|
|Session management duplicated across 4 services|Codebase analysis|Inconsistent timeout behavior; maintenance burden|
|No token refresh mechanism|User reports (JIRA-2847)|Users forced to re-login every 15 minutes|
|Failed login attempts not rate-limited|Penetration test report|Brute-force attack vector remains open|

### 1.2 Scope Boundary

**In scope**: User registration, login/logout, JWT token issuance and refresh, password hashing, authenticated profile retrieval, password reset flow.

**Out of scope**: OAuth2/OIDC federation, multi-factor authentication, role-based access control (RBAC), social login providers. These are planned for v2.0.

## 2. Solution Overview

Build a standalone `AuthService` module that centralizes all authentication concerns behind a clean API. The service uses JWT tokens for stateless session management, bcrypt for password hashing, and a refresh token rotation strategy to balance security with user convenience.

The architecture follows a layered approach: `AuthService` orchestrates authentication flows, `TokenManager` handles JWT lifecycle, `JwtService` provides low-level token signing and verification, and `PasswordHasher` encapsulates bcrypt operations. All components are injectable and independently testable.

### 2.1 Key Design Decisions

|Decision|Choice|Alternatives Considered|Rationale|
|----------|--------|------------------------|-----------|
|Token format|JWT with RS256 signing|Opaque tokens, PASETO|Industry standard; broad library support; stateless verification|
|Password hashing|bcrypt with cost factor 12|Argon2id, scrypt|Mature, well-audited; cost factor 12 balances security and latency|
|Token storage|Access token in memory, refresh token in httpOnly cookie|localStorage, sessionStorage|Prevents XSS access to tokens; refresh rotation mitigates CSRF|
|Session strategy|Stateless JWT with refresh rotation|Server-side sessions, sliding window|Horizontal scalability; no shared session store required|

### 2.2 Workflow / Data Flow

```
Client                    AuthService              TokenManager           Database
  |                           |                         |                     |
  |-- POST /auth/login ------>|                         |                     |
  |                           |-- validate credentials --------------------------->|
  |                           |<----- user record ---------------------------------|
  |                           |-- hash compare -------->|                     |
  |                           |-- issue tokens -------->|                     |
  |                           |                         |-- sign JWT -------->|
  |                           |                         |<--- access_token ---|
  |                           |                         |-- sign refresh ---->|
  |                           |                         |<--- refresh_token --|
  |<-- { access, refresh } ---|                         |                     |
  |                           |                         |                     |
  |-- GET /auth/me ---------->|                         |                     |
  |   (Bearer access_token)   |-- verify token -------->|                     |
  |                           |<--- decoded claims -----|                     |
  |                           |-- fetch profile ------------------------------>|
  |<-- { user profile } ------|                         |                     |
```

## 3. Functional Requirements

### FR-AUTH.1: User Login

**Description**: The system shall authenticate users via email and password, returning a valid JWT access token and a refresh token upon successful credential verification.

**Acceptance Criteria**:
- [ ] Given valid email and password, the system shall return a 200 response with access_token (15min TTL) and refresh_token (7d TTL)
- [ ] Given invalid credentials, the system shall return a 401 response with error message and not reveal whether email or password was incorrect
- [ ] Given a locked account, the system shall return a 403 response indicating account suspension
- [ ] The system shall rate-limit login attempts to 5 per minute per IP address

**Dependencies**: PasswordHasher, TokenManager, User database table

### FR-AUTH.2: User Registration

**Description**: The system shall register new users with input validation, creating a user record with a securely hashed password and returning confirmation of successful registration.

**Acceptance Criteria**:
- [ ] Given valid registration data (email, password, display name), the system shall create a user record and return 201 with user profile
- [ ] Given an already-registered email, the system shall return a 409 conflict response
- [ ] The system shall enforce password policy: minimum 8 characters, at least one uppercase, one lowercase, one digit
- [ ] The system shall validate email format before attempting registration

**Dependencies**: PasswordHasher, User database table

### FR-AUTH.3: Token Refresh

**Description**: The system shall issue and refresh JWT tokens, allowing clients to obtain a new access token using a valid refresh token without re-entering credentials.

**Acceptance Criteria**:
- [ ] Given a valid refresh token, the system shall return a new access_token and rotate the refresh_token
- [ ] Given an expired refresh token, the system shall return 401 and require re-authentication
- [ ] Given a previously-rotated (revoked) refresh token, the system shall invalidate all tokens for that user (replay detection)
- [ ] The system shall store refresh token hashes in the database for revocation support

**Dependencies**: TokenManager, JwtService, RefreshToken database table

### FR-AUTH.4: Profile Retrieval

**Description**: The system shall provide authenticated user profile retrieval, returning the current user's profile data when presented with a valid access token.

**Acceptance Criteria**:
- [ ] Given a valid Bearer access_token, the system shall return the user profile (id, email, display_name, created_at)
- [ ] Given an expired or invalid token, the system shall return 401
- [ ] The system shall not return sensitive fields (password_hash, refresh_token_hash) in the profile response

**Dependencies**: TokenManager, User database table

### FR-AUTH.5: Password Reset

**Description**: The system shall support a secure password reset flow, allowing users to request a reset link and set a new password using a time-limited token.

**Acceptance Criteria**:
- [ ] Given a registered email, the system shall generate a password reset token (1-hour TTL) and dispatch a reset email
- [ ] Given a valid reset token, the system shall allow setting a new password and invalidate the reset token
- [ ] Given an expired or invalid reset token, the system shall return 400 with an appropriate error message
- [ ] The system shall invalidate all existing sessions (refresh tokens) upon successful password reset

**Dependencies**: TokenManager, PasswordHasher, Email service (external)

## 4. Architecture

### 4.1 New Files

|File|Purpose|Dependencies|
|------|---------|-------------|
|`src/auth/auth-service.ts`|Core authentication orchestrator; coordinates login, register, refresh, and reset flows|`TokenManager`, `PasswordHasher`, User repository|
|`src/auth/token-manager.ts`|JWT lifecycle management; issues, refreshes, and revokes token pairs|`JwtService`, RefreshToken repository|
|`src/auth/jwt-service.ts`|Low-level JWT signing and verification using RS256|`jsonwebtoken` library, RSA key pair|
|`src/auth/password-hasher.ts`|bcrypt password hashing and comparison with configurable cost factor|`bcrypt` library|

### 4.2 Modified Files

|File|Change|Rationale|
|------|--------|-----------|
|`src/middleware/auth-middleware.ts`|Add Bearer token extraction and verification|Integrate token validation into request pipeline|
|`src/routes/index.ts`|Register `/auth/*` route group|Expose authentication endpoints|
|`src/database/migrations/003-auth-tables.ts`|Add users and refresh_tokens tables|Persistent storage for auth data|

### 4.4 Module Dependency Graph

```
auth-middleware.ts
       |
       v
  auth-service.ts
    /         \
   v           v
token-manager.ts   password-hasher.ts
       |
       v
  jwt-service.ts
```

### 4.5 Data Models

```typescript
interface UserRecord {
  id: string;               // UUID v4
  email: string;            // Unique, indexed
  display_name: string;
  password_hash: string;    // bcrypt hash
  is_locked: boolean;       // Account suspension flag
  created_at: Date;
  updated_at: Date;
}

interface RefreshTokenRecord {
  id: string;               // UUID v4
  user_id: string;          // FK to UserRecord.id
  token_hash: string;       // SHA-256 hash of refresh token
  expires_at: Date;
  revoked: boolean;
  created_at: Date;
}

interface AuthTokenPair {
  access_token: string;     // JWT, 15-minute TTL
  refresh_token: string;    // Opaque token, 7-day TTL
}
```

### 4.6 Implementation Order

```
1. password-hasher.ts      -- No dependencies; pure utility
2. jwt-service.ts          -- No dependencies; pure crypto
   token-manager.ts        -- [parallel with jwt-service once interface defined]
3. auth-service.ts         -- depends on 1, 2
4. auth-middleware.ts      -- depends on token-manager
5. routes + migrations     -- depends on 3, 4
```

## 5. Interface Contracts

### 5.1 CLI Surface

The authentication service does not expose a CLI interface. All interactions occur through the REST API endpoints defined in the functional requirements. Administrative operations (account locking, token revocation) are handled through the existing admin dashboard.

## 6. Non-Functional Requirements

|ID|Requirement|Target|Measurement|
|----|-------------|--------|-------------|
|NFR-AUTH.1|Authentication endpoint response time|< 200ms p95 under normal load|Load testing with k6; monitor p95 latency in production APM|
|NFR-AUTH.2|Service availability|99.9% uptime (< 8.76 hours downtime/year)|Uptime monitoring via health check endpoint; PagerDuty alerting|
|NFR-AUTH.3|Password hashing security|bcrypt cost factor 12 (approx. 250ms per hash)|Unit test verifying cost factor; benchmark test for hash timing|

## 7. Risk Assessment

|Risk|Probability|Impact|Mitigation|
|------|-------------|--------|------------|
|JWT secret key compromise allows forged tokens|Low|High|Use RS256 asymmetric keys; store private key in secrets manager; implement key rotation every 90 days|
|Refresh token replay attack after token theft|Medium|High|Implement refresh token rotation with replay detection; revoke all user tokens on suspicious reuse|
|bcrypt cost factor too low for future hardware|Low|Medium|Make cost factor configurable; review annually against OWASP recommendations; migration path to Argon2id if needed|

## 8. Test Plan

### 8.1 Unit Tests

|Test|File|Validates|
|------|------|-----------|
|`PasswordHasher` hashes and verifies passwords correctly|`tests/auth/password-hasher.test.ts`|FR-AUTH.1, FR-AUTH.2: bcrypt hash generation and comparison|
|`JwtService` signs and verifies JWT tokens with RS256|`tests/auth/jwt-service.test.ts`|FR-AUTH.3: Token signing produces valid JWT; expired tokens rejected|
|`TokenManager` issues token pairs and rotates refresh tokens|`tests/auth/token-manager.test.ts`|FR-AUTH.3: Access/refresh pair generation; rotation invalidates old refresh token|
|`AuthService.login` returns tokens for valid credentials|`tests/auth/auth-service.test.ts`|FR-AUTH.1: Successful login flow; invalid credentials rejected|
|`AuthService.register` creates user with hashed password|`tests/auth/auth-service.test.ts`|FR-AUTH.2: Registration stores bcrypt hash; duplicate email rejected|

### 8.2 Integration Tests

|Test|Validates|
|------|-----------|
|Full login flow through HTTP endpoint returns valid JWT|FR-AUTH.1: End-to-end credential validation, token issuance, and response format|
|Token refresh endpoint issues new pair and revokes old refresh token|FR-AUTH.3: Refresh rotation works through the HTTP layer; replay detection triggers revocation|
|Registration followed by login succeeds with same credentials|FR-AUTH.1, FR-AUTH.2: Data persistence between registration and authentication|

### 8.3 E2E Scenario

|Scenario|Steps|Expected Outcome|
|----------|-------|-----------------|
|Complete user lifecycle|1. Register new user 2. Login with credentials 3. Access profile with token 4. Refresh token 5. Reset password 6. Login with new password|Each step returns expected status codes; tokens are valid; old credentials rejected after reset|

## 9. Migration & Rollout

- **Breaking changes**: No. The authentication service is additive; existing unauthenticated endpoints remain functional during the rollout period.
- **Backwards compatibility**: Existing API consumers are unaffected. Authentication will be opt-in during phase 1, required for protected endpoints in phase 2.
- **Rollback plan**: Feature flag `AUTH_SERVICE_ENABLED` controls routing. Disable flag to revert to pre-auth behavior. Database migrations include down-migration scripts for users and refresh_tokens tables.

## 10. Downstream Inputs

### For sc:roadmap
The authentication service introduces a single theme ("Secure User Authentication") spanning two milestones: (1) Core Auth Infrastructure (password hashing, JWT signing, token management) and (2) Auth API Endpoints (login, register, refresh, profile, reset). Each milestone maps directly to the implementation order in Section 4.6.

### For sc:tasklist
Tasks should be generated per functional requirement (FR-AUTH.1 through FR-AUTH.5), with sub-tasks for unit tests, integration tests, and documentation. The `PasswordHasher` and `JwtService` tasks have no dependencies and can be parallelized. `AuthService` tasks depend on both utility modules completing first.

## 11. Open Items

|Item|Question|Impact|Resolution Target|
|------|----------|--------|-------------------|
|OI-1|Should password reset emails be sent synchronously or via a message queue?|Affects latency of reset endpoint and system resilience|Sprint planning for v1.0|
|OI-2|What is the maximum number of active refresh tokens per user?|Affects storage requirements and multi-device support|Architecture review meeting|

## 12. Brainstorm Gap Analysis

|Gap ID|Description|Severity|Affected Section|Persona|
|--------|-------------|----------|-----------------|---------|
|GAP-1|No account lockout policy defined after N failed attempts|Medium|Section 3 (FR-AUTH.1)|security|
|GAP-2|Audit logging for authentication events not specified|Low|Section 6 (NFR)|backend|
|GAP-3|Token revocation on user deletion not addressed|Medium|Section 3 (FR-AUTH.3)|architect|

The gap analysis identifies three areas for future iteration. GAP-1 (account lockout) is partially addressed by the rate-limiting criterion in FR-AUTH.1 but should be expanded to include progressive lockout. GAP-2 and GAP-3 are deferred to v1.1 as they do not affect core authentication functionality.


## Appendix A: Glossary

|Term|Definition|
|------|-----------|
|JWT|JSON Web Token; a compact, URL-safe token format for representing claims between two parties|
|bcrypt|A password hashing function based on the Blowfish cipher, designed to be computationally expensive|
|Refresh token rotation|Security pattern where each use of a refresh token invalidates it and issues a new one|
|RS256|RSA Signature with SHA-256; an asymmetric signing algorithm for JWT tokens|
|Bearer token|An HTTP authentication scheme where the client sends a token in the Authorization header|

## Appendix B: Reference Documents

|Document|Relevance|
|----------|-----------|
|OWASP Authentication Cheatsheet|Industry best practices for authentication implementation|
|RFC 7519 (JWT)|JWT token format specification|
|RFC 6749 (OAuth 2.0)|Reference for refresh token rotation pattern|