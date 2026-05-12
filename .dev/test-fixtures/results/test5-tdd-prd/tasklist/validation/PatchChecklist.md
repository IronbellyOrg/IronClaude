# PatchChecklist.md -- Tasklist v1.1 Patches

Ordered list of patches to apply in Stage 9. Each patch is scoped to a single drift item and a single `old_string -> new_string` replacement unless noted.

| # | File | Target | Action |
|---|------|--------|--------|
| P1 | phase-1-tasklist.md | T01.01 D-0001 deliverable | Replace `consent_flag, consent_ts` with `consent_accepted_at:timestamptz, consent_version:varchar` in schema description |
| P2a | phase-3-tasklist.md | T03.04 (FR-AUTH-006) | Replace `202` -> `200` and update envelope |
| P2b | phase-3-tasklist.md | T03.10 (API-RESET-REQ) | Replace `202` -> `200` (multiple) + update text |
| P3 | phase-3-tasklist.md | T03.10 (API-RESET-REQ) rate limit | Replace `5/min per IP` with `3/hour per email + 10/hour per IP` |
| P4 | phase-3-tasklist.md | T03.06 (DM-RESET cleanup) | Replace `< now() - 1h` with `< now() - 7 days` |
| P5 | phase-4-tasklist.md | T04.07 (SEC-HTTPONLY) cookie | Replace `SameSite=Lax; Path=/auth` with `SameSite=Strict; Path=/auth/refresh` |
| P6 | phase-6-tasklist.md | T06.04 (FEAT-FLAG-NEWLOGIN) | Replace rollout stages + add SLO-green >=60min + error-rate delta <0.5% criteria |
| P7 | phase-6-tasklist.md | T06.11 (ALERT-LOGIN-FAIL) | Replace `>5% for 5m` with `>30% sustained 10min` |
| P8 | phase-6-tasklist.md | T06.13 (ALERT-REDIS) | Replace `redis_up == 0 for 2m` with `redis_up == 0 for >1min` |
| P9 | phase-6-tasklist.md | T06.14 (ROLLBACK-AUTO-LATENCY) | Replace trigger condition with `p95 >500ms for 15min` |
| P10 | phase-6-tasklist.md | T06.15 (ROLLBACK-AUTO-ERR) | Replace `>2% for 5m` with `>1% for 10min` |
| P11 | phase-6-tasklist.md | T06.17 (ROLLBACK-AUTO-DATA) | Add `sustained 5 minutes` to threshold |
| P12 | phase-6-tasklist.md | T06.21 (OPS-011) | Reduce to 3 sign-offs (sec-reviewer, eng-manager, product) |
| P13 | phase-6-tasklist.md | T06.06 (OPS-001) | Metrics retention `15 days hot` -> `30 days` |
| P14 | phase-6-tasklist.md | T06.07 (OPS-002) | Tempo retention `14 days` -> `7 days`; add sampling rules |
| P15 | phase-6-tasklist.md | T06.08 (OPS-003) | Loki retention `30 days` -> `14d hot + 90d cold` |
| P16 | phase-6-tasklist.md | T06.10 (OPS-005) | Add `complaint rate <0.1%` AC |
| P17 | phase-6-tasklist.md | T06.16 (ROLLBACK-AUTO-REDIS) | Add `>3min` unreachable duration to trigger |

**Total patches:** 17 (12 primary fidelity + 5 minor)

Execution: sequential Edit calls, each verified by re-reading the affected section.
