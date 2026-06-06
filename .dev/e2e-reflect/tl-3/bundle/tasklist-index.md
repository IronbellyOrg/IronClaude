# TASKLIST INDEX -- Sandbox Auth Hardening v0.1-e2e-tl3

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Sandbox Auth Hardening v0.1-e2e-tl3 |
| Generator Version | Roadmap->Tasklist Generator v4.0 |
| Generated | 2026-06-04T00:00:00Z |
| TASKLIST_ROOT | .dev/e2e-reflect/tl-3/bundle |
| Total Phases | 2 |
| Total Tasks | 7 |
| Total Deliverables | 7 |
| Complexity Class | MEDIUM |
| Primary Persona | security |
| Consulting Personas | analyzer, qa |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | `.dev/e2e-reflect/tl-3/bundle/tasklist-index.md` |
| Phase 1 Tasklist | `.dev/e2e-reflect/tl-3/bundle/phase-1-tasklist.md` |
| Phase 2 Tasklist | `.dev/e2e-reflect/tl-3/bundle/phase-2-tasklist.md` |
| Execution Log | `.dev/e2e-reflect/tl-3/bundle/execution-log.md` |
| Checkpoint Reports | `.dev/e2e-reflect/tl-3/bundle/checkpoints/` |
| Evidence Directory | `.dev/e2e-reflect/tl-3/bundle/evidence/` |
| Artifacts Directory | `.dev/e2e-reflect/tl-3/bundle/artifacts/` |
| Validation Reports | `.dev/e2e-reflect/tl-3/bundle/validation/` |
| Feedback Log | `.dev/e2e-reflect/tl-3/bundle/feedback-log.md` |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-tasklist.md | Authentication & Credential Migration | T01.01-T01.05 | STRICT: 3, STANDARD: 0, LIGHT: 2, EXEMPT: 0 |
| 2 | phase-2-tasklist.md | Documentation | T02.01-T02.02 | STRICT: 0, STANDARD: 0, LIGHT: 1, EXEMPT: 1 |

## Source Snapshot

- Phase 1 is deliberately auth and credential-migration heavy.
- The roadmap states the override condition: `n_cpo ≥ 1 OR n_strict ≥ 2` floors reflect to `--depth deep --tier 2`.
- Phase 1 contains token-refresh authentication, credential schema migration/rollback, and password hashing parameters.
- Phase 2 contains only a short documentation overview linking the Phase 1 documents.
- All work is sandboxed under `.dev/e2e-reflect/tl-3/work/`.

## Deterministic Rules Applied

- Phase headings were converted to contiguous phase files.
- Task IDs use zero-padded `T<PP>.<TT>` identifiers.
- Security, credential, password, schema, migration, and breaking-change keywords classified Phase 1 tasks as STRICT.
- Documentation overview classified as EXEMPT/LIGHT and did not trigger the phase override.
- Critical path override was applied to Phase 1 tasks that mention auth, credential migration, schema, or security-sensitive work.
- Reflection depth map was emitted under validation/reflect-pre.
- Each phase includes a terminal Post-Execution Reflection task.
- Deliverables are rooted under `.dev/e2e-reflect/tl-3/bundle/artifacts/`.

## Roadmap Item Registry

| Roadmap Item ID | Phase Bucket | Original Text (<= 20 words) |
|---|---|---|
| R-001 | Phase 1 | Design the token-refresh authentication flow and write it to `.dev/e2e-reflect/tl-3/work/auth-design.md` |
| R-002 | Phase 1 | Migrate the legacy credential store schema; document the migration and rollback in `.dev/e2e-reflect/tl-3/work/credential-migration.md` |
| R-003 | Phase 1 | Document the password-hashing parameters in `.dev/e2e-reflect/tl-3/work/hashing-params.md` |
| R-004 | Phase 2 | Add a short overview `.dev/e2e-reflect/tl-3/work/overview.md` linking the three Phase-1 docs |

## Deliverable Registry

| Deliverable ID | Task ID | Roadmap Item ID(s) | Deliverable (short) | Tier | Verification | Intended Artifact Paths | Effort | Risk |
|---:|---:|---:|---|---|---|---|---|---|
| D-0001 | T01.01 | R-001 | Auth design document | STRICT | Sub-agent (quality-engineer) | `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0001/spec.md` | M | High |
| D-0002 | T01.02 | R-002 | Credential migration and rollback document | STRICT | Sub-agent (quality-engineer) | `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0002/spec.md` | L | High |
| D-0003 | T01.03 | R-003 | Hashing parameters document | STRICT | Sub-agent (quality-engineer) | `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0003/spec.md` | M | High |
| D-CP01 | T01.04 | R-003 | End-of-phase checkpoint report | LIGHT | Quick sanity check | `.dev/e2e-reflect/tl-3/bundle/checkpoints/CP-P01-END.md` | XS | Low |
| D-RF01 | T01.05 | R-001,R-002,R-003 | Phase 1 post-execution reflection | LIGHT | Quick sanity check | `.dev/e2e-reflect/tl-3/bundle/artifacts/D-RF01/evidence.md` | XS | Low |
| D-0004 | T02.01 | R-004 | Overview documentation | EXEMPT | Skip verification | `.dev/e2e-reflect/tl-3/bundle/artifacts/D-0004/spec.md` | XS | Low |
| D-RF02 | T02.02 | R-004 | Phase 2 post-execution reflection | LIGHT | Quick sanity check | `.dev/e2e-reflect/tl-3/bundle/artifacts/D-RF02/evidence.md` | XS | Low |

## Traceability Matrix

| Roadmap Item ID | Task ID(s) | Deliverable ID(s) | Tier | Confidence | Artifact Paths (rooted) |
|---:|---:|---:|---|---|---|
| R-001 | T01.01,T01.05 | D-0001,D-RF01 | STRICT | 95% | `.dev/e2e-reflect/tl-3/work/auth-design.md` |
| R-002 | T01.02,T01.05 | D-0002,D-RF01 | STRICT | 95% | `.dev/e2e-reflect/tl-3/work/credential-migration.md` |
| R-003 | T01.03,T01.04,T01.05 | D-0003,D-CP01,D-RF01 | STRICT | 95% | `.dev/e2e-reflect/tl-3/work/hashing-params.md` |
| R-004 | T02.01,T02.02 | D-0004,D-RF02 | EXEMPT | 90% | `.dev/e2e-reflect/tl-3/work/overview.md` |

## Execution Log Template

**Intended Path:** `.dev/e2e-reflect/tl-3/bundle/execution-log.md`

| Timestamp (ISO 8601) | Task ID | Tier | Deliverable ID(s) | Action Taken (<= 12 words) | Validation Run | Result (Pass/Fail/TBD) | Evidence Path |
|---|---:|---|---:|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | Manual | TBD | `.dev/e2e-reflect/tl-3/bundle/evidence/` |

## Checkpoint Report Template

**Template:** write checkpoint reports under `.dev/e2e-reflect/tl-3/bundle/checkpoints/`.

## Feedback Collection Template

**Intended Path:** `.dev/e2e-reflect/tl-3/bundle/feedback-log.md`

| Task ID | Original Tier | Override Tier | Override Reason (<= 15 words) | Completion Status | Quality Signal | Time Variance |
|---:|---|---|---|---|---|---|
