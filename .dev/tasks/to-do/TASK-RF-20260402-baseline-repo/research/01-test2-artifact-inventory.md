# Research: Test 2 and Test 1 Artifact Inventory
**Topic type:** File Inventory
**Scope:** .dev/test-fixtures/results/test2-spec-modified/ and .dev/test-fixtures/results/test1-tdd-modified/
**Status:** Complete
**Date:** 2026-04-02
---

## 1. Directory Structure Overview

Both directories contain the same 18 files: 9 content `.md` files + 9 `.err` files (all `.err` files are 0 bytes). Additionally, each directory contains a `.roadmap-state.json` metadata file.

### Pipeline Steps (from .roadmap-state.json)

Both runs executed 9 steps in order: `extract` -> `generate-opus-architect` + `generate-haiku-architect` (parallel) -> `diff` -> `debate` -> `score` -> `merge` -> `anti-instinct` -> `wiring-verification`

- **Test 2** (spec input): All steps PASS except `anti-instinct` (FAIL). Total elapsed: ~14 min (15:39:59 - 15:53:49).
- **Test 1** (TDD input): All steps PASS except `anti-instinct` (FAIL). Total elapsed: ~14 min (15:15:14 - 15:28:57).

---

## 2. Test 2 Artifact Inventory (test2-spec-modified/)

**Input spec:** `test-spec-user-auth.md` (spec_hash: `2db9d8c5...`)

| # | File | Size (bytes) | Frontmatter Fields | Body Sections (## or ###) |
|---|------|--------------|--------------------|---------------------------|
| 1 | extraction.md | 17,129 | 14 | 16 |
| 2 | roadmap-opus-architect.md | 21,216 | 10 | 31 |
| 3 | roadmap-haiku-architect.md | 26,041 | 3 | 66 |
| 4 | diff-analysis.md | 12,674 | 2 | 21 |
| 5 | debate-transcript.md | 23,072 | 2 | 11 |
| 6 | base-selection.md | 10,431 | 2 | 16 |
| 7 | roadmap.md | 31,096 | 3 | 60 |
| 8 | anti-instinct-audit.md | 1,013 | 9 | 4 |
| 9 | wiring-verification.md | 3,064 | 16 | 7 |
| 10 | .roadmap-state.json | 3,228 | N/A | N/A |

**Total content size (excl. .err and .json):** 145,736 bytes

---

## 3. Test 1 Artifact Inventory (test1-tdd-modified/)

**Input spec:** `test-tdd-user-auth.md` (spec_hash: `43c9e660...`)

| # | File | Size (bytes) | Frontmatter Fields | Body Sections (## or ###) |
|---|------|--------------|--------------------|---------------------------|
| 1 | extraction.md | 27,999 | 20 | 43 |
| 2 | roadmap-opus-architect.md | 23,222 | 3 | 37 |
| 3 | roadmap-haiku-architect.md | 22,966 | 3 | 72 |
| 4 | diff-analysis.md | 10,627 | 2 | 18 |
| 5 | debate-transcript.md | 12,614 | 2 | 14 |
| 6 | base-selection.md | 12,733 | 2 | 17 |
| 7 | roadmap.md | 38,850 | 3 | 60 |
| 8 | anti-instinct-audit.md | 1,651 | 9 | 4 |
| 9 | wiring-verification.md | 3,064 | 16 | 7 |
| 10 | .roadmap-state.json | 3,218 | N/A | N/A |

**Total content size (excl. .err and .json):** 153,726 bytes

---

## 4. extraction.md Deep Dive

### Test 2 extraction.md (14 frontmatter fields, 16 body sections)

**Frontmatter fields (14):**
1. `spec_source` = test-spec-user-auth.md
2. `generated` = 2026-03-27T00:00:00Z
3. `generator` = requirements-extraction-specialist-v1
4. `functional_requirements` = 5
5. `nonfunctional_requirements` = 3
6. `total_requirements` = 8
7. `complexity_score` = 0.62
8. `complexity_class` = MEDIUM
9. `domains_detected` = [backend, security, database]
10. `risks_identified` = 3
11. `dependencies_identified` = 7
12. `success_criteria_count` = 8
13. `extraction_mode` = standard
14. `pipeline_diagnostics` = {elapsed_seconds: 121.4, ...}

