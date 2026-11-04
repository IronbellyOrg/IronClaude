# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent read-only fault-finder (not an advocate), probing the Round 2 consensus across all 6 categories. Paths are relative to the repo root. Orchestrator spot-check 2026-11-02T18:38Z confirmed: `git remote -v` lists only `origin`; `git worktree list` shows `/home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates`; scripts/eval_runner.py:136-147 as quoted; the eight list-argument hits in INV-003; `.github/workflows/test.yml:17` uses `actions/checkout@v4` with no `fetch-depth`.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | An `upstream` remote exists and causes Orca's upstream project id | UNADDRESSED | MEDIUM | `git remote -v` lists only `origin`; plan lines 73, 76 and CLAUDE.md:41 assume `upstream`; pyproject.toml:64-67 and package.json carry upstream URLs; the plan line 76 guard may never lift |
| INV-002 | state_variables | No checkout is still in use at the retired location | UNADDRESSED | LOW | `git worktree list`: /home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates is live; plan says nothing about existing checkouts there |
| INV-003 | collection_boundaries | eval_runner.py is the only worktree creation the grep misses | UNADDRESSED | MEDIUM | List-argument hits outside the 17 files: tests/unit/test_ccsession_tag.py:1858, :1912; tests/troubleshoot/backtest/test_git_replay_unit.py:34. Extra uncounted lines in listed files: src/superclaude/cli/reflect/config.py:202, tests/troubleshoot/backtest/git_replay.py:191, tests/skills/test_implement_retry_revert.py:614, :1054, tests/cli/reflect/test_isolate_reviewers_cli.py:147 |
| INV-004 | count_divergence | Adding eval_runner leaves the 108/17 accounting valid | UNADDRESSED | MEDIUM | Plan line 42 requires counts that sum to the live `git grep -c` total; a row from a second search breaks the sum unless it carries its own total |
| INV-005 | guard_conditions | eval_runner.py can be classified under the existing scheme | UNADDRESSED | HIGH | scripts/eval_runner.py:138 puts the checkout at `REPO_ROOT.parent` (Orca's own directory from an Orca worktree); :142-147 never removes it and ignores the return code; fits neither class (plan line 57 "creates and removes itself", plan line 33 "Use exactly these classes"); no task edits the script; Task 7 (plan line 134) re-runs only the first grep |
| INV-006 | guard_conditions | A zero-skip rule is always achievable | UNADDRESSED | MEDIUM | .github/workflows/test.yml:17 `actions/checkout@v4` without `fetch-depth` (shallow) -> test_git_replay_integration.py:56-68 skips; test_implement_retry_revert.py:357 skips as root |
| INV-007 | interaction_effects | Rewriting check 3 to "stop and report" conflicts with /sc:pr-submit | ADDRESSED | LOW | src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:222 already HALTs on a misrouted URL without closing the PR |
| INV-008 | interaction_effects | Banning interaction leaves a way to recover from a leaked upstream PR | UNADDRESSED | MEDIUM | CLAUDE.md:66 (close the PR) is removed and plan line 77 allows no exceptions; the rewrite must say the agent reports and the user closes |
| INV-009 | guard_conditions | "--repo on every gh call that accepts it" covers every call that can reach upstream | UNADDRESSED | MEDIUM | `gh repo view` takes a positional repo; `gh api repos/{owner}/{repo}` fills in the default repo; tests/pr_submit/test_static_grep.py:616 pins the bare `gh repo view` fallback |
| INV-010 | sufficiency_challenge | Editing CLAUDE.md alone makes the tooling obey the gh rule | UNADDRESSED | MEDIUM | Bare gh calls in sc-auggie-review-protocol/SKILL.md:30, :97, :127, :319, :331 and sc-troubleshoot-protocol/SKILL.md:207; whether gh resolves them to the parent with only `origin` is inferred |
| INV-011 | collection_boundaries | Deciding CLAUDE.md:251 settles the static-link reading (X-001) | UNADDRESSED | MEDIUM | 22 lines in 10 tracked files hold the upstream URL (pyproject.toml 4, package.json 3, SECURITY.md 3, docs 6, CLAUDE.md 3, test_crash_recovery.py:179, test_pre_pr_checks.py:37, :82 as negative fixtures); supports narrowing plan line 73 to tool calls and link flags |
| INV-012 | sufficiency_challenge | Rewriting CLAUDE.md breaks no test (A-001) | ADDRESSED | LOW | tests/core/test_how_we_work_routing_table.py:352-357 is the only reader of root CLAUDE.md; it rejects only an `@...HOW-WE-WORK` line |
| INV-013 | interaction_effects | A hook enforces the old worktree rule | ADDRESSED | LOW | No `worktree` match in .claude/settings.json or src/superclaude/hooks |
| INV-014 | collection_boundaries | `.claude/worktrees/` appears only in CLAUDE.md and .gitignore | UNADDRESSED | LOW | docs/swarm/runbook.md:34 cites a `.claude/worktrees/BareReview` path, outside both greps |
| INV-015 | state_variables | Orca's default location is outside the main checkout (A-002) | ADDRESSED (this host only) | LOW | `git worktree list`: main checkout /home/coder/workspaces/IronClaude; Orca worktrees under /home/coder/workspaces/worktrees/IronClaude/ |

## Summary

- **Total findings**: 15
- **ADDRESSED**: 4 (all LOW)
- **UNADDRESSED**: 11
  - HIGH: 1 (INV-005)
  - MEDIUM: 8 (INV-001, INV-003, INV-004, INV-006, INV-008, INV-009, INV-010, INV-011)
  - LOW: 2 (INV-002, INV-014)

CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-005
These invariant violations must be resolved before convergence can be declared.

WARNING: 8 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-003, INV-004, INV-006, INV-008, INV-009, INV-010, INV-011
