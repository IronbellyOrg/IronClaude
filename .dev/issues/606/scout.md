# Scout report

- Mode: claim
- Repo: IronbellyOrg/IronClaude
- Written by: issue-worker-t3

## Claim

- Issue: #606
- url: https://github.com/IronbellyOrg/IronClaude/issues/606
- is_pull_request: false
- State: OPEN
- Assignees: none
- Current login: ironbelly
- Earlier claim comment ID: none
- Earlier accuracy-check comment ID: none
- Created at: 2026-11-17T17:55:57Z

### Merged pull requests since creation

- Result truncated at the 200 limit: no (35 PRs matched the search window, 21 merged after createdAt)

| PR | Title | Merged at | Changed files |
|---|---|---|---|
| #633 | feat(install): retire commands and skills that 6.0.0 no longer ships | 2026-11-18T03:08:00Z | src/superclaude/cli/{install_retired_data.py,install_retired_files.py,main.py}, scripts/gen_retired_install_data.py, src/superclaude/hooks/scripts/launch-level-guard.sh, plugins/superclaude/hooks/scripts/launch-level-guard.sh, docs (developer-guide, getting-started), tests/cli/test_install_retired_files.py, tests/hooks/test_launch_level_guard.py, .dev/tasks/TASK-WF-buildTheRetireSt-20261118-021743/** |
| #632 | refactor(cli): remove the roadmap, tasklist and sprint family (6.0.0) | 2026-11-18 | src/superclaude/cli/** (100 files; roadmap/tasklist/sprint removal + main.py), tests/cli/** |
| #631 | refactor(commands): remove /sc:index and /sc:index-repo (6.0.0) | 2026-11-18 | src/superclaude/commands/**, tests/** (61 files) |
| #630 | perf(ccsession): transcript and start folder scan in one process (#607 stage 2) | 2026-11-17T21:33:39Z | src/superclaude/skills/ccsession-tag/{ccsession,scan_sessions.py}, tests/unit/test_ccsession_tag.py, .dev/tasks/TASK-WF-ccsession607-20261117-230835/artifacts/** |
| #629 | refactor(cli): remove cli-portify (6.0.0) | 2026-11-18 | src/superclaude/cli/**, tests/** (100 files) |
| #628 | perf(ccsession): saved-session list without a process per name (#607 stage 1) | 2026-11-17T21:31:51Z | src/superclaude/skills/ccsession-tag/ccsession, tests/unit/test_ccsession_tag.py, .dev/tasks/TASK-WF-ccsession607-20261117-230835/** |
| #627 | refactor(commands): remove /sc:improve (6.0.0) | 2026-11-18 | src/superclaude/commands/**, tests/** (73 files) |
| #626 | fix(help): correct help text and messages (6.0.0) | 2026-11-18 | 44 files across src/superclaude/commands and docs |
| #625 | fix(ic): launcher alias, preset and help fixes (6.0.0) | 2026-11-18 | 18 files |
| #623 | feat(review): wonsol becomes the provisional default review panel | 2026-11-17T20:26:25Z | src/superclaude/cli/review/{data/review-default.json,data/review-panel.*.json,data/review-tiers.default.json,panel.py,panel_cmd.py}, tests/review/**, docs/reference/review-panel-live7.md, .dev/tasks/done/TASK-WF-wonsolDefaultV2-20261117-185458/** |
| #622 | refactor(commands): remove /sc:build (6.0.0) | 2026-11-18 | src/superclaude/commands/**, tests/** (55 files) |
| #621 | refactor(commands): remove /sc:review-translation (6.0.0) | 2026-11-18 | src/superclaude/commands/**, tests/** (38 files) |
| #620 | refactor(commands): remove /sc:save and /sc:load (6.0.0) | 2026-11-18 | src/superclaude/commands/**, tests/** (53 files) |
| #619 | docs(how-we-work): drop built-in and local review steps from the shipping flow | 2026-11-17T21:34:41Z | src/superclaude/core/HOW-WE-WORK.md, plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md, docs/onboarding/ironclaude-onboarding.html, tests/core/test_how_we_work_routing_table.py |
| #617 | refactor(commands): remove /sc:spawn (6.0.0) | 2026-11-18 | src/superclaude/commands/**, tests/** (51 files) |
| #616 | refactor(cli): remove the prd command-line pipeline (6.0.0) | 2026-11-18 | src/superclaude/cli/**, tests/** (75 files) |
| #615 | refactor(cli): remove the cleanup-audit headless runner (6.0.0) | 2026-11-18 | src/superclaude/cli/**, tests/** (72 files) |
| #614 | docs(plans): wonsol default-panel plan v2 and the surgical-remediation design | 2026-11-17 | docs/designs/surgical-remediation.md, .dev/reflect/**, .dev/spec-panel/**, .dev/tasks/** |
| #613 | fix: stop recommending /sc:task; it no longer releases a bound worker | 2026-11-17 | src/superclaude/core/{CLAUDE.md,HOW-WE-WORK.md}, src/superclaude/hooks/scripts/launch-level-guard.sh, plugins mirrors, docs/designs/{issue-pipeline-guard-g2.md,sc-issue-launch-level-hook.md}, docs/onboarding, tests |
| #608 | docs(style): define plain English and give the wrap-up a fixed five-part body | 2026-11-17T21:34:22Z | src/superclaude/output-styles/pragmatic.md, tests/commands/{test_pragmatic_plain_english.py,test_sweep_command.py} |
| #605 | feat(review): reflect reviewer carries the review severity rule (issue 552 stage 3b) | 2026-11-17 | src/superclaude/agents/reflect-reviewer.md, tests/skills/test_review_severity_rule.py, .dev/tasks/done/TASK-WF-stage3BRequest-20261117-172514/** |

