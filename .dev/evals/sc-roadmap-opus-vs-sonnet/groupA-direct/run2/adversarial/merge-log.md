# Merge Log: Variant 1 base + Variant 2 additions + Invariant Patches

## Metadata

- **Merge date**: 2026-05-22
- **Base variant**: Variant 1 (opus / default persona)
- **Source variant for additions**: Variant 2 (sonnet / default persona)
- **Refactoring plan**: `adversarial/refactor-plan.md`
- **Output**: `merged-roadmap.md`
- **Pipeline**: `/sc:adversarial` Step 5 (merge-executor)
- **Total changes applied**: 24 planned + 8 supplementary = 32 edits across 23 logical patches

---

## Per-Change Execution Log

### Section A — V2-Additive Incorporations

| ID | Target section | Source | Before (summary) | After (summary) | Status |
|----|----------------|--------|------------------|-----------------|--------|
| A1 | New section "FR Coverage Matrix" | V2 lines 342–358 | No FR matrix in V1 | New section inserted after "Success Criteria → Milestone Mapping" with 12 FRs mapped to merged D{M}.{N} numbering | applied |
| A2 | Milestone Map + new Schedule subsection | V2 lines 12–22, 36 | V1 Milestone Map had no Duration column or critical path | Added Duration column (M1=3w, M2..M7=2w) + Critical Path annotation; new Schedule subsection in Overview | applied |
| A3 | D6.1 (User profile management) | V2 D3.2 line 135 | V1 D6.1 silent on email change | Added `PATCH /v1/users/me/email` with re-verification via D2.1 path; `pending_email_changes` table referenced (encrypted per P-3, hash-indexed per P-7) | applied |
| A4 | New deliverable D4.3 in M4 | V2 D5.3 line 211 | No consent ledger in V1 | New D4.3 "Consent ledger" with `user_consents` table + policy_version + GDPR Art 7 rationale | applied |
| A5 | D6.3 (Account deactivation) | V2 D5.3 lines 209–211 | V1 erasure used "overwrite encrypted columns with NULL" | Replaced with `erased_<uuid>@erased.local` for email, NULL for display_name/phone/address, `actor_user_id = ERASED_<uuid>` in audit_events | applied |
| A6 | D5.2 (API rate limiting) | V2 D4.2 line 171 | No burst-detection in V1 | Added 1000 req/min IP → 1h auto-block + PagerDuty webhook within 5s | applied |
| A7 | D5.3 (Audit logging) | V2 D5.1 line 195 | V1 had hash chain but no GRANT restriction | Added REVOKE UPDATE, DELETE for `auth_app` role; DBA-only repair path | applied |
| A8 | D3.1 (OAuth2 integration) | V2 D2.1 line 95 | No `/health/oauth` endpoint in V1 | Added `GET /health/oauth` polling Google OIDC + GitHub /zen every 60s; lagging-indicator contract documented (Patch-additional-5) | applied |
| A9 | D2.1 (Registration) | V2 D1.1 line 46 | No disposable-email check in V1 | Added `disposable-email-domains` npm list (v1.0.x) with quarterly dependabot refresh | applied |
| A10 | D2.1 (Registration) | V2 D1.1 line 46 | No prune cron in V1 | Added `prune-unverified-users` cron at 03:00 UTC with +1 min buffer per INV-012 | applied |
| A11 | D3.2 (Session management) | V2 D1.3 line 78 + D1.2 line 62 | No session cap or concurrent-login detection in V1 | Added 50-session cap with eviction → denylist publish; 60s concurrent-login window with notification | applied |
| A12 | D6.1 (User profile management) | V2 D3.2 line 135 | No avatar upload in V1 | Added `POST /v1/users/me/avatar` with ≤2 MiB cap + magic-byte check + Sharp v0.33 resize | applied |
| A13 | New section "Technology & Version Pinning" | V2 lines 362–375 | No tech-pinning table in V1 | Inserted new section after FR Coverage Matrix, augmented with V1-specific entries (Patroni, Sentinel, Vault, simple-oauth2, otplib, pgcrypto, node-pg-migrate, Semgrep, Sharp, K8s, etc.) | applied |
| A14 | D1.3 (Secrets management & TLS) | V2 D5.3 line 219 | V1 had testssl.sh only | Added `nmap --script ssl-enum-ciphers -p 443` acceptance test complementary to testssl.sh | applied |
| A15 | D7.4 (Reliability gate) | V2 D7.3 lines 284–285 | No Prometheus alerting in V1 D7.4 | Added `/metrics` exposition + Alertmanager rules (auth_error_rate P2, auth_p99_latency P2, auth_denylist_publish_lag P1 binding to ≤60s claim) | applied |

### Section B — Invariant Patches (HIGH severity required)

