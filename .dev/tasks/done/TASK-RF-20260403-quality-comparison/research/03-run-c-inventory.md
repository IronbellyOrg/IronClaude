# Run C Inventory: test1-tdd-prd-v2

**Inventory date:** 2026-04-03
**Source directory:** `.dev/test-fixtures/results/test1-tdd-prd-v2/`
**Status**: Complete
**Total .md files:** 13
**Total .err files:** 7 (all 0 bytes)

---

## 1. File Manifest

| File | Lines | Size | YAML Frontmatter |
|------|------:|-----:|------------------|
| extraction.md | 660 | 32,452 B | Yes (21 fields) |
| roadmap.md | 746 | 44,004 B | Yes (8 fields) |
| roadmap-opus-architect.md | 438 | 25,015 B | Yes (3 fields) |
| roadmap-haiku-architect.md | 886 | 53,791 B | Yes (7 fields) |
| diff-analysis.md | 162 | 12,339 B | Yes (2 fields) |
| debate-transcript.md | 162 | 15,849 B | Yes (2 fields) |
| base-selection.md | 71 | 8,131 B | Yes (2 fields) |
| anti-instinct-audit.md | 53 | 1,234 B | Yes (9 fields) |
| wiring-verification.md | 68 | 3,064 B | Yes (15 fields) |
| tasklist-index.md | 219 | 16,655 B | No |
| phase-1-tasklist.md | 1,325 | 58,653 B | No |
| phase-2-tasklist.md | 455 | 21,118 B | No |
| phase-3-tasklist.md | 408 | 17,913 B | No |

---

## 2. YAML Frontmatter Detail

### extraction.md
| Field | Value |
|-------|-------|
| spec_source | "test-tdd-user-auth.md" |
| generated | "2026-04-03T00:00:00Z" |
| generator | "extraction-agent-opus-4.6" |
| functional_requirements | 5 |
| nonfunctional_requirements | 8 |
| total_requirements | 13 |
| complexity_score | 0.55 |
| complexity_class | "MEDIUM" |
| domains_detected | [backend, security, frontend, testing, devops] |
| risks_identified | 7 |
| dependencies_identified | 10 |
| success_criteria_count | 10 |
| extraction_mode | "standard" |
| data_models_identified | 2 |
| api_surfaces_identified | 6 |
| components_identified | 9 |
| test_artifacts_identified | 6 |
| migration_items_identified | 15 |
| operational_items_identified | 9 |
| pipeline_diagnostics | {elapsed_seconds: 353.0, started_at: "2026-04-03T14:31:03Z", finished_at: "2026-04-03T14:36:56Z"} |

### roadmap.md (merged)
| Field | Value |
|-------|-------|
| spec_source | "test-tdd-user-auth.md" |
| prd_source | "test-prd-user-auth.md" |
| complexity_score | 0.55 |
| adversarial | true |
| base_variant | "B (Haiku Architect)" |
| variant_scores | "A:71 B:79" |
| convergence_score | 0.72 |
| timeline | "6 weeks" |

### roadmap-opus-architect.md
| Field | Value |
|-------|-------|
| spec_source | "test-tdd-user-auth.md" |
| complexity_score | 0.55 |
| primary_persona | architect |

### roadmap-haiku-architect.md
| Field | Value |
|-------|-------|
| spec_source | "test-tdd-user-auth.md" |
| prd_source | "test-prd-user-auth.md" |
| complexity_score | 0.55 |
| complexity_class | "MEDIUM" |
| primary_persona | architect |
| roadmap_version | "1.0" |
| generated | "2026-04-03T00:00:00Z" |

### diff-analysis.md
| Field | Value |
|-------|-------|
| total_diff_points | 14 |
| shared_assumptions_count | 18 |

### debate-transcript.md
| Field | Value |
|-------|-------|
| convergence_score | 0.72 |
| rounds_completed | 2 |

### base-selection.md
| Field | Value |
|-------|-------|
| base_variant | "B (Haiku Architect)" |
| variant_scores | "A:71 B:79" |

