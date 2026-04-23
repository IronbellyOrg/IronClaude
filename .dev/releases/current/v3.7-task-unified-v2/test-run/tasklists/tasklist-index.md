# TASKLIST INDEX -- User Authentication Service (test6-spec)

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | User Authentication Service (test6-spec) |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-04-23 |
| TASKLIST_ROOT | `.dev/releases/current/v3.7-task-unified-v2/test-run/tasklists/` |
| Total Phases | 5 |
| Total Tasks | 31 |
| Total Deliverables | 26 |
| Complexity Class | MEDIUM |
| Primary Persona | architect |
| Consulting Personas | backend, security, devops |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `TASKLIST_ROOT/tasklist-index.md` |
| Phase 1 Tasklist | `TASKLIST_ROOT/phase-1-tasklist.md` |
| Phase 2 Tasklist | `TASKLIST_ROOT/phase-2-tasklist.md` |
| Phase 3 Tasklist | `TASKLIST_ROOT/phase-3-tasklist.md` |
| Phase 4 Tasklist | `TASKLIST_ROOT/phase-4-tasklist.md` |
| Phase 5 Tasklist | `TASKLIST_ROOT/phase-5-tasklist.md` |
| Execution Log | `TASKLIST_ROOT/execution-log.md` |
| Checkpoint Reports | `TASKLIST_ROOT/../checkpoints/` |
| Evidence Directory | `TASKLIST_ROOT/../evidence/` |
| Artifacts Directory | `TASKLIST_ROOT/../artifacts/` |
| Validation Reports | `TASKLIST_ROOT/../validation/` |
| Feedback Log | `TASKLIST_ROOT/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Foundation, Data Layer, Key Management | T01.01-T01.06 | STRICT: 5, CHECKPOINT: 1 |
| 2 | phase-2-tasklist.md | Core Authentication Primitives | T02.01-T02.05 | STRICT: 3, STANDARD: 1, CHECKPOINT: 1 |
| 3 | phase-3-tasklist.md | Authentication Service and Endpoints | T03.01-T03.11 | STRICT: 9, CHECKPOINT: 2 |
| 4 | phase-4-tasklist.md | NFRs and Observability | T04.01-T04.05 | STRICT: 1, STANDARD: 3, CHECKPOINT: 1 |
| 5 | phase-5-tasklist.md | Hardening, Validation, Release | T05.01-T05.05 | STRICT: 3, STANDARD: 1, CHECKPOINT: 1 |

## Source Snapshot

- Source roadmap: `.dev/test-fixtures/results/test6-spec/roadmap.md` (MEDIUM 0.6 complexity, adversarial convergence 0.82)
- 5 milestones mapped 1:1 to phases (M1..M5 → Phase 1..Phase 5)
- Roadmap is a stateless JWT authentication service spanning registration, login, token refresh, profile, and password reset
- Architectural constraints: RS256 (2048-bit), bcrypt cost=12, httpOnly refresh cookie scoped `/auth/refresh`, stateless JWT, reversible migrations
- Phase 3 (M3) contains the richest surface (28 roadmap items across 3 weeks) — a mid-phase checkpoint is emitted per Wave 4 contract
- 99.9% availability target; all security-domain tasks marked STRICT with Critical Path Override

## Deterministic Rules Applied

- Phase numbering is sequential (1..5) per Section 4.3 — no gaps
- Every task ID follows `T<PP>.<TT>` zero-padded format
- Checkpoints are numbered tasks per Wave 4 contract (`### T<PP>.<NN> -- Checkpoint:`)
- End-of-phase checkpoint appears as the last task in each phase file
- Phase 3 includes a mid-phase checkpoint (`T03.06 -- Checkpoint: M3 Authenticated Flow Verified`) — triggered by M3's 28-item size
- Tier classification: security/auth/migration/crypto items → STRICT with Critical Path Override; infra/observability items → STANDARD
- Deliverable IDs `D-0001..D-0026` assigned in task-order, globally unique
- Confidence bars use the standard `[████████--] XX%` format
- Every task has exactly 4 Acceptance Criteria bullets and 2 Validation bullets
- Artifact paths use only `TASKLIST_ROOT/artifacts/D-####/` placeholders (no invented code paths)
- Risk drivers are matched keywords only; no invented categories
- MCP requirements propagate from tier (STRICT → Required: Sequential, Serena)

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | COMP-007 AuthTablesMigration: Migration module orchestrating creation of users and refresh_tokens tables with reversible down-migration |
| R-002 | Phase 1 | MIG-001 users table migration: Forward/backward migration creating users table with unique email index |
| R-003 | Phase 1 | MIG-002 refresh_tokens table migration: Forward/backward migration creating refresh_tokens with FK and indexes |
| R-004 | Phase 1 | COMP-008 UserRepository: Persistence-layer abstraction for UserRecord CRUD |
| R-005 | Phase 1 | INFRA-001 RSA key pair generation: Tooling to generate RS256-compatible RSA key pair (2048-bit min) |
| R-018 | Phase 2 | COMP-004 PasswordHasher: bcrypt wrapper exposing hash and compare with configurable cost factor |
| R-019 | Phase 2 | COMP-003 JwtService: RS256 sign and verify wrapper supporting multi-key verification during rotation |
| R-020 | Phase 2 | COMP-002 TokenManager: Issues, rotates, and revokes AuthTokenPair with refresh-token replay detection |
| R-021 | Phase 2 | VALID-001/002: Password policy + email format validators (pure utilities) |
| R-035 | Phase 3 | COMP-001 AuthService: Core orchestrator coordinating login, register, refresh, profile, and reset flows |
| R-036 | Phase 3 | COMP-005 AuthMiddleware: Bearer token extraction and verification in request pipeline |
| R-037 | Phase 3 | FR-AUTH.1 + API-001: POST /auth/login endpoint |
| R-038 | Phase 3 | FR-AUTH.2 + API-002: POST /auth/register endpoint |
| R-039 | Phase 3 | FR-AUTH.3 + API-003: POST /auth/refresh with rotation |
| R-040 | Phase 3 | FR-AUTH.4 + API-004: GET /auth/me profile retrieval |
| R-041 | Phase 3 | FR-AUTH.5 + API-005/006: Password reset request + confirm endpoints |
| R-042 | Phase 3 | RATE-001 Login rate-limit middleware: 5 attempts per minute per IP |
| R-043 | Phase 3 | ERR-001 + DTO-001: Uniform auth error contract + DTO field whitelist |
| R-063 | Phase 4 | OPS-001 APM instrumentation: Distributed tracing + p95/p99 metrics for every /auth/* route |
| R-064 | Phase 4 | OPS-002 Health check endpoint: GET /healthz with DB + secrets + key cache |
| R-065 | Phase 4 | OPS-004 k6 load test: Repeatable load profile against staging, gates p95<200ms |
| R-066 | Phase 4 | SEC-001 bcrypt cost benchmark: CI bench proving cost=12 within 200-350ms band |
| R-073 | Phase 5 | SC-1..SC-7 validation suite: every mechanically-verifiable success criterion against staging |
| R-074 | Phase 5 | SEC-003 Penetration smoke test: enumeration, brute force, replay, JWT attacks |
| R-075 | Phase 5 | FF-001 Feature flag rollout plan: canary→25%→100% with kill-switch |
| R-076 | Phase 5 | OPS-006 Rollback procedure rehearsal: CFG-002=false + MIG-003 down in staging |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | AuthTablesMigration orchestrator | STRICT | Sub-agent | `artifacts/D-0001/spec.md`, `artifacts/D-0001/evidence.md` | M | High |
| D-0002 | T01.02 | R-002 | users table migration | STRICT | Sub-agent | `artifacts/D-0002/spec.md`, `artifacts/D-0002/evidence.md` | S | High |
| D-0003 | T01.03 | R-003 | refresh_tokens table migration | STRICT | Sub-agent | `artifacts/D-0003/spec.md`, `artifacts/D-0003/evidence.md` | S | High |
| D-0004 | T01.04 | R-004 | UserRepository | STRICT | Sub-agent | `artifacts/D-0004/spec.md`, `artifacts/D-0004/evidence.md` | M | Medium |
| D-0005 | T01.05 | R-005 | RSA keypair generation | STRICT | Sub-agent | `artifacts/D-0005/spec.md`, `artifacts/D-0005/evidence.md` | S | High |
| D-CP01-END | T01.06 | (phase checkpoint) | End-of-Phase-1 checkpoint report | n/a | Checkpoint | `checkpoints/CP-P01-END.md` | XS | Low |
| D-0006 | T02.01 | R-018 | PasswordHasher (cost=12) | STRICT | Sub-agent | `artifacts/D-0006/spec.md`, `artifacts/D-0006/evidence.md` | M | High |
| D-0007 | T02.02 | R-019 | JwtService RS256 dual-key | STRICT | Sub-agent | `artifacts/D-0007/spec.md`, `artifacts/D-0007/evidence.md` | M | High |
| D-0008 | T02.03 | R-020 | TokenManager + replay detection | STRICT | Sub-agent | `artifacts/D-0008/spec.md`, `artifacts/D-0008/evidence.md` | L | High |
| D-0009 | T02.04 | R-021 | Password + email validators | STANDARD | Direct test | `artifacts/D-0009/spec.md`, `artifacts/D-0009/evidence.md` | S | Low |
| D-CP02-END | T02.05 | (phase checkpoint) | End-of-Phase-2 checkpoint report | n/a | Checkpoint | `checkpoints/CP-P02-END.md` | XS | Low |
| D-0010 | T03.01 | R-035 | AuthService orchestrator | STRICT | Sub-agent | `artifacts/D-0010/spec.md`, `artifacts/D-0010/evidence.md` | L | High |
| D-0011 | T03.02 | R-036 | AuthMiddleware | STRICT | Sub-agent | `artifacts/D-0011/spec.md`, `artifacts/D-0011/evidence.md` | M | High |
| D-0012 | T03.03 | R-037 | POST /auth/login | STRICT | Sub-agent | `artifacts/D-0012/spec.md`, `artifacts/D-0012/evidence.md` | M | High |
| D-0013 | T03.04 | R-038 | POST /auth/register | STRICT | Sub-agent | `artifacts/D-0013/spec.md`, `artifacts/D-0013/evidence.md` | M | High |
| D-0014 | T03.05 | R-039 | POST /auth/refresh | STRICT | Sub-agent | `artifacts/D-0014/spec.md`, `artifacts/D-0014/evidence.md` | M | High |
| D-CP03-MID | T03.06 | (phase checkpoint) | Mid-phase M3 checkpoint (authflow) | n/a | Checkpoint | `checkpoints/CP-P03-MID-AUTHFLOW.md` | XS | Low |
| D-0015 | T03.07 | R-040 | GET /auth/me | STRICT | Sub-agent | `artifacts/D-0015/spec.md`, `artifacts/D-0015/evidence.md` | S | Medium |
| D-0016 | T03.08 | R-041 | Password reset request+confirm | STRICT | Sub-agent | `artifacts/D-0016/spec.md`, `artifacts/D-0016/evidence.md` | L | High |
| D-0017 | T03.09 | R-042 | Rate-limit middleware | STRICT | Sub-agent | `artifacts/D-0017/spec.md`, `artifacts/D-0017/evidence.md` | M | Medium |
| D-0018 | T03.10 | R-043 | Error contract + DTO whitelist | STRICT | Sub-agent | `artifacts/D-0018/spec.md`, `artifacts/D-0018/evidence.md` | S | Medium |
| D-CP03-END | T03.11 | (phase checkpoint) | End-of-Phase-3 checkpoint report | n/a | Checkpoint | `checkpoints/CP-P03-END.md` | XS | Low |
| D-0019 | T04.01 | R-063 | APM instrumentation | STANDARD | Direct test | `artifacts/D-0019/spec.md`, `artifacts/D-0019/evidence.md` | M | Medium |
| D-0020 | T04.02 | R-064 | /healthz endpoint | STANDARD | Direct test | `artifacts/D-0020/spec.md`, `artifacts/D-0020/evidence.md` | S | Medium |
| D-0021 | T04.03 | R-065 | k6 load test | STANDARD | Direct test | `artifacts/D-0021/spec.md`, `artifacts/D-0021/evidence.md` | M | Medium |
| D-0022 | T04.04 | R-066 | bcrypt cost benchmark | STRICT | Sub-agent | `artifacts/D-0022/spec.md`, `artifacts/D-0022/evidence.md` | S | Medium |
| D-CP04-END | T04.05 | (phase checkpoint) | End-of-Phase-4 checkpoint report | n/a | Checkpoint | `checkpoints/CP-P04-END.md` | XS | Low |
| D-0023 | T05.01 | R-073 | SC-1..SC-7 validation pack | STRICT | Sub-agent | `artifacts/D-0023/spec.md`, `artifacts/D-0023/evidence.md` | M | High |
| D-0024 | T05.02 | R-074 | Penetration smoke test | STRICT | Sub-agent | `artifacts/D-0024/spec.md`, `artifacts/D-0024/evidence.md` | M | High |
| D-0025 | T05.03 | R-075 | Feature-flag rollout plan | STANDARD | Direct test | `artifacts/D-0025/spec.md`, `artifacts/D-0025/evidence.md` | S | Medium |
| D-0026 | T05.04 | R-076 | Rollback rehearsal | STRICT | Sub-agent | `artifacts/D-0026/spec.md`, `artifacts/D-0026/evidence.md` | M | High |
| D-CP05-END | T05.05 | (phase checkpoint) | End-of-Phase-5 checkpoint report | n/a | Checkpoint | `checkpoints/CP-P05-END.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01 | D-0001 | STRICT | 85% | `artifacts/D-0001/` |
| R-002 | T01.02 | D-0002 | STRICT | 85% | `artifacts/D-0002/` |
| R-003 | T01.03 | D-0003 | STRICT | 85% | `artifacts/D-0003/` |
| R-004 | T01.04 | D-0004 | STRICT | 80% | `artifacts/D-0004/` |
| R-005 | T01.05 | D-0005 | STRICT | 90% | `artifacts/D-0005/` |
| R-018 | T02.01 | D-0006 | STRICT | 90% | `artifacts/D-0006/` |
| R-019 | T02.02 | D-0007 | STRICT | 90% | `artifacts/D-0007/` |
| R-020 | T02.03 | D-0008 | STRICT | 85% | `artifacts/D-0008/` |
| R-021 | T02.04 | D-0009 | STANDARD | 80% | `artifacts/D-0009/` |
| R-035 | T03.01 | D-0010 | STRICT | 90% | `artifacts/D-0010/` |
| R-036 | T03.02 | D-0011 | STRICT | 90% | `artifacts/D-0011/` |
| R-037 | T03.03 | D-0012 | STRICT | 90% | `artifacts/D-0012/` |
| R-038 | T03.04 | D-0013 | STRICT | 85% | `artifacts/D-0013/` |
| R-039 | T03.05 | D-0014 | STRICT | 90% | `artifacts/D-0014/` |
| R-040 | T03.07 | D-0015 | STRICT | 85% | `artifacts/D-0015/` |
| R-041 | T03.08 | D-0016 | STRICT | 75% | `artifacts/D-0016/` |
| R-042 | T03.09 | D-0017 | STRICT | 80% | `artifacts/D-0017/` |
| R-043 | T03.10 | D-0018 | STRICT | 85% | `artifacts/D-0018/` |
| R-063 | T04.01 | D-0019 | STANDARD | 80% | `artifacts/D-0019/` |
| R-064 | T04.02 | D-0020 | STANDARD | 85% | `artifacts/D-0020/` |
| R-065 | T04.03 | D-0021 | STANDARD | 80% | `artifacts/D-0021/` |
| R-066 | T04.04 | D-0022 | STRICT | 85% | `artifacts/D-0022/` |
| R-073 | T05.01 | D-0023 | STRICT | 85% | `artifacts/D-0023/` |
| R-074 | T05.02 | D-0024 | STRICT | 85% | `artifacts/D-0024/` |
| R-075 | T05.03 | D-0025 | STANDARD | 80% | `artifacts/D-0025/` |
| R-076 | T05.04 | D-0026 | STRICT | 85% | `artifacts/D-0026/` |

## Execution Log Template

**Intended Path:** `TASKLIST_ROOT/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run | Result | Evidence Path |
|---|---:|---|---:|---|---|---|---|

## Checkpoint Report Template

- `# Checkpoint Report -- <Checkpoint Title>`
- `**Checkpoint Report Path:** TASKLIST_ROOT/../checkpoints/<name>.md`
- `**Scope:** <tasks covered>`
- `## Status` — Overall: Pass | Fail | TBD
- `## Verification Results` (exactly 3 bullets)
- `## Exit Criteria Assessment` (exactly 3 bullets)
- `## Issues & Follow-ups` — reference `T<PP>.<TT>` and `D-####`
- `## Evidence` — intended paths under `TASKLIST_ROOT/../evidence/`

## Feedback Collection Template

**Intended Path:** `TASKLIST_ROOT/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|

## Generation Notes

- Fixture is a proportional condensation of the 88-item source roadmap (M1=17, M2=17, M3=28, M4=10, M5=16 items). Core items kept; auxiliary items (unit tests, DTOs, config) merged into parent tasks' Acceptance Criteria where appropriate.
- Phase 3 explicitly retains a mid-phase checkpoint task (`T03.06`) to exercise Wave-4 checkpoint cadence per the TEST-SPEC.
- Phase files follow `phase-N-tasklist.md` convention for Sprint CLI discovery.
- Checkpoint tasks are numbered `T<PP>.<NN>` per Wave-4 contract (not bare `### Checkpoint:` headings).
