# Research Report 03: PRD Fixture Requirements

**Researcher**: researcher-03
**Topic**: Patterns & Conventions — PRD Fixture Requirements
**Status**: Complete
**Created**: 2026-03-27

---

## Scope

Determine what `test-prd-user-auth.md` must contain so it serves as the product-level precursor to the existing TDD and spec fixtures, reads like a PM wrote it, and does NOT trigger TDD auto-detection.

---

## 1. PRD Template Section Structure (from `src/superclaude/examples/prd_template.md`)

The PRD template defines 28 sections. Full Table of Contents (lines 123-150 of template):

| # | Section Name | Pipeline Relevance |
|---|---|---|
| 1 | Executive Summary | HIGH - overview + key success metrics |
| 2 | Problem Statement | HIGH - business rationale, "why this feature" |
| 3 | Background & Strategic Fit | MEDIUM - strategic context |
| 4 | Product Vision | MEDIUM - north star alignment |
| 5 | Business Context | HIGH - business justification, cost drivers |
| 6 | Jobs To Be Done (JTBD) | HIGH - user outcomes that ground roadmap phases |
| 7 | User Personas | HIGH - shapes acceptance criteria completeness |
| 8 | Value Proposition Canvas | N/A for Feature PRD (template line 375) |
| 9 | Competitive Analysis | N/A for Feature PRD (template line 376) |
| 10 | Assumptions & Constraints | MEDIUM |
| 11 | Dependencies | MEDIUM |
| 12 | Scope Definition | HIGH - prevents scope creep during phased planning |
| 13 | Open Questions | MEDIUM |
| 14 | Technical Requirements | HIGH - FRs and NFRs in product language |
| 15 | Technology Stack | LOW for PRD (engineering detail) |
| 16 | User Experience Requirements | HIGH - user flows, customer journeys |
| 17 | Legal & Compliance Requirements | HIGH - regulatory constraints |
| 18 | Business Requirements | N/A for Feature PRD (template line 383) |
| 19 | Success Metrics & Measurement | HIGH - original business-form metrics |
| 20 | Risk Analysis | MEDIUM |
| 21 | Implementation Plan (Epics/Stories/Phasing/DoD/Timeline) | HIGH - user stories + ACs |
| 22 | Customer Journey Map | HIGH - user-facing validation requirements |
| 23 | Error Handling & Edge Cases | HIGH - drives test strategy completeness |
| 24 | User Interaction & Design | MEDIUM |
| 25 | API Contract Examples | LOW for PRD |
| 26 | Contributors & Collaboration | LOW |
| 27 | Related Resources | LOW |
| 28 | Maintenance & Ownership | LOW |

### PRD Template YAML Frontmatter (lines 1-40 of template)

```yaml
id: "[PROJECT-ID]-PRD-CORE"
title: "[Product Name] - Product Requirements Document (PRD)"
description: "..."
version: "1.0"
status: "Draft"                    # NOT emoji-prefixed for fixture simplicity
type: "Product Requirements"       # CRITICAL: NOT "Technical Design Document"
priority: "Highest"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: "product-team"        # NOT "auth-team" (engineering)
autogen: false
coordinator: "product-manager"     # NOT "test-lead" (engineering)
parent_task: ""                    # NOT "parent_doc" (TDD field)
depends_on: []
related_docs: []
tags:
- prd
- requirements
- product-core
- user-stories
- acceptance-criteria
```

**Key differentiators from TDD frontmatter** (lines 1-54 of `test-tdd-user-auth.md`):
- TDD uses `type: "Technical Design Document"` -- PRD must use `type: "Product Requirements"`
- TDD uses `parent_doc: "AUTH-PRD-001"` -- PRD has no parent_doc field (it IS the parent)
- TDD uses `coordinator: "test-lead"` -- PRD uses `coordinator: "product-manager"`
- TDD uses `assigned_to: "auth-team"` -- PRD uses `assigned_to: "product-team"`
- TDD uses tags: `technical-design-document, architecture, specifications` -- PRD uses tags: `prd, requirements, user-stories, acceptance-criteria`
- TDD has `approvers` with `tech_lead, engineering_manager, architect, security` -- PRD has Document Approval with `Product Manager, Engineering Lead, Design Lead, Executive Sponsor`

---

## 2. TDD Fixture Feature Scope (from `.dev/test-fixtures/test-tdd-user-auth.md`)

### Feature Coverage

