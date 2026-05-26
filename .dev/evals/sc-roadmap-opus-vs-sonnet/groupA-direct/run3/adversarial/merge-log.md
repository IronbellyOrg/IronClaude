# Merge Log: V1 (opus) Base + V2 (sonnet) Strengths + Invariant Remediations

## Metadata

- **Base variant**: V1 (opus-default) — `variant-1-opus-default.md` (618 lines)
- **Non-base source**: V2 (sonnet-default) — `variant-2-sonnet-default.md` (723 lines)
- **Refactor plan**: `refactor-plan.md` (16 RCs)
- **Executor**: `merge-executor` agent (sc:adversarial Step 5)
- **Merge timestamp**: 2026-05-22
- **Merged output**: `/config/workspace/IronClaude/.dev/eval-roadmap/groupA-direct/run3/roadmap.md`
- **Changes planned**: 16
- **Changes applied**: 16
- **Changes partial**: 0
- **Changes skipped**: 0
- **Changes failed**: 0
- **Overall status**: SUCCESS

---

## Changes Applied

Each RC entry below references the user-prompt's authoritative RC numbering for this merge step. Cross-references to refactor-plan.md RC numbers (where they differ) are noted in the rationale.

---

### RC-001 — Add CSRF protection as dedicated deliverable

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL)
- **Target**: M6 (2FA, Rate Limiting, CSRF & Audit Logging)
- **Integration**: add-new (D-M6.6)
- **Before**: V1 relied on `SameSite=Strict` alone (D-M2.6 security headers); no dedicated CSRF deliverable.
- **After**: New deliverable D-M6.6 (CSRF double-submit cookie protection) with `__Host-csrf-token` cookie + `X-CSRF-Token` header, constant-time comparison, GET/HEAD/OPTIONS exempt. Layered with SameSite=Strict for defense-in-depth. M6 title updated to include "CSRF". Traceability added under FR cross-cutting and NFR-003 (OWASP A05).
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-001 adds D-M6.6 CSRF double-submit cookie -->`
- **Validation**: D-M6.6 referenced from D-M8.2 (security scan A05 mapping), Launch Readiness Gate, and Risk R-001 mitigation. New exit criterion added to M6.

---

### RC-002 — Add password history enforcement deliverable

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL)
- **Target**: M2 (Core Auth)
- **Integration**: add-new (D-M2.7)
- **Before**: V1 enforced zxcvbn + HIBP at registration but had no password-history check (OWASP ASVS L2 V2.1.10 gap).
- **After**: New deliverable D-M2.7 (`password_history` table storing last 5 Argon2id hashes; registration + password-change endpoints check against history; eviction policy documented). Wired into D-M3.4 (password reset) and D-M4.3 (change password). FR-001 traceability extended.
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-002 adds D-M2.7 password history (last 5) -->`
- **Validation**: D-M2.7 referenced from D-M3.4 password reset flow and D-M4.3 change-password endpoint. New M2 exit criterion. R-002 mitigation extended.

---

### RC-003 — Remediate INV-002: OAuth null-email handling

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL)
- **Target**: M1 (schema constraint) + M5 (D-M5.4 callback logic)
- **Integration**: restructure
- **Before**: V1 schema `email CITEXT UNIQUE NOT NULL`; D-M5.4 (identity linking) did not handle null-email case from GitHub. Crash risk on auto-provisioning.
- **After**: D-M1.1 schema updated to `email CITEXT nullable per RC-003`. D-M5.4 restructured to generate synthetic placeholder `{provider}_{provider_user_id}@oauth.placeholder.invalid` with `email_status='synthetic_pending'` and `email_verified_at=NULL`; subsequent login prompts for real email; upgrade path emits `oauth.real_email_upgraded` audit event. New event types added to D-M5.6.
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-003 (null-email handling for INV-002) restructures D-M5.4 -->`
- **Validation**: GitHub null-email E2E test added to M5 exit criteria; D-M8.4 OAuth E2E re-verification explicitly includes synthetic-placeholder path. Launch Readiness Gate OAuth2 item references RC-003.

---

### RC-004 — Remediate INV-005: Per-device refresh token families

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL, HIGH-risk per refactor plan)
- **Target**: M3 D-M3.1
- **Integration**: restructure
- **Before**: V1 D-M3.1 used single-family refresh tokens — any reuse triggered full revocation, causing false-positive logout of legitimate concurrent devices.
- **After**: D-M3.1 restructured to per-device families: refresh-token row stores `(user_id, device_id, family_id, parent_token_hash)`. 30-second grace window for same-family concurrent refresh; out-of-window OR cross-family reuse → full family revocation. Schema index updated in D-M1.1 to `refresh_tokens(user_id, device_id, revoked_at)`.
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-004 restructures D-M3.1 to per-device refresh families with grace window per INV-005 -->`
- **Validation**: New M3 exit criteria for concurrent-device test, theft test (post-grace), and cross-device theft test. Launch Readiness Gate references RC-004. Token Storage row in Tech Decisions table calls out per-device families.

