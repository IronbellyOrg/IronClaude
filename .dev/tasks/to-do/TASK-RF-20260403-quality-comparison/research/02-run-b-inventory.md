# Run B Inventory: test2-spec-prd-v2

**Source directory**: `.dev/test-fixtures/results/test2-spec-prd-v2/`
**Inventory date**: 2026-04-03
**Agent**: research (evidence-based, no inference)
**Status**: Complete

---

## 1. Directory Contents

| # | File | Size (bytes) | Lines | Type |
|---|------|-------------|-------|------|
| 1 | extraction.md | 14,403 | 247 | Pipeline artifact |
| 2 | roadmap-opus-architect.md | 23,252 | 377 | Variant roadmap |
| 3 | roadmap-haiku-architect.md | 41,350 | 659 | Variant roadmap |
| 4 | diff-analysis.md | 11,798 | 146 | Pipeline artifact |
| 5 | debate-transcript.md | 15,305 | 178 | Pipeline artifact |
| 6 | base-selection.md | 10,705 | 96 | Pipeline artifact |
| 7 | roadmap.md | 35,772 | 558 | Final merged roadmap |
| 8 | anti-instinct-audit.md | 1,205 | 46 | Pipeline artifact |
| 9 | wiring-verification.md | 3,064 | 68 | Pipeline artifact |
| 10 | .roadmap-state.json | 3,345 | 85 | Pipeline state |
| 11 | *.err (7 files) | 0 each | 0 | Empty error logs |

**Total .md files**: 9
**Total lines across .md**: 2,375

---

## 2. Per-File YAML Frontmatter

### 2.1 extraction.md

| Field | Value |
|-------|-------|
| spec_source | "test-spec-user-auth.md" |
| generated | "2026-04-03T00:00:00Z" |
| generator | "requirements-extraction-agent" |
| functional_requirements | 5 |
| nonfunctional_requirements | 6 |
| total_requirements | 11 |
| complexity_score | 0.6 |
| complexity_class | MEDIUM |
| domains_detected | [backend, security, frontend, infrastructure] |
| risks_identified | 7 |
| dependencies_identified | 7 |
| success_criteria_count | 7 |
| extraction_mode | standard |
| pipeline_diagnostics | {elapsed_seconds: 96.4, started_at: "2026-04-03T15:05:10", finished_at: "2026-04-03T15:06:46"} |

### 2.2 roadmap-opus-architect.md

| Field | Value |
|-------|-------|
| spec_source | "test-spec-user-auth.md" |
| complexity_score | 0.6 |
| primary_persona | architect |
| generated | "2026-04-03" |
| generator | "architect-roadmap-agent" |
| phases | 4 |
| total_requirements | 11 |
| total_risks | 7 |
| epics | ["AUTH-E1", "AUTH-E2", "AUTH-E3"] |

### 2.3 roadmap-haiku-architect.md

| Field | Value |
|-------|-------|
| spec_source | "test-spec-user-auth.md" |
| complexity_score | 0.6 |
| primary_persona | architect |

*Note*: Haiku variant has minimal frontmatter (3 fields) vs. Opus variant (9 fields).

### 2.4 diff-analysis.md

| Field | Value |
|-------|-------|
| total_diff_points | 14 |
| shared_assumptions_count | 12 |

### 2.5 debate-transcript.md

| Field | Value |
|-------|-------|
| convergence_score | 0.62 |
| rounds_completed | 2 |

### 2.6 base-selection.md

| Field | Value |
|-------|-------|
| base_variant | "Variant A (Opus Architect)" |
| variant_scores | "A:81 B:76" |

### 2.7 roadmap.md (final merged)

| Field | Value |
|-------|-------|
| spec_source | "test-spec-user-auth.md" |
| complexity_score | 0.6 |
| adversarial | true |
| base_variant | "Variant A (Opus Architect)" |
| variant_scores | "A:81 B:76" |
| convergence_score | 0.62 |
| debate_rounds | 2 |
| prd_source | "test-prd-user-auth.md" |

### 2.8 anti-instinct-audit.md

| Field | Value |
|-------|-------|
| undischarged_obligations | 2 |
| uncovered_contracts | 3 |
| fingerprint_coverage | 0.72 |
| total_obligations | 2 |
| total_contracts | 6 |
| fingerprint_total | 18 |
| fingerprint_found | 13 |
| generated | "2026-04-03T15:21:19" |
| generator | superclaude-anti-instinct-audit |

### 2.9 wiring-verification.md

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
| whitelist_entries_applied | 0 |

---

## 3. extraction.md Deep Analysis

### 3.1 Section Headers (`## `)

Total `## ` headers: **8**