The TDD covers "User Authentication Service" with these components (lines 198-211):
- `AuthService` - core orchestration layer
- `TokenManager` and `JwtService` - JWT access/refresh token lifecycle
- `PasswordHasher` - bcrypt with configurable cost factor
- RESTful API endpoints: `/auth/login`, `/auth/register`, `/auth/me`, `/auth/refresh`
- `UserProfile` and `AuthToken` data models backed by PostgreSQL
- Frontend integration: `LoginPage`, `RegisterPage`, `AuthProvider`

### Functional Requirements (lines 280-287)

| ID | Name | Brief Description |
|---|---|---|
| FR-AUTH-001 | Login with email and password | Authenticate via email/password, return AuthToken with accessToken+refreshToken |
| FR-AUTH-002 | User registration with validation | Create accounts with email uniqueness, password strength, UserProfile creation |
| FR-AUTH-003 | JWT token issuance and refresh | Issue JWT access tokens (15min) and refresh tokens (7d), support silent refresh |
| FR-AUTH-004 | User profile retrieval | Return authenticated user's UserProfile via /auth/me |
| FR-AUTH-005 | Password reset flow | Two-step reset: request (email with token) + confirmation (validate token, update password) |

### Non-Functional Requirements (lines 289-309)

| ID | Category | Requirement |
|---|---|---|
| NFR-PERF-001 | Performance | All auth endpoints < 200ms p95 |
| NFR-PERF-002 | Performance | Support 500 concurrent login requests |
| NFR-REL-001 | Reliability | 99.9% uptime over 30-day windows |
| NFR-SEC-001 | Security | bcrypt with cost factor 12 |
| NFR-SEC-002 | Security | RS256 with 2048-bit RSA keys |

### Key Identifiers Used in TDD

- Components: `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserRepo`
- Data models: `UserProfile`, `AuthToken`, `RefreshTokenRecord`
- Infrastructure: PostgreSQL (users), Redis (tokens), Email (reset)
- Frontend: `LoginPage`, `RegisterPage`, `AuthProvider`
- Parent PRD reference: `AUTH-PRD-001` (lines 14, 28, 31, 59, 79, 83, 202)

---

## 3. Spec Fixture Comparison (from `.dev/test-fixtures/test-spec-user-auth.md`)

### Spec Frontmatter (lines 1-19)

```yaml
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
quality_scores:
  clarity: 8.0
  completeness: 7.5
  testability: 8.5
  consistency: 8.0
  overall: 8.0
```

**Spec uses numbered `## N. Heading` sections** (lines 23, 44, 82, 143, etc.):
- `## 1. Problem Statement`
- `## 2. Solution Overview`
- `## 3. Functional Requirements` (with FR-AUTH.1 through FR-AUTH.5)
- `## 4. Architecture`
- `## 5. Interface Contracts`
- `## 6. Non-Functional Requirements` (NFR-AUTH.1 through NFR-AUTH.3)
- `## 7. Risk Assessment`
- `## 8. Test Plan`
- `## 9. Migration & Rollout`
- `## 10. Downstream Inputs`
- `## 11. Open Items`
- `## 12. Brainstorm Gap Analysis`

**The spec uses a different FR ID format**: `FR-AUTH.1` (dot notation) vs TDD's `FR-AUTH-001` (dash-padded notation).

**The PRD fixture must NOT use numbered `## N. Heading` format** -- that is the spec/TDD pattern. PRD sections use descriptive headings per the PRD template.

---

## 4. Pipeline Content Types the PRD Must Serve

From the research prompt at `.dev/tasks/to-do/RESEARCH-PROMPT-prd-pipeline-integration.md` (lines 12-21), the pipeline needs these 8 content types from the PRD that are lost in the PRD-to-TDD translation:

1. **Business rationale / strategic fit / "why now"** -- informs roadmap prioritization
2. **User personas and stakeholder segments** -- shapes AC completeness
3. **Jobs To Be Done (JTBD)** -- grounds roadmap phases in user outcomes
4. **Success metrics in original business form** -- before TDD converts to engineering proxies
5. **Scope boundaries with rationale** -- prevents scope creep
6. **Compliance / legal / policy constraints** -- ensures regulatory work is planned
7. **Customer journey / UX-critical flows** -- identifies user-facing validation requirements
8. **Product edge cases and error scenarios** -- drives test strategy completeness

---

## 5. PRD Fixture Content Requirements for `test-prd-user-auth.md`

