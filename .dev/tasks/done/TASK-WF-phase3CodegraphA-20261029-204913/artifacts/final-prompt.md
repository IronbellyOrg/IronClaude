# Managed FINAL review (archive gate) — TASK-WF-phase3CodegraphA-20261029-204913

Do not trust the implementer's report.

You are the one fresh FINAL reviewer for this archive attempt. Work read-only in the worktree /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption (do not edit, stage, commit, push, comment, or run anything that writes; read-only git, rg, cmp, gh view/api calls and `uv run pytest <files> -q -p no:cacheprovider` are allowed). Start from an adversarial position: assume defects exist.

Inputs (read the real current files):
- Plan (with its `## Constraints`, which bind every task): /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md
- Source spec snapshot: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md
- Ledger: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/progress.md (package root for `./artifacts/` tokens: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913)
- Every file in /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/retries/T<id>/ for T1..T14 (notes, probes, prompts, reviews); no `retry … step=revert` record exists in the ledger.
- The package logs under /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/.
- The reviewer template the saved prompts were built from: /tmp/impl-review/template.md (compare each saved `prompt-<k>-<j>.md` with it outside the slots; T13's two prompts carry one sentence, inside the diff-description slot, noting that six raw JSON transcripts were trimmed from the diff file).
- Delivery files (the helper's --print-state list; repo-relative to /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption):
  - .dev/codegraph-migration/decisions/P3X-execution-log.md
  - .dev/codegraph-migration/experiments/P3-T0/E1-freshness.md
  - .dev/codegraph-migration/experiments/P3-T0/E2-help.md
  - .dev/codegraph-migration/experiments/P3-T0/E3-allowlist.md
  - .dev/codegraph-migration/experiments/P3-T0/E6-agent-matrix.md
  - .dev/codegraph-migration/experiments/P3-T0/E7-slots-map.md
  - .dev/codegraph-migration/experiments/P3-T11-failures.txt
  - .dev/codegraph-migration/experiments/P3-T11-smoke.md
  - .dev/codegraph-migration/experiments/P3-baseline-failures.txt
  - .dev/codegraph-migration/progress/P3-0.md
  - .dev/codegraph-migration/progress/P3-A.md
  - .dev/codegraph-migration/progress/P3-B.md
  - .dev/codegraph-migration/progress/P3-C.md
  - .dev/codegraph-migration/progress/P3-D.md
  - .dev/codegraph-migration/progress/P3-E.md
  - .dev/codegraph-migration/progress/P3-G.md
  - .dev/codegraph-migration/progress/P3-coder-addendum.md
  - .dev/codegraph-migration/progress/P3-pr-body.md
  - CHANGELOG.md
  - commands/sc-explain.md
  - commands/sc-load.md
  - docs/user-guide/mcp-installation.md
  - plugins/superclaude/commands/brainstorm.md
  - plugins/superclaude/commands/explain.md
  - plugins/superclaude/commands/load.md
  - plugins/superclaude/commands/reflect.md
  - plugins/superclaude/core/CODEGRAPH.md
  - plugins/superclaude/modes/MODE_Orchestration.md
  - plugins/superclaude/skills/sc-implement-protocol/SKILL.md
  - plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
  - plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md
  - src/superclaude/agents/auggie-reviewer.md
  - src/superclaude/agents/reflect-reviewer.md
  - src/superclaude/agents/reuse-auditor.md
  - src/superclaude/agents/troubleshoot-analyst.md
  - src/superclaude/cli/install_core.py
  - src/superclaude/commands/auggie-review.md
  - src/superclaude/commands/brainstorm.md
  - src/superclaude/commands/cleanup-audit.md
  - src/superclaude/commands/explain.md
  - src/superclaude/commands/graph.md
  - src/superclaude/commands/impact.md
  - src/superclaude/commands/load.md
  - src/superclaude/commands/reflect.md
  - src/superclaude/commands/troubleshoot.md
  - src/superclaude/commands/validate-roadmap.md
  - src/superclaude/core/CLAUDE.md
  - src/superclaude/core/CODEGRAPH.md
  - src/superclaude/core/HOW-WE-WORK.md
  - src/superclaude/mcp/MCP_Auggie.md
  - src/superclaude/modes/MODE_Orchestration.md
  - src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
  - src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
  - src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
  - src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
  - src/superclaude/skills/sc-graph-protocol/SKILL.md
  - src/superclaude/skills/sc-impact-protocol/SKILL.md
  - src/superclaude/skills/sc-implement-protocol/SKILL.md
  - src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
  - src/superclaude/skills/sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
  - src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md
  - src/superclaude/skills/sc-reflect-protocol/SKILL.md
  - src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml
  - src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md
  - src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md
  - src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md
  - src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md
  - src/superclaude/skills/sc-task-protocol/SKILL.md
  - src/superclaude/skills/sc-tasklist-protocol/SKILL.md
  - src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
  - src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md
  - src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md
  - src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md
  - tests/agents/test_codegraph_rosters.py
  - tests/cli/reflect/fixtures/degraded_graph_absent.yaml
  - tests/cli/reflect/test_verdict_mapping.py
  - tests/commands/test_graph_command.py
  - tests/commands/test_impact_command.py
  - tests/core/test_codegraph_guide.py
  - tests/core/test_how_we_work_routing_table.py
  - tests/recommend/test_routing_refresh.py
  - tests/skills/test_codegraph_adoption.py
  - tests/troubleshoot/test_codegraph_grounding.py
  - tests/troubleshoot/test_diagnostic_worker_contract.py
  - tests/unit/test_cli_install.py

Rules (from the protocol's refs/qa.md, "Managed FINAL review" and "FINAL derived test"):
- For every task T1..T14, verify every acceptance criterion against the current files and the package's ./artifacts/ logs, not the ledger's claims. A moved line number alone is never `issues`.
- `issues` when an AC is unmet at the end state, no evidence for it exists in current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line.
- Severity test: each finding gets four yes/no answers (ac-outcome-missing, false-claim, harmful-effect, quoted-constraint-breach) with one anchor per yes. A notes entry whose answers are all `no` is `noted`, never `issues`; a confirmed `yes` is `issues` even if labelled minor. Review lines later marked `resolved`, and notes lines prefixed `superseded `, are history.
- Saved prompts that differ from the template outside the slots → `issues`.
- Never rewrite per-task verdicts; this is not a code-quality ensemble.

Return exactly:
FINAL: pass|issues
Per task: `T<n>: <AC ids> met|unmet — <path:line evidence>` (one line per task, every AC id listed).
Findings (if any): `F<k> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<y/n,y/n,y/n,y/n> : <text>`
Noted (all-no notes entries you checked): one line each.
Self-audit: what you actively checked and why no further defect exists (required when FINAL is pass).
