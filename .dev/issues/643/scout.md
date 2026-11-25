# Scout report

- Mode: claim
- Repo: IronbellyOrg/IronClaude
- Written by: issue-worker-t3

## Claim

- Issue: #643
- url: https://github.com/IronbellyOrg/IronClaude/issues/643
- is_pull_request: false
- State: OPEN
- Assignees: ironbelly
- Current login: ironbelly
- Earlier claim comment ID: 6985692080 (https://github.com/IronbellyOrg/IronClaude/issues/643#issuecomment-6985692080)
- Earlier accuracy-check comment ID: 6985691501 (https://github.com/IronbellyOrg/IronClaude/issues/643#issuecomment-6985691501)
- Created at: 2026-11-18T16:26:43Z

### Merged pull requests since creation

- Result truncated at the 200 limit: no (16 PRs returned)

| PR | Title | Merged at | Changed files |
|---|---|---|---|
| #649 | docs: post-release sync and install runs for 6.0.0 | 2026-11-18T18:31:55Z | CHANGELOG.md, README.md, docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, docs/developer-guide/codegraph-integration.md, docs/developer-guide/documentation-index.md, docs/developer-guide/review-* (and more; GitHub file response capped at 100 paths) |
| #646 | fix(install): stop filecmp from returning a stale "identical" answer | 2026-11-18T17:11:14Z | src/superclaude/cli/install_core.py, src/superclaude/cli/install_keep.py, tests/cli/test_install_keep.py |
| #640 | release: 6.0.0 (removals, retire step, eight fixes) | 2026-11-18T16:30:09Z | merge commit; broad release diff (.dev/cleanup/*, .dev/releases/*, launch-level guard, many paths; GitHub file response capped at 100 paths) |
| #639 | chore(release): merge master into integration for 6.0.0 (resolve the routing-guide conflict) | 2026-11-18T15:46:21Z | .dev/tasks/done/TASK-WF-refactorScIssueC-20261118-041634/* |
| #637 | docs(review): say the tier5 gateway aliases are labels, not ccsession tiers | 2026-11-18T07:05:08Z | docs/reference/review-panel-live7.md |
| #636 | feat(issue): pick the default --claim pipeline level from the issue | 2026-11-18T07:39:25Z | .dev/tasks/*, issue-protocol skill files |
| #634 | chore(release): 6.0.0 version, changelog and release notes | 2026-11-18T14:50:57Z | .dev/releases/current/v6.0.0/* |
| #633 | feat(install): retire commands and skills that 6.0.0 no longer ships | 2026-11-18T03:08:00Z | .dev/cleanup/retire-step/*, .dev/tasks/*, launch-level guard and tests |
| #632 | refactor(cli): remove the roadmap, tasklist and sprint family (6.0.0) | 2026-11-18T02:05:51Z | .dev/cleanup/roadmap-family/*, src CLI removals, tests |
| #631 | refactor(commands): remove /sc:index and /sc:index-repo (6.0.0) | 2026-11-18T01:22:11Z | .dev/cleanup/index/*, .dev/reflect/*, commands removals |
| #630 | perf(ccsession): find every transcript and start folder of the worktree list in one process (#607, stage 2) | 2026-11-18T03:33:40Z | .dev/tasks/to-do/TASK-WF-ccsession607-20261117-230835/*, ccsession sources |
| #629 | refactor(cli): remove cli-portify (6.0.0) | 2026-11-18T00:25:55Z | .dev/cleanup/cli-portify/*, .dev/reflect/*, CLI removals |
| #628 | perf(ccsession): build the saved-session list without a process per saved name (#607, stage 1) | 2026-11-18T03:31:52Z | .dev/tasks/to-do/TASK-WF-ccsession607-20261117-230835/*, ccsession sources |
| #623 | feat(review): wonsol becomes the provisional default review panel | 2026-11-18T01:26:25Z | .dev/tasks/done/TASK-WF-wonsolDefaultV2-20261117-185458/*, review defaults |
| #619 | docs(how-we-work): drop built-in and local review steps from the shipping flow | 2026-11-18T03:34:41Z | docs/onboarding/ironclaude-onboarding.html, plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md, src/superclaude/core/HOW-WE-WORK.md, tests/core/test_how_we_work_routing_table.py |
| #608 | docs(style): define plain English and give the wrap-up a fixed five-part body | 2026-11-18T03:34:22Z | src/superclaude/output-styles/pragmatic.md, tests/commands/test_pragmatic_plain_english.py, tests/commands/test_sweep_command.py |

Note: only #646, #649 and #640 merged after the issue's createdAt (16:26:43Z); the other 13 merged earlier the same day and are included because the search window is date-based.

### Commits on the default branch since creation

| Commit | Changed files |
|---|---|
| 3f3b34a26 (merge, release: 6.0.0 (#640)) | merge commit; `git log --name-only` without `-m` lists no files for it; its diff is the #640 row above |

### First guesses

- Complexity: simple: one new file with a single fixed line, nothing else to touch.
- Type: feature: it asks to create a new file, not fix broken behavior.
