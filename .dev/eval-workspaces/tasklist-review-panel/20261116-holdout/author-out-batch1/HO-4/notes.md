# HO-4 notes

## Result: 0 ground-truth items (all findings dropped)

The plan copied (sha256 bfc36351..., 236 lines) is **not the text the report reviewed**.
- The report's `artifacts/input-snapshot.yaml` records the reviewed plan as sha256 020f2cea... Git history holds only the 236-line bfc36351... version (the same hash as the ledger's `PLAN:` line); the reviewed draft is not recoverable.
- The report's plan line cites do not match (for example plan:218/:221 for the `--body-file` problem; plan:22 vs :67 for the installer ban).
- Every one of the 19 merged findings is already fixed in the copied plan text:
  - M-01 placeholder `--body` plus `gh pr edit --body-file` (Task 14 step 3, with "second-pass fix M-01" named).
  - M-02 PR body at `.dev/codegraph-migration/progress/P3-pr-body.md` (Task 14 step 2).
  - M-03 `_OTHER_COMMANDS` set edited (Task 12). M-04 single `$TESTSET` (Constraints). M-05 `KNOWN_CORE_FILES` exception (Constraints).
  - M-06 setup before `/sc:implement` (Constraints). M-07 fresh `claude` session for check (9) (Task 13).
  - M-08 reordered Task 14 steps 1-7. M-09 `git add ...progress ...decisions .dev/tasks` (Constraints, Task 2).
  - M-10, M-11 (Task 7: verify-only task.md; Task 12 replaces inline STRICT step 7). M-12 merge-base diff (Task 11).
  - M-13 sentinel scan exclusion and banned verbs (Task 3). M-14 `N=` form (Task 13). M-15 `graph:not_initialized` message (Task 3).
  - M-16 reflect.md `mcp-servers` (Task 10). M-17 G3/G5 routing (Task 1). M-18 commit messages use the spec's wording. M-19 baseline-comparison clause (Constraints).
- The implementation-time review records under artifacts/retries (T2, T6, T8, T9, T10, T12, T13, T14 review-*.md) grade blocking findings, but each concerns code or evidence the implementation produced (E1-freshness.md wording, group-comment rows, telemetry parsing, `/sc:impact` self row, root-copy mirroring, degraded-copy). None is a defect of the plan text (the plan states those rules correctly), so none was included. final-review.md reports no findings.

## Base
`start sha=18841c6d...` is a **tree** object, not a commit. The package uses the HEAD commit in `artifacts/retries/T1/q0-head`: 5e163da0b1d172fa49ea4fbf58c6cafbe7904243 (commit; ancestor of implementing commit 75d0d1e2c). That commit's tree holds the plan folder (4 files) under `.dev/tasks/to-do/`. masked_paths: [] (no file added by the implementation exists at base).
