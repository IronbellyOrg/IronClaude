---
topic: "Design version 1 of a hook that uses Jev to fire BEFORE certain events and validate that the model about to be used is the one the defined rules require, and to REJECT the event when it is not (issue IronbellyOrg/IronClaude#546)"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-14T00:00:00Z
unattended: true
---

# Seed Brief: jev-model-validation-hook

## Problem Statement

A standing owner rule ("the Opus tier is for blind scoring only") lived only in conversation context. Long unattended stages were launched on Opus anyway (about 4.2 million Opus output tokens, issue #546). Version 1 must make one property mechanical: **the model that was requested or defined is always the model used, and any different model is rejected before the event runs.** The hook never chooses or changes a model. Choosing the best, fastest or cheapest model (version 2, dynamic routing, only for skills, agents or commands configured for it) is out of scope except for one short "room for version 2" section.

## Known Context

(Details and sources in `enrichment/codebase-context.md`.)

- Claude Code PreToolUse hooks see `tool_name` and `tool_input` (Bash `command`; Agent tool `model` alias parameter). They do not see: a Python subprocess that starts `claude`, the contents of a script run by `bash script.sh`, `/model` typed by a person (UNVERIFIED), frontmatter that applies inside Claude Code (agents, skills; only indirectly through the Agent call), or env overrides applied by the harness. `SubagentStart` has no model field. `claude --bare` children run no hooks.
- Claude Code has a native, in-process allowlist: `availableModels`, `deniedModels`, `enforceAvailableModels` (applies to `/model`, `--model`, `ANTHROPIC_MODEL`, settings, alias env redirects, subagent frontmatter, Agent `model` parameter, skill and command frontmatter). It is global and static (no per-stage roles); a managed list replaces lower layers; unmanaged lists concatenate.
- IronClaude hook layout: sources in `src/superclaude/hooks/scripts/`, registration in `src/superclaude/hooks/hooks.json`, installer `src/superclaude/cli/install_hooks.py` (script list plus ownership-aware settings merge), `make sync-dev` / `make verify-sync`, tests in `tests/hooks/`. Closest precedents: `require-orca-worktree-agent.sh` (awk tokenizer, fail open, documented ceilings) and `launch-level-guard.sh` (governed-session fail closed, TAMPER class, Blocked/Why/You-can message, 64 KB cap).
- Python launchers under `src/superclaude/cli/` start `claude` as a subprocess outside the Bash tool; launcher scripts under `.dev/` carry literal `--model` flags; agent frontmatter holds 11 `sonnet`, 2 `opus`, 3 gateway ids.
- On this host aliases resolve through env (`ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]` and so on), so alias and id must be canonicalised before comparing.
- Jev: fast (70 to 500 ms reported) and very cheap (about $0.000025 per call measured), good on short single-item judgments, poor on multi-hop reasoning, answers out-of-scope inputs unless a "none" option exists. Principle: policy stays in code; Jev answers narrow questions; code decides; Jev may only ever add a block, never allow.

## Constraints

- v1 scope only: enforce "requested or defined model is the one used". No model quality or cost judgment.
- Hook blocks with a clear reason (never silent) and never rewrites the model.
- Must state plainly what it cannot see; indirection (script containing `--model`, alias, env override) must be covered or explicitly listed as uncovered.
- Missing or malformed policy must fail safe in a documented way (per event).
- Fits the IronClaude layout: `src/superclaude/hooks/scripts/`, `hooks.json`, `install_hooks.py` list, `make sync-dev`, never edit `.claude/` by hand, installed primitives never name `src/superclaude/` paths; Python only via `uv`.
- Time cost per event must be small (existing Bash hooks have 1 to 5 s timeouts).

## Success Criteria

- Answers all eight questions: (1) events and what a hook can see, citing docs; (2) policy format, scope, storage, loading; (3) Jev versus code, latency, cost, failure behaviour per event, offline test plan on labelled historical calls; (4) rejection reporting and override recording; (5) bypass resistance; (6) time cost per event; (7) test plan and numbered testable requirements; (8) implementation plan in the IronClaude layout.
- One short section on leaving room for version 2.
- Numbered, individually testable requirements (REQ-xx) with a verification method each.

## Open Questions

- Does `UserPromptSubmit` fire for the `/model` built-in? (UNVERIFIED; design must work either way, for example by relying on `availableModels` for the interactive switch.)
- Can `availableModels` be injected per headless child through `--settings` (additive with user lists) so each stage gets its own allowlist? (UNVERIFIED.)
- Should enforcement default to governed sessions only (like launch-level-guard) or to all sessions? Which events fail closed?
- Is Jev needed in v1 at all, or only for the dynamic-flag residue?