**Body sections (16):**
1. `## Functional Requirements`
2. `### FR-AUTH.1: User Login`
3. `### FR-AUTH.2: User Registration`
4. `### FR-AUTH.3: Token Refresh`
5. `### FR-AUTH.4: Profile Retrieval`
6. `### FR-AUTH.5: Password Reset`
7. `## Non-Functional Requirements`
8. `### NFR-AUTH.1: Authentication Endpoint Latency`
9. `### NFR-AUTH.2: Service Availability`
10. `### NFR-AUTH.3: Password Hashing Security`
11. `## Complexity Assessment`
12. `## Architectural Constraints`
13. `## Risk Inventory`
14. `## Dependency Inventory`
15. `## Success Criteria`
16. `## Open Questions`

### Test 1 extraction.md (20 frontmatter fields, 43 body sections)

**Frontmatter fields (20):**
1. `spec_source` = test-tdd-user-auth.md
2. `generated` = 2026-03-27T00:00:00Z
3. `generator` = requirements-extraction-agent
4. `functional_requirements` = 5
5. `nonfunctional_requirements` = 4
6. `total_requirements` = 9
7. `complexity_score` = 0.65
8. `complexity_class` = MEDIUM
9. `domains_detected` = [backend, security, frontend, testing, devops]
10. `risks_identified` = 3
11. `dependencies_identified` = 6
12. `success_criteria_count` = 7
13. `extraction_mode` = standard
14. `data_models_identified` = 2
15. `api_surfaces_identified` = 4
16. `components_identified` = 4
17. `test_artifacts_identified` = 6
18. `migration_items_identified` = 3
19. `operational_items_identified` = 2
20. `pipeline_diagnostics` = {elapsed_seconds: 158.6, ...}

**Body sections (43):**
1. `## Functional Requirements`
2. `## Non-Functional Requirements`
3. `## Complexity Assessment`
4. `## Architectural Constraints`
5. `## Risk Inventory`
6. `## Dependency Inventory`
7. `## Success Criteria`
8. `## Open Questions`
9. `## Data Models and Interfaces`
10. `### Entity: UserProfile`
11. `### Entity: AuthToken`
12. `### Relationships`
13. `### Additional Data Stores`
14. `## API Specifications`
15. `### Endpoint Inventory`
16. `### Endpoint: POST /auth/login`
17. `### Endpoint: POST /auth/register`
18. `### Endpoint: GET /auth/me`
19. `### Endpoint: POST /auth/refresh`
20. `### Error Response Format`
21. `### Versioning Strategy`
22. `### Implicit Endpoints (from FR-AUTH-005)`
23. `## Component Inventory`
24. `### Route/Page Structure`
25. `### Shared Components`
26. `### Component Hierarchy`
27. `### Backend Components`
28. `## Testing Strategy`
29. `### Test Pyramid`
30. `### Test Cases -- Unit`
31. `### Test Cases -- Integration`
32. `### Test Cases -- E2E`
33. `### Test Environments`
34. `## Migration and Rollout Plan`
35. `### Migration Phases`
36. `### Feature Flags`
37. `### Rollback Procedure`
38. `### Rollback Trigger Criteria`
39. `## Operational Readiness`
40. `### Runbook Scenarios`
41. `### On-Call Expectations`
42. `### Capacity Planning`
43. `### Observability`

**Key difference:** Test 1 (TDD input) produces 6 additional top-level extraction sections not present in Test 2 (spec input): Data Models and Interfaces, API Specifications, Component Inventory, Testing Strategy, Migration and Rollout Plan, Operational Readiness. This reflects the TDD's richer structural content compared to a simpler spec.

---

## 5. anti-instinct-audit.md Deep Dive

### Test 2 (spec input)

**`fingerprint_coverage`: 0.72**

| Metric | Value |
|--------|-------|
| undischarged_obligations | 0 |
| uncovered_contracts | 3 |
| fingerprint_coverage | 0.72 |
| total_obligations | 0 |
| total_contracts | 6 |
| fingerprint_total | 18 |
| fingerprint_found | 13 |

- Missing fingerprints (5): JIRA, PASETO, UUID, REST, OWASP
- Pipeline status: FAIL (gate failure despite 0 undischarged obligations -- failed due to uncovered contracts)

### Test 1 (TDD input)

**`fingerprint_coverage`: 0.76**

| Metric | Value |
|--------|-------|
| undischarged_obligations | 5 |
| uncovered_contracts | 4 |
| fingerprint_coverage | 0.76 |
| total_obligations | 5 |
| total_contracts | 8 |
| fingerprint_total | 45 |
| fingerprint_found | 34 |

- Missing fingerprints (11): complexity_class, feature_id, spec_type, target_release, quality_scores, WHAT, CORS, SMTP, PRIMARY, AUTH_INVALID_CREDENTIALS, OWASP
- Undischarged obligations: 5 (all "skeleton" references in Phase 1 and Phase 2)
- Pipeline status: FAIL

