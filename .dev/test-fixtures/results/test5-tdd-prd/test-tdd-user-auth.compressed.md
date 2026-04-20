---
id: "AUTH-001-TDD"
title: "User Authentication Service - Technical Design Document"
description: "Technical architecture, data models, API specifications, and implementation details for the User Authentication Service"
version: "1.2"
status: "🟡 Draft"
type: "📐 Technical Design Document"
priority: "🔥 Highest"
created_date: "2026-03-26"
updated_date: "2026-03-26"
assigned_to: "auth-team"
autogen: false
coordinator: "test-lead"
parent_doc: "AUTH-PRD-001"
feature_id: "AUTH-001"
spec_type: "new_feature"
complexity_score: ""
complexity_class: ""
target_release: "v1.0"
authors: ["test-engineer"]
quality_scores:
  clarity: ""
  completeness: ""
  testability: ""
  consistency: ""
  overall: ""
depends_on:
- "AUTH-PRD-001"
- "INFRA-DB-001"
related_docs:
- "AUTH-PRD-001"
- "SEC-POLICY-001"
tags:
- technical-design-document
- authentication
- architecture
- specifications
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
approvers:
  tech_lead: ""
  engineering_manager: ""
  architect: ""
  security: ""
---

# User Authentication Service - Technical Design Document (TDD)

> **WHAT:** Technical Design Document specifying the architecture, data models, API specifications, and implementation details for the User Authentication Service.
> **WHY:** Translates product requirements (from AUTH-PRD-001) into an engineering specification that the auth-team builds against. Where the PRD defines *what* to build, this TDD defines *how* to build it.
> **HOW TO USE:** Engineers, architects, and technical stakeholders use this document to align on the technical approach before implementation begins.

Sentinel self-check (run before submitting TDD for pipeline consumption):
- feature_id must not be a placeholder -- value is "AUTH-001" (PASS)
- spec_type must be one of the valid enum values -- value is "new_feature" (PASS)
- target_release must not be a placeholder -- value is "v1.0" (PASS)
- complexity_score and complexity_class may remain empty (computed by sc:roadmap)

Pipeline field consumption:
- `complexity_score`, `complexity_class`: Computed by sc:roadmap during extraction (not read from frontmatter). Pre-populated values are advisory only.
- `feature_id`, `spec_type`, `target_release`: Consumed by sc:spec-panel `--downstream roadmap` (Step 6b) when generating scoped release specs.
- `quality_scores`: Populated by sc:spec-panel review output. Not consumed by sc:roadmap.

Quality gate: /sc:spec-panel @test-tdd-user-auth.md --focus correctness,architecture --mode critique

### Document Lifecycle Position

|Phase|Document|Ownership|Status|
|-------|----------|-----------|--------|
|Requirements|AUTH-PRD-001|Product|Approved|
|**Design**|**This TDD**|**Engineering**|**Draft**|
|Implementation|Technical Reference|Engineering|Not Started|

This TDD implements requirements from AUTH-PRD-001 Epics AUTH-E1 (Login/Registration), AUTH-E2 (Token Management), AUTH-E3 (Profile Management).

### Tiered Usage

|Tier|When to Use|Sections Required|
|------|-------------|-------------------|
|**Lightweight**|Bug fixes, config changes, small features (<1 sprint)|1, 2, 3, 6.4, 21, 22|
|**Standard**|Most features and services (1-3 sprints)|All numbered sections; skip conditional sections marked *(if applicable)*|
|**Heavyweight**|New systems, platform changes, cross-team projects|All sections fully completed, including all conditional sections|


## Document Information

|Field|Value|
|-------|-------|
|**Component Name**|User Authentication Service|
|**Component Type**|Backend Service|
|**Tech Lead**|test-lead|
|**Engineering Team**|auth-team|
|**Maintained By**|auth-team|
|**Target Release**|v1.0|
|**Last Verified**|2026-03-26 against initial design state|
|**Status**|Draft|

### Approvers

|Role|Name|Status|Date|
|------|------|--------|------|
|Tech Lead|test-lead|⬜ Pending||
|Engineering Manager|eng-manager|⬜ Pending||
|Architect|sys-architect|⬜ Pending||
|Security|sec-reviewer|⬜ Pending||


## Completeness Status

**Completeness Checklist:**
- [x] Section 1: Executive Summary — Complete
- [x] Section 2: Problem Statement & Context — Complete
- [x] Section 3: Goals & Non-Goals — Complete
- [x] Section 4: Success Metrics — Complete
- [x] Section 5: Technical Requirements — Complete
- [x] Section 6: Architecture — Complete
- [x] Section 7: Data Models — Complete
- [x] Section 8: API Specifications — Complete
- [ ] Section 9: State Management — Not applicable
- [x] Section 10: Component Inventory — Complete
- [x] Section 11: User Flows & Interactions — Complete
- [x] Section 12: Error Handling & Edge Cases — Complete
- [x] Section 13: Security Considerations — Complete
- [x] Section 14: Observability & Monitoring — Complete
- [x] Section 15: Testing Strategy — Complete
- [ ] Section 16: Accessibility Requirements — Not applicable
- [x] Section 17: Performance Budgets — Complete
- [x] Section 18: Dependencies — Complete
- [x] Section 19: Migration & Rollout Plan — Complete
- [x] Section 20: Risks & Mitigations — Complete
- [x] Section 21: Alternatives Considered — Complete
- [x] Section 22: Open Questions — Complete
- [x] Section 23: Timeline & Milestones — Complete
- [x] Section 24: Release Criteria — Complete
- [x] Section 25: Operational Readiness — Complete
- [x] Section 26: Cost & Resource Estimation — Complete
- [x] Section 27: References & Resources — Complete
- [x] Section 28: Glossary — Complete
- [ ] All links verified — Pending
- [ ] Reviewed by auth-team — Pending

