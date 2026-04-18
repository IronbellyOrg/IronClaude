# Roadmap Pipeline Comparison: test4-spec vs test6-spec

> **Date**: 2026-04-15
> **Spec source**: `.dev/test-fixtures/test-spec-user-auth.md`
> **Old output**: `.dev/test-fixtures/results/test4-spec/roadmap.md` (pre-template, adversarial merge)
> **New output**: `.dev/test-fixtures/results/test6-spec/roadmap.md` (template-driven, incremental write)
> **Template**: `src/superclaude/examples/roadmap_template.md`

---

## 1. Structural Summary

| Dimension | test4 (old) | test6 (new) | Delta |
|---|---|---|---|
| Phases | 6 | 4 | -2 |
| Task rows | 101 | 58 | -43 (43% reduction) |
| Timeline | ~7.5 weeks | 17-21 days | ~50% shorter |
| Risks | 6 | 6 | Same |
| Open questions | 8 (OQ-1..8) | 6 (OQ-1..6) | -2 |
| Success criteria | 14 (SC-1..14) | 22 (SC-1..22) | +8 |
| Top-level sections | 7 | 7 | Same (matches template) |
| Frontmatter fields | 14 | 16 | +2 (`complexity_class`, `risk_count`, `open_questions`) |

### Phase Structure Comparison

| test4 Phases | test6 Phases |
|---|---|
| Phase 0: Foundation, Architecture & Contracts | Phase 1: Security and Data Foundation |
| Phase 1: Registration & Login | Phase 2: Core Authentication Flows |
| Phase 2: Token Lifecycle & Profile | Phase 3: API Exposure and Verification |
| Checkpoint B (advisory) | — |
| Phase 3: Password Reset | — |
| Phase 4: NFR & Hardening | Phase 4: Hardening, Operations, and Release |
| Phase 5: Validation, OQ Closure & Deploy | — |

test6 consolidates registration, login, token refresh, profile, and password reset into two phases (2 and 3) instead of three separate phases (1, 2, 3) in test4. The validation/deploy phase is folded into Phase 4.

---

## 2. Template Conformance

### Where test6 Conforms Well

- **Frontmatter**: all template fields present; adds `complexity_class`, `risk_count`, `open_questions` for machine-parseable metadata
- **8-column task table**: `# | ID | Task | Comp | Deps | AC | Eff | Pri` used consistently in all 4 phases
- **Integration Points per phase**: present with the template's `Artifact | Type | Wired | Phase | Consumed By` schema
- **All required sections present**: Executive Summary, Risk Assessment, Resource Requirements, Success Criteria, Timeline, Open Questions
- **AC format**: terse semicolon-separated conditions as the template requires

### Minor Template Deviations in test6

| Template Specifies | test6 Uses |
|---|---|
| `**Objective:** ... \| **Duration:** ... \| **Entry:** ... \| **Exit:** ...` | `**Phase N** \| milestone: ... \| duration: ... \| exit criteria: ...` |
| Entry criteria per phase | Omitted |
| Phase numbering starts at template placeholder | Starts at Phase 1 (reasonable) |

### test4 Template Non-Conformance

test4 predates the template and deviates in several ways:
- Phase header format uses paragraph-style objectives, not the template's inline format
- Integration Points are top-level prose sections (Section 2) rather than per-phase tables
- Frontmatter lacks `complexity_class`, `risk_count`, `open_questions`
- Has non-template sections: Merge Provenance, Checkpoint B, Release Gate Criteria, Validation Strategy

---

## 3. Spec Fidelity — Functional Requirements

The spec defines 5 functional requirements with 19 total acceptance criteria. Both roadmaps cover all 19.

### FR-AUTH.1: User Login (4 ACs)

| Spec AC | test4 | test6 |
|---|---|---|
| Valid credentials → 200 + access(15m) + refresh(7d) | FR-AUTH.1a (Phase 1, row 8) | Row 24: `valid→200+access15m+refresh7d` |
| Invalid credentials → 401, no enumeration | FR-AUTH.1b (Phase 1, row 9) | Row 24: `invalid→401+no-enum` |
| Locked account → 403 | FR-AUTH.1c (Phase 1, row 10) | Row 24: `locked→403` |
| Rate limit 5/min/IP | FR-AUTH.1d (Phase 1, row 11) | Row 24: `limit:5/min/IP` |