### anti-instinct-audit.md
| Field | Value |
|-------|-------|
| undischarged_obligations | 1 |
| uncovered_contracts | 4 |
| fingerprint_coverage | 0.73 |
| total_obligations | 1 |
| total_contracts | 8 |
| fingerprint_total | 45 |
| fingerprint_found | 33 |
| generated | "2026-04-03T14:58:12Z" |
| generator | superclaude-anti-instinct-audit |

### wiring-verification.md
| Field | Value |
|-------|-------|
| gate | wiring-verification |
| target_dir | src/superclaude |
| files_analyzed | 164 |
| files_skipped | 31 |
| rollout_mode | soft |
| analysis_complete | true |
| audit_artifacts_used | 0 |
| unwired_callable_count | 0 |
| orphan_module_count | 7 |
| unwired_registry_count | 0 |
| critical_count | 0 |
| major_count | 7 |
| info_count | 0 |
| total_findings | 7 |
| blocking_findings | 0 |

### tasklist-index.md, phase-1/2/3-tasklist.md
No YAML frontmatter present.

---

## 3. extraction.md Deep Analysis

### Structure
- **`## ` headers:** 14
- **Sections:** Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions, Data Models and Interfaces, API Specifications, Component Inventory, Testing Strategy, Migration and Rollout Plan, Operational Readiness

### Persona References
| Persona | Occurrences | Context |
|---------|----------:|---------|
| Alex | 1 | Architectural constraint (persona-driven design requirements) |
| Jordan | 2 | Architectural constraint (admin visibility), open questions |
| Sam | 2 | Architectural constraint (API consumer), open questions |

### Compliance References
| Term | Occurrences |
|------|----------:|
| GDPR | 3 |
| SOC2 | 5 |

### TDD Component Name References
| Component | Occurrences |
|-----------|----------:|
| AuthService | 36 |
| TokenManager | 25 |
| PasswordHasher | 21 |
| JwtService | 15 |
| LoginPage | 12 |
| RegisterPage | 9 |
| AuthProvider | 7 |
| UserRepo | 5 |
| ProfilePage | 4 |

### Data Model References
| Model | Occurrences |
|-------|----------:|
| UserProfile | 23 |
| AuthToken | 15 |

### API Endpoint References
| Endpoint | Occurrences |
|----------|----------:|
| /auth/login | 5 |
| /auth/register | 5 |
| /auth/me | 5 |
| /auth/reset-request | 5 |
| /auth/reset-confirm | 5 |
| /auth/refresh | 4 |
| /auth/logout | 0 (GAP-002 identifies this as missing) |

### Test ID References
| Test ID | Occurrences |
|---------|----------:|
| UT-001 | 0 |
| IT-001 | 0 |
| E2E-001 | 0 |

**Note:** extraction.md does not use formal test IDs. Tests are described by numbered test cases (1-6) across Unit/Integration/E2E levels.

---

## 4. roadmap.md (Merged) Deep Analysis

### Structure
- **`## ` headers:** 10
- **Sections:** Executive Summary, Phased Implementation Plan, Integration Points and Wiring Summary, Risk Assessment and Mitigation, Resource Requirements and Dependencies, Success Criteria and Validation Approach, Timeline Summary, Open Questions, Gap Resolution Summary, API Endpoint Inventory

### Persona References
| Persona | Occurrences |
|---------|----------:|
| Alex | 2 |
| Jordan | 6 |
| Sam | 6 |

### Compliance References
| Term | Occurrences |
|------|----------:|
| GDPR | 14 |
| SOC2 | 11 |

### TDD Component Name References
| Component | Occurrences |
|-----------|----------:|
| AuthService | 25 |
| PasswordHasher | 18 |
| TokenManager | 17 |
| JwtService | 13 |
| UserRepo | 11 |
| AuthProvider | 7 |
| RegisterPage | 4 |
| LoginPage | 3 |
| ProfilePage | 3 |

### Data Model References
| Model | Occurrences |
|-------|----------:|
| UserProfile | 9 |
| AuthToken | 5 |

### API Endpoint References
| Endpoint | Occurrences |
|----------|----------:|
| /auth/refresh | 5 |
| /auth/logout | 5 |
| /auth/login | 4 |
| /auth/me | 4 |
| /admin/auth/audit-logs | 4 |
| /auth/register | 3 |
| /auth/reset-request | 2 |
| /auth/reset-confirm | 2 |

