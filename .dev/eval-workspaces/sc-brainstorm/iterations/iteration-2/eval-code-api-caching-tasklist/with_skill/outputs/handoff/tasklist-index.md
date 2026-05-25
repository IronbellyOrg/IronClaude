---
handoff_type: tasklist
source_merged_requirements: ../merged-requirements.md
generated_from: sc-brainstorm v2
created: 2026-05-25T00:00:00Z
target_executor: sc:task
---

# Tasklist Index: API Layer Caching

This tasklist decomposes the merged requirements into Sprint-CLI-compatible task files. Tasks are ordered to satisfy dependencies; parallel-eligible tasks are flagged.

## Task ordering

| # | Task ID | Title | Depends on | Parallel-eligible |
|---|---|---|---|---|
| 1 | T-001 | Cache adapter foundation (`src/api/middleware/request_cache.py` skeleton + Redis adapter) | — | no |
| 2 | T-002 | Cache-key derivation function + unit tests | T-001 | no |
| 3 | T-003 | Per-route config schema + loader integration in `config/api.yaml` | T-001 | yes (with T-002) |
| 4 | T-004 | RequestCacheMiddleware integration into FastAPI middleware chain | T-001, T-002, T-003 | no |
| 5 | T-005 | Stampede protection via SETNX + 300ms wait window | T-001, T-004 | yes (with T-006) |
| 6 | T-006 | Invalidation dispatcher + handlers for affected write routes | T-001 | yes (with T-005) |
| 7 | T-007 | Migrate pricing.py per-instance LRU → shared cache | T-001, T-002, T-006 | no |
| 8 | T-008 | Background-job programmatic API + integration in `catalog_refresher.py`, `pricing_warmer.py` | T-001 | yes (with T-005, T-006) |
| 9 | T-009 | Observability — counters + histogram + OTel span | T-004 | yes (with T-007, T-008) |
| 10 | T-010 | Integration test suite (Redis Testcontainer, ≥12 cases) | T-004, T-005, T-006, T-007 | no |
| 11 | T-011 | E2E load test scenarios (hit-rate, stampede, chaos-Redis-kill) | T-010 | no |
| 12 | T-012 | Runbook + on-call training material | T-011 | yes (with T-013) |
| 13 | T-013 | Canary rollout (10% traffic, 1 week) — config + monitoring dashboard | T-011 | yes (with T-012) |

## Task file index

- `tasks/T-001-cache-adapter-foundation.md`
- `tasks/T-002-cache-key-derivation.md`
- `tasks/T-003-per-route-config-schema.md`
- `tasks/T-004-middleware-integration.md`
- `tasks/T-005-stampede-protection.md`
- `tasks/T-006-invalidation-dispatcher.md`
- `tasks/T-007-pricing-lru-migration.md`
- `tasks/T-008-background-job-api.md`
- `tasks/T-009-observability.md`
- `tasks/T-010-integration-tests.md`
- `tasks/T-011-e2e-load-tests.md`
- `tasks/T-012-runbook-and-training.md`
- `tasks/T-013-canary-rollout.md`

## Critical path

T-001 → T-002 → T-004 → T-006 → T-007 → T-010 → T-011 → T-013

Estimated critical-path duration: ~3.5 weeks of single-engineer work, or ~2.5 weeks with two engineers paralleling T-005/T-006 and T-008/T-009.

## Acceptance gates per task

Each task file (`tasks/T-NNN-*.md`) carries its own:
- Acceptance criteria (subset of the merged requirements AC list)
- Test surface (unit / integration / e2e markers)
- Definition-of-done checklist
- Provenance link back to merged-requirements.md sections

## Risks carried into execution

- R1 (stale data after missed invalidation) — primary discipline burden on T-006; PR checklist mandates that any new write route on a cached resource includes its invalidation handler.
- R2 (latency budget) — T-011 must validate before T-013 can proceed.
- R3 (stampede) — fully addressed by T-005; load-test verification in T-011.

## Next step

Run `/sc:tasklist --execute .dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-code-api-caching-tasklist/with_skill/outputs/handoff/` to generate the per-task `tasks/T-NNN-*.md` files via Sprint CLI, or hand this index to a human reviewer for adjustment before generation.

## Notes

This is the index manifest. The individual task files are not generated as part of this brainstorm artifact — they are produced by the downstream tasklist generator. The brainstorm's contract is satisfied by the index + dependency graph + acceptance-gate alignment with the merged requirements.
