# DevOps Claude Plugin — Handoff

## High-Level Goal

We are designing and building a **single curated Claude Code plugin** for DevOps, infrastructure management, CI/CD, SRE workflows, and infra-framework development
This plugin will be built for and all work should be saved to /config/workspace/IronOps/.dev/releases/1.0/0.1
This plugin should provide a curated Claude Code experience for infrastructure repositories and CI/CD workspaces. It should bundle the most valuable skills, commands, agents, hooks, and supporting files from multiple upstream Claude Code framework repos — especially IronClaude — plus our own custom DevOps-specific additions.

## Important Product Direction

The plugin should be a **curated build-time aggregator**, not a runtime multi-repo puller.

Desired flow:

```text
IronClaude and other upstream repos
→ latest mainline checkout during build/CI
→ manifest allowlist selects specific files/directories
→ build system assembles one curated plugin
→ plugin marketplace/private plugin distribution publishes latest
→ all infra/CICD projects install or update that one plugin
```

Target experience for projects:

- Install one plugin only.
- Get a DevOps/infra-focused Claude Code environment.
- Do not expose every upstream command/agent/skill unless explicitly curated.
- Always pull latest from upstream mainline when rebuilding.
- Do not maintain local forks or modified copies of IronClaude files.

## Non-Negotiable Constraints

1. **IronClaude files are read-only upstream assets.**
   - We do not modify IronClaude files.
   - We do not patch IronClaude files.
   - We do not overlay changes onto IronClaude files.
   - IronClaude owns and maintains those files exclusively.

2. **Always latest mainline.**
   - We do not care about semantic version pinning for upstream files.
   - The builder should pull latest from the upstream mainline branch.
   - We may record source commit SHAs as provenance/debug metadata, but not as governance locks.

3. **Single curated plugin output.**
   - The target infra projects should consume one plugin, not a pile of upstream plugins.
   - The plugin may be published through the Claude Code plugin marketplace, private plugin registry, or Git-based install, depending on what is supported.

4. **Build-time multi-repo aggregation.**
   - The framework builder may pull files from IronClaude plus other future repos.
   - A manifest should define sources and selected imports.
   - The final plugin should contain only selected files/directories.

5. **No direct copying into each infra repo.**
   - Target projects should not vendor copied `.claude/` files directly.
   - Plugin distribution should be the boundary.

## Candidate Upstream Assets From IronClaude

These were previously identified as valuable for a DevOps/infra-focused framework.

### Agents

Strong candidates:

- `src/superclaude/agents/devops-architect.md`
- `src/superclaude/agents/system-architect.md`
- `src/superclaude/agents/security-engineer.md`
- `src/superclaude/agents/root-cause-analyst.md`
- `src/superclaude/agents/performance-engineer.md`
- `src/superclaude/agents/backend-architect.md`
- `src/superclaude/agents/quality-engineer.md`
- `src/superclaude/agents/pm-agent.md`
- `src/superclaude/agents/self-review.md`
- `src/superclaude/agents/technical-writer.md`
- `src/superclaude/agents/requirements-analyst.md`

Likely skip initially:

- `frontend-architect`
- `business-panel-experts`
- `socratic-mentor`
- `learning-guide`

### Skills

Strong candidates:

- `src/superclaude/skills/sc-crash-recovery/`
- `src/superclaude/skills/sc-troubleshoot-protocol/`
- `src/superclaude/skills/sc-cli-portify-protocol/`
- `src/superclaude/skills/task-builder/`
- `src/superclaude/skills/task/`
- `src/superclaude/skills/tech-research/`
- potentially `src/superclaude/skills/prd/`
- potentially `src/superclaude/skills/tdd/`
- potentially `src/superclaude/skills/tech-reference/`

For the spec/design phase, `prd`, `tdd`, `tech-research`, and `task-builder` may be especially useful even if the runtime plugin eventually focuses more narrowly on infra operations.

### Commands

Strong candidates:

- `src/superclaude/commands/troubleshoot.md`
- `src/superclaude/commands/git.md`
- `src/superclaude/commands/cli-portify.md`
- `src/superclaude/commands/cleanup-audit.md`
- `/sc:task`, if present in the repo
- `/sc:research`, if present in the repo
- `/sc:test`, if appropriate
- `/sc:implement`, if appropriate
- `/sc:workflow`, if appropriate
- `/sc:spawn`, if appropriate

The command recommender pattern may also be useful:

- `/sc:recommend`
- `sc:recommend-protocol`

But recommendations must verify commands/flags against authoritative source files before suggesting them.

### Hooks

Strong candidates:

- `src/superclaude/hooks/hooks.json`
- `src/superclaude/hooks/scripts/freshness-session-start.sh`
- `src/superclaude/hooks/scripts/freshness-user-prompt.sh`
- `src/superclaude/hooks/scripts/freshness-pre-edit.sh`
- `src/superclaude/hooks/scripts/freshness-post-read.sh`
- `src/superclaude/hooks/scripts/freshness-subagent-start.sh`
- `src/superclaude/hooks/scripts/freshness-subagent-stop.sh`
- `src/superclaude/hooks/scripts/freshness-file-changed.sh`
- `src/superclaude/hooks/scripts/reject-workspace-writes.sh`
- `src/superclaude/hooks/scripts/auggie-flag-clear.sh`