| ID | Resolves | Target section | Risk | Status | Notes |
|----|----------|----------------|------|--------|-------|
| P-1 | INV-001 + INV-009 + INV-022 | D3.2 (session management) + D7.4 (chaos test) | HIGH | applied | **Removed V1's pub/sub denylist** entirely; replaced with TTL-keyed `SETEX denylist:<jti>` + per-pod cache TTL ≤30s + clock skew ≤5s + Sentinel reconnect ≤10s = ≤50s ≤ 60s budget. AOF persistence + Sentinel chaos test added to D7.4. **Note**: D4.2 retains a `perms:invalidated` pub/sub event for the permission cache — this is per-user-id invalidation only, NOT the access-token denylist; the two are now distinct mechanisms. |
| P-2 | INV-023 | D1.2 (schema) + D1.3 + D1.1 v2-follow-up | MEDIUM | applied | Clarified per-request KMS `GenerateDataKey` unwrap; plaintext-DEK held in request-scoped memory, zeroed in try/finally; `pg_log_statement = off` enforced; `pg_tde`/Vault Transit tracked as v2 follow-up in D1.1 |
| P-3 | INV-002 + INV-005 + INV-024 | D1.2 (new PII Encryption Inventory subsection) + D7.2 (new acceptance test) | MEDIUM | applied | Inventory table enumerates 12 columns across 11 tables incl. V2-added `pending_email_changes` + `user_consents`; CI grep test in D7.2 catches plaintext-email leak |
| P-4 | INV-004 + INV-019 | D5.3 (audit logging) | MEDIUM | applied | Added `pg_advisory_xact_lock('audit_events'::regclass::oid)` for single-writer serialization; DBA repair runbook with 15-min investigation SLA + 60-min repair SLA |
| P-5 | INV-010 | Schedule subsection in Overview + Milestone Map | LOW | applied | Replaced V2's "~13 weeks (M2//M3 parallel)" with corrected text: 15w sequential / ~13w with M3//M4 parallel; critical path M1→M2→M3→M5→M6→M7 (or M1→M2→M4→M5→M6→M7) |
| P-6 | INV-019 (operational dead-end) | D5.3 (covered jointly with P-4) | MEDIUM | applied | Same edit location as P-4; DBA repair runbook entry. Logically distinct concern but consolidated edit. |
| P-7 | INV-021 | D1.2 (schema) + D2.1 (registration insert) + D2.2 (login lookup) | HIGH | applied | `email_lookup_hash BYTEA NOT NULL` via HMAC-SHA256 with separate KMS `lookup_key` (independent rotation cadence); unique index `users_email_lookup_hash_uidx`; defensive post-decrypt compare for hash-collision rejection; `EXPLAIN ANALYZE` acceptance criterion in D1.2 |
| P-8 | INV-008 | D5.2 (rate limiting) — paired with Change A6 | LOW | applied | `RATE_LIMIT_IP_ALLOWLIST` env var with CIDR support; allowlist exempts only IP-wide auto-block (per-account lockout + per-route limits still apply); SIGHUP reload + audited mutations |
| P-9 | INV-016 | D6.3 (deactivation workflow) — paired with Change A5 | LOW | applied | Erasure path guarded by `WHERE … AND users.erased_at IS NULL` + atomic `SET users.erased_at = now()` in same transaction as anonymization writes |

### Additional Patches

| ID | Resolves | Target section | Status |
|----|----------|----------------|--------|
| Patch-additional-1 | INV-007 (MEDIUM) | D3.3 (cookie hardening) + D7.3 deployment-guard reference | applied — admin SPA must share registrable domain; pre-cutover runbook validates |
| Patch-additional-2 | INV-011 (MEDIUM) | D5.2 (rate limiting) | applied — lockout × burst-block composition: `max(account_lockout_remaining, ip_burst_block_remaining)`; both controls audited |
| Patch-additional-3 | INV-013 (MEDIUM) | D4.1 (role and permission model) | applied — `unverified_user` role with permissions `{user.profile.read.own, user.profile.complete-verification}`; full `user` role granted on `email_verified_at` set |
| Patch-additional-4 | INV-015 (LOW) | D5.3 (audit logging) | applied — genesis row `prev_hash = '0' × 64`; cron emits `audit.fresh-deployment` on empty table |
| Patch-additional-5 | INV-020 (LOW) | D3.1 (OAuth2 integration) | applied — `/health/oauth` is lagging indicator at 60s cadence; live-request fallback is authoritative for routing |
| Patch-additional-6 | INV-003 (MEDIUM) | D3.2 — covered by Change A11 integration | applied — eviction publishes denylist entry for evicted refresh token's last access-token `jti` |
| Patch-additional-7 | INV-012 (LOW) | D2.1 — covered by Change A10 integration | applied — `+1 min` buffer in prune cron query |
| Patch-additional-8 | INV-006 (LOW) | D2.1 — covered by Change A9 integration | applied — quarterly dependabot PR with regression-test sample |

---

## Post-Merge Validation

### Structural integrity

