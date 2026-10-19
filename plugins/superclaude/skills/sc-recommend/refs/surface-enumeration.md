# Phase 0 — Surface Enumeration and Auggie Sweep

This reference documents the algorithm SKILL.md Phase 0 calls. SKILL.md owns the *when* and *why*; this file owns the *how*.

## Why enumeration is dynamic, not tabular

The previous version of this skill carried a hand-curated `keyword → command-category` mapping (a 10-row table covering ml/web/api/debug/performance/security/create/test/improve/learning). It went stale on every framework release. A live invocation missed `/sc:spec-panel` even though the command file was sitting in `src/superclaude/commands/spec-panel.md`. That single miss is the proximate reason this skill was rewritten.

The replacement is: enumerate the actual surface every invocation, rank with auggie, verify against source files. There is no list of "categories" in this skill, no synonyms, no keyword aliases. If a command exists in the surface, enumeration finds it; if it does not, it is never recommended. That is the entire contract. The one fixed routing source is the routing table in the guide (`~/.claude/HOW-WE-WORK.md`), which SKILL.md Step 0 reads before this enumeration runs; this file never copies it.

## Glob set

Search these locations. List the `$HOME` locations with one Bash call that uses `find`, not shell globs (zsh aborts the whole command on an unmatched glob, and `2>/dev/null` cannot stop that): `find -L "$HOME/.claude/commands/sc" "$HOME/.claude/agents" -maxdepth 1 -name '*.md' 2>/dev/null; find -L "$HOME/.claude/skills" -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null; find -L "$HOME/.claude/templates" -name '*.md' 2>/dev/null`. Or resolve `$HOME` once and give Glob the absolute folder as `path`. Never put `~` in a Glob pattern. Run the project and checkout globs in parallel. Record the path where each name was found; Step C reads that path.

| # | Surface | Location | When |
|---|---|---|---|
| 1 | Installed commands | `$HOME/.claude/commands/sc/*.md` | always |
| 2 | Installed skills | `$HOME/.claude/skills/*/SKILL.md` | always |
| 3 | Installed agents | `$HOME/.claude/agents/*.md` | always |
| 4 | Installed templates | `$HOME/.claude/templates/**/*.md` | always |
| 5 | Project commands, skills, agents | `.claude/commands/**/*.md`, `.claude/skills/*/SKILL.md`, `.claude/agents/*.md` (cwd) | always |
| 6 | Plugin install | `${CLAUDE_PLUGIN_ROOT}/commands/*.md`, `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md`, `${CLAUDE_PLUGIN_ROOT}/agents/*.md` | only when the variable is expanded (plugin skill) |
| 7 | IronClaude source checkout | `src/superclaude/commands/*.md`, `src/superclaude/skills/*/SKILL.md`, `src/superclaude/agents/*.md`, `src/superclaude/templates/**/*.md`, `src/superclaude/examples/*-template.md` (repository root) | only inside an IronClaude checkout (`src/superclaude/commands/` exists under `git rev-parse --show-toplevel`) |

If the same name is found in several places: inside an IronClaude checkout trust `src/` (`.claude/` there is the `make sync-dev` mirror); otherwise prefer the project `.claude/` copy, then `$HOME/.claude/`, then the plugin. Note duplicates in `degradation_notes`.

### Worktree awareness

The current working directory may be a worktree under `.dev/worktrees/<name>/` rather than the main checkout. The checkout paths (row 7) resolve under the repository root (`git rev-parse --show-toplevel`); the project paths (row 5) are read from cwd. Inside a worktree under `.dev/worktrees/<name>/` that command returns the worktree's root, so both resolve against that worktree, not the main checkout. Run it once at the start of Phase 0 if uncertain — the cost is a single Bash call.

## Auggie semantic-rank query (Step B)

Skip this step in matched mode (SKILL.md Step 0 matched a routing row) and set `auggie_status: skipped`; Step A and Step C still run. Otherwise: one query. One. Iterating across files defeats the purpose of having auggie.

```text
mcp__auggie__augment_code_search(
  information_request: "Given the user request: '<verbatim user request>',
    and the project's enumerated surface (commands: <comma-separated names>;
    skills: <comma-separated names>; agents: <comma-separated names>;
    templates: <comma-separated names>), rank the top 3-5 candidates by
    capability fit for this specific request. For each candidate, return:
    (1) one-line summary of what it does;
    (2) when it wins over native Read/Edit/Glob/Grep/Bash;
    (3) required flags or inputs it expects;
    (4) any known caveats or recent behavioral changes;
    (5) related skills/commands typically paired with it in this repo.
    Do NOT invent candidates not in the enumerated list.",
  directory_path: "<absolute path to cwd>"
)
```

