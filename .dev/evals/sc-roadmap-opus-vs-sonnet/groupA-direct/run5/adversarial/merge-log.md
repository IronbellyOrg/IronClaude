# Merge Log: V1 Base → Merged Roadmap

## Metadata

| Field | Value |
|---|---|
| Base variant | `variant-1-opus-default.md` (opus, default) |
| Cross-referenced variant | `variant-2-sonnet-default.md` (sonnet, default) |
| Invariant probe | `invariant-probe.md` (16 findings, 6 HIGH) |
| Refactor plan | `refactor-plan.md` (17 planned changes) |
| Executor | merge-executor (sc:adversarial Step 5) |
| Timestamp | 2026-05-22 |
| Planned change count | 17 (11 V2 incorporations + 6 mandatory invariant resolutions) |
| Output | `../merged-output.md` (386 lines) |
| Status | **success** — all 17 changes applied; all 6 HIGH invariants concretely resolved |

---

## Per-Change Applied Log

### Category A: V2 Strength Incorporations

#### Change #1: Adopt versioned API paths (`/api/v1/*`)

- **Status**: APPLIED
- **Before**: V1 used `/auth/*`, `/me/*` throughout milestone deliverables, risk register, and verification matrix.
- **After**: All endpoint references rewritten to `/api/v1/auth/*` and `/api/v1/me/*` across M1 D1.8, M2 D2.1–D2.7, M3 D3.2–D3.4, M4 D4.2–D4.8, M5 D5.1–D5.3, Risk Register mitigation column, FR/NFR verification matrix. Deprecation policy (Sunset header, 6-month parallel-version window) added to new "API Conventions" section and Cross-Cutting Security.
- **Provenance tag added**: `<!-- Source: Base (modified) — Change #1 (versioning) -->` on milestone headers and "API Conventions" section.
- **Side effect**: Resolves INV-009 (deprecation policy gap).

#### Change #2: Add walking-skeleton login to M1

- **Status**: APPLIED
- **Before**: V1 M1 had 7 deliverables (D1.1–D1.7); nothing user-facing shipped in M1.
- **After**: Added D1.8 "Walking-skeleton login endpoint + bootstrap admin CLI" combining the walking-skeleton requirement with the #M2 bootstrap CLI requirement. M1 title updated to "Foundation & Security Primitives + Walking-Skeleton Login". Executive summary M1 sentence amended. Acceptance criteria include the skeleton login + ADR Argon2id-tier recording.
- **Provenance tag added**: M1 header carries Change #2 reference.

#### Change #3: Pin technology stack via week-0 ADR

- **Status**: APPLIED
- **Before**: V1 line 7 said "(reference; the spec does not pin a language — substitute equivalents if implementing in Python/Go)"; no ADR section.
- **After**: New "Week-0 Architecture Decision Record" section before "## Milestones" with explicit table pinning Python 3.11+ / FastAPI / SQLAlchemy / Alembic / pyotp / authlib / OpenTelemetry + Node.js 20 LTS alternative; framework-agnostic disclaimer removed from header. Argon2id parameter-tier row anticipates #M5.
- **Provenance tag added**: `<!-- Source: Base (modified) — Change #3: Pin stack via ADR -->` on the ADR section.

#### Change #4: Admin <500ms@50K performance gate + EXPLAIN ANALYZE CI

- **Status**: APPLIED
- **Before**: V1 D5.2 (admin dashboard) had no explicit performance gate; no query-plan CI step.
- **After**: D5.2 acceptance amended: "Admin user list loads in <500ms p95 with 50,000 seeded user records." New D5.10 "Query-plan CI gate" added with explicit rule: PR fails if EXPLAIN ANALYZE shows sequential scan on >10K-row table.
- **Provenance tag added**: M5 header carries Change #4 reference.

#### Change #5: Pagination defaults (50 / max 200)