---

## 6. roadmap.md Key Structural Features

### Test 2 (spec input) -- roadmap.md

- **Frontmatter:** spec_source, complexity_score (0.62), adversarial (true)
- **Size:** 31,096 bytes, 60 body sections
- **Title:** "Project Roadmap: User Authentication Service v1.0 -- Merged Final -- Adversarial Synthesis (Base: Variant B + Variant A Grafts)"
- **Base variant:** B (Haiku), with A (Opus) grafts
- **Phase structure:** Phase 0 through Phase 4 (5 phases)

### Test 1 (TDD input) -- roadmap.md

- **Frontmatter:** spec_source, complexity_score (0.65), adversarial (true)
- **Size:** 38,850 bytes, 60 body sections
- **Title:** Begins with "Executive Summary" (no H1 title)
- **Base variant:** B (Haiku)
- **Phase structure:** Phase 0 through Phase 5 (6 phases)

---

## 7. wiring-verification.md

Both Test 1 and Test 2 produce **identical** wiring-verification.md files (3,064 bytes each). Both report:
- files_analyzed: 166, files_skipped: 31
- 7 orphan modules (all in cli.cli_portify.steps), 0 blocking findings
- Pipeline status: PASS

This artifact is generated from the codebase state, not from the spec, so it is expected to be identical.

---

## 8. Variant Roadmap Files

### Test 2 variant files

| File | Size | Frontmatter Fields | Body Sections |
|------|------|--------------------|---------------|
| roadmap-opus-architect.md | 21,216 | 10 (spec_source, complexity_score, primary_persona, generated, generator, total_phases, total_milestones, total_requirements_mapped, risks_addressed, open_questions) | 31 |
| roadmap-haiku-architect.md | 26,041 | 3 (spec_source, complexity_score, primary_persona) | 66 |

### Test 1 variant files

| File | Size | Frontmatter Fields | Body Sections |
|------|------|--------------------|---------------|
| roadmap-opus-architect.md | 23,222 | 3 (spec_source, complexity_score, primary_persona) | 37 |
| roadmap-haiku-architect.md | 22,966 | 3 (spec_source, complexity_score, primary_persona) | 72 |

---

## 9. Adversarial Pipeline Files

### diff-analysis.md

| | Test 2 (spec) | Test 1 (TDD) |
|---|---|---|
| Size | 12,674 | 10,627 |
| Frontmatter | total_diff_points: 17, shared_assumptions_count: 17 | total_diff_points: 12, shared_assumptions_count: 14 |

### debate-transcript.md

| | Test 2 (spec) | Test 1 (TDD) |
|---|---|---|
| Size | 23,072 | 12,614 |
| Frontmatter | convergence_score: 0.64, rounds_completed: 2 | convergence_score: 0.72, rounds_completed: 2 |

### base-selection.md

| | Test 2 (spec) | Test 1 (TDD) |
|---|---|---|
| Size | 10,431 | 12,733 |
| Frontmatter | base_variant: B, variant_scores: "A:67 B:77" | base_variant: B, variant_scores: "A:71 B:78" |
| Selected base | Variant B (Haiku) | Variant B (Haiku) |

---

## 10. Comparison Summary Table (for task file template)

| Metric | Test 2 (spec input) | Test 1 (TDD input) |
|--------|---------------------|---------------------|
| Input spec | test-spec-user-auth.md | test-tdd-user-auth.md |
| complexity_score | 0.62 | 0.65 |
| Total content size | 145,736 B | 153,726 B |
| extraction.md size | 17,129 B | 27,999 B |
| extraction.md frontmatter fields | 14 | 20 |
| extraction.md body sections | 16 | 43 |
| roadmap.md size | 31,096 B | 38,850 B |
| roadmap.md body sections | 60 | 60 |
| roadmap phases | 5 (Phase 0-4) | 6 (Phase 0-5) |
| base_variant selected | B (Haiku) | B (Haiku) |
| variant_scores | A:67 B:77 | A:71 B:78 |
| convergence_score | 0.64 | 0.72 |
| diff_points | 17 | 12 |
| shared_assumptions | 17 | 14 |
| fingerprint_coverage | 0.72 | 0.76 |
| undischarged_obligations | 0 | 5 |
| anti-instinct status | FAIL | FAIL |
| wiring-verification status | PASS | PASS |
| Pipeline elapsed | ~14 min | ~14 min |
| All steps pass? | 8/9 (anti-instinct FAIL) | 8/9 (anti-instinct FAIL) |