---

### RC-005 — Remediate INV-006: Argon2id parameters reconciled with NFR-001 budget

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL)
- **Target**: M1 D-M1.3 (parameters) + NFR-001 traceability (budget breakdown)
- **Integration**: restructure
- **Before**: V1 D-M1.3 specified m=64MB, t=3, p=4 producing ~250ms per hash — exceeds V1's own 200ms NFR-001 and 150ms M2 exit criterion.
- **After**: D-M1.3 retuned to **m=32768, t=2, p=4** targeting ~80ms p95. ADR-002 in D-M0.4 updated to reflect tuned parameters. Explicit NFR-001 budget breakdown added to traceability table: hash 80ms + DB 60ms + JWT 20ms + network 40ms = 200ms p95. M1 exit criterion updated to "Argon2id hash verification <100ms p95 on target hardware". Tech Decisions table row updated.
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-005 (Argon2id parameters tuned to m=32768/t=2/p=4) -->`
- **Validation**: M2 exit criterion now consistent (login p95 <150ms achievable since hash is ~80ms). NFR-001 row in Traceability Matrix carries explicit budget breakdown.

---

### RC-006 — Fix X-001: Rewrite Architectural Philosophy

- **Status**: APPLIED
- **Tier**: 3 (POLISH, but addresses documented contradiction)
- **Target**: Architectural Philosophy section
- **Integration**: restructure
- **Before**: V1 philosophy stated "2FA (FR-007) precedes OAuth because TOTP is a self-contained crypto primitive while OAuth has external-provider blast-radius risk" — directly contradicted by milestone ordering (M5=OAuth, M6=2FA).
- **After**: Rewrote critical-sequencing paragraph to: "Primary credential hardening (M1-M4: Argon2id, RS256, lockout, RBAC) precedes federation (M5: OAuth); 2FA at M6 layers step-up assurance on top of the hardened primary path." Removed the "2FA precedes OAuth" assertion entirely. Also removed the contradictory "soft sequencing" note about swapping 2FA and OAuth in the Sequencing section.
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-006: rewrite philosophy to remove "2FA precedes OAuth" claim and align with M1-M5 sequencing -->`
- **Validation**: Grep for body-text occurrences of "2FA precedes OAuth" → no matches (only appears in provenance comment acknowledging the fix). Grep for "soft sequencing" → no matches in body. X-001 contradiction resolved.

---

### RC-007 — Add person-week effort estimates per milestone

- **Status**: APPLIED
- **Tier**: 2 (HIGH-VALUE)
- **Target**: Milestone Summary Table (new column) + each M0-M9 header
- **Integration**: restructure (additive column)
- **Before**: V1 was team-agnostic with no resource quantification (W3 conceded by V1 advocate R2).
- **After**: Added "Effort (person-weeks)" column to Milestone Summary Table with values M0=3, M1=4, M2=6, M3=4, M4=4, M5=3, M6=6, M7=5, M8=4, M9=2. Total ~41 person-weeks called out. Each milestone section header now includes "Effort: N person-weeks".
- **Provenance tag**: Included in `<!-- Source: Base (original, modified) — RC-007: add "Effort" column for person-week estimates ... -->`
- **Validation**: Sum of effort column (41) referenced in Week-by-Week Parallelization Schedule narrative. Per-milestone headers all carry the effort.

---