### 5.1 Frontmatter (must NOT trigger TDD auto-detection)

```yaml
id: "AUTH-PRD-001"
title: "User Authentication Service - Product Requirements Document (PRD)"
description: "Product requirements, user personas, success metrics, and acceptance criteria for the User Authentication Service"
version: "1.0"
status: "Draft"
type: "Product Requirements"          # CRITICAL: not "Technical Design Document"
priority: "Highest"
created_date: "2026-03-26"
updated_date: "2026-03-26"
assigned_to: "product-team"
autogen: false
coordinator: "product-manager"
parent_task: ""
depends_on: []
related_docs:
- "SEC-POLICY-001"
tags:
- prd
- requirements
- authentication
- user-stories
- acceptance-criteria
```

**Anti-TDD-detection requirements:**
- `type` field must be `"Product Requirements"` (not `"Technical Design Document"`)
- No `parent_doc` field (TDD-specific)
- No `approvers` block with `tech_lead`/`engineering_manager`/`architect`/`security` (TDD-specific)
- `coordinator` must be `"product-manager"` (not `"test-lead"`)
- `assigned_to` must be `"product-team"` (not `"auth-team"`)
- Tags must include `prd` and `requirements` (not `technical-design-document` or `architecture`)

### 5.2 Document Header

Must include the PRD template's standard header block (template lines 42-55):
- WHAT/WHY/HOW TO USE callout in product language
- Document Lifecycle Position table showing THIS PRD as Requirements phase, TDD as Design phase
- Tiered Usage table (Lightweight/Standard/Heavyweight)
- Product Type: "Feature PRD" (since this is a feature within a platform, not a standalone product)

### 5.3 Required Sections (Feature PRD, Standard Tier)

Based on PRD template section structure and Feature PRD scoping rules (SKILL.md lines 363-385), the fixture needs:

**Sections to INCLUDE (with content):**