- **Status**: APPLIED
- **Before**: V1 list endpoints had no documented pagination envelope.
- **After**: "API Conventions" section now codifies `page` (default 1) and `per_page` (default 50, max 200) with `{"results": [...], "total": N, ...}` envelope. D4.6 audit-log query, D5.2 admin user list, and session-management view inherit this.
- **Provenance tag added**: "API Conventions" section carries Change #5 reference.
- **Side effect**: Resolves INV-007 (empty-shape divergence).

#### Change #6: Schemathesis contract testing per PR

- **Status**: APPLIED
- **Before**: V1 testing strategy had nightly contract tests against external Google/GitHub OIDC discovery only; no own-API contract gate.
- **After**: Testing Strategy table now has separate "Contract (own API) — Schemathesis v3+ — Every PR (CI)" and "Contract (external) — Provider OIDC discovery harness — Nightly (CI)" rows. D1.6 CI pipeline references Schemathesis.
- **Provenance tag added**: Testing Strategy section carries Change #6.

#### Change #7: Email-change-keeps-old-email-valid

- **Status**: APPLIED (folded into Mandatory Change #M1 since they are coupled)
- **Before**: V1 D5.1 said "email re-verification required" with no specification of which email holds the login key during pending window; schema had a single unique `email` column.
- **After**: D5.1 specifies the full pending_email/pending_email_token_hash flow; D1.1 schema includes both columns; D2.7 password-reset keys on old email; D4.8 erasure handles tombstone of `email_blind_index`.
- **Provenance tag added**: D5.1 + D1.1 reference both Change #7 and Mandatory #M1.

#### Change #8: Redis Sentinel (dev/test) + managed Redis (prod)

- **Status**: APPLIED
- **Before**: V1 D1.2 said "Redis 7.2 cluster configuration with TLS" — single environment description; D5.4 inherited generically.
- **After**: D1.2 specifies Sentinel-based failover (1 primary + 2 replicas + 3 sentinels) for dev/test docker-compose. D5.4 specifies managed Redis (ElastiCache / Memorystore) via Kubernetes Service for production — explicit split.
- **Provenance tag added**: D1.2 row carries Change #8 reference; D5.4 row carries Change #8 reference.

#### Change #9: Markdown table deliverable format

- **Status**: APPLIED
- **Before**: V1 deliverables were bullet lists per milestone (D1.1 through D5.9).
- **After**: All milestones (M1–M5) now use `| ID | Deliverable | Description |` tables. All content preserved verbatim with additions from mandatory changes folded into the relevant rows.
- **Provenance tag added**: Each milestone header carries Change #9 reference.

#### Change #10: STRIDE-row revalidation per milestone gate

- **Status**: APPLIED
- **Before**: V1 had a single threat-model sign-off at M1; no per-milestone re-validation.
- **After**: M2, M3, M4, M5 acceptance criteria each include "STRIDE threat model rows mapped to milestone scope are re-tested and signed off by the named Security Lead within 2 business days of milestone completion." D1.7 names the Security Lead role.
- **Provenance tag added**: M2–M5 headers reference Change #10.

#### Change #11: Spec-aligned role taxonomy (admin/user) + status separation

- **Status**: APPLIED
- **Before**: V1 D3.5 had roles `admin/user/support`; V2 had `admin/user/suspended` mixing role and status.
- **After**: D3.5 specifies roles `admin`, `user` (default) with `users.status` enum (`active`, `suspended`, `deactivated`) orthogonal to role. RBAC middleware checks role; lockout/suspension middleware checks status. D1.1 schema includes `users.status` column. D5.3 deactivation flow sets status, not role.
- **Provenance tag added**: M3 header references Change #11; D1.1 row references status separation.

### Category B: Mandatory Invariant Probe Resolutions

#### Mandatory Change #M1: INV-001 — pending-email state representation

- **Status**: APPLIED
- **Before**: V1 had a single unique `email` column; ambiguity about which email is the login key during pending window.
- **After**: D1.1 includes `pending_email` (nullable, encrypted) and `pending_email_token_hash` (nullable). D5.1 email-change flow uses pending columns. Verification transactionally promotes pending to current, recomputes blind-index, revokes refresh-token families. Reset-password keys on OLD email (`email_blind_index` unchanged until verification) — preventing account takeover.
- **Provenance tag added**: M1 + M5 headers reference Mandatory #M1; D5.1 row carries explicit "(per #M1)" annotations.

#### Mandatory Change #M2: INV-003 — admin promotion 2FA enrollment gate

- **Status**: APPLIED
- **Before**: V1 said "2FA mandatory for admin (enforced at login)" — silent on role-promotion-while-logged-in path.
- **After**: D1.1 schema includes `users.pending_2fa_enrollment` boolean. D3.6 authorization middleware enforces the gate: returns HTTP 403 `{"error": "admin_2fa_required", ...}` for all routes except `/api/v1/auth/2fa/enroll` and `/logout`. D3.9 codifies role-change protocol (set flag + revoke families). D4.2 2FA-enroll clears the flag atomically. D1.8 includes the bootstrap admin CLI with out-of-band TOTP provisioning.
- **Provenance tag added**: M1 + M3 + M4 headers reference Mandatory #M2.

#### Mandatory Change #M3: INV-010 — encrypted email + unique btree

- **Status**: APPLIED
- **Before**: V1 D1.1 had AES-256-GCM encryption AND a unique btree on `users.email` — mutually exclusive with non-deterministic IV.
- **After**: D1.1 adds `email_blind_index BYTEA NOT NULL UNIQUE` = HMAC-SHA256(lower(email), blind_index_key). Lookup queries (D2.1, D2.4, D5.1, D4.8) key on `email_blind_index`; `email_ciphertext` returned for display/audit only. Blind-index key is rotated separately from data-encryption key (both in KMS). D1.4 crypto module adds HMAC-SHA256 utility. Cross-Cutting Security amended.
- **Provenance tag added**: M1 + M2 headers reference Mandatory #M3; Cross-Cutting Security section calls out #M3 explicitly.

#### Mandatory Change #M4: INV-011 — S3 object-lock vs GDPR erasure

- **Status**: APPLIED
- **Before**: V1 D4.6 audit log wrote raw IP, user agent, and `metadata_jsonb` that could contain PII; D4.7 archived to S3 with 7yr object-lock — irreconcilable with GDPR Art. 17 30-day erasure.
- **After**: D4.6 redacts PII at write-time — only opaque UUIDs, `ip_hash` (HMAC), `user_agent_hash` (HMAC), `request_id`, `event_type`, `result` survive into `audit_events`. D4.7 retention explicitly notes the immutable archive contains no PII. D5.8 documents GDPR Art. 17(3)(b) legal-basis-for-retention rationale. D4.8 erasure tombstones `email_blind_index`.
- **Provenance tag added**: M4 + M5 headers reference Mandatory #M4.

#### Mandatory Change #M5: INV-013 — NFR-001 latency sufficiency

- **Status**: APPLIED
- **Before**: V1 M2 acceptance measured p95 ≤ 200ms at 100 RPS — silent on cold/warm cache, Argon2id cold-process tax, RBAC cache misses.
- **After**: (a) D1.4 documents two Argon2id parameter tiers; ADR records which tier the target instance class meets. (b) D3.5 RBAC cache pre-warmed on deploy for top-100 active users; D5.4 readiness probe gated on cache warm-up. (c) M2 acceptance and M5 D5.6 load test exercise cold-Redis + warm-Redis segments AND cold-Argon2id + warm-Argon2id segments; all must satisfy NFR-001. Observability metrics include `rbac_cache_hit_ratio` and `argon2_hash_duration_seconds`.
- **Provenance tag added**: M1 + M2 + M5 headers reference Mandatory #M5.

#### Mandatory Change #M6: INV-015 — NFR-005 SLO sufficiency

- **Status**: APPLIED
- **Before**: V1 D5.5 had burn-rate alerts but no documented SLO scope (which endpoints, which deps).
- **After**: D5.5 includes the full SLO definition: (a) in-scope endpoints (login, refresh, OAuth callback, RBAC-protected `/me/*` reads); (b) excluded endpoints with graceful-degradation documentation (register, password-reset/request, oauth/start); (c) dependency exclusion policy; (d) documented dependency SLAs (SendGrid 99.95%, Google OIDC 99.95%, GitHub OAuth 99.9%, managed PG 99.99%, managed Redis 99.99%) and composite-availability arithmetic showing ~99.93% > 99.9% target. Observability "Dashboards & alerts" scoped to in-scope endpoints only.
- **Provenance tag added**: M5 header references Mandatory #M6; Cross-Cutting Observability references #M6 alert scoping.

---

## Post-Merge Validation

### Structural Integrity Check

| Check | Result |
|---|---|
| Heading hierarchy consistent (single H1, ordered H2/H3 nesting) | PASS — one H1 title; H2 sections (Executive Summary, Week-0 ADR, API Conventions, Milestones, Cross-Cutting Concerns, Risk Register, Success Criteria, Known Limitations, Provenance Footnote); H3 used for milestones (M1–M5) and Cross-Cutting subsections (Security, Observability, Testing Strategy); H4 used for "Deliverables" / "Acceptance Criteria" subheaders. No level gaps. |
| Milestone count preserved (5) | PASS — M1, M2, M3, M4, M5 |
| Milestone ordering preserved | PASS — M1 (Foundation+Skeleton) → M2 (Core Identity) → M3 (Federation+RBAC) → M4 (Hardening) → M5 (Admin+GA) |
| Timeline arithmetic consistent | PASS — 3 + 4 + 3 + 4 + 4 = 18 weeks; M1 retains 3 weeks per the walking-skeleton compromise (V2 sonnet's full-feature M1@3-weeks rejected as unrealistic); roadmap header states 18 weeks. |
| Deliverable IDs unique and contiguous within each milestone | PASS — D1.1–D1.8, D2.1–D2.10, D3.1–D3.9, D4.1–D4.8, D5.1–D5.10. New deliverables (D1.8, D3.9, D5.10) numbered as the next available index per milestone. |
| Section ordering logical | PASS — header → ADR → API conventions → milestones → cross-cutting → risk register → verification matrix → known limitations → provenance footnote |
| No orphaned sections | PASS |
| Provenance annotations present | PASS — document header has `<!-- Provenance: ... -->`; section-level annotations on Executive Summary, ADR, API Conventions, each milestone, each Cross-Cutting subsection, Risk Register, Verification Matrix |

**Structural integrity: PASS**

### Internal Reference Resolution

All references checked by content scan (`D\d+\.\d+|FR-0\d{2}|NFR-00[1-6]|R-00[1-4]|M[1-5]|INV-\d{3}`):

| Reference family | Defined targets | Citations | Status |
|---|---|---|---|
| D1.1–D1.8 | All 8 defined in M1 deliverables table | Cited in M2, M3, M4, M5, Cross-Cutting, Risk Register | All resolve |
| D2.1–D2.10 | All 10 defined in M2 deliverables table | Cited in M3 dependencies, M4 dependencies, M5, Risk Register | All resolve |
| D3.1–D3.9 | All 9 defined in M3 deliverables table | Cited in M4, M5, Risk Register | All resolve |
| D4.1–D4.8 | All 8 defined in M4 deliverables table | Cited in M5, Cross-Cutting, Risk Register | All resolve |
| D5.1–D5.10 | All 10 defined in M5 deliverables table | Cited within M5, Provenance Footnote, Known Limitations | All resolve |
| FR-001–FR-012 | All 12 defined in Verification Matrix | Cited in milestone "source-spec coverage" sections | All resolve |
| NFR-001–NFR-006 | All 6 defined in Verification Matrix | Cited across milestones and Cross-Cutting | All resolve |
| R-001–R-004 | All 4 defined in Risk Register | Cited in milestones and Cross-Cutting | All resolve |
| M1–M5 | 5 milestones defined under "## Milestones" | Cited via "Dependencies: M1, M2..." rows | All resolve |
| INV-001/003/010/011/013/015 | Resolved by #M1–#M6 (referenced inline) | Mentioned in body + Known Limitations | All resolve |
| Cross-doc links (./adversarial/*.md) | Resolved against sibling directory structure | 6 links in Provenance Footnote | All resolve (verified by path existence: variant-1, variant-2, diff-analysis, debate-transcript, invariant-probe, refactor-plan all present in `./adversarial/`) |

**Internal references: PASS** (0 broken, 0 dangling)

### Contradiction Re-Scan

Compared to baseline contradictions documented in diff-analysis.md (V1 vs V2 conflict points C-001 through C-018):

| Potential new contradiction | Status |
|---|---|
| Argon2id default tier `m=64MB` (D1.4) vs fallback `m=46MB` (D1.4, M5) | NOT a contradiction — ADR explicitly documents both tiers as conditional alternatives based on target instance class measurement |
| Roles `admin/user` (D3.5) vs older V1 mention of `admin/user/support` | RESOLVED — all references in merged doc are `admin/user`; `support` removed |
| Status `active/suspended/deactivated` (D3.5) vs role taxonomy | NOT a contradiction — orthogonal axes by design (Change #11); RBAC checks role, status middleware checks status |
| `email` unique column (V1 D1.1 original) vs blind-index (#M3) | RESOLVED — merged doc has only the blind-index version; original V1 wording removed |
| Audit `metadata_jsonb` containing PII (V1 D4.6 original) vs PII redaction at write (#M4) | RESOLVED — merged doc has redaction language only |
| 99.9% SLO covering all endpoints (V1 D5.5 original implicit) vs scoped SLO (#M6) | RESOLVED — merged doc has explicit in-scope/excluded endpoint lists |
| Pagination `default 50 / max 200` (Change #5) vs any other page-size mention | CONSISTENT — single canonical statement in API Conventions; all deliverable references defer to it |
| Endpoint paths `/auth/*` (V1 original) vs `/api/v1/auth/*` (Change #1) | RESOLVED — all paths in merged doc are versioned |
| M1 duration "3 weeks" + walking-skeleton vs V2 sonnet's "M1 ships 7 features in 3 weeks" | NOT a contradiction — walking-skeleton is a thin endpoint (Change #2), not full M2 surface; M1 remains 3 weeks with a clear scope boundary |
| Refresh-token TTL 30 days (V1 D2.4) vs V2's 7 days | RESOLVED per refactor plan "Changes NOT Being Made" — V1's 30-day TTL kept with family-revocation mitigating blast radius |

**No NEW contradictions introduced by the merge.** All previously contradictory points are unified to a single canonical statement (typically the variant retained by the refactor plan, or the explicit resolution from #M1–#M6).

---

## Summary

| Metric | Count |
|---|---|
| Planned changes | 17 |
| Applied | 17 |
| Skipped | 0 |
| Failed | 0 |
| HIGH-severity invariants resolved | 6 / 6 (INV-001, INV-003, INV-010, INV-011, INV-013, INV-015) |
| MEDIUM/LOW invariants addressed inline (non-blocking) | 10 (documented in Known Limitations) |
| New contradictions introduced | 0 |
| Internal references broken | 0 |
| Structural integrity | PASS |
| Output line count | 386 (vs V1 baseline 277; +109 lines, within 350-450 target band) |

**Overall merge status: SUCCESS** — all 17 refactor-plan changes applied; all 6 HIGH-severity invariants concretely resolved in the body of the merged document; no new contradictions; all internal references resolve.