**Both: complete.** test4 uses 5 rows (scaffold + 4 sub-tasks). test6 uses 1 row with compound AC.

### FR-AUTH.2: User Registration (4 ACs)

| Spec AC | test4 | test6 |
|---|---|---|
| Valid data → 201 + profile | FR-AUTH.2a (Phase 1, row 2) | Row 22: `valid→201+profile` |
| Duplicate email → 409 | FR-AUTH.2b (Phase 1, row 3) | Row 22: `dup-email→409` |
| Password policy (8+, upper, lower, digit) | FR-AUTH.2c (Phase 1, row 4) | Row 22: `pwd:min8+upper+lower+digit` |
| Email format validation | FR-AUTH.2d (Phase 1, row 5) | Row 22: `email:format-valid` |

**Both: complete.**

### FR-AUTH.3: Token Refresh (4 ACs)

| Spec AC | test4 | test6 |
|---|---|---|
| Valid refresh → new pair, rotate | FR-AUTH.3a (Phase 2, row 2) | Row 26: `valid-refresh→200+rotated pair` |
| Expired refresh → 401 | FR-AUTH.3b (Phase 2, row 3) | Row 26: `expired→401` |
| Replay detection → revoke all | FR-AUTH.3c (Phase 2, row 4) | Row 26: `replay→global revoke` |
| Hash storage in DB | FR-AUTH.3d (Phase 2, row 5) | Row 26: `token-hash:persisted` |

**Both: complete.**

### FR-AUTH.4: Profile Retrieval (3 ACs)

| Spec AC | test4 | test6 |
|---|---|---|
| Valid bearer → 200 + profile fields | FR-AUTH.4a (Phase 2, row 8) | Row 35: `valid bearer→200+id+email+display_name+created_at` |
| Expired/invalid token → 401 | FR-AUTH.4b (Phase 2, row 9) | Row 35: `invalid/expired→401` |
| No sensitive fields in response | FR-AUTH.4c (Phase 2, row 10) | Row 35: `sensitive:excluded(password_hash,token_hash)` |

**Both: complete.**

### FR-AUTH.5: Password Reset (4 ACs)

| Spec AC | test4 | test6 |
|---|---|---|
| Reset token (1h TTL) + email | FR-AUTH.5a (Phase 3, row 3) | Row 28: `registered-email→reset1h+email` |
| Valid token → password changed, token invalidated | FR-AUTH.5b (Phase 3, row 4) | Row 28: `valid token→pwd changed+token invalidated` |
| Expired/invalid → 400 | FR-AUTH.5c (Phase 3, row 5) | Row 28: `bad token→400` |
| All sessions revoked on reset | FR-AUTH.5d (Phase 3, row 6) | Row 28: `reset→revoke all sessions` |

**Both: complete.**

### Functional Requirements Verdict

**Zero spec ACs lost in either roadmap.** test4 explodes each FR into 4-5 rows (scaffold + labeled sub-IDs). test6 compresses to 1 row with semicolon-separated compound ACs. Content is identical; granularity differs.

---

## 4. Spec Fidelity — Data Models

The spec defines exact field names and types in Section 4.5. This is where the roadmaps diverge meaningfully.

### UserRecord

| Spec Field | test4 (DM-001) | test6 (DM-001) | Faithful? |
|---|---|---|---|
| `id: string` (UUID v4) | `id (UUID PK)` | `id:uuid-v4` | Both |
| `email: string` (unique, indexed) | `email (unique index)` | `email:string+unique+idx` | Both |
| `display_name: string` | `display_name` | `display_name:string` | Both |
| `password_hash: string` (bcrypt) | `password_hash` | `password_hash:bcrypt` | Both |
| `is_locked: boolean` | **`locked_at (nullable)`** | `is_locked:boolean` | **test6 wins** |
| `created_at: Date` | `created_at` | `created_at:Date` | Both |
| `updated_at: Date` | **Omitted** | `updated_at:Date` | **test6 wins** |