**Contract Table:**

|Element|Details|
|---------|---------|
|**Dependencies**|PostgreSQL 15+, Redis 7+, Node.js 20 LTS|
|**Upstream**|Feeds from: AUTH-PRD-001 product requirements|
|**Downstream**|Feeds to: Technical Reference, implementation tasks, test plans|
|**Change Impact**|Notify: auth-team, platform-team, frontend-team|
|**Review Cadence**|As-needed during active development|


## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement & Context](#2-problem-statement--context)
3. [Goals & Non-Goals](#3-goals--non-goals)
4. [Success Metrics](#4-success-metrics)
5. [Technical Requirements](#5-technical-requirements)
6. [Architecture](#6-architecture)
7. [Data Models](#7-data-models)
8. [API Specifications](#8-api-specifications)
9. [State Management](#9-state-management)
10. [Component Inventory](#10-component-inventory)
11. [User Flows & Interactions](#11-user-flows--interactions)
12. [Error Handling & Edge Cases](#12-error-handling--edge-cases)
13. [Security Considerations](#13-security-considerations)
14. [Observability & Monitoring](#14-observability--monitoring)
15. [Testing Strategy](#15-testing-strategy)
16. [Accessibility Requirements](#16-accessibility-requirements)
17. [Performance Budgets](#17-performance-budgets)
18. [Dependencies](#18-dependencies)
19. [Migration & Rollout Plan](#19-migration--rollout-plan)
20. [Risks & Mitigations](#20-risks--mitigations)
21. [Alternatives Considered](#21-alternatives-considered)
22. [Open Questions](#22-open-questions)
23. [Timeline & Milestones](#23-timeline--milestones)
24. [Release Criteria](#24-release-criteria)
25. [Operational Readiness](#25-operational-readiness)
26. [Cost & Resource Estimation](#26-cost--resource-estimation)
27. [References & Resources](#27-references--resources)
28. [Glossary](#28-glossary)


## 1. Executive Summary

The User Authentication Service provides secure identity management for the platform, handling user registration, login, token issuance, and profile management. The service is built on `AuthService` as the primary orchestrator, delegating to `TokenManager`, `JwtService`, and `PasswordHasher` for specialized concerns. It exposes a RESTful API consumed by frontend clients including `LoginPage`, `RegisterPage`, and the `AuthProvider` context wrapper.

This TDD defines the technical approach for implementing the authentication system described in AUTH-PRD-001, targeting v1.0 release with JWT-based stateless authentication, bcrypt password hashing, and a phased rollout strategy.

**Key Deliverables:**
- `AuthService` core orchestration layer with login, registration, and profile flows
- `TokenManager` and `JwtService` for JWT access/refresh token lifecycle
- `PasswordHasher` abstraction over bcrypt with configurable cost factor
- RESTful API endpoints: `/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`
- `UserProfile` and `AuthToken` data models backed by PostgreSQL
- Frontend integration points: `LoginPage`, `RegisterPage`, `AuthProvider`


## 2. Problem Statement & Context

### 2.1 Background

The platform currently lacks a centralized authentication system. Users cannot create accounts, log in, or maintain authenticated sessions. All API endpoints are either publicly accessible or protected by ad-hoc API keys, creating security vulnerabilities and preventing personalized experiences.

### 2.2 Problem Statement

Without a robust authentication service, the platform cannot support user-specific features, enforce access control, or comply with security audit requirements. The `AuthService` must provide a standards-compliant identity layer that other services can rely on for verifying user identity.

### 2.3 Business Context

User authentication is a prerequisite for all personalization features planned in Q2 2026. The marketing team projects a 40% increase in engagement once user accounts are available. Compliance requires authentication audit trails before the Q3 regulatory review.


## 3. Goals & Non-Goals

### 3.1 Goals

|ID|Goal|Success Criteria|
|----|------|-----------------|
|G-001|Secure user registration and login|`AuthService` handles email/password flows with bcrypt hashing|
|G-002|Stateless token-based sessions|`JwtService` issues and validates JWT access and refresh tokens|
|G-003|Self-service password reset|Users can reset passwords via email verification flow|
|G-004|Profile management|`UserProfile` CRUD operations available via `/auth/me`|
|G-005|Frontend integration|`LoginPage`, `RegisterPage`, and `AuthProvider` consume the API|

### 3.2 Non-Goals

|ID|Non-Goal|Rationale|
|----|----------|-----------|
|NG-001|Social/OAuth login|Deferred to v1.1; requires third-party integrations|
|NG-002|Multi-factor authentication|Planned for v1.2 as a separate feature|
|NG-003|Role-based access control (RBAC)|`UserProfile` includes a roles field but enforcement is out of scope|

### 3.3 Future Considerations

OAuth2 provider integration and MFA are planned for subsequent releases and should be considered when designing the `AuthService` interface to avoid breaking changes.


## 4. Success Metrics

### 4.1 Technical Metrics

|Metric|Target|Measurement Method|
|--------|--------|--------------------|
|Login response time (p95)|< 200ms|APM instrumentation on `AuthService.login()`|
|Registration success rate|> 99%|Ratio of successful registrations to attempts|
|Token refresh latency (p95)|< 100ms|APM instrumentation on `TokenManager.refresh()`|
|Service availability|99.9% uptime|Health check monitoring over 30-day windows|
|Password hash time|< 500ms|Benchmark of `PasswordHasher.hash()` with bcrypt cost 12|

### 4.2 Business Metrics

|Metric|Target|Measurement Method|
|--------|--------|--------------------|
|User registration conversion|> 60%|Funnel analytics from `RegisterPage` to confirmed account|
|Daily active authenticated users|> 1000 within 30 days of GA|`AuthToken` issuance counts|


## 5. Technical Requirements

### 5.1 Functional Requirements

|ID|Requirement|Description|Acceptance Criteria|
|----|-------------|-------------|---------------------|
|FR-AUTH-001|Login with email and password|`AuthService` must authenticate users by validating email/password credentials against stored bcrypt hashes via `PasswordHasher`|1. Valid credentials return 200 with `AuthToken` containing accessToken and refreshToken. 2. Invalid credentials return 401 with error message. 3. Non-existent email returns 401 (no user enumeration). 4. Account locked after 5 failed attempts within 15 minutes.|
|FR-AUTH-002|User registration with validation|`AuthService` must create new user accounts with email uniqueness validation, password strength enforcement, and `UserProfile` creation|1. Valid registration returns 201 with `UserProfile` data. 2. Duplicate email returns 409 Conflict. 3. Weak passwords (< 8 chars, no uppercase, no number) return 400. 4. `PasswordHasher` stores bcrypt hash with cost factor 12.|
|FR-AUTH-003|JWT token issuance and refresh|`TokenManager` must issue JWT access tokens (15-minute expiry) and refresh tokens (7-day expiry) via `JwtService`, supporting silent refresh|1. Login returns both accessToken (15 min TTL) and refreshToken (7 day TTL). 2. POST `/auth/refresh` with valid refreshToken returns new `AuthToken` pair. 3. Expired refreshToken returns 401. 4. Revoked refreshToken returns 401.|
|FR-AUTH-004|User profile retrieval|`AuthService` must return the authenticated user's `UserProfile` including id, email, displayName, roles, and timestamps|1. GET `/auth/me` with valid accessToken returns `UserProfile`. 2. Expired or invalid token returns 401. 3. Response includes id, email, displayName, createdAt, updatedAt, lastLoginAt, roles.|
|FR-AUTH-005|Password reset flow|`AuthService` must support a two-step password reset: request (sends email with token) and confirmation (validates token, updates password via `PasswordHasher`)|1. POST `/auth/reset-request` with valid email sends reset token via email. 2. POST `/auth/reset-confirm` with valid token updates the password hash. 3. Reset tokens expire after 1 hour. 4. Used reset tokens cannot be reused.|

### 5.2 Non-Functional Requirements

**Performance:**

|ID|Requirement|Target|Measurement|
|----|-------------|--------|-------------|
|NFR-PERF-001|API response time|All auth endpoints must respond in < 200ms at p95|APM tracing on `AuthService` methods|
|NFR-PERF-002|Concurrent authentication|Support 500 concurrent login requests|Load testing with k6|

**Reliability:**

|ID|Requirement|Target|Measurement|
|----|-------------|--------|-------------|
|NFR-REL-001|Service availability|99.9% uptime measured over 30-day rolling windows|Uptime monitoring via health check endpoint|

**Security:**

|ID|Requirement|Target|Measurement|
|----|-------------|--------|-------------|
|NFR-SEC-001|Password hashing|`PasswordHasher` must use bcrypt with cost factor 12|Unit test asserting bcrypt cost parameter|
|NFR-SEC-002|Token signing|`JwtService` must sign tokens with RS256 using 2048-bit RSA keys|Configuration validation test|


## 6. Architecture

### 6.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                   API Gateway                        │
│              (rate limiting, CORS)                    │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                  AuthService                         │
│         (orchestrates all auth flows)                 │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ TokenManager  │  │PasswordHasher│  │  UserRepo  │ │
│  │              │  │              │  │            │ │
│  │ ┌──────────┐ │  │  bcrypt      │  │ PostgreSQL │ │
│  │ │JwtService│ │  │  cost: 12    │  │            │ │
│  │ └──────────┘ │  └──────────────┘  └────────────┘ │
│  └──────────────┘                                    │
└─────────────────────────────────────────────────────┘
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
         PostgreSQL   Redis   Email
         (users)    (tokens)  (reset)
```

### 6.2 Component Interactions

The `AuthService` acts as the facade, receiving requests from the API Gateway and delegating to specialized components. Login requests flow through `PasswordHasher` for credential validation, then to `TokenManager` which uses `JwtService` to sign JWT tokens. The `TokenManager` stores refresh tokens in Redis for revocation support. Registration requests validate input, call `PasswordHasher` to generate bcrypt hashes, and persist the `UserProfile` to PostgreSQL.

### 6.3 System Boundaries

|Boundary|Internal/External|Protocol|Notes|
|----------|-------------------|----------|-------|
|API Gateway to `AuthService`|Internal|HTTP/REST|JSON request/response|
|`AuthService` to PostgreSQL|Internal|TCP/SQL|Connection pooling via pg-pool|
|`TokenManager` to Redis|Internal|TCP/RESP|Used for refresh token storage and revocation|
|`AuthService` to Email Service|External|SMTP/API|Password reset emails via SendGrid|

### 6.4 Key Design Decisions

|Decision|Choice|Alternatives Considered|Rationale|
|----------|--------|------------------------|-----------|
|Session mechanism|JWT with refresh tokens|Server-side sessions with cookies|JWT enables stateless verification across services. Refresh tokens mitigate short access token lifetimes. `TokenManager` handles the dual-token lifecycle.|
|Password hashing|bcrypt via `PasswordHasher`|argon2id, scrypt|bcrypt is battle-tested with well-understood security properties. Cost factor 12 provides adequate resistance against brute force while keeping hash time under 500ms. `PasswordHasher` abstracts the algorithm for future migration.|


## 7. Data Models

### 7.1 Data Entities

**`UserProfile` Interface:**

```ts
interface UserProfile {
  id: string;            // UUID v4, primary key
  email: string;         // unique, indexed, lowercase normalized
  displayName: string;   // user-chosen display name, 2-100 chars
  createdAt: string;     // ISO 8601 timestamp
  updatedAt: string;     // ISO 8601 timestamp
  lastLoginAt: string;   // ISO 8601 timestamp, nullable
  roles: string[];       // e.g., ["user"], ["user", "admin"]
}
```

**`UserProfile` Field Table:**

|Field|Type|Constraints|Description|
|-------|------|-------------|-------------|
|id|string (UUID)|PRIMARY KEY, NOT NULL|Unique user identifier generated by `AuthService`|
|email|string|UNIQUE, NOT NULL, indexed|User email, normalized to lowercase by `AuthService`|
|displayName|string|NOT NULL, 2-100 chars|Display name shown in UI via `LoginPage` and `RegisterPage`|
|createdAt|string (ISO 8601)|NOT NULL, DEFAULT now()|Account creation timestamp|
|updatedAt|string (ISO 8601)|NOT NULL, auto-updated|Last profile modification timestamp|
|lastLoginAt|string (ISO 8601)|NULLABLE|Updated by `AuthService` on each successful login|
|roles|string[]|NOT NULL, DEFAULT ["user"]|Authorization roles; enforced downstream, not by `AuthService`|

**`AuthToken` Interface:**

```ts
interface AuthToken {
  accessToken: string;   // JWT signed by JwtService, 15-min expiry
  refreshToken: string;  // opaque token stored in Redis by TokenManager
  expiresIn: number;     // seconds until accessToken expires (900)
  tokenType: string;     // always "Bearer"
}
```

**`AuthToken` Field Table:**

|Field|Type|Constraints|Description|
|-------|------|-------------|-------------|
|accessToken|string (JWT)|NOT NULL|Signed by `JwtService` using RS256; contains user id and roles in payload|
|refreshToken|string|NOT NULL, unique|Opaque token managed by `TokenManager`; stored in Redis with 7-day TTL|
|expiresIn|number|NOT NULL|Seconds until accessToken expiration; always 900 (15 minutes)|
|tokenType|string|NOT NULL|Always "Bearer"; included for OAuth2 compatibility|

### 7.2 Data Storage

|Store|Technology|Purpose|Retention|
|-------|-----------|---------|-----------|
|User records|PostgreSQL 15|`UserProfile` persistence, password hashes|Indefinite|
|Refresh tokens|Redis 7|`TokenManager` token storage and revocation|7-day TTL|
|Audit log|PostgreSQL 15|Login attempts, password resets|90 days|


## 8. API Specifications

### 8.1 API Overview

|Method|Path|Auth Required|Rate Limit|Description|
|--------|------|---------------|------------|-------------|
|POST|`/auth/login`|No|10 req/min per IP|Authenticate user, return `AuthToken`|
|POST|`/auth/register`|No|5 req/min per IP|Create new `UserProfile`, return profile data|
|GET|`/auth/me`|Yes (Bearer)|60 req/min per user|Return authenticated user's `UserProfile`|
|POST|`/auth/refresh`|No (refresh token in body)|30 req/min per user|Exchange refresh token for new `AuthToken`|

### 8.2 Endpoint Details

#### POST `/auth/login`

Authenticates a user via `AuthService` by validating email/password credentials through `PasswordHasher` and issuing tokens via `TokenManager`.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**

```json
{
  "accessToken": "eyJhbGciOiJSUzI1NiIs...",
  "refreshToken": "dGhpcyBpcyBhIHJlZnJlc2g...",
  "expiresIn": 900,
  "tokenType": "Bearer"
}
```

**Error Responses:**
- 401 Unauthorized: Invalid email or password
- 429 Too Many Requests: Rate limit exceeded
- 423 Locked: Account locked after 5 failed attempts

#### POST `/auth/register`

Creates a new user account via `AuthService`. Validates email uniqueness, enforces password policy, hashes password with `PasswordHasher`, and persists the `UserProfile`.

**Request:**

```json
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "displayName": "New User"
}
```

**Response (201 Created):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "newuser@example.com",
  "displayName": "New User",
  "createdAt": "2026-03-26T10:00:00Z",
  "updatedAt": "2026-03-26T10:00:00Z",
  "lastLoginAt": null,
  "roles": ["user"]
}
```

**Error Responses:**
- 400 Bad Request: Validation errors (weak password, invalid email format)
- 409 Conflict: Email already registered

#### GET `/auth/me`

Returns the authenticated user's `UserProfile`. Requires a valid JWT accessToken issued by `JwtService` in the Authorization header.

**Request Headers:**

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "displayName": "Example User",
  "createdAt": "2026-03-20T08:00:00Z",
  "updatedAt": "2026-03-25T14:30:00Z",
  "lastLoginAt": "2026-03-26T09:00:00Z",
  "roles": ["user"]
}
```

**Error Responses:**
- 401 Unauthorized: Missing, expired, or invalid accessToken

#### POST `/auth/refresh`

Exchanges a valid refresh token for a new `AuthToken` pair via `TokenManager`. The old refresh token is revoked and a new one is issued.

**Request:**

```json
{
  "refreshToken": "dGhpcyBpcyBhIHJlZnJlc2g..."
}
```

**Response (200 OK):**

```json
{
  "accessToken": "eyJhbGciOiJSUzI1NiIs...",
  "refreshToken": "bmV3IHJlZnJlc2ggdG9rZW4...",
  "expiresIn": 900,
  "tokenType": "Bearer"
}
```

**Error Responses:**
- 401 Unauthorized: Expired or revoked refresh token

### 8.3 Error Response Format

All error responses from `AuthService` follow a consistent JSON structure:

```json
{
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "The provided email or password is incorrect.",
    "status": 401
  }
}
```

### 8.4 API Governance and Versioning

The authentication API is versioned via URL prefix (`/v1/auth/*` in production). Breaking changes require a new major version. Non-breaking additions (new optional fields) are permitted within the current version.


## 9. State Management

Not applicable — backend service. The User Authentication Service is a stateless REST API. Session state is managed entirely through JWT tokens issued by `JwtService` and validated on each request. No server-side session state is maintained beyond refresh token records in Redis managed by `TokenManager`.


## 10. Component Inventory

### 10.1 Page/Route Structure

|Route|Page Component|Auth Required|Description|
|-------|---------------|---------------|-------------|
|`/login`|`LoginPage`|No|Email/password login form; calls POST `/auth/login`|
|`/register`|`RegisterPage`|No|Registration form with validation; calls POST `/auth/register`|
|`/profile`|ProfilePage|Yes|Displays `UserProfile` data; calls GET `/auth/me`|

### 10.2 Shared Components

|Component|Props|Description|
|-----------|-------|-------------|
|`LoginPage`|onSuccess: () => void, redirectUrl?: string|Renders email and password fields, handles form submission to `AuthService` login endpoint, stores `AuthToken` via `AuthProvider`|
|`RegisterPage`|onSuccess: () => void, termsUrl: string|Renders registration form with email, password, displayName fields, validates password strength client-side before calling `AuthService`|
|`AuthProvider`|children: ReactNode|Context provider wrapping the application; manages `AuthToken` state, handles silent refresh via `TokenManager`, exposes `UserProfile` and auth methods to child components|

### 10.3 Component Hierarchy

```
App
├── AuthProvider
│   ├── PublicRoutes
│   │   ├── LoginPage
│   │   └── RegisterPage
│   └── ProtectedRoutes
│       └── ProfilePage
```

The `AuthProvider` component wraps all routes and manages the authentication state. It intercepts 401 responses, triggers token refresh through `TokenManager`, and redirects unauthenticated users from protected routes to `LoginPage`.


## 11. User Flows & Interactions

The primary user flow starts at `LoginPage`, where the user submits credentials. The `AuthService` validates them via `PasswordHasher`, and on success, `TokenManager` issues an `AuthToken` pair. The `AuthProvider` stores the tokens and redirects to the profile page. Token refresh happens transparently when the `AuthProvider` detects an expiring accessToken.

Registration follows a similar pattern: `RegisterPage` submits user data, `AuthService` validates and creates the `UserProfile`, and the user is redirected to `LoginPage` to complete their first login.


## 12. Error Handling & Edge Cases

Error handling in the `AuthService` follows a layered approach. Input validation errors (malformed email, weak password) return 400 with specific field-level error codes. Authentication failures (wrong password, unknown email) return a generic 401 to prevent user enumeration. Rate limiting at the API Gateway returns 429 before requests reach `AuthService`. The `TokenManager` handles token expiration gracefully by distinguishing between expired tokens (re-authenticate) and revoked tokens (security event).

Edge cases include concurrent registration with the same email (handled by database unique constraint), clock skew in JWT validation (5-second tolerance in `JwtService`), and Redis unavailability (fallback to reject refresh requests rather than serve stale tokens).


## 13. Security Considerations

The `AuthService` implements defense-in-depth security. Passwords are never stored in plaintext; `PasswordHasher` uses bcrypt with cost factor 12. The `JwtService` signs tokens with RS256 using 2048-bit RSA keys rotated quarterly. Refresh tokens are stored as hashed values in Redis by `TokenManager` to prevent token theft from compromising sessions. All endpoints enforce TLS 1.3, and sensitive fields (password, tokens) are excluded from application logs.

Account lockout after 5 failed login attempts within 15 minutes mitigates brute-force attacks. Password reset tokens are single-use with 1-hour expiry. CORS is restricted to known frontend origins.


## 14. Observability & Monitoring

The `AuthService` emits structured logs for all authentication events (login success/failure, registration, token refresh, password reset). Metrics are exposed via Prometheus: `auth_login_total` (counter), `auth_login_duration_seconds` (histogram), `auth_token_refresh_total` (counter), `auth_registration_total` (counter). Distributed tracing via OpenTelemetry spans covers the full request lifecycle through `AuthService`, `PasswordHasher`, `TokenManager`, and `JwtService`.

Alerts are configured for: login failure rate exceeding 20% over 5 minutes, p95 latency exceeding 500ms, and `TokenManager` Redis connection failures.


## 15. Testing Strategy

### 15.1 Test Pyramid

|Level|Coverage Target|Tools|Focus Areas|
|-------|----------------|-------|-------------|
|Unit|80%|Jest, ts-jest|`AuthService` methods, `PasswordHasher` hashing/verification, `JwtService` sign/verify, `TokenManager` token lifecycle, `UserProfile` validation|
|Integration|15%|Supertest, testcontainers|API endpoint request/response cycles, database operations, Redis token storage, `AuthService` to `PasswordHasher` to database flow|
|E2E|5%|Playwright|`LoginPage` login flow, `RegisterPage` registration flow, `AuthProvider` token refresh, full user journey from registration to profile view|

### 15.2 Test Cases

**Unit Tests:**

|Test Case|Component|Validates|
|-----------|-----------|-----------|
|Login with valid credentials returns `AuthToken`|`AuthService`|FR-AUTH-001: `AuthService.login()` calls `PasswordHasher.verify()`, then `TokenManager.issueTokens()`, returns valid `AuthToken` with accessToken and refreshToken|
|Login with invalid credentials returns error|`AuthService`|FR-AUTH-001: `AuthService.login()` returns 401 when `PasswordHasher.verify()` returns false; no `AuthToken` is issued|
|Token refresh with valid refresh token|`TokenManager`|FR-AUTH-003: `TokenManager.refresh()` validates the refresh token, revokes the old token, issues new `AuthToken` pair via `JwtService`|

**Integration Tests:**

|Test Case|Scope|Validates|
|-----------|-------|-----------|
|Registration persists `UserProfile` to database|`AuthService` + PostgreSQL|FR-AUTH-002: full flow from API request through `PasswordHasher` to database insert|
|Expired refresh token rejected by `TokenManager`|`TokenManager` + Redis|FR-AUTH-003: Redis TTL expiration correctly invalidates refresh tokens|

**E2E Tests:**

|Test Case|Flow|Validates|
|-----------|------|-----------|
|User registers and logs in|`RegisterPage` -> `LoginPage` -> ProfilePage|FR-AUTH-001, FR-AUTH-002: complete user journey through `AuthProvider`|

### 15.3 Test Environments

|Environment|Purpose|Data|
|-------------|---------|------|
|Local|Developer testing|Docker Compose with PostgreSQL and Redis containers|
|CI|Automated pipeline|testcontainers for ephemeral databases|
|Staging|Pre-production validation|Seeded test accounts, isolated from production|


## 16. Accessibility Requirements

Not applicable — backend service. The `AuthService` is a REST API with no direct UI rendering. Accessibility requirements for `LoginPage`, `RegisterPage`, and `AuthProvider` are defined in the frontend TDD (FE-AUTH-001-TDD).


## 17. Performance Budgets

Backend performance targets for the `AuthService` are defined in NFR-PERF-001 and NFR-PERF-002. The `PasswordHasher` bcrypt cost factor of 12 has been benchmarked at ~300ms per hash operation, which fits within the 200ms p95 target when combined with connection pooling optimizations. The `JwtService` sign and verify operations complete in under 5ms. `TokenManager` Redis operations target < 10ms latency.


## 18. Dependencies

The `AuthService` depends on PostgreSQL 15+ for `UserProfile` persistence, Redis 7+ for refresh token management by `TokenManager`, and Node.js 20 LTS as the runtime. External dependencies include the `bcryptjs` library for `PasswordHasher`, `jsonwebtoken` for `JwtService`, and SendGrid API for password reset emails. The service has no internal service dependencies beyond the database and cache layers.


## 19. Migration & Rollout Plan

### 19.1 Migration Strategy

|Phase|Description|Duration|Success Criteria|
|-------|-------------|----------|-----------------|
|Phase 1: Internal Alpha|Deploy `AuthService` to staging. auth-team and QA test all endpoints. `LoginPage` and `RegisterPage` available behind feature flag `AUTH_NEW_LOGIN`.|1 week|All FR-AUTH-001 through FR-AUTH-005 pass manual testing. Zero P0/P1 bugs.|
|Phase 2: Beta (10%)|Enable `AUTH_NEW_LOGIN` for 10% of traffic. Monitor `AuthService` latency, error rates, and `TokenManager` Redis usage. `AuthProvider` handles token refresh under real load.|2 weeks|p95 latency < 200ms. Error rate < 0.1%. No `TokenManager` Redis connection failures.|
|Phase 3: General Availability (100%)|Remove feature flag `AUTH_NEW_LOGIN`. All users route through new `AuthService`. Legacy auth endpoints deprecated. `AUTH_TOKEN_REFRESH` flag enables refresh token flow.|1 week|99.9% uptime over first 7 days. All monitoring dashboards green.|

### 19.2 Feature Flags

|Flag|Purpose|Default|Removal Target|
|------|---------|---------|---------------|
|`AUTH_NEW_LOGIN`|Gates access to new `LoginPage` and `AuthService` login endpoint|OFF|Remove after Phase 3 GA|
|`AUTH_TOKEN_REFRESH`|Enables refresh token flow in `TokenManager`; when OFF, only access tokens are issued|OFF|Remove after Phase 3 + 2 weeks|

### 19.3 Rollback Procedure

1. Disable `AUTH_NEW_LOGIN` feature flag to route traffic back to legacy auth
2. Verify legacy login flow is operational via smoke tests
3. Investigate `AuthService` failure root cause using structured logs and traces
4. If data corruption is detected in `UserProfile` table, restore from last known-good backup
5. Notify auth-team and platform-team via incident channel
6. Post-mortem within 48 hours of rollback

### 19.4 Rollback Criteria

Rollback is triggered if any of the following occur during rollout:
- p95 latency exceeds 1000ms for more than 5 minutes
- Error rate exceeds 5% for more than 2 minutes
- `TokenManager` Redis connection failures exceed 10 per minute
- Any data loss or corruption detected in `UserProfile` records


## 20. Risks & Mitigations

|ID|Risk|Probability|Impact|Mitigation|Contingency|
|----|------|------------|--------|------------|-------------|
|R-001|Token theft via XSS allows session hijacking|Medium|High|Store `AuthToken` accessToken in memory only (not localStorage). `AuthProvider` clears tokens on tab close. HttpOnly cookies for refreshToken. `JwtService` uses short 15-minute expiry.|Immediate token revocation via `TokenManager`. Force password reset for affected `UserProfile` accounts.|
|R-002|Brute-force attacks on login endpoint|High|Medium|Rate limiting at API Gateway (10 req/min per IP). Account lockout after 5 failed attempts in `AuthService`. `PasswordHasher` bcrypt cost factor 12 makes offline cracking expensive.|Block offending IPs at WAF level. Enable CAPTCHA challenge on `LoginPage` after 3 failed attempts.|
|R-003|Data loss during migration from legacy auth|Low|High|Run `AuthService` in parallel with legacy system during Phase 1 and Phase 2. `UserProfile` migration uses idempotent upsert operations. Full database backup before each phase.|Rollback to legacy auth system. Restore `UserProfile` data from pre-migration backup.|


## 21. Alternatives Considered

**Alternative 0: Do Nothing** — Continue without centralized authentication. Rejected because the platform cannot support user-specific features or pass security audits without a proper auth system.

**Alternative 1: Third-party auth provider (Auth0, Firebase Auth)** — Would reduce implementation effort but introduces vendor lock-in, ongoing SaaS costs, and limited customization of the `UserProfile` schema and `TokenManager` behavior. Rejected in favor of a self-hosted `AuthService` that provides full control over the authentication flow.

**Alternative 2: Session-based authentication with cookies** — Simpler implementation but requires server-side session storage, complicating horizontal scaling of `AuthService`. JWT-based approach via `JwtService` was chosen for stateless verification across multiple service instances.


## 22. Open Questions

|ID|Question|Owner|Target Date|Status|Resolution|
|----|----------|-------|-------------|--------|------------|
|OQ-001|Should `AuthService` support API key authentication for service-to-service calls?|test-lead|2026-04-15|Open|Deferred to v1.1 scope discussion|
|OQ-002|What is the maximum allowed `UserProfile` roles array length?|auth-team|2026-04-01|Open|Pending RBAC design review|


## 23. Timeline & Milestones

### 23.1 High-Level Timeline

|Milestone|Target Date|Deliverables|
|-----------|------------|-------------|
|M1: Core `AuthService`|2026-04-14|`AuthService`, `PasswordHasher`, `UserProfile` schema, POST `/auth/register`, POST `/auth/login`|
|M2: Token Management|2026-04-28|`TokenManager`, `JwtService`, `AuthToken` model, POST `/auth/refresh`, GET `/auth/me`|
|M3: Password Reset|2026-05-12|FR-AUTH-005 password reset flow, email integration|
|M4: Frontend Integration|2026-05-26|`LoginPage`, `RegisterPage`, `AuthProvider` components|
|M5: GA Release|2026-06-09|Phase 3 rollout complete, feature flags removed|

### 23.2 Implementation Phases

**Phase 1 (M1-M2):** Build `AuthService` core with `PasswordHasher` and `TokenManager`. Exit criteria: all unit tests pass, integration tests against PostgreSQL and Redis pass.

**Phase 2 (M3-M4):** Add password reset flow and frontend components. Exit criteria: E2E tests pass through `LoginPage` and `RegisterPage`.

**Phase 3 (M5):** Rollout and stabilization. Exit criteria: 99.9% uptime over 7 days in production.


## 24. Release Criteria

### 24.1 Definition of Done

- [ ] All functional requirements (FR-AUTH-001 through FR-AUTH-005) implemented and verified with passing tests
- [ ] Unit test coverage for `AuthService`, `TokenManager`, `JwtService`, and `PasswordHasher` exceeds 80%
- [ ] Integration tests for all four API endpoints pass against real PostgreSQL and Redis instances
- [ ] Security review completed: `PasswordHasher` bcrypt cost factor verified, `JwtService` RS256 key rotation documented
- [ ] Performance testing confirms all endpoints meet < 200ms p95 latency target under 500 concurrent users

### 24.2 Release Checklist

- [ ] `AuthService` deployed to staging and smoke-tested
- [ ] `LoginPage` and `RegisterPage` functional in staging environment
- [ ] `AuthProvider` token refresh verified with 15-minute access token expiry
- [ ] Feature flags `AUTH_NEW_LOGIN` and `AUTH_TOKEN_REFRESH` configured in production
- [ ] Runbooks reviewed and published for on-call team
- [ ] Monitoring dashboards verified: `auth_login_total`, `auth_login_duration_seconds`, `auth_token_refresh_total`
- [ ] Rollback procedure tested in staging
- [ ] `UserProfile` data migration script validated with production-like dataset
- [ ] Go/no-go sign-off from test-lead and eng-manager


## 25. Operational Readiness

### 25.1 Runbook

|Scenario|Symptoms|Diagnosis|Resolution|Escalation|
|----------|----------|-----------|------------|------------|
|`AuthService` down|5xx errors on all `/auth/*` endpoints; `LoginPage` and `RegisterPage` show error state|Check `AuthService` pod health in Kubernetes. Verify PostgreSQL connectivity. Check `PasswordHasher` and `TokenManager` initialization logs.|Restart `AuthService` pods. If PostgreSQL is unreachable, failover to read replica. If Redis is down, `TokenManager` will reject refresh requests — users must re-login via `LoginPage`.|Page auth-team on-call. If unresolved in 15 minutes, escalate to platform-team.|
|Token refresh failures|Users report being logged out unexpectedly; `AuthProvider` enters redirect loop to `LoginPage`; `auth_token_refresh_total` error counter spikes|Check Redis connectivity from `TokenManager`. Verify `JwtService` signing key is accessible. Check `AUTH_TOKEN_REFRESH` feature flag state.|If Redis is degraded, scale Redis cluster. If `JwtService` key is unavailable, re-mount secrets volume. If feature flag is OFF, enable `AUTH_TOKEN_REFRESH`.|Page auth-team on-call. If Redis cluster issue, escalate to platform-team.|

### 25.2 On-Call Expectations

|Aspect|Expectation|
|--------|-------------|
|Response time|Acknowledge P1 alerts within 15 minutes|
|Coverage|auth-team provides 24/7 on-call rotation during first 2 weeks post-GA|
|Tooling|Access to Kubernetes dashboards, Grafana monitoring, Redis CLI, PostgreSQL admin|
|Escalation path|auth-team on-call -> test-lead -> eng-manager -> platform-team|

### 25.3 Capacity Planning

|Resource|Current Capacity|Expected Load|Scaling Plan|
|----------|-----------------|---------------|-------------|
|`AuthService` pods|3 replicas|500 concurrent users|HPA scales to 10 replicas based on CPU > 70%|
|PostgreSQL connections|100 pool size|50 avg concurrent queries|Increase pool to 200 if connection wait time > 50ms|
|Redis memory|1 GB|~100K refresh tokens (~50 MB)|Monitor memory usage; scale to 2 GB if > 70% utilized|


## 26. Cost & Resource Estimation

Infrastructure costs for the `AuthService` are estimated at $450/month for production: 3 Kubernetes pods ($150), managed PostgreSQL ($200), managed Redis ($100). Costs scale linearly with user growth; each additional 10K users adds approximately $50/month in database and cache resources.


## 27. References & Resources

### 27.1 Related Documents

|Document|Relevance|
|----------|-----------|
|AUTH-PRD-001|Product requirements that this TDD implements|
|SEC-POLICY-001|Organization security policy governing `PasswordHasher` and `JwtService` configurations|

### 27.2 External References

|Resource|URL|
|----------|-----|
|JWT RFC 7519|https://datatracker.ietf.org/doc/html/rfc7519|
|bcrypt paper|https://www.usenix.org/legacy/events/usenix99/provos/provos.pdf|
|OWASP Authentication Cheat Sheet|https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html|


## 28. Glossary

|Term|Definition|
|------|-----------|
|JWT|JSON Web Token — a compact, URL-safe token format used by `JwtService` for stateless authentication|
|bcrypt|Adaptive password hashing function used by `PasswordHasher` with configurable cost factor|
|Refresh Token|Long-lived opaque token managed by `TokenManager` in Redis, exchanged for new `AuthToken` pairs|
|Access Token|Short-lived JWT issued by `JwtService`, carried in Authorization header for API authentication|
|Cost Factor|bcrypt work factor parameter (set to 12 in `PasswordHasher`) controlling hash computation time|