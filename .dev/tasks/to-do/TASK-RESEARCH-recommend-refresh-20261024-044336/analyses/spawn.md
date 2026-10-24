# Research: /sc:spawn recommendation refresh

- **Topic type:** Command history and recommendation-contract review
- **Scope:** `/sc:spawn`, its plugin copy, governing routing guide, recommendation skill and references, cache prompts, hooks, and routing tests
- **Status:** Complete, research only; no files changed
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/spawn.txt`, worker `a6836c8048c92b682`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Two commits changed the canonical command during the inventory window, 2026-04-24 through 2026-10-24:

- `db824c4be3213cc76b605a1c4695f472563bd470`, 2026-05-17: substantive addition of Rule 2.5, requiring branch-trace evidence for narrowly defined failing-test investigation pipelines.
- `89df2c1105c01caff199288f949d5783f6594e70`, 2026-05-22: formatting only. The inspected patch adds blank lines and a final newline without changing command semantics.

Evidence: exact-path `git log` and both command patches; current Rule 2.5 is at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:74-124`.

[CODE-VERIFIED] The substantive commit also changed the adversarial protocol. Its current sufficiency challenge requires downstream-gate evidence and consultation of branch traces when available. This is complementary verification behavior, not a new universal requirement to route debugging through spawn. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-adversarial-protocol/SKILL.md:1188-1199`.

### Current command contract

[CODE-VERIFIED] Spawn is self-contained: its complete command file contains no Activation section or delegated protocol skill. It accepts a complex-task description, `--strategy sequential|parallel|adaptive`, and `--depth normal|deep`. Neither a default strategy nor a default depth is explicitly declared. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:1-210`, particularly lines 19-23.

[CODE-VERIFIED] The decisive boundary is “STOP AFTER TASK DECOMPOSITION.” Its output is a task breakdown document containing epic decomposition, dependencies, command assignments, and coordination strategy. It explicitly prohibits implementation, code modification, and system changes, then hands individual tasks to other commands. No durable resume interface, output-path flag, or authorization to execute implementation is documented. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:190-210`.

[CODE-VERIFIED] Delegated analytical prompts must resolve synchronous inputs to absolute paths, distinguish verification evidence from exploratory inference, and avoid overriding the delegate’s output organization. Asynchronous hierarchies may use directory and glob hints instead. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:41-72`.

