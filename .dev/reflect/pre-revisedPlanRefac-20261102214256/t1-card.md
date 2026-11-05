# Tier 1 reflection card (UC-1, pre-execution, revised plan)

hypothesis_source: inline-orchestrator
spec: .dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/source.md
tasklist: .dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md
prior report: .dev/reflect/pre-refactorIronClau-20261102175540/REPORT.md (14 deviations D-001..D-014)

## Coverage section (qa lens)

- Pass 1 parsed IDs: 0. Pass 2 inferred rows: 41 (artifacts/pass2-inferred.yaml), including one or more rows per D-001..D-014. coverage_degraded: parsed-sparse, so a Tier 1 stop is forbidden.
- Containment match (artifacts/coverage-matrix.json): 36 of 41 matched; coverage_pct_union 0.878; coverage_pct null; S_dev_density 0.122.
- The 5 lexically unmatched rows, content-level disposition (all COVERED):
  - INF-010 "never stage .claude mirrors": plan Constraints bullet "Never stage any `.claude/` path except `.claude/settings.json`" plus the Task 7 and Task 8 staging criteria.
  - INF-011 "This revision supersedes plan ...": the first Constraints bullet names the superseded plan and says "Do not execute the superseded plan" (see S4 for the archive gap).
  - INF-012 "must resolve all 14 deviations": every task names the D-ids it resolves; a count of `D-0NN` tokens in the plan finds each of D-001..D-014 at least once.
  - INF-016 "add a list-argument search to the inventory and the final residual check": Constraints define Search B; Task 1 tables it; Task 8 re-runs it.
  - INF-039 "(do not move or remove them in this plan)": Constraints bullet "recorded only. No task moves, removes or edits them" and Task 1's "left in place" note.
- Content level: 41 of 41 covered; the open items are findings F1-F4 and S3-S4, not coverage gaps.

## Root-cause / deviation section (analyzer lens)

- F1 (gap, medium): the new "allowed gh forms" rule in Task 4 (a positional repo must be named; no `{owner}/{repo}` placeholder) is broken by the repo's own installed tooling, which the plan does not mention. src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:22, poll-ci-checks.sh:35, reply-resolve-thread.sh:57 and retrigger-review.sh:50 each fall back to a bare `gh repo view --json nameWithOwner -q .nameWithOwner` when `$REPO` is empty. The fallback is guarded (it runs only when origin gives no URL), and the prior run's debate kept this informational (U-007), but the new CLAUDE.md wording makes it a literal violation. Recommendation: Task 4 either scopes the allowed-forms rule to commands an agent issues by hand or names the guarded pr-submit fallback as a known, guarded exception. Classification: drift (plan-internal conflict with existing code).
- F2 (decision taken by the planner, low): D-013 asks the plan to "say what happens" to the two retired-location checkouts; Task 3 chooses "may stay until their branch is merged, then removed with `git worktree remove`". The source did not dictate the policy. Classification: necessary (the source requires a statement; this is a conservative choice that moves nothing).
- F3 (decision taken by the planner, low): D-005 asks to "decide the CLAUDE.md:251 issue link explicitly"; Task 4 keeps it unchanged as a static documentation reference, consistent with its own out-of-scope statement. Classification: necessary.
- F4 (residual scope, low, [INFERRED]): bare gh calls in other skills (sc-auggie-review-protocol, sc-troubleshoot-protocol; INV-010 in the prior run) are not covered by the plan. The source's 14 deviations do not include INV-010, so this is out of the source's scope; whether gh resolves those calls to upstream with only `origin` present is unverified.

## Structural / tech-debt section (refactorer lens)

- S1: Task 2's design is executable. Verified 2026-11-02 in a throwaway repo under /tmp: `git worktree add --detach <empty mktemp -d dir> master` exits 0, and `git worktree remove --force <dir>` exits 0 and deletes the directory. scripts/eval_runner.py:136-162 (`run_global`) and :287-300 (`main`'s global block, which reuses `REPO_ROOT.parent / "IronClaude-eval-master"` at :294) are the two places Task 2 must change; the plan names both.
- S2: Task 8's zero-skip rule is achievable on this host: the only skip markers in its test files are tests/troubleshoot/backtest/test_git_replay_integration.py:56-68 (module skip when a pinned replay parent is missing) and tests/skills/test_implement_retry_revert.py:357 (skip as root). All five pinned parents (git_replay.py:52-58) are present locally, `git rev-parse --is-shallow-repository` prints `false`, and `id -u` prints 1000. In CI (shallow checkout) the module would skip, which the plan handles with the recorded-reason-and-rerun clause.
- S3: Task 4's acceptance check "saved as ./artifacts/t4-gh-lines.txt from `grep -n 'gh ' CLAUDE.md`" matches words such as "through " and "high " across the whole file, so the artifact is noisy and the criterion still needs judgment for the section. Low.
- S4: The superseded plan's package (.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/) is still under to-do; the revised plan says "Do not execute the superseded plan" but nothing archives or marks it. Low; an executor scanning to-do could pick it up.
- S5: Mirror discipline unchanged and correct: Task 7 copies the three sc-recommend files, runs `make sync-dev` before `make verify-sync`, and adds tests/skills/test_sc_recommend_routing_contract.py (D-011). sc-post-release-protocol has no plugin copy (checked `ls plugins/superclaude/skills/`).

## Self-reported confidence (NOT used by the rubric; calibrator re-grades)

self_reported: 0.85. Structural signals: S_scope 8 tasks; S_domains 4 (docs, config, tests, code: scripts/eval_runner.py); S_dev_density 0.122.
