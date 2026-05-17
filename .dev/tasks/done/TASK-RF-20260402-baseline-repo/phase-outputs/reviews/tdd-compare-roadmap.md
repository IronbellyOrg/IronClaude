# TDD Comparison: roadmap.md (Test 1 vs Test 3)

**Generated**: 2026-04-02
**Purpose**: Prove Test 1 (TDD) roadmap has richer, more specific content than Test 3 (spec) roadmap

---

## Frontmatter Comparison

| Field | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| spec_source | test-tdd-user-auth.md | test-spec-user-auth.md |
| complexity_score | 0.65 | 0.6 |
| adversarial | true | true |

Both have 3 core frontmatter fields. Structurally equivalent at this level.

---

## Backticked Identifier Presence Table

### Component/Model Identifiers

| Identifier | Test 1 (TDD) Count | Test 3 (Spec) Count | TDD Richer? |
|---|---|---|---|
| `UserProfile` | 14 | 0 | **YES** |
| `AuthToken` | 6 | 0 | **YES** |
| `AuthService` | 14 | 0 | **YES** |
| `TokenManager` | 21 | 2 | **YES** |
| `JwtService` | 15 | 2 | **YES** |
| `PasswordHasher` | 17 | 2 | **YES** |
| `LoginPage` | 15 | 0 | **YES** |
| `RegisterPage` | 13 | 0 | **YES** |
| `AuthProvider` | 14 | 0 | **YES** |

**Test 1 total backticked identifier mentions**: 129
**Test 3 total backticked identifier mentions**: 6

Test 3 only references 3 identifiers (`TokenManager`, `JwtService`, `PasswordHasher`) at 2 mentions each. Test 1 references all 9 identifiers extensively.

### Endpoint Path Identifiers

| Endpoint Path | Test 1 (TDD) Count | Test 3 (Spec) Count | TDD Richer? |
|---|---|---|---|
| `/auth/login` | 4 | 1 | **YES** |
| `/auth/register` | 4 | 1 | **YES** |
| `/auth/me` | 6 | 0 | **YES** |
| `/auth/refresh` | 2 | 1 | **YES** |

**Test 1 total endpoint path mentions**: 16
**Test 3 total endpoint path mentions**: 3

---

## Structural Comparison

| Aspect | Test 1 (TDD) | Test 3 (Spec) |
|---|---|---|
| Phase count | 6 (Phase 0-5) | 5 (Phase 1-5) |
| Executive summary identifiers | Lists all named components and pages | Generic "authentication service" language |
| Per-phase wiring tables | YES (detailed, per-phase) | YES (per-phase) |
| Endpoint-level task checklists | YES (all 6 endpoints with rate limits) | YES (6 endpoints) |
| Frontend component tasks | YES (AuthProvider, LoginPage, RegisterPage, ProfilePage with props) | NO (no frontend phase) |
| Per-endpoint rate limits specified | YES (10/5/60/30/5 req/min) | Partial |
| Rollback trigger thresholds | YES (p95 > 1000ms, error > 5%, Redis > 10/min) | YES |
| Architecture decision log | Referenced in Phase 0 | YES (ADC-1 through ADC-8) |

---

## Content Richness Assessment

Test 1's roadmap is substantially more specific than Test 3's:

1. **Named component threading**: Test 1 threads named components (`AuthService`, `TokenManager`, etc.) through every phase, making traceability from extraction to roadmap explicit. Test 3 uses generic service descriptions.

2. **Frontend phase**: Test 1 includes a dedicated Phase 3 for frontend integration (`AuthProvider`, `LoginPage`, `RegisterPage`, `ProfilePage`) with React-specific implementation details. Test 3 has no frontend phase -- its spec covers only backend.

3. **Per-endpoint granularity**: Test 1 specifies each endpoint with its rate limit, error codes, and audit log writes. Test 3 specifies endpoints but with less per-endpoint detail.

4. **Identifier density**: 129 backticked identifier mentions vs 6. The TDD roadmap is 21.5x more specific in named artifact references.

5. **Domain breadth**: Test 1 spans 5 domains (backend, security, frontend, testing, devops). Test 3 spans 3 domains (backend, security, database).

---

## Verdict: **TDD_RICHER_CONFIRMED**

Test 1 roadmap contains dramatically more specific, identifier-rich content than Test 3. The backticked identifier count (129 vs 6) demonstrates that TDD extraction propagates named components, data models, and API surfaces into the roadmap, producing a far more actionable planning document.
