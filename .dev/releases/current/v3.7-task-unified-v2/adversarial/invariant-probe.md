# Invariant Probe Results

## Round 2.5 -- Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | SummaryWorker thread pool state (`_summaries` dict) is accessed concurrently by writer threads and reader property; consensus agrees on threading.Lock but neither variant specifies lock granularity (per-key vs global) | ADDRESSED | MEDIUM | Round 2 rebuttal: Variant A mandates threading.Lock; B conceded. Global lock is standard for dict access patterns. |
| INV-002 | guard_conditions | `_verify_checkpoints()` replaces `_warn_missing_checkpoints()` in Wave 2. If Wave 2 is rolled back without re-applying Wave 1, executor has no checkpoint awareness at all. Cross-wave rollback creates a guard condition gap. | UNADDRESSED | HIGH | Diff analysis C-007; B's CE-Q2 raises this but no resolution in either variant. Neither variant specifies a rollback strategy that preserves Wave 1 when Wave 2 is reverted. |
| INV-003 | interaction_effects | Post-phase hook ordering (verify_checkpoints -> summary_worker.submit -> manifest update) creates an implicit dependency: if verify_checkpoints takes >30s (e.g., disk I/O timeout), it delays summary_worker.submit, which delays summary availability. Neither variant bounds verify_checkpoints execution time. | UNADDRESSED | HIGH | Variant A Section 6.4 defines the ordering but does not specify timeout/deadline for verify_checkpoints. Variant B does not define ordering at all. |
| INV-004 | collection_boundaries | `extract_checkpoint_paths()` returns empty list when no checkpoint sections found. Consumers (gate, manifest) must handle empty list gracefully. Neither variant specifies behavior when a phase has zero checkpoint sections. | ADDRESSED | LOW | Both variants note "If no `### Checkpoint:` sections exist, skip this step" (A Section 3.2 Wave 1, B T01.01 Step 2). Empty list is the expected representation. |
| INV-005 | count_divergence | Task numbering divergence: A has 15 tasks (T01.01-T01.02, T02.01-T02.05, T03.01-T03.06, T04.01-T04.03), B has 14 tasks (T02.01-T02.04, T03.01-T03.05). Different task counts create different checkpoint expectations if Wave 4 ties checkpoint tasks to task numbers. | ADDRESSED | MEDIUM | X-005 in diff analysis. Round 2 resolved: A's numbering (with test tasks) is preferred. Merge will use A's task list. |
| INV-006 | guard_conditions | Haiku subprocess env var stripping: both variants agree on stripping `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`. Neither checks if additional env vars (e.g., `ANTHROPIC_API_KEY`, `CLAUDE_CODE_*` glob) could cause recursive session or leaked credentials. | ADDRESSED | MEDIUM | A Section 6.3 specifies the two vars. This is sufficient per Claude Code documentation — no other vars cause recursive sessions. |

## Summary

- **Total findings**: 6
- **ADDRESSED**: 4
- **UNADDRESSED**: 2
  - HIGH: 2 (INV-002, INV-003)
  - MEDIUM: 0
  - LOW: 0