### RefreshTokenRecord

| Spec Field | test4 (DM-002) | test6 (DM-002) | Faithful? |
|---|---|---|---|
| `id: string` (UUID v4) | `id (UUID PK)` | `id:uuid-v4` | Both |
| `user_id: string` (FK) | `user_id (FK → users, indexed)` | `user_id:FK->UserRecord.id` | Both |
| `token_hash: string` (SHA-256) | `token_hash (SHA-256)` | `token_hash:SHA-256` | Both |
| `expires_at: Date` | `expires_at` | `expires_at:Date` | Both |
| `revoked: boolean` | **`revoked_at (nullable)`** | `revoked:boolean` | **test6 wins** |
| `created_at: Date` | `created_at` | `created_at:Date` | Both |

### AuthTokenPair

| Spec Field | test4 | test6 (DM-003) | Faithful? |
|---|---|---|---|
| `access_token: string` (JWT, 15min) | No explicit task | `access_token:JWT-RS256-15m-TTL` | **test6 wins** |
| `refresh_token: string` (opaque, 7d) | No explicit task | `refresh_token:opaque-7d-TTL` | **test6 wins** |

### Data Model Verdict

**test6 reproduces spec data models exactly.** test4 silently altered two field semantics:
- `is_locked: boolean` → `locked_at: nullable Date` (different semantics: boolean flag vs timestamp)
- `revoked: boolean` → `revoked_at: nullable Date` (same pattern)

These are arguably better designs, but they deviate from the spec without flagging the deviation.

---

## 5. Spec Fidelity — Architecture Components

Spec Section 4.1 defines 4 new files and 3 modified files.

### New Files (Spec Section 4.1)

| Spec Component | Path | test4 | test6 |
|---|---|---|---|
| AuthService | `src/auth/auth-service.ts` | Implicit via FR handlers | COMP-001 (explicit row) |
| TokenManager | `src/auth/token-manager.ts` | COMP-003 | COMP-002 (explicit row) |
| JwtService | `src/auth/jwt-service.ts` | COMP-002 | COMP-003 (explicit row) |
| PasswordHasher | `src/auth/password-hasher.ts` | COMP-001 | COMP-004 (explicit row) |

### Modified Files (Spec Section 4.2)

| Spec Component | Path | test4 | test6 |
|---|---|---|---|
| AuthMiddleware | `src/middleware/auth-middleware.ts` | COMP-004, COMP-005 | COMP-005 |
| Route registration | `src/routes/index.ts` | COMP-006 | COMP-006 |
| Migration | `src/database/migrations/003-auth-tables.ts` | MIG-001, MIG-002 | COMP-007, MIG-001..003 |

### Additional Components Derived from Spec

test6 extracts additional components that are implied but not explicitly listed in the spec:

| test6 Component | Spec Source | Traceable? |
|---|---|---|
| COMP-008 UserRepository | Spec: "User repository" dependency in FR-AUTH.1, FR-AUTH.2 | Yes |
| COMP-009 RefreshTokenRepository | Spec: "RefreshToken repository" in dependency graph | Yes |
| COMP-010 AuthRateLimiter | Spec: FR-AUTH.1 AC4 "rate-limit login attempts to 5 per minute per IP" | Yes |
| COMP-011 ResetEmailAdapter | Spec: FR-AUTH.5 dependency "Email service (external)" | Yes |
| COMP-012 SecretsProvider | Spec: Risk R-1 "store private key in secrets manager" | Yes |
| COMP-013 AuthConfig | Reasonable derivation (boot-time config validation) | Partial |
| COMP-014 AuthFeatureGate | Spec: Section 9 `AUTH_SERVICE_ENABLED` | Yes |
| COMP-015 AuthCookiePolicy | Spec: Decision table row 3 "refresh token in httpOnly cookie" | Yes |

### Architecture Verdict

