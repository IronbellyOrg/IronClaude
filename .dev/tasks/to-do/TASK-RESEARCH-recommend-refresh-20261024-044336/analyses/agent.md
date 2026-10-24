# Research: /sc:agent recommendation accuracy

- **Topic type:** Command contract and recommendation routing
- **Scope:** Six-month command history, current command, recommendation surfaces, plugin mirrors, startup hooks, classifier/cache, and routing tests
- **Status:** Complete, read-only investigation; findings returned directly rather than written to a report file
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/agent.txt`, worker `abe998e847f932c09`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The exact command has one change in the requested interval: commit `89df2c1105c01caff199288f949d5783f6594e70`, dated `2026-05-22T15:47:02-04:00`, titled “chore: apply markdownlint MD022/MD031/MD032/MD034 auto-format repo-wide (#74)”. Its actual patch adds one blank line after “Startup Checklist”. This is formatting only, not new orchestration, planning, resume, or review functionality. Evidence: exact-path `git log` and `git show`; current affected location is `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/agent.md:11-13`.

### Current command contract

[CODE-VERIFIED] `/sc:agent` is a self-contained session-controller instruction document, not a dispatcher to an `sc-agent-protocol` skill. Its startup checklist reports Git status, reminds the user about context budget, names core services, and then explicitly waits for a task. It documents no flag table, argument hint, structured input schema, or required artifact input. The supported minimal invocation is therefore `/sc:agent`, without added flags. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/agent.md:1-23`.

[CODE-VERIFIED] Once a task is assigned, the controller clarifies scope, investigates with parallel tools, requests confidence checking and specialist agents, requires confidence of at least 0.90 before implementation, performs edits, runs agreed tests, and asks for self-review. Its output is concise phase updates and validated results, not a prescribed plan package or report file. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/agent.md:25-50`.

[CODE-VERIFIED] This is not inherently report-only: the implementation wave explicitly prepares and applies edits. The command does not define a persistent execution ledger, restart token, archive lifecycle, or task-file resume procedure. It allows memory persistence only when requested. A recommendation must not advertise those missing guarantees or treat invoking the controller as authorization for unrelated Git or publication actions. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/agent.md:41-48,54-68`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide already describes `/sc:agent` accurately as “A general session controller” and says to prefer its process levels instead. The plugin guide carries the same entry. Consequently, there is no evidence that recent `/sc:agent` functionality needs a new implementation-routing row. Evidence on both surfaces: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:260-268` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:260-268`.

[CODE-VERIFIED] Recommendation discovery can find the command without a command-specific keyword mapping. Step 0 admits matching “Other commands” as candidates only when no routing row matches; Phase 0 enumerates command files and verifies candidates by reading them. The absence of an explicit `/sc:agent` entry in the main recommend command, classifier, and recommendation references is therefore not itself a discovery defect. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:50-60,96-135`.

[CODE-CONTRADICTED] The recommendation skill’s blanket statement that commands are thin dispatchers delegating through `## Activation` is false for this command. `/sc:agent` contains its own behavior and no `Skill <name>` handoff. The verification reference already supports `activation_style: self-contained`, so the correction should clarify existing discovery semantics rather than invent another protocol. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:114`, `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/agent.md:7-72`, and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md:75-89`. The plugin skill repeats the blanket statement at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/SKILL.md:114`.

[CODE-VERIFIED] Existing routing tests require `/sc:agent` to remain represented in “Other commands” and verify named command files exist. They do not establish that a model correctly distinguishes this controller from a protocol dispatcher or an implementation executor. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:26-41,275-283`.

### Proposed recommendation changes

[UNVERIFIED] **Proposed SHOULD:** In the source and plugin recommendation skill, replace the universal dispatcher claim with a conditional rule: inspect the selected command; follow an explicit skill activation when present; otherwise classify it as self-contained. A missing protocol skill must not disqualify a valid self-contained command. This proposal follows the existing verification-record model, not a new capability. Targets: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:114` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/SKILL.md:114`.

[UNVERIFIED] **Proposed SHOULD:** Refine the guide’s existing `/sc:agent` description, mirrored into the plugin guide: “General session controller: startup checks, then waits for a task. Use only when that controller is wanted; not a substitute for a written implementation plan or persisted task execution.” Keep it in “Other commands”; do not add a routing row. The paste-ready invocation remains simply `/sc:agent`. Grounding: command startup and implementation behavior cited above.

[UNVERIFIED] **Proposed MUST acceptance constraint:** Do not redirect ordinary implementation planning, report-only investigation, or explicit persisted-task execution into `/sc:agent`. Apply the user’s desired workflow-first policy through the governing implementation routes, not by promoting this general controller. The current guide still routes “many files”, “more than one session”, and “must not drift” to MDTM, so that broader policy change belongs to the consolidated specification rather than being claimed as current behavior. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:305-308`.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed regression cases:

1. An explicit request to start the general controller yields `/sc:agent`, no invented flags or protocol name, and describes startup-then-wait behavior.
2. A candidate-verification fixture marks this file `self-contained`, with no protocol skill and no documented flags.
3. A planned implementation involving several files selects the appropriate written-plan route, not `/sc:agent`; under the desired policy, file count or multiple sessions alone must not force MDTM.
4. A naturally parallel research request does not become a generic controller invocation merely because its name contains “agent”.
5. Explicit MDTM execution and workflow-plan resume retain their corresponding executors, not this controller.

## Gaps

[CODE-CONTRADICTED] The command says the plugin automatically launches `/sc:agent` at session start. The inspected plugin registration invokes a shell script, and that script prints status/service announcements without invoking the slash command. Do not repeat automatic-controller execution as a verified capability. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/agent.md:9`, `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/hooks/hooks.json:3-10`, and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/scripts/session-init.sh:5-30`. Correcting startup machinery itself is follow-up, not recommendation implementation.

[CODE-VERIFIED] The classifier has no session-controller key. Its parallel-agent key means independent-item processing and synthesis, not `/sc:agent`. Unknown requests can fall through to discovery; no additional fixed classifier key is justified here. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:50-67`.

[UNVERIFIED] No model-driven routing scenarios or startup execution were run. No installed legacy protocol behavior is asserted.

## Key Takeaways

[UNVERIFIED] **CHANGE, narrowly:** clarify self-contained command verification and optionally sharpen the existing guide description. **NO CHANGE** to `/sc:agent` implementation or its current non-default routing position: the six-month update was formatting only.

[UNVERIFIED] **MUST:** preserve correct executor/report-only boundaries and avoid invented flags or protocol capabilities. **SHOULD:** add the self-contained verification regression and mirror wording changes into plugin recommendation surfaces. **NONE:** new `/sc:agent` routing row, classifier key, keyword table, or dedicated cache mechanism.
