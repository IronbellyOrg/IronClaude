# evals.json Registry-State Record (Phase 6 discovery)

**Date:** 2026-06-03
**Step:** Phase 6, Step 6.1
**Registry:** `.dev/eval-workspaces/sc-reflect/evals/evals.json`

## Current state (fresh Read)
- **Current max `id` = 26.** The low-spec (`TASK-RF-20260602-135209`, DONE) already consumed ids **21–26**
  (6 cases: `serena-wave0-config`, `serena-find-implementations`, `serena-find-declaration`,
  `serena-search-deps`, `serena-memory-retention`, `serena-summarize-changes`).
- The research's assumed "max 20 → ids 21-27" is STALE — the low-spec landed first. **Medium ids shift up.**
- Top-level `scope` string today: `"v1.0-ship-it-3-pilot-15-promotion-2-falsifier-skeleton-6-serena-v3"`.
- Array insertion point: append new objects before the closing `]` of `"evals": [ ... ]`.

## Assigned ids for the 10 medium cases (27–36)
| id | case_dir | FR/NFR | step |
|----|----------|--------|------|
| 27 | serena-execute-verify | FR-4 | 6.2 |
| 28 | serena-verify-injection | FR-4.2b / NFR-8 | 6.3 |
| 29 | serena-verify-exitcodes | FR-4.3 / C2 | 6.4 |
| 30 | serena-verify-drift-guard | FR-4.8 / M-COR2 | 6.5 |
| 31 | serena-onboarding | FR-2 | 6.6 |
| 32 | serena-handoff | FR-3 | 6.7 |
| 33 | serena-type-hierarchy | FR-1 | 6.8 |
| 34 | serena-token-budget | NFR-3 (§8.2) | 6.11 |
| 35 | serena-telemetry-completeness | NFR-2 holistic (§8.2) | 6.12 |
| 36 | serena-citation-freshness | NFR-4 holistic (§8.2) | 6.12 |

## Authority
Each Step 6.x append item re-reads `evals.json` fresh for the THEN-current max id (append-one-object per the
I3 incremental rule), so the actual assigned id is whatever is next after the live max at append time. This
table is the planned mapping; the fresh-Read at each append is authoritative if any drift occurs.

## Scope-string update (Step 6.10)
Update `scope` to reflect the 10 added medium cases, e.g. append `-10-serena-v3-medium` (ids 27-36 covering
FR-RV3-MED.1-4 + the 3 §8.2 integration cases).