test6 has more granular component decomposition with 15 COMP-IDs vs test4's 7. All test6 components are traceable to specific spec sections. test4 covers the same ground but with fewer explicit rows, relying on FR handler tasks to implicitly create components.

---

## 6. The "Lost" Items — Spec Provenance Audit

This section examines every item present in test4 but absent in test6, and determines whether it originated from the spec.

### Items NOT in the Spec (Invented by Adversarial Merge)

| Lost Item | test4 Location | Spec Evidence | Verdict |
|---|---|---|---|
| **Security interface contracts** (CONT-001, CONT-002) | Phase 0, rows 17-18 | Spec Section 5.1 only says "no CLI interface." No requirement for security-engineer-reviewed interface contracts. | **Invented.** Useful engineering practice but not spec-required. |
| **Sub-AC ID labeling** (FR-AUTH.1a/1b/1c/1d) | Phases 1-3 | Spec uses unlabeled bullet points for ACs, not indexed sub-IDs. | **Labeling scheme invented.** The AC content itself is spec-faithful in both. |
| **Test architecture tasks** (TEST-ARCH-001, TEST-ARCH-002) | Phase 0, rows 9-10 | Spec Section 8 defines specific tests. No "test strategy matrix" or "shared test fixture planning" meta-tasks. | **Invented.** |
| **OQ validation tasks** (OQ-1-VAL, OQ-3-VAL, OQ-7-VAL, OQ-8-VAL) | Phase 5, rows 16-19 | Spec Section 11 has open items. No requirement to validate decisions with measured evidence post-implementation. | **Invented.** |
| **Checkpoint B** (mid-implementation review) | Between Phases 2-3 | No review checkpoints anywhere in spec. | **Invented.** |
| **Named integration artifacts** (SecurityServiceContainer, AuthMiddlewareChain, AuthRouteRegistry) | Section 2 | Spec Section 4.4 shows dependency graph using file names, not DI container/chain abstractions. | **Invented.** |
| **Merge provenance section** | Section 1 | Meta-information about generator process. | **Pipeline metadata, not spec content.** |
| **Team resource allocation table** | Section 5 | No staffing or resource section in spec. | **Invented.** |
| **Validation strategy tiers** (4-tier framework) | Section 6 | Spec Section 8 has unit/integration/E2E. No 4-tier validation methodology. | **Invented.** Expands spec's test plan. |

### Items Partially Derived from Spec

| Lost Item | test4 Location | Spec Source | Verdict |
|---|---|---|---|
| **Release gate criteria** (7-condition go/no-go) | Section 6, bottom | Spec Section 9 mentions feature flag and rollback but not a formal gate. | **Mostly invented.** Seed from spec Section 9 but the gate formalism is added. |
| **OQ-7** (email interface contract) | Phase 0, row 4 | Spec: FR-AUTH.5 lists "Email service (external)" as a dependency. Not an open question. | **Reasonable derivation** promoted to OQ. |
| **OQ-8** (RSA key rotation procedure) | Phase 0, row 8 | Spec Risk R-1: "implement key rotation every 90 days." Not flagged as an open question. | **Reasonable derivation** promoted from risk mitigation to OQ. |

### Summary

**0 of 12 "lost" items were spec requirements.** All were invented by the adversarial merge process. Some (security contracts, release gate, OQ validation) represent genuinely valuable engineering practice, but they are generator additions, not spec obligations.

---

## 7. Open Items and Gap Analysis Mapping

The spec defines 2 open items (OI-1, OI-2) and 3 gap analysis items (GAP-1, GAP-2, GAP-3).

| Spec Source | Description | test4 OQ | test6 OQ |
|---|---|---|---|
| OI-1 | Sync vs async email dispatch | OQ-1 | OQ-1 |
| OI-2 | Max active refresh tokens per user | OQ-2 | OQ-2 |
| GAP-1 | Account lockout policy | OQ-4 | OQ-3 |
| GAP-2 | Audit logging scope | OQ-6 | OQ-4 |
| GAP-3 | Token revocation on user deletion | OQ-5 | OQ-5 |

### Additional OQs (Not in Spec)