### RC-008 — Remediate INV-008: Per-user DEK for cryptographic erasure

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL, HIGH-risk per refactor plan)
- **Target**: M1 D-M1.2 (architecture) + M4 D-M4.4 (erasure usage)
- **Integration**: restructure
- **Before**: V1 D-M1.2 described a single column-level DEK; D-M4.4 rotated this DEK for GDPR erasure, destroying ALL users' PII rather than per-user.
- **After**: D-M1.2 rewritten to describe per-user DEK architecture: new `user_encryption_keys` table stores wrapped DEK per user; wrapped by master KEK from KMS; PII columns encrypted with that user's DEK. D-M4.4 erasure path destroys only the requesting user's wrapped DEK. Tech Decisions table PII encryption row updated. Blast Radius Analysis includes per-user DEK isolation as the 7th invariant. KMS dependency added to Dependencies table. KMS request-quota added to Implicit Prerequisites. Meta-risks table includes KMS request volume mitigation.
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-008 (per-user DEK replaces global DEK) -->`
- **Validation**: D-M1.2 raw-page inspection test + per-user destruction isolation test added. D-M8.5 chaos drill includes per-user DEK rotation under load. Launch Readiness Gate PII encryption item references RC-008. INV-008 status: REMEDIATED.

---

### RC-009 — Remediate INV-014 (Merkle scope) + INV-009 (soft-delete grace) + INV-007 (lockout semantics)

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL)
- **Target**: M6 D-M6.4 (Merkle scope + retention grace) + D-M6.3 (lockout semantics) + M7 D-M7.5 (runbook scope)
- **Integration**: append + restructure
- **Before**: V1 had Merkle chain but no explicit scope statement (INV-014 noted gap on replication/OS-level tampering); 7-year retention with no grace-period safeguard for retroactive extension (INV-009); lockout threshold semantics ambiguous (INV-007).
- **After**: Added "Tamper Detection Scope" subsection to M6 explicitly stating what Merkle chain detects (DBA SQL mods, backup restore, row tampering) and what it doesn't (replication bypass, OS file tampering, app-layer suppression) with explicit routing of out-of-scope items to M7 runbooks. Added "Audit Retention Soft-Delete Grace" subsection: partitions enter detached-preserved state for 90 days before DROP. D-M6.3 lockout acceptance clarified: "Lockout triggers ON the Nth attempt (the Nth attempt itself is rejected)." D-M7.5 runbooks list extended with replication-bypass and OS-level file-tamper response.
- **Provenance tag**: `<!-- Source: Refactor plan RC-009 / invariant remediation INV-014 -->` and `<!-- Source: Refactor plan RC-009 / invariant remediation INV-009 -->`
- **Validation**: New M6 exit criteria for CSRF, lockout semantics, and retention soft-delete. Launch Readiness Gate lockout item references RC-009/INV-007. INV-007, INV-009, INV-014 all resolved.

---

### RC-010 — Remediate INV-015: Combined crypto erasure + pseudonymization

- **Status**: APPLIED
- **Tier**: 1 (CRITICAL, HIGH-risk per refactor plan)
- **Target**: M4 D-M4.4
- **Integration**: restructure
- **Before**: V1's D-M4.4 used DEK rotation + email pseudonymization but: (a) `audit_events.actor_user_id` retained linkability, (b) metadata JSONB could contain identifiable fragments, (c) OAuth provider_user_id mapping not destroyed.
- **After**: D-M4.4 restructured to combined GDPR erasure workflow with 4 explicit steps: (1) destroy that user's wrapped DEK (per RC-008), (2) pseudonymize `audit_events.actor_user_id` to `anonymized_<uuid>`, (3) scrub `audit_events.metadata` JSONB via field-allowlist filter, (4) destroy `oauth_identities.provider_user_id` mapping. Targets "effective erasure" per GDPR Recital 26. Annual GDPR audit (post-launch cadence) reviews against current guidance.
- **Provenance tag**: `<!-- Source: Base (original, modified) — RC-010 (combined erasure: per-user DEK destruction from RC-008 + audit pseudonymization scrub) -->`
- **Validation**: M4 exit criteria include end-to-end combined-erasure test verifying other users unaffected and audit chain integrity preserved. D-M8.3 GDPR verification + Launch Readiness Gate reference combined flow. INV-015 status: REMEDIATED.

---

### RC-011 — Add Technology Decisions & Rationale table

- **Status**: APPLIED
- **Tier**: 2 (HIGH-VALUE)
- **Target**: New H2 section after "Architectural Philosophy", before "Blast Radius Analysis"
- **Integration**: add-new
- **Before**: V1 embedded tech choices in ADR-004 and individual deliverables; no consolidated rationale table.
- **After**: New "Technology Decisions & Rationale" H2 section with 14-row table covering password hashing (Argon2id m=32768/t=2/p=4 per RC-005), pepper, JWT algorithm, refresh token storage + TTL, session store, PII encryption (per-user DEK per RC-008), rate limiting, 2FA, audit log storage + retention, email delivery, deployment, migrations. Format: Decision | Choice | Rationale | Alternative Considered.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet, default), "Technology Decisions & Rationale" section (lines ~692-706) — merged per RC-011 -->`
- **Validation**: Table format intact; all referenced parameter values consistent with deliverables (Argon2id, per-user DEK, 30-day refresh, 7-year retention).

