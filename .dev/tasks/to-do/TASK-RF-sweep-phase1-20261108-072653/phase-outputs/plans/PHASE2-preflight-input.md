# Phase 2 preflight input (owner message of 2026-11-12)

Status: INPUT RECORDED, not yet used. Phase 2 does not exist as a plan yet.

## Owner instructions

- "No need to write FIN-F7 for phase 2": FIN-F7 (the exempt `/sc:sweep` chat reply does not relay an Orca outage; ruled a documented limitation of Phase 1) is not part of Phase 2 scope.
- "For phase 2, add a preflight phase that ingests the following information and instructions." The Phase 2 plan (when it is written with `/sc:workflow` or `/tech-research`) starts with a preflight phase that reads the material below before any design or build step.
- The agent that runs that preflight is told three things: (1) sub-orchestrator mode is deferred and was never shipped; (2) behaviour on the installed host must not be inferred from the checkout; (3) the open owner questions are questions, not decisions.
- Merge PR #532 first so the technical reference is on master. Until then, point the agent at the `docs/supervised-orchestration-technical-reference` branch.
- The owner states every path below exists; the owner judged contents from names, headings or earlier work and did not re-read them. The preflight must therefore check that each path exists and read it, and must not rely on the descriptions.

## Reading list given by the owner (verbatim)

The most useful files for that agent, in the order I would have it read them. I confirmed that every path exists. I judged what each file contains from its name, its headings or my earlier work, and did not re-read them for this list.

1. Read first (how it works today, and the open design question)
- docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md (2,243 lines): the evidence-based map of roles, lifecycle, guards, launchers and limits. It holds the 19 open owner questions in Section 14.3.1. It is on the PR #532 branch, not yet on master.
- .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md (2,981 lines): the research on this exact feature. Start at Section 3 (target state, line 758), Section 4 (gaps, line 840), Section 7 (recommendation, line 2107), Section 8 (implementation plan, line 2296) and Section 9 (open questions, line 2470).
- src/superclaude/core/WORKER-CONTRACT.md (338 lines): the contract workers and coordinators follow.
- .dev/issues/444/: start with description.md, issue-body.md and recommend.md, then analysis/. This issue holds the sub-orchestrator question.
- CLAUDE.md and src/superclaude/core/CLAUDE.md: the Orca rules, including "every Orca worktree gets an agent" and who owns what.

2. Orca's own skills (installed copies, identical to the Orca checkout's)
- ~/.claude/skills/orchestration/SKILL.md and ~/.claude/skills/orca-cli/SKILL.md (68 lines for the first). These are short loaders that tell the agent to fetch the version-matched guide from the CLI.

3. Enforcement code, with its tests
- src/superclaude/hooks/scripts/: launch-level-guard.sh, require-orca-worktree-agent.sh, launch-job-identity.sh, launch-level-pre-push.sh. The plugins/superclaude/hooks/scripts/ mirror holds copies.
- tests/hooks/test_launch_level_guard*.py, test_require_orca_worktree_agent*.py, test_launch_job_identity.py and tests/core/test_orca_session_launch_guidance.py.
- Known defect: the guard recognizes the Orca CLI only as orca. It is recorded, not fixed.

4. How skills are built in this repo, and how they use Orca
- src/superclaude/skills/sc-issue-protocol/ (scripts/orca_worktree.py creates a worktree and launches an agent).
- src/superclaude/skills/sc-implement-protocol/, sc-workflow-protocol/, sc-pr-submit-protocol/ and ccsession-tag/.
- src/superclaude/core/HOW-WE-WORK.md and docs/designs/sc-issue-claim-pipeline-flag.md.

5. Orca source (read-only, /home/coder/workspaces/IronOrca at commit dc57b3d6e8)
- src/cli/specs/orchestration.ts and orchestration-worker-specs.ts: the command surface.
- src/cli/handlers/orchestration/: worker-launch-handler.ts, dispatch-handlers.ts, gate-handlers.ts, task-handlers.ts, run-handlers.ts, message-*.ts.
- src/shared/orchestration-*.ts and src/shared/worktree/lineage-types.ts (nested depth and lineage).

6. Evidence trail, only when a claim needs checking
- .dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/research/ (01-roles-authority.md through 06-distribution-evidence.md, and the gap-P3-G*.md files) and synthesis/.
- .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/research/scope/scope-01 to scope-04, research/web-04-orca-nested-depth-helpers.md, synthesis/synth-06-questions-evidence.md and reviews/user-presentation-summary.md.

RECOMMENDED ACTION: Give the agent groups 1 and 2 first, and tell it three things: sub-orchestrator mode is deferred and was never shipped, behavior on the installed host must not be inferred from the checkout, and the open owner questions are questions, not decisions. Merge PR #532 first so the reference is on master. Until then, point the agent at the docs/supervised-orchestration-technical-reference branch.