| OQ | Roadmap | Source | Assessment |
|---|---|---|---|
| OQ-3 (latency conflict bcrypt vs p95) | test4 | Derived from comparing NFR-AUTH.1 vs NFR-AUTH.3 | Reasonable, but the conflict is inherent in the spec and could be resolved without a formal OQ |
| OQ-7 (email interface contract) | test4 only | Derived from FR-AUTH.5 dependency | Reasonable derivation |
| OQ-8 (RSA key rotation procedure) | test4 only | Derived from Risk R-1 mitigation | Reasonable derivation |
| OQ-6 (confirm REST paths) | test6 only | Not in spec; spec Section 3 defines endpoint paths implicitly via FR descriptions | Reasonable; spec doesn't explicitly freeze paths |

### Open Items Verdict

Both roadmaps cover all 5 spec-originated items. test4 adds 3 extra invented OQs (total 8). test6 adds 1 (total 6). test6 is tighter and closer to spec scope.

---

## 8. NFR and Risk Coverage

### Non-Functional Requirements

| Spec NFR | test4 | test6 | Both Complete? |
|---|---|---|---|
| NFR-AUTH.1 (p95 < 200ms) | NFR-AUTH.1 + OQ-3 + R-4 + OQ-3-VAL | NFR-AUTH.1 (row 43) + TEST-010 (k6 load test) | Yes |
| NFR-AUTH.2 (99.9% uptime) | NFR-AUTH.2 + OPS-003 | NFR-AUTH.2 (row 44) + OPS-002 (health checks) | Yes |
| NFR-AUTH.3 (bcrypt cost 12) | NFR-AUTH.3 + R-3 + TEST-011 | NFR-AUTH.3 (row 45) + TEST-001 (crypto tests) | Yes |

### Risk Assessment

Spec defines 3 risks. Both roadmaps expand to 6.

| Spec Risk | Description | test4 | test6 |
|---|---|---|---|
| R-1 | JWT key compromise | R-1 + OPS-002 + OQ-8 + OQ-8-VAL | R-1 + OPS-004 + OPS-012 |
| R-2 | Refresh token replay | R-2 + FR-AUTH.3c | R-2 + FR-AUTH.3 compound AC |
| R-3 | bcrypt cost obsolescence | R-3 | R-3 |
| — | Email service unavailability | R-5 (invented) | R-4 (invented) |
| — | Distributed brute force / no lockout | R-6 (invented, from GAP-1) | R-5 (invented, from GAP-1) |
| — | Feature flag rollback untested | — | R-6 (invented, from Section 9) |
| — | Latency conflict (bcrypt vs p95) | R-4 (invented, from NFR tension) | — |

Both fully cover spec risks. Additional risks are reasonable derivations.

---

## 9. Deployment and Rollout Coverage

Spec Section 9 specifies: feature flag (`AUTH_SERVICE_ENABLED`), down-migrations, additive/non-breaking changes.

| Spec Requirement | test4 | test6 |
|---|---|---|
| `AUTH_SERVICE_ENABLED` flag | OPS-009 (Phase 0, early) | COMP-014 AuthFeatureGate (Phase 3) |
| Down-migration scripts | MIG-002 | MIG-002 + MIG-003 (idempotent down) |
| Staged/safe rollout | OPS-006, OPS-007, OPS-008 (3 tasks) | OPS-008 runbook, OPS-009 canary 10%, OPS-010 SC validation, OPS-011 full rollout (4 tasks) |
| Rollback plan | SC-13 (flag rollback verification) | Implicit via feature gate + canary |

### Deployment Verdict

test6 has more granular deployment sequencing (4 rollout tasks with explicit canary percentage and validation). test4 introduces the feature flag earlier (Phase 0 vs Phase 3), which is an architectural choice not required by the spec.

---

## 10. Test Plan Coverage

Spec Section 8 defines 5 unit tests, 3 integration tests, and 1 E2E scenario.