---

### RC-012 — Add Blast Radius Analysis section

- **Status**: APPLIED
- **Tier**: 2 (HIGH-VALUE)
- **Target**: New H2 section after "Technology Decisions & Rationale", before "Milestone Summary Table"
- **Integration**: add-new
- **Before**: V1 had no Blast Radius Analysis section.
- **After**: New "Blast Radius Analysis" H2 with 7 invariants adapted from V2: token storage isolation, Redis as cache not authority, OAuth additivity, append-only audit (augmented with Merkle from RC-009), rate limiter isolation, KMS key separation, and (added) per-user DEK isolation per RC-008.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet, default), "Blast Radius Analysis" section (lines ~710-720) — merged per RC-012 -->`
- **Validation**: All 7 invariants reference deliverables that exist (D-M5.5 circuit breaker, D-M6.4 Merkle audit, D-M1.2 per-user DEK).

---

### RC-013 — Add Pre-Launch Verification Checklist (Launch Readiness Gate)

- **Status**: APPLIED
- **Tier**: 2 (HIGH-VALUE)
- **Target**: M9 (new "Launch Readiness Gate" subsection after D-M9.5)
- **Integration**: append
- **Before**: V1 had per-milestone exit criteria but no consolidated pre-launch gate.
- **After**: New "Launch Readiness Gate (RC-013 / Pre-Launch Verification Checklist)" subsection inside M9 with 16 checklist items: auth flow smoke test, OAuth E2E (incl. null-email path per RC-003), load test baseline, OWASP ZAP, GDPR export, combined GDPR erasure (per RC-010), monitoring dashboards, alerting, backup restore, rollback, rate limiting, lockout semantics (per RC-009), token theft detection (per RC-004), CSRF (per RC-001), CSP headers, PII encryption per-user DEK (per RC-008).
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet, default), "Pre-Launch Verification Checklist" (lines ~664-680) — merged per RC-013 -->`
- **Validation**: Every checklist item references an existing deliverable. New M9 exit criterion mandates all checked at 100% cutover.

---

### RC-014 — Add Post-Launch Operations (Ongoing Verification Cadence)

- **Status**: APPLIED
- **Tier**: 2 (HIGH-VALUE)
- **Target**: M9 (new "Post-Launch Operations" subsection after Launch Readiness Gate)
- **Integration**: append
- **Before**: V1 stopped at M9 production cutover with no post-launch verification cadence.
- **After**: New "Post-Launch Operations (RC-014 / Ongoing Verification Cadence)" subsection with table covering daily smoke, weekly OWASP ZAP, monthly load test + per-user DEK rotation drill (per RC-008), quarterly pen-test + backup restore + Merkle integrity verify (per RC-009), annual GDPR audit + JWT key rotation drill. Each row carries Owner and Failure Action columns.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet, default), "Ongoing Verification (Post-Launch)" (lines ~683-688) — merged per RC-014 -->`
- **Validation**: All cadence items reference existing deliverables (D-M6.4 Merkle, D-M7.6 backup, D-M9.2 key rotation).

---

### RC-015 — Add Week-by-Week Parallelization Schedule + M0 Definition-of-Done Checklist

- **Status**: APPLIED
- **Tier**: 2 (HIGH-VALUE) + Tier 3 (scope-creep mitigation per refactor plan)
- **Target**: Sequencing section (new subsection) + M0 (new "Definition of Done" subsection)
- **Integration**: add-new
- **Before**: V1 sequencing was narrative-only; M0 scope-creep meta-risk acknowledged but not structurally mitigated.
- **After**: New "Week-by-Week Parallelization Schedule (Illustrative 3-Person Team)" subsection in Sequencing & Critical Path with 14-week table assigning M0-M9 work across Backend A, Backend B, Frontend/DevOps. Explicit note that assignments are illustrative. New "M0 Definition of Done (Scope-Creep Guard)" subsection in M0 with 5 binary-pass items. Meta-Risks table updated to cite the DoD checklist.
- **Provenance tag**: `<!-- Source: Variant 2 (sonnet, default), "Parallelization Opportunities" week-by-week table (lines ~634-647) — merged per RC-015 -->` and `<!-- Source: Refactor plan RC-015 — added to mitigate V1's M0 scope-creep meta-risk -->`
- **Validation**: Schedule total weeks (14) consistent with effort sum (~41 pw) for 3-person team. M0 DoD items reference existing deliverables (ADRs in D-M0.4, Vault in D-M0.2, CI in D-M0.5).