(File lists abbreviated to the principal paths; full per-PR file lists are in the gh pr list output.)

### Commits on the default branch since creation

| Commit | Changed files |
|---|---|
| 3fb35a5ae | docs/onboarding/ironclaude-onboarding.html, plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md, src/superclaude/core/HOW-WE-WORK.md, tests/core/test_how_we_work_routing_table.py |
| a04ed5273 | src/superclaude/output-styles/pragmatic.md, tests/commands/test_pragmatic_plain_english.py, tests/commands/test_sweep_command.py |
| 90676ba02 | src/superclaude/skills/ccsession-tag/{ccsession,scan_sessions.py}, tests/unit/test_ccsession_tag.py, .dev/tasks/TASK-WF-ccsession607-20261117-230835/** |
| 8f9709db3 | src/superclaude/skills/ccsession-tag/ccsession, tests/unit/test_ccsession_tag.py, .dev/tasks/TASK-WF-ccsession607-20261117-230835/** |
| 7f93c0d9f | src/superclaude/cli/review/{panel.py,panel_cmd.py,data/*}, tests/review/**, docs/reference/review-panel-live7.md, .dev/tasks/done/TASK-WF-wonsolDefaultV2-20261117-185458/** |
| c00caea93 | docs/designs/surgical-remediation.md, .dev/reflect/**, .dev/spec-panel/**, .dev/tasks/** |
| b3c0aad59 | src/superclaude/core/{CLAUDE.md,HOW-WE-WORK.md}, src/superclaude/hooks/scripts/launch-level-guard.sh, plugins mirrors, docs/designs/**, docs/onboarding, tests |
| e3e9d636a | src/superclaude/agents/reflect-reviewer.md, tests/skills/test_review_severity_rule.py, .dev/tasks/done/TASK-WF-stage3BRequest-20261117-172514/** |

(Local origin/master has 8 commits since creation; gh shows more PRs merged 2026-11-18 than the local fetch has commits — the local ref may lag the GitHub state.)

### First guesses

- Complexity: complex: multi-phase visual redesign of `superclaude observe` with render gates, an automated capture/compare/fix loop, two-column layout work and pinned spec parts already posted in issue comments.
- Type: feature: the issue is a design-parity enhancement (labelled enhancement) extending the shipped observer, not a defect report, though it enumerates visual shortfalls.