Keep the enumerated-surface list literal in the query — auggie has stronger grounding when shown the candidate set rather than asked to discover it.

## Per-candidate verification (Step C) — the prerequisite gate

For each candidate auggie ranks, before it is allowed into the recommendation (in matched mode, for each step's command or skill in the matched routing row, whether or not auggie would rank it):

1. **Direct Read** of the candidate's source file. Extract:
   - For commands: flag table (Options section), `## Required Input` rules (if any), `## Activation > Skill <name>` handoff, `## Boundaries`.
   - For skills: frontmatter (`name`, `description`, `allowed-tools`, `argument-hint`), Return Contract, Boundaries.
   - For agents: frontmatter `description` line + Tools list + Boundaries.
2. **Auggie record** (skip in matched mode) — capture the usage notes, caveats, and related-skills auggie surfaced in Step B for this candidate.
3. **Outcome**:
   - Source resolved + auggie record present → full verified record. Proceed.
   - Source resolved + matched mode (Step B skipped) → verified record with `auggie_summary: skipped`. Proceed. Emit no degradation notice.
   - Source resolved + auggie query failed (unavailable) / returned nothing (empty) → degraded record. Emit the degradation notice in the output header.
   - Source missing → ghost candidate. Drop silently. Do not warn the user. Exception: in matched mode a routing row's step is kept and marked `not installed: <name>` (SKILL.md Phase 2), never dropped.

If the literal path misses but the name looks close (e.g., user said "deep research" and surface contains `deep-research-agent.md` and `deep-research.md`), run a `Grep -r <name>` over the folder where the near-miss was found to rule out a rename before dropping.

## Verified candidate record (per surviving candidate)

Carry this record into Phase 1 (net-value evaluation) and Phase 2 (prompt construction):

```yaml
target: "sc:spec-panel"                       # canonical name
kind: "command"                                # command | skill | agent | template | native
source_path: "src/superclaude/commands/spec-panel.md"
activation_style: "self-contained"             # skill-indirected | self-contained | n/a
protocol_skill: null                           # the protocol skill name if skill-indirected
flags:                                         # exact set from the source file
  - "--mode"
  - "--experts"
  - "--focus"
  - "--iterations"
  - "--format"
required_inputs:                               # from a Required Input section, if any
  - "<file>"
return_contract: "<summary if present>"        # from skill frontmatter / return section
auggie_summary: |
  How this is actually used in the repo, common flag combos, related skills,
  caveats. "skipped" in matched mode (Step B not run); "unavailable" only if the
  auggie query failed; "empty" if auggie returned nothing.
related: ["sc:reflect", "..."]                 # only what auggie surfaced AND was verified
caveats: "<one-line, or 'none surfaced'>"
```

Cache these records within a single `/sc:recommend` invocation keyed by `target`. Cache does not persist across invocations.

## Cardinality bound

- Hard cap: **3 candidates max** carried into Phase 2. The skill picks one as the primary recommendation; up to two more may appear as multi-path branches if and only if they reach the net-value bar (Phase 1) and represent a genuinely different approach (not a flag variation of the primary). A matched routing row (SKILL.md Step 0) counts as one candidate; each of its steps is verified in Step C on its own.
- Auggie calls per invocation: **1 in Step B** (0 in matched mode, where Step B is skipped). No per-candidate auggie calls. (Step C uses Read, not auggie, because auggie's value was already extracted in Step B.)

## When to ask the user a clarifying question instead of guessing

If after Phase 0 Step B, auggie's top-ranked candidate has fit confidence < ~50% (the request was vague enough that 4+ candidates tied), **ask one clarifying question** rather than emitting a guess. The clarification cost is one short user turn; the cost of a wrong recommendation is the user re-asking from scratch.

Example clarification: "You said 'research how X works' — is X (a) a third-party library you want docs for, (b) something in this repo whose code paths you need traced, or (c) an external system you want compared against this repo's approach? Each maps to a different delegation."

Do not ask more than one clarifying question. If one is not enough, the request is too vague to recommend against; say so and ask the user to elaborate before invoking the skill again.