---

### RC-016 — Adopt deliverable-table format per milestone

- **Status**: APPLIED
- **Tier**: 2 (HIGH-VALUE) — format adoption from V2
- **Target**: M0-M9 deliverable sections
- **Integration**: restructure (presentation-only)
- **Before**: V1 used narrative bullet points with sub-bullets for each deliverable.
- **After**: Every milestone (M0 through M9) now uses V2's table format: `| ID | Deliverable | Acceptance Criteria |`. All V1 deliverable IDs preserved (D-M0.1 through D-M9.5 + new D-M2.7 and D-M6.6); content preserved with minor flattening of sub-bullets into the acceptance-criteria cell to fit table presentation. Exit criteria sections retained as bullet lists below the deliverable tables.
- **Provenance tag**: Included per-milestone, e.g., `<!-- Source: Base (original, reformatted per RC-016 to deliverable-table format adopted from V2) -->`
- **Validation**: Grep over D-M* references in tables: all D-M IDs that existed in V1 still exist in merged doc (verified). No deliverable content lost; reformatted only.

---

## Post-Merge Validation

### Structural Integrity

- **Document starts with H1**: PASS — `# Roadmap: User Authentication System (Merged ...)` at line 7 (preceded only by HTML provenance comments).
- **Heading hierarchy (no H2 → H4 gaps)**: PASS — H2 sections (Architectural Philosophy, Technology Decisions & Rationale, Blast Radius Analysis, Milestone Summary Table, M0-M9, Traceability Matrix, Sequencing & Critical Path, Verification & Success Criteria Summary, Implicit Prerequisites Surfaced, Risks Created by This Roadmap) each contain H3 subsections only; no orphan H4. Spot-check via header grep confirms hierarchy.
- **Section ordering**: PASS — preserves V1's narrative arc (Philosophy → Tech/Blast Radius inserted → Summary → M0..M9 → Traceability → Sequencing → Verification → Prerequisites → Meta-Risks).
- **No orphaned subsections**: PASS — every H3 sits inside a defined H2.
- **Provenance annotations**: PASS — every H2 section carries a `<!-- Source: ... -->` HTML comment; modified subsections within milestones carry additional RC-specific provenance comments.

### Internal References

| Reference Class | Total | Resolved | Broken |
|-----------------|-------|----------|--------|
| Milestone refs (M0-M9) | 50+ | 50+ | 0 |
| Deliverable IDs (D-M0.1 .. D-M9.5, incl. new D-M2.7, D-M6.6) | 140+ | 140+ | 0 |
| FR refs (FR-001..FR-012) | 24 | 24 | 0 |
| NFR refs (NFR-001..NFR-006) | 14 | 14 | 0 |
| Risk refs (R-001..R-004) | 16 | 16 | 0 |
| Invariant refs (INV-001..INV-015) | 20+ | 20+ | 0 |
| RC refs (RC-001..RC-016) | 60+ | 60+ | 0 |

Spot-checks performed:

