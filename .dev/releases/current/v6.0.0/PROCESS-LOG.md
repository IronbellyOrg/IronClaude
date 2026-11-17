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

### 6. PR 615 body check and one nudge (2026-11-17 20:19Z)
- **Step:** PR 2 (cleanup-audit runner) opened as #615 at about 20:15Z with the check "Generator-Constraint Considered (Contract #3)" failing: any PR that deletes a gate file (`gates.py`) must carry a `## Generator-Constraint Considered` section in its body. PR 1 (#616) hit the same check and fixed it on its own. The PR 2 agent had not after about 4 minutes, so I sent one nudge with `orca terminal send` giving the exact fix. It fixed the body within a few minutes.
- **Time:** 3 minutes of my time.
- **Got in the way:** the check is not in the plan or the prompt template, so every PR that deletes a gates or validator file finds it only after opening.
- **Change next time:** add "if the PR deletes or edits `gates.py`, `structural_checkers.py` or a `*_validator.py`, put a `## Generator-Constraint Considered` section in the PR body from the start" to the prompt template. Also expect it for PR 4 and PR 11.

### 7. PR 2 verified and merged (2026-11-17 20:25Z)
- **Step:** checked #615 on GitHub myself: 7 of 7 checks SUCCESS (latest runs), merge state CLEAN, head `0e9e7c51b`; Augment's review completed on that head with 1 low-severity suggestion whose thread is answered with evidence and resolved; Codex code review and security review both completed on that head with no findings; 0 unresolved threads. Read the agent's evidence folder. Merged with `gh pr merge 615 --repo IronbellyOrg/IronClaude --squash --delete-branch` as `049dcbbf0`.
- **Test counts (agent's run, `-n auto`):** before 27912 passed, 5 failed, 178 skipped, 2 xpassed; after 27875 passed, 4 failed, 178 skipped, 2 xpassed; 38 tests removed (`tests/test_cleanup_audit_structure.py`). The five baseline failures are not from this change. Of the four after: `test_claude_process_adapter` x2 and `test_install_keep::test_same_content_is_true_only_for_identical_readable_files` were already failing, and `test_schema_id_rejection::test_no_fs_write_when_schema_rejected` failed because `/tmp/eval-runs` is shared by the other agents' test runs happening at the same time (passes alone, 20 of 20). CI on GitHub passed `Test on Python 3.10`.
- **Note:** the agent's baseline is 27912 passed, far above the plan's 14610 (the 5.0.0 figure). The reason is UNVERIFIED (more tests since 5.0.0, or a different way of counting). G8 (b) must therefore compare against a fresh baseline taken on `integration` with the same command, not against 14610. Raised for the release PR.
- **Got in the way:** concurrent agents running the full suite collide on `/tmp/eval-runs` and on machine load (baseline took 8m34s, after 5m49s).
- **Change next time:** give each agent its own temp directory for test runs (for example set `TMPDIR` per worktree) or run the full suite for at most one agent at a time; record a fresh `integration` baseline in `RELEASE-READINESS.md` before wave 1.
- **From the agent's PROCESS-NOTES:** the first `/sc:workflow` call swallowed `--depth` and `--handoff` because of unbalanced quotes; the plan's acceptance wording said "neither cleanup_audit nor cleanup-audit" but the kept skill and command still say `cleanup-audit`, so the criterion should name only the removed runner (the module `cleanup_audit` or the command `superclaude cleanup-audit`).

## Out of scope, for later
- The task and documentation bundle (Part B of issue 571) and the agents evaluation (issue 572).
- Ryan's request of 2026-11-17 14:40 to fold the eight analysis documents (`sweep`, `observe`, `review-safety-scan`, `review-fixcheck-and-consequence-rule`, `shadow-run-and-review-panel`, `issue-pipeline`, `launch-level-guard`, `ccsession-retention`) into the docs and processes.
- The new repo that is to carry the project after the release.
