# PRD: [FEATURE_NAME]

> **This is a planning artifact, NOT an MDTM task file.**
> Produced during Phase 0 (Planning) of the `/rf:project` pipeline.
> Template: `.claude/templates/workflow/05_prd_template.md`

---

**Version:** [1.0]
**Status:** [Draft | In Review | Approved]
**Date:** [YYYY-MM-DD]

## References

- **Feature Brief**: [path to phase-outputs/reports/feature-brief.md]
- **Codebase Inventory**: [path to phase-outputs/discovery/codebase-inventory.md]
- **Research Notes**: [path to research notes file]

---

## Overview

[1-2 paragraph summary of the feature/project. Recap the problem and proposed solution from the Feature Brief. This section should give a reader unfamiliar with the project enough context to understand the requirements below.]

## Goals & Objectives

| # | Objective | Measurable Target | Priority |
|---|-----------|-------------------|----------|
| 1 | [Objective from feature brief, expanded] | [How to measure success] | [Must/Should/Could] |
| 2 | [...] | [...] | [...] |

---

## Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-001 | [Clear, specific requirement statement] | [Must/Should/Could] | [How to verify this requirement is met] |
| FR-002 | [...] | [...] | [...] |
| FR-003 | [...] | [...] | [...] |

> **Priority key:** Must = required for launch, Should = important but not blocking, Could = nice to have.

---

## Non-Functional Requirements

| ID | Category | Requirement | Target |
|----|----------|-------------|--------|
| NFR-001 | Performance | [e.g., "API response time under load"] | [e.g., "< 200ms at 100 concurrent users"] |
| NFR-002 | Security | [e.g., "Input validation on all endpoints"] | [e.g., "No SQL injection, XSS vectors"] |
| NFR-003 | Maintainability | [e.g., "Code follows existing project patterns"] | [e.g., "Passes existing linters"] |
| NFR-004 | Scalability | [...] | [...] |

---

## User Stories / Use Cases

### US-001: [Story Title]
**As a** [user role], **I want** [action/capability], **so that** [benefit/outcome].

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [...]

### US-002: [Story Title]
**As a** [user role], **I want** [action/capability], **so that** [benefit/outcome].

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [...]

---

## Data Model / Schema

> Include this section if the feature involves data storage, new entities, or schema changes. Remove if not applicable.

### Entities

| Entity | Description | Key Fields |
|--------|-------------|------------|
| [EntityName] | [What it represents] | [field1 (type), field2 (type), ...] |

### Relationships

- [EntityA] → [EntityB]: [relationship description, e.g., "one-to-many"]
- [...]

---

## API / Interface Definitions

> Include this section if the feature involves API endpoints, CLI commands, or public interfaces. Remove if not applicable.

| Method | Endpoint / Interface | Description | Input | Output |
|--------|---------------------|-------------|-------|--------|
| [GET/POST/etc.] | [/api/path or function signature] | [What it does] | [Key parameters] | [Response shape] |
| [...] | [...] | [...] | [...] | [...] |

---

## Dependencies

### External Dependencies

| Dependency | Purpose | Version/Constraint |
|------------|---------|-------------------|
| [Library/service name] | [Why it's needed] | [Version requirement or constraint] |

### Internal Dependencies

| Module/Component | Purpose | Impact |
|-----------------|---------|--------|
| [Existing module path] | [What we depend on from it] | [Risk if it changes] |

---

## Risks & Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | [What could go wrong] | [Low/Med/High] | [Low/Med/High] | [How to prevent or address] |
| 2 | [...] | [...] | [...] | [...] |

---

## Acceptance Criteria (Feature-Level)

The feature is considered **complete** when ALL of the following are true:

- [ ] All functional requirements (FR-*) are implemented and verified
- [ ] All non-functional requirements (NFR-*) meet their targets
- [ ] All user stories pass their acceptance criteria
- [ ] [Project-specific criterion, e.g., "Tests pass with >80% coverage"]
- [ ] [Project-specific criterion, e.g., "Documentation is complete"]

---

## Out of Scope

> Carried from Feature Brief. Included here for reference so reviewers don't ask for things explicitly excluded.

- [Item explicitly not part of this project]
- [...]