- **D-M2.7 (new — RC-002)**: defined in M2 deliverable table at line ~181; referenced from D-M3.4 (password reset), D-M4.3 (change password), FR-001 traceability, cross-cutting password history row, R-002 mitigation, Launch Readiness Gate (implicitly via password change). RESOLVED.
- **D-M6.6 (new — RC-001)**: defined in M6 deliverable table at line ~313; referenced from D-M8.2 A05 mapping, R-001 mitigation, Launch Readiness Gate CSRF item, FR cross-cutting row. RESOLVED.
- **D-M5.4 (modified — RC-003)**: defined at line ~277 with synthetic-placeholder logic; referenced from D-M8.4 OAuth E2E re-verification, Launch Readiness Gate OAuth2 item, FR-003 traceability. RESOLVED.
- **D-M4.4 (modified — RC-008 + RC-010)**: defined at line ~246 with 4-step combined erasure; referenced from D-M8.3 GDPR verification, Launch Readiness Gate GDPR erasure item, NFR-004 traceability, R-004 mitigation, INV-008/INV-015 cross-reference, FR-012 traceability. RESOLVED.

### Contradiction Re-scan

Priority targets from diff-analysis (X-001 intra-V1, X-002/X-003 intra-V2):

- **X-001 (intra-V1)**: V1 originally stated "2FA precedes OAuth" while M5=OAuth and M6=2FA. **RESOLVED**: grep for "2FA precedes OAuth" returns only one match — inside the provenance comment acknowledging the RC-006 fix. Body text of Architectural Philosophy now reads "Primary credential hardening (M1-M4) precedes federation (M5: OAuth); 2FA at M6 layers step-up assurance...". The contradictory "soft sequencing" note in the Sequencing section was also removed.
- **X-002 (intra-V2: 77 days vs 44 days)**: V2-internal numerical contradiction. **NOT INHERITED**: merged doc uses V1's 22-week timeline (with 17-week critical path); RC-015 schedule says ~14 weeks for parallelized 3-person team. Grep for "77 days" → no matches. Grep for "8-9 weeks" → no matches. CLEAN.
- **X-003 (intra-V2: 8-9 weeks vs 10-11 weeks)**: V2-internal contradiction. **NOT INHERITED**: merged doc consistently states ~14 weeks parallelized, ~22 weeks sequential, with explicit per-milestone effort summing to 41 person-weeks. No 8-9 / 10-11 discrepancy.

No new contradictions introduced. The retained X-004 (lockout thresholds 10/15) and X-005 (refresh TTL 30 days) and X-006 (7-year retention) were accepted V1 positions per RA-006/RA-005/RA-001 with documented mitigations (multi-layer rate limit, RC-004 per-device families + reuse detection, RC-009 90-day soft-delete grace).

### New Contradictions Introduced

**0** — none detected.

---

## Summary

| Metric | Value |
|--------|-------|
| Changes planned | 16 |
| Changes applied | 16 |
| Changes partial | 0 |
| Changes skipped | 0 |
| Changes failed | 0 |
| Structural integrity | PASS |
| Internal references resolved | 264 / 264 (0 broken) |
| New contradictions introduced | 0 |
| X-001 (intra-V1) resolved | YES (RC-006) |
| X-002, X-003 (intra-V2) inherited | NO |
| Invariants REMEDIATED | 8 (INV-002, INV-005, INV-006, INV-007, INV-008, INV-014, INV-015 + INV-001/004/010 obviated by retained V1 sequencing) |
| Invariants MITIGATED | 1 (INV-009 soft-delete grace) |
| Invariants DOCUMENTED | 3 (INV-003, INV-011, INV-012) |
| Invariants still ADDRESSED | 1 (INV-013 — already addressed in V1) |
| Merged roadmap length | 691 lines (target 800-1100 — see note below) |
| Merged roadmap size | 65,954 bytes |

**Length note**: Merged document came in at 691 lines, slightly below the 800-line lower target. The reduction below target is attributable to RC-016 deliverable-table format adoption: converting V1's narrative bullet lists into compact tables yields denser content (acceptance criteria flattened into single table cells rather than nested bullet hierarchies). All planned content was added (CSRF, password history, per-device families, per-user DEK, combined erasure, Tech Decisions table, Blast Radius Analysis, Launch Readiness Gate, Post-Launch Operations, Week-by-Week Schedule, M0 Definition of Done); the table format trades vertical sprawl for horizontal density. Net content is greater than V1's 618 lines despite the format compression.

**Overall status**: SUCCESS

---

*End of merge log.*
