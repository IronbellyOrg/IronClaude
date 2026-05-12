# TDD Comparison: extraction.md (Test 1 vs Test 3)

**Generated**: 2026-04-02
**Purpose**: Prove Test 1 (TDD) extraction is a superset of Test 3 (spec) extraction

---

## Frontmatter Field Comparison

| Field | Test 1 (TDD) | Test 3 (Spec) | TDD-Specific? |
|---|---|---|---|
| spec_source | test-tdd-user-auth.md | test-spec-user-auth.md | No (different source) |
| generated | 2026-03-27T00:00:00Z | 2026-04-02T00:00:00Z | No |
| generator | requirements-extraction-agent | requirements-extraction-agent | No |
| functional_requirements | 5 | 5 | No |
| nonfunctional_requirements | 4 | 3 | No |
| total_requirements | 9 | 8 | No |
| complexity_score | 0.65 | 0.6 | No |
| complexity_class | MEDIUM | MEDIUM | No |
| domains_detected | [backend, security, frontend, testing, devops] | [backend, security, database] | No |
| risks_identified | 3 | 3 | No |
| dependencies_identified | 6 | 6 | No |
| success_criteria_count | 7 | 7 | No |
| extraction_mode | standard | standard | No |
| pipeline_diagnostics | {elapsed_seconds: 158.6, ...} | {elapsed_seconds: 73.3, ...} | No |
| data_models_identified | 2 | -- | **YES (TDD)** |
| api_surfaces_identified | 4 | -- | **YES (TDD)** |
| components_identified | 4 | -- | **YES (TDD)** |
| test_artifacts_identified | 6 | -- | **YES (TDD)** |
| migration_items_identified | 3 | -- | **YES (TDD)** |
| operational_items_identified | 2 | -- | **YES (TDD)** |

**Test 1 frontmatter fields**: 20
**Test 3 frontmatter fields**: 14
**TDD-specific fields**: 6 (data_models_identified, api_surfaces_identified, components_identified, test_artifacts_identified, migration_items_identified, operational_items_identified)

All 14 Test 3 fields are present in Test 1. Test 1 adds 6 TDD-specific fields.

---

## Body Section Comparison

### Test 1 (TDD) Top-Level Sections (14 `##` sections)

1. Functional Requirements
2. Non-Functional Requirements
3. Complexity Assessment
4. Architectural Constraints
5. Risk Inventory
6. Dependency Inventory
7. Success Criteria
8. Open Questions
9. **Data Models and Interfaces** (TDD-specific)
10. **API Specifications** (TDD-specific)
11. **Component Inventory** (TDD-specific)
12. **Testing Strategy** (TDD-specific)
13. **Migration and Rollout Plan** (TDD-specific)
14. **Operational Readiness** (TDD-specific)

### Test 3 (Spec) Top-Level Sections (8 `##` sections)

1. Functional Requirements
2. Non-Functional Requirements
3. Complexity Assessment
4. Architectural Constraints
5. Risk Inventory
6. Dependency Inventory
7. Success Criteria
8. Open Questions

### Total Headers (all `##` and `###` levels)

- **Test 1**: 43 headers
- **Test 3**: 20 headers

### TDD-Specific Top-Level Sections (6)

| TDD Section | Subsections | Content Summary |
|---|---|---|
| Data Models and Interfaces | Entity: UserProfile, Entity: AuthToken, Relationships, Additional Data Stores | Full TypeScript interface definitions, field constraint tables, storage details |
| API Specifications | Endpoint Inventory (4 endpoints), per-endpoint request/response schemas, Error Response Format, Versioning Strategy, Implicit Endpoints | Complete REST API surface with status codes, rate limits, error formats |
| Component Inventory | Route/Page Structure, Shared Components, Component Hierarchy, Backend Components | Frontend pages (LoginPage, RegisterPage, ProfilePage), backend services (AuthService, TokenManager, JwtService, PasswordHasher, UserRepo) |
| Testing Strategy | Test Pyramid, Test Cases (Unit/Integration/E2E), Test Environments | 6 test cases across 3 levels, coverage targets, tool selections |
| Migration and Rollout Plan | Migration Phases (3), Feature Flags (2), Rollback Procedure, Rollback Trigger Criteria | Phase 1 Alpha, Phase 2 Beta 10%, Phase 3 GA with feature flags |
| Operational Readiness | Runbook Scenarios (2), On-Call Expectations, Capacity Planning, Observability | Prometheus metrics, OpenTelemetry tracing, Grafana dashboards, alerting rules |

---

## Subset Verification

All 8 Test 3 top-level sections exist in Test 1:

| Test 3 Section | Present in Test 1? | Notes |
|---|---|---|
| Functional Requirements | YES | Test 1 uses table format with backticked identifiers; Test 3 uses narrative subsections |
| Non-Functional Requirements | YES | Test 1 has 4 NFRs (inc. security); Test 3 has 3 |
| Complexity Assessment | YES | Both MEDIUM; Test 1 scores 0.65, Test 3 scores 0.6 |
| Architectural Constraints | YES | Test 1 has 10 constraints; Test 3 has 10 |
| Risk Inventory | YES | Both have 3 risks |
| Dependency Inventory | YES | Both have 6 dependencies |
| Success Criteria | YES | Both have 7 criteria |
| Open Questions | YES | Test 1 has 6 (OQ-001 to OQ-006); Test 3 has 7 (OI-1 to OI-7) |

All Test 3 content categories are represented in Test 1. Test 1 additionally provides 6 TDD-specific sections with 23 additional subsection headers.

---

## Verdict: **SUPERSET_CONFIRMED**

Test 1 extraction contains all content categories present in Test 3, plus 6 additional TDD-specific frontmatter fields and 6 additional TDD-specific top-level body sections (with 23 additional subsections). Test 1 is a strict superset of Test 3.
