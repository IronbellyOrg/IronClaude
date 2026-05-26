# Refactor Plan: V1 (opus) Base + V2 Strengths + Invariant Remediations

> **Pipeline**: sc:adversarial Mode B, Step 4
> **Base variant**: V1 (opus-default, 618 lines)
> **Non-base variant**: V2 (sonnet-default, 723 lines)
> **Source inputs**: diff-analysis.md, debate-transcript.md, base-selection.md, invariant-probe.md

---

## Overview

- **Base variant**: V1 (opus-default)
- **Non-base variant**: V2 (sonnet-default)
- **Planned changes**: 16
- **Rejected alternatives**: 7
- **Overall risk**: Medium

V1 was selected as base (score 0.763 vs 0.707) on the strength of its quantitative dominance (0.992 vs 0.914), RBAC-before-OAuth sequencing, M0 foundations, tamper-evident audit trail, and superior failure-mode coverage. Both variants score 0/5 on Dimension 6 (Invariant and Edge Case Coverage), so invariant remediations dominate the plan. The merge strategy grafts V2's operational legibility improvements (rationale tables, blast radius analysis, checklists, schedule) onto V1's structurally correct security architecture, then patches five cross-variant invariant violations and two V1-specific ones.

---

## Planned Changes

### TIER 1 — CRITICAL (must-do): Invariant remediations + V1 conceded weaknesses

---

**RC-001** — Add CSRF protection as dedicated deliverable

- **Source**: V2 D-M6.8 (U-011, strength S1); V1 conceded in R2 ("Real defect")
- **Target location**: V1 Milestone M6 (2FA, Rate Limiting and Audit Logging)
- **Integration approach**: add-new
- **Rationale**: V1 relies on SameSite=Strict alone. Both OWASP ASVS L2 and the debate (V1 advocate R2 concession, V2 advocate R2 acceptance) confirm this is a gap. V2's double-submit cookie pattern with `__Host-csrf-token` is the standard remediation. The CSRF token must be validated on all state-changing requests (POST, PUT, PATCH, DELETE).
- **Risk level**: Low (additive deliverable within existing M6 scope)

---

**RC-002** — Add password history enforcement deliverable

- **Source**: V2 D-M7.5 (U-012, strength S2); V1 conceded in R2 ("OWASP ASVS L2 V2.1.10 requires")
- **Target location**: V1 Milestone M2 (Core Auth: Registration + Login + JWT)
- **Integration approach**: add-new
- **Rationale**: OWASP ASVS L2 V2.1.10 requires password history. V1's zxcvbn + HIBP checking covers strength but not reuse. Add deliverable: `password_history` table storing bcrypt-hashed previous passwords (last 5); registration and password-change endpoints check new password against history before acceptance.
- **Risk level**: Low (additive deliverable; no modification to existing M2 deliverables)

---

**RC-003** — Remediate INV-002: OAuth null-email handling

- **Source**: INV-002 (HIGH-UNADDRESSED, both variants)
- **Target location**: V1 Milestone M5 (OAuth2), deliverable D-M5.3 (OAuth callback)
- **Integration approach**: restructure
- **Rationale**: GitHub OAuth returns null email when user has no public email set. V1 schema has `email CITEXT UNIQUE` (D-M1.1), which rejects null. The merged output must either: (a) make email nullable and generate a synthetic email from `provider_user_id` + domain (e.g., `{github_12345}@oauth.placeholder.invalid`), or (b) redirect the user to an email-collection screen on first OAuth login. Option (a) is simpler and does not block the auth flow; option (b) is stricter but adds UX complexity. Recommend option (a) with a flag marking the email as unverified, requiring email verification on next login to upgrade to a real address.
- **Risk level**: Medium (modifies schema constraint and OAuth callback logic)

---

**RC-004** — Remediate INV-005: Per-device refresh token families

