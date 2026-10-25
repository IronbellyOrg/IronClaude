# Task 10: GPT T1 spawn-path verification (evidence only)

Date: 2026-10-25. Host: this worktree's Claude Code session.

## Attempt

1. Alias route: listed the alias environment variables of this session.
   - `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5[1m]`
   - `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5-5[1m]`
   - `ANTHROPIC_DEFAULT_HAIKU_MODEL=grok-4.7[1m]`
   - No `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` maps to a `gpt-` id.
2. Full-id route: the Agent tool's `model` input accepts only the enum `sonnet | opus | haiku | fable`; a full model id such as `gpt-6.1-sol` cannot be passed.
3. Inheritance: `ANTHROPIC_MODEL=gpt-6.1-sol[1m]` is set in the environment, but the session runs on `claude-opus-5-5[1m]` (the `/model` selection), and an Agent spawned without `model` inherits the parent model, so this does not give a GPT subagent.

## Result

No spawn path to a GPT T1 model is verified on this host. Value used in `refs/retry.md`:

GPT spawn path: none verified; family-fallback applies