| Section | PRD Fixture Content | Maps to Pipeline Content Type |
|---|---|---|
| S1: Executive Summary | 2-3 para product summary; 4 key success metrics (registration rate, login latency, session duration, failed login rate) | #4 (business metrics) |
| S2: Problem Statement | Business problem (users can't create accounts, no personalization, security audit failures); "Why This Feature is Required" subsection (not TAM/SAM/SOM) | #1 (business rationale) |
| S3: Background & Strategic Fit | Why auth is needed NOW: Q2 personalization features depend on it, compliance deadline in Q3, marketing projects 40% engagement lift | #1 (business rationale) |
| S4: Product Vision | North star: every user has a secure, frictionless identity that unlocks personalized experiences | #1 (business rationale) |
| S5: Business Context | Business justification only (no market sizing per Feature PRD rules); forward-reference S19 for KPIs | #1 (business rationale) |
| S6: Jobs To Be Done | 3-4 JTBD: "When I visit the platform, I want to create an account so I can access personalized features"; "When I return, I want to log in quickly so I can resume where I left off"; "When I forget my password, I want to reset it without contacting support" | #2 (JTBD) |
| S7: User Personas | 3 personas with names, goals, pain points: (1) "Alex the End User" - wants quick secure access, frustrated by re-login; (2) "Jordan the Platform Admin" - needs audit logs and account management; (3) "Sam the API Consumer" - needs programmatic token management, stable contracts | #2 (personas) |
| S10: Assumptions & Constraints | Email delivery infrastructure exists; PostgreSQL available; no social login in v1.0 | #5 (scope boundaries) |
| S11: Dependencies | Email service (SendGrid), PostgreSQL 15+, frontend routing | -- |
| S12: Scope Definition | IN: registration, login, logout, token refresh, profile, password reset. OUT: OAuth/OIDC, MFA, RBAC enforcement, social login. Rationale for each exclusion. | #5 (scope boundaries) |
| S13: Open Questions | Password reset sync vs async? Max refresh tokens per user? Account lockout policy after N failures? | -- |
| S14: Technical Requirements | FRs stated as user-facing requirements (same FR-AUTH.1 through FR-AUTH.5 but in product language); NFRs stated as user-perceived quality (same NFR-AUTH.1 through NFR-AUTH.3) | #4 (business metrics) |
| S16: User Experience Requirements | Feature-specific user flows only (per Feature PRD rules, line 378): signup flow, login flow, password reset flow. No onboarding/accessibility/localization (platform-level). | #7 (customer journey) |
| S17: Legal & Compliance | Feature-specific data handling: GDPR consent for data collection at registration, SOC2 audit logging for auth events, password storage compliance. Reference Platform PRD for full compliance. | #6 (compliance) |
| S19: Success Metrics | 4+ specific numeric targets: registration conversion > 60%, login p95 < 200ms, avg session duration > 30min, failed login rate < 5%, password reset completion > 80% | #4 (business metrics) |
| S20: Risk Analysis | Business risks: low adoption if UX is poor, security breach if implementation is flawed, compliance failure if audit logging is incomplete | -- |
| S21: Implementation Plan | Epics (AUTH-E1: Login/Registration, AUTH-E2: Token Management, AUTH-E3: Profile & Reset); User stories in "As a [persona], I want [action], so that [outcome]" format with acceptance criteria; phasing (Phase 1: core auth, Phase 2: password reset + profile) | #3 (JTBD grounding) |
| S22: Customer Journey Map | Detailed step-by-step flows: Signup (land -> click register -> fill form -> submit -> verify email -> confirmed); Login (land -> enter creds -> receive token -> access dashboard); Password Reset (click forgot -> enter email -> receive link -> set new password -> login with new) | #7 (customer journey) |
| S23: Error Handling & Edge Cases | Product-level edge cases: expired sessions while editing, password reset with unregistered email, concurrent login from multiple devices, account locked after brute force | #8 (edge cases) |
| S26-28: Contributors, Resources, Maintenance | Brief sections for completeness | -- |

**Sections to mark N/A (Feature PRD rules):**

| Section | Reason |
|---|---|
| S8: Value Proposition Canvas | N/A for Feature PRD (SKILL.md line 375) |
| S9: Competitive Analysis | N/A for Feature PRD (SKILL.md line 376) |
| S15: Technology Stack | Abbreviated -- reference TDD for full stack details |
| S18: Business Requirements | N/A for Feature PRD (SKILL.md line 383) |
| S24: User Interaction & Design | Abbreviated (no mockups in fixture) |
| S25: API Contract Examples | Abbreviated -- reference TDD for API specs |

### 5.4 FR/NFR ID Alignment

The PRD must use the SAME FR IDs as the TDD to enable cross-document traceability:

| PRD FR ID | PRD Requirement (product language) | TDD FR ID | TDD Requirement (engineering language) |
|---|---|---|---|
| FR-AUTH.1 | Users can log in with email and password and receive a session | FR-AUTH-001 | AuthService authenticates via email/password returning AuthToken |
| FR-AUTH.2 | New users can create an account with email and password | FR-AUTH-002 | AuthService creates accounts with validation and UserProfile |
| FR-AUTH.3 | Sessions persist across page refreshes without re-login | FR-AUTH-003 | TokenManager issues JWT access/refresh tokens via JwtService |
| FR-AUTH.4 | Logged-in users can view and manage their profile | FR-AUTH-004 | AuthService returns UserProfile via /auth/me |
| FR-AUTH.5 | Users can reset a forgotten password via email | FR-AUTH-005 | AuthService supports two-step password reset flow |

Note: PRD uses dot notation (FR-AUTH.1) matching the spec fixture convention, not the TDD's dash-padded notation (FR-AUTH-001). The TDD explicitly references `AUTH-PRD-001` as its parent (line 14), so the PRD fixture `id` field must be `AUTH-PRD-001`.

NFR alignment:

| PRD NFR ID | PRD Requirement (product language) | TDD NFR IDs |
|---|---|---|
| NFR-AUTH.1 | Login and registration must feel instant (< 200ms perceived) | NFR-PERF-001, NFR-PERF-002 |
| NFR-AUTH.2 | Service must be available 99.9% of the time | NFR-REL-001 |
| NFR-AUTH.3 | Passwords must be stored securely per industry standards | NFR-SEC-001, NFR-SEC-002 |

### 5.5 Persona Definitions

Three personas aligned with the track goal:

**Persona 1: Alex the End User**
- Role: Platform user who needs an account for personalized features
- Goals: Quick registration, fast login, seamless session persistence
- Pain points: Forced re-login every 15 minutes, no way to recover forgotten password, inconsistent session behavior
- JTBD: "When I visit the platform, I want to create an account quickly so I can start using personalized features"

**Persona 2: Jordan the Platform Admin**
- Role: Internal admin who manages user accounts and monitors auth health
- Goals: Visibility into failed login attempts, ability to lock/unlock accounts, audit trail for compliance
- Pain points: No centralized user management, no audit logs, manual account operations
- JTBD: "When a security incident occurs, I want to see who attempted access and lock compromised accounts"

**Persona 3: Sam the API Consumer**
- Role: Developer building integrations against the platform API
- Goals: Programmatic token management, stable authentication contracts, clear error codes
- Pain points: No standardized auth mechanism, ad-hoc API keys, no refresh capability
- JTBD: "When building an integration, I want to authenticate programmatically and refresh tokens without user interaction"

### 5.6 User Journeys (for S22 Customer Journey Map)

**Journey 1: First-time Signup**
1. User lands on platform -> sees "Sign Up" CTA
2. Clicks register -> fills email, password, display name
3. Submits form -> receives confirmation
4. (Optional) Verifies email via link
5. Redirected to dashboard as authenticated user

**Journey 2: Returning User Login**
1. User visits platform -> sees "Log In"
2. Enters email + password -> submits
3. Receives access token (15min) + refresh token (7d)
4. Accesses dashboard; token refreshes silently in background
5. After 7 days of inactivity, prompted to re-login

**Journey 3: Password Reset**
1. User clicks "Forgot Password" on login page
2. Enters email -> receives reset email (1h TTL token)
3. Clicks reset link -> enters new password
4. Password updated; all existing sessions invalidated
5. Redirected to login with new credentials

**Journey 4: Profile Management**
1. Authenticated user navigates to profile page
2. Views display name, email, account creation date
3. (Future: edit display name, change email)

### 5.7 Success Metrics (for S19)

| Metric | Target | Measurement | Business Rationale |
|---|---|---|---|
| Registration conversion rate | > 60% | Funnel: landing -> register form -> confirmed account | Validates frictionless onboarding |
| Login response time (p95) | < 200ms | APM on login endpoint | Users perceive anything > 200ms as slow |
| Average session duration | > 30 minutes | Token refresh analytics | Indicates engaged authenticated users |
| Failed login rate | < 5% of attempts | Auth event logging | High failure rate indicates UX or security issues |
| Password reset completion | > 80% | Funnel: reset requested -> new password set | Validates self-service recovery works |

### 5.8 Acceptance Scenarios (for S21 user stories)

**Happy Path:**
- New user registers with valid email/password -> account created, session started
- Existing user logs in with correct credentials -> token pair issued, dashboard loaded
- User with expired access token has valid refresh token -> silent refresh, no interruption
- User requests password reset -> email sent, new password set, old sessions invalidated

**Edge Cases:**
- Registration with duplicate email -> clear error, suggest login or reset
- Login with wrong password (< 5 attempts) -> generic error, no user enumeration
- Login with wrong password (>= 5 attempts) -> account locked, admin notification
- Password reset with unregistered email -> same success response (no enumeration)
- Expired reset token -> clear error, offer to request new reset
- Concurrent login from multiple devices -> both sessions valid (multi-device support)

---

## 6. What the PRD Fixture Must NOT Contain

### 6.1 No TDD-style numbered sections

The PRD must NOT use `## N. Heading` format (e.g., `## 1. Executive Summary`). Instead, use descriptive PRD headings without leading numbers to distinguish from the spec/TDD pattern. Reasoning: the pipeline's `detect_input_type()` may use section numbering patterns as a heuristic for document type detection.

**CORRECTION**: Looking at the PRD template more carefully (lines 154, 166, etc.), the template DOES use numbered sections: `## 1. Executive Summary`, `## 2. Problem Statement`, etc. The TDD also uses numbered sections but with a DIFFERENT numbering scheme (28 sections vs the spec's 12). The key differentiator is the **frontmatter `type` field**, not the section numbering. The PRD fixture SHOULD use the PRD template's numbered section format for template conformance.

### 6.2 No TDD-specific frontmatter

- No `type: "Technical Design Document"` -- must be `type: "Product Requirements"`
- No `parent_doc` field (PRD is the root document)
- No `approvers` block with engineering roles
- No `template_schema_doc`, `estimation`, `sprint` (engineering planning fields)
- No `blocker_reason`, `review_info` with engineering review cadence

### 6.3 No engineering implementation language

The PRD must read like a PM wrote it:
- "Users can log in" not "AuthService authenticates via PasswordHasher"
- "Sessions persist across page refreshes" not "TokenManager issues JWT via JwtService"
- "Passwords stored securely" not "bcrypt with cost factor 12"
- References to component names (`AuthService`, `TokenManager`) should appear only in a brief "Technical Context" subsection or S14 (Technical Requirements), not throughout the document

### 6.4 No architecture diagrams or data models

PRD should NOT contain:
- Component dependency graphs
- TypeScript interface definitions
- Database schema
- API endpoint specifications (those belong in the TDD)

PRD CAN contain:
- High-level system context ("the auth service sits between the client and the database")
- Data flow descriptions in user terms ("when you log in, the system verifies your password and gives you a session token")

---

## 7. Cross-Document Traceability Summary

```
test-prd-user-auth.md (AUTH-PRD-001)
  ├── id: AUTH-PRD-001
  ├── type: "Product Requirements"
  ├── FRs: FR-AUTH.1 through FR-AUTH.5 (product language, dot notation)
  ├── NFRs: NFR-AUTH.1 through NFR-AUTH.3 (user-perceived quality)
  ├── Personas: Alex (end user), Jordan (admin), Sam (API consumer)
  ├── Epics: AUTH-E1, AUTH-E2, AUTH-E3
  └── downstream: feeds AUTH-001-TDD
        │
        ▼
test-tdd-user-auth.md (AUTH-001-TDD)
  ├── id: AUTH-001-TDD
  ├── type: "Technical Design Document"
  ├── parent_doc: AUTH-PRD-001
  ├── FRs: FR-AUTH-001 through FR-AUTH-005 (engineering language, dash notation)
  ├── NFRs: NFR-PERF-001/002, NFR-REL-001, NFR-SEC-001/002
  ├── Components: AuthService, TokenManager, JwtService, PasswordHasher
  └── downstream: feeds spec/roadmap/tasklist
        │
        ▼
test-spec-user-auth.md (AUTH-001)
  ├── feature_id: AUTH-001
  ├── spec_type: new_feature
  ├── FRs: FR-AUTH.1 through FR-AUTH.5 (spec format, dot notation)
  ├── NFRs: NFR-AUTH.1 through NFR-AUTH.3
  └── downstream: feeds roadmap extraction
```

---

## 8. Estimated Fixture Size

Based on the spec fixture (~313 lines) and TDD fixture (~500+ lines), the PRD fixture should be approximately **250-350 lines**. This is sufficient for:
- Complete frontmatter (~40 lines)
- Document header + lifecycle table (~20 lines)
- 15-18 populated sections at Standard tier (~180-250 lines)
- 5-6 N/A sections (~20 lines)
- Appendices (~10 lines)

The fixture does NOT need to be a comprehensive production PRD. It needs to be large enough to:
1. Exercise all 8 pipeline content types from the research prompt
2. Provide traceable FRs/NFRs that map to the TDD and spec fixtures
3. Contain enough persona/JTBD/journey content to validate supplementary enrichment
4. Be structurally valid against the PRD template

---

## 9. Summary of Findings

The PRD fixture `test-prd-user-auth.md` must:

1. **Use PRD-appropriate frontmatter** with `id: AUTH-PRD-001`, `type: "Product Requirements"`, `coordinator: "product-manager"`, `assigned_to: "product-team"`, and PRD tags. No TDD-specific fields.

2. **Follow the PRD template's 28-section structure** but scoped as a Feature PRD (S8, S9, S18 marked N/A; S5, S16, S17 abbreviated per SKILL.md lines 363-385).

3. **Cover all 8 pipeline content types** identified in the research prompt: business rationale, personas, JTBD, business-form success metrics, scope boundaries, compliance constraints, customer journeys, and edge cases.

4. **Use FR-AUTH.1 through FR-AUTH.5 and NFR-AUTH.1 through NFR-AUTH.3** in product language (dot notation matching the spec fixture), traceable to the TDD's FR-AUTH-001 through FR-AUTH-005.

5. **Include 3 named personas** (Alex the End User, Jordan the Admin, Sam the API Consumer) with goals, pain points, and JTBD.

6. **Include 4+ user journeys** with step-by-step flows (signup, login, reset, profile).

7. **Include 5+ success metrics** with specific numeric targets in business form.

8. **Include acceptance scenarios** (happy path + edge cases) written as user stories.

9. **Read like a PM wrote it** -- product language throughout, no component references in main body, no architecture diagrams, no TypeScript interfaces.

10. **NOT trigger TDD auto-detection** -- no `type: "Technical Design Document"`, no `parent_doc` field, no engineering-role approvers block.