[CODE-VERIFIED] Branch tracing is narrowly conditional: a single function or closely coupled pair, at least two early-exit statements, at least two tracebacks through that function, and at least four failing tests. Missing trace entries produce warnings injected into the adversarial stage, not a hard stop. Single-test failures, non-Python targets, documentation/configuration-only changes, and task execution without an adversarial stage are excluded. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:74-124`. These are verified prose contracts, not demonstrated runtime enforcement.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide currently describes spawn as “Break a large job into parts,” then directs code-changing work to task-builder. This omits spawn’s decomposition-only boundary and conflicts with the user’s desired policy of workflow plus implement for most planned implementation. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:282`, compared with the explicit stop boundary at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:190-210`.

[CODE-VERIFIED] Spawn appears in the Other commands block, not a routing-table workflow. Recommend considers that block only when no routing row matches. Matched rows bypass cache and semantic ranking, then dictate the route. Consequently, changing spawn’s short description alone cannot correct broad implementation-routing rules already matched by `task-file` or `feature-existing`. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:50-61,148-155`; existing guide rows at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:305-308`.

[CODE-VERIFIED] A separate anti-fabrication mismatch suppresses legitimate spawn options: recommend Rule R1 accepts flags only from a flag table or argument hint, but spawn declares both options in Usage and has neither of those alternative declarations. Correct source verification therefore needs to recognize explicit Usage signatures, without treating arbitrary examples as flag definitions. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:335-337` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:19-23`.

[CODE-VERIFIED] The plugin spawn command is materially older. It lacks Prompt Construction Rules, branch tracing, and the canonical critical stop boundary; its remaining behavior still says to execute coordinated tasks. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/spawn.md:25-98`, compared with canonical lines 41-128 and 190-210. Recommend’s source-selection rule prefers checkout source inside IronClaude, but outside it can select project, installed, or plugin copies. Thus recommendation meaning can vary with the verified distribution surface. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:102-116`.

[CODE-VERIFIED] Existing routing tests require spawn’s presence in Other commands but do not assert its decomposition boundary. Plugin parity tests cover the recommend skill tree and copied guide, not spawn’s command body. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:26-41,275-283` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py:27-36`.

### Proposed recommendation changes

[UNVERIFIED] **MUST, desired policy:** Replace the spawn entry in the governing guide’s Other commands block with wording such as: “Produce a cross-domain task hierarchy, dependencies, delegation assignments, and coordination strategy only. Does not implement. For most planned implementation use workflow followed by implement; reserve task-builder and task for exceptionally complex, long-running MDTM work.” Update the plugin guide copy together. This is a proposed change, not current behavior; its command-boundary basis is canonical spawn lines 190-210.

[UNVERIFIED] **MUST, routing alignment:** Preserve decomposition-only requests as supporting work rather than upgrading them to implementation because the described subject is large or spans domains. Modify existing guide conditions and recommend’s matched-mode treatment accordingly, without introducing a second keyword table. Preserve explicitly selected MDTM inputs. Current over-broad conditions are visible in the guide’s `task-file` and `feature-existing` rows, cited above.

[UNVERIFIED] **MUST, usable options:** Extend R1 and candidate verification to accept explicitly declared Usage signatures, including enumerated values. Carry the same rule into the condensed cold-path runbook and plugin recommend mirror. A grounded illustrative handoff is:

`/sc:spawn "Produce only a task hierarchy, dependencies, and delegation assignments for a cross-domain migration; do not implement" --strategy adaptive --depth deep`

Both options and values are declared in canonical spawn lines 19-23. This is a proposed recommendation example, not a command executed during research.

[UNVERIFIED] **SHOULD, distribution accuracy:** Align the plugin spawn contract before claiming it provides canonical evidence-enrichment or branch-trace capabilities. Preserve self-contained activation; do not invent a spawn protocol skill. Keep branch-trace mechanics in the target command rather than copying them into every recommendation.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed regression coverage:

1. A user requesting only a migration task hierarchy receives spawn, with no automatic implementation handoff.
2. Ordinary planned implementation across many files defaults to workflow plus implement; file count, multiple sessions, auditability, or an existing spec alone does not select MDTM.
3. An explicitly supplied MDTM execution request remains with task.
4. Verified spawn Usage accepts `--strategy adaptive --depth deep`; invented options such as `--resume` remain rejected.
5. Spawn’s candidate record is self-contained and decomposition-only.
6. Source and plugin spawn descriptions expose the same stop boundary.
7. A matched decomposition route, if introduced in the existing guide, bypasses cache as documented; no cache hit can substitute an implementation workflow for a report-only request.

## Gaps

[CODE-VERIFIED] Exact searches found no spawn-specific recommendation entry in the recommend skill, its references, or classifier/runbook. Generic “spawn” occurrences mostly concern Agent execution and are false positives for the slash command. The classifier’s `parallel-agent-fanout` category describes processing independent items, not producing spawn’s hierarchy. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:50-81`.

[CODE-CONTRADICTED] Canonical spawn’s early orchestration/execution prose contradicts its final decomposition-only boundary. Recommendations should honor the explicit critical boundary; harmonizing the command body is follow-up work, not permission to implement it here. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/spawn.md:25-39,176-210`.

[UNVERIFIED] No behavioral routing evaluation or tests were executed. This analysis does not establish actual hook enforcement, installed legacy-protocol behavior, or cross-model recommendation reliability.

## Key Takeaways

[CODE-VERIFIED] **CHANGE.** Current routing underspecifies spawn’s deliverable, over-directs code work toward task-builder, and cannot consistently retain its documented flags under literal R1. The plugin additionally lacks load-bearing canonical safeguards.

[UNVERIFIED] **MUST:** preserve decomposition-only intent, adopt the user’s workflow-first implementation policy in governing routes, and support verified Usage options. **SHOULD:** align plugin spawn and add behavioral regressions. **NONE:** new keyword tables, invented protocol skills, universal branch tracing, or implementation during this research pass.
