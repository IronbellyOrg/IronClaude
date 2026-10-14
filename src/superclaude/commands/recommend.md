---
name: sc:recommend
description: "Build a refined, paste-ready prompt that delegates the user's goal to the right local skill, command, agent, or native-tool sequence — or, with --plugin, searches the Claude plugin / community skill ecosystem instead."
category: utility
complexity: standard
mcp-servers: [auggie, tavily]
personas: []
argument-hint: "<goal description> [--plugin] [--eval <mode>] [--minstar <N>]"
---

# /sc:recommend — Refined-Prompt Builder

## Triggers

- User asks "which command should I use?" or "what skill fits this?"
- User describes a goal without naming a specific command or skill
- User pastes a task that could plausibly map onto multiple skills/agents/commands
- User invokes `/sc:recommend <goal>` explicitly
- User adds `--plugin` to search the plugin ecosystem instead of the local project surface

## Usage

```bash
/sc:recommend <goal description>
/sc:recommend <goal description> --plugin
/sc:recommend <goal description> --plugin --minstar 1000
/sc:recommend <goal description> --eval quick
```

### Flags

| Flag | Description |
|------|-------------|
| `--plugin` | Ignore the local project surface; search the Claude Code plugin marketplace + community skill repos instead. Out: install commands, repo URLs, capability summaries, citations. |
| `--eval <mode>` | **Opt-in** per-row `best_model` evaluation, triggered on a cold-path cache insert. Modes: `none` (default — no eval), `quick` (opus ×1), `normal` (opus+sonnet ×2 each), `deep` (opus+sonnet+haiku ×3 each). Spawns parallel per-model subagents, grades their deliverables, aggregates per-model metrics, and writes a deterministic `best_model` into the lookup row. Auto-eval was rejected — evaluation runs **only** when `--eval` is passed. |
| `--minstar <N>` | **`--plugin` mode only.** Minimum GitHub-star floor a candidate repo must meet to appear in the primary results. Default **500** — the floor applies even when the flag is omitted. Surviving GitHub candidates are sorted by stars descending; credible candidates with no own-repo star count (Anthropic-curated marketplace entries, non-GitHub sources, or skills nested inside a larger repo) are not dropped but moved to a separate "Bonus — not ranked by GitHub stars" section. `--minstar 0` disables the floor. Must be a non-negative integer. In default (local) mode `--minstar` has no stars to act on, so it is **warned-and-ignored**. |

`--plugin`, `--eval`, and `--minstar` are the only flags. The skill picks the smallest delegation that wins; there is no `--alternatives` (multi-path output is automatic when two paths are genuinely distinct), no `--estimate`, no `--stream`, no `--community`, no `--maxstar`, no `--sort`, no language toggle.

## Behavioral Summary

`/sc:recommend` generates a **paste-ready prompt** that hands the user's goal off to the right delegation — or recommends native `Read`/`Edit`/`Glob`/`Grep`/`Bash` when no delegation adds net value. Every invocation:

1. Reads the routing guide first (`~/.claude/HOW-WE-WORK.md`, else the skill's `refs/HOW-WE-WORK.md` in a plugin install, else `src/superclaude/core/HOW-WE-WORK.md`; inside an IronClaude checkout, where `src/superclaude/commands/` exists under `git rev-parse --show-toplevel`, the `src/` copy is read first); when a routing row matches the goal, returns that row's steps in order with their mandatory flags. Then enumerates the installed (`~/.claude/`), project (`.claude/`), plugin and (in an IronClaude checkout) `src/` surface (commands, skills, agents, templates). No hand-written keyword table.
2. Issues one `mcp__auggie__codebase-retrieval` query to semantically rank candidates against the verbatim user request, except in matched mode (a routing row matched in step 1), where the query is skipped and the row's steps are verified directly.
3. Reads each candidate's source file before it is allowed into the recommendation.
4. Evaluates whether the chosen delegation earns its overhead vs. native tooling, and falls back to native when it does not.
5. Emits a hand-off envelope — never restates the target's protocol logic inline.

With `--plugin`, steps 1-3 are replaced by an ecosystem search (Claude plugin marketplaces + community skill repos like `anthropic/skills`). Local skills and plugins do not bleed into each other's output.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:

> Skill sc-recommend

Do NOT proceed using only this command file. The full behavioral specification — Phase 0 surface enumeration, Phase 1 net-value evaluation, Phase 2 refined-prompt construction, Phase 3 `--plugin` ecosystem search, anti-fabrication rules R1-R4 — is in the protocol skill.

A PreToolUse hook (`sc-recommend-phase0.sh`) defense-in-depths the Phase 0 gate at the moment the Skill tool is invoked. Even under context pressure, the gate cannot be silently skipped.

## Examples

### Local recommendation (default mode)

```bash
/sc:recommend "Critique this release spec before we build it: docs/specs/release-spec.md"

# Output (illustrative — actual paths/flags verified at runtime):
#   Level: not on the six-level scale (a supporting task) — guide section 3.6, row `critique-spec`
#   Changes files: no
#   Run these in order:
#   1. /sc:spec-panel @docs/specs/release-spec.md --mode critique
```

### Native-tooling fallback (anti-bloat default)

```bash
/sc:recommend "Rename the local variable tz_offest to tz_offset in src/utils/timefmt.py (3 uses)"

# Output (illustrative):
#   Level: 2 — guide section 1, 3.3, row `small-change`
#   (1 source file, 5 edits or fewer, exact change known: no skill adds net value)
#   Changes files: yes
#   Run these in order:
#   1. a plain edit: Read src/utils/timefmt.py, then Edit the 3 uses
#   2. run the related test
```

### Plugin / community-skill search

```bash
/sc:recommend "Find a Claude Code plugin for Notion sync" --plugin

# Output: top 3 candidates from the Claude plugin marketplace + anthropic/skills,
# each with install command, repo URL, version, integration notes, and citations.
```

### Plugin search with a higher popularity floor

```bash
/sc:recommend "Find a Claude Code plugin for Notion sync" --plugin --minstar 2000

# Output: primary section lists only repos with >= 2000 GitHub stars, sorted by
# stars descending; a "Bonus — not ranked by GitHub stars" section lists credible
# curated/non-GitHub/nested candidates separately. (Omit --minstar to use the
# default 500 floor; --minstar 0 disables the floor entirely.)
```

## Boundaries

**Will:**

- Read the routing guide first, then enumerate the live surface on every invocation
- Use auggie to semantically rank candidates against the user's request
- Verify every candidate against its source file before emitting it
- Emit refined paste-ready prompts that invoke existing skills/commands/agents
- Recommend native tooling when delegation does not add net value
- Switch to ecosystem search when `--plugin` is set
- Apply a minimum-star floor (default 500) and sort by stars in `--plugin` mode, with a separate bonus section for credible candidates that have no own-repo star count
- Warn and ignore `--minstar` in default (local) mode, where there are no stars to filter on
- Cite every source it read

**Will Not:**

- Keep a hand-written keyword → category mapping of its own (the guide's routing table is the only fixed routing source)
- Recommend flags or commands not present in a verified source file (Rule R1, R2)
- Restate a target skill's protocol logic inline in the generated prompt (Rule R3)
- Mix local-surface candidates with `--plugin` ecosystem results
- Execute the recommended prompt (the user pastes it manually)
- Estimate time, budget, or token cost
- Detect user language or project framework via file-system heuristics

## Output Constraints

- Single-line bash for any install / invocation commands embedded in the output (project memory: terminals cannot paste heredocs or `\` continuations). The prompt block itself may be multi-line because it is an argument string passed to the next tool, not a shell command.
- Paths are absolute or repo-relative and worktree-aware. When cwd is `.dev/worktrees/<name>/`, paths resolve against the worktree, not the main checkout.
- No emojis in any output (project convention).
