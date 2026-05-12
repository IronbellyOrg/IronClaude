# ValidationReport.md -- Tasklist v1.1 Stage 7-10

**Source roadmap:** `.dev/test-fixtures/results/test24-tdd-prd/roadmap.md` (527 lines)
**Tasklist bundle:** `.dev/releases/current/v1.1/` (index + 6 phase files, 108 tasks)
**Validation date:** 2026-04-20
**Validation method:** Structural self-check + 2 parallel fidelity agents + source grep cross-check
**Verdict:** PATCH_REQUIRED (fidelity drift on 12 constraint values)

---

## Structural Self-Check (Stage 6) -- PASS

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Files emitted | 7 (index + 6 phases) | 7 | PASS |
| Phase task counts | 24/19/13/18/13/21 = 108 | 24/19/13/18/13/21 = 108 | PASS |
| R-ID coverage | R-001..R-107 (107 unique) | 107 unique | PASS |
| D-ID coverage | D-0001..D-0108 (108 unique) | 108 unique | PASS |
| Tier distribution (index vs files) | STRICT 57 / STANDARD 50 / EXEMPT 1 | STRICT 57 / STANDARD 50 / EXEMPT 1 | PASS |
| Phase 2 Clarification | T02.01 EXEMPT, D-0025, no R-ID | Present and correct | PASS |
| Checkpoint cadence | every 5 + end-of-phase | Phase 1 has 1 redundant closing checkpoint | MINOR |
| Phase heading format | `# Phase N -- Name` em-dash | Conformant | PASS |

Minor: Phase 1 has "Checkpoint: Phase 1 / Tasks 21-24 + End of Phase" immediately followed by a second "Checkpoint: End of Phase 1" block. Non-blocking; historical artifact from an earlier cadence variant.

---

## Fidelity Drift Findings (Stage 7) -- 12 PATCH ITEMS

Each finding: ID | File / Task | Tasklist value | Roadmap source | Patch direction

| # | File / Task | Tasklist value | Roadmap source | Patch |
|---|-------------|----------------|----------------|-------|
| D1 | phase-1 / T01.01 D-0001 | columns `consent_flag, consent_ts` | DM-001 (line 90): `consent_accepted_at:timestamptz`, `consent_version:varchar` | Rename columns + add `consent_version` field |
| D2 | phase-3 / T03.04, T03.10 | reset-request returns `202` | FR-AUTH-006 (line 232) + API-RESET-REQ (line 238): "Always returns 200" | Change `202` -> `200` |
| D3 | phase-3 / T03.10 | rate-limit `5/min per IP` | API-RESET-REQ (line 238): "3/hour/email + 10/hour/IP" | Replace rate policy |
| D4 | phase-3 / T03.06 | cleanup `expires_at < now() - 1h` | DM-RESET cleanup (line 249): "expires_at < now - 7d" | Change `1h` -> `7d` |
| D5 | phase-4 / T04.07 | cookie `SameSite=Lax; Path=/auth` | SEC-HTTPONLY (line 294): `SameSite=Strict; Path=/auth/refresh` | Update cookie attributes |
| D6 | phase-6 / T06.04 | rollout `1% -> 10% -> 50% -> 100%` | FEAT-FLAG-NEWLOGIN (line 373): `0% -> 1% -> 5% -> 25% -> 50% -> 100%` with SLO-green >=60min + error-rate delta <0.5% | Replace stages + add advancement criteria |
| D7 | phase-6 / T06.11 | ALERT-LOGIN-FAIL `>5% for 5m` | ALERT-LOGIN-FAIL (line 380): `>30% sustained 10min` | Update threshold + window |
| D8 | phase-6 / T06.13 | ALERT-REDIS `redis_up == 0 for 2m` | ALERT-REDIS (line 382): `redis_up == 0 for >1min` | Change `2m` -> `1m` |
| D9 | phase-6 / T06.14 | Trigger = `ALERT-LATENCY firing 10m` (p95 >300ms) | ROLLBACK-AUTO-LATENCY (line 383): `p95 >500ms for 15min` | Replace trigger condition |
| D10 | phase-6 / T06.15 | threshold `>2% for 5m` | ROLLBACK-AUTO-ERR (line 384): `>1% for 10min` | Change threshold + window |
| D11 | phase-6 / T06.17 | window missing | ROLLBACK-AUTO-DATA (line 386): `>5% for 5min` | Add explicit 5-minute window |
| D12 | phase-6 / T06.21 | 5 stakeholder sign-offs (Product, Security, SRE, Legal, Support) | OPS-011 (line 390): 3 sign-offs (sec-reviewer + eng-manager + product) | Reduce to 3 required sign-offs |

