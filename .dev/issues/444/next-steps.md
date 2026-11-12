/model claude-gw-tier1a

# Next steps for #444

Plan boundary: after step 1

Run these in order, after the `/model` line. `/sc:issue` itself does not run them: the agent it launches does (up to the plan boundary at the default level), or you do after `--pipeline none`.

1. `/tech-research "Evaluate whether and how the proposed /sc:orchestrator should support a sub-orchestrator or coordinator mode (possibly selected with --sub): a session that delegates work to its own sessions inside a worktree while taking orders from, and reporting to, an orchestrator above. I need a decision with options, risks and a recommendation, covering value, implications, unlocks and rethinks, especially of rule WC-13 (a worker may not start workers), decision D5 (Orca nesting depth kept at 1; the scoped sub-workers option was rejected) and the role 'a coordinator under another orchestrator' that PR #449 named in the installed rules without defining. Why: GitHub issue #444 asks for this evaluation before anyone builds it, and issues #339 (v1) and #423 (v2) of /sc:orchestrator depend on the answer. Where to look: src/superclaude/core/WORKER-CONTRACT.md, src/superclaude/core/CLAUDE.md, src/superclaude/hooks/scripts/require-orca-worktree-agent.sh, .dev/orca-command-refactor/ (decisions/D5, specs, changes/CR-01-feature-worktree-hierarchy.md), docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md section 7.7, tests/skills/test_worker_contract.py. Start from .dev/issues/444/issue-summary.md and .dev/issues/444/analysis/analyze-orchestration.md. Output: a decision report; do not plan or start an implementation."`
   - Input: `@.dev/issues/444/issue-summary.md`
   - Stop at the report it prints (`.dev/tasks/to-do/TASK-RESEARCH-<topic>-<timestamp>/RESEARCH-REPORT-<topic>.md`). Whether to build any mode it recommends is a separate decision: only then run `/sc:workflow "<what to build> as recommended in <report path>. Code: <folders>"`, read its printed plan, and run `/sc:implement <printed plan path>` when execution is requested.

- Effort estimate: 24 hours
- Default row not used: Feature, complex (brainstorm, design, workflow, implement). The issue asks for an evaluation, not a build, so the chain stops at a research report (guide row `research-first`); implementation is a later decision.