1. Functional Requirements
2. Non-Functional Requirements
3. Complexity Assessment
4. Architectural Constraints
5. Risk Inventory
6. Dependency Inventory
7. Success Criteria
8. Open Questions

### 3.2 Persona References

**Total persona mentions**: 10

| Persona | Count | Locations (line numbers) |
|---------|-------|--------------------------|
| Alex | 5 | 32, 48, 79, 95, 188 |
| Jordan | 2 | 189, 247 |
| Sam | 3 | 64, 190, 246 |

*Note: Line 188 contains "Alex" once. Previous count of 7 was a triple-count error.*

Context: Personas appear in PRD Trace fields on each FR, in the Architectural Constraints section (lines 188-190), and in Open Questions (lines 246-247).

### 3.3 Compliance References (GDPR / SOC2)

**Total compliance mentions**: 10

| Term | Count | Key Locations |
|------|-------|---------------|
| GDPR | 6 | NFR-AUTH.4 (line 125), NFR-AUTH.6 (line 143), complexity table (165), narrative (170) |
| SOC2 | 4 | NFR-AUTH.5 (line 134), complexity table (165), risk inventory (203), open questions (245) |

Three NFRs are explicitly marked as "PRD-derived":
- NFR-AUTH.4: GDPR Registration Consent
- NFR-AUTH.5: SOC2 Audit Logging
- NFR-AUTH.6: GDPR Data Minimization

### 3.4 TDD Component Names (Spec-Path Expectation: ABSENT)

**FINDING: TDD component names ARE PRESENT in extraction.md.**

| Component | Occurrences | Context |
|-----------|-------------|---------|
| PasswordHasher | 4 | Dependencies fields (lines 30, 46, 93), Architectural Constraints (line 181) |
| TokenManager | 5 | Dependencies fields (lines 30, 62, 77, 93), Architectural Constraints (line 181) |
| JwtService | 3 | Dependencies field (line 62), Architectural Constraints (line 181), Dependency Inventory (lines 212, 216) |
| AuthService | 1 | Architectural Constraints (line 181) |
| RefreshToken | 1 | Dependencies field (line 62) |

**Assessment**: These component names appear because the extraction was run against a spec that already contained TDD-level implementation detail (file names like `jwt-service.ts`, `password-hasher.ts`, component architecture `AuthService -> TokenManager -> JwtService`). The extraction faithfully preserved these from the source spec. This is expected for a spec-path run where the input spec contains implementation details.

---

## 4. roadmap.md Deep Analysis

### 4.1 Milestones

**Total milestones**: 4

| # | Milestone Name | Line | Phase |
|---|---------------|------|-------|
| 1 | Foundation Ready | 96 | Phase 1: Foundation & Infrastructure (Weeks 1-2) |
| 2 | Core Auth Complete | 207 | Phase 2: Core Authentication (Weeks 3-5) |
| 3 | Full Feature Complete | 285 | Phase 3: Profile & Password Reset (Weeks 5-7) |
| 4 | Production Launch | 381 | Phase 4: Hardening, Compliance & Launch (Weeks 7-9) |

### 4.2 Persona References

**Total persona mentions**: 17

| Persona | Key Appearances |
|---------|----------------|
| Alex | Login error messaging (127), registration time (140), session persistence (157), logout story (164), profile (238) |
| Jordan | Audit log querying (376), admin scope deferral (529, 543, 557) |
| Sam | Programmatic refresh (156), headless auth OQ (297), API keys deferral (544, 558) |

Persona coverage summary table exists at lines 556-558:
- Alex: Full coverage
- Jordan: Partial (admin UI deferred, audit API conditional)
- Sam: Partial (service accounts deferred)

### 4.3 Compliance References

**Total compliance mentions**: 25

| Term | Count |
|------|-------|
| GDPR | ~8 references (consent, data minimization, right to erasure) |
| SOC2 | ~10 references (audit logging, Q3 deadline, Type II) |
| NIST | ~7 references (SP 800-63B, password policy) |

Compliance validation is concentrated in Phase 4 with a dedicated section. SOC2 audit logging is elevated to Phase 1 as a hard requirement.

### 4.4 Business Metrics

**Total business metric references**: 11

| Metric | Target | Source |
|--------|--------|--------|
| Registration conversion rate | > 60% | PRD S19 (lines 141, 356, 387, 450) |
| Average session duration | > 30 minutes | PRD (line 451) |
| Revenue impact | $2.4M projected annual | Executive summary (line 16) |
| Engagement lift | 40% | Not in merged roadmap (Haiku variant only) |
| Log retention | 12 months | SOC2 requirement (lines 80, 328) |