---

## Additional Minor Fidelity Notes (non-blocking, documented for record)

| Note | Detail |
|------|--------|
| M1 | T06.06 retention says `15 days hot`; roadmap OPS-001 says `30d metrics`. Correct to 30d. |
| M2 | T06.07 Tempo retention says `14 days hot`; roadmap OPS-002 says `7-day retention` + `10% sampling + 100% 5xx + 100% refresh-replay`. Correct both. |
| M3 | T06.08 Loki retention says `30 days hot`; roadmap OPS-003 says `14d hot + 90d cold`. Correct. |
| M4 | T06.10 OPS-005 missing `complaint rate <0.1%`. Add. |
| M5 | T06.16 ROLLBACK-AUTO-REDIS missing explicit `>3min` duration. Add. |

---

## Confirmations (verified against roadmap)

- JWT RS256 2048-bit carried in T02.03.
- bcrypt cost=12 carried in T01.04 + T01.14.
- Redis 5-cap LRU carried in T02.02.
- Lockout 5/15min carried in T01.11 + T05.05.
- CONFLICT-2 (register 201, no auto-login) carried in T01.08 + T01.10.
- NFR-GDPR-CONSENT wiring through T01.06/T01.16/T01.21 (column names aside).
- Clarification Task T02.01 correctly marked EXEMPT.
- HttpOnly + in-memory access-token pattern carried in T04.07 + T04.08.
- WCAG AA in T04.12.
- 4 rollback triggers + chaos drills in T06.14-T06.17.
- 99.9% SLO in T06.19.
- Critical Path Override applied on all auth/security/migrations paths.
- All 107 roadmap items mapped to tasks; 108 deliverables registered.

---

## Patch Execution (Stage 9)

See `PatchChecklist.md` for the ordered patch list. Execution mode: direct Edit calls (in-place, per protocol Stage 9). After patching, Stage 10 spot-check results are appended below.

---

## Spot-Check Verification Results (Stage 10)

**Verification date:** 2026-04-20
**Method:** Direct `Grep` of patched files for (a) absence of drifted values and (b) presence of roadmap-aligned values.
**Verdict:** **PASS** -- all 17 patches landed; no residual drift on scanned tokens.

### Per-patch verification