Important hook design note:

- Do not blindly merge multiple upstream `hooks.json` files.
- The curated framework should probably own the final generated `hooks.json`.
- Upstream hook scripts can be imported as assets.
- The builder should validate hook references.

### Supporting Core Files

Potentially useful:

- `src/superclaude/pm_agent/confidence.py`
- `src/superclaude/pm_agent/self_check.py`
- `src/superclaude/execution/parallel.py`
- `src/superclaude/core/CLAUDE.md`
- `src/superclaude/core/PRINCIPLES.md`

Need to determine whether these belong in the plugin itself, in build tooling, or only as design references.

## Recommended Architecture To Explore

Possible repository layout:

```text
/config/workspace/IronOps
├── manifest.yaml
├── sources/
│   └── optional local checkout/cache
├── src/
│   └── custom/
│       ├── agents/
│       ├── skills/
│       ├── commands/
│       └── hooks/
├── scripts/
│   ├── fetch_sources.py
│   ├── build_plugin.py
│   └── verify_plugin.py
├── plugin/
│   └── generated curated plugin
├── dist/
│   └── packaged plugin artifact
├── tests/
├── docs/
└── README.md
```

Conceptual manifest:

```yaml
sources:
  ironclaude:
    repo: git@github.com:IronbellyOrg/IronClaude.git
    branch: master

  sre_pack:
    repo: git@github.com:ORG/claude-sre-pack.git
    branch: main

imports:
  - source: ironclaude
    from: src/superclaude/agents/devops-architect.md
    to: agents/devops-architect.md

  - source: ironclaude
    from: src/superclaude/skills/sc-troubleshoot-protocol/
    to: skills/sc-troubleshoot-protocol/

  - source: sre_pack
    from: skills/incident-response/
    to: skills/incident-response/
```

Generated provenance metadata should record source repo, branch, commit SHA, and generated timestamp for debugging, even though we always consume latest.

## Known Risks / Design Questions

Please explore these during brainstorming/specification:

1. What is the current Claude Code plugin marketplace/plugin packaging format?
2. Can a plugin contain agents, skills, commands, hooks, scripts, templates, and core rules?
3. How do plugin updates work?
4. Can plugins declare dependencies?
5. Can plugins define hooks safely?
6. How are command/agent/skill name collisions handled?
7. Should this be one plugin forever or one initial monolith that can later split?
8. What validation should the builder perform before publishing?
9. How should multiple upstream repos be represented in the manifest?
10. How should final `hooks.json` be generated?
11. How should command-to-skill dependencies be discovered or declared?
12. How should the plugin expose provenance/build metadata?
13. What should be custom to this framework versus imported from IronClaude?
14. Should `/sc:recommend` or an equivalent command be included to help users discover curated workflows?
15. Should there be a custom onboarding command, doctor command, or project bootstrap command?

## Desired First Outcome

Do not start implementation immediately.

Start with **interactive brainstorming and spec work**.

I want you to help produce, in order:

1. A short decision brief comparing:
   - direct upstream plugin dependencies
   - one curated aggregator plugin
   - multiple focused plugins
   - simple file-copy installer

2. A recommended product direction.

3. A PRD for the curated DevOps Claude plugin.

4. A TDD / architecture design for:
   - multi-source manifest
   - source fetching
   - plugin assembly
   - validation
   - plugin publishing/update flow
   - provenance metadata
   - hook generation
   - collision/dependency checks

5. A follow-up implementation task plan only after the PRD/TDD are approved.

## Suggested Claude Code Workflow

If available in this environment, use the most appropriate commands/skills/agents rather than improvising everything inline.

Strongly consider:

- `/sc:recommend` or `sc:recommend-protocol` first, to recommend the correct workflow.
  - If using `/sc:recommend`, obey its rule: verify every shortlisted command/skill by reading its authoritative source file and using codebase retrieval for project-specific context before recommending it.
- `tech-research` to research the current Claude Code plugin format and marketplace behavior.
- `prd` to create the Product Requirements Document.
- `tdd` to convert the approved PRD into a technical design.
- `task-builder` only after the spec/design are approved.
- `requirements-analyst` for clarifying questions and scope shaping.
- `system-architect` for plugin architecture.
- `devops-architect` for CI/build/publishing workflow.
- `security-engineer` for hook safety, secrets handling, and supply-chain risk.
- `quality-engineer` for validation gates and test strategy.
- `technical-writer` for user-facing install/update docs.

## Operating Instructions

1. Begin by asking focused clarifying questions only where needed.
2. Prefer evidence over assumptions.
3. Inspect authoritative repo files before making claims about existing commands, skills, agents, hooks, or plugin structure.
4. Use codebase retrieval for broad context where useful.
5. Do not recommend nonexistent flags, commands, skills, agents, or plugin capabilities.
6. If Claude Code plugin marketplace details are not available locally, perform external research or explicitly mark assumptions.
7. Do not write implementation code until the product direction and spec are accepted.
8. Keep the experience centered on DevOps, infra management, CI/CD, SRE, security, incident response, and framework operations.
9. Remember: upstream files are included unchanged; custom behavior belongs in our own plugin files or build system, not in modified IronClaude files.

Please start by recommending the best discovery/specification workflow for this effort, then begin the interactive requirements questions.