---

## 5. Variant Roadmap Comparison (Quick Stats)

| Metric | Opus (Variant A) | Haiku (Variant B) |
|--------|-----------------|-------------------|
| Lines | 377 | 659 |
| Phases | 4 | 2 |
| Milestones | 4 | 2 |
| Timeline | ~10 weeks | ~6 weeks |
| Frontmatter fields | 9 | 3 |
| Base selection score | 81 | 76 |

---

## 6. anti-instinct-audit.md Key Metrics

| Metric | Value |
|--------|-------|
| **fingerprint_coverage** | **0.72** (13 of 18 found) |
| **undischarged_obligations** | **2** |
| **uncovered_contracts** | **3** (IC-004, IC-005, IC-006 -- all middleware_chain) |

### Missing Fingerprints (5)
- JIRA
- PASETO
- CSRF
- UUID
- REST

### Undischarged Obligations (2)
1. Line 40: `skeleton` in Phase 1 (no discharge found)
2. Line 192: `hardcoded` in Phase 2 (static reference, not discharged)

### Uncovered Contracts (3)
All relate to `middleware_chain` integration:
- IC-004: `src/middleware/auth-middleware.ts` Bearer token extraction
- IC-005: auth-middleware.ts (line 165)
- IC-006: auth-middleware.ts depends on token-manager (line 212)

### Pipeline Status
The anti-instinct step has status **FAIL** in `.roadmap-state.json` (fingerprint_coverage 0.72 < threshold).

---

## 7. wiring-verification.md Summary

- **Status**: PASS (0 blocking findings)
- **Total findings**: 7 (all major, 0 critical)
- **All 7 findings**: Orphan modules in `cli.cli_portify.steps.*` -- these are SuperClaude framework modules, **not** related to the auth roadmap content
- **Scan duration**: 0.54s against `src/superclaude` (164 files analyzed)

*Note*: The wiring verification scanned the SuperClaude codebase itself, not the roadmap content. Its findings are framework-internal orphan modules unrelated to the auth service roadmap.

---

## 8. Pipeline State (.roadmap-state.json)

| Step | Status | Duration |
|------|--------|----------|
| extract | PASS | 96.4s |
| generate-opus-architect | PASS | 144.9s |
| generate-haiku-architect | PASS | 189.2s |
| diff | PASS | 81.5s |
| debate | PASS | 110.7s |
| score | PASS | 79.5s |
| merge | PASS | 391.4s |
| anti-instinct | **FAIL** | 0.03s |
| wiring-verification | PASS | 0.54s |

**Total pipeline duration**: ~16 minutes 9 seconds (extract start to wiring-verification end)

**Input files**:
- spec: `test-spec-user-auth.md`
- prd: `test-prd-user-auth.md`
- tdd: null (no TDD input)

**Agents**: opus/architect + haiku/architect (standard depth)

---

## 9. Tasklist Status

**Tasklist not yet generated.** No `*tasklist*` files exist in this directory. The pipeline state confirms no tasklist step was executed.

---

## 10. Key Observations for Quality Comparison

1. **Run B is a spec+PRD path** (no TDD input). The `tdd_file` field in `.roadmap-state.json` is `null`.
2. **TDD component names (AuthService, TokenManager, etc.) appear in extraction.md** because the source spec contained implementation-level detail, not because a TDD was provided.
3. **Anti-instinct audit failed** with 0.72 fingerprint coverage (5 missing fingerprints, 2 undischarged obligations, 3 uncovered middleware contracts).
4. **Adversarial pipeline completed fully**: diff -> debate (2 rounds, 0.62 convergence) -> base selection (Opus A:81, Haiku B:76) -> merge.
5. **Merged roadmap (roadmap.md)** has 4 phases, 4 milestones, 558 lines, and includes both `spec_source` and `prd_source` in frontmatter.
6. **All 7 .err files are empty** (0 bytes) -- no stderr output from any pipeline step.

---

## Summary

Run B (test2-spec-prd-v2) is a spec+PRD pipeline run (no TDD input) producing 9 .md files, 7 .err files (all empty), and a .roadmap-state.json. The pipeline completed with adversarial debate (convergence 0.62, Opus A:81 vs Haiku B:76), producing a merged roadmap of 558 lines with 4 phases and 4 milestones. No tasklist was generated. Key differentiators from Run A: PRD-derived personas (Alex=5, Jordan=2, Sam=3), GDPR/SOC2 compliance references (10 in extraction, 25 in roadmap), and business metrics (revenue $2.4M, conversion >60%). Anti-instinct audit failed (0.72 fingerprint coverage, 2 undischarged obligations, 3 uncovered contracts).