| Spec Test | test4 | test6 |
|---|---|---|
| PasswordHasher unit test | TEST-001 | TEST-001 (crypto primitives) |
| JwtService unit test | TEST-002 | TEST-001 (crypto primitives) |
| TokenManager unit test | Implicit in TEST-005 | TEST-002 (auth service units) |
| AuthService.login unit test | Implicit in TEST-004 | TEST-002 (auth service units) |
| AuthService.register unit test | Implicit in TEST-003 | TEST-002 (auth service units) |
| Login integration test | TEST-004 | TEST-006 |
| Token refresh integration test | TEST-005 | TEST-008 |
| Registration → login integration | TEST-003 | TEST-007 |
| Full lifecycle E2E | TEST-012 | TEST-004 |

Both cover all spec tests. test4 has 12 test tasks; test6 has 10. The difference is test4's additional security scan (TEST-007), enumeration timing test (TEST-009), rate limit load test (TEST-010), and bcrypt benchmark (TEST-011) — none of which are in the spec test plan.

---

## 11. Success Criteria Comparison

| Dimension | test4 | test6 |
|---|---|---|
| Total SCs | 14 | 22 |
| Spec-traceable SCs | 14 (all map to FRs/NFRs) | 22 (all map to FRs/NFRs, more granular) |
| SC per FR-AUTH | 1 per FR (SC-1..5) | Multiple per FR (e.g., SC-1 through SC-4 for login alone) |

test6 has more granular success criteria, with individual SCs for each AC within a functional requirement. test4 bundles all ACs for a given FR into a single SC.

---

## 12. Spec Loyalty Ranking

### Scoring by Dimension

| Dimension | test4 | test6 | Winner |
|---|---|---|---|
| FR AC coverage | 19/19 | 19/19 | Tie |
| Data model fidelity | 5/7 fields exact | 7/7 fields exact | **test6** |
| Component traceability | 7 COMP-IDs, all traceable | 15 COMP-IDs, all traceable | **test6** |
| Open item coverage | 5/5 spec items + 3 invented | 5/5 spec items + 1 invented | **test6** (tighter scope) |
| NFR coverage | 3/3 | 3/3 | Tie |
| Risk coverage | 3/3 spec + 3 invented | 3/3 spec + 3 invented | Tie |
| Test plan coverage | 9/9 spec tests + 3 extra | 9/9 spec tests + 1 extra | **test6** (tighter scope) |
| Deployment coverage | 3 tasks | 4 tasks (more granular) | **test6** |
| Invented content volume | High (12 non-spec items) | Low (1 non-spec item) | **test6** |
| Template conformance | N/A (predates template) | Strong | **test6** |

### Overall Verdict

**test6 is more faithful to the spec.** It covers every spec requirement with zero losses while staying within spec scope. test4 covers the same spec requirements but inflates the roadmap with 43 additional task rows, most of which represent invented engineering practices (security contracts, test strategy meta-tasks, OQ validation, checkpoints) that, while valuable, are not spec-derived.

---

## 13. Template Effectiveness Assessment

### What the Template Does Well

1. **Enforces structural consistency** — all required sections present in correct order
2. **Standardizes frontmatter** — machine-parseable metadata enables automated validation
3. **Constrains task tables to 8 columns** — prevents column drift and inconsistent schemas
4. **Requires integration points per phase** — makes wiring decisions explicit
5. **Forces terse AC format** — semicolon-separated conditions eliminate prose bloat
6. **Keeps the generator focused on spec content** — the template's structure naturally discourages invented meta-sections

### Template Gaps That Could Be Addressed

| Gap | Effect | Recommendation |
|---|---|---|
| No "Release Readiness" or gate section | Generator has no signal to produce go/no-go criteria | Add optional section between Success Criteria and Timeline |
| No guidance on sub-AC decomposition | Template says "Every extraction ID = one row. Do NOT merge IDs" but doesn't prevent compound ACs within a single row | Clarify whether FR sub-ACs should be separate rows or compound conditions |
| No conditional merge provenance | When `adversarial: true`, there's no section for documenting variant contributions | Add optional provenance block in Executive Summary when adversarial |
| No entry criteria in phase headers | Template specifies `Entry:` but the generator omitted it | Reinforce entry criteria as required, not optional |
| No security contracts section | For security-sensitive projects, interface contracts are valuable even if not spec-required | Add optional "Contracts" section gated by complexity or domain |