- **Source**: INV-005 (HIGH-UNADDRESSED, both variants)
- **Target location**: V1 Milestone M3 (Sessions, Refresh Tokens and Password Reset), deliverable D-M3.1
- **Integration approach**: restructure
- **Rationale**: Two legitimate devices racing on refresh rotation triggers reuse detection that logs out all devices. RFC 6819 section 5.2.2.3 pattern (used by both variants) has no device isolation. Remediation: add per-device refresh token families. Each device gets a `device_id` (set on first refresh). When device A refreshes, only device A's old token is revoked. If device B's old token is then used, the system checks whether it belongs to the same device family -- if within a 30-second grace window, both old and new tokens are accepted. If outside the window and different device, full revocation triggers (genuine theft). This preserves theft detection while eliminating false positives from concurrent legitimate usage.
- **Risk level**: High (restructures refresh token lifecycle; modifies token schema, rotation logic, and revocation decision tree)

---

**RC-005** — Remediate INV-006: Reconcile Argon2id parameters with NFR-001 budget

- **Source**: INV-006 (HIGH-UNADDRESSED, both variants); V2 Technology Decisions rationale (strength S3)
- **Target location**: V1 Milestone M1 (Data Layer and Crypto Primitives), deliverable D-M1.3; NFR-001 traceability entry
- **Integration approach**: restructure
- **Rationale**: V1's Argon2id at m=65536/t=3/p=4 produces approximately 250ms per hash. V1 NFR-001 specifies p95 < 200ms total API response, and V1 M2 exit criteria specify login p95 < 150ms. The hash alone exceeds both budgets. Remediation: tune Argon2id to m=32768/t=2/p=4 targeting approximately 80ms p95 hash on production hardware. Document explicit NFR budget breakdown: hash verification 80ms + DB user lookup 60ms + JWT signing 20ms + network overhead 40ms = 200ms p95. Add budget-breakdown table to NFR-001 traceability entry. M1 exit criterion updates to: "Argon2id hash verification < 100ms p95 on target hardware (m=32768/t=2/p=4)."
- **Risk level**: Medium (modifies security parameters; must re-verify that tuned parameters remain above OWASP minimum thresholds)

---

**RC-006** — Remediate INV-008: Per-user DEK for cryptographic erasure

- **Source**: INV-008 (HIGH-UNADDRESSED, V1-specific)
- **Target location**: V1 Milestone M1 (Data Layer), deliverable D-M1.2; Milestone M4 (RBAC), deliverable D-M4.4
- **Integration approach**: restructure
- **Rationale**: V1's DEK rotation destroys ALL users' PII, not just the requesting user. This is system-wide data destruction, not GDPR Article 17 per-user erasure. Remediation: adopt per-user DEK architecture. Each user gets a unique Data Encryption Key (`user_dek`) encrypted with a master KEK from KMS (envelope encryption). When a user requests erasure, only that user's KEK-wrapped DEK is destroyed, rendering only that user's PII columns undecryptable. Other users are unaffected. D-M1.2 updated to describe per-user DEK generation at registration; D-M4.4 updated to describe per-user DEK destruction for erasure requests. Schema adds `user_encryption_keys` table.
- **Risk level**: High (restructures encryption architecture from column-level to per-user key management; adds schema table, KMS call volume, and key rotation complexity)

---

**RC-007** — Remediate INV-015: Combined crypto erasure + pseudonymization for GDPR

