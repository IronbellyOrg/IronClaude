# /sc:recommend output for #444

- Recorded: 2026-11-08T17:59:07Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/444. Type: feature. Complexity: complex. Summary: .dev/issues/444/issue-summary.md. Suggested route (default row "Feature, complex" of the /sc:issue chains): /model claude-gw-tier1a; 1. /sc:brainstorm "<topic> @.dev/issues/444/issue-summary.md" --depth deep --research deep --codebase --blind; 2. /sc:design <brainstorm dir>/merged-requirements.md --type <architecture|api|component|database> --format spec; 3. /sc:workflow <design doc> --depth deep --handoff none; 4. /sc:implement <plan path>. Note: the issue asks for an evaluation (value, implications, unlocks and rethinks of a sub-orchestrator or coordinator mode), not a build. Implementation is a separate, later decision.

The block below is the skill's output, copied verbatim.

````text
Goal: Evaluate whether a sub-orchestrator or coordinator mode for the proposed /sc:orchestrator is worth building (issue #444), and stop at a written decision. No build.

Level: 5 - guide section 1, 3.5, row `research-first`

Changes files: yes, report artifacts only. /tech-research writes a task folder .dev/tasks/to-do/TASK-RESEARCH-<topic>-<timestamp>/ holding its research files, QA files and RESEARCH-REPORT-<topic>.md (it drives /task-builder and /task internally; that is the skill's own machinery, not a separate level-4 choice). No product source, Git, or GitHub changes.

Run these in order:

1. /tech-research "Evaluate whether and how the proposed /sc:orchestrator should support a sub-orchestrator or coordinator mode (possibly selected with --sub): a session that delegates work to its own sessions inside a worktree while taking orders from, and reporting to, an orchestrator above. I need a decision with options, risks and a recommendation, covering value, implications, unlocks and rethinks, especially of rule WC-13 (a worker may not start workers), decision D5 (Orca nesting depth kept at 1; the scoped sub-workers option was rejected) and the role 'a coordinator under another orchestrator' that PR #449 named in the installed rules without defining. Why: GitHub issue #444 asks for this evaluation before anyone builds it, and issues #339 (v1) and #423 (v2) of /sc:orchestrator depend on the answer. Where to look: src/superclaude/core/WORKER-CONTRACT.md, src/superclaude/core/CLAUDE.md, src/superclaude/hooks/scripts/require-orca-worktree-agent.sh, .dev/orca-command-refactor/ (decisions/D5, specs, changes/CR-01-feature-worktree-hierarchy.md), docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md section 7.7, tests/skills/test_worker_contract.py. Start from .dev/issues/444/issue-summary.md and .dev/issues/444/analysis/analyze-orchestration.md. Output: a decision report; do not plan or start an implementation."

Notes:
- Research-only: stop after step 1. Do not append implementation planning or shipping. Reading many files is not a reason to build a plan.
- If the report recommends building a mode, planning is a separate decision: /sc:workflow "<what to build> as recommended in <report path>. Code: <folders>", then /sc:implement <printed plan path> only when execution is requested.
- MDTM as a deliberate level-4 choice is separate from the machinery /tech-research uses inside itself.

Sources verified:
- /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/core/HOW-WE-WORK.md (routing table, row `research-first`)
- /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test/src/superclaude/skills/tech-research/SKILL.md (Read; identical to ~/.claude/skills/tech-research/SKILL.md; input is free text, no flags)
- auggie semantic rank: skipped (matched row)
````