| Patch | File | Old token (expected gone) | New token (expected present) | Status |
|-------|------|---------------------------|------------------------------|--------|
| P1 | phase-1-tasklist.md | `consent_flag` / `consent_ts` | `consent_accepted_at` + `consent_version` (13 hits) | PASS |
| P2a | phase-3-tasklist.md (T03.04) | `202` (3 sites) | `200` in deliverable, step 4, timing check | PASS |
| P2b | phase-3-tasklist.md (T03.10 + checkpoint) | `202` (3 sites) | `200` at line 240, 443, 451; `200 response for every request` present | PASS |
| P3 | phase-3-tasklist.md (T03.10 rate-limit) | `5/min per IP` | `3/hour per email + 10/hour per IP` + 429 AC updated | PASS |
| P4 | phase-3-tasklist.md (T03.06 cleanup) | `< now() - 1h` | `< now() - 7 days` | PASS |
| P5 | phase-4-tasklist.md (T04.07 cookie) | `SameSite=Lax` + `Path=/auth` (bare) | `SameSite=Strict` + `Path=/auth/refresh` (2 hits) | PASS |
| P6 | phase-6-tasklist.md (T06.04 rollout) | `1% -> 10% -> 50% -> 100%` | `0% -> 1% -> 5% -> 25% -> 50% -> 100%` + `SLO-green >=60min + error-rate delta <0.5%` | PASS |
| P7 | phase-6-tasklist.md (T06.11 ALERT-LOGIN-FAIL) | `> 5% for 5m` | `>30% sustained 10min` (deliverable + step + AC) | PASS |
| P8 | phase-6-tasklist.md (T06.13 ALERT-REDIS) | `redis_up == 0 for 2m` / `> 2m` | `redis_up == 0 for >1min` + `>1min` AC | PASS |
| P9 | phase-6-tasklist.md (T06.14 ROLLBACK-AUTO-LATENCY) | `ALERT-LATENCY firing 10m` | `p95 >500ms for 15min per ROLLBACK-AUTO-LATENCY` | PASS |
| P10 | phase-6-tasklist.md (T06.15 ROLLBACK-AUTO-ERR) | `> 2% for 5m` | `>1% for 10min` (why + AC) | PASS |
| P11 | phase-6-tasklist.md (T06.17 ROLLBACK-AUTO-DATA) | `> 5%` (window missing) | `>5% sustained 5 minutes` | PASS |
| P12 | phase-6-tasklist.md (T06.21 OPS-011) | 5 stakeholder sign-offs | `sec-reviewer, eng-manager, product` + `3 required sign-offs` | PASS |
| P13 | phase-6-tasklist.md (T06.06 OPS-001) | `15 days hot` | `30 days metrics per OPS-001` | PASS |
| P14 | phase-6-tasklist.md (T06.07 OPS-002) | `14 days hot` only | `7 days retention` + sampling `10% default + 100% 5xx + 100% refresh-replay` | PASS |
| P15 | phase-6-tasklist.md (T06.08 OPS-003) | `30 days hot, 12 months cold` | `14 days hot + 90 days cold per OPS-003, 12 months archive via OPS-004` | PASS |
| P16 | phase-6-tasklist.md (T06.10 OPS-005) | AC missing complaint rate | `complaint rate <0.1%` added to DMARC AC | PASS |
| P17 | phase-6-tasklist.md (T06.16 ROLLBACK-AUTO-REDIS) | no explicit duration | `unreachable >3min` added to Why + AC | PASS |

### Cross-phase grep sweep (final sanity)

| Old-value pattern | Hits (expected 0) | Notes |
|-------------------|-------------------|-------|
| `consent_flag` / `consent_ts` | 0 | P1 clean. |
| `202` in phase-3-tasklist.md | 0 | P2a + P2b clean. |
| `5/min per IP` / `< now() - 1h` | 0 | P3 + P4 clean. |
| `SameSite=Lax` / `Path=/auth[^/]` | 0 | P5 clean. |
| `1% -> 10% -> 50%` / `redis_up == 0 for 2m` / `> 2% for 5m` / `> 5% for 5m` / `15 days hot` / `30 days hot` | 0 (only new-value substring overlap for `14 days hot` within `14 days hot + 90 days cold`, expected) | P6-P17 clean. |

### Minor structural variance (non-blocking, documented)

- Phase files 1-4 use bare `Checkpoint:` headings; phases 5-6 use `### Checkpoint:`. The Sprint CLI phase-file regex tolerates both; no patch required. Flagged for a future cosmetic cleanup pass.
- Phase 1 retains a duplicate `Checkpoint: End of Phase 1` block (noted in Stage 6 self-check). Historical artifact from the every-5 + end-of-phase cadence overlap on a 24-task phase. Non-blocking.

---

## Final Verdict

**ACCEPTED FOR SPRINT EXECUTION**

All 12 primary fidelity drift items (D1-D12) resolved. All 5 minor notes (M1-M5) resolved. Structural self-check (Stage 6) remains PASS. Generated tasklist bundle at `.dev/releases/current/v1.1/` is now roadmap-aligned and Sprint CLI-ready.

Next step (out of scope for this protocol run): the user may invoke `superclaude sprint run .dev/releases/current/v1.1/tasklist-index.md` to begin execution.

