# Phase 0 — Surface Enumeration and Auggie Sweep

This reference documents the algorithm SKILL.md Phase 0 calls. SKILL.md owns the *when* and *why*; this file owns the *how*.

## Why enumeration is dynamic, not tabular

The previous version of this skill carried a hand-curated `keyword → command-category` mapping (a 10-row table covering ml/web/api/debug/performance/security/create/test/improve/learning). It went stale on every framework release. A live invocation missed `/sc:spec-panel` even though the command file was sitting in `src/superclaude/commands/spec-panel.md`. That single miss is the proximate reason this skill was rewritten.

The replacement is: enumerate the actual surface every invocation, rank with auggie, verify against source files. There is no list of "categories" in this skill, no synonyms, no keyword aliases. If a command exists in the surface, enumeration finds it; if it does not, the user is told so. That is the entire contract.

## Glob set

Run these globs in parallel. Each line below is one Glob call:

| Surface | Glob pattern |
|---|---|
| Commands | `src/superclaude/commands/*.md` |
| Skills (src-of-truth) | `src/superclaude/skills/*/SKILL.md` |
| Skills (dev mirror) | `.claude/skills/*/SKILL.md` |
| Agents (src-of-truth) | `src/superclaude/agents/*.md` |
| Agents (dev mirror) | `.claude/agents/*.md` |
| Workflow templates | `src/superclaude/templates/workflow/*.md` |
| Document templates | `src/superclaude/templates/documents/*.md` |
| Example templates | `examples/*-template.md` |

If `src/superclaude/skills/*/SKILL.md` and `.claude/skills/*/SKILL.md` disagree, **trust `src/`** (source of truth per CLAUDE.md) and note the drift in `degradation_notes`. The user has bigger problems than a recommendation gap if their sync is broken; tell them.

### Worktree awareness

The current working directory may be a worktree under `.claude/worktrees/<name>/` rather than the main checkout. All Glob paths above are **relative to cwd**, not to `/config/workspace/IronClaude/`. Confirm cwd via `pwd` once at the start of Phase 0 if uncertain — the cost is a single Bash call.

## Auggie semantic-rank query (Step B)

One query. One. Iterating across files defeats the purpose of having auggie.

```text
mcp__auggie__codebase-retrieval(
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

For each candidate auggie ranks, before it is allowed into the recommendation:

1. **Direct Read** of the candidate's source file. Extract:
   - For commands: flag table (Options section), `## Required Input` rules (if any), `## Activation > Skill <name>` handoff, `## Boundaries`.
   - For skills: frontmatter (`name`, `description`, `allowed-tools`, `argument-hint`), Return Contract, Boundaries.
   - For agents: frontmatter `description` line + Tools list + Boundaries.
2. **Auggie record** — capture the usage notes, caveats, and related-skills auggie surfaced in Step B for this candidate.
3. **Outcome**:
   - Source resolved + auggie record present → full verified record. Proceed.
   - Source resolved + auggie unavailable / empty → degraded record. Emit the degradation notice in the output header.
   - Source missing → ghost candidate. Drop silently. Do not warn the user.

If the literal path misses but the name looks close (e.g., user said "deep research" and surface contains `deep-research-agent.md` and `deep-research.md`), run a `Grep -r <name> src/superclaude/` to rule out a rename before dropping.

## Verified candidate record (per surviving candidate)

Carry this record into Phase 1 (net-value evaluation) and Phase 2 (prompt construction):

```yaml
target: "sc:spec-panel"                       # canonical name
kind: "command"                                # command | skill | agent | template | native
source_path: "src/superclaude/commands/spec-panel.md"
activation_style: "skill-indirected"           # skill-indirected | self-contained | n/a
protocol_skill: "sc-spec-panel"                # if skill-indirected
flags:                                         # exact set from the source file
  - "--persona-architect"
  - "..."
required_inputs:                               # from a Required Input section, if any
  - "<file>"
return_contract: "<summary if present>"        # from skill frontmatter / return section
auggie_summary: |
  How this is actually used in the repo, common flag combos, related skills,
  caveats. "unavailable" if auggie skipped; "empty" if auggie returned nothing.
related: ["sc:reflect", "..."]                 # only what auggie surfaced AND was verified
caveats: "<one-line, or 'none surfaced'>"
```

Cache these records within a single `/sc:recommend` invocation keyed by `target`. Cache does not persist across invocations.

## Cardinality bound

- Hard cap: **3 candidates max** carried into Phase 2. The skill picks one as the primary recommendation; up to two more may appear as multi-path branches if and only if they reach the net-value bar (Phase 1) and represent a genuinely different approach (not a flag variation of the primary).
- Auggie calls per invocation: **1 in Step B**. No per-candidate auggie calls. (Step C uses Read, not auggie, because auggie's value was already extracted in Step B.)

## When to ask the user a clarifying question instead of guessing

If after Phase 0 Step B, auggie's top-ranked candidate has fit confidence < ~50% (the request was vague enough that 4+ candidates tied), **ask one clarifying question** rather than emitting a guess. The clarification cost is one short user turn; the cost of a wrong recommendation is the user re-asking from scratch.

Example clarification: "You said 'research how X works' — is X (a) a third-party library you want docs for, (b) something in this repo whose code paths you need traced, or (c) an external system you want compared against this repo's approach? Each maps to a different delegation."

Do not ask more than one clarifying question. If one is not enough, the request is too vague to recommend against; say so and ask the user to elaborate before invoking the skill again.