### Template ROI

The template achieved a 43% reduction in task rows with zero spec content loss. The compression came entirely from eliminating invented meta-tasks and reducing per-FR row inflation. This validates the template as an effective constraint on generator verbosity.

---

## 14. Recommendations

### For the Template

1. **Add an optional "Release Gate" section** after Success Criteria. While not spec-originated, this is the one test4 invention with universal value across all roadmaps.
2. **Reinforce entry criteria** in the phase header format — make it clear this is required, not optional.
3. **Add adversarial provenance guidance** — when `adversarial: true`, document what came from which variant.

### For the Pipeline

1. **Data model fidelity check** — the pipeline should flag when generated field names/types deviate from spec definitions. test4's `locked_at`/`revoked_at` substitutions were silent.
2. **Scope control** — the template effectively prevented test6 from inventing meta-tasks. This behavior should be preserved.
3. **OQ derivation audit** — both roadmaps promote spec gap analysis items to open questions, which is correct. But test4's additional OQ-7/OQ-8 show that without the template, the generator invents open questions from risk mitigations.

### For Future Comparisons

1. The spec should be the primary fidelity benchmark, not the previous roadmap output.
2. "Lost" items should always be audited against the spec before being classified as regressions.
3. Invented content is not inherently bad — security contracts and release gates are valuable — but it should be clearly marked as generator additions, not spec requirements.

---

## Appendix: Traceability Matrix

### Spec → test6 Traceability

| Spec Section | Spec Element | test6 Coverage |
|---|---|---|
| 3 / FR-AUTH.1 | Login (4 ACs) | Row 24 (compound AC) + TEST-006 |
| 3 / FR-AUTH.2 | Registration (4 ACs) | Row 22 (compound AC) + TEST-007 |
| 3 / FR-AUTH.3 | Token Refresh (4 ACs) | Row 26 (compound AC) + TEST-008 |
| 3 / FR-AUTH.4 | Profile (3 ACs) | Row 35 (compound AC) + TEST-003 |
| 3 / FR-AUTH.5 | Password Reset (4 ACs) | Row 28 (compound AC) + TEST-002 |
| 4.1 | auth-service.ts | COMP-001 |
| 4.1 | token-manager.ts | COMP-002 |
| 4.1 | jwt-service.ts | COMP-003 |
| 4.1 | password-hasher.ts | COMP-004 |
| 4.2 | auth-middleware.ts | COMP-005 |
| 4.2 | routes/index.ts | COMP-006 |
| 4.2 | migrations/003-auth-tables.ts | COMP-007 |
| 4.5 | UserRecord | DM-001 (exact match) |
| 4.5 | RefreshTokenRecord | DM-002 (exact match) |
| 4.5 | AuthTokenPair | DM-003 (exact match) |
| 6 | NFR-AUTH.1 (latency) | Row 43 + TEST-010 |
| 6 | NFR-AUTH.2 (uptime) | Row 44 + OPS-002 |
| 6 | NFR-AUTH.3 (bcrypt) | Row 45 + TEST-001 |
| 7 | Risk R-1 (key compromise) | R-1 + OPS-004 + OPS-012 |
| 7 | Risk R-2 (replay) | R-2 |
| 7 | Risk R-3 (bcrypt obsolescence) | R-3 |
| 8.1 | 5 unit tests | TEST-001, TEST-002 |
| 8.2 | 3 integration tests | TEST-003, TEST-006, TEST-007, TEST-008 |
| 8.3 | E2E lifecycle | TEST-004 |
| 9 | Feature flag | COMP-014 |
| 9 | Down-migration | MIG-002, MIG-003 |
| 11 / OI-1 | Sync vs async email | OQ-1 |
| 11 / OI-2 | Max refresh tokens | OQ-2 |
| 12 / GAP-1 | Account lockout | OQ-3 |
| 12 / GAP-2 | Audit logging | OQ-4 |
| 12 / GAP-3 | Revocation on deletion | OQ-5 |
