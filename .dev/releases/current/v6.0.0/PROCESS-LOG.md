# Process log (6.0.0)

One entry per step. Each entry: date and time (UTC), the step, the commands or skills used, how long it took, what went well, what got in the way, and what should change in the process or its tools. Copy in the useful lines of each agent's `PROCESS-NOTES.md` when its PR merges.

## Entries

### 1. Setup (2026-11-17 19:48Z)
- **Step:** read the orchestrator brief, issue 571 with all 21 comments, `release-procedure.md`, the 5.0.0 records; confirm worktree, branch and `gh` login; create this records folder.
- **Used:** `gh issue view 571 --repo IronbellyOrg/IronClaude --comments`, `gh auth status`, `orca worktree current --json`, `git fetch origin`.
- **Time:** about 5 minutes.
- **Went well:** the brief and issue 571 are complete enough to start with no questions. Worktree is on `clayphi/release-6.0.0`, `gh` is logged in as `clayphi`, `origin` is the fork.
- **Got in the way:** `gh issue view --comments` prints 155 KB for issue 571, too large to read in one go; the comment list had to be skimmed with `--json comments`. `orca worktree current --json` reports project id `github:superclaude-org/superclaude_framework` (the known, unverified Orca project id), so no Orca link flags are passed.
- **Change next time:** the release-plan issue body should say which comments hold decisions, or keep a "Decisions so far" section in the body so the orchestrator does not have to read every comment.

## Out of scope, for later
- The task and documentation bundle (Part B of issue 571) and the agents evaluation (issue 572).
- Ryan's request of 2026-11-17 14:40 to fold the eight analysis documents (`sweep`, `observe`, `review-safety-scan`, `review-fixcheck-and-consequence-rule`, `shadow-run-and-review-panel`, `issue-pipeline`, `launch-level-guard`, `ccsession-retention`) into the docs and processes.
- The new repo that is to carry the project after the release.
