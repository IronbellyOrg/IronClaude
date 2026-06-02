---
name: sc-recommend
description: "Build a refined, paste-ready prompt that hands the user's request off to the right local skill, command, agent, or native-tool sequence — only when delegation adds net value. Use this skill whenever the user asks 'which command should I use', 'how do I best prompt for X', 'help me invoke the right skill for Y', 'recommend a workflow for Z', or describes a task without naming a command. Also use proactively whenever the user pastes a goal that could plausibly map onto multiple skills/agents/commands in this repo and you would otherwise have to choose blindly. With --plugin, switches to ecosystem search (Claude plugin marketplaces + community skill repos) instead of the local project surface."
allowed-tools: Read, Glob, Grep, Bash, mcp__auggie__codebase-retrieval, mcp__tavily__tavily-search, mcp__tavily__tavily-extract, WebFetch, WebSearch
argument-hint: "[goal description] [--plugin]"
category: utility
---

# /sc:recommend — Refined-Prompt Builder

## Triggers

`sc-recommend` is invoked by the `/sc:recommend` command via its `## Activation` section. It is not invoked directly.

Activation conditions:

- User runs `/sc:recommend <goal>` in Claude Code
- `--plugin` flag may be passed to switch to ecosystem-search mode

## Purpose

Generate the **single best refined, paste-ready prompt** (occasionally a small set of clearly-distinguished prompts) that delegates the user's goal to whichever existing local skill / command / agent / native-tool sequence will execute it with the lowest waste and highest fidelity. Surface the project's *actual* current capability surface — not a stale mapping. Default to the smallest delegation that wins; recommend native tooling when delegation does not earn its overhead.

This skill **builds prompts**, it does not execute them. Output is a fenced prompt block the user can copy verbatim.

## Output

Every successful invocation emits one of:

1. **Refined-prompt block** — a fenced `text` block containing the paste-ready prompt to invoke a target skill/command/agent. Includes explicit parameters, deliverable shape, and file/agent handoffs. Single-line bash commands only (no heredocs, no `\` continuations); the prompt body itself may be multi-line because it is an argument string.
2. **Native-tooling recommendation** — when delegation adds no net value, a short paragraph naming the native tools (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`) and the order to run them in. No skill is invoked.
3. **Plugin-search result** (`--plugin` only) — one or more plugin/skill candidates with capability summary, install command, repo URL, and citations.

If multiple distinct paths are reasonable (e.g., "either /sc:tasklist or task-builder fits"), emit each as its own clearly-labeled prompt block with a one-line disambiguator — never as a flat "alternatives" list.

The skill never restates the target's internal logic (see Rule R3).

## Phase 0 — Mandatory Surface Enumeration + Auggie Sweep (GATE)

**Hard gate. Do not advance to Phase 1 until BOTH steps have landed or the documented degradation notice has been emitted.**

The old skill failed because its discovery layer was a hand-curated 10-row keyword table that went stale (it failed to surface `/sc:spec-panel` even though that command file was sitting in `src/superclaude/commands/`). The fix is to enumerate the actual surface every invocation and let auggie semantically rank it. There is no static mapping in this skill.

### Step A — Live surface enumeration (Glob)

Enumerate the project's *actual* current surface. Read every result lazily — Glob first, Read only what the candidate set later requires.

- `src/superclaude/commands/*.md` → live command index
- `src/superclaude/skills/*/SKILL.md` → live skill index
- `src/superclaude/agents/*.md` and `.claude/agents/*.md` → live agent index
- `src/superclaude/templates/**/*.md` and `examples/*-template.md` → templates

Commands are thin dispatchers that delegate to skills via `## Activation`. Treat `src/superclaude/commands/*.md` as the fast-path discovery surface for `/sc:*` slash commands.

If the user's cwd is a worktree under `.claude/worktrees/<name>/`, all paths above resolve relative to **that worktree**, not `/config/workspace/IronClaude/`. The skill must remain worktree-aware.

See `refs/surface-enumeration.md` for the full algorithm, the verification record schema, and worked examples.

### Step B — MANDATORY auggie semantic ranking

After enumeration, issue **one** `mcp__auggie__codebase-retrieval` query to semantically rank the enumerated surface against the user's request. Auggie is the speed lever: one semantic query ranks the whole surface; do not iterate file-by-file.

Query shape:

> Given the user request "<verbatim user request>", and the enumerated surface (commands: <names>; skills: <names>; agents: <names>; templates: <names>), rank the top 3-5 candidates by capability fit. For each, summarize: what it does, when it wins over native Read/Edit/Glob/Grep/Bash, what flags or required inputs it expects, and any known caveats or recent behavioral changes.

### Step C — Per-candidate verification (the prerequisite gate)

For each candidate auggie returns, **before** it is allowed into the recommendation:

1. **Direct read** — Read the candidate's source file (`src/superclaude/commands/<name>.md`, or `src/superclaude/skills/<name>/SKILL.md`, or `src/superclaude/agents/<name>.md`). Extract: flag table, required-input rules, activation handoff, return contract.
2. **Auggie record** — record the usage notes, related skills, and caveats auggie surfaced in Step B for this candidate.

A candidate that fails Step 1 (source file does not resolve) is a ghost. Drop it silently. Do not warn the user about candidates that did not survive verification; the user does not need that noise.

Verification is **exempt** for built-in tools (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch`) and for MCP server names referenced abstractly. Those have stable interfaces and verifying them adds overhead with no fabrication-risk return.

### Graceful degradation

| Failure | Response |
|---|---|
| Auggie MCP unavailable | Proceed with Glob+Read only. Emit a one-line header notice on the output: `Auggie unavailable — ranking falls back to literal Glob+Read; usage nuance may be thin.` Do not silently skip the gate. |
| Auggie returns empty | Note the gap in the output (`no auggie matches; ranking from file content only`) and proceed. The candidate may be new or rarely exercised — flag it rather than fake confidence. |
| Candidate source missing | Drop the candidate. Do not surface it. |
| User request is too vague to enumerate against | Ask one clarifying question. Do not emit a recommendation built on a guess. |

## Phase 1 — Net-Value Evaluation (anti-bloat default)

For **every** surviving candidate, answer explicitly before recommending:

1. Does invoking `<skill/agent/command>` add value beyond a 2-3 step Read/Grep/Glob/Edit/Write sequence?
2. Is the overhead (token cost of the skill body, subagent spawn time, protocol complexity, hook gates) justified by specialized capability the model lacks natively in this context?
3. Would a senior engineer reading the user's request choose this delegation, or roll the equivalent themselves in less time?

If the honest answer to any of these is "no" or "barely", **default to native tooling**. The skill is allowed — and expected — to emit:

> No skill/agent delegation adds net value here. Use Read on `<file>`, then Edit. Reason: <one-line why>.

as a complete, valid recommendation. Anti-bloat is **core**, not optional. A recommendation engine that recommends delegation reflexively trains users to over-invoke and burns tokens for no gain.

When delegation **does** win, the recommended prompt must invoke the smallest delegation that earns its cost. Prefer `/sc:<x>` → skill → agent over `/sc:<x>` → skill → agent → sub-skill chains unless the longer chain is the documented best path.

See `refs/delegation-vs-native-heuristics.md` for the full rubric (when commands beat skills, when skills beat agents, when parallel `Agent` calls beat sequential skills, when native is strictly best).

## Phase 2 — Refined Prompt Construction

Build the prompt as a **hand-off envelope**, not a specification. The prompt carries:

- the target invocation (`/sc:<command>` or `Skill <skill-name>` or `Agent <agent-name>` or native tool sequence)
- the user's verified parameters / file paths / flags
- the expected deliverable shape (what the user wants back)
- worktree-aware paths (relative to cwd if cwd is `.claude/worktrees/<name>/`)

The prompt MUST NOT restate the target's protocol logic — phase breakdown, scoring rules, agent roster, debate format, return contract internals. That belongs to the target skill. Trust the hand-off.

### Output template

````text
Goal: <one-line restatement of the user's intent>

Recommended delegation: <target name + why this wins net-value>

Paste-ready prompt:

```text
<the actual prompt — a hand-off envelope, not a specification>
```

Sources verified:

- <path/to/command.md> (Read)
- auggie semantic rank: <one-line summary>
````

If the recommendation is "use native tooling", drop the prompt block and emit the native-tool sequence as a numbered list instead.

## Phase 3 — `--plugin` Mode (ecosystem search)

When `--plugin` is set, **ignore the entire local surface enumeration** and search the plugin / community-skill ecosystem instead. Local skills and plugins must not bleed into each other's outputs.

In-scope sources (this configuration):

- Claude Code plugin marketplaces (`claude-plugins-official`, anthropic-managed listings)
- Community skill repos (`anthropic/skills`, `sammcj/agentic-tools`, etc.)

Out-of-scope (this configuration): raw MCP server marketplaces. Do not surface MCP servers under `--plugin` unless the user explicitly asks for one in their request.

Search via (in priority order): `tech-research` skill, the `deep-research` agent, or Tavily MCP directly. WebFetch / WebSearch are last-resort fallbacks.

For every candidate, return:

- plugin / skill name
- one-sentence capability summary
- install command (single-line bash)
- repo URL
- integration notes (what the user needs to wire up themselves)
- version / compatibility caveats
- citation (the URL the claim came from)

See `refs/plugin-ecosystem-sources.md` for the full source list, query patterns, and result-format template.

## Output Constraints — Anti-Fabrication Rules

These rules are non-negotiable. They survived from the old skill because they were the only parts that held up under scrutiny.

### Rule R1 — No unverified flags

A flag may appear in the recommended prompt **only if** it is present in the verified target's flag table (or `argument-hint`). Example: `/sc:adversarial` has a fixed flag set in `src/superclaude/commands/adversarial.md`; no flag may be attached to it that is not in that file. Fabricated flags (`--rounds`, `--measure-first`, `--verdict-per-claim`, etc., when they do not exist) are forbidden.

### Rule R2 — No unverified commands or skills

A command or skill may appear **only if** its source file was resolved in Phase 0 Step C. Auggie-mentioned but not file-resolved → drop. Memory-recalled but not file-resolved → drop.

### Rule R3 — No protocol reimplementation (the load-bearing rule)

When a verified target has `activation_style: skill-indirected` (its command file delegates to a protocol skill via `## Activation > Skill <name>`), the generated prompt MUST be a **hand-off**, not a **specification**.

- **Allowed**: `Run: /sc:adversarial --compare fileA.md,fileB.md --focus structure --depth standard`
- **Forbidden**: any inline content that restates the target's protocol — debate rules, phase counts, scoring formulas, "steelman strategy", artifact lists. The protocol skill owns that behavior; the prompt invokes and trusts.

R3 enforces: **invoke, don't reimplement**. Duplicating a target's protocol inline causes drift, wastes tokens, and produces prompts that disagree with the actual command when the command is run.

### Rule R4 — Built-ins exempt

`Read`, `Grep`, `Glob`, `Edit`, `Write`, `Bash`, `TodoWrite`, `WebFetch`, `WebSearch` are harness primitives. Recommend them by name without verification.

## Return Contract

| Field | Type | Description |
|---|---|---|
| `status` | string | `success`, `clarification_needed`, `degraded`, `plugin_search` |
| `mode` | string | `local` (default) or `plugin` |
| `recommendation_kind` | string | `delegation_prompt`, `native_tooling`, `multi_path`, `plugin_candidate` |
| `prompt_block` | string | The paste-ready prompt (empty for `native_tooling`) |
| `verified_sources` | list | Paths Read during Phase 0 Step C |
| `auggie_status` | string | `ok`, `unavailable`, `empty` |
| `degradation_notes` | string | One-line note when degraded |

## Boundaries

**Will:**

- Enumerate the live project surface (commands, skills, agents, templates) on every invocation
- Use auggie to semantically rank candidates against the user's request
- Verify every candidate against its source file before emitting
- Emit refined paste-ready prompts that hand off to existing skills/commands/agents
- Recommend native tooling when delegation does not add net value
- Switch to ecosystem search when `--plugin` is set
- Cite every source it read

**Will Not:**

- Use a static keyword → category mapping table (root cause of the old skill's discovery failure)
- Invent flags or commands not present in source files (R1, R2)
- Restate a target's protocol logic inline in the prompt (R3)
- Mix local-surface candidates with `--plugin` ecosystem results
- Execute the recommended prompt (the user pastes it manually)
- Estimate time, budget, or token cost (out of scope for prompt generation)
- Detect user language (English-only — Turkish detection from old skill is dropped)
- Detect project framework from file system heuristics (this skill ships in the SuperClaude repo; the relevant context is the source tree, not which JS framework is present)

## Related References

- `refs/surface-enumeration.md` — Phase 0 glob set, auggie sweep algorithm, verification record schema
- `refs/delegation-vs-native-heuristics.md` — the net-value rubric (Phase 1)
- `refs/plugin-ecosystem-sources.md` — `--plugin` search targets and result template
