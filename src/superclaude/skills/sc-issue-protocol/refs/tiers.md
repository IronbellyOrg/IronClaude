# Model tiers and worker pinning

Loaded before the first worker spawn of either mode.

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.

Workers are the agent files `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`; Claude Code reads the project `.claude/agents/` copy first when one exists. Workers run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout).

## Tier map (default D3)

| Tier | Picker ID pinned in agent frontmatter | Agent | Used for |
|---|---|---|---|
| T3 | `claude-gw-tier3` | `issue-worker-t3` | the first lookup on every claim and create (B13); quick-depth issue body |
| T2 | `claude-gw-tier2` | `issue-worker-t2` | accuracy check and summary on simple and medium claims; flag choice at quick depth when a flag is missing; validation of user-given flags at standard depth; standard-depth body. Next-step chains for simple work (B14) |
| T1 | `claude-gw-tier1a` | `issue-worker-t1` | accuracy check and summary on complex claims; flag choice at standard and deep depth when a flag is missing; the independent flag variant for the deep adversarial check; deep body. Next-step chains for medium and complex work (B14) |

Picker IDs are written without the `[1m]` context suffix (default D19).

## Why the pin lives in frontmatter

Verified against the Claude Code subagent docs (`https://code.claude.com/docs/en/sub-agents`, read 2026-11-04):

1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the agent file's `model:` frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main session's model.
2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It cannot carry a picker ID, and if passed it overrides the frontmatter.
3. Frontmatter `model:` accepts an alias, a full model ID (the same values as the `--model` flag) or `inherit`.
4. The `haiku` alias resolves through `ANTHROPIC_DEFAULT_HAIKU_MODEL`, which on this Coder workspace is `glm-5.3`. So "spawn with haiku" does not guarantee the T3 tier.

So each tier has its own agent file whose `model:` is the picker ID, and the spawn passes only `subagent_type`.

An installed mod whose `agent.spawn` hook sets a model overrides the pin (same docs page). The skill does not try to detect this; if a worker is served by the wrong model, look there first.

## `E-TIER-UNAVAILABLE` (default D4)

If a spawn fails because the picker ID is not served (for example, outside a ccsession tier workspace), STOP `E-TIER-UNAVAILABLE`, naming the agent file and the picker ID, for example:

```text
E-TIER-UNAVAILABLE: ~/.claude/agents/issue-worker-t3.md pins claude-gw-tier3, which this session cannot serve.
```

There is no alias fallback: a fallback to `haiku` can land on a non-Claude model (`glm-5.3` here), which defeats B13.

## Next-step tier (defaults D6 and D25)

The tier for the user's next-step chain is written into `next-steps.md` as its first line: `/model claude-gw-tier2` for simple work, `/model claude-gw-tier1a` for medium and complex work. The user runs the chain in their own session (B2, B14).