- [x] Document opens with H1 (`# Roadmap: User Authentication System`).
- [x] M1–M7 all present and in canonical order.
- [x] No heading-level gaps (no H2 followed directly by H4).
- [x] No orphaned subsections.
- [x] All deliverables D{M}.{N} preserved + 1 new (D4.3) per Change A4.
- [x] Sections present: Overview, Schedule, Milestone Map, M1–M7, Dependency
      Graph, Risk-to-Milestone Mapping, NFR Enforcement Strategy,
      Out-of-Scope Reaffirmation, FR Coverage Matrix, Technology & Version
      Pinning, Success Criteria → Milestone Mapping, Merged Postscript.

### Internal reference resolution

Scan for cross-references and verify each resolves:

| Reference pattern | Count | Resolved | Notes |
|-------------------|-------|----------|-------|
| `D{M}.{N}` deliverable refs | 60+ | all resolve | D1.1, D1.2, D1.3, D2.1, D2.2, D2.3, D3.1, D3.2, D3.3, D4.1, D4.2, D4.3, D5.1, D5.2, D5.3, D6.1, D6.2, D6.3, D7.1, D7.2, D7.3, D7.4 — all defined |
| `R-001..R-004` risk refs | 8 | all resolve | All four risks have mitigation rows in Risk-to-Milestone Mapping |
| `FR-001..FR-012` refs | 24+ | all resolve | All 12 FRs have rows in FR Coverage Matrix |
| `NFR-001..NFR-006` refs | 18+ | all resolve | All 6 NFRs have rows in NFR Enforcement Strategy |
| `Patch P-1..P-9` refs | 25+ | all resolve | All 9 patches defined in change log; cross-referenced in roadmap body |
| `Patch-additional-1..8` refs | 9 | all resolve | All 8 additional patches applied in body |
| `INV-NNN` refs | 17 | all resolve | Each cited invariant has a corresponding patch reference |
| `Change A1..A15` refs | 18 | all resolve | All 15 changes applied with provenance comments |

**Reference resolution rate**: 179 / 179 (100%).

### Contradiction re-scan

Verify no NEW contradictions introduced vs the pre-merge variants:

- [x] **TTL-keyed denylist (replaces V1 pub/sub)** — this is per Patch P-1
      and resolves INV-001/INV-009/INV-022; it is intentional, not a new
      contradiction. The merged document removes V1's pub/sub prose from
      D3.2 entirely.
- [x] **D4.2 `perms:invalidated` pub/sub** — retained for permission-cache
      invalidation (per-user-id key DEL). This is distinct from the
      access-token denylist mechanism (TTL-keyed in D3.2). Both mechanisms
      coexist by design; D3.2 explicitly notes the separation.
- [x] **Erasure pattern (`erased_<uuid>` vs NULL)** — per Change A5;
      intentional replacement preserving audit hash-chain integrity.
- [x] **DB GRANT INSERT-only** — per Change A7; complementary to V1's hash
      chain (defence-in-depth). DBA repair runbook (P-4/P-6) addresses the
      operational dead-end this would otherwise create.
- [x] **Schedule (15w sequential / ~13w parallel)** — per Patch P-5;
      corrects the ungrounded 13-week claim that did not survive the
      V1-ordering merge.
- [x] **`pgcrypto` key residency** — Patch P-2 clarifies (does not
      contradict) that DEK is unwrapped per-request; original "out of memory"
      claim is appropriately narrowed.
- [x] **Account lockout duration** — V1's 15 min retained; V2's 30 min not
      adopted. Lockout × burst-block composition (Patch-additional-2)
      documents the interaction with the 1-hour IP block.

**New contradictions introduced**: 0.

### Invariant patch coverage (HIGH severity)

| INV ID | Resolved by | Status |
|--------|-------------|--------|
| INV-001 | P-1 | resolved |
| INV-002 | P-3 | resolved |
| INV-005 | P-3 | resolved |
| INV-009 | P-1 | resolved |
| INV-010 | P-5 | resolved |
| INV-021 | P-7 | resolved |
| INV-022 | P-1 | resolved |
| INV-023 | P-2 | resolved |
| INV-024 | P-3 | resolved |

**HIGH UNADDRESSED count after merge**: 0 / 9 (was 9 / 9 pre-merge).

### Provenance annotations

- [x] Document-header Provenance block present (3-line HTML comment).
- [x] Every modified section carries `<!-- Source: Base (V1, modified) — Change/Patch ID: X -->`
      or `<!-- Source: Variant 2 (sonnet, default), Section <ref> — merged per Change X -->`.
- [x] Unchanged base sections marked `<!-- Source: Base (V1, original) -->`.

### Output statistics

- Merged roadmap: 511 lines (target: 500–700).
- All 15 V2-additive incorporations applied.
- All 9 invariant patches (HIGH severity) applied.
- All 8 supplementary patches applied.
- 0 changes deferred or escalated to orchestrator.

---

## Escalations to Orchestrator

None. All planned changes applied as specified in the refactoring plan.

---

## Merge Status: COMPLETE

Convergence achieved. The merged roadmap is ready for downstream consumption
(tasklist generation, sprint planning, or human review).
