# Model tiers and worker pinning

Loaded before the first worker spawn of either mode.

Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model` parameter.

Workers are the agent files `~/.claude/agents/issue-worker-t3.md`, `~/.claude/agents/issue-worker-t2.md` and `~/.claude/agents/issue-worker-t1.md`; Claude Code reads the project `.claude/agents/` copy first when one exists. Workers run `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout).

## Tier map (default D3)

| Tier | Picker ID pinned in agent frontmatter | Agent | Used for |
|---|---|---|---|
| T3 | `claude-gw-tier3` | `issue-worker-t3` | the first lookup on every claim and create (B13); quick-depth issue body |
| T2 | `claude-gw-tier2` | `issue-worker-t2` | accuracy check and summary on simple and medium claims; flag choice at quick depth when a flag is missing; validation of user-given flags at standard depth; standard-depth body. Next-step chains for simple work (B14) |
| T1 | `claude-gw-tier1b` | `issue-worker-t1` | accuracy check and summary on complex claims; flag choice at standard and deep depth when a flag is missing; the independent flag variant for the deep adversarial check; deep body. Next-step chains for medium and complex work (B14) |

Picker IDs are written without the `[1m]` context suffix (default D19).

## Why the pin lives in frontmatter

Verified against the Claude Code subagent docs (`https://code.claude.com/docs/en/sub-agents`, read 2026-11-04):

1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the agent file's `model:` frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main session's model.
2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It cannot carry a picker ID, and if passed it overrides the frontmatter.
3. Frontmatter `model:` accepts an alias, a full model ID (the same values as the `--model` flag) or `inherit`.
4. The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Inside a ccsession tier workspace the launcher sets that variable to `claude-gw-tier2` when the owner may use tier2 (`docs/reference/model-aliases.md`); otherwise, and outside a tier workspace, it follows the inherited `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Either way, "spawn with haiku" does not guarantee the T3 tier.

So each tier has its own agent file whose `model:` is the picker ID, and the spawn passes only `subagent_type`. The only fallback is from `issue-worker-t1` to `issue-worker-t2` (below): it switches to a sibling agent file with its own pin, so it never uses an alias and never needs the `model` parameter.

An installed mod whose `agent.spawn` hook sets a model overrides the pin (same docs page). The skill does not try to detect this; if a worker is served by the wrong model, look there first.

## `E-TIER-UNAVAILABLE` (default D4)

## T1 -> T2 fallback

Users in the Coder role Member see only tiers 2 to 4, so the ccsession proxy answers a request for `claude-gw-tier1b` with HTTP 400 `invalid_request_error` (message starts `ccsession tier1b:`). If a spawn of `issue-worker-t1` fails because its picker ID (`claude-gw-tier1b`) is not served to this user (the API error says the tier is not available or allowed, or the picker ID is not served), retry the same job exactly once with `subagent_type: issue-worker-t2`: same job, same inputs, same output paths, and still no `model` parameter. The spawn prompt of the retry names the line below and the files to put it in. If that run succeeds, continue as normal. The file the T2 worker writes says in its first lines:

```text
Handled by issue-worker-t2 (tier 2): tier1b is not available to this user.
```

In claim mode the line is also shown in the posted accuracy-check comment (optional line of `templates/accuracy-check-comment.md`) and in `issue-summary.md`; in create mode it goes in `flags.md` or `draft-notes.md`, whichever file the job writes. The fallback runs once per job and only for T1. There is no fallback for T3 or T2.

## `E-TIER-UNAVAILABLE` (default D4)

If a spawn of `issue-worker-t3` or `issue-worker-t2` fails because its picker ID is not served (for example, outside a ccsession tier workspace), or the T2 fallback run itself is not served, STOP `E-TIER-UNAVAILABLE`, naming the agent file and the picker ID, for example:

```text
E-TIER-UNAVAILABLE: ~/.claude/agents/issue-worker-t3.md pins claude-gw-tier3, which this session cannot serve.
```

There is no alias fallback (no retry with the `haiku`, `sonnet` or `opus` alias): a fallback to `haiku` follows `ANTHROPIC_DEFAULT_HAIKU_MODEL` and can land on a model of another tier or family than the pin, which defeats B13.

Within the scope of `tests/skills/test_model_alias_policy.py`, the issue workers are the files that pin a picker ID in frontmatter `model:`; the other agent, skill and command files that have a frontmatter `model:` line name an alias (`docs/reference/model-aliases.md`).

## Next-step tier (defaults D6 and D25)

The tier for the user's next-step chain is written into `next-steps.md` as its first line: `/model claude-gw-tier2` for simple work, `/model claude-gw-tier1b` for medium and complex work; the line also says to use `claude-gw-tier2` when `claude-gw-tier1b` is not in the user's `/model` list. The user runs the chain in their own session (B2, B14).
