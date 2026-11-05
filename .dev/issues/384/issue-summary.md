# Summary: #384 [FEATURE] Primitives need to use ccsession model aliases instead of CC defaults

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/384
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 40 hours

## What the issue asks for

Agents, commands, skills and the Python CLI should stop relying on Claude Code's plain `opus`, `sonnet` and `haiku` aliases, whose real model depends on workspace settings (here `haiku` is `glm-5.3`). The owner fixed the mapping on 2026-11-05: inside a ccsession tier workspace opus = `claude-gw-tier1a`, sonnet = `claude-gw-tier1b`, haiku = `claude-gw-tier2`; outside one, keep plain `opus`, `sonnet`, `haiku`. Python package code is in scope. The main design problem is that the Agent tool's `model` parameter accepts aliases only and agent frontmatter is static, so a mechanism (tier agent files, a session-level remap of `ANTHROPIC_DEFAULT_*_MODEL`, or install-time rendering) must be chosen before any edits; see the analysis.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/agents/*.md` (13 agents) and `skills/sc-bare-review/SKILL.md:5` | `model: sonnet` / `model: opus` frontmatter to map |
| `src/superclaude/agents/issue-worker-t1.md:6` (t2, t3) | existing picker-ID pin pattern |
| `src/superclaude/skills/sc-issue-protocol/refs/tiers.md:23-40` | how Claude Code resolves a subagent model; the Agent `model` parameter is alias-only; no-fallback precedent |
| `src/superclaude/skills/sc-adversarial-protocol/` (`SKILL.md:76,581,963,1022,1968`, `refs/agent-specs.md`) | `--agents model:persona` parsing, validation and Agent-tool dispatch used by brainstorm, roadmap, release-split, cli-eval |
| `src/superclaude/commands/brainstorm.md`, `skills/sc-brainstorm-protocol/` | default `--models opus,sonnet,haiku`, alias validation |
| `src/superclaude/commands/{roadmap,validate-roadmap,release-split,cli-eval,adversarial,recommend,troubleshoot,auggie-review}.md` and their protocol skills | defaults, examples, validation of model names |
| `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:84-89,380-381` | `--revagent` accepts only plain aliases |
| `src/superclaude/skills/sc-recommend/SKILL.md:73,332-334` | Haiku classifier spawn and eval fan-out per model |
| `src/superclaude/skills/sc-reflect-protocol/` | reviewer diversity by model class; mapping changes the class set |
| `src/superclaude/skills/sc-implement-protocol/refs/retry.md:162-185` | adviser model ladder; its env names (`T1_Model01`) do not match the Coder env (`T1Model01`), so the alias ladder always runs |
| `src/superclaude/skills/sc-issue-protocol/refs/chains.md:11-13,21` | `--models opus,sonnet` workaround in next-step chains |
| `src/superclaude/cli/roadmap/models.py:104-105,151-152`, `executor.py:3680-3685`, `commands.py:41,434` | default agents; `AgentSpec.id` feeds step ids and resume state |
| `src/superclaude/cli/recommend/eval_aggregate.py:16-21`, `commands.py:207`, `best_model.py:130` | eval panel models, stored as `best_model` |
| `src/superclaude/cli/reflect/runner.py:287-310`, `commands.py:31,359` | alias diversity count; hard-coded `claude-opus-4-8` default |
| `src/superclaude/cli/sprint/summarizer.py:47-51,330-331`, `aienv.py:43-47` | `--model sonnet` narrative call; alias rotation on exhaustion |
| `src/superclaude/cli/user_settings_defaults.json:3` | installed main-session default `opus[1m]` |
| `src/superclaude/cli/eval/suites/*.yaml` | eval prompts with `--agents opus,sonnet,haiku` |
| `src/superclaude/skills/ccsession-tag/` (`ccsession-models.json:70-121`, `models.py:469-479,843-863`, `MODEL-TIERS.md:35-42`) | READ-ONLY here (issue #315): tier definitions, tier-mode detection, picker IDs |
| `plugins/superclaude/` mirror | same aliases in brainstorm, recommend, sc-recommend, retry.md |
| `tests/skills/test_issue_worker_agents.py:21-25` and about 11 test files that pin aliases | test pattern to follow; tests to update |
| `docs/user-guide/commands.md`, `docs/user-guide/brainstorm.md`, developer guide | user-facing model documentation |

## Analysis

- [analyze-superclaude.md](analysis/analyze-superclaude.md): deep architecture pass over `src/superclaude/` with every selection site, the four selection surfaces, three mechanism options, and the sites the issue missed.
