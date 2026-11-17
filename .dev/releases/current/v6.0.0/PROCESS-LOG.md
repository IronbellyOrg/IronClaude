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

### 2. Records committed and pushed (2026-11-17 19:49Z)
- **Step:** wrote README, RELEASE-READINESS, DECISIONS and this log on `clayphi/release-6.0.0`; committed and pushed.
- **Used:** `git add`, `git commit`, `git push -u origin clayphi/release-6.0.0`.
- **Time:** about 4 minutes, most of it writing the tables.
- **Went well:** the 5.0.0 files gave a ready shape for the decisions table and the readiness sections.
- **Got in the way:** a bare `python3` call is blocked by a user hook (`block-bare-python.sh`); helper scripts must run with `uv run --no-project python`.
- **Change next time:** a release template should ship these four files as stubs so the first commit is a copy, not a write.

### 3. Master merged into `integration` before wave 1 (2026-11-17 19:49Z)
- **Step:** `gh api -X POST repos/IronbellyOrg/IronClaude/merges -f base=integration -f head=master`.
- **Result:** HTTP 201, `integration` moved from `8c21ac41f` to `c873befec` (15 master commits).
- **Time:** under 1 minute. Nothing got in the way.
- **Change next time:** none; keep this one call per wave.

### 4. Issue 571 start comment (2026-11-17 19:50Z)
- **Step:** posted the start comment with branch name and wave list (https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6959094863).
- **Time:** 1 minute.

### 5. Wave 1 started: PR 1 prd-cli, PR 2 cleanup-audit-runner, PR 5 spawn (2026-11-17 19:50Z)
- **Step:** filled the prompt template for each PR with a small generator script (`/tmp/ic6-gen/gen.py`, not committed), saved the prompts in `prompts/`, created each worktree and agent with `orca worktree create ... --agent claude --prompt ... --json`, saved the replies in `launches/`, and started one background Monitor per agent (`/tmp/ic6-gen/watch.sh`, not committed).
- **Used:** `orca worktree create`, `orca terminal read --json`, `gh pr list`, `gh pr view`, the Monitor tool.
- **Time:** about 8 minutes for all three, including the generator and the watch script.
- **Went well:** the worktrees were created as children of this worktree (parentWorktreeId matches), based on `origin/integration` at `c873befec`, and each agent started reading its prompt within seconds.
- **Got in the way:** the first generator run was blocked by the bare-python hook (see entry 2). The prompt template is long; filling it by hand for 13 PRs would be slow and error-prone.
- **Change next time:** keep the generator and the watch script in the repo (for example under `scripts/release/`) so the next release does not rebuild them. Proposal only; not done here.

## Out of scope, for later
- The task and documentation bundle (Part B of issue 571) and the agents evaluation (issue 572).
- Ryan's request of 2026-11-17 14:40 to fold the eight analysis documents (`sweep`, `observe`, `review-safety-scan`, `review-fixcheck-and-consequence-rule`, `shadow-run-and-review-panel`, `issue-pipeline`, `launch-level-guard`, `ccsession-retention`) into the docs and processes.
- The new repo that is to carry the project after the release.