### Test ID References
| Test ID | Occurrences |
|---------|----------:|
| UT-001 | 0 |
| IT-001 | 0 |
| E2E-001 | 0 |

**Note:** roadmap.md does not use formal test IDs. Testing described via coverage targets and validation methods.

---

## 5. Tasklist Files Analysis

### Task Counts
| File | Tasks (^### T) | Tier Distribution |
|------|-------------:|-------------------|
| phase-1-tasklist.md | 27 | STRICT: 15, STANDARD: 10, LIGHT: 2, EXEMPT: 0 |
| phase-2-tasklist.md | 9 | STRICT: 6, STANDARD: 4, LIGHT: 1, EXEMPT: 0 |
| phase-3-tasklist.md | 8 | STRICT: 3, STANDARD: 3, LIGHT: 0, EXEMPT: 2 |
| **Total** | **44** | **STRICT: 24, STANDARD: 17, LIGHT: 3, EXEMPT: 2** |

**Note:** tasklist-index.md reports tier distribution differently (STRICT:12/10/3, STANDARD:10/3/2, LIGHT:2/0/1, EXEMPT:3/1/2). The index counts are per-phase summaries; the grep counts include both metadata fields and body text mentions.

### Enrichment Pattern Coverage (Tasklist Files Combined)

#### Persona References
| Persona | index | phase-1 | phase-2 | phase-3 | Total |
|---------|------:|--------:|--------:|--------:|------:|
| Alex | 3 | 16 | 1 | 0 | 20 |
| Jordan | 4 | 2 | 4 | 0 | 10 |
| Sam | 3 | 5 | 6 | 3 | 17 |

#### Compliance References
| Term | index | phase-1 | phase-2 | phase-3 | Total |
|------|------:|--------:|--------:|--------:|------:|
| GDPR | 6 | 19 | 5 | 0 | 30 |
| SOC2 | 3 | 3 | 8 | 0 | 14 |

#### Component References (Tasklist Files Combined)
| Component | index | phase-1 | phase-2 | phase-3 | Total |
|-----------|------:|--------:|--------:|--------:|------:|
| AuthService | 5 | 29 | 5 | 6 | 45 |
| TokenManager | 4 | 22 | 2 | 0 | 28 |
| JwtService | 5 | 19 | 0 | 0 | 24 |
| PasswordHasher | 4 | 19 | 5 | 0 | 28 |
| UserRepo | 4 | 14 | 3 | 0 | 21 |
| UserProfile | 4 | 18 | 0 | 0 | 22 |
| AuthToken | 1 | 7 | 0 | 0 | 8 |
| LoginPage | 3 | 6 | 0 | 0 | 9 |
| RegisterPage | 3 | 6 | 0 | 0 | 9 |
| AuthProvider | 3 | 10 | 0 | 0 | 13 |
| ProfilePage | 3 | 8 | 0 | 0 | 11 |

#### API Endpoint References (Tasklist Files Combined)
| Endpoint | index | phase-1 | phase-2 | phase-3 | Total |
|----------|------:|--------:|--------:|--------:|------:|
| /auth/login | 2 | 7 | 0 | 3 | 12 |
| /auth/me | 2 | 7 | 0 | 0 | 9 |
| /auth/register | 2 | 4 | 0 | 0 | 6 |
| /auth/refresh | 2 | 4 | 0 | 1 | 7 |
| /auth/logout | 2 | 4 | 0 | 0 | 6 |
| /auth/reset-request | 2 | 0 | 3 | 0 | 5 |
| /auth/reset-confirm | 2 | 0 | 3 | 0 | 5 |

#### Test ID References (Tasklist Files)
| Test ID | index | phase-1 | phase-2 | phase-3 | Total |
|---------|------:|--------:|--------:|--------:|------:|
| UT-001 | 1 | 2 | 0 | 0 | 3 |
| IT-001 | 1 | 1 | 0 | 0 | 2 |
| E2E-001 | 1 | 2 | 0 | 0 | 3 |

---

## 6. anti-instinct-audit.md Analysis

| Metric | Value |
|--------|-------|
| fingerprint_coverage | **0.73** (33 of 45 fingerprints found) |
| undischarged_obligations | **1** (of 1 total) |
| uncovered_contracts | **4** (of 8 total contracts) |

### Undischarged Obligations
1. Line 553: `Hardcoded` in Phase 3: GA Rollout and Stabilization (feature)

### Uncovered Contracts (4)
1. IC-001: strategy_pattern — Section 15: Testing Strategy (line 136)
2. IC-002: strategy_pattern — Testing Strategy TOC reference (line 181)
3. IC-006: strategy_pattern — Section 15 heading (line 644)
4. IC-007: strategy_pattern — Migration Strategy heading (line 707)

### Missing Fingerprints (12 of 45)
`complexity_class`, `feature_id`, `spec_type`, `target_release`, `quality_scores`, `WHAT`, `SMTP`, `UUID`, `NULL`, `NULLABLE`, `AUTH_INVALID_CREDENTIALS`, `OWASP`

---

## 7. Adversarial Pipeline Artifacts Summary

| Artifact | Purpose | Key Finding |
|----------|---------|-------------|
| roadmap-opus-architect.md | Opus variant (A) | 9-week conservative timeline, 3 phases, progressive delivery |
| roadmap-haiku-architect.md | Haiku variant (B) | 4-week aggressive timeline, 3 phases, feature-complete Phase 1 |
| diff-analysis.md | Structured comparison | 14 divergence points, 18 shared assumptions |
| debate-transcript.md | Adversarial debate | 2 rounds, convergence score 0.72 |
| base-selection.md | Base variant pick | Haiku (B) selected at 79 vs Opus (A) at 71 |
| roadmap.md | Merged roadmap | 6-week compromise, Haiku base + Opus phasing |

---

## 8. Pipeline Artifact Completeness

| Expected Artifact | Present | Non-empty |
|-------------------|---------|-----------|
| extraction.md | Yes | Yes (660 lines) |
| extraction.err | Yes | No (0 bytes) |
| roadmap-opus-architect.md | Yes | Yes (438 lines) |
| roadmap-opus-architect.err | Yes | No (0 bytes) |
| roadmap-haiku-architect.md | Yes | Yes (886 lines) |
| roadmap-haiku-architect.err | Yes | No (0 bytes) |
| diff-analysis.md | Yes | Yes (162 lines) |
| diff-analysis.err | Yes | No (0 bytes) |
| debate-transcript.md | Yes | Yes (162 lines) |
| debate-transcript.err | Yes | No (0 bytes) |
| base-selection.md | Yes | Yes (71 lines) |
| base-selection.err | Yes | No (0 bytes) |
| roadmap.md | Yes | Yes (746 lines) |
| roadmap.err | Yes | No (0 bytes) |
| anti-instinct-audit.md | Yes | Yes (53 lines) |
| wiring-verification.md | Yes | Yes (68 lines) |
| tasklist-index.md | Yes | Yes (219 lines) |
| phase-1-tasklist.md | Yes | Yes (1,325 lines) |
| phase-2-tasklist.md | Yes | Yes (455 lines) |
| phase-3-tasklist.md | Yes | Yes (408 lines) |
| .roadmap-state.json | Yes | Yes (3,334 bytes) |
| artifacts/ | Yes | Empty |
| checkpoints/ | Yes | Empty |
| evidence/ | Yes | Empty |
| validation/ | Yes | Contains 1 item |

**All pipeline stages produced output. Zero errors logged.** Pipeline elapsed time: 353 seconds (5.9 minutes) per extraction frontmatter.

---

## Summary

Run C (test1-tdd-prd-v2) is a TDD+PRD pipeline run producing 13 .md files, 7 .err files (all empty), and a .roadmap-state.json. This is the most comprehensive run with 660-line extraction (21 YAML fields), 3 tasklist phases with 44 tasks, and the richest component coverage (AuthService=36, TokenManager=25, PasswordHasher=21, JwtService=15 in extraction alone). Haiku variant (B) was selected as base (79 vs 71), producing a 6-week merged roadmap. Key differentiators: 5 domains detected (vs 2 for Run A), 13 total requirements (vs 8 for Run A), TDD-specific sections (Data Models, API Specifications, Component Inventory, Testing Strategy, Migration Plan, Operational Readiness). Anti-instinct audit shows 0.73 fingerprint coverage (33/45), 1 undischarged obligation, 4 uncovered contracts.