- **Source**: INV-015 (HIGH-UNADDRESSED, V1-specific); V2 D-M8.4 anonymization approach (X-007)
- **Target location**: V1 Milestone M4, deliverable D-M4.4; Milestone M6, deliverable D-M6.4
- **Integration approach**: restructure
- **Rationale**: V1's crypto erasure + PII pseudonymization may not satisfy strict GDPR Article 17 because: (a) pseudonymization is not erasure under Recital 26; (b) audit_events.actor_user_id retains linkability; (c) metadata JSONB may contain identifiable fragments. Remediation: combine V1's per-user DEK destruction (RC-006) with V2's field-level anonymization. Erasure flow: (1) destroy user's DEK (crypto erasure of PII columns), (2) pseudonymize actor_user_id in audit_events to `anonymized_<uuid>` after 30-day grace period, (3) scrub user-identifiable fragments from metadata JSONB, (4) remove OAuth provider_user_id mapping. Document that this combined approach targets "effective erasure" per Recital 26 (data no longer identifiable by any means reasonably likely to be used).
- **Risk level**: High (combines two erasure strategies; modifies audit log schema and erasure workflow)

---

**RC-008** — Remediate INV-014: Document Merkle chain tamper detection scope

- **Source**: INV-014 (HIGH-UNADDRESSED, both variants; V2's role-permission approach is weaker)
- **Target location**: V1 Milestone M6, deliverable D-M6.4
- **Integration approach**: append
- **Rationale**: V1's hash chain + daily Merkle root is the correct approach (already present in base). The invariant finding is that V2's role-permission-only approach was insufficient, and V1's approach needs explicit scope documentation. Add a "Tamper Detection Scope" subsection to D-M6.4 explicitly stating what the Merkle chain detects (DBA direct SQL modifications, backup restoration with tampered data) and what it does not (replication bypass, OS-level file tampering -- require separate detective controls documented in M7 operational readiness).
- **Risk level**: Low (documentation-only addition; no code or schema changes)

---

**RC-009** — Remediate INV-009: Add soft-delete-before-hard-delete for audit partitions

- **Source**: INV-009 (HIGH-UNADDRESSED, V2-specific); V1 uses 7-year retention so the retroactive-gap risk is lower, but the partition-drop irreversibility applies to both
- **Target location**: V1 Milestone M6, deliverable D-M6.4 (audit log retention)
- **Integration approach**: append
- **Rationale**: V1 retains for 7 years, which covers most compliance regimes. However, partition drops are irreversible even in V1. If a regulated customer requires extension beyond 7 years retroactively, already-dropped partitions cannot be recovered. Remediation: add a soft-delete-before-hard-delete schema option. Audit partitions enter a "detached but preserved" state for 90 days after exceeding retention threshold before actual DROP. This provides a 90-day recovery window for retention-extension decisions. Document this as an operational safeguard, not a default behavior change.
- **Risk level**: Low (additive operational safeguard; does not change 7-year default retention)

---

### TIER 2 — HIGH-VALUE incorporations from V2

---

**RC-010** — Add Technology Decisions and Rationale table

- **Source**: V2 lines ~693-707 (strength S3, U-010); V1 advocate R2 noted it "landed strongly"
- **Target location**: New section after V1 Milestone Summary Table, before M0
- **Integration approach**: add-new
- **Rationale**: V2's explicit rationale table (Argon2id m=65536/t=3/p=4, RS256 over HS256, AES-256-GCM, Redis sliding-window, TOTP with rationale) improves specificity and provides decision-audit trail. Adapt V2's format to V1's technology choices, incorporating the tuned Argon2id parameters from RC-005 (m=32768/t=2/p=4) and per-user DEK architecture from RC-006. Table format: Technology | Choice | Rationale | Alternative Considered.
- **Risk level**: Low (additive section; does not modify any existing V1 content)

---

**RC-011** — Add Blast Radius Analysis section

- **Source**: V2 lines ~712-720 (strength S4, U-010); V1 advocate R2 noted it "landed partially"
- **Target location**: New section after V1 Architectural Philosophy, before Milestone Summary
- **Integration approach**: add-new
- **Rationale**: V2's 6 named failure-isolation invariants (token storage isolation, Redis as cache not authority, OAuth additivity, append-only audit, rate limiter isolation, KMS key separation) make architectural trade-offs explicit. Adapt to V1's architecture: add per-user DEK isolation (from RC-006) as a 7th blast-radius invariant. This section complements V1's M0 threat model by documenting runtime failure containment.
- **Risk level**: Low (additive section)

---

**RC-012** — Add consolidated pre-launch verification checklist and ongoing verification cadence

- **Source**: V2 lines ~666-680 (strength S5) and V2 lines ~683-688 (strength S6)
- **Target location**: V1 Milestone M9 (Production Cutover and Hardening); new subsection after M9 exit criteria
- **Integration approach**: append
- **Rationale**: V1 has per-milestone exit criteria but no single consolidated pre-launch gate. V2's 15-item checklist (auth smoke test, OAuth E2E, load test baseline, OWASP scan, GDPR export/delete, monitoring, alerting, backup restore, rollback, rate limiting, lockout, token theft detection, CSP, PII encryption) is actionable and trackable. Additionally, V1 stops at M9 production cutover with no post-launch verification cadence. Add V2's daily/weekly/monthly/quarterly/annual ongoing verification schedule as a subsection of M9.5 (Post-launch review).
- **Risk level**: Low (additive checklists and cadence schedule)

---

**RC-013** — Add person-week effort estimates per milestone and week-by-week parallelization schedule

- **Source**: V2 lines ~634-647 (strength S7); V1 advocate R2 conceded ("honest concession that V1 should provide effort estimates")
- **Target location**: V1 Milestone Summary Table (add "Effort" column); new subsection in Sequencing section
- **Integration approach**: restructure
- **Rationale**: V1 is team-agnostic with no resource quantification. V2 advocate R2 identified this as a shared weakness, and V1 advocate conceded. Add person-week estimates per milestone to the Milestone Summary Table. Add a week-by-week parallelization schedule subsection (adapted from V2's 3-person model) to the Sequencing section, noting that assignments are illustrative and should be adjusted to actual team composition.
- **Risk level**: Low (additive information to existing tables and sections)

---

### TIER 3 — POLISH: Clarity improvements and internal consistency fixes

---

**RC-014** — Fix X-001: Rewrite Architectural Philosophy to align with milestone ordering

- **Source**: X-001 (intra-V1 contradiction, Medium severity); V1 advocate R2 partial concession
- **Target location**: V1 Architectural Philosophy section (line ~11)
- **Integration approach**: restructure
- **Rationale**: Philosophy states "2FA (FR-007) precedes OAuth" but milestone ordering is M5=OAuth, M6=2FA. V1 advocate's R2 reframe (philosophy refers to "trust delegation" not "foundational hardening") is linguistically creative but structurally hollow per V2 R2 rebuttal. Rewrite the philosophy statement to: "Primary credential hardening (M1-M4: argon2id, RS256, lockout, RBAC) precedes federation (M5: OAuth); 2FA at M6 layers step-up assurance on top of the hardened primary path." Remove the misleading "2FA precedes OAuth" claim entirely.
- **Risk level**: Low (documentation fix; no milestone or deliverable changes)

---

**RC-015** — Add M0 definition-of-done checklist to mitigate scope-creep meta-risk

- **Source**: V1 W5 (M0 scope-creep meta-risk acknowledged but not structurally mitigated); V1 Meta-Risks section
- **Target location**: V1 Milestone M0, after exit criteria
- **Integration approach**: append
- **Rationale**: V1's Meta-Risks section identifies M0 scope creep as a risk. V2 advocate R2 rebutted that "named deliverables with definition-of-done do not prevent M0 from absorbing parallelizable work." Add an explicit M0 definition-of-done checklist: (1) STRIDE threat model document reviewed by security lead, (2) ADR-001 through ADR-004 approved, (3) Vault dev-mode operational with pepper stored, (4) CI/CD pipeline passes smoke test, (5) No auth-related code merged. M0 is complete when all 5 items pass; no additional items may be added without explicit scope-change request documented in ADR.
- **Risk level**: Low (additive checklist; no deliverable changes)

---

**RC-016** — Adopt deliverable table format per milestone (from V2's structured tables)

- **Source**: V1 W6 (narrative bullets harder to track than V2 tables); V2 S-003 (deliverable format)
- **Target location**: All V1 milestone deliverable sections (M0 through M9)
- **Integration approach**: restructure
- **Rationale**: V2's ID / Deliverable / Acceptance Criteria table format is more trackable than V1's narrative bullet points. Convert each milestone's deliverables from bullet list to table format: Deliverable ID | Description | Acceptance Criteria. Preserve all existing V1 content (deliverable IDs, descriptions, exit criteria) in the new format. This is a presentation-only change that improves scanability for PM tracking.
- **Risk level**: Medium (restructures formatting of all 10 milestone sections; content preserved but presentation changed)

---

## Changes NOT Being Made (Rejected Alternatives)

---

**RA-001** — V2's 2-year audit retention (instead of V1's 7-year)

- **V2 approach**: 2-year configurable retention via partition drop cron (D-M8.5)
- **V1 approach (kept)**: 7-year retention covering SOX, HIPAA, PCI-DSS, FINRA
- **Debate evidence**: V1 advocate R2 rebuttal (R-005 reframe): "7-year is configurable downward; V2's shorter default forces costly retention-extension project." V2 advocate R2 YAGNI rebuttal was noted but the base-selection scoring favored V1's future-proofing (V1 Risk Coverage 4/5 vs V2's 2/5). INV-009 (retention retroactive gap) is mitigated by RC-009 (soft-delete grace period).
- **Risk if rejected**: None -- 7-year is strictly more conservative and covers the 2-year case trivially.

---

**RA-002** — V2's parallel RBAC/OAuth sequencing (M4/M5 concurrent)

- **V2 approach**: M4 (OAuth) and M5 (RBAC) run in parallel after M3, no dependency edge
- **V1 approach (kept)**: M4 (RBAC) before M5 (OAuth) as hard constraint
- **Debate evidence**: S-007 (High severity): V1 enforces RBAC-before-OAuth; V2 creates authorization vacuum. V2 advocate R2 partial rebuttal ("default-role hook merged before either considered complete") was undermined by INV-001, INV-004, INV-010 -- all HIGH-UNADDRESSED findings confirming the vacuum exists during integration testing. The merged output retains V1 sequencing, making INV-001, INV-004, and INV-010 N/A.
- **Risk if rejected**: None -- V1 sequencing eliminates the authorization vacuum class of invariants entirely.

---

**RA-003** — V2's anonymization-only GDPR erasure

- **V2 approach**: Replace PII with `anonymized_<uuid>`, schedule hard deletion after 30 days
- **V1 approach (kept)**: Cryptographic erasure via DEK rotation, augmented per RC-006/RC-007
- **Debate evidence**: X-007 (High): V2's anonymization preserves data structure and retains actor_id references; V1's DEK rotation destroys decryptability. V2 advocate R2 conceded V1 is stronger on this point. INV-015 confirms V1's approach alone is insufficient for strict GDPR but the combined approach (RC-007) addresses both concerns.
- **Risk if rejected**: None -- RC-007's combined approach is strictly stronger than either variant alone.

---

**RA-004** — V2's distributed foundations (no M0)

- **V2 approach**: Infrastructure bootstrap in M1 (5 days), no dedicated threat model or ADR milestone
- **V1 approach (kept)**: Dedicated M0 "Foundations and Threat Model" (2 weeks)
- **Debate evidence**: S-002 (High): U-001 (V1's M0 is a high-value unique contribution). V2 advocate R2 rebuttal ("compresses critical path by 2 weeks") was noted but base-selection scoring weighted V1's security-first sequencing. V1 advocate R1: "OWASP/SAMM shift left prescription." M0 scope creep (V1 meta-risk) mitigated by RC-015 (definition-of-done checklist).
- **Risk if rejected**: 2 weeks added to schedule front. Accepted trade-off for threat-modeling discipline.

---

**RA-005** — V2's 7-day refresh token TTL (instead of V1's 30-day)

- **V2 approach**: 7-day refresh token TTL (D-M3.4)
- **V1 approach (kept)**: 30-day refresh token TTL with reuse detection
- **Debate evidence**: X-005 (High): 30-day gives 4x larger theft window. V1 advocate R2 argued reuse detection collapses effective window. V2 advocate R2 identified V1's pivotal factual error (V2 also has reuse detection, so effective windows are equal). With RC-004 (per-device token families), the false-positive concern is resolved. Remaining V1 advantage is UX (less frequent re-auth). Kept as legitimate UX trade-off.
- **Risk if rejected**: 30-day tokens have larger theoretical theft window than 7-day. Mitigated by reuse detection + per-device families (RC-004). Accepted trade-off for UX.

---

**RA-006** — V2's lockout thresholds (5 failures / 30 min) instead of V1's (10 failures / 15 min)

- **V2 approach**: 5 failed attempts in 15 min triggers 30-min lockout (D-M3.9)
- **V1 approach (kept)**: 10 failed attempts in 15 min triggers 15-min lockout (D-M6.3)
- **Debate evidence**: X-004 (High): opposing thresholds. V1's 10/15 is less aggressive, giving attackers more attempts. However, V1 pairs this with 50/IP/h IP-block (D-M6.2) and 10/min/IP rate limiting, providing defense-in-depth. INV-007 (lockout semantics ambiguity) applies to both. The merged output should clarify semantics (lockout triggers ON the Nth failed attempt, which is also rejected) regardless of which threshold is chosen.
- **Risk if rejected**: 10-attempt threshold is less conservative than 5. Mitigated by V1's multi-layer rate limiting. Accepted trade-off for lower false-positive risk on legitimate users.

---

**RA-007** — V2's role taxonomy (admin/moderator/user) instead of V1's (user/admin/support/auditor)

- **V2 approach**: admin (all permissions), moderator (users:read, users:suspend), user (self:read, self:write)
- **V1 approach (kept)**: user, admin, support, auditor (read-only audit log access)
- **Debate evidence**: C-012 (Medium). V1's taxonomy includes a dedicated `auditor` role with read-only audit log access, which is important for compliance scenarios where audit reviewers must not have mutation capabilities. V2's `moderator` role is a reasonable alternative but does not provide the audit-isolation property. V1's approach is kept for compliance readiness.
- **Risk if rejected**: V2's moderator role covers user-management use cases not in V1's taxonomy. Can be added as a future role if needed without architectural change.

---

## Risk Summary

| Change ID | Risk | Impact if Poorly Executed | Rollback Approach |
|-----------|------|---------------------------|-------------------|
| RC-001 | Low | CSRF token added incorrectly could break state-changing requests | Remove deliverable; revert to SameSite=Strict only |
| RC-002 | Low | Password history table adds migration complexity | Remove deliverable; password changes revert to strength-only checks |
| RC-003 | Medium | Nullable email or synthetic email may cause downstream issues (email verification flows, uniqueness constraints) | Revert to NOT NULL email; require email-collection screen on OAuth first login instead |
| RC-004 | High | Per-device token families change core auth flow; incorrect grace-window logic could either (a) re-introduce false positives or (b) weaken theft detection | Revert to single-family tokens; document as known limitation |
| RC-005 | Medium | Tuned Argon2id parameters may be below OWASP minimum on slower hardware | Benchmark on target hardware before merging; revert to m=65536/t=3/p=4 if below threshold |
| RC-006 | High | Per-user DEK adds KMS call volume (one call per user per encryption/decryption); key management complexity increases operational surface | Revert to column-level DEK; accept INV-008 as documented limitation with per-user erasure via field-level anonymization only |
| RC-007 | High | Combined erasure flow is complex; audit-log pseudonymization could break audit trail integrity if foreign keys not handled | Revert to V1 crypto-erasure only; document GDPR risk acceptance |
| RC-008 | Low | Documentation-only; no functional impact | Remove subsection |
| RC-009 | Low | Soft-delete adds storage overhead for 90-day grace period | Remove grace period; accept irreversibility of partition drops |
| RC-010 | Low | Additive section; no functional impact | Remove section |
| RC-011 | Low | Additive section; no functional impact | Remove section |
| RC-012 | Low | Additive checklists; no functional impact | Remove subsections |
| RC-013 | Low | Additive estimates; schedule is illustrative | Remove column and subsection |
| RC-014 | Low | Documentation fix; no functional impact | Restore original philosophy text |
| RC-015 | Low | Additive checklist; no functional impact | Remove checklist |
| RC-016 | Medium | Formatting change across all milestones; could introduce copy errors during conversion | Revert to narrative bullet format |

### High-risk changes (RC-004, RC-006, RC-007) mitigation strategy

The three High-risk changes all relate to the auth token and encryption core. They should be applied in sequence: RC-006 (per-user DEK) first, then RC-007 (combined erasure, which depends on RC-006), then RC-004 (per-device tokens, which is independent but touches the same auth subsystem). Each should be validated against the base variant's exit criteria before the next is applied. If any High-risk change fails validation, it should be documented as a known limitation and the corresponding invariant remediation noted as "accepted risk with documented mitigation."

---

## Invariant Remediation Cross-Reference

| Invariant | Severity | Change(s) | Status After Merge |
|-----------|----------|-----------|-------------------|
| INV-001 (V2-specific) | HIGH | N/A -- V1 sequencing kept | N/A (authorization vacuum does not exist with RBAC-before-OAuth) |
| INV-002 (both) | HIGH | RC-003 | REMEDIATED (nullable email + synthetic placeholder) |
| INV-003 (both) | MEDIUM | Not in scope -- 15-min JWT TTL is a known design trade-off | DOCUMENTED (JWT self-validation window accepted; denylist checked on refresh, not every request) |
| INV-004 (V2-specific) | HIGH | N/A -- V1 sequencing kept | N/A |
| INV-005 (both) | HIGH | RC-004 | REMEDIATED (per-device token families with grace window) |
| INV-006 (both) | HIGH | RC-005 | REMEDIATED (tuned parameters + explicit budget breakdown) |
| INV-007 (both) | MEDIUM | Implicit in RC-016 formatting | DOCUMENTED (clarify lockout triggers ON the Nth attempt in acceptance criteria) |
| INV-008 (V1) | HIGH | RC-006 | REMEDIATED (per-user DEK with envelope encryption) |
| INV-009 (V2) | HIGH | RC-009 | MITIGATED (soft-delete grace period for partition recovery) |
| INV-010 (V2-specific) | HIGH | N/A -- V1 sequencing kept | N/A |
| INV-011 (both) | MEDIUM | Not in scope -- V1 already has circuit breaker + retry queue | PARTIALLY ADDRESSED (V1 retry queue kept; user-facing degradation note added) |
| INV-012 (both) | MEDIUM | Not in scope -- emergency key-compromise procedure | DOCUMENTED (add note to D-M9.2 that key compromise = immediate revocation of all tokens, no overlap period) |
| INV-013 (both) | LOW | Already ADDRESSED per invariant probe | ADDRESSED |
| INV-014 (both) | HIGH | RC-008 | REMEDIATED (Merkle chain scope documented; V2's weaker approach rejected) |
| INV-015 (V1) | HIGH | RC-007 | REMEDIATED (combined crypto erasure + pseudonymization + audit scrub) |

---

## Review Status

- **Approval mode**: auto-approved (non-interactive mode)
- **Approval status**: auto-approved
- **Timestamp**: 2026-05-22

---

*End of refactor plan. Proceed to Step 5: Assembly.*
